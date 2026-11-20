# Fuentes

## Reglas escritas para el español

Las reglas se escribieron para el español y se midieron en un corpus propio (ver abajo).
Muchas señales del inglés no tienen equivalente útil: en español no se apilan palabras
compuestas con guion, y la raya tiene un uso correcto que el inglés no tiene.

## Punto de partida para los candidatos

La primera lista de candidatos salió de reglas de escritura que Ender Lopez ya usaba
para su contenido en español: palabras de folleto (`potenciar`, `optimizar`,
`revolucionario`), aperturas y cierres hechos, el contraste `no es X, es Y`, las
frases que anuncian algo en lugar de decirlo y la prohibición de la raya como pausa.

También se miró el catálogo de Wikipedia en inglés,
[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
que mantiene WikiProject AI Cleanup.

Ninguna de esas listas decidió nada por sí sola. Un candidato entra en el checker
solo si el corpus lo respalda. Varias palabras de esas listas salieron más en los
textos de personas que en los de IA y quedaron fuera; están en
[senales-de-ia.md](senales-de-ia.md) con sus cifras.

## El corpus

Todo el detalle está en [corpus/MEDICIONES.md](../corpus/MEDICIONES.md) y los scripts
para repetirlo en `corpus/scripts/`.

### Lado IA

Catorce encargos en español (README, página de inicio, correo, guion de
reel, publicación de LinkedIn, guía, descripción de producto y artículo de blog), la
mitad para Latinoamérica y la mitad para España. Cada encargo se le pidió a
tres familias de modelos el 19 de noviembre de 2026: Claude (Sonnet, por la CLI de
Claude Code), GPT (por la CLI de Codex) y Gemma 4 12B (local, por LM Studio). Los
borradores están en `corpus/ia/` tal como salieron. Son nuestros y se pueden leer.

### Lado humano

Textos en español escritos por personas, con licencia abierta, en su
versión anterior a 2022 para no mezclar borradores de IA:

| Fuente | Licencia | Formato |
|---|---|---|
| [Wikinoticias](https://es.wikinews.org) | CC BY 2.5 | noticias de Latinoamérica y España |
| [Wikiviajes](https://es.wikivoyage.org) | CC BY-SA 3.0 | guías de ciudades |
| [Wikilibros](https://es.wikibooks.org) | CC BY-SA 3.0 | tutoriales |
| READMEs de GitHub en español | MIT | documentación de proyectos |

### Control

Para medir fuera de la muestra hay 6 encargos más (`corpus/ia-control/`,
pedidos a las mismas tres familias) y 14 textos humanos más
(`corpus/fuentes-humano-control.tsv`). Ninguno se miró al elegir las reglas.

Esos textos no se suben al repositorio: son de otras personas. El repositorio guarda la
lista exacta de revisiones (`corpus/fuentes-humano.tsv`, con la URL de cada una) y los
scripts que los descargan, así que cualquiera puede repetir la medición.

## Lo que no hay

No hay textos de venta, correos ni guiones escritos por personas con licencia abierta
en el corpus, y por eso el lado humano es sobre todo periodístico, de viajes y técnico.
Tampoco hay un corpus de Ender hablando o escribiendo en español sin ayuda de IA. Las
consecuencias de eso están en la sección de límites del README.
