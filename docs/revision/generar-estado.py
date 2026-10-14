#!/usr/bin/env python3
"""Genera docs/revision/ESTADO.md: la foto en texto de la mesa de revision.

Uso (lo corre Claude en cada pasada):
  1. Exportar la mesa con la herramienta ArtifactData, action "list" con
     out_dir, de las colecciones notas, envios, secciones y pendientes, a una
     carpeta (por ejemplo <scratchpad>/mesa).
  2. python3 docs/revision/generar-estado.py <carpeta> > docs/revision/ESTADO.md

Solo texto: las fotos de las notas no se copian; se cuenta cuantas tiene.
"""
import json, glob, os, sys
from datetime import datetime, timezone, timedelta

URL = "https://claude.ai/artifact/8X9qiXVU8PWTPd84PWn5MV"
base = sys.argv[1]


def cargar(col):
    out = []
    for f in sorted(glob.glob(os.path.join(base, col, "*.json"))):
        d = json.load(open(f)); d = d.get("data", d); d["id"] = os.path.basename(f)[:-5]; out.append(d)
    return out


secciones = sorted(cargar("secciones"), key=lambda s: s.get("orden", 99))
notas = cargar("notas"); envios = cargar("envios"); pendientes = cargar("pendientes")
NOMBRE = {"borrador": "Borrador", "enviada": "Enviada", "en_trabajo": "En trabajo", "para_revisar": "Para revisar", "resuelta": "Resuelta", "descartada": "Descartada"}
ORDEN = ["para_revisar", "en_trabajo", "enviada", "borrador", "resuelta", "descartada"]
QUIEN = {"andy": "Andy", "claude": "Claude", "juntos": "Los dos"}
hoy = datetime.now(timezone(timedelta(hours=-5))).strftime("%Y-%m-%d %H:%M")


def celda(t):
    return " ".join(str(t or "").split()).replace("|", "/")


print("# Estado de la mesa de revisión de CabriCoach\n")
print(f"> Foto en texto de <{URL}>, generada el {hoy} (hora de Bogotá) con `generar-estado.py`. ")
print("> La mesa manda: este archivo es para tener el contexto desde cualquier máquina sin abrirla.\n")

abiertos = [p for p in pendientes if p.get("estado") != "hecho"]
if pendientes:
    print("## Pendientes\n\n| Quién | Prioridad | Pendiente | Origen |\n|---|---|---|---|")
    for p in sorted(abiertos, key=lambda p: (["andy", "juntos", "claude"].index(p.get("quien", "claude")) if p.get("quien") in QUIEN else 9, p.get("orden", 0))):
        print(f"| {QUIEN.get(p.get('quien'), p.get('quien'))} | {celda(p.get('prioridad'))} | {celda(p.get('titulo'))} | {celda(p.get('origen'))} |")
    hechos = [p for p in pendientes if p.get("estado") == "hecho"]
    if hechos:
        print(f"\nHechos: {len(hechos)} ({', '.join(celda(p.get('titulo')) for p in hechos)}).")
    print()

conteo = {k: sum(1 for n in notas if n.get("estado") == k) for k in ORDEN}
if any(conteo.values()):
    print("## Notas\n\n| Estado | Notas |\n|---|---|")
    for k in ORDEN:
        if conteo[k]: print(f"| {NOMBRE[k]} | {conteo[k]} |")
    print()
if envios:
    print("## Envíos\n\n| Enviado | Notas | Estado | Resumen |\n|---|---|---|---|")
    for e in sorted(envios, key=lambda e: e.get("creadoEn", ""), reverse=True):
        print(f"| {str(e.get('creadoEn',''))[:10]} | {len(e.get('notas') or [])} | {celda(NOMBRE.get(e.get('estado'), e.get('estado')))} | {celda(e.get('resumen'))} |")
    print()
for s in secciones:
    ns = [n for n in notas if n.get("seccion") == s["id"]]
    if not ns: continue
    ns.sort(key=lambda n: (ORDEN.index(n.get("estado")) if n.get("estado") in ORDEN else 9, n.get("creadoEn", "")))
    print(f"## {s.get('nombre', s['id'])}\n")
    print("| Estado | Pedido de Andy | Respuesta de Claude |\n|---|---|---|")
    for n in ns:
        pedido = celda(n.get("texto")) or "(solo foto)"
        extras = []
        if n.get("imagenes"): extras.append(f"{len(n['imagenes'])} foto(s)")
        if n.get("capturaId"): extras.append("marca sobre captura")
        if n.get("parte"): extras.append("parte " + celda(n["parte"]))
        if n.get("ancla"): extras.append("responde a: " + celda(n["ancla"].get("cita"))[:120])
        if extras: pedido += " _(" + "; ".join(extras) + ")_"
        turnos = [x for x in (n.get("hilo") or []) if x.get("quien") == "andy"]
        if turnos: pedido += " **Última respuesta de Andy:** " + (celda(turnos[-1].get("texto")) or "(solo foto)")
        print(f"| {NOMBRE.get(n.get('estado'), n.get('estado'))} | {pedido} | {celda(n.get('respuesta'))} |")
    print()
