"""Tests for shared text preprocessing."""

from spark_processing.src.text_preprocessing import preprocess_text


def test_preprocess_text_is_conservative():
    """Lowercase and normalize spacing without removing words."""
    assert preprocess_text("  Hello\tWorld\n") == "hello world"
