# Mapa del sitio · Cabricoach

Nombres acordados para señalar cualquier parte de la app sin ambigüedad.
Cada zona tiene un código corto. Ejemplos de uso: "en I4b el botón no responde",
"C3d debería mostrar la tienda", "quita P2d en la categoría Tiempo".

Entre paréntesis va el nombre de la función en el código (para Claude).

## G · Global (visible en varias pantallas)

- **G1** Barra superior con logo y REV (`#topbar`)
- **G2** Barra de navegación inferior de 5 iconos (`#nav`)
- **G3** Tira de días de la semana bajo el topbar (`daystrip`)
- **G4** Toasts (avisos flotantes de confirmación)
- **G5** Ventana flotante genérica (overlays de PIN, stats de ejercicio, fotos) (`.fbox`)
- **G6** Isla dinámica de descanso/cronómetro (`#island`)

## I · Inicio (`vInicio`)

- **I1** Hero del peso: número grande, "toca para registrar", slider y meta (`.bignum`, `.wtap`)
- **I2** Checkpoint del día: tarjetas de atajos (`ckSection`)
  - I2a Entreno ("Ir a entrenar" + check que completa la rutina)
  - I2b Pasos · I2c Agua · **I2d Medidas** (lleva a Progreso → Medidas, `medGo`; dice
    qué toca hoy o en cuántos días) · I2e Foto del día
- **I4x** Guardar una combinación como **plato reutilizable** (alimento compuesto en
  customFoods, sale en la categoría Platos y se registra con su desglose). Se puede
  desde el borrador (`platoGuardar`) **y desde un loggeo ya guardado** con 2+
  ingredientes (`platoDeEntry`); ambos usan `platoDesde`, que rechaza nombres
  repetidos. Ojo con los macros: en el borrador van por unidad y hay que multiplicar
  por la cantidad; en un registro guardado ya vienen multiplicados
- **I2x** Isla semanal de entrenos: tocar la CAJA de entrenamiento (junto a pasos)
  abre una fbox con los 7 días y su rutina/movilidad/descanso sobre el mismo
  `S.week` del calendario, más botón "Entrenar: rutina de hoy" y plantilla base
  (`islaSemanaHTML`, `ACTIONS.islaSemana`). La semana se reinicia sola cada
  domingo 8 pm (`weekAutoReset`, sello en `S.cfg.weekResetStamp`)
- **I3** Caja rotativa "Para ti": pendiente de hoy, coach del día, versículos, datos, hitos (`homeRotator`, `rotcard`)
  - I3a Cápsula "Tu próximo entreno": desde REV 121 la tarjeta trae jerarquía propia
    (rutina como título, hora, hasta 2 líneas de análisis de las últimas sesiones:
    días sin esa rutina, récords cerca, estancados, series incompletas) y la ventana
    lleva ese análisis arriba (`proxEntreno`, `proxAnalisis`, `proxCardRich`,
    `proxBoxOpen`). Enganche de IA: `afc2:u:<uid>:proxIA` con `{d, txt}` (mismo patrón
    que `coachDaily`) reemplaza el análisis local mientras esté fresco (`proxIA`)
- **I4** Nutrición del día (`nutriDay(t)`, modo completo, + `nutriExtras()`)
  - I4a Anillo de proteína + mensaje del día
  - I4b Caja "Con qué cerrar" (sugerencias sueltas y combinaciones) (`sugBox`)
  - I4c Fila de macros: Carbo / Grasa / Proteína (`.macrow`)
  - I4d Franjas Mañana/Tarde/Noche + buscador de loggeo (`nlogPanel`). Desde REV 137:
    el BORRADOR va arriba (se ve lo que llevas sin bajar), las categorías viven en una
    caja colapsable (`nlogCatTgl`), la cantidad se escribe a mano en cualquier unidad
    (`nlogQtyIn`, antes solo gramos), se puede **Corregir** un registro ya guardado
    (`nlogEditEntry`: vuelve al borrador y se guarda de nuevo), copiar el registro del
    otro usuario (`nlogCopiar`) y **pegar** la tabla nutricional de Google para que la
    app saque los macros sola (`leerMacros` + `pegarTgl`/`pegarUsar`)
  - I4h Cifra de **g de proteína por kg de peso** del día contra la meta de 1,8,
    pegada al total de proteína (`.gkg`); en el bloque de texto de abajo pasaba
    desapercibida
  - I4e Barras de proteína de los últimos 7 días (`.pweek`)
  - I4f/I4g **ya no viven aquí** (Tarea 3): el registro libre "¿Qué comiste?" y la tabla
    "Comidas y macros" se sacaron del Inicio (el dueño no quiere registro en el resumen
    del día) y quedaron en Comida > Gestión, ver C5b. El Inicio conserva solo el resumen:
    anillo, macros, franjas con buscador, sugerencias y barra semanal
- **I5** Tarjeta del ciclo (solo Cami, `cycHome`): anillo de los días del ciclo con el
  tramo de sangrado resaltado y el día actual marcado (`.cycmod`, `cycGradient`), texto
  central con la fecha del próximo período (`cycleInfo` trae `next`/`toNext`), fase y
  cabrita debajo con el consejo del momento (tip/food/animo rotan según la hora). Toca
  la tarjeta y abre el detalle en una `.fbox` (`ACTIONS.cycDetail` → `cycBox`) con las
  cuatro fases del mes (`cycFasesStrip`). Incluye **cómo va su peso esta semana leído
  según la fase** (`cycPesoNota`): compara el promedio de 7 días contra los 7
  anteriores y, en lútea o menstrual, explica que una subida es retención de líquido
  y no grasa. Sin `cycStart` muestra una tarjeta de
  invitación con cabrita, beneficio en dos líneas y botón propio "Activar mi ciclo"
  (`ACTIONS.cycCfgGo` → M6); antes era una línea de texto chiquita que pasaba
  desapercibida (Tarea 4).

- **I6** Reto "Mi primera dominada" (solo Cami, `puCapsula`, en el Inicio bajo el
  checkpoint): la tarea del día son 15
  minutos de 3 dominadas + 1 minuto de descanso. 5 niveles que quitan ayuda en vez de
  sumar reps (banda gruesa → media → delgada → negativas → sin ayuda), y se sube tras
  4 sesiones (`PU_NIVELES`, `S.pullup`). El contador vive en una ventana
  (`puBoxOpen`/`puRedraw`, estado en vivo en `PU`) con **contador circular** (anillo
  que se vacía con el minuto de descanso y muestra las reps en la fase de trabajo,
  sobre la cabrita difuminada) y al minimizarla sigue corriendo en la **isla
  flotante**, que lleva su propio anillo (`updateIsland`) y devuelve a la sesión.
  La resistencia de la banda se elige a mano (`puNivelSet`): la progresión sigue
  subiendo sola, pero un día flojo se puede bajar sin perder el avance

## E · Entrenar (`vEntrenar`)

- **E1x** Tarjeta "Crear rutina" (junto a Personalizado): armador propio, guardado en
  `S.customRoutines` (por usuario, sincroniza a nube). Desde REV 133 es interactivo:
  sin búsqueda muestra las categorías del catálogo navegables con foto y check
  (`crCat`), la búsqueda también trae fotos, y cada ejercicio agregado permite
  editar series (+/-) y el rango de reps (dos campos, `crReps`, coherencia min≤max).
  El teclado ya no se cierra por tecla: `crNombre` no re-pinta la caja (solo toca el
  disabled de Guardar) y `crBuscar` re-enfoca SÍNCRONO (el setTimeout viejo llegaba
  tarde para el teclado de iOS). Las propias entran a ROUTINES vía
  `rutinasRefrescar()`; se borran con la X de su tarjeta
- **E5x** Catálogo enriquecido: los 24 de calistenia y anillas traen grupo muscular
  MÁS implicado (`mus`, "Principal: Espalda" en lista, chip en el detalle) y
  descripción corta de ejecución (`desc`, reemplaza al texto genérico del detalle)
- **E2x** Catálogo: categorías nuevas Calistenia (12 progresiones/habilidades) y
  Calistenia en anillas (12), con equipo "Anillas" en el filtro; las 24 fotos (set
  Andrés-Cabrito) viven en assets/ej desde REV 130
- **E6** Movilidad completa: tocar la tarjeta Movilidad despliega la rutina real de
  14 ejercicios en 3 bloques (muñecas/tobillos, cadera, columna/hombros) con foto,
  dosis y detalle (`MOV_RUTINA`, `ACTIONS.movDetail`), botón "Hecha hoy (+1)" de
  siempre (`mobilTgl`) y "Empezar rutina guiada": player en ventana flotante con
  temporizador que avanza solo, pausa y saltos (`movPlayerOpen`/`movPlayerRedraw`,
  estado en `MOVP`). Al terminar marca la movilidad del día. Los 10 ejercicios
  también están en el catálogo E5 bajo la categoría Movilidad (ids `mov_*`)
- **E1b** Mapa muscular de cabra en Personalizado: dos siluetas (frente y espalda)
  con zonas tocables que seleccionan los mismos grupos que los chips
  (`cabraMapa`, mismo `ACTIONS.persoGrupo`)
- **E1** Rutina del día / lista de rutinas (`.pcard`, sub-pestañas de entrenar: Rutinas · Ejercicios, `UI.sub.train`, `ACTIONS.trainSub`)
  - E1a Caja "Personalizado" junto a Movilidad en el grid de rutinas: formulario de herramientas/tiempo/grupos/intensidad, genera y arranca una sesión con `rid:'perso'` (`vPerso`, `persoGen`, `ACTIONS.persoOpen/persoRoll/persoStart`)
- **E2** Sesión activa (modo foco)
  - E2a Tabla de series: kg, reps, check, botón × de borrar (`setTable`)
  - E2b Divisor de descanso entre series (`.restdiv`)
  - E2c Opciones del ejercicio: nota, cambiar, discos (`exOpts`)
  - E2d Botón "Empezar entreno" / finalizar sesión
  - E2e Círculos de verificación por serie en la cabecera de cada ejercicio: tocar uno
    marca/desmarca esa serie sola (misma lógica que el check de la tabla, reusa
    `ACTIONS.mark`) (`exDots`)
  - E2f Ventana "Series sin marcar" al finalizar con pendientes: completar todas y
    finalizar, finalizar solo con lo hecho, o seguir entrenando (`finishPendBox`)
- **E3** Importar entreno pegando texto (Strong, etc.) (`impTgl`). Desde REV 131 el
  emparejador (`matchExId`) va: nombre exacto del plan > sinónimos > nombre exacto
  del catálogo EXCAT > similitud; si el día ya tiene registros de esos ejercicios
  pregunta si REEMPLAZAR o añadir encima; los ids fuera del plan salen en P7 bajo
  "Importados y catálogo" y sus registros se borran con la X de la tabla
- **E4** Historial de entrenos
- **E5** Sub-pestaña Ejercicios: catálogo EXCAT completo (`vExcat`)
  - E5a Buscador en vivo, sin acentos ni mayúsculas (`excatq`)
  - E5b Cajas colapsadas por categoría con conteo, tocables enteras (`excatRow`, patrón `schedhead`)
  - E5c Ventana flotante de detalle: foto, categoría, equipo, tipo, último peso y "Agregar a la sesión de hoy" si hay sesión activa (`excatDetailBox`)

## A · Agenda (`vAgenda` / `vCalendario`)

- **A1** Selector Semana/Mes + chip de hoy + botón de cámara (`.calpick`, `.calseg`)
- **A2** Vista Semana
  - A2a Caja "Días de cada rutina" (planificador: rutina/movilidad/descanso por día) (`#schedbox`)
  - A2b Campo de hora de entreno + "Crear alerta en el calendario" (.ics) (`trainHour`, `downloadTrainICS`)
- **A3** Vista Mes (rejilla del calendario)
- **A4** Detalle de un día: pasos, entreno de ese día (`vDia` → `calEditor`)
  - A4a Panel de nutrición de ese día, en modo compacto (un día pasado no necesita el
    aparato completo de Inicio): resumen de una línea (proteína y kcal), franjas
    Mañana/Tarde/Noche con lo ya registrado y su buscador/borrador de loggeo real. Sin
    anillo, sin cabritas, sin "con qué cerrar" ni barra de 7 días
    (`nutriDay(sel, {compacto:true})`, contexto de fecha en `nutriT()`/`UI.nutriDate`,
    fijado por `calEditor()`)
  - A4b Chips "Comidas del plan" para marcar sin detallar (no duplican macro si esa
    franja ya tiene loggeo detallado, ver `eatenOn`) (`mealAt`)
  - A4c Agua, peso, inyección y foto de ese día
  - A4d **Correr**: al marcar "Salí a correr" aparece la caja de la carrera con
    distancia y duración; el ritmo se calcula solo (`runBox`, `paceTxt`,
    `runKm`/`runMin`, datos en `S.acts[dia].run`)
- **A5** Modo foto: las tarjetas de los días se giran y muestran la foto (`calFotoTgl`, `.flip3d`)

## C · Comida (`vComida`, sub-pestañas Recetas / Mercado / Gestión)

- **C1** Selector de sub-pestañas (Recetas · Mercado · Gestión; internamente la clave
  de la tercera sigue siendo `UI.sub.food==='mealprep'`, solo cambió el rótulo y lo que
  pinta, para no tocar todas las referencias)
  - C1a Botones flotantes (`foodFabs`, mismo patrón que `trainFabs` de Entrenar):
    calculadora de proteína (`pcalBoxTgl` → `pcalBox`, rescatada de la vieja Plan día) y
    comidas al día + reparto de macros (`repartoBoxTgl` → `repBoxOpen`/`repBoxHTML`,
    N6). Visibles en las 3 sub-pestañas. El reparto también se abre desde C2g, desde
    C5b y es la fuente de `comidasDe(uid)`
- **C2** Recetas (`vRecetas`)
  - C2a CTA "Ármame la semana" + banner de rotación activa (abre C2g)
  - C2b Buscador de recetas
  - C2h Caja "En el mercado · N" con botón "Vaciar mercado" (confirm + deshacer,
    `ACTIONS.mercadoVaciar`); vaciar no borra cambios de ingrediente ni scoops
  - C2c Rejilla de categorías (res, pollo, pescado, desayunos, etc.)
  - C2d Tarjeta de receta abierta: ingredientes, costos, sección "Preparación" (`recCard`)
  - C2e Caja "Sugerir receta" + lista "Ideas de recetas" (`vIdeasReceta`)
  - C2f Proteína de la semana
  - C2g Formulario "Arma la semana": proteínas, comidas al día por persona (N6,
    alimenta las porciones de la semana con `ACTIONS.wkComidas`, 7×comidas tope 14, y
    enlaza a C1a para el reparto fino), porciones por persona, desayuno,
    presupuesto/aprovechar lo de casa, tiempo de cocina, antojos y descartes; genera con
    `autoWeekGen()` y muestra un resumen antes de ir al mercado (`weekFormOpen`,
    `weekFormHTML`, `weekSummaryHTML`, preferencias en `S.meal.prefs`)
- **C3** Mercado (`vLista`)
  - C3a Toggle Ambos/Andrés/Cami + periodo (semanal/quincenal/mensual)
  - C3b Barra de suma parcial: $ marcado vs total
  - C3c Checklist agrupado: Proteínas / Vegetales y frutas / Despensa (`mktCat`).
    Cada fila `.mktrow` se quita con la X o deslizando a la izquierda ("ya lo
    tengo": `S.meal.hide`, `ACTIONS.mkHide`), con deshacer y chip de restaurar.
    Las cantidades salen de la SEMANA REAL del plan (ver ARQUITECTURA §5)
  - C3d Caja "Precios y facturas": registrar precio, foto, pegar texto de factura, histórico (`vFacturas`)
- **C5** Gestión alimentación (`vGestion`, antes "Meal prep"; Tarea 1/2/3 de la fase de
    Gestión). Sin rotación activa (`S.meal.selected` vacío) toda la vista es un estado
    vacío que invita a "Ármame la semana"; el registro libre (C5b) se muestra siempre,
    tenga o no rotación. Desde REV 121 las tres zonas grandes (Resumen y recetas, La
    semana comida por comida, Registro libre) son cajas colapsables con memoria por
    usuario (`gestCaja`, `S.cfg.gestOpen`); por defecto solo la semana está abierta y
    el contenido de una caja cerrada ni se construye
  - C5x Cambio de acompañamiento/salsa por receta: en la semana comida por comida,
    abrir ingredientes muestra los cambiables como chips con flechas
    (`.swapchip`); tocar abre la ventana de alternativas con cantidad convertida
    por carbohidratos equivalentes y costo (`swapBoxHTML`, `S.meal.swaps`,
    `recetaEfectiva`). Por persona y por receta; el mercado lo refleja
  - C5a "La semana con lo que elegiste" (Tarea 2, `gestData`/`gestSemanaHTML`): cruza
    `S.meal.selected` (recetas + porciones `{a,c}`) con `comidasDe(uid)` (comidas al día
    según meta y reparto de cada uno). Tres bloques:
    - "Qué elegiste": cada receta de la rotación con su ícono de categoría, porciones de
      cada uno y macros por porción
    - "Cómo se distribuye": por persona, anillo de proteína/día promedio si lo cocinado
      se reparte en la semana, cuántos de los 7 días alcanza y cuál es la comida más
      grande de su día (`comidasDe` ordenado por `pg`)
    - "Qué te hace falta": huecos calculados y con acción concreta cada uno —
      `faltanComidas = max(0, comidas/día×7 − porciones cocinadas)` con botón "Ármame la
      semana"; proteína/día por debajo del 85% de la meta del plan con botón "Agregar
      recetas" (va a C2); días sin nada cocinado (`diasCubiertos = floor(porciones /
      comidas por día)`, `diasSinNada = 7 − diasCubiertos`) con botón "Ajustar comidas
      por día" (abre C1a). Sin huecos: aviso de que la semana está cubierta
  - C5b Registro del día: "¿Qué comiste?" registro libre (`freeTxt`/`freeAdd`/`freeDel`)
    y tabla "Comidas y macros" con el aviso de comidas vencidas (`mealStatus`) y chip
    "Ajustar" (`repartoBoxTgl`, ver C1a). Vivió un tiempo en el panel de nutrición del
    Inicio (I4f/I4g); el dueño pidió sacarlo de ahí porque el Inicio es un resumen, no
    el lugar de registrar (Tarea 3). Sigue siendo la misma función (`nutriExtras`), solo
    cambió quién la llama; las filas salen de `comidasDe(UID)`, no de una lista fija
  - C5c Caja colapsable "Meal prep del domingo" (`mealPrepBoxHTML`/`mealPrepBody`,
    patrón `schedhead`/`schedbody` como A2a; Tarea 1). Cerrada muestra el dato clave en
    la cabecera (horas estimadas y tuppers de cada uno); abierta despliega el resto:
    - "La misión del domingo": recetas de la rotación activa, porciones de cada uno,
      tuppers totales, tiempo intercalado vs. sumado y hora de arranque (toma
      `S.reminders` id `prep`, hoy 15:00) (`mealPrepTracks`, `mealPrepTimeline`)
    - "Antes de empezar": qué bajar del congelador (`meta.descongelar`), los pasos de
      remojo/reposo nocturno de la víspera (avena trasnochada, `min>=180` en
      `RECIPE_PREP`), utensilios (unión de todas las recetas) y tuppers a alistar
    - "La línea de tiempo": pasos intercalados de todas las recetas con reloj corrido,
      activo/pasivo, marcables uno a uno (`mpStepTgl`, no persiste: es la checklist de
      la sesión de cocina)
    - "Empaque y conservación": tuppers por receta y persona con sus macros, y nevera
      vs. congelador según `meta.conserva`
    - Cierre: cómo recalienta cada receta (`meta.recalienta`) y botón "Meal prep hecho"
      que paga XP una vez por día (`ACTIONS.mealprepHecho` →
      `xpEntrenoExterno('mealprep', …)`)
  - Metadatos por receta (tiempos, utensilios, conservación, pasos activo/pasivo)
    embebidos en `RECIPE_PREP`, alineados índice a índice con `RECIPES[].prep`
  - **C5d** "La semana comida por comida" (`gestPlanHTML`, id `gestplan`), con toggle
    Semana/Día (`gestVista`/`gestDaySel`). Cada comida es una tarjeta (`.mealrow`,
    `comidaCardHTML`) con jerarquía en tres niveles (segunda pasada de jerarquía
    visual, ver `docs/DESIGN-STANDARDS.md`): 1) nombre + proteína real vs meta en
    `--num` con color de estado; 2) receta asignada (select) + kcal; 3) carbos/grasa
    y la lista de ingredientes, apagados y plegados tras "ver ingredientes"
    (`gestIngTgl`), con el factor de porción como chip aparte. El % del día es un
    control angosto (label corta), nunca compite con las cifras
    - **Color por persona y por estado** (segunda pasada, pedido del dueño "todo es
      muy plano"): cada bloque de persona lleva borde lateral + punto + nombre en su
      color propio (`PERSCOL`, azul Andrés `#5C8DFF` / dorado Cami `#FFC94D`, mismo
      par que ya usan `recPersonRow`/`retoCard`); cada tarjeta de comida lleva fondo
      sutil + borde en el color de su estado (`ESTCOL`, verde/ámbar/rojo fijos,
      independientes de `--mint`/`--gold` porque esas variables cambian de
      significado según el tema del usuario activo y aquí se pintan las dos personas
      a la vez). Día (`t-h2`, Outfit) > Persona (Instrument Sans 700, color de
      persona) > Comida (Instrument Sans 400, `--ink`) quedan en tres tamaños/pesos
      distintos
    - **Aplicar un día a toda la semana** (pedido del dueño, botón "Aplicar este día
      a toda la semana" al final de cada bloque de persona, `ACTIONS.planApplyWeek`):
      copia a los otros 6 días la receta que se ve en cada comida de ese día (manual
      o de rotación, vía `recetaDeComida`/`recetaDeComidaExtra`), sus scoops, y sus
      comidas extra solo si el día de origen tiene alguna. Pide confirmación
      explícita con la lista de lo que va a copiar (no hay deshacer con botón); se
      eligió un botón por día en vez de un interruptor fijo para que no quede
      "prendido" y pise un día sin que el usuario lo note
    - **Comidas extra por día** (pedido del dueño): botones "Agregar comida a este
      día" (Desayuno/Almuerzo/Cena/Snack, `ACTIONS.addExtra`) solo en la vista Día.
      Viven en `S.meal.extras2[key][dl]` (no confundir con `S.meal.extras`, del
      Mercado), con id propio por comida extra que reutiliza `S.meal.plan`/
      `S.meal.scoops` para receta manual/scoop (mismas claves que las comidas
      normales, solo que con ese id en vez de `mN`). Se quitan con `ACTIONS.rmExtra`
      (chip "quitar"). Decisión de macros: la extra SUMA por encima de la meta del
      día (no reparte la de las demás), y si el total del día se pasa de las kcal
      meta se avisa (`sobreKc` en `diaBlock`) solo cuando hay al menos una extra ese
      día, para no encender una alarma nueva en días sin extras (ver comentario largo
      en `extrasDeDia`, coach-afc-v2.html)
    - **Redondeo de ingredientes contables** (`redondeaCantidad`): unidades (huevos,
      bananos, scoops de whey) redondean a medios (1 / 1,5 / 2), no a cuartos, porque
      a cuartos un valor como 1,25 se mostraba como "1,3" (con un decimal) y nadie
      compra 1,3 bananos. Gramos y mililitros siguen igual (pasos de 5/10)

## P · Progreso (`vProgreso`)

- **P1** Selector grande con cabritas: Actividad física / Nutrición (`progGrpSelector`)
- **P10** Metas de fuerza (caja colapsable arriba del Rendimiento, solo grupo
  Actividad física): objetivos tipo "120 kg × 5 en sentadilla". Todo se calcula en
  1RM estimado (Epley, `e1rm`) para comparar metas a N reps contra historial a
  otras reps, y en pantalla se muestra convertido a las reps de la meta: mejor
  marca hoy, barra, escalones y proyección de fecha por regresión
  (`metasCard`, `goalCardHTML`, `goalProy`, `rmAReps`; datos en `S.goals`).
  El formulario pide peso × reps y muestra un caption en vivo con el 1RM
  equivalente y la fecha en que se lograría (`goalw`/`goalr`). Cada meta con 2+
  registros trae su gráfica: historial a las reps de la meta, línea de meta y
  tendencia extendida con el punto "≈ fecha" del cruce (mismo `lineChart`).
  Las gráficas de rango corto (SEM) marcan el eje con letras L M X J V S D en
  vez de fechas; los días proyectados salen atenuados
- **P2** Tarjeta Rendimiento (`rendimientoCard`)
  - P2a Selector de intervalo (SEM/15D/30D/6M/AÑO), esquina superior derecha
  - P2b Número grande + delta del periodo
  - P2c Gráfica con valores en el eje Y y tres estilos: Línea, Barras (por defecto
    en Volumen y Tiempo: son totales por día) y Suave (promedio móvil de 7 con los
    datos crudos en punticos). Chips bajo la gráfica, elección por modo en
    `UI.chartKind` (`lineChart` opción `estilo`)
  - P2d Trío de medidores (cambia según la categoría)
- **P3** Botonera de 6 categorías: General · Peso · Volumen · Tiempo · Fuerza · Pasos
- **P4** Vista Peso: chips Diario/Promedio semanal, registro, historial (`vPeso`)
- **P5** Vista Volumen (tonelaje, logros, series por grupo) (`vVolumen`)
- **P6** Vista Tiempo (duración, frecuencia, historial) (`vTiempo`). En el historial,
  "Editar" además de corregir kg/reps permite QUITAR un ejercicio del día
  (`dayDelEx`) o borrar todos los registros del día con su sesión (`dayDelAll`),
  ambos con confirmación (pedido del dueño tras el import duplicado)
- **P7** Vista Fuerza (por ejercicio, récords) (`vEjercicios`)
  - P7a "Tu nivel de fuerza" (`fzaCard`): compara el 1RM estimado de cada básico
    contra el peso corporal y lo traduce a nivel (Principiante → Élite) con los
    baremos de fuerza relativa, distintos por sexo (`FZA_STD`). Destaca el ejercicio
    más fuerte y el más flojo, dice cuántos kg faltan para el siguiente nivel y
    recomienda priorizar el eslabón débil
- **P8** Vista Pasos (`vPasos`)
- **P9** Nutrición en Progreso: adherencia, kcal, dona de macros, top alimentos (`vNutriStats`)

## MD · Medidas (categoría de Progreso, `vMedidasCuerpo`; también vista propia
`vMedidas` a la que se llega desde PF7)

- **MD1** Aviso de lo que toca hoy: cada grupo tiene su cadencia (peso diario,
  **cintura y cuello cada 8 días**, resto del set cada 15, estructura cada 365). Si
  coinciden varios se funden en un solo formulario (`medEstado`, `medCamposHoy`).
  Se puede medir cuando se quiera con los chips de abajo, no solo el día que toca.
  Para Cami, si el set cae en fase menstrual se SUGIERE aplazar (`medAvisoFase`)
- **MD2** Mapa corporal (`medMapa`): el **model sheet anatómico de la cabra**, en tres
  vistas rotables (`MED_VISTAS`: frente, perfil, espalda) con chips arriba y **swipe**
  (`data-swnav="medvista"` → `ACTIONS.medRotar`). El arte viene del render de Magnific
  vectorizado; las tres figuras se separaron por posición y se normalizaron al mismo alto
  (1460) centradas en 700 de ancho, para que rotar no haga saltar el cuerpo. Vive en
  `MED_ARTE` (~98 KB); las clases `a`..`f` son los grises del original, tintables por CSS.
  Al tocar una zona: un **velo oscurece todo** y una copia del arte recortada por esa zona
  (`<use mask>` + `feColorMatrix` al color del usuario + `feDropShadow`) vuelve a plena luz.
  La máscara lleva degradado en los extremos para que el corte no parezca una caja.
  Las zonas son rectángulos (`MED_ZONAS`) que **recortan el arte**, así que lo que se
  ilumina es el trozo de cuerpo, no un recuadro. Al rotar, una zona que no existe en la
  vista nueva salta a su pareja del otro lado. **Cotas al lado** (`MED_COTAS`) con línea
  guía, valor e **indicador de cambio**: el triángulo apunta según el signo, el color según
  si ese cambio es bueno en esa zona (bajar es bueno en cintura y cadera, subir en el
  resto). Todo tocable y navegable por teclado
- **MD3** Panel de la zona (`medPanelZona`): valor, fecha, delta y sparkline, más
  **medida objetivo** con barra de avance (`medObjetivoDe`), **histórico de hasta 8
  tomas con el peso promedio de ese día al lado** y una **sugerencia por zona**
  (`medSugerenciaZona`). En cintura el objetivo sale de despejar el Navy al % de
  grasa meta (`medCinturaObjetivo`); si esa inversión cae por debajo de 0,40 de
  cintura/estatura se marca imposible y se explica en vez de mostrar un número irreal
  (es lo que pasa con la cadera de Cami). En Cami el pecho no lleva objetivo: es busto
- **MD11** Medidas es el **tercer grupo del selector de Progreso** (`progGrpSelector`),
  al lado de Actividad física y Nutrición: dejó de ser un chip perdido entre los de
  actividad. `progGroup()` devuelve `cuerpo` cuando la sub-vista es `medidas`
- **MD10** "Cada cuánto medirte" (`medCadenciaCard`): las cuatro cadencias con el
  porqué de cada una, cuáles son clave y cuántos días faltan para la próxima
- **MD4** Bloque Navy: % de grasa, masa grasa y magra sobre el promedio de 7 días,
  la fórmula literal con los valores sustituidos y el margen de error (±3-4 puntos).
  Para Cami añade el aviso de que su cadera ancha es estructural e infla el
  resultado, con el cálculo alternativo para que se vea cuánto pesa (`medNavy`)
- **MD5** Proporciones: cintura/estatura (≤0,50) y cintura/cadera (≤0,90 él, ≤0,85
  ella) (`medRatios`); diferencias entre lados desde 1 cm (`medAsimetrias`)
- **MD7** Meta de grasa (`metaGrasaCard`): slider con **tope duro por sexo** (mínimo
  8% él, 18% ella; por defecto 15% y 22%). El tope se aplica también en
  `metaGrasaDe`, así que no se salta con un dato guardado ni escribiéndolo a mano.
  Bajo 20% en mujer sale el aviso de ciclo y densidad ósea. Tabla de rangos por sexo
- **MD8** Meta en dos fases (`metaFases`, `metaCard`): Fase 1 definición hasta tu %
  meta con la masa magra de hoy; Fase 2 recomposición hasta los 89 kg, que no se
  borran. La fecha sale de la tasa real de 4 semanas (o del 0,5%/semana si no hay
  historia) y **siempre con rango de ±3 semanas**. `metaGuardia` avisa si la magra
  cae más de 1 kg sin que baje la grasa, preguntando antes por hidratación
- **MD9** Proporciones (`propObjetivos`, `propCard`): ancla en la muñeca (él,
  McCallum) o en la cadera (ella). Ordena por diferencia relativa, semáforo por
  categoría (nunca rojo por superar un objetivo), ratios de forma con la áurea y
  simetría de Reeves. Sin el ancla no calcula nada parcial
- **MD6** "Qué hacer con esto": lee la tendencia de cintura contra el peso promedio
  y devuelve máximo 3 frases con una acción concreta (`medPlan`)

## FT · Fotos (sección independiente, `vFotos`)

- **FT1** Caja de captura "Tomar hoy" con la cabrita + repetir pose + subir antigua
  - FT1a Botón "Cargar varias": lote de fotos con revisión previa antes de guardar
    (fecha por EXIF, sin fecha se pregunta una por una, choques con foto existente se
    preguntan por foto) (`loteIniciar`, `loteReviewOpen`, `.fbox.lotebox`)
  - FT1b Botón "Deshacer el último lote": visible solo si hay un lote reversible
    (`S.fotoLote`), pide confirmación y restaura byte a byte lo que el lote tocó
    (`loteDeshacer`, IndexedDB `cabritos-fotos` store `loteBak`)
- **FT2** Antes y después: presets 7/30/365 días, primera vs última, comparar 2 a mano.
  La ventana de comparación (`fotoCompare`) tiene desde REV 135 un **deslizador sobre
  la foto**: se arrastra la imagen misma (Pointer Events, dedo o ratón), con línea de
  degradado, halo lateral y manija; la fecha del lado que casi no se ve se atenúa.
  Al abrir hace un barrido corto de bienvenida (se detiene al primer toque; no corre
  con `prefers-reduced-motion`). Accesible por teclado (flechas, Home/End) con
  `role="slider"`. Reemplaza al `input type=range` que estaba debajo de la foto
- **FT3** Galería: filtro por persona + Esta semana / Ver todas (`fotoFill`)

## K · Check-in (vista propia, `vCheckin`)

- **K1** Resumen de la semana que cierra (peso promedio, días, entrenos)
- **K2** Formulario: peso, grasa %, medidas, adherencia, energía, sueño, notas, foto
- **K3** Gráficas de cintura y grasa corporal
- **K4** Tabla de evolución completa

## R · Retos (`vRetos`)

- **R1** Hero del versus con las dos cabritas y el marcador
- **R2** Puntos de la semana y desglose
- **R3** Premios: proponer, votar, reto de la semana/mes/trimestre
- **R4** Vitrina de trofeos y palmarés

## PF · Perfil (se llega tocando el avatar del nav, `vPerfil`)

- **PF1** Hola + nivel + XP
- **PF2** Calcomanías y logros
- **PF3** Composición corporal
- **PF4** Últimas medidas
- **PF5** Tu ciclo (Cami)
- **PF6** Mis trofeos
- **PF7** Accesos (Progreso, Check-in, Fotos, Ajustes)

## M · Más / Ajustes (`vMas`)

- **M1** Recordatorios (incluye el check-in semanal `#rem-checkin`)
- **M2** Salud (iPhone) · pasos + atajo pro
- **M3** Inyección semanal
- **M4** Plan · referencia
- **M5** Buzón de ideas
- **M6** Ciclo · configuración
- **M7** Privacidad · PIN
- **M8** Preferencias (meta de agua, meta de pasos)
- **M9** Nube (Supabase)
- **M10** Datos (respaldos, exportar, borrar)

---
Si una zona cambia de lugar, el código se queda con la zona, no con la posición.
Al agregar cajas nuevas se les asigna el siguiente número libre de su pantalla.

## E8 · Elegir ejercicios por músculo (`vExcat`, botón "Elegir por músculo")

El mismo cuerpo de Medidas, aquí como buscador: `medMapa(z, {accion:'excatZona',
cotas:false})`. Tocar el pecho o el hombro filtra el catálogo a ese grupo, que es como
uno piensa cuando quiere "algo de hombro" y no se acuerda del nombre. `medGrupoEj(zona,
vista)` traduce zona a categoría de `EXCAT`, y **depende de la vista**: en la espalda el
torso alto no es pecho sino dorsales. Respeta el filtro de equipo que ya esté puesto.

## MC · Carga por músculo (Progreso → Medidas → pestaña Carga)

El mismo cuerpo, pintado por volumen de la semana en vez de por medidas.

- **MC1** Mapa de calor (`medMapa` con `calor`): cada zona se pinta del color de su nivel
  de volumen, con la forma de sus músculos. La zona toma el estado del músculo que la
  define en esa vista (`ZONA_MUSC`), así que el torso alto por delante habla del pectoral
  y por detrás del dorsal. Rojo sin trabajo, naranja por debajo del mínimo, verde creciendo,
  amarillo alto, rojo pasado
- **MC2** Selector de periodo: 7, 14 o 28 días (`UI.cargaDias`)
- **MC3** Detalle del músculo tocado: series efectivas, ejercicios que lo trabajaron,
  barra contra MEV/MAV/MRV y consejo concreto (`cargaConsejo`)
- **MC4** "Lo que pide atención": los que están por debajo del mínimo o por encima de lo
  recuperable, con cuántas series faltan o sobran
- **MC5** Ranking de todo el cuerpo con la marca del mínimo en cada barra
- **E9** En la ficha de cada ejercicio (`muscReparto`), el reparto en % con barra apilada:
  "de cada serie, 65% pectoral, 20% deltoide anterior, 15% tríceps"

De dónde salen los números: [CARGA-MUSCULAR.md](CARGA-MUSCULAR.md).

## Elegir ejercicios por músculo, no por categoría

`ejerciciosDe(musculo, equipo)` devuelve los ejercicios que trabajan un músculo **ordenados
de mayor a menor activación**, con el % a la derecha de cada fila. Filtrar por la categoría
del catálogo no servía: tocar el glúteo devolvía "pierna" entera, extensiones de cuádriceps
incluidas. Si la zona tiene varios músculos (el hombro son tres deltoides) se eligen con
chips, y se descartan los que no tienen ningún ejercicio (el cuello).

## Nivel de fuerza · la escalera (P7a)

Cada fila se abre (`UI.fzaOpen`) y muestra:
- **De dónde sale el número**: el día, el peso y las repeticiones de la mejor serie del
  historial, y la cuenta de Epley hecha a la vista
- **El peso de cada categoría** con tu peso corporal, en 1RM y en serie de 5, que es lo que
  uno hace de verdad en el gimnasio
- Qué falta exactamente para el siguiente nivel

Debajo, plegado, **los demás ejercicios que registras**: no tienen baremo de nivel (los
estándares de fuerza relativa solo existen para los básicos) pero sí 1RM y cuánto ha subido.

## Metas · reiniciar el punto de partida

Una meta puede reiniciarse a propósito: bajar el peso para corregir la técnica, volver
después de parar, cambiar de máquina o venir de una lesión (`GOAL_MOTIVOS`). Sin esto la app
leía ese bajón como retroceso y la proyección se iba a la basura, cuando en realidad es el
arranque de una curva nueva. `g.base = {d, rm, w, r, motivo, previoRM}`: `goalHistRM`,
`goalBestRM` y `goalProy` ignoran todo lo anterior a esa fecha, y la marca vieja se guarda y
se muestra para no perderla.

### Los otros ejercicios (P7a, plegado)

Llevan **nivel propio** cuando hay baremo para su patrón (`fzaNivelOtro`), con su escalera
completa al abrir. Se pueden marcar con estrella para **seguirlos de cerca**
(`S.cfg.fzaSigue`): los marcados suben a un bloque propio junto a los principales.

El `<details>` guarda su estado en `UI.fzaOtros`. Sin eso se cerraba en cada render y tocar
un ejercicio de dentro daba un salto de pantalla enorme.

### Peso por lado

`exUnilateral(id)` detecta los ejercicios que se hacen un lado a la vez;
`S.cfg.porLado[id]` guarda si el peso apuntado es de un lado o el total, y `exPesoReal`
lo aplica al tonelaje y al 1RM. La app no lo puede adivinar: 27 kg en un curl con mancuerna
pueden ser 27 o 54 de trabajo real. Se marca desde la ficha del ejercicio o desde la fila
abierta en nivel de fuerza, y donde aparece el peso se ve la etiqueta "por lado".

### De qué ejercicio sale cada estándar

`FZA_MAP` lista los candidatos de cada estándar **en orden de fidelidad** y se usa el primero
que tenga registros. Antes se cogía el que diera más 1RM, y por eso el press banca acababa
saliendo de un press inclinado y el curl de barra de uno en polea, que mueve más peso pero no
es el mismo levantamiento. Los que tienen tabla propia en `FZA_STD2` (inclinado, hack,
rumano, remo con mancuerna) salieron de aquí: se ven en su propia fila con su propio baremo.

Se puede elegir a mano desde la fila abierta (`S.cfg.fzaFuente[estandar] = exId`), con los
candidatos y el 1RM de cada uno a la vista.

## Editar una rutina del plan (E2b)

Las rutinas del plan son constantes: el mismo plan para los dos. Pero uno quiere quitar un
ejercicio que hoy no puede hacer, subir series o meter otro. En vez de duplicar las rutinas,
se guarda una **capa de cambios** por rutina en `S.rutMod[rid] = {quita, sets, reps, extra,
orden}` y `rutAplicarMods` la aplica encima al montar `ROUTINES`. El plan original nunca se
toca, así que **"Volver al plan original"** siempre funciona, y los ejercicios quitados
quedan a la vista para poder devolverlos de un toque.

## Long press

Mantener pulsado sobre una imagen abría el menú del navegador (guardar, copiar, compartir).
En una app eso no tiene sentido. Se desactivó el callout y el arrastre en todo lo tocable, y
el long press sobre la fila de un ejercicio abre su ficha, que es lo que uno quería hacer.

## Peso corporal y lastre

En anillas, dominadas, fondos y flexiones el número que se apunta es el **lastre** (0 si va
a peso limpio) y el peso real de la serie es **el corporal de ese día más el lastre**
(`exPesoCorporal`, `pesoDeDia`, `exPesoReal`). Sin esto una dominada contaba 0 kg y no
aportaba nada ni al tonelaje ni al 1RM.

## Correr en el mapa de carga

Correr también carga las piernas, y dejarlo fuera hacía que el gemelo saliera "sin trabajo"
en una semana de 30 km. Se cuenta en series equivalentes: **10 minutos ≈ 1 serie**, repartida
30% pantorrilla, 25% cuádriceps, 20% isquio, 20% glúteo, 5% abdomen. La equivalencia es
conservadora a propósito: correr es resistencia, no hipertrofia, y no debe tapar la falta de
trabajo con carga.

## A5b · Registro libre de un día (Agenda → día → "Personalizado")

Para cuando lo que hiciste no fue ninguna rutina. Una línea por ejercicio con **series,
peso y reps** (`libreForm`, `UI.libre`), que es lo mínimo para que entre al historial sin
abrir una sesión entera y marcar serie por serie. Al agregar un ejercicio **precarga lo de
la última vez**, que casi siempre es lo mismo o muy parecido, y ofrece los cuatro que más
usas para no tener que buscar.

Guarda en `S.logs` con la fecha del día elegido y registra la sesión como `rid:'libre'`,
así el resumen del día, el tonelaje y las gráficas de fuerza la cuentan igual.

También aparece **en días que ya tienen sesión registrada** ("Agregar más ejercicios de ese
día"): si entrenaste la rutina y además hiciste algo extra, antes no había forma de anotarlo.

### Buscar ejercicio por categorías

En el editor de rutinas y en el registro libre, sin búsqueda escrita se ve el catálogo
**agrupado por grupo muscular** en secciones plegables (`exPickCats`, `exPickRow`), que es
como uno busca cuando no tiene el nombre en la cabeza. Al escribir, pasa a resultados de
texto.

### Peso limpio en anillas y calistenia

En esos ejercicios dejar el kg vacío **no es un dato que falta**: significa peso limpio, sin
lastre. Antes la app exigía escribir un número para poder registrar la serie, que es justo
lo contrario de fácil de llenar. `serieW` / `serieValida` tratan el vacío como 0 cuando
`exPesoCorporal(id)`, el campo muestra **"lastre"** en vez de "kg", y al marcar una serie no
se rellena el peso desde el histórico. Sirve igual en la sesión y en el registro libre.

## MD0 · Las tres cajas de Medidas

Al entrar solo se ven **tres cajas plegadas** en fila (`UI.medBox`, acordeón), en vez de una
pared de secciones: **Meta de grasa · Tu cuerpo · Tu meta**. El aviso de lo que toca hoy
queda siempre arriba porque es lo único accionable desde ahí.

**"Tu forma" (las proporciones) vive dentro de "Tu cuerpo"**: es lo mismo mirado de otra
manera, y tenerlo aparte obligaba a saltar entre cajas para entender un solo número. Esa caja
lleva el mapa, el detalle de la zona, las proporciones, las asimetrías, la cadencia y el
historial: una sola sección.

Cada caja lleva **una cabrita que ya existía** en `assets/cab` (racha, medidas, plan) según
el usuario, más su icono en el rótulo. No hizo falta generar nada: antes de pedir imágenes
nuevas conviene mirar las 106 que ya hay. Los nodos por si se quieren propias están creados
en Magnific (`UI — med_grasa`, `UI — med_cuerpo`, `UI — med_meta`), sin generar.

## De dónde salieron las series (Carga → músculo)

Al abrir un músculo, un desplegable lista **día, ejercicio, series y cuánto aportó cada uno**
con su porcentaje. Un total suelto no dice si esas 6 series salieron de un día o de tres, ni
de qué ejercicios. Los minutos de carrera aparecen como series equivalentes.

## Banner de rutina de anillas

`routineBanner` reconoce sola una rutina de anillas: si la mitad o más de sus ejercicios son
de anillas, el banner es `ring_pullup.jpg` en vez del de push/pull genérico. El nodo del
banner propio (`BAN — rutina_anillas`) está creado en Magnific, sin generar.

### Elegir la tabla con la que se compara (P7a)

Un peso muerto rumano no se juzga con la tabla del convencional, ni una dominada lastrada
con la del jalón: el mismo número significa cosas distintas. `FZA_VARIANTES` lista, por cada
básico, las tablas que tienen sentido, y se elige desde la fila abierta
(`S.cfg.fzaTabla[k]`). Medido: una dominada con 20 kg de lastre pasa de **Avanzado** con la
tabla de jalón a **Intermedio** con la de dominada lastrada, que es el listón correcto.

Baremos nuevos para las variantes: `dominada_lastrada`, `peso_muerto_sumo`, `trap_bar`.

### Metas · qué hacer la próxima sesión

Una gráfica te dice dónde estás, no qué hacer mañana. Cada meta lleva ahora `goalProxima`:
mira la última serie y aplica la regla de progresión (si completaste el tope de repeticiones
sube peso, si no suma una repetición), y dice el peso y las reps concretas de la próxima vez
más cuántas sesiones faltan a ese paso.

**Corregido de paso**: en ejercicios de peso corporal la meta se guarda como lastre pero el
actual se calculaba con el cuerpo sumado, así que una meta de 25 kg de lastre salía cumplida
teniendo 10. Ahora ambos lados se miden igual.

### El detalle de la zona, flotando sobre el mapa

Al tocar una zona sale una **tarjeta sobre el cuerpo** (`medZonaPop`): nombre en el color de
acento, valor grande en blanco, el cambio en verde o rojo según si es bueno en esa zona, y
debajo el objetivo con **cuánto falta y hacia dónde** (▲ verde si hay que subir, ▼ rojo si
hay que bajar). Antes eso vivía en un panel debajo del cuerpo y había que bajar la vista.

Medidas de la tarjeta: **92-149 px sobre un mapa de 354**. La primera versión llevaba también
la sugerencia y medía 237 px, o sea dos tercios del mapa: se salía por abajo y le tapaba la
cara al cabrito. La sugerencia se quedó en el panel de abajo. Las zonas altas se anclan con
`top` y las bajas (cy > 0,58) con `bottom`, que es lo único que evita que se salga del lienzo.
Verificado en las **70 combinaciones** de zona × vista × usuario: cero desbordes.

Ojo con el color: el acento se usa como `rgb(var(--acc-rgb))`, **no** `var(--acc)`, que solo
existe dentro del `<style>` del SVG del mapa. Usarlo fuera deja el fondo transparente.

El **recuadro oscuro** que se veía alrededor del cuerpo era un `<rect>` que cubría todo el
lienzo para atenuar el fondo. Se quitó: ahora la atenuación es la opacidad del propio arte.

## Ficha de cada ejercicio (`EJ_DATA`)

Los 301 del catálogo clasificados uno por uno: patrón de movimiento, si es de peso corporal
(el kg que se apunta es lastre), si se hace un lado a la vez y con qué tabla de fuerza se
compara. Antes todo eso se deducía del nombre con expresiones regulares y fallaba en los
casos raros: el preacher curl se quedaba sin patrón, el dragon flag contaba como pecho y un
salto al cajón se juzgaba con la tabla de sentadilla. Las reglas por nombre siguen ahí como
**respaldo** para lo que se importe de Strong y no esté en el catálogo.

Correcciones aplicadas sobre lo que devolvió la clasificación automática: preacher curl sin
patrón, fondo en banco como press, dragon flag como pecho, back lever como jalón, muscle up
sin patrón, remo al mentón como remo horizontal, curl de muñeca como bíceps, y las asistidas
y los saltos comparándose con tablas que no les corresponden.

### Isla flotante en el mapa de carga

La misma tarjeta de Medidas, aquí con las **series efectivas** del músculo tocado: cuántas
recibió, en qué nivel está, cuánto le falta para el mínimo y de qué ejercicios salieron. Si
la zona tiene varios músculos (el hombro son tres deltoides) se cambian con chips dentro de
la propia isla.

Y las filas del resumen de abajo **ahora son tocables** (`cargaFila`): llevan a ese músculo en
el mapa y hacen scroll hasta él. Antes no hacían nada, que era justo lo que se esperaba de
ellas al verlas listadas.

## Fuerza, la tercera lectura del mismo mapa (Medidas → Fuerza)

El nivel de fuerza salió de la sub-vista de un ejercicio en Progreso y pasó a ser la tercera
pestaña de Medidas, al lado de Medidas y Carga. Son las tres lecturas del mismo cuerpo:
**cuánto mides, cuánto trabajas y cuánto levantas**.

Al tocar una zona salen **todos sus músculos con su nivel**, del más flojo al más fuerte, y
cada uno se amplía para ver los ejercicios que lo cargan con su porcentaje, la escalera y el
selector de fuente. Tocar el brazo da bíceps, tríceps y antebrazo por separado; el muslo da
cuádriceps, isquios y glúteo. Antes devolvía ejercicios sueltos y no se sabía si el brazo iba
flojo de bíceps o de tríceps.

Para fuerza la zona agrupa **la región entera**, no la cara que se ve (`ZONA_MUSC_FZA`): al
tocar el muslo uno quiere los isquios aunque estén detrás. En el mapa de carga la distinción
frente/espalda sí tiene sentido, por eso el mapeo es aparte.

El cuerpo se pinta por el **músculo más flojo** de cada zona, que es el que limita. La isla
flotante dice cuál es y su nivel.

**El selector de fuente ya ofrece todos los candidatos**, no solo los que tienen registros:
los que no tienen salen en gris con un guion, y al elegirlos el nivel se calcula en cuanto
entrenes uno. Antes solo aparecía si ya habías registrado dos variantes, así que en la
práctica no aparecía casi nunca.

`exVariante` da el nombre distintivo: `shortEx` corta en el paréntesis y dejaba siete
candidatos llamados todos "Bench Press", que es justo lo que hay que diferenciar.

## El Cruce (Medidas → Cruce) · cuarta pestaña

Las otras tres dicen dónde estás. Esta busca **dónde se contradicen**, que es lo único que
ninguna da por separado. Mira sobre **28 días**, no una semana: una semana suelta no
distingue entre un músculo abandonado y una semana rara.

`cruceDatos()` junta por músculo las tres capas (series efectivas por semana, nivel del mejor
básico que lo carga al 25% o más, y la tendencia de la medida de su zona) y saca un
diagnóstico:

| Situación | Qué dice |
|---|---|
| Fuerte + poco volumen | *"Fuerte pero abandonado"* · la fuerza aguanta un tiempo sin volumen, el tamaño no |
| Mucho volumen + medida estancada | *"Mucho trabajo, cero cambio"* · más volumen no es la respuesta, mira la comida |
| Flojo + poco volumen | *"Aquí está la ganancia fácil"* · ponlo de primero en la sesión |
| Medida creciendo + volumen ok | *"Va bien, no lo toques"* |

Los que están en orden se pliegan aparte para no hacer ruido.

## Lado contra lado (Fuerza)

`fzaAsimetria` compara las medidas de ambos lados. Hasta 1 cm no significa nada; desde 1,5 la
recomendación es empezar por el lado flojo y **igualar repeticiones, no peso**.

## Qué meter para subir de nivel (Fuerza → zona)

`fzaQueMeter` propone los tres ejercicios que más cargan esa zona, con su porcentaje, sacados
del mismo reparto EMG del mapa de carga y descartando los que ya haces. Cierra el círculo
entre "estoy flojo aquí" y "haz esto".

## Las cuatro capas viven en el mapa

El selector de capa (`medCapaBar`) son cuatro chips pequeños encima del cuerpo, no una fila
de pestañas aparte: **Medidas · Carga · Fuerza · Cruce**. Vive fuera de `medMapa` a
propósito, porque si una capa no tiene datos y la barra estuviera dentro del mapa te quedabas
encerrado en ella. En pantallas de menos de 360 px se queda solo el icono.

**Zoom a la zona** (Fuerza): al elegir una zona el `viewBox` se recorta alrededor con margen,
cuadrado a la proporción del lienzo para que el cuerpo no se deforme, con un botón "Ver el
cuerpo" para volver.

**Animaciones**: las zonas de color entran con un fundido corto, el contorno del músculo
seleccionado se dibuja desde un trazo grueso, la isla entra con un desplazamiento y escala, y
las zonas tocables responden al `:active`. Todas con la misma curva `cubic-bezier(.32,.72,0,1)`
que ya usa el resto de la app.

**El cruce también se ve en el mapa**: cada zona toma el estado de su músculo más urgente
(rojo pide atención, naranja ganancia fácil, verde en orden) y al tocarla salen solo las
tarjetas de esa zona.

### El peso por lado se ofrece siempre

`exUnilateral` adivinaba por el nombre si un ejercicio se hace a un lado, y con eso decidía si
mostrar el toggle. Bloqueaba casos reales: un curl en polea se puede hacer a un brazo y solo
el dueño lo sabe. Donde hay sitio (la escalera de fuerza, el registro libre, la ficha del
ejercicio) el toggle se ofrece **siempre**; `exUnilateral` se queda solo para destacarlo donde
es lo habitual.

### Elegir un ejercicio que aún no has entrenado

El selector guardaba la elección pero `fzaTabla` la ignoraba si ese ejercicio **no tenía
registros**, y el chip se marcaba según el que se usaba, no según el elegido. Efecto: tocabas
y no pasaba nada visible, ni siquiera un cambio de estado. Desde fuera, "no me deja cambiar el
ejercicio".

Ahora la elección se respeta siempre en pantalla y, si aún no hay series suyas, se dice con
qué se está midiendo mientras tanto: *"Elegiste Bench Press · Barbell, pero todavía no tienes
series suyas. Mientras tanto el nivel se calcula con Bench Press · barra; en cuanto lo
entrenes, cambia solo."*

Sobre qué registro se usa: `fzaMejor1RM` recorre **todo el historial** y se queda con el 1RM
más alto, no con el último. Verificado con tres series del mismo ejercicio (100×5 → 116,7 ·
180×5 → 210 · 150×3 → 165): toma los 210. La escalera lo dice en pantalla.

