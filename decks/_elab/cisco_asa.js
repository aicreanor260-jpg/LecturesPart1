/* Межсетевой экран Cisco ASA 5506 (как в Packet Tracer, ПО 9.6) — спецификация sources/cisco/spec/asa.md (CLI Book 9.2/9.12, Command Reference).
   До 9.7 порты 5506-X — обычные routed-интерфейсы GigabitEthernet1/1–1/8 (Quick Start «9.6 and Earlier»), bridge-group не нужен.
   Правила по документации (RT, NAT, MPF): nameif + security-level (inside без level → 100, остальные → 0); трафик с высокого уровня на низкий
   разрешён неявно, обратно — только по ACL (access-list … + access-group … in interface IF); одинаковый уровень — только с
   same-security-traffic permit inter-interface; ответы пропускаются по таблице соединений (stateful), но для ICMP — только при
   inspect icmp в policy-map global_policy (по умолчанию ICMP не инспектируется — пинг изнутри наружу не возвращается);
   NAT — object network + nat (real,mapped) dynamic interface | static A; маршрут — route IF net mask gw; DHCP — dhcpd address/enable.
   Вид: «show interface ip brief», «show nameif», «show route», «show xlate», «show access-list», ping «!!!!!» / «?????».
   Упрощения (в отчёте): нет заводской конфигурации (схема начинается с пустой), static NAT для исходящего трафика — в адрес интерфейса,
   ICMP к самой ASA разрешён (icmp permit по умолчанию), Telnet/SSH/ASDM-доступ к ASA не моделируется. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, I = EL.ios, cmd = I.cmd, pad = I.pad, full = I.full, P = EL.Net.prototype;
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  EL.MODELS['ASA 5506'] = { type: 'esr', kind: 'cs-asa', portList: range('gi1/', 1, 8), ports: 8, group: 'Cisco (как в Packet Tracer)', vendor: 'cisco', host: 'ciscoasa', ios: '9.6',
    note: 'Межсетевой экран Cisco ASA 5506-X (ПО 9.6, как в Packet Tracer): GigabitEthernet1/1–1/8, nameif + security-level, object NAT, access-group',
    login: [{ u: '—', p: '—', a: 'консоль без логина; enable — пароль пустой (Enter)' }] };
  function A(st) { return st.ios.kind === 'asa'; }
  function ac(views, pat, run, d) { var e = cmd(views, pat, run, d); e.ok = A; return e; }
  I.T.forEach(function (e) { if (e.p.join(' ') === 'show ip interface brief') e.ok = function (st) { return !A(st); }; });
  function C(st) { return st.ios.c; }
  function top(st) { return I.top(st); }
  function x0(st) { return I.cur(st)[0]; }
  // ---------------------------------------------------------------- интерфейсы
  ac('config', 'interface <if>', function (st, a) { var ports = st.net ? I.dports(st.net, st.net.devs[st.dev]) : []; if (ports.indexOf(a[0]) < 0) return null;
    I.ifc(st, a[0]); I.push(st, { v: 'if', name: a[0] }); }, 'Select an interface to configure');
  ac('if', 'nameif <w>', function (st, a) { var x = x0(st); x.nameif = a[0]; if (x.sec === undefined) { x.secAuto = a[0].toLowerCase() === 'inside' ? 100 : 0;
    return 'INFO: Security level for "' + a[0] + '" set to ' + x.secAuto + ' by default.'; } }, 'Assign name to interface');
  ac('if', 'no nameif', function (st) { delete x0(st).nameif; delete x0(st).secAuto; });
  ac('if', 'security-level <n>', function (st, a) { if (a[0] > 100) return null; x0(st).sec = a[0]; }, 'Specify security level of this interface');
  ac('if', 'ip address dhcp setroute', function (st) { x0(st).dhcpc = true; delete x0(st).ip; });
  ac('if', 'ip address dhcp', function (st) { x0(st).dhcpc = true; delete x0(st).ip; });
  function sec(x) { return x.sec !== undefined ? x.sec : x.secAuto !== undefined ? x.secAuto : 0; }
  function byName(st, n) { var c = C(st); return Object.keys(c.ifs).filter(function (k) { return c.ifs[k].nameif === n; })[0] || null; }
  // ---------------------------------------------------------------- маршруты, NAT, ACL, инспекция, DHCP
  ac('config', 'route <w> <ip> <ip> <ip>', function (st, a) { if (!byName(st, a[0])) return 'ERROR: % Invalid input: interface "' + a[0] + '" not found';
    var l = IP.mask2len(a[2] === '0' ? '0.0.0.0' : a[2]); if (l === null) return null; var c = C(st); (c.routes = c.routes || []).push({ ifn: a[0], net: IP.netOf(a[1] === '0' ? '0.0.0.0' : a[1], l), nh: a[3], ad: 1 }); }, 'Configure a static route for an interface');
  ac('config', 'route <w> <ip> <ip> <ip> <n>', function (st, a) { var l = IP.mask2len(a[2]); if (l === null || !byName(st, a[0])) return null; var c = C(st); (c.routes = c.routes || []).push({ ifn: a[0], net: IP.netOf(a[1], l), nh: a[3], ad: a[4] }); });
  ac('config', 'route <w> 0 0 <ip>', function (st, a) { if (!byName(st, a[0])) return null; var c = C(st); (c.routes = c.routes || []).push({ ifn: a[0], net: '0.0.0.0/0', nh: a[1], ad: 1 }); });
  ac('config', 'no route <w> <rest>', function (st, a) { var c = C(st); c.routes = (c.routes || []).filter(function (r) { return r.ifn !== a[0]; }); });
  function objs(st) { var c = C(st); return c.objs || (c.objs = {}); }
  ac('config', 'object network <w>', function (st, a) { objs(st)[a[0]] = objs(st)[a[0]] || {}; I.push(st, { v: 'obj', obj: a[0] }); }, 'Configure an object');
  function ob(st) { return objs(st)[top(st).obj]; }
  ac('obj', 'host <ip>', function (st, a) { var o = ob(st); o.host = a[0]; delete o.subnet; }, 'Enter this keyword to specify a single host object');
  ac('obj', 'subnet <ip> <ip>', function (st, a) { var l = IP.mask2len(a[1] === '0' ? '0.0.0.0' : a[1]); if (l === null) return null; var o = ob(st); o.subnet = IP.netOf(a[0] === '0' ? '0.0.0.0' : a[0], l); delete o.host; });
  ac('obj', 'subnet 0 0', function (st) { var o = ob(st); o.subnet = '0.0.0.0/0'; delete o.host; });
  ac('obj', 'nat <w> dynamic interface', function (st, a) { var m = a[0].match(/^\((\S+),(\S+)\)$/); if (!m) return null; ob(st).nat = { real: m[1], mapped: m[2], dyn: true }; }, 'Enable NAT on this object');
  ac('obj', 'nat <w> static <ip>', function (st, a) { var m = a[0].match(/^\((\S+),(\S+)\)$/); if (!m) return null; ob(st).nat = { real: m[1], mapped: m[2], st: a[1] }; });
  ac('obj', 'no nat', function (st) { delete ob(st).nat; });
  ac('obj', 'exit', function (st) { st.ios.stack.pop(); });
  ac('obj', 'end', function (st) { st.ios.stack = [{ v: 'priv' }]; });
  function acls(st) { var c = C(st); return c.acls || (c.acls = {}); }
  function addr(st, t, i) {                  // any | host A | object NAME | A MASK
    if (t[i] === 'any' || t[i] === 'any4') return [null, 1, t[i]];
    if (t[i] === 'host' && IP.ip2n(t[i + 1] || '') !== null) return [[t[i + 1], t[i + 1]], 2, 'host ' + t[i + 1]];
    if (t[i] === 'object' && objs(st)[t[i + 1]]) { var o = objs(st)[t[i + 1]]; if (o.host) return [[o.host, o.host], 2, 'object ' + t[i + 1]];
      if (o.subnet) { var p = o.subnet.split('/'), lo = IP.ip2n(p[0]), hi = lo + Math.pow(2, 32 - +p[1]) - 1; return [[p[0], IP.n2ip(hi >>> 0)], 2, 'object ' + t[i + 1]]; } return null; }
    if (IP.ip2n(t[i] || '') !== null && IP.mask2len(t[i + 1] || '') !== null) { var l = IP.mask2len(t[i + 1]), n = IP.netOf(t[i], l).split('/')[0], h = IP.ip2n(n) + Math.pow(2, 32 - l) - 1;
      return [[n, IP.n2ip(h >>> 0)], 2, t[i] + ' ' + t[i + 1]]; }
    return null;
  }
  var PN = { www: 80, http: 80, https: 443, telnet: 23, ftp: 21, ssh: 22, domain: 53, smtp: 25 };
  ac('config', 'access-list <w> extended <rest>', function (st, a) {
    var t = a[1].split(/\s+/).map(function (w, j, all) { return all[j - 1] === 'object' || all[j - 1] === 'object-group' ? w : w.toLowerCase(); }), r = { act: t[0] }, i = 1;   // имена объектов — с учётом регистра if (r.act !== 'permit' && r.act !== 'deny') return null;
    var pr = t[i++]; if (!/^(ip|tcp|udp|icmp)$/.test(pr || '')) return null; r.proto = pr === 'ip' ? 'any' : pr;
    var s = addr(st, t, i); if (!s) return null; r.src = s[0]; i += s[1]; var d = addr(st, t, i); if (!d) return null; r.dst = d[0]; i += d[1];
    if (t[i] === 'eq' && (PN[t[i + 1]] || /^\d+$/.test(t[i + 1] || ''))) { var pv = PN[t[i + 1]] || +t[i + 1]; r.dport = [pv, pv]; i += 2; }
    if (t[i] === 'echo-reply' || t[i] === 'echo') { r.icmpT = t[i]; i++; }
    if (i !== t.length) return null; r.txt = 'extended ' + a[1]; var L = acls(st); (L[a[0]] = L[a[0]] || []).push(r); }, 'Configure an access control element');
  ac('config', 'no access-list <w> <rest>', function (st, a) { var L = acls(st)[a[0]]; if (!L) return null; acls(st)[a[0]] = L.filter(function (r) { return r.txt !== a[1]; }); });
  ac('config', 'clear configure access-list <w>', function (st, a) { delete acls(st)[a[0]]; });
  ac('config', 'access-group <w> in interface <w>', function (st, a) { if (!acls(st)[a[0]] || !byName(st, a[1])) return null; var c = C(st); (c.ag = c.ag || {})[a[1]] = a[0]; }, 'Bind an access-list to an interface');
  ac('config', 'no access-group <w> in interface <w>', function (st, a) { if (C(st).ag) delete C(st).ag[a[1]]; });
  ac('config', 'same-security-traffic permit inter-interface', function (st) { C(st).same = true; });
  ac('config', 'policy-map global_policy', function (st) { I.push(st, { v: 'pmap' }); }, 'Configure MPF Policy Map');
  ac('pmap', 'class inspection_default', function (st) { I.push(st, { v: 'pmapc' }); });
  ac('pmapc', 'inspect icmp', function (st) { C(st).inspIcmp = true; }, 'Configure ICMP Inspection');
  ac('pmapc', 'no inspect icmp', function (st) { delete C(st).inspIcmp; });
  ac('pmapc', 'inspect <w>', function () {});
  ac('pmap pmapc', 'exit', function (st) { st.ios.stack.pop(); });
  ac('pmap pmapc', 'end', function (st) { st.ios.stack = [{ v: 'priv' }]; });
  ac('config', 'dhcpd address <w> <w>', function (st, a) { var m = a[0].match(/^(\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+)$/); if (!m || !byName(st, a[1])) return null;
    var c = C(st); (c.dhcpd = c.dhcpd || {})[a[1]] = Object.assign((c.dhcpd || {})[a[1]] || {}, { range: [m[1], m[2]] }); }, 'Configure DHCP Server');
  ac('config', 'dhcpd enable <w>', function (st, a) { var c = C(st); if (!(c.dhcpd || {})[a[0]]) return 'ERROR: % Address pool not set for interface ' + a[0]; c.dhcpd[a[0]].on = true; });
  ac('config', 'dhcpd dns <ip>', function (st, a) { C(st).dhcpDns = a[0]; });
  ac('exec', 'show interface ip brief', function (st) { var net = st.net, c = C(st), o = ['Interface                  IP-Address      OK? Method Status                Protocol'];
    I.dports(net, net.devs[st.dev]).forEach(function (p) { var x = c.ifs[p] || {}, up = I.phyUp(st, p), sh = !x.noShut;
      o.push(pad(full(p), 27) + pad(x.ip ? x.ip[0] : 'unassigned', 16) + pad('YES', 4) + pad(x.ip ? 'CONFIG' : x.dhcpc ? 'DHCP' : 'unset', 7) + pad(sh ? 'administratively down' : up ? 'up' : 'down', 22) + (!sh && up ? 'up' : 'down')); });
    return o.join('\n'); }, 'Show interface').cfg = false;
  ac('exec', 'show nameif', function (st) { var c = C(st), o = ['Interface                Name                     Security'];
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k]; if (x.nameif) o.push(pad(full(k), 25) + pad(x.nameif, 25) + sec(x)); }); return o.join('\n'); }).cfg = false;
  ac('exec', 'show route', function (st) { return I.showRoute(st).replace(/^Codes:[\s\S]*?\n\n/, 'Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP\n       * - candidate default, U - per-user static route, o - ODR\n\n')
    .replace(/GigabitEthernet\d\/\d+/g, function (m) { var x = C(st).ifs[m.replace('GigabitEthernet', 'gi')]; return x && x.nameif || m; }); }, 'Show routing table').cfg = false;
  ac('exec', 'show xlate', function (st) { var ct = (st.net && st.net.ctLast) || [], L = ct.filter(function (c) { return c.dev === st.dev && c.kind === 's'; }), o = [L.length + ' in use, ' + L.length + ' most used',
    'Flags: D - DNS, i - dynamic, r - portmap, s - static, I - identity, T - twice', '       e - extended'];
    L.forEach(function (c) { o.push((c.proto || 'icmp').toUpperCase() + ' PAT from ' + inName(st, c.orig) + ':' + c.orig + '/0 to ' + inName(st, c.pub) + ':' + c.pub + '/0 flags ri idle 0:00:00 timeout 0:00:30'); });
    return o.join('\n'); }).cfg = false;
  function inName(st, ip) { var c = C(st), k = Object.keys(c.ifs).filter(function (q) { var x = c.ifs[q]; return x.ip && IP.sameNet(ip, x.ip[0], x.ip[1]); })[0]; return k ? c.ifs[k].nameif || k : 'outside'; }
  ac('exec', 'show access-list', function (st) { var L = acls(st);
    return Object.keys(L).map(function (k) { return 'access-list ' + k + '; ' + L[k].length + ' elements\n' + L[k].map(function (r, i) { return 'access-list ' + k + ' line ' + (i + 1) + ' ' + r.txt + ' (hitcnt=0)'; }).join('\n'); }).join('\n'); }).cfg = false;
  ac('exec', 'show nat', function (st) { var O = objs(st), o = ['Auto NAT Policies (Section 2)'], i = 0;
    Object.keys(O).forEach(function (k) { var n = O[k].nat; if (!n) return; i++; o.push(i + ' (' + n.real + ') to (' + n.mapped + ') source ' + (n.dyn ? 'dynamic ' + k + ' interface' : 'static ' + k + ' ' + n.st), '    translate_hits = 0, untranslate_hits = 0'); });
    return o.join('\n'); }).cfg = false;
  ac('config', 'write memory', function (st) { st.ios.saved = EL.clone(st.ios.c); return 'Building configuration...\n[OK]'; }).cfg = false;

  // ---------------------------------------------------------------- compile: ASA → модель ESR (межсетевой экран — своя проверка в fwPass)
  EL.ios.compileAsa = function (st) {
    var c = C(st), run = st.run, net = st.net, d = net && net.devs[st.dev], ports = d ? I.dports(net, d) : [];
    var ifs = {}; Object.keys(run.ifs).forEach(function (k) { if (!/^gi\d/.test(k)) ifs[k] = run.ifs[k]; });
    ports.forEach(function (p) { var x = c.ifs[p] || {}; ifs[p] = { ip: x.ip ? x.ip[0] + '/' + x.ip[1] : null, fw: true, shut: !x.noShut, asaSec: sec(x), asaName: x.nameif || null }; });
    run.ifs = ifs; run.host = c.hostname || 'ciscoasa';
    run.routes = (c.routes || []).map(function (r) { return { net: r.net, nh: r.nh, ad: r.ad || 1 }; });
    run.snat = null; run.dnat = null; run.dhcp = null; run.acls = {};
    Object.keys(objs(st)).forEach(function (k) { var o = objs(st)[k], n = o.nat; if (!n) return; var out = byName(st, n.mapped); if (!out) return;
      var rk = byName(st, n.real), rx = rk && c.ifs[rk], sub = o.subnet === '0.0.0.0/0' && rx && rx.ip ? IP.netOf(rx.ip[0], rx.ip[1]) : o.subnet;   // subnet 0 0 — весь трафик с real-интерфейса (его подсеть)
      var src = o.host ? [o.host, o.host] : sub ? (function () { var p = sub.split('/'), lo = IP.ip2n(p[0]); return [p[0], IP.n2ip((lo + Math.pow(2, 32 - +p[1]) - 1) >>> 0)]; })() : null;
      run.snat = run.snat || { rulesets: {} }; var rs = run.snat.rulesets['asa-' + out] = run.snat.rulesets['asa-' + out] || { ifn: out, rules: {} };
      rs.rules[Object.keys(rs.rules).length + 1] = { on: true, act: 'interface', src: src };
      if (n.st && o.host) { run.dnat = run.dnat || { rulesets: {} }; var ds = run.dnat.rulesets['asa-' + out] = run.dnat.rulesets['asa-' + out] || { ifn: out, rules: {} };
        ds.rules[Object.keys(ds.rules).length + 1] = { on: true, to: o.host, dst: [n.st, n.st] }; } });
    Object.keys(c.dhcpd || {}).forEach(function (nm) { var D = c.dhcpd[nm], k = byName(st, nm), x = k && c.ifs[k]; if (!D.on || !x || !x.ip) return;
      run.dhcp = run.dhcp || { on: true, pools: {} }; run.dhcp.pools[nm] = { net: IP.netOf(x.ip[0], x.ip[1]), range: D.range, gw: x.ip[0], dns: c.dhcpDns || null, lease: null }; });
    st.cand = EL.clone(run);
  };
  // адрес static NAT (nat … static A) тоже принадлежит ASA: на него отвечает ARP с outside
  var if0 = P.ifaces;
  P.ifaces = function (id) { var o = if0.apply(this, arguments), d = this.devs[id]; if (!d || !I.isIos(d) || !A(d.st)) return o;
    var c = d.st.ios.c; Object.keys(c.objs || {}).forEach(function (k) { var n = c.objs[k].nat, out = n && n.st && byName(d.st, n.mapped), f = out && o.filter(function (x) { return x.name === out; })[0];
      if (f && n.st !== f.ip) o.push({ name: out, ip: n.st, len: f.len, port: f.port, tag: f.tag, fw: true, nat: true }); }); return o; };
  // ARP на адрес static NAT: ASA отвечает на него с mapped-интерфейса (proxy ARP) — добавляем конечную точку рядом с основной
  var fl0 = P.flood;
  P.flood = function (id, f) { var res = fl0.apply(this, arguments), s = this, add = [];
    res.eps.forEach(function (e) { var d = s.devs[e.dev]; if (!d || !I.isIos(d) || !A(d.st)) return;
      s.ifaces(e.dev).forEach(function (q) { if (q.nat && q.name === e.iface.name && q.ip !== e.iface.ip && (!f || IP.sameNet(q.ip, f.ip, f.len))) add.push({ dev: e.dev, iface: q, path: e.path }); }); });
    if (add.length) res.eps = res.eps.concat(add);
    return res; };
  // политика ASA: уровни безопасности, ACL на входе, stateful-ответы (ICMP — только с inspect icmp)
  var fw0 = P.fwPass;
  P.fwPass = function (dev, iface, pk, ct, pre) {
    var d = this.devs[dev]; if (!d || !I.isIos(d) || !A(d.st)) return fw0.apply(this, arguments);
    var s = this, c = d.st.ios.c, nm = d.name, inK = String(iface.name).split(':')[0], inX = d.st.run.ifs[inK] || {}, alt = pre || {};
    var est = ct.filter(function (x) { return x.kind === 'fw' && x.dev === dev && x.proto === pk.proto && (x.a.indexOf(pk.dst) >= 0 || x.a.indexOf(alt.dst) >= 0) && (x.b.indexOf(pk.src) >= 0 || x.b.indexOf(alt.src) >= 0); })[0];
    if (est) return { ok: true, t: nm + ': ответ в рамках соединения (' + pk.proto.toUpperCase() + ') — ASA пропускает' };
    if (!inX.asaName) return { ok: false, t: nm + ': на интерфейсе ' + full(inK) + ' не задан nameif — ASA не пропускает трафик' };
    var own = s.ifaces(dev).some(function (f) { return f.ip === pk.dst && !f.nat; });
    if (own) return pk.proto === 'icmp' ? { ok: true } : { ok: false, t: nm + ': доступ к самой ASA (' + pk.proto.toUpperCase() + ') не разрешён (telnet/ssh/http … IF)' };
    var r = s.lookup(dev, pk.dst); if (!r) return { ok: true };
    var outK = String(r.iface.name).split(':')[0], outX = d.st.run.ifs[outK] || {}, acl = (c.ag || {})[inX.asaName], ok, why;
    if (acl) { var hit = (c.acls[acl] || []).filter(function (a) { return (a.proto === 'any' || a.proto === pk.proto) && (!a.src || inR(alt.src || pk.src, a.src) || inR(pk.src, a.src)) &&
        (!a.dst || inR(alt.dst || pk.dst, a.dst) || inR(pk.dst, a.dst)) && (!a.dport || pk.dport === a.dport[0]) && (!a.icmpT || pk.proto === 'icmp' && (a.icmpT === 'echo-reply') === !!pk.reply); })[0];
      ok = !!hit && hit.act === 'permit'; why = 'access-list ' + acl + (hit ? ' — ' + hit.act : ' — неявный deny в конце') + ' на ' + inX.asaName; }
    else if (inX.asaSec > outX.asaSec || inX.asaSec === outX.asaSec && c.same) { ok = true; why = 'уровень ' + inX.asaName + ' (' + inX.asaSec + ') выше ' + (outX.asaName || outK) + ' (' + outX.asaSec + ') — разрешено неявно'; }
    else { ok = false; why = 'с ' + inX.asaName + ' (' + inX.asaSec + ') на ' + (outX.asaName || outK) + ' (' + outX.asaSec + ') без ACL трафик запрещён'; }
    if (!ok) return { ok: false, t: nm + ': ' + why + ' (' + pk.proto.toUpperCase() + ' ' + (alt.src || pk.src) + ' → ' + (alt.dst || pk.dst) + ')' };
    if (pk.proto !== 'icmp' || c.inspIcmp) ct.push({ kind: 'fw', dev: dev, proto: pk.proto, a: [pk.src, alt.src].filter(Boolean), b: [pk.dst, alt.dst].filter(Boolean) });
    return { ok: true, t: nm + ': ' + why + (pk.proto === 'icmp' && !c.inspIcmp ? '; ICMP не инспектируется (нет inspect icmp) — ответ вернётся, только если его разрешает ACL' : '') };
  };
  function inR(ip, r) { var n = IP.ip2n(ip); return n >= IP.ip2n(r[0]) && n <= IP.ip2n(r[1]); }

  // ---------------------------------------------------------------- show running-config
  EL.ios.cfgAsa = function (st, c) {
    var net = st.net, d = net && net.devs[st.dev], o = [': Saved', ':', 'ASA Version 9.6(1)', '!', 'hostname ' + (c.hostname || 'ciscoasa')];
    if (c.secret || c.enpw) o.push('enable password ' + (c.secret || c.enpw) + ' encrypted'); o.push('names', '!');
    (d ? I.dports(net, d) : []).forEach(function (p) { var x = c.ifs[p] || {}; o.push('interface ' + full(p)); if (!x.noShut) o.push(' shutdown');
      if (x.nameif) o.push(' nameif ' + x.nameif); else o.push(' no nameif'); o.push(' security-level ' + sec(x));
      o.push(x.ip ? ' ip address ' + x.ip[0] + ' ' + IP.len2mask(x.ip[1]) : x.dhcpc ? ' ip address dhcp setroute' : ' no ip address'); o.push('!'); });
    if (c.same) o.push('same-security-traffic permit inter-interface');
    Object.keys(c.objs || {}).forEach(function (k) { var b = c.objs[k]; o.push('object network ' + k); if (b.host) o.push(' host ' + b.host); if (b.subnet) o.push(' subnet ' + b.subnet.split('/')[0] + ' ' + IP.len2mask(+b.subnet.split('/')[1])); });
    Object.keys(c.acls || {}).forEach(function (k) { c.acls[k].forEach(function (r) { o.push('access-list ' + k + ' ' + r.txt); }); });
    Object.keys(c.objs || {}).forEach(function (k) { var n = c.objs[k].nat; if (n) o.push('object network ' + k, ' nat (' + n.real + ',' + n.mapped + ') ' + (n.dyn ? 'dynamic interface' : 'static ' + n.st)); });
    Object.keys(c.ag || {}).forEach(function (k) { o.push('access-group ' + c.ag[k] + ' in interface ' + k); });
    (c.routes || []).forEach(function (r) { var p = r.net.split('/'); o.push('route ' + r.ifn + ' ' + p[0] + ' ' + IP.len2mask(+p[1]) + ' ' + r.nh + ' ' + (r.ad || 1)); });
    Object.keys(c.dhcpd || {}).forEach(function (k) { var D = c.dhcpd[k]; if (D.range) o.push('dhcpd address ' + D.range.join('-') + ' ' + k); }); if (c.dhcpDns) o.push('dhcpd dns ' + c.dhcpDns);
    Object.keys(c.dhcpd || {}).forEach(function (k) { if (c.dhcpd[k].on) o.push('dhcpd enable ' + k); });
    o.push('!', 'class-map inspection_default', ' match default-inspection-traffic', '!', 'policy-map global_policy', ' class inspection_default', '  inspect dns', '  inspect ftp', '  inspect tftp');
    if (c.inspIcmp) o.push('  inspect icmp'); o.push('!', 'service-policy global_policy global', ': end');
    return o.join('\n');
  };
})(typeof window !== 'undefined' ? window : global);
