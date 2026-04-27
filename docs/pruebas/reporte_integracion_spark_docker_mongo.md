# Reporte de Integracion Spark Docker Mongo

## Objetivo

Validar el flujo:

```text
microbatch CSV -> Spark dentro de Docker -> MongoDB en Docker -> Flask API
```

## Bloqueo Original

La ejecucion local de Spark en Windows es inestable. El proceso quedaba detenido en:

```text
SparkSession.builder.getOrCreate()
```

Por esa razon se decidio migrar la ejecucion del job Spark a Docker.

## Estado Inicial Confirmado

- Docker Desktop responde correctamente a `docker version`.
- MongoDB corre en Docker.
- Servicio Mongo real: `mongo`
- Contenedor Mongo real: `sentimentstream-mongo`
- Puerto expuesto: `27017`
- Estado verificado: `Up (healthy)`

## Archivos Revisados

- `docker-compose.yml`
- `docker/spark/Dockerfile`
- `requirements.txt`
- `spark_processing/jobs/process_microbatch_sentiments.py`
- `spark_processing/src/spark_session_factory.py`
- `database/mongo_repository.py`
- `api_flask/app.py`

## Cambios Realizados

1. Se ajusto `docker-compose.yml`:
   - `mongo` con `healthcheck`
   - `api` dependiente de `mongo` saludable
   - `spark-job` dependiente de `mongo` saludable
   - `spark-job` con volumen `./:/app`
   - `spark-job` con `working_dir=/app`
   - variables:
     - `MONGO_URI=mongodb://mongo:27017`
     - `MONGO_ENABLED=true`
     - `MONGO_DB_NAME=sentimentstream_db`
     - `MONGO_COLLECTION=predictions`

2. Se ajusto `docker/spark/Dockerfile`:
   - base `python:3.11-slim`
   - Java cambiada a `openjdk-21-jre-headless`

## Comandos Ejecutados

### Validacion de Docker

```powershell
docker version
docker ps
docker compose config
docker compose --profile processing config
```

### MongoDB

```powershell
docker compose up -d mongo
docker exec sentimentstream-mongo mongosh --quiet --eval "db.adminCommand('ping').ok"
docker exec sentimentstream-mongo mongosh --quiet --eval "db.getSiblingDB('sentimentstream_db').predictions.countDocuments({})"
```

### Spark en Docker

```powershell
docker compose --profile processing build spark-job
```

## Estado de Mongo

- `docker exec ... ping` devolvio: `1`
- Conteo real previo en `sentimentstream_db.predictions`: `0`

## Resultado del Job Spark en Docker

El job Spark en Docker se ejecuto correctamente.

Salida resumida:

- `training_rows`: 30
- `rows` procesadas en `microbatch_001.csv`: 25
- `records_written`: 25
- `mongo_inserted`: 25

Se genero tambien:

```text
/app/data/streaming/processed/predictions_microbatch_001.csv
```

## Error Real Encontrado

Primer fallo:

```text
failed to solve: write /var/lib/desktop-containerd/daemon/io.containerd.metadata.v1.bolt/meta.db: input/output error
```

Diagnostico adicional del daemon:

```text
failed to retrieve image list: rpc error: code = Unknown desc = blob sha256:... input/output error
```

y

```text
Error response from daemon: rpc error: code = Unknown desc = blob sha256:... input/output error
```

Esto indica un problema del content store / metadata store de Docker Desktop (`containerd`), no del codigo del proyecto.

## Inserciones Reales En Mongo

- Antes del job: `0`
- Despues del job: `25`

## Flask API

La API sigue preparada para usar:

```text
MONGO_URI=mongodb://mongo:27017
```

dentro de Docker.

La ejecucion de `docker compose up -d api` no quedo levantada como contenedor persistente en esta sesion, asi que los endpoints no se validaron en vivo en esta corrida.

## Bloqueo Pendiente

El flujo Spark -> Mongo quedo validado.

Queda pendiente dejar la API Flask corriendo de forma persistente para probar:

- `/sentiments`
- `/stats`
- `/predictions/latest`

## Proximos Pasos Recomendados

1. Levantar Flask API en una sesion separada.
2. Probar los endpoints contra Mongo real.
3. Dejar listo el reporte final de la integracion.

## Confirmacion de Alcance

- No se uso Spark local para esta integracion.
- No se modificaron datasets.
- No se avanzo a Power BI.
- No se avanzo a Jenkins.
