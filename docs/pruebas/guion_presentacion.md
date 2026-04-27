# Guion De Presentacion - SentimentStream

Duracion estimada: 5 a 7 minutos.

Repositorio:

```text
https://github.com/Sev419/sentimentstream-bigdata
```

## 0:00 - 0:45 | Introduccion

Buenos dias. Hoy presento SentimentStream, un proyecto de Big Data orientado al analisis de sentimientos en textos.

El problema que aborda es el siguiente: cuando una organizacion recibe muchos comentarios, opiniones o mensajes, necesita una forma automatizada de procesarlos, clasificarlos y visualizarlos para entender rapidamente la distribucion de sentimientos.

SentimentStream resuelve este flujo de extremo a extremo. No se queda solo en entrenar un modelo o crear un dashboard aislado, sino que integra procesamiento de datos, persistencia, API, visualizacion y automatizacion basica.

La arquitectura final del proyecto es:

```text
Spark -> MongoDB -> Flask API -> Power BI -> Jenkins
```

## 0:45 - 2:00 | Arquitectura Paso A Paso

El primer componente es Spark con PySpark. Spark se encarga de procesar micro-batches de datos en formato CSV. En este proyecto los micro-batches simulan un flujo de datos por lotes pequenos, que es una aproximacion comun cuando se quiere representar procesamiento cercano a streaming.

Despues del procesamiento, las predicciones se guardan en MongoDB. Mongo funciona como capa de persistencia, donde quedan almacenados los textos procesados, sus etiquetas predichas y campos de trazabilidad.

Luego aparece Flask. La API Flask consulta MongoDB y expone endpoints REST para que otros consumidores puedan acceder a la informacion sin conectarse directamente a la base de datos.

Power BI consume esos endpoints de Flask. A partir de la API se construyo un dashboard con indicadores visuales del estado de las predicciones.

Finalmente, Jenkins se uso como una capa DevOps demostrativa. Su funcion es validar automaticamente pasos basicos del flujo: que Docker responda, que Mongo levante, que Spark procese, que Mongo tenga datos y que la API responda.

## 2:00 - 3:10 | Demostracion Del Flujo

El flujo inicia con un archivo de entrada, por ejemplo:

```text
data/streaming/input/microbatch_001.csv
```

Ese microbatch es procesado por el job de Spark:

```text
spark_processing/jobs/process_microbatch_sentiments.py
```

El job genera predicciones de sentimiento y las inserta en MongoDB, en la base:

```text
sentimentstream_db
```

y en la coleccion:

```text
predictions
```

Luego Flask expone esos datos mediante endpoints como:

```text
/stats
/sentiments
/predictions/latest
```

El endpoint `/stats` permite consultar el total de predicciones y la distribucion por sentimiento. El endpoint `/sentiments` entrega registros procesados, que luego se usan para alimentar la tabla de predicciones recientes en Power BI.

En resumen, el recorrido es:

```text
microbatch -> prediccion -> MongoDB -> API Flask -> dashboard Power BI
```

## 3:10 - 4:10 | Explicacion Del Dashboard

El dashboard de Power BI resume visualmente el resultado del pipeline.

Primero, tiene una tarjeta de total de predicciones. Esta tarjeta muestra el numero total de registros procesados disponibles desde la API.

Segundo, tiene un grafico de distribucion de sentimientos. Este grafico permite comparar las predicciones por etiqueta, por ejemplo positivo, neutral y negativo.

Tercero, incluye una tabla de predicciones recientes. Esta tabla permite revisar los registros procesados, sus textos y la etiqueta de sentimiento generada.

Un punto importante es que el dashboard no esta basado en datos manuales. Consume la API Flask, y Flask a su vez lee desde MongoDB. Eso mantiene la separacion entre procesamiento, persistencia, servicio y visualizacion.

El archivo del dashboard esta en:

```text
dashboard/powerbi/sentimientos.pbix
```

y las capturas estan en:

```text
dashboard/exports/
```

## 4:10 - 5:00 | Tecnologias Utilizadas Y Justificacion

Se uso PySpark porque el objetivo era trabajar con una herramienta de procesamiento distribuido, apropiada para escenarios Big Data.

Se uso MongoDB porque permite guardar documentos flexibles con campos de texto, etiquetas, fechas y metadatos sin requerir un esquema rigido.

Se uso Flask porque permite construir una API REST simple, clara y suficiente para exponer los datos procesados.

Se uso Power BI porque facilita convertir los resultados en visualizaciones entendibles para usuarios tecnicos y no tecnicos.

Se uso Docker para mejorar la reproducibilidad del entorno y reducir problemas de configuracion local.

Se uso Jenkins para demostrar una validacion automatizada basica del flujo, como primer acercamiento a CI/CD.

## 5:00 - 6:10 | Retos Encontrados Y Soluciones

Uno de los retos principales fue ejecutar Spark en Windows. Spark puede ser sensible a rutas con espacios, configuraciones de Java y comportamiento del entorno local. Para resolverlo, el procesamiento principal se llevo a Docker, donde el entorno es mas controlado.

Otro reto fue coordinar Spark con MongoDB. La solucion fue levantar Mongo como servicio en Docker Compose y configurar el job de Spark para escribir en la base `sentimentstream_db`.

Tambien hubo retos con Power BI, especialmente al transformar la respuesta de `/stats`. El campo `by_predicted_label` llegaba como columnas separadas y fue necesario convertirlo a formato largo en Power Query para crear correctamente el grafico de distribucion.

Finalmente, Jenkins presento el reto de integrarse con Docker. Por eso se planteo como pipeline basico y demostrativo, enfocado en validar comandos esenciales y no como despliegue productivo.

## 6:10 - 6:45 | Limitaciones

El proyecto tiene algunas limitaciones claras.

El dataset es pequeno y se uso con fines academicos. El modelo baseline es simple y no pretende competir con modelos avanzados de NLP.

La API y Power BI trabajan en entorno local, usando `127.0.0.1`.

Jenkins no esta configurado como pipeline de produccion. Es una validacion demostrativa del flujo.

Tampoco se implemento despliegue en nube ni Kubernetes, porque el objetivo del proyecto era demostrar la integracion local completa del pipeline.

## 6:45 - 7:00 | Conclusion Final

Como conclusion, SentimentStream logra integrar un flujo Big Data completo:

```text
datos -> Spark -> MongoDB -> Flask API -> Power BI -> Jenkins
```

El valor academico del proyecto esta en demostrar que los datos pueden pasar por todo el ciclo: entrada, procesamiento, almacenamiento, exposicion, visualizacion y validacion automatizada.

Es una base solida que podria evolucionar hacia datasets mas grandes, modelos NLP mas robustos, despliegue en nube y pipelines CI/CD mas completos.
