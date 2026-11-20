# Mediciones del corpus

Archivo generado por `python3 corpus/scripts/medir.py --informe`. No se edita a mano.

Corpus: **42 borradores de IA** y **51 textos humanos**. Cada texto se recorta a sus primeras 700 palabras de prosa en los dos lados.

Lado IA por familia: claude 14, gemma 14, gpt 14.

Lado humano por formato: guia-viaje 14, noticia 22, readme 10, tutorial 5.


## 1. El checker tal como está

| Categoría | Borradores de IA | Textos humanos | p (Fisher, una cola) |
|---|---|---|---|
| Vocabulario | 17 de 42 | 0 de 51 | 1.5e-07 |
| Patrones de frase | 6 de 42 | 0 de 51 | 0.0069 |
| Puntuación y formato | 21 de 42 | 0 de 51 | 1.5e-09 |
| Tríos | 2 de 42 | 0 de 51 | 0.2 |
| Prueba sin respaldo | 0 de 42 | 0 de 51 | 1 |
| Avisos (no restan) | 10 de 42 | 4 de 51 | 0.032 |
| **Nota por debajo de 5/5** | **28 de 42 (67 %)** | **0 de 51 (0 %)** | 1.1e-13 |

Por familia de modelos:

| Familia | Marcados | Total |
|---|---|---|
| claude | 12 | 14 |
| gemma | 13 | 14 |
| gpt | 3 | 14 |

Por región del encargo (lado IA) y de la fuente (lado humano):

| Región | IA marcados | Humanos marcados |
|---|---|---|
| latam | 16 de 21 | 0 de 23 |
| espana | 12 de 21 | 0 de 13 |

Textos humanos marcados por error: ninguno.

Borradores de IA que pasan con 5/5: `01-readme-latam-gpt`, `02-readme-espana-gpt`, `03-landing-latam-gpt`, `04-landing-espana-gpt`, `05-email-latam-claude`, `06-email-espana-gpt`, `07-guion-latam-gpt`, `08-guion-espana-claude`, `08-guion-espana-gemma`, `08-guion-espana-gpt`, `09-post-latam-gpt`, `10-post-espana-gpt`, `12-guia-espana-gpt`, `14-blog-espana-gpt`.


## 1b. Fuera de la muestra: el conjunto de control

Las reglas se eligieron mirando el corpus de arriba, así que esas cifras son las del mejor caso. El conjunto de control son encargos y textos nuevos que no se miraron al elegir ninguna regla (`corpus/ia-control/`, `corpus/fuentes-humano-control.tsv`).

| | Marcados | Total |
|---|---|---|
| Borradores de IA | 9 (50 %) | 18 |
| Textos humanos | 0 (0 %) | 14 |
| IA, claude | 4 | 6 |
| IA, gemma | 3 | 6 |
| IA, gpt | 2 | 6 |

Humanos marcados en el control: ninguno.


## 2. Todos los candidatos medidos

Criterio para restar puntos: el patrón sale en 2 borradores de IA o más, de 2 encargos distintos o más (para que no sea el tema del encargo), y en los textos humanos sale como mucho en una cuarta parte de esa proporción. Los que no cumplen quedan fuera o pasan a aviso. "enc." es el número de encargos distintos.

| Cat. | Candidato | IA | Humanos | enc. | p |
|---|---|---|---|---|---|
| vocab | potenciar | 0 | 3 | 0 | 1 |
| vocab | optimizar | 3 | 2 | 3 | 0.41 |
| vocab | agilizar | 0 | 0 | 0 | 1 |
| vocab | empoderar | 0 | 0 | 0 | 1 |
| vocab | revolucionar | 0 | 0 | 0 | 1 |
| vocab | transformador | 0 | 0 | 0 | 1 |
| vocab | innovador | 0 | 0 | 0 | 1 |
| vocab | holístico | 0 | 0 | 0 | 1 |
| vocab | sinergia | 0 | 0 | 0 | 1 |
| vocab | paradigma | 0 | 0 | 0 | 1 |
| vocab | robusto | 1 | 0 | 1 | 0.45 |
| vocab | sin fricciones | 0 | 0 | 0 | 1 |
| vocab | integral | 0 | 1 | 0 | 1 |
| vocab | fundamental | 3 | 3 | 3 | 0.56 |
| vocab | crucial | 1 | 0 | 1 | 0.45 |
| vocab | esencial | 0 | 0 | 0 | 1 |
| vocab | aprovechar | 2 | 1 | 1 | 0.43 |
| vocab | adentrarse | 0 | 0 | 0 | 1 |
| vocab | sumergirse | 0 | 0 | 0 | 1 |
| vocab | embarcarse | 0 | 1 | 0 | 1 |
| vocab | desbloquear | 2 | 0 | 1 | 0.2 |
| vocab | elevar | 0 | 0 | 0 | 1 |
| vocab | impulsar | 0 | 1 | 0 | 1 |
| vocab | fomentar | 0 | 0 | 0 | 1 |
| vocab | navegar (figurado) | 0 | 0 | 0 | 1 |
| vocab | panorama | 0 | 0 | 0 | 1 |
| vocab | ecosistema | 0 | 1 | 0 | 1 |
| vocab | vibrante | 0 | 0 | 0 | 1 |
| vocab | fascinante | 0 | 0 | 0 | 1 |
| vocab | apasionante | 0 | 0 | 0 | 1 |
| vocab | increíble | 0 | 0 | 0 | 1 |
| vocab | poderoso | 1 | 0 | 1 | 0.45 |
| vocab | sin esfuerzo | 0 | 0 | 0 | 1 |
| vocab | sin complicaciones | 1 | 0 | 1 | 0.45 |
| vocab | de vanguardia | 1 | 0 | 1 | 0.45 |
| vocab | de última generación | 0 | 0 | 0 | 1 |
| vocab | siguiente nivel | 0 | 0 | 0 | 1 |
| vocab | reglas del juego | 0 | 0 | 0 | 1 |
| vocab | viaje (figurado) | 0 | 0 | 0 | 1 |
| vocab | aventura | 1 | 0 | 1 | 0.45 |
| vocab | magia | 0 | 0 | 0 | 1 |
| vocab | descubre | 2 | 0 | 2 | 0.2 |
| vocab | garantizar | 3 | 1 | 3 | 0.24 |
| vocab | a medida | 1 | 0 | 1 | 0.45 |
| vocab | intuitivo | 0 | 1 | 0 | 1 |
| vocab | eficiente | 3 | 0 | 3 | 0.088 |
| vocab | experiencia (producto) | 1 | 1 | 1 | 0.7 |
| vocab | soluciones | 0 | 0 | 0 | 1 |
| vocab | tranquilidad | 1 | 2 | 1 | 0.84 |
| vocab | sin preocupaciones | 0 | 0 | 0 | 1 |
| vocab | resonar | 0 | 0 | 0 | 1 |
| vocab | meticuloso | 0 | 0 | 0 | 1 |
| vocab | inigualable | 0 | 1 | 0 | 1 |
| vocab | imprescindible | 0 | 0 | 0 | 1 |
| vocab | maximizar | 1 | 0 | 1 | 0.45 |
| vocab | sacar el máximo | 0 | 0 | 0 | 1 |
| vocab | en un abrir y cerrar | 0 | 0 | 0 | 1 |
| vocab | clave (adjetivo) | 0 | 0 | 0 | 1 |
| vocab | herramienta poderosa | 1 | 0 | 1 | 0.45 |
| vocab | transformar (figurado) | 0 | 0 | 0 | 1 |
| vocab | únicos | 0 | 0 | 0 | 1 |
| vocab | ideal para | 5 | 0 | 3 | 0.016 |
| vocab | perfecto para | 1 | 0 | 1 | 0.45 |
| vocab | acompañarte | 2 | 0 | 2 | 0.2 |
| vocab | gestionar | 4 | 0 | 4 | 0.038 |
| vocab | facilitar | 1 | 3 | 1 | 0.91 |
| vocab | crear contenido de valor | 0 | 0 | 0 | 1 |
| frases | no es solo… es | 1 | 0 | 1 | 0.45 |
| frases | no solo… sino | 0 | 4 | 0 | 1 |
| frases | no se trata de… sino | 1 | 0 | 1 | 0.45 |
| frases | no es X, es Y (sin solo) | 0 | 0 | 0 | 1 |
| frases | más que un | 0 | 0 | 0 | 1 |
| frases | ya sea / ya seas | 0 | 1 | 0 | 1 |
| frases | ahí es donde entra | 0 | 0 | 0 | 1 |
| frases | di adiós a | 0 | 0 | 0 | 1 |
| frases | imagina… | 0 | 0 | 0 | 1 |
| frases | en conclusión / en resumen | 0 | 0 | 0 | 1 |
| frases | cuando se trata de | 0 | 0 | 0 | 1 |
| frases | al final del día | 0 | 0 | 0 | 1 |
| frases | la clave está | 0 | 0 | 0 | 1 |
| frases | la verdad es que | 0 | 0 | 0 | 1 |
| frases | te ayuda a | 4 | 1 | 4 | 0.13 |
| frases | hedge apilado | 0 | 0 | 0 | 1 |
| frases | pregunta que se responde | 0 | 0 | 0 | 1 |
| frases | ¿por qué? suelto | 0 | 0 | 0 | 1 |
| frases | lo mejor de todo | 1 | 0 | 1 | 0.45 |
| frases | pero eso no es todo | 0 | 0 | 0 | 1 |
| frases | ¿listo para…? | 0 | 0 | 0 | 1 |
| frases | empecemos / manos a la obra | 0 | 0 | 0 | 1 |
| frases | es importante destacar | 0 | 1 | 0 | 1 |
| frases | juega un papel | 0 | 0 | 0 | 1 |
| frases | en el mundo actual | 0 | 1 | 0 | 1 |
| frases | hoy en día | 0 | 1 | 0 | 1 |
| frases | ya no es un lujo | 0 | 0 | 0 | 1 |
| frases | no necesitas ser experto | 1 | 0 | 1 | 0.45 |
| frases | de forma sencilla/rápida | 3 | 0 | 3 | 0.088 |
| frases | teaser (lo peor/lo mejor) | 2 | 0 | 2 | 0.2 |
| frases | aquí viene lo interesante | 0 | 0 | 0 | 1 |
| frases | lo que nadie te dice | 0 | 0 | 0 | 1 |
| frases | esto lo cambia todo | 0 | 0 | 0 | 1 |
| frases | déjame contarte | 0 | 0 | 0 | 1 |
| frases | calco: hacer sentido | 0 | 0 | 0 | 1 |
| frases | calco: aplicar para | 0 | 0 | 0 | 1 |
| frases | calco: en orden de | 0 | 0 | 0 | 1 |
| frases | calco: tomar lugar | 0 | 0 | 0 | 1 |
| frases | calco: jugar un rol | 0 | 0 | 0 | 1 |
| frases | ojo / spoiler | 0 | 0 | 0 | 1 |
| frases | desde X hasta Y | 1 | 3 | 1 | 0.91 |
| frases | todo lo que necesitas | 0 | 0 | 0 | 1 |
| frases | en este artículo | 0 | 0 | 0 | 1 |
| frases | pasos sencillos | 1 | 0 | 1 | 0.45 |
| frases | ¿sabías que | 0 | 0 | 0 | 1 |
| frases | no estás solo | 1 | 0 | 1 | 0.45 |
| frases | menos X. más Y. | 0 | 0 | 0 | 1 |
| frases | diseñado para | 9 | 0 | 6 | 0.00046 |
| frases | una forma sencilla de | 1 | 0 | 1 | 0.45 |
| frases | todo en un solo lugar | 2 | 0 | 1 | 0.2 |
| frases | ¿te suena? | 1 | 0 | 1 | 0.45 |
| frases | sin sorpresas | 3 | 0 | 2 | 0.088 |
| frases | al instante / en segundos | 5 | 0 | 3 | 0.016 |
| frases | cero X | 1 | 0 | 1 | 0.45 |
| frases | par de sin | 2 | 0 | 2 | 0.2 |
| frases | no era X. era Y | 3 | 1 | 3 | 0.24 |
| frases | no V X. V Y (mismo verbo) | 1 | 0 | 1 | 0.45 |
| frases | no para X, sino para Y | 2 | 0 | 2 | 0.2 |
| frases | la diferencia está en | 1 | 0 | 1 | 0.45 |
| frases | quiasmo cuidar es cuidar | 0 | 0 | 0 | 1 |
| frases | y listo / tip extra | 3 | 0 | 2 | 0.088 |
| frases | desde el primer día | 1 | 0 | 1 | 0.45 |
| punct | raya espaciada | 1 | 22 | 1 | 1 |
| punct | raya como pausa entre minúsculas | 1 | 0 | 1 | 0.45 |
| punct | semiraya espaciada | 0 | 0 | 0 | 1 |
| punct | guion espaciado como pausa | 2 | 12 | 2 | 1 |
| punct | dos puntos de revelación | 0 | 0 | 0 | 1 |
| trios | trío de palabras | 10 | 15 | 7 | 0.8 |
| trios | trío anafórico | 2 | 0 | 2 | 0.2 |
| trios | tres frases cortas | 0 | 0 | 0 | 1 |
| prueba | número junto a un sustantivo | 1 | 6 | 1 | 0.99 |
| formato | punto y coma > 2 | 0 | 1 | 0 | 1 |
| formato | pregunta sin ¿ | 0 | 0 | 0 | 1 |
| formato | exclamación sin ¡ | 0 | 1 | 0 | 1 |
| formato | títulos en Mayúsculas | 0 | 0 | 0 | 1 |
| formato | etiquetas en negrita ≥3 | 25 | 1 | 13 | 1.7e-10 |
| formato | título con emoji | 2 | 0 | 2 | 0.2 |
| formato | separadores --- ≥2 | 5 | 0 | 3 | 0.016 |
| formato | flechas → como viñetas ≥2 | 4 | 0 | 3 | 0.038 |
| formato | emojis ≥3 | 8 | 2 | 7 | 0.022 |
