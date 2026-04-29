# Reporte Modelo V2 Augmented 1800

## Proposito

Entrenar modelos con dataset augmented de 1800 registros, incorporando ejemplos dirigidos a errores realistic.

## Dataset

- Archivo: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_augmented_1800.csv`
- Total registros: `1800`
- Train: `1440`
- Test: `360`

## Modelos Evaluados

| Modelo | Accuracy | Precision ponderada | Recall ponderado | F1 ponderado |
| --- | ---: | ---: | ---: | ---: |
| logistic_regression | 1.0 | 1.0 | 1.0 | 1.0 |
| naive_bayes | 0.980556 | 0.981202 | 0.980556 | 0.980428 |

## Mejor Modelo Interno

- Modelo: `logistic_regression`
- F1 ponderado: `1.0`

## Nota De Aislamiento

Este entrenamiento solo lee `data/experiments/dataset_v2/labeled/` y escribe en `data/experiments/dataset_v2/reports/`.
No modifica ni integra el pipeline productivo.
