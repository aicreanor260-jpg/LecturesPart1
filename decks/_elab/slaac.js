/* SLAAC (справочник ESR-Series CLI 1.23): на интерфейсе ESR ipv6 nd prefix <IPV6-ADDR/LEN> <VALID-TIME> <PREFER-TIME> [no-autoconfig],
   ipv6 nd ra lifetime <TIME> — маршрутизатор рассылает Router Advertisement с префиксом. Узлы строят адрес сами: префикс /64 + EUI-64 из MAC,
   шлюз — link-local адрес маршрутизатора. VPC: ip auto (как в VPCS); Debian: адрес появляется при ip link set ens3 up (accept_ra),
   повторить запрос — rdisc6 ens3. В трассе: Router Solicitation (ff02::2) и Router Advertisement (ff02::1).
   Упрощения: время жизни префикса не отсчитывается, DHCPv6 (managed/other-config-flag) не моделируется. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, H = EL.hosts, A = EL.ip6;
  function touch(st) { st.pending = true; }
  function each(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }
  function setP(st, a, noAuto) { var c = A.cidr(a[0]); if (!c || a[1] < 1 || a[2] < 1 || a[2] > a[1]) return 'Syntax error: Illegal parameter';
    each(st, function (x) { x.ndp = { net: A.netOf(c.ip, c.len), valid: a[1], pref: a[2], auto: !noAuto }; }); }
  S.cmd('gi sub', 'ipv6 nd prefix <w> <n> <n>', function (st, a) { return setP(st, a, false); }, 'Префикс в Router Advertisement (SLAAC)');
  S.cmd('gi sub', 'ipv6 nd prefix <w> <n> <n> no-autoconfig', function (st, a) { return setP(st, a, true); });
  S.cmd('gi sub', 'no ipv6 nd prefix', function (st) { each(st, function (x) { delete x.ndp; }); });
  S.cmd('gi sub', 'ipv6 nd ra lifetime <n>', function (st, a) { if (a[0] > 9000) return 'Syntax error: Illegal parameter'; each(st, function (x) { x.raLife = a[0]; }); }, 'Время жизни RA');
  S.cmd('gi sub', 'no ipv6 nd ra lifetime', function (st) { each(st, function (x) { delete x.raLife; }); });
  S.RUNX.push(function (c, o) { Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k], d = [];
    if (x.ndp) d.push('  ipv6 nd prefix ' + x.ndp.net + ' ' + x.ndp.valid + ' ' + x.ndp.pref + (x.ndp.auto ? '' : ' no-autoconfig'));
    if (x.raLife !== undefined) d.push('  ipv6 nd ra lifetime ' + x.raLife);
    if (d.length) o.push('interface ' + S.longIf(k), d.join('\n'), 'exit'); }); });

  // Router Solicitation → Router Advertisement: найти маршрутизатор в сегменте узла
  P.slaac = function (id) {
    var s = this, d = s.devs[id], port = d.type === 'vpc' ? 'eth0' : 'ens3', mac = EL.mac(d.name + port), steps = s.stepLog();
    var ll = A.eui64(mac), fl = s.flood(id, { name: port, port: port, tag: null }, mac), ra = null;
    steps.push({ k: 'arp', segs: fl.segs, t: d.name + ': Router Solicitation на ff02::2 (все маршрутизаторы)',
      f: { type: 'ip6', icmp6: 'rs', mcast: true, smac: mac, dmac: '33:33:00:00:00:02', src: ll, dst: 'ff02::2', hlim: 255, proto: 'icmp6' } });
    fl.reach.some(function (e) { var rd = s.devs[e.dev]; if (rd.type !== 'esr') return false;
      var k = e.tag !== null ? e.port + '.' + e.tag : e.port, x = rd.st.run.ifs[k]; if (!x || !x.ndp || x.shut) return false;
      var rll = s.ifaces6(e.dev).filter(function (f) { return f.ll && f.name === k; })[0]; if (!rll) return false;
      ra = { dev: e.dev, ifn: k, prefix: x.ndp, gw: rll.ip, path: e.path }; return true; });
    if (!ra) { steps.push({ k: 'drop', t: 'Router Advertisement не пришёл: в сегменте нет ESR с ipv6 nd prefix (и включённым IPv6)' }); return { ok: false, steps: steps }; }
    var back = ra.path.slice().reverse().map(function (g) { return { li: g.li, from: g.to, to: g.from, tag: g.tag }; }), rmac = s.ifMac(ra.dev, { name: ra.ifn, port: ra.ifn.split('.')[0] });
    steps.push({ k: 'arpr', segs: back, t: s.devs[ra.dev].name + ' (' + ra.ifn + '): Router Advertisement — префикс ' + ra.prefix.net + (ra.prefix.auto ? '' : ' (no-autoconfig)') + ', шлюз ' + ra.gw,
      f: { type: 'ip6', icmp6: 'ra', mcast: true, smac: rmac, dmac: '33:33:00:00:00:01', src: ra.gw, dst: 'ff02::1', hlim: 255, proto: 'icmp6', prefix: ra.prefix.net } });
    if (!ra.prefix.auto || +ra.prefix.net.split('/')[1] !== 64) { steps.push({ k: 'drop', t: 'Адрес не построен: префикс ' + (ra.prefix.auto ? 'не /64' : 'с no-autoconfig') + '; шлюз ' + ra.gw + ' принят' });
      return { ok: false, steps: steps, gw: ra.gw, prefix: ra.prefix.net }; }
    var host = A.parse(ll) & ((BigInt(1) << BigInt(64)) - BigInt(1)), addr = A.fmt(A.parse(ra.prefix.net.split('/')[0]) | host);
    steps.push({ k: 'ok', t: d.name + ': адрес ' + addr + '/64 (префикс + EUI-64 из MAC), шлюз ' + ra.gw });
    if (s.countSteps) s.countSteps(steps, 'icmp6');
    return { ok: true, steps: steps, addr: addr + '/64', gw: ra.gw, prefix: ra.prefix.net };
  };
  var vpc0 = H.vpcExec;
  H.vpcExec = function (st, raw) {
    var t = String(raw).trim().split(/\s+/);
    if ((t[0] || '').toLowerCase() === 'ip' && (t[1] || '').toLowerCase() === 'auto' && st.net) {
      var r = st.net.slaac(st.dev); if (st.net.onTrace) st.net.onTrace(r, st.dev, 'SLAAC');
      if (!r.ok) return 'No router answered ICMPv6 Router Solicitation';
      st.ip6 = r.addr; st.gw6 = r.gw; return 'GLOBAL SCOPE      : ' + r.addr + '\nROUTER LINK-LAYER : ' + r.gw; }
    return vpc0.apply(this, arguments);
  };
  var deb0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    var line = String(raw).trim(), wasUp = st.up;
    if (st.user && !st.ssh && st.net && /^rdisc6\s+ens3$/.test(line)) { var r = st.net.slaac(st.dev); if (st.net.onTrace) st.net.onTrace(r, st.dev, 'SLAAC');
      if (!r.gw) return 'Soliciting ff02::2 (ff02::2) on ens3...\nTimed out.\nNo response.';
      if (r.ok) { st.ip6 = (st.ip6 || []).filter(function (x) { return x !== r.addr; }).concat([r.addr]); st.gw6 = r.gw; st.net.gen++; }
      return 'Soliciting ff02::2 (ff02::2) on ens3...\n\nHop limit                 :           64\nPrefix                    : ' + (r.prefix || '-') + '\n from ' + r.gw; }
    var out = deb0.apply(this, arguments);
    if (st.net && !wasUp && st.up && /^ip\s+link\s+set\s+(dev\s+)?ens3\s+up$/.test(line)) {   // accept_ra: адрес из RA при поднятии интерфейса
      if (!raAddr(st)) st.rsPend = { n: 2, at: st.net.now + 4 }; }   // Linux: ещё 2 Router Solicitation через 4 с (порт коммутатора мог быть не в forwarding)
    return out;
  };
  function raAddr(st) { var q = st.net.slaac(st.dev); if (!q.ok) return false;
    st.ip6 = (st.ip6 || []).filter(function (x) { return x !== q.addr; }).concat([q.addr]); st.gw6 = st.gw6 || q.gw; st.net.gen++; return true; }
  var tick0 = P.tick;
  P.tick = function (dt) {                     // часы идут до момента очередного RS, затем дальше
    var s = this, end = this.now + dt, gone = [];
    for (;;) {
      var due = this.order.map(function (id) { return s.devs[id]; }).filter(function (d) { var p = d.st && d.st.rsPend; return p && p.at <= end; })
        .sort(function (a, b) { return a.st.rsPend.at - b.st.rsPend.at; })[0];
      if (!due) break;
      var st = due.st, p = st.rsPend; gone = gone.concat(tick0.call(this, Math.max(0, p.at - this.now)));
      if (!st.up || raAddr(st) || !--p.n) delete st.rsPend; else p.at += 4;
    }
    return gone.concat(tick0.call(this, end - this.now));
  };
})(typeof window !== 'undefined' ? window : global);
