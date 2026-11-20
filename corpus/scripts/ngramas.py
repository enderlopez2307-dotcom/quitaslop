#!/usr/bin/env python3
"""Descubre candidatos sin adivinar: n-gramas que salen en muchos borradores de IA
y en casi ningún texto humano. La lista sale del corpus, no de la intuición."""
import re, sys, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from medir import carga

def ngr(t, n):
    w = re.findall(r'[a-záéíóúñü¿¡]+', t.lower())
    return {' '.join(w[i:i + n]) for i in range(len(w) - n + 1)}

ia, hu = carga('ia'), carga('humano')
for n in (1, 2, 3):
    ca, ch = collections.Counter(), collections.Counter()
    for _, _, p in ia: ca.update(ngr(p, n))
    for _, _, p in hu: ch.update(ngr(p, n))
    filas = [(g, a, ch[g]) for g, a in ca.items() if a >= (6 if n == 1 else 4) and ch[g] <= 1]
    filas.sort(key=lambda x: (-x[1], x[2]))
    print(f'\n== {n}-gramas (IA ≥ umbral, humanos ≤ 1) ==')
    print('  '.join(f'{g} {a}/{h}' for g, a, h in filas[:70]))
