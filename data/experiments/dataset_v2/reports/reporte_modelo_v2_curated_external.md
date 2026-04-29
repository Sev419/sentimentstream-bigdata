# Reporte Evaluacion Externa Modelo V2 Curated

## Proposito

Evaluar el modelo entrenado con `dataset_sentimientos_v2_curated_1500.csv` sobre el dataset externo existente, sin mezclar datos externos con entrenamiento.

## Dataset De Entrenamiento

- Archivo: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_curated_1500.csv`
- Registros: `1500`

## Dataset Externo

- Archivo: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_external_validation.csv`
- Registros: `150`
- Distribucion: negativo `50`, neutral `50`, positivo `50`

## Metricas Externas Curated

| Metrica | Valor |
| --- | ---: |
| Accuracy | 0.933333 |
| Precision ponderada | 0.936304 |
| Recall ponderado | 0.933333 |
| F1 ponderado | 0.932261 |

## Comparacion Final

| Experimento | F1 externo | Nota |
| --- | ---: | --- |
| v2_300 | N/A | solo referencia interna F1 0.622983 |
| v2_1500 sintetico | 0.735499 | validacion externa previa |
| v2_curated_1500 | 0.932261 | validacion externa actual |

- Delta F1 curated vs sintetico externo: `0.196762`
- Criterio de exito F1 >= 0.78: `True`

## Matriz De Confusion Externa

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 42 | 4 | 4 |
| neutral | 0 | 50 | 0 |
| positivo | 1 | 1 | 48 |

## Recomendacion Tecnica

No integrar aun al pipeline estable. Aunque el dataset curado mejora frente al sintetico en validacion externa, debe ampliarse con textos reales y revisar estabilidad antes de promoverlo.

## Nota De Aislamiento

Esta evaluacion solo lee y escribe dentro de `data/experiments/dataset_v2/`.

No modifica `spark_processing/`, no conecta MongoDB, no reemplaza modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
