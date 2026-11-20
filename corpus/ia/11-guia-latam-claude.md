# Tu primer presupuesto en Google Sheets
### Guía gratuita para principiantes

## Introducción

Llegar a fin de mes sin saber en qué se fue el dinero es más común de lo que parece. No es falta de disciplina. Es que nadie nos enseñó a verlo.

Un presupuesto personal es solo una lista: cuánto dinero entra, cuánto sale y cuánto queda. Con eso puedes decidir en qué gastar, cuánto ahorrar y qué recortar sin sentir culpa.

Para hacerlo no necesitas ser bueno con los números, ni pagar una app, ni saber de finanzas. Necesitas **Google Sheets**, que es gratis y funciona en tu computadora o en tu celular. Solo te hace falta una cuenta de Google (la misma de Gmail).

**Al terminar esta guía tendrás:**

• Una hoja de presupuesto propia, lista para usar cada mes.

• Fórmulas simples que hacen las sumas por ti.

• Un hábito de 10 minutos a la semana para saber dónde está tu dinero.

**Antes de empezar:**

• Esta guía sirve para cualquier moneda: pesos, soles, quetzales, bolívares, dólares. Usa la tuya.

• No hace falta instalar nada. Todo se hace desde el navegador o la app de Google Sheets.

• Ten a mano tu último estado de cuenta o tus últimos gastos. No tienen que ser exactos, un estimado basta para arrancar.

---

## Primeros pasos

### Paso 1: Crea tu hoja

1. Entra a **sheets.google.com** e inicia sesión con tu cuenta de Google.

2. Haz clic en **Hoja de cálculo en blanco** (el cuadro con el signo +).

3. Arriba a la izquierda, donde dice "Hoja de cálculo sin título", escribe un nombre. Por ejemplo: **Presupuesto 2026**.

4. Abajo a la izquierda verás una pestaña llamada "Hoja 1". Haz doble clic y cámbiale el nombre a **Noviembre** (o al mes en que estés). Cada mes tendrá su propia pestaña.

Google guarda todo automáticamente. No existe un botón de guardar.

### Paso 2: Anota tus ingresos

Aquí va todo el dinero que entra en el mes: sueldo, ventas, trabajos extra, ayudas familiares.

1. En la celda **A1** escribe: `INGRESOS`

2. Desde la **A2** hacia abajo, escribe cada fuente. Por ejemplo:
   • Sueldo
   • Trabajo extra
   • Otros

3. En la columna **B**, al lado de cada una, escribe el monto.

4. En la celda **A6** escribe `Total ingresos`.

**Consejo:** si tus ingresos cambian de un mes a otro, usa el monto más bajo que has recibido. Así tu plan es realista y cualquier extra es ganancia.

### Paso 3: Anota tus gastos

Divide tus gastos en dos grupos. Es la separación más útil de todo el presupuesto.

**Gastos fijos:** casi no cambian cada mes. Alquiler, internet, celular, transporte, cuotas, suscripciones.

**Gastos variables:** cambian según el mes. Comida, ocio, ropa, salidas, imprevistos.

1. En la celda **D1** escribe: `GASTOS FIJOS`

2. Debajo, escribe cada gasto en la columna **D** y su monto en la columna **E**.

3. Deja unas filas de espacio y escribe `GASTOS VARIABLES` con el mismo formato.

Si no sabes cuánto gastas en algo, escribe un estimado y corrígelo cuando tengas datos reales. Ajustar es parte del proceso.

### Paso 4: Tu primera fórmula

Esta fórmula suma por ti. Con ella no tendrás que usar calculadora.

1. Haz clic en la celda **B6**, donde va el total de ingresos.

2. Escribe exactamente esto y presiona **Enter**:

`=SUMA(B2:B5)`

Eso suma todo lo que escribiste entre B2 y B5. Si agregas o cambias un monto, el total se actualiza solo.

**Si te sale un error:** revisa que no haya espacios ni letras dentro de los montos. Las celdas con números deben tener solo números. Si tu Google Sheets está en inglés, la fórmula se escribe `=SUM(B2:B5)`.

Repite lo mismo con tus gastos: crea una celda de `Total gastos` y usa `=SUMA(` con el rango de tus gastos.

### Paso 5: Descubre cuánto te queda

Esta es la cifra que más importa. En una celda libre escribe `Me queda` y, al lado, esta fórmula (ajusta las celdas a tu hoja):

`=B6-E20`

Eso es tus ingresos menos tus gastos.

• **Si es positivo:** te sobra dinero. En la siguiente parte de la guía verás cómo darle un destino.

• **Si es negativo:** estás gastando más de lo que ganas. No es un fracaso, es información. Ahora sabes dónde mirar.

---

## Lo que viene en la siguiente parte

• Cómo agregar categorías con colores para ver tus gastos de un vistazo.

• Cómo crear un gráfico automático.

• La regla 50/30/20 adaptada a la realidad de Latinoamérica.

• Cómo duplicar tu hoja cada mes en 10 segundos.

**Por ahora, tu tarea es una sola:** completa los pasos 1 al 5 con tus números reales. Aunque queden a medias, ya habrás hecho lo que la mayoría nunca hace: mirar su dinero de frente.
