# Reporte Validacion Externa Modelo V2 1500

## Proposito

Evaluar el modelo experimental v2 1500 contra un dataset externo/adversarial mas natural y menos estructurado.

## Entrenamiento

- Dataset entrenamiento: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_labeled_1500.csv`
- Registros entrenamiento: `1500`
- Modelo: `logistic_regression`
- Vectorizacion: `TF-IDF ngram_range=(1, 2)`
- Limpieza: conservadora, sin stopwords agresivas

## Dataset Externo

- Dataset externo: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_external_validation.csv`
- Registros externos: `150`
- Distribucion externo:
  - negativo: `50`
  - neutral: `50`
  - positivo: `50`

## Comparacion Interna Vs Externa

| Evaluacion | Accuracy | F1 ponderado |
| --- | ---: | ---: |
| Interna v2 1500 | 1.0 | 1.0 |
| Externa adversarial | 0.74 | 0.735499 |

- Delta F1 externo vs interno: `-0.264501`

## Metricas Externas

| Metrica | Valor |
| --- | ---: |
| Accuracy | 0.74 |
| Precision ponderada | 0.742555 |
| Recall ponderado | 0.74 |
| F1 ponderado | 0.735499 |

## Matriz De Confusion Externa

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 33 | 6 | 11 |
| neutral | 0 | 46 | 4 |
| positivo | 8 | 10 | 32 |

## Riesgo De Sobreajuste Sintetico

El resultado interno perfecto del dataset v2 1500 puede explicarse por patrones sinteticos muy separables. La validacion externa usa frases mas naturales, ambiguas y menos estructuradas para medir generalizacion fuera del patron de generacion.

## Recomendacion Tecnica

No integrar al pipeline estable. La validacion externa muestra degradacion frente al resultado interno, lo que confirma riesgo de sobreajuste a patrones sinteticos.

## Archivos Generados

- `data/experiments/dataset_v2/reports/metricas_modelo_v2_external_validation.json`
- `data/experiments/dataset_v2/reports/predicciones_modelo_v2_external_validation.csv`

## Nota De Aislamiento

Esta evaluacion solo lee y escribe dentro de `data/experiments/dataset_v2/`.

No modifica `spark_processing/`, no conecta MongoDB, no reemplaza modelos productivos y no toca Flask, Docker, Jenkins ni Power BI.
