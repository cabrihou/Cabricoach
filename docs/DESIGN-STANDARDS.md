# Estándar visual — CabriCoach (REV 4.0 "Night Gym")

> Fuente: referentes visuales entregados por Andy el 15/07/2026 (kits UI de apps fitness:
> Evomare/GYM & FITNESS teal sobre negro, dashboard navy+magenta, MULTI FITNESS rojo profundo,
> apps dark con acento lima). Este documento ES la herramienta de estandarización: cualquier
> pantalla nueva se valida contra esta lista antes de darse por terminada.
> Las fotos reales de stock (Freepik, licencia free, NO generadas por IA) viven en `assets/stock/`.
>
> **Actualizado en REV 101 (31/07/2026)** con el sistema tipográfico Opción 4, los patrones de
> interacción que salieron de la tanda de ajustes (ventanas flotantes, cajas colapsadas, giro de
> tarjetas), las reglas táctiles de la PWA y el mapa de zonas.
> Para señalar una pantalla concreta usa los códigos de `MAPA.md` (I4b, C3d, P2d…).

## Regla madre

**Negro profundo como lienzo, un solo acento vivo con gradiente encima, tarjetas redondeadas
que flotan, números grandes, y fotografía real oscura.** Nada de look "papel impreso", nada
de esquinas a 90°, nada de uppercase en todo.

## 1. Color

| Token | Valor | Uso |
|---|---|---|
| `--paper` (bg) | `#0B0D0F` | fondo de página (negro azulado, nunca #000 puro) |
| `--paper2` | `#14171A` | superficies hundidas / pistas de progreso |
| `--white` (card2) | `#1B1F23` | inputs, tiles anidados, superficies elevadas |
| card | `#15181C` → en `.mod` | tarjeta base sobre el fondo |
| `--ink` | `#F2F5F4` | texto primario |
| `--ink2` | `#AEB6B3` | texto secundario |
| `--smoke` | `#737C79` | texto atenuado, labels |
| `--line` | `rgba(255,255,255,.08)` | hairlines y bordes de tarjeta |
| `--mint` | `#5C8DFF` | acento único (azul, decisión de Andy 16/07: "un azul más azul") |
| `--grad` | `linear-gradient(135deg,#8FB5FF,#3D63F2)` | rellenos de progreso, CTA, anillos |
| `--red` | `#FF5257` | SOLO alertas, récords y línea de meta |

- Un solo acento por pantalla. El rojo nunca decora: significa alerta/meta/récord.
- Glows ambientales permitidos: radial-gradient del acento al 8–14 % de opacidad, arriba de la página o dentro de tarjetas destacadas.
- Texto sobre acento: siempre tinta oscura `#081128`, nunca blanco.
- **Glow interior de tarjeta** (`.glowtop`): radial del acento arriba de la tarjeta héroe fundiéndose a negro (ref. tarjeta "Cognitive Score"); reservado para 1-2 tarjetas por pantalla.
- **Número héroe en gradiente** (`.bignum`): gradiente vertical claro→acento con background-clip:text, peso 700 en Archivo (bajó de 300 al entrar el sistema Opción 4: la fuente de métricas no tiene pesos ligeros).
- **Acento por contexto (`scopeOf`)**: el acento no se escribe a mano por sección, sale del atributo `data-scope` del documento. Nutrición usa el scope compartido (`--mint:#58DFA3`, verde) y el resto hereda el azul. Al agregar una sección que deba cambiar de acento, se registra en `scopeOf()`; nunca se inventa un color suelto en la regla CSS de esa caja.
- **Máximo dos colores tipográficos por tarjeta**, sin contar los de estado. El acento se reserva para acciones, estados activos, progreso y la métrica principal: si todo es acento, nada resalta.

## 2. Forma y profundidad

- Radios: tarjetas 20 px, tiles internos 14 px, inputs 12 px, botones y chips = píldora (999 px).
- Tarjetas: fondo card + borde 1 px `--line` + sombra suave `0 8px 24px rgba(0,0,0,.35)`.
- Chrome (topbar, nav inferior, barra de descanso): vidrio — `backdrop-filter: blur(18px)` sobre rgba del bg al 78–85 %.
- El grano/noise se conserva pero a opacidad ≤ .04 (textura, no protagonismo).

## 3. Tipografía (sistema Opción 4, REV 100, 31/07)

Cuatro familias embebidas como data-URI (nunca por link externo), cuatro variables CSS:

- **Display de impacto: League Spartan 800** (`--display`, 48-64 px, MAYÚSCULAS). Un solo Display por pantalla (hoy solo Retos).
- **Títulos H1/H2: Outfit** (`--ttl`, H1 600 a 28-32 px, H2 500 a 20-24 px, caja de oración).
- **Métricas y toda cifra: Archivo 700** (`--num`, héroe 40-56 px, siempre `font-variant-numeric: tabular-nums`).
- **Cuerpo/labels/botones/UI: Instrument Sans** (`--ui`, cuerpo 400 a 16 px mínimo, labels 500 a 12-13 px, botones 600 a 15-16 px).
- Clases listas: `.t-display .t-h1 .t-h2 .t-metric .t-metric-md .t-unit .t-body .t-body-sm .t-label .t-btn` — no inventar estilos nuevos, reusar estas.
- Mayúsculas sostenidas solo en Display y labels cortos. La unidad de una métrica va 40-60 % más pequeña que el número (`.t-unit`).
- Jerarquía de referencia: número enorme → label pequeño debajo.

### Tabla de referencia

| Rol | Variable | Peso | Tamaño móvil | Caja |
|---|---|---|---|---|
| Display | `--display` | 800 | 48-64 px | MAYÚSCULAS |
| H1 | `--ttl` | 600 | 28-32 px | oración |
| H2 | `--ttl` | 500 (600 con énfasis) | 20-24 px | oración |
| Métrica XL | `--num` | 700 | 40-56 px | tabulares |
| Métrica mediana | `--num` | 600 | 24-36 px | tabulares |
| Body | `--ui` | 400 | 16 px (secundario 14-15) | oración |
| Label | `--ui` | 500 | 12-13 px, tracking .05em | MAYÚS si corto |
| Botón | `--ui` | 600 | 15-16 px | oración |

### Reglas duras

- **Toda cifra va en `--num` con `font-variant-numeric: tabular-nums`.** Nunca League Spartan para cifras funcionales: es la fuente de impacto, no de datos.
- Un solo Display por pantalla (hoy solo lo tiene Retos) y un solo H1 por vista. El Display es opcional: no hay que forzar uno donde no hay mensaje emocional.
- Botones: nunca todo en mayúsculas, nunca bajo 15 px, misma familia y peso en primarios y secundarios. La jerarquía cambia por fondo, borde o contraste, jamás cambiando de fuente.
- Body nunca bajo 16 px. Es también lo que evita el auto-zoom de iOS al enfocar un campo.
- Máximo dos niveles de énfasis dentro de una tarjeta.

### Excepciones aceptadas (documentadas, no ignoradas)

- **28 labels quedaron entre 9 y 11,5 px**: celdas de calendario, ejes de gráficas SVG, texto dentro de la barra de discos, tiras de días. En contenedores de 30-90 px no cabe 12,5 px sin romper la rejilla. Se subieron desde 8-10,5 px hasta donde el espacio permitió.
- **Chips y controles segmentados van a 12-13 px, no a los 15 px de botón**: se tratan como *labels* de navegación y filtro, no como botones de acción. Los botones reales (`.btn` y variantes) sí cumplen el mínimo. Llevarlos a 15 px exigiría rediseñarlos porque a 320 px no caben.

(El sistema anterior Bricolage Grotesque + Schibsted Grotesk + IBM Plex Mono quedó retirado en REV 100. Las cuatro familias nuevas pesan 121 KB, menos que las 187 KB que salieron.)

## 4. Componentes canónicos (de los referentes)

- **Slider de progreso con perilla** (barra fina + knob blanco con halo) para la métrica principal del hero; **anillos de progreso** pequeños con gradiente para métricas secundarias (checkpoint, rotación de recetas).
- **Fila de stats dividida** (`.statrow`): 3 columnas separadas por hairlines verticales, número grande peso 300, label pequeño, mini-barra de 44px debajo (ref. 83 | 79 | 1.15).
- **Regla anti-"IA"**: máximo un tipo de chip por tarjeta; los datos secundarios van en UNA línea mono compacta ("40 g prot · ~750 kcal · $6.475"), no en filas de chips idénticos. Listas largas llevan badge cuadrado-redondeado con las 3 letras de la categoría (RES/POL/CER), no chips repetidos.
- **Week strip**: 7 chips L–D, hoy = contorno acento, día cumplido = punto/relleno acento (ref. Mr.Bobrovsky y Evomare); toca un día → calendario.
- **Calendario mensual** (Entrenar → Calendario): celdas redondeadas, día entrenado = relleno acento, otra actividad = icono (pádel/cardio), pendiente pasado = letra roja; editor de día debajo (actividad, pasos, proteína, agua, peso) y "mover días" con select por rutina.
- **Iconos de comida**: set propio estilo Lucide (beef/drum/pig/fish/egg/zap) en badges y filtros; probados a 12-19-28 px antes de fijarlos.
- **Firma de iconografía (REV 3.3)**: cada icono clave lleva UN punto relleno de acento (`<circle class="acc">`), el resto es trazo; sobre fondos de acento el punto hereda la tinta oscura. Es la firma de la marca: todo icono nuevo debe traer su punto.
- **Dos sets de iconos, y `ic()` consulta SOLID primero.** `SOLID` son los rellenos con degradado; `ICONS` son los de trazo (viewBox 0 0 24 24, stroke-width 2, caps y joins redondeados). Si creas un icono de trazo con un nombre que ya existe en SOLID, **gana SOLID y tu dibujo nunca se ve**: usa un nombre nuevo. Todo icono de interfaz es SVG vectorial; nunca imágenes rasterizadas, que pixelan a 16 px, pesan y no heredan el color del tema.
- **Ventanas flotantes (`.fbox`)**: para cajas que estorban en el flujo pero se necesitan a mano. Se abren desde un botón circular de 44 px fijo arriba a la derecha, con su icono y su `aria-label`; se cierran tocando fuera, con la X o volviendo a tocar el botón. Deben desaparecer al cambiar de contexto (otra pestaña, sesión de entreno activa) y dejar un espaciador arriba para no tapar la primera tarjeta. Hoy: Importar entreno y Calculadora RM en Entrenar. **Ojo**: este patrón se probó en Inicio y se revirtió, porque ahí las cajas sí son el contenido principal. Sirve para herramientas ocasionales, no para lo que se consulta a diario.
- **Cajas colapsadas**: cuando una caja es larga pero su dato clave cabe en una línea, se muestra cerrada con el dato visible en la cabecera y se despliega al tocar en cualquier punto de esa cabecera. Puede auto-abrirse cuando el contexto lo amerita (I4b "Con qué cerrar" se abre sola pasadas las 7 pm si falta 40 % de la proteína), pero **una sola vez al día**: si el usuario la cierra, se respeta.
- **Giro de tarjeta (flip 3D)**: para revelar una segunda cara del mismo dato sin cambiar de pantalla (el modo foto del calendario). `transform-style:preserve-3d` + `rotateY(180deg)` + `backface-visibility:hidden`, 0.55 s, apagado con `prefers-reduced-motion`. La cara trasera siempre tiene un estado vacío sensato: nunca se rompe por falta de dato.
- **Superficie tocable completa**: si una caja lleva a algún lado, se toca entera (`role="button"` + `data-a` en el contenedor), no solo una flecha de 12 px en la esquina.
- **Borrar por fila (swipe + ×)**: el swipe volvió (F6/F7): deslizar la fila de una serie la borra, deslizar la cabecera de un ejercicio lo saca de la sesión de hoy, con fondo rojo revelado detrás (`.swdslot`/`.swdbg`) y un umbral de arrastre antes de confirmar (con Deshacer). El `×` discreto al final de la fila queda como alternativa siempre visible y descubrible (oculto con `visibility:hidden` solo cuando borrar dejaría la lista vacía), para quien no descubra el gesto o esté en una fila llena de inputs donde el swipe no se dispara.
- **Micro-animaciones canónicas**: tanque de agua con ola (`.wtank/.wfill`, sube al marcar vasos), shimmer en barra de pasos mientras no se cumple la meta (`.bar.run`) y glow al cumplirla, count-up de números héroe (620 ms, ease-out), llama de racha viva (`.flick`), pulso del anillo al completar el día (`.ringdone`). Todas se apagan con `prefers-reduced-motion`.
- **Fotos de comida** (mismo set navy): tuppers (`ph-prep`, Plan día), shaker+avena (`ph-shake`, resumen de rotación), bolsa de mercado (`ph-market`, cabecera del Mercado con el costo encima).
- **Más imágenes del set**: caminadora (`ph-tread`, Progreso→Pasos), báscula+metro (`ph-tape`, Check-in), ícono de app 180px (mancuerna glow, apple-touch-icon).
- **Logo (REV 3.4)**: monograma "A" con travesaño de barra de pesas (placas en gradiente, punto de acento central) en insignia squircle rx14 con borde `--grad` y glow; wordmark "Coach AFC" con AFC en texto-gradiente. Es SVG inline en el topbar; reusar el mismo dibujo si se necesita en splash o marketing.
- **Modo foco de sesión**: stepper de chips cuadrado-redondeados (número → check con gradiente al completar), tarjeta única por ejercicio, navegación píldora ANTERIOR/SIGUIENTE, sustitución vía chips.
- **Stat tiles**: icono en cápsula redondeada + número mono + unidad dim, 2–3 por fila.
- **Tarjeta-foto**: fotografía real oscura, overlay `linear-gradient(180deg, transparent 30%, rgba(11,13,15,.94))`, título encima, CTA píldora acento (ref. "Workout ▶", "Weight Training").
- **Barras de progreso**: píldora 8–10 px, pista `rgba(255,255,255,.09)`, relleno `--grad`.
- **Nav inferior**: vidrio, iconos Lucide-style stroke redondeado; tab activo = acento (icono + label), sin fondos duros por celda.
- **Botón primario**: píldora con `--grad`, texto oscuro, glow `0 6px 20px rgba(94,233,206,.35)`.
- **Toggle/checkbox**: redondeados; estado on = acento con tinta oscura.

## 5. Imágenes (assets/stock/)

**Miniaturas de rutinas/actividades (vigente, 16/07):** set propio GENERADO en Magnific (flux-dev),
aprobado por Andy al preferirlo sobre el stock "genérico". Estilo obligatorio del set: bodegón
cinematográfico de EQUIPO (nunca personas), fondo navy-negro, un solo rim light azul eléctrico,
bruma sutil, sin texto. Archivos `gen-{push,pull,legs,rest,padel}-web.jpg`. Cualquier miniatura
nueva se genera con el mismo prompt base para mantener la serie.

**Fotos con personas:** si algún día se necesitan, solo stock real de Freepik (`license=free`,
`ai_generated=excluded`); quedan las 5 anteriores (`push/pull/legs/rest/row-web.jpg`) como reserva.

Reglas comunes: overlay oscuro garantiza contraste AA del texto; ancho 900 px, JPEG q≈52-55,
embebidas como data-URI (la app es un único HTML offline).

### Dónde se generan las imágenes (REGLA DURA, 09/08)

**Todo nodo de imagen se crea en el space "Character Model Sheet Development" de
Magnific, en la pestaña del personaje que corresponda: `Andrés` o `Cami`.** Ahí vive
la referencia del personaje conectada al puerto `reference` de cada generador, que es
lo que mantiene la cara y el color consistentes entre cientos de fotos.

- Nunca se crean nodos sueltos en otro space ni en la Página 1: se pierde la
  referencia y sale otro personaje (pasó y costó una tanda entera).
- Cada nodo es de tipo `image-generator`, 1:1, se llama `EJ — <id>` (ejercicio),
  `MOV — <id>` (movilidad) o `APP — <escena>`, y su prompt es AUTÓNOMO: personaje
  completo + acción + estilo, aunque se repita entre nodos.
- Los dos personajes vigentes, y no se mezclan:
  - **Andrés-Cabrito**: pelaje café/tan (moreno), banda roja, muñequeras azules
    (#5C8DFF), camiseta oscura, brillo azul.
  - **Cami-Cabrita**: pelaje crema-blanco, moño y muñequeras amarillas (#FFC94D),
    brillo dorado.
- Prohibiciones que van SIEMPRE en el prompt: cero texto en la imagen (ni rótulos en
  máquinas o discos) y **sin collar ni campana** en el cuello.
- La cabrita crema con brillo AZUL es la versión de la primera generación: si aparece,
  la foto se rehace. Los ejercicios de Andrés van con el cabrito tan.
- Antes de aceptar una foto: que la POSE sea el ejercicio (no la mascota parada junto
  al equipo), que se vea el punto de apoyo (colchoneta, pared, barra, palo) y que no
  haya dos mascotas en la misma escena.
- Salida a la app: JPEG 480×480 en `assets/ej/` **y** copia en `site/assets/ej/`.

### Las cabritas (constante `CAB`)

Mascota 3D de la casa: cabrita de pelaje crema, cuernos pequeños, gorra granate o gafas
redondas, camiseta navy, render suave tipo Pixar, luz de estudio y **fondo navy plano**.
Se generan en Magnific con ese prompt base para que la serie no se rompa. Formato: 420×420,
JPEG q≈62, ~25-30 KB, embebidas como data-URI.

- **La ilustración debe corresponder al texto.** Una tarjeta que habla de pasos no puede
  mostrar la cabrita leyendo. El mapeo tipo→ilustración vive en `ROTIMG` y hay variante por
  usuario (Andrés / Cami) donde aplica.
- **Magnific es para ilustraciones, no para iconos.** Los glifos de interfaz van en SVG
  (ver sección 4): un icono generado pixela a 16 px, pesa cuarenta veces más y no se puede
  teñir con el acento.
- Cuando falte una ilustración, se deja la clave vacía con un comentario `/* pendiente: … */`
  y un fallback que no rompa el diseño; nunca un hueco.

Existentes en el set: entrenando, comiendo por franja, planeando, celebrando, con el metro,
leyendo, con la Biblia, con idea, tomándose una foto, dormida, con el reloj.

## 6. Movimiento

- Entradas: fade + translateY 10 px, 280 ms, curva `cubic-bezier(.32,.72,0,1)`.
- Barras y anillos animan su relleno (500–700 ms). Respetar `prefers-reduced-motion`.
- Nada debe deslizarse en el primer pintado: los indicadores que se mueven (el de la nav) nacen en su posición final y habilitan la transición dos frames después.

## 7. Gráficas

- **Una gráfica por idea.** Si dos gráficas cuentan lo mismo, sobra una: Rendimiento y Tendencia de peso se solapaban y quedó Rendimiento.
- Selector de intervalo en la esquina superior derecha de la tarjeta, no arriba de la pantalla.
- **Contexto que explica las caídas**: las semanas de descarga se marcan con una franja translúcida (`rgba(255,201,77,.09)`) y un label corto. Sin eso, un bajón planificado se lee como fracaso.
- **Series secundarias** en línea punteada, color distinto y discreto, con leyenda mínima; se normalizan a su propio rango y no se pintan si no hay datos (kcal/día sobre la gráfica de peso).
- Los tres medidores que acompañan una gráfica cambian según la categoría y hablan de su tema. Nunca cifras inventadas: todo sale de datos reales.
- El color nunca es el único indicador de subida, bajada o alerta: siempre lo acompaña un signo, icono o texto.

## 8. Táctil y entrada (PWA en iPhone)

- **Sin zoom.** Viewport con `maximum-scale=1, user-scalable=no`, `touch-action:manipulation` en html y body, y cancelación de `gesturestart` y `dblclick`. El doble toque se bloquea **solo fuera de controles reales** (`button, a, input, select, textarea, label, [data-a], [role=button]`), para no romper los +/− que se tocan repetido.
- **Campos nunca bajo 16 px**: por debajo de eso iOS hace auto-zoom al enfocar y descuadra la pantalla. Es la razón práctica del mínimo de cuerpo del sistema tipográfico.
- **Teclado abierto**: solo se desplaza el campo si quedó tapado, y lo mínimo (`block:'nearest'`), midiendo contra `visualViewport`. Centrar siempre pelea con el desplazamiento propio del navegador y hace brincar la pantalla. Mientras haya un campo enfocado, el render no toca el scroll, y la barra inferior se esconde (`body.kb`).
- Altura táctil cómoda en todo lo que se toca; los botones circulares flotantes van a 44 px.

## 9. Accesibilidad

- Todo botón solo-icono lleva `aria-label` descriptivo. **Deuda actual: ~53 botones sin nombre**, la mayoría con texto condicional; es lo próximo a saldar.
- Los elementos que actúan como botón llevan `role="button"` y son alcanzables por teclado.
- Contraste AA en texto secundario sobre tarjetas.
- Toda animación se apaga con `prefers-reduced-motion`.

## 10. Copy

- Español de Colombia, cercano, sin regaños. La app acompaña, no vigila.
- **Nada de rayas largas (—)** en texto visible.
- Caja de oración en todo salvo Display y labels cortos. Un aviso en mayúscula sostenida se lee como grito.
- Botones con verbos de acción concretos ("Guardar check-in", no "Aceptar").
- El tono se ajusta al contexto: un 34 % de proteína a las 9 am es normal y se dice neutro; a las 9 pm sí es alerta. La misma cifra no significa lo mismo a toda hora.
- Precios en COP con separador de miles. Cantidades medibles por una persona (100 g, 2 unidades), nunca 137,4 g.

## 11. Checklist de aceptación (pasar TODOS antes de entregar)

**Visual**
1. ¿Fondo #0B0D0F y ninguna superficie clara heredada del look "papel"?
2. ¿Un solo acento + gradiente, rojo solo semántico, máximo dos colores tipográficos por tarjeta?
3. ¿Cero esquinas rectas visibles (excepto la foto a sangre dentro de su tarjeta)?
4. ¿Al menos un elemento "wow" por pantalla principal (anillo, tarjeta-foto, gráfica glow)?
5. ¿Imágenes dentro del sistema (set navy generado para equipo; nunca personas generadas), siempre con overlay oscuro, y la ilustración corresponde al texto?
5b. Si hay imagen nueva de mascota: ¿se generó en el space "Character Model Sheet Development", en la pestaña del personaje (Andrés / Cami) y con la referencia conectada? ¿La pose ES el ejercicio, con su punto de apoyo visible, UNA sola mascota, sin texto pegado y sin collar ni campana?
6. ¿Nav y topbar en vidrio, tab activo en acento?
7. ¿Se ve como los referentes y NO "hecho por IA" (sin emojis, sin morado genérico, sin glassmorphism gratuito en todo)?

**Tipografía**
8. ¿Cada texto usa la variable de su rol, y toda cifra está en `--num` con cifras tabulares?
9. ¿Un solo H1 por vista, máximo un Display, mayúsculas solo en Display y labels cortos?
10. ¿Botones en caja de oración, mínimo 15 px, misma fuente en primarios y secundarios?
11. ¿Ningún campo por debajo de 16 px (auto-zoom de iOS)?

**Interacción**
12. ¿Las cajas que llevan a algún lado se tocan enteras, y llevan a donde prometen?
13. ¿Botones solo-icono con `aria-label`, y animaciones apagadas con `prefers-reduced-motion`?
14. ¿Probado a 320, 360, 390 y 430 px, con los dos usuarios, sin desborde horizontal?

**Antes de dar por terminado**
15. ¿`herramientas/verificar.py --base=<snapshot previo>` dice "sin regresiones"?
16. ¿Se vio renderizado en Chrome headless con clics reales, no solo en el código?
17. ¿`MAPA.md` refleja las cajas nuevas o movidas?
18. ¿`./publicar.sh` corrió sin fallos y `site/` quedó sincronizado?

## Recursos externos evaluados (16/07/2026)

- **21st.dev (MCP)**: búsqueda y metadatos gratis; el CSS de *themes* es gratis; el código de
  componentes React tiene cuota free de 2/día (plan free). Al ser esta app HTML vanilla, se usan
  como referencia de patrón (Apple Activity Ring de kokonutd inspiró el anillo del hero), sin
  gastar retrievals.
- **Freepik stock vía Magnific (MCP)**: incluido en el plan, filtros `license=free` +
  `ai_generated=excluded`. Fuente de toda la fotografía.
