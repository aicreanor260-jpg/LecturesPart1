/* Маршрутизаторы Eltex ME (ME2001, ME5100S, ME5100 rev.X, ME5200S, ME5210S; спецификация sources/eltex/spec/me.md:
   руководство по настройке, справочник команд ME 3.13, руководство пользователя). Своя CLI: приглашение 0/<МОДЕЛЬ>:<hostname>#,
   режим хранится стеком, приглашение — по последнему узлу ((config-tengigabitethernet)#, (config-area)#, (config-unicast)#…);
   exit — на уровень выше, root — в (config)#, end — в глобальный режим. Все правки — в кандидат-конфигурацию; commit применяет их
   и сразу сохраняет как загрузочную (отдельного save нет), abort очищает кандидат; rollback и confirm, как у ESR, нет.
   Работает (компилируется в модель сети): hostname, user (privilege p1–p15), interface te|twe|hu|fo 0/0/N, сабинтерфейсы с
   encapsulation outer-vid, loopback, mgmt 0/fmc0/1 (VRF mgmt-intf), ipv4 address, vrf, shutdown; vrf NAME; router static →
   address-family ipv4 unicast → destination P/L NH и router static → vrf NAME → … (решение автора, вариант А);
   router ospfv2 NAME → router-id, area → interface (passive, metric — по умолчанию 1, вариант А). Межсетевого экрана нет.
   router bgp ASN → bgp router-id, neighbor (remote-as, update-source, ebgp-multihop, address-family ipv4 unicast, next-hop-self), network,
   redistribution — компилируется в BGP-модель ESR. Хранятся, но трафик не меняют (упрощение): IS-IS, VPNv4, MPLS/LDP, L2VPN,
   prefix-list, route-map, admin-distance, redistribution. Выводы show route / ospfv2 / ping — в формате ESR-модели (упрощение);
   диалог при exit с неприменёнными правками не моделируется; ввод проверяется по шаблонам справочника. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip, E = EL.E;
  var GR = {"global":["configure","config","abort","clear candidate-config","show configuration changes","show candidate-config","show candidate-config <rest>","show running-config","show running-config <rest>","change-privilege <w>","show privilege","show version","ping <ip>","ping <ip> vrf <w>","ping <ip> source <ip>","traceroute <ip>","reload system","logout","show interfaces","show interfaces <w>","show interfaces loopback <n>","show interfaces mgmt <w>","show interfaces status","show interfaces description","show interfaces description with-ifindex","show ipv4 interfaces brief","show vrf <w>","show arp vrf <w>","show route","show route <w>","show route vrf <w>","show route vrf <w> <w>","show route ipv4 <w>","show route rib summary","show ospfv2","show ospfv2 instance <w>","show ospfv2 neighbors","show ospfv2 neighbors detailed","show ospfv2 interfaces","show ospfv2 interfaces detailed","show ospfv2 database","show ospfv2 vrf <w> neighbors","show isis","show isis neighbors","show isis database","show isis interfaces","show bgp","show bgp <rest>","show bgp summary","show bgp all summary","show bgp vpnv4 unicast summary","show bgp neighbors","show bgp neighbors <ip>","show bgp vpnv4 unicast neighbors <ip> routes","clear bgp neighbor <w>","show mpls ldp forwarding","show mpls ldp neighbors","show mpls ldp neighbors detail","show mpls ldp bindings","show mpls ldp bindings remote","show mpls ldp parameters","show mpls ldp igp sync","show l2vpn xconnect","show l2vpn xconnect p2p-name <w> detail","show l2vpn xconnect group <w>","show l2vpn summary"],"any_config":["exit","root","end","commit","commit confirmed <n>","commit replace","abort","do <rest>"],"config":["hostname <w>","user <w>","no user <w>","system rootshell password <w>","system rootshell console-access disable","ssh server vrf <w>","telnet server vrf <w>","interface <w>","no interface <w>","interface loopback <n>","interface bundle-ether <w>","interface mgmt <w>","vrf <w>","no vrf <w>","router static","router ospfv2 <w>","no router ospfv2 <w>","router isis <w>","router bgp <n>","no router bgp <n>","router admin-distance","prefix-list <w>","route-map <w>","mpls","mpls ldp neighbor <ip>","l2vpn","l2vpn pw-class <w>"],"user":["password <w>","password encrypted <w>","privilege <w>"],"if":["ipv4 address <w>","no ipv4 address <w>","vrf <w>","no vrf","description <rest>","shutdown","no shutdown","mtu <n>","ip mtu <n>","arp aging-time <n>"],"sub":["ipv4 address <w>","no ipv4 address <w>","vrf <w>","no vrf","description <rest>","shutdown","no shutdown","encapsulation outer-vid <n>","encapsulation outer-vid <n> inner-vid <n>","no encapsulation","arp aging-time <n>","ipv4 unnumbered loopback <n>","arp proxy"],"lo":["ipv4 address <w>","no ipv4 address <w>","vrf <w>","no vrf","description <rest>","shutdown","no shutdown"],"mgmt":["ipv4 address <w>","no ipv4 address <w>"],"vrf":["rd <w>","import route-target <w>","export route-target <w>","description <rest>"],"static":["address-family ipv4 unicast","vrf <w>"],"static_af":["destination <w> <ip>","no destination <w> <ip>"],"static_dst":["description <rest>","metric <n>","admin-distance <n>","interface <w>","tag <n>"],"ospf":["router-id <ip>","area <ip>","vrf <w>","redistribution <w> <w>"],"ospf_vrf":["router-id <ip>","area <ip>","redistribution <w> <w>"],"ospf_area":["interface <w>","interface loopback <n>","no interface <w>","stub","nssa"],"ospf_if":["passive","no passive","network <w>","metric <n>","hello-interval <n>","dead-interval <n>","priority <n>","mtu-ignore","ldp-igp-synchronization"],"ospf_redist":["match prefix <w>","metric-type <w>","metric-value <n>","priority <n>","redistribute disable"],"isis":["net <w>","is-level <w>","host-name <w>","level <w>","interface <w>","interface loopback <n>"],"isis_level":["metric-style <w>"],"isis_if":["address-family ipv4 unicast","circuit-level <w>","level <w>","passive","point-to-point","hello-padding <w>","ldp-igp-synchronization","shutdown"],"isis_if_level":["metric <n>"],"bgp":["bgp router-id <ip>","neighbor <ip>","no neighbor <ip>","address-family ipv4 unicast","address-family vpnv4 unicast","vrf <w>"],"bgp_vrf":["bgp router-id <ip>","neighbor <ip>","no neighbor <ip>","address-family ipv4 unicast"],"bgp_af":["network <w>","aggregate-address <w>","redistribution connected <w>","redistribution static <w>","redistribution manual"],"bgp_redist":["set local-preference <n>","set origin <w>"],"bgp_nbr":["remote-as <n>","update-source <ip>","description <rest>","ebgp-multihop","ebgp-multihop ttl <n>","send-community","send-community-ext","route-reflector-client","address-family ipv4 unicast","address-family vpnv4 unicast","address-family l2vpn vpls"],"bgp_nbr_af":["next-hop-self","prefix-list in <w>","prefix-list out <w>","route-map in <w>","route-map out <w>","soft-reconfiguration inbound"],"adist":["bgp external <n>","bgp internal <n>"],"pl":["seq-num <n>"],"pl_seq":["prefix <w>","action <w>","le <n>","ge <n>"],"rm_seq":["action <w>","match prefix-list destination <w>","match as-path <rest>","set local-preference <n>","set med value <n>","set prepend as-path <n>"],"rm":["seq-num <n>"],"mpls":["router-id <ip>","transport-address <ip>","forwarding","ldp"],"mpls_fwd":["interface <w>","interface loopback <n>"],"ldp":["discovery interface <w>","no discovery interface <w>","neighbor <ip>","penultimate-hop-popping disable"],"ldp_if":["bfd fast-detect"],"ldp_nbr":["bfd fast-detect"],"l2vpn":["pw-class <w>","xconnect-group <w>"],"pwclass":["encapsulation mpls signaling-type <w>","encapsulation mpls control-word <w>","encapsulation mpls mtu <n>"],"xcg":["p2p <w>"],"p2p":["interface <w>","pw <ip> <n>","transport-mode <w>","mtu <n>"],"pw":["pw-class <w>","backup"]};
  // вход в блок: режим → шаблон → режим ребёнка
  var TR = {
    config: { 'user <w>': 'user', 'interface <w>': 'IF', 'interface loopback <n>': 'lo', 'interface bundle-ether <w>': 'IF', 'interface mgmt <w>': 'mgmt', 'vrf <w>': 'vrf',
      'router static': 'static', 'router ospfv2 <w>': 'ospf', 'router isis <w>': 'isis', 'router bgp <n>': 'bgp', 'router admin-distance': 'adist', 'prefix-list <w>': 'pl',
      'route-map <w>': 'rm', 'mpls': 'mpls', 'l2vpn': 'l2vpn', 'ssh server vrf <w>': 'srvvrf', 'telnet server vrf <w>': 'srvvrf', 'l2vpn pw-class <w>': 'pwclass', 'mpls ldp neighbor <ip>': 'ldp_nbr' },
    static: { 'address-family ipv4 unicast': 'static_af', 'vrf <w>': 'static_vrf' }, static_vrf: { 'address-family ipv4 unicast': 'static_af' },
    static_af: { 'destination <w> <ip>': 'static_dst' }, static_dst: { 'interface <w>': 'static_dst_if' },
    ospf: { 'area <ip>': 'ospf_area', 'vrf <w>': 'ospf_vrf', 'redistribution <w> <w>': 'ospf_redist' }, ospf_vrf: { 'area <ip>': 'ospf_area', 'redistribution <w> <w>': 'ospf_redist' },
    ospf_area: { 'interface <w>': 'ospf_if', 'interface loopback <n>': 'ospf_if' },
    isis: { 'level <w>': 'isis_level', 'interface <w>': 'isis_if', 'interface loopback <n>': 'isis_if' }, isis_if: { 'address-family ipv4 unicast': 'isis_af', 'level <w>': 'isis_if_level' },
    bgp: { 'neighbor <ip>': 'bgp_nbr', 'address-family ipv4 unicast': 'bgp_af', 'address-family vpnv4 unicast': 'bgp_af', 'vrf <w>': 'bgp_vrf' },
    bgp_vrf: { 'neighbor <ip>': 'bgp_nbr', 'address-family ipv4 unicast': 'bgp_af' }, bgp_af: { 'redistribution connected <w>': 'bgp_redist', 'redistribution static <w>': 'bgp_redist' },
    bgp_nbr: { 'address-family ipv4 unicast': 'bgp_nbr_af', 'address-family vpnv4 unicast': 'bgp_nbr_af', 'address-family l2vpn vpls': 'bgp_nbr_af' },
    pl: { 'seq-num <n>': 'pl_seq' }, rm: { 'seq-num <n>': 'rm_seq' }, mpls: { 'forwarding': 'mpls_fwd', 'ldp': 'ldp' },
    mpls_fwd: { 'interface <w>': 'fwd_if', 'interface loopback <n>': 'fwd_if' }, ldp: { 'discovery interface <w>': 'ldp_if', 'neighbor <ip>': 'ldp_nbr' },
    l2vpn: { 'pw-class <w>': 'pwclass', 'xconnect-group <w>': 'xcg' }, xcg: { 'p2p <w>': 'p2p' }, p2p: { 'pw <ip> <n>': 'pw' } };
  var LEAF = { IF: 'if', sub: 'sub', lo: 'lo', mgmt: 'mgmt', srvvrf: 'none', static_vrf: 'none', static_dst_if: 'static_dst', isis_af: 'none', fwd_if: 'none', bgp_vrf: 'bgp_vrf' };
  var PRM = { user: 'user', lo: 'loopback', mgmt: 'mgmt', vrf: 'vrf', static_vrf: 'vrf', ospf_vrf: 'vrf', bgp_vrf: 'vrf', srvvrf: 'vrf', static: 'static', static_af: 'unicast',
    bgp_af: 'unicast', isis_af: 'unicast', bgp_nbr_af: 'unicast', static_dst: 'destination', ospf: 'ospfv2', ospf_area: 'area', ospf_redist: 'connected', bgp_redist: 'connected',
    isis: 'isis', isis_level: 'level', isis_if_level: 'level', bgp: 'bgp', bgp_nbr: 'neighbor', ldp_nbr: 'neighbor', adist: 'admin-distance', pl: 'prefix-list', rm: 'route-map',
    pl_seq: 'seq-num', rm_seq: 'seq-num', mpls: 'mpls', mpls_fwd: 'forwarding', ldp: 'ldp', l2vpn: 'l2vpn', pwclass: 'pw-class', xcg: 'xconnect-group', p2p: 'p2p', pw: 'pw' };
  var IFT = { te: 'tengigabitethernet', twe: 'twentyfivegigabitethernet', hu: 'hundredgigabitethernet', fo: 'fortygigabitethernet', gi: 'gigabitethernet', bu: 'bundle-ether' };
  function isMe(d) { return !!d && d.sub === 'me'; }
  // имена интерфейсов: tengigabitethernet 0/0/1 | te 0/0/1 → te0/0/1 (fortygigabitethernet и fourtygigabitethernet → fo)
  function norm(line) {
    return String(line).replace(/\b(tengigabitethernet|te|twentyfivegigabitethernet|twe|hundredgigabitethernet|hu|fortygigabitethernet|fourtygigabitethernet|fo|gigabitethernet|gi)\s*(\d+\/\d+\/\d+(?:\.\d+)?)/ig,
      function (m, t, n) { t = t.toLowerCase(); var s = /^te/.test(t) ? 'te' : /^tw/.test(t) ? 'twe' : /^hu/.test(t) ? 'hu' : /^fo/.test(t) ? 'fo' : 'gi'; return s + n; });
  }
  function ifOk(w) { return /^(te|twe|hu|fo|gi)0\/\d+\/\d+(\.\d+)?$/.test(w); }
  function ifFull(w) { var m = String(w).match(/^([a-z]+)(.*)$/); return (IFT[m[1]] || m[1]) + ' ' + m[2]; }
  function ifPrompt(w) { var m = String(w).match(/^([a-z]+)\d.*?(\.\d+)?$/); return 'config-' + IFT[m[1]] + (m[2] ? '-sub' : ''); }

  // ---------------------------------------------------------------- устройство
  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}, st = d.st;
    if (m.kind === 'me') { d.sub = 'me'; st.dialect = 'me'; st.me = { model: m.promptModel || model, stack: [], cand: { L: [], K: {} }, run: { L: [], K: {} } };
      Object.keys(st.cand.ifs).forEach(function (k) { st.cand.ifs[k].fw = false; }); st.cand.host = 'EOS'; st.run = EL.clone(st.cand); }
    return d;
  };
  function M(st) { return st.me; }
  function prompt(st) { var me = M(st), top = me.stack[me.stack.length - 1], h = '0/' + me.model + ':' + st.run.host;
    if (!top) return h + '#'; return h + '(' + (top.mode === 'config' ? 'config' : top.prm) + ')#'; }
  function node(me, stack) { var n = me.cand; (stack || me.stack).slice(1).forEach(function (f) { n = n.K[f.h]; }); return n; }
  function match(pat, toks) { var r = E.match(pat.split(' '), toks); return r; }
  // ключ строки: слова без последнего значения (metric 15 → metric), «no X» удаляет
  function lkey(line) { var w = line.split(' '); return w.length > 1 && !/^(passive|stub|nssa|shutdown|send-community|send-community-ext|backup|point-to-point|mtu-ignore|next-hop-self|keepalive-disable|default-profile|802\.11kv)$/.test(line) ? w.slice(0, -1).join(' ') : line; }
  function header(pat, a, line) { return line.replace(/\b(te|twe|hu|fo|gi)(0\/\d+\/\d+(?:\.\d+)?)/g, function (m, t, n) { return IFT[t] + ' ' + n; }); }
  function config(st, line) {
    var me = M(st), top = me.stack[me.stack.length - 1], mode = top.mode, low = line.toLowerCase().split(/\s+/), toks = line.split(/\s+/);
    if (line === 'exit') { me.stack.pop(); if (me.stack.length === 0) return ''; return ''; }
    if (line === 'root') { me.stack = me.stack.slice(0, 1); return ''; }
    if (line === 'end') { me.stack = []; return ''; }
    if (line === 'abort') { me.cand = EL.clone(me.run); me.stack = []; return ''; }
    if (line === 'commit' || /^commit (confirmed \d+|replace)$/.test(line)) return commit(st);
    var tr = TR[mode === 'IF' && top.sub ? 'sub' : mode] || {}, ent = Object.keys(tr).filter(function (p) { return match(p, low); })[0];
    if (ent) {
      var a = match(ent, toks), iw0 = toks[toks.length - 1];
      if (/interface <w>$/.test(ent) && !ifOk(iw0)) return '% Invalid input';
      var ch = tr[ent], h = header(ent, a, line), n = node(me); n.K[h] = n.K[h] || { L: [], K: {} };
      var iw = toks[toks.length - 1], prm = ch === 'IF' || /_if$/.test(ch) && !/loopback/.test(line) ? ifPrompt(iw) : /loopback/.test(line) && /_if$|^IF$/.test(ch) ? 'config-loopback' : 'config-' + PRM[ch];
      if (ch === 'IF' && /bundle-ether/.test(line)) prm = 'config-bundle-ether';
      me.stack.push({ mode: ch, h: h, prm: prm.replace(/^config-config-/, 'config-'), sub: ch === 'IF' && /\.\d+$/.test(iw) }); me.dirty = true; return '';
    }
    var lm = LEAF[mode === 'IF' && top.sub ? 'sub' : mode] || mode, L = (GR[lm] || []).concat(GR.any_config_leaf || []);
    if (/^no /.test(line)) { var k = line.slice(3), n2 = node(me); var before = n2.L.length + Object.keys(n2.K).length;
      n2.L = n2.L.filter(function (x) { return x !== k && lkey(x) !== k && x.indexOf(k + ' ') !== 0; }); Object.keys(n2.K).forEach(function (h2) { if (h2 === header('', [], k)) delete n2.K[h2]; });
      if (!(GR[lm] || []).concat(GR.config || []).some(function (p) { return /^no /.test(p) && match(p, low); }) && before === n2.L.length + Object.keys(n2.K).length) return '% Invalid input';
      me.dirty = true; return ''; }
    var hit = pick(L, low); if (!hit) return '% Invalid input';
    line = canon(hit, toks);
    if (/^privilege /.test(line) && !/^privilege p(1[0-5]|[1-9])$/.test(line)) return '% Invalid input';
    var n3 = node(me), key = lkey(line); n3.L = n3.L.filter(function (x) { return lkey(x) !== key || /^(band|import route-target|export route-target)$/.test(key); }); n3.L.push(line); me.dirty = true; return '';
  }
  // шаблон для строки: сокращение слова не считается, если это слово целиком — ключевое слово другой команды режима (ip ≠ ipv4: есть ip mtu)
  function pick(L, low) { return L.filter(function (p) { return match(p, low); }).filter(function (p) { var w = p.split(' ');
    return w.every(function (x, i) { return /^</.test(x) || low[i] === x || !L.some(function (q) { return q.split(' ')[i] === low[i]; }); }); })[0] || null; }
  function canon(p, toks) { var w = p.split(' '); return w.map(function (x, i) { return /^</.test(x) ? toks[i] : x; }).concat(w[w.length - 1] === '<rest>' ? toks.slice(w.length) : []).join(' '); }
  function dump(n, ind, o) { n.L.forEach(function (l) { o.push(ind + l); }); Object.keys(n.K).forEach(function (h) { o.push(ind + h); dump(n.K[h], ind + '   ', o); o.push(ind + 'exit'); }); return o; }

  // ---------------------------------------------------------------- commit: дерево → модель сети (ESR-движок)
  function val(n, k) { var x = n.L.filter(function (l) { return lkey(l) === k || l.indexOf(k + ' ') === 0; })[0]; return x ? x.slice(k.length + 1) : null; }
  function compile(st) {
    var me = M(st), t = me.run, c = st.run, base = {};
    Object.keys(c.ifs).forEach(function (k) { if (/^(te|twe|hu|fo|gi|mgmt)/.test(k) && k.indexOf('.') < 0) base[k] = { ip: null, fw: false, shut: false, speed: c.ifs[k].speed, duplex: c.ifs[k].duplex }; });
    c.ifs = base; c.routes = []; c.vrfs = { 'mgmt-intf': {} }; c.ospf = null; c.host = val(t, 'hostname') || 'EOS';
    c.users = { admin: { pw: 'password', priv: 15 } };
    Object.keys(t.K).forEach(function (h) { var n = t.K[h], m;
      if ((m = h.match(/^user (\S+)$/))) { var pv = (val(n, 'privilege') || 'p1').slice(1); c.users[m[1]] = { pw: val(n, 'password') || '', priv: +pv }; }
      if ((m = h.match(/^vrf (\S+)$/))) c.vrfs[m[1]] = {};
      if ((m = h.match(/^interface (\S+) (\S+)$/)) && IFT[Object.keys(IFT).filter(function (k) { return IFT[k] === m[1]; })[0]]) {
        var short = Object.keys(IFT).filter(function (k) { return IFT[k] === m[1]; })[0] + m[2], phys = short.split('.')[0], key = short, enc = val(n, 'encapsulation outer-vid');
        if (short.indexOf('.') > 0) { if (!enc) return; key = phys + '.' + parseInt(enc, 10); }
        if (!base[phys] && short.indexOf('.') < 0) return;
        var x = c.ifs[key] = c.ifs[key] || { ip: null, fw: false, shut: false }; x.ip = val(n, 'ipv4 address'); x.shut = n.L.indexOf('shutdown') >= 0; if (val(n, 'vrf')) x.vrf = val(n, 'vrf'); }
      if ((m = h.match(/^interface loopback (\d+)$/))) c.ifs['lo' + m[1]] = { ip: val(n, 'ipv4 address'), fw: false, shut: n.L.indexOf('shutdown') >= 0, vrf: val(n, 'vrf') || undefined };
      if ((m = h.match(/^interface mgmt (\S+)$/)) && c.ifs['mgmt' + m[1]]) { var g = c.ifs['mgmt' + m[1]]; g.ip = val(n, 'ipv4 address'); g.vrf = 'mgmt-intf'; }
      if (h === 'router static') Object.keys(n.K).forEach(function (h2) { var vm = h2.match(/^vrf (\S+)$/), af = vm ? n.K[h2].K['address-family ipv4 unicast'] : h2 === 'address-family ipv4 unicast' ? n.K[h2] : null;
        if (af) Object.keys(af.K).forEach(function (h3) { var d = h3.match(/^destination (\S+) (\S+)$/), cc = d && IP.parseCidr(d[1]); if (!cc) return;
          var ad = val(af.K[h3], 'admin-distance'); c.routes.push({ net: IP.netOf(cc.ip, cc.len), nh: d[2], ad: ad ? +ad : 1, vrf: vm ? vm[1] : undefined }); }); });
      if ((m = h.match(/^router ospfv2 (\S+)$/)) && !c.ospf) { c.ospf = { id: 1, rid: val(n, 'router-id'), on: true, areas: {} };
        Object.keys(n.K).forEach(function (h2) { var am = h2.match(/^area (\S+)$/); if (!am) return; c.ospf.areas[am[1]] = { on: true };
          Object.keys(n.K[h2].K).forEach(function (h3) { var im = h3.match(/^interface (\S+) (\S+)$/), k3 = null;
            if (im && im[1] === 'loopback') k3 = 'lo' + im[2]; else if (im) { var sh = Object.keys(IFT).filter(function (k) { return IFT[k] === im[1]; })[0]; k3 = sh + im[2]; }
            var nn = n.K[h2].K[h3], x3 = k3 && (c.ifs[k3] || Object.keys(c.ifs).filter(function (k) { return k.split('.')[0] === k3.split('.')[0] && k3.indexOf('.') > 0; }).map(function (k) { return c.ifs[k]; })[0]);
            if (x3) x3.ospf = { inst: 1, area: am[1], on: true, passive: nn.L.indexOf('passive') >= 0, cost: +(val(nn, 'metric') || 1) }; }); }); }
    });
    // BGP (РН гл. BGP, СК 13.x): router bgp ASN → bgp router-id, neighbor → remote-as, update-source, ebgp-multihop, address-family ipv4 unicast (обязательна у соседа),
    // address-family ipv4 unicast → network, redistribution connected|static; enable нет — процесс работает сразу
    c.bgp = null;
    Object.keys(t.K).forEach(function (h) { var m = h.match(/^router bgp (\d+)$/); if (!m || c.bgp) return; var n = t.K[h], b = c.bgp = { as: +m[1], on: true, rid: val(n, 'bgp router-id'), nets: [], redist: [], nbr: {} };
      var af = n.K['address-family ipv4 unicast'];
      if (af) { af.L.forEach(function (l) { var nm = l.match(/^network (\S+)$/), cc = nm && IP.parseCidr(nm[1]); if (cc) b.nets.push(IP.netOf(cc.ip, cc.len)); });
        Object.keys(af.K).forEach(function (h2) { var r = h2.match(/^redistribution (connected|static) /); if (r && b.redist.indexOf(r[1]) < 0) b.redist.push(r[1]); }); }
      Object.keys(n.K).forEach(function (h2) { var nm = h2.match(/^neighbor (\S+)$/); if (!nm) return; var x = n.K[h2], naf = x.K['address-family ipv4 unicast'];
        b.nbr[nm[1]] = { as: +(val(x, 'remote-as') || 0) || null, src: val(x, 'update-source'), on: true, af: !!naf, multihop: x.L.some(function (l) { return /^ebgp-multihop/.test(l); }),
          nhs: !!(naf && naf.L.indexOf('next-hop-self') >= 0), desc: val(x, 'description') }; }); });
    st.cand = EL.clone(c);
  }
  function commit(st) { var me = M(st); me.run = EL.clone(me.cand); compile(st); me.dirty = false; if (st.net) st.net.gen++;
    var host = st.run.host; return EL.clock.fmt(EL.clock.now()) + '\nCommit successfully completed in 0.031951 sec' + (host ? '' : ''); }

  // ---------------------------------------------------------------- глобальный режим
  function global(st, line) {
    var me = M(st), low = line.toLowerCase().split(/\s+/), net = st.net;
    if (line === 'configure' || line === 'config') { me.stack = [{ mode: 'config', h: null, prm: 'config' }]; return ''; }
    if (line === 'abort' || line === 'clear candidate-config') { me.cand = EL.clone(me.run); return ''; }
    if (line === 'show running-config') return dump(me.run, '', []).join('\n');
    if (/^show running-config /.test(line)) { var w = norm(line.slice(20)).replace(/\b(te|twe|hu|fo|gi)(0\/)/g, function (m, t, r) { return IFT[t] + ' ' + r; }); return dump(me.run, '', []).join('\n').split(/\n(?=\S)/).filter(function (b) { return b.indexOf(w) === 0; }).join('\n'); }
    if (line === 'show candidate-config') return dump(me.cand, '', []).join('\n');
    if (line === 'show configuration changes') { var a = dump(me.run, '', []), b = dump(me.cand, '', []); var d = b.filter(function (l) { return a.indexOf(l) < 0; });
      return d.length ? EL.clock.fmt(EL.clock.now()) + '\n' + d.map(function (l) { return l.trim(); }).join('\n') : ''; }
    if (line === 'show version') { var m = EL.MODELS[net && net.devs[st.dev].model] || {}; return 'Eltex ' + me.model + ' · ' + (m.sw || ''); }
    if (/^show route( vrf \S+)?$/.test(line) || line === 'show route ospf' || line === 'show route static') return net ? net.routeText(st.dev, false) : '';
    if (line === 'show ospfv2 neighbors') return net ? net.ospfNbrText(st.dev) : '';
    // BGP — выводы ESR-модели (упрощение: формат ME в выводах другой)
    var bq = { 'show bgp': 'show bgp ipv4 unicast', 'show bgp summary': 'show bgp summary', 'show bgp all summary': 'show bgp summary', 'show bgp neighbors': 'show bgp neighbors' }[line] ||
      (/^show bgp neighbors \S+$/.test(line) ? 'show bgp neighbors' : null);
    if (bq) { var md = st.mode; st.mode = 'priv'; try { return st.run.bgp ? EL.esr.exec(st, bq) : ''; } finally { st.mode = md; } }
    if (line === 'show ipv4 interfaces brief') return net ? net.ifaces(st.dev).map(function (f) { return (f.name + '                    ').slice(0, 22) + f.ip + '/' + f.len; }).join('\n') : '';
    if (/^ping \S+( vrf \S+)?$/.test(line)) { var pm = line.match(/^ping (\S+)(?: vrf (\S+))?$/); if (!net) return ''; if (pm[2]) net._vrfSrc = { dev: st.dev, vrf: pm[2] };
      try { return net.pingText(st.dev, pm[1], 'esr'); } finally { net._vrfSrc = null; } }
    if (/^traceroute \S+$/.test(line)) return net ? net.traceText(st.dev, line.split(' ')[1]) : '';
    if ((GR.global || []).some(function (p) { return match(p, low); })) return '';
    return '% Invalid input';
  }
  function exec(st, raw) {
    var line = norm(String(raw).trim()).replace(/\s+/g, ' '), me = M(st); if (!line) return '';
    var d = line.match(/^do (.+)$/); if (d && me.stack.length) return global(st, d[1]);
    return me.stack.length ? config(st, line) : global(st, line);
  }
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id]; if (isMe(d)) { this.gen++; return d.off ? '' : exec(d.st, line); } return ex0.apply(this, arguments); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; return isMe(d) ? prompt(d.st) : pr0.apply(this, arguments); };
  EL.me = { exec: exec, prompt: prompt, norm: norm };
})(typeof window !== 'undefined' ? window : global);
