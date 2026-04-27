"""Verificador local de prerequisitos para ejecutar PySpark.

Este script no instala paquetes, no modifica archivos y no entrena modelos.
Su unica responsabilidad es diagnosticar si el entorno puede ejecutar la
Fase 5 de SentimentStream.
"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
import shutil
import subprocess
import sys


def check_pyspark() -> dict[str, object]:
    """Check whether Python can import pyspark."""
    try:
        pyspark = importlib.import_module("pyspark")
    except ModuleNotFoundError:
        return {
            "ok": False,
            "name": "pyspark",
            "detail": "Modulo pyspark no disponible para el Python actual.",
        }

    version = getattr(pyspark, "__version__", "version no detectada")
    return {
        "ok": True,
        "name": "pyspark",
        "detail": f"Modulo pyspark importable. Version: {version}.",
    }


def check_command(name: str, version_args: list[str]) -> dict[str, object]:
    """Check whether a command is available and can print version information."""
    executable = shutil.which(name)
    if executable is None:
        return {
            "ok": False,
            "name": name,
            "detail": f"Comando '{name}' no encontrado en PATH.",
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
            "name": name,
            "detail": f"Comando encontrado en {executable}, pero fallo: {exc}",
        }

    output = (result.stdout or result.stderr or "").strip().splitlines()
    first_line = output[0] if output else "Comando encontrado."

    return {
        "ok": result.returncode == 0,
        "name": name,
        "detail": f"{executable} - {first_line}",
    }


def print_result(result: dict[str, object]) -> None:
    """Print a single diagnostic result."""
    status = "OK" if result["ok"] else "NO OK"
    print(f"[{status}] {result['name']}: {result['detail']}")


def main() -> int:
    """Run environment diagnostics for PySpark execution."""
    project_root = Path(__file__).resolve().parents[2]

    print("Verificacion de entorno PySpark - SentimentStream")
    print(f"Proyecto: {project_root}")
    print(f"Python: {sys.executable}")
    print(f"PYSPARK_PYTHON: {os.environ.get('PYSPARK_PYTHON', '<no definida>')}")
    print(
        "PYSPARK_DRIVER_PYTHON: "
        f"{os.environ.get('PYSPARK_DRIVER_PYTHON', '<no definida>')}"
    )
    print(
        "Python que fijara el script principal para driver/worker: "
        f"{sys.executable}"
    )
    print()

    diagnostics = [
        check_pyspark(),
        check_command("java", ["-version"]),
        check_command("spark-submit", ["--version"]),
    ]

    for result in diagnostics:
        print_result(result)

    required_ready = diagnostics[0]["ok"] and diagnostics[1]["ok"]
    spark_submit_ready = diagnostics[2]["ok"]

    print()
    if required_ready:
        print("Entorno minimo listo para intentar la Fase 5 con PySpark local.")
        if not spark_submit_ready:
            print(
                "Nota: spark-submit no esta disponible. El script puede ejecutarse "
                "con python si pyspark esta correctamente instalado."
            )
        return 0

    print("Entorno NO listo para ejecutar la Fase 5.")
    print("Faltan prerequisitos minimos: Python con pyspark importable y Java disponible.")
    print("No se instalo nada y no se modifico ningun archivo.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
