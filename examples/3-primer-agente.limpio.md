> Un agente es una IA con permiso para trabajar con tus archivos, hacer una tarea, revisarla y seguir hasta terminar. Para crear el de esta guía necesitas una carpeta con cuatro piezas y este prompt: "revisa mi correo".

Aquí vas a crear un agente que lee correos de práctica, sigue tus reglas y guarda borradores de respuesta para que tú los revises. Los correos serán archivos en tu computadora; el agente no se conectará a tu bandeja de entrada.

Al terminar tendrás:

- Una carpeta con los archivos que Claude necesita.
- Un archivo que le dice qué hacer cuando le pidas algo.
- Tres borradores de respuesta, escritos con tus reglas.
- Una regla: no envía nada sin que le des el sí.

## Antes de empezar

Necesitas:

- La aplicación de escritorio de Claude, instalada y con tu sesión iniciada.
- Un plan de pago de Claude. Este agente funciona en **Claude Code**, que está en la pestaña **Code** de la aplicación de escritorio. Es la parte de Claude que trabaja con las carpetas de tu computadora y no está en el plan gratis. Los precios cambian según el país, así que revisa el tuyo antes de pagar.
- Una carpeta vacía en tu computadora, llamada `agente-correos`.

Si todavía no tienes un plan de pago, lee la guía completa antes de decidir. No pagues solo para probar una cosa.

## 1. Abre la carpeta en Claude Code

Abre la aplicación y haz clic en la pestaña **Code**, arriba en el centro. Ahí está Claude Code. No uses **Chat**: esa pestaña no ve los archivos de tu computadora y el agente no funcionaría.

Antes de escribir, selecciona estas dos opciones en la parte de abajo:

- **Local**, para que Claude trabaje con los archivos de tu computadora.
- La carpeta `agente-correos`, con el botón de elegir carpeta.

Claude solo puede leer y escribir dentro de esa carpeta. No toca nada más.

## 2. Crea las cuatro piezas

Dentro de la carpeta, el agente necesita:

1. Un archivo con tu nombre y cómo escribes.
2. Tu skill, un archivo con las reglas que quieres que siga al responder. Si ya hiciste la tuya en el video anterior, úsala. Si no, puedes empezar con las seis reglas del prompt.
3. Los correos, un archivo por cada uno que quieres responder.
4. Una carpeta de borradores, donde el agente va a guardar sus respuestas.

Pega este prompt en Claude y cambia lo que está entre corchetes por tus datos. También puedes descargarlo con el enlace de abajo para que Claude te pregunte esos datos. Los tres correos son inventados para practicar.

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

Cuando Claude termine, abre la carpeta y comprueba que están las dos subcarpetas y los cinco archivos.
