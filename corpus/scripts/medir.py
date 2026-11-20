#!/usr/bin/env python3
"""Mide cada patrón candidato contra el corpus: ¿en cuántos borradores de IA
aparece y en cuántos textos humanos?

    python3 corpus/scripts/medir.py            # tabla de candidatos
    python3 corpus/scripts/medir.py --final    # puntuación del checker final

Cada texto se recorta a sus primeras TOPE palabras de prosa, en los dos lados,
para que un artículo humano largo no tenga más ocasiones de fallar que un
correo corto de IA.
"""
import glob, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, '..', '..')
sys.path.insert(0, os.path.join(RAIZ, 'tools'))
sys.path.insert(0, AQUI)

import deslop_es as D            # noqa: E402
import candidatos as C           # noqa: E402

TOPE = 700


def recorta(t, n=TOPE):
    pal = t.split()
    if len(pal) <= n:
        return t
    t = ' '.join(pal[:n])
    corte = max(t.rfind('. '), t.rfind('? '), t.rfind('! '))
    return t[:corte + 1] if corte > 0 else t


def carga(lado):
    docs = []
    for p in sorted(glob.glob(os.path.join(RAIZ, 'corpus', lado, '*.md'))):
        crudo = open(p, encoding='utf-8').read()
        if not crudo.split():
            continue
        prosa = recorta(D.markdown_prose(crudo))
        docs.append((os.path.basename(p)[:-3], crudo, prosa))
    return docs


def dispara(cat, rx, crudo, prosa):
    if cat == 'punct':
        return bool(re.search(rx, prosa, re.M))
    if cat == 'trios' and rx.startswith('(?:(?:^'):
        return bool(re.search(rx, prosa))
    return bool(re.search(rx, prosa.lower(), re.M))


def candidatos():
    for i, rx in C.VOCAB:
        yield 'vocab', i, C.B + '(?:' + rx + ')' + C.E
    for i, rx in C.PHRASES:
        yield 'frases', i, rx
    for i, rx in C.PUNCT:
        yield 'punct', i, rx
    for i, rx in C.TRIOS:
        yield 'trios', i, rx
    yield 'prueba', 'número junto a un sustantivo', C.PROOF
    for n in C.PROOF_NOUNS:
        yield 'prueba', f'  · {n}', (r'(?<![\w.,])(\d[\d.,]*\s*(?:mil|k)?\+?|miles de|cientos de|'
                                    r'millones de)\s+(?:[a-záéíóúñ]+\s+){0,1}' + n + r'(?!\w)')


def estructurales(crudo, prosa):
    """Señales que no son una regex sobre la prosa."""
    r = {}
    r['punto y coma > 2'] = prosa.count(';') > 2
    preg = [s for s in re.split(r'(?<=[.!?])\s+', prosa) if s.endswith('?')]
    r['pregunta sin ¿'] = any('¿' not in s for s in preg)
    excl = [s for s in re.split(r'(?<=[.!?])\s+', prosa) if s.endswith('!')]
    r['exclamación sin ¡'] = any('¡' not in s for s in excl)
    r['títulos en Mayúsculas'] = bool(D.titulos_en_mayusculas(crudo))
    r['etiquetas en negrita ≥3'] = len(re.findall(r'^\s*(?:[-*+]|\d+\.)?\s*\*\*[^*\n]{2,40}:?\*\*:?', crudo, re.M)) >= 3
    r['título con emoji'] = bool(re.search(r'^\s{0,3}#{1,6}\s*[\U0001F300-\U0001FAFF\u2600-\u27BF]', crudo, re.M))
    r['separadores --- ≥2'] = len(re.findall(r'^\s*(?:---|\*\*\*)\s*$', crudo, re.M)) >= 2
    r['flechas → como viñetas ≥2'] = len(re.findall(r'^\s*(?:→|➡|➜|✅|✔|👉)', crudo, re.M)) >= 2
    r['emojis ≥3'] = len(re.findall(r'[\U0001F300-\U0001FAFF☀-➿]', crudo)) >= 3
    return r


def fisher(a, na, h, nh):
    """p de una cola de la prueba exacta de Fisher: probabilidad de ver a o más
    textos de IA con el patrón si IA y humanos lo usaran igual."""
    from math import comb
    k = a + h
    tot = comb(na + nh, k)
    return sum(comb(na, x) * comb(nh, k - x) for x in range(a, min(k, na) + 1)) / tot


def tabla():
    ia, hu = carga('ia'), carga('humano')
    print(f'IA: {len(ia)} textos · humanos: {len(hu)} textos · tope {TOPE} palabras\n')
    print(f'{"cat":7} {"patrón":38} {"IA":>8} {"humano":>8}  quién')
    filas = []
    for cat, i, rx in candidatos():
        a = [n for n, c, p in ia if dispara(cat, rx, c, p)]
        h = [n for n, c, p in hu if dispara(cat, rx, c, p)]
        filas.append((cat, i, len(a), len(h), h, len({x[:2] for x in a})))
    for nombre in estructurales('', '').keys():
        a = [n for n, c, p in ia if estructurales(c, p)[nombre]]
        h = [n for n, c, p in hu if estructurales(c, p)[nombre]]
        filas.append(('estruct', nombre, len(a), len(h), h, len({x[:2] for x in a})))
    for cat, i, a, h, quien, enc in filas:
        print(f'{cat:7} {i[:38]:38} {a:>3}/{len(ia):<4} {h:>3}/{len(hu):<4} enc={enc:<2} p={fisher(a, len(ia), h, len(hu)):.3f} {",".join(quien)[:40]}')


def final():
    ia, hu = carga('ia'), carga('humano')
    out = []
    for lado, docs in (('ia', ia), ('humano', hu)):
        notas = []
        for n, c, p in docs:
            hits = D.audit(p, crudo=c)
            score = D.puntua(hits)
            notas.append((n, score, [k for k, v in hits.items() if v]))
        out.append((lado, notas))
    cats = ['vocab', 'frases', 'puntuacion', 'trios', 'prueba', 'avisos']
    print(f'IA: {len(ia)} textos · humanos: {len(hu)} textos · tope {TOPE} palabras\n')
    print(f'{"categoría":12} {"IA":>8} {"humanos":>8}   p (Fisher, una cola)')
    for k in cats:
        a = sum(1 for n, s_, c in out[0][1] if k in c)
        h = sum(1 for n, s_, c in out[1][1] if k in c)
        print(f'{k:12} {a:>3}/{len(ia):<4} {h:>3}/{len(hu):<4}   {fisher(a, len(ia), h, len(hu)):.2g}')
    a = sum(1 for x in out[0][1] if x[1] < 5); h = sum(1 for x in out[1][1] if x[1] < 5)
    print(f'{"nota < 5/5":12} {a:>3}/{len(ia):<4} {h:>3}/{len(hu):<4}   {fisher(a, len(ia), h, len(hu)):.2g}')
    for lado, notas in out:
        bajo = [x for x in notas if x[1] < 5]
        print(f'\n{lado}: {len(bajo)}/{len(notas)} por debajo de 5/5')
        for n, s, cats in notas:
            print(f'  {s}/5  {n:34} {" ".join(cats)}')
    return out


if __name__ == '__main__' and '--informe' not in sys.argv:
    final() if '--final' in sys.argv else tabla()


def informe():
    """Escribe corpus/MEDICIONES.md con todas las cifras de esta ejecución."""
    import io, contextlib
    ia, hu = carga('ia'), carga('humano')
    L = []
    L.append('# Mediciones del corpus\n')
    L.append('Archivo generado por `python3 corpus/scripts/medir.py --informe`. No se edita a mano.\n')
    L.append(f'Corpus: **{len(ia)} borradores de IA** y **{len(hu)} textos humanos**. Cada texto se '
             f'recorta a sus primeras {TOPE} palabras de prosa en los dos lados.\n')
    fam = {}
    for n, c, p in ia:
        fam.setdefault(n.rsplit('-', 1)[1], []).append(n)
    reg_h = {}
    for linea in open(os.path.join(RAIZ, 'corpus', 'fuentes-humano.tsv'), encoding='utf-8').read().splitlines()[1:]:
        f = linea.split('\t')
        if os.path.exists(os.path.join(RAIZ, 'corpus', 'humano', f[0] + '.md')):
            reg_h.setdefault(f[1], []).append(f[0])
    L.append('Lado IA por familia: ' + ', '.join(f'{k} {len(v)}' for k, v in sorted(fam.items())) + '.\n')
    L.append('Lado humano por formato: ' + ', '.join(f'{k} {len(v)}' for k, v in sorted(reg_h.items())) + '.\n')

    # 1. el checker final
    notas = {}
    for lado, docs in (('ia', ia), ('humano', hu)):
        notas[lado] = [(n, D.puntua(h := D.audit(p, crudo=c)), [k for k, v in h.items() if v]) for n, c, p in docs]
    L.append('\n## 1. El checker tal como está\n')
    L.append('| Categoría | Borradores de IA | Textos humanos | p (Fisher, una cola) |')
    L.append('|---|---|---|---|')
    nombres = {'vocab': 'Vocabulario', 'frases': 'Patrones de frase', 'puntuacion': 'Puntuación y formato',
               'trios': 'Tríos', 'prueba': 'Prueba sin respaldo', 'avisos': 'Avisos (no restan)'}
    for k in ('vocab', 'frases', 'puntuacion', 'trios', 'prueba', 'avisos'):
        a = sum(1 for x in notas['ia'] if k in x[2]); h = sum(1 for x in notas['humano'] if k in x[2])
        L.append(f'| {nombres[k]} | {a} de {len(ia)} | {h} de {len(hu)} | {fisher(a, len(ia), h, len(hu)):.2g} |')
    a = sum(1 for x in notas['ia'] if x[1] < 5); h = sum(1 for x in notas['humano'] if x[1] < 5)
    L.append(f'| **Nota por debajo de 5/5** | **{a} de {len(ia)} ({100*a/len(ia):.0f} %)** | '
             f'**{h} de {len(hu)} ({100*h/len(hu):.0f} %)** | {fisher(a, len(ia), h, len(hu)):.2g} |')
    L.append('\nPor familia de modelos:\n')
    L.append('| Familia | Marcados | Total |')
    L.append('|---|---|---|')
    for k, v in sorted(fam.items()):
        m = sum(1 for x in notas['ia'] if x[0] in v and x[1] < 5)
        L.append(f'| {k} | {m} | {len(v)} |')
    L.append('\nPor región del encargo (lado IA) y de la fuente (lado humano):\n')
    L.append('| Región | IA marcados | Humanos marcados |')
    L.append('|---|---|---|')
    for reg in ('latam', 'espana'):
        ai = [x for x in notas['ia'] if f'-{reg}-' in x[0]]
        hh = [x for x in notas['humano'] if reg in x[0]]
        L.append(f'| {reg} | {sum(1 for x in ai if x[1] < 5)} de {len(ai)} | '
                 f'{sum(1 for x in hh if x[1] < 5)} de {len(hh)} |')
    L.append('\nTextos humanos marcados por error: ' +
             (', '.join(f'`{x[0]}` ({", ".join(c for c in x[2] if c != "avisos")})'
                        for x in notas['humano'] if x[1] < 5) or 'ninguno') + '.\n')
    L.append('Borradores de IA que pasan con 5/5: ' +
             ', '.join(f'`{x[0]}`' for x in notas['ia'] if x[1] == 5) + '.\n')

    # 1b. el conjunto de control, que no se miró al elegir las reglas
    ic, hc = carga('ia-control'), carga('humano-control')
    if ic and hc:
        nc = {lado: [(n, D.puntua(D.audit(p, crudo=c))) for n, c, p in docs]
              for lado, docs in (('ia', ic), ('humano', hc))}
        a = sum(1 for x in nc['ia'] if x[1] < 5); h = sum(1 for x in nc['humano'] if x[1] < 5)
        L.append('\n## 1b. Fuera de la muestra: el conjunto de control\n')
        L.append('Las reglas se eligieron mirando el corpus de arriba, así que esas cifras son las del '
                 'mejor caso. El conjunto de control son encargos y textos nuevos que no se miraron al '
                 'elegir ninguna regla (`corpus/ia-control/`, `corpus/fuentes-humano-control.tsv`).\n')
        L.append('| | Marcados | Total |')
        L.append('|---|---|---|')
        L.append(f'| Borradores de IA | {a} ({100*a/len(ic):.0f} %) | {len(ic)} |')
        L.append(f'| Textos humanos | {h} ({100*h/len(hc):.0f} %) | {len(hc)} |')
        for fam_ in ('claude', 'gemma', 'gpt'):
            v = [x for x in nc['ia'] if x[0].endswith('-' + fam_)]
            L.append(f'| IA, {fam_} | {sum(1 for x in v if x[1] < 5)} | {len(v)} |')
        L.append('\nHumanos marcados en el control: ' +
                 (', '.join(f'`{x[0]}`' for x in nc['humano'] if x[1] < 5) or 'ninguno') + '.\n')

    # 2. todos los candidatos medidos
    L.append('\n## 2. Todos los candidatos medidos\n')
    L.append('Criterio para restar puntos: el patrón sale en 2 borradores de IA o más, de 2 encargos '
             'distintos o más (para que no sea el tema del encargo), y en los textos humanos sale como '
             'mucho en una cuarta parte de esa proporción. Los que no cumplen quedan fuera o pasan a '
             'aviso. "enc." es el número de encargos distintos.\n')
    L.append('| Cat. | Candidato | IA | Humanos | enc. | p |')
    L.append('|---|---|---|---|---|---|')
    for cat, i, rx in candidatos():
        if i.startswith('  ·'):
            continue
        a = [n for n, c, p in ia if dispara(cat, rx, c, p)]
        h = [n for n, c, p in hu if dispara(cat, rx, c, p)]
        L.append(f'| {cat} | {i} | {len(a)} | {len(h)} | {len({x[:2] for x in a})} | '
                 f'{fisher(len(a), len(ia), len(h), len(hu)):.2g} |')
    for nombre in estructurales('', '').keys():
        a = [n for n, c, p in ia if estructurales(c, p)[nombre]]
        h = [n for n, c, p in hu if estructurales(c, p)[nombre]]
        L.append(f'| formato | {nombre} | {len(a)} | {len(h)} | {len({x[:2] for x in a})} | '
                 f'{fisher(len(a), len(ia), len(h), len(hu)):.2g} |')
    open(os.path.join(RAIZ, 'corpus', 'MEDICIONES.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('corpus/MEDICIONES.md escrito')


if __name__ == '__main__' and '--informe' in sys.argv:
    informe()
