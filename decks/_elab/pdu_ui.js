/* «Простой PDU» и «Сложный PDU» (как в Packet Tracer): конверт на нижней панели — щёлкнуть источник, затем получатель → ICMP echo;
   таблица PDU: источник, получатель, тип, время (модельное), успешно / неудачно, «Повторить», «Удалить», «Повторить всё».
   Сложный PDU — протокол (ICMP, UDP, TCP), порт, размер, количество, интервал. Работает в обоих режимах (это действие, а не подсказка);
   в «Тесте» щелчок по строке открывает трассу пакета. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  function net() { return U.net(); }
  var rows = [], pick = null, seq = 0;
  // кнопка-конверт рядом с «Терминалом»
  var bt = document.getElementById('bTerm'), bp = document.createElement('button');
  bp.className = 'term-btn pdu-btn'; bp.id = 'bPdu'; bp.title = 'Простой PDU: щёлкните источник, затем получатель (ICMP echo)'; bp.innerHTML = '✉ PDU';
  if (bt) bt.parentNode.insertBefore(bp, bt.nextSibling);
  function setPick(p) { pick = p; document.body.classList.toggle('pdu-pick', !!p); bp.classList.toggle('on', !!p); }
  bp.addEventListener('click', function () { if (pick) { setPick(null); U.toast('PDU отменён'); return; } setPick({}); U.toast('PDU: щёлкните источник'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && pick) { setPick(null); U.toast('PDU отменён'); } });
  // щелчки по устройствам перехватываются до обычной обработки (перетаскивание, выделение)
  document.getElementById('gd').addEventListener('mousedown', function (e) {
    if (!pick || e.button !== 0) return; var g = e.target.closest('g.dev'); if (!g) return;
    e.stopPropagation(); e.preventDefault(); var id = g.getAttribute('data-id'), n = net(), d = n.devs[id];
    if (!pick.src) { if (!n.ifaces(id).length) { U.toast(d.name + ': нет IP-адреса — источником быть не может'); return; } pick.src = id; U.toast('PDU: источник ' + d.name + ' — щёлкните получатель'); return; }
    if (id === pick.src) { U.toast('Получатель должен отличаться от источника'); return; }
    var dst = n.pduDst(id); if (!dst) { U.toast(d.name + ': нет IP-адреса'); return; }
    var src = pick.src; setPick(null); add({ src: src, dstDev: id, dst: dst, proto: 'icmp', count: 1, simple: true });
  }, true);

  function name(id) { var d = net().devs[id]; return d ? d.name : '?'; }
  function tfmt(t) { var s = Math.floor(t || 0); return Math.floor(s / 3600) + ':' + ('0' + Math.floor(s / 60) % 60).slice(-2) + ':' + ('0' + s % 60).slice(-2); }
  function fire(row) { var n = net(), r = n.pdu(row.src, row); row.res = r; row.t = n.now || 0; row.ok = r.ok; return r; }
  function add(o) { o.n = ++seq; fire(o); rows.push(o); open(); U.draw(); if (U.mode() === 'test') showRow(o); }
  function showRow(o) { if (U.mode() === 'test' && net().onTrace) net().onTrace(o.res.r, o.src, o.dst + (o.proto !== 'icmp' ? ':' + o.port : '')); }
  function typeOf(o) { return o.proto === 'icmp' ? 'ICMP' : o.proto.toUpperCase() + ' ' + o.port; }

  function open() {
    var body = document.createElement('div'); body.className = 'pad pduw';
    function render() {
      var H = net().list().filter(function (d) { return !d.off && net().ifaces(d.id).length; });
      body.innerHTML = '<div class="row"><button data-c="all">↻ Повторить всё</button><button data-c="clr">Удалить всё</button><button data-c="cx">Сложный PDU…</button>' +
        '<span class="cs2">' + (U.mode() === 'test' ? 'Щелчок по строке — трасса пакета' : 'Трасса пакета — в режиме «Тест»') + '</span></div>' +
        '<form class="cx" hidden><div class="cxg"><label>Источник<select class="q" data-f="src">' + H.map(function (d) { return '<option value="' + d.id + '">' + esc(d.name) + '</option>'; }).join('') + '</select></label>' +
        '<label>Получатель (IP)<input class="q" data-f="dst" placeholder="10.0.0.2"></label><label>Протокол<select class="q" data-f="proto"><option value="icmp">ICMP</option><option value="udp">UDP</option><option value="tcp">TCP</option></select></label>' +
        '<label>Порт<input class="q" data-f="port" type="number" value="80"></label><label>Размер, байт<input class="q" data-f="size" type="number" value="56"></label>' +
        '<label>Количество<input class="q" data-f="count" type="number" value="1"></label><label>Интервал, с<input class="q" data-f="interval" type="number" step="0.1" value="1"></label></div>' +
        '<div class="row"><button class="pri" data-c="cxgo">Отправить</button><span class="cs"></span></div></form>' +
        '<table class="ptab"><thead><tr><th>№</th><th>Результат</th><th>Источник</th><th>Получатель</th><th>Тип</th><th>Время</th><th></th></tr></thead><tbody>' +
        rows.map(function (o, i) { return '<tr data-i="' + i + '" class="' + (o.ok ? 'ok' : 'bad') + '"><td>' + o.n + '</td><td><b>' + (o.ok ? 'Успешно' : 'Неудачно') + '</b>' +
          (o.res.sent > 1 ? ' ' + o.res.recv + '/' + o.res.sent : '') + (o.ok ? '' : '<br><i>' + esc(o.res.why || '') + '</i>') + '</td><td>' + esc(name(o.src)) + '</td><td>' + esc(o.dstDev ? name(o.dstDev) + ' · ' : '') + esc(o.dst) +
          '</td><td>' + esc(typeOf(o)) + '</td><td>' + tfmt(o.t) + '</td><td><button data-c="again" title="Повторить">↻</button><button data-c="del" title="Удалить">✕</button></td></tr>'; }).join('') +
        '</tbody></table>' + (rows.length ? '' : '<p class="cs2">PDU нет: нажмите ✉ PDU на нижней панели, затем щёлкните источник и получатель.</p>');
    }
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('submit', function (e) { e.preventDefault(); });
    body.addEventListener('click', function (e) {
      var b = e.target.closest('[data-c]'), tr = e.target.closest('tr[data-i]');
      if (!b) { if (tr) showRow(rows[+tr.dataset.i]); return; }
      var c = b.dataset.c, i = tr ? +tr.dataset.i : -1;
      if (c === 'again') { fire(rows[i]); render(); showRow(rows[i]); U.draw(); }
      if (c === 'del') { rows.splice(i, 1); render(); }
      if (c === 'all') { rows.forEach(fire); render(); U.draw(); }
      if (c === 'clr') { rows = []; render(); }
      if (c === 'cx') { var f = body.querySelector('form.cx'); f.hidden = !f.hidden; }
      if (c === 'cxgo') { var v = function (k) { return body.querySelector('[data-f="' + k + '"]').value.trim(); }, o = { src: v('src'), dst: v('dst'), proto: v('proto'), port: +v('port') || 0,
          size: Math.max(0, Math.min(9000, +v('size') || 56)), count: Math.max(1, Math.min(100, +v('count') || 1)), interval: Math.max(0.001, +v('interval') || 1) };
        if (!o.src) { body.querySelector('.cs').textContent = 'Нет устройств с IP-адресом'; return; }
        if (EL.ip.ip2n(o.dst) === null) { body.querySelector('.cs').textContent = 'Получатель — IPv4-адрес'; return; }
        if (o.proto !== 'icmp' && (o.port < 1 || o.port > 65535)) { body.querySelector('.cs').textContent = 'Порт 1–65535'; return; }
        var own = net().owner(o.dst); o.dstDev = own && (own.id || own); add(o); }
    });
    render();
    var w = U.wins.pdu; if (w) { var wb = w.el.querySelector('.wb'); wb.innerHTML = ''; wb.appendChild(body); return; }
    U.makeWin('pdu', 'PDU', 'простые и сложные', body, { w: 620, h: 260, x: 20, y: Math.max(70, innerHeight - 340) });
  }
  EL.pduOpen = open;
  var mode0 = X.onMode; X.onMode = function (m) { mode0(m); if (U.wins.pdu) open(); };
})();
