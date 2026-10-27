/* Симулятор CLI коммутатора Eltex для тренажёров дек «Базовая настройка» и «VLAN».
   Режимы и приглашения как на устройстве: switch# → configure → switch(config)# → interface … → switch(config-if)#.
   Задания генерируются случайно (кнопка «Обновить»), проверяется итоговое состояние коммутатора. */
(function () {
  'use strict';
  var NPORTS = 24;

  // ------------------------------------------------------------------ состояние коммутатора
  function fresh(n) {
    var ports = {};
    for (var i = 1; i <= (n || NPORTS); i++) {
      ports['gi1/0/' + i] = { mode: 'access', access: 1, allowed: [], native: 1, pvid: 1, gtag: [], guntag: [1] };
    }
    return {
      host: 'switch', mode: 'priv', ctx: null,
      vlans: { 1: '-' }, ports: ports, svi: {}, gw: null, ssh: false, rsa: false, http: true,
      users: {}, enable: {}, banner: { login: null, exec: null, motd: null },
      line: { console: {}, telnet: {}, ssh: {} }, aaa: null
    };
  }

  var PROMPT = { user: '>', priv: '#', config: '(config)#', 'if': '(config-if)#', range: '(config-if-range)#',
                 vlan: '(config-vlan)#', line: '(config-line)#' };
  function prompt(st) { return st.host + PROMPT[st.mode]; }

  function parseList(s) {           // "10,20,30-40" → [10,20,30..40]
    var out = [];
    String(s).split(',').forEach(function (p) {
      var m = p.match(/^(\d+)-(\d+)$/);
      if (m) { for (var i = +m[1]; i <= +m[2]; i++) out.push(i); }
      else if (/^\d+$/.test(p)) out.push(+p);
    });
    return out;
  }
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }).sort(function (a, b) { return a - b; }); }
  function fmtList(a) {
    a = uniq(a); var r = [], i = 0;
    while (i < a.length) { var j = i; while (j + 1 < a.length && a[j + 1] === a[j] + 1) j++;
      r.push(j > i ? a[i] + '-' + a[j] : '' + a[i]); i = j + 1; }
    return r.join(',');
  }
  // gi1/0/1, gi1/0/1-4, te1/0/1, fo1/0/2; без префикса — порты FASTPATH (MES5448/7048): 1/0/1, 1/0/1-1/0/4
  var PFX = { gi: 'gigabitethernet', te: 'tengigabitethernet', fo: 'fortygigabitethernet', hu: 'hundredgigabitethernet',
              tw: 'twopointfivegigabitethernet', fa: 'fastethernet' };
  function ifList(spec) {
    var m = spec.match(/^(gi|te|fo|hu|tw|fa)?(\d+)\/(\d+)\/(\d+)(?:-(?:(?:gi|te|fo|hu|tw|fa)?\d+\/\d+\/)?(\d+))?$/);
    if (!m || m[2] !== '1' || m[3] !== '0') return null;
    var pf = m[1] || '', a = +m[4], b = m[5] ? +m[5] : a, out = [];
    if (a < 1 || b > 64 || b < a) return null;
    for (var i = a; i <= b; i++) out.push(pf + '1/0/' + i);
    return out;
  }
  function longIf(k) { var m = k.match(/^([a-z]*)(\d.*)$/); return m[1] ? PFX[m[1]] + ' ' + m[2] : m[2]; }
  function portGroups(names) {      // ['gi1/0/1','gi1/0/2','te1/0/1'] → 'gi1/0/1-2, te1/0/1'
    var g = {}, order = [];
    names.forEach(function (k) { var m = k.match(/^(.*\/)(\d+)$/); if (!g[m[1]]) { g[m[1]] = []; order.push(m[1]); } g[m[1]].push(+m[2]); });
    return order.map(function (p) { return p + fmtList(g[p]); }).join(', ');
  }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    var x = (h >>> 0).toString(16); return (x + x + x + x + x).slice(0, 40); }

  // ------------------------------------------------------------------ команды: шаблоны с префиксами ключевых слов
  // <n> число, <w> слово, <ip> адрес, <if> интерфейс, <list> список VLAN, <rest> остаток строки
  var CMDS = [];
  function cmd(modes, pat, run) { CMDS.push({ modes: modes.split(' '), pat: pat.split(' '), run: run }); }
  var CFG = 'config if range vlan line';

  function match(pat, toks) {
    var args = [], i = 0;
    for (var k = 0; k < pat.length; k++) {
      var p = pat[k], t = toks[i];
      if (p === '<rest>') { if (i >= toks.length) return null; args.push(toks.slice(i).join(' ')); return args; }
      if (t === undefined) return null;
      if (p === '<n>') { if (!/^\d+$/.test(t)) return null; args.push(+t); i++; continue; }
      if (p === '<w>') { args.push(t); i++; continue; }
      if (p === '<ip>') { if (!/^\d+\.\d+\.\d+\.\d+$/.test(t)) return null; args.push(t); i++; continue; }
      if (p === '<if>') { var L = ifList(t); if (!L) return null; args.push(L); i++; continue; }
      if (p === '<list>') { if (!/^[\d,\-]+$/.test(t)) return null; args.push(parseList(t)); i++; continue; }
      if (p === '<mask>') {           // /24, 24 или 255.255.255.0
        var mm = t.match(/^\/?(\d{1,2})$/);
        if (mm) { args.push(+mm[1]); i++; continue; }
        if (/^\d+\.\d+\.\d+\.\d+$/.test(t)) { args.push(t.split('.').reduce(function (a, o) {
          return a + (+o).toString(2).replace(/0/g, '').length; }, 0)); i++; continue; }
        return null;
      }
      // ключевое слово: точное совпадение или префикс от 2 символов
      if (t === p || (t.length >= 2 && p.indexOf(t) === 0) || (p === 'terminal' && t === 't')) { i++; continue; }
      return null;
    }
    return i === toks.length ? args : null;
  }

  // --- режимы
  cmd('priv', 'configure', function (st) { st.mode = 'config'; });
  cmd('priv', 'configure terminal', function (st) { st.mode = 'config'; });
  cmd(CFG, 'exit', function (st) { st.mode = st.mode === 'config' ? 'priv' : 'config'; st.ctx = null; });
  cmd(CFG, 'end', function (st) { st.mode = 'priv'; st.ctx = null; });
  cmd('priv', 'exit', function () { return '% Сессия остаётся открытой (тренажёр)'; });

  // --- базовая настройка
  cmd('config', 'hostname <rest>', function (st, a) {
    var h = a[0].replace(/^"(.*)"$/, '$1');
    if (/\s/.test(h) && !/^".*"$/.test(a[0])) return '% Имя с пробелом нужно указывать в кавычках';
    if (h.length > 128) return '% Имя длиннее 128 символов';
    st.host = h;
  });
  cmd('config', 'no hostname', function (st) { st.host = 'switch'; });
  cmd('config', 'username <w> password <w> privilege <n>', function (st, a) {
    if (a[2] < 1 || a[2] > 15) return '% Уровень привилегии 1–15'; st.users[a[0]] = { pw: a[1], priv: a[2] }; });
  cmd('config', 'no username <w>', function (st, a) {
    if (!st.users[a[0]]) return '% Пользователь не найден'; delete st.users[a[0]]; });
  cmd('config', 'enable password level <n> <w>', function (st, a) { st.enable[a[0]] = a[1]; });
  cmd('config', 'enable password <w>', function (st, a) { st.enable[15] = a[0]; });
  cmd('config', 'line console', function (st) { st.mode = 'line'; st.ctx = 'console'; });
  cmd('config', 'line ssh', function (st) { st.mode = 'line'; st.ctx = 'ssh'; });
  cmd('config', 'line telnet', function (st) { st.mode = 'line'; st.ctx = 'telnet'; if (!st.line.telnet) st.line.telnet = {}; });
  cmd('line', 'password <w>', function (st, a) { st.line[st.ctx].pw = a[0]; });
  cmd('line', 'exec-timeout <n>', function (st, a) { st.line[st.ctx].timeout = a[0]; });
  cmd('line', 'login authentication <w>', function (st, a) { st.line[st.ctx].auth = a[0]; });
  cmd('line', 'login-attempts <n>', function (st, a) { st.line[st.ctx].attempts = a[0]; });
  cmd('line', 'history size <n>', function (st, a) { st.line[st.ctx].history = a[0]; });
  cmd('config', 'aaa authentication login <w> <rest>', function (st, a) { st.aaa = a[0] + ' ' + a[1]; });
  cmd('config', 'ip ssh server', function (st) { st.ssh = true; });
  cmd('config', 'no ip ssh server', function (st) { st.ssh = false; });
  cmd('config', 'crypto key generate rsa', function (st) {
    st.rsa = true; return 'Replace Existing (Default) RSA Key ? (Y/N)[N] Y\nThe SSH Server is generating a RSA key. This may take a few minutes, depending on the key size.'; });
  cmd('config', 'ip http server', function (st) { st.http = true; });
  cmd('config', 'no ip http server', function (st) { st.http = false; });
  cmd('config', 'ip default-gateway <ip>', function (st, a) { st.gw = a[0]; });
  cmd('config', 'interface vlan <n>', function (st, a) { st.mode = 'if'; st.ctx = { svi: a[0] }; });
  cmd('if', 'ip address <ip> <mask>', function (st, a) {
    if (!st.ctx || !st.ctx.svi) return '% Команда доступна на интерфейсе VLAN';
    st.svi[st.ctx.svi] = a[0] + '/' + a[1]; });

  // --- VLAN
  cmd('config', 'vlan <n> name <w>', function (st, a) { if (a[0] < 2 || a[0] > 4094) return '% VLAN 1 и 4095 зарезервированы';
    st.vlans[a[0]] = a[1]; });
  cmd('config vlan', 'vlan <n>', function (st, a) { if (a[0] < 2 || a[0] > 4094) return '% VLAN 1 и 4095 зарезервированы';
    if (!st.vlans[a[0]]) st.vlans[a[0]] = '-'; st.mode = 'vlan'; st.ctx = a[0]; });
  cmd('vlan', 'name <w>', function (st, a) { st.vlans[st.ctx] = a[0]; });
  cmd('config', 'no vlan <n>', function (st, a) {
    if (a[0] === 1) return '% VLAN 1 удалить нельзя'; if (!st.vlans[a[0]]) return '% VLAN не существует';
    delete st.vlans[a[0]];
    Object.keys(st.ports).forEach(function (k) { if (st.ports[k].access === a[0]) st.ports[k].access = 1; });
  });
  cmd('config', 'interface <if>', function (st, a) {
    if (a[0].length > 1) return '% Для нескольких портов используйте interface range';
    if (!st.ports[a[0][0]]) return '% Такого порта нет на устройстве';
    st.mode = 'if'; st.ctx = { ports: a[0] }; });
  cmd('config', 'interface range <if>', function (st, a) { st.mode = 'range'; st.ctx = { ports: a[0] }; });
  function eachPort(st, f) {
    if (!st.ctx || !st.ctx.ports) return '% Команда доступна в настройке физического порта';
    if (st.ctx.ports.some(function (k) { return !st.ports[k] && !(st.pos && st.pos[k]); })) return '% Такого порта нет на устройстве';
    st.ctx.ports.forEach(function (k) { f(st.ports[k] || st.pos[k]); });
  }
  var IFM = 'if range';
  cmd(IFM, 'switchport mode access', function (st) { return eachPort(st, function (p) { p.mode = 'access'; }); });
  cmd(IFM, 'switchport mode trunk', function (st) { return eachPort(st, function (p) { p.mode = 'trunk'; }); });
  cmd(IFM, 'switchport mode general', function (st) { return eachPort(st, function (p) { p.mode = 'general'; }); });
  cmd(IFM, 'switchport access vlan <n>', function (st, a) {
    if (!st.vlans[a[0]]) return '% VLAN ' + a[0] + ' не создана';
    return eachPort(st, function (p) { p.access = a[0]; }); });
  cmd(IFM, 'no switchport access vlan', function (st) { return eachPort(st, function (p) { p.access = 1; }); });
  cmd(IFM, 'switchport trunk allowed vlan add <list>', function (st, a) {
    var bad = a[0].filter(function (v) { return !st.vlans[v]; });
    if (bad.length) return '% VLAN ' + fmtList(bad) + ' не созданы';
    return eachPort(st, function (p) { p.allowed = uniq(p.allowed.concat(a[0])); }); });
  cmd(IFM, 'switchport trunk allowed vlan remove <list>', function (st, a) {
    return eachPort(st, function (p) { p.allowed = p.allowed.filter(function (v) { return a[0].indexOf(v) < 0; }); }); });
  cmd(IFM, 'switchport trunk native vlan <n>', function (st, a) {
    if (!st.vlans[a[0]]) return '% VLAN ' + a[0] + ' не создана';
    return eachPort(st, function (p) { p.native = a[0]; }); });
  cmd(IFM, 'switchport general pvid <n>', function (st, a) {
    if (!st.vlans[a[0]]) return '% VLAN ' + a[0] + ' не создана';
    return eachPort(st, function (p) { p.pvid = a[0]; }); });
  cmd(IFM, 'switchport general allowed vlan add <list> tagged', function (st, a) {
    var bad = a[0].filter(function (v) { return !st.vlans[v]; }); if (bad.length) return '% VLAN ' + fmtList(bad) + ' не созданы';
    return eachPort(st, function (p) { p.gtag = uniq(p.gtag.concat(a[0])); p.guntag = p.guntag.filter(function (v) { return a[0].indexOf(v) < 0; }); }); });
  cmd(IFM, 'switchport general allowed vlan add <list> untagged', function (st, a) {
    var bad = a[0].filter(function (v) { return !st.vlans[v]; }); if (bad.length) return '% VLAN ' + fmtList(bad) + ' не созданы';
    return eachPort(st, function (p) { p.guntag = uniq(p.guntag.concat(a[0])); p.gtag = p.gtag.filter(function (v) { return a[0].indexOf(v) < 0; }); }); });

  // --- show
  var RUNX = [], PORTX = [];                  // PORTX: доп. строки внутри блока interface                              // доп. строки running-config от модулей эмулятора
  function showRun(st) {
    var o = [];
    var vl = Object.keys(st.vlans).map(Number).filter(function (v) { return v !== 1; });
    if (vl.length) { o.push('vlan database', ' vlan ' + fmtList(vl));
      vl.forEach(function (v) { if (st.vlans[v] !== '-') o.push(' vlan ' + v + ' name ' + st.vlans[v]); }); o.push('exit', '!'); }
    if (st.host !== 'switch') o.push('hostname ' + (/\s/.test(st.host) ? '"' + st.host + '"' : st.host), '!');
    Object.keys(st.users).forEach(function (u) { o.push('username ' + u + ' password encrypted ' + hash(st.users[u].pw) + ' privilege ' + st.users[u].priv); });
    Object.keys(st.enable).forEach(function (l) { o.push('enable password ' + (l == 15 ? '' : 'level ' + l + ' ') + 'encrypted ' + hash(st.enable[l])); });
    if (Object.keys(st.users).length) o.push('!');
    if (st.banner.motd) o.push('banner motd ^', st.banner.motd, '^');
    if (st.banner.login) o.push('banner login ^', st.banner.login, '^');
    if (st.banner.exec) o.push('banner exec ^', st.banner.exec, '^');
    if (st.banner.login || st.banner.exec || st.banner.motd) o.push('!');
    ['console', 'telnet', 'ssh'].forEach(function (l) { var c = st.line[l]; if (!c || !Object.keys(c).length) return;
      o.push('line ' + l); if (c.timeout !== undefined) o.push(' exec-timeout ' + c.timeout);
      if (c.attempts) o.push(' login-attempts ' + c.attempts); if (c.history) o.push(' history size ' + c.history);
      if (c.auth) o.push(' login authentication ' + c.auth); if (c.pw) o.push(' password encrypted ' + hash(c.pw)); o.push('exit', '!'); });
    if (st.aaa) o.push('aaa authentication login ' + st.aaa, '!');
    Object.keys(st.ports).forEach(function (k) {
      var p = st.ports[k], d = p.desc ? [' description ' + p.desc] : [];
      if (p.mode === 'access' && p.access !== 1) d.push(' switchport access vlan ' + p.access);
      if (p.mode === 'trunk') { d.push(' switchport mode trunk'); if (p.allowed.length) d.push(' switchport trunk allowed vlan add ' + fmtList(p.allowed));
        if (p.native !== 1) d.push(' switchport trunk native vlan ' + p.native); }
      if (p.mode === 'general') { d.push(' switchport mode general');
        if (p.gtag.length) d.push(' switchport general allowed vlan add ' + fmtList(p.gtag) + ' tagged');
        var u = p.guntag.filter(function (v) { return v !== 1; }); if (u.length) d.push(' switchport general allowed vlan add ' + fmtList(u) + ' untagged');
        if (p.pvid !== 1) d.push(' switchport general pvid ' + p.pvid); }
      PORTX.forEach(function (f) { f(st, k, p, d); });
      if (d.length) o.push('interface ' + longIf(k).replace(' ', ''), d.join('\n'), 'exit', '!');
    });
    Object.keys(st.svi).forEach(function (v) { o.push('interface vlan ' + v, ' ip address ' + st.svi[v].replace('/', ' /'), 'exit', '!'); });
    if (st.gw) o.push('ip default-gateway ' + st.gw);
    if (st.ssh) o.push('ip ssh server');
    if (!st.http) o.push('no ip http server');
    RUNX.forEach(function (f) { f(st, o); });
    o.push('!');
    return o.join('\n');
  }
  function showVlan(st) {
    var o = ['Created by: D-Default, S-Static, G-GVRP, R-Radius Assigned VLAN, V-Voice VLAN', '',
             'Vlan       Name           Tagged Ports      UnTagged Ports      Created by',
             '---- ----------------- ------------------ ------------------ ----------------'];
    Object.keys(st.vlans).map(Number).sort(function (a, b) { return a - b; }).forEach(function (v) {
      var tg = [], un = [];
      Object.keys(st.ports).forEach(function (k) { var p = st.ports[k], n = k;
        if (p.mode === 'access' && p.access === v) un.push(n);
        if (p.mode === 'trunk') { if (p.native === v) un.push(n); else if (p.allowed.indexOf(v) >= 0) tg.push(n); }
        if (p.mode === 'general') { if (p.gtag.indexOf(v) >= 0) tg.push(n); if (p.guntag.indexOf(v) >= 0) un.push(n); } });
      var f = function (a) { return a.length ? portGroups(a) : ''; };
      o.push((v + '    ').slice(0, 5) + ((st.vlans[v] === '-' ? '-' : st.vlans[v]) + '                  ').slice(0, 18) +
             (f(tg) + '                   ').slice(0, 19) + (f(un) + '                   ').slice(0, 19) + (v === 1 ? 'D' : 'S'));
    });
    return o.join('\n');
  }
  function showSw(st, ports) {
    var k = ports[0], p = st.ports[k];
    var o = ['Port : ' + k, 'Port Mode: ' + p.mode.charAt(0).toUpperCase() + p.mode.slice(1),
             'Gvrp Status: disabled', 'Ingress Filtering: true'];
    if (p.mode === 'access') o.push('Acceptable Frame Type: admitUntaggedOnly', 'Ingress UnTagged VLAN ( NATIVE ): ' + p.access);
    if (p.mode === 'trunk') o.push('Acceptable Frame Type: admitAll', 'Ingress UnTagged VLAN ( NATIVE ): ' + p.native,
                                   'Trunking VLANs Enabled: ' + (fmtList(p.allowed) || 'none'));
    if (p.mode === 'general') o.push('Acceptable Frame Type: admitAll', 'Ingress UnTagged VLAN ( NATIVE ): ' + p.pvid,
                                     'Tagged VLANs: ' + (fmtList(p.gtag) || 'none'), 'Untagged VLANs: ' + (fmtList(p.guntag) || 'none'));
    return o.join('\n');
  }
  function addShow(prefix, modes) {
    cmd(modes, prefix + 'show running-config', function (st) { return showRun(st); });
    cmd(modes, prefix + 'show vlan', function (st) { return showVlan(st); });
    cmd(modes, prefix + 'show interfaces switchport <if>', function (st, a) { return showSw(st, a[0]); });
    cmd(modes, prefix + 'show privilege', function () { return 'Current privilege level is 15'; });
  }
  addShow('', 'priv');
  addShow('do ', CFG);

  // ------------------------------------------------------------------ выполнение строки
  function normLine(s) {
    return s.replace(/\b(?:te|ten|tengig\w*)\s*(?=\d+\/\d+\/\d+)/ig, 'te').replace(/\b(?:fo|for|forty\w*)\s*(?=\d+\/\d+\/\d+)/ig, 'fo')
            .replace(/\b(?:hu|hun|hundred\w*)\s*(?=\d+\/\d+\/\d+)/ig, 'hu').replace(/\b(?:tw|two\w*)\s*(?=\d+\/\d+\/\d+)/ig, 'tw')
            .replace(/\b(?:fa|fast\w*)\s*(?=\d+\/\d+\/\d+)/ig, 'fa')
            .replace(/\b(?:g|gi|gig|giga|gigabit|gigabitethernet)\s*(?=\d+\/\d+\/\d+)/ig, 'gi');
  }
  function exec(st, raw) {
    var line = normLine(raw.trim());
    if (!line) return '';
    // баннер: banner login @ текст @
    var b = line.match(/^ban\w*\s+(log\w*|exe\w*|motd)\s+(\S)([\s\S]*)$/i);
    if (b && st.mode === 'config') {
      var kind = /^l/i.test(b[1]) ? 'login' : (/^m/i.test(b[1]) ? 'motd' : 'exec'), d = b[2], rest = b[3], e = rest.lastIndexOf(d);
      if (e < 0) return '% Текст баннера должен заканчиваться разделителем ' + d;
      st.banner[kind] = rest.slice(0, e).trim(); return '';
    }
    var toks = line.split(/\s+/);
    var low = toks.map(function (t) { return t.toLowerCase(); });
    for (var i = 0; i < CMDS.length; i++) {
      var c = CMDS[i]; if (c.modes.indexOf(st.mode) < 0) continue;
      // значения (имена, пароли, баннеры) сохраняем как ввели — регистр важен
      var args = match(c.pat, low);
      if (args) {
        var ri = c.pat.indexOf('<rest>');
        var orig = match(c.pat, toks.map(function (t, j) { return (c.pat[j] === '<w>' || (ri >= 0 && j >= ri)) ? t : low[j]; }));
        return c.run(st, orig || args) || '';
      }
    }
    var other = CMDS.some(function (c) { return match(c.pat, low); });
    return other ? '% Команда недоступна в этом режиме — проверьте приглашение' : '% Unrecognized command';
  }

  // ------------------------------------------------------------------ задания
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  function ports2() { var a = rnd(1, 20), b; do { b = rnd(1, 20); } while (Math.abs(a - b) < 2); return [a, b]; }

  var NAMES = ['SW1-Room502', 'SW2-Floor3', 'Core-SW-NSK', 'SW-Lab214', 'Access-SW-7', 'SW3-Building2'];
  var NAMES_SP = ['SW1 Room502 Floor5', 'Lab SW 214', 'Core SW NSK'];
  var BANNERS = ['Unauthorized intrusion is prohibited!', 'Neavtorizovanniy vhod zapreschon!', 'Authorized access only!',
                 'Legal action may follow!'];
  var WELCOME = ['Welcome!', 'Dobro pojalovat!', 'Wilkommen!', 'Hello, admin!'];
  var USERS = ['admin1', 'netadmin', 'support', 'student', 'operator'];
  var VNAMES = ['IT', 'Management', 'Buh', 'Guest', 'Voice', 'Lab'];

  var TASKS = {
    base: [
      { gen: function () { var sp = Math.random() < .35; return { h: sp ? pick(NAMES_SP) : pick(NAMES) }; },
        text: function (p) { return 'Задайте коммутатору имя <b>' + p.h + '</b>.' + (/\s/.test(p.h) ? ' В имени есть пробелы.' : ''); },
        sol: function (p) { return ['configure', 'hostname ' + (/\s/.test(p.h) ? '"' + p.h + '"' : p.h), 'end']; },
        checks: function (p) { return [['Имя устройства — ' + p.h, function (s) { return s.host === p.h; }],
                                       ['Вы вернулись в привилегированный режим (#)', function (s) { return s.mode === 'priv'; }]]; } },
      { gen: function () { return { t: pick(BANNERS), w: pick(WELCOME) }; },
        text: function (p) { return 'Настройте <b>banner login</b> с текстом «' + p.t + '» и <b>banner exec</b> с текстом «' + p.w + '». Разделитель — @.'; },
        sol: function (p) { return ['configure', 'banner login @ ' + p.t + ' @', 'banner exec @ ' + p.w + ' @', 'end']; },
        checks: function (p) { return [['banner login: «' + p.t + '»', function (s) { return s.banner.login === p.t; }],
                                       ['banner exec: «' + p.w + '»', function (s) { return s.banner.exec === p.w; }]]; },
        login: true },
      { gen: function () { var u = pick(USERS); return { u: u, pw: u + rnd(10, 99), l: pick([1, 4, 7, 15]), u2: 'user', l2: 1 }; },
        text: function (p) { return 'Создайте пользователя <b>' + p.u + '</b> с паролем <b>' + p.pw + '</b> и уровнем привилегий <b>' + p.l +
                                    '</b>, а также пользователя <b>user</b> с паролем <b>user</b> и уровнем <b>1</b>.'; },
        sol: function (p) { return ['configure', 'username ' + p.u + ' password ' + p.pw + ' privilege ' + p.l,
                                    'username user password user privilege 1', 'end']; },
        checks: function (p) { return [['Пользователь ' + p.u + ' / ' + p.pw + ' / privilege ' + p.l, function (s) {
                                         var u = s.users[p.u]; return u && u.pw === p.pw && u.priv === p.l; }],
                                       ['Пользователь user / user / privilege 1', function (s) {
                                         var u = s.users.user; return u && u.pw === 'user' && u.priv === 1; }]]; },
        login: true },
      { gen: function () { return { pw: pick(['consolepass', 'c0ns0le', 'eltexcon']), t: pick([3, 5, 10]) }; },
        text: function (p) { return 'Защитите консольный порт: пароль <b>' + p.pw + '</b>, период неактивности <b>' + p.t +
                                    '</b> минут, метод <b>login authentication console</b>, а в глобальной конфигурации — аутентификация console: сначала line, затем local.'; },
        sol: function (p) { return ['configure', 'line console', 'password ' + p.pw, 'exec-timeout ' + p.t,
                                    'login authentication console', 'exit', 'aaa authentication login console line local', 'end']; },
        checks: function (p) { return [['Пароль консоли ' + p.pw, function (s) { return s.line.console.pw === p.pw; }],
                                       ['exec-timeout ' + p.t, function (s) { return s.line.console.timeout === p.t; }],
                                       ['login authentication console', function (s) { return s.line.console.auth === 'console'; }],
                                       ['aaa authentication login console line local', function (s) { return s.aaa === 'console line local'; }]]; } },
      { gen: function () { return { l: pick([3, 4, 7]), p4: 'eltex' + rnd(2, 9), p15: 'eltex15' }; },
        text: function (p) { return 'Задайте пароль <b>' + p.p4 + '</b> для временного повышения до уровня <b>' + p.l +
                                    '</b> и пароль <b>' + p.p15 + '</b> для повышения до уровня 15.'; },
        sol: function (p) { return ['configure', 'enable password level ' + p.l + ' ' + p.p4, 'enable password ' + p.p15, 'end']; },
        checks: function (p) { return [['enable password level ' + p.l, function (s) { return s.enable[p.l] === p.p4; }],
                                       ['enable password (уровень 15)', function (s) { return s.enable[15] === p.p15; }]]; } },
      { gen: function () { var v = pick([20, 30, 99, 100]), o = rnd(2, 200); return { v: v, ip: '10.10.' + rnd(1, 9) + '.' + o, gw: null, t: rnd(1, 24) }; },
        text: function (p) { var g = p.ip.replace(/\.\d+$/, '.1'); p.gw = g;
          return 'Подготовьте управление по SSH: VLAN <b>' + p.v + '</b> с именем <b>Management</b>, разрешите её на транке <b>gi1/0/' + p.t +
                 '</b>, на SVI VLAN ' + p.v + ' адрес <b>' + p.ip + ' /24</b>, шлюз <b>' + g + '</b>, включите SSH-сервер и сгенерируйте ключи RSA.'; },
        sol: function (p) { return ['configure', 'vlan ' + p.v + ' name Management', 'interface gigabitethernet 1/0/' + p.t, 'switchport mode trunk',
                                    'switchport trunk allowed vlan add ' + p.v, 'exit', 'interface vlan ' + p.v, 'ip address ' + p.ip + ' /24', 'exit',
                                    'ip default-gateway ' + p.gw, 'ip ssh server', 'crypto key generate rsa', 'end']; },
        checks: function (p) { return [['VLAN ' + p.v + ' Management', function (s) { return s.vlans[p.v] === 'Management'; }],
                                       ['gi1/0/' + p.t + ': trunk, VLAN ' + p.v + ' разрешена', function (s) { var q = s.ports['gi1/0/' + p.t];
                                         return q.mode === 'trunk' && q.allowed.indexOf(p.v) >= 0; }],
                                       ['SVI VLAN ' + p.v + ': ' + p.ip + '/24', function (s) { return s.svi[p.v] === p.ip + '/24'; }],
                                       ['Шлюз ' + p.gw, function (s) { return s.gw === p.gw; }],
                                       ['SSH-сервер и ключи RSA', function (s) { return s.ssh && s.rsa; }]]; } }
    ],
    vlan: [
      { gen: function () { var a = rnd(2, 50) * 2, b = a + rnd(1, 9) * 10; return { a: a, b: b, na: pick(VNAMES), nb: pick(VNAMES) }; },
        text: function (p) { if (p.na === p.nb) p.nb = p.nb + '2';
          return 'Создайте VLAN <b>' + p.a + '</b> с именем <b>' + p.na + '</b> и VLAN <b>' + p.b + '</b> с именем <b>' + p.nb +
                 '</b> через режим config-vlan, затем проверьте командой show vlan.'; },
        sol: function (p) { return ['configure', 'vlan ' + p.a, 'name ' + p.na, 'vlan ' + p.b, 'name ' + p.nb, 'end', 'show vlan']; },
        checks: function (p) { return [['VLAN ' + p.a + ' ' + p.na, function (s) { return s.vlans[p.a] === p.na; }],
                                       ['VLAN ' + p.b + ' ' + p.nb, function (s) { return s.vlans[p.b] === p.nb; }]]; } },
      { gen: function () { var pp = ports2(); return { v: pick([10, 20, 30, 40]), p1: pp[0], p2: pp[1] }; },
        text: function (p) { return 'ПК1 подключён к <b>gi1/0/' + p.p1 + '</b>, ПК2 — к <b>gi1/0/' + p.p2 + '</b>. Создайте VLAN <b>' + p.v +
                                    '</b> и переведите оба порта в режим доступа этой VLAN. Затем отправьте кадр ПК1 → ПК2.'; },
        sol: function (p) { return ['configure', 'vlan ' + p.v, 'exit', 'interface gigabitethernet 1/0/' + p.p1, 'switchport mode access',
                                    'switchport access vlan ' + p.v, 'exit', 'interface gigabitethernet 1/0/' + p.p2, 'switchport mode access',
                                    'switchport access vlan ' + p.v, 'end']; },
        checks: function (p) { return [['VLAN ' + p.v + ' создана', function (s) { return !!s.vlans[p.v]; }],
                                       ['gi1/0/' + p.p1 + ': access VLAN ' + p.v, function (s) { var q = s.ports['gi1/0/' + p.p1]; return q.mode === 'access' && q.access === p.v; }],
                                       ['gi1/0/' + p.p2 + ': access VLAN ' + p.v, function (s) { var q = s.ports['gi1/0/' + p.p2]; return q.mode === 'access' && q.access === p.v; }]]; },
        send: function (p, s) { return sendAccess(s, p.p1, p.p2); } },
      { gen: function () { var a = rnd(1, 12), n = rnd(3, 6); return { v: pick([10, 20, 50]), a: a, b: a + n, x: a + n + 2 }; },
        text: function (p) { return 'Одной командой interface range назначьте порты <b>gi1/0/' + p.a + '-' + p.b + '</b> в VLAN <b>' + p.v +
                                    '</b> (VLAN создайте заранее). Порт gi1/0/' + p.x + ' не трогайте — кадр к нему из VLAN ' + p.v + ' не должен дойти.'; },
        sol: function (p) { return ['configure', 'vlan ' + p.v, 'exit', 'interface range gigabitethernet 1/0/' + p.a + '-' + p.b,
                                    'switchport mode access', 'switchport access vlan ' + p.v, 'end', 'show vlan']; },
        checks: function (p) { return [['Порты gi1/0/' + p.a + '-' + p.b + ' в VLAN ' + p.v, function (s) {
                                         for (var i = p.a; i <= p.b; i++) { var q = s.ports['gi1/0/' + i]; if (q.mode !== 'access' || q.access !== p.v) return false; } return true; }],
                                       ['gi1/0/' + p.x + ' остался в VLAN 1', function (s) { return s.ports['gi1/0/' + p.x].access === 1; }]]; },
        send: function (p, s) { return sendAccess(s, p.a, p.b).concat(sendAccess(s, p.a, p.x)); } },
      { gen: function () { var t = rnd(20, 24), a = pick([10, 20]), b = a + 10, n = pick([50, 99]); return { t: t, a: a, b: b, n: n, x: b + 10 }; },
        text: function (p) { return 'Порт <b>gi1/0/' + p.t + '</b> смотрит на соседний коммутатор. Создайте VLAN ' + p.a + ', ' + p.b + ' и ' + p.n +
                                    ', сделайте порт транком: разрешите VLAN <b>' + p.a + '</b> и <b>' + p.b + '</b>, нативная VLAN — <b>' + p.n +
                                    '</b>. Проверьте отправкой кадров через транк.'; },
        sol: function (p) { return ['configure', 'vlan ' + p.a, 'vlan ' + p.b, 'vlan ' + p.n, 'exit', 'interface gigabitethernet 1/0/' + p.t,
                                    'switchport mode trunk', 'switchport trunk allowed vlan add ' + p.a + ',' + p.b,
                                    'switchport trunk native vlan ' + p.n, 'end']; },
        checks: function (p) { return [['gi1/0/' + p.t + ' в режиме trunk', function (s) { return s.ports['gi1/0/' + p.t].mode === 'trunk'; }],
                                       ['Разрешены VLAN ' + p.a + ' и ' + p.b, function (s) { var q = s.ports['gi1/0/' + p.t];
                                         return q.allowed.indexOf(p.a) >= 0 && q.allowed.indexOf(p.b) >= 0; }],
                                       ['Нативная VLAN ' + p.n, function (s) { return s.ports['gi1/0/' + p.t].native === p.n; }]]; },
        send: function (p, s) { return sendTrunk(s, p.t, [p.a, p.b, p.n, p.x]); } },
      { gen: function () { var g = rnd(1, 8); return { g: g, d: pick([10, 20]), v: pick([100, 110]) }; },
        text: function (p) { return 'К порту <b>gi1/0/' + p.g + '</b> подключён IP-телефон, через него — ПК. Создайте VLAN ' + p.d + ' и ' + p.v +
                                    '. Настройте порт в режиме <b>general</b>: данные ПК — VLAN <b>' + p.d + '</b> без тега (PVID ' + p.d +
                                    '), голос — VLAN <b>' + p.v + '</b> с тегом.'; },
        sol: function (p) { return ['configure', 'vlan ' + p.d, 'vlan ' + p.v, 'exit', 'interface gigabitethernet 1/0/' + p.g, 'switchport mode general',
                                    'switchport general allowed vlan add ' + p.d + ' untagged', 'switchport general pvid ' + p.d,
                                    'switchport general allowed vlan add ' + p.v + ' tagged', 'end']; },
        checks: function (p) { var k = 'gi1/0/' + p.g; return [['gi1/0/' + p.g + ' в режиме general', function (s) { return s.ports[k].mode === 'general'; }],
                                       ['PVID ' + p.d + ', VLAN ' + p.d + ' untagged', function (s) { var q = s.ports[k]; return q.pvid === p.d && q.guntag.indexOf(p.d) >= 0; }],
                                       ['VLAN ' + p.v + ' tagged', function (s) { return s.ports[k].gtag.indexOf(p.v) >= 0; }]]; },
        send: function (p, s) { return sendGeneral(s, p.g, p.d, p.v); } },
      { gen: function () { return { p: rnd(1, 20), v: pick([10, 20, 30]) }; },
        text: function (p) { return 'Порт <b>gi1/0/' + p.p + '</b> сейчас в VLAN ' + p.v + ' (уже настроено). Удалите его из VLAN командой ' +
                                    '<b>no switchport access vlan</b> и проверьте show vlan — порт должен вернуться в VLAN 1.'; },
        setup: function (p, s) { s.vlans[p.v] = '-'; s.ports['gi1/0/' + p.p].access = p.v; },
        sol: function (p) { return ['configure', 'interface gigabitethernet 1/0/' + p.p, 'no switchport access vlan', 'end', 'show vlan']; },
        checks: function (p) { return [['gi1/0/' + p.p + ' вернулся в VLAN 1', function (s) { return s.ports['gi1/0/' + p.p].access === 1; }]]; } }
    ]
  };

  // ------------------------------------------------------------------ мини-проверки отправки
  function pv(s, n) { var p = s.ports['gi1/0/' + n]; return p.mode === 'access' ? p.access : (p.mode === 'general' ? p.pvid : p.native); }
  function sendAccess(s, a, b) {
    var va = pv(s, a), vb = pv(s, b), ok = va === vb;
    return [{ ok: ok, t: 'Кадр gi1/0/' + a + ' (VLAN ' + va + ') → gi1/0/' + b + ' (VLAN ' + vb + '): ' +
             (ok ? 'доставлен — один широковещательный домен' : 'не доставлен — порты в разных VLAN') }];
  }
  function sendTrunk(s, t, vls) {
    var p = s.ports['gi1/0/' + t];
    return vls.map(function (v) {
      if (p.mode !== 'trunk') return { ok: false, t: 'VLAN ' + v + ': порт gi1/0/' + t + ' не транк — тегированный кадр отброшен' };
      if (v === p.native) return { ok: true, t: 'VLAN ' + v + ': нативная — кадр уходит БЕЗ тега' };
      if (p.allowed.indexOf(v) >= 0) return { ok: true, t: 'VLAN ' + v + ': разрешена — кадр уходит с тегом 802.1Q VID ' + v };
      return { ok: false, t: 'VLAN ' + v + ': не в списке allowed — кадр отброшен', exp: true };
    });
  }
  function sendGeneral(s, g, d, v) {
    var p = s.ports['gi1/0/' + g];
    if (p.mode !== 'general') return [{ ok: false, t: 'Порт gi1/0/' + g + ' не в режиме general' }];
    return [{ ok: p.pvid === d && p.guntag.indexOf(d) >= 0, t: 'Кадр ПК без тега → помещается в PVID ' + p.pvid + (p.pvid === d ? ' (VLAN данных) ✓' : ' — ожидалась VLAN ' + d) },
            { ok: p.gtag.indexOf(v) >= 0, t: 'Голосовой кадр с тегом VID ' + v + (p.gtag.indexOf(v) >= 0 ? ' — принят' : ' — отброшен: VLAN не разрешена tagged') }];
  }
  function loginView(s) {
    var o = [];
    if (s.banner.motd) o.push(s.banner.motd, '');
    if (s.banner.login) o.push(s.banner.login, '');
    o.push('User Name:' + (Object.keys(s.users)[0] || 'admin'), 'Password:********', '');
    if (s.banner.exec) o.push(s.banner.exec, '');
    o.push(s.host + '#');
    return o.join('\n');
  }

  // ------------------------------------------------------------------ виджет
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function init(box) {
    var deck = box.dataset.deck, pool = (box.dataset.pool || '').split(',').map(Number);
    var out = box.querySelector('.cs-out'), inp = box.querySelector('.cs-in input'), pr = box.querySelector('.cs-pr');
    var taskEl = box.querySelector('.cs-task'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol');
    var sendB = box.querySelector('[data-cs=send]');
    var st, T, P, hist = [], hi = 0, last = -1;
    function print(t, cls) { var d = document.createElement('div'); d.className = cls || ''; d.innerHTML = esc(t); out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function newTask() {
      var k; do { k = pool[rnd(0, pool.length - 1)]; } while (pool.length > 1 && k === last); last = k;
      T = TASKS[deck][k]; P = T.gen(); st = fresh(); if (T.setup) T.setup(P, st);
      taskEl.innerHTML = T.text(P); res.innerHTML = ''; sol.style.display = 'none';
      sol.textContent = T.sol(P).join('\n');
      out.innerHTML = ''; print('Console baud-rate auto detection is enabled. Подключение установлено.', 'cs-sys');
      pr.textContent = prompt(st);
      sendB.style.display = (T.send || T.login) ? '' : 'none';
      sendB.textContent = T.login ? 'Подключиться заново' : 'Отправить кадр';
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        var v = inp.value; print(prompt(st) + v, 'cs-cmd'); hist.push(v); hi = hist.length;
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
        if (T.login) { print('--- новое подключение к консоли ---', 'cs-sys'); print(loginView(st)); return; }
        var r = T.send(P, st);
        res.innerHTML = '<div class="cs-send">' + r.map(function (x) {
          return '<div class="' + (x.ok ? 'ok' : (x.exp ? 'exp' : 'no')) + '"><span class="env">✉</span> ' + esc(x.t) + '</div>'; }).join('') + '</div>';
      }
    });
    newTask();
  }
  // движок открыт наружу — его переиспользует отдельный эмулятор eltex-cli.html
  var api = { NPORTS: NPORTS, longIf: longIf, portGroups: portGroups, PFX: PFX, CMDS: CMDS, cmd: cmd, match: match, fresh: fresh, exec: exec, prompt: prompt, PROMPT: PROMPT,
              normLine: normLine, parseList: parseList, fmtList: fmtList, uniq: uniq, ifList: ifList, hash: hash,
              showRun: showRun, RUNX: RUNX, PORTX: PORTX, showVlan: showVlan, showSw: showSw, addShow: addShow, TASKS: TASKS, rnd: rnd, pick: pick,
              pv: pv, sendAccess: sendAccess, sendTrunk: sendTrunk, sendGeneral: sendGeneral, loginView: loginView, CFG: CFG };
  if (typeof window !== 'undefined') window.EltexCLI = api;
  if (typeof module !== 'undefined') module.exports = api;
  if (typeof document !== 'undefined') document.querySelectorAll('.clisim').forEach(init);
})();
