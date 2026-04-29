# Reporte Modelo V2 Improved

## Proposito

Evaluar una mejora experimental de features para NLP sin modificar el pipeline estable.

## Mejoras Aplicadas

- Lower case.
- Normalizacion basica de acentos.
- Eliminacion de puntuacion.
- Eliminacion de stopwords en espanol.
- TF-IDF con `ngram_range=(1, 2)`.
- `max_features=2000`.

## Dataset

- Archivo: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_labeled_300.csv`
- Total registros: `300`
- Train: `240`
- Test: `60`
- Estratificacion: `True`

## Modelos Evaluados

| Modelo | Accuracy | Precision ponderada | Recall ponderado | F1 ponderado |
| --- | ---: | ---: | ---: | ---: |
| naive_bayes | 0.55 | 0.564478 | 0.55 | 0.556099 |
| logistic_regression | 0.483333 | 0.491729 | 0.483333 | 0.487305 |
| linear_svm | 0.5 | 0.503133 | 0.5 | 0.501407 |

## Mejor Modelo Improved

- Modelo: `naive_bayes`
- Accuracy: `0.55`
- F1 ponderado: `0.556099`

## Comparacion Contra Baseline Experimental

- Baseline F1 ponderado: `0.622983`
- Baseline accuracy: `0.616667`
- Mejor F1 improved: `0.556099`
- Diferencia F1: `-0.066884`

## Matrices De Confusion

### Matriz De Confusion - naive_bayes

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 7 | 1 | 12 |
| neutral | 4 | 16 | 0 |
| positivo | 9 | 1 | 10 |

### Matriz De Confusion - logistic_regression

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 6 | 2 | 12 |
| neutral | 5 | 15 | 0 |
| positivo | 10 | 2 | 8 |

### Matriz De Confusion - linear_svm

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 6 | 4 | 10 |
| neutral | 5 | 15 | 0 |
| positivo | 10 | 1 | 9 |

## Nota De Aislamiento

Este experimento solo lee `data/experiments/dataset_v2/labeled/` y solo escribe en `data/experiments/dataset_v2/reports/`.

No modifica `spark_processing/`, no conecta MongoDB, no reemplaza modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
