# Botellas (water sort) · investigación del género

21/10/2026. Pedido de Andy: un juego de llenar botellas para Cami dentro de CabriCoach.
Fuente: búsqueda web (modo standard) más criterio propio. **[V]** = verificado con fuente,
**[I]** = inferencia nuestra.

## Reglas canónicas

- Se vierte la capa de arriba de una botella a otra solo si la de destino está vacía o su
  capa de arriba es del mismo color, y si tiene espacio. Cae toda la racha contigua de ese
  color que quepa. **[V]** ([App Store](https://apps.apple.com/us/app/id1571446860))
- Se gana cuando cada botella tiene un solo color. **[V]**
- Casi todas traen deshacer, reiniciar y "botella extra" (en las comerciales son
  potenciadores que se compran o se ganan con anuncios). **[V]**
  ([Nintendo](https://www.nintendo.com/en_US/games/detail/color-water-sort-complete-edition-switch))
- Capacidad estándar 4. Hay niveles especiales con "botellas largas"
  ([Appcelent](https://apps.apple.com/us/app/water-sort-color-puzzle-game/id1585297796)).
  El solver de Kociemba admite hasta 14 colores y 6 capas.

## Variantes que existen

Colores ocultos ("?" que se revelan al quedar arriba), botellas con candado, capas
congeladas, límite de movimientos, contrarreloj, botellas largas, ball sort (bolas en vez
de líquido; es el mismo problema: uno se resuelve si y solo si el otro,
[arXiv 2202.09495](https://arxiv.org/pdf/2202.09495)), y versiones con objetos (patitos,
frutas). El juego exacto de la captura de Cami (patitos sobre botellas largas completas)
no se identificó: hay que preguntarle a ella el nombre.

## Dificultad

- Sube con más colores, más botellas y menos vacías; las vacías son el espacio de trabajo. **[V]**
- Resolver es NP-completo y hallar la solución más corta también
  ([FUN 2022](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FUN.2022.16)), pero
  en la práctica, con capacidad 4 y hasta 14 colores, un solver encuentra la solución en
  segundos ([hkociemba](https://github.com/hkociemba/WaterBallSortPuzzleOptimalSolver)). **[V]**
- No encontramos estudios publicados de curva de dificultad ni de retención en este
  género: la curva de abajo es propuesta nuestra, calibrada con el solver.

## Generación de niveles (lo que usamos)

1. Semilla fija por nivel (`camino:14`) y por fecha (`dia:2026-10-21`): el nivel 14 es el
   mismo para Cami y para Andrés, y el reto del día también, sin servidor.
2. Se reparten las capas al azar y se descarta todo reparto que el solver no resuelva.
3. Heurística A*: número total de rachas de color menos el número de colores. Cada
   vertido baja esa cuenta en 1 como mucho, así que la heurística es admisible y la
   solución que encuentra es la más corta: esa es la **meta** de movimientos para las
   estrellas. Si A* se pasa del tope de estados, se usa A* ponderado (meta casi óptima).
4. Varios candidatos por nivel: el "difícil" se queda con el que más movimientos pide y el
   de "respiro" con el que menos.

## Curva propuesta

| Niveles | Colores | Vacías | Capacidad | Notas |
|---|---|---|---|---|
| 1-2 | 3 | 2 | 4 | tutorial guiado |
| 3-9 | 4-5 | 2 | 4 | |
| 10-20 | 6-7 | 2 | 4 | difícil cada 7 niveles (+1 color), respiro después (-1) |
| 21-50 | 8-10 | 2 | 4 | misterio cada 5 niveles desde el 25; botellas largas cada 10 desde el 30 |
| 51+ | 11-12 | 2 | 4 | tope de 12 colores; la dificultad sigue subiendo por selección de candidatos |

## Retención sin dinero

Sí: reto del día igual para los dos, racha, estrellas por movimientos frente a la meta,
estadísticas propias, colección de recompensas, deshacer gratis e ilimitado, "aquí ya no
hay salida" con vuelta al último punto que sí la tiene.

No: anuncios, vidas o energía, muros de pago, niveles imposibles sin potenciador,
rachas que castigan, contrarreloj obligatorio.

## Sensación de juego

Vertido corto (unos 700 ms en total) para que repetir no canse, la botella se levanta, se
inclina hacia la de destino y cae un chorro; tapa que cae con rebote al completar una;
confeti al ganar; sonido sintetizado con Web Audio. `navigator.vibrate` no existe en el
iPhone, así que la vibración es solo para Android. Símbolos por color para daltonismo.
Todo se apaga con `prefers-reduced-motion`.
