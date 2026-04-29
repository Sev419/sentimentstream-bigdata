"""Auditoria automatica del dataset experimental v2.

Este script trabaja solo con archivos dentro de data/experiments/dataset_v2.
No entrena modelos, no conecta MongoDB y no modifica el pipeline productivo.
"""

from __future__ import annotations

import csv
import json
import re
import argparse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean


REQUIRED_COLUMNS = ["id", "texto", "sentimiento", "fuente", "version"]
VALID_LABELS = {"positivo", "neutral", "negativo"}


EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audita un CSV experimental del dataset v2.")
    parser.add_argument(
        "--input",
        default=None,
        help="Ruta opcional del CSV experimental a auditar. Por defecto usa el template raw.",
    )
    return parser.parse_args()


def read_rows(csv_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = [{key: (value if value is not None else "") for key, value in row.items()} for row in reader]
    return rows, fieldnames


def detect_sensitive_texts(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for index, row in enumerate(rows, start=2):
        text = row.get("texto", "")
        detected = []
        if EMAIL_PATTERN.search(text):
            detected.append("correo")
        if PHONE_PATTERN.search(text):
            detected.append("telefono")
        if detected:
            findings.append(
                {
                    "linea_csv": str(index),
                    "id": row.get("id", ""),
                    "tipo": ", ".join(detected),
                    "texto": text,
                }
            )
    return findings


def audit_dataset(csv_path: Path) -> dict[str, object]:
    exists = csv_path.exists()
    rows: list[dict[str, str]] = []
    columns: list[str] = []

    if exists:
        rows, columns = read_rows(csv_path)

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in columns]
    extra_columns = [column for column in columns if column not in REQUIRED_COLUMNS]

    total_records = len(rows)
    labels = [row.get("sentimiento", "").strip().lower() for row in rows]
    label_distribution = dict(Counter(labels))
    invalid_label_rows = [
        {
            "linea_csv": index,
            "id": row.get("id", ""),
            "sentimiento": row.get("sentimiento", ""),
        }
        for index, row in enumerate(rows, start=2)
        if row.get("sentimiento", "").strip().lower() not in VALID_LABELS
    ]

    null_text_rows = [
        {"linea_csv": index, "id": row.get("id", "")}
        for index, row in enumerate(rows, start=2)
        if "texto" not in row or row.get("texto") is None
    ]
    empty_text_rows = [
        {"linea_csv": index, "id": row.get("id", "")}
        for index, row in enumerate(rows, start=2)
        if row.get("texto", "").strip() == ""
    ]

    normalized_texts = [row.get("texto", "").strip().lower() for row in rows]
    text_counts = Counter(text for text in normalized_texts if text)
    duplicate_texts = [
        {"texto": text, "cantidad": count}
        for text, count in sorted(text_counts.items())
        if count > 1
    ]

    full_row_values = [tuple(row.get(column, "") for column in columns) for row in rows]
    full_row_counts = Counter(full_row_values)
    duplicate_full_rows = [
        {"fila": dict(zip(columns, values)), "cantidad": count}
        for values, count in full_row_counts.items()
        if count > 1
    ]

    text_lengths = [len(row.get("texto", "").strip()) for row in rows if row.get("texto", "").strip()]
    length_metrics = {
        "minima": min(text_lengths) if text_lengths else 0,
        "media": round(mean(text_lengths), 2) if text_lengths else 0,
        "maxima": max(text_lengths) if text_lengths else 0,
    }

    sensitive_findings = detect_sensitive_texts(rows)

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_csv": str(csv_path),
        "csv_exists": exists,
        "required_columns": REQUIRED_COLUMNS,
        "columns_found": columns,
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "total_records": total_records,
        "label_distribution": {
            "positivo": label_distribution.get("positivo", 0),
            "neutral": label_distribution.get("neutral", 0),
            "negativo": label_distribution.get("negativo", 0),
        },
        "raw_label_distribution": label_distribution,
        "invalid_labels_count": len(invalid_label_rows),
        "invalid_label_rows": invalid_label_rows,
        "null_texts_count": len(null_text_rows),
        "null_text_rows": null_text_rows,
        "empty_texts_count": len(empty_text_rows),
        "empty_text_rows": empty_text_rows,
        "duplicate_texts_count": len(duplicate_texts),
        "duplicate_texts": duplicate_texts,
        "duplicate_full_rows_count": len(duplicate_full_rows),
        "duplicate_full_rows": duplicate_full_rows,
        "text_length": length_metrics,
        "sensitive_findings_count": len(sensitive_findings),
        "sensitive_findings": sensitive_findings,
    }


def markdown_table_distribution(distribution: dict[str, int], total: int) -> str:
    lines = [
        "| Clase | Cantidad | Porcentaje |",
        "| --- | ---: | ---: |",
    ]
    for label in ["positivo", "neutral", "negativo"]:
        count = distribution.get(label, 0)
        percentage = (count / total * 100) if total else 0
        lines.append(f"| {label} | {count} | {percentage:.2f}% |")
    return "\n".join(lines)


def render_markdown(metrics: dict[str, object]) -> str:
    distribution = metrics["label_distribution"]
    assert isinstance(distribution, dict)
    total = int(metrics["total_records"])
    text_length = metrics["text_length"]
    assert isinstance(text_length, dict)

    status = "apto para revision experimental"
    if metrics["missing_columns"] or metrics["invalid_labels_count"] or metrics["empty_texts_count"]:
        status = "requiere revision"
    if not metrics["csv_exists"]:
        status = "archivo de entrada no encontrado"

    return f"""# Resultado Auditoria Dataset V2

## Resumen

- Archivo auditado: `{metrics["input_csv"]}`
- Existe CSV: `{metrics["csv_exists"]}`
- Fecha UTC de auditoria: `{metrics["generated_at_utc"]}`
- Estado: `{status}`

## Columnas

- Columnas obligatorias: `{", ".join(REQUIRED_COLUMNS)}`
- Columnas encontradas: `{", ".join(metrics["columns_found"]) if metrics["columns_found"] else "N/A"}`
- Columnas faltantes: `{", ".join(metrics["missing_columns"]) if metrics["missing_columns"] else "ninguna"}`
- Columnas extra: `{", ".join(metrics["extra_columns"]) if metrics["extra_columns"] else "ninguna"}`

## Validacion General

| Criterio | Resultado |
| --- | ---: |
| Total registros | {metrics["total_records"]} |
| Etiquetas invalidas | {metrics["invalid_labels_count"]} |
| Textos nulos | {metrics["null_texts_count"]} |
| Textos vacios | {metrics["empty_texts_count"]} |
| Duplicados por texto | {metrics["duplicate_texts_count"]} |
| Duplicados completos | {metrics["duplicate_full_rows_count"]} |
| Posibles datos sensibles | {metrics["sensitive_findings_count"]} |

## Distribucion Por Sentimiento

{markdown_table_distribution(distribution, total)}

## Longitud Del Texto

| Metrica | Valor |
| --- | ---: |
| Minima | {text_length["minima"]} |
| Media | {text_length["media"]} |
| Maxima | {text_length["maxima"]} |

## Problemas Encontrados

- Etiquetas invalidas: `{metrics["invalid_labels_count"]}`
- Textos nulos: `{metrics["null_texts_count"]}`
- Textos vacios: `{metrics["empty_texts_count"]}`
- Duplicados por texto: `{metrics["duplicate_texts_count"]}`
- Duplicados completos: `{metrics["duplicate_full_rows_count"]}`
- Posibles correos o telefonos en texto: `{metrics["sensitive_findings_count"]}`

## Nota De Aislamiento

Esta auditoria solo lee archivos dentro de `data/experiments/dataset_v2/` y solo escribe resultados en `data/experiments/dataset_v2/reports/`.

No entrena modelos, no modifica datos productivos, no conecta MongoDB y no toca el pipeline estable.
"""


def resolve_input_path(root: Path, input_arg: str | None) -> Path:
    default_path = root / "data" / "experiments" / "dataset_v2" / "raw" / "dataset_sentimientos_v2_template.csv"
    if not input_arg:
        return default_path

    input_path = Path(input_arg)
    if not input_path.is_absolute():
        input_path = root / input_path

    resolved = input_path.resolve()
    allowed_root = (root / "data" / "experiments" / "dataset_v2").resolve()
    if allowed_root not in [resolved, *resolved.parents]:
        raise ValueError(f"El archivo de entrada debe estar dentro de {allowed_root}")
    return resolved


def output_paths_for_input(root: Path, csv_path: Path) -> tuple[Path, Path]:
    reports_dir = root / "data" / "experiments" / "dataset_v2" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    if csv_path.name == "dataset_sentimientos_v2_template.csv":
        return (
            reports_dir / "reporte_auditoria_v2_resultado.md",
            reports_dir / "metricas_auditoria_v2.json",
        )

    if csv_path.name == "dataset_sentimientos_v2_labeled.csv":
        return (
            reports_dir / "reporte_auditoria_v2_labeled.md",
            reports_dir / "metricas_auditoria_v2_labeled.json",
        )

    if csv_path.name == "dataset_sentimientos_v2_labeled_300.csv":
        return (
            reports_dir / "reporte_auditoria_v2_labeled_300.md",
            reports_dir / "metricas_auditoria_v2_labeled_300.json",
        )

    if csv_path.name == "dataset_sentimientos_v2_labeled_1500.csv":
        return (
            reports_dir / "reporte_auditoria_v2_labeled_1500.md",
            reports_dir / "metricas_auditoria_v2_labeled_1500.json",
        )

    if csv_path.name == "dataset_sentimientos_v2_curated_1500.csv":
        return (
            reports_dir / "reporte_auditoria_v2_curated_1500.md",
            reports_dir / "metricas_auditoria_v2_curated_1500.json",
        )

    if csv_path.name == "dataset_sentimientos_v2_realistic_validation.csv":
        return (
            reports_dir / "reporte_auditoria_v2_realistic_validation.md",
            reports_dir / "metricas_auditoria_v2_realistic_validation.json",
        )

    if csv_path.name == "dataset_sentimientos_v2_augmented_1800.csv":
        return (
            reports_dir / "reporte_auditoria_v2_augmented_1800.md",
            reports_dir / "metricas_auditoria_v2_augmented_1800.json",
        )

    if csv_path.name == "dataset_sentimientos_v2_focused_negative_1950.csv":
        return (
            reports_dir / "reporte_auditoria_v2_focused_negative_1950.md",
            reports_dir / "metricas_auditoria_v2_focused_negative_1950.json",
        )

    safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "_", csv_path.stem)
    return (
        reports_dir / f"reporte_auditoria_v2_{safe_stem}.md",
        reports_dir / f"metricas_auditoria_v2_{safe_stem}.json",
    )


def main() -> None:
    args = parse_args()
    root = project_root()
    csv_path = resolve_input_path(root, args.input)

    metrics = audit_dataset(csv_path)

    markdown_path, json_path = output_paths_for_input(root, csv_path)

    json_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown(metrics), encoding="utf-8")

    print(f"Reporte Markdown: {markdown_path}")
    print(f"Resumen JSON: {json_path}")
    print(f"Total registros: {metrics['total_records']}")
    print(f"Etiquetas invalidas: {metrics['invalid_labels_count']}")
    print(f"Textos vacios: {metrics['empty_texts_count']}")
    print(f"Duplicados por texto: {metrics['duplicate_texts_count']}")
    print(f"Posibles datos sensibles: {metrics['sensitive_findings_count']}")


if __name__ == "__main__":
    main()
