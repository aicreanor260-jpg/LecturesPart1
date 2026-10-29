/* «Результаты» симуляции в духе OMNeT++ (режим «Тест»), без внешних библиотек — графики на SVG:
   — журнал событий (время, узел, событие) с управлением: шаг, запуск, быстрее, до времени; текущий кадр подсвечивается на схеме;
   — векторы (значение во времени): загрузка выбранного порта, задержка пакетов, длина очереди порта;
   — гистограммы: распределение задержек и размеров кадров;
   — скаляры: по потокам отправлено / получено / потеряно, % потерь, RTT min/avg/max, джиттер; сходимость протоколов по ленте событий сети;
   — лента событий сети (линк, STP, OSPF, VRRP, BGP) по модельному времени — копится, пока идут часы (в т.ч. после загрузки проекта). */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  function net() { return U.net(); }
  function fmt(s) { if (s === undefined || s === null || isNaN(s)) return '—'; if (s < 1e-3) return (s * 1e6).toFixed(1) + ' мкс'; if (s < 1) return (s * 1e3).toFixed(3) + ' мс'; return s.toFixed(3) + ' с'; }
  function hms(t) { t = Math.floor(t); var p = function (v) { return ('0' + v).slice(-2); }; return p(Math.floor(t / 3600)) + ':' + p(Math.floor(t / 60) % 60) + ':' + p(t % 60); }

  // ---------------------------------------------------------------- графики
  function axes(w, h, x0, x1, y0, y1, ux, uy) {
    return '<line x1="44" y1="' + (h - 20) + '" x2="' + (w - 6) + '" y2="' + (h - 20) + '" stroke="var(--dim)"/><line x1="44" y1="6" x2="44" y2="' + (h - 20) + '" stroke="var(--dim)"/>' +
      '<text x="40" y="14" text-anchor="end" fill="var(--dim)" font-size="10">' + esc(y1) + '</text><text x="40" y="' + (h - 20) + '" text-anchor="end" fill="var(--dim)" font-size="10">' + esc(y0) + '</text>' +
      '<text x="46" y="' + (h - 6) + '" fill="var(--dim)" font-size="10">' + esc(x0) + '</text><text x="' + (w - 6) + '" y="' + (h - 6) + '" text-anchor="end" fill="var(--dim)" font-size="10">' + esc(x1) + '</text>' +
      '<text x="' + (w / 2) + '" y="' + (h - 6) + '" text-anchor="middle" fill="var(--dim)" font-size="10">' + esc(ux) + '</text><text x="4" y="' + (h / 2) + '" fill="var(--dim)" font-size="10">' + esc(uy) + '</text>';
  }
  // вектор: точки [t, v] → ступенчатая линия
  function vector(pts, tEnd, uy, fy) {
    var w = 640, h = 180; if (!pts.length) return '<p class="note">Нет данных.</p>';
    var mx = Math.max.apply(null, pts.map(function (p) { return p[1]; })) || 1, sx = (w - 52) / (tEnd || 1), sy = (h - 30) / mx;
    var d = pts.map(function (p, i) { var x = 44 + p[0] * sx, y = h - 20 - p[1] * sy; return (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); }).join(' ');
    return '<svg viewBox="0 0 ' + w + ' ' + h + '" style="width:100%;height:auto">' + axes(w, h, '0', fmt(tEnd), '0', fy ? fy(mx) : mx.toFixed(2), 't', uy) +
      '<path d="' + d + '" fill="none" stroke="var(--cy)" stroke-width="1.6"/></svg>';
  }
  // гистограмма: значения → столбцы
  function histo(vals, bins, ux, fx) {
    var w = 640, h = 180; if (!vals.length) return '<p class="note">Нет данных.</p>';
    var mn = Math.min.apply(null, vals), mx = Math.max.apply(null, vals); if (mx === mn) { mx = mn + 1; bins = 1; }
    var c = []; for (var i = 0; i < bins; i++) c.push(0);
    vals.forEach(function (v) { c[Math.min(bins - 1, Math.floor((v - mn) / (mx - mn) * bins))]++; });
    var top = Math.max.apply(null, c), bw = (w - 52) / bins;
    return '<svg viewBox="0 0 ' + w + ' ' + h + '" style="width:100%;height:auto">' + axes(w, h, fx(mn), fx(mx), '0', String(top), ux, 'шт') +
      c.map(function (n, i) { var bh = n / top * (h - 30); return '<rect x="' + (46 + i * bw).toFixed(1) + '" y="' + (h - 20 - bh).toFixed(1) + '" width="' + Math.max(1, bw - 2).toFixed(1) + '" height="' + bh.toFixed(1) + '" fill="var(--arp,#ffc65c)" opacity=".85"><title>' + n + '</title></rect>'; }).join('') + '</svg>';
  }

  // ---------------------------------------------------------------- данные
  function ports(r) { var o = {}; r.events.forEach(function (e) { if (e.kind === 'tx' && e.port) o[e.port] = 1; }); return Object.keys(o).sort(); }
  function loadVec(r, port, bins) {               // доля времени, когда порт передавал, по интервалам
    var T = r.tEnd || 1, bw = T / bins, busy = []; for (var i = 0; i < bins; i++) busy.push(0);
    r.events.forEach(function (e) { if (e.kind !== 'tx' || e.port !== port) return; var a = e.t1, b = e.t1 + (e.tx || (e.t2 - e.t1));
      for (var k = Math.floor(a / bw); k <= Math.min(bins - 1, Math.floor(b / bw)); k++) busy[k] += Math.max(0, Math.min(b, (k + 1) * bw) - Math.max(a, k * bw)); });
    var out = []; busy.forEach(function (v, k) { var u = v / bw * 100; out.push([k * bw, u], [(k + 1) * bw, u]); }); return out;
  }
  function queueVec(r, port) { var o = [[0, 0]]; r.events.forEach(function (e) { if (e.kind === 'tx' && e.port === port) o.push([e.t1, e.q || 0]); }); o.push([r.tEnd, 0]); return o; }
  function delays(r) { return r.events.filter(function (e) { return e.kind === 'deliver' && e.delay !== undefined && (e.dir === 'bk' || r.flows[e.flow].kind === 'udp'); }); }
  function conv(log) {                            // сходимость: от последнего изменения линка до последнего изменения протоколов после него
    var L = log.filter(function (x) { return x.k === 'link'; }).pop(); if (!L) return null;
    var P = log.filter(function (x) { return x.t >= L.t && x.k !== 'link'; });
    return { from: L, last: P.length ? P[P.length - 1] : null, n: P.length };
  }

  // ---------------------------------------------------------------- окно
  var R = null, cur = -1, timer = null, speed = 1, tab = 'log';
  function open(r) {
    R = r || null; cur = -1; stop();
    var body = document.createElement('div'); body.className = 'pad simres';
    body.innerHTML = '<div class="row" data-tabs>' + [['log', 'Журнал событий'], ['vec', 'Векторы'], ['his', 'Гистограммы'], ['sca', 'Скаляры'], ['net', 'События сети']].map(function (t) {
      return '<button data-t="' + t[0] + '"' + (t[0] === tab ? ' class="pri"' : '') + '>' + t[1] + '</button>'; }).join('') + '</div>' +
      (R ? '<div class="row exp"><span>Экспорт как в OMNeT++:</span><button data-x="vec">.vec</button><button data-x="sca">.sca</button><button data-x="csv">CSV (Excel)</button>' + (EL.simNotebook ? '<button data-x="ipynb">Скачать тетрадку .ipynb</button>' : '') + '</div>' : '') + '<div data-v></div>';
    U.makeWin('simres', 'Результаты', 'как в OMNeT++: события, векторы, гистограммы, скаляры', body, { w: Math.min(760, innerWidth - 40), h: Math.min(620, innerHeight - 120), x: Math.max(20, innerWidth - 800), y: 70 });
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) { var xb = e.target.closest('[data-x]'); if (xb && R) { saveRes(xb.dataset.x); return; }
      var b = e.target.closest('[data-t],[data-k]'); if (!b) return;
      if (b.dataset.t) { tab = b.dataset.t; [].forEach.call(body.querySelectorAll('[data-t]'), function (x) { x.classList.toggle('pri', x === b); }); paint(body); return; }
      ctl(body, b.dataset.k); });
    body.addEventListener('change', function (e) { if (e.target.dataset.sel) paint(body); });
    paint(body);
  }
  // ---------------------------------------------------------------- экспорт результатов (simexp.js) и тетрадка Jupyter (simnb.js)
  function convSec() { var c = conv(net()._evlog || []); return c && c.last ? c.last.t - c.from.t : null; }
  function exportNow() { return EL.simExport(net(), R, { conv: convSec(), qcap: R.qcap }); }
  function saveRes(k) { var x = exportNow(), nm = 'netcat-' + new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-');
    var data = k === 'ipynb' ? EL.simNotebook(nm) : x[k], type = k === 'csv' ? 'text/csv;charset=utf-8' : k === 'ipynb' ? 'application/x-ipynb+json' : 'text/plain;charset=utf-8';
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([data], { type: type })); a.download = (k === 'ipynb' ? 'analiz-netcat' : nm) + '.' + k;
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000); U.toast('Сохранено: ' + a.download); }
  EL.simResData = function () { return R ? exportNow() : null; };
  function evRows() { return R ? R.events.slice().sort(function (a, b) { return a.t - b.t; }) : []; }
  function evText(e) { var n = net(), from = e.seg && n.devs[e.seg.from], to = e.seg && n.devs[e.seg.to], f = R.flows[e.flow] || {};
    var what = f.kind === 'udp' ? 'UDP' : e.dir === 'bk' ? 'ICMP echo-reply' : 'ICMP echo-request';
    if (e.kind === 'tx') return [from ? from.name : '?', what + ' #' + (e.pkt + 1) + ' → ' + (to ? to.name : '?') + ', ' + e.bytes + ' байт, очередь ' + (e.q || 0)];
    if (e.kind === 'drop') return [from ? from.name : '?', 'ПОТЕРЯ ' + what + ' #' + (e.pkt + 1) + ': ' + e.why];
    return [e.node || '?', 'доставлен ' + what + ' #' + (e.pkt + 1) + (e.delay !== undefined ? ', задержка ' + fmt(e.delay) : '')];
  }
  function paint(body) {
    var v = body.querySelector('[data-v]'), h = '';
    if (tab !== 'net' && !R) { v.innerHTML = '<p>Запустите «Симуляцию трафика» (ПКМ по полю или вкладка «Файл») — здесь появятся результаты прогона. Вкладка «События сети» работает и без неё.</p>'; return; }
    if (tab === 'log') {
      var E = evRows();
      h = '<div class="row"><button data-k="first">⏮ К началу</button><button data-k="step">⏭ Шаг</button><button data-k="run">' + (timer ? '❚❚ Пауза' : '▶ Запуск') + '</button>' +
        '<button data-k="fast">⏩ Быстрее (×' + speed + ')</button><input class="q" data-until placeholder="до t, мс" style="width:90px"><button data-k="until">До времени</button></div>' +
        '<p data-now style="color:var(--cy)">' + (cur >= 0 ? 'Событие ' + (cur + 1) + ' из ' + E.length + ', t = ' + fmt(E[cur].t) : 'Событий: ' + E.length + ' — «Шаг» или «Запуск»') + '</p>' +
        '<div style="max-height:340px;overflow:auto"><table><tr><th>#</th><th>t</th><th>Узел</th><th>Событие</th></tr>' +
        E.slice(0, 1500).map(function (e, i) { var x = evText(e); return '<tr data-row="' + i + '"' + (i === cur ? ' class="hot"' : '') + (e.kind === 'drop' ? ' style="color:var(--bad)"' : '') + '><td>' + (i + 1) + '</td><td>' + fmt(e.t) + '</td><td>' + esc(x[0]) + '</td><td>' + esc(x[1]) + '</td></tr>'; }).join('') + '</table></div>';
    }
    if (tab === 'vec') {
      var P = ports(R), sel = (body.querySelector('[data-sel="port"]') || {}).value || P[0];
      var D = delays(R).map(function (e) { return [e.t, e.delay * 1000]; });
      h = '<label>Порт (узел и интерфейс)</label><select data-sel="port">' + P.map(function (p) { return '<option' + (p === sel ? ' selected' : '') + '>' + esc(p) + '</option>'; }).join('') + '</select>' +
        '<h3>Загрузка порта, % во времени</h3>' + vector(loadVec(R, sel, 40), R.tEnd, '%', function (m) { return m.toFixed(1) + ' %'; }) +
        '<h3>Длина очереди порта, кадров</h3>' + vector(queueVec(R, sel), R.tEnd, 'кадров', function (m) { return String(Math.round(m)); }) +
        '<h3>Задержка пакетов (RTT ping / в одну сторону UDP), мс</h3>' + vector(D, R.tEnd, 'мс', function (m) { return m.toFixed(3); });
    }
    if (tab === 'his') {
      var dl = delays(R).map(function (e) { return e.delay * 1000; }), sz = R.events.filter(function (e) { return e.kind === 'tx'; }).map(function (e) { return e.bytes; });
      h = '<h3>Распределение задержек, мс</h3>' + histo(dl, 16, 'мс', function (x) { return x.toFixed(3); }) +
        '<h3>Распределение размеров кадров на кабелях, байт</h3>' + histo(sz, 12, 'байт', function (x) { return String(Math.round(x)); });
    }
    if (tab === 'sca') {
      h = '<table><tr><th>Поток</th><th>Отправлено</th><th>Получено</th><th>Потеряно</th><th>Потери</th><th>min / avg / max</th><th>Джиттер</th></tr>' + R.flows.map(function (f, i) { var d = net().devs[f.src];
        return '<tr><td>' + (i + 1) + '. ' + esc((d ? d.name : '?') + ' → ' + f.dst) + '</td><td>' + f.sent + '</td><td>' + f.recv + '</td><td>' + (f.sent - f.recv) + '</td><td>' + f.loss + ' %</td><td>' +
          fmt(f.min) + ' / ' + fmt(f.avg) + ' / ' + fmt(f.max) + '</td><td>' + fmt(f.jitter) + '</td></tr>'; }).join('') + '</table>' +
        '<h3>Кабели</h3><table><tr><th>Кабель</th><th>Скорость</th><th>Кадров</th><th>Загрузка</th></tr>' + R.links.map(function (l) { return '<tr><td>' + esc(l.name) + '</td><td>' + l.mbps + ' Мбит/с</td><td>' + l.frames + '</td><td>' + l.util.toFixed(3) + ' %</td></tr>'; }).join('') + '</table>' +
        '<p>Длительность прогона: ' + fmt(R.tEnd) + '. ' + convText() + '</p>';
    }
    if (tab === 'net') {
      var log = net()._evlog || [];
      h = '<p>' + convText() + '</p>' + timeline(log) + '<div style="max-height:300px;overflow:auto"><table><tr><th>Время сети</th><th>Узел</th><th>Событие</th></tr>' +
        log.slice().reverse().slice(0, 400).map(function (x) { return '<tr><td>' + hms(x.t) + '</td><td>' + esc(x.dev) + '</td><td>' + esc(x.msg) + '</td></tr>'; }).join('') + '</table></div>' +
        (log.length ? '' : '<p class="note">Событий ещё нет: подключите кабели, выключите порт, перезагрузите устройство — изменения линков, STP, OSPF, VRRP, BGP появятся здесь по модельному времени.</p>');
    }
    v.innerHTML = h;
  }
  function convText() { var c = conv(net()._evlog || []); if (!c) return 'Сходимость: изменений линков ещё не было.';
    return c.last ? 'Сходимость после изменения линка (' + esc(c.from.dev) + ', ' + hms(c.from.t) + '): последнее изменение протоколов через ' + Math.round(c.last.t - c.from.t) + ' с (' + c.n + ' событий).'
      : 'После последнего изменения линка (' + hms(c.from.t) + ') протоколы состояние не меняли.'; }
  function timeline(log) {
    var w = 700, h = 70; if (!log.length) return '';
    var t0 = log[0].t, t1 = Math.max(t0 + 1, log[log.length - 1].t), sx = (w - 20) / (t1 - t0), COL = { link: '#ff6b62', stp: '#ffc65c', root: '#ffc65c', ospf: '#6fe3ea', vrrp: '#c99bff', bpdug: '#ff6b62' };
    return '<svg viewBox="0 0 ' + w + ' ' + h + '" style="width:100%;height:auto"><line x1="10" y1="40" x2="' + (w - 10) + '" y2="40" stroke="var(--dim)"/>' +
      log.map(function (x) { var X0 = 10 + (x.t - t0) * sx; return '<line x1="' + X0.toFixed(1) + '" y1="22" x2="' + X0.toFixed(1) + '" y2="40" stroke="' + (COL[x.k] || '#7dffb0') + '" stroke-width="2"><title>' + esc(hms(x.t) + ' ' + x.dev + ': ' + x.msg) + '</title></line>'; }).join('') +
      '<text x="10" y="58" fill="var(--dim)" font-size="10">' + hms(t0) + '</text><text x="' + (w - 10) + '" y="58" text-anchor="end" fill="var(--dim)" font-size="10">' + hms(t1) + '</text>' +
      '<text x="10" y="14" fill="var(--dim)" font-size="10">красный — линк, жёлтый — STP, бирюза — OSPF, фиолетовый — VRRP</text></svg>';
  }

  // ---------------------------------------------------------------- управление журналом: шаг, запуск, быстрее, до времени
  function stop() { if (timer) { clearTimeout(timer); timer = null; } }
  function show(body) { var E = evRows(), e = E[cur]; paint(body);
    var row = body.querySelector('[data-row="' + cur + '"]'); if (row) row.scrollIntoView({ block: 'nearest' });
    var g = document.getElementById('pk'); if (!g) return; g.innerHTML = ''; if (!e || !e.seg) return;
    var n = net(), a = n.devs[e.seg.from], b = n.devs[e.seg.to]; if (!a || !b) return;
    var of = U.linkOff(e.seg.li), d = U.el('g', { 'class': 'pkt' }, g);
    if (e.kind === 'drop') U.el('text', { x: -6, y: 6, fill: '#ff6b62', 'font-size': 22 }, d).textContent = '✕';
    else U.el('path', { d: 'M-8 -5h16v10h-16z', fill: e.dir === 'bk' ? '#ffc65c' : '#6fe3ea' }, d);
    d.setAttribute('transform', 'translate(' + ((a.x + b.x) / 2 + of.x) + ',' + ((a.y + b.y) / 2 + of.y) + ')');
  }
  function ctl(body, k) { var E = evRows(); if (!E.length) return;
    if (k === 'first') { stop(); cur = -1; paint(body); var g = document.getElementById('pk'); if (g) g.innerHTML = ''; return; }
    if (k === 'step') { stop(); cur = Math.min(E.length - 1, cur + 1); show(body); return; }
    if (k === 'fast') { speed = speed >= 16 ? 1 : speed * 2; paint(body); return; }
    if (k === 'until') { stop(); var ms = parseFloat((body.querySelector('[data-until]') || {}).value); if (isNaN(ms)) { U.toast('Укажите время в мс модели'); return; }
      var i = 0; while (i < E.length - 1 && E[i + 1].t * 1000 <= ms) i++; cur = i; show(body); return; }
    if (k === 'run') { if (timer) { stop(); paint(body); return; }
      (function next() { if (cur >= E.length - 1) { timer = null; paint(body); return; } cur++; show(body);
        var dt = cur < E.length - 1 ? (E[cur + 1].t - E[cur].t) * 1e6 : 0;            // мкс модели → мс экрана
        timer = setTimeout(next, Math.max(40, Math.min(700, dt)) / speed); })(); paint(body); }
  }

  // вкладка «Файл»: открыть «Результаты» (события сети работают и без прогона)
  var side0 = X.side, click0 = X.sideClick;
  X.side = function (t) { return side0(t) + (t === 'file' && U.mode() === 'test' ? '<button class="act" data-s="simres">Результаты и события сети</button>' : ''); };
  X.sideClick = function (a) { click0(a); if (a === 'simres') open(R); };
  EL.simRes = { open: open };
})();
