#!/usr/bin/env python3
"""Genera la semilla de la Mesa de revision de CabriCoach (2026-10-14).

Escribe un JSON por documento en semilla/<coleccion>/<id>.json y un
lotes.json con las escrituras agrupadas de a 50 para ArtifactData batch.
El contenido sale del analisis UX del 14/10, de los docs del proyecto y del
historial de git. Se corre una vez; despues la mesa manda.
"""
import json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
LOTE = '2026-10-14'
AHORA = '2026-10-14T08:00:00.000Z'
docs = []  # (coleccion, id, data)


def add(col, id_, data):
    docs.append((col, id_, data))


# ---------------------------------------------------------------- secciones
SECCIONES = [
    ('general', 'General', 'Lo que cruza toda la app: barra inferior, navegación, nube, avisos, arranque, accesibilidad y tema claro.',
     [('G2', 'Barra inferior'), ('G5', 'Ventanas flotantes'), ('G6', 'Isla de rutina y descanso'), ('G4', 'Avisos (toasts)'), ('nube', 'Nube y sincronización'), ('recordatorios', 'Recordatorios'), ('arranque', 'Arranque y versión nueva'), ('tema', 'Tema claro'), ('texto', 'Tamaño del texto y accesibilidad')]),
    ('inicio', 'Inicio', 'El resumen del día: peso, checkpoint, metas y nutrición.',
     [('I1', 'I1 · Héroe del peso'), ('I1b', 'I1b · Tira de días'), ('I2', 'I2 · Checkpoint del día'), ('I2b', 'I2b · Pasos'), ('I2c', 'I2c · Agua'), ('I2d', 'I2d · Medidas'), ('I2e', 'I2e · Hyrox'), ('IM', 'IM · Tus metas'), ('I3', 'I3 · Caja Para ti'), ('I4', 'I4 · Nutrición del día'), ('I4b', 'I4b · Con qué cerrar'), ('franjas', 'Franjas y registro de comida'), ('I5', 'I5 · Ciclo de Cami'), ('I2f', 'I2f · Botón de foto del día')]),
    ('entrenar', 'Entrenar', 'Rutinas, sesión en vivo, catálogo de ejercicios y reloj.',
     [('E1', 'E1 · Rutinas'), ('E2', 'E2 · Sesión activa'), ('E2a', 'E2a · Series'), ('E3', 'E3 · Importar entreno'), ('E4', 'E4 · Historial'), ('E5', 'E5 · Ejercicios'), ('E6', 'E6 · Movilidad'), ('reloj', 'Reloj'), ('E1b', 'E1b · Personalizado'), ('E1x', 'E1x · Crear rutina')]),
    ('agenda', 'Agenda', 'Mi semana (planificador) y el calendario del mes.',
     [('A1', 'A1 · Selector Semana/Mes'), ('A2', 'A2 · Mi semana'), ('A3', 'A3 · Mes'), ('A4', 'A4 · Detalle de un día'), ('A5', 'A5 · Modo foto')]),
    ('comida', 'Comida', 'Recetas, Mercado y Gestión (la semana de comida de los dos).',
     [('C1', 'C1 · Sub-pestañas'), ('C2', 'C2 · Recetas'), ('C3', 'C3 · Mercado'), ('C5', 'C5 · Gestión'), ('libre', 'Registro libre'), ('pcal', 'Calculadora de proteína')]),
    ('progreso', 'Progreso', 'Actividad física y nutrición en gráficas.',
     [('P1', 'P1 · Selector de grupo'), ('P2', 'P2 · Rendimiento'), ('P3', 'P3 · Categorías'), ('P4', 'P4 · Peso'), ('P5', 'P5 · Volumen'), ('P6', 'P6 · Tiempo'), ('P7', 'P7 · Ejercicios y fuerza'), ('P8', 'P8 · Pasos'), ('P9', 'P9 · Nutrición'), ('P10', 'P10 · Metas de fuerza')]),
    ('plan', 'Plan', 'Etapas, checkpoints, rescans, creatina y diario de decisiones.',
     [('PL1', 'PL1 · Semáforo de la semana'), ('PL2', 'PL2 · Lo que comes'), ('PL3', 'PL3 · Checkpoints'), ('PL4', 'PL4 · El plan completo'), ('PL5', 'PL5 · Rescans'), ('PL6', 'PL6 · Creatina'), ('PL7', 'PL7 · Diario de decisiones')]),
    ('medidas', 'Medidas', 'Cuerpo, composición, historial y carga por músculo.',
     [('MD0b', 'MD0b · Formulario'), ('MD1', 'MD1 · Lo que toca hoy'), ('MD2', 'MD2 · Mapa corporal'), ('MD3', 'MD3 · Panel de la zona'), ('MD4', 'MD4 · Navy'), ('MD12', 'MD12 · Bioimpedancia'), ('comp', 'Composición'), ('hist', 'Historial'), ('MC', 'MC · Carga por músculo')]),
    ('fotos', 'Fotos', 'Foto del día, antes y después, galería.',
     [('FT1', 'FT1 · Tomar hoy'), ('FT2', 'FT2 · Antes y después'), ('FT3', 'FT3 · Galería'), ('FT4', 'FT4 · Ventana de una foto')]),
    ('checkin', 'Check-in', 'El cierre del domingo: semáforo, resumen, formulario y evolución.',
     [('K0', 'K0 · Semáforo'), ('K1', 'K1 · Resumen de la semana'), ('K2', 'K2 · Formulario'), ('K3', 'K3 · Gráficas'), ('K4', 'K4 · Tabla de evolución')]),
    ('retos', 'Retos', 'El versus de los cabritos: puntos, premios y vitrina.',
     [('R1', 'R1 · Héroe del versus'), ('R2', 'R2 · Puntos'), ('R3', 'R3 · Premios'), ('R4', 'R4 · Vitrina')]),
    ('perfil', 'Perfil', 'Nivel, logros, trofeos y accesos.',
     [('PF1', 'PF1 · Nivel y XP'), ('PF2', 'PF2 · Logros'), ('PF3', 'PF3 · Composición'), ('PF6', 'PF6 · Trofeos'), ('PF7', 'PF7 · Accesos')]),
    ('mas', 'Más (ajustes)', 'Recordatorios, Salud, PIN, nube, datos y preferencias.',
     [('M1', 'M1 · Recordatorios'), ('M2', 'M2 · Salud y pasos'), ('M3', 'M3 · Inyección'), ('M7', 'M7 · PIN'), ('M8', 'M8 · Preferencias'), ('M9', 'M9 · Nube'), ('M10', 'M10 · Datos'), ('M11', 'M11 · Hyrox')]),
    ('hyrox', 'Hyrox', 'Nivel, marcas, sesiones, progresiones y plan de 12 semanas.',
     [('HX0', 'HX0 · Portada'), ('HX1', 'HX1 · Nivel'), ('HX2', 'HX2 · Marcas'), ('HX3', 'HX3 · Sesiones'), ('HX4', 'HX4 · Progresiones'), ('HX5', 'HX5 · Plan 12 semanas')]),
]
for i, (sid, nombre, desc, partes) in enumerate(SECCIONES):
    add('secciones', sid, {'orden': i, 'nombre': nombre, 'descripcion': desc, 'partes': [{'id': p, 'nombre': n} for p, n in partes]})

# ---------------------------------------------------------------- capturas
CAPTURAS = [  # (seccion, titulo, assetId) en el orden en que se suben: la ultima de cada seccion es la que abre
    ('inicio', 'Inicio de Cami', '329ddd892ad9d5fa94b699d730472d60'),
    ('inicio', 'Inicio con el registro de comida abierto', '4741b01be0fb2e1211a2e894bd65b215'),
    ('inicio', 'Inicio de Andrés', 'd7f5e605c4dfffb3326f2effe37179ee'),
    ('entrenar', 'Sesión con un ejercicio abierto', '00e2111bef38326bb1b5565d8b18fc1f'),
    ('entrenar', 'Rutinas', '859ec35aaa6589a2530b6ee2f1f70a61'),
    ('agenda', 'Mes', '17f58c50cf38b77d0151594c1a24159c'),
    ('comida', 'Gestión', 'f5794757a3f74a34ef38d28a1293d4b8'),
    ('comida', 'Mercado', 'ea59bfacf4289d8861331cf277ed12fd'),
    ('comida', 'Recetas', '51ad2651966bdf0635bcbe92df366e06'),
    ('progreso', 'Nutrición', '9f9a18ce0dc7479fb1aaca724bb0133e'),
    ('progreso', 'Peso', '07067e5e9cf701a3a0ac6130a5985619'),
    ('progreso', 'General', '60341600109c7abd21444f9e653a552b'),
    ('plan', 'Plan', 'eeb58e542f64fc7f41d74140e1aca889'),
    ('medidas', 'Composición', '007a68c0374b938414393e4e36fc851d'),
    ('medidas', 'Cuerpo', '699b7c4947487caa3bb86003d724fcf0'),
    ('medidas', 'Portada', 'abe5c4b6411ade94d532eaa25925938e'),
    ('fotos', 'Fotos', 'bb9fce5f86d4d91ca445c93d4cece4fb'),
    ('checkin', 'Check-in', '942ff4a4f97374e47102e95119ceab9c'),
    ('retos', 'Retos de Cami', '41d096a537a4fdc2f533517348aa17d4'),
    ('retos', 'Retos de Andrés', '78bd2b8d3c2de5cd08968742c219463f'),
    ('perfil', 'Perfil', 'fabffa1028198bd6763163df078e5285'),
    ('mas', 'Más', 'f91e6d0386d4f85326e3be52ca6fdf94'),
    ('hyrox', 'Tu nivel', 'aebd69a98ba930b28f748117d6772c7d'),
    ('hyrox', 'Portada', '4323547bb9f53829046c8fb3c6b692aa'),
]
for i, (sec, tit, aid) in enumerate(CAPTURAS):
    ts = (datetime.datetime(2026, 10, 14, 8, 0) + datetime.timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M:00.000Z')
    add('capturas', f'cap-{i+1:02d}', {'seccion': sec, 'titulo': tit + ' · REV 222, datos de prueba', 'assetId': aid, 'autor': None, 'creadoEn': ts, 'origen': 'agente', 'movil': True})

# ---------------------------------------------------------------- informes
COMO = 'Marca Va en lo que quieres que haga. Usa Responder si lo quieres distinto o tienes una pregunta: va en el próximo envío. Lo que no marques se queda aquí.'

def informe(sec, lead, items, extras=None, verificacion=None):
    add('informes', f'{LOTE}-{sec}', {
        'seccion': sec, 'lote': LOTE, 'titulo': 'Análisis UX y UI · 14 de octubre',
        'lead': lead, 'columnas': ['Hallazgo', 'Propuesta'], 'okTexto': 'Va', 'comoUsar': COMO,
        'items': [{'codigo': c, 'zona': z, 'tipo': t, 'impacto': im, 'esfuerzo': es, 'pedido': h, 'hecho': p} for (c, z, t, im, es, h, p) in items],
        'decisiones': [], 'pendiente': [], 'verificacion': verificacion, 'extras': extras or [], 'revisar': [], 'revisado': {}, 'archivado': {},
    })

informe('general',
    'Visto en 30 pantallas por usuario con 70 días de datos sembrados y cuatro auditorías de código (flujos, robustez, texto y parte técnica). La base visual es fuerte y el cuidado del detalle se nota en todas partes. Lo que más pesa hoy: dónde vive cada cosa (navegación y puntos de registro), la confianza en los datos (nube, respaldo, recordatorios) y la cantidad de texto y cifras por pantalla.',
    [
        ('G01', 'G2', 'Navegación', 'alto', 'medio', 'La barra inferior es solo íconos: el de Comida parece un enchufe, y Progreso, Retos, Check-in, Plan y Más no tienen entrada directa. A Más se llega por una línea gris diminuta al pie del checkpoint o al fondo del Perfil; a Retos solo manteniendo oprimido el avatar, sin ninguna pista.', 'Rótulo corto bajo cada ícono (Inicio, Entrenar, Yo, Agenda, Comida). Tocar el avatar abre una hoja con Perfil, Progreso, Retos, Check-in, Plan y Ajustes; el gesto largo se queda como atajo para cambiar de usuario.'),
        ('G02', 'G6', 'Bug', 'alto', 'bajo', 'Con solo abrir una rutina se crea la sesión en curso y aparece la isla «Legs A · 0/5 ejercicios · toca para volver». Se queda fija encima de la barra en todas las vistas y tapa el final del contenido (Gestión, Perfil, Plan, Progreso) aunque no hayas marcado nada.', 'Crear la sesión al marcar la primera serie, o borrarla al salir si no tiene series hechas. Mientras la isla esté visible, dejar el espacio abajo para que no tape nada.'),
        ('G03', 'Navegación', 'Bug', 'medio', 'bajo', 'El gesto de deslizar desde el borde izquierdo siempre lleva a Inicio: ignora el «volver» que sí usa el botón. Desde Fotos abierta en Perfil, el botón vuelve a Perfil y el gesto a Inicio; dentro de Medidas o Hyrox el gesto salta a Inicio en vez de a la portada de la sección.', 'Que el gesto haga lo mismo que el botón: volver a donde venías y, dentro de una subsección, a su portada.'),
        ('G04', 'Navegación', 'Interfaz', 'medio', 'medio', 'Volver es inconsistente: Medidas, Hyrox, Fotos, Check-in y Plan tienen cabecera con flecha; Perfil, Progreso, Retos y Más no tienen ninguna.', 'La misma cabecera con flecha y título en todas las vistas que no están en la barra.'),
        ('G05', 'Botones flotantes', 'Interfaz', 'medio', 'bajo', 'Los botones flotantes (cámara en Inicio, importar y calculadora en Entrenar, rayo y plato en Comida) quedan fijos sobre el contenido y no dicen qué hacen. La cámara tapa el + de «Lo tuyo» al registrar comida y los de arriba tapan títulos como «Push B».', 'Que se escondan al bajar y vuelvan al subir, con un rótulo corto; o pasar los de Entrenar y Comida a la cabecera de su vista.'),
        ('G06', 'Nube', 'Datos', 'alto', 'medio', 'Al abrir la app (y al volver tras 30 s) la nube escribe cada dato encima de lo del teléfono sin comparar fechas, y un envío que falló sin señal no se reintenta. Cami registra comida y agua sin señal en el gimnasio, abre la app ya con señal y la versión vieja de la nube borra lo del día.', 'Marcar como pendiente lo que no subió, reintentar al volver la señal y al abrir, y no bajar un dato pendiente antes de subirlo. Para peso, agua, pasos, comida y series, fusionar por fecha en vez de reemplazar todo.'),
        ('G07', 'Nube', 'Interfaz', 'alto', 'bajo', 'Fuera de Más no hay ninguna señal de si lo que registraste ya está en la nube.', 'Un punto discreto en la cabecera (al día, pendiente o con error) que al tocarlo diga «3 cambios sin subir».'),
        ('G08', 'M10', 'Bug', 'alto', 'bajo', 'Importar un respaldo reemplaza todo sin preguntar ni revisar de quién es: Cami puede cargar el de Andrés por error y quedan reemplazados sus pesos, entrenos, PIN y lo compartido, y se sube a la nube.', 'Hoja de confirmación con resumen («Respaldo de Andrés del 10/10: 320 pesajes, 86 entrenos»), bloqueo si no es del usuario activo, Deshacer, y nunca importar el PIN ni lo compartido.'),
        ('G09', 'M1', 'Flujo', 'alto', 'medio', 'Los recordatorios solo suenan con la app abierta (un temporizador dentro de la página, sin push), y el interruptor dice «Activas». Con la app cerrada, la inyección y el check-in no avisan. En iOS puede fallar incluso con la app abierta (por probar en el iPhone).', 'Decirlo claro en Ajustes y usar el calendario (.ics) como camino principal para inyección y check-in. Push real solo si vale la pena: pide una función en Supabase.'),
        ('G10', 'Fotos', 'Datos', 'alto', 'medio', 'Las fotos de progreso viven en un bucket público con la ruta casa/usuario/fecha. «Privada» solo cambia lo que ve la pareja dentro de la app: el archivo sigue abierto para quien adivine la ruta.', 'Bucket privado con enlaces temporales. Mientras tanto, nombre de archivo aleatorio y un texto honesto sobre qué protege «privada».'),
        ('G11', 'Datos', 'Técnico', 'medio', 'bajo', 'Si el almacenamiento del teléfono se llena, guardar falla en silencio y la app sigue diciendo «Guardado». Tampoco pide almacenamiento persistente.', 'Un aviso visible cuando falle guardar y pedir almacenamiento persistente al abrir.'),
        ('G12', 'Arranque', 'Técnico', 'medio', 'bajo', 'Con señal mala en el gimnasio la app se queda en negro hasta que la red se rinde: el service worker espera la red sin límite. Tampoco avisa cuando hay versión nueva.', 'Esperar la red máximo 1,5 s y si no abrir desde el teléfono; aviso «Hay una versión nueva · Actualizar»; y una pantalla de carga con el logo en vez del negro.'),
        ('G13', 'Texto', 'Accesibilidad', 'medio', 'medio', 'El zoom está bloqueado, los tamaños van en px y hay unas 159 reglas de texto bajo 12 px: el texto no crece con el ajuste de tamaño del iPhone.', 'Quitar el bloqueo de zoom, piso de 11 px para etiquetas y 12 para lectura, y un ajuste «Tamaño del texto» (100, 115, 130 %) en Ajustes.'),
        ('G14', 'G5', 'Accesibilidad', 'medio', 'medio', 'Las 32 ventanas flotantes no cierran con Escape, no retienen el foco y casi ninguna se anuncia como ventana; al cerrar, el foco no vuelve a donde estaba.', 'Un solo ayudante para abrir ventanas que haga todo eso; cambio mecánico en los 32 sitios.'),
        ('G15', 'Varias', 'Flujo', 'medio', 'medio', 'El mismo dato se registra en muchos lugares: el peso en 5, los pasos en 4, la foto del día en 5, hay cuatro maneras de dar un entreno por hecho y tres almacenes de comida (franjas, comidas del plan y registro libre).', 'Un solo punto de entrada por dato; los demás lugares abren ese mismo control. Para la comida, una sola lista del día con las comidas del plan como pendientes.'),
        ('G16', 'Varias', 'Datos', 'medio', 'medio', 'Hay varias metas de peso a la vista: 83,8 (Inicio y Medidas), 87,2 (Progreso y Más), 87,7 «esperado» (Plan) y 88,2 «con creatina», con tres fechas de llegada. Y el peso cambia sin rótulo: 89,6 hoy, 90,1 promedio, 89,9 en el historial.', 'Dos nombres fijos y siempre iguales: «Meta de la etapa» y «Esperado esta semana». El peso del día y el promedio de 7 días con su rótulo en cada lugar.'),
        ('G17', 'Texto', 'Texto', 'medio', 'bajo', 'Vocabulario mezclado: Comida, Nutrición y Alimentación; Sesión, Entreno y Rutina; ejercicios en inglés junto a otros en español (Hack Squat y Pantorrilla de pie), y la misma rutina como Legs A en Entrenar y Pierna A en Plan. Miles sin punto (2501, 1416), fechas largas en mayúscula y «loggeo».', 'Un glosario corto con un término por concepto y una pasada mecánica por toda la app.'),
        ('G18', 'Texto', 'Texto', 'medio', 'medio', 'Términos técnicos sin explicación a mano: RIR, 1RM y E1RM, Navy, bioimpedancia, TMB, déficit, tonelaje, series efectivas, descarga, PR.', 'Un glosario en las ventanas de detalle y una «i» junto al término la primera vez que aparece en cada pantalla.'),
        ('G19', 'Proyecciones', 'Interfaz', 'bajo', 'bajo', 'Las fechas proyectadas no llevan año: Cami ve «≈ 25 de agosto», que se lee como una fecha ya pasada (es de 2027).', 'Mostrar el año cuando la fecha está a más de 6 meses.'),
        ('G20', 'Tema claro', 'Accesibilidad', 'medio', 'medio', 'En tema claro el acento como texto no se lee: el azul da 3,05:1 y el dorado de Cami 1,49:1. La barra de estado del iPhone queda blanca sobre papel claro y el primer pintado siempre es oscuro.', 'Tonos de texto propios para el claro (azul, ámbar y rojo más profundos), barra de estado según el tema y el tema aplicado antes del primer pintado. Es parte de cerrar la Fase 5.'),
    ],
    extras=[
        {'titulo': 'Lo que necesito que decidas', 'lineas': [
            '¿La barra inferior lleva rótulos? Cambia la estética minimal, pero hoy media app no se descubre.',
            '¿El registro de comida se muda a la pestaña Comida (y el Inicio solo resume) o se queda en el Inicio con un botón fijo?',
            'Recordatorios: ¿push real (pide una función en Supabase) o calendario .ics con un texto honesto?',
            'Fotos: ¿pasamos el bucket a privado? Hay que migrar las fotos que ya están arriba.',
            'Nombres de ejercicios: ¿español, inglés, o español con el inglés entre paréntesis?',
        ]},
        {'titulo': 'Por dónde empezaría', 'lineas': [
            'Lote 1, arreglos rápidos y verificados: la isla que no se va, el nodo de comidas que no se toca, el gesto de volver, el sustituto con los pesos del original, borrar serie sin Deshacer y las tarjetas cortadas del Inicio.',
            'Lote 2, que nada se pierda: la nube que no pisa lo local, el indicador de sincronización, importar con confirmación y el aviso de almacenamiento.',
            'Lote 3, dónde vive cada cosa: barra con rótulos, menú del avatar, registro de comida a un toque y un punto de entrada por dato.',
            'Lote 4, leer menos: glosario, metas con nombre fijo, Plan y Composición plegados y vocabulario único.',
            'Lote 5, accesibilidad y tema claro, que cierra la Fase 5 del plan de revisión.',
        ]},
    ],
    verificacion='Verifiqué en el código lo grave: la nube reescribe sin comparar fechas (sbPull), un envío fallido no se reintenta (sbSend), importar no confirma, el nodo de comidas usa la clave COMIDAS cuando el mapa de destinos dice COMIDA, el gesto de volver ignora backTo, cambiar de ejercicio rellena con el historial del original, y no hay Wake Lock, almacenamiento persistente ni aviso de versión nueva. Sin verificar porque piden el iPhone: si los recordatorios fallan con la app abierta en iOS, si ?steps= desde Atajos llega a la app instalada y el contraste real en pantalla.')

informe('inicio',
    'El héroe del peso y el checkpoint tienen muy buena presencia y las cabritas le dan personalidad. Lo que más cuesta es el largo (4 pantallas) y que la acción diaria más importante, registrar comida, esté al fondo.',
    [
        ('IN01', 'I4', 'Flujo', 'alto', 'medio', 'Registrar comida, lo más importante del día para Andrés (llegar a la proteína), vive al final del Inicio, a unas 3 pantallas de scroll, y la pestaña Comida no registra.', 'Un botón «+ Comida» siempre a mano que abra el registro con la franja según la hora y el buscador listo para escribir. Y subir la nutrición justo después del héroe.'),
        ('IN02', 'I2', 'Bug', 'alto', 'bajo', 'En el checkpoint los rótulos se cortan («PAS…», «CO…», «BON…») y el nodo de comidas no se puede tocar: el mapa de destinos tiene COMIDA y el nodo se pinta como COMIDAS.', 'Corregir la clave y dejar el ícono con su cifra (el rótulo completo para el lector de pantalla), o rótulos de una palabra que quepan.'),
        ('IN03', 'I2', 'Bug', 'alto', 'bajo', 'Tarjetas que se desbordan a 390 px: la pastilla «Bonus» del Entreno se sale por la derecha, la cifra «1.000» del Agua invade la tarjeta de Medidas, «+250 ML» parte en dos líneas y en Medidas queda un «5» suelto con «EN 5 D» tapado por la cabrita.', 'Cifras que se ajustan al ancho, la pastilla Bonus debajo del título y Medidas con cifra y rótulo («en 5 días») como las demás tarjetas.'),
        ('IN04', 'I1, I2', 'Texto', 'medio', 'bajo', 'Datos repetidos en la misma pantalla: la racha («0 días de racha» en el héroe y «Racha 0» en el checkpoint) y lo que falta de proteína («te faltan 126 g» en Con qué cerrar y la tarjeta «126 te falta»).', 'Cada dato una sola vez: la racha en el checkpoint y lo que falta en Con qué cerrar.'),
        ('IN05', 'I4', 'Interfaz', 'medio', 'bajo', 'La fila de macros mezcla lo comido (29 de carbo, 15 de grasa) con lo que falta (126 de proteína), y la «g» chiquita tras la cifra parece una flecha.', 'Las tres tarjetas en el mismo sentido (comido sobre meta, con barra); lo que falta solo en Con qué cerrar.'),
        ('IN06', 'I4', 'Datos', 'medio', 'bajo', 'Dos metas de proteína lado a lado: «24 / 150 g» y «0,3 g/kg · meta 1,8» (1,8 × 89,6 son 161 g, no 150), y el g/kg sale en rojo a las 2 de la mañana.', 'Una sola meta visible (150 g, piso 140), el g/kg en la ventana de detalle y el color según la hora, como pide el estándar.'),
        ('IN07', 'I4', 'Interfaz', 'medio', 'bajo', '«Cómo» y «Meta» son dos píldoras grandes que compiten con las cifras del anillo.', 'Una «i» pequeña junto al dato que explican.'),
        ('IN08', 'Inicio', 'Flujo', 'medio', 'medio', 'El Inicio pide mucho: unas 35 cifras, 6 bloques de texto y 4 pantallas de alto. En 3 segundos no queda claro qué es lo principal: el peso compite con el anillo de proteína y con Con qué cerrar.', 'Dos niveles: arriba «Hoy» (peso, proteína, agua y entreno) y abajo, plegado, lo de la semana (metas, progreso, próximos).'),
        ('IN09', 'Inicio', 'Flujo', 'medio', 'bajo', 'Antes del peso aparecen tarjetas de tareas: el respaldo semanal desde el primer día y la guía de bienvenida.', 'Un solo espacio de aviso con prioridad; el respaldo solo si no hay nube y ya pasaron 7 días.'),
        ('IN10', 'IM', 'Interfaz', 'bajo', 'bajo', '«Tus metas» plegada muestra 4 anillos sin cifra (Etapa 1, Pasos, Peso, Cintura): se ven bien pero no dicen cuánto falta.', 'La cifra o el porcentaje dentro de cada anillo.'),
        ('IN11', 'I2c', 'Flujo', 'medio', 'bajo', 'Para cambiar el tamaño del vaso hay que mantener el + durante 1,5 s, sin ninguna pista de que existe.', 'Bajarlo a 0,6 s y un punto en el botón que insinúe el menú.'),
        ('IN12', 'I1', 'Flujo', 'medio', 'bajo', 'La ventana del peso abre con el último peso pero sin el campo listo: hay que tocarlo, borrar y escribir (la de pasos sí lo deja listo).', 'Campo enfocado y seleccionado, Enter guarda, y atajos −0,5, −0,2, igual y +0,2.'),
        ('IN13', 'I2f', 'Flujo', 'bajo', 'bajo', 'La foto del día abre primero la hoja de fototeca de iOS y no la cámara.', 'Que abra la cámara directo, con la fototeca como segunda opción.'),
        ('IN14', 'franjas', 'Interfaz', 'bajo', 'medio', 'Las tres franjas (Mañana, Tarde, Noche) miden unos 350 px de alto cada una, con una ilustración grande para un solo dato.', 'Franjas más bajas, cabrita pequeña y la proteína de cada franja grande.'),
        ('IN15', 'I2b', 'Texto', 'bajo', 'bajo', 'En la ventana de pasos, «Sincronizar desde Salud» no sincroniza: te manda a Más.', 'Llamarlo «Cómo conectar Salud» y mostrar ahí mismo los pasos del Atajo.'),
    ])

informe('entrenar',
    'La sesión ya repite pesos con un toque y se retoma sola al abrir, que es lo que más importa en el gimnasio. Los riesgos están en datos que quedan mal guardados y en tocar con precisión con una mano.',
    [
        ('EN01', 'E2', 'Bug', 'alto', 'bajo', 'Al cambiar un ejercicio por otro, las series se rellenan con los pesos del original: el cambio solo guarda el sustituto y al marcar se usa el historial del ejercicio original. Queda guardado un peso que no levantaste.', 'Al sustituir, vaciar kg y reps de las series sin hacer y usar el historial del sustituto si lo hay.'),
        ('EN02', 'E2a', 'Bug', 'alto', 'bajo', 'Borrar una serie (con la X o deslizando) no tiene Deshacer, y la X de 26 px está pegada al check.', 'Deshacer en el aviso, como ya tiene quitar un ejercicio, y la X más separada.'),
        ('EN03', 'E2', 'Accesibilidad', 'alto', 'bajo', 'En el gimnasio, con una mano y sudado, los objetivos son chicos: círculos de serie de 28 px, casilla del ejercicio de 26 px y botón de gráfica de 32 px.', 'Zona de toque invisible de 44 px alrededor de cada uno, sin cambiar el dibujo.'),
        ('EN04', 'E2', 'Flujo', 'alto', 'medio', 'Durante la sesión la pantalla se apaga y el descanso no avisa con el teléfono bloqueado: el pitido no suena bloqueado y la vibración no existe en iOS.', 'Mantener la pantalla encendida mientras haya sesión abierta y un temporizador de descanso grande y visible.'),
        ('EN05', 'E2', 'Flujo', 'medio', 'bajo', 'La lista de la sesión dice «última 102,0 kg» pero no lo que toca hoy; el objetivo de progresión solo aparece al abrir el ejercicio.', 'En la fila: «Hoy: 104,5 × 6-8», con la regla de progresión ya aplicada.'),
        ('EN06', 'E2', 'Interfaz', 'medio', 'bajo', 'Cada ejercicio tiene tres controles sin rótulo en la cabecera: gráfica, «…» y una casilla vacía que no se sabe qué marca.', 'La casilla con su significado («Hecho») y la gráfica dentro del menú «…».'),
        ('EN07', 'E1', 'Flujo', 'medio', 'bajo', 'En Rutinas, la de hoy queda en la segunda fila, debajo del aviso de progresión e igual de grande que las demás.', 'Arriba una tarjeta «Hoy: Legs A · Empezar»; el aviso de progresión dentro de la sesión.'),
        ('EN08', 'E1', 'Texto', 'bajo', 'bajo', '«5 ej. · 28/09» no dice que la fecha es la última vez, y «RIR 1-2» no se explica en ningún lado.', '«5 ejercicios · última vez 28/09» y una «i» en RIR (repeticiones que te quedan en reserva).'),
        ('EN09', 'E2a', 'Flujo', 'medio', 'bajo', 'Editar kg y reps pide tocar campos de 58 y 50 px, y el teclado no pasa de kg a reps.', 'Botones ±2,5 kg y ±1 rep debajo del campo enfocado, y Siguiente pasa de kg a reps.'),
        ('EN10', 'E2', 'Flujo', 'bajo', 'medio', 'Hay cuatro maneras de dar un entreno por hecho (marcar hecho, completar con lo sugerido, sesión de un día pasado y registro libre) y dos quedan a un toque de un accidente.', 'Las que no registran series dentro de un menú «Marcar sin series».'),
        ('EN11', 'E5', 'Técnico', 'medio', 'bajo', 'Las fotos de los ejercicios no se guardan para usar sin señal: en el gimnasio sin datos las que no has visto no cargan.', 'Guardar en el teléfono las fotos de las rutinas activas de cada uno.'),
    ])

informe('agenda', 'El calendario es claro y la isla semanal funciona bien. Faltan detalles de lectura.', [
    ('AG01', 'A4', 'Flujo', 'medio', 'bajo', 'Un día pasado guarda sus datos en dos cajas plegadas y llegar desde Mes son 3 toques.', 'Abrir «Registro de ese día» por defecto.'),
    ('AG02', 'A3', 'Texto', 'bajo', 'bajo', 'Las siglas PA, PB, LA y LB no tienen leyenda; la de abajo explica colores, no siglas.', 'Al tocar un día, el nombre completo; y la leyenda con las siglas.'),
    ('AG03', 'A3', 'Interfaz', 'medio', 'bajo', 'Los días pasados sin registro se pintan en rojo como fallo, y el estándar pide acompañar, no regañar.', 'Gris punteado «sin registro»; el rojo solo si había un entreno planeado y no se hizo.'),
    ('AG04', 'A3', 'Texto', 'bajo', 'bajo', 'La fecha va en mayúscula sostenida («MIÉRCOLES 14 DE OCTUBRE 2026»).', 'Caja de oración.'),
])

informe('comida', 'El motor de la semana (recetas escaladas a la meta de cada uno y un mercado que compra lo que se cocina) es de lo más fuerte de la app. El problema es de entrada: lo diario no está donde la pestaña promete.', [
    ('CO01', 'C1', 'Flujo', 'alto', 'medio', 'La pestaña Comida no registra lo que comes: tiene Recetas, Mercado y Gestión. El registro está al fondo del Inicio y el registro libre dentro de Gestión.', 'Primera tarjeta de Comida: «Hoy», con las franjas y el + para registrar. Recetas, Mi semana y Mercado debajo.'),
    ('CO02', 'C1', 'Interfaz', 'medio', 'bajo', 'El orden y los íconos de las sub-pestañas no siguen el flujo: los pasos dicen Recetas → Gestión → Mercado y las pestañas van Recetas, Mercado, Gestión; el carrito está en Recetas y el plato en Mercado.', 'Recetas · Mi semana · Mercado, con el carrito en Mercado.'),
    ('CO03', 'C5', 'Texto', 'medio', 'bajo', 'Nombres internos a la vista: «Gestión alimentación», «rotación activa», «Meal prep compartido», «tuppers A y C».', '«Mi semana de comida», «tu semana armada» y «porciones de Andrés y de Cami».'),
    ('CO04', 'franjas', 'Flujo', 'medio', 'medio', 'Al registrar, el buscador no queda listo para escribir, la franja no se elige por la hora, «Medir en» apila 5 píldoras en vertical y después de agregar el buscador queda debajo del botón Guardar.', 'Buscador enfocado, franja según la hora, la unidad en una sola fila y el orden buscador, lista, total y Guardar.'),
    ('CO05', 'franjas', 'Flujo', 'medio', 'bajo', 'No hay forma de repetir lo de ayer (o el desayuno de siempre), que es lo que más se repite.', 'Un chip «Repetir lo de ayer» en la franja. «Lo tuyo» ya ayuda y se queda.'),
    ('CO06', 'C2', 'Flujo', 'medio', 'medio', 'Los pasos de una receta están en un desplegable dentro de otro (3 toques) y la pantalla se apaga mientras cocinas.', 'Modo cocinando: pasos grandes uno por uno, pantalla encendida y temporizador por paso.'),
    ('CO07', 'C3', 'Datos', 'medio', 'medio', 'En el mercado compartido solo el checklist se fusiona; las recetas elegidas, el plan, los ocultos y los favoritos los gana el último que guardó.', 'Fusionar por clave con su hora y avisar «Cami cambió el mercado».'),
    ('CO08', 'C2', 'Texto', 'bajo', 'bajo', 'Placeholders que se cortan: «busca: hamburguesa, huevos, arepa, (» e «Ítem libre (café, límpi…».', 'Placeholders cortos: «Busca un alimento», «Agrega algo a la lista».'),
])

informe('progreso', 'Las gráficas son de lo más cuidado (franjas de descarga, proyección, estilos). Falta que cada cifra se lea sola.', [
    ('PR01', 'P2', 'Datos', 'medio', 'medio', 'Las cifras compuestas no dicen de qué son porcentaje: Rendimiento 47 %, Fuerza +19 %, Resistencia 78 %, Movilidad 43 %. La gráfica marca de 0,5 a 2,5 mientras la cifra dice 47 %.', 'Una frase que la lea («cumpliste el 47 % de lo planeado en 30 días») y el eje en la misma unidad.'),
    ('PR02', 'P4', 'Interfaz', 'medio', 'bajo', 'Metas e Hyrox se repiten en las 5 pestañas de Actividad (Peso, Volumen, Pasos…), aunque no tengan que ver.', 'Solo en General.'),
    ('PR03', 'P3', 'Interfaz', 'medio', 'bajo', 'Las pestañas de Actividad son íconos sueltos (portapapeles, barras, reloj, mancuerna, pasos): no se sabe qué hay hasta tocar.', 'Rótulo corto en todas, o una fila desplazable con texto.'),
    ('PR04', 'P4, P8', 'Interfaz', 'bajo', 'bajo', 'Gráficas apretadas: en Pasos las fechas del eje se pegan («15/0917/0919/09…»), en Peso «DESCARGA» queda encima de los puntos y en Ejercicios hay un eje de 7 días para 2 puntos.', 'Menos marcas en el eje, la etiqueta de descarga arriba de la franja y el eje según los datos.'),
    ('PR05', 'P2', 'Flujo', 'medio', 'bajo', '«Cómo se calcula» abre la misma ventana en las 5 pestañas.', 'Una explicación por pestaña.'),
    ('PR06', 'P7', 'Texto', 'bajo', 'bajo', '«PRS DEL PERIODO», «TON. SEMANA», «E1RM», y 148,1 t junto a −11.029 kg en el mismo bloque.', '«Récords del periodo», «Volumen de la semana», «Fuerza máxima estimada» y una sola unidad por bloque.'),
])

informe('plan', 'El motor de etapas, checkpoints y diario de decisiones está muy completo. Lo que falta es que se lea en 10 segundos.', [
    ('PL01', 'PL4', 'Flujo', 'medio', 'medio', 'Plan son unos 9 bloques de texto seguidos y cada etapa trae 3 a 5 párrafos sin plegar: para saber si vas bien hay que leer un manual.', 'Cada etapa plegada con su dato clave (peso de salida, fechas, estado) y el texto en la ventana de detalle.'),
    ('PL02', 'PL1', 'Texto', 'medio', 'bajo', '«fuera dos semanas» en rojo (Plan, Check-in y Medidas) suena a regaño.', '«2 semanas sobre lo esperado» en ámbar, con la tolerancia de ±0,5 kg en el detalle.'),
    ('PL03', 'PL1', 'Texto', 'medio', 'bajo', 'El aviso «La proteína viene floja dos semanas. Adherencia de 29% y 29%…» sale igual en Check-in y en Plan.', 'Que viva en Plan y en Check-in sea una línea con enlace. Más simple: «Llevas dos semanas con 29 % de la proteína: súbela antes de tocar las calorías».'),
    ('PL04', 'PL4', 'Texto', 'bajo', 'bajo', 'Inglés técnico sin explicar: Cut final, Mini cut, taper, peak week, rescan.', 'Español con el término entre paréntesis la primera vez: «Definición final (cut)», «Nueva medición (rescan)».'),
])

informe('medidas', 'La portada de Medidas (lista de destinos con su dato) es de lo mejor resuelto de la app, y el formulario abre directo.', [
    ('MD01', 'MD12, MD4', 'Datos', 'medio', 'medio', 'Composición muestra la grasa por Navy (18,6 %) y por bioimpedancia (15,0 %) sin decir cuál manda; son 12 tarjetas y 8 párrafos.', 'Una cifra principal con su método, la otra como comparación plegada y una frase de por qué difieren.'),
    ('MD02', 'MD0b', 'Datos', 'alto', 'medio', 'Check-in y Medidas piden lo mismo y lo guardan en sitios distintos: medir la cintura en el check-in no apaga el pendiente de Medidas y la grasa Navy no la lee. Por eso la cintura sale 88,8 en Medidas y 92,5 en Check-in.', 'Que el check-in lea la última medición de Medidas (o escriba ahí), para medir una sola vez.'),
    ('MD03', 'MD2', 'Accesibilidad', 'bajo', 'bajo', 'El botón «Frente» va con texto oscuro sobre fondo oscuro, y en Hombros sale una raya larga en lugar de la cifra.', 'Contraste del botón y «sin dato» en vez de la raya.'),
    ('MD04', 'MD1', 'Texto', 'bajo', 'bajo', '«Te acercas: peso de hoy en 1 día. Puedes adelantarla ya: se registra cuando sea» no se entiende.', '«Te toca medirte mañana. Si quieres, hazlo hoy y queda registrado.»'),
])

informe('fotos', 'Borrar una foto tiene confirmación y Deshacer con la imagen guardada: es el mejor patrón de borrado de la app y debería copiarse en el resto.', [
    ('FT01', 'FT1', 'Datos', 'alto', 'medio', '«Foto privada» no protege el archivo: todas suben a un bucket público (ver G10 en General).', 'Bucket privado o, mientras tanto, nombre aleatorio y un texto honesto.'),
    ('FT02', 'FT1', 'Técnico', 'medio', 'bajo', 'Si una foto no alcanza a subir por falta de señal, queda solo en el teléfono y nunca se reintenta.', 'Reintentar al volver la señal y mostrar «2 fotos sin subir».'),
])

informe('checkin', 'La espera cuantificada («entrenos esperando el check-in») está muy bien. Duplica cosas de Plan y Medidas.', [
    ('CK01', 'K4', 'Interfaz', 'medio', 'bajo', 'La tabla Evolución tiene 6 columnas con abreviaturas (ADH., CINT., E/S) que solo se explican al pie, y la columna Grasa va llena de puntos.', 'Encabezados completos con desplazamiento lateral o una tarjeta por semana, y «sin dato» en vez de puntos.'),
    ('CK02', 'K2', 'Flujo', 'medio', 'bajo', 'Pide a mano los pasos promedio de la semana cuando la app ya los tiene.', 'Calcularlos y mostrarlos para confirmar.'),
    ('CK03', 'K1', 'Flujo', 'medio', 'bajo', 'Llegar al check-in del domingo pide ir al Perfil y bajar hasta Accesos.', 'Que el recordatorio y una tarjeta del Inicio el domingo lleven directo, y la entrada en el menú del avatar (G01).'),
])

informe('retos', 'El versus de los cabritos es el momento con más carácter de la app. Son ajustes de lectura.', [
    ('RE01', 'R1, R2', 'Interfaz', 'bajo', 'bajo', 'El marcador va apretado («Cami ★7 ★2 ★1 5 – 2 ★2Andrés»), con nombres cortados y un «VS» fantasma detrás del título.', 'Marcador en dos líneas: avatares y puntos grandes arriba, estrellas debajo; sin el VS de fondo.'),
    ('RE02', 'R2', 'Texto', 'bajo', 'bajo', 'Textos crípticos: «semana del 12/10 · 4 D», «bonus entrenos: 1 · 1», «puntos (máx 49)».', '«Faltan 4 días», «Entrenos bonus: Cami 1, Andrés 1», «Cami lidera 5 a 2 (máximo 49)».'),
    ('RE03', 'R1', 'Flujo', 'medio', 'bajo', 'Retos solo se encuentra manteniendo oprimido el avatar o si aparece una tarjeta en el Inicio.', 'Entrada en el menú del avatar (G01).'),
])

informe('perfil', 'Funciona como centro de la app, pero lo que más se busca está al final.', [
    ('PF01', 'PF7', 'Flujo', 'medio', 'bajo', 'Los Accesos (Progreso, Check-in, Medidas, Plan, Ajustes) están al fondo del Perfil, después del héroe, los trofeos y las estadísticas.', 'Subirlos justo debajo del héroe.'),
    ('PF02', 'PF7', 'Texto', 'bajo', 'bajo', 'Queda un texto sobrante: «Llegaste aquí tocando tu propio avatar».', 'Quitarlo.'),
])

informe('mas', 'Todo está, pero mezcla lo que se toca cada semana con lo que se toca una vez al año.', [
    ('MA01', 'M1', 'Interfaz', 'medio', 'bajo', 'Más abre con 7 recordatorios de unos 230 px cada uno; la nube, el PIN y los datos quedan muy abajo.', 'Secciones plegadas con su estado en la cabecera: Recordatorios (5 activos), Apariencia, Nube y datos (al día), Hyrox (encendida).'),
    ('MA02', 'M10', 'Datos', 'medio', 'bajo', '«Borrar mis datos» borra el teléfono, pero con la nube conectada todo vuelve al recargar.', 'Decirlo y ofrecer aparte «Borrar también de la nube» con doble confirmación.'),
    ('MA03', 'M9', 'Texto', 'medio', 'bajo', 'Mensajes técnicos para el usuario: «Corre supabase-schema.sql en el SQL Editor», «RLS sin política», «llave equivocada».', 'Un texto humano («No se pudo subir ahora; se reintenta solo») y el diagnóstico solo en «Probar conexión».'),
    ('MA04', 'M7', 'Flujo', 'medio', 'medio', 'No hay un lugar que diga qué ve tu pareja de ti (puntos, entrenos, fotos marcadas), y el PIN evita curiosear pero no cifra nada.', 'Una sección «Qué ve Cami de mí» y «Qué ve Andrés de mí», y una línea honesta sobre lo que hace el PIN.'),
])

informe('hyrox', 'Bien resuelto que diga en pantalla cuáles baremos son reales (SkiErg y Sled Push) y cuáles no.', [
    ('HX01', 'HX0', 'Interfaz', 'bajo', 'bajo', '«3/8» aparece 4 veces en la portada y «1:17:39» dos veces en Tu nivel.', 'Cada cifra una sola vez.'),
    ('HX02', 'HX3', 'Interfaz', 'bajo', 'bajo', 'El carrusel de sesiones corta el texto a mitad («con 45 segundos de…»).', 'Altura según el contenido o «Ver más».'),
    ('HX03', 'HX2', 'Texto', 'bajo', 'bajo', '«Mide farmers»; percentiles, baremo y lastre sin definir.', '«Empieza midiendo Farmers» y una «i» en los términos.'),
])

# ---------------------------------------------------------------- novedades (lo ultimo publicado, REV 215 a 222)
NOV = [
    ('inicio', 'REV 215', 'Tus metas en el Inicio', 'Rejilla plegada con la etapa siempre visible y la meta de la esquina del héroe a elección.'),
    ('inicio', 'REV 217', 'Fuera las instrucciones de las cajas', 'El espacio de "toca para registrar" se fue a los datos: anillo de pasos más grande y vaso de agua más alto.'),
    ('inicio', 'REV 221', 'La meta de la esquina puede ser cualquier medida', 'No solo la cintura.'),
    ('plan', 'REV 215', 'Plan por etapas', 'Vista propia con semáforo, checkpoints, rescans, creatina y diario de decisiones.'),
    ('plan', 'REV 220', 'La caja de etapa, reordenada', 'El peso a la izquierda y la gráfica más pequeña a la derecha.'),
    ('medidas', 'REV 215', 'Medidas reorganizada', 'Portada con destinos rotulados y salto entre hermanos por hoja inferior.'),
    ('medidas', 'REV 222', 'Las medidas se registran sin saltos', 'El número es el control (se arrastra) y se corrigieron bugs del recorrido.'),
    ('hyrox', 'REV 215', 'Hyrox reorganizada', 'Portada con destinos, como Medidas.'),
]
for i, (sec, cod, tit, det) in enumerate(NOV):
    add('novedades', f'nov-{i+1:02d}', {'seccion': sec, 'codigo': cod, 'titulo': tit, 'detalle': det, 'lote': 'REV 215 a 222', 'publicado': '2026-09-23', 'orden': i})

# ---------------------------------------------------------------- hitos: fases
FASES = [
    ('Plan de revisión general (aprobado 24/08)', 'Fase 1 · Movimiento', 'hecho', 'Número rodante, pestañas que se despliegan, transición entre vistas (REV 208).'),
    ('Plan de revisión general (aprobado 24/08)', 'Fase 2 · Tres niveles', 'hecho', 'Cifra, desglose plegado y ventana en Comida, Agenda, Check-in y Retos (REV 209).'),
    ('Plan de revisión general (aprobado 24/08)', 'Fase 3 · Menos toques', 'hecho', '"Lo tuyo" en el buscador, micro-confirmaciones y hoja inferior (REV 210).'),
    ('Plan de revisión general (aprobado 24/08)', 'Fase 4 · Deuda', 'hecho', 'Cero botones sin nombre, tabla que cabe a 320 px, leche sin duplicar (REV 211).'),
    ('Plan de revisión general (aprobado 24/08)', 'Fase 5 · Tema claro', 'en_curso', 'Infraestructura en REV 213. Faltan ilustraciones, contraste del acento como texto y el barrido final.'),
    ('Plan por etapas y medidas (19/09)', 'Las 8 fases', 'hecho', 'Etapas, checkpoints, semáforo, rescans, creatina, diario, Medidas reorganizada y metas en el Inicio (REV 215 a 221).'),
    ('Análisis UX y mesa de revisión (14/10)', 'Análisis', 'hecho', '30 pantallas por usuario, cuatro auditorías y la verificación en el código.'),
    ('Análisis UX y mesa de revisión (14/10)', 'Tus decisiones', 'en_curso', 'Marcar Va o responder en los informes de cada sección.'),
    ('Análisis UX y mesa de revisión (14/10)', 'Lote 1 · Arreglos rápidos', 'pendiente', 'Bugs verificados y tarjetas cortadas.'),
    ('Análisis UX y mesa de revisión (14/10)', 'Lote 2 · Que nada se pierda', 'pendiente', 'Nube, sincronización, importar y almacenamiento.'),
    ('Análisis UX y mesa de revisión (14/10)', 'Lote 3 · Dónde vive cada cosa', 'pendiente', 'Barra, menú del avatar y registro de comida.'),
    ('Análisis UX y mesa de revisión (14/10)', 'Lote 4 · Leer menos', 'pendiente', 'Glosario, metas con nombre fijo y textos plegados.'),
    ('Análisis UX y mesa de revisión (14/10)', 'Lote 5 · Accesibilidad', 'pendiente', 'Tamaño de texto, ventanas y cierre del tema claro.'),
]
for i, (plan, tit, est, det) in enumerate(FASES):
    add('hitos', f'fase-{i+1:02d}', {'tipo': 'fase', 'plan': plan, 'titulo': tit, 'estado': est, 'detalle': det, 'orden': i})

HITOS = [
    ('2026-07-29', 'REV 64', 'CabriCoach se vuelve app instalable', 'PWA en Netlify con fuentes embebidas y la fecha de las fotos leída del EXIF.'),
    ('2026-07-30', 'REV 70 a 73', 'Sesión de entreno rediseñada', 'Tabla de series, récords, isla flotante, reloj de descanso e importar entreno.'),
    ('2026-07-30', 'REV 80 a 85', 'Nutrición en el Inicio', 'Anillo de proteína, tres franjas del día y 739 alimentos colombianos validados.'),
    ('2026-07-30', 'REV 91', 'Planificador semanal por día', 'Cada día elige rutina, movilidad o descanso.'),
    ('2026-07-31', 'REV 100', 'Sistema tipográfico y estándar Night Gym', 'Cuatro familias con rol fijo; el estándar visual lo escribió Andy y manda.'),
    ('2026-08-01', None, 'El repo se cuida solo', 'Hook de pre-commit que verifica y sincroniza site/, y setup para computador nuevo.'),
    ('2026-08-01', None, 'Las cabritas en los ejercicios', '149 fotos generadas en el space del personaje; el catálogo quedó completo el 02/08 (289).'),
    ('2026-08-02', 'REV 104', 'La app baja de 4,3 MB a 991 KB', 'Las imágenes de la interfaz salen del HTML a archivos sueltos.'),
    ('2026-08-02', 'REV 105 a 117', 'La semana de comida', 'Recetas escaladas a la meta de cada uno y un mercado que compra la semana real, con precios verificados.'),
    ('2026-08-02', 'REV 111', 'Metas que se calculan con el peso', 'Proteína por kilo sobre el promedio semanal de pesajes.'),
    ('2026-08-04', 'REV 124 a 126', '1.924 productos de supermercado', 'Buscador con productos colombianos y código de barras.'),
    ('2026-08-07', 'REV 130', 'Movilidad guiada y metas de fuerza', 'Player con temporizador, mapa de cabra y swipe para navegar.'),
    ('2026-08-09', 'REV 136', 'La vista se actualiza en sitio', 'El morph acabó con los saltos al escribir.'),
    ('2026-08-09', 'REV 142', 'Nace Medidas', 'Mapa corporal, Navy con fórmula visible y cadencia por grupo.'),
    ('2026-08-10', 'REV 157 a 182', 'Ficha de 301 ejercicios y capas de fuerza', 'Carga, Fuerza y Cruce sobre el mismo mapa, con nivel por músculo.'),
    ('2026-08-10', 'REV 184', 'Nuevas metas de Andrés', '2.400 kcal y 150 g de proteína con piso de 140.'),
    ('2026-08-11', 'REV 188 a 190', 'Tablas de fuerza verificadas', 'Y la auditoría automática de objetivos táctiles.'),
    ('2026-08-12', 'REV 191', 'Creatina como objetivo diario', 'Con lo que hace en la báscula para que no se lea como "dejé de bajar".'),
    ('2026-08-12', 'REV 196 y 197', 'El déficit se fija y va en rampa', '500 kcal arriba, 250 en la meta; las calorías salen del gasto.'),
    ('2026-08-18', 'REV 206', 'Las cinco rutinas nuevas de Cami', 'Las viejas pasaron al archivo sin borrarse.'),
    ('2026-08-23', 'REV 207', 'Hyrox completo', 'Y el rediseño de jerarquías de Medidas y Progreso.'),
    ('2026-08-24', 'REV 208 a 212', 'Plan de revisión general, fases 1 a 4', 'Más los injertos de transitions.dev.'),
    ('2026-08-26', 'REV 213', 'Infraestructura del tema claro', 'Tokens, interruptor por usuario y modo automático por hora.'),
    ('2026-09-19', 'REV 215 a 221', 'Plan por etapas y metas en el Inicio', 'Checkpoints, semáforo, rescans y diario de decisiones.'),
    ('2026-09-23', 'REV 222', 'Medidas que se registran sin saltos', 'Último deploy en producción.'),
    ('2026-10-14', None, 'Análisis UX completo y esta mesa', '30 pantallas por usuario con datos sembrados, cuatro auditorías y la mesa de revisión.'),
]
for i, (f, rev, tit, det) in enumerate(HITOS):
    add('hitos', f'hito-{i+1:02d}', {'tipo': 'hito', 'fecha': f, 'rev': rev, 'titulo': tit, 'detalle': det, 'orden': 100 + i})

# ---------------------------------------------------------------- aprendizajes
APR = [
    ('El archivo', 'Nunca buscar con grep amplio sobre el archivo', "Tiene fuentes en base64 en líneas muy largas: un grep amplio se cuelga o encuentra basura. Buscar con python3 limpiando antes los data-URI con re.sub(r'data:[a-z0-9/+.-]+;base64,[A-Za-z0-9+/=]+','data:B',t). La clase debe incluir dígitos o woff2 no se limpia.", 'CLAUDE.md del proyecto'),
    ('El archivo', 'Un solo agente a la vez editando el archivo', 'Dos agentes en paralelo se pisan las ediciones, y un conflicto en el archivo único es irresoluble a mano. Leer y auditar en paralelo sí se puede.', 'Memoria de Claude'),
    ('El archivo', 'Claves duplicadas en ACTIONS y CHANGES', 'En un objeto grande gana la última clave y la otra queda muerta en silencio. Así se rompieron el registro de medidas y el botón de cambiar ejercicio (REV 222). Buscar duplicados al tocar esos objetos.', 'REV 222'),
    ('El archivo', 'SOLID gana sobre ICONS', 'ic() consulta primero los íconos rellenos: un ícono de trazo con un nombre repetido nunca se ve. Usar un nombre nuevo.', 'DESIGN-STANDARDS §4'),
    ('El archivo', 'iCloud deja archivos sin descargar', 'Documents se sincroniza y puede dejar archivos "dataless". Si una lectura o un Edit tarda una eternidad, revisar con ls -lO antes de culpar al entorno.', 'Memoria de Claude'),
    ('El archivo', 'El MAPA es el idioma común', 'Los códigos de zona (I4b, C3d, P2d) sirven para señalar sin ambigüedad. Se quedan con la zona, no con la posición, y el MAPA se actualiza cada vez que algo se mueve.', 'MAPA.md'),
    ('Probar y verificar', 'No hay suite de tests', 'La red de seguridad es herramientas/verificar.py con el parser JavaScriptCore de macOS, en modo diferencial contra un snapshot tomado antes de empezar. Lo que importa es no introducir hallazgos nuevos.', 'PRUEBAS.md'),
    ('Probar y verificar', 'Siempre por http, nunca file://', 'Con file:// el localStorage se bloquea. Servir con python3 -m http.server y probar en Chrome headless por CDP a 390 × 844.', 'PRUEBAS.md'),
    ('Probar y verificar', 'Limpiar el service worker antes de navegar', 'Si no, se prueba una versión vieja. Y la página no se recarga sola después de editar: hay que navegar de nuevo.', 'PRUEBAS.md'),
    ('Probar y verificar', 'innerText miente con content-visibility', 'Las secciones no pintadas devuelven texto vacío: usar textContent. Y medir el layout dos veces, porque tras render() hay marcadores de 240 px.', 'ARQUITECTURA §3'),
    ('Probar y verificar', 'En headless las animaciones se congelan', 'Las transiciones y los requestAnimationFrame no avanzan si nadie mira. El render de la app usa rAF, así que después de cambiar de vista hay que forzar 4 a 6 capturas antes de medir.', 'PRUEBAS.md, 24/08'),
    ('Probar y verificar', 'Cambiar de usuario en pruebas', "ACTIONS._doSwitch('cami') salta el PIN. confirm() bloquea el headless: sobreescribir window.confirm antes del clic.", 'PRUEBAS.md'),
    ('Probar y verificar', 'Cada agente en su propia pestaña de Chrome', 'El 14/10 un agente navegó la pestaña compartida y tumbó una captura a mitad. Abrir pestaña propia con /json/new.', 'Análisis del 14/10'),
    ('Probar y verificar', 'Sembrar datos para ver la app de verdad', 'Con el estado vacío muchas pantallas no muestran nada. ?demo=1 da 18 días de Andrés sin guardar; el análisis del 14/10 sembró 70 días de peso, pasos, agua, comidas, entrenos, medidas y Hyrox para los dos (herramientas/sembrar-datos-prueba.js, con el ayudante de CDP en herramientas/cdp_pruebas.py).', 'Análisis del 14/10'),
    ('Publicar', 'Push a main es el deploy', 'Netlify publica cabricoach.netlify.app con cada push a main de cabrihou/Cabricoach. Commitear sin push está bien mientras Andy revisa en local.', 'CLAUDE.md del proyecto'),
    ('Publicar', 'Subir APPREV y el caché del service worker', "APPREV ('REV N') en el HTML y cabritos-vN en sw.js y site/sw.js; si no, los teléfonos no actualizan. El hook de pre-commit verifica, avisa y sincroniza site/index.html.", 'CLAUDE.md del proyecto'),
    ('Publicar', 'git pull --rebase antes de tocar nada', 'Si dos computadores editan el archivo en paralelo, toca descartar el trabajo de uno.', 'CLAUDE.md del proyecto'),
    ('Publicar', 'Revisión en dos capas antes de Andy', 'El agente entrega con verificador y CDP; la sesión coordinadora revisa capturas como director de producto; después Andy en local. Nada se despliega sin que él lo vea.', 'PLAN-REVISION-GENERAL'),
    ('Diseño', 'Night Gym con un solo acento', 'Fondo #0B0D0F, azul de Andrés, dorado de Cami y verde en nutrición (scopeOf). El rojo solo para alertas, récords y meta.', 'DESIGN-STANDARDS §1'),
    ('Diseño', 'Cuatro familias con rol fijo', 'League Spartan solo para Display (hoy solo Retos), Outfit para títulos, Archivo para toda cifra con tabulares e Instrument Sans para el resto. Ningún campo bajo 16 px por el zoom de iOS.', 'DESIGN-STANDARDS §3'),
    ('Diseño', 'Sistema de tres niveles', 'La cifra arriba, el desglose plegado y la explicación en una ventana (INFO3). Ninguna vista con más de unas 4 líneas de texto corrido sin pedirlas.', 'PLAN-REVISION-GENERAL'),
    ('Diseño', 'Las ventanas flotantes no sirven para lo diario', 'Se probaron en el Inicio y se revirtieron: ahí las cajas son el contenido. Sirven para herramientas ocasionales.', 'DESIGN-STANDARDS §4'),
    ('Diseño', 'Las cajas se abren solas una vez al día', 'Cuando el contexto lo amerita (Con qué cerrar pasadas las 7 pm). Si el usuario la cierra, se respeta.', 'DESIGN-STANDARDS §4'),
    ('Diseño', 'Confirmar con qué pasó y su efecto', '"Serie 3 · 12 reps · +10 XP", nunca un "Guardado" seco.', 'REV 210'),
    ('Diseño', 'Sin instrucciones dentro de las cajas del Inicio', 'Desde REV 217 el espacio va a los datos; las instrucciones viven en la ventana de detalle.', 'REV 217'),
    ('Diseño', 'El tema claro va por tokens', 'html[data-tema=claro] redefine superficies y tintas; los acentos son identidad y no cambian. Nada de blancos o negros fijos en CSS nuevo: usar --lift y los tokens.', 'DESIGN-STANDARDS §4b'),
    ('Imágenes', 'Siempre en el space del personaje', 'Magnific, space "Character Model Sheet Development", pestaña Andrés o Cami con la referencia conectada. En otro space sale otro personaje (pasó y costó una tanda).', 'DESIGN-STANDARDS §5'),
    ('Imágenes', 'Reglas del prompt', 'Sin texto en la imagen, sin collar ni campana, una sola mascota, y la pose ES el ejercicio con su apoyo visible. Para máquinas: "unbranded machine, no logos" (hx_ski y hx_row salieron con Concept 2).', 'DESIGN-STANDARDS §5'),
    ('Imágenes', 'Salida y costo', 'JPEG 480 × 480 a assets/ej/ y copia en site/assets/ej/. Las de interfaz van a assets/cab/ y a UI_IMGS de los dos sw.js. Generar cuesta créditos: solo cuando Andy lo pida.', 'CLAUDE.md del proyecto'),
    ('Decisiones del plan', 'Andrés: el riesgo es comer de menos', 'Usa retatrutida, que quita el apetito. Todo lo de nutrición empuja a llegar a la proteína, nunca a restringir.', 'ARQUITECTURA §1'),
    ('Decisiones del plan', '150 g de proteína con piso de 140', '195 g era inalcanzable (la adherencia real era 120 a 125). 150 g con un déficit chico preserva más masa magra que 125 reales con uno grande. Dos scoops de whey fijos (48 g) se descuentan del reparto.', 'CONTEXTO, agosto'),
    ('Decisiones del plan', 'Se fija el déficit, no las calorías', 'kcal(peso) = kcal_base + 15 × (peso − peso_base); los 15 kcal/kg salen de Mifflin-St Jeor con actividad de ~1,5. Andrés en rampa de 500 a 250; Cami fija en 330.', 'CONTEXTO, REV 196'),
    ('Decisiones del plan', 'Creatina: 3 g diarios desde el 7 de agosto', 'Sube el peso 0,8 a 1,6 kg en Andrés y 0,6 a 1,2 en Cami en unas 5 semanas por agua dentro del músculo. La app lo descuenta en el peso comparable. No entra en la racha ni en los retos.', 'CONTEXTO, agosto'),
    ('Decisiones del plan', 'La meta de agua usa el peso del día', '30 ml por kilo, +300 en días de entreno y +250 por la creatina mientras satura (+150 después), con tope de 3,5 L.', 'CONTEXTO, REV 195'),
    ('Decisiones del plan', 'Hyrox: solo dos baremos son reales', 'SkiErg y Sled Push tienen tabla por nivel; lo demás se compara contra el promedio general y el propio historial, y la app lo dice. Las marcas viven en S.hyrox y nunca en S.logs. Wall balls Open mujer: 75 reps sin confirmar contra el rulebook.', 'Memoria de Claude, 23/08'),
    ('Decisiones del plan', 'Las rutinas viejas no se borran', 'Pasan al archivo (ocultas) para que el historial siga resolviendo nombres y fotos.', 'CONTEXTO, 12/08'),
    ('Decisiones del plan', 'El plan por etapas manda', 'Las etapas reemplazan la meta vieja. Factor de actividad 1,45 para Andrés y 1,49 para Cami, que se recalibra solo con 21 días de comida y una recta de peso; freno de cintura de +1,5 cm en el volumen.', 'PLAN-ETAPAS-Y-MEDIDAS'),
    ('Nube y datos', 'La nube es opcional y sin login', 'Supabase, tabla kv con código de casa y llave anónima: el aislamiento lo da el código. La sesión en curso y los avisos disparados no se sincronizan.', 'ARQUITECTURA'),
    ('Nube y datos', 'Al abrir, la nube manda', 'Y hoy eso puede pisar lo que no alcanzó a subir (hallazgo G06 del 14/10).', 'Análisis del 14/10'),
    ('Nube y datos', 'Lo que no viaja por git', '~/.config/cabritos.env (credenciales) y la programación del coach diario. En el MacBook todavía no existe el cabritos.env.', 'CLAUDE.md del proyecto'),
]
for i, (tema, tit, txt, fte) in enumerate(APR):
    add('aprendizajes', f'apr-{i+1:02d}', {'tema': tema, 'titulo': tit, 'texto': txt, 'fuente': fte, 'orden': i})

# ---------------------------------------------------------------- pendientes
PEND = [
    ('andy', 'alta', 'Revisar el análisis y marcar Va en lo que quieres', 'Cada sección tiene su informe con hallazgo, propuesta, impacto y esfuerzo. Lo que marques Va entra al primer lote; lo que respondas, lo ajusto antes de tocar la app.', 'Análisis del 14/10'),
    ('andy', 'alta', 'Decidir las 5 preguntas de fondo', 'Están en el informe de General, en "Lo que necesito que decidas": rótulos en la barra, dónde se registra la comida, push o calendario, bucket privado de fotos e idioma de los ejercicios.', 'Análisis del 14/10'),
    ('andy', 'media', 'Probar en el iPhone tres cosas que el navegador de pruebas no ve', '1) Si los recordatorios suenan con la app abierta y con la app cerrada. 2) Si el Atajo de Salud con ?steps= llega a la app instalada o se queda en Safari. 3) Si la pantalla se apaga durante el descanso.', 'Análisis del 14/10'),
    ('andy', 'media', 'Correr los 3 nodos de imagen pendientes', 'En el space "Character Model Sheet Development": hx_ski y hx_row con "unbranded machine, no logos" en el prompt, y hx_zercher_carry con la barra en los codos. Cuestan créditos. Cuando estén, Claude los baja a 480 × 480 y los instala.', 'Plan de revisión, Fase 4'),
    ('andy', 'media', 'Crear ~/.config/cabritos.env en este Mac', 'Con la URL, la llave y el código de casa (están en la app, en Más > Nube). Activa el coach diario y deja que Claude lea la nube real en solo lectura para analizar con tus datos y no con datos de prueba.', 'CLAUDE.md del proyecto'),
    ('andy', 'baja', 'Confirmar las wall balls de Open mujer (75)', 'Tres fuentes contra una; falta el rulebook oficial. Si es otro número, se cambia en el catálogo Hyrox.', 'Hyrox, 23/08'),
    ('claude', 'alta', 'Armar el lote 1 con lo que marques Va', 'Empezar por los bugs verificados (isla, nodo de comidas, gesto de volver, sustituto, borrar serie, tarjetas cortadas), con snapshot, verificador, CDP a 390 px y los dos usuarios. Commit sin push hasta que lo revises en local.', 'Análisis del 14/10'),
    ('claude', 'media', 'Cerrar la Fase 5: tema claro', 'Tratamiento de las ilustraciones de Retos y miniaturas, tonos de texto para el acento en claro, barra de estado de iOS, tema antes del primer pintado y barrido de las 12 vistas por usuario.', 'Plan de revisión, Fase 5'),
    ('claude', 'media', 'Poner docs/CONTEXTO.md al día', 'Se quedó en REV 130 (03/08). Que apunte a esta mesa como estado vivo y recoja lo que pasó del 07/08 al 14/10.', 'Análisis del 14/10'),
    ('claude', 'baja', 'Quitar docs/PROYECTO.md', 'Es un archivo vacío desde el 10/08.', 'Análisis del 14/10'),
    ('juntos', 'media', 'Instalar el coach diario', 'Después del cabritos.env: zsh herramientas/coach-diario/instalar.sh. Escribe la evaluación del día que la app ya sabe leer.', 'CLAUDE.md del proyecto'),
]
for i, (quien, prio, tit, det, origen) in enumerate(PEND):
    add('pendientes', f'pend-{i+1:02d}', {'titulo': tit, 'detalle': det, 'quien': quien, 'prioridad': prio, 'estado': 'abierto', 'origen': origen, 'orden': i, 'creadoEn': AHORA})

# ---------------------------------------------------------------- escribir
for col, id_, data in docs:
    d = os.path.join(BASE, col)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, id_ + '.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
writes = [{'op': 'set', 'collection': col, 'doc_id': id_, 'file_path': os.path.join(BASE, col, id_ + '.json')} for col, id_, _ in docs]
lotes = [writes[i:i + 50] for i in range(0, len(writes), 50)]
json.dump(lotes, open(os.path.join(BASE, 'lotes.json'), 'w'), ensure_ascii=False)
cuenta = {}
for col, _, _ in docs:
    cuenta[col] = cuenta.get(col, 0) + 1
print(cuenta, 'total', len(docs), 'lotes', [len(l) for l in lotes])
# chequeo de rayas largas en todo lo que se muestra
malos = [(c, i) for c, i, d in docs if '—' in json.dumps(d, ensure_ascii=False)]
print('con raya larga:', malos)
