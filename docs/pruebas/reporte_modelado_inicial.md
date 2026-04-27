# Reporte de modelado inicial con PySpark

## Fase

Fase 5 - Primer modelado con PySpark.

## Dataset utilizado

`C:\Users\User\Desktop\Big DAta\sentimentstream\data\processed\dataset_modelado_sin_duplicados.csv`

Se uso la version sin duplicados porque en la Fase 4 se identifico una alta cantidad de repeticiones completas. Esta decision reduce el riesgo de que ejemplos identicos inflen artificialmente las metricas iniciales.

## Columnas utilizadas

- Texto principal: `texto_preprocesado`
- Etiqueta: `sentimiento`

## Configuracion Python para PySpark

- Python del driver: `C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe`
- PYSPARK_PYTHON: `C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe`
- PYSPARK_DRIVER_PYTHON: `C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe`

Estas variables se fijan antes de crear SparkSession para evitar `PYTHON_VERSION_MISMATCH` entre driver y workers en Windows.

## Etapas del pipeline

1. Carga del CSV con Spark.
2. Validacion de columnas esperadas.
3. Indexacion de la etiqueta `sentimiento`.
4. Tokenizacion de `texto_preprocesado`.
5. Eliminacion de stopwords.
6. Vectorizacion con HashingTF.
7. Aplicacion de IDF.
8. Entrenamiento de NaiveBayes.
9. Evaluacion con metricas basicas.

## Particion usada

- Estrategia: particion estratificada simple por clase.
- Proporcion aproximada: 70% entrenamiento y 30% prueba.
- Filas de entrenamiento: 21.
- Filas de prueba: 9.

## Metricas obtenidas

- Accuracy: 0.111111.
- F1 ponderado: 0.066667.
- Precision ponderada: 0.047619.
- Recall ponderado: 0.111111.

## Limitaciones

- El dataset sin duplicados tiene solo 30 filas.
- La evaluacion es inicial y no debe interpretarse como resultado final.
- No se realizo tuning de hiperparametros.
- No se construyo pipeline final de produccion.
- No se comparo contra el dataset con duplicados.
- En Windows, las predicciones se escriben desde Python despues de seleccionarlas con Spark para evitar la dependencia local de Hadoop `winutils.exe`.

## Confirmacion de alcance

- No se uso MongoDB.
- No se creo API.
- No se uso Docker.
- No se creo Jenkinsfile.
- No se creo dashboard.
- No se realizo despliegue.
