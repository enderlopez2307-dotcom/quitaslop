# Ejemplo: 31 códigos de video para Claude

Un recorrido completo sobre un borrador real de Ender Lopez: el primer texto que se
guardó de su guía `codigos-de-video` (commit `f18e27b` del repositorio de su web), recortado a la
primera parte. El borrador lo escribió Claude, así que la segunda pasada la hizo GPT
con `tools/limpiar.sh` (Codex CLI, 19 de noviembre de 2026).

Los cuatro archivos del recorrido están al lado de este:
[borrador](2-codigos-de-video.borrador.md), [reescrito](2-codigos-de-video.reescrito.md),
[segunda pasada](2-codigos-de-video.limpio.md) y [notas de la segunda pasada](2-codigos-de-video.notas.txt).

## 1. El checker sobre el borrador

```text
$ python3 tools/deslop_es.py examples/2-codigos-de-video.borrador.md
414 palabras de texto visible

  Patrones de frase:
    · el contraste "no es X. Es Y"  (1)
  Puntuación y formato:
    · etiquetas en negrita al empezar cada línea  (7 líneas empiezan con una etiqueta en negrita)

  nota 3/5  necesita limpieza
(código de salida 1)
```

## 2. Reescritura (Claude, siguiendo SKILL.md)

Cambios hechos a mano después de leer el borrador entero, no solo los hallazgos:
ver [la reescritura](2-codigos-de-video.reescrito.md).

```text
$ python3 tools/deslop_es.py examples/2-codigos-de-video.reescrito.md
397 palabras de texto visible


  nota 5/5  LIMPIO
(código de salida 0)
```

## 3. Segunda pasada con otra familia (GPT)

```text
$ DESLOP_WRITER=claude tools/limpiar.sh examples/2-codigos-de-video.reescrito.md > examples/2-codigos-de-video.limpio.md 2> examples/2-codigos-de-video.notas.txt
limpiar: qué cambió:
- El comienzo explica qué se descarga y cómo se usa. La lista distingue entre tener los códigos instalados y aplicar cada edición.
- Cambié «color de cine» por «ajustar el color» para describir la tarea sin prometer un acabado impreciso.
- Antes de publicar, conviene comprobar los planes que incluyen **Code**, los nombres y posiciones de sus controles y si admite adjuntar el ZIP como se indica.
- La afirmación de que **Chat** no ve archivos de la computadora es absoluta y necesita comprobación. La conservé para no cambiar la instrucción técnica sin respaldo.
- Se mantiene explícito que el funcionamiento en Windows todavía no está comprobado.
```

## 4. El checker otra vez

```text
$ python3 tools/deslop_es.py examples/2-codigos-de-video.limpio.md
399 palabras de texto visible


  nota 5/5  LIMPIO
(código de salida 0)
```

## 5. Revisión de la segunda pasada

La segunda pasada no se acepta entera. Lo que se queda y lo que vuelve atrás:

- Revierto otra vez la etiqueta "La respuesta corta:" que la segunda pasada quitó.
- "Ajustar el color" en lugar de "color de cine" es más prudente, pero "color de cine" es el nombre que Ender le da a ese código en su guía. Si el nombre promete de más, lo decide él, no la segunda pasada.
- Acepto "un transcriptor, que convierte lo que dices en texto": explica mejor la herramienta.
- Las dudas sobre la pestaña Chat y el plan gratis son de hecho, no de estilo: se comprueban en la app antes de publicar.
- El checker no encontró nada nuevo en la versión de GPT: 5/5.
