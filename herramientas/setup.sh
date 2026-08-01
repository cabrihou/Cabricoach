#!/bin/zsh
# Deja este computador listo para trabajar en CabriCoach.
# Se puede correr las veces que sea: no pisa nada que ya este bien.
#
#   zsh herramientas/setup.sh
set -uo pipefail
cd "$(dirname "$0")/.."
RAIZ=$(pwd)
ok=0; falta=0

titulo(){ print -P "\n%F{cyan}$1%f"; }
si(){ print -P "  %F{green}ok%f  $1"; ok=$((ok+1)); }
no(){ print -P "  %F{yellow}--%f  $1"; falta=$((falta+1)); }

titulo "1. Herramientas necesarias"

if command -v python3 >/dev/null; then si "python3 $(python3 -V 2>&1 | cut -d' ' -f2)"
else no "falta python3 (instalalo desde python.org o con brew install python)"; fi

JSC=/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc
if [ -x "$JSC" ]; then si "jsc (parser de JavaScript para verificar.py)"
else no "no encontre jsc; verificar.py va a usar el chequeo aproximado"; fi

CLAUDE=$(command -v claude || ls -t ~/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude 2>/dev/null | head -1)
if [ -n "${CLAUDE:-}" ] && [ -x "$CLAUDE" ]; then si "CLI de claude en $CLAUDE"
else no "no encontre el CLI de claude (solo lo necesita el coach diario)"; fi

titulo "2. Credenciales de la nube"

ENV=~/.config/cabritos.env
if [ -f "$ENV" ]; then
  source "$ENV" 2>/dev/null || true
  if [[ "${SUPABASE_URL:-}" == https://*.supabase.co && "${SUPABASE_KEY:-}" == ey* && -n "${HOUSE:-}" && "${HOUSE:-}" != "tu-codigo-de-casa" ]]; then
    codigo=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 \
      -H "apikey: $SUPABASE_KEY" -H "Authorization: Bearer $SUPABASE_KEY" \
      "$SUPABASE_URL/rest/v1/kv?house=eq.$HOUSE&select=uid&limit=1" 2>/dev/null)
    if [ "$codigo" = "200" ]; then si "cabritos.env valido y la nube responde"
    else no "cabritos.env existe pero la nube devolvio HTTP $codigo (revisa URL, key o que corriste supabase-schema.sql)"; fi
  else
    no "cabritos.env existe pero todavia tiene los valores de ejemplo"
  fi
else
  no "falta $ENV"
  print "      mkdir -p ~/.config && cp herramientas/cabritos.env.ejemplo ~/.config/cabritos.env && chmod 600 ~/.config/cabritos.env"
fi

titulo "3. Automatizacion de git"

if [ "$(git config core.hooksPath 2>/dev/null)" = ".githooks" ]; then
  si "hooks activos (site/ se sincroniza solo en cada commit)"
else
  git config core.hooksPath .githooks && si "hooks activados ahora"
fi
chmod +x .githooks/* publicar.sh herramientas/*.sh 2>/dev/null

titulo "4. Coach diario (opcional)"

PLIST=~/Library/LaunchAgents/com.cabritos.coach.plist
if [ -f "$PLIST" ]; then si "coach diario programado a las 9 pm"
else
  no "coach diario sin programar"
  print "      zsh herramientas/coach-diario/instalar.sh"
fi

titulo "5. Estado del repositorio"
git fetch --quiet origin 2>/dev/null || true
adelante=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo 0)
atras=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo 0)
[ "$atras" != "0" ] && no "estas $atras commits ATRAS: corre 'git pull --rebase' ANTES de editar" || si "al dia con origin/main"
[ "$adelante" != "0" ] && no "tienes $adelante commits sin publicar: 'git push origin main'"

print -P "\n%F{cyan}Resumen%f  $ok listo, $falta por hacer"
[ "$falta" = "0" ] && print "Todo en orden." || print "Sigue las lineas marcadas con -- de arriba."
