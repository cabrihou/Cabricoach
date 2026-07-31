#!/bin/zsh
# Coach diario de Cabritos.
# Lee el dia de hoy desde Supabase (la misma nube que sincroniza la app),
# se lo pasa a `claude -p` para una evaluacion corta, y guarda el resultado
# de vuelta en la nube para que la app lo muestre. Tambien notifica en el Mac.
#
# Requisitos:
#   1. Archivo ~/.config/cabritos.env con:
#        SUPABASE_URL=https://xxxx.supabase.co
#        SUPABASE_KEY=<anon key>
#        HOUSE=<codigo de casa de la app>
#   2. Claude Code instalado y con sesion iniciada (el comando `claude`).
#   3. Programarlo con launchd (ver coach-diario.plist) o cron.
set -euo pipefail
source ~/.config/cabritos.env

# Encuentra el CLI de Claude: instalado suelto o embebido en la extension de VSCode
CLAUDE=$(command -v claude || true)
if [ -z "$CLAUDE" ]; then
  CLAUDE=$(ls -t ~/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude 2>/dev/null | head -1)
fi
[ -x "$CLAUDE" ] || { echo "no encontre el CLI de claude"; exit 1; }

HOY=$(date +%Y-%m-%d)
API="$SUPABASE_URL/rest/v1/kv"
HDR=(-H "apikey: $SUPABASE_KEY" -H "Authorization: Bearer $SUPABASE_KEY")

# Trae las claves del dia de los dos usuarios en una sola pasada
DATA=$(curl -s "${HDR[@]}" \
  "$API?house=eq.$HOUSE&k=in.(weights,steps,water,meals,nlog,sessions,cfg)&select=uid,k,v")

if [ -z "$DATA" ] || [ "$DATA" = "[]" ]; then
  echo "sin datos en la nube (revisa URL/key/casa)"; exit 1
fi

# Compacta: solo lo de hoy y los ultimos 7 dias de peso, para no gastar contexto
export DATA
RESUMEN=$(python3 - "$HOY" <<'PY'
import json,sys,os
hoy=sys.argv[1]
data=json.loads(os.environ['DATA'])
out={}
for fila in data:
    uid,k,v=fila['uid'],fila['k'],fila['v']
    u=out.setdefault(uid,{})
    if k=='weights' and isinstance(v,list): u['pesos_7d']=v[-7:]
    elif k in ('steps','water') and isinstance(v,dict): u[k+'_hoy']=v.get(hoy,0)
    elif k=='meals' and isinstance(v,dict): u['comidas_hoy']=v.get(hoy,{})
    elif k=='nlog' and isinstance(v,dict):
        logs=v.get(hoy,[])
        u['prote_hoy']=sum(i.get('pg',0) for e in logs for i in e.get('items',[]))
        u['kcal_hoy']=sum(i.get('kc',0) for e in logs for i in e.get('items',[]))
    elif k=='sessions' and isinstance(v,list): u['entreno_hoy']=any(s.get('d')==hoy for s in v)
    elif k=='cfg' and isinstance(v,dict): u['metas']={x:v.get(x) for x in ('stepGoal','waterGoal')}
print(json.dumps(out,ensure_ascii=False))
PY
)

EVAL=$("$CLAUDE" -p "Eres el coach de la app Cabritos. Datos de hoy ($HOY) de Andres (corte, meta 195 g proteina, usa retatrutida: el riesgo es comer de menos) y Cami (recomposicion, meta 115 g). Evalua el dia en maximo 4 frases en espanol, tono cercano, sin reganos: que se cumplio, que falta y UNA sugerencia concreta para manana. Sin markdown. Datos: $RESUMEN")

# Publica el resultado en la nube: la app lo puede leer del uid 'coach'
BODY=$(python3 -c "import json,sys,datetime;print(json.dumps({'house':'$HOUSE','uid':'coach','k':'daily','v':{'d':'$HOY','txt':sys.argv[1]}}))" "$EVAL")
curl -s -X POST "${HDR[@]}" -H "Content-Type: application/json" -H "Prefer: resolution=merge-duplicates" \
  -d "$BODY" "$API" > /dev/null

# Aviso local en el Mac
osascript -e "display notification \"$(echo "$EVAL" | head -c 200)\" with title \"Coach Cabritos · $HOY\"" || true
echo "$EVAL"
