"""Entrenamiento experimental NLP para dataset v2.

Este script no pertenece al pipeline productivo de SentimentStream.
Solo lee data/experiments/dataset_v2/labeled/ y escribe reportes en
data/experiments/dataset_v2/reports/.
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
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


REQUIRED_COLUMNS = ["id", "texto", "sentimiento", "fuente", "version"]
LABELS = ["negativo", "neutral", "positivo"]
BASELINE_V1 = {
    "filas_usadas": 30,
    "accuracy": 0.111111,
    "f1_ponderado": 0.066667,
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def preprocess_text(text: object) -> str:
    normalized = str(text).lower().strip()
    normalized = re.sub(r"[^a-záéíóúüñ\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def validate_dataset(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Faltan columnas obligatorias: {missing_columns}")

    invalid_labels = sorted(set(df["sentimiento"].astype(str)) - set(LABELS))
    if invalid_labels:
        raise ValueError(f"Etiquetas invalidas encontradas: {invalid_labels}")

    if df["texto"].isna().any():
        raise ValueError("Existen textos nulos en el dataset experimental.")

    empty_texts = df["texto"].astype(str).str.strip().eq("")
    if empty_texts.any():
        raise ValueError("Existen textos vacios en el dataset experimental.")


def build_models() -> dict[str, Pipeline]:
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    return {
        "naive_bayes": Pipeline(
            steps=[
                ("tfidf", vectorizer),
                ("model", MultinomialNB()),
            ]
        ),
        "logistic_regression": Pipeline(
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
        ),
    }


def evaluate_model(model: Pipeline, x_test: pd.Series, y_test: pd.Series) -> tuple[dict[str, object], list[str]]:
    predictions = model.predict(x_test)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 6),
        "precision_ponderada": round(
            float(precision_score(y_test, predictions, average="weighted", zero_division=0)),
            6,
        ),
        "recall_ponderado": round(
            float(recall_score(y_test, predictions, average="weighted", zero_division=0)),
            6,
        ),
        "f1_ponderado": round(
            float(f1_score(y_test, predictions, average="weighted", zero_division=0)),
            6,
        ),
        "matriz_confusion": confusion_matrix(y_test, predictions, labels=LABELS).tolist(),
        "labels_matriz_confusion": LABELS,
    }
    return metrics, list(predictions)


def metrics_table(metrics_by_model: dict[str, dict[str, object]]) -> str:
    lines = [
        "| Modelo | Accuracy | Precision ponderada | Recall ponderado | F1 ponderado |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for model_name, metrics in metrics_by_model.items():
        lines.append(
            f"| {model_name} | {metrics['accuracy']} | {metrics['precision_ponderada']} | "
            f"{metrics['recall_ponderado']} | {metrics['f1_ponderado']} |"
        )
    return "\n".join(lines)


def confusion_matrix_table(model_name: str, metrics: dict[str, object]) -> str:
    matrix = metrics["matriz_confusion"]
    assert isinstance(matrix, list)
    lines = [
        f"### Matriz De Confusion - {model_name}",
        "",
        "| Real \\ Predicho | negativo | neutral | positivo |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, row in zip(LABELS, matrix):
        lines.append(f"| {label} | {row[0]} | {row[1]} | {row[2]} |")
    return "\n".join(lines)


def render_report(results: dict[str, object]) -> str:
    metrics_by_model = results["modelos"]
    assert isinstance(metrics_by_model, dict)

    confusion_sections = "\n\n".join(
        confusion_matrix_table(model_name, metrics)
        for model_name, metrics in metrics_by_model.items()
    )

    best_model = results["mejor_modelo"]
    best_metrics = metrics_by_model[str(best_model)]

    return f"""# Reporte Modelo V2 Experimental

## Proposito

Entrenar modelos NLP simples sobre el dataset experimental v2 de 300 registros, sin modificar el pipeline estable de SentimentStream.

## Dataset

- Archivo: `{results["input_csv"]}`
- Total registros: `{results["total_registros"]}`
- Train: `{results["train_registros"]}`
- Test: `{results["test_registros"]}`
- Estratificacion: `{results["estratificacion"]}`

## Distribucion General

| Clase | Registros |
| --- | ---: |
| negativo | {results["distribucion_total"]["negativo"]} |
| neutral | {results["distribucion_total"]["neutral"]} |
| positivo | {results["distribucion_total"]["positivo"]} |

## Modelos Evaluados

{metrics_table(metrics_by_model)}

## Mejor Modelo Experimental

- Modelo: `{best_model}`
- Accuracy: `{best_metrics["accuracy"]}`
- F1 ponderado: `{best_metrics["f1_ponderado"]}`

## Comparacion Contra Baseline V1

Baseline v1 conocido:

- Filas usadas: `{BASELINE_V1["filas_usadas"]}`
- Accuracy aproximado: `{BASELINE_V1["accuracy"]}`
- F1 ponderado aproximado: `{BASELINE_V1["f1_ponderado"]}`

Resultado v2 experimental:

- Filas usadas: `{results["total_registros"]}`
- Mejor accuracy: `{best_metrics["accuracy"]}`
- Mejor F1 ponderado: `{best_metrics["f1_ponderado"]}`

Esta comparacion es preliminar porque el dataset v2 es experimental y no esta integrado al pipeline productivo.

## Matrices De Confusion

{confusion_sections}

## Archivos Generados

- Metricas JSON: `data/experiments/dataset_v2/reports/metricas_modelo_v2_experimental.json`
- Predicciones test: `data/experiments/dataset_v2/reports/predicciones_modelo_v2_experimental.csv`

## Nota De Aislamiento

Este entrenamiento solo lee `data/experiments/dataset_v2/labeled/` y solo escribe en `data/experiments/dataset_v2/reports/`.

No modifica `spark_processing/`, no conecta MongoDB, no guarda modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
"""


def main() -> None:
    root = project_root()
    input_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_labeled_300.csv"
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_json = reports_dir / "metricas_modelo_v2_experimental.json"
    report_md = reports_dir / "reporte_modelo_v2_experimental.md"
    predictions_csv = reports_dir / "predicciones_modelo_v2_experimental.csv"

    df = pd.read_csv(input_csv, encoding="utf-8")
    validate_dataset(df)
    df["texto_preprocesado"] = df["texto"].apply(preprocess_text)

    stratify = df["sentimiento"] if df["sentimiento"].value_counts().min() >= 2 else None
    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=stratify,
    )

    models = build_models()
    metrics_by_model: dict[str, dict[str, object]] = {}
    prediction_columns = test_df[["id", "texto", "texto_preprocesado", "sentimiento"]].copy()

    for model_name, model in models.items():
        model.fit(train_df["texto_preprocesado"], train_df["sentimiento"])
        model_metrics, predictions = evaluate_model(
            model,
            test_df["texto_preprocesado"],
            test_df["sentimiento"],
        )
        metrics_by_model[model_name] = model_metrics
        prediction_columns[f"prediccion_{model_name}"] = predictions

    best_model = max(
        metrics_by_model,
        key=lambda name: (
            float(metrics_by_model[name]["f1_ponderado"]),
            float(metrics_by_model[name]["accuracy"]),
        ),
    )

    results: dict[str, object] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_csv": str(input_csv),
        "total_registros": int(len(df)),
        "train_registros": int(len(train_df)),
        "test_registros": int(len(test_df)),
        "estratificacion": stratify is not None,
        "distribucion_total": {label: int((df["sentimiento"] == label).sum()) for label in LABELS},
        "distribucion_train": {label: int((train_df["sentimiento"] == label).sum()) for label in LABELS},
        "distribucion_test": {label: int((test_df["sentimiento"] == label).sum()) for label in LABELS},
        "baseline_v1": BASELINE_V1,
        "modelos": metrics_by_model,
        "mejor_modelo": best_model,
        "archivos_generados": {
            "metricas_json": str(metrics_json),
            "reporte_md": str(report_md),
            "predicciones_csv": str(predictions_csv),
        },
    }

    metrics_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text(render_report(results), encoding="utf-8")
    prediction_columns.to_csv(predictions_csv, index=False, encoding="utf-8")

    print(f"Metricas JSON: {metrics_json}")
    print(f"Reporte Markdown: {report_md}")
    print(f"Predicciones test: {predictions_csv}")
    print(f"Mejor modelo: {best_model}")
    print(f"Accuracy: {metrics_by_model[best_model]['accuracy']}")
    print(f"F1 ponderado: {metrics_by_model[best_model]['f1_ponderado']}")


if __name__ == "__main__":
    main()
