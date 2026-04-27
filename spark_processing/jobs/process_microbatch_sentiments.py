"""Process simulated sentiment micro-batches with PySpark.

This job is intentionally modular because it is the operational bridge between
the academic baseline model and the end-to-end Big Data pipeline:

microbatch CSV -> PySpark ML -> data/streaming/processed -> optional MongoDB

Supported modes:
- --smoke: validate Spark, input files and schemas without training.
- --train-only: train the baseline pipeline and report labels.
- --process-only: train an in-memory baseline and process micro-batch files.

The model is still a simple academic baseline. It is not a production model and
does not replace later model-selection work.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
import sys
import time
from typing import Any

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.mongo_repository import insert_predictions
from spark_processing.src.project_paths import env_bool, project_root
from spark_processing.src.spark_session_factory import (
    configure_python_for_pyspark,
    create_spark_session,
    import_pyspark_components,
    warn_if_windows_path_has_spaces,
)


TRAINING_DATA = Path("data") / "processed" / "dataset_modelado_sin_duplicados.csv"
DEFAULT_INPUT_PATH = Path("data") / "streaming" / "input" / "microbatch_001.csv"
DEFAULT_OUTPUT_DIR = Path("data") / "streaming" / "processed"
EXPECTED_TRAINING_COLUMNS = {"id", "texto", "texto_preprocesado", "sentimiento"}
EXPECTED_MICROBATCH_COLUMNS = {"texto"}
OUTPUT_COLUMNS = [
    "id",
    "texto",
    "texto_preprocesado",
    "sentimiento",
    "microbatch_id",
    "event_time",
    "prediction",
    "predicted_label",
]


LOGGER = logging.getLogger("sentimentstream.microbatch")


def configure_logger(output_dir: Path) -> Path:
    """Configure console and persistent file logging."""
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "process_microbatch.log"

    LOGGER.handlers.clear()
    LOGGER.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    LOGGER.addHandler(console_handler)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)

    return log_path


def build_pipeline(components: dict[str, Any]):
    """Build the baseline PySpark ML pipeline."""
    return components["Pipeline"](
        stages=[
            components["StringIndexer"](
                inputCol="sentimiento",
                outputCol="label",
                handleInvalid="error",
            ),
            components["Tokenizer"](inputCol="texto_preprocesado", outputCol="tokens"),
            components["StopWordsRemover"](inputCol="tokens", outputCol="filtered_tokens"),
            components["HashingTF"](
                inputCol="filtered_tokens",
                outputCol="raw_features",
                numFeatures=1024,
            ),
            components["IDF"](inputCol="raw_features", outputCol="features"),
            components["NaiveBayes"](
                featuresCol="features",
                labelCol="label",
                predictionCol="prediction",
                modelType="multinomial",
            ),
        ]
    )


def validate_path_exists(path: Path, description: str) -> None:
    """Validate that a required path exists."""
    if not path.exists():
        raise FileNotFoundError(f"No existe {description}: {path}")


def discover_input_files(input_path: Path) -> list[Path]:
    """Return micro-batch CSV files from a file or directory."""
    if input_path.is_file():
        return [input_path]
    validate_path_exists(input_path, "entrada de micro-batches")
    files = sorted(input_path.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No se encontraron CSV de micro-batch en: {input_path}")
    return files


def read_csv(spark: Any, path: Path):
    """Read a CSV with conservative defaults."""
    return spark.read.option("header", True).option("inferSchema", True).csv(str(path))


def validate_columns(df: Any, expected: set[str], context: str) -> None:
    """Validate that a Spark DataFrame contains required columns."""
    missing = expected.difference(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en {context}: {sorted(missing)}")


def ensure_text_preprocessed(df: Any, components: dict[str, Any]):
    """Create texto_preprocesado if a micro-batch does not include it."""
    if "texto_preprocesado" in df.columns:
        return df

    return df.withColumn(
        "texto_preprocesado",
        components["trim"](
            components["regexp_replace"](
                components["regexp_replace"](components["lower"](components["col"]("texto")), r"[\r\n\t]+", " "),
                r"\s+",
                " ",
            )
        ),
    )


def smoke_check(spark: Any, training_path: Path, input_path: Path) -> dict[str, Any]:
    """Validate Spark, training data and micro-batch input without training."""
    LOGGER.info("Iniciando modo smoke.")
    validate_path_exists(training_path, "dataset de entrenamiento")
    input_files = discover_input_files(input_path)

    training_df = read_csv(spark, training_path)
    validate_columns(training_df, EXPECTED_TRAINING_COLUMNS, "dataset de entrenamiento")
    training_count = training_df.count()
    LOGGER.info("Dataset de entrenamiento OK. Filas: %s", training_count)

    batch_df = read_csv(spark, input_files[0])
    validate_columns(batch_df, EXPECTED_MICROBATCH_COLUMNS, f"micro-batch {input_files[0]}")
    batch_count = batch_df.count()
    LOGGER.info("Micro-batch OK: %s. Filas: %s", input_files[0], batch_count)

    return {
        "mode": "smoke",
        "training_rows": training_count,
        "microbatch_file": str(input_files[0]),
        "microbatch_rows": batch_count,
    }


def train_model(spark: Any, components: dict[str, Any], training_path: Path):
    """Train the baseline model from the prepared dataset."""
    validate_path_exists(training_path, "dataset de entrenamiento")

    LOGGER.info("Cargando dataset de entrenamiento: %s", training_path)
    training_df = read_csv(spark, training_path)
    validate_columns(training_df, EXPECTED_TRAINING_COLUMNS, "dataset de entrenamiento")

    training_count = training_df.count()
    LOGGER.info("Filas de entrenamiento detectadas: %s", training_count)
    LOGGER.info("Entrenando pipeline baseline PySpark.")
    pipeline_model = build_pipeline(components).fit(training_df)
    label_model = pipeline_model.stages[0]
    labels = list(label_model.labels)
    LOGGER.info("Modelo entrenado. Etiquetas: %s", labels)
    return pipeline_model, labels, training_count


def dataframe_to_records(df: Any, columns: list[str]) -> list[dict[str, Any]]:
    """Collect a small micro-batch to the driver as dictionaries."""
    selected = df.select(*columns)
    rows = selected.collect()
    records = [row.asDict(recursive=True) for row in rows]
    LOGGER.info("Filas recolectadas al driver: %s", len(records))
    return records


def write_records_csv(records: list[dict[str, Any]], output_path: Path) -> None:
    """Write prediction records with pandas to avoid Hadoop CSV writer on Windows."""
    import pandas as pd

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(".tmp")
    if temp_path.exists():
        temp_path.unlink()

    pd.DataFrame(records).to_csv(temp_path, index=False, encoding="utf-8")
    temp_path.replace(output_path)
    LOGGER.info("CSV de predicciones escrito: %s", output_path)


def process_file(
    spark: Any,
    components: dict[str, Any],
    model: Any,
    labels: list[str],
    input_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """Classify one micro-batch file, write local CSV and optionally persist."""
    LOGGER.info("Procesando micro-batch: %s", input_path)
    batch_df = read_csv(spark, input_path)
    validate_columns(batch_df, EXPECTED_MICROBATCH_COLUMNS, f"micro-batch {input_path}")

    batch_count = batch_df.count()
    LOGGER.info("Filas del micro-batch: %s", batch_count)

    batch_df = ensure_text_preprocessed(batch_df, components)
    LOGGER.info("Aplicando modelo al micro-batch.")
    predictions = model.transform(batch_df)
    predictions = components["IndexToString"](
        inputCol="prediction",
        outputCol="predicted_label",
        labels=labels,
    ).transform(predictions)

    selected_columns = [column for column in OUTPUT_COLUMNS if column in predictions.columns]
    records = dataframe_to_records(predictions, selected_columns)

    output_path = output_dir / f"predictions_{input_path.stem}.csv"
    write_records_csv(records, output_path)

    inserted = 0
    if env_bool("MONGO_ENABLED", False):
        LOGGER.info("Persistiendo predicciones en MongoDB.")
        mongo_records = []
        for record in records:
            document = dict(record)
            document.setdefault("source", "spark_processing")
            document.setdefault("microbatch_source_file", input_path.name)
            mongo_records.append(document)
        inserted = insert_predictions(mongo_records)
        LOGGER.info("Registros insertados en MongoDB: %s", inserted)
    else:
        LOGGER.info("MongoDB deshabilitado por MONGO_ENABLED=false.")

    return {
        "input_file": str(input_path),
        "output_file": str(output_path),
        "rows": batch_count,
        "records_written": len(records),
        "mongo_inserted": inserted,
    }


def process_microbatches(
    spark: Any,
    components: dict[str, Any],
    training_path: Path,
    input_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """Train the in-memory model and process one or more micro-batches."""
    model, labels, training_count = train_model(spark, components, training_path)
    input_files = discover_input_files(input_path)
    LOGGER.info("Micro-batches encontrados: %s", len(input_files))

    outputs = [
        process_file(spark, components, model, labels, file_path, output_dir)
        for file_path in input_files
    ]
    return {
        "mode": "process-only",
        "training_rows": training_count,
        "labels": labels,
        "processed_files": outputs,
    }


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Procesa micro-batches de SentimentStream con PySpark."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--smoke", action="store_true", help="Valida Spark y datos sin entrenar.")
    mode.add_argument("--train-only", action="store_true", help="Entrena el baseline sin procesar micro-batches.")
    mode.add_argument("--process-only", action="store_true", help="Procesa micro-batches con el baseline.")
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
        help="Archivo o carpeta de micro-batches CSV.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directorio donde se guardan predicciones y logs.",
    )
    parser.add_argument(
        "--training-data",
        default=str(TRAINING_DATA),
        help="Dataset preparado para entrenar el baseline.",
    )
    return parser.parse_args()


def resolve_project_path(root: Path, value: str) -> Path:
    """Resolve relative paths against the project root."""
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def run() -> int:
    """Run the selected operational mode."""
    args = parse_args()
    root = project_root()
    input_path = resolve_project_path(root, args.input)
    output_dir = resolve_project_path(root, args.output_dir)
    training_path = resolve_project_path(root, args.training_data)
    log_path = configure_logger(output_dir)

    LOGGER.info("Log persistente: %s", log_path)
    LOGGER.info("Proyecto: %s", root)
    LOGGER.info("Entrada configurada: %s", input_path)
    LOGGER.info("Salida configurada: %s", output_dir)
    LOGGER.info("Dataset de entrenamiento: %s", training_path)

    warn_if_windows_path_has_spaces(root, LOGGER)
    configure_python_for_pyspark(LOGGER)
    components = import_pyspark_components()
    spark = None
    start = time.time()
    try:
        spark = create_spark_session(
            components,
            LOGGER,
            app_name="SentimentStream_MicroBatch_Processing",
        )
        spark.sparkContext.setLogLevel("WARN")

        if args.smoke:
            summary = smoke_check(spark, training_path, input_path)
        elif args.train_only:
            _, labels, training_count = train_model(spark, components, training_path)
            summary = {
                "mode": "train-only",
                "training_rows": training_count,
                "labels": labels,
            }
        else:
            summary = process_microbatches(
                spark,
                components,
                training_path,
                input_path,
                output_dir,
            )

        elapsed = round(time.time() - start, 2)
        LOGGER.info("Ejecucion completada en %s segundos. Resumen: %s", elapsed, summary)
        print(f"Resumen: {summary}")
        return 0
    except Exception:
        LOGGER.exception("Fallo controlado en el procesamiento de micro-batches.")
        return 1
    finally:
        if spark is not None:
            LOGGER.info("Cerrando SparkSession.")
            spark.stop()
            LOGGER.info("SparkSession cerrada.")


if __name__ == "__main__":
    sys.exit(run())
