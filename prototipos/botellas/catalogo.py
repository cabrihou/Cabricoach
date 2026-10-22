#!/usr/bin/env python3
"""Genera el catalogo de 200 niveles (un solo camino, v4) con jsc en paralelo.

Uso (desde esta carpeta):
    python3 catalogo.py              # los 200, en 10 procesos
    python3 catalogo.py --procs 6

Escribe niveles.json (compacto) e INFORME-NIVELES.md. Es repetible: el motor es determinista por
semilla y modo, y el resultado se ordena por ruta y nivel sin importar que proceso termino primero.
Solo usa la biblioteca estandar de python.
"""
import json, os, subprocess, sys, time, datetime
from concurrent.futures import ThreadPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'


def generar_uno(L):
    r = subprocess.run([JSC, 'motor.js', 'generar-catalogo.js', '--', str(L), str(L)],
                       cwd=AQUI, capture_output=True, text=True)
    lineas = [x for x in r.stdout.splitlines() if x.startswith('{')]
    if r.returncode != 0 or not lineas:
        raise RuntimeError('fallo %d: %s %s' % (L, r.stdout[-300:], r.stderr[-300:]))
    return L, json.loads(lineas[-1])


def colores(n):
    return len({c for b in n['botellas'] for c in b})


DIFS = ['facil', 'normal', 'dificil', 'muy', 'extra']
NOMBRES = {'facil': 'Facil', 'normal': 'Normal', 'dificil': 'Dificil', 'muy': 'Muy dificil', 'extra': 'Extra dificil'}
# Franjas de la RECETA del motor (motor.js): bot = [min, max], atasco = minimo. Deben coincidir con RECETA.
FRANJAS = {'facil': ([0.55, 1], 0), 'normal': ([0.1, 0.599], 0), 'dificil': ([0, 0.249], 0.3),
           'muy': ([0, 0.05], 0.5), 'extra': ([0, 0], 0.65)}
DUROS = ('dificil', 'muy', 'extra')


def en_franja(n):
    (lo, hi), at = FRANJAS[n['dif']]
    return lo <= n['bot'] <= hi and n['atasco'] >= at
NIVELES = 200


def main():
    args = sys.argv[1:]
    procs = int(args[args.index('--procs') + 1]) if '--procs' in args else 10
    t0 = time.time()
    res, segs = {}, {}
    with ThreadPoolExecutor(max_workers=procs) as ex:
        for i, (L, d) in enumerate(ex.map(generar_uno, range(NIVELES, 0, -1))):
            segs[L] = d.pop('_seg')
            res[L] = d
            if (i + 1) % 50 == 0:
                print('  %d/%d (%.0f s)' % (i + 1, NIVELES, time.time() - t0), flush=True)
    total = time.time() - t0
    camino = [res[L] for L in range(1, NIVELES + 1)]
    resumen = tabla_resumen(camino)
    print(resumen)
    print('catalogo: %.0f s de reloj, %.0f s de CPU sumada, nivel mas lento %.1f s' % (total, sum(segs.values()), max(segs.values())))
    ruta_json = os.path.join(AQUI, 'niveles.json')
    generado = datetime.date.today().isoformat()
    try:
        previo = json.load(open(ruta_json))
        if previo.get('camino') == camino:
            generado = previo.get('generado', generado)  # igual al anterior: no cambia ni la fecha
    except Exception:
        pass
    with open(ruta_json, 'w') as f:
        json.dump({'version': 5, 'generado': generado, 'camino': camino}, f, separators=(',', ':'), ensure_ascii=False)
    print('niveles.json: %.1f KB' % (os.path.getsize(ruta_json) / 1024))
    informe(camino, segs, resumen, total)


def tabla_resumen(camino):
    filas = ['| Dificultad | Niveles | En su franja | Meta prom | Bot prom | Atasco prom | Colores | Llave | Candado | Cajon de 2 | Colores nuevos | Misterio | Largas | Gigante | No optimos |',
             '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for d in DIFS:
        lista = [n for n in camino if n['dif'] == d]
        if not lista:
            continue
        cs = [colores(n) for n in lista]
        cuenta = lambda t: sum(1 for n in lista if t in n['rasgos'])
        filas.append('| %s | %d | %d (%.0f %%) | %.1f | %.3f | %.3f | %d a %d | %d | %d | %d | %d | %d | %d | %d | %d |' % (
            NOMBRES[d], len(lista), sum(1 for n in lista if en_franja(n)), 100.0 * sum(1 for n in lista if en_franja(n)) / len(lista),
            sum(n['meta'] for n in lista) / len(lista), sum(n['bot'] for n in lista) / len(lista),
            sum(n['atasco'] for n in lista) / len(lista), min(cs), max(cs),
            cuenta('llave'), cuenta('candado'), sum(1 for n in lista if any(len(x['bots']) == 2 for x in n['cajas'])),
            sum(1 for n in lista if n['nuevos']), cuenta('misterio'), cuenta('largas'), cuenta('gigante'),
            sum(1 for n in lista if not n['optimo'])))
    return '\n'.join(filas)


def reparto(camino):
    filas = ['| Tramo | Facil | Normal | Dificil | Muy dificil | Extra dificil | Duros |', '|---|---|---|---|---|---|---|']
    for a in range(0, NIVELES, 50):
        ch = camino[a:a + 50]
        cuenta = [sum(1 for n in ch if n['dif'] == d) for d in DIFS]
        duros = sum(1 for n in ch if n['dif'] in DUROS)
        filas.append('| L%d-%d | %s | %d (%.0f %%) |' % (a + 1, a + 50, ' | '.join(str(c) for c in cuenta), duros, 100.0 * duros / len(ch)))
    duros = sum(1 for n in camino if n['dif'] in DUROS)
    d81 = sum(1 for n in camino[80:] if n['dif'] in DUROS)
    pm = next((n['L'] for n in camino if n['dif'] == 'muy'), None)
    px = next((n['L'] for n in camino if n['dif'] == 'extra'), None)
    filas.append('| Total | %s | %d (%.0f %%) |' % (' | '.join(str(sum(1 for n in camino if n['dif'] == d)) for d in DIFS), duros, 100.0 * duros / len(camino)))
    filas += ['', 'Duros desde L81: %d de %d (%.0f %%). Primer Muy: L%s. Primer Extra: L%s.' % (d81, len(camino) - 80, 100.0 * d81 / (len(camino) - 80), pm, px)]
    return '\n'.join(filas)


def informe(camino, segs, resumen, total):
    o = ['# Informe de niveles (camino de 200)', '',
         'Generado por `catalogo.py` (modo catalogo del motor). `bot` = fraccion de 40 partidas que gana el jugador',
         'medio-aleatorio (en el catalogo y en vivo; 40 y 20 partidas); `atasco` = fraccion que termino sin jugadas. Tiempo total de reloj: %.0f s.' % total, '',
         '## Resumen por dificultad', '', resumen, '',
         '## Reparto por tramo de 50 niveles', '', reparto(camino), '',
         '## Franjas de la receta (motor.js, RECETA)', '',
         '| Grado | bot (gana el jugador simulado) | atasco minimo |', '|---|---|---|'] + [
         '| %s | %s | %s |' % (NOMBRES[d], '%g a %g' % tuple(FRANJAS[d][0]), '%g' % FRANJAS[d][1]) for d in DIFS] + ['',
         '## Meta promedio por tramo de 20 niveles (niveles de esa dificultad en el tramo entre parentesis)', '',
         '| Tramo | Facil | Normal | Dificil | Muy dificil | Extra dificil | Todos |', '|---|---|---|---|---|---|---|']
    for a in range(0, NIVELES, 20):
        ch = camino[a:a + 20]
        celdas = []
        for d in DIFS:
            x = [n['meta'] for n in ch if n['dif'] == d]
            celdas.append('%.1f (%d)' % (sum(x) / len(x), len(x)) if x else '-')
        o.append('| L%d-%d | %s | %.1f |' % (a + 1, a + 20, ' | '.join(celdas), sum(n['meta'] for n in ch) / len(ch)))
    o += ['', '## Todos los niveles', '',
          '| L | Dif | Colores | Botellas | Rasgos | Meta | Optimo | Bot | Atasco | En franja | Seg |', '|---|---|---|---|---|---|---|---|---|---|---|']
    for n in camino:
        o.append('| %d | %s | %d | %d | %s | %d | %s | %.3f | %.3f | %s | %.1f |' % (
            n['L'], n['dif'], colores(n), len(n['botellas']), ', '.join(n['rasgos']) or '-', n['meta'],
            'si' if n['optimo'] else 'no', n['bot'], n['atasco'], 'si' if en_franja(n) else 'no', segs[n['L']]))
    with open(os.path.join(AQUI, 'INFORME-NIVELES.md'), 'w') as f:
        f.write('\n'.join(o))


if __name__ == '__main__':
    main()
