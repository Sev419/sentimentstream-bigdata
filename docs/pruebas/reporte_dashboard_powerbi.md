# Reporte De Dashboard Power BI

## Objetivo

Registrar el estado de la fase Power BI del proyecto SentimentStream despues de construir el dashboard real consumiendo la API Flask local.

Este reporte documenta la evidencia funcional disponible. No modifica componentes de procesamiento, persistencia, API, contenedores ni datasets.

## Estado Registrado

El dashboard fue construido en Power BI Desktop y consume datos desde la API Flask del proyecto SentimentStream.

La validacion registrada corresponde a un dashboard real con:

- Tarjeta `Total de Predicciones`.
- Grafico `Distribucion de Sentimientos`.
- Tabla `Predicciones Recientes`.

El valor observado en la tarjeta total es:

```text
Total de Predicciones = 25
```

## Endpoints Usados

### `GET /stats`

URL local:

```text
http://127.0.0.1:8000/stats
```

Uso en el dashboard:

- Alimentar la tarjeta de total de predicciones.
- Alimentar el grafico de distribucion por sentimiento predicho.

Transformacion aplicada en Power Query:

- El campo `by_predicted_label` fue preparado en formato largo para usar:
  - `predicted_label`
  - `cantidad`
  - `total`

### `GET /sentiments`

URL local:

```text
http://127.0.0.1:8000/sentiments
```

Uso en el dashboard:

- Alimentar la tabla de predicciones recientes.
- Mostrar registros clasificados con sus campos de trazabilidad.

## Visualizaciones Creadas

### Tarjeta Total

Visualizacion creada:

- Tarjeta `Total de Predicciones`.

Fuente:

- Endpoint `/stats`.

Resultado observado:

```text
25
```

### Grafico De Distribucion

Visualizacion creada:

- Grafico `Distribucion de Sentimientos`.

Fuente:

- Endpoint `/stats`.

Campos usados:

- `predicted_label`
- `cantidad`

Proposito:

- Mostrar la distribucion de predicciones por sentimiento.

### Tabla De Predicciones Recientes

Visualizacion creada:

- Tabla `Predicciones Recientes`.

Fuente:

- Endpoint `/sentiments`.

Proposito:

- Mostrar predicciones recientes consumidas desde la API Flask.
- Revisar textos, etiquetas predichas y campos de trazabilidad disponibles.

## Evidencias Del Dashboard

Se registran las siguientes evidencias asociadas al dashboard Power BI:

- Archivo Power BI:
  - `dashboard/powerbi/sentimentstream_dashboard.pbix`
- Captura general del dashboard:
  - `dashboard/exports/dashboard_overview.png`
- Captura de la tarjeta total:
  - `dashboard/exports/card_total.png`
- Captura del grafico de distribucion:
  - `dashboard/exports/chart_distribution.png`
- Captura de la tabla de predicciones:
  - `dashboard/exports/table_predictions.png`

Evidencias confirmadas:

- Las capturas muestran datos reales consumidos desde la API Flask.
- La tarjeta total muestra `25` predicciones.
- La distribucion de sentimientos corresponde a `9/8/8`.
- El dashboard incluye tarjeta total, grafico de distribucion y tabla de predicciones recientes.

## Alcance De Esta Actualizacion

Esta actualizacion solo documenta la fase Power BI.

No se modifico:

- Spark.
- MongoDB.
- Flask.
- Docker.
- Datasets.
- Archivos JSON mock.
- Jenkins.

## Pendientes Antes De Jenkins

Antes de avanzar a Jenkins, quedan pendientes estas actividades:

1. Confirmar la ruta final del archivo `.pbix` usado como entregable.
2. Ejecutar una validacion final de actualizacion de datos desde Power BI contra la API Flask.
3. Verificar que las capturas registradas correspondan a la version final del dashboard.
4. Actualizar la documentacion final de cierre visual si se agregan nuevas evidencias.
5. Mantener Jenkins sin cambios hasta que la fase Power BI quede cerrada formalmente.

## Conclusion

La fase Power BI queda registrada como construida y validada visualmente con consumo desde la API Flask local.

El dashboard incluye tarjeta total, grafico de distribucion y tabla de predicciones recientes. Jenkins no se aborda en esta fase.
