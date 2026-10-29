/* MikroTik RouterOS v7 в эмуляторе — спецификация sources/mikrotik/spec/routeros.md (help.mikrotik.com: CLI, Console, Bridge VLAN Table,
   VLAN, IP Routing, DHCP, NAT, Filter, OSPF, RIP). Устройство — тип 'esr' модели (маршрутизатор); мост RouterOS собирается из bridge-group
   модели ESR: без vlan-filtering — один L2-домен портов, с vlan-filtering=yes — по домену на VLAN (pvid → нетегированный порт,
   tagged → подынтерфейс порта с тегом), /interface vlan на мосту — L3-адрес этого домена, на ether — подынтерфейс (router-on-a-stick).
   CLI: приглашение v7 «[admin@MikroTik] /ip/address>», путь через пробел или «/», «..» — вверх, «/» — в корень; команды меню
   add / set / remove / enable / disable / print [detail] / export; номера # выдаёт print; имена и [find …] вместо номеров; сокращения слов.
   Ошибки — только документированные тексты: «bad command name X (line 1 column N)», «syntax error (line 1 column N)».
   Firewall filter: цепочки input/forward, action accept/drop/reject, connection-state, connection-nat-state, interface-list; без правил — accept.
   Упрощения (в отчёте): схема начинается без defconf (как после reset-configuration no-defaults=yes); на интерфейсе учитывается первый адрес;
   RSTP моста не моделируется (кольцо через мосты MikroTik даёт шторм); DHCP-клиент RouterOS не моделируется; SwOS — нет. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip;
  var GROUP = 'MikroTik (RouterOS)';
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  [['CHR', range('ether', 1, 4), 'Cloud Hosted Router: виртуальный маршрутизатор RouterOS v7, 4 × ether (число NIC задаёт гипервизор)'],
   ['hEX RB750Gr3', range('ether', 1, 5), 'MikroTik hEX (RB750Gr3): 5 × Gigabit Ethernet ether1–ether5, RouterOS v7'],
   ['RB4011iGS+RM', range('ether', 1, 10).concat(['sfp-sfpplus1']), 'MikroTik RB4011iGS+RM: 10 × Gigabit Ethernet ether1–ether10 + SFP+, RouterOS v7'],
   ['CRS326-24G-2S+', range('ether', 1, 24).concat(['sfp-sfpplus1', 'sfp-sfpplus2']), 'MikroTik CRS326-24G-2S+ в режиме RouterOS: 24 × ether + 2 × SFP+ (коммутация — мостом)']
  ].forEach(function (x) { EL.MODELS[x[0]] = { type: 'esr', kind: 'ros', portList: x[1], ports: x[1].length, group: GROUP, vendor: 'mikrotik', host: 'MikroTik', note: x[2],
    login: [{ u: 'admin', p: '(пустой)', a: 'консоль; у новых устройств пароль — на наклейке' }] }; });
  function isRos(d) { return !!d && d.sub === 'ros'; }

  // ---------------------------------------------------------------- меню
  // L — список элементов (add/set/remove/print), S — одиночные настройки (set/print); key — свойство-имя для ссылок по имени
  var MENU = {
    'interface': { L: 1, sys: true, key: 'name' }, 'interface ethernet': { L: 1, sys: true, key: 'name' },
    'interface bridge': { L: 1, key: 'name', def: { 'vlan-filtering': 'no', 'protocol-mode': 'rstp', pvid: '1' } }, 'interface bridge port': { L: 1, def: { pvid: '1' } },
    'interface bridge vlan': { L: 1 }, 'interface vlan': { L: 1, key: 'name' }, 'interface list': { L: 1, key: 'name' }, 'interface list member': { L: 1 },
    'ip address': { L: 1 }, 'ip route': { L: 1, def: { distance: '1' } }, 'ip pool': { L: 1, key: 'name' }, 'ip dhcp-server': { L: 1, key: 'name', def: { 'lease-time': '30m' } },
    'ip dhcp-server network': { L: 1 }, 'ip dhcp-client': { L: 1 }, 'ip firewall filter': { L: 1 }, 'ip firewall nat': { L: 1 }, 'ip dns': { S: 1 }, 'ip neighbor': { L: 1, sys: true },
    'routing ospf instance': { L: 1, key: 'name' }, 'routing ospf area': { L: 1, key: 'name' }, 'routing ospf interface-template': { L: 1 }, 'routing ospf neighbor': { L: 1, sys: true },
    'routing rip instance': { L: 1, key: 'name' }, 'routing rip interface-template': { L: 1 }, 'system identity': { S: 1 }, 'user': { L: 1, key: 'name' }, 'system resource': { S: 1, sys: true }
  };
  var DIRS = ['interface', 'ip', 'ip firewall', 'ip dhcp-server', 'routing', 'routing ospf', 'routing rip', 'system', 'interface bridge', 'interface list', 'tool'];
  function children(path) { var p = path.join(' '), o = []; Object.keys(MENU).concat(DIRS).forEach(function (k) { var w = k.split(' ');
    if (w.length === path.length + 1 && (path.length === 0 || k.indexOf(p + ' ') === 0) && o.indexOf(w[w.length - 1]) < 0) o.push(w[w.length - 1]); }); return o; }
  function uniq(cands, w) { var ex = cands.filter(function (c) { return c === w; }); if (ex.length) return ex[0]; var m = cands.filter(function (c) { return c.indexOf(w) === 0; }); return m.length === 1 ? m[0] : null; }
  var CMDS = ['add', 'set', 'remove', 'print', 'export', 'enable', 'disable', 'find', 'edit', 'comment'];

  // ---------------------------------------------------------------- состояние
  function R(st) { return st.ros; }
  function C(st) { return st.ros.c; }
  function list(st, m) { var c = C(st); c.L = c.L || {}; return c.L[m] || (c.L[m] = []); }
  function single(st, m) { var c = C(st); c.S = c.S || {}; return c.S[m] || (c.S[m] = {}); }
  function ports(st) { var net = st.net, d = net && net.devs[st.dev]; return d ? net.portsOf(d).filter(function (p) { return /^(ether|sfp)/.test(p); }) : []; }
  function identity(st) { return single(st, 'system identity').name || 'MikroTik'; }
  function prompt(st) { var x = R(st); if (x.ask) return x.ask.pr; return '[' + (x.user || 'admin') + '@' + identity(st) + '] ' + (x.path.length ? '/' + x.path.join('/') : '') + '>'; }

  // ---------------------------------------------------------------- разбор строки
  function toks(line) { var o = [], re = /("([^"\\]|\\.)*"|\[[^\]]*\]|\S+)/g, m; while ((m = re.exec(line))) o.push(m[0]); return o; }
  function unq(v) { return /^".*"$/.test(v) ? v.slice(1, -1) : v; }
  function err(kind, line, w) { var col = Math.max(1, String(line).indexOf(w) + 1); return kind === 'bad' ? 'bad command name ' + w + ' (line 1 column ' + col + ')' : 'syntax error (line 1 column ' + col + ')'; }
  function exec(st, raw) {
    var x = R(st); if (x.ask) { var a = x.ask; x.ask = null; return a.fn(raw); }
    var line = String(raw).trim(); if (!line) return '';
    if (/\?$/.test(line)) return help(st, line.replace(/\?$/, ''));
    var T = [], abs = false, i = 0;                // «/ip/address/add», «/ip address add», «ip address», «..»
    toks(line).forEach(function (t, j) {
      if (/=|^\[|^"/.test(t)) { T.push(t); return; }
      if (j === 0 && t.charAt(0) === '/') { abs = true; t = t.slice(1); }
      if (/^[a-z0-9-]+(\/[a-z0-9-]*)+$/.test(t)) t.split('/').filter(Boolean).forEach(function (q) { T.push(q); }); else if (t) T.push(t); });
    var path = abs ? [] : x.path.slice();
    for (; i < T.length; i++) { var t = T[i];
      if (t === '..') { path.pop(); continue; } if (t === '/') { path = []; continue; }
      if (/=/.test(t)) break;
      var ch = uniq(children(path), t); if (ch) { path.push(ch); continue; }
      break; }
    if (i >= T.length) { if (!MENU[path.join(' ')] && DIRS.indexOf(path.join(' ')) < 0 && path.length) return err('bad', line, T[T.length - 1]); x.path = path; return ''; }
    var w = T[i], rest = T.slice(i + 1), m = path.join(' ');
    if (w === 'ping' || w === 'traceroute' || !path.length) {   // команды корня: ping, traceroute, export, password, quit
      var rc = uniq(['ping', 'quit', 'export', 'password', 'traceroute'], w);
      if (rc === 'ping') return ping(st, rest); if (rc === 'traceroute') return trace(st, rest); if (rc === 'export' && !path.length) return exportAll(st); if (rc === 'quit') return '';
      if (rc === 'password') return passwd(st);
      if (!path.length) return err('bad', line, w);
    }
    if (m === 'tool' && uniq(['traceroute', 'ping'], w) === 'traceroute') return trace(st, rest);
    if (m === 'system' && uniq(['reboot', 'reset-configuration', 'identity'], w) === 'reboot') { x.ask = { pr: '', fn: function (s) { if (/^y/i.test(s) && st.net) st.net.reboot(st.dev); return ''; } }; return 'Reboot, yes? [y/N]: '; }
    var M = MENU[m]; if (!M) return err('bad', line, w);
    var cmd = uniq(CMDS.concat(m === 'ip dhcp-server' ? ['setup'] : []), w); if (!cmd) return err('bad', line, w);
    var r = run(st, m, M, cmd, rest, line);
    if (r === null) return err('syntax', line, rest[rest.length - 1] || w);
    if (cmd !== 'print' && cmd !== 'export' && cmd !== 'find') compile(st);
    return r === undefined ? '' : r;
  }
  function kv(st, m, rest) { var o = {}, bad = false; rest.forEach(function (t) { var mm = t.match(/^([a-z0-9-]+)=(.*)$/); if (!mm) { bad = true; return; } o[mm[1]] = unq(mm[2]); }); return bad ? null : o; }
  function items(st, m) { var M = MENU[m]; if (M.sys) return sysItems(st, m); return list(st, m); }
  function sel(st, m, ref) {                      // номера 0,1,2 | имя | [find where …] | [find key=val]
    var L = items(st, m), M = MENU[m], nums = (R(st).nums || {})[m] || L.map(function (e, i) { return i; });
    if (/^\[find/.test(ref)) { var f = ref.replace(/^\[find\s*(where\s*)?/, '').replace(/\]$/, '').trim(), conds = toks(f).map(function (t) { var q = t.match(/^([a-z0-9-]+)=(.*)$/); return q ? [q[1], unq(q[2])] : null; }).filter(Boolean);
      return L.filter(function (e) { return conds.every(function (c) { return String(e[c[0]]) === c[1]; }); }); }
    if (/^[\d,]+$/.test(ref)) { var o = []; ref.split(',').forEach(function (n) { var k = nums[+n]; if (k !== undefined && L[k]) o.push(L[k]); }); return o.length ? o : null; }
    var byName = L.filter(function (e) { return M.key && e[M.key] === unq(ref); }); return byName.length ? byName : null;
  }
  function run(st, m, M, cmd, rest, line) {
    if (cmd === 'print') return print(st, m, rest);
    if (cmd === 'export') return exportMenu(st, m);
    if (M.S) { if (cmd !== 'set') return null; var p = kv(st, m, rest); if (!p) return null; var S = single(st, m); Object.keys(p).forEach(function (k) { S[k] = p[k]; }); return; }
    if (cmd === 'add') { if (M.sys) return null; var q = kv(st, m, rest); if (!q) return null; var v = validate(st, m, q); if (v !== true) return v;
      var e = Object.assign({}, M.def || {}, q); if (M.key && !e[M.key]) e[M.key] = autoName(st, m); list(st, m).push(e); return; }
    if (cmd === 'set' || cmd === 'remove' || cmd === 'enable' || cmd === 'disable' || cmd === 'comment') {
      if (!rest.length) return null; var ref = rest[0], es = sel(st, m, ref); if (!es || !es.length) return null;
      if (cmd === 'remove') { if (M.sys) return null; var L = list(st, m); es.forEach(function (e) { var k = L.indexOf(e); if (k >= 0) L.splice(k, 1); }); return; }
      if (cmd === 'enable' || cmd === 'disable') { es.forEach(function (e) { setProp(st, m, e, 'disabled', cmd === 'disable' ? 'yes' : 'no'); }); return; }
      var pr = kv(st, m, rest.slice(1)); if (!pr) return null;
      es.forEach(function (e) { Object.keys(pr).forEach(function (k) { setProp(st, m, e, k, pr[k]); }); }); return; }
    return null;
  }
  function setProp(st, m, e, k, v) { if (MENU[m].sys) { var c = C(st), o = (c.ifp = c.ifp || {}); (o[e.name] = o[e.name] || {})[k] = v; return; } e[k] = v; }
  function autoName(st, m) { var base = { 'interface bridge': 'bridge', 'interface vlan': 'vlan', 'ip pool': 'pool', 'ip dhcp-server': 'dhcp', 'routing ospf instance': 'ospf-instance-', 'routing ospf area': 'ospf-area-',
    'routing rip instance': 'rip-instance-', 'interface list': 'list', 'user': 'user' }[m] || 'item'; var n = 1; while (list(st, m).some(function (e) { return e[MENU[m].key] === base + n; })) n++; return base + n; }
  function ifaceNames(st) { return ports(st).concat(list(st, 'interface bridge').map(function (b) { return b.name; }), list(st, 'interface vlan').map(function (v) { return v.name; })); }
  function validate(st, m, q) {                   // ссылки на интерфейсы должны существовать
    var bad = ['interface', 'bridge', 'out-interface', 'in-interface'].filter(function (k) { return q[k] && ifaceNames(st).indexOf(q[k]) < 0; })[0];
    if (bad) return 'input does not match any value of ' + bad;   // текст API (routeros.md §2.6)
    if (q.address && m === 'ip address' && !IP.parseCidr(q.address)) return null;
    return true;
  }
  function sysItems(st, m) {
    var ifp = C(st).ifp || {};
    if (m === 'interface' || m === 'interface ethernet') { var o = ports(st).map(function (p) { return Object.assign({ name: p, type: 'ether', mtu: '1500' }, ifp[p] || {}); });
      if (m === 'interface') { list(st, 'interface bridge').forEach(function (b) { o.push({ name: b.name, type: 'bridge', mtu: 'auto', disabled: b.disabled }); });
        list(st, 'interface vlan').forEach(function (v) { o.push({ name: v.name, type: 'vlan', mtu: '1500', disabled: v.disabled }); }); } return o; }
    if (m === 'ip neighbor') return neighbors(st);
    if (m === 'routing ospf neighbor') return ospfNb(st);
    return [];
  }

  // ---------------------------------------------------------------- print / export
  function pad(s, n) { s = String(s === undefined ? '' : s); return s.length >= n ? s + ' ' : (s + new Array(n + 1).join(' ')).slice(0, n); }
  var FLAGS = { 'interface': 'Flags: X - disabled, D - dynamic, R - running', 'interface bridge': 'Flags: X - disabled, R - running', 'interface bridge port': 'Flags: X - disabled, I - inactive, D - dynamic, H - hw-offload',
    'interface bridge vlan': 'Flags: X - disabled, D - dynamic', 'interface vlan': 'Flags: X - disabled, R - running, S - slave', 'ip address': 'Flags: X - disabled, I - invalid, D - dynamic',
    'ip firewall filter': 'Flags: X - disabled, I - invalid; D - dynamic', 'ip firewall nat': 'Flags: X - disabled, I - invalid; D - dynamic', 'user': 'Flags: X - disabled', 'ip dhcp-client': 'Flags: X - disabled, I - invalid' };
  function print(st, m, rest) {
    var M = MENU[m], detail = rest.some(function (t) { return /^d(e(t(a(il?)?)?)?)?$/.test(t); }), x = R(st);
    if (m === 'ip route') return routePrint(st);
    if (M.S) { var S = single(st, m); if (m === 'system identity') return 'name: ' + identity(st);
      if (m === 'system resource') return '  uptime: ' + Math.floor(((st.net && st.net.now) || 0) / 60) + 'm\n  version: 7.16 (stable)\n  board-name: ' + ((st.net && st.net.devs[st.dev].model) || '');
      return Object.keys(S).map(function (k) { return pad(k + ':', 22) + S[k]; }).join('\n'); }
    var L = items(st, m); (x.nums = x.nums || {})[m] = L.map(function (e, i) { return i; });
    var o = FLAGS[m] ? [FLAGS[m]] : [];
    var COLS = { 'interface': [['NAME', 'name', 21], ['TYPE', 'type', 17], ['MTU', 'mtu', 6]], 'ip address': [['ADDRESS', 'address', 19], ['NETWORK', 'network', 16], ['INTERFACE', 'interface', 12]],
      'interface bridge port': [['INTERFACE', 'interface', 16], ['BRIDGE', 'bridge', 13], ['PVID', 'pvid', 5]], 'interface bridge vlan': [['BRIDGE', 'bridge', 27], ['VLAN-IDS', 'vlan-ids', 10], ['CURRENT-TAGGED', 'tagged', 21], ['CURRENT-UNTAGGED', 'untagged', 16]],
      'interface vlan': [['NAME', 'name', 22], ['MTU', 'mtu', 6], ['ARP', 'arp', 11], ['VLAN-ID', 'vlan-id', 8], ['INTERFACE', 'interface', 12]], 'ip pool': [['NAME', 'name', 44], ['RANGES', 'ranges', 20]],
      'ip neighbor': [['INTERFACE', 'interface', 10], ['ADDRESS', 'address', 16], ['MAC-ADDRESS', 'mac', 18], ['IDENTITY', 'identity', 11], ['VERSION', 'version', 11], ['BOARD', 'board', 10]],
      'routing ospf neighbor': [['INSTANCE', 'instance', 10], ['AREA', 'area', 13], ['ADDRESS', 'address', 16], ['ROUTER-ID', 'router-id', 16], ['STATE', 'state', 10]] }[m];
    if (COLS && !detail) { o.push(' #   ' + COLS.map(function (c) { return pad(c[0], c[2]); }).join('').replace(/\s+$/, ''));
      L.forEach(function (e, i) { var fl = (e.disabled === 'yes' ? 'X' : '') + (m === 'interface' || m === 'interface bridge' || m === 'interface vlan' ? (e.disabled === 'yes' ? '' : running(st, e.name) ? 'R' : '') : '');
        var ee = Object.assign({}, e); if (m === 'ip address' && e.address) { var cc = IP.parseCidr(e.address); ee.network = cc ? IP.netOf(cc.ip, cc.len).split('/')[0] : ''; }
        if (m === 'interface vlan') { ee.mtu = '1500'; ee.arp = 'enabled'; }
        o.push(pad(' ' + i, 3) + pad(fl, 2) + COLS.map(function (c) { return pad(ee[c[1]], c[2]); }).join('').replace(/\s+$/, '')); });
      return o.join('\n'); }
    L.forEach(function (e, i) { o.push(pad(i, 3) + (e.disabled === 'yes' ? 'X ' : '  ') + Object.keys(e).filter(function (k) { return k !== 'disabled'; }).map(function (k) { return k + '=' + (/[\s]/.test(e[k]) ? '"' + e[k] + '"' : e[k]); }).join(' ')); });
    return o.join('\n');
  }
  function running(st, name) { var net = st.net; if (!net) return false; if (/^(ether|sfp)/.test(name)) return net.linkUp(st.dev, name);
    return true; }
  function routePrint(st) {
    var net = st.net; if (!net) return ''; var all = net.routes(st.dev), by = net.best(st.dev, all), o = ['Flags: D - dynamic; X - disabled, I - inactive, A - active; C - connect, S - static, r - rip, b - bgp, o - ospf, d - dhcp, v - vpn',
      'Columns: DST-ADDRESS, GATEWAY, DISTANCE', '#     DST-ADDRESS        GATEWAY            DISTANCE'], stat = list(st, 'ip route'), n = 0;
    all.filter(function (r) { return r.p !== 'S'; }).concat(stat.map(function (s) { return all.filter(function (r) { return r.p === 'S' && r.net === norm(s['dst-address'] || '0.0.0.0/0') && r.nh === s.gateway; })[0] || { p: 'S', net: norm(s['dst-address'] || '0.0.0.0/0'), nh: s.gateway, ad: +(s.distance || 1), dead: true }; }))
      .forEach(function (r) { var act = !r.dead && by[r.net] === r, code = r.p === 'C' ? 'C' : r.p === 'S' ? 'S' : r.p === 'O' ? 'o' : r.p === 'R' ? 'r' : r.p;
        var num = r.p === 'S' ? pad(n++, 2) : '  ', fl = (r.p === 'S' ? '' : 'D') + (act ? 'A' : 'I') + code;
        o.push(num + pad(fl, 4) + pad(r.net, 19) + pad(r.p === 'C' ? alias(st, r.ifn) : r.nh + (r.p !== 'S' ? '%' + alias(st, r.ifn) : ''), 19) + (r.p === 'C' ? 0 : r.cad || r.ad)); });
    return o.join('\n');
  }
  function norm(n) { var c = IP.parseCidr(n); return c ? IP.netOf(c.ip, c.len) : n; }
  var ORDER = ['interface bridge', 'interface vlan', 'interface list', 'interface bridge port', 'interface bridge vlan', 'interface list member', 'ip address', 'ip pool', 'ip dhcp-server', 'ip dhcp-server network',
    'ip dhcp-client', 'ip dns', 'ip firewall filter', 'ip firewall nat', 'ip route', 'routing ospf instance', 'routing ospf area', 'routing ospf interface-template', 'routing rip instance', 'routing rip interface-template', 'system identity'];
  function line(e) { return Object.keys(e).filter(function (k) { return !(k === 'disabled' && e[k] === 'no'); }).map(function (k) { return k + '=' + (/[\s]/.test(e[k]) ? '"' + e[k] + '"' : e[k]); }).join(' '); }
  function exportMenu(st, m) { var M = MENU[m]; if (M.S) { var S = single(st, m); return Object.keys(S).length ? '/' + m + '\nset ' + line(S) : ''; }
    var L = list(st, m), D = M.def || {}; if (!L.length) return ''; return '/' + m + '\n' + L.map(function (e) { var o = {}; Object.keys(e).forEach(function (k) { if (D[k] !== e[k]) o[k] = e[k]; }); return 'add ' + line(o); }).join('\n'); }
  function exportAll(st) { var d = new Date(); return ['# ' + d.toISOString().slice(0, 19).replace('T', ' ') + ' by RouterOS 7.16', '# software id = ' + softId(st), '#'].concat(ORDER.map(function (m) { return exportMenu(st, m); }).filter(Boolean)).join('\n'); }
  function softId(st) { var s = String(st.dev || 'x'), h = 0; for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; var a = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; var o = ''; for (var k = 0; k < 8; k++) { o += a[h % 32]; h = Math.floor(h / 32) + 7 * k; } return o.slice(0, 4) + '-' + o.slice(4); }
  function help(st, txt) { var p = R(st).path; return children(p).concat(MENU[p.join(' ')] ? CMDS : []).map(function (w) { return '  ' + w; }).join('\n'); }
  function passwd(st) { var x = R(st); x.ask = { pr: 'old-password: ', fn: function () { x.ask = { pr: 'new-password: ', fn: function (n) { x.ask = { pr: 'confirm-new-password: ', fn: function (c) {
    if (c !== n) return 'passwords do not match'; var u = list(st, 'user').filter(function (e) { return e.name === (x.user || 'admin'); })[0]; if (u) u.password = n; else x.adminPw = n; return ''; } }; return ''; } }; return ''; } }; return ''; }

  // ---------------------------------------------------------------- ping / traceroute (PING, TR)
  function ping(st, rest) {
    var net = st.net, dst = rest[0], cnt = 4; rest.slice(1).forEach(function (t, i) { var m = t.match(/^count=(\d+)$/); if (m) cnt = Math.min(+m[1], 20); if (/^c(o(u(nt?)?)?)?$/.test(t) && /^\d+$/.test(rest[i + 2] || '')) cnt = +rest[i + 2]; });
    if (!net || !dst || IP.ip2n(dst) === null) return null;
    var r = net.ping(st.dev, dst); if (net.onTrace) net.onTrace(r, st.dev, dst);
    var o = ['  SEQ HOST                                     SIZE TTL TIME  STATUS'], got = 0, ttl = 64 - (r.hops || []).length;
    for (var i = 0; i < cnt; i++) { if (r.ok) { got++; o.push('    ' + i + ' ' + pad(dst, 41) + '56  ' + pad(ttl, 3) + ' ' + (i % 3) + 'ms'); } else o.push('    ' + i + ' ' + pad(dst, 41) + '                timeout'); }
    o.push('    sent=' + cnt + ' received=' + got + ' packet-loss=' + Math.round((cnt - got) * 100 / cnt) + '%' + (got ? ' min-rtt=0ms avg-rtt=1ms max-rtt=2ms' : ''));
    return o.join('\n');
  }
  function trace(st, rest) { var net = st.net, dst = rest[0]; if (!net || IP.ip2n(dst || '') === null) return null; var r = net.ping(st.dev, dst), hops = (r.hops || []).map(function (h) { return h.ip; }); if (r.ok) hops.push(dst);
    return ['     ADDRESS                                    STATUS'].concat(hops.map(function (ip, i) { return pad('   ' + (i + 1), 8) + ('                ' + ip).slice(-16) + ' 1ms 1ms 1ms'; })).join('\n'); }

  // ---------------------------------------------------------------- compile: RouterOS → модель ESR
  function alias(st, k) { var a = (R(st).alias || {})[String(k || '').split(':')[0]]; return a || k; }
  function cidrRange(n) { var c = IP.parseCidr(n); if (!c) { return IP.ip2n(n) !== null ? [n, n] : null; } var lo = IP.ip2n(IP.netOf(c.ip, c.len).split('/')[0]); return [IP.n2ip(lo), IP.n2ip((lo + Math.pow(2, 32 - c.len) - 1) >>> 0)]; }
  function compile(st) {
    var run = st.run, c = C(st), ifp = c.ifp || {}, al = {}, key = {};
    var ifs = {}; Object.keys(run.ifs).forEach(function (k) { if (!/^(ether|sfp)/.test(k)) ifs[k] = run.ifs[k]; });
    ports(st).forEach(function (p) { ifs[p] = { ip: null, fw: true, shut: (ifp[p] || {}).disabled === 'yes', ros: true }; key[p] = p; });
    run.bridges = {}; var bgN = 0;
    list(st, 'interface bridge').forEach(function (b, bi) { var vf = b['vlan-filtering'] === 'yes', mem = list(st, 'interface bridge port').filter(function (q) { return q.bridge === b.name && q.disabled !== 'yes'; });
      if (!vf) { var N = ++bgN; run.bridges[N] = { on: b.disabled !== 'yes', ip: null, fw: true }; key[b.name] = 'bridge' + N; al['bridge' + N] = b.name;
        mem.forEach(function (q) { if (ifs[q.interface]) ifs[q.interface].bg = N; }); return; }
      var vl = {}, add = function (v) { v = +v; if (!vl[v]) { vl[v] = ++bgN; run.bridges[vl[v]] = { on: true, ip: null, fw: true }; al['bridge' + vl[v]] = b.name + (v === +(b.pvid || 1) ? '' : '.' + v); } return vl[v]; };
      mem.forEach(function (q) { if (ifs[q.interface]) ifs[q.interface].bg = add(q.pvid || 1); });
      list(st, 'interface bridge vlan').filter(function (e) { return e.bridge === b.name; }).forEach(function (e) {
        String(e['vlan-ids'] || '').split(',').forEach(function (v) { if (!/^\d+$/.test(v)) return; var N = add(v);
          String(e.tagged || '').split(',').filter(Boolean).forEach(function (t) { if (t === b.name || !ifs[t]) return; ifs[t + '.' + v] = { ip: null, fw: true, shut: false, bg: N }; });
          void e.untagged; }); });   // нетегированный порт попадает в VLAN по своему PVID (входящие кадры), список untagged его не меняет
      key[b.name] = 'bridge' + add(b.pvid || 1); b._vl = vl; });
    list(st, 'interface vlan').forEach(function (v) { var on = list(st, 'interface bridge').filter(function (b) { return b.name === v.interface; })[0];
      if (on) { var N = on['vlan-filtering'] === 'yes' && on._vl && on._vl[+v['vlan-id']] ? on._vl[+v['vlan-id']] : null; if (N) { key[v.name] = 'bridge' + N; al['bridge' + N] = v.name; } return; }
      if (ifs[v.interface]) { var k = v.interface + '.' + v['vlan-id']; ifs[k] = { ip: null, fw: true, shut: v.disabled === 'yes' }; key[v.name] = k; al[k] = v.name; } });
    list(st, 'ip address').forEach(function (a) { if (a.disabled === 'yes') return; var k = key[a.interface], cc = IP.parseCidr(a.address || ''); if (!k || !cc) return;
      var b = k.match(/^bridge(\d+)$/); if (b) { if (!run.bridges[b[1]].ip) run.bridges[b[1]].ip = cc.ip + '/' + cc.len; } else if (ifs[k] && !ifs[k].ip) ifs[k].ip = cc.ip + '/' + cc.len; });
    run.ifs = ifs; run.host = identity(st); R(st).alias = al; R(st).key = key;
    run.routes = list(st, 'ip route').filter(function (r) { return r.disabled !== 'yes' && IP.ip2n(r.gateway || '') !== null; }).map(function (r) { return { net: norm(r['dst-address'] || '0.0.0.0/0'), nh: r.gateway, ad: +(r.distance || 1) }; });
    // DHCP-сервер: пул + сеть по интерфейсу сервера
    var pools = {}; list(st, 'ip dhcp-server').forEach(function (s) { if (s.disabled === 'yes') return; var pl = list(st, 'ip pool').filter(function (p) { return p.name === s['address-pool']; })[0]; if (!pl) return;
      var r0 = String(pl.ranges || '').split(',')[0].split('-'); var n0 = list(st, 'ip dhcp-server network').filter(function (n) { var cc = IP.parseCidr(n.address || ''); return cc && IP.sameNet(r0[0], cc.ip, cc.len); })[0];
      if (!n0) return; var cc = IP.parseCidr(n0.address); pools[s.name] = { net: IP.netOf(cc.ip, cc.len), range: [r0[0], r0[1] || r0[0]], gw: n0.gateway || null, dns: (n0['dns-server'] || '').split(',')[0] || null, lease: null }; });
    run.dhcp = Object.keys(pools).length ? { on: true, pools: pools } : null;
    // NAT
    run.snat = null; run.dnat = null; var lists = memberLists(st);
    list(st, 'ip firewall nat').forEach(function (r, i) { if (r.disabled === 'yes') return;
      var outs = r['out-interface'] ? [r['out-interface']] : r['out-interface-list'] ? (lists[r['out-interface-list']] || []) : r.chain === 'srcnat' ? Object.keys(key) : [];
      var ins = r['in-interface'] ? [r['in-interface']] : r['in-interface-list'] ? (lists[r['in-interface-list']] || []) : Object.keys(key);
      if (r.chain === 'srcnat' && /^(masquerade|src-nat)$/.test(r.action)) outs.forEach(function (o) { var k = key[o]; if (!k) return; run.snat = run.snat || { rulesets: {} };
        var rs = run.snat.rulesets['ros-' + k] = run.snat.rulesets['ros-' + k] || { ifn: k, rules: {} }; rs.rules[i + 1] = { on: true, act: 'interface', src: r['src-address'] ? cidrRange(r['src-address']) : null, dst: r['dst-address'] ? cidrRange(r['dst-address']) : null, proto: r.protocol || null }; });
      if (r.chain === 'dstnat' && r.action === 'dst-nat') ins.forEach(function (o) { var k = key[o]; if (!k) return; run.dnat = run.dnat || { rulesets: {} };
        var rs = run.dnat.rulesets['ros-' + k] = run.dnat.rulesets['ros-' + k] || { ifn: k, rules: {} }; var dp = r['dst-port'] || r.port;
        rs.rules[i + 1] = { on: true, to: r['to-addresses'] || r['to-address'], dst: r['dst-address'] ? cidrRange(r['dst-address']) : null, proto: r.protocol || null, dport: dp ? [+dp, +dp] : null }; }); });
    // OSPF v7: instance → area → interface-template (networks= или interfaces=)
    run.ospf = null; var inst = list(st, 'routing ospf instance').filter(function (x) { return x.disabled !== 'yes' && (x.version || '2') === '2'; })[0];
    if (inst) { var areas = {}; run.ospf = { id: 1, rid: inst['router-id'] || null, on: true, areas: areas, dra: inst['originate-default'] && inst['originate-default'] !== 'never' ? 'yes' : null };
      list(st, 'routing ospf interface-template').forEach(function (t) { var ar = list(st, 'routing ospf area').filter(function (a) { return a.name === t.area && a.instance === inst.name; })[0]; if (!ar) return; var aid = ar['area-id'] || '0.0.0.0';
        Object.keys(ifs).concat(Object.keys(run.bridges).map(function (b) { return 'bridge' + b; })).forEach(function (k) { var y = /^bridge/.test(k) ? null : ifs[k], ipl = y ? y.ip : (run.bridges[k.slice(6)] || {}).ip; if (!ipl || !y) return;
          var nm = alias(st, k), hit = t.interfaces ? String(t.interfaces).split(',').indexOf(nm) >= 0 : String(t.networks || t.network || '').split(',').some(function (n) { var cc = IP.parseCidr(n); return cc && IP.sameNet(ipl.split('/')[0], cc.ip, cc.len); });
          if (!hit || y.ospf) return; areas[aid] = { on: true };
          y.ospf = { on: true, inst: 1, area: aid, passive: t.passive === 'yes' || t.passive === '', cost: +(t.cost || 1), hello: 10, dead: 40, net: t.type === 'ptp' ? 'point-to-point' : 'broadcast', prio: +(t.priority || 128) }; }); }); }
    // RIP v7 (только RIPv2)
    run.rip = null; var ri = list(st, 'routing rip instance').filter(function (x) { return x.disabled !== 'yes'; })[0];
    if (ri) { var on = [], nets = []; list(st, 'routing rip interface-template').forEach(function (t) { String(t.interfaces || '').split(',').filter(Boolean).forEach(function (nm) { var k = key[nm]; if (k && ifs[k] && ifs[k].ip) { on.push(k); nets.push(IP.netOf(ifs[k].ip.split('/')[0], +ifs[k].ip.split('/')[1])); } }); });
      run.rip = { on: nets.length > 0, nets: nets, passive: Object.keys(ifs).filter(function (k) { return ifs[k].ip && on.indexOf(k) < 0; }), redist: String(ri.redistribute || '').split(',').filter(Boolean).map(function (w) { return w === 'connected' ? 'connected' : w; }), ver: 2 }; }
    st.cand = EL.clone(run);
    if (st.net) st.net.gen++;
  }
  function memberLists(st) { var o = {}; list(st, 'interface list member').forEach(function (m) { (o[m.list] = o[m.list] || []).push(m.interface); }); return o; }
  function neighbors(st) { var net = st.net; if (!net) return []; var o = [];
    ports(st).forEach(function (p) { var pr = net.peer(st.dev, p), d = pr && net.devs[pr.dev]; if (!d || !isRos(d) || d.off || !net.linkUp(st.dev, p)) return;
      var f = net.ifaces(d.id)[0]; o.push({ interface: p, address: f ? f.ip : '', mac: '', identity: identity(d.st), version: '7.16', board: d.model }); }); return o; }
  function ospfNb(st) { var net = st.net; if (!net || !st.run.ospf) return []; net.dyn(); var A = (net._adj || {}).O || {};
    return Object.keys(A).map(function (k) { return A[k]; }).filter(function (r) { return r.id === st.dev; }).map(function (r) { var y = st.run.ifs[r.ifn] || {};
      return { instance: 'v2inst', area: (y.ospf || {}).area, address: r.nh, 'router-id': (net.devs[r.dev].st.run.ospf || {}).rid || net.ifaces(r.dev).map(function (f) { return f.ip; }).sort(function (x, y) { return IP.ip2n(y) - IP.ip2n(x); })[0], state: r.state === 'full' ? 'Full' : r.state }; }); }

  // ---------------------------------------------------------------- firewall filter (FLT): input / forward, connection-state
  var fw0 = P.fwPass;
  P.fwPass = function (dev, iface, pk, ct, pre) {
    var d = this.devs[dev]; if (!isRos(d)) return fw0.apply(this, arguments);
    var s = this, st = d.st, alt = pre || {}, F = list(st, 'ip firewall filter').filter(function (r) { return r.disabled !== 'yes'; });
    var est = ct.some(function (x) { return x.kind === 'fw' && x.dev === dev && x.proto === pk.proto && (x.a.indexOf(pk.dst) >= 0 || x.a.indexOf(alt.dst) >= 0) && (x.b.indexOf(pk.src) >= 0 || x.b.indexOf(alt.src) >= 0); });
    var own = s.ifaces(dev).some(function (f) { return f.ip === pk.dst; }), chain = own ? 'input' : 'forward';
    var inN = alias(st, String(iface.name).split(':')[0]), r = own ? null : s.lookup(dev, pk.dst), outN = r ? alias(st, String(r.iface.name).split(':')[0]) : null, lists = memberLists(st);
    var dn = !!(alt.dst && alt.dst !== pk.dst), state = est ? 'established' : 'new';
    var hit = F.filter(function (q) { if (q.chain !== chain) return false;
      if (q['connection-state'] && String(q['connection-state']).split(',').indexOf(state) < 0) return false;
      if (q['connection-nat-state']) { var neg = /^!/.test(q['connection-nat-state']), v = q['connection-nat-state'].replace(/^!/, '') === 'dstnat' ? dn : false; if (neg ? v : !v) return false; }
      if (q.protocol && q.protocol !== pk.proto) return false;
      if (q['src-address'] && !inR(alt.src || pk.src, cidrRange(q['src-address']))) return false;
      if (q['dst-address'] && !inR(pk.dst, cidrRange(q['dst-address'])) && !inR(alt.dst || pk.dst, cidrRange(q['dst-address']))) return false;
      if (q['dst-port'] && +q['dst-port'] !== pk.dport) return false;
      if (q['in-interface'] && q['in-interface'] !== inN) return false;
      if (q['out-interface'] && q['out-interface'] !== outN) return false;
      if (q['in-interface-list']) { var ng = /^!/.test(q['in-interface-list']), inL = (lists[q['in-interface-list'].replace(/^!/, '')] || []).indexOf(inN) >= 0; if (ng ? inL : !inL) return false; }
      if (q['out-interface-list']) { var ng2 = /^!/.test(q['out-interface-list']), outL = (lists[q['out-interface-list'].replace(/^!/, '')] || []).indexOf(outN) >= 0; if (ng2 ? outL : !outL) return false; }
      return !q['ipsec-policy'] && q.action !== 'fasttrack-connection'; })[0];
    var act = hit ? hit.action : 'accept';
    if (act === 'accept' || act === 'passthrough') { if (!est) ct.push({ kind: 'fw', dev: dev, proto: pk.proto, a: [pk.src, alt.src].filter(Boolean), b: [pk.dst, alt.dst].filter(Boolean) });
      return { ok: true, t: hit ? d.name + ': /ip firewall filter, chain=' + chain + ' — правило ' + F.indexOf(hit) + ' action=accept' + (est ? ' (connection-state=established)' : '') : null }; }
    return { ok: false, t: d.name + ': /ip firewall filter, chain=' + chain + ' — правило ' + F.indexOf(hit) + ' action=' + act + ' (' + pk.proto + ' ' + (alt.src || pk.src) + ' → ' + (alt.dst || pk.dst) + ', connection-state=' + state + ')' };
  };
  function inR(ip, r) { if (!r) return false; var n = IP.ip2n(ip); return n >= IP.ip2n(r[0]) && n <= IP.ip2n(r[1]); }

  // ---------------------------------------------------------------- устройство в модели сети
  function fresh() { return { L: {}, S: {} }; }
  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {};
    if (m.vendor !== 'mikrotik') return d;
    d.sub = 'ros'; d.st.mode = 'ros'; d.st.ros = { path: [], c: fresh(), saved: null, ask: null, user: 'admin' };
    compile(d.st); return d;
  };
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id]; if (!isRos(d)) return ex0.apply(this, arguments); this.gen++; if (d.off) return ''; var r = exec(d.st, line); d.st.ros.saved = EL.clone(d.st.ros.c); return r; };   // RouterOS сохраняет изменения сразу
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; return isRos(d) ? prompt(d.st) : pr0.apply(this, arguments); };
  var he0 = P.help;
  P.help = function (id, line) { var d = this.devs[id]; return isRos(d) ? help(d.st, line) : he0.apply(this, arguments); };
  var tb0 = P.tab;
  P.tab = function (id, line) { var d = this.devs[id]; if (!isRos(d)) return tb0.apply(this, arguments);
    var t = toks(line), w = t.length && !/\s$/.test(line) ? t[t.length - 1] : null; if (!w) return null; var c = children(d.st.ros.path).concat(CMDS).filter(function (x) { return x.indexOf(w) === 0; });
    return c.length === 1 ? line.replace(/\S+$/, c[0]) + ' ' : null; };
  var rb0 = P.reboot;
  P.reboot = function (id) { var d = this.devs[id]; if (!isRos(d)) return rb0.apply(this, arguments); var x = d.st.ros; x.c = x.saved ? EL.clone(x.saved) : fresh(); x.path = []; x.ask = null; compile(d.st);
    this.mac[id] = {}; this.arp[id] = {}; d.off = false; this.gen++; };
  var sh0 = P.setHost;
  P.setHost = function (id, name) { var d = this.devs[id]; if (!isRos(d)) return sh0.apply(this, arguments); single(d.st, 'system identity').name = name; compile(d.st); };
  if (EL.cfgText) { var ct0 = EL.cfgText; EL.cfgText = function (d) { return isRos(d) ? exportAll(d.st) : ct0.apply(this, arguments); }; }
  if (EL.applyConfig) { var ap0 = EL.applyConfig; EL.applyConfig = function (n, id, text) { var d = n.devs[id]; if (!isRos(d)) return ap0.apply(this, arguments); var errs = [], menu = '';
    String(text).split('\n').forEach(function (l) { l = l.trim(); if (!l || /^#/.test(l)) return; if (/^\//.test(l) && !/=/.test(l)) { menu = l; n.exec(id, l); return; }
      var r = n.exec(id, (menu && !/^\//.test(l) ? menu + ' ' : '') + l); if (/syntax error|bad command|does not match/.test(r)) errs.push(d.name + ' «' + l + '» → ' + r); });
    d.st.ros.path = []; return errs; }; }
  var ifn0 = P.ifaces;
  EL.ros = { exec: exec, prompt: prompt, isRos: isRos, compile: compile, alias: alias };
  void ifn0;
})(typeof window !== 'undefined' ? window : global);
