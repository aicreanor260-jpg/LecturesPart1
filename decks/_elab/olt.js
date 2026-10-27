/* OLT Eltex LTP-N / LTX и ONT-мосты (спецификация sources/eltex/spec/olt.md: справочник CLI и Quick guide LTP 1.12.0, РЭ LTP/LTX).
   CLI OLT — своя: LTP-16N# → configure → LTP-16N(configure)# → подрежимы LTP-16N(config)(if-ont-2/1)#; правки копятся в candidate,
   commit делает их действующими (running), save — пишет в NVRAM (после перезагрузки грузится NVRAM).
   Трафик: front-port — порт general с VLAN из vlan allow (по умолчанию запрещены все); ONT активна, если на pon-port P подключён
   ONT с серийным номером из interface ont P/O (serial) и сделан commit; сервис service N profile cross-connect X даёт outer vid:
   кадры этой VLAN идут front-port ↔ pon-port ↔ ONT; на LAN ONT — без тега (ont-mode bridge, нет user vid) или с тегом user vid.
   Упрощения (в источниках нет или вне учебной модели — помечено): к pon-port подключается одна ONT (сплиттер не моделируется);
   изоляция front ↔ front и pon ↔ pon не моделируется; трансляция outer vid ≠ user vid, bridge group, DBA, IGMP/multicast,
   профили management и ACS только хранятся; running-config — по образцу примеров справочника; EquipmentID ONT, кроме примеров
   справочника, — n/a; RSSI и расстояние — условные; у ONT своей CLI нет (настраивается с OLT по OMCI). */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, P = EL.Net.prototype, IP = EL.ip;
  var T = [];
  function cmd(modes, pat, run, d) { T.push({ modes: modes.split(' '), pat: pat.split(' '), run: run, d: d }); }
  function isOlt(d) { return !!d && d.sub === 'olt'; }
  function isOnt(d) { return !!d && d.sub === 'ont'; }
  function cfg() { return { host: null, mgmt: { ip: '192.168.1.2', mask: '255.255.255.0', gw: '0.0.0.0', vid: 1 }, front: {}, ont: {}, cc: {}, pp: {}, dba: {}, mgp: {}, vlans: {}, igmp: false,
    users: { admin: { pw: 'password', priv: 15 } } }; }
  var CFG = 'configure front pon ont cc pp dba mgp vlan oob slot';

  // ---------------------------------------------------------------- устройства
  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}, st = d.st;
    if (m.kind === 'olt') { d.sub = 'olt'; st.stp = { on: false }; st.olt = { host: m.host, mode: 'root', ctx: null, cand: cfg(), run: null, nv: null, pon: m.pon, dl: m.oltDialect || 'ltp-n', slots: m.slots };
      st.olt.run = EL.clone(st.olt.cand); st.olt.nv = EL.clone(st.olt.cand); st.users = { admin: { pw: 'password', priv: 15 } }; st.mode = 'priv'; }
    if (m.kind === 'ont') { d.sub = 'ont'; st.stp = { on: false }; st.serial = 'ELTX' + ('00000000' + (0x73000100 + (EL.Net.seq * 7 % 0xff)).toString(16).toUpperCase()).slice(-8); }
    if (m.kind === 'olt' || m.kind === 'ont') this.oltDirty = true;
    return d;
  };
  // PON-кабель: оптика между pon-port и PON ONT
  EL.CABLES.pon = 'Оптика PON (SC/APC)';
  function ponPort(p) { return /^g?pon-port \d+(\/\d+)?$/.test(p) || p === 'PON'; }
  // LTP-X (ПО 3.52): PON-порт в CLI OLT — gpon-port N, нумерация с нуля
  function PN(st) { return st.olt.dl === 'ltp-x' ? 'gpon-port ' : 'pon-port '; }
  var defc0 = P.defaultCable;
  P.defaultCable = function (a, ap, b, bp) { return ponPort(ap) || ponPort(bp) ? 'pon' : defc0.apply(this, arguments); };
  var phys0 = P.phys;
  P.phys = function (id, port) {
    var pr = this.peer(id, port); if (!pr) return phys0.apply(this, arguments);
    var l = this.links[pr.li], cab = l.cab || this.defaultCable(l.a.dev, l.a.port, l.b.dev, l.b.port);
    if (cab !== 'pon' && !ponPort(port) && !ponPort(pr.port)) return phys0.apply(this, arguments);
    if (cab !== 'pon') return { up: false, why: 'PON-порт — оптика PON', dup: {} };
    if (!ponPort(port) || !ponPort(pr.port) || (port === 'PON') === (pr.port === 'PON')) return { up: false, why: 'оптика PON соединяет pon-port OLT с портом PON ONT', dup: {} };
    return { up: true, cab: 'pon', speed: 1000, dup: {}, mismatch: false };
  };

  // ---------------------------------------------------------------- L2: порты OLT и ONT по действующей конфигурации
  function onts(net, olt) { var c = olt.st.olt.run, out = [];
    Object.keys(c.ont).forEach(function (k) { var o = c.ont[k], pp = k.replace(/\/\d+$/, ''), pr = net.peer(olt.id, PN(olt.st) + pp), od = pr && net.devs[pr.dev];
      var ok = !!(o.serial && isOnt(od) && !od.off && od.st.serial === o.serial && net.phys(olt.id, PN(olt.st) + pp).up && pr.port === 'PON') && slotOk(olt.st, pp);
      var vids = Object.keys(o.svc || {}).map(function (s) { var cc = c.cc[(o.svc[s] || {}).cc]; return cc && cc.outer ? { outer: cc.outer, user: cc.user || null, mode: cc.mode || null } : null; }).filter(Boolean);
      out.push({ key: k, pp: pp, id: +k.split('/').pop(), o: o, dev: ok ? od : null, vids: vids }); });
    return out; }
  P.oltSync = function () {
    var s = this;
    this.list().filter(isOlt).forEach(function (d) {
      var st = d.st, c = st.olt.run, V = {};
      Object.keys(st.ports).forEach(function (k) { var p = st.ports[k]; p.mode = 'general'; p.gtag = []; p.guntag = []; p.pvid = 4095; });
      if (st.olt.dl === 'ltp-x') { var SV = (c.sw || {}).vlans || {}; c.front = {}; Object.keys(SV).forEach(function (v) { SV[v].front.forEach(function (fp) { (c.front[fp] = c.front[fp] || { allow: [] }).allow.push(+v); }); }); }
      Object.keys(c.front).forEach(function (n) { var f = c.front[n], p = st.ports['front-port ' + n]; if (!p) return; p.gtag = (f.allow || []).slice(); p.shut = !!f.shut;
        p.gtag.forEach(function (v) { V[v] = 1; }); });
      onts(s, d).forEach(function (x) { if (!x.dev) return; var p = st.ports[PN(st) + x.pp], o = x.dev.st;
        if (st.olt.dl === 'ltp-x') x.vids = x.vids.filter(function (v) { var sv = ((c.sw || {}).vlans || {})[v.outer]; return sv && sv.pon.indexOf(+x.pp) >= 0; });   // VLAN должна быть tagged pon-port во встроенном коммутаторе
        x.vids.forEach(function (v) { if (p.gtag.indexOf(v.outer) < 0) p.gtag.push(v.outer); V[v.outer] = 1; });
        o.ports.PON.mode = 'general'; o.ports.PON.gtag = x.vids.map(function (v) { return v.outer; }); o.ports.PON.guntag = []; o.ports.PON.pvid = 4095;
        var L = o.ports.LAN; L.mode = 'general'; L.gtag = []; L.guntag = []; L.pvid = 4095;
        x.vids.forEach(function (v) { if (v.user) L.gtag.push(v.outer); else { L.guntag.push(v.outer); L.pvid = v.outer; } });
        o.vlans = {}; x.vids.forEach(function (v) { o.vlans[v.outer] = '-'; }); o.vlans[1] = 'default'; o.olt = d.id; });
      st.vlans = { 1: 'default' }; Object.keys(V).forEach(function (v) { st.vlans[v] = '-'; });
      var m = c.mgmt, len = IP.mask2len(m.mask) || 24; st.svi = {}; if (m.ip) st.svi[m.vid] = m.ip + '/' + len; st.gw = m.gw && m.gw !== '0.0.0.0' ? m.gw : null;
    });
    this.list().filter(isOnt).forEach(function (o) { var on = s.list().some(function (d) { return isOlt(d) && onts(s, d).some(function (x) { return x.dev === o; }); });
      if (!on) { Object.keys(o.st.ports).forEach(function (k) { var p = o.st.ports[k]; p.mode = 'general'; p.gtag = []; p.guntag = []; p.pvid = 4095; }); o.st.vlans = { 1: 'default' }; } });
    this.oltGen = this.gen;
  };
  var flood0 = P.flood;
  P.flood = function () { if (this.oltGen !== this.gen && this.list().some(function (d) { return d.sub === 'olt' || d.sub === 'ont'; })) this.oltSync(); return flood0.apply(this, arguments); };

  // ---------------------------------------------------------------- CLI OLT
  var PRM = { slot: function (c) { return 'slot-' + c; }, front: function (c) { return 'if-front-' + c; }, pon: function (c) { return 'if-pon-' + c; }, ont: function (c) { return 'if-ont-' + c; }, oob: function () { return 'if-port-oob'; },
    cc: function (c) { return 'profile-cross-connect-' + c; }, pp: function (c) { return 'profile-ports-' + c; }, dba: function (c) { return 'profile-dba-' + c; },
    mgp: function (c) { return 'profile-management-' + c; }, vlan: function (c) { return 'vlan-' + c; } };
  var PRX = { cc: 'config-cross-connect', pp: 'config-ports', dba: 'config-dba', mgp: 'config-management' }, SWP = { sw: '(switch)#', swcfg: '(switch)(config)#', swif: '(switch)(config-if)#', swvlan: '(switch)(config-vlan)#' };
  function prompt(st) { var o = st.olt, h = o.run.host || o.host;
    if (o.dl === 'ltp-x') { if (o.mode === 'root') return h + '#'; if (o.mode === 'configure') return h + '(config)#'; if (SWP[o.mode]) return h + (o.mode === 'swvlan' && /[,-]/.test(o.ctx) ? '(switch)(config-vlan-range)#' : SWP[o.mode]);
      if (PRX[o.mode]) return h + '(' + PRX[o.mode] + ')("' + o.ctx + '")#'; return h + '(config)(' + (o.mode === 'pon' ? 'if-gpon-' + o.ctx : PRM[o.mode](o.ctx)) + ')#'; }
    if (o.mode === 'root') return h + '#'; if (o.mode === 'configure') return h + '(configure)#'; return h + '(config)(' + PRM[o.mode](o.ctx) + ')#'; }
  function C(st) { return st.olt.cand; }
  // MA5160/MA5020: линейная карта слота работает, если задан тип (slot N → type lc16g) и сделан commit
  function slotOk(st, pp) { if (st.olt.dl !== 'ma5000') return true; var sl = (st.olt.run.slots || {})[String(pp).split('/')[0]]; return !!(sl && sl.type && sl.type !== 'unknown'); }
  // номера портов: N, N-M, a,b; с слотом/FC: S/P, A-B/P; у MA5000 «4» в show interface ont — все pon-port слота 4
  function portIds(st, kind, w, slotAll) { var pre = kind + ' ', have = Object.keys(st.ports).filter(function (k) { return k.indexOf(pre) === 0; }).map(function (k) { return k.slice(pre.length); });
    var out = [], bad = false;
    String(w).split(',').forEach(function (x) { var m = x.match(/^(\d+)(?:-(\d+))?(?:\/(\d+)(?:-(\d+))?)?$/); if (!m) { bad = true; return; }
      for (var a = +m[1]; a <= +(m[2] || m[1]); a++) { if (m[3] === undefined) { if (slotAll && st.olt.dl === 'ma5000') have.forEach(function (h) { if (h.split('/')[0] === String(a)) out.push(h); }); else out.push(String(a)); }
        else for (var b = +m[3]; b <= +(m[4] || m[3]); b++) out.push(a + '/' + b); } });
    if (bad || !out.length || out.some(function (x) { return have.indexOf(x) < 0; })) return null; return out; }
  function nums(w, max) { var L = []; String(w).split(',').forEach(function (x) { var m = x.match(/^(\d+)(?:-(\d+))?$/); if (!m) { L = null; return; } if (!L) return;
    for (var i = +m[1]; i <= +(m[2] || m[1]); i++) L.push(i); }); return L && L.every(function (n) { return n >= 1 && n <= max; }) ? L : null; }
  function nfront(st) { return Object.keys(st.ports).filter(function (k) { return /^front-port/.test(k); }).length; }
  function npon(st) { return Object.keys(st.ports).filter(function (k) { return /^pon-port/.test(k); }).length; }
  // ONT на pon-port: GPON — до 128, XGS-PON — до 256; LTX по умолчанию в GPON (справочник CLI, вариант А), у C-моделей чётные порты — XGS-PON
  function maxOnt(st, pp) { var n = +String(pp).split('/').pop(); return st.olt.pon === 'combo' && n % 2 === 0 ? 256 : 128; }
  var ERR = '% Invalid input';
  cmd('root', 'configure', function (st) { st.olt.mode = 'configure'; }, 'Режим конфигурации');
  cmd('root', 'configure terminal', function (st) { st.olt.mode = 'configure'; });
  function commit(st) { st.olt.run = EL.clone(st.olt.cand); if (st.net) st.net.gen++;
    return st.olt.dl === 'ma5000' ? 'After commit operation, the configuration has to be confirmed within: 5 minutes\nConfiguration committed successfully' : 'Configuration committed successfully'; }
  function confirm(st) { st.olt.nv = EL.clone(st.olt.run); return 'Configuration is confirmed for master device (all changes are saved in NVRAM)'; }
  cmd('root', 'confirm', function (st) { if (st.olt.dl !== 'ma5000') return ERR; return confirm(st); }, 'MA5160/MA5020: подтвердить и сохранить в NVRAM');
  cmd('root', 'commit confirm', function (st) { if (st.olt.dl !== 'ma5000') return ERR; return commit(st) + '\n' + confirm(st); });
  cmd('root', 'commit', function (st) { return commit(st); }, 'Применить candidate-конфигурацию');
  cmd('root', 'save', function (st) { if (st.olt.dl === 'ma5000') return ERR; st.olt.nv = EL.clone(st.olt.run); return 'Configuration successfully saved to file'; }, 'Сохранить в NVRAM');
  cmd('root', 'rollback candidate-config', function (st) { st.olt.cand = EL.clone(st.olt.run); return 'Candidate configuration is rolled back successfully'; });
  cmd('root', 'restore running-config', function (st) { st.olt.run = EL.clone(st.olt.nv); st.olt.cand = EL.clone(st.olt.nv); if (st.net) st.net.gen++; return 'Restore configuration success'; });
  cmd('root', 'show version', function (st) { var d = st.net && st.net.devs[st.dev], m = EL.MODELS[d ? d.model : ''] || {};
    return 'Eltex ' + (d ? d.model : 'LTP') + ': software version ' + String(m.sw || '').replace(/^ПО /, ''); }, 'Версия ПО');
  cmd('root', 'exit', function (st) { st.olt.mode = 'root'; return ''; });
  cmd(CFG, 'exit', function (st) { st.olt.mode = st.olt.mode === 'configure' ? 'root' : 'configure'; st.olt.ctx = null; });
  cmd(CFG, 'end', function (st) { st.olt.mode = 'root'; st.olt.ctx = null; });
  // configure
  cmd('configure', 'system hostname <w>', function (st, a) { C(st).host = a[0]; }, 'Имя устройства');
  cmd('configure', 'management ip <ip>', function (st, a) { C(st).mgmt.ip = a[0]; }, 'Адрес управления');
  cmd('configure', 'management mask <ip>', function (st, a) { if (IP.mask2len(a[0]) === null) return ERR; C(st).mgmt.mask = a[0]; });
  cmd('configure', 'management gateway <ip>', function (st, a) { C(st).mgmt.gw = a[0]; });
  cmd('configure', 'management vid <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return ERR; C(st).mgmt.vid = a[0]; });
  cmd('configure', 'user <w> password <w> privilege <n>', function (st, a) { if (a[1].length < 8 || a[1].length > 31 || a[2] < 0 || a[2] > 15) return ERR; C(st).users[a[0]] = { pw: a[1], priv: a[2] }; }, 'Пользователь (пароль 8–31)');
  cmd('configure', 'ip igmp snooping enable', function (st) { C(st).igmp = true; });
  function enter(mode, keyFn) { return function (st, a) { var k = keyFn(st, a); if (k === null) return ERR; st.olt.mode = mode; st.olt.ctx = k; }; }
  cmd('configure', 'interface front-port <w>', enter('front', function (st, a) { var L = portIds(st, 'front-port', a[0]); if (!L) return null;
    L.forEach(function (n) { C(st).front[n] = C(st).front[n] || { allow: [] }; }); return a[0]; }), 'Порт к ядру сети');
  cmd('configure', 'interface pon-port <w>', enter('pon', function (st, a) { return portIds(st, 'pon-port', a[0]) ? a[0] : null; }), 'PON-порт');
  cmd('configure', 'slot <n>', enter('slot', function (st, a) { if (st.olt.dl !== 'ma5000' || a[0] < 1 || a[0] > (st.olt.slots || 16)) return null; var S = C(st).slots = C(st).slots || {}; S[a[0]] = S[a[0]] || {}; return a[0]; }), 'MA5160/MA5020: слот линейной карты');
  cmd('slot', 'type <w>', function (st, a) { if (['lc16g', 'lc16xg', 'lc16c', 'unknown'].indexOf(a[0]) < 0) return ERR; C(st).slots[st.olt.ctx].type = a[0]; }, 'Тип линейной карты: lc16g | lc16xg | lc16c');
  cmd('configure', 'interface port-oob', enter('oob', function () { return ''; }));
  cmd('configure', 'interface ont <w>', enter('ont', function (st, a) { var m = String(a[0]).match(/^(\d+(?:\/\d+)?)\/(\d+)$/); var b0 = st.olt.dl === 'ltp-x' ? 0 : 1; if (!m || !st.ports[PN(st) + m[1]] || +m[2] < b0 || +m[2] > maxOnt(st, m[1]) - 1 + b0) return null;
    C(st).ont[a[0]] = C(st).ont[a[0]] || { svc: {} }; return a[0]; }), 'ONT P/O');
  cmd('configure', 'no interface ont <w>', function (st, a) { delete C(st).ont[a[0]]; });
  cmd('configure', 'vlan <n>', enter('vlan', function (st, a) { if (a[0] < 1 || a[0] > 4094) return null; C(st).vlans[a[0]] = C(st).vlans[a[0]] || {}; return a[0]; }));
  [['cross-connect', 'cc'], ['ports', 'pp'], ['dba', 'dba'], ['management', 'mgp']].forEach(function (x) {
    cmd('configure', 'profile ' + x[0] + ' <w>', enter(x[1], function (st, a) { C(st)[x[1]][a[0]] = C(st)[x[1]][a[0]] || {}; return a[0]; }), 'Профиль ' + x[0]);
    cmd('configure', 'no profile ' + x[0] + ' <w>', function (st, a) { delete C(st)[x[1]][a[0]]; }); });
  // front-port
  function fronts(st) { return portIds(st, 'front-port', st.olt.ctx).map(function (n) { return C(st).front[n]; }); }
  cmd('front', 'vlan allow <list>', function (st, a) { if (a[0].some(function (v) { return v < 1 || v > 4094; })) return ERR;
    fronts(st).forEach(function (f) { a[0].forEach(function (v) { if (f.allow.indexOf(v) < 0) f.allow.push(v); }); f.allow.sort(function (x, y) { return x - y; }); }); }, 'Разрешить VLAN на порту');
  cmd('front', 'no vlan allow <list>', function (st, a) { fronts(st).forEach(function (f) { f.allow = f.allow.filter(function (v) { return a[0].indexOf(v) < 0; }); }); });
  cmd('front', 'shutdown', function (st) { fronts(st).forEach(function (f) { f.shut = true; }); });
  cmd('front', 'no shutdown', function (st) { fronts(st).forEach(function (f) { f.shut = false; }); });
  cmd('front', 'switchport mode <w>', function (st, a) { if (['general', 'trunk', 'access'].indexOf(a[0]) < 0) return ERR; fronts(st).forEach(function (f) { f.mode = a[0]; }); });
  cmd('front', 'pvid <n>', function (st, a) { fronts(st).forEach(function (f) { f.pvid = a[0]; }); });
  // ONT
  function ont(st) { return C(st).ont[st.olt.ctx]; }
  // серийный номер: ELTX73000140 или 16 hex (LTP-X показывает так: 454C5458… = «ELTX»)
  function snIn(w) { w = String(w).toUpperCase(); if (/^[A-Z]{4}[0-9A-F]{8}$/.test(w)) return w; if (!/^[0-9A-F]{16}$/.test(w)) return null;
    var v = ''; for (var i = 0; i < 8; i += 2) v += String.fromCharCode(parseInt(w.substr(i, 2), 16)); return /^[A-Z]{4}$/.test(v) ? v + w.slice(8) : null; }
  function snHex(sn) { return sn.slice(0, 4).split('').map(function (c) { return c.charCodeAt(0).toString(16).toUpperCase(); }).join('') + sn.slice(4); }
  cmd('ont', 'serial <w>', function (st, a) { var v = snIn(a[0]); if (!v) return ERR; ont(st).serial = v; }, 'Серийный номер ONT (ELTX… или 16 hex)');
  cmd('ont', 'no serial', function (st) { delete ont(st).serial; });
  cmd('ont', 'profile ports <w>', function (st, a) { ont(st).ports = a[0]; });
  cmd('ont', 'profile management <w>', function (st, a) { ont(st).mgmt = a[0]; });
  cmd('ont', 'description <rest>', function (st, a) { ont(st).desc = a[0]; });
  cmd('ont', 'service <n> profile cross-connect <w>', function (st, a) { if (st.olt.dl === 'ltp-x' ? a[0] > 28 : (a[0] < 1 || a[0] > 32)) return ERR; var s = ont(st).svc; s[a[0]] = s[a[0]] || {}; s[a[0]].cc = a[1]; }, 'Сервис: профиль cross-connect');
  cmd('ont', 'service <n> profile dba <w>', function (st, a) { var s = ont(st).svc; s[a[0]] = s[a[0]] || {}; s[a[0]].dba = a[1]; });
  cmd('ont', 'service <n> profile cross-connect <w> dba <w>', function (st, a) { var s = ont(st).svc; s[a[0]] = { cc: a[1], dba: a[2] }; });
  cmd('ont', 'no service <n>', function (st, a) { delete ont(st).svc[a[0]]; });
  // профили
  function cc(st) { return C(st).cc[st.olt.ctx]; }
  cmd('cc', 'ont-mode <w>', function (st, a) { if (['bridge', 'router'].indexOf(a[0]) < 0) return ERR; cc(st).mode = a[0]; });
  cmd('cc', 'bridge group <n>', function (st, a) { if (a[0] < 1 || a[0] > 75) return ERR; cc(st).bg = a[0]; });
  cmd('cc', 'outer vid <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return ERR; cc(st).outer = a[0]; }, 'VLAN сервиса на стороне OLT');
  cmd('cc', 'user vid <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return ERR; cc(st).user = a[0]; }, 'VLAN на стороне абонента');
  cmd('cc', 'no user vid', function (st) { delete cc(st).user; });
  cmd('cc', 'multicast enable', function (st) { cc(st).mc = true; });
  function gen(mode, pat) { cmd(mode, pat, function (st, a, line) { var o = C(st)[mode][st.olt.ctx]; (o.L = o.L || []).push(line); }); }
  ['port <n> bridge group <n>', 'port <n> multicast enable', 'veip multicast enable', 'veip igmp downstream vid <n>', 'veip igmp upstream vid <n>',
   'igmp multicast dynamic-entry <n> vid <n> group <ip> <ip>', 'port <n> igmp upstream vid <n>', 'port <n> igmp downstream vid <n>'].forEach(function (p) { gen('pp', p); });
  cmd('dba', '<rest>', function (st, a, line) { var o = C(st).dba[st.olt.ctx]; (o.L = o.L || []).push(line); });
  cmd('mgp', '<rest>', function (st, a, line) { var o = C(st).mgp[st.olt.ctx]; (o.L = o.L || []).push(line); });
  cmd('vlan', 'ip igmp snooping enable', function (st) { C(st).vlans[st.olt.ctx].igmp = true; });
  cmd('vlan', 'ip igmp snooping querier enable', function (st) { C(st).vlans[st.olt.ctx].querier = true; });

  // ---------------------------------------------------------------- show
  function runText(c) { var o = [];
    if (c.host) o.push('system hostname ' + c.host);
    Object.keys(c.slots || {}).forEach(function (n) { o.push('slot ' + n); if (c.slots[n].type) o.push('    type ' + c.slots[n].type); o.push('exit'); });
    var m = c.mgmt; o.push('management ip ' + m.ip, 'management mask ' + m.mask, 'management gateway ' + m.gw, 'management vid ' + m.vid);
    if (c.igmp) o.push('ip igmp snooping enable');
    Object.keys(c.vlans).forEach(function (v) { var x = c.vlans[v]; o.push('vlan ' + v); if (x.igmp) o.push('    ip igmp snooping enable'); if (x.querier) o.push('    ip igmp snooping querier enable'); o.push('exit'); });
    Object.keys(c.cc).forEach(function (k) { var x = c.cc[k]; o.push('profile cross-connect ' + k);
      if (x.mode) o.push('    ont-mode ' + x.mode); if (x.bg) o.push('    bridge group ' + x.bg); if (x.outer) o.push('    outer vid ' + x.outer); if (x.user) o.push('    user vid ' + x.user);
      if (x.mc) o.push('    multicast enable'); o.push('exit'); });
    ['pp', 'dba', 'mgp'].forEach(function (t) { Object.keys(c[t]).forEach(function (k) { o.push('profile ' + { pp: 'ports', dba: 'dba', mgp: 'management' }[t] + ' ' + k);
      (c[t][k].L || []).forEach(function (l) { o.push('    ' + l); }); o.push('exit'); }); });
    Object.keys(c.front).forEach(function (n) { var f = c.front[n]; o.push('interface front-port ' + n);
      if (f.allow.length) o.push('    vlan allow ' + E.fmtList(f.allow)); if (f.shut) o.push('    shutdown'); if (f.mode) o.push('    switchport mode ' + f.mode); if (f.pvid) o.push('    pvid ' + f.pvid); o.push('exit'); });
    Object.keys(c.ont).forEach(function (k) { var x = c.ont[k]; o.push('interface ont ' + k);
      if (x.serial) o.push('    serial ' + x.serial); if (x.ports) o.push('    profile ports ' + x.ports);
      Object.keys(x.svc).forEach(function (s) { if (x.svc[s].cc) o.push('    service ' + s + ' profile cross-connect ' + x.svc[s].cc); if (x.svc[s].dba) o.push('    service ' + s + ' profile dba ' + x.svc[s].dba); });
      if (x.mgmt) o.push('    profile management ' + x.mgmt); if (x.desc) o.push('    description ' + x.desc); o.push('exit'); });
    return o.join('\n'); }
  cmd('root', 'show running-config', function (st) { return runText(st.olt.run); }, 'Действующая конфигурация');
  cmd('root', 'show running-config <rest>', function (st, a) { var w = String(a[0]).replace(/\s+all$/, ''), L = runText(st.olt.run).split('\n'), o = [], on = false;
    L.forEach(function (l) { if (!/^\s/.test(l) && l !== 'exit') on = l.indexOf(w) === 0; if (on) o.push(l); }); return o.join('\n'); });
  cmd('root', 'show candidate-config', function (st) { var a = runText(st.olt.run).split('\n'), b = runText(st.olt.cand).split('\n');
    var d = b.filter(function (l) { return a.indexOf(l) < 0; }); return d.length ? ['configure terminal'].concat(d, ['exit', 'commit', 'exit']).join('\n') : ''; }, 'Неприменённые изменения');
  function dash(t) { return '-----------------------------------\n' + t + '\n-----------------------------------'; }
  function list(st, w, kind) {
    var net = st.net, d = net.devs[st.dev], pp = portIds(st, PN(st).trim(), w, true); if (!pp) return ERR;
    var HX = { unactivated: '## Serial ONT ID GPON-port Status RSSI[dBm] Version EquipmentID\nDescription', online: '## Serial ONT ID GPON-port Status RSSI[dBm] Version EquipmentID\nDescription',
      configured: '## Serial ONT ID GPON-port Description', offline: '## Serial ONT ID GPON-port Status\nDescription' };
    var X = onts(net, d), rows = [], H = st.olt.dl === 'ltp-x' ? HX[kind] : { unactivated: '## PON-port ONT ID Serial Status RSSI\nEquipmentID Version', configured: '## PON-port ONT ID Serial Status Description',
      online: '## PON-port ONT ID Serial Status RSSI\nEquipmentID Version', offline: '## PON-port ONT ID Serial Status\nDescription' }[kind];
    var out = [];
    pp.forEach(function (p) { var R = [];
      if (kind === 'unactivated') { var pr = net.peer(st.dev, PN(st) + p), od = pr && net.devs[pr.dev];
        if (isOnt(od) && !od.off && net.phys(st.dev, PN(st) + p).up && !X.some(function (x) { return x.dev === od; })) R.push([String(p).split('/').pop(), 'n/a', od.st.serial, 'UNACTIVATED', 'n/a', 'n/a', 'n/a']); }
      X.filter(function (x) { return x.pp === p; }).forEach(function (x) {
        if (kind === 'configured') R.push([String(p).split('/').pop(), x.id, x.o.serial || 'n/a', x.dev ? 'OK' : 'OFFLINE', x.o.desc || 'n/a']);
        if (kind === 'online' && x.dev) R.push([String(p).split('/').pop(), x.id, x.o.serial, 'OK', '-18.50', 'n/a', String((EL.MODELS[x.dev.model] || {}).swv || 'n/a')]);
        if (kind === 'offline' && !x.dev) R.push([String(p).split('/').pop(), x.id, x.o.serial || 'n/a', 'OFFLINE', x.o.desc || 'n/a']); });
      var bySlot = (st.olt.dl === 'ma5000' && String(w).indexOf('/') < 0) || st.olt.dl === 'ltp-x';   // MA5000: «show interface ont 4 …» — порты слота 4, пустые не выводятся
      if (!R.length && pp.length > 1) { if (!bySlot) out.push('PON-port ' + p + ' has no ' + kind + ' ONTs'); return; }
      rows = rows.concat(R); if (pp.length === 1 || bySlot) out.push(dash((st.olt.dl === 'ltp-x' ? 'GPON-port ' : 'pon-port ') + p + ' ONT ' + kind + ' list'), H);
      if (st.olt.dl === 'ltp-x') { R.forEach(function (r) { var n = rows.indexOf(r) + 1;   // ПО 3.52: Serial ONT-ID GPON-port Status RSSI Version EquipmentID Description
        out.push(n + ' ' + [r[2] === 'n/a' ? r[2] : snHex(r[2]), r[1], r[0], r[3]].concat(kind === 'configured' || kind === 'offline' ? [r[4]] : [r[4] || 'n/a', r[6] || 'n/a', r[5] || 'n/a', 'n/a']).join(' ')); }); return; }
      R.forEach(function (r) { var n = rows.indexOf(r) + 1; out.push(n + ' ' + r.slice(0, kind === 'offline' ? 4 : 5).join(' ') + (r.length > 5 ? '\n' + r.slice(5).join(' ') : kind === 'offline' ? '\n' + r[4] : '')); }); });
    out.push('Total ONT count: ' + rows.length); return out.join('\n'); }
  ['unactivated', 'configured', 'online', 'offline'].forEach(function (k) { cmd('root', 'show interface ont <w> ' + k, function (st, a) { return st.net ? list(st, a[0], k) : ''; }, 'Список ONT: ' + k); });
  cmd('root', 'show interface ont <w> unconfigured', function (st, a) { var p = a[0], used = Object.keys(st.olt.run.ont).filter(function (k) { return k.replace(/\/\d+$/, '') === p; }).map(function (k) { return +k.split('/').pop(); }); if (!st.ports['pon-port ' + p]) return ERR;
    var free = []; for (var i = 1; i <= maxOnt(st, p); i++) if (used.indexOf(i) < 0) free.push(i); return 'pon-port ' + p + ' ONT unconfigured: ' + E.fmtList(free); });
  cmd('root', 'show interface ont <w> state', function (st, a) { var x = onts(st.net, st.net.devs[st.dev]).filter(function (y) { return y.key === a[0]; })[0]; if (!x) return ERR;
    return [dash('[ONT ' + a[0] + '] state'), 'Serial number: ' + (x.o.serial || 'n/a'), 'Pon-port: ' + x.pp, 'ONT ID: ' + x.id, 'Equipment ID: n/a',
      'Current software version: ' + (x.dev ? (EL.MODELS[x.dev.model] || {}).swv : 'n/a'), 'State: ' + (x.dev ? 'OK' : 'OFFLINE'), 'RSSI: ' + (x.dev ? '-18.50 [dBm]' : 'n/a')].join('\n'); });
  cmd('root', 'show interface front-port <w> state', function (st, a) { var k = 'front-port ' + a[0]; if (!st.ports[k]) return ERR;
    return k + ': ' + (st.net && st.net.linkUp(st.dev, k) ? 'up' : 'down'); }, 'Состояние front-port');
  // MA5160/MA5020: состав шасси (вставлена одна LC16G — допущение эмулятора)
  cmd('root', 'show shelf', function (st) { if (st.olt.dl !== 'ma5000') return ERR; var r = st.olt.run.slots || {}, n = st.olt.slots || 16, have = {};
    Object.keys(st.ports).forEach(function (k) { var m = k.match(/^pon-port (\d+)\//); if (m) have[m[1]] = 1; });
    var o = ['## Configured Detected Serial number Rev. Uptime Status', '--- ---------- ---------- ------------- ----- -------- ---------------'];
    for (var i = 1; i <= n; i++) { var t = (r[i] || {}).type, det = have[i] ? 'MA5K-LC16G' : '-', ok = have[i] && t === 'lc16g';
      o.push(i + ' ' + (t && t !== 'unknown' ? t.toUpperCase() : 'Not set') + ' ' + det + ' ' + (have[i] ? 'OL1400003' + i + ' 1v1' : '- -') + ' ' + (ok ? '- running' : have[i] ? '- present' : '- -')); }
    return o.join('\n'); }, 'Состав шасси: слоты и линейные карты');
  cmd('root', 'show mac', function (st) { return st.net ? st.net.macTable(st.dev) : ''; }, 'Таблица MAC-адресов');
  cmd('root', 'ping <ip>', function (st, a) { return st.net ? st.net.pingText(st.dev, a[0], 'linux') : ''; }, 'Проверка связи с адреса управления');

  function exec(st, raw) {
    var line = String(raw).trim(), o = st.olt, m = line.match(/^do\s+(.+)$/i);
    if (m && o.mode !== 'root') { var md = o.mode, cx = o.ctx; o.mode = 'root'; var r = EL.cli.runTable(T, { mode: 'root', olt: o, net: st.net, dev: st.dev, ports: st.ports, dialect: o.dl }, m[1]); if (o.mode === 'root') { o.mode = md; o.ctx = cx; } return r; }
    var proxy = { get mode() { return o.mode; }, olt: o, net: st.net, dev: st.dev, ports: st.ports, dialect: o.dl };
    return EL.cli.runTable(T, proxy, line);
  }
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id];
    if (isOlt(d)) { this.gen++; if (d.off) return ''; if (/\?\s*$/.test(line)) return T.filter(function (c) { return c.modes.indexOf(d.st.olt.mode) >= 0; }).map(function (c) { return '  ' + c.pat.join(' '); }).join('\n');
      return exec(d.st, line); }
    if (isOnt(d)) return '';
    return ex0.apply(this, arguments); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; if (isOlt(d)) return prompt(d.st); if (isOnt(d)) return ''; return pr0.apply(this, arguments); };
  // перезагрузка: running = NVRAM
  var boot0 = P.reboot;
  if (boot0) P.reboot = function (id) { var d = this.devs[id], keep = d && { olt: d.st.olt, serial: d.st.serial, users: d.st.users };   // состояние MES пересоздаётся — данные OLT/ONT сохраняем
    var r = boot0.apply(this, arguments); d = this.devs[id];
    if (isOlt(d)) { var o = keep.olt; o.run = EL.clone(o.nv); o.cand = EL.clone(o.nv); o.mode = 'root'; o.ctx = null; d.st.olt = o; d.st.users = keep.users; d.st.stp = { on: false }; d.st.mode = 'priv'; }
    if (isOnt(d)) { d.st.serial = keep.serial; d.st.stp = { on: false }; }
    this.gen++; return r; };
  // ---------------------------------------------------------------- LTP-4X/8X (ПО 3.52): встроенный коммутатор и синтаксис 3.52
  // switch → configure → vlan N → tagged front-port 0 / tagged pon-port 0-7 → commit; профили — (config-cross-connect)("ИМЯ")#; bridge вместо ont-mode bridge;
  // нумерация с нуля (gpon-port 0, ONT 0/0–0/127, service 0–28, port 0); rollback без аргумента. VLAN front-port берутся из коммутатора.
  var X = ['ltp-x'];
  function xc(modes, pat, run, d) { cmd(modes, pat, run, d); T[T.length - 1].dl = X; T.unshift(T.pop()); }
  T.forEach(function (c) { var p = c.pat.join(' '); if (/^interface (pon-port|front-port) |^slot |^confirm|^commit confirm|^rollback candidate-config|^restore running-config|^ont-mode /.test(p)) c.xdl = (c.xdl || []).concat(X); });
  function SW(st) { var c = C(st); return c.sw || (c.sw = { vlans: {} }); }
  function nlist(w) { var t = String(w).replace(/[–—]/g, '-').replace(/\s+/g, ''), L = []; t.split(',').forEach(function (x) { var m = x.match(/^(\d+)(?:-(\d+))?$/); if (m) for (var i = +m[1]; i <= +(m[2] || m[1]); i++) L.push(i); }); return L; }
  xc('root', 'switch', function (st) { st.olt.mode = 'sw'; }, 'Встроенный коммутатор (VLAN uplink)');
  xc('root', 'rollback', function (st) { st.olt.cand = EL.clone(st.olt.run); }, 'Отменить изменения');
  xc('root', 'send omci restore interface ont <w>', function () { return ''; });
  xc('sw', 'configure', function (st) { st.olt.mode = 'swcfg'; }); xc('sw', 'configure terminal', function (st) { st.olt.mode = 'swcfg'; });
  xc('sw', 'exit', function (st) { st.olt.mode = 'root'; });
  xc('sw', 'show vlan <n>', function (st, a) { var v = (st.olt.run.sw || { vlans: {} }).vlans[a[0]]; if (!v) return ERR;
    return 'VLAN ' + a[0] + '\ntagged: ' + v.front.map(function (x) { return 'front-port ' + x; }).concat(v.pon.map(function (x) { return 'pon-port ' + x; })).join(', '); });
  xc('swcfg', 'vlan <list>', function (st, a) { var V = SW(st).vlans; a[0].forEach(function (v) { V[v] = V[v] || { front: [], pon: [] }; }); st.olt.mode = 'swvlan'; st.olt.ctx = E.fmtList(a[0]); }, 'VLAN коммутатора');
  xc('swcfg', 'interface front-port <n>', function (st, a) { st.olt.mode = 'swif'; st.olt.ctx = 'front-port ' + a[0]; });
  xc('swcfg', 'interface port-channel <n>', function (st, a) { st.olt.mode = 'swif'; st.olt.ctx = 'port-channel ' + a[0]; });
  xc('swcfg', 'commit', function (st) { st.olt.run.sw = EL.clone(SW(st)); if (st.net) st.net.gen++; return ''; }, 'Принять изменения коммутатора');
  xc('swcfg', 'exit', function (st) { st.olt.mode = 'sw'; st.olt.ctx = null; });
  function vl(st) { return nlist(st.olt.ctx).map(function (v) { return SW(st).vlans[v]; }); }
  function tag(kind, add) { return function (st, a) { var L = nlist(a[0]), max = Object.keys(st.ports).filter(function (k) { return k.indexOf(kind === 'front' ? 'front-port ' : 'gpon-port ') === 0; }).length;
    if (!L.length || L.some(function (x) { return x >= max; })) return ERR;
    vl(st).forEach(function (v) { L.forEach(function (x) { var A = v[kind], i = A.indexOf(x); if (add && i < 0) A.push(x); if (!add && i >= 0) A.splice(i, 1); }); }); }; }
  xc('swvlan', 'tagged front-port <rest>', tag('front', true), 'Порт uplink — с тегом');
  xc('swvlan', 'tagged pon-port <rest>', tag('pon', true), 'PON-порты — с тегом (0 – 7)');
  xc('swvlan', 'no tagged front-port <rest>', tag('front', false)); xc('swvlan', 'no tagged pon-port <rest>', tag('pon', false));
  xc('swvlan', 'exit', function (st) { st.olt.mode = 'swcfg'; st.olt.ctx = null; });
  xc('swif', 'exit', function (st) { st.olt.mode = 'swcfg'; st.olt.ctx = null; });
  xc('swif', '<rest>', function () { return ''; });
  xc('configure', 'interface gpon-port <w>', enter('pon', function (st, a) { return portIds(st, 'gpon-port', a[0]) ? a[0] : null; }), 'GPON-порт');
  xc('configure', 'gpon olt model <n>', function (st, a) { if (a[0] < 0 || a[0] > 2) return ERR; C(st).model = a[0]; }, 'Модель datapath');
  xc('cc', 'bridge', function (st) { cc(st).mode = 'bridge'; }, 'ONT в режиме моста');
  xc('cc', 'user vid untagged', function (st) { delete cc(st).user; });
  xc('cc', 'type <w>', function (st, a) { if (['management', 'multicast'].indexOf(a[0]) < 0) return ERR; cc(st).type = a[0]; });
  ['veip multicast', 'veip upstream vid <n>', 'veip downstream vid <n>', 'igmp multicast dynamic-entry <n> vid <n>', 'igmp multicast dynamic-entry <n> group <ip> <ip>'].forEach(function (p) {
    xc('pp', p, function (st, a, line) { var o = C(st).pp[st.olt.ctx]; (o.L = o.L || []).push(line); }); });
  EL.olt = { T: T, exec: exec, prompt: prompt };
})(typeof window !== 'undefined' ? window : global);
