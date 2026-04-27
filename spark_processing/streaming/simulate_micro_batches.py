"""Simulate streaming input by writing small CSV micro-batches.

This script does not run Spark. It prepares deterministic micro-batches that
can be consumed by the Spark processing job.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

import pandas as pd

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from spark_processing.src.project_paths import env_int, project_root
from spark_processing.src.text_preprocessing import preprocess_text


DEFAULT_SOURCE = Path("data") / "processed" / "dataset_modelado_con_duplicados.csv"
OUTPUT_DIR = Path("data") / "streaming" / "input"


def load_source(source_path: Path) -> pd.DataFrame:
    """Load and normalize source columns for simulated events."""
    if not source_path.exists():
        raise FileNotFoundError(f"No existe el archivo fuente: {source_path}")

    df = pd.read_csv(source_path)
    if "texto" not in df.columns:
        raise ValueError(f"El archivo fuente no contiene columna texto: {df.columns}")

    if "sentimiento" not in df.columns and "etiqueta" in df.columns:
        df = df.rename(columns={"etiqueta": "sentimiento"})

    if "id" not in df.columns:
        df.insert(0, "id", range(1, len(df) + 1))

    if "texto_preprocesado" not in df.columns:
        df["texto_preprocesado"] = df["texto"].apply(preprocess_text)

    selected_columns = ["id", "texto", "texto_preprocesado"]
    if "sentimiento" in df.columns:
        selected_columns.append("sentimiento")

    return df[selected_columns].copy()


def write_batches(df: pd.DataFrame, output_dir: Path, batch_size: int, max_batches: int) -> list[Path]:
    """Write deterministic micro-batch CSV files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written_files: list[Path] = []

    if batch_size <= 0:
        raise ValueError("batch_size debe ser mayor que cero.")

    batch_number = 0
    for start in range(0, len(df), batch_size):
        if batch_number >= max_batches:
            break

        batch_number += 1
        batch = df.iloc[start : start + batch_size].copy()
        batch["microbatch_id"] = batch_number
        batch["event_time"] = datetime.now(timezone.utc).isoformat()

        output_path = output_dir / f"microbatch_{batch_number:03d}.csv"
        batch.to_csv(output_path, index=False, encoding="utf-8")
        written_files.append(output_path)

    return written_files


def main() -> None:
    """Generate simulated streaming micro-batches."""
    root = project_root()
    source_path = root / Path(
        sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SOURCE
    )
    output_dir = root / OUTPUT_DIR
    batch_size = env_int("STREAM_BATCH_SIZE", 25)
    max_batches = env_int("STREAM_MAX_BATCHES", 3)

    df = load_source(source_path)
    files = write_batches(df, output_dir, batch_size=batch_size, max_batches=max_batches)

    print("Simulacion de micro-batches completada.")
    print(f"Fuente: {source_path}")
    print(f"Directorio salida: {output_dir}")
    print(f"Archivos generados: {len(files)}")
    for file_path in files:
        print(f"- {file_path}")


if __name__ == "__main__":
    main()
