"""Auditoria de accesibilidad medida (WCAG 2.1 AA) sobre la app en Chrome headless.
Requiere el servidor http y Chrome con CDP como en docs/PRUEBAS.md, y datos sembrados
(herramientas/sembrar-datos-prueba.js). Uso: CDP_TAB_FILE=<archivo con el ws de la pestana> SALIDA=<carpeta> python3 herramientas/a11y_run.py
Mide toque, contraste de texto y de controles, teclado, arbol de accesibilidad, la ventana del peso y el zoom. Usado el 14/10/2026."""
import json, time
from cdp_pruebas import *

SALIDA = os.environ.get('SALIDA', '/tmp')  # donde quedan el JSON y las capturas de zoom
c = CDP()
MED = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'a11y_medir.js')).read()
OUT = {}

def pantalla(js, extra=None):
    c.metrics(390, 844)
    c.ev(js + ";render();window.scrollTo(0,0);1"); time.sleep(1.2); c.frames(5)
    if extra: c.ev(extra); time.sleep(1); c.frames(5)
    h = int(c.ev("document.documentElement.scrollHeight") or 844)
    c.metrics(390, min(h, 9000)); time.sleep(1); c.frames(6)

def medir(nombre, js, extra=None, tema='oscuro'):
    c.ev(f"S.cfg.tema='{tema}';1")
    pantalla(js, extra)
    r = c.ev(MED)
    OUT[nombre + ('' if tema == 'oscuro' else '@claro')] = json.loads(r) if isinstance(r, str) else r

c.ev("ACTIONS._doSwitch('andres')"); time.sleep(1.5)
c.ev("window.confirm=()=>true; S.draft=null; save('draft'); UI.session=null; S.cfg.tour=1; save('cfg'); 1")
PANT = [
    ('inicio', "UI.tab='inicio';UI.nlogSlot=null", None),
    ('inicio-registro', "UI.tab='inicio';UI.nlogSlot=null", "ACTIONS.nlogOpen({s:'t'})"),
    ('sesion', "UI.tab='entrenar';UI.session='legsA'", "document.querySelector('[data-a=\"exToggle\"][data-ex=\"hack\"]').click()"),
    ('comida-recetas', "UI.session=null;S.draft=null;UI.tab='comida';UI.sub.food='recetas'", None),
    ('comida-mercado', "UI.tab='comida';UI.sub.food='lista'", None),
    ('progreso', "UI.tab='progreso';UI.sub.prog='general';UI.progAct='general'", None),
    ('medidas-cuerpo', "UI.tab='medidas';UI.medSec='cuerpo'", None),
    ('checkin', "UI.tab='checkin'", None),
    ('mas', "UI.tab='mas'", None),
]
for n, js, ex in PANT:
    medir(n, js, ex)
    if n == 'sesion': c.ev("S.draft=null;save('draft');UI.session=null;1")
for n, js, ex in PANT[:1] + PANT[3:4] + PANT[5:6]:
    medir(n, js, ex, tema='claro')
c.ev("S.cfg.tema='oscuro';render();1")

# ---- lo que anuncia el lector de pantalla (arbol de accesibilidad) en la barra y el Inicio ----
pantalla("UI.tab='inicio';UI.nlogSlot=null")
c.send('Accessibility.enable')
ax = c.send('Accessibility.getFullAXTree')['result']['nodes']
anuncios = []
for nd in ax:
    role = (nd.get('role') or {}).get('value'); name = (nd.get('name') or {}).get('value', '')
    if role in ('button', 'link', 'checkbox', 'tab', 'switch', 'slider', 'textbox', 'spinbutton', 'img', 'heading', 'navigation', 'main', 'banner', 'dialog') and not nd.get('ignored'):
        anuncios.append((role, str(name)[:60]))
OUT['ax_inicio'] = {'total': len(anuncios), 'por_rol': {}, 'muestra': anuncios[:60]}
for r, _ in anuncios: OUT['ax_inicio']['por_rol'][r] = OUT['ax_inicio']['por_rol'].get(r, 0) + 1

# ---- teclado: 30 tabulaciones desde el principio del Inicio ----
c.metrics(390, 844); c.ev("window.scrollTo(0,0); document.activeElement && document.activeElement.blur(); 1")
orden = []
for i in range(30):
    c.send('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
    c.send('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Tab', 'code': 'Tab', 'windowsVirtualKeyCode': 9})
    time.sleep(0.08)
    d = c.ev("""(()=>{const e=document.activeElement; if(!e||e===document.body) return null; const cs=getComputedStyle(e); const r=e.getBoundingClientRect();
      const foco=(cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0)||(cs.boxShadow&&cs.boxShadow!=='none');
      return (e.getAttribute('aria-label')||e.textContent||'').replace(/\\s+/g,' ').trim().slice(0,32)+' | '+e.tagName+' | foco visible: '+(foco?'si':'no')+' | y='+Math.round(r.top)})()""")
    orden.append(d)
OUT['tab_inicio'] = orden

# ---- ventana del peso: rol, foco, Escape y fondo tabulable ----
pantalla("UI.tab='inicio'")
c.metrics(390, 844)
c.ev("document.querySelector('[data-a=\"pesoModal\"]').click();1"); time.sleep(1); c.frames(4)
modal = c.ev("""(()=>{const b=document.querySelector('.fbox'); if(!b) return {abierta:false};
  const dentro=b.contains(document.activeElement);
  return {abierta:true, role:b.getAttribute('role'), ariaModal:b.getAttribute('aria-modal'), focoDentro:dentro, activo:(document.activeElement||{}).tagName, wrapInert: !!document.querySelector('#wrap[inert], #view[inert]')}})()""")
c.send('Input.dispatchKeyEvent', {'type': 'keyDown', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27})
c.send('Input.dispatchKeyEvent', {'type': 'keyUp', 'key': 'Escape', 'code': 'Escape', 'windowsVirtualKeyCode': 27})
time.sleep(.6); c.frames(3)
modal['sigueAbiertaTrasEscape'] = c.ev("!!document.querySelector('.fbox')")
c.ev("document.querySelectorAll('.fbox').forEach(e=>e.remove());1")
OUT['modal_peso'] = modal

# ---- zoom al 200 % (equivale a 195 px de ancho) y a 320 px ----
for ancho in (320, 195):
    c.metrics(ancho, 844); c.ev("UI.tab='inicio';render();window.scrollTo(0,0);1"); time.sleep(1.2); c.frames(6)
    OUT[f'reflow_{ancho}'] = c.ev("""(()=>{const W=document.documentElement.clientWidth; const sw=document.documentElement.scrollWidth;
      const fuera=[...document.querySelectorAll('#view *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width>0 && r.right>W+2}).slice(0,8).map(e=>(e.className&&typeof e.className==='string'?e.className.split(' ')[0]:e.tagName)+' '+Math.round(e.getBoundingClientRect().right));
      return {ancho:W, scrollWidth:sw, desbordaHorizontal: sw>W+1, elementosFuera: fuera}})()""")
    c.shot(os.path.join(SALIDA, f'zoom-{ancho}.png'))
c.metrics()
OUT['errores_consola'] = c.errors
json.dump(OUT, open(os.path.join(SALIDA, 'a11y_resultados.json'), 'w'), ensure_ascii=False, indent=1)
print('listo')
