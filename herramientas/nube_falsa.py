"""Nube falsa que imita la tabla kv de Supabase (GET y upsert POST) para probar la
sincronizacion sin tocar la nube real. /__off la deja respondiendo 503 (sin señal),
/__on la vuelve a prender, /__dump devuelve lo guardado y /__set siembra una fila."""
import json, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

DATA = {}   # (house, uid, k) -> v
ESTADO = {'on': True, 'posts': []}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'apikey, authorization, content-type, prefer')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    def responder(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.cors(); self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == '/__off': ESTADO['on'] = False; return self.responder(200, {'on': False})
        if u.path == '/__on': ESTADO['on'] = True; return self.responder(200, {'on': True})
        if u.path == '/__dump': return self.responder(200, {'filas': [{'house': h, 'uid': ui, 'k': k, 'v': v} for (h, ui, k), v in DATA.items()], 'posts': ESTADO['posts']})
        if not ESTADO['on']: return self.responder(503, {'error': 'sin señal'})
        q = parse_qs(u.query); house = (q.get('house', ['eq.'])[0])[3:]
        return self.responder(200, [{'uid': ui, 'k': k, 'v': v} for (h, ui, k), v in DATA.items() if h == house])
    def do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get('Content-Length') or 0); body = json.loads(self.rfile.read(n) or b'[]')
        if u.path == '/__set':
            for r in body: DATA[(r['house'], r['uid'], r['k'])] = r['v']
            return self.responder(200, {'ok': True})
        if not ESTADO['on']: return self.responder(503, {'error': 'sin señal'})
        for r in body:
            DATA[(r['house'], r['uid'], r['k'])] = r['v']; ESTADO['posts'].append(r['uid'] + '|' + r['k'])
        return self.responder(201, [])

ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 9150), H).serve_forever()
