/* Тренажёр CLI коммутатора Eltex MES (MES2308P) для дек «STP» и «Агрегация каналов LACP». Команды — со слайдов pptx:
   spanning-tree mode stp|rstp|pvst, spanning-tree priority, spanning-tree pathcost method long|short, spanning-tree hello-time /
   max-age / forward-time, на порту spanning-tree cost / portfast / bpdu filtering, vlan database → vlan, switchport mode trunk,
   switchport trunk allowed vlan add, no spanning-tree vlan; default interface, channel-group N mode on|auto|passive, no channel-group,
   interface port-channel N, lacp system-priority, lacp port-priority, lacp timeout long|short, show interfaces channel-group N.
   «Проверить с соседом» — что произойдёт в сети (корень STP, состояние LAG по таблице совместимости режимов). */
(function () {
  'use strict';
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function list(s) { var o = []; String(s).split(',').forEach(function (p) { var m = p.match(/^(\d+)-(\d+)$/);
    if (m) for (var i = +m[1]; i <= +m[2]; i++) o.push(i); else if (/^\d+$/.test(p)) o.push(+p); }); return o; }
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }).sort(function (x, y) { return x - y; }); }

  function fresh() {
    var ports = {}; for (var i = 1; i <= 8; i++) ports['0/' + i] = { cost: null, portfast: false, bpduf: false, mode: 'access', allowed: [], group: null, gmode: null, prio: 32768, timeout: 'long' };
    return { host: 'MES2308P', mode: 'priv', ctx: null, stp: { mode: 'stp', prio: 32768, method: 'short', hello: 2, maxage: 20, fwd: 15, off: [] },
             vlans: [1], ports: ports, pcs: {}, lacpSys: 1 };
  }
  var PROMPT = { priv: '#', config: '(config)#', 'if': '(config-if)#', vlan: '(config-vlan)#', pc: '(config-if)#' };
  function prompt(st) { return st.host + PROMPT[st.mode]; }
  function port(s) { var m = s.match(/^(?:gigabitethernet|gi|fastethernet|fa)\s*(?:1\/)?(0\/[1-8])$/i); return m ? m[1] : null; }

  var CMDS = [];
  function cmd(modes, re, run) { CMDS.push({ modes: modes.split(' '), re: re, run: run }); }
  var CFG = 'config if vlan pc';
  function P(st) { return st.ports[st.ctx]; }
  cmd('priv', /^(?:configure|conf)(?: terminal)?$/, function (st) { st.mode = 'config'; });
  cmd('priv', /^exit$/, function () { return '% Сессия остаётся открытой (тренажёр)'; });
  cmd(CFG, /^exit$/, function (st) { st.mode = st.mode === 'config' ? 'priv' : 'config'; st.ctx = null; });
  cmd(CFG, /^end$/, function (st) { st.mode = 'priv'; st.ctx = null; });
  // STP глобально
  cmd('config', /^spanning-tree$/, function () { });
  cmd('config', /^spanning-tree mode (stp|rstp|pvst|mst)$/, function (st, m) { st.stp.mode = m[1]; });
  cmd('config', /^spanning-tree priority (\d+)$/, function (st, m) { var v = +m[1];
    if (v > 61440 || v % 4096) return '% Приоритет 0–61440, кратный 4096'; st.stp.prio = v; });
  cmd('config', /^no spanning-tree priority$/, function (st) { st.stp.prio = 32768; });
  cmd('config', /^spanning-tree pathcost method (long|short)$/, function (st, m) { st.stp.method = m[1]; });
  cmd('config', /^spanning-tree hello-time (\d+)$/, function (st, m) { if (+m[1] < 1 || +m[1] > 10) return '% hello-time 1–10'; st.stp.hello = +m[1]; });
  cmd('config', /^spanning-tree max-age (\d+)$/, function (st, m) { st.stp.maxage = +m[1]; });
  cmd('config', /^spanning-tree forward-time (\d+)$/, function (st, m) { if (+m[1] < 4 || +m[1] > 30) return '% forward-time 4–30'; st.stp.fwd = +m[1]; });
  cmd('config', /^no spanning-tree vlan (\S+)$/, function (st, m) { st.stp.off = uniq(st.stp.off.concat(list(m[1]))); });
  cmd('config', /^vlan database$/, function (st) { st.mode = 'vlan'; });
  cmd('vlan', /^vlan (\S+)$/, function (st, m) { var l = list(m[1]); if (!l.length || l.some(function (v) { return v < 2 || v > 4094; })) return '% VLAN 2–4094';
    st.vlans = uniq(st.vlans.concat(l)); });
  // интерфейсы
  cmd('config', /^interface (?:range )?(\S+(?: \S+)?)$/, function (st, m) {
    var pc = m[1].match(/^port-channel ?(\d+)$/i);
    if (pc) { var n = +pc[1]; if (n < 1 || n > 48) return '% Номер группы 1–48'; st.pcs[n] = st.pcs[n] || {}; st.mode = 'pc'; st.ctx = 'Po' + n; return; }
    var k = port(m[1].replace(' ', '')); if (!k) return '% В тренажёре порты gigabitethernet 0/1 – 0/8'; st.mode = 'if'; st.ctx = k; });
  cmd('config', /^default interface (\S+(?: \S+)?)$/, function (st, m) { var k = port(m[1].replace(' ', '')); if (!k) return '% Неверный порт';
    st.ports[k] = fresh().ports['0/1']; return 'Configuration for these interfaces will be set to default.\nAre you sure you want to proceed? (Y/N)[N] Y'; });
  cmd('if', /^spanning-tree cost (\d+)$/, function (st, m) { var max = st.stp.method === 'long' ? 200000000 : 65535;
    if (+m[1] < 1 || +m[1] > max) return '% Стоимость 1..' + max + ' (метод ' + st.stp.method + ')'; P(st).cost = +m[1]; });
  cmd('if', /^(no )?spanning-tree portfast$/, function (st, m) { P(st).portfast = !m[1]; });
  cmd('if', /^(no )?spanning-tree bpdu filtering$/, function (st, m) { P(st).bpduf = !m[1]; });
  cmd('if', /^switchport mode (trunk|access|general)$/, function (st, m) { P(st).mode = m[1]; });
  cmd('if', /^switchport trunk allowed vlan add (\S+)$/, function (st, m) { var l = list(m[1]);
    var bad = l.filter(function (v) { return st.vlans.indexOf(v) < 0; }); if (bad.length) return '% VLAN ' + bad.join(',') + ' не созданы (vlan database)';
    P(st).allowed = uniq(P(st).allowed.concat(l)); });
  cmd('if', /^channel-group (\d+) mode (on|auto|active|passive)$/, function (st, m) { var n = +m[1]; if (n < 1 || n > 48) return '% Номер группы 1–48';
    if (m[2] === 'active') return '% На MES23xx/33xx/35xx/53xx активный режим называется auto';
    P(st).group = n; P(st).gmode = m[2]; st.pcs[n] = st.pcs[n] || {};
    return '%TRUNK-I-PORTADDED: Port gi1/0/' + st.ctx.split('/')[1] + ' added to Po' + n; });
  cmd('if', /^no channel-group$/, function (st) { P(st).group = null; P(st).gmode = null; });
  cmd('if', /^lacp port-priority (\d+)$/, function (st, m) { if (+m[1] > 65535) return '% 0–65535'; P(st).prio = +m[1]; });
  cmd('if', /^no lacp port-priority$/, function (st) { P(st).prio = 32768; });
  cmd('if', /^lacp timeout (long|short)$/, function (st, m) { P(st).timeout = m[1]; });
  cmd('if', /^no lacp timeout$/, function (st) { P(st).timeout = 'long'; });
  cmd('config', /^lacp system-priority (\d+)$/, function (st, m) { if (+m[1] > 65535) return '% 0–65535'; st.lacpSys = +m[1]; });
  cmd('config', /^no lacp system-priority$/, function (st) { st.lacpSys = 1; });
  // show
  function members(st, n) { return Object.keys(st.ports).filter(function (k) { return st.ports[k].group === n; }); }
  cmd('priv', /^show interfaces channel-group(?: (\d+))?$/, function (st, m) {
    var o = ['Load balancing: src-dst-mac-ip', '', 'Gathering information...', 'Channel  Ports', '-------  -----'];
    Object.keys(st.pcs).forEach(function (n) { if (m[1] && +m[1] !== +n) return; var ms = members(st, +n);
      o.push(('Po' + n + '      ').slice(0, 9) + (ms.length ? 'Active: ' + ms.map(function (k) { return 'gi1/' + k; }).join(',') : 'Inactive')); });
    return o.join('\n'); });
  cmd('priv', /^show spanning-tree$/, function (st) {
    return ['Spanning tree enabled mode ' + st.stp.mode.toUpperCase(), 'Default port cost method:  ' + st.stp.method, '',
      'Root ID    Priority    ' + Math.min(st.stp.prio, 32768) + (st.stp.prio < 32768 ? '\n           This switch is the root' : ''),
      'Bridge ID  Priority    ' + st.stp.prio, '           Hello Time ' + st.stp.hello + ' sec  Max Age ' + st.stp.maxage + ' sec  Forward Delay ' + st.stp.fwd + ' sec'].join('\n'); });
  cmd('priv', /^show running-config$/, function (st) {
    var o = ['spanning-tree mode ' + st.stp.mode];
    if (st.stp.prio !== 32768) o.push('spanning-tree priority ' + st.stp.prio);
    if (st.stp.method !== 'short') o.push('spanning-tree pathcost method long');
    if (st.lacpSys !== 1) o.push('lacp system-priority ' + st.lacpSys);
    if (st.vlans.length > 1) o.push('vlan database', ' vlan ' + st.vlans.filter(function (v) { return v > 1; }).join(','), 'exit');
    Object.keys(st.ports).forEach(function (k) { var p = st.ports[k], d = [];
      if (p.mode !== 'access') d.push(' switchport mode ' + p.mode); if (p.allowed.length) d.push(' switchport trunk allowed vlan add ' + p.allowed.join(','));
      if (p.cost) d.push(' spanning-tree cost ' + p.cost); if (p.portfast) d.push(' spanning-tree portfast'); if (p.bpduf) d.push(' spanning-tree bpdu filtering');
      if (p.group) d.push(' channel-group ' + p.group + ' mode ' + p.gmode); if (p.prio !== 32768) d.push(' lacp port-priority ' + p.prio);
      if (p.timeout !== 'long') d.push(' lacp timeout short');
      if (d.length) o = o.concat(['interface gigabitethernet1/' + k], d, ['exit']); });
    return o.join('\n'); });

  function exec(st, line) {
    var s = line.trim().replace(/\s+/g, ' ').replace(/^\S+?(\([^)]*\))?#\s*/, '');
    if (!s) return '';
    s = s.replace(/^int(?:erface)? /, 'interface ').replace(/^(interface|default interface) (gigabitethernet|gi|fastethernet|fa) ?/i, '$1 gi').replace(/^sh /, 'show ');
    if (/\?$/.test(s)) return 'См. шпаргалку команд; exit, end, do';
    var d = s.match(/^do (.+)$/);
    if (d) { var keep = st.mode, ctx = st.ctx; st.mode = 'priv'; var r0 = run1(st, d[1]); st.mode = keep; st.ctx = ctx; return r0 === null ? '% Unknown command' : r0; }
    var r = run1(st, s); if (r !== null) return r;
    for (var j = 0; j < CMDS.length; j++) if (s.match(CMDS[j].re)) return '% Команда недоступна в этом режиме';
    return '% Unrecognized command';
  }
  function run1(st, s) { for (var i = 0; i < CMDS.length; i++) { var c = CMDS[i], m = s.match(c.re); if (m && c.modes.indexOf(st.mode) >= 0) return c.run(st, m) || ''; } return null; }

  // таблица совместимости режимов (pptx): Auto/Active–Auto/Active, Auto–Passive — да; Passive–Passive — нет; On только с On
  function compat(a, b) { if (a === 'on' || b === 'on') return a === 'on' && b === 'on'; return !(a === 'passive' && b === 'passive'); }
  function pp(n) { return '0/' + n; }

  var TASKS = [
    { deck: 'stp', gen: function () { return { prio: pick([0, 4096, 8192]) }; },
      text: function (P) { return 'Включите на коммутаторе протокол <b>RSTP</b> и сделайте его корневым мостом: задайте приоритет <b>' + P.prio +
        '</b> (у соседей 32768).'; },
      sol: function (P) { return ['configure', 'spanning-tree mode rstp', 'spanning-tree priority ' + P.prio, 'end', 'show spanning-tree']; },
      checks: function (P) { return [['spanning-tree mode rstp', function (s) { return s.stp.mode === 'rstp'; }],
        ['приоритет ' + P.prio, function (s) { return s.stp.prio === P.prio; }]]; },
      send: function (P, s) { var root = s.stp.prio < 32768; return [{ ok: root && s.stp.mode === 'rstp', t: 'выборы корня: ' + (root ? 'этот коммутатор — корневой мост (приоритет ' + s.stp.prio + ' меньше 32768)' : 'приоритеты равны 32768 — корнем станет мост с наименьшим MAC') }]; } },
    { deck: 'stp', gen: function () { var a = rnd(1, 3), b = a + rnd(1, 2); return { a: a, b: b, up: rnd(b + 1, 8) }; },
      text: function (P) { return 'К портам <b>gigabitethernet 0/' + P.a + '</b> и <b>0/' + P.b + '</b> подключены ПК. Включите на них режим граничного порта '
        + '(<b>portfast</b>), чтобы ПК сразу переходили в Forwarding. Порт 0/' + P.up + ' — к коммутатору, его не трогайте.'; },
      sol: function (P) { return ['configure', 'interface gigabitethernet 0/' + P.a, 'spanning-tree portfast', 'exit', 'interface gigabitethernet 0/' + P.b,
        'spanning-tree portfast', 'end']; },
      checks: function (P) { return [['portfast на 0/' + P.a, function (s) { return s.ports[pp(P.a)].portfast; }], ['portfast на 0/' + P.b, function (s) { return s.ports[pp(P.b)].portfast; }],
        ['на 0/' + P.up + ' portfast нет', function (s) { return !s.ports[pp(P.up)].portfast; }]]; },
      send: function (P, s) { return [P.a, P.b].map(function (n) { var e = s.ports[pp(n)].portfast;
        return { ok: e, t: 'ПК на 0/' + n + ' включили: ' + (e ? 'порт edge — сразу Forwarding' : 'Listening → Learning → Forwarding, ждём 2 × ' + s.stp.fwd + ' с') }; }); } },
    { deck: 'stp', gen: function () { return { p: rnd(1, 8), c: pick([20000, 200000, 2000000]) }; },
      text: function (P) { return 'Переключите метод вычисления стоимости пути на <b>long</b> и административно задайте порту <b>gigabitethernet 0/' + P.p +
        '</b> стоимость <b>' + P.c + '</b>.'; },
      sol: function (P) { return ['configure', 'spanning-tree pathcost method long', 'interface gigabitethernet 0/' + P.p, 'spanning-tree cost ' + P.c, 'end']; },
      checks: function (P) { return [['pathcost method long', function (s) { return s.stp.method === 'long'; }], ['cost ' + P.c + ' на 0/' + P.p, function (s) { return s.ports[pp(P.p)].cost === P.c; }]]; } },
    { deck: 'stp', gen: function () { return { h: rnd(1, 4), m: pick([16, 20, 24]), f: pick([10, 12, 15, 20]) }; },
      text: function (P) { return 'Настройте таймеры STP: hello-time <b>' + P.h + '</b> с, max-age <b>' + P.m + '</b> с, forward-time <b>' + P.f + '</b> с.'; },
      sol: function (P) { return ['configure', 'spanning-tree hello-time ' + P.h, 'spanning-tree max-age ' + P.m, 'spanning-tree forward-time ' + P.f, 'end', 'show spanning-tree']; },
      checks: function (P) { return [['hello-time ' + P.h, function (s) { return s.stp.hello === P.h; }], ['max-age ' + P.m, function (s) { return s.stp.maxage === P.m; }],
        ['forward-time ' + P.f, function (s) { return s.stp.fwd === P.f; }]]; } },
    { deck: 'stp', gen: function () { var a = rnd(2, 20); return { a: a, b: a + rnd(5, 40), p: rnd(1, 8) }; },
      text: function (P) { return 'Включите <b>PVST+</b> для VLAN <b>' + P.a + '-' + P.b + '</b>: режим pvst, создайте VLAN в vlan database, порт <b>gigabitethernet 0/' + P.p +
        '</b> переведите в trunk и разрешите на нём эти VLAN.'; },
      sol: function (P) { var r = P.a + '-' + P.b; return ['configure', 'spanning-tree mode pvst', 'vlan database', 'vlan ' + r, 'exit', 'interface gigabitethernet 0/' + P.p,
        'switchport mode trunk', 'switchport trunk allowed vlan add ' + r, 'end']; },
      checks: function (P) { var l = list(P.a + '-' + P.b); return [['spanning-tree mode pvst', function (s) { return s.stp.mode === 'pvst'; }],
        ['VLAN ' + P.a + '-' + P.b + ' созданы', function (s) { return l.every(function (v) { return s.vlans.indexOf(v) >= 0; }); }],
        ['0/' + P.p + ' trunk, VLAN разрешены', function (s) { var x = s.ports[pp(P.p)]; return x.mode === 'trunk' && l.every(function (v) { return x.allowed.indexOf(v) >= 0; }); }]]; } },
    { deck: 'lacp', gen: function () { var a = rnd(1, 6); return { g: rnd(1, 8), a: a, b: a + 1 }; },
      text: function (P) { return 'Соберите <b>статический LAG</b> (группа <b>' + P.g + '</b>) из портов <b>gigabitethernet 0/' + P.a + '</b> и <b>0/' + P.b +
        '</b>. Перед этим сбросьте настройки портов командой default interface. На соседе — тоже статика (mode on).'; },
      sol: function (P) { return ['configure', 'default interface gigabitethernet 0/' + P.a, 'default interface gigabitethernet 0/' + P.b, 'interface gigabitethernet 0/' + P.a,
        'channel-group ' + P.g + ' mode on', 'exit', 'interface gigabitethernet 0/' + P.b, 'channel-group ' + P.g + ' mode on', 'end', 'show interfaces channel-group ' + P.g]; },
      checks: function (P) { return [P.a, P.b].map(function (n) { return ['0/' + n + ' в Po' + P.g + ' mode on', function (s) { var x = s.ports[pp(n)]; return x.group === P.g && x.gmode === 'on'; }]; }); },
      send: function (P, s) { return [P.a, P.b].map(function (n) { var x = s.ports[pp(n)], ok = x.group === P.g && compat(x.gmode, 'on');
        return { ok: ok, t: '0/' + n + ' ↔ сосед (on): ' + (ok ? 'в Po' + P.g + ', Active' : 'в агрегат не входит') }; }); } },
    { deck: 'lacp', gen: function () { var a = rnd(1, 6); return { g: rnd(1, 8), a: a, b: a + 1, nb: pick(['auto', 'passive']), sp: pick([1, 100, 4096]) }; },
      text: function (P) { return 'Соберите LAG с протоколом <b>LACP</b> (группа <b>' + P.g + '</b>) из портов <b>0/' + P.a + '</b> и <b>0/' + P.b + '</b> в <b>активном</b> режиме. '
        + 'Сосед настроен в режиме <b>' + P.nb + '</b>. Задайте приоритет системы LACP <b>' + P.sp + '</b>.'; },
      sol: function (P) { return ['configure', 'lacp system-priority ' + P.sp, 'interface gigabitethernet 0/' + P.a, 'channel-group ' + P.g + ' mode auto', 'exit',
        'interface gigabitethernet 0/' + P.b, 'channel-group ' + P.g + ' mode auto', 'end']; },
      checks: function (P) { return [P.a, P.b].map(function (n) { return ['0/' + n + ' в Po' + P.g + ' mode auto', function (s) { var x = s.ports[pp(n)]; return x.group === P.g && x.gmode === 'auto'; }]; })
        .concat([['lacp system-priority ' + P.sp, function (s) { return s.lacpSys === P.sp; }]]); },
      send: function (P, s) { return [P.a, P.b].map(function (n) { var x = s.ports[pp(n)], ok = x.group === P.g && compat(x.gmode, P.nb);
        return { ok: ok, t: '0/' + n + ' (' + (x.gmode || 'нет') + ') ↔ сосед (' + P.nb + '): ' + (ok ? 'LACP согласован, в Po' + P.g : 'агрегат не собрался') }; }); } },
    { deck: 'lacp', gen: function () { var a = rnd(1, 6); return { g: rnd(1, 8), a: a, b: a + 1 }; },
      text: function (P) { return 'Сосед уже настроен в режиме <b>auto</b> (активный). Добавьте порты <b>0/' + P.a + '</b> и <b>0/' + P.b + '</b> в группу <b>' + P.g +
        '</b> в <b>пассивном</b> режиме и включите на них отправку LACPDU с коротким интервалом (<b>timeout short</b>).'; },
      sol: function (P) { var o = ['configure']; [P.a, P.b].forEach(function (n) { o.push('interface gigabitethernet 0/' + n, 'channel-group ' + P.g + ' mode passive', 'lacp timeout short', 'exit'); });
        return o.concat(['end']); },
      checks: function (P) { return [P.a, P.b].map(function (n) { return ['0/' + n + ': passive, timeout short', function (s) { var x = s.ports[pp(n)];
        return x.group === P.g && x.gmode === 'passive' && x.timeout === 'short'; }]; }); },
      send: function (P, s) { return [P.a, P.b].map(function (n) { var x = s.ports[pp(n)], ok = x.group === P.g && compat(x.gmode, 'auto');
        return { ok: ok, t: '0/' + n + ' ↔ сосед (auto): ' + (ok ? 'в Po' + P.g + ', LACPDU каждую ' + (x.timeout === 'short' ? '1 с' : '30 с') : 'агрегат не собрался') }; }); } },
    { deck: 'lacp', gen: function () { return { p: rnd(1, 8), v: pick([100, 1000, 16384]) }; },
      text: function (P) { return 'Чтобы порт <b>gigabitethernet 0/' + P.p + '</b> гарантированно был активным в LAG, задайте ему приоритет LACP <b>' + P.v +
        '</b> (по умолчанию 32768, меньше — лучше).'; },
      sol: function (P) { return ['configure', 'interface gigabitethernet 0/' + P.p, 'lacp port-priority ' + P.v, 'end']; },
      checks: function (P) { return [['lacp port-priority ' + P.v + ' на 0/' + P.p, function (s) { return s.ports[pp(P.p)].prio === P.v; }]]; } }
  ];

  function init(box) {
    var pool = (box.dataset.pool || '').split(',').map(Number);
    var out = box.querySelector('.cs-out'), inp = box.querySelector('.cs-in input'), pr = box.querySelector('.cs-pr');
    var taskEl = box.querySelector('.cs-task'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol'), sendB = box.querySelector('[data-cs=send]');
    var st, T, P, hist = [], hi = 0, last = -1;
    function print(x, cls) { var d = document.createElement('div'); d.className = cls || ''; d.innerHTML = esc(x); out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function newTask() {
      var k; do { k = pool[rnd(0, pool.length - 1)]; } while (pool.length > 1 && k === last); last = k;
      T = TASKS[k]; P = T.gen(); st = fresh();
      taskEl.innerHTML = T.text(P); res.innerHTML = ''; sol.style.display = 'none'; sol.textContent = T.sol(P).join('\n');
      out.innerHTML = ''; print('*** Eltex MES2308P ***', 'cs-sys'); pr.textContent = prompt(st); sendB.style.display = T.send ? '' : 'none';
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var v = inp.value; print(prompt(st) + ' ' + v, 'cs-cmd'); if (v.trim()) hist.push(v); hi = hist.length;
        var r = exec(st, v); if (r) print(r, /^%(?!TRUNK)/.test(r) ? 'cs-err' : ''); inp.value = ''; pr.textContent = prompt(st); e.preventDefault(); }
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
      if (a === 'send' && T.send) res.innerHTML = '<div class="cs-send">' + T.send(P, st).map(function (x) { return '<div class="' + (x.ok ? 'ok' : 'no') + '"><span class="env">✉</span> ' + esc(x.t) + '</div>'; }).join('') + '</div>';
    });
    newTask();
  }
  window.MES_CLI = { TASKS: TASKS, fresh: fresh, exec: exec };
  document.querySelectorAll('.clisim[data-deck=mes]').forEach(init);
})();
