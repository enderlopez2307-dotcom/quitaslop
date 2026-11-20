#!/usr/bin/env python3
"""Conjunto de control humano: textos que NO se miraron al elegir las reglas.
Sirve para medir el checker fuera de la muestra con la que se construyó."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import fetch_humano as F

F.OUT = os.path.join(os.path.dirname(__file__), '..', 'humano-control')
os.makedirs(F.OUT, exist_ok=True)
usadas = {l.split('\t')[5] for l in open(os.path.join(os.path.dirname(__file__), '..',
          'fuentes-humano.tsv'), encoding='utf-8').read().splitlines()[1:] if l}
filas = []


def por_titulos(site, titulos, prefijo, lic, region, formato):
    n = 1
    for t in titulos:
        rev = F.revision_previa(site, t)
        if not rev:
            continue
        url = f'https://{site}/w/index.php?oldid={rev["revid"]}'
        if url in usadas:
            continue
        try:
            cuerpo = F.texto(site, rev['revid'])
        except Exception as e:
            print('  error', t, e); continue
        if F.guarda(f'{prefijo}-{n:02d}', site, t, rev, cuerpo, lic, region, formato, filas):
            print(f'{prefijo}-{n:02d}', t, len(cuerpo.split())); n += 1
        F.time.sleep(2)


S, W = 'CC BY-SA 3.0', 'CC BY 2.5'
por_titulos('es.wikivoyage.org', ['Guadalajara (México)', 'Cartagena de Indias', 'Quito', 'Arequipa'],
            'control-viaje-latam', S, 'latam', 'guia-viaje')
por_titulos('es.wikivoyage.org', ['Málaga', 'Córdoba (España)', 'Segovia', 'Oviedo'],
            'control-viaje-espana', S, 'espana', 'guia-viaje')
d = F.api('es.wikinews.org', action='query', list='categorymembers', cmtitle='Categoría:Ecuador',
          cmlimit=20, cmnamespace=0, cmtype='page', cmsort='timestamp', cmdir='desc')
t1 = [m['title'] for m in d['query']['categorymembers']][:3]
d = F.api('es.wikinews.org', action='query', list='categorymembers', cmtitle='Categoría:Andalucía',
          cmlimit=20, cmnamespace=0, cmtype='page', cmsort='timestamp', cmdir='desc')
t2 = [m['title'] for m in d['query']['categorymembers']][:3]
por_titulos('es.wikinews.org', t1, 'control-noticia-latam', W, 'latam', 'noticia')
por_titulos('es.wikinews.org', t2, 'control-noticia-espana', W, 'espana', 'noticia')
with open(os.path.join(os.path.dirname(__file__), '..', 'fuentes-humano-control.tsv'), 'w',
          encoding='utf-8') as f:
    f.write('nombre\tformato\tregion\tlicencia\trevision\turl\n')
    for r in filas:
        f.write(r + '\n')
