"""Preparacion conservadora del dataset para modelado futuro.

Fase 4:
- Carga el dataset preprocesado.
- Valida la estructura esperada.
- Analiza duplicados completos con criterio metodologico explicito.
- Genera una version de trabajo con duplicados conservados.
- Genera una version alternativa sin duplicados completos.

Esta fase no entrena modelos, no construye TF-IDF, no realiza split train/test,
no usa PySpark, no persiste en MongoDB y no implementa API ni infraestructura.
"""

from pathlib import Path

import pandas as pd


INPUT_RELATIVE_PATH = (
    Path("data") / "processed" / "dataset_sentimientos_preprocesado.csv"
)
WITH_DUPLICATES_RELATIVE_PATH = (
    Path("data") / "processed" / "dataset_modelado_con_duplicados.csv"
)
WITHOUT_DUPLICATES_RELATIVE_PATH = (
    Path("data") / "processed" / "dataset_modelado_sin_duplicados.csv"
)

EXPECTED_COLUMNS = ("id", "texto", "texto_preprocesado", "sentimiento")
DUPLICATE_CRITERIA = ("texto", "texto_preprocesado", "sentimiento")


def get_project_root() -> Path:
    """Return the project root based on this script location."""
    return Path(__file__).resolve().parents[2]


def validate_input_dataset(df: pd.DataFrame, input_path: Path) -> None:
    """Validate that the preprocessed dataset has the expected columns."""
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(
            "El dataset preprocesado no tiene la estructura esperada. "
            f"Columnas faltantes: {missing_columns}. "
            f"Columnas encontradas: {list(df.columns)}. "
            f"Archivo revisado: {input_path}"
        )


def validate_modeling_dataset(
    df_reference: pd.DataFrame,
    df_output: pd.DataFrame,
    output_path: Path,
    require_same_rows: bool,
) -> None:
    """Validate a generated modeling dataset."""
    if not output_path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de modelado esperado en: {output_path}"
        )

    if tuple(df_output.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            "El dataset de modelado no conserva las columnas esperadas. "
            f"Columnas esperadas: {list(EXPECTED_COLUMNS)}. "
            f"Columnas encontradas: {list(df_output.columns)}."
        )

    if require_same_rows and len(df_output) != len(df_reference):
        raise ValueError(
            "El dataset con duplicados no conserva todas las filas de entrada. "
            f"Filas entrada: {len(df_reference)}. Filas salida: {len(df_output)}."
        )

    if not require_same_rows and len(df_output) > len(df_reference):
        raise ValueError(
            "El dataset sin duplicados tiene mas filas que el dataset de entrada. "
            f"Filas entrada: {len(df_reference)}. Filas salida: {len(df_output)}."
        )

    if not set(df_output["sentimiento"].dropna().unique()).issubset(
        set(df_reference["sentimiento"].dropna().unique())
    ):
        raise ValueError("El dataset de salida contiene sentimientos no presentes en la entrada.")


def prepare_modeling_datasets(
    input_path: Path,
    with_duplicates_path: Path,
    without_duplicates_path: Path,
) -> dict[str, object]:
    """Create modeling datasets with and without complete duplicates."""
    if not input_path.exists():
        raise FileNotFoundError(
            f"No se encontro el dataset preprocesado esperado en: {input_path}"
        )

    df_input = pd.read_csv(input_path)
    validate_input_dataset(df_input, input_path)

    duplicate_mask = df_input.duplicated(subset=DUPLICATE_CRITERIA, keep="first")
    duplicate_count = int(duplicate_mask.sum())

    df_with_duplicates = df_input.loc[:, EXPECTED_COLUMNS].copy()
    df_without_duplicates = (
        df_input.drop_duplicates(subset=DUPLICATE_CRITERIA, keep="first")
        .loc[:, EXPECTED_COLUMNS]
        .copy()
    )

    with_duplicates_path.parent.mkdir(parents=True, exist_ok=True)
    df_with_duplicates.to_csv(with_duplicates_path, index=False, encoding="utf-8")
    df_without_duplicates.to_csv(without_duplicates_path, index=False, encoding="utf-8")

    df_with_saved = pd.read_csv(with_duplicates_path)
    df_without_saved = pd.read_csv(without_duplicates_path)

    validate_modeling_dataset(
        df_input,
        df_with_saved,
        with_duplicates_path,
        require_same_rows=True,
    )
    validate_modeling_dataset(
        df_input,
        df_without_saved,
        without_duplicates_path,
        require_same_rows=False,
    )

    remaining_duplicates = int(
        df_without_saved.duplicated(subset=DUPLICATE_CRITERIA, keep="first").sum()
    )
    if remaining_duplicates != 0:
        raise ValueError(
            "El dataset sin duplicados aun contiene duplicados completos bajo el criterio definido. "
            f"Duplicados restantes: {remaining_duplicates}."
        )

    return {
        "input_rows": len(df_input),
        "duplicate_count": duplicate_count,
        "unique_rows": len(df_without_saved),
        "with_duplicates_rows": len(df_with_saved),
        "without_duplicates_rows": len(df_without_saved),
        "duplicate_criteria": list(DUPLICATE_CRITERIA),
        "input_class_counts": df_input["sentimiento"].value_counts(dropna=False).to_dict(),
        "unique_class_counts": df_without_saved["sentimiento"].value_counts(dropna=False).to_dict(),
    }


def main() -> None:
    """Run the modeling preparation process."""
    project_root = get_project_root()
    input_path = project_root / INPUT_RELATIVE_PATH
    with_duplicates_path = project_root / WITH_DUPLICATES_RELATIVE_PATH
    without_duplicates_path = project_root / WITHOUT_DUPLICATES_RELATIVE_PATH

    summary = prepare_modeling_datasets(
        input_path,
        with_duplicates_path,
        without_duplicates_path,
    )

    print("Preparacion para modelado completada.")
    print(f"Archivo de entrada: {input_path}")
    print(f"Dataset con duplicados: {with_duplicates_path}")
    print(f"Dataset sin duplicados: {without_duplicates_path}")
    print(f"Filas de entrada: {summary['input_rows']}")
    print(f"Duplicados detectados: {summary['duplicate_count']}")
    print(f"Filas con duplicados: {summary['with_duplicates_rows']}")
    print(f"Filas sin duplicados: {summary['without_duplicates_rows']}")
    print(f"Criterio de duplicado: {summary['duplicate_criteria']}")
    print(f"Distribucion original: {summary['input_class_counts']}")
    print(f"Distribucion sin duplicados: {summary['unique_class_counts']}")
    print("Validacion de salidas: correcta.")
    print("Nota: no se entreno ningun modelo ni se construyo TF-IDF.")


if __name__ == "__main__":
    main()
