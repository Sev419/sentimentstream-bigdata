# Guia Visualizacion Temporal Power BI

## Objetivo

Agregar al dashboard de Power BI una visualizacion de evolucion temporal o por micro-batch para alinear la entrega con la rubrica de la actividad.

Esta guia no crea dashboards ficticios ni modifica automaticamente el archivo `.pbix`.

## Fuente De Datos

Usar la consulta conectada al endpoint:

```text
http://127.0.0.1:8000/sentiments
```

Esta consulta alimenta la tabla de predicciones recientes y debe contener campos como texto, sentimiento predicho y campos de trazabilidad disponibles.

## Campo Recomendado Para El Eje Temporal

Prioridad de uso:

1. `event_time`, si existe y Power BI lo reconoce como fecha/hora.
2. `created_at`, si las predicciones vienen desde el endpoint `/predict`.
3. `fecha`, si el dato esta disponible desde la fuente.
4. `microbatch_id`, si no hay fecha confiable.

Si se usa `microbatch_id`, la visualizacion debe explicarse como evolucion por lote procesado, no como serie temporal real.

## Preparacion En Power Query

1. Abrir Power BI Desktop.
2. Ir a `Transformar datos`.
3. Seleccionar la consulta que consume `/sentiments`.
4. Verificar que exista un campo temporal o de lote:
   - `event_time`
   - `created_at`
   - `fecha`
   - `microbatch_id`
5. Si se usa `event_time`, `created_at` o `fecha`, cambiar el tipo de dato a `Fecha/Hora` o `Fecha`.
6. Si se usa `microbatch_id`, dejarlo como `Texto` o `Numero entero`, segun como llegue desde la API.
7. Verificar que `predicted_label` este como `Texto`.
8. Cerrar y aplicar cambios.

## Crear Grafico De Evolucion

Visual recomendado:

```text
Grafico de lineas
```

Alternativa:

```text
Grafico de columnas agrupadas
```

Configuracion:

- Eje X:
  - `event_time`, `created_at`, `fecha` o `microbatch_id`
- Valores:
  - conteo de registros
  - puede usarse conteo de `id`, conteo de `texto` o conteo de filas
- Leyenda:
  - `predicted_label`

Titulo sugerido:

```text
Evolucion De Predicciones Por Sentimiento
```

## Si No Aparece Conteo De Filas

Opciones:

1. Arrastrar `id` a valores y cambiar agregacion a `Recuento`.
2. Arrastrar `texto` a valores y cambiar agregacion a `Recuento`.
3. Crear una columna auxiliar en Power Query llamada `cantidad` con valor `1`, solo dentro del modelo Power BI.

No modificar datasets productivos para crear esta visualizacion.

## Alineacion Con La Rubrica

La actividad solicita minimo:

- distribucion de sentimientos
- evolucion temporal
- tabla de predicciones recientes

Con esta visualizacion, el dashboard queda alineado asi:

| Requisito | Visualizacion |
| --- | --- |
| Distribucion de sentimientos | Grafico de barras por `predicted_label` |
| Evolucion temporal | Grafico por `event_time`, `fecha` o `microbatch_id` |
| Tabla de predicciones recientes | Tabla conectada a `/sentiments` |

La tarjeta de total de predicciones puede mantenerse como visual adicional.

## Recomendacion Para El Video

Durante el video, mostrar brevemente:

1. El dashboard completo.
2. La tarjeta total.
3. La distribucion por sentimiento.
4. La evolucion por tiempo o micro-batch.
5. La tabla de predicciones recientes.

Explicar que Power BI consume datos desde la API Flask local y no desde archivos pegados manualmente.

## Restricciones

- No crear datos ficticios.
- No modificar el `.pbix` automaticamente desde scripts.
- No modificar Spark.
- No modificar MongoDB.
- No modificar Flask.
- No modificar Docker.
- No modificar datasets productivos.
