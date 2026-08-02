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
- **I3** Caja rotativa "Para ti": pendiente de hoy, coach del día, versículos, datos, hitos (`homeRotator`, `rotcard`)
  - I3a Cápsula "Tu próximo entreno": recomendación según planeación del día antes, se abre como ventana flotante con insights de la jornada (`proxEntreno`, `proxBoxOpen`, `ACTIONS.proxBox`)
- **I4** Nutrición del día (`nutriDay`)
  - I4a Anillo de proteína + mensaje del día
  - I4b Caja "Con qué cerrar" (sugerencias sueltas y combinaciones) (`sugBox`)
  - I4c Fila de macros: Carbo / Grasa / Proteína (`.macrow`)
  - I4d Franjas Mañana/Tarde/Noche + buscador de loggeo (`nlogPanel`)
  - I4e Barras de proteína de los últimos 7 días (`.pweek`)
- **I5** Tarjeta del ciclo (solo Cami) (`cyccard`)

## E · Entrenar (`vEntrenar`)

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
- **E3** Importar entreno pegando texto (Strong, etc.) (`impTgl`)
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
  - A4a Panel de nutrición completo de ese día: mismo panel que Inicio (I4), anillo
    de proteína, franjas Mañana/Tarde/Noche con buscador y loggeo real, "con qué
    cerrar" y semana de proteína, pero con textos en pasado y sin autoabrir
    sugerencias por hora (`nutriDay(sel)`, contexto de fecha en `nutriT()`/
    `UI.nutriDate`, fijado por `calEditor()`)
  - A4b Chips "Comidas del plan" para marcar sin detallar (no duplican macro si esa
    franja ya tiene loggeo detallado, ver `eatenOn`) (`mealAt`)
  - A4c Agua, peso, inyección y foto de ese día
- **A5** Modo foto: las tarjetas de los días se giran y muestran la foto (`calFotoTgl`, `.flip3d`)

## C · Comida (`vComida`, sub-pestañas Recetas / Mercado / Plan día)

- **C1** Selector de sub-pestañas (Recetas · Mercado · Plan día)
- **C2** Recetas (`vRecetas`)
  - C2a CTA "Ármame la semana" + banner de rotación activa (abre C2g)
  - C2b Buscador de recetas
  - C2c Rejilla de categorías (res, pollo, pescado, desayunos, etc.)
  - C2d Tarjeta de receta abierta: ingredientes, costos, sección "Preparación" (`recCard`)
  - C2e Caja "Sugerir receta" + lista "Ideas de recetas" (`vIdeasReceta`)
  - C2f Proteína de la semana
  - C2g Formulario "Arma la semana": proteínas, porciones por persona, desayuno,
    presupuesto/aprovechar lo de casa, tiempo de cocina, antojos y descartes; genera con
    `autoWeekGen()` y muestra un resumen antes de ir al mercado (`weekFormOpen`,
    `weekFormHTML`, `weekSummaryHTML`, preferencias en `S.meal.prefs`)
- **C3** Mercado (`vLista`)
  - C3a Toggle Ambos/Andrés/Cami + periodo (semanal/quincenal/mensual)
  - C3b Barra de suma parcial: $ marcado vs total
  - C3c Checklist agrupado: Proteínas / Vegetales y frutas / Despensa (`mktCat`)
  - C3d Caja "Precios y facturas": registrar precio, foto, pegar texto de factura, histórico (`vFacturas`)
- **C4** Plan día (`vPlanDia`)
  - C4a Números del día
  - C4b "¿Qué comiste?" registro libre (`freeTxt`)
  - C4c Tabla "Comidas y macros" + aviso de comidas vencidas (`mealStatus`)
  - C4d Calculadora "¿Cuánta proteína tiene?"
  - C4e Guía del meal prep del domingo

## P · Progreso (`vProgreso`)

- **P1** Selector grande con cabritas: Actividad física / Nutrición (`progGrpSelector`)
- **P2** Tarjeta Rendimiento (`rendimientoCard`)
  - P2a Selector de intervalo (SEM/15D/30D/6M/AÑO), esquina superior derecha
  - P2b Número grande + delta del periodo
  - P2c Gráfica de línea
  - P2d Trío de medidores (cambia según la categoría)
- **P3** Botonera de 6 categorías: General · Peso · Volumen · Tiempo · Fuerza · Pasos
- **P4** Vista Peso: chips Diario/Promedio semanal, registro, historial (`vPeso`)
- **P5** Vista Volumen (tonelaje, logros, series por grupo) (`vVolumen`)
- **P6** Vista Tiempo (duración, frecuencia, historial) (`vTiempo`)
- **P7** Vista Fuerza (por ejercicio, récords) (`vEjercicios`)
- **P8** Vista Pasos (`vPasos`)
- **P9** Nutrición en Progreso: adherencia, kcal, dona de macros, top alimentos (`vNutriStats`)

## FT · Fotos (sección independiente, `vFotos`)

- **FT1** Caja de captura "Tomar hoy" con la cabrita + repetir pose + subir antigua
  - FT1a Botón "Cargar varias": lote de fotos con revisión previa antes de guardar
    (fecha por EXIF, sin fecha se pregunta una por una, choques con foto existente se
    preguntan por foto) (`loteIniciar`, `loteReviewOpen`, `.fbox.lotebox`)
  - FT1b Botón "Deshacer el último lote": visible solo si hay un lote reversible
    (`S.fotoLote`), pide confirmación y restaura byte a byte lo que el lote tocó
    (`loteDeshacer`, IndexedDB `cabritos-fotos` store `loteBak`)
- **FT2** Antes y después: presets 7/30/365 días, primera vs última, comparar 2 a mano
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
