/* Коммутаторы Huawei S (S5700, S3700) — спецификация sources/huawei/spec/s-switch.md (HCIA-LG гл. 3, CR S V200R011C10, CG V200R005).
   Настройки VRP (st.vrp.c) → поля модели MES: ports (access/trunk/general = hybrid), vlans, svi (Vlanif), pos + cg (Eth-Trunk), stp, mst, routes.
   Значения по умолчанию по документации: порт hybrid, PVID 1, untagged VLAN 1 (до V200R005 — как у образов eNSP);
   trunk пропускает VLAN 1, пока не дано undo port trunk allow-pass vlan 1; STP — MSTP, имя региона = MAC моста (каждый Huawei — свой регион),
   приоритет 32768, стоимость 802.1t (GE — 20000), порты не edge; Eth-Trunk — manual load-balance, LACP — mode lacp (mode lacp-static — старое имя);
   LLDP выключен (до V200R011C10SPC200). Статика — preference 60. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, Vr = EL.vrp, cmd = Vr.cmd, pad = Vr.pad, full = Vr.full;
  function S(st) { return st.vrp.kind === 's'; }
  function C(st) { return st.vrp.c; }
  function top(st) { return Vr.top(st); }
  function cur(st) { return Vr.cur(st); }
  function isPhys(n) { return /^(GE|Eth)\d+\/\d+\/\d+$/.test(n); }
  function curNames(st) { var t = top(st); return t.v === 'if' ? t.names || [t.name] : []; }
  var INFO = 'Info: This operation may take a few seconds. Please wait for a moment...done.';
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i; }).sort(function (x, y) { return x - y; }); }
  function minus(a, b) { return a.filter(function (x) { return b.indexOf(x) < 0; }); }
  // preference VRP → AD модели: сохраняется порядок Huawei (OSPF 10 < static 60 < RIP 100), шкала модели — OSPF 110, RIP 120
  EL.vrp.adOf = function (p) { return p <= 10 ? p * 11 : p <= 100 ? 110 + (p - 10) / 9 : 120 + (p - 100); };
  function sw(st) { return S(st); }
  function only(f) { return function (st) { return sw(st) && f(st); }; }
  function l2(st) { return curNames(st).every(function (n) { return isPhys(n) || /^Eth-Trunk/.test(n); }); }
  function each(st, f) { var bad = false, N = curNames(st); cur(st).forEach(function (x, i) { if (f(x, N[i]) === false) bad = true; }); return bad ? null : undefined; }   // false у одного из портов — ошибка
  function sc(views, pat, run, d) { var e = cmd(views, pat, run, d); e.ok = sw; return e; }

  // ---------------------------------------------------------------- VLAN
  function vl(st) { var c = C(st); return c.vlans || (c.vlans = {}); }
  sc('sys', 'vlan <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return null; if (a[0] !== 1) vl(st)[a[0]] = vl(st)[a[0]] || {}; Vr.push(st, { v: 'vlan', id: a[0] }); }, 'Configure VLAN');
  sc('sys', 'vlan batch <vl>', function (st, a) { a[0].forEach(function (v) { if (v !== 1) vl(st)[v] = vl(st)[v] || {}; }); return INFO; });
  sc('sys', 'undo vlan <n>', function (st, a) { if (a[0] === 1) return null; delete vl(st)[a[0]]; });
  sc('sys', 'undo vlan batch <vl>', function (st, a) { a[0].forEach(function (v) { delete vl(st)[v]; }); return INFO; });
  sc('vlan', 'name <w>', function (st, a) { var t = top(st); if (t.id !== 1) vl(st)[t.id].name = a[0]; });
  sc('vlan', 'description <rest>', function (st, a) { var t = top(st); if (t.id !== 1) vl(st)[t.id].desc = a[0]; });
  // ---------------------------------------------------------------- тип порта и VLAN на порту
  sc('if', 'port link-type <w>', function (st, a) { var t = a[0].toLowerCase(); if (['access', 'trunk', 'hybrid'].indexOf(t) < 0 || !l2(st)) return null;
    return each(st, function (x) { if (x.et) return false; if (x.type !== t) { ['pvid', 'tpvid', 'allow', 'allowAll', 'hpvid', 'htag', 'huntag'].forEach(function (k) { delete x[k]; }); } x.type = t; }); }, 'Set the link type of the port');
  sc('if', 'undo port link-type', function (st) { return each(st, function (x) { ['type', 'pvid', 'tpvid', 'allow', 'allowAll', 'hpvid', 'htag', 'huntag'].forEach(function (k) { delete x[k]; }); }); });
  function need(t, f) { return function (st, a) { return each(st, function (x) { if ((x.type || 'hybrid') !== t) return false; return f(x, a); }); }; }
  sc('if', 'port default vlan <n>', need('access', function (x, a) { if (a[0] < 1 || a[0] > 4094) return false; x.pvid = a[0]; }), 'Set the default VLAN of the port');
  sc('if', 'undo port default vlan', need('access', function (x) { delete x.pvid; }));
  sc('if', 'port trunk allow-pass vlan all', need('trunk', function (x) { x.allowAll = true; }));
  sc('if', 'port trunk allow-pass vlan <vl>', need('trunk', function (x, a) { x.allow = uniq((x.allow || [1]).concat(a[0])); }), 'Allow VLANs on the trunk port');
  sc('if', 'undo port trunk allow-pass vlan all', need('trunk', function (x) { delete x.allowAll; x.allow = []; }));
  sc('if', 'undo port trunk allow-pass vlan <vl>', need('trunk', function (x, a) { x.allow = minus(x.allow || [1], a[0]); if (x.allowAll) { delete x.allowAll; x.allow = minus(range(1, 4094), a[0]); } }));
  sc('if', 'port trunk pvid vlan <n>', need('trunk', function (x, a) { x.tpvid = a[0]; }));
  sc('if', 'undo port trunk pvid vlan', need('trunk', function (x) { delete x.tpvid; }));
  sc('if', 'port hybrid tagged vlan <vl>', need('hybrid', function (x, a) { x.htag = uniq((x.htag || []).concat(a[0])); x.huntag = minus(x.huntag || [1], a[0]); }));
  sc('if', 'port hybrid untagged vlan <vl>', need('hybrid', function (x, a) { x.huntag = uniq((x.huntag || [1]).concat(a[0])); x.htag = minus(x.htag || [], a[0]); }));
  sc('if', 'undo port hybrid vlan <vl>', need('hybrid', function (x, a) { x.htag = minus(x.htag || [], a[0]); x.huntag = minus(x.huntag || [1], a[0]); }));
  sc('if', 'undo port hybrid tagged vlan <vl>', need('hybrid', function (x, a) { x.htag = minus(x.htag || [], a[0]); }));
  sc('if', 'undo port hybrid untagged vlan <vl>', need('hybrid', function (x, a) { x.huntag = minus(x.huntag || [1], a[0]); }));
  sc('if', 'port hybrid pvid vlan <n>', need('hybrid', function (x, a) { x.hpvid = a[0]; }));
  sc('if', 'undo port hybrid pvid vlan', need('hybrid', function (x) { delete x.hpvid; }));
  function range(a, b) { var o = []; for (var i = a; i <= b; i++) o.push(i); return o; }
  // ---------------------------------------------------------------- Vlanif
  sc('if', 'ip address <ip> <mask>', function (st, a) { var n = top(st).name; if (!/^Vlanif/.test(n) || a[1] < 1 || a[1] > 32) return null; cur(st)[0].ip = [a[0], a[1]]; }, 'Configure the IP address of an interface');
  sc('if', 'undo ip address', function (st) { var n = top(st).name; if (!/^Vlanif/.test(n)) return null; delete cur(st)[0].ip; });
  // ---------------------------------------------------------------- STP / RSTP / MSTP
  function stp(st) { var c = C(st); return c.stp || (c.stp = {}); }
  sc('sys', 'stp mode <w>', function (st, a) { var m = a[0].toLowerCase(); if (['stp', 'rstp', 'mstp'].indexOf(m) < 0) return null; stp(st).mode = m; return INFO; }, 'Configure the STP mode');
  sc('sys', 'undo stp mode', function (st) { delete stp(st).mode; return INFO; });
  sc('sys', 'stp enable', function (st) { delete stp(st).off; });
  sc('sys', 'stp disable', function (st) { stp(st).off = true; });
  sc('sys', 'undo stp enable', function (st) { stp(st).off = true; });
  function prio(st, k, p) { if (p > 61440 || p % 4096) return null; var s = stp(st); s.prio = s.prio || {}; s.prio[k] = p; s.root = s.root || {}; delete s.root[k]; }
  sc('sys', 'stp priority <n>', function (st, a) { return prio(st, 0, a[0]); }, 'Set the bridge priority');
  sc('sys', 'stp instance <n> priority <n>', function (st, a) { return prio(st, a[0], a[1]); });
  function root(st, k, w) { w = w.toLowerCase(); if (['primary', 'secondary'].indexOf(w) < 0) return null; var s = stp(st); s.root = s.root || {}; s.root[k] = w; if (s.prio) delete s.prio[k]; }
  sc('sys', 'stp root <w>', function (st, a) { return root(st, 0, a[0]); }, 'Configure the switch as a root bridge');
  sc('sys', 'stp instance <n> root <w>', function (st, a) { return root(st, a[0], a[1]); });
  sc('sys', 'undo stp priority', function (st) { var s = stp(st); if (s.prio) delete s.prio[0]; });
  sc('sys', 'undo stp root', function (st) { var s = stp(st); if (s.root) delete s.root[0]; });
  sc('sys', 'stp region-configuration', function (st) { var s = stp(st); s.reg = s.reg || { inst: {} }; Vr.push(st, { v: 'mst', key: 'mst' }); }, 'Enter MST region view');
  function reg(st) { return stp(st).reg; }
  sc('mst', 'region-name <w>', function (st, a) { reg(st).name = a[0]; });
  sc('mst', 'undo region-name', function (st) { delete reg(st).name; });
  sc('mst', 'revision-level <n>', function (st, a) { if (a[0] > 65535) return null; reg(st).rev = a[0]; });
  sc('mst', 'instance <n> vlan <vl>', function (st, a) { if (a[0] < 1 || a[0] > 48) return null; var R = reg(st).inst;
    Object.keys(R).forEach(function (k) { R[k] = minus(R[k], a[1]); }); R[a[0]] = uniq((R[a[0]] || []).concat(a[1])); });
  sc('mst', 'undo instance <n>', function (st, a) { delete reg(st).inst[a[0]]; });
  sc('mst', 'active region-configuration', function (st) { stp(st).act = EL.clone(reg(st)); return INFO; });
  sc('mst', 'check region-configuration', function (st) { var r = reg(st); return ' Admin configuration\n   Format selector    :0\n   Region name        :' + (r.name || mac(st)) + '\n   Revision level     :' + (r.rev || 0); }).cfg = false;
  function eachP(st, f) { if (!l2(st)) return null; return each(st, f); }
  sc('if', 'stp disable', function (st) { return eachP(st, function (x) { x.stpOff = true; }); });
  sc('if', 'stp enable', function (st) { return eachP(st, function (x) { delete x.stpOff; }); });
  sc('if', 'stp edged-port enable', function (st) { return eachP(st, function (x) { x.edged = true; }); }, 'Configure the port as an edge port');
  sc('if', 'stp edged-port disable', function (st) { return eachP(st, function (x) { delete x.edged; }); });
  sc('if', 'undo stp edged-port', function (st) { return eachP(st, function (x) { delete x.edged; }); });
  sc('if', 'stp cost <n>', function (st, a) { if (a[0] < 1 || a[0] > 200000000) return null; return eachP(st, function (x) { x.cost = a[0]; }); }, 'Set the path cost of the port');
  sc('if', 'stp instance <n> cost <n>', function (st, a) { if (a[1] < 1 || a[1] > 200000000) return null;
    return eachP(st, function (x) { if (a[0] === 0) x.cost = a[1]; else (x.mcost = x.mcost || {})[a[0]] = a[1]; }); });
  sc('if', 'undo stp cost', function (st) { return eachP(st, function (x) { delete x.cost; }); });
  sc('if', 'undo stp instance <n> cost', function (st, a) { return eachP(st, function (x) { if (a[0] === 0) delete x.cost; else if (x.mcost) delete x.mcost[a[0]]; }); });
  // ---------------------------------------------------------------- Eth-Trunk
  function trunkOf(st, n) { return C(st).ifs['Eth-Trunk' + n]; }
  function members(st, n) { var c = C(st); return Object.keys(c.ifs).filter(function (k) { return c.ifs[k].et === n; }); }
  sc('if', 'mode lacp', function (st) { var n = top(st).name; if (!/^Eth-Trunk/.test(n) || members(st, +n.slice(9)).length) return null; cur(st)[0].mode = 'lacp'; }, 'Set the working mode of the Eth-Trunk');
  sc('if', 'mode lacp-static', function (st) { var n = top(st).name; if (!/^Eth-Trunk/.test(n) || members(st, +n.slice(9)).length) return null; cur(st)[0].mode = 'lacp-static'; });
  sc('if', 'mode manual load-balance', function (st) { var n = top(st).name; if (!/^Eth-Trunk/.test(n) || members(st, +n.slice(9)).length) return null; delete cur(st)[0].mode; });
  sc('if', 'undo mode', function (st) { var n = top(st).name; if (!/^Eth-Trunk/.test(n) || members(st, +n.slice(9)).length) return null; delete cur(st)[0].mode; });
  sc('if', 'eth-trunk <n>', function (st, a) { if (!trunkOf(st, a[0]) || !curNames(st).every(isPhys)) return null;
    var r = each(st, function (x) { if (x.type) return false; x.et = a[0]; }); return r === null ? null : INFO; }, 'Add the port to an Eth-Trunk');
  sc('if', 'undo eth-trunk', function (st) { if (!curNames(st).every(isPhys)) return null; each(st, function (x) { delete x.et; delete x.lacpPrio; }); return INFO; });
  function tports(st, rest) {                     // trunkport GE0/0/10 to 0/0/12 | GE0/0/10 GE0/0/11
    var t = rest.split(/\s+/), o = [], ports = st.net ? EL.vrp.dports(st.net, st.net.devs[st.dev]) : [];
    for (var i = 0; i < t.length; i++) { var a = t[i]; if (!isPhys(a)) return null;
      if (t[i + 1] && /^to$/i.test(t[i + 1]) && t[i + 2]) { var b = a.replace(/\d+\/\d+\/\d+$/, '') + t[i + 2].replace(/^[A-Za-z]+/, ''), x = ports.indexOf(a), y = ports.indexOf(b);
        if (x < 0 || y < x) return null; o = o.concat(ports.slice(x, y + 1)); i += 2; } else { if (ports.indexOf(a) < 0) return null; o.push(a); } }
    return o;
  }
  sc('if', 'trunkport <rest>', function (st, a) { var n = top(st).name, L = /^Eth-Trunk/.test(n) && tports(st, a[0]); if (!L) return null;
    L.forEach(function (p) { var x = Vr.ifc(st, p); x.et = +n.slice(9); delete x.type; }); return INFO; });
  sc('if', 'undo trunkport <rest>', function (st, a) { var n = top(st).name, L = /^Eth-Trunk/.test(n) && tports(st, a[0]); if (!L) return null;
    L.forEach(function (p) { var x = Vr.ifc(st, p); if (x.et === +n.slice(9)) delete x.et; }); return INFO; });
  ['max active-linknumber', 'least active-linknumber'].forEach(function (k) {
    sc('if', k + ' <n>', function (st, a) { if (!/^Eth-Trunk/.test(top(st).name) || a[0] < 1 || a[0] > 8) return null; cur(st)[0][k] = a[0]; }); });
  sc('if', 'load-balance <w>', function (st, a) { if (!/^Eth-Trunk/.test(top(st).name)) return null; cur(st)[0].lb = a[0].toLowerCase(); });
  sc('if', 'lacp preempt enable', function (st) { if (!/^Eth-Trunk/.test(top(st).name)) return null; cur(st)[0].preempt = true; });
  sc('if', 'lacp priority <n>', function (st, a) { if (!curNames(st).every(isPhys) || a[0] > 65535) return null; each(st, function (x) { x.lacpPrio = a[0]; }); });
  sc('sys', 'lacp priority <n>', function (st, a) { if (a[0] > 65535) return null; C(st).lacpPrio = a[0]; });
  // ---------------------------------------------------------------- LLDP
  sc('sys', 'lldp enable', function (st) { C(st).lldp = true; });
  sc('sys', 'undo lldp enable', function (st) { var x = st.vrp; x.ask = { yes: function () { delete C(st).lldp; EL.vrp.compile(st); return ''; } };
    return 'Warning: This command will delete the configurations of LLDP on all the ports.Continue?[Y/N]:'; }).cfg = false;

  // ---------------------------------------------------------------- compile: настройки VRP → модель MES
  function port(P, x) {
    var t = x.type || 'hybrid';
    P.shut = !!x.shut; if (x.desc) P.desc = x.desc; else delete P.desc;
    P.mode = t === 'access' ? 'access' : t === 'trunk' ? 'trunk' : 'general';
    P.access = x.pvid || 1;
    P.allowed = x.allow ? x.allow.slice() : [1]; P.allAll = !!x.allowAll;
    var tp = x.tpvid || 1; P.native = t === 'trunk' && (P.allAll || P.allowed.indexOf(tp) >= 0) ? tp : t === 'trunk' ? 0 : 1;
    P.pvid = x.hpvid || 1; P.gtag = (x.htag || []).slice(); P.guntag = (x.huntag || [1]).slice();
    if (x.cost) P.stpCost = x.cost; else delete P.stpCost;
    if (x.mcost) P.mstCost = EL.clone(x.mcost); else delete P.mstCost;
    P.stpOff = !!x.stpOff; P.portfast = !!x.edged; P.noAutoEdge = true;
    return P;
  }
  function mac(st) { var m = String(st.bmac || '').replace(/:/g, ''); return m.slice(0, 4) + '-' + m.slice(4, 8) + '-' + m.slice(8, 12); }
  EL.vrp.compileS = function (st) {
    var c = C(st), net = st.net, d = net && net.devs[st.dev], ports = d ? EL.vrp.dports(net, d) : Object.keys(st.ports);
    st.host = c.sysname || 'Huawei';
    st.vlans = { 1: '-' }; Object.keys(c.vlans || {}).forEach(function (v) { st.vlans[v] = (c.vlans[v].name) || '-'; });
    ports.forEach(function (p) { var x = c.ifs[p] || {}, P = port(st.ports[p] || (st.ports[p] = {}), x);
      if (x.et && c.ifs['Eth-Trunk' + x.et]) P.cg = { id: x.et, mode: c.ifs['Eth-Trunk' + x.et].mode ? 'active' : 'on' }; else delete P.cg; });
    st.pos = {}; st.svi = {}; st.sviShut = {};
    Object.keys(c.ifs).forEach(function (k) { var m;
      if ((m = k.match(/^Eth-Trunk(\d+)$/))) st.pos['po' + m[1]] = port({}, c.ifs[k]);
      if ((m = k.match(/^Vlanif(\d+)$/)) && c.ifs[k].ip) { st.svi[m[1]] = c.ifs[k].ip[0] + '/' + c.ifs[k].ip[1]; if (c.ifs[k].shut) st.sviShut[m[1]] = true; } });
    st.routes = (c.routes || []).map(function (r) { return { net: r.net, nh: r.nh, ad: EL.vrp.adOf(r.pref), pref: r.pref }; }); st.gw = null;
    var s = c.stp || {}, pr = s.prio || {}, rt = s.root || {}, rp = function (k) { return rt[k] === 'primary' ? 0 : rt[k] === 'secondary' ? 4096 : pr[k] !== undefined ? pr[k] : 32768; };
    st.stp = { on: !s.off, mode: { stp: 'stp', rstp: 'rst', mstp: 'mst' }[s.mode || 'mstp'], prio: rp(0) };
    var A = s.act || {}, inst = {};
    Object.keys(A.inst || {}).forEach(function (k) { inst[k] = { vlans: A.inst[k].slice(), prio: rp(+k) }; });
    st.mst = { name: A.name || mac(st), rev: A.rev || 0, inst: inst };   // имя региона по умолчанию — MAC моста (CR j015 → region-name)
  };

  // ---------------------------------------------------------------- display current-configuration (части коммутатора)
  function ifLines(x, n) {
    var o = [], t = x.type;
    if (x.desc) o.push(' description ' + x.desc);
    if (x.shut) o.push(' shutdown');
    if (/^Eth-Trunk/.test(n) && x.mode) o.push(' mode ' + x.mode);
    if (t) o.push(' port link-type ' + t);
    if (t === 'access' && x.pvid && x.pvid !== 1) o.push(' port default vlan ' + x.pvid);
    if (t === 'trunk') { if (x.tpvid) o.push(' port trunk pvid vlan ' + x.tpvid);
      var al = x.allow || [1]; if (al.indexOf(1) < 0 && !x.allowAll) o.push(' undo port trunk allow-pass vlan 1');
      if (x.allowAll) o.push(' port trunk allow-pass vlan 2 to 4094'); else if (minus(al, [1]).length) o.push(' port trunk allow-pass vlan ' + Vr.vlTxt(minus(al, [1]))); }
    if (t === 'hybrid') { if (x.hpvid) o.push(' port hybrid pvid vlan ' + x.hpvid);
      var hu = x.huntag || [1]; if (hu.indexOf(1) < 0) o.push(' undo port hybrid vlan 1');
      if ((x.htag || []).length) o.push(' port hybrid tagged vlan ' + Vr.vlTxt(x.htag)); if (minus(hu, [1]).length) o.push(' port hybrid untagged vlan ' + Vr.vlTxt(minus(hu, [1]))); }
    if (x.ip) o.push(' ip address ' + x.ip[0] + ' ' + IP.len2mask(x.ip[1]));
    ['least active-linknumber', 'max active-linknumber'].forEach(function (k) { if (x[k]) o.push(' ' + k + ' ' + x[k]); });
    if (x.lb) o.push(' load-balance ' + x.lb); if (x.preempt) o.push(' lacp preempt enable');
    if (x.stpOff) o.push(' stp disable'); if (x.edged) o.push(' stp edged-port enable');
    if (x.cost) o.push(' stp instance 0 cost ' + x.cost);
    Object.keys(x.mcost || {}).forEach(function (k) { o.push(' stp instance ' + k + ' cost ' + x.mcost[k]); });
    if (x.et) o.push(' eth-trunk ' + x.et); if (x.lacpPrio) o.push(' lacp priority ' + x.lacpPrio);
    return o;
  }
  EL.vrp.ifLines = ifLines;
  EL.vrp.renderS = function (st) {
    var c = C(st), net = st.net, d = net && net.devs[st.dev], out = [], vs = Object.keys(c.vlans || {}).map(Number);
    if (vs.length) out.push({ h: 'vlan', L: ['vlan batch ' + Vr.vlTxt(vs)] });
    vs.forEach(function (v) { var y = c.vlans[v]; if (y.name || y.desc) out.push({ h: 'vlan ' + v, L: ['vlan ' + v].concat(y.desc ? [' description ' + y.desc] : [], y.name ? [' name ' + y.name] : []) }); });
    var s = c.stp || {}, L = [];
    if (s.off) L.push('stp disable'); if (s.mode) L.push('stp mode ' + s.mode);
    Object.keys(s.root || {}).forEach(function (k) { L.push('stp instance ' + k + ' root ' + s.root[k]); });
    Object.keys(s.prio || {}).forEach(function (k) { L.push('stp instance ' + k + ' priority ' + s.prio[k]); });
    if (c.lacpPrio) L.push('lacp priority ' + c.lacpPrio);
    if (L.length) out.push({ h: 'stp', L: L });
    if (s.reg) { var R = s.reg; out.push({ h: 'mst', L: ['stp region-configuration'].concat(R.name ? [' region-name ' + R.name] : [], R.rev ? [' revision-level ' + R.rev] : [],
      Object.keys(R.inst).map(function (k) { return ' instance ' + k + ' vlan ' + Vr.vlTxt(R.inst[k]); }), s.act ? [' active region-configuration'] : []) }); }
    if (c.lldp) out.push({ h: 'lldp', L: ['lldp enable'] });
    var ks = Object.keys(c.ifs), byN = function (re) { return ks.filter(function (k) { return re.test(k); }).sort(function (a, b) { return +a.replace(/\D/g, '') - +b.replace(/\D/g, ''); }); };
    byN(/^Vlanif/).concat(byN(/^Eth-Trunk/)).concat(d ? EL.vrp.dports(net, d) : []).forEach(function (k) {
      out.push({ h: 'interface ' + full(k), L: ['interface ' + full(k)].concat(ifLines(c.ifs[k] || {}, k)) }); });
    out.push({ h: 'interface NULL0', L: ['interface NULL0'] });
    if ((c.routes || []).length) out.push({ h: 'route', L: c.routes.map(function (r) { var p = r.net.split('/');
      return 'ip route-static ' + p[0] + ' ' + IP.len2mask(+p[1]) + ' ' + r.nh + (r.pref !== 60 ? ' preference ' + r.pref : ''); }) });
    return out;
  };

  // ---------------------------------------------------------------- display (коммутатор)
  function lname(n) { return /^po\d+$/.test(n) ? 'Eth-Trunk' + n.slice(2) : n; }
  function upTxt(st, L) { return L.members && L.members.length && Vr.phyUp(st, L.members[0]) ? 'U' : 'D'; }
  function inVlan(cfg, v) { if (cfg.mode === 'access') return cfg.access === v ? 'UT' : null;
    if (cfg.mode === 'trunk') return cfg.native === v ? 'UT' : cfg.allAll || cfg.allowed.indexOf(v) >= 0 ? 'TG' : null;
    return cfg.guntag.indexOf(v) >= 0 ? 'UT' : cfg.gtag.indexOf(v) >= 0 ? 'TG' : null; }
  function allL(st) { var net = st.net, d = net.devs[st.dev], o = [];
    EL.vrp.dports(net, d).forEach(function (p) { var P = st.ports[p]; if (!P.cg) o.push({ name: p, cfg: P, members: [p] }); });
    Object.keys(st.pos).forEach(function (k) { var L = net.lports(st.dev).filter(function (x) { return x.name === k; })[0]; o.push({ name: k, cfg: st.pos[k], members: L ? L.members : [] }); });
    return o; }
  sc('*', 'display vlan', function (st) {
    if (!st.net) return ''; var vs = Object.keys(st.vlans).map(Number).sort(function (a, b) { return a - b; }), Ls = allL(st);
    var o = ['The total number of VLANs is : ' + vs.length, new Array(81).join('-'), 'U: Up;         D: Down;         TG: Tagged;         UT: Untagged;',
      'MP: Vlan-mapping;               ST: Vlan-stacking;', '#: ProtocolTransparent-vlan;    *: Management-vlan;', new Array(81).join('-'), '', 'VID  Type    Ports', new Array(81).join('-')];
    vs.forEach(function (v) { var first = true;
      ['UT', 'TG'].forEach(function (k) { var ps = Ls.filter(function (L) { return inVlan(L.cfg, v) === k; }).map(function (L) { return Vr.short(full(lname(L.name))) + '(' + upTxt(st, L) + ')'; });
        for (var i = 0; i < ps.length; i += 4) { var row = ps.slice(i, i + 4).map(function (p, j) { return pad((i === 0 && j === 0 ? k + ':' : '') + p, 19); }).join('').replace(/\s+$/, '');
          o.push((first ? pad(v, 5) + pad('common', 8) : new Array(14).join(' ') + (i === 0 ? '' : '   ')) + row); first = false; } });
      if (first) o.push(pad(v, 5) + 'common'); });
    o.push('', 'VID  Status  Property      MAC-LRN Statistics Description', new Array(81).join('-'));
    vs.forEach(function (v) { o.push(pad(v, 5) + pad('enable', 8) + pad('default', 14) + pad('enable', 8) + pad('disable', 11) + 'VLAN ' + ('000' + v).slice(-4)); });
    return o.join('\n');
  });
  sc('*', 'display port vlan', function (st) {
    if (!st.net) return ''; var o = ['Port                    Link Type    PVID  Trunk VLAN List', new Array(80).join('-')], c = C(st);
    EL.vrp.dports(st.net, st.net.devs[st.dev]).concat(Object.keys(st.pos)).forEach(function (p) {
      var P = st.ports[p] || st.pos[p], x = c.ifs[/^po/.test(p) ? lname(p) : p] || {}, mem = st.ports[p] && P.cg;
      var t = mem ? '-' : x.type || 'hybrid', pv = mem ? 0 : t === 'access' ? P.access : t === 'trunk' ? (x.tpvid || 1) : P.pvid;
      var tl = t === 'trunk' ? (P.allAll ? '1-4094' : Vr.vlTxt(P.allowed).replace(/ to /g, '-')) || '-' : '-';
      o.push(pad(full(lname(p)), 24) + pad(t, 13) + pad(pv, 6) + tl); });
    return o.join('\n');
  });
  var ROLE = { Root: 'ROOT', Desg: 'DESI', Altn: 'ALTE', Back: 'BACK' }, STATE = { Frw: 'FORWARDING', Lrn: 'LEARNING', Dsc: 'DISCARDING', Blk: 'DISCARDING', Lsn: 'DISCARDING' };
  function insts(st) { return st.stp.mode === 'mst' ? [0].concat(Object.keys(st.mst.inst).map(Number)) : [0]; }
  sc('*', 'display stp brief', function (st) {
    var net = st.net; if (!net || !st.stp.on) return ''; var o = [' MSTID   Port                        Role  STP State     Protection'];
    insts(st).forEach(function (k) { var t = net.stp(k)[st.dev] || {};
      net.lports(st.dev).forEach(function (L) { var r = t[L.name]; if (!r || r.nostp) return;
        o.push('    ' + pad(k, 5) + pad(full(lname(L.name)), 28) + pad(ROLE[r.role] || 'DESI', 6) + pad(STATE[net.stpSts(st.dev, L.name, k)] || 'FORWARDING', 16) + 'NONE'); }); });
    return o.join('\n');
  }, 'Display STP brief information');
  function bidTxt(p, m) { return pad(p, 5) + '.' + m; }
  sc('*', 'display stp', function (st) {
    var net = st.net; if (!net) return '';
    if (!st.stp.on) return ' Protocol Status       :Disabled\n Protocol Standard     :IEEE 802.1s\n Version               :3\n CIST Bridge Priority  :' + st.stp.prio + '\n MAC address           :' + mac(st) +
      '\n Max age(s)            :20\n Forward delay(s)      :15\n Hello time(s)         :2\n Max hops              :20';
    var t = net.stp(0)[st.dev] || {}, R = net._stp.root[st.dev], rs = net.devs[R].st, rm = EL.vrp.isVrp(net.devs[R]) ? mac(rs) : macOf(rs), dist = net._stp.dist[st.dev];
    var rpL = Object.keys(t).filter(function (k) { return t[k].role === 'Root'; })[0], c = C(st), s = c.stp || {};
    var o = ['-------[CIST Global Info][Mode ' + { stp: 'STP', rst: 'RSTP', mst: 'MSTP' }[st.stp.mode] + ']-------', 'CIST Bridge         :' + bidTxt(st.stp.prio, mac(st)),
      'Config Times        :Hello 2s MaxAge 20s FwDly 15s MaxHop 20', 'Active Times        :Hello 2s MaxAge 20s FwDly 15s MaxHop 20',
      'CIST Root/ERPC      :' + bidTxt((rs.stp || {}).prio, rm) + ' / ' + dist + (R === st.dev ? ' (This bridge is the root)' : ''),
      'CIST RegRoot/IRPC   :' + bidTxt(st.stp.prio, mac(st)) + ' / 0', 'CIST RootPortId     :' + (rpL ? '128.' + portNo(st, rpL) : '0.0'), 'BPDU-Protection     :Disabled'];
    if ((s.root || {})[0]) o.push('CIST Root Type      :' + (s.root[0] === 'primary' ? 'Primary root' : 'Secondary root'));
    o.push('TC or TCN received  :0', 'TC count per hello  :0', 'STP Converge Mode   :Normal', 'Time since last TC  :0 days 0h:0m:0s', 'Number of TC        :0');
    net.lports(st.dev).forEach(function (L) { var r = t[L.name]; if (!r || r.nostp) return; var P = L.cfg || {};
      o.push('', '----[Port' + portNo(st, L.name) + '(' + full(lname(L.name)) + ')][' + (STATE[net.stpSts(st.dev, L.name, 0)] || 'FORWARDING') + ']----',
        ' Port Protocol       :Enabled', ' Port Role           :' + { ROOT: 'Root Port', DESI: 'Designated Port', ALTE: 'Alternate Port', BACK: 'Backup Port' }[ROLE[r.role] || 'DESI'],
        ' Port Priority       :128', ' Port Cost(Dot1T)    :Config=' + (P.stpCost || 'auto') + ' / Active=' + (P.stpCost || (/^po/.test(L.name) ? 10000 : 20000)),
        ' Port Edged          :Config=' + (P.portfast ? 'enabled' : 'disabled') + ' / Active=' + (P.portfast ? 'enabled' : 'disabled'), ' Point-to-point      :Config=auto / Active=true',
        ' Port STP Mode       :' + { stp: 'STP', rst: 'RSTP', mst: 'MSTP' }[st.stp.mode]); });
    return o.join('\n');
  });
  function macOf(s) { var m = String(s.bmac || '').replace(/:/g, ''); return m.slice(0, 4) + '-' + m.slice(4, 8) + '-' + m.slice(8, 12); }
  function portNo(st, n) { if (/^po/.test(n)) return 1000 + +n.slice(2); var L = EL.vrp.dports(st.net, st.net.devs[st.dev]); return L.indexOf(n) + 1; }
  sc('*', 'display stp region-configuration', function (st) {
    var m = st.mst, o = ['Oper configuration', '   Format selector :0', '   Region name     :' + m.name, '   Revision level  :' + m.rev, '', '   Instance   VLANs Mapped'];
    var used = []; Object.keys(m.inst).forEach(function (k) { used = used.concat(m.inst[k].vlans); });
    var rest = minus(range(1, 4094), used); o.push('      0       ' + Vr.vlTxt(rest));
    Object.keys(m.inst).forEach(function (k) { o.push('      ' + pad(k, 8) + Vr.vlTxt(m.inst[k].vlans)); });
    return o.join('\n');
  });
  sc('*', 'display eth-trunk', function (st) { return Object.keys(st.pos).map(function (k) { return etText(st, +k.slice(2)); }).join('\n\n'); });
  sc('*', 'display eth-trunk <n>', function (st, a) { return st.pos['po' + a[0]] ? etText(st, a[0]) : ''; });
  function etText(st, n) {
    var net = st.net, x = C(st).ifs['Eth-Trunk' + n] || {}, mem = members(st, n), L = net.lports(st.dev).filter(function (q) { return q.name === 'po' + n; })[0] || { members: [] };
    var up = mem.filter(function (p) { return L.members.indexOf(p) >= 0; }), least = x['least active-linknumber'] || 1, opUp = up.length >= least && up.length > 0;
    if (!x.mode) return ['Eth-Trunk' + n + '\'s state information is:', 'WorkingMode: NORMAL          Hash arithmetic: According to SIP-XOR-DIP',
      'Least Active-linknumber: ' + least + '         Max Bandwidth-affected-linknumber: 8', 'Operate status: ' + (opUp ? 'up' : 'down') + '                Number Of Up Port In Trunk: ' + (opUp ? up.length : 0),
      new Array(81).join('-'), 'PortName                      Status      Weight'].concat(mem.map(function (p) { return pad(full(p), 33) + pad(up.indexOf(p) >= 0 ? 'Up' : 'Down', 12) + '1'; })).join('\n');
    var sp = C(st).lacpPrio || 32768, o = ['Eth-Trunk' + n + '\'s state information is:', 'Local:', 'LAG ID: ' + pad(n, 22) + 'WorkingMode: LACP', 'Preempt Delay: ' + pad(x.preempt ? 'Enabled' : 'Disabled', 15) + 'Hash arithmetic: According to SIP-XOR-DIP',
      'System Priority: ' + pad(sp, 13) + 'System ID: ' + mac(st), 'Least Active-linknumber: ' + pad(least, 5) + 'Max Active-linknumber: ' + (x['max active-linknumber'] || 8),
      'Operate status: ' + pad(opUp ? 'up' : 'down', 14) + 'Number Of Up Port In Trunk: ' + (opUp ? up.length : 0), new Array(81).join('-'),
      'ActorPortName          Status   PortType  PortPri PortNo PortKey PortState Weight'];
    mem.forEach(function (p) { var sel = up.indexOf(p) >= 0; o.push(pad(full(p), 24) + pad(sel ? 'Selected' : 'Unselect', 10) + pad(/^Eth/.test(p) ? '100M' : '1GE', 10) + pad((C(st).ifs[p] || {}).lacpPrio || 32768, 8) +
      pad(portNo(st, p) + 1, 7) + pad(305, 8) + pad(sel ? '10111100' : '10100000', 10) + '1'); });
    o.push('', 'Partner:', new Array(81).join('-'), 'ActorPortName          SysPri     SystemID        PortPri  PortNo PortKey   PortState');
    mem.forEach(function (p) { var pr = net.peer(st.dev, p), sel = up.indexOf(p) >= 0, pd = pr && net.devs[pr.dev];
      o.push(pad(full(p), 24) + (sel && pd ? pad(EL.vrp.isVrp(pd) ? (pd.st.vrp.c.lacpPrio || 32768) : 32768, 11) + pad(EL.vrp.isVrp(pd) ? mac(pd.st) : macOf(pd.st), 16) + pad(32768, 9) + pad(net.portsOf(pd).indexOf(pr.port) + 2, 7) + pad(305, 10) + '10111100'
        : pad(0, 11) + pad('0000-0000-0000', 16) + pad(0, 9) + pad(0, 7) + pad(0, 10) + '10100011')); });
    return o.join('\n');
  }
  sc('*', 'display mac-address', function (st) {
    var net = st.net; if (!net) return ''; var T = net.mac[st.dev] || {}, ks = Object.keys(T), line = new Array(80).join('-');
    var o = [line, 'MAC Address          VLAN/VSI/BD                 Learned-From        Type', line];
    ks.forEach(function (k) { var e = T[k], m = String(e.mac).replace(/:/g, ''); o.push(pad(m.slice(0, 4) + '-' + m.slice(4, 8) + '-' + m.slice(8, 12), 21) + pad(e.vlan + '/-/-', 28) + pad(Vr.short(full(lname(e.port))), 20) + (e.st ? 'static' : 'dynamic')); });
    o.push(line, 'Total items displayed = ' + ks.length);
    return o.join('\n');
  });
  sc('*', 'display lldp neighbor brief', function (st) {
    var net = st.net; if (!net || !C(st).lldp) return ''; var o = ['Local Intf   Neighbor Dev             Neighbor Intf             Exptime(s)'];
    EL.vrp.dports(net, net.devs[st.dev]).forEach(function (p) { var pr = net.peer(st.dev, p); if (!pr || !net.linkUp(st.dev, p)) return; var pd = net.devs[pr.dev];
      if (pd.type !== 'mes' && pd.type !== 'esr' || EL.vrp.isVrp(pd) && !pd.st.vrp.c.lldp) return;
      var h = pd.type === 'esr' ? pd.st.run.host : pd.st.host; o.push(pad(Vr.short(p), 13) + pad(h, 25) + pad(Vr.short(pr.port), 26) + (90 + ((net.now || 0) % 30 | 0))); });
    return o.join('\n');
  });
})(typeof window !== 'undefined' ? window : global);
