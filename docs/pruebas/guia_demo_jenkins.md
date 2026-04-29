# Guia Demo Jenkins

## Objetivo

Preparar la demostracion de Jenkins para el video final de SentimentStream, mostrando el pipeline como validacion local demostrativa del flujo principal.

## Archivo Del Pipeline

El Jenkinsfile recomendado para mostrar es:

```text
infra/jenkins/Jenkinsfile
```

Este pipeline valida:

- Docker disponible.
- MongoDB levantado con Docker Compose.
- Spark job ejecutado sobre un micro-batch.
- MongoDB con predicciones persistidas.
- API Flask respondiendo a `/stats`.

## Aclaracion Importante

Este Jenkinsfile es demostrativo local. No representa un despliegue productivo, no usa Kubernetes y no publica en nube.

Para ejecutarlo correctamente, Jenkins debe tener acceso al Docker host de la maquina.

## Como Abrir Jenkins

1. Abrir Jenkins en el navegador.
2. Iniciar sesion si Jenkins lo solicita.
3. Entrar al job configurado para SentimentStream.
4. Verificar que el job use el repositorio del proyecto o que apunte al workspace local.
5. Confirmar que la ruta del Jenkinsfile sea:

```text
infra/jenkins/Jenkinsfile
```

## Como Mostrar El Pipeline

Durante el video, abrir el Jenkinsfile y explicar sus etapas:

1. `Setup`
   - ejecuta `docker version`.
2. `Levantar Mongo`
   - ejecuta `docker compose up -d mongo`.
3. `Ejecutar Spark job`
   - procesa `data/streaming/input/microbatch_001.csv`.
4. `Validar Mongo`
   - cuenta documentos en `sentimentstream_db.predictions`.
5. `Validar API`
   - levanta la API y consulta `http://127.0.0.1:8000/stats`.

## Como Ejecutar Build Now

1. En el job de Jenkins, hacer clic en `Build Now`.
2. Esperar a que aparezca una nueva ejecucion en el historial.
3. Abrir la ejecucion.
4. Entrar a `Console Output`.
5. Mostrar las etapas principales y el resultado final.

## Que Mostrar En Consola

Buscar evidencias como:

- salida de `docker version`
- inicio de MongoDB
- ejecucion del Spark job
- conteo mayor que cero en MongoDB
- respuesta exitosa de `/stats`
- estado final del build

No es necesario leer toda la consola. Mostrar solo las partes que prueban el flujo.

## Que Explicar Durante El Video

Guion breve:

```text
Jenkins se usa como una validacion automatizada demostrativa.
El pipeline confirma que Docker funciona, levanta MongoDB, ejecuta el job Spark, valida que Mongo tenga predicciones y comprueba que la API Flask responda.
No es un pipeline productivo en nube; es una integracion local para evidenciar automatizacion.
```

## Si Jenkins No Ejecuta Completo

Si hay problemas de permisos con Docker, mostrar:

- el archivo `infra/jenkins/Jenkinsfile`
- el reporte `docs/pruebas/reporte_jenkins_pipeline.md`
- la explicacion de que Jenkins requiere acceso al Docker host

No afirmar que el pipeline se ejecuto si no existe evidencia real.

## Restricciones

- No modificar Docker Compose para la demo.
- No modificar Spark.
- No modificar Flask.
- No modificar MongoDB.
- No crear despliegue en nube.
- No presentar Jenkins como produccion.
