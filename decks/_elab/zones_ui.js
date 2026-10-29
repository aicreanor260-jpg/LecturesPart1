/* Зоны на схеме: прямоугольник с подписью и цветом («Офис 1», «DMZ»). Перетаскивание за заголовок двигает зону вместе с устройствами
   и заметками внутри, уголок справа внизу — размер, ПКМ или двойной щелчок по заголовку — подпись, цвет, удаление.
   На работу сети не влияют; хранятся в файле схемы (zones). Работают в обоих режимах. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  var COLORS = ['#6fe3ea', '#ffc65c', '#c99bff', '#7dffb0', '#ff8a7a', '#8fb4ff'];
  function net() { return U.net(); }
  var world = document.getElementById('world'), gz = document.getElementById('gz');
  if (!gz) { gz = document.createElementNS('http://www.w3.org/2000/svg', 'g'); gz.id = 'gz'; world.insertBefore(gz, world.firstChild); }
  function Z() { var n = net(); return n.zones || (n.zones = []); }
  function inside(z, x, y) { return x >= z.x && x <= z.x + z.w && y >= z.y && y <= z.y + z.h; }
  EL.zoneInside = inside;
  var items0 = X.items, run0 = X.run;
  X.items = function (k, d) { return items0(k, d) + (k === 'field' ? '<button data-a="zone"><span>▭</span>Зона</button>' : ''); };
  X.run = function (k, a, p) { run0(k, a, p); if (k === 'field' && a === 'zone') { var L = Z(), z = { x: p.x - 40, y: p.y - 30, w: 420, h: 280, t: 'Зона ' + (L.length + 1), c: COLORS[L.length % COLORS.length] }; L.push(z); X.onDraw(); edit(z); } };
  var save0 = X.saveX, load0 = X.loadX;
  X.saveX = function (j) { save0(j); var L = Z(); if (L.length) j.zones = L; };
  X.loadX = function (j) { load0(j); net().zones = Array.isArray(j.zones) ? j.zones.filter(function (z) { return z && isFinite(z.x) && isFinite(z.w); }) : []; };
  var draw0 = X.onDraw;
  X.onDraw = function () { draw0(); paint(); };
  function paint() {
    gz.innerHTML = '';
    Z().forEach(function (z) {
      var g = U.el('g', { 'class': 'zone' + (z.min ? ' min' : ''), transform: 'translate(' + z.x + ',' + z.y + ')', style: '--zc:' + z.c }, gz);
      if (z.min) return;
      U.el('rect', { 'class': 'zb', x: 0, y: 0, width: z.w, height: z.h, rx: 6 }, g);
      var hw = Math.min(z.w, String(z.t).length * 9.5 + 34), h = U.el('g', { 'class': 'zh' }, g);
      U.el('rect', { x: 0, y: 0, width: hw, height: 26, rx: 4 }, h); U.el('text', { x: 12, y: 18 }, h).textContent = z.t;
      var rs = U.el('path', { 'class': 'zr', d: 'M' + (z.w - 16) + ' ' + z.h + ' L' + z.w + ' ' + (z.h - 16) + ' L' + z.w + ' ' + z.h + ' Z' }, g);
      h.addEventListener('mousedown', function (e) { e.stopPropagation(); if (e.button === 0) drag(e, z); });
      h.addEventListener('dblclick', function (e) { e.stopPropagation(); edit(z); });
      h.addEventListener('contextmenu', function (e) { e.preventDefault(); e.stopPropagation(); edit(z); });
      rs.addEventListener('mousedown', function (e) { e.stopPropagation(); if (e.button === 0) resize(e, z); });
    });
  }
  // зона тянет за собой всё, что было внутри в момент нажатия
  function drag(e, z) {
    var n = net(), p0 = U.toWorld(e.clientX, e.clientY), x0 = z.x, y0 = z.y;
    var D = n.list().filter(function (d) { return inside(z, d.x, d.y); }).map(function (d) { return { o: d, x: d.x, y: d.y }; });
    var N = (n.notes || []).filter(function (o) { return inside(z, o.x, o.y); }).map(function (o) { return { o: o, x: o.x, y: o.y }; });
    var moved = false;
    function mv(ev) { var p = U.toWorld(ev.clientX, ev.clientY), dx = p.x - p0.x, dy = p.y - p0.y; if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
      z.x = x0 + dx; z.y = y0 + dy; D.concat(N).forEach(function (q) { q.o.x = q.x + dx; q.o.y = q.y + dy; }); U.draw(); }
    function up() { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up);
      if (moved) D.forEach(function (q) { X.rec({ k: 'move', name: q.o.name, x: q.x, y: q.y }); }); }
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  }
  function resize(e, z) {
    var p0 = U.toWorld(e.clientX, e.clientY), w0 = z.w, h0 = z.h;
    function mv(ev) { var p = U.toWorld(ev.clientX, ev.clientY); z.w = Math.max(160, w0 + p.x - p0.x); z.h = Math.max(110, h0 + p.y - p0.y); paint(); }
    function up() { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); }
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  }
  function edit(z) {
    var body = document.createElement('div'); body.className = 'pad zonew';
    body.innerHTML = '<label>Подпись</label><input class="q" data-f="t" value="' + esc(z.t) + '" maxlength="40"><label>Цвет</label><div class="zcol">' +
      COLORS.map(function (c) { return '<button data-col="' + c + '" style="background:' + c + '"' + (c === z.c ? ' class="on"' : '') + '></button>'; }).join('') + '</div>' +
      '<div class="row">' + (EL.zoneExtra ? EL.zoneExtra(z) : '') + '<button class="pri" data-c="ok">Сохранить</button><button data-c="del">Удалить зону</button></div>' +
      '<p class="cs2">Удаляется только рамка — устройства остаются на схеме.</p>';
    U.closeWin('zone', true); U.makeWin('zone', 'Зона', z.t, body, { w: 360, h: 280 });
    var col = z.c, inp = body.querySelector('[data-f="t"]'); inp.focus(); inp.select();
    body.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter') body.querySelector('[data-c="ok"]').click(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return;
      if (b.dataset.col) { col = b.dataset.col; [].forEach.call(body.querySelectorAll('[data-col]'), function (x) { x.classList.toggle('on', x === b); }); return; }
      if (b.dataset.c === 'ok') { z.t = inp.value.trim() || z.t; z.c = col; }
      if (b.dataset.c === 'del') { net().zones = Z().filter(function (x) { return x !== z; }); }
      if (b.dataset.zx && EL.zoneAct) EL.zoneAct(z, b.dataset.zx);
      U.closeWin('zone', true); U.draw(); });
  }
  // ---------------------------------------------------------------- кластеры: свёрнутая зона — один значок, кабели наружу идут от него
  var gc = document.getElementById('gc');
  if (!gc) { gc = document.createElementNS('http://www.w3.org/2000/svg', 'g'); gc.id = 'gc'; world.insertBefore(gc, document.getElementById('pk')); }
  function members(z) { var n = net(); return (z.members || []).map(function (nm) { return n.byName(nm); }).filter(Boolean); }
  function ctr(z) { return { x: z.x + 70, y: z.y + 44 }; }
  X.preDraw = function () { var keep = [];
    Z().forEach(function (z) { if (!z.min) return; var c = ctr(z); members(z).forEach(function (d) { keep.push([d, d.x, d.y]); d.x = c.x; d.y = c.y; }); });
    return keep.length ? function () { keep.forEach(function (k) { k[0].x = k[1]; k[0].y = k[2]; }); } : null; };
  function collapse(z, on) {
    if (on) { z.members = net().list().filter(function (d) { return inside(z, d.x, d.y); }).map(function (d) { return d.name; }); z.min = true; }
    else { z.min = false; delete z.members; }
  }
  EL.zoneExtra = function (z) { return '<button data-zx="toggle">' + (z.min ? 'Развернуть' : 'Свернуть в значок') + '</button>'; };
  EL.zoneAct = function (z, a) { if (a === 'toggle') collapse(z, !z.min); };
  function hideInner() { var n = net();
    Z().forEach(function (z) { if (!z.min) return; var ids = {}; members(z).forEach(function (d) { ids[d.id] = 1; });
      Object.keys(ids).forEach(function (id) { var g = document.querySelector('#gd g.dev[data-id="' + id + '"]'); if (g) g.style.display = 'none'; });
      n.links.forEach(function (l, i) { if (!(ids[l.a.dev] && ids[l.b.dev])) return;
        var ln = document.querySelector('#gl [data-li="' + i + '"]'); if (ln) ln.style.display = 'none';
        [l.a.dev + '|' + l.a.port, l.b.dev + '|' + l.b.port].forEach(function (k) { [].forEach.call(document.querySelectorAll('#gp [data-dp="' + k + '"]'), function (x) { x.style.display = 'none'; }); }); }); }); }
  function paintClusters() { gc.innerHTML = ''; hideInner();
    Z().forEach(function (z) { if (!z.min) return; var c = ctr(z), M = members(z), g = U.el('g', { 'class': 'clu', transform: 'translate(' + c.x + ',' + c.y + ')', style: '--zc:' + z.c }, gc);
      U.el('rect', { x: -66, y: -38, width: 132, height: 76, rx: 10 }, g);
      [[-30, -6], [0, -14], [30, -6]].forEach(function (q) { U.el('circle', { cx: q[0], cy: q[1], r: 9 }, g); });
      U.el('path', { d: 'M-30 -6 L0 -14 L30 -6 M-30 -6 L30 -6', 'class': 'cl' }, g);
      U.el('text', { y: 18, 'class': 'ct' }, g).textContent = M.length + ' устр.';
      U.el('text', { y: 54, 'class': 'lbl' }, g).textContent = z.t;
      var t = U.el('title', {}, g); t.textContent = z.t + ': ' + M.map(function (d) { return d.name; }).join(', ') + ' — двойной щелчок: развернуть';
      g.addEventListener('mousedown', function (e) { e.stopPropagation(); if (e.button === 0) dragC(e, z); });
      g.addEventListener('dblclick', function (e) { e.stopPropagation(); collapse(z, false); U.draw(); });
      g.addEventListener('contextmenu', function (e) { e.preventDefault(); e.stopPropagation(); edit(z); }); }); }
  function dragC(e, z) { var p0 = U.toWorld(e.clientX, e.clientY), x0 = z.x, y0 = z.y, D = members(z).map(function (d) { return { o: d, x: d.x, y: d.y }; });
    function mv(ev) { var p = U.toWorld(ev.clientX, ev.clientY); z.x = x0 + p.x - p0.x; z.y = y0 + p.y - p0.y; D.forEach(function (q) { q.o.x = q.x + p.x - p0.x; q.o.y = q.y + p.y - p0.y; }); U.draw(); }
    function up() { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); }
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up); }
  var draw1 = X.onDraw; X.onDraw = function () { draw1(); paintClusters(); };
  EL.zones = { list: Z, paint: paint, edit: edit, inside: inside, collapse: collapse };
})();
