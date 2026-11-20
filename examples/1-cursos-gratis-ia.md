# Ejemplo: Diez cursos gratis de IA en español

Un recorrido completo sobre un borrador real de Ender Lopez: el primer texto que se
guardó de su guía `cursos-gratis-ia` (commit `75f11d0` del repositorio de su web), recortado a la
primera parte. El borrador lo escribió Claude, así que la segunda pasada la hizo GPT
con `tools/limpiar.sh` (Codex CLI, 19 de noviembre de 2026).

Los cuatro archivos del recorrido están al lado de este:
[borrador](1-cursos-gratis-ia.borrador.md), [reescrito](1-cursos-gratis-ia.reescrito.md),
[segunda pasada](1-cursos-gratis-ia.limpio.md) y [notas de la segunda pasada](1-cursos-gratis-ia.notas.txt).

## 1. El checker sobre el borrador

```text
$ python3 tools/deslop_es.py examples/1-cursos-gratis-ia.borrador.md
399 palabras de texto visible

  Puntuación y formato:
    · etiquetas en negrita al empezar cada línea  (12 líneas empiezan con una etiqueta en negrita)
  Avisos (no restan: el corpus aún no los respalda):
    · contraste con coma "no es X, es Y"  (1)

  nota 4/5  necesita limpieza
(código de salida 1)
```

## 2. Reescritura (Claude, siguiendo SKILL.md)

Cambios hechos a mano después de leer el borrador entero, no solo los hallazgos:
ver [la reescritura](1-cursos-gratis-ia.reescrito.md).

```text
$ python3 tools/deslop_es.py examples/1-cursos-gratis-ia.reescrito.md
387 palabras de texto visible


  nota 5/5  LIMPIO
(código de salida 0)
```

## 3. Segunda pasada con otra familia (GPT)

```text
$ DESLOP_WRITER=claude tools/limpiar.sh examples/1-cursos-gratis-ia.reescrito.md > examples/1-cursos-gratis-ia.limpio.md 2> examples/1-cursos-gratis-ia.notas.txt
limpiar: qué cambió:
- El comienzo responde directamente si hace falta pagar para empezar.
- Quité frases que retrasaban la información y precisé las explicaciones de los dos cursos.
- Dejé marcadores para los ocho cursos y los dos extras que faltan; la tabla remite a varios de ellos.
- Conservé la fecha de revisión, las duraciones y las insignias del original; no las he comprobado.
- La afirmación de que cualquier solicitud de tarjeta indica que no es el curso enlazado necesita comprobarse: que un curso sea gratuito no basta para asegurarlo.
```

## 4. El checker otra vez

```text
$ python3 tools/deslop_es.py examples/1-cursos-gratis-ia.limpio.md
388 palabras de texto visible


  nota 5/5  LIMPIO
(código de salida 0)
```

## 5. Revisión de la segunda pasada

La segunda pasada no se acepta entera. Lo que se queda y lo que vuelve atrás:

- Acepto que el comienzo responda directo si hay que pagar.
- Revierto que quitara la etiqueta "La respuesta corta:": es el formato fijo de todas sus guías y la segunda pasada la borró sin avisar en las notas.
- Los marcadores "[Faltan los cursos 3 a 10]" salen porque le pasé solo un trozo de la guía, no porque falte algo en la guía real. Se quitan.
- La nota sobre la tarjeta es justa: "si te pide la tarjeta, no es el curso de esta lista" es una regla práctica, no un hecho comprobado. Queda para que Ender decida.
- El checker no encontró nada nuevo en la versión de GPT: 5/5.
