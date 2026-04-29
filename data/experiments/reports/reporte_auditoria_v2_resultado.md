# Resultado Auditoria Dataset V2

## Resumen

- Archivo auditado: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\raw\dataset_sentimientos_v2_template.csv`
- Existe CSV: `True`
- Fecha UTC de auditoria: `2026-04-27T05:03:53.774060+00:00`
- Estado: `apto para revision experimental`

## Columnas

- Columnas obligatorias: `id, texto, sentimiento, fuente, version`
- Columnas encontradas: `id, texto, sentimiento, fuente, version`
- Columnas faltantes: `ninguna`
- Columnas extra: `ninguna`

## Validacion General

| Criterio | Resultado |
| --- | ---: |
| Total registros | 10 |
| Etiquetas invalidas | 0 |
| Textos nulos | 0 |
| Textos vacios | 0 |
| Duplicados por texto | 0 |
| Duplicados completos | 0 |
| Posibles datos sensibles | 0 |

## Distribucion Por Sentimiento

| Clase | Cantidad | Porcentaje |
| --- | ---: | ---: |
| positivo | 3 | 30.00% |
| neutral | 4 | 40.00% |
| negativo | 3 | 30.00% |

## Longitud Del Texto

| Metrica | Valor |
| --- | ---: |
| Minima | 17 |
| Media | 29.1 |
| Maxima | 40 |

## Problemas Encontrados

- Etiquetas invalidas: `0`
- Textos nulos: `0`
- Textos vacios: `0`
- Duplicados por texto: `0`
- Duplicados completos: `0`
- Posibles correos o telefonos en texto: `0`

## Nota De Aislamiento

Esta auditoria solo lee `data/experiments/dataset_v2/raw/` y solo escribe resultados en `data/experiments/dataset_v2/reports/`.

No entrena modelos, no modifica datos productivos, no conecta MongoDB y no toca el pipeline estable.
