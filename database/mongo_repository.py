"""MongoDB repository helpers for SentimentStream predictions."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any


def get_collection():
    """Create a MongoDB collection handle from environment variables."""
    try:
        from pymongo import MongoClient
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "pymongo no esta instalado. Instale dependencias o ejecute con "
            "MONGO_ENABLED=false para pruebas sin MongoDB."
        ) from exc

    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    database_name = os.environ.get("MONGO_DB_NAME", "sentimentstream_db")
    collection_name = os.environ.get("MONGO_COLLECTION", "predictions")

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    return client[database_name][collection_name]


def insert_predictions(records: list[dict[str, Any]]) -> int:
    """Insert prediction records and return the inserted count."""
    if not records:
        return 0

    now = datetime.now(timezone.utc)
    documents = []
    for record in records:
        document = dict(record)
        document.setdefault("created_at", now)
        document.setdefault("source", "spark_processing")
        documents.append(document)

    result = get_collection().insert_many(documents)
    return len(result.inserted_ids)


def list_predictions(limit: int = 50) -> list[dict[str, Any]]:
    """Return recent predictions from MongoDB."""
    collection = get_collection()
    cursor = collection.find({}, {"_id": 0}).sort("created_at", -1).limit(limit)
    return list(cursor)


def latest_prediction() -> dict[str, Any] | None:
    """Return the latest prediction if available."""
    collection = get_collection()
    return collection.find_one({}, {"_id": 0}, sort=[("created_at", -1)])


def sentiment_stats() -> dict[str, Any]:
    """Aggregate prediction counts by predicted label."""
    collection = get_collection()
    pipeline = [
        {"$group": {"_id": "$predicted_label", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    by_label = {
        item["_id"] or "unknown": item["count"] for item in collection.aggregate(pipeline)
    }
    total = sum(by_label.values())
    return {"total": total, "by_predicted_label": by_label}
