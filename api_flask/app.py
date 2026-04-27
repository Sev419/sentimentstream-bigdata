"""Flask API for SentimentStream JSON access."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

from flask import Flask, jsonify, request

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_flask.config import API_HOST, API_PORT, MONGO_ENABLED
from api_flask.predictor import predict_sentiment_for_api
from database.mongo_repository import insert_predictions, latest_prediction, list_predictions, sentiment_stats


app = Flask(__name__)


def local_error_response(exc: Exception, status_code: int = 503):
    """Return a clear JSON error when MongoDB is not reachable."""
    return (
        jsonify(
            {
                "status": "error",
                "message": "MongoDB no disponible o no configurado.",
                "detail": str(exc),
            }
        ),
        status_code,
    )


@app.get("/health")
def health():
    """Health endpoint for Docker/Jenkins checks."""
    return jsonify({"status": "ok", "service": "sentimentstream-api"})


@app.get("/sentiments")
def get_sentiments():
    """Return stored sentiment predictions."""
    limit = int(request.args.get("limit", "50"))
    try:
        return jsonify({"items": list_predictions(limit=limit)})
    except Exception as exc:  # noqa: BLE001 - API boundary.
        return local_error_response(exc)


@app.get("/stats")
def get_stats():
    """Return aggregated prediction stats."""
    try:
        return jsonify(sentiment_stats())
    except Exception as exc:  # noqa: BLE001 - API boundary.
        return local_error_response(exc)


@app.get("/predictions/latest")
def get_latest_prediction():
    """Return the most recent prediction."""
    try:
        item = latest_prediction()
        return jsonify({"item": item})
    except Exception as exc:  # noqa: BLE001 - API boundary.
        return local_error_response(exc)


@app.post("/predict")
def post_predict():
    """Return a transparent demo prediction and optionally persist it."""
    payload = request.get_json(silent=True) or {}
    text = payload.get("texto") or payload.get("text")
    if not text:
        return jsonify({"status": "error", "message": "Campo requerido: texto"}), 400

    prediction = predict_sentiment_for_api(text)
    prediction["created_at"] = datetime.now(timezone.utc).isoformat()

    if MONGO_ENABLED:
        try:
            insert_predictions([prediction])
            prediction["persisted"] = True
        except Exception as exc:  # noqa: BLE001 - API boundary.
            prediction["persisted"] = False
            prediction["persistence_error"] = str(exc)
    else:
        prediction["persisted"] = False

    return jsonify(prediction)


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, debug=False)
