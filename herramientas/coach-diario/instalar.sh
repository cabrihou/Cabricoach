#!/bin/zsh
# Programa el coach diario a las 9 pm en ESTE computador.
# Genera el plist con la ruta real de la carpeta, asi que funciona aunque
# muevas el proyecto o lo clones en otro Mac.
#
#   zsh herramientas/coach-diario/instalar.sh          instala
#   zsh herramientas/coach-diario/instalar.sh --quitar desinstala
set -euo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
SCRIPT="$AQUI/coach-diario.sh"
PLIST=~/Library/LaunchAgents/com.cabritos.coach.plist

if [ "${1:-}" = "--quitar" ]; then
  launchctl unload "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
  echo "coach diario desinstalado"
  exit 0
fi

if [ ! -f ~/.config/cabritos.env ]; then
  echo "Falta ~/.config/cabritos.env. Crealo primero:"
  echo "  mkdir -p ~/.config"
  echo "  cp herramientas/cabritos.env.ejemplo ~/.config/cabritos.env"
  echo "  chmod 600 ~/.config/cabritos.env"
  echo "  (y reemplaza los tres valores con los de tu app)"
  exit 1
fi

chmod +x "$SCRIPT"
mkdir -p ~/Library/LaunchAgents

cat > "$PLIST" <<PLIST_FIN
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.cabritos.coach</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/zsh</string>
    <string>$SCRIPT</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>21</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/tmp/coach-diario.log</string>
  <key>StandardErrorPath</key><string>/tmp/coach-diario.err</string>
</dict>
</plist>
PLIST_FIN

launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "coach diario programado a las 9 pm"
echo "  script: $SCRIPT"
echo "  logs:   /tmp/coach-diario.log  y  /tmp/coach-diario.err"
echo
echo "Para probarlo ya mismo sin esperar:  zsh $SCRIPT"
