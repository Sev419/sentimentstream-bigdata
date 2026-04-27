# Reporte de preparacion para modelado

## Fase

Fase 4 - Preparacion para modelado y estrategia de duplicados.

## Archivo de entrada usado

`data/processed/dataset_sentimientos_preprocesado.csv`

## Columnas detectadas

- `id`
- `texto`
- `texto_preprocesado`
- `sentimiento`

## Criterio exacto de duplicado

Se considero duplicado completo todo registro que repite la misma combinacion de:

1. `texto`
2. `texto_preprocesado`
3. `sentimiento`

La columna `id` no se incluyo en el criterio porque es un identificador tecnico unico por fila. Incluirla impediria detectar repeticiones reales de contenido.

## Resultados

- Filas del dataset de entrada: 502.
- Duplicados completos detectados: 472.
- Registros unicos bajo el criterio definido: 30.
- Filas en dataset con duplicados: 502.
- Filas en dataset sin duplicados: 30.

## Archivos generados

- `data/processed/dataset_modelado_con_duplicados.csv`
- `data/processed/dataset_modelado_sin_duplicados.csv`

## Diferencia entre datasets

### Dataset con duplicados

Conserva todas las filas del dataset preprocesado. Es util para mantener trazabilidad completa del archivo recibido y para evaluar el impacto real de los duplicados en una etapa posterior.

### Dataset sin duplicados

Elimina unicamente duplicados completos bajo el criterio `texto`, `texto_preprocesado`, `sentimiento`, conservando la primera ocurrencia y su `id` original. No altera el texto, el texto preprocesado ni la etiqueta de sentimiento.

## Observaciones metodologicas

- El volumen de duplicados es alto: 472 de 502 filas.
- El dataset sin duplicados queda con 30 registros, distribuidos de forma balanceada entre las clases.
- La deduplicacion reduce ruido por repeticion, pero tambien deja un dataset muy pequeno para entrenamiento robusto.
- No se realizo division train/test porque eso pertenece a una fase posterior de modelado y debe decidirse junto con la estrategia de evaluacion.

## Recomendacion para la siguiente fase

Para una primera fase de modelado academico, se recomienda comparar con cautela ambos enfoques:

- Usar `dataset_modelado_sin_duplicados.csv` como referencia principal para evitar que repeticiones identicas inflen artificialmente el desempeno del modelo.
- Conservar `dataset_modelado_con_duplicados.csv` como respaldo metodologico y para analizar el efecto de la repeticion sobre metricas futuras.

Antes de entrenar, conviene documentar la decision final de dataset y definir una estrategia de evaluacion que evite fuga de informacion entre entrenamiento y prueba.

## Confirmaciones de alcance

- No se entrenaron modelos.
- No se construyo TF-IDF.
- No se creo split train/test.
- No se uso PySpark pipeline final.
- No se conecto MongoDB.
- No se creo API, Docker, Jenkins ni dashboard.
- No se modifico el dataset raw.
