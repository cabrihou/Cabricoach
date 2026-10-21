#!/usr/bin/env python3
"""Pasada en Chrome sin interfaz (CDP) sobre botellas-local.html (v3: un camino de 200 niveles con dificultad sorteada, llaves, cajas y candados).
Guarda capturas en capturas/ (las v3 llevan prefijo v3-; las de la v0 quedan de referencia).
Requiere el servidor: python3 -m http.server 8931 (desde esta carpeta) y websocket-client."""
import base64, json, os, shutil, subprocess, sys, tempfile, time, urllib.request
import websocket

AQUI = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(AQUI, "capturas")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = "http://127.0.0.1:8931/botellas-local.html"
PUERTO = 9333
os.makedirs(CAP, exist_ok=True)


class Pagina:
    def __init__(self):
        self.tmp = tempfile.mkdtemp(prefix="botellas-chrome-")
        self.proc = subprocess.Popen([CHROME, "--headless=new", "--remote-debugging-port=%d" % PUERTO, "--user-data-dir=" + self.tmp,
                                      "--no-first-run", "--remote-allow-origins=*", "--no-default-browser-check", "--hide-scrollbars", "--autoplay-policy=no-user-gesture-required",
                                      "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        url = None
        for _ in range(60):
            try:
                t = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % PUERTO))
                pg = [x for x in t if x.get("type") == "page"]
                if pg:
                    url = pg[0]["webSocketDebuggerUrl"]
                    break
            except Exception:
                pass
            time.sleep(0.25)
        if not url:
            raise RuntimeError("Chrome no arranco")
        self.ws = websocket.create_connection(url, max_size=None, timeout=60)
        self.n = 0
        self.errores = []
        self.enviar("Page.enable")
        self.enviar("Runtime.enable")

    def enviar(self, metodo, **p):
        self.n += 1
        mi = self.n
        self.ws.send(json.dumps({"id": mi, "method": metodo, "params": p}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("method") == "Runtime.exceptionThrown":
                self.errores.append(json.dumps(m["params"]["exceptionDetails"])[:400])
            if m.get("method") == "Runtime.consoleAPICalled" and m["params"]["type"] == "error":
                self.errores.append("console.error " + json.dumps(m["params"]["args"])[:300])
            if m.get("id") == mi:
                if "error" in m:
                    raise RuntimeError(metodo + ": " + json.dumps(m["error"]))
                return m.get("result", {})

    def vista(self, w, h, dsf=2):
        self.enviar("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=dsf, mobile=True)
        self.enviar("Emulation.setTouchEmulationEnabled", enabled=True)

    def ir(self, url, espera=1.2):
        self.enviar("Page.navigate", url=url)
        time.sleep(espera)

    def js(self, expr, espera=True):
        r = self.enviar("Runtime.evaluate", expression=expr, awaitPromise=espera, returnByValue=True)
        if "exceptionDetails" in r:
            self.errores.append("eval: " + json.dumps(r["exceptionDetails"])[:400])
        return r.get("result", {}).get("value")

    def foto(self, nombre, completa=False):
        p = {"format": "png"}
        if completa:
            alto = self.js("document.documentElement.scrollHeight", False)
            ancho = self.js("document.documentElement.clientWidth", False)
            p.update(captureBeyondViewport=True, clip={"x": 0, "y": 0, "width": ancho, "height": alto, "scale": 1})
        r = self.enviar("Page.captureScreenshot", **p)
        ruta = os.path.join(CAP, nombre + ".png")
        with open(ruta, "wb") as f:
            f.write(base64.b64decode(r["data"]))
        print("captura", ruta)

    def cerrar(self):
        try:
            self.ws.close()
        except Exception:
            pass
        self.proc.terminate()
        time.sleep(0.5)
        shutil.rmtree(self.tmp, ignore_errors=True)


def limpio(pg, url, w=390, h=844, espera=1.5, S=None):
    """Abre la pagina con localStorage vacio (o con el estado S)."""
    pg.vista(w, h)
    pg.ir("about:blank", 0.2)
    pg.ir(BASE, 0.8)
    pg.js("localStorage.clear(); " + ("localStorage.setItem('botellas:v1', %s);" % json.dumps(json.dumps(S)) if S else "") + " true", False)
    pg.ir(url if url.startswith("http") else BASE + url, espera)
    pg.js("location.reload()", False)
    time.sleep(espera)


CAT = json.load(open(os.path.join(AQUI, "niveles.json")))["camino"]


def buscar(pred, desde=1):
    for n in CAT:
        if n["L"] >= desde and pred(n):
            return n["L"]
    raise RuntimeError("no hay nivel que cumpla")


def estado(nivel=1, estrellas=None, vistos=True, jugador="cami"):
    """Estado guardado v3 para arrancar; vistos = ya vio todas las novedades."""
    p = {"v": 3, "nivel": nivel, "estrellas": {str(k): v for k, v in (estrellas or {}).items()}, "dias": {},
         "racha": {"actual": 0, "mejor": 0, "ultimo": None}, "stats": {"ganados": 1, "segundos": 0},
         "vistos": {k: True for k in ("llave", "candado", "misterio", "largas")} if vistos else {}}
    return {"jugador": jugador, "perfiles": {"cami": p, "andres": p}, "ajustes": {"sonido": False, "vibra": False, "simbolos": False}}


JUGAR = """window.__jugar = async (k) => { const b = window.__botellas; await b.libre(); const nv = b.G.nv;
  for(let q = 0; q < k; q++){ const m = nv.movs[q]; b.tocar(m[0]); await new Promise(r => setTimeout(r, 90)); b.tocar(m[1]); await new Promise(r => setTimeout(r, 60)); await b.libre(); } return k; };
window.__primera = (T) => { const b = window.__botellas, M = b.motor, nv = b.G.nv; let E = {b:nv.botellas, ab:0};
  for(let k = 0; k < nv.movs.length; k++){ const m = nv.movs[k], r = M.verter(E, m[0], m[1], nv); if(r.abre.length && r.abre[0].tipo === T) return k; E = r.estado; } return -1; };
window.__espera = async (sel, extra) => { for(let i = 0; i < 200; i++){ if(document.querySelector(sel)) break; await new Promise(r => setTimeout(r, 15)); } await new Promise(r => setTimeout(r, extra)); return !!document.querySelector(sel); }; true"""


def abrir(pg, url, S, w=390, h=844, espera=1.6, aviso=False):
    """Abre el nivel con el estado S. Con aviso=False salta la tarjeta de nivel dificil para llegar al tablero."""
    limpio(pg, url, w, h, espera, S)
    pg.js(JUGAR, False)
    pg.js("window.__botellas.libre()")
    if not aviso:
        pg.js("window.__botellas.aviso()", False)
        time.sleep(0.45)


def scroll_h(pg, etiqueta):
    sh = pg.js("document.documentElement.scrollWidth > document.documentElement.clientWidth", False)
    print("scroll horizontal", etiqueta, sh)


if __name__ == "__main__":
    pg = Pagina()
    try:
        which = sys.argv[1:] or ["todo"]
        todo = "todo" in which
        if todo or "inicio" in which:
            limpio(pg, "", S=estado(37, {i: (3 if i % 3 else 2) for i in range(1, 37)}))
            pg.foto("v3-01-inicio")
            pg.foto("v3-02-inicio-completo", True)
            pg.js("document.querySelectorAll('.schedhead').forEach(h=>h.click()); true", False)
            time.sleep(0.5)
            pg.foto("v3-02b-inicio-cajas", True)
            scroll_h(pg, "inicio 390")
            limpio(pg, "", 320, 640, S=estado(37, {i: 3 for i in range(1, 37)}))
            pg.foto("v3-02c-inicio-320", True)
            scroll_h(pg, "inicio 320")
            limpio(pg, "")
            pg.js("document.getElementById('who').click(); true", False)
            time.sleep(0.4)
            pg.foto("v3-02d-inicio-nuevo-andres")
            # inicio con un nivel muy dificil y uno dificil como siguiente
            for dif, nom in (("muy", "muy"), ("dificil", "dificil")):
                L = buscar(lambda n: n["dif"] == dif)
                limpio(pg, "", S=estado(L, {i: 3 for i in range(1, L)}))
                pg.foto("v3-02e-inicio-%s" % nom)
        if todo or "aviso" in which:
            for dif in ("dificil", "muy"):
                L = buscar(lambda n: n["dif"] == dif)
                limpio(pg, "#nivel%d" % L, S=estado(L), espera=0.3)
                time.sleep(0.3)
                pg.foto("v3-03-aviso-%s" % dif)
                print("aviso", dif, "nivel", L, "visible:", pg.js("!document.getElementById('aviso').hidden", False))
                time.sleep(1.6)
                print("   tras 1,6 s visible:", pg.js("!document.getElementById('aviso').hidden", False))
                pg.foto("v3-03b-tras-aviso-%s" % dif)
            # un toque lo salta
            limpio(pg, "#nivel%d" % L, S=estado(L), espera=1.0)
            time.sleep(0.4)
            pg.js("document.getElementById('aviso').click(); true", False)
            time.sleep(0.5)
            print("tras toque visible:", pg.js("!document.getElementById('aviso').hidden", False))
            # retomado a medias: no avisa
            pg.js(JUGAR, False)
            pg.js("window.__botellas.libre()")
            pg.js("document.getElementById('aviso').click(); true", False)
            time.sleep(0.4)
            pg.js("window.__jugar(1)")
            pg.js("location.reload()", False)
            time.sleep(1.6)
            print("al retomar visible:", pg.js("!document.getElementById('aviso').hidden", False))
            # no avisa en facil
            limpio(pg, "#nivel1", S=estado(1), espera=1.0)
            time.sleep(0.5)
            print("nivel facil visible:", pg.js("!document.getElementById('aviso').hidden", False))
        if todo or "difs" in which:
            for dif in ("facil", "normal", "dificil", "muy"):
                L = buscar(lambda n: n["dif"] == dif and len(n["cajas"]) <= 1, 20)
                abrir(pg, "#nivel%d" % L, estado(L))
                print(dif, "nivel", L, "botellas", pg.js("window.__botellas.G.estado.b.length", False), pg.js("document.getElementById('gChip').textContent", False))
                pg.foto("v3-04-nivel-%s" % dif)
        if todo or "llave" in which:
            L = buscar(lambda n: n["rasgos"] == ["llave"] and len(n["cajas"]) == 1 and n["dif"] in ("facil", "normal"))
            abrir(pg, "#nivel%d" % L, estado(L))
            pg.foto("v3-05-llave-antes")
            k = pg.js("window.__primera('caja')", False)
            print("llave: nivel", L, "se abre en el movimiento", k)
            pg.js("window.__jugar(%d)" % k)
            pg.js("(async()=>{const b=window.__botellas, m=b.G.nv.movs[%d]; b.tocar(m[0]); await new Promise(r=>setTimeout(r,90)); b.tocar(m[1]); return 1})()" % k)
            pg.js("window.__espera('.vllave', 230)")
            pg.js("window.__botellas.pausar(); true", False)
            pg.foto("v3-05b-llave-vuelo")
            pg.js("window.__botellas.reanudar(); true", False)
            time.sleep(1.5)
            pg.foto("v3-05c-llave-despues")
            print("caja abierta:", pg.js("JSON.stringify([document.querySelectorAll('#board .caja.cerrada').length, window.__botellas.G.estado.ab])", False))
        if todo or "candado" in which:
            L = buscar(lambda n: n["rasgos"] == ["candado"] and n["dif"] in ("facil", "normal"))
            abrir(pg, "#nivel%d" % L, estado(L))
            pg.foto("v3-06-candado-antes")
            k = pg.js("window.__primera('candado')", False)
            print("candado: nivel", L, "se abre en el movimiento", k)
            pg.js("window.__jugar(%d)" % k)
            pg.js("(async()=>{const b=window.__botellas, m=b.G.nv.movs[%d]; b.tocar(m[0]); await new Promise(r=>setTimeout(r,90)); b.tocar(m[1]); return 1})()" % k)
            pg.js("window.__espera('.pdot', 170)")
            pg.js("window.__botellas.pausar(); true", False)
            pg.foto("v3-06b-candado-punto")
            pg.js("window.__botellas.reanudar(); true", False)
            time.sleep(1.6)
            pg.foto("v3-06c-candado-despues")
            print("candados cerrados al final:", pg.js("document.querySelectorAll('#board .slot.cerrada').length", False))
        if todo or "dos" in which:
            L = buscar(lambda n: len(n["cajas"]) == 2 and any(l["b"] in n["cajas"][0]["bots"] for l in n["llaves"]))
            abrir(pg, "#nivel%d" % L, estado(L))
            print("dos cajas con cadena: nivel", L, n_dif := pg.js("window.__botellas.G.nv.dif", False), "botellas", pg.js("window.__botellas.G.estado.b.length", False))
            pg.foto("v3-07-dos-cajas")
            scroll_h(pg, "dos cajas 390")
            abrir(pg, "#nivel%d" % L, estado(L), 320, 640)
            pg.foto("v3-07b-dos-cajas-320")
            scroll_h(pg, "dos cajas 320")
        if todo or "misterio" in which:
            L = buscar(lambda n: n["rasgos"] == ["misterio"])
            abrir(pg, "#nivel%d" % L, estado(L))
            n0 = pg.js("document.querySelectorAll('.ly.oc').length", False)
            pg.foto("v3-08-misterio-inicio")
            pg.js("window.__jugar(6)")
            n1 = pg.js("document.querySelectorAll('.ly.oc').length", False)
            pg.js("(async()=>{for(let i=0;i<6;i++){document.getElementById('cUndo').click(); await new Promise(r=>setTimeout(r,60));} return 1})()")
            time.sleep(0.3)
            n2 = pg.js("document.querySelectorAll('.ly.oc').length", False)
            pg.foto("v3-08b-misterio-tras-deshacer")
            print("capas ocultas: inicio", n0, "tras 6 movs", n1, "tras deshacer todo", n2)
        if todo or "novedad" in which:
            limpio(pg, "#nivel4")
            pg.js("window.__botellas.libre()")
            time.sleep(0.8)
            pg.foto("v3-09-novedad-candado")
            pg.js("window.__botellas.novedad(); true", False)
            time.sleep(0.5)
            print("vistos:", pg.js("JSON.stringify(window.__botellas.S().perfiles.cami.vistos)", False))
            # aviso y luego Novedad en un mismo nivel (primer nivel dificil con una mecanica nueva para este perfil)
            L = buscar(lambda n: n["dif"] in ("dificil", "muy") and "misterio" in n["rasgos"])
            limpio(pg, "#nivel%d" % L, S=estado(L, vistos=False), espera=1.0)
            time.sleep(0.5)
            print("aviso primero:", pg.js("!document.getElementById('aviso').hidden", False), "novedad:", pg.js("document.getElementById('veloNov').classList.contains('on')", False))
            time.sleep(1.8)
            print("despues del aviso, novedad:", pg.js("document.getElementById('veloNov').classList.contains('on')", False))
            pg.foto("v3-09b-novedad-tras-aviso")
        if todo or "chico" in which:
            L = max((n["L"] for n in CAT if n["dif"] == "muy"), key=lambda i: (len(CAT[i - 1]["botellas"]), len(CAT[i - 1]["cajas"])))
            abrir(pg, "#nivel%d" % L, estado(L), 320, 640)
            print("muy nivel", L, "botellas", pg.js("window.__botellas.G.estado.b.length", False), "rasgos", pg.js("JSON.stringify(window.__botellas.G.nv.rasgos)", False))
            pg.foto("v3-10-muy-320x640")
            pg.js("document.getElementById('cExtra').click(); true", False)
            time.sleep(0.6)
            pg.foto("v3-10b-muy-320x640-extra")
            print("botellas con la extra:", pg.js("window.__botellas.G.estado.b.length", False))
            scroll_h(pg, "muy 320")
            abrir(pg, "#nivel%d" % L, estado(L), 390, 844)
            pg.js("document.getElementById('cExtra').click(); true", False)
            time.sleep(0.6)
            pg.foto("v3-10c-muy-390-extra")
        if todo or "ganar" in which:
            abrir(pg, "#nivel1", estado(1))
            pg.js("window.__botellas.resolver(0)")
            time.sleep(1.4)
            pg.foto("v3-11-ganar")
            print("tras ganar el 1, nivel guardado:", pg.js("window.__botellas.S().perfiles.cami.nivel", False))
            abrir(pg, "#nivel200", estado(200))
            pg.js("window.__botellas.resolver(0)")
            time.sleep(1.6)
            pg.foto("v3-11b-ganar-200")
            print("tras el 200:", pg.js("window.__botellas.S().perfiles.cami.nivel", False), pg.js("document.getElementById('wTit').textContent", False), "|", pg.js("document.getElementById('wSig').textContent", False))
            pg.js("document.getElementById('wSig').click(); true", False)
            time.sleep(8)
            print("nivel 201:", pg.js("(()=>{const g=window.__botellas.G; return JSON.stringify([g.clave, g.nv && g.nv.id, g.nv && g.nv.dif, g.nv && g.nv.rasgos, g.nv && g.nv.botellas.length])})()", False))
            pg.js("window.__botellas.aviso(); true", False)
            time.sleep(0.5)
            pg.foto("v3-11c-nivel-201")
            # repetir no avisa
            L = buscar(lambda n: n["dif"] == "dificil")
            abrir(pg, "#nivel%d" % L, estado(L))
            pg.js("window.__botellas.resolver(0)")
            time.sleep(1.5)
            pg.foto("v3-11d-ganar-dificil")
            pg.js("document.getElementById('wRep').click(); true", False)
            time.sleep(0.9)
            print("repetir, aviso visible:", pg.js("!document.getElementById('aviso').hidden", False))
        if todo or "migra" in which:
            # perfil v2 y partida v2 en el almacenamiento: no rompe, el camino empieza de cero y todo queda en legado
            v2 = {"jugador": "cami", "perfiles": {"cami": {"ruta": "normal", "rutas": {"normal": {"nivel": 12, "estrellas": {"1": 3}}}, "dias": {}, "racha": {"actual": 2, "mejor": 3, "ultimo": "2026-10-20"}, "stats": {"ganados": 11, "segundos": 5}, "vistos": {}}},
                  "ajustes": {"sonido": False}, "partida": {"jugador": "cami", "modo": "ruta", "ruta": "normal", "clave": "12", "estado": {"b": [[1]], "ab": 0}}}
            limpio(pg, "", S=v2)
            print("migracion:", pg.js("JSON.stringify([window.__botellas.S().perfiles.cami.nivel, !!window.__botellas.S().perfiles.cami.legado, window.__botellas.S().partida, window.__botellas.S().perfiles.cami.racha.mejor])", False))
            pg.foto("v3-12-inicio-migrado")
        if todo or "dia" in which:
            limpio(pg, "#dia", S=estado())
            pg.js("window.__botellas.libre()")
            pg.foto("v3-13-reto-dia")
            print("dia:", pg.js("JSON.stringify([window.__botellas.G.nv.id, window.__botellas.G.nv.rasgos, window.__botellas.G.nv.dif])", False))
        print("errores:", pg.errores if pg.errores else "ninguno")
    finally:
        pg.cerrar()
