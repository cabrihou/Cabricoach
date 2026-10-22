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
         "vistos": {k: True for k in ("llave", "candado", "misterio", "largas", "gigante", "nuevos")} if vistos else {}}
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
            print("capas ocultas: inicio", n0, "tras 6 movs", n1)
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
            scroll_h(pg, "muy 320")
            abrir(pg, "#nivel%d" % L, estado(L), 390, 844)
            pg.foto("v3-10c-muy-390")
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

        if todo or "v4" in which:
            GIG = json.load(open("/private/tmp/claude-501/-Users-afcastro-Documents-Projects/4e98e039-e9b2-48eb-b87f-a3c14e238be4/scratchpad/gig.json"))
            def inyectar(pg, nv, L=30):
                pass   # con el niveles.json v4 los niveles reales ya traen gigante (L30, L33, L41) y colores nuevos (desde L12)
            # sin pista: barra de 3 botones
            abrir(pg, "#nivel24", estado(24))
            print("v4 botones de la barra:", pg.js("JSON.stringify([...document.querySelectorAll('#gCtl .ctl')].map(b=>b.textContent.trim()))", False), "| #cHint:", pg.js("!!document.getElementById('cHint')", False), "| texto 'ista' en la pagina de juego:", pg.js("/Pista/.test(document.getElementById('vJuego').innerText)", False))
            pg.foto("v4-01-sin-pista-390")
            scroll_h(pg, "juego 390")
            abrir(pg, "#nivel24", estado(24), 320, 640)
            pg.foto("v4-01b-sin-pista-320")
            scroll_h(pg, "juego 320")
            # gigante
            for tag, w, h in (("390", 390, 844), ("320", 320, 640)):
                limpio(pg, "", w, h, 1.2, estado(30))
                pg.js(JUGAR, False)
                inyectar(pg, GIG["gig"])
                pg.js("window.__botellas.abrir('camino','camino',30); true", False)
                pg.js("window.__botellas.libre()")
                time.sleep(0.4)
                pg.foto("v4-02-gigante-%s" % tag)
                print("gigante", tag, pg.js("(()=>{const s=[...document.querySelectorAll('#board .slot')]; const g=s.find(x=>x.classList.contains('gig')).getBoundingClientRect(), n=s.find(x=>!x.classList.contains('gig')).getBoundingClientRect(); return JSON.stringify({ancho:[g.width,n.width,+(g.width/n.width).toFixed(2)], alto:[g.height,n.height,+(g.height/n.height).toFixed(2)], base:[g.bottom, n.bottom]})})()", False))
                scroll_h(pg, "gigante " + tag)
                if tag == "390":
                    nvg = GIG["gig"]
                    # vertido desde la gigante a otra botella (a mitad) y de otra hacia la gigante
                    mv = pg.js("JSON.stringify(window.__botellas.G.sol)", False)
                    sol = json.loads(mv)
                    desde = [m for m in sol if m[0] == 0]
                    haci = [m for m in sol if m[1] == 0]
                    print("movs con gigante de origen:", desde[:2], "de destino:", haci[:2])
                    # jugar la solucion hasta el primer mov que sale de la gigante
                    k = sol.index(desde[0])
                    pg.js("window.__jugar(%d)" % k)
                    pg.js("(async()=>{const b=window.__botellas,m=b.G.sol[%d];b.tocar(m[0]);await new Promise(r=>setTimeout(r,200));b.tocar(m[1]);await new Promise(r=>setTimeout(r,420));b.pausar();return 1})()" % k)
                    pg.foto("v4-03-vertido-desde-gigante")
                    pg.js("window.__botellas.reanudar(); true", False); time.sleep(1.2)
                    pg.foto("v4-03b-tras-vertido-gigante")
                    # hacia la gigante
                    limpio(pg, "", 390, 844, 1.2, estado(30)); pg.js(JUGAR, False); inyectar(pg, GIG["gig"])
                    pg.js("window.__botellas.abrir('camino','camino',30); true", False); pg.js("window.__botellas.libre()"); time.sleep(0.3)
                    kk = sol.index(haci[0])
                    pg.js("window.__jugar(%d)" % kk)
                    pg.js("(async()=>{const b=window.__botellas,m=b.G.sol[%d];b.tocar(m[0]);await new Promise(r=>setTimeout(r,200));b.tocar(m[1]);await new Promise(r=>setTimeout(r,420));b.pausar();return 1})()" % kk)
                    pg.foto("v4-03c-vertido-hacia-gigante")
                    pg.js("window.__botellas.reanudar(); true", False); time.sleep(1.2)
                    # resolver completo: la gigante se completa con 4
                    pg.js("window.__botellas.resolver(0)"); time.sleep(1.4)
                    pg.foto("v4-03d-gigante-ganar")
                    print("gigante: ganado", pg.js("window.__botellas.G.ganado", False), "| tapas:", pg.js("document.querySelectorAll('#board .tapa').length", False), "| tapa en la gigante:", pg.js("!!document.querySelector('#board .slot.gig .tapa')", False))
            # colores nuevos
            limpio(pg, "", 390, 844, 1.2, estado(12)); pg.js(JUGAR, False)
            pg.js("window.__botellas.abrir('camino','camino',12); true", False); pg.js("window.__botellas.libre()"); time.sleep(0.4)
            pg.foto("v4-04-nuevos-antes")
            k = pg.js("window.__primera('caja')", False)
            pg.js("window.__jugar(%d)" % k)
            pg.js("(async()=>{const b=window.__botellas,m=b.G.nv.movs[%d];b.tocar(m[0]);await new Promise(r=>setTimeout(r,90));b.tocar(m[1]);return 1})()" % k)
            pg.js("window.__espera('.slot.llegan', 250)")
            pg.js("window.__botellas.pausar(); true", False)
            print("llegan:", pg.js("document.querySelectorAll('#board .slot.llegan').length", False), "| live:", pg.js("document.getElementById('live').textContent", False))
            pg.foto("v4-04b-colores-nuevos-brillo")
            pg.js("window.__botellas.reanudar(); true", False); time.sleep(1.8)
            pg.foto("v4-04c-nuevos-despues")
            # tablero chico y grande
            for L_, tag in ((2, "chico"), (111, "grande")):
                for w, h in ((390, 844), (320, 640)):
                    abrir(pg, "#nivel%d" % L_, estado(L_), w, h)
                    pg.foto("v4-05-tablero-%s-%d" % (tag, w))
                    print("tablero", tag, w, "botellas", pg.js("window.__botellas.G.estado.b.length", False), "ancho botella", pg.js("Math.round(document.querySelector('#board .slot').getBoundingClientRect().width)", False), "| filas", pg.js("document.querySelectorAll('#board .brow').length", False), "| hueco arriba (px):", pg.js("(()=>{const b=document.getElementById('board').getBoundingClientRect(), r=document.querySelector('#board .brow').getBoundingClientRect(); return Math.round(r.top-b.top)})()", False), "abajo:", pg.js("(()=>{const b=document.getElementById('board').getBoundingClientRect(), rs=document.querySelectorAll('#board .brow'), r=rs[rs.length-1].getBoundingClientRect(); return Math.round(b.bottom-r.bottom)})()", False))
                    scroll_h(pg, "tablero %s %d" % (tag, w))
            # vertido a mitad en un tablero grande, desde la fila de arriba (que no se corte)
            abrir(pg, "#nivel2", estado(2))
            pg.js("(async()=>{const b=window.__botellas,m=b.G.sol[0];b.tocar(m[0]);await new Promise(r=>setTimeout(r,200));b.tocar(m[1]);await new Promise(r=>setTimeout(r,430));b.pausar();return 1})()")
            pg.foto("v4-06-vertido-tablero-chico")
            pg.js("window.__botellas.reanudar(); true", False)
            # inicio (menos vacio)
            limpio(pg, "", S=estado(37, {i: 3 for i in range(1, 37)}))
            pg.foto("v4-07-inicio-390")
            limpio(pg, "", 320, 640, S=estado(37, {i: 3 for i in range(1, 37)}))
            pg.foto("v4-07b-inicio-320")
            scroll_h(pg, "inicio 320 v4")
        if todo or "arrastre" in which:
            def toque(tipo, x, y):
                pg.enviar("Input.dispatchTouchEvent", type=tipo, touchPoints=([{"x": x, "y": y}] if tipo != "touchEnd" else []))
            def centro(i):
                r_ = json.loads(pg.js("(()=>{const r=document.querySelector('#board .slot[data-i=\"%d\"]').getBoundingClientRect(); return JSON.stringify([r.left+r.width/2, r.top+r.height/2])})()" % i, False))
                return r_
            def tap(i=None, xy=None):
                x, y = xy if xy else centro(i)
                toque("touchStart", x, y); time.sleep(0.05); toque("touchEnd", x, y); time.sleep(0.15)
            def arrastrar(i, destino_xy, pasos=8, pausa_mitad=None, soltar=True):
                x0, y0 = centro(i); x1, y1 = destino_xy
                toque("touchStart", x0, y0); time.sleep(0.05)
                for k in range(1, pasos + 1):
                    toque("touchMove", x0 + (x1 - x0) * k / pasos, y0 + (y1 - y0) * k / pasos); time.sleep(0.03)
                    if pausa_mitad and k == pasos // 2 + 2:
                        time.sleep(0.15); pg.foto(pausa_mitad)
                if soltar:
                    toque("touchEnd", x1, y1)
            ESTADO = "JSON.stringify({movs:window.__botellas.G.movs, sel:window.__botellas.G.sel, busy:window.__botellas.G.busy, arrastra:document.querySelectorAll('#board .slot.arrastra').length, destino:document.querySelectorAll('#board .slot.destino').length, tr:(document.querySelector('#board .slot[data-i=\"%d\"] .bwrap')||{style:{}}).style.transform||''})"
            L = 24
            abrir(pg, "#nivel%d" % L, estado(L))
            sol = json.loads(pg.js("JSON.stringify(window.__botellas.G.sol)", False)); i0, j0 = sol[0]
            print("arrastre: nivel", L, "primera jugada", sol[0], "| touch-action del tablero:", pg.js("getComputedStyle(document.getElementById('board')).touchAction", False))
            # 1) arrastrar a una valida: marca el destino a mitad y vierte al soltar
            arrastrar(i0, centro(j0), pausa_mitad="v5-01-arrastre-a-mitad-destino-marcado", soltar=False)
            print("a mitad:", pg.js(ESTADO % i0, False))
            toque("touchEnd", *centro(j0)); time.sleep(0.2)
            pg.foto("v5-01b-arrastre-soltado")
            time.sleep(1.4)
            print("tras soltar en valida:", pg.js(ESTADO % i0, False))
            # 2) arrastrar a una invalida (misma botella de origen a una que no puede recibir) y a la nada
            abrir(pg, "#nivel%d" % L, estado(L))
            E_ = json.loads(pg.js("JSON.stringify(window.__botellas.G.estado.b)", False))
            inval = [j for j in range(len(E_)) if j != i0 and not pg.js("window.__botellas.motor.puedeVerter(window.__botellas.G.estado, %d, %d, window.__botellas.G.nv)" % (i0, j), False)]
            print("invalidas desde", i0, ":", inval)
            arrastrar(i0, centro(inval[0]), pausa_mitad="v5-02-arrastre-sobre-invalida-sin-marca", soltar=False)
            print("sobre invalida, marcas:", pg.js(ESTADO % i0, False))
            toque("touchEnd", *centro(inval[0])); time.sleep(0.6)
            print("tras soltar en invalida:", pg.js(ESTADO % i0, False))
            arrastrar(i0, (195, 300))   # a la nada (espacio sin botella)
            time.sleep(0.6)
            print("tras soltar en la nada:", pg.js(ESTADO % i0, False))
            pg.foto("v5-03-tras-cancelar")
            # 3) toque-toque sigue
            tap(i0); print("toque 1:", pg.js(ESTADO % i0, False)); tap(j0); time.sleep(1.4)
            print("toque-toque:", pg.js(ESTADO % i0, False))
            # 4) tocar afuera cancela (fondo del tablero, cabecera, alrededor)
            for etiqueta, xy in (("fondo del tablero", (386, 262)), ("cabecera", (200, 40)), ("junto a las botellas", (8, 420))):
                abrir(pg, "#nivel%d" % L, estado(L))
                tap(i0)
                antes = pg.js("window.__botellas.G.sel", False)
                tap(xy=xy)
                print("tocar afuera (%s): sel antes %s, despues %s" % (etiqueta, antes, pg.js("window.__botellas.G.sel", False)))
            abrir(pg, "#nivel%d" % L, estado(L))
            tap(i0); pg.foto("v5-04-seleccionada"); tap(xy=(386, 262)); time.sleep(0.3); pg.foto("v5-04b-tras-tocar-afuera")
            # un boton de control tambien la baja
            tap(i0); pg.js("document.getElementById('cReset').click(); true", False); time.sleep(0.5)
            pg.js("document.getElementById('cNo') && document.getElementById('cNo').click(); true", False); time.sleep(0.3)
            print("boton de control: sel", pg.js("window.__botellas.G.sel", False))
            # 5) cerrada: no se arrastra, sacude
            Lc = buscar(lambda n: len(n["cajas"]) == 1 and n["dif"] in ("facil", "normal"))
            abrir(pg, "#nivel%d" % Lc, estado(Lc))
            cb = pg.js("window.__botellas.G.nv.cajas[0].bots[0]", False)
            x, y = centro(cb); toque("touchStart", x, y); [toque("touchMove", x + 10 * k, y + 5 * k) for k in range(1, 6)]; toque("touchEnd", x + 50, y + 25); time.sleep(0.3)
            print("cerrada: arrastra=", pg.js("document.querySelectorAll('#board .slot.arrastra').length", False), "| movs", pg.js("window.__botellas.G.movs", False))
            # 6) a 320 tambien
            abrir(pg, "#nivel%d" % L, estado(L), 320, 640)
            arrastrar(i0, centro(j0), pausa_mitad="v5-05-arrastre-320", soltar=True); time.sleep(1.6)
            print("320: movs", pg.js("window.__botellas.G.movs", False)); scroll_h(pg, "arrastre 320")
        if todo or "v6" in which:
            # v6: lo cerrado no deja ver sus colores; sin Deshacer; Reiniciar (y Repetir) sacan otros colores y otro orden
            def toque(tipo, x, y):
                pg.enviar("Input.dispatchTouchEvent", type=tipo, touchPoints=([{"x": x, "y": y}] if tipo != "touchEnd" else []))
            def tap_sel(sel):
                x, y = json.loads(pg.js("(()=>{const r=document.querySelector('%s').getBoundingClientRect(); return JSON.stringify([r.left+r.width/2, r.top+r.height/2])})()" % sel, False))
                toque("touchStart", x, y); time.sleep(0.05); toque("touchEnd", x, y); time.sleep(0.2)
            VISTA = """(()=>{const g=window.__botellas.G; const bs=%s; return JSON.stringify(bs.map(i=>{const s=document.querySelector('#board .slot[data-i="'+i+'"]');
              return {i:i, capas:g.estado.b[i].length, tapadas:s.querySelectorAll('.ly.oc').length, conColor:s.querySelectorAll('.ly:not(.oc)').length, aria:s.getAttribute('aria-label')};}))})()"""
            # 1) candado
            L = buscar(lambda n: n["candados"] and not n["cajas"] and not n.get("ocultas"))
            abrir(pg, "#nivel%d" % L, estado(L))
            print("candado nivel", L, "cerrado:", pg.js(VISTA % "[window.__botellas.G.nv.candados[0].b]", False))
            pg.foto("v6-01-candado-tapado")
            k = pg.js("window.__primera('candado')", False)
            pg.js("window.__jugar(%d)" % (k + 1)); time.sleep(2.0)
            print("candado abierto:", pg.js(VISTA % "[window.__botellas.G.nv.candados[0].b]", False))
            pg.foto("v6-02-candado-abierto")
            # 2) cajon de dos
            L = buscar(lambda n: len(n["cajas"]) == 1 and len(n["cajas"][0]["bots"]) == 2 and not n.get("ocultas"))
            abrir(pg, "#nivel%d" % L, estado(L))
            print("cajon nivel", L, "cerrado:", pg.js(VISTA % "window.__botellas.G.nv.cajas[0].bots", False))
            pg.foto("v6-03-cajon-tapado")
            k = pg.js("window.__primera('caja')", False)
            pg.js("window.__jugar(%d)" % (k + 1)); time.sleep(2.4)
            print("cajon abierto:", pg.js(VISTA % "window.__botellas.G.nv.cajas[0].bots", False))
            pg.foto("v6-04-cajon-abierto")
            # 3) sin Deshacer
            print("boton deshacer existe:", pg.js("!!document.getElementById('cUndo')", False), "| controles en la barra:", pg.js("document.querySelectorAll('#gCtl .ctl').length", False))
            # 4) Reiniciar con movimientos: pregunta, y al aceptar cambian colores y orden
            L = 24
            abrir(pg, "#nivel%d" % L, estado(L))
            B = "JSON.stringify(window.__botellas.G.estado.b)"
            b0 = pg.js(B, False)
            pg.js("window.__jugar(2)")
            tap_sel("#cReset"); time.sleep(0.4)
            print("pregunta al reiniciar:", pg.js("document.getElementById('veloConf').classList.contains('on')", False), "|", pg.js("document.getElementById('cTit').textContent", False))
            pg.foto("v6-05-confirmar-reinicio")
            tap_sel("#cSi"); time.sleep(0.8)
            b1 = pg.js(B, False); vr = pg.js("window.__botellas.G.vr", False)
            print("tras reiniciar: movs", pg.js("window.__botellas.G.movs", False), "| distinto del original:", b1 != b0, "| variante", vr)
            pg.foto("v6-06-tras-reiniciar")
            # recargar sigue con la misma variante
            pg.js("location.reload()", False); time.sleep(1.8); pg.js(JUGAR, False); pg.js("window.__botellas.libre()"); pg.js("window.__botellas.aviso()", False); time.sleep(0.4)
            print("tras recargar: misma variante", pg.js("window.__botellas.G.vr", False) == vr, "| mismas botellas", pg.js(B, False) == b1)
            # la variante se gana con su solucion traducida
            meta = pg.js("window.__botellas.G.nv.movs.length", False)
            pg.js("window.__jugar(%d)" % meta); time.sleep(1.2)
            print("variante ganada:", pg.js("window.__botellas.G.ganado", False))
            # Repetir tras ganar tambien cambia los colores
            pg.js("document.getElementById('wRep').click(); true", False); time.sleep(1.4); pg.js("window.__botellas.aviso()", False); time.sleep(0.3)
            print("repetir: variante nueva", pg.js("window.__botellas.G.vr", False) not in (None, vr), "| movs", pg.js("window.__botellas.G.movs", False))
            # 5) sin movimientos no pregunta
            abrir(pg, "#nivel%d" % L, estado(L))
            tap_sel("#cReset"); time.sleep(0.5)
            print("sin movimientos: pregunta", pg.js("document.getElementById('veloConf').classList.contains('on')", False), "| cambio", pg.js(B, False) != b0)
            # 6) aviso de sin salida: solo Empezar de nuevo, sin volver atras
            pg.js("window.__jugar(1)"); pg.js("window.__botellas.sinSalida(); true", False); time.sleep(0.3)
            print("aviso sin salida:", pg.js("JSON.stringify(Array.from(document.querySelectorAll('#strip button')).map(b=>b.textContent))", False))
            pg.foto("v6-07-sin-salida")
            time.sleep(2.6)   # el aviso "Empezaste de nuevo" del paso anterior tapa el boton unos segundos
            tap_sel("#strip button"); time.sleep(0.6)
            print("tras Empezar de nuevo: pregunta", pg.js("document.getElementById('veloConf').classList.contains('on')", False), "| movs", pg.js("window.__botellas.G.movs", False), "| aviso visible", not pg.js("document.getElementById('strip').hidden", False))
            # 7) la hoja de Novedad del candado muestra la botella tapada
            limpio(pg, "#nivel4", S=estado(4, vistos=False))
            pg.js("window.__botellas.libre()"); pg.js("window.__botellas.aviso()", False); time.sleep(0.9)
            pg.foto("v6-08-novedad-candado")
        if todo or "v7" in which:
            # v7: sin botella extra, grado Extra difícil (5 barritas), chip sin desbordar y partidas con firma
            def toque(tipo, x, y):
                pg.enviar("Input.dispatchTouchEvent", type=tipo, touchPoints=([{"x": x, "y": y}] if tipo != "touchEnd" else []))
            def tap_sel(sel):
                x, y = json.loads(pg.js("(()=>{const r=document.querySelector('%s').getBoundingClientRect(); return JSON.stringify([r.left+r.width/2, r.top+r.height/2])})()" % sel, False))
                toque("touchStart", x, y); time.sleep(0.05); toque("touchEnd", x, y); time.sleep(0.2)
            def forzar_extra(L, rasgos=None):
                # el catalogo todavia puede no traer Extra: se fuerza en la pagina ya cargada y antes de abrir el nivel
                pg.js("(()=>{const n=window.__botellas.catalogo.camino[%d]; n.dif='extra'; %s return n.dif})()" % (L - 1, ("n.rasgos=%s;" % json.dumps(rasgos)) if rasgos else ""), False)
            def barras(sel):
                return pg.js("JSON.stringify([document.querySelectorAll('%s i').length, document.querySelectorAll('%s i.on').length])" % (sel, sel), False)
            def sin_desborde(etiqueta):
                r = json.loads(pg.js("""(()=>{const c=document.getElementById('gChip'), t=document.getElementById('gTop'), cr=c.getBoundingClientRect(), tr=t.getBoundingClientRect(), m=document.getElementById('gMov').getBoundingClientRect();
                  return JSON.stringify({ancho:Math.round(cr.width), der:Math.round(cr.right), izq:Math.round(cr.left), movsIzq:Math.round(m.left), recorte:c.scrollWidth>c.clientWidth+1, hscroll:document.documentElement.scrollWidth>document.documentElement.clientWidth, alto:Math.round(cr.height)})})()""", False))
                ok = not r["recorte"] and not r["hscroll"] and r["der"] <= r["movsIzq"] + 1
                print("chip %s: %s -> %s" % (etiqueta, json.dumps(r), "bien" if ok else "DESBORDA"))
            # 1) sin botella extra: ni boton ni insignia, una sola accion en la barra
            L = buscar(lambda n: n["dif"] in ("dificil", "muy"))
            abrir(pg, "#nivel%d" % L, estado(L))
            print("existe #cExtra:", pg.js("!!document.getElementById('cExtra')", False), "| existe #extraBdg:", pg.js("!!document.getElementById('extraBdg')", False),
                  "| controles en #gCtl:", pg.js("JSON.stringify(Array.from(document.querySelectorAll('#gCtl .ctl')).map(b=>b.textContent.trim()))", False),
                  "| G.extra:", pg.js("'extra' in window.__botellas.G", False))
            print("barra centrada: x del boton", pg.js("(()=>{const r=document.querySelector('#gCtl .ctl').getBoundingClientRect(); return Math.round(r.left+r.width/2)})()", False), "de ancho 390")
            pg.foto("v7-01-barra-un-control-390")
            # 2) aviso de sin salida con un solo boton
            pg.js("window.__botellas.sinSalida(); true", False); time.sleep(0.4)
            print("aviso sin salida:", pg.js("JSON.stringify(Array.from(document.querySelectorAll('#strip button')).map(b=>b.textContent))", False))
            pg.foto("v7-02-sin-salida-un-boton")
            # 3) aviso del grado Extra: 5 barritas, 2,2 s
            L = buscar(lambda n: n["dif"] == "normal" and n["L"] > 20)
            limpio(pg, "", S=estado(L, {i: 3 for i in range(1, L)}))
            forzar_extra(L)
            pg.js("window.__botellas.abrir('camino', 'camino', %d); true" % L, False)
            time.sleep(0.5)
            print("aviso extra visible:", pg.js("!document.getElementById('aviso').hidden", False), "| barras (total, encendidas):", barras("#aviso .medidor"),
                  "| titulo:", pg.js("document.querySelector('#aviso .t-h2').textContent", False))
            pg.foto("v7-03-aviso-extra-390")
            time.sleep(1.3)
            print("   a 1,8 s sigue visible (dura ~2,2 s):", pg.js("!document.getElementById('aviso').hidden", False))
            time.sleep(0.9)
            print("   a 2,7 s visible:", pg.js("!document.getElementById('aviso').hidden", False))
            # el aviso a 320 px
            limpio(pg, "", 320, 640, S=estado(L, {i: 3 for i in range(1, L)}))
            forzar_extra(L)
            pg.js("window.__botellas.abrir('camino', 'camino', %d); true" % L, False)
            time.sleep(0.5)
            pg.foto("v7-04-aviso-extra-320")
            # 4) medidor del Inicio con 5 barritas
            limpio(pg, "", S=estado(L, {i: 3 for i in range(1, L)}))
            forzar_extra(L)
            pg.js("pintarInicio(); true", False); time.sleep(0.4)
            print("Inicio extra: barras (total, encendidas):", barras("#hDif .medidor"), "|", pg.js("document.getElementById('hDif').textContent", False))
            pg.foto("v7-05-inicio-extra-390")
            scroll_h(pg, "inicio extra 390")
            # 5) chip con tres rasgos a 390 y a 320
            for w, h in ((390, 844), (320, 640)):
                limpio(pg, "", w, h, S=estado(L, {i: 3 for i in range(1, L)}))
                forzar_extra(L, ["llave", "candado", "misterio"])
                pg.js("window.__botellas.abrir('camino', 'camino', %d); true" % L, False)
                pg.js(JUGAR, False); pg.js("window.__botellas.libre()"); pg.js("window.__botellas.aviso()", False); time.sleep(0.6)
                print("chip texto (%d px):" % w, pg.js("document.getElementById('gChip').textContent", False))
                sin_desborde(str(w))
                pg.foto("v7-06-chip-extra-%d" % w)
            # el mismo chip de un Muy difícil normal a 320 (sin regresion)
            # 6) partida con firma distinta no se restaura; con su firma, si
            L2 = 24
            abrir(pg, "#nivel%d" % L2, estado(L2))
            pg.js("window.__jugar(3)"); time.sleep(0.4)
            print("jugados 3 movs: movs", pg.js("window.__botellas.G.movs", False), "| firma guardada", pg.js("window.__botellas.S().partida.firma", False))
            pg.js("location.reload()", False); time.sleep(1.8); pg.js(JUGAR, False); pg.js("window.__botellas.libre()"); pg.js("window.__botellas.aviso()", False); time.sleep(0.4)
            print("recargar con su firma: movs", pg.js("window.__botellas.G.movs", False), "(esperado 3)")
            pg.js("(()=>{const s=JSON.parse(localStorage.getItem('botellas:v1')); s.partida.firma='otra-firma'; localStorage.setItem('botellas:v1', JSON.stringify(s)); return 1})()", False)
            pg.js("location.reload()", False); time.sleep(1.8); pg.js(JUGAR, False); pg.js("window.__botellas.libre()"); time.sleep(0.4)
            print("recargar con otra firma: movs", pg.js("window.__botellas.G.movs", False), "(esperado 0) | firma nueva", pg.js("window.__botellas.S().partida && window.__botellas.S().partida.firma", False) != "otra-firma")
            pg.foto("v7-07-firma-distinta-reinicia")
            pg.js("(()=>{const s=JSON.parse(localStorage.getItem('botellas:v1')); delete s.partida.firma; s.partida.movs=4; localStorage.setItem('botellas:v1', JSON.stringify(s)); return 1})()", False)
            pg.js("location.reload()", False); time.sleep(1.8); pg.js(JUGAR, False); pg.js("window.__botellas.libre()"); time.sleep(0.4)
            print("recargar sin firma: movs", pg.js("window.__botellas.G.movs", False), "(esperado 0)")
            # 7) la cache vieja v3 se borra
            pg.js("localStorage.setItem('botellas:niveles:v3', '{}'); true", False)
            pg.js("location.reload()", False); time.sleep(1.8)
            print("cache v3 tras recargar:", pg.js("localStorage.getItem('botellas:niveles:v3')", False), "| claves:", pg.js("JSON.stringify(Object.keys(localStorage))", False))
        if todo or "mapa" in which:
            # v6: el mapa del recorrido (los cabritos suben la montana). Toques reales, nunca .click() en lo que se prueba de interaccion
            fallas_mapa = []
            def chk(cond, msg):
                print(("OK    " if cond else "FALLA ") + msg)
                if not cond:
                    fallas_mapa.append(msg)
            def toque(tipo, x, y):
                pg.enviar("Input.dispatchTouchEvent", type=tipo, touchPoints=([{"x": x, "y": y}] if tipo != "touchEnd" else []))
            def tap_sel(sel):
                x, y = json.loads(pg.js("(()=>{const r=document.querySelector('%s').getBoundingClientRect(); return JSON.stringify([r.left+r.width/2, r.top+r.height/2])})()" % sel, False))
                toque("touchStart", x, y); time.sleep(0.05); toque("touchEnd", x, y); time.sleep(0.35)
            def a_la_vista(n):
                # solo coloca el nodo en pantalla (el desplazamiento del dedo no es lo que se prueba)
                pg.js("(()=>{const b=document.querySelector('.nodo[data-n=\"%d\"]'); const sc=document.getElementById('mScroll'); const r=b.getBoundingClientRect(), s=sc.getBoundingClientRect(); sc.scrollTop += (r.top-s.top) + r.height/2 - sc.clientHeight/2; return 1})()" % n, False)
                time.sleep(0.25)
            INFO = """(()=>{ const q=(s)=>document.querySelector(s), r=(e)=>{const b=e.getBoundingClientRect(); return {l:b.left,t:b.top,r:b.right,b:b.bottom,cx:b.left+b.width/2,cy:b.top+b.height/2}};
              const sc=q('#mScroll'), s=r(sc), act=q('.nodo.actual'), a=act?r(act):null;
              const nodos=[...document.querySelectorAll('.nodo')].map(e=>({n:+e.dataset.n, rc:r(e)}));
              const pines=[...document.querySelectorAll('.pin')].map(e=>({cls:e.className, rc:r(e), vis:!e.hidden}));
              const cruza=[]; pines.forEach(p=>nodos.forEach(n=>{ if(p.vis && p.rc.l<n.rc.r && p.rc.r>n.rc.l && p.rc.t<n.rc.b && p.rc.b>n.rc.t) cruza.push([p.cls,n.n]); }));
              const corta=[...document.querySelectorAll('.mpar .tx,.mpar b,.cartel .txt h3')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent);
              return JSON.stringify({ sc:s, act:a, hechos:document.querySelectorAll('.nodo.hecho').length, actuales:document.querySelectorAll('.nodo.actual').length, futuros:document.querySelectorAll('.nodo.futuro').length,
                zonas:document.querySelectorAll('.zona').length, nodosTotal:nodos.length, pines:pines, cruza:cruza, corta:corta,
                hscroll:document.documentElement.scrollWidth>document.documentElement.clientWidth, hscrollMapa:sc.scrollWidth>sc.clientWidth+1,
                mapaVisible:!q('#vMapa').hidden, inicioVisible:!q('#vInicio').hidden, juegoVisible:!q('#vJuego').hidden,
                pares:q('#mPares').innerText.replace(/\\n/g,' | '), boton:q('#mJugar').textContent, toast:q('#toast').textContent, toastOn:q('#toast').classList.contains('show'),
                resumen:(q('.resumen')||{}).innerText||null, tope:q('.tope').textContent }); })()"""
            def info():
                v = pg.js(INFO, False)
                if v is None:
                    print("   info() fallo:", pg.errores[-1:])
                return json.loads(v)
            def estado_mapa(nivel, pareja, visto=None, jugador="cami", estrellas=True):
                def perfil(n):
                    pf = {"v": 3, "nivel": n, "estrellas": ({str(i): (3 if i % 3 else 2) for i in range(1, n)} if estrellas else {}), "dias": {},
                          "racha": {"actual": 0, "mejor": 0, "ultimo": None}, "stats": {"ganados": 1, "segundos": 0},
                          "vistos": {k: True for k in ("llave", "candado", "misterio", "largas", "gigante", "nuevos")}}
                    return pf
                yo, otro = perfil(nivel), perfil(pareja)
                if visto is not None:
                    yo["mapaVisto"] = visto
                perfiles = {jugador: yo, ("andres" if jugador == "cami" else "cami"): otro}
                return {"jugador": jugador, "perfiles": perfiles, "ajustes": {"sonido": False, "vibra": False, "simbolos": False}}
            def abrir_mapa(S, w=390, h=844, espera=1.5):
                limpio(pg, "", w, h, espera, S)
                pg.js("document.getElementById('hMapa').scrollIntoView({block:'center'}); 1", False); time.sleep(0.2)
                tap_sel("#hMapa"); time.sleep(0.8)

            # 1) abrir desde el Inicio con toque real: nivel 37, la pareja (Andres) en el 12
            abrir_mapa(estado_mapa(37, 12, visto=37))
            i = info()
            chk(i["mapaVisible"] and not i["inicioVisible"] and not i["juegoVisible"], "tocar 'Ver el recorrido' abre el mapa y oculta el Inicio")
            chk(i["hechos"] == 36 and i["actuales"] == 1, "nodos hechos = nivel - 1 (%d) y un actual (%d)" % (i["hechos"], i["actuales"]))
            chk(i["act"] and i["sc"]["t"] <= i["act"]["t"] and i["act"]["b"] <= i["sc"]["b"], "el nivel actual esta dentro de la pantalla")
            chk(i["act"] and abs(i["act"]["cy"] - (i["sc"]["t"] + i["sc"]["b"]) / 2) < 40, "el nivel actual queda centrado (desvio %.0f px)" % abs(i["act"]["cy"] - (i["sc"]["t"] + i["sc"]["b"]) / 2))
            print("   cabecera:", i["pares"], "| boton:", i["boton"])
            chk("Tú" in i["pares"] and "nivel 37" in i["pares"] and "Andrés" in i["pares"] and "nivel 12" in i["pares"], "la cabecera muestra a los dos y su nivel")
            chk(i["boton"] == "Jugar el nivel 37", "barra de abajo: Jugar el nivel 37")
            chk(not i["hscroll"] and not i["hscrollMapa"], "390 px sin scroll horizontal")
            chk(not i["cruza"] and not i["corta"], "ninguna cara toca un nodo y no hay textos cortados %s %s" % (i["cruza"], i["corta"]))
            # la cara de la pareja esta en su nivel: se pone el 12 a la vista y se mide contra el nodo 12
            a_la_vista(12)
            j = json.loads(pg.js("""(()=>{const c=(e)=>{const b=e.getBoundingClientRect(); return [b.left+b.width/2,b.top+b.height/2]}; return JSON.stringify({pin:c(document.querySelector('.pin.otro')), nodo:c(document.querySelector('.nodo[data-n="12"]'))})})()""", False))
            dist = ((j["pin"][0] - j["nodo"][0]) ** 2 + (j["pin"][1] - j["nodo"][1]) ** 2) ** 0.5
            chk(dist < 75, "la cara de Andres esta pegada al nodo 12 (distancia %.0f px)" % dist)
            pg.foto("v8-02-nivel12-pareja")
            # toque en un nodo hecho: aviso con sus estrellas, no abre el juego
            tap_sel('.nodo[data-n="12"]')
            i = info()
            print("   toast hecho:", i["toast"])
            chk(i["toastOn"] and i["toast"].startswith("Nivel 12 · 2 estrellas") and not i["juegoVisible"] and i["mapaVisible"], "tocar un nodo hecho avisa 'Nivel 12 · 2 estrellas' y no abre el juego")
            tap_sel('.nodo[data-n="11"]')
            i = info()
            chk(i["toast"] == "Nivel 11 · 3 estrellas", "otro nodo hecho: " + i["toast"])
            # estreno ya pasado: nombre de la mecanica
            a_la_vista(7); tap_sel('.nodo[data-n="7"]'); i = info()
            chk("Estreno: Llave escondida" in i["toast"], "un estreno que ya paso dice su mecanica: " + i["toast"])
            # nodo futuro: aviso, nada se abre
            a_la_vista(40); tap_sel('.nodo[data-n="40"]'); i = info()
            chk(i["toast"] == "Primero el nivel 37" and not i["juegoVisible"] and i["mapaVisible"], "tocar un nodo futuro avisa 'Primero el nivel 37' y no abre nada")
            # etiquetas accesibles
            et = json.loads(pg.js("""JSON.stringify([12,37,40,50].map(n=>document.querySelector('.nodo[data-n="'+n+'"]').getAttribute('aria-label')))""", False))
            print("   etiquetas:", et)
            chk(et[0].startswith("Nivel 12, ") and "2 estrellas" in et[0] and et[1].startswith("Nivel 37, el actual, ") and et[2].endswith("todavía no") and "meta del tramo" in et[3], "etiquetas accesibles de los nodos")
            chk(pg.js("document.querySelectorAll('ol.nodos').length>=2 && document.querySelector('ol.nodos li button.nodo')!==null", False), "los nodos son una lista de botones")
            # tocar el actual abre ese nivel
            a_la_vista(37); tap_sel('.nodo[data-n="37"]'); time.sleep(0.6)
            i = info()
            chk(i["juegoVisible"] and not i["mapaVisible"] and pg.js("window.__botellas.G.clave", False) == "37", "tocar el actual abre el nivel 37")
            pg.js("window.__botellas.libre()"); pg.js("window.__botellas.aviso()", False); time.sleep(0.4)
            tap_sel("#gBack"); time.sleep(0.5)
            i = info()
            chk(i["mapaVisible"] and not i["juegoVisible"], "al salir del nivel abierto desde el mapa se vuelve al mapa")
            # volver regresa al Inicio
            tap_sel("#mBack"); time.sleep(0.4)
            i = info()
            chk(i["inicioVisible"] and not i["mapaVisible"], "el boton volver del mapa regresa al Inicio")
            # tambien se abre tocando la barra de Proxima meta
            tap_sel("#hProgBar"); time.sleep(0.6)
            chk(info()["mapaVisible"], "tocar la barra de 'Próxima meta' abre el mapa")
            # la barra de abajo juega el actual
            tap_sel("#mJugar"); time.sleep(0.5)
            chk(info()["juegoVisible"] and pg.js("window.__botellas.G.clave", False) == "37", "'Jugar el nivel 37' de la barra de abajo abre el nivel")

            # 2) una zona con meta alcanzada (nivel 60, pareja en el 55): la cima con su ilustracion
            abrir_mapa(estado_mapa(60, 55, visto=60))
            i = info()
            chk(i["zonas"] == 3 and i["hechos"] == 59, "nivel 60: tres zonas dibujadas y 59 hechos (%d zonas, %d hechos)" % (i["zonas"], i["hechos"]))
            chk(pg.js("document.querySelectorAll('.cima').length", False) == 1, "la meta alcanzada (50) muestra la cima")
            a_la_vista(50); time.sleep(0.2)
            pg.foto("v8-03-meta-alcanzada")
            chk(not info()["cruza"], "sin caras sobre los nodos (nivel 60)")
            pg.js("document.getElementById('mScroll').scrollTop = 0", False); time.sleep(0.2)
            pg.foto("v8-03b-zona-siguiente")

            # 3) primer dia: nivel 1, los dos en el mismo nodo
            abrir_mapa(estado_mapa(1, 1, visto=1))
            i = info()
            chk(i["hechos"] == 0 and i["actuales"] == 1 and i["act"]["t"] >= i["sc"]["t"] and i["act"]["b"] <= i["sc"]["b"], "nivel 1: un actual, ningun hecho y a la vista")
            chk(len(i["pines"]) == 2 and not i["cruza"], "nivel 1: las dos caras juntas, sin tapar el nodo")
            chk(i["boton"] == "Jugar el nivel 1", "barra: Jugar el nivel 1")
            pg.foto("v8-04-nivel1")

            # 4) 320 de ancho
            abrir_mapa(estado_mapa(37, 12, visto=37), 320, 640)
            i = info()
            chk(not i["hscroll"] and not i["hscrollMapa"], "320 px sin scroll horizontal")
            chk(not i["cruza"] and not i["corta"], "320 px: sin caras sobre nodos ni textos cortados %s %s" % (i["cruza"], i["corta"]))
            pg.foto("v8-05-320")
            a_la_vista(12); pg.foto("v8-05b-320-pareja")
            a_la_vista(50); pg.foto("v8-05c-320-meta")
            abrir_mapa(estado_mapa(1, 1, visto=1), 320, 640)
            chk(not info()["hscroll"], "320 px, nivel 1, sin scroll horizontal")
            pg.foto("v8-05d-320-nivel1")

            # 5) nivel 1.000: se dibuja rapido (3 zonas + una tarjeta de resumen)
            S1000 = estado_mapa(1000, 300, visto=1000)
            limpio(pg, "", 390, 844, 1.5, S1000)
            pg.js("document.getElementById('hMapa').scrollIntoView({block:'center'}); 1", False); time.sleep(0.2)
            t0 = time.time(); tap_sel("#hMapa"); t_total = time.time() - t0
            time.sleep(0.5)
            i = info()
            ms = pg.js("window.__botellas.mapaMs()", False)
            print("   nivel 1000: render %.0f ms (JS) | toque a mapa listo %.0f ms | zonas %d | nodos %d" % (ms, t_total * 1000, i["zonas"], i["nodosTotal"]))
            chk(i["zonas"] == 3 and i["nodosTotal"] == 150, "nivel 1000: solo 3 zonas dibujadas (150 nodos)")
            chk(i["resumen"] and "Tramos 1 a 18 completos" in i["resumen"] and "Niveles 1 a 900" in i["resumen"] and "Andrés va en el nivel 300" in i["resumen"], "tarjeta de resumen: " + str(i["resumen"]).replace("\n", " | "))
            chk(ms < 150, "el mapa del nivel 1000 se dibuja en menos de 150 ms (%.0f)" % ms)
            chk(i["act"] and i["sc"]["t"] <= i["act"]["t"] and i["act"]["b"] <= i["sc"]["b"], "nivel 1000: el actual a la vista")
            pg.foto("v8-06-nivel1000")
            pg.js("document.getElementById('mScroll').scrollTop = document.getElementById('mScroll').scrollHeight", False); time.sleep(0.3)
            pg.foto("v8-06b-nivel1000-resumen")
            tap_sel('[data-accion="mas"]'); time.sleep(0.4)
            i = info()
            chk(i["zonas"] == 4 and "Tramos 1 a 17 completos" in (i["resumen"] or ""), "'Ver el tramo 18' abre un tramo mas: " + str(i["resumen"]).splitlines()[0])
            # la pareja por encima (nivel 1200 de 1000): aviso arriba
            abrir_mapa(estado_mapa(1000, 1200, visto=1000))
            chk("más arriba, en el nivel 1200" in info()["tope"], "pareja muy por encima: aviso arriba (%s)" % info()["tope"])

            # 6) animacion al volver: avanzaste desde la ultima vez que viste el mapa
            Sa = estado_mapa(37, 12, visto=36)
            limpio(pg, "", 390, 844, 1.5, Sa)
            tap_sel("#hMapa"); time.sleep(0.25)
            pg.js("window.__botellas.pausar(500 + 325)", False); time.sleep(0.2)
            j = json.loads(pg.js("""(()=>{const c=(e)=>{const b=e.getBoundingClientRect(); return [b.left+b.width/2,b.top+b.height/2]}; return JSON.stringify({pin:c(document.querySelector('.pin.yo')), a:c(document.querySelector('.nodo[data-n="36"]')), b:c(document.querySelector('.nodo[data-n="37"]'))})})()""", False))
            ymin, ymax = sorted([j["a"][1], j["b"][1]])
            print("   pin y=%.0f entre nodo 36 (%.0f) y 37 (%.0f)" % (j["pin"][1], j["a"][1], j["b"][1]))
            chk(ymin + 5 < j["pin"][1] < ymax - 5, "a mitad de la animacion la cara va entre el nodo 36 y el 37")
            pg.foto("v8-07-animacion-mitad")
            pg.js("window.__botellas.reanudar()", False); time.sleep(1.8)
            j = json.loads(pg.js("""(()=>{const c=(e)=>{const b=e.getBoundingClientRect(); return [b.left+b.width/2,b.top+b.height/2]}; return JSON.stringify({pin:c(document.querySelector('.pin.yo')), b:c(document.querySelector('.nodo[data-n="37"]'))})})()""", False))
            chk(abs(j["pin"][1] - j["b"][1]) < 4, "al terminar la cara queda en el nodo 37")
            chk(pg.js("JSON.parse(localStorage.getItem('botellas:v1')).perfiles.cami.mapaVisto", False) == 37, "se guarda el ultimo nivel visto (37) en el perfil local")
            chk(pg.js("localStorage.getItem('botellas:v1').indexOf('mapaVisto')>0 && !('mapaVisto' in perfilPublico(P()))", False) is True, "el ultimo nivel visto no viaja a la nube (perfilPublico no lo incluye)")
            # solo una vez: al reabrir no camina
            tap_sel("#mBack"); time.sleep(0.3); tap_sel("#hMapa"); time.sleep(0.4)
            chk(pg.js("document.querySelector('.pin.yo').getAnimations().length", False) == 0, "al reabrir sin avanzar la cara ya no camina")
            # primera vez (sin ultimo visto): tampoco camina
            limpio(pg, "", 390, 844, 1.5, estado_mapa(37, 12))
            tap_sel("#hMapa"); time.sleep(0.4)
            chk(pg.js("document.querySelector('.pin.yo').getAnimations().length", False) == 0, "la primera vez que se abre el mapa no hay animacion")
            # movimiento reducido: sin animacion
            limpio(pg, "", 390, 844, 1.5, estado_mapa(37, 12, visto=36))
            pg.enviar("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
            tap_sel("#hMapa"); time.sleep(0.4)
            chk(pg.js("document.querySelector('.pin.yo').getAnimations().length", False) == 0, "con movimiento reducido la cara no camina")
            pg.enviar("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "no-preference"}])

            # 7) partida a medias: 'Seguir el nivel N'
            Sp = estado_mapa(37, 12, visto=37)
            Sp["partida"] = {"jugador": "cami", "modo": "camino", "ruta": "camino", "clave": "37", "movs": 3, "estado": {"b": [[1]], "ab": 0}}
            abrir_mapa(Sp)
            chk(info()["boton"] == "Seguir el nivel 37", "con partida a medias la barra dice 'Seguir el nivel 37'")

            # 8) otro jugador (Andres) y la pareja Cami: colores y datos del otro perfil local
            abrir_mapa(estado_mapa(20, 8, visto=20, jugador="andres"))
            i = info()
            chk("Cami" in i["pares"] and "nivel 8" in i["pares"] and "nivel 20" in i["pares"], "jugando Andres, la pareja es Cami (%s)" % i["pares"])
            pg.foto("v8-08-andres")

            # 9) dentro de CabriCoach (.enapp): sin dobles margenes ni scroll horizontal; la pareja viene de HOST.leerPareja
            pg.vista(390, 844)
            pg.ir("about:blank", 0.2)
            pg.ir("http://127.0.0.1:8931/", 0.6)
            Sh = estado_mapa(37, 1, visto=37)
            pg.js("""(()=>{ localStorage.clear(); localStorage.setItem('botellas:v1', %s);
              window.__botellasHost = { usuario:'cami', barra:true, perfil:null, guardar(){}, cerrar(){}, leerPareja(){ return { nombre:'Andrés', usuario:'andres', perfil:{ v:3, nivel:12, estrellas:{}, dias:{}, racha:{}, stats:{}, vistos:{} } }; } };
              const mv=document.createElement('meta'); mv.name='viewport'; mv.content='width=device-width,initial-scale=1'; document.head.appendChild(mv);
              const f=document.createElement('iframe'); f.id='bot'; f.style.cssText='position:fixed;inset:0;width:100%%;height:100%%;border:0'; f.src='/botellas-local.html'; document.body.appendChild(f); return 1; })()""" % json.dumps(json.dumps(Sh)), False)
            time.sleep(2.0)
            dentro = lambda c: pg.js("document.getElementById('bot').contentWindow.eval(%s)" % json.dumps(c), False)
            dentro("document.getElementById('hMapa').click(); 1"); time.sleep(0.8)
            r_ = json.loads(dentro("JSON.stringify({enapp:document.documentElement.classList.contains('enapp'), sa:getComputedStyle(document.documentElement).getPropertyValue('--sa-t'), pares:document.getElementById('mPares').innerText, hs:document.documentElement.scrollWidth>document.documentElement.clientWidth, pines:document.querySelectorAll('.pin').length})"))
            print("   en la app:", r_)
            chk(r_["enapp"] and r_["sa"].strip() == "0px" and not r_["hs"] and "Andrés" in r_["pares"] and "nivel 12" in r_["pares"] and r_["pines"] == 2, "dentro de la app: .enapp, sin zonas seguras dobles y la pareja sale de HOST.leerPareja")
            pg.foto("v8-09-en-la-app")

            # 10) el build sin las imagenes nuevas no falla
            hay = [n for n in ("zona1", "zona2", "zona3", "zona4", "cima") if os.path.exists(os.path.join(AQUI, "recursos", n + ".b64"))]
            r2 = subprocess.run([sys.executable, os.path.join(AQUI, "build.py")], capture_output=True, text=True)
            html_ = open(os.path.join(AQUI, "botellas-local.html"), encoding="utf-8").read()
            chk(r2.returncode == 0 and "@IMG?:" not in html_ and "@IMG:" not in html_, "build.py sale bien sin recursos/%s (existen: %s)" % ("zona1.b64 ...", hay or "ninguna"))

            # 11) v9: adornos a los lados del sendero y tinte por zona
            ADOR = """(()=>{ const R=(e)=>{const b=e.getBoundingClientRect(); return {l:b.left,t:b.top,r:b.right,b:b.bottom}};
              const hit=(a,b)=>a.l<b.r&&a.r>b.l&&a.t<b.b&&a.b>b.t, inf=(r,k)=>({l:r.l-k,t:r.t-k,r:r.r+k,b:r.b+k});
              const ad=[...document.querySelectorAll('.ador')].map(e=>({e:e, r:R(e)}));
              const otros=[]; document.querySelectorAll('.nodo').forEach(e=>otros.push(['nodo',inf(R(e),8)]));
              document.querySelectorAll('.sello,.ests,.pin,.cartel,.cima,.cartel .txt').forEach(e=>{ if(!e.hidden) otros.push([e.className.split(' ')[0],R(e)]); });
              const pts=[]; document.querySelectorAll('.camino path').forEach(p=>{ const sv=p.ownerSVGElement, rc=sv.getBoundingClientRect(), vb=sv.viewBox.baseVal, L=p.getTotalLength(); for(let d=0; L>0 && d<=L; d+=5){ const q=p.getPointAtLength(d); pts.push([rc.left+q.x/vb.width*rc.width, rc.top+q.y/vb.height*rc.height]); } });
              const mal=[]; ad.forEach(a=>{ otros.forEach(o=>{ if(hit(a.r,o[1])) mal.push(o[0]); }); if(pts.some(p=>p[0]>a.r.l&&p[0]<a.r.r&&p[1]>a.r.t&&p[1]<a.r.b)) mal.push('sendero');
                const sc=document.getElementById('mCont').getBoundingClientRect(); if(a.r.l<sc.left-1||a.r.r>sc.right+1) mal.push('fuera-ancho'); });
              const sup=ad.filter((a,i)=>ad.some((b,j)=>j>i&&hit(a.r,b.r))).length;
              const porZona={}; document.querySelectorAll('.zona').forEach(z=>{ porZona[z.dataset.z]=z.querySelectorAll('.ador').length; });
              const tam=ad.map(a=>Math.round(a.r.r-a.r.l)); const firma=[...document.querySelectorAll('.ador')].map(e=>e.getAttribute('style')+'|'+e.className).join(';');
              return JSON.stringify({n:ad.length, mal:mal, sup:sup, porZona:porZona, min:Math.min(...tam), max:Math.max(...tam), firma:firma,
                brillan:document.querySelectorAll('.ador.glow').length, fut:document.querySelectorAll('.ador.fut').length, hs:document.documentElement.scrollWidth>document.documentElement.clientWidth||document.getElementById('mScroll').scrollWidth>document.getElementById('mScroll').clientWidth+1,
                tinte:getComputedStyle(document.querySelector('.ruta'),'::before').backgroundImage.slice(0,60)}); })()"""
            def ador():
                v = pg.js(ADOR, False)
                if v is None:
                    print("   ador() fallo:", pg.errores[-1:])
                return json.loads(v)
            def chequeo_ador(etq):
                a = ador()
                print("   %s: %d adornos %s, tamanos %d a %d px, brillan %d, tenues %d, superpuestos %d" % (etq, a["n"], a["porZona"], a["min"], a["max"], a["brillan"], a["fut"], a["sup"]))
                chk(a["n"] >= 15 and all(v >= 8 for v in a["porZona"].values()), "%s: hay adornos en cada zona dibujada" % etq)
                chk(not a["mal"], "%s: ningun adorno toca nodos, sellos, estrellas, caras, carteles, cima ni sendero %s" % (etq, sorted(set(a["mal"]))))
                chk(a["sup"] == 0 and a["min"] >= 36 and a["max"] <= 80, "%s: sin adornos superpuestos y tamanos entre 40 y 76" % etq)
                chk(not a["hs"], "%s: sin scroll horizontal" % etq)
                return a
            casos = [(1, 1, "pradera-nivel1"), (37, 12, "pradera-nivel37"), (60, 55, "bosque-nivel60"), (120, 90, "nieve-nivel120"), (170, 160, "cumbre-nivel170")]
            n_cap = 0
            for (w, h) in ((390, 844), (320, 640)):
                for (Lx, Px, nom) in casos:
                    abrir_mapa(estado_mapa(Lx, Px, visto=Lx), w, h)
                    a = chequeo_ador("%s a %d" % (nom, w))
                    n_cap += 1
                    pg.foto("v9-%02d-%s-%d" % (n_cap, nom, w))
                # paso entre dos zonas: el cartel del tramo 2 a media pantalla
                abrir_mapa(estado_mapa(60, 55, visto=60), w, h)
                pg.js("(()=>{const c=document.querySelector('.zona[data-z=\"1\"] .cartel'); const sc=document.getElementById('mScroll'); const r=c.getBoundingClientRect(), s=sc.getBoundingClientRect(); sc.scrollTop += (r.top-s.top)+r.height/2-sc.clientHeight/2; return 1})()", False); time.sleep(0.3)
                n_cap += 1
                pg.foto("v9-%02d-paso-entre-zonas-%d" % (n_cap, w))
                chk(not ador()["mal"], "paso entre zonas a %d: sin cruces" % w)
            # lo futuro mas tenue que lo recorrido (a color pleno)
            ops = json.loads(pg.js("""(()=>{const f=document.querySelector('.ador.fut'), n=[...document.querySelectorAll('.ador:not(.fut):not(.glow)')][0]; return JSON.stringify([f?+getComputedStyle(f).opacity:null, n?+getComputedStyle(n).opacity:null])})()""", False))
            chk(ops[0] is not None and ops[1] == 1 and ops[0] < 0.7, "adornos de lo que falta atenuados (%s) y lo recorrido a pleno (%s)" % (ops[0], ops[1]))
            # tinte propio por zona
            tn = pg.js("JSON.stringify([...document.querySelectorAll('.ruta')].map(r=>getComputedStyle(r).getPropertyValue('--t').trim()).filter((v,i,a)=>a.indexOf(v)===i))", False)
            chk(len(json.loads(tn)) == 3, "cada zona tiene su propio tinte: " + tn)
            # misma posicion tras recargar
            abrir_mapa(estado_mapa(37, 12, visto=37)); f1 = ador()["firma"]
            pg.js("location.reload()", False); time.sleep(1.8)
            pg.js("document.getElementById('hMapa').scrollIntoView({block:'center'}); 1", False); time.sleep(0.2)
            tap_sel("#hMapa"); time.sleep(0.8)
            chk(f1 and ador()["firma"] == f1, "los adornos quedan en el mismo lugar tras recargar (%d caracteres de firma)" % len(f1))
            # nivel 1000 sigue rapido
            limpio(pg, "", 390, 844, 1.5, estado_mapa(1000, 300, visto=1000))
            pg.js("document.getElementById('hMapa').scrollIntoView({block:'center'}); 1", False); time.sleep(0.2)
            tap_sel("#hMapa"); time.sleep(0.6)
            ms = pg.js("window.__botellas.mapaMs()", False); a = ador()
            print("   nivel 1000 con adornos: render %.0f ms | %d adornos" % (ms, a["n"]))
            chk(ms < 250 and not a["mal"] and a["n"] >= 30, "nivel 1000 con adornos sigue rapido (%.0f ms) y sin cruces" % ms)
            pg.foto("v9-%02d-nivel1000" % (n_cap + 1))
            # movimiento reducido: las luces no parpadean
            pg.enviar("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
            abrir_mapa(estado_mapa(120, 90, visto=120))
            chk(pg.js("[...document.querySelectorAll('.ador.glow')].every(e=>e.getAnimations().length===0)", False), "con movimiento reducido los adornos que brillan no animan")
            pg.enviar("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "no-preference"}])
            abrir_mapa(estado_mapa(120, 90, visto=120))
            chk(pg.js("[...document.querySelectorAll('.ador.glow')].some(e=>e.getAnimations().length>0)", False), "sin movimiento reducido las luces parpadean muy lento")
            # sin las hojas el mapa funciona como antes
            r_ = pg.js("""(()=>{ const g=['adorPradera','adorBosque','adorNieve','adorCumbre'], g0=g.map(k=>IMG[k]); g.forEach(k=>{IMG[k]=''}); pintarMapa({}); const sin=document.querySelectorAll('.ador').length, nod=document.querySelectorAll('.nodo').length, ad=document.querySelectorAll('.adornos').length; g.forEach((k,i)=>{IMG[k]=g0[i]}); pintarMapa({}); return JSON.stringify({sin:sin, nod:nod, ad:ad, con:document.querySelectorAll('.ador').length}); })()""", False)
            r_ = json.loads(r_)
            chk(r_["sin"] == 0 and r_["ad"] == 0 and r_["nod"] > 100 and r_["con"] > 0, "sin las hojas no hay adornos y el mapa sigue igual: %s" % r_)
            tam = os.path.getsize(os.path.join(AQUI, "botellas.html"))
            print("   peso final de botellas.html: %.0f KB" % (tam / 1024))
            print("mapa: %s" % ("sin fallas" if not fallas_mapa else "FALLAS: %s" % fallas_mapa))
            pg.errores.extend(["mapa: " + f for f in fallas_mapa])
        if todo or "zona" in which:
            # v7: la zona del nivel dentro del juego (fondo, adornos, ambiente, cabecera y victoria)
            fallas_zona = []
            def chk(cond, msg):
                print(("OK    " if cond else "FALLA ") + msg)
                if not cond:
                    fallas_zona.append(msg)
            ZONA = """(()=>{ const R=(e)=>{const b=e.getBoundingClientRect(); return {l:b.left,t:b.top,r:b.right,b:b.bottom}}, hit=(a,b)=>a.l<b.r&&a.r>b.l&&a.t<b.b&&a.b>b.t;
              const fx=document.getElementById('zonaFx'), ad=[...fx.querySelectorAll('.ador'), ...document.querySelectorAll('.labo')], bd=R(document.getElementById('board'));
              const cab=document.getElementById('cabrito'); let cabR=null; if(!cab.hidden){ const b=R(cab), w=b.r-b.l, h=b.b-b.t; cabR={l:b.l+0.18*w, r:b.r-0.18*w, t:b.t+0.04*h, b:b.b}; }
              const ob=[...document.querySelectorAll('#board .slot,#board .caja,#board .llave,#strip:not([hidden]),#gCtl,#gTop,#aviso:not([hidden])')];
              const mal=[]; ad.forEach(a=>{ const r=R(a); ob.forEach(o=>{ if(hit(r,R(o))) mal.push(o.id||o.className.split(' ')[0]); }); if(r.l<bd.l-1||r.r>bd.r+1||r.t<bd.t-1||r.b>bd.b+1) mal.push('fuera-del-tablero');
                const e=document.elementFromPoint((r.l+r.r)/2,(r.t+r.b)/2); if(e && fx.contains(e)) mal.push('recibe-toques'); if(cabR && hit(r,cabR)) mal.push('cabrito'); });
              if(cabR){ ob.forEach(o=>{ if(o.id!=='gCtl' && hit(cabR,R(o))) mal.push('cabrito-'+(o.id||o.className.split(' ')[0])); }); document.querySelectorAll('#board .repisa').forEach(o=>{ if(hit(cabR,R(o))) mal.push('cabrito-repisa'); }); }
              const reps=[...document.querySelectorAll('.repisa')].map(e=>{ const sh=R(e), row=e.parentElement, sl=[...row.querySelectorAll('.slot')].map(R); const fondo=Math.max(...sl.map(r=>r.b)); return {dy:+(sh.t-fondo).toFixed(1), dentro:sh.l>=bd.l-1&&sh.r<=bd.r+1, cubre:sh.l<=Math.min(...sl.map(r=>r.l))&&sh.r>=Math.max(...sl.map(r=>r.r))}; });
              const filas=document.querySelectorAll('#board .brow').length;
              const cs=getComputedStyle(fx), pais=getComputedStyle(fx.querySelector('.zpais'));
              const anims=document.getAnimations().filter(a=>a.effect&&a.effect.target&&fx.contains(a.effect.target));
              const tit=document.getElementById('gTop'), zt=document.getElementById('gZona');
              return JSON.stringify({ clase:fx.className, n:fx.querySelectorAll('.ador').length, clasesAd:[...fx.querySelectorAll('.ador')].map(a=>a.className.split(' ')[1]), mal:mal, pe:cs.pointerEvents, nlabo:document.querySelectorAll('.labo').length, cabrito:!cab.hidden, cabW:cab.hidden?0:Math.round(R(cab).r-R(cab).l), cabFig:cab.hidden?0:Math.round(0.96*(R(cab).b-R(cab).t)), cabEnBarra:!cab.hidden && R(cab).b<=R(document.getElementById('gCtl')).b+1 && R(cab).b>=R(document.getElementById('gCtl')).b-12, cabPose:cab._pose, repisas:reps, filas:filas, img:pais.backgroundImage.slice(0,22), amb:fx.querySelectorAll('.zamb i').length, anims:anims.length,
                pausa:fx.classList.contains('pausa'), play:anims.map(a=>a.playState).join(','), zonaTxt:zt.hidden?null:zt.textContent, gtopW:tit.scrollWidth<=tit.clientWidth+1, gtopH:Math.round(tit.getBoundingClientRect().height),
                hs:document.documentElement.scrollWidth>document.documentElement.clientWidth, firma:ad.map(a=>a.getAttribute('style')).join(';'), boardH:Math.round(bd.b-bd.t) }); })()"""
            def zona():
                return json.loads(pg.js(ZONA, False))
            def L_de(zi_abs, pred):
                return buscar(lambda n: 50 * zi_abs < n["L"] <= 50 * (zi_abs + 1) and pred(n))
            nombres = ["pradera", "bosque", "nieve", "cumbre"]
            ncap = [0]
            def foto10(nombre):
                ncap[0] += 1
                pg.foto("v10-%02d-%s" % (ncap[0], nombre))
            # 1) fondo, adornos y ambiente de la zona correcta, en las 4 zonas y en una vuelta (nivel 201+)
            casos = [(15, 0), (75, 1), (130, 2), (180, 3), (230, 0), (260, 1)]
            for (Lx, zi) in casos:
                abrir(pg, "#nivel%d" % Lx, estado(Lx))
                z = zona()
                print("   nivel %d: %s, %d adornos %s, ambiente %d, animaciones %d, texto '%s'" % (Lx, z["clase"], z["n"], z["clasesAd"], z["amb"], z["anims"], z["zonaTxt"]))
                chk(("zz%d" % zi) in z["clase"] and z["img"].startswith("var(") is False, "nivel %d: capa de la zona %s" % (Lx, nombres[zi]))
                chk(z["n"] <= 3 and all(c == "z%d" % zi for c in z["clasesAd"]), "nivel %d: hasta 3 adornos y todos de la hoja de %s" % (Lx, nombres[zi]))
                chk(not z["mal"] and z["pe"] == "none", "nivel %d: ningun adorno toca botellas, cajas, llaves, barra, cabecera ni recibe toques %s" % (Lx, sorted(set(z["mal"]))))
                chk(z["amb"] == 7 and z["anims"] > 0, "nivel %d: ambiente de %s con animacion lenta" % (Lx, nombres[zi]))
                chk(len(z["repisas"]) == z["filas"] and all(r["cubre"] and r["dentro"] and -6 <= r["dy"] <= 1 for r in z["repisas"]), "nivel %d: una repisa bajo cada una de las %d filas, apoyada donde acaban las botellas %s" % (Lx, z["filas"], [r["dy"] for r in z["repisas"]]))
                print("      laboratorio %d, cabrito %s (%d px)" % (z["nlabo"], z["cabrito"], z["cabW"]))
            # al menos en uno de ellos hay adornos (si no, la prueba no dice nada)
            tot = 0
            for Lx in (15, 75, 130, 180):
                abrir(pg, "#nivel%d" % Lx, estado(Lx)); tot += zona()["n"]
            chk(tot >= 6, "entre los niveles de prueba hay adornos en el suelo (%d)" % tot)
            # 2) reto del dia: zona fija por fecha
            abrir(pg, "#dia", estado(1))
            z1 = zona(); abrir(pg, "#dia", estado(1)); z2 = zona()
            chk(z1["clase"] == z2["clase"] and z1["firma"] == z2["firma"] and z1["zonaTxt"] is None and not z1["mal"], "reto del dia: zona fija (%s), sin linea de meta y sin cruces" % z1["clase"])
            # 3) cabecera y victoria a 390 y 320, y un Extra dificil de cada zona para ver la lectura
            for zi in range(4):
                Lx = L_de(zi, lambda n: n["dif"] == "extra" and (n.get("ocultas") or n["candados"]) and n["cajas"]) if zi else L_de(zi, lambda n: n["dif"] == "extra" and (n.get("ocultas") or n["candados"]))
                for (w, h) in ((390, 844), (320, 640)):
                    abrir(pg, "#nivel%d" % Lx, estado(Lx), w, h)
                    z = zona()
                    print("   Extra de %s: nivel %d a %d px: tablero %d px alto, cabecera %d px, '%s', adornos %d" % (nombres[zi], Lx, w, z["boardH"], z["gtopH"], z["zonaTxt"], z["n"]))
                    chk(z["gtopW"] and not z["hs"] and not z["mal"], "Extra de %s a %d px: cabecera sin desbordar, sin scroll horizontal y sin cruces" % (nombres[zi], w))
                    foto10("extra-%s-%d" % (nombres[zi], w))
            # niveles normales: cajas (15), gigante (75) y uno de nieve (130), a 390 y 320
            for (Lx, w, h) in ((15, 390, 844), (15, 320, 640), (75, 390, 844), (75, 320, 640), (130, 390, 844), (130, 320, 640)):
                abrir(pg, "#nivel%d" % Lx, estado(Lx), w, h)
                z = zona()
                chk(not z["mal"] and not z["hs"] and z["gtopW"], "nivel %d a %d px: sin cruces ni desborde (laboratorio %d, cabrito %s)" % (Lx, w, z["nlabo"], z["cabrito"]))
                foto10("nivel%d-%d" % (Lx, w))
            # textos de la cabecera
            esperado = {75: "El bosque · faltan 25 para la meta", 99: "El bosque · falta 1 para la meta", 100: "La meta del bosque", 50: "La meta de la pradera", 200: "La meta de la cumbre"}
            for Lx, txt in esperado.items():
                abrir(pg, "#nivel%d" % Lx, estado(Lx)); t = zona()["zonaTxt"]
                chk(t == txt, "cabecera nivel %d: '%s'" % (Lx, t))
            # 4) sin cruces tras girar o cambiar de tamano (el tablero se vuelve a medir)
            abrir(pg, "#nivel75", estado(75))
            for (w, h) in ((320, 640), (390, 844), (844, 390), (390, 844)):
                pg.vista(w, h); time.sleep(0.6)
                z = zona()
                chk(not z["mal"] and not z["hs"], "tras cambiar a %dx%d: adornos sin cruces (%d) y sin scroll horizontal" % (w, h, z["n"]))
            foto10("tras-girar")
            # 5) movimiento reducido: ni ambiente ni animaciones
            pg.enviar("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
            abrir(pg, "#nivel130", estado(130))
            z = zona()
            chk(z["amb"] == 0 and z["anims"] == 0, "con movimiento reducido no hay ambiente ni animacion (ambiente %d, animaciones %d)" % (z["amb"], z["anims"]))
            pg.enviar("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "no-preference"}])
            # 6) pausa: juego en pausa y pestana oculta detienen el ambiente
            abrir(pg, "#nivel180", estado(180))
            pg.js("window.__botellas.G.pausa = true", False); time.sleep(1.3)
            z = zona(); chk(z["pausa"] and set(z["play"].split(",")) <= {"paused"}, "con el juego en pausa el ambiente se detiene (%s)" % z["play"])
            pg.js("window.__botellas.G.pausa = false", False); time.sleep(1.3)
            z = zona(); chk(not z["pausa"], "al reanudar el ambiente sigue")
            pg.js("Object.defineProperty(document, 'hidden', {configurable:true, get:()=>true}); document.dispatchEvent(new Event('visibilitychange')); 1", False); time.sleep(0.2)
            z = zona(); chk(z["pausa"], "con la pestana oculta el ambiente se detiene")
            pg.js("Object.defineProperty(document, 'hidden', {configurable:true, get:()=>false}); document.dispatchEvent(new Event('visibilitychange')); 1", False)
            # 7) los adornos no cambian la logica de toques: un toque en un adorno no hace nada y seleccionar/soltar sigue igual
            def toque(tipo, x, y):
                pg.enviar("Input.dispatchTouchEvent", type=tipo, touchPoints=([{"x": x, "y": y}] if tipo != "touchEnd" else []))
            abrir(pg, "#nivel12", estado(12))
            ad = json.loads(pg.js("JSON.stringify([...document.querySelectorAll('#zonaFx .ador')].map(a=>{const b=a.getBoundingClientRect(); return [b.left+b.width/2,b.top+b.height/2]}))", False))
            if ad:
                toque("touchStart", ad[0][0], ad[0][1]); time.sleep(0.05); toque("touchEnd", ad[0][0], ad[0][1]); time.sleep(0.3)
                chk(pg.js("window.__botellas.G.sel", False) is None and pg.js("window.__botellas.G.movs", False) == 0, "tocar un adorno no selecciona ni mueve nada")
            def centro(i):
                return json.loads(pg.js("(()=>{const r=document.querySelector('#board .slot[data-i=\"%d\"]').getBoundingClientRect(); return JSON.stringify([r.left+r.width/2, r.top+r.height/2])})()" % i, False))
            i0 = pg.js("(()=>{const b=window.__botellas, G=b.G; for(let i=0;i<G.estado.b.length;i++){ if(G.estado.b[i].length && !b.motor.completa(G.estado.b[i], G.u) && !b.motor.cerrada(G.estado, i, G.nv)) return i; } return -1; })()", False)
            c0 = centro(i0); toque("touchStart", *c0); time.sleep(0.05); toque("touchEnd", *c0); time.sleep(0.3)
            chk(pg.js("window.__botellas.G.sel", False) == i0, "tocar una botella la selecciona")
            toque("touchStart", 195, 60); time.sleep(0.05); toque("touchEnd", 195, 60); time.sleep(0.3)
            chk(pg.js("window.__botellas.G.sel", False) is None, "tocar afuera suelta la seleccion")
            # 8) mismo nivel, mismos adornos tras recargar
            abrir(pg, "#nivel75", estado(75)); f1 = zona()["firma"]
            abrir(pg, "#nivel75", estado(75)); f2 = zona()["firma"]
            chk(f1 == f2, "los adornos de un nivel son fijos (%s)" % (f1[:60] or "ninguno"))
            # 9) dentro de la app (.enapp)
            abrir(pg, "#nivel130", estado(130))
            pg.js("document.documentElement.classList.add('enapp'); window.dispatchEvent(new Event('resize')); 1", False); time.sleep(0.5)
            z = zona(); chk(not z["hs"] and not z["mal"] and z["gtopW"], "dentro de la app: sin desborde ni cruces")
            # 10) sin las hojas ni los paisajes el juego funciona igual
            abrir(pg, "#nivel75", estado(75))
            r_ = json.loads(pg.js("""(()=>{ const ks=['adorPradera','adorBosque','adorNieve','adorCumbre']; const g0=ks.map(k=>IMG[k]); ks.forEach(k=>{IMG[k]=''}); medir(); const sin=document.querySelectorAll('#zonaFx .ador').length; ks.forEach((k,i)=>{IMG[k]=g0[i]}); medir(); return JSON.stringify({sin:sin, slots:document.querySelectorAll('#board .slot').length}); })()""", False))
            chk(r_["sin"] == 0 and r_["slots"] > 0, "sin las hojas no hay adornos y el tablero sigue igual %s" % r_)
            # 10a) el cabrito vive en la barra de abajo y se ve siempre: niveles 15, 37, 75, 130 y 161 a 390 y 320, con el aviso de sin salida y tras ganar
            for (Lx, w, h) in [(a_, b_, c_) for a_ in (15, 37, 75, 130, 161) for (b_, c_) in ((390, 844), (320, 640))]:
                min_fig = 70 if w >= 360 else 58
                abrir(pg, "#nivel%d" % Lx, estado(Lx), w, h)
                z = zona()
                chk(z["cabrito"] and z["cabFig"] >= min_fig and z["cabEnBarra"] and not z["mal"], "nivel %d a %d px: cabrito en la barra, visible (%d px de alto) y sin cruces %s" % (Lx, w, z["cabFig"], sorted(set(z["mal"]))))
                foto10("cabrito-barra-%d-%d" % (Lx, w)) if Lx in (75, 161) else None
                pg.js("window.__botellas.sinSalida()", False); time.sleep(0.6)
                z = zona()
                chk(z["cabrito"] and z["cabFig"] >= min_fig - 8 and z["cabPose"] == 2 and not z["mal"], "nivel %d a %d px con el aviso de sin salida: cabrito visible (%d px) y pensando, sin tapar el aviso %s" % (Lx, w, z["cabFig"], sorted(set(z["mal"]))))
                if Lx in (75, 15): foto10("sin-salida-%d-%d" % (Lx, w))
                pg.js("document.getElementById('strip').hidden = true; setTimeout(medir, 0); 1", False); time.sleep(0.5)
                pg.js("window.__botellas.G.ganado = true; refrescarPose()", False); time.sleep(0.4)
                z = zona()
                chk(z["cabrito"] and z["cabFig"] >= min_fig and z["cabPose"] == 3 and not z["mal"], "nivel %d a %d px tras ganar: cabrito visible y celebrando" % (Lx, w))
            # tras ganar de verdad (hoja de victoria abierta) el cabrito sigue en la barra
            abrir(pg, "#nivel15", estado(15)); pg.js("window.__botellas.novedad()", False); pg.js("window.__botellas.resolver(0)"); time.sleep(0.6)
            z = zona(); chk(z["cabrito"] and z["cabPose"] == 3, "victoria real del nivel 15: cabrito celebrando en la barra")
            # Andres, dentro de la app (.enapp)
            abrir(pg, "#nivel75", estado(75, jugador="andres"))
            pg.js("document.documentElement.classList.add('enapp'); window.dispatchEvent(new Event('resize')); 1", False); time.sleep(0.6)
            z = zona(); chk(z["cabrito"] and z["cabFig"] >= 70 and z["cabEnBarra"] and not z["mal"] and not z["hs"], "Andres dentro de la app: cabrito en la barra (%d px) sin cruces" % z["cabFig"])
            foto10("andres-barra-app")
            # 10b) elementos del juego: el cabrito reacciona, la repisa se queda al arrastrar, y sin imagenes hay respaldo
            abrir(pg, "#nivel15", estado(15))
            chk(pg.js("!document.getElementById('cabrito').hidden", False), "nivel 15: el cabrito de Cami esta en una esquina")
            chk(pg.js("document.getElementById('cabrito')._pose", False) == 0, "pose por defecto: mira")
            pg.js("window.__poses = new Set(); setInterval(()=>window.__poses.add(document.getElementById('cabrito')._pose), 40); 1", False)
            pg.js("window.__botellas.sinSalida()", False); time.sleep(0.4)
            chk(pg.js("document.getElementById('cabrito')._pose", False) == 2, "con el aviso de sin salida el cabrito piensa")
            foto10("cabrito-piensa")
            pg.js("window.__botellas.libre()"); pg.js("document.getElementById('strip').hidden = true", False); time.sleep(1.2)
            chk(pg.js("document.getElementById('cabrito')._pose", False) == 0, "al quitarse el aviso vuelve a mirar")
            pg.js("window.__botellas.novedad()", False)
            pg.js("window.__botellas.resolver(0)"); time.sleep(1.0)
            ps = sorted(json.loads(pg.js("JSON.stringify([...window.__poses])", False)))
            print("   poses vistas durante la partida:", ps)
            chk(1 in ps and 3 in ps and pg.js("document.getElementById('cabrito')._pose", False) == 3, "el cabrito anima al completar una botella y gana al terminar")
            foto10("cabrito-gana")
            abrir(pg, "#nivel15", estado(15))
            pg.js("window.__botellas.libre()"); pg.js("reaccionar(1200)", False); time.sleep(0.2)
            a1 = pg.js("document.getElementById('cabrito')._pose", False); time.sleep(1.5)
            chk(a1 == 1 and pg.js("document.getElementById('cabrito')._pose", False) == 0, "anima unos 1,2 s y vuelve a mirar")
            pg.enviar("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
            abrir(pg, "#nivel15", estado(15)); pg.js("ponerPose(1)", False)
            chk(pg.js("(()=>{const c=document.getElementById('cabrito'); return c.classList.contains('seco') && !c.classList.contains('salto') && parseFloat(getComputedStyle(c.children[0]).transitionDuration)<0.001})()", False), "con movimiento reducido el cabrito cambia de pose en seco")
            pg.enviar("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "no-preference"}])
            abrir(pg, "#nivel15", estado(15, jugador="andres"))
            chk(pg.js("document.getElementById('cabrito').style.getPropertyValue('--reacimg').indexOf('url(')===0 && IMG.reacA.length>1000", False), "jugando Andres sale su cabrito")
            foto10("andres")
            abrir(pg, "#nivel15", estado(15))
            REPS = "JSON.stringify([...document.querySelectorAll('.repisa')].map(e=>{const b=e.getBoundingClientRect(); return [Math.round(b.left),Math.round(b.top),Math.round(b.width)]}))"
            r0 = pg.js(REPS, False)
            c3 = json.loads(pg.js("(()=>{const r=document.querySelector('#board .slot[data-i=\"3\"]').getBoundingClientRect(); return JSON.stringify([r.left+r.width/2, r.top+r.height/2])})()", False))
            toque("touchStart", *c3); time.sleep(0.05)
            for k in range(1, 7):
                toque("touchMove", c3[0] - 8 * k, c3[1] - 10 * k); time.sleep(0.03)
            time.sleep(0.1)
            r1 = pg.js(REPS, False)
            foto10("arrastrando")
            toque("touchEnd", 0, 0); time.sleep(0.4)
            chk(r0 == r1, "al arrastrar una botella las repisas se quedan quietas")
            SINIMG = "(()=>{ const ks=['repisa','labo','reacC','reacA'], g0=ks.map(k=>IMG[k]); ks.forEach(k=>{IMG[k]=''}); medir(); const o={ repisas:document.querySelectorAll('.repisa').length, conimg:document.querySelectorAll('.repisa.conimg').length, labo:document.querySelectorAll('.labo').length, cab:!document.getElementById('cabrito').hidden, fondo:getComputedStyle(document.querySelector('.repisa')).backgroundImage.slice(0,15), ador:document.querySelectorAll('#zonaFx .ador').length }; ks.forEach((k,i)=>{IMG[k]=g0[i]}); medir(); return JSON.stringify(o); })()"
            r_ = json.loads(pg.js(SINIMG, False))
            chk(r_["repisas"] > 0 and r_["conimg"] == 0 and r_["labo"] == 0 and not r_["cab"] and "gradient" in r_["fondo"] and r_["ador"] > 0, "sin repisa, labo ni reacC/reacA: tabla CSS de respaldo, sin laboratorio ni cabrito %s" % r_)
            # 11) victoria normal (linea de avance) y de meta (cima y texto)
            for (Lx, tit, ztxt) in ((75, "Nivel superado", "Te faltan 24 para la meta del bosque"), (99, "Nivel superado", "El siguiente nivel es la meta del bosque"), (100, "¡Coronaste el bosque!", "Llegaste a la meta del bosque. Sigue el tramo 3.")):
                abrir(pg, "#nivel%d" % Lx, estado(Lx))
                pg.js("window.__botellas.novedad()", False)
                pg.js("window.__botellas.resolver(0)"); time.sleep(1.4)
                v = json.loads(pg.js("JSON.stringify({tit:document.getElementById('wTit').textContent, z:document.getElementById('wZona').textContent, zh:document.getElementById('wZona').hidden, cima:document.getElementById('wImg').classList.contains('metacima'), src:document.getElementById('wImg').src.slice(0,11), on:document.getElementById('veloWin').classList.contains('on'), hs:document.documentElement.scrollWidth>document.documentElement.clientWidth})", False))
                print("   victoria %d: %s" % (Lx, v))
                chk(v["on"] and v["tit"] == tit and v["z"] == ztxt and (v["cima"] == (Lx % 50 == 0)) and not v["hs"], "victoria del nivel %d: '%s' / '%s'" % (Lx, v["tit"], v["z"]))
                foto10("victoria-%d" % Lx)
            pg.vista(320, 640); time.sleep(0.4); foto10("victoria-meta-320")
            abrir(pg, "#dia", estado(1)); pg.js("window.__botellas.novedad()", False); pg.js("window.__botellas.resolver(0)"); time.sleep(1.4)
            chk(pg.js("document.getElementById('wZona').hidden", False) and pg.js("document.getElementById('wTit').textContent", False) == "Reto del día resuelto", "victoria del reto del dia: sin linea de meta")
            print("zona: %s" % ("sin fallas" if not fallas_zona else "FALLAS: %s" % fallas_zona))
            pg.errores.extend(["zona: " + f for f in fallas_zona])
        print("errores:", pg.errores if pg.errores else "ninguno")
    finally:
        pg.cerrar()
