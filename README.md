# SentimentStream

SentimentStream es un proyecto universitario de Big Data para analisis de sentimientos en datos textuales. El objetivo es demostrar un flujo de extremo a extremo, no solo un notebook o un modelo aislado.

## Arquitectura Objetivo

```text
dataset / simulacion streaming
    -> micro-batches CSV
    -> Spark / PySpark NLP + ML
    -> MongoDB
    -> Flask API
    -> Power BI
    -> alertas opcionales
```

Docker y Jenkins se usan como capas transversales para portabilidad, reproducibilidad y automatizacion.

## Estado Actual

El proyecto conserva dos areas:

- `spark/`: historial academico de fases previas. No se elimina porque contiene exploracion, normalizacion, preprocesamiento, preparacion para modelado, baseline PySpark y metricas reales.
- `spark_processing/`: pipeline operativo final para ingesta simulada y procesamiento de micro-batches.

El flujo minimo que se esta estabilizando es:

```text
data/streaming/input/microbatch_001.csv
    -> spark_processing/jobs/process_microbatch_sentiments.py
    -> data/streaming/processed/
    -> MongoDB
    -> api_flask/app.py
```

## Estructura Principal

```text
sentimentstream/
├── data/
│   ├── raw/
│   ├── processed/
│   └── streaming/
│       ├── input/
│       └── processed/
├── spark/
├── spark_processing/
│   ├── src/
│   ├── streaming/
│   └── jobs/
├── database/
├── api_flask/
├── dashboard/
├── alerts/
├── docker/
├── jenkins/
├── tests/
├── demo/
├── docker-compose.yml
├── Jenkinsfile
├── .env.example
├── requirements.txt
└── README.md
```

## Carpetas De Transicion

- `api/`: estructura heredada de la fase inicial. La API operativa actual esta en `api_flask/`.
- `infra/`: estructura heredada vacia. La infraestructura operativa actual esta en `docker/`, `docker-compose.yml` y `jenkins/`.

## Componentes Operativos

### Simulacion De Micro-Batches

```powershell
python spark_processing\streaming\simulate_micro_batches.py
```

Genera archivos en:

```text
data/streaming/input/
```

### Smoke Test De SparkSession

Antes de ejecutar el pipeline completo, validar solo el arranque de Spark:

```powershell
$env:SPARK_MASTER="local[1]"
$env:SPARK_SHUFFLE_PARTITIONS="1"
$env:SPARK_DEFAULT_PARALLELISM="1"
$env:SPARK_UI_ENABLED="false"
$env:SPARK_DRIVER_BIND_ADDRESS="127.0.0.1"
$env:SPARK_DRIVER_HOST="127.0.0.1"
python spark_processing\jobs\smoke_spark_session.py --timeout 60
```

El log queda en:

```text
data/streaming/processed/smoke_spark_session.log
```

Si esta prueba se cuelga o expira en Windows, no se debe ejecutar el pipeline completo localmente. La recomendacion es usar Docker o mover el proyecto a una ruta sin espacios.

### Procesamiento PySpark De Micro-Batches

Modos disponibles:

```powershell
python spark_processing\jobs\process_microbatch_sentiments.py --smoke --input data\streaming\input\microbatch_001.csv
python spark_processing\jobs\process_microbatch_sentiments.py --train-only
python spark_processing\jobs\process_microbatch_sentiments.py --process-only --input data\streaming\input\microbatch_001.csv
```

Salidas esperadas:

```text
data/streaming/processed/process_microbatch.log
data/streaming/processed/predictions_microbatch_001.csv
```

### MongoDB

Activar persistencia:

```powershell
$env:MONGO_ENABLED="true"
$env:MONGO_URI="mongodb://localhost:27017"
```

Levantar MongoDB con Docker:

```powershell
docker compose up -d mongo
```

### Flask API

```powershell
$env:MONGO_ENABLED="true"
$env:MONGO_URI="mongodb://localhost:27017"
python api_flask\app.py
```

Endpoints:

```text
GET  /health
GET  /sentiments
GET  /stats
GET  /predictions/latest
POST /predict
```

Nota: `POST /predict` usa un predictor liviano de demostracion para respuesta inmediata. El clasificador principal del proyecto sigue siendo PySpark por micro-batches.

## Ejecucion Local Minima

1. Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

2. Verificar entorno PySpark:

```powershell
python spark\src\verificar_entorno_pyspark.py
```

3. Ejecutar smoke test:

```powershell
python spark_processing\jobs\smoke_spark_session.py --timeout 60
```

4. Generar micro-batches:

```powershell
python spark_processing\streaming\simulate_micro_batches.py
```

5. Procesar un micro-batch sin MongoDB:

```powershell
$env:MONGO_ENABLED="false"
python spark_processing\jobs\process_microbatch_sentiments.py --process-only --input data\streaming\input\microbatch_001.csv
```

6. Procesar un micro-batch con MongoDB:

```powershell
docker compose up -d mongo
$env:MONGO_ENABLED="true"
$env:MONGO_URI="mongodb://localhost:27017"
python spark_processing\jobs\process_microbatch_sentiments.py --process-only --input data\streaming\input\microbatch_001.csv
```

7. Probar API Flask:

```powershell
$env:MONGO_ENABLED="true"
$env:MONGO_URI="mongodb://localhost:27017"
python api_flask\app.py
```

En otra terminal:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/sentiments
Invoke-RestMethod http://127.0.0.1:8000/stats
Invoke-RestMethod http://127.0.0.1:8000/predictions/latest
```

## Ejecucion Con Docker

Docker es la ruta recomendada si Spark se queda colgado en Windows local.

Validar Spark en Docker:

```powershell
docker compose --profile processing run --rm spark-job python spark_processing/jobs/smoke_spark_session.py --timeout 120
```

Ejecutar pipeline Spark en Docker:

```powershell
docker compose --profile processing up --build spark-job
```

Levantar MongoDB y API:

```powershell
docker compose up --build mongo api
```

El servicio `spark-job` monta `./data:/app/data`, por lo que las salidas quedan visibles en:

```text
data/streaming/processed/
```

## Resultados Del Baseline Historico

Archivo:

```text
spark/outputs/metricas_modelo_inicial.json
```

Metricas reales:

| Metrica | Valor |
|---|---:|
| Accuracy | 0.111111 |
| F1 ponderado | 0.066667 |
| Precision ponderada | 0.047619 |
| Recall ponderado | 0.111111 |
| Filas usadas | 30 |
| Train | 21 |
| Test | 9 |

Estas metricas son bajas porque el dataset sin duplicados conserva solo 30 textos unicos. Es un baseline academico, no un modelo final.

## Plan De Trabajo

- [x] Fase 1: estructura base.
- [x] Fase 2: exploracion del dataset.
- [x] Fase 2.5: normalizacion estructural.
- [x] Fase 3: preprocesamiento inicial.
- [x] Fase 4: preparacion para modelado.
- [x] Fase 5: baseline PySpark.
- [x] Reestructuracion end-to-end por capas.
- [x] Simulacion de micro-batches.
- [x] Capa MongoDB preparada.
- [x] API Flask minima.
- [x] Docker Compose inicial.
- [x] Jenkinsfile inicial.
- [x] Factory central de SparkSession.
- [x] Smoke test aislado de SparkSession.
- [ ] Validar procesamiento Spark hacia `data/streaming/processed/`.
- [ ] Validar insercion real en MongoDB.
- [ ] Validar API Flask leyendo MongoDB real.
- [ ] Conectar Power BI.
- [ ] Crear dashboard final.
- [ ] Grabar video demo.

## Riesgos

- La ruta local contiene espacios: `C:\Users\User\Desktop\Big DAta\sentimentstream`. En Windows esto puede afectar Spark/JVM. Si el smoke test falla, usar Docker o mover el proyecto a una ruta sin espacios.
- PySpark en Windows puede dejar procesos colgados si `SparkSession` no arranca.
- MongoDB debe estar activo antes de usar `MONGO_ENABLED=true`.
- Power BI queda pendiente hasta estabilizar Spark -> Mongo -> Flask.
