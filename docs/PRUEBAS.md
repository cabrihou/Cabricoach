# Cómo se prueba CabriCoach

> No hay suite de tests y nunca la hubo. La red de seguridad son tres capas:
> el verificador estático, el navegador real por CDP, y la comparación contra un
> snapshot. Este documento es la receta completa para correrlas en cualquier máquina.

## 1. Regla de oro: snapshot antes de tocar

```bash
cp coach-afc-v2.html /tmp/base.html        # ANTES del primer cambio
# ... trabajo ...
python3 herramientas/verificar.py coach-afc-v2.html --base=/tmp/base.html
```

Debe decir **"sin regresiones"**. La app arrastra avisos heredados (~22): lo que
importa no es el número absoluto sino NO INTRODUCIR hallazgos nuevos. El verificador
usa el parser JavaScriptCore de macOS (`jsc`), así que los errores de sintaxis son
reales; además cruza cada `data-a` con `ACTIONS`, revisa iconos, mayúsculas
sostenidas y nombres accesibles.

## 2. Navegador real (Chrome headless + CDP)

`file://` bloquea localStorage: **siempre por http**.

```bash
python3 -m http.server 9140 --directory /ruta/a/SandyApp &
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --remote-debugging-port=9744 \
  --remote-allow-origins='*' --window-size=390,900 \
  --user-data-dir=/tmp/cdp-cabricoach about:blank &
```

Guion python típico (websocket-client): conectar al target `page` de
`http://localhost:9744/json`, y SIEMPRE en este orden:

1. **Limpiar service workers y caches** antes de navegar, o verás una versión vieja:
   ```js
   const rs=await navigator.serviceWorker.getRegistrations();
   for(const r of rs) await r.unregister();
   for(const k of await caches.keys()) await caches.delete(k);
   ```
2. `Page.navigate` con un query único (`?t=123`) y esperar ~7-8 s (la app pesa).
3. `Emulation.setDeviceMetricsOverride` a 390x844 (móvil) para medir como el iPhone.
4. Habilitar `Runtime` y registrar `Runtime.exceptionThrown` durante TODA la sesión:
   una prueba sin contador de errores de consola no cuenta.

### Trampas de prueba que ya nos mordieron (leer antes de confiar en un resultado)

- **La página NO se recarga sola tras editar el archivo.** Si editas y vuelves a
  medir sin `Page.navigate`, estás probando el código viejo. Nos pasó dos veces:
  resultados idénticos tras "arreglos" eran la señal.
- **`innerText` miente con content-visibility**: las secciones no renderizadas
  devuelven texto vacío. Para saber si una vista tiene contenido usa `textContent`.
- **Cualquier medición de layout inmediatamente tras `render()` puede estar sobre
  los placeholders de 240px.** Espera frames o mide dos veces (ver ARQUITECTURA §3).
- Cambio de usuario en pruebas: `ACTIONS._doSwitch('cami')` (el `switchUser` normal
  pide PIN si existe). Espera ~1,5 s tras el switch.
- La tarjeta del rotador se fuerza a "próximo entreno" una vez al día: para verla en
  pruebas, `UI.rotIdx=null; _rotProxDay=null; render()`.
- `window.confirm` bloquea headless: si la acción confirma, sobreescribe
  `window.confirm=()=>true` antes del click.
- Los `sleep` del guion importan: renders + expansión de content-visibility toman
  0,5-1,5 s. Mediciones a destiempo dan falsos rojos.

### Cómo se mide un "salto"

```js
el.scrollIntoView({block:'center'});
const t0 = el.getBoundingClientRect().top;   // antes de la interacción
el.click();                                   // o dispatchEvent input/change
// esperar >= 1.2 s (el estabilizador re-aplica por frames)
const t1 = elEquivalente.getBoundingClientRect().top;
// |t1 - t0| <= 5 px es lo esperado; >10 px es un salto reportable
```

El elemento "equivalente" tras el render se busca por sus data-* y por ÍNDICE de
aparición (los 7 días de la semana repiten atributos idénticos).

### Gestos (deslizar para borrar)

Simular touchstart → varios touchmove (dx negativo creciente, |dx| > |dy|·1.5,
superando 18 px) → touchend con dx < -120. Un tap normal NO debe disparar el
gesto: verifica ambas cosas.

## 3. Qué probar por zona (lista mínima de regresión)

- **Inicio**: agua +/-, pasos (0 y 99999), peso, loggeo por franja con verificación
  ARITMÉTICA (la proteína del día debe cuadrar con lo agregado al gramo), buscador
  en vivo (foco retenido y <10 px de movimiento por tecla), rotador (varios taps),
  isla semanal (abrir desde la caja de entrenamiento, cambiar un día, verificar
  `S.week` y que calendario/Entrenar lo vean), ciclo de Cami (sembrar
  `S.cfg.cycStart`), avatar → perfil.
- **Entrenar**: abrir rutina, sesión, marcar series, editar peso/reps, deslizar para
  borrar serie y para quitar ejercicio, checkbox de ejercicio, colapsar caja,
  terminar sesión (XP contra las reglas), catálogo con filtros y buscador.
- **Comida**: mercado == consumo de la semana (reconstruir el consumo con
  `comidaArmada` 7 días x 2 personas y comparar con la lista: desfase esperado 0%),
  porciones gobiernan la rotación (subir una a 8 y verificar `vecesEnSemana`),
  escalado (aviso "Ajusté la receta" con números verdaderos, cero cantidades
  absurdas: nada de 8,5 huevos), cambios de ingrediente (conversión por carbos
  equivalentes; el otro usuario NO se afecta), % del día con pisos, aplicar día a
  toda la semana, vaciar mercado (confirm + deshacer), quitar ítem con X y con
  deslizar + restaurar, semana práctica, formulario ármame la semana.
- **Progreso**: cada modo x cada rango sin errores; eje con piso verosímil (la
  línea no toca el borde inferior ni se aplasta); proyección = duración del rango
  (mirar las fechas del eje); tríos contra aritmética propia con datos sembrados.
- **Agenda**: editar comida/pasos/agua/peso de un día pasado escribe en ESE día
  (verificar que hoy queda intacto), sesión retroactiva, actividades alternativas.
- **Ambos usuarios** en todo lo anterior; las 10 vistas de `VIEWS` deben pintar
  con `textContent` no vacío y 0 errores de consola.

## 4. Rendimiento y offline

- La app debe seguir bajo ~1,2 MB; si crece, sospecha de imágenes embebidas nuevas
  (van en `assets/cab/` y se agregan a `UI_IMGS` del sw.js para el precache).
- Prueba offline: cargar con red, matar el server, recargar: TODAS las pantallas
  deben verse con sus imágenes (el precache cubre las no visitadas).

## 5. Sembrar datos de prueba útiles

```js
// pesajes 60 días bajando (para gráficas/proyección)
S.weights=[]; for(let i=60;i>=0;i-=2) S.weights.push({d:addDays(TODAY(),-i), kg:94.4-(60-i)*0.04});
save('weights');
// historial de un ejercicio estancado y cerca del récord (para la cápsula)
S.logs[exId]=[{d:addDays(TODAY(),-19),sets:[{w:62.5,r:8}]},{d:addDays(TODAY(),-12),sets:[{w:62.5,r:8}]},{d:addDays(TODAY(),-5),sets:[{w:62.5,r:8}]}]; save('logs');
// ciclo de Cami en fase folicular
S.cfg.cycStart=addDays(TODAY(),-9); S.cfg.cycEnd=addDays(TODAY(),-5); S.cfg.cycLen=28; save('cfg');
```

Las pruebas corren sobre el localStorage del perfil de Chrome de prueba
(`--user-data-dir` propio): no tocan los datos reales del teléfono de nadie.

## Auditoría automática de UI (REV 190)

`scratchpad/audit.py` recorre las 22 vistas y sub-vistas con los dos perfiles y mide tres
cosas en cada una: desborde horizontal, objetivos táctiles por debajo de 32 px y texto por
debajo de 9 px. También cronometra el render.

Lo que encontró y se corrigió:

- **Objetivos táctiles a la mitad de lo que pide cualquier guía.** Los chips medían 22 px de
  alto, los selectores de rango 21, el interruptor 27. Ahora el alto real es 32-38 y encima
  llevan un área de toque invisible (`::after` de −4 a −7 px) que llega a 42-44 sin engordar
  el dibujo. El margen no pasa de la mitad del hueco entre filas, así que nunca roba el toque
  del control de al lado.
- **La fila de checkpoint no cabía**: seis nodos fijos de 62 px son 372 px más huecos, contra
  362 de ancho de pantalla. Pasó a `flex:1 1 0` con `max-width:72px` y la etiqueta con elipsis.
- **Texto de 8,5 px** en la cadencia de medidas, subido a 10.

Render: todas las vistas por debajo de 16 ms. La más lenta es Retos.

Lo que queda y es a propósito: las zonas del SVG del mapa miden 17×30 px en pantalla. Son las
formas del dibujo, agrandar el área de toque implicaría rectángulos invisibles encima que
taparían zonas vecinas. Las cotas de al lado (100-200 px de ancho) hacen de alternativa.
