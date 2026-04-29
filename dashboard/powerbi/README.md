# Power BI Dashboard

## Proposito

Esta carpeta contiene el archivo Power BI final del proyecto SentimentStream.

El dashboard consume datos desde la API Flask local y forma parte de la evidencia visual del flujo:

```text
Spark -> MongoDB -> Flask API -> Power BI
```

## Archivo Principal

Archivo real del dashboard:

```text
dashboard/powerbi/sentimientos.pbix
```

No usar rutas alternativas para el `.pbix` en la documentacion final.

## Fuentes De Datos

Endpoints usados desde Power BI:

```text
GET http://127.0.0.1:8000/stats
GET http://127.0.0.1:8000/sentiments
```

Endpoint disponible para consulta reciente:

```text
GET http://127.0.0.1:8000/predictions/latest
```

La API Flask consulta MongoDB, donde se almacenan las predicciones generadas por el job Spark.

## Visualizaciones Actuales

El dashboard incluye:

- tarjeta `Total de Predicciones`
- grafico `Distribucion de Sentimientos`
- grafico de evolucion por micro-batch o campo temporal disponible
- tabla `Predicciones Recientes`

## Capturas Relacionadas

Las capturas finales se guardan en:

```text
dashboard/exports/
```

Archivos esperados:

- `dashboard/exports/dashboard_overview.png`
- `dashboard/exports/card_total.png`
- `dashboard/exports/chart_distribution.png`
- `dashboard/exports/chart_temporal.png`
- `dashboard/exports/table_predictions.png`

## Notas De Uso

- Abrir el archivo `.pbix` con Power BI Desktop.
- Verificar que la API Flask este disponible en `http://127.0.0.1:8000` antes de refrescar datos.
- Mantener las consultas conectadas a Flask, no a archivos manuales.
- No usar datos experimentales de `data/experiments/` en este dashboard.

## Restricciones

- No modificar Spark desde Power BI.
- No modificar MongoDB desde Power BI.
- No modificar Flask desde Power BI.
- No usar mocks JSON como fuente final del dashboard.
- No reemplazar el `.pbix` sin actualizar la documentacion y las capturas.
