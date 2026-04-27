"""Configuration helpers for the Flask API."""

from __future__ import annotations

import os


def env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean environment variable."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", "8000"))
MONGO_ENABLED = env_bool("MONGO_ENABLED", True)
