db = db.getSiblingDB("sentimentstream_db");

db.createCollection("predictions");
db.predictions.createIndex({ created_at: -1 });
db.predictions.createIndex({ predicted_label: 1 });
