"""Evalua modelo v2 curated contra validacion realistic."""

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
REFERENCES = {
    "v2_300": {"f1": 0.622983, "nota": "baseline interno 300"},
    "v2_1500_sintetico_externo": {"f1": 0.735499, "nota": "validacion externa previa"},
    "v2_curated_externo": {"f1": 0.932261, "nota": "validacion externa curated"},
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


def decision_text(f1_value: float) -> str:
    if f1_value >= 0.85:
        return "Recomendado para integracion controlada en una rama separada, manteniendo validaciones adicionales."
    if f1_value >= 0.75:
        return "Hay mejora, pero conviene revisar errores antes de integrar."
    return "No integrar. Se debe mejorar el dataset antes de promover el modelo."


def render_report(results: dict[str, object]) -> str:
    metrics = results["realistic_metrics"]
    assert isinstance(metrics, dict)
    matrix = metrics["matriz_confusion"]
    assert isinstance(matrix, list)
    f1_realistic = float(metrics["f1_ponderado"])
    return f"""# Reporte Validacion Realistic Modelo V2 Curated

## Proposito

Evaluar el modelo entrenado con `dataset_sentimientos_v2_curated_1500.csv` sobre un dataset realistic de 300 registros mas natural y menos estructurado.

## Entrenamiento

- Dataset entrenamiento: `{results["train_csv"]}`
- Registros entrenamiento: `{results["train_records"]}`
- Modelo: `logistic_regression`
- Vectorizacion: `TF-IDF ngram_range=(1, 2)`
- Limpieza: conservadora

## Dataset Realistic

- Dataset realistic: `{results["realistic_csv"]}`
- Registros: `{results["realistic_records"]}`
- Distribucion:
  - negativo: `{results["realistic_distribution"]["negativo"]}`
  - neutral: `{results["realistic_distribution"]["neutral"]}`
  - positivo: `{results["realistic_distribution"]["positivo"]}`

## Metricas Realistic

| Metrica | Valor |
| --- | ---: |
| Accuracy | {metrics["accuracy"]} |
| Precision ponderada | {metrics["precision_ponderada"]} |
| Recall ponderado | {metrics["recall_ponderado"]} |
| F1 ponderado | {metrics["f1_ponderado"]} |

## Comparacion Final

| Experimento | F1 | Nota |
| --- | ---: | --- |
| v2_300 | {REFERENCES["v2_300"]["f1"]} | {REFERENCES["v2_300"]["nota"]} |
| v2_1500 sintetico externo | {REFERENCES["v2_1500_sintetico_externo"]["f1"]} | {REFERENCES["v2_1500_sintetico_externo"]["nota"]} |
| v2_curated externo | {REFERENCES["v2_curated_externo"]["f1"]} | {REFERENCES["v2_curated_externo"]["nota"]} |
| v2_curated realistic | {metrics["f1_ponderado"]} | validacion realistic final |

## Matriz De Confusion Realistic

{matrix_table(matrix)}

## Recomendacion Tecnica Final

{decision_text(f1_realistic)}

## Nota De Aislamiento

Esta evaluacion solo lee y escribe dentro de `data/experiments/dataset_v2/`.

No modifica `spark_processing/`, no conecta MongoDB, no reemplaza modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
"""


def main() -> None:
    root = project_root()
    train_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_curated_1500.csv"
    realistic_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_realistic_validation.csv"
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_json = reports_dir / "metricas_modelo_v2_curated_realistic.json"
    report_md = reports_dir / "reporte_modelo_v2_curated_realistic.md"
    predictions_csv = reports_dir / "predicciones_modelo_v2_curated_realistic.csv"

    train_df = pd.read_csv(train_csv, encoding="utf-8")
    realistic_df = pd.read_csv(realistic_csv, encoding="utf-8")
    validate_dataset(train_df, "train")
    validate_dataset(realistic_df, "realistic")
    train_df["texto_preprocesado"] = train_df["texto"].apply(preprocess_text)
    realistic_df["texto_preprocesado"] = realistic_df["texto"].apply(preprocess_text)

    model = build_model()
    model.fit(train_df["texto_preprocesado"], train_df["sentimiento"])
    predictions = model.predict(realistic_df["texto_preprocesado"])
    y_true = realistic_df["sentimiento"]
    matrix = confusion_matrix(y_true, predictions, labels=LABELS).tolist()
    metrics = {
        "accuracy": round(float(accuracy_score(y_true, predictions)), 6),
        "precision_ponderada": round(float(precision_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "recall_ponderado": round(float(recall_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "f1_ponderado": round(float(f1_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "matriz_confusion": matrix,
        "labels_matriz_confusion": LABELS,
    }

    prediction_df = realistic_df[["id", "texto", "texto_preprocesado", "sentimiento"]].copy()
    prediction_df["prediccion_logistic_regression_curated"] = predictions
    prediction_df.to_csv(predictions_csv, index=False, encoding="utf-8")

    results: dict[str, object] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "train_csv": str(train_csv),
        "realistic_csv": str(realistic_csv),
        "train_records": int(len(train_df)),
        "realistic_records": int(len(realistic_df)),
        "realistic_distribution": {label: int((realistic_df["sentimiento"] == label).sum()) for label in LABELS},
        "references": REFERENCES,
        "realistic_metrics": metrics,
        "decision": decision_text(float(metrics["f1_ponderado"])),
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
    print(f"Predicciones realistic: {predictions_csv}")
    print(f"F1 realistic: {metrics['f1_ponderado']}")
    print(results["decision"])


if __name__ == "__main__":
    main()
