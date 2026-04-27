# Guia De Correccion Power Query Para `/stats`

## Proposito

Esta guia documenta como corregir la preparacion del endpoint `GET /stats` en Power BI cuando el campo `by_predicted_label` queda expandido en formato ancho.

No indica que el dashboard ya este terminado. Solo corrige la transformacion necesaria para poder construir el grafico por sentimiento predicho.

## Contexto

La API Flask ya responde en estos endpoints:

- `http://127.0.0.1:8000/stats`
- `http://127.0.0.1:8000/sentiments`
- `http://127.0.0.1:8000/predictions/latest`

En Power Query, al consumir `/stats`, el campo `by_predicted_label` puede quedar expandido asi:

| by_predicted_label.negativo | by_predicted_label.neutral | by_predicted_label.positivo | total |
| --- | --- | --- | --- |
| 8 | 8 | 9 | 25 |

Ese formato es ancho. Para un grafico de barras por `predicted_label`, Power BI necesita un formato largo.

## Resultado Esperado

La tabla corregida debe quedar asi:

| predicted_label | cantidad | total |
| --- | ---: | ---: |
| negativo | 8 | 25 |
| neutral | 8 | 25 |
| positivo | 9 | 25 |

## Correccion Paso A Paso En Power Query

1. Abrir Power BI Desktop.
2. Entrar a `Transformar datos` para abrir Power Query.
3. Seleccionar la consulta que consume:

```text
http://127.0.0.1:8000/stats
```

4. Verificar que existan estas columnas:

- `by_predicted_label.negativo`
- `by_predicted_label.neutral`
- `by_predicted_label.positivo`
- `total`

5. Seleccionar al mismo tiempo estas tres columnas:

- `by_predicted_label.negativo`
- `by_predicted_label.neutral`
- `by_predicted_label.positivo`

6. En la cinta superior de Power Query, aplicar:

```text
Transformar > Anular dinamizacion de columnas
```

7. Power Query debe crear dos columnas nuevas:

- `Atributo`
- `Valor`

8. Renombrar la columna `Atributo` como:

```text
predicted_label
```

9. Renombrar la columna `Valor` como:

```text
cantidad
```

10. En la columna `predicted_label`, reemplazar el prefijo:

```text
by_predicted_label.
```

por texto vacio.

Resultado de la limpieza:

- `by_predicted_label.negativo` pasa a `negativo`
- `by_predicted_label.neutral` pasa a `neutral`
- `by_predicted_label.positivo` pasa a `positivo`

11. Definir tipos de datos:

- `predicted_label`: texto
- `cantidad`: numero entero
- `total`: numero entero

12. Revisar que la vista previa quede con tres filas y tres columnas:

- `predicted_label`
- `cantidad`
- `total`

13. Aplicar los cambios con:

```text
Cerrar y aplicar
```

## Validacion De La Correccion

Despues de la transformacion, validar:

- La columna `predicted_label` no conserva el prefijo `by_predicted_label.`
- La columna `cantidad` contiene numeros, no texto.
- La columna `total` contiene numeros, no texto.
- El valor `total` se repite en las tres filas. Esto es esperado porque representa el total global del endpoint `/stats`.
- La tabla tiene una fila por cada sentimiento predicho.

## Como Continuar Despues

Una vez corregida la consulta de `/stats`, continuar con estas visualizaciones:

1. Crear una tarjeta con `total`.
   - Fuente: consulta de `/stats`.
   - Campo: `total`.
   - Uso: mostrar el total de registros procesados.

2. Crear un grafico de barras por sentimiento predicho.
   - Fuente: consulta de `/stats`.
   - Eje: `predicted_label`.
   - Valores: `cantidad`.
   - Uso: mostrar la distribucion de predicciones.

3. Conectar el endpoint `/sentiments`.
   - URL: `http://127.0.0.1:8000/sentiments`.
   - Uso: alimentar el detalle de textos clasificados.

4. Crear una tabla de predicciones recientes.
   - Fuente recomendada: `/sentiments` o `/predictions/latest`, segun el nivel de detalle que se quiera mostrar.
   - Campos recomendados:
     - `created_at`
     - `event_time`
     - `id`
     - `microbatch_id`
     - `predicted_label`
     - `prediction`
     - `sentimiento`
     - `texto`

## Errores Comunes

### `by_predicted_label` Quedo Como Columnas

Si aparecen columnas como `by_predicted_label.negativo`, `by_predicted_label.neutral` y `by_predicted_label.positivo`, la tabla sigue en formato ancho.

Correccion:

- seleccionar esas tres columnas
- aplicar `Anular dinamizacion de columnas`
- renombrar `Atributo` y `Valor`

### No Aparece `Anular Dinamizacion`

Puede ocurrir si no hay columnas seleccionadas o si se esta en una vista que no permite la transformacion.

Correccion:

- entrar a Power Query con `Transformar datos`
- seleccionar exactamente las tres columnas de `by_predicted_label`
- revisar la pestana `Transformar`

### `total` Se Repite En Tres Filas

Esto es normal despues de anular dinamizacion. El endpoint `/stats` entrega un total global y Power Query lo conserva en cada fila generada.

Uso correcto:

- usar `total` para la tarjeta
- usar `cantidad` para el grafico por `predicted_label`

### `cantidad` Aparece Como Texto

Si `cantidad` queda como texto, los graficos pueden ordenar o sumar mal.

Correccion:

- seleccionar la columna `cantidad`
- cambiar el tipo de dato a `Numero entero`

### `predicted_label` Queda Con Prefijo

Si los valores quedan como `by_predicted_label.negativo`, `by_predicted_label.neutral` y `by_predicted_label.positivo`, falta limpiar el texto.

Correccion:

- seleccionar la columna `predicted_label`
- usar `Reemplazar valores`
- buscar `by_predicted_label.`
- reemplazar por vacio

## Restricciones De Esta Correccion

Esta correccion solo modifica la preparacion del endpoint `/stats` dentro de Power BI / Power Query.

No se debe modificar:

- Spark
- MongoDB
- Flask
- Docker
- datasets
- archivos JSON mock
- Jenkins

Tampoco se debe afirmar que el dashboard final ya esta terminado. Esta guia solo deja lista la transformacion necesaria para continuar con el armado del dashboard en Power BI.
