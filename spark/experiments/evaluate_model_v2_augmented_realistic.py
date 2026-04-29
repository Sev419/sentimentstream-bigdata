"""Evalua modelo v2 augmented contra validacion realistic."""

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
    "v2_300": 0.622983,
    "v2_1500_sintetico_externo": 0.735499,
    "v2_curated_realistic": 0.737524,
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
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=3000)),
            ("model", LogisticRegression(max_iter=1200, class_weight="balanced", random_state=42)),
        ]
    )


def matrix_table(matrix: list[list[int]]) -> str:
    lines = ["| Real \\ Predicho | negativo | neutral | positivo |", "| --- | ---: | ---: | ---: |"]
    for label, row in zip(LABELS, matrix):
        lines.append(f"| {label} | {row[0]} | {row[1]} | {row[2]} |")
    return "\n".join(lines)


def decision(f1_value: float, recalls: dict[str, float]) -> str:
    balanced = min(recalls.values()) >= 0.7
    if f1_value >= 0.8 and balanced:
        return "Cumple criterio experimental. Recomendado para integracion controlada en rama separada, con revision humana adicional."
    if f1_value >= 0.75:
        return "Mejora documentada, pero se deben revisar errores y estabilidad por clase antes de integrar."
    return "No integrar. Se debe mejorar el dataset antes de promover el modelo."


def render_report(results: dict[str, object]) -> str:
    metrics = results["realistic_metrics"]
    assert isinstance(metrics, dict)
    recalls = results["recall_por_clase"]
    assert isinstance(recalls, dict)
    matrix = metrics["matriz_confusion"]
    assert isinstance(matrix, list)
    return f"""# Reporte Modelo V2 Augmented Realistic

## Proposito

Evaluar el dataset augmented 1800 contra la validacion realistic, sin mezclar datos externos con entrenamiento.

## Metricas Realistic

| Metrica | Valor |
| --- | ---: |
| Accuracy | {metrics["accuracy"]} |
| Precision ponderada | {metrics["precision_ponderada"]} |
| Recall ponderado | {metrics["recall_ponderado"]} |
| F1 ponderado | {metrics["f1_ponderado"]} |

## Recall Por Clase

| Clase | Recall |
| --- | ---: |
| negativo | {recalls["negativo"]} |
| neutral | {recalls["neutral"]} |
| positivo | {recalls["positivo"]} |

## Comparacion Final

| Experimento | F1 |
| --- | ---: |
| v2_300 | {REFERENCES["v2_300"]} |
| v2_1500 externo | {REFERENCES["v2_1500_sintetico_externo"]} |
| v2_curated realistic | {REFERENCES["v2_curated_realistic"]} |
| v2_augmented realistic | {metrics["f1_ponderado"]} |

## Matriz De Confusion

{matrix_table(matrix)}

## Conclusion

{results["decision"]}

## Nota De Aislamiento

Esta evaluacion solo lee y escribe dentro de `data/experiments/dataset_v2/`.
No modifica ni integra el pipeline productivo.
"""


def main() -> None:
    root = project_root()
    train_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_augmented_1800.csv"
    realistic_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_realistic_validation.csv"
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    metrics_json = reports_dir / "metricas_modelo_v2_augmented_realistic.json"
    report_md = reports_dir / "reporte_modelo_v2_augmented_realistic.md"
    predictions_csv = reports_dir / "predicciones_modelo_v2_augmented_realistic.csv"

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
    recalls = {}
    for label, row in zip(LABELS, matrix):
        total = sum(row)
        recalls[label] = round(row[LABELS.index(label)] / total, 6) if total else 0.0
    metrics = {
        "accuracy": round(float(accuracy_score(y_true, predictions)), 6),
        "precision_ponderada": round(float(precision_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "recall_ponderado": round(float(recall_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "f1_ponderado": round(float(f1_score(y_true, predictions, average="weighted", zero_division=0)), 6),
        "matriz_confusion": matrix,
        "labels_matriz_confusion": LABELS,
    }
    final_decision = decision(float(metrics["f1_ponderado"]), recalls)
    pred_df = realistic_df[["id", "texto", "texto_preprocesado", "sentimiento"]].copy()
    pred_df["prediccion_logistic_regression_augmented"] = predictions
    pred_df.to_csv(predictions_csv, index=False, encoding="utf-8")
    results: dict[str, object] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "train_csv": str(train_csv),
        "realistic_csv": str(realistic_csv),
        "train_records": int(len(train_df)),
        "realistic_records": int(len(realistic_df)),
        "references": REFERENCES,
        "realistic_metrics": metrics,
        "recall_por_clase": recalls,
        "decision": final_decision,
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
    print(f"Predicciones: {predictions_csv}")
    print(f"F1 realistic: {metrics['f1_ponderado']}")
    print(final_decision)


if __name__ == "__main__":
    main()
