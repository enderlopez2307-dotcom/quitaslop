#!/usr/bin/env python3
"""Busca señales de texto escrito por IA en español. Regex, sin opiniones, sale en rojo.

    python3 tools/deslop_es.py borrador.md
    python3 tools/deslop_es.py pagina.html
    python3 tools/deslop_es.py pagina.html --view view-inicio   # solo un bloque
    python3 tools/deslop_es.py --text "un texto para revisar"
    python3 tools/deslop_es.py borrador.md --allow-proof        # cifra comprobada

Puntúa sobre 5, una categoría por punto. Por debajo de 5 sale con código 1.
En HTML lee solo lo que ve quien visita la página: quita <script>, <style> y las
etiquetas. En Markdown quita el código, los ejemplos tachados y las imágenes.

Cada patrón que resta puntos entró porque, medido en el corpus de corpus/, sale
claramente más en borradores de IA que en textos de personas (corpus/MEDICIONES.md).
Los patrones conocidos que el corpus todavía no respalda salen como AVISOS: se
imprimen, no restan. Nada regional resta: vos, vosotros, ustedes, celular o móvil
son español de personas.
"""
import html as _html
import re
import sys

B = r'(?<!\w)'   # inicio de palabra; \w de Python incluye tildes y eñes
E = r'(?!\w)'    # fin de palabra

# ── el catálogo ──────────────────────────────────────────────────────────────
# Cada entrada: (regex, etiqueta). Las cifras de los comentarios son textos de IA
# donde aparece / textos humanos donde aparece, sobre el corpus medido.
# Criterio para restar: IA en 2 textos o más y humanos en 0, o IA en 4 o más y
# humanos en 1 como mucho. Ver corpus/MEDICIONES.md.

VOCAB = [
    # Palabras y giros de folleto. Cifras: textos de IA / textos humanos del corpus.
    (r'(?:dise[nñ]ad|pensad)(?:o|a|os|as) (?:para|espec[ií]ficamente|especialmente|pensando)',
     'diseñado para / pensado para'),
    (r'al instante|en (?:cuesti[oó]n de |pocos )?segundos|con un (?:solo )?(?:clic|toque)',
     'al instante / en segundos'),
    (r'de (?:forma|manera) (?:sencilla|r[aá]pida|f[aá]cil|eficiente|eficaz|intuitiva|segura|c[oó]moda|[aá]gil)',
     'de forma sencilla / rápida / segura'),
    (r'sin (?:sorpresas|complicaciones|letra peque[nñ]a|compromiso)',
     'sin sorpresas / sin complicaciones'),
    (r'ideal(?:es)? para', 'ideal para'),
    (r'eficiente(?:s|mente)?', 'eficiente'),
    (r'acompa[nñ]ar(?:te|les|los)|te acompa[nñ]a(?:mos|r[eé]|r[aá]|n)?', 'acompañarte'),
    (r'descubre', 'descubre (como llamada a la acción)'),
]

# El contraste "no es X, es Y" en sus formas españolas. La X no puede llevar un
# " y no " dentro: "no es un clon y no corre código. Es una app" es una descripción,
# no el giro, y el corpus humano lo tenía.
_X = r"(?:(?! y no )[^.!?]){1,60}?"

FRASES = [
    (r'(?<!\w)no (?:es|son|era|eran|fue|est[aá]) (?:solo |s[oó]lo |solamente |simplemente )?'
     + _X + r'[.;:]\s+(?:es|son|era|eran|fue|est[aá]|es que) ',
     'el contraste "no es X. Es Y"'),
    (r'(?<!\w)no (?:es|son|era) (?:solo|s[oó]lo|solamente|simplemente)\b' + _X + r',\s*(?:es|son|era)\s',
     'el contraste "no es solo X, es Y"'),
    (r'(?:^|[.!?]\s)no (?:para|por|porque|con|de|en) ' + _X + r', sino ',
     'el contraste "no para X, sino para Y"'),
    (r'no se trata (?:solo |s[oó]lo |simplemente )?de\b' + _X + r'\b(?:sino|se trata)\b',
     'el contraste "no se trata de X, sino de Y"'),
]

# Puntuación y marcas de formato: se miran sobre el texto original, no en minúsculas.
# Etiquetas que las personas también ponen en negrita para avisar: no cuentan.
_AVISO_HUMANO = (r'(?:nota|importante|aviso|advertencia|atenci[oó]n|ojo|salida|ejemplo|problema|'
                 r'soluci[oó]n|resultado|requisitos?|uso)')
_ETIQUETA = re.compile(
    r'^[ \t]*(?:[-*+•]|\d+[.)])?[ \t]*(?:\*\*|__)(?!' + _AVISO_HUMANO + r'\W)[^*_\n]{2,50}?[:.]?'
    r'(?:\*\*|__)[:.]?[ \t]*(?:[-–—][ \t]*)?(?:\S+[ \t]+){2,}\S', re.M | re.I)
_ETIQUETA_HTML = re.compile(r'<(?:strong|b)>[^<]{2,50}[:.]\s*</(?:strong|b)>\s*(?:\w+\s+){2,}', re.I)


def _etiquetas_negrita(texto, crudo):
    """Líneas que empiezan con una etiqueta en negrita y siguen con la explicación:
    "**Copias rápidas:** detecta los archivos nuevos". Una etiqueta sola en su línea
    ("**Nota:**") es costumbre humana y no cuenta. Tres o más: 14 de 39 borradores de
    IA, 0 de 51 textos humanos."""
    n = len(_ETIQUETA.findall(crudo)) + len(_ETIQUETA_HTML.findall(crudo))
    return f'{n} líneas empiezan con una etiqueta en negrita' if n >= 3 else None


def _separadores(texto, crudo):
    n = len(re.findall(r'^\s*(?:---|\*\*\*|___)\s*$', crudo, re.M))
    # La cabecera YAML de arriba también usa ---: esa no cuenta.
    if re.match(r'\A---\n.*?\n---\n', crudo, re.S):
        n -= 2
    return f'{n} separadores --- entre secciones' if n >= 2 else None


def _flechas(texto, crudo):
    n = len(re.findall(r'^\s*(?:→|➡️?|➜|👉|✅|✔️?)\s', crudo, re.M))
    return f'{n} viñetas hechas con flechas o emojis' if n >= 2 else None


def _titulo_emoji(texto, crudo):
    t = re.findall(r'^\s{0,3}#{1,6}\s*[\U0001F300-\U0001FAFF☀-➿]', crudo, re.M)
    return f'{len(t)} títulos que empiezan con emoji' if t else None


PUNTUACION = [
    (_etiquetas_negrita, 'etiquetas en negrita al empezar cada línea'),
    (_separadores, 'separadores --- entre secciones'),
    (_flechas, 'viñetas con flechas o emojis'),
    (_titulo_emoji, 'títulos con emoji'),
]

TRIOS = [
    # La serie que repite la misma palabra para marcar ritmo: "sin planillas, sin
    # cuadernos y sin perder mesas". Una lista normal de tres cosas NO cuenta: en el
    # corpus, "X, Y y Z" salió en 10 de 39 textos de IA y en 15 de 51 humanos.
    # Tres elementos, y los dos primeros separados por coma o punto: "sin batería y
    # sin cargador" o "cuanto más tardas, más pagas" son español de toda la vida.
    (r'(?<!cuanto )(?<!mientras )(?<!\w)(sin|m[aá]s|menos|cero|nada de)\s+[^.,;!?]{1,30}?[,.;]\s*'
     r'\1\s+[^.,;!?]{1,30}?(?:[,.;]\s*|\s+(?:y|e|ni)\s+)\1\s+\w',
     'serie que repite "sin", "más" o "menos"'),
]

# Prueba sin respaldo: una cifra junto a un sustantivo de prueba social. Es la única
# equivocación que no tiene vuelta atrás, así que aquí importa más no dejar pasar
# nada que no avisar de más. Con una cifra real y demostrable, --allow-proof la
# deja como aviso y no resta.
PRUEBA_SUSTANTIVOS = [
    'usuarios', 'usuarias', 'clientes', 'empresas', 'negocios', 'restaurantes', 'tiendas',
    'profesionales', 'suscriptores', 'seguidores', 'emprendedores', 'alumnos', 'alumnas',
    'estudiantes', 'miembros', 'descargas', 'pymes', 'autónomos', 'marcas', 'comercios',
    'reseñas', 'opiniones', 'valoraciones', 'equipos', 'creadores', 'agencias',
]
PRUEBA = re.compile(
    # Cifra con separadores de miles o decimales, sin tragarse un punto final: un
    # número y su sustantivo viven en la misma frase.
    r'(?<![\w.,])((?:más de |mas de |\+\s?)?\d[\d.,]*(?<![.,])\s*(?:mil|k|M)?\s*\+?'
    r'|miles de|cientos de|millones de)\s+'
    r'(?:(?:de\s+)?[a-záéíóúñ]+\s+){0,1}'
    r'(' + '|'.join(PRUEBA_SUSTANTIVOS) + r')' + E,
    re.I)

# Avisos: patrones conocidos que el corpus todavía no respalda. Se imprimen para
# que una persona los mire, pero no restan puntos.
def _raya_pausa(texto, crudo):
    m = re.findall(r'[a-záéíóúñ,] (?:—|–) [a-záéíóúñ]|[a-záéíóúñ]—[a-záéíóúñ]', texto)
    return f'{len(m)} rayas usadas como pausa' if m else None


def _sin_apertura(texto, crudo):
    malas = [f for f in frases(texto)
             if (f.endswith('?') and '¿' not in f) or (f.endswith('!') and '¡' not in f)]
    return f'{len(malas)} preguntas o exclamaciones sin ¿ o ¡' if malas else None


def _title_case(texto, crudo):
    t = titulos_en_mayusculas(crudo)
    return f'{len(t)}: "{t[0][:40]}"' if t else None


def _punto_y_coma(texto, crudo):
    n = texto.count(';')
    return f'{n} punto y coma' if n > max(3, len(texto) // 1200) else None


AVISOS = [
    (_raya_pausa, 'raya como pausa a la inglesa'),
    (_sin_apertura, 'falta el signo de apertura'),
    (_title_case, 'títulos con Mayúscula En Cada Palabra'),
    (_punto_y_coma, 'muchos punto y coma'),
    (r'(?:^|[.!?¡"]\s*)imag[ií]n(?:a|ate|emos)\b', 'el arranque "imagina..."'),
    (r'en conclusi[oó]n|en resumen|en definitiva|para concluir', 'cierre de redacción escolar'),
    (r'cuando se trata de|al final del d[ií]a|hoy (?:en d[ií]a|m[aá]s que nunca)|'
     r'en (?:el mundo|la sociedad) (?:actual|de hoy|acelerado)|en la era (?:digital|de)',
     'muletilla de redacción'),
    (r'(?:es|resulta) (?:importante|fundamental|crucial|esencial|clave) '
     r'(?:destacar|se[nñ]alar|recordar|tener en cuenta|mencionar|subrayar)|cabe (?:destacar|mencionar|se[nñ]alar)',
     '"es importante destacar"'),
    (r'(?:es|son) (?:mucho )?m[aá]s que (?:un|una) ', '"es más que un X"'),
    (r'(?<!\w)no (?:es|son|era|eran|fue) (?:(?! y no )[^.!?,]){1,50}?, (?:es|son|era|eran|fue) ',
     'contraste con coma "no es X, es Y"'),
    (r'¿(?:el|la|lo) (?:resultado|respuesta|mejor|peor|clave|secreto|truco|problema|motivo|raz[oó]n)\?',
     'pregunta que se responde sola ("¿el resultado?")'),
    (r'podr[ií]an? potencialmente|posiblemente podr[ií]a|quiz[aá]s? podr[ií]a', 'rodeos apilados'),
    (r'hac(?:e|er|en) sentido|tom(?:a|ar|[oó]) lugar|jug(?:ar|ando|ó) un rol|en orden de (?:poder|lograr)',
     'calco del inglés'),
    (r'desbloque(?:a|ar|ará)\w* (?:tu|el|todo su|su) (?:potencial|poder)|(?:siguiente|otro) nivel|'
     r'cambi(?:a|ar) las reglas del juego|de vanguardia|revolucionari[oa]s?',
     'promesa de folleto'),
    (r'(?:en|desde) un (?:solo|[uú]nico) lugar|todo en uno', '"todo en un solo lugar"'),
    (r'¡?y listo!?|tip extra|mira este truco', '"y listo" / "tip extra"'),
    # Estos dos restaban con el corpus a medias y bajaron del criterio con el corpus
    # completo: "te ayuda a" salió en 3 borradores de IA y en 1 texto humano, y la
    # frase que anuncia, en 1 borrador.
    (r'(?<!\w)(?:te|les?|nos|os) ayuda(?:r[aá]n?|n)? a|puede(?:n)? ayudarte|podemos ayudarte',
     '"te ayuda a" / "puede ayudarte"'),
    (r'(?:^|[.!?¿¡"]\s*)(?:y )?lo (?:peor|mejor|m[aá]s (?:curioso|interesante|loco)) '
     r'(?:no (?:es|era)|viene|vino|es que|de todo)',
     'frase que anuncia en lugar de decir ("lo mejor viene ahora")'),
]


# ── lectura del texto ───────────────────────────────────────────────────────

def normaliza(t):
    """Pasa las variantes tipográficas a las formas simples que buscan las reglas.

    El espacio duro no es un espacio y el apóstrofo curvo no es el recto. La raya y
    la semirraya NO se tocan: son justo lo que mira la regla de puntuación.
    """
    t = (t.replace('‑', '-').replace('\xa0', ' ').replace(' ', ' ')
          .replace('’', "'").replace('‘', "'")
          .replace('“', '"').replace('”', '"'))
    # Caracteres invisibles que algunos modelos dejan como marca de agua.
    t = re.sub(r'[​-‍⁠﻿]', '', t)
    return re.sub(r'\s+', ' ', t).strip()


def _quita_entre(t, apertura, cierre):
    """Quita cada bloque desde `apertura` hasta `cierre`, en tiempo lineal.

    Con una regex perezosa (<!--.*?-->), un archivo con miles de aperturas sin cerrar
    tardaba segundos o minutos: cada apertura volvía a recorrer el resto del texto. Un
    archivo hecho a propósito podía dejar colgado un CI. Sin cierre, se quita hasta el
    final, como hace un navegador con un comentario sin cerrar.
    """
    low = t.lower()
    patron = re.compile(apertura)
    out, i = [], 0
    while True:
        m = patron.search(low, i)
        if not m:
            out.append(t[i:])
            break
        out.append(t[i:m.start()])
        k = low.find(cierre, m.end())
        if k < 0:
            break
        out.append(' ')
        fin = low.find('>', k) if cierre.startswith('</') else k + len(cierre) - 1
        i = len(t) if fin < 0 else fin + 1
    return ''.join(out)


def visible_text(html):
    """Lo que de verdad lee quien visita la página."""
    t = _quita_entre(html, r'<script\b', '</script')
    t = _quita_entre(t, r'<style\b', '</style')
    t = _quita_entre(t, r'<!--', '-->')
    # Cada bloque es su propia frase: unidos, dos títulos se leerían como una sola.
    t = re.sub(r'</?(?:h[1-6]|p|li|div|br|tr|td|th|section|article|header|footer|button)\b[^>]*>',
               ' . ', t, flags=re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = normaliza(_html.unescape(t))
    return re.sub(r'(?:\s*\.\s*){2,}', ' . ', t).strip(' .')


def lee_utf8(path):
    """Lee siempre en UTF-8, diga lo que diga la configuración del equipo.

    Con la codificación local (cp1252 en un Windows de fábrica) las tildes, la ñ y
    los signos ¿ ¡ llegan rotos y las reglas se quedan ciegas sin avisar.
    """
    return open(path, encoding='utf-8', errors='replace').read()


def markdown_prose(md):
    """La prosa de un Markdown, sin los ejemplos.

    Un literal no es texto publicado. Un README que documenta "potenciar" no lo
    usa, lo cita. Así que salen: la cabecera YAML, los bloques de código, el código
    en línea, el texto tachado, las imágenes y las URLs. El texto de los enlaces se
    queda, porque se lee como parte de la frase.
    """
    md = re.sub(r'\A---\n.*?\n---\n', ' ', md, count=1, flags=re.S)
    md = re.sub(r'```.*?```', ' ', md, flags=re.S)
    md = re.sub(r'~~~.*?~~~', ' ', md, flags=re.S)
    md = _quita_entre(md, r'<!--', '-->')
    md = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' . ', md)
    md = re.sub(r'\[([^\]\[\n]{0,500})\]\([^)\s]{0,2000}\)', r'\1', md)
    md = re.sub(r'https?://\S+', ' enlace ', md)
    # Sustitutos, no borrados: quitar el ejemplo a secas soldaría dos trozos de la
    # frase y podría inventar un patrón que nadie escribió.
    md = re.sub(r'`[^`\n]*`', ' eso ', md)
    md = re.sub(r'~~.*?~~', ' eso ', md, flags=re.S)
    # Títulos, viñetas, citas y celdas son textos separados, no una frase larga.
    md = re.sub(r'^\s{0,3}#{1,6}\s*(.*)$', r' . \1 . ', md, flags=re.M)
    md = re.sub(r'^\s*(?:[-*+•→]|\d+[.)])\s+', ' . ', md, flags=re.M)
    md = re.sub(r'^\s*>\s?', ' . ', md, flags=re.M)
    md = re.sub(r'\|', ' . ', md)
    md = re.sub(r'<[^>]+>', ' ', md)
    md = re.sub(r'(?<!\w)[*_]+|[*_]+(?!\w)', ' ', md)
    t = normaliza(_html.unescape(md))
    return re.sub(r'(?:\s*\.\s*){2,}', ' . ', t).strip(' .')


# Palabras de función: en español van en minúscula dentro de un título. Una "Con" o
# un "Tu" en mayúscula a mitad de título es el Title Case del inglés, y los nombres
# propios casi nunca son palabras de función, así que "Universidad de Alicante" pasa.
FUNCION = {'de', 'del', 'la', 'las', 'el', 'los', 'un', 'una', 'unos', 'unas', 'y', 'e',
           'o', 'u', 'con', 'sin', 'para', 'por', 'en', 'a', 'al', 'tu', 'tus', 'su', 'sus',
           'mi', 'mis', 'que', 'se', 'te', 'lo', 'como', 'más', 'desde', 'hasta', 'sobre',
           'entre', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'ni', 'pero', 'según'}


def titulos_en_mayusculas(crudo):
    """Títulos de Markdown o HTML escritos en Title Case a la inglesa."""
    titulos = re.findall(r'^\s{0,3}#{1,6}\s*(.+)$', crudo, re.M)
    titulos += re.findall(r'<h[1-6]\b[^>]*>(.*?)</h[1-6]>', crudo, re.S | re.I)
    malos = []
    for t in titulos:
        t = re.sub(r'<[^>]+>|[*_`]', '', t).strip()
        pal = re.findall(r'[A-Za-zÁÉÍÓÚÑÜáéíóúñü]+', t)
        if len(pal) < 3:
            continue
        # Después de dos puntos, de un signo de apertura o de un punto empieza
        # otra frase y la mayúscula es correcta.
        inicios = {m.group(1) for m in re.finditer(r'[:¿¡.]\s*([A-Za-zÁÉÍÓÚÑáéíóúñ]+)', t)}
        if any(w[0].isupper() and not w.isupper() and w.lower() in FUNCION
               and w not in inicios for w in pal[1:]):
            malos.append(t)
    return malos


def frases(texto):
    return [f for f in re.split(r'(?<=[.!?])\s+', texto) if f]


# ── la auditoría ────────────────────────────────────────────────────────────

def audit(texto, crudo=None):
    """Devuelve las coincidencias por categoría.

    `texto` es la prosa ya limpia. `crudo` es el original (Markdown o HTML), para
    las reglas de formato que miran negritas, separadores o títulos.
    """
    crudo = crudo if crudo is not None else texto
    hits = {'vocab': [], 'frases': [], 'puntuacion': [], 'trios': [], 'prueba': [],
            'avisos': []}
    low = texto.lower()

    for rx, etiqueta in VOCAB:
        n = len(re.findall(B + '(?:' + rx + ')' + E, low))
        if n:
            hits['vocab'].append((etiqueta, n))

    for rx, etiqueta in FRASES:
        n = len(re.findall(rx, low, re.M))
        if n:
            hits['frases'].append((etiqueta, n))

    for fn, etiqueta in PUNTUACION:
        r = fn(texto, crudo)
        if r:
            hits['puntuacion'].append((etiqueta, r))

    for rx, etiqueta in TRIOS:
        for m in re.finditer(rx, low):
            hits['trios'].append((etiqueta, m.group(0)[:60]))

    for m in PRUEBA.finditer(texto):
        hits['prueba'].append(m.group(0).strip())

    for regla, etiqueta in AVISOS:
        r = regla(texto, crudo) if callable(regla) else len(re.findall(regla, low, re.M))
        if r:
            hits['avisos'].append((etiqueta, r))

    return hits


TITULOS = {
    'vocab': 'Vocabulario',
    'frases': 'Patrones de frase',
    'puntuacion': 'Puntuación y formato',
    'trios': 'Tríos',
    'prueba': 'Prueba sin respaldo',
    'avisos': 'Avisos (no restan: el corpus aún no los respalda)',
}


def puntua(hits, allow_proof=False):
    pesos = {'vocab': 1, 'frases': 1, 'puntuacion': 1, 'trios': 1, 'prueba': 1, 'avisos': 0}
    if allow_proof:
        # La única regla que una regex no puede juzgar: ve una cifra al lado de un
        # sustantivo, no si la puedes demostrar. --allow-proof sigue mostrándola,
        # pero no deja que una cifra cierta bloquee el texto para siempre.
        pesos['prueba'] = 0
    return max(0, 5 - sum(pesos[k] for k, v in hits.items() if v))


def report(hits, allow_proof=False):
    score = puntua(hits, allow_proof)
    for k in ('prueba', 'frases', 'vocab', 'puntuacion', 'trios', 'avisos'):
        if not hits[k]:
            continue
        titulo = TITULOS[k]
        if k == 'prueba' and allow_proof:
            titulo += ' (aviso: --allow-proof)'
        print(f'  {titulo}:')
        for item in hits[k][:8]:
            if isinstance(item, tuple):
                print(f'    · {item[0]}  ({item[1]})')
            else:
                print(f'    · {item}')
        if len(hits[k]) > 8:
            print(f'    · …y {len(hits[k]) - 8} más')
    print(f'\n  nota {score}/5', end='  ')
    print('LIMPIO' if score == 5 else 'necesita limpieza')
    return score


def main(argv):
    # Leer bien UTF-8 significa que llegan tildes y emojis al print(), y una consola
    # de Windows en cp1252 se rompería con un error. Mejor reemplazar que fallar.
    try:
        sys.stdout.reconfigure(errors='replace')
    except (AttributeError, ValueError):
        pass

    args = list(argv)
    if not args:
        sys.exit(__doc__)
    allow_proof = '--allow-proof' in args
    args = [a for a in args if a != '--allow-proof']
    as_md = '--markdown' in args
    args = [a for a in args if a != '--markdown']
    if not args:
        sys.exit(__doc__)

    if args[0] == '--text':
        crudo = ' '.join(args[1:])
        texto = markdown_prose(crudo) if as_md else normaliza(crudo)
    elif args[0].lower().endswith(('.md', '.markdown', '.txt')) or as_md:
        try:
            crudo = lee_utf8(args[0])
        except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
            sys.exit(f'deslop_es: no puedo leer {args[0]}: {e.strerror}')
        texto = markdown_prose(crudo)
    else:
        try:
            crudo = lee_utf8(args[0])
        except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
            sys.exit(f'deslop_es: no puedo leer {args[0]}: {e.strerror}')
        if '--view' in args:
            i = args.index('--view')
            if i + 1 >= len(args):
                sys.exit('deslop_es: --view necesita un id')
            vid = args[i + 1]
            ini = crudo.find(f'id="{vid}"')
            if ini < 0:
                sys.exit(f'deslop_es: no hay ningún elemento con id "{vid}"')
            sig = crudo.find('id="view-', ini + 1)
            crudo = crudo[ini:sig if sig > 0 else len(crudo)]
        texto = visible_text(crudo)

    # Nada que puntuar es un fallo, no un aprobado. Una limpieza que se corta deja
    # un archivo vacío, y darlo por LIMPIO justo cuando el proceso se rompió sería
    # mentir en el peor momento.
    if not texto.split():
        sys.exit('deslop_es: no hay texto visible que puntuar, la entrada está vacía')

    print(f'{len(texto.split())} palabras de texto visible\n')
    return 0 if report(audit(texto, crudo), allow_proof) == 5 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
