"""Genera dataset experimental v2 de 1500 registros balanceados.

Este generador solo escribe en data/experiments/dataset_v2/labeled/.
No modifica datos productivos ni se conecta al pipeline estable.
"""

from __future__ import annotations

import csv
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_rows(subjects: list[str], phrases: list[str], label: str, start_id: int) -> tuple[list[dict[str, object]], int]:
    rows: list[dict[str, object]] = []
    next_id = start_id
    seen: set[str] = set()

    for subject in subjects:
        for phrase in phrases:
            text = f"{subject} {phrase}"
            if text in seen:
                raise ValueError(f"Texto duplicado interno: {text}")
            seen.add(text)
            rows.append(
                {
                    "id": next_id,
                    "texto": text,
                    "sentimiento": label,
                    "fuente": "manual",
                    "version": "v2",
                }
            )
            next_id += 1

    if len(rows) != 500:
        raise ValueError(f"{label} genero {len(rows)} registros; se esperaban 500")

    return rows, next_id


def main() -> None:
    output_path = (
        project_root()
        / "data"
        / "experiments"
        / "dataset_v2"
        / "labeled"
        / "dataset_sentimientos_v2_labeled_1500.csv"
    )

    positive_subjects = [
        "El servicio",
        "La atencion",
        "El producto",
        "La entrega",
        "El soporte",
        "La plataforma",
        "El sistema",
        "La compra",
        "El proceso",
        "La informacion",
        "La respuesta",
        "El tramite",
        "La herramienta",
        "El pedido",
        "La experiencia",
        "La guia",
        "La solicitud",
        "El reporte",
        "La orientacion",
        "La gestion",
    ]
    positive_phrases = [
        "fue excelente y clara",
        "funciono de manera correcta",
        "supero las expectativas",
        "resulto muy satisfactoria",
        "fue rapida y ordenada",
        "cumplio lo prometido",
        "se completo sin inconvenientes",
        "fue facil de entender",
        "ofrecio una solucion util",
        "mantuvo buena calidad",
        "fue precisa y oportuna",
        "ayudo a resolver la duda",
        "se desarrollo con eficiencia",
        "dejo una buena impresion",
        "fue confiable durante el uso",
        "respondio de forma adecuada",
        "mejoro la experiencia general",
        "fue amable y profesional",
        "permitio avanzar sin problemas",
        "tuvo un resultado positivo",
        "llego en buen estado",
        "se gestiono correctamente",
        "fue simple y practica",
        "entrego informacion completa",
        "mostro un desempeno estable",
    ]

    neutral_subjects = [
        "El pedido",
        "La solicitud",
        "El producto",
        "El reporte",
        "La factura",
        "El documento",
        "La consulta",
        "La entrega",
        "El sistema",
        "La orden",
        "El archivo",
        "La plataforma",
        "El formulario",
        "La revision",
        "El registro",
        "La informacion",
        "El tramite",
        "La respuesta",
        "El panel",
        "La notificacion",
    ]
    neutral_phrases = [
        "quedo registrado en el sistema",
        "se encuentra en revision",
        "muestra el estado actual",
        "fue recibido correctamente",
        "esta disponible para consulta",
        "permanece en proceso",
        "tiene informacion general",
        "fue actualizado en la plataforma",
        "aparece en el historial",
        "mantiene estado activo",
        "fue clasificado para revision",
        "esta programado para seguimiento",
        "quedo guardado sin cambios",
        "incluye datos descriptivos",
        "se muestra en el panel",
        "fue enviado para validacion",
        "esta pendiente de confirmacion",
        "contiene una descripcion breve",
        "se encuentra en la lista",
        "fue marcado como recibido",
        "tiene una fecha asignada",
        "continua abierto en el sistema",
        "presenta opciones disponibles",
        "quedo documentado en el reporte",
        "se mantiene sin novedad",
    ]

    negative_subjects = positive_subjects
    negative_phrases = [
        "fue lento y confuso",
        "no resolvio el problema",
        "presento fallas constantes",
        "resulto insatisfactorio",
        "tuvo demasiados errores",
        "no cumplio lo esperado",
        "se interrumpio sin aviso",
        "fue dificil de completar",
        "genero mucha confusion",
        "tuvo baja calidad",
        "fue incompleta y tardia",
        "no ayudo a resolver la duda",
        "se desarrollo con demoras",
        "dejo una mala impresion",
        "fue poco confiable durante el uso",
        "respondio de forma deficiente",
        "empeoro la experiencia general",
        "fue fria y poco clara",
        "impidio avanzar correctamente",
        "tuvo un resultado negativo",
        "llego en mal estado",
        "se gestiono incorrectamente",
        "fue complicada y poco practica",
        "entrego informacion insuficiente",
        "mostro un desempeno inestable",
    ]

    rows: list[dict[str, object]] = []
    next_id = 1
    for subjects, phrases, label in [
        (positive_subjects, positive_phrases, "positivo"),
        (neutral_subjects, neutral_phrases, "neutral"),
        (negative_subjects, negative_phrases, "negativo"),
    ]:
        generated, next_id = build_rows(subjects, phrases, label, next_id)
        rows.extend(generated)

    texts = [str(row["texto"]) for row in rows]
    if len(rows) != 1500:
        raise ValueError(f"Conteo total inesperado: {len(rows)}")
    if len(set(texts)) != len(texts):
        raise ValueError("Se encontraron textos duplicados exactos")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "texto", "sentimiento", "fuente", "version"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset generado: {output_path}")
    print(f"Registros: {len(rows)}")


if __name__ == "__main__":
    main()
