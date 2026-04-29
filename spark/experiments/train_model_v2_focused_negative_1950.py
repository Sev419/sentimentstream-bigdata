"""Entrena modelos experimentales con dataset focused_negative_1950."""

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

LABELS = ["negativo", "neutral", "positivo"]
REQUIRED_COLUMNS = ["id", "texto", "sentimiento", "fuente", "version"]


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def preprocess(text: object) -> str:
    value = str(text).lower().strip()
    value = re.sub(r"[^a-záéíóúüñ\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def validate(df: pd.DataFrame) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas: {missing}")
    invalid = sorted(set(df["sentimiento"].astype(str)) - set(LABELS))
    if invalid:
        raise ValueError(f"Etiquetas invalidas: {invalid}")


def models() -> dict[str, Pipeline]:
    params = {"ngram_range": (1, 2), "min_df": 1, "max_features": 3000}
    return {
        "logistic_regression": Pipeline([("tfidf", TfidfVectorizer(**params)), ("model", LogisticRegression(max_iter=1200, class_weight="balanced", random_state=42))]),
        "naive_bayes": Pipeline([("tfidf", TfidfVectorizer(**params)), ("model", MultinomialNB())]),
    }


def evaluate(model: Pipeline, x: pd.Series, y: pd.Series) -> dict[str, object]:
    pred = model.predict(x)
    return {
        "accuracy": round(float(accuracy_score(y, pred)), 6),
        "precision_ponderada": round(float(precision_score(y, pred, average="weighted", zero_division=0)), 6),
        "recall_ponderado": round(float(recall_score(y, pred, average="weighted", zero_division=0)), 6),
        "f1_ponderado": round(float(f1_score(y, pred, average="weighted", zero_division=0)), 6),
        "matriz_confusion": confusion_matrix(y, pred, labels=LABELS).tolist(),
        "labels_matriz_confusion": LABELS,
    }


def render(results: dict[str, object]) -> str:
    rows = ["| Modelo | Accuracy | Precision | Recall | F1 |", "| --- | ---: | ---: | ---: | ---: |"]
    modelos = results["modelos"]
    assert isinstance(modelos, dict)
    for name, metrics in modelos.items():
        rows.append(f"| {name} | {metrics['accuracy']} | {metrics['precision_ponderada']} | {metrics['recall_ponderado']} | {metrics['f1_ponderado']} |")
    return f"""# Reporte Modelo V2 Focused Negative 1950

## Dataset

- Archivo: `{results["input_csv"]}`
- Total: `{results["total_registros"]}`
- Train: `{results["train_registros"]}`
- Test: `{results["test_registros"]}`

## Modelos

{chr(10).join(rows)}

## Mejor Modelo

- `{results["mejor_modelo"]}`

## Nota

Entrenamiento experimental aislado. No se integra al pipeline estable.
"""


def main() -> None:
    root = project_root()
    input_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_focused_negative_1950.csv"
    reports = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    metrics_path = reports / "metricas_modelo_v2_focused_negative_1950.json"
    report_path = reports / "reporte_modelo_v2_focused_negative_1950.md"
    df = pd.read_csv(input_csv, encoding="utf-8")
    validate(df)
    df["texto_preprocesado"] = df["texto"].apply(preprocess)
    train, test = train_test_split(df, test_size=0.2, random_state=42, stratify=df["sentimiento"])
    metrics_by_model = {}
    for name, model in models().items():
        model.fit(train["texto_preprocesado"], train["sentimiento"])
        metrics_by_model[name] = evaluate(model, test["texto_preprocesado"], test["sentimiento"])
    best = max(metrics_by_model, key=lambda n: (float(metrics_by_model[n]["f1_ponderado"]), float(metrics_by_model[n]["accuracy"])))
    results = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_csv": str(input_csv),
        "total_registros": int(len(df)),
        "train_registros": int(len(train)),
        "test_registros": int(len(test)),
        "distribucion_total": {label: int((df["sentimiento"] == label).sum()) for label in LABELS},
        "modelos": metrics_by_model,
        "mejor_modelo": best,
    }
    metrics_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(render(results), encoding="utf-8")
    print(f"Metricas: {metrics_path}")
    print(f"Reporte: {report_path}")
    print(f"Mejor modelo: {best}")
    print(f"F1 interno: {metrics_by_model[best]['f1_ponderado']}")


if __name__ == "__main__":
    main()
