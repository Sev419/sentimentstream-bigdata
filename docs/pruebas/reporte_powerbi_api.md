# Reporte de Preparacion Power BI y API Flask

## Estado Actual

La API Flask se encuentra operativa y responde contra MongoDB real en local:

- API: `http://127.0.0.1:8000`
- Servicio Compose: `api`
- Contenedor: `sentimentstream-api`
- Origen de datos: `MongoDB` con `25` documentos reales en `sentimentstream_db.predictions`

## Endpoints Disponibles

### `GET /sentiments`

URL local:

```text
http://127.0.0.1:8000/sentiments
```

Estructura real:

```json
{
  "items": [
    {
      "created_at": "string",
      "event_time": "string",
      "id": 1,
      "microbatch_id": 1,
      "microbatch_source_file": "string",
      "predicted_label": "positivo",
      "prediction": 2.0,
      "sentimiento": "positivo",
      "source": "spark_processing",
      "texto": "string",
      "texto_preprocesado": "string"
    }
  ]
}
```

Uso recomendado en Power BI:

- Tabla de registros.
- Detalle de predicciones por microbatch.
- Historial de textos clasificados.

Campos recomendados:

- `created_at`
- `event_time`
- `id`
- `microbatch_id`
- `microbatch_source_file`
- `predicted_label`
- `prediction`
- `sentimiento`
- `source`
- `texto`
- `texto_preprocesado`

### `GET /stats`

URL local:

```text
http://127.0.0.1:8000/stats
```

Estructura real:

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

Uso recomendado en Power BI:

- Tarjeta para `total`.
- Grado / donut / barras para `by_predicted_label`.
- Resumen ejecutivo de distribución por sentimiento predicho.

Campos recomendados:

- `total`
- `by_predicted_label.negativo`
- `by_predicted_label.neutral`
- `by_predicted_label.positivo`

### `GET /predictions/latest`

URL local:

```text
http://127.0.0.1:8000/predictions/latest
```

Estructura real:

```json
{
  "item": {
    "created_at": "string",
    "event_time": "string",
    "id": 1,
    "microbatch_id": 1,
    "microbatch_source_file": "string",
    "predicted_label": "positivo",
    "prediction": 2.0,
    "sentimiento": "positivo",
    "source": "spark_processing",
    "texto": "string",
    "texto_preprocesado": "string"
  }
}
```

Uso recomendado en Power BI:

- Tarjeta de "ultimo registro".
- Tabla de detalle para depuracion.
- Vista operativa de la prediccion mas reciente.

Campos recomendados:

- mismos campos que `/sentiments`, usando `item` como registro unico

## Como Conectar Power BI A La API

1. Abrir Power BI Desktop.
2. Elegir `Obtener datos`.
3. Seleccionar `Web`.
4. Pegar la URL del endpoint:
   - `http://127.0.0.1:8000/sentiments`
   - `http://127.0.0.1:8000/stats`
   - `http://127.0.0.1:8000/predictions/latest`
5. En el Editor de Power Query:
   - expandir `items` para `/sentiments`
   - expandir `item` para `/predictions/latest`
   - convertir `by_predicted_label` en una tabla o usar una consulta separada para el resumen de estadisticas
6. Cargar los datos al modelo de Power BI.

## Visualizaciones Recomendadas

- `GET /stats`
  - tarjeta con `total`
  - barras o donut por `by_predicted_label`
- `GET /sentiments`
  - tabla de textos y predicciones
  - conteo por `microbatch_id`
  - linea temporal usando `event_time`
- `GET /predictions/latest`
  - tarjeta de ultimo sentimiento
  - tarjeta de ultimo texto

## Limitaciones Actuales

- La API corre en modo local y de desarrollo.
- `POST /predict` sigue siendo un predictor liviano de demostracion, no el modelo Spark principal.
- `GET /stats` devuelve un objeto anidado que en Power BI requiere una transformacion adicional.
- La conexion Power BI se hace contra Flask, no directo a Mongo, para mantener la capa de exposicion ya validada.

## Proximos Pasos

1. Construir el reporte o dashboard en Power BI usando los endpoints reales.
2. Documentar capturas y evidencias en `dashboard/exports/`.
3. Preparar la fase de Jenkins cuando la parte visual quede resuelta.

