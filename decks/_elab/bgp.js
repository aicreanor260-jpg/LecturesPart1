/* BGP на ESR (справочник ESR-Series CLI 1.23): router bgp <AS> → (config-bgp)#: router-id, address-family ipv4 unicast → (config-bgp-af)#:
   network <ADDR/LEN>, redistribute connected | static, neighbor <ADDR> → (config-bgp-neighbor)#: remote-as, update-source, ebgp-multihop,
   next-hop-self, description, enable; enable (процесс). Показ: show bgp summary, show bgp ipv4 unicast, show ip route (код B).
   Сессия: соседи ссылаются друг на друга (адрес соседа — адрес интерфейса/update-source другой стороны), AS совпадают с remote-as,
   TCP 179 доступен по таблице маршрутов (без BGP); eBGP — сосед в подключённой сети или ebgp-multihop. Маршруты: эталонный вектор путей —
   AS_PATH (петля — маршрут отбрасывается), выбор по длине AS_PATH, затем меньшему адресу соседа; от iBGP-соседа к iBGP-соседу не передаётся;
   next-hop: eBGP — адрес соседа, iBGP — как пришёл (next-hop-self — адрес соседа); AD: eBGP 20, iBGP 200.
   Упрощения: атрибуты LOCAL_PREF/MED/community, route-map, peer-group, таймеры keepalive/hold и межсетевой экран для TCP 179 не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  S.PROMPT.bgp = '(config-bgp)#'; S.PROMPT.bgpaf = '(config-bgp-af)#'; S.PROMPT.bgpn = '(config-bgp-neighbor)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('bgp', 'bgpaf', 'bgpn'); });
  function touch(st) { st.pending = true; }
  function B(st) { return st.cand.bgp; }
  S.cmd('config', 'router bgp <n>', function (st, a) { if (a[0] < 1 || a[0] > 4294967295) return 'Syntax error: Illegal parameter';
    if (!st.cand.bgp || st.cand.bgp.as !== a[0]) st.cand.bgp = { as: a[0], on: false, rid: null, nets: [], redist: [], nbr: {} };
    touch(st); st.mode = 'bgp'; st.ctx = null; }, 'Настройка BGP');
  S.cmd('config', 'no router bgp <n>', function (st, a) { if (st.cand.bgp && st.cand.bgp.as === a[0]) st.cand.bgp = null; touch(st); });
  S.cmd('bgp', 'router-id <ip>', function (st, a) { B(st).rid = a[0]; touch(st); }, 'Идентификатор маршрутизатора');
  S.cmd('bgp', 'address-family ipv4 unicast', function (st) { st.mode = 'bgpaf'; }, 'Семейство IPv4 unicast');
  S.cmd('bgp bgpaf', 'network <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return 'Syntax error: Illegal parameter';
    var v = IP.netOf(c.ip, c.len), L = B(st).nets; if (L.indexOf(v) < 0) L.push(v); touch(st); }, 'Анонсировать сеть');
  S.cmd('bgp bgpaf', 'no network <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (c) B(st).nets = B(st).nets.filter(function (x) { return x !== IP.netOf(c.ip, c.len); }); touch(st); });
  ['connected', 'static'].forEach(function (k) {
    S.cmd('bgp bgpaf', 'redistribute ' + k, function (st) { var L = B(st).redist; if (L.indexOf(k) < 0) L.push(k); touch(st); }, 'Анонсировать ' + (k === 'connected' ? 'подключённые' : 'статические'));
    S.cmd('bgp bgpaf', 'no redistribute ' + k, function (st) { B(st).redist = B(st).redist.filter(function (x) { return x !== k; }); touch(st); }); });
  S.cmd('bgp bgpaf', 'neighbor <ip>', function (st, a) { var N = B(st).nbr; N[a[0]] = N[a[0]] || { as: null, src: null, on: false, multihop: false, nhs: false };
    st.ctxAf = st.mode === 'bgpaf'; st.mode = 'bgpn'; st.ctx = a[0]; touch(st); }, 'BGP-сосед');
  S.cmd('bgp bgpaf', 'no neighbor <ip>', function (st, a) { delete B(st).nbr[a[0]]; touch(st); });
  function nb(st) { return B(st).nbr[st.ctx]; }
  S.cmd('bgpn', 'remote-as <n>', function (st, a) { nb(st).as = a[0]; touch(st); }, 'AS соседа');
  S.cmd('bgpn', 'update-source <ip>', function (st, a) { nb(st).src = a[0]; touch(st); }, 'Адрес источника сессии');
  S.cmd('bgpn', 'ebgp-multihop', function (st) { nb(st).multihop = true; touch(st); }, 'eBGP через несколько хопов');
  S.cmd('bgpn', 'ebgp-multihop <n>', function (st) { nb(st).multihop = true; touch(st); });
  S.cmd('bgpn', 'next-hop-self', function (st) { nb(st).nhs = true; touch(st); }, 'Next-hop — свой адрес (iBGP)');
  S.cmd('bgpn', 'description <rest>', function (st, a) { nb(st).desc = a[0].replace(/^["']|["']$/g, ''); touch(st); }, 'Описание');
  S.cmd('bgpn', 'enable', function (st) { nb(st).on = true; touch(st); }, 'Включить соседство');
  S.cmd('bgpn', 'no enable', function (st) { nb(st).on = false; touch(st); });
  S.cmd('bgpn', 'exit', function (st) { st.mode = st.ctxAf ? 'bgpaf' : 'bgp'; st.ctx = null; });
  S.cmd('bgpaf', 'exit', function (st) { st.mode = 'bgp'; });
  S.cmd('bgp', 'exit', function (st) { st.mode = 'config'; });
  S.cmd('bgp bgpaf', 'enable', function (st) { B(st).on = true; touch(st); }, 'Запустить BGP');
  S.cmd('bgp bgpaf', 'no enable', function (st) { B(st).on = false; touch(st); });
  S.RUNX.push(function (c, o) { var b = c.bgp; if (!b) return;
    o.push('router bgp ' + b.as); if (b.rid) o.push('  router-id ' + b.rid); o.push('  address-family ipv4 unicast');
    b.nets.forEach(function (n) { o.push('    network ' + n); }); b.redist.forEach(function (n) { o.push('    redistribute ' + n); });
    Object.keys(b.nbr).forEach(function (ip) { var x = b.nbr[ip]; o.push('    neighbor ' + ip); if (x.desc) o.push('      description "' + x.desc + '"');
      if (x.as) o.push('      remote-as ' + x.as); if (x.src) o.push('      update-source ' + x.src); if (x.multihop) o.push('      ebgp-multihop'); if (x.nhs) o.push('      next-hop-self');
      if (x.on) o.push('      enable'); o.push('    exit'); });
    if (b.on) o.push('    enable'); o.push('  exit', 'exit'); });

  // ---------------------------------------------------------------- расчёт
  function rid(s, id) { var b = s.devs[id].st.run.bgp; return (b && b.rid) || (s.ifaces(id).map(function (f) { return f.ip; }).sort(function (a, b2) { return IP.ip2n(b2) - IP.ip2n(a); })[0] || '0.0.0.0'); }
  // достижимость без BGP и без побочных эффектов: по таблицам маршрутов и L2-рассылке, хоп за хопом
  function reach(s, src, dst) {
    var cur = src, o = s._noBgp; s._noBgp = true;
    try { for (var i = 0; i < 16; i++) {
      if (s.ifaces(cur).some(function (f) { return f.ip === dst; })) return true;
      var r = s.lookup(cur, dst); if (!r) return false;
      if (r.iface.tun) return false;
      var ep = s.flood(cur, r.iface).eps.filter(function (e) { return e.iface.ip === r.nh; })[0]; if (!ep) return false; cur = ep.dev; } }
    finally { s._noBgp = o; }
    return false;
  }
  P.bgpSessions = function () {
    if (this._bgpS && this._bgpS.gen === this.gen) return this._bgpS.t;
    var s = this, t = {};
    s.order.forEach(function (id) { var d = s.devs[id]; if (d.type !== 'esr' || d.off) return; var b = d.st.run.bgp; if (!b || !b.on) return;
      Object.keys(b.nbr).forEach(function (ip) { var x = b.nbr[ip], st = 'Idle', peer = null, why = '';
        if (!x.on) why = 'neighbor не включён (enable)'; else if (!x.as) why = 'не задан remote-as';
        else { var pid = s.owner(ip), pd = pid && s.devs[pid], pb = pd && pd.type === 'esr' && !pd.off ? pd.st.run.bgp : null;
          var mine = x.src || null;
          if (!pb || !pb.on) { st = 'Active'; why = 'у соседа нет BGP или он выключен'; }
          else if (pb.as !== x.as) { st = 'Active'; why = 'remote-as ' + x.as + ' не совпадает с AS соседа ' + pb.as; }
          else { var back = Object.keys(pb.nbr).filter(function (q) { var y = pb.nbr[q]; return y.on && s.ifaces(id).some(function (f) { return f.ip === q; }) && (!mine || q === mine); })[0];
            if (!back) { st = 'Active'; why = 'у соседа нет neighbor на наш адрес'; }
            else if (pb.nbr[back].as !== b.as) { st = 'Active'; why = 'сосед ждёт AS ' + pb.nbr[back].as + ', а у нас ' + b.as; }
            else { var ebgp = b.as !== pb.as, direct = s.ifaces(id).some(function (f) { return f.port !== null && IP.sameNet(ip, f.ip, f.len); });
              if (ebgp && !direct && !x.multihop) { st = 'Active'; why = 'eBGP-сосед не в подключённой сети — нужен ebgp-multihop'; }
              else if (!reach(s, id, ip) || !reach(s, pid, back)) { st = 'Active'; why = 'нет связи с соседом (TCP 179)'; }
              else { st = 'Established'; peer = { dev: pid, ip: back, ebgp: ebgp }; } } } }
        (t[id] = t[id] || {})[ip] = { state: st, peer: peer, why: why, as: x.as, since: s.now }; }); });
    var prev = this._bgpS && this._bgpS.t; if (prev) Object.keys(t).forEach(function (id) { Object.keys(t[id]).forEach(function (ip) {
      var p = prev[id] && prev[id][ip]; if (p && p.state === t[id][ip].state) t[id][ip].since = p.since; }); });
    this._bgpS = { gen: this.gen, t: t };
    return t;
  };
  // вектор путей: маршруты каждого ESR — {net: {path:[AS…], nh, from, ibgp}}
  P.bgpRib = function () {
    if (this._bgpR && this._bgpR.gen === this.gen) return this._bgpR.t;
    var s = this, S2 = s.bgpSessions(), rib = {}, ids = Object.keys(S2);
    s.order.forEach(function (id) { var d = s.devs[id], b = d.type === 'esr' && !d.off && d.st.run.bgp; if (!b || !b.on) return; rib[id] = {};
      var o = s._noBgp; s._noBgp = true; var rs; try { rs = s.routes(id); } finally { s._noBgp = o; }
      var live = rs.filter(function (r) { return !r.dead; });
      b.nets.forEach(function (n) { if (live.some(function (r) { return r.net === n; })) rib[id][n] = { path: [], nh: '0.0.0.0', local: true }; });
      b.redist.forEach(function (k) { live.filter(function (r) { return r.p === (k === 'connected' ? 'C' : 'S'); }).forEach(function (r) { if (!rib[id][r.net]) rib[id][r.net] = { path: [], nh: '0.0.0.0', local: true, origin: '?' }; }); }); });
    for (var it = 0; it < 12; it++) { var ch = false;
      ids.forEach(function (id) { if (!rib[id]) return; var asMe = s.devs[id].st.run.bgp.as;
        Object.keys(S2[id]).forEach(function (ip) { var ss = S2[id][ip]; if (ss.state !== 'Established') return; var pd = ss.peer.dev; if (!rib[pd]) return;
          var pAs = s.devs[pd].st.run.bgp.as, pn = s.devs[pd].st.run.bgp.nbr[ss.peer.ip] || {};
          Object.keys(rib[pd]).forEach(function (net) { var e = rib[pd][net];
            if (!ss.peer.ebgp && e.ibgp) return;                       // iBGP → iBGP не передаётся
            var path = ss.peer.ebgp ? [pAs].concat(e.path) : e.path.slice();
            if (path.indexOf(asMe) >= 0) return;                        // петля AS_PATH
            var nh = ss.peer.ebgp || pn.nhs || e.local ? ip : e.nh, cand = { path: path, nh: nh, from: ip, ibgp: !ss.peer.ebgp, origin: e.origin };
            var cur = rib[id][net];
            if (cur && cur.local) return;
            if (!cur || path.length < cur.path.length || (path.length === cur.path.length && IP.ip2n(ip) < IP.ip2n(cur.from))) {
              if (!cur || cur.from !== ip || cur.path.join() !== path.join() || cur.nh !== nh) { rib[id][net] = cand; ch = true; } } }); }); });
      if (!ch) break; }
    this._bgpR = { gen: this.gen, t: rib };
    return rib;
  };
  var routes0 = P.routes;
  P.routes = function (id) {
    var r = routes0.apply(this, arguments);
    if (this._noBgp || this.devs[id].type !== 'esr' || this._vrfCtx) return r;
    var s = this, rib = (this.bgpRib() || {})[id]; if (!rib) return r;
    Object.keys(rib).forEach(function (net) { var e = rib[net]; if (e.local) return;
      var o = s._noBgp; s._noBgp = true; var via; try { via = s.lookup(id, e.nh); } finally { s._noBgp = o; }
      if (!via) return;
      r.push({ p: 'B', net: net, len: +net.split('/')[1], nh: via.nh === e.nh || IP.sameNet(e.nh, via.iface.ip, via.iface.len) ? e.nh : via.nh, ifn: via.iface.name, ad: e.ibgp ? 200 : 20, m: 0 }); });
    return r;
  };
  // ---------------------------------------------------------------- show
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function hms(n) { n = Math.max(0, Math.floor(n)); var p = function (v) { return ('0' + v).slice(-2); }; return p(Math.floor(n / 3600)) + ':' + p(Math.floor(n / 60) % 60) + ':' + p(n % 60); }
  S.cmd('priv', 'show bgp summary', function (st) { var s = st.net, b = st.run.bgp; if (!s || !b) return '';
    var t = s.bgpSessions()[st.dev] || {}, rib = s.bgpRib()[st.dev] || {};
    return ['  BGP router identifier ' + rid(s, st.dev) + ', local AS number ' + b.as, '  BGP activity ' + Object.keys(rib).length + '/0 prefixes',
      '  Neighbor                 AS              MsgRcvd      MsgSent      Up/Down      St/PfxRcd', '  ----------------------   -------------   ----------   ----------   ----------   ------------']
      .concat(Object.keys(b.nbr).map(function (ip) { var x = t[ip] || { state: 'Idle', as: b.nbr[ip].as }, up = x.state === 'Established', k = Math.floor((s.now - (x.since || 0)) / 60);
        var pfx = Object.keys(rib).filter(function (n) { return rib[n].from === ip; }).length;
        return '  ' + rp(ip, 25) + rp(x.as || '--', 16) + rp(up ? 2 + k : 0, 13) + rp(up ? 2 + k : 0, 13) + rp(hms(s.now - (x.since || 0)), 13) + (up ? pfx : x.state); })).join('\n'); }, 'Сводка BGP');
  S.cmd('priv', 'show bgp ipv4 unicast', function (st) { var s = st.net; if (!s || !st.run.bgp) return '';
    var rib = s.bgpRib()[st.dev] || {};
    return ['Status codes: u – unicast, b – broadcast, m – multicast a – anycast', '              * – valid, > – best', 'Origin codes: i – IGP, e – EGP, ? – incomplete',
      '     Network              Next Hop             Metric  LocPrf  Path'].concat(Object.keys(rib).sort().map(function (n) { var e = rib[n];
        return '*> u ' + rp(n, 21) + rp(e.nh, 21) + rp('', 8) + rp(100, 8) + (e.path.length ? e.path.join(' ') + ' ' : '') + (e.origin || 'i'); })).join('\n'); }, 'Таблица BGP');
  S.cmd('priv', 'show bgp neighbors', function (st) { var s = st.net, b = st.run.bgp; if (!s || !b) return ''; var t = s.bgpSessions()[st.dev] || {};
    return Object.keys(b.nbr).map(function (ip) { var x = t[ip] || {}; return 'BGP neighbor is ' + ip + ', remote AS ' + (b.nbr[ip].as || '--') + ', ' + (x.peer && !x.peer.ebgp ? 'internal' : 'external') + ' link\n' +
      '  BGP state = ' + (x.state || 'Idle') + (x.why ? '  (' + x.why + ')' : ''); }).join('\n\n'); }, 'Соседи BGP');
})(typeof window !== 'undefined' ? window : global);
