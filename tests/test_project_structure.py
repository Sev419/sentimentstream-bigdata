"""Basic repository structure checks."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_architecture_directories_exist():
    """Validate expected end-to-end architecture directories."""
    required = [
        "data",
        "spark_processing",
        "database",
        "api_flask",
        "dashboard",
        "alerts",
        "docker",
        "jenkins",
        "tests",
        "demo",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    assert not missing, f"Missing directories: {missing}"


def test_required_entrypoints_exist():
    """Validate key runnable files."""
    required = [
        "spark_processing/streaming/simulate_micro_batches.py",
        "spark_processing/jobs/process_microbatch_sentiments.py",
        "spark_processing/jobs/smoke_spark_session.py",
        "spark_processing/src/spark_session_factory.py",
        "api_flask/app.py",
        "docker-compose.yml",
        "jenkins/Jenkinsfile",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    assert not missing, f"Missing files: {missing}"
