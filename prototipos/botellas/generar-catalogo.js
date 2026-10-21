/* Genera un rango de niveles del camino en modo catalogo y los imprime, uno por linea en JSON.
   Uso (desde esta carpeta):
     jsc motor.js generar-catalogo.js -- 1 10
   Cada linea es el nivel v2/v3 mas "_seg" (segundos que tardo), que catalogo.py quita antes de guardar.
   jsc no escribe archivos: catalogo.py recoge la salida estandar. */
// los argumentos de jsc solo se ven en el nivel de arriba, no dentro de una funcion
const ARGS_JSC = typeof arguments !== 'undefined' ? arguments : [];
(function () {
  const desde = parseInt(ARGS_JSC[0] || '1', 10);
  const hasta = parseInt(ARGS_JSC[1] || String(desde), 10);
  for (let L = desde; L <= hasta; L++) {
    const t0 = Date.now();
    const nivel = MOTOR.generar(MOTOR.nivelParams(L), 'camino:' + L, { modo: 'catalogo' });
    nivel._seg = Math.round(Date.now() - t0) / 1000;
    print(JSON.stringify(nivel));
  }
})();
