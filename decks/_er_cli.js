/* Симулятор CLI маршрутизатора Eltex ESR для деки «Маршрутизаторы ESR» (2.3 доп.).
   Команды и приглашения — как в pptx: esr-200# → configure → esr-200(config)# → interface … → (config-if-gi)# и т. д.
   Изменения копятся в кандидат-конфигурации; commit применяет, confirm подтверждает (имя меняется после commit).
   Задания случайные (кнопка «Обновить»), проверяется итоговое применённое и подтверждённое состояние. */
(function () {
  'use strict';
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }

  // ------------------------------------------------------------------ состояние
  function blank() {
    return { host: 'esr-200', ifs: {}, users: { admin: { pw: 'password', priv: 15 } }, ssh: false,
             banner: { login: null, exec: null }, tz: null, maxfail: [5, 300], lines: { console: {}, telnet: {}, ssh: {} } };
  }
  function fresh() {
    var c = blank();
    return { cand: c, run: clone(c), mode: 'priv', ctx: null, pending: false, confirmed: true, expired: false, date: null };
  }
  var PROMPT = { priv: '#', config: '(config)#', gi: '(config-if-gi)#', sub: '(config-if-sub)#', qinq: '(config-if-qinq)#',
                 lo: '(config-loopback)#', user: '(config-user)#', line: null, exp: '(change-expiredpassword)#' };
  function prompt(st) {
    if (st.mode === 'line') return st.run.host + '(config-line-' + st.ctx + ')#';
    return st.run.host + PROMPT[st.mode];
  }

  // ------------------------------------------------------------------ команды
  var CMDS = [];
  function cmd(modes, re, run) { CMDS.push({ modes: modes.split(' '), re: re, run: run }); }
  var IFM = 'gi sub qinq lo', CFG = 'config gi sub qinq lo user line';
  function ifKey(n) { return n.replace(/^(gigabitethernet|gi)\s*/i, 'gi'); }
  function ensureIf(st, k) { if (!st.cand.ifs[k]) st.cand.ifs[k] = { ip: null, fw: true, speed: null }; return st.cand.ifs[k]; }
  function cur(st) { return st.cand.ifs[st.ctx]; }

  cmd('exp', /^password (\S+)$/, function (st, m) {
    if (m[1].length < 8) return '% Пароль должен содержать не менее 8 символов';
    st.cand.users.admin.pw = m[1]; st.newpw = true; });
  cmd('exp', /^commit$/, function (st) {
    if (!st.newpw) return '% Сначала смените пароль командой password';
    st.run = clone(st.cand); st.pending = true; st.confirmed = false; st.mode = 'priv';
    return 'Configuration has been successfully applied and saved to flash. Commit timer started, 600 seconds.'; });
  cmd('exp', /^confirm$/, function () { return '% Сначала commit'; });
  cmd('exp', /^exit$/, function () { return '% Сессия остаётся открытой (тренажёр)'; });

  cmd('priv', /^configure( terminal)?$/, function (st) { st.mode = 'config'; });
  cmd('priv', /^commit$/, function (st) {
    if (JSON.stringify(st.cand) === JSON.stringify(st.run)) return 'Nothing to commit in configuration';
    st.run = clone(st.cand); st.pending = true; st.confirmed = false;
    return 'Configuration has been successfully applied and saved to flash. Commit timer started, 600 seconds.'; });
  cmd('priv', /^confirm$/, function (st) {
    if (!st.pending) return 'Nothing to confirm in configuration. You must commit some changes first.';
    st.pending = false; st.confirmed = true; return 'Configuration has been confirmed. Commit timer canceled.'; });
  cmd('priv', /^exit$/, function () { return '% Сессия остаётся открытой (тренажёр)'; });
  cmd(CFG, /^exit$/, function (st) {
    st.mode = (st.mode === 'config') ? 'priv' : (/^(sub|qinq)$/.test(st.mode) ? 'config' : 'config'); st.ctx = null; });
  cmd(CFG, /^end$/, function (st) { st.mode = 'priv'; st.ctx = null; });

  cmd('config', /^hostname (\S+)$/, function (st, m) { st.cand.host = m[1]; });
  cmd('config', /^interface (?:gigabitethernet|gi) ?1\/0\/([1-8])$/i, function (st, m) {
    st.ctx = 'gi1/0/' + m[1]; ensureIf(st, st.ctx); st.mode = 'gi'; });
  cmd('config', /^interface (?:gigabitethernet|gi) ?1\/0\/([1-8])\.(\d+)$/i, function (st, m) {
    if (+m[2] < 1 || +m[2] > 4094) return '% Неверный VLAN-тег';
    st.ctx = 'gi1/0/' + m[1] + '.' + m[2]; ensureIf(st, st.ctx); st.mode = 'sub'; });
  cmd('config', /^interface (?:gigabitethernet|gi) ?1\/0\/([1-8])\.(\d+)\.(\d+)$/i, function (st, m) {
    var sub = 'gi1/0/' + m[1] + '.' + m[2];
    if (!st.cand.ifs[sub]) return '% Сначала создайте sub-интерфейс ' + sub;
    st.ctx = sub + '.' + m[3]; ensureIf(st, st.ctx); st.mode = 'qinq'; });
  cmd('config', /^interface loopback ?(\d+)$/i, function (st, m) { st.ctx = 'lo' + m[1]; ensureIf(st, st.ctx); st.mode = 'lo'; });
  cmd(IFM, /^ip address (\d+\.\d+\.\d+\.\d+)\/(\d+)$/, function (st, m) {
    if (+m[2] > 32 || m[1].split('.').some(function (o) { return +o > 255; })) return '% Неверный адрес';
    cur(st).ip = m[1] + '/' + m[2]; });
  cmd(IFM, /^no ip address$/, function (st) { cur(st).ip = null; });
  cmd('gi sub qinq', /^ip firewall disable$/, function (st) { cur(st).fw = false; });
  cmd('gi sub qinq', /^no ip firewall disable$/, function (st) { cur(st).fw = true; });
  cmd('gi', /^speed (10M|100M|1000M|10G|25G|40G|100G|auto)( full-duplex| half-duplex)?$/i, function (st, m) {
    if (m[2] && /1000M|G/i.test(m[1])) return '% С 1000M работает только режим full-duplex';
    cur(st).speed = m[1] + (m[2] || ''); });
  cmd('config', /^ip ssh server$/, function (st) { st.cand.ssh = true; });
  cmd('config', /^no ip ssh server$/, function (st) { st.cand.ssh = false; });
  cmd('config', /^banner (login|exec) (.+)$/, function (st, m) { st.cand.banner[m[1]] = m[2]; });
  cmd('config', /^no banner (login|exec)$/, function (st, m) { st.cand.banner[m[1]] = null; });
  cmd('config', /^clock timezone gmt ([+-]\d{1,2})$/i, function (st, m) {
    if (Math.abs(+m[1]) > 12) return '% Допустимо gmt -12 … gmt +12'; st.cand.tz = +m[1]; });
  cmd('config', /^username (\S+)$/, function (st, m) {
    if (!st.cand.users[m[1]]) st.cand.users[m[1]] = { pw: null, priv: 1 }; st.ctx = m[1]; st.mode = 'user'; });
  cmd('config', /^no username (\S+)$/, function (st, m) {
    if (m[1] === 'admin') { st.cand.users.admin.pw = 'password'; return; }
    if (!st.cand.users[m[1]]) return '% Пользователь не найден'; delete st.cand.users[m[1]]; });
  cmd('user', /^password encrypted (\S+)$/, function (st, m) { st.cand.users[st.ctx].pw = 'enc:' + m[1]; });
  cmd('user', /^password (\S+)$/, function (st, m) { st.cand.users[st.ctx].pw = m[1]; });
  cmd('user', /^privilege (\d+)$/, function (st, m) {
    if (+m[1] < 1 || +m[1] > 15) return '% Уровень 1–15'; st.cand.users[st.ctx].priv = +m[1]; });
  cmd('config', /^aaa authentication attempts max-fail (\d+) (\d+)$/, function (st, m) { st.cand.maxfail = [+m[1], +m[2]]; });
  cmd('config', /^line (console|telnet|ssh)$/, function (st, m) { st.ctx = m[1]; st.mode = 'line'; });
  cmd('line', /^aaa disable$/, function (st) { st.cand.lines[st.ctx].disabled = true; });
  cmd('line', /^no aaa disable$/, function (st) { delete st.cand.lines[st.ctx].disabled; });

  var MON = 'January February March April May June July August September October November December'.split(' ');
  cmd('priv', /^set date (\d{1,2}):(\d{2}):(\d{2})(?: (\d{1,2}) (\w+)(?: (\d{4}))?)?$/, function (st, m) {
    if (+m[1] > 23 || +m[2] > 59 || +m[3] > 59) return '% Неверное время';
    if (m[5] && MON.indexOf(m[5][0].toUpperCase() + m[5].slice(1).toLowerCase()) < 0) return '% Неверный месяц';
    if (m[6] && (+m[6] < 2001 || +m[6] > 2037)) return '% Год 2001..2037';
    st.date = { t: m[1] + ':' + m[2] + ':' + m[3], d: m[4], mo: m[5], y: m[6] };
    return '%TIME-I-INFO: System time was changed by user admin'; });
  cmd('priv', /^show date$/, function (st) {
    var d = st.date || { t: '12:00:00', d: '09', mo: 'October', y: '2023' };
    var tz = st.run.tz === null ? 'UTC' : 'GMT' + (st.run.tz >= 0 ? '+' : '') + st.run.tz;
    return '"' + d.t + ' ' + tz + ' ' + (d.mo || 'October') + ' ' + (d.d || '09') + ' ' + (d.y || '2023') + '"'; });
  cmd('priv', /^show running-config$/, function (st) { return showRun(st.run); });
  cmd('priv', /^show candidate-config$/, function (st) { return showRun(st.cand); });
  cmd('priv', /^show interfaces status$/, function (st) {
    var o = ['Interface          Admin  Link   MTU    Mode', '                   State  State',
             '-----------------  -----  -----  -----  -----------'];
    var ks = ['gi1/0/1', 'gi1/0/2'].concat(Object.keys(st.run.ifs).filter(function (k) { return !/^gi1\/0\/[12]$/.test(k); }));
    ks.forEach(function (k) { o.push((k + '                  ').slice(0, 19) + 'Up     Up     1500   routerport'); });
    return o.join('\n'); });
  cmd('priv', /^show user accounts$/, function (st) {
    var o = ['Name                 Password             Privilege', '-------------------- -------------------- ---------'];
    Object.keys(st.run.users).forEach(function (u) {
      o.push((u + '                    ').slice(0, 21) + (st.run.users[u].pw ? '$6$' + hash(st.run.users[u].pw) : '').slice(0, 20) +
        '  ' + st.run.users[u].priv); });
    return o.join('\n'); });
  cmd('priv', /^show users blocked$/, function () { return 'Blocked users: нет'; });
  cmd('priv', /^clear users blocked( \S+)?$/, function () { return ''; });
  cmd('priv', /^show aaa authentication$/, function (st) {
    var o = ['Line       Login method list   Enable method list', '--------   -----------------   ------------------'];
    ['console', 'telnet', 'ssh'].forEach(function (l) {
      o.push((l + '         ').slice(0, 11) + (st.run.lines[l].disabled ? 'aaa disable        ' : 'default            ') + 'default'); });
    return o.join('\n'); });

  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return ('00000000' + (h >>> 0).toString(36)).slice(-8) + 'Qe' + s.length; }

  function showRun(c) {
    var o = ['hostname ' + c.host, ''];
    if (c.banner.login) o.push('banner login ' + c.banner.login);
    if (c.banner.exec) o.push('banner exec ' + c.banner.exec);
    if (c.tz !== null) o.push('clock timezone gmt ' + (c.tz >= 0 ? '+' : '') + c.tz);
    if (c.maxfail[0] !== 5 || c.maxfail[1] !== 300) o.push('aaa authentication attempts max-fail ' + c.maxfail.join(' '));
    Object.keys(c.users).forEach(function (u) {
      var x = c.users[u]; o.push('username ' + u);
      if (x.pw) o.push('  password encrypted $6$' + hash(x.pw)); if (x.priv !== 1) o.push('  privilege ' + x.priv); o.push('exit');
    });
    Object.keys(c.ifs).forEach(function (k) {
      var x = c.ifs[k], typ = /^lo/.test(k) ? 'loopback ' + k.slice(2) : 'gigabitethernet ' + k.slice(2);
      o.push('interface ' + typ);
      if (x.ip) o.push('  ip address ' + x.ip);
      if (!x.fw && !/^lo/.test(k)) o.push('  ip firewall disable');
      if (x.speed) o.push('  speed ' + x.speed);
      o.push('exit');
    });
    ['console', 'telnet', 'ssh'].forEach(function (l) { if (c.lines[l].disabled) o.push('line ' + l, '  aaa disable', 'exit'); });
    if (c.ssh) o.push('ip ssh server');
    return o.join('\n');
  }

  function exec(st, line) {
    var s = line.trim().replace(/\s+/g, ' ');
    s = s.replace(/^\S+?(\([^)]*\))?#\s*/, '');
    if (!s) return '';
    if (/\?$/.test(s)) return help(st);
    for (var i = 0; i < CMDS.length; i++) {
      var c = CMDS[i];
      var m = s.match(c.re);
      if (m && c.modes.indexOf(st.mode) >= 0) return c.run(st, m) || '';
    }
    for (var j = 0; j < CMDS.length; j++) if (s.match(CMDS[j].re)) return '% Команда недоступна в этом режиме';
    return '% Unknown command';
  }
  function help(st) {
    if (st.mode === 'exp') return 'commit    Apply current changes\nconfirm   Confirm changes\npassword  Change password\nexit      Exit';
    if (st.mode === 'priv') return 'commit  confirm  configure  set  show  clear  exit';
    return 'Доступно: команды режима ' + prompt(st) + ', exit, end';
  }

  // ------------------------------------------------------------------ задания (только по материалу pptx)
  var NAMES = ['R1', 'R2', 'Office-R1', 'Core-ESR', 'Branch-R3', 'ESR-Lab'];
  var USERS = ['user1', 'master', 'student', 'netadmin', 'operator'];
  function ip24() { return '192.168.' + rnd(10, 99) + '.' + rnd(1, 254); }
  function applied(st) { return st.confirmed && !st.pending && JSON.stringify(st.cand) === JSON.stringify(st.run); }
  var A = ['Изменения применены (commit) и подтверждены (confirm)', applied];

  var TASKS = [
    { // 0 первое включение
      gen: function () { return { pw: pick(['eltex2024', 'Rout3rPass', 'secure-esr', 'labpass12']) }; },
      setup: function (P, st) { st.mode = 'exp'; },
      text: function (P) { return 'Первое включение ESR. Смените заводской пароль admin на <b>' + P.pw + '</b> (не менее 8 символов), примените и подтвердите.'; },
      sol: function (P) { return ['password ' + P.pw, 'commit', 'confirm']; },
      checks: function (P) { return [['Пароль admin = ' + P.pw, function (s) { return s.run.users.admin.pw === P.pw; }], A]; }
    },
    { // 1 имя
      gen: function () { return { h: pick(NAMES) }; },
      text: function (P) { return 'Задайте маршрутизатору имя <b>' + P.h + '</b>. Помните: имя сменится только после commit.'; },
      sol: function (P) { return ['configure', 'hostname ' + P.h, 'exit', 'commit', 'confirm']; },
      checks: function (P) { return [['Имя устройства ' + P.h, function (s) { return s.run.host === P.h; }], A]; }
    },
    { // 2 физический интерфейс
      gen: function () { return { n: rnd(1, 3), ip: ip24() }; },
      text: function (P) { return 'Назначьте интерфейсу <b>gi1/0/' + P.n + '</b> адрес <b>' + P.ip + '/24</b>, отключите на нём межсетевой экран, примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'interface gigabitethernet 1/0/' + P.n, 'ip address ' + P.ip + '/24', 'ip firewall disable', 'end', 'commit', 'confirm']; },
      checks: function (P) { var k = 'gi1/0/' + P.n; return [
        ['IP ' + P.ip + '/24 на ' + k, function (s) { return s.run.ifs[k] && s.run.ifs[k].ip === P.ip + '/24'; }],
        ['Межсетевой экран на ' + k + ' отключён', function (s) { return s.run.ifs[k] && !s.run.ifs[k].fw; }], A]; },
      send: function (P, st) { var x = st.run.ifs['gi1/0/' + P.n], ok = x && x.ip === P.ip + '/24' && !x.fw && applied(st);
        return [{ ok: ok, t: 'ping ' + P.ip + ' с узла в той же сети: ' + (ok ? 'эхо-ответ получен' : (x && x.fw ? 'нет ответа — межсетевой экран блокирует трафик' : 'нет ответа')) }]; }
    },
    { // 3 loopback
      gen: function () { return { n: rnd(1, 8), ip: '10.' + rnd(0, 99) + '.' + rnd(0, 99) + '.1' }; },
      text: function (P) { return 'Создайте интерфейс <b>loopback' + P.n + '</b> с адресом <b>' + P.ip + '/24</b>, примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'interface loopback' + P.n, 'ip address ' + P.ip + '/24', 'end', 'commit', 'confirm']; },
      checks: function (P) { return [['loopback' + P.n + ' ' + P.ip + '/24', function (s) { var x = s.run.ifs['lo' + P.n]; return x && x.ip === P.ip + '/24'; }], A]; }
    },
    { // 4 sub + qinq
      gen: function () { return { n: rnd(1, 3), o: rnd(10, 90), i: rnd(100, 900) }; },
      text: function (P) { return 'Создайте на gi1/0/' + P.n + ' QinQ-интерфейс с внешним тегом <b>' + P.o + '</b> и внутренним <b>' + P.i + '</b>. QinQ сразу создать нельзя — сначала sub-интерфейс. Примените и подтвердите.'; },
      sol: function (P) { var b = 'gigabitethernet 1/0/' + P.n + '.' + P.o; return ['configure', 'interface ' + b, 'exit', 'interface ' + b + '.' + P.i, 'end', 'commit', 'confirm']; },
      checks: function (P) { var b = 'gi1/0/' + P.n + '.' + P.o; return [
        ['Sub-интерфейс ' + b, function (s) { return !!s.run.ifs[b]; }],
        ['QinQ-интерфейс ' + b + '.' + P.i, function (s) { return !!s.run.ifs[b + '.' + P.i]; }], A]; }
    },
    { // 5 пользователь
      gen: function () { return { u: pick(USERS), pw: pick(['eltex', 'support', 'labpass']), l: rnd(1, 15) }; },
      text: function (P) { return 'Создайте локального пользователя <b>' + P.u + '</b> с паролем <b>' + P.pw + '</b> и уровнем привилегий <b>' + P.l + '</b>. Примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'username ' + P.u, 'password ' + P.pw, 'privilege ' + P.l, 'exit', 'exit', 'commit', 'confirm']; },
      checks: function (P) { return [['Пользователь ' + P.u, function (s) { return !!s.run.users[P.u]; }],
        ['Пароль ' + P.pw, function (s) { return s.run.users[P.u] && s.run.users[P.u].pw === P.pw; }],
        ['privilege ' + P.l, function (s) { return s.run.users[P.u] && s.run.users[P.u].priv === P.l; }], A]; }
    },
    { // 6 баннеры
      gen: function () { var h = pick(['esr-200', 'R1', 'Lab']); return { l: 'Router-' + h, e: 'Connect_Router_' + h.replace(/-/g, '_') }; },
      login: true,
      text: function (P) { return 'Настройте баннеры: перед авторизацией — <b>' + P.l + '</b>, после авторизации — <b>' + P.e + '</b> (без пробелов). Примените, подтвердите и проверьте кнопкой «Подключиться заново».'; },
      sol: function (P) { return ['configure', 'banner login ' + P.l, 'banner exec ' + P.e, 'exit', 'commit', 'confirm']; },
      checks: function (P) { return [['banner login ' + P.l, function (s) { return s.run.banner.login === P.l; }],
        ['banner exec ' + P.e, function (s) { return s.run.banner.exec === P.e; }], A]; }
    },
    { // 7 часовой пояс
      gen: function () { return { z: rnd(-12, 12) }; },
      text: function (P) { return 'Установите часовой пояс <b>gmt ' + (P.z >= 0 ? '+' : '') + P.z + '</b>, примените и подтвердите, затем выведите время командой show date.'; },
      sol: function (P) { return ['configure', 'clock timezone gmt ' + (P.z >= 0 ? '+' : '') + P.z, 'exit', 'commit', 'confirm', 'show date']; },
      checks: function (P) { return [['Часовой пояс gmt ' + (P.z >= 0 ? '+' : '') + P.z, function (s) { return s.run.tz === P.z; }], A]; }
    },
    { // 8 ssh + запрет консоли
      gen: function () { return { l: pick(['console', 'telnet']) }; },
      text: function (P) { return 'Включите ssh-сервер и запретите доступ через линию <b>' + P.l + '</b> командой aaa disable. Примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'ip ssh server', 'line ' + P.l, 'aaa disable', 'exit', 'exit', 'commit', 'confirm']; },
      checks: function (P) { return [['ip ssh server', function (s) { return s.run.ssh; }],
        ['line ' + P.l + ': aaa disable', function (s) { return !!s.run.lines[P.l].disabled; }], A]; }
    },
    { // 9 блокировка
      gen: function () { return { n: rnd(3, 10), t: pick([60, 120, 600, 900]) }; },
      text: function (P) { return 'Измените блокировку: после <b>' + P.n + '</b> неверных вводов пароля пользователь блокируется на <b>' + P.t + '</b> секунд. Примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'aaa authentication attempts max-fail ' + P.n + ' ' + P.t, 'exit', 'commit', 'confirm']; },
      checks: function (P) { return [['max-fail ' + P.n + ' ' + P.t, function (s) { return s.run.maxfail[0] === P.n && s.run.maxfail[1] === P.t; }], A]; }
    }
  ];

  function loginView(s) {
    var o = ['user@user-System-Product-Name:~$ ssh admin@172.16.100.12'];
    if (s.run.banner.login) o.push(s.run.banner.login);
    o.push('(admin@172.16.100.12) Password:');
    if (s.run.banner.exec) o.push(s.run.banner.exec);
    o.push(s.run.host + '#');
    return o.join('\n');
  }

  // ------------------------------------------------------------------ виджет
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function init(box) {
    var pool = (box.dataset.pool || '').split(',').map(Number);
    var out = box.querySelector('.cs-out'), inp = box.querySelector('.cs-in input'), pr = box.querySelector('.cs-pr');
    var taskEl = box.querySelector('.cs-task'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol');
    var sendB = box.querySelector('[data-cs=send]');
    var st, T, P, hist = [], hi = 0, last = -1;
    function print(t, cls) { var d = document.createElement('div'); d.className = cls || ''; d.innerHTML = esc(t); out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function newTask() {
      var k; do { k = pool[rnd(0, pool.length - 1)]; } while (pool.length > 1 && k === last); last = k;
      T = TASKS[k]; P = T.gen(); st = fresh(); if (T.setup) T.setup(P, st);
      taskEl.innerHTML = T.text(P); res.innerHTML = ''; sol.style.display = 'none';
      sol.textContent = T.sol(P).join('\n');
      out.innerHTML = '';
      print(st.mode === 'exp' ? 'esr-200 login: admin\nPassword:\n% Пароль по умолчанию устарел — смените его' : '*** Welcome to ESR ***', 'cs-sys');
      pr.textContent = prompt(st);
      sendB.style.display = (T.send || T.login) ? '' : 'none';
      sendB.textContent = T.login ? 'Подключиться заново' : 'Отправить ping';
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        var v = inp.value; print(prompt(st) + ' ' + v, 'cs-cmd'); hist.push(v); hi = hist.length;
        var r = exec(st, v); if (r) print(r, /^%/.test(r) ? 'cs-err' : ''); inp.value = ''; pr.textContent = prompt(st);
        e.preventDefault();
      } else if (e.key === 'ArrowUp') { if (hi > 0) { hi--; inp.value = hist[hi]; } e.preventDefault(); }
      else if (e.key === 'ArrowDown') { if (hi < hist.length) { hi++; inp.value = hist[hi] || ''; } e.preventDefault(); }
      e.stopPropagation();
    });
    out.addEventListener('click', function () { inp.focus(); });
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cs]'); if (!b) return;
      var a = b.dataset.cs;
      if (a === 'new') newTask();
      if (a === 'sol') sol.style.display = sol.style.display === 'none' ? 'block' : 'none';
      if (a === 'check') {
        var cs = T.checks(P), ok = 0;
        res.innerHTML = cs.map(function (c) { var y = !!c[1](st); if (y) ok++; return '<div class="' + (y ? 'ok' : 'no') + '">' + (y ? '✓ ' : '✗ ') + c[0] + '</div>'; }).join('') +
          '<div class="cs-sum ' + (ok === cs.length ? 'ok' : 'no') + '">' + (ok === cs.length ? 'Задание выполнено' : 'Выполнено ' + ok + ' из ' + cs.length) + '</div>';
      }
      if (a === 'send') {
        if (T.login) { print('--- новое подключение по ssh ---', 'cs-sys'); print(loginView(st)); return; }
        var r = T.send(P, st);
        res.innerHTML = '<div class="cs-send">' + r.map(function (x) {
          return '<div class="' + (x.ok ? 'ok' : 'no') + '"><span class="env">✉</span> ' + esc(x.t) + '</div>'; }).join('') + '</div>';
      }
    });
    newTask();
  }
  window.ER_CLI = { TASKS: TASKS, fresh: fresh, exec: exec, prompt: prompt };
  document.querySelectorAll('.clisim[data-deck=esr]').forEach(init);
})();
