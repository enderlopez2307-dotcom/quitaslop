#!/usr/bin/env python3
"""Segunda tanda del corpus humano: guías de viaje por título y noticias de más
países latinoamericanos (la primera tanda salió solo de Argentina)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import fetch_humano as F

filas = []


def por_titulos(site, titulos, prefijo, lic, region, formato, desde=1):
    n = desde
    for t in titulos:
        rev = F.revision_previa(site, t)
        if not rev:
            print('  sin revisión', t); continue
        try:
            cuerpo = F.texto(site, rev['revid'])
        except Exception as e:
            print('  error', t, e); continue
        if F.guarda(f'{prefijo}-{n:02d}', site, t, rev, cuerpo, lic, region, formato, filas):
            print(f'{prefijo}-{n:02d}', t, len(cuerpo.split())); n += 1
        F.time.sleep(2)


def recientes(site, cat, k, prefijo, lic, region, formato, desde):
    d = F.api(site, action='query', list='categorymembers', cmtitle=cat, cmlimit=60,
              cmnamespace=0, cmtype='page', cmsort='timestamp', cmdir='asc')
    titulos = [m['title'] for m in d['query']['categorymembers']]
    hechos = 0
    n = desde
    for t in titulos:
        if hechos >= k:
            break
        rev = F.revision_previa(site, t)
        if not rev:
            continue
        try:
            cuerpo = F.texto(site, rev['revid'])
        except Exception as e:
            print('  error', t, e); continue
        if F.guarda(f'{prefijo}-{n:02d}', site, t, rev, cuerpo, lic, region, formato, filas):
            print(f'{prefijo}-{n:02d}', t, len(cuerpo.split())); n += 1; hechos += 1
        F.time.sleep(2)
    return n


S = 'CC BY-SA 3.0'
por_titulos('es.wikivoyage.org', ['Ciudad de México', 'Oaxaca de Juárez', 'Bogotá', 'Medellín',
            'Lima', 'Cuzco', 'Valparaíso', 'Montevideo'], 'viaje-latam', S, 'latam', 'guia-viaje')
por_titulos('es.wikivoyage.org', ['Sevilla', 'Granada', 'Salamanca', 'Bilbao', 'Toledo',
            'Cádiz', 'Santiago de Compostela', 'Zaragoza'], 'viaje-espana', S, 'espana', 'guia-viaje')
W = 'CC BY 2.5'
n = 8
for cat in ['Categoría:México', 'Categoría:Chile', 'Categoría:Colombia', 'Categoría:Perú',
            'Categoría:Venezuela', 'Categoría:Uruguay']:
    n = recientes('es.wikinews.org', cat, 2, 'noticia-latam', W, 'latam', 'noticia', n)

with open(os.path.join(os.path.dirname(__file__), '..', 'fuentes-humano.tsv'), 'a', encoding='utf-8') as f:
    for r in filas:
        f.write(r + '\n')
