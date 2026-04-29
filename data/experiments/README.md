# Dataset V2 Experimental

## Proposito

Esta carpeta contiene la base experimental para una futura mejora del dataset de SentimentStream.

Su objetivo es permitir trabajo controlado sobre nuevos datos, etiquetas, auditorias y salidas de preparacion sin afectar el pipeline estable del proyecto.

## Advertencia

Esta zona es experimental.

No debe usarse como entrada del pipeline productivo hasta que existan evidencias de calidad, auditoria y mejora real de metricas.

No conectar esta carpeta directamente con:

- `spark_processing/`
- `api_flask/`
- MongoDB
- Power BI
- Jenkins
- `docker-compose.yml`

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

- `raw/`: archivos base del dataset v2 antes de limpieza o transformacion.
- `labeled/`: archivos revisados o etiquetados manualmente.
- `processed/`: salidas procesadas experimentales.
- `reports/`: auditorias, metricas y reportes de validacion del dataset v2.

## Reglas De Uso

- No sobrescribir archivos de `data/raw/`.
- No sobrescribir archivos de `data/processed/`.
- No modificar `data/streaming/input/microbatch_001.csv`.
- No usar estos datos en el pipeline estable sin validacion previa.
- No guardar datos sensibles, credenciales ni informacion personal.
- Mantener nombres de archivos con sufijo `v2` cuando aplique.
- Documentar cualquier cambio relevante en `reports/`.
- Comparar resultados contra el dataset actual antes de proponer integracion.
