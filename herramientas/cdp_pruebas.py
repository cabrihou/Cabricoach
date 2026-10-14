import json, time, base64, urllib.request, websocket, os

SP = os.path.dirname(os.path.abspath(__file__))
URL = 'http://localhost:9140/coach-afc-v2.html'


class CDP:
    def __init__(self):
        try:
            wsurl = open(os.environ['CDP_TAB_FILE']).read().strip()
        except Exception:
            tabs = json.load(urllib.request.urlopen('http://localhost:9744/json'))
            wsurl = [t for t in tabs if t['type'] == 'page'][0]['webSocketDebuggerUrl']
        self.ws = websocket.create_connection(wsurl, timeout=120, suppress_origin=True)
        self.i = 0
        self.errors = []
        self.send('Runtime.enable')
        self.send('Page.enable')
        self.metrics()

    def send(self, method, params=None):
        self.i += 1
        mid = self.i
        self.ws.send(json.dumps({'id': mid, 'method': method, 'params': params or {}}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get('method') == 'Runtime.exceptionThrown':
                d = m['params']['exceptionDetails']
                self.errors.append((d.get('text'), (d.get('exception') or {}).get('description', '')[:300]))
            if m.get('id') == mid:
                return m

    def metrics(self, w=390, h=844, dpr=2):
        self.send('Emulation.setDeviceMetricsOverride', {'width': w, 'height': h, 'deviceScaleFactor': dpr, 'mobile': True})
        self.send('Emulation.setTouchEmulationEnabled', {'enabled': True, 'maxTouchPoints': 5})

    def ev(self, expr, await_promise=True):
        r = self.send('Runtime.evaluate', {'expression': expr, 'awaitPromise': await_promise, 'returnByValue': True})
        res = r.get('result', {})
        if 'exceptionDetails' in res:
            return {'__err__': res['exceptionDetails'].get('exception', {}).get('description', res['exceptionDetails'].get('text'))}
        return res.get('result', {}).get('value')

    def nav(self, q='', wait=8):
        self.ev("""(async()=>{try{const rs=await navigator.serviceWorker.getRegistrations();for(const r of rs) await r.unregister();for(const k of await caches.keys()) await caches.delete(k);}catch(e){} return 1})()""")
        self.send('Page.navigate', {'url': URL + '?t=' + str(int(time.time() * 1000)) + q})
        time.sleep(wait)

    def frames(self, n=5):
        for _ in range(n):
            self.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 10})

    def shot(self, path, full=False, clip=None):
        self.frames(4)
        p = {'format': 'png'}
        if full:
            h = self.ev("Math.ceil(Math.max(document.documentElement.scrollHeight, document.body.scrollHeight))")
            p['captureBeyondViewport'] = True
            p['clip'] = {'x': 0, 'y': 0, 'width': 390, 'height': h, 'scale': 1}
        if clip:
            p['clip'] = clip
        r = self.send('Page.captureScreenshot', p)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(r['result']['data']))
        return path
