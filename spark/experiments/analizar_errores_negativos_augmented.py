"""Analiza negativos mal clasificados por el modelo augmented realistic."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


PRED_COL = "prediccion_logistic_regression_augmented"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def top_ngrams(texts: list[str]) -> list[tuple[str, int]]:
    if not texts:
        return []
    vectorizer = CountVectorizer(ngram_range=(1, 2), lowercase=True)
    matrix = vectorizer.fit_transform(texts)
    counts = matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()
    return [(term, int(count)) for term, count in sorted(zip(terms, counts), key=lambda x: (-x[1], x[0]))[:20]]


def examples(rows: pd.DataFrame) -> str:
    if rows.empty:
        return "Sin ejemplos."
    lines = ["| id | predicho | texto |", "| ---: | --- | --- |"]
    for _, row in rows.head(12).iterrows():
        lines.append(f"| {row['id']} | {row[PRED_COL]} | {str(row['texto']).replace('|', '/')} |")
    return "\n".join(lines)


def ngram_table(title: str, texts: list[str]) -> str:
    lines = [f"### {title}", "", "| n-gram | frecuencia |", "| --- | ---: |"]
    for term, count in top_ngrams(texts):
        lines.append(f"| {term} | {count} |")
    return "\n".join(lines)


def main() -> None:
    root = project_root()
    input_path = root / "data" / "experiments" / "dataset_v2" / "reports" / "predicciones_modelo_v2_augmented_realistic.csv"
    output_path = root / "data" / "experiments" / "dataset_v2" / "reports" / "reporte_errores_negativos_augmented.md"
    df = pd.read_csv(input_path, encoding="utf-8")
    negatives = df[df["sentimiento"] == "negativo"].copy()
    neg_as_neutral = negatives[negatives[PRED_COL] == "neutral"]
    neg_as_positive = negatives[negatives[PRED_COL] == "positivo"]
    total_errors = len(neg_as_neutral) + len(neg_as_positive)

    report = f"""# Reporte Errores Negativos Augmented

## Resumen

- Archivo analizado: `{input_path}`
- Negativos reales: `{len(negatives)}`
- Negativos clasificados como neutral: `{len(neg_as_neutral)}`
- Negativos clasificados como positivo: `{len(neg_as_positive)}`
- Total errores negativos: `{total_errors}`
- Recall negativo observado: `{round((len(negatives) - total_errors) / len(negatives), 6)}`

## Negativos Clasificados Como Neutral

{examples(neg_as_neutral)}

## Negativos Clasificados Como Positivo

{examples(neg_as_positive)}

## Patrones Frecuentes

{ngram_table("Negativo -> Neutral", neg_as_neutral["texto"].astype(str).tolist())}

{ngram_table("Negativo -> Positivo", neg_as_positive["texto"].astype(str).tolist())}

## Lectura Tecnica

Los negativos ambiguos suelen contener problemas expresados con tono moderado, palabras informativas o frases que comparten vocabulario con positivos y neutrales. La siguiente iteracion debe reforzar quejas suaves, decepcion moderada, retrasos con cierre incompleto, y experiencias mixtas donde domina lo negativo.
"""
    output_path.write_text(report, encoding="utf-8")
    print(f"Reporte: {output_path}")
    print(f"Errores negativos: {total_errors}")


if __name__ == "__main__":
    main()
