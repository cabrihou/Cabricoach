# Carga por músculo · de dónde salen los números

Investigado el 09/08/2026. Vive en `coach-afc-v2.html` como `EJ_PATRONES` (reparto por
patrón de movimiento) y `MUSC_VOL` (volumen semanal de referencia).

## La idea

Un ejercicio no entrena "pecho": reparte el trabajo. El press de banca carga sobre todo el
pectoral, pero el tríceps y el deltoide anterior también reciben, y eso cuenta como volumen
aunque uno no los haya entrenado aparte. Por eso el volumen se mide en **series efectivas**:
cada serie se reparte entre los músculos según cuánto participan.

Ejemplo real: 3 series de banca + 3 de inclinado + 3 de aperturas son 9 series de pecho,
pero para el pectoral cuentan **6,1** y el tríceps se lleva **0,9** de regalo.

## Reparto por patrón (`EJ_PATRONES`)

38 patrones de movimiento, cada uno suma 100. Sale de estudios de EMG normalizados a MVIC
(contracción isométrica máxima voluntaria), principalmente Boeckh-Behrens & Buskies y las
tablas de involucramiento de ExRx.

Los ejercicios se asignan a un patrón por id (los de las rutinas propias) o por lo que diga
el nombre (`EJ_PATRON_NOM`, ~45 reglas), que es lo único que traen los importados de Strong.
Cobertura: **273 de 300** del catálogo. Los que quedan fuera son estiramientos y un
olímpico raro; la app los lista como "no supe repartir" en vez de callarlos.

### Correcciones propias sobre la fuente

**El bíceps en jalones y remos.** En jalón vertical, remos y muscle up la recopilación no
lo contaba. Se le devolvió su 15-20%. Sin eso, el volumen de bíceps de quien entrena espalda
salía a la mitad del que realmente recibe, y la app le habría recomendado añadir curl sin
necesidad.

**Aductor, abductor y lumbar** (encontrado auditando las rutinas reales, 09/08). El aductor
de máquina caía en el mismo saco que el hip thrust y contaba **85% glúteo**, cuando trabaja
la cara interna del muslo. Ahora hay tres patrones separados:

| Patrón | Reparto | Ejercicios |
|---|---|---|
| `hip_thrust` | glúteo 85 · isquio 10 · cuádriceps 5 | hip thrust, puente |
| `abduccion_cadera` | glúteo 90 · aductor 10 | abductor de máquina, patada de glúteo |
| `aduccion_cadera` | **aductor 90** · glúteo 10 | aductor de máquina |
| `extension_lumbar` | lumbar 45 · glúteo 35 · isquio 20 | hiperextensiones, superman |

Antes, la hiperextensión también contaba como peso muerto rumano.

**Press con agarre cerrado** (`press_cerrado`: tríceps 45, pectoral 40) se separó del banca
normal, donde el reparto es al revés.

Lo más discutible son los olímpicos (cargada, arrancada): ahí el reparto depende mucho de la
técnica y de la carga relativa.

## Volumen semanal de referencia (`MUSC_VOL`)

En series efectivas por semana, de Renaissance Periodization y literatura de hipertrofia:

- **MEV**: mínimo para crecer
- **MAV**: punto óptimo
- **MRV**: máximo que se recupera

Varía mucho por persona (años de entreno, sueño, comida): son referencias, no leyes, y la
app lo dice. El deltoide anterior lleva MEV 0 a propósito: se llena solo con cualquier press.

## Fuentes

- [Cinco inclinaciones de banco: EMG de pectoral, deltoide anterior y tríceps](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7579505/)
- [ExRx.net · base de ejercicios con músculo objetivo y sinergistas](https://exrx.net/WeightExercises/GluteusMaximus/BWSquat)
- [Renaissance Periodization · training volume landmarks](https://rpstrength.com/blogs/articles/training-volume-landmarks-muscle-growth)
- [Activación del glúteo mayor en la sentadilla trasera (JSCR)](https://journals.lww.com/nsca-jscr/fulltext/2021/01000/activation_of_the_gluteus_maximus_during.3.aspx)
- [EMG y cinética: peso muerto convencional vs rumano](https://www.sciencedirect.com/science/article/pii/S1728869X18301291)
- [EMG del deltoides en distintos ejercicios de hombro](https://minds.wisconsin.edu/bitstream/handle/1793/70129/sweeney_samantha_thesis.pdf)
- [Fondos en banco, barra y anillas: cinemática y activación](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9603242/)
- [Actividad EMG en el peso muerto y sus variantes (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0229507)
- [Pullover: efecto sobre pectoral mayor y dorsal ancho](https://www.researchgate.net/publication/51695295_Effects_of_the_Pullover_Exercise_on_the_Pectoralis_Major_and_Latissimus_Dorsi_Muscles_as_Evaluated_by_EMG)

## Baremos de fuerza relativa ampliados

`FZA_STD` cubre los nueve básicos. `FZA_STD2` (09/08/2026) añade **22 ejercicios más**
para poder dar nivel también a lo que no es un básico: press inclinado, elevación lateral,
pájaro posterior, remo con mancuerna, remo en polea, encogimiento, curl martillo, tríceps en
polea, press francés, sentadilla frontal, hack, extensión de cuádriceps, curl femoral, peso
muerto rumano, zancada, búlgara, gemelo, abductor, aductor y face pull.

Se llega a ellos por **patrón de movimiento** (`FZA_PAT2`), así cubren también los
importados de Strong, con overrides por nombre (`FZA_NOM2`) donde el patrón se queda corto:
el face pull comparte patrón con el pájaro posterior pero mueve mucho menos peso, y con la
tabla equivocada un intermedio salía élite.

**Se excluyeron a propósito** flexiones, remo invertido y muscle up: se registran sin kilos,
así que no hay ratio que calcular.

Los baremos de mancuerna están normalizados al **total de las dos**. Por eso importa marcar
si un peso es por lado (`S.cfg.porLado`): un curl de 27 por brazo son 54 kg de trabajo, y sin
ese dato el nivel sale a la mitad y el tonelaje también.

Fuentes: [StrengthLevel](https://strengthlevel.com/strength-standards),
[ExRx](https://exrx.net/Testing/WeightLifting/StrengthStandards),
[Symmetric Strength](https://symmetricstrength.com/standards),
[Fitness Volt](https://fitnessvolt.com/strength-standards/).

## Exigencia por implemento y esfuerzo de la carrera

Tres series de dominadas en anillas no cuestan lo mismo que tres en barra fija. `EX_ESFUERZO`
guarda un factor por implemento (referencia 1,00 = barra), de estudios de EMG que comparan
activación de estabilizadores:

| Implemento | Factor |
|---|---|
| Anillas | 1,28 |
| Suspensión (TRX) | 1,18 |
| Kettlebell | 1,14 |
| Mancuerna | 1,13 |
| Peso corporal | 1,12 |
| Banda | 1,03 |
| **Barra** | **1,00** |
| Polea | 0,92 |
| Máquina | 0,85 |
| Smith | 0,80 |

Trabajar un lado a la vez suma otro **+0,18** (`EX_UNILAT_EXTRA`).

**El factor multiplica el esfuerzo, no las series.** Las series efectivas se dejan como están,
porque es una medida estándar y compararla con las referencias de volumen exige que lo sea. La
exigencia se muestra aparte: "hiciste 6 series, equivalen a 6,4 de barra".

### Correr

`CORR_MET` son los MET por ritmo del **ACSM Compendium of Physical Activities**, y de ahí salen
las kcal y una carga sRPE comparable con la de pesas.

La primera recopilación traía los MET **inflados un 40% en la zona rápida**: daba 828 kcal en
6 km para 90 kg. Contrastado contra la regla de ~1 kcal por kg y por km (540 kcal), estaba
claramente mal. Con la tabla del compendium da 557, que sí cuadra. Verificado en cuatro ritmos:
6 km/34 min → 557 (regla 540) · 10 km/60 min → 945 (900) · 5 km/22 min → 426 (450) ·
3 km/20 min → 296 (270).

Fuentes: [ACSM Compendium](https://pacompendium.com/running/),
[Foster 2001 · sRPE](https://pmc.ncbi.nlm.nih.gov/articles/PMC5294946/),
[EMG suspensión e inestabilidad](https://pubmed.ncbi.nlm.nih.gov/38288256/).

## Revisión de repartos y volúmenes (10/08/2026)

Dos problemas encontrados usándolo:

**Faltaban sinergistas.** La sentadilla no contaba lumbar ni abdomen, el peso muerto no
contaba trapecio ni antebrazo (el agarre), los jalones y remos no contaban antebrazo, y el
press militar no contaba trapecio ni core. Se añadieron a 24 patrones, siempre sumando 100.
Resultado: el press militar reparte ahora **deltoide anterior 42, tríceps 28, deltoide
lateral 20, trapecio 6, abdomen 4**, y una semana normal mueve 14 músculos en el mapa en vez
de 9.

**Los mínimos estaban altos.** Con el volumen indirecto mal contado y un MEV alto, casi todo
salía "por debajo del mínimo" siempre, que es ruido y no información. Ajustados a las guías:

| Músculo | Antes (MEV) | Ahora | Por qué |
|---|---|---|---|
| Deltoide lateral | 10 | 6 | el MEV típico está en 6-8 |
| Trapecio | 8 | 4 | se llena casi solo con remos y peso muerto |
| Glúteo | 8 | 4 | idem con sentadilla y peso muerto |
| Cuádriceps | 10 | 8 | |
| Bíceps, tríceps, dorsal, deltoide posterior | 8 | 6 | reciben mucho volumen indirecto |
| Isquiotibial | 8 | 6 | |
| Antebrazo | 4 | 2 | ahora lo alimenta el agarre de todos los jalones |

También subieron algunos techos (MRV) donde estaban cortos: pectoral y dorsal a 22, abdomen
a 16, lumbar a 14, antebrazo a 16.

## Los ejercicios que miden cada grupo (`FZA_GRUPOS`)

Lista cerrada, definida a mano por el dueño: son los que **de verdad miden** la fuerza de ese
grupo, no todo lo que lo roza.

| Grupo | Ejercicios |
|---|---|
| Espalda | Remo con barra · Jalón al pecho · Dominada · Dominada en anillas |
| Pecho | Press banca · Fondos lastrados · Fondos en anillas |
| Tríceps | Skullcrusher · Fondos lastrados · Fondos en anillas |
| Bíceps | Curl con barra · Curl con mancuerna · Curl preacher |
| Hombro | Press militar con barra · con mancuerna · en máquina |
| Pierna | Sentadilla · Hack squat · Prensa · Hip thrust |

Cada entrada lleva varios ids alternativos (el mismo ejercicio según venga de las rutinas
propias o importado de Strong) y declara si el peso apuntado es **lastre** y si es de
**anillas**. Los que no has hecho salen igual, en gris, para que se vea qué falta.

## Fiabilidad de cada baremo (`FZA_FUENTE`)

Un "eres avanzado" sin respaldo no vale nada, así que cada ejercicio dice de dónde sale su
tabla y cuánto hay que fiarse:

- **alta** (`sl`): directo de Strength Level, 195 millones de levantamientos. Todos los de
  carga externa: press, remos, jalón, curl, sentadilla, hack, prensa, hip thrust.
- **media** (`est`): dominadas y fondos lastrados. La fuente da el lastre en **libras
  absolutas**, no un ratio; convertirlo a `(peso corporal + lastre) / peso corporal` obliga a
  asumir un peso corporal medio, así que el número se mueve según ese supuesto.
- **baja** (`ext`): anillas. **No hay datos**. Se usa la tabla de la versión en barra fija y
  se avisa de que en anillas el mismo peso es más difícil, así que el nivel real es
  probablemente mayor. La literatura sugiere entre 1,3 y 1,5 veces más exigente pero **sin
  consenso medible**, así que no se aplica un factor inventado.

### Qué peso cuenta en cada caso

En press, remos, curl y prensa cuenta solo la carga externa. En **dominadas y fondos** cuenta
el peso corporal del día **más el lastre**, porque es lo que se mueve de verdad. En los de
mancuerna, si está marcado "por lado" se suman las dos.

### Sobre ajustar por porcentaje de grasa

**No existe ningún estándar serio que lo haga.** Todos comparan contra el peso total. Dos
personas del mismo peso con distinta composición dan el mismo ratio aunque su fuerza por kilo
de músculo sea distinta: es una limitación real del método, y la app lo dice en pantalla en
vez de inventar un ajuste.

Fuente verificada el 10/08/2026: [Strength Level](https://strengthlevel.com). No se pudo
acceder a ExRx ni Symmetric Strength (403), así que los números descansan sobre una sola
fuente y eso también está declarado.

## No todo el peso corporal cuenta (`EX_FRAC`)

En una dominada o un fondo cuelgas el cuerpo entero, pero en un **curl en anillas**, un remo
invertido o una flexión el cuerpo va inclinado y solo mueves una parte, que además cambia con
el ángulo. Contarlos al 100% daba disparates: un curl en anillas salía como levantar **114 kg**
y ponía el bíceps en Élite.

| Patrón | Fracción del peso corporal |
|---|---|
| Dominada, fondo, muscle up, colgarse | 1,00 |
| Palanca frontal | 0,60 |
| Flexión de pecho | 0,64 |
| Remo invertido | 0,55 |
| Apertura en anillas | 0,50 |
| Tríceps en anillas | 0,45 |
| Plancha | 0,45 |
| **Curl en anillas** | **0,40** |

Con eso el curl en anillas pasa de 114,5 a **49,3 kg** de 1RM, que es lo razonable. En los que
dependen mucho del ángulo se usa el extremo conservador.

## Descartar un registro del cálculo

`S.cfg.fzaFuera` guarda ejercicios que no cuentan para el nivel, sin borrar el historial: un
peso apuntado en otra unidad, un ejercicio que no mueve tu peso entero, una serie mal
registrada. Se descarta desde la fila abierta y se recupera con un botón. Antes, un registro
erróneo que te ponía en Élite se quedaba ahí sin forma de corregirlo.

## El carro de la máquina (`S.cfg.tara`)

Las máquinas de discos —hack squat, prensa, press de hombro *plate loaded*— llevan un carro
que **ya pesa por sí solo**, entre 15 y 45 kg según el modelo. Contando solo los discos, el
1RM sale corto: en un hack squat de 140 kg con carro de 40, el 1RM pasa de **177,3 a 228 kg**.

Como el peso del carro cambia de gimnasio a gimnasio y de modelo a modelo, no se puede
adivinar: lo pone el dueño desde la ficha del ejercicio, con chips de los valores habituales.
Por defecto es **cero**, porque quedarse corto es mejor que inventar un número. El detalle de
"de dónde sale tu número" lo dice cuando está puesto: *"Más los 40 kg del carro: 180 kg"*.


## Nivel de fuerza: qué se aplicó del pliego (REV 179)

Ya estaba antes de esto:

- **Ratio contra peso corporal con umbrales por ejercicio y por sexo.** `FZA_STD` y `FZA_STD2`
  llevan dos arrays: `a` (Andrés) y `c` (Cami). No es un multiplicador plano: son las tablas
  femeninas de Strength Level. Salen entre 60 y 75% del hombre en tren superior y entre 75 y
  100% en dominantes de cadera, que es lo que pasa de verdad (en hip thrust la mujer está
  a la par). Los umbrales viven como datos, no repartidos por el código.
- **Progreso dentro del nivel.** "Camino a Avanzado, 68%", interpolación lineal entre el
  umbral actual y el siguiente.
- **El nivel nunca baja.** `fzaMejor1RM` recorre todo el historial y se queda con el mejor,
  así que dejar de entrenar no degrada a nadie.

Lo que se agregó ahora:

- **Categorías de ejercicio.** `FZA_SECUNDARIO` marca los aislados (curl, elevación lateral,
  pájaro, tríceps en polea, encogimiento, extensión, curl femoral, gemelo, abductor, aductor,
  zancada, búlgara). Esos ya no reciben etiqueta de nivel: la tarjeta dice **tu récord** y
  **cuánto subiste desde la primera vez**. Decir que 16 kg de curl predicador es "avanzado" es
  inventarse un dato que no existe a nivel poblacional. El nivel de un grupo tampoco lo puede
  marcar un accesorio: `fzaGrupo` solo mira los calibrados.
- **Los dos ejes, a la vista.** `fzaScoreMixto` da `rel` (ratio contra tu peso), `abs`
  (qué tan raro es ese peso, ver abajo) y `mix`
  = 0.7·rel + 0.3·abs, con los pesos en `FZA_MEZCLA`. `fzaGlobal` promedia los calibrados y
  `fzaGlobalHTML` pinta el bloque que abre la sección: **nivel global** con su porcentaje al
  siguiente y, debajo, **fuerza relativa** y **fuerza total** en dos cajas separadas con su
  propio nivel y su propia barra. No se fusionan en la etiqueta de cada ejercicio: ahí manda
  la relativa y el absoluto sale como cápsula solo cuando difiere. Un tipo de 60 kg con banca
  de 90 y uno de 120 con banca de 150 no son comparables con un solo número.
  El segundo eje **no** es "el mismo peso en un cuerpo de referencia", que era un atajo. Es
  **cuánta gente que entrena mueve esos kilos**, sin mirar la báscula. Se calcula así:

  1. Los umbrales de la tabla **son percentiles** de la gente que entrena, así los publica
     Strength Level: Novato el 20%, Intermedio el 50%, Avanzado el 80%, Élite el 95%. Con eso
     `fzaPctlRatio` lee cualquier ratio como percentil, interpolando entre umbrales y con una
     cola exponencial por encima de Élite.
  2. Para pasar de ratio a kilos sueltos, `fzaPctlAbs` integra ese percentil sobre la
     distribución de pesos corporales de la población que entrena (`FZA_PESO_DIST`, normal de
     80 ± 13 kg en hombre y 64 ± 12 en mujer, en pasos de 0.125 sigma entre ±2.5): para cada
     peso posible, qué fracción de gente de ese peso mueve esos kilos. La suma ponderada es el
     percentil absoluto.
  3. `fzaUnoDeCada` lo traduce a lenguaje llano: "1 de cada 5", "la mayoría llega".

  Contraste con datos reales de Cami (59,5 kg): hip thrust de 160,3 kg sale relativo Avanzado
  (percentil 84) y en kilos "1 de cada 5"; press banca de 23,8 kg sale Principiante y "la
  mayoría llega". Los dos números conviven en pantalla: la etiqueta de nivel de siempre y la
  rareza del peso.
- **Sin datos recientes.** Si el mejor 1RM tiene más de 60 días (`FZA_VIEJO`), sale una cápsula
  que lo dice. Se marca, no se degrada.
- **Guardia de déficit.** `fzaDeficitGanancia` cruza el peso con las cargas: si bajaste 1 kg o
  más en 8 semanas y el mejor 1RM se sostuvo, la sección lo celebra en voz alta con el ratio
  antes y después. Es progreso que no se ve en la barra.

Pendiente y a propósito: el cabrito no cambia de forma según el nivel. Generar variantes en
Magnific cuesta créditos y solo se hace cuando Andy lo pide.

## De qué serie sale el nivel (REV 185)

Dos lecturas legítimas del mismo historial, y ninguna es la correcta siempre:

- **Tope histórico**: el mejor 1RM estimado de todo el historial. Es tu marca y no se borra
  nunca. El problema es que una serie vieja con técnica floja se queda mandando para siempre.
  Caso real: 130 kg × 7 con rebote en mayo dan 160,3 kg estimados y pesan más que 120 × 7 al
  fallo bien controladas en agosto, que dan 148,0. La segunda representa mejor la fuerza de hoy.
- **Lo más reciente**: la mejor serie de la última sesión registrada de ese ejercicio. Refleja
  lo que mueves hoy con la técnica de hoy, y se corrige sola.

Y una tercera, que es el punto medio:

- **Últimas 4 semanas**: la mejor serie de los últimos 28 días. No arrastra una serie de hace
  un año ni se desploma porque la última sesión cayera en fatiga o en semana de descarga.

El modo vive en `S.cfg.fzaBase` (`max` por defecto) y se elige en el bloque de Tu nivel global.
`fzaLecturas(id)` calcula **las dos de una sola pasada** y `fzaMejor1RM` devuelve la que manda
con `lecturas` pegado, así que la UI siempre puede mostrar la otra:

- En la tarjeta de ejercicio, una cápsula gris con la lectura que no se está usando
  (`tope 160,3 kg` cuando manda la reciente, `hoy 148,0 kg` cuando manda el tope).
- En "De dónde sale tu número", las dos lado a lado con su peso, sus repeticiones y su fecha,
  resaltada la que manda.

Cambiar de modo **no borra nada**: son tres lecturas del mismo historial, no tres historiales.

## La sesión de PR

`fzaPRPlan(x, pc)` arma el intento y la aproximación. El objetivo es el 1RM del siguiente nivel
si está a tiro (hasta un 6% por encima de lo que ya mueves); si está más lejos, un PR de
**+2,5%**, que es un salto que se logra en una sesión buena sin jugarse la semana. Todo se
redondea a la placa de 2,5 kg, porque un número que no se puede cargar no sirve de nada.

- **El intento**: un single al objetivo, y al lado el equivalente en triple
  (`objetivo / (1 + 3/30)`, Epley al revés) para quien no quiere ir a una repetición.
- **Cómo llegar**: rampa de 40% × 5 → 55% × 4 → 70% × 3 → 80% × 2 → 88% × 1 → intento. Sube
  rápido y llega fresco; una aproximación larga se come el PR.
- **Cuándo**: de primero en la sesión, con 48 a 72 horas desde la última carga de ese grupo, y
  con 3 a 5 minutos entre las tres últimas. Si `isDeload()` dice que la semana es de descarga,
  lo advierte en amarillo.
- **Qué hacer con el resultado**: si sale con dos repeticiones de sobra, +2,5 a 5 kg y repetir;
  si se pega en la mitad, parar. Un fallo no suma y cuesta el resto de la semana.

Vive dentro de la escalera de cada ejercicio, debajo de "De dónde sale tu número", así que
cambia solo cuando cambia la lectura que manda.
