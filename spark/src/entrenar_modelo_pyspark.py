"""Modelado inicial de sentimientos con PySpark.

Fase 5:
- Usa el dataset sin duplicados como entrada principal.
- Construye un pipeline simple de NLP con PySpark ML.
- Entrena un clasificador Naive Bayes.
- Guarda metricas basicas, predicciones de ejemplo y reporte metodologico.

Esta fase no usa MongoDB, no crea API, no usa Docker, no crea Jenkinsfile,
no genera dashboard y no realiza despliegue.
"""

from __future__ import annotations

from pathlib import Path
import importlib.util
import json
import os
import subprocess
import shutil
import sys


INPUT_RELATIVE_PATH = (
    Path("data") / "processed" / "dataset_modelado_sin_duplicados.csv"
)
METRICS_RELATIVE_PATH = Path("spark") / "outputs" / "metricas_modelo_inicial.json"
PREDICTIONS_RELATIVE_PATH = (
    Path("spark") / "outputs" / "predicciones_modelo_inicial.csv"
)
REPORT_RELATIVE_PATH = Path("docs") / "pruebas" / "reporte_modelado_inicial.md"

EXPECTED_COLUMNS = ("id", "texto", "texto_preprocesado", "sentimiento")
TEXT_COLUMN = "texto_preprocesado"
LABEL_COLUMN = "sentimiento"
TRAIN_RATIO = 0.70
RANDOM_SEED = 42
NUM_FEATURES = 1024


class EnvironmentNotReadyError(RuntimeError):
    """Raised when local prerequisites for PySpark execution are missing."""


def get_project_root() -> Path:
    """Return the project root based on this script location."""
    return Path(__file__).resolve().parents[2]


def configure_pyspark_python() -> dict[str, str]:
    """Force PySpark driver and workers to use the current Python executable.

    On Windows it is common to have multiple Python installations. If Spark
    workers resolve a different Python than the driver, PySpark raises
    PYTHON_VERSION_MISMATCH. Setting both variables before SparkSession is
    created keeps driver and worker on the same interpreter.
    """
    python_executable = sys.executable
    os.environ["PYSPARK_PYTHON"] = python_executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = python_executable

    return {
        "PYSPARK_PYTHON": os.environ["PYSPARK_PYTHON"],
        "PYSPARK_DRIVER_PYTHON": os.environ["PYSPARK_DRIVER_PYTHON"],
    }


def command_diagnostic(command: str, version_args: list[str]) -> dict[str, object]:
    """Check whether a command exists and capture a short version message."""
    executable = shutil.which(command)
    if executable is None:
        return {
            "ok": False,
            "path": None,
            "detail": f"Comando '{command}' no encontrado en PATH.",
        }

    try:
        result = subprocess.run(
            [executable, *version_args],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001 - diagnostic only.
        return {
            "ok": False,
            "path": executable,
            "detail": f"Comando encontrado, pero no pudo ejecutarse: {exc}",
        }

    version_text = (result.stdout or result.stderr or "").strip().splitlines()
    detail = version_text[0] if version_text else "Comando encontrado."

    return {
        "ok": result.returncode == 0,
        "path": executable,
        "detail": detail,
    }


def validate_execution_environment() -> dict[str, dict[str, object]]:
    """Validate prerequisites before importing or creating Spark objects."""
    pyspark_available = importlib.util.find_spec("pyspark") is not None
    diagnostics = {
        "pyspark": {
            "ok": pyspark_available,
            "detail": "Modulo pyspark importable."
            if pyspark_available
            else "Modulo pyspark no disponible para el Python actual.",
        },
        "java": command_diagnostic("java", ["-version"]),
        "spark-submit": command_diagnostic("spark-submit", ["--version"]),
    }

    required_failures = [
        name for name in ("pyspark", "java") if not diagnostics[name]["ok"]
    ]

    if required_failures:
        detail_lines = [
            f"- {name}: {'OK' if data['ok'] else 'NO OK'} - {data['detail']}"
            for name, data in diagnostics.items()
        ]
        raise EnvironmentNotReadyError(
            "El entorno local no esta listo para ejecutar la Fase 5 con PySpark.\n"
            + "\n".join(detail_lines)
            + "\n\nAccion sugerida: habilite un entorno con Python, pyspark y Java "
            "antes de volver a ejecutar el entrenamiento. No se generaron "
            "metricas ni predicciones."
        )

    return diagnostics


def import_pyspark_components() -> dict[str, object]:
    """Import PySpark lazily to provide a clear error when it is unavailable."""
    try:
        from pyspark.ml import Pipeline
        from pyspark.ml.classification import NaiveBayes
        from pyspark.ml.evaluation import MulticlassClassificationEvaluator
        from pyspark.ml.feature import HashingTF, IDF, IndexToString, StopWordsRemover, StringIndexer, Tokenizer
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import col, count, floor, lit, rand, row_number, when
        from pyspark.sql.window import Window
    except ModuleNotFoundError as exc:
        raise EnvironmentNotReadyError(
            "PySpark no esta disponible en el entorno actual. "
            "Instale o habilite pyspark y Java antes de ejecutar la Fase 5. "
            "No se generaron metricas ni predicciones para evitar resultados ficticios."
        ) from exc

    return {
        "Pipeline": Pipeline,
        "NaiveBayes": NaiveBayes,
        "MulticlassClassificationEvaluator": MulticlassClassificationEvaluator,
        "HashingTF": HashingTF,
        "IDF": IDF,
        "IndexToString": IndexToString,
        "StopWordsRemover": StopWordsRemover,
        "StringIndexer": StringIndexer,
        "Tokenizer": Tokenizer,
        "SparkSession": SparkSession,
        "col": col,
        "count": count,
        "floor": floor,
        "lit": lit,
        "rand": rand,
        "row_number": row_number,
        "when": when,
        "Window": Window,
    }


def validate_input_path(input_path: Path) -> None:
    """Validate that the modeling dataset exists."""
    if not input_path.exists():
        raise FileNotFoundError(
            f"No se encontro el dataset de entrada esperado en: {input_path}"
        )


def create_spark_session(components: dict[str, object]):
    """Create a local SparkSession for the initial academic model."""
    spark_session_cls = components["SparkSession"]
    python_executable = sys.executable
    try:
        spark = (
            spark_session_cls.builder.appName("SentimentStream_Fase5_ModeladoInicial")
            .master("local[*]")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.pyspark.python", python_executable)
            .config("spark.pyspark.driver.python", python_executable)
            .config("spark.executorEnv.PYSPARK_PYTHON", python_executable)
            .getOrCreate()
        )
    except Exception as exc:  # noqa: BLE001 - Spark often wraps Java errors.
        raise EnvironmentNotReadyError(
            "No se pudo crear SparkSession. Revise que Java y PySpark esten "
            f"correctamente configurados. Detalle: {exc}"
        ) from exc

    if spark is None:
        raise EnvironmentNotReadyError("No se pudo crear SparkSession.")

    return spark


def validate_columns(df) -> None:
    """Validate that the Spark DataFrame contains the expected columns."""
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(
            "El dataset de entrada no tiene la estructura esperada. "
            f"Columnas faltantes: {missing_columns}. "
            f"Columnas encontradas: {df.columns}."
        )


def validate_no_required_nulls(df, components: dict[str, object]) -> None:
    """Stop early if required columns contain null values."""
    col = components["col"]
    required_nulls = {
        column: df.filter(col(column).isNull()).count() for column in EXPECTED_COLUMNS
    }
    columns_with_nulls = {
        column: count_value
        for column, count_value in required_nulls.items()
        if count_value > 0
    }

    if columns_with_nulls:
        raise ValueError(
            "El dataset contiene nulos en columnas requeridas. "
            f"Detalle: {columns_with_nulls}."
        )


def build_stratified_split(df, components: dict[str, object]):
    """Create a simple stratified train/test split by sentiment label."""
    col = components["col"]
    count = components["count"]
    floor = components["floor"]
    lit = components["lit"]
    rand = components["rand"]
    row_number = components["row_number"]
    when = components["when"]
    Window = components["Window"]

    label_window = Window.partitionBy(LABEL_COLUMN)
    random_window = label_window.orderBy(rand(RANDOM_SEED))

    ranked = (
        df.withColumn("__label_count", count(lit(1)).over(label_window))
        .withColumn("__row_number", row_number().over(random_window))
        .withColumn(
            "__train_limit",
            when(
                col("__label_count") <= lit(1),
                col("__label_count"),
            ).otherwise(floor(col("__label_count") * lit(TRAIN_RATIO))),
        )
    )

    train_df = ranked.filter(col("__row_number") <= col("__train_limit")).drop(
        "__label_count", "__row_number", "__train_limit"
    )
    test_df = ranked.filter(col("__row_number") > col("__train_limit")).drop(
        "__label_count", "__row_number", "__train_limit"
    )

    train_count = train_df.count()
    test_count = test_df.count()

    if train_count == 0 or test_count == 0:
        raise ValueError(
            "La particion train/test produjo un conjunto vacio. "
            f"Train: {train_count}. Test: {test_count}."
        )

    return train_df, test_df


def build_pipeline(components: dict[str, object]):
    """Build the initial NLP classification pipeline."""
    Pipeline = components["Pipeline"]
    NaiveBayes = components["NaiveBayes"]
    HashingTF = components["HashingTF"]
    IDF = components["IDF"]
    StopWordsRemover = components["StopWordsRemover"]
    StringIndexer = components["StringIndexer"]
    Tokenizer = components["Tokenizer"]

    label_indexer = StringIndexer(
        inputCol=LABEL_COLUMN,
        outputCol="label",
        handleInvalid="error",
    )
    tokenizer = Tokenizer(inputCol=TEXT_COLUMN, outputCol="tokens")
    stopwords = StopWordsRemover(inputCol="tokens", outputCol="filtered_tokens")
    hashing_tf = HashingTF(
        inputCol="filtered_tokens",
        outputCol="raw_features",
        numFeatures=NUM_FEATURES,
    )
    idf = IDF(inputCol="raw_features", outputCol="features")
    classifier = NaiveBayes(
        featuresCol="features",
        labelCol="label",
        predictionCol="prediction",
        modelType="multinomial",
    )

    return Pipeline(
        stages=[label_indexer, tokenizer, stopwords, hashing_tf, idf, classifier]
    )


def add_predicted_label(predictions, pipeline_model, components: dict[str, object]):
    """Map numeric predictions back to readable sentiment labels without Python UDF."""
    IndexToString = components["IndexToString"]

    label_model = pipeline_model.stages[0]
    labels = list(label_model.labels)

    converter = IndexToString(
        inputCol="prediction",
        outputCol="predicted_label",
        labels=labels,
    )

    return converter.transform(predictions), labels


def write_predictions_csv_without_hadoop(df, output_path: Path) -> None:
    """Write predictions locally without Spark DataFrameWriter.

    On Windows, Spark's DataFrameWriter uses Hadoop local filesystem helpers
    and can require winutils.exe through HADOOP_HOME. The prediction dataset is
    intentionally small in this academic phase, so collecting the selected
    prediction rows to the driver and writing with pandas avoids that Windows
    filesystem dependency without changing the PySpark training pipeline.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        output_path.unlink()

    pandas_df = df.toPandas()
    pandas_df.to_csv(output_path, index=False, encoding="utf-8")


def write_metrics(metrics_path: Path, metrics: dict[str, object]) -> None:
    """Write model metrics as JSON."""
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_report(report_path: Path, metrics: dict[str, object]) -> None:
    """Write the short methodological modeling report."""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = f"""# Reporte de modelado inicial con PySpark

## Fase

Fase 5 - Primer modelado con PySpark.

## Dataset utilizado

`{metrics["dataset_utilizado"]}`

Se uso la version sin duplicados porque en la Fase 4 se identifico una alta cantidad de repeticiones completas. Esta decision reduce el riesgo de que ejemplos identicos inflen artificialmente las metricas iniciales.

## Columnas utilizadas

- Texto principal: `{metrics["columna_texto"]}`
- Etiqueta: `{metrics["etiqueta_usada"]}`

## Configuracion Python para PySpark

- Python del driver: `{metrics["python_executable"]}`
- PYSPARK_PYTHON: `{metrics["pyspark_python"]}`
- PYSPARK_DRIVER_PYTHON: `{metrics["pyspark_driver_python"]}`

Estas variables se fijan antes de crear SparkSession para evitar `PYTHON_VERSION_MISMATCH` entre driver y workers en Windows.

## Etapas del pipeline

1. Carga del CSV con Spark.
2. Validacion de columnas esperadas.
3. Indexacion de la etiqueta `sentimiento`.
4. Tokenizacion de `texto_preprocesado`.
5. Eliminacion de stopwords.
6. Vectorizacion con HashingTF.
7. Aplicacion de IDF.
8. Entrenamiento de NaiveBayes.
9. Evaluacion con metricas basicas.

## Particion usada

- Estrategia: particion estratificada simple por clase.
- Proporcion aproximada: {int(TRAIN_RATIO * 100)}% entrenamiento y {100 - int(TRAIN_RATIO * 100)}% prueba.
- Filas de entrenamiento: {metrics["train_size"]}.
- Filas de prueba: {metrics["test_size"]}.

## Metricas obtenidas

- Accuracy: {metrics["accuracy"]}.
- F1 ponderado: {metrics["f1"]}.
- Precision ponderada: {metrics["weighted_precision"]}.
- Recall ponderado: {metrics["weighted_recall"]}.

## Limitaciones

- El dataset sin duplicados tiene solo {metrics["filas_usadas"]} filas.
- La evaluacion es inicial y no debe interpretarse como resultado final.
- No se realizo tuning de hiperparametros.
- No se construyo pipeline final de produccion.
- No se comparo contra el dataset con duplicados.
- En Windows, las predicciones se escriben desde Python despues de seleccionarlas con Spark para evitar la dependencia local de Hadoop `winutils.exe`.

## Confirmacion de alcance

- No se uso MongoDB.
- No se creo API.
- No se uso Docker.
- No se creo Jenkinsfile.
- No se creo dashboard.
- No se realizo despliegue.
"""
    report_path.write_text(report, encoding="utf-8")


def validate_output_files(paths: list[Path]) -> None:
    """Validate that all expected output files exist."""
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"No se generaron las salidas esperadas: {missing}")


def train_initial_model(
    input_path: Path,
    metrics_path: Path,
    predictions_path: Path,
    report_path: Path,
) -> dict[str, object]:
    """Train the initial PySpark model and write required outputs."""
    validate_input_path(input_path)
    python_environment = configure_pyspark_python()
    validate_execution_environment()
    components = import_pyspark_components()
    spark = create_spark_session(components)

    try:
        df = (
            spark.read.option("header", True)
            .option("inferSchema", True)
            .csv(str(input_path))
        )
        validate_columns(df)
        validate_no_required_nulls(df, components)

        total_rows = df.count()
        train_df, test_df = build_stratified_split(df, components)
        train_size = train_df.count()
        test_size = test_df.count()

        pipeline = build_pipeline(components)
        pipeline_model = pipeline.fit(train_df)
        predictions = pipeline_model.transform(test_df)
        predictions, label_order = add_predicted_label(
            predictions, pipeline_model, components
        )

        evaluator_cls = components["MulticlassClassificationEvaluator"]
        accuracy = evaluator_cls(
            labelCol="label", predictionCol="prediction", metricName="accuracy"
        ).evaluate(predictions)
        f1 = evaluator_cls(
            labelCol="label", predictionCol="prediction", metricName="f1"
        ).evaluate(predictions)
        weighted_precision = evaluator_cls(
            labelCol="label",
            predictionCol="prediction",
            metricName="weightedPrecision",
        ).evaluate(predictions)
        weighted_recall = evaluator_cls(
            labelCol="label",
            predictionCol="prediction",
            metricName="weightedRecall",
        ).evaluate(predictions)

        metrics = {
            "accuracy": round(float(accuracy), 6),
            "f1": round(float(f1), 6),
            "weighted_precision": round(float(weighted_precision), 6),
            "weighted_recall": round(float(weighted_recall), 6),
            "filas_usadas": int(total_rows),
            "train_size": int(train_size),
            "test_size": int(test_size),
            "etiqueta_usada": LABEL_COLUMN,
            "columna_texto": TEXT_COLUMN,
            "dataset_utilizado": str(input_path),
            "python_executable": sys.executable,
            "pyspark_python": python_environment["PYSPARK_PYTHON"],
            "pyspark_driver_python": python_environment["PYSPARK_DRIVER_PYTHON"],
            "label_order": label_order,
            "pipeline": [
                "StringIndexer",
                "Tokenizer",
                "StopWordsRemover",
                "HashingTF",
                "IDF",
                "NaiveBayes",
            ],
            "limitacion": (
                "Dataset sin duplicados pequeno; las metricas son solo una "
                "referencia academica inicial."
            ),
        }

        prediction_sample = predictions.select(
            "id",
            "texto",
            "texto_preprocesado",
            "sentimiento",
            "prediction",
            "predicted_label",
        )

        write_metrics(metrics_path, metrics)
        write_predictions_csv_without_hadoop(prediction_sample, predictions_path)
        write_report(report_path, metrics)
        validate_output_files([metrics_path, predictions_path, report_path])

        return metrics
    finally:
        spark.stop()


def main() -> int:
    """Run the initial PySpark modeling phase."""
    project_root = get_project_root()
    input_path = project_root / INPUT_RELATIVE_PATH
    metrics_path = project_root / METRICS_RELATIVE_PATH
    predictions_path = project_root / PREDICTIONS_RELATIVE_PATH
    report_path = project_root / REPORT_RELATIVE_PATH

    try:
        metrics = train_initial_model(
            input_path=input_path,
            metrics_path=metrics_path,
            predictions_path=predictions_path,
            report_path=report_path,
        )
    except EnvironmentNotReadyError as exc:
        print("Fase 5 no ejecutada: entorno PySpark no disponible.", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError) as exc:
        print("Fase 5 no ejecutada: validacion fallida.", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1

    print("Modelado inicial con PySpark completado.")
    print(f"Dataset utilizado: {input_path}")
    print(f"Filas usadas: {metrics['filas_usadas']}")
    print(f"Train: {metrics['train_size']}")
    print(f"Test: {metrics['test_size']}")
    print(f"Accuracy: {metrics['accuracy']}")
    print(f"Metricas: {metrics_path}")
    print(f"Predicciones: {predictions_path}")
    print(f"Reporte: {report_path}")
    print("Nota: no se uso MongoDB, API, Docker, Jenkins ni dashboard.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
