# Botellas v6 · El mapa del recorrido (2026-10-21)

Todo lo de ESPEC-v5 sigue valiendo.

Pedido de Andy: "Quiero ahora que hagas un mapa como un recorrido de niveles, y que vea el progreso. Puedes
crear recursos con Magnific; si quieres crea en el space de los cabritos y deja los nodos para que yo los
reproduzca."

## 1. Qué es (y qué no)

- Un mapa de **progreso**, no un selector: los niveles siguen saliendo en orden (corrección de Andy en la v3,
  "no es que los elija"). Desde el mapa solo se juega el nivel actual.
- La idea: **los cabritos suben la montaña**. El nivel 1 está abajo y el recorrido sube. Cada tramo de 50
  niveles es una zona del ascenso y termina en una meta (50, 100, 150...), la misma "Próxima meta" del
  Inicio.

| Tramo | Zona | Ambiente (para el color de respaldo) |
|---|---|---|
| 1 a 50 | La pradera | pasto oscuro, flores, luz cálida de atardecer |
| 51 a 100 | El bosque | pinos, verde azulado, luciérnagas |
| 101 a 150 | La nieve | roca y hielo, azul frío, cristales de colores |
| 151 a 200 | La cumbre | cielo nocturno violeta con estrellas y aurora |
| 201 en adelante | se repiten las cuatro en ciclo, con "· vuelta 2", "· vuelta 3"... | igual |

## 2. Vista

- Vista propia `#vMapa` a pantalla completa (como `#vJuego`), con cabecera: botón volver (al Inicio),
  título "El recorrido" y el progreso de los dos ("Tú: nivel 37 · Andrés: nivel 12" o equivalente compacto).
- Se abre desde el Inicio: botón secundario "Ver el recorrido" debajo de "Jugar el nivel N" y tocando la
  barra de "Próxima meta". Al abrir, el nivel actual queda centrado en pantalla sin animación de scroll.
- Abajo, fijo: "Jugar el nivel N" (o "Seguir el nivel N" si hay partida a medias), igual que el Inicio.
- Camino: un sendero serpenteante (SVG) que une los nodos de abajo hacia arriba. Lo recorrido va sólido
  con el acento; lo que falta, punteado y tenue.
- Nodo por nivel (círculo, número adentro, mínimo 44 px de toque):
  - **Hecho**: relleno con el degradado de acento y sus estrellas (1 a 3) debajo.
  - **Actual**: más grande, anillo que late, y la cara del jugador encima.
  - **Futuro**: tenue, solo el número.
  - **Grado**: Fácil y Normal sin marca; Difícil, Muy difícil y Extra difícil con un borde o sello que se
    distinga (escalonado, el Extra el más fuerte). Se puede ver lo que viene: es parte de la gracia.
    Leyenda corta arriba del mapa o en la primera zona.
  - **Estreno** (L4, 7, 12, 20, 25, 30, 35, 50, 80): insignia con el icono de la mecánica (los SVG ya están
    en la página) y, al tocarlo si ya pasó, el nombre de la mecánica.
  - **Meta** (cada 50): nodo grande con bandera; al alcanzarla muestra la ilustración de la cima.
- **La pareja**: la cara del otro (Andrés o Cami) en su nivel, para que cada uno vea dónde va el otro. Mismo
  origen de datos que la tarjeta "Tú y Andrés/Cami" (`parejaAhora()` dentro de la app; fuera de la app, el
  otro perfil local de `S.perfiles`). Si están en el mismo nivel, las dos caras juntas.
- Al tocar:
  - nodo hecho: aviso corto con sus estrellas ("Nivel 12 · 3 estrellas"); no abre el juego.
  - nodo actual: abre el nivel actual.
  - nodo futuro: aviso corto "Primero el nivel N" (N = el actual); no abre nada.
- Cada zona empieza (abajo) con un **cartel de zona**: ilustración ancha que se funde con el fondo oscuro,
  "Tramo 1 · La pradera", "Niveles 1 a 50" y cuántos lleva de ese tramo.
- **Animación al volver**: si el jugador avanzó desde la última vez que vio el mapa, su cara camina del nodo
  anterior al actual (una vez; se guarda el último nivel visto en el perfil local, no en la nube). Respeta
  prefers-reduced-motion.

## 3. Imágenes (Magnific, las genera Andy)

Los nodos quedan creados en el space "Character Model Sheet Development" sin ejecutar. Huecos en la página:
`IMG.zona1` a `IMG.zona4` (carteles de zona, horizontales 16:9) e `IMG.cima` (los dos cabritos en la
cima con la bandera, para las metas). Mientras no existan, cada cartel usa un degradado propio de su zona y
la meta usa `IMG.botDuo`. El build debe funcionar con o sin esos archivos: marcador opcional
`@IMG?:nombre@` en build.py que da el data URI si existe `recursos/nombre.b64` y una cadena vacía si no.

Nodos creados el 2026-10-21 (image-generator, nano banana 2 flash, 1k, 16:9, sin ejecutar):

| Hueco | Pestaña | Nodo |
|---|---|---|
| zona1 · La pradera | Cami | 5926b2e9-b4ff-4da1-a643-3ff9bf7ae0bc |
| zona2 · El bosque | Cami | 32551dc1-f7ab-44c2-bce8-e1128776f9e3 |
| zona3 · La nieve | Cami | 5e66c720-9c16-4d69-9c93-197feba54e1b |
| zona4 · La cumbre | Cami | f0e90d4d-b14f-422e-916b-130cb9eb7cac |
| cima (dúo con bandera) | Andrés | 5266f4f0-7d8a-4099-a68d-0db97c69cdf8, con AND MAESTRO y la copia de CAMI MAESTRO conectados |

Cuando Andy los ejecute: bajar cada imagen, pasarla a JPEG de unos 900 px de ancho (calidad ~78) y
guardarla como data URI en `recursos/zona1.b64` ... `recursos/cima.b64`; el original va a
`recursos/originales/` (fuera de git).

Las cinco imágenes de arriba ya están generadas e integradas (Artifact versión 8, 2026-10-21).

Adornos para los lados del sendero (pedidos 2026-10-21, sin ejecutar). Son cuatro hojas 3x3 de 9 adornos
sobre gris #D9D9D9, cada una encadenada a un nodo image-background (mode remove). Todos van en la pestaña
Cami, debajo de su zona:

| Zona | Hoja | Sin fondo |
|---|---|---|
| pradera | 522a15b0-d8ad-4fa9-8c69-f1a081a93d6a | 9bcd7883-c8e2-43b5-83a0-e0204887ba14 |
| bosque | f96150fc-3af1-42ab-a71e-d97a2fd17322 | aed095f1-38da-4c0c-bd60-51878ee6e848 |
| nieve | 406fa2de-0fbb-48b3-b689-ca26bc5c1911 | 3234182c-2848-4c79-91bb-9cf045b8fcf0 |
| cumbre | bb1cb3bc-69e4-402c-9fa4-44c7d15d39e1 | 4b7e63ed-ee91-4d52-8281-8b2b7c254d82 |

Integración prevista:
- Bajar la versión sin fondo y cortar la cuadrícula en local.
- Hacer una hoja WebP con alfa por zona (liviana; iOS 14 o más).
- Esparcir los adornos a los lados del sendero, sin tocar nodos ni caras, con tamaño y semilla fijos por
  nivel para que no bailen.
- Darle a cada zona un tinte de fondo propio a lo largo de sus 50 niveles.

## 4. Rendimiento y casos

- Fluido con el nivel 1.000: se dibujan completas la zona actual, la anterior y la siguiente; las zonas
  viejas se resumen en una tarjeta ("Tramos 1 a 18 completos") que se puede abrir.
- 390 y 320 px sin scroll horizontal. Dentro de la app (`.enapp`) igual, sin dobles márgenes.
- Accesible: cada nodo con etiqueta ("Nivel 12, Normal, 3 estrellas", "Nivel 37, el actual, Extra difícil",
  "Nivel 40, todavía no"), el mapa como lista.

## 5. Pruebas (`pruebas-chrome.py`, sección "mapa")

Abrir desde el Inicio con toque real; el nivel actual dentro de la pantalla; nodos hechos = nivel − 1 y un
actual; cara de la pareja en su nivel (con un perfil de pareja de prueba); tocar hecho y futuro no abre el
juego; tocar el actual abre ese nivel; volver regresa al Inicio; 320 sin scroll horizontal; nivel 1.000 se
dibuja rápido (medir y reportar); el build sin las imágenes nuevas no falla. Capturas con prefijo v8-.
