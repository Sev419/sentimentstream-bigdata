# Reporte De Pipeline Jenkins

## Objetivo

Documentar un pipeline Jenkins basico para validar automaticamente el flujo principal de SentimentStream:

```text
Spark -> MongoDB -> Flask API
```

Este reporte no registra una ejecucion real del pipeline. Solo documenta el archivo creado, sus etapas, los comandos definidos y la forma recomendada de ejecutarlo localmente.

## Archivo Del Pipeline

El pipeline se define en:

```text
infra/jenkins/Jenkinsfile
```

El pipeline usa Docker Compose y los servicios ya definidos por el proyecto. No modifica Spark, MongoDB, Flask ni Docker Compose.

## Etapas Del Pipeline

### Stage 1 - Setup

Comando:

```bash
docker version
```

Validacion:

- Confirma que Docker esta disponible en el agente Jenkins.
- Permite detectar errores basicos de instalacion, permisos o conexion con Docker Engine.

### Stage 2 - Levantar Mongo

Comando:

```bash
docker compose up -d mongo
```

Validacion:

- Inicia MongoDB usando el servicio `mongo` existente en `docker-compose.yml`.
- Deja disponible la base de datos requerida por el proceso Spark y la API Flask.

### Stage 3 - Ejecutar Spark Job

Comando:

```bash
docker compose --profile processing run --rm spark-job python spark_processing/jobs/process_microbatch_sentiments.py --process-only --input data/streaming/input/microbatch_001.csv
```

Validacion:

- Ejecuta el procesamiento del microbatch `microbatch_001.csv`.
- Usa el servicio `spark-job` ya definido en Docker Compose.
- Valida que Spark pueda procesar datos y escribir predicciones en MongoDB.

### Stage 4 - Validar Mongo

Comando:

```bash
docker compose exec -T mongo mongosh --quiet --eval "const count = db.getSiblingDB('sentimentstream_db').predictions.countDocuments({}); print(count); if (count <= 0) { quit(1); }"
```

Consulta validada:

```javascript
db.getSiblingDB('sentimentstream_db').predictions.countDocuments({})
```

Validacion:

- Cuenta documentos en `sentimentstream_db.predictions`.
- Falla el pipeline si el conteo es `0` o menor.
- Confirma que el job Spark dejo resultados persistidos en MongoDB.

### Stage 5 - Validar API

Comandos:

```bash
docker compose up -d api
curl --fail --silent --show-error http://127.0.0.1:8000/stats
```

Validacion:

- Levanta la API Flask usando el servicio `api` existente.
- Consulta el endpoint `/stats`.
- Falla el pipeline si la API no responde correctamente.
- Confirma que Flask puede exponer las estadisticas generadas a partir de MongoDB.

## Como Ejecutar Jenkins Localmente

Requisitos:

- Docker Desktop instalado y ejecutandose.
- Jenkins con acceso al comando `docker`.
- Plugin Pipeline instalado en Jenkins.
- El workspace de Jenkins debe apuntar al repositorio SentimentStream.

Pasos recomendados:

1. Abrir Jenkins local.
2. Crear un nuevo job tipo `Pipeline`.
3. Configurar el origen del pipeline como `Pipeline script from SCM` si el repositorio esta versionado.
4. Indicar la ruta del Jenkinsfile:

```text
infra/jenkins/Jenkinsfile
```

5. Ejecutar `Build Now`.
6. Revisar la consola del build para confirmar cada etapa:
   - `Setup`
   - `Levantar Mongo`
   - `Ejecutar Spark job`
   - `Validar Mongo`
   - `Validar API`

## Resultado Esperado

El pipeline debe completarse exitosamente cuando:

- Docker responde.
- MongoDB inicia correctamente.
- El job Spark procesa el microbatch indicado.
- MongoDB contiene al menos un documento en `sentimentstream_db.predictions`.
- La API Flask responde a `http://127.0.0.1:8000/stats`.

## Alcance Y Restricciones

Este pipeline es una validacion local y basica del flujo.

No incluye:

- Despliegue en nube.
- Kubernetes.
- Publicacion de artefactos.
- Construccion de dashboard Power BI.
- Cambios en Spark.
- Cambios en MongoDB.
- Cambios en Flask.
- Cambios en Docker Compose.

## Pendientes

- Ejecutar el pipeline desde Jenkins local y guardar evidencia de la consola.
- Documentar el resultado real de la primera ejecucion.
- Definir si el Jenkinsfile raiz debe seguir delegando o apuntar directamente a `infra/jenkins/Jenkinsfile`.
