/* Тренажёр CLI маршрутизатора Eltex ESR для деки 2.4 «Маршрутизация».
   Режимы и приглашения как в pptx: R1# → configure → R1(config)# → interface gigabitethernet 1/0/1 → R1(config-if-gi)#,
   подинтерфейс gi1/0/1.10 → R1(config-subif)#. Таблица маршрутизации строится из состояния: C — адрес на интерфейсе up/up,
   S — ip route (в FIB попадает маршрут с наименьшей метрикой и достижимым next-hop). Проверка — по итоговому состоянию. */
(function () {
  'use strict';
  var NP = 8;
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }

  // ------------------------------------------------------------------ адреса
  function ip2n(s) { var p = s.split('.').map(Number); if (p.length !== 4 || p.some(function (x) { return isNaN(x) || x < 0 || x > 255; })) return null;
    return ((p[0] << 24) >>> 0) + (p[1] << 16) + (p[2] << 8) + p[3]; }
  function n2ip(n) { return [n >>> 24, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join('.'); }
  function mask(l) { return l === 0 ? 0 : (0xFFFFFFFF << (32 - l)) >>> 0; }
  function net(ipn, l) { return (ipn & mask(l)) >>> 0; }
  function inNet(ipn, nn, l) { return net(ipn, l) === nn; }
  function parsePfx(s) { var m = String(s).match(/^(\d+\.\d+\.\d+\.\d+)\s*\/\s*(\d{1,2})$/); if (!m) return null;
    var n = ip2n(m[1]), l = +m[2]; if (n === null || l > 32) return null; return { ip: n, len: l }; }

  function fresh(links) {
    var ifs = {};
    for (var i = 1; i <= NP; i++) ifs['gi1/0/' + i] = { ip: null, len: 0, shut: false, fw: true, link: links.indexOf(i) >= 0 };
    return { host: 'R1', mode: 'priv', ctx: null, ifs: ifs, routes: [], commit: false, confirm: false, t0: Date.now() };
  }
  var PROMPT = { priv: '#', config: '(config)#', 'if': '(config-if-gi)#', subif: '(config-subif)#' };
  function prompt(st) { return st.host + PROMPT[st.mode]; }

  function ifName(t) {
    t = t.toLowerCase().replace(/^gigabitethernet/, 'gi');
    var m = t.match(/^gi(\d)\/(\d)\/(\d+)(?:\.(\d+))?$/);
    if (!m || m[1] !== '1' || m[2] !== '0' || +m[3] < 1 || +m[3] > NP) return null;
    return m[4] ? 'gi1/0/' + m[3] + '.' + (+m[4]) : 'gi1/0/' + m[3];
  }
  function up(st, k) { var f = st.ifs[k]; if (!f) return false; var base = st.ifs[k.split('.')[0]];
    return !f.shut && !base.shut && base.link; }

  // ------------------------------------------------------------------ таблица маршрутизации
  function connected(st) {
    var out = [];
    Object.keys(st.ifs).forEach(function (k) { var f = st.ifs[k]; if (f.ip !== null && up(st, k)) out.push({ c: 'C', net: net(f.ip, f.len), len: f.len, dev: k, pref: 0, met: 0 }); });
    return out;
  }
  function resolve(st, nh) { var c = connected(st); for (var i = 0; i < c.length; i++) if (inNet(nh, c[i].net, c[i].len)) return c[i].dev; return null; }
  function rib(st) {
    var all = connected(st);
    st.routes.forEach(function (r) {
      var dev = r.dev ? (up(st, r.dev) ? r.dev : null) : resolve(st, r.nh);
      all.push({ c: 'S', net: r.net, len: r.len, nh: r.nh, dev: dev, pref: 1, met: r.met || 0, bad: !dev });
    });
    // FIB: по префиксу — наименьшие preference, затем метрика
    var best = {};
    all.forEach(function (r) { if (r.bad) return; var k = r.net + '/' + r.len, b = best[k];
      if (!b || r.pref < b.pref || (r.pref === b.pref && r.met < b.met)) best[k] = r; });
    all.forEach(function (r) { r.fib = best[r.net + '/' + r.len] === r; });
    return all;
  }
  function lookup(st, dst) {
    var f = rib(st).filter(function (r) { return r.fib && inNet(dst, r.net, r.len); });
    f.sort(function (a, b) { return b.len - a.len; });
    return f[0] || null;
  }
  function pad(s, n) { s = String(s); while (s.length < n) s += ' '; return s; }
  function hms(st) { var s = Math.floor((Date.now() - st.t0) / 1000); return [Math.floor(s / 3600), Math.floor(s / 60) % 60, s % 60]
    .map(function (x) { return (x < 10 ? '0' : '') + x; }).join(':'); }
  var CODES = ' Codes: C - connected, S - static, R - RIP derived,\n        O - OSPF derived, IA - OSPF inter area route,\n' +
              '        E1 - OSPF external type 1 route, E2 - OSPF external type 2 route\n' +
              '        B - BGP derived, D - DHCP derived, K - kernel route, V - VRRP route\n' +
              '        i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area\n        * - FIB route\n';
  function showRoute(st, what) {
    var rows = rib(st).filter(function (r) {
      if (what === 'static') return r.c === 'S'; if (what === 'connected') return r.c === 'C';
      return what === 'all' ? !r.bad : r.fib; });
    var o = [CODES];
    rows.forEach(function (r) {
      var via = r.c === 'C' ? 'dev ' + r.dev : ('via ' + n2ip(r.nh || 0) + ' on ' + r.dev);
      if (r.c === 'S' && !r.nh) via = 'dev ' + r.dev;
      o.push(pad(r.c, 6) + pad(r.fib ? '*' : '', 2) + pad(n2ip(r.net) + '/' + r.len, 20) + pad('[' + r.pref + '/' + r.met + ']', 12) +
             pad(via, 32) + '[' + (r.c === 'C' ? 'direct ' : 'static ') + hms(st) + ']');
    });
    return o.join('\n');
  }
  function showIf(st) {
    var o = ['IP address                              Interface              Admin    Link     Type',
             '-------------------------------------   -------------------    -----    -----    ------'];
    Object.keys(st.ifs).forEach(function (k) { var f = st.ifs[k]; if (f.ip === null) return;
      var b = st.ifs[k.split('.')[0]];
      o.push(pad(n2ip(f.ip) + '/' + f.len, 40) + pad(k, 23) + pad(f.shut ? 'Down' : 'Up', 9) + pad(b.link && !b.shut && !f.shut ? 'Up' : 'Down', 9) + 'static'); });
    return o.join('\n');
  }

  // ------------------------------------------------------------------ команды
  function exec(st, line) {
    var s = line.trim().replace(/\s+/g, ' '); if (!s) return '';
    var low = s.toLowerCase();
    if (/^do /.test(low) && st.mode !== 'priv') { s = s.slice(3); low = low.slice(3);
      if (!/^(sh|sho|show)\b/.test(low)) return exec(st, s);
      var save = st.mode; st.mode = 'priv'; var r0 = exec(st, s); st.mode = save; return r0; }
    var m;
    if (/^(sh|sho|show) (ip )?route( (all|static|connected))?$/.test(low) || /^(sh|sho|show) ip route( (all|static|connected))?$/.test(low)) {
      if (st.mode !== 'priv') return '% Неизвестная команда в этом режиме (используйте do show …)';
      return showRoute(st, (low.match(/(all|static|connected)$/) || [])[1]); }
    if (/^(sh|sho|show) ip int(erfaces)?$/.test(low)) { if (st.mode !== 'priv') return '% Используйте do show ip interfaces'; return showIf(st); }
    if (low === 'configure' || low === 'configure terminal' || low === 'conf t') {
      if (st.mode !== 'priv') return '% Неизвестная команда'; st.mode = 'config'; return ''; }
    if (low === 'end') { st.mode = 'priv'; st.ctx = null; return ''; }
    if (low === 'exit') { if (st.mode === 'priv') return '% Сессия остаётся открытой (тренажёр)';
      st.mode = st.mode === 'config' ? 'priv' : 'config'; st.ctx = null; return ''; }
    if (low === 'commit') { if (st.mode === 'priv') return '% Неизвестная команда'; st.commit = true; st.confirm = false;
      return 'Configuration has been successfully applied and saved to flash. Commit timer started, changes will be reverted in 600 seconds.'; }
    if (low === 'confirm') { if (!st.commit) return '% Нечего подтверждать: сначала commit';
      st.confirm = true; return 'Configuration has been confirmed. Commit timer canceled.'; }
    if (st.mode === 'priv') return '% Неизвестная команда. Для настройки войдите в режим configure';
    if ((m = low.match(/^hostname (\S+)$/)) && st.mode === 'config') { st.host = s.split(' ')[1]; return ''; }
    if ((m = low.match(/^interface (gigabitethernet ?\S+|gi\S+)$/))) {
      var nm = ifName(m[1].replace(/\s/g, '')); if (!nm) return '% Неверное имя интерфейса (gigabitethernet 1/0/1–1/0/' + NP + ')';
      if (nm.indexOf('.') > 0) { if (!st.ifs[nm]) st.ifs[nm] = { ip: null, len: 0, shut: false, fw: true, link: true }; st.mode = 'subif'; }
      else st.mode = 'if';
      st.ctx = nm; st.commit = false; return ''; }
    if (st.mode === 'if' || st.mode === 'subif') {
      var f = st.ifs[st.ctx];
      if ((m = s.match(/^ip (?:add|addr|address) (\d+\.\d+\.\d+\.\d+\s*\/\s*\d{1,2})$/i))) {
        var pf = parsePfx(m[1]); if (!pf) return '% Неверный адрес';
        if (pf.len < 8 || pf.len > 30 && pf.len !== 32) return '% Недопустимая длина префикса';
        f.ip = pf.ip; f.len = pf.len; st.commit = false; return ''; }
      if (/^no ip (add|addr|address)$/.test(low)) { f.ip = null; st.commit = false; return ''; }
      if (low === 'ip firewall disable') { f.fw = false; st.commit = false; return ''; }
      if (low === 'shutdown') { f.shut = true; st.commit = false;
        return st.mode === 'if' ? '%LINK-W-DOWN: gigabitethernet ' + st.ctx.slice(2) + ' changed state to down' : ''; }
      if (low === 'no shutdown') { var was = f.shut; f.shut = false; st.commit = false;
        return was && st.mode === 'if' && f.link ? '%LINK-I-UP: gigabitethernet ' + st.ctx.slice(2) + ' changed state to up' : ''; }
    }
    if (st.mode === 'config') {
      if ((m = s.match(/^ip route (\S+) (\d+\.\d+\.\d+\.\d+)(?: (\d+))?$/i))) {
        var p1 = parsePfx(m[1]); if (!p1) return '% Сеть назначения задаётся как A.B.C.D/NN';
        if (net(p1.ip, p1.len) !== p1.ip) return '% Адрес сети не совпадает с маской: ' + n2ip(net(p1.ip, p1.len)) + '/' + p1.len;
        var met = m[3] ? +m[3] : 0; if (met > 255) return '% Метрика 0..255';
        st.routes = st.routes.filter(function (r) { return !(r.net === p1.ip && r.len === p1.len && r.nh === ip2n(m[2])); });
        st.routes.push({ net: p1.ip, len: p1.len, nh: ip2n(m[2]), met: met }); st.commit = false; return ''; }
      if ((m = s.match(/^ip route (\S+) interface (gigabitethernet ?\S+|gi\S+)$/i))) {
        var p2 = parsePfx(m[1]), d = ifName(m[2].replace(/\s/g, '')); if (!p2 || !d) return '% Неверная команда';
        st.routes.push({ net: net(p2.ip, p2.len), len: p2.len, nh: null, dev: d, met: 0 }); st.commit = false; return ''; }
      if ((m = s.match(/^no ip route (\S+)(?: (\d+\.\d+\.\d+\.\d+))?$/i))) {
        var p3 = parsePfx(m[1]); if (!p3) return '% Неверная команда'; var n0 = st.routes.length;
        st.routes = st.routes.filter(function (r) { return !(r.net === p3.ip && r.len === p3.len && (!m[2] || r.nh === ip2n(m[2]))); });
        st.commit = false; return n0 === st.routes.length ? '% Маршрут не найден' : ''; }
    }
    return '% Неизвестная команда или неверный режим: ' + line.trim();
  }

  // ------------------------------------------------------------------ задания (по примерам pptx 2.4)
  function oct() { return rnd(1, 254); }
  function hasC(st, dev, ip, len) { var f = st.ifs[dev]; return f && f.ip === ip2n(ip) && f.len === len && up(st, dev); }
  function hasS(st, n, l, nh, met) { return st.routes.some(function (r) { return r.net === ip2n(n) && r.len === l && r.nh === ip2n(nh) && (r.met || 0) === (met || 0); }); }
  function send(st, dst) {
    var r = lookup(st, ip2n(dst));
    if (!r) return { ok: false, t: 'Пакет для ' + dst + ': подходящего маршрута нет — пакет отброшен' };
    var how = r.c === 'C' ? 'сеть подключена напрямую — кадр уходит узлу из ' + r.dev
                          : 'маршрут S ' + n2ip(r.net) + '/' + r.len + ' → next-hop ' + n2ip(r.nh || 0) + ', выход ' + r.dev;
    return { ok: true, t: 'Пакет для ' + dst + ': ' + how };
  }
  var TASKS = [
    { gen: function () { var a = pick([10, 20, 30]), b = oct(); return { a: '192.168.' + a + '.1', n1: '192.168.' + a + '.0', b: '203.0.' + rnd(100, 120) + '.1' }; },
      links: [1, 2],
      text: function (p) { return 'Новый маршрутизатор R1. Настройте <b>gi1/0/1</b> — <b>' + p.a + '/24</b> (сеть ПК1), <b>gi1/0/2</b> — <b>' + p.b +
                                  '/24</b> (канал к R2). Проверьте <b>show ip route</b>: должны появиться две сети с кодом C.'; },
      sol: function (p) { return ['configure', 'interface gigabitethernet 1/0/1', 'ip address ' + p.a + '/24', 'exit',
                                  'interface gigabitethernet 1/0/2', 'ip address ' + p.b + '/24', 'exit', 'end', 'show ip route']; },
      checks: function (p) { return [['C: gi1/0/1 ' + p.a + '/24 (up/up)', function (s) { return hasC(s, 'gi1/0/1', p.a, 24); }],
                                     ['C: gi1/0/2 ' + p.b + '/24 (up/up)', function (s) { return hasC(s, 'gi1/0/2', p.b, 24); }]]; },
      send: function (p, s) { return [send(s, p.a.replace(/\.1$/, '.254')), send(s, '10.10.10.10')]; } },
    { gen: function () { var r = pick([20, 30, 40]); return { r: '192.168.' + r + '.0', d: '192.168.' + r + '.' + oct() }; },
      links: [1, 2],
      setup: function (p, s) { s.ifs['gi1/0/1'].ip = ip2n('192.168.10.1'); s.ifs['gi1/0/1'].len = 24; s.ifs['gi1/0/2'].ip = ip2n('203.0.113.1'); s.ifs['gi1/0/2'].len = 24; },
      text: function (p) { return 'Интерфейсы R1 уже настроены: gi1/0/1 — 192.168.10.1/24, gi1/0/2 — 203.0.113.1/24. Добавьте статический маршрут в сеть <b>' +
                                  p.r + '/24</b> через R2 <b>203.0.113.2</b>, затем проверьте <b>show ip route static</b> и отправьте пакет.'; },
      sol: function (p) { return ['configure', 'ip route ' + p.r + '/24 203.0.113.2', 'end', 'show ip route static']; },
      checks: function (p) { return [['S ' + p.r + '/24 via 203.0.113.2', function (s) { return hasS(s, p.r, 24, '203.0.113.2'); }],
                                     ['Маршрут в FIB (next-hop достижим)', function (s) { var r = lookup(s, ip2n(p.d)); return r && r.c === 'S'; }]]; },
      send: function (p, s) { return [send(s, p.d)]; } },
    { gen: function () { return { x: pick(['8.8.8.8', '1.1.1.1', '77.88.8.8', '203.0.113.200']) }; },
      links: [1, 3],
      setup: function (p, s) { s.ifs['gi1/0/1'].ip = ip2n('192.168.10.1'); s.ifs['gi1/0/1'].len = 24; s.ifs['gi1/0/3'].ip = ip2n('203.0.113.1'); s.ifs['gi1/0/3'].len = 24; },
      text: function (p) { return 'R1 — тупиковый маршрутизатор: gi1/0/1 — 192.168.10.1/24, gi1/0/3 — 203.0.113.1/24 (к R2). Настройте <b>маршрут по умолчанию</b> ' +
                                  '(«шлюз последней надежды») через <b>203.0.113.2</b> и проверьте, куда уйдёт пакет на ' + p.x + '.'; },
      sol: function () { return ['configure', 'ip route 0.0.0.0/0 203.0.113.2', 'end', 'show ip route']; },
      checks: function () { return [['S 0.0.0.0/0 via 203.0.113.2', function (s) { return hasS(s, '0.0.0.0', 0, '203.0.113.2'); }]]; },
      send: function (p, s) { return [send(s, p.x)]; } },
    { gen: function () { return { m: pick([10, 20, 50]) }; },
      links: [1, 2, 3],
      setup: function (p, s) { [['gi1/0/1', '198.18.0.1', 30], ['gi1/0/2', '198.51.100.1', 30], ['gi1/0/3', '192.0.2.1', 24]].forEach(function (x) {
        s.ifs[x[0]].ip = ip2n(x[1]); s.ifs[x[0]].len = x[2]; }); },
      text: function (p) { return 'Как на схеме pptx: R1 — R2 (198.18.0.0/30) и R1 — R3 (198.51.100.0/30). Настройте основной маршрут в <b>203.0.113.0/24</b> через ' +
                                  '<b>198.18.0.2</b> и плавающий через <b>198.51.100.2</b> с метрикой <b>' + p.m + '</b>. Затем выключите gi1/0/1 (shutdown) и снова отправьте пакет.'; },
      sol: function (p) { return ['configure', 'ip route 203.0.113.0/24 198.18.0.2', 'ip route 203.0.113.0/24 198.51.100.2 ' + p.m, 'end', 'show ip route all',
                                  'configure', 'interface gigabitethernet 1/0/1', 'shutdown', 'end', 'show ip route']; },
      checks: function (p) { return [['Основной: 203.0.113.0/24 via 198.18.0.2', function (s) { return hasS(s, '203.0.113.0', 24, '198.18.0.2'); }],
                                     ['Плавающий: via 198.51.100.2, метрика ' + p.m, function (s) { return hasS(s, '203.0.113.0', 24, '198.51.100.2', p.m); }],
                                     ['gi1/0/1 выключен — в FIB плавающий маршрут', function (s) { var r = lookup(s, ip2n('203.0.113.10')); return s.ifs['gi1/0/1'].shut && r && r.nh === ip2n('198.51.100.2'); }]]; },
      send: function (p, s) { return [send(s, '203.0.113.10')]; } },
    { gen: function () { var a = pick([10, 20, 30]), b = a + 10; return { a: a, b: b }; },
      links: [1],
      text: function (p) { return 'Router-on-a-Stick: к gi1/0/1 R1 подключён транк L2SW-1 с VLAN ' + p.a + ' и ' + p.b + '. Создайте подинтерфейсы <b>gi1/0/1.' + p.a +
                                  '</b> — <b>10.10.1.1/24</b> и <b>gi1/0/1.' + p.b + '</b> — <b>10.10.2.1/24</b>, на каждом <b>ip firewall disable</b>, затем commit и confirm.'; },
      sol: function (p) { return ['configure', 'interface gi1/0/1.' + p.a, 'ip add 10.10.1.1/24', 'ip firewall disable', 'exit',
                                  'interface gi1/0/1.' + p.b, 'ip add 10.10.2.1/24', 'ip firewall disable', 'exit', 'do commit', 'do confirm', 'end', 'show ip route']; },
      checks: function (p) { return [['gi1/0/1.' + p.a + ': 10.10.1.1/24, firewall disable', function (s) { var f = s.ifs['gi1/0/1.' + p.a]; return f && f.ip === ip2n('10.10.1.1') && f.len === 24 && !f.fw; }],
                                     ['gi1/0/1.' + p.b + ': 10.10.2.1/24, firewall disable', function (s) { var f = s.ifs['gi1/0/1.' + p.b]; return f && f.ip === ip2n('10.10.2.1') && f.len === 24 && !f.fw; }],
                                     ['commit + confirm', function (s) { return s.commit && s.confirm; }]]; },
      send: function (p, s) { return [send(s, '10.10.2.10'), send(s, '10.10.1.15')]; } },
    { gen: function () { return { o: pick([1, 2, 3]) }; },
      links: [1, 2],
      text: function () { return 'Традиционный метод: gi1/0/1 R1 — шлюз VLAN 10 (<b>10.10.1.1/24</b>), gi1/0/2 — шлюз VLAN 20 (<b>10.10.2.1/24</b>). На обоих интерфейсах ' +
                                 '<b>ip firewall disable</b> и <b>no shutdown</b>, затем <b>do commit</b> и <b>do confirm</b>.'; },
      setup: function (p, s) { s.ifs['gi1/0/1'].shut = true; s.ifs['gi1/0/2'].shut = true; },
      sol: function () { return ['configure', 'interface gi1/0/1', 'ip address 10.10.1.1/24', 'ip firewall disable', 'no shutdown', 'exit',
                                 'interface gi1/0/2', 'ip address 10.10.2.1/24', 'ip firewall disable', 'no shutdown', 'do commit', 'do confirm', 'end', 'show ip route']; },
      checks: function () { return [['C 10.10.1.0/24 dev gi1/0/1', function (s) { return hasC(s, 'gi1/0/1', '10.10.1.1', 24) && !s.ifs['gi1/0/1'].fw; }],
                                    ['C 10.10.2.0/24 dev gi1/0/2', function (s) { return hasC(s, 'gi1/0/2', '10.10.2.1', 24) && !s.ifs['gi1/0/2'].fw; }],
                                    ['commit + confirm', function (s) { return s.commit && s.confirm; }]]; },
      send: function (p, s) { return [send(s, '10.10.2.20')]; } }
  ];
  window.M4CLI = { TASKS: TASKS, fresh: fresh, exec: exec, lookup: lookup, ip2n: ip2n };

  // ------------------------------------------------------------------ виджет
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function init(box) {
    var pool = (box.dataset.pool || '').split(',').map(Number);
    var out = box.querySelector('.cs-out'), inp = box.querySelector('.cs-in input'), pr = box.querySelector('.cs-pr');
    var taskEl = box.querySelector('.cs-task'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol');
    var st, T, P, hist = [], hi = 0, last = -1;
    function print(t, cls) { var d = document.createElement('div'); d.className = cls || ''; d.innerHTML = esc(t); out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function newTask() {
      var k; do { k = pool[rnd(0, pool.length - 1)]; } while (pool.length > 1 && k === last); last = k;
      T = TASKS[k]; P = T.gen(); st = fresh(T.links); if (T.setup) T.setup(P, st);
      taskEl.innerHTML = T.text(P); res.innerHTML = ''; sol.style.display = 'none'; sol.textContent = T.sol(P).join('\n');
      out.innerHTML = ''; print('Eltex ESR · console. Подключение установлено. Кабели подключены к: ' +
                                T.links.map(function (i) { return 'gi1/0/' + i; }).join(', '), 'cs-sys');
      pr.textContent = prompt(st);
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var v = inp.value; print(prompt(st) + ' ' + v, 'cs-cmd'); hist.push(v); hi = hist.length;
        var r = exec(st, v); if (r) print(r, /^%[^L]/.test(r) ? 'cs-err' : ''); inp.value = ''; pr.textContent = prompt(st); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { if (hi > 0) { hi--; inp.value = hist[hi]; } e.preventDefault(); }
      else if (e.key === 'ArrowDown') { if (hi < hist.length) { hi++; inp.value = hist[hi] || ''; } e.preventDefault(); }
      e.stopPropagation();
    });
    out.addEventListener('click', function () { inp.focus(); });
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cs]'); if (!b) return; var a = b.dataset.cs;
      if (a === 'new') newTask();
      if (a === 'sol') sol.style.display = sol.style.display === 'none' ? 'block' : 'none';
      if (a === 'check') { var cs = T.checks(P), ok = 0;
        res.innerHTML = cs.map(function (c) { var y = !!c[1](st); if (y) ok++; return '<div class="' + (y ? 'ok' : 'no') + '">' + (y ? '✓ ' : '✗ ') + esc(c[0]) + '</div>'; }).join('') +
          '<div class="cs-sum ' + (ok === cs.length ? 'ok' : 'no') + '">' + (ok === cs.length ? 'Задание выполнено' : 'Выполнено ' + ok + ' из ' + cs.length) + '</div>'; }
      if (a === 'send') { var r = T.send(P, st);
        res.innerHTML = '<div class="cs-send">' + r.map(function (x) { return '<div class="' + (x.ok ? 'ok' : 'no') + '"><span class="env">✉</span> ' + esc(x.t) + '</div>'; }).join('') + '</div>'; }
    });
    newTask();
  }
  document.querySelectorAll('.clisim[data-deck="m4"]').forEach(init);
})();
