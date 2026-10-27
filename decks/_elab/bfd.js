/* BFD на ESR (справочник ESR-Series CLI 1.23): ip route <SUBNET> <NEXTHOP> bfd [<METRIC>] — статический маршрут снимается, когда
   BFD-сессия с next-hop падает; ip bfd min-rx-interval | min-tx-interval | idle-tx-interval | multiplier (по умолчанию 200/300 мс и 5);
   show ip bfd, show bfd neighbors [<ADDR>]; при падении сессии — «%BFD-W-NEIG: Session to A.B.C.D Down» (как в справочнике).
   Без bfd маршрут живёт, пока подключена сеть next-hop, даже если сам next-hop выключен за коммутатором (кадры уходят в никуда);
   с bfd маршрут снимается и включается запасной (плавающий) маршрут. Сессия поднимается с ESR, достижимым в подключённой сети.
   Упрощения: время обнаружения (интервал × multiplier, около 1 с) считается мгновенным; ip ospf bfd-enable не моделируется. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  function touch(st) { st.pending = true; }
  function big(st) { var m = st.net && st.net.devs[st.dev] ? st.net.devs[st.dev].model : ''; return /^ESR-(1\d\d\d|3\d\d\d)/.test(m); }
  function cfg(st, c) { var b = (c || st.run).bfd || {}, d = big(st) ? 200 : 300; return { rx: b.rx || d, tx: b.tx || d, idle: b.idle || 1000, mult: b.mult || 5 }; }
  function bset(st, k, v, lo, hi) { if (v < lo || v > hi) return 'Syntax error: Illegal parameter'; (st.cand.bfd = st.cand.bfd || {})[k] = v; touch(st); }
  S.cmd('config', 'ip bfd min-rx-interval <n>', function (st, a) { return bset(st, 'rx', a[0], big(st) ? 200 : 300, 65535); }, 'Интервал приёма BFD, мс');
  S.cmd('config', 'ip bfd min-tx-interval <n>', function (st, a) { return bset(st, 'tx', a[0], big(st) ? 200 : 300, 65535); }, 'Интервал передачи BFD, мс');
  S.cmd('config', 'ip bfd idle-tx-interval <n>', function (st, a) { return bset(st, 'idle', a[0], 1000, 65535); }, 'Интервал BFD без сессии, мс');
  S.cmd('config', 'ip bfd multiplier <n>', function (st, a) { return bset(st, 'mult', a[0], 1, 100); }, 'Сколько пропусков — сосед недоступен');
  S.RUNX.push(function (c, o) { var b = c.bfd || {};
    if (b.rx) o.push('ip bfd min-rx-interval ' + b.rx); if (b.tx) o.push('ip bfd min-tx-interval ' + b.tx); if (b.idle) o.push('ip bfd idle-tx-interval ' + b.idle); if (b.mult) o.push('ip bfd multiplier ' + b.mult); });
  function addRoute(st, net, nh, ad) {
    var c = IP.parseCidr(net); if (!c || (ad !== undefined && (ad < 1 || ad > 255))) return 'Syntax error: Illegal parameter';
    var n2 = IP.netOf(c.ip, c.len); st.cand.routes = st.cand.routes.filter(function (r) { return !(r.net === n2 && r.nh === nh && !r.vrf); });
    st.cand.routes.push({ net: n2, nh: nh, ad: ad || 1, bfd: true }); touch(st);
  }
  S.cmd('config', 'ip route <w> <ip> bfd', function (st, a) { return addRoute(st, a[0], a[1]); }, 'Маршрут с проверкой next-hop по BFD');
  S.cmd('config', 'ip route <w> <ip> bfd <n>', function (st, a) { return addRoute(st, a[0], a[1], a[2]); });

  // сессия BFD с next-hop: сосед — включённый ESR, до которого доходит кадр в подключённой сети
  P.bfdUp = function (id, nh) {
    var s = this, k = id + '|' + nh, c = (s._bfdC = s._bfdC && s._bfdC.gen === s.gen ? s._bfdC : { gen: s.gen, t: {} });
    if (c.t[k] !== undefined) return c.t[k];
    c.t[k] = false;
    var out = routes0.call(s, id).filter(function (r) { return r.p === 'C'; }).map(function (r) { return r.ifn; });
    var f = s.ifaces(id).filter(function (x) { return out.indexOf(x.name) >= 0 && (x.port !== null || x.br || x.tun) && IP.sameNet(nh, x.ip, x.len); })[0];
    if (f) { var fl = s.flood(id, f, s.ifMac(id, f)), ep = fl.eps.filter(function (e) { return e.iface.ip === nh; })[0];
      c.t[k] = !!ep && s.devs[ep.dev].type === 'esr' && !s.devs[ep.dev].off; }
    return c.t[k];
  };
  var routes0 = P.routes;
  P.routes = function (id) {
    var s = this, r = routes0.apply(this, arguments);
    if (this.devs[id].type !== 'esr') return r;
    return r.map(function (x) { if (x.p === 'S' && x.bfd && !x.dead && !s.bfdUp(id, x.nh)) { var y = Object.assign({}, x); y.dead = true; y.bfdDown = true; return y; } return x; });
  };
  function sessions(s, id) { var c = s.devs[id].st.run, L = [];
    c.routes.forEach(function (r) { if (r.bfd && L.indexOf(r.nh) < 0) L.push(r.nh); }); return L; }
  function nbText(st, only) {
    var s = st.net; if (!s) return ''; var L = sessions(s, st.dev).filter(function (a) { return !only || a === only; });
    return L.map(function (nh) { var f = s.ifaces(st.dev).filter(function (x) { return IP.sameNet(nh, x.ip, x.len); })[0] || {}, up = s.bfdUp(st.dev, nh);
      return ['Neighbor address:                   ' + nh, 'Local address:                      ' + (f.ip || '--'), 'Interface:                          ' + (f.name || '--'),
        'Remote discriminator:               ' + (up ? parseInt(EL.E.hash(nh + 'r').slice(0, 8), 16) : 0), 'Local discriminator:                ' + parseInt(EL.E.hash(st.dev + nh).slice(0, 8), 16),
        'State:                              ' + (up ? 'Up' : 'Down')].join('\n'); }).join('\n\n');
  }
  S.cmd('priv', 'show bfd neighbors', function (st) { return nbText(st); }, 'Сессии BFD');
  S.cmd('priv', 'show bfd neighbors <ip>', function (st, a) { return nbText(st, a[0]); });
  S.cmd('priv', 'show ip bfd', function (st) { var c = cfg(st);
    return ['Minimum RX interval: ' + c.rx + ' ms', 'Minimum TX interval: ' + c.tx + ' ms', 'Idle TX interval:    ' + c.idle + ' ms', 'Multiplier:          ' + c.mult + ' packets', 'Passive:             No'].join('\n'); }, 'Параметры BFD');
  S.cmd('priv', 'clear bfd', function () { }, 'Перезапустить BFD');
  // сообщения о смене состояния сессий
  var events0 = P.events;
  P.events = function (quiet) {
    var out = events0.apply(this, arguments), s = this, now = {}, prev = s._bfdEv;
    s.order.forEach(function (id) { var d = s.devs[id]; if (d.type !== 'esr' || d.off) return; sessions(s, id).forEach(function (nh) { now[id + '|' + nh] = s.bfdUp(id, nh); }); });
    s._bfdEv = now;
    if (prev && !quiet) Object.keys(now).forEach(function (k) { if (prev[k] === undefined || prev[k] === now[k]) return; var q = k.split('|');
      if (s.devs[q[0]].st.run.logcon !== false) out.push({ id: q[0], msg: '%BFD-W-NEIG: Session to ' + q[1] + (now[k] ? ' Up' : ' Down') }); });
    return out;
  };
})(typeof window !== 'undefined' ? window : global);
