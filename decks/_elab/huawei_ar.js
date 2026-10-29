/* Маршрутизаторы Huawei AR (AR2220, AR1220) — спецификация sources/huawei/spec/ar-router.md (HCIA-LG гл. 2, 4, 5; AR-CR V200R010).
   Настройки VRP (st.vrp.c) → st.run модели ESR: ifs (ip, shut, ospf, vrrp, acl, helper), routes, rip, ospf, acls, snat/dnat, dhcp, relay.
   Межсетевого экрана нет (fw выключен на всех интерфейсах). По документации: статика — preference 60, OSPF — 10, RIP — 100
   (в модели порядок сохранён через EL.vrp.adOf); OSPF — hello 10 / dead 40, broadcast на Ethernet, DR priority 1, MTU в DD не проверяется;
   RIP — шлёт v1 (version 2 — v2), network — только классовая сеть; VRRP — v2, приоритет 100, вытеснение включено.
   LAN-порты AR1220 (Ethernet0/0/0–7) — L2, адрес на них — после undo portswitch.
   Упрощения (в отчёте): traffic-filter пропускает пакеты, не попавшие ни в одно правило (в снятых страницах документации не указано);
   nat outbound с address-group транслирует в адрес интерфейса; nat server без смены порта; RIP-суммирование не моделируется. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, Vr = EL.vrp, pad = Vr.pad, full = Vr.full;
  function AR(st) { return st.vrp.kind === 'ar'; }
  function ac(views, pat, run, d) { var e = Vr.cmd(views, pat, run, d); e.ok = AR; return e; }
  function C(st) { return st.vrp.c; }
  function top(st) { return Vr.top(st); }
  function x0(st) { return Vr.cur(st)[0]; }
  function nm(st) { return top(st).name; }
  function isL3(st, n) { var x = C(st).ifs[n.split('.')[0]] || {}; return !/^Eth\d/.test(n) || !!x.l3; }
  function wcRange(ip, w) { var a = IP.ip2n(ip), m = IP.ip2n(w); if (a === null || m === null) return null; var lo = (a & ~m) >>> 0; return [IP.n2ip(lo), IP.n2ip((lo | m) >>> 0)]; }
  function area(w) { return /^\d+$/.test(w) ? IP.n2ip(+w >>> 0) : IP.ip2n(w) !== null ? w : null; }

  // ---------------------------------------------------------------- интерфейсы
  ac('if', 'ip address <ip> <mask>', function (st, a) { var n = nm(st); if (/^(Eth-Trunk|Vlanif)/.test(n) || !isL3(st, n) || a[1] < 1 || a[1] > 32) return null; x0(st).ip = [a[0], a[1]]; }, 'Configure the IP address of an interface');
  ac('if', 'undo ip address', function (st) { delete x0(st).ip; });
  ac('if', 'undo portswitch', function (st) { if (!/^Eth\d+\/\d+\/\d+$/.test(nm(st))) return null; x0(st).l3 = true; });
  ac('if', 'portswitch', function (st) { if (!/^Eth\d+\/\d+\/\d+$/.test(nm(st))) return null; delete x0(st).l3; delete x0(st).ip; });
  ac('if', 'dot1q termination vid <n>', function (st, a) { if (nm(st).indexOf('.') < 0 || a[0] < 1 || a[0] > 4094) return null; x0(st).vid = a[0]; });
  ac('if', 'undo dot1q termination vid <n>', function (st) { delete x0(st).vid; });
  ac('if', 'arp broadcast enable', function (st) { if (nm(st).indexOf('.') < 0) return null; x0(st).arpb = true; });
  ac('if', 'mtu <n>', function (st, a) { if (a[0] < 46 || a[0] > 1500) return null; x0(st).mtu = a[0]; });
  ac('if', 'undo mtu', function (st) { delete x0(st).mtu; });

  // ---------------------------------------------------------------- RIP
  function rip(st) { return C(st).rip; }
  function ripEnter(st, n) { var c = C(st); if (!c.rip || c.rip.id !== n) c.rip = { id: n, nets: [], silent: [] }; Vr.push(st, { v: 'rip', key: 'rip', tag: 'rip-' + n }); }
  ac('sys', 'rip', function (st) { ripEnter(st, 1); }, 'Specify the RIP process');
  ac('sys', 'rip <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return null; ripEnter(st, a[0]); });
  ac('sys', 'undo rip <n>', function (st) { delete C(st).rip; });
  ac('rip', 'version <n>', function (st, a) { if (a[0] !== 1 && a[0] !== 2) return null; rip(st).ver = a[0]; }, 'Specify the RIP version');
  ac('rip', 'undo version', function (st) { delete rip(st).ver; });
  ac('rip', 'network <ip>', function (st, a) { var n = IP.ip2n(a[0]), cl = n >>> 31 === 0 ? 8 : n >>> 30 === 2 ? 16 : 24;   // только классовая сеть
    if (IP.netOf(a[0], cl) !== a[0] + '/' + cl) return null; var R = rip(st); if (R.nets.indexOf(a[0]) < 0) R.nets.push(a[0]); }, 'Enable RIP on the specified network segment');
  ac('rip', 'undo network <ip>', function (st, a) { var R = rip(st); R.nets = R.nets.filter(function (x) { return x !== a[0]; }); });
  ac('rip', 'summary', function (st) { delete rip(st).noSum; });
  ac('rip', 'undo summary', function (st) { rip(st).noSum = true; });
  ac('rip', 'silent-interface <if>', function (st, a) { var R = rip(st); if (R.silent.indexOf(a[0]) < 0) R.silent.push(a[0]); });
  ac('rip', 'undo silent-interface <if>', function (st, a) { var R = rip(st); R.silent = R.silent.filter(function (x) { return x !== a[0]; }); });
  ac('rip', 'import-route <w>', function (st, a) { var w = a[0].toLowerCase(); if (['direct', 'static'].indexOf(w) < 0) return null; var R = rip(st); R.imp = R.imp || []; if (R.imp.indexOf(w) < 0) R.imp.push(w); });
  ac('rip', 'default-route originate', function (st) { rip(st).defOrig = true; });
  ac('if', 'rip version <n>', function (st, a) { if (a[0] !== 1 && a[0] !== 2) return null; x0(st).ripVer = a[0]; });
  ac('if', 'undo rip version', function (st) { delete x0(st).ripVer; });

  // ---------------------------------------------------------------- OSPF
  function ospfEnter(st, n, rid) { var c = C(st); if (!c.ospf || c.ospf.id !== n) c.ospf = { id: n, areas: {}, silent: [] }; if (rid) c.ospf.rid = rid;
    Vr.push(st, { v: 'ospf', key: 'ospf', tag: 'ospf-' + n }); }
  ac('sys', 'ospf', function (st) { ospfEnter(st, 1); }, 'Specify the OSPF process');
  ac('sys', 'ospf <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return null; ospfEnter(st, a[0]); });
  ac('sys', 'ospf <n> router-id <ip>', function (st, a) { ospfEnter(st, a[0], a[1]); });
  ac('sys', 'ospf router-id <ip>', function (st, a) { ospfEnter(st, 1, a[0]); });
  ac('sys', 'undo ospf <n>', function (st, a) { if (C(st).ospf && C(st).ospf.id === a[0]) delete C(st).ospf; });
  ac('ospf', 'area <w>', function (st, a) { var id = area(a[0]); if (!id) return null; var O = C(st).ospf; O.areas[id] = O.areas[id] || { nets: [] };
    Vr.push(st, { v: 'area', key: 'ospf', id: id, tag: 'ospf-' + O.id + '-area-' + id }); }, 'Specify an OSPF area');
  ac('ospf', 'undo area <w>', function (st, a) { var id = area(a[0]); if (id) delete C(st).ospf.areas[id]; });
  function ar0(st) { return C(st).ospf.areas[top(st).id]; }
  ac('area', 'network <ip> <ip>', function (st, a) { var r = wcRange(a[0], a[1]); if (!r) return null; var A = ar0(st);
    if (!A.nets.some(function (x) { return x[0] === r[0] && x[1] === a[1]; })) A.nets.push([r[0], a[1]]); }, 'Enable OSPF on the interface');   // адрес приводится к сети (HCIA-LG с. 41)
  ac('area', 'undo network <ip> <ip>', function (st, a) { var r = wcRange(a[0], a[1]); var A = ar0(st); A.nets = A.nets.filter(function (x) { return !(r && x[0] === r[0] && x[1] === a[1]); }); });
  ac('area', 'authentication-mode md5 <n> cipher <w>', function (st, a) { ar0(st).auth = a[0] + ' ' + a[1]; });
  ac('ospf', 'silent-interface <if>', function (st, a) { var O = C(st).ospf; if (O.silent.indexOf(a[0]) < 0) O.silent.push(a[0]); });
  ac('ospf', 'undo silent-interface <if>', function (st, a) { var O = C(st).ospf; O.silent = O.silent.filter(function (x) { return x !== a[0]; }); });
  ac('ospf', 'default-route-advertise', function (st) { C(st).ospf.dra = 'yes'; });
  ac('ospf', 'default-route-advertise always', function (st) { C(st).ospf.dra = 'always'; });
  ac('ospf', 'undo default-route-advertise', function (st) { delete C(st).ospf.dra; });
  ac('ospf', 'import-route <w>', function (st, a) { var w = a[0].toLowerCase(); if (['direct', 'static', 'rip'].indexOf(w) < 0) return null; var O = C(st).ospf; O.imp = O.imp || []; if (O.imp.indexOf(w) < 0) O.imp.push(w); });
  ac('if', 'ospf timer hello <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return null; x0(st).hello = a[0]; });
  ac('if', 'ospf timer dead <n>', function (st, a) { if (a[0] < 1 || a[0] > 235926000) return null; x0(st).dead = a[0]; });
  ac('if', 'undo ospf timer hello', function (st) { delete x0(st).hello; });
  ac('if', 'undo ospf timer dead', function (st) { delete x0(st).dead; });
  ac('if', 'ospf network-type <w>', function (st, a) { var w = a[0].toLowerCase(); if (['p2p', 'broadcast'].indexOf(w) < 0) return null; x0(st).ntype = w; });
  ac('if', 'undo ospf network-type', function (st) { delete x0(st).ntype; });
  ac('if', 'ospf cost <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return null; x0(st).ocost = a[0]; });
  ac('if', 'undo ospf cost', function (st) { delete x0(st).ocost; });
  ac('if', 'ospf dr-priority <n>', function (st, a) { if (a[0] > 255) return null; x0(st).oprio = a[0]; });
  ac('if', 'undo ospf dr-priority', function (st) { delete x0(st).oprio; });
  ac('if', 'ospf mtu-enable', function (st) { x0(st).mtuEn = true; });
  ac('if', 'undo ospf mtu-enable', function (st) { delete x0(st).mtuEn; });
  ac('if', 'ospf authentication-mode md5 <n> cipher <w>', function (st, a) { x0(st).oauth = a[0] + ' ' + a[1]; });

  // ---------------------------------------------------------------- ACL
  function acls(st) { var c = C(st); return c.acls || (c.acls = {}); }
  function aclEnter(st, n) { if (n < 2000 || n > 3999) return null; var A = acls(st); A[n] = A[n] || { rules: {} };
    Vr.push(st, { v: 'acl', key: 'acl', n: n, tag: 'acl-' + (n < 3000 ? 'basic-' : 'adv-') + n }); }
  ac('sys', 'acl <n>', function (st, a) { return aclEnter(st, a[0]); }, 'Specify ACL configuration information');
  ac('sys', 'acl number <n>', function (st, a) { return aclEnter(st, a[0]); });
  ac('sys', 'undo acl <n>', function (st, a) { delete acls(st)[a[0]]; });
  ac('sys', 'undo acl number <n>', function (st, a) { delete acls(st)[a[0]]; });
  var PORTN = { telnet: 23, www: 80, ftp: 21, ssh: 22, smtp: 25, domain: 53, bootps: 67, tftp: 69, snmp: 161 };
  function portNum(w) { return /^\d+$/.test(w) ? +w : PORTN[String(w).toLowerCase()] || null; }
  // rule [id] permit|deny [proto] [source A W|any] [destination A W|any] [destination-port eq N]
  function parseRule(adv, t) {
    var r = {}, i = 0; if (!/^(permit|deny)$/.test(t[0])) return null; r.act = t[0]; i = 1;
    if (adv) { var pr = t[1]; if (!pr || !/^(ip|tcp|udp|icmp|\d+)$/.test(pr)) return null; r.proto = pr === 'ip' ? 'any' : pr === '6' ? 'tcp' : pr === '17' ? 'udp' : pr === '1' ? 'icmp' : pr; i = 2; }
    while (i < t.length) { var k = t[i];
      if (k === 'source' || k === 'destination' && adv) { var f = k === 'source' ? 'src' : 'dst';
        if (t[i + 1] === 'any') { i += 2; continue; } var w = t[i + 2] === '0' ? '0.0.0.0' : t[i + 2], rr = wcRange(t[i + 1], w); if (!rr) return null; r[f] = rr; r[f + 'T'] = t[i + 1] + ' ' + (w === '0.0.0.0' ? '0' : w); i += 3; continue; }
      if (k === 'destination-port' && adv && t[i + 1] === 'eq' && portNum(t[i + 2])) { r.dport = [portNum(t[i + 2]), portNum(t[i + 2])]; r.dportT = t[i + 2]; i += 3; continue; }
      return null; }
    return r;
  }
  ac('acl', 'rule <rest>', function (st, a) { var t = a[0].toLowerCase().split(/\s+/), A = acls(st)[top(st).n], id = null;
    if (/^\d+$/.test(t[0])) { id = +t[0]; t = t.slice(1); }
    var r = parseRule(top(st).n >= 3000, t); if (!r) return null;
    if (id === null) { var ks = Object.keys(A.rules).map(Number); id = ks.length ? Math.ceil((Math.max.apply(null, ks) + 1) / 5) * 5 : 5; }   // шаг правил — 5
    A.rules[id] = r; }, 'Specify an ACL rule');
  ac('acl', 'undo rule <n>', function (st, a) { delete acls(st)[top(st).n].rules[a[0]]; });
  ac('if', 'traffic-filter <w> acl <n>', function (st, a) { var d = a[0].toLowerCase(); if (['inbound', 'outbound'].indexOf(d) < 0 || !acls(st)[a[1]]) return null; x0(st)['tf' + d] = a[1]; });
  ac('if', 'undo traffic-filter <w>', function (st, a) { delete x0(st)['tf' + a[0].toLowerCase()]; });

  // ---------------------------------------------------------------- NAT
  ac('sys', 'nat address-group <n> <ip> <ip>', function (st, a) { if (IP.ip2n(a[2]) < IP.ip2n(a[1]) || IP.ip2n(a[2]) - IP.ip2n(a[1]) > 254) return null; var c = C(st); c.natGroups = c.natGroups || {}; c.natGroups[a[0]] = [a[1], a[2]]; });
  ac('sys', 'undo nat address-group <n>', function (st, a) { if (C(st).natGroups) delete C(st).natGroups[a[0]]; });
  ac('if', 'nat outbound <n>', function (st, a) { if (a[0] < 2000 || a[0] > 3999) return null; x0(st).natOut = { acl: a[0] }; }, 'Configure NAT outbound');
  ac('if', 'nat outbound <n> address-group <n>', function (st, a) { if (!(C(st).natGroups || {})[a[1]]) return null; x0(st).natOut = { acl: a[0], grp: a[1] }; });
  ac('if', 'nat outbound <n> address-group <n> no-pat', function (st, a) { if (!(C(st).natGroups || {})[a[1]]) return null; x0(st).natOut = { acl: a[0], grp: a[1], nopat: true }; });
  ac('if', 'undo nat outbound <rest>', function (st) { delete x0(st).natOut; });
  ac('if', 'nat server protocol <w> global <w> <w> inside <ip> <w>', function (st, a) { return natSrv(st, a[0], a[1], a[2], a[3], a[4]); }, 'Configure NAT server');
  ac('if', 'nat server protocol <w> global <w> <w> inside <ip>', function (st, a) { return natSrv(st, a[0], a[1], a[2], a[3], a[2]); });
  ac('if', 'nat server global <ip> inside <ip>', function (st, a) { var x = x0(st); x.natSrv = (x.natSrv || []).concat([{ g: a[0], in: a[1] }]); });
  ac('if', 'undo nat server <rest>', function (st) { delete x0(st).natSrv; });
  function natSrv(st, pr, g, gp, ip, ipp) { pr = pr.toLowerCase(); if (['tcp', 'udp'].indexOf(pr) < 0 || !portNum(gp) || !portNum(ipp)) return null;
    if (g.toLowerCase() !== 'current-interface' && IP.ip2n(g) === null) return null;
    var x = x0(st); x.natSrv = (x.natSrv || []).concat([{ pr: pr, g: g.toLowerCase() === 'current-interface' ? 'current-interface' : g, gp: gp, in: ip, ip: ipp }]); }

  // ---------------------------------------------------------------- DHCP
  ac('sys', 'dhcp enable', function (st) { C(st).dhcp = true; return 'Info: The operation may take a few seconds. Please wait for a moment.done.'; }, 'Enable DHCP');
  ac('sys', 'undo dhcp enable', function (st) { delete C(st).dhcp; });
  function pools(st) { var c = C(st); return c.pools || (c.pools = {}); }
  ac('sys', 'ip pool <w>', function (st, a) { var P = pools(st), n = !P[a[0]]; P[a[0]] = P[a[0]] || {}; Vr.push(st, { v: 'pool', key: 'pool', n: a[0], tag: 'ip-pool-' + a[0] });
    if (n) return 'Info: It\'s successful to create an IP address pool.'; }, 'Configure an IP address pool');
  ac('sys', 'undo ip pool <w>', function (st, a) { delete pools(st)[a[0]]; });
  function pl(st) { return pools(st)[top(st).n]; }
  ac('pool', 'network <ip> mask <mask>', function (st, a) { if (a[1] < 1 || a[1] > 30) return null; pl(st).net = IP.netOf(a[0], a[1]); });
  ac('pool', 'gateway-list <ip>', function (st, a) { pl(st).gw = a[0]; });
  ac('pool', 'dns-list <rest>', function (st, a) { var L = a[0].split(/\s+/); if (L.some(function (x) { return IP.ip2n(x) === null; })) return null; pl(st).dns = L; });
  ac('pool', 'excluded-ip-address <ip>', function (st, a) { var p = pl(st); p.excl = (p.excl || []).concat([[a[0], a[0]]]); });
  ac('pool', 'excluded-ip-address <ip> <ip>', function (st, a) { var p = pl(st); p.excl = (p.excl || []).concat([[a[0], a[1]]]); });
  ac('pool', 'lease unlimited', function (st) { pl(st).lease = 'unlimited'; });
  ac('pool', 'lease day <n>', function (st, a) { pl(st).lease = [a[0], 0, 0]; });
  ac('pool', 'lease day <n> hour <n>', function (st, a) { pl(st).lease = [a[0], a[1], 0]; });
  ac('pool', 'lease day <n> hour <n> minute <n>', function (st, a) { pl(st).lease = [a[0], a[1], a[2]]; });
  ac('pool', 'static-bind ip-address <ip> mac-address <w>', function (st, a) { var p = pl(st); p.bind = (p.bind || []).concat([[a[0], a[1]]]); });
  ac('if', 'dhcp select <w>', function (st, a) { var w = a[0].toLowerCase(); if (!C(st).dhcp || ['global', 'interface', 'relay'].indexOf(w) < 0) return null; x0(st).dsel = w; });
  ac('if', 'undo dhcp select <w>', function (st) { delete x0(st).dsel; });
  ac('if', 'dhcp server dns-list <rest>', function (st, a) { x0(st).ddns = a[0].split(/\s+/); });
  ac('if', 'dhcp relay server-ip <ip>', function (st, a) { x0(st).relay = a[0]; });
  ac('if', 'undo dhcp relay server-ip <ip>', function (st) { delete x0(st).relay; });

  // ---------------------------------------------------------------- VRRP
  function vr(st, id) { var x = x0(st); x.vrrp = x.vrrp || {}; return x.vrrp[id] || (x.vrrp[id] = {}); }
  ac('if', 'vrrp vrid <n> virtual-ip <ip>', function (st, a) { if (a[0] < 1 || a[0] > 255 || !x0(st).ip) return null; vr(st, a[0]).vip = a[1]; }, 'Configure VRRP');
  ac('if', 'vrrp vrid <n> priority <n>', function (st, a) { if (a[1] < 1 || a[1] > 254) return null; vr(st, a[0]).prio = a[1]; });
  ac('if', 'vrrp vrid <n> preempt-mode timer delay <n>', function (st, a) { vr(st, a[0]).delay = a[1]; });
  ac('if', 'vrrp vrid <n> preempt-mode disable', function (st, a) { vr(st, a[0]).nopre = true; });
  ac('if', 'vrrp vrid <n> timer advertise <n>', function (st, a) { vr(st, a[0]).adv = a[1]; });
  ac('if', 'undo vrrp vrid <n>', function (st, a) { if (x0(st).vrrp) delete x0(st).vrrp[a[0]]; });

  // ---------------------------------------------------------------- compile: настройки VRP → модель ESR
  function ifKey(st, n) { var x = C(st).ifs[n] || {}; if (/^LoopBack/.test(n)) return 'lo' + n.slice(8); if (n.indexOf('.') > 0) return x.vid ? n.split('.')[0] + '.' + x.vid : null; return n; }
  function inNet(ip, len, nets) { return nets.some(function (w) { var r = wcRange(w[0], w[1]); return r && IP.ip2n(ip) >= IP.ip2n(r[0]) && IP.ip2n(ip) <= IP.ip2n(r[1]); }); }
  function aclRules(L, permitRest) { var o = {}; Object.keys(L.rules).forEach(function (k) { var r = L.rules[k];
      o[k] = { on: true, act: r.act, proto: r.proto || 'any', src: r.src, dst: r.dst, dport: r.dport }; });
    if (permitRest) o[99999] = { on: true, act: 'permit', proto: 'any' }; return { rules: o }; }
  EL.vrp.compileAr = function (st) {
    var c = C(st), run = st.run, net = st.net, d = net && net.devs[st.dev], ports = d ? Vr.dports(net, d) : Object.keys(run.ifs).filter(function (k) { return /^(GE|Eth)/.test(k); });
    var old = run.ifs, ifs = {}, sub = {};
    Object.keys(old).forEach(function (k) { if (!/^(GE|Eth)\d+\/\d+\/\d+$/.test(k)) ifs[k] = old[k]; });   // служебные порты (console и т. п.) не трогаем
    run.host = c.sysname || 'Huawei'; run.routes = []; run.rip = null; run.ospf = null; run.acls = {}; run.snat = null; run.dnat = null; run.dhcp = null; run.relay = false;
    Object.keys(ifs).forEach(function (k) { if (/^(lo\d|GE|Eth)/.test(k)) delete ifs[k]; });
    ports.forEach(function (p) { ifs[p] = { ip: null, fw: false, shut: false, speed: (old[p] || {}).speed, duplex: (old[p] || {}).duplex }; });
    Object.keys(c.ifs).forEach(function (n) { var x = c.ifs[n], k = ifKey(st, n); if (!k) return; if (k !== n) sub[k] = n;
      var y = ifs[k] = ifs[k] || { ip: null, fw: false, shut: false };
      y.shut = !!x.shut; y.ip = x.ip && isL3(st, n) ? x.ip[0] + '/' + x.ip[1] : null; if (x.mtu) y.mtu = x.mtu;
      if (x.tfinbound && (c.acls || {})[x.tfinbound]) { run.acls['hw' + x.tfinbound] = aclRules(c.acls[x.tfinbound], true); y.acl = 'hw' + x.tfinbound; }
      if (x.relay && x.dsel === 'relay' && c.dhcp) { y.helper = x.relay; run.relay = true; }
      var vk = Object.keys(x.vrrp || {}).filter(function (id) { return x.vrrp[id].vip; })[0];
      if (vk && x.ip) y.vrrp = { on: true, id: +vk, ip: x.vrrp[vk].vip + '/' + x.ip[1], prio: x.vrrp[vk].prio || 100 }; });
    st.vrp.sub = sub;
    run.ifs = ifs;
    run.routes = (c.routes || []).map(function (r) { return { net: r.net, nh: r.nh, ad: EL.vrp.adOf(r.pref), pref: r.pref }; });
    // RIP: интерфейс в процессе, если его адрес в классовой сети network; остальные — пассивные (не шлют и не слушают)
    if (c.rip) { var R = c.rip, nets = R.nets.map(function (n) { var v = IP.ip2n(n); return n + '/' + (v >>> 31 === 0 ? 8 : v >>> 30 === 2 ? 16 : 24); });
      var pas = []; Object.keys(ifs).forEach(function (k) { var y = ifs[k]; if (!y.ip) return; var ip = y.ip.split('/')[0];
        var inR = nets.some(function (n) { return IP.sameNet(ip, n.split('/')[0], +n.split('/')[1]); });
        var hn = sub[k] || (/^lo/.test(k) ? 'LoopBack' + k.slice(2) : k);
        if (!inR || R.silent.indexOf(hn) >= 0) pas.push(k); });
      run.rip = { on: nets.length > 0, nets: nets, passive: pas, redist: (R.imp || []).map(function (w) { return w === 'direct' ? 'connected' : w; }), ver: R.ver || 1 }; }
    if (c.ospf) { var O = c.ospf; run.ospf = { id: O.id, rid: O.rid || null, on: true, areas: {}, dra: O.dra || null };
      Object.keys(O.areas).forEach(function (a) { run.ospf.areas[a] = { on: true };
        Object.keys(ifs).forEach(function (k) { var y = ifs[k]; if (!y.ip || y.ospf) return; var p = y.ip.split('/'); if (!inNet(p[0], +p[1], O.areas[a].nets)) return;
          var hn = sub[k] || (/^lo/.test(k) ? 'LoopBack' + k.slice(2) : k), x = c.ifs[hn] || {};
          y.ospf = { on: true, inst: O.id, area: a, passive: O.silent.indexOf(hn) >= 0, cost: x.ocost || (/^lo/.test(k) ? 0 : 1), hello: x.hello || 10, dead: x.dead || (x.hello ? x.hello * 4 : 40),
            net: x.ntype === 'p2p' ? 'point-to-point' : 'broadcast', prio: x.oprio !== undefined ? x.oprio : 1, mtuCheck: !!x.mtuEn }; }); }); }
    // NAT: Easy IP / пул — Source NAT по разрешающим правилам ACL; nat server — Destination NAT на этом интерфейсе
    Object.keys(c.ifs).forEach(function (n) { var x = c.ifs[n], k = ifKey(st, n); if (!k) return;
      if (x.natOut && (c.acls || {})[x.natOut.acl]) { var L = c.acls[x.natOut.acl], rs = {}, q = 1;
        Object.keys(L.rules).map(Number).sort(function (a, b) { return a - b; }).forEach(function (id) { var r = L.rules[id]; if (r.act !== 'permit') return;
          rs[q++] = { on: true, act: 'interface', src: r.src, dst: r.dst, proto: r.proto && r.proto !== 'any' ? r.proto : null }; });
        run.snat = run.snat || { rulesets: {} }; run.snat.rulesets['hw-' + k] = { ifn: k, rules: rs }; }
      if (x.natSrv && x.ip) { var ds = {}; x.natSrv.forEach(function (s, i) { var g = s.g === 'current-interface' ? x.ip[0] : s.g;
          ds[i + 1] = { on: true, to: s.in, dst: [g, g], proto: s.pr || null, dport: s.gp ? [portNum(s.gp), portNum(s.gp)] : null }; });
        run.dnat = run.dnat || { rulesets: {} }; run.dnat.rulesets['hw-' + k] = { ifn: k, rules: ds }; } });
    // DHCP: глобальный пул — для интерфейса с dhcp select global в его подсети; пул интерфейса — подсеть и шлюз интерфейса
    if (c.dhcp) { var pp = {};
      Object.keys(c.ifs).forEach(function (n) { var x = c.ifs[n]; if (!x.ip || !x.dsel) return;
        if (x.dsel === 'interface') { var nt = IP.netOf(x.ip[0], x.ip[1]); pp[n] = { net: nt, range: hostRange(nt, [[x.ip[0], x.ip[0]]]), gw: x.ip[0], dns: (x.ddns || [])[0] || null, lease: null }; }
        if (x.dsel === 'global') Object.keys(c.pools || {}).forEach(function (k) { var p = c.pools[k]; if (!p.net || !IP.sameNet(x.ip[0], p.net.split('/')[0], +p.net.split('/')[1])) return;
          pp[k] = { net: p.net, range: hostRange(p.net, (p.excl || []).concat(p.gw ? [[p.gw, p.gw]] : [])), gw: p.gw || null, dns: (p.dns || [])[0] || null, lease: null }; }); });
      Object.keys(c.pools || {}).forEach(function (k) { var p = c.pools[k];      // пул не своей подсети — для запросов через relay (выбор по giaddr)
        if (pp[k] || !p.net || Object.keys(ifs).some(function (q) { var y = ifs[q]; return y.ip && IP.sameNet(y.ip.split('/')[0], p.net.split('/')[0], +p.net.split('/')[1]); })) return;
        pp[k] = { net: p.net, range: hostRange(p.net, (p.excl || []).concat(p.gw ? [[p.gw, p.gw]] : [])), gw: p.gw || null, dns: (p.dns || [])[0] || null, lease: null }; });
      run.dhcp = { on: Object.keys(pp).length > 0, pools: pp }; }
    st.cand = EL.clone(run);
  };
  // диапазон выдачи: вся подсеть без исключённых адресов на концах (адреса внутри диапазона модель всё равно не выдаёт — они заняты)
  function hostRange(nt, ex) { var p = nt.split('/'), lo = IP.ip2n(p[0]) + 1, hi = IP.ip2n(p[0]) + Math.pow(2, 32 - +p[1]) - 2;
    var ok = function (n) { return !ex.some(function (e) { return n >= IP.ip2n(e[0]) && n <= IP.ip2n(e[1]); }); };
    while (lo <= hi && !ok(lo)) lo++; while (hi >= lo && !ok(hi)) hi--; return lo <= hi ? [IP.n2ip(lo), IP.n2ip(hi)] : null; }

  // ---------------------------------------------------------------- display current-configuration (части маршрутизатора)
  function ruleTxt(id, r) { return ' rule ' + id + ' ' + r.act + (r.proto && r.proto !== 'any' ? ' ' + r.proto : r.proto === 'any' && r.dstT === undefined && r.srcT === undefined ? ' ip' : r.proto === 'any' ? ' ip' : '') +
    (r.srcT ? ' source ' + r.srcT : '') + (r.dstT ? ' destination ' + r.dstT : '') + (r.dport ? ' destination-port eq ' + (Object.keys(PORTN).filter(function (k) { return PORTN[k] === r.dport[0]; })[0] || r.dport[0]) : ''); }
  function ifLinesAr(x, n) {
    var o = [];
    if (x.desc) o.push(' description ' + x.desc); if (x.shut) o.push(' shutdown'); if (x.l3) o.push(' undo portswitch');
    if (x.mtu) o.push(' mtu ' + x.mtu);
    if (x.vid) o.push(' dot1q termination vid ' + x.vid);
    if (x.ip) o.push(' ip address ' + x.ip[0] + ' ' + IP.len2mask(x.ip[1]));
    if (x.arpb) o.push(' arp broadcast enable');
    Object.keys(x.vrrp || {}).forEach(function (id) { var v = x.vrrp[id]; if (v.vip) o.push(' vrrp vrid ' + id + ' virtual-ip ' + v.vip);
      if (v.prio) o.push(' vrrp vrid ' + id + ' priority ' + v.prio); if (v.delay !== undefined) o.push(' vrrp vrid ' + id + ' preempt-mode timer delay ' + v.delay);
      if (v.nopre) o.push(' vrrp vrid ' + id + ' preempt-mode disable'); if (v.adv) o.push(' vrrp vrid ' + id + ' timer advertise ' + v.adv); });
    if (x.ntype) o.push(' ospf network-type ' + x.ntype); if (x.hello) o.push(' ospf timer hello ' + x.hello); if (x.dead) o.push(' ospf timer dead ' + x.dead);
    if (x.ocost) o.push(' ospf cost ' + x.ocost); if (x.oprio !== undefined) o.push(' ospf dr-priority ' + x.oprio); if (x.mtuEn) o.push(' ospf mtu-enable');
    if (x.oauth) o.push(' ospf authentication-mode md5 ' + x.oauth.split(' ')[0] + ' cipher ' + x.oauth.split(' ')[1]);
    if (x.ripVer) o.push(' rip version ' + x.ripVer);
    if (x.tfinbound) o.push(' traffic-filter inbound acl ' + x.tfinbound); if (x.tfoutbound) o.push(' traffic-filter outbound acl ' + x.tfoutbound);
    (x.natSrv || []).forEach(function (s) { o.push(s.pr ? ' nat server protocol ' + s.pr + ' global ' + s.g + ' ' + s.gp + ' inside ' + s.in + ' ' + s.ip : ' nat server global ' + s.g + ' inside ' + s.in); });
    if (x.natOut) o.push(' nat outbound ' + x.natOut.acl + (x.natOut.grp ? ' address-group ' + x.natOut.grp + (x.natOut.nopat ? ' no-pat' : '') : ''));
    if (x.dsel) o.push(' dhcp select ' + x.dsel); if (x.ddns) o.push(' dhcp server dns-list ' + x.ddns.join(' ')); if (x.relay) o.push(' dhcp relay server-ip ' + x.relay);
    return o;
  }
  EL.vrp.renderAr = function (st) {
    var c = C(st), net = st.net, d = net && net.devs[st.dev], out = [];
    if (c.dhcp) out.push({ h: 'dhcp', L: ['dhcp enable'] });
    Object.keys(c.acls || {}).sort().forEach(function (n) { var L = c.acls[n]; out.push({ h: 'acl ' + n, L: ['acl number ' + n].concat(Object.keys(L.rules).map(Number).sort(function (a, b) { return a - b; }).map(function (id) { return ruleTxt(id, L.rules[id]); })) }); });
    if (c.natGroups) out.push({ h: 'nat', L: Object.keys(c.natGroups).map(function (k) { return ' nat address-group ' + k + ' ' + c.natGroups[k].join(' '); }) });
    Object.keys(c.pools || {}).forEach(function (k) { var p = c.pools[k], L = ['ip pool ' + k];
      if (p.gw) L.push(' gateway-list ' + p.gw); if (p.net) L.push(' network ' + p.net.split('/')[0] + ' mask ' + IP.len2mask(+p.net.split('/')[1]));
      (p.excl || []).forEach(function (e) { L.push(' excluded-ip-address ' + e[0] + (e[1] !== e[0] ? ' ' + e[1] : '')); });
      (p.bind || []).forEach(function (b) { L.push(' static-bind ip-address ' + b[0] + ' mac-address ' + b[1]); });
      if (p.lease) L.push(p.lease === 'unlimited' ? ' lease unlimited' : ' lease day ' + p.lease[0] + ' hour ' + p.lease[1] + ' minute ' + p.lease[2]);
      if (p.dns) L.push(' dns-list ' + p.dns.join(' ')); out.push({ h: 'pool', L: L }); });
    var ph = d ? Vr.dports(net, d) : [], ks = Object.keys(c.ifs);
    ph.forEach(function (p) { [p].concat(ks.filter(function (k) { return k.split('.')[0] === p && k !== p; })).forEach(function (k) {
      out.push({ h: 'interface ' + full(k), L: ['interface ' + full(k)].concat(ifLinesAr(c.ifs[k] || {}, k)) }); }); });
    ks.filter(function (k) { return /^LoopBack/.test(k); }).forEach(function (k) { out.push({ h: 'interface ' + k, L: ['interface ' + k].concat(ifLinesAr(c.ifs[k], k)) }); });
    out.push({ h: 'interface NULL0', L: ['interface NULL0'] });
    if (c.ospf) { var O = c.ospf, L = ['ospf ' + O.id + (O.rid ? ' router-id ' + O.rid : '')];
      O.silent.forEach(function (s) { L.push(' silent-interface ' + full(s)); }); if (O.dra) L.push(' default-route-advertise' + (O.dra === 'always' ? ' always' : ''));
      (O.imp || []).forEach(function (w) { L.push(' import-route ' + w); });
      Object.keys(O.areas).forEach(function (a) { L.push(' area ' + a); if (O.areas[a].auth) L.push('  authentication-mode md5 ' + O.areas[a].auth.replace(' ', ' cipher '));
        O.areas[a].nets.forEach(function (w) { L.push('  network ' + w[0] + ' ' + w[1]); }); });
      out.push({ h: 'ospf', L: L }); }
    if (c.rip) { var R = c.rip, RL = ['rip ' + R.id]; if (R.noSum) RL.push(' undo summary'); if (R.ver) RL.push(' version ' + R.ver);
      R.nets.forEach(function (n) { RL.push(' network ' + n); }); R.silent.forEach(function (s) { RL.push(' silent-interface ' + full(s)); });
      (R.imp || []).forEach(function (w) { RL.push(' import-route ' + w); }); if (R.defOrig) RL.push(' default-route originate'); out.push({ h: 'rip', L: RL }); }
    if ((c.routes || []).length) out.push({ h: 'route', L: c.routes.map(function (r) { var p = r.net.split('/');
      return 'ip route-static ' + p[0] + ' ' + IP.len2mask(+p[1]) + ' ' + r.nh + (r.pref !== 60 ? ' preference ' + r.pref : ''); }) });
    return out;
  };

  // ---------------------------------------------------------------- display (маршрутизатор)
  function hn(st, k) { return full((st.vrp.sub || {})[k] || k); }
  function rid(net, id) { var c = net.devs[id].st.run; return (c.ospf && c.ospf.rid) || (net.ifaces(id).map(function (f) { return f.ip; }).sort(function (a, b) { return IP.ip2n(b) - IP.ip2n(a); })[0] || '0.0.0.0'); }
  function adj(st) { var net = st.net; net.dyn(); var A = (net._adj || {}).O || {}; return Object.keys(A).map(function (k) { return A[k]; }).filter(function (r) { return r.id === st.dev; }); }
  var OST = { full: 'Full', '2way': '2-Way', init: 'Init', exstart: 'ExStart', exchange: 'Exchange', loading: 'Loading' };
  ac('*', 'display ospf peer brief', function (st) { var net = st.net, run = st.run; if (!net || !run.ospf) return '';
    var o = ['', '  OSPF Process ' + run.ospf.id + ' with Router ID ' + rid(net, st.dev), '    Peer Statistic Information', ' ' + new Array(77).join('-'),
      ' Area Id          Interface                             Neighbor id       State'], L = adj(st);
    L.forEach(function (r) { var y = run.ifs[r.ifn] || {}; o.push(' ' + pad((y.ospf || {}).area || '0.0.0.0', 17) + pad(hn(st, r.ifn), 40) + pad(rid(net, r.dev), 18) + (OST[r.state] || r.state)); });
    o.push(' ' + new Array(77).join('-'), 'Total Peer(s):     ' + L.length); return o.join('\n'); }, 'Display OSPF peer brief information');
  ac('*', 'display ospf peer', function (st) { var net = st.net, run = st.run; if (!net || !run.ospf) return '';
    var o = ['', '         OSPF Process ' + run.ospf.id + ' with Router ID ' + rid(net, st.dev), '                 Neighbors'];
    adj(st).forEach(function (r) { var y = run.ifs[r.ifn] || {}, me = net.ifaces(st.dev).filter(function (f) { return f.name === r.ifn; })[0] || {}, t = (y.ospf || {}).dead || 40;
      o.push('', ' Area ' + ((y.ospf || {}).area || '0.0.0.0') + ' interface ' + me.ip + '(' + hn(st, r.ifn) + ')\'s neighbors', ' Router ID: ' + pad(rid(net, r.dev), 17) + 'Address: ' + r.nh,
        '   State: ' + (OST[r.state] || r.state) + '  Mode:Nbr is  Master  Priority: 1', '   MTU: 0', '   Dead timer due in ' + Math.max(0, Math.round(r.lost !== undefined ? t - (net.now - r.lost) : t - ((net.now - r.since) % ((y.ospf || {}).hello || 10)))) + '  sec',
        '   Retrans timer interval: 0', '   Neighbor is up for ' + hms(net.now - r.since), '   Authentication Sequence: [ 0 ]'); });
    return o.join('\n'); });
  function hms(s) { s = Math.max(0, Math.floor(s)); return ('0' + Math.floor(s / 3600)).slice(-2) + ':' + ('0' + Math.floor(s / 60) % 60).slice(-2) + ':' + ('0' + s % 60).slice(-2); }
  ac('*', 'display ospf interface', function (st) { var net = st.net, run = st.run; if (!net || !run.ospf) return '';
    var o = ['          OSPF Process ' + run.ospf.id + ' with Router ID ' + rid(net, st.dev), '                  Interfaces'];
    Object.keys(run.ospf.areas).forEach(function (a) { o.push('', ' Area: ' + a + '        (MPLS TE not enabled)', ' IP Address      Type         State    Cost  Pri   DR              BDR');
      net.ifaces(st.dev).forEach(function (f) { var y = (run.ifs[f.name] || {}).ospf; if (!y || y.area !== a) return;
        o.push(' ' + pad(f.ip, 16) + pad(y.net === 'point-to-point' ? 'P2P' : 'Broadcast', 13) + pad(y.net === 'point-to-point' ? 'P-2-P' : 'DR', 9) + pad(y.cost, 6) + pad(y.prio, 6) + pad('0.0.0.0', 16) + '0.0.0.0'); }); });
    return o.join('\n'); });
  ac('*', 'display rip <n> route', function (st, a) { var net = st.net, run = st.run; if (!net || !run.rip || C(st).rip.id !== a[0]) return '';
    var o = [' Route Flags: R - RIP', '              A - Aging, G - Garbage-collect', ' ' + new Array(75).join('-')], by = {};
    net.routes(st.dev).filter(function (r) { return r.p === 'R'; }).forEach(function (r) { (by[r.nh + '|' + r.ifn] = by[r.nh + '|' + r.ifn] || []).push(r); });
    Object.keys(by).forEach(function (k) { o.push(' Peer ' + k.split('|')[0] + '  on ' + hn(st, k.split('|')[1]), '      Destination/Mask        Nexthop     Cost   Tag     Flags   Sec');
      by[k].forEach(function (r) { o.push(('                  ' + r.net).slice(-18) + '         ' + pad(r.nh, 15) + pad(r.m, 5) + pad(0, 8) + pad('RA', 8) + (Math.floor(net.now || 0) % 30)); }); });
    return o.join('\n'); });
  ac('*', 'display acl <n>', function (st, a) { var L = (C(st).acls || {})[a[0]]; if (!L) return ''; var ks = Object.keys(L.rules).map(Number).sort(function (x, y) { return x - y; });
    return (a[0] < 3000 ? 'Basic' : 'Advanced') + ' ACL ' + a[0] + ', ' + ks.length + ' rule' + (ks.length === 1 ? '' : 's') + '\nAcl\'s step is 5\n' + ks.map(function (id) { return ruleTxt(id, L.rules[id]); }).join('\n'); });
  ac('*', 'display acl all', function (st) { var A = C(st).acls || {}; return Object.keys(A).sort().map(function (n) { var L = A[n], ks = Object.keys(L.rules).map(Number).sort(function (x, y) { return x - y; });
    return (n < 3000 ? 'Basic' : 'Advanced') + ' ACL ' + n + ', ' + ks.length + ' rule' + (ks.length === 1 ? '' : 's') + '\nAcl\'s step is 5\n' + ks.map(function (id) { return ruleTxt(id, L.rules[id]); }).join('\n'); }).join('\n\n'); });
  ac('*', 'display nat outbound', function (st) { var c = C(st), rows = Object.keys(c.ifs).filter(function (n) { return c.ifs[n].natOut; }), line = ' ' + new Array(75).join('-');
    return [' NAT Outbound Information:', line, ' Interface                     Acl     Address-group/IP/Interface      Type', line].concat(rows.map(function (n) { var x = c.ifs[n].natOut;
      return ' ' + pad(full(n), 29) + pad(x.acl, 8) + ('                              ' + (x.grp || (c.ifs[n].ip || ['0.0.0.0'])[0])).slice(-30) + '    ' + (x.grp ? (x.nopat ? 'no-pat' : 'pat') : 'easyip'); }), [line, '  Total : ' + rows.length]).join('\n'); });
  ac('*', 'display nat server', function (st) { var c = C(st), o = ['', '    Nat Server Information:'], n = 0;
    Object.keys(c.ifs).forEach(function (k) { (c.ifs[k].natSrv || []).forEach(function (s) { n++; var g = s.g === 'current-interface' ? 'current-interface' : s.g;
      o.push('    Interface  : ' + full(k), '    Global IP/Port     : ' + g + '/' + (s.gp ? portNum(s.gp) : '----'), '    Inside IP/Port     : ' + s.in + '/' + (s.ip ? portNum(s.ip) : '----'),
        '    Protocol : ' + (s.pr === 'tcp' ? '6(tcp)' : s.pr === 'udp' ? '17(udp)' : '----'), '    VPN instance-name  : ----', '    Acl number         : ----', '    Vrrp id            : ----', '    Description : ----', ''); }); });
    o.push('  Total :    ' + n); return o.join('\n'); });
  ac('*', 'display nat address-group', function (st) { var g = C(st).natGroups || {}, line = ' --------------------------------------';
    return ['NAT Address-Group Information:', line, ' Index   Start-address      End-address', line].concat(Object.keys(g).map(function (k) { return ' ' + pad(k, 4) + ('                ' + g[k][0]).slice(-16) + ('                 ' + g[k][1]).slice(-17); }), [line, '  Total : ' + Object.keys(g).length]).join('\n'); });
  function leaseTxt(l) { return l === 'unlimited' ? 'Unlimited' : (l ? l[0] + ' Days ' + l[1] + ' Hours ' + l[2] + ' Minutes' : '1 Days 0 Hours 0 Minutes'); }
  function poolText(st, name, p, iface) {
    var net = st.net, L = (net && st.leases) || {}, used = Object.keys(L).filter(function (k) { return p.net && IP.sameNet(L[k], p.net.split('/')[0], +p.net.split('/')[1]); }).length;
    var nt = p.net ? p.net.split('/') : ['0.0.0.0', '24'], tot = Math.pow(2, 32 - +nt[1]) - 3, s = IP.n2ip(IP.ip2n(nt[0]) + 1), e = IP.n2ip(IP.ip2n(nt[0]) + Math.pow(2, 32 - +nt[1]) - 2);
    return ['  Pool-name      : ' + name, '  Pool-No        : ' + (iface ? 0 : 1), '  Lease          : ' + leaseTxt(p.lease), '  Domain-name    : -', '  DNS-server0    : ' + ((p.dns || [])[0] || '-'),
      '  NBNS-server0   : -', '  Netbios-type   : -', '  Position       : ' + (iface ? 'Interface' : 'Local') + '           Status           : Unlocked', '  Gateway-0      : ' + (p.gw || '-'),
      '  Mask           : ' + IP.len2mask(+nt[1]), '  VPN instance   : --', ' ' + new Array(78).join('-'), '         Start           End     Total  Used  Idle(Expired)  Conflict  Disable', ' ' + new Array(78).join('-'),
      ('                ' + s).slice(-16) + ('                ' + e).slice(-16) + pad('', 0) + ('      ' + tot).slice(-6) + ('      ' + used).slice(-6) + ('            ' + (tot - used) + '(0)').slice(-14) + '         0        0', ' ' + new Array(78).join('-')].join('\n');
  }
  ac('*', 'display ip pool name <w>', function (st, a) { var p = (C(st).pools || {})[a[0]]; return p ? poolText(st, a[0], p) : ''; });
  ac('*', 'display ip pool interface <if>', function (st, a) { var x = C(st).ifs[a[0]]; if (!x || x.dsel !== 'interface' || !x.ip) return '';
    return poolText(st, full(a[0]), { net: IP.netOf(x.ip[0], x.ip[1]), gw: x.ip[0], dns: x.ddns }, true); });
  ac('*', 'display ip pool', function (st) { var P = C(st).pools || {}; return Object.keys(P).map(function (k) { return poolText(st, k, P[k]); }).join('\n\n'); });
  ac('*', 'display vrrp brief', function (st) { var net = st.net; if (!net) return ''; var t = net.vrrp()[st.dev] || {}, ks = Object.keys(t), m = 0, b = 0, n = 0;
    var rows = ks.map(function (k) { var v = t[k], s = !v.up ? 'Initialize' : v.master ? 'Master' : 'Backup'; if (s === 'Master') m++; else if (s === 'Backup') b++; else n++;
      return pad(v.id, 6) + pad(s, 13) + pad(hn(st, k), 25) + pad('Normal', 9) + v.vip.split('/')[0]; });
    return ['Total:' + ks.length + '     Master:' + m + '     Backup:' + b + '     Non-active:' + n, 'VRID  State        Interface                Type     Virtual IP', new Array(65).join('-')].concat(rows).join('\n'); });
  ac('*', 'display vrrp', function (st) { var net = st.net; if (!net) return ''; var t = net.vrrp()[st.dev] || {};
    return Object.keys(t).map(function (k) { var v = t[k], md = v.masterDev && net.devs[v.masterDev], mi = md ? ((md.st.run.ifs[Object.keys(net.vrrp()[v.masterDev] || {}).filter(function (q) { return net.vrrp()[v.masterDev][q].id === v.id; })[0]] || {}).ip || '').split('/')[0] : '-';
      var mp = md ? (net.vrrp()[v.masterDev][Object.keys(net.vrrp()[v.masterDev]).filter(function (q) { return net.vrrp()[v.masterDev][q].id === v.id; })[0]] || {}).prio : '-';
      return [hn(st, k) + ' | Virtual Router ' + v.id, '    State : ' + (!v.up ? 'Initialize' : v.master ? 'Master' : 'Backup'), '    Virtual IP : ' + v.vip.split('/')[0], '    Master IP : ' + mi,
        '    PriorityRun : ' + v.prio, '    PriorityConfig : ' + v.prio, '    MasterPriority : ' + mp, '    Preempt : YES   Delay Time : 0 s', '    TimerRun : 1 s', '    TimerConfig : 1 s',
        '    Auth type : NONE', '    Virtual MAC : 0000-5e00-01' + ('0' + (+v.id).toString(16)).slice(-2), '    Check TTL : YES', '    Config type : normal-vrrp'].join('\n'); }).join('\n'); });
  // ---------------------------------------------------------------- совместимость соседств с Huawei (AR-CR)
  // RIP: «By default, an interface sends only RIP-1 packets, and receives both RIP-1 and RIP-2 packets» (version_rip);
  //   с version 1 / version 2 в процессе — шлёт и принимает только эту версию. ESR в модели шлёт v2 и принимает обе.
  // OSPF: тип сети на концах линка должен совпадать — «both ends of the link must be identical» (ospf_network-type_1);
  //   проверяется, если хотя бы один из концов — Huawei (поведение Eltex при несовпадении в спецификациях не описано).
  function ripVer(net, id) { var d = net.devs[id]; if (d && EL.ios && EL.ios.isIos(d)) return (d.st.ios.c.rip || {}).ver || null;   // Cisco: так же, шлёт v1 по умолчанию
    return d && Vr.isVrp(d) && d.st.vrp.c.rip ? d.st.vrp.c.rip.ver || null : 'esr'; }
  var tl0 = EL.Net.prototype.timeLayer;
  EL.Net.prototype.timeLayer = function (proto, rs, info, tab) {
    var s = this;
    rs.forEach(function (id) { var I = info[id]; if (!I) return;
      I.nb = I.nb.filter(function (nb) {
        if (proto === 'R') { var mine = ripVer(s, id), his = ripVer(s, nb.dev), sent = his === 'esr' ? 2 : his || 1;
          return mine === 'esr' || !mine || mine === sent; }
        if (proto === 'O' && (Vr.isVrp(s.devs[id]) || Vr.isVrp(s.devs[nb.dev]))) {
          var a = (s.devs[id].st.run.ifs[nb.ifn] || {}).ospf || {}, nf = (s.ifaces(nb.dev).filter(function (f) { return f.ip === nb.nh; })[0] || {}).name,
            b = nf ? (s.devs[nb.dev].st.run.ifs[nf] || {}).ospf || {} : {};
          return (a.net || 'broadcast') === (b.net || 'broadcast'); }
        return true; }); });
    return tl0 ? tl0.apply(this, arguments) : undefined;
  };
  // имена интерфейсов в выводах ядра (маршруты): подынтерфейс — номер из конфигурации
  var ifn0 = Vr.ifn; Vr.ifn = function (n, st) { return st && st.vrp && st.vrp.sub && st.vrp.sub[n] ? full(st.vrp.sub[n]) : ifn0(n); };
})(typeof window !== 'undefined' ? window : global);
