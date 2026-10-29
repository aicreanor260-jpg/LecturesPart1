/* WLAN Huawei: контроллер AC6005 и точки доступа Fit AP (AP5030DN, AP2050DN) — спецификация sources/huawei/spec/wlan.md
   (V200R010C00: TCE EDOC1100064368, CR EDOC1100064351, CG EDOC1100064365; HCIA-LG гл. 6, 9).
   wlc.js Eltex не переиспользуется: там CLI ESR и своя модель (SoftGRE, опция 43/15, ap-location); общие здесь только приёмы —
   точка доступа как конечный узел с портом LAN (тип 'deb', как WEP), адрес по DHCP вместе с опциями пула, обнаружение контроллера по запросу из сети.
   AC — коммутатор VRP (тип 'mes', huawei_s.js: VLAN, trunk, Vlanif) плюс DHCP-сервер (команды AR: dhcp enable, ip pool, dhcp select)
   и вид wlan. Как AP выходит в сеть (CG j0cz): адрес по DHCP → поиск AC: опция 43 sub-option 3 (адрес AC) или broadcast в своей подсети →
   AC отвечает, только если задан capwap source interface (адрес этого интерфейса) → допуск по ap auth-mode (mac-auth по умолчанию: AP добавлена
   ap-id … ap-mac … или в белом списке; no-auth — любая; иначе — в списке неавторизованных до ap-confirm) → normal.
   VAP на радио AP создаётся, если к её группе привязан vap-profile (display vap: Status ON). Группа по умолчанию — default.
   Тексты Info/Warning — по TCE/CR V200R010C00 (строки HCIA-LG V200R019 вроде «SSID profile … is created.» не выводятся).
   Упрощения (в отчёте): CAPWAP (UDP 5246/5247) проверяется ICMP-доступностью адреса AC; состояния download/config сжаты — сразу normal;
   клиентов Wi-Fi (STA) в модели нет — display station пуст; forward-mode, service-vlan, радио (channel, eirp) и vlan pool только хранятся;
   sn-auth: серийных номеров у AP в модели нет — такие AP остаются неавторизованными; число портов AC6005 в источниках нет — взято 8 (GE0/0/1–8);
   CLI самой Fit AP в источниках нет — консоль AP молчит; пароль pass-phrase в конфигурации показан условной шифровкой %^%#…%^%#. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, Vr = EL.vrp, pad = Vr.pad, full = Vr.full, P = EL.Net.prototype;
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  EL.MODELS.AC6005 = { type: 'mes', kind: 'hw-s', ac: true, portList: range('GE0/0/', 1, 8), ports: 8, group: 'Huawei (как в eNSP)', vendor: 'huawei', host: 'AC6005',
    note: 'Контроллер WLAN Huawei AC6005 (V200R010): VLAN/trunk/Vlanif, DHCP для AP, вид wlan — группы AP, профили SSID/безопасности/VAP, допуск Fit AP',
    login: [{ u: '—', p: '—', a: 'консоль без пароля (на устройстве при первом входе задают пароль)' }] };
  // type-id — по таблице display ap-type all V200R010C00 (CR j1m7); радио AP5030DN — 2 (TCE j01x), у AP2050DN число в источниках нет — взято 2
  [['AP5030DN', 35], ['AP2050DN', 69]].forEach(function (x) { EL.MODELS[x[0]] = { type: 'deb', kind: 'hwap', typeId: x[1], radios: 2, ports: 1, portList: ['LAN'], group: 'Huawei (как в eNSP)', vendor: 'huawei',
    note: 'Точка доступа Huawei ' + x[0] + ' (Fit AP): адрес по DHCP, находит AC (broadcast или опция 43), настраивается с AC · порт LAN (имя условное)',
    login: [{ u: 'admin', p: '—', a: 'пользователь по умолчанию admin (display ap username); пароль — в закрытом документе Huawei' }] }; });
  function AC(st) { return !!st.vrp && !!st.vrp.ac; }
  function isAp(d) { return !!d && d.sub === 'hwap'; }
  function wc(views, pat, run, d) { var e = Vr.cmd(views, pat, run, d); e.ok = AC; return e; }
  function C(st) { return st.vrp.c; }
  function top(st) { return Vr.top(st); }
  function ask(st, txt, yes) { st.vrp.ask = { yes: yes }; return txt; }
  function hwMac(m) { var h = String(m).replace(/[^0-9a-f]/gi, '').toLowerCase(); return h.length === 12 ? h.slice(0, 4) + '-' + h.slice(4, 8) + '-' + h.slice(8) : null; }
  function macArg(w) { var m = String(w).toLowerCase().match(/^([0-9a-f]{1,4})-([0-9a-f]{1,4})-([0-9a-f]{1,4})$/); if (!m) return null;
    return m.slice(1).map(function (x) { return ('000' + x).slice(-4); }).join('-'); }
  function apMac(d) { return hwMac(EL.mac(EL.macKey(d) + 'LAN')); }

  // ---------------------------------------------------------------- DHCP на AC: команды AR (dhcp enable, ip pool, dhcp select) доступны и контроллеру
  var DH = ['dhcp enable', 'undo dhcp enable', 'ip pool <w>', 'undo ip pool <w>', 'dhcp select <w>', 'undo dhcp select <w>', 'dhcp server dns-list <rest>'];
  Vr.T.forEach(function (e) { if (!e.ok || !(DH.indexOf(e.p.join(' ')) >= 0 || e.v.indexOf('pool') >= 0)) return; var ok0 = e.ok; e.ok = function (st) { return ok0(st) || AC(st); }; });
  function AROrAC(st) { return st.vrp.kind === 'ar' || AC(st); }
  var o43 = Vr.cmd('pool', 'option 43 sub-option 3 ascii <ip>', function (st, a) { C(st).pools[top(st).n].o43 = a[0]; }, 'Configure option 43');
  o43.ok = AROrAC;
  var u43 = Vr.cmd('pool', 'undo option 43', function (st) { delete C(st).pools[top(st).n].o43; }); u43.ok = AROrAC;
  function hostRange(nt, ex) { var p = nt.split('/'), lo = IP.ip2n(p[0]) + 1, hi = IP.ip2n(p[0]) + Math.pow(2, 32 - +p[1]) - 2;
    var ok = function (n) { return !ex.some(function (e) { return n >= IP.ip2n(e[0]) && n <= IP.ip2n(e[1]); }); };
    while (lo <= hi && !ok(lo)) lo++; while (hi >= lo && !ok(hi)) hi--; return lo <= hi ? [IP.n2ip(lo), IP.n2ip(hi)] : null; }
  function gpool(p) { return { net: p.net, range: hostRange(p.net, (p.excl || []).concat(p.gw ? [[p.gw, p.gw]] : [])), gw: p.gw || null, dns: (p.dns || [])[0] || null, lease: null, o43: p.o43 || null }; }
  // пулы AC для общей логики DHCP (net.js): как у AR — пул интерфейса (dhcp select interface) или глобальный пул его подсети (dhcp select global); чужая подсеть — для relay
  var dc0 = EL.debDhcpCfg;
  EL.debDhcpCfg = function (d) { if (!d || !d.st.vrp || !d.st.vrp.ac) return dc0 ? dc0.apply(this, arguments) : null;
    var c = d.st.vrp.c; if (d.off || !c.dhcp) return null; var pp = {};
    Object.keys(c.ifs).forEach(function (n) { var x = c.ifs[n]; if (!/^Vlanif/.test(n) || !x.ip || !x.dsel || x.shut) return;
      if (x.dsel === 'interface') { var nt = IP.netOf(x.ip[0], x.ip[1]); pp[n] = { net: nt, range: hostRange(nt, [[x.ip[0], x.ip[0]]]), gw: x.ip[0], dns: (x.ddns || [])[0] || null, lease: null }; }
      if (x.dsel === 'global') Object.keys(c.pools || {}).forEach(function (k) { var p = c.pools[k]; if (p.net && IP.sameNet(x.ip[0], p.net.split('/')[0], +p.net.split('/')[1])) pp[k] = gpool(p); }); });
    Object.keys(c.pools || {}).forEach(function (k) { var p = c.pools[k]; if (pp[k] || !p.net) return;
      if (!Object.keys(c.ifs).some(function (n) { var x = c.ifs[n]; return /^Vlanif/.test(n) && x.ip && IP.sameNet(x.ip[0], p.net.split('/')[0], +p.net.split('/')[1]); })) pp[k] = gpool(p); });
    return { dhcp: { on: Object.keys(pp).length > 0, pools: pp }, ifs: {}, relay: false }; };
  // AR: опция 43 глобального пула — в пул модели
  var cAr = Vr.compileAr;
  Vr.compileAr = function (st) { cAr.apply(this, arguments); var c = C(st), D = st.run.dhcp; if (!D) return;
    Object.keys(D.pools).forEach(function (k) { var p = (c.pools || {})[k]; if (p && p.o43) D.pools[k].o43 = p.o43; }); st.cand = EL.clone(st.run); };

  // ---------------------------------------------------------------- вид wlan: профили, группы, AP
  var DEFSEC = ['default', 'default-wds', 'default-mesh'];
  function W(st) { var c = C(st); if (!c.wlan) c.wlan = { auth: 'mac-auth', groups: { default: { vaps: [] } }, reg: { default: { cc: 'cn' } }, sec: { default: {}, 'default-wds': {}, 'default-mesh': {} },
    ssid: { default: { ssid: 'HUAWEI-WLAN' } }, vap: { default: { fm: 'direct-forward', vlan: 1, ssid: 'default', sec: 'default' } }, aps: {}, wl: [], r2g: {}, r5g: {}, scan: {}, vpool: {} }; return c.wlan; }
  wc('sys', 'wlan', function (st) { W(st); Vr.push(st, { v: 'wlan', tag: 'wlan-view' }); }, 'WLAN view');
  wc('sys', 'capwap source interface <if>', function (st, a) { if (!/^(Vlanif|LoopBack)\d+$/.test(a[0])) return null; C(st).capwap = a[0]; }, 'CAPWAP source interface');
  wc('sys', 'undo capwap source interface', function (st) { delete C(st).capwap; });
  wc('sys', 'vlan pool <w>', function (st, a) { var V = W(st).vpool; V[a[0]] = V[a[0]] || { vl: [] }; Vr.push(st, { v: 'vpool', n: a[0], tag: 'vlan-pool-' + a[0] }); }, 'VLAN pool');
  wc('sys', 'undo vlan pool <w>', function (st, a) { delete W(st).vpool[a[0]]; });
  wc('vpool', 'vlan <vl>', function (st, a) { var p = W(st).vpool[top(st).n]; a[0].forEach(function (v) { if (p.vl.indexOf(v) < 0) p.vl.push(v); }); });
  wc('vpool', 'assignment hash', function (st) { W(st).vpool[top(st).n].hash = true; });
  wc('wlan', 'ap auth-mode <w>', function (st, a) { var m = a[0].toLowerCase(); if (['mac-auth', 'no-auth', 'sn-auth'].indexOf(m) < 0) return null; W(st).auth = m; }, 'AP authentication mode');
  wc('wlan', 'undo ap auth-mode', function (st) { W(st).auth = 'mac-auth'; });
  // офлайн-добавление AP: ap-id N [type-id T | ap-type X] ap-mac M [ap-sn S]
  function apAdd(st, id, mac, sn, tid) { if (id > 8191) return null; var w = W(st), m = mac === null ? null : macArg(mac); if (mac !== null && !m) return null;
    var A = w.aps[id] = w.aps[id] || {}; if (m) A.mac = m; if (sn) A.sn = sn; if (tid !== undefined) A.tid = tid; Vr.push(st, { v: 'wap', id: id, tag: 'wlan-ap-' + id }); }
  wc('wlan', 'ap-id <n>', function (st, a) { if (!W(st).aps[a[0]]) return null; Vr.push(st, { v: 'wap', id: a[0], tag: 'wlan-ap-' + a[0] }); }, 'AP ID');
  wc('wlan', 'ap-id <n> ap-mac <w>', function (st, a) { return apAdd(st, a[0], a[1]); });
  wc('wlan', 'ap-id <n> ap-sn <w>', function (st, a) { return apAdd(st, a[0], null, a[1]); });
  wc('wlan', 'ap-id <n> ap-mac <w> ap-sn <w>', function (st, a) { return apAdd(st, a[0], a[1], a[2]); });
  wc('wlan', 'ap-id <n> type-id <n> ap-mac <w>', function (st, a) { if (a[1] > 255) return null; return apAdd(st, a[0], a[2], null, a[1]); });
  wc('wlan', 'ap-id <n> type-id <n> ap-mac <w> ap-sn <w>', function (st, a) { if (a[1] > 255) return null; return apAdd(st, a[0], a[2], a[3], a[1]); });
  wc('wlan', 'ap-id <n> ap-type <w> ap-mac <w>', function (st, a) { var t = TYPES.filter(function (x) { return x[1].toLowerCase() === a[1].toLowerCase(); })[0]; if (!t) return null; return apAdd(st, a[0], a[2], null, t[0]); });
  function freeId(w) { var i = 0; while (w.aps[i]) i++; return i; }
  function byMac(w, m) { return Object.keys(w.aps).filter(function (k) { return w.aps[k].mac === m; })[0]; }
  wc('wlan', 'ap-mac <w>', function (st, a) { var m = macArg(a[0]), w = W(st); if (!m) return null; var id = byMac(w, m); if (id === undefined) { id = freeId(w); w.aps[id] = { mac: m }; }
    Vr.push(st, { v: 'wap', id: +id, tag: 'wlan-ap-' + id }); });
  function confirm(st, f) { var x = st.vrp, w = W(st), U = x.unauth || {}; Object.keys(U).forEach(function (m) { if (!f(m)) return; if (byMac(w, m) === undefined) w.aps[freeId(w)] = { mac: m }; delete U[m]; }); }
  wc('wlan', 'ap-confirm all', function (st) { confirm(st, function () { return true; }); }, 'Confirm unauthorized APs');
  wc('wlan', 'ap-confirm mac <w>', function (st, a) { var m = macArg(a[0]); if (!m) return null; confirm(st, function (q) { return q === m; }); });
  wc('wlan', 'ap whitelist mac <w>', function (st, a) { var m = macArg(a[0]); if (!m) return null; var L = W(st).wl; if (L.indexOf(m) < 0) L.push(m); }, 'AP whitelist');
  wc('wlan', 'undo ap whitelist mac <w>', function (st, a) { var w = W(st), m = macArg(a[0]); w.wl = w.wl.filter(function (q) { return q !== m; }); });
  wc('wlan', 'undo ap whitelist mac all', function (st) { W(st).wl = []; });
  function delAp(st, f) { var w = W(st); return ask(st, 'Warning: Deleting the AP will interrupt services on the AP. Continue?[Y/N]:', function () { Object.keys(w.aps).forEach(function (k) { if (f(k, w.aps[k])) delete w.aps[k]; }); Vr.compile(st); return ''; }); }
  wc('wlan', 'undo ap ap-id <vl>', function (st, a) { return delAp(st, function (k) { return a[0].indexOf(+k) >= 0; }); });
  wc('wlan', 'undo ap ap-mac <w>', function (st, a) { var m = macArg(a[0]); return delAp(st, function (k, A) { return A.mac === m; }); });
  wc('wlan', 'undo ap ap-name <w>', function (st, a) { return delAp(st, function (k, A) { return A.name === a[0]; }); });
  wc('wlan', 'undo ap all', function (st) { return delAp(st, function () { return true; }); });
  wc('wlan', 'ap-rename ap-id <n> new-name <w>', function (st, a) { var A = W(st).aps[a[0]]; if (!A) return null; A.name = a[1]; });
  wc('wlan', 'ap-rename ap-name <w> new-name <w>', function (st, a) { var w = W(st), k = Object.keys(w.aps).filter(function (q) { return w.aps[q].name === a[0]; })[0]; if (k === undefined) return null; w.aps[k].name = a[1]; });
  // профили: имя → объект; вид — тег по CR (regulate-domain, sec-prof, ssid-prof, vap-prof …)
  [['ap-group', 'groups', 'wgrp', 'ap-group', function () { return { vaps: [] }; }],
   ['regulatory-domain-profile', 'reg', 'wreg', 'regulate-domain', function () { return { cc: 'cn' }; }],
   ['security-profile', 'sec', 'wsec', 'sec-prof', function () { return {}; }],
   ['ssid-profile', 'ssid', 'wssid', 'ssid-prof', function () { return { ssid: 'HUAWEI-WLAN' }; }],
   ['vap-profile', 'vap', 'wvap', 'vap-prof', function () { return { fm: 'direct-forward', vlan: 1, ssid: 'default', sec: 'default' }; }],
   ['radio-2g-profile', 'r2g', 'wr2g', 'radio-2g-prof', function () { return {}; }], ['radio-5g-profile', 'r5g', 'wr5g', 'radio-5g-prof', function () { return {}; }],
   ['air-scan-profile', 'scan', 'wscan', 'air-scan-prof', function () { return {}; }]].forEach(function (x) {
    wc('wlan', x[0] + ' name <w>', function (st, a) { var M = W(st)[x[1]]; M[a[0]] = M[a[0]] || x[4](); Vr.push(st, { v: x[2], n: a[0], tag: 'wlan-' + x[3] + '-' + a[0] }); }, 'Configure ' + x[0]);
    wc('wlan', 'undo ' + x[0] + ' name <w>', function (st, a) { if (a[0] === 'default' || DEFSEC.indexOf(a[0]) >= 0 && x[1] === 'sec') return null; delete W(st)[x[1]][a[0]]; });
  });
  function pr(st, k) { return W(st)[k][top(st).n]; }
  wc('wreg', 'country-code <w>', function (st, a) { var r = pr(st, 'reg'), cc = a[0].toLowerCase(); if (!/^[a-z]{2}$/.test(cc)) return null;
    if (r.cc === cc) return 'Info: The current country code is same with the input country code.';
    return ask(st, 'Warning: Modifying the country code will clear channel, power and antenna gain configurations of the radio and reset the AP. Continue?[Y/N]:', function () { r.cc = cc; return ''; }); }, 'Country code');
  wc('wreg', 'undo country-code', function (st) { pr(st, 'reg').cc = 'cn'; });
  wc('wreg', 'dca-channel 2.4g channel-set <w>', function (st, a) { pr(st, 'reg').dca24 = a[0]; });
  wc('wreg', 'dca-channel 5g channel-set <w>', function (st, a) { pr(st, 'reg').dca5 = a[0]; });
  wc('wreg', 'dca-channel 5g bandwidth <w>', function (st, a) { pr(st, 'reg').dca5bw = a[0]; });
  wc('wsec', 'security <w> psk <w> <w> <w>', function (st, a) { var t = a[0].toLowerCase(), k = a[1].toLowerCase(), e = a[3].toLowerCase();
    if (['wpa', 'wpa2', 'wpa-wpa2'].indexOf(t) < 0 || ['pass-phrase', 'hex'].indexOf(k) < 0 || ['aes', 'tkip', 'aes-tkip'].indexOf(e) < 0) return null;
    if (k === 'pass-phrase' && (a[2].length < 8 || a[2].length > 63)) return null; var p = pr(st, 'sec'); p.mode = t; p.psk = { k: k, v: a[2], enc: e }; }, 'Security policy');
  wc('wsec', 'security open', function (st) { var p = pr(st, 'sec'); delete p.mode; delete p.psk; });
  wc('wsec', 'undo security', function (st) { var p = pr(st, 'sec'); delete p.mode; delete p.psk; });
  wc('wssid', 'ssid <w>', function (st, a) { if (a[0].length > 32) return null; pr(st, 'ssid').ssid = a[0]; }, 'SSID name');
  wc('wssid', 'undo ssid', function (st) { pr(st, 'ssid').ssid = 'HUAWEI-WLAN'; });
  wc('wvap', 'forward-mode direct-forward', function (st) { pr(st, 'vap').fm = 'direct-forward'; }, 'Forward mode');
  wc('wvap', 'forward-mode tunnel', function (st) { var v = pr(st, 'vap'); return ask(st, 'Warning: This action may cause service interruption. Continue?[Y/N]', function () { v.fm = 'tunnel'; return ''; }); });
  wc('wvap', 'undo forward-mode', function (st) { pr(st, 'vap').fm = 'direct-forward'; });
  wc('wvap', 'service-vlan vlan-id <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return null; var v = pr(st, 'vap'); v.vlan = a[0]; delete v.vpool; }, 'Service VLAN');
  wc('wvap', 'service-vlan vlan-pool <w>', function (st, a) { if (!W(st).vpool[a[0]]) return null; var v = pr(st, 'vap'); v.vpool = a[0]; delete v.vlan; });
  wc('wvap', 'undo service-vlan', function (st) { var v = pr(st, 'vap'); v.vlan = 1; delete v.vpool; });
  wc('wvap', 'ssid-profile <w>', function (st, a) { if (!W(st).ssid[a[0]]) return null; pr(st, 'vap').ssid = a[0]; }, 'Bind SSID profile');
  wc('wvap', 'undo ssid-profile', function (st) { pr(st, 'vap').ssid = 'default'; });
  wc('wvap', 'security-profile <w>', function (st, a) { if (!W(st).sec[a[0]]) return null; pr(st, 'vap').sec = a[0]; }, 'Bind security profile');
  wc('wvap', 'undo security-profile', function (st) { pr(st, 'vap').sec = 'default'; });
  ['wr2g', 'wr5g'].forEach(function (v) { wc(v, 'air-scan-profile <w>', function (st, a) { if (!W(st).scan[a[0]]) return null; pr(st, v === 'wr2g' ? 'r2g' : 'r5g').scan = a[0]; }); });
  wc('wscan', 'scan-channel-set dca-channel', function (st) { pr(st, 'scan').dca = true; });
  wc('wscan', 'scan-period <n>', function (st, a) { pr(st, 'scan').period = a[0]; });
  wc('wscan', 'scan-interval <n>', function (st, a) { pr(st, 'scan').interval = a[0]; });
  // группа AP
  function grp(st) { return W(st).groups[top(st).n]; }
  wc('wgrp', 'regulatory-domain-profile <w>', function (st, a) { if (!W(st).reg[a[0]]) return null; var g = grp(st);
    return ask(st, 'Warning: Modifying the country code will clear channel, power and antenna gain configurations of the radio and reset the AP. Continue?[Y/N]:', function () { g.reg = a[0]; return ''; }); }, 'Bind regulatory domain profile');
  wc('wgrp', 'undo regulatory-domain-profile', function (st) { delete grp(st).reg; });
  function bindVap(L, vap, wlan, radios, svlan) { L = L.filter(function (b) { return !(b.wlan === wlan && radios.indexOf(b.radio) >= 0); });
    radios.forEach(function (r) { L.push({ vap: vap, wlan: wlan, radio: r, svlan: svlan }); }); return L; }
  [['wgrp', grp], ['wap', function (st) { return W(st).aps[top(st).id]; }]].forEach(function (x) { var v = x[0], O = x[1];
    function vb(st, a, radios, svlan) { if (!W(st).vap[a[0]] || a[1] < 1 || a[1] > 16) return null; var o = O(st); o.vaps = bindVap(o.vaps || [], a[0], a[1], radios, svlan); return 'Info: This operation may take a few seconds, please wait...done.'; }
    wc(v, 'vap-profile <w> wlan <n> radio <n>', function (st, a) { if (a[2] > 2) return null; return vb(st, a, [a[2]]); }, 'Bind VAP profile');
    wc(v, 'vap-profile <w> wlan <n> radio all', function (st, a) { return vb(st, a, [0, 1]); });
    wc(v, 'vap-profile <w> wlan <n> radio <n> service-vlan vlan-id <n>', function (st, a) { if (a[2] > 2) return null; return vb(st, a, [a[2]], a[3]); });
    wc(v, 'vap-profile <w> wlan <n> radio all service-vlan vlan-id <n>', function (st, a) { return vb(st, a, [0, 1], a[2]); });
    wc(v, 'undo vap-profile <w> wlan <n> radio <n>', function (st, a) { var o = O(st); o.vaps = (o.vaps || []).filter(function (b) { return !(b.vap === a[0] && b.wlan === a[1] && b.radio === a[2]); }); });
    wc(v, 'undo vap-profile <w> wlan <n> radio all', function (st, a) { var o = O(st); o.vaps = (o.vaps || []).filter(function (b) { return !(b.vap === a[0] && b.wlan === a[1]); }); });
    wc(v, 'radio-2g-profile <w> radio <n>', function (st, a) { if (!W(st).r2g[a[0]]) return null; var o = O(st); (o.rp = o.rp || {})[a[1]] = '2g ' + a[0]; });
    wc(v, 'radio-5g-profile <w> radio <n>', function (st, a) { if (!W(st).r5g[a[0]]) return null; var o = O(st); (o.rp = o.rp || {})[a[1]] = '5g ' + a[0]; });
    wc(v, 'radio <n>', function (st, a) { if (a[0] > 2) return null; var o = O(st); o.radio = o.radio || {}; o.radio[a[0]] = o.radio[a[0]] || {};
      Vr.push(st, { v: v === 'wgrp' ? 'wgrad' : 'wrad', r: a[0], o: v === 'wgrp' ? top(st).n : top(st).id, tag: v === 'wgrp' ? 'wlan-group-radio-' + top(st).n + '/' + a[0] : 'wlan-radio-' + top(st).id + '/' + a[0] }); }, 'Radio');
  });
  function rad(st) { var t = top(st), w = W(st), o = t.v === 'wgrad' ? w.groups[t.o] : w.aps[t.o]; return o.radio[t.r]; }
  wc('wgrad wrad', 'calibrate auto-channel-select disable', function (st) { rad(st).noAutoCh = true; });
  wc('wgrad wrad', 'undo calibrate auto-channel-select disable', function (st) { delete rad(st).noAutoCh; });
  wc('wgrad wrad', 'calibrate auto-txpower-select disable', function (st) { rad(st).noAutoPw = true; });
  wc('wgrad wrad', 'undo calibrate auto-txpower-select disable', function (st) { delete rad(st).noAutoPw; });
  wc('wgrad wrad', 'channel <w> <n>', function (st, a) { if (!/^(20mhz|40mhz-minus|40mhz-plus|80mhz|160mhz)$/i.test(a[0])) return null; var r = rad(st);
    return ask(st, 'Warning: This action may cause service interruption. Continue?[Y/N]', function () { r.ch = a[0].toLowerCase() + ' ' + a[1]; return ''; }); }, 'Channel');
  wc('wgrad wrad', 'undo channel', function (st) { delete rad(st).ch; });
  wc('wgrad wrad', 'eirp <n>', function (st, a) { if (a[0] < 1 || a[0] > 127) return null; rad(st).eirp = a[0]; if (!rad(st).noAutoPw) return 'Info: The EIRP value takes effect only when automatic transmit power selection is disabled.'; }, 'EIRP');
  wc('wgrad wrad', 'undo eirp', function (st) { delete rad(st).eirp; });
  // AP
  function ap(st) { return W(st).aps[top(st).id]; }
  wc('wap', 'ap-name <w>', function (st, a) { var w = W(st); if (Object.keys(w.aps).some(function (k) { return +k !== top(st).id && w.aps[k].name === a[0]; })) return null; ap(st).name = a[0]; }, 'AP name');
  wc('wap', 'undo ap-name', function (st) { delete ap(st).name; });
  wc('wap', 'ap-group <w>', function (st, a) { var A = ap(st); if (!W(st).groups[a[0]]) return null;
    return ask(st, 'Warning: This operation may cause AP reset. If the country code changes, it will clear channel, power and antenna gain\nconfigurations of the radio, Whether to continue? [Y/N]:', function () { A.group = a[0]; return ''; }); }, 'AP group');
  wc('wap', 'undo ap-group', function (st) { delete ap(st).group; });
  wc('wap', 'regulatory-domain-profile <w>', function (st, a) { if (!W(st).reg[a[0]]) return null; ap(st).reg = a[0]; });
  wc('wlan', 'ap username <w> password cipher <w>', function (st, a) { if (a[1].length < 8 || a[1].length > 32) return null; W(st).user = { u: a[0], p: a[1] }; });
  wc('wlan', 'undo ap username', function (st) { delete W(st).user; });
  // provision-ap: режим Fat/Cloud, применяется commit — AP выходит из-под управления AC
  wc('wlan', 'provision-ap', function (st) { Vr.push(st, { v: 'wprov', tag: 'wlan-provision-ap' }); }, 'Provision AP');
  wc('wprov', 'ap-mode <w>', function (st, a) { var m = a[0].toLowerCase(); if (m !== 'fat' && m !== 'cloud') return null; var x = st.vrp;
    return ask(st, 'Warning: When the configuration is committed, the AP mode will be switched if supported and the AP will be out of control by the AC.Continue?[Y/N]:', function () { x.prov = m; return ''; }); }, 'AP mode');
  wc('wprov', 'undo ap-mode', function (st) { delete st.vrp.prov; });
  function commit(st, f) { var x = st.vrp, w = W(st), net = st.net, m = x.prov; if (!m) return '';
    return ask(st, 'Warning: The incorrect configuration will cause the AP to go out of management. This operation will deliver parameter setting and ma\ny cause reboot of AP(s). Continue?[Y/N]:', function () {
      Object.keys(w.aps).forEach(function (k) { var A = w.aps[k], o = (x.online || {})[A.mac]; if (!o || o.state !== 'normal' || !f(k, A)) return; var d = net && net.devs[o.dev]; if (d) d.st.apMode = m; delete x.online[A.mac]; });
      return ''; }); }
  wc('wprov', 'commit ap-id <n>', function (st, a) { return commit(st, function (k) { return +k === a[0]; }); }, 'Commit');
  wc('wprov', 'commit ap-mac <w>', function (st, a) { var m = macArg(a[0]); return commit(st, function (k, A) { return A.mac === m; }); });
  wc('wprov', 'commit ap-name <w>', function (st, a) { return commit(st, function (k, A) { return A.name === a[0]; }); });
  wc('wprov', 'commit ap-group <w>', function (st, a) { return commit(st, function (k, A) { return (A.group || 'default') === a[0]; }); });
  wc('wprov', 'commit all', function (st) { return commit(st, function () { return true; }); });

  // ---------------------------------------------------------------- выход AP в сеть (CG j0cz): DHCP → поиск AC → допуск → normal
  function acIp(net, d) { var c = d.st.vrp.c, n = c.capwap; if (!n) return null;
    var k = /^Vlanif/.test(n) ? 'vlan' + n.slice(6) : 'lo' + n.slice(8), f = net.ifaces(d.id).filter(function (q) { return q.name === k; })[0]; return f ? f.ip : null; }
  P.hwapSync = function () {
    var s = this, ACs = this.list().filter(function (d) { return d.st.vrp && d.st.vrp.ac; });
    ACs.forEach(function (a) { var x = a.st.vrp; x.online = x.online || {}; x.unauth = x.unauth || {}; });
    this.list().filter(isAp).forEach(function (d) {
      var st = d.st, mac = apMac(d), m = EL.MODELS[d.model] || {};
      var drop = function () { ACs.forEach(function (a) { delete a.st.vrp.online[mac]; }); };
      if (d.off || st.apMode !== 'fit' || !s.linkUp(d.id, 'LAN')) { if (d.off || !s.linkUp(d.id, 'LAN')) { st.ip = null; st.o43 = null; } drop(); return; }
      if (!st.ip) { var r = s.dhcp(d.id); if (!r.ok) { drop(); return; } st.ip = r.ip; st.len = r.len; st.gw = r.gw || null; st.o43 = r.pool && r.pool.o43 || null; }
      // кандидаты: опция 43 — адрес AC; без неё — AC, чей адрес CAPWAP в подсети AP (broadcast Discovery)
      var acs = ACs.filter(function (a) { var ip = acIp(s, a); return ip && !a.off && (st.o43 ? ip === st.o43 : IP.sameNet(ip, st.ip, st.len)); });
      var hit = acs.filter(function (a) { return s.ping(d.id, acIp(s, a)).ok; })[0];
      ACs.forEach(function (a) { if (a !== hit) delete a.st.vrp.online[mac]; });
      if (!hit) return;
      var x = hit.st.vrp, w = W(hit.st), id = byMac(w, mac);
      var ok = id !== undefined || w.auth === 'no-auth' || w.wl.indexOf(mac) >= 0;
      if (!ok) { delete x.online[mac]; if (!x.unauth[mac]) x.unauth[mac] = { type: d.model, ip: st.ip, t: s.now || 0 }; else x.unauth[mac].ip = st.ip; return; }
      if (id === undefined) { id = freeId(w); w.aps[id] = { mac: mac }; }
      var A = w.aps[id]; delete x.unauth[mac];
      if (A.tid !== undefined && A.tid !== m.typeId) { x.online[mac] = { dev: d.id, id: +id, ip: st.ip, state: 'type-mismatch', since: x.online[mac] ? x.online[mac].since : s.now || 0 }; return; }
      A.tid = m.typeId;
      var o = x.online[mac]; if (!o || o.state !== 'normal') x.online[mac] = { dev: d.id, id: +id, ip: st.ip, state: 'normal', since: s.now || 0 }; else { o.ip = st.ip; o.id = +id; }
    });
  };
  function sync(st) { if (st.net) st.net.hwapSync(); }

  // ---------------------------------------------------------------- display
  var TYPES = [[35, 'AP5030DN'], [43, 'AP4030DN'], [45, 'AP3030DN'], [46, 'AP2030DN'], [60, 'AP4030TN'], [61, 'AP4050DN-E'], [69, 'AP2050DN'], [70, 'AP2050DN-E'], [75, 'AP4050DN']];
  function tname(t) { var x = TYPES.filter(function (q) { return q[0] === t; })[0]; return x ? x[1] : '-'; }
  function upt(t) { t = Math.max(0, Math.floor(t)); var h = Math.floor(t / 3600), m = Math.floor(t / 60) % 60, s = t % 60; return (h ? h + 'H:' : '') + (h || m ? m + 'M:' : '') + s + 'S'; }
  function apList(st) { var x = st.vrp, w = W(st), on = x.online || {}, now = (st.net && st.net.now) || 0;
    return Object.keys(w.aps).map(Number).sort(function (a, b) { return a - b; }).map(function (k) { var A = w.aps[k], o = A.mac && on[A.mac];
      return { id: k, mac: A.mac || '-', name: A.name || A.mac || '-', group: A.group || 'default', ip: o ? o.ip : '-', type: tname(A.tid), state: o ? o.state : 'idle', up: o ? upt(now - o.since) : '-', A: A }; }); }
  var ST = { normal: 'nor', idle: 'idle', 'type-mismatch': 'type-mismatch' };
  function apTable(L) { var SEP = new Array(99).join('-'), o = ['Total AP information:'], n = L.filter(function (r) { return r.state === 'normal'; }).length;
    if (n) o.push('nor  : normal          [' + n + ']'); o.push('Extra information:', 'P  : insufficient power supply', SEP,
      'ID   MAC            Name   Group     IP            Type            State STA Uptime      ExtraInfo', SEP);
    L.forEach(function (r) { o.push(pad(r.id, 5) + pad(r.mac, 15) + pad(r.name, 7) + pad(r.group, 10) + pad(r.ip, 14) + pad(r.type, 16) + pad(ST[r.state] || r.state, 6) + pad(0, 4) + pad(r.up, 12) + '-'); });
    o.push(SEP, 'Total: ' + L.length); return o.join('\n'); }
  wc('*', 'display ap all', function (st) { sync(st); return apTable(apList(st)); }, 'Display AP information').cfg = false;
  wc('*', 'display ap ap-group <w>', function (st, a) { sync(st); return apTable(apList(st).filter(function (r) { return r.group === a[0]; })); }).cfg = false;
  wc('*', 'display ap by-state <w>', function (st, a) { sync(st); return apTable(apList(st).filter(function (r) { return r.state === a[0].toLowerCase(); })); }).cfg = false;
  wc('*', 'display ap by-ssid <w>', function (st, a) { sync(st); return apTable(apList(st).filter(function (r) { return vaps(st, r).some(function (v) { return v.ssid === a[0]; }); })); }).cfg = false;
  // VAP: для AP в normal — привязки vap-profile её группы и её самой
  function authType(sp) { return !sp || !sp.mode ? 'Open' : sp.mode === 'wpa-wpa2' ? 'WPA/WPA2-PSK' : sp.mode.toUpperCase() + '-PSK'; }
  function bssid(mac, r) { var n = parseInt(mac.replace(/-/g, ''), 16) + r * 16, h = ('000000000000' + n.toString(16)).slice(-12).toUpperCase(); return h.slice(0, 4) + '-' + h.slice(4, 8) + '-' + h.slice(8); }
  function vaps(st, r) { var w = W(st); if (r.state !== 'normal') return []; var g = w.groups[r.group] || { vaps: [] }, L = (g.vaps || []).concat(r.A.vaps || []);
    return L.map(function (b) { var v = w.vap[b.vap] || {}, sp = w.sec[v.sec], ss = w.ssid[v.ssid] || {};
      return { ap: r, radio: b.radio, wlan: b.wlan, bssid: bssid(r.mac, b.radio), auth: authType(sp), ssid: ss.ssid || 'HUAWEI-WLAN' }; }); }
  function vapTable(st, f) { sync(st); var SEP = new Array(81).join('-'), o = ['WID : WLAN ID', SEP, 'AP ID AP name RfID WID   BSSID          Status  Auth type     STA   SSID', SEP], L = [];
    apList(st).forEach(function (r) { vaps(st, r).forEach(function (v) { if (!f || f(v)) L.push(v); }); });
    L.forEach(function (v) { o.push(pad(v.ap.id, 6) + pad(v.ap.name, 8) + pad(v.radio, 5) + pad(v.wlan, 6) + pad(v.bssid, 15) + pad('ON', 8) + pad(v.auth, 14) + pad(0, 6) + v.ssid); });
    o.push(SEP.slice(1), 'Total: ' + L.length); return o.join('\n'); }
  wc('*', 'display vap all', function (st) { return vapTable(st); }, 'Display VAP').cfg = false;
  wc('*', 'display vap ssid <w>', function (st, a) { return vapTable(st, function (v) { return v.ssid === a[0]; }); }).cfg = false;
  wc('*', 'display vap ap-group <w>', function (st, a) { return vapTable(st, function (v) { return v.ap.group === a[0]; }); }).cfg = false;
  wc('*', 'display vap ap-id <n>', function (st, a) { return vapTable(st, function (v) { return v.ap.id === a[0]; }); }).cfg = false;
  wc('*', 'display vap ap-name <w>', function (st, a) { return vapTable(st, function (v) { return v.ap.name === a[0]; }); }).cfg = false;
  function staTable() { var SEP = new Array(82).join('-');
    return ['Rf/WLAN: Radio ID/WLAN ID', 'Rx/Tx: link receive rate/link transmit rate(Mbps)', SEP, 'STA MAC         AP ID Ap name   Rf/WLAN  Band  Type  Rx/Tx      RSSI  VLAN  IP address', SEP, SEP, 'Total: 0 2.4G: 0 5G: 0'].join('\n'); }
  ['all', 'ssid <w>', 'ap-group <w>', 'ap-name <w>', 'ap-id <n>', 'sta-mac <w>', 'vlan <n>'].forEach(function (s, i) { wc('*', 'display station ' + s, function () { return staTable(); }, i ? '' : 'Display station').cfg = false; });
  function listTbl(head, rows, w, total) { var SEP = new Array(w + 1).join('-'); return [SEP, head, SEP].concat(rows, [SEP, 'Total: ' + (total === undefined ? rows.length : total)]).join('\n'); }
  function refs(st, kind, n) { var w = W(st);
    if (kind === 'ssid') return Object.keys(w.vap).filter(function (k) { return w.vap[k].ssid === n; }).length;
    if (kind === 'sec') return Object.keys(w.vap).filter(function (k) { return w.vap[k].sec === n; }).length + (DEFSEC.indexOf(n) > 0 ? 1 : 0);
    if (kind === 'vap') return Object.keys(w.groups).reduce(function (s, g) { return s + (w.groups[g].vaps || []).filter(function (b) { return b.vap === n; }).length; }, 0);
    if (kind === 'reg') return Object.keys(w.groups).filter(function (g) { return (w.groups[g].reg || 'default') === n; }).length;
    return 0; }
  wc('*', 'display ap-group all', function (st) { sync(st); var w = W(st), L = apList(st);
    return listTbl('Name                           APs', Object.keys(w.groups).map(function (g) { return pad(g, 31) + L.filter(function (r) { return r.group === g; }).length; }), 58); }, 'Display AP group').cfg = false;
  wc('*', 'display ssid-profile all', function (st) { var w = W(st);
    return listTbl('Profile name  Beacon 2.4G/5G rate(Mbps)  Reference  SSID', Object.keys(w.ssid).map(function (k) { return pad(k, 14) + pad('1/6', 27) + pad(refs(st, 'ssid', k), 11) + w.ssid[k].ssid; }), 63); }).cfg = false;
  wc('*', 'display vap-profile all', function (st) { var w = W(st), SEP = new Array(109).join('-');
    return ['FMode   : Forward mode', 'STA U/D : Rate limit client up/down', 'VAP U/D : Rate limit VAP up/down', 'BR2G/5G : Beacon 2.4G/5G rate', SEP,
      'Name          FMode    Type      VLAN    AuthType  STA U/D(Kbps)  VAP U/D(Kbps)  BR2G/5G(Mbps)  Reference  SSID', SEP].concat(Object.keys(w.vap).map(function (k) { var v = w.vap[k];
        return pad(k, 14) + pad(v.fm === 'tunnel' ? 'tunnel' : 'direct', 9) + pad('service', 10) + pad(v.vpool ? 'pool' : 'VLAN ' + v.vlan, 8) + pad(authType(w.sec[v.sec]) === 'Open' ? 'Open' : 'PSK', 10) +
          pad('-/-', 15) + pad('-/-', 15) + pad('1/6', 15) + pad(refs(st, 'vap', k), 11) + ((w.ssid[v.ssid] || {}).ssid || 'HUAWEI-WLAN'); }), [SEP, 'Total: ' + Object.keys(w.vap).length]).join('\n'); }).cfg = false;
  wc('*', 'display security-profile all', function (st) { var w = W(st);
    return listTbl('Profile name                   Reference', Object.keys(w.sec).map(function (k) { return pad(k, 31) + refs(st, 'sec', k); }), 58); }).cfg = false;
  wc('*', 'display regulatory-domain-profile all', function (st) { var w = W(st);
    return listTbl('Profile name        Reference', Object.keys(w.reg).map(function (k) { return pad(k, 20) + refs(st, 'reg', k); }), 60); }).cfg = false;
  wc('*', 'display ap unauthorized record', function (st) { sync(st); var U = st.vrp.unauth || {}, K = Object.keys(U), SEP = new Array(81).join('-'), o = ['Unauthorized AP record:', 'Total number: ' + K.length];
    K.forEach(function (m) { o.push(SEP, 'AP type: ' + U[m].type, 'AP SN: -', 'AP MAC address: ' + m, 'AP IP address: ' + U[m].ip, 'Record time: ' + EL.clock.fmt(EL.clock.now())); });
    if (K.length) o.push(SEP); return o.join('\n'); }, 'Display unauthorized AP').cfg = false;
  wc('*', 'display ap whitelist mac', function (st) { var L = W(st).wl, SEP = new Array(41).join('-');
    return [SEP, 'Index  MAC', SEP].concat(L.map(function (m, i) { return pad(i, 7) + m; }), [SEP, 'Total: ' + L.length]).join('\n'); }).cfg = false;
  wc('*', 'display ap-type all', function () { var SEP = new Array(41).join('-'); return listTbl('ID     Type', TYPES.map(function (t) { return pad(t[0], 7) + t[1]; }), 40, 86).replace(/^-+\n/, SEP + '\n'); }).cfg = false;
  wc('*', 'display capwap configuration', function (st) { var n = C(st).capwap, L = [['Source interface', n ? n.toLowerCase() : '-'], ['Source ip-address', '-'], ['Echo interval(seconds)', 25], ['Echo times', 6],
      ['Control priority(server to client)', 7], ['Control priority(client to server)', 7], ['Data-link DTLS encrypt', 'disable'], ['Data-link inter-controller DTLS encrypt', 'disable'],
      ['Control-link DTLS encrypt', 'disable'], ['DTLS PSK value', '******'], ['PSK mandatory match switch', 'disable'], ['Control-link inter-controller DTLS encrypt', 'disable'],
      ['Inter-controller DTLS PSK value', '******'], ['IPv6 status', 'disable'], ['Message-integrity PSK value', '******'], ['Message-integrity check switch', 'enable'],
      ['Sensitive-info PSK value', '******'], ['Sensitive-info inter-controller PSK value', '******']], SEP = '  ' + new Array(64).join('-');
    return [SEP].concat(L.map(function (x) { return '  ' + pad(x[0], 49) + ': ' + x[1]; }), [SEP]).join('\n'); }, 'Display CAPWAP configuration').cfg = false;
  wc('*', 'display ap username', function (st) { var u = W(st).user; return 'AP username: ' + (u ? u.u : 'admin') + '\nIs original password : ' + (u ? 'NO' : 'YES'); }).cfg = false;

  // ---------------------------------------------------------------- display current-configuration (AC): DHCP, пулы, capwap, wlan
  function cipher(p) { return '%^%#' + EL.E.hash(p).slice(0, 40) + '%^%#'; }
  function wlanLines(c) { var w = c.wlan, o = ['wlan']; if (!w) return null;
    if (w.auth !== 'mac-auth') o.push(' ap auth-mode ' + w.auth); w.wl.forEach(function (m) { o.push(' ap whitelist mac ' + m); });
    Object.keys(w.sec).forEach(function (k) { var p = w.sec[k]; if (DEFSEC.indexOf(k) >= 0 && !p.mode) return; o.push(' security-profile name ' + k);
      if (p.mode) o.push('  security ' + p.mode + ' psk ' + p.psk.k + ' ' + cipher(p.psk.v) + ' ' + p.psk.enc); });
    Object.keys(w.ssid).forEach(function (k) { var p = w.ssid[k]; if (k === 'default' && p.ssid === 'HUAWEI-WLAN') return; o.push(' ssid-profile name ' + k); if (p.ssid !== 'HUAWEI-WLAN') o.push('  ssid ' + p.ssid); });
    Object.keys(w.vpool).forEach(function (k) { void k; });
    Object.keys(w.vap).forEach(function (k) { var v = w.vap[k], L = []; if (v.fm !== 'direct-forward') L.push('  forward-mode ' + v.fm);
      if (v.vpool) L.push('  service-vlan vlan-pool ' + v.vpool); else if (v.vlan !== 1) L.push('  service-vlan vlan-id ' + v.vlan);
      if (v.ssid !== 'default') L.push('  ssid-profile ' + v.ssid); if (v.sec !== 'default') L.push('  security-profile ' + v.sec);
      if (k !== 'default' || L.length) o.push(' vap-profile name ' + k); o.push.apply(o, L); });
    Object.keys(w.reg).forEach(function (k) { var r = w.reg[k], L = []; if (r.cc !== 'cn') L.push('  country-code ' + r.cc);
      if (r.dca24) L.push('  dca-channel 2.4g channel-set ' + r.dca24); if (r.dca5bw) L.push('  dca-channel 5g bandwidth ' + r.dca5bw); if (r.dca5) L.push('  dca-channel 5g channel-set ' + r.dca5);
      if (k !== 'default' || L.length) o.push(' regulatory-domain-profile name ' + k); o.push.apply(o, L); });
    Object.keys(w.scan).forEach(function (k) { var p = w.scan[k]; o.push(' air-scan-profile name ' + k); if (p.dca) o.push('  scan-channel-set dca-channel');
      if (p.period) o.push('  scan-period ' + p.period); if (p.interval) o.push('  scan-interval ' + p.interval); });
    [['r2g', '2g'], ['r5g', '5g']].forEach(function (x) { Object.keys(w[x[0]]).forEach(function (k) { o.push(' radio-' + x[1] + '-profile name ' + k); if (w[x[0]][k].scan) o.push('  air-scan-profile ' + w[x[0]][k].scan); }); });
    function radios(O, ind) { var R = {}; (O.vaps || []).forEach(function (b) { (R[b.radio] = R[b.radio] || []).push(ind + ' vap-profile ' + b.vap + ' wlan ' + b.wlan + (b.svlan ? ' service-vlan vlan-id ' + b.svlan : '')); });
      Object.keys(O.rp || {}).forEach(function (r) { var p = O.rp[r].split(' '); (R[r] = R[r] || []).unshift(ind + ' radio-' + p[0] + '-profile ' + p[1]); });
      Object.keys(O.radio || {}).forEach(function (r) { var y = O.radio[r], L = R[r] = R[r] || []; if (y.noAutoCh) L.push(ind + ' calibrate auto-channel-select disable'); if (y.noAutoPw) L.push(ind + ' calibrate auto-txpower-select disable');
        if (y.ch) L.push(ind + ' channel ' + y.ch); if (y.eirp) L.push(ind + ' eirp ' + y.eirp); });
      var out = []; Object.keys(R).sort().forEach(function (r) { if (R[r].length) out.push(ind + 'radio ' + r); out.push.apply(out, R[r]); }); return out; }
    Object.keys(w.groups).forEach(function (k) { var g = w.groups[k], L = (g.reg && g.reg !== 'default' ? ['  regulatory-domain-profile ' + g.reg] : []).concat(radios(g, '  '));
      if (k !== 'default' || L.length) o.push(' ap-group name ' + k); o.push.apply(o, L); });
    Object.keys(w.aps).map(Number).sort(function (a, b) { return a - b; }).forEach(function (k) { var A = w.aps[k];
      o.push(' ap-id ' + k + (A.tid !== undefined ? ' type-id ' + A.tid : '') + (A.mac ? ' ap-mac ' + A.mac : '') + (A.sn ? ' ap-sn ' + A.sn : ''));
      if (A.name) o.push('  ap-name ' + A.name); if (A.group) o.push('  ap-group ' + A.group); if (A.reg) o.push('  regulatory-domain-profile ' + A.reg); o.push.apply(o, radios(A, '  ')); });
    if (w.user) o.push(' ap username ' + w.user.u + ' password cipher ' + cipher(w.user.p));
    return o; }
  var rS = Vr.renderS;
  Vr.renderS = function (st) { var out = rS.apply(this, arguments); if (!AC(st)) return out; var c = C(st), add = [];
    out.forEach(function (p) { var m = p.h.match(/^interface (Vlanif\d+)$/); if (!m) return; var x = c.ifs[m[1]] || {};
      if (x.dsel) p.L.push(' dhcp select ' + x.dsel); if (x.ddns) p.L.push(' dhcp server dns-list ' + x.ddns.join(' ')); });
    if (c.dhcp) add.push({ h: 'dhcp', L: ['dhcp enable'] });
    Object.keys(c.pools || {}).forEach(function (k) { var p = c.pools[k], L = ['ip pool ' + k];
      if (p.gw) L.push(' gateway-list ' + p.gw); if (p.net) L.push(' network ' + p.net.split('/')[0] + ' mask ' + IP.len2mask(+p.net.split('/')[1]));
      (p.excl || []).forEach(function (e) { L.push(' excluded-ip-address ' + e[0] + (e[1] !== e[0] ? ' ' + e[1] : '')); }); if (p.dns) L.push(' dns-list ' + p.dns.join(' '));
      if (p.o43) L.push(' option 43 sub-option 3 ascii ' + p.o43); add.push({ h: 'pool', L: L }); });
    var vi = out.map(function (p) { return p.h; }).indexOf('vlan'); out.splice.apply(out, [vi + 1, 0].concat(add));
    var w = c.wlan; Object.keys((w || {}).vpool || {}).forEach(function (k) { var p = w.vpool[k]; out.push({ h: 'vpool', L: ['vlan pool ' + k].concat(p.vl.length ? [' vlan ' + Vr.vlTxt(p.vl)] : [], p.hash ? [' assignment hash'] : []) }); });
    if (c.capwap) out.push({ h: 'capwap', L: ['capwap source interface ' + c.capwap.toLowerCase()] });
    var wl = c.wlan && wlanLines(c); if (wl) out.push({ h: 'wlan', L: wl });
    return out; };
  // AR: опция 43 в пуле
  var rAr = Vr.renderAr;
  Vr.renderAr = function (st) { var out = rAr.apply(this, arguments), c = C(st);
    out.forEach(function (p) { var m = p.h === 'pool' && p.L[0].match(/^ip pool (\S+)$/), x = m && (c.pools || {})[m[1]]; if (x && x.o43) p.L.push(' option 43 sub-option 3 ascii ' + x.o43); }); return out; };

  // ---------------------------------------------------------------- устройства
  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}, st = d.st;
    if (m.ac) { st.vrp.ac = true; st.vrp.c.sysname = model; Vr.compile(st); }
    if (m.kind === 'hwap') { d.sub = 'hwap'; st.port = 'LAN'; st.up = true; st.apMode = 'fit'; st.ip = null; st.host = d.name; }
    return d; };
  var rb0 = P.reboot;
  P.reboot = function (id) { var d = this.devs[id], r = rb0.apply(this, arguments); if (d && d.st.vrp && d.st.vrp.ac) { var x = d.st.vrp; if (!x.saved) x.c.sysname = d.model; x.online = {}; x.unauth = {}; Vr.compile(d.st); }
    if (isAp(d)) { d.st.ip = null; d.st.o43 = null; } return r; };
  // у Fit AP своей CLI в источниках нет — консоль молчит
  var ex0 = P.exec, pr0 = P.prompt, he0 = P.help, tb0 = P.tab;
  P.exec = function (id) { return isAp(this.devs[id]) ? '' : ex0.apply(this, arguments); };
  P.prompt = function (id) { return isAp(this.devs[id]) ? '' : pr0.apply(this, arguments); };
  P.help = function (id) { return isAp(this.devs[id]) ? '' : he0.apply(this, arguments); };
  P.tab = function (id) { return isAp(this.devs[id]) ? null : tb0.apply(this, arguments); };
  var pw0 = P.power;
  P.power = function (id, on) { var r = pw0.apply(this, arguments), d = this.devs[id]; if (isAp(d) && !on) { d.st.ip = null; d.st.o43 = null; } return r; };
  EL.hwlan = { apMac: apMac };
})(typeof window !== 'undefined' ? window : global);
