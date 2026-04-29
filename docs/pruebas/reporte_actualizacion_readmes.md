# Reporte Actualizacion READMEs

## Objetivo

Registrar la revision y actualizacion de los archivos `README.md` del proyecto SentimentStream antes del cierre final de entrega.

## Alcance

La revision se limito a documentacion. No se modifico codigo, datasets, Docker, Jenkins, Power BI ni la logica del pipeline productivo.

## READMEs Revisados

| Archivo | Estado encontrado | Accion |
| --- | --- | --- |
| `README.md` | Actualizado en lo general, pero podia reflejar mejor la fase experimental y guias finales | Modificado |
| `data/experiments/dataset_v2/README.md` | Desactualizado; describia solo una zona inicial experimental | Modificado |
| `spark/experiments/README.md` | Desactualizado; hablaba de experimentos futuros aunque ya existen scripts y resultados | Modificado |
| `dashboard/powerbi/README.md` | Desactualizado; describia visualizaciones sugeridas y tenia texto con caracteres corruptos | Modificado |

## Inconsistencias Encontradas

- `data/experiments/dataset_v2/README.md` no mencionaba los datasets v2 ya creados.
- `data/experiments/dataset_v2/README.md` no documentaba la mejor version experimental actual.
- `spark/experiments/README.md` indicaba que los modelos eran futuros, aunque ya existen scripts de auditoria, entrenamiento, evaluacion y analisis de errores.
- `dashboard/powerbi/README.md` no reflejaba el archivo real `dashboard/powerbi/sentimientos.pbix`.
- `dashboard/powerbi/README.md` no incluia las visualizaciones actuales ni las capturas finales.

## Cambios Realizados

### README raiz

Se agregaron referencias a:

- `reporte_consolidado_mejora_dataset_v2.md`
- `reporte_validacion_documental_final.md`
- `guia_visualizacion_temporal_powerbi.md`
- `guia_demo_jenkins.md`
- `guion_video_final.md`

Tambien se amplio la seccion experimental para indicar que:

- `data/experiments/dataset_v2/` contiene datasets y reportes experimentales.
- `spark/experiments/` contiene scripts experimentales.
- la mejor referencia actual es `v2_augmented_1800`.
- no se integra ningun modelo experimental al pipeline estable.

### data/experiments/dataset_v2/README.md

Se actualizo para documentar:

- proposito actual de la carpeta
- estructura experimental
- datasets creados
- reportes generados
- mejor version experimental: `v2_augmented_1800`
- F1 realistic: `0.792533`
- razon para no integrar: recall negativo bajo
- reglas de aislamiento frente al pipeline productivo

### spark/experiments/README.md

Se actualizo para documentar:

- scripts de auditoria
- scripts de generacion de datasets
- scripts de entrenamiento
- scripts de evaluacion externa y realistic
- scripts de analisis de errores
- decision tecnica de no integrar modelos experimentales

### dashboard/powerbi/README.md

Se actualizo para documentar:

- archivo real: `dashboard/powerbi/sentimientos.pbix`
- fuentes API usadas desde Power BI
- visualizaciones actuales
- capturas finales en `dashboard/exports/`
- restricciones de uso

## Confirmacion De No Afectacion Productiva

No se modifico:

- codigo fuente
- datasets productivos
- `spark_processing/`
- `api_flask/`
- `database/`
- `docker/`
- `docker-compose.yml`
- `Jenkinsfile`
- MongoDB
- Jenkins
- Power BI
- logica del pipeline productivo

## Resultado

Los README principales y secundarios quedan alineados con el estado actual del proyecto, la fase experimental v2 y la evidencia final para entrega academica.
