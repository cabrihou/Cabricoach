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
