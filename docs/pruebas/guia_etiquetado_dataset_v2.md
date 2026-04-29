# Guia De Etiquetado Dataset V2

## Proposito

Esta guia define criterios iniciales para etiquetar textos del dataset experimental v2 de SentimentStream.

El objetivo es mejorar la consistencia de las etiquetas antes de entrenar modelos experimentales.

## Etiquetas Permitidas

Las unicas etiquetas permitidas son:

- `positivo`
- `neutral`
- `negativo`

## Definicion De `positivo`

Un texto es `positivo` cuando expresa satisfaccion, aprobacion, recomendacion, alegria, agradecimiento o una experiencia favorable.

Ejemplos:

```text
"El servicio fue excelente y rapido"
"Me gusto mucho la atencion recibida"
"La entrega llego antes de lo esperado"
```

## Definicion De `neutral`

Un texto es `neutral` cuando informa, describe o pregunta sin expresar una emocion clara. Tambien aplica cuando el sentimiento es ambiguo o insuficiente para clasificar como positivo o negativo.

Ejemplos:

```text
"El pedido llego el lunes"
"Quiero saber el estado de mi solicitud"
"El producto es de color negro"
```

## Definicion De `negativo`

Un texto es `negativo` cuando expresa queja, rechazo, molestia, frustracion, insatisfaccion, problema o una experiencia desfavorable.

Ejemplos:

```text
"El pedido llego tarde y en mal estado"
"No me resolvieron el problema"
"La atencion fue muy mala"
```

## Reglas Para Sarcasmo

Si el sarcasmo comunica una queja o molestia, etiquetar como `negativo`.

Ejemplo:

```text
"Excelente, otra vez se cayo el servicio"
```

Etiqueta:

```text
negativo
```

Si el sarcasmo no permite interpretar claramente la emocion, etiquetar como `neutral` y documentar el caso.

## Reglas Para Textos Cortos

Textos muy cortos deben etiquetarse solo si el sentimiento es claro.

Ejemplos:

```text
"Excelente" -> positivo
"Pesimo" -> negativo
"Ok" -> neutral
```

Si un texto corto no tiene contexto suficiente, usar `neutral`.

## Reglas Para Emociones Mixtas

Cuando un texto contiene elementos positivos y negativos, clasificar segun la emocion dominante.

Ejemplo:

```text
"El producto es bueno, pero llego muy tarde"
```

Si la queja es el foco principal, etiquetar como `negativo`.

Si no hay una emocion dominante, etiquetar como `neutral`.

## Reglas Para Emojis

Los emojis pueden apoyar la etiqueta, pero no deben ser el unico criterio si el texto contradice el emoji.

Ejemplos:

```text
"Me encanto el servicio :)" -> positivo
"Nunca respondieron :(" -> negativo
"Recibido 👍" -> neutral
```

## Criterios De Consistencia

- Usar siempre las etiquetas en minuscula.
- No crear etiquetas nuevas.
- No mezclar idiomas en las etiquetas.
- Revisar duplicados antes de entrenar.
- Evitar textos con informacion personal o sensible.
- Mantener una regla consistente para textos ambiguos.
- Documentar casos dudosos para revision posterior.
- Priorizar la intencion general del mensaje sobre palabras aisladas.

## Criterio De Revision

Antes de usar el dataset v2 para entrenamiento experimental, revisar:

- Distribucion por clase.
- Duplicados exactos.
- Textos vacios.
- Etiquetas invalidas.
- Casos ambiguos.
- Posibles datos sensibles.
