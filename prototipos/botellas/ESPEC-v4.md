# Botellas v4 · ajustes de Andy tras probarlo en la app (2026-10-21)

Pedidos, en sus palabras resumidas:
1. "No me deja salir una vez entro."
2. "Quiero que pueda ingresar desde el home, así como tengo un icono para entrar rápidamente con
   la cámara, crea un icono para poder entrar en el juego."
3. "Cuando desbloqueo una botella, esa botella tiene más colores para asignar: no termino, sino que
   ahí me desbloquean unos nuevos colores que también tengo que redistribuir." Cajones que al sacar
   la llave abren dos botellas.
4. "También puedo tener una botella gigante que se llena no con 4, sino con 10."
5. "Hay mucho espacio en negativo, está muy vacío alrededor." Ambientar el home del juego con
   cabritas (máximo 3 o 4 imágenes nuevas, en el space de CabriCoach en Magnific).
6. "Quita las pistas, no quiero que tenga pistas."

Todo lo de ESPEC-v3 sigue valiendo salvo lo que cambia aquí.

## 1. Salir del juego (app)

En Chrome el botón `#salir` del juego responde a un toque real, así que el bloqueo es propio del
iPhone y no se puede reproducir aquí. La salida deja de depender del iframe: la capa de la app
lleva su propia barra arriba (DOM de la app, no del juego) con el botón "Volver a CabriCoach"
(chevron + texto, 44 px de alto mínimo, vidrio como el chrome de la app). El iframe va dentro de un
contenedor `position:relative; flex:1; overflow:hidden` y el iframe en `position:absolute; inset:0;
width:100%; height:100%` (en iOS un iframe puede crecer a la altura de su contenido si no se le
encierra). El host avisa `barra:true` y el juego, al verlo, esconde su `#salir`.

## 2. Icono en el Inicio de la app

Junto al icono de acceso rápido de la cámara en el Inicio, uno igual para Botellas (SVG de trazo
con el punto de acento, una botella) que abre el juego (`botellasAbrir`). Mismo tamaño, estilo y
`aria-label` ("Jugar Botellas").

## 3. Lo que se desbloquea trae liquido (motor)

- **Nada cerrado viene vacío.** Se acaban "candado en vacía" y "caja con vacía": toda botella con
  candado y toda botella dentro de una caja trae líquido. Abrir no termina el nivel: suelta más
  líquido para ordenar.
- **Colores nuevos.** Cuando lo cerrado suma 8 capas o más (un cajón de dos botellas, o candado +
  caja), al menos un color vive completo ahí adentro: no aparece afuera, así que al abrir "llegan"
  colores nuevos. Esas capas se mezclan con algunas de colores de afuera para que haya que
  redistribuir. Con una sola botella cerrada (4 capas) no cabe un color entero sin que ya venga
  completo: ahí trae una mezcla de colores de afuera.
- **Cajón de dos botellas**: la caja de 2 botellas (ya existe) es la forma normal de la llave
  desde su estreno.
- El nivel campo `nuevos:[colores]` lista los colores que solo están en lo cerrado.
- Siempre al menos 2 vacías libres (lo cerrado ya no regala espacio).

## 4. Botella gigante (motor ya listo en el núcleo)

- El núcleo ya acepta `caps` (capacidad por botella) y `u` (capas por color). Una botella está
  completa con las `u` capas de un color aunque le sobre espacio. Pruebas en `pruebas-nucleo.js`.
- Gigante = capacidad 10 en un nivel de botellas de 4 (`u = 4`). Empieza con 5 a 8 capas
  mezcladas (nunca `u` de un solo color, nunca cerrada). Cuenta como una botella para el tope de 15.
- Rasgo `gigante`, estreno en L30 (Normal), después de vez en cuando (no con largas).
- Interfaz: más ancha (~1,4×) y más alta (~1,7×) que las normales, apoyada abajo en su fila, capas de
  `alto/10`; tapa cuando se completa; el vertido usa el tamaño de cada botella (superficie por su
  capacidad). En todo lado `completa` se mide con `u` (`nv.u || nv.cap`), no con la capacidad.

## 5. Menos vacío (interfaz del juego)

- Tablero: las botellas crecen hasta llenar el espacio (subir el tope de ancho para niveles con
  pocas botellas, menos reserva arriba), y el bloque queda bien centrado.
- Ambientación con cabritas: hasta 4 imágenes nuevas de Magnific (las hace el principal en el space
  de CabriCoach) para el inicio del juego y el tablero. Mientras llegan, usar las que ya hay.

## 6. Sin pistas (interfaz del juego)

Fuera el botón Pista, su código y toda mención. La barra queda con Deshacer, Reiniciar y Botella
extra. Se queda el aviso de "sin salida" (con "Volver al último punto con salida" y "Usar la botella
extra"): no es una pista, es lo que garantiza que nunca te quedas encerrada.

## Estrenos de mecánicas (nuevo calendario)

L4 candado (con líquido), L7 llave con caja de una botella, L12 cajón de dos botellas con un color
nuevo, L20 misterio leve, L25 largas, L30 gigante, L35 misterio total, L50 dos cajas, L80 cadena.
