#!/usr/bin/env python3
"""
Verificador estatico de coach-afc-v2.html.

No hay build step ni node en este proyecto, asi que esto es la red de seguridad:
revisa que el HTML de una sola pagina siga siendo coherente consigo mismo.

Uso:  python3 verificar.py [archivo]
Sale con codigo 1 si hay algun fallo.
"""
import re
import sys
import pathlib

ARCHIVO = sys.argv[1] if len(sys.argv) > 1 else "coach-afc-v2.html"

# Las imagenes van embebidas como data-URI base64 en lineas larguisimas.
# Base64 contiene cualquier letra, asi que hace saltar cualquier regex ingenuo.
# Las quitamos antes de analizar nada.
DATA_URI = re.compile(r"data:[a-z0-9/+.-]+;base64,[A-Za-z0-9+/=]+")  # ojo: los digitos importan (woff2)

fallos = []
avisos = []


def falla(cat, msg):
    fallos.append((cat, msg))


def avisa(cat, msg):
    avisos.append((cat, msg))


def cargar(ruta):
    txt = pathlib.Path(ruta).read_text(encoding="utf-8")
    return txt, DATA_URI.sub("data:__BLOB__", txt)


def bloque_script(limpio):
    """Devuelve el contenido del <script> principal (el mas grande)."""
    trozos = re.findall(r"<script[^>]*>(.*?)</script>", limpio, re.S)
    if not trozos:
        falla("script", "no se encontro ningun bloque <script>")
        return ""
    return max(trozos, key=len)


def _es_regex(fuera):
    """
    Heuristica estandar para decidir si un '/' abre un literal regex o es
    division: mira el ultimo caracter significativo emitido. Tras un valor
    (identificador, numero, ')' o ']') un '/' es division; en cualquier otro
    contexto abre regex.
    """
    for ch in reversed(fuera):
        if ch.isspace():
            continue
        if ch.isalnum() or ch in "_$)]":
            # 'return /re/' y 'typeof /re/' son regex pese a terminar en letra.
            cola = "".join(fuera[-12:])
            return bool(re.search(r"\b(return|typeof|case|in|of|new|delete|void|instanceof)\s*$", cola))
        return True
    return True


def sin_comentarios_ni_texto(js):
    """
    Quita comentarios, cadenas, regex y template literals para poder contar
    delimitadores sin que los caracteres dentro de texto cuenten.
    """
    fuera = []
    i, n = 0, len(js)
    while i < n:
        c = js[i]
        if c == "/" and i + 1 < n and js[i + 1] == "/":
            i = js.find("\n", i)
            if i == -1:
                break
        elif c == "/" and i + 1 < n and js[i + 1] == "*":
            j = js.find("*/", i + 2)
            i = n if j == -1 else j + 2
        elif c == "/" and _es_regex(fuera):
            # literal regex: saltarlo entero, respetando \/ y clases [ ... /]
            i += 1
            clase = False
            while i < n:
                if js[i] == "\\":
                    i += 2
                    continue
                if js[i] == "[":
                    clase = True
                elif js[i] == "]":
                    clase = False
                elif js[i] == "/" and not clase:
                    i += 1
                    break
                elif js[i] == "\n":
                    break
                i += 1
            while i < n and js[i].isalpha():  # banderas gimsuy
                i += 1
        elif c in "\"'":
            q = c
            i += 1
            while i < n and js[i] != q:
                i += 2 if js[i] == "\\" else 1
            i += 1
        elif c == "`":
            # Los template literals pueden anidar ${ ... } con mas backticks
            # dentro. Los recorremos conservando solo los delimitadores de las
            # interpolaciones, que si cuentan para el balance.
            i += 1
            prof = 0
            while i < n:
                if js[i] == "\\":
                    i += 2
                    continue
                if js[i] == "`" and prof == 0:
                    i += 1
                    break
                if js[i] == "$" and i + 1 < n and js[i + 1] == "{":
                    prof += 1
                    fuera.append("{")
                    i += 2
                    continue
                if prof > 0 and js[i] == "}":
                    prof -= 1
                    fuera.append("}")
                    i += 1
                    continue
                if prof > 0:
                    fuera.append(js[i])
                i += 1
        else:
            fuera.append(c)
            i += 1
    return "".join(fuera)


JSC = pathlib.Path(
    "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"
)


def revisar_sintaxis(js):
    """
    Sintaxis de verdad, con el parser de JavaScriptCore que trae macOS.
    Se usa new Function(src): parsea el codigo entero sin ejecutarlo, asi que
    no hace falta DOM ni nada del navegador.
    """
    if not JSC.exists():
        avisa("sintaxis", "jsc no disponible; solo se reviso el balance aproximado")
        return revisar_balance(js)
    import subprocess
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as fh:
        fh.write(js)
        tmp = fh.name
    try:
        r = subprocess.run(
            [str(JSC), "-e",
             f"try{{ new Function(readFile({tmp!r})); print('OK'); }}"
             f"catch(e){{ print('ERR '+e); }}"],
            capture_output=True, text=True, timeout=120)
        out = (r.stdout or "").strip()
        if not out.startswith("OK"):
            falla("sintaxis", out.replace("ERR ", "") or (r.stderr or "").strip()[:200])
    except Exception as e:  # noqa: BLE001
        avisa("sintaxis", f"no pude correr jsc ({e}); uso el balance aproximado")
        revisar_balance(js)
    finally:
        try:
            pathlib.Path(tmp).unlink()
        except OSError:
            pass


def revisar_balance(js):
    """
    Respaldo si no hay jsc. Sin un parser de verdad esto no es exacto
    (regex vs division sigue siendo ambiguo), asi que va como AVISO.
    """
    codigo = sin_comentarios_ni_texto(js)
    pares = {")": "(", "]": "[", "}": "{"}
    pila = []
    for ch in codigo:
        if ch in "([{":
            pila.append(ch)
        elif ch in pares:
            if not pila:
                avisa("balance", f"cierre '{ch}' sin apertura")
                return
            if pila[-1] != pares[ch]:
                avisa("balance", f"cierre '{ch}' no coincide con '{pila[-1]}'")
                return
            pila.pop()
    if pila:
        avisa("balance", f"quedaron {len(pila)} delimitadores sin cerrar: {''.join(pila[-8:])}")


def revisar_acciones(limpio, js):
    """Todo data-a="X" debe tener un handler ACTIONS.X."""
    m = re.search(r"const ACTIONS\s*=\s*\{", js)
    if not m:
        falla("acciones", "no encontre el objeto ACTIONS")
        return
    # Nombres declarados en el primer nivel del objeto ACTIONS.
    cuerpo = js[m.end():]
    prof = 0
    declaradas = set()
    for linea in cuerpo.splitlines():
        if prof == 0:
            d = re.match(r"\s*([A-Za-z_$][\w$]*)\s*(?:\(|:)", linea)
            if d:
                declaradas.add(d.group(1))
        prof += linea.count("{") + linea.count("[") + linea.count("(")
        prof -= linea.count("}") + linea.count("]") + linea.count(")")
        if prof < 0:
            break

    usadas = set(re.findall(r'data-a="([A-Za-z_$][\w$]*)"', limpio))
    for a in sorted(usadas - declaradas):
        falla("acciones", f'data-a="{a}" no tiene handler en ACTIONS')
    sin_uso = declaradas - usadas
    dinamicas = set(re.findall(r'data-a="\$\{([^}]*)\}', limpio))
    if sin_uso and not dinamicas:
        for a in sorted(sin_uso):
            avisa("acciones", f"ACTIONS.{a} declarada pero sin data-a que la invoque")
    return declaradas, usadas


def revisar_iconos(limpio, js):
    m = re.search(r"const ICONS\s*=\s*\{(.*?)\n\}", js, re.S)
    if not m:
        falla("iconos", "no encontre el objeto ICONS")
        return
    disponibles = set(re.findall(r"^\s*([A-Za-z_$][\w$]*)\s*:", m.group(1), re.M))
    usados = set(re.findall(r"\bic\(\s*'([^']+)'", limpio))
    for i in sorted(usados - disponibles):
        falla("iconos", f"ic('{i}') no existe en ICONS")


def revisar_grid(limpio):
    """
    Las filas .settbl deben declarar tantas columnas como celdas se renderizan.
    Es exactamente el error que rompio la tabla de series antes.
    """
    m = re.search(r"\.settbl\{[^}]*grid-template-columns:([^;}]+)", limpio)
    if not m:
        avisa("grid", "no encontre grid-template-columns de .settbl")
        return
    cols = len(m.group(1).split())
    filas = re.findall(r'<div class="settbl[^"]*">(.*?)</div>\s*(?:\$\{|`)', limpio, re.S)
    for f in filas[:4]:
        celdas = len(re.findall(r"<(span|input|button)\b", f))
        if celdas and celdas != cols:
            falla("grid", f".settbl declara {cols} columnas pero una fila renderiza {celdas} celdas")


def revisar_mayusculas(limpio):
    """Texto visible en mayuscula sostenida (>=3 palabras o >=12 letras)."""
    hallazgos = []
    for m in re.finditer(r">([^<>{}]{6,})<", limpio):
        t = m.group(1).strip()
        letras = [c for c in t if c.isalpha()]
        if len(letras) >= 12 and all(c.isupper() for c in letras) and " " in t:
            hallazgos.append(t)
    for t in sorted(set(hallazgos))[:40]:
        avisa("mayusculas", f"texto en mayuscula sostenida: {t[:60]}")
    # Ojo: buscar el selector con ([^{}]+) antes de la llave provoca
    # backtracking catastrofico sobre 4 MB. Se recorren las reglas de una vez.
    for m in re.finditer(r"\{[^{}]*text-transform:\s*uppercase", limpio):
        ini = limpio.rfind("}", 0, m.start())
        sel = limpio[ini + 1:m.start()].strip().splitlines()
        if sel:
            avisa("mayusculas", f"CSS uppercase en: {sel[-1][:60]}")


def revisar_accesibilidad(limpio):
    """Botones solo-icono sin nombre accesible."""
    sin_nombre = 0
    for m in re.finditer(r"<button\b([^>]*)>(.*?)</button>", limpio, re.S):
        attrs, cont = m.group(1), m.group(2)
        if "aria-label" in attrs or "title=" in attrs:
            continue
        texto = re.sub(r"\$\{[^}]*\}", "", cont)
        texto = re.sub(r"<[^>]+>", "", texto).strip()
        if not texto:
            sin_nombre += 1
    if sin_nombre:
        avisa("a11y", f"{sin_nombre} botones sin texto ni aria-label")


def analizar(ruta):
    """Corre todas las revisiones sobre un archivo y devuelve (fallos, avisos)."""
    global fallos, avisos
    fallos, avisos = [], []
    crudo, limpio = cargar(ruta)
    js = bloque_script(limpio)
    revisar_sintaxis(js)
    revisar_acciones(limpio, js)
    revisar_iconos(limpio, js)
    revisar_grid(limpio)
    revisar_mayusculas(limpio)
    revisar_accesibilidad(limpio)
    return list(fallos), list(avisos), crudo, js


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = None
    for a in sys.argv[1:]:
        if a.startswith("--base="):
            base = a.split("=", 1)[1]

    ruta = pathlib.Path(args[0] if args else "coach-afc-v2.html")
    if not ruta.exists():
        print(f"no existe {ruta}")
        return 1

    f_now, a_now, crudo, js = analizar(ruta)
    print(f"archivo: {ruta}  ({len(crudo)/1024:.0f} KB, {crudo.count(chr(10))+1} lineas)")
    print(f"js analizado: {len(js)/1024:.0f} KB")

    if base:
        # Lo que importa no es el numero absoluto de hallazgos (esta app arrastra
        # varios de antes) sino no introducir ninguno nuevo.
        bp = pathlib.Path(base)
        if not bp.exists():
            print(f"baseline no existe: {bp}")
            return 1
        f_base, a_base, _, _ = analizar(bp)
        print(f"baseline: {bp.name}\n")
        nuevos_f = [x for x in f_now if x not in f_base]
        nuevos_a = [x for x in a_now if x not in a_base]
        resueltos = [x for x in f_base if x not in f_now]
        for cat, m in resueltos:
            print(f"  RESUELTO  [{cat}] {m}")
        for cat, m in nuevos_a:
            print(f"  AVISO NUEVO [{cat}] {m}")
        for cat, m in nuevos_f:
            print(f"  FALLO NUEVO [{cat}] {m}")
        print()
        print(f"heredados: {len(f_now)-len(nuevos_f)} fallos, {len(a_now)-len(nuevos_a)} avisos")
        if nuevos_f:
            print(f"REGRESION: {len(nuevos_f)} fallos nuevos")
            return 1
        print("sin regresiones")
        return 0

    print()
    if avisos:
        print(f"AVISOS ({len(a_now)}):")
        for cat, m in a_now:
            print(f"  [{cat}] {m}")
        print()
    if f_now:
        print(f"FALLOS ({len(f_now)}):")
        for cat, m in f_now:
            print(f"  [{cat}] {m}")
        return 1
    print("sin fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
