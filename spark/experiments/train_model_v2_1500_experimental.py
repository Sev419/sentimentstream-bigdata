"""Entrena modelos NLP experimentales con dataset v2 de 1500 registros.

Este script no pertenece al pipeline productivo. Solo lee datos de
data/experiments/dataset_v2/labeled/ y escribe resultados en
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

BASELINES = {
    "baseline_v1": {
        "descripcion": "Dataset v1 academico",
        "accuracy": 0.111111,
        "f1_ponderado": 0.066667,
    },
    "baseline_v2_300": {
        "descripcion": "Dataset v2 300 con enfoque conservador",
        "accuracy": 0.616667,
        "f1_ponderado": 0.622983,
    },
    "improved_v2_300": {
        "descripcion": "Dataset v2 300 con stopwords y features agresivas",
        "accuracy": 0.55,
        "f1_ponderado": 0.556099,
    },
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

    if df["texto"].astype(str).str.strip().eq("").any():
        raise ValueError("Existen textos vacios en el dataset experimental.")


def build_models() -> dict[str, Pipeline]:
    return {
        "naive_bayes": Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
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


def baseline_table(results: dict[str, object]) -> str:
    best_model = str(results["mejor_modelo"])
    best_metrics = results["modelos"][best_model]
    lines = [
        "| Referencia | Accuracy | F1 ponderado | Delta F1 vs mejor 1500 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, baseline in BASELINES.items():
        delta = round(float(best_metrics["f1_ponderado"]) - float(baseline["f1_ponderado"]), 6)
        lines.append(f"| {name} | {baseline['accuracy']} | {baseline['f1_ponderado']} | {delta} |")
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
    best_model = str(results["mejor_modelo"])
    best_metrics = metrics_by_model[best_model]
    confusion_sections = "\n\n".join(
        confusion_matrix_table(model_name, metrics)
        for model_name, metrics in metrics_by_model.items()
    )

    return f"""# Reporte Modelo V2 1500 Experimental

## Proposito

Entrenar modelos NLP experimentales con el dataset v2 de 1500 registros usando el enfoque conservador que funciono mejor en el experimento de 300 registros.

## Dataset

- Archivo: `{results["input_csv"]}`
- Total registros: `{results["total_registros"]}`
- Train: `{results["train_registros"]}`
- Test: `{results["test_registros"]}`
- Estratificacion: `{results["estratificacion"]}`

## Distribucion General

| Clase | Total | Train | Test |
| --- | ---: | ---: | ---: |
| negativo | {results["distribucion_total"]["negativo"]} | {results["distribucion_train"]["negativo"]} | {results["distribucion_test"]["negativo"]} |
| neutral | {results["distribucion_total"]["neutral"]} | {results["distribucion_train"]["neutral"]} | {results["distribucion_test"]["neutral"]} |
| positivo | {results["distribucion_total"]["positivo"]} | {results["distribucion_train"]["positivo"]} | {results["distribucion_test"]["positivo"]} |

## Enfoque

- Limpieza basica conservadora.
- Sin eliminacion agresiva de stopwords.
- TF-IDF con `ngram_range=(1, 2)`.
- Modelos simples: Naive Bayes y Logistic Regression.

## Modelos Evaluados

{metrics_table(metrics_by_model)}

## Mejor Modelo Experimental

- Modelo: `{best_model}`
- Accuracy: `{best_metrics["accuracy"]}`
- F1 ponderado: `{best_metrics["f1_ponderado"]}`

## Comparacion Contra Experimentos Previos

{baseline_table(results)}

## Matrices De Confusion

{confusion_sections}

## Archivos Generados

- Metricas JSON: `data/experiments/dataset_v2/reports/metricas_modelo_v2_1500_experimental.json`
- Predicciones test: `data/experiments/dataset_v2/reports/predicciones_modelo_v2_1500_experimental.csv`

## Nota De Aislamiento

Este entrenamiento solo lee `data/experiments/dataset_v2/labeled/` y solo escribe en `data/experiments/dataset_v2/reports/`.

No modifica `spark_processing/`, no conecta MongoDB, no guarda modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
"""


def main() -> None:
    root = project_root()
    input_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_labeled_1500.csv"
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_json = reports_dir / "metricas_modelo_v2_1500_experimental.json"
    report_md = reports_dir / "reporte_modelo_v2_1500_experimental.md"
    predictions_csv = reports_dir / "predicciones_modelo_v2_1500_experimental.csv"

    df = pd.read_csv(input_csv, encoding="utf-8")
    validate_dataset(df)
    df["texto_preprocesado"] = df["texto"].apply(preprocess_text)

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["sentimiento"],
    )

    metrics_by_model: dict[str, dict[str, object]] = {}
    prediction_columns = test_df[["id", "texto", "texto_preprocesado", "sentimiento"]].copy()

    for model_name, model in build_models().items():
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
        "estratificacion": True,
        "distribucion_total": {label: int((df["sentimiento"] == label).sum()) for label in LABELS},
        "distribucion_train": {label: int((train_df["sentimiento"] == label).sum()) for label in LABELS},
        "distribucion_test": {label: int((test_df["sentimiento"] == label).sum()) for label in LABELS},
        "baselines": BASELINES,
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
