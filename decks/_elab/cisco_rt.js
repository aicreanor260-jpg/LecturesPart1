/* Маршрутизаторы Cisco ISR (1941, 2901, 2911, ISR4321) — спецификация sources/cisco/spec/router-ios.md (PI-CR, OSPF-CR, RIP-CR, ACL-CG, NAT-CG, DHCP-CG, FHRP).
   Настройки IOS (st.ios.c) → st.run модели ESR (межсетевого экрана нет). По документации: интерфейсы маршрутизатора выключены (shutdown, HIG1900),
   AD: connected 0, static 1, OSPF 110, RIP 120; OSPF hello 10 / dead 40, priority 1, cost = 100 Мбит/с / полоса; RIP шлёт v1, принимает v1 и v2,
   auto-summary включено (не моделируется); ACL — первое совпадение, неявный deny в конце, входной и выходной; NAT inside/outside, PAT (overload);
   DHCP-сервер отвечает по пулу подсети, excluded-address; HSRP: priority 100, preempt выключен; VRRP: priority 100, preempt включён.
   Упрощения (в отчёте): EIGRP не моделируется (нет в модели сети); NAT с пулом и static NAT для исходящего трафика транслируют в адрес интерфейса;
   HSRP preempt не влияет (активный — наибольший приоритет); OSPF только одна область на маршрутизатор с разными network допускается (как в модели ESR). */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, I = EL.ios, cmd = I.cmd, pad = I.pad, full = I.full, short = I.short, P = EL.Net.prototype;
  function RT(st) { return st.ios.kind === 'rt'; }
  function rc(views, pat, run, d) { var e = cmd(views, pat, run, d); e.ok = RT; return e; }
  function C(st) { return st.ios.c; }
  function top(st) { return I.top(st); }
  function x0(st) { return I.cur(st)[0]; }
  function nm(st) { return top(st).name; }
  function wc(ip, w) { var a = IP.ip2n(ip), m = IP.ip2n(w); if (a === null || m === null) return null; var lo = (a & ~m) >>> 0; return [IP.n2ip(lo), IP.n2ip((lo | m) >>> 0)]; }

  // ---------------------------------------------------------------- интерфейсы
  rc('config', 'interface <if>', function (st, a) { var n = a[0], ph = n.split('.')[0], ports = st.net ? I.dports(st.net, st.net.devs[st.dev]) : [];
    if (/^(fa|gi)/.test(n) && ports.indexOf(ph) < 0) return null; if (/^(vlan|po)/.test(n)) return null;
    I.ifc(st, n); I.push(st, { v: n.indexOf('.') > 0 ? 'subif' : 'if', name: n }); }, 'Select an interface to configure');
  rc('config', 'no interface <if>', function (st, a) { if (!/\.|^lo/.test(a[0])) return null; delete C(st).ifs[a[0]]; });
  rc('subif', 'encapsulation dot1q <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return null; var x = x0(st); x.vid = a[0]; delete x.native; }, 'Set encapsulation type for an interface');
  rc('subif', 'encapsulation dot1q <n> native', function (st, a) { var x = x0(st); x.vid = a[0]; x.native = true; });
  rc('if subif', 'ip address <ip> <ip> secondary', function (st) { void st; return null; });
  rc('if subif', 'ip helper-address <ip>', function (st, a) { x0(st).helper = a[0]; }, 'Specify a destination address for UDP broadcasts');
  rc('if subif', 'no ip helper-address', function (st) { delete x0(st).helper; });
  rc('if subif', 'ip access-group <w> <w>', function (st, a) { var d = a[1].toLowerCase(); if (d !== 'in' && d !== 'out') return null; x0(st)['acl' + d] = a[0]; }, 'Specify access control for packets');
  rc('if subif', 'no ip access-group <w> <w>', function (st, a) { delete x0(st)['acl' + a[1].toLowerCase()]; });
  rc('if subif', 'ip nat inside', function (st) { x0(st).nat = 'inside'; }, 'NAT configuration commands');
  rc('if subif', 'ip nat outside', function (st) { x0(st).nat = 'outside'; });
  rc('if subif', 'no ip nat <w>', function (st) { delete x0(st).nat; });
  // OSPF / RIP на интерфейсе
  [['ip ospf hello-interval <n>', 'hello'], ['ip ospf dead-interval <n>', 'dead'], ['ip ospf cost <n>', 'ocost'], ['ip ospf priority <n>', 'oprio']].forEach(function (x) {
    rc('if subif', x[0], function (st, a) { if (a[0] > 65535 || x[1] === 'oprio' && a[0] > 255) return null; x0(st)[x[1]] = a[0]; });
    rc('if subif', 'no ' + x[0].replace(/ <n>$/, ''), function (st) { delete x0(st)[x[1]]; }); });
  rc('if subif', 'ip ospf network point-to-point', function (st) { x0(st).ntype = 'p2p'; });
  rc('if subif', 'ip ospf network broadcast', function (st) { x0(st).ntype = 'broadcast'; });
  rc('if subif', 'no ip ospf network', function (st) { delete x0(st).ntype; });
  // HSRP / VRRP
  function grp(st, k, n) { var x = x0(st); x[k] = x[k] || {}; return x[k][n] || (x[k][n] = {}); }
  rc('if subif', 'standby <n> ip <ip>', function (st, a) { if (a[0] > 255 || !x0(st).ip) return null; grp(st, 'hsrp', a[0]).ip = a[1]; }, 'HSRP interface configuration commands');
  rc('if subif', 'standby <n> priority <n>', function (st, a) { if (a[1] > 255) return null; grp(st, 'hsrp', a[0]).prio = a[1]; });
  rc('if subif', 'standby <n> preempt', function (st, a) { grp(st, 'hsrp', a[0]).pre = true; });
  rc('if subif', 'standby version <n>', function (st, a) { if (a[0] !== 1 && a[0] !== 2) return null; x0(st).hver = a[0]; });
  rc('if subif', 'no standby <n>', function (st, a) { if (x0(st).hsrp) delete x0(st).hsrp[a[0]]; });
  rc('if subif', 'vrrp <n> ip <ip>', function (st, a) { if (a[0] < 1 || a[0] > 255 || !x0(st).ip) return null; grp(st, 'vrrp', a[0]).ip = a[1]; }, 'VRRP Interface configuration commands');
  rc('if subif', 'vrrp <n> priority <n>', function (st, a) { if (a[1] < 1 || a[1] > 254) return null; grp(st, 'vrrp', a[0]).prio = a[1]; });
  rc('if subif', 'no vrrp <n>', function (st, a) { if (x0(st).vrrp) delete x0(st).vrrp[a[0]]; });
  rc('if subif', 'ip address dhcp', function (st) { x0(st).dhcpc = true; delete x0(st).ip; });

  // ---------------------------------------------------------------- статика, OSPF, RIP
  function route(st, a, ad) { var l = IP.mask2len(a[1]); if (l === null) return null; var c = C(st), net = IP.netOf(a[0], l);
    c.routes = (c.routes || []).filter(function (r) { return !(r.net === net && r.nh === a[2]); }); c.routes.push({ net: net, nh: a[2], ad: ad || 1 }); }
  rc('config', 'ip route <ip> <ip> <ip>', function (st, a) { return route(st, a); }, 'Establish static routes');
  rc('config', 'ip route <ip> <ip> <ip> <n>', function (st, a) { if (a[3] < 1 || a[3] > 255) return null; return route(st, a, a[3]); });
  rc('config', 'ip route <ip> <ip> <if>', function (st, a) { var l = IP.mask2len(a[1]); if (l === null) return null; var c = C(st); (c.routes = c.routes || []).push({ net: IP.netOf(a[0], l), dev: a[2], ad: 1 }); });
  rc('config', 'no ip route <ip> <ip> <ip>', function (st, a) { var l = IP.mask2len(a[1]), c = C(st), n = IP.netOf(a[0], l); c.routes = (c.routes || []).filter(function (r) { return !(r.net === n && r.nh === a[2]); }); });
  rc('config', 'no ip route <ip> <ip>', function (st, a) { var l = IP.mask2len(a[1]), c = C(st), n = IP.netOf(a[0], l); c.routes = (c.routes || []).filter(function (r) { return r.net !== n; }); });
  rc('config', 'router ospf <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return null; var c = C(st); if (!c.ospf || c.ospf.id !== a[0]) c.ospf = { id: a[0], nets: [], passive: [] };
    I.push(st, { v: 'router', proto: 'ospf' }); }, 'Enable a routing process');
  rc('config', 'no router ospf <n>', function (st) { delete C(st).ospf; });
  rc('config', 'router rip', function (st) { var c = C(st); c.rip = c.rip || { nets: [], passive: [] }; I.push(st, { v: 'router', proto: 'rip' }); });
  rc('config', 'no router rip', function (st) { delete C(st).rip; });
  function R(st) { return C(st)[top(st).proto]; }
  function isO(st) { return top(st).proto === 'ospf'; }
  rc('router', 'network <ip> <ip> area <w>', function (st, a) { if (!isO(st)) return null; var r = wc(a[0], a[1]), ar = /^\d+$/.test(a[2]) ? IP.n2ip(+a[2] >>> 0) : IP.ip2n(a[2]) !== null ? a[2] : null;
    if (!r || !ar) return null; var O = R(st); O.nets = O.nets.filter(function (x) { return !(x[0] === a[0] && x[1] === a[1]); }); O.nets.push([a[0], a[1], ar, a[2]]); }, 'Enable routing on an IP network');
  rc('router', 'no network <ip> <ip> area <w>', function (st, a) { if (!isO(st)) return null; var O = R(st); O.nets = O.nets.filter(function (x) { return !(x[0] === a[0] && x[1] === a[1]); }); });
  rc('router', 'router-id <ip>', function (st, a) { if (!isO(st)) return null; R(st).rid = a[0]; return 'Reload or use "clear ip ospf process" command, for this to take effect'; });
  rc('router', 'default-information originate', function (st) { R(st).dio = 'yes'; });
  rc('router', 'default-information originate always', function (st) { R(st).dio = 'always'; });
  rc('router', 'passive-interface <if>', function (st, a) { var r = R(st); if (r.passive.indexOf(a[0]) < 0) r.passive.push(a[0]); }, 'Suppress routing updates on an interface');
  rc('router', 'no passive-interface <if>', function (st, a) { var r = R(st); r.passive = r.passive.filter(function (x) { return x !== a[0]; }); });
  rc('router', 'auto-cost reference-bandwidth <n>', function (st, a) { if (!isO(st)) return null; R(st).refbw = a[0]; });
  rc('router', 'network <ip>', function (st, a) { if (isO(st)) return null; var n = IP.ip2n(a[0]), cl = n >>> 31 === 0 ? 8 : n >>> 30 === 2 ? 16 : 24, net = IP.netOf(a[0], cl).split('/')[0], r = R(st);
    if (r.nets.indexOf(net) < 0) r.nets.push(net); });
  rc('router', 'no network <ip>', function (st, a) { if (isO(st)) return null; var r = R(st); r.nets = r.nets.filter(function (x) { return x !== a[0]; }); });
  rc('router', 'version <n>', function (st, a) { if (isO(st) || a[0] < 1 || a[0] > 2) return null; R(st).ver = a[0]; });
  rc('router', 'no version', function (st) { delete R(st).ver; });
  rc('router', 'no auto-summary', function (st) { R(st).noAuto = true; });
  rc('router', 'auto-summary', function (st) { delete R(st).noAuto; });
  rc('router', 'redistribute static', function (st) { R(st).redistS = true; });
  rc('router', 'redistribute connected', function (st) { R(st).redistC = true; });

  // ---------------------------------------------------------------- ACL
  function acls(st) { var c = C(st); return c.acls || (c.acls = {}); }
  var PORTN = { www: 80, telnet: 23, ftp: 21, ssh: 22, smtp: 25, domain: 53, tftp: 69, pop3: 110, bootps: 67 };
  function pnum(w) { return /^\d+$/.test(w) ? +w : PORTN[String(w).toLowerCase()] || null; }
  function addr(t, i) {                      // any | host A | A W — [диапазон, токенов, текст]
    if (t[i] === 'any') return [null, 1, 'any']; if (t[i] === 'host' && IP.ip2n(t[i + 1] || '') !== null) return [[t[i + 1], t[i + 1]], 2, 'host ' + t[i + 1]];
    if (IP.ip2n(t[i] || '') !== null && IP.ip2n(t[i + 1] || '') !== null) { var r = wc(t[i], t[i + 1]); return r ? [r, 2, t[i] + ' ' + t[i + 1]] : null; }
    if (IP.ip2n(t[i] || '') !== null) return [[t[i], t[i]], 1, t[i]];
    return null;
  }
  function parseAce(std, t) {
    var r = { act: t[0] }, i = 1; if (r.act !== 'permit' && r.act !== 'deny') return null;
    if (std) { var a = addr(t, i); if (!a || i + a[1] !== t.length) return null; r.src = a[0]; r.srcT = a[2]; r.proto = 'any'; return r; }
    var pr = t[i++]; if (!/^(ip|tcp|udp|icmp)$/.test(pr || '')) return null; r.proto = pr === 'ip' ? 'any' : pr; r.protoT = pr;
    var s = addr(t, i); if (!s) return null; r.src = s[0]; r.srcT = s[2]; i += s[1];
    var d = addr(t, i); if (!d) return null; r.dst = d[0]; r.dstT = d[2]; i += d[1];
    if (t[i] === 'eq' && pnum(t[i + 1] || '')) { r.dport = [pnum(t[i + 1]), pnum(t[i + 1])]; r.dportT = t[i + 1]; i += 2; }
    if (t[i] === 'established') { r.est = true; i++; }
    return i === t.length ? r : null;
  }
  function addAce(st, name, std, line) { var A = acls(st); A[name] = A[name] || { std: std, rules: [] }; if (A[name].std !== std) return null;
    var r = parseAce(std, line.toLowerCase().split(/\s+/)); if (!r) return null; A[name].rules.push(r); }
  rc('config', 'access-list <n> <rest>', function (st, a) { var n = a[0], std = n >= 1 && n <= 99 || n >= 1300 && n <= 1999; if (!std && !(n >= 100 && n <= 199 || n >= 2000 && n <= 2699)) return null;
    if (/^remark /.test(a[1])) return; return addAce(st, String(n), std, a[1]); }, 'Add an access list entry');
  rc('config', 'no access-list <n>', function (st, a) { delete acls(st)[String(a[0])]; });
  rc('config', 'ip access-list standard <w>', function (st, a) { var A = acls(st); A[a[0]] = A[a[0]] || { std: true, rules: [] }; if (!A[a[0]].std) return null; I.push(st, { v: 'std', acl: a[0] }); }, 'Named access-list');
  rc('config', 'ip access-list extended <w>', function (st, a) { var A = acls(st); A[a[0]] = A[a[0]] || { std: false, rules: [] }; if (A[a[0]].std) return null; I.push(st, { v: 'ext', acl: a[0] }); });
  rc('config', 'no ip access-list <w> <w>', function (st, a) { delete acls(st)[a[1]]; });
  rc('std', 'permit <rest>', function (st, a) { return addAce(st, top(st).acl, true, 'permit ' + a[0]); }, 'Specify packets to forward');
  rc('std', 'deny <rest>', function (st, a) { return addAce(st, top(st).acl, true, 'deny ' + a[0]); }, 'Specify packets to reject');
  rc('ext', 'permit <rest>', function (st, a) { return addAce(st, top(st).acl, false, 'permit ' + a[0]); }, 'Specify packets to forward');
  rc('ext', 'deny <rest>', function (st, a) { return addAce(st, top(st).acl, false, 'deny ' + a[0]); }, 'Specify packets to reject');
  rc('std ext', 'remark <rest>', function () {});

  // ---------------------------------------------------------------- NAT
  function nat(st) { var c = C(st); return c.nat || (c.nat = { rules: [], pools: {} }); }
  rc('config', 'ip nat inside source list <w> interface <if> overload', function (st, a) { nat(st).rules.push({ k: 'list', acl: a[0], ifn: a[1], over: true }); }, 'NAT configuration commands');
  rc('config', 'ip nat inside source list <w> pool <w> overload', function (st, a) { nat(st).rules.push({ k: 'list', acl: a[0], pool: a[1], over: true }); });
  rc('config', 'ip nat inside source list <w> pool <w>', function (st, a) { nat(st).rules.push({ k: 'list', acl: a[0], pool: a[1] }); });
  rc('config', 'ip nat inside source static <ip> <ip>', function (st, a) { nat(st).rules.push({ k: 'static', local: a[0], glob: a[1] }); });
  rc('config', 'ip nat inside source static <w> <ip> <n> <ip> <n>', function (st, a) { var p = a[0].toLowerCase(); if (p !== 'tcp' && p !== 'udp') return null;
    nat(st).rules.push({ k: 'static', pr: p, local: a[1], lport: a[2], glob: a[3], gport: a[4] }); });
  rc('config', 'ip nat pool <w> <ip> <ip> netmask <ip>', function (st, a) { nat(st).pools[a[0]] = [a[1], a[2], a[3]]; });
  rc('config', 'no ip nat inside source <rest>', function (st) { nat(st).rules = []; });

  // ---------------------------------------------------------------- DHCP
  function pools(st) { var c = C(st); return c.pools || (c.pools = {}); }
  rc('config', 'ip dhcp excluded-address <ip>', function (st, a) { var c = C(st); (c.excl = c.excl || []).push([a[0], a[0]]); }, 'Prevent DHCP from assigning certain addresses');
  rc('config', 'ip dhcp excluded-address <ip> <ip>', function (st, a) { var c = C(st); (c.excl = c.excl || []).push([a[0], a[1]]); });
  rc('config', 'ip dhcp pool <w>', function (st, a) { pools(st)[a[0]] = pools(st)[a[0]] || {}; I.push(st, { v: 'dhcp', pool: a[0] }); }, 'Configure DHCP address pools');
  rc('config', 'no ip dhcp pool <w>', function (st, a) { delete pools(st)[a[0]]; });
  function pl(st) { return pools(st)[top(st).pool]; }
  rc('dhcp', 'network <ip> <ip>', function (st, a) { var l = IP.mask2len(a[1]); if (l === null) return null; pl(st).net = IP.netOf(a[0], l); }, 'Network number and mask');
  rc('dhcp', 'default-router <ip>', function (st, a) { pl(st).gw = a[0]; }, 'Default routers');
  rc('dhcp', 'dns-server <ip>', function (st, a) { pl(st).dns = a[0]; }, 'DNS servers');
  rc('dhcp', 'domain-name <w>', function (st, a) { pl(st).dom = a[0]; });
  rc('dhcp', 'lease <n>', function (st, a) { pl(st).lease = a[0]; });

  // ---------------------------------------------------------------- compile: IOS → модель ESR
  function key(st, n) { var x = C(st).ifs[n] || {}; if (/^lo/.test(n)) return n; if (n.indexOf('.') > 0) return x.native ? null : x.vid ? n.split('.')[0] + '.' + x.vid : null; return n; }
  function inWc(ip, nets) { return nets.filter(function (w) { var r = wc(w[0], w[1]); return r && IP.ip2n(ip) >= IP.ip2n(r[0]) && IP.ip2n(ip) <= IP.ip2n(r[1]); })[0]; }
  function aclModel(L) { var o = {}; L.rules.forEach(function (r, i) { o[(i + 1) * 10] = { on: true, act: r.act, proto: r.proto || 'any', src: r.src, dst: r.dst, dport: r.dport }; }); return { rules: o }; }
  EL.ios.compileRt = function (st) {
    var c = C(st), run = st.run, net = st.net, d = net && net.devs[st.dev], ports = d ? I.dports(net, d) : Object.keys(run.ifs).filter(function (k) { return /^(fa|gi)\d/.test(k); }), sub = {};
    var ifs = {}; Object.keys(run.ifs).forEach(function (k) { if (!/^(fa|gi|lo)\d/.test(k)) ifs[k] = run.ifs[k]; });
    run.host = c.hostname || 'Router'; run.acls = {}; run.snat = null; run.dnat = null; run.dhcp = null; run.relay = false; run.rip = null; run.ospf = null;
    ports.forEach(function (p) { var o = run.ifs[p] || {}; ifs[p] = { ip: null, fw: false, shut: true, speed: o.speed, duplex: o.duplex }; });
    Object.keys(c.ifs).forEach(function (n) { var x = c.ifs[n], k = key(st, n), ph = n.split('.')[0];
      if (n.indexOf('.') > 0 && x.native) { k = ph; }                 // encapsulation dot1q N native — нетегированный трафик на физическом
      if (!k) return; if (k !== n) sub[k] = n;
      var y = ifs[k] = ifs[k] || { ip: null, fw: false, shut: false };
      if (k === n || n.indexOf('.') < 0) y.shut = /^lo/.test(n) ? !!x.shut : !x.noShut;
      if (n.indexOf('.') > 0 && k !== ph) y.shut = !!x.shut;
      if (x.ip) y.ip = x.ip[0] + '/' + x.ip[1];
      if (x.aclin && (c.acls || {})[x.aclin]) { run.acls['cs' + x.aclin] = aclModel(c.acls[x.aclin]); y.acl = 'cs' + x.aclin; }
      if (x.aclout && (c.acls || {})[x.aclout]) { run.acls['cs' + x.aclout] = aclModel(c.acls[x.aclout]); y.aclOut = 'cs' + x.aclout; }
      if (x.helper) { y.helper = x.helper; run.relay = true; }
      var h = Object.keys(x.hsrp || {}).filter(function (g) { return x.hsrp[g].ip; })[0], v = Object.keys(x.vrrp || {}).filter(function (g) { return x.vrrp[g].ip; })[0];
      if (h && x.ip) y.vrrp = { on: true, id: 'hsrp' + h, ip: x.hsrp[h].ip + '/' + x.ip[1], prio: x.hsrp[h].prio || 100, hsrp: +h };
      else if (v && x.ip) y.vrrp = { on: true, id: +v, ip: x.vrrp[v].ip + '/' + x.ip[1], prio: x.vrrp[v].prio || 100 }; });
    st.ios.sub = sub; run.ifs = ifs;
    run.routes = (c.routes || []).filter(function (r) { return r.nh; }).map(function (r) { return { net: r.net, nh: r.nh, ad: r.ad || 1 }; });
    if (c.ospf) { var O = c.ospf, areas = {}, ref = O.refbw || 100;
      Object.keys(ifs).forEach(function (k) { var y = ifs[k]; if (!y.ip) return; var hit = inWc(y.ip.split('/')[0], O.nets); if (!hit) return;
        var hn = sub[k] || k, x = c.ifs[hn] || {}, bw = /^fa/.test(k) ? 100 : 1000; areas[hit[2]] = { on: true };
        y.ospf = { on: true, inst: O.id, area: hit[2], passive: O.passive.indexOf(hn) >= 0, cost: x.ocost || (/^lo/.test(k) ? 1 : Math.max(1, Math.floor(ref / bw))), hello: x.hello || 10,
          dead: x.dead || (x.hello ? x.hello * 4 : 40), net: x.ntype === 'p2p' ? 'point-to-point' : 'broadcast', prio: x.oprio !== undefined ? x.oprio : 1 }; });
      run.ospf = { id: O.id, rid: O.rid || null, on: true, areas: areas, dra: O.dio || null }; }
    if (c.rip) { var Rp = c.rip, nets = Rp.nets.map(function (n) { var v = IP.ip2n(n); return n + '/' + (v >>> 31 === 0 ? 8 : v >>> 30 === 2 ? 16 : 24); }), pas = [];
      Object.keys(ifs).forEach(function (k) { var y = ifs[k]; if (!y.ip) return; var ip = y.ip.split('/')[0], hn = sub[k] || k;
        if (!nets.some(function (n) { return IP.sameNet(ip, n.split('/')[0], +n.split('/')[1]); }) || Rp.passive.indexOf(hn) >= 0) pas.push(k); });
      run.rip = { on: nets.length > 0, nets: nets, passive: pas, redist: (Rp.redistS ? ['static'] : []).concat(Rp.redistC ? ['connected'] : []), ver: Rp.ver || 1, cisco: true }; }
    // NAT: inside source list → Source NAT на каждом outside-интерфейсе (в адрес интерфейса); static → Destination NAT на outside
    if (c.nat && c.nat.rules.length) { var outs = Object.keys(c.ifs).filter(function (n) { return c.ifs[n].nat === 'outside' && key(st, n); });
      outs.forEach(function (n) { var k = key(st, n), rs = {}, q = 1, ds = {}, dq = 1;
        c.nat.rules.forEach(function (r) {
          if (r.k === 'list') { var L = (c.acls || {})[r.acl]; if (!L) return; L.rules.forEach(function (a) { if (a.act === 'permit') rs[q++] = { on: true, act: 'interface', src: a.src, dst: a.dst, proto: a.proto && a.proto !== 'any' ? a.proto : null }; }); }
          if (r.k === 'static') { ds[dq++] = { on: true, to: r.local, dst: [r.glob, r.glob], proto: r.pr || null, dport: r.gport ? [r.gport, r.gport] : null }; rs[q++] = { on: true, act: 'interface', src: [r.local, r.local] }; } });
        run.snat = run.snat || { rulesets: {} }; run.snat.rulesets['cs-' + k] = { ifn: k, rules: rs };
        run.dnat = run.dnat || { rulesets: {} }; run.dnat.rulesets['cs-' + k] = { ifn: k, rules: ds }; }); }
    if (c.pools) { var pp = {}; Object.keys(c.pools).forEach(function (k) { var p = c.pools[k]; if (!p.net) return; var r = hostRange(p.net, (c.excl || []));
      if (r) pp[k] = { net: p.net, range: r, gw: p.gw || null, dns: p.dns || null, lease: null }; }); run.dhcp = { on: Object.keys(pp).length > 0, pools: pp }; }
    st.cand = EL.clone(run);
  };
  function hostRange(nt, ex) { var p = nt.split('/'), lo = IP.ip2n(p[0]) + 1, hi = IP.ip2n(p[0]) + Math.pow(2, 32 - +p[1]) - 2;
    var ok = function (n) { return !ex.some(function (e) { return n >= IP.ip2n(e[0]) && n <= IP.ip2n(e[1]); }); };
    while (lo <= hi && !ok(lo)) lo++; while (hi >= lo && !ok(hi)) hi--; return lo <= hi ? [IP.n2ip(lo), IP.n2ip(hi)] : null; }
  EL.ios.isShut = (function (o) { return function (st, k, x) { if (st.ios.kind === 'rt' && /^(fa|gi)\d+(\/\d+){1,2}$/.test(k)) return !x.noShut; return o(st, k, x); }; })(EL.ios.isShut);
  EL.ios.ifUp = (function (o) { return function (st, k, x) { if (/^lo\d/.test(k)) return true; if (k.indexOf('.') > 0) return !!st.net && st.net.ifaces(st.dev).some(function (f) { return (st.ios.sub[f.name] || f.name) === k; }); return o(st, k, x); }; })(EL.ios.ifUp);

  // выходной ACL (ip access-group … out) — проверка перед отправкой с интерфейса (точка проверки MTU выходного интерфейса)
  var mc0 = P.mtuCheck;
  P.mtuCheck = function (cur, iface, inIf, pk, steps) {
    var d = this.devs[cur], x = d && d.type === 'esr' && d.st.run.ifs[String(iface.name).split(':')[0]];
    if (x && x.aclOut) { var r = EL.aclPass(d.st.run.acls[x.aclOut], pk);
      if (!r.ok) { steps.push({ k: 'drop', t: d.name + ': список доступа ' + x.aclOut.replace(/^cs/, '') + ' на выходе ' + I.ifn(d.st, iface.name) + ' отбросил пакет от ' + pk.src + (r.rule ? '' : ' (неявный deny в конце списка)') });
        return { ok: false, why: 'Destination host unreachable', pk: pk }; } }
    return mc0 ? mc0.apply(this, arguments) : null;
  };
  // RIP Cisco: шлёт v1, принимает v1 и v2; с version 1 / version 2 — только свою (RIP-CR version), как у Huawei
  var tl0 = P.timeLayer;
  P.timeLayer = function (proto, rs, info) {
    var s = this;
    if (proto === 'R') rs.forEach(function (id) { var I0 = info[id]; if (!I0 || !I.isIos(s.devs[id])) return; var r = s.devs[id].st.ios.c.rip, mine = r && r.ver;
      I0.nb = I0.nb.filter(function (nb) { if (!mine) return true; var pd = s.devs[nb.dev], sent = I.isIos(pd) ? ((pd.st.ios.c.rip || {}).ver || 1) : EL.vrp && EL.vrp.isVrp(pd) ? ((pd.st.vrp.c.rip || {}).ver || 1) : 2; return sent === mine; }); });
    return tl0 ? tl0.apply(this, arguments) : undefined;
  };

  // ---------------------------------------------------------------- show running-config (маршрутизатор)
  function aceTxt(r) { return r.act + (r.protoT ? ' ' + r.protoT : '') + ' ' + r.srcT + (r.dstT !== undefined ? ' ' + r.dstT : '') + (r.dportT ? ' eq ' + r.dportT : '') + (r.est ? ' established' : ''); }
  EL.ios.renderRt = function (st, c, o) {
    var net = st.net, d = net && net.devs[st.dev], ks = Object.keys(c.ifs);
    if (c.excl) c.excl.forEach(function (e) { o.push('ip dhcp excluded-address ' + e[0] + (e[1] !== e[0] ? ' ' + e[1] : '')); });
    if (c.excl) o.push('!');
    Object.keys(c.pools || {}).forEach(function (k) { var p = c.pools[k]; o.push('ip dhcp pool ' + k); if (p.net) o.push(' network ' + p.net.split('/')[0] + ' ' + IP.len2mask(+p.net.split('/')[1]));
      if (p.gw) o.push(' default-router ' + p.gw); if (p.dns) o.push(' dns-server ' + p.dns); if (p.dom) o.push(' domain-name ' + p.dom); o.push('!'); });
    o.push('ip cef', 'no ipv6 cef', '!');
    var ph = d ? I.dports(net, d) : [];
    ks.filter(function (k) { return /^lo/.test(k); }).concat(ph.reduce(function (a, p) { return a.concat([p], ks.filter(function (k) { return k.indexOf(p + '.') === 0; })); }, [])).forEach(function (k) {
      var x = c.ifs[k] || {}; o.push('interface ' + full(k)); if (x.desc) o.push(' description ' + x.desc);
      if (x.vid) o.push(' encapsulation dot1Q ' + x.vid + (x.native ? ' native' : ''));
      if (x.ip) o.push(' ip address ' + x.ip[0] + ' ' + IP.len2mask(x.ip[1])); else if (x.dhcpc) o.push(' ip address dhcp'); else o.push(' no ip address');
      if (x.helper) o.push(' ip helper-address ' + x.helper); if (x.aclin) o.push(' ip access-group ' + x.aclin + ' in'); if (x.aclout) o.push(' ip access-group ' + x.aclout + ' out');
      if (x.nat) o.push(' ip nat ' + x.nat);
      if (x.hello) o.push(' ip ospf hello-interval ' + x.hello); if (x.dead) o.push(' ip ospf dead-interval ' + x.dead); if (x.ntype) o.push(' ip ospf network ' + (x.ntype === 'p2p' ? 'point-to-point' : 'broadcast'));
      if (x.ocost) o.push(' ip ospf cost ' + x.ocost); if (x.oprio !== undefined) o.push(' ip ospf priority ' + x.oprio);
      Object.keys(x.hsrp || {}).forEach(function (g) { var h = x.hsrp[g]; if (h.ip) o.push(' standby ' + g + ' ip ' + h.ip); if (h.prio) o.push(' standby ' + g + ' priority ' + h.prio); if (h.pre) o.push(' standby ' + g + ' preempt'); });
      Object.keys(x.vrrp || {}).forEach(function (g) { var h = x.vrrp[g]; if (h.ip) o.push(' vrrp ' + g + ' ip ' + h.ip); if (h.prio) o.push(' vrrp ' + g + ' priority ' + h.prio); });
      if (k.indexOf('.') < 0 && !/^lo/.test(k)) { if (I.isShut(st, k, x)) o.push(' shutdown'); o.push(' duplex auto', ' speed auto'); }
      o.push('!'); });
    if (c.rip) { var R0 = c.rip; o.push('router rip'); if (R0.ver) o.push(' version ' + R0.ver); R0.passive.forEach(function (p) { o.push(' passive-interface ' + full(p)); });
      R0.nets.forEach(function (n) { o.push(' network ' + n); }); if (R0.noAuto) o.push(' no auto-summary'); o.push('!'); }
    if (c.ospf) { var O = c.ospf; o.push('router ospf ' + O.id); if (O.rid) o.push(' router-id ' + O.rid); o.push(' log-adjacency-changes');
      O.passive.forEach(function (p) { o.push(' passive-interface ' + full(p)); }); O.nets.forEach(function (n) { o.push(' network ' + n[0] + ' ' + n[1] + ' area ' + n[3]); });
      if (O.dio) o.push(' default-information originate' + (O.dio === 'always' ? ' always' : '')); o.push('!'); }
    if (c.nat) { Object.keys(c.nat.pools).forEach(function (k) { var p = c.nat.pools[k]; o.push('ip nat pool ' + k + ' ' + p[0] + ' ' + p[1] + ' netmask ' + p[2]); });
      c.nat.rules.forEach(function (r) { o.push(r.k === 'list' ? 'ip nat inside source list ' + r.acl + (r.ifn ? ' interface ' + full(r.ifn) : ' pool ' + r.pool) + (r.over ? ' overload' : '')
        : 'ip nat inside source static ' + (r.pr ? r.pr + ' ' + r.local + ' ' + r.lport + ' ' + r.glob + ' ' + r.gport : r.local + ' ' + r.glob)); }); }
    o.push('ip classless'); (c.routes || []).forEach(function (r) { var p = r.net.split('/'); o.push('ip route ' + p[0] + ' ' + IP.len2mask(+p[1]) + ' ' + (r.nh || full(r.dev)) + (r.ad && r.ad !== 1 ? ' ' + r.ad : '')); });
    o.push('!', 'ip flow-export version 9', '!');
    Object.keys(c.acls || {}).forEach(function (k) { var L = c.acls[k];
      if (/^\d+$/.test(k)) L.rules.forEach(function (r) { o.push('access-list ' + k + ' ' + aceTxt(r)); });
      else { o.push('ip access-list ' + (L.std ? 'standard ' : 'extended ') + k); L.rules.forEach(function (r) { o.push(' ' + aceTxt(r)); }); } });
    if (Object.keys(c.acls || {}).length) o.push('!');
  };

  // ---------------------------------------------------------------- show (маршрутизатор)
  function rid(net, id) { var c = net.devs[id].st.run; return (c.ospf && c.ospf.rid) || (net.ifaces(id).map(function (f) { return f.ip; }).sort(function (a, b) { return IP.ip2n(b) - IP.ip2n(a); })[0] || '0.0.0.0'); }
  function adj(st) { var net = st.net; net.dyn(); var A = (net._adj || {}).O || {}; return Object.keys(A).map(function (k) { return A[k]; }).filter(function (r) { return r.id === st.dev; }); }
  function mmss(s) { s = Math.max(0, Math.round(s)); return Math.floor(s / 3600) + ':' + ('0' + Math.floor(s / 60) % 60).slice(-2) + ':' + ('0' + s % 60).slice(-2); }
  rc('exec', 'show ip ospf neighbor', function (st) { var net = st.net, run = st.run; if (!net || !run.ospf) return '';
    var o = ['', 'Neighbor ID     Pri   State           Dead Time   Address         Interface'];
    adj(st).forEach(function (r) { var y = run.ifs[r.ifn] || {}, t = (y.ospf || {}).dead || 40, pd = net.devs[r.dev], nf = (net.ifaces(r.dev).filter(function (f) { return f.ip === r.nh; })[0] || {}).name;
      var np = nf && pd.type === 'esr' ? (((pd.st.run.ifs[nf] || {}).ospf || {}).prio) : 1; np = np === undefined ? (I.isIos(pd) || EL.vrp && EL.vrp.isVrp(pd) ? 1 : 128) : np;
      var stt = r.state === 'full' ? 'FULL/' + ((y.ospf || {}).net === 'point-to-point' ? '  -' : np > 1 ? 'DR' : 'BDR') : r.state === '2way' ? '2WAY/DROTHER' : String(r.state).toUpperCase() + '/  -';
      o.push(pad(rid(net, r.dev), 16) + pad(np, 6) + pad(stt, 16) + pad(mmss(r.lost !== undefined ? t - (net.now - r.lost) : t - ((net.now - r.since) % ((y.ospf || {}).hello || 10))), 12) + pad(r.nh, 16) + I.ifn(st, r.ifn)); });
    return o.join('\n'); }, 'OSPF neighbor list').cfg = false;
  rc('exec', 'show ip ospf interface brief', function (st) { var net = st.net, run = st.run; if (!net || !run.ospf) return '';
    var o = ['Interface    PID   Area            IP Address/Mask    Cost  State Nbrs F/C'];
    net.ifaces(st.dev).forEach(function (f) { var y = (run.ifs[f.name] || {}).ospf; if (!y) return; var n = adj(st).filter(function (r) { return r.ifn === f.name; });
      o.push(pad(short(I.ifn(st, f.name)), 13) + pad(run.ospf.id, 6) + pad(y.area.split('.').reduce(function (a, b) { return a * 256 + +b; }, 0), 16) + pad(f.ip + '/' + f.len, 19) + pad(y.cost, 6) + pad(y.net === 'point-to-point' ? 'P2P' : 'DR', 6) +
        n.filter(function (r) { return r.state === 'full'; }).length + '/' + n.length); });
    return o.join('\n'); }).cfg = false;
  rc('exec', 'show ip protocols', function (st) { var run = st.run, o = [];
    if (run.ospf) o.push('Routing Protocol is "ospf ' + run.ospf.id + '"', '  Router ID ' + rid(st.net, st.dev), '  Routing for Networks:'); if (run.ospf) (C(st).ospf.nets || []).forEach(function (n) { o.push('    ' + n[0] + ' ' + n[1] + ' area ' + n[3]); });
    if (run.rip) o.push('Routing Protocol is "rip"', '  Default version control: send version ' + (run.rip.ver === 2 ? 2 : 1) + ', receive ' + (C(st).rip.ver ? 'version ' + C(st).rip.ver : 'any version'), '  Routing for Networks:');
    if (run.rip) C(st).rip.nets.forEach(function (n) { o.push('    ' + n); }); return o.join('\n'); }).cfg = false;
  rc('exec', 'show access-lists', function (st) { var A = C(st).acls || {};
    return Object.keys(A).map(function (k) { var L = A[k]; return (L.std ? 'Standard' : 'Extended') + ' IP access list ' + k + '\n' + L.rules.map(function (r, i) { return '    ' + (i + 1) * 10 + ' ' + aceTxt(r); }).join('\n'); }).join('\n'); }).cfg = false;
  rc('exec', 'show ip nat translations', function (st) { var net = st.net, ct = (net && net.ctLast) || [], o = ['Pro  Inside global     Inside local       Outside local      Outside global'];
    ct.filter(function (c) { return c.dev === st.dev && (c.kind === 's' || c.kind === 'd'); }).forEach(function (c) {
      if (c.kind === 's') o.push(pad(c.proto === 'icmp' ? 'icmp' : c.proto, 5) + pad(c.pub, 18) + pad(c.orig, 19) + pad(c.peer, 19) + c.peer);
      else o.push(pad(c.proto === 'icmp' ? 'icmp' : c.proto, 5) + pad(c.pub, 18) + pad(c.target, 19) + pad(c.client, 19) + c.client); });
    (C(st).nat || { rules: [] }).rules.filter(function (r) { return r.k === 'static' && !r.pr; }).forEach(function (r) { o.push(pad('---', 5) + pad(r.glob, 18) + pad(r.local, 19) + pad('---', 19) + '---'); });
    return o.join('\n'); }, 'Translation entries').cfg = false;
  rc('exec', 'show ip dhcp binding', function (st) { var L = st.leases || {}, o = ['IP address       Client-ID/              Lease expiration        Type', '                 Hardware address'];
    Object.keys(L).forEach(function (k) { var m = String(EL.mac ? EL.mac(k + 'eth0') : '').replace(/:/g, ''); o.push(pad(L[k], 17) + pad(m.slice(0, 4) + '.' + m.slice(4, 8) + '.' + m.slice(8, 12), 24) + pad('--', 24) + 'Automatic'); });
    return o.join('\n'); }).cfg = false;
  rc('exec', 'show standby brief', function (st) { var net = st.net; if (!net) return ''; var t = net.vrrp()[st.dev] || {};
    var o = ['                     P indicates configured to preempt.', '                     |', 'Interface   Grp  Pri P State    Active          Standby         Virtual IP'];
    Object.keys(t).forEach(function (k) { var v = t[k], y = st.run.ifs[k.split(':')[0]] || {}; if (!y.vrrp || !y.vrrp.hsrp) return; var md = v.masterDev && net.devs[v.masterDev];
      var act = v.master ? 'local' : md ? (md.st.run.ifs[Object.keys(net.vrrp()[v.masterDev]).filter(function (q) { return net.vrrp()[v.masterDev][q].id === v.id; })[0]] || {}).ip.split('/')[0] : 'unknown';
      o.push(pad(short(I.ifn(st, k)), 12) + pad(y.vrrp.hsrp, 5) + pad(v.prio, 4) + pad(((C(st).ifs[st.ios.sub[k] || k] || {}).hsrp || {})[y.vrrp.hsrp] && C(st).ifs[st.ios.sub[k] || k].hsrp[y.vrrp.hsrp].pre ? 'P' : ' ', 2) +
        pad(!v.up ? 'Init' : v.master ? 'Active' : 'Standby', 9) + pad(act, 16) + pad(v.master ? (v.peers > 1 ? 'unknown' : 'unknown') : 'local', 16) + v.vip.split('/')[0]); });
    return o.join('\n'); }, 'Hot standby information').cfg = false;
  rc('exec', 'show vrrp brief', function (st) { var net = st.net; if (!net) return ''; var t = net.vrrp()[st.dev] || {};
    var o = ['Interface          Grp Pri Time  Own Pre State   Master addr     Group addr'];
    Object.keys(t).forEach(function (k) { var v = t[k], y = st.run.ifs[k] || {}; if (!y.vrrp || y.vrrp.hsrp) return;
      o.push(pad(short(I.ifn(st, k)), 19) + pad(v.id, 4) + pad(v.prio, 4) + pad(3609, 6) + pad(' ', 4) + pad('Y', 4) + pad(!v.up ? 'Init' : v.master ? 'Master' : 'Backup', 8) + pad(v.master ? y.ip.split('/')[0] : '-', 16) + v.vip.split('/')[0]); });
    return o.join('\n'); }).cfg = false;
  // CDP — между соседями Cisco (Doc 43485)
  cmd('exec', 'show cdp neighbors', function (st) { var net = st.net; if (!net) return ''; if (st.ios.c.noCdp) return '% CDP is not enabled';
    var o = ['Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge', '                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone', '',
      'Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID'];
    I.dports(net, net.devs[st.dev]).forEach(function (p) { var pr = net.peer(st.dev, p), pd = pr && net.devs[pr.dev]; if (!pd || !I.isIos(pd) || pd.off || pd.st.ios.c.noCdp || !net.linkUp(st.dev, p)) return;
      o.push(pad(pd.st.ios.c.hostname || (pd.type === 'mes' ? 'Switch' : 'Router'), 17) + pad(short(p).replace(/^(Fa|Gi)/, '$1 '), 18) + pad(150 + ((net.now | 0) % 30), 11) + pad(pd.type === 'mes' ? 'S' : 'R', 12) + pad(pd.model, 10) + short(pr.port).replace(/^(Fa|Gi)/, '$1 ')); });
    return o.join('\n'); }, 'CDP information').cfg = false;
  cmd('exec', 'show cdp', function (st) { if (st.ios.c.noCdp) return '% CDP is not enabled'; return 'Global CDP information:\n        Sending CDP packets every 60 seconds\n        Sending a holdtime value of 180 seconds\n        Sending CDPv2 advertisements is  enabled'; }).cfg = false;
  cmd('exec', 'show arp', function (st) { var net = st.net; if (!net) return ''; var A = net.arp[st.dev] || {}, o = ['Protocol  Address          Age (min)  Hardware Addr   Type   Interface'];
    net.ifaces(st.dev).forEach(function (f) { var m = String(net.ifMac(st.dev, f)).replace(/:/g, ''); o.push(pad('Internet', 10) + pad(f.ip, 17) + pad('-', 11) + pad(m.slice(0, 4) + '.' + m.slice(4, 8) + '.' + m.slice(8, 12), 16) + pad('ARPA', 7) + I.ifn(st, f.name)); });
    Object.keys(A).forEach(function (ip) { var e = A[ip], m = String(e.mac).replace(/:/g, ''); o.push(pad('Internet', 10) + pad(ip, 17) + pad(Math.floor((net.now - (e.t || 0)) / 60), 11) + pad(m.slice(0, 4) + '.' + m.slice(4, 8) + '.' + m.slice(8, 12), 16) + pad('ARPA', 7) + I.ifn(st, e.ifn)); });
    return o.join('\n'); }).cfg = false;
})(typeof window !== 'undefined' ? window : global);
