/* DHCPv6 и старение ND (справочник ESR-Series CLI 1.23).
   Сервер ESR: ipv6 dhcp-server (включить) · ipv6 dhcp-server pool NAME → (config-ipv6-dhcp-server)#: network X::/len, address-range A-B, dns-server, domain-name,
     default-lease-time DD:HH:MM; на интерфейсе ipv6 nd managed-config-flag / other-config-flag (флаги M/O в RA). show ipv6 dhcp binding.
   Клиент Debian: dhclient -6 [ens3] — Solicit на ff02::1:2 → Advertise → Request → Reply, адрес /128 (шлюз и префикс — из RA/SLAAC).
   ND: ipv6 nd reachable-time 5000..100000000 мс (30000) — в CONFIG и на интерфейсе; запись REACHABLE это время, затем STALE.
   Упрощения: аренда DHCPv6 не отсчитывается (адрес держится, пока клиент включён); DUID — MAC клиента; relay DHCPv6 и prefix delegation не моделируются;
   флаг M в RA только показывается — клиент запрашивает адрес командой dhclient -6. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, A = EL.ip6, H = EL.hosts;
  S.PROMPT.d6 = '(config-ipv6-dhcp-server)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('d6'); });
  function touch(st) { st.pending = true; }
  function cmd(modes, pat, fn, d) { return S.cmd(modes, pat, fn, d); }        // в конец таблицы: «ip dhcp-server …» не должно сокращаться до ipv6
  function bad() { return 'Syntax error: Illegal parameter'; }
  function D(st) { return st.cand.dhcp6 || (st.cand.dhcp6 = { on: false, pools: {} }); }
  function pool(st) { return D(st).pools[st.ctx]; }
  cmd('config', 'ipv6 dhcp-server', function (st) { D(st).on = true; touch(st); }, 'Включить DHCPv6-сервер');
  cmd('config', 'no ipv6 dhcp-server', function (st) { D(st).on = false; touch(st); });
  cmd('config', 'ipv6 dhcp-server pool <w>', function (st, a) { if (!/^[\w.-]{1,31}$/.test(a[0])) return bad(); var P2 = D(st).pools; P2[a[0]] = P2[a[0]] || {};
    st.mode = 'd6'; st.ctx = a[0]; touch(st); }, 'Пул DHCPv6');
  cmd('config', 'no ipv6 dhcp-server pool <w>', function (st, a) { delete D(st).pools[a[0]]; touch(st); });
  cmd('d6', 'network <w>', function (st, a) { var c = A.cidr(a[0]); if (!c) return bad(); pool(st).net = A.netOf(c.ip, c.len); touch(st); }, 'Подсеть пула');
  cmd('d6', 'address-range <w>', function (st, a) { var q = a[0].split('-'); if (q.length !== 2 || A.parse(q[0]) === null || A.parse(q[1]) === null || A.parse(q[0]) > A.parse(q[1])) return bad();
    pool(st).range = [A.fmt(A.parse(q[0])), A.fmt(A.parse(q[1]))]; touch(st); }, 'Диапазон выдаваемых адресов');
  cmd('d6', 'dns-server <w>', function (st, a) { if (A.parse(a[0]) === null) return bad(); pool(st).dns = a[0]; touch(st); }, 'DNS-сервер для клиентов');
  cmd('d6', 'domain-name <w>', function (st, a) { pool(st).dom = a[0]; touch(st); }, 'Домен');
  cmd('d6', 'default-lease-time <w>', function (st, a) { if (!/^\d+:\d+:\d+$/.test(a[0])) return bad(); pool(st).lease = a[0]; touch(st); }, 'Время аренды DD:HH:MM');
  cmd('d6', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  function ifs(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }
  ['managed-config-flag', 'other-config-flag'].forEach(function (k) {
    cmd('gi sub', 'ipv6 nd ' + k, function (st) { ifs(st, function (x) { (x.ndf = x.ndf || {})[k] = true; }); }, k === 'managed-config-flag' ? 'Флаг M в RA: адрес по DHCPv6' : 'Флаг O в RA: прочие параметры по DHCPv6');
    cmd('gi sub', 'no ipv6 nd ' + k, function (st) { ifs(st, function (x) { if (x.ndf) delete x.ndf[k]; }); }); });
  function rt(st, a, set) { var n = +a[0]; if (!/^\d+$/.test(a[0]) || n < 5000 || n > 100000000) return bad(); set(n); touch(st); }
  cmd('config', 'ipv6 nd reachable-time <w>', function (st, a) { return rt(st, a, function (n) { st.cand.ndReach = n; }); }, 'Сколько запись ND считается REACHABLE, мс (30000)');
  cmd('config', 'no ipv6 nd reachable-time', function (st) { delete st.cand.ndReach; touch(st); });
  cmd('gi sub', 'ipv6 nd reachable-time <w>', function (st, a) { return rt(st, a, function (n) { ifs(st, function (x) { x.ndReach = n; }); }); });
  cmd('gi sub', 'no ipv6 nd reachable-time', function (st) { ifs(st, function (x) { delete x.ndReach; }); });
  P.ndReach = function (id, ifn) { var d = this.devs[id]; if (!d || d.type !== 'esr') return 30; var c = d.st.run, x = c.ifs[ifn] || {};
    return (x.ndReach || c.ndReach || 30000) / 1000; };
  S.RUNX.push(function (c, o) {
    if (c.ndReach) o.push('ipv6 nd reachable-time ' + c.ndReach);
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k], L = []; Object.keys(x.ndf || {}).forEach(function (f) { L.push('  ipv6 nd ' + f); }); if (x.ndReach) L.push('  ipv6 nd reachable-time ' + x.ndReach);
      if (L.length) o.push('interface ' + S.longIf(k), L.join('\n'), 'exit'); });
    var d = c.dhcp6; if (!d) return;
    Object.keys(d.pools).forEach(function (n) { var p = d.pools[n]; o.push('ipv6 dhcp-server pool ' + n); if (p.net) o.push('  network ' + p.net);
      if (p.range) o.push('  address-range ' + p.range.join('-')); if (p.dns) o.push('  dns-server ' + p.dns); if (p.dom) o.push('  domain-name ' + p.dom);
      if (p.lease) o.push('  default-lease-time ' + p.lease); o.push('exit'); });
    if (d.on) o.push('ipv6 dhcp-server'); });
  // ---------------------------------------------------------------- выдача адреса
  P.dhcp6 = function (id) {
    var s = this, d = s.devs[id], port = d.st.port || 'ens3', mac = EL.mac(EL.macKey(d) + port), steps = s.stepLog(), fl = s.flood(id, { name: port, port: port, tag: null }, mac), hit = null;
    steps.push({ k: 'arp', segs: fl.segs, t: d.name + ': DHCPv6 Solicit на ff02::1:2 (все DHCPv6-серверы и ретрансляторы), UDP 546 → 547',
      f: { type: 'ip6', mcast: true, smac: mac, dmac: '33:33:00:01:00:02', src: A.eui64(mac), dst: 'ff02::1:2', hlim: 1, proto: 'udp', sport: 546, dport: 547 } });
    fl.reach.some(function (e) { var rd = s.devs[e.dev]; if (rd.type !== 'esr') return false; var c = rd.st.run, d6 = c.dhcp6; if (!d6 || !d6.on) return false;
      var k = e.tag !== null ? e.port + '.' + e.tag : e.port;
      var mine = s.ifaces6(e.dev).filter(function (f) { return f.name === k && !f.ll; });
      return Object.keys(d6.pools).some(function (n) { var p = d6.pools[n]; if (!p.net || !p.range) return false;
        var q = p.net.split('/'); if (!mine.some(function (f) { return A.same(f.ip, q[0], +q[1]); })) return false;
        var L = rd.st.lease6 = rd.st.lease6 || {}, used = Object.keys(L).map(function (k2) { return L[k2]; });
        if (L[d.name]) { hit = { dev: e.dev, ip: L[d.name], pool: p, path: e.path, ifn: k }; return true; }
        for (var x = A.parse(p.range[0]), end = A.parse(p.range[1]); x <= end; x++) { var ip = A.fmt(x);
          if (used.indexOf(ip) < 0 && !s.owns6(e.dev, ip)) { L[d.name] = ip; hit = { dev: e.dev, ip: ip, pool: p, path: e.path, ifn: k }; return true; } }
        steps.push({ k: 'drop', t: rd.name + ': пул ' + n + ' исчерпан' }); return false; }); });
    if (!hit) { steps.push({ k: 'drop', t: 'Advertise не пришёл: в сегменте нет ESR с ipv6 dhcp-server и пулом для сети этого интерфейса' }); return { ok: false, steps: steps }; }
    var back = hit.path.slice().reverse().map(function (g) { return { li: g.li, from: g.to, to: g.from, tag: g.tag }; }), sv = s.devs[hit.dev].name;
    steps.push({ k: 'arpr', segs: back, t: sv + ': DHCPv6 Advertise — адрес ' + hit.ip + (hit.pool.dns ? ', DNS ' + hit.pool.dns : '') });
    steps.push({ k: 'ok', t: d.name + ': Request → ' + sv + ': Reply — адрес ' + hit.ip + '/128 закреплён (префикс и шлюз — из RA)' });
    return { ok: true, steps: steps, ip: hit.ip, dns: hit.pool.dns, server: sv };
  };
  var deb0 = H.debExec;
  H.debExec = function (st, raw) {
    var line = String(raw).trim();
    if (st.user && !st.ssh && st.net && /^dhclient\s+-6(\s+ens3)?$/.test(line)) {
      if (st.user !== 'root') return 'dhclient: must be run as root';
      if (!st.up) return 'Bind socket to interface: No such device';
      var r = st.net.dhcp6(st.dev); if (st.net.onTrace) st.net.onTrace({ ok: r.ok, steps: r.steps }, st.dev, 'DHCPv6');
      var head = 'Internet Systems Consortium DHCP Client 4.4.1\nListening on Socket/ens3\nSending on   Socket/ens3\nPRC: Soliciting for leases (INIT).\nXMT: Forming Solicit, 0 ms elapsed.\nXMT: Solicit on ens3';
      if (!r.ok) return head + '\nXMT: Solicit on ens3, interval 2050ms.\nNo DHCPv6 servers responded.';
      st.ip6 = (st.ip6 || []).filter(function (x) { return x.split('/')[0] !== r.ip; }).concat([r.ip + '/128']); if (r.dns) st.dns = st.dns || r.dns; st.net.gen++;
      return head + '\nRCV: Advertise message on ens3 from ' + r.server + '.\nPRC: Selecting best advertised lease.\nXMT: Forming Request.\nRCV: Reply message on ens3.\nPRC: Bound to lease ' + r.ip + '.';
    }
    return deb0.apply(this, arguments);
  };
  function pad(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  cmd('priv', 'show ipv6 dhcp binding', function (st) { var L = st.lease6 || {}, s = st.net, ks = Object.keys(L);
    return [pad('IPv6 address', 42) + pad('DUID / MAC', 20) + 'Binding type', pad('', 41, '-').replace(/ /g, '-') + ' ' + '------------------- ------------']
      .concat(ks.map(function (k) { var d = s && s.byName(k); return pad(L[k], 42) + pad(EL.mac(k + (d && d.st.port || 'ens3')), 20) + 'active'; })).join('\n'); }, 'Адреса, выданные DHCPv6');
})(typeof window !== 'undefined' ? window : global);
