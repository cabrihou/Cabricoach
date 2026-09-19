# Plan: etapas, checkpoints y reorganización de Medidas

> **EJECUTADO el 19/09/2026 en la REV 214** (sin commitear, sin desplegar). Este
> documento se conserva como el porqué de cada decisión; el qué y el dónde están en
> `docs/MAPA.md` (secciones PL, MD, IM, K0).
>
> Análisis del 19/09/2026. Insumo: el documento de Andy
> "Proyecciones por etapas y checkpoints semanales" (bioimpedancias Biody Xpert del
> 15/09/2026). Estado del archivo: REV 213, sin cambios sin commitear.

## 0. Antes que nada: el archivo

El documento dice `coach-afc.jsx`. Ese es el prototipo React de julio que vive en
`archivo/` y está fuera de git. La app viva es `coach-afc-v2.html`. Todo lo de aquí
va sobre ese archivo.

## 1. Decisiones que Andy ya tomó (19/09/2026)

1. **Las kcal**: la app debe tener el conocimiento del plan y decidir en consecuencia.
   No copiar las cifras del documento a mano: reproducirlas con el motor.
2. **La meta**: las etapas reemplazan la meta vieja (86,6 kg fase 1 / 89 kg fase 2).
3. **Ubicación**: vista propia para el plan, con el semáforo de la semana dentro de
   Check-in.
4. **Pasos de Cami**: calcular la meta del historial real de las últimas 4 semanas.
5. **Navegación de Medidas**: portada con lista de destinos rotulados, y salto entre
   hermanos por hoja inferior. Nada de pestañas con solo iconos.
6. **Acceso**: Medidas pasa a ser vista propia única y deja de ser grupo de Progreso.

## 2. Lo que encontré al cruzar el documento con la app

### 2.1 Las fechas de checkpoint son lunes, no domingos

`15/09/2026` es **martes**, no lunes. Y de las fechas listadas como domingos, casi
todas son lunes: 21 sep, 28 sep, 5 oct, 12 oct, 19 oct, 26 oct, 2 nov, 9 nov, 16 nov y
23 nov caen en lunes. Las únicas que sí son domingo son 15 nov y 29 nov.

La regla del documento es clara ("check-in todos los domingos") y la app ya está
anclada al domingo (el recordatorio de check-in es `days:[0]` y la vista lo dice).

**Propuesta**: generar los domingos reales desde el **20/09/2026**. El plan no cambia,
se corre un día, y todo encaja: etapa 1 de Andrés da 6 domingos (el documento lista 6),
etapa 1 de Cami da 11 (lista 11), etapa 2 de Andrés da 3 (lista 3), etapa 2 de Cami da
5 (lista 5) y el volumen da 16 (el documento pide "la tabla de 16 domingos"). La semana
de descarga sigue cayendo en la semana 4.

### 2.2 La masa magra del Biody no cuadra, y no importa

El reporte dice magra (MLG) 71,1 kg, pero 89,7 menos 13,4 de grasa son **76,3**. Biody
reporta varias masas y la MLG no es la masa libre de grasa. La app calcula
`peso × (1 − grasa%)`, o sea 76,3.

Y ahí está lo bueno: con 76,3 kg de masa libre de grasa, el **12,5% cae exactamente en
87,2 kg**, que es la cifra de salida del documento. Con Cami igual: 56,7 × (1 − 0,294)
= 40,0 kg, y al **26% da 54,1 kg**, otra vez la cifra del documento.

**Conclusión**: no hay que escribir los pesos objetivo a mano. Basta con fijar el **%
de grasa de salida de cada etapa** y el motor que ya existe (`metaFases`) produce el
peso solo, con la magra real de cada semana. El 71,1 se guarda como dato del reporte,
no se usa para calcular.

### 2.3 Las calorías del documento salen solas de la TMB medida

Este es el hallazgo que hace posible lo que pidió Andy. La TMB medida de Andrés es
1.981 kcal. Con factor de actividad 1,45 (entrena 4 veces por semana y camina 8 a 10k):

| Etapa | Gasto estimado | Ajuste | Resultado | El documento dice |
|---|---|---|---|---|
| 1 · cut | 2.870 | −440 (son los 0,40 kg/sem) | 2.430 | 2.400 |
| 2 · mantenimiento | 2.835 | 0 | 2.835 | 2.700 → 2.800 |
| 3 · volumen | 2.845 | +275 | 3.120 | 3.050 a 3.100 |
| 4 · mini cut | 2.900 | −440 | 2.460 | 2.500 |

Las cuatro caen dentro de 50 kcal. Es decir: **el plan es internamente coherente y el
motor puede calcularlo** en vez de copiarlo, que es justo lo que pidió Andy. La ventaja
real es que sigue siendo verdad cuando el peso cambie: en marzo de 2027, a 91,5 kg, el
número se recalcula solo.

**Lo que esto le cambia hoy a Andrés**: su gasto está anclado en una estimación vieja
(2.650 kcal a 94,4 kg), así que la app le está dando **~2.230 kcal**. Con la TMB medida
pasa a **~2.430**. Son 200 kcal más al día desde el día que se despliegue, y reescala
recetas, reparto por comidas y mercado. No es un efecto lateral: es lo que dice el plan.

**Cami no se mueve**: su etapa 1 declara exactamente el déficit que ya tiene (330 kcal),
así que su número queda idéntico al de hoy. Etapa 2 son +150 y etapa 3 mantenimiento,
tal como pide el documento.

### 2.4 Creatina: la dosis de Andrés está mal en la app

El documento dice Andrés 5 g y Cami 3 g. La app tiene 3 g para los dos (el comentario
del código dice 5 y el dato dice 3). El agua asociada también se corrige a los rangos
del documento: 0,8 a 1,2 kg él, 0,4 a 0,7 ella.

### 2.5 Lo que ya existe y no hay que construir

- Vista de Check-in con formulario (peso promedio automático, grasa %, medidas,
  adherencia, energía, sueño, notas y foto), tabla de evolución y gráficas.
- Sistema de medidas por cadencia, Navy, proporciones, asimetrías y mapa corporal.
- Motor de creatina: fecha de arranque, saturación, agua estimada y avisos.
- `metasDe` como **único** surtidor de kcal y macros: un solo punto donde enganchar
  las etapas.
- Meta de peso derivada de la masa magra real (`metaFases`, `metaCard`).

Lo que falta: la estructura de etapas, los checkpoints, el semáforo, la pausa de
creatina, los rescans y **un sitio donde guardar un BIA completo**.

## 3. Parte A · El motor de etapas (lo que pidió el documento)

### 3.1 Modelo de datos

Cada etapa declara **qué hace con el cuerpo**, no cuántas kcal se comen:

```
{k, n, nombre, ini, fin, tipo:'cut'|'mant'|'volumen',
 ajuste: kcal/día contra mantenimiento,   // de aquí salen las calorías
 prot, protPiso, fat,
 proy:{base, ritmo, tol} o {rango:[min,max], tope},  // el peso esperado
 salida:{pct, kg},                         // el % manda, el kg es consecuencia
 entreno, pasos, notas}
```

Etapas de Andrés: cut (15 sep a 26 oct, −0,40 kg/sem, salida 12,5%), mantenimiento
(27 oct a 15 nov, con rebote de glucógeno esperado), volumen de piernas (16 nov a 8 mar,
+0,25 kg/sem) y mini cut (9 mar a 26 abr, −0,40 kg/sem, salida 12 a 13%).

Etapas de Cami: cut (15 sep a 29 nov, −0,25 kg/sem, salida 26%), mantenimiento de
diciembre (rango 54,0 a 54,5), fuerza de tren superior (4 ene a 28 mar, rango 54 a 55,5,
donde **el progreso se mide en cargas y no en peso**) y la decisión del 29 mar.

### 3.2 Calorías

`metasDe` consulta la etapa activa: `kcal = gasto estimado + ajuste`. Si no hay etapa
activa (después del 26 abr de 2027), cae al comportamiento de hoy. El ajuste sugerido
por el check-in (−100 o +100 kcal) se guarda por etapa y es reversible.

### 3.3 Checkpoints semanales

Se generan solos, un domingo por semana, con el peso esperado de la etapa menos el
ajuste por pausa de creatina. Semáforo: verde dentro de tolerancia, amarillo una semana
fuera, rojo dos o más seguidas.

### 3.4 Reglas de ajuste

Tal como las escribió el documento, todas con tendencia de 2 a 3 semanas y nunca con un
dato suelto. La de Cami respeta el orden que pide el documento: **primero** se revisan
pasos y entrenos, y solo si esos están al 100% dos semanas se sugiere bajar calorías.

### 3.5 Pausa de creatina

Toggle por persona con fecha. Ajusta el peso esperado con la tabla del documento (él
0,2 / 0,5 / 0,8 / 1,0; ella 0,1 / 0,3 / 0,5 / 0,6), marca los rescans de esas 4 semanas
como no comparables en magra, avisa de la caída de 1 a 2 repeticiones y aplica la tabla
al revés al reanudar. La recomendación del coach (la ventana barata es la etapa 2 de
cada uno, y lo caro es enero a marzo de 2027) va en la UI del toggle.

### 3.6 Rescans

Los seis del documento como eventos, con el protocolo (misma hora, misma hidratación,
sin entrenar antes, 2 horas sin comer) y la regla del agua: si varía más de 1 L contra
el anterior, la lectura de magra se marca no comparable.

## 4. Parte B · Los checkpoints que faltan

El documento solo proyecta **peso**. El peso es el indicador más ruidoso y el más lento
de los tres que importan. Estos son los que propongo agregar, ordenados por lo que
aportan:

1. **Cintura semanal.** Ya se mide cada 8 días y es el checkpoint de grasa honesto. En
   cut debería bajar ~0,3 cm por semana en Andrés; si el peso baja y la cintura no, lo
   que se está yendo no es solo grasa. **Y en el volumen es el freno**: el checkpoint de
   la etapa 3 no es "subir 0,25 kg/sem", es "subir 0,25 kg/sem **con la cintura
   quieta**". Sin ese freno, un volumen de 16 semanas se convierte en un cut más largo
   después. Propongo tope de +1,5 cm en toda la etapa 3.
2. **Un BIA completo guardado.** Hoy el check-in solo guarda `fat`. Los rescans dan
   magra, músculo esquelético, visceral, TMB, agua y segmentario, y sin ellos la mitad
   de las reglas del documento no se pueden evaluar (la de "agua ±1 L" necesita el agua
   guardada; la de "magra <1,2 kg se atribuye a agua" necesita la magra). **Este es
   requisito de casi todo lo demás.**
3. **Magra segmentaria como checkpoint de etapa 3.** Es literalmente la meta de esas
   etapas y hoy no hay dónde ponerla: piernas de Andrés (hoy 11,81 y 11,91) y brazos de
   Cami (hoy 1,96 y 1,94, meta >2,1). Se evalúa en el rescan, no cada semana.
4. **Fuerza de salida por etapa.** El documento solo pone una (sentadilla 135×8 en la
   etapa 1). Falta una de empuje y una de tirón por etapa para Andrés, y para Cami el
   registro de jalón, remo y press con la progresión de +1,25 kg que ella misma define.
   La app ya tiene metas de fuerza (P10) y el sistema de niveles: se cuelgan de ahí.
5. **Adherencia de proteína semanal.** Hoy el semáforo de proteína es diario. Como
   checkpoint semanal: verde si el 85% de los días llegó a la meta. Es el indicador que
   explica un peso plano mejor que el peso mismo.
6. **Pasos promedio de la semana** contra la meta, para los dos. El documento solo se lo
   pone a Cami; Andrés tiene 8 a 10k en todas las etapas y nadie lo está midiendo
   semanalmente.
7. **Energía y sueño como freno.** Ya se capturan (1 a 5). Dos semanas con energía ≤2
   deberían bloquear cualquier sugerencia de bajar calorías: primero se revisa el sueño.
8. **Checkpoint mensual para la etapa 3.** El documento pide juzgar el volumen por
   promedio mensual (>1,5 kg/mes es demasiado, <0,5 es poco). Eso es agregación
   mensual, no semanal, y necesita su propia tarjeta.

## 5. Parte C · Qué más agregar para que el plan se cumpla

1. **Diario de decisiones.** Cada ajuste aceptado (−100 kcal, +100, pausa de creatina,
   fecha de etapa movida) queda con fecha y motivo. Es un plan de 7 meses: sin esto, en
   enero nadie recuerda por qué come lo que come.
2. **Cierre de etapa.** Una pantalla que compara lo proyectado contra lo real al llegar
   al último domingo, y propone confirmar o mover las fechas de la etapa siguiente. El
   documento dice que las de etapa 3 y 4 son tentativas: esto es lo que las confirma.
3. **Proyección de composición, no solo de peso.** Con el ritmo de grasa se proyecta
   grasa en kg y % semana a semana. Es lo que el plan realmente promete ("12,5% de
   salida"), y es lo que hace visible la diferencia entre bajar grasa y bajar peso.
4. **Recordatorio de rescan con protocolo**, el día antes, con las cuatro condiciones.
   Un rescan mal tomado no se puede arreglar después.
5. **Marca automática de "no comparable"** en cualquier lectura de magra afectada por
   pausa de creatina, salto de agua >1 L o (en Cami) fase lútea o menstrual.
6. **La nota de creatina junto a toda lectura de magra**, como pide el documento.
7. **La nota de Cami en su perfil**: lo que produjo el cambio de agosto a septiembre
   (más pasos y constancia) fue el primero en 8 meses. Es la variable a proteger y tiene
   que estar escrita donde ella la vea.
8. **Ignorar los artefactos del reporte Biody** ("peso ideal 68 kg", "control de peso
   −21 kg"): no se muestran nunca, y si algún día se importa el reporte entero, se
   filtran.

## 6. Parte D · Reorganizar Medidas

### 6.1 Diagnóstico

Medidas tiene **tres barras de navegación en una sola pantalla** y **una sola variable
haciendo dos trabajos distintos**.

- `UI.cuerpoSub` es a la vez la **capa del mapa** (Medidas, Carga, Fuerza, Cruce) y la
  **sub-pestaña de composición** (Grasa, Meta). Por eso Grasa y Meta aparecen como
  "capas del cuerpo" en la barra de arriba aunque no pinten nada en el mapa.
- `medCapaBar` se dibuja **dos veces**, encima y debajo del contenido, con seis chips
  cada una.
- Dentro de la capa Medidas hay **una tercera barra** al pie con Grasa, Meta y Tomar
  medidas: repite dos de los seis chips de arriba y agrega la única acción de la
  pantalla, al fondo.
- Los seis destinos son hermanos pero no son de la misma naturaleza: cuatro son
  **lecturas del mismo mapa** y dos son **análisis de composición** sin mapa.
- **La acción tiene dos caminos**: el botón "Registrar lo de hoy" arriba (solo cuando
  toca) y el desplegable "Tomar medidas" abajo (siempre). Hacen lo mismo.
- **La composición está partida en cuatro sitios**: el % Navy vive en Meta, el slider de
  meta de grasa en Grasa, la masa magra en Meta, y el % de báscula se captura en
  Check-in. Un solo número, cuatro pantallas.
- **No hay nivel 1.** Al entrar no hay nada que responda "¿cómo voy?": hay un aviso de
  tarea pendiente y un mapa del cuerpo.

### 6.2 El sistema de navegación (decidido el 19/09/2026)

El problema de fondo no es que haya muchas secciones: es que **los tres niveles se ven
iguales**, la misma fila de chips con solo iconos, y en un teléfono no hay hover que
revele el rótulo. Un cajón lateral izquierdo no sirve aquí: la app ya usa el
deslizamiento horizontal para cambiar de capa y reserva los primeros 36 px para el
gesto de atrás de iOS.

**La solución: cada nivel con una forma distinta.**

- **Nivel 1, portada.** Medidas abre en una portada, no en el mapa. Arriba el estado de
  la semana, abajo una **lista de destinos con nombre completo y su cifra viva**
  (nunca un icono suelto). Es el patrón de Ajustes de iOS y encaja con el `accgrid`
  que la app ya usa en Perfil.
- **Nivel 2, pantalla completa con volver.** Cada destino es una pantalla propia con
  `pageHead`, igual que Check-in, Fotos y Hyrox. El **título es un botón**: al tocarlo
  sale una **hoja inferior** con los cuatro destinos en texto, para saltar de hermano a
  hermano sin devolverse a la portada.
- **Nivel 3, controles, no navegación.** Las capas del mapa (Medidas, Carga, Fuerza,
  Cruce) dejan de ser "navegación": son un control **del mapa**, van pegadas a él y
  **con rótulo de texto siempre visible**, no solo en la activa.

Así, en cualquier momento se sabe en qué nivel se está por la forma de la pantalla:
lista con chevrones, cabecera con volver, o control pegado al mapa.

### 6.3 Los cuatro destinos

**Nivel 1 · la portada.** Una pantalla que se lee en diez segundos:

- Cabecera de etapa: en qué etapa voy, semana N de M, peso esperado contra real,
  semáforo.
- Tres cifras y nada más: **peso** (promedio 7 días), **grasa %** (con su fuente) y
  **cintura**, cada una con su delta.
- Una sola acción: el botón de medir, que dice qué toca hoy o deja elegir.
- Debajo, los cuatro destinos, cada uno con su cifra viva ("15,0% y 76,3 kg de magra",
  "etapa 1, 5 semanas", "12 tomas, última el 15/09").

**Nivel 2 · cuatro destinos, no seis, agrupados por naturaleza:**

| Destino | Qué es | Qué se lleva de hoy |
|---|---|---|
| **Cuerpo** | el mapa y sus capas | MD2, MD3, proporciones (MD9), asimetrías (MD5), y las capas Carga, Fuerza y Cruce como capas **del mapa** |
| **Composición** | el % de grasa y de qué está hecho el peso | MD4 (Navy), MD7 (meta de grasa), la masa magra de MD8, el BIA nuevo y la nota de creatina |
| **Plan** | etapas y checkpoints | el módulo nuevo entero, más MD8 (la meta de peso) y MD6 ("qué hacer con esto") |
| **Historial** | todas las tomas | la tabla de 8 tomas, las gráficas y MD10 (cadencia) como referencia al final |

**Nivel 3 · dentro de cada destino**, una sola barra:

- Cuerpo: las 4 capas del mapa. Tocar una zona abre su panel. Proporciones y asimetrías
  bajan a caja plegada, porque son lectura del mismo mapa.
- Composición: las fuentes del mismo número (cinta Navy, báscula, BIA) una al lado de la
  otra, con cuál manda hoy y por qué. La meta de grasa se fija desde aquí y la etapa
  activa la propone.
- Plan: etapa activa, checkpoints, rescans, creatina y diario de decisiones.
- Historial: por medida.

### 6.4 Qué se elimina

- La barra de seis chips repetida arriba y abajo: queda una sola, en su nivel.
- La tercera barra del pie con Grasa y Meta duplicados.
- El doble camino para medir.
- `UI.cuerpoSub` haciendo dos trabajos: se parte en `UI.medSec` (destino de nivel 2) y
  `UI.medCapa` (capa del mapa).
- **El doble acceso**: Medidas deja de ser el tercer grupo de `progGrpSelector` y pasa a
  ser vista propia única (como Check-in, Fotos y Hyrox). Progreso queda con Actividad
  física y Nutrición, y deja un acceso grande a Medidas. `progGroup()` y el valor
  `medidas` de `PROG_KEYS` se retiran, cuidando que `?sub=medidas` siga llevando a la
  vista nueva.

### 6.5 Lo que no se toca

Ningún cálculo: Navy, proporciones, objetivos por zona, el mapa y su arte quedan igual.
Esto es reorganización y jerarquía, más el motor nuevo enchufado donde corresponde.

## 7. Parte E · Las metas al Inicio, en cajitas, con islas al contacto

Pedido de Andy (19/09/2026): las metas trazadas necesitan protagonismo, con cajitas
propias y las proyecciones en islas flotantes al contacto.

### 7.1 Todo esto ya existe, solo que disperso

Antes de construir nada: la app **ya tiene metas en cuatro sitios distintos** y ninguno
se ve desde el Inicio.

| Qué | Dónde vive hoy | Qué sabe hacer |
|---|---|---|
| Metas de fuerza (`S.goals`, `metasCard`) | Progreso → Actividad física, plegada | peso × reps, 1RM equivalente y **fecha proyectada al ritmo real** (`goalProy`) |
| Meta de peso (`metaFases`) | Medidas → Meta | objetivo con la magra real, ventana de fechas por regresión |
| Meta de grasa (`metaGrasaDe`) | Medidas → Grasa | slider con tope duro por sexo |
| Objetivos por medida (`medObjetivoDe`) | dentro del mapa, al tocar una zona | cintura objetivo despejando el Navy, proporciones |

El sistema de proyección más completo de la app (el de fuerza, que ya dice "al ritmo
actual la lograrías el 12/11") está tres toques adentro y plegado. **La mitad del
trabajo es sacarlo, no escribirlo.**

### 7.2 Los componentes se reusan tal cual

- **Cajita**: `.cktile` dentro de `.ckgrid` (dos columnas, `.wide` para ancho completo).
  Es lo que ya usa el Inicio para pasos, creatina y entreno.
- **Isla al contacto**: `.fbox` con `.scroll`, creada al vuelo como hace `islaSemana`
  (la cajita de entreno del Inicio ya abre una). No pasa por `render()`, así que abrir
  una isla no reconstruye la vista.
- **Anillo de avance**: `ring()`. **Cifras**: `.ckmetric` y `nrod()` (número rodante).

No hace falta CSS nuevo ni imágenes nuevas.

### 7.3 La sección "Tus metas" en el Inicio

Va **después del héroe y antes del checkpoint del día**: primero quién soy y cómo voy,
después a qué le estoy apuntando, después qué hago hoy.

```
┌──────────────────────────────────────┐
│ Tus metas                  ver todas │
├──────────────────────────────────────┤
│ ETAPA 1 · CUT FINAL      sem 1 de 6  │  ← cajita ancha (.wide)
│ 89,7 kg    esperado 89,3      ● verde│
│ ████████░░░░░░░░░░░░  salida 87,2    │
├──────────────────┬───────────────────┤
│ PESO DE SALIDA   │ GRASA DE SALIDA   │
│ 87,2 kg          │ 12,5 %            │
│ faltan 2,5       │ vas en 15,0       │
│ ≈ 26 oct         │ ≈ 2,5 pts         │
├──────────────────┼───────────────────┤
│ SENTADILLA       │ CINTURA           │
│ 135 × 8          │ 88,0 cm           │
│ vas en 120 × 8   │ vas en 91,5       │
│ ≈ 14 nov         │ faltan 3,5        │
├──────────────────┴───────────────────┤
│              +  Nueva meta           │
└──────────────────────────────────────┘
```

Reglas de la sección:

- **Máximo cuatro cajitas más la de etapa.** El Inicio ya es largo; si hay más metas,
  "ver todas" lleva a la vista Plan. Se muestran las de la etapa activa primero y
  después las que estén más cerca de cumplirse.
- **Cada cajita dice tres cosas y nada más**: a dónde voy, dónde voy hoy, y cuándo
  llego (o cuánto falta). El resto vive en la isla.
- **Color por estado**, no por tipo: verde en rumbo, ámbar atención, rojo dos semanas
  fuera. Es el mismo semáforo de los checkpoints, para no inventar un segundo lenguaje.
- **"Nueva meta"** abre el formulario que ya existe para fuerza, ampliado a los otros
  tipos (peso, grasa, medida, hábito).

### 7.4 La isla de la proyección

Al tocar cualquier cajita se abre la isla con **la proyección completa**, que es justo
lo que no cabe en la cajita:

```
╭────────────────────────────────────────╮
│ Peso de salida · etapa 1            ✕  │
│                                        │
│  87,2 kg          ● en rumbo           │
│  salida del cut · 12,5% de grasa       │
│                                        │
│  ╭──────────────────────────────────╮  │
│  │      ·  ·                        │  │  ← real (puntos) contra
│  │   ●─────●╲                       │  │    esperado (línea)
│  │           ╲──●───                │  │
│  │                  ╲───── 87,2     │  │
│  ╰──────────────────────────────────╯  │
│   20sep  27sep  4oct  11oct 18oct 25oct│
│                                        │
│  DOM      ESPERADO   REAL    ESTADO    │
│  20 sep     89,3     89,4      ●       │
│  27 sep     88,9      ·        ·       │
│  4 oct      88,5      ·        ·       │
│  11 oct     88,1      ·      descarga  │
│  18 oct     87,7      ·        ·       │
│  25 oct     87,3      ·      rescan    │
│                                        │
│  De dónde sale este número             │
│  76,3 kg de masa libre de grasa al     │
│  12,5% caen en 87,2 kg. Ritmo 0,40     │
│  kg/sem, tolerancia ±0,5.              │
│                                        │
│  [ Ver la etapa ]   [ Ajustar meta ]   │
╰────────────────────────────────────────╯
```

Por tipo de meta, la isla cambia de contenido pero no de forma:

- **Etapa y peso**: la tabla de checkpoints con esperado contra real y el semáforo, más
  la gráfica. Si hay pausa de creatina activa, el esperado ya viene ajustado y la isla
  lo dice con una línea.
- **Fuerza**: la curva de 1RM estimado, la fecha proyectada (`goalProy`, que ya existe)
  y qué hacer en la próxima sesión.
- **Medida**: la serie de esa medida, el objetivo y de dónde sale (Navy invertido o
  proporción).
- **Hábito**: las últimas 8 semanas contra la meta, y para Cami el recordatorio de que
  los pasos son la variable que produjo su cambio.

### 7.5 El héroe del Inicio habla de la etapa

Hoy el héroe dice "Faltan 5,6 kg para 86,6" con una barra que va de 94,4 a 86,6. Con
etapas eso queda desactualizado y además desmotiva: 7 meses en una sola barra.

- El pie del peso pasa a "**Faltan 2,5 kg para 87,2 · salida de la etapa 1**".
- La barra grande pasa a ser **la de la etapa activa** (6 semanas, no 7 meses), con el
  recorrido total del plan como una marca tenue detrás.
- En `statrow`, "kg/sem · meta 0,40" toma el ritmo de la etapa. **En volumen cambia de
  signo**: pasa a decir "kg ganados" y el verde es subir. Hoy el widget divide por
  `ritmoObjetivo()` sin protección: con ritmo 0 (mantenimiento) o negativo (volumen) hay
  que blindarlo o pinta cualquier cosa.

### 7.6 Lo que hay que cuidar

- **El Inicio no puede crecer sin control.** Entra una sección y sale peso de otra: la
  `statrow` y la barra se funden con la cajita de etapa en vez de repetir el mismo dato
  dos veces en la misma pantalla.
- **Las islas no pasan por `render()`** (patrón de `islaSemana`): si se reconstruye la
  vista con la isla abierta, se pierde el scroll de la vista de abajo.
- **Una meta cumplida no desaparece**: se marca lograda y se va a la vista Plan. Que
  desaparezca borra la sensación de haber llegado, que es justo lo que se está buscando.

## 8. Orden de ejecución propuesto

| Fase | Qué | Por qué en ese orden |
|---|---|---|
| 1 | Datos del plan: BIA base, etapas, creatina corregida, almacén `S.bia` | todo lo demás lee de aquí |
| 2 | Motor: etapa activa, checkpoints, semáforo, pausa de creatina, reglas de ajuste | lógica pura, verificable sin UI |
| 3 | Enganche en `metasDe` y en la meta de peso | **es la fase que le cambia la comida a Andrés**; revisar con él antes de seguir |
| 4 | Check-in: campos nuevos (entrenos, pasos), semáforo de la semana, sugerencias | el ritual del domingo ya existe |
| 5 | Vista Plan | el módulo nuevo completo |
| 6 | Reorganización de Medidas | la más invasiva y la que menos riesgo tiene de perder datos |
| 7 | Metas al Inicio: cajitas e islas (Parte E) | necesita el motor de etapas y las metas ya unificadas |
| 8 | Checkpoints nuevos de la Parte B y extras de la Parte C | encima de una estructura ya ordenada |

Cada fase: snapshot, `verificar.py --base=`, Chrome headless con los dos usuarios,
bump de `APPREV` y de los dos `sw.js`, un commit. **Nada se despliega sin que Andy lo
vea en local.**

## 9. Ya hecho en esta sesión (fuera del plan)

**Bug de "Registrar lo de hoy" (19/09/2026).** El botón grande de Medidas pasaba
`data-g="pend"` y `medCamposHoy` lo buscaba en `MED_GRUPOS`, donde no existe:
`undefined is not an object (evaluating 'MED_GRUPOS[x].campos')`. El camino más usado
de la pantalla estaba roto. El mismo fallo tenía el botón de `propCard`, que pasaba
`'mes'` (la letra del campo) en vez de `'quince'` (la clave del grupo).

Arreglado: `medCamposHoy` resuelve `'pend'` a los pendientes, filtra claves que no
existen y cae a "todos los grupos" si no queda ninguna válida. Verificado con
`verificar.py --base` (sin regresiones) y con Chrome headless: el formulario abre con
sus 16 campos y cero errores de consola. **Sin commitear, sin desplegar.**

## 10. Lo que Andy decidió y cómo quedó

1. **Las kcal**: "haz lo que consideres pertinente". Se aplicaron de una, sin rampa: con
   89,7 kg la app da **2.432 kcal**, que son los 2.400 del plan. Mantenerlo en 2.230
   habría dado 0,63 kg/semana, muy por encima de los 0,40 proyectados, y con 43 kg de
   músculo esquelético eso no es solo grasa.
2. **El factor de actividad**: 1,45 para Andrés (4 entrenos y 8 a 10k pasos) y 1,49 para
   Cami, que es el número que reproduce exactamente sus calorías de hoy. **Y se
   recalibra solo** (`factorActividad`): con 21 días de comida registrada y una recta de
   peso fiable, la app compara lo que se comió con los kilos que se movieron y corrige
   el factor, acotado entre 1,2 y 1,9.
3. **El freno de cintura** en el volumen (+1,5 cm máximo): aprobado, va en `etapas[2].cintura.tope`.
4. **Todo de una**: las 8 fases quedaron hechas.
5. **Las cajitas del Inicio**: las elige la app (`metasDestacadas`), primero lo que pide
   atención y después lo que está más cerca de lograrse.

## 11. Decisiones pendientes de Andy

1. **Las 200 kcal de Andrés** (fase 3): pasa de ~2.230 a ~2.430 al día. ¿Se aplica de
   una, o se sube en dos pasos de 100 para que el cuerpo no lo lea como un rebote?
2. **El factor de actividad 1,45** sobre la TMB medida es mi estimación (entrena 4 veces
   por semana y camina 8 a 10k). Es la única cifra del motor que no sale de un dato
   medido. Si prefieres, se expone como ajuste fino en la app.
3. **El freno de cintura en el volumen** (+1,5 cm máximo en la etapa 3): número mío, no
   del documento. ¿Lo dejamos ahí?
4. **Fases 6, 7 y 8**: ¿van en esta tanda o las dejamos para después de ver funcionando
   lo de las etapas?
5. **Cuántas cajitas en el Inicio**: propongo la de etapa más cuatro. ¿Las eliges tú
   (fijar metas al Inicio) o las elige la app por urgencia?
