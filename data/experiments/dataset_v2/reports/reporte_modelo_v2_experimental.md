# Reporte Modelo V2 Experimental

## Proposito

Entrenar modelos NLP simples sobre el dataset experimental v2 de 300 registros, sin modificar el pipeline estable de SentimentStream.

## Dataset

- Archivo: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_labeled_300.csv`
- Total registros: `300`
- Train: `240`
- Test: `60`
- Estratificacion: `True`

## Distribucion General

| Clase | Registros |
| --- | ---: |
| negativo | 100 |
| neutral | 100 |
| positivo | 100 |

## Modelos Evaluados

| Modelo | Accuracy | Precision ponderada | Recall ponderado | F1 ponderado |
| --- | ---: | ---: | ---: | ---: |
| naive_bayes | 0.616667 | 0.634697 | 0.616667 | 0.622983 |
| logistic_regression | 0.616667 | 0.632767 | 0.616667 | 0.620642 |

## Mejor Modelo Experimental

- Modelo: `naive_bayes`
- Accuracy: `0.616667`
- F1 ponderado: `0.622983`

## Comparacion Contra Baseline V1

Baseline v1 conocido:

- Filas usadas: `30`
- Accuracy aproximado: `0.111111`
- F1 ponderado aproximado: `0.066667`

Resultado v2 experimental:

- Filas usadas: `300`
- Mejor accuracy: `0.616667`
- Mejor F1 ponderado: `0.622983`

Esta comparacion es preliminar porque el dataset v2 es experimental y no esta integrado al pipeline productivo.

## Matrices De Confusion

### Matriz De Confusion - naive_bayes

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 12 | 0 | 8 |
| neutral | 3 | 15 | 2 |
| positivo | 8 | 2 | 10 |

### Matriz De Confusion - logistic_regression

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 9 | 0 | 11 |
| neutral | 2 | 16 | 2 |
| positivo | 6 | 2 | 12 |

## Archivos Generados

- Metricas JSON: `data/experiments/dataset_v2/reports/metricas_modelo_v2_experimental.json`
- Predicciones test: `data/experiments/dataset_v2/reports/predicciones_modelo_v2_experimental.csv`

## Nota De Aislamiento

Este entrenamiento solo lee `data/experiments/dataset_v2/labeled/` y solo escribe en `data/experiments/dataset_v2/reports/`.

No modifica `spark_processing/`, no conecta MongoDB, no guarda modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
