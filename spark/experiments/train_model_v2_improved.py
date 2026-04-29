"""Experimento NLP mejorado para dataset v2.

Este script no integra modelos al pipeline estable. Solo lee el dataset v2
experimental y escribe metricas/reporte en data/experiments/dataset_v2/reports/.
"""

from __future__ import annotations

import json
import re
import unicodedata
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
from sklearn.svm import LinearSVC


REQUIRED_COLUMNS = ["id", "texto", "sentimiento", "fuente", "version"]
LABELS = ["negativo", "neutral", "positivo"]
BASELINE_EXPERIMENTAL = {
    "descripcion": "train_model_v2_experimental.py",
    "f1_ponderado": 0.622983,
    "accuracy": 0.616667,
}

SPANISH_STOPWORDS = {
    "a",
    "al",
    "algo",
    "ante",
    "antes",
    "como",
    "con",
    "contra",
    "cual",
    "cuando",
    "de",
    "del",
    "desde",
    "donde",
    "durante",
    "e",
    "el",
    "ella",
    "ellas",
    "ellos",
    "en",
    "entre",
    "era",
    "es",
    "esa",
    "esas",
    "ese",
    "eso",
    "esos",
    "esta",
    "estaba",
    "estado",
    "estan",
    "estar",
    "este",
    "esto",
    "estos",
    "fue",
    "ha",
    "hay",
    "la",
    "las",
    "le",
    "lo",
    "los",
    "mas",
    "me",
    "mi",
    "mis",
    "muy",
    "no",
    "nos",
    "o",
    "para",
    "pero",
    "por",
    "porque",
    "que",
    "se",
    "sin",
    "sobre",
    "su",
    "sus",
    "tambien",
    "tiene",
    "un",
    "una",
    "uno",
    "y",
    "ya",
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(character for character in normalized if not unicodedata.combining(character))


def preprocess_text(text: object) -> str:
    normalized = strip_accents(str(text).lower().strip())
    normalized = re.sub(r"[^a-zñ\s]", " ", normalized)
    tokens = [token for token in normalized.split() if token not in SPANISH_STOPWORDS and len(token) > 1]
    return " ".join(tokens)


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
    vectorizer_params = {
        "ngram_range": (1, 2),
        "max_features": 2000,
        "min_df": 1,
        "sublinear_tf": True,
    }
    return {
        "naive_bayes": Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(**vectorizer_params)),
                ("model", MultinomialNB(alpha=0.5)),
            ]
        ),
        "logistic_regression": Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(**vectorizer_params)),
                (
                    "model",
                    LogisticRegression(
                        max_iter=1500,
                        class_weight="balanced",
                        C=2.0,
                        random_state=42,
                    ),
                ),
            ]
        ),
        "linear_svm": Pipeline(
            steps=[
                ("tfidf", TfidfVectorizer(**vectorizer_params)),
                (
                    "model",
                    LinearSVC(
                        C=1.0,
                        class_weight="balanced",
                        random_state=42,
                    ),
                ),
            ]
        ),
    }


def evaluate_model(model: Pipeline, x_test: pd.Series, y_test: pd.Series) -> tuple[dict[str, object], list[str]]:
    predictions = model.predict(x_test)
    return (
        {
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
        },
        list(predictions),
    )


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
    best_model = str(results["mejor_modelo"])
    best_metrics = metrics_by_model[best_model]
    baseline_f1 = float(BASELINE_EXPERIMENTAL["f1_ponderado"])
    improvement = round(float(best_metrics["f1_ponderado"]) - baseline_f1, 6)
    confusion_sections = "\n\n".join(
        confusion_matrix_table(model_name, metrics)
        for model_name, metrics in metrics_by_model.items()
    )

    return f"""# Reporte Modelo V2 Improved

## Proposito

Evaluar una mejora experimental de features para NLP sin modificar el pipeline estable.

## Mejoras Aplicadas

- Lower case.
- Normalizacion basica de acentos.
- Eliminacion de puntuacion.
- Eliminacion de stopwords en espanol.
- TF-IDF con `ngram_range=(1, 2)`.
- `max_features=2000`.

## Dataset

- Archivo: `{results["input_csv"]}`
- Total registros: `{results["total_registros"]}`
- Train: `{results["train_registros"]}`
- Test: `{results["test_registros"]}`
- Estratificacion: `{results["estratificacion"]}`

## Modelos Evaluados

{metrics_table(metrics_by_model)}

## Mejor Modelo Improved

- Modelo: `{best_model}`
- Accuracy: `{best_metrics["accuracy"]}`
- F1 ponderado: `{best_metrics["f1_ponderado"]}`

## Comparacion Contra Baseline Experimental

- Baseline F1 ponderado: `{BASELINE_EXPERIMENTAL["f1_ponderado"]}`
- Baseline accuracy: `{BASELINE_EXPERIMENTAL["accuracy"]}`
- Mejor F1 improved: `{best_metrics["f1_ponderado"]}`
- Diferencia F1: `{improvement}`

## Matrices De Confusion

{confusion_sections}

## Nota De Aislamiento

Este experimento solo lee `data/experiments/dataset_v2/labeled/` y solo escribe en `data/experiments/dataset_v2/reports/`.

No modifica `spark_processing/`, no conecta MongoDB, no reemplaza modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
"""


def main() -> None:
    root = project_root()
    input_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_labeled_300.csv"
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_json = reports_dir / "metricas_modelo_v2_improved.json"
    report_md = reports_dir / "reporte_modelo_v2_improved.md"

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

    metrics_by_model: dict[str, dict[str, object]] = {}
    for model_name, model in build_models().items():
        model.fit(train_df["texto_preprocesado"], train_df["sentimiento"])
        model_metrics, _ = evaluate_model(
            model,
            test_df["texto_preprocesado"],
            test_df["sentimiento"],
        )
        metrics_by_model[model_name] = model_metrics

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
        "features": {
            "preprocesamiento": [
                "lowercase",
                "normalizacion_acentos",
                "eliminacion_puntuacion",
                "stopwords_espanol",
            ],
            "tfidf": {
                "ngram_range": [1, 2],
                "max_features": 2000,
                "sublinear_tf": True,
            },
        },
        "baseline_experimental": BASELINE_EXPERIMENTAL,
        "modelos": metrics_by_model,
        "mejor_modelo": best_model,
        "comparacion": {
            "f1_baseline": BASELINE_EXPERIMENTAL["f1_ponderado"],
            "f1_mejor_improved": metrics_by_model[best_model]["f1_ponderado"],
            "delta_f1": round(
                float(metrics_by_model[best_model]["f1_ponderado"]) - float(BASELINE_EXPERIMENTAL["f1_ponderado"]),
                6,
            ),
        },
        "archivos_generados": {
            "metricas_json": str(metrics_json),
            "reporte_md": str(report_md),
        },
    }

    metrics_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    report_md.write_text(render_report(results), encoding="utf-8")

    print(f"Metricas JSON: {metrics_json}")
    print(f"Reporte Markdown: {report_md}")
    print(f"Mejor modelo: {best_model}")
    print(f"Accuracy: {metrics_by_model[best_model]['accuracy']}")
    print(f"F1 ponderado: {metrics_by_model[best_model]['f1_ponderado']}")
    print(f"Delta F1 vs baseline: {results['comparacion']['delta_f1']}")


if __name__ == "__main__":
    main()
