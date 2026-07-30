# Proyecto: Coach de Nutrición y Entrenamiento — Andrés Felipe Castro

> Documento de especificación para continuar el desarrollo en Claude Code.
> Contiene: perfil del usuario, plan nutricional, programa de entrenamiento, lógica de negocio y requerimientos de la aplicación.
> Existe un prototipo funcional en React (`coach-afc.jsx`) que sirve como punto de partida del frontend.

---

## 1. Perfil del usuario

- **Nombre:** Andrés Felipe Castro Casas
- **Edad:** 29 años · **Sexo:** Masculino
- **Ubicación:** Colombia (Bogotá) — precios, comida y unidades en contexto colombiano (COP, kg, gramos)
- **Idioma de la app:** Español

### Bioimpedancia (Smart Fit Body — 16/07/2026)

| Métrica | Valor | Rango ideal |
|---|---|---|
| Peso | 94.4 kg | 58–78 |
| IMC | 29.79 | 18–24 |
| Grasa corporal | 18.53 % | 8–19 |
| Masa libre de grasa | 71.45 kg | 56–64 |
| Masa muscular esquelética | 45.31 kg | — |
| Agua | 52.3 L | 47–61 |
| Grasa visceral | 7.0 | 1–9 |
| Metabolismo basal | 2057 kcal | — |

**Segmentario (cambio vs. medición anterior):**
- Tronco: +0.78 kg músculo / −0.84 kg grasa (recomposición positiva)
- Piernas: −0.65 kg músculo / +0.63 kg grasa entre ambas → señal de tren inferior desatendido; motiva frecuencia 2×/semana de pierna en el nuevo plan.

**Interpretación:** perfil musculoso con colchón moderado de grasa (~17.5 kg). El IMC alto es engañoso por la masa magra.

### Contexto farmacológico (relevante para la lógica de la app)
- Usa **retatrutida 1 mg/semana** (dosis inicial conservadora), primera inyección 15/07/2026.
- Implicaciones: supresión de apetito → el riesgo NO es comer de más sino comer de menos; prioridad absoluta = proteína y entrenamiento de fuerza para preservar músculo. Recordatorios de hidratación son útiles.
- La app NO da consejo médico. Si hay señales de problema (náuseas severas, mareo), sugerir consultar médico.

---

## 2. Meta

- **Objetivo:** corte 94.4 → **89–90 kg** (usamos 89.5 kg como meta en la app)
- **Fecha límite:** 27 de agosto de 2026 (cumpleaños) → ~6 semanas desde el 15/07
- **Ritmo:** 0.75–0.9 kg/semana (~0.8–1 % del peso corporal). Agresivo pero viable.
- **Grasa corporal esperada al llegar:** ~14.5–15.5 % (asumiendo 80 % grasa / 20 % magro de lo perdido)
- **Regla de éxito del corte:** si las cargas en el gym se mantienen, se está preservando músculo. Si caen 2 semanas seguidas en varios ejercicios → alerta y revisar comida/sueño.

---

## 3. Nutrición

### Números diarios
- **TDEE estimado:** 2900–3100 kcal (MB 2057 × actividad con 5-6 días de entreno)
- **Objetivo calórico:** ~2200 kcal (piso — con retatrutida el riesgo es quedarse corto, no pasarse)
- **Macros:** **195 g proteína · 75 g grasa · 180 g carbohidrato**
- Estructura: **3 comidas** (usuario prefiere pocas comidas; 2 comidas no alcanzan los 195 g de proteína con apetito suprimido)
- Regla en días difíciles: **la proteína primero** — recortar arroz/grasa antes que la proteína.

### Estructura del día
1. **Desayuno — Avena trasnochada:** 60 g avena + 200 g yogur griego + 1.5 scoop whey (45 g) + 150 ml leche + 100 g banano + 15 g mantequilla de maní → ~68 g prot, ~620 kcal
2. **Almuerzo (tupper del meal prep):** ~180 g proteína guisada + 250 g arroz cocido + 180 g fríjol cocido + verduras → ~55 g prot, ~750 kcal
3. **Cena:** ~160 g proteína + arepa/papa + 80 g aguacate (+2 huevos si falta proteína) → ~50–60 g prot
- Carne asada ocasional (punta de anca/lomo 250–300 g) reemplaza la cena 1–2×/semana sin alterar el plan.

### Meal prep (domingo, ~2 h, rinde 5 días)

| Preparación | Cantidad cruda | Rinde |
|---|---|---|
| Carne molida magra guisada | 900 g | 5 × ~180 g |
| Pollo desmechado | 800 g pechuga | 5 × ~160 g |
| Arroz | 500 g crudo | 5 × ~250 g cocido |
| Fríjol o lenteja | 400 g crudo | 5 × ~180 g cocido |
| Verduras asadas | 1 kg | 5 porciones |
| Huevos duros | 10 unid. | snacks |

Tips operativos: pesar al porcionar (no al comer), tuppers de vidrio iguales, congelar porciones de jueves/viernes si el prep es de 6 días. Guisados aguantan 4–5 días en nevera.

### Catálogo de proteínas (selector en la app — 3 opciones por categoría)
- **Res:** carne molida magra · lomo en tiras · punta de anca
- **Pollo:** pechuga entera · muslos deshuesados · pollo desmechado
- **Alternativas:** lomo de cerdo · tilapia/pescado · base de huevo

### Recetas (con ingredientes por porción, crudo)

| Receta | Proteína | Prot/porción | Ingredientes por porción |
|---|---|---|---|
| Boloñesa colombiana | Carne molida | ~40 g | carne 180 g, tomate 80 g, cebolla larga 30 g, arroz 100 g, fríjol 80 g, verduras 200 g |
| Chili con fríjol | Carne molida | ~42 g | carne 180 g, fríjol 120 g, tomate 80 g, pimentón 50 g, arroz 100 g |
| Lomo salteado | Lomo de res | ~40 g | lomo 180 g, pimentón 60 g, cebolla 40 g, arroz 100 g, verduras 150 g |
| Punta de anca asada | Punta de anca | ~50 g | punta 250 g, papa criolla 150 g, ensalada 150 g |
| Pollo desmechado guisado | Pechuga | ~38 g | pechuga 160 g, tomate 80 g, cebolla larga 30 g, arroz 100 g, aguacate 80 g |
| Pollo al curry ligero | Pechuga | ~38 g | pechuga 160 g, leche coco light 60 ml, arroz 100 g, verduras 200 g |
| Tinga de pollo | Pechuga | ~38 g | pechuga 160 g, tomate 100 g, cebolla 40 g, chipotle 10 g, 2 arepas |
| Muslos al horno | Muslos | ~36 g | muslos 200 g, papa 200 g, verduras 200 g |

Rotación sugerida: cada semana 1 receta de res + 1 de pollo; variar la salsa/preparación para evitar monotonía.

### Básicos semanales fijos (desayuno + snacks, 7 días)
Avena 420 g · yogur griego 1.4 kg · whey 315 g · banano 700 g · mantequilla de maní 105 g · huevos 12 · aguacate 400 g · leche 1 L

### Presupuesto de referencia (COP, julio 2026)
- Dieta completa: **$240.000–280.000/semana** (~$1.0–1.15 M/mes)
- Versión optimizada (menos whey y más pollo, yogur natural en vez de griego, pollo de plaza): **$180.000–200.000/semana**
- Precios base usados (por kg salvo indicación): carne molida 22.000 · lomo res 32.000 · punta de anca 38.000 · pechuga 17.000 · muslos 12.000 · arroz 4.500 · fríjol 8.000 · tomate 4.000 · cebolla 3.500 · pimentón 6.000 · papa 3.000 · papa criolla 6.000 · avena 8.000 · yogur griego 22.000 · whey 220.000 · banano 3.500 · mant. maní 40.000 · aguacate 9.000 · huevo 700/unid · leche 4.500/L · verduras mixtas 5.000 · chipotle 30.000 · arepa 800/unid
- Marcar siempre como "estimado / referencia".

---

## 4. Entrenamiento

### Estructura semanal — PPL × 2 (6 días, domingo libre)

| Día | Rutina | Foco |
|---|---|---|
| Lunes | Push A | Pesado (5–8 reps) |
| Martes | Pull A | Pesado |
| Miércoles | Legs A | Quad dominante |
| Jueves | Push B | Moderado (8–12+ reps) |
| Viernes | Pull B | Moderado |
| Sábado | Legs B | Femoral/glúteo dominante |

- **Cardio:** caminadora en casa, **8.000–10.000 pasos/día todos los días**. Si falta energía, se recorta el paseo, nunca la pesa. NO reemplazar la 2.ª pierna por cardio (la bioimpedancia mostró pérdida muscular en piernas).
- **Calentamiento:** 5 min caminadora + 2 series de aproximación en el 1er ejercicio (50 % × 8, 75 % × 4).
- **Intensidad:** RIR 1–2 (terminar pudiendo hacer 1–2 reps más). Semanas 5–6: RIR 0–1 en últimas series.

### Rutinas completas (series × reps · descanso · incremento de progresión)

**PUSH A (pesado):**
| Ejercicio | S×R | Descanso | Incremento |
|---|---|---|---|
| Bench Press (barra) | 3 × 5–6 | 3 min | +2.5 kg |
| Shoulder Press (plate loaded) | 3 × 6–8 | 2.5 min | +2.5 kg |
| Incline Bench (mancuerna) | 3 × 8–10 | 2 min | +2.5 kg |
| Lateral Raise (mancuerna) | 3 × 10–12 | 90 s | +1 kg |
| Skullcrusher | 3 × 8–10 | 90 s | +2.5 kg |

**PULL A (pesado):**
| Ejercicio | S×R | Descanso | Incremento |
|---|---|---|---|
| Bent Over Row (barra) | 3 × 6–8 | 3 min | +2.5 kg |
| Pull Up (lastrada) | 3 × 6–8 | 2.5 min | +2.5 kg |
| Lat Pulldown cerrado | 3 × 10–12 | 2 min | +2.5 kg |
| Preacher Curl | 3 × 8–10 | 90 s | +1 kg |
| Reverse Fly (máquina) | 3 × 12–15 | 60 s | +2.5 kg |

**LEGS A (quad — compuestos primero):**
| Ejercicio | S×R | Descanso | Incremento |
|---|---|---|---|
| Hack Squat | 3 × 6–8 | 3 min | +5 kg |
| Leg Press | 3 × 8–10 | 2.5 min | +5 kg |
| Leg Extension | 3 × 12–15 | 90 s | +2.5 kg |
| Seated Leg Curl | 3 × 10–12 | 90 s | +2.5 kg |
| Pantorrilla de pie | 3 × 12–15 | 60 s | +2.5 kg |

**PUSH B (moderado):**
| Ejercicio | S×R | Descanso | Incremento |
|---|---|---|---|
| Chest Dip | 3 × 8–10 | 2 min | +2.5 kg |
| Incline Chest Press (máquina) | 3 × 10–12 | 2 min | +2.5 kg |
| Overhead Press (mancuerna) | 3 × 8–10 | 2 min | +2.5 kg |
| Chest Fly | 3 × 12–15 | 90 s | +2.5 kg |
| Lateral Raise (cable) | 3 × 12–15 | 60 s | +1 kg |
| Triceps Extension (cable) | 3 × 10–12 | 90 s | +2.5 kg |

**PULL B (moderado):**
| Ejercicio | S×R | Descanso | Incremento |
|---|---|---|---|
| Pull Up | 3 × 8–10 | 2 min | +2.5 kg |
| Row Cable Unilateral | 3 × 10–12/lado | 90 s | +2.5 kg |
| Lat Pulldown abierto | 3 × 10–12 | 2 min | +2.5 kg |
| Hammer Curl | 3 × 10–12 | 90 s | +1 kg |
| Curl bíceps (cable) | 2 × 12–15 | 60 s | +1 kg |
| Face Pull | 3 × 15 | 60 s | +2.5 kg |

**LEGS B (femoral/glúteo):**
| Ejercicio | S×R | Descanso | Incremento |
|---|---|---|---|
| Peso Muerto Rumano | 3 × 6–8 | 3 min | +5 kg |
| Hip Thrust (barra) | 3 × 8–10 | 2.5 min | +5 kg |
| Seated Leg Curl | 3 × 10–12 | 90 s | +2.5 kg |
| Hip Adductor | 2 × 12–15 | 60 s | +2.5 kg |
| Zancadas / Ext. ligera | 2 × 12–15 | 90 s | +2.5 kg |
| Pantorrilla sentado | 3 × 15 | 60 s | +2.5 kg |

### Periodización (6 semanas)
- **Semanas 1–3:** progresión de carga a RPE 7–8. Regla: al llegar al tope del rango de reps en TODAS las series → subir peso (incremento de la tabla) la siguiente semana.
- **Semana 4 — descarga:** mismos pesos de la semana 3, pero 2 series por ejercicio (coincide con posible subida de dosis del fármaco).
- **Semanas 5–6:** empuje final, RIR 0–1 en las últimas series.

### Contexto de la rutina anterior del usuario (referencia)
Usaba app tipo Strong/Hevy con plantillas: iPush/iPush 2.0, iPull 2.0, iQuads. Problemas detectados y corregidos en el nuevo plan: pierna 1×/semana (vs. torso 2–3×), compuestos al final de la sesión de pierna, muchos ejercicios de solo 2 series, bíceps y densidad de espalda algo bajos. Volumen previo por grupo: pecho 6, tríceps 4–6, delt lateral 4, quads 7, femoral 6, glúteo 5, bíceps 4.

---

## 5. Seguimiento (lógica de check-ins)

- **Check-in semanal:** peso promedio de la semana, medidas (cintura, cadera), adherencia (0–100 %), energía, sueño, sensaciones de entrenamiento.
- Ajustar solo con **tendencia de 2–3 semanas**, no con un dato: calorías ±5–10 %, o volumen de entrenamiento.
- **Revisión de bloque cada 4–6 semanas:** progreso vs. meta, qué mantener, qué cambiar.
- Registrar evolución en tabla acumulada: fecha, peso, medidas, adherencia, ajustes hechos.
- Pesaje: mismas condiciones siempre (mañana, en ayunas); mirar tendencia, no dato diario.

---

## 6. La aplicación — requerimientos

### Visión
App web instalable (PWA) de coach personal: entrenamiento + nutrición + tracking, con inteligencia para sugerir progresiones y generar listas de mercado. Usuario inicial: Andrés. Futuro: segunda usuaria (esposa) con sus propios macros.

### Funcionalidades confirmadas por el usuario
1. **Rutinas integradas y usables durante el entrenamiento** (modo sesión en el gym).
2. **Cronómetro de descanso** que arranca al marcar una serie como hecha (duración según el ejercicio).
3. **Registro de cargas por serie** (kg × reps), con precarga del último peso usado.
4. **"Autoaprendizaje" de progresión:** con los pesos registrados, la app calcula qué debería levantar la siguiente semana (regla: todas las series al tope del rango → sube el incremento definido).
5. **Alertas:** estancamiento/regresión (cargas cayendo 2 sesiones seguidas → alerta de revisar comida/sueño).
6. **Selector de proteína semanal:** 3 sugerencias por tipo (res/pollo/alternativas) + recetas compatibles.
7. **Lista de mercado generada automáticamente** a partir de las recetas elegidas y sus porciones, con:
   - Períodos: **semanal / quincenal / mensual** (multiplicadores ×1 / ×2 / ×4)
   - **Checklist** para marcar comprado / pendiente (persistente)
   - Costo estimado por ítem y total (COP)
   - Toggle para incluir/excluir los básicos del desayuno
8. **Tracker de peso corporal** con gráfica de tendencia hacia la meta (línea en 89.5 kg).
9. **Dashboard:** progreso hacia la meta, rutina del día, macros objetivo, sesiones registradas.
10. Futuro: check-in semanal guiado (formulario), tabla acumulada de evolución, fotos de progreso, multiusuario.

### Arquitectura recomendada
- **Frontend:** React / Next.js como PWA (instalable en el celular, offline para cronómetro y registro en el gym).
- **Backend + DB:** Supabase (Postgres, auth, API incluidos; plan gratuito suficiente).
- **Hosting:** Vercel o Netlify.
- **IA (Nivel 2):** llamadas a la API de Claude desde el backend para: sugerencias de progresión más contextuales, recetas nuevas según lo que haya en la nevera respetando macros, y respuestas tipo "el lomo está caro esta semana, ¿qué me sugieres?". El 80 % de la app es lógica programada (Nivel 1) — rápida y sin costo; la IA se usa quirúrgicamente.
- **Costo objetivo:** $0–5 USD/mes + consumo de API (centavos para 1 usuario).

### Modelo de datos sugerido
- `users` (id, nombre, macros objetivo, peso meta, fecha meta)
- `exercises` (id, nombre, grupo muscular, incremento, descanso)
- `routines` (id, nombre, tag, día) + `routine_exercises` (orden, sets, rep_min, rep_max)
- `workout_sessions` (id, user, routine, fecha) + `set_logs` (session, exercise, set_n, kg, reps)
- `body_weights` (user, fecha, kg)
- `checkins` (user, fecha, peso_prom, cintura, cadera, adherencia, energía, sueño, notas, ajustes)
- `recipes` (id, nombre, categoría, proteína, prot_g) + `recipe_ingredients` (nombre, qty, unidad, costo_base)
- `grocery_lists` (user, período, fecha) + `grocery_items` (nombre, qty, unidad, costo_est, comprado bool)

### Prototipo v1 (retirado como referencia visual)
`coach-afc.jsx` — React de un solo archivo, funcional, con: 4 tabs (Inicio, Entrenar, Comida, Progreso), las 6 rutinas cargadas, cronómetro de descanso, registro y precarga de cargas, sugerencia de progresión y alerta de estancamiento, selector de recetas con porciones, lista de mercado agregada con períodos, checklist y costos, tracker de peso con SVG. Persistencia con `window.storage` (API key-value del entorno de artefactos de Claude). Diseño: dark (#0F1216), acento ámbar (#F2A33C). El usuario lo rechazó visualmente ("se siente IA"); queda solo como referencia de lógica de negocio.

### Prototipo v2 — REV 2.0 (15/07/2026, vigente)
`coach-afc-v2.html` — HTML autocontenido (vanilla JS, fuentes embebidas como data-URI, funciona offline y con `file://`). Preview: `python3 -m http.server 8091` en `SandyApp/` → `http://localhost:8091/coach-afc-v2.html`. Modo demo con datos de muestra sin persistir: `?demo=1`; deep-links `?tab=&sub=&rid=` para desarrollo.

**Sistema de diseño — REV 3.0 "Night Gym" (16/07/2026, vigente).** Andy rechazó el look "Swiss Industrial Print" de la REV 2 ("se ve muy IA") y entregó referentes de apps fitness dark (teal sobre negro, gradientes, tarjetas redondeadas, fotografía real). El estándar completo y su checklist de aceptación viven en `DESIGN-STANDARDS.md` (leerlo antes de tocar UI). Resumen: fondo `#0B0D0F`, tarjetas `#15181C` radio 20px, acento único azul `#5C8DFF` (REV 3.1, 16/07: glow radial en tarjetas clave, número héroe en gradiente, slider con perilla, stats divididas por hairlines; Comida rediseñada con badges de categoría y línea mono de macros) con gradiente `--grad`, rojo `#FF5257` solo semántico (alerta/meta/récord), Archivo 800 sentence case + IBM Plex Mono para datos, topbar/nav de vidrio (backdrop-blur), anillo de progreso con gradiente en Inicio, week strip L–D, tarjetas con fotografía real de stock (Freepik free, NO IA, en `assets/stock/`, embebidas como data-URI: push/pull/legs/rest). El look REV 2 quedó respaldado en `coach-afc-v2.backup-rev2.html`. Gráficas SVG con serie azul + glow, meta en rojo discontinuo.

**REV 3.2 (16/07/2026):** horario movible (`S.sched`, selector de día por rutina en Calendario), registro manual retroactivo por día (`S.acts`: gym/pádel/cardio/descanso + pasos/proteína/agua/peso de cualquier fecha, todo entra a racha/adherencia/gráficas), calendario mensual en Entrenar (celdas con estado y editor de día; el week strip de Inicio enlaza ahí), iconos de comida por categoría, y miniaturas nuevas: set generado en Magnific (flux-dev, 50 créditos) estilo bodegón navy rim-light sin personas (`assets/stock/gen-*-web.jpg`), decisión estética aprobada por Andy en vez del stock genérico.

**REV 3.3 (16/07/2026):** firma de iconografía (punto de acento azul en cada icono, `class="acc"`), tanque de agua animado con ola en Inicio y calendario, shimmer/glow en barra de pasos, count-up de números héroe, llama de racha animada, pulso del anillo al cumplir el día, inyección registrable desde el editor de día del calendario (anillo hueco azul como marcador en la celda), y 3 imágenes de comida del set navy generado (tuppers/shaker/mercado, +30 créditos Magnific) como cabeceras de Plan día, Recetas y Mercado.

**REV 3.4 (16/07/2026):** modo foco en la sesión de entreno (un ejercicio a la vez con "EJERCICIO X DE N", stepper de chips para saltar a cualquiera, ANTERIOR/SIGUIENTE, toggle VER LISTA, y auto-avance al completar las series del ejercicio); sustitución de ejercicio por sesión (catálogo `ALTS` con 2 alternativas por ejercicio; el sustituto se guarda en el log con `alt` y esa sesión no genera sugerencia de progresión); barra de progreso de ejercicios en el header de sesión; cabeceras con imagen en Progreso→Pasos (caminadora) y Check-in (báscula+metro); ícono de app (mancuerna glow azul) como apple-touch-icon en data-URI; instrucciones de pasos actualizadas a multi-hora (iOS no permite sync en segundo plano: automatizaciones de Atajos a horas fijas, cada una abre la app un instante). +30 créditos Magnific (total ~110).

**Funcionalidades sobre la v1:**
- Progreso interactivo: peso con línea de meta, proyección al 27/08 por regresión de 14 días y tooltips; **progreso por ejercicio** (selector agrupado por rutina, récord marcado en rojo, e1RM Epley, tabla de sesiones, botón directo desde la sesión de entreno).
- **Pasos**: checkpoint diario con meta configurable (8-10k), registro rápido en Inicio, gráfica de 14 días. **Integración con Salud del iPhone** vía Atajos: la app lee `?steps=N` de la URL y lo registra (instrucciones dentro de la app, MÁS → SALUD); HealthKit no tiene API web, el atajo automatizado a las 9 p.m. es el puente.
- **Recordatorios**: 7 por defecto (pesaje, entreno, hidratación multi-hora, pasos, inyección, meal prep, check-in) con toggle y hora editable; avisos del navegador (Notification API) con la app abierta + **exportación .ics** con RRULE y alarma para tener alertas nativas vía Calendario del iPhone.
- Base de recetas ampliada a **29 recetas** en 6 categorías (res/pollo/cerdo/pescado/huevo-económicas/cenas rápidas) con búsqueda, filtros, macros, costo por porción e ingredientes: cubre las 6 semanas sin repetir. Sin API de Claude (decisión: Nivel 1 puro por ahora).
- "Mano derecha": semana del plan y fase en el header (banner de descarga en semana 4, RIR 0-1 en semanas 5-6), checkpoint diario (entreno/pasos/proteína por comida/agua) con **racha**, registro de inyección semanal con próxima fecha, check-in semanal guiado con adherencia sugerida desde los checkpoints + tabla de evolución, cronómetro con beep/vibración y +30s, sesión en borrador persistente (no se pierde si se cierra), export/import JSON.

Persistencia: `localStorage` (claves `afc2:*`) — sigue pendiente migrar a Supabase al portar a Next.js PWA. Artifact publicado para probar en el teléfono (URL en el historial de la conversación de Claude Code). Fuente del ensamblado: partes en scratchpad de la sesión (`css.part`, `data.part.js`, `app.part.js`, `body.part`, `assemble.py`); si se pierde el scratchpad, `coach-afc-v2.html` es la fuente de verdad.

**REV 4 (27/07/2026) — dos usuarios (Andrés + Cami), spec en `spec-coach-app.md`:**
- **Multiusuario**: selector AFC/CAMI en el topbar (`ACTIONS.switchUser`), tema por perfil (Cami: acento coral `#FF7A9E` vía `:root[data-user=cami]`, anillos/gráficas paramétricos con `USERS[uid].g1/g2`). Datos separados por usuario con claves `afc2:u:{id}:{clave}`; el mercado es compartido (`afc2:shared:meal`). Migración automática de las claves viejas `afc2:*` → namespace de Andrés (`migrateV3`).
- **Persistencia (el bug del "se resetea")**: el entorno de Artifacts de claude.ai bloquea localStorage (sandbox) y NO ofrece capacidad de storage (solo `downloads` y `mcp`), así que la app caía al fallback en memoria y perdía todo. Ahora detecta el backend (`BACKEND='ls'|'mem'`), avisa con banner en Inicio + estado en MÁS → DATOS cuando no puede guardar, y el respaldo JSON usa `window.claude.downloads` dentro del artifact (capability declarada al publicar). Para uso diario con guardado garantizado: servir el HTML (localhost o hosting propio); pendiente el port a Supabase.
- **Rutinas Cami**: 4 días + 1 opcional (Lower A/B/C, Upper A/B+core), ids `c_*`, con alternativas en `ALTS`, RPE 7-8, bloques continuos de 6 semanas con descarga en la 4 (`PLAN.block:true`, helpers `weekInBlock`/`blockNum`). Las 6 rutinas de Andrés quedaron intactas (más específicas que las genéricas del spec; sus logs se preservan). Tracker de fuerza por ejercicio ya es por usuario (logs namespaced).
- **Nutrición**: macros por usuario (A: 2.200 · 195P/75G/180C, 2 comidas + snack; C: 1.700 · 115P/50G/195C, 3 comidas) con **conteo de macros por comida** (`USERS[uid].meals`, línea mono P·C·G·kcal y total Σ en PLAN DÍA). Catálogo reemplazado por las **8 recetas del meal prep compartido** con doble porción (`r.a`/`r.c`) e ingredientes en crudo para el mercado. Mercado con vista **AMBOS / ANDRÉS / CAMI** (`S.meal.view`); básicos etiquetados por dueño (5.º elemento `'a'|'c'`); el único scoop de whey es de Cami. Rotación de 5 desayunos de Cami en su PLAN DÍA. Presupuesto ref: $200-260 mil/sem los dos.
- **Alarmas de peso** por usuario en PROGRESO → PESO: A >1 kg/sem → subir kcal 10%; C >0,7 kg/sem → subir a 1.850 kcal. Nota fija de retatrutida (dosis la valida un médico) en Inicio y Más.
- Cami arranca con su evolución real sembrada (dic/25: 59,0 kg · jul/26: 59,5 kg; grasa 31,5→30,4%). Deep-link `?user=cami`. Pruebas: smoke test de 54 casos en jsc (harness en scratchpad) + test de migración, todo en verde. Artifact republicado en la misma URL.

**REV 5 (27/07/2026) — "Coach Cabritos":**
- **Rebrand**: la app se llama **Coach Cabritos**; mascota cabrito 3D (glossy toy-render con mancuerna y anillos azul+amarillo en los cuernos) generada en Magnific (flux-dev, 20 créditos, 2 candidatos, elegido el de la mancuerna). Embebida como logo del topbar (120px jpg) y apple-touch-icon (180px png). Original 1024px en el historial de Magnific.
- **Temas**: Cami pasó de coral a **amarillo dominante** (`#FFC94D`/grad `#FFE08A→#F2A93B`). Todos los azules quemados del CSS/JS se migraron a variables (`--acc-rgb`, `--acc2-rgb`, `--accHi-rgb`, `--bn1/2`); el tanque de agua queda azul a propósito (semántico). **Scope de color en Comida**: recetas y mercado AMBOS = **verde** (`data-scope=shared`), mercado ANDRÉS = azul (`=a`), mercado CAMI = amarillo (`=c`); `scopeOf()` en render() y `accColors()` para anillos SVG.
- **Registro de comidas con redistribución** (`mealStatus()` + `MEAL_CUTOFF`): si pasa la hora límite de una comida sin registrarla (A: almuerzo 15:00, snack 18:30; C: desayuno 11:00, almuerzo 15:30), sus macros se reparten en partes iguales entre las comidas restantes; chips del checkpoint muestran `85→100G`, PLAN DÍA muestra la línea "hoy: … (ajustado)" y la equivalencia práctica en gramos de proteína cocida extra por plato (≈P/0,30). Sin comidas restantes → aviso de respaldo.
- **Supabase**: sync opcional integrado (MÁS → NUBE): tabla `kv(house,uid,k,v)` (esquema en `supabase-schema.sql`), push con debounce 800 ms en cada `save()` (excluye `draft`/`fired`), pull al abrir (la nube manda), botones traer/subir/desactivar. Config en `afc2:sb` (localStorage). Falta solo crear el proyecto en supabase.com y pegar URL + anon key en la app.
- **Netlify**: carpeta `site/` lista (index.html + netlify.toml con X-Robots-Tag noindex + robots.txt Disallow). No hay CLI/token en la máquina: desplegar arrastrando `site/` a app.netlify.com/drop o con `npx netlify-cli`. La app también lleva `<meta name="robots" content="noindex">`.
- Suite de humo ampliada a **67 casos** (scopes de color, redistribución de comidas, supabase sin config) en verde. Artifact republicado en la misma URL.

**REV 5.1 (27/07/2026) — assets de La Cabrita integrados:**
- Space de Magnific "Character Model Sheet Development" (`a25cabc3-…`): CHARACTER CORE + STYLE Render (claro) + STYLE — App Night Gym (oscuro, dominante por prompt) + referencia + 14 poses model-sheet + 22 nodos APP (azul/amarillo/verde/neutros, NanoBanana 2 flash 1k) + 5 nodos ANIM (Kling 2.5 720p 5s, start frame cableado). El usuario ejecutó todo.
- **Imágenes**: las 22 se optimizaron (sips, sin WebP disponible: JPEG 820px q48 los 16:9, 420px q55 los 1:1; promedio 29 KB vs 1,2 MB originales). 20 embebidas: 15 photocards CSS (`ph-a-*`, `ph-c-*`, `ph-v-*`, `ph-rest`) + 5 en el objeto JS `CAB` (celebA/celebC/reloj/vacio/racha) para checkpoint, avisos de comida y estados vacíos. NO embebidas (viven en el space): hidratación y meal-prep-tuppers. Se removieron las 10 fotos genéricas anteriores (gen-* y stock, incl. ph-padel huérfana, −350 KB). HTML final ~1,05 MB autocontenido.
- **Videos**: `assets/anim/{celeb-a,celeb-c,descanso,racha,reps-a}.mp4` (avconvert PresetMediumQuality, 270-470 KB c/u; originales 2,5-6,5 MB). Son archivos EXTERNOS (no data-URI): en local/Netlify se reproducen; en el Artifact el 404 deja el poster embebido (helpers `cabVid`/`pcVid`, respetan reduced-motion). Usos: descanso = fondo del photocard de día libre; reps-a = fondo de la sesión Push de Andrés; celebración A/C = checkpoint al cumplir el día; racha = checkpoint con racha ≥7.
- **Rendimiento**: `content-visibility:auto` en `.mod`, `decoding="async"`, `preload="metadata"`, poster-fallback sin JS. phOf() mapea rutinas → miniaturas por usuario (PH_A para Andrés, `ph:` explícito para Cami).
- 67 pruebas en verde. Artifact republicado (misma URL). `site/` sincronizado con los videos para el deploy de Netlify.

**REV 6 (27/07/2026):**
- **Portada/ícono oficial**: apple-touch-icon y logo del topbar ahora usan el HERO oficial de La Cabrita del space (recorte de fondo con `images_remove_background`, compuesto con PIL sobre navy con glow azul+dorado; 512→180 png y 120 jpg).
- **Selector de usuario con avatares**: el uswitch ya no dice AFC/CAMI; muestra dos cabritas circulares (imagen de celebración azul = Andrés, dorada = Cami), la inactiva desaturada. Se construye en `applyUser()`.
- **Plan continuo**: se retiró el marco de corte con fecha (PLANS: `block:true`, weeks 156 para ambos). Hero muestra "Bloque N · Semana X/6"; sin cuenta regresiva ni "empuje final"; RIR 1-2 fijo; vPeso ya no proyecta a fecha, estima "~N semanas para llegar a la meta". La descarga sigue en la semana 4 de cada bloque. Las sugerencias de subir carga NO se tocaron.
- **Stepper con nombres**: los `exdot` de la sesión son pastillas con el nombre corto del ejercicio (`shortEx`, respeta sustitutos) en vez de números.
- **Media por ejercicio**: `exMedia(exId)` en modo foco busca `assets/ej/{key}.jpg` + `assets/anim/ej/{key}.mp4` (archivos EXTERNOS; se auto-oculta con onerror si no existen — p. ej. en el Artifact). Alias: pullup2→pullup, lcurl2→lcurl, c_abd2→c_abd, c_calf2→c_calf, c_hipl→c_hip, c_z2→sin media. **En el space quedaron creados SIN ejecutar 54 nodos "EJ — {key}" (NanoBanana 2 flash 1k, 16:9, Night Gym, azul/dorado según usuario) y 54 "ANIM — {key}" (Kling 2.5 720p 5s, start frame cableado del EJ correspondiente).** Al ejecutarlos: primero imágenes, luego videos; después se descargan a `assets/ej/` y `assets/anim/ej/` con el nombre del key.
- **Recetas**: catálogo ampliado a 33 (las 8 del prep + 25 reconvertidas del catálogo viejo con generador: tabla nutricional por ingrediente, porción Cami derivada — proteína ×0,6, carbo ×0,75 — y macros P/C/G/kcal calculados por porción). Vuelve la categoría "Cenas rápidas" (icono bowl nuevo) y cada categoría tiene color propio en badges y filtros.
- Supabase: la config (URL/key/casa) persiste en `afc2:sb` del dispositivo; las actualizaciones de la app NO la borran (mismo origen). 67 pruebas en verde. Artifact republicado.

**REV 7 (27/07/2026):**
- **Ícono/logo solo-rostro** (1:1): cabeza de La Cabrita sobre navy con glow azul+dorado; el logo ya no se desborda. **Topbar sin weekchip** (la info de semana vive en el hero y en Entrenar); el selector son 2 avatares de rostro 42px (mismo rostro oficial sobre glow azul/dorado, `CAB.faceA/faceC`), inactivo desaturado.
- **Reloj de La Cabrita** (`cabClock()` en Inicio): tarjeta según la hora — >21:30 durmiendo (video descanso), 5-9 pasos, 9-12 hidratación, 12-15 almuerzo, 15-18 racha/pre-entreno, 18-21:30 la rutina del día. Media reutiliza clases CSS ph-* e imágenes CAB; respeta reduced-motion.
- **Rutinas REALES de Cami** (de sus plantillas en `Rutina Cami/`, 3 días): Glúteo (abductor 2, leg curl sentado 2, hip thrust 3 @130 kg, búlgara 2, deadlift 2, kickback 3, back extension 2, step-up 3), Pierna·Quads (aductor 2, leg curl acostado 2, extensión 2, Smith squat 2, prensa 2 @160) y Tren superior (jalón 3, chest press 3, remo cable 3, fly 3, reverse fly 3). Ids nuevos: c_dead, c_adduct, c_lying, c_smith, c_chest, c_fly, c_rfly, c_backext, c_step (con ALTS). **Pesos reales sembrados en `SEED_LOGS.cami`** (precarga + sugerencias desde el día 1; el deadlift quedó sin peso porque el pantallazo lo cortaba). En el space se crearon (sin ejecutar) los 9 nodos EJ/ANIM dorados de los ids nuevos; los dorados de la rutina inventada anterior (c_squat, c_super, c_ohp, c_curl, c_face, c_latr, c_bench, c_rowm, c_plank, c_legr, c_sumo, c_hipl, c_lunge, c_calf) quedaron huérfanos: no ejecutarlos.
- **Series editables**: ✕ por serie en la sesión (mín. 1) y botón "+ SERIE"; al FINALIZAR, el número de series usado se guarda en `S.custom[exId]` (persistido y sincronizado) y las próximas sesiones abren con ese número. `buildDraft` y `suggestion` respetan el custom.
- **Recetas más legibles**: badge 48px con color de categoría, título 15,5px y dos filas humanas con punto azul/dorado ("Andrés · 82 g prot · 670 kcal"); la línea mono completa (P·C·G·kcal·$) y los ingredientes bajaron al detalle.
- 71 pruebas en verde. Artifact republicado; site/ sincronizado.

**REV 8 (27/07/2026) — paquete de confiabilidad + features (auditado):**
- **Confiabilidad**: cronómetro por timestamp (`TIMER.end`, sobrevive el bloqueo del teléfono, repinta en `visibilitychange`); BORRAR ÚLTIMO pesaje pide confirmación con fecha; metas `apple-mobile-web-app-capable` + `manifest.webmanifest` (standalone en iOS); **service worker** `sw.js` (cache-first, offline total con hosting; registrado solo en http/https). manifest+sw+icon-192/512 viven junto al HTML y en `site/`.
- **Checkpoint inteligente**: `prote` cuenta si todas las comidas están registradas O si el día cerró con ≥2 (la vencida ya se redistribuyó). Horas límite de comida **editables** (MÁS → Preferencias, `S.cfg.cut`), meta de agua editable.
- **Sesión**: notas por ejercicio (`S.exnotes`, sincronizadas), calculadora de discos (`plates()`, barra 20 kg), detección de **PR** al finalizar (toast, compara vs. histórico, ignora sustitutos).
- **Progreso**: buscador de ejercicios, borrar registros del historial (con confirm), **volumen semanal por grupo muscular** (`MUSCLE` map + `weekVolume()`, guía 10-20 series), gráficas de **cintura** y **grasa %** (campo nuevo en check-in, meta 14,5/26,5), **carta dominical de la Cabrita** (peso vs. semana anterior, sesiones, series, PRs, racha).
- **Comida**: botón **ÁRMAME LA SEMANA** (1 res + 1 pollo evitando repetir `meal.lastAuto`, porciones 5+5, mercado listo), **ítems libres** en el mercado (`S.meal.extras`, con costo opcional), calculadora "¿cuánta proteína tiene?" en Plan día.
- **Otros**: onboarding de 3 pasos la primera vez por perfil (`cfg.tour`), movilidad pre-entreno en Rutinas (contenido), rotación de sitio de inyección sugerida (abdomen izq/der, muslo izq/der por conteo), botones ✕ de serie a 34px.
- **Auditoría**: 85 pruebas en verde; 0 emojis en UI (se removió uno que violaba DESIGN-STANDARDS); localStorage solo en la capa de storage; reduced-motion respetado; confirm() en las 3 acciones destructivas. HTML 1,11 MB autocontenido. Pendientes conocidos: peso del deadlift de Cami, fotos de progreso (necesita storage), merge fino de conflictos en Supabase.

**REV 8.1 (27/07/2026) — media de ejercicios + Cabrita interactiva:**
- **46 imágenes de ejercicios** descargadas del space (mapeadas por el texto único del prompt vía `creations_search`, 2 páginas), optimizadas a 820px JPEG q48 (~32 KB c/u, 1,5 MB total) en `assets/ej/{key}.jpg` como archivos EXTERNOS (no infla el HTML). El modo foco de la sesión ya las muestra. **Faltan 3 sin ejecutar**: "EJ — c_dead", "EJ — c_adduct", "EJ — c_lying" (y todas las "ANIM — …" de video); cuando se corran, integrar igual (pipeline en esta nota + `ejmap.json`/`ejurls.txt` del scratchpad como referencia del método).
- **Cabrita interactiva** en el hero de Inicio: botón flotante con su rostro (flota suave, se apaga con reduced-motion); al tocarla suelta 1 de 12 frases "tierna pero ruda" en toast y rebota (`ACTIONS.cabTap`, keyframes cabfloat/cabboing).
- 89 pruebas en verde. Artifact republicado; `site/` sincronizado (index + assets/ej).

**REV 9 (27/07/2026):**
- **Bug del scroll**: render() ya no salta al tope en actualizaciones dentro de la misma vista (clave de vista `render._k`; tocar vasos/chips mantiene la posición; cambiar de tab sí va arriba).
- **Rutinas multi-día**: `S.sched[rid]` acepta array de días (`daysOf()`, `routineOn()` actualizado; los valores viejos numéricos se envuelven solos). El selector de "mover días" ahora son 7 daychips por rutina (Cami puede repetir Glúteo 2-3×/sem).
- **Calendario rediseñado**: segmento SEMANA/MES. Vista semanal nueva (filas por día con miniatura de rutina, título, estado y 4 pips de iconos entreno/pasos/comidas/agua + marca de inyección; borde rojo = pendiente). Vista mensual con barrita inferior de checkpoint (done/4) por celda y leyenda con iconos.
- **Galería de fotos de registro** (Progreso → FOTOS): 1 foto/día por usuario, redimensionada a 1080px JPEG en el dispositivo y guardada en **IndexedDB** (`cabritos-fotos`, clave `{uid}:{iso}`; NO se sube a la nube, se dice en la UI). Grid 3 col con fecha, lightbox con borrar. Fila "Foto del día" en el checkpoint (extra, no afecta la racha; se oculta si el entorno no tiene IndexedDB, p. ej. artifact).
- **Iconografía de navegación nueva**: home/barbell/food/chart/more redibujados (línea 1.75, radios suaves, punto de acento; more = cuadrícula de apps) + icono camera nuevo.
- Pendiente del space: siguen sin ejecutar "EJ — c_dead", "EJ — c_adduct", "EJ — c_lying" y todas las ANIM. 97 pruebas en verde. Artifact republicado; site/ sincronizado.

**REV 10 (27/07/2026):**
- **Fotos en la nube compartidas**: con Supabase configurado, las fotos suben al bucket `fotos` de Storage (`{house}/{uid}/{fecha}.jpg`, bucket público — la privacidad la da el código de casa; esquema actualizado en `supabase-schema.sql`, hay que re-correrlo). La galería muestra las de AMBOS (borde azul A / dorado C), cada uno borra solo las suyas; sin nube cae a IndexedDB local. Si la subida falla (sin señal), guarda local y avisa.
- **Foto en días pasados**: fila "Foto de ese día" en el editor del calendario (`FOTO_TARGET` + `fotoShotAt`). **Foto en el check-in** (fila antes de guardar). El input perdió `capture` → iOS ofrece cámara O galería.
- **49/49 imágenes de ejercicios**: integradas las 3 últimas (c_dead, c_adduct, c_lying). Solo faltan las ANIM (ninguna corrida).
- **Recetas en cajitas desplegables**: catálogo agrupado por categoría (`recListing`/`recCard`, `<details class="catgroup">` con badge de color, contador y chevron), grupo "En el mercado" fijado arriba y abierto; buscar muestra lista plana; se quitaron los chips de filtro.
- 104 pruebas en verde. Artifact republicado; site/ sincronizado. NOTA: para las fotos compartidas hay que 1) re-correr `supabase-schema.sql` en el SQL Editor y 2) re-subir `site/` a Netlify.

**REV 10.1 (27/07/2026):** soporte `?stepsbulk=yyyy-MM-dd:pasos,…` para backfill de pasos desde Salud (varios días en una sola apertura; sanitiza formato local, ignora fechas futuras/lineas malas, sobreescribe lo manual — Salud es fuente de verdad; entra a `save('steps')` → sube a Supabase). El atajo recomendado agrupa por día los últimos 15 días y sirve tanto de backfill como de auto-reparación diaria. 105 pruebas en verde.

**REV 10.2 (27/07/2026):** botón "PROBAR CONEXIÓN" en MÁS → NUBE (diagnóstico separado de tabla kv y bucket de fotos con el HTTP y la acción a tomar), mensajes específicos al fallar subida de foto (distingue bucket faltante), y la galería en modo nube ahora también muestra las fotos LOCALES pendientes de subir (antes quedaban invisibles). El ERROR del usuario: su teléfono corría REV 8 (Netlify sin re-subir + SW v1 viejo); solución: re-subir site/ y abrir la app dos veces.

**REV 11-12 (28/07/2026):**
- **REV 11**: versión unificada en `const APPREV` (la etiqueta "REV 8" llevaba 3 revisiones mintiendo — bumps manuales olvidados; ahora un solo lugar). `?stepsbulk` ya estaba (10.1); diagnóstico nube (10.2).
- **REV 12**: **AGENDA como 6.ª pestaña** de navegación (icono cal; Entrenar quedó solo con rutinas, el daystrip de Inicio lleva a Agenda). Tercer segmento **FOTOS** en el calendario: grid mensual 7×n con la foto de cada día como celda (toggle Andrés/Cami con mini-avatares; requiere nube para ver las del otro). **Candado juguetón**: las fotos del OTRO en fecha D solo se desbloquean si el espectador cumplió SU entreno de ese día (`canSeePartner(d)`=dayState.entreno; celdas/ítems `locked` con icono lock nuevo, toast "termina tu entreno y se desbloquea"); aplica en calendario-fotos y en la galería de Progreso. Es candado de cliente (el bucket es público): suficiente como juego de pareja, no como seguridad.
- Usuario confirmó nube OK (había corrido el schema en el proyecto equivocado). Pasos: le faltaba filtro de Fuente=iPhone (doble conteo Watch+iPhone) y la unidad del rango (semanas vs. días) — instrucciones dadas, sin cambios de código. 112 pruebas en verde.

**REV 13 (28/07/2026) — UX de sesión y home:**
- **Swipe para borrar serie**: deslizar una `.setrow` a la izquierda >90px la elimina (touchstart/move/end delegados, tinte rojo mientras deslizas, mín. 1 serie; el ✕ sigue existiendo).
- **Cronómetro**: `mark()` ahora usa `S.draft.restSec ?? e.rest ?? 90` (robustez ante datasets raros) y hay **selector de descanso por sesión** en la cabecera de la sesión: AUTO / 1:00 / 1:30 / 2:00 / 3:00 (`S.draft.restSec`, persiste en el borrador). Test automatizado confirma que mark() arranca el timer.
- **Ejercicios extra en la sesión**: caja "AGREGAR EJERCICIO" antes de FINALIZAR — del catálogo completo (select agrupado, precarga pesos, respeta `S.custom`) o **nombre libre** (id `x_slug`, 3×8-12, desc 90 s). `sessEx(r)` = rutina + extras; todo el flujo (stepper, foco, auto-avance, finish, PRs) usa la lista efectiva. `vEjercicios` tolera ids libres.
- **Modo lista**: el título de cada ejercicio va en color de acento (azul/dorado según usuario).
- **Home en cajitas**: checkpoint rediseñado como grid 2 col (`.ckgrid`/`.cktile`): Entreno (tap → sesión) | Pasos (**anillo circular** de progreso + input) / Agua (ancha, tanque) / Comidas (ancha, chips + avisos de redistribución) / Foto del día (ancha). Tiles cumplidos con borde de acento y tick de gradiente. Recordatorios compactados a 2 en tarjeta tight.
- **Navegación 6 tabs**: #nav forzado a grid de 6 columnas (labels 8.5px, iconos 20px) — nada se cae de nivel.
- 118 pruebas en verde. Artifact republicado (REV 13); site/ sincronizado (falta re-subir a Netlify).

**REV 14 (28/07/2026):**
- **Fuera "Semana 3/6"**: weekLabel() → "PLAN CONTINUO" / "SEMANA DE DESCARGA"; hero chip igual; check-in dice "Semana del dd/mm"; Más muestra "Fase: Progresión/Descarga"; tabla renombrada "Ciclo (se repite cada 6 semanas)". La lógica interna de bloques sigue intacta (deload semana 4).
- **Tile de Entreno**: ya no se ve vacía — lleva la miniatura de la rutina (`.tilethumb`) y un **check rápido** (`quickTrain`: marca/desmarca S.acts gym sin abrir la sesión; si hay sesión registrada no hace nada). El tile completo sigue llevando a la sesión (ahora también cuando ya está registrada, para consultarla).
- **La Cabrita del hero** subió a bottom:76px (ya no tapa el week strip).
- **Discos gráficos**: `plateViz(w)` dibuja la barra con placas por lado (alturas proporcionales 25→1.25, etiquetas dentro, manguito y collarín) en el panel DISCOS del modo foco.
- **Tendencias**: `lineChart` acepta `trend:true` (regresión lineal punteada `.trendl`) — activa en peso, fuerza (top kg), **nueva gráfica de reps promedio por sesión**, cintura y grasa %.
- **Sugerencia con más data** (`suggestion()` v2): 1) tope de rango en todas las series → sube carga; 2) e1RM cayendo 2 sesiones → alerta (manda sobre todo); 3) a ≤3 reps del tope con reps sosteniéndose → "A N reps de subir a X kg". Detectado y corregido en tests: la regla 3 se disparaba con fuerza cayendo (orden invertido).
- 127 pruebas en verde. Artifact republicado (REV 14); site/ listo para re-subir.

**REV 15 (28/07/2026):**
- **Tendencia proyectada**: con `trend:true` la gráfica comprime los datos (~45% de espacio futuro), extiende la línea punteada hacia adelante, escribe el valor proyectado ("≈ 90,1 kg") al final y pone un **punto en la intersección con la meta** cuando la tendencia la cruza dentro de la ventana (peso, fuerza kg/reps, cintura, grasa).
- **Barras de pasos en gradiente** (`defs` con `accColors()` en barChart, `.barmark{fill:url(#bgr)}`, `.low` al 35%).
- **Check rápido visible**: `.tick.off` ahora es 26px con borde y fondo de acento (antes se camuflaba en gris).
- **Home más limpio**: los "Próximos" son una nota de una línea dentro del checkpoint (tap → Más); se eliminó la tarjeta de retatrutida del final del home (permanece en Más).
- 132 pruebas en verde. Artifact republicado (REV 15); site/ listo para re-subir.

**REV 16 (28/07/2026) — gráficas con eje de TIEMPO real:**
- `lineChart` entra en `timeMode` cuando los puntos traen fecha (`d`): el eje X posiciona por días reales (13/07→27/07 ya no se ve igual de cerca que 27/07→28/07), la regresión se calcula sobre días, la proyección se extiende ~45% del rango en días futuros, y cuando la tendencia cruza la meta se marca el punto con **la fecha estimada** ("≈ 05/08"). Ticks del eje = 2-4 fechas repartidas por días. Zonas de tooltip centradas en cada punto real (espaciado desigual). Etiqueta "≈ valor" se desplaza si choca con la de META. Todos los llamadores (peso, fuerza kg, reps, cintura, grasa) pasan `d`.
- Test de espaciado real (14 días vs 1 día debe diferir >5×) y de proyección con fecha. Un test viejo era frágil (buscaba "/6" y lo encontró dentro de un base64) — ahora limpia data-URIs antes de afirmar. 135 pruebas en verde. Artifact republicado (REV 16); site/ listo.

**REV 17 (28/07/2026):** proyección interactiva en las gráficas de tendencia (timeMode): la zona futura tiene un hit-rect por día con tooltip "Proyección dd/mm · ≈ valor"; el hit del último punto real ya no invade la zona futura. Aplica a todas las gráficas con `trend:true` y fecha (peso, fuerza, reps, cintura, grasa). 136 pruebas en verde. Artifact republicado (REV 17); site/ listo.

**REV 18 (28/07/2026):**
- **Tipografía nueva**: Bricolage Grotesque (display: títulos, números grandes, stats, timer — 800/700) + Schibsted Grotesk (cuerpo 400, botones/énfasis 500, micro-labels 600). **Embebidas como woff2 variable en data-URI** (latin subset bajado de Google Fonts; NO por link — el artifact bloquea hosts externos y la app es offline). Archivo y Archivo Black eliminadas; IBM Plex Mono se conserva para datos tabulares pequeños. DESIGN-STANDARDS.md §3 actualizado. HTML ~1,25 MB.
- **Resumen de sesión** (`showSummary`, modal al FINALIZAR): tonelaje del día (Σ kg×reps), series/ejercicios/minutos (buildDraft guarda `t0`), **récords** con +kg (celebración de La Cabrita en video si hay PR), **mejoras** (+reps a mismo peso vs. sesión anterior), y **"Para la próxima"**: hasta 4 recomendaciones generadas con la data (sugerencias por ejercicio, alertas de fuerza primero, + agua/proteína pendientes del checkpoint).
- 138 pruebas en verde (harness ganó document.body). Artifact republicado (REV 18); site/ listo para re-subir.

**REV 19 (28/07/2026):**
- **Agua en ml con vaso animado**: 1 vaso = 250 ml. `waterUI` es ahora un vaso (clip-path trapezoide) que se llena con ola animada; botones − / +250 ML. Metas por defecto: Andrés 2.500, Cami 2.000 ml (editable en MÁS, pasos de 250, 1.000–5.000). `migrateWater()` en `loadState` convierte datos viejos (valores ≤40 se multiplican ×250) en local y al bajar de la nube.
- **Home en cuadrícula 2×**: Agua dejó de ser tile ancho; ahora comparte fila con el nuevo tile de **Check-in semanal** (estado hecho/pendiente por `S.checkins` vs. lunes de la semana, "HOY TOCA" los domingos, navega a Progreso→Check con `ckGo`).
- **Comida libre** (`S.free`, sincronizada en SB_KEYS): en Plan del Día, sección "¿Qué comiste?" con dos modos: texto libre → `parseFood()` offline (FOODDB ~50 alimentos con macros por 100 g, unidades taza/cda/scoop/lata/tajada, números en palabra "una/media/dos", match por límite de palabra para evitar falsos positivos tipo fresas→res) → desglose + confirmar; o POR MACROS manual (P/C/G, kcal auto). Total "comido hoy" = plan marcado + libre, con barra de proteína. Chip de acceso "COMÍ ALGO FUERA DEL PLAN" en el tile de comidas del home.
- **switchUser mantiene la página**: ya no manda a Inicio ni fuerza Entrenar; solo resetea estado por-usuario (sesión abierta → draft del nuevo usuario o lista de rutinas).
- **Entrenos retroactivos**: en Agenda, el editor del día ofrece "¿Entrenaste? Regístralo con series" con chips por rutina (`pastSession`); `buildDraft(r, fecha)` y `finish()` escriben logs/sesión con la fecha del calendario (ordenando historial), la sesión se abre en modo lista con encabezado "Registro del dd/mm". En retro no se generan PRs/mejoras/recs (evita falsos récords contra datos posteriores).
- **Auditoría de tipografía**: inputs/textarea/select pasaron a Schibsted (los numéricos y type=time conservan IBM Plex Mono vía `[inputmode]`), tablas `.tb` a Schibsted con celdas `.r` en mono, `.ingrow` (ingredientes) a Schibsted con cantidades mono, `.num` (numeración 01/02) y números del daystrip a Bricolage 800.
- **Pasos dobles**: paso 05 en MÁS→Salud: el filtro **Fuente es &lt;iPhone&gt;** va DENTRO de la acción "Buscar muestras de salud" (agrupar por día sin filtrar suma todas las fuentes).
- 157 pruebas en verde (chk15: migración de agua, parser de comida, switchUser, retro-sesiones, tiles nuevos). Artifact republicado (REV 19); site/ sincronizado, pendiente re-subir a Netlify.

**REV 20 (28/07/2026):**
- **Placeholders en Schibsted**: los campos numéricos siguen en IBM Plex Mono, pero su placeholder ("actualizar", "pasos", "al ombligo"…) es texto → regla `::placeholder{font-family:var(--ui)}`. Detectado por Andy en el input de pasos del home.
- **Cabrita de check-in sin fondo** (`CAB.medidas`, PNG alpha 300px cuantizado a 256 colores, ~16 KB): generada en Magnific (NanoBanana 2 flash, ref. de identidad de una creación EJ dorada + `images_remove_background`; 1er intento salió fuera de personaje —sin banda roja, pelaje dorado— y se regeneró con la corrección explícita; ~153 créditos en total). Cinta métrica en la cintura, cámara instantánea colgada, pulgar arriba.
- **Check-in rediseñado**: resumen visual arriba (grid de 3 stats: peso promedio con delta ▾/▴ en color vs. semana pasada, días de checkpoint, entrenos + series + PRs) con la línea de La Cabrita debajo; formulario con la cabrita recortada flotando a la derecha (`.cicab`), campos con iconos (cintura/cadera con regla y placeholders-guía "al ombligo" / "lo más ancho"), energía y sueño lado a lado, foto del check-in con copy de la cámara. Mismos ids (`ciPeso`…): `saveCheckin`/`segpick` intactos.
- 160 pruebas en verde (chk16 + aserción de chk3 actualizada al diseño nuevo). Artifact republicado (REV 20); site/ sincronizado, pendiente re-subir a Netlify.
- Pasos: **Andy confirmó que el atajo ya quedó** (el doble era el filtro de fuente).

**REV 21 (28/07/2026):**
- **Bug real de Andy**: los pasos del atajo llegaban "a la web pero no a la app". Causa: en iOS, el atajo abre la URL en **Safari**, y Safari y la PWA instalada son **contenedores de almacenamiento separados** (localStorage aislado por app de pantalla de inicio). El puente es la nube, pero (a) Supabase estaba conectado solo en la PWA, (b) el push tenía debounce de 800 ms y podía morir al cerrarse Safari, y (c) la PWA solo hacía `sbPull` en init, que iOS no re-ejecuta al volver a abrirla.
- Fixes: `sbPush(k, now)` con envío inmediato y `keepalive:true` (si el body <50 KB) para el import de `?steps`/`?stepsbulk`; registro `sbPending` + `sbFlush()` en `visibilitychange(hidden)` y `pagehide` (lo debounced se sube antes de morir la página); al **volver a primer plano** con la nube ok y >30 s del último pull → `sbPull` + re-render (`sbLastPull`); toasts honestos ("subidos a la nube" vs. "solo en este navegador: conecta la nube en MÁS"); paso 05 nuevo en MÁS → Salud explicando las dos copias. **Acción del usuario (una vez): abrir cabritos.netlify.app en Safari → MÁS → NUBE → conectar con la misma URL/llave/casa.**
- Harness: `window.addEventListener` stub. 164 pruebas en verde (chk17). Artifact republicado (REV 21); site/ sincronizado, pendiente re-subir a Netlify.
- Limitación conocida (documentada, no urgente): el pull al primer plano es "cloud gana" por clave; si un push falló offline, el pull se salta (guard `sbState==='ok'`), pero no hay merge fino por campo — ediciones simultáneas de los dos en la misma clave se pisan (última gana).

**REV 22 (28/07/2026):** tanda completa del plan de acción (Andy: "hazlos todos", seguridad excluida porque la app no sale de ellos dos). Corrección de auditoría: el auto-avance en modo foco YA existía (tanda UI de REV 13-14); se retiró del plan.
- **Proteína libre cuenta al checkpoint**: `eatenOn(dISO)` (generaliza eatenToday); `dayState.prote` también pasa si plan marcado + registro libre ≥ 80% de la meta de proteína. El chip del home ahora muestra "N G LIBRES".
- **Merge fino del mercado**: checklist con `{v,t}` por ítem (normalizeMeal migra booleanos, `ckOn()` para leer); `checkitem` estampa `Date.now()`; en `sbPull` la clave shared/meal fusiona checklist ítem por ítem (gana el toque más reciente) en vez de pisar. Los dos pueden chulear en el súper a la vez.
- **Respaldo semanal**: banner en Inicio si han pasado ≥7 días de `cfg.lastBackup` (o nunca); `backupNow` descarga el .json y estampa la fecha.
- **Atajo PRO (steps_in)**: el Atajo puede hacer POST directo a la kv (clave `steps_in` con `{fecha:pasos}`); `applyStepsIn()` fusiona en `steps` tras cada sbPull (válidas ≤ hoy, idempotente). Sección en MÁS con la receta exacta (URL/cabeceras/cuerpo con house y uid reales) solo si SB está conectada. El atajo clásico de abrir la página sigue vivo.
- **Peso**: toggle DIARIO / PROMEDIO SEMANAL (`weightPts()` agrupa por lunes, tooltip con nº de pesajes).
- **Recetas favoritas** (`meal.favs`, compartidas): botón ★ en la tarjeta, ★ en el título, orden favs-primero por categoría, y "Ármame la semana" prefiere favoritas (respetando la rotación anti-repetición).
- **Check-in**: placeholders "ant. X" en cintura/cadera/grasa, línea "Anterior (fecha): …", y al guardar el toast dice los deltas (CINTURA −1,5 CM…).
- **Nuevas funciones**: `rachaRisk(h)` — banner nocturno (≥19 h) con lo que falta exacto para cerrar el día; sección LOGROS en Fuerza (tonelaje acumulado en toneladas, récords de 30 días, sesiones); **Duelo de cabritos** en el check-in (`partnerWeekScore()` lee el estado del otro usuario del storage post-sync y compara días cumplidos de la semana, aprox).
- 178 pruebas en verde (chk18). Artifact republicado (REV 22); site/ sincronizado, pendiente re-subir a Netlify.

**REV 23 (28/07/2026):** Andy pidió expandir la competencia y las ideas del tintero.
- **Retos de Cabritos** (en Progreso→Check, debajo del duelo): semanal, mensual y trimestral. Score = días cumplidos (dayDone) en el período; `periodRange(kind, prev)` (semana lunes-domingo, mes calendario, trimestre I-IV), `myScoreRange` + `partnerScoreRange` (generaliza el duelo; `partnerWeekScore` ahora es un wrapper). Barras de los dos (la del otro con su color), días restantes, líder actual, **premio editable compartido** (clave shared `retos` {sem,mes,tri}.p, en SB_KEYS/SHARED_KEYS, handler `retoPremio` en CHANGES sin render para no perder el foco) y **ganador del período anterior** calculado retroactivamente ("Cami ganó el anterior (5-3) · a cobrar: masaje").
- **Comparador de fotos**: modo COMPARAR en la galería (toca 2 fotos → `cmpAdd` → `fotoCompare` con cortinilla deslizable: capa superior con clip-path + range + barra luminosa; CSS .cmpwrap/.cmptop/.cmpbar); atajo **PRIMERA VS ÚLTIMA** (`myFotoItems()` une nube + locales); funciona con fotos propias, locales y del otro (si están desbloqueadas).
- **Foto antigua**: chip FOTO ANTIGUA → date input (máx. hoy) + subir de galería a esa fecha (`fotoShotOld` reutiliza FOTO_TARGET); pensado para cargar fotos de hace un año y ver el cambio completo.
- **La Cabrita comenta el resumen**: `cabPhrase(s)` con 5 pools (2+ récords / 1 récord / mejoras / alerta de bajón / base), rotación determinista por nº de sesiones (sin Math.random), frase en comillas verdes bajo el titular del modal.
- 190 pruebas en verde (chk19). Artifact republicado (REV 23); site/ sincronizado, pendiente re-subir a Netlify.

**REV 24 (28/07/2026):** batch grande de UX pedido por Andy (retos pesados, calendario, fotos, cabClock, tiles, comida, hero, notificaciones).
- **Regla de racha nueva** (pedida por Andy): el día cuenta con **agua + pasos + comidas** (`dayDone` = los tres); el **entreno es bonus** y desempata retos. Ring del checkpoint a /3, textos del tour/checkpoint/calendario ('/3'), `rachaRisk` ya no lista entreno, `partnerScoreRange` con la misma regla.
- **Retos rediseñados con sección propia**: sub-tab RETOS en Progreso (seg → `.seg.scrollx` deslizable de 6); `vRetos()` con hero de **las dos cabritas en versus** (imagen nueva `CAB.vs`, Magnific + recorte) y `retoCard()`: marcador grande 5–3 (.vsscore), barra versus única (dos llenados desde extremos, colores de cada uno), entrenos como desempate visible, **premio detrás de un chip** (PONER PREMIO/EDITAR → input solo al tocar, `UI.retoEdit`), ganador del período anterior en una línea. Duelo/retos removidos del check-in (respira).
- **Calendario**: input de fecha + IR + HOY (`calJumpGo` calcula `calM` por diferencia de meses; `calToday`).
- **Fotos**: presets "VS HACE 1 SEMANA / 1 MES / 1 AÑO" (`cmpPreset` busca la foto más cercana a esa época y avisa si queda lejos) + PRIMERA VS ÚLTIMA + comparar 2 a mano; bloque con label propio.
- **cabClock**: media 96px, título Bricolage 17px + cuerpo 13.5px (antes small casi invisible).
- **Tiles del home**: Check-in con la cabrita de medidas asomando; Foto del día con **cabrita selfie nueva** (`CAB.selfie`, Magnific: teléfono en alto + bíceps, recortada) y copy "La Cabrita ya posó: te toca".
- **Comida**: chips rápidos que arman y calculan al toque ("2 huevos", "150 g de pollo"…, `freeChip` con parseFood en vivo); el aviso de redistribución ahora muestra **cómo quedaría cada comida pendiente** (≈ g de pollo/pescado/yogur + macros ajustados); banner de **rotación automática** en Recetas si `meal.lastAutoAt` ≥ 7 días (autoWeek lo estampa).
- **Hero**: `.motstrip` deslizable con datos motivacionales (toneladas levantadas, entrenos, racha, fotos, última cintura) + chip del otro ("Cami va 4/7 esta semana" → navega a retos).
- **Notificaciones**: botón PROBAR UN AVISO AHORA (`notifTest`) + explicación honesta (iOS solo avisa con la web abierta; sin servidor push las rutas nativas son .ics o automatización de Atajos).
- Magnific: 2 generaciones + 2 recortes (~156 créditos): selfie y versus, ambas en personaje a la primera.
- 207 pruebas en verde (chk20; chk19 ajustado a vRetos). Artifact republicado (REV 24); site/ 1,37 MB sincronizado, pendiente re-subir a Netlify.

**REV 25 (28/07/2026):** feedback de pantallazos de Andy + "aplica toda la auditoría".
- **Bug de arranque en Entrenar**: cualquier goSession creaba draft y el init lo retomaba. Ahora solo retoma si el draft tiene series MARCADAS, y `backTrain` descarta drafts vacíos (mirar una rutina ya no deja fantasmas).
- **Nav solo iconos** (26px, aria-label conservado; spans fuera).
- **Tiles**: cabritas reencuadradas (dentro del tile, bottom 4px, ~50px) mientras llegan las definitivas; **2 nodos nuevos creados en el Space** "Character Model Sheet Development" (sin ejecutar, los corre Andy): "APP — tile check-in (medio cuerpo)" y "APP — tile foto del día (selfie medio cuerpo)" — waist-up, asomándose desde la derecha mirando a la izquierda, fondo gris liso para recorte.
- **Comidas del home rediseñadas**: barra de proteína del día (comido/meta con libre incluido), filas por comida con estado (✓ registrada / ✗ venció·repartida / pendiente con gramos ajustados) y **tarjeta "AHORA: SNACK"** para la comida vigente con su descripción del plan, equivalencias concretas (g de pollo / scoops) y la receta de la semana del mercado con "porción y algo más" si viene recargada.
- **Agenda abre en MES** (default calView).
- **Resumen de sesión centrado**: `.sumedia` circular 104px con aro glow, titular Bricolage centrado, frase de La Cabrita bajo el titular.
- **Resumen de día pasado**: en la agenda, "VER LO QUE HICE ESE DÍA" (`daySummary`) — rutina(s), tonelaje, series por ejercicio (con sustitutos marcados).
- **Motstrip verificado y enriquecido** (funcionaba, pero con poca data quedaba vacío): ahora entrenos de la semana, toneladas, racha, pasos/día 7d, entrenos totales, fotos, cintura.
- **Auditoría aplicada**: tour personalizado de Cami (rutinas reales + scoop), búsqueda tocable en Fuerza (chips de resultado, `exPick`), **palmarés** en Retos (`periodRangeN`, conteo de semanas/meses/trimestres ganados por cada uno), **banner de ganador** en el home los primeros días de cada período nuevo (lun-mar / día 1-3 / inicio de trimestre) con premio a cobrar. El punto de peso del HTML se decidió NO aplicar: mover imágenes a assets rompería el artifact y el SW ya cachea todo en el teléfono.
- 217 pruebas en verde (chk21). Artifact republicado (REV 25); site/ sincronizado, pendiente re-subir a Netlify.

**REV 26 (28/07/2026):** correcciones de pantallazos de Andy.
- **Agenda no abría en mes**: el default real estaba en el init de `UI` (`calView:'sem'`), no en los fallbacks — corregido a 'mes'.
- **Día como pantalla propia**: tocar cualquier día (calendario o daystrip del home) abre `vDia()` — barra con ← AGENDA, título del día y flechas ‹ › para navegar día a día; el editor completo dentro y, si hubo entreno, el resumen "LO QUE HICISTE ESTE DÍA" se muestra directo (sin toggle). El editor ya no vive apretado debajo del calendario.
- **AHORA con macros completas**: la tarjeta de la comida vigente muestra chips P/C/G/kcal recalculados, la línea "antes: XP · YC · ZG" cuando viene recargada, la explicación explícita ("Snack no se comió: esta comida quedó recargada…") y la traducción a plato con proteína Y carbohidrato (g de pollo + g de arroz cocido) + receta de la semana. Se recalcula en vivo con cada render/comida vencida. "ajustada"→"recargada" en las filas.
- **Celebración**: la imagen salía chica y encajonada por `.fboxin img{width:100%;object-fit:contain;background:var(--card)}` del visor de fotos — override con `!important` en `.sumedia`: 118px, circular, cover, con aro glow.
- 223 pruebas en verde (chk22; chk20/21 ajustadas al nuevo flujo de día). Artifact republicado (REV 26); site/ sincronizado, pendiente re-subir a Netlify.

**REV 27 (28/07/2026):**
- **Tiles con las cabritas de medio cuerpo** que Andy ejecutó en el space (nodos "APP — tile check-in/foto del día"): fondo removido (3 créditos c/u), recorte, 240px, 256 colores (~18+14 KB) → `CAB.tileCheck` (96px alto, esquina) y `CAB.tileFoto` (88px). `CAB.medidas`/`CAB.selfie` siguen para el form del check-in.
- **Sistema de puntos** (Andy: "el gym es bonus, revisa cómo lo ponderas"): antes el score era días cumplidos y el entreno solo desempataba (un día entrenado sin agua valía 0). Ahora `dayPts()`: agua 1 + pasos 1 + comidas 1 + **entreno real (trained||alt) 1 de bonus** — máx 4/día. `myPtsRange`/`partnerPtsRange` en retoCard (marcador en pts, "máx N", fila "bonus entrenos: 3 · 2"), palmarés, banner de ganador ("21-18 pts") y chip del hero ("Cami lleva 12 pts esta semana"). La RACHA no cambia (sigue siendo los 3 diarios). Las funciones viejas de días quedan por compat.
- **3 nodos nuevos en el space** (sin ejecutar, para Andy): "APP — hero retos (versus horizontal)" 16:9 con composición simétrica de cuerpo completo, y "APP — avatar Andrés (cara)" / "APP — avatar Cami (cara)" 1:1 — identidad diferenciada definida: Andrés-cabrito = muñequeras AZULES + cejas rectas gruesas + smirk; Cami-cabrita = muñequeras AMARILLAS + pestañas largas + moño amarillo junto a la banda roja. Al ejecutarlos: bg removal → embebido (vs del hero de retos + `#uswitch` avatares).
- 228 pruebas en verde (chk23; chk20 ajustado a la imagen nueva). Artifact republicado (REV 27); site/ sincronizado, pendiente re-subir a Netlify.

**REV 28 (28/07/2026): la app ahora se llama CabriCoach.**
- **Rebrand**: brand del topbar "Cabri**Coach**", `<title>`, notificaciones, footer de MÁS y manifest de site/ (name y short_name; ojo: iOS puede pedir reinstalar la PWA para ver el nombre nuevo). La línea "ANDRÉS · REV" salió del topbar; la **versión ahora vive al pie del home** ("CABRICOACH · REV 28 · ANDRÉS") — sigue siendo el check de deploy.
- **Avatares diferenciados** (ejecutados por Andy en el space, bg removal + 160px): `CAB.avA` (cejas gruesas, smirk, puño con muñequera azul) y `CAB.avC` (pestañas, moño amarillo, puño amarillo) en el selector del topbar y en el hero. **Tercer botón** en el topbar (`vsbtn`, llama) → Retos.
- **Versus horizontal** nuevo reemplaza `CAB.vs` (simétrico, 523×300): hero de retos a `min(78%,300px)` y banner de ganador a 72px. `CAB.selfie` eliminada (ya sin uso).
- **Home reorganizado**: el photocard de rutina/descanso salió (el tile Entreno ya lo cubre); `cabClock` tomó ese formato — photocard de 150px con la frase de la hora en grande (h2 22px), la cabrita del momento asomando a la derecha en los casos de imagen, y tap para abrir la rutina cuando aplica.
- **Hero**: la cabrita flotante rara salió; ahora es un avatar de 46px centrado junto al chip del plan (mismo tap → frases). `cabTap` ganó **datos curiosos** calculados con la data real (km caminados vs. Bogotá–Medellín/Cartagena/maratón, toneladas vs. elefantes/ballena azul/carro, litros de agua), mezclados 65/35 con las frases de siempre.
- **Puntaje explicado en Entrenar**: tarjeta "Así se puntúa" (1+1+1 diarios y racha; entreno +1 bonus en retos).
- **Check-in tile**: cabrita a 114px (tile 122px).
- 234 pruebas en verde (chk24). Artifact republicado (REV 28); site/ sincronizado (incluye manifest), pendiente re-subir a Netlify.

**REV 29 (28/07/2026):**
- **Pasos ponderados en retos** (idea de Andy: es su terreno de desventaja y abre diferencial): `stepXtra(steps,goal)` = +1 punto por cada 5.000 pasos POR ENCIMA de la meta, tope +2. `dayPts` y `partnerPtsRange` lo suman → máximo **6 pts/día** (agua 1 + comidas 1 + pasos 1 + extra 2 + entreno 1). Barras de retoCard sobre days*6. La racha NO cambia.
- **Retos como sección propia, fuera del nav**: se entra SOLO por el botón de la llama del topbar (`retosGo` → `UI.tab='retos'`, en VIEWS; el botón se marca `.on` cuando estás ahí). RETOS salió del seg de Progreso.
- **Explicación del puntaje movida de Entrenar a Retos** (tarjeta bajo el hero, con la regla de pasos: "caminar de más es donde se abre la brecha").
- **Título con fuerza**: "RETOS / DE CABRITOS" apilado, Bricolage 34px uppercase, "cabritos" en gradiente (`gradtxt`).
- 238 pruebas en verde (chk25; chk19/20/21/24 ajustadas). Artifact republicado (REV 29); site/ sincronizado, pendiente re-subir a Netlify.

**REV 30 (28/07/2026):**
- **Cabrita del check-in on-model**: Andy ejecutó el nodo "APP — check-in form (medidas cuerpo completo)"; bg removal + recorte + 300px/256c (~16 KB) reemplaza a `CAB.medidas` (la vieja era la primera generación directa, dorada y fuera de estilo).
- **Seg de Progreso repartido**: con RETOS fuera quedaban 5 pestañas apiladas a la izquierda (scrollx); vuelve a `cols5` a lo ancho.
- **Filtro de persona en Fotos**: seg LOS DOS / ANDRÉS / CAMI (solo con nube activa; `UI.fotoWho`, filtra remotas y oculta locales ajenas). 
- 242 pruebas en verde (chk26). Artifact republicado (REV 30); site/ sincronizado, pendiente re-subir a Netlify.

**REV 31 (28/07/2026): testeo de uso simultáneo (pedido por Andy) — 2 bugs reales encontrados y corregidos.**
- **Bug 1 (cruce de datos entre usuarios)**: `sbPush` con debounce y `sbFlush` leían `S[k]` al momento de DISPARAR el envío; si el usuario cambiaba en esa ventana de 0,8 s (o en el flush de pagehide), los datos del usuario nuevo se escribían bajo la fila del saliente en la nube. Fix: `rawGet(uid,k)` lee el payload del namespace correcto (localStorage/MEM) en el momento del envío — los 3 puntos de envío migrados (verificado por grep: 0 restantes con S[k]) — y `switchUser` hace `sbFlush()` ANTES de cambiar UID.
- **Bug 2 (retos compartidos se pisan)**: el objeto `retos` era last-write-wins entero; si Andrés editaba el premio semanal y Cami el mensual a la vez, uno borraba al otro. Fix: `retoPremio` estampa `{p, t:Date.now()}` y `sbPull` fusiona **por reto** (sem/mes/tri) ganando la edición más reciente; formato viejo sin `t` cuenta como 0.
- **Verificado sin problema** (chk27, flujo entrelazado real con save como MARCAR): sesiones/logs/draft por usuario no se mezclan al alternar, el draft del saliente sobrevive con sus series marcadas, checklist del mercado ya fusionaba por ítem, fotos por rutas separadas, pasos por uid.
- **Límites conocidos que quedan (LWW, riesgo bajo y aceptado)**: `meal.selected`/`favs` y campos no-checklist del mercado se pisan si los dos editan exactamente a la vez; mismo usuario en dos dispositivos simultáneos comparte fila. Documentado, no corregido a propósito.
- **Nodo nuevo en el space** (sin ejecutar): "APP — hero retos (arena nocturna)" 16:9 estilo App Night Gym (arena oscura #0B0D0F, rim light azul vs. dorado, chispas al centro, espacio para overlay de texto) — al ejecutarlo se integra como fondo photocard del hero de retos.
- Auditoría del fix: suite completa 247 en verde; greps de verificación (payloads, lectores de premio compatibles, orden del flush).

**REV 32 (28/07/2026):**
- **Arena nocturna en el hero de Retos**: Andy ejecutó "APP — hero retos (arena nocturna)" y le encantó; integrada como `.ph-retos` (JPEG 820px q52, ~24 KB) — photocard con veil degradado y el título "RETOS / DE CABRITOS" superpuesto (chip "La casa se divide"). El modelo le metió un "VS" azul/dorado al centro pese al no-text: funciona a favor, se queda. `CAB.vs` (recorte) sigue en el banner de ganador del home.
- **Ícono de duelo en el topbar**: compuesto con PIL (mitad avatar Andrés + mitad Cami, divisor oscuro, 160px/128c ~10 KB) → `CAB.vsIcon` reemplaza la llama en el botón de retos.
- **Presets de entreno** (pregunta de Andy): ya existía la precarga de PESOS por serie + sugerencia por datos + balances (resumen/LOGROS). Nuevo: `buildDraft` precarga también las **REPS** de la última sesión (por serie), y cuando la sugerencia es "Sube a X" (`sug.apply`), el peso ya viene **subido automáticamente** en todas las series. `addExFromCat` igual. Hint en modo foco: "Precargado con tu última sesión · carga ya subida a X — solo MARCAR si repites". Registrar una sesión repetida = puro MARCAR.
- 252 pruebas en verde (chk28; chk24/25 ajustadas al hero nuevo). Artifact republicado (REV 32); site/ sincronizado, pendiente re-subir a Netlify.

**REV 33 (28/07/2026):** fix del "hueco" del header en iPhone (pantallazo de Andy): con `viewport-fit=cover` la página corre bajo la barra de estado, pero `#topbar` (sticky, top:0) no cubría esa franja → al hacer scroll el contenido se veía por detrás, entre el notch y el header. Fix: `padding-top:calc(14px + env(safe-area-inset-top))` en el topbar — su fondo blur ahora tapa la zona del notch. Artifact republicado (REV 33); site/ sincronizado. Nota: su pantallazo mostraba REV 23 en el teléfono — recordar re-subir site/ a Netlify para ver todo lo de hoy.

**REV 34 (28/07/2026):**
- **PIN por usuario** (candado de cortesía): cada uno lo activa en MÁS → PRIVACIDAD (`cfg.pin`, 4-6 dígitos); al cambiar al perfil del otro se pide con prompt (destino leído vía `partnerState('cfg')`). Documentado en la UI que no es cifrado.
- **Fotos privadas por defecto**: `canSeePartner(d)` dejó de ser "si entrenaste" → ahora lee el `fotopub` del dueño (clave por-usuario nueva, en SB_KEYS). El dueño comparte foto a foto: al abrir una suya, botón "COMPARTIR CON CAMI/ANDRÉS" (toggle `fotoPub`), y el grid marca "· C VE". Candado ajeno: "privada: se ve cuando su dueño la comparta".
- **Rutinas 2×3**: `.rgrid`/`.rcard` (thumb arriba, nombre + chip de días de una letra, última fecha).
- **Desglose de puntos por reto**: chip "¿DE DÓNDE SALEN LOS PUNTOS?" → tabla por concepto (agua/comidas/pasos meta/pasos extra/entrenos bonus) con columnas de los dos (`ptsBreakdown` + `partnerBreakdown`) y fila TOTAL que cuadra con el marcador.
- **Iconos del nav a 29px.**
- **Historial de entrenos por fecha** en Fuerza: filtro 7 DÍAS / 30 DÍAS / TODO, lista de días (fecha · rutinas) y al tocar expande `daySummary` (kg×reps por ejercicio).
- **Tonelaje de Cami verificado**: la mate estaba BIEN (11,63 t reales de sus registros del gym: prensa 2.560 kg + hip 2.210 + …), el problema era de credibilidad: los logs semilla estaban todos fechados 27/07 y SIN sesiones ("0 sesiones · 11,6 t"). `migrateCamiSeeds` (en loadState, idempotente, solo si sessions vacío y todo con esa fecha) reparte por rutina (Glúteo 23/07, Quads 25/07, Superior 27/07) y crea las 3 sesiones; LOGROS ahora muestra "~X t/sesión" (3,9 t/sesión de pierna es normal con prensa y hip thrust).
- 260 pruebas en verde (chk29; smoke ajustado a las semillas). Artifact republicado (REV 34); site/ sincronizado, pendiente re-subir a Netlify.

**REV 35 (29/07/2026): mega-batch de la lista de Andy.** Todo lo pedido menos auth real (plan escrito, decisión pendiente).
- **Check-in**: medidas nuevas brazo/pecho/muslo (con "ant." y deltas en el toast) + **uno por día** (mismo día sobreescribe).
- **Plan semanal con criterio**: en Agenda, bajo los días de rutina, análisis automático: grupos grandes 2 días seguidos ("dale 48 h") y volumen semanal fuera de 10-20 series/grupo; si todo bien, lo dice en verde.
- **Retos**: `agreedPrize` — **cada uno propone premio (clave por-usuario retoprops) y vota (retovotes); queda cuando ambos votan igual**; `agreedReset` — **reinicio desde fecha solo si los dos proponen la misma** (retoreset; los marcadores del período actual arrancan en esa fecha vía a0); **vitrina de trofeos** (palmaresData: sem=bronce/mes=plata/tri=oro, ★ de colores junto al nombre en el marcador vía troMini; las copas 3D llegan con los nodos del space); desglose con fila de movilidad.
- **Movilidad = rutina bonus**: card en el grid de rutinas (abre la guía de 8-10 min con HECHA HOY), `S.mobil` por día, **+1 punto de reto** (máx 7/día; racha intacta) — también contada para el otro.
- **Snacks**: categoría nueva con 4 recetas colombianas fit (yogur griego+frutos rojos+granola, batido whey+banano+maní, huevos duros+tostada, chocolate 85%+almendras) con macros y mercado A/C.
- **Buzón de ideas** (compartido, merge por ítem): recetas antojadas + ejercicios sugeridos, en MÁS, para traérmelos cada 15 días.
- **Swipe para borrar series ARREGLADO**: el touchstart excluía inputs y botones… y la fila es casi toda inputs y botones (por eso "nunca funcionó"); ahora arranca en cualquier parte de la fila y distingue swipe horizontal de scroll vertical (dy vs dx).
- **Ciclo de 6 semanas → nota de arranque de semana** con OK (cycleAck por lunes); la tabla salió de Rutinas.
- **Aproximación por ejercicio** (50%×8 → 75%×4 sobre el peso precargado, redondeado a 2,5) + **RM estimado con 80%/90% en cada ejercicio**; **CALCULADORA RM** en Entrenar (peso×reps → 1RM y %70-95) + chip **DÍA RM DEL MES** (cfg.rmMonth).
- **Cambio de ejercicio en vivo por grupo muscular**: el panel CAMBIAR ahora muestra grid con IMÁGENES de los ejercicios del mismo grupo (MUSCLE + assets/ej) + las alternativas de texto.
- **Ciclo menstrual (solo Cami)**: config en MÁS (última menstruación + duración); card en Inicio con fase (menstrual/folicular/ovulación/lútea), sugerencia de cargas y comida.
- **PIN con hash real** (SHA-256 con sal, nunca el número en claro; fallback marcado si no hay WebCrypto) + **candado al abrir** opt-in (5 intentos y bloquea). Auth de verdad (Supabase Auth + RLS + storage privado) queda PROPUESTA: cambia login y el modelo de compartir; decidir en sesión dedicada.
- **Perfil**: pestaña propia (tocar TU avatar; el del otro cambia usuario) — avatar grande, stats vitales, trofeos, últimas medidas, accesos.
- 276 pruebas en verde (chk30; chk3/8/19/25 ajustadas). Artifact republicado (REV 35); site/ 1,54 MB sincronizado, pendiente re-subir a Netlify. **4 nodos nuevos en el space** (sin ejecutar): 3 trofeos (bronce/plata/oro) + movilidad (cabrita estirando).

**REV 36 (29/07/2026):**
- **Accesos del perfil como cajitas**: `.accgrid` 2×2, cada `.accbox` con icono en contenedor tintado (`.accic`), título y subtítulo (Check-in/Retos/Fotos/Ajustes). Seguridad real: pospuesta por decisión de Andy.
- **Moodboard de referentes publicado como artifact aparte** (https://claude.ai/code/artifact/42b7ad8e-78b3-40a9-981d-f3f180f09386): 6 apps (Gentler Streak, Hevy, Whoop, Duolingo, Opal, Copilot Money) con 2 capturas reales c/u (fichas del App Store: search API para Hevy; scraping de trackViewUrl + plantilla {w}x{h}→392x696 para el resto, webp embebido), nota "qué robarle" por app, tokens actuales de CabriCoach y el prompt de brandbook completo en un bloque copiable. 458 KB autocontenido.
- Suite verde tras el cambio (chk30 ajustado a accgrid). Artifact de la app republicado (REV 36); site/ sincronizado.

**REV 37 (29/07/2026):** apoyo emocional del ciclo (pedido por Andy).
- **4 imágenes de fase generadas en Magnific** (Cami-cabrita, bg removal, 260px/128c, ~49 KB total): menstrual (acurrucada con manta + bolsa de agua caliente), folicular (mancuerna en alto + chispas), ovulación (radiante, manos en cintura), lútea (auto-abrazo + té y chocolate). ~312 créditos.
- **`cycleInfo()`**: helper única fuente de verdad (día, key, fase, tip de carga, food, animo, img de fase, color) — reemplaza la lógica inline.
- **Card de Inicio rediseñada** (`.cyccard`): imagen de la fase + gradiente del color de fase + frase de ánimo + consejo; toca → perfil.
- **Sección "TU CICLO" en el perfil de Cami**: imagen grande de la fase, ánimo, entreno y comida con badges del color, y **línea de las 4 fases** (`.cycline`/`.cycstep`) con la actual resaltada. Colores por fase: menstrual #E8637A, folicular #58DFA3, ovulación #FFC94D, lútea #C98BFF. Sin ciclo configurado → invita a hacerlo en MÁS. Solo Cami; nota de que es orientativo y privado.
- 283 pruebas en verde (chk31; chk30 ajustado a "FASE FOLICULAR"). Artifact republicado (REV 37); site/ 1,61 MB sincronizado, pendiente re-subir a Netlify.

**REV 38 (29/07/2026): tanda de rediseño visual (pantallazos de referencia de Andy).**
- **Space "Icons Cabri"** (a2602484-…, ref node wProE047EI = grid verde de iconos): creados 6 nodos (SIN ejecutar) — láminas por tema en el estilo del ref (línea gruesa redondeada): Navegación, Entrenamiento, Nutrición, Seguimiento, Estados, y Colores de marca (los 9 clave en azul/dorado/menta). Andy ejecuta; luego se vectorizan para reemplazar `ic()`.
- **4 cabritas de ciclo re-creadas como nodos** en el space de personajes (para consistencia, ya que las embebidas "no funcionaban" en su teléfono — realmente era el deploy viejo).
- **Progreso segmentable**: `UI.progRange` (7/15/30/180/365 → SEM/15D/30D/6M/AÑO) con `rangeSeg()` en Peso, Fuerza y Pasos. Peso y fuerza filtran por fecha (con fallback a últimos 8 si el rango queda con <2 puntos); Pasos muestra barras diarias hasta 30 días y **promedio semanal** en 6M/AÑO.
- **Gráficas estilo "Evolución de Peso"**: área con gradiente del color del usuario bajo la línea + punto "Hoy" con glow (lineChart gana `<path class="area">` + linearGradient por chart).
- **Perfil con actividad reciente + resumen**: cajas de COMPOSICIÓN (grasa corporal % y masa magra kg = peso×(1−grasa%), con delta ▲/▼ vs. check-in de hace ~1 mes, color según si el cambio es bueno) y ACTIVIDAD RECIENTE (últimas sesiones con series y kcal estimadas ≈ tonelaje×0,045 + series×6; VER MÁS a 15; toca → agenda del día).
- **Nav flotante tipo pill**: barra despegada del borde (bottom 10px+safe-area), ancho acotado, radios 22px, sombra; 7 items ahora (se agregó Perfil con icono `user`), item activo con fondo tintado redondeado.
- **Calendario a color**: celdas con relleno sólido — entrenado = gradiente del usuario, día cumplido (3/3 sin entreno) = verde menta, otra actividad = tinte; se quitó la barrita de checkpoint; leyenda actualizada.
- 292 pruebas en verde (chk32; chk5 ajustado a calcell). Artifact republicado (REV 38); site/ sincronizado, pendiente re-subir a Netlify.
- **Pendiente de análisis futuro**: nav de 7 items en pill de 440px queda apretado en pantallas chicas; si molesta, agrupar (Perfil dentro del avatar del topbar) o reducir a 5 + overflow.

**REV 39 (29/07/2026): batch visual (pantallazos de referencia de Andy).**
- **Perfil fuera del nav** (vuelve a 6; se entra por el avatar).
- **Composición arreglada**: `composicion()` helper reutilizable, ahora SIEMPRE aparece — con estado vacío que invita a MEDIR (grasa%) si no hay dato. Presente en Perfil y bajo la comparativa de Fotos. Bug real: los checkins semilla de Andrés no traían `fat`, por eso nunca salía.
- **Estadísticas clave** (30 días: volumen, entrenos, calorías estimadas, tiempo) y **Mis medallas** (oro/plata/bronce hexagonales según palmarés) en el Perfil.
- **Botón deslizar para iniciar** el entreno en el home (`.slidebtn` + handlers touch: arrastrar knob ≥85% dispara goSession; click también funciona).
- **Barras del barChart redondeadas** (rx) + relleno de gradiente `url(#bgr)`; iconos con stroke 2 (más cuerpo).
- **Calendario**: data arriba-izq ("N entrenos este mes"), chip "HOY 29", y pie con la fecha completa del día seleccionado; celdas ya a color (REV 38).
- **Inputs con icono de búsqueda** (`.inwrap`/`.in.has-ic`) en Fuerza.
- 302 pruebas en verde (chk33). Artifact republicado (REV 39); site/ sincronizado.
- **Artifact de estrategia** publicado (https://claude.ai/code/artifact/9be2c88d-d1e6-403c-8947-e339e8cb7fea): explica por qué los iconos siguen siendo SVG in-line (no PNG del space), el sistema de reglas (grid 24, trazo 2px, roles de color heredados por currentColor), prompt reutilizable, y la decisión de tipografías — **Neue Montreal es de pago (Pangram Pangram), no embebible; propuesta: Geist Sans + Geist Mono + Manrope (todas OFL)**. Espera decisión de Andy.
- **Secuenciado (no hecho aún, comunicado)**: tipografías (tras decisión), cajas de profundidad radio 28, ejercicios lista→expandir, completar-ejercicio +XP y número animado 12→13, redibujar set de iconos SVG chunky.

**REV 40 (29/07/2026):**
- **Imágenes ejecutadas del space integradas**: 4 cabritas de ciclo re-hechas (nodos definitivos, incluye la menstrual con moño) reemplazan las embebidas; **3 trofeos 3D** (oro/plata/bronce con cara de cabrita) → `CAB.troOro/Plata/Bronce`. ~21 créditos de bg removal.
- **Flujo de rutina corregido**: quité el botón deslizar del home; ahora tocar una rutina en Entrenar abre **detalle general** (`vRutinaDetalle`: hero, stats, lista de ejercicios) y AHÍ está el deslizar para iniciar. `routineOpen`/`routineBack`/`UI.routineView`; goSession lo limpia.
- **Deslizar arreglado**: reescrito con **pointer events** (funciona con dedo y mouse; antes touchstart no disparaba bien y el click auto-iniciaba). Arrastrar ≥80% inicia; un toque limpio también (accesible).
- **Composición siempre visible**: las dos cajas (grasa/masa magra) se renderizan aunque no haya grasa% (con "—" + invitación a medir). Bug: los checkins de Andrés no traían fat.
- **Ir a fecha colapsable**: chip "IR A FECHA" que despliega el date picker solo al tocar; "HOY" siempre visible.
- **Trofeos con imágenes**: Mis Trofeos (perfil) y Vitrina (retos) usan las copas 3D en vez de estrellas/hexágonos.
- **Micro-recompensas**: `xpFloat()` "+10 XP" flotante al marcar serie (+ vibración), `exDoneCelebrate()` overlay "¡EJERCICIO LISTO! +25 XP" con check y glow al completar todas las series de un ejercicio.
- 312 pruebas en verde (chk34; chk33 ajustado). Artifact republicado (REV 40); site/ sincronizado.
- **Artifact comparador de iconos** (https://claude.ai/code/artifact/41c0f05c-23ae-427c-befc-9f621d955a56): las dos propuestas (Geométrica 2px angular vs Orgánica 2.4px redondeada) dibujadas como SVG REAL, mismo set de 12, + versión en color de marca. Espera decisión de Andy para volver el ganador el set completo.
- **Pendiente**: número animado 12→13 (queda para micro-anim v2), cajas de profundidad radio 28, ejercicios lista→expandir en sesión, tipografías (decisión Geist vs comprar Neue Montreal). El "dato arriba/abajo del calendario" (REV 39) ya está en código; si Andy no lo ve es por deploy viejo — recordar re-subir site/.

**REV 41 (29/07/2026): recompensas + rediseño del checkpoint (pantallazos de Andy).**
- **2 imágenes de Andrés masculino** generadas (buff brazos cruzados + levantando mancuernas, ceja recta, muñequeras azules) → `CAB.andBuff`/`CAB.andLift`. ~156 créditos.
- **Sistema de recompensas**: XP real (`S.cfg.xp`) que sube al marcar serie (+10), completar ejercicio (+25), terminar sesión (+50), desbloquear calcomanía (+100); `levelInfo(xp)` → nivel + título (curva 1.15^n); barra de nivel en el perfil. **Calcomanías** (`achList()`, 19 hitos derivados de la data: tonelaje con comparaciones — moto/carro/elefante/camión/avión/ballena — PRs, rachas, entrenos, pasos, retos ganados); grid en el perfil (desbloqueadas vs bloqueadas), `checkNewAch()` detecta nuevas (S.cfg.achSeen) y `achCelebrate()` lanza overlay dorado "¡CALCOMANÍA DESBLOQUEADA!".
- **Checkpoint rediseñado** (ref de Andy): `.ckhero` con la cabrita masculina (andBuff/Andrés, cycFoli/Cami) + "N de 3 al momento"; fila de 4 `.ckpip` (agua/pasos/comidas/bonus con el entreno en dorado); mini-marcador del reto de la semana (`.ckreto` → retos). Tile de pasos con número grande + anillo + mini-barras de 10 días + botón sync. Cabrita del check-in más grande (134px). Tile de Entreno con la cabrita levantando (Andrés).
- **cabClock arreglado**: el caso `img:` (media mañana/tarde) ya no es photocard cortada con espacio arriba — ahora es tarjeta compacta con thumbnail redondo (`.ccthumb`) + texto.
- **Tarjeta RENDIMIENTO** en Progreso (Peso/Fuerza): % de checkpoints de la semana (grande) + delta vs. semana pasada + mini-línea de 7 días + 3 cajas (Fuerza = e1RM vs. primer registro, Resistencia = pasos vs. meta, Movilidad = días con estiramiento). El "dato de progreso" que Andy quería, no en el calendario.
- 322 pruebas en verde (chk35; chk10/20 ajustadas). Artifact republicado (REV 41); site/ 1,73 MB sincronizado.
- **Artifact iconos v2** (https://claude.ai/code/artifact/ffd2ac9a-8af2-4f1f-9318-94e327e659f7): más tech — Duotono (contorno + plano al 15%) vs Bicorte (mono + acento de color pleno). Espera decisión.
- **Sigue pendiente**: número animado 12→13, cajas de profundidad, lista→expandir, tipografías (al final por decisión de Andy).

**REV 42 (29/07/2026): nueva estructura del home + fidelidad al checkpoint.**
- **REGLA GUARDADA EN MEMORIA** (imagenes-siempre-en-space): toda imagen se crea como NODO en el Space y Andy la ejecuta; nunca images_generate directo.
- **2 nodos nuevos creados** (sin ejecutar): "APP — entreno tile (Andrés levantando)" (pose de curl, la anterior no servía) y "APP — calcomanías (hoja de 9 stickers)" (moto/carro/elefante/camión/avión/ballena/flama/pasos/estrella).
- **Home reestructurado fiel a la imagen**: hero = avatar + "NOMBRE · PLAN CONTINUO" + PESO ACTUAL grande + faltan; tarjeta `.wprog` (INICIO/ACTUAL/META + barra knob + PROGRESO %); fila `.hstats` de 3 cajas (perdidos/ritmo/racha con icono). Card **LOGROS** (toneladas / pasos/día 7d / entrenos 7d + VER TODOS) reemplaza el motstrip. Daystrip en su tarjeta. `cabClock` ahora es card **TU COACH** con botón de acción contextual (Registrar agua / Ir a entrenar / Check-in).
- **Checkpoint fiel a la ref**: quité el mini-marcador de reto de debajo (ckreto). Queda `.ckhero` (cabrita + N de 3) + fila `.ckpips`.
- **Pasos**: el % ahora va DENTRO del anillo (66px), con el número grande y mini-barras al lado — mejor distribuido como la ref.
- **Avatar con long-press**: mantener oprimido el avatar del hero (`data-avatar`, pointerdown 480ms) abre menú modal (Mi perfil / Retos / Cambiar a <otro>); tap corto sigue yendo al perfil (guard AVLP para no navegar tras el long-press).
- **Cajas de profundidad**: sombra de doble nivel (inset highlight + drop) en mod/wprog/cktile/hstat/kbox/sbox/calco/rcard.
- **Iconos**: Andy eligió **BICORTE** — la migración del set (~30 iconos SVG a mono+acento) queda como tanda dedicada siguiente (no se hizo en REV 42 para no dejarla a medias).
- 328 pruebas en verde (chk36; chk10/20/24/35 ajustadas al home nuevo). Artifact republicado (REV 42); site/ sincronizado.
- **Pendiente firme**: bicorte set completo, número animado 12→13, lista→expandir en sesión, integrar los 2 nodos nuevos cuando Andy los ejecute, tipografías (al final).

**REV 43 (29/07/2026): fidelidad visual a las referencias de Andy.**
- **Imágenes ejecutadas integradas**: cabra de curl de Andrés (`CAB.entCurl`, reemplaza la que no servía en la caja de entreno) + **9 calcomanías** recortadas de la hoja de stickers (moto/carro/elefante/camión/avión/ballena/flama/pasos/estrella → `CAB.stkX`). 2 nodos MÁS creados (sin ejecutar): entreno contrapicado y 3/4 espalda (ángulos de cámara para variar la caja de entreno).
- **Topbar**: fuera el logo y el texto "CabriCoach"; queda SOLO el avatar. Mantener oprimido (data-avatar, long-press) abre el menú perfil/retos/cambiar-usuario (el vsbtn de retos también salió del header).
- **Hero fiel a la imagen**: número de peso mucho más grande (clamp 64-84px) con **gradiente vertical** (blanco→acento). Cajas contenedoras con gradación apenas perceptible (mod y card2 con linear-gradient sutil + borde al 5%). Insights (`.hstat`) con iconos de color por columna (azul/lila/naranja) y textos más grandes. Sección LOGROS con las mismas cajas. Daystrip **ovalado y angosto** (pills con check dentro del pip).
- **TU COACH**: card compacta (min 128px), sin icono de corazón, con la imagen ocupando el lado derecho a sangre (`.coachimg`), jerarquía de texto (label mint + titular Bricolage + cuerpo + botón).
- **Checkpoint fiel**: la fila de pips pasó a **secuencia de círculos conectados por línea punteada** (`.ckpath`/`.cknode`/`.ckcirc`), con badge de conteo arriba y cambio de color al cumplir (bonus en dorado) — como la referencia. Caja de entreno con el personaje nuevo centrado + "IR A ENTRENAR".
- **Rendimiento con filtros**: chips GENERAL/PESO/VOLUMEN/TIEMPO (`UI.rendMode`), stat grande (58px), y las 3 cajas Fuerza/Resistencia/Movilidad apiladas en una fila (`.kgrid.k3`).
- **Calcomanías** ahora usan los stickers 3D reales (grises si bloqueadas); la celebración de desbloqueo muestra el sticker grande.
- 336 pruebas en verde (chk37; chk35/36 ajustadas). Artifact republicado (REV 43); site/ 1,81 MB sincronizado.
- **Pendiente**: bicorte set completo, número animado 12→13, lista→expandir, integrar los 2 nodos de ángulos de entreno cuando Andy los ejecute, tipografías.

**REV 44 (29/07/2026): correcciones finas de Andy.**
- **Avatar press-and-slide**: mantener oprimido (260ms) despliega 3 opciones flotantes (`.avpop`/`.avopt`: Perfil/Retos/Cambiar); deslizar resalta y soltar elige; toque corto → menú modal completo (que ahora incluye MÁS/AJUSTES). Reescrito con pointer events; el click del avatar ya no navega (lo maneja pointerup).
- **Hero REVERTIDO** al anterior (Andy: "no me entendiste"): volvió el `.mod hero glowtop tc` centrado con avatar+chip, PESO ACTUAL, bignum, **statrow** (3 stats inline con mini-barras) y **motstrip** de chips. Se quitó wprog/hstats y la card LOGROS separada.
- **Checkpoint 2 columnas** (`.ck2col`): columna A = imagen de la cabrita (ocupa las 2 filas), columna B = fila 1 "N de 3 al momento", fila 2 la secuencia de círculos agua/pasos/comidas/bonus.
- **Nav sin "Más"**: 5 iconos, más grandes (32px). "Más/Ajustes" se movió al menú del avatar (modal y picker).
- **Gradación imperceptible en TODAS las cajas**: gradiente vertical de un tono levemente más claro (#13181D/#161B21) al fondo de la app (#0B0D0F/#0F1216), aplicado a mod/cktile/kbox/sbox/hstat/wprog/rcard/accbox/calco/medal/day/catcard/catgroup/coachc.
- **Comida rediseñada** (fiel a la ref): categorías como **grid de 2 columnas** (`.catgrid`/`.catcard` con badge + conteo + thumb); "EN EL MERCADO" arriba; tocar una categoría (`UI.foodCat`) abre sus recetas con botón CATEGORÍAS para volver. Search y PROTEÍNA DE LA SEMANA se mantienen. (Los thumbs usan placeholder hasta que Andy ejecute el nodo "recetas categorías (7 platos)".)
- **3 nodos nuevos creados** (sin ejecutar): "entreno card (horizontal night gym)" + "coach card (horizontal night gym)" — sujeto a la derecha, izquierda oscura para texto, ángulo que da protagonismo a las pesas; y "recetas categorías (7 platos)".
- 342 pruebas en verde (chk38; chk6/18/20/36 ajustadas a los reverts). Artifact republicado (REV 44); site/ sincronizado.
- **Pendiente firme**: integrar los nodos horizontales de entreno/coach + food sheet cuando Andy los ejecute; bicorte set completo; número animado 12→13; lista→expandir; tipografías.

**REV 45 (29/07/2026): overhaul de nav + fixes finos.**
- **Bug del checkpoint 2col**: faltaba el CSS (renombré ckhero→ck2col en HTML pero no en CSS). Agregado `.ck2col{display:grid;grid-template-columns:96px 1fr}` + `.ck2b`. Ahora sí son 2 columnas (imagen | texto+círculos).
- **Header eliminado**: fuera `#topbar` completo. El avatar se movió al **centro del nav** (`.navav`, 52px, más grande que los iconos), con los 5 slots [inicio, entrenar, AVATAR, agenda, comida]. Iconos del nav a 31px, más juntos. `buildNav()` reconstruye en cada cambio de usuario.
- **Progreso fuera del nav** → acceso desde el Perfil (`progGo`, en la grid de accesos).
- **Avatar press-and-slide corregido**: `touch-action:none` + `preventDefault` para que NO scrollee la app; mantener oprimido despliega **3 CÍRCULOS** (avatar del otro · reto · mi avatar), se arrastra y suelta para elegir; **toque corto → mi perfil** (ya no abre el modal, como pidió Andy).
- **Días del hero más rectangulares** (border-radius 14px).
- **Hero con gradación del color del usuario** (`.mod.hero` radial-gradient del acento).
- **Gradación más marcada/oscura en TODAS las cajas** (top #161C24/#1A212A → fondo casi negro #080A0C/#0A0D11).
- **Comida rediseñada**: tabs con icono y más altas (`.segfood`); caja MEAL PREP en **gradiente verde** completo (`.mealprep`); buscador con **botón de filtro** (chips de categoría); **categorías (`.catcard2`)** con gradiente del color de la proteína, icono pequeño arriba + conteo grande + nombre; iconos de PROTEÍNA DE LA SEMANA **con color**.
- **3 nodos nuevos creados** (sin ejecutar): "comida cabrita chef (meal prep)" + "comida cabrita proteína" (para la sección de comida). Los horizontales de entreno/coach y el food sheet quedaron pendientes de recuperar/integrar (Andy confirmó que ya los ejecutó — integrar en la próxima).
- 351 pruebas en verde (chk39). Artifact republicado (REV 45); site/ sincronizado.
- **Artifact iconos v3** (https://claude.ai/code/artifact/b9c0a441-5b3c-4d49-8597-1040dc1a5ee4): **sólidos con gradación leve** (relleno pleno + linearGradient claro→oscuro, se tiñe por contexto) — el recurso general que pidió Andy. Espera su OK para volverlo el set completo.
- **Pendiente**: integrar entreno/coach horizontal + food sheet + food cabritas cuando estén; set de iconos elegido; número 12→13; lista→expandir; tipografías.

**REV 46 (29/07/2026):**
- **Iconos sólidos con gradación aplicados** (Andy eligió esa propuesta): nuevo mapa `SOLID` con ~20 iconos clave (home/barbell/chart/food/cal/user/flame/steps/drop/camera/more/star/check/target/heart/clip/zap/cart/book/trend); `ic()` los renderiza como fill con `linearGradient` de currentColor (1 → .62 opacity) para el degradado sutil que se tiñe por contexto; el resto cae a stroke (migración progresiva). Ya se ven sólidos en nav, home, comida, perfil.
- **Avatar**: `draggable="false"` + `-webkit-user-drag:none`/`user-select:none` para que no se arrastre la imagen; el círculo de **Reto** ahora usa `CAB.vsIcon` (las dos caras divididas) para representar el duelo.
- **Nav subido** (bottom 20px, no pegado al borde), más alto (padding 10px) e iconos más grandes (34px; avatar 60px). Wrap con más padding inferior.
- **Checkpoint**: máscara de degradado inferior en `.ckheroimg` (mask linear-gradient 74%→transparente) para ocultar el corte de la imagen.
- **Botones del input de agua centrados** (justify-content:center).
- **Tabs de comida icono-sobre-texto** (`.segfood` column, icono 20px).
- **Calcomanías compactas**: ya no ocupan todo el perfil — muestran 3 destacadas + "VER TODAS" para desplegar (`UI.calcoOpen`).
- **Ciclo (Cami)**: campo **FIN DEL SANGRADO** (`cfg.cycEnd`) en config; la duración menstrual se calcula con él; **recordatorio en Inicio** cuando faltan ≤3 días para el próximo período ("actualiza las fechas en tu perfil"). La nota/frase/recomendaciones por fase ya existían (cycleInfo).
- **5 nodos nuevos creados** (sin ejecutar): HOJA Andrés (model sheet, cabra oscura/musculosa/masculina) + HOJA Cami; checkpoint Andrés/Cami brazos cruzados (cuadradas); calcomanías CON cabrito (la hoja anterior no tenía al cabrito). Andy: **Andrés se personaliza más moreno (tan/marrón claro) y musculoso**.
- 355 pruebas en verde (chk40; chk33 ajustado a los iconos sólidos). Artifact republicado (REV 46); site/ sincronizado.
- **Pendiente**: ejecutar+integrar las hojas/checkpoint/calcomanías-con-cabrito + entreno/coach horizontal + food; completar el set sólido a TODOS los iconos; número 12→13; lista→expandir; tipografías.

**REV 47 (29/07/2026):**
- **Nav iconos más grandes** (39px).
- **Iconos rehechos** (Andy: no se entendían): `barbell` ahora es una mancuerna clara (5 rects: platos+barra), `food` un bowl con palillos. El resto del set sólido sigue.
- **SPACE reorganizado en PÁGINAS** (pedido de Andy): en "Character Model Sheet Development" se crearon 4 páginas nuevas — **Andrés** (54139604-…), **Cami** (6d87d912-…), **Recetas** (cd2fec63-…), **Iconos** (b99db8c3-…) — para manejar todo desde un solo documento.
  - **Recetas**: 7 nodos de proteínas en **3D estilo cabrita** (NO fotos — Andy corrigió la dirección): pollo, res, cerdo, pescado, huevo, yogur, arroz — solo la proteína, fondo gris para recorte.
  - **Andrés**: 15 nodos de sus ejercicios clave (PPL) con el personaje **oscuro/musculoso/masculino**, fondo night-gym azul, sujeto a la derecha + espacio de texto a la izquierda.
  - **Cami**: 17 nodos de sus ejercicios reales (Glúteo/Femoral, Pierna/Cuádriceps, Tren superior), night-gym dorado.
  - **Iconos**: 4 láminas de referencia de estilo (sólido con gradiente) por familia.
  - Todos con base consistente para generar más fácil después.
- **Pendiente**: Andy ejecuta las páginas → integro proteínas 3D en Recetas, ejercicios por perfil (exMedia), y uso las referencias de iconos para completar el set SVG; + lo ya en cola (entreno/coach horizontal, checkpoint brazos cruzados, calcomanías-con-cabrito, número 12→13, lista→expandir, tipografías).

**REV 48 (29/07/2026):**
- **Bases de consistencia en el space** (Andy: primero el mood/base): en las páginas **Andrés** y **Cami** se crearon 5 nodos FUNDACIÓN cada una (primer plano, plano general, expresiones, ángulos, outfit y props) que fijan el look&feel aprobado — camiseta/tank top, pesas 3D pero realistas, fondo night-gym azul (Andrés, moreno/musculoso) / dorado (Cami). Estos anteceden a los ejercicios para máxima consistencia.
- **Proteínas corregidas** (Andy: sin ojos, look thiings.co): en la página **Recetas** se crearon 2 nodos de TEXTO con la guía de estilo (clean 3D matte, isométrico, sombra suave, fondo crema #F5F2EC, SIN caras/ojos) + se re-crearon los 7 nodos de proteína en ese estilo (solo el alimento, sin ojos).
- **Perfil rediseñado**: hero combinado = avatar + nivel/XP + insights (peso, racha, trofeos) + tira de calcomanías destacadas con "ver todas" (`.calcostrip`/`.calcomini`/`.calcomore`); debajo, accesos en **2 columnas Progreso | Fotos** (`.pgrid2`/`.pcard`) con imagen de cabrita (andLift/cycFoli y tileFoto, con máscara inferior). El grid completo de calcomanías se despliega con VER TODAS.
- 355 pruebas en verde (chk41; chk30/35/37/40 ajustadas). Artifact republicado (REV 48); site/ sincronizado.
- **Pendiente**: Andy ejecuta las bases + ejercicios + proteínas 3D + hojas → integro todo (exMedia por perfil, recetas 3D, cabritas de progreso/fotos definitivas); completar iconos SVG; número 12→13; lista→expandir; tipografías.

**REV 49-50 (29/07/2026):**
- **REV 49**: fix del picker del avatar (había una regla `.avpop{width:168px}` vieja del menú modal que achicaba el popup y cortaba el 3er círculo; eliminada + clamp de posición dentro del viewport + círculos 62px). Agua: el número consumido más grande (`.wml` 34px). Artifact rev49.
- **REV 50 — iconos sólidos a TODA la app** (Andy: usar los del space): se completó el mapa `SOLID` con bell, egg, lock, moon, repeat, scale, search, share, syringe, target (con fill-rule evenodd donde hay huecos). Los glifos micro (chevL/chevR/x/plus/up/down) y los que necesitan cutout de línea (alert, info, ruler) siguen en stroke a propósito. 361 pruebas en verde.
- **Nota de plataforma**: al cerrar REV 50 el clasificador de acciones estuvo intermitente; site/ quedó sincronizado (REV 50), el republish del artifact quedó pendiente de reintento.
- **Imágenes**: artifact de REGLAS E INVENTARIO publicado (60f552fa-…) para que Andy verifique antes de generar. **Corrección del linking del space** (pedido de Andy): en páginas Andrés y Cami se instruyó crear un nodo MAESTRO (plano general, MUSCULOSO, SIN campana) y encadenar todos los demás nodos (base + ejercicios) desde él para consistencia. cami/andrés MAESTRO sin bell.

**REV 51 (29/07/2026):**
- **Proteínas 3D integradas en las categorías de recetas** (Andy: "algunas imágenes ya están, empieza por las recetas"): se recuperaron del space las 7 proteínas ejecutadas en estilo thiings.co (pollo, res, cerdo, pescado, huevo, yogur, arroz — matte, sin caras/ojos, fondo crema), se les quitó el fondo, se recortaron a 200px y se cuantizaron (~14-35 KB c/u, 234 KB total b64). Nuevo objeto `REC={}` con las 7 y mapa `CATPROT` (res/pollo/cerdo/pescado/huevo→su proteína; cena→arroz; snack→yogur).
- **Tarjeta de categoría rediseñada** (`.catcard2`): ahora muestra la imagen 3D de la proteína como héroe (62px con drop-shadow) + badge esquinero con ícono pequeño y cantidad (`.catbadge`) + label; conserva el gradiente de color por categoría. Reemplaza el ícono grande centrado anterior.
- 372 pruebas en verde (chk39 ajustada a catbadge/catprot; nuevo chk43 valida REC/CATPROT y el embebido). Artifact republicado (REV 51, mismo URL); site/ sincronizado.
- **Pendiente del space** (en curso este turno): re-cablear el grafo de nodos (MAESTRO→base→ejercicio, cada ejercicio a los 2-3 nodos que necesita, no todo al maestro) y crear los slots de cabrita por personaje (avatar, foto, check-in, checkpoint, estados dormido/mañana/hidratación/almuerzo/media tarde/celebración/racha; fases del ciclo de Cami). Regla vigente: crear nodos, Andy los ejecuta.

**REV 52 (29/07/2026):**
- **Imágenes de Andrés integradas desde el space** (Andy: "tomemos las de Andrés y reemplacemos en toda la sección de Andrés"). Se verificó primero que las páginas Andrés/Cami del space están bien cableadas (MAESTRO plano general → hojas base → cada nodo referencia solo lo que necesita; sin campana; Andrés tan/moreno, Cami crema/moño). Los nodos de Andrés ya tenían render, así que se recuperaron, se les quitó el fondo (estaban sobre gris #CCCCCC) y se embebieron reemplazando las claves exclusivas de Andrés: `avA`/`faceA` (avatar cara), `andBuff` (checkpoint brazos cruzados), `andLift` (barbell squat, columna Progreso del perfil), `entCurl` (hammer curls, tile de entreno), `celebA` (estado celebración). Las claves compartidas (tileFoto/tileCheck/medidas) se dejaron intactas para no mostrar a Andrés en la vista de Cami.
- **Calcomanías con cabrito**: la hoja 3×3 ejecutada en el space se cortó en 9 (flood-fill del gris desde los bordes para no borrar el elefante gris), se recortó y cuantizó cada sticker, y se reemplazaron las 9 claves `stk*` (moto, carro, elefante, camión, avión, ballena, trofeo llama, huellas, estrella) — mismo orden y significado, ahora con el cabrito interactuando con cada objeto y borde die-cut blanco.
- +576 KB de imágenes (archivo ~2.42 MB). 372 pruebas en verde. site/ sincronizado y artifact republicado (REV 52, mismo URL).
- **Pendiente**: hacer lo mismo con las imágenes de Cami (avatar, checkpoint, entreno, celebración, fases del ciclo) cuando Andy confirme que están ejecutadas; opcional: los 15 ejercicios de Andrés del space → `assets/ej/` (hoy son fotos reales en Netlify); el ajuste de cableado del primer plano de Cami quedó solo señalado, no ejecutado (Andy pidió no tocar).

**REV 53 (29/07/2026):**
- **Sesión de entreno en lista con expandir** (Andy): al iniciar una rutina ahora arranca en VISTA LISTA (`UI.sessList=true` en `goSession`), con filas compactas (`exRow`): número, nombre, series/última carga, y un check circular al final de la barra (verde si el ejercicio está completo, chevrón si no). Al tocar la fila se expande la tarjeta completa del ejercicio inline (`ACTIONS.exToggle`/`UI.exOpen`, con `exCard(...,false)` embebido y animación `exslide`). Se mantiene el toggle MODO FOCO/VER LISTA.
- **Calendario siempre abre en vista mes**: `ACTIONS.tab` ahora, si el destino es `agenda`, resetea `calView='mes'`, `calM=0`, `calSel/calDay=null`, `session=null` — sin importar dónde estabas.
- **Ícono de pasos** rehecho como huellas reales (elipses + dedos) en el mapa `SOLID`; antes era una silueta de piernas que no leía como "pasos".
- **Tamaños de imagen**: checkpoint del día → columna de la cabrita a ~1/3 del ancho (`grid-template-columns:minmax(116px,33%) 1fr`), imagen alineada abajo y con menos recorte de máscara; caja de entreno → imagen de 104→150 px; columnas Progreso/Fotos del perfil → imagen de 96→132 px, anclada arriba, menos recorte y `.pcard` más alto (150 px). Regla general del usuario: la imagen ocupa ~1/3 del ancho de la caja.
- **Check-in y foto del día por usuario**: se crearon variantes de Andrés (`tileCheckA`, `tileFotoA`, `medidasA`) desde los nodos ejecutados del space (check-in con cinta métrica full body; foto selfie), y los slots ahora conmutan `UID==='andres'?...A:compartida`. Cami conserva las compartidas hasta hacer su pase.
- 382 pruebas en verde (chk44 nuevo; chk20/chk23 ajustadas a las variantes per-user). Archivo ~2.53 MB. site/ sincronizado y artifact republicado (REV 53).
- **Pendiente / a confirmar con Andy**: (1) alcance de "las de los ejercicios" — las 49 fotos de `assets/ej/` son demostraciones reales; el space solo tiene 15 nodos de ejercicio de Andrés y 17 de Cami (llaves distintas), así que reemplazarlas todas por cabritas no calza 1:1. (2) Qué otros íconos "de la tarjeta después del hero" corregir además de pasos. (3) Pase completo de imágenes de Cami (avatar, checkpoint, entreno, celebración, fases del ciclo) cuando confirme que están ejecutadas.

**REV 54-55 (29/07/2026):**
- **Pase completo de imágenes de Cami** desde el space (avatar, checkpoint brazos cruzados `camCheck`, celebración, check-in/foto/medidas por usuario `tileCheckC`/`tileFotoC`/`medidasC`, las 4 fases del ciclo `cycMens/Foli/Ovul/Lute` y racha). Todas conmutan `UID==='andres'?...A:...C`.
- **Checkpoint del día**: la cabrita se acercó (recorte a la altura de la primera costilla vía `object-fit:cover;object-position:center 20%` con altura fija) para que se vea más grande sin cambiar el contenedor.
- **Íconos de proteína** (res/pollo/cerdo/pescado/huevo/cena) pasados a `SOLID` con siluetas claras (steak con hueco, muslo con hueso, hocico de cerdo con narices, pez, bol) — antes eran trazos abstractos.
- **Tarjeta coach de media tarde**: usaba una imagen vieja y cortada; ahora usa la racha nueva por usuario (`rachaA`/`rachaC`) con fallback, y `.coachimg` cambiada a `object-fit:contain` para que no se corte.
- **Nav con selector deslizante**: como el nav es persistente (render solo alterna `.on`), se añadió `.navind` (indicador absoluto) que se mueve con `transform:translateX(calc(var(--navi)*100%))` y transición suave; `navIndicator()` fija `--navi/--navop` en buildNav y en cada render.
- **Fotos**: las opciones (1 semana / 1 mes / 1 año / primera vs última / comparar 2 a mano / subir antigua) pasaron de chips a **cajitas** (`.optgrid`/`.optbox`) y debajo la **GALERÍA** (`#fgrid`).
- **Caja de entreno = ejercicio del día** (REV 55): `entrenoImg(routine)` elige push/pull/legs por perfil reutilizando renders de ejercicios ya ejecutados del space (Andrés bench=`entPushA`, pull-up=`entPullA`, legs=squat=`andLift`; Cami chest press=`entPushC`, legs=`camLift`).
- 405 pruebas en verde (chk45 nuevo; chk19/chk20 ajustadas a las cajitas). Archivo ~3.4 MB. Artifact republicado REV 54 y 55.
- **Nota sobre ejercicios**: el space YA tiene un nodo de cabrita para casi todos los ejercicios del app (llaves calzan 1:1 en Página 1: 31 de Andrés, 32 de Cami). Falta (a) confirmar cuáles están ejecutados y (b) el swap de las 49 fotos reales de `assets/ej/` por los renders de cabrita (operación aparte, archivos en Netlify, no embebida). Pendiente también: fondos `ph-*` de las tarjetas de rutina (aún cabrita vieja); animación deslizante en los segmentos internos (hoy hacen cross-fade porque se recrean por render).

**REV 56 (29/07/2026):**
- **Swap de imágenes de ejercicios** (Andy: "solo fotos, sin video"). Verificación previa: los 63 nodos de ejercicio del space (31 Andrés + 32 Cami) YA tienen render — nada por crear. Se mapeó cada llave del app a la creación del nodo de Página 1, se descargaron las 63, se recortaron a 480×480 jpg (~1.7 MB total) y se escribieron en `site/assets/ej/` (respaldo de las fotos reales en `site/assets/ej_realfotos_backup/`).
- **exMedia sin video**: se quitó el `<video>` overlay para que se vea la imagen fija de la cabrita en cada ejercicio.
- 405 pruebas en verde. **Importante**: `assets/ej/` solo se ve en la versión **Netlify** (el artifact de claude.ai solo publica el HTML); Andy debe desplegar `site/` para verlas.
- **Pendiente**: fondos `ph-*` de las tarjetas de rutina (aún cabrita vieja) y de los photocards de sesión; animaciones de ejercicio (mp4) quedaron fuera por decisión (solo fotos).

**REV 57 (29/07/2026):** barrido de "imágenes viejas" (fondos `ph-*` JPEG embebidos) + retos.
- **Tarjetas de rutina**: el thumb `ph-*` viejo se reemplazó por `.rthumb` (gradiente night-gym) + la cabrita nueva del tipo de rutina vía `entrenoImg(r)` (push/pull/legs por perfil). Movilidad usa `andLift`/`camLift`.
- **Tarjeta coach (cabClock)** y **check-in semanal** y **hero de pasos**: dejaron de usar `ph-*`; ahora son `.coachc` con cutout (coach: entrenoImg/racha/checkpoint según hora; check-in: `tileCheckA/C`; pasos: `rachaA/C`). `.coachimg` ya con `object-fit:contain`.
- **Retos**: hero `ph-retos` viejo reemplazado por `.retohero` con las **dos caras nuevas** (`faceA`/`faceC`) enfrentadas + "VS" + chip de **líder vigente** de la semana. En cada caja de reto (`.vsrow`) se añadió la **cara de cada uno a su lado** (`.vsface`).
- **Fotos**: `.optgrid` a **3 columnas** (2 filas), subtítulos ocultos por espacio.
- **Ícono de pasos** rehecho otra vez como dos huellas silueta (bola + talón) más legibles.
- **Íconos de comida**: se creó en el space de iconos (`a2602484…`) el nodo **"Iconos — Categorías de comida (7)"** (id 7200420a) en el estilo de línea gruesa del set, conectado a la Ref, **sin ejecutar** — Andy lo corre y luego se recortan e integran los 7 (res/pollo/cerdo/pescado/huevo/cena/snack).
- 405 pruebas en verde (chk20/24/25/28/44 ajustadas al nuevo markup). Archivo ~3.34 MB. Artifact REV 57.
- **Checkpoint del día**: confirmado que usa `andBuff`/`camCheck` (torso brazos cruzados) — correcto, no requiere ejecutar nada; si se veían "piernas" era caché.
- **Pendiente**: photocards `ph-*` restantes (banner de sesión de entreno, plan del día, recetas/mercado) e integrar los iconos de comida cuando se ejecuten.

**REV 58 (29/07/2026):**
- **Fix avatar en iOS Safari**: el botón `.navav` no dejaba usar el press-slide en Safari iOS. Se añadió `touch-action:none`, `-webkit-touch-callout:none`, `user-select:none` y `tap-highlight` transparente al botón y al `.avpop`/imágenes (el long-press disparaba el callout/scroll de iOS y cancelaba el gesto).
- **Checkpoint recortado al pecho**: se regeneraron localmente `andBuff` y `camCheck` recortando al 60% superior (cabeza + brazos cruzados + pecho, sin piernas) y `.ckheroimg` pasó a `object-fit:contain`.
- **Versus del reto (`vsIcon`)** recompuesto con las **dos caras nuevas** (avatares Andrés+Cami) — el círculo "Reto" del picker ya no usa la imagen vieja.
- **Minis del día-de-rutina**: dejaron de usar `ph-*`; ahora reusan el cutout nuevo del tipo de rutina (`.rmini` + `entrenoImg`).
- 405 pruebas en verde. Artifact REV 58.
- **Space (create-only, Andy ejecuta)**: (1) **Iconos de comida en la página correcta** — se creó `ICON — categorías de comida (7)` (id 0add202c) en la página **Iconos** del space de personajes (estilo sólido con gradiente, igual al set del app). El nodo que se creó antes por error en el space "Icons Cabri" (7200420a) se puede borrar. (2) **Banners horizontales de rutina** dedicados: Andrés (Push/Pull/Legs) y Cami (Tren superior/Glúteo-femoral/Cuádriceps), 16:9 night-gym, sujeto a la derecha con copy space a la izquierda, conectados a cada MAESTRO. Al ejecutarlos se integran como fondo de las tarjetas de rutina (reemplazan el cutout readaptado actual).
- **Pendiente**: ejecutar en el space los banners de rutina + el nodo de iconos de comida, y luego integrarlos (recortar los 7 iconos y poner los banners en `.rthumb`).

**REV 59 (29/07/2026):**
- **Checkpoint** con desvanecido inferior (mask-gradient) para que el corte al pecho no se sienta abrupto.
- **Versus del reto (`vsIcon`)** rehecho como **media cara Andrés | media cara Cami** (split vertical con divisor), en vez de dos caras superpuestas.
- **Banners horizontales de rutina integrados**: se recuperaron y ejecutaron los 6 nodos del space (Andrés Push/Pull/Legs, Cami Tren superior/Glúteo-femoral/Cuádriceps), se embebieron (`banPushA…banCuadC`, ~178 KB jpg) y `routineBanner(r)` los pone como fondo full-bleed 16:9 (`.rbanner`) en las tarjetas de rutina; Movilidad conserva el cutout.
- **Íconos de comida como imagen**: se ejecutó el nodo `ICON — categorías de comida (7)` de la página Iconos, se recortaron los 7 (flood-fill del fondo oscuro), se embebieron (`fic_*`) y un helper `catIco()` + mapa `CATIMG` reemplazan los SVG en las categorías/badges/chips/mercado.
- **Ícono de app**: (interino) se generó local un ícono con las dos cabritas (caras + glow azul/dorado) en `icon-192/512.png` (SandyApp + site). Andy pidió que sea **mitad y mitad con glow, generado en Magnific** → se creó el nodo `APP ICON — dúo split (Andrés | Cami)` (create-only, conectado a ambos MAESTRO) en la página Iconos; al ejecutarlo se descarga y reemplaza el ícono.
- 423 pruebas en verde (chk46 nuevo). Archivo ~3.70 MB. Artifact REV 59.
- **Pendiente**: (1) ejecutar el nodo del ícono de app dúo-split e integrarlo; (2) animación de "deslizador" en los segmentos internos (`.seg`) — el nav ya desliza, pero los segmentos se recrean por render y no animan entre estados sin usar View Transitions (queda como mejora aparte).

**REV 66-70 (29-30/07/2026):** tanda grande de UX + features.
- **REV 66**: comparación de fotos con pie de **fecha completa + peso + pasos/entreno** y delta de kg (`fotoStats`/`fmtLong`); padding de la rejilla de medidas (clase `mcells`); check del ejercicio al final y alineado; ícono de filtro de recetas → embudo (`filter`).
- **REV 67**: **tabla compacta de series** (Set/Anterior/kg/Reps/✓) con descanso entre filas y "+Agregar serie · m:ss", íconos de progreso/cambiar arriba de la tarjeta; **Records Personales por ejercicio** (peso más pesado, mejor 1RM, mejor volumen de serie y de sesión) en la vista de progreso.
- **REV 68**: detalle de receta con **bloques por persona** (color + chips de macros P/C/G/kcal/costo); **duración del entreno** guardada en la sesión (`min` desde `draft.t0`) y mostrada en actividad reciente.
- **REV 69**: **caja rotativa del home** (`homeRotator`/`HOMEFEED`): rota entre pendiente del día, frases motivacionales, versículos (Reina-Valera dominio público, editables para pegar TPT) y datos útiles; **cabrita durmiendo** en el coach card de la noche (`dormidoA`/`dormidoC`). Nodo `APP — cabrita lectora` creado en el space (create-only).
- **REV 70**: **isla flotante** de la rutina en curso (`updateIsland`, `#island`) para volver al entreno desde cualquier parte; **avisos al abrir** (`partnerAlerts`) si el otro propuso premio/reinicio de reto o ideas (banner en home + toast); **imagen del ejercicio en círculo** en la lista de la sesión.
- 437 pruebas en verde (chk46-50). SW cache v14. Todo publicado en el artifact y en `site/` (git → Netlify).
- **Space create-only pendiente de ejecutar por Andy**: `APP — cabrita lectora` (para el rotador; mientras usa el avatar). Ya ejecutados e integrados: dúo-split app icon, banners de rutina, íconos de comida, dormido.

**Nota MCP**: quedó registrado el servidor `21st` (21st.dev, componentes React/Tailwind) en la config local de Claude Code; requiere exportar `API_KEY_21ST` en el shell para autenticar. Útil para el port a Next.js, no para el prototipo vanilla.

### Notas de producto
- Todo en español, unidades métricas, COP.
- Tono: directo y práctico, sin sermones. Explicar el porqué en 1–2 líneas.
- La app no da consejo médico; ante síntomas o temas clínicos, remitir a profesional.
- Regla de oro visible en el corte: **si las cargas se mantienen, el músculo se queda.**
