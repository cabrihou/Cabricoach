# Botellas v7 · La zona del nivel dentro del juego (2026-10-21)

Todo lo de ESPEC-v6 sigue valiendo.

Pedido de Andy: "¿No te gustaría que cada nivel tuviera algo de detalles en medio del juego relacionados
con el nivel?". Respuesta acordada: sí, con la zona del recorrido a la que pertenece el nivel, reusando los
paisajes (`IMG.zona1..4`) y los adornos (`adorPradera..Cumbre`) sin imágenes nuevas. Regla: los detalles
acompañan, las botellas mandan (en Extra difícil, con capas tapadas, la lectura no puede bajar).

## 1. Tablero según la zona (`#vJuego`)

- **Fondo**: el paisaje de la zona reemplaza al estante (`--estante`, hoy al 0,17) en una franja baja del
  tablero, oscurecido y difuminado hacia arriba, con el tinte de la zona del mapa. Arriba queda el negro de
  siempre. Las zonas 201+ siguen el ciclo. Reto del día: usa la zona que le toque por su fecha (o la
  pradera), da igual cuál mientras sea fija.
- **Adornos en el suelo**: 2 o 3 adornos de la hoja de la zona, apoyados abajo, en las esquinas o los
  bordes, nunca detrás de una botella, una caja, el aviso de sin salida ni la barra de abajo (medir con el
  tablero ya distribuido; en tableros de 3 filas que llenan el alto, puede quedar uno o ninguno). Cuáles y
  dónde, fijos por nivel (semilla del nivel), así cada nivel tiene "su" escena.
- **Ambiente** (CSS, sin imágenes): pradera unas pocas chispas cálidas, bosque luciérnagas, nieve copos,
  cumbre estrellas que titilan. Muy pocas, lentas, casi transparentes, detrás de las botellas, sin
  interceptar toques. Nada con prefers-reduced-motion. Se pausan si el juego está en pausa o la pestaña
  oculta.
- **Lectura**: comprobar contraste de capas, "?" de lo tapado, candados y llaves sobre el fondo nuevo en un
  nivel Extra difícil de cada zona; si algo baja, gana la lectura (más oscuro o menos adornos).

## 2. Cabecera y victoria

- Debajo de "Nivel N", la zona y lo que falta: "El bosque · faltan 40 para la meta" (en la meta: "La meta
  del bosque"). Sin desbordar a 320 px con el chip de grado.
- Hoja de victoria: una línea con el avance del tramo ("Te faltan 39 para la meta del bosque"). Al ganar un
  nivel de meta (50, 100...), la hoja lleva arriba la ilustración de la cima (`IMG.cima`) y el texto de
  meta ("¡Coronaste el bosque!" o similar, sin rayas largas).

## 2b. Elementos del juego en el tablero (pedido con captura, 2026-10-21)

Andy, sobre una captura del tablero (negro, solo botellas): "Acá es donde te digo que deberían haber más
elementos asociados al juego". La zona sola no basta: falta el juego mismo. Imágenes nuevas (nodos creados,
Andy los ejecuta; huecos opcionales `@IMG?:` con respaldo):

| Hueco | Qué es | Formato que entrego (recursos/*.b64) | Nodo (hoja → sin fondo) |
|---|---|---|---|
| `repisa` | repisa de madera bajo cada fila de botellas | WebP con alfa, ~900 px de ancho, recortado a la tabla | 299ab9b7-62b4-4a17-9dca-0c74b7a0ed7d → 9c53e12c-53e2-4ca1-ae2a-a60018748f40 (pestaña Cami) |
| `labo` | 9 objetos de laboratorio (matraz, embudo, gotero, balón, corchos, lupa, libreta, beaker, gradilla) | WebP con alfa 480x480, 3x3 celdas de 160 apoyadas abajo (como los adornos) | 4e4bdb0e-2752-4965-b2c8-44c06c1663b0 → 490ea33d-04b2-43d0-a5bf-f9fe029fc939 (Cami) |
| `reacC` | Cami en 4 poses: 0 mira, 1 anima, 2 piensa, 3 gana | WebP con alfa 400x400, 2x2 celdas de 200 apoyadas abajo | f0b54181-65d9-4e84-a6c6-cc7dee2f7823 → 907134f5-357c-4e81-a67d-cb4d70a92cc1 (Cami, con CAMI MAESTRO) |
| `reacA` | Andrés en las mismas 4 poses | igual | 04976832-ddfe-43a2-8fe0-0a2d65447b1e → b6f34037-94dc-4412-9431-b730cb5c98a4 (Andrés, con AND MAESTRO) |

- **Repisa**: cada fila de botellas (`.brow`, incluidas las cajas y la fila con gigante) se para sobre una
  repisa a lo ancho de la fila, un poco más ancha que ella, con sombra suave de contacto. Respaldo sin
  imagen: una tabla discreta en CSS (degradado madera oscuro, borde de luz arriba). Al arrastrar o levantar
  una botella, la repisa se queda.
- **Laboratorio**: 1 a 3 objetos sobre los extremos de las repisas donde sobre espacio (nunca tocando una
  botella ni su zona de toque) y en el suelo junto a los adornos de la zona. Fijos por nivel.
- **El cabrito del jugador** (Cami o Andrés según `S.jugador`) en una esquina de abajo, fuera de las
  botellas, del tamaño que quepa (orientativo 90 a 120 px de alto a 390; se esconde si no cabe), reaccionando:
  `mira` por defecto; `anima` ~1,2 s al completar una botella o abrir una caja o candado; `piensa` mientras
  esté el aviso de sin salida; `gana` al ganar. Cambio con fundido y un saltito; con reduced-motion, cambio
  seco. Sin toques (pointer-events:none). Sin la imagen, no aparece.
- Todo con la misma regla de lectura de la sección 1.

## 3. Pruebas (`pruebas-chrome.py`, sección "zona")

Fondo y adornos de la zona correcta en niveles de las 4 zonas y en uno 201+; ningún adorno se cruza con
botellas, cajas, aviso de sin salida ni barra (getBoundingClientRect); con movimiento reducido no hay
animación; arrastrar y tocar siguen igual (los adornos no reciben toques); cabecera a 390 y 320 sin
desbordar; victoria normal y de meta. Capturas v10-, incluido un Extra difícil por zona para revisar la
lectura.
