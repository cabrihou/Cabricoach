#!/bin/zsh
# Programa el coach diario en ESTE computador.
# Genera el plist con la ruta real de la carpeta, asi que funciona aunque
# muevas el proyecto o lo clones en otro Mac.
#
#   zsh instalar.sh                 una vez al dia, 9 pm (por defecto)
#   zsh instalar.sh --cada 4        cada 4 horas (0,4,8,12,16,20)
#   zsh instalar.sh --horas 8,13,21 solo a esas horas
#   zsh instalar.sh --quitar        desinstala
#
# launchd no tiene "cada N horas": se le pasa la lista de horas exactas.
# Si el Mac esta dormido a esa hora, la corrida se dispara al despertar.
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

HORAS=(21)
case "${1:-}" in
  --cada)
    paso=${2:-4}
    [[ "$paso" =~ ^[0-9]+$ ]] && [ "$paso" -ge 1 ] && [ "$paso" -le 24 ] || { echo "--cada necesita un numero de 1 a 24"; exit 1; }
    HORAS=(); h=0
    while [ $h -lt 24 ]; do HORAS+=($h); h=$((h+paso)); done ;;
  --horas)
    [ -n "${2:-}" ] || { echo "--horas necesita una lista, por ejemplo 8,13,21"; exit 1; }
    HORAS=(${(s:,:)2}) ;;
esac

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

bloques=""
for h in $HORAS; do
  bloques+="    <dict><key>Hour</key><integer>$h</integer><key>Minute</key><integer>0</integer></dict>
"
done

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
  <array>
$bloques  </array>
  <key>StandardOutPath</key><string>/tmp/coach-diario.log</string>
  <key>StandardErrorPath</key><string>/tmp/coach-diario.err</string>
</dict>
</plist>
PLIST_FIN

plutil -lint "$PLIST" > /dev/null || { echo "el plist quedo mal formado"; exit 1; }
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "coach diario programado a las horas: ${HORAS[*]} (en punto)"
echo "  script: $SCRIPT"
echo "  logs:   /tmp/coach-diario.log  y  /tmp/coach-diario.err"
echo
echo "Probarlo ya:        zsh $SCRIPT"
echo "Ver si esta vivo:   launchctl list | grep cabritos"
echo "Cambiar horario:    zsh $0 --cada 4   |   zsh $0 --horas 8,13,21"
