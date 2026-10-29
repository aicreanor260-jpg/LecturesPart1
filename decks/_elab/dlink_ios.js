/* D-Link «Cisco-подобный» CLI (DGS-1510-28X, DGS-3130-30TS) — спецификация sources/dlink/spec/dlink-ios.md (CLI Reference R1510 1.81, R3130 1.00).
   Диалект движка Cisco (cisco.js / cisco_sw.js): приглашения Switch# / Switch(config-if)#, порты ethernet 1/0/N (в выводах eth1/0/N),
   ошибки без «%»: «Invalid input detected at ^marker», «Ambiguous command», «Incomplete command» (§4).
   Отличия от Cisco по документации (§6): режим порта по умолчанию — hybrid (switchport mode access | hybrid | trunk; DTP нет),
   switchport hybrid allowed vlan add tagged|untagged, switchport hybrid native vlan; VTP и CDP нет; STP выключен глобально
   (spanning-tree global state enable), режим по умолчанию RSTP, стоимость 20000 на 1G; ip routing включён (DGS-1510);
   имя — snmp-server name; сохранение — copy running-config startup-config с вопросом [y/n] и «Saving all configurations to NV-RAM.......... Done.»
   Упрощения (в отчёте): вход без учётной записи (у DGS-1510 заводская admin/admin), show running-config — в виде движка Cisco. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, I = EL.ios, P = EL.Net.prototype, pad = I.pad;
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  [['DGS-1510-28X', 28, 'Gigabit Ethernet SmartPro Switch', 'Коммутатор D-Link DGS-1510-28X (Cisco-подобный CLI): eth1/0/1–1/0/28, IP 10.90.90.90/8 на VLAN 1'],
   ['DGS-3130-30TS', 30, 'Gigabit Ethernet Switch', 'Коммутатор D-Link DGS-3130-30TS (Cisco-подобный CLI): eth1/0/1–1/0/30, IP 10.90.90.90/8 на VLAN 1']
  ].forEach(function (x) { EL.MODELS[x[0]] = { type: 'mes', kind: 'cs-sw', dlink: true, vendor: 'cisco', portList: range('eth1/0/', 1, x[1]), ports: x[1], group: 'D-Link', host: 'Switch', costs: 'long', ios: '1.81',
    banner: x[2], note: x[3], login: [{ u: 'admin', p: 'admin', a: 'DGS-1510 (у DGS-3130 учётных записей нет)' }] }; });
  function DL(st) { return !!st.ios && !!st.ios.dl; }
  function C(st) { return st.ios.c; }
  function dc(views, pat, run, d) { var e = I.cmd(views, pat, run, d); e.ok = DL; return e; }
  // команды Catalyst, которых у D-Link нет или которые выглядят иначе — скрыть для D-Link
  var HIDE = /^(vtp |switchport mode dynamic|switchport nonegotiate|show vtp|show cdp|cdp |show vlan|show spanning-tree$|spanning-tree mode|spanning-tree vlan|copy running-config|write|hostname)/;
  I.T.forEach(function (e) { if (HIDE.test(e.p.join(' '))) { var o = e.ok; e.ok = function (st) { return !DL(st) && (!o || o(st)); }; } });
  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}; if (!m.dlink) return d;
    d.st.ios.dl = true; d.st.ios.stack = [{ v: 'priv' }]; d.st.bmac = '3c:1e:04:' + d.st.bmac.slice(9);   /* уровень 12/15 — сразу Privileged EXEC (§2.4) */ C(d.st).ifs.vlan1 = { ip: ['10.90.90.90', 8], noShut: true }; I.compile(d.st); return d; };

  var rb0 = P.reboot;
  P.reboot = function (id) { var r = rb0.apply(this, arguments), d = this.devs[id]; if (d && d.st.ios && d.st.ios.dl) d.st.ios.stack = [{ v: 'priv' }]; return r; };
  function each(st, f) { var bad = false; I.cur(st).forEach(function (x) { if (f(x) === false) bad = true; }); return bad ? null : undefined; }
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }).sort(function (x, y) { return x - y; }); }
  dc('if range', 'switchport mode hybrid', function (st) { return each(st, function (x) { delete x.mode; delete x.htag; delete x.hun; delete x.hpvid; }); }, 'Set the switchport mode');
  dc('if range', 'switchport hybrid allowed vlan add tagged <list>', function (st, a) { return each(st, function (x) { if (x.mode) return false; x.htag = uniq((x.htag || []).concat(a[0])); x.hun = (x.hun || [1]).filter(function (v) { return a[0].indexOf(v) < 0; }); }); });
  dc('if range', 'switchport hybrid allowed vlan add untagged <list>', function (st, a) { return each(st, function (x) { if (x.mode) return false; x.hun = uniq((x.hun || [1]).concat(a[0])); x.htag = (x.htag || []).filter(function (v) { return a[0].indexOf(v) < 0; }); }); });
  dc('if range', 'switchport hybrid allowed vlan remove <list>', function (st, a) { return each(st, function (x) { x.htag = (x.htag || []).filter(function (v) { return a[0].indexOf(v) < 0; }); x.hun = (x.hun || [1]).filter(function (v) { return a[0].indexOf(v) < 0; }); }); });
  dc('if range', 'switchport hybrid native vlan <n>', function (st, a) { return each(st, function (x) { if (x.mode) return false; x.hpvid = a[0]; }); });
  dc('config', 'spanning-tree global state <w>', function (st, a) { var w = a[0].toLowerCase(); if (w !== 'enable' && w !== 'disable') return null; C(st).dlStp = w === 'enable'; }, 'Spanning tree');
  dc('config', 'spanning-tree mode <w>', function (st, a) { var w = a[0].toLowerCase(); if (['rstp', 'mstp', 'stp'].indexOf(w) < 0) return null; C(st).dlMode = w; });
  dc('config', 'spanning-tree priority <n>', function (st, a) { if (a[0] > 61440 || a[0] % 4096) return null; C(st).dlPrio = a[0]; });
  dc('config', 'snmp-server name <w>', function (st, a) { C(st).hostname = a[0]; }, 'Set the system name');
  dc('config', 'prompt <w>', function (st, a) { C(st).hostname = a[0]; });
  dc('config', 'no prompt', function (st) { delete C(st).hostname; });
  dc('priv', 'copy running-config startup-config', function (st) { st.ios.ask = { pr: '', fn: function (s) { if (!/^y/i.test(s)) return ''; st.ios.saved = EL.clone(C(st)); return 'Saving all configurations to NV-RAM.......... Done.'; } };
    return 'Destination filename startup-config? [y/n]: '; }, 'Copy from one file to another').cfg = false;

  // compile: после компиляции Catalyst — порты hybrid по умолчанию, STP D-Link, ip routing включён
  var cs0 = EL.ios.compileSw;
  EL.ios.compileSw = function (st) { cs0.apply(this, arguments); if (!DL(st)) return;
    var c = C(st), net = st.net, d = net && net.devs[st.dev], ports = d ? I.dports(net, d) : [];
    ports.forEach(function (p) { var x = c.ifs[p] || {}, P0 = st.ports[p]; if (!P0 || x.routed) return;
      if (!x.mode) { delete P0.admin; P0.mode = 'general'; P0.pvid = x.hpvid || 1; P0.gtag = (x.htag || []).slice(); P0.guntag = (x.hun || [1]).slice(); } });
    Object.keys(st.pos || {}).forEach(function (k) { var x = c.ifs[k] || {}, P0 = st.pos[k]; if (!x.mode) { delete P0.admin; P0.mode = 'general'; P0.pvid = x.hpvid || 1; P0.gtag = (x.htag || []).slice(); P0.guntag = (x.hun || [1]).slice(); } });
    st.stp = { on: !!c.dlStp, mode: { rstp: 'rst', mstp: 'mst', stp: 'stp' }[c.dlMode || 'rstp'], prio: c.dlPrio || 32768, pvst: false };
    st.mst = { name: 'dlink-' + st.dev, rev: 0, inst: {} }; st.routing = true; st.gw = null;
  };
  // show vlan (R1510 с.751) и show spanning-tree (с.669)
  function rng(L) { L = L.map(function (p) { return +String(p).split('/').pop(); }).sort(function (a, b) { return a - b; }); var r = [], i = 0;
    while (i < L.length) { var j = i; while (j + 1 < L.length && L[j + 1] === L[j] + 1) j++; r.push(j > i ? 'eth1/0/' + L[i] + '-1/0/' + L[j] : 'eth1/0/' + L[i]); i = j + 1; } return r.join(','); }
  dc('exec', 'show vlan', function (st) { var net = st.net, ps = I.dports(net, net.devs[st.dev]), o = [];
    Object.keys(st.vlans).map(Number).filter(function (v) { return v < 4000; }).sort(function (a, b) { return a - b; }).forEach(function (v) {
      var tg = ps.filter(function (p) { var P0 = st.ports[p]; return P0.mode === 'trunk' ? (P0.allAll || P0.allowed.indexOf(v) >= 0) && P0.native !== v : P0.mode === 'general' && P0.gtag.indexOf(v) >= 0; });
      var un = ps.filter(function (p) { var P0 = st.ports[p]; return P0.mode === 'access' ? P0.access === v : P0.mode === 'trunk' ? P0.native === v : P0.guntag.indexOf(v) >= 0; });
      o.push('  VLAN ' + v, '     Name : ' + (st.vlans[v] !== '-' ? st.vlans[v] : v === 1 ? 'default' : 'VLAN' + ('000' + v).slice(-4)), '     Description :', '     Tagged Member Ports : ' + rng(tg), '     Untagged Member Ports : ' + rng(un)); });
    o.push('  Total Entries : ' + Object.keys(st.vlans).filter(function (v) { return +v < 4000; }).length); return o.join('\n'); }, 'Show VLAN').cfg = false;
  var RL = { Root: 'root', Desg: 'designated', Altn: 'alternate', Back: 'backup' }, SS = { Frw: 'forwarding', Dsc: 'discarding', Lrn: 'learning', Blk: 'blocking', Lsn: 'listening' };
  dc('exec', 'show spanning-tree', function (st) { var net = st.net; if (!net) return ''; if (!st.stp.on) return 'Spanning Tree: Disabled';
    var t = net.stp(0)[st.dev] || {}, R = net._stp.root[st.dev], rs = net.devs[R].st, mac = function (s) { return String(s.bmac).toUpperCase().replace(/:/g, '-'); };
    var o = ['Spanning Tree: Enabled', 'Protocol Mode: ' + st.stp.mode.replace('rst', 'RSTP').replace('mst', 'MSTP').replace(/^stp$/, 'STP'), 'Tx-hold-count: 6', 'Root ID Priority: ' + ((rs.stp || {}).prio || 32768),
      'Address: ' + mac(rs), 'Hello Time: 2 sec, Max Age: 20 sec, Forward Delay: 15 sec', 'Bridge ID Priority: ' + st.stp.prio + ' (priority ' + st.stp.prio + ' sys-id-ext 0)', 'Address: ' + mac(st),
      'Hello Time: 2 sec, Max Age: 20 sec, Forward Delay: 15 sec,', 'Topology Changes Count: 0', 'Interface Role State Cost Priority Link', '                          .Port#   Type Edge', '--------- ---- ----- ---- ------- ----- ----'];
    net.lports(st.dev).forEach(function (L) { var r = t[L.name]; if (!r) return; o.push(L.name + ' ' + (RL[r.role] || 'designated') + ' ' + (SS[net.stpSts(st.dev, L.name, 0)] || 'forwarding') + ' ' + (L.cfg.stpCost || 20000) + ' 128.' + String(L.name).split('/').pop() + ' p2p ' + (L.cfg.portfast ? 'edge' : 'non-edge')); });
    return o.join('\n'); }, 'Show spanning tree').cfg = false;
  dc('exec', 'show interfaces status', function (st) { var net = st.net, o = ['Port          Status        VLAN         Duplex  Speed          Type', '------------- ------------- ------------ ------- -------------- -------------'], ps = I.dports(net, net.devs[st.dev]);
    ps.forEach(function (p) { var P0 = st.ports[p], up = I.phyUp(st, p); o.push(pad(p, 14) + pad(P0.shut ? 'disabled' : up ? 'connected' : 'not-connected', 14) + pad(P0.mode === 'trunk' ? 'trunk' : P0.mode === 'access' ? P0.access : P0.pvid, 13) + pad(up ? 'a-full' : 'auto', 8) + pad(up ? 'a-1000' : 'auto', 15) + '1000BASE-T'); });
    o.push('Total Entries: ' + ps.length); return o.join('\n'); }).cfg = false;
  // у Catalyst-версии show interfaces status — свой вид; для D-Link — этот
  I.T.forEach(function (e) { if (e.p.join(' ') === 'show interfaces status' && e.ok !== DL) { var o = e.ok; e.ok = function (st) { return !DL(st) && (!o || o(st)); }; } });
})(typeof window !== 'undefined' ? window : global);
