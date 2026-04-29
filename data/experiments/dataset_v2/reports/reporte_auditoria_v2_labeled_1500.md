# Resultado Auditoria Dataset V2

## Resumen

- Archivo auditado: `C:\Users\User\Desktop\Big DAta\sentimentstream\data\experiments\dataset_v2\labeled\dataset_sentimientos_v2_labeled_1500.csv`
- Existe CSV: `True`
- Fecha UTC de auditoria: `2026-04-27T05:33:20.890896+00:00`
- Estado: `apto para revision experimental`

## Columnas

- Columnas obligatorias: `id, texto, sentimiento, fuente, version`
- Columnas encontradas: `id, texto, sentimiento, fuente, version`
- Columnas faltantes: `ninguna`
- Columnas extra: `ninguna`

## Validacion General

| Criterio | Resultado |
| --- | ---: |
| Total registros | 1500 |
| Etiquetas invalidas | 0 |
| Textos nulos | 0 |
| Textos vacios | 0 |
| Duplicados por texto | 0 |
| Duplicados completos | 0 |
| Posibles datos sensibles | 0 |

## Distribucion Por Sentimiento

| Clase | Cantidad | Porcentaje |
| --- | ---: | ---: |
| positivo | 500 | 33.33% |
| neutral | 500 | 33.33% |
| negativo | 500 | 33.33% |

## Longitud Del Texto

| Metrica | Valor |
| --- | ---: |
| Minima | 25 |
| Media | 37.45 |
| Maxima | 48 |

## Problemas Encontrados

- Etiquetas invalidas: `0`
- Textos nulos: `0`
- Textos vacios: `0`
- Duplicados por texto: `0`
- Duplicados completos: `0`
- Posibles correos o telefonos en texto: `0`

## Nota De Aislamiento

Esta auditoria solo lee archivos dentro de `data/experiments/dataset_v2/` y solo escribe resultados en `data/experiments/dataset_v2/reports/`.

No entrena modelos, no modifica datos productivos, no conecta MongoDB y no toca el pipeline estable.
