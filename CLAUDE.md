# CabriCoach

App de entrenamiento y nutrición de Andrés y Cami. PWA de **archivo único**, sin build
step, sin node, sin dependencias: todo va embebido como data-URI en base64.

**Para trabajar en la app, usa el agente `cabricoach`** (`.claude/agents/cabricoach.md`):
tiene la arquitectura, las trampas del archivo, el sistema tipográfico y el flujo de
publicación.

## Estructura

```
coach-afc-v2.html      la fuente · es lo único que se edita
site/                  lo que se despliega (copia de la fuente + assets)
assets/                imágenes y videos que usa la fuente al abrirla local
docs/                  proyecto, estándar de diseño, mapa de zonas, indicaciones
herramientas/          verificar.py y el coach diario
archivo/               prototipo React y respaldos viejos (fuera de git)
publicar.sh            verifica y sincroniza site/
supabase-schema.sql    esquema de la nube opcional
```

## Antes de tocar el archivo

Tiene ~4,8 MB con líneas de megabytes de base64. **Nunca** grep/sed/awk con patrones
amplios: se cuelgan o hacen match dentro del base64. Busca con python3 limpiando primero:

```python
t = re.sub(r'data:[a-z0-9/+.-]+;base64,[A-Za-z0-9+/=]+', 'data:B', t)
```

Los dígitos en la clase son obligatorios, si no `data:font/woff2` no se limpia.

## Verificar

No hay tests y nunca los hubo. La red de seguridad es:

```bash
python3 herramientas/verificar.py coach-afc-v2.html --base=<copia-previa>
```

Usa el parser JavaScriptCore de macOS, así que los errores de sintaxis son reales.
Toma un snapshot antes de empezar y compara: lo que importa es **no introducir
hallazgos nuevos**. Chrome headless funciona para validar con clics (sirve con
`python3 -m http.server`; con `file://` el localStorage se bloquea).

## Publicar

```bash
./publicar.sh
```

Verifica, avisa si olvidaste subir el `APPREV` o el cache de `sw.js`, y copia la fuente
a `site/index.html`. Después: commit y push a `main` de `cabrihou/Cabricoach`, que
dispara Netlify.

## Señalar dónde está algo

`docs/MAPA.md` da un código corto a cada caja de la app (I4b, C3d, P2d…). Úsalos para
hablar sin ambigüedad y mantén el mapa al día cuando muevas o agregues secciones.

## Copy

Español de Colombia, cercano, sin regaños. **Nada de rayas largas (—)** en texto
visible. Comentarios de código en español sin tildes, explicando el porqué.
