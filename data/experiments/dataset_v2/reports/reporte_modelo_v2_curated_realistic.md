# Reporte Validacion Realistic Modelo V2 Curated

## Proposito

Evaluar el modelo entrenado con `dataset_sentimientos_v2_curated_1500.csv` sobre un dataset realistic de 300 registros mas natural y menos estructurado.

## Entrenamiento

- Dataset entrenamiento: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_curated_1500.csv`
- Registros entrenamiento: `1500`
- Modelo: `logistic_regression`
- Vectorizacion: `TF-IDF ngram_range=(1, 2)`
- Limpieza: conservadora

## Dataset Realistic

- Dataset realistic: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_realistic_validation.csv`
- Registros: `300`
- Distribucion:
  - negativo: `100`
  - neutral: `100`
  - positivo: `100`

## Metricas Realistic

| Metrica | Valor |
| --- | ---: |
| Accuracy | 0.746667 |
| Precision ponderada | 0.768151 |
| Recall ponderado | 0.746667 |
| F1 ponderado | 0.737524 |

## Comparacion Final

| Experimento | F1 | Nota |
| --- | ---: | --- |
| v2_300 | 0.622983 | baseline interno 300 |
| v2_1500 sintetico externo | 0.735499 | validacion externa previa |
| v2_curated externo | 0.932261 | validacion externa curated |
| v2_curated realistic | 0.737524 | validacion realistic final |

## Matriz De Confusion Realistic

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 53 | 15 | 32 |
| neutral | 2 | 95 | 3 |
| positivo | 5 | 19 | 76 |

## Recomendacion Tecnica Final

No integrar. Se debe mejorar el dataset antes de promover el modelo.

## Nota De Aislamiento

Esta evaluacion solo lee y escribe dentro de `data/experiments/dataset_v2/`.

No modifica `spark_processing/`, no conecta MongoDB, no reemplaza modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
