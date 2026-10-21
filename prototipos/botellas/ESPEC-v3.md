# Botellas v3 · un solo camino con dificultad al azar

Corrección de Andy (2026-10-21) sobre la v2: **"Los niveles van saliendo, no es que los elija,
es aleatorio."** Como en el juego de Cami: no se escoge ruta ni nivel. Los niveles salen uno
detrás de otro y cada uno trae su dificultad (Fácil, Normal, Difícil o Muy difícil) sorteada.

Se conserva todo lo de la v2 que no choca con esto: reglas y núcleo (llaves, cajas, candados),
generador con mecánicas, métricas `bot`/`atasco`, garantía de solución, misterio justo,
animaciones, hoja de Novedad, reto del día (por día de la semana, sin cambios), Worker, contrato
del Artifact. Se quitan: las 4 rutas, el selector de dificultad y el mapa de niveles.

## 1. Motor (frente A)

### 1.1 `nivelParams(L)` (L ≥ 1, sin tope)
Devuelve la misma forma que `rutaParams` más `ruta:'camino'`, `L`, `id:'camino-L'` y `dif`.

**Dificultad sorteada** `difDe(L)`: determinista (rng `'dif:'+L`), calculada en orden desde L=1
(depende de la anterior; memorizar). Pesos por tramo:

| Tramo | Fácil | Normal | Difícil | Muy difícil |
|---|---|---|---|---|
| L1-3 | 100 | 0 | 0 | 0 |
| L4-10 | 60 | 40 | 0 | 0 |
| L11-29 | 35 | 45 | 20 | 0 |
| L30-100 | 25 | 45 | 20 | 10 |
| L101+ | 20 | 40 | 25 | 15 |

Reglas encima del sorteo: nunca dos seguidos entre Difícil y Muy difícil; después de un Muy
difícil viene un Fácil; después de L10, nunca cuatro Fáciles seguidos (el cuarto pasa a Normal);
los niveles que estrenan mecánica y el anterior a cada uno no son difíciles (Fácil o Normal).

**Colores**: base por L: L1-2: 3, L3-5: 4, L6-12: 5, L13-25: 6, L26-45: 7, L46-70: 8, L71-100: 9,
L101-140: 10, L141+: 11. Ajuste por dificultad: Fácil −1, Normal 0, Difícil +1, Muy difícil +2
(piso 3, techo 12). Total de botellas ≤ 15.

**Estreno de mecánicas** (nivel fijo, siempre Fácil o Normal, con su Novedad en la interfaz):
L4 candado en vacía, L7 llave con caja vacía, L12 candado con líquido, L16 llave con caja de
líquido, L20 misterio leve, L25 largas, L35 misterio total, L50 dos cajas, L80 cadena.

**Después del estreno**, cada nivel sortea sus mecánicas (rng `'mec:'+L`) entre las ya
estrenadas: Fácil 0 o 1, Normal 1 (a veces 0), Difícil 1 o 2, Muy difícil 2 o 3. Largas de vez en
cuando en Fácil y Normal (cap 6, colores n−3). Misterio leve en Fácil y Normal, total en Difícil y
Muy difícil (una vez estrenado). Con una sola vacía libre, solo caja con vacía (lo que ya mediste
que tiene salida); el candado vacío siempre con 2 libres.

**Elección** entre candidatos según `dif`, como en `rutaParams` (Fácil la más fácil, Normal la
mediana, Difícil la de mayor meta, Muy difícil la de mayor `meta + 15·(1−bot)`).

Más allá de 200: la misma función, generada en el teléfono en modo rápido (≤ 2 s).

### 1.2 Catálogo
`niveles.json` = `{ version:3, generado, camino:[200 niveles] }` con el formato de nivel v2
(`id:'camino-L'`, `ruta:'camino'`, `L`, `dif`, `rasgos`, `meta`, `movs`, `bot`, `atasco`...).
`INFORME-NIVELES.md`: tabla por nivel (L, dif, colores, botellas, rasgos, meta, bot, atasco) y
resúmenes: cuántos de cada dificultad, promedios por dificultad, y por tramo de 20 niveles la meta
promedio por dificultad. `rutaParams` puede quedarse como función interna si sirve.

### 1.3 Pruebas
Las de la v2 sobre los 200 (solución que gana, meta = movs, estructura, llaves, candados, cajas,
rasgos), más: L correlativos e id `camino-L`; las reglas de dificultad (sin dos difíciles
seguidos, Fácil después de Muy difícil, sin cuatro Fáciles seguidos después de L10, estrenos en
su nivel y no difíciles); dentro de cada tramo de 50, meta promedio Fácil < Normal < Difícil <
Muy difícil (donde haya); la meta promedio de los Normales sube por tramos de 50 sin saltos de más
de 50 %. En vivo: niveles 201-205 y 14 retos del día, deterministas y ≤ 2 s.

## 2. Interfaz (frente B)

- **Inicio**: héroe con `.t-label` "CAMINO", `.bignum` "Nivel 37", la línea "8 colores · 10
  botellas · Llave", la **insignia de dificultad** del nivel (medidor de 1 a 4 barritas y el
  nombre: Fácil, Normal, Difícil, Muy difícil), la vista previa, "Jugar el nivel 37" (o "Seguir")
  y una barra fina de progreso "37 de 200". Se quitan la grilla de rutas, el mapa y "Ver los 50
  niveles". El reto del día queda igual. Estadísticas: Niveles (de 200), Estrellas, Mejor racha.
  "Cómo se juega": agregar **La dificultad sale al azar.** Unos niveles son de respiro y otros
  más duros; todos tienen solución.
- **Aviso de nivel difícil**: al abrir un Difícil o Muy difícil (no al retomarlo a medias, ni en
  "Repetir"), antes de jugar, una tarjeta sobre el tablero de ~1,4 s (se salta con un toque):
  el medidor grande, "Nivel difícil" o "Nivel muy difícil" y una línea: "Con calma: tiene
  solución." / "De los duros. Tiene solución comprobada." Entra con escala y sale con fundido;
  con movimiento reducido, solo fundido. Si además hay Novedad, primero el aviso y luego la hoja.
- **Juego**: el chip dice la dificultad y los rasgos ("Difícil · Llave"). Hoja de ganar: etiqueta
  "Nivel 37 · Difícil", botón "Siguiente nivel". En el 200: "Completaste los 200 niveles" y
  "Seguir con el nivel 201". "Repetir" se queda (es el mismo nivel, no se escoge otro).
- **Persistencia**: perfil `{ nivel, estrellas, dias, racha, stats, vistos }`. El progreso por
  rutas de la v2 se guarda en `legado` y no se usa. Partida `modo:'camino'`; una de la v2
  (`modo:'ruta'`) se descarta. Caché `botellas:niveles:v3`.
- **URL**: `#nivel37` y `#dia` (se quitan las de rutas y mapa).
- **build.py**: `CATALOGO.camino[L-1]`; la muestra corta pasa al formato v3.
- **Capturas**: inicio (390 y 320), aviso de difícil y de muy difícil, un nivel de cada
  dificultad, llave y candado (siguen), Muy difícil a 320 con la extra, ganar en el 200. Sin
  errores de JS ni scroll horizontal.
