# Reporte de normalizacion estructural del dataset

## Fase

Fase 2.5 - Normalizacion estructural del dataset.

## Archivo de entrada usado

`data/raw/dataset_sentimientos_500.csv`

## Columnas originales detectadas

- `texto`
- `etiqueta`

## Columnas finales generadas

1. `id`
2. `texto`
3. `sentimiento`

## Numero de registros

- Dataset original: 502 registros.
- Dataset normalizado: 502 registros.

## Decisiones aplicadas

- Se genero `id` como identificador tecnico secuencial desde 1.
- Se conservo `texto` sin limpieza avanzada.
- Se renombro `etiqueta` a `sentimiento`.
- Se conservaron los valores originales de las etiquetas.

## Confirmaciones

- Se conservaron los duplicados del dataset original.
- No se creo columna `fecha`.
- No se hizo limpieza avanzada de texto.
- No se realizo modelado.
- No se conecto MongoDB.
- No se creo API, Docker, Jenkins ni dashboard.
