# Guion De Demo

1. Mostrar estructura del repositorio.
2. Verificar entorno PySpark:

   ```powershell
   python spark/src/verificar_entorno_pyspark.py
   ```

3. Generar micro-batches:

   ```powershell
   python spark_processing/streaming/simulate_micro_batches.py
   ```

4. Procesar micro-batches con Spark:

   ```powershell
   python spark_processing/jobs/process_microbatch_sentiments.py
   ```

5. Levantar MongoDB y API con Docker Compose.
6. Consultar endpoints:

   ```text
   GET /health
   GET /sentiments
   GET /stats
   GET /predictions/latest
   POST /predict
   ```

7. Mostrar dashboard Power BI conectado a API o MongoDB.
8. Explicar limitaciones del baseline y próximos pasos.
