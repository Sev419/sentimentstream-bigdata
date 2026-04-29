# Dataset V2 Experimental

## Proposito Actual

Esta carpeta contiene la fase experimental de mejora del dataset de SentimentStream.

Su objetivo es documentar y conservar datasets v2, auditorias, metricas, predicciones de prueba y reportes de validacion sin afectar el pipeline estable del proyecto.

Esta zona no alimenta el flujo productivo:

```text
Spark productivo -> MongoDB -> Flask API -> Power BI -> Jenkins
```

## Advertencia

Todo el contenido de esta carpeta es experimental.

No debe conectarse automaticamente con:

- `spark_processing/`
- `api_flask/`
- `database/`
- MongoDB
- Power BI
- Jenkins
- `docker-compose.yml`
- datasets productivos en `data/raw/`, `data/processed/` o `data/streaming/`

La version estable del proyecto sigue siendo el pipeline productivo actual.

## Estructura

```text
data/experiments/dataset_v2/
|-- raw/
|-- labeled/
|-- processed/
|-- reports/
`-- README.md
```

## Descripcion De Carpetas

- `raw/`: template y archivos base iniciales del dataset v2.
- `labeled/`: datasets experimentales etiquetados y versiones de validacion.
- `processed/`: reservado para salidas procesadas experimentales.
- `reports/`: auditorias, metricas, predicciones y reportes de evaluacion.

## Datasets Creados

Archivos principales en `labeled/`:

| Dataset | Proposito |
| --- | --- |
| `dataset_sentimientos_v2_labeled_300.csv` | Version inicial balanceada de 300 registros |
| `dataset_sentimientos_v2_labeled_1500.csv` | Version sintetica balanceada de 1500 registros |
| `dataset_sentimientos_v2_curated_1500.csv` | Version curada de 1500 registros con mayor variabilidad |
| `dataset_sentimientos_v2_augmented_1800.csv` | Version ampliada dirigida a errores realistic |
| `dataset_sentimientos_v2_focused_negative_1950.csv` | Version focalizada en negativos ambiguos |
| `dataset_sentimientos_v2_realistic_validation.csv` | Dataset de validacion realistic de 300 registros |

Tambien existen archivos de apoyo como:

- `dataset_sentimientos_v2_labeled.csv`
- `dataset_sentimientos_v2_external_validation.csv`

## Reportes Generados

Los reportes y metricas se encuentran en:

```text
data/experiments/dataset_v2/reports/
```

Tipos de evidencia generada:

- auditorias automaticas de datasets
- metricas JSON de auditoria
- reportes de entrenamiento experimental
- metricas de modelos
- predicciones de evaluacion
- evaluaciones externas y realistic
- analisis de errores
- analisis focalizado de errores negativos

Reportes clave:

- `reporte_modelo_v2_augmented_realistic.md`
- `metricas_modelo_v2_augmented_realistic.json`
- `reporte_modelo_v2_focused_negative_realistic.md`
- `metricas_modelo_v2_focused_negative_realistic.json`
- `reporte_errores_realistic.md`
- `reporte_errores_negativos_augmented.md`

## Resultado Consolidado

La mejor referencia experimental actual es:

```text
v2_augmented_1800
```

Resultado registrado:

```text
F1 realistic: 0.792533
Recall negativo: 0.66
Recall neutral: 0.96
Recall positivo: 0.77
```

La version `v2_focused_negative_1950` no se adopta porque no mejoro frente a `v2_augmented_1800`:

```text
F1 realistic: 0.781374
Recall negativo: 0.64
```

## Decision Tecnica

No se integra ningun dataset experimental al pipeline estable.

Motivo principal:

- el recall de la clase negativa sigue bajo para una integracion controlada.

El dataset `v2_augmented_1800` queda como mejor baseline experimental para futuras iteraciones, pero no reemplaza al dataset actual ni modifica la arquitectura productiva.

## Reglas De Uso

- No sobrescribir archivos en `data/raw/`.
- No sobrescribir archivos en `data/processed/`.
- No modificar `data/streaming/`.
- No conectar estos datasets a MongoDB.
- No usar estos datos desde Flask.
- No actualizar Power BI con estos datos experimentales.
- No modificar Docker Compose ni Jenkins.
- No reemplazar modelos o scripts productivos.
- Mantener cualquier nuevo experimento dentro de `data/experiments/` y `spark/experiments/`.

## Referencia Documental

El cierre consolidado de esta fase esta documentado en:

```text
docs/pruebas/reporte_consolidado_mejora_dataset_v2.md
```
