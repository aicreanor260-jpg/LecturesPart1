/* OLT Turbo GEPON LTE-8X / LTE-2X (руководство и Quick guide ПО 3.16.7) и абонентский EPON-терминал NTE-2 (B+) — один сценарий:
   VLAN во встроенном коммутаторе → ONT по MAC → профиль правил → reconfigure → save.
   CLI: LTE-8X# → switch → LTE-8X(switch)# → configure → (switch)(config)# → vlan N → (switch)(config-vlan)#: tagged front-port|pon-port A-B, name; exit → reconfig;
     show ont list all (ONT без конфигурации — AUTHFAILED); ont_mac MAC → LTE-8X(ONT-x/x/MAC)#: add config, set description, set profile rules N, reconfigure, exit;
     add profile rules N; profile rules N → (profile-rules)#: set description, rule add uni0|pon IDX: if (…) then …; forward, rule delete, rule show uni0|pon;
     set management ip address A/L, set management vid N, set default gateway A; save (в NVRAM); show system information; reboot.
   Правила: uni0 «if (Always) then AddTagVID = V; forward» — кадры с LAN без тега уходят в VLAN V; pon «if (VID == V) then DeleteTag; forward» — VLAN V к абоненту без тега;
     uni0 «if (VID == A) then ReplaceTagVID = V» — абонент шлёт с тегом A (в модели — LAN tagged V, подмена тега не показывается).
   Упрощения: на pon-port одна ONT, сплиттер, линки LLID, DBA, шейперы, IPMC, PPPoE/DHCP snooping не моделируются; формы вывода — по примерам руководства. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip, E = EL.E;
  var T = [], ERR = 'Unknown command';
  function cmd(modes, pat, run, d) { T.push({ modes: modes.split(' '), pat: pat.split(' '), run: run, d: d }); }
  function isL(d) { return !!d && d.sub === 'lte'; }
  function isE(d) { return !!d && d.sub === 'eont'; }
  function cfg() { return { mgmt: { ip: '192.168.1.2', len: 24, vid: 1, gw: '192.168.1.1' }, vlans: {}, ont: {}, rules: {} }; }

  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}, st = d.st;
    if (m.kind === 'lte') { d.sub = 'lte'; st.stp = { on: false }; st.users = { admin: { pw: 'password', priv: 15 } };
      st.lte = { host: m.host, mode: 'root', ctx: null, cand: cfg(), run: null, nv: null, swc: {} }; st.lte.run = EL.clone(st.lte.cand); st.lte.nv = EL.clone(st.lte.cand); }
    if (m.kind === 'eont') { d.sub = 'eont'; st.stp = { on: false }; var n = (EL.Net.seq * 37 + 0x7451) & 0xffffff;
      st.mac = '02:00:4B:' + [n >> 16, (n >> 8) & 255, n & 255].map(function (x) { return ('0' + x.toString(16).toUpperCase()).slice(-2); }).join(':'); }
    if (m.kind === 'lte' || m.kind === 'eont') this.lteDirty = true;
    return d;
  };

  // ---------------------------------------------------------------- L2 по действующей конфигурации
  function ontsOf(net, d) { var c = d.st.lte.run, out = [];
    Object.keys(d.st.ports).filter(function (k) { return /^pon-port /.test(k); }).forEach(function (pp) {
      var pr = net.peer(d.id, pp), od = pr && net.devs[pr.dev]; if (!isE(od) || od.off || !net.phys(d.id, pp).up) return;
      var o = c.ont[od.st.mac]; out.push({ pp: pp, n: +pp.split(' ')[1], dev: od, o: o, ok: !!(o && o.done) }); });
    return out; }
  function svc(c, o) { var R = c.rules[o && o.rules] || { uni0: [], pon: [] }, u = [], t = [], down = [];   // u — LAN без тега, t — LAN с тегом
    R.uni0.forEach(function (r) { var m = r.text.match(/AddTagVID\s*=\s*(\d+)/i), q = r.text.match(/ReplaceTagVID\s*=\s*(\d+)/i);
      if (m && /Always/i.test(r.text)) u.push(+m[1]); else if (q) t.push(+q[1]); });
    R.pon.forEach(function (r) { var m = r.text.match(/VID\s*==\s*(\d+)\)\s*then\s*DeleteTag/i); if (m) down.push(+m[1]); });
    return { untag: u.filter(function (v) { return down.indexOf(v) >= 0; }), tag: t }; }
  P.lteSync = function () {
    var s = this;
    this.list().filter(isL).forEach(function (d) { var st = d.st, c = st.lte.run, V = {};
      Object.keys(st.ports).forEach(function (k) { var p = st.ports[k]; p.mode = 'general'; p.gtag = []; p.guntag = []; p.pvid = 4095; });
      Object.keys(c.vlans).forEach(function (v) { var x = c.vlans[v]; x.front.forEach(function (f) { var p = st.ports['front-port ' + f]; if (p) { p.gtag.push(+v); V[v] = 1; } }); });
      ontsOf(s, d).forEach(function (x) { if (!x.ok) return; var sv = svc(c, x.o), os = x.dev.st, p = st.ports[x.pp];
        var vids = sv.untag.concat(sv.tag).filter(function (v) { var vv = c.vlans[v]; return vv && vv.pon.indexOf(x.n) >= 0; });   // VLAN должна быть tagged на pon-port коммутатора
        vids.forEach(function (v) { if (p.gtag.indexOf(v) < 0) p.gtag.push(v); V[v] = 1; });
        var PO = os.ports.PON, L = os.ports.LAN; PO.mode = 'general'; PO.gtag = vids.slice(); PO.guntag = []; PO.pvid = 4095;
        L.mode = 'general'; L.gtag = sv.tag.filter(function (v) { return vids.indexOf(v) >= 0; }); L.guntag = sv.untag.filter(function (v) { return vids.indexOf(v) >= 0; });
        L.pvid = L.guntag[0] || 4095; os.vlans = { 1: 'default' }; vids.forEach(function (v) { os.vlans[v] = '-'; }); os.lteOn = true; });
      st.vlans = { 1: 'default' }; Object.keys(V).forEach(function (v) { st.vlans[v] = '-'; });
      var m = c.mgmt; st.svi = {}; st.svi[m.vid] = m.ip + '/' + m.len; st.gw = m.gw || null; });
    this.list().filter(isE).forEach(function (o) { var on = s.list().some(function (d) { return isL(d) && ontsOf(s, d).some(function (x) { return x.dev === o && x.ok; }); });
      if (!on) { Object.keys(o.st.ports).forEach(function (k) { var p = o.st.ports[k]; p.mode = 'general'; p.gtag = []; p.guntag = []; p.pvid = 4095; }); o.st.vlans = { 1: 'default' }; } });
    this.lteGen = this.gen;
  };
  var flood0 = P.flood;
  P.flood = function () { if (this.lteGen !== this.gen && this.list().some(function (d) { return isL(d) || isE(d); })) this.lteSync(); return flood0.apply(this, arguments); };

  // ---------------------------------------------------------------- CLI
  function C(st) { return st.lte.cand; }
  function prompt(st) { var o = st.lte, h = o.host;
    return h + ({ root: '#', sw: '(switch)#', swc: '(switch)(config)#', swv: '(switch)(config-vlan)#', rules: '(profile-rules)#' }[o.mode] || ('(ONT-x/x/' + o.ctx + ')#')); }
  function nlist(w, max) { var t = String(w).replace(/[–—]/g, '-').replace(/\s+/g, ''), L = [], ok = true;
    t.split(',').forEach(function (x) { var m = x.match(/^(\d+)(?:-(\d+))?$/); if (!m) { ok = false; return; } for (var i = +m[1]; i <= +(m[2] || m[1]); i++) L.push(i); });
    return ok && L.length && L.every(function (n) { return n >= 0 && n < max; }) ? L : null; }
  function cnt(st, kind) { return Object.keys(st.ports).filter(function (k) { return k.indexOf(kind + ' ') === 0; }).length; }
  cmd('root', 'switch', function (st) { st.lte.mode = 'sw'; if (!st.lte.swc) st.lte.swc = EL.clone(C(st).vlans); }, 'Встроенный коммутатор (правки VLAN копятся до reconfig)');
  cmd('sw', 'configure', function (st) { st.lte.mode = 'swc'; }, 'Настройка коммутатора');
  cmd('sw', 'exit', function (st) { st.lte.mode = 'root'; });
  cmd('swc', 'vlan <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return ERR; var V = st.lte.swc; V[a[0]] = V[a[0]] || { front: [], pon: [], name: '' }; st.lte.mode = 'swv'; st.lte.ctx = a[0]; }, 'VLAN');
  cmd('swc', 'no vlan <n>', function (st, a) { delete st.lte.swc[a[0]]; });
  cmd('swc', 'reconfig', function (st) { C(st).vlans = EL.clone(st.lte.swc); st.lte.run.vlans = EL.clone(st.lte.swc); if (st.net) st.net.gen++; return ''; }, 'Применить настройки коммутатора');
  cmd('swc', 'exit', function (st) { st.lte.mode = 'sw'; });
  function tg(kind, add) { return function (st, a) { var L = nlist(a[0], cnt(st, kind + '-port')); if (!L) return ERR; var v = st.lte.swc[st.lte.ctx], A = v[kind];
    L.forEach(function (x) { var i = A.indexOf(x); if (add && i < 0) A.push(x); if (!add && i >= 0) A.splice(i, 1); }); A.sort(function (x, y) { return x - y; }); }; }
  cmd('swv', 'tagged front-port <rest>', tg('front', true), 'Uplink-порты с тегом (0 – 7)');
  cmd('swv', 'tagged pon-port <rest>', tg('pon', true), 'PON-порты с тегом');
  cmd('swv', 'no tagged front-port <rest>', tg('front', false)); cmd('swv', 'no tagged pon-port <rest>', tg('pon', false));
  cmd('swv', 'name <w>', function (st, a) { st.lte.swc[st.lte.ctx].name = a[0]; });
  cmd('swv', 'exit', function (st) { st.lte.mode = 'swc'; st.lte.ctx = null; });
  // ONT
  function macIn(w) { var m = String(w).toUpperCase().match(/^([0-9A-F]{1,2}):([0-9A-F]{1,2}):([0-9A-F]{1,2}):([0-9A-F]{1,2}):([0-9A-F]{1,2}):([0-9A-F]{1,2})$/);
    return m ? m.slice(1).map(function (x) { return ('0' + x).slice(-2); }).join(':') : null; }
  cmd('root', 'ont_mac <w>', function (st, a) { var m = macIn(a[0]); if (!m) return 'Wrong MAC address'; st.lte.mode = 'ont'; st.lte.ctx = m; }, 'ONT по MAC-адресу');
  function O(st) { return C(st).ont[st.lte.ctx]; }
  cmd('ont', 'add config', function (st) { if (O(st)) return 'Config for ONT-' + st.lte.ctx + ' already exists'; C(st).ont[st.lte.ctx] = { desc: '', rules: null, done: false }; return 'Config for ONT-' + st.lte.ctx + ' created'; }, 'Создать конфигурацию ONT');
  cmd('ont', 'delete config', function (st) { delete C(st).ont[st.lte.ctx]; delete st.lte.run.ont[st.lte.ctx]; if (st.net) st.net.gen++; return 'Config for ONT-' + st.lte.ctx + ' deleted'; });
  function needCfg(f) { return function (st, a) { if (!O(st)) return 'Config for ONT-' + st.lte.ctx + ' not found. Use "add config"'; return f(st, a); }; }
  cmd('ont', 'set description <rest>', needCfg(function (st, a) { O(st).desc = a[0]; }), 'Описание ONT');
  cmd('ont', 'set profile rules <n>', needCfg(function (st, a) { if (a[0] > 63) return ERR; if (!C(st).rules[a[0]]) return 'Profile ' + a[0] + ' not found'; O(st).rules = a[0]; }), 'Профиль правил 0–63');
  cmd('ont', 'reconfigure', function (st) { var r = st.net && st.net.devs[st.dev], x = r && ontsOf(st.net, r).filter(function (y) { return y.dev.st.mac === st.lte.ctx; })[0];
    if (!O(st)) return 'Config for ONT-' + st.lte.ctx + ' not found';
    if (!x) return 'ONT-' + st.lte.ctx + ' is not connected';
    O(st).done = true; st.lte.run.ont[st.lte.ctx] = EL.clone(O(st)); st.lte.run.rules = EL.clone(C(st).rules); if (st.net) st.net.gen++; return 'ONT-' + st.lte.ctx + ' reconfiguration successfull'; }, 'Применить конфигурацию к ONT');
  cmd('ont', 'exit', function (st) { st.lte.mode = 'root'; st.lte.ctx = null; });
  // профили правил
  cmd('root', 'add profile rules <n>', function (st, a) { if (a[0] > 63) return ERR; if (C(st).rules[a[0]]) return 'Profile ' + a[0] + ' already exists';
    C(st).rules[a[0]] = { desc: '', uni0: [], pon: [] }; return 'Profile ' + a[0] + ' created'; }, 'Создать профиль правил');
  cmd('root', 'profile rules <n>', function (st, a) { if (!C(st).rules[a[0]]) return 'Profile ' + a[0] + ' not found'; st.lte.mode = 'rules'; st.lte.ctx = a[0]; }, 'Настроить профиль правил');
  function RL(st) { return C(st).rules[st.lte.ctx]; }
  cmd('rules', 'set description <rest>', function (st, a) { RL(st).desc = a[0]; });
  cmd('rules', 'rule add <w> <rest>', function (st, a) { var k = a[0].toLowerCase(); if (k !== 'uni0' && k !== 'pon') return ERR;
    var m = String(a[1]).match(/^(\d+)\s*:\s*if\s*\((.+)\)\s*then\s+(.+?);\s*forward\s*$/i); if (!m) return 'Wrong rule format: IDX: if (CONDITION) then ACTION; forward';
    RL(st)[k] = RL(st)[k].filter(function (r) { return r.idx !== +m[1] || r.text !== a[1]; }).concat([{ idx: +m[1], text: a[1].trim() }]); }, 'Правило: uni0|pon N: if (…) then …; forward');
  cmd('rules', 'rule delete <w> <n>', function (st, a) { var k = a[0].toLowerCase(); if (!RL(st)[k]) return ERR; RL(st)[k] = RL(st)[k].filter(function (r) { return r.idx !== a[1]; }); });
  cmd('rules', 'rule show <w>', function (st, a) { var L = RL(st)[a[0].toLowerCase()]; if (!L) return ERR; return L.length ? L.map(function (r, i) { return i + ') ' + r.idx + ': ' + r.text; }).join('\n') : 'No rules'; });
  cmd('rules', 'exit', function (st) { st.lte.mode = 'root'; st.lte.ctx = null; });
  // система
  cmd('root', 'set management ip address <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return ERR; C(st).mgmt.ip = c.ip; C(st).mgmt.len = c.len; st.lte.run.mgmt = EL.clone(C(st).mgmt); if (st.net) st.net.gen++; }, 'Адрес управления A/L');
  cmd('root', 'set management vid <n>', function (st, a) { C(st).mgmt.vid = a[0]; st.lte.run.mgmt = EL.clone(C(st).mgmt); if (st.net) st.net.gen++; });
  cmd('root', 'set default gateway <ip>', function (st, a) { C(st).mgmt.gw = a[0]; st.lte.run.mgmt = EL.clone(C(st).mgmt); if (st.net) st.net.gen++; });
  cmd('root', 'save', function (st) { st.lte.nv = EL.clone(st.lte.run); return 'Configuration saved successfully'; }, 'Сохранить конфигурацию');
  cmd('root', 'show system information', function (st) { var m = st.lte.run.mgmt;
    return ['System overview', 'Device type: ' + st.lte.host, 'Host ID: 0', 'Host name: ' + st.lte.host, '', 'Management interface:', '', 'IP address:            ' + m.ip + '/' + m.len, '',
      'Default gateway:       ' + m.gw, '', 'VID:                   ' + m.vid].join('\n'); }, 'Сведения о системе');
  cmd('root', 'show ont list all', function (st) { var net = st.net, d = net && net.devs[st.dev]; if (!d) return '';
    var L = ontsOf(net, d), c = st.lte.run, o = ['ONT list for all OLTs:', '', 'CONFIG Ch/ID:  STATUS Ch/ID:       MAC:               State:    Description:'];
    L.forEach(function (x, i) { var cf = c.ont[x.dev.st.mac]; o.push(i + ')  ' + (cf ? 'x/' + (100 + i) : 'x/x') + '        ' + x.n + '/' + (cf ? 100 + i : 'x') + '        ' + x.dev.st.mac + '  ' +
      (x.ok ? 'OK' : cf ? 'CONFIGURED' : 'AUTHFAILED') + '        ' + (cf && cf.desc || '-')); });
    Object.keys(c.ont).filter(function (k) { return !L.some(function (x) { return x.dev.st.mac === k; }); }).forEach(function (k, i) { o.push((L.length + i) + ')  x/x        x/x        ' + k + '  OFFLINE   ' + (c.ont[k].desc || '-')); });
    return o.join('\n'); }, 'Список ONT');
  cmd('root', 'reboot', function (st) { st.lte.run = EL.clone(st.lte.nv); st.lte.cand = EL.clone(st.lte.nv); st.lte.swc = EL.clone(st.lte.nv.vlans); if (st.net) st.net.gen++; return 'System is rebooting...'; }, 'Перезагрузка (загрузится сохранённая конфигурация)');
  cmd('root', 'ping <ip>', function (st, a) { return st.net ? st.net.pingText(st.dev, a[0], 'linux') : ''; });
  cmd('root', 'exit', function () { return ''; });

  function exec(st, raw) { var o = st.lte, proxy = { get mode() { return o.mode; }, lte: o, net: st.net, dev: st.dev, ports: st.ports };
    var r = EL.cli.runTable(T, proxy, String(raw).trim()); return /^% (Unrecognized|Incomplete|Ambiguous)/i.test(r) ? ERR : r; }
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id];
    if (isL(d)) { this.gen++; if (d.off) return ''; if (/\?\s*$/.test(line)) return T.filter(function (c) { return c.modes.indexOf(d.st.lte.mode) >= 0; }).map(function (c) { return '  ' + c.pat.join(' ') + (c.d ? '    ' + c.d : ''); }).join('\n');
      return exec(d.st, line); }
    if (isE(d)) return '';
    return ex0.apply(this, arguments); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; if (isL(d)) return prompt(d.st); if (isE(d)) return ''; return pr0.apply(this, arguments); };
  EL.lte = { T: T, exec: exec };
})(typeof window !== 'undefined' ? window : global);
