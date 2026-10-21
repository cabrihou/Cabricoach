/* Motor de Botellas: puro, sin DOM, sin window.
   Corre en jsc (pruebas), en la pagina y dentro de un Web Worker creado desde un blob.
   Se expone como el objeto global MOTOR (globalThis), asi los tres lugares lo usan igual.

   Representacion: botella = arreglo de enteros de abajo hacia arriba (1..12),
   estado = arreglo de botellas, cap = capacidad de cada botella. */
(function (G) {
  'use strict';

  /* ---------- aleatoriedad con semilla ---------- */

  // cyrb53: hash de cadena a numero. Se queda con 32 bits para la semilla de mulberry32.
  function hashCadena(str) {
    let h1 = 0xdeadbeef, h2 = 0x41c6ce57;
    for (let i = 0; i < str.length; i++) {
      const ch = str.charCodeAt(i);
      h1 = Math.imul(h1 ^ ch, 2654435761);
      h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
    return (h2 >>> 0) * 4294967296 + (h1 >>> 0);
  }

  // mulberry32: generador diminuto y rapido; mismo seedStr => misma secuencia en toda maquina
  function rng(seedStr) {
    let a = (hashCadena(String(seedStr)) >>> 0) || 1;
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* ---------- parametros por nivel y por dia ---------- */

  /* ---------- rutas: 4 caminos de 50 niveles (la curva sale de ajustarla con INFORME-NIVELES.md) ---------- */

  const MAXBOT = 15; // tope de botellas del tablero (con la extra del jugador, 16)

  // tabla [[desde, valor], ...] ascendente: el valor del ultimo tramo que ya empezo
  function tramo(tabla, L) {
    let v = tabla[0][1];
    for (let i = 0; i < tabla.length; i++) if (L >= tabla[i][0]) v = tabla[i][1];
    return v;
  }
  // piezas de mecanica, siempre las mismas formas para que la lectura de la curva sea corta
  function cajaLiq(bots) { return { bots: bots, vacia: false }; }
  function cajaVacia(bots) { return { bots: bots, vacia: true }; }
  const CAND_LIQ = { vacia: false }, CAND_VACIO = { vacia: true };

  function coloresRuta(ruta, L) {
    if (ruta === 'facil') {
      // la meseta de 6 colores es larga a proposito: en Facil lo que sube son las mecanicas, no el cupo
      return tramo([[1, 3], [3, 4], [6, 5], [13, 6], [31, 7]], L);
    }
    if (ruta === 'normal') return tramo([[1, 5], [5, 6], [13, 7], [25, 8], [39, 9]], L);
    if (ruta === 'dificil') return tramo([[1, 8], [11, 9], [26, 10], [41, 11]], L);
    return tramo([[1, 10], [16, 11], [36, 12]], L); // muy
  }

  // Parametros de un nivel de ruta. L 1..50 sigue la curva; L > 50 repite el patron de mecanicas
  // de L41-50 con los colores de L50 (asi el que termina la ruta sigue con algo parecido a lo ultimo).
  function rutaParams(ruta, L) {
    if (ruta !== 'facil' && ruta !== 'normal' && ruta !== 'dificil' && ruta !== 'muy') ruta = 'normal';
    L = Math.max(1, Math.floor(L) || 1);
    const Lp = L > 50 ? 41 + ((L - 41) % 10) : L;       // nivel cuyo patron se usa
    let n = coloresRuta(ruta, L > 50 ? 50 : L);
    const p = { ruta: ruta, L: L, n: n, vacias: 2, cap: 4, misterio: 0, cajas: [], candados: [], cadena: false, hondo: 0, dif: ruta };
    if (ruta === 'facil') {
      p.seleccion = 'facil'; p.cuantos = 6; p.hondo = 0;
      if (Lp >= 20 && Lp % 10 === 0) { p.cap = 6; p.n = 4; }                  // largas: pocas franjas, mucha botella
      else if (Lp >= 15 && Lp % 5 === 0) p.misterio = 1;
      else if (Lp === 4) p.candados = [CAND_VACIO];                           // primer candado: premio en botella vacia
      else if (Lp === 7) p.cajas = [cajaVacia(1)];                            // primera llave: caja con una vacia
      else if (Lp >= 8) {
        const r = Lp % 3;
        if (r === 0) p.candados = [CAND_VACIO]; else if (r === 1) p.cajas = [cajaVacia(1)];
      }
    } else if (ruta === 'normal') {
      p.seleccion = 'mediana'; p.cuantos = 6; p.hondo = 0.5;
      const mis = Lp <= 15 ? 1 : 2;
      const poner = function (m) {
        if (m === 'cand') p.candados.push(CAND_LIQ);
        else if (m === 'llave') p.cajas.push(cajaLiq(1));
        else if (m === 'mist') p.misterio = mis;
      };
      if (Lp % 10 === 0) { p.cap = 6; p.n = Math.max(4, n - 3); }              // largas
      else if (Lp >= 25) { const ms = ['cand', 'llave', 'mist']; poner(ms[Lp % 3]); poner(ms[(Lp + 1) % 3]); }
      else if (Lp >= 2) poner(['cand', 'llave', 'mist', null][(Lp - 2) % 4]);
    } else if (ruta === 'dificil') {
      p.seleccion = 'dificil'; p.cuantos = 8; p.hondo = 1;
      if (Lp >= 15) {
        const par = Lp % 4;
        if (par === 0) { p.cajas.push(cajaLiq(2)); p.candados.push(CAND_LIQ); }
        else if (par === 1) { p.cajas.push(cajaLiq(1)); p.misterio = 2; }
        else if (par === 2) { p.candados.push(CAND_LIQ); p.misterio = 2; }
        else { p.cajas.push(cajaLiq(2)); p.misterio = 2; }
      } else {
        const m = Lp % 3;
        if (m === 0) p.cajas.push(cajaLiq(2)); else if (m === 1) p.candados.push(CAND_LIQ); else p.cajas.push(cajaLiq(1));
      }
      // Cada 5: una vacia de premio cerrada. Con caja se puede dejar solo 1 vacia libre; con candado no:
      // medido con el solver, un candado vacio con 1 sola libre casi nunca tiene salida (el color que
      // lo abre no se puede completar sin espacio), asi que ahi se queda con 2.
      if (Lp % 5 === 0) {
        if ((Lp / 5) % 2 === 0) p.candados.push(CAND_VACIO); else { p.vacias = 1; p.cajas.push(cajaVacia(1)); }
      }
    } else { // muy
      p.seleccion = 'muy'; p.cuantos = 10; p.hondo = 1;
      const m = Lp % 3;
      if (m === 0) { p.cajas = [cajaLiq(1), cajaLiq(2)]; p.candados = [CAND_VACIO]; } // 2 libres: con 1 no tiene salida
      else if (m === 1) { p.cajas = [cajaLiq(2)]; p.candados = [CAND_LIQ]; }
      else p.cajas = [cajaLiq(1), cajaLiq(1)];
      if (Lp >= 20 && Lp % 2 === 0 && p.cajas.length > 1) p.cadena = true;
      if (Lp % 4 === 0) p.misterio = 2;
    }
    // tope de botellas: si las vacias extra no caben, pasan a ser botellas con liquido
    const extras = function () {
      let t = p.n + p.vacias;
      p.cajas.forEach(function (c) { if (c.vacia) t++; });
      p.candados.forEach(function (c) { if (c.vacia) t++; });
      return t;
    };
    while (extras() > MAXBOT) {
      let hecho = false;
      for (let i = 0; i < p.candados.length && !hecho; i++) if (p.candados[i].vacia) { p.candados[i] = CAND_LIQ; hecho = true; }
      for (let i = 0; i < p.cajas.length && !hecho; i++) if (p.cajas[i].vacia) { p.cajas[i] = cajaLiq(p.cajas[i].bots); hecho = true; }
      if (!hecho) p.vacias--;
    }
    return p;
  }

  // El reto del dia: dificultad y mecanicas por dia de la semana (domingo a sabado), siempre en modo rapido
  function diaParams(fechaISO) {
    const q = fechaISO.split('-').map(Number);
    const dow = new Date(Date.UTC(q[0], q[1] - 1, q[2])).getUTCDay();
    const dia = [
      { n: 10, dif: 'muy', llave: 1, cand: 1 },        // dom
      { n: 6, dif: 'facil', candVacio: 1 },            // lun
      { n: 7, dif: 'normal', llave: 1 },               // mar
      { n: 8, dif: 'normal', mis: 1 },                 // mie
      { n: 9, dif: 'dificil', cand: 1 },               // jue
      { n: 8, dif: 'normal', llave: 1, cand: 1 },      // vie
      { n: 9, dif: 'dificil', mis: 1, llave: 1 }       // sab
    ][dow];
    return {
      ruta: 'dia', fecha: fechaISO, n: dia.n, vacias: 2, cap: 4, dif: dia.dif,
      misterio: dia.mis ? 2 : 0,
      cajas: dia.llave ? [cajaLiq(1)] : [],
      candados: dia.cand ? [CAND_LIQ] : (dia.candVacio ? [CAND_VACIO] : []),
      cadena: false, hondo: dia.dif === 'facil' ? 0 : (dia.dif === 'normal' ? 0.5 : 1),
      seleccion: { facil: 'facil', normal: 'mediana', dificil: 'dificil', muy: 'muy' }[dia.dif], cuantos: 3
    };
  }


  /* ---------- el camino (v3): un solo recorrido, con dificultad sorteada por nivel ---------- */

  const DIFS = ['facil', 'normal', 'dificil', 'muy'];
  // [nivel, mecanica]: en ese nivel se estrena (siempre Facil o Normal, y con la Novedad en la interfaz)
  const ESTRENOS = [[4, 'candVacio'], [7, 'cajaVacia'], [12, 'candLiq'], [16, 'cajaLiq'], [20, 'mistLeve'],
                    [25, 'largas'], [35, 'mistTotal'], [50, 'dosCajas'], [80, 'cadena']];
  function estrenoDe(L) {
    for (let i = 0; i < ESTRENOS.length; i++) if (ESTRENOS[i][0] === L) return ESTRENOS[i][1];
    return null;
  }
  function antesDeEstreno(L) { return estrenoDe(L + 1) !== null; }

  function pesosDif(L) {
    if (L <= 3) return [100, 0, 0, 0];
    if (L <= 10) return [60, 40, 0, 0];
    if (L <= 29) return [35, 45, 20, 0];
    if (L <= 100) return [25, 45, 20, 10];
    return [20, 40, 25, 15];
  }
  // Se sortea en orden desde L=1 porque cada nivel depende del anterior (por eso se memoriza).
  // Cada nivel usa su propio rng('dif:'+L): el resultado no depende de cuantos se hayan pedido antes.
  const MEMO_DIF = [null];
  function sortearDif(L) {
    const prev = MEMO_DIF[L - 1];
    const w = pesosDif(L).slice();
    const duro = function (d) { return d === 'dificil' || d === 'muy'; };
    if (prev === 'muy') return 'facil';                    // despues de un Muy dificil, respiro
    if (duro(prev)) { w[2] = 0; w[3] = 0; }                 // nunca dos duros seguidos
    let tot = 0; w.forEach(function (x) { tot += x; });
    let x = rng('dif:' + L)() * tot, d = DIFS[0];
    for (let i = 0; i < 4; i++) { x -= w[i]; if (x < 0) { d = DIFS[i]; break; } }
    if (duro(d) && (estrenoDe(L) || antesDeEstreno(L))) d = 'normal'; // el estreno y su vispera no son duros
    if (d === 'facil' && L > 10 && MEMO_DIF[L - 1] === 'facil' && MEMO_DIF[L - 2] === 'facil' && MEMO_DIF[L - 3] === 'facil') d = 'normal';
    return d;
  }
  function difDe(L) {
    L = Math.max(1, Math.floor(L) || 1);
    for (let k = MEMO_DIF.length; k <= L; k++) MEMO_DIF[k] = sortearDif(k);
    return MEMO_DIF[L];
  }

  function coloresBase(L) { return tramo([[1, 3], [3, 4], [6, 5], [13, 6], [26, 7], [46, 8], [71, 9], [101, 10], [141, 11]], L); }

  // Parametros de un nivel del camino (L >= 1, sin tope). Misma forma que rutaParams, mas id, dif y estreno.
  function nivelParams(L) {
    L = Math.max(1, Math.floor(L) || 1);
    const dif = difDe(L), idx = DIFS.indexOf(dif), estreno = estrenoDe(L);
    const R = rng('mec:' + L);
    const n = Math.max(3, Math.min(12, coloresBase(L) + [-1, 0, 1, 2][idx]));
    const p = { ruta: 'camino', L: L, id: 'camino-' + L, n: n, vacias: 2, cap: 4, misterio: 0, cajas: [], candados: [], cadena: false,
                hondo: [0, 0.5, 1, 1][idx], dif: dif, estreno: estreno,
                seleccion: ['facil', 'mediana', 'dificil', 'muy'][idx], cuantos: [6, 6, 8, 10][idx] };
    const largas = function () { p.cap = 6; p.n = Math.max(4, Math.min(6, n - 3)); };
    if (estreno) {
      // el estreno va solo y limpio: la mecanica nueva es lo unico distinto del nivel
      if (estreno === 'candVacio') p.candados = [CAND_VACIO];
      else if (estreno === 'cajaVacia') p.cajas = [cajaVacia(1)];
      else if (estreno === 'candLiq') p.candados = [CAND_LIQ];
      else if (estreno === 'cajaLiq') p.cajas = [cajaLiq(1)];
      else if (estreno === 'mistLeve') p.misterio = 1;
      else if (estreno === 'largas') largas();
      else if (estreno === 'mistTotal') p.misterio = 2;
      else if (estreno === 'dosCajas') p.cajas = [cajaLiq(1), cajaLiq(1)];
      else if (estreno === 'cadena') { p.cajas = [cajaLiq(1), cajaLiq(2)]; p.cadena = true; }
    } else {
      sortearMecanicas(p, L, idx, R);
    }
    return topar(p);
  }

  // Mecanicas ya estrenadas, sorteadas segun la dificultad: Facil 0-1, Normal 1 (a veces 0), Dificil 1-2, Muy 2-3.
  function sortearMecanicas(p, L, idx, R) {
    if (L >= 25 && idx <= 1 && R() < 0.12) { p.cap = 6; p.n = Math.max(4, Math.min(6, p.n - 3)); return; } // largas: solas
    const cuantas = idx === 0 ? (R() < 0.5 ? 1 : 0) : idx === 1 ? (R() < 0.85 ? 1 : 0) : idx === 2 ? 1 + (R() < 0.5 ? 1 : 0) : 2 + (R() < 0.4 ? 1 : 0);
    const kinds = [];
    if (L >= 4) kinds.push('cv');
    if (L >= 7) kinds.push('xv');
    if (L >= 12) kinds.push('cl');
    if (L >= 16) kinds.push('xl');
    if (L >= 20) kinds.push('m');
    if (L >= 50 && idx >= 2) kinds.push('2c');
    if (L >= 80 && idx >= 2) kinds.push('cad');
    barajar(kinds, R);
    const pick = {};
    let hechas = 0;
    for (let i = 0; i < kinds.length && hechas < cuantas; i++) {
      const k = kinds[i];
      const esCaja = k === 'xv' || k === 'xl' || k === '2c' || k === 'cad';
      const hayCaja = pick.xv || pick.xl || pick['2c'] || pick.cad;
      if ((k === 'cv' || k === 'cl') && (pick.cv || pick.cl)) continue;   // un solo candado
      if (esCaja && hayCaja && !((k === 'xv' && pick.xl) || (k === 'xl' && pick.xv)) ) continue;
      if (esCaja && hayCaja && L < 50) continue;                           // dos cajas solo desde que se estrenan
      pick[k] = true; hechas++;
    }
    if (pick.cv) p.candados.push(CAND_VACIO);
    if (pick.cl) p.candados.push(CAND_LIQ);
    if (pick.xv) p.cajas.push(cajaVacia(1));
    if (pick.xl) p.cajas.push(cajaLiq(idx >= 2 && R() < 0.5 ? 2 : 1));
    if (pick['2c']) p.cajas.push(cajaLiq(1), cajaLiq(idx >= 2 && R() < 0.5 ? 2 : 1));
    if (pick.cad) { p.cajas.push(cajaLiq(1), cajaLiq(2)); p.cadena = true; }
    if (pick.m) p.misterio = (idx >= 2 && L >= 35) ? 2 : 1;
    // una sola vacia libre solo con caja vacia (medido: el candado vacio con una libre casi nunca tiene salida)
    if (idx >= 2 && pick.xv && !pick.cv && R() < 0.5) p.vacias = 1;
  }

  // si las vacias extra no caben en 15 botellas, pasan a ser botellas con liquido
  function topar(p) {
    const total = function () {
      let t = p.n + p.vacias;
      p.cajas.forEach(function (c) { if (c.vacia) t++; });
      p.candados.forEach(function (c) { if (c.vacia) t++; });
      return t;
    };
    while (total() > MAXBOT) {
      let hecho = false;
      for (let i = 0; i < p.candados.length && !hecho; i++) if (p.candados[i].vacia) { p.candados[i] = CAND_LIQ; hecho = true; }
      for (let i = 0; i < p.cajas.length && !hecho; i++) if (p.cajas[i].vacia) { p.cajas[i] = cajaLiq(p.cajas[i].bots); hecho = true; }
      if (!hecho) { if (p.vacias > 2) p.vacias--; else p.n--; }
    }
    return p;
  }

  /* ---------- contexto del nivel y estado ----------
     C (fijo por nivel): { cap, llaves:[{b,k,caja}], cajas:[{bots:[i,...]}], candados:[{b,color}] }
       llave: esta en la capa k (desde abajo) de la botella b y abre la caja `caja`.
              Sale cuando esa capa queda arriba (la botella baja a k+1 capas o menos).
       caja: botellas que no se pueden tocar hasta que su llave salga.
       candado: la botella b no se puede tocar hasta que se complete una botella de `color`.
     E (cambia en cada jugada): { b:[[...],...], ab } con ab = bits de lo que ya abrio:
       bit c = caja c (c < 4), bit 4+d = candado d (d < 4).
     Atajos: C puede ser un numero (solo cap) y E un arreglo de botellas (nada abierto).
     Un objeto de nivel completo (el que devuelve generar) sirve tal cual como C. */
  const MAXC = 4;
  const CACHE = typeof WeakMap !== 'undefined' ? new WeakMap() : null;
  function compilar(C) {
    const P = { esP: true, cap: C.cap, llaves: C.llaves || [], cajas: C.cajas || [], candados: C.candados || [], cierre: [], porColor: [], llaveEn: [] };
    P.cajas.forEach(function (cj, c) { cj.bots.forEach(function (i) { P.cierre[i] = (P.cierre[i] || 0) | (1 << c); }); });
    P.candados.forEach(function (cd, d) {
      const bit = 1 << (MAXC + d);
      P.cierre[cd.b] = (P.cierre[cd.b] || 0) | bit;
      P.porColor[cd.color] = (P.porColor[cd.color] || 0) | bit;
    });
    P.llaves.forEach(function (ll, q) { (P.llaveEn[ll.b] = P.llaveEn[ll.b] || []).push({ k: ll.k, bit: 1 << ll.caja, caja: ll.caja, q: q }); });
    P.simple = !P.llaves.length && !P.cajas.length && !P.candados.length;
    return P;
  }
  // el compilado se guarda aparte (WeakMap) para no ensuciar el objeto del nivel que se serializa
  function prep(C) {
    if (typeof C === 'number') return compilar({ cap: C });
    if (C.esP) return C;
    let P = CACHE && CACHE.get(C);
    if (!P) { P = compilar(C); if (CACHE) CACHE.set(C, P); }
    return P;
  }
  function nE(E) { return Array.isArray(E) ? { b: E, ab: 0 } : { b: E.b, ab: E.ab | 0 }; }
  function cerradaP(P, ab, i) { const m = P.cierre[i]; return !!m && (m & ~ab) !== 0; }
  function llaveDentro(P, ab, i) {
    const ls = P.llaveEn[i];
    if (ls) for (let q = 0; q < ls.length; q++) if (!(ab & ls[q].bit)) return true;
    return false;
  }

  /* ---------- reglas ---------- */

  function racha(b) {
    // largo de la racha contigua del color de arriba
    if (!b.length) return 0;
    const c = b[b.length - 1];
    let k = 0;
    for (let x = b.length - 1; x >= 0 && b[x] === c; x--) k++;
    return k;
  }
  function unColor(b) {
    for (let x = 1; x < b.length; x++) if (b[x] !== b[0]) return false;
    return b.length > 0;
  }
  function completa(b, cap) { return b.length === cap && unColor(b); }
  function ganadoB(b, cap) {
    // las cerradas tambien cuentan: una caja con liquido adentro no deja ganar
    for (let i = 0; i < b.length; i++) if (b[i].length && !completa(b[i], cap)) return false;
    return true;
  }
  function puedeV(b, ab, i, j, P) {
    if (i === j) return false;
    const a = b[i], d = b[j], cap = P.cap;
    if (!a || !d || !a.length || completa(a, cap)) return false;
    if (d.length >= cap) return false;
    if (P.cierre[i] && cerradaP(P, ab, i)) return false;
    if (P.cierre[j] && cerradaP(P, ab, j)) return false;
    if (!d.length) {
      // verter una botella de un solo color a una vacia solo la cambia de lugar,
      // salvo que tenga una llave adentro: ahi sacar el liquido libera la llave
      return !unColor(a) || llaveDentro(P, ab, i);
    }
    return d[d.length - 1] === a[a.length - 1];
  }
  function vert(b, ab, i, j, P) {
    const cap = P.cap, a = b[i], d = b[j];
    const color = a[a.length - 1];
    const cantidad = Math.min(racha(a), cap - d.length);
    const nb = b.slice();
    nb[i] = a.slice(0, a.length - cantidad);
    const nd = d.slice();
    for (let k = 0; k < cantidad; k++) nd.push(color);
    nb[j] = nd;
    let ab2 = ab, abre = null;
    // llaves: salen cuando su capa queda arriba (o cuando se va con el chorro)
    const ls = P.llaveEn[i];
    if (ls) for (let q = 0; q < ls.length; q++) {
      const l = ls[q];
      if (!(ab2 & l.bit) && nb[i].length <= l.k + 1) {
        ab2 |= l.bit;
        (abre = abre || []).push({ tipo: 'caja', caja: l.caja, llave: l.q, b: i, k: l.k });
      }
    }
    // candados: abren cuando se completa una botella de su color
    if (P.porColor[color] && completa(nd, cap)) {
      const bits = P.porColor[color] & ~ab2;
      if (bits) {
        ab2 |= bits;
        for (let dd = 0; dd < P.candados.length; dd++)
          if (bits & (1 << (MAXC + dd))) (abre = abre || []).push({ tipo: 'candado', candado: dd, b: P.candados[dd].b, color: color });
      }
    }
    return { b: nb, ab: ab2, cantidad: cantidad, color: color, abre: abre };
  }

  // API publica: E = {b, ab} (o arreglo), C = nivel (o cap)
  function puedeVerter(E, i, j, C) { const e = nE(E); return puedeV(e.b, e.ab, i, j, prep(C)); }
  function verter(E, i, j, C) {
    const e = nE(E), r = vert(e.b, e.ab, i, j, prep(C));
    return { estado: { b: r.b, ab: r.ab }, cantidad: r.cantidad, color: r.color, abre: r.abre || [] };
  }
  function ganado(E, C) { return ganadoB(nE(E).b, prep(C).cap); }
  function cerrada(E, i, C) { const e = nE(E); return cerradaP(prep(C), e.ab, i); }
  function hayJugadas(E, C) {
    const e = nE(E), P = prep(C);
    for (let i = 0; i < e.b.length; i++)
      for (let j = 0; j < e.b.length; j++)
        if (puedeV(e.b, e.ab, i, j, P)) return true;
    return false;
  }
  function estrellasDe(movs, meta) {
    if (movs <= meta) return 3;
    if (movs <= Math.ceil(meta * 1.25)) return 2;
    return 1;
  }

  /* ---------- solver ---------- */

  function cadena(b) {
    let t = '';
    for (let x = 0; x < b.length; x++) t += String.fromCharCode(96 + b[x]);
    return t;
  }
  // marca de la botella: su contenido mas las llaves que todavia tiene adentro
  function marca(b, ab, i, P) {
    let t = cadena(b[i]);
    const ls = P.llaveEn[i];
    if (ls) for (let q = 0; q < ls.length; q++) if (!(ab & ls[q].bit)) t += '#' + ls[q].k;
    return t;
  }
  // el orden de las botellas abiertas no importa: la clave las ordena.
  // Las cerradas van aparte por posicion, y lo abierto (ab) entra en la clave.
  function claveP(b, ab, P) {
    const t = [];
    if (P.simple) {
      for (let i = 0; i < b.length; i++) t.push(cadena(b[i]));
      t.sort();
      return t.join(',');
    }
    const fijas = [];
    for (let i = 0; i < b.length; i++) {
      const m = marca(b, ab, i, P);
      if (P.cierre[i] && cerradaP(P, ab, i)) fijas.push(i + ':' + m); else t.push(m);
    }
    t.sort();
    return ab + '|' + t.join(',') + '|' + fijas.join(',');
  }
  function clave(E, C) { const e = nE(E); return claveP(e.b, e.ab, prep(C)); }
  // h = rachas totales menos colores distintos. Admisible: un vertido baja la cuenta en 1 como mucho,
  // y abrir una caja o un candado no cuesta jugadas.
  function heuristica(s) {
    if (!Array.isArray(s)) s = s.b;
    let rachas = 0, mask = 0;
    for (let i = 0; i < s.length; i++) {
      const b = s[i];
      for (let x = 0; x < b.length; x++) {
        mask |= (1 << b[x]);
        if (x === 0 || b[x] !== b[x - 1]) rachas++;
      }
    }
    let colores = 0;
    for (let m = mask; m; m &= m - 1) colores++;
    return rachas - colores;
  }

  // jugadas de un estado, sin las equivalentes (mismo origen repetido, destinos iguales)
  function jugadasP(b, ab, P) {
    const out = [], origenes = {}, cap = P.cap;
    for (let i = 0; i < b.length; i++) {
      const a = b[i];
      if (!a.length || completa(a, cap)) continue;
      if (P.cierre[i] && cerradaP(P, ab, i)) continue;
      const ka = marca(b, ab, i, P);
      if (origenes[ka]) continue;
      origenes[ka] = 1;
      const destinos = {};
      for (let j = 0; j < b.length; j++) {
        if (!puedeV(b, ab, i, j, P)) continue;
        const kd = marca(b, ab, j, P);
        if (destinos[kd]) continue;
        destinos[kd] = 1;
        out.push([i, j]);
      }
    }
    return out;
  }
  function jugadas(E, C) { const e = nE(E); return jugadasP(e.b, e.ab, prep(C)); }

  // montículo binario por (f, luego mayor g)
  function Monticulo() { this.a = []; }
  Monticulo.prototype.mejor = function (x, y) { return x.f < y.f || (x.f === y.f && x.g > y.g); };
  Monticulo.prototype.push = function (n) {
    const a = this.a; a.push(n);
    let i = a.length - 1;
    while (i > 0) {
      const p = (i - 1) >> 1;
      if (this.mejor(a[i], a[p])) { const t = a[i]; a[i] = a[p]; a[p] = t; i = p; } else break;
    }
  };
  Monticulo.prototype.pop = function () {
    const a = this.a;
    const top = a[0], last = a.pop();
    if (a.length) {
      a[0] = last;
      let i = 0;
      for (;;) {
        const l = 2 * i + 1, r = l + 1;
        let m = i;
        if (l < a.length && this.mejor(a[l], a[m])) m = l;
        if (r < a.length && this.mejor(a[r], a[m])) m = r;
        if (m === i) break;
        const t = a[i]; a[i] = a[m]; a[m] = t; i = m;
      }
    }
    return top;
  };

  // peso 1 = A* optimo; peso 3 = ponderado (rapido, casi optimo)
  function astar(b0, ab0, P, peso, tope) {
    const mejorG = new Map();
    const open = new Monticulo();
    const raiz = { s: b0, ab: ab0, g: 0, f: peso * heuristica(b0), p: null, m: null, k: claveP(b0, ab0, P) };
    mejorG.set(raiz.k, 0);
    open.push(raiz);
    let nodos = 0;
    while (open.a.length) {
      const n = open.pop();
      if (n.g > mejorG.get(n.k)) continue; // version vieja del estado
      if (ganadoB(n.s, P.cap)) {
        const movs = [];
        for (let x = n; x.p; x = x.p) movs.push(x.m);
        movs.reverse();
        return { movs: movs, largo: movs.length, optimo: peso === 1, nodos: nodos };
      }
      if (++nodos > tope) return null;
      const js = jugadasP(n.s, n.ab, P);
      for (let q = 0; q < js.length; q++) {
        const i = js[q][0], j = js[q][1];
        const r = vert(n.s, n.ab, i, j, P);
        const k = claveP(r.b, r.ab, P);
        const g = n.g + 1;
        const prev = mejorG.get(k);
        if (prev !== undefined && prev <= g) continue;
        mejorG.set(k, g);
        open.push({ s: r.b, ab: r.ab, g: g, f: g + peso * heuristica(r.b), p: n, m: [i, j], k: k });
      }
    }
    // se vacio la frontera: el espacio alcanzable se agoto sin ganar
    return { sinSolucion: true, nodos: nodos };
  }

  // DFS con visitados: ultimo recurso, no es optimo. Primero las jugadas que completan o juntan color.
  function dfs(b0, ab0, P, tope) {
    const visto = new Set();
    let nodos = 0;
    const camino = [];
    const cap = P.cap;
    function rec(s, ab, prof) {
      if (ganadoB(s, cap)) return true;
      if (++nodos > tope || prof > 300) return false;
      const js = jugadasP(s, ab, P);
      const pun = js.map(function (m) {
        const d = s[m[1]];
        const r = vert(s, ab, m[0], m[1], P);
        let sc = 0;
        if (completa(r.b[m[1]], cap)) sc -= 100;
        if (r.abre) sc -= 50;
        if (d.length) sc -= 10;
        sc += heuristica(r.b);
        return { m: m, r: r, sc: sc };
      });
      pun.sort(function (a, b) { return a.sc - b.sc; });
      for (let q = 0; q < pun.length; q++) {
        const k = claveP(pun[q].r.b, pun[q].r.ab, P);
        if (visto.has(k)) continue;
        visto.add(k);
        camino.push(pun[q].m);
        if (rec(pun[q].r.b, pun[q].r.ab, prof + 1)) return true;
        camino.pop();
        if (nodos > tope) return false;
      }
      return false;
    }
    visto.add(claveP(b0, ab0, P));
    if (rec(b0, ab0, 0)) return { movs: camino.slice(), largo: camino.length, optimo: false, nodos: nodos };
    return nodos > tope ? null : { sinSolucion: true, nodos: nodos };
  }

  // Devuelve {movs,largo,optimo,nodos}, {sinSolucion:true} si se demostro que no hay, o null si se paso el tope.
  // opts.tope baja los tres topes (opts.topes = [a*, ponderado, dfs] los fija uno por uno);
  // opts.rapido se salta el A* optimo (para pistas y vigilancia en juego).
  function resolver(E, C, opts) {
    opts = opts || {};
    const e = nE(E), P = prep(C);
    if (ganadoB(e.b, P.cap)) return { movs: [], largo: 0, optimo: true, nodos: 0 };
    const tt = opts.topes || [Math.min(60000, opts.tope || 60000), Math.min(150000, opts.tope || 150000), Math.min(200000, opts.tope || 200000)];
    let total = 0, r;
    if (!opts.rapido) {
      r = astar(e.b, e.ab, P, 1, tt[0]);
      if (r) return r;
      total += tt[0];
    }
    r = astar(e.b, e.ab, P, 3, tt[1]);
    if (r) { r.nodos += total; return r; }
    total += tt[1];
    r = dfs(e.b, e.ab, P, tt[2]);
    if (r) { r.nodos += total; return r; }
    return null;
  }

  // primer movimiento de la solucion desde el estado actual
  function pista(E, C, opts) {
    if (ganado(E, C)) return { listo: true };
    const r = resolver(E, C, { rapido: true, tope: (opts && opts.tope) || 40000 });
    if (!r) return { desconocido: true };
    if (r.sinSolucion) return { sinSalida: true };
    return { mov: r.movs[0], restan: r.largo };
  }

  /* ---------- generador de niveles v2 ---------- */

  function barajar(arr, R) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(R() * (i + 1));
      const t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
  }

  // Un reparto con sus mecanicas, todavia sin resolver. Devuelve null si no hubo donde poner algo
  // (el llamador lo cuenta como intento fallido). Orden final: sueltas mezcladas y al final las
  // botellas de cada caja, contiguas (el formato de nivel v2).
  function armar(p, R) {
    const cap = p.cap, n = p.n;
    const cajasP = p.cajas || [], candP = p.candados || [];
    let cont = null;
    for (let t = 0; t < 60 && !cont; t++) {
      const capas = [];
      for (let c = 1; c <= n; c++) for (let k = 0; k < cap; k++) capas.push(c);
      barajar(capas, R);
      const bs = [];
      let mono = false;
      for (let b = 0; b < n; b++) {
        const bt = capas.slice(b * cap, (b + 1) * cap);
        if (completa(bt, cap)) mono = true; // una botella ya resuelta regala el nivel
        bs.push(bt);
      }
      if (!mono) cont = bs;
    }
    if (!cont) return null;
    const enCaja = [];
    for (let i = 0; i < n; i++) enCaja.push(-1);
    const pool = [];
    for (let i = 0; i < n; i++) pool.push(i);
    barajar(pool, R);

    // cajas: de liquido (botellas del reparto) o con una vacia de premio
    const miembros = [];
    for (let c = 0; c < cajasP.length; c++) {
      const m = [];
      let faltan = cajasP[c].bots;
      if (cajasP[c].vacia) { cont.push([]); enCaja.push(c); m.push(cont.length - 1); faltan--; }
      for (; faltan > 0; faltan--) {
        if (!pool.length) return null;
        const i = pool.pop(); enCaja[i] = c; m.push(i);
      }
      miembros.push(m);
    }
    // llaves: enterradas bajo al menos una capa (k <= len-2), mas hondo en las rutas dificiles.
    // La llave de una caja nunca va en esa misma caja; con cadena, la de la caja 1 va dentro de la 0.
    const llaveEn = [], llaves = [];
    for (let c = 0; c < cajasP.length; c++) {
      let hosts = [];
      if (p.cadena && c === 1) {
        hosts = miembros[0].filter(function (i) { return cont[i].length > 0 && !llaveEn[i]; });
      } else {
        for (let i = 0; i < n; i++) if (enCaja[i] < 0 && !llaveEn[i]) hosts.push(i);
      }
      if (!hosts.length) return null;
      const h = hosts[Math.floor(R() * hosts.length)];
      const kmax = cont[h].length - 2;
      const k = Math.max(0, kmax - Math.floor(R() * (1 + (p.hondo || 0) * kmax)));
      llaveEn[h] = true;
      llaves.push({ b: h, k: k, caja: c });
    }
    // candados: el color pedido no puede estar dentro de la botella cerrada (si no, no habria salida)
    const candEn = [], candados = [], usados = {};
    for (let d = 0; d < candP.length; d++) {
      let b, opciones = [];
      if (candP[d].vacia) {
        cont.push([]); enCaja.push(-1); b = cont.length - 1;
        for (let c = 1; c <= n; c++) if (!usados[c]) opciones.push(c);
      } else {
        const hosts = [];
        for (let i = 0; i < n; i++) if (enCaja[i] < 0 && !llaveEn[i] && !candEn[i]) hosts.push(i);
        if (!hosts.length) return null;
        b = hosts[Math.floor(R() * hosts.length)];
        for (let c = 1; c <= n; c++) if (!usados[c] && cont[b].indexOf(c) < 0) opciones.push(c);
      }
      if (!opciones.length) return null;
      const color = opciones[Math.floor(R() * opciones.length)];
      usados[color] = true; candEn[b] = true;
      candados.push({ b: b, color: color });
    }
    for (let v = 0; v < p.vacias; v++) { cont.push([]); enCaja.push(-1); }
    if (cont.length > MAXBOT) return null;

    // orden final: sueltas mezcladas, luego cada caja entera
    const orden = [];
    for (let i = 0; i < cont.length; i++) if (enCaja[i] < 0) orden.push(i);
    barajar(orden, R);
    const cajasOut = [];
    for (let c = 0; c < miembros.length; c++) {
      const m = miembros[c].slice();
      barajar(m, R);
      const nuevos = [];
      for (let q = 0; q < m.length; q++) { orden.push(m[q]); nuevos.push(orden.length - 1); }
      cajasOut.push({ bots: nuevos });
    }
    const nuevo = [];
    orden.forEach(function (viejo, pos) { nuevo[viejo] = pos; });
    const botellas = orden.map(function (i) { return cont[i].slice(); });
    const out = {
      botellas: botellas,
      llaves: llaves.map(function (l) { return { b: nuevo[l.b], k: l.k, caja: l.caja }; }),
      cajas: cajasOut,
      candados: candados.map(function (d) { return { b: nuevo[d.b], color: d.color }; }),
      ocultas: null
    };
    if (p.misterio) {
      // 1 = leve (se ven las 2 de arriba), 2 = total (solo la de arriba). Las botellas de caja se
      // ven a traves del vidrio, asi que no llevan capas ocultas.
      const ven = (p.misterio === 2 || p.misterio === true) ? 1 : 2;
      out.ocultas = botellas.map(function (b, i) {
        const cerrada = enCaja[orden[i]] >= 0;
        return b.map(function (_, k) { return !cerrada && k < b.length - ven; });
      });
    }
    return out;
  }

  /* ---------- jugador medio-aleatorio: mide que tan relajado es un nivel ---------- */

  // Devuelve 1 si gana, -1 si se queda sin jugadas posibles, 0 si se acaban las jugadas del tope.
  // Elige al azar entre las jugadas validas (sin equivalentes y sin deshacer la anterior) con pesos:
  // completar una botella 8, abrir caja o candado 6, caer sobre su mismo color 3, caer en una vacia 1.
  function jugarBot(b0, P, meta, R) {
    let b = b0, ab = 0, prevK = null, curK = claveP(b, ab, P);
    const tope = 3 * meta + 20, cap = P.cap;
    for (let t = 0; t < tope; t++) {
      if (ganadoB(b, cap)) return 1;
      const js = jugadasP(b, ab, P);
      if (!js.length) return -1;
      let op = [], total = 0;
      for (let q = 0; q < js.length; q++) {
        const i = js[q][0], j = js[q][1];
        const r = vert(b, ab, i, j, P);
        const k = claveP(r.b, r.ab, P);
        let w = b[j].length ? 3 : 1;
        if (r.abre && w < 6) w = 6;
        if (completa(r.b[j], cap)) w = 8;
        op.push({ r: r, k: k, w: w, undo: k === prevK });
      }
      const sin = op.filter(function (o) { return !o.undo; });
      if (sin.length) op = sin;
      for (let q = 0; q < op.length; q++) total += op[q].w;
      let x = R() * total, el = op[op.length - 1];
      for (let q = 0; q < op.length; q++) { x -= op[q].w; if (x < 0) { el = op[q]; break; } }
      prevK = curK; curK = el.k; b = el.r.b; ab = el.r.ab;
    }
    return ganadoB(b, cap) ? 1 : 0;
  }

  /* ---------- generar ---------- */

  // topes del solver: el catalogo se genera una sola vez y puede gastar minutos; en vivo se queda
  // corto a proposito (A* optimo solo si es chico, luego ponderado) para entrar en ~2 s por nivel.
  const TOPES_CATALOGO = [400000, 400000, 400000];
  const TOPES_RAPIDO = [12000, 40000, 30000];

  // opts.modo: 'catalogo' (6 a 10 candidatos con metricas bot y atasco) o 'rapido' (3 candidatos, sin metricas).
  // Determinista por semilla y modo: todo el azar sale de rng(seedStr) y de las semillas 'bot:...'.
  function generar(p, seedStr, opts) {
    opts = opts || {};
    const cat = opts.modo === 'catalogo';
    const R = rng(seedStr);
    // compatibilidad con los parametros viejos (nivelParams): tipo -> seleccion
    const sel = p.seleccion || (p.tipo === 'dificil' ? 'dificil' : (p.tipo === 'respiro' ? 'facil' : 'mediana'));
    const cuantosP = p.cuantos || { normal: 4, dificil: 10, respiro: 3, largas: 3 }[p.tipo] || 4;
    const cuantos = cat ? cuantosP : Math.min(3, cuantosP);
    const topes = cat ? TOPES_CATALOGO : TOPES_RAPIDO;
    const partidas = opts.partidas || 40;
    const cands = [];
    let intentos = 0;
    const maxInt = cat ? 800 : 150;
    while (cands.length < cuantos && intentos < maxInt) {
      intentos++;
      const a = armar(p, R);
      if (!a) continue;
      const C = { cap: p.cap, llaves: a.llaves, cajas: a.cajas, candados: a.candados };
      const r = resolver(a.botellas, C, { topes: topes });
      if (!r || r.sinSolucion) continue;
      const c = { a: a, C: C, meta: r.largo, optimo: r.optimo, movs: r.movs, bot: 0, atasco: 0, idx: cands.length };
      if (cat) {
        const P = prep(C), Rb = rng('bot:' + seedStr + ':' + cands.length);
        let gana = 0, atasca = 0;
        for (let g = 0; g < partidas; g++) {
          const z = jugarBot(a.botellas, P, r.largo, Rb);
          if (z === 1) gana++; else if (z === -1) atasca++;
        }
        c.bot = Math.round(1000 * gana / partidas) / 1000;
        c.atasco = Math.round(1000 * atasca / partidas) / 1000;
      }
      cands.push(c);
    }
    if (!cands.length) throw new Error('No se pudo generar ' + seedStr);
    // criterio por ruta; el indice desempata para que la eleccion sea estable
    let puntaje;
    if (!cat) {
      if (sel === 'facil') puntaje = function (c) { return -c.meta; };
      else if (sel === 'mediana') puntaje = null;
      else puntaje = function (c) { return c.meta; };
    } else if (sel === 'facil') puntaje = function (c) { return c.bot * 1000 - c.meta; };
    else if (sel === 'dificil') puntaje = function (c) { return c.meta * 1000 - c.bot; };
    else if (sel === 'muy') puntaje = function (c) { return c.meta + 15 * (1 - c.bot); };
    else puntaje = null;
    let el;
    if (!puntaje) {
      const ord = cands.slice().sort(function (x, y) { return x.meta - y.meta || x.idx - y.idx; });
      el = ord[Math.floor(ord.length / 2)];
    } else {
      el = cands[0];
      for (let q = 1; q < cands.length; q++) if (puntaje(cands[q]) > puntaje(el)) el = cands[q];
    }
    const a = el.a;
    const rasgos = [];
    if (a.llaves.length) rasgos.push('llave');
    if (a.candados.length) rasgos.push('candado');
    if (a.ocultas) rasgos.push('misterio');
    if (p.cap > 4) rasgos.push('largas');
    const out = {};
    if (p.ruta === 'dia' && p.fecha) { out.id = 'dia-' + p.fecha; out.ruta = 'dia'; }
    else if (p.ruta && p.L) { out.id = p.ruta + '-' + p.L; out.ruta = p.ruta; out.L = p.L; }
    out.cap = p.cap; out.botellas = a.botellas; out.llaves = a.llaves; out.cajas = a.cajas; out.candados = a.candados;
    out.ocultas = a.ocultas; out.meta = el.meta; out.movs = el.movs; out.optimo = el.optimo;
    out.rasgos = rasgos; out.dif = p.dif || (sel === 'mediana' ? 'normal' : sel === 'facil' ? 'facil' : sel);
    if (cat) { out.bot = el.bot; out.atasco = el.atasco; }
    return out;
  }

  G.MOTOR = {
    rng: rng, hashCadena: hashCadena, nivelParams: nivelParams, difDe: difDe, rutaParams: rutaParams, diaParams: diaParams,
    racha: racha, unColor: unColor, completa: completa, ganado: ganado,
    puedeVerter: puedeVerter, verter: verter, hayJugadas: hayJugadas, estrellasDe: estrellasDe,
    clave: clave, heuristica: heuristica, jugadas: jugadas, cerrada: cerrada, prep: prep,
    resolver: resolver, pista: pista, generar: generar
  };
})(typeof globalThis !== 'undefined' ? globalThis : (typeof self !== 'undefined' ? self : this));
