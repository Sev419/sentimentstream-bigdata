"""Genera dataset v2 curado de 1500 registros balanceados.

Solo escribe en data/experiments/dataset_v2/labeled/.
No modifica datos productivos ni integra cambios al pipeline estable.
"""

from __future__ import annotations

import csv
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


PREFIXES = [
    "",
    "La verdad, ",
    "En general, ",
    "Bueno, ",
    "Al final, ",
    "Por ahora, ",
    "Mmm, ",
    "Despues de revisar, ",
    "Con lo visto, ",
    "Para este caso, ",
]


POSITIVE_BASE = [
    "no estuvo mal y termino ayudando",
    "tuvo una demora pequena pero salio bien",
    "resolvio lo principal sin tanta vuelta",
    "me dejo una impresion bastante buena",
    "funciono mejor de lo que esperaba",
    "fue claro cuando mas lo necesitaba",
    "avanzo lento al inicio pero cerro bien",
    "me permitio completar la tarea sin problema",
    "la respuesta fue corta pero util",
    "el resultado quedo correcto",
    "la guia aclaro casi todas mis dudas",
    "la plataforma respondio de forma estable",
    "el pedido llego completo y cuidado",
    "el soporte entendio la situacion",
    "la gestion fue simple y ordenada",
    "el proceso se sintio confiable",
    "la informacion fue suficiente para decidir",
    "la compra fue tranquila hasta el cierre",
    "el producto cumplio con lo necesario",
    "la entrega estuvo dentro de lo esperado",
    "la atencion fue amable sin exagerar",
    "el sistema guardo todo correctamente",
    "la solucion fue sencilla y efectiva",
    "el panel facilito revisar el avance",
    "el seguimiento llego a tiempo",
    "la experiencia resulto comoda",
    "la respuesta aclaro el punto clave",
    "el tramite quedo resuelto",
    "el servicio mantuvo buen ritmo",
    "la herramienta simplifico el trabajo",
    "el mensaje de confirmacion fue suficiente",
    "la revision ayudo a corregir la duda",
    "el flujo fue facil de seguir",
    "el cambio solicitado quedo aplicado",
    "la comunicacion fue adecuada",
    "el resultado fue util para continuar",
    "la plataforma permitio terminar rapido",
    "el producto funciono desde el primer uso",
    "la asesoria fue practica",
    "el estado se actualizo correctamente",
    "no me disgusto el resultado final",
    "no tuve inconvenientes importantes",
    "pudo mejorar detalles pero cumplio",
    "la espera valio la pena",
    "me sirvio para resolver la solicitud",
    "fue mejor que la opcion anterior",
    "la explicacion quedo entendible",
    "el pedido se manejo con cuidado",
    "la herramienta respondio sin fallar",
    "la experiencia cerro de forma positiva",
]

NEUTRAL_BASE = [
    "el pedido aparece registrado",
    "la solicitud sigue en revision",
    "el sistema muestra el estado actual",
    "la factura esta disponible",
    "el documento quedo cargado",
    "la consulta fue enviada",
    "el reporte contiene informacion general",
    "la entrega figura en seguimiento",
    "la orden permanece abierta",
    "el mensaje quedo guardado",
    "la respuesta indica proceso activo",
    "el producto tiene descripcion breve",
    "la revision fue asignada",
    "el tramite continua en curso",
    "la pantalla muestra los datos",
    "el archivo esta listo para descarga",
    "la consulta tiene prioridad normal",
    "el registro incluye fecha",
    "la entrega esta programada",
    "el sistema genero una notificacion",
    "la solicitud fue recibida hoy",
    "el producto aparece en inventario",
    "la respuesta espera confirmacion",
    "el reporte fue generado",
    "la informacion se mantiene igual",
    "el tramite quedo documentado",
    "la consulta esta disponible",
    "el panel muestra actividad reciente",
    "la orden quedo en cola",
    "el documento contiene datos generales",
    "la solicitud tiene respuesta parcial",
    "el sistema conserva el registro",
    "la entrega fue programada",
    "el producto tiene dos alternativas",
    "la consulta quedo sin asignar",
    "la respuesta fue registrada",
    "el estado se muestra activo",
    "la solicitud esta documentada",
    "el reporte incluye varias secciones",
    "la informacion fue recibida",
    "el tramite espera confirmacion",
    "la consulta fue guardada",
    "el producto se encuentra reservado",
    "el sistema muestra el detalle",
    "la orden sigue activa",
    "el panel contiene el resumen",
    "la notificacion queda visible",
    "el formulario conserva los campos",
    "la fecha aparece en el registro",
    "el caso queda para revision",
]

NEGATIVE_BASE = [
    "llego tarde y con problemas",
    "no aclaro nada importante",
    "fue mas confuso de lo necesario",
    "se cerro mientras avanzaba",
    "tardo y no resolvio el caso",
    "fallo durante la primera prueba",
    "no coincidia con lo indicado",
    "llego incompleto",
    "perdio los cambios realizados",
    "termino siendo complicado",
    "fue poco claro",
    "no mostro los datos esperados",
    "dejo dudas sin resolver",
    "se quedo detenido",
    "llego demasiado tarde",
    "fue inestable durante la solicitud",
    "no cumplio con lo indicado",
    "no permitio terminar el proceso",
    "fue insuficiente para continuar",
    "fue cancelado sin aviso claro",
    "dejo una sensacion negativa",
    "mostro errores al guardar",
    "no avanzo despues de varios intentos",
    "quedo sin seguimiento",
    "respondio con informacion incompleta",
    "tomo mas tiempo del esperado",
    "fue dificil de usar",
    "genero varios inconvenientes",
    "llego con fallas visibles",
    "fue breve pero poco util",
    "no dio confianza",
    "fue contradictorio",
    "tuvo demasiados pasos",
    "cargo muy lento",
    "no coincidio con la solicitud",
    "no explico el problema principal",
    "termino de forma decepcionante",
    "fue desordenado",
    "dejo el caso abierto",
    "fallo al finalizar",
    "tuvo bajo rendimiento",
    "no fue cuidadoso",
    "fue lento desde el inicio",
    "quedo sin resolver",
    "no fue suficiente",
    "termino con error",
    "no respondia bien",
    "no explico los pasos",
    "tuvo retrasos repetidos",
    "fue frustrante",
]


def build_rows(base_phrases: list[str], label: str, start_id: int) -> tuple[list[dict[str, object]], int]:
    rows: list[dict[str, object]] = []
    next_id = start_id
    seen: set[str] = set()
    for prefix in PREFIXES:
        for phrase in base_phrases:
            text = f"{prefix}{phrase}".strip()
            if text in seen:
                raise ValueError(f"Texto duplicado en {label}: {text}")
            if len(text) > 120:
                raise ValueError(f"Texto demasiado largo: {text}")
            seen.add(text)
            rows.append(
                {
                    "id": next_id,
                    "texto": text,
                    "sentimiento": label,
                    "fuente": "curated",
                    "version": "v2_curated",
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
        / "dataset_sentimientos_v2_curated_1500.csv"
    )

    rows: list[dict[str, object]] = []
    next_id = 1
    for base, label in [
        (POSITIVE_BASE, "positivo"),
        (NEUTRAL_BASE, "neutral"),
        (NEGATIVE_BASE, "negativo"),
    ]:
        generated, next_id = build_rows(base, label, next_id)
        rows.extend(generated)

    texts = [str(row["texto"]) for row in rows]
    if len(rows) != 1500:
        raise ValueError(f"Conteo inesperado: {len(rows)}")
    if len(set(texts)) != len(texts):
        raise ValueError("Existen duplicados exactos")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "texto", "sentimiento", "fuente", "version"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset curado generado: {output_path}")
    print(f"Registros: {len(rows)}")


if __name__ == "__main__":
    main()
