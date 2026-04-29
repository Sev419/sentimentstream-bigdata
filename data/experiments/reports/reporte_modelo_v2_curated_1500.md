# Reporte Modelo V2 Curated 1500

## Proposito

Entrenar modelos NLP con el dataset v2 curado de 1500 registros usando baseline conservador.

## Dataset

- Archivo: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_curated_1500.csv`
- Total registros: `1500`
- Train: `1200`
- Test: `300`
- Estratificacion: `True`

## Enfoque

- Preprocesamiento ligero.
- Sin eliminacion agresiva de stopwords.
- TF-IDF con `ngram_range=(1, 2)`.
- Modelos: Naive Bayes y Logistic Regression.

## Modelos Evaluados

| Modelo | Accuracy | Precision ponderada | Recall ponderado | F1 ponderado |
| --- | ---: | ---: | ---: | ---: |
| naive_bayes | 0.993333 | 0.993464 | 0.993333 | 0.993333 |
| logistic_regression | 1.0 | 1.0 | 1.0 | 1.0 |

## Mejor Modelo Interno

- Modelo: `logistic_regression`
- Accuracy: `1.0`
- F1 ponderado: `1.0`

## Matrices De Confusion

### Matriz De Confusion - naive_bayes

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 100 | 0 | 0 |
| neutral | 0 | 100 | 0 |
| positivo | 0 | 2 | 98 |

### Matriz De Confusion - logistic_regression

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 100 | 0 | 0 |
| neutral | 0 | 100 | 0 |
| positivo | 0 | 0 | 100 |

## Nota De Aislamiento

Este entrenamiento solo lee `data/experiments/dataset_v2/labeled/` y solo escribe en `data/experiments/dataset_v2/reports/`.
No modifica ni integra el pipeline productivo.
