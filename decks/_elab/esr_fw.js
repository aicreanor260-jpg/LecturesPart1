/* Межсетевой экран ESR по зонам (справочник ESR-Series CLI 1.23):
     security zone NAME · security-zone NAME на интерфейсе · security zone-pair FROM TO (TO может быть self)
     rule N → action permit|deny|reject · match [not] protocol|source-address|destination-address|source-port|destination-port · enable
     object-group network NAME → ip prefix A/L · ip address-range A-B;  object-group service NAME → port-range 22,80-81
   Поведение: пакет на интерфейс с включённым firewall проходит, только если подошло правило permit в паре
   «зона входа → зона выхода» (или self для пакетов самому маршрутизатору); ответы разрешённой сессии проходят сами (stateful).
   Без зоны на интерфейсе и без ip firewall disable пакет отбрасывается. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, S = EL.esr, cmd = S.cmd, P = EL.Net.prototype;
  // таймауты сессий по справочнику ESR (ip firewall sessions …-timeout), секунды
  var TO = { 'generic': 60, 'icmp': 30, 'tcp-connect': 60, 'tcp-disconnect': 30, 'tcp-estabilished': 120, 'tcp-latecome': 120, 'udp-assured': 180, 'udp-wait': 30 };
  // состояние сессии → какой таймаут к нему применяется
  var STATE_TO = { ICMP: 'icmp', SYN_SENT: 'tcp-connect', ESTABLISHED: 'tcp-estabilished', TIME_WAIT: 'tcp-disconnect', UNREPLIED: 'udp-wait', ASSURED: 'udp-assured', GENERIC: 'generic' };
  var KEEP_OPEN = [22, 23];                    // SSH и Telnet остаются открытыми; остальные TCP-обмены (HTTP) закрываются после ответа
  function toVal(c, k) { return ((c && c.fwto) || {})[k] || TO[k]; }
  function sessTtl(net, dev, x) { return toVal(net.devs[dev].st.run, STATE_TO[x.state] || 'generic') - (net.now - x.t); }
  function firstState(proto) { return proto === 'icmp' ? 'ICMP' : proto === 'tcp' ? 'SYN_SENT' : proto === 'udp' ? 'UNREPLIED' : 'GENERIC'; }
  function replyState(x) { return x.proto === 'tcp' ? (KEEP_OPEN.indexOf(x.dport) >= 0 ? 'ESTABLISHED' : 'TIME_WAIT') : x.proto === 'udp' ? 'ASSURED' : x.state; }

  function touch(st) { st.pending = true; }
  var M = { zone: '(config-zone)#', zpair: '(config-zone-pair)#', zrule: '(config-zone-pair-rule)#',
            ogn: '(config-object-group-network)#', ogs: '(config-object-group-service)#' };
  Object.keys(M).forEach(function (k) { S.PROMPT[k] = M[k]; });
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes = c.modes.concat(Object.keys(M)); });
  cmd('zone zpair ogn ogs', 'exit', function (st) { st.mode = 'config'; st.ctx = null; }, 'Выход на уровень выше');
  cmd('zrule', 'exit', function (st) { st.mode = 'zpair'; st.ctx = st.zpKey; }, 'Выход на уровень выше');

  // ================================================================ object-group
  function og(c) { c.og = c.og || { net: {}, svc: {} }; return c.og; }
  function range(s) {
    var m = String(s).match(/^(\d+\.\d+\.\d+\.\d+)(?:-(\d+\.\d+\.\d+\.\d+))?$/);
    if (m && IP.ip2n(m[1]) !== null && (!m[2] || IP.ip2n(m[2]) !== null)) return [m[1], m[2] || m[1]];
    return null;
  }
  function prefix(s) { var c = IP.parseCidr(s); if (!c) return null; var n = IP.ip2n(c.ip) & IP.maskN(c.len);
    return [IP.n2ip(n >>> 0), IP.n2ip((n | ~IP.maskN(c.len)) >>> 0)]; }
  function ports(s) {
    var out = [], ok = String(s).split(',').every(function (p) { var m = p.trim().match(/^(\d+)(?:-(\d+))?$/); if (!m) return false;
      var a = +m[1], b = +(m[2] || m[1]); if (a < 1 || b > 65535 || b < a) return false; out.push([a, b]); return true; });
    return ok && out.length ? out : null;
  }
  cmd('config', 'object-group network <w>', function (st, a) { var g = og(st.cand).net; g[a[0]] = g[a[0]] || { items: [] };
    st.mode = 'ogn'; st.ctx = st.ogName = a[0]; touch(st); }, 'Группа IP-адресов');
  cmd('config', 'object-group service <w>', function (st, a) { var g = og(st.cand).svc; g[a[0]] = g[a[0]] || { items: [] };
    st.mode = 'ogs'; st.ctx = st.ogName = a[0]; touch(st); }, 'Группа TCP/UDP-портов');
  cmd('config', 'no object-group network <w>', function (st, a) { delete og(st.cand).net[a[0]]; touch(st); });
  cmd('config', 'no object-group service <w>', function (st, a) { delete og(st.cand).svc[a[0]]; touch(st); });
  function curNet(st) { return og(st.cand).net[st.ogName]; }
  function curSvc(st) { return og(st.cand).svc[st.ogName]; }
  function addItem(g, r, txt) { if (!g.items.some(function (x) { return x[0] === r[0] && x[1] === r[1]; })) g.items.push([r[0], r[1], txt]); }
  cmd('ogn', 'ip prefix <w>', function (st, a) { var r = prefix(a[0]); if (!r) return '% Формат: ip prefix A.B.C.D/длина';
    addItem(curNet(st), r, 'ip prefix ' + a[0]); touch(st); }, 'Подсеть');
  cmd('ogn', 'ip address-range <w>', function (st, a) { var r = range(a[0]); if (!r) return '% Формат: ip address-range A.B.C.D[-A.B.C.D]';
    if (IP.ip2n(r[0]) > IP.ip2n(r[1])) return '% Начало диапазона больше конца'; addItem(curNet(st), r, 'ip address-range ' + a[0]); touch(st); }, 'Диапазон адресов');
  cmd('ogn', 'no ip prefix <w>', function (st, a) { var g = curNet(st); g.items = g.items.filter(function (x) { return x[2] !== 'ip prefix ' + a[0]; }); touch(st); });
  cmd('ogn', 'no ip address-range <w>', function (st, a) { var g = curNet(st); g.items = g.items.filter(function (x) { return x[2] !== 'ip address-range ' + a[0]; }); touch(st); });
  cmd('ogs', 'port-range <w>', function (st, a) { var r = ports(a[0]); if (!r) return '% Формат: port-range 22 | 80,443 | 8000-8080';
    r.forEach(function (x) { addItem(curSvc(st), x, x[0] === x[1] ? '' + x[0] : x.join('-')); }); touch(st); }, 'Порты');
  cmd('ogs', 'no port-range <w>', function (st, a) { var g = curSvc(st);
    g.items = a[0] === 'all' ? [] : g.items.filter(function (x) { return x[2] !== a[0]; }); touch(st); });
  cmd('ogn ogs zone zpair zrule', 'description <rest>', function (st, a) { var o = descTarget(st); if (o) { o.desc = a[0]; touch(st); } }, 'Описание');
  function descTarget(st) {
    if (st.mode === 'ogn') return curNet(st); if (st.mode === 'ogs') return curSvc(st);
    if (st.mode === 'zone') return st.cand.zones[st.zoneName]; if (st.mode === 'zpair') return zp(st); if (st.mode === 'zrule') return zr(st);
  }
  EL.ogNet = function (c, name, ip) {
    var g = c && c.og && c.og.net[name], n = IP.ip2n(ip); if (!g || n === null) return false;
    return g.items.some(function (x) { return n >= IP.ip2n(x[0]) && n <= IP.ip2n(x[1]); });
  };
  EL.ogSvc = function (c, name, port) {
    var g = c && c.og && c.og.svc[name]; if (!g || !port) return false;
    return g.items.some(function (x) { return port >= x[0] && port <= x[1]; });
  };

  // ================================================================ зоны и пары зон
  function zones(c) { return c.zones || (c.zones = {}); }
  function pairs(c) { return c.zp || (c.zp = {}); }
  cmd('config', 'security zone <w>', function (st, a) { if (a[0] === 'self' || a[0] === 'all') return '% Имя ' + a[0] + ' зарезервировано';
    if (a[0].length > 12) return '% Имя зоны — до 12 символов';
    zones(st.cand)[a[0]] = zones(st.cand)[a[0]] || {}; st.mode = 'zone'; st.ctx = st.zoneName = a[0]; touch(st); }, 'Зона безопасности');
  cmd('config', 'no security zone <w>', function (st, a) {
    var used = Object.keys(st.cand.ifs).filter(function (k) { return st.cand.ifs[k].zone === a[0]; });
    if (used.length) return '% Зона используется на ' + used.join(', ') + ' — сначала no security-zone';
    delete zones(st.cand)[a[0]]; touch(st); });
  function setZone(st, z) {
    if (z && !zones(st.cand)[z]) return '% Зона ' + z + ' не создана — security zone ' + z;
    if (st.mode === 'bridge') { var b = st.cand.bridges[st.ctx]; if (z) b.zone = z; else delete b.zone; touch(st); return; }
    (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { var x = st.cand.ifs[k]; if (z) x.zone = z; else delete x.zone; }); touch(st);
  }
  cmd('gi sub bridge', 'security-zone <w>', function (st, a) { return setZone(st, a[0]); }, 'Включить интерфейс в зону безопасности');
  cmd('gi sub bridge', 'no security-zone', function (st) { return setZone(st, null); });

  cmd('config', 'security zone-pair <w> <w>', function (st, a) {
    var Z = zones(st.cand); if (!Z[a[0]]) return '% Зона ' + a[0] + ' не создана'; if (a[1] !== 'self' && !Z[a[1]]) return '% Зона ' + a[1] + ' не создана';
    var k = a[0] + '|' + a[1]; pairs(st.cand)[k] = pairs(st.cand)[k] || { from: a[0], to: a[1], rules: {} };
    st.mode = 'zpair'; st.ctx = st.zpKey = k; touch(st); }, 'Правила для трафика из одной зоны в другую (или self)');
  cmd('config', 'no security zone-pair <w> <w>', function (st, a) { delete pairs(st.cand)[a[0] + '|' + a[1]]; touch(st); });
  function zp(st) { return pairs(st.cand)[st.zpKey]; }
  function zr(st) { return zp(st).rules[st.zrN]; }
  cmd('zpair', 'rule <n>', function (st, a) { if (a[0] < 1 || a[0] > 10000) return '% Номер правила 1..10000';
    var R = zp(st).rules; R[a[0]] = R[a[0]] || { on: false, act: null };
    st.mode = 'zrule'; st.ctx = st.zrN = a[0]; touch(st); }, 'Правило');
  cmd('zpair', 'no rule <n>', function (st, a) { delete zp(st).rules[a[0]]; touch(st); });
  ['permit', 'deny', 'reject'].forEach(function (x) {
    cmd('zrule', 'action ' + x, function (st) { zr(st).act = x; delete zr(st).log; touch(st); }, { permit: 'Разрешить', deny: 'Запретить молча', reject: 'Запретить с уведомлением' }[x]);
    cmd('zrule', 'action ' + x + ' log', function (st) { zr(st).act = x; zr(st).log = true; touch(st); });
  });
  cmd('zrule', 'no action', function (st) { zr(st).act = null; touch(st); });
  cmd('zrule', 'enable', function (st) { if (!zr(st).act) return '% Сначала action permit | deny | reject'; zr(st).on = true; touch(st); }, 'Включить правило');
  cmd('zrule', 'no enable', function (st) { zr(st).on = false; touch(st); });

  // match [not] … — разбор хвоста команды
  var PROTO = ['any', 'icmp', 'icmp6', 'tcp', 'udp', 'gre', 'esp', 'ah', 'ospf', 'vrrp', 'igmp', 'pim'];
  function parseAddr(st, w) {
    var t = w.trim().split(/\s+/), not = t[0] === 'not'; if (not) t.shift();
    var k = t[0], v = t[1], og1 = og(st.cand).net;
    if (k === 'any' && t.length === 1) return { not: not, kind: 'any', txt: 'any' };
    if (k === 'address-range' && range(v)) return { not: not, kind: 'range', r: range(v), txt: 'address-range ' + v };
    if (k === 'prefix' && prefix(v)) return { not: not, kind: 'range', r: prefix(v), txt: 'prefix ' + v };
    if (k === 'object-group' && v) return og1[v] ? { not: not, kind: 'og', v: v, txt: 'object-group ' + v } : '% object-group network ' + v + ' не создан';
    if (t.length === 1 && og1[k]) return { not: not, kind: 'og', v: k, txt: 'object-group ' + k };
    return '% Формат: [not] address-range A.B.C.D-A.B.C.D | prefix A.B.C.D/L | object-group ИМЯ | any';
  }
  function parsePort(st, w) {
    var t = w.trim().split(/\s+/), not = t[0] === 'not'; if (not) t.shift();
    var k = t[0], v = t[1], og1 = og(st.cand).svc;
    if (k === 'any' && t.length === 1) return { not: not, kind: 'any', txt: 'any' };
    if (k === 'port-range' && ports(v)) return { not: not, kind: 'ports', r: ports(v), txt: 'port-range ' + v };
    if (k === 'object-group' && v) return og1[v] ? { not: not, kind: 'og', v: v, txt: 'object-group ' + v } : '% object-group service ' + v + ' не создан';
    if (t.length === 1 && og1[k]) return { not: not, kind: 'og', v: k, txt: 'object-group ' + k };
    return '% Формат: [not] port-range 22,80-81 | object-group ИМЯ | any';
  }
  function setMatch(st, field, val) { if (typeof val === 'string') return val; zr(st)[field] = val; touch(st); }
  cmd('zrule', 'match protocol <w>', function (st, a) { var p = a[0].toLowerCase(); if (PROTO.indexOf(p) < 0) return '% Протокол: ' + PROTO.join(' | ');
    zr(st).proto = { not: false, v: p }; touch(st); }, 'Протокол');
  cmd('zrule', 'match not protocol <w>', function (st, a) { var p = a[0].toLowerCase(); if (PROTO.indexOf(p) < 0) return '% Протокол: ' + PROTO.join(' | ');
    zr(st).proto = { not: true, v: p }; touch(st); });
  cmd('zrule', 'match source-address <rest>', function (st, a) { return setMatch(st, 'src', parseAddr(st, a[0])); }, 'Адрес источника');
  cmd('zrule', 'match destination-address <rest>', function (st, a) { return setMatch(st, 'dst', parseAddr(st, a[0])); }, 'Адрес назначения');
  cmd('zrule', 'match source-port <rest>', function (st, a) { return setMatch(st, 'sport', parsePort(st, a[0])); }, 'Порт источника');
  cmd('zrule', 'match destination-port <rest>', function (st, a) { return setMatch(st, 'dport', parsePort(st, a[0])); }, 'Порт назначения');
  ['protocol', 'source-address', 'destination-address', 'source-port', 'destination-port'].forEach(function (f) {
    var key = { protocol: 'proto', 'source-address': 'src', 'destination-address': 'dst', 'source-port': 'sport', 'destination-port': 'dport' }[f];
    cmd('zrule', 'no match ' + f, function (st) { delete zr(st)[key]; touch(st); });
  });
  // NAT: match source/destination-address с object-group (как в справочнике 1.23)
  function natRule(st) { return st.cand[st.mode.slice(0, 4)].rulesets[st.natRs].rules[st.ctx]; }
  ['source', 'destination'].forEach(function (dir) {
    cmd('snatr dnatr', 'match ' + dir + '-address object-group <w>', function (st, a) {
      if (!og(st.cand).net[a[0]]) return '% object-group network ' + a[0] + ' не создан';
      var r = natRule(st); r[dir === 'source' ? 'srcOg' : 'dstOg'] = a[0]; delete r[dir === 'source' ? 'src' : 'dst']; touch(st); }, 'Группа адресов');
  });
  cmd('snatr dnatr', 'match destination-port object-group <w>', function (st, a) {
    if (!og(st.cand).svc[a[0]]) return '% object-group service ' + a[0] + ' не создан';
    var r = natRule(st); r.dportOg = a[0]; delete r.dport; touch(st); }, 'Группа портов');

  // ================================================================ проверка пакета
  function addrHit(c, m, ip) {
    if (!m || m.kind === 'any') return true;
    var hit = m.kind === 'og' ? EL.ogNet(c, m.v, ip) : IP.ip2n(ip) >= IP.ip2n(m.r[0]) && IP.ip2n(ip) <= IP.ip2n(m.r[1]);
    return m.not ? !hit : hit;
  }
  function portHit(c, m, port) {
    if (!m || m.kind === 'any') return true;
    var hit = !!port && (m.kind === 'og' ? EL.ogSvc(c, m.v, port) : m.r.some(function (x) { return port >= x[0] && port <= x[1]; }));
    return m.not ? !hit : hit;
  }
  EL.fwRuleMatch = function (c, r, pk) { return ruleMatch(c, r, pk); };
  function ruleMatch(c, r, pk) {
    if (r.proto && r.proto.v !== 'any') { var h = r.proto.v === pk.proto; if (r.proto.not ? h : !h) return false; }
    return addrHit(c, r.src, pk.src) && addrHit(c, r.dst, pk.dst) && portHit(c, r.dport, pk.dport) && portHit(c, r.sport, pk.sport);
  }
  EL.fwZoneOf = function (c, ifname) {
    var base = String(ifname).split(':')[0];
    if (base.indexOf('bridge') === 0) return (c.bridges[base.slice(6)] || {}).zone || null;
    return (c.ifs[base] || {}).zone || null;
  };
  function pkTxt(pk) { return (pk.proto === 'icmp' ? 'ICMP' : pk.proto.toUpperCase() + (pk.dport ? ':' + pk.dport : '')) + ' ' + pk.src + ' → ' + pk.dst; }
  // ct — сессии текущего обмена (запрос + ответ); pre — адреса до трансляций на этом маршрутизаторе
  P.fwPass = function (dev, iface, pk, ct, pre) {
    var s = this, d = s.devs[dev], c = d.st.run, nm = d.name, alt = pre || {};
    var est = ct.filter(function (x) { return x.kind === 'fw' && x.dev === dev && x.proto === pk.proto &&
      (x.a.indexOf(pk.dst) >= 0 || x.a.indexOf(alt.dst) >= 0) && (x.b.indexOf(pk.src) >= 0 || x.b.indexOf(alt.src) >= 0); })[0];
    if (est) {
      var why = '';
      if (est.sess) { var old = est.sess.state; est.sess.state = replyState(est.sess); est.sess.t = s.now;
        why = old !== est.sess.state ? ' Состояние сессии ' + old + ' → ' + est.sess.state + ', таймаут ' + toVal(c, STATE_TO[est.sess.state]) + ' с' : ''; }
      return { ok: true, t: est.self ? null : nm + ': ответ в рамках разрешённой сессии — stateful firewall пропускает его без правил.' + why };
    }
    if (!iface.fw) return { ok: true };
    var live = pk.proto === 'udp' && ((s.fwSess || {})[dev] || []).filter(function (x) { return x.proto === 'udp' && x.dport === pk.dport &&
      (x.src === (alt.src || pk.src)) && (x.dst === (alt.dst || pk.dst)) && sessTtl(s, dev, x) > 0; })[0];
    if (live) { live.t = s.now; ct.push({ kind: 'fw', dev: dev, proto: pk.proto, sess: live, a: [pk.src, alt.src].filter(Boolean), b: [pk.dst, alt.dst].filter(Boolean) });
      return { ok: true, t: nm + ': UDP-поток ' + live.src + ' → ' + live.dst + ':' + live.dport + ' уже есть в таблице сессий (' + live.state + ') — правила не проверяются, таймер продлён' }; }
    var inz = EL.fwZoneOf(c, iface.name);
    if (!inz) return { ok: false, t: nm + ': межсетевой экран на ' + iface.name.split(':')[0] + ' включён, а интерфейс не в зоне — пакет отброшен (security-zone ИМЯ или ip firewall disable)' };
    var outz = 'self', own = s.ifaces(dev).some(function (f) { return f.ip === pk.dst; });
    if (!own) {
      var r = s.lookup(dev, pk.dst); if (!r) return { ok: true };            // маршрута нет — отбросит маршрутизация
      if (!r.iface.fw) return { ok: true, t: nm + ': выходной интерфейс ' + r.iface.name + ' с ip firewall disable — проверка зон не нужна' };
      outz = EL.fwZoneOf(c, r.iface.name);
      if (!outz) return { ok: false, t: nm + ': выходной интерфейс ' + r.iface.name + ' не в зоне безопасности — пакет отброшен' };
    }
    var key = inz + '|' + outz, pair = (c.zp || {})[key], cnt = (s.fwCnt = s.fwCnt || {})[dev] || (s.fwCnt[dev] = {});
    if (!pair) return { ok: false, t: nm + ': нет security zone-pair ' + inz + ' ' + outz + ' — трафик между зонами по умолчанию запрещён (' + pkTxt(pk) + ')' };
    var ks = Object.keys(pair.rules).map(Number).sort(function (a, b) { return a - b; });
    for (var i = 0; i < ks.length; i++) {
      var rl = pair.rules[ks[i]]; if (!rl.on || !rl.act || !ruleMatch(c, rl, pk)) continue;
      cnt[key + '|' + ks[i]] = (cnt[key + '|' + ks[i]] || 0) + 1;
      if (rl.act !== 'permit') return { ok: false, t: nm + ': zone-pair ' + inz + ' → ' + outz + ', rule ' + ks[i] + ' — ' + rl.act + ' (' + pkTxt(pk) + ')' };
      var L = (s.fwSess = s.fwSess || {})[dev] || (s.fwSess[dev] = []);
      var rec = { proto: pk.proto, src: alt.src || pk.src, dst: alt.dst || pk.dst, osrc: pk.src, odst: pk.dst, dport: pk.dport, from: inz, to: outz, t: s.now, state: firstState(pk.proto) };
      L.push(rec); if (L.length > 50) L.shift();
      ct.push({ kind: 'fw', dev: dev, proto: pk.proto, sess: rec, a: [pk.src, alt.src].filter(Boolean), b: [pk.dst, alt.dst].filter(Boolean) });
      return { ok: true, t: nm + ': zone-pair ' + inz + ' → ' + outz + ', rule ' + ks[i] + ' — permit (' + pkTxt(pk) + '), новая сессия ' + rec.state +
        ' (таймаут ' + toVal(c, STATE_TO[rec.state]) + ' с)' };
    }
    cnt[key + '|default'] = (cnt[key + '|default'] || 0) + 1;
    return { ok: false, t: nm + ': zone-pair ' + inz + ' → ' + outz + ' — ни одно правило не подошло, неявный запрет (' + pkTxt(pk) + ')' };
  };
  // старение записей о сессиях
  var tick0 = P.tick;
  P.tick = function (dt) { var g = tick0.call(this, dt), s = this;
    Object.keys(s.fwSess || {}).forEach(function (id) { s.fwSess[id] = s.fwSess[id].filter(function (x) { return sessTtl(s, id, x) > 0; }); });
    return g; };

  // ================================================================ таймауты сессий
  Object.keys(TO).forEach(function (k) {
    var pats = [k]; if (k === 'tcp-estabilished') pats.push('tcp-established');   // в CLI ESR команда написана с опечаткой — принимаем оба
    pats.forEach(function (w, i) {
      cmd('config', 'ip firewall sessions ' + w + '-timeout <n>', function (st, a) { if (a[0] < 1 || a[0] > 8553600) return '% Допустимо 1..8553600 с';
        st.cand.fwto = st.cand.fwto || {}; st.cand.fwto[k] = a[0]; touch(st); }, i ? undefined : 'Таймаут сессий, с (по умолчанию ' + TO[k] + ')');
      cmd('config', 'no ip firewall sessions ' + w + '-timeout', function (st) { if (st.cand.fwto) delete st.cand.fwto[k]; touch(st); });
    });
  });
  cmd('priv', 'show ip firewall sessions timeouts', function (st) {
    return ['Timeout                    Value  Default', '-------------------------  -----  -------'].concat(Object.keys(TO).map(function (k) {
      return (k + '-timeout                          ').slice(0, 27) + (toVal(st.run, k) + '       ').slice(0, 7) + TO[k]; })).join('\n'); }, 'Таймауты сессий по протоколам');

  // ================================================================ show
  function zoneText(st) {
    var c = st.run, Z = Object.keys(c.zones || {});
    if (!Z.length) return '% Зоны не созданы — security zone ИМЯ';
    return ['Zone name     Interfaces', '------------  ------------------------------------------'].concat(Z.map(function (z) {
      var ifs = Object.keys(c.ifs).filter(function (k) { return c.ifs[k].zone === z; })
        .concat(Object.keys(c.bridges || {}).filter(function (k) { return c.bridges[k].zone === z; }).map(function (k) { return 'bridge ' + k; }));
      return (z + '              ').slice(0, 14) + (ifs.join(', ') || '--'); })).join('\n');
  }
  function ruleTxt(r) {
    var o = [r.act || '-'];
    if (r.proto) o.push('protocol ' + (r.proto.not ? 'not ' : '') + r.proto.v);
    [['src', 'source-address'], ['dst', 'destination-address'], ['sport', 'source-port'], ['dport', 'destination-port']].forEach(function (f) {
      if (r[f[0]]) o.push(f[1] + ' ' + (r[f[0]].not ? 'not ' : '') + r[f[0]].txt); });
    return o.join(', ') + (r.on ? '' : '  (выключено — нет enable)');
  }
  function pairText(st, a, b) {
    var c = st.run, P2 = c.zp || {}, ks = Object.keys(P2).filter(function (k) { return !a || k === a + '|' + b; });
    if (!ks.length) return a ? '% Пара ' + a + ' → ' + b + ' не создана' : '% Пары зон не созданы — security zone-pair ИЗ В';
    return ks.map(function (k) { var p = P2[k], R = Object.keys(p.rules).map(Number).sort(function (x, y) { return x - y; });
      return 'Zone-pair ' + p.from + ' → ' + p.to + (p.desc ? ' («' + p.desc + '»)' : '') + '\n' +
        (R.length ? R.map(function (n) { return '  rule ' + n + ': ' + ruleTxt(p.rules[n]); }).join('\n') : '  (правил нет — всё запрещено)') +
        '\n  остальное — неявный запрет'; }).join('\n');
  }
  function sessText(st) {
    var L = ((st.net && st.net.fwSess) || {})[st.dev] || [], now = st.net ? st.net.now : 0;
    if (!L.length) return '% Активных сессий нет';
    return ['Prot  Inside source     Inside destination  Outside source    Outside destination  Zones                State        Expire', '----  ----------------  ------------------  ----------------  -------------------  -------------------  -----------  ------']
      .concat(L.map(function (x) { var pad = function (v, n) { return (v + '                      ').slice(0, n); };
        return pad(x.proto, 6) + pad(x.src, 18) + pad(x.dst + (x.dport ? ':' + x.dport : ''), 20) + pad(x.osrc, 18) + pad(x.odst, 21) +
          pad(x.from + '→' + x.to, 21) + pad(x.state, 13) + Math.max(0, Math.ceil(sessTtl(st.net, st.dev, x))); })).join('\n');
  }
  function cntText(st) {
    var C = ((st.net && st.net.fwCnt) || {})[st.dev] || {}, ks = Object.keys(C).sort();
    if (!ks.length) return '% Счётчики пусты — через межсетевой экран ещё ничего не проходило';
    return ['Zone-pair                 Rule      Packets', '------------------------  --------  -------'].concat(ks.map(function (k) { var p = k.split('|');
      return ((p[0] + ' → ' + p[1]) + '                          ').slice(0, 26) + ((p[2] === 'default' ? 'implicit' : p[2]) + '          ').slice(0, 10) + C[k]; })).join('\n');
  }
  function ogText(st, kind, name) {
    var c = st.run, G2 = (c.og || { net: {}, svc: {} }), out = [];
    ['net', 'svc'].forEach(function (t) { if (kind && kind !== t) return;
      Object.keys(G2[t]).forEach(function (n) { if (name && n !== name) return; var g = G2[t][n];
        out.push('object-group ' + (t === 'net' ? 'network' : 'service') + ' ' + n + (g.desc ? '  — ' + g.desc : ''));
        if (t === 'net') g.items.forEach(function (x) { out.push('  ' + x[2]); });
        else if (g.items.length) out.push('  port-range ' + g.items.map(function (x) { return x[2]; }).join(','));
        if (!g.items.length) out.push('  (пусто)'); }); });
    return out.length ? out.join('\n') : '% Групп нет';
  }
  cmd('priv', 'show security zone', zoneText, 'Зоны безопасности и их интерфейсы');
  cmd('priv', 'show security zone-pair', function (st) { return pairText(st); }, 'Пары зон и правила');
  cmd('priv', 'show security zone-pair <w> <w>', function (st, a) { return pairText(st, a[0], a[1]); });
  cmd('priv', 'show security zone-pair configuration <w> <w>', function (st, a) { return pairText(st, a[0], a[1]); });
  cmd('priv', 'show ip firewall sessions', sessText, 'Сессии межсетевого экрана');
  cmd('priv', 'show ip firewall counters', cntText, 'Счётчики правил');
  cmd('priv', 'clear ip firewall sessions', function (st) { if (st.net && st.net.fwSess) st.net.fwSess[st.dev] = []; }, 'Сбросить сессии');
  cmd('priv', 'clear ip firewall counters', function (st) { if (st.net && st.net.fwCnt) st.net.fwCnt[st.dev] = {}; }, 'Сбросить счётчики');
  // что изменится после commit: разница кандидата и применённой конфигурации
  cmd('priv', 'show configuration changes', function (st) {
    var run = S.showRun(st).split('\n'), r0 = st.run; st.run = st.cand; var cand = S.showRun(st).split('\n'); st.run = r0;
    var add = cand.filter(function (l) { return run.indexOf(l) < 0 && l.trim() !== 'exit'; }), del = run.filter(function (l) { return cand.indexOf(l) < 0 && l.trim() !== 'exit'; });
    if (!add.length && !del.length) return '% Изменений нет — кандидат совпадает с применённой конфигурацией';
    return del.map(function (l) { return '- ' + l; }).concat(add.map(function (l) { return '+ ' + l; })).join('\n') + '\n(применить: commit, затем confirm)';
  }, 'Что изменится после commit');
  cmd('priv', 'show object-group', function (st) { return ogText(st); }, 'Группы объектов');
  cmd('priv', 'show object-group network', function (st) { return ogText(st, 'net'); });
  cmd('priv', 'show object-group service', function (st) { return ogText(st, 'svc'); });
  cmd('priv', 'show object-group network <w>', function (st, a) { return ogText(st, 'net', a[0]); });
  cmd('priv', 'show object-group service <w>', function (st, a) { return ogText(st, 'svc', a[0]); });

  // ================================================================ running-config
  S.RUNX.push(function (c, o) {
    var G2 = c.og || { net: {}, svc: {} };
    Object.keys(c.fwto || {}).forEach(function (k) { o.push('ip firewall sessions ' + k + '-timeout ' + c.fwto[k]); });
    Object.keys(G2.net).forEach(function (n) { o.push('object-group network ' + n); if (G2.net[n].desc) o.push('  description "' + G2.net[n].desc + '"');
      G2.net[n].items.forEach(function (x) { o.push('  ' + x[2]); }); o.push('exit'); });
    Object.keys(G2.svc).forEach(function (n) { o.push('object-group service ' + n); if (G2.svc[n].desc) o.push('  description "' + G2.svc[n].desc + '"');
      if (G2.svc[n].items.length) o.push('  port-range ' + G2.svc[n].items.map(function (x) { return x[2]; }).join(',')); o.push('exit'); });
    Object.keys(c.zones || {}).forEach(function (z) { o.push('security zone ' + z); if (c.zones[z].desc) o.push('  description "' + c.zones[z].desc + '"'); o.push('exit'); });
    Object.keys(c.ifs).forEach(function (k) { if (c.ifs[k].zone) o.push('interface ' + S.longIf(k), '  security-zone ' + c.ifs[k].zone, 'exit'); });
    Object.keys(c.bridges || {}).forEach(function (k) { if (c.bridges[k].zone) o.push('bridge ' + k, '  security-zone ' + c.bridges[k].zone, 'exit'); });
    Object.keys(c.zp || {}).forEach(function (k) { var p = c.zp[k]; o.push('security zone-pair ' + p.from + ' ' + p.to);
      Object.keys(p.rules).map(Number).sort(function (a, b) { return a - b; }).forEach(function (n) { var r = p.rules[n]; o.push('  rule ' + n);
        if (r.desc) o.push('    description "' + r.desc + '"');
        if (r.act) o.push('    action ' + r.act + (r.log ? ' log' : ''));
        if (r.proto) o.push('    match ' + (r.proto.not ? 'not ' : '') + 'protocol ' + r.proto.v);
        [['src', 'source-address'], ['dst', 'destination-address'], ['sport', 'source-port'], ['dport', 'destination-port']].forEach(function (f) {
          if (r[f[0]]) o.push('    match ' + (r[f[0]].not ? 'not ' : '') + f[1] + ' ' + r[f[0]].txt); });
        if (r.on) o.push('    enable'); o.push('  exit'); });
      o.push('exit'); });
  });
})(typeof window !== 'undefined' ? window : global);
