# Fase 2.5 - Normalizacion estructural del dataset

## Objetivo

Crear una version estructuralmente normalizada del dataset original sin aplicar limpieza avanzada, deduplicacion, modelado ni transformaciones NLP.

## Archivo de entrada

`data/raw/dataset_sentimientos_500.csv`

Columnas reales detectadas:

- `texto`
- `etiqueta`

## Archivo de salida

`data/processed/dataset_sentimientos_normalizado.csv`

Columnas finales generadas, en orden:

1. `id`
2. `texto`
3. `sentimiento`

## Transformaciones aplicadas

- Se genero `id` como identificador tecnico secuencial desde 1 hasta 502.
- Se preservo `texto` desde la columna original `texto`.
- Se renombro `etiqueta` a `sentimiento`.
- Se conservaron los valores originales de las etiquetas.

## Transformaciones no aplicadas

- No se creo columna `fecha`.
- No se eliminaron duplicados.
- No se balancearon clases.
- No se limpio semanticamente el texto.
- No se modificaron nombres de etiquetas.
- No se altero el archivo original en `data/raw/`.
- No se entrenaron modelos ni se implementaron pipelines, persistencia, API o infraestructura.

## Validacion

- Registros de entrada: 502.
- Registros de salida: 502.
- Columnas de salida: `id`, `texto`, `sentimiento`.
- Duplicados de contenido preservados: 472.
- Textos preservados sin transformacion avanzada.
- Etiquetas preservadas sin recodificacion.
