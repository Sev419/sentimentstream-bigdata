# Reporte Consolidado De Mejora Dataset V2

## Objetivo

Consolidar los resultados de la fase experimental de mejora del dataset v2 de SentimentStream, evaluando si alguna version experimental debe ser integrada al pipeline estable.

La mejora tuvo como objetivo aumentar la calidad del modelo de analisis de sentimientos mediante mas registros, mejor balance de clases, mayor variabilidad lexica y validaciones externas mas realistas.

## Alcance

Este reporte corresponde unicamente a la zona experimental del proyecto:

```text
data/experiments/
spark/experiments/
```

No se modifica ni se integra ningun cambio en el pipeline productivo.

## Versiones Evaluadas

| Version experimental | Descripcion | Evaluacion principal | Resultado |
| --- | --- | --- | --- |
| v2_300 | Dataset balanceado inicial de 300 registros | Validacion interna | F1 `0.622983` |
| v2_1500 sintetico | Dataset balanceado de 1500 registros con patrones muy separables | Interna y externa | F1 interno `1.0`, F1 externo `0.735499` |
| v2_curated_1500 | Dataset curado con mayor variedad y ambiguedad controlada | Externa curated y realistic | F1 externo curated `0.932261`, F1 realistic `0.737524` |
| v2_augmented_1800 | Dataset ampliado con ejemplos dirigidos a errores realistic | Realistic | F1 `0.792533`, recall negativo `0.66`, recall neutral `0.96`, recall positivo `0.77` |
| v2_focused_negative_1950 | Dataset focalizado en negativos ambiguos | Realistic | F1 `0.781374`, recall negativo `0.64` |

## Tabla Comparativa De Metricas

| Version | F1 principal | Recall negativo | Recall neutral | Recall positivo | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| v2_300 | 0.622983 | No registrado | No registrado | No registrado | Superado por versiones posteriores |
| v2_1500 sintetico | 0.735499 externo | No registrado | No registrado | No registrado | No integrar por riesgo de sobreajuste sintetico |
| v2_curated_1500 | 0.737524 realistic | No registrado | No registrado | No registrado | Mejora parcial, no suficiente para integrar |
| v2_augmented_1800 | 0.792533 realistic | 0.66 | 0.96 | 0.77 | Mejor referencia experimental actual |
| v2_focused_negative_1950 | 0.781374 realistic | 0.64 | 0.97 | 0.75 | No se adopta frente a augmented |

## Mejor Version Experimental

La mejor referencia experimental actual es `v2_augmented_1800`.

Esta version obtuvo el mejor equilibrio general en validacion realistic:

- F1 realistic: `0.792533`
- Recall negativo: `0.66`
- Recall neutral: `0.96`
- Recall positivo: `0.77`

Aunque no cumple completamente el criterio de integracion, representa la mejora experimental mas solida frente a las versiones anteriores.

## Por Que No Se Adopta v2_focused_negative_1950

La version `v2_focused_negative_1950` fue creada para mejorar especificamente el recall de la clase negativa. Sin embargo, los resultados no superaron a `v2_augmented_1800`:

- F1 realistic bajo de `0.792533` a `0.781374`.
- Recall negativo bajo de `0.66` a `0.64`.
- Recall positivo quedo en `0.75`.
- Recall neutral se mantuvo alto en `0.97`, pero el problema principal sigue en negativos ambiguos.

Por esta razon, `v2_focused_negative_1950` no debe adoptarse como referencia principal.

## Riesgos Detectados

- Riesgo de sobreajuste sintetico: las metricas internas perfectas no representan necesariamente generalizacion real.
- Persisten errores en negativos ambiguos, especialmente quejas suaves, decepcion moderada y experiencias mixtas con tono calmado.
- La clase neutral mantiene recall alto, pero puede absorber textos negativos expresados de forma moderada.
- La mejora de datos debe continuar con ejemplos mas naturales y validacion externa, no solo con aumento de volumen.

## Decision Final

No se debe integrar ningun modelo ni dataset experimental al pipeline estable por ahora.

La version `v2_augmented_1800` queda como mejor referencia experimental actual, pero el recall negativo de `0.66` sigue por debajo del criterio esperado para una integracion controlada.

El pipeline productivo de SentimentStream debe permanecer estable y sin modificaciones.

## Proximos Pasos Recomendados

1. Mantener `v2_augmented_1800` como baseline experimental actual.
2. Revisar manualmente los negativos clasificados como neutral o positivo.
3. Crear una nueva muestra de validacion externa con textos reales o semi-reales revisados manualmente.
4. Mejorar el etiquetado de casos frontera antes de generar mas registros.
5. Evaluar tecnicas complementarias sin modificar produccion, por ejemplo ajuste de pesos por clase o umbrales de decision.
6. Considerar integracion solo si se alcanza F1 realistic mayor o igual a `0.80` y recall negativo mayor o igual a `0.75`.

## Confirmacion De Aislamiento

Esta consolidacion no modifica Spark productivo, MongoDB, Flask, Docker, Jenkins, Power BI, datasets productivos ni el pipeline estable.
