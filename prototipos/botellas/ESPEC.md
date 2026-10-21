# Botellas · especificación del prototipo (v0)

Prototipo jugable, independiente de la app, para decidir si el juego entra a CabriCoach.
**No se toca `coach-afc-v2.html`.** Se publica como Artifact para que Cami lo pruebe en el
iPhone. Todo debe verse como CabriCoach (estándar en `../../docs/DESIGN-STANDARDS.md`).

## Archivos

```
prototipos/botellas/
  motor.js            motor puro, sin DOM: rng, parametros, generador, solver, reglas
  botellas.src.html   pagina con marcadores (ver abajo)
  build.py            arma botellas.html (Artifact) y botellas-local.html (prueba local)
  pruebas-motor.js    pruebas del motor con jsc
  recursos/           fuentes.css, *.b64 (data URIs ya listos), fragmentos-app.txt
```

Marcadores que reemplaza `build.py`:
- `/*@FUENTES@*/` dentro del `<style>` → contenido de `recursos/fuentes.css` (las 4 familias embebidas)
- `/*@MOTOR@*/` dentro de un `<script>` → contenido de `motor.js`
- `@IMG:celebC@`, `@IMG:celebA@`, `@IMG:faceC@`, `@IMG:faceA@`, `@IMG:rachaC@`, `@IMG:rachaA@` → el data URI de `recursos/<nombre>.b64`

`botellas.html` (Artifact): **sin** `<!doctype>`, `<html>`, `<head>` ni `<body>` (la
plataforma los pone). Empieza con:
```html
<title>Botellas de Cami</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>...</style>
```
`botellas-local.html`: lo mismo envuelto en `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=1,user-scalable=no">…</head><body>…</body></html>` para probar en Chrome.

Restricciones del Artifact: nada externo (todo inline), sin `alert/confirm/prompt` (la
confirmación de borrar progreso va dentro de la página), `localStorage` siempre dentro de
`try/catch` y la página debe funcionar sin él. Lado: gutter `padding-left: max(16px, env(safe-area-inset-left, 0px))` y su par derecho en el contenedor exterior. Nada de scroll horizontal. Arranque:
```js
const boot = (data) => start(data);
window.claude?.hot?.ready ? window.claude.hot.ready(boot) : boot(window.claude?.hot?.data ?? {});
window.claude?.hot?.snapshot?.(() => ({ /* estado persistible actual */ }));
```

## Identidad visual (CabriCoach "Night Gym", tema oscuro fijo)

Un solo tema, oscuro, a propósito: `:root{color-scheme:dark}` y `body{background:var(--paper)}`.
Copiar de la app (están en `recursos/fragmentos-app.txt`) los tokens y clases: `--paper #0B0D0F`,
`--paper2`, `--card #15181C`, `--card2 #1B1F23`, `--cardbg`, `--tile`, `--ink #F2F5F4`, `--ink2 #AEB6B3`,
`--smoke #828C89`, `--line`, `--line2`, `--line-ctl`, `--red`, `--shadow`, `--r-lg 26px`,
`--r-md 16px`, `--r-sm 13px`, y las fuentes `--ui` Instrument Sans, `--display` League Spartan,
`--ttl` Outfit, `--num` Archivo. Clases `.t-h1 .t-h2 .t-metric .t-metric-md .t-unit .t-body
.t-body-sm .t-label .t-btn`, `.mod`, `.glowtop`, `.bignum`, `.statrow`, `.btn`, `.btn.primary`,
`.chip`, `#toast`, `.flick`, `.shake`, `@keyframes badgepop` y `confettiBurst()`.

Acento por jugador con `data-user` en `<html>`:
- `cami` (por defecto): `--mint:#FFC94D; --mint2:#E89B2E; --onmint:#2A1B04; --grad:linear-gradient(135deg,#FFE08A 0%,#F2A93B 100%); --acc-rgb:255,201,77; --acc2-rgb:242,169,59; --accHi-rgb:255,222,128; --bn1:#FFF3D6; --bn2:#FFC94D; --glow:0 6px 22px rgba(242,169,59,.32)` y el resplandor ambiental del `body::before` dorado.
- `andres`: `--mint:#5C8DFF; --mint2:#3D63F2; --onmint:#081128; --grad:linear-gradient(135deg,#8FB5FF 0%,#3D63F2 100%); --acc-rgb:92,141,255; --acc2-rgb:61,99,242; --accHi-rgb:101,150,255; --bn1:#D6E4FF; --bn2:#5C8DFF; --glow:0 6px 22px rgba(92,141,255,.32)`.
El `.glowtop` de la app trae `border-color:rgba(140,175,255,.22)` horneado en azul: usar
`rgba(var(--accHi-rgb),.22)` para que siga al jugador.

Reglas duras del estándar:
- Toda cifra en `var(--num)` con `font-variant-numeric:tabular-nums`.
- Mayúsculas sostenidas solo en labels cortos (`.t-label`). Botones en caja de oración, 15 px mínimo.
- Un solo H1 por vista. Cuerpo 16 px (secundario 14-15).
- Radios: tarjetas 26, tiles 16, botones píldora. Cero esquinas rectas.
- Chrome (barra superior y barra de controles) en vidrio: `background:rgba(11,13,15,.8); backdrop-filter:blur(18px)`.
- Iconos SVG de trazo (viewBox 24, stroke-width 2, caps y joins redondos, `stroke:currentColor`, `fill:none`) y **cada icono lleva un punto relleno del acento** (`<circle class="acc" r="1.6" fill="var(--mint)">`): es la firma de la marca. Botón solo-icono = `aria-label`.
- Texto sobre relleno de acento: `var(--onmint)`, nunca blanco.
- Sin emojis. Sin rayas largas (—) en texto visible. Español de Colombia, cercano, sin regaños.
- Animaciones con la curva de la app `cubic-bezier(.32,.72,0,1)`; rebotes con `cubic-bezier(.34,1.36,.64,1)`. Todo se apaga con `prefers-reduced-motion`.

### Colores de líquido (contenido del juego, no acento de interfaz)

Doce tokens `--c1`..`--c12`, saturados y separables sobre negro:
1 rojo coral `#FF5A6E` · 2 naranja `#FF9F43` · 3 amarillo `#FFD93D` · 4 lima `#8BE04E` ·
5 esmeralda `#1FBF8F` · 6 cian `#3DD6F5` · 7 azul `#4C7DFF` · 8 violeta `#9B6BFF` ·
9 rosa `#FF6FCF` · 10 café `#A86B3C` · 11 perla `#D5DCE0` · 12 vino `#A3284F`.
Nombres para `aria-label`: rojo, naranja, amarillo, lima, esmeralda, cian, azul, violeta, rosa, café, perla, vino.

Modo símbolos (daltonismo, apagado por defecto): cada capa muestra un glifo SVG de 12-14 px
centrado, blanco al 85 % con contorno oscuro al 35 %: círculo, cuadrado, triángulo, rombo,
estrella, cruz, corazón, luna, gota, rayo, anillo, hexágono (en el mismo orden de colores).

## Motor (`motor.js`, sin DOM, debe correr en jsc y en un Worker)

Representación: botella = arreglo de enteros de abajo hacia arriba (1..12), estado = arreglo de botellas, `cap` capacidad.

- `rng(seedStr)`: hash de cadena (cyrb53 o FNV-1a) a semilla y `mulberry32`.
- `nivelParams(L)`:
  - colores por tramo: L≥1:3, ≥3:4, ≥6:5, ≥10:6, ≥15:7, ≥21:8, ≥29:9, ≥39:10, ≥51:11, ≥71:12.
  - `tipo`: si L≥8 y L%7===0 → `'dificil'` (+1 color, tope 12); si L≥9 y L%7===1 → `'respiro'` (-1 color, piso 3); si L≥30 y L%10===0 y no es difícil → `'largas'` (cap 6, colores = max(4, n-3)); si no, `'normal'`.
  - `misterio`: L≥25 y L%5===0 y tipo no es `'dificil'` ni `'largas'`.
  - `vacias: 2`, `cap: 4` (salvo largas).
- `diaParams(fechaISO)`: colores por día de la semana `[10,7,8,8,9,9,10]` (domingo a sábado, `getUTCDay` de la fecha), sábado con misterio, domingo con selección de difícil, cap 4, 2 vacías.
- `generar({n, vacias, cap, tipo, misterio}, seedStr)`: con el rng de la semilla, crea `n*cap` capas, baraja (Fisher-Yates), reparte en `n` botellas llenas + `vacias` vacías. Rechaza si alguna botella sale completa de un solo color. Resuelve con el solver; si no tiene solución, otro candidato. Candidatos válidos: normal 4, difícil 10, respiro 3, largas 3. Elige: difícil = el de meta más alta, respiro = el de meta más baja, normal y largas = la mediana. Devuelve `{botellas, cap, meta, tipo, misterio, ocultas}` donde `ocultas` (solo misterio) marca cada capa que no es la de arriba de su botella como oculta.
- Reglas: `puedeVerter(s,i,j,cap)` (i≠j, i no vacía, i no completa, j con espacio, j vacía o mismo color arriba; además prohibido verter una botella de un solo color (racha = todo su contenido) en una vacía, porque no cambia nada); `verter(s,i,j,cap)` → `{estado, cantidad, color}` con cantidad = min(racha de arriba de i, espacio en j); `completa(b,cap)`; `ganado(s,cap)` (cada botella vacía o completa).
- Solver `resolver(s, cap, {tope})`:
  - Clave canónica: botellas serializadas y ordenadas (el orden de las botellas no importa).
  - Heurística h = (total de rachas en todas las botellas) − (colores distintos). Es admisible: cada vertido baja esa cuenta en 1 como mucho.
  - A* (montículo binario, g = movimientos). Tope de expansiones 60.000. Si se pasa, A* ponderado (f = g + 3h) con tope 150.000. Si también, DFS con visitados y orden de jugadas (primero las que completan o juntan color) con tope 200.000. Si nada, `null`.
  - Devuelve `{movs:[[i,j],...], largo, optimo:bool, nodos}` con índices de la posición original (no de la ordenada).
- `pista(s, cap)`: primer movimiento de `resolver` desde el estado actual, o `{sinSalida:true}` si se demuestra sin solución, o `{desconocido:true}` si se pasó el tope.

`pruebas-motor.js` (se corre con `/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc motor.js pruebas-motor.js`; jsc tiene `print`, no `console.log`): genera los niveles 1 a 80 y 14 retos del día (desde 2026-10-21), comprueba que todos tienen solución, que la semilla es determinista (generar dos veces da lo mismo), que aplicar los movimientos de la solución gana, y muestra una tabla por nivel: colores, tipo, meta, óptimo, nodos, milisegundos. Debe terminar en menos de 60 s en total.

## Generación en la página

Generar un nivel puede tardar cientos de ms: se hace en un Web Worker creado desde un blob
con el código del motor; si el Worker falla, en el hilo principal con `setTimeout`. Mientras
tanto la vista de juego muestra el tablero en esqueleto (botellas vacías con shimmer suave) y
"Preparando el nivel". Al empezar un nivel se pre-genera el siguiente en segundo plano. Los
niveles generados se guardan en `localStorage` (`botellas:niveles:v1`, clave `camino:L` o
`dia:fecha`) para que abrir de nuevo sea instantáneo.

## Pantallas

### 1. Inicio (vista de entrada)

- Barra superior de vidrio, pegajosa (`top: env(safe-area-inset-top, 0px)`, más el `body::before` que pinta la franja del safe-area): a la izquierda el H1 "Botellas"; a la derecha la ficha del jugador: avatar redondo 34 px (`@IMG:faceC@` o `@IMG:faceA@`) + nombre ("Cami" / "Andrés"). Tocarla alterna jugador (cambia `data-user`, el acento y el progreso, cada uno tiene el suyo).
- Tarjeta héroe `.mod.glowtop`: `.t-label` "CAMINO", número héroe `.bignum` con "Nivel 14", una línea `.t-body-sm` con "8 colores · 10 botellas" (y "· Difícil", "· Misterio", "· Botellas largas" o "· Respiro" si aplica), **vista previa en miniatura del tablero real del nivel** (no interactiva, botellas a escala chica) y botón primario a lo ancho "Jugar el nivel 14". Es el único botón primario de la pantalla.
- Tarjeta "Reto del día": `.t-label` "RETO DEL DÍA · MAR 21 OCT" (fecha local), estado en una línea ("Todavía sin jugar" o "Resuelto en 24 movimientos · 3 estrellas"), la racha con la imagen `@IMG:rachaC@`/`@IMG:rachaA@` de 56 px y la cifra "3 días seguidos" (en `--num`), y botón secundario `.btn` "Jugar el reto" (o "Ver cómo quedó" si ya se resolvió, que abre el tablero resuelto).
- Tarjeta de estadísticas `.statrow`: "Niveles" (superados) | "Estrellas" (ganadas) | "Mejor racha".
- Caja plegable "Cómo se juega" (cabecera tocable entera con el dato clave, se despliega): filas de negrita inicial: **Toca una botella y luego otra.** El color de arriba cae en la segunda. / **Solo cae sobre el mismo color o en una vacía.** Y si cabe. / **Ganas cuando cada botella tiene un solo color.** / **Deshacer es gratis y sin límite.** Si te enredas, la app te dice si todavía hay salida.
- Caja plegable "Ajustes": interruptores redondeados (on = acento con tinta oscura) para Sonido, Vibración (aclara "en iPhone no aplica") y Símbolos por color; botón "Borrar mi progreso" (`.btn.red`) que abre una confirmación dentro de la página: "¿Borrar el progreso de Cami?" / "Vuelves al nivel 1 y se pierde la racha." / [Conservar] [Borrar progreso] con el foco en Conservar.
- Pie en gris: "Prototipo para CabriCoach. Los niveles se arman solos y todos tienen solución."

### 2. Juego (pantalla completa, sin scroll)

- `html, body` con `height:100%`; la vista de juego es una columna flex: barra superior, tablero que ocupa el resto, barra de controles abajo.
- Barra superior de vidrio: botón circular 44 px "volver" (chevron, `aria-label="Volver al inicio"`), al lado "Nivel 14" en `.t-h2` y debajo un `.chip` pequeño con el tipo si no es normal ("Difícil", "Misterio", "Botellas largas", "Respiro") o "Reto del día". A la derecha: movimientos en `.t-metric-md` con `.t-label` "MOVS" y debajo "Meta 22" en `.t-body-sm` `--smoke`. No hay reloj visible (el tiempo se mide en silencio para las estadísticas: el juego no presiona).
- Tablero: botellas en una fila si son ≤ 6, si no en dos filas (`ceil(total/2)` arriba). El tamaño se calcula con JS para caber a lo ancho y a lo alto (ancho entre 34 y 64 px, alto ≈ ancho × (0,85 × cap)… ajustar para que con cap 4 la proporción sea ~1:3,3 y con cap 6 ~1:4,6), recalculado en `resize`. Centrado vertical.
- Botella: vidrio oscuro `rgba(255,255,255,.035)`, borde 1,5 px `rgba(255,255,255,.26)`, radio arriba 8 px y abajo medio ancho (fondo de tubo de ensayo), boca con un labio un poco más ancho (pseudo-elemento), brillo vertical a la izquierda (franja blanca al 14 %, con degradado). Capas apiladas desde abajo, cada una `altura = 100%/cap` del interior, fondo con degradado horizontal (más oscuro en los bordes, más claro al 40 %) para dar volumen; la capa de arriba lleva un menisco (franja 3 px un poco más clara). Las capas de un mismo color contiguas se ven como un bloque (sin línea entre ellas).
- Capa oculta (misterio): vidrio ahumado `rgba(255,255,255,.06)` con un "?" en `--num` 700 `--smoke`. Cuando queda arriba se revela con un giro vertical (scaleY 0→1, 260 ms) y queda revelada para siempre.
- Tocar botella: si no hay seleccionada y se puede verter desde ella, se levanta (`translateY(-16px)`, 160 ms) con borde y resplandor del acento. Tocar otra: si el vertido es válido, se anima; si no, la de destino hace `.shake` y suena un golpe sordo; tocar la misma la baja. Tocar una completa o vacía sin selección: nada (o leve shake).
- **Vertido** (el momento clave, ~700 ms): la botella de origen se eleva por encima de las demás (z-index), viaja hasta quedar con su boca arriba y al lado de la boca de destino (WAAPI, 220 ms), se inclina hacia ella entre 55° y 75° según cuánto vierte; aparece un chorro (div de ancho ≈ 14 % de la botella, del color, con bordes redondeados) que nace en la boca de origen y baja hasta la superficie del líquido destino (scaleY 0→1 en 80 ms); durante 280 ms las capas de origen bajan y las de destino suben (animando altura); el chorro se retira; la botella vuelve a su lugar (200 ms). Durante el vertido no se aceptan toques. Al terminar se re-pinta el estado limpio. Con movimiento reducido: sin viaje ni giro, solo el cambio de capas con un fundido de 120 ms.
- **Botella completa**: cae una tapa (píldora del ancho de la boca, relleno `var(--grad)`, con el punto de acento oscuro `--onmint` al centro como firma) desde -28 px con la curva de rebote, un brillo corto alrededor de la boca, sonido de campanita y `vibrate(18)`. Las completas no se pueden tocar.
- **Ganar**: 350 ms después de la última tapa, `confettiBurst()` y una hoja inferior (anclada abajo, esquinas superiores 20 px, manija, entra con `translateY` 280 ms y velo oscuro): imagen `@IMG:celebC@` (o `celebA`) de 120 px, `.t-label` "NIVEL 14", `.t-h1` "Nivel superado" (en reto: "Reto del día resuelto"), tres estrellas SVG que aparecen una tras otra (120 ms de escalonado, badgepop; las no ganadas en contorno `--line-ctl`), `.statrow` con Movimientos | Meta | Tiempo (m:ss), y botones: primario "Siguiente nivel" (en reto: "Volver al inicio") y secundario "Repetir".
- Estrellas: movimientos ≤ meta → 3; ≤ `ceil(meta*1.25)` → 2; si no, 1. Se guarda la mejor de cada nivel. Usar pista o la botella extra no quita estrellas (la app acompaña, no castiga).
- Barra de controles abajo (vidrio, `padding-bottom: calc(10px + env(safe-area-inset-bottom, 0px))`, más el gutter lateral): cuatro botones iguales con icono 22 px y texto 13 px debajo: "Deshacer" (ilimitado; desactivado sin historial), "Reiniciar", "Pista", "Botella extra" (una por nivel, con insignia "1" que se apaga al usarla; agrega una botella vacía de la misma capacidad). Alto mínimo 52 px por botón. Estados desactivados al 40 %.
- **Pista**: corre `pista()` en el Worker. Si hay jugada: la botella de origen late con un anillo del acento y la de destino con un anillo punteado, 2,5 s. Si `sinSalida`: muestra la franja de "sin salida" (abajo). Si `desconocido`: toast "Esta está enredada: prueba deshacer un par de movimientos".
- **Sin salida**: después de cada vertido, si no queda ninguna jugada válida, o si el solver (en el Worker, tope 20.000) demuestra que no hay solución, aparece sobre la barra de controles una franja `.mod` compacta: "Por aquí ya no hay salida." + botón "Volver al último punto con salida" (deshace hasta el estado más reciente del historial que el solver sí resuelve; si ninguno, reinicia) y, si queda, "Usar la botella extra". Nunca en rojo: es información, no regaño.
- Tutorial en los niveles 1 y 2: una burbuja (tooltip píldora de alto contraste como el `#toast`) señala la botella de origen de la primera jugada de la solución con el texto "Toca esta botella" y luego la de destino con "Ahora esta". Desaparece al primer vertido válido.
- Accesibilidad: cada botella es `role="button"` con `tabindex="0"`, Enter/Espacio la tocan, `aria-label` tipo "Botella 3: rojo, rojo, azul. Le cabe 1 más" u "… 2 capas ocultas". Región `aria-live="polite"` que anuncia "Vertiste azul en la botella 5" y "Botella 5 completa".

## Sonido y vibración

Web Audio sintetizado, sin archivos; el `AudioContext` se crea y se despierta en el primer toque. Volumen bajo (ganancia máx 0,12):
- vertido: ruido filtrado pasa-banda (frecuencia de 900 a 500 Hz en 300 ms) + un "glu" senoidal corto de 420→260 Hz;
- tapa: dos notas senoidales 880 y 1320 Hz, 90 ms cada una;
- inválido: 140 Hz, 90 ms, triangular;
- ganar: arpegio 523, 659, 784, 1047 Hz, 110 ms cada una.
Vibración (`navigator.vibrate` si existe): vertido 8 ms, tapa 18 ms, ganar [30,40,60].

## Estado persistente (`localStorage`, clave `botellas:v1`, todo en try/catch)

```
{ jugador:'cami',
  perfiles:{ cami:{ nivel:1, estrellas:{'1':3,...}, dias:{'2026-10-21':{movs,estrellas,seg}},
                    racha:{actual:0, mejor:0, ultimo:null}, stats:{ganados:0, segundos:0} },
             andres:{ ...igual } },
  ajustes:{ sonido:true, vibra:true, simbolos:false },
  partida:{ jugador, modo:'camino'|'dia', clave, estado, ocultas, historial, movs, extraUsada, seg } }
```
- `partida` permite retomar el nivel a medias al volver a abrir.
- Racha: resolver el reto del día en días consecutivos (fecha local). Si se salta un día, `actual` vuelve a 1 al resolver el siguiente; la copia nunca regaña.
- "Niveles" = nivel − 1 superados; "Estrellas" = suma de las mejores.

## Lo que se entrega

1. `motor.js`, `pruebas-motor.js` con salida limpia de jsc (todo resoluble, determinista, tiempos).
2. `botellas.src.html`, `build.py` y los dos HTML construidos.
3. Comprobación de sintaxis del JS de la página con jsc (extraer el script y parsearlo) y una pasada en Chrome sin interfaz a 390×844 con capturas de: inicio, nivel 1 con tutorial, un vertido a mitad (captura durante la animación), nivel con misterio (25), nivel con botellas largas (30), hoja de ganar. Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --headless=new --screenshot=... --window-size=390,844 --virtual-time-budget=...` o CDP; servir con `python3 -m http.server` desde la carpeta (con file:// localStorage puede fallar). Para llegar a un nivel concreto en las capturas, aceptar `#nivel25` en la URL (solo un `#` y letras/dígitos: es lo único que el Artifact deja pasar) que abre directo ese nivel del camino.
