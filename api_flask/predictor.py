"""Small API-side fallback predictor.

The main project classifier is the PySpark batch job. This predictor only keeps
POST /predict useful for demos when a Spark job is not running in-process.
"""

from __future__ import annotations

from spark_processing.src.text_preprocessing import preprocess_text


NEGATIVE_TERMS = {
    "bad",
    "crash",
    "crashing",
    "poor",
    "slow",
    "terrible",
    "unresponsive",
    "hate",
    "not recommend",
}
POSITIVE_TERMS = {
    "amazing",
    "excellent",
    "great",
    "helped",
    "love",
    "recommend",
    "smooth",
    "useful",
}


def predict_sentiment_for_api(text: str) -> dict[str, str]:
    """Return a transparent demo prediction for the API endpoint."""
    processed = preprocess_text(text)

    if any(term in processed for term in NEGATIVE_TERMS):
        label = "negativo"
    elif any(term in processed for term in POSITIVE_TERMS):
        label = "positivo"
    else:
        label = "neutral"

    return {
        "texto": text,
        "texto_preprocesado": processed,
        "predicted_label": label,
        "model_source": "api_demo_rules",
    }
