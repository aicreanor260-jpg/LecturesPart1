/* Межсетевой экран Huawei USG6510E (VRP, USG6000E V600R007C20) — спецификация sources/huawei/spec/usg.md (CR/CG/TCE EDOC1100149308).
   Маршрутная часть — как у AR (huawei_ar.js: интерфейсы, статика, OSPF/RIP, DHCP), сверху — по документации:
   зоны local 100 / trust 85 / dmz 50 / untrust 5 (зарезервированы, приоритет не меняется), интерфейс вне зоны не передаёт трафик;
   security-policy — правила rule name сверху вниз, первое совпавшее; условия внутри правила — И, значения одного условия — ИЛИ;
   правило без action не действует; внизу — default (deny, меняется default action); внутризонный трафик default-политикой
   не ограничивается, пока нет default packet-filter intrazone enable; ответы проходят по таблице сессий (TTL tcp 1200, udp 120, icmp 20 с);
   к самому МЭ (зона local) — сначала service-manage входного интерфейса (у управляющего GE0/0/0 по умолчанию разрешены http, https, ping,
   у остальных — ничего), при undo service-manage enable — security-policy с destination-zone local;
   nat-policy — Source NAT (easy-ip, address-group, no-nat), первое совпавшее правило, внизу default no-nat;
   nat server — Destination NAT; политика проверяется по адресам до Source NAT и после nat server (как в TCE).
   Широковещательные пакеты (DHCP DISCOVER) политикой не контролируются (CG). Свой трафик МЭ (ping, tracert с устройства) пропускается.
   Упрощения (в отчёте): address-group транслирует в адрес исходящего интерфейса; nat server без смены порта; time-range хранится,
   но правило с ним действует всегда (в модели нет часов); application, приложения и предопределённые сервисы, кроме перечисленных
   в документации (icmp, telnet, ssh, http, https, ftp, dns), не моделируются; ALG (detect ftp) только сохраняется; USG5500 (policy interzone) не делался. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, Vr = EL.vrp, pad = Vr.pad, full = Vr.full, P = EL.Net.prototype;
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  // порты USG6510E по аппаратному руководству (HWE): GE0/0/0–7, WAN GE0/0/8–9, SFP GE0/0/10–11; GE0/0/0 — inband-управление 192.168.0.1
  EL.MODELS.USG6510E = { type: 'esr', kind: 'hw-ar', usg: true, portList: range('GE0/0/', 0, 11), ports: 12, group: 'Huawei (как в eNSP)', vendor: 'huawei', host: 'FW',
    note: 'Межсетевой экран Huawei USG6510E (USG6000E V600): GE0/0/0–11, зоны trust/untrust/dmz/local, security-policy, nat-policy, nat server; GE0/0/0 — управление 192.168.0.1/24',
    login: [{ u: '—', p: '—', a: 'консоль без пароля (на устройстве при первом входе задают пароль admin)' }] };
  var ZP = { local: 100, trust: 85, dmz: 50, untrust: 5 }, MGMT = 'GE0/0/0';
  function U(st) { return !!st.vrp && !!st.vrp.usg; }
  function uc(views, pat, run, d) { var e = Vr.cmd(views, pat, run, d); e.ok = U; return e; }
  function C(st) { return st.vrp.c; }
  function top(st) { return Vr.top(st); }
  function factory() { var c = { sysname: 'FW', ifs: {}, zones: {}, sp: { rules: [], def: 'deny' }, np: { rules: [] } };
    c.ifs[MGMT] = { ip: ['192.168.0.1', 24] }; return c; }
  function zones(c) { if (!c.zones) c.zones = {}; Object.keys(ZP).forEach(function (z) { c.zones[z] = c.zones[z] || { pr: ZP[z], ifs: [] }; }); return c.zones; }
  function zoneOf(c, n) { var Z = zones(c); return Object.keys(Z).filter(function (z) { return Z[z].ifs.indexOf(n) >= 0; })[0] || null; }
  function zpr(c, z) { var x = zones(c)[z]; return x && x.pr !== undefined ? x.pr : null; }
  var PORTN = { telnet: 23, www: 80, http: 80, https: 443, ftp: 21, ssh: 22, smtp: 25, domain: 53, dns: 53, snmp: 161 };
  function portNum(w) { return /^\d+$/.test(w) ? +w : PORTN[String(w).toLowerCase()] || null; }
  // предопределённые сервисы — только встречающиеся в документации USG (сессии, aging-time, service-manage)
  var PRE = { icmp: [{ proto: 'icmp' }], telnet: [{ proto: 'tcp', dp: [23, 23] }], ssh: [{ proto: 'tcp', dp: [22, 22] }], http: [{ proto: 'tcp', dp: [80, 80] }],
    https: [{ proto: 'tcp', dp: [443, 443] }], ftp: [{ proto: 'tcp', dp: [21, 21] }], dns: [{ proto: 'udp', dp: [53, 53] }] };
  // service protocol tcp|udp|icmp [source-port A [to B]] [destination-port N [to M]]
  function parseSvc(s) { var t = s.toLowerCase().split(/\s+/), r = { proto: t[0] }, i = 1; if (!/^(tcp|udp|icmp)$/.test(r.proto)) return null;
    while (i < t.length) { var k = t[i], f = k === 'source-port' ? 'sp' : k === 'destination-port' ? 'dp' : null; if (!f || !/^\d+$/.test(t[i + 1] || '')) return null;
      var a = +t[i + 1], b = a; i += 2; if (t[i] === 'to' && /^\d+$/.test(t[i + 1] || '')) { b = +t[i + 1]; i += 2; } if (a > b || b > 65535) return null; r[f] = [a, b]; }
    r.txt = 'protocol ' + r.proto + (r.sp ? ' source-port ' + r.sp[0] + (r.sp[1] !== r.sp[0] ? ' to ' + r.sp[1] : '') : '') + (r.dp ? ' destination-port ' + r.dp[0] + (r.dp[1] !== r.dp[0] ? ' to ' + r.dp[1] : '') : '');
    return r; }

  // ---------------------------------------------------------------- зоны
  uc('sys', 'firewall zone <w>', function (st, a) { var z = a[0].toLowerCase(), Z = zones(C(st)); if (!Z[z]) return null; Vr.push(st, { v: 'zone', z: z, tag: 'zone-' + z }); }, 'Configure security zone');
  uc('sys', 'firewall zone name <w>', function (st, a) { var z = a[0]; if (/^(name|vpn-instance)$/i.test(z) || /[?",\-;]/.test(z)) return null; var Z = zones(C(st));
    Z[z] = Z[z] || { ifs: [] }; Vr.push(st, { v: 'zone', z: z, tag: 'zone-' + z }); });
  uc('sys', 'firewall zone name <w> id <n>', function (st, a) { if (a[1] < 4 || a[1] > 254) return null; var Z = zones(C(st)); Z[a[0]] = Z[a[0]] || { ifs: [] }; Z[a[0]].id = a[1];
    Vr.push(st, { v: 'zone', z: a[0], tag: 'zone-' + a[0] }); });
  uc('sys', 'undo firewall zone name <w>', function (st, a) { if (ZP[a[0]] !== undefined) return null; delete zones(C(st))[a[0]]; });
  function zx(st) { return zones(C(st))[top(st).z]; }
  uc('zone', 'add interface <if>', function (st, a) { var z = top(st).z, n = a[0]; if (z === 'local' || /^(LoopBack|NULL)/.test(n)) return null;
    var Z = zones(C(st)); Object.keys(Z).forEach(function (k) { Z[k].ifs = Z[k].ifs.filter(function (q) { return q !== n; }); }); Z[z].ifs.push(n); }, 'Add an interface to the security zone');
  uc('zone', 'undo add interface <if>', function (st, a) { var x = zx(st); x.ifs = x.ifs.filter(function (q) { return q !== a[0]; }); });
  uc('zone', 'set priority <n>', function (st, a) { if (ZP[top(st).z] !== undefined || a[0] < 1 || a[0] > 100) return null; var Z = zones(C(st));
    if (Object.keys(Z).some(function (k) { return k !== top(st).z && Z[k].pr === a[0]; })) return null; zx(st).pr = a[0]; }, 'Set the priority of the security zone');
  uc('zone', 'undo set priority', function (st) { if (ZP[top(st).z] !== undefined) return null; delete zx(st).pr; });
  uc('zone', 'description <rest>', function (st, a) { zx(st).desc = a[0]; });
  uc('zone', 'undo description', function (st) { delete zx(st).desc; });
  uc('sys', 'firewall interzone <w> <w>', function (st, a) { var Z = zones(C(st)); if (!Z[a[0]] || !Z[a[1]] || a[0] === a[1]) return null; var c = C(st), k = a[0] + ' ' + a[1];
    c.iz = c.iz || {}; c.iz[k] = c.iz[k] || []; Vr.push(st, { v: 'iz', k: k, tag: 'interzone-' + a[0] + '-' + a[1] }); }, 'Configure interzone');
  uc('iz', 'detect <w>', function (st, a) { var L = C(st).iz[top(st).k], w = a[0].toLowerCase(); if (L.indexOf(w) < 0) L.push(w); }, 'Detect the application protocol');
  uc('iz', 'undo detect <w>', function (st, a) { var c = C(st); c.iz[top(st).k] = c.iz[top(st).k].filter(function (w) { return w !== a[0].toLowerCase(); }); });

  // ---------------------------------------------------------------- service-manage на интерфейсе
  var SM = ['http', 'https', 'ping', 'ssh', 'snmp', 'netconf', 'telnet'];
  function smOf(n, x) { var o = {}; if (n === MGMT) { o.http = o.https = o.ping = 'permit'; } Object.keys(x.sm || {}).forEach(function (k) { o[k] = x.sm[k]; }); return o; }
  uc('if', 'service-manage <w> <w>', function (st, a) { var p = a[0].toLowerCase(), act = a[1].toLowerCase(); if (SM.indexOf(p) < 0 || ['permit', 'deny'].indexOf(act) < 0) return null;
    Vr.cur(st).forEach(function (x) { x.sm = x.sm || {}; x.sm[p] = act; }); }, 'Configure the service management');
  uc('if', 'service-manage enable', function (st) { Vr.cur(st).forEach(function (x) { delete x.smOff; }); });
  uc('if', 'undo service-manage enable', function (st) { Vr.cur(st).forEach(function (x) { x.smOff = true; }); });

  // ---------------------------------------------------------------- объекты: адреса, сервисы, время
  function objs(st, k) { var c = C(st); return c[k] || (c[k] = {}); }
  uc('sys', 'ip address-set <w> type object', function (st, a) { var O = objs(st, 'as'); O[a[0]] = O[a[0]] || []; Vr.push(st, { v: 'aset', n: a[0], tag: 'object-address-set-' + a[0] }); }, 'Configure an address set');
  uc('sys', 'undo ip address-set <w>', function (st, a) { delete objs(st, 'as')[a[0]]; });
  uc('aset', 'address <ip> mask <mask>', function (st, a) { objs(st, 'as')[top(st).n].push(IP.netOf(a[0], a[1])); }, 'Add an address');
  uc('aset', 'address <n> <ip> mask <mask>', function (st, a) { objs(st, 'as')[top(st).n].push(IP.netOf(a[1], a[2])); });
  uc('sys', 'ip service-set <w> type object', function (st, a) { var O = objs(st, 'ss'); O[a[0]] = O[a[0]] || []; Vr.push(st, { v: 'sset', n: a[0], tag: 'object-service-set-' + a[0] }); }, 'Configure a service set');
  uc('sys', 'undo ip service-set <w>', function (st, a) { delete objs(st, 'ss')[a[0]]; });
  uc('sset', 'service protocol <rest>', function (st, a) { var r = parseSvc(a[0]); if (!r) return null; objs(st, 'ss')[top(st).n].push(r); }, 'Add a service');
  uc('sset', 'service <n> protocol <rest>', function (st, a) { var r = parseSvc(a[1]); if (!r) return null; objs(st, 'ss')[top(st).n].push(r); });
  uc('sys', 'time-range <w>', function (st, a) { var O = objs(st, 'tr'); O[a[0]] = O[a[0]] || []; Vr.push(st, { v: 'trange', n: a[0], tag: 'time-range-' + a[0] }); }, 'Configure a time range');
  uc('sys', 'undo time-range <w>', function (st, a) { delete objs(st, 'tr')[a[0]]; });
  // весь неделя «mon … sun» устройство выводит как daily (итоговый скрипт TCE)
  uc('trange', 'period-range <rest>', function (st, a) { var s = a[0].replace(/\s+mon tue wed thu fri sat sun$/i, ' daily'); objs(st, 'tr')[top(st).n].push(s); }, 'Configure a periodic time range');

  // ---------------------------------------------------------------- security-policy
  function sp(st) { var c = C(st); return c.sp || (c.sp = { rules: [], def: 'deny' }); }
  function ask(st, txt, yes) { st.vrp.ask = { yes: yes }; return txt; }
  uc('sys', 'security-policy', function (st) { sp(st); Vr.push(st, { v: 'secp', tag: 'policy-security' }); }, 'Configure security policy');
  uc('secp', 'default action <w>', function (st, a) { var w = a[0].toLowerCase(), S = sp(st); if (w !== 'permit' && w !== 'deny') return null;
    return ask(st, w === 'permit' ? 'Warning:Setting the default packet filtering to permit poses security risks.\nYou are advised to configure the security policy based on the actual data flows.\nAre you sure you want to continue?[Y/N]'
      : 'Warning: Setting the default interzone packet filtering to deny may affect actual data traffic.\n You are advised to configure the security policy based on the actual services.\n Are you sure you want to continue? [Y/N]',
      function () { S.def = w; Vr.compile(st); return ''; }); }, 'Configure the default action');
  uc('secp', 'default packet-filter intrazone enable', function (st) { sp(st).intra = true; });
  uc('secp', 'undo default packet-filter intrazone enable', function (st) { delete sp(st).intra; });
  function rule(L, name) { return L.rules.filter(function (r) { return r.name === name; })[0]; }
  function newRule(L, name) { var id = L.rules.reduce(function (m, r) { return Math.max(m, r.id); }, 0) + 1, r = { name: name, id: id, sz: [], dz: [], sa: [], da: [], svc: [] }; L.rules.push(r); return r; }
  uc('secp', 'rule name <w>', function (st, a) { if (a[0].length > 32) return null; var S = sp(st); if (!rule(S, a[0])) newRule(S, a[0]);
    Vr.push(st, { v: 'secr', n: a[0], tag: 'policy-security-rule-' + a[0] }); }, 'Configure a security policy rule');
  uc('secp', 'undo rule name <w>', function (st, a) { var S = sp(st); S.rules = S.rules.filter(function (r) { return r.name !== a[0]; }); });
  uc('secp', 'undo rule all', function (st) { sp(st).rules = []; });
  function sr(st) { return rule(sp(st), top(st).n); }
  function zoneList(st, s) { var t = s.split(/\s+/), Z = zones(C(st)); if (t.length > 6 || t.some(function (z) { return z !== 'any' && !Z[z]; })) return null; return t; }
  function addTo(L, v) { if (L.indexOf(v) < 0) L.push(v); }
  function addrArg(st, a) { if (IP.ip2n(a[0]) === null) return null; return IP.netOf(a[0], a[1]); }
  // условия правил безопасности и NAT (общие слова)
  ['secr', 'natr'].forEach(function (v) {
    var R = v === 'secr' ? sr : nr;
    uc(v, 'source-zone <rest>', function (st, a) { var L = zoneList(st, a[0]); if (!L) return null; var r = R(st); L.forEach(function (z) { if (z === 'any') r.sz = []; else addTo(r.sz, z); }); }, 'Source security zone');
    uc(v, 'undo source-zone <rest>', function (st, a) { var r = R(st); r.sz = r.sz.filter(function (z) { return a[0].split(/\s+/).indexOf(z) < 0; }); });
    uc(v, 'source-address <ip> <mask>', function (st, a) { var n = addrArg(st, a); if (!n) return null; addTo(R(st).sa, n); }, 'Source address');
    uc(v, 'source-address address-set <w>', function (st, a) { if (!objs(st, 'as')[a[0]]) return null; addTo(R(st).sa, 'set:' + a[0]); });
    uc(v, 'source-address any', function (st) { R(st).sa = []; });
    uc(v, 'undo source-address <rest>', function (st) { R(st).sa = []; });
    uc(v, 'destination-address <ip> <mask>', function (st, a) { var n = addrArg(st, a); if (!n) return null; addTo(R(st).da, n); }, 'Destination address');
    uc(v, 'destination-address address-set <w>', function (st, a) { if (!objs(st, 'as')[a[0]]) return null; addTo(R(st).da, 'set:' + a[0]); });
    uc(v, 'destination-address any', function (st) { R(st).da = []; });
    uc(v, 'undo destination-address <rest>', function (st) { R(st).da = []; });
    uc(v, 'service <w>', function (st, a) { var w = a[0]; if (!objs(st, 'ss')[w] && !PRE[w.toLowerCase()]) return null; addTo(R(st).svc, objs(st, 'ss')[w] ? w : w.toLowerCase()); }, 'Service');
    uc(v, 'service protocol <rest>', function (st, a) { var s = parseSvc(a[0]); if (!s) return null; R(st).svc.push(s); });
    uc(v, 'undo service <rest>', function (st) { R(st).svc = []; });
  });
  uc('secr', 'destination-zone <rest>', function (st, a) { var L = zoneList(st, a[0]); if (!L) return null; var r = sr(st); L.forEach(function (z) { if (z === 'any') r.dz = []; else addTo(r.dz, z); }); }, 'Destination security zone');
  uc('secr', 'undo destination-zone <rest>', function (st, a) { var r = sr(st); r.dz = r.dz.filter(function (z) { return a[0].split(/\s+/).indexOf(z) < 0; }); });
  uc('secr', 'time-range <w>', function (st, a) { if (!objs(st, 'tr')[a[0]]) return null; sr(st).tr = a[0]; }, 'Time range');
  uc('secr', 'undo time-range', function (st) { delete sr(st).tr; });
  uc('secr', 'action <w>', function (st, a) { var w = a[0].toLowerCase(); if (w !== 'permit' && w !== 'deny') return null; sr(st).act = w; }, 'Action');
  uc('secr', 'undo action', function (st) { delete sr(st).act; });
  uc('secr', 'description <rest>', function (st, a) { sr(st).desc = a[0]; });
  uc('secr', 'enable', function (st) { delete sr(st).off; return 'Info: The policy is enabled successfully.'; }, 'Enable the rule');
  uc('secr', 'disable', function (st) { var r = sr(st); return ask(st, 'Warning: This command will invalidate the rule. Continue?[Y/N]', function () { r.off = true; Vr.compile(st); return 'Info: The policy is disabled successfully.'; }); }, 'Disable the rule');

  // ---------------------------------------------------------------- nat-policy, пулы, nat server
  function np(st) { var c = C(st); return c.np || (c.np = { rules: [] }); }
  function nr(st) { return rule(np(st), top(st).n); }
  uc('sys', 'nat-policy', function (st) { np(st); Vr.push(st, { v: 'natp', tag: 'policy-nat' }); }, 'Configure NAT policy');
  uc('natp', 'rule name <w>', function (st, a) { if (a[0].length > 32) return null; var N = np(st); if (!rule(N, a[0])) newRule(N, a[0]);
    Vr.push(st, { v: 'natr', n: a[0], tag: 'policy-nat-rule-' + a[0] }); }, 'Configure a NAT policy rule');
  uc('natp', 'undo rule name <w>', function (st, a) { var N = np(st); N.rules = N.rules.filter(function (r) { return r.name !== a[0]; }); });
  uc('natp', 'undo rule all', function (st) { np(st).rules = []; });
  // destination-zone и egress-interface взаимоисключаемы: последнее заданное заменяет предыдущее (CR)
  uc('natr', 'destination-zone <w>', function (st, a) { if (!zones(C(st))[a[0]]) return null; var r = nr(st); r.dz = [a[0]]; delete r.egr; }, 'Destination security zone');
  uc('natr', 'egress-interface <if>', function (st, a) { var r = nr(st); r.egr = a[0]; r.dz = []; }, 'Egress interface');
  uc('natr', 'action source-nat easy-ip', function (st) { nr(st).act = { k: 'easy-ip' }; }, 'Action');
  uc('natr', 'action source-nat address-group <w>', function (st, a) { if (!(C(st).ag || {})[a[0]]) return null; nr(st).act = { k: 'address-group', g: a[0] }; });
  uc('natr', 'action no-nat', function (st) { nr(st).act = { k: 'no-nat' }; });
  uc('natr', 'undo action', function (st) { delete nr(st).act; });
  uc('natr', 'enable', function (st) { delete nr(st).off; });
  uc('natr', 'disable', function (st) { nr(st).off = true; });
  function ags(st) { var c = C(st); return c.ag || (c.ag = {}); }
  function agEnter(st, n, id) { var A = ags(st); if (!A[n]) { var used = Object.keys(A).map(function (k) { return A[k].id; }), i = 0; while (used.indexOf(i) >= 0) i++;
    A[n] = { id: id !== undefined ? id : i, mode: 'pat', secs: [] }; } Vr.push(st, { v: 'agrp', n: n, tag: 'address-group-' + n }); }
  uc('sys', 'nat address-group <w>', function (st, a) { agEnter(st, a[0]); }, 'Configure a NAT address pool');
  uc('sys', 'nat address-group <w> <n>', function (st, a) { agEnter(st, a[0], a[1]); });
  uc('sys', 'undo nat address-group <w>', function (st, a) { if (np(st).rules.some(function (r) { return r.act && r.act.g === a[0]; })) return null; delete ags(st)[a[0]]; });
  function ag(st) { return ags(st)[top(st).n]; }
  uc('agrp', 'mode pat', function (st) { ag(st).mode = 'pat'; }, 'Configure the address translation mode');
  uc('agrp', 'mode <w> <w>', function (st, a) { var m = a[0].toLowerCase() + ' ' + a[1].toLowerCase(); if (!/^(no-pat|full-cone) (global|local)$/.test(m)) return null; ag(st).mode = m; });
  uc('agrp', 'section <ip> <ip>', function (st, a) { var g = ag(st); g.secs.push({ id: g.secs.length, a: a[0], b: a[1] }); }, 'Configure an address section');
  uc('agrp', 'section <n> <ip> <ip>', function (st, a) { if (IP.ip2n(a[2]) < IP.ip2n(a[1])) return null; var g = ag(st); g.secs = g.secs.filter(function (s) { return s.id !== a[0]; }).concat([{ id: a[0], a: a[1], b: a[2] }]); });
  uc('agrp', 'route enable', function (st) { ag(st).route = true; });
  function srvs(st) { var c = C(st); return c.srv || (c.srv = []); }
  function srvAdd(st, name, pr, g, gif, gp, ip, ipp, unr) { pr = pr.toLowerCase(); if (['tcp', 'udp'].indexOf(pr) < 0 || !portNum(gp) || !portNum(ipp)) return null;
    var L = srvs(st), id = L.reduce(function (m, s) { return Math.max(m, s.id + 1); }, 0); if (name === null) name = String(id);
    if (L.some(function (s) { return s.name === name; })) return null;
    L.push({ name: name, id: id, pr: pr, g: g, gif: gif, gp: gp, in: ip, ip: ipp, unr: !!unr }); }
  uc('sys', 'nat server <w> protocol <w> global <ip> <w> inside <ip> <w>', function (st, a) { return srvAdd(st, a[0], a[1], a[2], null, a[3], a[4], a[5]); }, 'Configure NAT server');
  uc('sys', 'nat server <w> protocol <w> global <ip> <w> inside <ip> <w> unr-route', function (st, a) { return srvAdd(st, a[0], a[1], a[2], null, a[3], a[4], a[5], true); });
  uc('sys', 'nat server protocol <w> global <ip> <w> inside <ip> <w>', function (st, a) { return srvAdd(st, null, a[0], a[1], null, a[2], a[3], a[4]); });
  uc('sys', 'nat server <w> protocol <w> global interface <if> <w> inside <ip> <w>', function (st, a) { return srvAdd(st, a[0], a[1], null, a[2], a[3], a[4], a[5]); });
  uc('sys', 'undo nat server name <w>', function (st, a) { var c = C(st); c.srv = srvs(st).filter(function (s) { return s.name !== a[0]; }); });
  uc('sys', 'undo nat server all', function (st) { C(st).srv = []; });
  uc('user', 'reset firewall session table', function (st) { return ask(st, 'Warning:Reseting session table will affect the system\'s normal service.\nContinue? [Y/N]:', function () {
    if (st.net && st.net.usgSess) st.net.usgSess[st.dev] = []; return ''; }); }).cfg = false;

  // ---------------------------------------------------------------- compile: поверх AR — межсетевой экран на всех интерфейсах, NAT по политикам
  function srvGlobal(c, s) { if (s.g) return s.g; var x = c.ifs[s.gif]; return x && x.ip ? x.ip[0] : null; }
  var cAr = Vr.compileAr;
  Vr.compileAr = function (st) {
    cAr.apply(this, arguments); if (!U(st)) return;
    var c = C(st), run = st.run; zones(c);
    Object.keys(run.ifs).forEach(function (k) { if (/^(GE|Eth)\d/.test(k) || k.indexOf('.') > 0) run.ifs[k].fw = true; });
    // Source NAT: одно правило на каждом интерфейсе; решение (какое правило nat-policy) принимает fwPass для конкретного пакета
    run.snat = { rulesets: {} }; run.dnat = null;
    Object.keys(run.ifs).forEach(function (k) { if (run.ifs[k].fw) run.snat.rulesets['usg-' + k] = { ifn: k, rules: { 1: { on: true, act: 'interface', srcOg: '\u0001usg' } } }; });
    var L = srvs(st).filter(function (s) { return srvGlobal(c, s); });
    if (L.length) { run.dnat = { rulesets: {} };
      Object.keys(run.ifs).forEach(function (k) { if (!run.ifs[k].fw) return; var rs = {}; L.forEach(function (s, i) { var g = srvGlobal(c, s);
          rs[i + 1] = { on: true, to: s.in, dst: [g, g], proto: s.pr, dport: [portNum(s.gp), portNum(s.gp)] }; });
        run.dnat.rulesets['usg-' + k] = { ifn: k, rules: rs }; }); }
    st.cand = EL.clone(run);
  };
  var og0 = EL.ogNet;
  EL.ogNet = function (c, name, ip) { if (name !== '\u0001usg') return og0.apply(this, arguments); var d = c && c._usgNat; if (!d || d.src !== ip) return false; c._usgNat = null; return true; };
  // внешний адрес nat server (если это не адрес интерфейса) — МЭ отвечает на ARP за него на интерфейсе той же сети
  var if0 = P.ifaces;
  P.ifaces = function (id) { var o = if0.apply(this, arguments), d = this.devs[id]; if (!d || !d.st.vrp || !d.st.vrp.usg) return o;
    var c = d.st.vrp.c; (c.srv || []).forEach(function (s) { if (!s.g || o.some(function (f) { return f.ip === s.g; })) return;
      var f = o.filter(function (q) { return !q.nat && IP.sameNet(s.g, q.ip, q.len) && /^GE/.test(q.name); })[0]; if (f) o.push({ name: f.name, ip: s.g, len: f.len, port: f.port, tag: f.tag, fw: true, nat: true }); }); return o; };
  var fl0 = P.flood;
  P.flood = function (id, f) { var res = fl0.apply(this, arguments), s = this, add = [];
    res.eps.forEach(function (e) { var d = s.devs[e.dev]; if (!d || !d.st.vrp || !d.st.vrp.usg) return;
      s.ifaces(e.dev).forEach(function (q) { if (q.nat && q.name === e.iface.name && q.ip !== e.iface.ip && (!f || IP.sameNet(q.ip, f.ip, f.len))) add.push({ dev: e.dev, iface: q, path: e.path }); }); });
    if (add.length) res.eps = res.eps.concat(add);
    return res; };

  // ---------------------------------------------------------------- политика: зоны, правила, сессии, service-manage
  function inNet(ip, n) { var p = n.split('/'); return IP.sameNet(ip, p[0], +p[1]); }
  function addrHit(c, L, ip) { return !L.length || L.some(function (a) { return a.indexOf('set:') === 0 ? ((c.as || {})[a.slice(4)] || []).some(function (n) { return inNet(ip, n); }) : inNet(ip, a); }); }
  function svcOne(s, pk) { return s.proto === pk.proto && (!s.dp || pk.dport >= s.dp[0] && pk.dport <= s.dp[1]) && (!s.sp || !pk.sport || pk.sport >= s.sp[0] && pk.sport <= s.sp[1]); }
  function svcHit(c, L, pk) { return !L.length || L.some(function (s) { var items = typeof s === 'string' ? (c.ss || {})[s] || PRE[s] || [] : [s]; return items.some(function (x) { return svcOne(x, pk); }); }); }
  function ruleOk(c, r, zin, zout, src, dst, pk) { return !r.off && (!r.sz.length || r.sz.indexOf(zin) >= 0) && (!r.dz.length || r.dz.indexOf(zout) >= 0) &&
    addrHit(c, r.sa, src) && addrHit(c, r.da, dst) && svcHit(c, r.svc, pk); }
  function pkTxt(pk, src, dst) { return (pk.proto === 'icmp' ? 'ICMP' : pk.proto.toUpperCase() + (pk.dport ? ':' + pk.dport : '')) + ' ' + src + ' → ' + dst; }
  var SMP = { 23: 'telnet', 22: 'ssh', 80: 'http', 443: 'https', 8443: 'https', 830: 'netconf' };
  function smProto(pk) { return pk.proto === 'icmp' ? 'ping' : pk.proto === 'tcp' ? SMP[pk.dport] || null : pk.proto === 'udp' && pk.dport === 161 ? 'snmp' : null; }
  var TTL = { tcp: 1200, udp: 120, icmp: 20 };
  function hit(s, dev, k, name) { var H = (s.usgHits = s.usgHits || {})[dev] || (s.usgHits[dev] = {}); H[k + name] = (H[k + name] || 0) + 1; }
  var fw0 = P.fwPass;
  P.fwPass = function (dev, iface, pk, ct, pre) {
    var d = this.devs[dev]; if (!d || !d.st.vrp || !d.st.vrp.usg) return fw0.apply(this, arguments);
    var s = this, c = d.st.vrp.c, run = d.st.run, nm = d.name, alt = pre || {}, inK = String(iface.name).split(':')[0], src = pk.src, dst = pk.dst;
    run._usgNat = null;
    var est = ct.filter(function (x) { return x.kind === 'fw' && x.dev === dev && x.proto === pk.proto && (x.a.indexOf(pk.dst) >= 0 || x.a.indexOf(alt.dst) >= 0) && (x.b.indexOf(pk.src) >= 0 || x.b.indexOf(alt.src) >= 0); })[0];
    if (est) return { ok: true, t: est.self ? null : nm + ': ответ по таблице сессий (' + pk.proto.toUpperCase() + ') — security-policy не проверяется' };
    if (pk.src === '0.0.0.0') return { ok: true };                    // широковещательный DHCP DISCOVER политикой не контролируется
    var zin = zoneOf(c, (st0(d).sub || {})[inK] || inK);
    if (!zin) return { ok: false, t: nm + ': интерфейс ' + full((st0(d).sub || {})[inK] || inK) + ' не добавлен ни в одну зону (firewall zone … add interface) — пакет отброшен' };
    var own = s.ifaces(dev).some(function (f) { return f.ip === pk.dst && !f.nat; }), zout = 'local', r = null;
    if (own) {
      var hn = (st0(d).sub || {})[inK] || inK, x = c.ifs[hn] || {}, sp0 = smProto(pk);
      if (!x.smOff && sp0) { var allow = smOf(hn, x)[sp0] === 'permit';
        return allow ? { ok: true, t: nm + ': service-manage ' + sp0 + ' permit на ' + full(hn) + ' — доступ к устройству разрешён (security-policy не проверяется)' }
          : { ok: false, t: nm + ': к самому МЭ по ' + sp0 + ' через ' + full(hn) + ' — service-manage не разрешает (service-manage ' + sp0 + ' permit) — пакет отброшен' }; }
    } else {
      r = s.lookup(dev, pk.dst); if (!r) return { ok: true };
      var oK = String(r.iface.name).split(':')[0]; zout = zoneOf(c, (st0(d).sub || {})[oK] || oK);
      if (!zout) return { ok: false, t: nm + ': выходной интерфейс ' + full((st0(d).sub || {})[oK] || oK) + ' не в зоне безопасности — пакет отброшен' };
    }
    var S = c.sp || { rules: [], def: 'deny' }, m = S.rules.filter(function (q) { return q.act && ruleOk(c, q, zin, zout, src, dst, pk); })[0], act, why;
    if (m) { act = m.act; why = 'security-policy rule ' + m.name + ' — ' + act; hit(s, dev, 's:', m.name); }
    else if (zin === zout && !S.intra) { act = 'permit'; why = 'трафик внутри зоны ' + zin + ' — по умолчанию разрешён (default packet-filter intrazone не включён)'; }
    else { act = S.def; why = 'ни одно правило не подошло — default ' + act + ' (' + zin + ' → ' + zout + ')'; hit(s, dev, 's:', 'default'); }
    if (act !== 'permit') return { ok: false, t: nm + ': ' + why + ' (' + pkTxt(pk, src, dst) + ')' };
    // Source NAT: первое подходящее правило nat-policy (по зонам или egress-interface и адресам до трансляции)
    var nt = '', pub = null;
    if (r && !own) { var oK2 = String(r.iface.name).split(':')[0], oh = (st0(d).sub || {})[oK2] || oK2;
      var nrl = ((c.np || {}).rules || []).filter(function (q) { return q.act && !q.off && (!q.sz.length || q.sz.indexOf(zin) >= 0) && (q.egr ? q.egr === oh : !q.dz.length || q.dz.indexOf(zout) >= 0) &&
        addrHit(c, q.sa, src) && addrHit(c, q.da, dst) && svcHit(c, q.svc, pk); })[0];
      if (nrl) { hit(s, dev, 'n:', nrl.name); if (nrl.act.k !== 'no-nat') { run._usgNat = { src: pk.src }; pub = r.iface.ip; } nt = '; nat-policy rule ' + nrl.name + ' — ' + (nrl.act.k === 'no-nat' ? 'no-nat' : 'source-nat ' + nrl.act.k + (nrl.act.g ? ' ' + nrl.act.g : '')); } }
    var L = (s.usgSess = s.usgSess || {})[dev] || (s.usgSess[dev] = []);
    L.push({ proto: pk.proto, src: alt.src || src, dst: alt.dst || dst, sport: pk.sport, dport: pk.dport, pub: pub, zin: zin, zout: zout, pol: m ? m.name : 'default', t: s.now || 0, ifn: r ? r.iface.name : inK, nh: r ? r.nh || pk.dst : null });
    if (L.length > 50) L.shift();
    ct.push({ kind: 'fw', dev: dev, proto: pk.proto, a: [pk.src, alt.src].filter(Boolean), b: [pk.dst, alt.dst].filter(Boolean) });
    return { ok: true, t: nm + ': ' + zin + ' → ' + zout + ', ' + why + ' (' + pkTxt(pk, src, dst) + '), создана сессия (TTL ' + TTL[pk.proto] + ' с)' + nt };
  };
  function st0(d) { return d.st.vrp; }
  function live(net, dev) { var now = net.now || 0; return ((net.usgSess || {})[dev] || []).filter(function (x) { return now - x.t < (TTL[x.proto] || 20); }); }

  // ---------------------------------------------------------------- display
  function hits(st, k, n) { return (((st.net && st.net.usgHits) || {})[st.dev] || {})[k + n] || 0; }
  function zoneOrder(c) { var Z = zones(c); return ['local', 'trust', 'untrust', 'dmz'].concat(Object.keys(Z).filter(function (z) { return ZP[z] === undefined; })); }
  function zoneTxt(c, z, part) { var x = zones(c)[z], o = [z]; if (part !== 'interface') o.push(x.pr !== undefined ? ' priority is ' + x.pr : ' priority is not set');
    if (part !== 'priority') { o.push(' interface of the zone is (' + x.ifs.length + '):'); x.ifs.forEach(function (n) { o.push('    ' + full(n)); }); } o.push('#'); return o.join('\n'); }
  uc('*', 'display zone', function (st) { var c = C(st); return zoneOrder(c).map(function (z) { return zoneTxt(c, z); }).join('\n'); }, 'Display security zone').cfg = false;
  uc('*', 'display zone <w>', function (st, a) { if (!zones(C(st))[a[0]]) return null; return zoneTxt(C(st), a[0]); }).cfg = false;
  uc('*', 'display zone <w> interface', function (st, a) { if (!zones(C(st))[a[0]]) return null; return zoneTxt(C(st), a[0], 'interface'); }).cfg = false;
  uc('*', 'display zone <w> priority', function (st, a) { if (!zones(C(st))[a[0]]) return null; return zoneTxt(C(st), a[0], 'priority'); }).cfg = false;
  function izTxt(c, k) { return ['interzone ' + k].concat((c.iz[k] || []).map(function (w) { return ' detect ' + w; }), ['#']).join('\n'); }
  uc('*', 'display interzone', function (st) { var c = C(st); return Object.keys(c.iz || {}).map(function (k) { return izTxt(c, k); }).join('\n'); }, 'Display interzone').cfg = false;
  uc('*', 'display interzone <w> <w>', function (st, a) { var c = C(st), k = a[0] + ' ' + a[1]; if (!(c.iz || {})[k]) return null; return izTxt(c, k); }).cfg = false;
  function svcTxt(s) { return typeof s === 'string' ? s : s.txt; }
  function addrTxt(a) { return a.indexOf('set:') === 0 ? 'address-set ' + a.slice(4) : a.replace('/', ' '); }
  function ruleLines(r, i1, i2, nat) { var o = [i1 + 'rule name ' + r.name];
    if (r.desc) o.push(i2 + 'description ' + r.desc); if (r.sz.length) o.push(i2 + 'source-zone ' + r.sz.join(' ')); r.dz.forEach(function (z) { o.push(i2 + 'destination-zone ' + z); });
    if (r.egr) o.push(i2 + 'egress-interface ' + full(r.egr));
    r.sa.forEach(function (a) { o.push(i2 + 'source-address ' + addrTxt(a)); }); r.da.forEach(function (a) { o.push(i2 + 'destination-address ' + addrTxt(a)); });
    r.svc.forEach(function (s) { o.push(i2 + 'service ' + svcTxt(s)); }); if (r.tr) o.push(i2 + 'time-range ' + r.tr);
    if (r.off) o.push(i2 + 'disable');
    if (r.act) o.push(i2 + 'action ' + (nat ? (r.act.k === 'no-nat' ? 'no-nat' : 'source-nat ' + r.act.k + (r.act.g ? ' ' + r.act.g : '')) : r.act));
    return o; }
  function spTable(st, L) { var S = sp(st), o = ['RULE ID RULE NAME                      STATE      ACTION     HITS', new Array(80).join('-')];
    L.forEach(function (r) { o.push(pad(r.id, 8) + pad(r.name, 31) + pad(r.off ? 'disable' : 'enable', 11) + pad(r.act || '-', 11) + hits(st, 's:', r.name)); });
    o.push(pad(0, 8) + pad('default', 31) + pad('enable', 11) + pad(S.def, 11) + hits(st, 's:', 'default'), new Array(80).join('-')); return o.join('\n'); }
  uc('*', 'display security-policy rule all', function (st) { return spTable(st, sp(st).rules); }, 'Display security policy').cfg = false;
  uc('*', 'display security-policy rule name <w>', function (st, a) { var r = rule(sp(st), a[0]); if (!r) return null;
    return ['  (' + hits(st, 's:', r.name) + ' times matched)'].concat(ruleLines(r, '  ', '  ').map(function (l) { return /^ {2}action/.test(l) ? '  ' + l : l; })).join('\n'); }).cfg = false;
  uc('*', 'display security-policy rule all | include <rest>', function (st, a) { var w = a[0];
    return sp(st).rules.filter(function (r) { return ruleLines(r, '', ' ').join('\n').indexOf(w) >= 0; }).map(function (r) { return ruleLines(r, '', ' ').join('\n'); }).join('\n'); }).cfg = false;
  uc('*', 'display security-policy rule verbose <rest>', function (st, a) { var t = a[0].split(/\s+/), S = sp(st);
    var L = S.rules.filter(function (r) { for (var i = 0; i + 1 < t.length; i += 2) { var k = t[i], v = t[i + 1];
      if (k === 'source-zone' && r.sz.indexOf(v) < 0) return false; if (k === 'destination-zone' && r.dz.indexOf(v) < 0) return false; } return true; });
    return L.map(function (r) { return [' (' + hits(st, 's:', r.name) + ' times matched)'].concat(ruleLines(r, ' ', '  ')).join('\n'); }).join('\n'); }).cfg = false;
  uc('*', 'display nat-policy rule all', function (st) { var L = np(st).rules, o = ['Total:' + (L.length + 1), 'RULE ID  RULE NAME                  STATE        ACTION       HITS',
      new Array(72).join('-')], row = function (id, n, s2, a, h) { o.push(pad(id, 9) + pad(n, 27) + pad(s2, 13) + pad(a, 13) + ('    ' + h).slice(-4)); };
    L.forEach(function (r) { row(r.id, r.name, r.off ? 'disable' : 'enable', !r.act ? '-' : r.act.k === 'no-nat' ? 'no-nat' : 'source-nat', hits(st, 'n:', r.name)); });
    row(0, 'default', 'enable', 'no-nat', 0); o.push(new Array(71).join('-')); return o.join('\n'); }, 'Display NAT policy').cfg = false;
  uc('*', 'display nat-policy rule name <w>', function (st, a) { var r = rule(np(st), a[0]); if (!r) return null;
    return ['  (' + hits(st, 'n:', r.name) + ' times matched)'].concat(ruleLines(r, '  ', '    ', true)).join('\n'); }).cfg = false;
  uc('*', 'display nat address-group', function (st) { var A = ags(st), K = Object.keys(A), L = np(st).rules, o = ['NAT address-group information:', '  Total ' + K.length + ' address-group(s)'];
    K.forEach(function (k) { var g = A[k]; o.push('nat address-group ' + k + ' ' + g.id, ' reference count: ' + L.filter(function (r) { return r.act && r.act.g === k; }).length, ' mode ' + g.mode, ' status active');
      g.secs.forEach(function (s) { o.push(' section ' + s.id + ' ' + s.a + ' ' + s.b); }); });
    return o.join('\n'); }, 'Display NAT address group').cfg = false;
  var PNAME = { 80: 'www', 21: 'ftp', 23: 'telnet', 22: 'ssh', 25: 'smtp', 53: 'domain' };
  uc('*', 'display nat server', function (st) { var c = C(st), L = srvs(st), o = ['Server in private network information:', '  Total   ' + L.length + ' NAT server(s)'];
    L.forEach(function (s) { var g = srvGlobal(c, s) || '---', gp = portNum(s.gp), ip = portNum(s.ip), r2 = function (a, b) { o.push(' ' + pad(a, 23) + b); };
      o.push(' server name   : ' + s.name); r2('id            : ' + s.id, 'zone          : ---');
      r2('global-start-addr : ' + g, 'global-end-addr   : ' + g); r2('inside-start-addr : ' + s.in, 'inside-end-addr   : ' + s.in);
      r2('global-start-port : ' + gp + (PNAME[gp] && !/^\d+$/.test(s.gp) ? '(' + PNAME[gp] + ')' : ''), 'global-end-port   : ' + gp);
      r2('inside-start-port : ' + ip + (PNAME[ip] ? '(' + PNAME[ip] + ')' : ''), 'inside-end-port   : ' + ip);
      r2('globalvpn     : public', 'insidevpn     : public'); r2('vsys          : public', 'protocol      : ' + s.pr); r2('vrrp          : ---', 'no-revers     : 0');
      r2('interface     : ' + (s.gif ? full(s.gif) : '---'), 'vrrp-bind-interface: ---'); r2('unr-route     :' + (s.unr ? 1 : 0), 'description   : ---'); o.push(' nat-disable   :0'); });
    return o.join('\n'); }, 'Display NAT server').cfg = false;
  var APPN = { 23: 'telnet', 80: 'http', 21: 'ftp', 22: 'ssh', 53: 'dns', 443: 'https' };
  function sessName(x) { return x.proto === 'icmp' ? 'icmp' : APPN[x.dport] || x.proto; }
  function sport(x, i) { return x.sport || 43985 + i; }
  function dport(x) { return x.proto === 'icmp' ? 2048 : x.dport; }
  function hms(t) { t = Math.max(0, Math.floor(t)); return ('0' + Math.floor(t / 3600)).slice(-2) + ':' + ('0' + Math.floor(t / 60) % 60).slice(-2) + ':' + ('0' + t % 60).slice(-2); }
  uc('*', 'display firewall session table', function (st) { var L = st.net ? live(st.net, st.dev) : [], o = [' Current Total Sessions : ' + L.length];
    L.forEach(function (x, i) { o.push('  ' + sessName(x) + '  VPN:public --> public ' + x.src + ':' + sport(x, i) + (x.pub ? '[' + x.pub + ':' + (2048 + i) + ']' : '') + '-->' + x.dst + ':' + dport(x)); });
    return o.join('\n'); }, 'Display session table').cfg = false;
  uc('*', 'display firewall session table verbose', function (st) { var net = st.net, L = net ? live(net, st.dev) : [], o = [' Current Total Sessions : ' + L.length];
    L.forEach(function (x, i) { var ttl = TTL[x.proto] || 20;
      o.push(' ' + sessName(x) + '  VPN: public --> public', ' Zone: ' + x.zin + ' --> ' + x.zout + '  TTL: ' + hms(ttl) + '  Left: ' + hms(ttl - ((net.now || 0) - x.t)),
        ' Interface: ' + full(String(x.ifn).split(':')[0]) + '  NextHop: ' + (x.nh || '---'),
        ' ' + x.src + ':' + sport(x, i) + (x.pub ? '[' + x.pub + ':' + (2048 + i) + ']' : '') + ' --> ' + x.dst + ':' + dport(x) + ' PolicyName: ' + x.pol); });
    return o.join('\n'); }).cfg = false;
  uc('*', 'display firewall session aging-time', function () {
    return ['Sequence  Pre-defined                        Default-Time(s)    Timeout(s)', new Array(75).join('-')].concat([['tcp', 1200], ['udp', 120], ['icmp', 20], ['fin-rst', 10], ['first-fin', 900],
      ['fragment', 5], ['syn', 5], ['http', 1200], ['dns', 30], ['ftp', 1200]].map(function (r, i) { var t = ('     ' + r[1]).slice(-4) + ' (s)';
      return pad(i + 1, 12) + pad(r[0], 33) + '   ' + t + '      ' + t; })).join('\n'); }).cfg = false;

  // ---------------------------------------------------------------- display current-configuration (части USG)
  var rAr = Vr.renderAr;
  Vr.renderAr = function (st) {
    var out = rAr.apply(this, arguments); if (!U(st)) return out;
    var c = C(st);
    out.forEach(function (p) { var m = p.h.match(/^interface (\S+)$/); if (!m) return; var k = Vr.norm('interface ' + m[1])[1], x = c.ifs[k]; if (!x) return;
      Object.keys(x.sm || {}).forEach(function (w) { p.L.push(' service-manage ' + w + ' ' + x.sm[w]); }); if (x.smOff) p.L.push(' undo service-manage enable'); });
    var ri = out.map(function (p) { return p.h; }).indexOf('route'), add = [];
    zoneOrder(c).forEach(function (z) { var x = zones(c)[z]; if (z !== 'local' && !x.ifs.length && ZP[z] !== undefined) return;
      add.push({ h: 'zone', L: ['firewall zone ' + (ZP[z] === undefined ? 'name ' + z + (x.id ? ' id ' + x.id : '') : z)].concat(x.pr !== undefined ? [' set priority ' + x.pr] : [], x.desc ? [' description ' + x.desc] : [],
        x.ifs.map(function (n) { return ' add interface ' + full(n); })) }); });
    Object.keys(c.iz || {}).forEach(function (k) { add.push({ h: 'interzone', L: ['firewall interzone ' + k].concat(c.iz[k].map(function (w) { return ' detect ' + w; })) }); });
    out.splice.apply(out, [ri < 0 ? out.length : ri, 0].concat(add));
    Object.keys(c.as || {}).forEach(function (k) { out.push({ h: 'aset', L: ['ip address-set ' + k + ' type object'].concat(c.as[k].map(function (n, i) { return ' address ' + i + ' ' + n.split('/')[0] + ' mask ' + n.split('/')[1]; })) }); });
    Object.keys(c.ss || {}).forEach(function (k) { out.push({ h: 'sset', L: ['ip service-set ' + k + ' type object'].concat(c.ss[k].map(function (s, i) { return ' service ' + i + ' ' + s.txt; })) }); });
    Object.keys(c.tr || {}).forEach(function (k) { out.push({ h: 'trange', L: ['time-range ' + k].concat(c.tr[k].map(function (s) { return ' period-range ' + s; })) }); });
    Object.keys(c.ag || {}).forEach(function (k) { var g = c.ag[k]; out.push({ h: 'agrp', L: ['nat address-group ' + k + ' ' + g.id, ' mode ' + g.mode].concat(g.route ? [' route enable'] : [],
      g.secs.map(function (s) { return ' section ' + s.id + ' ' + s.a + ' ' + s.b; })) }); });
    if ((c.srv || []).length) out.push({ h: 'nat server', L: c.srv.map(function (s) { return ' nat server ' + s.name + ' protocol ' + s.pr + ' global ' + (s.gif ? 'interface ' + full(s.gif) : s.g) + ' ' + s.gp + ' inside ' + s.in + ' ' + s.ip + (s.unr ? ' unr-route' : ''); }) });
    var S = sp(st); out.push({ h: 'security-policy', L: ['security-policy'].concat(S.def !== 'deny' ? [' default action ' + S.def] : [], S.intra ? [' default packet-filter intrazone enable'] : [],
      [].concat.apply([], S.rules.map(function (r) { return ruleLines(r, ' ', '  '); }))) });
    var N = np(st); if (N.rules.length) out.push({ h: 'nat-policy', L: ['nat-policy'].concat([].concat.apply([], N.rules.map(function (r) { return ruleLines(r, ' ', '  ', true); }))) });
    return out;
  };

  // ---------------------------------------------------------------- устройство: заводская конфигурация (GE0/0/0 192.168.0.1/24, sysname FW)
  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}; if (!m.usg) return d;
    var x = d.st.vrp; x.usg = true; x.c = factory(); Vr.compile(d.st); return d; };
  var rb0 = P.reboot;
  P.reboot = function (id) { var r = rb0.apply(this, arguments), d = this.devs[id]; if (d && d.st.vrp && d.st.vrp.usg) { if (!d.st.vrp.saved) d.st.vrp.c = factory(); Vr.compile(d.st); } return r; };
  // одноимённые команды AR (display nat server и др.) на USG уступают командам USG
  var mine = Vr.T.filter(function (e) { return e.ok === U; }).map(function (e) { return e.v.join(' ') + '|' + e.p.join(' '); });
  Vr.T.forEach(function (e) { if (e.ok === U || mine.indexOf(e.v.join(' ') + '|' + e.p.join(' ')) < 0) return; var ok0 = e.ok; e.ok = function (st) { return !U(st) && (!ok0 || ok0(st)); }; });
  EL.usg = { zoneOf: zoneOf, factory: factory };
})(typeof window !== 'undefined' ? window : global);
