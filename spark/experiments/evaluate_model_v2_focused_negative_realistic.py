"""Evalua focused_negative_1950 contra validacion realistic."""

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

LABELS = ["negativo", "neutral", "positivo"]
REFERENCES = {
    "v2_curated_realistic": 0.737524,
    "v2_augmented_realistic": 0.792533,
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def preprocess(text: object) -> str:
    value = str(text).lower().strip()
    value = re.sub(r"[^a-záéíóúüñ\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def model() -> Pipeline:
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=3000)),
        ("model", LogisticRegression(max_iter=1200, class_weight="balanced", random_state=42)),
    ])


def matrix_table(matrix: list[list[int]]) -> str:
    lines = ["| Real \\ Predicho | negativo | neutral | positivo |", "| --- | ---: | ---: | ---: |"]
    for label, row in zip(LABELS, matrix):
        lines.append(f"| {label} | {row[0]} | {row[1]} | {row[2]} |")
    return "\n".join(lines)


def decision(f1_value: float, recalls: dict[str, float]) -> str:
    if f1_value >= 0.8 and recalls["negativo"] >= 0.75 and recalls["neutral"] >= 0.7 and recalls["positivo"] >= 0.7:
        return "Cumple criterio experimental. Recomendado para integracion controlada en rama separada, sin tocar main."
    if f1_value >= 0.75:
        return "Mejora parcial. Revisar errores por clase antes de integrar."
    return "No integrar. Mejorar dataset antes de promover."


def render(results: dict[str, object]) -> str:
    metrics = results["realistic_metrics"]
    recalls = results["recall_por_clase"]
    matrix = metrics["matriz_confusion"]
    return f"""# Reporte Modelo V2 Focused Negative Realistic

## Metricas

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

## Comparacion

| Experimento | F1 |
| --- | ---: |
| v2_curated realistic | {REFERENCES["v2_curated_realistic"]} |
| v2_augmented realistic | {REFERENCES["v2_augmented_realistic"]} |
| v2_focused_negative realistic | {metrics["f1_ponderado"]} |

## Matriz De Confusion

{matrix_table(matrix)}

## Recomendacion

{results["decision"]}

## Nota De Aislamiento

Evaluacion experimental aislada. No modifica ni integra el pipeline productivo.
"""


def main() -> None:
    root = project_root()
    train_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_focused_negative_1950.csv"
    realistic_csv = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_realistic_validation.csv"
    reports = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    metrics_path = reports / "metricas_modelo_v2_focused_negative_realistic.json"
    report_path = reports / "reporte_modelo_v2_focused_negative_realistic.md"
    pred_path = reports / "predicciones_modelo_v2_focused_negative_realistic.csv"
    train = pd.read_csv(train_csv, encoding="utf-8")
    realistic = pd.read_csv(realistic_csv, encoding="utf-8")
    train["texto_preprocesado"] = train["texto"].apply(preprocess)
    realistic["texto_preprocesado"] = realistic["texto"].apply(preprocess)
    clf = model()
    clf.fit(train["texto_preprocesado"], train["sentimiento"])
    pred = clf.predict(realistic["texto_preprocesado"])
    y = realistic["sentimiento"]
    matrix = confusion_matrix(y, pred, labels=LABELS).tolist()
    recalls = {}
    for label, row in zip(LABELS, matrix):
        total = sum(row)
        recalls[label] = round(row[LABELS.index(label)] / total, 6) if total else 0.0
    metrics = {
        "accuracy": round(float(accuracy_score(y, pred)), 6),
        "precision_ponderada": round(float(precision_score(y, pred, average="weighted", zero_division=0)), 6),
        "recall_ponderado": round(float(recall_score(y, pred, average="weighted", zero_division=0)), 6),
        "f1_ponderado": round(float(f1_score(y, pred, average="weighted", zero_division=0)), 6),
        "matriz_confusion": matrix,
        "labels_matriz_confusion": LABELS,
    }
    final_decision = decision(float(metrics["f1_ponderado"]), recalls)
    out_pred = realistic[["id", "texto", "texto_preprocesado", "sentimiento"]].copy()
    out_pred["prediccion_logistic_regression_focused"] = pred
    out_pred.to_csv(pred_path, index=False, encoding="utf-8")
    results = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "train_csv": str(train_csv),
        "realistic_csv": str(realistic_csv),
        "train_records": int(len(train)),
        "realistic_records": int(len(realistic)),
        "references": REFERENCES,
        "realistic_metrics": metrics,
        "recall_por_clase": recalls,
        "decision": final_decision,
        "archivos_generados": {"metricas_json": str(metrics_path), "reporte_md": str(report_path), "predicciones_csv": str(pred_path)},
    }
    metrics_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(render(results), encoding="utf-8")
    print(f"Metricas: {metrics_path}")
    print(f"Reporte: {report_path}")
    print(f"Predicciones: {pred_path}")
    print(f"F1 realistic: {metrics['f1_ponderado']}")
    print(final_decision)


if __name__ == "__main__":
    main()
