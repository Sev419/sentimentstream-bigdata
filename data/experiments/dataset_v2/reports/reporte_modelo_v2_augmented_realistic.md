# Reporte Modelo V2 Augmented Realistic

## Proposito

Evaluar el dataset augmented 1800 contra la validacion realistic, sin mezclar datos externos con entrenamiento.

## Metricas Realistic

| Metrica | Valor |
| --- | ---: |
| Accuracy | 0.796667 |
| Precision ponderada | 0.805523 |
| Recall ponderado | 0.796667 |
| F1 ponderado | 0.792533 |

## Recall Por Clase

| Clase | Recall |
| --- | ---: |
| negativo | 0.66 |
| neutral | 0.96 |
| positivo | 0.77 |

## Comparacion Final

| Experimento | F1 |
| --- | ---: |
| v2_300 | 0.622983 |
| v2_1500 externo | 0.735499 |
| v2_curated realistic | 0.737524 |
| v2_augmented realistic | 0.792533 |

## Matriz De Confusion

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 66 | 12 | 22 |
| neutral | 2 | 96 | 2 |
| positivo | 7 | 16 | 77 |

## Conclusion

Mejora documentada, pero se deben revisar errores y estabilidad por clase antes de integrar.

## Nota De Aislamiento

Esta evaluacion solo lee y escribe dentro de `data/experiments/dataset_v2/`.
No modifica ni integra el pipeline productivo.
