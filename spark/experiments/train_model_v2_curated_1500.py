"""Entrena modelos NLP experimentales con dataset v2 curado de 1500 registros."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


REQUIRED_COLUMNS = ["id", "texto", "sentimiento", "fuente", "version"]
LABELS = ["negativo", "neutral", "positivo"]


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def preprocess_text(text: object) -> str:
    normalized = str(text).lower().strip()
    normalized = re.sub(r"[^a-záéíóúüñ\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def validate_dataset(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {missing}")
    invalid = sorted(set(df["sentimiento"].astype(str)) - set(LABELS))
    if invalid:
        raise ValueError(f"Etiquetas invalidas: {invalid}")
    if df["texto"].isna().any() or df["texto"].astype(str).str.strip().eq("").any():
        raise ValueError("Existen textos nulos o vacios")


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
                ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
            ]
        ),
    }


def evaluate(model: Pipeline, x_test: pd.Series, y_test: pd.Series) -> tuple[dict[str, object], list[str]]:
    predictions = model.predict(x_test)
    return (
        {
            "accuracy": round(float(accuracy_score(y_test, predictions)), 6),
            "precision_ponderada": round(float(precision_score(y_test, predictions, average="weighted", zero_division=0)), 6),
            "recall_ponderado": round(float(recall_score(y_test, predictions, average="weighted", zero_division=0)), 6),
            "f1_ponderado": round(float(f1_score(y_test, predictions, average="weighted", zero_division=0)), 6),
            "matriz_confusion": confusion_matrix(y_test, predictions, labels=LABELS).tolist(),
            "labels_matriz_confusion": LABELS,
        },
        list(predictions),
    )


def metrics_table(models: dict[str, dict[str, object]]) -> str:
    lines = [
        "| Modelo | Accuracy | Precision ponderada | Recall ponderado | F1 ponderado |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, metrics in models.items():
        lines.append(
            f"| {name} | {metrics['accuracy']} | {metrics['precision_ponderada']} | "
            f"{metrics['recall_ponderado']} | {metrics['f1_ponderado']} |"
        )
    return "\n".join(lines)


def confusion_table(name: str, metrics: dict[str, object]) -> str:
    matrix = metrics["matriz_confusion"]
    assert isinstance(matrix, list)
    lines = [
        f"### Matriz De Confusion - {name}",
        "",
        "| Real \\ Predicho | negativo | neutral | positivo |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, row in zip(LABELS, matrix):
        lines.append(f"| {label} | {row[0]} | {row[1]} | {row[2]} |")
    return "\n".join(lines)


def render_report(results: dict[str, object]) -> str:
    models = results["modelos"]
    assert isinstance(models, dict)
    best = str(results["mejor_modelo"])
    best_metrics = models[best]
    matrices = "\n\n".join(confusion_table(name, metrics) for name, metrics in models.items())
    return f"""# Reporte Modelo V2 Curated 1500

## Proposito

Entrenar modelos NLP con el dataset v2 curado de 1500 registros usando baseline conservador.

## Dataset

- Archivo: `{results["input_csv"]}`
- Total registros: `{results["total_registros"]}`
- Train: `{results["train_registros"]}`
- Test: `{results["test_registros"]}`
- Estratificacion: `{results["estratificacion"]}`

## Enfoque

- Preprocesamiento ligero.
- Sin eliminacion agresiva de stopwords.
- TF-IDF con `ngram_range=(1, 2)`.
- Modelos: Naive Bayes y Logistic Regression.

## Modelos Evaluados

{metrics_table(models)}

## Mejor Modelo Interno

- Modelo: `{best}`
- Accuracy: `{best_metrics["accuracy"]}`
- F1 ponderado: `{best_metrics["f1_ponderado"]}`

## Matrices De Confusion

{matrices}

## Nota De Aislamiento

Este entrenamiento solo lee `data/experiments/dataset_v2/labeled/` y solo escribe en `data/experiments/dataset_v2/reports/`.
No modifica ni integra el pipeline productivo.
"""


def main() -> None:
    root = project_root()
    input_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_curated_1500.csv"
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    metrics_json = reports_dir / "metricas_modelo_v2_curated_1500.json"
    report_md = reports_dir / "reporte_modelo_v2_curated_1500.md"

    df = pd.read_csv(input_csv, encoding="utf-8")
    validate_dataset(df)
    df["texto_preprocesado"] = df["texto"].apply(preprocess_text)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["sentimiento"])

    model_metrics: dict[str, dict[str, object]] = {}
    for name, model in build_models().items():
        model.fit(train_df["texto_preprocesado"], train_df["sentimiento"])
        metrics, _ = evaluate(model, test_df["texto_preprocesado"], test_df["sentimiento"])
        model_metrics[name] = metrics

    best = max(model_metrics, key=lambda name: (float(model_metrics[name]["f1_ponderado"]), float(model_metrics[name]["accuracy"])))
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
        "modelos": model_metrics,
        "mejor_modelo": best,
        "archivos_generados": {"metricas_json": str(metrics_json), "reporte_md": str(report_md)},
    }
    metrics_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text(render_report(results), encoding="utf-8")
    print(f"Metricas JSON: {metrics_json}")
    print(f"Reporte Markdown: {report_md}")
    print(f"Mejor modelo: {best}")
    print(f"F1 ponderado: {model_metrics[best]['f1_ponderado']}")


if __name__ == "__main__":
    main()
