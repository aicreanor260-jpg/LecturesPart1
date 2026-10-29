/* Расширение движка MES (_dk_cli.js) для эмулятора: пользовательский режим switch>, enable/disable,
   vlan database, списки VLAN, shutdown, L3 на SVI (ip route), ping, show ip interface/route, write/reload. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, IP = EL.ip, cmd = E.cmd, CFG = E.CFG;

  EL.attach = function (st, net, dev) {         // ссылки на сеть не попадают в JSON-копии состояния
    Object.defineProperty(st, 'net', { value: net, writable: true, configurable: true, enumerable: false });
    Object.defineProperty(st, 'dev', { value: dev, writable: true, configurable: true, enumerable: false });
  };

  function fresh(n, host, list, dialect) {
    var st = E.fresh(n);
    if (list) { var tpl = st.ports['gi1/0/1']; st.ports = {}; list.forEach(function (k) { st.ports[k] = EL.clone(tpl); }); }
    st.kind = 'mes'; st.mode = 'user'; st.host = host || 'switch'; st.routes = []; st.startup = null; st.dialect = dialect || '10';
    st.stp = { on: true, mode: st.dialect === '6' ? 'rst' : 'mst', prio: 32768 };
    Object.keys(st.ports).forEach(function (k) { st.ports[k].shut = false; });
    return st;
  }

  // ---------------------------------------------------------------- режимы
  cmd('user', 'enable', function (st) {
    if (st.enable[15]) { st.askPw = { ok: function () { st.mode = 'priv'; }, pw: st.enable[15] }; return 'Password:'; }
    st.mode = 'priv'; });
  cmd('priv', 'disable', function (st) { st.mode = 'user'; });
  cmd('user', 'exit', function () { return '% Сессия остаётся открытой (эмулятор)'; });
  cmd('config', 'vlan database', function (st) { st.mode = 'vlan'; st.ctx = null; });
  cmd('config vlan', 'vlan <list>', function (st, a) {
    if (a[0].some(function (v) { return v < 2 || v > 4094; })) return '% VLAN 1 и 4095 зарезервированы';
    a[0].forEach(function (v) { if (!st.vlans[v]) st.vlans[v] = '-'; });
    st.mode = 'vlan'; st.ctx = a[0].length === 1 ? a[0][0] : null; });
  cmd('vlan', 'name <rest>', function (st, a) {
    if (!st.ctx) return '% Имя задаётся для одной VLAN: vlan N, затем name';
    st.vlans[st.ctx] = a[0].replace(/^["«](.*)["»]$/, '$1'); });
  cmd('config', 'no vlan <list>', function (st, a) {
    if (a[0].indexOf(1) >= 0) return '% VLAN 1 удалить нельзя';
    a[0].forEach(function (v) { if (!st.vlans[v]) return; delete st.vlans[v];
      Object.keys(st.ports).forEach(function (k) { var p = st.ports[k]; if (p.access === v) p.access = 1;
        p.allowed = p.allowed.filter(function (x) { return x !== v; }); }); }); });

  // ---------------------------------------------------------------- порты
  function each(st, f) {
    if (!st.ctx || !st.ctx.ports) return '% Команда доступна в настройке физического порта';
    st.ctx.ports.forEach(function (k) { f(st.ports[k]); });
  }
  cmd('if range', 'shutdown', function (st) {
    if (st.ctx && st.ctx.svi) { st.sviShut = st.sviShut || {}; st.sviShut[st.ctx.svi] = true; return; }
    return each(st, function (p) { p.shut = true; }); });
  cmd('if range', 'no shutdown', function (st) {
    if (st.ctx && st.ctx.svi) { if (st.sviShut) delete st.sviShut[st.ctx.svi]; return; }
    return each(st, function (p) { p.shut = false; }); });
  cmd('if range', 'description <rest>', function (st, a) { return each(st, function (p) { p.desc = a[0]; }); });
  cmd('if', 'ip address <w>', function (st, a) {         // форма 10.0.0.1/24 одним словом
    if (!st.ctx || !st.ctx.svi) return '% Команда доступна на интерфейсе VLAN';
    var c = IP.parseCidr(a[0]); if (!c) return '% Формат: ip address A.B.C.D A.B.C.D (маска) или A.B.C.D /длина';
    st.svi[st.ctx.svi] = c.ip + '/' + c.len; });
  cmd('if', 'no ip address', function (st) { if (st.ctx && st.ctx.svi) delete st.svi[st.ctx.svi]; });
  cmd('config', 'no interface vlan <n>', function (st, a) { delete st.svi[a[0]]; });

  // ---------------------------------------------------------------- маршруты
  cmd('config', 'ip route <ip> <mask> <ip>', function (st, a) {
    var net = IP.netOf(a[0], a[1]);
    if (!st.routes.some(function (r) { return r.net === net && r.nh === a[2]; })) st.routes.push({ net: net, nh: a[2] }); });
  cmd('config', 'no ip route <ip> <mask> <ip>', function (st, a) {
    var net = IP.netOf(a[0], a[1]); st.routes = st.routes.filter(function (r) { return !(r.net === net && r.nh === a[2]); }); });
  cmd('config', 'no ip default-gateway', function (st) { st.gw = null; });
  cmd('config', 'ip routing', function (st) { st.routing = true; });

  // ---------------------------------------------------------------- сохранение
  function save(st) { var c = EL.clone(st); delete c.startup; c.mode = 'user'; c.ctx = null; st.startup = c;
    return 'Building configuration...\n[OK]\nCopy succeeded'; }
  cmd('priv', 'write', save); cmd('priv', 'write memory', save);
  cmd('priv', 'copy running-config startup-config', save);
  cmd('priv', 'show startup-config', function (st) { return st.startup ? E.showRun(st.startup) : '% Startup-config пуста — выполните write'; });
  cmd('priv', 'reload', function (st) {
    var keep = st.startup, nports = Object.keys(st.ports).length, host = 'console';
    var src = keep ? EL.clone(keep) : fresh(nports, host, Object.keys(st.ports), st.dialect);
    Object.keys(st).forEach(function (k) { delete st[k]; });
    Object.keys(src).forEach(function (k) { st[k] = src[k]; });
    st.startup = keep; st.mode = 'user';
    return 'Перезагрузка… загружена ' + (keep ? 'startup-config' : 'заводская конфигурация') + '.'; });

  // ---------------------------------------------------------------- show
  function sviUp(st, v) { return !(st.sviShut && st.sviShut[v]) && !!st.vlans[v]; }
  function showIpIf(st) {
    var ks = Object.keys(st.svi).map(Number).sort(function (a, b) { return a - b; });
    if (!ks.length) return '% IP-интерфейсы не настроены';
    return ks.map(function (v) { var p = st.svi[v].split('/');
      return ['vlan' + v + ' is ' + (sviUp(st, v) ? 'up' : 'down') + ', line protocol is ' + (sviUp(st, v) ? 'up' : 'down'),
              'Internet Address is ' + p[0] + '/' + p[1],
              'Broadcast Address  ' + IP.n2ip((IP.ip2n(p[0]) | (~IP.maskN(+p[1]) >>> 0)) >>> 0)].join('\n'); }).join('\n\n');
  }
  function showIpRoute(st) {
    var o = ['Codes: C - connected, S - static, R - rip, O - ospf', ''];
    Object.keys(st.svi).forEach(function (v) { if (!sviUp(st, v)) return; var p = st.svi[v].split('/');
      o.push('C ' + IP.netOf(p[0], +p[1]) + ' is directly connected, vlan' + v); });
    st.routes.forEach(function (r) { o.push('S ' + r.net + ' [1/0] via ' + r.nh); });
    if (st.gw) o.push('S 0.0.0.0/0 [1/0] via ' + st.gw);
    return o.join('\n');
  }
  function showStatus(st) {
    var o = ['Port         Status     Vlan   Mode', '------------ ---------- ------ -------'];
    Object.keys(st.ports).forEach(function (k) { var p = st.ports[k];
      var link = !p.shut && st.net && st.net.linked(st.dev, k);
      o.push((k + '             ').slice(0, 13) + ((p.shut ? 'disabled' : (link ? 'connected' : 'notconnect')) + '           ').slice(0, 11) +
             ((p.mode === 'access' ? '' + p.access : p.mode === 'trunk' ? 'trunk' : 'gen') + '       ').slice(0, 7) + p.mode); });
    return o.join('\n');
  }
  function shows(prefix, modes) {
    cmd(modes, prefix + 'show ip interface', function (st) { return showIpIf(st); });
    cmd(modes, prefix + 'show ip route', function (st) { return showIpRoute(st); });
    cmd(modes, prefix + 'show interfaces status', function (st) { return showStatus(st); });
    cmd(modes, prefix + 'show mac address-table', function (st) { return st.net ? st.net.macTable(st.dev) : ''; });
    cmd(modes, prefix + 'ping <ip>', function (st, a) { return st.net ? st.net.pingText(st.dev, a[0], 'mes') : '% Нет сети'; });
  }
  shows('', 'priv'); shows('do ', CFG);
  cmd('user', 'show vlan', function (st) { return E.showVlan(st); });
  cmd('user', 'show ip interface', function (st) { return showIpIf(st); });
  cmd('user', 'ping <ip>', function (st, a) { return st.net ? st.net.pingText(st.dev, a[0], 'mes') : '% Нет сети'; });

  // описания для «?» по первому слову
  var D = { enable: 'Привилегированный режим', disable: 'Пользовательский режим', configure: 'Режим глобальной конфигурации',
    show: 'Просмотр состояния и конфигурации', ping: 'Проверка связности', write: 'Сохранить конфигурацию',
    copy: 'Копировать конфигурацию', reload: 'Перезагрузить коммутатор', exit: 'Выход на уровень выше', end: 'Выход в режим #',
    hostname: 'Имя устройства', username: 'Локальный пользователь', interface: 'Настройка интерфейса', vlan: 'Создание VLAN',
    no: 'Отменить настройку', ip: 'Настройки IP', line: 'Консоль / Telnet / SSH', banner: 'Баннеры', enable_: '',
    switchport: 'Режим и VLAN порта', shutdown: 'Выключить порт', name: 'Имя VLAN', do: 'Команда режима # из конфигурации',
    password: 'Пароль', aaa: 'Аутентификация', crypto: 'Ключи шифрования', description: 'Описание' };
  E.CMDS.forEach(function (c) { if (!c.d && D[c.pat[0]]) c.d = D[c.pat[0]]; });

  function exec(st, raw) {
    if (/^\s*banner\s+motd\s/i.test(raw) && st.mode !== 'config') return '% Команда недоступна в этом режиме — проверьте приглашение';
    if (/^\s*ban/i.test(raw)) return E.exec(st, raw);       // баннеры с разделителем разбирает движок
    // interface gi / interface range te — тип порта без номера: команда не дописана
    if (st.mode === 'config' && /^\s*int\w*\s+(ran\w*\s+)?(g\w*|te\w*|fa\w*|fo\w*|hu\w*|tw\w*|po\w*)\s*$/i.test(raw) && !/^\s*int\w*\s+(ran\w*\s+)?(gr\w*)\s*$/i.test(raw)) return '% Incomplete command';
    return EL.cli.runTable(E.CMDS, st, raw);
  }
  EL.mes = { fresh: fresh, save: save, exec: exec, prompt: E.prompt, T: E.CMDS, showIpIf: showIpIf, sviUp: sviUp };
})(typeof window !== 'undefined' ? window : global);
