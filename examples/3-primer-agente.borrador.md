> **La respuesta corta:** un agente es la misma IA, pero con permiso para abrir tus archivos, hacer una tarea, revisarla y seguir hasta terminar. Para tener el primero solo necesitas una carpeta con cuatro piezas y una frase: "revisa mi correo".

Un chat contesta una pregunta y se acaba. Un agente lee tus archivos, sigue tus reglas y deja el resultado guardado. Tú lo revisas al final. Aquí vas a construir uno pequeño y real. Los correos que va a leer son archivos de práctica, no tu bandeja de entrada.

**Al terminar tendrás:**

- Una carpeta con cuatro piezas que Claude entiende solo.
- Un mapa que le dice qué hacer cuando le pidas algo.
- Tres borradores de respuesta, escritos con tus reglas.
- Una regla de oro: no envía nada sin que le des el sí.

## Antes de empezar

Necesitas tres cosas:

- La aplicación de escritorio de Claude, instalada y con tu sesión iniciada.
- Un plan de pago de Claude. Este agente funciona en **Claude Code**, que viene dentro de la app de escritorio, en la pestaña **Code**. Es la parte de Claude que trabaja con las carpetas de tu computadora, y no está en el plan gratis. Los precios cambian según el país, así que revisa el tuyo antes de pagar nada.
- Una carpeta vacía en tu computadora, llamada `agente-correos`.

Si todavía no tienes plan de pago, lee la guía completa y decide con calma. No pagues solo para probar una cosa.

## 1. Abre la carpeta en Claude Code

Abre la aplicación y haz clic en la pestaña **Code**, arriba en el centro. Ahí está Claude Code. No uses **Chat**: esa pestaña no ve los archivos de tu computadora y el agente no funcionaría.

Antes de escribir nada, elige dos cosas en la parte de abajo:

- **Local**, para que Claude trabaje con los archivos de tu computadora.
- La carpeta `agente-correos`, con el botón de elegir carpeta.

Claude solo puede leer y escribir dentro de esa carpeta. No toca nada más.

## 2. Crea las cuatro piezas

Tu agente necesita cuatro cosas dentro de la carpeta:

- **Quién eres.** Un archivo corto con tu nombre y cómo escribes.
- **Tu skill.** Las reglas que quieres que siga al responder. Si ya hiciste la tuya en el video anterior, úsala. Si no, estas seis reglas sirven para empezar.
- **Los correos.** Un archivo por cada correo que quieres responder.
- **Una carpeta de borradores.** Donde el agente va a dejar sus respuestas.

Pega esto en Claude y cambia lo que está entre corchetes por tus datos, o descarga el archivo que hay debajo y deja que Claude te lo pregunte. Los tres correos son inventados, para practicar sin riesgo.

```text
En esta carpeta crea dos carpetas vacías, una llamada correos y otra llamada borradores. Después crea estos archivos con el texto exacto que te doy.

Archivo quien-soy.md:
Me llamo [tu nombre]. [A qué te dedicas, en una frase].
Respondo con calma, en frases cortas, sin tecnicismos.
Siempre cierro con una acción clara para la otra persona.

Archivo skill-respuestas.md:
# Mi skill para responder correos
1. Saluda por el nombre de la persona.
2. Responde la pregunta en la primera frase.
3. Máximo 5 frases en total.
4. Tono cálido y directo, como un amigo que sabe del tema.
5. Cierra con un siguiente paso concreto.
6. No uses guiones largos ni jerga técnica.

Archivo correos/01-laura.txt:
De: Laura Gómez
Asunto: ¿La guía es gratis?
Hola [tu nombre], vi tu video sobre el agente. ¿La guía cuesta algo? ¿Y necesito pagar alguna herramienta para seguirla?

Archivo correos/02-marco.txt:
De: Marco Ruiz
Asunto: Colaboración
Hola [tu nombre], soy Marco, tengo una academia online. Me gustaría que hablaras de IA con mis alumnos. ¿Tienes disponibilidad el mes que viene?

Archivo correos/03-sofia.txt:
De: Sofía Herrera
Asunto: No me sale el paso 2
Hola, intenté guardar mis instrucciones pero no sé dónde pegarlas. ¿Me ayudas?
```
<a class="prompt-download" href="/guias/primer-agente-prompt.md" download data-guide-prompt-download>
<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11"></path><path d="m7 11 5 5 5-5"></path><path d="M5 20h14"></path></svg>
<span class="prompt-download__text"><span class="prompt-download__name">Descarga el prompt 1 (.md)</span><span class="prompt-download__hint">Arrástralo a Claude Code y envíalo. Te pregunta tu nombre y a qué te dedicas, y crea los archivos por ti.</span></span>
</a>

**Qué hacer con esto:** cuando Claude termine, abre la carpeta y comprueba que están las dos subcarpetas y los cinco archivos.
