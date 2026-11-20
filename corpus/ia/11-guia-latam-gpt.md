# Tu primer presupuesto personal en Google Sheets

¿Sabes cuánto dinero necesitas para llegar a fin de mes? Entre la renta, el mercado, el transporte y los gastos pequeños, a veces cuesta verlo con claridad.

Esta guía te ayudará a reunir tus ingresos y gastos en una hoja sencilla de Google Sheets. No necesitas saber de contabilidad ni haber usado una hoja de cálculo antes. Solo necesitas una cuenta de Google y unos minutos para empezar.

Tu presupuesto no tiene que quedar perfecto. Puedes comenzar con cantidades aproximadas y ajustarlas cuando revises tus movimientos. Lo importante es que refleje tu situación y te sirva para decidir cómo usar tu dinero.

**1. Crea tu hoja**

Entra a **sheets.google.com**, inicia sesión y crea una hoja de cálculo en blanco.

Ponle un nombre fácil de reconocer, por ejemplo: **Presupuesto personal — noviembre**.

Puedes hacerlo desde el celular, aunque una computadora te permitirá escribir y revisar las cifras con más comodidad.

**2. Elige el mes y la moneda**

Empieza con un solo mes. Usa tu moneda habitual: pesos, soles, quetzales o la que corresponda.

Si recibes o gastas dinero en distintas monedas, convierte los importes a una misma moneda antes de sumarlos.

En la hoja verás columnas identificadas con letras y filas con números. Cada casilla se llama *celda*. Por ejemplo, **B4** es la celda donde se cruzan la columna B y la fila 4.

**3. Escribe la estructura**

Copia estos textos en las celdas indicadas. Deja vacías las filas que no aparecen en la tabla.

| Fila | Columna A | Columna B |
|---|---|---|
| 1 | Mi presupuesto mensual | |
| 2 | Mes | Escribe el mes |
| 3 | Concepto | Monto previsto |
| 4 | Ingreso disponible | |
| 6 | GASTOS | |
| 7 | Vivienda | |
| 8 | Servicios e internet | |
| 9 | Alimentación | |
| 10 | Transporte | |
| 11 | Salud | |
| 12 | Pagos de deudas | |
| 13 | Gustos y entretenimiento | |
| 14 | Otros gastos | |
| 15 | Total de gastos | |
| 17 | Ahorro previsto | |
| 19 | Saldo por asignar | |

Puedes cambiar las categorías. Si envías dinero a tu familia o pagas estudios, incluye esos gastos en tu presupuesto.

**4. Completa tus primeras cantidades**

En **B4**, escribe el ingreso que esperas tener disponible durante el mes, después de descuentos.

Si tus ingresos cambian, empieza con una cantidad prudente basada en lo que sueles recibir. Evita contar dinero que todavía no tienes confirmado.

Después, completa tus gastos previstos en **B7 a B14**. Usa recibos, movimientos bancarios o anotaciones para orientarte. Escribe **0** cuando una categoría no aplique.

Introduce solo números, sin escribir el símbolo de moneda dentro de cada celda.

**5. Haz que la hoja calcule**

En **B15**, escribe:

`=SUMA(B7:B14)`

Esta fórmula suma tus gastos. Si aparece un error porque tu hoja utiliza funciones en inglés, prueba:

`=SUM(B7:B14)`

En **B17**, escribe cuánto quieres reservar para ahorrar este mes. Puedes poner **0** para empezar.

Por último, en **B19**, escribe:

`=B4-B15-B17`

El resultado muestra cuánto queda después de los gastos y el ahorro previstos:

- **Positivo:** todavía hay dinero por asignar.
- **Cero:** ya asignaste todo tu ingreso.
- **Negativo:** lo previsto supera tu ingreso y necesitas revisar las cantidades.

Ya tienes una primera versión de tu presupuesto. Ahora puedes mirar tus cifras juntas y ajustar el plan a lo que realmente necesitas este mes.