/* Coach Cabritos · offline para el gimnasio sin señal */
const CACHE = 'cabritos-v171';
const CORE = ['./', 'index.html', 'manifest.webmanifest'];
/* Las imagenes de la interfaz salieron del HTML a archivos sueltos (bajo de 4,3 MB a
   1 MB). Como el gimnasio puede no tener señal, se precargan en segundo plano al
   instalar: si se dejaran solo bajo demanda, una pantalla que no hubieras abierto
   antes se veria sin sus imagenes al quedarte sin datos. Las fotos de ejercicios
   (assets/ej, 8 MB) NO se precargan: son muchas y solo se ven al abrir el catalogo. */
const UI_IMGS = ['assets/cab/pu_gruesa.jpg','assets/cab/pu_media.jpg','assets/cab/pu_delgada.jpg','assets/cab/pu_negativa.jpg','assets/cab/pu_libre.jpg','assets/cab/pu_celebra.jpg',
  'assets/cab/andBuff.png',
  'assets/cab/andLift.png',
  'assets/cab/apple-touch-icon.png',
  'assets/cab/arroz.png',
  'assets/cab/avA.png',
  'assets/cab/avC.png',
  'assets/cab/banCuadC.jpg',
  'assets/cab/banGluC.jpg',
  'assets/cab/banLegsA.jpg',
  'assets/cab/banPullA.jpg',
  'assets/cab/banPushA.jpg',
  'assets/cab/banUpC.jpg',
  'assets/cab/biblia.jpg',
  'assets/cab/camCheck.png',
  'assets/cab/camLift.png',
  'assets/cab/celebA.png',
  'assets/cab/celebC.png',
  'assets/cab/cerdo.png',
  'assets/cab/comerMA.png',
  'assets/cab/comerMC.png',
  'assets/cab/comerNA.png',
  'assets/cab/comerNC.png',
  'assets/cab/comerTA.png',
  'assets/cab/comerTC.png',
  'assets/cab/curiosa.jpg',
  'assets/cab/cycFoli.png',
  'assets/cab/cycLute.png',
  'assets/cab/cycMens.png',
  'assets/cab/cycOvul.png',
  'assets/cab/dormidoA.png',
  'assets/cab/dormidoC.png',
  'assets/cab/faceA.png',
  'assets/cab/faceC.png',
  'assets/cab/fic_cena.png',
  'assets/cab/fic_cerdo.png',
  'assets/cab/fic_huevo.png',
  'assets/cab/fic_pescado.png',
  'assets/cab/fic_pollo.png',
  'assets/cab/fic_res.png',
  'assets/cab/fic_snack.png',
  'assets/cab/fotoShot.jpg',
  'assets/cab/huevo.png',
  'assets/cab/icAcomp.png',
  'assets/cab/icBeb.png',
  'assets/cab/icDes.png',
  'assets/cab/icPlato.png',
  'assets/cab/icProt.png',
  'assets/cab/icRec.png',
  'assets/cab/icSnack.png',
  'assets/cab/lectora.png',
  'assets/cab/medidasA.png',
  'assets/cab/medidasC.png',
  'assets/cab/movA.png',
  'assets/cab/nutriA.png',
  'assets/cab/nutriC.png',
  'assets/cab/pescado.png',
  'assets/cab/ph_ph-a-checkin.jpg',
  'assets/cab/ph_ph-a-legs.jpg',
  'assets/cab/ph_ph-a-pasos.jpg',
  'assets/cab/ph_ph-a-plan.jpg',
  'assets/cab/ph_ph-a-pull.jpg',
  'assets/cab/ph_ph-a-push.jpg',
  'assets/cab/ph_ph-c-cardio.jpg',
  'assets/cab/ph_ph-c-checkin.jpg',
  'assets/cab/ph_ph-c-lower.jpg',
  'assets/cab/ph_ph-c-pasos.jpg',
  'assets/cab/ph_ph-c-plan.jpg',
  'assets/cab/ph_ph-c-upper.jpg',
  'assets/cab/ph_ph-rest.jpg',
  'assets/cab/ph_ph-retos.jpg',
  'assets/cab/ph_ph-v-mercado.jpg',
  'assets/cab/ph_ph-v-recetas.jpg',
  'assets/cab/planA.png',
  'assets/cab/planC.png',
  'assets/cab/pollo.png',
  'assets/cab/rachaA.png',
  'assets/cab/rachaC.png',
  'assets/cab/reloj.jpg',
  'assets/cab/res.png',
  'assets/cab/restA.png',
  'assets/cab/stkAvion.png',
  'assets/cab/stkBallena.png',
  'assets/cab/stkCamion.png',
  'assets/cab/stkCarro.png',
  'assets/cab/stkElefante.png',
  'assets/cab/stkEstrella.png',
  'assets/cab/stkFlama.png',
  'assets/cab/stkMoto.png',
  'assets/cab/stkPasos.png',
  'assets/cab/tileCheckA.png',
  'assets/cab/tileCheckC.png',
  'assets/cab/tileFotoA.png',
  'assets/cab/tileFotoC.png',
  'assets/cab/troBronce.png',
  'assets/cab/troOro.png',
  'assets/cab/troPlata.png',
  'assets/cab/vacio.jpg',
  'assets/cab/vs.png',
  'assets/cab/vsIcon.png',
  'assets/cab/yogur.png'
];
/* el juego de botellas cambia sin cambiar de nombre: se precarga saltando la cache HTTP (reload)
   y se sirve red primero (ver fetch). La app lo pide con ?v=APPREV. */
const JUEGO = 'assets/botellas.html';
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(CORE).catch(()=>{}))
      /* el precache de imagenes no bloquea la instalacion: si falla una, la app
         igual queda usable y esa imagen se pedira a la red cuando toque */
      /* el catalogo de paquetes va en este lote resiliente (una falla no tumba el resto),
         no en CORE: alla addAll es todo-o-nada y por eso el JSON no entraba en dev */
      .then(() => caches.open(CACHE).then(c => Promise.allSettled(UI_IMGS.concat(['assets/paq/nutricion-co.json']).map(u => c.add(u)).concat([c.add(new Request(JUEGO, { cache:'reload' }))]))))
      .then(()=>self.skipWaiting())
  );
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  /* el juego (assets/botellas.html) se pide con fetch, no es navegacion; aun asi, nada bajo /assets/ cuenta como la app */
  const isPage = !new URL(req.url).pathname.includes('/assets/') && (req.mode === 'navigate' || req.url.endsWith('/index.html'));
  if (new URL(req.url).pathname.endsWith('/' + JUEGO)) {
    /* REV 227: el juego, red primero (espera maximo 4 s) y la copia guardada si no hay senal.
       Antes iba cache primero y el iPhone se quedaba con un juego viejo. Se guarda sin el ?v= para
       que cualquier version sirva de respaldo. */
    const red = fetch(req).then(res => {
      if (res && res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(JUEGO, copy)); }
      return res;
    });
    e.waitUntil(red.then(() => {}, () => {}));
    const guardada = () => caches.match(JUEGO, { ignoreSearch:true });
    e.respondWith(Promise.race([red.catch(() => null), new Promise(r => setTimeout(() => r(null), 4000))])
      .then(res => (res && res.ok) ? res : guardada().then(g => g || red)));
    return;
  }
  if (isPage) {
    /* la app: red primero (para recibir actualizaciones), caché si no hay señal.
       REV 223: con señal mala la red podia tardar un minuto en rendirse y la app se quedaba
       en negro. Ahora se espera la red maximo 3 s; si no llega, abre la version guardada y
       la descarga sigue en segundo plano para la proxima vez. Sin version guardada (primera
       vez) se espera la red como siempre. */
    const red = fetch(req).then(res => {
      if (res && res.ok) {
        const copy = res.clone(), copy2 = res.clone();
        caches.open(CACHE).then(c => { c.put(req, copy); c.put('index.html', copy2); });
      }
      return res;
    });
    e.waitUntil(red.then(() => {}, () => {}));
    e.respondWith(
      caches.match('index.html').then(guardada => {
        if (!guardada) return red.catch(() => caches.match(req));
        const espera = new Promise(r => setTimeout(() => r(null), 3000));
        return Promise.race([red.catch(() => null), espera]).then(res => res || guardada);
      })
    );
  } else {
    /* assets (videos, imagenes de interfaz y fotos de ejercicios): cache primero,
       no cambian de nombre. Lo que no se precargo entra aqui la primera vez que se pide. */
    e.respondWith(
      caches.match(req).then(hit => hit || fetch(req).then(res => {
        if (res && res.status === 200) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
        return res;
      }))
    );
  }
});
