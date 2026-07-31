# Estándar visual — Coach AFC (REV 3.0 "Night Gym")

> Fuente: referentes visuales entregados por Andy el 15/07/2026 (kits UI de apps fitness:
> Evomare/GYM & FITNESS teal sobre negro, dashboard navy+magenta, MULTI FITNESS rojo profundo,
> apps dark con acento lima). Este documento ES la herramienta de estandarización: cualquier
> pantalla nueva se valida contra esta lista antes de darse por terminada.
> Las fotos reales de stock (Freepik, licencia free, NO generadas por IA) viven en `assets/stock/`.

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
- **Número héroe en gradiente** (`.bignum`): peso 300, gradiente vertical claro→acento con background-clip:text.

## 2. Forma y profundidad

- Radios: tarjetas 20 px, tiles internos 14 px, inputs 12 px, botones y chips = píldora (999 px).
- Tarjetas: fondo card + borde 1 px `--line` + sombra suave `0 8px 24px rgba(0,0,0,.35)`.
- Chrome (topbar, nav inferior, barra de descanso): vidrio — `backdrop-filter: blur(18px)` sobre rgba del bg al 78–85 %.
- El grano/noise se conserva pero a opacidad ≤ .04 (textura, no protagonismo).

## 3. Tipografía (actualizada REV 18, pedido de Andy 28/07)

- **Display/títulos/números grandes: Bricolage Grotesque** (variable opsz/wdth/wght, embebida como data-URI, NUNCA Google Fonts por link — el artifact bloquea hosts externos). Peso 800 títulos y números destacados, 700 subtítulos. Solo display, nunca párrafos.
- **Cuerpo/labels/botones/UI: Schibsted Grotesk** (variable, embebida). Cuerpo 400, botones y énfasis 500, micro-labels uppercase 600 (por legibilidad a 10px).
- Labels/eyebrows: 10-11 px, uppercase, tracking .12em, color `--smoke` (único uppercase permitido).
- Números de datos tabulares pequeños (tablas, macrolines, series): IBM Plex Mono 700 se conserva. Números héroe (34-44 px), stats y timer: Bricolage 800.
- Jerarquía de referencia: número enorme → label pequeño debajo.

## 4. Componentes canónicos (de los referentes)

- **Slider de progreso con perilla** (barra fina + knob blanco con halo) para la métrica principal del hero; **anillos de progreso** pequeños con gradiente para métricas secundarias (checkpoint, rotación de recetas).
- **Fila de stats dividida** (`.statrow`): 3 columnas separadas por hairlines verticales, número grande peso 300, label pequeño, mini-barra de 44px debajo (ref. 83 | 79 | 1.15).
- **Regla anti-"IA"**: máximo un tipo de chip por tarjeta; los datos secundarios van en UNA línea mono compacta ("40 g prot · ~750 kcal · $6.475"), no en filas de chips idénticos. Listas largas llevan badge cuadrado-redondeado con las 3 letras de la categoría (RES/POL/CER), no chips repetidos.
- **Week strip**: 7 chips L–D, hoy = contorno acento, día cumplido = punto/relleno acento (ref. Mr.Bobrovsky y Evomare); toca un día → calendario.
- **Calendario mensual** (Entrenar → Calendario): celdas redondeadas, día entrenado = relleno acento, otra actividad = icono (pádel/cardio), pendiente pasado = letra roja; editor de día debajo (actividad, pasos, proteína, agua, peso) y "mover días" con select por rutina.
- **Iconos de comida**: set propio estilo Lucide (beef/drum/pig/fish/egg/zap) en badges y filtros; probados a 12-19-28 px antes de fijarlos.
- **Firma de iconografía (REV 3.3)**: cada icono clave lleva UN punto relleno de acento (`<circle class="acc">`), el resto es trazo; sobre fondos de acento el punto hereda la tinta oscura. Es la firma de la marca: todo icono nuevo debe traer su punto.
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

## 6. Movimiento

- Entradas: fade + translateY 10 px, 280 ms, curva `cubic-bezier(.32,.72,0,1)`.
- Barras y anillos animan su relleno (500–700 ms). Respetar `prefers-reduced-motion`.

## 7. Checklist de aceptación (pasar TODOS antes de entregar)

1. ¿Fondo #0B0D0F y ninguna superficie clara heredada del look "papel"?
2. ¿Un solo acento + gradiente, rojo solo semántico?
3. ¿Cero esquinas rectas visibles (excepto la foto a sangre dentro de su tarjeta)?
4. ¿Display en sentence case, labels pequeños como único uppercase?
5. ¿Al menos un elemento "wow" por pantalla principal (anillo, tarjeta-foto, gráfica glow)?
6. ¿Imágenes dentro del sistema (set navy generado para equipo; nunca personas generadas), siempre con overlay oscuro?
7. ¿Nav y topbar en vidrio, tab activo en acento?
8. ¿Contraste AA en texto secundario sobre tarjetas?
9. ¿Se ve como los referentes y NO "hecho por IA" (sin emojis, sin morado genérico, sin glassmorphism gratuito en todo)?

## Recursos externos evaluados (16/07/2026)

- **21st.dev (MCP)**: búsqueda y metadatos gratis; el CSS de *themes* es gratis; el código de
  componentes React tiene cuota free de 2/día (plan free). Al ser esta app HTML vanilla, se usan
  como referencia de patrón (Apple Activity Ring de kokonutd inspiró el anillo del hero), sin
  gastar retrievals.
- **Freepik stock vía Magnific (MCP)**: incluido en el plan, filtros `license=free` +
  `ai_generated=excluded`. Fuente de toda la fotografía.
