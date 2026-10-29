/* Пограничный контроллер сессий ESBC-3200 / vESBC (руководство пользователя ESBC 1.9.0, пример «Настройка для SIP-абонентов»).
   Основа — ESR: интерфейсы, маршруты, межсетевой экран, commit / confirm — как на ESR. Раздел esbc → esbc(config-esbc)#:
     sip transport ИМЯ → (config-esbc-sip-transport)#: ip address A, port N (по умолчанию 5060);
     media resource ИМЯ → (config-esbc-media-resource)#: ip address A, port-range A-B;
     trunk sip ИМЯ → (config-esbc-trunk-sip)#: sip transport ИМЯ, remote address A, remote port N, media resource N ИМЯ;
     user-interface sip ИМЯ → (config-esbc-user-interface-sip)#: sip transport ИМЯ, media resource N ИМЯ, nat comedia-mode on|off, route-table ИМЯ;
     route-table ИМЯ → (config-esbc-route-table)#: rule N → (config-esbc-route-table-rule)#: action direct-to-trunk ТРАНК.
   show esbc users sip, show esbc trunks sip, show esbc active calls.
   Сценарий с TAU / SMG: абоненты (TAU) регистрируются на адрес и порт транспорта user-interface; ESBC по route-table отправляет REGISTER и INVITE
   в SIP-транк (на SMG / Softswitch) со своего транспорта транка; встречные вызовы приходят из транка и уходят абоненту по его регистрации.
   Речь (RTP) идёт через ESBC: абонент ↔ media resource user-interface, media resource транка ↔ встречная сторона.
   nat comedia-mode on — RTP отправляется туда, откуда он пришёл (абонент за NAT); без него у абонента за Source NAT разговор без звука.
   Упрощения: правила маршрутизации без условий (первое правило route-table), SIP-профили, модификаторы, балансировка, H.323, CDR,
   белые/чёрные списки и защита от флуда не моделируются; порты ESBC-3200 названы gigabitethernet 1/0/N, как в примере руководства. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  function isE(d) { return !!d && d.sub === 'esbc'; }
  EL.isEsbc = isE;
  var M = { esbc: '(config-esbc)#', esbt: '(config-esbc-sip-transport)#', esbm: '(config-esbc-media-resource)#', esbk: '(config-esbc-trunk-sip)#',
            esbu: '(config-esbc-user-interface-sip)#', esbr: '(config-esbc-route-table)#', esbq: '(config-esbc-route-table-rule)#' };
  Object.keys(M).forEach(function (k) { S.PROMPT[k] = M[k]; });
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes = c.modes.concat(Object.keys(M)); });
  function touch(st) { st.pending = true; }
  function bad() { return 'Syntax error: Illegal parameter'; }
  function B(c) { return c.esbc || (c.esbc = { tr: {}, media: {}, trunk: {}, ui: {}, rt: {} }); }
  function cur(st, k) { return B(st.cand)[k][st.esb]; }
  function onE(st) { var d = st.net && st.net.devs[st.dev]; return !st.net || isE(d); }

  S.cmd('config', 'esbc', function (st) { if (!onE(st)) return 'Syntax error: Unknown command'; B(st.cand); st.mode = 'esbc'; }, 'Настройка пограничного контроллера сессий (ESBC)');
  S.cmd('esbc', 'exit', function (st) { st.mode = 'config'; });
  // объекты раздела esbc: создание, удаление, выход
  [['sip transport', 'tr', 'esbt', 'SIP-транспорт (адрес и порт приёма SIP)'], ['media resource', 'media', 'esbm', 'Медиаресурс (адрес и порты RTP)'],
   ['trunk sip', 'trunk', 'esbk', 'SIP-транк к Softswitch / SMG'], ['user-interface sip', 'ui', 'esbu', 'Интерфейс SIP-абонентов'], ['route-table', 'rt', 'esbr', 'Таблица маршрутизации вызовов']]
    .forEach(function (o) { var name = o[0], k = o[1], mode = o[2];
      S.cmd('esbc', name + ' <w>', function (st, a) { var L = B(st.cand)[k]; if (!L[a[0]]) { L[a[0]] = k === 'rt' ? { rules: {} } : k === 'ui' || k === 'trunk' ? { media: {} } : {}; touch(st); }
        st.mode = mode; st.esb = a[0]; }, o[3]);
      S.cmd('esbc', 'no ' + name + ' <w>', function (st, a) { delete B(st.cand)[k][a[0]]; touch(st); });
      S.cmd(mode, 'exit', function (st) { st.mode = 'esbc'; st.esb = null; }); });
  S.cmd('esbt esbm', 'ip address <ip>', function (st, a) { cur(st, st.mode === 'esbt' ? 'tr' : 'media').ip = a[0]; touch(st); }, 'Локальный IP-адрес');
  S.cmd('esbt', 'port <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return bad(); cur(st, 'tr').port = a[0]; touch(st); }, 'UDP-порт SIP (по умолчанию 5060)');
  S.cmd('esbt', 'no port', function (st) { delete cur(st, 'tr').port; touch(st); });
  S.cmd('esbm', 'port-range <w>', function (st, a) { var m = a[0].match(/^(\d+)-(\d+)$/); if (!m || +m[1] < 1 || +m[2] > 65535 || +m[1] > +m[2]) return bad();
    cur(st, 'media').range = [+m[1], +m[2]]; touch(st); }, 'Диапазон UDP-портов RTP A-B');
  S.cmd('esbk esbu', 'sip transport <w>', function (st, a) { cur(st, st.mode === 'esbk' ? 'trunk' : 'ui').tr = a[0]; touch(st); }, 'SIP-транспорт');
  S.cmd('esbk esbu', 'media resource <n> <w>', function (st, a) { if (a[0] > 15) return bad(); cur(st, st.mode === 'esbk' ? 'trunk' : 'ui').media[a[0]] = a[1]; touch(st); }, 'Медиаресурс (индекс, имя)');
  S.cmd('esbk esbu', 'no media resource <n>', function (st, a) { delete cur(st, st.mode === 'esbk' ? 'trunk' : 'ui').media[a[0]]; touch(st); });
  S.cmd('esbk', 'remote address <ip>', function (st, a) { cur(st, 'trunk').ra = a[0]; touch(st); }, 'Адрес встречной стороны транка');
  S.cmd('esbk', 'remote port <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return bad(); cur(st, 'trunk').rp = a[0]; touch(st); }, 'Порт встречной стороны (5060)');
  S.cmd('esbu', 'nat comedia-mode <w>', function (st, a) { if (!/^(on|off)$/.test(a[0])) return bad(); cur(st, 'ui').comedia = a[0] === 'on'; touch(st); }, 'RTP туда, откуда пришёл (абоненты за NAT)');
  S.cmd('esbu', 'route-table <w>', function (st, a) { cur(st, 'ui').rt = a[0]; touch(st); }, 'Таблица маршрутизации вызовов абонентов');
  S.cmd('esbu', 'no route-table', function (st) { delete cur(st, 'ui').rt; touch(st); });
  S.cmd('esbr', 'rule <n>', function (st, a) { var R = cur(st, 'rt').rules; R[a[0]] = R[a[0]] || {}; st.esbRule = a[0]; st.mode = 'esbq'; touch(st); }, 'Правило таблицы');
  S.cmd('esbr', 'no rule <n>', function (st, a) { delete cur(st, 'rt').rules[a[0]]; touch(st); });
  S.cmd('esbq', 'action direct-to-trunk <w>', function (st, a) { cur(st, 'rt').rules[st.esbRule].trunk = a[0]; touch(st); }, 'Направить вызов в транк');
  S.cmd('esbq', 'exit', function (st) { st.mode = 'esbr'; st.esbRule = null; });

  S.RUNX.push(function (c, out) { var x = c.esbc; if (!x) return; out.push('esbc');
    function md(o) { Object.keys(o.media).sort().forEach(function (i) { out.push('    media resource ' + i + ' ' + o.media[i]); }); }
    Object.keys(x.tr).sort().forEach(function (k) { var t = x.tr[k]; out.push('  sip transport ' + k); if (t.ip) out.push('    ip address ' + t.ip); if (t.port) out.push('    port ' + t.port); out.push('  exit'); });
    Object.keys(x.media).sort().forEach(function (k) { var t = x.media[k]; out.push('  media resource ' + k); if (t.ip) out.push('    ip address ' + t.ip); if (t.range) out.push('    port-range ' + t.range.join('-')); out.push('  exit'); });
    Object.keys(x.trunk).sort().forEach(function (k) { var t = x.trunk[k]; out.push('  trunk sip ' + k); if (t.tr) out.push('    sip transport ' + t.tr);
      if (t.ra) out.push('    remote address ' + t.ra); if (t.rp) out.push('    remote port ' + t.rp); md(t); out.push('  exit'); });
    Object.keys(x.rt).sort().forEach(function (k) { var t = x.rt[k]; out.push('  route-table ' + k);
      Object.keys(t.rules).sort(function (a, b) { return a - b; }).forEach(function (n) { out.push('    rule ' + n); if (t.rules[n].trunk) out.push('      action direct-to-trunk ' + t.rules[n].trunk); out.push('    exit'); }); out.push('  exit'); });
    Object.keys(x.ui).sort().forEach(function (k) { var t = x.ui[k]; out.push('  user-interface sip ' + k); if (t.tr) out.push('    sip transport ' + t.tr); md(t);
      if (t.comedia) out.push('    nat comedia-mode on'); if (t.rt) out.push('    route-table ' + t.rt); out.push('  exit'); });
    out.push('exit'); });

  // ---------------------------------------------------------------- логика: транспорт → user-interface → route-table → транк
  function cfg(d) { return d.st.run.esbc || { tr: {}, media: {}, trunk: {}, ui: {}, rt: {} }; }
  function port(t) { return t && (t.port || 5060); }
  function owns(net, d, ip) { return net.ifaces(d.id).some(function (x) { return x.ip === ip; }); }
  // абонентский интерфейс, принимающий SIP на ip:port
  function uiAt(net, d, ip, p) { var c = cfg(d); return Object.keys(c.ui).map(function (k) { var u = c.ui[k], t = c.tr[u.tr];
    return t && t.ip === ip && port(t) === p && owns(net, d, t.ip) ? { name: k, ui: u, tr: t, trName: u.tr } : null; }).filter(Boolean)[0] || null; }
  function trunkOf(d, ui) { var c = cfg(d), rt = ui.rt && c.rt[ui.rt]; if (!rt) return { why: ui.rt ? 'нет route-table ' + ui.rt : 'у user-interface не задан route-table' };
    var n = Object.keys(rt.rules).sort(function (a, b) { return a - b; }).filter(function (k) { return rt.rules[k].trunk; })[0];
    if (n === undefined) return { why: 'в route-table ' + ui.rt + ' нет правила с action direct-to-trunk' };
    var tk = c.trunk[rt.rules[n].trunk]; if (!tk) return { why: 'нет trunk sip ' + rt.rules[n].trunk };
    var t = c.tr[tk.tr]; if (!t || !t.ip) return { why: 'у trunk sip ' + rt.rules[n].trunk + ' не задан sip transport с ip address' };
    if (!tk.ra) return { why: 'у trunk sip ' + rt.rules[n].trunk + ' не задан remote address' };
    return { name: rt.rules[n].trunk, rule: n, rt: ui.rt, tk: tk, tr: t, trName: tk.tr }; }
  // транк, в который смотрит встречная сторона (запрос от SMG на ip:port транспорта транка)
  function trunkAt(d, ip, p) { var c = cfg(d); return Object.keys(c.trunk).map(function (k) { var tk = c.trunk[k], t = c.tr[tk.tr];
    return t && t.ip === ip && port(t) === p ? { name: k, tk: tk, tr: t } : null; }).filter(Boolean)[0] || null; }
  function mediaIp(d, o) { var c = cfg(d), m = o && c.media[o.media[Object.keys(o.media).sort()[0]]]; return m && m.ip ? m : null; }
  EL.listensX = (function (lx0) { return function (d, proto, p) {
    if (isE(d) && proto === 'udp') { var c = cfg(d);
      if (Object.keys(c.tr).some(function (k) { return port(c.tr[k]) === p && c.tr[k].ip; })) return true;
      if (p === 5004 && Object.keys(c.media).some(function (k) { return c.media[k].ip; })) return true; }   // порт RTP ESBC выбирает сам из port-range
    return lx0 ? lx0(d, proto, p) : undefined; }; })(EL.listensX);
  EL.esbcHop = { uiAt: uiAt, trunkOf: trunkOf, trunkAt: trunkAt, mediaIp: mediaIp, cfg: cfg, port: port };

  // ---------------------------------------------------------------- show esbc
  function pad(s, n) { return (String(s) + new Array(n + 1).join(' ')).slice(0, n); }
  S.cmd('priv', 'show esbc users sip', function (st) { var net = st.net; if (!net) return ''; var d = net.devs[st.dev], t = net.voipRegs(), o = [pad('Number', 12) + pad('User-interface', 18) + pad('Contact', 22) + 'Trunk'];
    Object.keys(t).forEach(function (k) { var r = t[k]; if (!r.ok || r.via !== d.id) return; o.push(pad(r.num, 12) + pad(r.ui, 18) + pad(net.devs[r.tau].st.ip + ':5060', 22) + r.trunk); });
    return o.length > 1 ? o.join('\n') : o.concat(['Нет зарегистрированных абонентов']).join('\n'); }, 'Зарегистрированные SIP-абоненты');
  S.cmd('priv', 'show esbc trunks sip', function (st) { var net = st.net, d = net && net.devs[st.dev]; if (!d) return ''; var c = cfg(d), o = [pad('Trunk', 16) + pad('Transport', 24) + pad('Remote', 22) + 'State'];
    Object.keys(c.trunk).sort().forEach(function (k) { var tk = c.trunk[k], t = c.tr[tk.tr], ok = t && t.ip && tk.ra && net.request(d.id, tk.ra, 'udp', tk.rp || 5060).ok;
      o.push(pad(k, 16) + pad(t && t.ip ? t.ip + ':' + port(t) : '-', 24) + pad(tk.ra ? tk.ra + ':' + (tk.rp || 5060) : '-', 22) + (ok ? 'available' : 'unavailable')); });
    return o.join('\n'); }, 'Состояние SIP-транков');
  S.cmd('priv', 'show esbc active calls', function (st) { var net = st.net; if (!net) return ''; var L = (net._esbCalls || []).filter(function (x) { return x.esbc === st.dev; });
    return L.length ? [pad('From', 10) + pad('To', 10) + 'Legs'].concat(L.map(function (x) { return pad(x.from, 10) + pad(x.to, 10) + x.legs; })).join('\n') : 'No active calls'; }, 'Активные вызовы');

  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}; if (m.kind === 'esbc') d.sub = 'esbc'; return d; };
  var boot0 = P.reboot;
  if (boot0) P.reboot = function (id) { var was = isE(this.devs[id]), r = boot0.apply(this, arguments); if (was && this.devs[id]) this.devs[id].sub = 'esbc'; return r; };
})(typeof window !== 'undefined' ? window : global);
