# Señales de texto escrito por IA en español

Este catálogo dice qué busca el checker, cuánto respalda cada regla el corpus y qué se
midió y quedó fuera. Las cifras dicen en cuántos borradores de IA y en cuántos textos
humanos aparece cada regla, sobre 42 borradores de IA y 51 textos humanos. El detalle de cada
medición está en [corpus/MEDICIONES.md](../corpus/MEDICIONES.md).

Una coincidencia no prueba quién escribió el texto. Sirve para mirar esa frase otra vez.

## Cómo entra una regla

1. El candidato sale de una lista de reglas de escritura o de leer los borradores de IA.
2. Se mide en el corpus. Resta puntos solo si aparece en 2 borradores de IA o más, de 2
   encargos distintos o más (para que no sea el tema del encargo), y en los textos humanos
   como mucho en una cuarta parte de esa proporción.
3. Si es un patrón conocido pero el corpus no lo respalda, pasa a **aviso**: se imprime y
   no resta.
4. Si sale igual o más en los textos humanos, queda fuera.

## 1. Vocabulario (17 de 42 borradores de IA, 0 de 51 textos humanos)

Giros de folleto. En el corpus no aparecen las palabras de siempre (`potenciar`,
`revolucionario`, `sinergia`): aparecen promesas cortas que se repiten en páginas,
correos y guías.

| Regla | IA | Humanos |
|---|---|---|
| `diseñado para`, `pensado para` | 9 | 0 |
| `al instante`, `en segundos`, `con un clic` | 5 | 0 |
| `ideal para` | 5 | 0 |
| `de forma sencilla`, `rápida`, `segura`, `eficiente` | 3 | 0 |
| `sin sorpresas`, `sin complicaciones`, `sin letra pequeña` | 3 | 0 |
| `eficiente` | 3 | 0 |
| `acompañarte`, `te acompañamos` | 2 | 0 |
| `descubre` como llamada a la acción | 2 | 0 |

`Gestionar` cumple el criterio (4 y 0), pero se dejó fuera a propósito: es un verbo de
uso diario, y si no sale en el lado humano es porque el corpus humano casi no tiene
textos de oficina ni de negocio.

## 2. Patrones de frase (6 de 42 borradores de IA, 0 de 51 textos humanos)

El contraste `no es X, es Y` en sus formas españolas. Cuentan como una sola regla.

| Forma | IA | Humanos | Ejemplo del corpus |
|---|---|---|---|
| `no es X. Es Y` | 3 | 0 | `No es falta de ganas. Es falta de tiempo.` |
| `no es solo X, es Y` | 1 | 0 | `No es solo una bebida, es un ritual diario.` |
| `no para X, sino para Y` | 2 | 0 | `No para dejar de ser enfermera, sino para entender...` |
| `no se trata de X, sino de Y` | 1 | 0 | |
| **Las cuatro juntas** | **6** | **0** | |

La forma con coma sin `solo` (`no es X, es Y`) salió en 1 borrador y queda como aviso.

`No solo X, sino también Y` **no** está: salió en 4 textos humanos y en ninguno de IA.
Es español de periódico.

Dos reglas restaban con el corpus a medias y pasaron a aviso con el corpus completo:
`te ayuda a` (3 borradores de IA y 1 texto humano) y la frase que anuncia en lugar de
decir, como `lo mejor viene ahora` (1 borrador).

## 3. Puntuación y formato (21 de 42 borradores de IA, 0 de 51 textos humanos)

| Regla | IA | Humanos |
|---|---|---|
| Tres líneas o más que empiezan con una etiqueta en negrita y siguen con la explicación (`**Copias rápidas:** detecta...`) | 16 | 0 |
| Dos separadores `---` o más entre secciones | 5 | 0 |
| Dos viñetas o más hechas con flechas o emojis (→, 👉, ✅) | 4 | 0 |
| Títulos que empiezan con emoji | 2 | 0 |

La etiqueta en negrita es la marca más repetida del corpus. La versión amplia (cualquier
negrita al principio de línea) salía en 22 borradores de IA y en 3 READMEs humanos; esos
READMEs usaban `**Nota:**`, `**Importante:**` o una etiqueta sola en su línea, y esas
formas ya no cuentan.

**La raya no es una señal en español.** La raya espaciada apareció en 22 textos humanos y
en 1 de IA: las noticias la usan para la fuente (`— Reuters, 12 de junio`) y el español la
usa en diálogos e incisos. La raya como pausa a la inglesa entre minúsculas salió en 1 borrador de IA y en
ningún texto humano, así que queda como aviso.

## 4. Tríos (2 de 42 borradores de IA, 0 de 51 textos humanos)

| Regla | IA | Humanos |
|---|---|---|
| Serie de tres que repite `sin`, `más` o `menos`: `sin planillas, sin cuadernos y sin perder mesas` | 2 | 0 |

Es la categoría más débil: con este corpus no llega a ser una diferencia clara (p = 0,2).
La lista de tres a secas (`rápida, segura y eficiente`) salió en 10 borradores de IA y en
15 textos humanos, así que no cuenta. `Sin batería y sin cargador` y `cuanto más tardas,
más pagas` tampoco cuentan: son español normal.

## 5. Prueba sin respaldo

Una cifra al lado de un sustantivo de prueba social: `más de 5.000 clientes`,
`1200 restaurantes`, `miles de usuarios`, `+300 empresas`. En el corpus no aparece en ningún
borrador de IA ni en ningún texto humano, así que funciona como protección y no
como señal de IA. Es la única equivocación que no tiene vuelta atrás, una cifra inventada publicada, y por eso
avisa de más a propósito.

`Personas`, `familias` o `pacientes` no están en la lista: en las noticias humanas salían
cifras reales de personas (`14 mil personas evacuadas`) en 6 de 51 textos.

Si la cifra es real y la puedes demostrar, `--allow-proof` la deja como aviso.

## Avisos: se imprimen, no restan

Patrones conocidos que el corpus todavía no respalda. Míralos, pero no cambies una frase
solo porque aparezca aquí.

| Aviso | IA | Humanos | Por qué es aviso |
|---|---|---|---|
| `te ayuda a`, `puede ayudarte` | 3 | 1 | sale también en humanos |
| Frase que anuncia en lugar de decir (`lo mejor viene ahora`) | 1 | 0 | un solo caso |
| Contraste con coma `no es X, es Y` | 1 | 0 | un solo caso |
| Raya como pausa entre minúsculas | 1 | 0 | un solo caso |
| Promesa de folleto (`al siguiente nivel`, `revolucionario`) | 1 | 0 | un solo caso |
| `todo en un solo lugar` | 2 | 0 | los dos del mismo encargo |
| `y listo`, `tip extra` | 2 | 0 | los dos del mismo encargo |
| Falta el ¿ o el ¡ de apertura | 0 | 1 | ningún borrador de IA lo omitió |
| Muchos punto y coma | 0 | 1 | sale en humanos |
| `cuando se trata de`, `hoy en día`, `en el mundo actual` | 0 | 1 | sale en humanos |
| `es importante destacar`, `cabe mencionar` | 0 | 1 | sale en humanos |
| Títulos con Mayúscula En Cada Palabra | 0 | 0 | sin casos |
| El arranque `imagina...` | 0 | 0 | sin casos |
| `en conclusión`, `en resumen` | 0 | 0 | sin casos |
| `es más que un X` | 0 | 0 | sin casos |
| Pregunta que se responde sola (`¿el resultado?`) | 0 | 0 | sin casos |
| Rodeos apilados (`podría potencialmente`) | 0 | 0 | sin casos |
| Calcos (`hace sentido`, `toma lugar`) | 0 | 0 | sin casos |

## Lo que se midió y quedó fuera

Palabras que las listas de `palabras de IA` dan por señal y que en este corpus salieron
igual o más en los textos humanos:

| Candidato | IA | Humanos |
|---|---|---|
| potenciar | 0 | 3 |
| fundamental | 2 | 3 |
| facilitar | 1 | 3 |
| tranquilidad | 1 | 2 |
| optimizar | 3 | 2 |
| aprovechar | 1 | 1 |
| integral, impulsar, ecosistema | 0 | 1 cada una |
| `no solo X, sino Y` | 0 | 4 |
| `desde X hasta Y` | 1 | 3 |
| lista de tres sin repetición | 10 | 15 |
| guion espaciado como pausa | 2 | 12 |

Y muchas que no salieron en ningún lado: `sinergia`, `holístico`, `empoderar`,
`sumérgete`, `adentrarse`, `paradigma`, `de vanguardia`, `en el mundo actual`. Los modelos
de 2026 escriben en español con menos de esas palabras que lo que dicen las listas.

## Lo que el checker no ve

- Un texto correcto y vacío: frases sin errores que no dicen nada.
- El registro neutro y prudente de GPT (`conviene`, `permite`, `puede resultar`). Se midió
  y sale igual en los textos humanos.
- Si un dato es cierto.
- Si el texto le sirve a quien lo lee. Para eso está [principios.md](principios.md).
