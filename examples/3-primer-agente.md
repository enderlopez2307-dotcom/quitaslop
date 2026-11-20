# Ejemplo: Tu primer agente con Claude Code

Un recorrido completo sobre un borrador real de Ender Lopez: el primer texto que se
guardó de su guía `primer-agente` (commit `32088f1` del repositorio de su web), recortado a la
primera parte. El borrador lo escribió Claude, así que la segunda pasada la hizo GPT
con `tools/limpiar.sh` (Codex CLI, 19 de noviembre de 2026).

Los cuatro archivos del recorrido están al lado de este:
[borrador](3-primer-agente.borrador.md), [reescrito](3-primer-agente.reescrito.md),
[segunda pasada](3-primer-agente.limpio.md) y [notas de la segunda pasada](3-primer-agente.notas.txt).

## 1. El checker sobre el borrador

```text
$ python3 tools/deslop_es.py examples/3-primer-agente.borrador.md
514 palabras de texto visible

  Puntuación y formato:
    · etiquetas en negrita al empezar cada línea  (6 líneas empiezan con una etiqueta en negrita)

  nota 4/5  necesita limpieza
(código de salida 1)
```

## 2. Reescritura (Claude, siguiendo SKILL.md)

Cambios hechos a mano después de leer el borrador entero, no solo los hallazgos:
ver [la reescritura](3-primer-agente.reescrito.md).

```text
$ python3 tools/deslop_es.py examples/3-primer-agente.reescrito.md
513 palabras de texto visible


  nota 5/5  LIMPIO
(código de salida 0)
```

## 3. Segunda pasada con otra familia (GPT)

```text
$ DESLOP_WRITER=claude tools/limpiar.sh examples/3-primer-agente.reescrito.md > examples/3-primer-agente.limpio.md 2> examples/3-primer-agente.notas.txt
limpiar: qué cambió:
- Quité la comparación tajante entre chat y agente y centré la introducción en lo que hará este ejercicio.
- Expliqué «skill» donde aparece y conservé intactos el código, las etiquetas HTML y el enlace.
- Queda por verificar la disponibilidad de Claude Code según el plan, la ubicación de los controles y la afirmación sobre el acceso a archivos desde **Chat**.
- La afirmación de que Claude solo puede acceder a la carpeta elegida requiere comprobación: seleccionar una carpeta no demuestra por sí solo ese límite de permisos.
- Este fragmento no muestra cómo se cargan las reglas, se generan los borradores ni se establece la autorización antes de enviar. Tampoco permite comprobar que el prompt descargable pregunte los datos, como anuncia el enlace.
```

## 4. El checker otra vez

```text
$ python3 tools/deslop_es.py examples/3-primer-agente.limpio.md
491 palabras de texto visible


  nota 5/5  LIMPIO
(código de salida 0)
```

## 5. Revisión de la segunda pasada

La segunda pasada no se acepta entera. Lo que se queda y lo que vuelve atrás:

- Revierto la etiqueta "La respuesta corta:" quitada.
- Revierto "este prompt: 'revisa mi correo'": ahí "revisa mi correo" es una frase que se le dice al agente, y la segunda pasada aplicó la regla de "prompt" donde no tocaba.
- Acepto que la introducción diga desde el principio que los correos son de práctica y no la bandeja de entrada real.
- La duda sobre "Claude solo puede leer y escribir dentro de esa carpeta" es buena: es una afirmación de seguridad y hay que comprobarla en la documentación antes de publicarla.
- El checker no encontró nada nuevo en la versión de GPT: 5/5.
