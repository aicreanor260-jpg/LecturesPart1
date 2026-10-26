/* Тренажёр CLI маршрутизатора Eltex ESR для деки «IP-сервисы 2.6».
   Режимы и приглашения как в pptx: ESR# → configure → ESR(config)# → interface … → ESR(config-if-gi)# и т.д.
   Задания генерируются случайно («Обновить задание»), проверяется итоговое состояние; «Отправить пакет» показывает,
   что произойдёт с DHCP-запросом / пакетом через NAT / синхронизацией NTP при текущей конфигурации. */
(function () {
  'use strict';

  function fresh() {
    return { mode: 'priv', ctx: null, ifs: {}, zones: {}, pairs: {}, og: {}, snat: { pools: {}, rs: {} },
      dnat: { pools: {}, rs: {} }, routes: [], dhcp: false, pools: {}, relay: false, ntp: { on: false, servers: {} } };
  }
  var PR = { priv: '#', config: '(config)#', ifgi: '(config-if-gi)#', ifte: '(config-if-te)#', zone: '(config-zone)#',
    zpair: '(config-zone-pair)#', zrule: '(config-zone-pair-rule)#', snat: '(config-snat)#', snatpool: '(config-snat-pool)#',
    snatrs: '(config-snat-ruleset)#', snatrule: '(config-snat-rule)#', dnat: '(config-dnat)#', dnatpool: '(config-dnat-pool)#',
    dnatrs: '(config-dnat-ruleset)#', dnatrule: '(config-dnat-rule)#', ogn: '(config-object-group-network)#',
    ogs: '(config-object-group-service)#', dhcp: '(config-dhcp-server)#', ntp: '(config-ntp)#' };
  var PARENT = { ifgi: 'config', ifte: 'config', zone: 'config', zpair: 'config', zrule: 'zpair', snat: 'config',
    snatpool: 'snat', snatrs: 'snat', snatrule: 'snatrs', dnat: 'config', dnatpool: 'dnat', dnatrs: 'dnat',
    dnatrule: 'dnatrs', ogn: 'config', ogs: 'config', dhcp: 'config', ntp: 'config', config: 'priv' };
  function prompt(st) { return 'ESR' + PR[st.mode]; }

  var IPRE = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/;
  function isIp(s) { var m = IPRE.exec(s); return !!m && m.slice(1).every(function (o) { return +o <= 255; }); }
  function ip2n(s) { return s.split('.').reduce(function (a, o) { return a * 256 + (+o); }, 0); }
  function pfx(s) {                       // 192.168.1.1/24 или "192.168.1.1 /24"
    var m = /^([\d.]+)\/(\d{1,2})$/.exec(s); if (!m || !isIp(m[1]) || +m[2] > 32) return null; return { ip: m[1], len: +m[2] };
  }
  function range(s) {                     // a-b или a
    var p = s.split('-'); if (p.length > 2 || !p.every(isIp)) return null;
    var a = ip2n(p[0]), b = ip2n(p[1] || p[0]); return b < a ? null : { a: a, b: b, s: s };
  }
  function ifname(t) {
    var m = /^(gigabitethernet|gi|tengigabitethernet|te)(\d+\/\d+\/\d+(?:\.\d+)?)$/.exec(t.replace(/\s+/g, ''));
    if (!m) return null; return { kind: /^te/.test(m[1]) ? 'te' : 'gi', id: m[2] };
  }
  function kw(t, word, min) { return t === word || (t && t.length >= (min || 2) && word.indexOf(t) === 0); }

  // ------------------------------------------------------------------ интерпретатор
  function run(st, line) {
    var raw = line.trim(); if (!raw) return '';
    var tk = raw.split(/\s+/);
    // «interface gigabitethernet 1/0/1» → склеить имя интерфейса
    if (kw(tk[0], 'interface') && tk.length === 3) tk = [tk[0], tk[1] + tk[2]];
    // «ip address 10.10.1.28 /24» → склеить маску
    for (var i = 1; i < tk.length; i++) if (/^\/\d+$/.test(tk[i])) { tk[i - 1] += tk[i]; tk.splice(i, 1); }
    var c0 = tk[0], m = st.mode;

    if (kw(c0, 'end')) { st.mode = 'priv'; st.ctx = null; return ''; }
    if (kw(c0, 'exit')) { if (m === 'priv') return '% Сессия остаётся открытой (тренажёр)'; st.mode = PARENT[m];
      if (st.mode === 'config' || st.mode === 'priv') st.ctx = null; else st.ctx = st.ctx && st.ctx.up; return ''; }
    if (kw(c0, 'show')) return show(st, tk.slice(1));
    if (kw(c0, 'do') && m !== 'priv') return show(st, tk.slice(2));
    if (m === 'priv') {
      if (kw(c0, 'configure')) { st.mode = 'config'; return ''; }
      return '% Unknown command. В привилегированном режиме: configure, show …';
    }
    var f = H[m]; var r = f ? f(st, tk) : undefined;
    return r === undefined ? '% Unknown command' : r;
  }
  function enter(st, mode, ctx) { if (ctx) ctx.up = st.ctx; st.mode = mode; st.ctx = ctx || null; return ''; }
  function rule(set, n) { if (!set[n]) set[n] = { match: {}, action: null, en: false }; return set[n]; }

  var H = {
    config: function (st, t) {
      var a = t[0], b = t[1];
      if (kw(a, 'interface')) { var f = ifname(t[1] || ''); if (!f) return '% Неверное имя интерфейса';
        var I = st.ifs[f.kind + f.id] = st.ifs[f.kind + f.id] || { kind: f.kind, id: f.id };
        return enter(st, f.kind === 'te' ? 'ifte' : 'ifgi', { iface: I }); }
      if (kw(a, 'security') && kw(b, 'zone') && t.length === 3) { st.zones[t[2]] = true; return enter(st, 'zone', { z: t[2] }); }
      if (kw(a, 'security') && kw(b, 'zone-pair', 6) && t.length === 4) {
        if (!st.zones[t[2]] || !st.zones[t[3]]) return '% Зона не создана: security zone ' + (!st.zones[t[2]] ? t[2] : t[3]);
        var k = t[2] + '>' + t[3]; st.pairs[k] = st.pairs[k] || {}; return enter(st, 'zpair', { pair: st.pairs[k] }); }
      if (kw(a, 'object-group') && t.length === 3 && (kw(b, 'network') || kw(b, 'service'))) {
        var net = kw(b, 'network'); st.og[t[2]] = st.og[t[2]] || { type: net ? 'net' : 'svc', items: [] };
        return enter(st, net ? 'ogn' : 'ogs', { og: st.og[t[2]] }); }
      if (kw(a, 'nat') && kw(b, 'source') && t.length === 2) return enter(st, 'snat');
      if (kw(a, 'nat') && kw(b, 'destination') && t.length === 2) return enter(st, 'dnat');
      if (kw(a, 'ip') && kw(b, 'route') && t.length === 4) { var p = pfx(t[2]); if (!p || !isIp(t[3])) return '% Формат: ip route 0.0.0.0/0 <шлюз>';
        st.routes.push(t[2] + ' ' + t[3]); return ''; }
      if (kw(a, 'ip') && b === 'dhcp-server' && t.length === 2) { st.dhcp = true; return ''; }
      if (kw(a, 'ip') && b === 'dhcp-server' && kw(t[2], 'pool') && t[3]) {
        st.pools[t[3]] = st.pools[t[3]] || { name: t[3] }; return enter(st, 'dhcp', { pool: st.pools[t[3]] }); }
      if (kw(a, 'ip') && b === 'dhcp-relay' && t.length === 2) { st.relay = true; return ''; }
      if (kw(a, 'ntp') && kw(b, 'enable')) { st.ntp.on = true; return ''; }
      if (kw(a, 'ntp') && kw(b, 'server') && t[2]) { if (!isIp(t[2])) return '% Неверный IP-адрес';
        st.ntp.servers[t[2]] = st.ntp.servers[t[2]] || { prefer: false, minpoll: 6 }; return enter(st, 'ntp', { srv: st.ntp.servers[t[2]] }); }
    },
    ifgi: function (st, t) { return iface(st, t); },
    ifte: function (st, t) { return iface(st, t); },
    zone: function () { },
    zpair: function (st, t) { if (kw(t[0], 'rule') && /^\d+$/.test(t[1] || '')) return enter(st, 'zrule', { r: rule(st.ctx.pair, t[1]) }); },
    zrule: function (st, t) { return ruleCmd(st, t, ['source-address', 'destination-address', 'destination-nat'], ['permit', 'deny']); },
    snat: function (st, t) {
      if (kw(t[0], 'pool') && t[1]) { st.snat.pools[t[1]] = st.snat.pools[t[1]] || {}; return enter(st, 'snatpool', { p: st.snat.pools[t[1]] }); }
      if (kw(t[0], 'ruleset') && t[1]) { st.snat.rs[t[1]] = st.snat.rs[t[1]] || { rules: {} }; return enter(st, 'snatrs', { rs: st.snat.rs[t[1]] }); }
    },
    snatpool: function (st, t) { if (kw(t[0], 'ip') && kw(t[1], 'address-range', 9) && t[2]) { if (!range(t[2])) return '% Неверный диапазон';
      st.ctx.p.range = t[2]; return ''; } },
    snatrs: function (st, t) {
      if (kw(t[0], 'to') && kw(t[1], 'zone') && t[2]) { if (!st.zones[t[2]]) return '% Зона не создана'; st.ctx.rs.to = t[2]; return ''; }
      if (kw(t[0], 'rule') && /^\d+$/.test(t[1] || '')) return enter(st, 'snatrule', { r: rule(st.ctx.rs.rules, t[1]) });
    },
    snatrule: function (st, t) {
      if (kw(t[0], 'action') && kw(t[1], 'source-nat', 6) && kw(t[2], 'pool') && t[3]) {
        if (!st.snat.pools[t[3]]) return '% Пул не найден: pool ' + t[3]; st.ctx.r.action = 'source-nat pool ' + t[3]; return ''; }
      return ruleCmd(st, t, ['source-address'], []);
    },
    dnat: function (st, t) {
      if (kw(t[0], 'pool') && t[1]) { st.dnat.pools[t[1]] = st.dnat.pools[t[1]] || {}; return enter(st, 'dnatpool', { p: st.dnat.pools[t[1]] }); }
      if (kw(t[0], 'ruleset') && t[1]) { st.dnat.rs[t[1]] = st.dnat.rs[t[1]] || { rules: {} }; return enter(st, 'dnatrs', { rs: st.dnat.rs[t[1]] }); }
    },
    dnatpool: function (st, t) {
      if (kw(t[0], 'ip') && kw(t[1], 'address') && isIp(t[2] || '')) { st.ctx.p.ip = t[2]; return ''; }
      if (kw(t[0], 'ip') && kw(t[1], 'port') && /^\d+$/.test(t[2] || '')) { st.ctx.p.port = +t[2]; return ''; }
    },
    dnatrs: function (st, t) {
      if (kw(t[0], 'from') && kw(t[1], 'zone') && t[2]) { if (!st.zones[t[2]]) return '% Зона не создана'; st.ctx.rs.from = t[2]; return ''; }
      if (kw(t[0], 'rule') && /^\d+$/.test(t[1] || '')) return enter(st, 'dnatrule', { r: rule(st.ctx.rs.rules, t[1]) });
    },
    dnatrule: function (st, t) {
      if (kw(t[0], 'match') && kw(t[1], 'protocol') && /^(tcp|udp)$/.test(t[2] || '')) { st.ctx.r.match.protocol = t[2]; return ''; }
      if (kw(t[0], 'action') && kw(t[1], 'destination-nat', 6) && kw(t[2], 'pool') && t[3]) { st.ctx.r.action = 'destination-nat pool ' + t[3]; return ''; }
      return ruleCmd(st, t, ['destination-address', 'destination-port'], []);
    },
    ogn: function (st, t) {
      if (kw(t[0], 'ip') && (kw(t[1], 'address-range', 9) || kw(t[1], 'address')) && t[2]) {
        if (!range(t[2])) return '% Неверный адрес или диапазон'; st.ctx.og.items.push(t[2]); return ''; }
    },
    ogs: function (st, t) { if (kw(t[0], 'port') && /^\d+(-\d+)?$/.test(t[1] || '')) { st.ctx.og.items.push(t[1]); return ''; } },
    dhcp: function (st, t) {
      var P = st.ctx.pool;
      if (kw(t[0], 'network') && pfx(t[1] || '')) { P.network = t[1]; return ''; }
      if (kw(t[0], 'address-range', 9) && t[1]) { if (!range(t[1])) return '% Неверный диапазон'; P.range = t[1]; return ''; }
      if (kw(t[0], 'excluded-address-range', 4) && t[1]) { if (!range(t[1])) return '% Неверный диапазон'; P.excl = t[1]; return ''; }
      if (kw(t[0], 'default-router') && isIp(t[1] || '')) { P.gw = t[1]; return ''; }
    },
    ntp: function (st, t) {
      if (kw(t[0], 'prefer')) { st.ctx.srv.prefer = true; return ''; }
      if (kw(t[0], 'minpoll') && /^\d+$/.test(t[1] || '')) { if (+t[1] < 4 || +t[1] > 6) return '% minpoll <4..6>';
        st.ctx.srv.minpoll = +t[1]; return ''; }
    }
  };
  function iface(st, t) {
    var I = st.ctx.iface;
    if (kw(t[0], 'ip') && kw(t[1], 'address') && t[2] === 'dhcp') { I.dhcp = true; I.ip = null; return ''; }
    if (kw(t[0], 'ip') && kw(t[1], 'address') && t[2]) { var p = pfx(t[2]); if (!p) return '% Формат: ip address A.B.C.D/N'; I.ip = t[2]; I.dhcp = false; return ''; }
    if (kw(t[0], 'ip') && kw(t[1], 'dhcp') && kw(t[2], 'server') && kw(t[3], 'address') && isIp(t[4] || '')) { I.dhcpSrv = t[4]; return ''; }
    if (kw(t[0], 'ip') && kw(t[1], 'helper-address', 3) && isIp(t[2] || '')) { I.helper = t[2]; return ''; }
    if (kw(t[0], 'security-zone', 9) && t[1]) { if (!st.zones[t[1]]) return '% Зона не создана: security zone ' + t[1]; I.zone = t[1]; return ''; }
  }
  function ruleCmd(st, t, matches, actions) {
    var R = st.ctx.r;
    if (kw(t[0], 'match')) {
      var what = t[1] || '';
      for (var i = 0; i < matches.length; i++) if (kw(what, matches[i], 6)) {
        if (matches[i] === 'destination-nat') { R.match.dnat = true; return ''; }
        if (!t[2]) return '% Укажите object-group';
        if (!st.og[t[2]]) return '% object-group не найдена: ' + t[2];
        R.match[matches[i]] = t[2]; return '';
      }
      return;
    }
    if (kw(t[0], 'action') && actions.indexOf(t[1]) >= 0) { R.action = t[1]; return ''; }
    if (kw(t[0], 'enable')) { R.en = true; return ''; }
  }

  // ------------------------------------------------------------------ show
  function runcfg(st) {
    var o = [];
    Object.keys(st.og).forEach(function (n) { var g = st.og[n];
      o.push('object-group ' + (g.type === 'net' ? 'network ' : 'service ') + n);
      g.items.forEach(function (x) { o.push(g.type === 'net' ? (x.indexOf('-') > 0 ? '  ip address-range ' + x : '  ip address ' + x) : '  port ' + x); });
      o.push('exit'); });
    Object.keys(st.zones).forEach(function (z) { o.push('security zone ' + z, 'exit'); });
    Object.keys(st.ifs).forEach(function (k) { var I = st.ifs[k];
      o.push('interface ' + (I.kind === 'te' ? 'tengigabitethernet ' : 'gigabitethernet ') + I.id);
      if (I.zone) o.push('  security-zone ' + I.zone);
      if (I.ip) o.push('  ip address ' + I.ip); if (I.dhcp) o.push('  ip address dhcp');
      if (I.dhcpSrv) o.push('  ip dhcp server address ' + I.dhcpSrv); if (I.helper) o.push('  ip helper-address ' + I.helper);
      o.push('exit'); });
    Object.keys(st.pairs).forEach(function (k) { var P = st.pairs[k], z = k.split('>');
      o.push('security zone-pair ' + z[0] + ' ' + z[1]); Object.keys(P).forEach(function (n) { rshow(o, n, P[n]); }); o.push('exit'); });
    ['snat', 'dnat'].forEach(function (s) { var N = st[s];
      if (!Object.keys(N.pools).length && !Object.keys(N.rs).length) return;
      o.push(s === 'snat' ? 'nat source' : 'nat destination');
      Object.keys(N.pools).forEach(function (p) { var P = N.pools[p]; o.push('  pool ' + p);
        if (P.range) o.push('    ip address-range ' + P.range); if (P.ip) o.push('    ip address ' + P.ip);
        if (P.port) o.push('    ip port ' + P.port); o.push('  exit'); });
      Object.keys(N.rs).forEach(function (r) { var R = N.rs[r]; o.push('  ruleset ' + r);
        if (R.to) o.push('    to zone ' + R.to); if (R.from) o.push('    from zone ' + R.from);
        Object.keys(R.rules).forEach(function (n) { rshow(o, n, R.rules[n], '    '); }); o.push('  exit'); });
      o.push('exit'); });
    if (st.dhcp) o.push('ip dhcp-server');
    Object.keys(st.pools).forEach(function (n) { var P = st.pools[n]; o.push('ip dhcp-server pool ' + n);
      if (P.network) o.push('  network ' + P.network); if (P.range) o.push('  address-range ' + P.range);
      if (P.excl) o.push('  excluded-address-range ' + P.excl); if (P.gw) o.push('  default-router ' + P.gw); o.push('exit'); });
    if (st.relay) o.push('ip dhcp-relay');
    st.routes.forEach(function (r) { o.push('ip route ' + r); });
    if (st.ntp.on) o.push('ntp enable');
    Object.keys(st.ntp.servers).forEach(function (a) { var S = st.ntp.servers[a]; o.push('ntp server ' + a);
      if (S.prefer) o.push('  prefer'); if (S.minpoll !== 6) o.push('  minpoll ' + S.minpoll); o.push('exit'); });
    return o.join('\n') || '!';
  }
  function rshow(o, n, R, ind) {
    ind = ind || '  '; o.push(ind + 'rule ' + n);
    Object.keys(R.match).forEach(function (k) { o.push(ind + '  match ' + (k === 'dnat' ? 'destination-nat' : k + ' ' + R.match[k])); });
    if (R.action) o.push(ind + '  action ' + R.action);
    if (R.en) o.push(ind + '  enable'); o.push(ind + 'exit');
  }
  function show(st, t) {
    var s = t.join(' ');
    if (/^ru/.test(s)) return runcfg(st);
    if (/^ip dhcp server pool/.test(s)) { var ks = Object.keys(st.pools); if (!ks.length) return '% Пулы не настроены';
      return ks.map(function (n) { var P = st.pools[n]; return ['name:               ' + n, 'network:            ' + (P.network || '--'),
        'address-ranges:     ' + (P.range || '--'), 'default-router:     ' + (P.gw || '--')].join('\n'); }).join('\n\n'); }
    if (/^ntp conf/.test(s)) { var o = ['NTP status:         ' + (st.ntp.on ? 'Enabled' : 'Disabled'), '',
        'Address          Min poll  Prefer', '---------------  --------  ------'];
      Object.keys(st.ntp.servers).forEach(function (a) { var S = st.ntp.servers[a];
        o.push((a + '                ').slice(0, 17) + (S.minpoll + '         ').slice(0, 10) + (S.prefer ? 'Yes' : 'No')); });
      return o.join('\n'); }
    if (/^ip nat/.test(s)) return runcfg(st).split('\n').filter(function (l, i, a) { return true; }).join('\n');
    return '% Тренажёр поддерживает: show running-config, show ip dhcp server pool, show ntp configuration, show ip nat';
  }

  // ------------------------------------------------------------------ задания
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[R(0, a.length - 1)]; }
  function inRange(st, ogName, ip) {
    var g = st.og[ogName]; if (!g) return false;
    return g.items.some(function (x) { var r = range(x); return r && ip2n(ip) >= r.a && ip2n(ip) <= r.b; });
  }
  function enabledRule(rules, pred) { return Object.keys(rules).some(function (n) { return rules[n].en && pred(rules[n]); }); }

  var TASKS = [
    { // 0. DHCP-сервер (pptx 14)
      gen: function () { var v = pick([10, 20, 30, 40, 50]), g = pick([1, 10, 254]), hi = pick([100, 150, 200]);
        return { v: v, net: '192.168.' + v + '.0/24', gw: '192.168.' + v + '.' + g, rng: '192.168.' + v + '.1-192.168.' + v + '.' + hi }; },
      text: function (p) { return 'Настройте <b>DHCP-сервер</b> на ESR: интерфейс <b>gi1/0/1.' + p.v + '</b> с адресом <b>' + p.gw +
        '/24</b>; включите DHCP-сервер; пул <b>DHCP-' + p.v + '</b>: сеть <b>' + p.net + '</b>, диапазон <b>' + p.rng +
        '</b>, исключить адрес шлюза <b>' + p.gw + '</b>, шлюз по умолчанию <b>' + p.gw + '</b>.'; },
      sol: function (p) { return ['configure', 'interface gi1/0/1.' + p.v, 'ip address ' + p.gw + '/24', 'exit', 'ip dhcp-server',
        'ip dhcp-server pool DHCP-' + p.v, 'network ' + p.net, 'address-range ' + p.rng, 'excluded-address-range ' + p.gw,
        'default-router ' + p.gw, 'exit']; },
      checks: function (p, st) { var I = st.ifs['gi1/0/1.' + p.v] || {}, P = st.pools['DHCP-' + p.v] || {};
        return [['Адрес ' + p.gw + '/24 на gi1/0/1.' + p.v, I.ip === p.gw + '/24'], ['ip dhcp-server', st.dhcp],
          ['Пул DHCP-' + p.v + ': network ' + p.net, P.network === p.net], ['address-range ' + p.rng, P.range === p.rng],
          ['excluded-address-range ' + p.gw, P.excl === p.gw], ['default-router ' + p.gw, P.gw === p.gw]]; },
      send: function (p, st) { var P = st.pools['DHCP-' + p.v] || {}, r = P.range && range(P.range);
        if (!st.dhcp) return ['ПК → DHCPDISCOVER (broadcast)', '✗ ответа нет: DHCP-сервер не включён (ip dhcp-server)'];
        if (!r || !P.network) return ['ПК → DHCPDISCOVER (broadcast)', '✗ пул не настроен — адрес выдать неоткуда'];
        var first = r.a, ex = P.excl && range(P.excl); while (ex && first >= ex.a && first <= ex.b) first++;
        var a = [first >>> 24, first >> 16 & 255, first >> 8 & 255, first & 255].join('.');
        return ['ПК → DHCPDISCOVER (broadcast)', 'ESR → DHCPOFFER: ' + a + (P.gw ? ', шлюз ' + P.gw : ', шлюз не задан'),
          'ПК → DHCPREQUEST', 'ESR → DHCPACK ✓ ПК получил ' + a]; } },
    { // 1. DHCP-ретранслятор (pptx 15)
      gen: function () { var x = R(0, 9), y = R(0, 9); return { wan: '10.' + x + '.0.1/24', srv: '10.' + x + '.0.2', lan: '192.168.' + y + '.1/24' }; },
      text: function (p) { return 'DHCP-сервер <b>' + p.srv + '</b> находится в другой сети. На ESR: <b>gi1/0/1</b> — <b>' + p.wan +
        '</b>, <b>gi1/0/2</b> (сторона клиентов) — <b>' + p.lan + '</b>. Включите <b>DHCP relay</b> и укажите на gi1/0/2 адрес сервера.'; },
      sol: function (p) { return ['configure', 'interface gigabitethernet 1/0/1', 'ip address ' + p.wan, 'exit',
        'interface gigabitethernet 1/0/2', 'ip address ' + p.lan, 'exit', 'ip dhcp-relay', 'interface gigabitethernet 1/0/2',
        'ip helper-address ' + p.srv, 'exit']; },
      checks: function (p, st) { var a = st.ifs['gi1/0/1'] || {}, b = st.ifs['gi1/0/2'] || {};
        return [['gi1/0/1: ' + p.wan, a.ip === p.wan], ['gi1/0/2: ' + p.lan, b.ip === p.lan], ['ip dhcp-relay', st.relay],
          ['gi1/0/2: ip helper-address ' + p.srv, b.helper === p.srv]]; },
      send: function (p, st) { var b = st.ifs['gi1/0/2'] || {};
        if (!st.relay || b.helper !== p.srv) return ['Клиент → DHCPDISCOVER (broadcast) на gi1/0/2',
          '✗ ESR отбрасывает broadcast: ' + (!st.relay ? 'DHCP relay не включён' : 'на gi1/0/2 нет helper-address ' + p.srv)];
        return ['Клиент → DHCPDISCOVER (broadcast) на gi1/0/2', 'ESR (relay) → ' + p.srv + ' (unicast)',
          p.srv + ' → DHCPOFFER через ESR', '✓ клиент получает адрес из сети ' + p.lan.replace(/\.1\//, '.0/')]; } },
    { // 2. DHCP-клиент (pptx 13)
      gen: function () { return { port: R(1, 4), srv: '192.168.' + R(1, 9) + '.' + pick([10, 20, 254]) }; },
      text: function (p) { return 'Настройте интерфейс <b>gi1/0/' + p.port + '</b> как <b>DHCP-клиент</b> и явно укажите DHCP-сервер <b>' +
        p.srv + '</b>.'; },
      sol: function (p) { return ['configure', 'interface gi1/0/' + p.port, 'ip address dhcp', 'ip dhcp server address ' + p.srv, 'exit']; },
      checks: function (p, st) { var I = st.ifs['gi1/0/' + p.port] || {};
        return [['gi1/0/' + p.port + ': ip address dhcp', !!I.dhcp], ['ip dhcp server address ' + p.srv, I.dhcpSrv === p.srv]]; },
      send: function (p, st) { var I = st.ifs['gi1/0/' + p.port] || {};
        if (!I.dhcp) return ['✗ gi1/0/' + p.port + ' не DHCP-клиент — DHCPDISCOVER не отправляется'];
        return ['ESR gi1/0/' + p.port + ' → DHCPDISCOVER', I.dhcpSrv ? 'принимаются предложения сервера ' + I.dhcpSrv : 'принимается первое предложение',
          '✓ интерфейс получает адрес по DHCP']; } },
    { // 3. Source NAT (pptx 33–34)
      gen: function () { var n = R(1, 9), k = pick([1, 2, 3]);
        return { n: n, lan: '192.168.' + n + '.1/24', lr: '192.168.' + n + '.1-192.168.' + n + '.254', wan: '1.1.1.' + k, gw: '1.1.1.254' }; },
      text: function (p) { return 'Настройте <b>Source NAT</b>: зоны <b>TRUST</b> (gi1/0/1, <b>' + p.lan + '</b>) и <b>UNTRUST</b> (te1/0/2, <b>' +
        p.wan + '/29</b>); object-group <b>LOCAL_NET</b> = ' + p.lr + ', <b>WAN_NET</b> = ' + p.wan +
        '; пара зон TRUST → UNTRUST (rule 1, permit для LOCAL_NET); пул <b>WAN_ADDRESS</b> = ' + p.wan +
        '; ruleset <b>SNAT</b> в зону UNTRUST; маршрут по умолчанию через <b>' + p.gw + '</b>.'; },
      sol: function (p) { return ['configure', 'security zone UNTRUST', 'exit', 'security zone TRUST', 'exit',
        'interface gigabitethernet 1/0/1', 'security-zone TRUST', 'ip address ' + p.lan, 'exit',
        'interface tengigabitethernet 1/0/2', 'ip address ' + p.wan + '/29', 'security-zone UNTRUST', 'exit',
        'object-group network LOCAL_NET', 'ip address-range ' + p.lr, 'exit', 'object-group network WAN_NET',
        'ip address-range ' + p.wan, 'exit', 'security zone-pair TRUST UNTRUST', 'rule 1', 'match source-address LOCAL_NET',
        'action permit', 'enable', 'exit', 'exit', 'nat source', 'pool WAN_ADDRESS', 'ip address-range ' + p.wan, 'exit',
        'ruleset SNAT', 'to zone UNTRUST', 'rule 1', 'match source-address LOCAL_NET', 'action source-nat pool WAN_ADDRESS',
        'enable', 'exit', 'exit', 'exit', 'ip route 0.0.0.0/0 ' + p.gw]; },
      checks: function (p, st) { var a = st.ifs['gi1/0/1'] || {}, b = st.ifs['te1/0/2'] || {}, Z = st.pairs['TRUST>UNTRUST'] || {},
        PL = st.snat.pools.WAN_ADDRESS || {}, RS = st.snat.rs.SNAT || { rules: {} };
        return [['gi1/0/1: TRUST, ' + p.lan, a.zone === 'TRUST' && a.ip === p.lan],
          ['te1/0/2: UNTRUST, ' + p.wan + '/29', b.zone === 'UNTRUST' && b.ip === p.wan + '/29'],
          ['LOCAL_NET = ' + p.lr, (st.og.LOCAL_NET || { items: [] }).items.indexOf(p.lr) >= 0],
          ['WAN_NET = ' + p.wan, (st.og.WAN_NET || { items: [] }).items.indexOf(p.wan) >= 0],
          ['TRUST → UNTRUST: rule с LOCAL_NET, permit, enable', enabledRule(Z, function (r) { return r.match['source-address'] === 'LOCAL_NET' && r.action === 'permit'; })],
          ['pool WAN_ADDRESS = ' + p.wan, PL.range === p.wan],
          ['ruleset SNAT: to zone UNTRUST', RS.to === 'UNTRUST'],
          ['rule: LOCAL_NET → source-nat pool WAN_ADDRESS, enable', enabledRule(RS.rules, function (r) { return r.match['source-address'] === 'LOCAL_NET' && r.action === 'source-nat pool WAN_ADDRESS'; })],
          ['ip route 0.0.0.0/0 ' + p.gw, st.routes.indexOf('0.0.0.0/0 ' + p.gw) >= 0]]; },
      send: function (p, st) { var host = '192.168.' + p.n + '.' + R(2, 200), c = this.checks(p, st);
        var bad = c.filter(function (x) { return !x[1]; });
        if (!inRange(st, 'LOCAL_NET', host)) return ['ПК ' + host + ' → 8.8.8.8', '✗ адрес не входит в LOCAL_NET — трансляции нет'];
        if (bad.length) return ['ПК ' + host + ' → 8.8.8.8', '✗ пакет не уходит: ' + bad[0][0]];
        return ['ПК ' + host + ' → 8.8.8.8', 'ESR: TRUST → UNTRUST, rule 1 permit', 'SNAT: источник ' + host + ' → ' + p.wan,
          '✓ ответ 8.8.8.8 → ' + p.wan + ' транслируется обратно на ' + host]; } },
    { // 4. Destination NAT (pptx 35–36)
      gen: function () { var n = R(1, 9), sv = ['FTP_PORT', 21];
        return { n: n, lan: '192.168.' + n + '.1/24', srv: '192.168.' + n + '.100', wan: '1.1.1.1', og: sv[0], port: sv[1] }; },
      text: function (p) { return 'Сервер <b>' + p.srv + '</b> (зона TRUST, gi1/0/1 — <b>' + p.lan + '</b>) должен быть доступен извне по адресу <b>' +
        p.wan + '</b> и порту <b>' + p.port + '</b> (te1/0/2 — ' + p.wan + '/29, зона UNTRUST). Профили: <b>WAN_IP</b>, <b>SERVER_IP</b>, <b>' + p.og +
        '</b>; ruleset <b>DNAT</b> из зоны UNTRUST (tcp, action destination-nat pool <b>SERVER_POOL</b>); пара зон UNTRUST → TRUST с match destination-nat.'; },
      sol: function (p) { return ['configure', 'security zone UNTRUST', 'exit', 'security zone TRUST', 'exit',
        'interface gigabitethernet 1/0/1', 'security-zone TRUST', 'ip address ' + p.lan, 'exit',
        'interface tengigabitethernet 1/0/2', 'ip address ' + p.wan + '/29', 'security-zone UNTRUST', 'exit',
        'object-group network WAN_IP', 'ip address ' + p.wan, 'exit', 'object-group network SERVER_IP', 'ip address ' + p.srv, 'exit',
        'object-group service ' + p.og, 'port ' + p.port, 'exit', 'nat destination', 'ruleset DNAT', 'from zone UNTRUST', 'rule 1',
        'match destination-address WAN_IP', 'match protocol tcp', 'match destination-port ' + p.og,
        'action destination-nat pool SERVER_POOL', 'enable', 'exit', 'exit', 'exit', 'security zone-pair UNTRUST TRUST', 'rule 1',
        'match destination-address SERVER_IP', 'match destination-nat', 'action permit', 'enable', 'exit', 'exit']; },
      checks: function (p, st) { var a = st.ifs['gi1/0/1'] || {}, b = st.ifs['te1/0/2'] || {}, RS = st.dnat.rs.DNAT || { rules: {} },
        Z = st.pairs['UNTRUST>TRUST'] || {}, og = function (n, v) { return (st.og[n] || { items: [] }).items.indexOf(v) >= 0; };
        return [['gi1/0/1: TRUST, ' + p.lan, a.zone === 'TRUST' && a.ip === p.lan],
          ['te1/0/2: UNTRUST, ' + p.wan + '/29', b.zone === 'UNTRUST' && b.ip === p.wan + '/29'],
          ['WAN_IP = ' + p.wan, og('WAN_IP', p.wan)], ['SERVER_IP = ' + p.srv, og('SERVER_IP', p.srv)],
          [p.og + ': port ' + p.port, og(p.og, String(p.port))], ['ruleset DNAT: from zone UNTRUST', RS.from === 'UNTRUST'],
          ['rule: WAN_IP, tcp, ' + p.og + ' → SERVER_POOL, enable', enabledRule(RS.rules, function (r) {
            return r.match['destination-address'] === 'WAN_IP' && r.match.protocol === 'tcp' && r.match['destination-port'] === p.og &&
              r.action === 'destination-nat pool SERVER_POOL'; })],
          ['UNTRUST → TRUST: SERVER_IP, destination-nat, permit, enable', enabledRule(Z, function (r) {
            return r.match['destination-address'] === 'SERVER_IP' && r.match.dnat && r.action === 'permit'; })]]; },
      send: function (p, st) { var c = this.checks(p, st), bad = c.filter(function (x) { return !x[1]; });
        var head = 'Интернет 203.0.113.2 → ' + p.wan + ':' + p.port + ' (tcp)';
        if (bad.length) return [head, '✗ запрос отброшен: ' + bad[0][0]];
        var P = st.dnat.pools.SERVER_POOL;
        return [head, 'DNAT: назначение ' + p.wan + ':' + p.port + ' → SERVER_POOL' + (P && P.ip ? ' (' + P.ip + ')' : ''),
          'UNTRUST → TRUST: match destination-nat, permit', '✓ запрос доставлен серверу ' + p.srv]; } },
    { // 5. NTP (pptx 43–44)
      gen: function () { return { srv: '192.0.2.' + pick([1, 2, 5]), mp: R(4, 6) }; },
      text: function (p) { return 'Включите синхронизацию времени по <b>NTP</b>, укажите сервер <b>' + p.srv +
        '</b>, сделайте его предпочтительным (<b>prefer</b>) и задайте <b>minpoll ' + p.mp + '</b>.'; },
      sol: function (p) { return ['configure', 'ntp enable', 'ntp server ' + p.srv, 'prefer', 'minpoll ' + p.mp, 'exit']; },
      checks: function (p, st) { var S = st.ntp.servers[p.srv] || {};
        return [['ntp enable', st.ntp.on], ['ntp server ' + p.srv, !!st.ntp.servers[p.srv]], ['prefer', !!S.prefer], ['minpoll ' + p.mp, S.minpoll === p.mp]]; },
      send: function (p, st) { var S = st.ntp.servers[p.srv];
        if (!st.ntp.on) return ['✗ синхронизация выключена (ntp enable)'];
        if (!S) return ['✗ NTP-сервер ' + p.srv + ' не задан'];
        return ['ESR → NTP-запрос ' + p.srv + ' (minpoll ' + S.minpoll + ')', p.srv + ' → время',
          '✓ Clock is synchronized' + (S.prefer ? ', reference is ' + p.srv : '')]; } }
  ];

  // ------------------------------------------------------------------ UI
  function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function init(box) {
    var pool = box.dataset.pool.split(',').map(Number), out = box.querySelector('.cs-out'), inp = box.querySelector('input'),
      pr = box.querySelector('.cs-pr'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol');
    var S = { st: fresh(), t: null, p: null, hist: [], hi: 0 };
    function print(s, cls) { var d = document.createElement('div'); d.className = cls || ''; d.textContent = s; out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function upd() { pr.textContent = prompt(S.st) + ' '; }
    function task(keep) {
      S.t = TASKS[pick(pool)]; S.p = S.t.gen(); S.st = fresh(); out.innerHTML = ''; res.innerHTML = ''; sol.style.display = 'none';
      box.querySelector('.cs-task').innerHTML = S.t.text(S.p);
      print('Eltex ESR · консоль. Режим privileged EXEC.', 'cs-sys'); upd();
    }
    inp.addEventListener('keydown', function (e) {
      e.stopPropagation();
      if (e.key === 'ArrowUp') { if (S.hi > 0) inp.value = S.hist[--S.hi]; e.preventDefault(); return; }
      if (e.key === 'ArrowDown') { inp.value = S.hi < S.hist.length - 1 ? S.hist[++S.hi] : (S.hi = S.hist.length, ''); e.preventDefault(); return; }
      if (e.key !== 'Enter') return;
      var v = inp.value; inp.value = ''; if (v.trim()) { S.hist.push(v); S.hi = S.hist.length; }
      print(prompt(S.st) + ' ' + v, 'cs-cmd');
      var r = run(S.st, v.replace(/^\s*ESR[^#]*#\s*/i, ''));
      if (r) print(r, /^%/.test(r) ? 'cs-err' : '');
      upd();
    });
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cs]'); if (!b) { if (e.target.closest('.cs-term')) inp.focus(); return; }
      var a = b.dataset.cs;
      if (a === 'new') task();
      if (a === 'sol') { sol.textContent = S.t.sol(S.p).map(function (l) { return l; }).join('\n'); sol.style.display = sol.style.display === 'none' ? 'block' : 'none'; }
      if (a === 'check') { var c = S.t.checks(S.p, S.st), ok = c.filter(function (x) { return x[1]; }).length;
        res.innerHTML = c.map(function (x) { return '<div class="' + (x[1] ? 'ok' : 'no') + '">' + (x[1] ? '✓ ' : '✗ ') + esc(x[0]) + '</div>'; }).join('') +
          '<div class="cs-sum ' + (ok === c.length ? 'ok' : 'no') + '">' + (ok === c.length ? '✓ Задание выполнено' : 'Выполнено ' + ok + ' из ' + c.length) + '</div>'; }
      if (a === 'send') { res.innerHTML = '<div class="cs-send">' + S.t.send(S.p, S.st).map(function (l) {
        return '<div class="' + (/✗/.test(l) ? 'no' : /✓/.test(l) ? 'ok' : '') + '"><span class="env">✉</span> ' + esc(l) + '</div>'; }).join('') + '</div>'; }
    });
    task();
  }
  function boot() { Array.prototype.forEach.call(document.querySelectorAll('.clisim6'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
  window.I6CLI = { fresh: fresh, run: run, TASKS: TASKS };
})();
