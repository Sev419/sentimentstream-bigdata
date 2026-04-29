"""Evaluacion externa del modelo experimental v2 1500.

Entrena el mejor enfoque experimental sobre dataset_sentimientos_v2_labeled_1500.csv
y evalua exclusivamente sobre dataset_sentimientos_v2_external_validation.csv.
No modifica ni integra el pipeline productivo.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline


REQUIRED_COLUMNS = ["id", "texto", "sentimiento", "fuente", "version"]
LABELS = ["negativo", "neutral", "positivo"]
INTERNAL_V2_1500 = {
    "accuracy": 1.0,
    "f1_ponderado": 1.0,
    "modelo": "logistic_regression",
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def preprocess_text(text: object) -> str:
    normalized = str(text).lower().strip()
    normalized = re.sub(r"[^a-záéíóúüñ\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def validate_dataset(df: pd.DataFrame, name: str) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"{name}: faltan columnas obligatorias: {missing_columns}")

    invalid_labels = sorted(set(df["sentimiento"].astype(str)) - set(LABELS))
    if invalid_labels:
        raise ValueError(f"{name}: etiquetas invalidas encontradas: {invalid_labels}")

    if df["texto"].isna().any():
        raise ValueError(f"{name}: existen textos nulos.")

    if df["texto"].astype(str).str.strip().eq("").any():
        raise ValueError(f"{name}: existen textos vacios.")


def build_model() -> Pipeline:
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def render_confusion_matrix(matrix: list[list[int]]) -> str:
    lines = [
        "| Real \\ Predicho | negativo | neutral | positivo |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, row in zip(LABELS, matrix):
        lines.append(f"| {label} | {row[0]} | {row[1]} | {row[2]} |")
    return "\n".join(lines)


def render_report(results: dict[str, object]) -> str:
    external = results["external_metrics"]
    assert isinstance(external, dict)
    matrix = external["matriz_confusion"]
    assert isinstance(matrix, list)
    delta_f1 = round(float(external["f1_ponderado"]) - INTERNAL_V2_1500["f1_ponderado"], 6)

    recommendation = (
        "No integrar al pipeline estable. La validacion externa muestra degradacion frente al resultado interno, "
        "lo que confirma riesgo de sobreajuste a patrones sinteticos."
    )
    if float(external["f1_ponderado"]) >= 0.85:
        recommendation = (
            "Mantener como experimental. Aunque el resultado externo es alto, se recomienda ampliar validacion "
            "con textos reales antes de integrar."
        )

    return f"""# Reporte Validacion Externa Modelo V2 1500

## Proposito

Evaluar el modelo experimental v2 1500 contra un dataset externo/adversarial mas natural y menos estructurado.

## Entrenamiento

- Dataset entrenamiento: `{results["train_csv"]}`
- Registros entrenamiento: `{results["train_records"]}`
- Modelo: `logistic_regression`
- Vectorizacion: `TF-IDF ngram_range=(1, 2)`
- Limpieza: conservadora, sin stopwords agresivas

## Dataset Externo

- Dataset externo: `{results["external_csv"]}`
- Registros externos: `{results["external_records"]}`
- Distribucion externo:
  - negativo: `{results["external_distribution"]["negativo"]}`
  - neutral: `{results["external_distribution"]["neutral"]}`
  - positivo: `{results["external_distribution"]["positivo"]}`

## Comparacion Interna Vs Externa

| Evaluacion | Accuracy | F1 ponderado |
| --- | ---: | ---: |
| Interna v2 1500 | {INTERNAL_V2_1500["accuracy"]} | {INTERNAL_V2_1500["f1_ponderado"]} |
| Externa adversarial | {external["accuracy"]} | {external["f1_ponderado"]} |

- Delta F1 externo vs interno: `{delta_f1}`

## Metricas Externas

| Metrica | Valor |
| --- | ---: |
| Accuracy | {external["accuracy"]} |
| Precision ponderada | {external["precision_ponderada"]} |
| Recall ponderado | {external["recall_ponderado"]} |
| F1 ponderado | {external["f1_ponderado"]} |

## Matriz De Confusion Externa

{render_confusion_matrix(matrix)}

## Riesgo De Sobreajuste Sintetico

El resultado interno perfecto del dataset v2 1500 puede explicarse por patrones sinteticos muy separables. La validacion externa usa frases mas naturales, ambiguas y menos estructuradas para medir generalizacion fuera del patron de generacion.

## Recomendacion Tecnica

{recommendation}

## Archivos Generados

- `data/experiments/dataset_v2/reports/metricas_modelo_v2_external_validation.json`
- `data/experiments/dataset_v2/reports/predicciones_modelo_v2_external_validation.csv`

## Nota De Aislamiento

Esta evaluacion solo lee y escribe dentro de `data/experiments/dataset_v2/`.

No modifica `spark_processing/`, no conecta MongoDB, no reemplaza modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
"""


def main() -> None:
    root = project_root()
    train_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_labeled_1500.csv"
    external_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_external_validation.csv"
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_json = reports_dir / "metricas_modelo_v2_external_validation.json"
    report_md = reports_dir / "reporte_modelo_v2_external_validation.md"
    predictions_csv = reports_dir / "predicciones_modelo_v2_external_validation.csv"

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

    external_metrics = {
        "accuracy": round(float(accuracy_score(y_true, predictions)), 6),
        "precision_ponderada": round(float(precision_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "recall_ponderado": round(float(recall_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "f1_ponderado": round(float(f1_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "matriz_confusion": matrix,
        "labels_matriz_confusion": LABELS,
    }

    prediction_df = external_df[["id", "texto", "texto_preprocesado", "sentimiento"]].copy()
    prediction_df["prediccion_logistic_regression"] = predictions
    prediction_df.to_csv(predictions_csv, index=False, encoding="utf-8")

    results: dict[str, object] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "train_csv": str(train_csv),
        "external_csv": str(external_csv),
        "train_records": int(len(train_df)),
        "external_records": int(len(external_df)),
        "internal_v2_1500": INTERNAL_V2_1500,
        "external_distribution": {label: int((external_df["sentimiento"] == label).sum()) for label in LABELS},
        "external_metrics": external_metrics,
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
    print(f"Accuracy externo: {external_metrics['accuracy']}")
    print(f"F1 externo: {external_metrics['f1_ponderado']}")


if __name__ == "__main__":
    main()
