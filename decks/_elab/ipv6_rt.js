/* RIPng и OSPFv3 на ESR (справочник ESR-Series CLI 1.23):
   RIPng — ipv6 router rip → (config-ripng)#: network X::/len, redistribute connected, enable; show ipv6 rip.
   OSPFv3 — ipv6 router ospf <ID> → (config-ipv6-ospf)#: router-id, area <ID> → (config-ipv6-ospf-area)#: enable; enable;
            на интерфейсе: ipv6 ospf instance <ID>, ipv6 ospf area <ID>, ipv6 ospf; show ipv6 ospf neighbors.
   Соседи — ESR в одном сегменте с адресами из одной IPv6-сети; next-hop — link-local соседа (как в RIPng/OSPFv3).
   Упрощение: маршруты сходятся сразу (таймеры RIPng/OSPFv3 не моделируются), одна область OSPFv3, стоимость интерфейса 10. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, A = EL.ip6, IP = EL.ip;
  S.PROMPT.ripng = '(config-ripng)#'; S.PROMPT.o6 = '(config-ipv6-ospf)#'; S.PROMPT.o6a = '(config-ipv6-ospf-area)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('ripng', 'o6', 'o6a'); });
  function touch(st) { st.pending = true; }
  function each(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }

  // ---------------------------------------------------------------- RIPng
  function rng(st) { return st.cand.ripng || (st.cand.ripng = { on: false, nets: [], redist: [] }); }
  S.cmd('config', 'ipv6 router rip', function (st) { rng(st); touch(st); st.mode = 'ripng'; st.ctx = null; }, 'Настройка RIPng');
  S.cmd('config', 'no ipv6 router rip', function (st) { st.cand.ripng = null; touch(st); });
  S.cmd('ripng', 'network <w>', function (st, a) { var c = A.cidr(a[0]); if (!c) return 'Syntax error: Illegal parameter';
    var r = rng(st), v = A.netOf(c.ip, c.len); if (r.nets.indexOf(v) < 0) r.nets.push(v); touch(st); }, 'Анонсировать подсеть');
  S.cmd('ripng', 'no network <w>', function (st, a) { var c = A.cidr(a[0]), r = rng(st); if (c) r.nets = r.nets.filter(function (x) { return x !== A.netOf(c.ip, c.len); }); touch(st); });
  S.cmd('ripng', 'redistribute connected', function (st) { var r = rng(st); if (r.redist.indexOf('connected') < 0) r.redist.push('connected'); touch(st); }, 'Анонсировать подключённые');
  S.cmd('ripng', 'no redistribute connected', function (st) { var r = rng(st); r.redist = r.redist.filter(function (x) { return x !== 'connected'; }); touch(st); });
  S.cmd('ripng', 'enable', function (st) { rng(st).on = true; touch(st); }, 'Запустить RIPng');
  S.cmd('ripng', 'no enable', function (st) { rng(st).on = false; touch(st); });
  S.cmd('ripng o6 o6a', 'exit', function (st) { st.mode = st.mode === 'o6a' ? 'o6' : 'config'; if (st.mode === 'config') st.ctx = null; });

  // ---------------------------------------------------------------- OSPFv3
  function o6(st) { return st.cand.ospf6; }
  S.cmd('config', 'ipv6 router ospf <n>', function (st, a) {
    if (!st.cand.ospf6 || st.cand.ospf6.id !== a[0]) st.cand.ospf6 = { id: a[0], on: false, rid: null, areas: {} };
    touch(st); st.mode = 'o6'; st.ctx = null; }, 'Настройка OSPFv3');
  S.cmd('config', 'no ipv6 router ospf <n>', function (st, a) { if (st.cand.ospf6 && st.cand.ospf6.id === a[0]) st.cand.ospf6 = null; touch(st); });
  S.cmd('o6', 'router-id <ip>', function (st, a) { o6(st).rid = a[0]; touch(st); }, 'Идентификатор маршрутизатора');
  S.cmd('o6', 'area <ip>', function (st, a) { var o = o6(st); o.areas[a[0]] = o.areas[a[0]] || { on: false }; st.mode = 'o6a'; st.ctx = a[0]; touch(st); }, 'Область OSPFv3');
  S.cmd('o6a', 'enable', function (st) { o6(st).areas[st.ctx].on = true; touch(st); }, 'Активировать область');
  S.cmd('o6a', 'no enable', function (st) { o6(st).areas[st.ctx].on = false; touch(st); });
  S.cmd('o6', 'enable', function (st) { o6(st).on = true; touch(st); }, 'Запустить OSPFv3');
  S.cmd('o6', 'no enable', function (st) { o6(st).on = false; touch(st); });
  S.cmd('gi sub lo', 'ipv6 ospf instance <n>', function (st, a) { each(st, function (x) { (x.ospf6 = x.ospf6 || {}).inst = a[0]; }); }, 'Процесс OSPFv3 на интерфейсе');
  S.cmd('gi sub lo', 'ipv6 ospf area <ip>', function (st, a) { each(st, function (x) { (x.ospf6 = x.ospf6 || {}).area = a[0]; }); }, 'Область OSPFv3 интерфейса');
  S.cmd('gi sub lo', 'ipv6 ospf', function (st) { each(st, function (x) { (x.ospf6 = x.ospf6 || {}).on = true; }); }, 'Включить OSPFv3 на интерфейсе');
  S.cmd('gi sub lo', 'no ipv6 ospf', function (st) { each(st, function (x) { if (x.ospf6) x.ospf6.on = false; }); });

  S.RUNX.push(function (c, o) {
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k].ospf6; if (!x) return; var d = [];
      if (x.inst) d.push('  ipv6 ospf instance ' + x.inst); if (x.area) d.push('  ipv6 ospf area ' + x.area); if (x.on) d.push('  ipv6 ospf');
      if (d.length) o.push('interface ' + S.longIf(k), d.join('\n'), 'exit'); });
    if (c.ripng) { o.push('ipv6 router rip'); c.ripng.nets.forEach(function (n) { o.push('  network ' + n); });
      c.ripng.redist.forEach(function (n) { o.push('  redistribute ' + n); }); if (c.ripng.on) o.push('  enable'); o.push('exit'); }
    if (c.ospf6) { o.push('ipv6 router ospf ' + c.ospf6.id); if (c.ospf6.rid) o.push('  router-id ' + c.ospf6.rid);
      Object.keys(c.ospf6.areas).forEach(function (k) { o.push('  area ' + k); if (c.ospf6.areas[k].on) o.push('    enable'); o.push('  exit'); });
      if (c.ospf6.on) o.push('  enable'); o.push('exit'); }
  });

  // ---------------------------------------------------------------- расчёт
  // интерфейсы, на которых работает протокол: RIPng — адрес попадает в network; OSPFv3 — ipv6 ospf + instance = процесс + активная область
  function active(s, id, proto) {
    var d = s.devs[id]; if (d.type !== 'esr' || d.off) return [];
    var c = d.st.run, fs = s.ifaces6(id).filter(function (f) { return !f.ll; });
    if (proto === 'R') { var r = c.ripng; if (!r || !r.on) return [];
      return fs.filter(function (f) { return r.nets.some(function (n) { var q = n.split('/'); return +q[1] <= f.len && A.same(f.ip, q[0], +q[1]); }); }); }
    var o = c.ospf6; if (!o || !o.on || !rid(s, id)) return [];
    return fs.filter(function (f) { var x = (c.ifs[f.name] || {}).ospf6; return x && x.on && (!x.inst || x.inst === o.id) && o.areas[x.area || '0.0.0.0'] && o.areas[x.area || '0.0.0.0'].on; });
  }
  function rid(s, id) { var c = s.devs[id].st.run; return (c.ospf6 && c.ospf6.rid) || (s.ifaces(id).map(function (f) { return f.ip; }).sort(function (a, b) { return IP.ip2n(b) - IP.ip2n(a); })[0] || null); }
  // соседи по сегменту: кадр с интерфейса доходит до интерфейса другого ESR с адресом из той же сети
  function nbrs(s, id, proto, act) {
    var out = [];
    act.forEach(function (f) { if (f.port === null) return;
      var fl = s.flood(id, f, s.ifMac(id, f));
      fl.reach.forEach(function (e) { if (e.dev === id) return;
        var mine = active(s, e.dev, proto).filter(function (g) { return g.port === e.port && g.tag === e.tag && g.len === f.len && A.same(g.ip, f.ip, f.len); })[0];
        if (!mine) return; var ll = s.ifaces6(e.dev).filter(function (g) { return g.ll && g.name === mine.name; })[0];
        if (ll && !out.some(function (x) { return x.dev === e.dev && x.ifn === f.name; })) out.push({ dev: e.dev, ifn: f.name, nh: ll.ip, his: mine.name }); }); });
    return out;
  }
  function originated(s, id, proto) {
    var act = active(s, id, proto), o = act.map(function (f) { return A.netOf(f.ip, f.len); });
    if (proto === 'R' && s.devs[id].st.run.ripng.redist.indexOf('connected') >= 0) s.ifaces6(id).forEach(function (f) { if (!f.ll) o.push(A.netOf(f.ip, f.len)); });
    return o.filter(function (v, i, a) { return a.indexOf(v) === i; });
  }
  P.dyn6 = function () {
    if (this._dyn6 && this._dyn6.gen === this.gen) return this._dyn6.t;
    var s = this, t = {}, N = {};
    s.gen0 = s.gen;
    ['R', 'O'].forEach(function (proto) {
      var rs = s.order.filter(function (id) { return active(s, id, proto).length; });
      var info = {}; rs.forEach(function (id) { info[id] = { nb: nbrs(s, id, proto, active(s, id, proto)), own: originated(s, id, proto) }; N[proto + id] = info[id].nb; });
      // RIPng — вектор расстояний (метрика = переходы, 16 — недостижимо); OSPFv3 — кратчайший путь, стоимость интерфейса 10
      var step = proto === 'R' ? 1 : 10, lim = proto === 'R' ? 15 : 1e9, ad = proto === 'R' ? 120 : 110;
      rs.forEach(function (id) {
        var dist = {}, first = {}, q = [{ id: id, m: 0, via: null }], seen = {};
        while (q.length) { q.sort(function (a, b) { return a.m - b.m; }); var u = q.shift(); if (seen[u.id]) continue; seen[u.id] = true;
          if (u.id !== id) info[u.id].own.forEach(function (n) { if (dist[n] === undefined || u.m < dist[n]) { dist[n] = u.m; first[n] = u.via; } });
          info[u.id].nb.forEach(function (nb) { if (!info[nb.dev] || seen[nb.dev]) return;
            var back = info[nb.dev].nb.some(function (x) { return x.dev === u.id; }); if (!back) return;
            if (u.m + step <= lim) q.push({ id: nb.dev, m: u.m + step, via: u.via || nb }); }); }
        var mine = s.ifaces6(id).filter(function (f) { return !f.ll; }).map(function (f) { return A.netOf(f.ip, f.len); });
        Object.keys(dist).forEach(function (n) { if (mine.indexOf(n) >= 0 || !first[n]) return;
          (t[id] = t[id] || []).push({ p: proto, net: n, len: +n.split('/')[1], nh: first[n].nh, ifn: first[n].ifn, ad: ad, m: proto === 'R' ? dist[n] + 1 : dist[n] + 10 }); });
      });
    });
    this._dyn6 = { gen: this.gen, t: t, nb: N };
    return t;
  };
  var routes0 = P.routes6;
  P.routes6 = function (id) { return routes0.call(this, id).concat(this.devs[id].type === 'esr' ? this.dyn6()[id] || [] : []); };
  P.lookup6 = (function (lk0) { return function (id, dst) {
    var s = this; if (A.isLL(dst)) return lk0.call(this, id, dst);
    var fs = this.ifaces6(id), best = null;
    this.routes6(id).forEach(function (r) { if (r.dead || !A.same(dst, r.net.split('/')[0], r.len)) return;
      if (!best || r.len > best.len || (r.len === best.len && (r.ad || 0) < (best.ad || 0))) best = r; });
    if (!best) return null; void s;
    var out = fs.filter(function (f) { return f.name === best.ifn && (best.nh && A.isLL(best.nh) ? f.ll : !f.ll); })[0] || fs.filter(function (f) { return f.name === best.ifn; })[0];
    return out ? { iface: out, nh: best.nh || dst, r: best } : null; }; })(P.lookup6);

  // ---------------------------------------------------------------- show
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  S.cmd('priv', 'show ipv6 rip', function (st) { var s = st.net; if (!s) return '';
    return (s.dyn6()[st.dev] || []).filter(function (r) { return r.p === 'R'; }).map(function (r) {
      return rp(r.net, 16) + 'via ' + r.nh + ' on ' + r.ifn + ' [rip 00:00:00] * (120/' + r.m + ')'; }).join('\n'); }, 'Таблица маршрутов RIPng');
  S.cmd('priv', 'show ipv6 ospf neighbors', function (st) { var s = st.net; if (!s) return ''; s.dyn6();
    var L = (s._dyn6.nb['O' + st.dev] || []); if (!L.length) return '';
    return ['Router ID        Pri  State           DTime  Interface  Router IP'].concat(L.map(function (nb) {
      return rp(rid(s, nb.dev), 17) + '1    ' + rp('full/ptp', 16) + '00:40  ' + rp(nb.ifn, 11) + nb.nh; })).join('\n'); }, 'Соседи OSPFv3');
})(typeof window !== 'undefined' ? window : global);
