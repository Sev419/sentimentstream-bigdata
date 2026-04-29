# Experimentos Spark Y ML

## Proposito Actual

Esta carpeta contiene scripts experimentales para auditar datasets v2, generar versiones controladas, entrenar modelos NLP y evaluar resultados externos o realistic.

No forma parte del pipeline productivo de SentimentStream.

El pipeline estable sigue estando en:

```text
spark_processing/
```

## Advertencia

Ningun script de esta carpeta debe reemplazar, modificar o conectarse automaticamente con:

- `spark_processing/`
- `api_flask/`
- `database/`
- MongoDB
- Docker
- Jenkins
- Power BI
- datasets productivos en `data/raw/`, `data/processed/` o `data/streaming/`

Las salidas experimentales deben permanecer en:

```text
data/experiments/dataset_v2/reports/
```

## Scripts De Auditoria

- `auditar_dataset_v2.py`: valida estructura, columnas, distribucion por clase, duplicados, nulos, textos vacios, longitudes y posibles datos sensibles.

## Scripts De Generacion De Datasets

- `generar_dataset_v2_labeled_1500.py`
- `generar_dataset_v2_curated_1500.py`
- `generar_dataset_v2_realistic_validation.py`
- `generar_dataset_v2_augmented_1800.py`
- `generar_dataset_v2_focused_negative_1950.py`

Estos scripts pertenecen a la fase experimental y no deben alimentar produccion.

## Scripts De Entrenamiento

- `train_model_v2_experimental.py`
- `train_model_v2_improved.py`
- `train_model_v2_1500_experimental.py`
- `train_model_v2_curated_1500.py`
- `train_model_v2_augmented_1800.py`
- `train_model_v2_focused_negative_1950.py`

Modelos evaluados en la fase experimental:

- Naive Bayes
- Logistic Regression
- Linear SVM en la version improved, si esta disponible por dependencias

## Scripts De Evaluacion

- `evaluate_model_v2_1500_external.py`
- `evaluate_model_v2_curated_external.py`
- `evaluate_model_v2_curated_realistic.py`
- `evaluate_model_v2_augmented_realistic.py`
- `evaluate_model_v2_focused_negative_realistic.py`

Estas evaluaciones comparan modelos entrenados con datasets experimentales contra datasets externos o realistic sin mezclar train/test con la validacion.

## Scripts De Analisis De Errores

- `analizar_errores_realistic.py`
- `analizar_errores_negativos_augmented.py`

Su proposito es identificar confusiones por clase, especialmente errores sobre textos negativos ambiguos.

## Resultado Consolidado

La mejor referencia experimental actual es:

```text
v2_augmented_1800
```

Resultado realistic registrado:

```text
F1 realistic: 0.792533
Recall negativo: 0.66
Recall neutral: 0.96
Recall positivo: 0.77
```

La version `v2_focused_negative_1950` no se adopta porque no mejora el resultado realistic:

```text
F1 realistic: 0.781374
Recall negativo: 0.64
```

## Decision Tecnica

No se integra ningun modelo experimental al pipeline estable.

Motivo:

- aunque `v2_augmented_1800` mejora el F1 general, el recall negativo sigue bajo para una integracion controlada.

## Reglas De Uso

- Ejecutar estos scripts solo como experimentos aislados.
- Guardar metricas y reportes en `data/experiments/dataset_v2/reports/`.
- No escribir resultados en `data/processed/`.
- No conectar con MongoDB.
- No modificar Docker Compose.
- No modificar Jenkins.
- No modificar Power BI.
- Documentar cualquier nueva iteracion antes de proponer integracion.

## Documentacion Relacionada

```text
docs/pruebas/reporte_consolidado_mejora_dataset_v2.md
docs/pruebas/guia_etiquetado_dataset_v2.md
```
