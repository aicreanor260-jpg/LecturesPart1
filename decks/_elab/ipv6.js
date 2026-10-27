/* IPv6: адресация, Neighbor Discovery, статическая маршрутизация, ping (справочник ESR-Series CLI 1.23: ipv6 address, ipv6 enable,
   ipv6 route, show ipv6 interfaces | route | neighbors; VPCS: ip X::Y/64 [шлюз], show ipv6; Debian: ip -6 addr | route | neigh, ping -6).
   Link-local адрес — fe80::/64 из MAC (EUI-64). Разрешение адреса — Neighbor Solicitation на solicited-node multicast ff02::1:ffXX:XXXX
   (MAC 33:33:ff:XX:XX:XX), ответ — Neighbor Advertisement. Коммутаторы MES передают IPv6-кадры как обычные (L2).
   Упрощения: межсетевой экран ESR к IPv6 не применяется, RA/SLAAC и DHCPv6 нет, записи ND не стареют. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, H = EL.hosts;

  // ================================================================ адреса
  function parse(s) {
    s = String(s || '').toLowerCase(); if (!/^[0-9a-f:]+$/.test(s) || s.indexOf(':::') >= 0) return null;
    var dc = s.split('::'); if (dc.length > 2) return null;
    var a = dc[0] ? dc[0].split(':') : [], b = dc.length === 2 && dc[1] ? dc[1].split(':') : [];
    if (dc.length === 1 && a.length !== 8) return null;
    if (dc.length === 2 && a.length + b.length > 7) return null;
    var g = a.concat(new Array(8 - a.length - b.length).fill('0'), b), n = BigInt(0);
    for (var i = 0; i < 8; i++) { if (!/^[0-9a-f]{1,4}$/.test(g[i])) return null; n = (n << BigInt(16)) + BigInt(parseInt(g[i], 16)); }
    return n;
  }
  function fmt(n) {
    var g = []; for (var i = 7; i >= 0; i--) g.push(Number((n >> BigInt(i * 16)) & BigInt(0xffff)).toString(16));
    var bs = -1, bl = 0;
    for (var j = 0; j < 8;) { if (g[j] !== '0') { j++; continue; } var k = j; while (k < 8 && g[k] === '0') k++; if (k - j > bl && k - j >= 2) { bs = j; bl = k - j; } j = k; }
    if (bs < 0) return g.join(':');
    return g.slice(0, bs).join(':') + '::' + g.slice(bs + bl).join(':');
  }
  function mask(len) { return len === 0 ? BigInt(0) : ((BigInt(1) << BigInt(128)) - BigInt(1)) ^ ((BigInt(1) << BigInt(128 - len)) - BigInt(1)); }
  function cidr(s) { var m = String(s).match(/^([0-9a-fA-F:]+)\/(\d{1,3})$/); if (!m || +m[2] > 128 || +m[2] < 1) return null;
    var n = parse(m[1]); return n === null ? null : { ip: fmt(n), len: +m[2], n: n }; }
  function same(a, b, len) { var x = parse(a), y = parse(b); return x !== null && y !== null && (x & mask(len)) === (y & mask(len)); }
  function netOf(ip, len) { return fmt(parse(ip) & mask(len)) + '/' + len; }
  function eui64(mac) { var b = mac.split(':').map(function (x) { return parseInt(x, 16); }); b[0] ^= 2;
    var h = [b[0] << 8 | b[1], b[2] << 8 | 0xff, 0xfe << 8 | b[3], b[4] << 8 | b[5]].map(function (x) { return x.toString(16); });
    return fmt(parse('fe80::' + h.join(':'))); }
  function snm(ip) { var n = parse(ip) & BigInt(0xffffff); return fmt(parse('ff02::1:ff00:0') | n); }
  function mmac(ip) { var n = Number(parse(ip) & BigInt(0xffffff)), p = function (x) { return ('0' + x.toString(16)).slice(-2); };
    return '33:33:ff:' + p(n >> 16) + ':' + p((n >> 8) & 255) + ':' + p(n & 255); }
  function isLL(ip) { var n = parse(ip); return n !== null && (n >> BigInt(118)) === BigInt(0x3fa); }
  EL.ip6 = { parse: parse, fmt: fmt, cidr: cidr, same: same, netOf: netOf, eui64: eui64, snm: snm, mmac: mmac, isLL: isLL, norm: function (s) { var n = parse(s); return n === null ? null : fmt(n); } };

  // ================================================================ интерфейсы, маршруты, ND
  P.ifaces6 = function (id) {
    var s = this, d = this.devs[id], st = d.st, o = [];
    function add(name, port, tag, list, on) { if (!on && !(list || []).length) return;
      var mac = s.ifMac(id, { name: name, port: port });
      o.push({ name: name, ip: eui64(mac), len: 64, ll: true, port: port, tag: tag });
      (list || []).forEach(function (c) { var x = cidr(c); if (x) o.push({ name: name, ip: x.ip, len: x.len, port: port, tag: tag }); }); }
    if (d.off) return o;
    if (d.type === 'vpc') add('eth0', 'eth0', null, st.ip6 ? [st.ip6] : [], true);
    if (d.type === 'deb' && st.up) add('ens3', 'ens3', null, st.ip6 || [], true);
    if (d.type === 'esr') Object.keys(st.run.ifs).forEach(function (k) {
      var x = st.run.ifs[k]; if (x.shut || x.sw) return;
      var ph = k.split('.')[0], lo = k.charAt(0) === 'l'; if (!lo && (st.run.ifs[ph].shut || !s.linkUp(id, ph))) return;
      add(k, lo ? null : ph, k.indexOf('.') > 0 ? +k.split('.')[1] : null, x.ip6, x.v6); });
    return o;
  };
  P.owns6 = function (id, ip) { return this.ifaces6(id).some(function (f) { return f.ip === ip; }); };
  P.routes6 = function (id) {
    var d = this.devs[id], st = d.st, fs = this.ifaces6(id), o = [];
    fs.forEach(function (f) { if (!f.ll) o.push({ p: 'C', net: netOf(f.ip, f.len), len: f.len, nh: null, ifn: f.name }); });
    var stat = d.type === 'esr' ? st.run.routes6 || [] : st.gw6 ? [{ net: '::/0', nh: st.gw6 }] : [];
    stat.forEach(function (r) { var c = r.net === '::/0' ? { ip: '::', len: 0 } : cidr(r.net), out = fs.filter(function (f) { return !f.ll && f.port !== null && same(r.nh, f.ip, f.len); })[0];
      if (!out && isLL(r.nh)) out = fs.filter(function (f) { return f.ll && f.port !== null && (!r.ifn || f.name === r.ifn); })[0];
      if (c) o.push({ p: 'S', net: netOf(c.ip, c.len), len: c.len, nh: r.nh, ifn: out ? out.name : null, ad: r.m === undefined ? 1 : r.m, dead: !out }); });
    return o;
  };
  P.lookup6 = function (id, dst) {
    var fs = this.ifaces6(id), best = null;
    if (isLL(dst)) { var l = fs.filter(function (f) { return f.ll && f.port !== null; })[0]; return l ? { iface: l, nh: dst } : null; }
    this.routes6(id).forEach(function (r) { if (r.dead || !same(dst, r.net.split('/')[0], r.len)) return; if (!best || r.len > best.len) best = r; });
    if (!best) return null;
    var out = fs.filter(function (f) { return f.name === best.ifn && (!f.ll || isLL(best.nh || '')); })[0] || fs.filter(function (f) { return f.name === best.ifn; })[0];
    return out ? { iface: out, nh: best.nh || dst, r: best } : null;
  };
  // заметки flood про IPv4-адреса к IPv6 не относятся
  function n6(L) { return (L || []).filter(function (x) { return !/IP-адрес/.test(x); }); }
  function nd(s, id) { var t = (s.nd = s.nd || {}); return t[id] || (t[id] = {}); }
  P.ndTable = function (id) { return nd(this, id); };
  function srcFor(s, id, ifn, dst) { var fs = s.ifaces6(id).filter(function (f) { return f.name === ifn; });
    return (isLL(dst) ? fs.filter(function (f) { return f.ll; })[0] : fs.filter(function (f) { return !f.ll; })[0] || fs[0]) || {}; }

  // ================================================================ отправка IPv6-пакета в одну сторону
  P.send6 = function (src, pk, steps, ct) {
    ct = ct || []; if (this.devs[src].type === 'esr') ct.push({ kind: 'fw6', dev: src, a: [], b: [pk.dst], self: true });
    var cur = src, hops = [], ttl = 16;
    while (ttl-- > 0) {
      var cd = this.devs[cur];
      if (this.owns6(cur, pk.dst)) return { ok: true, dev: cur, pk: pk, hops: hops };
      var r = this.lookup6(cur, pk.dst);
      if (!r) { steps.push({ k: 'drop', t: cd.name + ': нет IPv6-маршрута до ' + pk.dst + (cd.type !== 'esr' ? ' (не задан шлюз или адрес IPv6)' : '') });
        return { ok: false, why: 'Network is unreachable', pk: pk }; }
      if (!pk.src) pk.src = srcFor(this, cur, r.iface.name, pk.dst).ip || r.iface.ip;
      var srcMac = this.ifMac(cur, r.iface), fl = this.flood(cur, r.iface, srcMac), s = this, nh = r.nh;
      var ll = srcFor(this, cur, r.iface.name, 'fe80::1').ip || pk.src;
      var ep = fl.reach.filter(function (e) { return s.ifaces6(e.dev).some(function (f) { return f.ip === nh && f.port === e.port && f.tag === e.tag; }); })[0];
      var dmac = ep ? this.ifMac(ep.dev, { name: ep.tag !== null ? ep.port + '.' + ep.tag : ep.port, port: ep.port }) : null, cached = nd(this, cur)[nh];
      if (fl.storm) { steps.push({ k: 'drop', segs: fl.segs, t: 'Широковещательный шторм: петля без STP — Neighbor Solicitation размножается', notes: n6(fl.notes) }); return { ok: false, why: 'Request timed out', pk: pk }; }
      if (cached && cached.mac === dmac) steps.push({ k: 'route', t: cd.name + ': ' + nh + ' уже есть в таблице соседей (' + cached.mac + ') — Neighbor Solicitation не нужен' });
      else {
        steps.push({ k: 'arp', segs: fl.segs, notes: n6(fl.notes), t: cd.name + ' (' + r.iface.name + ', ' + srcMac + '): Neighbor Solicitation «кто ' + nh + '?» на ' + snm(nh) +
          ' (multicast ' + mmac(nh) + ')' + (nh !== pk.dst ? ' — это шлюз к ' + pk.dst : ''),
          f: { type: 'ip6', icmp6: 'ns', smac: srcMac, dmac: mmac(nh), src: ll, dst: snm(nh), target: nh, hlim: 255, proto: 'icmp6' } });
        if (!ep) { steps.push({ k: 'drop', t: 'Нет Neighbor Advertisement: ' + nh + ' не найден в этом сегменте (другая VLAN, нет адреса, кабель или порт выключен)', notes: n6(fl.notes) });
          return { ok: false, why: 'Address unreachable', pk: pk }; }
      }
      var nd2 = this.devs[ep.dev], back = ep.path.slice().reverse().map(function (sg) { return { li: sg.li, from: sg.to, to: sg.from, tag: sg.tag, qtag: sg.qtag }; });
      var viol = this.learn(back, dmac);
      if (viol) { steps.push({ k: 'drop', segs: back, t: nd2.name + ': Neighbor Advertisement отброшен — ' + viol }); return { ok: false, why: 'Address unreachable', pk: pk }; }
      var epIf = s.ifaces6(ep.dev).filter(function (f) { return f.ip === nh; })[0];
      nd(this, cur)[nh] = { mac: dmac, ifn: r.iface.name, t: this.now };
      nd(this, ep.dev)[ll] = { mac: srcMac, ifn: epIf.name, t: this.now };
      this.learn(ep.path, srcMac);
      if (!cached || cached.mac !== dmac) steps.push({ k: 'arpr', segs: back, t: nd2.name + ' (' + epIf.name + '): Neighbor Advertisement «' + nh + ' — это я, MAC ' + dmac + '» (unicast)',
        f: { type: 'ip6', icmp6: 'na', smac: dmac, dmac: srcMac, src: nh, dst: ll, target: nh, hlim: 255, proto: 'icmp6' } });
      steps.push({ k: 'ip', segs: ep.path, t: cd.name + ' → ' + nd2.name + ': ICMPv6 ' + pk.src + ' → ' + pk.dst + ' в кадре до MAC ' + dmac,
        f: { type: 'ip6', smac: srcMac, dmac: dmac, src: pk.src, dst: pk.dst, proto: 'icmp6', reply: !!pk.reply, hlim: 64 - hops.length } });
      if (nd2.type === 'esr') { var fw = this.fw6(ep.dev, epIf.name, pk, ct); if (fw.t) steps.push({ k: fw.ok ? 'route' : 'drop', t: fw.t });
        if (!fw.ok) return { ok: false, why: 'Request timed out', pk: pk }; }
      hops.push({ dev: ep.dev, ip: epIf.ip });
      cur = ep.dev;
      if (!this.owns6(cur, pk.dst) && nd2.type !== 'esr') { steps.push({ k: 'drop', t: nd2.name + ' получил чужой пакет и не маршрутизирует его' }); return { ok: false, why: 'Request timed out', pk: pk }; }
      if (!this.owns6(cur, pk.dst)) steps.push({ k: 'route', t: nd2.name + ': адрес ' + pk.dst + ' не мой — ищу IPv6-маршрут дальше' });
    }
    steps.push({ k: 'drop', t: 'Hop Limit истёк — петля маршрутизации' });
    return { ok: false, why: 'Time exceeded', pk: pk };
  };
  P.ping6 = function (src, dst) {
    var steps = this.stepLog(), d = this.devs[src], n = parse(dst);
    if (n === null) return { ok: false, why: 'Bad address', steps: steps };
    dst = fmt(n);
    if (!this.ifaces6(src).length) { steps.push({ k: 'drop', t: d.name + ': IPv6 не включён ни на одном интерфейсе' }); return { ok: false, why: 'No IPv6 address', steps: steps }; }
    var ct = [], f = this.send6(src, { src: null, dst: dst }, steps, ct);
    if (!f.ok) return { ok: false, why: f.why, steps: steps };
    if (f.dev === src) return { ok: true, steps: steps, hops: [] };
    steps.push({ k: 'ok', t: this.devs[f.dev].name + ' получил ICMPv6 Echo Request и отвечает Echo Reply' });
    var b = this.send6(f.dev, { src: dst, dst: f.pk.src, reply: true }, steps, ct);
    if (!b.ok || b.dev !== src) { steps.push({ k: 'drop', t: 'Ответ не вернулся к ' + d.name + ' — проверьте IPv6-маршрут в обратную сторону' }); return { ok: false, why: 'Request timed out', steps: steps }; }
    steps.push({ k: 'ok', t: d.name + ' получил ответ от ' + dst });
    return { ok: true, steps: steps, hops: f.hops, dev: f.dev };
  };
  P.ping6Text = function (id, dst, style) {
    var r = this.ping6(id, dst), o = [], hl = function (i) { return 64 - (r.hops || []).length + 1; };
    if (this.countSteps) this.countSteps(r.steps, 'icmp6');
    if (this.onTrace) this.onTrace(r, id, dst);
    if (r.why === 'Bad address') return style === 'linux' ? 'ping: ' + dst + ': Name or service not known' : style === 'esr' ? 'Syntax error: Illegal parameter' : 'Invalid address';
    dst = fmt(parse(dst));
    if (style === 'vpc') { for (var i = 1; i <= 5; i++) o.push(r.ok ? dst + ' icmp6_seq=' + i + ' ttl=' + hl() + ' time=' + (0.6 + i * 0.11).toFixed(3) + ' ms' : dst + ' icmp6_seq=' + i + ' timeout'); return o.join('\n'); }
    if (style === 'linux') {
      if (r.why === 'No IPv6 address' || r.why === 'Network is unreachable') return 'ping: connect: Network is unreachable';
      o.push('PING ' + dst + '(' + dst + ') 56 data bytes');
      for (var j = 1; j <= 4; j++) if (r.ok) o.push('64 bytes from ' + dst + ': icmp_seq=' + j + ' ttl=' + hl() + ' time=0.' + (640 + j * 31) + ' ms');
      if (!r.ok && /Address unreachable/.test(r.why || '')) o.push('From ' + ((this.ifaces6(id).filter(function (f) { return !f.ll; })[0] || this.ifaces6(id)[0] || {}).ip || dst) + ' icmp_seq=1 Destination unreachable: Address unreachable');
      o.push('', '--- ' + dst + ' ping statistics ---', '4 packets transmitted, ' + (r.ok ? 4 : 0) + ' received, ' + (r.ok ? '0' : '100') + '% packet loss, time 3004ms');
      return o.join('\n');
    }
    o.push('PING ' + dst + '(' + dst + ') 56 data bytes', r.ok ? '!!!!!' : '.....', '--- ' + dst + ' ping statistics ---',
           '5 packets transmitted, ' + (r.ok ? 5 : 0) + ' received, ' + (r.ok ? '0' : '100') + '% packet loss, time 4005ms');
    return o.join('\n');
  };
  // межсетевой экран ESR для IPv6 — те же зоны и zone-pair (протокол icmp6); адресные правила (IPv4 object-group) к IPv6 не подходят
  P.fw6 = function (dev, ifn, pk, ct) {
    var s = this, d = s.devs[dev], c = d.st.run, nm = d.name, x = c.ifs[ifn] || {}, pk2 = { src: pk.src, dst: pk.dst, proto: 'icmp6', dport: null, sport: null };
    if (ct.some(function (e) { return e.kind === 'fw6' && e.dev === dev && e.b.indexOf(pk.src) >= 0 && (e.self || e.a.indexOf(pk.dst) >= 0); }))
      return { ok: true, t: ct.some(function (e) { return e.kind === 'fw6' && e.dev === dev && !e.self; }) ? nm + ': ответ в рамках разрешённой сессии (ICMPv6)' : null };
    if (x.fw === false) return { ok: true };
    var inz = EL.fwZoneOf(c, ifn); if (!inz) return { ok: false, t: nm + ': межсетевой экран на ' + ifn + ' включён и для IPv6, а интерфейс не в зоне — пакет отброшен (security-zone или ip firewall disable)' };
    var outz = 'self';
    if (!s.owns6(dev, pk.dst)) { var r = s.lookup6(dev, pk.dst); if (!r) return { ok: true }; var y = c.ifs[r.iface.name] || {}; if (y.fw === false) return { ok: true };
      outz = EL.fwZoneOf(c, r.iface.name); if (!outz) return { ok: false, t: nm + ': выходной интерфейс ' + r.iface.name + ' не в зоне безопасности — пакет отброшен' }; }
    var pair = (c.zp || {})[inz + '|' + outz]; if (!pair) return { ok: false, t: nm + ': нет security zone-pair ' + inz + ' ' + outz + ' — ICMPv6 ' + pk.src + ' → ' + pk.dst + ' запрещён' };
    var ks = Object.keys(pair.rules).map(Number).sort(function (a, b) { return a - b; });
    for (var i = 0; i < ks.length; i++) { var rl = pair.rules[ks[i]]; if (!rl.on || !rl.act || !EL.fwRuleMatch(c, rl, pk2)) continue;
      if (rl.act !== 'permit') return { ok: false, t: nm + ': zone-pair ' + inz + ' → ' + outz + ', rule ' + ks[i] + ' — ' + rl.act + ' (ICMPv6)' };
      ct.push({ kind: 'fw6', dev: dev, a: [pk.src], b: [pk.dst] });
      return { ok: true, t: nm + ': zone-pair ' + inz + ' → ' + outz + ', rule ' + ks[i] + ' — permit (ICMPv6 ' + pk.src + ' → ' + pk.dst + ')' }; }
    return { ok: false, t: nm + ': zone-pair ' + inz + ' → ' + outz + ' — ни одно правило не подошло для ICMPv6, неявный запрет' };
  };
  var reboot0 = P.reboot; P.reboot = function (id) { var r = reboot0.apply(this, arguments); if (this.nd) delete this.nd[id]; return r; };

  // ================================================================ ESR
  function touch(st) { st.pending = true; }
  function each(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }
  S.cmd('gi sub lo', 'ipv6 address <w>', function (st, a) {
    var L = a[0].split(','), C = L.map(cidr); if (C.some(function (x) { return !x; })) return 'Syntax error: Illegal parameter';
    var bad = null; each(st, function (x) { var cur = (x.ip6 || []).concat(C.map(function (c) { return c.ip + '/' + c.len; })).filter(function (v, i, A) { return A.indexOf(v) === i; });
      if (cur.length > 8) bad = '% Может быть назначено до 8 IPv6-адресов'; else x.ip6 = cur; });
    return bad;
  }, 'IPv6-адрес интерфейса');
  S.cmd('gi sub lo', 'no ipv6 address <w>', function (st, a) { each(st, function (x) {
    if (a[0] === 'all') x.ip6 = []; else { var c = cidr(a[0]); x.ip6 = (x.ip6 || []).filter(function (v) { return !c || v !== c.ip + '/' + c.len; }); } }); });
  S.cmd('gi sub lo', 'ipv6 enable', function (st) { each(st, function (x) { x.v6 = true; }); }, 'Включить IPv6 (link-local)');
  S.cmd('gi sub lo', 'no ipv6 enable', function (st) { each(st, function (x) { x.v6 = false; }); });
  S.cmd('config', 'ipv6 route <w> <w>', function (st, a) { return route6(st, a[0], a[1]); }, 'Статический IPv6-маршрут');
  S.cmd('config', 'ipv6 route <w> <w> <n>', function (st, a) { return route6(st, a[0], a[1], a[2]); });
  S.cmd('config', 'no ipv6 route <w>', function (st, a) { var c = a[0] === '::/0' ? { ip: '::', len: 0 } : cidr(a[0]);
    st.cand.routes6 = (st.cand.routes6 || []).filter(function (r) { return !c || r.net !== c.ip + '/' + c.len; }); touch(st); });
  function route6(st, net, nh, m) {
    var c = net === '::/0' ? { ip: '::', len: 0 } : /\//.test(net) ? cidr(net) : cidr(net + '/128'), h = parse(nh);
    if (!c || h === null || (m !== undefined && m > 255)) return 'Syntax error: Illegal parameter';
    var R = st.cand.routes6 = (st.cand.routes6 || []).filter(function (r) { return r.net !== c.ip + '/' + c.len; });
    R.push({ net: c.ip + '/' + c.len, nh: fmt(h), m: m }); touch(st);
  }
  function ifs6Text(st) { var s = st.net; if (!s) return '';
    var o = ['IPv6 address                                          Interface       Type', '---------------------------------------------------   -------------   -------'];
    s.ifaces6(st.dev).forEach(function (f) { o.push(rp(f.ip + '/' + f.len, 54) + rp(f.name, 16) + 'static'); });
    return o.join('\n'); }
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function route6Text(st) { var s = st.net; if (!s) return '';
    var o = [' Codes: C – connected, S – static, R – RIP derived,', '        O – OSPF derived, IA – OSPF inter area route,', '        E1 – OSPF external type 1 route, E2 – OSPF external type 2 route',
      '        B – BGP derived, D – DHCP derived, K – kernel route,', '        * – FIB route', ''];
    s.routes6(st.dev).filter(function (r) { return !r.dead; }).sort(function (a, b) { return a.net < b.net ? -1 : 1; }).forEach(function (r) {
      o.push(rp(r.p, 6) + '* ' + rp(r.net, 18) + rp('[' + (r.p === 'C' ? '0/0' : r.ad + '/' + (r.m || 0)) + ']', 9) + rp(r.nh ? 'via ' + r.nh + ' on ' + r.ifn : 'dev ' + r.ifn, 34) + ' ' +
        '[' + ({ C: 'direct', R: 'rip', O: 'ospf', B: 'bgp' }[r.p] || 'static') + ' 00:00:00]'); });
    return o.join('\n'); }
  function nd6Text(st) { var s = st.net; if (!s) return ''; var t = nd(s, st.dev);
    var o = ['Interface         IPv6 address                MAC address         State             Age(min)', '---------------   -------------------------   -----------------   ---------------   ----------'];
    Object.keys(t).forEach(function (ip) { var e = t[ip]; o.push(rp(e.ifn, 18) + rp(ip, 28) + rp(e.mac, 20) + rp(s.now - e.t < 30 ? 'reachable' : 'stale', 18) + Math.floor((s.now - e.t) / 60)); });
    return o.join('\n'); }
  S.cmd('priv', 'show ipv6 interfaces', ifs6Text, 'IPv6-интерфейсы');
  S.cmd('priv', 'show ipv6 route', route6Text, 'Таблица IPv6-маршрутов');
  S.cmd('priv', 'show ipv6 neighbors', nd6Text, 'Таблица соседей IPv6 (ND)');
  S.cmd('priv', 'clear ipv6 neighbors', function (st) { if (st.net && st.net.nd) st.net.nd[st.dev] = {}; }, 'Очистить таблицу соседей');
  S.cmd('priv', 'ping <w>', function (st, a) { return st.net && parse(a[0]) !== null ? st.net.ping6Text(st.dev, a[0], 'esr') : 'Syntax error: Illegal parameter'; });
  S.RUNX.push(function (c, o) {
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k], d = [];
      if (x.v6) d.push('  ipv6 enable'); if (x.ip6 && x.ip6.length) d.push('  ipv6 address ' + x.ip6.join(','));
      if (d.length) o.push('interface ' + S.longIf(k), d.join('\n'), 'exit'); });
    (c.routes6 || []).forEach(function (r) { o.push('ipv6 route ' + r.net + ' ' + r.nh + (r.m !== undefined ? ' ' + r.m : '')); });
  });

  // ================================================================ VPC и Debian
  var vpc0 = H.vpcExec;
  H.vpcExec = function (st, raw) {
    var t = String(raw).trim().split(/\s+/), c = (t[0] || '').toLowerCase();
    if (c === 'ip' && t[1] && t[1].indexOf(':') >= 0) {
      var x = cidr(t[1].indexOf('/') > 0 ? t[1] : t[1] + '/64'); if (!x) return 'Invalid address';
      var gw = t[2] ? parse(t[2]) : null; if (t[2] && gw === null) return 'Invalid gateway';
      st.ip6 = x.ip + '/' + x.len; st.gw6 = gw !== null ? fmt(gw) : null;
      return st.name + ' : ' + x.ip + '/' + x.len + (st.gw6 ? ' gateway ' + st.gw6 : '');
    }
    if (c === 'show' && (t[1] || '').toLowerCase() === 'ipv6') { var fs = st.net ? st.net.ifaces6(st.dev) : [];
      return ['NAME              : ' + st.name, 'LINK-LOCAL SCOPE  : ' + ((fs.filter(function (f) { return f.ll; })[0] || {}).ip || '') + '/64',
        'GLOBAL SCOPE      : ' + (st.ip6 || ''), 'ROUTER LINK-LAYER : ' + (st.gw6 || ''), 'MAC               : ' + EL.mac(st.name + 'eth0')].join('\n'); }
    if (c === 'clear' && (t[1] || '').toLowerCase() === 'ipv6') { st.ip6 = null; st.gw6 = null; return 'IPv6 address/mask and router link-layer address cleared'; }
    if (c === 'ping' && t[1] && t[1].indexOf(':') >= 0) return st.net ? st.net.ping6Text(st.dev, t[1], 'vpc') : '';
    return vpc0.apply(this, arguments);
  };
  var deb0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    var line = String(raw).trim(), t = line.split(/\s+/);
    if (!st.user || st.ssh) return deb0.apply(this, arguments);
    if (st.user !== 'root' && /^ip\s+-6\s+\S+\s+(add|del)/.test(line)) return 'RTNETLINK answers: Operation not permitted';
    var m = line.match(/^ip\s+-6\s+(?:address|addr|a)\s+(add|del)\s+(\S+)\s+dev\s+(\S+)$/);
    if (m) { if (m[3] !== 'ens3') return 'Cannot find device "' + m[3] + '"'; var x = cidr(m[2]); if (!x) return 'Error: inet6 prefix is expected rather than "' + m[2] + '".';
      var L = st.ip6 || [], v = x.ip + '/' + x.len;
      if (m[1] === 'add') { if (L.indexOf(v) >= 0) return 'RTNETLINK answers: File exists'; st.ip6 = L.concat([v]); }
      else { if (L.indexOf(v) < 0) return 'RTNETLINK answers: Cannot assign requested address'; st.ip6 = L.filter(function (y) { return y !== v; }); }
      return ''; }
    m = line.match(/^ip\s+-6\s+(?:route|r)\s+(add|del)\s+(default|::\/0)\s+via\s+(\S+)/);
    if (m) { var g = parse(m[3]); if (g === null) return 'Error: inet6 address is expected rather than "' + m[3] + '".'; st.gw6 = m[1] === 'add' ? fmt(g) : null; return ''; }
    if (/^ip\s+-6\s+(address|addr|a)(\s+show)?$/.test(line)) { var fs = st.net ? st.net.ifaces6(st.dev) : [];
      if (!fs.length) return ''; return ['2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 state UP qlen 1000'].concat(fs.slice().reverse().map(function (f) {
        return '    inet6 ' + f.ip + '/' + f.len + ' scope ' + (f.ll ? 'link' : 'global') + '\n       valid_lft forever preferred_lft forever'; })).join('\n'); }
    if (/^ip\s+-6\s+(route|r)(\s+show)?$/.test(line)) { var rs = st.net ? st.net.routes6(st.dev) : [];
      return rs.filter(function (r) { return !r.dead; }).map(function (r) { return r.p === 'C' ? r.net + ' dev ens3 proto kernel metric 256 pref medium' : 'default via ' + r.nh + ' dev ens3 metric 1024 pref medium'; })
        .concat(st.net && st.net.ifaces6(st.dev).length ? ['fe80::/64 dev ens3 proto kernel metric 256 pref medium'] : []).join('\n'); }
    if (/^ip\s+-6\s+(neigh|neighbour|n)(\s+show)?$/.test(line)) { var T = st.net ? nd(st.net, st.dev) : {};
      return Object.keys(T).map(function (ip) { return ip + ' dev ens3 lladdr ' + T[ip].mac + ' REACHABLE'; }).join('\n'); }
    var p = line.match(/^(ping6|ping)\s+(.*)$/);
    if (p) { var dst = p[2].split(/\s+/).filter(function (x) { return x.indexOf(':') >= 0 && parse(x) !== null; })[0];
      if (dst || p[1] === 'ping6' || /(^|\s)-6(\s|$)/.test(p[2])) { if (!dst) return 'ping: ' + (p[2].split(/\s+/).pop()) + ': Name or service not known';
        return st.net ? st.net.ping6Text(st.dev, dst, 'linux') : ''; } }
    return deb0.apply(this, arguments);
  };
})(typeof window !== 'undefined' ? window : global);
