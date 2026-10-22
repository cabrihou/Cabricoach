#!/usr/bin/env python3
"""Arma botellas.html (Artifact) y botellas-local.html (prueba local) desde botellas.src.html.

Sin dependencias. Marcadores que reemplaza:
  /*@FUENTES@*/   recursos/fuentes.css
  /*@MOTOR@*/     motor.js
  @IMG:nombre@    data URI de recursos/nombre.b64
  @IMG?:nombre@   igual, pero opcional: si no existe recursos/nombre.b64 queda una cadena vacia (v6: zona1..zona4 y cima)
  /*@NIVELES@*/    const CATALOGO = <niveles.json>; CATALOGO.camino[L-1] (o recursos/niveles-muestra.json si aun no hay un v3)
  /*@TEST@*/      atajo window.__botellas, solo en la version local
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def leer(*ruta):
    with open(os.path.join(AQUI, *ruta), encoding="utf-8") as f:
        return f.read()


# Atajo de prueba: existe solo en botellas-local.html, nunca en el Artifact.
# Aplica la solucion del motor con toques reales (los mismos que daria un dedo).
TEST = r"""
window.__botellas = {
  get G(){ return G; },
  S: () => S,
  motor: MOTOR,
  catalogo: typeof CATALOGO !== 'undefined' ? CATALOGO : null,
  abrir: (m, r, c, o) => abrirJuego(m, r, c, o),
  mapaMs: () => MAPA_MS,
  aviso: () => { const a = document.getElementById('aviso'); if(!a.hidden) a.click(); return true; },
  tocar: (i) => tocar(i),
  libre: async () => { for(let k = 0; k < 400; k++){ if(G && G.estado && !G.busy) return true; await esperar(25); } return false; },
  // cierra la hoja de Novedad si esta abierta (para llegar al tablero)
  novedad: () => { const v = document.getElementById('veloNov'); if(v.classList.contains('on')) document.getElementById('nOk').click(); return true; },
  // juega la solucion del motor desde el estado actual; dejar = cuantos movimientos se dejan sin jugar
  resolver: async (dejar) => {
    await window.__botellas.libre();
    const sol = MOTOR.resolver(G.estado, G.nv).movs;
    for(let k = 0; k < sol.length - (dejar || 0); k++){
      tocar(sol[k][0]); await esperar(120);
      tocar(sol[k][1]); await esperar(80);
      await window.__botellas.libre();
    }
    return sol.length;
  },
  // e = {b, ab}
  forzar: (e) => { G.estado = e; G.oc = null; G.sel = null; construirTablero(); pintarControles(); vigilar(); },
  sinSalida: () => mostrarStrip(),
  pausar: (t) => { document.getAnimations().forEach(a => { try{ a.pause(); if(t !== undefined) a.currentTime = t; }catch(e){} }); },
  reanudar: () => { document.getAnimations().forEach(a => { try{ a.play(); }catch(e){} }); }
};
"""


def armar():
    src = leer("botellas.src.html")
    fuentes = leer("recursos", "fuentes.css")
    motor = leer("motor.js")
    # el catalogo de los 200 niveles; sin niveles.json (aun no generado) se usa la muestra corta
    # niveles.json solo vale si es el v3 (version 3 con "camino"); si no, la muestra corta, tambien en formato v3
    fuente = os.path.join("recursos", "niveles-muestra.json")
    if os.path.exists(os.path.join(AQUI, "niveles.json")):
        try:
            if json.loads(leer("niveles.json")).get("camino"):
                fuente = "niveles.json"
        except ValueError:
            pass
    niveles = leer(fuente).strip()
    if "</script" in niveles:
        sys.exit("el catalogo no puede contener </script")
    print("catalogo:", fuente)
    if "</script" in motor:
        sys.exit("motor.js no puede contener </script")

    def con(test):
        t = src
        t = t.replace("/*@FUENTES@*/", fuentes)
        t = t.replace("/*@MOTOR@*/", motor)
        t = t.replace("/*@NIVELES@*/", "const CATALOGO = " + niveles + ";")
        t = t.replace("/*@TEST@*/", TEST if test else "")

        def img(m):
            return leer("recursos", m.group(1) + ".b64").strip()

        def img_opc(m):
            ruta = os.path.join(AQUI, "recursos", m.group(1) + ".b64")
            return leer("recursos", m.group(1) + ".b64").strip() if os.path.exists(ruta) else ""

        t = re.sub(r"@IMG:([A-Za-z]+)@", img, t)
        t = re.sub(r"@IMG\?:([A-Za-z0-9]+)@", img_opc, t)
        return t

    art = con(False)
    # El Artifact no lleva doctype, html, head ni body: la plataforma los pone
    assert art.lstrip().startswith("<title>Botellas de Cami</title>")
    with open(os.path.join(AQUI, "botellas.html"), "w", encoding="utf-8") as f:
        f.write(art)

    loc = con(True)
    cabeza = ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
              '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=1,user-scalable=no">')
    # titulo y meta quedan en el head; el resto (style, contenido, scripts) va en el body
    m = re.match(r"\s*(<title>.*?</title>)\s*(<meta name=\"claude:viewport-fit-sides\"[^>]*>)\s*(.*)\Z", loc, re.S)
    assert m, "estructura inesperada"
    html = cabeza + m.group(1) + m.group(2) + "</head><body>" + m.group(3) + "</body></html>\n"
    with open(os.path.join(AQUI, "botellas-local.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # la version para CabriCoach: documento completo sin el atajo de prueba. La app lo trae con
    # fetch y lo pone en un iframe (srcdoc), asi que vive en assets/ de la fuente y del sitio
    m2 = re.match(r"\s*(<title>.*?</title>)\s*(<meta name=\"claude:viewport-fit-sides\"[^>]*>)\s*(.*)\Z", art, re.S)
    app = cabeza + m2.group(1) + "</head><body>" + m2.group(3) + "</body></html>\n"
    raiz = os.path.normpath(os.path.join(AQUI, "..", ".."))
    for destino in (os.path.join(raiz, "assets", "botellas.html"), os.path.join(raiz, "site", "assets", "botellas.html")):
        with open(destino, "w", encoding="utf-8") as f:
            f.write(app)
        print(os.path.relpath(destino, raiz), os.path.getsize(destino) // 1024, "KB")

    # el JS de la pagina, aparte, para revisarlo con jsc
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
    with open(os.path.join(AQUI, "pagina-extraida.js"), "w", encoding="utf-8") as f:
        f.write("\n;\n".join(scripts))
    for n in ("botellas.html", "botellas-local.html"):
        print(n, os.path.getsize(os.path.join(AQUI, n)) // 1024, "KB")


if __name__ == "__main__":
    armar()
