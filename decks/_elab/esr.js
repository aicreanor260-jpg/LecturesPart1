/* CLI маршрутизатора ESR (vESR). Синтаксис — по лабораторным NTF2v2 и справочнику ESR-Series CLI:
   правки копятся в кандидате и вступают в силу только после commit (+ confirm). */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip;
  var T = [], RUNX = [];
  function cmd(modes, pat, run, d) { T.push({ modes: modes.split(' '), pat: pat.split(' '), run: run, d: d }); }
  var CFG = 'config gi sub lo user bridge rip ospf ospfa';
  var IFM = 'gi sub lo bridge';
  var PROMPT = { priv: '#', config: '(config)#', gi: '(config-if-gi)#', sub: '(config-if-sub)#', lo: '(config-if-loopback)#',
                 user: '(config-user)#', bridge: '(config-bridge)#',
                 rip: '(config-rip)#', ospf: '(config-ospf)#', ospfa: '(config-ospf-area)#' };

  function freshCfg(host, nports, list) {
    var ifs = {};
    (list || []).forEach(function (k) { ifs[k] = { ip: null, fw: true, shut: false }; });
    if (!list) for (var i = 1; i <= nports; i++) ifs['gi1/0/' + i] = { ip: null, fw: true, shut: false };
    return { host: host, ifs: ifs, users: { admin: { pw: 'password', priv: 15 } }, ssh: false, banner: { login: null, exec: null },
             routes: [], tz: null, bridges: {}, rip: null, ospf: null };
  }
  function fresh(host, nports, list) {
    var c = freshCfg(host || 'esr', nports || 8, list);
    return { kind: 'esr', mode: 'priv', ctx: null, cand: c, run: EL.clone(c), pending: false, date: null, nports: nports || 8 };
  }
  // приглашение порта по типу: (config-if-gi)#, (config-if-te)#, (config-if-twe)#, (config-if-fo)# …
  function prompt(st) { var c = Array.isArray(st.ctx) ? st.ctx[0] : st.ctx, t = st.mode === 'gi' && c ? String(c).match(/^[a-z]+/)[0] : null;
    return st.run.host + (t && t !== 'gi' ? '(config-if-' + t + ')#' : PROMPT[st.mode]); }

  // имена интерфейсов: gi1/0/1, gi1/0/1.10, lo1
  // типы портов ESR: gi — gigabitethernet, te — tengigabitethernet, twe — twentyfivegigabitethernet,
  // fo — fourtygigabitethernet (так пишется в CLI ESR), hu — hundredgigabitethernet; диапазоны и списки: gi1/0/1-3,te1/0/1
  var IFT = { gi: 'gigabitethernet', te: 'tengigabitethernet', twe: 'twentyfivegigabitethernet', fo: 'fourtygigabitethernet', hu: 'hundredgigabitethernet' };
  function ifName(t) {
    var parts = String(t).split(','), L = [];
    for (var j = 0; j < parts.length; j++) {
      var r = parts[j].match(/^(gi|te|twe|fo|hu)1\/0\/(\d+)-(?:(?:gi|te|twe|fo|hu)1\/0\/)?(\d+)$/);
      if (r) { if (+r[3] < +r[2]) return null; for (var i = +r[2]; i <= +r[3]; i++) L.push(r[1] + '1/0/' + i); continue; }
      if (parts.length > 1) { var one = parts[j].match(/^(gi|te|twe|fo|hu)1\/0\/(\d+)$/); if (!one) return null; L.push(one[0]); continue; }
      var m = parts[j].match(/^(gi|te|twe|fo|hu)(\d+)\/(\d+)\/(\d+)(?:\.(\d+))?$/);
      if (!m || m[2] !== '1' || m[3] !== '0') return null;
      var ph = m[1] + '1/0/' + m[4];
      return { phys: ph, sub: m[5] ? +m[5] : null, name: ph + (m[5] ? '.' + m[5] : '') };
    }
    return L.length ? { range: L } : null;
  }
  // полные имена ESR, которых нет в общем нормализаторе MES
  function normEsr(line) {
    return line.replace(/\b(?:twentyfive\w*|twe)\s*(?=\d+\/\d+\/\d+)/ig, 'twe').replace(/\bfourty\w*\s*(?=\d+\/\d+\/\d+)/ig, 'fo')
               .replace(/\b(?:hundred\w*)\s*(?=\d+\/\d+\/\d+)/ig, 'hu');
  }
  function ctxList(st) { return Array.isArray(st.ctx) ? st.ctx : [st.ctx]; }
  function cur(st) { return st.ctx && !Array.isArray(st.ctx) && st.cand.ifs[st.ctx]; }
  function each(st, f) { ctxList(st).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }
  function touch(st) { st.pending = true; }

  // ---------------------------------------------------------------- режимы
  cmd('priv', 'configure', function (st) { st.mode = 'config'; }, 'Режим глобальной конфигурации');
  cmd('priv', 'configure terminal', function (st) { st.mode = 'config'; });
  cmd(CFG, 'exit', function (st) {
    if (st.mode === 'ospfa') { st.mode = 'ospf'; st.ctx = st.ospfId; return; }
    st.mode = st.mode === 'config' ? 'priv' : 'config'; st.ctx = null; }, 'Выход на уровень выше');
  cmd(CFG, 'end', function (st) { st.mode = 'priv'; st.ctx = null; }, 'Выход в привилегированный режим');

  // ---------------------------------------------------------------- commit / confirm
  function commit(st) {
    if (!st.pending) return 'Nothing to commit';
    st.run = EL.clone(st.cand); st.pending = false; st.unconfirmed = true; st.commits = (st.commits || 0) + 1;
    return 'Configuration has been successfully applied and saved to flash. Commit timer started, changes will be reverted in 600 seconds.';
  }
  function confirm(st) {
    if (!st.unconfirmed) return '% Нет изменений, ожидающих подтверждения';
    st.unconfirmed = false; return 'Configuration has been confirmed. Commit timer canceled.';
  }
  cmd('priv', 'commit', commit, 'Применить изменения кандидата');
  cmd('priv', 'confirm', confirm, 'Подтвердить применённую конфигурацию');
  cmd('priv', 'copy system:default-config system:candidate-config', function (st) {
    var h = st.cand.host; st.cand = freshCfg('vesr', st.nports); st.pending = true;
    return 'Candidate configuration replaced with default. Apply: commit'; }, 'Сбросить кандидат к заводской конфигурации');
  cmd('priv', 'reload system', function (st) { st.cand = EL.clone(st.run); st.pending = false; st.unconfirmed = false;
    return 'System is going to reboot... Done. Загружена применённая конфигурация (неприменённые правки потеряны)'; }, 'Перезагрузить');
  cmd('priv', 'rollback', function (st) { st.cand = EL.clone(st.run); st.pending = false; return 'Configuration has been successfully rolled back'; },
      'Откатить неприменённые изменения');

  // ---------------------------------------------------------------- базовая настройка
  cmd('config', 'hostname <w>', function (st, a) { st.cand.host = a[0]; touch(st); }, 'Имя устройства');
  cmd('config', 'clock timezone gmt <w>', function (st, a) {
    if (!/^[+-]?\d{1,2}$/.test(a[0])) return '% Неверный часовой пояс (пример: +7)';
    st.cand.tz = (/^[+-]/.test(a[0]) ? '' : '+') + a[0]; touch(st); }, 'Часовой пояс');
  cmd('priv', 'set date <w> <n> <w> <n>', function (st, a) {
    if (!/^\d{1,2}:\d{2}:\d{2}$/.test(a[0])) return '% Формат: set date ЧЧ:ММ:СС ДД Месяц ГГГГ';
    var M = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
    var mi = M.map(function (m) { return a[2].length >= 3 && m.indexOf(a[2].toLowerCase()) === 0; }).indexOf(true);
    if (mi < 0) return '% Месяц словом по-английски: January … December';
    var t = a[0].split(':'), local = Date.UTC(a[3], mi, a[1], +t[0], +t[1], +t[2]);
    st.date = a[0] + ' ' + a[1] + ' ' + a[2] + ' ' + a[3];
    st.clk = local - EL.clock.tzMs(st.run.tz) - EL.clock.now(); }, 'Установить дату и время');
  cmd('priv', 'show date', function (st) {
    var utc = st.net ? st.net.esrUtc(st.dev) : EL.clock.now() + (st.clk || 0);
    return '"' + EL.clock.fmt(utc + EL.clock.tzMs(st.run.tz)) + '"'; }, 'Текущие дата и время');
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
    var n = ifName(a[0]); if (!n) return '% Неверное имя интерфейса (пример: gigabitethernet 1/0/1, tengigabitethernet 1/0/1, gi1/0/1.10)';
    if (n.range) { if (n.range.some(function (k) { return !st.cand.ifs[k]; })) return '% Таких интерфейсов нет на устройстве';
      st.mode = 'gi'; st.ctx = n.range; return; }
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
    if (!cur(st)) return '% IP-адрес задаётся на одном интерфейсе, не на диапазоне';
    var c = IP.parseCidr(v); if (!c) return '% Формат адреса: A.B.C.D/длина, например 192.168.1.1/24';
    var me = st.ctx;
    var clash = Object.keys(st.cand.ifs).filter(function (k) { var x = st.cand.ifs[k]; return k !== me && x.ip &&
      IP.sameNet(x.ip.split('/')[0], c.ip, Math.min(+x.ip.split('/')[1], c.len)) && x.ip.split('/')[1] !== '32' && c.len !== 32; });
    if (clash.length) return '% Адрес пересекается с подсетью интерфейса ' + clash[0];
    cur(st).ip = c.ip + '/' + c.len; touch(st);
  }
  cmd('gi sub lo', 'ip address <w>', function (st, a) { return setIp(st, a[0]); }, 'IP-адрес/префикс');
  cmd('gi sub lo', 'no ip address', function (st) { each(st, function (x) { x.ip = null; }); });
  cmd('gi sub', 'ip firewall disable', function (st) { each(st, function (x) { x.fw = false; }); }, 'Отключить межсетевой экран');
  cmd('gi sub', 'no ip firewall disable', function (st) { each(st, function (x) { x.fw = true; }); });
  cmd('gi sub lo', 'shutdown', function (st) { each(st, function (x) { x.shut = true; }); }, 'Выключить интерфейс');
  cmd('gi sub lo', 'no shutdown', function (st) { each(st, function (x) { x.shut = false; }); }, 'Включить интерфейс');
  cmd('gi sub lo', 'description <rest>', function (st, a) { each(st, function (x) { x.desc = a[0]; }); }, 'Описание');
  // OSPF на интерфейсе
  cmd('gi sub', 'ip ospf instance <n>', function (st, a) { each(st, function (x) { x.ospf = x.ospf || {}; x.ospf.inst = a[0]; }); }, 'Процесс OSPF интерфейса');
  cmd('gi sub', 'ip ospf area <w>', function (st, a) { if (!/^\d+\.\d+\.\d+\.\d+$/.test(a[0])) return '% Область в формате A.B.C.D, например 0.0.0.0';
    each(st, function (x) { x.ospf = x.ospf || {}; x.ospf.area = a[0]; }); });
  cmd('gi sub', 'ip ospf', function (st) { each(st, function (x) { x.ospf = x.ospf || {}; x.ospf.on = true; }); }, 'Включить OSPF на интерфейсе');
  cmd('gi sub', 'no ip ospf', function (st) { each(st, function (x) { if (x.ospf) x.ospf.on = false; }); });
  cmd('gi sub', 'ip ospf passive-interface', function (st) { each(st, function (x) { x.ospf = x.ospf || {}; x.ospf.passive = true; }); });
  cmd('gi sub', 'no ip ospf passive-interface', function (st) { each(st, function (x) { if (x.ospf) x.ospf.passive = false; }); });
  cmd('gi sub', 'ip ospf cost <n>', function (st, a) { each(st, function (x) { x.ospf = x.ospf || {}; x.ospf.cost = a[0]; }); });

  // ---------------------------------------------------------------- статические маршруты
  function addRoute(st, a, ad) {
    var c = IP.parseCidr(a[0]); if (!c) return '% Формат: ip route A.B.C.D/длина шлюз [метрика]';
    if (ad !== undefined && (ad < 1 || ad > 255)) return '% Метрика (административное расстояние) 1–255';
    var net = IP.netOf(c.ip, c.len);
    st.cand.routes = st.cand.routes.filter(function (r) { return !(r.net === net && r.nh === a[1]); });
    st.cand.routes.push({ net: net, nh: a[1], ad: ad || 1 }); touch(st);
  }
  cmd('config', 'ip route <w> <ip>', function (st, a) { return addRoute(st, a); }, 'Статический маршрут');
  cmd('config', 'ip route <w> <ip> <n>', function (st, a) { return addRoute(st, a, a[2]); }, 'Плавающий маршрут с метрикой');
  cmd('config', 'no ip route <w> <ip>', function (st, a) {
    var c = IP.parseCidr(a[0]); if (!c) return '% Формат: no ip route A.B.C.D/длина шлюз';
    var net = IP.netOf(c.ip, c.len), n = st.cand.routes.length; a = a.slice(0, 2);
    st.cand.routes = st.cand.routes.filter(function (r) { return !(r.net === net && r.nh === a[1]); });
    if (n === st.cand.routes.length) return '% Маршрут не найден'; touch(st); });

  // ---------------------------------------------------------------- show
  function ifSort(a, b) { var f = function (k) { return k.charAt(0) === 'l' ? 1e6 + +k.slice(2) : +k.split('/')[2].split('.')[0] * 1e4 + (+k.split('.')[1] || 0); };
    return f(a) - f(b); }
  function longIf(k) { if (k.charAt(0) === 'l') return 'loopback ' + k.slice(2); var t = k.match(/^[a-z]+/)[0]; return (IFT[t] || 'gigabitethernet') + ' ' + k.slice(t.length); }
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
      if (x.ospf) { if (x.ospf.inst) d.push('  ip ospf instance ' + x.ospf.inst); if (x.ospf.area) d.push('  ip ospf area ' + x.ospf.area);
        if (x.ospf.passive) d.push('  ip ospf passive-interface'); if (x.ospf.on) d.push('  ip ospf'); }
      if (x.ip) d.push('  ip address ' + x.ip);
      if (x.helper) d.push('  ip helper-address ' + x.helper);
      if (d.length || k.indexOf('.') > 0 || k.charAt(0) === 'l') o.push('interface ' + longIf(k), d.join('\n'), 'exit');
    });
    RUNX.forEach(function (f) { f(c, o); });
    c.routes.forEach(function (r) { o.push('ip route ' + r.net + ' ' + r.nh + (r.ad && r.ad !== 1 ? ' ' + r.ad : '')); });
    if (c.rip) { o.push('router rip'); c.rip.nets.forEach(function (n) { o.push('  network ' + n); });
      c.rip.passive.forEach(function (n) { o.push('  passive-interface ' + longIf(n)); }); c.rip.redist.forEach(function (n) { o.push('  redistribute ' + n); });
      if (c.rip.on) o.push('  enable'); o.push('exit'); }
    if (c.ospf) { o.push('router ospf ' + c.ospf.id); if (c.ospf.rid) o.push('  router-id ' + c.ospf.rid);
      Object.keys(c.ospf.areas).forEach(function (k) { o.push('  area ' + k); if (c.ospf.areas[k].on) o.push('    enable'); o.push('  exit'); });
      if (c.ospf.on) o.push('  enable'); o.push('exit'); }
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
  cmd('priv', 'show ip route', function (st) { return st.net ? st.net.routeText(st.dev, false) : ''; }, 'Таблица маршрутизации');
  cmd('priv', 'show users', function (st) { return 'User      Privilege\n--------- ---------\n' +
    Object.keys(st.run.users).map(function (u) { return (u + '          ').slice(0, 10) + st.run.users[u].priv; }).join('\n'); });
  cmd('priv', 'ping <ip>', function (st, a) { return st.net ? st.net.pingText(st.dev, a[0], 'esr') : '% Нет сети'; }, 'Проверка связности');
  cmd('priv', 'traceroute <ip>', function (st, a) { return st.net ? st.net.traceText(st.dev, a[0]) : '% Нет сети'; }, 'Трассировка маршрута');


  // ---------------------------------------------------------------- RIP
  function rip(st) { return st.cand.rip || (st.cand.rip = { on: false, nets: [], passive: [], redist: [] }); }
  cmd('config', 'router rip', function (st) { rip(st); touch(st); st.mode = 'rip'; st.ctx = null; }, 'Настройка протокола RIP');
  cmd('config', 'no router rip', function (st) { st.cand.rip = null; touch(st); });
  cmd('rip', 'network <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return '% Формат: network A.B.C.D/длина';
    var n = IP.netOf(c.ip, c.len), r = rip(st); if (r.nets.indexOf(n) < 0) r.nets.push(n); touch(st); }, 'Анонсировать сеть');
  cmd('rip', 'no network <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return '% Формат: no network A.B.C.D/длина';
    var n = IP.netOf(c.ip, c.len), r = rip(st); r.nets = r.nets.filter(function (x) { return x !== n; }); touch(st); });
  cmd('rip', 'passive-interface <w>', function (st, a) { var n = ifName(a[0]); if (!n || n.range || !st.cand.ifs[n.name]) return '% Неверный интерфейс';
    var r = rip(st); if (r.passive.indexOf(n.name) < 0) r.passive.push(n.name); touch(st); }, 'Не рассылать обновления в интерфейс');
  cmd('rip', 'no passive-interface <w>', function (st, a) { var n = ifName(a[0]); if (!n) return '% Неверный интерфейс';
    var r = rip(st); r.passive = r.passive.filter(function (x) { return x !== n.name; }); touch(st); });
  cmd('rip', 'redistribute connected', function (st) { var r = rip(st); if (r.redist.indexOf('connected') < 0) r.redist.push('connected'); touch(st); }, 'Анонсировать подключённые сети');
  cmd('rip', 'redistribute static', function (st) { var r = rip(st); if (r.redist.indexOf('static') < 0) r.redist.push('static'); touch(st); }, 'Анонсировать статические маршруты');
  cmd('rip', 'enable', function (st) { rip(st).on = true; touch(st); }, 'Запустить RIP');
  cmd('rip', 'no enable', function (st) { rip(st).on = false; touch(st); });

  // ---------------------------------------------------------------- OSPF
  cmd('config', 'router ospf <n>', function (st, a) {
    if (a[0] < 1 || a[0] > 65535) return '% Номер процесса 1–65535';
    if (!st.cand.ospf || st.cand.ospf.id !== a[0]) st.cand.ospf = { id: a[0], rid: null, on: false, areas: {} };
    touch(st); st.mode = 'ospf'; st.ctx = a[0]; st.ospfId = a[0]; }, 'Настройка процесса OSPF');
  cmd('config', 'no router ospf <n>', function (st, a) { if (st.cand.ospf && st.cand.ospf.id === a[0]) st.cand.ospf = null; touch(st); });
  cmd('ospf', 'router-id <ip>', function (st, a) { st.cand.ospf.rid = a[0]; touch(st); }, 'Идентификатор маршрутизатора');
  cmd('ospf', 'area <w>', function (st, a) { if (!/^\d+\.\d+\.\d+\.\d+$/.test(a[0])) return '% Область в формате A.B.C.D, например 0.0.0.0';
    var ar = st.cand.ospf.areas; if (!ar[a[0]]) ar[a[0]] = { on: false }; touch(st); st.mode = 'ospfa'; st.ctx = a[0]; }, 'Область OSPF');
  cmd('ospfa', 'enable', function (st) { st.cand.ospf.areas[st.ctx].on = true; touch(st); }, 'Активировать область');
  cmd('ospfa', 'no enable', function (st) { st.cand.ospf.areas[st.ctx].on = false; touch(st); });
  cmd('ospf', 'enable', function (st) { st.cand.ospf.on = true; touch(st); }, 'Запустить процесс OSPF');
  cmd('ospf', 'no enable', function (st) { st.cand.ospf.on = false; touch(st); });

  cmd('priv', 'show ip rip', function (st) { return st.net ? st.net.dynText(st.dev, 'R') : ''; }, 'Маршруты RIP');
  cmd('priv', 'show ip ospf neighbors', function (st) { return st.net ? st.net.ospfNbrText(st.dev) : ''; }, 'Соседи OSPF');
  cmd('priv', 'show ip ospf', function (st) { var o = st.run.ospf;
    return o ? 'Routing Process: ospf ' + o.id + ' with ID ' + (o.rid || '0.0.0.0') + '\nProcess is ' + (o.on ? 'enabled' : 'disabled') +
      Object.keys(o.areas).map(function (k) { return '\n Area ' + k + ' — ' + (o.areas[k].on ? 'active' : 'inactive'); }).join('') : '% OSPF не настроен'; });
  cmd('priv', 'show ip route all', function (st) { return st.net ? st.net.routeText(st.dev, true) : ''; }, 'Все маршруты, включая резервные');

  function E() { return EL.E; }

  // do <команда> из любого режима конфигурации
  function exec(st, raw) {
    var line = normEsr(String(raw).trim());
    var m = line.match(/^do\s+(.+)$/i);
    if (m && st.mode !== 'priv') { var md = st.mode; st.mode = 'priv'; var r = EL.cli.runTable(T, st, m[1]); if (st.mode === 'priv') st.mode = md; return r; }
    return EL.cli.runTable(T, st, line);
  }
  function helpTable(st, raw) {
    var m = String(raw).match(/^\s*do\s+(.*)$/i);
    return m && st.mode !== 'priv' ? { mode: 'priv', raw: m[1] } : { mode: st.mode, raw: raw };
  }
  EL.esr = { T: T, cmd: cmd, RUNX: RUNX, longIf: longIf, ifNameFn: null, fresh: fresh, prompt: prompt, exec: exec, showRun: showRun, ifName: ifName, helpTable: helpTable,
             PROMPT: PROMPT, commit: commit, confirm: confirm };
})(typeof window !== 'undefined' ? window : global);
