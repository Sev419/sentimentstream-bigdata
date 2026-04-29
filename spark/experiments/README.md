# Experimentos Spark

## Advertencia

Esta carpeta esta reservada para experimentos futuros de entrenamiento y comparacion de modelos.

No pertenece al pipeline productivo actual y no debe conectarse automaticamente con:

- `spark_processing/`
- MongoDB
- Flask
- Power BI
- Jenkins

## Proposito

Permitir pruebas controladas sobre el dataset experimental v2 sin modificar scripts productivos.

## Modelos Futuros A Probar

- Naive Bayes
- Logistic Regression
- Linear SVM, si aplica

## Reglas De Uso

- No modificar scripts productivos desde esta carpeta.
- No escribir salidas en `data/processed/`.
- Guardar resultados experimentales en `data/experiments/dataset_v2/reports/`.
- Comparar metricas contra el baseline actual antes de proponer integracion.
- Documentar cualquier experimento antes de integrarlo al flujo principal.
