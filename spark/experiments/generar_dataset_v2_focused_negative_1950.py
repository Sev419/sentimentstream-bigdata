"""Genera dataset focused_negative_1950 desde augmented_1800 + 150 ejemplos."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


NEGATIVE_BASE = [
    "no fue terrible pero esperaba mas claridad",
    "no estuvo fatal pero me dejo dudas",
    "no fue un desastre aunque si resulto flojo",
    "pudo ser peor pero no resolvio lo importante",
    "la respuesta sirvio poco y tarde",
    "el servicio fue correcto en forma pero no en fondo",
    "la entrega llego pero con detalles molestos",
    "el producto funciona a ratos y eso incomoda",
    "la atencion fue amable pero no soluciono",
    "el proceso avanzo pero demasiado lento",
    "la plataforma abre pero se vuelve confusa",
    "la compra se completo aunque con varios tropiezos",
    "el reporte aparece pero no ayuda mucho",
    "la guia explica algo pero deja lo principal afuera",
    "el soporte contesto pero sin resolver",
    "el pedido llego pero no como esperaba",
    "la informacion estaba pero no era suficiente",
    "el sistema guardo parte de los cambios",
    "la experiencia no fue mala del todo pero decepciono",
    "la solucion quedo a medias",
    "el tramite termino pero fue desgastante",
    "la entrega cumplio tarde y con dudas",
    "la respuesta fue educada pero poco util",
    "el producto sirve pero se siente limitado",
    "el servicio no fallo completo pero quedo corto",
]
NEGATIVE_VARIANTS = [
    "y eso pesa en la experiencia",
    "para lo que necesitaba",
    "despues de esperar bastante",
    "sin una mejora clara",
]

POSITIVE_BORDER = [
    "no fue perfecto pero me sirvio bastante",
    "la entrega demoro y aun asi llego bien",
    "tuvo detalles menores pero resolvio",
    "la respuesta fue breve pero suficiente",
    "el proceso empezo confuso y termino claro",
    "no me encanto todo pero cumplio",
    "la plataforma estaba lenta pero funciono",
    "el soporte tardo un poco pero ayudo",
    "el producto tenia detalles pero cumplio",
    "la compra fue regular al inicio y buena al final",
    "la guia no era larga pero si clara",
    "el pedido llego tarde pero completo",
    "la atencion fue simple y efectiva",
    "no tuve una gran experiencia pero salio bien",
    "el tramite tuvo pausas pero quedo resuelto",
    "la informacion era poca pero precisa",
    "el sistema se demoro pero guardo todo",
    "la solucion fue sencilla y funciono",
    "la respuesta aclaro lo necesario",
    "el servicio cerro bien el caso",
    "la experiencia mejoro al final",
    "el seguimiento fue suficiente",
    "el producto funciono mejor de lo esperado",
    "la entrega llego cuidada",
    "la herramienta ayudo con la tarea",
]

NEUTRAL_BORDER = [
    "el pedido llego despues de la hora estimada",
    "la solicitud sigue abierta sin comentario adicional",
    "el sistema muestra un aviso de revision",
    "la factura quedo disponible despues del cierre",
    "el documento aparece con estado pendiente",
    "la consulta fue enviada nuevamente",
    "el reporte muestra datos parciales",
    "la entrega figura como reprogramada",
    "la orden permanece en seguimiento",
    "el mensaje quedo marcado para revision",
    "la respuesta indica que falta validacion",
    "el producto aparece con observaciones",
    "el tramite continua sin cambio visible",
    "la pantalla muestra una alerta informativa",
    "el archivo esta disponible con nota",
    "la consulta quedo en espera",
    "el registro incluye una actualizacion",
    "la entrega tiene nueva fecha",
    "el sistema genero un estado intermedio",
    "la solicitud fue recibida sin decision",
    "el producto sigue reservado",
    "la respuesta esta pendiente",
    "el reporte fue actualizado parcialmente",
    "la informacion queda para revision",
    "el caso sigue abierto",
]


def main() -> None:
    root = project_root()
    base_path = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_augmented_1800.csv"
    output_path = root / "data" / "experiments" / "dataset_v2" / "labeled" / "dataset_sentimientos_v2_focused_negative_1950.csv"
    base = pd.read_csv(base_path, encoding="utf-8")
    rows = []
    next_id = 1
    for _, row in base.iterrows():
        rows.append({"id": next_id, "texto": row["texto"], "sentimiento": row["sentimiento"], "fuente": "augmented", "version": "v2_augmented"})
        next_id += 1
    for text in [f"{base_text} {variant}" for base_text in NEGATIVE_BASE for variant in NEGATIVE_VARIANTS]:
        rows.append({"id": next_id, "texto": text, "sentimiento": "negativo", "fuente": "augmented", "version": "v2_augmented"})
        next_id += 1
    for text in POSITIVE_BORDER:
        rows.append({"id": next_id, "texto": text, "sentimiento": "positivo", "fuente": "augmented", "version": "v2_augmented"})
        next_id += 1
    for text in NEUTRAL_BORDER:
        rows.append({"id": next_id, "texto": text, "sentimiento": "neutral", "fuente": "augmented", "version": "v2_augmented"})
        next_id += 1
    texts = [str(row["texto"]) for row in rows]
    if len(rows) != 1950:
        raise ValueError(f"Conteo inesperado: {len(rows)}")
    if len(set(texts)) != len(texts):
        raise ValueError("Duplicados exactos detectados")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "texto", "sentimiento", "fuente", "version"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Dataset focused generado: {output_path}")
    print(f"Registros: {len(rows)}")


if __name__ == "__main__":
    main()
