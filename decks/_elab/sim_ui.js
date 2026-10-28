/* Окно «Симуляция» режима «Тест» (поверх sim.js): потоки ping/UDP, прогон во времени, анимация кадров по кабелям
   в замедленном модельном времени (как в OMNeT++: часы модели, очереди, потери), итоговая статистика. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  var HOP_MS = 650, GAP_MS = 700, MAX_ANIM = 400;
  function net() { return U.net(); }
  function test() { return U.mode() === 'test'; }
  function hosts() { var n = net(); return n.list().filter(function (d) { return !d.off && n.ifaces(d.id).length; }); }
  function fmt(s) { if (s === undefined || s === null) return '—'; if (s < 1e-3) return (s * 1e6).toFixed(1) + ' мкс'; if (s < 1) return (s * 1e3).toFixed(3) + ' мс'; return s.toFixed(3) + ' с'; }
  var last = null;
  var flows = [{ kind: 'ping', src: '', dst: '', size: 64, count: 5, interval: 1, df: false, rate: 1000, dur: 0.5 }], qcap = 64, anim = null;

  // ---------------------------------------------------------------- меню и панель
  var items0 = X.items, run0 = X.run, side0 = X.side, click0 = X.sideClick, mode0 = X.onMode;
  X.items = function (k) { return items0(k) + (k === 'field' && test() ? '<button data-a="sim"><span>⏱</span>Симуляция трафика</button>' : ''); };
  X.run = function (k, a, arg) { run0(k, a, arg); if (k === 'field' && a === 'sim') openSim(); };
  X.side = function (tab) { return side0(tab) + (tab === 'file' && test() ? '<h4>Симуляция во времени</h4><button class="act" data-s="sim">Симуляция трафика</button>' +
    '<p class="note">Потоки ping и UDP во времени: задержка передачи по скорости линка, распространение, очереди портов, потери, MTU. Как OMNeT++, но на этой схеме.</p>' : ''); };
  X.sideClick = function (a) { click0(a); if (a === 'sim') openSim(); };
  X.onMode = function (m) { mode0(m); if (m === 'work') { stopAnim(); U.closeWin('sim', true); } };

  // ---------------------------------------------------------------- окно
  function row(f, i, H) {
    var opt = function (v, t, cur) { return '<option value="' + esc(v) + '"' + (v === cur ? ' selected' : '') + '>' + esc(t) + '</option>'; };
    var src = H.map(function (d) { return opt(d.name, d.name, f.src); }).join('');
    return '<tr data-i="' + i + '"><td><select data-f="kind">' + opt('ping', 'ping', f.kind) + opt('udp', 'UDP', f.kind) + '</select></td>' +
      '<td><select data-f="src">' + src + '</select></td><td><input data-f="dst" value="' + esc(f.dst) + '" placeholder="10.0.0.2" spellcheck="false"></td>' +
      '<td><input data-f="size" type="number" min="28" max="9000" value="' + f.size + '"></td>' +
      (f.kind === 'ping' ? '<td><input data-f="count" type="number" min="1" max="200" value="' + f.count + '"> шт</td><td><input data-f="interval" type="number" min="0.001" step="0.1" value="' + f.interval + '"> с</td>'
        : '<td><input data-f="rate" type="number" min="1" max="20000" value="' + f.rate + '"> п/с</td><td><input data-f="dur" type="number" min="0.01" max="5" step="0.1" value="' + f.dur + '"> с</td>') +
      '<td><input data-f="dscp" type="number" min="0" max="63" value="' + (f.dscp || 0) + '" style="width:48px"></td>' +
      '<td><label><input data-f="df" type="checkbox"' + (f.df ? ' checked' : '') + '> DF</label></td><td><button data-c="del">✕</button></td></tr>';
  }
  function openSim() {
    if (!test()) return;
    var H = hosts(); if (!H.length) { U.toast('На схеме нет устройств с IP-адресом'); return; }
    flows.forEach(function (f) { if (!H.some(function (d) { return d.name === f.src; })) f.src = H[0].name; });
    var body = document.createElement('div'); body.className = 'cap sim';
    body.innerHTML = '<div class="cbar"><button data-c="run">▶ Запустить</button><button data-c="add">+ Поток</button><button data-c="stop">■ Стоп</button>' +
      '<span class="cnt">Очередь порта <input data-g="qcap" type="number" min="1" max="1000" value="' + qcap + '"> кадров</span><span class="clk">t = 0</span></div>' +
      '<div class="list"><table><thead><tr><th>Поток</th><th>Откуда</th><th>Куда (IP)</th><th>Данные, байт</th><th>Сколько</th><th>Интервал</th><th>DSCP</th><th></th><th></th></tr></thead><tbody></tbody></table></div>' +
      '<div class="det">Задайте потоки и нажмите «Запустить». Кадры летят по кабелям в замедленном модельном времени, часы вверху — время модели.</div>';
    U.makeWin('sim', 'Симуляция', 'потоки во времени · очереди · потери', body, { w: Math.min(900, innerWidth - 40), h: Math.min(400, innerHeight - 160), x: 20, y: Math.max(70, innerHeight - 470) });
    var tb = body.querySelector('tbody'), det = body.querySelector('.det');
    function paint() { tb.innerHTML = flows.map(function (f, i) { return row(f, i, H); }).join(''); }
    paint();
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('change', function (e) { var t = e.target, g = t.dataset.g, k = t.dataset.f, tr = t.closest('tr[data-i]');
      if (g === 'qcap') qcap = Math.max(1, Math.min(1000, +t.value || 64));
      if (!k || !tr) return; var f = flows[+tr.dataset.i];
      f[k] = t.type === 'checkbox' ? t.checked : (t.type === 'number' ? +t.value : t.value.trim());
      if (k === 'kind') paint(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-c]'); if (!b) return; var c = b.dataset.c;
      if (c === 'add') { var l = flows[flows.length - 1]; flows.push(EL.clone(l)); paint(); }
      if (c === 'del') { if (flows.length > 1) flows.splice(+b.closest('tr').dataset.i, 1); paint(); }
      if (c === 'stop') stopAnim();
      if (c === 'run') simulate(body, det);
      if (c === 'res' && last && EL.simRes) EL.simRes.open(last); });
  }
  function simulate(body, det) {
    var n = net(), bad = null;
    var fl = flows.map(function (f) { var d = n.byName(f.src);
      if (!d) bad = 'нет устройства ' + f.src; else if (EL.ip.ip2n(f.dst) === null) bad = 'адрес назначения ' + (f.dst || '(пусто)') + ' — не IPv4';
      return { kind: f.kind, src: d && d.id, dst: f.dst, size: Math.max(28, Math.min(9000, f.size | 0)), count: Math.max(1, Math.min(200, f.count | 0)), interval: Math.max(0.001, +f.interval || 1),
               rate: Math.max(1, Math.min(20000, +f.rate || 100)), dur: Math.max(0.01, Math.min(5, +f.dur || 0.5)), df: !!f.df, dscp: Math.max(0, Math.min(63, f.dscp | 0)) }; });
    if (bad) { det.innerHTML = '<span style="color:var(--bad)">' + esc(bad) + '</span>'; return; }
    stopAnim();
    var r = n.simulate(fl, { qcap: qcap }); n.gen++;
    det.innerHTML = '<div class="row"><button class="pri" data-c="res">Результаты: журнал, векторы, гистограммы, скаляры</button></div>' + report(r); last = r;
    play(r, body.querySelector('.clk'));
  }
  function report(r) {
    var h = '<table><thead><tr><th>Поток</th><th>Отправлено</th><th>Получено</th><th>Потери</th><th>min</th><th>avg</th><th>max</th><th>Джиттер</th></tr></thead><tbody>' +
      r.flows.map(function (f, i) { var d = net().devs[f.src];
        return '<tr><td>' + (i + 1) + '. ' + (f.kind === 'ping' ? 'ping (RTT)' : 'UDP (в одну сторону)') + ' ' + esc((d ? d.name : '?') + ' → ' + f.dst) + (f.frag > 1 ? ' · ' + f.frag + ' фрагм.' : '') +
          '</td><td>' + f.sent + '</td><td>' + f.recv + '</td><td' + (f.loss ? ' style="color:var(--bad)"' : '') + '>' + f.loss + ' %</td><td>' + fmt(f.min) + '</td><td>' + fmt(f.avg) + '</td><td>' + fmt(f.max) + '</td><td>' + fmt(f.jitter) + '</td></tr>'; }).join('') + '</tbody></table>';
    var why = []; r.flows.forEach(function (f, i) { Object.keys(f.drops).forEach(function (k) { why.push((i + 1) + '. ' + k + ' — ' + f.drops[k]); }); });
    if (why.length) h += '<p><b>Потери:</b><br>' + why.map(esc).join('<br>') + '</p>';
    if (r.links.length) h += '<p><b>Загрузка кабелей</b> (за ' + fmt(r.tEnd) + '):<br>' + r.links.map(function (l) { return esc(l.name) + ' — ' + l.mbps + ' Мбит/с, кадров ' + l.frames + ', ' + l.util.toFixed(1) + ' %'; }).join('<br>') + '</p>';
    if (r.queues.length) h += '<p><b>Очереди</b> (максимум кадров):<br>' + r.queues.map(function (q) { return esc(q.name) + ' — ' + q.maxq; }).join('<br>') + '</p>';
    if (r.truncated) h += '<p style="color:var(--bad)">Слишком много событий — прогон остановлен на 200 000.</p>';
    return h;
  }

  // ---------------------------------------------------------------- анимация в замедленном модельном времени
  // соседние события идут в своём темпе, длинные паузы между пакетами сжаты до GAP_MS — как «быстрая перемотка» в OMNeT++
  function stopAnim() { if (anim) { cancelAnimationFrame(anim.raf); anim = null; } var g = document.getElementById('pk'); if (g) g.innerHTML = ''; }
  function play(r, clk) {
    var ev = r.events.filter(function (e) { return e.kind === 'tx' || e.kind === 'drop'; }).sort(function (a, b) { return a.t - b.t; }).slice(0, MAX_ANIM);
    if (!ev.length) { clk.textContent = 't = 0'; return; }
    var hops = ev.filter(function (e) { return e.kind === 'tx'; }).map(function (e) { return e.t2 - e.t1; }).sort(function (a, b) { return a - b; });
    var k = HOP_MS / ((hops[hops.length >> 1] || 1e-5) * 1000);           // мс экрана на мс модели
    var real = 0, prev = ev[0].t;
    ev.forEach(function (e) { real += Math.min(GAP_MS, (e.t - prev) * 1000 * k); prev = e.t; e.r0 = real; e.r1 = real + (e.kind === 'tx' ? Math.max(120, (e.t2 - e.t1) * 1000 * k) : 500); });
    var g = document.getElementById('pk'), n = net(), t0 = performance.now(), end = Math.max.apply(null, ev.map(function (e) { return e.r1; })), COL = ['#6fe3ea', '#ffc65c', '#c99bff', '#7dffb0'];
    g.innerHTML = '';
    var dots = ev.map(function (e) { var a0 = n.devs[e.seg.from], b0 = n.devs[e.seg.to]; if (!a0 || !b0) return null;
      var of = n.links[e.seg.li] ? U.linkOff(e.seg.li) : { x: 0, y: 0 }, d = U.el('g', { 'class': 'pkt', opacity: 0 }, g);
      if (e.kind === 'drop') U.el('text', { x: -6, y: 6, fill: '#ff6b62', 'font-size': 22 }, d).textContent = '✕';
      else U.el('path', { d: 'M-8 -5h16v10h-16z', fill: COL[e.flow % COL.length], opacity: e.dir === 'bk' ? 0.65 : 1 }, d);
      return { e: e, d: d, a: { x: a0.x + of.x, y: a0.y + of.y }, b: { x: b0.x + of.x, y: b0.y + of.y } }; }).filter(Boolean);
    anim = { raf: 0 };
    (function step(now) { if (!anim) return; var t = now - t0, mt = null;
      dots.forEach(function (o) { var e = o.e, q = (t - e.r0) / (e.r1 - e.r0);
        if (q < 0 || q > 1) { o.d.setAttribute('opacity', 0); return; }
        if (mt === null || e.t > mt) mt = e.kind === 'tx' ? e.t1 + (e.t2 - e.t1) * q : e.t;
        var p = e.kind === 'tx' ? q : 0.5;
        o.d.setAttribute('opacity', 1); o.d.setAttribute('transform', 'translate(' + (o.a.x + (o.b.x - o.a.x) * p) + ',' + (o.a.y + (o.b.y - o.a.y) * p) + ')'); });
      if (mt !== null) clk.textContent = 't = ' + fmt(mt);
      if (t < end) anim.raf = requestAnimationFrame(step); else { clk.textContent = 't = ' + fmt(r.tEnd) + (r.events.length > MAX_ANIM ? ' · показаны первые ' + MAX_ANIM + ' кадров' : ''); g.innerHTML = ''; anim = null; } })(t0);
  }
})();
