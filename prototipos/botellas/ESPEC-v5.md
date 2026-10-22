# Botellas v5 · más difíciles, grado Extra difícil, sin botella extra y la receta de niveles (2026-10-21)

Todo lo de ESPEC-v4 sigue valiendo salvo lo que cambia aquí.

## 0. Ya hecho en la ronda anterior (Artifact versión 5)

- Lo cerrado (candado o caja) va tapado: gris opaco con un "?" por capa hasta que se abre (`.slot.tapada`).
- Sin Deshacer ni historial. Reiniciar (pregunta si hay movimientos) y Repetir sacan
  `MOTOR.variante(nv, semilla)`: otros colores y otro orden, misma solución traducida. La semilla va en
  `S.partida.vr`.
- El aviso de sin salida ofrece "Empezar de nuevo" (y la botella extra, que ahora se va).

## 1. Pedido de Andy

"Deberían haber más difíciles, porque si no se va a acabar muy rápido. Quita la opción de botella extra.
Deja algunos extra difíciles que en el nivel de aleatoriedad pueda que me sea imposible resolverlo. Para que
no tengas que diseñar cada nivel, piensa en cómo automatizamos o cómo formulamos que defina la cantidad de
botellas, colores y pruebas según el grado de dificultad; con eso nunca nos quedamos sin niveles."

Interpretación (se le explica así a Andy):
- Todo nivel sigue teniendo solución comprobada por el motor (eso no se negocia, lo pidió en la v2).
- "Imposible" es para la persona, no para el motor: en Extra difícil casi todo va tapado (misterio total,
  cajas y candados con su contenido escondido), no hay deshacer ni botella extra, así que una mala decisión
  a ciegas te deja sin salida y toca reiniciar con otros colores.

## 2. Cinco grados

`DIFS = ['facil', 'normal', 'dificil', 'muy', 'extra']`. Nombres: Fácil, Normal, Difícil, Muy difícil,
Extra difícil. El medidor pasa de 4 a 5 barritas (Fácil 1 ... Extra 5).

## 3. La receta: un nivel sale de (nivel L, grado), sin diseñarlo a mano

Un solo lugar del motor (`RECETA`, tabla comentada) define qué trae cada grado. `nivelParams(L)` =
sortear el grado (sección 4) + aplicar la receta. Sirve igual para el catálogo (1 a 200) y para los niveles
en vivo (201 en adelante, sin fin).

| | Fácil | Normal | Difícil | Muy difícil | Extra difícil |
|---|---|---|---|---|---|
| Colores | etapa − 1 | etapa | etapa + 1 | etapa + 2 | etapa + 3 |
| Pruebas (mecánicas ya estrenadas) | 0 o 1 | 1 | 1 o 2 | 2 o 3 | 3 (todas las que haya) |
| Misterio | no | a veces leve | leve; total desde L35 | total a veces | total siempre |
| Llave enterrada (hondo) | 0 | 0,5 | 1 | 1 | 1 |
| Vacías libres | 2 | 2 | 2 | 2 | 2 |
| Candidatos que se prueban | 6 | 6 | 8 | 12 | 16 |
| Franja que debe cumplir (bot = % que gana el jugador simulado) | bot ≥ 0,55 | 0,2 ≤ bot < 0,6 | bot < 0,25 y atasco ≥ 0,3 | bot ≤ 0,05 y atasco ≥ 0,5 | bot = 0 y atasco ≥ 0,65 |

- **Etapa** (colores de base según L): la tabla `coloresBase` de hoy (3 en L1 a 11 desde L141). Siempre
  entre 3 y 12 colores y el tope de 15 botellas (`topar`).
- **Pruebas** = candado, caja/cajón, misterio, botella gigante, dos cajas, cadena, cada una solo desde su
  estreno (ESTRENOS de la v4 no cambia). Largas sigue siendo cosa de Fácil/Normal y va sola.
- **Las pruebas del motor ("cada nivel se prueba antes de llegar a ti")**: cada candidato se resuelve (si no
  tiene solución se descarta) y lo juega 40 veces el jugador simulado (`jugarBot`). Se queda el candidato
  que cae en la franja de su grado; entre varios en franja, el más largo (meta) para los duros y el más
  corto para Fácil; si ninguno cae en la franja tras los candidatos, el más cercano a ella. Las franjas son
  el punto de partida: calibrarlas con el catálogo real y dejar los números finales en el INFORME.
- **En vivo (201+)** el mismo proceso con menos: 4 candidatos y 20 partidas del bot. Tiempo: Fácil, Normal y
  Difícil en 2 s o menos; Muy y Extra en 5 s o menos (el siguiente nivel ya se arma en segundo plano
  mientras se juega el actual).

## 4. Más duros: el sorteo del grado

Pesos (Fácil, Normal, Difícil, Muy, Extra), punto de partida:

| Tramo | F | N | D | M | X |
|---|---|---|---|---|---|
| L1-3 | 100 | 0 | 0 | 0 | 0 |
| L4-10 | 50 | 50 | 0 | 0 | 0 |
| L11-35 | 20 | 40 | 30 | 10 | 0 |
| L36-80 | 12 | 28 | 35 | 17 | 8 |
| L81-200 | 8 | 22 | 35 | 22 | 13 |
| L201+ | 6 | 18 | 34 | 25 | 17 |

Reglas (reemplazan "nunca dos duros seguidos"):
- Duro = Difícil, Muy o Extra. Máximo dos duros seguidos; después de dos, respiro (Fácil o Normal).
- Después de un Muy o un Extra, respiro.
- El estreno y su víspera no son duros (máximo Normal). Extra no sale antes de L36.
- Después de L10, nunca 4 Fáciles seguidos.

Meta de reparto en L1-200 (ajustar pesos hasta cumplirla y reportarla): duros ≥ 45 % (hoy 24 %), al menos
15 Extra, el primer Muy antes de L25 y el primer Extra entre L36 y L50. Desde L81, duros ≥ 55 %.

## 5. Sin botella extra (interfaz)

Fuera el botón, su insignia, `botellaExtra`, `g.extra`, `extraUsada` y la opción del aviso de sin salida
(queda solo "Empezar de nuevo"). La barra de abajo queda con Reiniciar solo, centrado. Se ajusta todo texto
que la mencione.

## 6. Interfaz para Extra difícil

- `DIF_INFO.extra = { nom:'Extra difícil', barras:5 }` y medidor de 5 barritas en todo lado (Inicio,
  aviso). Alturas escalonadas en CSS para las 5.
- Aviso antes del nivel (como Difícil y Muy), un poco más largo (~2,2 s): "Nivel extra difícil" / "Casi
  todo va tapado. Tiene solución, pero puede que no salga a la primera."
- Chip de la cabecera sin desbordar a 320 px con 3 rasgos.
- "Cómo se juega": la línea de dificultad nombra que de vez en cuando sale uno extra difícil.

## 7. El catálogo cambia: no restaurar partidas de otro nivel

Al rehacer `niveles.json`, una partida guardada del nivel L sería de un tablero que ya no existe. La partida
guarda `firma` = `MOTOR.hashCadena(JSON.stringify(base.botellas))` del nivel base (sin variante) y solo se
restaura si coincide; una partida sin firma o con otra firma se descarta y el nivel empieza de cero. Además,
la caché de niveles generados en vivo pasa a `botellas:niveles:v4` (borrar la v3).

## 8. Pruebas

- `pruebas-motor.js`: cinco grados, reglas nuevas del sorteo, franjas cumplidas (o reportar cuáles no),
  reparto de la sección 4, 200 con solución, variantes (bloque 1b) siguen pasando, en vivo 201-230 con
  tiempos de la sección 3.
- `pruebas-chrome.py`: sin `#cExtra`, barra con un control, aviso de sin salida con un solo botón, aviso y
  medidor de Extra, chip a 320 px, partida con firma vieja que no se restaura.
