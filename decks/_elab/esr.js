/* CLI маршрутизатора ESR (vESR). Синтаксис — по лабораторным NTF2v2 и справочнику ESR-Series CLI:
   правки копятся в кандидате и вступают в силу только после commit (+ confirm). */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip;
  var T = [];
  function cmd(modes, pat, run, d) { T.push({ modes: modes.split(' '), pat: pat.split(' '), run: run, d: d }); }
  var CFG = 'config gi sub lo user bridge';
  var IFM = 'gi sub lo bridge';
  var PROMPT = { priv: '#', config: '(config)#', gi: '(config-if-gi)#', sub: '(config-if-sub)#', lo: '(config-if-loopback)#',
                 user: '(config-user)#', bridge: '(config-bridge)#' };

  function freshCfg(host, nports) {
    var ifs = {};
    for (var i = 1; i <= nports; i++) ifs['gi1/0/' + i] = { ip: null, fw: true, shut: false };
    return { host: host, ifs: ifs, users: { admin: { pw: 'password', priv: 15 } }, ssh: false, banner: { login: null, exec: null },
             routes: [], tz: null, bridges: {} };
  }
  function fresh(host, nports) {
    var c = freshCfg(host || 'esr', nports || 8);
    return { kind: 'esr', mode: 'priv', ctx: null, cand: c, run: EL.clone(c), pending: false, date: null, nports: nports || 8 };
  }
  function prompt(st) { return st.run.host + PROMPT[st.mode]; }

  // имена интерфейсов: gi1/0/1, gi1/0/1.10, lo1
  function ifName(t) {
    var m = String(t).match(/^gi(\d+)\/(\d+)\/(\d+)(?:\.(\d+))?$/);
    if (!m || m[1] !== '1' || m[2] !== '0') return null;
    return { phys: 'gi1/0/' + m[3], sub: m[4] ? +m[4] : null, name: 'gi1/0/' + m[3] + (m[4] ? '.' + m[4] : '') };
  }
  function cur(st) { return st.ctx && st.cand.ifs[st.ctx]; }
  function touch(st) { st.pending = true; }

  // ---------------------------------------------------------------- режимы
  cmd('priv', 'configure', function (st) { st.mode = 'config'; }, 'Режим глобальной конфигурации');
  cmd('priv', 'configure terminal', function (st) { st.mode = 'config'; });
  cmd(CFG, 'exit', function (st) { st.mode = st.mode === 'config' ? 'priv' : 'config'; st.ctx = null; }, 'Выход на уровень выше');
  cmd(CFG, 'end', function (st) { st.mode = 'priv'; st.ctx = null; }, 'Выход в привилегированный режим');

  // ---------------------------------------------------------------- commit / confirm
  function commit(st) {
    if (!st.pending) return 'Nothing to commit';
    st.run = EL.clone(st.cand); st.pending = false; st.unconfirmed = true;
    return 'Configuration has been successfully applied and saved to flash. Commit timer started, changes will be reverted in 600 seconds.';
  }
  function confirm(st) {
    if (!st.unconfirmed) return '% Нет изменений, ожидающих подтверждения';
    st.unconfirmed = false; return 'Configuration has been confirmed. Commit timer canceled.';
  }
  cmd('priv', 'commit', commit, 'Применить изменения кандидата');
  cmd('priv', 'confirm', confirm, 'Подтвердить применённую конфигурацию');
  cmd('priv', 'rollback', function (st) { st.cand = EL.clone(st.run); st.pending = false; return 'Configuration has been successfully rolled back'; },
      'Откатить неприменённые изменения');

  // ---------------------------------------------------------------- базовая настройка
  cmd('config', 'hostname <w>', function (st, a) { st.cand.host = a[0]; touch(st); }, 'Имя устройства');
  cmd('config', 'clock timezone gmt <w>', function (st, a) {
    if (!/^[+-]?\d{1,2}$/.test(a[0])) return '% Неверный часовой пояс (пример: +7)';
    st.cand.tz = (/^[+-]/.test(a[0]) ? '' : '+') + a[0]; touch(st); }, 'Часовой пояс');
  cmd('priv', 'set date <w> <n> <w> <n>', function (st, a) {
    if (!/^\d{1,2}:\d{2}:\d{2}$/.test(a[0])) return '% Формат: set date ЧЧ:ММ:СС ДД Месяц ГГГГ';
    st.date = a[0] + ' ' + a[1] + ' ' + a[2] + ' ' + a[3]; }, 'Установить дату и время');
  cmd('priv', 'show date', function (st) {
    var M = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
    if (!st.date) return '"2026-01-01 00:00:00"';
    var p = st.date.split(' '), mi = 0;
    M.forEach(function (m, i) { if (m.indexOf(p[2].toLowerCase()) === 0) mi = i; });
    return '"' + p[3] + '-' + ('0' + (mi + 1)).slice(-2) + '-' + ('0' + p[1]).slice(-2) + ' ' + p[0] + '"'; }, 'Текущие дата и время');
  cmd('config', 'username <w>', function (st, a) {
    if (!st.cand.users[a[0]]) st.cand.users[a[0]] = { pw: null, priv: 1 };
    st.mode = 'user'; st.ctx = a[0]; touch(st); }, 'Локальный пользователь');
  cmd('config', 'no username <w>', function (st, a) { if (!st.cand.users[a[0]]) return '% Пользователь не найден';
    delete st.cand.users[a[0]]; touch(st); });
  cmd('user', 'password <w>', function (st, a) { st.cand.users[st.ctx].pw = a[0]; touch(st); }, 'Пароль пользователя');
  cmd('user', 'privilege <n>', function (st, a) { if (a[0] < 1 || a[0] > 15) return '% Уровень привилегий 1–15';
    st.cand.users[st.ctx].priv = a[0]; touch(st); }, 'Уровень привилегий');
  cmd('config', 'ip ssh server', function (st) { st.cand.ssh = true; touch(st); }, 'Включить SSH-сервер');
  cmd('config', 'no ip ssh server', function (st) { st.cand.ssh = false; touch(st); });
  function banner(kind) { return function (st, a) { st.cand.banner[kind] = a[0].replace(/^["«](.*)["»]$/, '$1'); touch(st); }; }
  cmd('config', 'banner login <rest>', banner('login'), 'Баннер до авторизации');
  cmd('config', 'banner exec <rest>', banner('exec'), 'Баннер после авторизации');
  cmd('config', 'no banner login', function (st) { st.cand.banner.login = null; touch(st); });
  cmd('config', 'no banner exec', function (st) { st.cand.banner.exec = null; touch(st); });

  // ---------------------------------------------------------------- интерфейсы
  cmd('config', 'interface <w>', function (st, a) {
    var n = ifName(a[0]); if (!n) return '% Неверное имя интерфейса (пример: gigabitethernet 1/0/1 или 1/0/1.10)';
    if (!st.cand.ifs[n.phys]) return '% Interface ' + n.phys + ' not found';
    if (n.sub !== null) {
      if (n.sub < 1 || n.sub > 4094) return '% Номер саб-интерфейса = VLAN, 1–4094';
      if (!st.cand.ifs[n.name]) { st.cand.ifs[n.name] = { ip: null, fw: true, shut: false }; touch(st); }
      st.mode = 'sub';
    } else st.mode = 'gi';
    st.ctx = n.name; }, 'Настройка интерфейса');
  cmd('config', 'interface loopback <n>', function (st, a) {
    if (a[0] < 1 || a[0] > 8) return '% Loopback 1–8';
    var k = 'lo' + a[0]; if (!st.cand.ifs[k]) { st.cand.ifs[k] = { ip: null, fw: false, shut: false }; touch(st); }
    st.mode = 'lo'; st.ctx = k; }, 'Loopback-интерфейс');
  cmd('config', 'no interface <w>', function (st, a) {
    var n = ifName(a[0]); if (!n || n.sub === null || !st.cand.ifs[n.name]) return '% Удалить можно только саб-интерфейс';
    delete st.cand.ifs[n.name]; touch(st); });
  cmd('config', 'no interface loopback <n>', function (st, a) { delete st.cand.ifs['lo' + a[0]]; touch(st); });
  function setIp(st, v) {
    var c = IP.parseCidr(v); if (!c) return '% Формат адреса: A.B.C.D/длина, например 192.168.1.1/24';
    var me = st.ctx;
    var clash = Object.keys(st.cand.ifs).filter(function (k) { var x = st.cand.ifs[k]; return k !== me && x.ip &&
      IP.sameNet(x.ip.split('/')[0], c.ip, Math.min(+x.ip.split('/')[1], c.len)) && x.ip.split('/')[1] !== '32' && c.len !== 32; });
    if (clash.length) return '% Адрес пересекается с подсетью интерфейса ' + clash[0];
    cur(st).ip = c.ip + '/' + c.len; touch(st);
  }
  cmd('gi sub lo', 'ip address <w>', function (st, a) { return setIp(st, a[0]); }, 'IP-адрес/префикс');
  cmd('gi sub lo', 'no ip address', function (st) { cur(st).ip = null; touch(st); });
  cmd('gi sub', 'ip firewall disable', function (st) { cur(st).fw = false; touch(st); }, 'Отключить межсетевой экран');
  cmd('gi sub', 'no ip firewall disable', function (st) { cur(st).fw = true; touch(st); });
  cmd('gi sub lo', 'shutdown', function (st) { cur(st).shut = true; touch(st); }, 'Выключить интерфейс');
  cmd('gi sub lo', 'no shutdown', function (st) { cur(st).shut = false; touch(st); }, 'Включить интерфейс');
  cmd('gi sub lo', 'description <rest>', function (st, a) { cur(st).desc = a[0]; touch(st); }, 'Описание');

  // ---------------------------------------------------------------- статические маршруты
  cmd('config', 'ip route <w> <ip>', function (st, a) {
    var c = IP.parseCidr(a[0]); if (!c) return '% Формат: ip route A.B.C.D/длина шлюз';
    var net = IP.netOf(c.ip, c.len);
    if (!st.cand.routes.some(function (r) { return r.net === net && r.nh === a[1]; })) st.cand.routes.push({ net: net, nh: a[1] });
    touch(st); }, 'Статический маршрут');
  cmd('config', 'no ip route <w> <ip>', function (st, a) {
    var c = IP.parseCidr(a[0]); if (!c) return '% Формат: no ip route A.B.C.D/длина шлюз';
    var net = IP.netOf(c.ip, c.len), n = st.cand.routes.length;
    st.cand.routes = st.cand.routes.filter(function (r) { return !(r.net === net && r.nh === a[1]); });
    if (n === st.cand.routes.length) return '% Маршрут не найден'; touch(st); });

  // ---------------------------------------------------------------- show
  function ifSort(a, b) { var f = function (k) { return k.charAt(0) === 'l' ? 1e6 + +k.slice(2) : +k.split('/')[2].split('.')[0] * 1e4 + (+k.split('.')[1] || 0); };
    return f(a) - f(b); }
  function longIf(k) { return k.charAt(0) === 'l' ? 'loopback ' + k.slice(2) : 'gigabitethernet ' + k.slice(2); }
  function showRun(st) {
    var c = st.run, o = ['#!/usr/bin/clish', '#18', 'hostname ' + c.host, ''];
    Object.keys(c.users).forEach(function (u) { var x = c.users[u];
      o.push('username ' + u, '  password encrypted ' + E().hash(x.pw || '').slice(0, 30), '  privilege ' + x.priv, 'exit'); });
    o.push('');
    if (c.tz) o.push('clock timezone gmt ' + c.tz, '');
    if (c.banner.login) o.push('banner login "' + c.banner.login + '"');
    if (c.banner.exec) o.push('banner exec "' + c.banner.exec + '"');
    Object.keys(c.ifs).sort(ifSort).forEach(function (k) {
      var x = c.ifs[k], d = [];
      if (x.desc) d.push('  description "' + x.desc + '"');
      if (x.shut) d.push('  shutdown');
      if (!x.fw && k.charAt(0) !== 'l') d.push('  ip firewall disable');
      if (x.ip) d.push('  ip address ' + x.ip);
      if (d.length || k.indexOf('.') > 0 || k.charAt(0) === 'l') o.push('interface ' + longIf(k), d.join('\n'), 'exit');
    });
    c.routes.forEach(function (r) { o.push('ip route ' + r.net + ' ' + r.nh); });
    if (c.ssh) o.push('ip ssh server');
    return o.filter(function (x) { return x !== ''; }).join('\n').replace(/\nexit\n/g, '\nexit\n');
  }
  cmd('priv', 'show running-config', showRun, 'Применённая конфигурация');
  cmd('priv', 'show candidate-config', function (st) { var r = st.run; st.run = st.cand; var o = showRun(st); st.run = r; return o; },
      'Конфигурация-кандидат (до commit)');
  cmd('priv', 'show ip interfaces', function (st) {
    var o = ['IP address                Interface              Type', '------------------------- ---------------------- -------'];
    Object.keys(st.run.ifs).sort(ifSort).forEach(function (k) { var x = st.run.ifs[k]; if (!x.ip) return;
      o.push((x.ip + '                          ').slice(0, 26) + (k + '                       ').slice(0, 23) + 'static'); });
    return o.join('\n'); }, 'IP-адреса интерфейсов');
  cmd('priv', 'show interfaces status', function (st) {
    var o = ['Interface    Admin   Link    MTU    MAC address         Last change', '------------ ------- ------- ------ ------------------- ----------'];
    Object.keys(st.run.ifs).sort(ifSort).forEach(function (k) { var x = st.run.ifs[k];
      var up = !x.shut && (k.charAt(0) === 'l' || (st.net && st.net.linked(st.dev, k.split('.')[0])));
      o.push((k + '             ').slice(0, 13) + (x.shut ? 'Down    ' : 'Up      ') + (up ? 'Up      ' : 'Down    ') + '1500   ' +
             EL.mac(st.run.host + k.split('.')[0]) + '   00,00:00:00'); });
    return o.join('\n'); }, 'Состояние интерфейсов');
  cmd('priv', 'show ip route', function (st) {
    var o = ['Codes: C - connected, S - static, R - RIP derived, O - OSPF derived,', '       > - best route', ''];
    Object.keys(st.run.ifs).sort(ifSort).forEach(function (k) { var x = st.run.ifs[k]; if (!x.ip || x.shut) return;
      var p = x.ip.split('/'); o.push('C     ' + IP.netOf(p[0], +p[1]) + '  [0/0] dev ' + k + ', ' + p[0] + ' > '); });
    st.run.routes.forEach(function (r) { o.push('S     ' + r.net + '  [1/0] via ' + r.nh + ' > '); });
    return o.join('\n'); }, 'Таблица маршрутизации');
  cmd('priv', 'show users', function (st) { return 'User      Privilege\n--------- ---------\n' +
    Object.keys(st.run.users).map(function (u) { return (u + '          ').slice(0, 10) + st.run.users[u].priv; }).join('\n'); });
  cmd('priv', 'ping <ip>', function (st, a) { return st.net ? st.net.pingText(st.dev, a[0], 'esr') : '% Нет сети'; }, 'Проверка связности');
  cmd('priv', 'traceroute <ip>', function (st, a) { return st.net ? st.net.traceText(st.dev, a[0]) : '% Нет сети'; }, 'Трассировка маршрута');

  function E() { return EL.E; }

  // do <команда> из любого режима конфигурации
  function exec(st, raw) {
    var line = String(raw).trim();
    var m = line.match(/^do\s+(.+)$/i);
    if (m && st.mode !== 'priv') { var md = st.mode; st.mode = 'priv'; var r = EL.cli.runTable(T, st, m[1]); if (st.mode === 'priv') st.mode = md; return r; }
    return EL.cli.runTable(T, st, line);
  }
  function helpTable(st, raw) {
    var m = String(raw).match(/^\s*do\s+(.*)$/i);
    return m && st.mode !== 'priv' ? { mode: 'priv', raw: m[1] } : { mode: st.mode, raw: raw };
  }
  EL.esr = { T: T, fresh: fresh, prompt: prompt, exec: exec, showRun: showRun, ifName: ifName, helpTable: helpTable,
             PROMPT: PROMPT, commit: commit, confirm: confirm };
})(typeof window !== 'undefined' ? window : global);
