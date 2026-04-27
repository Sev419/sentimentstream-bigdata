# SentimentStream - Pipeline Big Data Para Analisis De Sentimientos

## 1. Descripcion Del Proyecto

SentimentStream es un proyecto academico y de portafolio que implementa un flujo end-to-end para analisis de sentimientos sobre datos textuales. El sistema procesa micro-batches con PySpark, guarda predicciones reales en MongoDB, expone los resultados mediante una API Flask, visualiza indicadores en Power BI y documenta una validacion automatizada basica con Jenkins.

El proyecto no se limita a un notebook o a un modelo aislado. Su foco principal es demostrar una arquitectura integrada de datos, backend, visualizacion y DevOps.

## 2. Arquitectura Final

La arquitectura final validada es:

```text
Spark -> MongoDB -> Flask API -> Power BI -> Jenkins
```

Flujo completo:

```text
CSV dataset
  -> micro-batches en data/streaming/input/
  -> procesamiento PySpark en Docker
  -> persistencia en MongoDB
  -> exposicion de datos con Flask API
  -> dashboard Power BI
  -> validacion basica con Jenkins
```

## 3. Explicacion Del Flujo

1. Los datos de entrada se almacenan como archivos CSV y se simulan como micro-batches.
2. PySpark procesa un micro-batch, aplica preparacion textual y genera predicciones de sentimiento.
3. Las predicciones se insertan en MongoDB en la base `sentimentstream_db`, coleccion `predictions`.
4. Flask consulta MongoDB y publica endpoints REST para consultar registros, estadisticas y predicciones recientes.
5. Power BI consume la API Flask y construye visualizaciones sobre datos reales.
6. Jenkins ejecuta un pipeline basico para validar Docker, MongoDB, Spark, Mongo y API.

## 4. Tecnologias Utilizadas

- PySpark: procesamiento de micro-batches y baseline de clasificacion.
- MongoDB: persistencia de predicciones.
- Flask: API REST para exponer datos procesados.
- Power BI: dashboard final de visualizacion.
- Docker: ejecucion portable de MongoDB, Spark job y API Flask.
- Jenkins: pipeline demostrativo de validacion automatizada.
- Python: scripts de procesamiento, API y pruebas.

## 5. Estructura Del Proyecto

```text
sentimentstream/
|-- api_flask/              # API Flask operativa
|-- dashboard/
|   |-- exports/            # Capturas del dashboard Power BI
|   |-- mock_responses/     # JSON de referencia para pruebas/documentacion
|   `-- powerbi/            # Archivo .pbix del dashboard
|-- data/
|   |-- raw/                # Dataset base
|   |-- processed/          # Datasets preparados
|   `-- streaming/input/    # Micro-batches de entrada
|-- database/               # Integracion con MongoDB
|-- docker/                 # Dockerfiles
|-- docs/
|   |-- arquitectura/       # Documentacion de arquitectura
|   |-- evidencias/         # Evidencias del proyecto
|   `-- pruebas/            # Reportes tecnicos por fase
|-- infra/jenkins/          # Jenkinsfile del pipeline demostrativo
|-- spark/                  # Fases academicas y baseline PySpark
|-- spark_processing/       # Pipeline operativo de micro-batches
|-- tests/                  # Pruebas automatizadas
|-- docker-compose.yml
|-- Jenkinsfile
|-- requirements.txt
`-- README.md
```

## 6. Como Ejecutar El Proyecto

### 6.1 Requisitos

- Docker Desktop o Docker Engine.
- Docker Compose.
- Python 3.12 o compatible, si se ejecutan scripts fuera de Docker.
- Power BI Desktop para abrir el dashboard `.pbix`.
- Jenkins para ejecutar el pipeline demostrativo.

### 6.2 Ejecucion Con Docker

Validar Docker:

```bash
docker version
```

Levantar MongoDB:

```bash
docker compose up -d mongo
```

Ejecutar el procesamiento Spark del micro-batch principal:

```bash
docker compose --profile processing run --rm spark-job python spark_processing/jobs/process_microbatch_sentiments.py --process-only --input data/streaming/input/microbatch_001.csv
```

Levantar la API Flask:

```bash
docker compose up -d api
```

Verificar contenedores:

```bash
docker compose ps
```

### 6.3 Endpoints De La API

URL base:

```text
http://127.0.0.1:8000
```

Endpoints:

```text
GET  /health
GET  /sentiments
GET  /stats
GET  /predictions/latest
POST /predict
```

Consultas de validacion:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/stats
curl http://127.0.0.1:8000/sentiments
curl http://127.0.0.1:8000/predictions/latest
```

`POST /predict` se conserva como endpoint de demostracion para respuesta inmediata. El flujo principal del proyecto es el procesamiento PySpark por micro-batches con persistencia en MongoDB.

## 7. Resultados

El proyecto valida el flujo completo desde datos hasta visualizacion:

- Dataset CSV preparado.
- Micro-batches disponibles en `data/streaming/input/`.
- Spark ejecutado en Docker.
- Inserciones reales en MongoDB.
- API Flask consultando datos reales.
- Dashboard Power BI construido sobre endpoints Flask.
- Pipeline Jenkins basico documentado y preparado para validacion.

Resultado registrado por `/stats`:

```json
{
  "by_predicted_label": {
    "negativo": 8,
    "neutral": 8,
    "positivo": 9
  },
  "total": 25
}
```

### 7.1 Metricas Baseline

El proyecto conserva un baseline academico de modelado PySpark. Las metricas documentadas son:

| Metrica | Valor |
| --- | ---: |
| Accuracy | 0.111111 |
| F1 ponderado | 0.066667 |
| Precision ponderada | 0.047619 |
| Recall ponderado | 0.111111 |
| Filas usadas | 30 |
| Train | 21 |
| Test | 9 |

Estas metricas corresponden a un dataset pequeno y sirven como referencia academica, no como resultado productivo de NLP avanzado.

## 8. Dashboard Power BI

El dashboard final fue construido en Power BI y consume datos desde la API Flask.

Archivo Power BI:

```text
dashboard/powerbi/sentimientos.pbix
```

Capturas disponibles:

```text
dashboard/exports/dashboard_overview.png
dashboard/exports/card_total.png
dashboard/exports/chart_distribution.png
dashboard/exports/table_predictions.png
```

Visualizaciones incluidas:

- Tarjeta `Total de Predicciones`: muestra `25`.
- Grafico `Distribucion de Sentimientos`: muestra la distribucion `9/8/8`.
- Tabla `Predicciones Recientes`: muestra registros consumidos desde `/sentiments`.

La consulta `/stats` fue preparada en Power Query en formato largo:

```text
predicted_label | cantidad | total
```

## 9. Jenkins

El pipeline Jenkins se encuentra en:

```text
infra/jenkins/Jenkinsfile
```

El pipeline es basico y demostrativo. Valida:

1. `docker version`.
2. Inicio de MongoDB con `docker compose up -d mongo`.
3. Ejecucion del Spark job con Docker Compose.
4. Conteo de documentos en `sentimentstream_db.predictions`.
5. Respuesta del endpoint `http://127.0.0.1:8000/stats`.

Este Jenkinsfile no representa una configuracion de produccion. No despliega en nube, no usa Kubernetes y depende de que el agente Jenkins tenga acceso al Docker host.

## 10. Documentacion Tecnica

La documentacion completa se encuentra en:

```text
docs/pruebas/
```

Reportes principales:

- `reporte_integracion_spark_docker_mongo.md`
- `reporte_validacion_api_flask.md`
- `reporte_powerbi_api.md`
- `guia_correccion_powerquery_stats.md`
- `reporte_dashboard_powerbi.md`
- `reporte_jenkins_pipeline.md`
- `reporte_preparacion_github.md`

## 11. Limitaciones Del Proyecto

- El dataset es pequeno y tiene finalidad academica.
- El baseline de clasificacion es simple.
- Las metricas del modelo no buscan representar un sistema productivo avanzado.
- Power BI consume una API local en `127.0.0.1`.
- Jenkins se usa en modo demostrativo.
- La integracion Jenkins-Docker requiere acceso correcto al Docker host.
- No se implementa despliegue en nube.
- No se usa Kubernetes.

## 12. Conclusion

SentimentStream completa un flujo Big Data end-to-end:

```text
datos -> Spark -> MongoDB -> Flask API -> Power BI -> Jenkins
```

El proyecto demuestra procesamiento por micro-batches, persistencia real, exposicion REST, visualizacion de indicadores y automatizacion basica. Su valor academico esta en integrar varias capas de una solucion de datos en una arquitectura reproducible, documentada y presentable como portafolio tecnico.
