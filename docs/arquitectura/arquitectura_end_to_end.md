# Arquitectura End-To-End SentimentStream

## Capas

1. **Ingesta:** `spark_processing/streaming/simulate_micro_batches.py`
2. **Procesamiento distribuido:** `spark_processing/jobs/process_microbatch_sentiments.py`
3. **Persistencia:** `database/mongo_repository.py`
4. **Exposición:** `api_flask/app.py`
5. **Visualización:** `dashboard/powerbi/`
6. **Despliegue:** `docker-compose.yml`, `docker/`, `jenkins/Jenkinsfile`

## Flujo

```text
data/processed
  -> data/streaming/input
  -> spark_processing/jobs
  -> data/streaming/processed
  -> MongoDB
  -> Flask API
  -> Power BI
```

## Decisiones

- Se conserva `spark/` como historial de fases y baseline.
- Se crea `spark_processing/` como capa operativa para la arquitectura final.
- Se usa micro-batch CSV para simular streaming sin introducir Kafka todavía.
- MongoDB es opcional por variable `MONGO_ENABLED` para permitir pruebas locales sin base de datos.
- Docker Compose levanta MongoDB y API; el procesamiento Spark se ejecuta como perfil separado.
