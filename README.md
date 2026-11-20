# quitaslop

quitaslop revisa un texto en busca de patrones comunes de la escritura
hecha con IA y trae instrucciones para editarlo. Sirve para un README, una página de
venta, un correo, una guía o el guion de un video. Está hecho para el español de
Latinoamérica y de España, con reglas escritas y medidas para el español, no traducidas
del inglés.

El checker de Python busca en cinco categorías y le pone al texto una nota sobre 5.
El flujo de edición le pide a un agente de IA que revise el borrador pensando en quién
lo va a leer, que lo reescriba y que pida una segunda pasada a otra familia de modelos.

Un 5/5 quiere decir que el checker no encontró ninguno de los patrones que restan.
Igual hay que leer el texto y ver si se entiende, si lo que dice es cierto y si le da al
lector lo que vino a buscar.

## Para empezar

El checker usa Python 3 y su biblioteca estándar. No necesita claves de API ni
paquetes.

```bash
git clone https://github.com/enderlopez2307-dotcom/quitaslop
cd quitaslop

# Revisa un borrador corto.
python3 tools/deslop_es.py --text "Una app diseñada para ti, sin sorpresas y al instante."
# Saca 4/5 y sale con código 1.

# Revisa un archivo Markdown.
python3 tools/deslop_es.py README.md

# Revisa el texto visible de un HTML.
python3 tools/deslop_es.py index.html
```

Cada categoría con algún hallazgo resta un punto, haya uno o muchos. El comando sale
con código 0 en 5/5 y con código 1 por debajo. Una entrada vacía también falla. Revisar
un archivo no lo modifica.

En Markdown, el checker se salta los bloques de código, el código en línea, las
imágenes, el texto tachado, las URLs y la cabecera YAML. En HTML quita las etiquetas y
el contenido de `script` y `style`. No dibuja la página, así que un texto escondido con
CSS también cuenta.

## Editar un borrador

Dale a tu agente el archivo [SKILL.md](SKILL.md) y el borrador. Dile para quién es y dónde
se va a publicar si el texto no lo deja claro.

1. Corre el checker para ver los patrones que reconoce.
2. Revisa el propósito y el orden del borrador. Un README explica qué hace la herramienta
   y cómo se usa. Un correo deja claro por qué escribe.
3. Reescribe lo confuso o repetido. Mira que cada frase sume algo y que lo que afirma
   coincida con los datos que tienes.
4. Pide una segunda pasada a otra familia de modelos, revisa sus cambios y corre el
   checker otra vez.

La segunda pasada usa [prompts/limpiar.txt](prompts/limpiar.txt). Con una CLI de IA
instalada y con la sesión iniciada:

```bash
# Si el borrador lo escribió Claude, la segunda pasada la hace GPT (Codex).
DESLOP_WRITER=claude tools/limpiar.sh borrador.md > limpio.md

# Si lo escribió GPT, la hace Claude.
DESLOP_WRITER=gpt tools/limpiar.sh borrador.md > limpio.md

# Lee el resultado y revísalo otra vez.
python3 tools/deslop_es.py limpio.md
```

El script escribe el texto editado en la salida estándar y las notas de cambios en la
salida de error. En Mac también encuentra la CLI que trae la app de Codex.

Si falta la CLI de la otra familia, el script imprime el prompt con el borrador y sale
con código 127: pégalo en el chat de la otra familia. Un tiempo agotado sale con 124, un
borrador vacío o ilegible con 66 y una respuesta vacía del modelo con 70. Mira el código
antes de dar por bueno el archivo.

El modelo de la segunda pasada trabaja sin herramientas: no puede leer tus archivos,
ejecutar comandos, navegar ni usar las apps conectadas a tu cuenta, como el correo o
Drive. Corre en una carpeta vacía y recibe el borrador por la entrada estándar. Así, un
texto con instrucciones escondidas para la IA (por ejemplo, uno que te mandan para
"revisar") no puede hacer que el modelo saque datos de tu equipo. Las pruebas comprueban
que esas protecciones siguen en el script.

Otro modelo da otra pasada de edición. Eso no garantiza un texto mejor. En los tres
ejemplos de [examples/](examples/) la segunda pasada borró una etiqueta que el autor usa en
todas sus guías y cambió una palabra donde no tocaba. Revisa siempre lo que cambió.

### Como skill de un agente

Para Claude Code, copia esta carpeta en `~/.claude/skills/quitaslop/` y usa
`/quitaslop`. Para Codex u otro agente, pídele que siga [SKILL.md](SKILL.md).

## Qué marca el checker

| Categoría | Qué busca |
|---|---|
| Vocabulario | Giros de folleto como `diseñado para`, `al instante`, `de forma sencilla` o `sin sorpresas`. |
| Patrones de frase | El contraste `no es X. Es Y` en sus formas españolas: `no es solo X, es Y`, `no para X, sino para Y`, `no se trata de X, sino de Y`. |
| Puntuación y formato | Tres líneas o más que empiezan con una etiqueta en negrita, separadores `---` entre secciones, viñetas con flechas o emojis y títulos con emoji. |
| Tríos | La serie de tres que repite `sin`, `más` o `menos`. |
| Prueba sin respaldo | Una cifra al lado de palabras como `clientes` o `usuarios`. No puede comprobar si es cierta. |

Además imprime avisos que no restan puntos: patrones conocidos que el corpus todavía no
respalda, como la raya usada como pausa, la falta de ¿ o ¡, los títulos con mayúscula en
cada palabra o el arranque `imagina`. El catálogo completo, con las cifras de cada regla y
lo que se midió y quedó fuera, está en
[references/senales-de-ia.md](references/senales-de-ia.md).

Si una cifra de clientes es real y la puedes demostrar:

```bash
python3 tools/deslop_es.py index.html --allow-proof
```

La cifra se sigue mostrando, pero deja de restar. El checker no comprueba la prueba.

Nada regional resta puntos. Vos, tú, usted, ustedes y vosotros, celular y móvil, carro y
coche: las pruebas comprueban que un texto con cualquiera de ellos saca 5/5.

## Las cifras

Cada regla que resta entró porque, medida en un corpus, sale claramente más en
borradores de IA que en textos escritos por personas.

El corpus tiene 42 borradores de IA y 51 textos humanos. Los borradores salieron
de 14 encargos (README, página de venta, correo, guion, publicación de LinkedIn, guía,
descripción de producto y blog), la mitad para Latinoamérica y la mitad para España, cada
uno pedido a tres familias de modelos el 19 de noviembre de 2026: Claude, GPT y Gemma.
Los textos humanos son noticias de Wikinoticias, guías de Wikiviajes, tutoriales de
Wikilibros y READMEs de GitHub en español, todos con licencia abierta y en su versión
anterior a 2022.

| | Marcados por el checker |
|---|---|
| Borradores de IA | 28 de 42 (67 %) |
| Textos humanos | 0 de 51 (0 %) |
| Borradores de Claude | 12 de 14 |
| Borradores de Gemma | 13 de 14 |
| Borradores de GPT | 3 de 14 |

Esas cifras son las del mejor caso: las reglas se eligieron mirando ese mismo corpus.
Para medir fuera de la muestra hay un conjunto de control con encargos y textos nuevos que
no se miraron al elegir ninguna regla:

| Control | Marcados por el checker |
|---|---|
| Borradores de IA | 9 de 18 (50 %) |
| Textos humanos | 0 de 14 (0 %) |

El control tiene 6 encargos nuevos pedidos a las mismas tres familias y 14 textos humanos
nuevos. Por familia, el checker marca 4 de 6 borradores de Claude, 3 de 6 de Gemma y 2 de 6
de GPT. Fuera de la muestra, entonces, encuentra señales en la mitad de los borradores de IA.

Todas las cifras, regla por regla y candidato por candidato, están en
[corpus/MEDICIONES.md](corpus/MEDICIONES.md). Se repiten con:

```bash
python3 corpus/scripts/medir.py --informe
```

Los borradores de IA están en el repositorio. Los textos humanos son de otras personas y
no se suben: `corpus/fuentes-humano.tsv` guarda la URL exacta de cada revisión y
`corpus/scripts/` los descarga.

## Revisar más allá de la nota

Lee el borrador donde lo va a encontrar quien lo lea. Antes de aceptar una edición:

- ¿Responde lo que el lector va a preguntar, con el detalle justo? Los términos técnicos
  se explican donde importan por primera vez.
- ¿El primer párrafo dice de qué se trata o da una razón útil para seguir leyendo?
- ¿Cada frase sigue de la anterior? Fuera las metáforas y los contrastes que no aportan.
- ¿Puedes respaldar cada afirmación? Las condiciones van pegadas a lo que limitan.
- ¿Suena como su autor y como su formato? La variedad de cada país se respeta.

Más en [references/principios.md](references/principios.md). Nunca agregues una cifra o
un testimonio para que una frase suene concreta. Si falta un dato, márcalo para el autor.

### Límites

Las reglas son para español y no detectan el idioma. Un texto en otro idioma puede sacar
5/5 porque ningún patrón coincide.

El corpus es chico. Con 42 y 51 textos, una regla que aparece en dos o tres borradores
tiene poca base, y la categoría de tríos no llega a ser una diferencia clara (p = 0,2).

El lado humano es sobre todo periodístico, de viajes y técnico. No hay páginas de venta,
correos ni guiones escritos por personas con licencia abierta. Una persona que escribe
textos de venta puede usar `diseñado para` o `sin sorpresas` y el checker la va a marcar.

Los borradores de GPT casi no tienen estas marcas: el checker solo marca 3 de 14. Su
español prudente y ordenado sale igual que el de los textos humanos en todo lo que se
midió.

Puede marcar una frase correcta y dejar pasar un texto malo. No sabe quién escribió el
texto, no comprueba datos y no juzga si un comienzo le sirve a su público. Usa los
hallazgos como motivo para revisar. Una nota de 5/5 no demuestra que el texto sea bueno.

## Pruebas

```bash
python3 tools/test_deslop_es.py
bash tools/test_limpiar.sh
python3 tools/deslop_es.py README.md
python3 tools/deslop_es.py SKILL.md
```

Cada regla tiene un caso que tiene que marcar y otro, escrito como lo escribiría una
persona, que no puede marcar. Las pruebas también comprueban que este README y
[SKILL.md](SKILL.md) sacan 5/5 y no usan la raya ni el guion como puntuación.

## Ejemplos y fuentes

- [Diez cursos gratis de IA](examples/1-cursos-gratis-ia.md), [31 códigos de video para
  Claude](examples/2-codigos-de-video.md) y [Tu primer agente](examples/3-primer-agente.md):
  tres recorridos completos sobre borradores reales de Ender Lopez, con el checker, la
  reescritura, la segunda pasada de GPT, el checker otra vez y qué cambios se aceptaron.
- [Fuentes](references/fuentes.md): las listas de partida y el
  detalle del corpus.

[Licencia MIT](LICENSE).
