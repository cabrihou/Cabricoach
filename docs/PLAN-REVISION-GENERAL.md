# Plan de revisión general · aprobado 24/08/2026

> **Para la sesión de Claude que ejecute esto**: este documento es autocontenido a
> propósito. La conversación donde se aprobó ya no existe; todo lo que necesitas está
> aquí o en los archivos que se enlazan. Ejecuta UNA fase por sesión de trabajo, en
> orden, y marca el registro de avance del final. No arranques una fase sin cerrar la
> anterior (commit hecho y revisión de Andy pasada).

## Qué es esto

Andy aprobó (24/08/2026) un plan de 5 fases para llevar TODA la app al nivel que
alcanzaron Hyrox, Medidas y Progreso en el rediseño de la REV 207. Incluye los
injertos del análisis de un prototipo de su trabajo (ver Insumos).

**Punto de partida**: REV 207 desplegada (commit `2a019ee`). Pendiente sin commitear al
escribir esto: una nota nueva en `docs/PRUEBAS.md` (la trampa de transiciones en
headless); va en el primer commit de la Fase 1.

## Reglas innegociables (resumen; el detalle manda en su fuente)

1. **Lee primero** `CLAUDE.md` del proyecto y `docs/DESIGN-STANDARDS.md` (lo escribió
   Andy; manda sobre cualquier gusto tuyo). `docs/MAPA.md` da los códigos de zona
   (I4b, P7a, HX1b...) que usa este plan.
2. **El archivo** `coach-afc-v2.html` (~1,9 MB, líneas de megabytes en base64): nunca
   grep/sed/awk amplio. Buscar con python3 sobre copia limpia
   (`re.sub(r'data:[a-z0-9/+.-]+;base64,[A-Za-z0-9+/=]+','data:B',t)`); editar con
   reemplazos EXACTOS verificando 1 sola coincidencia.
3. **Snapshot antes de cada fase**: `cp coach-afc-v2.html /tmp/base-fase-N.html` y
   tras cada tanda `python3 herramientas/verificar.py coach-afc-v2.html
   --base=/tmp/base-fase-N.html` → debe decir **"sin regresiones"**.
4. **Navegador real obligatorio** (receta completa en `docs/PRUEBAS.md`): servidor
   http, Chrome headless + CDP, viewport 390x844, 0 errores de consola, dos usuarios
   (`ACTIONS._doSwitch('cami')`). **Trampa nueva documentada**: las transiciones CSS y
   los rAF se congelan en headless; antes de medir una transición, fuerza 4-6
   `Page.captureScreenshot` seguidos.
5. **Agentes sobre el archivo SIEMPRE en serie**, nunca en paralelo. Opus para diseño
   y lógica, Sonnet para volumen mecánico.
6. **Revisión en dos capas antes de Andy**: (a) el agente entrega con verificador +
   CDP; (b) la sesión coordinadora revisa CAPTURAS como director de producto (busca
   truncamientos, incoherencias de datos, jerarquía, casos borde con datos vacíos) y
   devuelve correcciones las rondas que haga falta. Solo entonces se le muestra a Andy.
7. **Un commit/REV por fase** (bump de `APPREV` y de `cabritos-vN` en los dos
   `sw.js`; el hook de pre-commit sincroniza `site/`). **Nada se despliega sin que
   Andy lo revise en local** (`python3 -m http.server` + su navegador); el push a
   main ES el deploy (Netlify), así que commitear sin push está bien mientras revisa.
8. **Copy**: español de Colombia, cercano, sin regaños, **nada de rayas largas (—)**.
   Comentarios de código en español sin tildes explicando el porqué.
9. **Los cálculos no se tocan** en este plan: es reorganización, movimiento y
   presentación. Si una tarea parece exigir cambiar una fórmula, se anota y se
   pregunta a Andy antes.

## Insumos

- **Biblioteca de componentes**: `~/Documents/Projects/Recursos/componentes/`
  - `numero-rodante/vanilla/` (cifras que ruedan tipo odómetro; API
    `numeroRodante(el,{dec,locale,dur})`, `.set(v)`). OJO: para integrarlo a la app
    hay que INYECTAR su CSS y JS en el archivo único (no hay imports); adaptar
    nombres de clase si chocan.
  - `tabs-expandibles/vanilla/` (la técnica que interesa: medir el rótulo una vez y
    animar `max-width` a `var(--w)`; el patrón xtabs ya existe en la app).
  - Trampa aprendida (está en los README): el truco de grid 0fr→1fr NO sirve para
    ancho en contenedores auto; solo para altura con ancho definido.
- **Informe del prototipo de Bink**: `archivo/informe-prototipo-bink/`
  (`informe-prototipo.md` + 65 capturas en `capturas/` + `proto.css`).
  **Fuera de git a propósito: es material interno del trabajo de Andy. NO lo muevas
  a una carpeta versionada ni lo cites textualmente en commits.**
  Las propuestas A1-A5 / M1-M5 / B1-B3 que se citan abajo están definidas ahí con su
  técnica de implementación; ese documento es la especificación.

---

## Fase 1 · Movimiento y cifras vivas

*Objetivo: que la app se sienta viva sin cambiar ni un cálculo. Corta y de alto
impacto percibido.*

1. **Número rodante** (adaptar `numero-rodante` al archivo único, clase `.nrod`):
   - Peso del Inicio (I2, el `bignum`) al registrar un peso nuevo.
   - Proteína del día (I4a, el número del anillo) al agregar comida.
   - XP al marcar series (E2) y el acumulado del checkpoint (I3).
   - **NO** en el reloj (Entrenar → Reloj): repinta por frame con `rjPaint`, no lo
     necesita y pelearía con el intervalo.
   - Cuidado con `morphView`: el número rodante muta su propio DOM; hay que
     protegerlo del morph igual que se protege el timer (buscar cómo se excluyen
     nodos vivos del morph antes de decidir el mecanismo).
2. **Despliegue animado en `xtabs` y `mcapas`**: hoy el cambio icono→rótulo es seco.
   Aplicar la técnica de `--w` medido + `max-width` del port `tabs-expandibles`.
   Medir los rótulos tras el render (los tabs se repintan; cachear por texto).
3. **Transición entre pestañas principales**: fundido + deslizamiento corto (~200 ms,
   `cubic-bezier(.32,.72,0,1)` que ya usa la app) al cambiar de tab del nav. Sin
   pelear con morphView (la transición solo aplica cuando cambia la VISTA, no en
   re-renders de la misma). Respetar `prefers-reduced-motion` en todo lo anterior.
4. **B1 del informe**: el punto activo de los carruseles (`carrDots`) se estira de
   5x5 a 16x5 px con transición de width de 200 ms.

*Aceptación*: verificador sin regresiones; CDP con frames forzados mostrando la
animación completada; con `prefers-reduced-motion` emulado (CDP
`Emulation.setEmulatedMedia`) todo cambia SIN animar; 0 errores; dos usuarios.

## Fase 2 · El sistema de 3 niveles al resto de la app (+ injertos A del informe)

*Objetivo: que Comida/Gestión, Agenda y Check-in/Retos respiren como Hyrox y Medidas.
Los componentes ya existen: `.ngrid/.ncell`, `.steps`, `schedhead`, `INFO3`/`i3()`,
`carr()`, `hlCard`, `i3Aviso`.*

1. **Comida/Gestión** (C5, la vista más densa que queda): jerarquía cifra → desglose
   plegado → ventana; recetas del mercado en carrusel; la semana comida por comida
   con cabeceras compactas.
2. **Agenda** (A4): editar un día pasado con el mismo patrón; menos cajas abiertas a
   la vez.
3. **Check-in (K1) y Retos (R1)**: compactar con nivel 1 arriba y desglose plegado.
4. **A1 · "Cómo se calculó"**: helper `calcBox(filas, total)` dentro de `INFO3` para
   P7a (nivel de fuerza con Epley sustituido), MC3 (series efectivas), P10 (fecha
   proyectada) e I4h (g/kg). El modelo es MD4 (Navy), que ya lo hace bien.
5. **A2 · Barra de hitos etiquetados**: pista continua con 2-3 hitos posicionados por
   valor real (nombre + cifra; check cuando se supera) en P10, MD8 y HX1b. Es
   DISTINTA de `.steps` (escalones discretos): conviven.
6. **A3 · Cabecera de grupo con agregado a la derecha**: P6, E4, I4d, FT3d.
7. **A4 · Estado pendiente con tres señales** (borde punteado + cifra atenuada +
   estado en palabras, nunca solo color): E2a series, C5d `.mealrow`, A4b chips.
8. **A5 · Espera cuantificada**: I2d, K1, C5a dicen qué se acumula o se pierde
   mientras algo falta, con la frase tranquilizadora.
9. **M2 · Filas de negrita inicial + resto atenuado** (helper `filaExplica`): I1b,
   M1, M7, M9, HX1c.
10. **M4 · Avatar de respaldo con inicial en cápsula tintada**: definir EL fallback
    estándar (E5 fotos de ejercicio que faltan, C2c recetas, FT3d miniaturas).

*Aceptación*: además de lo estándar, ninguna vista muestra más de ~4 líneas de texto
corrido sin pedirlo; `MAPA.md` actualizado con cualquier zona que cambie de forma.

## Fase 3 · Flujos de registro en menos toques (+ injertos M del informe)

1. **Buscador de comida** (I4c/nlogPanel): lo frecuente y lo reciente del usuario
   primero, antes de escribir (hoy arranca en frío). Derivarlo de `S.nlog` (lo más
   registrado en 14 días); sin tocar el catálogo.
2. **Micro-confirmaciones consistentes**: serie marcada, agua sumada, meta del día
   cerrada; hoy conviven toast genérico, tooltip y nada. Unificar en un patrón (qué
   pasó + efecto: "Serie 3 · 12 reps · +10 XP").
3. **M3 · Contexto que aparece con el filtro**: P3 (elegir categoría añade línea de
   total del periodo y delta), MC2, FT3c.
4. **M1 · Hoja inferior** como variante de presentación de `.fbox` (`.fbox.sheet`,
   anclada abajo, translateY 280 ms) para E5c, MD3 y FT4. Hacerla MEJOR que el
   prototipo: la de ellos ni siquiera anima.
5. **M5 · Pie de espera que tranquiliza**: C2g, FT1a, M9, M10.
6. **B3 · Nudge de "te acercas"**: P10 a menos de un escalón de la meta, MD1 a 2 días
   de una toma.

## Fase 4 · Consistencia y deuda

1. Los ~88 botones solo-icono sin `aria-label` → **a cero** (el verificador los
   cuenta; bajar el número heredado, no solo no crecerlo).
2. La tabla de evolución del check-in que scrollea horizontal a 320 px (K1).
3. "Leche" duplicada en la lista de compras (recetas en ml vs básicos en L).
4. Revisar los ~50 avisos heredados del verificador y bajar los que se puedan.
5. Los 3 nodos de imagen pendientes de regenerar en el space "Character Model Sheet
   Development" (los corre ANDY, cuestan créditos; solo recordárselo): `hx_ski` y
   `hx_row` salieron con el rótulo "Concept 2" legible (agregar al prompt "unbranded
   machine, no logos"), `hx_zercher_carry` con pose de peso muerto en vez de barra en
   los codos. Al estar listos: bajar, `sips -z 480 480 -s format jpeg -s
   formatOptions 62`, a `assets/ej/` y `site/assets/ej/`.

## Fase 5 · Tema claro

*La más larga; va de última porque toca todo lo anterior.*

1. Inventario de supuestos dark horneados: transparencias `rgba(255,255,255,x)`,
   sombras, gradientes de las gráficas SVG, `glow`, imágenes de fondo night-gym.
2. Convertir a tokens todo lo que no lo sea; definir la paleta clara respetando la
   identidad (dorado de Cami y azul de Andrés siguen mandando).
3. Interruptor en MÁS (`S.cfg.tema`), con opción "automático" por hora del día.
4. Las ilustraciones de la cabra están pensadas para fondo oscuro: revisar cuáles
   necesitan tratamiento (halo/placa) en claro; NO regenerar imágenes sin Andy.
5. Probar TODA la app en claro con capturas de las 12 vistas x 2 usuarios; el
   verificador no ve colores, así que aquí la revisión visual es la red de seguridad.

---

## Registro de avance

Marca al cerrar cada punto. Una fase se cierra con: verificador sin regresiones +
pase CDP completo + revisión de producto en capturas + revisión de Andy en local +
commit "REV N: ..." (sin push hasta que Andy apruebe el deploy).

- [ ] Fase 1 · Movimiento y cifras vivas
- [ ] Fase 2 · Sistema de 3 niveles + injertos A
- [ ] Fase 3 · Flujos de registro + injertos M
- [ ] Fase 4 · Consistencia y deuda
- [ ] Fase 5 · Tema claro

Notas de ejecución (agrega aquí decisiones, hallazgos y lo que quede a medias):

### Fase 1 · ejecutada 24/08/2026 (commit REV 208, sin push: falta la revisión de Andy en local)

Implementado completo: número rodante, despliegue de xtabs/mcapas con `--w` medido,
transición direccional entre pestañas del nav y B1. Verificador sin regresiones
(0 fallos, 51 avisos heredados), suite CDP completa en verde, 0 errores de consola,
dos usuarios, reduced-motion emulado OK, sin desborde a 320 px.

Decisiones tomadas donde el plan era ambiguo (los códigos de zona del punto 1 venían
corridos respecto a MAPA.md):

- "Peso del Inicio (I2)" se leyó como el bignum del hero (I1 en MAPA). Ahí el rodante
  REEMPLAZA al count-up de entrada: al entrar a la vista rueda desde el 82% (mismo
  arranque que el count-up viejo) y al registrar un peso rueda al valor nuevo.
- "El número del anillo" de I4a es `<text>` de SVG y no se puede partir en columnas:
  quedó como número HTML superpuesto (`.ringrod`) centrado donde ring() pintaba main.
  Alineación verificada con capturas contra el anillo de pasos (sigue en SVG).
- "XP al marcar series (E2)": no existía cifra de XP visible en la sesión, así que se
  agregó un contador pequeño `.sesxp` (rayo + número + "XP") junto al progreso de
  ejercicios en la cabecera. Es solo presentación: lee el registro anti-farmeo
  `xpPaid` que ya existía en el draft. Documentado como E2g en MAPA.md.
- "El acumulado del checkpoint (I3)": se aplicó al contador de agua (`.wml`), el
  acumulador que más se toca. Los pasos NO ruedan: su formato cambia de forma
  ("1,9k") y el rodante formatea números puros.
- El cambio "seco" de xtabs se debía a que Hyrox y Medidas no están en MORPH_VISTAS
  (el reemplazo entero mata la transición CSS). No se metieron al morph (riesgo fuera
  de alcance): además del `--xw` medido, `xtabsPaso()` reproduce la apertura a mano
  solo cuando la pestaña activa cambió en un render sin morph.
- B1 ya estaba implementado en REV 207 (6→18 px con transición): solo se ajustó la
  duración a 200 ms según el informe. Verificado vivo (los puntos siguen el scroll).
- Transición de vistas: 200 ms, horizontal según el orden del nav (`vgo-r`/`vgo-l`),
  vertical (`vgo-u`) al llegar desde fuera del nav; los re-renders de la misma vista
  y los cambios de sub-pestaña ya no re-animan. morphView pasó de comparar
  `className==='view-in'` a `classList.contains` para tolerar la clase de dirección.

Hallazgo colateral corregido: la barra de progreso de la cabecera de sesión
(`.bar.thin.grow` en vSession) llevaba colapsada a 0 px desde antes: todas las
reglas CSS `.grow` son de ámbito (`.row .grow`, `.schedhead .grow`...) y ninguna
aplicaba ahí. Se arregló con estilo inline en esa fila; NO se creó una utilidad
global `.grow` porque hay decenas de usos de la clase que hoy no crecen y un cambio
global podía mover layouts que ya están bien.

Cifras de fuentes embebidas: `xtwDe` cachea por texto y se invalida con
`document.fonts.ready` por si midió antes de cargar la fuente.

