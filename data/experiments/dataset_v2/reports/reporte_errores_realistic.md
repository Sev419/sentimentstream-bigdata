# Reporte De Errores Realistic

## Resumen

- Archivo analizado: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\reports\predicciones_modelo_v2_curated_realistic.csv`
- Total predicciones: `300`
- Total errores: `76`
- Accuracy observado: `0.746667`

## Matriz De Confusion

| Real \ Predicho | negativo | neutral | positivo |
| --- | ---: | ---: | ---: |
| negativo | 53 | 15 | 32 |
| neutral | 2 | 95 | 3 |
| positivo | 5 | 19 | 76 |

## Falsos Positivos Y Falsos Negativos Por Clase

### Clase `negativo`

- Falsos positivos: `7`
- Falsos negativos: `47`

Falsos positivos representativos:

| id | real | predicho | texto |
| ---: | --- | --- | --- |
| 17 | positivo | negativo | La solucion no fue complicada y funciono |
| 18 | positivo | negativo | El proceso fue mas claro que otras veces |
| 64 | positivo | negativo | El soporte explico los pasos con claridad |
| 84 | positivo | negativo | La experiencia no tuvo mayores problemas |
| 87 | positivo | negativo | El tramite no fue pesado |

Falsos negativos representativos:

| id | real | predicho | texto |
| ---: | --- | --- | --- |
| 201 | negativo | positivo | El pedido llego tarde y con detalles pendientes |
| 206 | negativo | neutral | El producto fallo en la primera prueba |
| 208 | negativo | neutral | La entrega llego incompleta |
| 211 | negativo | positivo | La atencion fue poco clara |
| 218 | negativo | positivo | La plataforma no permitio terminar |

### Clase `neutral`

- Falsos positivos: `34`
- Falsos negativos: `5`

Falsos positivos representativos:

| id | real | predicho | texto |
| ---: | --- | --- | --- |
| 2 | positivo | neutral | La entrega demoro un poco y aun asi llego completa |
| 8 | positivo | neutral | La pagina cargo bien y pude terminar el tramite |
| 26 | positivo | neutral | La consulta quedo resuelta sin insistir |
| 36 | positivo | neutral | La factura quedo clara y disponible |
| 44 | positivo | neutral | La solicitud avanzo sin tropiezos |

Falsos negativos representativos:

| id | real | predicho | texto |
| ---: | --- | --- | --- |
| 151 | neutral | positivo | El pedido fue marcado como recibido |
| 159 | neutral | positivo | La plataforma muestra opciones disponibles |
| 184 | neutral | positivo | El pedido fue actualizado |
| 190 | neutral | negativo | El estado no ha cambiado |
| 198 | neutral | negativo | El caso sigue abierto |

### Clase `positivo`

- Falsos positivos: `35`
- Falsos negativos: `24`

Falsos positivos representativos:

| id | real | predicho | texto |
| ---: | --- | --- | --- |
| 151 | neutral | positivo | El pedido fue marcado como recibido |
| 159 | neutral | positivo | La plataforma muestra opciones disponibles |
| 184 | neutral | positivo | El pedido fue actualizado |
| 201 | negativo | positivo | El pedido llego tarde y con detalles pendientes |
| 211 | negativo | positivo | La atencion fue poco clara |

Falsos negativos representativos:

| id | real | predicho | texto |
| ---: | --- | --- | --- |
| 2 | positivo | neutral | La entrega demoro un poco y aun asi llego completa |
| 8 | positivo | neutral | La pagina cargo bien y pude terminar el tramite |
| 17 | positivo | negativo | La solucion no fue complicada y funciono |
| 18 | positivo | negativo | El proceso fue mas claro que otras veces |
| 26 | positivo | neutral | La consulta quedo resuelta sin insistir |


## Top N-Grams En Errores

### Error `negativo -> neutral`

| n-gram | frecuencia |
| --- | ---: |
| la | 10 |
| el | 7 |
| fue | 4 |
| en | 3 |
| quedo | 3 |
| consulta | 2 |
| consulta quedo | 2 |
| el producto | 2 |
| el reporte | 2 |
| entrega | 2 |
| estaba | 2 |
| incompleta | 2 |
| informacion | 2 |
| la consulta | 2 |
| la entrega | 2 |
### Error `negativo -> positivo`

| n-gram | frecuencia |
| --- | ---: |
| la | 22 |
| el | 15 |
| fue | 11 |
| no | 10 |
| lo | 4 |
| de | 3 |
| el producto | 3 |
| el servicio | 3 |
| experiencia | 3 |
| la experiencia | 3 |
| la plataforma | 3 |
| plataforma | 3 |
| producto | 3 |
| servicio | 3 |
| atencion | 2 |
### Error `neutral -> negativo`

| n-gram | frecuencia |
| --- | ---: |
| el | 2 |
| abierto | 1 |
| cambiado | 1 |
| caso | 1 |
| caso sigue | 1 |
| el caso | 1 |
| el estado | 1 |
| estado | 1 |
| estado no | 1 |
| ha | 1 |
| ha cambiado | 1 |
| no | 1 |
| no ha | 1 |
| sigue | 1 |
| sigue abierto | 1 |
### Error `neutral -> positivo`

| n-gram | frecuencia |
| --- | ---: |
| el | 2 |
| el pedido | 2 |
| fue | 2 |
| pedido | 2 |
| pedido fue | 2 |
| actualizado | 1 |
| como | 1 |
| como recibido | 1 |
| disponibles | 1 |
| fue actualizado | 1 |
| fue marcado | 1 |
| la | 1 |
| la plataforma | 1 |
| marcado | 1 |
| marcado como | 1 |
### Error `positivo -> negativo`

| n-gram | frecuencia |
| --- | ---: |
| el | 3 |
| fue | 3 |
| no | 3 |
| la | 2 |
| no fue | 2 |
| claridad | 1 |
| claro | 1 |
| claro que | 1 |
| complicada | 1 |
| complicada funciono | 1 |
| con | 1 |
| con claridad | 1 |
| el proceso | 1 |
| el soporte | 1 |
| el tramite | 1 |
### Error `positivo -> neutral`

| n-gram | frecuencia |
| --- | ---: |
| la | 13 |
| el | 9 |
| fue | 5 |
| entrega | 4 |
| la entrega | 4 |
| se | 4 |
| bien | 3 |
| la solicitud | 3 |
| quedo | 3 |
| solicitud | 3 |
| completa | 2 |
| el producto | 2 |
| el sistema | 2 |
| el tramite | 2 |
| entrega fue | 2 |

## Lectura Tecnica

Los errores se concentran en frases con negaciones, expresiones mixtas y comentarios positivos o negativos con lenguaje menos directo. Estos patrones deben alimentar el dataset augmented para mejorar generalizacion.
