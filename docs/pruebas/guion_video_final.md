# Guion Video Final SentimentStream

## Objetivo Del Video

Mostrar en 3 a 5 minutos que SentimentStream implementa un pipeline Big Data integrado para analisis de sentimientos:

```text
Spark -> MongoDB -> Flask API -> Power BI -> Jenkins
```

El video debe demostrar el flujo end-to-end sin entrar en detalles excesivos de codigo.

## Ventanas Que Deben Estar Abiertas Antes De Grabar

- Repositorio GitHub de SentimentStream.
- Proyecto abierto en VS Code.
- Terminal en la raiz del proyecto.
- Navegador con la API Flask lista.
- Power BI Desktop con `dashboard/powerbi/sentimientos.pbix`.
- Jenkins abierto o, si no se ejecuta en vivo, `infra/jenkins/Jenkinsfile`.
- Carpeta `dashboard/exports/` como respaldo visual.

## 0:00 - 0:30 | Introduccion

Mostrar README en GitHub.

Texto sugerido:

```text
SentimentStream es un proyecto Big Data de analisis de sentimientos. Integra procesamiento con PySpark, persistencia en MongoDB, exposicion de resultados con Flask API, visualizacion en Power BI y validacion automatizada con Jenkins.
```

Idea clave:

- No es solo un modelo.
- Es una arquitectura completa de datos.

## 0:30 - 1:00 | Arquitectura

Mostrar la seccion de arquitectura del README.

Explicar:

```text
CSV -> micro-batches -> Spark -> MongoDB -> Flask API -> Power BI -> Jenkins
```

Puntos a mencionar:

- Spark procesa micro-batches.
- MongoDB guarda predicciones.
- Flask expone endpoints.
- Power BI consume la API.
- Jenkins valida el flujo.

## 1:00 - 1:40 | Spark Y Docker

Mostrar `docker-compose.yml` y `spark_processing/jobs/process_microbatch_sentiments.py`.

Explicar:

```text
El procesamiento se ejecuta en Docker mediante el servicio spark-job. El job toma un micro-batch CSV, aplica limpieza de texto, tokenizacion, TF-IDF y clasificacion con Naive Bayes.
```

Comando que puede mostrarse:

```bash
docker compose --profile processing run --rm spark-job python spark_processing/jobs/process_microbatch_sentiments.py --process-only --input data/streaming/input/microbatch_001.csv
```

No explicar cada linea del script.

## 1:40 - 2:15 | MongoDB Y API Flask

Mostrar que la API responde en navegador.

Endpoints a abrir:

```text
http://127.0.0.1:8000/stats
http://127.0.0.1:8000/sentiments
http://127.0.0.1:8000/predictions/latest
```

Tambien se puede mencionar:

```text
POST /predict
```

Explicar:

```text
MongoDB almacena las predicciones y Flask las expone mediante endpoints REST. Power BI usa estos endpoints como fuente de datos.
```

## 2:15 - 3:10 | Power BI

Mostrar Power BI Desktop o capturas en `dashboard/exports/`.

Visualizaciones que se deben mostrar:

- tarjeta total de predicciones
- distribucion de sentimientos
- evolucion temporal o por micro-batch
- tabla de predicciones recientes

Texto sugerido:

```text
El dashboard consume la API Flask local. La distribucion muestra el conteo por sentimiento, la evolucion permite ver el comportamiento por tiempo o micro-batch y la tabla muestra predicciones recientes.
```

Archivo a mencionar:

```text
dashboard/powerbi/sentimientos.pbix
```

## 3:10 - 3:45 | Jenkins

Mostrar Jenkins o `infra/jenkins/Jenkinsfile`.

Explicar:

```text
Jenkins se usa como pipeline demostrativo local. Valida Docker, levanta MongoDB, ejecuta el job Spark, verifica que existan predicciones en MongoDB y consulta la API Flask.
```

Aclaracion:

```text
No es un despliegue productivo; es una validacion automatizada academica.
```

## 3:45 - 4:30 | Resultados Y Documentacion

Mostrar `docs/pruebas/`.

Mencionar:

- reportes de Spark, API, Power BI, Jenkins y GitHub
- reporte consolidado de mejora experimental del dataset v2
- decision de no integrar modelos experimentales aun

Texto sugerido:

```text
Tambien se documento una fase experimental para mejorar el dataset. La mejor referencia fue v2_augmented_1800, pero no se integro porque el recall negativo seguia bajo. El pipeline estable se mantiene separado.
```

## 4:30 - 5:00 | Cierre Tecnico

Texto sugerido:

```text
En conclusion, SentimentStream cumple un flujo end-to-end: ingesta y procesamiento con Spark, persistencia en MongoDB, exposicion con Flask, dashboard en Power BI y validacion con Jenkins. El proyecto queda documentado, reproducible y listo para entrega academica.
```

## Que No Explicar Para Ahorrar Tiempo

- No explicar todos los scripts experimentales.
- No leer todo el README.
- No abrir todos los reportes.
- No detallar cada linea de Docker Compose.
- No profundizar en todos los datasets v2.
- No afirmar que el modelo experimental fue integrado.
- No presentar Jenkins como produccion.
- No mostrar errores de terminal.

## Checklist Antes De Grabar

- API Flask responde.
- Power BI abre el archivo `dashboard/powerbi/sentimientos.pbix`.
- Capturas estan disponibles en `dashboard/exports/`.
- GitHub muestra el README actualizado.
- Jenkinsfile visible en `infra/jenkins/Jenkinsfile`.
- Terminal ubicada en la raiz del proyecto.
- Video configurado para durar entre 3 y 5 minutos.
