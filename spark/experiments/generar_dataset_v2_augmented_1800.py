"""Genera dataset v2 augmented 1800 desde curated_1500 + 300 ejemplos dirigidos."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


POSITIVE_SEEDS = [
    "no estuvo mal y al final me sirvio",
    "no me disgusto la respuesta, fue clara",
    "tenia dudas pero la solucion funciono",
    "demoro un poco aunque llego completo",
    "no fue perfecto pero resolvio lo importante",
    "la espera fue aceptable porque cerraron el caso",
    "me ayudo bastante aunque era algo breve",
    "el proceso tuvo detalles pero termino bien",
    "la atencion fue sencilla y util",
    "pude terminar sin pedir mas ayuda",
    "la compra salio bien, cero drama",
    "el producto cumplio incluso con dudas iniciales",
    "la pagina estaba lenta pero dejo finalizar",
    "la guia fue corta y aun asi clara",
    "el pedido no llego rapido pero llego bien",
    "la respuesta fue simple pero suficiente",
    "no tuve que insistir para resolverlo",
    "la herramienta me facilito el trabajo",
    "el seguimiento fue tranquilo",
    "la experiencia fue buena en general",
]
POSITIVE_VARIANTS = [
    "y eso dejo una buena impresion",
    "sin generar mas inconvenientes",
    "para lo que necesitaba",
    "con un cierre correcto",
    "y pude continuar",
]

NEUTRAL_SEEDS = [
    "el pedido sigue registrado",
    "la solicitud esta en revision",
    "el sistema muestra un estado",
    "la factura quedo disponible",
    "el documento aparece cargado",
    "la consulta fue enviada",
    "el reporte tiene datos generales",
    "la entrega figura en ruta",
    "la orden permanece abierta",
    "el mensaje quedo guardado",
    "la respuesta indica continuidad",
    "el producto tiene descripcion",
    "el tramite continua en proceso",
    "la pantalla muestra informacion",
    "el archivo esta disponible",
    "la consulta tiene prioridad normal",
    "el registro incluye fecha",
    "la notificacion fue emitida",
    "el caso queda para revision",
    "el formulario conserva los campos",
]
NEUTRAL_VARIANTS = [
    "sin valorar el resultado",
    "como dato informativo",
    "para seguimiento posterior",
    "sin comentario adicional",
    "en el panel actual",
]

NEGATIVE_SEEDS = [
    "no me gusto como cerraron el caso",
    "la respuesta no aclaro lo importante",
    "el proceso fue confuso y lento",
    "la plataforma se trabo varias veces",
    "el soporte tardo y no soluciono",
    "el producto fallo al probarlo",
    "la informacion no coincidia",
    "la entrega llego incompleta",
    "el sistema perdio cambios",
    "la compra se volvio complicada",
    "la atencion fue fria y poco clara",
    "el reporte no mostro lo esperado",
    "la guia dejo dudas abiertas",
    "el tramite quedo detenido",
    "la respuesta llego tarde",
    "el servicio fue inestable",
    "el producto no cumplio lo basico",
    "la plataforma no dejo terminar",
    "la orientacion fue insuficiente",
    "el pedido tuvo retrasos repetidos",
]
NEGATIVE_VARIANTS = [
    "y eso afecto la experiencia",
    "sin una salida concreta",
    "cuando mas lo necesitaba",
    "despues de varios intentos",
    "con poca claridad",
]


def expand(seeds: list[str], variants: list[str], label: str) -> list[dict[str, object]]:
    rows = []
    for seed in seeds:
        for variant in variants:
            rows.append({"texto": f"{seed} {variant}", "sentimiento": label})
    if len(rows) != 100:
        raise ValueError(f"{label}: se esperaban 100, se generaron {len(rows)}")
    return rows


def main() -> None:
    root = project_root()
    curated_path = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_curated_1500.csv"
    output_path = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_augmented_1800.csv"
    curated = pd.read_csv(curated_path, encoding="utf-8")

    rows = []
    next_id = 1
    for _, row in curated.iterrows():
        rows.append(
            {
                "id": next_id,
                "texto": row["texto"],
                "sentimiento": row["sentimiento"],
                "fuente": "augmented",
                "version": "v2_augmented",
            }
        )
        next_id += 1

    additions = (
        expand(POSITIVE_SEEDS, POSITIVE_VARIANTS, "positivo")
        + expand(NEUTRAL_SEEDS, NEUTRAL_VARIANTS, "neutral")
        + expand(NEGATIVE_SEEDS, NEGATIVE_VARIANTS, "negativo")
    )
    for row in additions:
        rows.append(
            {
                "id": next_id,
                "texto": row["texto"],
                "sentimiento": row["sentimiento"],
                "fuente": "augmented",
                "version": "v2_augmented",
            }
        )
        next_id += 1

    texts = [str(row["texto"]) for row in rows]
    if len(rows) != 1800:
        raise ValueError(f"Conteo inesperado: {len(rows)}")
    if len(set(texts)) != len(texts):
        raise ValueError("Duplicados exactos detectados")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "texto", "sentimiento", "fuente", "version"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Dataset augmented generado: {output_path}")
    print(f"Registros: {len(rows)}")


if __name__ == "__main__":
    main()
