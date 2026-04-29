"""Analiza errores de la validacion realistic del modelo v2 curated."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix


LABELS = ["negativo", "neutral", "positivo"]
PREDICTION_COLUMN = "prediccion_logistic_regression_curated"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def top_ngrams(texts: list[str], top_n: int = 15) -> list[tuple[str, int]]:
    if not texts:
        return []
    vectorizer = CountVectorizer(ngram_range=(1, 2), lowercase=True)
    matrix = vectorizer.fit_transform(texts)
    counts = matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()
    pairs = sorted(zip(terms, counts), key=lambda item: (-item[1], item[0]))
    return [(term, int(count)) for term, count in pairs[:top_n]]


def matrix_table(matrix: list[list[int]]) -> str:
    lines = [
        "| Real \\ Predicho | negativo | neutral | positivo |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, row in zip(LABELS, matrix):
        lines.append(f"| {label} | {row[0]} | {row[1]} | {row[2]} |")
    return "\n".join(lines)


def examples_table(rows: pd.DataFrame, limit: int = 5) -> str:
    if rows.empty:
        return "Sin ejemplos."
    lines = ["| id | real | predicho | texto |", "| ---: | --- | --- | --- |"]
    for _, row in rows.head(limit).iterrows():
        text = str(row["texto"]).replace("|", "/")
        lines.append(f"| {row['id']} | {row['sentimiento']} | {row[PREDICTION_COLUMN]} | {text} |")
    return "\n".join(lines)


def main() -> None:
    root = project_root()
    predictions_path = root / "data" / "experiments" / "dataset_v2" / "reports" / "predicciones_modelo_v2_curated_realistic.csv"
    output_path = root / "data" / "experiments" / "dataset_v2" / "reports" / "reporte_errores_realistic.md"

    df = pd.read_csv(predictions_path, encoding="utf-8")
    errors = df[df["sentimiento"] != df[PREDICTION_COLUMN]].copy()
    matrix = confusion_matrix(df["sentimiento"], df[PREDICTION_COLUMN], labels=LABELS).tolist()

    false_sections: list[str] = []
    for label in LABELS:
        fp = df[(df["sentimiento"] != label) & (df[PREDICTION_COLUMN] == label)]
        fn = df[(df["sentimiento"] == label) & (df[PREDICTION_COLUMN] != label)]
        false_sections.append(
            f"""### Clase `{label}`

- Falsos positivos: `{len(fp)}`
- Falsos negativos: `{len(fn)}`

Falsos positivos representativos:

{examples_table(fp)}

Falsos negativos representativos:

{examples_table(fn)}
"""
        )

    pair_groups: dict[str, list[str]] = defaultdict(list)
    for _, row in errors.iterrows():
        pair_groups[f"{row['sentimiento']} -> {row[PREDICTION_COLUMN]}"].append(str(row["texto"]))

    ngram_sections = []
    for pair, texts in sorted(pair_groups.items()):
        ngrams = top_ngrams(texts)
        lines = [f"### Error `{pair}`", "", "| n-gram | frecuencia |", "| --- | ---: |"]
        for term, count in ngrams:
            lines.append(f"| {term} | {count} |")
        ngram_sections.append("\n".join(lines))

    report = f"""# Reporte De Errores Realistic

## Resumen

- Archivo analizado: `{predictions_path}`
- Total predicciones: `{len(df)}`
- Total errores: `{len(errors)}`
- Accuracy observado: `{round((len(df) - len(errors)) / len(df), 6)}`

## Matriz De Confusion

{matrix_table(matrix)}

## Falsos Positivos Y Falsos Negativos Por Clase

{chr(10).join(false_sections)}

## Top N-Grams En Errores

{chr(10).join(ngram_sections)}

## Lectura Tecnica

Los errores se concentran en frases con negaciones, expresiones mixtas y comentarios positivos o negativos con lenguaje menos directo. Estos patrones deben alimentar el dataset augmented para mejorar generalizacion.
"""
    output_path.write_text(report, encoding="utf-8")
    print(f"Reporte de errores: {output_path}")
    print(f"Errores: {len(errors)}")


if __name__ == "__main__":
    main()
