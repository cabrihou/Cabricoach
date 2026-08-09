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
  - I2b Pasos · I2c Agua · I2d Check-in · I2e Foto del día
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
  cintura y cuello cada 14 días, set completo cada 28, estatura cada 365). Si
  coinciden varios se funden en un solo formulario (`medEstado`, `medCamposHoy`).
  Se puede medir cuando se quiera con los chips de abajo, no solo el día que toca.
  Para Cami, si el set mensual cae en fase menstrual se SUGIERE aplazar (`medAvisoFase`)
- **MD2** Mapa corporal: cabrito bípedo en SVG con 12 zonas tocables por `<path>`
  (`medMapa`). Al elegir una, el resto baja a 0,35 de opacidad y la activa toma el
  color del usuario. Navegable por teclado, cada zona con `aria-label`
- **MD3** Panel de la zona: valor, fecha, delta contra la medición anterior y
  sparkline de las últimas 6 (`medPanelZona`, `medSpark`). El delta solo se colorea
  en cintura y cadera: en brazo o pecho subir no es malo
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
