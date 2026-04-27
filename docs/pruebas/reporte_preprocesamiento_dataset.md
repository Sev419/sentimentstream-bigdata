# Reporte de preprocesamiento inicial del dataset

## Fase

Fase 3 - Preprocesamiento inicial del dataset.

## Archivo de entrada usado

`data/processed/dataset_sentimientos_normalizado.csv`

## Columnas detectadas

- `id`
- `texto`
- `sentimiento`

## Archivo de salida generado

`data/processed/dataset_sentimientos_preprocesado.csv`

## Columnas finales generadas

1. `id`
2. `texto`
3. `texto_preprocesado`
4. `sentimiento`

## Reglas de preprocesamiento aplicadas

- Conversion de texto a minusculas.
- Eliminacion de espacios repetidos.
- Eliminacion de espacios al inicio y al final.
- Reemplazo de saltos de linea, retornos de carro y tabulaciones por espacios.
- Remocion de caracteres de control no imprimibles.
- Preservacion del contenido semantico del texto.

## Resultados de validacion

- Filas de entrada: 502.
- Filas de salida: 502.
- Textos modificados por las reglas iniciales: 502.
- Textos preprocesados vacios: 0.
- Duplicados de contenido conservados: 472.
- `id` preservado.
- `texto` original preservado.
- `sentimiento` preservado.

## Transformaciones no aplicadas

- No se eliminaron duplicados.
- No se eliminaron stopwords.
- No se aplico stemming.
- No se aplico lematizacion.
- No se tradujo texto.
- No se entrenaron modelos.
- No se construyo TF-IDF.
- No se uso PySpark.
- No se conecto MongoDB.
- No se creo API, Docker, Jenkins ni dashboard.
- No se modifico el dataset raw.
