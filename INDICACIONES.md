# Indicaciones de Andy (sesión 30/07/2026)

Registro de los pedidos enviados durante la sesión, en orden. Estado al margen.

## Lote 1 (retomado tras el bloqueo de iCloud) — HECHO en REV 97

1. Peso: número grande abre registro (slider + input texto), ventana centrada.
2. PIN al abrir: bloquear por defecto + centrar ventana.
3. Caja rotativa: cambia al toque + cada 20 s + planea semana/datos curiosos.
4. Caja de pasos: quitar la palabra "actualizar".
5. Eliminar deslizar-para-iniciar, botón normal.
6. Borrar series: reemplazar swipe por botón de borrar.
7. Teclado: evitar que la app se mueva raro al escribir.
8. Fotos: vista de semana por defecto + botón para activar vista de fotos.
9. Evitar mayúsculas sostenidas, revisar tipografía y jerarquía.
10. Analizar y simplificar la sección Progreso.
11. Unificar interfaz de ingreso de comida.
12. XP por hábitos.
13. Pase de accesibilidad (role/tabindex) — parcial: quedan ~50 botones sin nombre.
14. Bump REV, tests, auditar, publicar, informe.

## Mensaje intermedio (con captura de la gráfica de proteína) — HECHO en REV 97

- La estadística solo se activa al tocar; abajo de la gráfica, caja de sugerencias
  de comidas que ayuden con el restante del día (estilo caja "planea tu semana").
- Revisar el cálculo de agua del día ("no sé si debe ser más") →
  quedó 35 ml/kg + 500 ml en día de entreno, ajustable a mano.

## Lote 2 (13 puntos + captura por punto) — HECHO en REV 98

1. Hero inicial: icono perdido en el lado izquierdo → eliminado.
2. Eliminar la caja "Hora de entrenar" (ya está en el checkpoint del día).
3. Caja rotativa: imágenes coherentes con el texto; "planea tu semana" debe llevar
   al organizador de entrenos (llevaba al check-in general); recordatorios llevaban
   a otro lado → destinos corregidos.
4. Nutrición: meta pequeña a la derecha; cada macro como rejilla (número+indicador
   dominando, nombre abajo, meta abajo a la derecha).
5. El texto de la gráfica de proteína no aparece de inmediato: solo al dar click a
   una barra.
6. Jerarquía tipográfica de "Con qué cerrar" + sugerencias por GRUPOS de comida
   (ej.: 100 g de pollo + 2 claras = un grupo; ofrecer varios grupos).
7. Las dos cajas del home como ventanas flotantes con botones circulares arriba a
   la derecha; en los botones de inicio la flecha final pasa a ser un check que
   completa todas las series/ejercicios con pesos y reps preestablecidos; la caja
   se despliega tocando cualquier lugar.  ← REVERTIDO parcialmente en Lote 3.
8. Rediseñar botones Semana/Mes/Fotos del calendario con iconos; botón de cámara
   que cambia la visual del calendario y muestra las fotos con animación de giro
   de tarjetas (manteniendo estructura y caja del calendario).
9. Días de cada rutina: flecha a la derecha; opción de crear alerta en el
   calendario para todos los entrenos; casilla de hora para setear la hora.
10. Fotos: mejores iconos para antes/después, mejor diagramación, eliminar la caja
    Composición, "Tomar hoy" como cajita con la cabrita fotografiándose; Fotos como
    sección independiente fuera de Progreso.
11. Check-in fuera del deslizable de Progreso; entrada solo desde la caja del home.
12. Progreso en dos grupos grandes: Actividad física y Nutrición (verde).
13. Sistema tipográfico "Opción 4" aplicado a TODA la app, con delegación a otros
    agentes y auditoría final:
    - Display: League Spartan ExtraBold 800, 48-64 px, mayúsculas, 1 por pantalla.
    - H1: Outfit SemiBold 600, 28-32 px, caja de oración, 1 por vista.
    - H2: Outfit Medium 500 (600 si énfasis), 20-24 px.
    - Métrica XL: Archivo Bold 700, 40-56 px, cifras tabulares; unidad 40-60%
      más pequeña, peso menor, alineada a línea base.
    - Métrica mediana: Archivo SemiBold 600, 24-36 px.
    - Body: Instrument Sans Regular 400, 16 px (secundario 14-15), sin mayúsculas
      sostenidas, sin justificar.
    - Label: Instrument Sans Medium 500, 12-13 px, tracking 4-6%, mayúsculas solo
      si es corto.
    - Botón: Instrument Sans SemiBold 600, 15-16 px, caja de oración, verbos de
      acción; jerarquía por fondo/borde, no por fuente.
    - Color: acento reservado a acciones/estados/métrica principal; máx. 2 colores
      tipográficos por tarjeta; estados siempre acompañados de icono o texto.

## Lote 3 (nuevo, en curso)

Progreso:
- Rendimiento y Tendencia de peso son muy similares → quedarse con Rendimiento.
- El scroll entre Actividad física y Nutrición va arriba, con una cabrita en cada
  uno (entrenando / comiendo); el scroll se mueve para elegir.
- Rendimiento debajo; en la esquina superior derecha se elige el intervalo.
- 6 botones: General, Peso, Volumen, Tiempo, Fuerza, Pasos.
- En Peso: chips de selección Diario / Promedio semanal.
- Los 3 medidores (Fuerza/Resistencia/Movilidad) cambian según la categoría,
  asociados a la temática de la gráfica.

Nutrición:
- Sección de preparación e instrucciones en las recetas del meal prep.
- Faltan desayunos dentro de alimentación para el mercado (ej. avena trasnochada).
- Caja de sugerencias tipo formulario para describir una receta vista o recordada:
  investigar, calcular y medir porciones.
- Lista de compras agrupada por categorías (proteínas, vegetales, supermercado).
- Suma parcial de lo que ya está registrado/marcado.
- Cargar fotos de facturas para leer el precio, pasarlo a texto, guardarlo y
  sugerir dónde comprar o cuál fue el último valor. → Acordado: solución gratuita
  sin OCR (foto adjunta + precio manual + histórico local).
- En "agregar elemento": sugerencias de elementos ya diligenciados antes.

Ajustes sobre el Lote 2:
- Punto 7: reincorporar las cajas flotantes al home (revertir el overlay).
- Punto 8: eliminar la pestaña Fotos del calendario; solo Semana y Mes; el cambio
  de visual queda solo en el icono de cámara.
- "Con qué cerrar": revisar jerarquía tipográfica (no funciona bien) y volverla
  caja cerrada que se despliega al click.

Método pedido: Claude planea y audita; agentes más económicos ejecutan.
Solución gratuita para todo el lote nuevo.

## Pregunta aparte (respondida)

¿Hay forma de conectarse con `claude -p`, en vivo, o activarse a una hora del día
para evaluar lo del día? → Sí: `claude -p` + cron/launchd en el Mac, /loop en
sesión abierta, o agentes programados en la nube. El límite es el acceso a datos:
localStorage del teléfono no es alcanzable; vía Supabase sí.
