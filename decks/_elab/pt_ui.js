/* Окно «Симуляция пакетов» (режим «Тест»), как Simulation в Packet Tracer: пока окно открыто, каждый обмен (ping, curl, DHCP,
   telnet …) попадает в список событий со временем модели; ▶ — проигрывание, шаги вперёд/назад, фильтр протоколов; конверты
   цвета протокола идут по кабелям в своём темпе (быстрый линк — короче). Щелчок по событию — карточка PDU по уровням OSI и L1:
   линейный код кабеля и рисунок сигнала первых байт кадра (MAC назначения). */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  var COL = { ARP: '#ffc65c', ICMP: '#6fe3ea', ICMPv6: '#6fe3ea', DHCP: '#7dffb0', DNS: '#c99bff', TCP: '#ff9d6b', UDP: '#9db7ff', HTTP: '#ff9d6b', HTTPS: '#ff9d6b', SSH: '#ff9d6b',
    Telnet: '#ff9d6b', NTP: '#9db7ff', BGP: '#ffd36b', ESP: '#ff7bd5', GRE: '#ff7bd5' };
  var S = { ev: [], i: -1, playing: false, timer: 0, off: {}, speed: 1 };
  function test() { return U.mode() === 'test'; }
  function net() { return U.net(); }
  function color(p) { return COL[p] || '#d9f7f9'; }
  function fmt(t) { return t < 1e-3 ? (t * 1e6).toFixed(1) + ' мкс' : (t * 1e3).toFixed(3) + ' мс'; }

  var items0 = X.items, run0 = X.run, side0 = X.side, click0 = X.sideClick, mode0 = X.onMode;
  X.items = function (k) { return items0(k) + (k === 'field' && test() ? '<button data-a="pt"><span>✉</span>Симуляция пакетов</button>' : ''); };
  X.run = function (k, a, arg) { run0(k, a, arg); if (k === 'field' && a === 'pt') open(); };
  X.side = function (tab) { return side0(tab) + (tab === 'file' && test() ? '<h4>Симуляция пакетов</h4><button class="act" data-s="pt">Список событий (как Packet Tracer)</button>' +
    '<p class="note">Пока окно открыто, ping, curl, DHCP и другие обмены идут сюда по шагам: время на кабеле, фильтр протоколов, PDU по уровням OSI и сигнал на L1.</p>' : ''); };
  X.sideClick = function (a) { click0(a); if (a === 'pt') open(); };
  X.onMode = function (m) { mode0(m); if (m === 'work') { stop(); U.closeWin('pt', true); U.closeWin('pdu', true); } };
  X.onTrace = function (r, id, dst) {
    if (!U.wins.pt) return false;
    if (r.steps.flush) r.steps.flush();
    var base = S.ev.length ? S.ev[S.ev.length - 1].t + S.ev[S.ev.length - 1].dur + 1e-3 : 0, n = net();
    var title = (n.devs[id] ? n.devs[id].name : '?') + ' → ' + dst + (r.ok ? '' : ' · не доставлено');
    EL.ptEvents(n, r.steps, id).forEach(function (e) { e.t += base; e.title = title; S.ev.push(e); });
    render(); if (!S.playing) { S.playing = true; tick(); } return true;
  };

  // ---------------------------------------------------------------- окно
  function open() {
    if (!test()) return;
    var body = document.createElement('div'); body.className = 'cap pt';
    body.innerHTML = '<div class="cbar"><button data-p="first" title="К началу">⏮</button><button data-p="back" title="Шаг назад">◀</button><button data-p="play">▶ Проиграть</button>' +
      '<button data-p="fwd" title="Шаг вперёд">▶|</button><button data-p="clear">Сброс</button><span class="cnt">Скорость <select data-p="spd"><option value="0.5">0,5×</option><option value="1" selected>1×</option><option value="2">2×</option><option value="4">4×</option></select></span>' +
      '<span class="clk">t = 0</span></div><div class="flt"></div><div class="list"><table><thead><tr><th></th><th>Время</th><th>Последнее устройство</th><th>На устройстве</th><th>Тип</th><th>Инфо</th></tr></thead><tbody></tbody></table></div>' +
      '<div class="det">Окно открыто — отправьте ping из консоли или «Ping отсюда…»: события появятся здесь. Щелчок по строке — PDU по уровням OSI и сигнал на кабеле.</div>';
    U.makeWin('pt', 'Симуляция пакетов', 'список событий · время модели', body, { w: Math.min(860, innerWidth - 40), h: Math.min(420, innerHeight - 160), x: 20, y: Math.max(70, innerHeight - 490) });
    body.addEventListener('click', function (e) {
      var b = e.target.closest('[data-p]'), row = e.target.closest('tr[data-i]'), f = e.target.closest('[data-f]');
      if (f) { S.off[f.dataset.f] = !S.off[f.dataset.f]; render(); return; }
      if (row) { stop(); S.i = +row.dataset.i; show(true); pdu(S.ev[S.i]); return; }
      if (!b) return; var a = b.dataset.p;
      if (a === 'play') { if (S.playing) stop(); else { if (S.i >= vis().length - 1) S.i = -1; S.playing = true; tick(); } }
      if (a === 'fwd') { stop(); step(1); } if (a === 'back') { stop(); step(-1); } if (a === 'first') { stop(); S.i = -1; show(false); }
      if (a === 'clear') { stop(); S.ev = []; S.i = -1; render(); document.getElementById('pk').innerHTML = ''; }
      render(); });
    body.querySelector('[data-p="spd"]').addEventListener('change', function () { S.speed = +this.value; });
    render();
  }
  function vis() { return S.ev.map(function (e, i) { return i; }).filter(function (i) { return !S.off[S.ev[i].proto]; }); }
  function render() {
    var w = U.wins.pt; if (!w) return; var el = w.el, tb = el.querySelector('tbody'), n = net(), V = vis(), cur = V[S.i];
    var P = []; S.ev.forEach(function (e) { if (P.indexOf(e.proto) < 0) P.push(e.proto); });
    el.querySelector('.flt').innerHTML = 'Фильтр: ' + (P.map(function (p) { return '<label data-f="' + esc(p) + '"><i style="background:' + color(p) + '"></i>' + (S.off[p] ? '<s>' + esc(p) + '</s>' : esc(p)) + '</label>'; }).join('') || '—');
    tb.innerHTML = V.map(function (k, i) { var e = S.ev[k], fd = n.devs[e.from], td = n.devs[e.to];
      return '<tr data-i="' + i + '" class="' + (i === S.i ? 'on' : i > S.i ? 'fut' : '') + '"><td><i style="background:' + color(e.proto) + '"></i></td><td>' + fmt(e.t) + '</td><td>' + esc(fd ? fd.name : '') +
        '</td><td>' + esc(e.kind === 'pdu' && td ? td.name : '—') + '</td><td>' + esc(e.proto) + '</td><td>' + esc(e.text.slice(0, 90)) + '</td></tr>'; }).join('');
    el.querySelector('[data-p="play"]').textContent = S.playing ? '❚❚ Пауза' : '▶ Проиграть';
    var c = S.ev[cur]; el.querySelector('.clk').textContent = 't = ' + (c ? fmt(c.t + c.dur) : '0');
    var on = tb.querySelector('tr.on'); if (on && S.playing) on.scrollIntoView({ block: 'nearest' });
  }
  function stop() { S.playing = false; clearTimeout(S.timer); }
  function step(d) { var V = vis(); S.i = Math.max(-1, Math.min(V.length - 1, S.i + d)); show(true); if (S.ev[V[S.i]]) pdu(S.ev[V[S.i]], true); }
  function tick() { if (!S.playing || !U.wins.pt) { S.playing = false; render(); return; } var V = vis();
    if (S.i >= V.length - 1) { S.playing = false; render(); return; }
    S.i++; var ms = show(true); render(); S.timer = setTimeout(tick, Math.max(350, ms) / S.speed); }
  // анимация события: конверт по кабелю; длительность — по времени кадра на линке (логарифмически, чтобы 10 Гбит/с и RS-232 были различимы)
  function show(anim) {
    var g = document.getElementById('pk'), n = net(); g.innerHTML = ''; var e = S.ev[vis()[S.i]]; render(); if (!e || e.kind !== 'pdu') return 300;
    var a0 = n.devs[e.from], b0 = n.devs[e.to]; if (!a0 || !b0) return 300;
    var of = U.linkOff ? U.linkOff(e.li) : { x: 0, y: 0 }, A = { x: a0.x + of.x, y: a0.y + of.y }, B = { x: b0.x + of.x, y: b0.y + of.y };
    var dur = Math.max(450, Math.min(2600, 900 + 220 * Math.log10(e.dur / 1e-6 + 1))) / S.speed;
    var env = U.el('g', { 'class': 'pkt' }, g); U.el('path', { d: 'M-12 -8h24v16h-24z', fill: color(e.proto) }, env); U.el('path', { d: 'M-12 -8l12 9 12-9', fill: 'none', stroke: '#0e1b1e', 'stroke-width': 1.6 }, env);
    U.el('text', { x: 15, y: -11 }, env).textContent = e.proto + (e.tag !== null && e.tag !== undefined ? ' · VLAN ' + e.tag : '');
    if (!anim) { env.setAttribute('transform', 'translate(' + B.x + ',' + B.y + ')'); return 300; }
    var st = performance.now();
    (function fr(now) { var k = Math.min(1, (now - st) / dur); env.setAttribute('transform', 'translate(' + (A.x + (B.x - A.x) * k) + ',' + (A.y + (B.y - A.y) * k) + ')'); if (k < 1 && g.contains(env)) requestAnimationFrame(fr); })(st);
    return dur;
  }

  // ---------------------------------------------------------------- карточка PDU
  function pdu(e, quiet) {
    if (!e) return; var n = net();
    var body = document.createElement('div'); body.className = 'pad pdu';
    var h = '<div class="k">' + esc(e.title || '') + '</div><h2>' + esc(e.proto) + ' · ' + esc(n.devs[e.from] ? n.devs[e.from].name : '') + (e.kind === 'pdu' ? ' → ' + esc(n.devs[e.to] ? n.devs[e.to].name : '') : '') + '</h2><p>' + esc(e.text) + '</p>';
    if (e.kind === 'pdu') {
      var lc = EL.lineCode(n, e.li), L = e.f && EL.decode ? EL.decode(e.f, e.tag === undefined ? null : e.tag, e.bytes) : [];
      if (lc) { var by = EL.ptBytes(e.f), wv = EL.waveform(lc.code, by);
        h += '<h3>L1 — ' + esc(lc.name) + '</h3><p>' + esc(lc.text) + '</p><p>Кадр ' + e.bytes + ' байт на линке: ' + fmt(e.dur) + ' (передача + распространение 100 м). Сигнал первых байт MAC назначения ' +
          by.map(function (b) { return ('0' + b.toString(16)).slice(-2); }).join(':') + ' (младший бит первым):</p>' + wave(wv, lc.code); }
      h += '<h3>Уровни OSI</h3><div class="osi">' + L.map(function (x) { return '<details' + (x.osi !== 'L1' ? ' open' : '') + '><summary><b>' + x.osi + '</b> ' + esc(x.name) + '</summary>' +
        x.fields.map(function (f) { return '<div>' + esc(f[0]) + ': ' + esc(String(f[1])) + '</div>'; }).join('') + '</details>'; }).join('') + '</div>';
    }
    U.closeWin('pdu', true); U.makeWin('pdu', 'PDU', e.proto + ' · уровни OSI', body, { w: 520, h: Math.min(560, innerHeight - 140), x: Math.max(20, innerWidth - 560), y: 70 });
    body.innerHTML = h; void quiet;
  }
  function wave(w, code) {
    var L = w.levels, n = L.length, W = Math.max(360, n * (code === 'pam5' ? 22 : 9)), H = 90, mid = 45, amp = 30, dx = W / n, d = 'M0 ' + (mid - L[0] * amp);
    L.forEach(function (v, i) { var y = mid - v * amp; d += ' L' + (i * dx).toFixed(1) + ' ' + y + ' L' + ((i + 1) * dx).toFixed(1) + ' ' + y; });
    var bits = code === 'manchester' ? w.bits : w.bits, bw = W / bits.length;
    var lab = bits.map(function (b, i) { return '<text x="' + (i * bw + bw / 2).toFixed(1) + '" y="12" text-anchor="middle">' + b + '</text>'; }).join('');
    return '<div class="wave"><svg viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H + '"><line x1="0" y1="' + mid + '" x2="' + W + '" y2="' + mid + '" class="ax" />' +
      '<path d="' + d + '" class="sig" />' + lab + '</svg></div>';
  }
})();
