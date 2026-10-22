# Informe de niveles (camino de 200)

Generado por `catalogo.py` (modo catalogo del motor). `bot` = fraccion de 40 partidas que gana el jugador
medio-aleatorio (en el catalogo y en vivo; 40 y 20 partidas); `atasco` = fraccion que termino sin jugadas. Tiempo total de reloj: 30 s.

## Resumen por dificultad

| Dificultad | Niveles | En su franja | Meta prom | Bot prom | Atasco prom | Colores | Llave | Candado | Cajon de 2 | Colores nuevos | Misterio | Largas | Gigante | No optimos |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Facil | 32 | 28 (88 %) | 16.5 | 0.827 | 0.086 | 3 a 10 | 5 | 5 | 1 | 1 | 5 | 0 | 3 | 0 |
| Normal | 75 | 66 (88 %) | 28.0 | 0.289 | 0.288 | 4 a 11 | 19 | 16 | 18 | 18 | 23 | 6 | 6 | 0 |
| Dificil | 50 | 46 (92 %) | 35.1 | 0.067 | 0.541 | 7 a 12 | 23 | 22 | 22 | 22 | 27 | 0 | 7 | 0 |
| Muy dificil | 25 | 25 (100 %) | 38.4 | 0.005 | 0.801 | 8 a 12 | 23 | 23 | 21 | 23 | 18 | 0 | 3 | 0 |
| Extra dificil | 18 | 17 (94 %) | 39.3 | 0.001 | 0.882 | 10 a 12 | 18 | 18 | 15 | 18 | 18 | 0 | 5 | 0 |

## Reparto por tramo de 50 niveles

| Tramo | Facil | Normal | Dificil | Muy dificil | Extra dificil | Duros |
|---|---|---|---|---|---|---|
| L1-50 | 21 | 15 | 9 | 4 | 1 | 14 (28 %) |
| L51-100 | 6 | 20 | 11 | 3 | 10 | 24 (48 %) |
| L101-150 | 2 | 23 | 11 | 9 | 5 | 25 (50 %) |
| L151-200 | 3 | 17 | 19 | 9 | 2 | 30 (60 %) |
| Total | 32 | 75 | 50 | 25 | 18 | 93 (46 %) |

Duros desde L81: 66 de 120 (55 %). Primer Muy: L13. Primer Extra: L37.

## Franjas de la receta (motor.js, RECETA)

| Grado | bot (gana el jugador simulado) | atasco minimo |
|---|---|---|
| Facil | 0.55 a 1 | 0 |
| Normal | 0.1 a 0.599 | 0 |
| Dificil | 0 a 0.249 | 0.3 |
| Muy dificil | 0 a 0.05 | 0.5 |
| Extra dificil | 0 a 0 | 0.65 |

## Meta promedio por tramo de 20 niveles (niveles de esa dificultad en el tramo entre parentesis)

| Tramo | Facil | Normal | Dificil | Muy dificil | Extra dificil | Todos |
|---|---|---|---|---|---|---|
| L1-20 | 8.3 (10) | 15.3 (6) | 22.5 (2) | 26.5 (2) | - | 13.7 |
| L21-40 | 14.1 (7) | 20.4 (7) | 25.0 (3) | 29.5 (2) | 34.0 (1) | 20.5 |
| L41-60 | 19.2 (4) | 24.5 (6) | 28.0 (8) | - | 38.5 (2) | 26.2 |
| L61-80 | 19.8 (4) | 26.6 (9) | 32.0 (1) | 34.0 (1) | 37.8 (5) | 28.6 |
| L81-100 | 23.0 (2) | 27.3 (7) | 33.0 (6) | 39.5 (2) | 41.0 (3) | 31.9 |
| L101-120 | - | 31.3 (9) | 36.0 (4) | 41.3 (3) | 40.8 (4) | 35.6 |
| L121-140 | 27.0 (1) | 30.4 (9) | 37.5 (4) | 41.6 (5) | 41.0 (1) | 35.0 |
| L141-160 | 30.0 (1) | 33.1 (9) | 40.4 (8) | 40.5 (2) | - | 36.6 |
| L161-180 | 29.0 (1) | 32.9 (7) | 39.2 (6) | 40.5 (4) | 40.0 (2) | 36.8 |
| L181-200 | 29.5 (2) | 33.5 (6) | 40.9 (8) | 39.8 (4) | - | 37.3 |

## Todos los niveles

| L | Dif | Colores | Botellas | Rasgos | Meta | Optimo | Bot | Atasco | En franja | Seg |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | facil | 3 | 5 | - | 6 | si | 1.000 | 0.000 | si | 0.0 |
| 2 | facil | 3 | 5 | - | 6 | si | 1.000 | 0.000 | si | 0.0 |
| 3 | facil | 3 | 5 | - | 5 | si | 1.000 | 0.000 | si | 0.0 |
| 4 | normal | 4 | 6 | candado | 12 | si | 0.425 | 0.000 | si | 0.0 |
| 5 | facil | 3 | 5 | candado | 6 | si | 1.000 | 0.000 | si | 0.0 |
| 6 | facil | 4 | 6 | - | 9 | si | 1.000 | 0.000 | si | 0.0 |
| 7 | facil | 4 | 6 | llave | 9 | si | 1.000 | 0.000 | si | 0.0 |
| 8 | facil | 4 | 6 | llave | 9 | si | 1.000 | 0.000 | si | 0.0 |
| 9 | normal | 5 | 7 | - | 16 | si | 0.875 | 0.125 | no | 0.1 |
| 10 | facil | 4 | 6 | - | 9 | si | 1.000 | 0.000 | si | 0.0 |
| 11 | facil | 4 | 6 | llave | 11 | si | 1.000 | 0.000 | si | 0.0 |
| 12 | normal | 5 | 7 | llave | 13 | si | 0.675 | 0.000 | no | 0.1 |
| 13 | muy | 8 | 10 | llave, candado | 27 | si | 0.000 | 0.950 | si | 0.2 |
| 14 | normal | 6 | 8 | llave | 15 | si | 0.575 | 0.000 | si | 0.1 |
| 15 | dificil | 7 | 9 | llave, candado | 24 | si | 0.100 | 0.650 | si | 0.1 |
| 16 | muy | 8 | 10 | llave, candado | 26 | si | 0.025 | 0.925 | si | 0.2 |
| 17 | normal | 6 | 8 | candado | 17 | si | 0.300 | 0.175 | si | 0.2 |
| 18 | dificil | 7 | 9 | llave | 21 | si | 0.450 | 0.275 | no | 0.2 |
| 19 | normal | 6 | 8 | candado | 19 | si | 0.250 | 0.375 | si | 0.1 |
| 20 | facil | 5 | 7 | misterio | 13 | si | 1.000 | 0.000 | si | 0.1 |
| 21 | facil | 5 | 7 | - | 13 | si | 1.000 | 0.000 | si | 0.1 |
| 22 | muy | 8 | 10 | llave, candado | 28 | si | 0.025 | 0.825 | si | 0.2 |
| 23 | facil | 5 | 7 | - | 13 | si | 1.000 | 0.000 | si | 0.1 |
| 24 | facil | 5 | 7 | llave | 12 | si | 1.000 | 0.000 | si | 0.1 |
| 25 | normal | 4 | 6 | largas | 20 | si | 0.925 | 0.000 | no | 0.1 |
| 26 | dificil | 8 | 10 | llave, misterio | 25 | si | 0.100 | 0.825 | si | 0.3 |
| 27 | dificil | 8 | 10 | llave, misterio | 22 | si | 0.100 | 0.525 | si | 0.3 |
| 28 | facil | 6 | 8 | - | 13 | si | 1.000 | 0.000 | si | 0.1 |
| 29 | facil | 6 | 8 | candado | 17 | si | 0.825 | 0.075 | si | 0.1 |
| 30 | normal | 7 | 9 | gigante | 19 | si | 0.700 | 0.100 | no | 0.8 |
| 31 | normal | 4 | 6 | largas | 21 | si | 0.975 | 0.000 | no | 0.1 |
| 32 | normal | 4 | 6 | largas | 16 | si | 0.850 | 0.000 | no | 0.1 |
| 33 | facil | 6 | 8 | candado, gigante | 14 | si | 1.000 | 0.000 | si | 0.1 |
| 34 | normal | 7 | 9 | misterio | 22 | si | 0.275 | 0.000 | si | 0.2 |
| 35 | normal | 7 | 9 | misterio | 22 | si | 0.450 | 0.250 | si | 0.1 |
| 36 | dificil | 8 | 10 | misterio | 28 | si | 0.075 | 0.375 | si | 0.3 |
| 37 | extra | 10 | 12 | llave, candado, misterio | 34 | si | 0.000 | 0.800 | si | 0.6 |
| 38 | facil | 6 | 8 | - | 17 | si | 0.750 | 0.000 | si | 0.1 |
| 39 | muy | 9 | 11 | llave, candado, misterio, gigante | 31 | si | 0.050 | 0.850 | si | 0.7 |
| 40 | normal | 7 | 9 | - | 23 | si | 0.275 | 0.200 | si | 0.1 |
| 41 | dificil | 8 | 10 | llave, candado | 27 | si | 0.025 | 0.475 | si | 0.1 |
| 42 | normal | 7 | 9 | - | 24 | si | 0.200 | 0.325 | si | 0.2 |
| 43 | dificil | 8 | 10 | llave, misterio, gigante | 24 | si | 0.675 | 0.150 | no | 0.2 |
| 44 | dificil | 8 | 10 | llave | 28 | si | 0.050 | 0.600 | si | 0.1 |
| 45 | facil | 6 | 8 | misterio | 17 | si | 0.900 | 0.000 | si | 0.1 |
| 46 | dificil | 9 | 11 | candado, gigante | 26 | si | 0.225 | 0.275 | no | 1.0 |
| 47 | facil | 7 | 9 | misterio | 19 | si | 0.650 | 0.275 | si | 0.2 |
| 48 | facil | 7 | 9 | - | 22 | si | 0.625 | 0.075 | si | 0.2 |
| 49 | facil | 7 | 9 | candado | 19 | si | 0.575 | 0.425 | si | 0.1 |
| 50 | normal | 8 | 10 | llave | 24 | si | 0.125 | 0.275 | si | 0.2 |
| 51 | dificil | 9 | 11 | misterio | 31 | si | 0.025 | 0.375 | si | 0.7 |
| 52 | dificil | 9 | 11 | candado | 30 | si | 0.000 | 0.800 | si | 0.1 |
| 53 | normal | 8 | 10 | candado | 24 | si | 0.175 | 0.150 | si | 0.1 |
| 54 | dificil | 9 | 11 | misterio | 31 | si | 0.025 | 0.300 | si | 0.7 |
| 55 | dificil | 9 | 11 | llave, misterio | 27 | si | 0.025 | 0.425 | si | 0.2 |
| 56 | normal | 8 | 10 | llave | 25 | si | 0.100 | 0.450 | si | 0.2 |
| 57 | extra | 11 | 13 | llave, candado, misterio | 37 | si | 0.000 | 0.975 | si | 0.8 |
| 58 | normal | 8 | 10 | misterio | 25 | si | 0.225 | 0.000 | si | 0.2 |
| 59 | extra | 11 | 13 | llave, candado, misterio | 40 | si | 0.000 | 1.000 | si | 0.4 |
| 60 | normal | 8 | 10 | misterio | 25 | si | 0.275 | 0.125 | si | 0.4 |
| 61 | extra | 11 | 13 | llave, candado, misterio | 35 | si | 0.000 | 0.825 | si | 0.7 |
| 62 | normal | 8 | 10 | misterio | 24 | si | 0.275 | 0.100 | si | 0.3 |
| 63 | normal | 8 | 10 | candado | 23 | si | 0.300 | 0.275 | si | 0.1 |
| 64 | muy | 10 | 12 | llave, candado, misterio | 34 | si | 0.000 | 0.975 | si | 0.4 |
| 65 | facil | 7 | 9 | llave | 18 | si | 0.575 | 0.400 | si | 0.1 |
| 66 | extra | 11 | 13 | llave, candado, misterio, gigante | 35 | si | 0.025 | 0.975 | no | 6.5 |
| 67 | facil | 7 | 9 | candado | 20 | si | 0.650 | 0.350 | si | 0.1 |
| 68 | facil | 7 | 9 | - | 18 | si | 0.700 | 0.150 | si | 0.1 |
| 69 | extra | 11 | 13 | llave, candado, misterio, gigante | 40 | si | 0.000 | 0.900 | si | 1.6 |
| 70 | normal | 8 | 10 | - | 25 | si | 0.275 | 0.150 | si | 0.4 |
| 71 | dificil | 10 | 12 | llave | 32 | si | 0.025 | 0.775 | si | 0.2 |
| 72 | normal | 9 | 11 | - | 27 | si | 0.275 | 0.300 | si | 0.4 |
| 73 | extra | 12 | 14 | llave, candado, misterio | 37 | si | 0.000 | 0.775 | si | 1.5 |
| 74 | facil | 8 | 10 | - | 23 | si | 0.900 | 0.000 | si | 0.2 |
| 75 | normal | 9 | 11 | misterio, gigante | 30 | si | 0.500 | 0.300 | si | 4.1 |
| 76 | normal | 9 | 11 | candado | 27 | si | 0.125 | 0.300 | si | 0.4 |
| 77 | extra | 12 | 14 | llave, candado, misterio, gigante | 42 | si | 0.000 | 0.675 | si | 7.2 |
| 78 | normal | 9 | 11 | misterio | 28 | si | 0.475 | 0.025 | si | 0.4 |
| 79 | normal | 9 | 11 | misterio | 27 | si | 0.450 | 0.325 | si | 0.4 |
| 80 | normal | 9 | 11 | llave | 28 | si | 0.575 | 0.300 | si | 0.3 |
| 81 | dificil | 10 | 12 | misterio | 33 | si | 0.225 | 0.300 | si | 1.0 |
| 82 | normal | 9 | 11 | misterio | 28 | si | 0.100 | 0.225 | si | 0.9 |
| 83 | facil | 8 | 10 | misterio, gigante | 23 | si | 0.975 | 0.000 | si | 0.4 |
| 84 | dificil | 10 | 12 | llave, misterio, gigante | 30 | si | 0.100 | 0.600 | si | 1.1 |
| 85 | muy | 11 | 13 | llave, candado, misterio | 39 | si | 0.000 | 0.975 | si | 0.5 |
| 86 | facil | 8 | 10 | gigante | 23 | si | 0.975 | 0.025 | si | 1.2 |
| 87 | extra | 12 | 14 | llave, candado, misterio, gigante | 42 | si | 0.000 | 1.000 | si | 5.0 |
| 88 | normal | 9 | 11 | candado | 27 | si | 0.225 | 0.700 | si | 0.3 |
| 89 | muy | 11 | 13 | llave, candado | 40 | si | 0.000 | 0.525 | si | 0.5 |
| 90 | normal | 9 | 11 | misterio | 27 | si | 0.175 | 0.150 | si | 0.4 |
| 91 | dificil | 10 | 12 | misterio | 34 | si | 0.100 | 0.425 | si | 0.8 |
| 92 | extra | 12 | 14 | llave, candado, misterio | 39 | si | 0.000 | 0.825 | si | 1.1 |
| 93 | normal | 9 | 11 | misterio | 26 | si | 0.200 | 0.000 | si | 0.8 |
| 94 | extra | 12 | 14 | llave, candado, misterio | 42 | si | 0.000 | 0.750 | si | 1.5 |
| 95 | normal | 9 | 11 | misterio | 28 | si | 0.500 | 0.150 | si | 0.7 |
| 96 | dificil | 10 | 12 | candado | 35 | si | 0.000 | 0.450 | si | 0.4 |
| 97 | dificil | 10 | 12 | misterio | 33 | si | 0.125 | 0.300 | si | 1.0 |
| 98 | normal | 9 | 11 | candado | 28 | si | 0.550 | 0.350 | si | 0.3 |
| 99 | dificil | 10 | 12 | candado, misterio | 33 | si | 0.025 | 0.425 | si | 0.3 |
| 100 | normal | 9 | 11 | misterio | 27 | si | 0.250 | 0.400 | si | 0.5 |
| 101 | normal | 10 | 12 | candado | 34 | si | 0.150 | 0.650 | si | 0.4 |
| 102 | normal | 10 | 12 | misterio | 32 | si | 0.100 | 0.250 | si | 1.1 |
| 103 | dificil | 11 | 13 | llave | 37 | si | 0.075 | 0.400 | si | 0.3 |
| 104 | extra | 12 | 14 | llave, candado, misterio | 40 | si | 0.000 | 0.900 | si | 1.1 |
| 105 | normal | 10 | 12 | candado | 29 | si | 0.100 | 0.600 | si | 0.5 |
| 106 | muy | 12 | 14 | llave, candado, misterio | 42 | si | 0.000 | 1.000 | si | 0.6 |
| 107 | normal | 10 | 12 | - | 31 | si | 0.175 | 0.500 | si | 0.7 |
| 108 | extra | 12 | 14 | llave, candado, misterio, gigante | 41 | si | 0.000 | 0.975 | si | 3.3 |
| 109 | normal | 10 | 12 | llave | 31 | si | 0.125 | 0.125 | si | 0.7 |
| 110 | dificil | 11 | 13 | candado | 40 | si | 0.000 | 0.900 | si | 0.5 |
| 111 | extra | 12 | 14 | llave, candado, misterio | 40 | si | 0.000 | 0.725 | si | 0.8 |
| 112 | normal | 10 | 12 | llave, gigante | 33 | si | 0.575 | 0.225 | si | 3.0 |
| 113 | muy | 12 | 14 | llave, candado, misterio | 40 | si | 0.000 | 0.900 | si | 0.7 |
| 114 | normal | 10 | 12 | - | 32 | si | 0.275 | 0.200 | si | 0.5 |
| 115 | muy | 12 | 14 | llave, candado, misterio | 42 | si | 0.000 | 0.575 | si | 0.8 |
| 116 | normal | 10 | 12 | llave | 30 | si | 0.225 | 0.375 | si | 0.4 |
| 117 | extra | 12 | 14 | llave, candado, misterio | 42 | si | 0.000 | 1.000 | si | 0.7 |
| 118 | normal | 10 | 12 | llave | 30 | si | 0.100 | 0.550 | si | 0.5 |
| 119 | dificil | 11 | 13 | misterio | 37 | si | 0.025 | 0.400 | si | 1.2 |
| 120 | dificil | 11 | 13 | llave, gigante | 30 | si | 0.325 | 0.500 | no | 4.4 |
| 121 | normal | 10 | 12 | llave | 30 | si | 0.275 | 0.500 | si | 0.5 |
| 122 | normal | 6 | 8 | largas | 29 | si | 0.250 | 0.025 | si | 0.3 |
| 123 | dificil | 11 | 13 | misterio | 36 | si | 0.000 | 0.575 | si | 1.2 |
| 124 | muy | 12 | 14 | llave, candado, misterio | 43 | si | 0.000 | 0.900 | si | 0.7 |
| 125 | normal | 10 | 12 | misterio | 31 | si | 0.250 | 0.225 | si | 0.6 |
| 126 | muy | 12 | 14 | llave, candado, misterio | 41 | si | 0.000 | 0.650 | si | 0.9 |
| 127 | normal | 10 | 12 | misterio | 30 | si | 0.225 | 0.350 | si | 1.3 |
| 128 | dificil | 11 | 13 | candado | 38 | si | 0.000 | 0.600 | si | 0.5 |
| 129 | dificil | 11 | 13 | candado, misterio | 38 | si | 0.000 | 0.775 | si | 0.5 |
| 130 | normal | 10 | 12 | - | 32 | si | 0.175 | 0.350 | si | 1.0 |
| 131 | muy | 12 | 14 | candado, misterio | 41 | si | 0.000 | 0.675 | si | 1.1 |
| 132 | facil | 9 | 11 | - | 27 | si | 0.775 | 0.000 | si | 0.2 |
| 133 | normal | 10 | 12 | misterio | 31 | si | 0.125 | 0.125 | si | 0.7 |
| 134 | extra | 12 | 14 | llave, candado, misterio | 41 | si | 0.000 | 0.900 | si | 0.8 |
| 135 | normal | 10 | 12 | candado | 32 | si | 0.125 | 0.275 | si | 0.5 |
| 136 | dificil | 11 | 13 | llave, misterio, gigante | 38 | si | 0.200 | 0.650 | si | 2.0 |
| 137 | normal | 10 | 12 | llave | 28 | si | 0.175 | 0.675 | si | 1.0 |
| 138 | muy | 12 | 14 | llave, candado, misterio | 41 | si | 0.000 | 0.750 | si | 1.1 |
| 139 | normal | 10 | 12 | misterio | 31 | si | 0.100 | 0.225 | si | 1.0 |
| 140 | muy | 12 | 14 | llave, candado | 42 | si | 0.000 | 0.775 | si | 0.9 |
| 141 | normal | 11 | 13 | llave | 34 | si | 0.275 | 0.525 | si | 0.6 |
| 142 | normal | 11 | 13 | gigante | 35 | si | 0.250 | 0.150 | si | 22.8 |
| 143 | facil | 10 | 12 | - | 30 | si | 0.375 | 0.250 | no | 0.9 |
| 144 | normal | 11 | 13 | candado, gigante | 33 | si | 0.200 | 0.375 | si | 4.9 |
| 145 | muy | 12 | 14 | llave, candado, misterio | 40 | si | 0.000 | 0.800 | si | 0.8 |
| 146 | normal | 11 | 13 | - | 32 | si | 0.200 | 0.600 | si | 1.6 |
| 147 | dificil | 12 | 14 | llave | 40 | si | 0.025 | 0.600 | si | 0.5 |
| 148 | dificil | 12 | 14 | candado, misterio | 40 | si | 0.000 | 0.700 | si | 1.0 |
| 149 | normal | 11 | 13 | misterio | 35 | si | 0.175 | 0.325 | si | 1.5 |
| 150 | dificil | 12 | 14 | llave, candado | 40 | si | 0.000 | 0.425 | si | 0.5 |
| 151 | dificil | 12 | 14 | llave | 41 | si | 0.000 | 0.725 | si | 0.5 |
| 152 | normal | 11 | 13 | misterio | 32 | si | 0.100 | 0.400 | si | 1.1 |
| 153 | muy | 12 | 14 | llave, candado, misterio | 41 | si | 0.000 | 0.725 | si | 0.7 |
| 154 | normal | 11 | 13 | misterio | 34 | si | 0.150 | 0.450 | si | 1.2 |
| 155 | dificil | 12 | 14 | llave | 41 | si | 0.000 | 0.625 | si | 0.5 |
| 156 | normal | 11 | 13 | llave | 31 | si | 0.125 | 0.300 | si | 1.1 |
| 157 | dificil | 12 | 14 | candado | 41 | si | 0.000 | 0.675 | si | 0.8 |
| 158 | dificil | 12 | 14 | candado | 40 | si | 0.000 | 0.950 | si | 0.8 |
| 159 | normal | 11 | 13 | candado | 32 | si | 0.075 | 0.925 | no | 0.9 |
| 160 | dificil | 12 | 14 | llave, candado | 40 | si | 0.025 | 0.550 | si | 0.6 |
| 161 | extra | 12 | 14 | llave, candado, misterio | 40 | si | 0.000 | 0.925 | si | 0.7 |
| 162 | normal | 11 | 13 | candado | 32 | si | 0.025 | 0.575 | no | 0.6 |
| 163 | extra | 12 | 14 | llave, candado, misterio | 40 | si | 0.000 | 0.950 | si | 0.7 |
| 164 | normal | 11 | 13 | llave | 33 | si | 0.175 | 0.150 | si | 1.1 |
| 165 | muy | 12 | 14 | llave, candado, misterio | 42 | si | 0.000 | 0.575 | si | 0.7 |
| 166 | normal | 11 | 13 | candado | 36 | si | 0.050 | 0.200 | no | 0.7 |
| 167 | dificil | 12 | 14 | llave | 41 | si | 0.000 | 0.650 | si | 0.5 |
| 168 | muy | 12 | 14 | llave, candado | 40 | si | 0.000 | 0.850 | si | 0.6 |
| 169 | normal | 11 | 13 | misterio | 34 | si | 0.300 | 0.450 | si | 1.2 |
| 170 | dificil | 12 | 14 | misterio, gigante | 36 | si | 0.150 | 0.500 | si | 26.4 |
| 171 | dificil | 12 | 14 | candado, misterio | 41 | si | 0.025 | 0.575 | si | 0.9 |
| 172 | normal | 11 | 13 | llave | 33 | si | 0.125 | 0.050 | si | 1.1 |
| 173 | dificil | 12 | 14 | candado, misterio | 39 | si | 0.000 | 0.300 | si | 0.7 |
| 174 | normal | 6 | 8 | largas | 27 | si | 0.525 | 0.075 | si | 0.1 |
| 175 | dificil | 12 | 14 | candado, misterio, gigante | 39 | si | 0.050 | 0.875 | si | 8.1 |
| 176 | facil | 10 | 12 | misterio | 29 | si | 0.275 | 0.075 | no | 0.6 |
| 177 | muy | 12 | 14 | llave, misterio | 39 | si | 0.000 | 0.825 | si | 1.1 |
| 178 | normal | 11 | 13 | misterio | 35 | si | 0.100 | 0.400 | si | 0.7 |
| 179 | dificil | 12 | 14 | llave | 39 | si | 0.000 | 0.350 | si | 1.0 |
| 180 | muy | 12 | 14 | llave, candado, misterio, gigante | 41 | si | 0.025 | 0.800 | si | 9.7 |
| 181 | normal | 11 | 13 | llave, gigante | 35 | si | 0.375 | 0.300 | si | 24.0 |
| 182 | dificil | 12 | 14 | candado, misterio | 40 | si | 0.000 | 0.525 | si | 0.9 |
| 183 | normal | 11 | 13 | llave | 33 | si | 0.125 | 0.725 | si | 0.9 |
| 184 | dificil | 12 | 14 | candado, misterio | 41 | si | 0.000 | 0.325 | si | 0.9 |
| 185 | muy | 12 | 14 | llave, misterio | 39 | si | 0.000 | 0.800 | si | 1.2 |
| 186 | normal | 6 | 8 | largas | 29 | si | 0.400 | 0.175 | si | 0.2 |
| 187 | dificil | 12 | 14 | llave, candado | 43 | si | 0.000 | 0.400 | si | 0.4 |
| 188 | muy | 12 | 14 | llave, candado, misterio, gigante | 38 | si | 0.000 | 0.625 | si | 10.5 |
| 189 | normal | 11 | 13 | candado | 37 | si | 0.150 | 0.775 | si | 0.5 |
| 190 | dificil | 12 | 14 | candado | 42 | si | 0.000 | 0.300 | si | 1.0 |
| 191 | dificil | 12 | 14 | llave, misterio | 38 | si | 0.000 | 0.900 | si | 1.0 |
| 192 | normal | 11 | 13 | llave | 31 | si | 0.200 | 0.175 | si | 0.5 |
| 193 | dificil | 12 | 14 | llave, misterio | 40 | si | 0.000 | 0.825 | si | 0.5 |
| 194 | muy | 12 | 14 | candado, misterio | 41 | si | 0.000 | 0.775 | si | 0.7 |
| 195 | facil | 10 | 12 | - | 29 | si | 0.475 | 0.100 | no | 0.4 |
| 196 | facil | 10 | 12 | - | 30 | si | 0.450 | 0.550 | no | 0.6 |
| 197 | muy | 12 | 14 | llave, candado | 41 | si | 0.000 | 1.000 | si | 0.7 |
| 198 | normal | 11 | 13 | llave | 36 | si | 0.150 | 0.675 | si | 0.9 |
| 199 | dificil | 12 | 14 | misterio | 41 | si | 0.000 | 0.350 | si | 1.1 |
| 200 | dificil | 12 | 14 | candado, misterio | 42 | si | 0.000 | 0.800 | si | 0.7 |