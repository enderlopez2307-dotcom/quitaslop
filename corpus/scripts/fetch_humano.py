#!/usr/bin/env python3
"""Descarga el corpus humano: textos en español con licencia abierta, en su
revisión anterior a 2022 (antes de que hubiera borradores de IA por todas partes).

Los textos quedan en corpus/humano/ y NO se suben a git (.gitignore): el repo solo
guarda la lista de fuentes (fuentes-humano.tsv) y las mediciones.
"""
import urllib.error, json, os, re, sys, time, urllib.parse, urllib.request, html

UA = {'User-Agent': 'quitaslop-corpus/0.1 (investigacion de estilo)'}
OUT = os.path.join(os.path.dirname(__file__), '..', 'humano')
CORTE = '2021-12-31T23:59:59Z'


def get(url):
    for intento in range(6):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(10 * (intento + 1))
    raise RuntimeError('demasiados 429')


def api(site, **kw):
    kw.update(format='json', formatversion='2')
    return json.loads(get(f'https://{site}/w/api.php?' + urllib.parse.urlencode(kw)))


def miembros(site, cat, n):
    d = api(site, action='query', list='categorymembers', cmtitle=cat, cmlimit=200,
            cmnamespace=0, cmtype='page')
    return [m['title'] for m in d['query']['categorymembers']][:n * 4]


def revision_previa(site, title):
    d = api(site, action='query', prop='revisions', titles=title, rvlimit=1,
            rvstart=CORTE, rvdir='older', rvprop='ids|timestamp')
    p = d['query']['pages'][0]
    if 'revisions' not in p:
        return None
    return p['revisions'][0]


def texto(site, oldid):
    d = api(site, action='parse', oldid=oldid, prop='text', disablelimitreport=1,
            disableeditsection=1)
    h = d['parse']['text']
    # fuera tablas, referencias, cajas de navegación, plantillas de licencia
    for tag in ('table', 'style', 'script', 'sup', 'figure'):
        h = re.sub(rf'<{tag}\b.*?</{tag}>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<div class="(?:[^"]*(?:navbox|references|reflist|thumb|toc|noprint|metadata|infobox|mw-references)[^"]*)".*?</div>', ' ', h, flags=re.S)
    parrafos = re.findall(r'<(p|li|h2|h3)\b[^>]*>(.*?)</\1>', h, flags=re.S)
    out = []
    for tag, p in parrafos:
        t = html.unescape(re.sub(r'<[^>]+>', '', p)).strip()
        if not t:
            continue
        out.append(('## ' + t) if tag in ('h2', 'h3') else ('- ' + t if tag == 'li' else t))
    return '\n\n'.join(out)


def guarda(nombre, site, title, rev, cuerpo, licencia, region, formato, filas):
    pal = len(cuerpo.split())
    if pal < 150:
        return False
    palabras = cuerpo.split()
    if pal > 900:      # recorte a ~900 palabras, por el final de un párrafo
        cuerpo = ' '.join(palabras[:900])
        cuerpo = cuerpo[:cuerpo.rfind('.') + 1]
    with open(os.path.join(OUT, nombre + '.md'), 'w', encoding='utf-8') as f:
        f.write(cuerpo + '\n')
    filas.append('\t'.join([nombre, formato, region, licencia, rev['timestamp'][:10],
                            f'https://{site}/w/index.php?oldid={rev["revid"]}']))
    return True


def lote(site, cats, n, prefijo, licencia, region, formato, filas):
    hechos = 0
    vistos = set()
    for cat in cats:
        for t in miembros(site, cat, n):
            if hechos >= n:
                return
            if t in vistos:
                continue
            vistos.add(t)
            rev = revision_previa(site, t)
            if not rev:
                continue
            try:
                cuerpo = texto(site, rev['revid'])
            except Exception as e:
                print('  error', t, e, file=sys.stderr)
                continue
            nombre = f'{prefijo}-{hechos + 1:02d}'
            if guarda(nombre, site, t, rev, cuerpo, licencia, region, formato, filas):
                hechos += 1
                print(nombre, t, len(cuerpo.split()))
            time.sleep(2)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    filas = []
    W = 'CC BY 2.5'
    lote('es.wikinews.org', ['Categoría:Argentina', 'Categoría:México', 'Categoría:Chile',
                             'Categoría:Colombia', 'Categoría:Perú'], 7,
         'noticia-latam', W, 'latam', 'noticia', filas)
    lote('es.wikinews.org', ['Categoría:España', 'Categoría:Madrid', 'Categoría:Cataluña'], 7,
         'noticia-espana', W, 'espana', 'noticia', filas)
    S = 'CC BY-SA 3.0'
    lote('es.wikivoyage.org', ['Categoría:Ciudades de México', 'Categoría:Ciudades de Argentina',
                               'Categoría:Ciudades de Colombia', 'Categoría:Ciudades de Chile'], 5,
         'viaje-latam', S, 'latam', 'guia-viaje', filas)
    lote('es.wikivoyage.org', ['Categoría:Ciudades de España', 'Categoría:Ciudades de Andalucía',
                               'Categoría:Ciudades de Castilla y León'], 5,
         'viaje-espana', S, 'espana', 'guia-viaje', filas)
    lote('es.wikibooks.org', ['Categoría:Programación', 'Categoría:Informática',
                              'Categoría:Cocina', 'Categoría:Libros de informática'], 6,
         'tutorial', S, 'mixta', 'tutorial', filas)
    with open(os.path.join(os.path.dirname(__file__), '..', 'fuentes-humano.tsv'), 'a',
              encoding='utf-8') as f:
        for r in filas:
            f.write(r + '\n')
