/* D-Link «старый» CLI (DES-3200-28, DGS-3000-28) — спецификация sources/dlink/spec/dlink-legacy.md (CLI Reference DES-3200 R4.04, DGS-3000 R4.00).
   Плоский CLI без режимов, приглашение «DES-3200-28:admin#»; каждая команда эхом печатает «Command: …» (маска в префиксе), затем «Success.»;
   неизвестная команда — «Available commands:» со списком верхнего уровня; неполная — «Next possible completions:».
   Коммутатор — тип 'mes' модели: VLAN D-Link (tagged / untagged / forbidden по VLAN + PVID порта) → порты в режиме general (как hybrid).
   По документации: заводской IP 10.90.90.90/8 на интерфейсе System (VLAN default), все порты untagged в default, STP выключен,
   логина нет (UserName/PassWord — Enter), save — «Saving all configurations to NV-RAM.......... Done.».
   Допущения (в отчёте): add untagged переносит PVID порта в эту VLAN (enable pvid auto_assign; подробностей поведения в источниках нет),
   версия STP после enable stp — RSTP (в источниках не названа), режим lacp_port по умолчанию — passive. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip;
  var GROUP = 'D-Link';
  function range(a, b) { var o = []; for (var i = a; i <= b; i++) o.push(String(i)); return o; }
  [['DES-3200-28', 28, 'Fast Ethernet Switch', '4.04.004', 'Коммутатор D-Link DES-3200-28 (старый CLI): порты 1–24 Fast Ethernet + 25–28 Gigabit, IP 10.90.90.90/8'],
   ['DGS-3000-28SC', 28, 'Gigabit Ethernet Switch', '4.00.010', 'Коммутатор D-Link DGS-3000-28SC (старый CLI): порты 1–28, IP 10.90.90.90/8']
  ].forEach(function (x) { EL.MODELS[x[0]] = { type: 'mes', kind: 'dl-legacy', portList: range(1, x[1]), ports: x[1], group: GROUP, vendor: 'dlink', host: x[0], banner: x[2], fw: x[3], note: x[4],
    login: [{ u: '—', p: '—', a: 'UserName/PassWord пустые — Enter (заводской), IP 10.90.90.90/8' }] }; });
  function isDl(d) { return !!d && d.sub === 'dlegacy'; }
  function D(st) { return st.dl; }
  function C(st) { return st.dl.c; }
  function host(st) { var d = st.net && st.net.devs[st.dev]; return d ? d.model : 'DES-3200-28'; }
  function prompt(st) { var x = D(st); if (x.ask) return x.ask.pr; return (C(st).prompt || host(st)) + ':admin#'; }
  var TOP = '..  ?  cable_diag  cd  cfm  clear  config  copy  create  debug  del  delete  dir  disable  download  enable  erase  login  logout  md  move  no  ping  ping6  rd  reboot  reconfig  rename  reset  save  show  smtp  telnet  traceroute  traceroute6  upload';
  function plist(s, max) { var o = [], ok = true; String(s).split(',').forEach(function (p) { var m = p.match(/^(\d+)(?:-(\d+))?$/); if (!m) { ok = false; return; }
    for (var i = +m[1]; i <= +(m[2] || m[1]); i++) { if (i < 1 || i > max) ok = false; o.push(String(i)); } }); return ok ? o : null; }
  function ptxt(a) { a = a.map(Number).sort(function (x, y) { return x - y; }).filter(function (x, i, s) { return s.indexOf(x) === i; }); var r = [], i = 0;
    while (i < a.length) { var j = i; while (j + 1 < a.length && a[j + 1] === a[j] + 1) j++; r.push(j > i ? a[i] + '-' + a[j] : '' + a[i]); i = j + 1; } return r.join(','); }
  function ok(cmd, out) { return 'Command: ' + cmd + '\n\n' + (out === undefined ? 'Success.' : out); }
  function nports(st) { var d = st.net && st.net.devs[st.dev]; return d ? EL.MODELS[d.model].ports : 28; }
  function vlans(st) { return C(st).vlans; }
  function vByName(st, n) { var V = vlans(st); return Object.keys(V).filter(function (k) { return V[k].name === n; })[0] || null; }

  // ---------------------------------------------------------------- команды (шаблон → обработчик); <name>, <n>, <ports>, <ip>, <cidr>
  var T = [];
  function cmd(pat, run) { T.push({ p: pat.split(' '), run: run }); }
  function tokOk(p, t) { if (p === '<name>') return /^[\w.-]{1,32}$/.test(t); if (p === '<n>') return /^\d+$/.test(t); if (p === '<ports>') return /^[\d,\-]+$/.test(t) || t === 'all';
    if (p === '<ip>') return IP.ip2n(t) !== null; if (p === '<cidr>') return /^\d+\.\d+\.\d+\.\d+\/(\d+|\d+\.\d+\.\d+\.\d+)$/.test(t); return t === p; }
  cmd('create vlan <name> tag <n>', function (st, a, raw) { if (a[1] < 2 || a[1] > 4094 || vlans(st)[a[1]] || vByName(st, a[0])) return null; vlans(st)[a[1]] = { name: a[0], t: [], u: [], f: [] }; return ok(raw); });
  cmd('create vlan <name> tag <n> type 1q_vlan advertisement', function (st, a, raw) { if (a[1] < 2 || a[1] > 4094 || vlans(st)[a[1]]) return null; vlans(st)[a[1]] = { name: a[0], t: [], u: [], f: [] }; return ok(raw); });
  cmd('delete vlan <name>', function (st, a, raw) { var v = vByName(st, a[0]); if (!v || v === '1') return null; delete vlans(st)[v]; return ok(raw); });
  function member(st, vs, kind, ps, raw) {
    if (!vs.length || !ps) return null;
    vs.forEach(function (v) { var V = vlans(st)[v]; ['t', 'u', 'f'].forEach(function (k) { V[k] = V[k].filter(function (p) { return ps.indexOf(p) < 0; }); });
      if (kind !== 'delete') V[kind.charAt(0)] = V[kind.charAt(0)].concat(ps);
      if (kind === 'untagged') ps.forEach(function (p) { C(st).pvid[p] = +v; });                 // enable pvid auto_assign (допущение)
      if (kind === 'delete') ps.forEach(function (p) { if (C(st).pvid[p] === +v) C(st).pvid[p] = 1; }); });
    return ok(raw);
  }
  ['tagged', 'untagged', 'forbidden'].forEach(function (k) {
    cmd('config vlan <name> add ' + k + ' <ports>', function (st, a, raw) { var v = vByName(st, a[0]); return v ? member(st, [v], k, a[1] === 'all' ? range(1, nports(st)) : plist(a[1], nports(st)), raw) : null; });
    cmd('config vlan vlanid <ports> add ' + k + ' <ports>', function (st, a, raw) { var vs = (plist(a[0], 4094) || []).filter(function (v) { return vlans(st)[v]; }); return member(st, vs, k, a[1] === 'all' ? range(1, nports(st)) : plist(a[1], nports(st)), raw); }); });
  cmd('config vlan <name> delete <ports>', function (st, a, raw) { var v = vByName(st, a[0]); return v ? member(st, [v], 'delete', a[1] === 'all' ? range(1, nports(st)) : plist(a[1], nports(st)), raw) : null; });
  cmd('config vlan vlanid <ports> delete <ports>', function (st, a, raw) { var vs = (plist(a[0], 4094) || []).filter(function (v) { return vlans(st)[v]; }); return member(st, vs, 'delete', plist(a[1], nports(st)), raw); });
  cmd('config ipif System ipaddress <cidr>', function (st, a, raw) { var p = a[0].split('/'), l = /\./.test(p[1]) ? IP.mask2len(p[1]) : +p[1]; if (l === null || l > 32 || IP.ip2n(p[0]) === null) return null;
    C(st).ip = [p[0], l]; return ok(raw.replace(a[0], p[0] + '/' + l)); });
  cmd('config ipif System vlan <name>', function (st, a, raw) { var v = vByName(st, a[0]); if (!v) return null; C(st).ipVlan = +v; return ok(raw); });
  cmd('create iproute default <ip>', function (st, a, raw) { C(st).gw = a[0]; return ok(raw); });
  cmd('delete iproute default', function (st, a, raw) { delete C(st).gw; return ok(raw); });
  cmd('enable stp', function (st, a, raw) { C(st).stp = true; return ok(raw); });
  cmd('disable stp', function (st, a, raw) { C(st).stp = false; return ok(raw); });
  cmd('config stp version <name>', function (st, a, raw) { if (['mstp', 'rstp', 'stp'].indexOf(a[0]) < 0) return null; if (C(st).stpVer === a[0]) return ok(raw, 'Configure value is the same with current value.\nSuccess.'); C(st).stpVer = a[0]; return ok(raw); });
  cmd('config stp priority <n> instance_id 0', function (st, a, raw) { if (a[0] > 61440 || a[0] % 4096) return null; C(st).stpPrio = a[0]; return ok(raw); });
  cmd('config stp ports <ports> edge <name>', function (st, a, raw) { var ps = plist(a[0], nports(st)); if (!ps || ['true', 'false', 'auto'].indexOf(a[1]) < 0) return null; ps.forEach(function (p) { C(st).edge[p] = a[1]; }); return ok(raw); });
  cmd('create link_aggregation group_id <n>', function (st, a, raw) { C(st).lag[a[0]] = { type: 'static', ports: [] }; return ok(raw); });
  cmd('create link_aggregation group_id <n> type <name>', function (st, a, raw) { if (['lacp', 'static'].indexOf(a[1]) < 0) return null; C(st).lag[a[0]] = { type: a[1], ports: [] }; return ok(raw); });
  cmd('config link_aggregation group_id <n> master_port <n> ports <ports>', function (st, a, raw) { var g = C(st).lag[a[0]], ps = plist(a[2], nports(st)); if (!g || !ps || ps.indexOf(String(a[1])) < 0) return null;
    g.master = String(a[1]); g.ports = ps; return ok(raw); });
  cmd('delete link_aggregation group_id <n>', function (st, a, raw) { if (!C(st).lag[a[0]]) return null; delete C(st).lag[a[0]]; return ok(raw); });
  cmd('config lacp_port <ports> mode <name>', function (st, a, raw) { var ps = plist(a[0], nports(st)); if (!ps || ['active', 'passive'].indexOf(a[1]) < 0) return null; ps.forEach(function (p) { C(st).lacp[p] = a[1]; }); return ok(raw); });
  cmd('config ports <ports> state <name>', function (st, a, raw) { var ps = a[0] === 'all' ? range(1, nports(st)) : plist(a[0], nports(st)); if (!ps || ['enable', 'disable'].indexOf(a[1]) < 0) return null;
    ps.forEach(function (p) { C(st).off[p] = a[1] === 'disable'; }); return ok(raw); });
  cmd('enable lldp', function (st, a, raw) { C(st).lldp = true; return ok(raw); });
  cmd('disable lldp', function (st, a, raw) { C(st).lldp = false; return ok(raw); });
  cmd('config command_prompt <name>', function (st, a, raw) { C(st).prompt = a[0]; return ok(raw); });
  cmd('config command_prompt default', function (st, a, raw) { delete C(st).prompt; return ok(raw); });
  cmd('save', function (st, a, raw) { D(st).saved = EL.clone(C(st)); return ok(raw, 'Saving all configurations to NV-RAM.......... Done.'); });
  cmd('save config', function (st, a, raw) { D(st).saved = EL.clone(C(st)); return ok(raw, 'Saving all configurations to NV-RAM.......... Done.'); });
  cmd('reboot', function (st) { D(st).ask = { pr: '', fn: function (s) { if (!/^y/i.test(s)) return ''; if (st.net) st.net.reboot(st.dev); return 'Please wait, the switch is rebooting...'; } };
    return 'Command: reboot\nAre you sure to proceed with the system reboot?(y/n)'; });
  cmd('ping <ip>', function (st, a) { return pingT(st, a[0], 4); });
  cmd('ping <ip> times <n>', function (st, a) { return pingT(st, a[0], Math.min(a[1], 20)); });
  cmd('logout', function () { return '**********\n* Logout *\n**********'; });
  // show
  cmd('show vlan', function (st, a, raw) { return ok(raw, showVlan(st)); });
  cmd('show switch', function (st, a, raw) { var c = C(st), m = EL.MODELS[host(st)], mac = macD(st);
    return ok(raw, ['Device Type        : ' + host(st) + ' ' + m.banner, 'MAC Address        : ' + mac, 'IP Address         : ' + c.ip[0] + ' (Manual)', 'VLAN Name          : ' + vlans(st)[c.ipVlan || 1].name,
      'Subnet Mask        : ' + IP.len2mask(c.ip[1]), 'Default Gateway    : ' + (c.gw || '0.0.0.0'), 'Firmware Version   : Build ' + m.fw, 'System Name        :',
      'System Uptime      : 0 days, 0 hours, ' + Math.floor(((st.net && st.net.now) || 0) / 60) + ' minutes, 0 seconds', 'Spanning Tree      : ' + (c.stp ? 'Enabled' : 'Disabled'),
      'GVRP               : Disabled', 'IGMP Snooping      : Disabled', 'VLAN Trunk         : Disabled', 'Telnet             : Enabled (TCP 23)', 'Web                : Enabled (TCP 80)', 'SNMP               : Disabled'].join('\n')); });
  cmd('show ipif', function (st, a, raw) { var c = C(st); return ok(raw, ['IP Interface             : System', 'VLAN Name                : ' + vlans(st)[c.ipVlan || 1].name, 'Interface Admin State    : Enabled',
    'Link Status              : ' + (st.net && st.net.ifaces(st.dev).length ? 'LinkUp' : 'LinkDown'), 'IPv4 Address             : ' + c.ip[0] + '/' + c.ip[1] + ' (Manual)', 'IPv4 State               : Enabled', '', 'Total Entries: 1'].join('\n')); });
  cmd('show iproute', function (st, a, raw) { var c = C(st), o = ['Routing Table', '', 'IP Address/Netmask  Gateway          Interface     Cost      Protocol', '------------------  ---------------  ------------  --------  --------'], n = 1;
    if (c.gw) { o.push(pad('0.0.0.0/0', 20) + pad(c.gw, 17) + pad('System', 14) + pad(1, 10) + 'Default'); n++; }
    o.push(pad(IP.netOf(c.ip[0], c.ip[1]), 20) + pad('0.0.0.0', 17) + pad('System', 14) + pad(1, 10) + 'Local', '', 'Total Entries : ' + n); return ok(raw, o.join('\n')); });
  cmd('show stp', function (st, a, raw) { var c = C(st); return ok(raw, ['STP Bridge Global Settings', '---------------------------', 'STP Status        : ' + (c.stp ? 'Enabled' : 'Disabled'),
    'STP Version       : ' + (c.stpVer || 'rstp').toUpperCase(), 'Max Age           : 20', 'Hello Time        : 2', 'Forward Delay     : 15', 'Max Hops          : 20', 'TX Hold Count     : 6', 'Forwarding BPDU   : Disabled'].join('\n')); });
  cmd('show link_aggregation', function (st, a, raw) { var c = C(st), net = st.net, L = net ? net.lports(st.dev) : [], ks = Object.keys(c.lag), o = ['Link Aggregation Algorithm = MAC-Source-Dest'];
    ks.forEach(function (k) { var g = c.lag[k], lp = L.filter(function (x) { return x.name === 'po' + k; })[0];
      o.push('Group ID      : ' + k, 'Type          : ' + (g.type === 'lacp' ? 'LACP' : 'Static'), 'Master Port   : ' + (g.master || ''), 'Member Port   : ' + ptxt(g.ports), 'Active Port   : ' + ptxt(lp ? lp.members : []),
        'Status        : Enabled', 'Flooding Port : ' + (lp && lp.members.length ? lp.members[0] : ''), ''); });
    o.push('Total Entries : ' + ks.length); return ok(raw, o.join('\n')); });
  cmd('show ports', function (st, a, raw) { var net = st.net, o = [' Port   State/          Settings             Connection           Address', '        MDIX            Speed/Duplex/FlowCtrl Speed/Duplex/FlowCtrl Learning',
    ' -----  --------        ---------------------  ---------------------  --------'];
    range(1, nports(st)).forEach(function (p) { var up = net && net.linkUp(st.dev, p); o.push(' ' + pad(p, 6) + pad(C(st).off[p] ? 'Disabled' : 'Enabled', 16) + pad('Auto/Disabled', 23) + pad(up ? (+p > 24 ? '1000M/Full/None' : '100M/Full/None') : 'Link Down', 23) + 'Enabled'); });
    return ok(raw, o.join('\n')); });
  cmd('show fdb', function (st, a, raw) { var net = st.net, T0 = (net && net.mac[st.dev]) || {}, ks = Object.keys(T0), o = ['Unicast MAC Address Aging Time  = 300', '',
    'VID  VLAN Name                        MAC Address        Port  Type     Status', '---- -------------------------------- ----------------- ----- -------- -------'];
    ks.forEach(function (k) { var e = T0[k]; o.push(pad(e.vlan, 5) + pad((vlans(st)[e.vlan] || {}).name || '', 33) + pad(String(e.mac).toUpperCase().replace(/:/g, '-'), 18) + pad(e.port, 6) + pad('Dynamic', 9) + 'Forward'); });
    o.push('', 'Total Entries: ' + ks.length); return ok(raw, o.join('\n')); });
  cmd('show config current_config', function (st, a, raw) { return ok(raw, cfg(st)); });
  function pad(s, n) { s = String(s); return s.length >= n ? s + ' ' : (s + new Array(n + 1).join(' ')).slice(0, n); }
  function macD(st) { return String(st.bmac || '').toUpperCase().replace(/:/g, '-'); }
  function showVlan(st) { var V = vlans(st), o = [];
    Object.keys(V).map(Number).sort(function (x, y) { return x - y; }).forEach(function (v) { var x = V[v], mem = x.t.concat(x.u);
      o.push('VID              :' + pad(v, 18) + 'VLAN Name      : ' + x.name, 'VLAN Type        : Static           Advertisement : Enabled', 'Member Ports : ' + ptxt(mem), 'Static Ports : ' + ptxt(mem),
        'Current Tagged Ports : ' + ptxt(x.t), 'Current Untagged Ports: ' + ptxt(x.u), 'Static Tagged Ports : ' + ptxt(x.t), 'Static Untagged Ports : ' + ptxt(x.u), 'Forbidden Ports      : ' + ptxt(x.f), ''); });
    o.push('Total Entries : ' + Object.keys(V).length); return o.join('\n'); }
  function cfg(st) { var c = C(st), m = EL.MODELS[host(st)], o = ['#-------------------------------------------------------------------------------', '#         ' + host(st) + ' ' + m.banner, '#                           Configuration', '#',
    '#                           Firmware: Build ' + m.fw, '#         Copyright(C) 2012 D-Link Corporation. All rights reserved.', '#-------------------------------------------------------------------------------', '', '# VLAN', ''];
    Object.keys(c.vlans).map(Number).sort(function (x, y) { return x - y; }).forEach(function (v) { var x = c.vlans[v]; if (v !== 1) o.push('create vlan ' + x.name + ' tag ' + v);
      if (v === 1 && x.u.length < nports(st)) o.push('config vlan default delete ' + ptxt(range(1, nports(st)).filter(function (p) { return x.u.indexOf(p) < 0 && x.t.indexOf(p) < 0; })));
      if (v !== 1 && x.t.length) o.push('config vlan ' + x.name + ' add tagged ' + ptxt(x.t)); if (v !== 1 && x.u.length) o.push('config vlan ' + x.name + ' add untagged ' + ptxt(x.u)); });
    o.push('', '# STP', '', (c.stp ? 'enable' : 'disable') + ' stp'); if (c.stpVer) o.push('config stp version ' + c.stpVer);
    Object.keys(c.lag).forEach(function (k) { var g = c.lag[k]; o.push('create link_aggregation group_id ' + k + ' type ' + g.type); if (g.master) o.push('config link_aggregation group_id ' + k + ' master_port ' + g.master + ' ports ' + ptxt(g.ports)); });
    o.push('', '# BASIC', '', 'config ipif System ipaddress ' + c.ip[0] + '/' + IP.len2mask(c.ip[1]) + ' vlan ' + c.vlans[c.ipVlan || 1].name); if (c.gw) o.push('create iproute default ' + c.gw);
    o.push('', '#-------------------------------------------------------------------------------', '#                             End of configuration file', '#-------------------------------------------------------------------------------');
    return o.join('\n'); }
  function pingT(st, dst, n) { var net = st.net; if (!net) return ''; var r = net.ping(st.dev, dst); if (net.onTrace) net.onTrace(r, st.dev, dst); var o = ['Command: ping ' + dst + (n !== 4 ? ' times ' + n : ''), ''], got = 0;
    for (var i = 0; i < n; i++) { if (r.ok) { got++; o.push('Reply from ' + dst + ', time<10ms'); } else o.push('Request timed out.'); }
    o.push('', 'Ping Statistics for ' + dst, 'Packets: Sent =' + n + ', Received =' + got + ', Lost =' + (n - got)); return o.join('\n'); }

  function exec(st, raw) {
    var x = D(st); if (x.ask) { var a = x.ask; x.ask = null; return a.fn(String(raw).trim()); }
    var line = String(raw).trim().replace(/\s+/g, ' '); if (!line) return '';
    if (line === '?') return 'Available commands:\n' + TOP;
    var t = line.split(' '), hits = T.filter(function (e) { return e.p.length === t.length && e.p.every(function (p, i) { return tokOk(p, t[i]); }); });
    if (hits.length) { var e = hits[0], args = []; e.p.forEach(function (p, i) { if (p.charAt(0) === '<') args.push(p === '<n>' ? +t[i] : t[i]); });
      var r = e.run(st, args, line); if (r === null) return 'Command: ' + line + '\n\nFail!'; compile(st); return r; }
    var part = T.filter(function (e) { return e.p.length > t.length && t.every(function (w, i) { return tokOk(e.p[i], w); }); });
    if (part.length) { var nx = part.map(function (e) { return e.p[t.length]; }).filter(function (w, i, s) { return s.indexOf(w) === i; });
      return 'Command: ' + line + '\nNext possible completions:\n' + nx.join('  '); }
    return 'Available commands:\n' + TOP;
  }
  // ---------------------------------------------------------------- compile → модель MES
  function compile(st) {
    var c = C(st), V = c.vlans, ps = range(1, nports(st));
    st.vlans = {}; Object.keys(V).forEach(function (v) { st.vlans[v] = V[v].name; });
    var lagOf = {}; Object.keys(c.lag).forEach(function (k) { (c.lag[k].ports || []).forEach(function (p) { lagOf[p] = k; }); });
    ps.forEach(function (p) { var P0 = st.ports[p] || (st.ports[p] = {}); P0.mode = 'general'; P0.pvid = c.pvid[p] || 1; P0.shut = !!c.off[p];
      P0.gtag = Object.keys(V).filter(function (v) { return V[v].t.indexOf(p) >= 0; }).map(Number); P0.guntag = Object.keys(V).filter(function (v) { return V[v].u.indexOf(p) >= 0; }).map(Number);
      P0.access = P0.pvid; P0.native = P0.pvid; P0.allowed = []; P0.portfast = c.edge[p] === 'true'; P0.noAutoEdge = c.edge[p] !== 'auto';
      var g = lagOf[p]; if (g) P0.cg = { id: +g, mode: c.lag[g].type === 'lacp' ? c.lacp[p] || 'passive' : 'on' }; else delete P0.cg; });
    st.pos = {}; Object.keys(c.lag).forEach(function (k) { var m = c.lag[k].master; if (m) st.pos['po' + k] = EL.clone(st.ports[m]); });
    st.svi = {}; st.svi[c.ipVlan || 1] = c.ip[0] + '/' + c.ip[1]; st.gw = c.gw || null; st.routes = []; st.host = c.prompt || host(st);
    st.stp = { on: !!c.stp, mode: { rstp: 'rst', stp: 'stp', mstp: 'mst' }[c.stpVer || 'rstp'], prio: c.stpPrio || 32768 }; st.mst = { name: 'dlink-' + st.dev, rev: 0, inst: {} };
    if (st.net) st.net.gen++;
  }
  function fresh(n) { var p = range(1, n), pv = {}; p.forEach(function (x) { pv[x] = 1; });
    return { vlans: { 1: { name: 'default', t: [], u: p, f: [] } }, pvid: pv, ip: ['10.90.90.90', 8], off: {}, edge: {}, lag: {}, lacp: {}, stp: false }; }
  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}; if (m.kind !== 'dl-legacy') return d;
    d.sub = 'dlegacy'; d.st.mode = 'dlegacy'; d.st.bmac = 'b8:a3:86:' + d.st.bmac.slice(9);   /* OUI D-Link из примера show switch */ d.st.dl = { c: fresh(m.ports), saved: null, ask: null }; compile(d.st); return d; };
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id]; if (!isDl(d)) return ex0.apply(this, arguments); this.gen++; return d.off ? '' : exec(d.st, line); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; return isDl(d) ? prompt(d.st) : pr0.apply(this, arguments); };
  var he0 = P.help;
  P.help = function (id, line) { var d = this.devs[id]; if (!isDl(d)) return he0.apply(this, arguments); var t = String(line).trim().split(/\s+/).filter(Boolean);
    var nx = T.filter(function (e) { return e.p.length > t.length && t.every(function (w, i) { return tokOk(e.p[i], w); }); }).map(function (e) { return e.p[t.length]; }).filter(function (w, i, s) { return s.indexOf(w) === i; });
    return t.length ? nx.join('  ') : 'Available commands:\n' + TOP; };
  var tb0 = P.tab;
  P.tab = function (id, line) { var d = this.devs[id]; if (!isDl(d)) return tb0.apply(this, arguments); var t = String(line).split(' '), w = t.pop();
    var c = T.map(function (e) { return e.p[t.length]; }).filter(function (p, i, s) { return p && p.charAt(0) !== '<' && p.indexOf(w) === 0 && s.indexOf(p) === i; }); return c.length === 1 ? t.concat([c[0]]).join(' ') + ' ' : null; };
  var rb0 = P.reboot;
  P.reboot = function (id) { var d = this.devs[id]; if (!isDl(d)) return rb0.apply(this, arguments); var x = d.st.dl; x.c = x.saved ? EL.clone(x.saved) : fresh(nports(d.st)); x.ask = null; compile(d.st);
    this.mac[id] = {}; this.arp[id] = {}; d.off = false; this.gen++; };
  var sh0 = P.setHost;
  P.setHost = function (id, name) { var d = this.devs[id]; if (!isDl(d)) return sh0.apply(this, arguments); d.st.dl.c.prompt = name; compile(d.st); };
  if (EL.cfgText) { var ct0 = EL.cfgText; EL.cfgText = function (d) { return isDl(d) ? cfg(d.st) : ct0.apply(this, arguments); }; }
  if (EL.applyConfig) { var ap0 = EL.applyConfig; EL.applyConfig = function (n, id, text) { var d = n.devs[id]; if (!isDl(d)) return ap0.apply(this, arguments); var errs = [];
    String(text).split('\n').forEach(function (l) { l = l.trim(); if (!l || /^#/.test(l)) return; var r = n.exec(id, l); if (/Fail!|Available commands/.test(r)) errs.push(d.name + ' «' + l + '» → ошибка'); }); return errs; }; }
  EL.dlink = { isDl: isDl, exec: exec, prompt: prompt };
})(typeof window !== 'undefined' ? window : global);
