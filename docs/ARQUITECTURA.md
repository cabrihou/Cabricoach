# Arquitectura de CabriCoach

> Estado al corte: REV 123 (03/08/2026). Este documento explica CÓMO funciona la app
> por dentro, con los porqués. Para tomar el proyecto en otro computador léelo junto
> con [PRUEBAS.md](PRUEBAS.md) (cómo verificar), [MAPA.md](MAPA.md) (dónde está cada
> cosa) y [CONTEXTO.md](CONTEXTO.md) (estado actual y pendientes). El estándar visual
> es [DESIGN-STANDARDS.md](DESIGN-STANDARDS.md) y manda sobre cualquier pantalla.

## 1. Forma general

PWA de **archivo único**: `coach-afc-v2.html` (~1,1 MB tras extraer las imágenes de
interfaz a `assets/cab/`; las fotos de ejercicios viven en `assets/ej/`). HTML + CSS +
JS vanilla, sin build, sin dependencias. `site/` es la copia desplegable (Netlify) y
se sincroniza sola en el pre-commit.

Dos usuarios en el mismo dispositivo: `UID` ∈ `andres | cami`. Cambio de usuario con
PIN opcional (`ACTIONS.switchUser` → `_doSwitch`).

## 2. Estado

- Objeto global `S`, persistido por clave con `save('clave')` → localStorage.
- Claves por usuario `afc2:u:<uid>:<clave>`; compartidas `afc2:shared:<clave>`
  (`SHARED_KEYS`: meal, retos, ideas, recipeIdeas, facturas, customFoods).
- `save()` además invalida cachés de día (`clearDayCache`) y dispara `sbPush` si hay
  nube (Supabase, tabla `kv`, aislamiento por código de casa, sin login).
- Fotos y facturas en IndexedDB `cabritos-fotos` (stores `fotos`, `facturas`).
- Datos del otro usuario se leen con `partnerState('clave')`.

Claves de estado que más se tocan: `week` (plan semanal de entreno por día 0-6),
`sessions`, `logs` (historial por ejercicio), `weights`, `steps`, `water`, `nlog`
(loggeo de comida por franja m/t/n), `free`, `meals`, `checkins`, `cfg` (metas,
PIN, `gestOpen`, `weekResetStamp`), `meal` (todo el sistema de comida compartido:
`selected`, `prefs`, `plan`, `scoops`, `extras2`, `swaps`, `hide`, `checks`...).

## 3. Ciclo de render y estabilidad del scroll

`render()` → `renderReal()` arma el HTML de `VIEWS[UI.tab]()` y lo aplica de dos
formas distintas:

- **Misma vista → MORPH** (REV 136). `morphView` compara el HTML nuevo contra el que
  ya está en pantalla y toca solo lo que cambió, en vez de reemplazarlo. Así el campo
  enfocado nunca se recrea (el teclado no se cierra), las imágenes no se vuelven a
  descargar, los `select` conservan su valor y las secciones con `content-visibility`
  no vuelven a medir su placeholder. Es un morphdom mínimo escrito en el archivo
  (la app no tiene npm ni build): `morphClave` identifica cada fila por sus `data-*`
  para poder reordenar sin recrear, y ante cualquier duda reemplaza el nodo, que es
  el comportamiento viejo. Si algo falla, `morphView` devuelve false y se cae al
  `innerHTML` de siempre. Vistas habilitadas en `MORPH_VISTAS`.
- **Cambio de vista → reemplazo entero**, que es lo correcto: la vista nueva arranca
  desde arriba.

Con morph el scroll no se toca (el DOM sobrevivió, la página nunca se encogió) y solo
se corrige con el **ancla visual**: se recuerda un NODO real y su posición en pantalla
antes de tocar el DOM, y después se ajusta el scroll por la diferencia exacta. A qué
se ancla depende de DE DÓNDE viene el render:

- viene de escribir → el ancla es el campo (no colapsa nunca) y se vigila ~1,5 s,
  porque el layout sigue moviéndose después (content-visibility);
- viene de un tap (`UI._ancla` lo dejó el despachador de clicks) → el ancla es la
  primera sección visible y se vigila solo unos frames. Seguir al campo aquí era un
  error: el buscador de comida conserva el foco, y al tocar "Guardar loggeo" el
  registro nuevo aparece encima y arrastraba la pantalla 178 px.

Debajo sigue vivo el aparato viejo (apuntalado de altura + ancla por selector) para
las vistas sin morph y para el cambio de vista.

### Cómo era antes (y por qué existe todo lo de abajo)

Hasta REV 135 `renderReal` reconstruía `#view` ENTERO en cada cambio. No hay virtual
DOM: cualquier cambio re-pintaba la vista completa.
`UI` es el estado efímero de interfaz (pestaña, sub-pestaña, ventanas, filtros); no
se persiste.

Tres piezas hacen que ese re-pintado total no se sienta:

1. **content-visibility**: `.mod{content-visibility:auto;contain-intrinsic-size:auto 240px}`.
   Las secciones fuera de pantalla no se renderizan (rendimiento), PERO recién
   pintadas miden su placeholder de 240px y el navegador las infla después, por
   frames. Consecuencia: cualquier medición de layout inmediatamente tras un render
   puede estar mintiendo. Esta es LA trampa número uno de la app.
2. **Apuntalado de altura**: al re-pintar la misma vista, si la página recién puesta
   es más corta que el scroll a devolver (por los placeholders), el navegador
   recortaría el scroll y el usuario saltaría al inicio. `renderReal` apuntala
   `#view.style.minHeight` para que el scroll quepa. NO se suelta por temporizador
   (con placeholders no se puede saber la altura real); se limpia al cambiar de
   vista, cuando el scroll arranca de cero.
3. **Ancla re-aplicada por frames**: se define UN ancla por render: el campo enfocado
   (si se está escribiendo) o el control recién tocado (el despachador de clicks
   guarda `UI._ancla` con selector construido de sus `data-*`, índice de aparición
   —los 7 días de la semana repiten atributos— y su `top` en pantalla). Tras el
   render, `aplicar()` corrige el scroll para dejar el ancla donde estaba, y un
   `vigila()` por `requestAnimationFrame` re-aplica durante ~1,5 s vigilando la
   POSICIÓN del ancla (no la altura del documento: content-visibility puede
   recolocar el ancla sin mover la altura total), salvo que el usuario mueva el
   scroll él mismo (guardia de 80px). Además cada render sube una GENERACIÓN
   (`renderReal._gen`) y los vigilantes de renders anteriores se apagan solos: dos
   vigilantes vivos a la vez corrigen contra fotos distintas de la pantalla y esa
   pelea era el salto que quedaba al escribir la primera búsqueda tras abrir la app
   (la carga perezosa de paquetes mete un segundo render a ~50 ms de la tecla; ver
   el comentario en `paqCargar`, que también preserva el foco del campo).

Si agregas un control con `data-*` nuevos y quieres que el ancla lo distinga,
revisa la lista de atributos que arma el selector en el despachador de clicks
(`['u','i','n','d','k','t','v','x','m','id','rid','ix','r','w','u2']`).

## 4. Despacho de eventos

- Click: delegación global `[data-a="nombre"]` → `ACTIONS.nombre(dataset, el)`.
  El botón MÁS INTERNO gana (closest). Errores caen en un toast, no revientan.
- Campos: `[data-ch]` → `CHANGES` en el evento `change`; los buscadores en vivo
  (`CH_ENVIVO`) también en `input`. OJO: no envuelvas un `CHANGES` en
  "guardar scroll y devolverlo": eso pelea con el ancla del render (pasó, se quitó).
- `<details>` de los días de la semana comida por comida: su estado vive en
  `UI.gestDiasOpen` vía listener de `toggle` en captura (no burbujea).
- Ventanas flotantes: `.fbox` colgadas de `document.body`, SOBREVIVEN al render.
  Patrón: `xxxBoxOpen()` crea, `xxxRedraw()` re-pinta su innerHTML, cerrar al tocar
  el fondo. Ejemplos: repartoBox, cycBox, isla semanal (`islaSemanaHTML`), cambio de
  ingrediente (`swapBoxHTML`), próximo entreno (`proxBoxOpen`).
- Gestos: motor de deslizar-para-borrar (`swdPick` decide qué fila participa:
  series `.settbl.srow`, cabecera de ejercicio `.exrowhead`, ítem del mercado
  `.mktrow`). Umbral 18px y claramente horizontal para no comerse los taps.

## 5. El sistema de comida (el corazón)

Cadena de dependencias, de metas a mercado:

```
metasDe(uid)            metas dinámicas por peso: prot=peso*1.8, grasa=peso*0.8,
  |                     kcal=peso*kcalKg (ratio por persona), carbos=lo que sobra.
  |                     Peso base: promedio de pesajes de 7 días. Cache semanal
  |                     (_metasCache por lunes), invalidable con metasInvalidar().
  v
comidasDe(uid)          reparte las metas entre 1-5 comidas según prefs
  |                     (S.meal.prefs.comidas y .reparto, repartoEfectivo()).
  v
recetaDeComida()        qué receta cae en cada comida de cada día: rotación
  |                     DETERMINISTA sobre la secuencia ponderada rotSecuencia()
  |                     (las porciones/semana son la frecuencia relativa, reparto
  |                     tipo Bresenham; pesos iguales = round-robin clásico).
  |                     Solo recetas APTAS por momento (mom: desayuno/almuerzo/
  |                     cena/snack, momentosDeEtiqueta). Lo manual (S.meal.plan)
  |                     siempre gana.
  v
recetaEfectiva(r,key)   aplica los cambios de ingrediente de esa persona
  |                     (S.meal.swaps[key][rid][nombreOriginal] = nuevo).
  |                     Grupos de equivalencia SWAP_GRUPOS (carb / salsa);
  |                     cantidad convertida por carbohidratos equivalentes
  |                     (cantEquivalente), salsas volumen por volumen. Ajusta
  |                     también los macros declarados con el delta real.
  v
escalaReceta(r,w,       motor de escalado POR INGREDIENTE (no factor único):
  objP, objKc)          sube los rol 'prot' hasta la meta de proteína; si las kcal
  |                     se pasan del techo, bajan primero 'gras' y luego 'carb'
  |                     con pisos (0.35/0.40); 'libre' (verduras) no se toca.
  |                     Las dos fases se ALTERNAN (4 vueltas) porque recortar
  |                     carbos se lleva proteína. Topes: FACTOR_TOPE=3 por
  |                     proporción y TOPE_ABS por cantidad real (5 huevos, 350 g).
  |                     La meta se traduce entre la escala de los macros DECLARADOS
  |                     y la de la suma de ingredientes (kProt/kKcal): sin eso se
  |                     apunta a un número y se mide en otro. Los macros mostrados
  |                     quedan anclados a los declarados (la tabla reparte el
  |                     ajuste, no reescribe cifras). Datos: ING_MACROS (los ~70
  |                     ingredientes con pg/cg/fg por 100g o unidad y su rol).
  |                     Si falta un ingrediente en la tabla: escalado proporcional
  |                     viejo (red de seguridad). Devuelve ajustes[] en lenguaje
  |                     llano para la UI ("menos arroz (120->70 g)").
  v
comidaArmada(uid,dl,i)  la comida lista: receta efectiva escalada + scoops.
  |                     La usan la semana comida por comida (gestPlanHTML), el
  |                     resumen (gestData), el chip de meal prep y el mercado.
  v
vLista()                el mercado compra EXACTAMENTE lo que la semana del plan
                        consume (7 días x comidas x 2 personas, ingredientes ya
                        escalados) + básicos (STAPLES) + extras. Nada de
                        multiplicar porciones a mano: eso compraba para 60 comidas
                        cuando la semana tiene 42. Ítems ocultables (S.meal.hide,
                        X o deslizar, chip restaurar). Precios COP por kg/L/unid,
                        verificados contra mercado real en jul-2026.
```

Reglas de negocio que no se negocian:
- **Andrés usa retatrutida: su riesgo es comer DE MENOS.** Toda la nutrición empuja
  a alcanzar la proteína, nunca a restringir.
- Nadie desayuna albóndigas: la rotación filtra por momento.
- El plan del día pasado se edita con el MISMO panel del home (nutriDay con fecha).

## 6. Entrenamiento

- Plan semanal: `S.week` = {dow: rutinaId | 'mov' | 'rest'}; `weekTok/routineOn/weekSet`.
  Sin `S.week`, cae a la plantilla por defecto (ROUTINES[].day).
- **Reinicio dominical**: `weekAutoReset()` (llamado al inicio de cada render, barato)
  vuelve a la plantilla base cada domingo 8 pm; sello en `S.cfg.weekResetStamp`.
  La primera corrida tras actualizar solo sella, no borra.
- **Isla semanal**: tocar la caja de entrenamiento del inicio abre la fbox con los 7
  días (selects) sobre el MISMO S.week: calendario, pestaña Entrenar e isla quedan
  sincronizados por construcción. Botón directo "Entrenar: rutina de hoy".
- Sesión: `S.draft` (series por ejercicio, `done`, peso/reps), al terminar pasa a
  `S.sessions` + `S.logs` (historial por ejercicio) y paga XP. Los círculos de serie,
  el checkbox de ejercicio completo y el completar-todo del final viven en Entrenar.
- Cápsula "Tu próximo entreno": `proxEntreno()` decide de qué hablar; `proxAnalisis()`
  saca insights REALES del historial (días sin esa rutina, récords cerca, estancados
  3 sesiones, series incompletas); `proxCardRich()` pinta la tarjeta del rotador y
  `proxBoxOpen()` la ventana. **Enganche de IA**: la clave localStorage
  `afc2:u:<uid>:proxIA` con `{d:'YYYY-MM-DD', txt}` (mismo patrón que
  `afc2:u:coach:daily` del coach diario) reemplaza el análisis local mientras esté
  fresca (hoy o ayer).

## 7. Gráficas (lineChart)

- `pts` con fecha (`d`) activan escala de tiempo real.
- `horizonte:N` extiende la tendencia N días (la proyección dura lo que el rango
  elegido, no un % de los datos). Las fechas del eje se reparten sobre TODO el
  horizonte, futuras incluidas.
- `piso:v` = mínimo VEROSÍMIL del eje (peso: 90% de la meta; grasa: meta-5). Si un
  dato real queda por debajo, el dato manda. `desdeCero` existe pero ya no se usa:
  el cero literal aplastaba la línea.
- Bandas de descarga (`bands`), serie secundaria (`series2`), meta (`goal`).
- Valores del eje Y en cada línea guía (`.ylab`, se saltan si chocan con la meta).
- `estilo`: `linea` (clásico), `barras` (totales por día: volumen y tiempo arrancan
  así) o `suave` (promedio móvil de 7 puntos con los crudos en punticos). El chip
  de Rendimiento lo guarda por modo en `UI.chartKind` (solo la sesión).

## 7b. Metas de fuerza (P10)

`S.goals` por usuario (viaja a nube): `{id, ex, name, target, start, d}`. La caja
`metasCard` en Progreso muestra mejor marca (`goalBest`: tope de peso por sesión de
`S.logs`), barra desde `start`, escalones a 2,5 kg (`goalSteps`) y proyección de
fecha (`goalProy`: regresión sobre los últimos 12 topes por sesión; si la pendiente
no sube, lo dice en vez de inventar fecha). Alta con buscador en vivo (`goalq`)
sobre EXMAP+EXCAT.

## 7c. Movilidad guiada y gestos de navegación

- `MOV_RUTINA` (10 ejercicios, 3 bloques, ids `mov_*` que también viven en EXCAT
  categoría Movilidad con foto en `assets/ej/`). Player en fbox con temporizador
  (`movPlayerOpen`/`movPlayerTick`, estado en `MOVP`, muere con la caja); al
  terminar marca `S.mobil` (mismo punto de reto de siempre).
- SWN (deslizar para navegar): zonas `data-swnav` — `cal` (mes/semana), `dia`
  (cabecera del detalle de día), `gestdia` (día de Gestión) — y el `#rotcard`.
  Umbral 64 px y 1.5x horizontal, nunca `preventDefault`, no arranca en el borde
  izquierdo (gesto de atrás) ni sobre las filas de deslizar-para-borrar.

## 8. Gestión alimentación (C5)

`vGestion()` arma cajas colapsables con `gestCaja(id, titulo, sub, fnInner, defecto)`:
memoria por usuario en `S.cfg.gestOpen`, y el contenido de una caja cerrada **ni se
construye** (gestPlanHTML arma 42 comidas escaladas; pintarla cerrada era pagar todo
eso). Por defecto solo "La semana comida por comida" abre.

## 9. Service worker y publicación

- `sw.js` (y su copia `site/sw.js`): página network-first (para recibir versiones),
  assets cache-first. `UI_IMGS` se PRECARGA al instalar: sin eso, sin señal en el
  gimnasio una pantalla no visitada quedaría sin imágenes. Las fotos de ejercicios
  (assets/ej, ~11 MB) no se precargan.
- Publicar = subir `APPREV` + subir `cabritos-vN` en LOS DOS sw.js + commit. El hook
  `.githooks/pre-commit` verifica la app, avisa si el REV no subió, exige caches
  iguales y sincroniza `site/index.html` dentro del mismo commit. Push a `main` de
  `cabrihou/Cabricoach` dispara Netlify (el sitio real es cabricoach.netlify.app).

## 10. Enganches externos

- Coach diario: script en `herramientas/coach-diario/` escribe
  `afc2:u:coach:daily`; el rotador lo muestra (`coachDaily`).
- Próximo entreno IA: `afc2:u:<uid>:proxIA` (ver §6).
- Base nutricional Colombia: proyecto hermano en `Personal/nutricion-co/`
  (Open Food Facts, ver su `reporte.md`). Desde REV 124 alimenta el buscador de
  alimentos: 970 productos con macros completos en `assets/paq/nutricion-co.json`,
  carga perezosa (`paqCargar`/`PAQFOODS`), categoría "Paquetes" en el loggeo y
  precache del service worker para offline. Regenerar: `procesar_csv.py` +
  el exportador del catálogo (ver ese repo).

## El mapa del cuerpo (REV 145)

El arte no se dibuja a mano: sale del model sheet anatómico generado en Magnific,
vectorizado a SVG. El archivo traía las tres vistas en un solo lienzo de 2048x1529, así
que el preproceso las **separa por la posición horizontal de cada path** (393 paths, solo
comandos `M L C z`, todos absolutos), calcula el bounding box de cada figura y las
reescribe trasladadas al mismo origen, redondeando a entero. Eso deja las tres vistas
alineadas y en la misma escala, que es lo que hace que la rotación no dé un salto.

Los grises del original se mapearon a clases `a`..`f` en vez de dejar el `fill` inline:
sin eso no se podría tintar ni oscurecer el arte desde CSS, y son 393 paths.

La iluminación no usa `clip-path` sino `<mask>` con degradado: el clip dejaba un corte
recto que delataba el rectángulo. Y el tinte va por `feColorMatrix` en el `<use>`, no por
CSS, porque **el contenido de un `<use>` está en shadow DOM y los selectores descendentes
no lo alcanzan**. Ese fue el intento fallido antes de llegar al filtro.

Peso: 98 KB de arte sobre un archivo que ya iba en 1,2 MB. Se aceptó porque sustituye
un dibujo hecho a mano que no convencía y porque no añade ninguna petición de red.

## La fecha de llegada a la meta (REV 146)

`pesoRecta(dias)` traza una recta de mínimos cuadrados sobre **todas** las pesadas del
periodo (8 semanas, o 4 si no alcanzan). Antes `metaFases` comparaba dos promedios
sueltos (hoy contra hace 28 días) y un solo día de sal o mal dormido movía la fecha de
llegada por semanas; con la recta el ruido diario se cancela.

De ahí salen tres cosas que la app enseña: la pendiente en kg/semana, el **r²** (qué tan
consistente va, traducido a palabras en `metaCalidad`) y el **error estándar de la
pendiente**, que es lo que abre o cierra la ventana de fechas. El viejo ±3 semanas era
un número inventado; ahora una bajada limpia da una ventana estrecha y uno con zigzag
una ancha, que es la información honesta.

En las gráficas de peso la meta pasó a ser el **piso del eje** y se dibuja su línea. Si
la recta cruza la meta dentro del periodo, se marca el punto y la fecha. Si el cruce cae
más allá del eje (mirando 30 días con la meta a 22 semanas), se prolonga la recta
punteada más tenue hasta la línea de meta y se rotula ahí: es la línea imaginaria de
cuándo se lograría, aunque el eje no llegue.

## Series efectivas (REV 147)

El volumen por grupo que había (`weekVolume`) contaba series enteras al grupo del
ejercicio: 3 series de banca eran 3 de pecho y cero de tríceps. Eso miente en las dos
direcciones, porque el tríceps recibe trabajo real que no se contaba y el pecho recibe
menos del que se le apuntaba.

`cargaMuscular(dias)` reparte cada serie entre los músculos según `EJ_PATRONES`, que es
una tabla de EMG por patrón de movimiento (ver [CARGA-MUSCULAR.md](CARGA-MUSCULAR.md)).
Los ejercicios llegan al patrón por id o, si vienen importados, por lo que diga el nombre.
Cobertura: 273 de 300 del catálogo, y lo que no se pudo repartir se dice en pantalla en vez
de desaparecer.

El mapa de calor reusa la misma maquinaria de máscaras del mapa de medidas: una máscara por
zona con los paths de sus músculos, y un rect del color del nivel encima. Por eso el color
sigue la forma anatómica y no se sale del cuerpo.

