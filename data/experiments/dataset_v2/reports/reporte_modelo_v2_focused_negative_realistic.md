# Reporte Modelo V2 Focused Negative Realistic

## Metricas

| Metrica | Valor |
| --- | ---: |
| Accuracy | 0.786667 |
| Precision ponderada | 0.79448 |
| Recall ponderado | 0.786667 |
| F1 ponderado | 0.781374 |

## Recall Por Clase

| Clase | Recall |
| --- | ---: |
| negativo | 0.64 |
| neutral | 0.97 |
| positivo | 0.75 |

## Comparacion

| Experimento | F1 |
| --- | ---: |
| v2_curated realistic | 0.737524 |
| v2_augmented realistic | 0.792533 |
| v2_focused_negative realistic | 0.781374 |

## Matriz De Confusion

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 64 | 12 | 24 |
| neutral | 1 | 97 | 2 |
| positivo | 9 | 16 | 75 |

## Recomendacion

Mejora parcial. Revisar errores por clase antes de integrar.

## Nota De Aislamiento

Evaluacion experimental aislada. No modifica ni integra el pipeline productivo.
