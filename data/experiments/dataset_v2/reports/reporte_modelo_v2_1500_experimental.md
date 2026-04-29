# Reporte Modelo V2 1500 Experimental

## Proposito

Entrenar modelos NLP experimentales con el dataset v2 de 1500 registros usando el enfoque conservador que funciono mejor en el experimento de 300 registros.

## Dataset

- Archivo: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_labeled_1500.csv`
- Total registros: `1500`
- Train: `1200`
- Test: `300`
- Estratificacion: `True`

## Distribucion General

| Clase | Total | Train | Test |
| --- | ---: | ---: | ---: |
| negativo | 500 | 400 | 100 |
| neutral | 500 | 400 | 100 |
| positivo | 500 | 400 | 100 |

## Enfoque

- Limpieza basica conservadora.
- Sin eliminacion agresiva de stopwords.
- TF-IDF con `ngram_range=(1, 2)`.
- Modelos simples: Naive Bayes y Logistic Regression.

## Modelos Evaluados

| Modelo | Accuracy | Precision ponderada | Recall ponderado | F1 ponderado |
| --- | ---: | ---: | ---: | ---: |
| naive_bayes | 0.983333 | 0.984127 | 0.983333 | 0.983323 |
| logistic_regression | 1.0 | 1.0 | 1.0 | 1.0 |

## Mejor Modelo Experimental

- Modelo: `logistic_regression`
- Accuracy: `1.0`
- F1 ponderado: `1.0`

## Comparacion Contra Experimentos Previos

| Referencia | Accuracy | F1 ponderado | Delta F1 vs mejor 1500 |
| --- | ---: | ---: | ---: |
| baseline_v1 | 0.111111 | 0.066667 | 0.933333 |
| baseline_v2_300 | 0.616667 | 0.622983 | 0.377017 |
| improved_v2_300 | 0.55 | 0.556099 | 0.443901 |

## Matrices De Confusion

### Matriz De Confusion - naive_bayes

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 100 | 0 | 0 |
| neutral | 0 | 100 | 0 |
| positivo | 5 | 0 | 95 |

### Matriz De Confusion - logistic_regression

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 100 | 0 | 0 |
| neutral | 0 | 100 | 0 |
| positivo | 0 | 0 | 100 |

## Archivos Generados

- Metricas JSON: `data/experiments/dataset_v2/reports/metricas_modelo_v2_1500_experimental.json`
- Predicciones test: `data/experiments/dataset_v2/reports/predicciones_modelo_v2_1500_experimental.csv`

## Nota De Aislamiento

Este entrenamiento solo lee `data/experiments/dataset_v2/labeled/` y solo escribe en `data/experiments/dataset_v2/reports/`.

No modifica `spark_processing/`, no conecta MongoDB, no guarda modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
