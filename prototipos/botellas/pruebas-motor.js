/* Pruebas del motor v2. Correr desde esta carpeta con:
   /System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc motor.js pruebas-motor.js
   (jsc tiene print y read, no console.log). Las del nucleo van aparte: motor.js pruebas-nucleo.js.
   1) Los 200 niveles del camino (niveles.json v3): estructura, solucion, rasgos, reglas de dificultad y estrenos.
   2) En vivo: niveles 201-205 y 14 retos del dia, en modo rapido: con solucion,
      deterministas y de menos de 2 s cada uno. */
(function () {
  const M = MOTOR;
  const t0all = Date.now();
  let fallos = 0;
  function falla(m) { fallos++; if (fallos <= 60) print('FALLA: ' + m); }
  function pad(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }

  // Todo lo que debe cumplir un nivel v2, venga del catalogo o del generador en vivo
  function revisar(nv, nombre, conMetricas) {
    const cap = nv.cap, u = nv.u || cap, B = nv.botellas, n = B.length;
    // la solucion gana, jugada por jugada con las reglas del nucleo (con llaves y candados)
    let E = { b: B, ab: 0 }, bien = true;
    for (let k = 0; k < nv.movs.length && bien; k++) {
      const m = nv.movs[k];
      if (!M.puedeVerter(E, m[0], m[1], nv)) { falla(nombre + ' jugada ' + k + ' no es valida: ' + m); bien = false; break; }
      E = M.verter(E, m[0], m[1], nv).estado;
    }
    if (bien && !M.ganado(E, nv)) falla(nombre + ' la solucion no gana');
    if (nv.meta !== nv.movs.length) falla(nombre + ' meta ' + nv.meta + ' distinta de movs ' + nv.movs.length);
    if (M.ganado(B, nv)) falla(nombre + ' ya viene ganado');
    // cada color con cap capas, colores 1..k sin huecos, tope de tamano
    const cuenta = {};
    let mono = false;
    B.forEach(function (b, i) {
      if (b.length > (nv.caps ? nv.caps[i] : cap)) falla(nombre + ' botella ' + i + ' con mas capas que su capacidad');
      if (M.completa(b, u)) mono = true;
      b.forEach(function (c) { cuenta[c] = (cuenta[c] || 0) + 1; });
    });
    if (mono) falla(nombre + ' tiene una botella completa de entrada');
    const cols = Object.keys(cuenta).map(Number);
    cols.forEach(function (c) { if (cuenta[c] !== u) falla(nombre + ' color ' + c + ' con ' + cuenta[c] + ' capas'); });
    if (cols.length > 12) falla(nombre + ' con ' + cols.length + ' colores');
    if (n > 15) falla(nombre + ' con ' + n + ' botellas');
    // cajas: contiguas al final, en orden, sin repetir botellas
    const enCaja = [];
    let k0 = n - nv.cajas.reduce(function (a, c) { return a + c.bots.length; }, 0), sig = k0;
    nv.cajas.forEach(function (cj, c) {
      if (cj.bots.length < 1 || cj.bots.length > 2) falla(nombre + ' caja ' + c + ' con ' + cj.bots.length + ' botellas');
      cj.bots.forEach(function (i) {
        if (i !== sig++) falla(nombre + ' las cajas no estan contiguas al final (caja ' + c + ', botella ' + i + ')');
        enCaja[i] = c;
      });
    });
    // candados: botella sin su color adentro, sin repetir botella, no dentro de una caja
    const candEn = [];
    nv.candados.forEach(function (cd, d) {
      if (B[cd.b].indexOf(cd.color) >= 0) falla(nombre + ' candado ' + d + ' con su color adentro');
      if (candEn[cd.b]) falla(nombre + ' dos candados en la botella ' + cd.b);
      candEn[cd.b] = true;
      if (enCaja[cd.b] !== undefined && B[cd.b].length) falla(nombre + ' candado con liquido dentro de una caja');
      if (!cuenta[cd.color]) falla(nombre + ' candado de un color que no existe');
    });
    // llaves: enterradas, no en botella cerrada (salvo la cadena), una por botella, una por caja, sin ciclos
    const llEn = [], cajaConLlave = [];
    nv.llaves.forEach(function (l, q) {
      if (!(B[l.b].length > l.k + 1)) falla(nombre + ' llave ' + q + ' no esta enterrada (len ' + B[l.b].length + ', k ' + l.k + ')');
      if (l.k < 0) falla(nombre + ' llave con k negativo');
      if (llEn[l.b]) falla(nombre + ' dos llaves en la botella ' + l.b);
      llEn[l.b] = true;
      if (cajaConLlave[l.caja]) falla(nombre + ' dos llaves para la caja ' + l.caja);
      cajaConLlave[l.caja] = true;
      if (candEn[l.b]) falla(nombre + ' llave en una botella con candado');
      const cj = enCaja[l.b];
      if (cj !== undefined) {
        if (cj === l.caja) falla(nombre + ' la llave de la caja ' + l.caja + ' esta en esa misma caja');
        else if (!(nv.cajas.length > 1 && l.caja === 1 && cj === 0)) falla(nombre + ' llave dentro de una caja sin ser cadena');
      }
    });
    if (nv.llaves.length !== nv.cajas.length) falla(nombre + ' llaves (' + nv.llaves.length + ') y cajas (' + nv.cajas.length + ') no coinciden');
    // v4: nada cerrado viene vacio; siempre 2 vacias libres
    B.forEach(function (b, i) {
      const cerr = enCaja[i] !== undefined || candEn[i];
      if (cerr && !b.length) falla(nombre + ' botella cerrada ' + i + ' viene vacia');
    });
    let libresVacias = 0;
    B.forEach(function (b, i) { if (!b.length && enCaja[i] === undefined && !candEn[i]) libresVacias++; });
    if (libresVacias < 2) falla(nombre + ' tiene ' + libresVacias + ' vacias libres');
    // colores nuevos: viven solo en lo cerrado, y hay nuevos si y solo si lo cerrado suma 8 capas o mas
    let capasCerr = 0;
    B.forEach(function (b, i) { if (enCaja[i] !== undefined || candEn[i]) capasCerr += b.length; });
    const nuev = nv.nuevos || [];
    if (!Array.isArray(nv.nuevos)) falla(nombre + ' sin campo nuevos');
    const enFuera = {};
    B.forEach(function (b, i) { if (enCaja[i] === undefined && !candEn[i]) b.forEach(function (c) { enFuera[c] = true; }); });
    nuev.forEach(function (c) { if (enFuera[c]) falla(nombre + ' el color nuevo ' + c + ' tiene capas afuera'); });
    nuev.forEach(function (c) { if (!cuenta[c]) falla(nombre + ' el color nuevo ' + c + ' no existe'); });
    if ((capasCerr >= 8) !== (nuev.length > 0)) falla(nombre + ' nuevos ' + nuev + ' con ' + capasCerr + ' capas cerradas');
    // todo color que solo vive en lo cerrado esta en nuevos
    Object.keys(cuenta).forEach(function (c) { if (!enFuera[c] && nuev.indexOf(Number(c)) < 0) falla(nombre + ' el color ' + c + ' solo esta en lo cerrado y no figura en nuevos'); });
    // botella gigante: capacidad 10, u = 4, entre 5 y 8 capas mezcladas, suelta, una sola
    if (nv.caps || nv.u) {
      if (!nv.caps || nv.caps.length !== n || nv.u !== cap) falla(nombre + ' gigante mal formada (caps/u)');
      else {
        const gs = [];
        nv.caps.forEach(function (c, i) { if (c !== cap) gs.push(i); });
        if (gs.length !== 1 || nv.caps[gs[0]] !== 10) falla(nombre + ' debe haber una sola botella de capacidad 10');
        else {
          const g = B[gs[0]], cnt = {};
          if (g.length < 5 || g.length > 8) falla(nombre + ' la gigante empieza con ' + g.length + ' capas');
          g.forEach(function (c) { cnt[c] = (cnt[c] || 0) + 1; });
          if (Object.keys(cnt).some(function (c) { return cnt[c] >= u; })) falla(nombre + ' la gigante trae un color entero');
          if (enCaja[gs[0]] !== undefined || candEn[gs[0]]) falla(nombre + ' la gigante esta cerrada');
          if (cap !== 4) falla(nombre + ' gigante con largas');
        }
      }
    }
    // rasgos y dificultad
    const rs = [];
    if (nv.llaves.length) rs.push('llave');
    if (nv.candados.length) rs.push('candado');
    if (nv.ocultas) rs.push('misterio');
    if (cap > 4) rs.push('largas');
    if (nv.caps) rs.push('gigante');
    if (rs.join() !== nv.rasgos.join()) falla(nombre + ' rasgos ' + nv.rasgos + ' distintos de lo que hay ' + rs);
    if (['facil', 'normal', 'dificil', 'muy'].indexOf(nv.dif) < 0) falla(nombre + ' dif invalida ' + nv.dif);
    if (nv.ocultas) {
      if (nv.ocultas.length !== n) falla(nombre + ' ocultas con otra forma');
      nv.ocultas.forEach(function (o, i) { if (o.length !== B[i].length) falla(nombre + ' ocultas[' + i + '] con otra forma'); });
    }
    if (conMetricas) {
      if (!(nv.bot >= 0 && nv.bot <= 1) || !(nv.atasco >= 0 && nv.atasco <= 1)) falla(nombre + ' metricas fuera de rango');
    }
    return cols.length;
  }

  /* ---------- 1) el catalogo ---------- */
  let doc;
  try { doc = JSON.parse(read('niveles.json')); } catch (e) { falla('no se pudo leer niveles.json: ' + e); doc = { camino: [] }; }
  const DIFS = ['facil', 'normal', 'dificil', 'muy'];
  const camino = doc.camino || [];
  if (doc.version !== 4) falla('version ' + doc.version + ' en vez de 4');
  if (camino.length !== 200) falla('el camino tiene ' + camino.length + ' niveles, no 200');
  const duro = function (d) { return d === 'dificil' || d === 'muy'; };
  const ESTR = { 4: 'candado', 7: 'cajaUna', 12: 'cajon', 20: 'mistLeve', 25: 'largas', 30: 'gigante', 35: 'mistTotal', 50: 'dosCajas', 80: 'cadena' };
  const dentroCaja = function (nv, b) { return nv.cajas.some(function (c) { return c.bots.indexOf(b) >= 0; }); };
  const total = function (nv) { return nv.ocultas && nv.ocultas.every(function (o, i) { return dentroCaja(nv, i) || o.length < 2 || o[o.length - 2]; }); };
  // el nivel mas bajo en el que ya se puede usar todo lo que trae este nivel (nada llega antes de su estreno)
  function minimoNivel(nv) {
    let m = 1;
    if (nv.candados.length) m = Math.max(m, 4);
    if (nv.cajas.length) m = Math.max(m, 7);
    if (nv.cajas.some(function (c) { return c.bots.length === 2; })) m = Math.max(m, 12);
    if (nv.ocultas) m = Math.max(m, total(nv) ? 35 : 20);
    if (nv.cap > 4) m = Math.max(m, 25);
    if (nv.caps) m = Math.max(m, 30);
    if (nv.cajas.length > 1) m = Math.max(m, 50);
    if (nv.llaves.some(function (l) { return dentroCaja(nv, l.b); })) m = Math.max(m, 80);
    return m;
  }
  const cuentaDif = { facil: 0, normal: 0, dificil: 0, muy: 0 };
  camino.forEach(function (nv, i) {
    const L = i + 1;
    if (nv.ruta !== 'camino' || nv.L !== L || nv.id !== 'camino-' + L) falla('id/L/ruta no correlativos en la posicion ' + L + ': ' + nv.id);
    if (nv.dif !== M.difDe(L)) falla('camino-' + L + ' dif ' + nv.dif + ' distinta de difDe ' + M.difDe(L));
    if (nv.dif !== M.nivelParams(L).dif) falla('camino-' + L + ' nivelParams dice otra dif');
    cuentaDif[nv.dif]++;
    revisar(nv, nv.id, true);
    if (minimoNivel(nv) > L) falla(nv.id + ' usa una mecanica que se estrena en el nivel ' + minimoNivel(nv));
    if (L <= 3 && nv.dif !== 'facil') falla(nv.id + ' deberia ser facil');
    if (L > 1) {
      const prev = camino[i - 1].dif;
      if (duro(prev) && duro(nv.dif)) falla(nv.id + ': dos duros seguidos');
      if (prev === 'muy' && nv.dif !== 'facil') falla(nv.id + ': despues de Muy dificil debe venir Facil');
    }
    if (L > 13 && nv.dif === 'facil' && camino[i - 1].dif === 'facil' && camino[i - 2].dif === 'facil' && camino[i - 3].dif === 'facil') falla(nv.id + ': cuatro Faciles seguidos');
    if (ESTR[L]) {
      if (duro(nv.dif)) falla(nv.id + ': el estreno no puede ser dificil');
      const ok = { candado: nv.candados.length, cajaUna: nv.cajas.length === 1 && nv.cajas[0].bots.length === 1, cajon: nv.cajas.length === 1 && nv.cajas[0].bots.length === 2 && nv.nuevos.length > 0,
        mistLeve: nv.ocultas && !total(nv), largas: nv.cap > 4, gigante: !!nv.caps, mistTotal: total(nv), dosCajas: nv.cajas.length === 2,
        cadena: nv.cajas.length === 2 && nv.llaves.some(function (l) { return dentroCaja(nv, l.b); }) }[ESTR[L]];
      if (!ok) falla(nv.id + ': no trae la mecanica que estrena (' + ESTR[L] + ')');
    }
    if (ESTR[L + 1] && duro(nv.dif)) falla(nv.id + ': la vispera de un estreno no puede ser dificil');
  });
  DIFS.forEach(function (d) { if (!cuentaDif[d]) falla('ningun nivel ' + d); });
  const cuentas = { candado: 0, cajon: 0, nuevos: 0, gigante: 0 };
  camino.forEach(function (nv) {
    if (nv.candados.length) cuentas.candado++;
    if (nv.cajas.some(function (c) { return c.bots.length === 2; })) cuentas.cajon++;
    if (nv.nuevos.length) cuentas.nuevos++;
    if (nv.caps) cuentas.gigante++;
  });
  print('con candado ' + cuentas.candado + ', con cajon de 2 ' + cuentas.cajon + ', con colores nuevos ' + cuentas.nuevos + ', con gigante ' + cuentas.gigante);
  print('catalogo: ' + camino.length + ' niveles revisados; facil ' + cuentaDif.facil + ', normal ' + cuentaDif.normal + ', dificil ' + cuentaDif.dificil + ', muy ' + cuentaDif.muy);
  // meta promedio por dificultad dentro de cada tramo de 50: Facil < Normal < Dificil < Muy (donde haya)
  const promNormal = [];
  for (let a = 0; a < 200; a += 50) {
    const pr = {};
    DIFS.forEach(function (d) {
      const x = camino.slice(a, a + 50).filter(function (nv) { return nv.dif === d; });
      if (x.length) pr[d] = x.reduce(function (s, nv) { return s + nv.meta; }, 0) / x.length;
    });
    let ult = null;
    DIFS.forEach(function (d) {
      if (pr[d] === undefined) return;
      if (ult !== null && !(pr[d] > pr[ult])) falla('L' + (a + 1) + '-' + (a + 50) + ': meta promedio de ' + d + ' (' + pr[d].toFixed(1) + ') no supera a ' + ult + ' (' + pr[ult].toFixed(1) + ')');
      ult = d;
    });
    promNormal.push(pr.normal);
    print('  tramo L' + (a + 1) + '-' + (a + 50) + ': ' + DIFS.map(function (d) { return d + ' ' + (pr[d] === undefined ? '-' : pr[d].toFixed(1)); }).join(', '));
  }
  for (let q = 1; q < promNormal.length; q++) {
    if (promNormal[q] <= promNormal[q - 1]) falla('la meta promedio de los Normales no sube en el tramo ' + (q + 1));
    if (promNormal[q] / promNormal[q - 1] > 1.5) falla('la meta de los Normales salta mas de 50 % en el tramo ' + (q + 1));
  }

  /* ---------- 2) en vivo, modo rapido ---------- */
  const vivos = [];
  for (let L = 201; L <= 205; L++) vivos.push({ nombre: 'camino-' + L, p: M.nivelParams(L), seed: 'camino:' + L });
  const base = Date.UTC(2026, 9, 21);
  for (let d = 0; d < 14; d++) {
    const f = new Date(base + d * 86400000).toISOString().slice(0, 10);
    vivos.push({ nombre: 'dia-' + f, p: M.diaParams(f), seed: 'dia:' + f });
  }
  let maxms = 0, maxn = '';
  const filas = [];
  vivos.forEach(function (v) {
    const t0 = Date.now();
    const n1 = M.generar(v.p, v.seed, { modo: 'rapido' });
    const ms = Date.now() - t0;
    const n2 = M.generar(v.p, v.seed, { modo: 'rapido' });
    if (JSON.stringify(n1) !== JSON.stringify(n2)) falla(v.nombre + ' no es determinista');
    if (n1.id !== v.nombre) falla(v.nombre + ' id ' + n1.id);
    if (ms > 2000) falla(v.nombre + ' tardo ' + ms + ' ms (mas de 2 s)');
    const cols = revisar(n1, v.nombre, false);
    if (ms > maxms) { maxms = ms; maxn = v.nombre; }
    filas.push(pad(v.nombre, 18) + pad(cols, 4) + pad(n1.botellas.length, 4) + pad(n1.rasgos.join('+') || '-', 24) + pad(n1.meta, 5) + pad(n1.optimo ? 'opt' : 'no', 5) + ms + ' ms');
  });
  print('en vivo (modo rapido): nivel, colores, botellas, rasgos, meta, optimo, tiempo');
  filas.forEach(function (f) { print('  ' + f); });
  print('mayor tiempo en vivo: ' + maxms + ' ms (' + maxn + ')');

  // jugador de prueba: pista y vigilancia siguen funcionando con llaves y candados
  (function () {
    const nv = camino.filter(function (x) { return x.llaves.length; })[0];
    if (!nv) return;
    const pi = M.pista({ b: nv.botellas, ab: 0 }, nv, { tope: 40000 });
    if (!pi.mov) falla('pista del nivel ' + nv.id + ' sin jugada: ' + JSON.stringify(pi));
  })();

  const tot = Date.now() - t0all;
  if (tot > 180000) falla('tardo ' + tot + ' ms en total (mas de 3 minutos)');
  print('---');
  print('total: ' + tot + ' ms, fallos: ' + fallos);
  print(fallos === 0 ? 'TODO BIEN' : 'HAY FALLOS');
})();
