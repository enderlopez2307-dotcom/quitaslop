#!/usr/bin/env python3
"""Pruebas del checker. Ejecuta: python3 tools/test_deslop_es.py

Dos direcciones, y la segunda es la que importa. Es fácil ensanchar una regex hasta
que lo atrapa todo, así que cada regla tiene un caso que tiene que disparar y otro,
escrito como lo escribiría una persona, que NO puede disparar.
"""
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import deslop_es as D  # noqa: E402

fallos = []
total = 0


def check(nombre, cond, detalle=''):
    global total
    total += 1
    if not cond:
        fallos.append(f'{nombre}: {detalle}')


def grupos(texto, crudo=None):
    return {k for k, v in D.audit(D.normaliza(texto), crudo).items() if v and k != 'avisos'}


def avisos(texto, crudo=None):
    return [e for e, _ in D.audit(D.normaliza(texto), crudo)['avisos']]


def md(crudo):
    return {k for k, v in D.audit(D.markdown_prose(crudo), crudo).items() if v and k != 'avisos'}


# ── Vocabulario: cada entrada dispara y su uso normal no ─────────────────────
VOCAB_SI = [
    'Una app diseñada para restaurantes pequeños.',
    'Un plan pensado para ti.',
    'Te responde al instante.',
    'Arma tu menú en segundos.',
    'Guardamos tus datos de forma segura.',
    'Precios claros, sin sorpresas.',
    'Ideal para ir al trabajo en bici.',
    'Un proceso eficiente.',
    'Te acompañamos en la configuración.',
    'Descubre el nuevo plan mensual.',
]
VOCAB_NO = [
    'El edificio fue diseñado por un arquitecto de Valencia.',   # diseñado por, no para
    'Llegó en treinta segundos exactos.',                        # una medida, no la promesa
    'Lo hizo de forma distinta a la de su hermano.',
    'La sorpresa fue enorme cuando abrió la puerta.',
    'El ideal de la época era otro.',
    'Descubrí el error al día siguiente.',                       # narración en primera persona
    'Nos acompañó hasta la estación.',
]
for t in VOCAB_SI:
    check(f'vocab dispara: {t}', 'vocab' in grupos(t))
for t in VOCAB_NO:
    check(f'vocab no dispara: {t}', 'vocab' not in grupos(t))
check('cada regla de vocabulario tiene su caso que dispara',
      all(any(re.search(D.B + '(?:' + rx + ')' + D.E, t.lower()) for t in VOCAB_SI)
          for rx, _ in D.VOCAB), 'hay una regla sin caso de prueba')

# ── Patrones de frase ────────────────────────────────────────────────────────
FRASES_SI = [
    'El problema no era la gente. Era la organización.',
    'No es falta de ganas. Es falta de tiempo.',
    'No es solo una app, es tu nueva agenda.',
    'Me apunté. No para dejar de ser enfermera, sino para entender cómo se decide.',
    'No se trata de trabajar más, sino de trabajar con un plan.',
]
FRASES_NO = [
    'Se parece a Visual Basic pero no es un clon y no corre su código. Es otra aplicación.',
    'No es tarde. Todavía hay tiempo.',             # dos frases sin el giro: "no es X. Es Y" exige copia del verbo
    'No vino a la reunión porque estaba enfermo.',
    'No solo llovió el lunes; el martes también.',  # "no solo" sin "sino" ni "es"
]
for t in FRASES_SI:
    check(f'frase dispara: {t}', 'frases' in grupos(t))
for t in FRASES_NO:
    check(f'frase no dispara: {t}', 'frases' not in grupos(t), str(D.audit(t)['frases']))
check('cada patrón de frase tiene su caso que dispara',
      all(any(re.search(rx, t.lower(), re.M) for t in FRASES_SI) for rx, _ in D.FRASES))

# ── Puntuación y formato ────────────────────────────────────────────────────
ETIQUETAS = ('- **Copias rápidas:** detecta los archivos nuevos.\n'
             '- **Multiplataforma:** funciona en Linux y en Mac.\n'
             '- **Registros claros:** muestra el progreso en tiempo real.\n')
check('etiquetas en negrita disparan', 'puntuacion' in md(ETIQUETAS))
check('dos etiquetas no bastan', 'puntuacion' not in md('\n'.join(ETIQUETAS.splitlines()[:2])))
NOTAS_HUMANAS = ('**Nota:** esto solo funciona en Linux.\n\n**Importante:** haz copia antes.\n\n'
                 '**Problema:** no arranca el servidor.\n\n**Solución:** reinstala la librería.\n')
check('etiquetas de aviso humanas no disparan', 'puntuacion' not in md(NOTAS_HUMANAS))
SOLAS = '__Salida__:\n\nalgo\n\n__Usuario__\n\nalgo\n\n__Contraseña__\n\nalgo\n'
check('etiqueta sola en su línea no dispara', 'puntuacion' not in md(SOLAS))
check('etiquetas en HTML disparan', 'puntuacion' in grupos(
    'texto', '<li><strong>Rápido:</strong> responde en el día siempre</li>' * 3))

SEP = 'Intro.\n\n---\n\nUno.\n\n---\n\nDos.\n'
check('dos separadores disparan', 'puntuacion' in md(SEP))
check('la cabecera YAML no cuenta como separador',
      'puntuacion' not in md('---\ntitulo: "x"\n---\n\nTexto.\n\n---\n\nMás texto.\n'))
check('flechas como viñetas disparan', 'puntuacion' in md('→ Uno es así.\n\n→ Otro es asá.\n'))
check('una flecha suelta no dispara', 'puntuacion' not in md('Ve a Ajustes → Cuenta.\n'))
check('título con emoji dispara', 'puntuacion' in md('# 🚀 Características\n\nTexto.\n'))
check('título sin emoji no dispara', 'puntuacion' not in md('# Características\n\nTexto.\n'))

# ── Tríos ────────────────────────────────────────────────────────────────────
for t in ('Reservas confirmadas, sin planillas, sin cuadernos y sin perder mesas.',
          'Sin desplazamientos, sin horarios imposibles, sin perder el ritmo.',
          'Más clientes, más reservas, más tiempo libre.'):
    check(f'trío dispara: {t}', 'trios' in grupos(t))
for t in ('Visitamos Argentina, Uruguay y Paraguay.',          # una lista de tres cosas de verdad
          'Es rápida, segura y barata.',                       # en el corpus, igual de humana
          'Se quedó sin batería y sin cargador.',              # "sin" dos veces dentro de una frase con y
          'Hay más gente que el año pasado.',
          'Sin desplazamientos, sin horarios imposibles.',                # dos no es una serie
          'Y cuanto más tardas en pagar, más dinero acabas devolviendo, más intereses.'):
    check(f'trío no dispara: {t}', 'trios' not in grupos(t), str(D.audit(t)['trios']))

# ── Prueba sin respaldo ─────────────────────────────────────────────────────
for t in ('Más de 5.000 clientes ya confían en nosotros.',
          'Lo usan 1200 restaurantes en México.',
          'Miles de usuarios lo recomiendan.',
          '+300 empresas trabajan con nosotros.',
          'Tenemos 10k seguidores.'):
    check(f'prueba dispara: {t}', 'prueba' in grupos(t))
for t in ('El incendio obligó a evacuar a 14 mil personas.',   # noticia, no prueba social
          'Llegaron 10 bebés en una patera a Cádiz.',
          'En 2021. Los clientes llegaron tarde.',             # el año no cruza el punto
          'Tengo 3 clientas fijas.'):                           # en femenino singular de verdad
    check(f'prueba no dispara: {t}', 'prueba' not in grupos(t), str(D.audit(t)['prueba']))
h = D.audit('Más de 5.000 clientes ya confían en nosotros.')
check('--allow-proof deja la prueba como aviso', D.puntua(h, allow_proof=True) == 5
      and D.puntua(h) == 4)

# ── Avisos: se imprimen, nunca restan ───────────────────────────────────────
AVISOS_SI = {
    'raya como pausa a la inglesa': 'Lo probé ayer — y funcionó a la primera.',
    'falta el signo de apertura': 'Te pasa esto?',
    'el arranque "imagina..."': 'Imagina un lunes sin correos.',
    'cierre de redacción escolar': 'En conclusión, vale la pena.',
    'muletilla de redacción': 'Cuando se trata de dinero, nadie duda.',
    '"es importante destacar"': 'Es importante destacar que es gratis.',
    '"es más que un X"': 'Es más que una app.',
    'pregunta que se responde sola ("¿el resultado?")': '¿El resultado? Más ventas.',
    'rodeos apilados': 'Esto podría potencialmente fallar.',
    'calco del inglés': 'Eso no hace sentido.',
    'promesa de folleto': 'Lleva tu negocio al siguiente nivel.',
    '"todo en un solo lugar"': 'Tus reservas en un solo lugar.',
    '"y listo" / "tip extra"': 'Lo pegas ¡y listo!',
    'muchos punto y coma': 'Uno; dos; tres; cuatro; cinco.',
    '"te ayuda a" / "puede ayudarte"': 'Esta guía te ayudará a reunir tus gastos.',
    'frase que anuncia en lugar de decir ("lo mejor viene ahora")': 'Paso tres. Lo mejor viene ahora.',
    'contraste con coma "no es X, es Y"': 'El problema no es encontrar cursos, es que hay demasiados.',
}
for etiqueta, t in AVISOS_SI.items():
    check(f'aviso dispara: {etiqueta}', etiqueta in avisos(t), str(avisos(t)))
    check(f'aviso no resta: {etiqueta}', D.puntua(D.audit(D.normaliza(t))) == 5
          or grupos(t), 'un aviso restó puntos')
check('aviso Title Case dispara', 'títulos con Mayúscula En Cada Palabra' in avisos(
    'x', '## Cómo Empezar Con Tu Presupuesto\n'))
for t in ('No es fácil, pero se puede.',
          'Le ayudé a cargar las cajas.',                 # ayudar en primera persona, otra cosa
          'Lo mejor fue el postre.',                      # opinión, no anuncio
          'El diálogo —dijo ella— se escribe así.',     # inciso con raya, correcto en español
          '¿Te pasa esto?', '¡Qué bien!',
          'Reuters — La empresa anunció ayer.'):        # pie de agencia, como en las noticias
    check(f'aviso no dispara: {t}', not avisos(t), str(avisos(t)))
check('título bien escrito no avisa', not avisos('x', '## Cómo empezar con tu presupuesto\n'))
check('título con nombre propio y función en minúscula no avisa',
      not avisos('x', '## Plantilla de la Universidad de Alicante\n'))
AV_TOTAL = len(D.AVISOS)
check('cada aviso tiene su caso', AV_TOTAL == len(AVISOS_SI) + 1, f'{AV_TOTAL} avisos')

# ── Nada regional resta ─────────────────────────────────────────────────────
REGIONALES = [
    # voseo rioplatense
    'Vos sabés cómo es: llegás tarde, agarrás el celular y te escriben tres clientes a la vez.',
    'Probalo una semana y, si no te sirve, me avisás.',
    # vosotros, España
    'Si tenéis dudas, escribidnos y os contestamos mañana. Vale, tío, nos vemos en el piso.',
    'Haced una copia del ordenador antes de tocar nada, que luego os arrepentís.',
    # ustedes, México, Colombia, Caribe
    'Ustedes ya saben que el carro no arranca. Ahorita les mando la foto, está chévere.',
    'La guagua pasa a las ocho y la pega empieza a las nueve, así que no da la plata para el taxi.',
    # usted
    'Usted puede pedir la cita por teléfono o en la ventanilla del ayuntamiento.',
]
for t in REGIONALES:
    check(f'regional limpio: {t[:40]}', not grupos(t) and not avisos(t),
          str(D.audit(D.normaliza(t))))

# ── Markdown: lo citado no cuenta ───────────────────────────────────────────
DOC = ('# Qué marca\n\nLa regla busca `diseñado para` y `sin sorpresas`.\n\n'
       '```\nUna app diseñada para ti, sin sorpresas.\n```\n\n'
       '~~Te responde al instante.~~ Así no.\n\n![una app diseñada para ti](a.png)\n')
check('código, tachado e imágenes no cuentan', not md(DOC), str(md(DOC)))
check('el texto de un enlace sí cuenta', 'vocab' in md('Mira [la app diseñada para ti](https://x.y).'))
check('la URL de un enlace no cuenta', not md('Mira [aquí](https://x.y/sin-sorpresas-al-instante).'))
check('la cabecera YAML no cuenta',
      not md('---\ndescripcion: "Diseñado para ti, sin sorpresas"\n---\n\nHola, esto es una guía.\n'))

# ── HTML: solo lo visible ───────────────────────────────────────────────────
PAG = ('<html><head><style>.a{}</style><script>var x="diseñado para"</script></head>'
       '<body><!-- sin sorpresas --><h1>Reservas</h1><p>Anotá cada reserva.</p></body></html>')
check('script, style y comentarios no cuentan', not grupos(D.visible_text(PAG)))
check('entidades HTML se decodifican', 'vocab' in grupos(D.visible_text('<p>Dise&ntilde;ado para ti</p>')))

# ── Normalización ───────────────────────────────────────────────────────────
check('espacio duro no rompe la regla', 'vocab' in grupos('diseñado\xa0para ti'))
check('caracteres invisibles fuera', D.normaliza('dise​ñado') == 'diseñado')
check('la raya no se normaliza', '—' in D.normaliza('a — b'))

# ── La línea de comandos ────────────────────────────────────────────────────
CLI = [sys.executable, os.path.join(AQUI, 'deslop_es.py')]


def corre(*args, stdin=None):
    return subprocess.run(CLI + list(args), capture_output=True, text=True, input=stdin,
                          encoding='utf-8')


r = corre('--text', 'Hola, te escribo por lo del lunes.')
check('--text limpio sale 0', r.returncode == 0 and 'LIMPIO' in r.stdout, r.stdout)
r = corre('--text', 'Una app diseñada para ti, sin sorpresas.')
check('--text con hallazgos sale 1', r.returncode == 1 and '4/5' in r.stdout, r.stdout)
r = corre('--text', 'Más de 5.000 clientes nos eligen.', '--allow-proof')
check('--allow-proof sale 0 y sigue avisando', r.returncode == 0 and '5.000 clientes' in r.stdout, r.stdout)
r = corre('--text', '   ')
check('entrada vacía falla', r.returncode != 0 and 'vacía' in r.stderr, r.stderr)
r = corre('/no/existe.md')
check('archivo inexistente falla sin traza', r.returncode != 0 and 'Traceback' not in r.stderr, r.stderr)
r = corre()
check('sin argumentos muestra la ayuda', r.returncode != 0 and 'deslop_es.py' in r.stderr)

with tempfile.TemporaryDirectory() as d:
    p = os.path.join(d, 'b.md')
    open(p, 'w', encoding='utf-8').write('# Hola\n\nUna app `diseñada para` ti.\n')
    r = corre(p)
    check('archivo .md limpio sale 0', r.returncode == 0, r.stdout)
    p = os.path.join(d, 'p.html')
    open(p, 'w', encoding='utf-8').write(
        '<div id="view-a"><p>Te responde al instante.</p></div><div id="view-b"><p>Hola.</p></div>')
    check('HTML con hallazgo sale 1', corre(p).returncode == 1)
    check('--view puntúa solo ese bloque', corre(p, '--view', 'view-b').returncode == 0)
    check('--view inexistente falla', corre(p, '--view', 'view-z').returncode != 0)
    p = os.path.join(d, 'vacio.md')
    open(p, 'w', encoding='utf-8').write('```\nsolo código\n```\n')
    check('Markdown sin prosa falla como vacío', corre(p).returncode != 0)
    p = os.path.join(d, 'u.md')
    open(p, 'wb').write('¿Qué tal? ¡Genial, niño! Ñandú.\n'.encode('utf-8'))
    r = subprocess.run(CLI + [p], capture_output=True, env={**os.environ, 'PYTHONIOENCODING': 'cp1252'})
    check('lee UTF-8 aunque la consola sea cp1252', r.returncode == 0 and b'Traceback' not in r.stderr,
          r.stderr.decode('utf-8', 'replace'))

# ── La documentación pasa su propio checker ─────────────────────────────────
for doc in ('README.md', 'SKILL.md'):
    ruta = os.path.join(RAIZ, doc)
    if not os.path.exists(ruta):
        continue
    r = corre(ruta)
    check(f'{doc} saca 5/5', r.returncode == 0, r.stdout[-400:])
    prosa = D.markdown_prose(open(ruta, encoding='utf-8').read())
    rayas = re.findall(r'.{20}(?:—|–| - ).{20}', prosa)
    check(f'{doc} no usa la raya ni el guion como puntuación', not rayas, str(rayas[:3]))
    check(f'{doc} sin avisos', 'Avisos' not in r.stdout, r.stdout[-400:])

if fallos:
    print(f'{len(fallos)} de {total} pruebas FALLARON:')
    for f in fallos:
        print('  ·', f)
    sys.exit(1)
print(f'las {total} pruebas pasaron')
