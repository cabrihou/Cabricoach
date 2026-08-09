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

El hook de pre-commit (`.githooks/pre-commit`) hace el trabajo solo: al commitear la
fuente, verifica la app, avisa si el `APPREV` no subió, comprueba que los dos `sw.js`
tengan el mismo cache y sincroniza `site/index.html` dentro del mismo commit.

```bash
git add -A && git commit -m "REV N: ..." && git push origin main
```

El push a `main` de `cabrihou/Cabricoach` dispara Netlify. `./publicar.sh` sigue
existiendo para verificar y sincronizar a mano cuando quieras, sin commitear.

Si el hook no corre: `git config core.hooksPath .githooks` (lo hace `setup.sh`).

## Trabajar desde varios computadores

En un computador nuevo:

```bash
git clone https://github.com/cabrihou/Cabricoach.git
cd Cabricoach
zsh herramientas/setup.sh
```

`setup.sh` revisa python3, jsc y el CLI de claude, activa los hooks, valida las
credenciales de la nube contra Supabase y dice qué falta. Se puede correr cuantas
veces sea.

**La regla que evita el dolor**: `git pull --rebase` **antes** de tocar nada. La app es
un solo archivo de 4,8 MB; si dos computadores lo editan en paralelo, el conflicto es
irresoluble a mano y toca descartar el trabajo de uno. `setup.sh` avisa si estás atrás.

Lo que **no** viaja por git y hay que crear en cada máquina: `~/.config/cabritos.env`
(credenciales) y la programación del coach diario
(`zsh herramientas/coach-diario/instalar.sh`).

## Imágenes nuevas (Magnific)

Los nodos de imagen se crean **siempre** en el space "Character Model Sheet
Development", en la pestaña **Andrés** o **Cami** según el personaje: ahí está la
referencia conectada que mantiene la mascota consistente. Nunca en otro space ni en la
Página 1. Andrés = cabrito café/tan con muñequeras azules; Cami = cabrita crema con
amarillo y brillo dorado. En el prompt siempre: sin texto en la imagen y sin collar ni
campana. Generar cuesta créditos: solo cuando Andy lo pida.
Regla completa en [docs/DESIGN-STANDARDS.md](docs/DESIGN-STANDARDS.md) §5.

## Señalar dónde está algo

`docs/MAPA.md` da un código corto a cada caja de la app (I4b, C3d, P2d…). Úsalos para
hablar sin ambigüedad y mantén el mapa al día cuando muevas o agregues secciones.

## Copy

Español de Colombia, cercano, sin regaños. **Nada de rayas largas (—)** en texto
visible. Comentarios de código en español sin tildes, explicando el porqué.
