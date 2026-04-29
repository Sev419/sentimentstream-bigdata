# Reporte Errores Negativos Augmented

## Resumen

- Archivo analizado: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\reports\predicciones_modelo_v2_augmented_realistic.csv`
- Negativos reales: `100`
- Negativos clasificados como neutral: `12`
- Negativos clasificados como positivo: `22`
- Total errores negativos: `34`
- Recall negativo observado: `0.66`

## Negativos Clasificados Como Neutral

| id | predicho | texto |
| ---: | --- | --- |
| 232 | neutral | La informacion fue contradictoria |
| 244 | neutral | La consulta quedo sin resolver |
| 254 | neutral | El producto no parecia en buen estado |
| 267 | neutral | El reporte estaba incompleto |
| 269 | neutral | La solicitud quedo bloqueada |
| 275 | neutral | La consulta quedo en el aire |
| 279 | neutral | El tramite se volvio agotador |
| 283 | neutral | La informacion estaba desactualizada |
| 289 | neutral | La entrega fue poco cuidadosa |
| 290 | neutral | La solicitud fue rechazada sin explicacion |
| 293 | neutral | El reporte genero confusion |
| 294 | neutral | La respuesta fue tardia e incompleta |

## Negativos Clasificados Como Positivo

| id | predicho | texto |
| ---: | --- | --- |
| 237 | positivo | El resultado final fue decepcionante |
| 238 | positivo | La gestion fue desordenada |
| 251 | positivo | No me gusto la forma en que cerraron el caso |
| 252 | positivo | El servicio prometia mas de lo que entrego |
| 253 | positivo | La espera fue larga y sin actualizaciones |
| 255 | positivo | La solucion no funciono cuando la probe |
| 257 | positivo | La respuesta no resolvio la duda |
| 260 | positivo | La comunicacion fue deficiente |
| 263 | positivo | El producto se sintio inestable |
| 264 | positivo | La plataforma mostro mensajes confusos |
| 265 | positivo | El proceso me hizo repetir pasos |
| 268 | positivo | La guia fue dificil de seguir |

## Patrones Frecuentes

### Negativo -> Neutral

| n-gram | frecuencia |
| --- | ---: |
| la | 8 |
| el | 5 |
| fue | 4 |
| quedo | 3 |
| consulta | 2 |
| consulta quedo | 2 |
| el reporte | 2 |
| en | 2 |
| estaba | 2 |
| informacion | 2 |
| la consulta | 2 |
| la informacion | 2 |
| la solicitud | 2 |
| reporte | 2 |
| sin | 2 |
| solicitud | 2 |
| agotador | 1 |
| aire | 1 |
| bloqueada | 1 |
| buen | 1 |

### Negativo -> Positivo

| n-gram | frecuencia |
| --- | ---: |
| la | 18 |
| el | 9 |
| fue | 7 |
| no | 6 |
| de | 3 |
| de lo | 2 |
| el producto | 2 |
| experiencia | 2 |
| gestion | 2 |
| la experiencia | 2 |
| la plataforma | 2 |
| lo | 2 |
| me | 2 |
| plataforma | 2 |
| producto | 2 |
| que | 2 |
| se | 2 |
| se sintio | 2 |
| sintio | 2 |
| actualizaciones | 1 |

## Lectura Tecnica

Los negativos ambiguos suelen contener problemas expresados con tono moderado, palabras informativas o frases que comparten vocabulario con positivos y neutrales. La siguiente iteracion debe reforzar quejas suaves, decepcion moderada, retrasos con cierre incompleto, y experiencias mixtas donde domina lo negativo.
