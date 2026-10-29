/* Интерфейс эмулятора в стиле pnetlab: поле на весь экран, левая выезжающая панель, контекстные меню (ПКМ),
   плавающие окна терминалов/свойств/заданий, нижняя панель с кнопкой «Терминал», пошаговая трасса пакетов. */
(function () {
  'use strict';
  var EL = window.EL, $ = function (id) { return document.getElementById(id); };
  var NS = 'http://www.w3.org/2000/svg';
  // точки подключения учебных инструментов (ui_tools.js): пункты меню, undo, захват, разбор шага, заметки
  var X = EL.uiX = { rec: function () {}, delOp: function () { return null; }, linkArr: function () { return null; }, items: function () { return ''; }, run: function () {},
    undo: function () {}, side: function () { return ''; }, sideClick: function () {}, onDraw: function () {}, onTrace: function () {}, onStep: function () {}, saveX: function () {}, loadX: function () {}, onMode: function () {}, preDraw: function () { return null; },
    roomRun: function () { return false; }, roomAct: function () { return false; }, roomTab: function () { return false; }, roomPrompt: function () { return null; }, onCmd: function () {}, onOut: function () {}, siteStart: function () { return false; } };   // клиент сайта и комнат — net_ws.js
  var readOnly = false;                            // просмотр преподавателем: схема и консоли без ввода
  var msel = {}, mselL = {}, spaceDown = false;    // множественное выделение: устройства и кабели
  var net = new EL.Net(), sel = null, selLink = null, cable = null, lab = null, labP = null, labShow = false, task = null, trace = null;
  var view = { x: 0, y: 0, k: 1 }, cv = $('cv'), world = $('world');
  var terms = {}, wins = {}, z = 60;

  // ================================================================== иконки устройств (HUD)
  // Иконки можно заменить своими SVG: ICONS[тип] = function (g, d) {...}
  var ICONS = {
    mes: function (g, d) { var m = EL.MODELS[d.model] || {}, big = /агрегации|ЦОД/.test(m.group || '');
      if (m.kind === 'olt' || m.kind === 'lte') { use(g, 'ic-olt', 104); return; } if (m.kind === 'ont' || m.kind === 'eont') { use(g, 'ic-ont', 70); return; }   // OLT и ONT
      use(g, big ? 'ic-stack' : 'ic-switch', big ? 84 : 104); },
    esr: function (g, d) { var k = (EL.MODELS[d.model] || {}).kind; if (k === 'isp') { use(g, 'ic-cloud', 120); return; } use(g, k === 'scs' ? 'ic-console' : k === 'wlc' ? 'ic-wlc' : k === 'me' ? 'ic-me' : 'ic-router', k ? 100 : 96); },   // SCS-32, WLC, ME — свои иконки
    vpc: function (g, d) { var k = (EL.MODELS[d.model] || {}).kind; if (k === 'tau') { use(g, 'ic-ont', 80); return; } if (k === 'smg') { use(g, 'ic-server', 80); return; } if (k === 'phone') { use(g, 'ic-phone', 64); return; } use(g, 'ic-pc', 78); },   // TAU, SMG, телефон
    deb: function (g, d) { if ((EL.MODELS[d.model] || {}).kind === 'ap') { use(g, 'ic-ap', 84); return; }
      use(g, d.model === 'Debian-server' ? 'ic-server' : d.model === 'Docker' ? 'ic-docker' : 'ic-pc', d.model === 'Debian-server' ? 74 : 78);
      if (d.model === 'Debian') el('path', { d: 'M24 -26a7 7 0 1 0 0 10', fill: 'none', stroke: '#d4574f', 'stroke-width': 3 }, g); }
  };
  // объёмные иконки из деки главы 7 (спрайт #ic-* вставляет сборщик, палитра — _elab/sprite.py)
  function use(g, id, w) { var u = el('use', { x: -w / 2, y: -w * 0.42, width: w, height: w * 0.84 }, g);
    u.setAttributeNS('http://www.w3.org/1999/xlink', 'href', '#' + id); u.setAttribute('href', '#' + id); return u; }
  function iconSvg(type, model) {
    var s = document.createElementNS(NS, 'svg'); s.setAttribute('viewBox', '-56 -46 112 92');
    ICONS[type](s, { model: model }); return s.outerHTML;
  }
  function el(tag, attrs, parent) { var x = document.createElementNS(NS, tag); Object.keys(attrs || {}).forEach(function (k) { x.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(x); return x; }
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  // ================================================================== вид: панорама и масштаб
  function applyView() { world.setAttribute('transform', 'translate(' + view.x + ',' + view.y + ') scale(' + view.k + ')'); }
  function toWorld(cx, cy) { var r = cv.getBoundingClientRect(); return { x: (cx - r.left - view.x) / view.k, y: (cy - r.top - view.y) / view.k }; }
  function fit() {
    var L = net.list(), r = cv.getBoundingClientRect(); if (!L.length) { view = { x: r.width / 2 - 500, y: r.height / 2 - 320, k: 1 }; applyView(); return; }
    var x0 = Math.min.apply(null, L.map(function (d) { return d.x; })) - 110, x1 = Math.max.apply(null, L.map(function (d) { return d.x; })) + 110;
    var y0 = Math.min.apply(null, L.map(function (d) { return d.y; })) - 90, y1 = Math.max.apply(null, L.map(function (d) { return d.y; })) + 110;
    var k = Math.min(r.width / (x1 - x0), r.height / (y1 - y0), 1.6);
    view = { k: k, x: (r.width - (x1 + x0) * k) / 2, y: (r.height - (y1 + y0) * k) / 2 }; applyView();
  }
  cv.addEventListener('wheel', function (e) {
    e.preventDefault(); var r = cv.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
    var k2 = Math.max(0.3, Math.min(3, view.k * (e.deltaY < 0 ? 1.12 : 0.89)));
    view.x = mx - (mx - view.x) * k2 / view.k; view.y = my - (my - view.y) * k2 / view.k; view.k = k2; applyView();
  }, { passive: false });
  $('bFit').addEventListener('click', fit);

  // ================================================================== схема
  function linkOff(i) {
    var l = net.links[i], same = [];
    net.links.forEach(function (x, j) { if ((x.a.dev === l.a.dev && x.b.dev === l.b.dev) || (x.a.dev === l.b.dev && x.b.dev === l.a.dev)) same.push(j); });
    if (same.length < 2) return { x: 0, y: 0 };
    var a = net.devs[l.a.dev], b = net.devs[l.b.dev], dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1;
    if (l.a.dev > l.b.dev) { dx = -dx; dy = -dy; }
    var k = (same.indexOf(i) - (same.length - 1) / 2) * 16; return { x: -dy / L * k, y: dx / L * k };
  }
  // «Тест»: подписи портов MES по STP-состоянию — янтарный переход (listening/learning/discarding до forwarding), красный блок
  function stpMarks() {
    [].forEach.call($('gp').querySelectorAll('g.pl'), function (g) {
      var dp = g.getAttribute('data-dp').split('|'), d = net.devs[dp[0]], z = null, cl = '';
      if (mode === 'test' && d && d.type === 'mes' && net.stpState) { var L = net.lportOf(dp[0], dp[1]); z = L && net.stpState(dp[0], L.name, 0); }
      if (z && z !== 'Frw') { var r = net.stp(0)[dp[0]][net.lportOf(dp[0], dp[1]).name]; cl = r.fwd ? ' stp-tr' : ' stp-blk'; }
      g.setAttribute('class', 'pl' + cl);
      var tt = g.querySelector('title'); if (!tt) tt = el('title', {}, g);
      tt.textContent = z ? 'STP: ' + EL.STPN[z] + (cl === ' stp-tr' ? ', до forwarding ' + net.stpLeft(dp[0], net.lportOf(dp[0], dp[1]).name, 0) + ' с' : '') : '';
    });
  }
  function draw() {
    var gl = $('gl'), gp = $('gp'), gd = $('gd'); gl.innerHTML = ''; gp.innerHTML = ''; gd.innerHTML = '';
    var undoPre = X.preDraw();          // кластеры: устройства свёрнутой зоны рисуются в точке значка
    net.links.forEach(function (l, i) {
      var a = net.devs[l.a.dev], b = net.devs[l.b.dev], o = linkOff(i), A = { x: a.x + o.x, y: a.y + o.y }, B = { x: b.x + o.x, y: b.y + o.y };
      var up = net.linkUp(l.a.dev, l.a.port);
      var ln = el('line', { x1: A.x, y1: A.y, x2: B.x, y2: B.y, 'class': 'lnk' + (up ? '' : ' down') + (selLink === i || mselL[i] ? ' sel' : '') + (/^(console|aux)/.test(l.a.port) || /^(console|aux)/.test(l.b.port) ? ' ser' : ''), 'data-li': i }, gl);   // ser — консольный RS-232
      ln.addEventListener('mousedown', function (e) { e.stopPropagation(); if (e.button !== 0) return;
        if (e.ctrlKey || e.metaKey) { if (mselL[i]) delete mselL[i]; else mselL[i] = 1; selLink = null; }
        else { msel = {}; mselL = {}; selLink = i; sel = null; } draw(); });
      ln.addEventListener('contextmenu', function (e) { e.preventDefault(); e.stopPropagation(); linkMenu(i, e); });
      [[A, B, l.a.port], [B, A, l.b.port]].forEach(function (zz) {
        var dx = zz[1].x - zz[0].x, dy = zz[1].y - zz[0].y, L = Math.hypot(dx, dy) || 1, k = Math.min(Math.abs(dy) > Math.abs(dx) ? 96 : 84, L * 0.38);
        var px = zz[0].x + dx / L * k, py = zz[0].y + dy / L * k, g = el('g', { 'class': 'pl', 'data-dp': (zz[0] === A ? l.a.dev : l.b.dev) + '|' + zz[2] }, gp), w = zz[2].length * 7.4 + 12;
        el('rect', { x: px - w / 2, y: py - 9, width: w, height: 18 }, g); el('text', { x: px, y: py }, g).textContent = zz[2];
        // огонёк порта у края значка устройства (виден всегда; причина — подсказкой в «Тесте»)
        var lo = net.ledOf ? net.ledOf(zz[0] === A ? l.a.dev : l.b.dev, zz[2]) : null;
        if (lo) { var t = Math.min(dx ? 70 / Math.abs(dx / L) : 1e9, dy ? 44 / Math.abs(dy / L) : 1e9, L * 0.3), hv = Math.abs(dx) >= Math.abs(dy) ? w / 2 : 9,
            sh = k - t < hv + 6 ? 13 : 0,              // подпись порта рядом — огонёк сбоку от кабеля
            c = el('circle', { 'class': 'pled ' + lo.c, 'data-dp': (zz[0] === A ? l.a.dev : l.b.dev) + '|' + zz[2], cx: zz[0].x + dx / L * t - dy / L * sh, cy: zz[0].y + dy / L * t + dx / L * sh, r: 5 }, gp);
          if (mode === 'test') el('title', {}, c).textContent = ({ g: 'Зелёный', o: 'Оранжевый', r: 'Красный' }[lo.c]) + ': ' + lo.why; }
      });
    });
    stpMarks();
    net.list().forEach(function (d) {
      var g = el('g', { 'class': 'dev' + (sel === d.id || msel[d.id] ? ' sel' : '') + (cable && cable.a === d.id ? ' pick' : '') + (d.off ? ' off' : ''),
                        transform: 'translate(' + d.x + ',' + d.y + ')', 'data-id': d.id }, gd);
      el('rect', { 'class': 'ring', x: -66, y: -38, width: 132, height: 76 }, g);
      ICONS[d.type](g, d);
      el('circle', { 'class': 'led', cx: 56, cy: -26, r: 4.5, fill: d.off ? '#ff6b62' : '#7dffb0' }, g);
      el('text', { y: 50, 'class': 'lbl' }, g).textContent = d.name;
      el('text', { y: 65, 'class': 'mdl' }, g).textContent = d.model + ipLabel(d);
      g.addEventListener('mousedown', function (e) { devDown(e, d); });
      g.addEventListener('contextmenu', function (e) { e.preventDefault(); e.stopPropagation(); devMenu(d, e); });
    });
    if (undoPre) undoPre();
    stat(); X.onDraw();
  }
  function ipLabel(d) { var f = net.ifaces(d.id)[0]; return f && (d.type === 'vpc' || d.type === 'deb') ? ' · ' + f.ip : ''; }
  // ================================================================== модельное время: старение MAC/ARP
  var speed = 1, mode = 'work';
  // Работа — как на оборудовании (без таблиц, трассы, часов и проверок); Тест — учебные инструменты
  function setMode(m) {
    mode = m; document.body.classList.toggle('mtest', m === 'test');
    [].forEach.call($('mode').querySelectorAll('[data-m]'), function (x) { x.classList.toggle('on', x.dataset.m === m); });
    X.onMode(m);
    if (m === 'work') { speed = 1; [].forEach.call($('clk').querySelectorAll('[data-sp]'), function (x) { x.classList.toggle('on', x.dataset.sp === '1'); });
      stopTrace(); trace = null; Object.keys(wins).forEach(function (k) { if (/^(tb|task|help|ping)/.test(k)) closeWin(k, true); }); chips();
      if (tab === 'task' || tab === 'file') { tab = 'dev'; [].forEach.call($('stabs').querySelectorAll('[data-t]'), function (x) { x.classList.toggle('on', x.dataset.t === 'dev'); }); }
      task = null; }
    renderSide(); renderLab(false);
  }
  $('mode').addEventListener('click', function (e) { var b = e.target.closest('[data-m]'); if (b) setMode(b.dataset.m); });
  var labTick = 0;
  function advance(dt, jump) {
    net.onReload = function (rid) { boot(rid, true); };   // reload system in/at — по модельному времени
    var gone = net.tick(dt); EL.clock.warp += (jump ? dt : dt - 1) * 1000;
    $('clkT').textContent = net.clockText();
    if (gone.length && mode === 'test') { toast('Истёк таймер: ' + gone.slice(0, 3).map(function (g) { return g.dev + ' ' + g.kind + ' ' + g.what; }).join('; ') + (gone.length > 3 ? ' и ещё ' + (gone.length - 3) : ''));
      $('clk').classList.add('flash'); setTimeout(function () { $('clk').classList.remove('flash'); }, 700); }
    if (Object.keys(wins).some(function (k) { return k.indexOf('tb') === 0; })) refreshTables();
    stpMarks(); pollEv();
    if (lab && ++labTick % 3 === 0) renderLab(false);        // пункты, которые выполняются со временем (NTP, OSPF, STP), загораются сами
    return gone.length;
  }
  setInterval(function () { if (speed) advance(speed, false); else EL.clock.warp -= 1000; }, 1000);   // пауза останавливает и часы устройств
  $('clk').addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return;
    if (b.dataset.ff === 'own') { var v = $('ffv').value.trim(), m = v.match(/^(\d+(?:[.,]\d+)?)\s*(с|сек|s|м|мин|m|ч|h)?$/i);
      if (!m) { toast('Промотка: число и единица — 90 с, 15 мин, 4 ч'); return; }
      var k = /^(ч|h)/i.test(m[2] || 'мин') ? 3600 : /^(с|сек|s)$/i.test(m[2] || '') ? 1 : 60, dt = Math.round(parseFloat(m[1].replace(',', '.')) * k);
      if (dt < 1 || dt > 7 * 86400) { toast('Промотка от 1 с до 7 суток'); return; } advance(dt, true); toast('Промотано ' + v + ' модельного времени'); return; }
    if (b.dataset.ff) { var sec = +b.dataset.ff; if (!advance(sec, true)) toast('Промотано ' + (sec >= 3600 ? sec / 3600 + ' ч' : sec / 60 + ' мин') + ' модельного времени'); return; }
    speed = +b.dataset.sp; [].forEach.call($('clk').querySelectorAll('[data-sp]'), function (x) { x.classList.toggle('on', x === b); }); });
  function stat() {
    $('bPower').hidden = !net.list().some(function (d) { return d.off; });
    $('stat').innerHTML = 'УСТРОЙСТВ <b>' + net.list().length + '</b> · КАБЕЛЕЙ <b>' + net.links.length + '</b><br>' +
      (lab ? 'ЛАБА <b>' + lab.id + '</b>' : task ? 'ЗАДАНИЕ <b>' + (task.kind === 'base' ? 'БАЗА' : 'VLAN') + '</b>' : 'СВОБОДНАЯ СХЕМА');
  }
  var lastClick = { id: null, t: 0 };     // двойной щелчок по устройству — консоль (dblclick не доходит: значок перерисовывается после первого щелчка)
  function devDown(e, d) {
    e.stopPropagation(); closeMenu();
    if (e.button !== 0) return;
    if (cable) { finishCable(d); return; }
    if (e.ctrlKey || e.metaKey) { if (msel[d.id]) delete msel[d.id]; else msel[d.id] = 1; sel = null; selLink = null; draw(); return; }   // Ctrl+клик — добавить/убрать
    if (!msel[d.id]) { msel = {}; mselL = {}; msel[d.id] = 1; }
    var grp = Object.keys(msel).map(function (k) { return net.devs[k]; }).filter(Boolean), p0 = toWorld(e.clientX, e.clientY);
    var start = grp.map(function (x) { return { d: x, x: x.x, y: x.y }; }), moved = false;
    function mv(ev) { var p = toWorld(ev.clientX, ev.clientY); start.forEach(function (q) { q.d.x = q.x + p.x - p0.x; q.d.y = q.y + p.y - p0.y; });
      if (Math.abs(p.x - p0.x) + Math.abs(p.y - p0.y) > 3) { moved = true; draw(); } }
    function up() { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); sel = d.id; selLink = null;
      if (!moved) { var tnow = Date.now(); if (lastClick.id === d.id && tnow - lastClick.t < 450) { lastClick = { id: null, t: 0 }; draw(); openTerm(d.id); return; } lastClick = { id: d.id, t: tnow }; } else lastClick = { id: null, t: 0 };
      if (moved) start.forEach(function (q) { if (q.d.x !== q.x || q.d.y !== q.y) X.roomAct({ k: 'dev.move', id: q.d.id, x: Math.round(q.d.x), y: Math.round(q.d.y) }); });
      if (moved) start.forEach(function (q) { if (q.d.x !== q.x || q.d.y !== q.y) X.rec({ k: 'move', name: q.d.name, x: q.x, y: q.y }); }); draw(); }
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  }
  // пустое поле: зажатый пробел или средняя кнопка — панорама; ЛКМ — рамка выделения (Ctrl — добавить к выделенному)
  function pan(e) {
    var sx = e.clientX, sy = e.clientY, vx = view.x, vy = view.y; cv.classList.add('pan');
    function mv(ev) { view.x = vx + ev.clientX - sx; view.y = vy + ev.clientY - sy; applyView(); }
    function up() { cv.classList.remove('pan'); window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); }
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  }
  function band(e) {
    var add = e.ctrlKey || e.metaKey, sx = e.clientX, sy = e.clientY, r = $('rband'), keep = add ? { d: EL.clone(msel), l: EL.clone(mselL) } : { d: {}, l: {} };
    if (!add) { msel = {}; mselL = {}; } sel = null; selLink = null; draw();
    function box(ev) { return { x0: Math.min(sx, ev.clientX), y0: Math.min(sy, ev.clientY), x1: Math.max(sx, ev.clientX), y1: Math.max(sy, ev.clientY) }; }
    function mv(ev) { var b = box(ev); if (b.x1 - b.x0 + b.y1 - b.y0 < 4) return; r.style.display = 'block';
      r.style.left = b.x0 + 'px'; r.style.top = b.y0 + 'px'; r.style.width = (b.x1 - b.x0) + 'px'; r.style.height = (b.y1 - b.y0) + 'px'; }
    function up(ev) { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); r.style.display = 'none';
      var b = box(ev); if (b.x1 - b.x0 + b.y1 - b.y0 < 4) { draw(); return; }
      var a = toWorld(b.x0, b.y0), c = toWorld(b.x1, b.y1), inR = function (x, y) { return x >= a.x && x <= c.x && y >= a.y && y <= c.y; };
      msel = keep.d; mselL = keep.l;
      net.list().forEach(function (d) { if (inR(d.x, d.y)) msel[d.id] = 1; });
      net.links.forEach(function (l, i) { var A = net.devs[l.a.dev], B = net.devs[l.b.dev]; if (msel[l.a.dev] && msel[l.b.dev] || inR((A.x + B.x) / 2, (A.y + B.y) / 2)) mselL[i] = 1; });
      draw(); var n = Object.keys(msel).length, m = Object.keys(mselL).length; if (n || m) toast('Выделено: устройств ' + n + ', кабелей ' + m + ' · Delete — удалить'); }
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  }
  cv.addEventListener('mousedown', function (e) {
    closeMenu();
    if (e.button === 1 || (e.button === 0 && spaceDown)) { e.preventDefault(); pan(e); return; }
    if (e.button !== 0) return;
    if (cable) { cable = null; $('ghost').style.display = 'none'; draw(); toast('Кабель отменён'); return; }
    band(e);
  });
  document.addEventListener('keydown', function (e) { if (e.key !== ' ' || /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) || e.target.closest && e.target.closest('.win')) return;
    e.preventDefault(); if (!spaceDown) { spaceDown = true; cv.classList.add('grab'); } });
  document.addEventListener('keyup', function (e) { if (e.key === ' ') { spaceDown = false; cv.classList.remove('grab'); } });
  cv.addEventListener('mousemove', function (e) {
    if (!cable) return; var a = net.devs[cable.a], p = toWorld(e.clientX, e.clientY), g = $('ghost');
    g.setAttribute('x1', a.x); g.setAttribute('y1', a.y); g.setAttribute('x2', p.x); g.setAttribute('y2', p.y); g.style.display = '';
  });
  cv.addEventListener('contextmenu', function (e) { e.preventDefault(); addMenu(e); });
  cv.addEventListener('dragover', function (e) { e.preventDefault(); });
  cv.addEventListener('drop', function (e) { e.preventDefault(); var m = e.dataTransfer.getData('text/model'); if (!m) return;
    var p = toWorld(e.clientX, e.clientY); addDev(m, p.x, p.y); });

  // ================================================================== контекстные меню
  var menu = null;
  function closeMenu() { if (menu) { menu.remove(); menu = null; } }
  function showMenu(x, y, html, onClick) {
    closeMenu(); menu = document.createElement('div'); menu.className = 'ctx'; menu.innerHTML = html; document.body.appendChild(menu);
    var r = menu.getBoundingClientRect();
    menu.style.left = Math.min(x, innerWidth - r.width - 8) + 'px'; menu.style.top = Math.min(y, innerHeight - r.height - 8) + 'px';
    menu.addEventListener('mousedown', function (e) { e.stopPropagation(); });
    menu.addEventListener('click', function (e) { var b = e.target.closest('[data-a]'); if (b) { var keep = onClick(b.dataset.a, b); if (!keep) closeMenu(); } });
    return menu;
  }
  document.addEventListener('mousedown', closeMenu);
  function item(a, ic, t) { return '<button data-a="' + a + '"><span>' + ic + '</span>' + t + '</button>'; }
  function devMenu(d, e) {
    if (readOnly) return;
    sel = d.id; draw();
    showMenu(e.clientX, e.clientY, '<div class="h">' + esc(d.name) + ' · ' + esc(d.model) + '</div>' +
      item('term', '▣', 'Консоль') + (mode === 'test' ? item('tables', '☰', 'Таблицы ARP / MAC / маршруты') : '') + item('props', 'ⓘ', 'Свойства') + item('cable', '⌁', 'Подключить кабель') +
      (mode === 'test' ? item('ping', '⇢', 'Ping отсюда…') : '') + '<hr>' +
      (net.manualFor(d.id) ? item('man', '❐', 'Руководство') : '') + X.items('dev', d) + (!d.off ? item('off', '■', 'Выключить') : item('on', '▶', 'Включить')) + item('reload', '⟳', 'Перезагрузить') + '<hr>' + item('del', '✕', 'Удалить'),
      function (a) {
        if (a === 'term') openTerm(d.id);
        if (a === 'props') openProps(d.id);
        if (a === 'man') openManual(d.id);
        if (a === 'tables') openTables(d.id);
        if (a === 'cable') startCable(d.id);
        if (a === 'ping') openPing(d.id);
        if (a === 'off') { if (X.roomAct({ k: 'power', dev: d.id, on: false })) return; net.power(d.id, false); tlog(d.id, '%SYS: питание выключено', 's'); setPr(d.id); draw(); }
        if (a === 'on') boot(d.id, false);
        if (a === 'reload') boot(d.id, true);
        if (a === 'del') { msel = {}; mselL = {}; msel[d.id] = 1; selLink = null; delSelected(); }
        return X.run('dev', a, d);
      });
  }
  function linkMenu(i, e) {
    if (readOnly) return;
    selLink = i; draw(); var l = net.links[i];
    var ph = net.phys ? net.phys(l.a.dev, l.a.port) : null;
    showMenu(e.clientX, e.clientY, '<div class="h">' + esc(net.devs[l.a.dev].name + ' ' + l.a.port + ' ↔ ' + net.devs[l.b.dev].name + ' ' + l.b.port) + '</div>' +
      (ph && mode === 'test' ? '<div class="h" style="border:0;text-transform:none;letter-spacing:0">' + esc((net.cableText ? net.cableText(l) : EL.CABLES[ph.cab || net.defaultCable(l.a.dev, l.a.port, l.b.dev, l.b.port)] || '') + ' · ' +
        (ph.up ? ph.speed + ' Мбит/с, ' + ph.dup[l.a.dev] + '/' + ph.dup[l.b.dev] + (ph.mismatch ? ' — дуплекс не совпадает!' : '') : 'нет линка: ' + ph.why)) + '</div>' : '') +
      X.items('link') + item('del', '✕', 'Удалить кабель'), function (a) { if (a === 'del') { if (X.roomAct({ k: 'link.del', i: i })) return; X.rec({ k: 'dis', l: X.linkArr(l) }); net.disconnect(i); selLink = null; draw(); refresh(); return; }
        return X.run('link', a, i); });
  }
  // панель устройств: сверху — что нужно в лабах (доступ, маршрутизаторы, серверы и ПК), остальное — «Ещё оборудование» (more: true)
  var TOP = [{ name: 'Коммутаторы доступа', first: ['MES1428', 'MES2308P'], from: ['Коммутаторы доступа'] },
    { name: 'Маршрутизаторы', first: ['ESR-200', 'vESR'], from: ['Маршрутизаторы ESR'] },
    { name: 'Серверы и ПК', first: ['Debian-server', 'Docker', 'VPC', 'Debian'], from: [] }];
  var MORE = ['Коммутаторы доступа PoE', 'Промышленные коммутаторы', 'Коммутаторы агрегации', 'Коммутаторы для ЦОД', 'Маршрутизаторы ME', 'Межсетевые экраны ESR ФСТЭК',
    'Контроллеры Wi-Fi', 'Точки доступа Wi-Fi', 'OLT GPON / XGS-PON', 'ONT (абонентские терминалы)', 'Консольные серверы SCS'];
  function catalogGroups() {
    var g = {}, used = {}, out = [];
    Object.keys(EL.MODELS).forEach(function (k) { var m = EL.MODELS[k]; (g[m.group] = g[m.group] || []).push(k); });
    TOP.forEach(function (t) { var its = t.first.filter(function (k) { return EL.MODELS[k]; });
      t.from.forEach(function (gr) { (g[gr] || []).slice().sort().forEach(function (k) { if (its.indexOf(k) < 0) its.push(k); }); });
      its.forEach(function (k) { used[k] = 1; }); out.push({ name: t.name, items: its }); });
    Object.keys(g).sort(function (a, b) { return (MORE.indexOf(a) + 99) % 99 - (MORE.indexOf(b) + 99) % 99; }).forEach(function (gr) {
      var its = g[gr].filter(function (k) { return !used[k]; }).sort(); if (its.length) out.push({ name: gr, items: its, more: true }); });
    return out;
  }
  function addMenu(e) {
    if (readOnly) return;
    var p = toWorld(e.clientX, e.clientY);
    var m = showMenu(e.clientX, e.clientY, '<div class="h">Добавить устройство</div><input class="q" placeholder="Поиск: MES2428, ESR, ПК…"><div class="list"></div><hr>' +
      X.items('field') + item('fit', '⤢', 'Показать всю схему') + item('clear', '✕', 'Очистить схему'), function (a, b) {
        X.run('field', a, p);
        if (a === 'add') addDev(b.dataset.m, p.x, p.y);
        if (a === 'fit') fit();
        if (a === 'clear') clearAll();
      });
    var q = m.querySelector('input'), list = m.querySelector('.list');
    function fill() { var s = q.value.trim().toLowerCase();
      list.innerHTML = catalogGroups().map(function (g) { var its = g.items.filter(function (k) { return !s || k.toLowerCase().indexOf(s) >= 0 || g.name.toLowerCase().indexOf(s) >= 0; });
        return its.length ? '<div class="h" style="border:0;margin:6px 0 0">' + esc(g.name) + '</div>' + its.slice(0, s ? 40 : 6).map(function (k) {
          return '<button data-a="add" data-m="' + k + '"><span>+</span>' + k + '</button>'; }).join('') : ''; }).join(''); }
    q.addEventListener('input', fill); q.addEventListener('keydown', function (ev) { ev.stopPropagation(); }); fill(); setTimeout(function () { q.focus(); }, 0);
  }
  function addDev(model, x, y) { if (X.roomAct({ k: 'dev.add', model: model, x: Math.round(x), y: Math.round(y) })) return null; var d = net.add(model, null, x, y); sel = d.id; X.rec({ k: 'add', name: d.name }); draw(); refresh(); toast(d.name + ' добавлен · ПКМ — меню, 2×клик — консоль'); return d; }
  function plural(n, a, b, c) { var m = n % 10, h = n % 100; return n + ' ' + (m === 1 && h !== 11 ? a : m >= 2 && m <= 4 && (h < 12 || h > 14) ? b : c); }
  // подтверждение в окне эмулятора (не window.confirm)
  function ask(text, yes, yesLabel) {
    var body = document.createElement('div'); body.className = 'pad';
    body.innerHTML = '<p style="color:var(--ink);font-size:15px">' + esc(text) + '</p><div class="row"><button class="pri" data-q="y">' + esc(yesLabel || 'Да, удалить') + '</button><button data-q="n">Отмена</button></div>';
    makeWin('ask', 'Подтверждение', '', body, { w: 380, h: 170, x: innerWidth / 2 - 190, y: innerHeight / 2 - 110 });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-q]'); if (!b) return; closeWin('ask'); if (b.dataset.q === 'y') yes(); });
    var y = body.querySelector('[data-q="y"]'); if (y) setTimeout(function () { y.focus(); }, 0);
  }
  function delSelected() {
    if (readOnly) return;
    var ds = Object.keys(msel).filter(function (k) { return net.devs[k]; }); if (!ds.length && sel && net.devs[sel]) ds = [sel];
    var ls = Object.keys(mselL).map(Number); if (selLink !== null) ls.push(selLink);
    ls = ls.filter(function (i, j, a) { var l = net.links[i]; return l && a.indexOf(i) === j && ds.indexOf(l.a.dev) < 0 && ds.indexOf(l.b.dev) < 0; });
    if (!ds.length && !ls.length) return;
    var txt = 'Вы точно хотите удалить ' + [ds.length ? plural(ds.length, 'устройство', 'устройства', 'устройств') : '', ls.length ? plural(ls.length, 'кабель', 'кабеля', 'кабелей') : ''].filter(Boolean).join(' и ') + '?';
    ask(txt, function () {
      ls.sort(function (a, b) { return b - a; }).forEach(function (i) { if (X.roomAct({ k: 'link.del', i: i })) return; X.rec({ k: 'dis', l: X.linkArr(net.links[i]) }); net.disconnect(i); });
      ds.forEach(function (id) { delDev(id); }); msel = {}; mselL = {}; selLink = null; sel = null; draw(); refresh(); });
  }
  function delDev(id) { if (X.roomAct({ k: 'dev.del', id: id })) return; X.rec(X.delOp(id)); closeWin('t' + id); closeWin('p' + id); delete terms[id]; net.remove(id); if (sel === id) sel = null; draw(); refresh(); }
  function clearAll() { if (net.list().length && !confirm('Очистить схему?')) return; lab = null; task = null; resetNet(); renderSide(); autoClear(); }

  // ================================================================== кабель
  function startCable(id) { if (!net.freePorts(id).length) { toast('Нет свободных портов'); return; } cable = { a: id }; draw(); toast('Щёлкните второе устройство'); }
  function finishCable(d) {
    var a = net.devs[cable.a]; cable = null; $('ghost').style.display = 'none'; draw();
    if (d.id === a.id) { toast('Нельзя соединить устройство само с собой'); return; }
    var fa = net.freePorts(a.id), fb = net.freePorts(d.id); if (!fb.length) { toast('У ' + d.name + ' нет свободных портов'); return; }
    var body = document.createElement('div'); body.className = 'pad';
    function opts(L) { return L.map(function (p) { return '<option>' + p + '</option>'; }).join(''); }
    body.innerHTML = '<div class="k">Новый кабель</div><label>' + esc(a.name) + ' — порт</label><select id="cpa">' + opts(fa) + '</select>' +
      '<label>' + esc(d.name) + ' — порт</label><select id="cpb">' + opts(fb) + '</select>' +
      '<label>Кабель / модуль</label><select id="cpc"><option value="">Авто: медь (Auto-MDIX), между портами 10G — SFP+</option>' +
      Object.keys(EL.CABLES || {}).map(function (k) { return '<option value="' + k + '">' + EL.CABLES[k] + '</option>'; }).join('') + '</select>' +
      '<label>Модуль на стороне ' + esc(d.name) + '</label><select id="cpd"><option value="">Такой же</option>' +
      Object.keys(EL.CABLES || {}).filter(function (k) { return /^(sfp|dac)/.test(k); }).map(function (k) { return '<option value="' + k + '">' + EL.CABLES[k] + '</option>'; }).join('') + '</select><div class="row"><button class="pri" data-c="ok">Соединить</button><button data-c="no">Отмена</button></div>';
    makeWin('cable', 'Кабель', a.name + ' ↔ ' + d.name, body, { w: 380, h: 330, x: innerWidth / 2 - 180, y: innerHeight / 2 - 140 });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-c]'); if (!b) return;
      if (b.dataset.c === 'ok' && X.roomAct({ k: 'link.add', a: a.id, pa: body.querySelector('#cpa').value, b: d.id, pb: body.querySelector('#cpb').value })) { closeWin('cable'); return; }
      if (b.dataset.c === 'ok') { var err = net.connect(a.id, body.querySelector('#cpa').value, d.id, body.querySelector('#cpb').value, (body.querySelector('#cpc').value ? body.querySelector('#cpc').value + (body.querySelector('#cpd').value ? '|' + body.querySelector('#cpd').value : '') : undefined)); if (err) { toast(err); return; }
        X.rec({ k: 'con', l: X.linkArr(net.links[net.links.length - 1]) }); draw(); refresh(); toast('Кабель проложен'); }
      closeWin('cable'); });
  }

  // ================================================================== плавающие окна
  function makeWin(key, title, sub, body, o) {
    o = o || {};
    if (wins[key]) closeWin(key, true);
    var w = document.createElement('div'), n = Object.keys(wins).length; w.className = 'win';
    w.style.left = (o.x !== undefined ? o.x : Math.max(20, innerWidth - (o.w || 640) - 30 - n * 26)) + 'px';
    w.style.top = (o.y !== undefined ? o.y : 80 + n * 26) + 'px';
    w.style.width = (o.w || 640) + 'px'; w.style.height = (o.h || 400) + 'px';
    w.innerHTML = '<div class="wt"><b>' + esc(title) + '</b><small>' + esc(sub || '') + '</small><button data-w="min" title="Свернуть">_</button><button data-w="close" title="Закрыть">×</button></div>';
    var wb = document.createElement('div'); wb.className = 'wb'; wb.appendChild(body); w.appendChild(wb);
    document.body.appendChild(w); wins[key] = { el: w, title: title, min: false }; focusWin(key);
    var bar = w.querySelector('.wt');
    bar.addEventListener('mousedown', function (e) {
      if (e.target.closest('button')) return; focusWin(key);
      var sx = e.clientX, sy = e.clientY, x0 = w.offsetLeft, y0 = w.offsetTop;
      function mv(ev) { w.style.left = Math.max(-w.offsetWidth + 80, Math.min(innerWidth - 80, x0 + ev.clientX - sx)) + 'px';
        w.style.top = Math.max(54, Math.min(innerHeight - 60, y0 + ev.clientY - sy)) + 'px'; if (o.onMove) o.onMove(ev); }
      function up(ev) { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); if (o.onDrop) o.onDrop(ev); }
      window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
    });
    w.addEventListener('mousedown', function (e) { e.stopPropagation(); focusWin(key); closeMenu(); });
    bar.addEventListener('click', function (e) { var b = e.target.closest('[data-w]'); if (!b) return;
      if (b.dataset.w === 'close') closeWin(key); else minWin(key, true); });
    chips(); return w;
  }
  function focusWin(key) { Object.keys(wins).forEach(function (k) { wins[k].el.classList.toggle('focus', k === key); }); var w = wins[key]; if (w) w.el.style.zIndex = ++z; }
  function minWin(key, m) { var w = wins[key]; if (!w) return; w.min = m; w.el.style.display = m ? 'none' : 'flex'; if (!m) focusWin(key); chips(); }
  function closeWin(key, silent) {
    var tid = key.charAt(0) === 't' && net && net.devs[key.slice(1)] ? key.slice(1) : null;
    if (tid !== null && !wins[key] && consOrder && consOrder.indexOf(String(tid)) >= 0) { closeTab(tid); return; }   // терминал во вкладке «Консолей»
    var w = wins[key]; if (!w) return;
    if (key === 'cons' && consOrder) { consOrder.forEach(function (id) { if (terms[id]) delete terms[id].body; }); consOrder = []; consActive = null; }
    if (tid !== null && terms[tid]) delete terms[tid].body;
    w.el.remove(); delete wins[key]; if (!silent) chips(); }
  function chips() {
    $('chips').innerHTML = Object.keys(wins).map(function (k) { var w = wins[k];
      return '<button class="chip' + (w.min ? ' min' : '') + '" data-k="' + k + '">' + esc(w.title) + '</button>'; }).join('');
  }
  $('chips').addEventListener('click', function (e) { var b = e.target.closest('[data-k]'); if (!b) return; var k = b.dataset.k, w = wins[k];
    if (w.min) minWin(k, false); else if (w.el.classList.contains('focus')) minWin(k, true); else focusWin(k); });

  // ================================================================== терминалы
  function term(id) { return terms[id] || (terms[id] = { html: '', hist: [], hi: 0, auth: false, user: null }); }
  // вход в консоль: MES — User Name/Password (заводской admin/admin или username из конфигурации), ESR — login/Password (admin/password)
  function needLogin(d) { return (d.type === 'mes' && d.sub !== 'ont' && d.sub !== 'eont') || d.type === 'esr'; }   // у ONT своей CLI нет (Web user/user)
  function loginPrompt(d, t) { return t.user === null ? (d.type === 'mes' ? 'User Name:' : d.st.run.host + ' login: ') : 'Password:'; }
  function checkLogin(d, u, p) {
    var aa = net.aaaLogin ? net.aaaLogin(d.id, 'console', u, p, function (uu, pp) { return localLogin(d, uu, pp); }) : null;   // RADIUS/TACACS+ (aaa.js)
    return aa ? aa.ok : localLogin(d, u, p);
  }
  function localLogin(d, u, p) {
    var U = d.type === 'esr' ? d.st.run.users : d.st.users;
    if (d.type === 'mes' && !Object.keys(U || {}).length) return u === 'admin' && p === (d.st.dialect === '8' ? '' : 'admin');   // MES 8.x — admin с пустым паролем, остальные — admin/admin (CREDENTIALS.md)
    return !!(U && U[u] && (U[u].pw === p || (U[u].pwEnc && EL.E.hash(p).slice(0, 30) === U[u].pwEnc)));
  }
  // в режиме «Работа» — только то, что пишет устройство: русские подсказки эмулятора убираются
  var CYR = /[А-Яа-яЁё]/;
  function realOut(d, line, r) {
    if (mode === 'test' || !r || (d.type !== 'mes' && d.type !== 'esr')) return r;
    var L = String(r).split('\n'), keep = [], err = false;
    L.forEach(function (x) {
      var hm = x.match(/^(  \S+(?: [^\sЀ-ӿ]+)*?)\s{2,}\S/); if (hm && CYR.test(x)) { keep.push(hm[1]); return; }   // строка подсказки «?»: слово (или «gigabitethernet 1/0/N») без русского описания
      if (!CYR.test(x)) { keep.push(x); return; }
      if (/^\s*%/.test(x)) { err = true; return; }
      var cut = x.replace(/\s+←.*$/, '').replace(/\s*\([^()]*[А-Яа-яЁё][^()]*\)\s*$/, '');
      if (!CYR.test(cut) && cut.trim()) keep.push(cut);
    });
    if (d.type === 'esr') keep = keep.map(function (x) { return x === '% Unrecognized command' ? 'Syntax error: Unknown command' : x === '% Incomplete command' ? 'Syntax error: Incomplete command' : x === '% Ambiguous command' ? 'Syntax error: Ambiguous command' : x; });
    if (!keep.length && err && !/^\s*(do\s+)?sh(o(w)?)?\b/i.test(line)) keep.push(d.type === 'esr' ? 'Syntax error: Illegal parameter' : "% Invalid input detected at '^' marker.");
    return keep.join('\n');
  }
  function banner(d) {
    if (d.type === 'deb') return d.model === 'Docker' ? 'Docker container · pnet-chrome · введите help' : 'Debian GNU/Linux 11 ' + d.st.host + ' tty1';
    if (d.sub === 'phone') return 'Аналоговый телефон · dial НОМЕР — набрать, hangup — положить трубку, status — состояние';
    if (d.sub === 'tau' || d.sub === 'smg') return 'Eltex ' + d.model + '\n';
    if (d.type === 'vpc') return 'Welcome to Virtual PC Simulator, version 0.8.3' + (mode === 'test' ? ' · введите ? для справки' : '');
    if (d.type === 'esr') return d.sub ? 'Eltex ' + d.model + '\n' : 'Eltex ' + d.model + ' · software version 1.24.2\n';   // SCS, WLC, ME — без версии ESR
    return d.model + '\n';
  }
  function openTerm(id) {
    var d = net.devs[id]; if (!d) return; sel = id; draw(); id = String(id);
    var key = 't' + id, t = term(id);
    if (t.body) { if (wins[key]) { minWin(key, false); focusTerm(id); } else consShow(id); return; }
    if (!t.html) t.html = '<div class="s">' + esc(banner(d)) + '</div>';
    var body = document.createElement('div'); body.className = 'tbody'; body.style.cssText = 'display:flex;flex-direction:column;flex:1;min-height:0';
    body.innerHTML = '<div class="out"></div><label class="inp"><span></span><input ' + NOFILL + '></label>';
    t.body = body;
    var out = body.querySelector('.out'), inp = body.querySelector('input');
    out.innerHTML = t.html;
    out.addEventListener('mouseup', function () { if (!getSelection().toString()) inp.focus(); });
    // ввод без keydown (IME, мобильные клавиатуры, вставка текста) — тоже в скрытый буфер
    inp.addEventListener('beforeinput', function (e) { if (!t.secret) return; e.preventDefault();
      if (/^delete/.test(e.inputType || '')) t.pwbuf = (t.pwbuf || '').slice(0, -1); else if (e.data) t.pwbuf = (t.pwbuf || '') + e.data; });
    inp.addEventListener('input', function () { if (t.secret && inp.value) { t.pwbuf = (t.pwbuf || '') + inp.value; inp.value = ''; } });
    inp.addEventListener('paste', function (e) { if (!t.secret) return; e.preventDefault(); t.pwbuf = (t.pwbuf || '') + ((e.clipboardData || window.clipboardData).getData('text') || '').split(/\r?\n/)[0]; });
    inp.addEventListener('keydown', function (e) {
      if ((e.ctrlKey && e.key === 'Tab') || (e.altKey && /^Arrow(Left|Right)$/.test(e.key))) {   // переключение вкладок «Консолей»
        e.preventDefault(); e.stopPropagation(); consNext(id, e.shiftKey || e.key === 'ArrowLeft' ? -1 : 1); return; }
      if (t.more) { e.preventDefault(); e.stopPropagation(); moreKey(id, e); return; }
      if (t.secret && !e.ctrlKey && !e.metaKey && !e.altKey) {           // пароль: строка остаётся пустой, нажатия — в буфер
        if (e.key === 'Enter') { var pv = t.pwbuf || ''; t.pwbuf = ''; inp.value = ''; e.preventDefault(); e.stopPropagation(); run(id, pv); return; }
        if (e.key === 'Backspace') { t.pwbuf = (t.pwbuf || '').slice(0, -1); e.preventDefault(); e.stopPropagation(); return; }
        if (e.key.length === 1) { t.pwbuf = (t.pwbuf || '') + e.key; e.preventDefault(); e.stopPropagation(); return; }
        if (/^(ArrowUp|ArrowDown|Tab)$/.test(e.key)) { e.preventDefault(); e.stopPropagation(); return; }
      }
      if (e.key === 'Enter') { var v = inp.value; inp.value = ''; run(id, v); e.preventDefault(); }
      else if (e.ctrlKey && /^[zZя]$/.test(e.key)) { e.preventDefault(); var dz = net.devs[id];   // Ctrl+Z — выход в привилегированный режим
        if (dz && needLogin(dz) && t.auth && !dz.off) { tlog(id, net.prompt(id) + inp.value + '^Z', 'c'); inp.value = '';
          if (dz.type === 'mes' ? dz.st.mode !== 'user' && dz.st.mode !== 'priv' : dz.st.mode !== 'priv') net.exec(id, 'end'); setPr(id); } }
      else if (e.key === 'ArrowUp') { if (t.hi > 0) { t.hi--; inp.value = t.hist[t.hi]; } e.preventDefault(); }
      else if (e.key === 'ArrowDown') { if (t.hi < t.hist.length) { t.hi++; inp.value = t.hist[t.hi] || ''; } e.preventDefault(); }
      else if (needLogin(net.devs[id]) && !t.auth) { if (e.key === 'Tab' || e.key === '?') e.preventDefault(); }
      else if (e.key === 'Tab' && X.roomTab(id, inp.value)) e.preventDefault();
      else if (e.key === 'Tab') { e.preventDefault(); var r = net.tab(id, inp.value); if (r) inp.value = r; else if (net.table(id, inp.value)) { tlog(id, net.prompt(id) + inp.value, 'c'); tlog(id, realOut(net.devs[id], '?', net.help(id, inp.value)), 'h'); } }
      else if (e.key === '?' && net.table(id, inp.value)) { e.preventDefault(); tlog(id, net.prompt(id) + inp.value + '?', 'c'); tlog(id, realOut(net.devs[id], '?', net.help(id, inp.value)), 'h'); }
      e.stopPropagation();
    });
    dockTerm(id);                                   // новая консоль — вкладкой в окне «Консоли»
  }
  // ================================================================== «Консоли»: вкладки, вынос в отдельное окно и возврат
  var consOrder = [], consActive = null, TYPE = { mes: 'SW', esr: 'R', vpc: 'PC', deb: 'PC', tau: 'TAU', smg: 'SMG', phone: 'TEL', olt: 'OLT', lte: 'OLT' };
  function tEl(id) { var t = terms[id]; return t && t.body || null; }
  function focusTerm(id) { var b = tEl(id); if (b) { var o = b.querySelector('.out'); o.scrollTop = o.scrollHeight; setTimeout(function () { b.querySelector('input').focus(); }, 0); } }
  function consWin() {
    if (wins.cons) return wins.cons.el;
    var b = document.createElement('div'); b.className = 'cons'; b.innerHTML = '<div class="ctabs"></div><div class="cbody"></div>';
    makeWin('cons', 'Консоли', '', b, { w: Math.min(760, innerWidth - 60), h: Math.min(480, innerHeight - 160) });
    var strip = b.querySelector('.ctabs');
    strip.addEventListener('mousedown', tabDown);
    return wins.cons.el;
  }
  function dockTerm(id, at) {
    id = String(id); var t = term(id), fw = wins['t' + id];
    if (fw) { fw.el.remove(); delete wins['t' + id]; }
    consWin(); var i = consOrder.indexOf(id); if (i >= 0) consOrder.splice(i, 1);
    consOrder.splice(at === undefined || at > consOrder.length ? consOrder.length : at, 0, id);
    if (t.body && t.body.parentNode) t.body.parentNode.removeChild(t.body);
    consShow(id);
  }
  function consShow(id) {
    id = String(id); if (consOrder.indexOf(id) < 0) return; consActive = id;
    var cb = consWin().querySelector('.cbody'); while (cb.firstChild) cb.removeChild(cb.firstChild);
    cb.appendChild(term(id).body); term(id).unread = false;
    minWin('cons', false); renderTabs(); setPr(id); focusTerm(id);
  }
  function consNext(id, dir) { if (consOrder.indexOf(String(id)) < 0 || consOrder.length < 2) return;
    var i = (consOrder.indexOf(String(id)) + dir + consOrder.length) % consOrder.length; consShow(consOrder[i]); }
  function renderTabs() {
    if (!wins.cons) return; var strip = wins.cons.el.querySelector('.ctabs');
    strip.innerHTML = consOrder.map(function (id) { var d = net.devs[id], t = terms[id] || {}; if (!d) return '';
      return '<div class="ctab' + (id === consActive ? ' on' : '') + (t.unread ? ' new' : '') + (d.off ? ' off' : '') + '" data-id="' + esc(id) + '" title="' + esc(d.model) +
        ' — перетащите за пределы полосы, чтобы открыть отдельным окном"><i>' + (TYPE[d.sub] || TYPE[d.type] || '•') + '</i><b>' + esc(d.name) + '</b><span class="cx" data-x="1" title="Закрыть">✕</span></div>'; }).join('') +
      (consActive && net.manualFor(consActive) ? '<button class="man cman" data-man="1">Руководство</button>' : '');
    wins.cons.title = 'Консоли (' + consOrder.length + ')'; wins.cons.el.querySelector('.wt b').textContent = 'Консоли'; chips();
  }
  function closeTab(id) {
    id = String(id); var i = consOrder.indexOf(id); if (i < 0) return; consOrder.splice(i, 1);
    var t = terms[id]; if (t && t.body) { if (t.body.parentNode) t.body.parentNode.removeChild(t.body); delete t.body; }
    if (!consOrder.length) { consActive = null; closeWin('cons'); return; }
    if (consActive === id) consShow(consOrder[Math.min(i, consOrder.length - 1)]); else renderTabs();
  }
  function undockTerm(id, x, y) {
    id = String(id); var i = consOrder.indexOf(id), d = net.devs[id], t = term(id); if (i < 0 || !d) return;
    consOrder.splice(i, 1); if (t.body.parentNode) t.body.parentNode.removeChild(t.body);
    var ww = Math.min(640, innerWidth - 60), wh = Math.min(420, innerHeight - 160);
    var tw = makeWin('t' + id, d.name, d.model, t.body, { x: Math.max(10, Math.min(x, innerWidth - ww - 10)), y: Math.max(60, Math.min(y, innerHeight - wh - 50)), w: ww, h: wh,
      onMove: function (ev) { stripHint(ev); }, onDrop: function (ev) { var at = stripAt(ev); stripHint(null); if (at !== null) dockTerm(id, at); } });
    if (net.manualFor(id)) { var mb = document.createElement('button'); mb.className = 'man'; mb.title = 'Официальное руководство Eltex'; mb.textContent = 'Руководство';
      tw.querySelector('.wt').insertBefore(mb, tw.querySelector('.wt [data-w="min"]')); mb.addEventListener('click', function () { openManual(id); }); }
    if (!consOrder.length) { consActive = null; closeWin('cons'); } else if (consActive === id) consShow(consOrder[Math.min(i, consOrder.length - 1)]); else renderTabs();
    setPr(id); focusTerm(id);
  }
  // место вставки на полосе вкладок под указателем: индекс или null (указатель не над полосой)
  function stripAt(ev) {
    if (!ev || !wins.cons || wins.cons.min) return null; var strip = wins.cons.el.querySelector('.ctabs'), r = strip.getBoundingClientRect();
    if (ev.clientX < r.left - 10 || ev.clientX > r.right + 10 || ev.clientY < r.top - 18 || ev.clientY > r.bottom + 18) return null;
    var tabs = [].slice.call(strip.querySelectorAll('.ctab')), k = tabs.length;
    for (var i = 0; i < tabs.length; i++) { var b = tabs[i].getBoundingClientRect(); if (ev.clientX < b.left + b.width / 2) { k = i; break; } }
    return k;
  }
  function stripHint(ev, skip) {
    if (!wins.cons) return; var strip = wins.cons.el.querySelector('.ctabs'), at = stripAt(ev), m = strip.querySelector('.cmark');
    strip.classList.toggle('drop', at !== null);
    if (at === null) { if (m) m.remove(); return; }
    if (!m) { m = document.createElement('span'); m.className = 'cmark'; }
    var tabs = [].slice.call(strip.querySelectorAll('.ctab')).filter(function (x) { return x !== skip; });
    strip.insertBefore(m, tabs[at] || strip.querySelector('.cman') || null);
  }
  // вкладка: щелчок — показать, ✕ — закрыть, перетаскивание по полосе — порядок, за пределы полосы — отдельное окно
  function tabDown(e) {
    if (e.target.closest('[data-man]')) { openManual(consActive); return; }
    var tab = e.target.closest('.ctab'); if (!tab) return; var id = tab.dataset.id;
    if (e.target.closest('[data-x]')) { closeTab(id); e.preventDefault(); return; }
    e.preventDefault(); e.stopPropagation(); focusWin('cons');
    var sx = e.clientX, sy = e.clientY, drag = false, ghost = null;
    function mv(ev) {
      if (!drag && Math.abs(ev.clientX - sx) + Math.abs(ev.clientY - sy) < 6) return;
      if (!drag) { drag = true; ghost = tab.cloneNode(true); ghost.classList.add('ghost'); document.body.appendChild(ghost); tab.classList.add('dragging'); }
      ghost.style.left = (ev.clientX - 30) + 'px'; ghost.style.top = (ev.clientY - 12) + 'px';
      var at = stripAt(ev); ghost.classList.toggle('out', at === null); stripHint(ev, tab);
    }
    function up(ev) {
      window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up);
      if (ghost) ghost.remove(); tab.classList.remove('dragging'); stripHint(null);
      if (!drag) { consShow(id); return; }
      var at = stripAt(ev);
      if (at === null) { undockTerm(id, ev.clientX - 120, ev.clientY - 14); return; }
      var i = consOrder.indexOf(id); consOrder.splice(i, 1); if (at > i) at--; consOrder.splice(at, 0, id); renderTabs(); focusTerm(consActive);
    }
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  }
  // ввод консоли — без type=password и без признаков формы входа: менеджер паролей браузера к нему не цепляется
  var NOFILL = 'type="text" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" data-lpignore="true" data-1p-ignore="true" data-bwignore="true" data-form-type="other" aria-autocomplete="none"';
  // все поля эмулятора (nano, тест, комментарии, поиск) — без автозаполнения браузера и менеджеров паролей
  document.addEventListener('focusin', function (e) { var x = e.target; if (!x || !/^(INPUT|TEXTAREA)$/.test(x.tagName) || /^(checkbox|radio|file|number)$/.test(x.type)) return;
    if (x.type === 'password') x.type = 'text';
    [['autocomplete', 'off'], ['autocorrect', 'off'], ['autocapitalize', 'off'], ['data-lpignore', 'true'], ['data-1p-ignore', 'true'], ['data-form-type', 'other']].forEach(function (a) { if (!x.hasAttribute(a[0])) x.setAttribute(a[0], a[1]); }); }, true);
  function tlog(id, text, cls) {
    var t = term(id), h = '<div class="' + (cls || '') + '">' + esc(text) + '</div>'; t.html += h; X.onOut(id, text, cls);
    var b = tEl(id); if (b) { var out = b.querySelector('.out'); out.insertAdjacentHTML('beforeend', h); out.scrollTop = out.scrollHeight;
      if (consOrder.indexOf(String(id)) >= 0 && consActive !== String(id) && !t.unread) { t.unread = true; renderTabs(); } }
  }
  function setPr(id) { var w = tEl(id) ? { el: tEl(id) } : null, d = net.devs[id]; if (!w || !d) return; var t = term(id), rp = X.roomPrompt(id), p = rp !== null ? rp : needLogin(d) && !t.auth ? loginPrompt(d, t) : net.prompt(id), inp = w.el.querySelector('input');
    if (t.more && !d.off && rp === null) p = net.moreText(id);
    if (t.ask && !d.off) p = t.ask.q;
    if (t.cep && !d.off) p = net.prompt(id).replace(/#$/, '') + '(change-expired-password)# ';
    var sec = !d.off && /(password|passphrase[^:]*): ?$/i.test(p); if (sec !== !!t.secret) { t.secret = sec; t.pwbuf = ''; inp.value = ''; }
    w.el.querySelector('.inp span').textContent = d.off ? '[выключено] ' : p; inp.disabled = !!d.off; inp.readOnly = !!t.more;
    if (wins.cons && consOrder.indexOf(String(id)) >= 0) { var tb = wins.cons.el.querySelector('.ctab[data-id="' + String(id) + '"]'); if (tb) tb.classList.toggle('off', !!d.off); } }
  var hooks = { clear: function () { var id = hooks.cur; term(id).html = ''; var b = tEl(id); if (b) b.querySelector('.out').innerHTML = ''; },
                edit: function (name, text, save) { openNano(name, text, save); } };
  function run(id, line) {
    var d = net.devs[id], t = term(id); if (!d || d.off || readOnly) return;
    if (X.roomRun(id, line)) return;                // комната: команду выполняет сервер, вывод придёт всем
    X.onCmd(id, line, !!t.secret || (needLogin(d) && !t.auth && t.user !== null));
    var w = wins['t' + id], pw = !!t.secret;
    if (needLogin(d) && !t.auth) {                 // вход в консоль
      tlog(id, loginPrompt(d, t) + (t.user === null ? line : ''), 'c');
      if (t.user === null) { t.user = line.trim(); if (!t.user) t.user = null; }
      else { var okL = checkLogin(d, t.user, line); t.user = null;
        if (okL) { t.auth = true; var bn = d.type === 'esr' ? d.st.run.banner : d.st.banner; if (bn && bn.exec) tlog(id, bn.exec, '');
          // ESR, ESR ФСТЭК, WLC, SCS-32: заводской пароль admin нужно сменить при первом входе (в «Тесте» — пропускается)
          if (mode === 'work' && d.type === 'esr' && d.sub !== 'me' && !d.st.pwChanged && line === 'password' && (d.st.run.users.admin || {}).pw === 'password') t.cep = {}; }
        else tlog(id, d.type === 'esr' ? 'Login incorrect' : '% Authentication failed', 'e'); }
      setPr(id); return;
    }
    if (t.cep) { tlog(id, net.prompt(id).replace(/#$/, '') + '(change-expired-password)# ' + line, 'c');   // режим смены истёкшего пароля
      var w = line.trim().split(/\s+/), U2 = d.st.run.users.admin, r2 = '';
      if (w[0] === 'password' && w[1]) { if (EL.pwCheck && !EL.pwCheck(d.st, w[1])) r2 = 'Syntax error: Illegal parameter'; else t.cep.pw = w[1]; }
      else if (w[0] === 'commit' && t.cep.pw) { U2.pw = t.cep.pw; d.st.cand.users.admin.pw = t.cep.pw; t.cep.done = true;
        r2 = 'Configuration has been successfully applied and saved to flash. Commit timer started, changes will be reverted in 600 seconds.'; }
      else if (w[0] === 'confirm' && t.cep.done) { d.st.pwChanged = true; t.cep = null; r2 = 'Configuration has been confirmed. Commit timer canceled.'; }
      else if (w[0] === 'logout') { t.cep = null; t.auth = false; t.user = null; }
      else if (line.trim()) r2 = 'Syntax error: Unknown command';
      if (r2) tlog(id, r2, /^Syntax/.test(r2) ? 'e' : ''); setPr(id); return; }
    if (t.ask) { var q = t.ask; t.ask = null; tlog(id, q.q + line, 'c'); if (/^\s*y/i.test(line)) q.yes(); setPr(id); return; }   // подтверждение (y/n)
    var p = net.prompt(id);
    tlog(id, p + (pw ? '' : line), 'c'); if (line.trim()) t.hist.push(line); t.hi = t.hist.length;
    hooks.cur = id;
    if (d.type === 'mes' && /^\s*rel(o(a(d)?)?)?\s*$/i.test(line) && d.st.mode === 'priv') {   // руководство 6.6.8.8: reload спрашивает подтверждение
      t.ask = { q: 'This command will reset the whole system and disconnect your current session. Do you want to continue (y/n) [n]? ', yes: function () { boot(id, true); } }; setPr(id); return; }
    if (d.type === 'esr' && /^\s*reload\s+system\s*$/i.test(line) && d.st.mode === 'priv') { boot(id, true); return; }
    var h0 = net.hostOf(id), r = realOut(d, line, net.exec(id, line, hooks)); syncHost(id, h0);
    if (r) outPaged(id, r, /^%|Unrecognized|Bad command|command not found|Permission denied|\bError\b|not reachable|timeout|100% packet loss|Login incorrect|Unable|refused/i.test(r) ? 'e' : '');
    setPr(id); draw(); refresh();
  }
  // hostname в консоли — сразу подпись на схеме (если имя свободно и допустимо)
  function syncHost(id, h0) { var d = net.devs[id], h = d && net.hostOf(id); if (!d || !h || h === h0 || h === d.name) return;
    var err = net.rename(id, h); if (err) { toast('Подпись на схеме не изменена: ' + err); return; }
    if (wins['t' + id]) { wins['t' + id].title = d.name; wins['t' + id].el.querySelector('.wt b').textContent = d.name; } renderTabs(); chips(); }
  // постраничный вывод длинных show: пробел — страница, Enter — строка, q — выход (ESR: R — всё остальное)
  function outPaged(id, r, cls) {
    var n = net.pageLen(id), L = String(r).split('\n');
    if (!n || L.length < n) { tlog(id, r, cls); return; }
    tlog(id, L.slice(0, n - 1).join('\n'), cls); term(id).more = { L: L, i: n - 1, n: n, cls: cls };
  }
  function moreKey(id, e) {
    var t = term(id), m = t.more, d = net.devs[id], k = e.key, step = 0;
    if (!m || !d) { t.more = null; return; }
    if (k === 'Enter') step = 1;
    else if (k === ' ') step = m.n - 1;
    else if (/^[qQйЙ]$/.test(k) || (e.ctrlKey && /^[zZя]$/.test(k))) step = -1;
    else if (d.type === 'esr' && /^[rRкК]$/.test(k)) step = m.L.length;
    else if (d.type === 'mes' && d.st.dialect === '8' && k.length === 1) step = m.n - 1;
    else return;
    if (step > 0) { tlog(id, m.L.slice(m.i, m.i + step).join('\n'), m.cls); m.i += step; }
    if (step < 0 || m.i >= m.L.length) t.more = null;
    setPr(id);
  }
  // системные сообщения устройств (линк, STP, OSPF, VRRP) — в их консоли
  function pollEv() {
    net.events().forEach(function (e) { var d = net.devs[e.id], t = term(e.id); if (!d) return;
      if (!t.html) t.html = '<div class="s">' + esc(banner(d)) + '</div>';
      tlog(e.id, e.msg, 's'); });
  }
  function boot(id, reload) {
    if (X.roomAct(reload ? { k: 'power', dev: id, reboot: true } : { k: 'power', dev: id, on: true })) return;
    var d = net.devs[id]; tlog(id, reload ? 'System is going to reboot…' : 'Power on…', 's');
    net.power(id, false); draw(); setPr(id);
    setTimeout(function () {
      if (!net.devs[id]) return;
      if (reload) net.reboot(id); else net.power(id, true);
      var tt = term(id); tt.auth = false; tt.user = null;   // после загрузки снова вход
      tlog(id, d.type === 'esr' ? 'Loading ' + d.model + ' firmware 1.24.2 … OK' : d.type === 'mes' ? 'Booting ' + d.model + ' … loading startup-config … OK' :
        d.type === 'deb' ? 'Debian GNU/Linux 11 ' + d.st.host + ' tty1' : 'VPCS ready', 's');
      draw(); setPr(id); refresh();
    }, 1100);
  }
  function powerAll() { var L = net.list().filter(function (d) { return d.off; }); if (!L.length) { toast('Всё оборудование уже включено'); return; }
    L.forEach(function (d, i) { setTimeout(function () { if (net.devs[d.id] && net.devs[d.id].off) boot(d.id, false); }, i * 150); }); toast('Включаю: ' + L.length + ' устр.'); }
  $('bPower').addEventListener('click', powerAll);
  $('bTerm').addEventListener('click', function () { if (sel) openTerm(sel); else toast('Выберите устройство на схеме (щелчок) или дважды щёлкните по нему'); });

  // ================================================================== nano, свойства, ping
  function openNano(name, text, save) {
    var body = document.createElement('div'); body.className = 'nano'; body.style.cssText = 'display:flex;flex-direction:column;flex:1;min-height:0';
    body.innerHTML = '<textarea spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="off" data-lpignore="true" data-1p-ignore="true" data-form-type="other"></textarea><div class="keys"><span><button data-n="s">^S</button> Сохранить</span><span><button data-n="x">^X</button> Выход</span></div>';
    makeWin('nano', 'GNU nano 5.4', name, body, { w: 680, h: 440 }); var ta = body.querySelector('textarea'); ta.value = text; ta.focus();
    function done(s) { if (s) { save(ta.value); toast('Файл сохранён'); } else closeWin('nano'); }
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-n]'); if (b) done(b.dataset.n === 's'); });
    ta.addEventListener('keydown', function (e) { if (e.ctrlKey && /^[sSы]$/.test(e.key)) { e.preventDefault(); done(true); } if (e.ctrlKey && /^[xXч]$/.test(e.key)) { e.preventDefault(); done(false); } e.stopPropagation(); });
  }
  // «Свойства»: карточка модели — описание, ветка ПО, порты с типами и скоростью, загрузка из последней симуляции, ссылка на eltex.ru;
  // заводские логин и пароль (поле login каталога) — только в «Тесте»
  var PSPEED = { fa: ['Fast Ethernet', 100], gi: ['Gigabit Ethernet', 1000], tw: ['2.5G Ethernet', 2500], te: ['10G Ethernet', 10000], twe: ['25G Ethernet', 25000],
    fo: ['40G Ethernet', 40000], hu: ['100G Ethernet', 100000], eth: ['Ethernet', 1000], ens: ['Ethernet', 1000], console: ['Консоль RS-232', 0], aux: ['Консоль RS-232', 0] };
  function portKind(m, list, p) {
    var i = list.indexOf(p), pre = (p.match(/^[a-z]+/) || ['gi'])[0], sp = PSPEED[pre] || (/^\d/.test(p) ? ['10G Ethernet', 10000] : ['Ethernet', 1000]), t = '';
    if (m.pt && i >= 0) { var c = 0; m.pt.some(function (g) { c += g[0]; if (i < c) { t = g[1]; return true; } return false; }); }
    return { name: sp[0], max: sp[1], type: t };
  }
  function openProps(id) {
    var d = net.devs[id], m = EL.MODELS[d.model] || {}, body = document.createElement('div'); body.className = 'pad';
    var list = net.portsOf(d), util = {};
    ((net._simLast || {}).links || []).forEach(function (x) { var l = net.links[x.li]; if (!l) return; util[l.a.dev + '|' + l.a.port] = util[l.b.dev + '|' + l.b.port] = x.util; });
    var rows = list.map(function (p) { var pr = net.peer(id, p), k = portKind(m, list, p), ph = pr && net.phys ? net.phys(id, p) : null, u = util[id + '|' + p];
      return '<tr><td>' + p + '</td><td>' + esc(k.name) + (k.type ? '<br><small style="color:var(--dim)">' + esc(k.type) + '</small>' : '') + '</td><td>' +
        (ph && ph.up ? (ph.speed >= 1000 ? ph.speed / 1000 + ' Гбит/с' : ph.speed + ' Мбит/с') + (ph.dup[id] === 'half' ? ', half' : '') : '—') + '</td><td>' +
        (pr ? esc(net.devs[pr.dev].name + ' ' + pr.port) : '—') + '</td><td>' + (pr ? (net.linkUp(id, p) ? '<span style="color:var(--ok)">up</span>' : '<span style="color:var(--bad)">down</span>') : '') +
        '</td>' + (mode === 'test' ? '<td>' + (u === undefined ? '—' : u.toFixed(u < 1 ? 3 : 1) + ' %') + '</td>' : '') + '</tr>'; }).join('');
    var sum = {}; list.forEach(function (p) { var k = portKind(m, list, p).name; sum[k] = (sum[k] || 0) + 1; });
    var login = mode === 'test' && m.login && m.login.length ? '<h3>Заводская учётная запись</h3><table>' + m.login.map(function (l) {
      return '<tr><td>' + esc(l.u) + '</td><td>' + (l.p ? '<code>' + esc(l.p) + '</code>' : '<i>пустой пароль</i>') + '</td><td>' + esc(l.a || '') + '</td></tr>'; }).join('') + '</table>' : '';
    body.innerHTML = '<div class="k">Карточка модели</div><h2>' + esc(d.model) + '</h2>' +
      '<p>' + esc(m.full || m.note || '') + '</p>' +
      '<table><tr><td>Группа</td><td>' + esc(m.group || '—') + '</td></tr><tr><td>Ветка ПО</td><td>' + esc(m.sw || '—') + (m.dialect ? ' (CLI ' + esc(m.dialect) + '.x)' : '') + '</td></tr>' +
      '<tr><td>Портов</td><td>' + list.length + ': ' + Object.keys(sum).map(function (k) { return sum[k] + ' × ' + k; }).join(', ') + '</td></tr>' +
      (m.url ? '<tr><td>Сайт</td><td><a href="' + esc(m.url) + '" target="_blank" rel="noopener">' + esc(m.url.replace(/^https?:\/\//, '')) + '</a></td></tr>' : '') + '</table>' +
      '<label>Имя на схеме (= hostname)</label><input class="q" id="pname" value="' + esc(d.name) + '">' +
      '<div class="row"><button class="pri" data-p="name">Сохранить имя</button><button data-p="term">Консоль</button>' + (d.off ? '<button data-p="on">Включить</button>' : '<button data-p="off">Выключить</button>') + '</div>' +
      '<p>Состояние: ' + (d.off ? '<b style="color:var(--bad)">выключено</b>' : '<b style="color:var(--ok)">работает</b>') + (d.type === 'mes' ? ' · MAC моста ' + esc(d.st.bmac || '') : '') + '</p>' +
      '<h3>Порты</h3><table><tr><th>Порт</th><th>Тип</th><th>Скорость</th><th>Соединён с</th><th>Линк</th>' + (mode === 'test' ? '<th>Загрузка*</th>' : '') + '</tr>' + rows + '</table>' +
      (mode === 'test' ? '<p style="color:var(--dim)">* по последней «Симуляции трафика» (доля времени, когда порт передавал, от его скорости).</p>' : '') + login;
    makeWin('p' + id, 'Свойства', d.name, body, { w: 600, h: 600 });
    var inp = body.querySelector('#pname'); inp.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-p]'); if (!b) return; var a = b.dataset.p;
      if (a === 'name' && X.roomAct({ k: 'dev.rename', id: id, name: inp.value.trim() })) return;
      if (a === 'name') { var err = net.rename(id, inp.value); if (err) { toast(err); return; } net.setHost(id, d.name); setPr(id); draw(); toast('Имя и hostname изменены');
        if (wins['t' + id]) { wins['t' + id].title = d.name; wins['t' + id].el.querySelector('.wt b').textContent = d.name; } renderTabs(); chips(); }
      if (a === 'term') openTerm(id);
      if (a === 'off') { if (X.roomAct({ k: 'power', dev: id, on: false })) return; net.power(id, false); setPr(id); draw(); openProps(id); }
      if (a === 'on') { boot(id, false); setTimeout(function () { openProps(id); }, 1200); }
    });
  }
  // «Ping отсюда»: цель — любое устройство схемы (адреса интерфейсов; без адреса — «нет IP») или адрес вручную.
  // Результат — как скаляры и вектор OMNeT++: отправлено / получено / потеряно, % потерь, RTT min/avg/max и RTT каждого эхо
  function openPing(id) {
    var d = net.devs[id], opts = [], body = document.createElement('div'); body.className = 'pad';
    net.list().forEach(function (x) { if (x.id === id) return; var fs = net.ifaces(x.id);
      if (!fs.length) opts.push('<option disabled>' + esc(x.name) + ' — нет IP</option>');
      fs.forEach(function (f) { opts.push('<option value="' + f.ip + '">' + esc(x.name + ' · ' + f.name + ' · ' + f.ip) + '</option>'); }); });
    body.innerHTML = '<div class="k">Ping c ' + esc(d.name) + '</div><label>Кому (все устройства схемы)</label><select id="pdst">' + (opts.join('') || '<option disabled>на схеме нет других устройств</option>') + '</select>' +
      '<label>Или адрес</label><input class="q" id="pip" placeholder="A.B.C.D">' +
      '<div class="row"><label style="margin:0">Эхо</label><input class="q" id="pcnt" value="5" style="width:60px"><label style="margin:0">Размер, байт</label><input class="q" id="psz" value="56" style="width:70px"></div>' +
      '<div class="row"><button class="pri" data-g="go">Отправить</button></div><div id="pres"></div>';
    makeWin('ping', 'Ping', d.name, body, { w: 470, h: 470 });
    [].forEach.call(body.querySelectorAll('input'), function (x) { x.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter') go(); }); });
    body.addEventListener('click', function (e) { if (e.target.closest('[data-g]')) go(); });
    function go() {
      var ip = body.querySelector('#pip').value.trim() || body.querySelector('#pdst').value, n = Math.max(1, Math.min(100, +body.querySelector('#pcnt').value || 5)),
        sz = Math.max(0, Math.min(65000, +body.querySelector('#psz').value || 56));
      if (EL.ip.ip2n(ip || '') === null) { toast('Укажите адрес'); return; }
      var r = net.ping(id, ip); showTrace(r, id, ip);
      var sm = net.simulate ? net.simulate([{ kind: 'ping', src: id, dst: ip, count: n, interval: 1, size: sz }]) : null, f = sm && sm.flows[0];
      if (!f) { body.querySelector('#pres').innerHTML = '<p>' + (r.ok ? 'Ответ получен' : 'Нет ответа: ' + esc(r.why || '')) + '</p>'; return; }
      var ms = function (v) { return v === undefined ? '—' : (v * 1000).toFixed(3) + ' мс'; };
      var drops = Object.keys(f.drops).map(function (k) { return esc(k) + ' × ' + f.drops[k]; }).join('<br>');
      body.querySelector('#pres').innerHTML = '<h3>Скаляры</h3><table>' +
        [['Отправлено', f.sent], ['Получено', f.recv], ['Потеряно', f.sent - f.recv], ['Потери', f.loss + ' %'],
         ['RTT min / avg / max', ms(f.min) + ' / ' + ms(f.avg) + ' / ' + ms(f.max)], ['Джиттер', ms(f.jitter)]].map(function (x) { return '<tr><td>' + x[0] + '</td><td><b>' + x[1] + '</b></td></tr>'; }).join('') +
        '</table>' + (drops ? '<p style="color:var(--bad)">Потери: ' + drops + '</p>' : '') + (f.rtt.length > 1 ? '<h3>Вектор: RTT по эхо-запросам</h3>' + vecSvg(f.rtt.map(function (v) { return v * 1000; }), 'мс') : '') +
        '<p style="color:var(--dim)">Путь пакета — внизу экрана; время — дискретно-событийная модель (передача, распространение, очереди).</p>';
    }
  }
  // мини-график вектора (значение по номеру/времени) — без внешних библиотек
  function vecSvg(v, unit, w, h) { w = w || 420; h = h || 110; if (!v.length) return '';
    var mx = Math.max.apply(null, v) || 1, mn = Math.min(0, Math.min.apply(null, v)), sx = (w - 40) / Math.max(1, v.length - 1), sy = (h - 24) / (mx - mn || 1);
    var pts = v.map(function (y, i) { return (34 + i * sx).toFixed(1) + ',' + (h - 14 - (y - mn) * sy).toFixed(1); }).join(' ');
    return '<svg viewBox="0 0 ' + w + ' ' + h + '" style="width:100%;height:auto"><line x1="34" y1="' + (h - 14) + '" x2="' + w + '" y2="' + (h - 14) + '" stroke="var(--dim)"/><line x1="34" y1="4" x2="34" y2="' + (h - 14) + '" stroke="var(--dim)"/>' +
      '<text x="2" y="12" fill="var(--dim)" font-size="10">' + mx.toFixed(2) + '</text><text x="2" y="' + (h - 14) + '" fill="var(--dim)" font-size="10">' + mn.toFixed(0) + '</text>' +
      '<text x="' + (w - 30) + '" y="' + (h - 2) + '" fill="var(--dim)" font-size="10">' + esc(unit || '') + '</text>' +
      '<polyline points="' + pts + '" fill="none" stroke="var(--cy)" stroke-width="2"/>' + v.map(function (y, i) { return '<circle cx="' + (34 + i * sx).toFixed(1) + '" cy="' + (h - 14 - (y - mn) * sy).toFixed(1) + '" r="2.5" fill="var(--cy)"/>'; }).join('') + '</svg>'; }

  // ================================================================== таблицы устройства (живые)
  function tbl(head, rows, empty) {
    return '<table><tr>' + head.map(function (h) { return '<th>' + h + '</th>'; }).join('') + '</tr>' +
      (rows.length ? rows.map(function (r) { return '<tr' + (r.hot ? ' class="hot"' : '') + '>' + r.map(function (c) { return '<td>' + esc(c) + '</td>'; }).join('') + '</tr>'; }).join('')
                   : '<tr><td colspan="' + head.length + '" style="color:var(--dim)">' + empty + '</td></tr>') + '</table>';
  }
  function tablesHtml(id) {
    var d = net.devs[id]; if (!d) return '';
    var h = '<div class="k">' + esc(d.model) + (d.off ? ' · выключено' : '') + '</div><h2>' + esc(d.name) + '</h2>';
    var hot = tview ? tview.hot : {};
    function mark(row, key) { if (hot[key]) row.hot = true; return row; }
    var arp = net.arpRows(id).map(function (r) { var e = net.arp[id][r.ip];
      return mark([r.ip, r.mac, r.ifn, net.ttl(id, 'a', e) + (d.type === 'deb' ? ' · ' + net.neighState(id, e) : '')], 'a|' + id + '|' + r.ip); });
    if (d.type === 'mes') {
      h += '<h3>MAC-таблица (коммутация) · aging ' + net.macAge(id) + ' с</h3>' + tbl(['VLAN', 'MAC', 'Порт', 'Осталось, с'], net.macRows(id).map(function (r) { return mark([r.vlan, r.mac, r.port + (r.st ? ' · static' : r.sec ? ' · secure' : ''), isFinite(net.ttl(id, 'm', r)) ? net.ttl(id, 'm', r) : '—'], 'm|' + id + '|' + r.vlan + '|' + r.mac); }),
        'пусто — коммутатор запоминает MAC отправителя каждого кадра, прошедшего через порт');
      var by = {}; Object.keys(d.st.vlans).forEach(function (v) { by[v] = []; });
      net.lports(id).forEach(function (L) { var c = L.cfg; if (c.mode === 'access') (by[c.access] = by[c.access] || []).push(L.name);
        else (c.mode === 'trunk' ? (c.allAll ? Object.keys(d.st.vlans).map(Number) : c.allowed.concat([c.native])) : c.gtag.concat(c.guntag)).forEach(function (v) { (by[v] = by[v] || []).push(L.name + (c.mode === 'trunk' && v !== c.native || c.gtag && c.gtag.indexOf(v) >= 0 ? '(T)' : '')); }); });
      h += '<h3>VLAN и порты</h3>' + tbl(['VLAN', 'Имя', 'Порты'], Object.keys(by).map(Number).sort(function (a, b) { return a - b; }).map(function (v) {
        var p = by[v].filter(function (x) { return net.linked(id, x.replace('(T)', '')) || x.indexOf('po') === 0; });
        return [v, d.st.vlans[v] || '—', p.join(', ') || '(подключённых нет)']; }), '');
      if (Object.keys(d.st.svi).length) h += '<h3>ARP-таблица</h3>' + tbl(['IP', 'MAC', 'Интерфейс', 'Осталось, с'], arp, 'пусто');
    } else {
      h += '<h3>ARP-таблица</h3>' + tbl(['IP', 'MAC', 'Интерфейс', 'Осталось, с'], arp, 'пусто — заполняется ARP-запросами и ответами (ping)');
    }
    if (d.type !== 'mes' || Object.keys(d.st.svi).length) {
      var by2 = net.best(id), rows = Object.keys(by2).map(function (k) { var r = by2[k]; return [r.p, r.net, r.nh ? 'через ' + r.nh : 'подключена', r.ifn || '—', r.ad + '/' + r.m]; });
      h += '<h3>Таблица маршрутизации</h3>' + tbl(['Код', 'Сеть', 'Следующий узел', 'Интерфейс', 'AD/метрика'], rows, 'нет маршрутов — не задан адрес или интерфейс без линка');
    }
    if (tview && tview.gone[id]) h += '<p class="gone">На этом шаге удалено: ' + tview.gone[id].map(esc).join('; ') + '</p>';
    h += '<p style="margin-top:8px">' + (tview ? 'Таблицы показаны на шаге ' + (trace.i + 1) + ' трассы — подсвечено то, что записалось этим шагом.'
      : 'Таблицы меняются от пакетов: запустите ping и смотрите, кто что запомнил.') + '</p>';
    return h;
  }
  function openTables(id) {
    var body = document.createElement('div'); body.className = 'pad'; body.dataset.tid = id; body.innerHTML = tablesHtml(id);
    var d = net.devs[id]; makeWin('tb' + id, 'Таблицы', d.name, body, { w: 520, h: 480 });
  }
  // во время трассы окно таблиц показывает состояние на текущем шаге: база (до пакета) + изменения шагов 0..i
  var tview = null;
  function setTab(key, val) { var p = key.split('|'), t = (p[0] === 'a' ? net.arp : net.mac)[p[1]]; if (!t) return;
    var k = p.slice(2).join('|'); if (val === null) delete t[k]; else t[k] = JSON.parse(val); }
  function stepView() {
    if (!trace || !trace.base || trace.i >= trace.steps.length - 1) return null;
    var live = { arp: net.arp, mac: net.mac }, hot = {}, gone = {};
    net.arp = EL.clone(trace.base.arp); net.mac = EL.clone(trace.base.mac);
    trace.steps.slice(0, trace.i + 1).forEach(function (st, j) { (st.tab || []).forEach(function (c) { setTab(c.k, c.n);
      if (j !== trace.i) return; var p = c.k.split('|');
      if (c.n !== null) hot[c.k] = 1;
      else (gone[p[1]] = gone[p[1]] || []).push((p[0] === 'a' ? 'ARP ' : 'MAC ') + p.slice(2).join(' ')); }); });
    return { live: live, hot: hot, gone: gone };
  }
  function refreshTables() {
    var v = stepView(); tview = v;
    try { Object.keys(wins).forEach(function (k) { if (k.indexOf('tb') !== 0) return; var b = wins[k].el.querySelector('[data-tid]');
      if (b) b.innerHTML = tablesHtml(b.dataset.tid); }); }
    finally { if (v) { net.arp = v.live.arp; net.mac = v.live.mac; } tview = null; }
  }
  function traceBase(steps) {   // откатываем изменения всех шагов назад — получаем таблицы до отправки пакета
    var live = { arp: net.arp, mac: net.mac }, base;
    net.arp = EL.clone(live.arp); net.mac = EL.clone(live.mac);
    steps.slice().reverse().forEach(function (st) { (st.tab || []).forEach(function (c) { setTab(c.k, c.o); }); });
    base = { arp: net.arp, mac: net.mac }; net.arp = live.arp; net.mac = live.mac; return base;
  }

  // ================================================================== трасса пакета
  net.onTrace = function (r, id, dst) { showTrace(r, id, dst); };
  function showTrace(r, id, dst) {
    if (mode !== 'test') return;
    if (X.onTrace(r, id, dst) === true) return;   // открыта «Симуляция пакетов» — события идут туда
    stopTrace();
    if (r.steps.flush) r.steps.flush();
    trace = { steps: r.steps.length ? r.steps : [{ k: r.ok ? 'ok' : 'drop', t: r.ok ? 'Адрес принадлежит самому устройству' : (r.why || 'нет ответа') }], i: 0, title: net.devs[id].name + ' → ' + dst, ok: r.ok };
    trace.base = r.steps.length ? traceBase(r.steps) : null;
    $('trace').classList.add('on'); play();
  }
  function stopTrace() { if (trace && trace.timer) { clearTimeout(trace.timer); trace.timer = null; } $('pk').innerHTML = ''; }
  function renderStep(anim) {
    var s = trace.steps[trace.i], cls = { arp: 'arp', arpr: 'arp', ip: 'ip', drop: 'drop', ok: 'ok', route: '', nat: 'nat' }[s.k];
    $('trN').textContent = trace.title + ' · шаг ' + (trace.i + 1) + '/' + trace.steps.length + (trace.i === trace.steps.length - 1 ? (trace.ok ? ' · ДОСТАВЛЕНО' : ' · НЕ ДОСТАВЛЕНО') : '');
    $('trT').className = 't ' + cls; $('trT').textContent = s.t;
    $('trNotes').textContent = (s.notes || []).length && (s.k === 'drop' || s.k === 'arp') ? 'Отброшено по пути: ' + s.notes.join('; ') : '';
    X.onStep(s);
    refreshTables();
    return anim && s.segs ? animSegs(s.segs, s.k === 'arp', { arp: '#ffc65c', arpr: '#ffc65c', ip: '#6fe3ea' }[s.k] || '#7dffb0') : 0;
  }
  function depth(segs, i) { var d = 0, cur = segs[i];
    for (var g = 0; g < 20; g++) { var par = segs.slice(0, segs.indexOf(cur)).filter(function (s) { return s.to === cur.from; }).pop(); if (!par) break; d++; cur = par; } return d; }
  function animSegs(segs, flood, color) {
    var g = $('pk'); g.innerHTML = ''; var dur = 650, gap = flood ? 160 : dur, total = 0;
    segs.forEach(function (sg, i) {
      var a0 = net.devs[sg.from], b0 = net.devs[sg.to]; if (!a0 || !b0) return;
      var of = net.links[sg.li] ? linkOff(sg.li) : { x: 0, y: 0 }, a = { x: a0.x + of.x, y: a0.y + of.y }, b = { x: b0.x + of.x, y: b0.y + of.y };
      var t0 = (flood ? depth(segs, i) : i) * gap; total = Math.max(total, t0 + dur);
      var dot = el('g', { 'class': 'pkt', opacity: 0 }, g); el('path', { d: 'M-9 -6h18v12h-18z', fill: color }, dot);
      if (sg.tag !== null) el('text', { x: 12, y: -10 }, dot).textContent = 'VLAN ' + sg.tag;
      var st = performance.now() + t0;
      (function step(now) { var k = (now - st) / dur;
        if (k < 0) { requestAnimationFrame(step); return; } if (k > 1) { dot.setAttribute('opacity', .3); return; }
        dot.setAttribute('opacity', 1); dot.setAttribute('transform', 'translate(' + (a.x + (b.x - a.x) * k) + ',' + (a.y + (b.y - a.y) * k) + ')');
        requestAnimationFrame(step); })(performance.now());
    });
    return total;
  }
  function play() { if (!trace) return; var dur = renderStep(true);
    if (trace.i < trace.steps.length - 1) trace.timer = setTimeout(function () { trace.i++; play(); }, Math.max(dur, 900) + 500); }
  $('trace').addEventListener('click', function (e) {
    var b = e.target.closest('[data-t]'); if (!b || !trace) return; var a = b.dataset.t; stopTrace();
    if (a === 'close') { $('trace').classList.remove('on'); trace = null; refreshTables(); return; }
    if (a === 'first') trace.i = 0; if (a === 'prev') trace.i = Math.max(0, trace.i - 1);
    if (a === 'next') trace.i = Math.min(trace.steps.length - 1, trace.i + 1);
    if (a === 'play') { trace.i = 0; play(); return; } renderStep(true);
  });

  // ================================================================== левая панель
  var tab = 'dev';
  $('edge').addEventListener('mouseenter', function () { $('side').classList.add('open'); });
  $('edge').addEventListener('click', function () { $('side').classList.toggle('open'); });
  $('side').addEventListener('mouseleave', function () { $('side').classList.remove('open'); });
  $('spin').addEventListener('click', function () { var p = $('side').classList.toggle('pin'); this.classList.toggle('on', p); });
  $('stabs').addEventListener('click', function (e) { var b = e.target.closest('[data-t]'); if (!b) return;
    if (b.dataset.t === 'help') { openHelp(); return; }
    tab = b.dataset.t; [].forEach.call(this.querySelectorAll('[data-t]'), function (x) { x.classList.toggle('on', x === b); }); renderSide(); });
  function renderSide() {
    var s = $('sbody'), h = '';
    if (tab === 'dev') {
      h = '<input class="q" id="sq" placeholder="Поиск модели…">';
      var more = false;
      catalogGroups().forEach(function (g) {
        if (g.more && !more) { more = true; h += '<details class="more" id="smore"><summary>Ещё оборудование</summary>'; }
        h += '<h4>' + esc(g.name) + '</h4>' + g.items.map(function (k) { var m = EL.MODELS[k];
          return '<button class="pi" draggable="true" data-model="' + k + '" title="' + esc(m.full || m.note) + '">' + iconSvg(m.type, k) +
            '<span><b>' + k + (m.sw ? '<span class="sw">' + m.sw.replace('ПО ', '') + '</span>' : '') + '</b><small>' + esc(m.note) + '</small></span></button>'; }).join('');
      });
      if (more) h += '</details>';
      h += '<p class="note">Перетащите модель на поле или щёлкните — появится в центре. ПКМ по пустому полю — то же с поиском. ' +
           'Коммутаторы: CLI по ветке ПО (10.x · 6.x/4.x · 8.x FASTPATH), порты как на устройстве. Это модель по документации Eltex, не прошивка.</p>';
    }
    if (tab === 'lab') {
      if (lab) h = '<button class="act" data-s="labwin">Окно задания ' + lab.id + '</button>';
      h += '<h4>Лабораторные NTF-2</h4>' + EL.labs.LABS.map(function (L) { return '<button class="lbtn" data-lab="' + L.id + '"><b>' + L.id + '</b>' + esc(L.title) + '</button>'; }).join('');
    }
    if (tab === 'task') h = '<h4>Случайное задание на коммутатор</h4><p class="note">Как тренажёры дек «Базовая настройка» и «VLAN»: проверяется итоговое состояние.</p>' +
      '<button class="act" data-s="tbase">Базовая настройка</button><button class="act" data-s="tvlan">VLAN</button>';
    if (tab === 'file') h = '<h4>Схема</h4><button class="act pri" data-s="png">Сохранить схему (PNG)</button><button class="act" data-s="save">Сохранить проект (.json)</button><button class="act" data-s="open">Открыть проект</button>' +
      '<button class="act" data-s="fit">Показать всю схему</button><button class="act red" data-s="clear">Очистить</button>' +
      '<p class="note">PNG — картинка схемы для отчёта. Проект .json хранит устройства, кабели и все настройки — его можно открыть снова. В браузере ничего не сохраняется само.</p>';
    s.innerHTML = h + X.side(tab);
    var q = $('sq'); if (q) q.addEventListener('input', function () { var v = q.value.trim().toLowerCase();
      [].forEach.call(s.querySelectorAll('.pi'), function (b) { b.style.display = !v || b.textContent.toLowerCase().indexOf(v) >= 0 ? '' : 'none'; });
      [].forEach.call(s.querySelectorAll('h4'), function (h4) { var n = h4.nextElementSibling, any = !v; while (n && n.classList.contains('pi')) { if (n.style.display !== 'none') any = true; n = n.nextElementSibling; }
        h4.style.display = any ? '' : 'none'; });
      if ($('smore')) $('smore').open = !!v; });
  }
  $('sbody').addEventListener('dragstart', function (e) { var b = e.target.closest('[data-model]'); if (b) e.dataTransfer.setData('text/model', b.dataset.model); });
  $('sbody').addEventListener('click', function (e) {
    var b = e.target.closest('[data-model],[data-lab],[data-s]'); if (!b) return;
    if (b.dataset.model) { var r = cv.getBoundingClientRect(), p = toWorld(r.left + r.width / 2 + (Math.random() - .5) * 160, r.top + r.height / 2 + (Math.random() - .5) * 120); addDev(b.dataset.model, p.x, p.y); return; }
    if (b.dataset.lab) { if (X.roomAct({ k: 'lab', id: b.dataset.lab })) return; startLab(b.dataset.lab); return; }
    var a = b.dataset.s;
    if (a === 'labwin') renderLab(true);
    if (a === 'tbase' || a === 'tvlan') startTask(a.slice(1));
    X.sideClick(a);
    if (a === 'png') savePng(); if (a === 'save') save(); if (a === 'open') $('fOpen').click(); if (a === 'fit') fit(); if (a === 'clear') clearAll();
  });

  // ================================================================== лабы и задания
  function resetNet() {
    stopTrace(); $('trace').classList.remove('on');
    Object.keys(wins).forEach(function (k) { closeWin(k, true); }); chips();
    net = new EL.Net(); net.onTrace = function (r, id, dst) { showTrace(r, id, dst); }; terms = {}; sel = null; selLink = null; msel = {}; mselL = {}; cable = null; draw();
  }
  function startLab(id) {
    lab = EL.labs.byId(id); lab._done = null; labSent = null; labP = lab.gen(); labShow = false; task = null; resetNet(); lab.build(net, labP); EL.labs.powerOff(net); draw(); fit(); renderLab(true); renderSide();
    report({ type: 'lab', lab: id, title: lab.title, mode: mode });
  }
  // учёт на сайте курса: какую лабу открыл студент. Офлайн (file://, GitHub Pages) запрос просто не проходит — молча
  function report(ev) {
    if (location.hostname !== 'net-cat.duckdns.org' || !window.fetch) return;      // только на сайте курса
    try { fetch('/api/event', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify(ev) }).catch(function () {}); } catch (err) { /* без сайта курса */ }
  }
  // «Сохранить» и значок NetCat — сохранить работу (на сервер — EL.serverSave из клиента /ws) и вернуться на курс; «Выйти» — сохранить и выйти из учётки
  var COURSE = '/';
  function saveNow() { autoSave(); var j = review ? null : snapshot(); return Promise.resolve(j && EL.serverSave ? EL.serverSave(j) : null).catch(function () { return null; }); }
  function saveAndGo() { toast('Сохраняю…'); saveNow().then(function () { autoOff = true; location.href = COURSE; }); }
  $('bSave').addEventListener('click', saveAndGo);
  $('logo').addEventListener('click', saveAndGo); $('logo').addEventListener('keydown', function (e) { if (e.key === 'Enter') saveAndGo(); });
  $('bOut').addEventListener('click', function () {
    saveNow().then(function () { autoOff = true;                          // выход не стирает работу: при следующем входе — «Продолжить?»
      fetch('/api/logout', { method: 'POST', credentials: 'same-origin' }).catch(function () {}).then(function () { location.href = '/login'; }); });
  });
  // ссылка с портала курса: eltex-cli.html#lab=4.1 — сразу открыть лабу (режим текущий); неизвестный id — без реакции
  function labFromHash() {
    var m = location.hash.match(/^#lab=([A-Za-z0-9.]+)$/); if (!m || !EL.labs.byId(m[1])) return;
    startLab(m[1]);
  }
  window.addEventListener('hashchange', labFromHash);
  setTimeout(function () { if (reviewFromHash()) return; var m = location.hash.match(/^#lab=([A-Za-z0-9.]+)$/);
    if (X.siteStart(m && EL.labs.byId(m[1]) ? m[1] : null, labFromHash)) return;    // на сайте: работа хранится на сервере (net_ws.js)
    autoOffer(m && EL.labs.byId(m[1]) ? m[1] : null, labFromHash); }, 0);
  // проверка пунктов по фактическому состоянию сети — при каждой команде и раз в 3 с модельного времени, даже если окно задания закрыто
  function labCheck() {
    var ts = lab.tasks(labP), was = lab._done || {}, now = {}, fresh = [], ok = 0, first = !lab._done;
    ts.forEach(function (t, i) { var y = false; try { y = !!t.ok(net); } catch (e) { y = false; } if (y) { ok++; now[i] = 1; if (!was[i]) fresh.push(i + 1); } });
    if (!first && fresh.length) toast('✓ Выполнено: пункт ' + fresh.join(', ') + (ok === ts.length ? ' — вся работа готова!' : ''));
    lab._done = now; labReport(ts, now);
    return { ts: ts, now: now, was: was, ok: ok, first: first };
  }
  // прогресс на сайт курса: {type:'task', lab, mode, total, done:[номера с 1], tasks:[тексты]} — только когда набор выполненных изменился
  var labSent = null;
  function labReport(ts, now) {
    var done = Object.keys(now).map(Number).sort(function (a, b) { return a - b; }).map(function (i) { return i + 1; }), key = lab.id + '|' + mode + '|' + done.join(',');
    if (key === labSent || review) return; labSent = key;          // при просмотре преподавателем прогресс студента не трогаем
    var ev = { type: 'task', lab: lab.id, mode: mode, total: ts.length, done: done, tasks: ts.map(function (t) { return String(t.t).replace(/<[^>]*>/g, '').slice(0, 300); }) };
    report(ev);
    if (window.parent && window.parent !== window) try { window.parent.postMessage({ source: 'eltex-lab', lab: ev.lab, mode: ev.mode, total: ev.total, done: ev.done, tasks: ev.tasks }, location.origin); } catch (e) { /* не во фрейме сайта */ }
  }
  function renderLab(open) {
    if (!lab) return;
    var c = labCheck(), ts = c.ts, ok = c.ok, was = c.was, now = c.now, body = $('labmain');
    if (!wins.lab) { if (!open) return; var box = document.createElement('div'); box.className = 'pad'; box.id = 'labbody';
      box.innerHTML = '<div id="labmain"></div><div id="labsub"></div><div id="labquiz"></div>';
      makeWin('lab', 'Задание ' + lab.id, lab.title, box, { x: 30, y: 80, w: 470, h: Math.min(620, innerHeight - 160) });
      box.addEventListener('click', labClick); body = $('labmain'); quizLab = null; }
    else if (open) minWin('lab', false);
    if (quizLab !== lab.id) quizLoad();
    if ($('labsub') && $('labsub').dataset.lab !== lab.id && !review) subLoad();
    // каждый пункт (в «Работе» и «Тесте») — с «лампочкой»: серая, пока не сделано; загорается зелёным со вспышкой в момент выполнения
    var li = ts.map(function (t, i) { var y = !!now[i];
      return '<li class="task' + (y ? ' ok' : '') + (y && !was[i] && !c.first ? ' lit' : '') + '"><span class="lamp"></span><span>' + t.t + '</span></li>'; }).join('');
    if (mode === 'work') {   // как методичка: текст задания с лампочками пунктов, без решения и подсказок
      body.innerHTML = '<div class="k">Лабораторная ' + lab.id + '</div><h2>' + esc(lab.title) + '</h2><p>' + esc(lab.goal) + '</p><ol class="tasks">' + li + '</ol>' +
        '<div class="sum ' + (ok === ts.length ? 'ok' : '') + '">' + (ok === ts.length ? 'РАБОТА ВЫПОЛНЕНА ✓' : 'Выполнено ' + ok + ' из ' + ts.length) + '</div>' +
        '<div class="row">' + (hasDoc(lab) ? '<button data-a="doc">Методичка</button>' : '') + '<button data-a="reset">Сбросить лабу</button></div>';
      return;
    }
    var sol = '';
    if (labShow === true) { var s = lab.sol(labP); sol = Object.keys(s).map(function (n) { return '<b>' + esc(n) + '</b><pre>' + esc(s[n].join('\n')) + '</pre>'; }).join('') + (lab.alt ? '<p>' + esc(lab.alt) + '</p>' : ''); }
    body.innerHTML = '<div class="k">Лабораторная ' + lab.id + '</div><h2>' + esc(lab.title) + '</h2><p>' + esc(lab.goal) + '</p><ol class="tasks">' + li + '</ol>' +
      '<div class="sum ' + (ok === ts.length ? 'ok' : '') + '">' + (ok === ts.length ? 'РАБОТА ВЫПОЛНЕНА ✓' : 'Выполнено ' + ok + ' из ' + ts.length) + '</div>' +
      (lab.hint && labShow === 'hint' ? '<div class="hint">' + esc(lab.hint(labP)) + '</div>' : '') +
      '<div class="row"><button data-a="new" class="pri">Новый вариант</button>' + (hasDoc(lab) ? '<button data-a="doc">Методичка</button>' : '') + (lab.hint ? '<button data-a="hint">Подсказка</button>' : '') +
      '<button data-a="sol">' + (labShow === true ? 'Скрыть решение' : 'Решение') + '</button><button data-a="reset">Сбросить лабу</button></div>' + sol;
  }
  // ---------------------------------------------------------------- «Тест» в окне лабы: вопросы с сайта курса (вне сайта блока нет)
  var quizLab = null;
  // GET /api/quiz?lab=ID → {ok, quiz:{title, pass_pct, attempts_left, best, aid, questions:[{id, type:'one'|'many'|'text', text, points, options}]}} (или те же поля без quiz);
  // нет теста (404), не вошёл (401), офлайн — блока нет
  function quizLoad() {
    var box = $('labquiz'); if (!box || !lab) return; quizLab = lab.id; box.innerHTML = '';
    if (location.hostname !== 'net-cat.duckdns.org' || !window.fetch) return;
    var id = lab.id;
    fetch('/api/quiz?lab=' + encodeURIComponent(id), { credentials: 'same-origin' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      var q = j && j.ok !== false ? (j.quiz || j) : null; if (!q || !lab || lab.id !== id || !$('labquiz')) return;
      var qs = q.questions || q.items || [];
      if (!qs.length && !q.best) return;
      quizRender($('labquiz'), id, q, qs);
    }).catch(function () { /* теста нет */ });
  }
  function qid(q, i) { return String(q.id !== undefined && q.id !== null ? q.id : 'q' + (i + 1)); }
  var QT = { many: 'multi', multi: 'multi', text: 'text', match: 'match', gaps: 'gaps', essay: 'essay', info: 'info' };
  function qType(t) { return QT[t] || 'single'; }
  // поле ответа по типу: single/multi — варианты, text — строка, match — список для каждой строки, gaps — текст с пропусками, essay — textarea
  function qInput(x, k, tp) {
    var opts = x.options || x.choices || [], sel = function (L, cls) { return '<select class="' + cls + '"><option value="">—</option>' + L.map(function (o, n) { return '<option value="' + n + '">' + esc(o) + '</option>'; }).join('') + '</select>'; };
    if (tp === 'text') return '<input type="text" class="qin" placeholder="Ваш ответ">';
    if (tp === 'essay') return '<textarea class="qin qes" rows="4" placeholder="Ваш ответ"></textarea>';
    if (tp === 'match') return '<div class="qmt">' + (x.left || []).map(function (l) { return '<label class="qml"><span>' + esc(l) + '</span>' + sel(x.right || [], 'qsel') + '</label>'; }).join('') + '</div>';
    if (tp === 'gaps') { var P = x.parts || [], Gs = x.gaps || [];
      return '<div class="qgp">' + P.map(function (t, i) { var g = Gs[i]; return esc(t) + (!g ? '' : g.kind === 'select' ? sel(g.options || [], 'qsel qg') : '<input type="text" class="qin qg" size="10">'); }).join('') + '</div>'; }
    return opts.map(function (o, n) { return '<label class="qo"><input type="' + (tp === 'multi' ? 'checkbox' : 'radio') + '" name="qz-' + esc(k) + '" value="' + n + '"> ' + esc(o) + '</label>'; }).join('');
  }
  function qAnswer(el, tp) {
    var v = function (x) { return x.tagName === 'SELECT' ? (x.value === '' ? null : +x.value) : (x.value || '').trim(); };
    if (tp === 'text' || tp === 'essay') return (el.querySelector('.qin').value || '').trim();
    if (tp === 'match') return [].map.call(el.querySelectorAll('.qmt select'), v);
    if (tp === 'gaps') return [].map.call(el.querySelectorAll('.qg'), v);
    if (tp === 'multi') return [].filter.call(el.querySelectorAll('input'), function (x) { return x.checked; }).map(function (x) { return +x.value; });
    var c = el.querySelector('input:checked'); return c ? +c.value : null;
  }
  function pctTxt(b) { return b ? b.score + ' из ' + b.max + (b.pct !== undefined && b.pct !== null ? ' (' + b.pct + '%)' : '') : ''; }
  function quizRender(box, id, q, qs) {
    var meta = [q.pass_pct ? 'зачёт от ' + q.pass_pct + '%' : '', q.attempts_left !== undefined && q.attempts_left !== null ? 'осталось попыток: ' + q.attempts_left : '',
      q.best ? 'лучший результат: ' + pctTxt(q.best) : ''].filter(Boolean).join(' · ');
    if (!qs.length) { box.innerHTML = '<div class="quiz"><div class="k">Тест</div><h3>' + esc(q.title || 'Проверьте себя') + '</h3><p>Попытки закончились' + (q.best ? '. Лучший результат: ' + esc(pctTxt(q.best)) : '') + '</p></div>'; return; }
    var num = 0;
    box.innerHTML = '<div class="quiz"><div class="k">Тест</div><h3>' + esc(q.title || 'Проверьте себя') + '</h3>' + (meta ? '<p class="qm">' + esc(meta) + '</p>' : '') + qs.map(function (x, i) {
      var k = qid(x, i), tp = qType(x.type), txt = esc(x.text || x.question || x.q || '');
      if (tp === 'info') return '<div class="qinfo">' + txt + '</div>';
      var hint = tp === 'multi' ? ' <i>(несколько ответов)</i>' : tp === 'match' ? ' <i>(сопоставьте)</i>' : tp === 'essay' ? ' <i>(проверяет преподаватель)</i>' : '';
      return '<div class="qq" data-qid="' + esc(k) + '" data-tp="' + tp + '"><div class="qt">' + (++num) + '. ' + txt + hint +
        (x.points ? ' <i>· ' + x.points + ' б.</i>' : '') + ' <b class="qr"></b></div>' + qInput(x, k, tp) + '<div class="qa"></div></div>'; }).join('') +
      '<div class="row"><button class="pri" data-qa="send">Ответить</button><span class="qs"></span></div></div>';
    [].forEach.call(box.querySelectorAll('input, textarea, select'), function (x) { x.addEventListener('keydown', function (e) { e.stopPropagation(); }); });
    box.querySelector('[data-qa="send"]').addEventListener('click', function () {
      var answers = {}, btn = this, out = box.querySelector('.qs');
      if (btn.dataset.again) { quizLoad(); return; }
      [].forEach.call(box.querySelectorAll('.qq'), function (el) { answers[el.dataset.qid] = qAnswer(el, el.dataset.tp); });
      btn.disabled = true; out.textContent = 'Проверяем…';
      fetch('/api/quiz/answer', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify({ lab: id, aid: q.aid, answers: answers }) })
        .then(function (r) { return r.json().catch(function () { return { ok: false, error: 'Ошибка сервера (' + r.status + ')' }; }); }).then(function (j) {
          btn.disabled = false;
          if (!j || j.ok === false) { out.textContent = (j && j.error) || 'Ответ не принят'; return; }
          var R = j.result || {}, res = j.results || j.correct || {}, items = {};
          (R.items || []).forEach(function (it) { items[String(it.id)] = it; });
          [].forEach.call(box.querySelectorAll('.qq'), function (el, i) { var k = el.dataset.qid, it = items[k], v = Array.isArray(res) ? res[i] : res[k];
            var mark = it && typeof it.mark === 'number' ? it.mark : v === true ? 1 : v === false ? 0 : null, m = el.querySelector('.qr'), a = el.querySelector('.qa');
            el.classList.toggle('good', mark === 1); el.classList.toggle('bad', mark === 0); el.classList.toggle('part', mark !== null && mark > 0 && mark < 1);
            var wait = mark === null && (el.dataset.tp === 'essay' || (R.pending && v === null));
            el.classList.toggle('wait', wait);
            m.textContent = mark === 1 ? '✓' : mark === 0 ? '✗' : mark !== null ? Math.round(mark * 100) + '%' : wait ? '⏳' : '';
            a.textContent = wait ? 'На проверке у преподавателя' : it && it.right ? 'Правильно: ' + it.right : '';
            [].forEach.call(el.querySelectorAll('input, textarea, select'), function (x) { x.disabled = true; }); });
          var score = j.score !== undefined ? j.score : R.score, max = j.max !== undefined ? j.max : R.max, pct = R.pct !== undefined ? R.pct : j.pct;
          out.textContent = 'Балл: ' + score + (max !== undefined ? ' из ' + max : '') + (pct !== undefined && pct !== null ? ' (' + pct + '%)' : '') +
            (R.passed === true ? ' — зачтено' : R.passed === false ? ' — не зачтено' : '') + (R.pending ? ' · есть ответы на проверке у преподавателя' : '') + (R.best ? ' · лучший: ' + pctTxt(R.best) : '') +
            (R.attempts_left !== undefined && R.attempts_left !== null ? ' · осталось попыток: ' + R.attempts_left : '') + (j.comment ? ' — ' + j.comment : '');
          if (R.attempts_left === undefined || R.attempts_left === null || R.attempts_left > 0) { btn.textContent = 'Новая попытка'; btn.dataset.again = '1'; } else btn.hidden = true;
        }).catch(function () { btn.disabled = false; out.textContent = 'Не удалось отправить ответы — проверьте вход на сайт курса'; });
    });
  }
  // ---------------------------------------------------------------- «Отправить на проверку» и статус проверки (только на сайте курса)
  var SITE = location.hostname === 'net-cat.duckdns.org', review = null, subTimer = null;
  function snapshot() { var j = net.toJSON(); X.saveX(j); if (lab) j.builtin = { id: lab.id, p: labP }; j.now = net.now; j.saved = Date.now(); return j; }
  function gz(text) {                 // base64(gzip(text)) через CompressionStream
    var cs = new Blob([text]).stream().pipeThrough(new CompressionStream('gzip'));
    return new Response(cs).arrayBuffer().then(function (b) { var u = new Uint8Array(b), s = ''; for (var i = 0; i < u.length; i += 0x8000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x8000)); return btoa(s); });
  }
  function ungz(b64) { var bin = atob(b64), u = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i);
    return new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('gzip'))).text(); }
  function fmtAt(t) { if (!t) return ''; var d = new Date(typeof t === 'number' && t < 1e12 ? t * 1000 : t), p = function (v) { return ('0' + v).slice(-2); };
    return isNaN(d) ? String(t) : p(d.getDate()) + '.' + p(d.getMonth() + 1) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes()); }
  function subLoad() {
    var box = $('labsub'); if (!box || !lab || review) return; box.dataset.lab = lab.id;
    if (!SITE || !window.fetch) { box.innerHTML = ''; return; }
    var id = lab.id;
    fetch('/api/submit?lab=' + encodeURIComponent(id), { credentials: 'same-origin' }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (!lab || lab.id !== id || !$('labsub')) return; subRender($('labsub'), j && j.ok !== false ? j : null);
    }).catch(function () { subRender($('labsub'), null); });
  }
  function subRender(box, j) {
    var s = j && j.sub, st = s && s.status, plate = '';
    if (s) plate = st === 'accepted' ? '<div class="subp ok">Принято ✓' + (s.reviewed_at ? ' · ' + esc(fmtAt(s.reviewed_at)) : '') + '</div>'
      : st === 'returned' ? '<div class="subp ret">На доработку' + (s.reviewed_at ? ' · ' + esc(fmtAt(s.reviewed_at)) : '') + '</div>'
      : '<div class="subp sent">Отправлено на проверку · ' + esc(fmtAt(s.at)) + '</div>';
    if (s && s.comment) plate += '<div class="subc"><b>Комментарий преподавателя:</b> ' + esc(s.comment) + '</div>';
    if (j && j.passed) plate += '<div class="subp ok">Лаба зачтена' + (j.pass_pct ? ' (порог ' + j.pass_pct + '% пунктов или «Принято»)' : '') + '</div>';
    else if (j && j.pass_pct) plate += '<div class="subm">Зачёт: ' + j.pass_pct + '% пунктов или «Принято» преподавателем</div>';
    box.innerHTML = '<div class="sub">' + plate + '<textarea class="qin subn" rows="2" placeholder="Комментарий для преподавателя (необязательно)"></textarea>' +
      '<div class="row"><button class="pri" data-sa="send">' + (s ? 'Отправить заново' : 'Отправить на проверку') + '</button><span class="subs"></span></div></div>';
    var ta = box.querySelector('textarea'); ta.addEventListener('keydown', function (e) { e.stopPropagation(); });
    box.querySelector('[data-sa="send"]').addEventListener('click', function () { subSend(box, this, ta.value.trim()); });
  }
  function subSend(box, btn, note) {
    var out = box.querySelector('.subs'), c = labCheck(), state = snapshot(), text = JSON.stringify(state);
    var body = { lab: lab.id, done: Object.keys(c.now).map(Number).sort(function (a, b) { return a - b; }).map(function (i) { return i + 1; }), total: c.ts.length,
      tasks: c.ts.map(function (t) { return String(t.t).replace(/<[^>]*>/g, '').slice(0, 300); }), note: note || '' };
    btn.disabled = true; out.textContent = 'Отправляем…';
    var big = text.length > 200000 && window.CompressionStream;
    (big ? gz(text).then(function (b) { body.state_gz = b; }) : Promise.resolve(body.state = state)).then(function () {
      return fetch('/api/submit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify(body) });
    }).then(function (r) { return r.json().catch(function () { return { ok: false, error: 'Ошибка сервера (' + r.status + ')' }; }); }).then(function (j) {
      btn.disabled = false;
      if (!j || j.ok === false) { out.textContent = (j && j.error) || 'Не отправлено'; return; }
      toast('Работа отправлена на проверку'); subLoad();
    }).catch(function () { btn.disabled = false; out.textContent = 'Не удалось отправить — проверьте вход на сайт курса'; });
  }
  setInterval(function () { if (lab && wins.lab && SITE && !review) subLoad(); }, 60000);

  // ---------------------------------------------------------------- просмотр работы преподавателем: emulator.html#review=<sid>
  function reviewFromHash() {
    var m = location.hash.match(/^#review=([\w-]+)$/); if (!m) return false;
    review = { sid: m[1] }; autoOff = true;                     // схема студента не попадает в автосохранение преподавателя
    if (!window.fetch) return true;
    fetch('/api/t/submission?id=' + encodeURIComponent(m[1]), { credentials: 'same-origin' }).then(function (r) { return r.json().catch(function () { return { ok: false, error: 'Ошибка сервера (' + r.status + ')' }; }); }).then(function (j) {
      if (!j || j.ok === false || !j.sub) { toast((j && j.error) || 'Работа не найдена'); return; }
      var s = j.sub; review.sub = s;
      var st = s.state ? Promise.resolve(typeof s.state === 'string' ? JSON.parse(s.state) : s.state) : s.state_gz ? ungz(s.state_gz).then(JSON.parse) : Promise.resolve(null);
      return st.then(function (state) {
        if (state) { loadScheme(state); if (state.now) net.now = state.now; }
        if (!lab && s.lab && EL.labs.byId(s.lab) && !state) startLab(s.lab);
        reviewRender();
      });
    }).catch(function (e) { toast('Не удалось открыть работу: ' + (e && e.message || e)); });
    return true;
  }
  function reviewRender() {
    var s = review.sub; if (!s) return;
    if (!wins.lab) renderLab(true);
    var box = $('labsub'); if (!box) { toast('Работа загружена, но окно задания не открылось'); return; }
    if ($('labmain') && box.nextSibling === $('labquiz')) box.parentNode.insertBefore(box, $('labmain'));   // плашка работы — над пунктами
    var num = s.id !== undefined ? ('00' + s.id).slice(-3) : s.sid;
    box.innerHTML = '<div class="sub rev"><div class="subp sent">Работа №' + esc(num) + (s.login ? ' · ' + esc(s.login) : '') + ' · лаба ' + esc(s.lab) + ' · отправлена ' + esc(fmtAt(s.at)) + '</div>' +
      '<div class="subm">По факту в схеме: ' + Object.keys(lab && lab._done || {}).length + ' из ' + (lab ? lab.tasks(labP).length : s.total) + ' пунктов (при отправке — ' + (s.done || []).length + ' из ' + s.total + ')</div>' +
      (s.note ? '<div class="subc"><b>Комментарий студента:</b> ' + esc(s.note) + '</div>' : '') +
      (s.status && s.status !== 'sent' ? '<div class="subm">Сейчас: ' + (s.status === 'accepted' ? 'принято' : 'на доработку') + (s.comment ? ' — ' + esc(s.comment) : '') + '</div>' : '') +
      '<textarea class="qin subn" rows="3" placeholder="Комментарий для студента">' + esc(s.comment || '') + '</textarea>' +
      '<div class="row"><button class="pri" data-ra="accepted">Принято</button><button data-ra="returned">На доработку</button><span class="subs"></span></div></div>';
    var ta = box.querySelector('textarea'); ta.addEventListener('keydown', function (e) { e.stopPropagation(); });
    [].forEach.call(box.querySelectorAll('[data-ra]'), function (b) { b.addEventListener('click', function () {
      var out = box.querySelector('.subs'), st = b.dataset.ra; out.textContent = 'Сохраняем…';
      fetch('/api/t/submission', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify({ id: s.sid, status: st, comment: ta.value.trim() }) })
        .then(function (r) { return r.json().catch(function () { return { ok: false, error: 'Ошибка сервера (' + r.status + ')' }; }); }).then(function (j) {
          if (!j || j.ok === false) { out.textContent = (j && j.error) || 'Не сохранено'; return; }
          s.status = st; s.comment = ta.value.trim(); reviewRender(); toast(st === 'accepted' ? 'Работа принята' : 'Работа возвращена на доработку'); })
        .catch(function () { out.textContent = 'Не удалось сохранить'; }); }); });
  }
  // методичка лабы — PDF курса рядом с эмулятором (labs/<id>.pdf на сайте курса); в репозиторий и в HTML не входит
  function hasDoc(L) { return /^(\d+\.\d+|E\.\d+)$/.test(L.id); }
  function openDoc(id) { openPdf('doc', 'labs/' + id + '.pdf', 'Методичка ' + id, 'PDF лабораторной', 'Методичка доступна', []); }
  // окно PDF с сайта курса: встроенный просмотр + «Открыть в новой вкладке»; без файла (офлайн, GitHub Pages) — строка про сайт курса
  function openPdf(key, url, title, sub, missText, extra) {
    var body = document.createElement('div'); body.style.cssText = 'display:flex;flex-direction:column;flex:1;min-height:0';
    var links = [{ url: url, title: 'Открыть в новой вкладке' }].concat(extra || []);
    body.innerHTML = '<div class="row" style="padding:6px 10px;margin:0">' + links.map(function (l) { return '<a class="act" target="_blank" rel="noopener" href="' + esc(l.url) + '">' + esc(l.title) + '</a>'; }).join(' ') +
      '</div><div class="pad" data-doc>Загрузка…</div>';
    closeWin(key, true); makeWin(key, title, sub, body, { x: Math.max(20, innerWidth - 720), y: 70, w: Math.min(700, innerWidth - 40), h: innerHeight - 140 });
    var box = body.querySelector('[data-doc]'), miss = function () { box.innerHTML = esc(missText) + ' на сайте курса <b>net-cat.duckdns.org</b>';
      [].forEach.call(body.querySelectorAll('a'), function (a) { a.style.display = 'none'; }); };
    if (location.protocol === 'file:' || !window.fetch) { miss(); return; }
    fetch(url, { method: 'HEAD', credentials: 'same-origin' }).then(function (r) {
      if (!r.ok || !/pdf/i.test(r.headers.get('content-type') || 'pdf')) { miss(); return; }
      box.className = ''; box.style.cssText = 'flex:1;min-height:0;display:flex'; box.innerHTML = '<iframe src="' + esc(url) + '" title="' + esc(title) + '" style="flex:1;border:0;background:#fff"></iframe>';
    }).catch(miss);
  }
  function openManual(id) { var d = net.devs[id], m = d && net.manualFor(id); if (!m) return;
    openPdf('man' + id, m.url, m.title, d.name + ' · ' + d.model, 'Руководство доступно', m.extra); }
  // исходная схема лабы того же варианта: все настройки студента пропадают
  function resetLab() { if (!lab) return; var L = lab, P = labP;
    ask('Сбросить лабу ' + L.id + '? Все настройки устройств и изменения схемы пропадут — вернётся исходная схема задания.', function () {
      resetNet(); lab = L; lab._done = null; labP = P; labShow = false; lab.build(net, labP); draw(); fit(); renderLab(true); renderSide(); toast('Лаба ' + L.id + ' сброшена'); }, 'Да, сбросить'); }
  function labClick(e) { var b = e.target.closest('[data-a]'); if (!b) return; var a = b.dataset.a; if (a === 'doc') { openDoc(lab.id); return; } if (a === 'reset') { resetLab(); return; }
    if (a === 'new') startLab(lab.id); if (a === 'sol') { labShow = labShow === true ? false : true; renderLab(); } if (a === 'hint') { labShow = 'hint'; renderLab(); } }
  function startTask(kind) {
    // тренажёры дек написаны синтаксисом ветки 6.x — коммутатор той же ветки
    lab = null; resetNet(); var d = net.add('MES3300-24', 'SW1', 500, 300); d.st.mode = 'priv'; d.st.host = 'switch';
    task = EL.labs.randomTask(kind); task.kind = kind; task.dev = d.id; if (task.T.setup) task.T.setup(task.P, d.st);
    task.html = task.T.text(task.P); task.res = ''; task.sol = false; term(d.id).auth = true; draw(); fit(); renderTask(true); openTerm(d.id);
  }
  function renderTask(open) {
    if (!task) return; var body = $('taskbody');
    if (!wins.task) { if (!open) return; body = document.createElement('div'); body.className = 'pad'; body.id = 'taskbody';
      makeWin('task', 'Задание', task.kind === 'base' ? 'базовая настройка' : 'VLAN', body, { x: 30, y: 80, w: 440, h: 420 }); body.addEventListener('click', taskClick); }
    var T = task.T;
    body.innerHTML = '<div class="k">Задание · ' + (task.kind === 'base' ? 'базовая настройка' : 'VLAN') + '</div><p style="color:var(--ink)">' + task.html + '</p>' +
      '<div class="row"><button data-a="check" class="pri">Проверить</button>' + (T.send ? '<button data-a="send">Отправить кадр</button>' : '') +
      '<button data-a="other">Другое</button><button data-a="sol">Решение</button></div>' + task.res + (task.sol ? '<pre>' + esc(T.sol(task.P).join('\n')) + '</pre>' : '');
  }
  function taskClick(e) { var b = e.target.closest('[data-a]'); if (!b) return; var a = b.dataset.a, st = net.devs[task.dev].st;
    if (a === 'other') { startTask(task.kind); return; } if (a === 'sol') task.sol = !task.sol;
    if (a === 'check') { var cs = task.T.checks(task.P), ok = 0;
      task.res = '<div class="send">' + cs.map(function (c) { var y = !!c[1](st); if (y) ok++; return '<div class="' + (y ? 'ok' : 'no') + '">' + (y ? '✓ ' : '✗ ') + c[0] + '</div>'; }).join('') +
        '</div><div class="sum ' + (ok === cs.length ? 'ok' : '') + '">' + (ok === cs.length ? 'ВЫПОЛНЕНО ✓' : ok + ' из ' + cs.length) + '</div>'; }
    if (a === 'send') { var r = task.T.send(task.P, st); task.res = '<div class="send">' + r.map(function (x) { return '<div class="' + (x.ok ? 'ok' : x.exp ? 'exp' : 'no') + '">✉ ' + esc(x.t) + '</div>'; }).join('') + '</div>'; }
    renderTask(); }
  function refresh() { renderLab(false); refreshTables(); pollEv(); }

  // ================================================================== справка, файл, клавиши
  function openHelp() {
    var body = document.createElement('div'); body.className = 'pad'; var src = document.getElementById('helpSrc');
    body.innerHTML = src ? src.innerHTML : ''; var c = body.querySelector('.close'); if (c) c.remove();
    makeWin('help', 'Справка', 'команды и управление', body, { x: 60, y: 70, w: Math.min(980, innerWidth - 120), h: innerHeight - 150 });
  }
  // схема картинкой: SVG поля со встроенными стилями и иконками → canvas → PNG (2×)
  var STYLE = ['fill', 'fill-opacity', 'stroke', 'stroke-width', 'stroke-dasharray', 'stroke-linecap', 'stroke-linejoin', 'paint-order', 'opacity', 'font-family', 'font-size', 'font-weight', 'letter-spacing', 'text-anchor', 'dominant-baseline', 'display', 'visibility'];
  function savePng() {
    if (!net.list().length) { toast('Схема пуста'); return; }
    var src = $('world'), bb = src.getBBox(), pad = 40, W = Math.ceil(bb.width + pad * 2), H = Math.ceil(bb.height + pad * 2);
    var svg = document.createElementNS(NS, 'svg'), g = src.cloneNode(true);
    svg.setAttribute('xmlns', NS); svg.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
    svg.setAttribute('viewBox', (bb.x - pad) + ' ' + (bb.y - pad) + ' ' + W + ' ' + H); svg.setAttribute('width', W * 2); svg.setAttribute('height', H * 2);
    g.removeAttribute('transform'); g.removeAttribute('id');
    var a = src.querySelectorAll('*'), b = g.querySelectorAll('*');
    for (var i = 0; i < a.length; i++) { var cs = getComputedStyle(a[i]), st = STYLE.map(function (k) { return k + ':' + cs.getPropertyValue(k); }).join(';'); b[i].setAttribute('style', st); }
    [].forEach.call(g.querySelectorAll('#pk,#ghost,title'), function (x) { x.remove(); });
    var bg = document.createElementNS(NS, 'rect'); bg.setAttribute('x', bb.x - pad); bg.setAttribute('y', bb.y - pad); bg.setAttribute('width', W); bg.setAttribute('height', H);
    bg.setAttribute('fill', getComputedStyle(document.body).backgroundColor || '#140b0e'); svg.appendChild(bg);
    var defs = document.createElementNS(NS, 'defs'), sym = document.querySelector('symbol[id^="ic-"]');        // весь спрайт иконок: символы и их градиенты
    if (sym) [].forEach.call(sym.parentNode.children, function (x) { defs.appendChild(x.cloneNode(true)); });
    svg.appendChild(defs); svg.appendChild(g);
    var url = URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(svg)], { type: 'image/svg+xml' })), img = new Image();
    img.onload = function () { var c = document.createElement('canvas'); c.width = W * 2; c.height = H * 2; c.getContext('2d').drawImage(img, 0, 0, c.width, c.height); URL.revokeObjectURL(url);
      c.toBlob(function (blob) { var l = document.createElement('a'); l.href = URL.createObjectURL(blob); l.download = 'eltex-shema.png'; document.body.appendChild(l); l.click(); l.remove();
        setTimeout(function () { URL.revokeObjectURL(l.href); }, 2000); toast('Схема сохранена картинкой'); }, 'image/png'); };
    img.onerror = function () { URL.revokeObjectURL(url); toast('Не удалось нарисовать картинку схемы'); };
    img.src = url;
  }
  function save() {
    var j = net.toJSON(); X.saveX(j); if (lab) j.builtin = { id: lab.id, p: labP };
    var blob = new Blob([JSON.stringify(j, null, 1)], { type: 'application/json' }), a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = 'eltex-shema.json'; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
  }
  function loadScheme(j) {
    var n = EL.Net.fromJSON(j); lab = null; task = null; resetNet(); net = n; net.onTrace = function (r, id, dst) { showTrace(r, id, dst); };
    X.loadX(j); draw(); fit();
    var bl = j.builtin && EL.labs.byId(j.builtin.id);           // схема встроенной лабы — с тем же вариантом и проверками
    if (bl) { lab = bl; lab._done = null; labP = j.builtin.p; labShow = false; renderLab(true); }
    renderSide(); }
  $('fOpen').addEventListener('change', function () { var f = this.files[0]; if (!f) return; var rd = new FileReader();
    rd.onload = function () { try { loadScheme(JSON.parse(rd.result)); toast('Схема загружена: ' + net.list().length + ' устройств'); } catch (err) { toast('Не удалось открыть: ' + err.message); } };
    rd.readAsText(f); this.value = ''; });
  document.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
    if (e.key === 'Escape') { closeMenu(); if (cable) { cable = null; $('ghost').style.display = 'none'; draw(); } }
    if (e.ctrlKey && /^[zZя]$/.test(e.key)) { e.preventDefault(); X.undo(); }
    if (e.key === 'Delete') delSelected();
  });
  var tt = null;
  function toast(t) { var x = $('toast'); x.textContent = t; x.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { x.classList.remove('on'); }, 2600); }

  // ================================================================== старт
  renderSide();
  draw(); setTimeout(fit, 30);            // при открытии — пустое поле (лаба по ссылке #lab=… строит свою схему)

  // ================================================================== автосохранение незаконченной работы (в этом браузере)
  // каждые 4 с, если что-то изменилось, и при закрытии вкладки; при открытии — предложение продолжить. «Выйти» и «Очистить» стирают сохранение
  var AUTO = 'eltex-cli-autosave', autoGen = -1, autoOff = false;
  function autoSave() {
    if (autoOff || review) return;
    try {
      if (!net.list().length && !lab) { localStorage.removeItem(AUTO); return; }
      var j = net.toJSON(); X.saveX(j); if (lab) j.builtin = { id: lab.id, p: labP }; j.now = net.now; j.saved = Date.now();
      localStorage.setItem(AUTO, JSON.stringify(j)); autoGen = net.gen;
    } catch (err) { /* хранилище недоступно или переполнено — работа идёт без автосохранения */ }
  }
  function autoClear() { try { localStorage.removeItem(AUTO); } catch (err) { /* хранилище недоступно */ } }
  function autoRead() { try { var t = localStorage.getItem(AUTO); return t ? JSON.parse(t) : null; } catch (err) { return null; } }
  setInterval(function () { if (net.gen !== autoGen) autoSave(); }, 4000);
  window.addEventListener('pagehide', autoSave);
  // при открытии: есть сохранение — предложить продолжить (для ссылки #lab=ID — только если это та же лаба)
  function autoOffer(hashLab, fresh) {
    var j = autoRead(), sameLab = j && j.builtin && j.builtin.id === hashLab;
    if (!j || (hashLab && !sameLab)) { fresh(); return; }
    var when = new Date(j.saved || Date.now()), p = function (v) { return ('0' + v).slice(-2); };
    var what = (j.builtin ? 'лаба ' + j.builtin.id + ', ' : '') + (j.devs || []).length + ' устр.';
    autoOff = true;                                             // пока студент не ответил — старое сохранение не затираем
    ask('Найдена незаконченная работа (' + what + ', сохранено ' + p(when.getDate()) + '.' + p(when.getMonth() + 1) + ' в ' + p(when.getHours()) + ':' + p(when.getMinutes()) +
      '). Продолжить с того же места?', function () { autoOff = false;
      try { loadScheme(j); if (j.now) net.now = j.now; toast('Работа восстановлена'); } catch (err) { toast('Не удалось восстановить: ' + err.message); fresh(); } }, 'Продолжить');
    var w = wins.ask; if (w) w.el.addEventListener('click', function (e) { var b = e.target.closest('[data-q="n"],.x,[data-w="close"]'); if (b) { autoOff = false; autoClear(); fresh(); } }, true);
  }
  window.addEventListener('resize', applyView);
  window.ELUI = { quizRender: function (box, id, q, qs) { quizRender(box, id, q, qs); }, subRender: function (box, j) { subRender(box, j); }, reviewFromHash: reviewFromHash, snapshot: snapshot, net: function () { return net; }, run: function (id, l) { run(id, l); }, startLab: startLab, openTerm: openTerm, toWorld: toWorld,
    mode: function () { return mode; }, makeWin: makeWin, closeWin: closeWin, minWin: minWin, wins: wins, esc: esc, toast: toast, draw: draw, refresh: refresh, el: el,
    renderSide: renderSide, ask: function (q, yes, ok) { ask(q, yes, ok); }, setAutoOff: function (v) { autoOff = v; }, setReadOnly: function (v) { readOnly = !!v; document.body.classList.toggle('ro', readOnly); },
    autoOffer: function (hl, fr) { autoOffer(hl, fr); },
    clearTerm: function (id) { term(id).html = ''; var b = tEl(id); if (b) b.querySelector('.out').innerHTML = ''; },
    labInfo: function () { if (!lab) return null; var ts = lab.tasks(labP); return { id: lab.id, title: lab.title, total: ts.length, done: Object.keys(lab._done || {}).map(function (i) { return +i + 1; }) }; },
    setNet: function (n) { lab = null; task = null; net = n; net.onTrace = function (r, id, dst) { showTrace(r, id, dst); }; sel = null; selLink = null; msel = {}; mselL = {}; draw(); renderSide(); },
    startFree: function () { lab = null; task = null; resetNet(); renderSide(); }, savePng: savePng, tlog: tlog, setPr: setPr, term: term, loadScheme: loadScheme, linkOff: linkOff, saveJSON: function () { var j = net.toJSON(); X.saveX(j); if (lab) j.builtin = { id: lab.id, p: labP }; return j; } };
})();
