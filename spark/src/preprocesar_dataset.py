"""Preprocesamiento inicial y conservador del dataset SentimentStream.

Fase 3:
- Carga el dataset normalizado desde data/processed.
- Valida la estructura esperada: id, texto y sentimiento.
- Crea texto_preprocesado con reglas basicas y trazables.
- Conserva id, texto original, sentimiento, filas y duplicados.

Esta fase no elimina stopwords, no aplica stemming ni lematizacion, no entrena
modelos, no usa PySpark, no persiste en MongoDB y no implementa API ni
infraestructura.
"""

from pathlib import Path
import re

import pandas as pd


INPUT_RELATIVE_PATH = (
    Path("data") / "processed" / "dataset_sentimientos_normalizado.csv"
)
OUTPUT_RELATIVE_PATH = (
    Path("data") / "processed" / "dataset_sentimientos_preprocesado.csv"
)

INPUT_COLUMNS = ("id", "texto", "sentimiento")
OUTPUT_COLUMNS = ("id", "texto", "texto_preprocesado", "sentimiento")

CONTROL_CHARS_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
WHITESPACE_PATTERN = re.compile(r"\s+")


def get_project_root() -> Path:
    """Return the project root based on this script location."""
    return Path(__file__).resolve().parents[2]


def validate_input_dataset(df: pd.DataFrame, input_path: Path) -> None:
    """Validate the expected normalized dataset structure."""
    missing_columns = [column for column in INPUT_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(
            "El dataset normalizado no tiene la estructura esperada. "
            f"Columnas faltantes: {missing_columns}. "
            f"Columnas encontradas: {list(df.columns)}. "
            f"Archivo revisado: {input_path}"
        )


def preprocess_text(value: object) -> str:
    """Apply minimal text preprocessing without changing semantic content."""
    if pd.isna(value):
        return ""

    text = str(value)
    text = CONTROL_CHARS_PATTERN.sub(" ", text)
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = text.lower()
    text = WHITESPACE_PATTERN.sub(" ", text).strip()

    return text


def validate_output_dataset(
    df_input: pd.DataFrame,
    df_output: pd.DataFrame,
    output_path: Path,
) -> None:
    """Validate the preprocessed file after writing it to disk."""
    if not output_path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo preprocesado esperado en: {output_path}"
        )

    if tuple(df_output.columns) != OUTPUT_COLUMNS:
        raise ValueError(
            "El dataset preprocesado no tiene las columnas esperadas. "
            f"Columnas esperadas: {list(OUTPUT_COLUMNS)}. "
            f"Columnas encontradas: {list(df_output.columns)}."
        )

    if len(df_output) != len(df_input):
        raise ValueError(
            "El dataset preprocesado no conserva el numero de filas de entrada. "
            f"Filas entrada: {len(df_input)}. Filas salida: {len(df_output)}."
        )

    if not df_input["id"].reset_index(drop=True).equals(
        df_output["id"].reset_index(drop=True)
    ):
        raise ValueError("La columna id fue alterada durante el preprocesamiento.")

    if not df_input["texto"].reset_index(drop=True).equals(
        df_output["texto"].reset_index(drop=True)
    ):
        raise ValueError("La columna texto original fue alterada.")

    if not df_input["sentimiento"].reset_index(drop=True).equals(
        df_output["sentimiento"].reset_index(drop=True)
    ):
        raise ValueError("La columna sentimiento fue alterada.")

    empty_preprocessed = int(
        df_output["texto_preprocesado"].fillna("").astype(str).str.strip().eq("").sum()
    )
    if len(df_output) > 0 and empty_preprocessed == len(df_output):
        raise ValueError("Todos los textos preprocesados quedaron vacios.")


def preprocess_dataset(input_path: Path, output_path: Path) -> tuple[pd.DataFrame, int]:
    """Create and write the initial preprocessed dataset."""
    if not input_path.exists():
        raise FileNotFoundError(
            f"No se encontro el dataset normalizado esperado en: {input_path}"
        )

    df_input = pd.read_csv(input_path)
    validate_input_dataset(df_input, input_path)

    df_output = pd.DataFrame(
        {
            "id": df_input["id"],
            "texto": df_input["texto"],
            "texto_preprocesado": df_input["texto"].apply(preprocess_text),
            "sentimiento": df_input["sentimiento"],
        },
        columns=OUTPUT_COLUMNS,
    )

    changed_texts = int(
        (df_output["texto"].astype(str) != df_output["texto_preprocesado"]).sum()
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_output.to_csv(output_path, index=False, encoding="utf-8")

    df_saved = pd.read_csv(output_path)
    validate_output_dataset(df_input, df_saved, output_path)

    return df_saved, changed_texts


def main() -> None:
    """Run the initial preprocessing process."""
    project_root = get_project_root()
    input_path = project_root / INPUT_RELATIVE_PATH
    output_path = project_root / OUTPUT_RELATIVE_PATH

    df_preprocessed, changed_texts = preprocess_dataset(input_path, output_path)
    duplicate_count = int(
        df_preprocessed.duplicated(["texto", "sentimiento"]).sum()
    )
    empty_preprocessed = int(
        df_preprocessed["texto_preprocesado"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    print("Preprocesamiento inicial completado.")
    print(f"Archivo de entrada: {input_path}")
    print(f"Archivo de salida: {output_path}")
    print(f"Registros procesados: {len(df_preprocessed)}")
    print(f"Columnas finales: {list(df_preprocessed.columns)}")
    print(f"Textos modificados por reglas iniciales: {changed_texts}")
    print(f"Textos preprocesados vacios: {empty_preprocessed}")
    print(f"Duplicados de contenido conservados: {duplicate_count}")
    print("Validacion de salida: correcta.")
    print("Nota: no se eliminaron duplicados, stopwords ni se aplico modelado.")


if __name__ == "__main__":
    main()
