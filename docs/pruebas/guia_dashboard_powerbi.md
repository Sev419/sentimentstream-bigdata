# Guia Operativa para Dashboard Power BI

## Objetivo

Esta guia define como construir el dashboard real de SentimentStream en Power BI usando la API Flask ya validada.

La fuente principal sera:

- `http://127.0.0.1:8000/sentiments`
- `http://127.0.0.1:8000/stats`

## Estado Previsto

- Spark en Docker ya genera datos reales.
- MongoDB ya almacena predicciones reales.
- Flask ya expone informacion real desde MongoDB.
- Power BI solo consumira la API, sin tocar Spark, Mongo ni Flask.

## Endpoints A Usar

### 1. `GET /sentiments`

URL:

```text
http://127.0.0.1:8000/sentiments
```

Uso:

- tabla de predicciones recientes
- detalle de textos clasificados
- trazabilidad por microbatch

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

### 2. `GET /stats`

URL:

```text
http://127.0.0.1:8000/stats
```

Uso:

- tarjeta con total de registros
- grafico de distribucion por sentimiento predicho
- resumen ejecutivo

Campos recomendados:

- `total`
- `by_predicted_label.negativo`
- `by_predicted_label.neutral`
- `by_predicted_label.positivo`

## Visualizaciones Minimas

### Tarjeta Total

Fuente:

- `GET /stats`

Campo:

- `total`

Descripcion:

- Muestra el total de registros procesados.

### Grafico Por `predicted_label`

Fuente:

- `GET /stats`

Campos:

- `by_predicted_label.negativo`
- `by_predicted_label.neutral`
- `by_predicted_label.positivo`

Descripcion:

- Grafico de barras o dona para mostrar la distribucion de predicciones.

### Tabla De Predicciones Recientes

Fuente:

- `GET /sentiments`

Campos:

- `created_at`
- `event_time`
- `id`
- `microbatch_id`
- `predicted_label`
- `prediction`
- `sentimiento`
- `texto`

Descripcion:

- Tabla operativa con las predicciones mas recientes y sus textos.

## Como Conectar Power BI

1. Abrir Power BI Desktop.
2. Seleccionar `Obtener datos`.
3. Elegir `Web`.
4. Ingresar la URL del endpoint.
5. En Power Query:
   - para `/sentiments`, expandir `items`
   - para `/stats`, transformar el objeto anidado `by_predicted_label`
6. Cargar los datos al modelo.
7. Construir las visualizaciones minimas.

## Checklist De Validacion

- [ ] Power BI conecta a `http://127.0.0.1:8000/sentiments`
- [ ] Power BI conecta a `http://127.0.0.1:8000/stats`
- [ ] La tabla de predicciones muestra columnas reales
- [ ] La tarjeta total usa `total`
- [ ] El grafico por `predicted_label` usa `by_predicted_label`
- [ ] La tabla de recientes usa `texto`, `predicted_label` y `created_at`
- [ ] Los datos coinciden con la API Flask validada
- [ ] No se modifico Spark, Mongo ni Flask

## Capturas Y Evidencias Esperadas

Para documentar la entrega final, se recomienda guardar:

- captura de Power BI conectado a `/sentiments`
- captura de Power BI conectado a `/stats`
- captura del dashboard con tarjeta total
- captura del grafico por `predicted_label`
- captura de la tabla de predicciones recientes
- captura del ultimo refresh exitoso

Las evidencias pueden guardarse en:

```text
dashboard/exports/
```

## Proximos Pasos

1. Construir el `.pbix` real con las consultas anteriores.
2. Exportar capturas del dashboard terminado.
3. Guardar el archivo `.pbix` en una ubicacion definida para la entrega.
4. Documentar el cierre visual del proyecto.

## Restricciones

- No crear un dashboard ficticio.
- No tocar Spark.
- No tocar Mongo.
- No tocar Flask.
- No avanzar a Jenkins en esta fase.
