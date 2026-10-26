/* Интерфейс эмулятора: палитра, схема (SVG), кабели, консоли устройств, пошаговая анимация пакетов, лабы и задания. */
(function () {
  'use strict';
  var EL = window.EL, $ = function (id) { return document.getElementById(id); };
  var NS = 'http://www.w3.org/2000/svg';
  var net = new EL.Net(), sel = null, selLink = null, cons = {}, tool = null, cable = null, mode = 'free';
  var lab = null, labP = null, labSolShown = false, task = null, trace = null;
  var cv = $('cv'), out = $('out'), inp = $('in'), pr = $('pr');

  // ------------------------------------------------------------------ иконки
  function icon(type, w) {
    var s = { mes: '<rect x="2" y="6" width="34" height="18" rx="2" class="box"/><path d="M10 12h16l-3-3M28 18H12l3 3" fill="none" stroke="currentColor" stroke-width="2"/>',
      esr: '<circle cx="19" cy="15" r="12" class="box"/><path d="M12 15h14M19 8v14M23 11l3 4-3 4M15 11l-3 4 3 4" fill="none" stroke="currentColor" stroke-width="1.8"/>',
      vpc: '<rect x="6" y="3" width="26" height="17" rx="1" class="box"/><path d="M14 25h10M19 20v5" stroke="currentColor" stroke-width="2"/>',
      deb: '<rect x="6" y="3" width="26" height="17" rx="1" class="box"/><path d="M14 25h10M19 20v5" stroke="currentColor" stroke-width="2"/><path d="M22 8a4 4 0 1 0 0 6" fill="none" stroke="#c70036" stroke-width="2"/>' }[type];
    return '<svg viewBox="0 0 38 28" width="' + (w || 38) + '" style="color:#14161a"><style>.box{fill:#fff;stroke:#14161a;stroke-width:2}</style>' + s + '</svg>';
  }
  // ------------------------------------------------------------------ палитра
  function buildPalette() {
    var g = {}, h = '';
    Object.keys(EL.MODELS).forEach(function (k) { var m = EL.MODELS[k]; (g[m.group] = g[m.group] || []).push(k); });
    Object.keys(g).forEach(function (gr) {
      h += '<h4>' + gr + '</h4>';
      g[gr].forEach(function (k) { var m = EL.MODELS[k];
        h += '<button class="pi" data-model="' + k + '">' + icon(m.type) + '<span><b>' + k + '</b><small>' + m.note + '</small></span></button>'; });
    });
    h += '<p class="note">Коммутаторы — CLI MES24xx (ПО 10.4), маршрутизатор — CLI ESR. Модели берутся из каталога и даташитов Eltex; поведение — модель по документации, не прошивка.</p>';
    $('pal').innerHTML = h;
  }
  $('pal').addEventListener('click', function (e) {
    var b = e.target.closest('[data-model]'); if (!b) return;
    var n = net.list().length, d = net.add(b.dataset.model, null, 130 + (n % 5) * 180, 110 + Math.floor(n / 5) % 3 * 190);
    selectDev(d.id); draw(); refresh();
  });

  // ------------------------------------------------------------------ схема
  function el(tag, attrs, parent) { var x = document.createElementNS(NS, tag); Object.keys(attrs || {}).forEach(function (k) { x.setAttribute(k, attrs[k]); });
    if (parent) parent.appendChild(x); return x; }
  function center(d) { return { x: d.x, y: d.y }; }
  function draw() {
    cv.innerHTML = '';
    var gl = el('g', {}, cv), gp = el('g', {}, cv), gd = el('g', {}, cv);
    el('g', { id: 'pk' }, cv);
    net.links.forEach(function (l, i) {
      var a = net.devs[l.a.dev], b = net.devs[l.b.dev], A = center(a), B = center(b);
      var ln = el('line', { x1: A.x, y1: A.y, x2: B.x, y2: B.y, 'class': 'lnk' + (selLink === i ? ' sel' : ''), 'data-li': i }, gl);
      ln.addEventListener('click', function (e) { e.stopPropagation(); selLink = i; sel = null; draw(); });
      [[A, B, l.a.port], [B, A, l.b.port]].forEach(function (z) {
        var dx = z[1].x - z[0].x, dy = z[1].y - z[0].y, L = Math.hypot(dx, dy) || 1, k = Math.min(95, L * 0.34);
        var px = z[0].x + dx / L * k, py = z[0].y + dy / L * k, g = el('g', { 'class': 'pl' }, gp), w = z[2].length * 9 + 12;
        el('rect', { x: px - w / 2, y: py - 11, width: w, height: 22, rx: 11 }, g);
        el('text', { x: px, y: py }, g).textContent = z[2];
      });
    });
    net.list().forEach(function (d) {
      var g = el('g', { 'class': 'dev' + (sel === d.id ? ' sel' : '') + (cable && cable.a === d.id ? ' pick' : ''), transform: 'translate(' + d.x + ',' + d.y + ') scale(1.5)', 'data-id': d.id }, gd);
      if (d.type === 'mes') { el('rect', { x: -46, y: -22, width: 92, height: 44, rx: 4, 'class': 'box' }, g);
        el('path', { d: 'M-24 -8h40l-7-7M24 8h-40l7 7', fill: 'none', stroke: '#14161a', 'stroke-width': 3 }, g); }
      if (d.type === 'esr') { el('circle', { r: 28, 'class': 'box' }, g);
        el('path', { d: 'M-16 0h32M0 -16v32M9 -7l7 7-7 7M-9 -7l-7 7 7 7', fill: 'none', stroke: '#14161a', 'stroke-width': 2.6 }, g); }
      if (d.type === 'vpc' || d.type === 'deb') { el('rect', { x: -26, y: -24, width: 52, height: 34, rx: 2, 'class': 'box' }, g);
        el('path', { d: 'M-12 22h24M0 10v12', stroke: '#14161a', 'stroke-width': 3 }, g);
        if (d.type === 'deb') el('path', { d: 'M6 -14a8 8 0 1 0 0 12', fill: 'none', stroke: '#c70036', 'stroke-width': 3 }, g); }
      el('text', { y: 46, 'class': 'lbl' }, g).textContent = d.name;
      el('text', { y: 61, 'class': 'mdl' }, g).textContent = d.model + ipLabel(d);
      g.addEventListener('pointerdown', function (e) { startDrag(e, d); });
    });
  }
  function ipLabel(d) { var f = net.ifaces(d.id)[0]; return f && (d.type === 'vpc' || d.type === 'deb') ? ' · ' + f.ip : ''; }
  function svgPt(e) { var p = cv.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; return p.matrixTransform(cv.getScreenCTM().inverse()); }
  function startDrag(e, d) {
    e.stopPropagation();
    if (tool === 'cable') { pickPort(d, e); return; }
    var p0 = svgPt(e), x0 = d.x, y0 = d.y, moved = false;
    function mv(ev) { var p = svgPt(ev); d.x = Math.max(50, Math.min(950, x0 + p.x - p0.x)); d.y = Math.max(40, Math.min(570, y0 + p.y - p0.y));
      if (Math.abs(p.x - p0.x) + Math.abs(p.y - p0.y) > 3) moved = true;
      var g = cv.querySelector('[data-id="' + d.id + '"]'); if (g) g.setAttribute('transform', 'translate(' + d.x + ',' + d.y + ') scale(1.5)'); if (moved) drawLinksOnly(); }
    function up() { window.removeEventListener('pointermove', mv); window.removeEventListener('pointerup', up); if (!moved) selectDev(d.id); draw(); }
    window.addEventListener('pointermove', mv); window.addEventListener('pointerup', up);
  }
  function drawLinksOnly() { draw(); }
  cv.addEventListener('pointerdown', function () { if (tool !== 'cable') { selLink = null; draw(); } closePop(); });

  // ------------------------------------------------------------------ кабель: выбор портов
  var pop = null;
  function closePop() { if (pop) { pop.remove(); pop = null; } }
  function pickPort(d, e) {
    closePop();
    var free = net.freePorts(d.id);
    if (!free.length) { toast('У ' + d.name + ' нет свободных портов'); return; }
    if (cable && cable.a === d.id) { cable = null; draw(); return; }
    pop = document.createElement('div'); pop.className = 'pop';
    pop.innerHTML = '<b>' + d.name + ': порт</b>' + free.map(function (p) { return '<button data-p="' + p + '">' + p + '</button>'; }).join('');
    var r = cv.parentNode.getBoundingClientRect();
    pop.style.left = Math.min(e.clientX - r.left + 10, r.width - 190) + 'px'; pop.style.top = Math.min(e.clientY - r.top, r.height - 290) + 'px';
    cv.parentNode.appendChild(pop);
    pop.addEventListener('pointerdown', function (ev) { ev.stopPropagation(); });
    pop.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-p]'); if (!b) return;
      if (!cable) { cable = { a: d.id, ap: b.dataset.p }; hint('Теперь щёлкните второе устройство'); }
      else { var err = net.connect(cable.a, cable.ap, d.id, b.dataset.p); if (err) toast(err); cable = null; hint('Кабель проложен. Щёлкните следующее устройство или выключите режим «Кабель»'); refresh(); }
      closePop(); draw();
    });
  }
  $('tCable').addEventListener('click', function () { tool = tool === 'cable' ? null : 'cable'; cable = null; this.classList.toggle('on', tool === 'cable');
    hint(tool ? 'Режим «Кабель»: щёлкните первое устройство и выберите порт' : 'Щёлкните устройство — откроется консоль'); draw(); });
  function delSel() {
    if (selLink !== null) { net.disconnect(selLink); selLink = null; }
    else if (sel) { net.remove(sel); delete cons[sel]; sel = null; }
    draw(); refresh(); renderTabs(); showConsole();
  }
  $('tDel').addEventListener('click', delSel);
  document.addEventListener('keydown', function (e) { if (e.key === 'Delete' && document.activeElement !== inp && !$('mNano').classList.contains('on')) delSel(); });

  // ------------------------------------------------------------------ консоли
  function con(id) { return cons[id] || (cons[id] = { html: '', hist: [], hi: 0 }); }
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function print(t, cls) { if (!sel) return; var c = con(sel), h = '<div class="' + (cls || '') + '">' + esc(t) + '</div>'; c.html += h;
    out.insertAdjacentHTML('beforeend', h); out.scrollTop = out.scrollHeight; }
  function selectDev(id) {
    sel = id; selLink = null;
    var c = con(id);
    if (!c.html) { var d = net.devs[id];
      c.html = '<div class="s">' + esc(d.type === 'deb' ? 'Debian GNU/Linux 11 debian tty1' : d.type === 'vpc' ? 'Welcome to Virtual PC Simulator. Введите ? для справки.' :
        'Console · ' + d.model + ' · ' + d.name + (d.type === 'mes' ? '\nUser Name:admin\nPassword:*****' : '\nesr login: admin\nPassword: ********')) + '</div>'; }
    renderTabs(); showConsole(); inp.focus();
  }
  function renderTabs() {
    $('tabs').innerHTML = Object.keys(cons).filter(function (id) { return net.devs[id]; }).map(function (id) {
      return '<button data-id="' + id + '" class="' + (id === sel ? 'on' : '') + '">' + esc(net.devs[id].name) + '</button>'; }).join('');
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('[data-id]'); if (b) { selectDev(b.dataset.id); draw(); } });
  function showConsole() {
    if (!sel || !net.devs[sel]) { out.innerHTML = '<div class="empty">Щёлкните устройство на схеме, чтобы открыть его консоль.</div>'; pr.textContent = ''; return; }
    out.innerHTML = con(sel).html; out.scrollTop = out.scrollHeight; setPrompt();
  }
  function setPrompt() { if (!sel) return; var p = net.prompt(sel); pr.textContent = p; inp.type = /password: ?$/i.test(p) ? 'password' : 'text'; }
  var uiHooks = { clear: function () { con(sel).html = ''; out.innerHTML = ''; }, edit: openNano };
  function run(line) {
    var d = net.devs[sel], p = net.prompt(sel), c = con(sel);
    print(p + (inp.type === 'password' ? '' : line), 'c');
    if (line.trim()) { c.hist.push(line); } c.hi = c.hist.length;
    var r = net.exec(sel, line, uiHooks);
    if (r) print(r, /^%|Unrecognized|Bad command|command not found|Permission denied|Error|not reachable|timeout|100% packet loss|Login incorrect/.test(r) ? 'e' : '');
    setPrompt(); draw(); refresh();
    if (d.type === 'vpc' || d.type === 'deb') fillPing();
  }
  inp.addEventListener('keydown', function (e) {
    if (!sel) return;
    var c = con(sel);
    if (e.key === 'Enter') { var v = inp.value; inp.value = ''; run(v); e.preventDefault(); }
    else if (e.key === 'ArrowUp') { if (c.hi > 0) { c.hi--; inp.value = c.hist[c.hi]; } e.preventDefault(); }
    else if (e.key === 'ArrowDown') { if (c.hi < c.hist.length) { c.hi++; inp.value = c.hist[c.hi] || ''; } e.preventDefault(); }
    else if (e.key === 'Tab') { e.preventDefault(); var t = net.tab(sel, inp.value); if (t) inp.value = t; else if (net.table(sel, inp.value)) { print(net.prompt(sel) + inp.value, 'c'); print(net.help(sel, inp.value), 'h'); } }
    else if (e.key === '?' && net.table(sel, inp.value)) { e.preventDefault(); print(net.prompt(sel) + inp.value + '?', 'c'); print(net.help(sel, inp.value), 'h'); }
  });
  out.addEventListener('click', function () { if (!getSelection().toString()) inp.focus(); });

  // ------------------------------------------------------------------ nano
  var nanoSave = null;
  function openNano(name, text, save) { nanoSave = save; $('nanoT').textContent = 'GNU nano 5.4    ' + name; $('nanoTx').value = text; $('mNano').classList.add('on'); $('nanoTx').focus(); }
  function nanoClose(saveIt) { if (saveIt && nanoSave) { nanoSave($('nanoTx').value); toast('Файл сохранён'); } if (!saveIt) { $('mNano').classList.remove('on'); inp.focus(); } }
  $('nanoS').addEventListener('click', function () { nanoClose(true); });
  $('nanoX').addEventListener('click', function () { nanoClose(false); });
  $('nanoTx').addEventListener('keydown', function (e) {
    if (e.ctrlKey && (e.key === 's' || e.key === 'S' || e.key === 'ы')) { e.preventDefault(); nanoClose(true); }
    if (e.ctrlKey && (e.key === 'x' || e.key === 'X' || e.key === 'ч')) { e.preventDefault(); nanoClose(false); }
    e.stopPropagation();
  });

  // ------------------------------------------------------------------ ping из панели
  function fillPing() {
    var s = $('pSrc'), v = s.value;
    s.innerHTML = net.list().filter(function (d) { return net.ifaces(d.id).length; }).map(function (d) { return '<option value="' + d.id + '">' + esc(d.name) + '</option>'; }).join('');
    if (v && net.devs[v]) s.value = v;
    var ips = []; net.list().forEach(function (d) { net.ifaces(d.id).forEach(function (f) { ips.push('<option value="' + f.ip + '">' + esc(d.name + ' ' + f.name) + '</option>'); }); });
    $('pIps').innerHTML = ips.join('');
  }
  $('pGo').addEventListener('click', function () {
    var s = $('pSrc').value, d = $('pDst').value.trim();
    if (!s) { toast('Нет устройств с IP-адресом'); return; }
    if (EL.ip.ip2n(d) === null) { toast('Введите адрес получателя'); return; }
    var r = net.ping(s, d); showTrace(r, s, d);
    toast(net.devs[s].name + ' → ' + d + ': ' + (r.ok ? 'ответ получен' : 'нет ответа (' + r.why + ')'));
  });

  // ------------------------------------------------------------------ пошаговая трасса пакета
  net.onTrace = function (r, id, dst) { showTrace(r, id, dst); };
  function showTrace(r, id, dst) {
    stopTrace();
    trace = { steps: r.steps.length ? r.steps : [{ k: r.ok ? 'ok' : 'drop', t: r.ok ? 'Адрес принадлежит самому устройству' : (r.why || 'нет ответа') }], i: 0, title: net.devs[id].name + ' → ' + dst, ok: r.ok };
    $('trace').classList.add('on'); play();
  }
  function stopTrace() { if (trace && trace.timer) { clearTimeout(trace.timer); trace.timer = null; } var g = $('pk'); if (g) g.innerHTML = ''; }
  function renderStep(animate) {
    var s = trace.steps[trace.i], cls = { arp: 'arp', arpr: 'arp', ip: 'ip', drop: 'drop', ok: 'ok', route: '' }[s.k];
    $('trN').textContent = trace.title + ' · шаг ' + (trace.i + 1) + ' из ' + trace.steps.length + (trace.i === trace.steps.length - 1 ? (trace.ok ? ' · ДОСТАВЛЕНО' : ' · НЕ ДОСТАВЛЕНО') : '');
    $('trT').className = 't ' + cls; $('trT').textContent = s.t;
    $('trNotes').textContent = (s.notes || []).length && (s.k === 'drop' || s.k === 'arp') ? 'Отброшено по пути: ' + s.notes.join('; ') : '';
    var dur = 0; if (animate && s.segs) dur = animSegs(s.segs, s.k === 'arp', { arp: '#d98c00', arpr: '#d98c00', ip: '#1756f5' }[s.k] || '#178a4c');
    return dur;
  }
  function animSegs(segs, flood, color) {
    var g = $('pk'); if (!g) return 0; g.innerHTML = '';
    var dur = 650, gap = flood ? 160 : dur, total = 0;
    segs.forEach(function (sg, i) {
      var a = net.devs[sg.from], b = net.devs[sg.to]; if (!a || !b) return;
      var t0 = (flood ? depth(segs, i) : i) * gap; total = Math.max(total, t0 + dur);
      var dot = el('g', { 'class': 'pkt' }, g); el('circle', { r: 9, fill: color }, dot);
      if (sg.tag !== null) el('text', { x: 12, y: -10 }, dot).textContent = 'VLAN ' + sg.tag;
      dot.setAttribute('opacity', 0);
      var st = performance.now() + t0;
      (function step(now) { var k = (now - st) / dur;
        if (k < 0) { requestAnimationFrame(step); return; }
        if (k > 1) { dot.setAttribute('opacity', 0.35); return; }
        dot.setAttribute('opacity', 1);
        dot.setAttribute('transform', 'translate(' + (a.x + (b.x - a.x) * k) + ',' + (a.y + (b.y - a.y) * k) + ')');
        requestAnimationFrame(step); })(performance.now());
    });
    return total;
  }
  function depth(segs, i) {                   // глубина отрезка в дереве рассылки: сколько отрезков до него ведут
    var d = 0, cur = segs[i];
    for (var guard = 0; guard < 20; guard++) {
      var par = segs.slice(0, segs.indexOf(cur)).filter(function (s) { return s.to === cur.from; }).pop();
      if (!par) break; d++; cur = par;
    }
    return d;
  }
  function play() { if (!trace) return; var dur = renderStep(true);
    if (trace.i < trace.steps.length - 1) trace.timer = setTimeout(function () { trace.i++; play(); }, Math.max(dur, 900) + 500); }
  $('trace').addEventListener('click', function (e) {
    var b = e.target.closest('[data-t]'); if (!b || !trace) return;
    var a = b.dataset.t; stopTrace();
    if (a === 'close') { $('trace').classList.remove('on'); trace = null; return; }
    if (a === 'first') trace.i = 0;
    if (a === 'prev') trace.i = Math.max(0, trace.i - 1);
    if (a === 'next') trace.i = Math.min(trace.steps.length - 1, trace.i + 1);
    if (a === 'play') { trace.i = 0; play(); return; }
    renderStep(true);
  });

  // ------------------------------------------------------------------ лабы
  function labList() {
    $('lab').innerHTML = '<div class="k">Лабораторные NTF2 · синтаксис MES и ESR</div><h2>Выберите работу</h2>' +
      '<p>Каждый запуск — новый вариант: номера VLAN и адреса меняются. Проверка идёт после каждой команды.</p><div class="labs">' +
      EL.labs.LABS.map(function (L) { return '<button data-lab="' + L.id + '"><b>' + L.id + '</b>' + esc(L.title) + '</button>'; }).join('') + '</div>';
  }
  function startLab(id) {
    lab = EL.labs.byId(id); labP = lab.gen(); labSolShown = false; resetNet();
    lab.build(net, labP); draw(); fillPing(); renderLab();
    var first = net.list()[0]; if (first) selectDev(first.id);
  }
  function renderLab() {
    if (mode !== 'lab' || !lab) return;
    var ts = lab.tasks(labP), ok = 0;
    var li = ts.map(function (t) { var y = false; try { y = !!t.ok(net); } catch (e) { y = false; } if (y) ok++; return '<li class="' + (y ? 'ok' : '') + '">' + t.t + '</li>'; }).join('');
    var sol = '';
    if (labSolShown) { var s = lab.sol(labP); sol = Object.keys(s).map(function (n) { return '<b>' + n + '</b><pre>' + esc(s[n].join('\n')) + '</pre>'; }).join('') + (lab.alt ? '<p>' + esc(lab.alt) + '</p>' : ''); }
    $('lab').innerHTML = '<div class="k">Лабораторная ' + lab.id + '</div><h2>' + esc(lab.title) + '</h2><p>' + esc(lab.goal) + '</p><ol>' + li + '</ol>' +
      '<div class="sum ' + (ok === ts.length ? 'ok' : '') + '">' + (ok === ts.length ? 'Работа выполнена ✓' : 'Выполнено ' + ok + ' из ' + ts.length) + '</div>' +
      (lab.hint && labSolShown === 'hint' ? '<div class="hintbox">' + esc(lab.hint(labP)) + '</div>' : '') +
      '<div class="row"><button data-a="new" class="pri">Новый вариант</button>' + (lab.hint ? '<button data-a="hint">Подсказка</button>' : '') +
      '<button data-a="sol">' + (labSolShown === true ? 'Скрыть решение' : 'Решение') + '</button><button data-a="list">Все работы</button></div>' + (labSolShown === true ? sol : '');
  }
  // ------------------------------------------------------------------ случайные задания (как в деках)
  function startTask(kind) {
    resetNet(); var d = net.add('MES2428', 'SW1', 500, 300); d.st.mode = 'priv';
    task = EL.labs.randomTask(kind); task.kind = kind; task.dev = d.id; if (task.T.setup) task.T.setup(task.P, d.st);
    task.html = task.T.text(task.P); task.res = ''; task.sol = false;
    draw(); selectDev(d.id); renderTask();
  }
  function renderTask() {
    if (mode !== 'task') return;
    if (!task) { $('lab').innerHTML = '<div class="k">Задания</div><h2>Случайное задание на коммутатор</h2><p>Те же задания, что в тренажёрах дек «Базовая настройка» и «VLAN». Решение проверяется по итоговому состоянию коммутатора.</p>' +
      '<div class="row"><button data-a="tbase" class="pri">Базовая настройка</button><button data-a="tvlan" class="pri">VLAN</button></div>'; return; }
    var T = task.T;
    $('lab').innerHTML = '<div class="k">Задание · ' + (task.kind === 'base' ? 'базовая настройка' : 'VLAN') + '</div><p style="color:var(--ink);font-weight:600">' + task.html + '</p>' +
      '<div class="row"><button data-a="tcheck" class="pri">Проверить</button>' + (T.send ? '<button data-a="tsend">Отправить кадр</button>' : '') +
      '<button data-a="t' + task.kind + '">Другое задание</button><button data-a="tsol">Решение</button><button data-a="tback">Назад</button></div>' + task.res +
      (task.sol ? '<pre>' + esc(T.sol(task.P).join('\n')) + '</pre>' : '');
  }
  $('lab').addEventListener('click', function (e) {
    var b = e.target.closest('[data-lab],[data-a]'); if (!b) return;
    if (b.dataset.lab) { startLab(b.dataset.lab); return; }
    var a = b.dataset.a, st = task && net.devs[task.dev] && net.devs[task.dev].st;
    if (a === 'new') startLab(lab.id);
    if (a === 'sol') { labSolShown = labSolShown === true ? false : true; renderLab(); }
    if (a === 'hint') { labSolShown = 'hint'; renderLab(); }
    if (a === 'list') { lab = null; labList(); }
    if (a === 'tbase' || a === 'tvlan') startTask(a.slice(1));
    if (a === 'tback') { task = null; renderTask(); }
    if (a === 'tsol') { task.sol = !task.sol; renderTask(); }
    if (a === 'tcheck') { var cs = task.T.checks(task.P), ok = 0;
      task.res = '<div class="send">' + cs.map(function (c) { var y = !!c[1](st); if (y) ok++; return '<div class="' + (y ? 'ok' : 'no') + '">' + (y ? '✓ ' : '✗ ') + c[0] + '</div>'; }).join('') +
        '</div><div class="sum ' + (ok === cs.length ? 'ok' : '') + '">' + (ok === cs.length ? 'Задание выполнено ✓' : 'Выполнено ' + ok + ' из ' + cs.length) + '</div>'; renderTask(); }
    if (a === 'tsend') { var r = task.T.send(task.P, st);
      task.res = '<div class="send">' + r.map(function (x) { return '<div class="' + (x.ok ? 'ok' : x.exp ? 'exp' : 'no') + '">✉ ' + esc(x.t) + '</div>'; }).join('') + '</div>'; renderTask(); }
  });
  function refresh() { if (mode === 'lab') renderLab(); }

  // ------------------------------------------------------------------ режимы и файл
  function resetNet() { stopTrace(); $('trace').classList.remove('on'); net = new EL.Net(); net.onTrace = function (r, id, dst) { showTrace(r, id, dst); };
    sel = null; selLink = null; cons = {}; renderTabs(); showConsole(); fillPing(); draw(); }
  $('nav').addEventListener('click', function (e) {
    var b = e.target.closest('[data-m]'); if (!b) return;
    if (b.dataset.m === 'help') { $('mHelp').classList.add('on'); return; }
    mode = b.dataset.m;
    [].forEach.call(this.children, function (x) { x.classList.toggle('on', x === b); });
    $('lab').classList.toggle('on', mode !== 'free');
    if (mode === 'lab') { if (lab) renderLab(); else labList(); }
    if (mode === 'task') renderTask();
  });
  $('bClear').addEventListener('click', function () { if (net.list().length && !confirm('Очистить схему?')) return; lab = null; task = null; resetNet(); if (mode === 'lab') labList(); if (mode === 'task') renderTask(); });
  $('bSave').addEventListener('click', function () {
    var blob = new Blob([JSON.stringify(net.toJSON(), null, 1)], { type: 'application/json' }), a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = 'eltex-shema.json'; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
  });
  $('bOpen').addEventListener('click', function () { $('fOpen').click(); });
  $('fOpen').addEventListener('change', function () {
    var f = this.files[0]; if (!f) return; var rd = new FileReader();
    rd.onload = function () { try { var n = EL.Net.fromJSON(JSON.parse(rd.result)); resetNet(); net = n; net.onTrace = function (r, id, dst) { showTrace(r, id, dst); };
        draw(); fillPing(); toast('Схема загружена: ' + net.list().length + ' устройств'); } catch (err) { toast('Не удалось открыть файл: ' + err.message); } };
    rd.readAsText(f); this.value = '';
  });
  $('mHelp').addEventListener('click', function (e) { if (e.target === this || e.target.closest('.close')) this.classList.remove('on'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { $('mHelp').classList.remove('on'); closePop(); } });

  var tt = null;
  function toast(t) { var x = $('toast'); x.textContent = t; x.classList.add('on'); clearTimeout(tt); tt = setTimeout(function () { x.classList.remove('on'); }, 2600); }
  function hint(t) { $('hint').textContent = t; }

  // ------------------------------------------------------------------ старт: демо-схема
  buildPalette();
  $('helpBody').innerHTML = document.getElementById('helpSrc') ? document.getElementById('helpSrc').innerHTML : '';
  (function demo() {
    var s = net.add('MES2428', 'SW1', 500, 330), r = net.add('vESR', 'R1', 500, 120);
    var a = net.add('VPC', 'VPC1', 230, 470), b = net.add('VPC', 'VPC2', 770, 470);
    net.connect(s.id, 'gi1/0/24', r.id, 'gi1/0/1'); net.connect(a.id, 'eth0', s.id, 'gi1/0/1'); net.connect(b.id, 'eth0', s.id, 'gi1/0/2');
    draw(); fillPing(); selectDev(s.id); draw();
  })();
  window.ELUI = { net: function () { return net; }, run: function (id, l) { sel = id; run(l); }, startLab: startLab };
})();
