/* BGP на ESR (справочник ESR-Series CLI 1.23, иерархия режимов сверена с ПО ESR): router bgp <AS> → (config-bgp)#: router-id, enable (процесс),
   neighbor <ADDR> → (config-bgp-neighbor)#: remote-as, update-source, ebgp-multihop, description, enable, address-family ipv4 unicast →
   (config-bgp-neighbor-af)#: enable (обмен маршрутами), next-hop-self, route-map; address-family ipv4 unicast → (config-bgp-af)#: network, redistribute. Показ: show bgp summary, show bgp ipv4 unicast, show ip route (код B).
   Сессия: соседи ссылаются друг на друга (адрес соседа — адрес интерфейса/update-source другой стороны), AS совпадают с remote-as,
   TCP 179 доступен по таблице маршрутов (без BGP); eBGP — сосед в подключённой сети или ebgp-multihop. Маршруты: эталонный вектор путей —
   AS_PATH (петля — маршрут отбрасывается), выбор по длине AS_PATH, затем меньшему адресу соседа; от iBGP-соседа к iBGP-соседу не передаётся;
   next-hop: eBGP — адрес соседа, iBGP — как пришёл (next-hop-self — адрес соседа); AD: eBGP 20, iBGP 200.
   Упрощения: атрибуты LOCAL_PREF/MED/community, route-map, peer-group, межсетевой экран для TCP 179 не моделируется.
   Таймеры: keepalive/holdtime (60/180, согласуется меньший hold); сосед пропал без разрыва своего линка — сессия и маршруты живут
   до истечения hold time; NOTIFICATION (смена настроек) или падение своего интерфейса — разрыв сразу; новая попытка — через error-wait 60 с,
   если соединение не вызвано изменением настроек на одной из сторон. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  S.PROMPT.bgp = '(config-bgp)#'; S.PROMPT.bgpaf = '(config-bgp-af)#'; S.PROMPT.bgpn = '(config-bgp-neighbor)#'; S.PROMPT.bgpnaf = '(config-bgp-neighbor-af)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('bgp', 'bgpaf', 'bgpn', 'bgpnaf'); });
  function touch(st) { st.pending = true; }
  function B(st) { return st.cand.bgp; }
  // иерархия как в ПО ESR: (config-bgp) → neighbor → (config-bgp-neighbor) → address-family ipv4 unicast → (config-bgp-neighbor-af);
  // network / redistribute — в (config-bgp) → address-family ipv4 unicast → (config-bgp-af)
  S.cmd('config', 'router bgp <n>', function (st, a) { if (a[0] < 1 || a[0] > 4294967295) return 'Syntax error: Illegal parameter';
    if (!st.cand.bgp || st.cand.bgp.as !== a[0]) st.cand.bgp = { as: a[0], on: false, rid: null, nets: [], redist: [], nbr: {} };
    touch(st); st.mode = 'bgp'; st.ctx = null; }, 'Настройка BGP');
  S.cmd('config', 'no router bgp <n>', function (st, a) { if (st.cand.bgp && st.cand.bgp.as === a[0]) st.cand.bgp = null; touch(st); });
  S.cmd('bgp', 'router-id <ip>', function (st, a) { B(st).rid = a[0]; touch(st); }, 'Идентификатор маршрутизатора');
  S.cmd('bgp', 'address-family ipv4 unicast', function (st) { st.mode = 'bgpaf'; }, 'Семейство IPv4 unicast: network, redistribute');
  S.cmd('bgpaf', 'network <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return 'Syntax error: Illegal parameter';
    var v = IP.netOf(c.ip, c.len), L = B(st).nets; if (L.indexOf(v) < 0) L.push(v); touch(st); }, 'Анонсировать сеть');
  S.cmd('bgpaf', 'no network <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (c) B(st).nets = B(st).nets.filter(function (x) { return x !== IP.netOf(c.ip, c.len); }); touch(st); });
  ['connected', 'static'].forEach(function (k) {
    S.cmd('bgpaf', 'redistribute ' + k, function (st) { var L = B(st).redist; if (L.indexOf(k) < 0) L.push(k); touch(st); }, 'Анонсировать ' + (k === 'connected' ? 'подключённые' : 'статические'));
    S.cmd('bgpaf', 'no redistribute ' + k, function (st) { B(st).redist = B(st).redist.filter(function (x) { return x !== k; }); touch(st); }); });
  S.cmd('bgp', 'neighbor <ip>', function (st, a) { var N = B(st).nbr; N[a[0]] = N[a[0]] || { as: null, src: null, on: false, af: false, multihop: false, nhs: false };
    st.mode = 'bgpn'; st.ctx = a[0]; touch(st); }, 'BGP-сосед');
  S.cmd('bgp', 'no neighbor <ip>', function (st, a) { delete B(st).nbr[a[0]]; touch(st); });
  function nb(st) { return B(st).nbr[st.ctx]; }
  S.cmd('bgpn', 'remote-as <n>', function (st, a) { nb(st).as = a[0]; touch(st); }, 'AS соседа');
  S.cmd('bgpn', 'update-source <ip>', function (st, a) { nb(st).src = a[0]; touch(st); }, 'Адрес источника сессии');
  S.cmd('bgpn', 'ebgp-multihop', function (st) { nb(st).multihop = true; touch(st); }, 'eBGP через несколько хопов');
  S.cmd('bgpn', 'ebgp-multihop <n>', function (st) { nb(st).multihop = true; touch(st); });
  S.cmd('bgpn', 'description <rest>', function (st, a) { nb(st).desc = a[0].replace(/^["']|["']$/g, ''); touch(st); }, 'Описание');
  S.cmd('bgpn', 'enable', function (st) { nb(st).on = true; touch(st); }, 'Включить соседство');
  S.cmd('bgpn', 'no enable', function (st) { nb(st).on = false; touch(st); });
  S.cmd('bgpn', 'address-family ipv4 unicast', function (st) { st.mode = 'bgpnaf'; }, 'Семейство IPv4 для соседа: enable, next-hop-self');
  S.cmd('bgpnaf', 'enable', function (st) { nb(st).af = true; touch(st); }, 'Обмениваться маршрутами IPv4 с соседом');
  S.cmd('bgpnaf', 'no enable', function (st) { nb(st).af = false; touch(st); });
  S.cmd('bgpnaf', 'next-hop-self', function (st) { nb(st).nhs = true; touch(st); }, 'Next-hop — свой адрес (iBGP)');
  S.cmd('bgpnaf', 'no next-hop-self', function (st) { nb(st).nhs = false; touch(st); });
  S.cmd('bgpnaf', 'route-map <w> <w>', function (st, a) { if (a[1] !== 'in' && a[1] !== 'out') return 'Syntax error: Illegal parameter'; (nb(st).rmap = nb(st).rmap || {})[a[1]] = a[0]; touch(st); }, 'Маршрутная карта in | out (не моделируется)');
  S.cmd('bgpnaf', 'exit', function (st) { st.mode = 'bgpn'; });
  S.cmd('bgpn', 'exit', function (st) { st.mode = 'bgp'; st.ctx = null; });
  S.cmd('bgpaf', 'exit', function (st) { st.mode = 'bgp'; });
  S.cmd('bgp', 'exit', function (st) { st.mode = 'config'; });
  [['bgp', function (st) { return B(st); }], ['bgpn', function (st) { return nb(st); }]].forEach(function (m) {
    S.cmd(m[0], 'timers keepalive <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return 'Syntax error: Illegal parameter'; m[1](st).ka = a[0]; touch(st); }, 'Период keepalive, с (по умолчанию 60)');
    S.cmd(m[0], 'no timers keepalive', function (st) { delete m[1](st).ka; touch(st); });
    S.cmd(m[0], 'timers holdtime <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return 'Syntax error: Illegal parameter'; m[1](st).hold = a[0]; touch(st); }, 'Hold time: сосед недоступен, если нет keepalive, с (по умолчанию 180)');
    S.cmd(m[0], 'no timers holdtime', function (st) { delete m[1](st).hold; touch(st); }); });
  S.cmd('bgp', 'enable', function (st) { B(st).on = true; touch(st); }, 'Запустить BGP');
  S.cmd('bgp', 'no enable', function (st) { B(st).on = false; touch(st); });
  S.RUNX.push(function (c, o) { var b = c.bgp; if (!b) return;
    o.push('router bgp ' + b.as); if (b.rid) o.push('  router-id ' + b.rid);
    if (b.ka) o.push('  timers keepalive ' + b.ka); if (b.hold) o.push('  timers holdtime ' + b.hold);
    Object.keys(b.nbr).forEach(function (ip) { var x = b.nbr[ip]; o.push('  neighbor ' + ip); if (x.desc) o.push('    description "' + x.desc + '"');
      if (x.as) o.push('    remote-as ' + x.as); if (x.src) o.push('    update-source ' + x.src); if (x.multihop) o.push('    ebgp-multihop');
      if (x.ka) o.push('    timers keepalive ' + x.ka); if (x.hold) o.push('    timers holdtime ' + x.hold);
      if (x.af || x.nhs || x.rmap) { o.push('    address-family ipv4 unicast'); if (x.nhs) o.push('      next-hop-self');
        Object.keys(x.rmap || {}).forEach(function (d) { o.push('      route-map ' + x.rmap[d] + ' ' + d); }); if (x.af) o.push('      enable'); o.push('    exit'); }
      if (x.on) o.push('    enable'); o.push('  exit'); });
    if (b.nets.length || b.redist.length) { o.push('  address-family ipv4 unicast'); b.nets.forEach(function (n) { o.push('    network ' + n); });
      b.redist.forEach(function (n) { o.push('    redistribute ' + n); }); o.push('  exit'); }
    if (b.on) o.push('  enable'); o.push('exit'); });

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
  // сессия возможна при текущей топологии и настройках (без учёта таймеров)
  function want(s) {
    var t = {};
    s.order.forEach(function (id) { var d = s.devs[id]; if (d.type !== 'esr' || d.off) return; var b = d.st.run.bgp; if (!b || !b.on) return;
      Object.keys(b.nbr).forEach(function (ip) { var x = b.nbr[ip], st = 'Idle', peer = null, why = '';
        if (!x.on) why = 'neighbor не включён (enable)'; else if (!x.as) why = 'не задан remote-as';
        else { var pid = s.owner(ip), pd = pid && s.devs[pid], pb = pd && pd.type === 'esr' && !pd.off ? pd.st.run.bgp : null;
          var mine = x.src || null;
          if (!pd || pd.off) { st = 'Active'; why = 'нет связи с соседом (TCP 179)'; }
          else if (!pb || !pb.on) { st = 'Active'; why = 'у соседа нет BGP или он выключен'; }
          else if (pb.as !== x.as) { st = 'Active'; why = 'remote-as ' + x.as + ' не совпадает с AS соседа ' + pb.as; }
          else { var back = Object.keys(pb.nbr).filter(function (q) { var y = pb.nbr[q]; return y.on && s.ifaces(id).some(function (f) { return f.ip === q; }) && (!mine || q === mine); })[0];
            if (!back) { st = 'Active'; why = 'у соседа нет neighbor на наш адрес'; }
            else if (pb.nbr[back].as !== b.as) { st = 'Active'; why = 'сосед ждёт AS ' + pb.nbr[back].as + ', а у нас ' + b.as; }
            else { var ebgp = b.as !== pb.as, direct = s.ifaces(id).some(function (f) { return f.port !== null && IP.sameNet(ip, f.ip, f.len); });
              if (ebgp && !direct && !x.multihop) { st = 'Active'; why = 'eBGP-сосед не в подключённой сети — нужен ebgp-multihop'; }
              else if (!reach(s, id, ip) || !reach(s, pid, back)) { st = 'Active'; why = 'нет связи с соседом (TCP 179)'; }
              else { st = 'Established'; peer = { dev: pid, ip: back, ebgp: ebgp }; } } } }
        (t[id] = t[id] || {})[ip] = { state: st, peer: peer, why: why, as: x.as, off: !!(pd && pd.off) }; }); });
    return t;
  }
  // таймеры сессии (справочник ESR 1.23): timers keepalive 60, timers holdtime 180 — на процессе или соседе; согласуется меньший hold,
  // keepalive не больше hold/3. Повторная попытка соединения — через error-wait (60 с)
  var KA = 60, HOLD = 180, RETRY = 60;
  function tmr(s, id, ip) { var b = s.devs[id].st.run.bgp || {}, x = (b.nbr || {})[ip] || {}; return { ka: x.ka || b.ka || KA, hold: x.hold || b.hold || HOLD }; }
  P.bgpTimers = function (id, ip) {
    var me = tmr(this, id, ip), w = (this._bgpA || {})[id + '|' + ip], hold = me.hold;
    if (w && w.peer) { var pt = tmr(this, w.peer.dev, w.peer.ip); hold = Math.min(me.hold, pt.hold); }
    return { hold: hold, ka: Math.min(me.ka, Math.floor(hold / 3)) || 1 };
  };
  // свой интерфейс в сеть соседа упал — сессия рвётся сразу (линк), иначе соседа ждут hold time
  function linkDown(s, id, ip) { var c = s.devs[id].st.run;
    return Object.keys(c.ifs).some(function (k) { var x = c.ifs[k]; if (!x.ip) return false; var q = x.ip.split('/');
      return IP.sameNet(ip, q[0], +q[1]) && (x.shut || !s.linkUp(id, k.split('.')[0])); }); }
  P.bgpSessions = function () {
    if (this._bgpS && this._bgpS.gen === this.gen && this._bgpS.now === this.now) return this._bgpS.t;
    var s = this, w = want(s), A = s._bgpA = s._bgpA || {}, K = s._bgpKick || {}, t = {};
    function attempt(k) {                        // момент ближайшей попытки этой стороны: сразу для новой сессии, иначе по шагу error-wait
      var a = A[k]; if (a && a.up) return s.now;
      if (!a || a.wantT === undefined) a = A[k] = { up: false, since: a ? a.since : s.now, next: a ? a.next : s.now, wantT: s.now };
      return a.next >= a.wantT ? a.next : a.next + Math.ceil((a.wantT - a.next) / RETRY) * RETRY;
    }
    Object.keys(w).forEach(function (id) { t[id] = {}; Object.keys(w[id]).forEach(function (ip) {
      var x = w[id][ip], k = id + '|' + ip, a = A[k], pid = s.owner(ip), kick = K[id] === s.now || (pid && K[pid] === s.now), r = null;
      if (x.state === 'Established') {
        if (a && a.up) { a.ka = s.now; a.peer = x.peer; }
        else {
          var at = kick ? s.now : Math.min(attempt(k), attempt(x.peer.dev + '|' + x.peer.ip));   // соединение открывает любая из сторон
          a = A[k];
          if (s.now >= at) a = A[k] = { up: true, since: at, ka: s.now, peer: x.peer };
          else r = { state: 'Active', why: 'повторная попытка соединения через ' + Math.ceil(at - s.now) + ' с (error-wait)' };
        }
        if (!r) r = { state: 'Established', peer: a.peer, why: '' };
      } else {
        var soft = a && a.up && (x.off || /нет связи/.test(x.why)) && !linkDown(s, id, ip);
        if (soft) { var hold = s.bgpTimers(id, ip).hold;
          if (s.now - a.ka < hold) r = { state: 'Established', peer: a.peer, stale: true, why: 'keepalive от соседа не приходят ' + Math.floor(s.now - a.ka) + ' с, hold time ' + hold + ' с' };
          else { var end = a.ka + hold; a = A[k] = { up: false, since: end, next: end + RETRY, hte: true }; } }
        else if (a && a.up) a = A[k] = { up: false, since: s.now, next: s.now + RETRY };
        else if (!a) a = A[k] = { up: false, since: s.now, next: s.now + RETRY };
        else if (a.wantT !== undefined) { delete a.wantT; }
        if (!r) r = { state: x.state, peer: null, why: (a.hte ? 'Hold timer expired; ' : '') + x.why };
      }
      t[id][ip] = { state: r.state, peer: r.peer, why: r.why, as: x.as, since: a.since, stale: !!r.stale };
    }); });
    Object.keys(A).forEach(function (k) { var q = k.split('|'); if (!w[q[0]] || !w[q[0]][q[1]]) delete A[k]; });
    this._bgpS = { gen: this.gen, now: this.now, t: t };
    return t;
  };
  // наблюдение за изменениями в момент модельного времени: до и после команды, перед ходом часов
  var ex0 = P.exec;
  // попытка соединения сразу — только когда меняется настройка (commit/confirm, clear bgp), а не на любую команду
  P.exec = function (id, line) { this.bgpSessions(); if (/^\s*(do\s+)?(commit|confirm|clear\s+(ip\s+)?bgp)\b/.test(String(line))) (this._bgpKick = this._bgpKick || {})[id] = this.now;
    var r = ex0.apply(this, arguments); this.bgpSessions(); return r; };
  ['connect', 'disconnect', 'power', 'reboot'].forEach(function (m) { var f = P[m]; if (!f) return;
    P[m] = function () { this.bgpSessions(); var r = f.apply(this, arguments); this.bgpSessions(); return r; }; });
  var tk0 = P.tick;
  P.tick = function () { this.bgpSessions(); return tk0.apply(this, arguments); };
  // запомненные маршруты соседа (adj-RIB-in): пока сессия жива по hold time, они остаются (соседа уже нет — «чёрная дыра»)
  // вектор путей: маршруты каждого ESR — {net: {path:[AS…], nh, from, ibgp}}
  P.bgpRib = function () {
    if (this._bgpR && this._bgpR.gen === this.gen && this._bgpR.now === this.now) return this._bgpR.t;
    var s = this, S2 = s.bgpSessions(), rib = {}, ids = Object.keys(S2), adjIn = s._adjIn = s._adjIn || {};
    Object.keys(adjIn).forEach(function (mk) { var q = mk.split('|'), ss = (S2[q[0]] || {})[q[1]];
      if (!ss || ss.state !== 'Established') delete adjIn[mk]; else if (!ss.stale) adjIn[mk] = {}; });
    s.order.forEach(function (id) { var d = s.devs[id], b = d.type === 'esr' && !d.off && d.st.run.bgp; if (!b || !b.on) return; rib[id] = {};
      var o = s._noBgp; s._noBgp = true; var rs; try { rs = s.routes(id); } finally { s._noBgp = o; }
      var live = rs.filter(function (r) { return !r.dead; });
      b.nets.forEach(function (n) { if (live.some(function (r) { return r.net === n; })) rib[id][n] = { path: [], nh: '0.0.0.0', local: true }; });
      b.redist.forEach(function (k) { live.filter(function (r) { return r.p === (k === 'connected' ? 'C' : 'S'); }).forEach(function (r) { if (!rib[id][r.net]) rib[id][r.net] = { path: [], nh: '0.0.0.0', local: true, origin: '?' }; }); }); });
    for (var it = 0; it < 12; it++) { var ch = false;
      ids.forEach(function (id) { if (!rib[id]) return; var asMe = s.devs[id].st.run.bgp.as;
        Object.keys(S2[id]).forEach(function (ip) { var ss = S2[id][ip]; if (ss.state !== 'Established') return; var pd = ss.peer.dev, mk = id + '|' + ip;
          if (ss.stale || !rib[pd]) { Object.keys(adjIn[mk] || {}).forEach(function (net) { var c = adjIn[mk][net], cur = rib[id][net];
              if (cur && cur.local) return; if (!cur || c.path.length < cur.path.length) { if (!cur || cur.from !== c.from || cur.nh !== c.nh) { rib[id][net] = c; ch = true; } } }); return; }
          var pAs = s.devs[pd].st.run.bgp.as, pn = s.devs[pd].st.run.bgp.nbr[ss.peer.ip] || {};
          var my = s.devs[id].st.run.bgp.nbr[ip] || {}; if (!my.af || !pn.af) return;    // address-family ipv4 unicast → enable у обоих
          Object.keys(rib[pd]).forEach(function (net) { var e = rib[pd][net];
            if (!ss.peer.ebgp && e.ibgp) return;                       // iBGP → iBGP не передаётся
            var path = ss.peer.ebgp ? [pAs].concat(e.path) : e.path.slice();
            if (path.indexOf(asMe) >= 0) return;                        // петля AS_PATH
            var nh = ss.peer.ebgp || pn.nhs || e.local ? ip : e.nh, cand = { path: path, nh: nh, from: ip, ibgp: !ss.peer.ebgp, origin: e.origin };
            (adjIn[mk] = adjIn[mk] || {})[net] = cand;
            var cur = rib[id][net];
            if (cur && cur.local) return;
            if (!cur || path.length < cur.path.length || (path.length === cur.path.length && IP.ip2n(ip) < IP.ip2n(cur.from))) {
              if (!cur || cur.from !== ip || cur.path.join() !== path.join() || cur.nh !== nh) { rib[id][net] = cand; ch = true; } } }); }); });
      if (!ch) break; }
    this._bgpR = { gen: this.gen, now: this.now, t: rib };
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
      .concat(Object.keys(b.nbr).map(function (ip) { var x = t[ip] || { state: 'Idle', as: b.nbr[ip].as }, up = x.state === 'Established', k = Math.floor((s.now - (x.since || 0)) / s.bgpTimers(st.dev, ip).ka);
        var pfx = Object.keys(rib).filter(function (n) { return rib[n].from === ip; }).length;
        return '  ' + rp(ip, 25) + rp(x.as || '--', 16) + rp(up ? 2 + k : 0, 13) + rp(up ? 2 + k : 0, 13) + rp(hms(s.now - (x.since || 0)), 13) + (up ? pfx : x.state); })).join('\n'); }, 'Сводка BGP');
  S.cmd('priv', 'show bgp ipv4 unicast', function (st) { var s = st.net; if (!s || !st.run.bgp) return '';
    var rib = s.bgpRib()[st.dev] || {};
    return ['Status codes: u – unicast, b – broadcast, m – multicast a – anycast', '              * – valid, > – best', 'Origin codes: i – IGP, e – EGP, ? – incomplete',
      '     Network              Next Hop             Metric  LocPrf  Path'].concat(Object.keys(rib).sort().map(function (n) { var e = rib[n];
        return '*> u ' + rp(n, 21) + rp(e.nh, 21) + rp('', 8) + rp(100, 8) + (e.path.length ? e.path.join(' ') + ' ' : '') + (e.origin || 'i'); })).join('\n'); }, 'Таблица BGP');
  S.cmd('priv', 'show bgp neighbors', function (st) { var s = st.net, b = st.run.bgp; if (!s || !b) return ''; var t = s.bgpSessions()[st.dev] || {};
    return Object.keys(b.nbr).map(function (ip) { var x = t[ip] || {}; return 'BGP neighbor is ' + ip + ', remote AS ' + (b.nbr[ip].as || '--') + ', ' + (x.peer && !x.peer.ebgp ? 'internal' : 'external') + ' link\n' +
      '  BGP state = ' + (x.state || 'Idle') + (x.state === 'Established' ? ', up for ' + hms(s.now - x.since) : '') + (x.why ? '  (' + x.why + ')' : '') +
      '\n  Hold time is ' +s.bgpTimers(st.dev, ip).hold + ', keepalive interval is ' + s.bgpTimers(st.dev, ip).ka + ' seconds'; }).join('\n\n'); }, 'Соседи BGP');
})(typeof window !== 'undefined' ? window : global);
