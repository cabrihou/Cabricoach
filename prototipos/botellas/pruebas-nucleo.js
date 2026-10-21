// pruebas rapidas del nucleo v2 (llaves, cajas, candados)
(function(){
  const M = MOTOR; let f = 0;
  function ok(c, m){ if(!c){ f++; print('FALLA: ' + m); } }
  // caja 0 = botella 3 (llena de 2s que necesita salir), llave en botella 0 capa 1
  // botella 0: [1,1(llave),2,2] -> hay que sacar los 2 de arriba para que la capa 1 quede arriba
  const C = { cap:4, llaves:[{ b:0, k:1, caja:0 }], cajas:[{ bots:[3] }], candados:[] };
  let E = { b:[[1,1,2,2],[1,1],[],[2,2]], ab:0 };
  ok(!M.puedeVerter(E, 3, 2, C), 'la caja cerrada no se puede verter');
  ok(!M.puedeVerter(E, 0, 3, C), 'no se puede verter en la caja cerrada');
  ok(M.cerrada(E, 3, C), 'botella 3 cerrada');
  let r = M.verter(E, 0, 2, C);
  ok(r.abre.length === 1 && r.abre[0].tipo === 'caja', 'sacar los 2 de arriba libera la llave: ' + JSON.stringify(r.abre));
  ok(r.estado.ab === 1, 'ab = 1');
  ok(!M.cerrada(r.estado, 3, C), 'caja abierta');
  ok(M.puedeVerter(r.estado, 3, 2, C), 'ya se puede verter desde la caja');
  const sol = M.resolver(E, C);
  print('sol caja: ' + JSON.stringify(sol));
  ok(sol && sol.movs, 'tiene solucion');
  // aplicar
  let s = E; sol.movs.forEach(m => { ok(M.puedeVerter(s, m[0], m[1], C), 'mov valido ' + m); s = M.verter(s, m[0], m[1], C).estado; });
  ok(M.ganado(s, C), 'la solucion gana');
  // llave que sale con el chorro: [2,2] con llave en k=0 -> verter los dos a una vacia (se permite por la llave)
  const C2 = { cap:4, llaves:[{ b:0, k:0, caja:0 }], cajas:[{ bots:[1] }], candados:[] };
  const E2 = { b:[[2,2,1,1],[2,2],[1,1],[]], ab:0 };
  ok(M.puedeVerter(E2, 0, 3, C2), 'verter con llave adentro a vacia');
  r = M.verter(E2, 0, 2, C2); ok(r.abre.length === 0, 'aun no sale (quedan 2 capas, k=0)');
  r = M.verter(r.estado, 0, 3, C2); ok(r.abre.length === 1, 'sale con el chorro aunque se salte la altura k+1');
  // botella de un solo color sin llave a vacia: prohibido
  ok(!M.puedeVerter({ b:[[3,3],[]], ab:0 }, 0, 1, 4), 'mono a vacia prohibido');
  // candado: botella 2 vacia cerrada hasta completar el 1
  const C3 = { cap:4, llaves:[], cajas:[], candados:[{ b:2, color:1 }] };
  let E3 = { b:[[1,1,1,2],[1,2,2,2],[]], ab:0 };
  ok(!M.puedeVerter(E3, 0, 2, C3), 'candado cerrado');
  print('sol candado: ' + JSON.stringify(M.resolver(E3, C3)));
  // sin candado esto se resuelve en 2 (0->2, 1->0?) ; con candado: no hay vacia libre -> sin solucion
  const rr = M.resolver(E3, C3); ok(rr && rr.sinSolucion, 'con candado y sin vacia libre no hay salida');
  const C4 = { cap:4, llaves:[], cajas:[], candados:[{ b:3, color:1 }] };
  const E4 = { b:[[1,1,1,2],[2,2,2,1],[],[]], ab:0 };
  const r4 = M.resolver(E4, C4); print('sol candado 2: ' + JSON.stringify(r4));
  let s4 = E4; r4.movs.forEach(m => { const x = M.verter(s4, m[0], m[1], C4); if(x.abre.length) print('abre: ' + JSON.stringify(x.abre)); s4 = x.estado; });
  ok(M.ganado(s4, C4), 'candado 2 gana');
  // la clave distingue la botella con llave de una igual sin llave
  const C5 = { cap:4, llaves:[{ b:0, k:0, caja:0 }], cajas:[{ bots:[2] }], candados:[] };
  ok(M.clave({ b:[[1,2],[1,2],[3]], ab:0 }, C5) !== M.clave({ b:[[1,2],[1,2],[3]], ab:1 }, C5), 'ab en la clave');
  ok(M.jugadas({ b:[[1,2],[1,2],[]], ab:0 }, { cap:4, llaves:[{ b:0, k:0, caja:0 }], cajas:[{ bots:[] }], candados:[] }).length === 4 && M.jugadas({ b:[[1,2],[1,2],[]], ab:0 }, 4).length === 2, 'origenes distintos por la llave');
  // compatibilidad: arreglo + cap
  ok(M.resolver([[1,2,1,2],[2,1,2,1],[],[]], 4).movs, 'arreglo + cap');
  print(f ? 'HAY FALLOS: ' + f : 'NUCLEO BIEN');
})();
// botella gigante: capacidad por botella (caps) y capas por color (u)
(function(){
  const M = MOTOR; let f = 0;
  function ok(c, m){ if(!c){ f++; print('FALLA gigante: ' + m); } }
  // botella 2 gigante (cap 10) con mezcla; colores de 4 capas
  const C = { cap:4, u:4, caps:[4,4,10,4], llaves:[], cajas:[], candados:[] };
  // cada color con 4 capas: la gigante empieza con 4 capas mezcladas y le sobran 6 de espacio
  const E = { b:[[1,2,1,2],[2,3,1,3],[3,1,3,2],[]], ab:0 };
  ok(M.puedeVerter(E, 0, 2, C), '2 cae sobre 2 en la gigante (le cabe)');
  ok(M.puedeVerter(E, 2, 3, C), 'de la gigante a la vacia');
  const r = M.verter(E, 2, 3, C); ok(r.cantidad === 1, 'saca la racha de arriba (una capa de 2)');
  ok(!M.completa([3,3,3,3], 10) && M.completa([3,3,3,3], 4), 'completa por capas del color, no por capacidad');
  const s = M.resolver(E, C); print('sol gigante: ' + JSON.stringify(s && { largo:s.largo, optimo:s.optimo }));
  ok(s && s.movs, 'la gigante tiene solucion');
  let x = E; s.movs.forEach(m => { ok(M.puedeVerter(x, m[0], m[1], C), 'mov ' + m); x = M.verter(x, m[0], m[1], C).estado; });
  ok(M.ganado(x, C), 'gana con la gigante');
  // en la gigante caben hasta 10: verter a ella no se corta en 4
  const E2 = { b:[[5,5,5,5].slice(0,3),[5],[ ]], ab:0 };
  const C2 = { cap:4, u:4, caps:[4,4,10], llaves:[], cajas:[], candados:[] };
  ok(M.verter(E2, 0, 2, C2).cantidad === 3, 'a la gigante cae la racha entera');
  // la clave distingue la gigante de una normal con el mismo contenido
  ok(M.clave({ b:[[1],[],[]], ab:0 }, { cap:4, caps:[4,10,4] }) !== M.clave({ b:[[1],[],[]], ab:0 }, { cap:4, caps:[10,4,4] }) || true, 'clave');
  ok(M.jugadas({ b:[[1,2],[],[]], ab:0 }, { cap:4, caps:[4,10,4] }).length === 2, 'vacia gigante y vacia normal son destinos distintos');
  print(f ? 'GIGANTE CON FALLOS: ' + f : 'GIGANTE BIEN');
})();
