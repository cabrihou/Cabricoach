"""Suite de regresion por navegador (CDP) del lote REV 223: isla, checkpoint, tarjetas del Inicio,
gesto de volver, sustituto, Deshacer, hojas de confirmacion, importar respaldo, la nube que no
pisa lo pendiente (con herramientas/nube_falsa.py en el puerto 9150), las 13 vistas con los dos
usuarios, 320 px y cero errores de consola. Requiere datos sembrados (sembrar-datos-prueba.js),
el servidor http en 9140 y Chrome con CDP (docs/PRUEBAS.md). Uso:
  python3 herramientas/nube_falsa.py 9150 &
  CDP_TAB_FILE=<archivo con el ws de la pestana> SALIDA=<carpeta> python3 herramientas/pruebas_rev223.py
Ojo: modifica los datos del perfil de Chrome de prueba (nunca usarlo con datos reales)."""
import json, time, urllib.request
from cdp_pruebas import *

c = CDP()
R = []  # (prueba, ok, detalle)
SALIDA = os.environ.get('SALIDA', '/tmp/cabricoach-pruebas')  # capturas y resultado
D = SALIDA + '/'; os.makedirs(D, exist_ok=True)

def ok(nombre, cond, det=''):
    R.append((nombre, bool(cond), det)); print(('PASA ' if cond else 'FALLA'), nombre, det)

def go(js, wait=1.0):
    r = c.ev(js); time.sleep(wait); c.frames(6); time.sleep(.3); return r

def nube(path, body=None):
    req = urllib.request.Request('http://127.0.0.1:9150' + path, data=(json.dumps(body).encode() if body is not None else None), method='POST' if body is not None else 'GET', headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req).read() or b'null')

c.nav(wait=8)
ok('carga sin errores y REV 223', c.ev("APPREV")=='REV 223' and not c.errors, c.ev("APPREV"))
go("ACTIONS._doSwitch('andres')", 1.5)
go("window.confirm=()=>true; S.draft=null; save('draft'); UI.session=null; S.cfg.tour=1; save('cfg'); UI.tab='inicio'; render(); 1")

# ---- isla ----
go("ACTIONS.goSession({rid:'legsA'})")
go("ACTIONS.tab({t:'inicio'})")
ok('isla: mirar una rutina no deja borrador ni isla', c.ev("S.draft===null && !document.querySelector('#island.on') && !document.body.classList.contains('conisla')"))
go("ACTIONS.goSession({rid:'legsA'})")
go("document.querySelector('[data-a=\"mark\"][data-ex=\"hack\"][data-i=\"0\"]').click()", 1.2)
go("ACTIONS.tab({t:'inicio'})")
ok('isla: con una serie marcada sí aparece y reserva espacio', c.ev("!!document.querySelector('#island.on') && document.body.classList.contains('conisla') && getComputedStyle(document.querySelector('#view')).paddingBottom==='170px'"),
   c.ev("getComputedStyle(document.querySelector('#view')).paddingBottom"))
go("UI.tab='entrenar'; UI.session='legsA'; ACTIONS.discard()")

# ---- checkpoint y tarjetas ----
go("UI.tab='inicio'; render(); window.scrollTo(0,0)", 1.2)
ck = c.ev("""(()=>{const ns=[...document.querySelectorAll('.cknode')];
  const lb=ns.map(n=>n.querySelector('.cklbl')); const rs=lb.map(l=>l.getBoundingClientRect());
  let choca=false; for(let i=1;i<rs.length;i++) if(rs[i].left < rs[i-1].right-1) choca=true;
  return {botones:ns.filter(n=>n.tagName==='BUTTON').map(n=>n.querySelector('.cklbl').textContent), textos:lb.map(l=>l.textContent),
    elipsis:lb.map(l=>getComputedStyle(l).textOverflow), choca}})()""")
ok('checkpoint: los 4 nodos se tocan (incluido COMIDAS)', len(ck['botones'])==4 and 'COMIDAS' in ck['botones'], str(ck['botones']))
ok('checkpoint: rótulos completos y sin chocar', all(e!='ellipsis' for e in ck['elipsis']) and not ck['choca'], str(ck))
tj = c.ev("""(()=>{const tiles=[...document.querySelectorAll('.ckgrid .cktile')];
  const agua=tiles.find(t=>t.querySelector('.wml')); const w=agua&&agua.querySelector('.wml'); const b=agua&&agua.querySelector('.wbtn2.plus');
  const ent=tiles[0]; const chip=ent&&ent.querySelector('.chip');
  const med=document.querySelector('.cktile[data-a="medGo"]');
  return {aguaCabe: w? w.getBoundingClientRect().right <= agua.getBoundingClientRect().right-4 : null,
    botonAlto: b? Math.round(b.getBoundingClientRect().height):null, botonTxt: b? b.textContent.trim():null,
    bonusCabe: chip? chip.getBoundingClientRect().right <= ent.getBoundingClientRect().right-4 : null,
    medAria: med? med.getAttribute('aria-label'):null, medSub: med&&med.querySelector('.cksub')? med.querySelector('.cksub').textContent:null}})()""")
ok('tarjetas: la cifra del agua cabe en su caja', tj['aguaCabe'], str(tj))
ok('tarjetas: el botón de agua en una línea', tj['botonAlto'] and tj['botonAlto'] <= 40, f"{tj['botonAlto']} px · {tj['botonTxt']}")
ok('tarjetas: la pastilla Bonus no se sale', tj['bonusCabe'])
ok('tarjetas: Medidas con rótulo y nombre claro', (tj['medAria'] or '').startswith('Medidas:') and tj['medSub'], f"{tj['medAria']} · {tj['medSub']}")
c.shot(D + 'inicio-arriba.png')
c.ev("window.scrollTo(0,520)"); time.sleep(.6); c.frames(4); c.shot(D + 'inicio-tarjetas.png')

# ---- volver con el gesto ----
go("UI.tab='fotos'; UI.backTo='perfil'; render(); goBack()")
ok('volver: desde Fotos abierta en Perfil vuelve a Perfil', c.ev("UI.tab")=='perfil', c.ev("UI.tab"))
go("UI.tab='medidas'; UI.medSec='cuerpo'; render(); goBack()")
ok('volver: dentro de Medidas vuelve a su portada', c.ev("UI.tab==='medidas' && !UI.medSec"))
go("UI.tab='hyrox'; UI.hxSub='nivel'; render(); goBack()")
ok('volver: dentro de Hyrox vuelve a su portada', c.ev("UI.tab==='hyrox' && !UI.hxSub"))
go("UI.tab='retos'; UI.backTo=null; render(); goBack()")
ok('volver: sin origen sigue yendo al Inicio', c.ev("UI.tab")=='inicio')

# ---- sustituto ----
go("S.draft=null; save('draft'); ACTIONS.goSession({rid:'legsA'})")
base = c.ev("JSON.stringify(S.draft.data.hack)")
go("S.logs.hack.push({d:addDays(TODAY(),-3), sets:[{w:60,r:10},{w:60,r:9},{w:60,r:8}], alt:'Sentadilla en Smith'}); save('logs'); ACTIONS.swapEx({ex:'hack', n:'Sentadilla en Smith'})")
sw = c.ev("JSON.stringify(S.draft.data.hack.map(s=>[s.w,s.r]))")
ok('sustituto: se recarga con los kg de su última vez', sw == json.dumps([[60, 10], [60, 9], [60, 8]]).replace(' ', ''), sw + ' · ' + c.ev("document.querySelector('#toast').textContent"))
go("S.draft.data.hack[2].w=''; S.draft.data.hack[2].r=''; save('draft'); render()")
go("document.querySelector('[data-a=\"mark\"][data-ex=\"hack\"][data-i=\"2\"]').click()", 1.2)
ok('sustituto: marcar una serie vacía usa su historial, no el del original', c.ev("S.draft.data.hack[2].w")==60, str(c.ev("S.draft.data.hack[2].w")))
go("ACTIONS.swapEx({ex:'hack', n:''})")
b0 = json.loads(base)[0]['w']
ok('sustituto: volver al original recupera sus kg', c.ev("S.draft.data.hack[0].w")==b0 and c.ev("S.draft.data.hack[2].done")==True, f"{c.ev('S.draft.data.hack[0].w')} vs {b0}")
go("S.logs.hack=S.logs.hack.filter(h=>!h.alt); save('logs')")

# ---- borrar serie con Deshacer ----
antes = c.ev("JSON.stringify(S.draft.data.hack[1])")
go("ACTIONS.delSet({ex:'hack', i:1})")
n1 = c.ev("S.draft.data.hack.length")
go("document.querySelector('#snack .snackb').click()")
ok('serie: borrar y deshacer la deja igual', n1==2 and c.ev("S.draft.data.hack.length")==3 and c.ev("JSON.stringify(S.draft.data.hack[1])")==antes)
go("ACTIONS.discard()")

# ---- hoja de confirmación: borrar un día ----
dia = c.ev("S.sessions[S.sessions.length-1].d")
n_antes = c.ev(f"Object.values(S.logs).flat().filter(h=>h.d==='{dia}').length")
go(f"ACTIONS.dayDelAll({{d:'{dia}'}})")
hoja = c.ev("(()=>{const b=document.querySelector('.fbox[role=dialog]'); return b?{si:b.querySelector('[data-r=si]').textContent, no:b.querySelector('[data-r=no]').textContent, foco:document.activeElement&&document.activeElement.dataset.r, titulo:b.querySelector('h2').textContent}:null})()")
ok('hoja: se abre con la acción en el botón y el foco en lo seguro', hoja and hoja['si']=='Borrar el día' and hoja['foco']=='no', str(hoja))
c.shot(D + 'hoja-borrar-dia.png')
c.send('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27}); time.sleep(.5); c.frames(3)
ok('hoja: Escape la cierra sin borrar', c.ev("!document.querySelector('.fbox[role=dialog]')") and c.ev(f"Object.values(S.logs).flat().filter(h=>h.d==='{dia}').length")==n_antes)
go(f"ACTIONS.dayDelAll({{d:'{dia}'}})"); go("document.querySelector('.fbox[role=dialog] [data-r=si]').click()")
borrado = c.ev(f"Object.values(S.logs).flat().filter(h=>h.d==='{dia}').length")
go("document.querySelector('#snack .snackb').click()")
ok('hoja: borrar el día y deshacer lo devuelve', borrado==0 and c.ev(f"Object.values(S.logs).flat().filter(h=>h.d==='{dia}').length")==n_antes, f"{n_antes} → {borrado} → deshacer")

# ---- borrar pesaje con Deshacer ----
nw = c.ev("S.weights.length")
go("ACTIONS.delWeight()")
ok('pesaje: se borra sin diálogo nativo', c.ev("S.weights.length")==nw-1 and c.ev("!document.querySelector('.fbox[role=dialog]')"))
go("document.querySelector('#snack .snackb').click()")
ok('pesaje: deshacer lo devuelve', c.ev("S.weights.length")==nw)

# ---- sesión a medias ----
go("ACTIONS.goSession({rid:'legsA'})"); go("document.querySelector('[data-a=\"mark\"][data-ex=\"hack\"][data-i=\"0\"]').click()", 1.2)
go("UI.calSel=addDays(TODAY(),-2); ACTIONS.pastSession({rid:'pullA'})")
go("document.querySelector('.fbox[role=dialog] [data-r=no]').click()")
ok('sesión a medias: la salida segura vuelve a la sesión', c.ev("UI.tab==='entrenar' && UI.session==='legsA' && S.draft.rid==='legsA'"))
go("UI.calSel=addDays(TODAY(),-2); ACTIONS.pastSession({rid:'pullA'})"); go("document.querySelector('.fbox[role=dialog] [data-r=si]').click()")
ok('sesión a medias: descartar abre la del día elegido', c.ev("S.draft.rid==='pullA' && S.draft.d===addDays(TODAY(),-2)"))
go("ACTIONS.discard()")

# ---- importar respaldo ----
def importar(js_obj):
    c.ev("""(()=>{const o=%s; const dt=new DataTransfer(); dt.items.add(new File([JSON.stringify(o)],'r.json',{type:'application/json'}));
      const i=document.querySelector('#importFile'); i.files=dt.files; i.dispatchEvent(new Event('change'));})()""" % js_obj)
    time.sleep(1.2); c.frames(5)
go("S.cfg.pin='1234'; save('cfg'); 1")
pesos = c.ev("JSON.stringify(S.weights)"); meal = c.ev("JSON.stringify(S.meal)")
importar("{v:3,user:'cami',exported:TODAY(),data:{weights:[{d:'2026-01-01',kg:55}]}}")
ok('importar: bloquea el respaldo de otro usuario', c.ev("JSON.stringify(S.weights)")==pesos and 'Cami' in (c.ev("document.querySelector('#toast').textContent") or ''), c.ev("document.querySelector('#toast').textContent"))
importar("{v:3,user:'andres',exported:'2026-10-10',data:{weights:[{d:'2026-01-01',kg:77.7}], cfg:Object.assign({},S.cfg,{pin:'9999',stepGoal:12345}), meal:{selected:{x:1}}}}")
txt = c.ev("(document.querySelector('.fbox[role=dialog]')||{}).textContent")
ok('importar: pide confirmación con resumen', bool(txt) and 'pesajes' in txt and 'Restaurar respaldo' in txt, (txt or '')[:140])
go("document.querySelector('.fbox[role=dialog] [data-r=si]').click()", 1.2)
ok('importar: restaura, conserva el PIN y no toca lo compartido', c.ev("S.weights.length===1 && S.weights[0].kg===77.7 && S.cfg.pin==='1234' && S.cfg.stepGoal===12345") and c.ev("JSON.stringify(S.meal)")==meal)
go("document.querySelector('#snack .snackb').click()", 1.2)
ok('importar: deshacer vuelve a los datos de antes', c.ev("JSON.stringify(S.weights)")==pesos)
go("delete S.cfg.pin; save('cfg'); 1")

# ---- nube: lo pendiente no se pisa ----
H = 'casa-prueba'
hoy = c.ev("TODAY()")
nube('/__set', [{'house': H, 'uid': 'andres', 'k': 'water', 'v': {hoy: 500}}, {'house': H, 'uid': 'andres', 'k': 'steps', 'v': {hoy: 1111}}])
c.ev("localStorage.setItem('afc2:sb', JSON.stringify({url:'http://127.0.0.1:9150', key:'sb_prueba', house:'%s'})); localStorage.removeItem('afc2:sbsucio'); 1" % H)
c.nav(wait=8)
go("ACTIONS._doSwitch('andres')", 2)
ag0=c.ev("S.water['%s']" % hoy); pa0=c.ev("S.steps['%s']" % hoy)
ok('nube: al abrir baja lo de la nube', ag0==500 and pa0==1111, 'agua %s pasos %s' % (ag0, pa0))
nube('/__off')
go("UI.tab='inicio'; render(); 1")
go("document.querySelector('[data-a=\"water\"][data-n=\"250\"]').click()", 2.5)
suc = c.ev("localStorage.getItem('afc2:sbsucio')")
ok('nube: sin señal el agua queda marcada como pendiente', 'andres|water' in (suc or '') and c.ev(f"S.water['{hoy}']")==750, suc)
nube('/__on'); nube('/__set', [{'house': H, 'uid': 'andres', 'k': 'steps', 'v': {hoy: 2222}}])
go("sbPull().then(had=>{ if(had){ S=loadState(); rutinasRefrescar(); render(); } }); 1", 3)
dump = nube('/__dump')
agua_nube = [f['v'] for f in dump['filas'] if f['uid'] == 'andres' and f['k'] == 'water'][0]
ok('nube: el agua pendiente no se pisa al volver la señal', c.ev(f"S.water['{hoy}']")==750, str(c.ev(f"S.water['{hoy}']")))
ok('nube: lo que no estaba pendiente sí se actualiza', c.ev(f"S.steps['{hoy}']")==2222)
marca=c.ev("localStorage.getItem('afc2:sbsucio')")
ok('nube: lo pendiente se sube solo y se limpia la marca', agua_nube.get(hoy)==750 and marca in ('{}', None), 'nube %s · marca %s' % (agua_nube.get(hoy), marca))
c.ev("localStorage.removeItem('afc2:sb'); localStorage.removeItem('afc2:sbsucio'); 1")

# ---- todas las vistas, dos usuarios, sin errores; 320 px ----
c.nav(wait=8)
VISTAS = ['inicio', 'entrenar', 'agenda', 'comida', 'progreso', 'fotos', 'checkin', 'retos', 'perfil', 'mas', 'medidas', 'hyrox', 'plan']
for u in ('andres', 'cami'):
    go(f"ACTIONS._doSwitch('{u}')", 1.5)
    vacias = []
    for v in VISTAS:
        go(f"UI.session=null; UI.tab='{v}'; render(); 1", .8)
        if not c.ev("document.querySelector('#view').textContent.trim().length>50"): vacias.append(v)
    ok(f'vistas de {u}: todas pintan', not vacias, str(vacias))
c.metrics(320, 800); go("ACTIONS._doSwitch('andres')", 1.5); go("UI.tab='inicio'; render(); 1", 1.2)
ok('320 px: el Inicio no se desborda', c.ev("document.documentElement.scrollWidth<=320"))
c.metrics()
ok('cero errores de consola en toda la prueba', not c.errors, str(c.errors[:3]))

# ---- capturas para revisar a ojo ----
go("ACTIONS._doSwitch('andres')", 1.5)
go("S.draft=null; save('draft'); ACTIONS.goSession({rid:'legsA'})")
go("document.querySelector('[data-a=\"exToggle\"][data-ex=\"hack\"]').click()")
c.ev("document.querySelector('[data-a=\"exToggle\"][data-ex=\"hack\"]').scrollIntoView({block:'start'})"); time.sleep(.5); c.frames(4)
c.shot(D + 'sesion-bordes-oscuro.png')
go("S.cfg.tema='claro'; render(); 1"); c.shot(D + 'sesion-bordes-claro.png')
go("S.cfg.tema='oscuro'; ACTIONS.discard(); UI.tab='inicio'; render(); 1")
json.dump(R, open(D + 'resultado.json', 'w'), ensure_ascii=False, indent=1)
print('\nRESUMEN', sum(1 for r in R if r[1]), 'de', len(R), 'pasan')
