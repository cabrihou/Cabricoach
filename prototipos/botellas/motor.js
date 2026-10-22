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

  const MAXBOT = 15; // tope de botellas del tablero

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


  /* ---------- el camino (v5): un solo recorrido, grado sorteado por nivel y receta por grado ---------- */

  const DIFS = ['facil', 'normal', 'dificil', 'muy', 'extra'];
  // [nivel, mecanica]: en ese nivel se estrena (siempre Facil o Normal, y con la Novedad en la interfaz)
  // v4: nada cerrado viene vacio. L4 candado (con liquido), L7 llave con caja de una botella, L12 cajon de dos
  // botellas (con un color nuevo adentro), L30 botella gigante.
  const ESTRENOS = [[4, 'candado'], [7, 'cajaUna'], [12, 'cajon'], [20, 'mistLeve'], [25, 'largas'],
                    [30, 'gigante'], [35, 'mistTotal'], [50, 'dosCajas'], [80, 'cadena']];
  function estrenoDe(L) {
    for (let i = 0; i < ESTRENOS.length; i++) if (ESTRENOS[i][0] === L) return ESTRENOS[i][1];
    return null;
  }
  function antesDeEstreno(L) { return estrenoDe(L + 1) !== null; }

  /* ---------- LA RECETA: lo unico que define como es un nivel de cada grado ----------
     Un nivel sale de (L, grado) sin diseñarlo a mano; para subir o bajar un grado se toca solo esta tabla.
       dc        desfase de colores sobre coloresBase(L) (siempre entre 3 y 12, y el tope de 15 botellas lo cuida topar)
       pruebas   [min, max] de mecanicas distintas (candado, familia de cajas, misterio) entre las ya estrenadas;
                 Extra pide todas las que haya
       mist      como sale el misterio cuando le toca: 'leve' siempre leve, 'auto' total desde L35 (leve antes),
                 'aVeces' total la mitad de las veces desde L35, 'siempre' total y obligatorio (Extra)
       hondo     que tan enterrada va la llave (0 = cerca de la tapa, 1 = lo mas hondo posible)
       cuantos   candidatos que se arman y se prueban en el catalogo (en vivo son 4)
       franja    donde debe caer el candidato elegido: bot = [min, max] de la fraccion de partidas que gana el
                 jugador simulado (jugarBot), atasco = minimo de la fraccion que se queda sin jugadas
                 (el atasco es la medida de "te puedes quedar sin salida a ciegas").
       topes     topes del solver en vivo [A* optimo, A* ponderado, dfs]: los grados duros tienen mas colores y
                 necesitan mas margen para no caer al "sin resolver", dentro de sus 5 s.
     Las franjas son punto de partida calibrado con el catalogo real (ver INFORME-NIVELES.md). */
  const RECETA = {
    facil:   { dc: -1, pruebas: [0, 1], mist: 'leve',    hondo: 0,   cuantos: 8,  franja: { bot: [0.55, 1],    atasco: 0 },    topes: [12000, 40000, 30000] },
    normal:  { dc: 0,  pruebas: [1, 1], mist: 'leve',    hondo: 0.5, cuantos: 10, franja: { bot: [0.1, 0.599], atasco: 0 },    topes: [12000, 40000, 30000] },
    dificil: { dc: 1,  pruebas: [1, 2], mist: 'auto',    hondo: 1,   cuantos: 8,  franja: { bot: [0, 0.249],   atasco: 0.3 },  topes: [12000, 40000, 30000] },
    muy:     { dc: 2,  pruebas: [2, 3], mist: 'aVeces',  hondo: 1,   cuantos: 12, franja: { bot: [0, 0.05],    atasco: 0.5 },  topes: [20000, 60000, 60000] },
    extra:   { dc: 3,  pruebas: [9, 9], mist: 'siempre', hondo: 1,   cuantos: 16, franja: { bot: [0, 0],       atasco: 0.65 }, topes: [20000, 60000, 60000] }
  };
  const CANDIDATOS_VIVO = 4, PARTIDAS_CATALOGO = 40, PARTIDAS_VIVO = 20;

  /* ---------- sorteo del grado ----------
     Pesos [Facil, Normal, Dificil, Muy, Extra] por tramo de nivel. El que sube la dureza del juego es esta tabla:
     "duros" = Dificil + Muy + Extra. Extra no sale antes de L36 (el misterio total se estrena en L35).
     Los pesos se calibraron con la meta de reparto de los 200 (duros >= 45 %, desde L81 >= 55 %, al menos 15
     Extra, primer Muy antes de L25, primer Extra entre L36 y L50). Los respiros obligatorios (tras Muy/Extra y
     tras dos duros) se comen parte de los duros, por eso los pesos duros son mas altos que el reparto real. */
  function pesosDif(L) {
    return tramo([[1, [100, 0, 0, 0, 0]], [4, [50, 50, 0, 0, 0]], [11, [17, 22, 29, 16, 0]],
                  [36, [13, 20, 31, 14, 21]], [81, [3, 15, 41, 23, 12]], [201, [3, 15, 40, 22, 20]]], L);
  }
  function esDuro(d) { return d === 'dificil' || d === 'muy' || d === 'extra'; }
  // Se sortea en orden desde L=1 porque cada nivel depende de los anteriores (por eso se memoriza).
  // Cada nivel usa su propio rng('dif:'+L): el resultado no depende de cuantos se hayan pedido antes.
  // Reglas: maximo dos duros seguidos; tras dos duros, o tras un Muy o un Extra, respiro (Facil o Normal);
  // el estreno y su vispera no son duros; nunca cuatro Faciles seguidos despues de L10.
  const MEMO_DIF = [null];
  function sortearDif(L) {
    const p1 = MEMO_DIF[L - 1], p2 = MEMO_DIF[L - 2], p3 = MEMO_DIF[L - 3];
    const w = pesosDif(L).slice();
    const respiro = (esDuro(p1) && esDuro(p2)) || p1 === 'muy' || p1 === 'extra' || estrenoDe(L) || antesDeEstreno(L);
    if (respiro) { w[2] = 0; w[3] = 0; w[4] = 0; }
    if (L > 10 && p1 === 'facil' && p2 === 'facil' && p3 === 'facil') w[0] = 0;
    let tot = 0; w.forEach(function (x) { tot += x; });
    let x = rng('dif:' + L)() * tot, d = DIFS[0];
    for (let i = 0; i < DIFS.length; i++) { x -= w[i]; if (x < 0) { d = DIFS[i]; break; } }
    return d;
  }
  function difDe(L) {
    L = Math.max(1, Math.floor(L) || 1);
    for (let k = MEMO_DIF.length; k <= L; k++) MEMO_DIF[k] = sortearDif(k);
    return MEMO_DIF[L];
  }

  // Etapa: colores de base segun L (3 en L1 a 11 desde L141); el grado le suma su desfase
  function coloresBase(L) { return tramo([[1, 3], [3, 4], [6, 5], [13, 6], [26, 7], [46, 8], [71, 9], [101, 10], [141, 11]], L); }

  // Parametros de un nivel del camino (L >= 1, sin tope): sortear el grado y aplicarle la receta.
  // Misma forma que rutaParams, mas id, dif y estreno.
  function nivelParams(L) {
    L = Math.max(1, Math.floor(L) || 1);
    const dif = difDe(L), idx = DIFS.indexOf(dif), rec = RECETA[dif], estreno = estrenoDe(L);
    const R = rng('mec:' + L);
    const n = Math.max(3, Math.min(12, coloresBase(L) + rec.dc));
    const p = { ruta: 'camino', L: L, id: 'camino-' + L, n: n, vacias: 2, cap: 4, misterio: 0, cajas: [], candados: [], cadena: false,
                hondo: rec.hondo, dif: dif, estreno: estreno,
                seleccion: ['facil', 'mediana', 'dificil', 'muy', 'extra'][idx], cuantos: rec.cuantos, franja: rec.franja, topes: rec.topes };
    const largas = function () { p.cap = 6; p.n = Math.max(4, Math.min(6, n - 3)); };
    if (estreno) {
      // el estreno va solo y limpio: la mecanica nueva es lo unico distinto del nivel
      if (estreno === 'candado') p.candados = [CAND_LIQ];
      else if (estreno === 'cajaUna') p.cajas = [cajaLiq(1)];
      else if (estreno === 'cajon') p.cajas = [cajaLiq(2)];
      else if (estreno === 'mistLeve') p.misterio = 1;
      else if (estreno === 'largas') largas();
      else if (estreno === 'gigante') p.gigante = true;
      else if (estreno === 'mistTotal') p.misterio = 2;
      else if (estreno === 'dosCajas') p.cajas = [cajaLiq(2), cajaLiq(1)];
      else if (estreno === 'cadena') { p.cajas = [cajaLiq(1), cajaLiq(2)]; p.cadena = true; }
    } else {
      aplicarPruebas(p, L, idx, rec, R);
    }
    return topar(p);
  }

  // Las pruebas del grado: cuantas mecanicas ya estrenadas lleva y cuales (cada una solo desde su estreno).
  // Mecanicas: 'c' candado (L4), 'x' familia de cajas (L7; cajon de 2 desde L12, dos cajas desde L50 y cadena
  // desde L80 solo en grados duros) y 'm' misterio (L20). Una sola familia de cajas por nivel.
  function aplicarPruebas(p, L, idx, rec, R) {
    // largas: solas y solo en Facil/Normal
    if (L >= 25 && idx <= 1 && R() < 0.12) { p.cap = 6; p.n = Math.max(4, Math.min(6, p.n - 3)); return; }
    const kinds = [];
    if (L >= 4) kinds.push('c');
    if (L >= 7) kinds.push('x');
    if (L >= 20) kinds.push('m');
    let cuantas = rec.pruebas[0] + (rec.pruebas[1] > rec.pruebas[0] ? Math.floor(R() * (rec.pruebas[1] - rec.pruebas[0] + 1)) : 0);
    // Normal: a veces 0 (15 %) para que no todos los Normales lleven prueba
    if (idx === 1 && R() < 0.15) cuantas = 0;
    barajar(kinds, R);
    let elegidas;
    if (rec.mist === 'siempre' && L >= 20) {
      // Extra: el misterio total va siempre (primero en la lista) y las demas pruebas, todas las que haya
      const orden = ['m'].concat(kinds.filter(function (k) { return k !== 'm'; }));
      elegidas = orden.slice(0, Math.min(cuantas, orden.length));
    } else {
      elegidas = kinds.slice(0, Math.min(cuantas, kinds.length));
    }
    const tiene = function (k) { return elegidas.indexOf(k) >= 0; };
    if (tiene('c')) p.candados.push(CAND_LIQ);
    if (tiene('x')) {
      const cajon = function () { return L >= 12 && R() < 0.85 ? 2 : 1; };
      // en los duros las formas de cajas mas complejas salen mas (dos cajas L50+, cadena L80+)
      const r = R();
      if (idx >= 2 && L >= 80 && r < 0.35) { p.cajas.push(cajaLiq(1), cajaLiq(2)); p.cadena = true; }
      else if (idx >= 2 && L >= 50 && r < 0.7) p.cajas.push(cajaLiq(cajon()), cajaLiq(idx >= 2 && R() < 0.5 ? 2 : 1));
      else p.cajas.push(cajaLiq(cajon()));
    }
    if (tiene('m')) {
      const total = L >= 35 && (rec.mist === 'auto' || rec.mist === 'siempre' || (rec.mist === 'aVeces' && R() < 0.5));
      p.misterio = total ? 2 : 1;
    }
    // la botella gigante aparece de vez en cuando (no con largas)
    if (L > 30 && R() < 0.15) p.gigante = true;
  }

  // 15 botellas como tope: n colores + 2 vacias libres. La gigante cuenta como una de las n.
  function topar(p) {
    let k = p.candados.length;
    p.cajas.forEach(function (c) { k += c.bots; });
    while (p.n + 2 > MAXBOT) p.n--;
    if (p.gigante && p.n - k - 1 < 1) p.gigante = false;
    p.vacias = 2;
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
     Capacidad por botella (botella gigante): C.caps[i] es la capacidad de la botella i (si falta,
       C.cap) y C.u las capas que tiene cada color (si falta, C.cap). Una botella esta completa cuando
       tiene las u capas de un solo color, aunque le sobre espacio (la gigante de 10 se completa con 4).
     Atajos: C puede ser un numero (solo cap) y E un arreglo de botellas (nada abierto).
     Un objeto de nivel completo (el que devuelve generar) sirve tal cual como C. */
  const MAXC = 4;
  const CACHE = typeof WeakMap !== 'undefined' ? new WeakMap() : null;
  function compilar(C) {
    const P = { esP: true, cap: C.cap, u: C.u || C.cap, caps: C.caps || null, llaves: C.llaves || [], cajas: C.cajas || [], candados: C.candados || [], cierre: [], porColor: [], llaveEn: [] };
    P.cajas.forEach(function (cj, c) { cj.bots.forEach(function (i) { P.cierre[i] = (P.cierre[i] || 0) | (1 << c); }); });
    P.candados.forEach(function (cd, d) {
      const bit = 1 << (MAXC + d);
      P.cierre[cd.b] = (P.cierre[cd.b] || 0) | bit;
      P.porColor[cd.color] = (P.porColor[cd.color] || 0) | bit;
    });
    P.llaves.forEach(function (ll, q) { (P.llaveEn[ll.b] = P.llaveEn[ll.b] || []).push({ k: ll.k, bit: 1 << ll.caja, caja: ll.caja, q: q }); });
    P.simple = !P.llaves.length && !P.cajas.length && !P.candados.length && !P.caps;
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
  function capDe(P, i) { return (P.caps && P.caps[i]) || P.cap; }
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
  // u = capas por color: completa es tener todas las de un color juntas
  function ganadoB(b, u) {
    // las cerradas tambien cuentan: una caja con liquido adentro no deja ganar
    for (let i = 0; i < b.length; i++) if (b[i].length && !completa(b[i], u)) return false;
    return true;
  }
  function puedeV(b, ab, i, j, P) {
    if (i === j) return false;
    const a = b[i], d = b[j];
    if (!a || !d || !a.length || completa(a, P.u)) return false;
    if (d.length >= capDe(P, j)) return false;
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
    const a = b[i], d = b[j];
    const color = a[a.length - 1];
    const cantidad = Math.min(racha(a), capDe(P, j) - d.length);
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
    if (P.porColor[color] && completa(nd, P.u)) {
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
  function ganado(E, C) { return ganadoB(nE(E).b, prep(C).u); }
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
    // una botella de otra capacidad no es intercambiable con las normales
    if (P.caps && P.caps[i] && P.caps[i] !== P.cap) t += '^' + P.caps[i];
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
    const out = [], origenes = {}, u = P.u;
    for (let i = 0; i < b.length; i++) {
      const a = b[i];
      if (!a.length || completa(a, u)) continue;
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
      if (ganadoB(n.s, P.u)) {
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
    const u = P.u;
    function rec(s, ab, prof) {
      if (ganadoB(s, u)) return true;
      if (++nodos > tope || prof > 300) return false;
      const js = jugadasP(s, ab, P);
      const pun = js.map(function (m) {
        const d = s[m[1]];
        const r = vert(s, ab, m[0], m[1], P);
        let sc = 0;
        if (completa(r.b[m[1]], u)) sc -= 100;
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
    if (ganadoB(e.b, P.u)) return { movs: [], largo: 0, optimo: true, nodos: 0 };
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
  // v4: nada cerrado viene vacio (toda botella de caja o con candado trae liquido), siempre 2 vacias
  // libres, colores nuevos escondidos en lo cerrado (si suma 8 capas o mas) y botella gigante opcional.
  const CAP_GIGANTE = 10;
  function armar(p, R) {
    const u = p.cap, n = p.n;                     // u = capas por color; las botellas normales caben u
    const cajasP = p.cajas || [], candP = p.candados || [];
    const conG = !!p.gigante;
    let nCerr = candP.length;
    cajasP.forEach(function (c) { nCerr += c.bots; });
    // 1) papeles de cada botella (todavia sin contenido): gigante, cajas y candados
    const pool = [];
    for (let i = 0; i < n; i++) pool.push(i);
    barajar(pool, R);
    let G = -1;
    if (conG) { if (n - nCerr - 1 < 1) return null; G = pool.pop(); }
    const enCaja = [];
    for (let i = 0; i < n; i++) enCaja.push(-1);
    const miembros = [];
    for (let c = 0; c < cajasP.length; c++) {
      const m = [];
      for (let q = 0; q < cajasP[c].bots; q++) {
        if (!pool.length) return null;
        const i = pool.pop(); enCaja[i] = c; m.push(i);
      }
      miembros.push(m);
    }
    const candHost = [];
    for (let d = 0; d < candP.length; d++) {
      if (!pool.length) return null;
      candHost.push(pool.pop());
    }
    const esCerrada = function (i) { return enCaja[i] >= 0 || candHost.indexOf(i) >= 0; };
    // 2) contenido. Lo cerrado suma capasK capas; desde 8 capas vive ahi al menos un color entero
    // (nuevos), mezclado con capas de colores de afuera para que haya que redistribuir al abrir.
    const K = [];
    miembros.forEach(function (m) { m.forEach(function (i) { K.push(i); }); });
    candHost.forEach(function (i) { K.push(i); });
    const capasK = K.length * u;
    const nn = capasK >= 8 ? Math.max(1, Math.floor(capasK / (2 * u))) : 0;
    if (n - nn < 1) return null;
    let cont = null, nuevos = null;
    for (let t = 0; t < 60 && !cont; t++) {
      const cols = [];
      for (let c = 1; c <= n; c++) cols.push(c);
      barajar(cols, R);
      const nuevosC = cols.slice(0, nn), fuera = cols.slice(nn);
      const capasF = [];
      fuera.forEach(function (c) { for (let k = 0; k < u; k++) capasF.push(c); });
      barajar(capasF, R);
      const relleno = capasK - nn * u;
      if (relleno > capasF.length) return null;
      const cerr = capasF.slice(0, relleno);
      // un color de afuera no puede quedar entero adentro de lo cerrado: eso seria un color nuevo sin declarar
      const dentro = {};
      cerr.forEach(function (c) { dentro[c] = (dentro[c] || 0) + 1; });
      if (Object.keys(dentro).some(function (c) { return dentro[c] >= u; })) continue;
      nuevosC.forEach(function (c) { for (let k = 0; k < u; k++) cerr.push(c); });
      barajar(cerr, R);
      const resto = capasF.slice(relleno);
      const bs = [];
      for (let i = 0; i < n; i++) bs.push(null);
      K.forEach(function (i, q) { bs[i] = cerr.slice(q * u, (q + 1) * u); });
      if (G >= 0) {
        // la gigante empieza con entre u+1 y 2u capas mezcladas; lo que le sobra de mas a las libres
        // lo pierde la ultima (queda con menos capas, o vacia si la gigante toma 2u)
        const g = u + 1 + Math.floor(R() * u);
        bs[G] = resto.splice(0, g);
        const cnt = {};
        bs[G].forEach(function (c) { cnt[c] = (cnt[c] || 0) + 1; });
        let entero = false;
        Object.keys(cnt).forEach(function (c) { if (cnt[c] >= u) entero = true; });
        if (entero) continue;
      }
      let pos = 0;
      for (let i = 0; i < n; i++) if (bs[i] === null) { bs[i] = resto.slice(pos, pos + u); pos += u; }
      let mono = false;
      bs.forEach(function (b) { if (completa(b, u)) mono = true; }); // una botella ya resuelta regala el nivel
      if (!mono) { cont = bs; nuevos = nuevosC.slice().sort(function (a, b) { return a - b; }); }
    }
    if (!cont) return null;
    // 3) llaves: enterradas bajo al menos una capa (k <= len-2), mas hondo en las rutas dificiles.
    // La llave de una caja nunca va en esa misma caja; con cadena, la de la caja 1 va dentro de la 0.
    const llaveEn = [], llaves = [];
    for (let c = 0; c < cajasP.length; c++) {
      let hosts = [];
      if (p.cadena && c === 1) {
        hosts = miembros[0].filter(function (i) { return !llaveEn[i]; });
      } else {
        for (let i = 0; i < n; i++) if (!esCerrada(i) && i !== G && !llaveEn[i] && cont[i].length >= 2) hosts.push(i);
      }
      if (!hosts.length) return null;
      const h = hosts[Math.floor(R() * hosts.length)];
      const kmax = cont[h].length - 2;
      const k = Math.max(0, kmax - Math.floor(R() * (1 + (p.hondo || 0) * kmax)));
      llaveEn[h] = true;
      llaves.push({ b: h, k: k, caja: c });
    }
    // 4) candados: el color pedido es de afuera y no puede estar dentro de la botella cerrada
    const candados = [], usados = {};
    for (let d = 0; d < candP.length; d++) {
      const b = candHost[d], opciones = [];
      for (let c = 1; c <= n; c++) if (!usados[c] && nuevos.indexOf(c) < 0 && cont[b].indexOf(c) < 0) opciones.push(c);
      if (!opciones.length) return null;
      const color = opciones[Math.floor(R() * opciones.length)];
      usados[color] = true;
      candados.push({ b: b, color: color });
    }
    for (let v = 0; v < 2; v++) { cont.push([]); enCaja.push(-1); } // siempre 2 vacias libres
    if (cont.length > MAXBOT) return null;

    // 5) orden final: sueltas mezcladas, luego cada caja entera
    const orden = [];
    for (let i = 0; i < cont.length; i++) if (enCaja[i] < 0) orden.push(i);
    barajar(orden, R);
    const cajasOut = [];
    for (let c = 0; c < miembros.length; c++) {
      const m = miembros[c].slice();
      barajar(m, R);
      const nuevosI = [];
      for (let q = 0; q < m.length; q++) { orden.push(m[q]); nuevosI.push(orden.length - 1); }
      cajasOut.push({ bots: nuevosI });
    }
    const nuevo = [];
    orden.forEach(function (viejo, pos) { nuevo[viejo] = pos; });
    const botellas = orden.map(function (i) { return cont[i].slice(); });
    const out = {
      botellas: botellas,
      llaves: llaves.map(function (l) { return { b: nuevo[l.b], k: l.k, caja: l.caja }; }),
      cajas: cajasOut,
      candados: candados.map(function (d) { return { b: nuevo[d.b], color: d.color }; }),
      ocultas: null,
      nuevos: nuevos,
      caps: G >= 0 ? orden.map(function (i) { return i === G ? CAP_GIGANTE : u; }) : null
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
    // cap aqui son las capas por color (u): con botella gigante no es la capacidad
    const tope = 3 * meta + 20, cap = P.u;
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
  // corto a proposito (A* optimo solo si es chico, luego ponderado). Los de vivo salen de la RECETA del grado
  // (los duros tienen mas colores y mas margen; Muy y Extra entran en ~5 s, los demas en ~2 s).
  const TOPES_CATALOGO = [400000, 400000, 400000];
  const TOPES_RAPIDO = [12000, 40000, 30000];

  // Que tan lejos queda un candidato de la franja de su grado (0 = dentro). Suma de lo que se pasa o le falta.
  function distanciaFranja(c, f) {
    return Math.max(0, f.bot[0] - c.bot) + Math.max(0, c.bot - f.bot[1]) + Math.max(0, f.atasco - c.atasco);
  }

  // opts.modo: 'catalogo' (candidatos de la receta, 40 partidas del bot) o 'rapido' (4 candidatos, 20 partidas).
  // En los dos se mide el bot y el atasco: es barato frente al solver y la franja del grado decide la eleccion.
  // Determinista por semilla y modo: todo el azar sale de rng(seedStr) y de las semillas 'bot:...'.
  function generar(p, seedStr, opts) {
    opts = opts || {};
    const cat = opts.modo === 'catalogo';
    const R = rng(seedStr);
    const dif = p.dif || (p.seleccion === 'mediana' ? 'normal' : p.seleccion) || 'normal';
    const rec = RECETA[dif] || RECETA.normal;
    const franja = p.franja || rec.franja;
    const cuantos = cat ? (p.cuantos || rec.cuantos) : CANDIDATOS_VIVO;
    const topes = cat ? TOPES_CATALOGO : (p.topes || rec.topes || TOPES_RAPIDO);
    const partidas = opts.partidas || (cat ? PARTIDAS_CATALOGO : PARTIDAS_VIVO);
    const cands = [];
    let intentos = 0;
    const maxInt = cat ? 800 : 150;
    while (cands.length < cuantos && intentos < maxInt) {
      intentos++;
      const a = armar(p, R);
      if (!a) continue;
      const C = { cap: p.cap, llaves: a.llaves, cajas: a.cajas, candados: a.candados };
      if (a.caps) { C.caps = a.caps; C.u = p.cap; } // botella gigante: capacidad por botella y capas por color
      const r = resolver(a.botellas, C, { topes: topes });
      if (!r || r.sinSolucion) continue;
      const c = { a: a, C: C, meta: r.largo, optimo: r.optimo, movs: r.movs, bot: 0, atasco: 0, idx: cands.length };
      const P = prep(C), Rb = rng('bot:' + seedStr + ':' + cands.length);
      let gana = 0, atasca = 0;
      for (let g = 0; g < partidas; g++) {
        const z = jugarBot(a.botellas, P, r.largo, Rb);
        if (z === 1) gana++; else if (z === -1) atasca++;
      }
      c.bot = Math.round(1000 * gana / partidas) / 1000;
      c.atasco = Math.round(1000 * atasca / partidas) / 1000;
      c.dist = distanciaFranja(c, franja);
      cands.push(c);
    }
    if (!cands.length) throw new Error('No se pudo generar ' + seedStr);
    // Eleccion por franja: entre los que caen en ella, los duros se quedan con el de mayor meta, Facil con el de
    // menor y Normal con el de en medio; si ninguno cae, el mas cercano a la franja (a igual distancia, el mismo
    // criterio de meta). El indice desempata para que la eleccion sea estable.
    const dentro = cands.filter(function (c) { return c.dist === 0; });
    const lista = dentro.length ? dentro : (function () {
      let m = Infinity;
      cands.forEach(function (c) { if (c.dist < m) m = c.dist; });
      return cands.filter(function (c) { return Math.abs(c.dist - m) < 1e-9; });
    })();
    let el;
    if (dif === 'normal') {
      const ord = lista.slice().sort(function (x, y) { return x.meta - y.meta || x.idx - y.idx; });
      el = ord[Math.floor(ord.length / 2)];
    } else {
      const quiereCorto = dif === 'facil';
      el = lista[0];
      for (let q = 1; q < lista.length; q++) {
        const mejor = quiereCorto ? lista[q].meta < el.meta : lista[q].meta > el.meta;
        if (mejor) el = lista[q];
      }
    }
    const a = el.a;
    const rasgos = [];
    if (a.llaves.length) rasgos.push('llave');
    if (a.candados.length) rasgos.push('candado');
    if (a.ocultas) rasgos.push('misterio');
    if (p.cap > 4) rasgos.push('largas');
    if (a.caps) rasgos.push('gigante');
    const out = {};
    if (p.ruta === 'dia' && p.fecha) { out.id = 'dia-' + p.fecha; out.ruta = 'dia'; }
    else if (p.ruta && p.L) { out.id = p.ruta + '-' + p.L; out.ruta = p.ruta; out.L = p.L; }
    out.cap = p.cap;
    if (a.caps) { out.caps = a.caps; out.u = p.cap; }
    out.botellas = a.botellas; out.llaves = a.llaves; out.cajas = a.cajas; out.candados = a.candados;
    out.ocultas = a.ocultas; out.nuevos = a.nuevos; out.meta = el.meta; out.movs = el.movs; out.optimo = el.optimo;
    out.rasgos = rasgos; out.dif = dif;
    out.bot = el.bot; out.atasco = el.atasco;
    return out;
  }

  /* ---------- variante para "Reiniciar": otros colores y otro orden, mismo nivel por dentro ---------- */
  // Cambiarle el nombre a los colores y el lugar a las botellas no cambia que jugadas existen: la solucion
  // del catalogo se traduce tal cual, asi que la variante tiene salida y la misma meta sin volver a resolver.
  // Las botellas de cada caja siguen juntas y al final (formato v2); adentro de la caja tambien se barajan.
  const NCOLORES = 12;
  function variante(nv, seedStr) {
    const n = nv.botellas.length;
    const enCaja = {};
    (nv.cajas || []).forEach(function (cj) { cj.bots.forEach(function (i) { enCaja[i] = 1; }); });
    const usados = {};
    nv.botellas.forEach(function (b) { b.forEach(function (c) { usados[c] = 1; }); });
    const cols = Object.keys(usados).map(Number).sort(function (a, b) { return a - b; });
    let mapaC = null, orden = null, cajas = null;
    // si el sorteo deja todo igual (pasa en niveles diminutos) se sortea otra vez: tiene que verse distinto
    for (let intento = 0; intento < 8; intento++) {
      const R = rng('var:' + seedStr + ':' + intento);
      const pal = []; for (let c = 1; c <= NCOLORES; c++) pal.push(c);
      barajar(pal, R);
      mapaC = {}; cols.forEach(function (c, q) { mapaC[c] = pal[q]; });
      orden = []; for (let i = 0; i < n; i++) if (!enCaja[i]) orden.push(i);
      barajar(orden, R);
      cajas = (nv.cajas || []).map(function (cj) {
        const m = cj.bots.slice(); barajar(m, R);
        return Object.assign({}, cj, { bots: m.map(function (viejo) { orden.push(viejo); return orden.length - 1; }) });
      });
      const mismos = cols.every(function (c) { return mapaC[c] === c; });
      if (!mismos || orden.some(function (v, i) { return v !== i; })) break;
    }
    const nuevoDe = []; orden.forEach(function (viejo, nuevo) { nuevoDe[viejo] = nuevo; });
    const o = Object.assign({}, nv);
    o.botellas = orden.map(function (v) { return nv.botellas[v].map(function (c) { return mapaC[c]; }); });
    if (nv.caps) o.caps = orden.map(function (v) { return nv.caps[v]; });
    if (nv.ocultas) o.ocultas = orden.map(function (v) { const a = nv.ocultas[v]; return a ? a.slice() : a; });
    o.llaves = (nv.llaves || []).map(function (l) { return Object.assign({}, l, { b: nuevoDe[l.b] }); });
    o.cajas = cajas;
    o.candados = (nv.candados || []).map(function (c) { return Object.assign({}, c, { b: nuevoDe[c.b], color: mapaC[c.color] }); });
    if (nv.nuevos) o.nuevos = nv.nuevos.map(function (c) { return mapaC[c]; }).sort(function (a, b) { return a - b; });
    if (nv.movs) o.movs = nv.movs.map(function (m) { return [nuevoDe[m[0]], nuevoDe[m[1]]]; });
    o.variante = String(seedStr);
    return o;
  }

  G.MOTOR = {
    rng: rng, hashCadena: hashCadena, nivelParams: nivelParams, difDe: difDe, rutaParams: rutaParams, diaParams: diaParams,
    racha: racha, unColor: unColor, completa: completa, ganado: ganado,
    puedeVerter: puedeVerter, verter: verter, hayJugadas: hayJugadas, estrellasDe: estrellasDe,
    clave: clave, heuristica: heuristica, jugadas: jugadas, cerrada: cerrada, prep: prep, capDe: function (C, i) { return capDe(prep(C), i); },
    resolver: resolver, pista: pista, generar: generar, variante: variante
  };
})(typeof globalThis !== 'undefined' ? globalThis : (typeof self !== 'undefined' ? self : this));
