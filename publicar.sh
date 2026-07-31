#!/bin/zsh
# Publica CabriCoach: verifica la fuente y la copia a site/.
#
# No hay build step: site/index.html es una copia byte a byte de
# coach-afc-v2.html. Este script existe para que las dos no se desincronicen
# y para que nadie olvide subir el cache del service worker (si no se sube,
# los telefonos siguen con la version vieja).
#
# Uso:  ./publicar.sh          verifica y sincroniza
#       ./publicar.sh --check  solo verifica, no copia
set -euo pipefail
cd "$(dirname "$0")"

FUENTE=coach-afc-v2.html
DESTINO=site/index.html
SOLO_CHEQUEO=${1:-}

rev=$(grep -o "const APPREV='REV [0-9]*'" "$FUENTE" | grep -o '[0-9]*')
cache=$(grep -o "cabritos-v[0-9]*" sw.js | head -1)
cache_site=$(grep -o "cabritos-v[0-9]*" site/sw.js | head -1)

echo "REV $rev · cache $cache"

if [ "$cache" != "$cache_site" ]; then
  echo "ERROR: sw.js dice $cache y site/sw.js dice $cache_site. Deben coincidir."
  exit 1
fi

rev_publicada=$(grep -o "const APPREV='REV [0-9]*'" "$DESTINO" 2>/dev/null | grep -o '[0-9]*' || echo 0)
if [ "$rev" = "$rev_publicada" ] && ! cmp -s "$FUENTE" "$DESTINO"; then
  echo "AVISO: cambiaste la app pero no subiste el REV (sigue en $rev)."
  echo "       Los telefonos con la version vieja no van a notar la diferencia."
fi

echo "verificando..."
python3 herramientas/verificar.py "$FUENTE" || { echo "la verificacion fallo, no publico"; exit 1; }

if [ "$SOLO_CHEQUEO" = "--check" ]; then
  echo "solo chequeo, no copie nada"
  exit 0
fi

cp "$FUENTE" "$DESTINO"
cmp -s "$FUENTE" "$DESTINO" && echo "listo: site/index.html sincronizado (REV $rev)"
echo "falta: git add -A && git commit && git push origin main"
