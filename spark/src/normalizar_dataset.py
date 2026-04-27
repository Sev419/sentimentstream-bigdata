"""Normalizacion estructural minima del dataset de SentimentStream.

Fase 2.5:
- Carga el dataset original desde data/raw.
- Valida que existan las columnas reales esperadas: texto y etiqueta.
- Genera un id tecnico secuencial porque el archivo original no lo trae.
- Renombra etiqueta a sentimiento.
- Conserva textos, etiquetas y duplicados sin limpieza avanzada.

Esta fase no realiza preprocesamiento NLP, deduplicacion, modelado,
persistencia, API ni configuracion de infraestructura.
"""

from pathlib import Path

import pandas as pd


RAW_RELATIVE_PATH = Path("data") / "raw" / "dataset_sentimientos_500.csv"
PROCESSED_RELATIVE_PATH = (
    Path("data") / "processed" / "dataset_sentimientos_normalizado.csv"
)

REQUIRED_COLUMNS = ("texto", "etiqueta")
OUTPUT_COLUMNS = ("id", "texto", "sentimiento")


def get_project_root() -> Path:
    """Return the project root based on this script location."""
    return Path(__file__).resolve().parents[2]


def validate_input_columns(df: pd.DataFrame) -> None:
    """Validate that the raw dataset contains the expected real columns."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(
            "El dataset raw no tiene la estructura esperada. "
            f"Columnas faltantes: {missing_columns}. "
            f"Columnas encontradas: {list(df.columns)}."
        )


def validate_output_dataset(
    df_raw: pd.DataFrame, df_normalized: pd.DataFrame, processed_path: Path
) -> None:
    """Validate the normalized file after writing it to disk."""
    if not processed_path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo normalizado esperado en: {processed_path}"
        )

    if tuple(df_normalized.columns) != OUTPUT_COLUMNS:
        raise ValueError(
            "El dataset normalizado no tiene las columnas esperadas. "
            f"Columnas esperadas: {list(OUTPUT_COLUMNS)}. "
            f"Columnas encontradas: {list(df_normalized.columns)}."
        )

    if len(df_normalized) != len(df_raw):
        raise ValueError(
            "El dataset normalizado no conserva el numero de filas del dataset raw. "
            f"Filas raw: {len(df_raw)}. Filas normalizadas: {len(df_normalized)}."
        )

    expected_ids = pd.Series(range(1, len(df_normalized) + 1), name="id")
    if not df_normalized["id"].reset_index(drop=True).equals(expected_ids):
        raise ValueError("La columna id no es secuencial desde 1 hasta N.")

    if not df_raw["texto"].reset_index(drop=True).equals(
        df_normalized["texto"].reset_index(drop=True)
    ):
        raise ValueError("La columna texto fue alterada durante la normalizacion.")

    if not df_raw["etiqueta"].reset_index(drop=True).equals(
        df_normalized["sentimiento"].reset_index(drop=True)
    ):
        raise ValueError("La columna etiqueta/sentimiento fue alterada.")


def normalize_dataset(raw_path: Path, processed_path: Path) -> pd.DataFrame:
    """Create the structurally normalized dataset and write it to CSV."""
    if not raw_path.exists():
        raise FileNotFoundError(f"No se encontro el dataset raw en: {raw_path}")

    df_raw = pd.read_csv(raw_path)
    validate_input_columns(df_raw)

    df_normalized = pd.DataFrame(
        {
            "id": range(1, len(df_raw) + 1),
            "texto": df_raw["texto"],
            "sentimiento": df_raw["etiqueta"],
        },
        columns=OUTPUT_COLUMNS,
    )

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df_normalized.to_csv(processed_path, index=False, encoding="utf-8")

    df_saved = pd.read_csv(processed_path)
    validate_output_dataset(df_raw, df_saved, processed_path)

    return df_saved


def main() -> None:
    """Run the structural normalization process."""
    project_root = get_project_root()
    raw_path = project_root / RAW_RELATIVE_PATH
    processed_path = project_root / PROCESSED_RELATIVE_PATH

    df_normalized = normalize_dataset(raw_path, processed_path)

    duplicate_count = int(
        df_normalized.duplicated(["texto", "sentimiento"]).sum()
    )

    print("Normalizacion estructural completada.")
    print(f"Archivo raw: {raw_path}")
    print(f"Archivo normalizado: {processed_path}")
    print(f"Registros generados: {len(df_normalized)}")
    print(f"Columnas finales: {list(df_normalized.columns)}")
    print(f"Duplicados de contenido conservados: {duplicate_count}")
    print("Validacion de salida: correcta.")
    print("Nota: no se eliminaron duplicados ni se realizo limpieza avanzada.")


if __name__ == "__main__":
    main()
