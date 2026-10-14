#!/usr/bin/env python3
"""Semilla del lote 2026-10-14b: la segunda pasada con el plugin Design de Anthropic.

Skills usadas: design-critique, accessibility-review, ux-copy, design-system y
user-research (plugin design@knowledge-work-plugins 1.2.0). Solo lleva lo NUEVO
frente al lote 2026-10-14; lo que confirmo y lo que no cubre va en el informe
General. Escribe JSON en semilla/<coleccion>/ y lotes_b.json para ArtifactData.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
LOTE = '2026-10-14b'
docs = []
COMO = 'Segunda pasada, con el plugin Design de Anthropic. Marca Va en lo que quieres que haga y usa Responder si lo quieres distinto. El informe del primer análisis sigue abajo.'


def informe(sec, lead, items, extras=None, verificacion=None):
    docs.append(('informes', f'{LOTE}-{sec}', {
        'seccion': sec, 'lote': LOTE, 'titulo': 'Segunda pasada con la skill Design · 14 de octubre',
        'lead': lead, 'columnas': ['Hallazgo', 'Propuesta'], 'okTexto': 'Va', 'comoUsar': COMO,
        'items': [{'codigo': c, 'tipo': t, 'impacto': im, 'esfuerzo': es, 'pedido': h, 'hecho': p, **({'zona': z} if z else {})} for (c, z, t, im, es, h, p) in items],
        'decisiones': [], 'pendiente': [], 'verificacion': verificacion, 'extras': extras or [], 'revisar': [], 'revisado': {}, 'archivado': {},
    }))


GENERAL = [
    ('DG01', 'Controles', 'Accesibilidad · WCAG 1.4.11', 'alto', 'bajo', 'Los bordes de campos y controles pendientes casi no se ven: inputs, círculos de serie sin marcar, el check pendiente, casillas y chips de contorno van a 1,26:1 contra el fondo (el mínimo para controles es 3:1). Con el brillo bajo, en el gimnasio, el campo de kg y la serie sin marcar se confunden con la tarjeta.', 'Un token de borde para controles que dé al menos 3:1 (por ejemplo blanco al 32 %) y dejar el borde actual solo para separadores decorativos.'),
    ('DG02', 'Controles', 'Accesibilidad · WCAG 4.1.2 y 2.1.1', 'medio', 'medio', 'Los controles no dicen su estado y varios no se alcanzan con el teclado: 0 de 9 interruptores anuncian si están encendidos (uno es un div), los segmentados no marcan cuál está activo (solo Progreso lo hace) y hay cosas tocables sin foco: 35 de 50 en la sesión, las 10 filas del Mercado y la tira de días y la tarjeta de Medidas en el Inicio.', 'Interruptores como botón con rol de interruptor y su estado; estado marcado en segmentados y pestañas; y un manejador global que haga enfocables y activables con Enter todos los elementos con data-a que no son botón.'),
    ('DG03', 'Estructura', 'Accesibilidad · WCAG 1.3.1', 'medio', 'bajo', 'Las pantallas no tienen títulos reales: el Inicio tiene 1 encabezado, Más y Progreso ninguno, aunque se ven 16 y 8 títulos de sección. Con VoiceOver no se puede saltar de sección en sección.', 'Los títulos de tarjeta como encabezados h2 y un h1 por vista, sin cambio visual.'),
    ('DG04', 'Formularios', 'Accesibilidad · WCAG 3.3.1 y 3.3.2', 'medio', 'bajo', 'Campos sin nombre y errores que se van: en Más 8 de 16 campos solo tienen el texto de ejemplo (el PIN dice «4 dígitos»), en la sesión los de reps no tienen nombre y en el Mercado tampoco el ítem libre ni el precio. Los 17 errores de validación son un aviso de 2,6 s que no marca el campo.', 'Nombre en cada campo y, al validar, el campo marcado con su error escrito debajo, además del aviso.'),
    ('DG05', 'Avisos', 'Accesibilidad · WCAG 2.2.1', 'medio', 'bajo', 'Los avisos duran 2,6 s sin importar su largo y el Deshacer 6 s, sin forma de pausarlos. «Pasos guardados solo en este navegador · conecta la nube en Más para que lleguen a la app» no alcanza a leerse; deshacer un borrado con la mano ocupada tampoco.', 'Duración según el largo (mínimo 2,5 s), pausa mientras el dedo está encima y Deshacer de 10 s en los borrados.'),
    ('DG06', 'Zoom', 'Accesibilidad · WCAG 1.4.4', 'medio', 'alto', 'Al 200 % la app se rompe: el peso del héroe desaparece, los nodos del checkpoint se montan uno encima de otro y la tira de días y las tarjetas se cortan (medido a 195 px, que equivale al 200 % en el iPhone). A 320 px no hay desborde. Importa porque el primer informe propone liberar el zoom (G13).', 'Antes de liberar el zoom, que el héroe y el checkpoint se reacomoden cuando no caben, y probar a 195 px.'),
    ('DG07', 'Animaciones', 'Accesibilidad · WCAG 2.2.2', 'bajo', 'bajo', 'Las cabritas en video y la cabrita flotante se mueven sin parar y sin botón de pausa; solo se detienen si el iPhone tiene «Reducir movimiento».', 'Que se detengan solas a los 5 s o al tocarlas, o un ajuste «Animaciones» en Preferencias.'),
    ('DG08', 'Confirmaciones', 'Texto · ux-copy', 'alto', 'medio', '22 confirmaciones usan el diálogo nativo, que en iOS solo ofrece «Cancelar» y «Aceptar»: hay que leer la pregunta para saber qué hace Aceptar. Solo 8 dicen la consecuencia y 2 tienen Deshacer; la de pegar registros explica en el texto que «Aceptar» reemplaza y «Cancelar» suma. La hoja propia de series pendientes al terminar, con botones con verbo, es el modelo.', 'Una hoja de confirmación propia: título con la acción, la consecuencia y botones con verbo («Borrar sesión» / «Conservar»). Si el borrado es reversible, sin diálogo: se borra de una con Deshacer.'),
    ('DG09', 'Errores', 'Texto · ux-copy', 'medio', 'bajo', 'Unos 15 errores dicen qué falló pero no qué hacer: «No pude abrir la cámara (permiso)», «No pude guardar la foto», «No pude exportar». El de la cámara tiene una salida concreta en iOS que no se dice.', 'Qué pasó, por qué y cómo arreglarlo: «Falta el permiso de la cámara. Actívalo en Ajustes > Safari > Cámara y vuelve».'),
    ('DG10', 'Estados vacíos', 'Texto · ux-copy', 'medio', 'bajo', 'De 31 estados vacíos, 17 no traen botón para empezar; el gráfico vacío solo dice «Sin datos todavía». El modelo ya está en la app: «Todavía no hay rotación activa», con ilustración, explicación y «Ármame la semana».', 'Cada vacío con qué es, por qué está vacío y un botón para empezar («Registra tu primer peso»).'),
    ('DG11', 'Botones', 'Texto · ux-copy', 'bajo', 'bajo', '35 botones genéricos o sin verbo: «Cancelar» (10), «Listo» (3), «Hecha», «IR», «Guardar» a secas en peso y pasos, «Conectar», «Medir».', 'Verbo y objeto: «Registrar inyección», «Ir a esa fecha», «Guardar peso», «Dejar así».'),
    ('DG12', 'Esperas', 'Texto · ux-copy', 'medio', 'bajo', '«Subiendo todo…» vuelve a pintar a los 1,5 s sin esperar la subida real ni decir si salió bien; «Cargando…» en la galería no dice qué ni cuánto. Solo el guardado de un lote de fotos pone expectativa (barra y «no cierres la app»).', 'Cada espera dice qué hace y cuánto tarda, y siempre cierra: «Todo al día en la nube» o el error.'),
    ('DG13', 'Sistema', 'Sistema de diseño', 'medio', 'alto', 'Los colores están bien tokenizados, pero no hay escala de espaciado, de letra ni de movimiento: 37 valores de espaciado (67 % no son múltiplo de 4), 33 tamaños de letra, 30 duraciones y 59 sombras distintas. Los radios tienen token y solo 2,8 % de las 363 declaraciones lo usan; las clases tipográficas oficiales aparecen en el 1,6 % de los elementos. Auditoría: 54/100.', 'Tres escalas nuevas (espaciado 4, 8, 12, 16, 24, 32; unos 8 tamaños de letra; movimiento rápido, normal y lento con la curva de la app) y migración por vista, en cada lote que toque esa vista.'),
    ('DG14', 'Sistema', 'Sistema de diseño', 'bajo', 'bajo', 'El estándar escrito no coincide con el código: radios 20/14/12 documentados contra 26/16/13 en el CSS, --smoke #737C79 contra #828C89, un glow verde agua que ya no existe y «28 etiquetas bajo 12 px» contra 135 medidas. --mint vale azul y --white vale casi negro.', 'Poner DESIGN-STANDARDS con las cifras reales (o el CSS con las del estándar) y renombrar --mint a --accent y --white a --surface-2.'),
    ('DG15', 'Sistema', 'Sistema de diseño', 'bajo', 'medio', 'Los componentes no tienen estados de carga ni de error, solo hay 4 reglas de deshabilitado en toda la hoja, y conviven 11 clases de chip, 15 de botón por fuera de .btn y 9 primas de la tarjeta .mod.', 'Estados .btn cargando, .in con error y deshabilitado, y chips, botones y tarjetas consolidados en un componente con variantes.'),
    ('DG16', 'Investigación', 'Investigación · user-research', 'medio', 'bajo', 'Todo se vio con datos de prueba y sin ustedes usándola: no sabemos qué usan de verdad, a qué hora registran, qué dejan a medias ni qué le cuesta a Cami.', 'El plan corto de investigación de abajo, antes de priorizar los lotes 3 y 4.'),
]
EXTRAS = [
    {'titulo': 'Qué me aportó la skill (lo nuevo)', 'lineas': [
        'Contraste de controles (WCAG 1.4.11). El primer análisis midió el texto; la skill pide medir también bordes y controles, y ahí salió que campos, casillas y series pendientes van a 1,26:1.',
        'La crítica empieza por qué ve el ojo en 2 segundos. Eso mostró que el Inicio, Progreso, Check-in y el Mercado abren con lo que se planea o se configura, no con lo que hay que hacer hoy.',
        'Los patrones de texto cambiaron el diagnóstico: el problema de las 22 confirmaciones no es la redacción sino el diálogo nativo, que no deja nombrar los botones.',
        'La auditoría del sistema de diseño midió lo que ninguna captura muestra: no hay escala de espaciado, letra ni movimiento, y el estándar escrito no coincide con el CSS.',
        'La prueba al 200 % mostró que liberar el zoom, que proponía el primer informe, rompe el héroe: hay que preparar el diseño antes.',
        'La skill de investigación puso sobre la mesa lo que faltaba: todo se vio con datos de prueba; propone medir el uso real de ustedes dos.',
    ]},
    {'titulo': 'Lo que confirmó del primer informe, ahora medido', 'lineas': [
        'Ventanas sin rol, sin foco y sin Escape (G14): en la del peso el foco se queda detrás, Escape no la cierra y el fondo sigue activo.',
        'Objetivos de toque chicos (EN03): 49 de 57 controles de la sesión, 31 de 50 del Inicio y 31 de 52 de Más quedan por debajo de 44 px.',
        'Acento ilegible en tema claro (G20): «Bonus» y el «126» dorados a 1,53:1 y el selector de Progreso a 1,25:1.',
        'Mensajes técnicos (MA03): 9 errores mencionan SQL, RLS, HTTP, el bucket o la llave.',
        'Foco visible: la skill lo exige y la app lo cumple; los 30 controles recorridos con teclado muestran el contorno.',
    ]},
    {'titulo': 'Lo que la skill no ve (y el primer análisis sí)', 'lineas': [
        'No sabe de PWA ni de iPhone: la nube que pisa datos, el service worker, la pantalla que se apaga, los recordatorios con la app cerrada y la purga de Safari salieron de leer el código.',
        'No recorre tareas: el registro de comida enterrado, el sustituto con los pesos del original o la isla que no se va salen de hacer los flujos, no de revisar pantallas sueltas.',
        'Sus plantillas son genéricas (pensadas para equipos con Figma): sin el estándar Night Gym y la voz de la app, sus textos salían en un tono que no es el de ustedes y hubo que adaptarlos.',
    ]},
    {'titulo': 'Auditoría WCAG 2.1 AA en números', 'lineas': [
        '1.4.3 Contraste de texto: en oscuro solo falla el número de serie de la sesión (3,04:1); en claro, 7 textos (dorados y rótulos del selector).',
        '1.4.11 Contraste de controles: bordes a 1,26:1 en campos, casillas, series pendientes y chips de contorno.',
        '2.1.1 Teclado: sin alcance 35 de 50 controles en la sesión, 10 de 49 en el Inicio y 10 de 40 en el Mercado.',
        '2.4.7 Foco visible: cumple.',
        '2.5.5 Toque de 44 px: por debajo 31 de 50 (Inicio), 49 de 57 (sesión) y 31 de 52 (Más). Bajo 24 px: la pastilla de grasa (18 px de alto) y 6 zonas del mapa del cuerpo.',
        '1.3.1 Estructura: 1 encabezado en el Inicio y ninguno en Más ni en Progreso.',
        '3.3.2 Etiquetas: sin nombre 8 de 16 campos en Más, 3 de 6 en la sesión y 2 de 2 en el Mercado.',
        '4.1.2 Estado: 0 de 9 interruptores y 0 de 15 segmentados fuera de Progreso anuncian su estado.',
        '1.4.4 Zoom al 200 %: se rompen el héroe y el checkpoint.',
    ]},
    {'titulo': 'Plan de investigación con ustedes dos', 'lineas': [
        'Leer el uso real en la nube, solo lectura (necesita el cabritos.env): qué registran, a qué hora, cuántas sesiones quedan a medias y qué pantallas nunca se abren.',
        'Diario de 2 semanas: una nota corta al día en esta mesa (qué te frenó hoy, qué buscaste y no encontraste).',
        'Prueba de 5 tareas con Cami en voz alta, 20 minutos: registrar el almuerzo, marcar una serie y cambiarle el peso, ver cómo va su semana, hacer el check-in y encontrar los Retos.',
        'Con eso se prioriza con datos: impacto contra esfuerzo sobre lo que de verdad pasa, antes de los lotes 3 y 4.',
    ]},
]
VERIF = 'Medido en Chrome a 390 px con las dos cuentas de prueba: tamaño de toque (incluida el área invisible que agranda los chips), contraste de texto y de controles en oscuro y en claro, recorrido con teclado, árbol de accesibilidad (lo que anuncia el lector de pantalla), la ventana del peso y el diseño a 320 y 195 px. Los textos y las confirmaciones se revisaron en el código con la skill ux-copy y el sistema de diseño con la skill design-system. Sin VoiceOver ni iPhone: lo que anuncia el lector sale del árbol de accesibilidad de Chrome, que se parece pero no es igual, y los textos sobre degradados se midieron contra el color dominante del degradado. Los scripts quedaron en herramientas/a11y_medir.js y herramientas/a11y_run.py.'

informe('general', 'Segunda pasada, ahora con el plugin Design de Anthropic: crítica de diseño, auditoría de accesibilidad WCAG 2.1 AA medida en el navegador, revisión de textos, auditoría del sistema de diseño y un plan de investigación. Aquí van solo los hallazgos nuevos. Al final está lo que la skill aportó, lo que confirmó del primer informe y lo que no ve.', GENERAL, EXTRAS, VERIF)

informe('inicio', 'Lo que atrapa la vista en 2 segundos es la cifra del peso, y está bien que sea así. Lo que falta es que la primera pantalla diga qué te queda pendiente hoy.', [
    ('DI01', 'I1, I2', 'Diseño · primera impresión', 'medio', 'medio', 'En 2 segundos el ojo va a la cifra del peso (89,6) y enseguida a la cabrita grande del checkpoint. Pero lo que te falta hoy no se lee arriba: el «0 de 3» y la proteína que falta quedan una y tres pantallas más abajo. Después del peso, el ojo salta entre cuatro tarjetas con el mismo peso visual (Entreno, Pasos, Creatina y Hyrox, Agua y Medidas) sin orden entre ellas.', 'Que la primera pantalla responda «qué me falta hoy»: el peso y debajo una sola fila con lo pendiente (proteína, agua, entreno) por urgencia. Las tarjetas iguales pasan a un segundo nivel.'),
    ('DI02', 'I1', 'Accesibilidad · WCAG 2.5.8', 'medio', 'bajo', 'La pastilla de grasa junto al peso mide 18 px de alto (WCAG 2.2 pide al menos 24) y está pegada al peso, que también se toca.', 'Área de toque de al menos 24 px, ideal 44, con el ::after que ya usa la app.'),
    ('DI03', 'I2', 'Accesibilidad · WCAG 4.1.2', 'medio', 'bajo', 'El lector anuncia la tarjeta de Medidas como «Medidas 5 EN 5 D» (y no se alcanza con teclado), la creatina como «Creatina, 5 gramos» sin decir si ya la tomaste, y el botón de la inyección solo como «Hecha».', 'Nombres completos con su estado: «Medidas: te toca en 5 días», «Creatina 5 g, tomada hoy», «Marcar la inyección semanal como hecha».'),
    ('DI04', 'I2', 'Diseño · consistencia', 'bajo', 'bajo', 'En la misma rejilla conviven tres anatomías de tarjeta: ilustración grande (Entreno, Medidas), anillo con barras (Pasos) y cifra en cápsula (Creatina, Hyrox), y las columnas no terminan a la misma altura.', 'Una anatomía común (rótulo, cifra y apoyo visual) y alturas parejas por fila.'),
])

informe('entrenar', 'Pensada para una mano y sin señal; lo que la skill agrega es que en el gimnasio, con poco brillo, los controles pendientes casi no se ven.', [
    ('DE01', 'E2a', 'Accesibilidad · WCAG 1.4.11', 'alto', 'bajo', 'En la sesión, los campos de kg y reps, el check pendiente y los círculos de serie sin marcar tienen un borde de 1,26:1: con el brillo bajo del gimnasio no se distingue qué es campo y qué es fondo.', 'Borde de control a 3:1 (DG01) y la serie pendiente con un relleno tenue además del punteado.'),
    ('DE02', 'E2', 'Accesibilidad · WCAG 2.1.1', 'medio', 'medio', '35 de los 50 controles de la sesión no se alcanzan con teclado ni con el control por botón de iOS: la cabecera del ejercicio, los círculos de serie, la gráfica y las opciones son elementos sin foco.', 'Botones reales, o foco y Enter en esos elementos.'),
    ('DE03', 'E2a', 'Accesibilidad · WCAG 3.3.2 y 1.4.3', 'medio', 'bajo', 'Los campos de reps no tienen nombre para el lector (los de kg sí dicen «peso en kilos») y el número de serie (1, 2, 3) va a 3,04:1 de contraste con 13 px.', 'Nombre «repeticiones de la serie 1» y el número de serie a 4,5:1.'),
    ('DE04', 'E2a', 'Diseño · jerarquía', 'medio', 'bajo', 'Al abrir un ejercicio, la columna «Anterior» (102,0 × 8) y los campos de hoy (102 y 8) pesan lo mismo a la vista: no queda claro cuál es el dato a superar y cuál el que escribes. El descanso (3:00) entre filas compite con los dos.', 'Anterior en gris y más pequeño, el campo de hoy con borde de control y el objetivo de progresión resaltado; el descanso como un separador fino.'),
    ('DE05', 'E2', 'Texto · ux-copy', 'medio', 'bajo', 'Las confirmaciones de la sesión son nativas y ambiguas: «Voy a registrar toda la rutina… ¿Sigo?», «Tienes una sesión a medias. ¿La descarto…?» y «¿Borrar la sesión X?» sin decir qué se pierde.', '«¿Registrar toda la rutina de hoy? Se guarda con los kg y reps sugeridos» con «Registrar rutina» y «Revisar antes»; «¿Descartar la sesión a medias? Perderías las series sin guardar» con «Descartar» y «Terminar la actual».'),
])

informe('comida', 'La crítica pregunta qué ve uno al llegar: aquí se ve lo que se planea antes que lo que toca hacer hoy.', [
    ('DC01', 'C2, C3', 'Diseño · primera impresión', 'medio', 'bajo', 'Recetas abre con una tarjeta verde grande («Meal prep compartido · 84 Recetas») y Mercado con el total de $110.015: las dos empiezan por lo planeado, no por comprar o cocinar. En Mercado, antes de la lista hay dos segmentados y un texto de 3 líneas que explica uno de ellos.', 'Mercado abre con la lista por comprar y el total pegado arriba; Los dos/Andrés/Cami y Semanal/Quincenal/Mensual en una fila de menús compactos.'),
    ('DC02', 'C3', 'Accesibilidad · WCAG 2.1.1 y 3.3.2', 'medio', 'bajo', 'Las filas del mercado (marcar comprado) no se alcanzan con teclado ni anuncian si ya se compró, y los campos «Ítem libre» y «$ opc.» no tienen nombre para el lector.', 'Filas como botones con su estado (comprado o pendiente) y nombre en los dos campos.'),
    ('DC03', 'C3', 'Accesibilidad · WCAG 4.1.2', 'bajo', 'bajo', 'El interruptor «Incluir básicos fijos» es un div: no se alcanza con teclado ni dice si está encendido; los segmentados no dicen cuál está activo.', 'Interruptor como botón con su estado y estado marcado en los segmentados.'),
    ('DC04', 'C3', 'Texto · ux-copy', 'bajo', 'bajo', '«Ambos = mercado grupal. Andrés / Cami muestran la distribución individual de cada uno con sus básicos» explica un control que debería entenderse solo.', 'Rótulos que no necesitan nota: «Los dos», «Solo Andrés», «Solo Cami».'),
])

informe('progreso', 'El dato aparece tarde: hay tres niveles de navegación antes de la primera cifra.', [
    ('DP01', 'P1, P3', 'Diseño · jerarquía', 'medio', 'medio', 'Antes del primer dato hay tres niveles de navegación apilados: tarjetas grandes con ilustración (Actividad, Nutrición, Medidas), una fila de 6 íconos y los rangos SEM a AÑO. La cifra aparece a unos 600 px. «Medidas» va punteado y dorado porque lleva a otra vista, pero se ve como si estuviera deshabilitado.', 'Un selector compacto para el grupo y la categoría, y Medidas como enlace con flecha, no como tarjeta.'),
    ('DP02', 'P2', 'Accesibilidad · WCAG 1.3.1 y 1.4.3', 'medio', 'bajo', 'Progreso no tiene ningún encabezado real (8 títulos que solo se ven), y en tema claro los rótulos del selector bajan a 1,25:1 («Medidas») y 3,88:1 («Nutrición»).', 'Encabezados h2 y tonos de texto propios del tema claro.'),
    ('DP03', 'P2', 'Diseño · consistencia', 'bajo', 'bajo', 'La tarjeta se llama «Rendimiento» en todas las pestañas, también en Peso, donde la cifra es el peso: el título no cambia con el contenido.', 'Que el título sea la categoría: «Peso», «Volumen», «Pasos».'),
])

informe('medidas', 'El mapa del cuerpo es lo más llamativo de la app y se lee bien: cifra, unidad y variación con flecha.', [
    ('DM01', 'MD2', 'Diseño · consistencia', 'bajo', 'bajo', 'La variación usa rojo para «bajó» en cuello y pecho (−0,1 y −0,6) y verde para «bajó» en cintura (−0,9): el mismo signo con colores opuestos. Puede ser a propósito (en definición bajar pecho puede ser músculo), pero la pantalla no lo dice.', 'Si es a propósito, que la ventana de detalle explique qué dirección se busca en cada medida durante la etapa; si no, un color neutro con la flecha.'),
])

informe('checkin', 'Al llegar se ve la etapa antes que el check-in de la semana.', [
    ('DK01', 'K0, K1', 'Diseño · primera impresión', 'medio', 'bajo', 'Lo primero no es el check-in del domingo sino la tarjeta de la etapa (la misma de Plan) con la pastilla roja y un párrafo de 5 líneas; el formulario queda dos pantallas abajo.', 'Abrir con «Semana del 12/10» y su formulario; la etapa en una línea con enlace a Plan.'),
])

informe('mas', 'Lo nuevo aquí es de accesibilidad: campos y recordatorios que el lector de pantalla no puede describir.', [
    ('DA01', 'M1, M7, M8', 'Accesibilidad · WCAG 3.3.2 y 4.1.2', 'medio', 'bajo', '8 de los 16 campos de Más no tienen nombre para el lector (el PIN dice solo «4 dígitos», la edad no tiene rótulo) y ninguno de los 8 interruptores de recordatorios dice si está encendido.', 'Rótulo en cada campo y el estado en los interruptores.'),
])

# ---------------------------------------------------------------- proyecto: hito, pendiente y aprendizaje
docs.append(('hitos', 'hito-27', {'tipo': 'hito', 'fecha': '2026-10-14', 'rev': None, 'titulo': 'Segunda pasada con el plugin Design', 'detalle': 'Crítica, accesibilidad medida, textos, sistema de diseño e investigación: 35 hallazgos nuevos.', 'orden': 126}))
docs.append(('pendientes', 'pend-12', {'titulo': 'Revisar la segunda pasada (skill Design)', 'detalle': 'Cada sección tiene ahora dos informes: el de la segunda pasada arriba y el primero abajo. En General están lo que aportó la skill, lo que confirmó, lo que no ve y el plan de investigación.', 'quien': 'andy', 'prioridad': 'alta', 'estado': 'abierto', 'origen': 'Segunda pasada del 14/10', 'orden': 2, 'creadoEn': '2026-10-14T09:30:00.000Z'}))
docs.append(('aprendizajes', 'apr-41', {'tema': 'Probar y verificar', 'titulo': 'El plugin Design de Anthropic sirve para revisar', 'texto': 'Instalado en Claude Code con claude plugin marketplace add anthropics/knowledge-work-plugins y claude plugin install design@knowledge-work-plugins (agregarlo en claude.ai no lo trae a Claude Code). Trae design-critique, accessibility-review, ux-copy, design-system, user-research, research-synthesis y design-handoff. Aporta método más que datos: contraste de controles, patrones de texto, escalas del sistema y plan de investigación. No sabe de PWA ni recorre flujos. Las mediciones de accesibilidad quedaron en herramientas/a11y_medir.js y a11y_run.py.', 'fuente': 'Segunda pasada del 14/10', 'orden': 40}))

for col, id_, data in docs:
    d = os.path.join(BASE, col); os.makedirs(d, exist_ok=True)
    json.dump(data, open(os.path.join(d, id_ + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
writes = [{'op': 'set', 'collection': col, 'doc_id': id_, 'file_path': os.path.join(col, id_ + '.json')} for col, id_, _ in docs]
json.dump(writes, open(os.path.join(BASE, 'lotes_b.json'), 'w'), ensure_ascii=False)
n = sum(len(d['items']) for c, _, d in docs if c == 'informes')
imp = {}
for c, _, d in docs:
    if c == 'informes':
        for it in d['items']: imp[it['impacto']] = imp.get(it['impacto'], 0) + 1
print('docs', len(docs), 'hallazgos', n, imp)
print('con raya larga:', [(c, i) for c, i, d in docs if '—' in json.dumps(d, ensure_ascii=False)])
