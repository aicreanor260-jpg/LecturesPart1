/* Коммутаторы Cisco Catalyst (2960-24TT, 2950-24, 3560-24PS) — спецификация sources/cisco/spec/switch-ios.md (CG/CR 2960-X, 9300).
   Настройки IOS (st.ios.c) → поля модели MES. Значения по умолчанию по документации:
   — порт: switchport mode dynamic auto (DTP), access VLAN 1, native 1, allowed 1–4094; транк поднимается по DTP:
     trunk/desirable с одной стороны и auto/desirable с другой (auto–auto — access); с не-Cisco (нет DTP) dynamic-порт — access;
   — VTP: server, домен пустой, версия 1; VLAN сервера с бо́льшей ревизией расходятся по транкам между Cisco того же домена
     (пустой домен принимает домен соседа), client VLAN не создаёт, transparent не участвует;
   — STP: PVST+ (до 15.2(4)E, у образов Packet Tracer 12.x/15.0), дерево на каждую VLAN (в модели — экземпляр на VLAN, все Cisco в одном
     «регионе»; с Huawei/Eltex стык по VLAN 1 — CST), приоритет 32768, стоимость short (FE 19, GE 4), PortFast выключен;
     root primary / secondary → 24576 / 28672 (в собранных документах значений нет — общеизвестные);
   — EtherChannel: PAgP auto/desirable, LACP active/passive, on; auto–auto и passive–passive не поднимаются; PAgP с LACP несовместим;
   — CDP включён (60/180 с), LLDP выключен; ip routing выключен (2960 — L2, ip default-gateway).
   Упрощения: VTP pruning и версии v2/v3 не моделируются; routed port на 3560 (no switchport) — скрытая VLAN 4000+ с SVI. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, I = EL.ios, cmd = I.cmd, pad = I.pad, full = I.full, short = I.short, P = EL.Net.prototype;
  function SW(st) { return st.ios.kind === 'sw'; }
  function sc(views, pat, run, d) { var e = cmd(views, pat, run, d); e.ok = SW; return e; }
  function C(st) { return st.ios.c; }
  function top(st) { return I.top(st); }
  function each(st, f) { var bad = false, N = I.curNames(st); I.cur(st).forEach(function (x, i) { if (f(x, N[i]) === false) bad = true; }); return bad ? null : undefined; }
  function phys(n) { return /^(fa|gi|eth)\d+(\/\d+){1,2}$/.test(n); }
  function vlans(st) { var c = C(st); return c.vlans || (c.vlans = {}); }
  function bump(st) { var c = C(st); c.vtp = c.vtp || {}; if ((c.vtp.mode || 'server') === 'server') c.vtp.rev = (c.vtp.rev || 0) + 1; }
  function vtpMode(st) { return ((C(st).vtp || {}).mode) || 'server'; }

  // ---------------------------------------------------------------- VLAN
  sc('config', 'vlan <list>', function (st, a) { if (a[0].some(function (v) { return v < 1 || v > 4094 || v >= 1002 && v <= 1005; })) return null;
    if (vtpMode(st) === 'client') return 'VTP VLAN configuration not allowed when device is in CLIENT mode.';
    a[0].forEach(function (v) { if (v !== 1 && !vlans(st)[v]) { vlans(st)[v] = {}; bump(st); } }); I.push(st, { v: 'vlan', ids: a[0] }); }, 'Vlan commands');
  sc('config', 'no vlan <list>', function (st, a) { if (vtpMode(st) === 'client') return 'VTP VLAN configuration not allowed when device is in CLIENT mode.';
    if (a[0].indexOf(1) >= 0) return '%Default VLAN 1 may not be deleted.'; a[0].forEach(function (v) { delete vlans(st)[v]; }); bump(st); });
  sc('vlan', 'name <w>', function (st, a) { top(st).ids.forEach(function (v) { if (v !== 1) vlans(st)[v].name = a[0]; }); bump(st); }, 'Ascii name of the VLAN');
  sc('vlan', 'no name', function (st) { top(st).ids.forEach(function (v) { if (vlans(st)[v]) delete vlans(st)[v].name; }); });
  // ---------------------------------------------------------------- interface / range
  sc('config', 'interface range <rest>', function (st, a) {                  // fa0/1 - 5, fa0/7 - 8 ; gi0/1 - 2
    var ports = st.net ? I.dports(st.net, st.net.devs[st.dev]) : [], L = [], ok = true;
    a[0].split(',').forEach(function (part) { var t = I.norm(part.trim()), m = (t[0] || '').match(/^((?:fa|gi|eth)\d+(?:\/\d+)*\/)(\d+)(?:-(?:(?:eth)?\d+\/\d+\/)?(\d+))?$/); if (!m) { ok = false; return; }
      var to = m[3] || (t[1] === '-' ? t[2] : null) || m[2]; for (var i = +m[2]; i <= +to; i++) { if (ports.indexOf(m[1] + i) < 0) { ok = false; return; } L.push(m[1] + i); } });
    if (!ok || !L.length) return null; L.forEach(function (n) { I.ifc(st, n); }); I.push(st, { v: 'range', name: L[0], names: L }); });
  sc('config', 'interface <if>', function (st, a) { var n = a[0], ports = st.net ? I.dports(st.net, st.net.devs[st.dev]) : [];
    if (/^(fa|gi|eth)/.test(n) && ports.indexOf(n) < 0) return null; if (/^lo/.test(n) && !st.ios.l3) return null; if (/^vlan/.test(n) && (+n.slice(4) < 1 || +n.slice(4) > 4094)) return null;
    I.ifc(st, n); I.push(st, { v: 'if', name: n }); }, 'Select an interface to configure');
  sc('config', 'no interface <if>', function (st, a) { if (/^(fa|gi|eth)/.test(a[0]) || a[0] === 'vlan1') return null; delete C(st).ifs[a[0]]; });
  function l2(f) { return function (st, a) { return each(st, function (x, n) { if (!(phys(n) || /^po/.test(n)) || x.routed) return false; return f(x, a, n); }); }; }
  sc('if range', 'switchport mode access', l2(function (x) { x.mode = 'access'; }), 'Set trunking mode of the interface');
  sc('if range', 'switchport mode trunk', l2(function (x) { x.mode = 'trunk'; }));
  sc('if range', 'switchport mode dynamic auto', l2(function (x) { delete x.mode; }));
  sc('if range', 'switchport mode dynamic desirable', l2(function (x) { x.mode = 'desirable'; }));
  sc('if range', 'no switchport mode', l2(function (x) { delete x.mode; }));
  sc('if range', 'switchport nonegotiate', l2(function (x) { if (!x.mode || x.mode === 'desirable') return false; x.noneg = true; }));
  sc('if range', 'no switchport nonegotiate', l2(function (x) { delete x.noneg; }));
  sc('if range', 'switchport access vlan <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return null;
    var r = l2(function (x) { x.av = a[0]; })(st, a); if (r !== null && !vlans(st)[a[0]] && a[0] !== 1 && vtpMode(st) !== 'client') { vlans(st)[a[0]] = {}; bump(st); return '% Access VLAN does not exist. Creating vlan ' + a[0]; } return r; }, 'Set access mode characteristics');
  sc('if range', 'no switchport access vlan', l2(function (x) { delete x.av; }));
  sc('if range', 'switchport trunk native vlan <n>', l2(function (x, a) { if (a[0] < 1 || a[0] > 4094) return false; x.nv = a[0]; }));
  sc('if range', 'no switchport trunk native vlan', l2(function (x) { delete x.nv; }));
  sc('if range', 'switchport trunk allowed vlan all', l2(function (x) { delete x.allow; }));
  sc('if range', 'switchport trunk allowed vlan none', l2(function (x) { x.allow = []; }));
  sc('if range', 'switchport trunk allowed vlan add <list>', l2(function (x, a) { if (x.allow) x.allow = uniq(x.allow.concat(a[0])); }));
  sc('if range', 'switchport trunk allowed vlan remove <list>', l2(function (x, a) { x.allow = (x.allow || range(1, 4094)).filter(function (v) { return a[0].indexOf(v) < 0; }); }));
  sc('if range', 'switchport trunk allowed vlan except <list>', l2(function (x, a) { x.allow = range(1, 4094).filter(function (v) { return a[0].indexOf(v) < 0; }); }));
  sc('if range', 'switchport trunk allowed vlan <list>', l2(function (x, a) { x.allow = uniq(a[0]); }));
  sc('if range', 'switchport trunk encapsulation dot1q', l2(function () {}));
  sc('if range', 'switchport port-security', l2(function (x) { x.psec = true; }));
  sc('if range', 'switchport port-security maximum <n>', l2(function (x, a) { x.psecMax = a[0]; }));
  sc('if range', 'switchport port-security mac-address sticky', l2(function (x) { x.psecSticky = true; }));
  sc('if range', 'switchport port-security violation <w>', l2(function (x, a) { x.psecV = a[0].toLowerCase(); }));
  sc('if range', 'spanning-tree portfast', l2(function (x) { x.portfast = true; }), 'Spanning Tree Subsystem');
  sc('if range', 'spanning-tree portfast edge', l2(function (x) { x.portfast = true; }));
  sc('if range', 'no spanning-tree portfast', l2(function (x) { delete x.portfast; }));
  sc('if range', 'spanning-tree bpduguard enable', l2(function (x) { x.bpduguard = true; }));
  sc('if range', 'no spanning-tree bpduguard', l2(function (x) { delete x.bpduguard; }));
  sc('if range', 'spanning-tree cost <n>', l2(function (x, a) { if (a[0] < 1) return false; x.cost = a[0]; }));
  sc('if range', 'no spanning-tree cost', l2(function (x) { delete x.cost; }));
  sc('if range', 'spanning-tree vlan <list> cost <n>', l2(function (x, a) { x.vcost = x.vcost || {}; a[0].forEach(function (v) { x.vcost[v] = a[1]; }); }));
  sc('if range', 'channel-group <n> mode <w>', function (st, a) { var m = a[1].toLowerCase(); if (['on', 'active', 'passive', 'auto', 'desirable'].indexOf(m) < 0 || a[0] < 1 || a[0] > 48) return null;
    var c = C(st), po = 'po' + a[0], r = each(st, function (x, n) { if (!phys(n)) return false; x.cg = { id: a[0], mode: m }; }); if (r === null) return null;
    if (!c.ifs[po]) { c.ifs[po] = {}; var f = I.cur(st)[0]; ['mode', 'av', 'nv', 'allow', 'noneg'].forEach(function (k) { if (f[k] !== undefined) c.ifs[po][k] = EL.clone(f[k]); });
      return 'Creating a port-channel interface Port-channel ' + a[0]; } }, 'Etherchannel/port bundling configuration');
  sc('if range', 'no channel-group', function (st) { return each(st, function (x) { delete x.cg; }); });
  sc('if range', 'no switchport', function (st) { if (!st.ios.l3) return null; return each(st, function (x, n) { if (!phys(n)) return false; x.routed = true; }); });
  sc('if range', 'switchport', function (st) { return each(st, function (x) { delete x.routed; delete x.ip; }); });
  // ---------------------------------------------------------------- VTP, STP, IP
  function vtp(st) { var c = C(st); return c.vtp || (c.vtp = {}); }
  sc('config', 'vtp mode <w>', function (st, a) { var m = a[0].toLowerCase(); if (['server', 'client', 'transparent', 'off'].indexOf(m) < 0) return null;
    var v = vtp(st); if (m === 'server') delete v.mode; else v.mode = m; return 'Setting device to VTP ' + m.toUpperCase() + ' mode.'; }, 'Configure VLAN database');
  sc('config', 'vtp domain <w>', function (st, a) { vtp(st).domain = a[0]; return 'Changing VTP domain name from ' + (vtp(st).was || 'NULL') + ' to ' + a[0]; });
  sc('config', 'vtp password <w>', function (st, a) { vtp(st).pw = a[0]; return 'Setting device VLAN database password to ' + a[0]; });
  sc('config', 'vtp version <n>', function (st, a) { if (a[0] < 1 || a[0] > 3) return null; vtp(st).ver = a[0]; });
  function stp(st) { var c = C(st); return c.stp || (c.stp = {}); }
  sc('config', 'spanning-tree mode <w>', function (st, a) { var m = a[0].toLowerCase(); if (['pvst', 'rapid-pvst', 'mst'].indexOf(m) < 0) return null; stp(st).mode = m; }, 'Spanning Tree Subsystem');
  sc('config', 'no spanning-tree mode', function (st) { delete stp(st).mode; });
  sc('config', 'spanning-tree vlan <list> priority <n>', function (st, a) { if (a[1] > 61440 || a[1] % 4096) return '% Bridge Priority must be in increments of 4096.\n% Allowed values are:\n  0     4096  8192  12288 16384 20480 24576 28672\n  32768 36864 40960 45056 49152 53248 57344 61440';
    var s = stp(st); s.prio = s.prio || {}; s.root = s.root || {}; a[0].forEach(function (v) { s.prio[v] = a[1]; delete s.root[v]; }); });
  sc('config', 'spanning-tree vlan <list> root <w>', function (st, a) { var w = a[1].toLowerCase(); if (['primary', 'secondary'].indexOf(w) < 0) return null;
    var s = stp(st); s.prio = s.prio || {}; s.root = s.root || {}; a[0].forEach(function (v) { s.root[v] = w; delete s.prio[v]; }); });
  sc('config', 'no spanning-tree vlan <list> priority', function (st, a) { var s = stp(st); a[0].forEach(function (v) { if (s.prio) delete s.prio[v]; }); });
  sc('config', 'no spanning-tree vlan <list> root', function (st, a) { var s = stp(st); a[0].forEach(function (v) { if (s.root) delete s.root[v]; }); });
  sc('config', 'no spanning-tree vlan <list>', function (st, a) { var s = stp(st); s.off = s.off || []; a[0].forEach(function (v) { if (s.off.indexOf(v) < 0) s.off.push(v); }); });
  sc('config', 'spanning-tree vlan <list>', function (st, a) { var s = stp(st); s.off = (s.off || []).filter(function (v) { return a[0].indexOf(v) < 0; }); });
  sc('config', 'spanning-tree portfast default', function (st) { stp(st).pfDefault = true; });
  sc('config', 'ip default-gateway <ip>', function (st, a) { C(st).gw = a[0]; }, 'Specify default gateway (if not routing IP)');
  sc('config', 'no ip default-gateway', function (st) { delete C(st).gw; });
  sc('config', 'ip routing', function (st) { if (!st.ios.l3) return null; C(st).routing = true; }, 'Enable IP routing');
  sc('config', 'no ip routing', function (st) { delete C(st).routing; });
  sc('config', 'ip route <ip> <ip> <ip>', function (st, a) { var l = IP.mask2len(a[1]); if (l === null || !st.ios.l3) return null; var c = C(st);
    c.routes = (c.routes || []).filter(function (r) { return !(r.net === IP.netOf(a[0], l) && r.nh === a[2]); }); c.routes.push({ net: IP.netOf(a[0], l), nh: a[2] }); }, 'Establish static routes');
  sc('config', 'no ip route <ip> <ip> <ip>', function (st, a) { var l = IP.mask2len(a[1]), c = C(st); c.routes = (c.routes || []).filter(function (r) { return !(r.net === IP.netOf(a[0], l) && r.nh === a[2]); }); });
  sc('config', 'mac address-table aging-time <n>', function (st, a) { C(st).macAge = a[0]; });
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }).sort(function (x, y) { return x - y; }); }
  function range(a, b) { var o = []; for (var i = a; i <= b; i++) o.push(i); return o; }

  // ---------------------------------------------------------------- compile: IOS → модель MES
  var PF = { 24576: 1, 28672: 1 };
  function shortCost(n, costs) { var fa = /^fa/.test(n); return costs === 'long' ? (fa ? 200000 : 20000) : (fa ? 19 : 4); }
  function port(P0, x, n, st) {
    var P = P0; P.shut = !!x.shut; if (x.desc) P.desc = x.desc; else delete P.desc;
    P.admin = x.mode || 'auto'; P.noneg = !!x.noneg;
    P.access = x.av || 1; P.native = x.nv || 1; P.allowed = x.allow ? x.allow.slice() : range(1, 4094); P.allAll = !x.allow;
    P.pvid = P.access; P.gtag = []; P.guntag = [P.access];
    P.mode = P.admin === 'trunk' ? 'trunk' : 'access';            // уточняется DTP по соседу (dtpSync)
    P.stpCost = x.cost || shortCost(n, st.ios.costs); if (x.vcost) P.mstCost = EL.clone(x.vcost); else delete P.mstCost;
    P.portfast = !!x.portfast || (!!(C(st).stp || {}).pfDefault && P.admin === 'access'); P.noAutoEdge = true; P.bpduGuard = !!x.bpduguard;
    return P;
  }
  EL.ios.compileSw = function (st) {
    var c = C(st), net = st.net, d = net && net.devs[st.dev], ports = d ? I.dports(net, d) : Object.keys(st.ports).filter(phys), x = st.ios;
    st.host = c.hostname || 'Switch';
    var own = { 1: '-' }; Object.keys(c.vlans || {}).forEach(function (v) { own[v] = c.vlans[v].name || '-'; });
    x.ownVlans = own; st.vlans = EL.clone(x.vtpVlans && vtpMode(st) !== 'transparent' && vtpMode(st) !== 'off' ? x.vtpVlans : own);
    st.svi = {}; st.sviShut = {}; var hid = 4000;
    ports.forEach(function (p) { var y = c.ifs[p] || {}, Pp = port(st.ports[p] || (st.ports[p] = {}), y, p, st);
      if (y.cg && c.ifs['po' + y.cg.id]) Pp.cg = { id: y.cg.id, mode: y.cg.mode === 'desirable' ? 'pagp-d' : y.cg.mode === 'auto' ? 'pagp-a' : y.cg.mode }; else delete Pp.cg;
      if (y.routed) { hid++; st.vlans[hid] = '-'; Pp.mode = 'access'; Pp.admin = 'access'; Pp.access = hid; Pp.routedVlan = hid; if (y.ip) st.svi[hid] = y.ip[0] + '/' + y.ip[1]; if (y.shut) st.sviShut[hid] = true; }
      else delete Pp.routedVlan; });
    st.pos = {};
    Object.keys(c.ifs).forEach(function (k) { var m;
      if ((m = k.match(/^po(\d+)$/))) st.pos[k] = port({}, c.ifs[k], k, st);
      if ((m = k.match(/^vlan(\d+)$/)) && c.ifs[k].ip) { st.svi[m[1]] = c.ifs[k].ip[0] + '/' + c.ifs[k].ip[1]; if (EL.ios.isShut(st, k, c.ifs[k])) st.sviShut[m[1]] = true; } });
    st.routes = (c.routes || []).map(function (r) { return { net: r.net, nh: r.nh, ad: 1 }; }); st.gw = c.routing ? null : c.gw || null; st.routing = !!c.routing;
    var s = c.stp || {}, pr = s.prio || {}, rt = s.root || {}, rp = function (v) { return rt[v] === 'primary' ? 24576 : rt[v] === 'secondary' ? 28672 : pr[v] !== undefined ? pr[v] : 32768; };
    st.stp = { on: (s.off || []).indexOf(1) < 0, mode: { pvst: 'stp', 'rapid-pvst': 'rst', mst: 'mst' }[s.mode || 'pvst'], prio: rp(1), pvst: s.mode !== 'mst' };
    var inst = {}; Object.keys(st.vlans).map(Number).forEach(function (v) { if (v !== 1 && v < 4000) inst[v] = { vlans: [v], prio: rp(v) }; });
    st.mst = { name: 'cisco-pvst', rev: 0, inst: st.stp.pvst ? inst : {} };
    st.macAge = c.macAge || 300; void PF;
  };
  EL.ios.isShut = (function (o) { return function (st, k, x) { if (/^vlan1$/.test(k) && st.ios.kind === 'sw') return !x.noShut; return o(st, k, x); }; })(EL.ios.isShut);
  EL.ios.ifUp = (function (o) { return function (st, k, x) { if (/^vlan\d+$/.test(k)) return !!st.net && st.net.ifaces(st.dev).some(function (f) { return f.name === k; });
    if (/^po\d+$/.test(k)) return !!st.net && st.net.lports(st.dev).some(function (L) { return L.name === k && L.members.length; }); return o(st, k, x); }; })(EL.ios.ifUp);

  // ---------------------------------------------------------------- сеть: DTP, VTP, PVST+, PAgP
  function isSw(d) { return I.isIos(d) && d.type === 'mes' && !d.st.ios.dl; }   // Catalyst (у D-Link нет DTP, VTP, PVST+)
  function cport(d, p) { return d && d.st.ports && d.st.ports[p]; }
  function trunkUp(a, b) {                       // DTP (CG-2960X Trunks Table 1): access — никогда; trunk — всегда (сосед auto/desirable тоже станет транком)
    if (a.admin === 'access') return false; if (a.admin === 'trunk') return true;
    if (!b) return false; if (b.admin === 'access' || b.noneg) return false;
    return b.admin === 'trunk' || b.admin === 'desirable' || a.admin === 'desirable' && b.admin === 'auto';
  }
  function dtpSync(net) {
    if (net._dtpGen === net.gen) return; net._dtpGen = net.gen;
    var sws = net.list().filter(function (d) { return isSw(d) && !d.off; });
    if (!sws.length) return;
    sws.forEach(function (d) { Object.keys(d.st.ports).forEach(function (p) { var A = d.st.ports[p]; if (!A.admin || A.routedVlan) return;
      var pr = net.peer(d.id, p), pd = pr && net.devs[pr.dev], B = pd && isSw(pd) ? cport(pd, pr.port) : null;
      A.mode = trunkUp(A, B) ? 'trunk' : 'access'; });
      Object.keys(d.st.pos || {}).forEach(function (k) { var A = d.st.pos[k], mem = Object.keys(d.st.ports).filter(function (p) { var c = d.st.ports[p].cg; return c && 'po' + c.id === k; });
        A.mode = mem.some(function (p) { return d.st.ports[p].mode === 'trunk'; }) || A.admin === 'trunk' ? 'trunk' : 'access'; }); });
    // VTP: компоненты по транкам между Cisco; в каждой — VLAN сервера/клиента с наибольшей ревизией того же домена
    var seen = {};
    sws.forEach(function (d0) { if (seen[d0.id]) return; var comp = [], q = [d0]; seen[d0.id] = true;
      while (q.length) { var d = q.shift(); comp.push(d);
        Object.keys(d.st.ports).forEach(function (p) { if (d.st.ports[p].mode !== 'trunk' || !net.linkUp(d.id, p)) return; var pr = net.peer(d.id, p), pd = pr && net.devs[pr.dev];
          if (pd && isSw(pd) && !pd.off && !seen[pd.id] && cport(pd, pr.port) && cport(pd, pr.port).mode === 'trunk') { seen[pd.id] = true; q.push(pd); } }); }
      var part = comp.filter(function (d) { var m = vtpMode(d.st); return m === 'server' || m === 'client'; });
      var dom = part.map(function (d) { return (d.st.ios.c.vtp || {}).domain; }).filter(Boolean)[0] || null;
      var mem = part.filter(function (d) { var x = (d.st.ios.c.vtp || {}).domain; return !x || x === dom; });
      var win = mem.slice().sort(function (a, b) { return ((b.st.ios.c.vtp || {}).rev || 0) - ((a.st.ios.c.vtp || {}).rev || 0); })[0];
      mem.forEach(function (d) { var x = d.st.ios; var nv = win && dom ? EL.clone(win.st.ios.ownVlans) : null;
        if (JSON.stringify(x.vtpVlans || null) !== JSON.stringify(nv)) { x.vtpVlans = nv; x.vtpDomain = dom; x.vtpRev = win ? ((win.st.ios.c.vtp || {}).rev || 0) : 0;
          var keep = {}; Object.keys(d.st.vlans).forEach(function (v) { if (+v >= 4000) keep[v] = d.st.vlans[v]; });
          d.st.vlans = Object.assign(EL.clone(nv && vtpMode(d.st) !== 'transparent' ? nv : x.ownVlans), keep); } }); });
    // PVST+: экземпляр VLAN начинает отсчёт таймеров портов с момента настройки, а не с первого кадра
    if (net.stpState) sws.forEach(function (d) { if (!d.st.stp.pvst || d.st.stp.on === false) return;
      Object.keys(d.st.vlans).map(Number).forEach(function (v) { if (v === 1 || v >= 4000) return; net.lports(d.id).forEach(function (L) { net.stpState(d.id, L.name, v); }); }); });
  }
  ['flood', 'stp', 'lports', 'ping', 'request', 'dyn'].forEach(function (m) { var f = P[m]; P[m] = function () { dtpSync(this); return f.apply(this, arguments); }; });
  var inst0 = P.stpInst;                          // PVST+: дерево на каждую VLAN (VLAN 1 — общее с не-Cisco)
  P.stpInst = function (id, v) { var d = this.devs[id]; if (isSw(d) && d.st.stp.pvst) return !v || v === 1 ? 0 : v; return inst0.apply(this, arguments); };
  var reg0 = P.mstRegion;
  P.mstRegion = function (id) { var d = this.devs[id]; if (isSw(d) && d.st.stp.pvst) return 'cisco-pvst'; return reg0 ? reg0.apply(this, arguments) : ''; };
  // PAgP (desirable/auto) несовместим с LACP и on; auto–auto не поднимается — пересчёт членов агрегата
  function pagp(m) { return /^pagp/.test(m || ''); }
  var lp0 = P.lports;
  P.lports = function (id) {
    var L = lp0.apply(this, arguments), d = this.devs[id], s = this;
    if (!d || d.type !== 'mes' || !Object.keys(d.st.ports).some(function (p) { var c = d.st.ports[p].cg; if (c && pagp(c.mode)) return true;
      var pr = c && s.peer(id, p), pd = pr && s.devs[pr.dev], pc = pd && pd.type === 'mes' && pd.st.ports[pr.port] && pd.st.ports[pr.port].cg; return !!(pc && pagp(pc.mode)); })) return L;
    var out = L.filter(function (x) { return !/^po/.test(x.name); }), po = {};
    s.portsOf(d).filter(function (p) { return d.st.ports[p]; }).forEach(function (p) { var c = d.st.ports[p].cg; if (!c) return;
      var k = 'po' + c.id; po[k] = po[k] || { name: k, cfg: (d.st.pos || {})[k], members: [], down: [] };
      var pr = s.peer(id, p), ok = false;
      if (pr && s.linkUp(id, p)) { var pd = s.devs[pr.dev], px = pd.type === 'mes' && pd.st.ports[pr.port];
        if (px && px.cg) { var a = c.mode, b = px.cg.mode;
          ok = pagp(a) || pagp(b) ? pagp(a) && pagp(b) && !(a === 'pagp-a' && b === 'pagp-a') : (a === 'on' && b === 'on') || (a === 'active' && b !== 'on') || (a === 'passive' && b === 'active'); } }
      (ok ? po[k].members : po[k].down).push(p); });
    Object.keys(po).forEach(function (k) { if (po[k].members.length && po[k].cfg) out.push(po[k]); });
    return out;
  };
  // 2960 без ip routing не маршрутизирует транзит (только свой трафик через ip default-gateway)
  var lk0 = P.lookup;
  P.lookup = function (id, dst) { var d = this.devs[id]; if (isSw(d) && !d.st.routing && this._pkCtx && this._pkCtx.inIf && this._pkCtx.dev === id) return null; return lk0.apply(this, arguments); };

  // ---------------------------------------------------------------- show running-config (коммутатор)
  EL.ios.renderSw = function (st, c, o) {
    var net = st.net, d = net && net.devs[st.dev], s = c.stp || {}, v = c.vtp || {};
    if (c.routing) o.push('ip routing', '!');
    o.push('spanning-tree mode ' + (s.mode || 'pvst')); if (s.pfDefault) o.push('spanning-tree portfast default');
    Object.keys(s.root || {}).forEach(function (x) { o.push('spanning-tree vlan ' + x + ' root ' + s.root[x]); });
    Object.keys(s.prio || {}).forEach(function (x) { o.push('spanning-tree vlan ' + x + ' priority ' + s.prio[x]); });
    (s.off || []).forEach(function (x) { o.push('no spanning-tree vlan ' + x); }); o.push('!');
    if (v.mode === 'transparent' || v.mode === 'off') { if (v.domain) o.push('vtp domain ' + v.domain); o.push('vtp mode ' + v.mode, '!');
      Object.keys(c.vlans || {}).forEach(function (x) { o.push('vlan ' + x); if (c.vlans[x].name) o.push(' name ' + c.vlans[x].name); o.push('!'); }); }
    var ks = Object.keys(c.ifs), ords = function (re) { return ks.filter(function (k) { return re.test(k); }).sort(function (a, b) { return +a.replace(/\D/g, '') - +b.replace(/\D/g, ''); }); };
    ords(/^po/).concat(d ? I.dports(net, d) : [], ['vlan1'], ords(/^vlan/).filter(function (k) { return k !== 'vlan1'; }), ords(/^lo/)).forEach(function (k) {
      var x = c.ifs[k] || {}; o.push('interface ' + full(k)); if (x.desc) o.push(' description ' + x.desc);
      if (x.routed) o.push(' no switchport');
      if (!/^vlan|^lo/.test(k) && !x.routed) {
        if (x.nv) o.push(' switchport trunk native vlan ' + x.nv); if (x.allow) o.push(' switchport trunk allowed vlan ' + (x.allow.length ? EL.ios.vtxt(x.allow) : 'none'));
        if (x.av && x.av !== 1) o.push(' switchport access vlan ' + x.av);
        if (x.mode) o.push(' switchport mode ' + (x.mode === 'desirable' ? 'dynamic desirable' : x.mode)); if (x.noneg) o.push(' switchport nonegotiate');
        if (x.psec) { o.push(' switchport port-security'); if (x.psecMax) o.push(' switchport port-security maximum ' + x.psecMax); if (x.psecSticky) o.push(' switchport port-security mac-address sticky');
          if (x.psecV) o.push(' switchport port-security violation ' + x.psecV); }
        if (x.cg) o.push(' channel-group ' + x.cg.id + ' mode ' + x.cg.mode);
        if (x.portfast) o.push(' spanning-tree portfast'); if (x.bpduguard) o.push(' spanning-tree bpduguard enable'); if (x.cost) o.push(' spanning-tree cost ' + x.cost); }
      if (x.ip) o.push(' ip address ' + x.ip[0] + ' ' + IP.len2mask(x.ip[1])); else if (/^vlan/.test(k) || x.routed) o.push(' no ip address');
      if (EL.ios.isShut(st, k, x)) o.push(' shutdown'); else if (x.speed) o.push(' speed ' + x.speed);
      o.push('!'); });
    if (c.gw) o.push('ip default-gateway ' + c.gw);
    (c.routes || []).forEach(function (r) { var p = r.net.split('/'); o.push('ip route ' + p[0] + ' ' + IP.len2mask(+p[1]) + ' ' + r.nh); });
    o.push('ip classless', '!', 'ip flow-export version 9', '!');
  };
  EL.ios.vtxt = function (a) { a = uniq(a); var r = [], i = 0; while (i < a.length) { var j = i; while (j + 1 < a.length && a[j + 1] === a[j] + 1) j++; r.push(j > i ? a[i] + '-' + a[j] : '' + a[i]); i = j + 1; } return r.join(','); };

  // ---------------------------------------------------------------- show (коммутатор)
  function vname(st, v) { return st.vlans[v] && st.vlans[v] !== '-' ? st.vlans[v] : v === 1 ? 'default' : 'VLAN' + ('000' + v).slice(-4); }
  function accessPorts(st, v) { var net = st.net; return I.dports(net, net.devs[st.dev]).filter(function (p) { var P0 = st.ports[p]; return !P0.cg && !P0.routedVlan && P0.mode === 'access' && P0.access === v; }); }
  function vlanTable(st, brief) {
    var vs = Object.keys(st.vlans).map(Number).filter(function (v) { return v < 4000; }).sort(function (a, b) { return a - b; }), o = ['', 'VLAN Name                             Status    Ports', '---- -------------------------------- --------- -------------------------------'];
    vs.forEach(function (v) { var ps = accessPorts(st, v).map(short), first = pad(v, 5) + pad(vname(st, v), 33) + pad('active', 10);
      if (!ps.length) { o.push(first.replace(/\s+$/, '')); return; }
      for (var i = 0; i < ps.length; i += 4) o.push((i ? new Array(49).join(' ') : first) + ps.slice(i, i + 4).join(', ') + (i + 4 < ps.length ? ',' : '')); });
    [[1002, 'fddi-default'], [1003, 'token-ring-default'], [1004, 'fddinet-default'], [1005, 'trnet-default']].forEach(function (x) { o.push(pad(x[0], 5) + pad(x[1], 33) + 'act/unsup'); });
    if (!brief) { o.push('', 'VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2', '---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------');
      vs.forEach(function (v) { o.push(pad(v, 5) + pad('enet', 6) + pad(100000 + v, 11) + pad(1500, 6) + pad('-', 7) + pad('-', 7) + pad('-', 9) + pad('-', 5) + pad('-', 9) + pad(0, 7) + '0'); }); }
    return o.join('\n');
  }
  sc('exec', 'show vlan brief', function (st) { dtpSync(st.net); return vlanTable(st, true); }, 'VTP VLAN status').cfg = false;
  sc('exec', 'show vlan', function (st) { dtpSync(st.net); return vlanTable(st, false); }).cfg = false;
  function trunks(st) { var net = st.net; return net.lports(st.dev).filter(function (L) { return L.cfg && L.cfg.mode === 'trunk' && L.members.length && I.phyUp(st, L.members[0]); }); }
  sc('exec', 'show interfaces trunk', function (st) {
    var net = st.net; if (!net) return ''; dtpSync(net); var T = trunks(st); if (!T.length) return '';
    var o = ['Port        Mode         Encapsulation  Status        Native vlan'];
    T.forEach(function (L) { o.push(pad(short(L.name), 12) + pad({ trunk: 'on', desirable: 'desirable', auto: 'auto' }[L.cfg.admin] || 'on', 13) + pad('802.1q', 15) + pad('trunking', 14) + L.cfg.native); });
    o.push('', 'Port        Vlans allowed on trunk'); T.forEach(function (L) { o.push(pad(short(L.name), 12) + (L.cfg.allAll ? '1-4094' : EL.ios.vtxt(L.cfg.allowed) || 'none')); });
    var act = function (L) { return (L.cfg.allAll ? Object.keys(st.vlans).map(Number) : L.cfg.allowed.filter(function (v) { return st.vlans[v]; })).filter(function (v) { return v < 4000; }); };
    o.push('', 'Port        Vlans allowed and active in management domain'); T.forEach(function (L) { o.push(pad(short(L.name), 12) + (EL.ios.vtxt(act(L)) || 'none')); });
    o.push('', 'Port        Vlans in spanning tree forwarding state and not pruned');
    T.forEach(function (L) { o.push(pad(short(L.name), 12) + (EL.ios.vtxt(act(L).filter(function (v) { return net.stpFwd(st.dev, L.name, v); })) || 'none')); });
    return o.join('\n');
  }, 'Show interface trunk information').cfg = false;
  sc('exec', 'show interfaces status', function (st) {
    var net = st.net; if (!net) return ''; dtpSync(net); var o = ['Port      Name               Status       Vlan       Duplex  Speed Type'];
    I.dports(net, net.devs[st.dev]).forEach(function (p) { var P0 = st.ports[p], up = I.phyUp(st, p), stt = P0.shut ? 'disabled' : up ? 'connected' : 'notconnect';
      o.push(pad(short(p), 10) + pad((P0.desc || '').slice(0, 18), 19) + pad(stt, 13) + pad(P0.routedVlan ? 'routed' : P0.mode === 'trunk' ? 'trunk' : P0.access, 11) + pad(up ? 'a-full' : 'auto', 8) + pad(up ? (/^fa/.test(p) ? 'a-100' : 'a-1000') : 'auto', 6) + (/^fa/.test(p) ? '10/100BaseTX' : '10/100/1000BaseTX')); });
    return o.join('\n');
  }).cfg = false;
  sc('exec', 'show interfaces <if> switchport', function (st, a) {
    var net = st.net, P0 = st.ports[a[0]] || st.pos[a[0]]; if (!net || !P0) return null; dtpSync(net);
    return ['Name: ' + short(a[0]), 'Switchport: ' + (P0.routedVlan ? 'Disabled' : 'Enabled'), 'Administrative Mode: ' + { trunk: 'trunk', access: 'static access', auto: 'dynamic auto', desirable: 'dynamic desirable' }[P0.admin || 'auto'],
      'Operational Mode: ' + (!I.phyUp(st, a[0]) && st.ports[a[0]] ? 'down' : P0.mode === 'trunk' ? 'trunk' : 'static access'), 'Administrative Trunking Encapsulation: dot1q',
      'Negotiation of Trunking: ' + (P0.noneg || P0.admin === 'access' ? 'Off' : 'On'), 'Access Mode VLAN: ' + P0.access + ' (' + vname(st, P0.access) + ')',
      'Trunking Native Mode VLAN: ' + P0.native + ' (' + vname(st, P0.native) + ')', 'Voice VLAN: none', 'Trunking VLANs Enabled: ' + (P0.allAll ? 'ALL' : EL.ios.vtxt(P0.allowed) || 'NONE'),
      'Pruning VLANs Enabled: 2-1001', '', 'Protected: false', 'Unknown unicast blocked: disabled', 'Unknown multicast blocked: disabled', 'Appliance trust: none'].join('\n');
  }).cfg = false;
  var ROLE = { Root: 'Root', Desg: 'Desg', Altn: 'Altn', Back: 'Back' }, STS = { Frw: 'FWD', Dsc: 'BLK', Blk: 'BLK', Lsn: 'LIS', Lrn: 'LRN' };
  function mac(st) { var m = String(st.bmac || '').replace(/:/g, ''); return m.slice(0, 4) + '.' + m.slice(4, 8) + '.' + m.slice(8, 12); }
  function macOf(d) { return mac(d.st); }
  function stpVlan(st, v) {
    var net = st.net, k = net.stpInst(st.dev, v), t = net.stp(k)[st.dev] || {}, res = k ? net._stpK[k] : net._stp, R = res.root[st.dev], rd = net.devs[R];
    var bp = function (d) { var s2 = d.st; return k && s2.mst && s2.mst.inst[k] && s2.mst.inst[k].prio !== undefined ? s2.mst.inst[k].prio : (s2.stp || {}).prio || 32768; };
    var me = bp(net.devs[st.dev]), rp = Object.keys(t).filter(function (n) { return t[n].role === 'Root'; })[0];
    var o = ['VLAN' + ('000' + v).slice(-4), '  Spanning tree enabled protocol ' + (st.stp.mode === 'rst' ? 'rstp' : 'ieee'),
      '  Root ID    Priority    ' + (bp(rd) + (I.isIos(rd) ? v : 0)), '             Address     ' + macOf(rd)];
    if (R === st.dev) o.push('             This bridge is the root'); else o.push('             Cost        ' + res.dist[st.dev], '             Port        ' + (rp ? (I.dports(net, net.devs[st.dev]).indexOf(rp) + 1) + ' (' + full(rp) + ')' : '-'));
    o.push('             Hello Time  2 sec  Max Age 20 sec  Forward Delay 15 sec', '', '  Bridge ID  Priority    ' + (me + v) + '  (priority ' + me + ' sys-id-ext ' + v + ')',
      '             Address     ' + mac(st), '             Hello Time  2 sec  Max Age 20 sec  Forward Delay 15 sec', '             Aging Time  300', '',
      'Interface        Role Sts Cost      Prio.Nbr Type', '---------------- ---- --- --------- -------- --------------------------------');
    net.lports(st.dev).forEach(function (L) { var r = t[L.name]; if (!r) return;
      var inV = L.cfg.mode === 'trunk' ? (L.cfg.allAll || L.cfg.allowed.indexOf(v) >= 0) : L.cfg.access === v; if (!inV || L.cfg.routedVlan) return;
      var c = (k && L.cfg.mstCost && L.cfg.mstCost[k]) || L.cfg.stpCost; o.push(pad(short(L.name), 17) + pad(ROLE[r.role] || 'Desg', 5) + pad(STS[net.stpSts(st.dev, L.name, k)] || 'FWD', 4) + pad(c, 10) + pad('128.' + (I.dports(net, net.devs[st.dev]).indexOf(L.members[0]) + 1), 9) + 'P2p'); });
    return o.join('\n');
  }
  sc('exec', 'show spanning-tree', function (st) { var net = st.net; if (!net) return ''; dtpSync(net);
    var used = Object.keys(st.vlans).map(Number).filter(function (v) { return v < 4000 && (accessPorts(st, v).length || trunks(st).length) && (((C(st).stp || {}).off) || []).indexOf(v) < 0; });
    return used.map(function (v) { return stpVlan(st, v); }).join('\n\n'); }, 'Spanning tree topology').cfg = false;
  sc('exec', 'show spanning-tree vlan <n>', function (st, a) { if (!st.vlans[a[0]]) return 'Spanning tree instance(s) for vlan ' + a[0] + ' does not exist.'; dtpSync(st.net); return stpVlan(st, a[0]); }).cfg = false;
  sc('exec', 'show etherchannel summary', function (st) { var net = st.net; if (!net) return ''; var c = C(st), gs = Object.keys(c.ifs).filter(function (k) { return /^po\d+$/.test(k); });
    var o = ['Flags:  D - down        P - in port-channel', '        I - stand-alone s - suspended', '        H - Hot-standby (LACP only)', '        R - Layer3      S - Layer2',
      '        U - in use      f - failed to allocate aggregator', '        u - unsuitable for bundling', '        w - waiting to be aggregated', '        d - default port', '',
      'Number of channel-groups in use: ' + gs.length, 'Number of aggregators:           ' + gs.length, '', 'Group  Port-channel  Protocol    Ports', '------+-------------+-----------+----------------------------------------------'];
    var L = net.lports(st.dev);
    gs.forEach(function (k) { var mem = I.dports(net, net.devs[st.dev]).filter(function (p) { var g = (c.ifs[p] || {}).cg; return g && 'po' + g.id === k; }), lp = L.filter(function (x) { return x.name === k; })[0], up = lp ? lp.members : [];
      var proto = mem.length ? { on: '-', active: 'LACP', passive: 'LACP', auto: 'PAgP', desirable: 'PAgP' }[c.ifs[mem[0]].cg.mode] : '-';
      o.push(pad(k.slice(2), 7) + pad('Po' + k.slice(2) + '(' + (up.length ? 'SU' : 'SD') + ')', 14) + pad(proto, 12) + mem.map(function (p) { return short(p) + '(' + (up.indexOf(p) >= 0 ? 'P' : 'D') + ')'; }).join(' ')); });
    return o.join('\n'); }, 'EtherChannel information').cfg = false;
  sc('exec', 'show mac address-table', function (st) { var net = st.net; if (!net) return ''; var T0 = net.mac[st.dev] || {}, ks = Object.keys(T0);
    var o = ['          Mac Address Table', '-------------------------------------------', '', 'Vlan    Mac Address       Type        Ports', '----    -----------       --------    -----'];
    ks.forEach(function (k) { var e = T0[k], m = String(e.mac).replace(/:/g, ''); if (+e.vlan >= 4000) return; o.push(pad('  ' + e.vlan, 8) + pad(m.slice(0, 4) + '.' + m.slice(4, 8) + '.' + m.slice(8, 12), 18) + pad(e.st ? 'STATIC' : 'DYNAMIC', 12) + short(e.port)); });
    return o.join('\n'); }, 'MAC forwarding table').cfg = false;
  sc('exec', 'show vtp status', function (st) { dtpSync(st.net); var v = C(st).vtp || {}, x = st.ios;
    return ['VTP Version                     : ' + (v.ver || 1), 'Configuration Revision          : ' + (vtpMode(st) === 'transparent' ? 0 : x.vtpRev !== undefined && x.vtpVlans ? x.vtpRev : v.rev || 0),
      'Maximum VLANs supported locally : 255', 'Number of existing VLANs        : ' + (Object.keys(st.vlans).filter(function (q) { return +q < 4000; }).length + 4),
      'VTP Operating Mode              : ' + { server: 'Server', client: 'Client', transparent: 'Transparent', off: 'Off' }[vtpMode(st)],
      'VTP Domain Name                 : ' + (v.domain || x.vtpDomain || ''), 'VTP Pruning Mode                : Disabled', 'VTP V2 Mode                     : Disabled', 'VTP Traps Generation            : Disabled'].join('\n'); }).cfg = false;
})(typeof window !== 'undefined' ? window : global);
