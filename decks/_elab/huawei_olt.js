/* OLT Huawei SmartAX MA5600T и ONT EchoLife EG8145V5 — спецификация sources/huawei/spec/olt.md (главный источник — HCIA-Access Lab Guide 2.5,
   снят на MA5600T V800R013C00; TechNotes EDOC1100108355–108357).
   Из olt.js Eltex взяты механика PON-кабеля (оптика между PON-портом OLT и портом PON ONT) и ONT как пассивный мост (тип 'mes', sub 'ont',
   своей CLI нет); CLI OLT другая (VRP-подобная SmartAX: > → enable → # → config → (config)# → (config-if-gpon-0/5)#), поэтому своя.
   Платы — как на стенде LG: 5 H802GPBD (8 GPON, порты 0/5/0–7), 9 H801SCUN (управление), 19 H801GICG (uplink 0/19/0–1);
   новая плата — Auto_find, после board confirm 0 — Normal (сервис только на Normal).
   Глобальные команды действуют сразу; commit — только в ont-lineprofile / ont-srvprofile; save — сохранение (после перезагрузки грузится оно).
   Цепочка сервиса (§6.4): dba-profile → line-profile (tcont, gem add, gem mapping G I vlan C) + srv-profile (port vlan eth K C) → ont add|confirm по SN →
   ONT online → ont port native-vlan (порт ONT без тега) → vlan S smart + port vlan S 0/19 P → service-port … vlan S gpon 0/5/P ont O gemport G … user-vlan C.
   Кадры: uplink — S-VLAN с тегом (native-vlan — без тега); PON ↔ ONT — S-VLAN; ETH K ONT — без тега при native-vlan C, иначе с тегом S.
   ONT видна в display ont autofind, только если port P ont-auto-find enable (TS-AF). Лазер: port P laser-switch off — ONT offline.
   Допущения (в отчёте): ввод — только полные команды; при неполной или неизвестной печатается подсказка следующего слова в формате { …<K> }:
   (тексты ошибок в источниках нет), сразу без ожидания; трансляция C-VLAN ↔ S-VLAN не моделируется (кадры за ONT — в S-VLAN);
   Match state — всегда match, Config state offline-ONT — initial; сплиттер — одна ONT на PON-порт; DBA, traffic table, rx/tx-cttr — только хранятся;
   display current-configuration — список команд в стиле «Configuration Reference» LG. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, P = EL.Net.prototype;
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  var PON = range('0/5/', 0, 7), UP = range('0/19/', 0, 1);
  EL.MODELS.MA5600T = { type: 'mes', kind: 'hwolt', portList: PON.concat(UP), ports: 10, group: 'Huawei (как в eNSP)', host: 'MA5600T',
    note: 'OLT Huawei SmartAX MA5600T (V800R013): плата GPON 0/5 (порты 0/5/0–7), uplink GIU 0/19 (0/19/0–1); профили DBA/line/srv, ont add, service-port',
    login: [{ u: 'root', p: 'admin', a: 'консоль (HCIA-Access LG)' }] };
  EL.MODELS.EG8145V5 = { type: 'mes', kind: 'ont', hw: true, ports: 5, portList: ['PON', 'ETH1', 'ETH2', 'ETH3', 'ETH4'], group: 'Huawei (как в eNSP)',
    note: 'ONT Huawei EchoLife EG8145V5 (HG8247H9): GPON + 4 × ETH, мост, настраивается с OLT по OMCI · имена портов ETH1–4 условные',
    login: [{ u: '—', p: '—', a: 'своей CLI нет — профили с OLT (OMCI)' }] };
  var BOARDS = { 5: 'H802GPBD', 9: 'H801SCUN', 19: 'H801GICG' };
  function isO(d) { return !!d && d.sub === 'hwolt'; }
  function isHwOnt(d) { return !!d && d.sub === 'ont' && !!d.st.hwSn; }
  function fresh() { return { sysname: null, boards: { 5: 'Auto_find', 9: 'Active_normal', 19: 'Auto_find' }, dba: {}, lp: { 0: { name: 'line-profile_default_0', run: { tc: {}, gem: {}, map: [] } } },
    sp: { 0: { name: 'srv-profile_default_0', run: { ports: {}, pv: [] } } }, vlans: {}, upv: {}, nv: {}, pon: {}, onts: {}, sps: {}, vif: {}, routes: [] }; }
  function O(st) { return st.hwo; }
  function C(st) { return st.hwo.c; }

  // ---------------------------------------------------------------- разбор команд: ключевые слова сокращаются до однозначного начала
  var T = [];
  function cmd(modes, pat, run, d) { var e = { m: modes.split(' '), p: pat.split(' '), run: run, d: d || '' }; T.push(e); return e; }
  function tok(p, t) { if (p === '<n>') return /^\d+$/.test(t); if (p === '<w>') return true; if (p === '<ip>') return IP.ip2n(t) !== null;
    if (p === '<fs>') return /^0\/\d+$/.test(t); if (p === '<fsp>') return /^0\/\d+\/\d+$/.test(t); if (p === '<mask>') return /^\d{1,2}$/.test(t) || IP.mask2len(t) !== null;
    return t.toLowerCase() === p || p.indexOf(t.toLowerCase()) === 0 && t.length >= 2; }
  function inMode(e, m) { return e.m.indexOf(m) >= 0 || e.m.indexOf('*') >= 0 || (e.m.indexOf('cfg') >= 0 && /^(config|gpon|giu|vlanif|meth|lp|sp)$/.test(m)) || (e.m.indexOf('priv') >= 0 && m !== 'user'); }
  function match(p, t) { var a = []; for (var k = 0; k < p.length; k++) { if (p[k] === '<rest>') { if (k >= t.length) return null; a.push(t.slice(k).join(' ')); return a; }
      if (t[k] === undefined || !tok(p[k], t[k])) return null; if (p[k].charAt(0) === '<') a.push(/^<(n)>$/.test(p[k]) ? +t[k] : p[k] === '<mask>' ? (/^\d+$/.test(t[k]) ? +t[k] : IP.mask2len(t[k])) : t[k]); }
    return t.length === p.length ? a : null; }
  var PH = { '<n>': 'U', '<w>': 'S', '<ip>': 'I', '<fs>': 'S', '<fsp>': 'S', '<mask>': 'U', '<rest>': 'S' };
  // подсказка в формате интерактивного ввода SmartAX: { a<K>|b<K>|value<U> }:
  function nextWords(st, t) { var m = O(st).mode, out = [], cr = false;
    T.forEach(function (e) { if (!inMode(e, m)) return; for (var k = 0; k < t.length; k++) { if (e.p[k] === '<rest>') return; if (k >= e.p.length || !tok(e.p[k], t[k])) return; }
      if (e.p.length === t.length) { cr = true; return; } var w = e.p[t.length]; w = w.charAt(0) === '<' ? w.slice(1, -1) + '<' + PH[w] + '>' : w + '<K>'; if (out.indexOf(w) < 0) out.push(w); });
    return (cr ? ['<cr>'] : []).concat(out); }
  function hintAt(st, t) { var k = t.length; while (k > 0 && !nextWords(st, t.slice(0, k)).length) k--; var L = nextWords(st, t.slice(0, k)); return L.length ? '{ ' + L.join('|') + ' }:' : ''; }
  function exec(st, raw) {
    var x = O(st); if (x.ask) { var q = x.ask; x.ask = null; return /^y/i.test(String(raw).trim()) ? q() : ''; }
    var line = String(raw).trim(); if (!line) return '';
    if (/\?$/.test(line)) { var t0 = line.slice(0, -1).trim().split(/\s+/).filter(Boolean); return nextWords(st, t0).map(function (w) { return '  ' + w; }).join('\n'); }
    var t = line.split(/\s+/), m = x.mode, hit = null;
    T.forEach(function (e) { if (hit || !inMode(e, m)) return; var a = match(e.p, t); if (a) hit = { e: e, a: a }; });
    if (!hit) return hintAt(st, t);
    var r = hit.e.run(st, hit.a); if (r === null) return hintAt(st, t.slice(0, -1));
    if (st.net) st.net.gen++;
    return r || '';
  }
  function prompt(st) { var x = O(st), h = C(st).sysname || x.model, m = x.mode;
    if (x.ask) return ''; if (m === 'user') return h + '>'; if (m === 'priv') return h + '#'; if (m === 'config') return h + '(config)#';
    return h + '(config-' + ({ gpon: 'if-gpon-' + x.ctx, giu: 'if-giu-' + x.ctx, vlanif: 'if-vlanif' + x.ctx, meth: 'if-meth0', lp: 'gpon-lineprofile-' + x.ctx, sp: 'gpon-srvprofile-' + x.ctx })[m] + ')#'; }

  // ---------------------------------------------------------------- режимы
  function go(m, ctx) { return function (st) { O(st).mode = m; O(st).ctx = ctx === undefined ? null : ctx; }; }
  cmd('user', 'enable', go('priv'), 'Enter privilege mode');
  cmd('priv', 'disable', go('user'), 'Return to user mode');
  cmd('priv', 'config', go('config'), 'Enter global config mode');
  cmd('priv', 'sysname <w>', function (st, a) { C(st).sysname = a[0]; st.host = a[0]; }, 'Set the host name');
  cmd('config gpon giu vlanif meth lp sp', 'quit', function (st) { var x = O(st); x.mode = x.mode === 'config' ? 'priv' : 'config'; x.ctx = null; }, 'Exit the current mode');
  cmd('config gpon giu vlanif meth lp sp', 'return', go('priv'), 'Return to privilege mode');
  cmd('user priv', 'quit', function (st) { var x = O(st); if (x.mode !== 'priv' && x.mode !== 'user') return null;
    x.ask = function () { x.mode = 'user'; return ''; }; return 'Check whether system data has been changed. Please save data before logout.\nAre you sure to log out? (y/n)[n]:'; }, 'Log out');
  cmd('cfg', 'interface meth 0', go('meth'));
  cmd('cfg', 'interface gpon <fs>', function (st, a) { if (a[0] !== '0/5') return null; go('gpon', a[0])(st); }, 'GPON board');
  cmd('cfg', 'interface giu <fs>', function (st, a) { if (a[0] !== '0/19') return null; go('giu', a[0])(st); }, 'Upstream board');
  cmd('cfg', 'interface vlanif <n>', function (st, a) { if (!C(st).vlans[a[0]]) return null; C(st).vif[a[0]] = C(st).vif[a[0]] || {}; go('vlanif', a[0])(st); }, 'VLAN interface');
  cmd('vlanif', 'ip address <ip> <mask>', function (st, a) { C(st).vif[O(st).ctx].ip = [a[0], a[1]]; }, 'Set the IP address');
  cmd('vlanif', 'undo ip address', function (st) { delete C(st).vif[O(st).ctx].ip; });
  cmd('cfg', 'ip route-static <ip> <ip> <ip>', function (st, a) { var l = IP.mask2len(a[1]); if (l === null) return null; var c = C(st);
    c.routes = c.routes.filter(function (r) { return r.net !== IP.netOf(a[0], l); }).concat([{ net: IP.netOf(a[0], l), nh: a[2] }]); }, 'Static route');

  // ---------------------------------------------------------------- платы
  cmd('cfg', 'board confirm 0', function (st) { var B = C(st).boards; Object.keys(B).forEach(function (s) { if (B[s] === 'Auto_find') B[s] = 'Normal'; }); }, 'Confirm boards');
  cmd('cfg', 'board confirm <fs>', function (st, a) { var B = C(st).boards, s = a[0].split('/')[1]; if (!B[s]) return null; if (B[s] === 'Auto_find') B[s] = 'Normal'; });
  function okB(c, s) { return c.boards[s] === 'Normal'; }
  function bline(s, c) { var n = BOARDS[s]; return '  ' + pad(s, 8) + (n ? pad(n, 11) + c.boards[s] : ''); }
  cmd('*', 'display board 0', function (st) { var c = C(st), SEP = '  ' + new Array(74).join('-'), o = [SEP, '  SlotID  BoardName  Status          SubType0 SubType1    Online/Offline', SEP];
    for (var s = 0; s <= 22; s++) o.push(bline(s, c)); o.push(SEP); return o.join('\n'); }, 'Display board information');
  cmd('*', 'display board <fs>', function (st, a) { var c = C(st), s = a[0].split('/')[1], S1 = '  ' + new Array(40).join('-'), S2 = '  ' + new Array(77).join('-'), S3 = '  ' + new Array(62).join('-');
    if (!BOARDS[s]) return null; var o = [S1, '  Board Name          : ' + BOARDS[s], '  Board Status        : ' + c.boards[s], S1, S2, '  Power Status      Power-off cause                    Power-off Time', S2,
      '  POWER-ON          -                                  -', S2];
    if (s === '5') { o.push(S3, '    Port   Port   min-distance   max-distance   Optical-module', '           type       (km)           (km)           status', S3);
      PON.forEach(function (p, i) { o.push('    ' + pad(i, 6) + pad('GPON', 8) + pad(0, 15) + pad(20, 15) + (st.net && st.net.peer(st.dev, p) ? 'Online' : 'Offline')); }); o.push(S3);
      PON.forEach(function (p, i) { var L = ontsOn(st, i); o.push('  In port 0/ 5/' + i + ' , the total of ONTs are: ' + L.all + ', online: ' + L.on); }); }
    return o.join('\n'); }).cfg = false;

  // ---------------------------------------------------------------- профили DBA / line / srv
  cmd('cfg', 'dba-profile add profile-id <n> <rest>', function (st, a) { if (a[0] < 10 || a[0] > 512) return null; var t = a[1].split(/\s+/), d = { id: a[0] }, i = 0;
    if (t[0] === 'profile-name') { d.name = t[1]; i = 2; } var ty = (t[i] || '').match(/^type([1-5])$/); if (!ty) return null; d.type = +ty[1]; d.txt = t.slice(i).join(' ');
    var g = function (k) { var j = t.indexOf(k); return j >= 0 && /^\d+$/.test(t[j + 1] || '') ? +t[j + 1] : 0; }; d.fix = g('fix'); d.assure = g('assure'); d.max = g('max');
    C(st).dba[a[0]] = d; return '  Adding a DBA profile succeeded\n  Profile ID  : ' + a[0] + '\n  Profile name: ' + (d.name || 'dba-profile_' + a[0]); }, 'DBA profile');
  cmd('cfg', 'dba-profile delete profile-id <n>', function (st, a) { delete C(st).dba[a[0]]; });
  var DBA0 = [[0, 3, 0, 8192, 20480], [1, 1, 5120, 0, 0], [2, 1, 1024, 0, 0], [3, 4, 0, 0, 32768], [4, 1, 1024000, 0, 0], [5, 1, 32768, 0, 0], [6, 1, 102400, 0, 0], [7, 2, 0, 32768, 0], [8, 2, 0, 102400, 0], [9, 3, 0, 32768, 65536]];
  function r(v, n) { return ('            ' + v).slice(-n); }
  cmd('*', 'display dba-profile all', function (st) { var c = C(st), SEP = '  ' + new Array(77).join('-'), o = [SEP, '  Profile-ID   type   Bandwidth      Fix        Assure        Max        Bind', '                     compensation    (kbps)     (kbps)        (kbps)     times', SEP];
    var bind = function (id) { return Object.keys(c.lp).reduce(function (s, k) { var tc = (c.lp[k].run || {}).tc || {}; return s + Object.keys(tc).filter(function (q) { return tc[q] === id; }).length; }, 0); };
    DBA0.concat(Object.keys(c.dba).map(function (k) { var d = c.dba[k]; return [d.id, d.type, d.fix, d.assure, d.max]; })).forEach(function (d) {
      o.push(r(d[0], 12) + r(d[1], 7) + r('No', 13) + r(d[2], 11) + r(d[3], 11) + r(d[4], 14) + r(bind(d[0]), 10)); }); o.push(SEP); return o.join('\n'); }, 'Display DBA profiles').cfg = false;
  function prof(st, kind, id, name) { var c = C(st), M = c[kind]; if (id > 8192) return null; if (!M[id]) M[id] = { name: name || (kind === 'lp' ? 'line-profile_' : 'srv-profile_') + id, run: kind === 'lp' ? { tc: {}, gem: {}, map: [] } : { ports: {}, pv: [] } };
    else if (name) M[id].name = name; M[id].cand = EL.clone(M[id].run); go(kind, id)(st); }
  cmd('cfg', 'ont-lineprofile gpon profile-id <n>', function (st, a) { return prof(st, 'lp', a[0]); }, 'ONT line profile');
  cmd('cfg', 'ont-lineprofile gpon profile-id <n> profile-name <w>', function (st, a) { return prof(st, 'lp', a[0], a[1]); });
  cmd('cfg', 'ont-srvprofile gpon profile-id <n>', function (st, a) { return prof(st, 'sp', a[0]); }, 'ONT service profile');
  cmd('cfg', 'ont-srvprofile gpon profile-id <n> profile-name <w>', function (st, a) { return prof(st, 'sp', a[0], a[1]); });
  function lc(st) { return C(st).lp[O(st).ctx].cand; }
  function sc(st) { return C(st).sp[O(st).ctx].cand; }
  cmd('lp', 'tcont <n> dba-profile-id <n>', function (st, a) { if (a[0] > 127 || a[1] > 512 || !(a[1] < 10 || C(st).dba[a[1]])) return null; lc(st).tc[a[0]] = a[1]; }, 'T-CONT');
  cmd('lp', 'gem add <n> eth tcont <n>', function (st, a) { if (a[0] > 1023 || lc(st).tc[a[1]] === undefined) return null; lc(st).gem[a[0]] = a[1]; }, 'GEM port');
  cmd('lp', 'mapping-mode vlan', function (st) { lc(st).mm = 'vlan'; }, 'Mapping mode');
  cmd('lp', 'gem mapping <n> <n> vlan <n>', function (st, a) { var L = lc(st); if (L.gem[a[0]] === undefined || a[1] > 7 || a[2] < 1 || a[2] > 4095) return null;
    L.map = L.map.filter(function (m) { return !(m.g === a[0] && m.i === a[1]); }).concat([{ g: a[0], i: a[1], v: a[2] }]); }, 'GEM mapping');
  cmd('lp sp', 'commit', function (st) { var M = C(st)[O(st).mode][O(st).ctx]; M.run = EL.clone(M.cand); }, 'Commit the profile');
  cmd('sp', 'ont-port <rest>', function (st, a) { var t = a[0].split(/\s+/), P2 = {}; for (var i = 0; i < t.length; i += 2) { if (!/^(eth|pots|catv)$/.test(t[i]) || !/^\d+$/.test(t[i + 1] || '')) return null; P2[t[i]] = +t[i + 1]; }
    sc(st).ports = P2; }, 'ONT ports');
  cmd('sp', 'port vlan eth <n> <n>', function (st, a) { var S = sc(st); if (a[0] < 1 || a[0] > ((S.ports || {}).eth || 0) || a[1] < 1 || a[1] > 4095) return null;
    S.pv = S.pv.filter(function (p) { return !(p.k === 'eth' && p.n === a[0]); }).concat([{ k: 'eth', n: a[0], v: a[1] }]); return '  Set ONT port(s) VLAN configuration, success: 1, failed: 0'; }, 'Port VLAN');
  cmd('sp', 'port vlan iphost <n>', function (st, a) { var S = sc(st); S.pv = S.pv.filter(function (p) { return p.k !== 'iphost'; }).concat([{ k: 'iphost', v: a[0] }]); return '  Set ONT port(s) VLAN configuration, success: 1, failed: 0'; });
  function binds(c, kind, id) { return Object.keys(c.onts).filter(function (k) { return c.onts[k][kind] === id; }).length; }
  ['lp', 'sp'].forEach(function (kind) { var w = kind === 'lp' ? 'ont-lineprofile' : 'ont-srvprofile';
    cmd('*', 'display ' + w + ' gpon all', function (st) { var c = C(st), SEP = '  ' + new Array(77).join('-'), K = Object.keys(c[kind]);
      return [SEP, '  Profile-ID   Profile-name                                Binding times', SEP].concat(K.map(function (k) { return '  ' + pad(k, 15) + pad(c[kind][k].name, 44) + binds(c, kind, +k); }),
        [SEP, '  Total: ' + K.length]).join('\n'); }, 'Display ' + w).cfg = false;
    cmd('*', 'display ' + w + ' gpon profile-id <n>', function (st, a) { var c = C(st), p = c[kind][a[0]]; if (!p) return null; var R = p.run, SEP = '  ' + new Array(77).join('-'),
      o = [SEP, '  Profile-ID          :' + a[0], '  Profile-name        :' + p.name, '  Binding times       :' + binds(c, kind, a[0]), SEP];
      if (kind === 'lp') { Object.keys(R.tc).forEach(function (t) { o.push('  T-CONT ID: ' + t + '  DBA Profile-ID: ' + R.tc[t]); });
        Object.keys(R.gem).forEach(function (g) { o.push('  GEM index: ' + g + '  T-CONT ID: ' + R.gem[g] + R.map.filter(function (m) { return m.g === +g; }).map(function (m) { return '  Mapping index: ' + m.i + ' VLAN: ' + m.v; }).join('')); }); }
      else { o.push('  ONT port: ' + Object.keys(R.ports).map(function (k) { return k + ' ' + R.ports[k]; }).join(' ')); R.pv.forEach(function (x) { o.push('  Port VLAN: ' + x.k + (x.n ? ' ' + x.n : '') + ' VLAN ' + x.v); }); }
      o.push(SEP); return o.join('\n'); }).cfg = false;
  });

  // ---------------------------------------------------------------- PON-порты и ONT (режим interface gpon 0/5)
  function pp(st, p) { var c = C(st); if (p > 7) return null; return c.pon[p] || (c.pon[p] = {}); }
  cmd('gpon', 'port <n> ont-auto-find <w>', function (st, a) { var x = pp(st, a[0]), w = a[1].toLowerCase(); if (!x || ['enable', 'disable'].indexOf(w) < 0) return null; x.af = w === 'enable'; }, 'Port settings');
  cmd('gpon', 'port <n> laser-switch <w>', function (st, a) { var x = pp(st, a[0]), w = a[1].toLowerCase(); if (!x || ['on', 'off'].indexOf(w) < 0) return null; x.off = w === 'off'; });
  function snOk(w) { return /^[0-9a-f]{16}$/i.test(w) ? w.toUpperCase() : null; }
  function addOnt(st, p, o, sn, lp, sp, desc) { var c = C(st); sn = snOk(sn); if (p > 7 || o > 127 || !sn || !c.lp[lp] || !c.sp[sp]) return null;
    var k = '0/5/' + p + '/' + o; if (c.onts[k] || Object.keys(c.onts).some(function (q) { return c.onts[q].sn === sn; })) return null;
    c.onts[k] = { p: p, o: o, sn: sn, lp: lp, sp: sp, desc: desc || null, nv: {}, on: true }; return '  Number of ONTs that can be added: 1, success: 1\n  PortID :' + p + ', ONTID :' + o; }
  ['add <n> <n> sn-auth <w> omci ont-lineprofile-id <n> ont-srvprofile-id <n>', 'confirm <n> ontid <n> sn-auth <w> omci ont-lineprofile-id <n> ont-srvprofile-id <n>'].forEach(function (pat, i) {
    cmd('gpon', 'ont ' + pat, function (st, a) { if (i && !autofind(st, a[0]).some(function (d) { return d.st.hwSn === String(a[2]).toUpperCase(); })) return null; return addOnt(st, a[0], a[1], a[2], a[3], a[4]); }, i ? 'Confirm an auto-found ONT' : 'Add an ONT');
    cmd('gpon', 'ont ' + pat + ' desc <w>', function (st, a) { if (i && !autofind(st, a[0]).some(function (d) { return d.st.hwSn === String(a[2]).toUpperCase(); })) return null; return addOnt(st, a[0], a[1], a[2], a[3], a[4], a[5]); });
  });
  cmd('gpon', 'ont delete <n> <n>', function (st, a) { var c = C(st), k = '0/5/' + a[0] + '/' + a[1]; if (!c.onts[k]) return null;
    if (Object.keys(c.sps).some(function (q) { var s = c.sps[q]; return s.fsp === '0/5/' + a[0] && s.ont === a[1]; })) return null; delete c.onts[k]; return '  Number of ONTs that can be deleted: 1, success: 1'; }, 'Delete an ONT');
  cmd('gpon', 'ont activate <n> <n>', function (st, a) { var x = C(st).onts['0/5/' + a[0] + '/' + a[1]]; if (!x) return null; x.on = true; }, 'Activate an ONT');
  cmd('gpon', 'ont deactivate <n> <n>', function (st, a) { var x = C(st).onts['0/5/' + a[0] + '/' + a[1]]; if (!x) return null; x.on = false; });
  cmd('gpon', 'ont port native-vlan <n> <n> eth <n> vlan <n>', function (st, a) { var x = C(st).onts['0/5/' + a[0] + '/' + a[1]]; if (!x || a[2] < 1 || a[2] > 4 || a[3] < 1 || a[3] > 4095) return null; x.nv[a[2]] = a[3]; }, 'Native VLAN of an ONT port');
  // ONT на PON-порту: подключена оптикой, включена; online — если добавлена её SN, ONT активна, плата Normal, лазер включён
  function peerOnt(st, p) { var net = st.net, pr = net && net.peer(st.dev, '0/5/' + p), d = pr && net.devs[pr.dev]; return d && isHwOnt(d) && pr.port === 'PON' && !d.off ? d : null; }
  function online(st, x) { var c = C(st), d = peerOnt(st, x.p); return !!(d && d.st.hwSn === x.sn && x.on && okB(c, 5) && !(c.pon[x.p] || {}).off) ? d : null; }
  function autofind(st, p) { var c = C(st), d = peerOnt(st, p), x = c.pon[p] || {}; if (!d || !x.af || x.off || !okB(c, 5)) return [];
    return Object.keys(c.onts).some(function (k) { return c.onts[k].sn === d.st.hwSn; }) ? [] : [d]; }
  function ontsOn(st, p) { var c = C(st), L = Object.keys(c.onts).filter(function (k) { return c.onts[k].p === p; }); return { all: L.length, on: L.filter(function (k) { return online(st, c.onts[k]); }).length, keys: L }; }
  function fsp(p) { return '0/ 5/' + p; }
  cmd('gpon', 'display ont autofind <n>', function (st, a) { var L = autofind(st, a[0]), SEP = '   ' + new Array(76).join('-'); if (!L.length) return '';
    var o = [SEP]; L.forEach(function (d, i) { o.push('   Number              : ' + (i + 1), '   F/S/P               : 0/5/' + a[0], '   Ont SN              : ' + d.st.hwSn, '   Password            : 0x00000000000000000000',
      '   Loid                : ', '   Checkcode           : ', '   VendorID            : HWTC', '   Ont Version         : 120D4600', '   Ont SoftwareVersion : V1R006C00S210', '   Ont EquipmentID     : 247',
      '   Ont autofind time   : ' + EL.clock.fmt(EL.clock.now()) + '+08:00', SEP); }); return o.join('\n'); }, 'Display auto-found ONTs').cfg = false;
  function infoAll(st, p) { var c = C(st), S = '  ' + new Array(77).join('-'), L = ontsOn(st, p), o = [S, '  F/S/P   ONT         SN         Control     Run      Config   Match    Protect', '          ID                     flag        state    state    state    side', S];
    L.keys.forEach(function (k) { var x = c.onts[k], on = online(st, x); o.push('  ' + pad(fsp(p), 7) + r(x.o, 4) + '  ' + pad(x.sn, 18) + pad(x.on ? 'active' : 'deactive', 12) + pad(on ? 'online' : 'offline', 9) + pad(on ? 'normal' : 'initial', 9) + pad(on ? 'match' : 'initial', 9) + 'no'); });
    o.push(S, '  F/S/P   ONT-ID   Description', S); L.keys.forEach(function (k) { var x = c.onts[k]; o.push('  ' + pad(fsp(p), 7) + r(x.o, 7) + '   ' + (x.desc || 'ONT_NO_DESCRIPTION')); });
    o.push(S, '  In port ' + fsp(p) + ' , the total of ONTs are: ' + L.all + ', online: ' + L.on); return o.join('\n'); }
  cmd('gpon', 'display ont info <n> all', function (st, a) { return infoAll(st, a[0]); }, 'Display ONT information').cfg = false;
  cmd('cfg', 'display ont info 0 5 <n> all', function (st, a) { return infoAll(st, a[0]); }).cfg = false;
  cmd('*', 'display ont info 0 5 <n> <n>', function (st, a) { var c = C(st), x = c.onts['0/5/' + a[0] + '/' + a[1]]; if (!x) return null; var on = online(st, x), S = '  ' + new Array(78).join('-');
    return [S, '  F/S/P                   : 0/5/' + a[0], '  ONT-ID                  : ' + a[1], '  Control flag            : ' + (x.on ? 'active' : 'deactive'), '  Run state               : ' + (on ? 'online' : 'offline'),
      '  Config state            : ' + (on ? 'normal' : 'initial'), '  Match state             : ' + (on ? 'match' : 'initial'), '  Authentic type          : SN-auth', '  SN                      : ' + x.sn,
      '  Management mode         : OMCI', '  Description             : ' + (x.desc || 'ONT_NO_DESCRIPTION'), S, '  Line profile ID      : ' + x.lp, '  Line profile name    : ' + c.lp[x.lp].name, S,
      '  Service profile ID   : ' + x.sp, '  Service profile name : ' + c.sp[x.sp].name, S].join('\n'); }).cfg = false;
  cmd('gpon', 'display port info <n>', function (st, a) { var x = pp(st, a[0]); if (!x) return null; var S = new Array(57).join('-');
    return [S, pad('F/S/P', 43) + '0/5/' + a[0], pad('Min distance(km)', 43) + '0', pad('Max distance(km)', 43) + '20', pad('Autofind', 43) + (x.af ? 'Enable' : 'Disable'), pad('Admin State', 42) + (x.off ? 'Off' : 'On'), S].join('\n'); }).cfg = false;

  // ---------------------------------------------------------------- VLAN, uplink, service-port
  function vn(v) { return 'VLAN_' + ('000' + v).slice(-4); }
  cmd('cfg', 'vlan <n> <w>', function (st, a) { var t = a[1].toLowerCase(); if (a[0] < 1 || a[0] > 4093 || ['smart', 'standard', 'mux', 'super'].indexOf(t) < 0) return null; C(st).vlans[a[0]] = { type: t }; }, 'Create a VLAN');
  cmd('cfg', 'undo vlan <n>', function (st, a) { var c = C(st); if (Object.keys(c.sps).some(function (k) { return c.sps[k].vlan === a[0]; })) return null; delete c.vlans[a[0]]; });
  cmd('cfg', 'vlan attrib <n> q-in-q', function (st, a) { var v = C(st).vlans[a[0]]; if (!v) return null; v.qinq = true; });
  cmd('cfg', 'port vlan <n> <fs> <n>', function (st, a) { var c = C(st); if (!c.vlans[a[0]] || a[1] !== '0/19' || a[2] > 1) return null; var L = c.upv[a[2]] = c.upv[a[2]] || []; if (L.indexOf(a[0]) < 0) L.push(a[0]); }, 'Add an upstream port to a VLAN');
  cmd('cfg', 'undo port vlan <n> <fs> <n>', function (st, a) { var c = C(st); c.upv[a[2]] = (c.upv[a[2]] || []).filter(function (v) { return v !== a[0]; }); });
  cmd('giu', 'native-vlan <n> vlan <n>', function (st, a) { if (a[0] > 1 || a[1] < 1 || a[1] > 4093) return null; C(st).nv[a[0]] = a[1]; }, 'Native VLAN of an upstream port');
  function spAdd(st, idx, a) { var c = C(st); if (!c.vlans[a[0]] || a[1] !== '0/5/' + a[1].split('/')[2] || +a[1].split('/')[2] > 7 || !c.onts[a[1] + '/' + a[2]]) return null;
    if (idx === null) { idx = 0; while (c.sps[idx]) idx++; } if (idx > 32767) return null;
    c.sps[idx] = { vlan: a[0], fsp: a[1], ont: a[2], gem: a[3], uv: a[4], rx: a[5], tx: a[6] }; }
  var SPP = 'vlan <n> gpon <fsp> ont <n> gemport <n> multi-service user-vlan <n>';
  cmd('cfg', 'service-port <n> ' + SPP, function (st, a) { return spAdd(st, a[0], a.slice(1)); }, 'Create a service port');
  cmd('cfg', 'service-port ' + SPP, function (st, a) { return spAdd(st, null, a); });
  cmd('cfg', 'service-port <n> ' + SPP + ' rx-cttr <n> tx-cttr <n>', function (st, a) { return spAdd(st, a[0], a.slice(1)); });
  cmd('cfg', 'service-port ' + SPP + ' rx-cttr <n> tx-cttr <n>', function (st, a) { return spAdd(st, null, a); });
  cmd('cfg', 'undo service-port <n>', function (st, a) { if (!C(st).sps[a[0]]) return null; delete C(st).sps[a[0]]; }, 'Delete a service port');
  function upVlan(c, v) { return okB(c, 19) && Object.keys(c.upv).some(function (p) { return c.upv[p].indexOf(v) >= 0; }); }
  function spUp(st, s) { var c = C(st), x = c.onts[s.fsp + '/' + s.ont]; return !!(x && online(st, x) && upVlan(c, s.vlan)); }
  cmd('*', 'display service-port all', function (st) { var c = C(st), K = Object.keys(c.sps).map(Number).sort(function (a, b) { return a - b; }), S = '  ' + new Array(78).join('-'), up = 0;
    var o = ['Switch-Oriented Flow List', S, '   INDEX VLAN VLAN     PORT F/ S/ P VPI  VCI   FLOW  FLOW       RX   TX   STATE', '         ID   ATTR     TYPE                    TYPE  PARA', S];
    K.forEach(function (k) { var s = c.sps[k], u = spUp(st, s); if (u) up++; var f = s.fsp.split('/');
      o.push(r(k, 8) + ' ' + pad(s.vlan, 5) + pad('common', 9) + pad('gpon', 5) + pad(f[0] + '/' + f[1] + ' /' + f[2], 8) + pad(s.ont, 5) + pad(s.gem, 6) + pad('vlan', 6) +
        pad(s.uv, 11) + pad(s.rx !== undefined ? s.rx : '-', 5) + pad(s.tx !== undefined ? s.tx : '-', 5) + (u ? 'up' : 'down')); });
    o.push(S, '   Total : ' + K.length + '  (Up/Down :    ' + up + '/' + (K.length - up) + ')'); return o.join('\n'); }, 'Display service ports').cfg = false;
  cmd('*', 'display vlan <n>', function (st, a) { var c = C(st), v = c.vlans[a[0]]; if (!v) return null; var S = '  ' + new Array(32).join('-'), ports = Object.keys(c.upv).filter(function (p) { return c.upv[p].indexOf(a[0]) >= 0; });
    return ['  VLAN ID: ' + a[0], '  VLAN name: ' + vn(a[0]), '  VLAN type: ' + v.type, '  VLAN attribute: ' + (v.qinq ? 'QinQ' : 'common'), '  VLAN description: ', '  VLAN forwarding mode in control board: VLAN-MAC',
      '  VLAN forwarding mode: VLAN-MAC', '  VLAN broadcast packet forwarding policy: forward', '  VLAN unknown multicast packet forwarding policy: forward', '  VLAN unknown unicast packet forwarding policy: forward',
      '  VLAN bind service profile ID: -', '  VLAN bind RAIO profile index: -', '  VLAN priority: -', S, '   F /S /P     Native VLAN  State', S]
      .concat(ports.map(function (p) { return '   0 /19/' + p + r(c.nv[p] || 1, 16) + r(st.net && st.net.linkUp(st.dev, '0/19/' + p) && okB(c, 19) ? 'up' : 'down', 7); }),
        [S, '  Standard port number: ' + ports.length, '  Service virtual port number: ' + Object.keys(c.sps).filter(function (k) { return c.sps[k].vlan === a[0]; }).length]).join('\n'); }, 'Display VLAN').cfg = false;
  cmd('*', 'display version', function (st) { var up = Math.floor((st.net && st.net.now) || 0);
    return ['  VERSION : MA5600V800R013C00', '  PRODUCT : MA5600T', '  Active Mainboard Running Area Information: ', '  --------------------------------------------------', '  Current Program Area : Area A ',
      '  Current Data Area : Area A ', '  Program Area A Version : MA5600V800R013C00 ', '  Program Area B Version : MA5600V800R013C00 ', '  Data Area A Version : MA5600V800R013C00 ',
      '  Data Area B Version : MA5600V800R013C00 ', '  --------------------------------------------------', '  Uptime is 0 day(s), ' + Math.floor(up / 3600) + ' hour(s), ' + Math.floor(up / 60) % 60 + ' minute(s), ' + up % 60 + ' second(s)'].join('\n'); }, 'Display version').cfg = false;
  cmd('priv cfg', 'save', function (st) { O(st).saved = EL.clone(C(st));
    return '  It will take several minutes to save configuration file, please wait...\n  Configuration file had been saved successfully\n  Note: The configuration file will take effect after being activated\n  The data is being saved, please wait a moment...'; }, 'Save the configuration').cfg = false;
  cmd('*', 'display current-configuration', function (st) { return cfgText(st); }, 'Display current configuration').cfg = false;

  // ---------------------------------------------------------------- конфигурация текстом (порядок «Configuration Reference» LG)
  function cfgText(st) { var c = C(st), o = ['#'];
    if (c.sysname) o.push('sysname ' + c.sysname, '#');
    Object.keys(c.dba).forEach(function (k) { var d = c.dba[k]; o.push('dba-profile add profile-id ' + k + (d.name ? ' profile-name ' + d.name : '') + ' ' + d.txt); }); if (Object.keys(c.dba).length) o.push('#');
    Object.keys(c.lp).filter(function (k) { return k !== '0'; }).forEach(function (k) { var p = c.lp[k], R = p.run; o.push('ont-lineprofile gpon profile-id ' + k + ' profile-name ' + p.name);
      Object.keys(R.tc).forEach(function (t) { o.push('tcont ' + t + ' dba-profile-id ' + R.tc[t]); }); Object.keys(R.gem).forEach(function (g) { o.push('gem add ' + g + ' eth tcont ' + R.gem[g]); });
      if (R.mm) o.push('mapping-mode ' + R.mm); R.map.forEach(function (m) { o.push('gem mapping ' + m.g + ' ' + m.i + ' vlan ' + m.v); }); o.push('commit', 'quit', '#'); });
    Object.keys(c.sp).filter(function (k) { return k !== '0'; }).forEach(function (k) { var p = c.sp[k], R = p.run; o.push('ont-srvprofile gpon profile-id ' + k + ' profile-name ' + p.name);
      if (Object.keys(R.ports).length) o.push('ont-port ' + Object.keys(R.ports).map(function (q) { return q + ' ' + R.ports[q]; }).join(' '));
      R.pv.forEach(function (x) { o.push('port vlan ' + x.k + (x.n ? ' ' + x.n : '') + ' ' + x.v); }); o.push('commit', 'quit', '#'); });
    var pons = Object.keys(c.pon).filter(function (p) { return c.pon[p].af || c.pon[p].off; }), on = Object.keys(c.onts);
    if (pons.length || on.length) { o.push('interface gpon 0/5'); pons.forEach(function (p) { if (c.pon[p].af) o.push('port ' + p + ' ont-auto-find enable'); if (c.pon[p].off) o.push('port ' + p + ' laser-switch off'); });
      on.forEach(function (k) { var x = c.onts[k]; o.push('ont add ' + x.p + ' ' + x.o + ' sn-auth ' + x.sn + ' omci ont-lineprofile-id ' + x.lp + ' ont-srvprofile-id ' + x.sp + (x.desc ? ' desc ' + x.desc : ''));
        if (!x.on) o.push('ont deactivate ' + x.p + ' ' + x.o); Object.keys(x.nv).forEach(function (e) { o.push('ont port native-vlan ' + x.p + ' ' + x.o + ' eth ' + e + ' vlan ' + x.nv[e]); }); }); o.push('quit', '#'); }
    Object.keys(c.vlans).forEach(function (v) { o.push('vlan ' + v + ' ' + c.vlans[v].type); if (c.vlans[v].qinq) o.push('vlan attrib ' + v + ' q-in-q'); });
    Object.keys(c.upv).forEach(function (p) { c.upv[p].forEach(function (v) { o.push('port vlan ' + v + ' 0/19 ' + p); }); });
    if (Object.keys(c.nv).length) { o.push('interface giu 0/19'); Object.keys(c.nv).forEach(function (p) { o.push('native-vlan ' + p + ' vlan ' + c.nv[p]); }); o.push('quit'); }
    Object.keys(c.vif).forEach(function (v) { var x = c.vif[v]; o.push('interface vlanif ' + v); if (x.ip) o.push('ip address ' + x.ip[0] + ' ' + x.ip[1]); o.push('quit'); });
    c.routes.forEach(function (q) { var p = q.net.split('/'); o.push('ip route-static ' + p[0] + ' ' + IP.len2mask(+p[1]) + ' ' + q.nh); });
    Object.keys(c.sps).forEach(function (k) { var s = c.sps[k]; o.push('service-port ' + k + ' vlan ' + s.vlan + ' gpon ' + s.fsp + ' ont ' + s.ont + ' gemport ' + s.gem + ' multi-service user-vlan ' + s.uv +
      (s.rx !== undefined ? ' rx-cttr ' + s.rx + ' tx-cttr ' + s.tx : '')); });
    if (Object.keys(c.boards).some(function (s) { return c.boards[s] === 'Normal'; })) o.splice(1, 0, 'board confirm 0', '#');
    o.push('#'); return o.join('\n'); }
  function pad(s, n) { s = String(s); return s.length >= n ? s + ' ' : (s + new Array(n + 1).join(' ')).slice(0, n); }

  // ---------------------------------------------------------------- L2: порты OLT и ONT по конфигурации
  function blank(p) { p.mode = 'general'; p.gtag = []; p.guntag = []; p.pvid = 4095; }
  P.hwOltSync = function () {
    var s = this;
    this.list().filter(isO).forEach(function (d) { var st = d.st, c = C(st), V = {};
      Object.keys(st.ports).forEach(function (k) { blank(st.ports[k]); });
      if (okB(c, 19)) UP.forEach(function (n, i) { var p = st.ports[n], L = (c.upv[i] || []).filter(function (v) { return c.vlans[v]; }); p.gtag = L.slice(); L.forEach(function (v) { V[v] = 1; });
        var nv = c.nv[i]; if (nv && L.indexOf(nv) >= 0) { p.gtag = L.filter(function (v) { return v !== nv; }); p.guntag = [nv]; p.pvid = nv; } });
      Object.keys(c.onts).forEach(function (k) { var x = c.onts[k], od = online(st, x); if (!od) return; var lp = c.lp[x.lp].run, sp = c.sp[x.sp].run, op = od.st.ports;
        Object.keys(c.sps).forEach(function (q) { var sv = c.sps[q]; if (sv.fsp + '/' + sv.ont !== k || !c.vlans[sv.vlan]) return;
          if (lp.gem[sv.gem] === undefined || !lp.map.some(function (m) { return m.g === sv.gem && m.v === sv.uv; })) return;   // GEM и C-VLAN должны быть в линейном профиле
          var eth = sp.pv.filter(function (y) { return y.k === 'eth' && y.v === sv.uv && op['ETH' + y.n]; }); if (!eth.length) return;
          var pn = st.ports[x.fsp || '0/5/' + x.p]; if (pn.gtag.indexOf(sv.vlan) < 0) pn.gtag.push(sv.vlan); V[sv.vlan] = 1;
          if (op.PON.gtag.indexOf(sv.vlan) < 0) op.PON.gtag.push(sv.vlan);
          eth.forEach(function (y) { var L = op['ETH' + y.n]; if (x.nv[y.n] === sv.uv) { L.guntag = [sv.vlan]; L.pvid = sv.vlan; } else if (L.gtag.indexOf(sv.vlan) < 0) L.gtag.push(sv.vlan); });
          od.st.vlans[sv.vlan] = '-'; }); });
      st.vlans = { 1: 'default' }; Object.keys(c.vlans).forEach(function (v) { st.vlans[v] = vn(v); });
      st.svi = {}; Object.keys(c.vif).forEach(function (v) { var x = c.vif[v]; if (x.ip && c.vlans[v]) st.svi[v] = x.ip[0] + '/' + x.ip[1]; });
      st.routes = c.routes.map(function (q) { return { net: q.net, nh: q.nh, ad: 1 }; }); st.gw = null; st.host = c.sysname || O(st).model; });
    this.hwOltGen = this.gen;
  };
  // ONT Huawei сбрасываются общей синхронизацией olt.js (они не на OLT Eltex) — порты задаём заново после неё
  function ontReset(net) { net.list().filter(isHwOnt).forEach(function (o) { Object.keys(o.st.ports).forEach(function (k) { blank(o.st.ports[k]); }); o.st.vlans = { 1: 'default' }; }); }
  var os0 = P.oltSync;
  P.oltSync = function () { var r = os0 ? os0.apply(this, arguments) : undefined; ontReset(this); this.hwOltSync(); return r; };
  var fl0 = P.flood;
  P.flood = function () { if (this.hwOltGen !== this.gen && this.list().some(isO)) { ontReset(this); this.hwOltSync(); } return fl0.apply(this, arguments); };
  // оптика PON: PON-порт OLT (0/5/N) ↔ порт PON ONT
  function isPon(net, id, port) { return isO(net.devs[id]) && PON.indexOf(port) >= 0; }
  var dc0 = P.defaultCable;
  P.defaultCable = function (a, ap, b, bp) { return isPon(this, a, ap) || isPon(this, b, bp) ? 'pon' : dc0.apply(this, arguments); };
  var ph0 = P.phys;
  P.phys = function (id, port) { var pr = this.peer(id, port); if (!pr) return ph0.apply(this, arguments);
    var mine = isPon(this, id, port), his = isPon(this, pr.dev, pr.port); if (!mine && !his) return ph0.apply(this, arguments);
    var other = mine ? pr : { dev: id, port: port }, l = this.links[pr.li], cab = l.cab || this.defaultCable(l.a.dev, l.a.port, l.b.dev, l.b.port);
    if (cab !== 'pon' || other.port !== 'PON' || isPon(this, other.dev, other.port)) return { up: false, why: 'оптика PON соединяет PON-порт OLT с портом PON ONT', dup: {} };
    return { up: true, cab: 'pon', speed: 1000, dup: {}, mismatch: false }; };

  // ---------------------------------------------------------------- устройства
  var n0 = 0;
  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}, st = d.st;
    if (m.kind === 'hwolt') { d.sub = 'hwolt'; st.stp = { on: false }; st.hwo = { model: model, mode: 'user', ctx: null, c: fresh(), saved: null, ask: null }; st.users = { root: { pw: 'admin', priv: 15 } }; st.host = model; }
    if (m.kind === 'ont' && m.hw) { n0++; st.hwSn = '48575443' + ('00000000' + ((0xD8EA0000 + n0 * 0x1F3 + (+String(d.id).slice(1) || 0) * 7) >>> 0).toString(16).toUpperCase()).slice(-8); st.serial = st.hwSn; st.host = d.name; }
    return d; };
  var ex0 = P.exec, pr0 = P.prompt, he0 = P.help, tb0 = P.tab;
  P.exec = function (id, line) { var d = this.devs[id]; if (!isO(d)) return ex0.apply(this, arguments); this.gen++; return d.off ? '' : exec(d.st, line); };
  P.prompt = function (id) { var d = this.devs[id]; return isO(d) ? prompt(d.st) : pr0.apply(this, arguments); };
  P.help = function (id, line) { var d = this.devs[id]; return isO(d) ? exec(d.st, String(line).replace(/\s*$/, '') + ' ?') : he0.apply(this, arguments); };
  P.tab = function (id, line) { var d = this.devs[id]; if (!isO(d)) return tb0.apply(this, arguments); var t = String(line).split(/\s+/), part = t.pop(), L = nextWords(d.st, t.filter(Boolean)).filter(function (w) { return /<K>$/.test(w) && w.indexOf(part.toLowerCase()) === 0; });
    return part && L.length === 1 ? t.concat([L[0].slice(0, -3)]).join(' ') + ' ' : null; };
  var sh0 = P.setHost;
  P.setHost = function (id, name) { var d = this.devs[id]; if (!isO(d)) return sh0.apply(this, arguments); C(d.st).sysname = name; d.st.host = name; this.gen++; };
  var rb0 = P.reboot;
  P.reboot = function (id) { var d = this.devs[id], keep = isO(d) ? { hwo: d.st.hwo, users: d.st.users } : null, ks = isHwOnt(d) ? d.st.hwSn : null, r = rb0.apply(this, arguments); d = this.devs[id];
    if (keep) { var o = keep.hwo; o.c = o.saved ? EL.clone(o.saved) : fresh(); o.mode = 'user'; o.ctx = null; o.ask = null; d.st.hwo = o; d.st.users = keep.users; d.st.stp = { on: false }; d.st.host = o.c.sysname || o.model; }
    if (ks) { d.st.hwSn = ks; d.st.serial = ks; } this.gen++; return r; };
  if (EL.cfgText) { var ct0 = EL.cfgText; EL.cfgText = function (d) { return isO(d) ? cfgText(d.st) : ct0.apply(this, arguments); }; }
  if (EL.applyConfig) { var ap0 = EL.applyConfig; EL.applyConfig = function (n, id, text) { var d = n.devs[id]; if (!isO(d)) return ap0.apply(this, arguments);
    var errs = [], x = d.st.hwo; x.mode = 'config'; String(text).split('\n').forEach(function (l) { l = l.trim(); if (!l || l === '#') return; var res = n.exec(id, l); if (/^\{/.test(res)) errs.push(d.name + ' «' + l + '» → ' + res); });
    x.mode = 'priv'; return errs; }; }
  EL.hwolt = { cfgText: cfgText };
})(typeof window !== 'undefined' ? window : global);
