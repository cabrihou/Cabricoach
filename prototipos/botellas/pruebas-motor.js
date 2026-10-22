/* Pruebas del motor (v5: cinco grados y receta). Correr desde esta carpeta con:
   /System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc motor.js pruebas-motor.js
   (jsc tiene print y read, no console.log). Las del nucleo van aparte: motor.js pruebas-nucleo.js.
   1) Los 200 niveles del camino (niveles.json v5): estructura, solucion, rasgos, reglas del sorteo del grado
      (duros, respiros, estrenos, Extra desde L36), meta de reparto, franjas de la receta y pruebas por grado.
   2) En vivo: niveles 201-230 y 14 retos del dia, en modo rapido: con solucion, deterministas y con tiempo
      (Facil, Normal y Dificil en 2 s o menos; Muy y Extra en 5 s o menos). */
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
    if (['facil', 'normal', 'dificil', 'muy', 'extra'].indexOf(nv.dif) < 0) falla(nombre + ' dif invalida ' + nv.dif);
    if (nv.ocultas) {
      if (nv.ocultas.length !== n) falla(nombre + ' ocultas con otra forma');
      nv.ocultas.forEach(function (o, i) { if (o.length !== B[i].length) falla(nombre + ' ocultas[' + i + '] con otra forma'); });
    }
    if (conMetricas) {
      if (!(nv.bot >= 0 && nv.bot <= 1) || !(nv.atasco >= 0 && nv.atasco <= 1)) falla(nombre + ' metricas fuera de rango');
    }
    // Extra: misterio total, con candado y con caja (todas las pruebas que hay desde L36)
    if (nv.dif === 'extra') {
      if (!nv.ocultas) falla(nombre + ' Extra sin misterio');
      else if (!total(nv)) falla(nombre + ' Extra con misterio leve');
      if (!nv.candados.length || !nv.cajas.length) falla(nombre + ' Extra sin candado o sin caja');
    }
    return cols.length;
  }

  /* ---------- 1) el catalogo ---------- */
  let doc;
  try { doc = JSON.parse(read('niveles.json')); } catch (e) { falla('no se pudo leer niveles.json: ' + e); doc = { camino: [] }; }
  const DIFS = ['facil', 'normal', 'dificil', 'muy', 'extra'];
  const camino = doc.camino || [];
  if (doc.version !== 5) falla('version ' + doc.version + ' en vez de 5');
  if (camino.length !== 200) falla('el camino tiene ' + camino.length + ' niveles, no 200');
  const duro = function (d) { return d === 'dificil' || d === 'muy' || d === 'extra'; };
  // la receta (tabla de motor.js, copiada aqui para comprobar que el catalogo la cumple)
  const PRUEBAS = { facil: [0, 1], normal: [0, 1], dificil: [1, 2], muy: [2, 3], extra: [3, 3] };
  const FRANJA = { facil: [0.55, 1, 0], normal: [0.1, 0.599, 0], dificil: [0, 0.249, 0.3], muy: [0, 0.05, 0.5], extra: [0, 0, 0.65] };
  const enFranja = function (nv) { const f = FRANJA[nv.dif]; return nv.bot >= f[0] && nv.bot <= f[1] && nv.atasco >= f[2]; };
  let largasN = 0;
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
  const cuentaDif = { facil: 0, normal: 0, dificil: 0, muy: 0, extra: 0 };
  const franjaGrado = { facil: [0, 0], normal: [0, 0], dificil: [0, 0], muy: [0, 0], extra: [0, 0] }, fueraDeFranja = [];
  camino.forEach(function (nv, i) {
    const L = i + 1;
    if (nv.ruta !== 'camino' || nv.L !== L || nv.id !== 'camino-' + L) falla('id/L/ruta no correlativos en la posicion ' + L + ': ' + nv.id);
    if (nv.dif !== M.difDe(L)) falla('camino-' + L + ' dif ' + nv.dif + ' distinta de difDe ' + M.difDe(L));
    if (nv.dif !== M.nivelParams(L).dif) falla('camino-' + L + ' nivelParams dice otra dif');
    cuentaDif[nv.dif]++;
    const cols = revisar(nv, nv.id, true);
    // colores = los de la receta (etapa + desfase del grado, sin largas que los reducen)
    const par = M.nivelParams(L);
    if (nv.cap === 4 && cols !== par.n) falla(nv.id + ' tiene ' + cols + ' colores y la receta pide ' + par.n);
    if (par.n < 3 || par.n > 12) falla(nv.id + ' receta con ' + par.n + ' colores');
    // franja
    franjaGrado[nv.dif][0]++;
    if (enFranja(nv)) franjaGrado[nv.dif][1]++; else fueraDeFranja.push(L + ' ' + nv.dif + ' bot ' + nv.bot + ' atasco ' + nv.atasco);
    // pruebas del grado: candado, caja y misterio (no cuentan estrenos ni largas, que van solas)
    if (!ESTR[L] && nv.cap === 4) {
      const hay = (nv.candados.length ? 1 : 0) + (nv.cajas.length ? 1 : 0) + (nv.ocultas ? 1 : 0);
      const disp = (L >= 4 ? 1 : 0) + (L >= 7 ? 1 : 0) + (L >= 20 ? 1 : 0);
      const pr = PRUEBAS[nv.dif];
      if (hay > pr[1]) falla(nv.id + ' ' + nv.dif + ' con ' + hay + ' pruebas (maximo ' + pr[1] + ')');
      if (hay < Math.min(pr[0], disp)) falla(nv.id + ' ' + nv.dif + ' con ' + hay + ' pruebas (minimo ' + Math.min(pr[0], disp) + ')');
    }
    if (nv.cap > 4) { largasN++; if (duro(nv.dif)) falla(nv.id + ': largas en un grado duro'); }
    if (minimoNivel(nv) > L) falla(nv.id + ' usa una mecanica que se estrena en el nivel ' + minimoNivel(nv));
    if (L <= 3 && nv.dif !== 'facil') falla(nv.id + ' deberia ser facil');
    if (L > 1) {
      const prev = camino[i - 1].dif;
      // maximo dos duros seguidos; tras dos, respiro; tras Muy o Extra, respiro (Facil o Normal)
      if (L > 2 && duro(prev) && duro(camino[i - 2].dif) && duro(nv.dif)) falla(nv.id + ': tres duros seguidos');
      if ((prev === 'muy' || prev === 'extra') && duro(nv.dif)) falla(nv.id + ': despues de ' + prev + ' debe haber respiro (Facil o Normal), salio ' + nv.dif);
    }
    if (nv.dif === 'extra' && L < 36) falla(nv.id + ': Extra antes de L36');
    if (L > 10 && nv.dif === 'facil' && camino[i - 1].dif === 'facil' && camino[i - 2].dif === 'facil' && camino[i - 3].dif === 'facil') falla(nv.id + ': cuatro Faciles seguidos');
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
  print('catalogo: ' + camino.length + ' niveles revisados; ' + DIFS.map(function (d) { return d + ' ' + cuentaDif[d]; }).join(', '));

  // meta de reparto de los 200 (ESPEC-v5 seccion 4)
  const nDuros = camino.filter(function (nv) { return duro(nv.dif); }).length;
  const nDuros81 = camino.slice(80).filter(function (nv) { return duro(nv.dif); }).length;
  const primero = function (d) { for (let i = 0; i < camino.length; i++) if (camino[i].dif === d) return i + 1; return 0; };
  print('reparto: duros ' + nDuros + ' (' + (nDuros / 2) + ' %), desde L81 ' + nDuros81 + ' de 120 (' + Math.round(nDuros81 / 1.2) + ' %), primer Muy L' + primero('muy') + ', primer Extra L' + primero('extra') + ', Extra ' + cuentaDif.extra);
  if (nDuros < 90) falla('duros ' + nDuros + ' de 200 (meta: 45 % o mas)');
  if (nDuros81 < 66) falla('duros desde L81: ' + nDuros81 + ' de 120 (meta: 55 % o mas)');
  if (cuentaDif.extra < 15) falla('solo ' + cuentaDif.extra + ' niveles Extra (meta: 15 o mas)');
  if (!(primero('muy') > 0 && primero('muy') < 25)) falla('el primer Muy esta en L' + primero('muy') + ' (meta: antes de L25)');
  if (!(primero('extra') >= 36 && primero('extra') <= 50)) falla('el primer Extra esta en L' + primero('extra') + ' (meta: entre L36 y L50)');
  for (let a = 0; a < 200; a += 50) {
    const ch = camino.slice(a, a + 50);
    print('  tramo L' + (a + 1) + '-' + (a + 50) + ': ' + DIFS.map(function (d) { return d + ' ' + ch.filter(function (nv) { return nv.dif === d; }).length; }).join(', ') + ' (duros ' + ch.filter(function (nv) { return duro(nv.dif); }).length + ')');
  }

  // franjas: la receta elige el candidato que cae en la de su grado; se reporta cuantos lo logran
  let enF = 0;
  DIFS.forEach(function (d) {
    enF += franjaGrado[d][1];
    const pc = franjaGrado[d][0] ? franjaGrado[d][1] / franjaGrado[d][0] : 1;
    print('  franja ' + d + ': ' + franjaGrado[d][1] + ' de ' + franjaGrado[d][0] + ' (' + Math.round(100 * pc) + ' %)');
    if (pc < 0.75) falla('solo ' + Math.round(100 * pc) + ' % de los ' + d + ' caen en su franja (minimo 75 %)');
  });
  if (enF < 170) falla('solo ' + enF + ' de 200 niveles caen en la franja de su grado (minimo 170)');
  print('  fuera de franja: ' + fueraDeFranja.join('; '));

  // meta promedio por grado: crece con la dureza (en Extra no baja de la de Muy, que ya esta casi en el tope de 12 colores)
  const metaMedia = {};
  DIFS.forEach(function (d) {
    const x = camino.filter(function (nv) { return nv.dif === d; });
    metaMedia[d] = x.reduce(function (s, nv) { return s + nv.meta; }, 0) / x.length;
  });
  print('meta media: ' + DIFS.map(function (d) { return d + ' ' + metaMedia[d].toFixed(1); }).join(', '));
  for (let q = 1; q < DIFS.length; q++) {
    const m = DIFS[q] === 'extra' ? metaMedia.extra >= metaMedia.muy * 0.97 : metaMedia[DIFS[q]] > metaMedia[DIFS[q - 1]];
    if (!m) falla('la meta media de ' + DIFS[q] + ' (' + metaMedia[DIFS[q]].toFixed(1) + ') no supera a ' + DIFS[q - 1] + ' (' + metaMedia[DIFS[q - 1]].toFixed(1) + ')');
  }
  // la meta promedio de los Normales sube de un tramo de 50 al siguiente (mas colores) y no salta mas de 50 %
  const promNormal = [];
  for (let a = 0; a < 200; a += 50) {
    const x = camino.slice(a, a + 50).filter(function (nv) { return nv.dif === 'normal'; });
    promNormal.push(x.reduce(function (s, nv) { return s + nv.meta; }, 0) / x.length);
  }
  for (let q = 1; q < promNormal.length; q++) {
    if (promNormal[q] <= promNormal[q - 1]) falla('la meta promedio de los Normales no sube en el tramo ' + (q + 1));
    if (promNormal[q] / promNormal[q - 1] > 1.5) falla('la meta de los Normales salta mas de 50 % en el tramo ' + (q + 1));
  }

  /* ---------- 1b) variantes de Reiniciar: otros colores y otro orden, la solucion traducida sigue ganando ---------- */
  (function () {
    let iguales = 0, hechas = 0;
    const firma = function (nv) { return JSON.stringify(nv.botellas.map(function (b) { return b.length; }).concat((nv.caps || []))); };
    camino.forEach(function (nv) {
      for (let s = 0; s < 3; s++) {
        const v = M.variante(nv, 'p' + s), nom = nv.id + ' variante ' + s;
        hechas++;
        if (JSON.stringify(v) !== JSON.stringify(M.variante(nv, 'p' + s))) falla(nom + ' no es determinista');
        if (JSON.stringify(v.botellas) === JSON.stringify(nv.botellas)) iguales++;
        if (v.botellas.length !== nv.botellas.length || v.meta !== nv.meta || v.movs.length !== nv.movs.length) falla(nom + ' cambio de tamano o de meta');
        // mismos colores distintos, mismas capas por color, todo dentro de la paleta
        const cu = {}, co = {};
        nv.botellas.forEach(function (b) { b.forEach(function (c) { co[c] = (co[c] || 0) + 1; }); });
        v.botellas.forEach(function (b) { b.forEach(function (c) { cu[c] = (cu[c] || 0) + 1; if (c < 1 || c > 12) falla(nom + ' color fuera de la paleta: ' + c); }); });
        const a1 = Object.keys(co).map(function (k) { return co[k]; }).sort(), a2 = Object.keys(cu).map(function (k) { return cu[k]; }).sort();
        if (JSON.stringify(a1) !== JSON.stringify(a2)) falla(nom + ' cambio el conteo de capas por color');
        // cajas contiguas al final, como el formato v2
        let fin = v.botellas.length;
        for (let c = v.cajas.length - 1; c >= 0; c--) {
          const bs = v.cajas[c].bots.slice().sort(function (x, y) { return x - y; });
          bs.forEach(function (i, q) { if (i !== fin - bs.length + q) falla(nom + ' caja ' + c + ' no queda contigua al final'); });
          fin -= bs.length;
        }
        // lo cerrado al empezar es lo mismo, contado
        let c0 = 0, c1 = 0;
        for (let i = 0; i < nv.botellas.length; i++) { if (M.cerrada({ b: nv.botellas, ab: 0 }, i, nv)) c0++; if (M.cerrada({ b: v.botellas, ab: 0 }, i, v)) c1++; }
        if (c0 !== c1) falla(nom + ' cerradas ' + c1 + ' en vez de ' + c0);
        // la solucion traducida gana jugada por jugada
        let E = { b: v.botellas, ab: 0 }, bien = true;
        for (let k = 0; k < v.movs.length; k++) {
          const m = v.movs[k];
          if (!M.puedeVerter(E, m[0], m[1], v)) { falla(nom + ' jugada ' + k + ' no es valida'); bien = false; break; }
          E = M.verter(E, m[0], m[1], v).estado;
        }
        if (bien && !M.ganado(E, v)) falla(nom + ' la solucion traducida no gana');
        if (v.candados.some(function (c, d) { return v.botellas[c.b].indexOf(c.color) < 0 && v.botellas.every(function (b) { return b.indexOf(c.color) < 0; }); })) falla(nom + ' candado de un color que no esta');
      }
    });
    print('variantes: ' + hechas + ' probadas, ' + iguales + ' con las mismas botellas que el original');
    if (iguales) falla(iguales + ' variantes salieron iguales al original');
  })();

  /* ---------- 2) en vivo, modo rapido ---------- */
  const vivos = [];
  for (let L = 201; L <= 230; L++) vivos.push({ nombre: 'camino-' + L, p: M.nivelParams(L), seed: 'camino:' + L });
  const base = Date.UTC(2026, 9, 21);
  for (let d = 0; d < 14; d++) {
    const f = new Date(base + d * 86400000).toISOString().slice(0, 10);
    vivos.push({ nombre: 'dia-' + f, p: M.diaParams(f), seed: 'dia:' + f });
  }
  let maxms = 0, maxn = '';
  const maxGrado = { facil: 0, normal: 0, dificil: 0, muy: 0, extra: 0 };
  const filas = [];
  vivos.forEach(function (v) {
    const t0 = Date.now();
    const n1 = M.generar(v.p, v.seed, { modo: 'rapido' });
    const ms = Date.now() - t0;
    const n2 = M.generar(v.p, v.seed, { modo: 'rapido' });
    if (JSON.stringify(n1) !== JSON.stringify(n2)) falla(v.nombre + ' no es determinista');
    if (n1.id !== v.nombre) falla(v.nombre + ' id ' + n1.id);
    const limite = (n1.dif === 'muy' || n1.dif === 'extra') ? 5000 : 2000;
    if (ms > limite) falla(v.nombre + ' (' + n1.dif + ') tardo ' + ms + ' ms (mas de ' + limite / 1000 + ' s)');
    if (ms > maxGrado[n1.dif]) maxGrado[n1.dif] = ms;
    if (v.p.dif !== n1.dif) falla(v.nombre + ' dif ' + n1.dif + ' distinta de la de sus parametros');
    const cols = revisar(n1, v.nombre, true);
    if (ms > maxms) { maxms = ms; maxn = v.nombre; }
    filas.push(pad(v.nombre, 18) + pad(cols, 4) + pad(n1.botellas.length, 4) + pad(n1.rasgos.join('+') || '-', 24) + pad(n1.meta, 5) + pad(n1.optimo ? 'opt' : 'no', 5) + ms + ' ms');
  });
  print('en vivo (modo rapido): nivel, colores, botellas, rasgos, meta, optimo, tiempo');
  filas.forEach(function (f) { print('  ' + f); });
  print('mayor tiempo en vivo: ' + maxms + ' ms (' + maxn + ')');
  print('maximo por grado (ms): ' + DIFS.map(function (d) { return d + ' ' + maxGrado[d]; }).join(', '));
  // las reglas del sorteo siguen valiendo mas alla de L200 (en vivo)
  (function () {
    for (let L = 201; L <= 400; L++) {
      const d = M.difDe(L), a = M.difDe(L - 1), b = M.difDe(L - 2);
      if (duro(d) && duro(a) && duro(b)) falla('L' + L + ': tres duros seguidos en vivo');
      if ((a === 'muy' || a === 'extra') && duro(d)) falla('L' + L + ': sin respiro tras ' + a);
    }
  })();

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
