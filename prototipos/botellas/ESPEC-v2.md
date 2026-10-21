# Botellas v2 · llaves, candados, 4 rutas y 200 niveles

Pedido de Andy (2026-10-21), sobre el prototipo v0 (`ESPEC.md` sigue valiendo en todo lo que
este archivo no cambia):

1. **Llaves escondidas en una franja de color** que abren un **compartimiento (caja)** con
   otras botellas adentro.
2. **Candado de color**: una botella que se abre cuando completas un color.
3. **Todos los niveles con solución**, y que nunca te quedes encerrada "haciéndolo bien".
4. **Cuatro dificultades**: Fácil, Normal, Difícil y Muy difícil, con los flujos que ya hay
   (reto del día, misterio, botellas largas, ayudas).
5. **Al menos 200 niveles.**

Respaldo de la v0 en `respaldo-v1/`. `coach-afc-v2.html` no se toca.

## 1. Reglas nuevas (ya están en el núcleo de `motor.js`, no cambiarlas)

- **Llave**: vive en la capa `k` (contada desde abajo, 0 = fondo) de la botella `b`. Sale
  cuando esa capa queda arriba, es decir cuando la botella baja a `k+1` capas o menos (si la
  franja de la llave se va entera con el chorro, también sale). Al salir abre su caja. Sale
  una sola vez y para siempre. Siempre se ve: también sobre una capa oculta de misterio.
- **Caja**: grupo de 1 o 2 botellas que no se pueden tocar (ni verter desde ni hacia ellas)
  hasta que salga su llave. Sus botellas se ven a través del vidrio de la caja, así se puede
  planear. Puede tener líquido o una botella vacía (premio de espacio).
- **Candado de color**: la botella `b` no se puede tocar hasta que se complete una botella del
  color `color`. Puede estar vacía (premio) o con líquido (que no tenga ese color, si no el
  nivel no tendría salida).
- Excepción nueva a la regla vieja: se puede verter una botella de un solo color a una vacía
  si tiene una llave adentro (sacar el líquido libera la llave).
- Se gana cuando cada botella está vacía o completa, las cerradas incluidas.

### Formato

```
C (fijo por nivel) = { cap, llaves:[{b,k,caja}], cajas:[{bots:[i,...]}], candados:[{b,color}] }
E (cambia)        = { b:[[...],...], ab }   // ab: bit c = caja c abierta (c<4), bit 4+d = candado d abierto
```
El objeto de nivel completo sirve tal cual como `C`. Atajos que el motor acepta: `C` número
(solo cap) y `E` arreglo (nada abierto).

API del núcleo (estable, la interfaz cuenta con ella):
`puedeVerter(E,i,j,C)`, `verter(E,i,j,C)` → `{estado:{b,ab}, cantidad, color, abre:[...]}` donde
cada elemento de `abre` es `{tipo:'caja', caja, llave, b, k}` o `{tipo:'candado', candado, b, color}`,
`ganado(E,C)`, `cerrada(E,i,C)`, `hayJugadas(E,C)`, `resolver(E,C,opts)` (opts: `tope`, `topes:[a*,ponderado,dfs]`,
`rapido`), `pista(E,C,opts)`, `clave(E,C)`, `jugadas(E,C)`, `heuristica(E)`, `completa(b,cap)`,
`estrellasDe(movs,meta)`, `rng`, `hashCadena`. Pruebas del núcleo: `pruebas-nucleo.js`.

## 2. Objeto de nivel v2

```
{ id:'normal-12', ruta:'normal', L:12,          // el reto del dia: id 'dia-2026-10-21', ruta:'dia'
  cap:4, botellas:[[...],...],
  llaves:[{b,k,caja}], cajas:[{bots:[...]}], candados:[{b,color}],
  ocultas:null | [[true/false,...],...],         // misterio: true = capa oculta
  meta, movs:[[i,j],...], optimo:true|false,     // movs = la solucion que da la meta (se juega con verter)
  rasgos:['llave','candado','misterio','largas'],// los que tenga, en ese orden
  dif:'facil'|'normal'|'dificil'|'muy',          // dificultad (en las rutas = la ruta)
  bot, atasco }                                  // metricas (ver 3.3), solo en el catalogo
```
Orden de las botellas: primero las sueltas (con líquido, vacías y las de candado, mezcladas),
**al final las de cada caja, contiguas** (caja 0, luego caja 1). La botella extra del jugador
se agrega después de todo.

Topes de tamaño: total de botellas ≤ 15 (con la extra, 16). Colores ≤ 12.

## 3. Motor: generador, rutas y catálogo (frente A)

### 3.1 Rutas: 4 × 50 niveles = 200, comprobados y embebidos

`rutaParams(ruta, L)` devuelve `{n, vacias, cap, misterio:0|1|2, cajas:[{bots, vacia}], candados:[{vacia}], cadena, seleccion, cuantos, dif}`:
- `misterio`: 0 nada, 1 leve (ocultas todas menos las 2 de arriba), 2 total (todas menos la de arriba).
- `cajas`: cuántas y cómo: `bots` 1 o 2 botellas adentro; `vacia:true` = una de ellas es una
  botella vacía extra (premio de espacio), si no son botellas con líquido del reparto.
- `candados`: cuántos; `vacia:true` = el candado va en una botella vacía extra, si no en una con líquido.
- `cadena`: la llave de la caja 1 va adentro de la caja 0 (solo Muy difícil).
- `seleccion` y `cuantos`: cómo se elige entre candidatos (3.3).

Curva propuesta (punto de partida: ajustarla con el informe para que las cuatro rutas queden
claramente separadas y cada una suba de a poco):

| Ruta | Colores | Vacías | Mecánicas | Elección |
|---|---|---|---|---|
| **Fácil** "Para relajarse" | L1-2: 3, L3-5: 4, L6-12: 5, L13-22: 6, L23-50: 6 y 7 | 2 | Una por nivel como mucho. L4 primer candado (en botella vacía), L7 primera llave (caja con una vacía), después rotan candado / llave / nada; misterio leve desde L15 cada 5; largas en L20, 30, 40, 50 con 4 colores | la más fácil: mayor `bot`, empate menor meta (6 candidatos) |
| **Normal** "El de siempre" | L1-4: 5, L5-12: 6, L13-24: 7, L25-38: 8, L39-50: 9 | 2 | Desde L2. Rotan candado con líquido, llave con caja de líquido, misterio (leve hasta L15, luego total), nada; dos mecánicas desde L25; largas en L%10==0 | mediana de meta (6) |
| **Difícil** "Para pensar" | L1-10: 8, L11-25: 9, L26-40: 10, L41-50: 11 | 2, y 1 + una vacía con candado o en caja cada 5 | Al menos una en todos; dos desde L15; cajas de 2 botellas; misterio total | mayor meta, empate menor `bot` (8) |
| **Muy difícil** "Reto mayor" | L1-15: 10, L16-35: 11, L36-50: 12 | 2, o 1 + vacía cerrada cada 3 | Dos o tres; dos cajas (con cadena desde L20); misterio total cada 4 | mayor `meta + 15·(1−bot)` (10) |

Ningún nivel es "imposible sin pagar": no hay vidas, ni límite de movimientos, ni reloj.

**Niveles 51 en adelante** (cuando alguien termina una ruta): se generan en el teléfono con la
misma semilla `ruta:L` y `rutaParams(ruta, L)` repitiendo el patrón de mecánicas de L41-50
con los colores de L50, en modo rápido (3.3). Deben generarse en ≤ 2 s en este Mac (jsc).

### 3.2 Reto del día con mecánicas

`diaParams(fechaISO)` por día de la semana (domingo a sábado), siempre en modo rápido y ≤ 2 s:
dom: 10 colores + llave + candado (dif 'muy'), lun: 6 + candado vacío ('facil'), mar: 7 + llave
('normal'), mié: 8 + misterio total ('normal'), jue: 9 + candado con líquido ('dificil'),
vie: 8 + llave + candado ('normal'), sáb: 9 + misterio total + llave ('dificil').

### 3.3 Generador y métricas

`generar(p, seedStr, opts)` con `opts.modo = 'catalogo' | 'rapido'` (por defecto `'rapido'`),
determinista por semilla y modo:
1. Reparto como en la v0 (rechaza botellas ya completas).
2. Mecánicas, siempre buscando que importen y que el nivel tenga salida:
   - caja de líquido: elige `bots` botellas llenas; caja vacía: agrega una botella vacía (y la otra, si `bots` es 2, llena).
   - llave: en una botella suelta con líquido (o, con `cadena`, dentro de la caja 0 para la caja 1), en `k` entre 0 y `len-2` (enterrada bajo al menos una capa; más hondo en las rutas difíciles). Nunca dos llaves en la misma botella.
   - candado: color `color` sin unidades dentro de la botella cerrada; si va en una con líquido, que no esté en una caja.
   - sin ciclos (la llave de una caja no puede estar en esa misma caja; con cadena, la de la caja 0 está afuera).
3. `resolver` con topes de catálogo (por ejemplo `[400000, 400000, 400000]`) o rápidos (los de siempre); descarta los sin solución o desconocidos.
4. Métricas por candidato (solo en modo catálogo):
   - `bot`: fracción de 40 partidas (semilla `'bot:'+seedStr+':'+candidato`) que gana un jugador
     medio-aleatorio: jugadas válidas sin repetidas, sin deshacer la jugada anterior, con pesos
     completa una botella 8, abre caja o candado 6, cae sobre su mismo color 3, a una vacía 1;
     hasta `3·meta + 20` jugadas.
   - `atasco`: fracción de esas partidas que terminó sin ninguna jugada posible.
5. Elección según `p.seleccion` (tabla de 3.1). En modo rápido sin métricas: fácil = menor meta,
   normal = mediana, difícil y muy = mayor meta, con 3 candidatos.
6. Devuelve el objeto de nivel v2 (sección 2). `misterio` arma `ocultas`.

### 3.4 Catálogo

- `generar-catalogo.js` (jsc): genera un rango de niveles de una ruta y los imprime, uno por
  línea en JSON (`jsc motor.js generar-catalogo.js -- normal 1 10`).
- `catalogo.py`: reparte los 200 niveles en procesos jsc en paralelo (el Mac tiene 12 núcleos,
  usar hasta 10), arma `niveles.json` (`{version, generado, rutas:{facil:[50], normal:[50], dificil:[50], muy:[50]}}`)
  e `INFORME-NIVELES.md` (tabla por nivel: ruta, L, colores, botellas, rasgos, meta, óptimo, bot,
  atasco, segundos; y promedios por ruta). Se puede correr de nuevo y da lo mismo.
- `niveles.json` compacto (sin espacios). Presupuesto ~150 KB.

### 3.5 Pruebas (`pruebas-motor.js`, más `pruebas-nucleo.js`)

Sobre `niveles.json` (los 200): jugar `movs` con `verter` gana; `meta === movs.length`; cada color
con `cap` capas; ninguna botella completa de entrada; cada llave enterrada (`len > k+1`) y no en una
botella cerrada salvo la cadena; candado sin su color adentro; cajas contiguas al final; total ≤ 15;
rasgos que coinciden con lo que hay; ids y L correlativos. Separación de dificultad: promedio de `bot`
estrictamente decreciente y promedio de meta creciente de Fácil a Muy difícil.
En vivo: niveles 51-55 de cada ruta y 14 retos del día desde 2026-10-21: con solución,
deterministas (dos veces igual) y ≤ 2 s cada uno. Todo junto en menos de 3 minutos.

## 4. Interfaz (frente B)

Todo lo visual sigue `ESPEC.md` (Night Gym, acento por jugador, iconos de trazo con punto de
acento, cifras en `--num`, sin emojis, sin rayas largas, movimiento reducido).

### 4.1 Inicio
- Héroe: `.t-label` "RUTA NORMAL", `.bignum` "Nivel 12", línea "8 colores · 10 botellas · Llave",
  vista previa, botón primario "Jugar el nivel 12" (o "Seguir el nivel 12"), y debajo un botón
  de texto "Ver los 50 niveles" que abre el mapa.
- **Elige la dificultad**: grilla 2×2 de tiles (radio 16): nombre (Fácil, Normal, Difícil, Muy
  difícil), frase corta (Para relajarse, El de siempre, Para pensar, Reto mayor), medidor de
  1 a 4 barritas en acento, "12 de 50" en `--num` con barra fina de progreso y estrellas
  ganadas (icono SVG de estrella, nada de caracteres ★). El tile elegido lleva borde de acento
  y `aria-pressed`. Tocar uno cambia la ruta del héroe y se guarda. Las cuatro rutas están
  abiertas desde el principio. Ruta por defecto: Normal.
- Reto del día: además dice la dificultad y las mecánicas de hoy ("Hoy: Normal · Llave").
- Estadísticas: Niveles (superados en total, con "de 200"), Estrellas, Mejor racha.
- "Cómo se juega", filas nuevas: **Llave escondida.** Está metida en una franja de color. Quítale
  lo que tiene encima y sale sola a abrir la caja. / **Candado de color.** La botella se abre
  cuando completas ese color. / **Misterio.** Las capas con signo de pregunta se ven al quedar
  arriba, y lo que ya viste no se vuelve a esconder aunque deshagas. / **Todos tienen salida.**
  Cada nivel se resolvió antes de llegar a ti. Si un movimiento te deja sin salida, te avisamos.
- Pie: "Prototipo para CabriCoach. 200 niveles comprobados, todos con solución."

### 4.2 Mapa de niveles (hoja)
Hoja inferior alta con scroll interno: título "Ruta Normal", "12 de 50", grilla de 5 columnas
(tiles redondeados ≥ 52 px): número en `--num`; superados con sus estrellas chiquitas y tinte de
acento; el actual con borde de acento; los siguientes atenuados con candadito; icono mínimo de
la mecánica en una esquina (llave, candado, ?, largas). Tocar uno abierto lo juega. Se avanza en
orden dentro de cada ruta. Con la ruta completa aparece una celda más "51 en adelante".

### 4.3 Tablero
- **Grupos**: las botellas de una caja se dibujan juntas dentro de un marco (`.caja`): radio 16,
  borde 1,5 px `rgba(255,255,255,.22)`, fondo `rgba(255,255,255,.03)`, padding 6 px. Las filas se
  arman por unidades (botella suelta o caja entera: una caja nunca se parte entre filas) y el
  cálculo de tamaño cuenta el padding del marco. Armar las unidades desde `cajas` (no suponer
  índices), en orden de índice.
- **Caja cerrada**: velo sobre sus botellas (`rgba(11,13,15,.5)` con rayado diagonal blanco al
  4 %), las botellas se ven atenuadas detrás, y un candado SVG de 22 px (trazo blanco y punto de
  acento) montado sobre el borde de arriba, al centro. Con dos cajas, un numerito 1 y 2 en el
  candado y en la llave correspondiente.
- **Llave**: icono SVG de llave de ~60 % del ancho de la botella, blanco con contorno oscuro,
  centrado en la capa `k`: va como capa aparte en `.liq`, posicionada en absoluto a
  `bottom: calc(100% * k / cap)` con alto `100% / cap` (así no depende de cómo se agrupan los
  bloques de color). Se ve también sobre una capa oculta.
- **Salida de la llave** (cuando `verter` devuelve `abre` con una caja), al terminar el vertido:
  la llave se separa de la capa con un pop (escala 1 → 1,25), vuela en arco hasta el candado de la
  caja (WAAPI ~520 ms, curva de la app), el arco del candado se levanta, el candado se encoge y se
  desvanece, el velo se funde (260 ms) y el marco brilla un instante en acento antes de quedar en
  línea suave. Sonido nuevo "abrir" (dos notas triangulares cortas 660 y 990 Hz con un clic de
  ruido) y `vib(14)`. `aria-live`: "Salió la llave: se abrió la caja".
- **Candado de color**: la botella con el líquido atenuado (opacidad .55) y un candado de 24 px
  al centro, con el cuerpo relleno del color `var(--cN)` y el arco blanco; en modo símbolos, el
  glifo del color dentro del cuerpo. `aria-label`: "Botella 9: cerrada con candado rojo. Se abre
  al completar el rojo". Al abrir (después de que cae la tapa de la botella que completó el
  color): un punto del color viaja de esa tapa al candado (360 ms), el candado se abre con un pop
  y se desvanece y la botella recupera su brillo. Mismo sonido "abrir".
- Tocar una botella cerrada: sacudida y, la primera vez por partida, un toast: "Se abre cuando
  completes el rojo" o "Primero saca la llave".
- Deshacer y "Volver al último punto con salida" restauran `E` completo (con `ab`): si se deshace
  hasta antes de abrir, vuelve a estar cerrada, sin animación.
- **Misterio justo**: lo revelado no se vuelve a ocultar. La partida lleva `vistos` (posiciones
  `b:k` del reparto original que ya se vieron) y al restaurar cualquier estado se aplica sobre
  sus `ocultas`. Reiniciar tampoco los vuelve a esconder; "Repetir" desde la hoja de ganar sí
  empieza de cero.
- Cabecera de la partida: "Nivel 12" y el chip "Normal · Llave" (ruta y rasgos); en el reto,
  "Reto del día" con el chip de la fecha y la dificultad.
- **Novedad**: la primera vez que un perfil encuentra una mecánica (llave, candado, misterio,
  largas), antes de jugar sale una hoja corta: mini ilustración (una botella dibujada con el
  mismo `htmlBot`, con su llave o candado), "Novedad" en `.t-label`, título ("Llave escondida",
  "Candado de color", "Misterio", "Botellas largas"), una frase, y "Entendido". Se guarda en
  `vistos` del perfil.
- Tutorial de toques (burbujas de la v0): en el nivel 1 de cualquier ruta si el perfil nunca ha
  ganado un nivel.
- Ganar: etiqueta "Normal · Nivel 12". En L50: título "Ruta completa" y botón "Seguir con el
  nivel 51". El reto del día igual que antes.
- "Ver cómo quedó" del reto: se juega `movs` en seco con `verter` (con `ab`).

### 4.4 Worker
`ejecutarOp` trabaja con `E` y `C` (`C` = `{cap, llaves, cajas, candados}` del nivel):
`generar` (rutas 51+ y reto del día, con `rutaParams`/`diaParams` y modo rápido), `pista`,
`vigilar` (`resolver(..., {rapido:true, tope:40000})`), `retroceder` (lista de `E`).
Los niveles 1-50 salen de `CATALOGO` (embebido): nada que generar.

### 4.5 Persistencia
- Clave `botellas:v1` con `normalizar` que acepta lo viejo. Perfil nuevo:
  `{ ruta:'normal', rutas:{facil:{nivel:1,estrellas:{}}, normal:{...}, dificil:{...}, muy:{...}},
  dias, racha, stats, vistos:{} }`. El `nivel`/`estrellas` del camino de la v0 se guardan en
  `legado` y no se usan.
- Caché de generados: `botellas:niveles:v2` (la v1 queda inválida: cambió el generador).
- `partida`: `{jugador, modo:'ruta'|'dia', ruta, clave, estado:{b,ab}, ocultas, vistos, historial,
  movs, extraUsada, seg}`. Una partida de la v0 (`modo:'camino'`) se descarta.
- URL: `#facil12`, `#normal30`, `#dificil5`, `#muy50`, `#dia`, `#nivel12` (= normal 12) y
  `#mapafacil` (abre el mapa de esa ruta), solo letras y dígitos.

### 4.6 Construcción y pruebas
- `build.py`: marcador nuevo `/*@NIVELES@*/` → `const CATALOGO = <niveles.json>;`. Si no existe
  `niveles.json`, usa `recursos/niveles-muestra.json`. El atajo `window.__botellas` se adapta a `E`/`C`.
- `pruebas-chrome.py` (CDP, ver memoria: `--window-size` no baja de ~500 px): capturas a 390×844
  de inicio con las rutas, mapa de niveles, nivel con llave (antes, a mitad del vuelo de la llave,
  después), nivel con candado (antes y después), nivel con dos cajas, misterio tras deshacer,
  hoja de Novedad, Muy difícil a 320×640 con la botella extra, y ganar "Ruta completa". Sin
  errores de JS y sin scroll horizontal.
