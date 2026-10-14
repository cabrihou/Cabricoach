# Bitácora de la mesa de revisión

Una entrada por pasada: qué llegó, qué se decidió, qué se construyó y qué quedó.

## 2026-10-14 · Nace la mesa con el análisis UX completo

Pedido de Andy: un análisis exhaustivo de UI y UX de CabriCoach, un artifact con el
aprendizaje, el progreso y los pendientes, y un revisor como el del tablero.

Qué se hizo:

- **Análisis**: la app (REV 222) en Chrome headless a 390 × 844 con 70 días sembrados
  para los dos usuarios (peso, pasos, agua, creatina, comidas, entrenos, check-ins,
  medidas, Hyrox), 30 pantallas por usuario más los flujos abiertos (registrar comida,
  marcar serie, peso, pasos, tema claro). Cuatro auditorías de código en paralelo con
  Sonnet (flujos y toques, estados y robustez, texto y carga cognitiva, rendimiento/PWA/
  accesibilidad) y verificación en el código de los hallazgos graves.
- **Mesa**: página adaptada de la del tablero (paleta y fuentes de CabriCoach, vista
  Proyecto con pendientes, progreso y aprendizajes, informe con "Va", chips de impacto y
  capturas de celular). Sembrada con 14 secciones con sus zonas del MAPA, 24 capturas,
  un informe por sección (89 hallazgos con propuesta), 8 novedades (REV 215 a 222), 13
  fases y 26 hitos, 40 aprendizajes y 11 pendientes.

Hallazgos graves verificados en el código: la nube reescribe lo local sin comparar fechas
y no reintenta envíos fallidos (G06), importar un respaldo no confirma (G08), el nodo de
comidas del checkpoint no es tocable por una clave mal escrita (IN02), el gesto de volver
ignora `backTo` (G03), cambiar un ejercicio rellena con los pesos del original (EN01) y la
isla de la rutina aparece con solo abrir una rutina (G02).

Qué falta: que Andy marque Va o responda en los informes y decida las 5 preguntas de fondo
del informe General. Con eso se arma el lote 1 (arreglos rápidos y verificados).

## 2026-10-14 · Segunda pasada con el plugin Design de Anthropic (lote 2026-10-14b)

Pedido de Andy: revisar la app con la skill Design que agregó y decir qué aportó frente a
lo que ya se sabía. La skill agregada en claude.ai no llegaba a Claude Code, así que se
instaló el plugin con `claude plugin marketplace add anthropics/knowledge-work-plugins` y
`claude plugin install design@knowledge-work-plugins` (versión 1.2.0).

Qué se hizo: crítica de diseño por pantalla (design-critique), auditoría WCAG 2.1 AA
medida en Chrome (accessibility-review; scripts en `herramientas/a11y_medir.js` y
`herramientas/a11y_run.py`), revisión de textos (ux-copy, agente Sonnet), auditoría del
sistema de diseño (design-system, agente Sonnet, 54/100) y plan de investigación
(user-research). Sembrado como un segundo informe en 8 secciones: 35 hallazgos nuevos
(3 de impacto alto, 23 medio, 9 bajo), más lo que aportó la skill, lo que confirmó del
primer informe, lo que no ve, la auditoría WCAG en números y el plan de investigación.

Lo nuevo más fuerte: bordes de campos y controles a 1,26:1 (WCAG 1.4.11), las 22
confirmaciones nativas que no dejan nombrar los botones, la app rota al 200 % de zoom,
35 de 50 controles de la sesión sin teclado, y un sistema de diseño sin escalas de
espaciado, letra ni movimiento con un estándar escrito que no coincide con el CSS.

## 2026-10-14 · REV 223, lote 1 (en local, sin deploy)

Pedido de Andy: "corrige lo más urgente y prioritario y levántala en un servidor local antes
de hacer deploy". Se tomó lo que no necesitaba una decisión suya (las 5 preguntas de fondo
siguen abiertas).

Hecho (18 cambios, ver Novedades en la mesa): la nube marca lo que no alcanzó a subir, no lo
pisa al bajar y lo reintenta al volver la señal (G06); importar respaldo con confirmación,
bloqueo de respaldo ajeno, sin tocar lo compartido ni el PIN y con Deshacer (G08); isla solo
con series marcadas y espacio al pie (G02); gesto de volver igual al botón (G03); sustituto
con sus propios kg (EN01); Deshacer en serie, pesaje y sesión de Hyrox; hoja de
confirmación propia (`hojaConfirmar`) en borrar día, sesión a medias e importar (DG08,
parcial); bordes de controles a 3:1 con `--line-ctl` (DG01); área de toque de 44 px de alto
en la sesión (EN03); pantalla encendida en la sesión (EN04); nodo de comidas tocable y
rótulos completos (IN02); tarjetas del checkpoint sin desbordes (IN03); avisos que duran
según su largo; aviso de almacenamiento lleno y `storage.persist` (G11); service worker que
espera la red 3 s y abre lo guardado (G12); textos de cámara y fotos con el paso para
arreglar (DG09).

Verificación: verificador sin regresiones (0 fallos, 39 avisos heredados); 37 de 37 pruebas
de `herramientas/pruebas_rev223.py` con clics reales, los dos usuarios, 13 vistas, 320 px,
nube falsa sin señal y 0 errores de consola; capturas revisadas. `site/` sincronizado con
`publicar.sh`. APPREV 'REV 223', caché `cabritos-v167` en los dos sw.js.

Servidor de revisión: `python3 -m http.server 8223 --bind 0.0.0.0 --directory site`
(http://localhost:8223/?demo=1). Andy dio el go: commit `8e8c7e8`, push a main y
Netlify confirmado en producción (cabricoach.netlify.app sirve REV 223 y `cabritos-v167`).
Quedan para otro lote: ~18 `confirm()` nativos por migrar (incluido "pegar registros",
que mezcla Aceptar/Cancelar con reemplazar/sumar), indicador de sincronización visible,
aviso de versión nueva y temporizador de descanso grande.
