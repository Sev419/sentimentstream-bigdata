"""Minimal text preprocessing shared by ingestion, Spark jobs and API."""

from __future__ import annotations

import re

CONTROL_CHARS_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
WHITESPACE_PATTERN = re.compile(r"\s+")


def preprocess_text(value: object) -> str:
    """Apply conservative preprocessing without changing semantic intent."""
    if value is None:
        return ""

    text = str(value)
    text = CONTROL_CHARS_PATTERN.sub(" ", text)
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    text = text.lower()
    text = WHITESPACE_PATTERN.sub(" ", text).strip()
    return text
