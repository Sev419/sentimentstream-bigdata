# Reporte de Validacion API Flask

## Objetivo

Validar que Flask lea datos reales desde MongoDB despues del procesamiento Spark en Docker.

## Servicio API Usado

- Servicio Compose: `api`
- Archivo de arranque: `api_flask/app.py`
- Contenedor: `sentimentstream-api`

## Estado del Entorno

- Docker: OK
- MongoDB: OK
- Spark en Docker: OK
- MongoDB con documentos reales: OK

## Comandos Ejecutados

```powershell
docker compose up -d api
docker logs --tail 80 sentimentstream-api
Invoke-RestMethod http://127.0.0.1:8000/sentiments
Invoke-RestMethod http://127.0.0.1:8000/stats
Invoke-RestMethod http://127.0.0.1:8000/predictions/latest
docker ps --filter "name=sentimentstream-api"
```

## Endpoints Probados

### `GET /sentiments`

Respuesta real con documentos de Mongo. La salida incluye items con campos como:

- `created_at`
- `event_time`
- `id`
- `microbatch_id`
- `predicted_label`

### `GET /stats`

Respuesta real:

```text
by_predicted_label: negativo=8, neutral=8, positivo=9
total: 25
```

### `GET /predictions/latest`

Respuesta real con el ultimo documento insertado desde Mongo.

## Resultado Real

- MongoDB recibio `25` documentos.
- Flask pudo leer esos documentos.
- Los endpoints principales respondieron correctamente.

## Errores Pendientes

- Ninguno bloqueante para la integracion MongoDB -> Flask.

## Confirmacion

La cadena `Spark Docker -> MongoDB -> Flask API` quedo validada en esta fase.

