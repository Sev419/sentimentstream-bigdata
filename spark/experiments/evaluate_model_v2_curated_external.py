"""Evalua modelo curado v2 1500 contra dataset externo."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline


REQUIRED_COLUMNS = ["id", "texto", "sentimiento", "fuente", "version"]
LABELS = ["negativo", "neutral", "positivo"]
PREVIOUS_RESULTS = {
    "v2_300": {"f1_externo": None, "f1_interno": 0.622983, "descripcion": "baseline 300 interno"},
    "v2_1500_sintetico": {"f1_externo": 0.735499, "f1_interno": 1.0},
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def preprocess_text(text: object) -> str:
    normalized = str(text).lower().strip()
    normalized = re.sub(r"[^a-záéíóúüñ\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def validate_dataset(df: pd.DataFrame, name: str) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"{name}: faltan columnas {missing}")
    invalid = sorted(set(df["sentimiento"].astype(str)) - set(LABELS))
    if invalid:
        raise ValueError(f"{name}: etiquetas invalidas {invalid}")
    if df["texto"].isna().any() or df["texto"].astype(str).str.strip().eq("").any():
        raise ValueError(f"{name}: textos nulos o vacios")


def build_model() -> Pipeline:
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
        ]
    )


def matrix_table(matrix: list[list[int]]) -> str:
    lines = [
        "| Real \\ Predicho | negativo | neutral | positivo |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, row in zip(LABELS, matrix):
        lines.append(f"| {label} | {row[0]} | {row[1]} | {row[2]} |")
    return "\n".join(lines)


def render_report(results: dict[str, object]) -> str:
    metrics = results["external_metrics"]
    assert isinstance(metrics, dict)
    matrix = metrics["matriz_confusion"]
    assert isinstance(matrix, list)
    f1_curated = float(metrics["f1_ponderado"])
    delta_vs_synthetic = round(f1_curated - float(PREVIOUS_RESULTS["v2_1500_sintetico"]["f1_externo"]), 6)
    success = f1_curated >= 0.78
    recommendation = (
        "No integrar aun al pipeline estable. Aunque el dataset curado mejora frente al sintetico en validacion externa, "
        "debe ampliarse con textos reales y revisar estabilidad antes de promoverlo."
        if success
        else "No integrar al pipeline estable. El resultado externo no alcanza el criterio F1 >= 0.78."
    )

    return f"""# Reporte Evaluacion Externa Modelo V2 Curated

## Proposito

Evaluar el modelo entrenado con `dataset_sentimientos_v2_curated_1500.csv` sobre el dataset externo existente, sin mezclar datos externos con entrenamiento.

## Dataset De Entrenamiento

- Archivo: `{results["train_csv"]}`
- Registros: `{results["train_records"]}`

## Dataset Externo

- Archivo: `{results["external_csv"]}`
- Registros: `{results["external_records"]}`
- Distribucion: negativo `{results["external_distribution"]["negativo"]}`, neutral `{results["external_distribution"]["neutral"]}`, positivo `{results["external_distribution"]["positivo"]}`

## Metricas Externas Curated

| Metrica | Valor |
| --- | ---: |
| Accuracy | {metrics["accuracy"]} |
| Precision ponderada | {metrics["precision_ponderada"]} |
| Recall ponderado | {metrics["recall_ponderado"]} |
| F1 ponderado | {metrics["f1_ponderado"]} |

## Comparacion Final

| Experimento | F1 externo | Nota |
| --- | ---: | --- |
| v2_300 | N/A | solo referencia interna F1 0.622983 |
| v2_1500 sintetico | {PREVIOUS_RESULTS["v2_1500_sintetico"]["f1_externo"]} | validacion externa previa |
| v2_curated_1500 | {metrics["f1_ponderado"]} | validacion externa actual |

- Delta F1 curated vs sintetico externo: `{delta_vs_synthetic}`
- Criterio de exito F1 >= 0.78: `{success}`

## Matriz De Confusion Externa

{matrix_table(matrix)}

## Recomendacion Tecnica

{recommendation}

## Nota De Aislamiento

Esta evaluacion solo lee y escribe dentro de `data/experiments/dataset_v2/`.

No modifica `spark_processing/`, no conecta MongoDB, no reemplaza modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
"""


def main() -> None:
    root = project_root()
    train_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_curated_1500.csv"
    external_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_external_validation.csv"
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_json = reports_dir / "metricas_modelo_v2_curated_external.json"
    report_md = reports_dir / "reporte_modelo_v2_curated_external.md"
    predictions_csv = reports_dir / "predicciones_modelo_v2_curated_external.csv"

    train_df = pd.read_csv(train_csv, encoding="utf-8")
    external_df = pd.read_csv(external_csv, encoding="utf-8")
    validate_dataset(train_df, "train")
    validate_dataset(external_df, "external")
    train_df["texto_preprocesado"] = train_df["texto"].apply(preprocess_text)
    external_df["texto_preprocesado"] = external_df["texto"].apply(preprocess_text)

    model = build_model()
    model.fit(train_df["texto_preprocesado"], train_df["sentimiento"])
    predictions = model.predict(external_df["texto_preprocesado"])
    y_true = external_df["sentimiento"]
    matrix = confusion_matrix(y_true, predictions, labels=LABELS).tolist()
    metrics = {
        "accuracy": round(float(accuracy_score(y_true, predictions)), 6),
        "precision_ponderada": round(float(precision_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "recall_ponderado": round(float(recall_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "f1_ponderado": round(float(f1_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "matriz_confusion": matrix,
        "labels_matriz_confusion": LABELS,
    }

    prediction_df = external_df[["id", "texto", "texto_preprocesado", "sentimiento"]].copy()
    prediction_df["prediccion_logistic_regression_curated"] = predictions
    prediction_df.to_csv(predictions_csv, index=False, encoding="utf-8")

    results: dict[str, object] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "train_csv": str(train_csv),
        "external_csv": str(external_csv),
        "train_records": int(len(train_df)),
        "external_records": int(len(external_df)),
        "external_distribution": {label: int((external_df["sentimiento"] == label).sum()) for label in LABELS},
        "previous_results": PREVIOUS_RESULTS,
        "external_metrics": metrics,
        "archivos_generados": {
            "metricas_json": str(metrics_json),
            "reporte_md": str(report_md),
            "predicciones_csv": str(predictions_csv),
        },
    }
    metrics_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text(render_report(results), encoding="utf-8")
    print(f"Metricas JSON: {metrics_json}")
    print(f"Reporte Markdown: {report_md}")
    print(f"Predicciones externas: {predictions_csv}")
    print(f"F1 externo curated: {metrics['f1_ponderado']}")


if __name__ == "__main__":
    main()
