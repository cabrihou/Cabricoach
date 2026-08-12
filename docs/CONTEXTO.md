# Contexto del proyecto · estado y pendientes

> Actualizado: 03/08/2026, corte en REV 123. Este es el documento de aterrizaje:
> qué es esto, en qué está, qué falta y dónde está todo lo demás.

## Qué es

CabriCoach: la app de entrenamiento y nutrición de Andrés y Cami (pareja, Bogotá).
PWA de archivo único instalada en sus iPhones desde Netlify (cabricoach.netlify.app).
No es un producto: es SU app, a la medida, y las decisiones se toman con ese lente.

Los dos perfiles y la regla de oro de nutrición están en
[ARQUITECTURA.md](ARQUITECTURA.md) §1 y §5 (Andrés usa retatrutida: el riesgo es
comer de menos, la app empuja a alcanzar la proteína). Metas de macros DINÁMICAS
por peso desde REV 111 (1,8 g/kg de proteína, promedio semanal de pesajes): el
"195 g" que aparece en documentos viejos ya no es fijo.

## Mapa de documentos

| Doc | Para qué |
|---|---|
| [ARQUITECTURA.md](ARQUITECTURA.md) | cómo funciona por dentro, con los porqués |
| [PRUEBAS.md](PRUEBAS.md) | receta completa de verificación (estático + CDP) |
| [MAPA.md](MAPA.md) | código corto por zona de pantalla (I4b, C3d...) para señalar sin ambigüedad |
| [DESIGN-STANDARDS.md](DESIGN-STANDARDS.md) | estándar visual REV 4.0 "Night Gym" (lo escribió Andy; manda). §5 tiene la regla de dónde se generan las imágenes |
| [AUDITORIA-IMAGENES.md](AUDITORIA-IMAGENES.md) | qué fotos hay que rehacer y por qué (09/08); los nodos ya están en el space del personaje |
| [PROYECTO-COACH-AFC.md](PROYECTO-COACH-AFC.md) | especificación original (perfiles, plan, rutinas). Histórico: los macros fijos que menciona ya son dinámicos |
| [INDICACIONES.md](INDICACIONES.md) | registro histórico de pedidos de la sesión del 30/07 |
| `../CLAUDE.md` | arranque para Claude Code (estructura, trampas, publicación) |
| `../.claude/agents/cabricoach.md` | contexto que carga el agente de trabajo |

## Cómo arrancar en un computador nuevo

```bash
git clone https://github.com/cabrihou/Cabricoach.git && cd Cabricoach
zsh herramientas/setup.sh     # revisa python3, jsc, claude, hooks, credenciales
```

Lo que NO viaja por git: `~/.config/cabritos.env` (credenciales de nube) y la
programación del coach diario (`zsh herramientas/coach-diario/instalar.sh`).
Regla que evita el dolor: `git pull --rebase` ANTES de tocar nada (el archivo es
uno solo; un conflicto es irresoluble a mano).

## Estado al corte (REV 130, 07/08)

REV 130: fotos de calistenia y anillas (24, set Andrés-Cabrito) conectadas al
catálogo; rutina de movilidad real (10 ejercicios en 3 bloques con foto, detalle y
player guiado con temporizador; categoría Movilidad en el catálogo); mapa muscular
de cabra en Personalizado (frente/espalda tocables); metas de fuerza en Progreso
(P10: barra, escalones, proyección de fecha por regresión); gráficas con eje Y y
estilos Línea/Barras/Suave; deslizar para navegar (calendario, rotador, día de
Gestión, detalle de día); y la causa raíz del salto al ingresar comida corregida
(doble render de `paqCargar` que robaba el foco + vigilantes de scroll solapados,
ver ARQUITECTURA §3). Verificado con CDP: por tecla ≤1,3 px, foco retenido,
aritmética exacta, 0 errores de consola en las 10 vistas × 2 usuarios.

## Estado anterior (REV 123)

Fase reciente (REV 101 → 123, jul 31 - ago 3): motor de escalado por ingrediente
con techo de kcal, mercado que compra la semana real del plan, rotación gobernada
por porciones, precios verificados contra mercado colombiano, cambios de
acompañamiento/salsa por receta, recetas del desvare (proteína asada + papas a la
francesa), Gestión en cajas colapsables, ciclo de Cami al final del inicio con la
paleta propia, isla semanal de entrenos con reinicio dominical 8 pm, cápsula del
próximo entreno con análisis del historial y enganche de IA, estabilizador de
scroll (la causa raíz de "los saltos" era content-visibility), gráficas con piso
verosímil y proyección del periodo elegido, metas dinámicas por peso.

## Pendientes que requieren a Andy

1. **Push bloqueado en el computador principal**: git quedó autenticado como
   `afcastrocc` (sin permiso de escritura en `cabrihou/Cabricoach`). Arreglo:
   `gh auth login` como `cabrihou`. Hasta entonces los commits se acumulan localmente.
2. **Netlify llegó a publicar REV 104 con versiones más nuevas ya en GitHub**:
   si el sitio no refleja el último REV tras un push exitoso, revisar el panel de
   Deploys en app.netlify.com.

## Deuda técnica conocida

- ~50 botones solo-icono sin `aria-label`; 28 labels bajo 12,5 px por espacio.
- La tabla de evolución del check-in scrollea horizontal a 320 px.
- "Leche" puede duplicarse en la lista de compras (recetas en ml, básicos en L).
- 22 avisos heredados del verificador (la línea base; no crecerla).
- Los macros declarados de ~13 recetas no cuadran del todo con sus ingredientes
  (sobre todo grasa por aceite de cocción no listado); el detalle está en
  `validacion-macros.md` del scratchpad de la sesión del 02/08. El motor de
  escalado ancla a los declarados precisamente para no arrastrar eso a la pantalla.

## Proyectos satélite

- **Base nutricional Colombia**: `Personal/nutricion-co/` (fuera de este repo).
  Cosecha de Open Food Facts (~7.100 productos con Colombia), tubería
  `cosechar_api.py` + vigilantes, entregables CSV/JSONL/reporte con validación de
  cuadre calórico y marcas propias por cadena derivadas de los datos. Licencia
  ODbL con atribución (ver su `ATRIBUCION.md`). Candidata a alimentar el buscador
  de alimentos de la app.
- **Coach diario**: `herramientas/coach-diario/` escribe `afc2:u:coach:daily`.
  El MISMO patrón sirve para el agente del próximo entreno
  (`afc2:u:<uid>:proxIA`, ver ARQUITECTURA §6): Andy definirá ese agente.

## Metas nutricionales de Andrés (agosto 2026)

Antes: 2.200 kcal y proteína derivada del peso (peso × 1,8 = 195 g a 94,4 kg).
Ahora: **2.400 kcal · 150 g de proteína · 75 g de grasa · 280 g de carbohidratos**, fijos.

El porqué, que es lo que no se deduce del código: 195 g era inalcanzable en la práctica. La
adherencia real estaba en 120-125 g por volumen de comida (usa un supresor del apetito) y por
costo. Se subieron las calorías y se bajó la proteína a un número sostenible. El razonamiento:
**150 g con un déficit de ~250 kcal preserva más masa magra que 125 g reales con un déficit de
500**. La proteína y el tamaño del déficit son la misma palanca. 150 g son 2,1 g por kg de masa
magra (70,72 kg, BIA del 27/07/2026), dentro del rango recomendado para atletas entrenados en
déficit.

- **Piso duro: 140 g.** Por debajo el día sale en rojo; verde desde 150. Está en
  `PLANS.andres.protPiso` y lo aplica `protEstado()`. La gráfica de proteína día a día pinta
  cada barra con ese semáforo y lleva una línea punteada roja en el piso.
- **2 scoops de whey diarios** (48 g de proteína, 240 kcal). Es el componente que hace viable
  llegar a 150 g comiendo lo que de verdad le cabe. Viven en `PLANS.andres.fijos`,
  se muestran en la caja "La semana comida por comida" y **se descuentan del reparto**: las
  comidas cubren 102 g y 2.160 kcal, no los 150 y 2.400.
- **El déficit bajó de ~500 a ~250 kcal**, así que el ritmo esperado se corre a la mitad:
  `rateGoal` pasa de 0,8 a 0,35 kg/semana y `lossAlert` de 1,0 a 0,7. La meta de 86,6 kg se
  mueve de mediados a finales de septiembre. **Ojo**: la proyección que se muestra en pantalla
  no sale de estos números sino de la regresión real del peso (`pesoRecta`), así que se corrige
  sola; `rateGoal` es solo contra qué se juzga la semana.

Las metas fijas se activan con `PLANS[uid].metasFijas`. Si un plan no lo trae, `metasDe` sigue
derivando del peso como siempre. **Cami no se tocó**: sigue en 1.700 kcal con proteína por peso
y su scoop dentro de la avena.

### Receta nueva: hamburguesa de res casera

Mezcla base que rinde 2.130 g crudos = 17 hamburguesas de 125 g. En crudo, que es como se pesa
la mezcla antes de armar: **139 kcal, 14,3 g de proteína, 7,0 de grasa y 2,3 de carbo por cada
100 g**. Una hamburguesa de 125 g son 174 kcal y 18 g de proteína, o sea **10,3 g de proteína
por cada 100 kcal**: apta para día normal.

La papada y la tocineta **no** van en la base. Son topping opcional y hunden la eficiencia
proteica a 8,0.

Ingredientes de la mezcla: 1.500 g de molida de res 90/10 (molida especial), 450 g de cebolla
roja, 150 ml de Malbec, un ramo de cilantro, sal, ajo y pimienta. En la receta de la app las
cantidades salen por plato: la carne es el 70% de la mezcla, la cebolla el 21% y el vino el 7%.

## Creatina (agosto 2026, los dos)

**3 g diarios** de monohidrato desde el **7 de agosto de 2026**, sin fase de carga: cargar con 20 g acelera la saturación una o dos
semanas y no cambia el resultado a los dos meses.

Lo que hay que saber, y es lo que la app dice en pantalla: **la creatina satura el músculo de
agua intracelular y sube el peso entre 0,8 y 1,6 kg en unas 5 semanas (con 3 g la saturación tarda un poco más y
retiene algo menos que con 5)**. No es grasa ni es
retención subcutánea. Si nadie lo avisa, ese salto se lee como "dejé de bajar" y lleva a
recortar calorías sin motivo.

Cómo quedó:

- `S.creat[iso]` es el registro diario y `S.cfg.creatDesde` la fecha de arranque, que se pone
  sola el primer día que se marca. Tarjeta en Inicio con el toggle, los días seguidos y el día
  del plan. Se sincroniza con la nube.
- `creatAgua()` estima el agua acumulada en rampa lineal hasta la mitad del rango (1,5 kg) al
  cerrar las 4 semanas, y de ahí se queda fija: es una constante, no algo que siga creciendo.
- **La lectura semanal cambia mientras satura**: "subiste 0,4 kg" pasa a decir que es agua del
  músculo y que no se toque el déficit; "peso estable" pasa a decir que estable ya es bajar,
  porque el agua nueva está tapando la grasa que se fue.
- En Peso sale el **peso comparable** (el de la báscula menos el agua) y la **meta corrida**:
  los 86,6 kg se fijaron sin creatina, así que el mismo cuerpo con creatina marca 88,1.

**Cami también, desde el 7 de agosto y también 3 g.** La dosis no escala con el peso corporal
sino con la masa muscular, y 3 g saturan igual solo que más despacio. El agua que retiene sí
escala con el músculo y ella tiene menos: 0,6 a 1,2 kg contra los 0,8 a 1,6 de él.

No entra en la racha ni en los puntos de los retos: cambiar la fórmula de puntaje a mitad de
camino invalidaría las semanas ya jugadas.


### La meta de agua bajó

Estaba en 35 ml/kg más 500 ml los días de entreno: 3,7 L a 92 kg, medio litro por encima de lo
que pide el propio plan (2,5 L). Una meta que nadie cumple deja de ser meta. Ahora **30 ml/kg del peso de hoy, +300 los días de entreno y +250 por la creatina mientras
satura (+150 después), con tope de 3,5 L**. A 94,4 kg en día de gym: 2.850 + 300 + 250 =
**3.400 ml**. Cami a 59,5 kg: 1.800 + 300 + 250 = **2.350 ml**. **Usa el peso de ESE día** (`pesoDeDia`), no el último del historial: la meta de un martes se
calcula con lo que marcaba la báscula el martes, y la de hoy se recalcula en cuanto te peses.
Si ese día no hubo pesaje, cae al último registro anterior y lo dice. El desglose sale escrito
en MÁS para que el número no salga de la nada.
El "+500 ml por creatina" que se repite por ahí no tiene respaldo firme; lo documentado es que
hay que mantenerse bien hidratado, y +250 lo cubre sin volver a una meta que nadie cumple. El agua de la comida no se
cuenta aquí, así que la ingesta real es mayor que el número.

## El déficit es lo que se fija, no las calorías (REV 196)

Estaban formulados **distinto entre los dos**, y los dos mal:

- **Andrés**: 2.400 kcal **fijas**, no se movían con el peso. Al bajar de 94,4 a 86,6 kg el
  gasto cae unas 117 kcal, así que el déficit se encogía solo de 250 a **133**: el plan se
  frenaba justo al final, cuando más cuesta.
- **Cami**: `kcal = peso × 28,6`. Recortaba 28,6 kcal por cada kilo perdido cuando el gasto
  real solo baja unas 15. Su déficit crecía solo de 330 a **371** sin que nadie lo decidiera,
  justo cuando menos margen hay.

Ahora los dos usan `metasBase:{peso, kcal, deficit}` y las calorías salen de
**gasto estimado − déficit**, con el gasto recalculado desde el peso de la semana:

```
kcal(peso) = kcal_base + 15 × (peso − peso_base)
```

Los 15 kcal/kg no son un invento: en Mifflin-St Jeor lo único que escala con el peso corporal
es el término de peso (10 kcal/kg); estatura, edad y constante no se mueven. Con un factor de
actividad de ~1,5 quedan ~15. Un "kcal por kg" plano de 28 recorta casi el doble de lo que de
verdad se deja de gastar.

Se ancla en el peso y las kcal de hoy, así que **no hace falta ni estatura ni edad**: lo que
importa es la pendiente, no el valor absoluto.

| | Hoy | A mitad de camino | En la meta | Déficit |
|---|---|---|---|---|
| Andrés | 2.400 @ 94,4 kg | 2.342 @ 90,5 | 2.283 @ 86,6 | 250 siempre |
| Cami | 1.700 @ 59,5 kg | 1.678 @ 58,0 | 1.655 @ 56,5 | 330 siempre |

En Gestión → La semana comida por comida sale la caja **"De dónde salen tus N kcal"** con el
gasto, el déficit y la meta, para que se vea que el número se mueve y por qué.
