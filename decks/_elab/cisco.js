/* Cisco IOS в эмуляторе (спецификации sources/cisco/spec: switch-ios, router-ios; набор устройств — как в Packet Tracer 9.0).
   Как Huawei: коммутатор Catalyst — тип 'mes' (поля ports/vlans/svi/stp/mst/pos модели MES), маршрутизатор ISR — тип 'esr' (st.run).
   Здесь — общее IOS: режимы и приглашения (Switch> / # / (config)# / (config-if)# …), сокращения слов, «?» и Tab, no-формы,
   exit / end / Ctrl+Z / do, переход в глобальную конфигурацию из подрежимов, сообщения парсера по CG-2960X Table 2:
   «% Invalid input detected at '^' marker.» (маркер под ошибкой), «% Ambiguous command: "…"», «% Incomplete command.»;
   неизвестное слово в EXEC — попытка Telnet по имени: «Translating "…"...domain server (255.255.255.255)» (Doc 46253),
   отключается no ip domain-lookup. Настройки — в st.ios.c, после каждой команды compile переносит их в модель сети.
   Сохранение: copy running-config startup-config / write memory; reload поднимает startup-config.
   Не из собранных документов (общеизвестный вывод IOS, в отчёте): ответ copy/write («Destination filename», «[OK]»), вопрос reload. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip;
  var GROUP = 'Cisco (как в Packet Tracer)';
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  // набор Packet Tracer 9.0 (catalog/packet-tracer.md): порты — по справке PT и документации Cisco
  [['2960-24TT', { type: 'mes', kind: 'cs-sw', portList: range('fa0/', 1, 24).concat(range('gi0/', 1, 2)), ios: '12.2', costs: 'short', note: 'Коммутатор Cisco Catalyst 2960-24TT: 24 × FastEthernet0/1–24 + 2 × GigabitEthernet0/1–2 (как в Packet Tracer)' }],
   ['2950-24', { type: 'mes', kind: 'cs-sw', portList: range('fa0/', 1, 24), ios: '12.1', costs: 'short', note: 'Коммутатор Cisco Catalyst 2950-24: 24 × FastEthernet0/1–24 (как в Packet Tracer)' }],
   ['3560-24PS', { type: 'mes', kind: 'cs-sw', l3: true, portList: range('fa0/', 1, 24).concat(range('gi0/', 1, 2)), ios: '12.2', costs: 'short', note: 'Коммутатор L3 Cisco Catalyst 3560-24PS: 24 × FastEthernet0/1–24 + 2 × GigabitEthernet0/1–2, ip routing (как в Packet Tracer)' }],
   ['1941', { type: 'esr', kind: 'cs-rt', portList: range('gi0/', 0, 1), ios: '15.1', note: 'Маршрутизатор Cisco 1941 ISR: GigabitEthernet0/0–0/1 (как в Packet Tracer)' }],
   ['2901', { type: 'esr', kind: 'cs-rt', portList: range('gi0/', 0, 1), ios: '15.1', note: 'Маршрутизатор Cisco 2901 ISR: GigabitEthernet0/0–0/1 (как в Packet Tracer)' }],
   ['2911', { type: 'esr', kind: 'cs-rt', portList: range('gi0/', 0, 2), ios: '15.1', note: 'Маршрутизатор Cisco 2911 ISR: GigabitEthernet0/0–0/2 (как в Packet Tracer)' }],
   ['ISR4321', { type: 'esr', kind: 'cs-rt', portList: range('gi0/0/', 0, 1), ios: '15.4', note: 'Маршрутизатор Cisco ISR4321: GigabitEthernet0/0/0–0/0/1 (как в Packet Tracer)' }]
  ].forEach(function (x) { var m = x[1]; m.ports = m.portList.length; m.group = GROUP; m.vendor = 'cisco'; m.host = m.type === 'mes' ? 'Switch' : 'Router';
    m.login = [{ u: '—', p: '—', a: 'консоль без пароля; enable secret не задан' }]; EL.MODELS[x[0]] = m; });

  function isIos(d) { return !!d && d.sub === 'ios'; }
  function dports(net, d) { return net.portsOf(d).filter(function (p) { return /^(fa|gi|eth)\d/.test(p); }); }
  // ---------------------------------------------------------------- имена интерфейсов
  var TY = { fa: ['FastEthernet', 'Fa'], gi: ['GigabitEthernet', 'Gi'], vlan: ['Vlan', 'Vl'], po: ['Port-channel', 'Po'], lo: ['Loopback', 'Lo'], eth: ['eth', 'eth'] };   // eth — D-Link (eth1/0/1)
  function full(n) { var m = String(n).match(/^(fa|gi|vlan|po|lo|eth)(\d.*)$/); return m ? TY[m[1]][0] + m[2] : n; }
  function short(n) { var m = String(n).match(/^(fa|gi|vlan|po|lo|eth)(\d.*)$/); return m ? TY[m[1]][1] + m[2] : n; }
  function pre(w, kw, min) { return w.length >= (min || 1) && kw.indexOf(w) === 0; }
  function ifType(w) { w = w.toLowerCase(); if (pre(w, 'ethernet', 2) || w === 'eth') return 'eth'; if (pre(w, 'fastethernet')) return 'fa'; if (pre(w, 'gigabitethernet')) return 'gi'; if (pre(w, 'port-channel', 2)) return 'po';
    if (pre(w, 'loopback', 2)) return 'lo'; if (pre(w, 'vlan', 1) && w.length >= 1 && w !== 'v') return 'vlan'; return null; }
  // строка → токены; «FastEthernet 0/1», «fa0/1», «f0/1» → fa0/1; «interface vlan 10» → vlan10; диапазон «fa0/1 - 5» → fa0/1-5
  function norm(line) {
    var t = String(line).trim().replace(/\s*-\s*(?=\d)/g, ' - ').split(/\s+/).filter(Boolean), o = [];
    for (var i = 0; i < t.length; i++) {
      var w = t[i], m = w.match(/^([A-Za-z-]+)(\d+(?:\/\d+){0,2}(?:\.\d+)?)$/), nx = t[i + 1], ty;
      var ifCtx = o.length && /^(interface|int|in|range|channel-group|passive-interface|ip|show|sh|source|neighbor|eth|switchport)/i.test(o[o.length - 1]);
      if (m && (ty = ifType(m[1])) && (ty !== 'vlan' || ifCtx)) { o.push(ty + m[2]); continue; }
      if (/^[A-Za-z-]+$/.test(w) && nx && /^\d+(\/\d+){0,2}(\.\d+)?$/.test(nx) && (ty = ifType(w)) && (/\//.test(nx) || ifCtx && ty !== 'fa' && ty !== 'gi')) {
        if (ty !== 'vlan' || /^(interface|int|in)$/i.test(o[o.length - 1] || '') || pre((o[o.length - 1] || '').toLowerCase(), 'interface', 2)) { o.push(ty + nx); i++; continue; } }
      if (w === '-' && o.length && /^(fa|gi|eth)\d/.test(o[o.length - 1]) && /^\d+$/.test(nx || '')) { o[o.length - 1] += '-' + nx; i++; continue; }
      o.push(w);
    }
    return o;
  }

  // ---------------------------------------------------------------- таблица команд
  var T = [];
  function cmd(views, pat, run, d) { var e = { v: views.split(' '), p: pat.split(' '), run: run, d: d || '' }; T.push(e); return e; }
  function isIf(t) { return /^(fa|gi|eth)\d+(\/\d+){1,2}(\.\d+)?$|^(vlan|po|lo)\d+$/.test(t); }
  function tokOk(p, t) {
    if (p === '<n>') return /^\d+$/.test(t); if (p === '<w>') return true; if (p === '<ip>') return IP.ip2n(t) !== null;
    if (p === '<if>') return isIf(t); if (p === '<rng>') return /^(fa|gi|eth)\d+(\/\d+){1,2}(-\d+)?$/.test(t); if (p === '<list>') return /^[\d,\-]+$/.test(t);
    return pre(t.toLowerCase(), p);
  }
  function list(s) { var o = []; String(s).split(',').forEach(function (p) { var m = p.match(/^(\d+)-(\d+)$/); if (m) { for (var i = +m[1]; i <= +m[2]; i++) o.push(i); } else if (/^\d+$/.test(p)) o.push(+p); }); return o; }
  function match(p, toks) {
    var a = [], ex = 0;
    for (var k = 0; k < p.length; k++) {
      if (p[k] === '<rest>') { if (k >= toks.length) return null; a.push(toks.slice(k).join(' ')); return { a: a, ex: ex }; }
      var t = toks[k]; if (t === undefined || !tokOk(p[k], t)) return null;
      if (p[k].charAt(0) === '<') a.push(p[k] === '<n>' ? +t : p[k] === '<list>' ? list(t) : t); else if (t.toLowerCase() === p[k]) ex++;
    }
    return toks.length === p.length ? { a: a, ex: ex } : null;
  }
  function inView(e, v) { return e.v.indexOf(v) >= 0 || e.v.indexOf('*') >= 0 || (e.v.indexOf('exec') >= 0 && (v === 'user' || v === 'priv')); }
  function hits(st, v, toks) { var o = []; T.forEach(function (e) { if (!inView(e, v) || (e.ok && !e.ok(st))) return; var r = match(e.p, toks); if (r) o.push({ e: e, r: r }); }); return o; }
  // неоднозначность: на одной позиции подходят разные ключевые слова, и введённое слово не совпадает ни с одним целиком
  function ambiguous(H, toks) {
    for (var k = 0; k < toks.length; k++) { var kw = []; H.forEach(function (h) { var p = h.e.p[k]; if (p && p.charAt(0) !== '<' && kw.indexOf(p) < 0) kw.push(p); });
      if (kw.length > 1) { if (kw.indexOf(toks[k].toLowerCase()) >= 0) { var x = toks[k].toLowerCase(); H = H.filter(function (h) { return h.e.p[k] === x || h.e.p[k].charAt(0) === '<'; }); continue; } return true; } }
    return false;
  }
  // сокращение подходит к нескольким ключевым словам на своей позиции («no s» → shutdown / switchport …)
  function ambPart(st, v, toks) {
    for (var k = 0; k < toks.length; k++) { var kw = [];
      T.forEach(function (e) { if (!inView(e, v) || (e.ok && !e.ok(st)) || k >= e.p.length) return;
        for (var i = 0; i < k; i++) { if (e.p[i] === '<rest>' || !tokOk(e.p[i], toks[i])) return; }
        var p = e.p[k]; if (p.charAt(0) !== '<' && pre(toks[k].toLowerCase(), p) && kw.indexOf(p) < 0) kw.push(p); });
      if (kw.length > 1 && kw.indexOf(toks[k].toLowerCase()) < 0) return true; }
    return false;
  }
  function partial(st, v, toks) { return T.some(function (e) { if (!inView(e, v) || toks.length >= e.p.length || (e.ok && !e.ok(st))) return false;
    for (var k = 0; k < toks.length; k++) { if (e.p[k] === '<rest>') return false; if (!tokOk(e.p[k], toks[k])) return false; } return true; }); }
  function errAt(st, v, toks) {
    var k = 0;
    T.forEach(function (e) { if (!inView(e, v) || (e.ok && !e.ok(st))) return; var i = 0; while (i < toks.length && i < e.p.length && e.p[i] !== '<rest>' && tokOk(e.p[i], toks[i])) i++;
      if (e.p[i] === '<rest>') i = toks.length; if (i > k) k = i; });
    return k;
  }
  function caret(st, raw, k) {                       // маркер под первым символом ошибочного слова (строка ввода — после приглашения)
    var s = String(raw), at = 0, pos = 0, words = s.match(/\S+/g) || [];
    for (var i = 0; i <= k && i < words.length; i++) { var j = s.indexOf(words[i], at); pos = j; at = j + words[i].length; }
    if (k >= words.length) pos = s.replace(/\s+$/, '').length + 1;
    return new Array(prompt(st).length + pos + 1).join(' ') + '^\n' + (X(st).dl ? 'Invalid input detected at ^marker' : '% Invalid input detected at \'^\' marker.');   // D-Link — без «%» (dlink-ios.md §4)
  }

  // ---------------------------------------------------------------- режимы и приглашения
  function X(st) { return st.ios; }
  function top(st) { var s = X(st).stack; return s[s.length - 1] || { v: 'user' }; }
  function host(st) { return X(st).c.hostname || { sw: 'Switch', rt: 'Router', asa: 'ciscoasa' }[X(st).kind]; }
  var PR = { user: '>', priv: '#', config: '(config)#', 'if': '(config-if)#', range: '(config-if-range)#', subif: '(config-subif)#', vlan: '(config-vlan)#', line: '(config-line)#',
    router: '(config-router)#', std: '(config-std-nacl)#', ext: '(config-ext-nacl)#', dhcp: '(dhcp-config)#', obj: '(config-network-object)#', pmap: '(config-pmap)#', pmapc: '(config-pmap-c)#' };
  function prompt(st) { var x = X(st); if (x.ask) return x.ask.pr || ''; return host(st) + PR[top(st).v]; }
  function push(st, f) { X(st).stack.push(f); }
  function toConfig(st) { var s = X(st).stack; while (s.length && s[s.length - 1].v !== 'config') s.pop(); }

  // ---------------------------------------------------------------- исполнение строки
  function exec(st, raw) {
    var x = X(st);
    if (x.ask) { var a = x.ask; x.ask = null; return a.fn(String(raw).trim()); }
    var line = String(raw).replace(/\s+$/, '');
    if (!line.trim()) return '';
    if (/\?$/.test(line)) return help(st, line.slice(0, -1));
    var toks = norm(line), v = top(st).v;
    if (/^do$/i.test(toks[0]) && v !== 'user' && v !== 'priv' && toks.length > 1) {   // do — команда привилегированного режима из конфигурации
      var s0 = x.stack; x.stack = [{ v: 'priv' }]; try { return run(st, line.replace(/^\s*do\s+/i, ''), norm(line.replace(/^\s*do\s+/i, '')), 'priv'); } finally { if (x.stack.length === 1 && x.stack[0].v === 'priv') x.stack = s0; } }
    var pipe = line.match(/^(.*?\S)\s+\|\s+(\S+)\s+(.+)$/);   // фильтры show: | include | exclude | begin | section (CG-2960X)
    if (pipe && /^(sh|sho|show)\b/i.test(pipe[1].trim()) && /^(i|in|inc|incl|inclu|includ|include|e|ex|exc|excl|exclu|exclud|exclude|b|be|beg|begi|begin|s|se|sec|sect|secti|sectio|section)$/i.test(pipe[2])) {
      var out = run(st, pipe[1], norm(pipe[1]), v), re; try { re = new RegExp(pipe[3]); } catch (e) { re = new RegExp(pipe[3].replace(/[.*+?^${}()|[\]\\]/g, '\\$&')); }
      var L = String(out).split('\n'), k = pipe[2].charAt(0).toLowerCase();
      if (k === 'i') L = L.filter(function (l) { return re.test(l); }); if (k === 'e') L = L.filter(function (l) { return !re.test(l); });
      if (k === 'b') { var at = -1; L.some(function (l, i) { if (re.test(l)) { at = i; return true; } return false; }); L = at < 0 ? [] : L.slice(at); }
      if (k === 's') { var o = [], inS = false; L.forEach(function (l) { if (/^\S/.test(l)) inS = re.test(l); if (inS) o.push(l); }); L = o; }
      return L.join('\n');
    }
    return run(st, line, toks, v);
  }
  function run(st, line, toks, v) {
    var x = X(st), H = hits(st, v, toks);
    if (!H.length && ['if', 'range', 'subif', 'vlan', 'line', 'router', 'std', 'ext', 'dhcp', 'obj', 'pmap', 'pmapc'].indexOf(v) >= 0) {   // команда глобальной конфигурации из подрежима
      var H2 = hits(st, 'config', toks); if (H2.length) { toConfig(st); v = 'config'; H = H2; } }
    var dl = !!x.dl;
    if (H.length > 1 && ambiguous(H, toks) || !H.length && ambPart(st, v, toks)) return dl ? 'Ambiguous command' : '% Ambiguous command:  "' + line.trim() + '"';
    if (!H.length) {
      if (partial(st, v, toks)) return dl ? 'Incomplete command' : '% Incomplete command.';
      if (!dl && (v === 'user' || v === 'priv') && toks.length === 1 && !T.some(function (e) { return inView(e, v) && tokOk(e.p[0], toks[0]); })) return translating(st, toks[0]);
      return caret(st, line, errAt(st, v, toks));
    }
    H.sort(function (a, b) { return b.r.ex - a.r.ex; });
    var r = H[0].e.run(st, H[0].r.a, toks);
    if (r === null) return caret(st, line, toks.length - 1);
    if (H[0].e.cfg !== false && v !== 'user' && v !== 'priv') compile(st);
    return r === undefined ? '' : r;
  }
  function translating(st, w) {                    // Doc 46253: неизвестное слово — имя хоста для Telnet
    var t = 'Translating "' + w + '"...domain server (255.255.255.255)\n';
    return (X(st).c.noLookup ? '' : t + '(255.255.255.255)\n' + t) + '% Unknown command or computer name, or unable to find computer address';
  }
  function compile(st) { ({ rt: EL.ios.compileRt, sw: EL.ios.compileSw, asa: EL.ios.compileAsa })[X(st).kind](st); if (st.net) st.net.gen++; }
  var PH = { '<n>': '<0-4294967295>', '<w>': 'WORD', '<ip>': 'A.B.C.D', '<if>': 'Interface', '<rng>': 'Interface range', '<list>': 'WORD', '<rest>': 'LINE' };
  function cands(st, txt) {
    var ends = /\s$/.test(txt) || !txt.trim(), toks = txt.trim() ? norm(txt) : [], part = ends ? null : toks.pop(), v = top(st).v, out = [], seen = {}, cr = false;
    T.forEach(function (e) { if (!inView(e, v) || (e.ok && !e.ok(st))) return;
      for (var k = 0; k < toks.length; k++) { if (e.p[k] === '<rest>') return; if (k >= e.p.length || !tokOk(e.p[k], toks[k])) return; }
      if (toks.length === e.p.length && ends) { cr = true; return; }
      var p = e.p[toks.length]; if (!p) return;
      if (p.charAt(0) === '<') { if (part === null && !seen[p]) { seen[p] = 1; out.push([PH[p] || p, '']); } return; }
      if (part !== null && !pre(part.toLowerCase(), p)) return;
      if (!seen[p]) { seen[p] = 1; out.push([p, toks.length === 0 ? e.d : '']); } });
    if (cr) out.push(['<cr>', '']);
    return { list: out, part: part };
  }
  function help(st, txt) {
    var c = cands(st, txt);
    if (!c.list.length) return '% Unrecognized command';
    if (c.part !== null) return c.list.map(function (x) { return x[0]; }).join('  ');      // «di?» — слова на эти буквы в строку (CG-2960X)
    return c.list.map(function (x) { return '  ' + (x[0] + '                  ').slice(0, Math.max(18, x[0].length + 2)) + x[1]; }).join('\n');
  }
  function tab(st, txt) { var c = cands(st, txt), kw = c.list.filter(function (x) { return x[0].charAt(0) !== '<' && !/^[A-Z]/.test(x[0]); });
    if (c.part === null || kw.length !== 1) return null; return txt.replace(/\S+$/, kw[0][0]) + ' '; }

  // ---------------------------------------------------------------- общие команды
  function C(st) { return X(st).c; }
  function ifc(st, n) { var c = C(st); return c.ifs[n] || (c.ifs[n] = {}); }
  function cur(st) { var t = top(st); return (t.names || (t.name ? [t.name] : [])).map(function (n) { return ifc(st, n); }); }
  function curNames(st) { var t = top(st); return t.names || (t.name ? [t.name] : []); }
  cmd('user', 'enable', function (st) { var c = C(st), p = c.secret || c.enpw;
    if (!p && X(st).kind === 'asa') { X(st).ask = { pr: 'Password: ', fn: function (s) { if (!s) { push(st, { v: 'priv' }); return ''; } return 'Invalid password'; } }; return ''; }   // ASA 9.x: пароль enable пустой — Enter (GS92)
    if (!p) { push(st, { v: 'priv' }); return; }
    X(st).ask = { pr: 'Password: ', fn: function (s) { if (s === p) { push(st, { v: 'priv' }); return ''; } return '% Bad secrets'; } }; return ''; }, 'Turn on privileged commands').cfg = false;
  cmd('priv', 'disable', function (st) { X(st).stack = []; }, 'Turn off privileged commands').cfg = false;
  cmd('exec', 'exit', function (st) { X(st).stack = []; return ''; }, 'Exit from the EXEC').cfg = false;
  cmd('exec', 'logout', function (st) { X(st).stack = []; return ''; }, 'Exit from the EXEC').cfg = false;
  cmd('priv', 'configure terminal', function (st) { push(st, { v: 'config' }); return 'Enter configuration commands, one per line.  End with CNTL/Z.'; }, 'Enter configuration mode').cfg = false;
  cmd('priv', 'configure', function (st) { push(st, { v: 'config' }); return 'Enter configuration commands, one per line.  End with CNTL/Z.'; }).cfg = false;
  cmd('config if range subif vlan line router std ext dhcp', 'exit', function (st) { X(st).stack.pop(); });
  cmd('config if range subif vlan line router std ext dhcp', 'end', function (st) { X(st).stack = [{ v: 'priv' }]; });
  cmd('config', 'hostname <w>', function (st, a) { C(st).hostname = a[0]; }, 'Set system\'s network name');
  cmd('config', 'no hostname', function (st) { delete C(st).hostname; });
  cmd('config', 'enable secret <w>', function (st, a) { C(st).secret = a[0]; }, 'Modify enable password parameters');
  cmd('config', 'enable password <w>', function (st, a) { C(st).enpw = a[0]; });
  cmd('config', 'no enable secret', function (st) { delete C(st).secret; });
  cmd('config', 'no enable password', function (st) { delete C(st).enpw; });
  cmd('config', 'service password-encryption', function (st) { C(st).pwEnc = true; });
  cmd('config', 'no service password-encryption', function (st) { delete C(st).pwEnc; });
  cmd('config', 'no ip domain-lookup', function (st) { C(st).noLookup = true; }, 'Global IP configuration subcommands');
  cmd('config', 'no ip domain lookup', function (st) { C(st).noLookup = true; });
  cmd('config', 'ip domain-lookup', function (st) { delete C(st).noLookup; });
  cmd('config', 'ip domain-name <w>', function (st, a) { C(st).domain = a[0]; });
  cmd('config', 'banner motd <rest>', function (st, a) { var m = a[0].match(/^(\S)([\s\S]*)\1/); if (!m) return null; C(st).motd = m[2]; });
  cmd('config', 'username <w> privilege <n> secret <w>', function (st, a) { (C(st).users = C(st).users || {})[a[0]] = { lvl: a[1], secret: a[2] }; });
  cmd('config', 'username <w> secret <w>', function (st, a) { (C(st).users = C(st).users || {})[a[0]] = { secret: a[1] }; });
  cmd('config', 'username <w> password <w>', function (st, a) { (C(st).users = C(st).users || {})[a[0]] = { pw: a[1] }; });
  function lineKey(a) { return a.join(' '); }
  cmd('config', 'line console 0', function (st) { push(st, { v: 'line', key: 'con 0' }); }, 'Configure a terminal line');
  cmd('config', 'line vty <n> <n>', function (st, a) { push(st, { v: 'line', key: 'vty ' + lineKey(a) }); });
  function ln(st) { var c = C(st), k = top(st).key; c.lines = c.lines || {}; return c.lines[k] || (c.lines[k] = {}); }
  cmd('line', 'password <w>', function (st, a) { ln(st).pw = a[0]; });
  cmd('line', 'login', function (st) { ln(st).login = 'login'; });
  cmd('line', 'login local', function (st) { ln(st).login = 'login local'; });
  cmd('line', 'no login', function (st) { delete ln(st).login; });
  cmd('line', 'transport input <rest>', function (st, a) { ln(st).tin = a[0]; });
  cmd('line', 'exec-timeout <n> <n>', function (st, a) { ln(st).eto = a[0] + ' ' + a[1]; });
  cmd('line', 'exec-timeout <n>', function (st, a) { ln(st).eto = a[0] + ''; });
  cmd('line', 'logging synchronous', function (st) { ln(st).sync = true; });
  cmd('config', 'cdp run', function (st) { delete C(st).noCdp; }, 'Enable CDP');
  cmd('config', 'no cdp run', function (st) { C(st).noCdp = true; });
  cmd('config', 'lldp run', function (st) { C(st).lldp = true; });
  cmd('config', 'no lldp run', function (st) { delete C(st).lldp; });
  // интерфейс: общие команды
  cmd('if range subif', 'description <rest>', function (st, a) { cur(st).forEach(function (x) { x.desc = a[0]; }); }, 'Interface specific description');
  cmd('if range subif', 'no description', function (st) { cur(st).forEach(function (x) { delete x.desc; }); });
  cmd('if range subif', 'shutdown', function (st) { cur(st).forEach(function (x) { x.shut = true; delete x.noShut; }); }, 'Shutdown the selected interface');
  cmd('if range subif', 'no shutdown', function (st) { cur(st).forEach(function (x) { delete x.shut; x.noShut = true; }); });
  cmd('if range', 'speed <w>', function (st, a) { cur(st).forEach(function (x) { x.speed = a[0]; }); });
  cmd('if range', 'duplex <w>', function (st, a) { cur(st).forEach(function (x) { x.duplex = a[0]; }); });
  cmd('if subif', 'ip address <ip> <ip>', function (st, a) { var l = IP.mask2len(a[1]); if (l === null || l < 1) return null; var n = curNames(st)[0];
    if (/^(fa|gi|eth)\d/.test(n) && X(st).kind === 'sw' && !cur(st)[0].routed) return null; cur(st)[0].ip = [a[0], l]; }, 'Set the IP address of an interface');
  cmd('if subif', 'no ip address', function (st) { delete cur(st)[0].ip; });

  // ---------------------------------------------------------------- конфигурация: show running-config, сохранение, reload
  function cfgText(st, c) {
    if (X(st).kind === 'asa') return EL.ios.cfgAsa(st, c || X(st).c);
    var x = X(st), o = [], d = st.net && st.net.devs[st.dev], m = EL.MODELS[d ? d.model : ''] || {};
    c = c || x.c;
    o.push('!', 'version ' + (m.ios || '15.0'), 'no service timestamps log datetime msec', 'no service timestamps debug datetime msec', (c.pwEnc ? '' : 'no ') + 'service password-encryption', '!',
      'hostname ' + (c.hostname || (x.kind === 'sw' ? 'Switch' : 'Router')), '!');
    if (c.secret) o.push('enable secret 5 ' + hash(c.secret)); if (c.enpw) o.push('enable password ' + (c.pwEnc ? '7 ' + hash(c.enpw).slice(0, 12) : c.enpw));
    if (c.secret || c.enpw) o.push('!');
    if (c.noLookup) o.push('no ip domain-lookup'); if (c.domain) o.push('ip domain-name ' + c.domain); if (c.noLookup || c.domain) o.push('!');
    Object.keys(c.users || {}).forEach(function (u) { var y = c.users[u]; o.push('username ' + u + (y.lvl !== undefined ? ' privilege ' + y.lvl : '') + (y.secret ? ' secret 5 ' + hash(y.secret) : ' password 0 ' + y.pw)); });
    var save = o.length; (x.kind === 'rt' ? EL.ios.renderRt : EL.ios.renderSw)(st, c, o); void save;
    if (c.motd !== undefined) o.push('banner motd ^C' + c.motd + '^C', '!');
    var L = c.lines || {};
    ['con 0', 'aux 0', 'vty 0 4'].concat(Object.keys(L).filter(function (k) { return ['con 0', 'vty 0 4'].indexOf(k) < 0; })).forEach(function (k) { if (k === 'aux 0' && x.kind === 'sw') return;
      var y = L[k] || {}; o.push('line ' + k); if (y.eto) o.push(' exec-timeout ' + y.eto); if (y.pw) o.push(' password ' + (c.pwEnc ? '7 ' + hash(y.pw).slice(0, 12) : y.pw));
      if (y.sync) o.push(' logging synchronous'); if (y.login) o.push(' ' + y.login); else if (/^vty/.test(k)) o.push(' login'); if (y.tin) o.push(' transport input ' + y.tin); });
    if (x.kind === 'sw' && !L['vty 5 15']) o.push('line vty 5 15', ' login');
    o.push('!', '!', 'end');
    var body = o.join('\n');
    return 'Building configuration...\n\nCurrent configuration : ' + body.length + ' bytes\n' + body;
  }
  function hash(s) { var h = 0, o = '$1$'; for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0; var A = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./';
    for (var k = 0; k < 26; k++) { o += A[h % 64]; h = (h * 1103515245 + 12345) >>> 0; } return o; }   // хэш для вида (не настоящий MD5)
  cmd('exec', 'show running-config', function (st) { return cfgText(st); }, 'Current operating configuration').cfg = false;
  cmd('priv', 'show startup-config', function (st) { var x = X(st); return x.saved ? cfgText(st, x.saved).replace('Current configuration', 'Using') : 'startup-config is not present'; }).cfg = false;
  function save(st) { X(st).saved = EL.clone(X(st).c); return 'Building configuration...\n[OK]'; }
  cmd('priv', 'copy running-config startup-config', function (st) { X(st).ask = { fn: function () { return save(st); } }; return 'Destination filename [startup-config]? '; }, 'Copy from one file to another').cfg = false;
  cmd('priv', 'write memory', function (st) { return save(st); }, 'Write running configuration to memory').cfg = false;
  cmd('priv', 'write', function (st) { return save(st); }).cfg = false;
  cmd('priv', 'erase startup-config', function (st) { var x = X(st); x.ask = { fn: function (s) { if (/^n/i.test(s)) return ''; x.saved = null; return '[OK]\nErase of nvram: complete'; } };
    return 'Erasing the nvram filesystem will remove all configuration files! Continue? [confirm]'; }).cfg = false;
  cmd('priv', 'write erase', function (st) { X(st).saved = null; return '[OK]\nErase of nvram: complete'; }).cfg = false;
  cmd('priv', 'reload', function (st) { var x = X(st); x.ask = { fn: function (s) { if (/^n/i.test(s)) return ''; if (st.net) st.net.reboot(st.dev); return ''; } };
    return (JSON.stringify(x.c) !== JSON.stringify(x.saved || fresh()) ? 'System configuration has been modified. Save? [yes/no]: ' : 'Proceed with reload? [confirm]'); }, 'Halt and perform a cold restart').cfg = false;
  cmd('exec', 'show version', function (st) { var d = st.net && st.net.devs[st.dev], m = EL.MODELS[d ? d.model : ''] || {};
    return 'Cisco IOS Software, ' + (d ? d.model : '') + ' Software, Version ' + (m.ios || '15.0') + '\n\n' + host(st) + ' uptime is ' + Math.floor(((st.net && st.net.now) || 0) / 60) + ' minutes\n' +
      'cisco ' + (d ? d.model : '') + ' processor\n' + dports(st.net, d).length + ' Ethernet interfaces\n\nConfiguration register is 0x2102'; }).cfg = false;
  cmd('exec', 'show history', function () { return ''; }).cfg = false;
  cmd('exec', 'terminal length <n>', function () { return ''; }).cfg = false;
  cmd('exec', 'show clock', function () { return '*' + new Date().toUTCString().slice(17, 25) + '.000 UTC ' + new Date().toUTCString().slice(0, 16); }).cfg = false;

  // ---------------------------------------------------------------- ping / traceroute (PING-TS, PING-CR)
  function ms(seed, i) { return 1 + ((seed * 7 + i * 13) % 9); }
  function ping(st, dst) {
    var net = st.net; if (!net || IP.ip2n(dst) === null) return null;
    var r = net.ping(st.dev, dst); if (net.onTrace) net.onTrace(r, st.dev, dst);
    var s = '', got = 0; for (var i = 0; i < 5; i++) { var ok = r.ok && !(net.lossHit && net.lossHit(r, i)); if (ok) got++; s += ok ? '!' : X(st).kind === 'asa' ? '?' : /unreachable/i.test(r.why || '') ? (i % 2 ? '.' : 'U') : '.'; }   // ASA без ответа — ????? (CMD)
    return (X(st).kind === 'asa' ? '' : 'Type escape sequence to abort.\n') + 'Sending 5, 100-byte ICMP Echos to ' + dst + ', timeout is 2 seconds:\n' + s + '\nSuccess rate is ' + got * 20 + ' percent (' + got + '/5)' +
      (got ? ', round-trip min/avg/max = ' + (function () { var t = [ms(dst.length, 1), ms(dst.length, 2), ms(dst.length, 3)].sort(function (a, b) { return a - b; });
        return t[0] + '/' + t[1] + '/' + t[2]; })() + ' ms' : '');
  }
  cmd('exec', 'ping <ip>', function (st, a) { return ping(st, a[0]); }, 'Send echo messages').cfg = false;
  cmd('exec', 'traceroute <ip>', function (st, a) { var net = st.net; if (!net) return ''; var r = net.ping(st.dev, a[0]), o = ['Type escape sequence to abort.', 'Tracing the route to ' + a[0], ''];
    var hops = (r.hops || []).map(function (h) { return h.ip; }); if (r.ok) hops.push(a[0]);
    hops.forEach(function (ip, i) { o.push('  ' + (i + 1) + '   ' + ip + '       ' + ms(i, 1) + ' msec    ' + ms(i, 2) + ' msec    ' + ms(i, 3) + ' msec'); });
    if (!r.ok) for (var k = hops.length + 1; k <= 30; k++) o.push('  ' + k + '   *    *    *'); return o.join('\n'); }, 'Trace route to destination').cfg = false;

  // ---------------------------------------------------------------- show ip interface brief / show ip route (общие)
  function pad(s, n) { s = String(s); return s.length >= n ? s + ' ' : (s + new Array(n + 1).join(' ')).slice(0, n); }
  function phyUp(st, p) { var net = st.net; return !!net && net.linkUp(st.dev, p) && (!net.phys || net.phys(st.dev, p).up); }
  cmd('exec', 'show ip interface brief', function (st) {
    var net = st.net, d = net && net.devs[st.dev], c = C(st), o = ['Interface              IP-Address      OK? Method Status                Protocol'];
    if (!d) return o.join('\n');
    var names = dports(net, d).concat(Object.keys(c.ifs).filter(function (k) { return !/^(fa|gi|eth)\d+(\/\d+){1,2}$/.test(k); }).sort());
    if (X(st).kind === 'sw' && names.indexOf('vlan1') < 0) names.push('vlan1');
    names.forEach(function (k) { var x = c.ifs[k] || {}, sh = EL.ios.isShut(st, k, x), up = EL.ios.ifUp(st, k, x);
      o.push(pad(full(k), 23) + pad(x.ip ? x.ip[0] : 'unassigned', 16) + pad('YES', 4) + pad(x.ip ? 'manual' : 'unset', 7) + pad(sh ? 'administratively down' : up ? 'up' : 'down', 22) + (!sh && up ? 'up' : 'down')); });
    return o.join('\n');
  });
  function ifn(st, n) { var s = X(st).sub || {}; n = String(n || '').split(':')[0]; return full(s[n] || n); }
  var CODES = 'Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP\n       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area\n' +
    '       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2\n       E1 - OSPF external type 1, E2 - OSPF external type 2\n' +
    '       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2\n       ia - IS-IS inter area, * - candidate default, U - per-user static route\n' +
    '       o - ODR, P - periodic downloaded static route, H - NHRP\n       + - replicated route\n';
  function classful(n) { var v = IP.ip2n(n); return v >>> 31 === 0 ? 8 : v >>> 30 === 2 ? 16 : 24; }
  function age(st) { var t = Math.floor((st.net && st.net.now) || 0); return ('0' + Math.floor(t / 3600)).slice(-2) + ':' + ('0' + Math.floor(t / 60) % 60).slice(-2) + ':' + ('0' + t % 60).slice(-2); }
  function showRoute(st) {
    var net = st.net; if (!net) return '';
    var all = net.routes(st.dev), by = net.best(st.dev, all), rows = [], gw = null;
    all.forEach(function (r) { if (r.dead || by[r.net] !== r) return; var p = r.net.split('/');
      if (r.p === 'C') { var me = net.ifaces(st.dev).filter(function (f) { return f.name === r.ifn; })[0];
        rows.push({ c: 'C', net: p[0], len: +p[1], t: 'is directly connected, ' + ifn(st, r.ifn) });
        if (me && me.len < 32) rows.push({ c: 'L', net: me.ip, len: 32, t: 'is directly connected, ' + ifn(st, r.ifn) }); return; }
      var code = r.p === 'O' ? 'O' : r.p === 'R' ? 'R' : r.p === 'S' ? 'S' : r.p === 'B' ? 'B' : r.p;
      if (r.net === '0.0.0.0/0') { code += '*'; gw = r.nh; }
      rows.push({ c: code, net: p[0], len: +p[1], t: '[' + (r.cad !== undefined ? r.cad : r.ad) + '/' + (r.m || 0) + '] via ' + r.nh + (r.p === 'S' ? '' : ', ' + age(st) + ', ' + ifn(st, r.ifn)) }); });
    var o = [CODES, gw ? 'Gateway of last resort is ' + gw + ' to network 0.0.0.0' : 'Gateway of last resort is not set', ''];
    var grp = {}; rows.forEach(function (r) { var cl = r.len === 0 ? 0 : classful(r.net), k = r.len === 0 ? '0.0.0.0/0' : IP.netOf(r.net, Math.min(cl, r.len)) + '|' + cl; (grp[k] = grp[k] || []).push(r); });
    Object.keys(grp).sort(function (a, b) { return IP.ip2n(a.split('/')[0]) - IP.ip2n(b.split('/')[0]); }).forEach(function (k) { var L = grp[k], cl = +k.split('|')[1], maj = k.split('|')[0].split('/')[0];
      L.sort(function (a, b) { return IP.ip2n(a.net) - IP.ip2n(b.net) || a.len - b.len; });
      var masks = L.map(function (r) { return r.len; }).filter(function (x, i, s) { return s.indexOf(x) === i; });
      if (k === '0.0.0.0/0' || L.length === 1 && L[0].len === cl) { L.forEach(function (r) { o.push(pad(r.c, 9) + r.net + '/' + r.len + ' ' + r.t); }); return; }
      if (masks.length === 1) { o.push('      ' + maj + '/' + cl + ' is subnetted, ' + L.length + ' subnets'); L.forEach(function (r) { o.push(pad(r.c, 9) + r.net + ' ' + r.t); }); }
      else { o.push('      ' + maj + '/' + cl + ' is variably subnetted, ' + L.length + ' subnets, ' + masks.length + ' masks'); L.forEach(function (r) { o.push(pad(r.c, 9) + r.net + '/' + r.len + ' ' + r.t); }); } });
    return o.join('\n');
  }
  var sr = cmd('exec', 'show ip route', function (st) { return showRoute(st); }, 'IP routing table'); sr.cfg = false; sr.ok = function (st) { return X(st).kind !== 'asa'; };

  // ---------------------------------------------------------------- устройство в модели сети
  function fresh() { return { ifs: {} }; }
  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {};
    if (m.vendor !== 'cisco') return d;
    var st = d.st, n = +String(d.id).slice(1) || 1;
    d.sub = 'ios'; st.mode = 'ios';
    if (m.type === 'mes') st.bmac = '00:0a:f3:' + ('0' + ((n * 37) & 255).toString(16)).slice(-2) + ':' + ('0' + ((n * 101) & 255).toString(16)).slice(-2) + ':' + ('0' + (n & 255).toString(16)).slice(-2);
    st.ios = { kind: m.kind === 'cs-asa' ? 'asa' : m.type === 'mes' ? 'sw' : 'rt', l3: !!m.l3, costs: m.costs || 'short', stack: [], c: fresh(), saved: null, ask: null };
    compile(st);
    return d;
  };
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id]; if (!isIos(d)) return ex0.apply(this, arguments); this.gen++; return d.off ? '' : exec(d.st, line); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; return isIos(d) ? prompt(d.st) : pr0.apply(this, arguments); };
  var he0 = P.help;
  P.help = function (id, line) { var d = this.devs[id]; return isIos(d) ? help(d.st, line) : he0.apply(this, arguments); };
  var tb0 = P.tab;
  P.tab = function (id, line) { var d = this.devs[id]; return isIos(d) ? tab(d.st, line) : tb0.apply(this, arguments); };
  var rb0 = P.reboot;
  P.reboot = function (id) { var d = this.devs[id]; if (!isIos(d)) return rb0.apply(this, arguments);
    var x = d.st.ios; x.c = x.saved ? EL.clone(x.saved) : fresh(); x.stack = []; x.ask = null; compile(d.st);
    this.mac[id] = {}; this.arp[id] = {}; d.off = false; this.gen++; };
  var sh0 = P.setHost;
  P.setHost = function (id, name) { var d = this.devs[id]; if (!isIos(d)) return sh0.apply(this, arguments); d.st.ios.c.hostname = name; compile(d.st); };
  var aa0 = P.arpAge;                              // ARP: 4 ч (spec/defaults-vs-eltex.md, общ.), MAC — 300 с (CG-2960X)
  P.arpAge = function (id) { return isIos(this.devs[id]) ? 14400 : aa0.apply(this, arguments); };
  if (EL.cfgText) { var ct0 = EL.cfgText; EL.cfgText = function (d) { return isIos(d) ? cfgText(d.st) : ct0.apply(this, arguments); }; }
  if (EL.applyConfig) { var ap0 = EL.applyConfig; EL.applyConfig = function (n, id, text) { var d = n.devs[id]; if (!isIos(d)) return ap0.apply(this, arguments);
    var errs = [], x = d.st.ios; x.ask = null; x.stack = [{ v: 'priv' }, { v: 'config' }];
    String(text).split('\n').forEach(function (l) { if (!l.trim() || /^\s*(!|end\s*$|Building|Current configuration|version )/.test(l)) return;
      if (/^\S/.test(l)) toConfig(d.st); var r = n.exec(id, l.trim()); if (/^%|\n%/.test(r)) errs.push(d.name + ' «' + l.trim() + '» → ' + r.split('\n').pop()); });
    x.stack = []; return errs; }; }

  EL.ios = { showRoute: showRoute, cmd: cmd, T: T, exec: exec, prompt: prompt, norm: norm, full: full, short: short, isIos: isIos, dports: dports, ifc: ifc, cur: cur, curNames: curNames, top: top, push: push,
    pad: pad, phyUp: phyUp, cfgText: cfgText, ifn: ifn, compile: compile, list: list, age: age, classful: classful,
    isShut: function (st, k, x) { return !!x.shut; }, ifUp: function (st, k) { return phyUp(st, k); },
    compileSw: function () {}, compileRt: function () {}, compileAsa: function () {}, cfgAsa: function () { return ''; }, renderSw: function () {}, renderRt: function () {} };
})(typeof window !== 'undefined' ? window : global);
