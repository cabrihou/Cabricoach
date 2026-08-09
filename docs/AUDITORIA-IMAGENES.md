# Auditoría de imágenes · 09/08/2026

Revisión una por una de las **327 fotos de ejercicios** (`assets/ej/`) y las
**100 imágenes de interfaz** (`assets/cab/`). Resultado: **47 fotos a rehacer**.
Los nodos para rehacerlas ya existen en Magnific (ver abajo dónde).

## Dónde se rehacen (regla, no sugerencia)

Space **"Character Model Sheet Development"**, pestaña **`Andrés`** o **`Cami`**.
Ahí está la referencia del personaje conectada al puerto `reference` de cada nodo
`image-generator`; sin esa conexión sale otro personaje. Nunca en otro space.
Regla completa en [DESIGN-STANDARDS.md](DESIGN-STANDARDS.md) §5.

Nodos creados el 09/08 en la pestaña **Andrés**:

| Prefijo | Cuántos | Qué son |
|---|---|---|
| `MOV — <id>` | 14 | la rutina de movilidad completa |
| `EJ v2 — <id>` | 29 | ejercicios que salieron con la mascota vieja |
| `EJ pose — <id>` | 12 | fotos cuya pose no era el ejercicio |

Y en la pestaña **Cami**: `CAMI pose — c_lunge`.

## 1. Mascota de la primera generación (29)

Salieron con **la cabrita crema/blanca sobre brillo azul**, varias con **collar y
campana** (hoy prohibido). Son justo los ejercicios de las rutinas diarias de Andrés,
que hoy es el cabrito **tan/moreno**: su plan entero se ve con la mascota equivocada.

`calfse, calfst, curl, dip, facep, fly, hack, hammer, hip, incdb, incmach, latcab,
latcl, latdb, latop, lcurl, lext, lpress, lunge, ohpdb, preach, pullup, rdl, revfly,
row, rowuni, shpress, skull, tricab`

## 2. La pose no es el ejercicio (13)

| Foto | Qué muestra hoy |
|---|---|
| `floorpress` | de pie con la barra, debería estar acostado |
| `revfly_mach` | parada sin hacer nada |
| `tbar_row` | sostiene una mancuerna de pie |
| `row_seat_wide` | de pie, debería estar sentada |
| `vup` | una patada de pie |
| `muscleup` | hala una barra en el rack |
| `powersnatch` | peso muerto, nada por encima de la cabeza |
| `kneeraise_flat` | sentada con una barra |
| `squat_db` | parada, la mancuerna en el piso |
| `squat_bw` | **dos cabras duplicadas** en la misma escena |
| `jumpshrug` | salta con la barra en la espalda |
| `c_lunge` | camina con mancuernas sin flexionar (Cami) |
| `front_lever_tuck` | ver punto 3 |

## 3. Texto pegado en la imagen (2)

- `front_lever_tuck`: dice "FRONT LEVER HOLD".
- `shpress`: dice "CABRITA STRENGTH" en la base de la máquina, **y** tiene collar con
  campana, **y** es la mascota vieja. Triple problema.

## 4. Movilidad (5) · YA CORREGIDAS

`mov_sentadilla` (estaba de pie), `mov_tobillo` (sin pared), `mov_rana` (tumbada de
lado), `mov_bisagra` (erguida) y `mov_pared` (sin pared). Regeneradas e instaladas
el 09/08. Los nodos `MOV — …` quedan con el prompt afinado por si hay que repetirlas.

## Revisado y descartado (no son problema)

- El **"VS"** del hero de Retos y el **"CARGO"** del sticker del camión son texto
  intencional del diseño.
- `trapbar_dead` está bien: la barra sí es hexagonal.
- Iconos (`fic_*`, `ic*`), comidas, trofeos y stickers: coherentes con el sistema.
- Ninguna imagen de interfaz tiene cara humana ni collar.

## Cómo se hizo

Hojas de contactos etiquetadas (25 fotos por hoja) revisadas celda por celda, con los
originales abiertos en grande para los casos límite. Los criterios de marcado fueron:
texto pegado, personaje que no es la cabra, pose que no corresponde al nombre del
archivo, versión vieja del personaje (crema con azul, o collar/campana) y estilo ajeno
al sistema.
