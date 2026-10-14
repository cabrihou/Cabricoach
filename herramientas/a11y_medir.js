(() => {
  // ---- utilidades de color ----
  const parse = (s) => { const m = String(s).match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const blend = (f, b) => ({ r: f.r * f.a + b.r * (1 - f.a), g: f.g * f.a + b.g * (1 - f.a), b: f.b * f.a + b.b * (1 - f.a), a: 1 });
  const lum = (c) => { const ch = [c.r, c.g, c.b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]; };
  const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
  const bodyBg = parse(getComputedStyle(document.body).backgroundColor) || { r: 11, g: 13, b: 15, a: 1 };
  // fondo efectivo: compone fondos semitransparentes hacia arriba; si hay gradiente o imagen, lo marca
  function fondo(el) {
    const capas = []; let complejo = false;
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') { complejo = true; const m = cs.backgroundImage.match(/rgba?\([^)]+\)/g); if (m) { const c = parse(m[0]); if (c) { capas.push({ ...c, a: Math.max(c.a, 0.85) }); break; } } }
      const c = parse(cs.backgroundColor); if (c && c.a > 0) { capas.push(c); if (c.a >= 0.99) break; }
    }
    let bg = { ...bodyBg, a: 1 };
    for (let i = capas.length - 1; i >= 0; i--) bg = blend(capas[i], bg);
    return { bg, complejo };
  }
  const visible = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0.05; };
  const desc = (el) => { const t = (el.getAttribute('aria-label') || el.textContent || el.getAttribute('placeholder') || '').replace(/\s+/g, ' ').trim().slice(0, 40); return (el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '') + (t ? ' «' + t + '»' : '')); };
  const raiz = document.body;

  // ---- 1. tamaño de toque (incluye el ::after invisible que agranda el área) ----
  const inter = [...raiz.querySelectorAll('button, a[href], input:not([type=hidden]), select, textarea, [data-a], [role=button], [role=checkbox], [role=tab], [role=switch]')].filter(visible);
  const toques = inter.map((el) => {
    const r = el.getBoundingClientRect(); let w = r.width, h = r.height;
    const af = getComputedStyle(el, '::after');
    if (af && af.content !== 'none' && af.position === 'absolute') {
      const px = (v) => (v && v.endsWith('px') ? parseFloat(v) : 0);
      const t = px(af.top), b = px(af.bottom), l = px(af.left), rr = px(af.right);
      if (t < 0 || l < 0) { w = Math.max(w, r.width - l - rr); h = Math.max(h, r.height - t - b); }
    }
    return { d: desc(el), w: Math.round(w), h: Math.round(h) };
  });
  const bajo44 = toques.filter((t) => t.w < 44 || t.h < 44), bajo24 = toques.filter((t) => t.w < 24 || t.h < 24);

  // ---- 2. contraste de texto (1.4.3) ----
  const textos = new Set();
  const walker = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT, { acceptNode: (n) => (n.nodeValue.trim().length > 0 ? 1 : 2) });
  while (walker.nextNode()) { const p = walker.currentNode.parentElement; if (p && !p.closest('svg, script, style')) textos.add(p); }
  let revisados = 0, complejos = 0; const fallas = [];
  textos.forEach((el) => {
    if (!visible(el)) return;
    const cs = getComputedStyle(el); const fg = parse(cs.color); if (!fg) return;
    const { bg, complejo } = fondo(el); if (complejo) complejos++;
    const col = blend({ ...fg, a: fg.a * (+cs.opacity || 1) }, bg);
    const size = parseFloat(cs.fontSize), peso = +cs.fontWeight || 400;
    const grande = size >= 24 || (size >= 18.66 && peso >= 700);
    const req = grande ? 3 : 4.5, rt = ratio(col, bg); revisados++;
    if (rt < req && !complejo) fallas.push({ d: desc(el), ratio: Math.round(rt * 100) / 100, req, size: Math.round(size * 10) / 10 });
  });
  const unicas = []; const vistos = new Set();
  fallas.sort((a, b) => a.ratio - b.ratio).forEach((f) => { const k = f.d; if (!vistos.has(k)) { vistos.add(k); unicas.push(f); } });

  // ---- 3. contraste de controles (1.4.11): borde visible contra el fondo cuando el control no tiene relleno propio ----
  const ctrl = [...raiz.querySelectorAll('.chip, .in, input, select, textarea, .sdot, .tgl, .seg button, .btn.ghost, .pmbtn, .exrck, .okbtn2')].filter(visible);
  const noTexto = [];
  ctrl.forEach((el) => {
    const cs = getComputedStyle(el); const bw = parseFloat(cs.borderTopWidth) || 0;
    const { bg: afuera } = fondo(el.parentElement || el);
    const propio = parse(cs.backgroundColor); const relleno = propio && propio.a > 0 ? blend(propio, afuera) : afuera;
    const rRelleno = ratio(relleno, afuera);
    if (rRelleno >= 3) return; // el relleno ya lo distingue
    const bc = parse(cs.borderTopColor);
    const rBorde = bw > 0 && bc ? ratio(blend(bc, afuera), afuera) : 1;
    if (rBorde < 3) noTexto.push({ d: desc(el), borde: Math.round(rBorde * 100) / 100, relleno: Math.round(rRelleno * 100) / 100 });
  });
  const ctrlUnicos = []; const v2 = new Set(); noTexto.forEach((x) => { const k = x.d.split(' «')[0]; if (!v2.has(k)) { v2.add(k); ctrlUnicos.push(x); } });

  // ---- 4. teclado: [data-a] que no se alcanzan con Tab ----
  const dataA = [...raiz.querySelectorAll('[data-a]')].filter(visible);
  const noTab = dataA.filter((el) => !['BUTTON', 'A', 'INPUT', 'SELECT', 'TEXTAREA', 'LABEL'].includes(el.tagName) && !(el.tabIndex >= 0 && el.hasAttribute('tabindex')));

  // ---- 5. estructura: titulos y regiones ----
  const heads = [...document.querySelectorAll('#view h1, #view h2, #view h3, #view h4')].filter(visible).map((h) => h.tagName + ' ' + h.textContent.replace(/\s+/g, ' ').trim().slice(0, 30));
  const titulosFalsos = [...document.querySelectorAll('#view .ttl, #view .mod-head .ttl, #view .lbl')].filter(visible).length;
  const regiones = { main: !!document.querySelector('main, [role=main]'), nav: !!document.querySelector('nav, [role=navigation]'), header: !!document.querySelector('header, [role=banner]') };

  // ---- 6. imagenes y campos ----
  const imgs = [...raiz.querySelectorAll('img')].filter(visible);
  const imgVacio = imgs.filter((i) => i.getAttribute('alt') === '').length, imgSin = imgs.filter((i) => !i.hasAttribute('alt')).length;
  const campos = [...raiz.querySelectorAll('input:not([type=hidden]), select, textarea')].filter(visible);
  const sinNombre = campos.filter((c) => !c.getAttribute('aria-label') && !c.getAttribute('aria-labelledby') && !(c.id && document.querySelector('label[for="' + c.id + '"]')) && !c.closest('label')).map((c) => desc(c));

  // ---- 7. estado de controles (4.1.2) ----
  const tgl = [...raiz.querySelectorAll('.tgl')].filter(visible), tglEstado = tgl.filter((t) => t.hasAttribute('aria-pressed') || t.hasAttribute('aria-checked')).length;
  const segs = [...raiz.querySelectorAll('.seg button, .xtabs button, [data-a=foodSub], [data-a=trainSub]')].filter(visible), segEstado = segs.filter((t) => t.hasAttribute('aria-pressed') || t.hasAttribute('aria-selected') || t.getAttribute('aria-current')).length;

  return JSON.stringify({
    interactivos: toques.length, bajo44: bajo44.length, bajo24: bajo24.length,
    ejemplos24: bajo24.slice(0, 8), ejemplos44: bajo44.filter((t) => t.w >= 24 && t.h >= 24).slice(0, 8),
    textosRevisados: revisados, textosSobreGradiente: complejos, fallasContraste: unicas.length, peoresContraste: unicas.slice(0, 10),
    controlesSinContraste: ctrlUnicos.length, ejemplosControles: ctrlUnicos.slice(0, 8),
    dataA: dataA.length, dataANoTab: noTab.length, ejemplosNoTab: noTab.slice(0, 6).map(desc),
    titulos: heads, titulosQueNoSonTitulo: titulosFalsos, regiones,
    imagenes: imgs.length, imgAltVacio: imgVacio, imgSinAlt: imgSin,
    campos: campos.length, camposSinNombre: sinNombre.slice(0, 6), nCamposSinNombre: sinNombre.length,
    interruptores: tgl.length, interruptoresConEstado: tglEstado, segmentados: segs.length, segmentadosConEstado: segEstado,
  });
})()
