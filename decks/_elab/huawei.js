/* Huawei VRP в эмуляторе (спецификации sources/huawei/spec: vrp-common, s-switch, ar-router; главный источник —
   HCIA-Datacom Lab Guide (рус.), снят на S5731-H/AR651C, недостающее — справочники Huawei S/AR V200R0xx).
   Устройства Huawei живут в общей модели сети: коммутатор S — тип 'mes' (те же поля ports/vlans/svi/stp/mst/pos, что у MES),
   маршрутизатор AR — тип 'esr' (тот же st.run, что у ESR). Поэтому кадры, STP, LACP, RIP/OSPF, VRRP, NAT, захват и трасса
   работают и в смешанных схемах Eltex + Huawei. Здесь — общее VRP: виды и приглашения (<Huawei>, [Huawei], [Huawei-GigabitEthernet0/0/1]),
   сокращения слов, «?» и Tab, undo, quit/return, intelligent rollback (команда system view из вида интерфейса), display, save с вопросом [Y/N],
   reboot, ping/tracert в формате VRP. Настройки хранятся в своей схеме st.vrp.c; после каждой команды compile переносит их в модель сети.
   Команды применяются сразу (commit нет); save — загрузочная конфигурация, её же поднимает reboot.
   Ошибки ввода: в документации есть только «Error: Unrecognized command found at '^' position.» — он и выводится
   (тексты Incomplete/Ambiguous/Wrong parameter в собранных источниках не найдены). */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip;
  var GROUP = 'Huawei (как в eNSP)';
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  // порты — нумерация по документации Huawei (слот/подкарта/порт, своя для каждой скорости); набор как в eNSP (по методичкам, у Huawei не описан)
  [['S5700', { type: 'mes', kind: 'hw-s', portList: range('GE0/0/', 1, 24), note: 'Коммутатор Huawei S5700 (VRP): 24 × GigabitEthernet0/0/1–24, как в eNSP' }],
   ['S3700', { type: 'mes', kind: 'hw-s', portList: range('Eth0/0/', 1, 22).concat(range('GE0/0/', 1, 2)), note: 'Коммутатор Huawei S3700 (VRP): 22 × Ethernet0/0/1–22 + 2 × GigabitEthernet0/0/1–2, как в eNSP' }],
   ['AR2220', { type: 'esr', kind: 'hw-ar', portList: range('GE0/0/', 0, 2), note: 'Маршрутизатор Huawei AR2220 (VRP): GigabitEthernet0/0/0–2, как в eNSP' }],
   ['AR1220', { type: 'esr', kind: 'hw-ar', portList: range('GE0/0/', 0, 1).concat(range('Eth0/0/', 0, 7)), note: 'Маршрутизатор Huawei AR1220 (VRP): 2 × GE0/0/0–1 (L3) + 8 × Ethernet0/0/0–7 (L2, в L3 — undo portswitch)' }]
  ].forEach(function (x) { var m = x[1]; m.ports = m.portList.length; m.group = GROUP; m.vendor = 'huawei'; m.host = 'Huawei';
    m.login = [{ u: '—', p: '—', a: 'консоль без пароля (как в eNSP)' }]; EL.MODELS[x[0]] = m; });

  function isVrp(d) { return !!d && d.sub === 'vrp'; }
  function dports(net, d) { return net.portsOf(d).filter(function (p) { return /^(GE|Eth)\d/.test(p); }); }   // порты данных (без console/aux)
  // ---------------------------------------------------------------- имена интерфейсов
  var FULL = { GE: 'GigabitEthernet', Eth: 'Ethernet' };
  function full(n) { var m = String(n).match(/^(GE|Eth)(\d.*)$/); if (m) return FULL[m[1]] + m[2];
    if (/^po\d+$/.test(n)) return 'Eth-Trunk' + n.slice(2); if (/^lo\d+$/.test(n)) return 'LoopBack' + n.slice(2);
    if (/^vlan\d+$/.test(n)) return 'Vlanif' + n.slice(4); return n; }
  function short(n) { return String(n).replace(/^GigabitEthernet/, 'GE').replace(/^Ethernet/, 'Eth'); }
  function pre(w, kw, min) { return w.length >= (min || 1) && kw.indexOf(w) === 0; }
  // строка → токены; «GigabitEthernet 0/0/1», «g0/0/1», «GE0/0/1» → GE0/0/1; после interface — Vlanif10, Eth-Trunk1, LoopBack0
  function norm(line) {
    var t = String(line).trim().split(/\s+/).filter(Boolean), o = [];
    for (var i = 0; i < t.length; i++) {
      var w = t[i], low = w.toLowerCase(), m = low.match(/^([a-z]+)(\d+\/\d+\/\d+(?:\.\d+)?)$/), nx = t[i + 1];
      var ifCtx = o.length && pre(o[o.length - 1].toLowerCase(), 'interface', 2);
      if (m && (pre(m[1], 'gigabitethernet') || m[1] === 'ge')) { o.push('GE' + m[2]); continue; }
      if (m && pre(m[1], 'ethernet')) { o.push('Eth' + m[2]); continue; }
      if (/^[a-z]+$/.test(low) && nx && /^\d+\/\d+\/\d+(\.\d+)?$/.test(nx) && (pre(low, 'gigabitethernet') || low === 'ge')) { o.push('GE' + nx); i++; continue; }
      if (/^[a-z]+$/.test(low) && nx && /^\d+\/\d+\/\d+(\.\d+)?$/.test(nx) && pre(low, 'ethernet')) { o.push('Eth' + nx); i++; continue; }
      if ((m = low.match(/^vlanif(\d+)$/))) { o.push('Vlanif' + m[1]); continue; }
      if ((m = low.match(/^eth-trunk(\d+)$/))) { o.push('Eth-Trunk' + m[1]); continue; }
      if ((m = low.match(/^loopback(\d+)$/))) { o.push('LoopBack' + m[1]); continue; }
      if (ifCtx && nx && /^\d+$/.test(nx)) {
        if (pre(low, 'vlanif', 5)) { o.push('Vlanif' + nx); i++; continue; }
        if (/^eth-t/.test(low) && pre(low, 'eth-trunk')) { o.push('Eth-Trunk' + nx); i++; continue; }
        if (pre(low, 'loopback', 4)) { o.push('LoopBack' + nx); i++; continue; }
      }
      o.push(w);
    }
    return o;
  }

  // ---------------------------------------------------------------- таблица команд
  // шаблон: слова — ключевые (сокращаются до любого однозначного начала), <n> число, <w> слово, <ip> адрес, <mask> маска или длина,
  // <if> интерфейс (GE0/0/1, Eth0/0/1, Vlanif10, Eth-Trunk1, LoopBack0, GE0/0/1.10), <vl> список VLAN «2 to 3 10» до конца строки, <rest> остаток
  var T = [];
  function cmd(views, pat, run, d) { var e = { v: views.split(' '), p: pat.split(' '), run: run, d: d || '' }; T.push(e); return e; }
  function isIf(t) { return /^(GE|Eth)\d+\/\d+\/\d+(\.\d+)?$|^(Vlanif|Eth-Trunk|LoopBack)\d+$/.test(t); }
  function vlist(toks) { var o = [], i = 0; if (!toks.length) return null;
    while (i < toks.length) { var a = toks[i]; if (!/^\d+$/.test(a)) return null; a = +a;
      if (toks[i + 1] && pre(toks[i + 1].toLowerCase(), 'to', 1) && /^\d+$/.test(toks[i + 2] || '')) { for (var v = a; v <= +toks[i + 2]; v++) o.push(v); i += 3; }
      else { o.push(a); i++; } }
    return o.every(function (v) { return v >= 1 && v <= 4094; }) ? o : null; }
  function tokOk(p, t) {
    if (p === '<n>') return /^\d+$/.test(t); if (p === '<w>') return true; if (p === '<ip>') return IP.ip2n(t) !== null;
    if (p === '<mask>') return /^\d{1,2}$/.test(t) && +t <= 32 || IP.mask2len(t) !== null;
    if (p === '<if>') return isIf(t);
    return pre(t.toLowerCase(), p);
  }
  function match(p, toks) {
    var a = [], ex = 0;
    for (var k = 0; k < p.length; k++) {
      if (p[k] === '<rest>') { if (k >= toks.length) return null; a.push(toks.slice(k).join(' ')); return { a: a, ex: ex }; }
      if (p[k] === '<vl>') { var l = vlist(toks.slice(k)); if (!l) return null; a.push(l); return { a: a, ex: ex }; }
      var t = toks[k]; if (t === undefined || !tokOk(p[k], t)) return null;
      if (p[k].charAt(0) === '<') a.push(p[k] === '<n>' ? +t : p[k] === '<mask>' ? (/^\d+$/.test(t) ? +t : IP.mask2len(t)) : t);
      else if (t.toLowerCase() === p[k]) ex++;
    }
    return toks.length === p.length ? { a: a, ex: ex } : null;
  }
  function inView(e, v) { return e.v.indexOf(v) >= 0 || e.v.indexOf('*') >= 0 || (e.v.indexOf('cfg') >= 0 && v !== 'user'); }
  function find(st, v, toks) {
    var best = null;
    T.forEach(function (e) { if (!inView(e, v) || (e.ok && !e.ok(st))) return; var r = match(e.p, toks); if (r && (!best || r.ex > best.r.ex)) best = { e: e, r: r }; });
    return best;
  }
  // на каком слове ошибка: самое длинное начало строки, которое подходит хоть к одному шаблону вида
  function errAt(st, v, toks) {
    var k = 0;
    T.forEach(function (e) { if (!inView(e, v)) return; var i = 0; while (i < toks.length && i < e.p.length && e.p[i] !== '<rest>' && e.p[i] !== '<vl>' && tokOk(e.p[i], toks[i])) i++;
      if (e.p[i] === '<rest>' || e.p[i] === '<vl>') i = toks.length; if (i > k) k = i; });
    return k;
  }
  function errText(st, raw, toks, k) {
    var pr = prompt(st), pos = 0, s = String(raw), at = 0;
    for (var i = 0; i < toks.length && i <= k; i++) { var w = s.slice(at).match(/\S+/); if (!w) break; pos = at + w.index; at = pos + w[0].length; }
    if (k >= toks.length) pos = s.replace(/\s+$/, '').length + 1;
    return new Array(pr.length + pos + 1).join(' ') + '^\nError: Unrecognized command found at \'^\' position.';
  }

  // ---------------------------------------------------------------- виды и приглашения
  function V(st) { return st.vrp; }
  function top(st) { var s = V(st).stack; return s[s.length - 1] || { v: 'user' }; }
  function host(st) { return V(st).c.sysname || 'Huawei'; }
  var VP = { sys: '', 'if': null, vlan: 'vlan', mst: 'mst-region', ui: null, aaa: 'aaa', ospf: null, area: null, rip: null, acl: null, pool: null, group: 'port-group' };
  function prompt(st) {
    var x = V(st); if (x.ask) return '';
    var t = top(st), h = host(st);
    if (t.v === 'user') return '<' + h + '>';
    var s = t.v === 'sys' ? '' : t.v === 'if' ? full(t.name) : t.v === 'vlan' ? 'vlan' + t.id : t.tag || VP[t.v];
    return '[' + h + (s ? '-' + s : '') + ']';
  }
  function push(st, f) { V(st).stack.push(f); }
  // ---------------------------------------------------------------- исполнение строки
  function exec(st, raw) {
    var x = V(st);
    if (x.ask) { var a = x.ask; x.ask = null; return /^y(es)?$/i.test(String(raw).trim()) ? a.yes() : (a.no ? a.no() : ''); }
    var line = String(raw).replace(/\s+$/, '');
    if (!line.trim()) return '';
    if (/\?$/.test(line)) return help(st, line.slice(0, -1));
    var toks = norm(line), v = top(st).v, hit = find(st, v, toks);
    if (!hit && v !== 'user' && v !== 'sys') {             // intelligent rollback: команда верхнего вида выполняется, вид меняется на него
      for (var i = x.stack.length - 2; i >= 0 && !hit; i--) { var h2 = find(st, x.stack[i].v, toks); if (h2 && h2.e.v.indexOf('*') < 0) { x.stack = x.stack.slice(0, i + 1); hit = h2; } }
    }
    if (!hit) return errText(st, line, toks, errAt(st, v, toks));
    var r = hit.e.run(st, hit.r.a, toks);
    if (r === null) return errText(st, line, toks, toks.length - 1);        // параметр вне допустимого — ошибка под последним словом
    if (hit.e.cfg !== false && v !== 'user') compile(st);
    return r === undefined || r === null ? '' : r;
  }
  function compile(st) { var k = V(st).kind; (k === 'ar' ? EL.vrp.compileAr : EL.vrp.compileS)(st); if (st.net) st.net.gen++; }
  // «?» — варианты следующего слова (после пробела) или слова с этим началом
  var PH = { '<n>': 'INTEGER', '<w>': 'STRING', '<ip>': 'IP_ADDR<X.X.X.X>', '<mask>': 'INTEGER<0-32>', '<if>': 'Interface', '<vl>': 'INTEGER<1-4094>', '<rest>': 'STRING' };
  function cands(st, txt) {
    var ends = /\s$/.test(txt) || !txt.trim(), toks = txt.trim() ? norm(txt) : [], part = ends ? null : toks.pop(), v = top(st).v, out = [], seen = {}, cr = false;
    T.forEach(function (e) { if (!inView(e, v) || (e.ok && !e.ok(st))) return;
      for (var k = 0; k < toks.length; k++) { if (e.p[k] === '<rest>' || e.p[k] === '<vl>') return; if (k >= e.p.length || !tokOk(e.p[k], toks[k])) return; }
      if (toks.length === e.p.length && ends) { cr = true; return; }
      var p = e.p[toks.length]; if (!p) return;
      if (p.charAt(0) === '<') { if (part === null && !seen[p]) { seen[p] = 1; out.push([PH[p] || p, e.d && toks.length === e.p.length - 1 ? e.d : '']); } return; }
      if (part !== null && !pre(part.toLowerCase(), p)) return;
      if (!seen[p]) { seen[p] = 1; out.push([p, toks.length === 0 ? e.d : '']); } });
    if (cr) out.push(['<cr>', '']);
    return { list: out, part: part };
  }
  function help(st, txt) {
    var c = cands(st, txt);
    if (!c.list.length) return errText(st, txt, norm(txt), errAt(st, top(st).v, norm(txt)));
    return c.list.map(function (x) { return '  ' + (x[0] + '                        ').slice(0, Math.max(24, x[0].length + 2)) + x[1]; }).join('\n');
  }
  function tab(st, txt) {
    var c = cands(st, txt), kw = c.list.filter(function (x) { return x[0].charAt(0) !== '<' && !/^[A-Z_]+/.test(x[0]); });
    if (c.part === null || kw.length !== 1) return null;
    return txt.replace(/\S+$/, kw[0][0]) + ' ';
  }

  // ---------------------------------------------------------------- общие команды
  function vlTxt(a) {                            // [2,3,10] → «2 to 3 10»
    a = a.slice().sort(function (x, y) { return x - y; }).filter(function (x, i, s) { return s.indexOf(x) === i; });
    var r = [], i = 0; while (i < a.length) { var j = i; while (j + 1 < a.length && a[j + 1] === a[j] + 1) j++; r.push(j > i ? a[i] + ' to ' + a[j] : '' + a[i]); i = j + 1; }
    return r.join(' ');
  }
  function ifc(st, n) { var c = V(st).c; return c.ifs[n] || (c.ifs[n] = {}); }
  function cur(st) { var t = top(st); return t.v === 'if' ? (t.names || [t.name]).map(function (n) { return ifc(st, n); }) : []; }
  cmd('user', 'system-view', function (st) { push(st, { v: 'sys' }); return 'Enter system view, return user view with Ctrl+Z.'; }, 'Enter the system view');
  cmd('*', 'quit', function (st) { var x = V(st); if (x.stack.length) x.stack.pop(); }, 'Exit from current mode and enter prior mode');
  cmd('*', 'return', function (st) { V(st).stack = []; }, 'Enter the privileged mode');
  cmd('sys', 'sysname <w>', function (st, a) { V(st).c.sysname = a[0]; }, 'Set the name of the host');
  cmd('sys', 'undo sysname', function (st) { delete V(st).c.sysname; });
  cmd('if', 'description <rest>', function (st, a) { cur(st).forEach(function (x) { x.desc = a[0]; }); }, 'Describe the interface');
  cmd('if', 'undo description', function (st) { cur(st).forEach(function (x) { delete x.desc; }); });
  cmd('if', 'shutdown', function (st) { cur(st).forEach(function (x) { x.shut = true; }); }, 'Shut down this interface');
  cmd('if', 'undo shutdown', function (st) { cur(st).forEach(function (x) { delete x.shut; }); });
  cmd('sys', 'interface <if>', function (st, a) {
    var n = a[0], x = V(st), ports = st.net ? EL.vrp.dports(st.net, st.net.devs[st.dev]) : [], ph = n.split('.')[0];
    if (/^(GE|Eth)\d/.test(n) && ports.indexOf(ph) < 0) return null;
    if (n.indexOf('.') > 0 && x.kind !== 'ar') return null;
    if (/^Vlanif/.test(n) && (x.kind !== 's' || +n.slice(6) < 1 || +n.slice(6) > 4094)) return null;
    ifc(st, n); push(st, { v: 'if', name: n });
  }, 'Specify the interface configuration view');
  cmd('sys', 'interface range <if> to <if>', function (st, a) {
    var ports = st.net ? EL.vrp.dports(st.net, st.net.devs[st.dev]) : [], i = ports.indexOf(a[0]), j = ports.indexOf(a[1]);
    if (i < 0 || j < i) return null; var L = ports.slice(i, j + 1); L.forEach(function (n) { ifc(st, n); }); push(st, { v: 'if', name: L[0], names: L, tag: 'port-group' });
  });
  cmd('sys', 'undo interface <if>', function (st, a) { if (/^(GE|Eth)\d+\/\d+\/\d+$/.test(a[0])) return null; delete V(st).c.ifs[a[0]]; });
  // AAA, консоль и VTY: хранятся и показываются в конфигурации (вход по Telnet в модели не проверяется)
  cmd('sys', 'user-interface console 0', function (st) { push(st, { v: 'ui', key: 'console 0', tag: 'ui-console0' }); });
  cmd('sys', 'user-interface vty <n> <n>', function (st, a) { push(st, { v: 'ui', key: 'vty ' + a[0] + ' ' + a[1], tag: 'ui-vty' + a[0] + '-' + a[1] }); });
  function ui(st) { var c = V(st).c, k = top(st).key; c.ui = c.ui || {}; return c.ui[k] || (c.ui[k] = {}); }
  cmd('ui', 'authentication-mode <w>', function (st, a) { var m = a[0].toLowerCase(); if (['aaa', 'password', 'none'].indexOf(m) < 0) return null; ui(st).auth = m;
    if (m === 'password') return 'Warning: The "password" authentication mode is not secure, and it is strongly re\ncommended to use "aaa" authentication mode.'; });
  cmd('ui', 'set authentication password cipher <w>', function (st, a) { ui(st).pw = a[0]; });
  cmd('ui', 'user privilege level <n>', function (st, a) { if (a[0] > 15) return null; ui(st).lvl = a[0]; });
  cmd('ui', 'idle-timeout <n>', function (st, a) { ui(st).idle = a[0]; });
  cmd('ui', 'protocol inbound <w>', function (st, a) { ui(st).proto = a[0].toLowerCase(); });
  cmd('sys', 'aaa', function (st) { push(st, { v: 'aaa' }); });
  function lu(st, u) { var c = V(st).c; c.users = c.users || {}; return c.users[u] || (c.users[u] = {}); }
  cmd('aaa', 'local-user <w> password cipher <w>', function (st, a) { var n = !(V(st).c.users || {})[a[0]]; lu(st, a[0]).pw = a[1]; if (n) return 'Info: Add a new user.'; });
  cmd('aaa', 'local-user <w> service-type <rest>', function (st, a) { lu(st, a[0]).svc = a[1]; });
  cmd('aaa', 'local-user <w> privilege level <n>', function (st, a) { lu(st, a[0]).lvl = a[1]; });
  cmd('sys', 'telnet server enable', function (st) { V(st).c.telnet = true; return 'Info: TELNET server has been enabled.'; });
  cmd('sys', 'undo telnet server enable', function (st) { V(st).c.telnet = false; });
  cmd('user', 'undo terminal monitor', function () { return 'Info: Current terminal monitor is off.'; }).cfg = false;
  cmd('sys', 'undo info-center enable', function (st) { V(st).c.noInfo = true; });
  cmd('sys', 'info-center enable', function (st) { delete V(st).c.noInfo; return 'Info: Information center is enabled.'; });
  // статика: preference по умолчанию 60
  function rt(st, a, pref) { var nh = a[2]; if (!IP.ip2n(nh) && nh !== undefined) return null; var c = V(st).c; c.routes = (c.routes || []).filter(function (r) { return !(r.net === IP.netOf(a[0], a[1]) && r.nh === nh); });
    c.routes.push({ net: IP.netOf(a[0], a[1]), nh: nh, pref: pref || 60 }); }
  cmd('sys', 'ip route-static <ip> <mask> <ip>', function (st, a) { return rt(st, a); }, 'Establish static routes');
  cmd('sys', 'ip route-static <ip> <mask> <ip> preference <n>', function (st, a) { if (a[3] < 1 || a[3] > 255) return null; return rt(st, a, a[3]); });
  cmd('sys', 'ip route-static <ip> <mask> <if> <ip>', function (st, a) { return rt(st, [a[0], a[1], a[3]]); });
  cmd('sys', 'undo ip route-static <ip> <mask> <ip>', function (st, a) { var c = V(st).c, n = IP.netOf(a[0], a[1]); c.routes = (c.routes || []).filter(function (r) { return !(r.net === n && r.nh === a[2]); }); });
  cmd('sys', 'undo ip route-static <ip> <mask>', function (st, a) { var c = V(st).c, n = IP.netOf(a[0], a[1]); c.routes = (c.routes || []).filter(function (r) { return r.net !== n; }); });

  // ---------------------------------------------------------------- конфигурация: display, save, reboot
  function cfgText(st, only) {
    var x = V(st), c = x.c, o = [], blk = function (L) { o.push('#'); L.forEach(function (l) { o.push(l); }); };
    if (!only) { blk(['sysname ' + host(st)]); }
    var parts = (x.kind === 'ar' ? EL.vrp.renderAr : EL.vrp.renderS)(st);
    parts.forEach(function (p) { if (!only || p.h === only) blk(p.L); });
    if (!only) {
      if (c.telnet) blk(['telnet server enable']);
      if (c.users) blk(['aaa'].concat([].concat.apply([], Object.keys(c.users).map(function (u) { var y = c.users[u];
        return [' local-user ' + u + ' password cipher ' + (y.pw || '')].concat(y.lvl !== undefined ? [' local-user ' + u + ' privilege level ' + y.lvl] : [], y.svc ? [' local-user ' + u + ' service-type ' + y.svc] : []); }))));
      var U = c.ui || {}; o.push('#');
      ['console 0', 'vty 0 4'].concat(Object.keys(U).filter(function (k) { return k !== 'console 0' && k !== 'vty 0 4'; })).forEach(function (k) { var y = U[k] || {};
        o.push('user-interface ' + (k === 'console 0' ? 'con 0' : k));
        if (y.auth) o.push(' authentication-mode ' + y.auth); if (y.pw) o.push(' set authentication password cipher ' + y.pw);
        if (y.lvl !== undefined) o.push(' user privilege level ' + y.lvl); if (y.idle !== undefined) o.push(' idle-timeout ' + y.idle);
        if (y.proto) o.push(' protocol inbound ' + y.proto); });
    }
    o.push('#'); o.push('return');
    return o.join('\n');
  }
  function thisText(st) { var t = top(st);
    if (t.v === 'if') return cfgText(st, 'interface ' + full(t.name)).replace(/\nreturn$/, '\nreturn');
    if (t.v === 'sys' || t.v === 'user') return cfgText(st);
    var hd = { ospf: 'ospf', rip: 'rip', acl: 'acl', pool: 'pool', aaa: 'aaa', mst: 'mst' }[t.v]; return hd ? cfgText(st, t.key || hd) : '#\nreturn'; }
  cmd('*', 'display current-configuration', function (st) { return cfgText(st); }, 'Current configuration');
  cmd('*', 'display current-configuration | include <rest>', function (st, a) { var re = a[0]; return cfgText(st).split('\n').filter(function (l) { return l.indexOf(re) >= 0; }).join('\n'); });
  cmd('*', 'display saved-configuration', function (st) { var x = V(st); if (!x.saved) return ''; var c0 = x.c; x.c = x.saved; try { return cfgText(st); } finally { x.c = c0; } });
  cmd('*', 'display this', function (st) { return thisText(st); }, 'Display the current view configuration');
  cmd('*', 'display version', function (st) {
    var d = st.net && st.net.devs[st.dev], m = d ? d.model : '', ar = V(st).kind === 'ar';
    return 'Huawei Versatile Routing Platform Software\nVRP (R) software, Version 5.' + (ar ? '1' : '') + '\nCopyright (C) 2000-2017 HUAWEI TECH Co., Ltd.\n' +
      'Huawei ' + m + (ar ? ' Router' : ' Routing Switch') + ' uptime is 0 week, 0 day, 0 hour, ' + Math.floor(((st.net && st.net.now) || 0) / 60) + ' minutes';
  });
  cmd('user', 'save', function (st) { var x = V(st), ar = x.kind === 'ar';
    x.ask = { yes: function () { x.saved = EL.clone(x.c);
      return ar ? '  It will take several minutes to save configuration file, please wait.......\n  Configuration file had been saved successfully\n  Note: The configuration file will take effect after being activated'
                : 'Now saving the current configuration to the slot 0..\nSave the configuration successfully.'; } };
    return ar ? '  The current configuration will be written to the device.\n  Are you sure to continue? .(y/n)[n]:' : 'The current configuration will be written to the device.\nAre you sure to continue?[Y/N]';
  }, 'Save the current configuration').cfg = false;
  cmd('user', 'compare configuration', function (st) { var x = V(st);
    return JSON.stringify(x.c) === JSON.stringify(x.saved || fresh(x.kind)) ? ' The current configuration is the same as the next startup configuration file.' : ' The current configuration is NOT the same as the next startup configuration file.'; }).cfg = false;
  cmd('user', 'reset saved-configuration', function (st) { var x = V(st), ar = x.kind === 'ar';
    x.ask = { yes: function () { x.saved = null; return ar ? ' Clear the configuration in the device successfully.' : 'Warning: Now clearing the configuration in the device.\nInfo: Succeeded in clearing the configuration in the device.'; } };
    return ar ? 'This will delete the configuration in the flash memory.\nThe device configurations will be erased to reconfigure.\nAre you sure? (y/n)[n]:'
              : 'Warning: The action will delete the saved configuration in the device.\nThe configuration will be erased to reconfigure. Continue? [Y/N]:';
  }).cfg = false;
  cmd('user', 'reboot', function (st) { var x = V(st), ar = x.kind === 'ar';
    x.ask = { yes: function () { if (st.net) st.net.reboot(st.dev); return ar ? 'Info: system is rebooting ,please wait...\nThe system is restarting.' : ''; } };
    return ar ? 'Info: The system is comparing the configuration, please wait.\nSystem will reboot! Continue ? [y/n]:' : 'Info: The system is now comparing the configuration, please wait........\nSystem will reboot! Continue?[Y/N]:';
  }).cfg = false;

  // ---------------------------------------------------------------- ping / tracert (CR j04u, HCIA-LG с. 26, 76)
  function ms(seed, i) { return 1 + ((seed * 7 + i * 13) % 29); }
  function ping(st, dst, n) {
    var net = st.net; if (!net) return '';
    if (IP.ip2n(dst) === null) return null;
    var r = net.ping(st.dev, dst), o = ['  PING ' + dst + ': 56  data bytes, press CTRL_C to break'], got = 0, cnt = n || 5;
    if (net.onTrace) net.onTrace(r, st.dev, dst);
    var rd = r.ok && r.dev && net.devs[r.dev], ttl = (rd && isVrp(rd) ? 255 : 64) - ((r.hops || []).length);
    for (var i = 1; i <= cnt; i++) { var ok = r.ok && !(net.lossHit && net.lossHit(r, i - 1));
      if (ok) { got++; o.push('    Reply from ' + dst + ': bytes=56 Sequence=' + i + ' ttl=' + ttl + ' time=' + ms(dst.length, i) + ' ms'); } else o.push('    Request time out'); }
    o.push('', '  --- ' + dst + ' ping statistics ---', '    ' + cnt + ' packet(s) transmitted', '    ' + got + ' packet(s) received', '    ' + ((cnt - got) * 100 / cnt).toFixed(2) + '% packet loss');
    if (got) o.push('    round-trip min/avg/max = 1/' + ms(dst.length, 2) + '/' + ms(dst.length, 4) + ' ms');
    return o.join('\n');
  }
  cmd('*', 'ping <ip>', function (st, a) { return ping(st, a[0]); }, 'Ping function').cfg = false;
  cmd('*', 'ping -c <n> <ip>', function (st, a) { return ping(st, a[1], Math.min(a[0], 20)); }).cfg = false;
  cmd('*', 'ping -a <ip> <ip>', function (st, a) { return ping(st, a[1]); }).cfg = false;
  cmd('*', 'tracert <ip>', function (st, a) {
    var net = st.net; if (!net) return ''; var r = net.ping(st.dev, a[0]), ar = V(st).kind === 'ar', o = [];
    o.push(ar ? ' traceroute to  ' + a[0] + '(' + a[0] + '), max hops: 30 ,packet length: 40,press CTRL_C to break' : 'traceroute to ' + a[0] + ' (' + a[0] + '), max hops: 30, packet length: 40, press CTRL_C to break');
    var hops = (r.hops || []).map(function (h) { return h.ip; }); if (r.ok) hops.push(a[0]);
    hops.forEach(function (ip, i) { o.push((ar ? '\n ' : '') + (i + 1) + ' ' + ip + ' ' + ms(i, 1) + ' ms  ' + ms(i, 2) + ' ms  ' + ms(i, 3) + ' ms'); });
    if (!r.ok) for (var k = hops.length + 1; k <= 30; k++) o.push((ar ? ' ' : '') + k + ' * * *');
    return o.join('\n');
  }, 'Trace route function').cfg = false;

  // ---------------------------------------------------------------- display: интерфейсы и маршруты (общие для S и AR)
  function pad(s, n) { s = String(s); return s.length >= n ? s + ' ' : (s + new Array(n + 1).join(' ')).slice(0, n); }
  function phyUp(st, port) { var net = st.net; return !!net && net.linkUp(st.dev, port) && (!net.phys || net.phys(st.dev, port).up); }
  cmd('*', 'display interface brief', function (st) {
    var net = st.net, d = net && net.devs[st.dev], c = V(st).c, o = ['PHY: Physical', '*down: administratively down', '(l): loopback', '(s): spoofing', '(b): BFD down',
      'InUti/OutUti: input utility/output utility', 'Interface                   PHY   Protocol InUti OutUti   inErrors  outErrors'];
    if (!d) return o.join('\n');
    Object.keys(c.ifs).filter(function (k) { return /^(Eth-Trunk|Vlanif|LoopBack)/.test(k); }).concat(EL.vrp.dports(net, d)).forEach(function (k) {
      var x = c.ifs[k] || {}, up = /^LoopBack/.test(k) ? true : /^Vlanif/.test(k) ? !!net.ifaces(st.dev).filter(function (f) { return f.name === 'vlan' + k.slice(6); }).length :
        /^Eth-Trunk/.test(k) ? (net.lports(st.dev).filter(function (L) { return L.name === 'po' + k.slice(9); })[0] || { members: [] }).members.length > 0 : phyUp(st, k);
      var phy = x.shut ? '*down' : up ? 'up' : 'down', pr = x.shut || !up ? 'down' : /^LoopBack/.test(k) ? 'up(s)' : 'up';
      o.push(pad(full(k), 28) + pad(phy, 6) + pad(pr, 9) + pad('0%', 6) + pad('0%', 9) + pad('0', 10) + '0'); });
    return o.join('\n');
  });
  cmd('*', 'display ip interface brief', function (st) {
    var net = st.net, c = V(st).c, o = ['*down: administratively down', '^down: standby', '(l): loopback', '(s): spoofing', '(E): E-Trunk down',
      'Interface                         IP Address/Mask      Physical   Protocol'];
    Object.keys(c.ifs).sort().forEach(function (k) { var x = c.ifs[k]; if (!x.ip) return;
      var up = net && net.ifaces(st.dev).some(function (f) { return f.ip === x.ip[0]; }), phy = x.shut ? '*down' : up ? 'up' : 'down';
      o.push(pad(full(k), 34) + pad(x.ip[0] + '/' + x.ip[1], 21) + pad(phy, 11) + (up ? (/^LoopBack/.test(k) ? 'up(s)' : 'up') : 'down')); });
    return o.join('\n');
  });
  // имена интерфейсов модели → VRP: vlan10 → Vlanif10, lo0 → LoopBack0, GE0/0/1.10 → GigabitEthernet0/0/1.10
  function ifn(n) { return n ? full(String(n).split(':')[0]) : 'NULL0'; }
  var PROTO = { C: 'Direct', S: 'Static', R: 'RIP', O: 'OSPF', B: 'EBGP' };
  function hwPref(r) { return r.p === 'S' ? (r.pref || 60) : r.p === 'O' ? (r.ase ? 150 : 10) : r.p === 'R' ? 100 : r.p === 'C' ? 0 : r.ad; }
  cmd('*', 'display ip routing-table', function (st) {
    var net = st.net; if (!net) return '';
    var all = net.routes(st.dev), by = net.best(st.dev, all), rows = [];
    all.forEach(function (r) { if (r.dead || by[r.net] !== r && !(by[r.net] && by[r.net].p === r.p && by[r.net].ad === r.ad && by[r.net].m === r.m && r.p !== 'C')) return;
      if (r.p === 'C') { var me = net.ifaces(st.dev).filter(function (f) { return f.name === r.ifn; })[0];
        rows.push([r.net, 'Direct', 0, 0, me ? me.ip : '0.0.0.0', EL.vrp.ifn(r.ifn, st)]); if (me) rows.push([me.ip + '/32', 'Direct', 0, 0, '127.0.0.1', EL.vrp.ifn(r.ifn, st)]); return; }
      rows.push([r.net, PROTO[r.p] || r.p, hwPref(r), r.m || 0, r.nh || '0.0.0.0', EL.vrp.ifn(r.ifn, st)]); });
    rows.push(['127.0.0.0/8', 'Direct', 0, 0, '127.0.0.1', 'InLoopBack0'], ['127.0.0.1/32', 'Direct', 0, 0, '127.0.0.1', 'InLoopBack0']);
    rows.sort(function (a, b) { var x = IP.ip2n(a[0].split('/')[0]) - IP.ip2n(b[0].split('/')[0]); return x || +a[0].split('/')[1] - +b[0].split('/')[1]; });
    var dests = rows.map(function (x) { return x[0]; }).filter(function (x, i, s) { return s.indexOf(x) === i; }).length, o = ['Route Flags: R - relay, D - download to fib',
      '------------------------------------------------------------------------------', 'Routing Tables: Public', '         Destinations : ' + dests + '        Routes : ' + rows.length, '',
      'Destination/Mask    Proto   Pre  Cost      Flags NextHop         Interface', ''], prev = null;
    rows.forEach(function (x) { var dst = x[0] === prev ? '' : x[0]; prev = x[0];
      o.push(('                 ' + dst).slice(-17) + '   ' + pad(x[1], 8) + pad(x[2], 5) + pad(x[3], 12) + (x[1] === 'RIP' || x[1] === 'OSPF' && x[4] !== '0.0.0.0' ? 'D' : 'D') + '   ' + pad(x[4], 16) + x[5]); });
    return o.join('\n');
  });

  // ---------------------------------------------------------------- устройство в модели сети
  function fresh(kind) { return { ifs: {} }; }
  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {};
    if (m.vendor !== 'huawei') return d;
    var st = d.st, kind = m.kind === 'hw-ar' ? 'ar' : 's';
    d.sub = 'vrp'; st.mode = 'vrp';
    var n = +String(d.id).slice(1) || 1;
    if (kind === 's') st.bmac = '4c:1f:cc:' + ('0' + ((n * 37) & 255).toString(16)).slice(-2) + ':' + ('0' + ((n * 101) & 255).toString(16)).slice(-2) + ':' + ('0' + (n & 255).toString(16)).slice(-2);
    st.vrp = { kind: kind, stack: [], c: fresh(kind), saved: null, ask: null };
    compile(st);
    return d;
  };
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id]; if (!isVrp(d)) return ex0.apply(this, arguments); this.gen++; return d.off ? '' : exec(d.st, line); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; return isVrp(d) ? prompt(d.st) : pr0.apply(this, arguments); };
  var he0 = P.help;
  P.help = function (id, line) { var d = this.devs[id]; return isVrp(d) ? help(d.st, line) : he0.apply(this, arguments); };
  var tb0 = P.tab;
  P.tab = function (id, line) { var d = this.devs[id]; return isVrp(d) ? tab(d.st, line) : tb0.apply(this, arguments); };
  // время жизни ARP у Huawei — 1200 с (S-CR j01d, AR-CR arp_expire-time; spec/defaults-vs-eltex.md §10); MAC — 300 с, как в модели
  var aa0 = P.arpAge;
  P.arpAge = function (id) { return isVrp(this.devs[id]) ? 1200 : aa0.apply(this, arguments); };
  var sh0 = P.setHost;                           // «Свойства» → имя: у VRP это sysname
  P.setHost = function (id, name) { var d = this.devs[id]; if (!isVrp(d)) return sh0.apply(this, arguments); d.st.vrp.c.sysname = name; compile(d.st); };
  var rb0 = P.reboot;
  P.reboot = function (id) { var d = this.devs[id]; if (!isVrp(d)) return rb0.apply(this, arguments);
    var x = d.st.vrp; x.c = x.saved ? EL.clone(x.saved) : fresh(x.kind); x.stack = []; x.ask = null; compile(d.st);
    this.mac[id] = {}; this.arp[id] = {}; d.off = false; this.gen++; };
  // конфигурация текстом (frames.js): вывод display current-configuration и вставка его же — по отступам видов (1 пробел — вид блока, 2 — вложенный)
  if (EL.cfgText) { var ct0 = EL.cfgText; EL.cfgText = function (d) { return isVrp(d) ? cfgText(d.st) : ct0.apply(this, arguments); }; }
  if (EL.applyConfig) { var ap0 = EL.applyConfig; EL.applyConfig = function (n, id, text) { var d = n.devs[id]; if (!isVrp(d)) return ap0.apply(this, arguments);
    var errs = [], x = d.st.vrp; x.ask = null; x.stack = []; n.exec(id, 'system-view');
    String(text).split('\n').forEach(function (l) { if (!l.trim() || /^\s*(#|return\s*$)/.test(l)) return; var dep = l.match(/^ */)[0].length;
      while (x.stack.length > dep + 1) x.stack.pop();
      var r = n.exec(id, l.trim()); if (/Error/.test(r)) errs.push(d.name + ' «' + l.trim() + '» → ' + r.split('\n').pop()); });
    x.stack = []; return errs; }; }

  EL.vrp = { dports: dports, cmd: cmd, T: T, exec: exec, prompt: prompt, norm: norm, full: full, short: short, isVrp: isVrp, vlTxt: vlTxt, ifc: ifc, cur: cur, top: top, push: push,
    pad: pad, phyUp: phyUp, cfgText: cfgText, ifn: ifn, compile: compile, compileS: function () {}, compileAr: function () {}, renderS: function () { return []; }, renderAr: function () { return []; } };
})(typeof window !== 'undefined' ? window : global);
