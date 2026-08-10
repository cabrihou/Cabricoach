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

