---
name: quitaslop
description: Revisa un texto en español para quien lo va a leer, busca patrones de texto escrito por IA medidos en un corpus, reescribe, pide una segunda pasada a otra familia de modelos y vuelve a comprobar. Úsalo con /quitaslop, "humaniza esto", "quítale lo de IA", "¿esto suena a IA?", "arregla este texto".
---

# quitaslop

Edita el borrador que te pasen pensando en su lector y en su propósito. Sirve para
READMEs, páginas de venta, correos, guiones de video y guías. El checker encuentra
patrones conocidos y después hay que leer el texto en su contexto. Un 5/5 significa
que ninguno de los patrones que restan apareció. No demuestra que el texto sea claro,
cierto ni escrito por una persona.

## Paso 1: el contexto y el checker

Averigua quién lo va a leer, en qué formato y qué necesita sacar de él. Usa lo que
te dieron y el propio borrador. Pregunta solo si falta algo que cambiaría la edición.

```bash
python3 tools/deslop_es.py borrador.md
python3 tools/deslop_es.py pagina.html
python3 tools/deslop_es.py --text "pega aquí el borrador"
```

El checker mira cinco categorías: vocabulario, patrones de frase, puntuación y
formato, tríos y prueba sin respaldo. Cada categoría con algún hallazgo resta un
punto. Por debajo de 5/5 sale con código 1, y una entrada vacía también falla.

Los avisos se imprimen pero no restan: son patrones conocidos que el corpus todavía
no respalda. Míralos igual.

Para Markdown, pásale la ruta del archivo: así el código y los ejemplos citados no
cuentan. Las reglas son para español: con un texto en otro idioma la nota no dice nada.

## Paso 2: revisar y reescribir

Lee [references/principios.md](references/principios.md) para la revisión editorial
y [references/senales-de-ia.md](references/senales-de-ia.md) para el catálogo con
sus mediciones.

Trabaja el borrador en este orden:

1. Primero el propósito y el orden. La primera pregunta del lector se responde
   pronto. Fuera los ganchos repetidos y las frases que anuncian algo en lugar de
   decirlo.
2. Después el sentido y las pruebas. Cada frase suma algo y sigue de la anterior. Las
   condiciones quedan pegadas a lo que limitan. Fuera los contrastes vacíos y las
   metáforas que no explican. Se conservan los datos, el comportamiento técnico y la
   postura del autor.
3. Al final las palabras, el formato y el ritmo. Revisa los hallazgos del checker y
   cambia lo vago por lo concreto. Lee las frases vecinas juntas para ver formas
   repetidas. Quita las etiquetas en negrita de cada viñeta cuando una frase normal se
   lee mejor.

Respeta la variedad del autor: vos, tú, usted, ustedes y vosotros se quedan como
están. No conviertas el texto a otro país ni a un español "neutro".

No fabriques personalidad con muletillas, faltas a propósito, frases cortas por cuota
ni opiniones que el autor no dio. No agregues una cifra a cada afirmación. Usa solo
datos que dio el autor o que comprobaste en una fuente adecuada.

El checker puede marcar una frase correcta. Mira el hallazgo antes de cambiarlo. Nunca
escondas prosa normal dentro de código para subir la nota. Si una frase necesaria sigue
marcada, explícaselo al usuario.

## Paso 3: segunda pasada con otra familia de modelos

La pasada la hace una familia distinta de la que escribió el borrador. Es una segunda
revisión con el mismo lector y el mismo propósito. Revisa sus cambios antes de
aceptarlos.

| Borrador escrito con | Comando |
|---|---|
| Claude | `DESLOP_WRITER=claude tools/limpiar.sh borrador.md > limpio.md` |
| GPT, Codex o ChatGPT | `DESLOP_WRITER=gpt tools/limpiar.sh borrador.md > limpio.md` |
| Gemini o un modelo local | Cualquiera de los dos, según la CLI que tengas. |

El script usa el modelo configurado en esa CLI y [prompts/limpiar.txt](prompts/limpiar.txt).
La CLI tiene que estar instalada y con sesión iniciada. En Mac, el script también
encuentra la CLI que trae la app de Codex. Si no hay ninguna, pega el prompt y el
borrador en el chat de la otra familia. Si no hay forma de usar un segundo modelo, dile
al usuario que esa pasada no se hizo y sigue con la revisión y el checker.

La salida estándar trae el texto editado. La salida de error trae las notas de cambios.
Para guardar las dos:

```bash
DESLOP_WRITER=claude tools/limpiar.sh borrador.md > limpio.md 2> notas.txt
```

Mira el código de salida. Un tiempo agotado devuelve 124. Sin la CLI de la otra
familia devuelve 127 e imprime el prompt con el borrador, y eso no es un texto editado.
Un borrador vacío o ilegible devuelve 66 y una respuesta vacía del modelo, 70. El modelo de
la segunda pasada corre sin herramientas, sin servidores MCP y en una carpeta vacía, así
que un borrador con instrucciones escondidas no puede usarlo para leer archivos ni
mandar nada. No le quites esas opciones al script.

El modelo separa sus notas con `<<<QUITASLOP-NOTAS>>>`. Si aparece un aviso de que
falta esa marca, puede que las notas se hayan colado en el texto. Revísalo.

## Paso 4: comparar y volver a comprobar

Compara el resultado con el original. Mira que los datos y los comandos no cambiaron,
que los enlaces y los marcadores siguen ahí y que el comienzo se entiende. Lee las notas
por si se borró algo necesario.

```bash
python3 tools/deslop_es.py limpio.md
```

Intenta resolver los hallazgos sin cambiar lo que el texto quiere decir. Cuenta las
excepciones justificadas. La revisión final hace falta aunque la nota sea 5/5.

Si cambias una regex, corre `python3 tools/test_deslop_es.py`. Si cambias el script de
limpieza, corre `bash tools/test_limpiar.sh`.

## Datos y cifras

Nunca inventes pruebas: ni cifras de clientes, ni testimonios, ni valoraciones, ni
resultados. Si al borrador le falta un dato, márcalo con `[falta el dato]` y avisa al
autor. No publiques un marcador sin resolver como si fuera un dato comprobado.

La regla de prueba solo ve una cifra al lado de una palabra como "clientes". No sabe
si es cierta. Usa `--allow-proof` solo después de comprobarla: la regla sigue avisando
pero deja de restar.

## Qué entregar

Devuelve el texto reescrito o guarda el archivo editado, según lo que te pidan.
Después, hasta cinco notas cortas con los cambios importantes y el resultado del
checker. Di si la segunda pasada se hizo. Deja a la vista los datos sin resolver y
los hallazgos que quedan. No digas que la edición demuestra que lo escribió una persona.
