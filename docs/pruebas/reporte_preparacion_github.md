# Reporte De Preparacion Para GitHub

## Objetivo

Preparar el proyecto SentimentStream para publicarlo en GitHub de forma limpia, segura y profesional.

Esta revision se limita a estructura, `.gitignore` y documentacion. No se ejecutaron comandos de publicacion, no se hizo commit y no se subio contenido a GitHub.

## Estado General Del Proyecto

El proyecto contiene componentes reproducibles y documentables:

- Spark en Docker.
- MongoDB en Docker.
- API Flask.
- Power BI.
- Jenkinsfile.
- Datasets CSV pequenos.
- Reportes en `docs/pruebas`.
- Evidencias en `docs/evidencias`.
- Capturas del dashboard en `dashboard/exports`.
- Archivo Power BI en `dashboard/powerbi`.

## Riesgo Git Detectado

Al consultar el repositorio Git desde la carpeta del proyecto, el directorio raiz detectado fue:

```text
C:/Users/User
```

Esto significa que Git esta tomando como raiz una carpeta superior al proyecto `sentimentstream`.

Riesgo:

- `git status` puede mostrar archivos personales o proyectos externos.
- `git add .` ejecutado desde una ruta incorrecta podria intentar incluir contenido ajeno al proyecto.

Recomendacion:

- Publicar desde una copia limpia o inicializar Git dentro de `C:\Users\User\Desktop\Big DAta\sentimentstream`.
- Antes de hacer `git add .`, confirmar que `git status` solo muestra archivos del proyecto SentimentStream.

## Estado Del `.gitignore`

El archivo `.gitignore` fue actualizado para:

- Mantener fuera secretos y archivos locales.
- Excluir caches de Python y pruebas.
- Excluir entornos virtuales.
- Excluir logs, temporales y backups.
- Excluir bases de datos locales y dumps.
- Excluir artefactos generados pesados.
- Excluir outputs generados de streaming.
- Permitir datasets CSV pequenos necesarios para reproducibilidad.
- Permitir capturas livianas del dashboard.
- Permitir el archivo `.pbix` si su tamano sigue siendo razonable.

Reglas relevantes:

```gitignore
.env
.env.*
!.env.example
__pycache__/
*.py[cod]
.venv/
venv/
*.log
pytest-cache-files-*/
data/streaming/processed/*
!data/streaming/processed/.gitkeep
*.pkl
*.joblib
*.parquet
*.orc
*.avro
~$*.pbix
*.tmp.pbix
```

## Archivos Recomendados Para Subir

Subir estos elementos porque permiten revisar, ejecutar o auditar el proyecto:

- `README.md`
- `requirements.txt`
- `.env.example`
- `.gitignore`
- `docker-compose.yml`
- `Dockerfiles` dentro de `docker/`
- `Jenkinsfile`
- `infra/jenkins/Jenkinsfile`
- Codigo fuente de Spark:
  - `spark/`
  - `spark_processing/`
- Codigo fuente de API Flask:
  - `api/`
  - `api_flask/`
- Codigo de acceso a MongoDB:
  - `database/`
- Pruebas:
  - `tests/`
- Reportes y guias:
  - `docs/pruebas/`
  - `docs/evidencias/`
  - `docs/arquitectura/`
- Mocks JSON:
  - `dashboard/mock_responses/`
- Capturas livianas del dashboard:
  - `dashboard/exports/card_total.png`
  - `dashboard/exports/chart_distribution.png`
  - `dashboard/exports/dashboard_overview.png`
  - `dashboard/exports/table_predictions.png`
- Datasets pequenos necesarios para reproducibilidad:
  - `data/raw/*.csv`
  - `data/processed/*.csv`
  - `data/streaming/input/*.csv`
- Archivo Power BI si se mantiene pequeno:
  - `dashboard/powerbi/sentimientos.pbix`

## Archivos Recomendados Para Excluir

No subir estos elementos:

- `.env`
- Credenciales reales.
- Contrasenas.
- Tokens.
- Llaves privadas o certificados.
- Carpetas `__pycache__/`.
- Archivos `*.pyc`.
- `.venv/`, `venv/` o `env/`.
- Caches de pruebas:
  - `.pytest_cache/`
  - `pytest-cache-files-*/`
- Logs:
  - `*.log`
- Temporales:
  - `*.tmp`
  - `*.temp`
  - `*.bak`
- Imagenes Docker exportadas.
- Volumenes locales de Docker.
- Bases de datos locales:
  - `*.db`
  - `*.sqlite`
  - `*.sqlite3`
- Dumps de MongoDB:
  - `*.dump`
  - `*.archive`
- Outputs generados pesados.
- Modelos entrenados o serializados:
  - `*.pkl`
  - `*.joblib`
- Formatos analiticos pesados generados:
  - `*.parquet`
  - `*.orc`
  - `*.avro`
- Outputs generados en:
  - `data/streaming/processed/`
  - `spark/models/`
  - `spark/outputs/`

## Revision De Datasets

Tamano real detectado:

| Ubicacion | Archivos | Tamano aproximado |
| --- | ---: | ---: |
| `data/raw` | 2 | 19 KB |
| `data/processed` | 5 | 96 KB |
| `data/streaming/input` | 4 | 8 KB |
| `data/streaming/processed` | 4 | 12 KB |

Total CSV detectado:

```text
127041 bytes, aproximadamente 124 KB
```

Recomendacion:

- Los datasets son pequenos y pueden subirse si no contienen datos sensibles.
- Mantener `data/raw`, `data/processed` y `data/streaming/input` para reproducibilidad.
- No subir `data/streaming/processed` porque contiene salidas generadas y logs de ejecucion.
- Si luego se reemplaza el dataset por uno grande o sensible, mover una muestra anonima a `data/samples` y documentar como obtener el dataset completo.

Riesgo pendiente:

- No se puede certificar sensibilidad de datos solo por tamano. Antes de publicar, revisar columnas y textos para confirmar que no contengan informacion personal, privada o confidencial.

## Revision De Power BI

Archivo `.pbix` detectado:

```text
dashboard/powerbi/sentimientos.pbix
```

Tamano real:

```text
61311 bytes, aproximadamente 60 KB
```

Recomendacion:

- El archivo es liviano y puede subirse como evidencia del dashboard.
- Si en el futuro crece demasiado o contiene datos sensibles embebidos, excluir el `.pbix` y conservar solo capturas en `dashboard/exports`.

Observacion:

- No se encontro el archivo `dashboard/powerbi/sentimentstream_dashboard.pbix` en la revision local.
- El archivo Power BI presente actualmente es `dashboard/powerbi/sentimientos.pbix`.

## Revision De Capturas

Capturas detectadas:

| Archivo | Tamano aproximado |
| --- | ---: |
| `dashboard/exports/card_total.png` | 6 KB |
| `dashboard/exports/chart_distribution.png` | 11 KB |
| `dashboard/exports/dashboard_overview.png` | 81 KB |
| `dashboard/exports/table_predictions.png` | 60 KB |

Tamano total de capturas:

```text
158420 bytes, aproximadamente 155 KB
```

Recomendacion:

- Las capturas son livianas y pueden subirse como evidencia visual.

## Riesgos Detectados

- La raiz Git actual aparece como `C:/Users/User`, no como la carpeta `sentimentstream`.
- Existen carpetas `pytest-cache-files-*` con acceso denegado; deben quedar ignoradas.
- Existen carpetas `__pycache__`; ya estan ignoradas.
- `.env.example` contiene variables de ejemplo y no debe contener secretos reales.
- Se detecto `TWILIO_AUTH_TOKEN=` vacio en `.env.example`; es aceptable como plantilla, pero nunca debe completarse con un token real.
- El dataset es pequeno, pero debe revisarse manualmente por sensibilidad antes de publicar.
- El `.pbix` es pequeno, pero debe revisarse si contiene datos embebidos sensibles.

## Comandos Sugeridos Para Inicializar Git

Estos comandos son sugeridos. No fueron ejecutados durante esta auditoria.

Ejecutarlos solo desde la carpeta raiz del proyecto:

```powershell
cd "C:\Users\User\Desktop\Big DAta\sentimentstream"
git init
git status
```

Antes de continuar, validar que `git status` solo muestre archivos de SentimentStream.

## Comandos Sugeridos Para Subir A GitHub

Estos comandos son sugeridos. No fueron ejecutados durante esta auditoria.

```bash
git add .
git commit -m "Initial commit - SentimentStream Big Data pipeline"
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

Reemplazar:

```text
URL_DEL_REPOSITORIO
```

por la URL real del repositorio GitHub.

## Checklist Antes De Publicar

- [ ] Confirmar que no existe `.env` con secretos reales.
- [ ] Confirmar que `.env.example` solo contiene valores de ejemplo.
- [ ] Confirmar que `git status` no muestra archivos fuera de SentimentStream.
- [ ] Revisar el dataset por datos personales o sensibles.
- [ ] Confirmar si se publicara `dashboard/powerbi/sentimientos.pbix`.
- [ ] Confirmar que las capturas en `dashboard/exports` son las finales.
- [ ] Verificar que no se agreguen caches ni logs.
- [ ] Revisar que `data/streaming/processed` no se agregue al commit.

## Conclusion

El proyecto esta cerca de estar listo para publicarse en GitHub. La recomendacion es subir codigo, Dockerfiles, Compose, Jenkinsfile, documentacion, mocks, capturas livianas, datasets pequenos de reproducibilidad y el `.pbix` actual por su bajo peso.

No se recomienda subir secretos, entornos virtuales, caches, logs, bases locales, dumps, outputs generados pesados ni datos sensibles.
