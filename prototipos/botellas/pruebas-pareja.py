#!/usr/bin/env python3
"""Punta a punta de Botellas en CabriCoach con dos telefonos (dos Chrome con perfiles aparte)
contra herramientas/nube_falsa.py. Desde la raiz del repo:
  python3 herramientas/nube_falsa.py 9150 &  python3 -m http.server 8932 &
  python3 prototipos/botellas/pruebas-pareja.py   (las capturas quedan en capturas/)"""
import json, os, shutil, subprocess, tempfile, time, urllib.request, base64
import websocket

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
APP = "http://127.0.0.1:8932/coach-afc-v2.html"
NUBE = "http://127.0.0.1:9150"
HOUSE = "prueba-botellas"
SP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "capturas")
FALLOS = []


def nube(path, body=None):
    req = urllib.request.Request(NUBE + path, data=(json.dumps(body).encode() if body is not None else None),
                                 method='POST' if body is not None else 'GET', headers={'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))


def ok(cond, msg):
    print(('OK   ' if cond else 'FALLA ') + msg)
    if not cond: FALLOS.append(msg)


class Tel:
    def __init__(self, nombre, puerto):
        self.nombre = nombre
        self.tmp = tempfile.mkdtemp(prefix="e2e-" + nombre + "-")
        self.proc = subprocess.Popen([CHROME, "--headless=new", "--remote-debugging-port=%d" % puerto, "--user-data-dir=" + self.tmp,
                                      "--no-first-run", "--remote-allow-origins=*", "--no-default-browser-check", "--hide-scrollbars", "about:blank"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        url = None
        for _ in range(80):
            try:
                pg = [x for x in json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % puerto)) if x.get("type") == "page"]
                if pg: url = pg[0]["webSocketDebuggerUrl"]; break
            except Exception: pass
            time.sleep(0.25)
        self.ws = websocket.create_connection(url, max_size=None, timeout=90)
        self.n = 0; self.errores = []
        self.send("Page.enable"); self.send("Runtime.enable")
        self.send("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=2, mobile=True)

    def send(self, m, **p):
        self.n += 1; mi = self.n
        self.ws.send(json.dumps({"id": mi, "method": m, "params": p}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get("method") == "Runtime.exceptionThrown":
                self.errores.append(json.dumps(r["params"]["exceptionDetails"])[:300])
            if r.get("id") == mi: return r.get("result", {})

    def js(self, e):
        r = self.send("Runtime.evaluate", expression=e, awaitPromise=True, returnByValue=True)
        if "exceptionDetails" in r: self.errores.append("eval: " + json.dumps(r["exceptionDetails"])[:300])
        return r.get("result", {}).get("value")

    def ir(self, url, t=2.5):
        self.send("Page.navigate", url=url); time.sleep(t)

    def foto(self, nombre):
        r = self.send("Page.captureScreenshot", format="png")
        ruta = os.path.join(SP, nombre + ".png")
        open(ruta, "wb").write(base64.b64decode(r["data"])); print("captura", ruta)

    def preparar(self, uid, limpiar=True):
        self.ir(APP, 2)
        self.js("""(async()=>{ const rs = await navigator.serviceWorker.getRegistrations(); for(const r of rs) await r.unregister();
          const ks = await caches.keys(); for(const k of ks) await caches.delete(k); return 1 })()""")
        if limpiar: self.js("localStorage.clear(); 1")
        self.js("localStorage.setItem('afc2:uid', %s); localStorage.setItem('afc2:sb', JSON.stringify({url:%s, key:'sb_prueba', house:%s})); localStorage.removeItem('afc2:sbsucio'); 1"
                % (json.dumps(uid), json.dumps(NUBE), json.dumps(HOUSE)))
        self.ir(APP, 4)

    def abrir_juego(self):
        self.js("ACTIONS.botellasAbrir({}); 1")
        for _ in range(60):
            if self.js("(()=>{ const f=document.querySelector('#botlayer iframe'); try{ return !!(f && f.contentWindow && f.contentWindow.eval('typeof G !== \"undefined\" && typeof pintarInicio === \"function\"')); }catch(e){ return false } })()"):
                break
            time.sleep(0.25)
        time.sleep(1.5)

    def en_juego(self, codigo):
        return self.js("(()=>{ const f=document.querySelector('#botlayer iframe'); return f.contentWindow.eval(%s); })()" % json.dumps(codigo))

    def ganar_nivel(self, L):
        # juega la solucion del motor con toques reales dentro del iframe
        return self.js("""(async()=>{ const w=document.querySelector('#botlayer iframe').contentWindow;
          return await w.eval(`(async()=>{
            abrirJuego('camino','camino',%d);
            const libre = async()=>{ for(let k=0;k<400;k++){ if(G && G.estado && !G.busy) return true; await esperar(25); } return false; };
            await esperar(300);
            for(const id of ['nOk']){ const b=document.getElementById(id); const v=document.getElementById('veloNov'); if(v && v.classList.contains('on') && b) b.click(); }
            await esperar(1700); await libre();
            const sol = MOTOR.resolver(G.estado, G.nv).movs;
            for(const m of sol){ tocar(m[0]); await esperar(120); tocar(m[1]); await esperar(80); await libre(); }
            await esperar(900);
            return sol.length; })()`); })()""" % L)

    def cerrar(self):
        try: self.ws.close()
        except Exception: pass
        self.proc.terminate(); time.sleep(0.4); shutil.rmtree(self.tmp, ignore_errors=True)


def fila(uid):
    for f in nube('/__dump')['filas']:
        if f['house'] == HOUSE and f['uid'] == uid and f['k'] == 'botellas': return f['v']
    return None


cami = Tel("cami", 9401)
andres = Tel("andres", 9402)
try:
    # 1) Cami juega y gana los niveles 1 y 2 en su telefono: su progreso sube a la nube
    cami.preparar('cami')
    cami.abrir_juego()
    ok(cami.en_juego("HOST && HOST.usuario") == 'cami', "el juego en el telefono de Cami juega como Cami")
    cami.ganar_nivel(1); cami.ganar_nivel(2)
    time.sleep(2.5)
    v = fila('cami')
    ok(bool(v) and v.get('nivel') == 3, "la nube tiene el perfil de Cami en el nivel 3: %s" % (v and v.get('nivel')))
    posts = [p for p in nube('/__dump')['posts'] if p == 'cami|botellas']
    print("subidas de cami|botellas:", len(posts))
    ok(0 < len(posts) <= 6, "guardar sube solo cuando cambia el perfil (no en cada jugada)")
    cami.en_juego("cerrarJuego && cerrarJuego(); 1"); time.sleep(0.6)
    cami.foto("e2e-1-cami-inicio")

    # 2) Andres abre su telefono: ve a Cami en el nivel 3 en Retos y en el juego
    andres.preparar('andres')
    tarjeta = andres.js("(()=>{ const s=document.querySelector('.botcard'); return s ? s.textContent.replace(/\\s+/g,' ').trim() : (typeof vRetos==='function' ? vRetos().replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ').slice(0,4000) : '') })()")
    print("tarjeta de Andres:", (tarjeta or '')[:300])
    ok('Cami' in (tarjeta or '') and '3' in (tarjeta or ''), "la tarjeta de Retos de Andres muestra a Cami con su nivel")
    andres.abrir_juego()
    ok(andres.en_juego("HOST && HOST.usuario") == 'andres', "el juego en el telefono de Andres juega como Andres")
    texto = andres.en_juego("document.getElementById('vInicio').textContent.replace(/\\s+/g,' ')")
    ok('Cami' in (texto or ''), "el inicio del juego de Andres muestra a Cami")
    andres.foto("e2e-2-andres-ve-a-cami")
    andres.ganar_nivel(1)
    time.sleep(2.5)
    va = fila('andres')
    ok(bool(va) and va.get('nivel') == 2, "la nube tiene a Andres en el nivel 2")

    # 3) Cami vuelve a abrir el juego: el pull al abrir trae a Andres y repinta
    cami.js("document.querySelector('#botlayer') && document.querySelector('#botlayer iframe').contentWindow.eval(\"HOST.cerrar()\"); 1"); time.sleep(0.8)
    cami.abrir_juego(); time.sleep(2.5)
    texto = cami.en_juego("document.getElementById('vInicio').textContent.replace(/\\s+/g,' ')")
    ok('Andrés' in (texto or ''), "Cami ve a Andres en su inicio del juego")
    cami.foto("e2e-3-cami-ve-a-andres")

    # 4) telefono nuevo de Cami: sin nada local, el progreso vuelve desde la nube
    cami.js("document.querySelector('#botlayer') && document.querySelector('#botlayer iframe').contentWindow.eval(\"HOST.cerrar()\"); 1"); time.sleep(0.5)
    cami.preparar('cami', limpiar=True)
    cami.abrir_juego(); time.sleep(1.5)
    nivel = cami.en_juego("S.perfiles.cami.nivel")
    ok(nivel == 3, "un telefono nuevo de Cami recupera el nivel 3 desde la nube: %s" % nivel)
    cami.foto("e2e-4-cami-telefono-nuevo")
    ok(not cami.errores, "sin errores de JS en el telefono de Cami: %s" % cami.errores[:3])
    ok(not andres.errores, "sin errores de JS en el telefono de Andres: %s" % andres.errores[:3])
finally:
    cami.cerrar(); andres.cerrar()
print("---")
print("TODO BIEN" if not FALLOS else "FALLAS: %d" % len(FALLOS))
