"""Centralized SparkSession startup helpers for SentimentStream.

The local Windows runtime has already shown that Spark may hang before the
pipeline starts. Keeping all Spark startup settings here makes diagnostics and
Docker fallback easier to maintain.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
import sys
from typing import Any


def configure_python_for_pyspark(logger: logging.Logger | None = None) -> str:
    """Force PySpark driver and workers to use the current Python executable."""
    python_executable = sys.executable
    os.environ["PYSPARK_PYTHON"] = python_executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = python_executable
    if logger:
        logger.info("PYSPARK_PYTHON=%s", python_executable)
        logger.info("PYSPARK_DRIVER_PYTHON=%s", python_executable)
    return python_executable


def warn_if_windows_path_has_spaces(project_path: Path, logger: logging.Logger) -> None:
    """Warn about a known Windows/Spark risk: paths containing spaces."""
    if os.name == "nt" and " " in str(project_path):
        logger.warning(
            "La ruta del proyecto contiene espacios: %s. En Windows esto puede "
            "afectar el arranque de Spark/JVM. Si Spark se cuelga, pruebe mover "
            "el proyecto a una ruta sin espacios o ejecutar la capa Spark en Docker.",
            project_path,
        )


def import_pyspark_components() -> dict[str, Any]:
    """Import PySpark lazily so callers can log a clean error if it is missing."""
    try:
        from pyspark.ml import Pipeline
        from pyspark.ml.classification import NaiveBayes
        from pyspark.ml.feature import (
            HashingTF,
            IDF,
            IndexToString,
            StopWordsRemover,
            StringIndexer,
            Tokenizer,
        )
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col, lower, regexp_replace, trim
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "No se pudo importar PySpark. Ejecute "
            "`python spark\\src\\verificar_entorno_pyspark.py` y confirme "
            "que pyspark y Java esten disponibles."
        ) from exc

    return {
        "Pipeline": Pipeline,
        "NaiveBayes": NaiveBayes,
        "HashingTF": HashingTF,
        "IDF": IDF,
        "IndexToString": IndexToString,
        "StopWordsRemover": StopWordsRemover,
        "StringIndexer": StringIndexer,
        "Tokenizer": Tokenizer,
        "SparkSession": SparkSession,
        "col": col,
        "lower": lower,
        "regexp_replace": regexp_replace,
        "trim": trim,
    }


def create_spark_session(
    components: dict[str, Any],
    logger: logging.Logger,
    app_name: str = "SentimentStream",
):
    """Create a small local SparkSession with conservative Windows settings."""
    spark_master = os.environ.get("SPARK_MASTER", "local[1]")
    shuffle_partitions = os.environ.get("SPARK_SHUFFLE_PARTITIONS", "1")
    default_parallelism = os.environ.get("SPARK_DEFAULT_PARALLELISM", "1")
    bind_address = os.environ.get("SPARK_DRIVER_BIND_ADDRESS", "127.0.0.1")
    driver_host = os.environ.get("SPARK_DRIVER_HOST", "127.0.0.1")

    logger.info(
        "Creando SparkSession app=%s master=%s shuffle=%s parallelism=%s bind=%s host=%s",
        app_name,
        spark_master,
        shuffle_partitions,
        default_parallelism,
        bind_address,
        driver_host,
    )

    spark = (
        components["SparkSession"]
        .builder.appName(app_name)
        .master(spark_master)
        .config("spark.sql.shuffle.partitions", shuffle_partitions)
        .config("spark.default.parallelism", default_parallelism)
        .config("spark.ui.enabled", os.environ.get("SPARK_UI_ENABLED", "false"))
        .config("spark.sql.adaptive.enabled", os.environ.get("SPARK_SQL_ADAPTIVE_ENABLED", "false"))
        .config("spark.driver.bindAddress", bind_address)
        .config("spark.driver.host", driver_host)
        .config("spark.pyspark.python", sys.executable)
        .config("spark.pyspark.driver.python", sys.executable)
        .config("spark.executorEnv.PYSPARK_PYTHON", sys.executable)
        .config("spark.python.worker.faulthandler.enabled", "true")
        .getOrCreate()
    )
    logger.info("SparkSession creada correctamente.")
    return spark
