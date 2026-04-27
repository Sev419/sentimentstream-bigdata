# Checklist Final para Dashboard Power BI

## Proposito

Esta lista sirve para validar el dashboard real de SentimentStream una vez construido en Power BI.

No afirma que el dashboard exista todavia. Solo deja una guia de verificacion final.

## Prerrequisitos Antes De Abrir Power BI

- [ ] Docker Desktop esta activo.
- [ ] MongoDB responde en `mongodb://mongo:27017` o en el entorno local definido.
- [ ] Flask API esta levantada y responde en `http://127.0.0.1:8000`.
- [ ] Los endpoints de la API devuelven datos reales.
- [ ] Existe acceso a la red local para consumir la API desde Power BI Desktop.
- [ ] El archivo `.pbix` esta definido en una ubicacion conocida.

## Endpoints Que Deben Responder

- [ ] `GET http://127.0.0.1:8000/sentiments`
- [ ] `GET http://127.0.0.1:8000/stats`
- [ ] `GET http://127.0.0.1:8000/predictions/latest`

## Visualizaciones Minimas Obligatorias

- [ ] Tarjeta con el total de registros.
- [ ] Grafico por `predicted_label`.
- [ ] Tabla de predicciones recientes.

## Campos Esperados

### Para `GET /sentiments`

- [ ] `created_at`
- [ ] `event_time`
- [ ] `id`
- [ ] `microbatch_id`
- [ ] `microbatch_source_file`
- [ ] `predicted_label`
- [ ] `prediction`
- [ ] `sentimiento`
- [ ] `source`
- [ ] `texto`
- [ ] `texto_preprocesado`

### Para `GET /stats`

- [ ] `total`
- [ ] `by_predicted_label`

### Para `GET /predictions/latest`

- [ ] `item`
- [ ] `created_at`
- [ ] `event_time`
- [ ] `id`
- [ ] `microbatch_id`
- [ ] `microbatch_source_file`
- [ ] `predicted_label`
- [ ] `prediction`
- [ ] `sentimiento`
- [ ] `source`
- [ ] `texto`
- [ ] `texto_preprocesado`

## Ubicacion Esperada Del Archivo `.pbix`

- [ ] La ruta del archivo `.pbix` esta definida y documentada.
- [ ] La ubicacion recomendada para dejar evidencia del archivo final es una subcarpeta del repositorio o una ruta acordada para la entrega.

## Ubicacion Esperada De Capturas

- [ ] `dashboard/exports/`
- [ ] Captura de la tarjeta total.
- [ ] Captura del grafico por `predicted_label`.
- [ ] Captura de la tabla de predicciones recientes.
- [ ] Captura de la conexion a la API.
- [ ] Captura del ultimo refresh exitoso.

## Criterios Para Considerar El Dashboard Terminado

- [ ] Consume la API Flask, no Mongo directamente.
- [ ] Muestra datos reales obtenidos desde `GET /sentiments`.
- [ ] Muestra estadisticas reales obtenidas desde `GET /stats`.
- [ ] Muestra informacion reciente obtenida desde `GET /predictions/latest`.
- [ ] Las visualizaciones se ven completas y coherentes.
- [ ] El archivo `.pbix` esta guardado.
- [ ] Las capturas de evidencia estan guardadas.
- [ ] La documentacion final referencia la fuente de datos correcta.

## Errores Comunes Y Como Diagnosticarlos

- [ ] La API no responde: verificar que Flask este corriendo en `http://127.0.0.1:8000`.
- [ ] Power BI no carga los datos: verificar la URL del endpoint y la conexion `Web`.
- [ ] `GET /stats` aparece anidado: transformar `by_predicted_label` en Power Query.
- [ ] La tabla sale vacia: confirmar que Mongo tiene documentos reales.
- [ ] Las credenciales o la red fallan: verificar que Power BI tenga acceso a localhost.
- [ ] El dashboard muestra datos viejos: forzar refresh y volver a consultar la API.

## Confirmacion De Fuente

- [ ] Power BI consume la API Flask.
- [ ] Power BI no consume Mongo directamente.
- [ ] Mongo solo actua como persistencia intermedia.

