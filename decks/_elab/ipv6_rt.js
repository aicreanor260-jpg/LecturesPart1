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
      if (x.inst) d.push('  ipv6 ospf instance ' + x.inst); if (x.hello) d.push('  ipv6 ospf hello-interval ' + x.hello); if (x.dead) d.push('  ipv6 ospf dead-interval ' + x.dead); if (x.area) d.push('  ipv6 ospf area ' + x.area); if (x.on) d.push('  ipv6 ospf');
      if (d.length) o.push('interface ' + S.longIf(k), d.join('\n'), 'exit'); });
    if (c.ripng) { o.push('ipv6 router rip'); c.ripng.nets.forEach(function (n) { o.push('  network ' + n); });
      c.ripng.redist.forEach(function (n) { o.push('  redistribute ' + n); }); Object.keys(c.ripng.timers || {}).forEach(function (k) { o.push('  timers ' + k + ' ' + c.ripng.timers[k]); }); if (c.ripng.on) o.push('  enable'); o.push('exit'); }
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
    if (this._dyn6 && this._dyn6.gen === this.gen && this._dyn6.now === this.now) return this._dyn6.t;
    var s = this, t = {}, N = {};
    s.gen0 = s.gen;
    ['R', 'O'].forEach(function (proto) {
      var rs = s.order.filter(function (id) { return active(s, id, proto).length; });
      var info = {}; rs.forEach(function (id) { info[id] = { nb: nbrs(s, id, proto, active(s, id, proto)), own: originated(s, id, proto) }; N[proto + id] = info[id].nb; });
      // время: OSPFv3 — соседство Full через wait timer (= dead), RIPng — триггерное обновление 1–5 с; пропавший сосед держится dead / invalid
      var Ad = (s._t6 = s._t6 || { R: {}, O: {} })[proto], seenK = {};
      rs.forEach(function (id) { info[id].nb = info[id].nb.filter(function (nb) { var k = id + '|' + nb.dev + '|' + nb.ifn;
        if (proto === 'O' && !timersOk(s, id, nb)) { (s._o6mis = s._o6mis || {})[k] = true; return false; } if (s._o6mis) delete s._o6mis[k];
        seenK[k] = 1; var a = Ad[k]; if (!a) a = Ad[k] = { since: s.now };
        if (a.lost !== undefined) { if (s.now - a.lost >= hold(s, proto, id, nb.ifn)) a.since = s.now; delete a.lost; }
        a.id = id; a.dev = nb.dev; a.ifn = nb.ifn; a.nh = nb.nh; return true; }); });
      Object.keys(Ad).forEach(function (k) { if (seenK[k]) return; var a = Ad[k]; if (a.lost === undefined) a.lost = s.now;
        if (s.now - a.lost >= (proto === 'R' ? flush(s, a.id) : hold(s, proto, a.id, a.ifn))) delete Ad[k]; });
      rs.forEach(function (id) { info[id].nb = info[id].nb.filter(function (nb) { var a = Ad[id + '|' + nb.dev + '|' + nb.ifn];
        return s.now - a.since >= (proto === 'O' ? wait(s, id, nb.ifn) : trig(s.devs[nb.dev].name)); }); });
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
          (t[id] = t[id] || []).push({ p: proto, net: n, len: +n.split('/')[1], nh: first[n].nh, ifn: first[n].ifn, ad: ad, m: proto === 'R' ? dist[n] + 1 : dist[n] + 10, via: id + '|' + first[n].dev + '|' + first[n].ifn }); });
        // маршруты через пропавшего соседа живут до истечения таймера (RIPng invalid, OSPFv3 dead)
        var L6 = (s._last6 = s._last6 || { R: {}, O: {} })[proto], prev = L6[id] || [];
        prev.forEach(function (r) { var a = Ad[r.via]; if (!a || a.lost === undefined || s.now - a.lost >= hold(s, proto, id, a.ifn)) return;
          if ((t[id] || []).some(function (x) { return x.net === r.net && x.p === proto; })) return;
          if (!s.ifaces6(id).some(function (f) { return f.name === r.ifn; })) return;
          var g = Object.assign({}, r); g.stale = true; (t[id] = t[id] || []).push(g); });
        L6[id] = (t[id] || []).filter(function (x) { return x.p === proto; });
      });
    });
    this._dyn6 = { gen: this.gen, now: this.now, t: t, nb: N };
    return t;
  };
  // таймеры по справочнику: OSPFv3 hello 10 / dead 40 (wait = dead), RIPng update 30 / invalid 180 / flush 240
  function o6if(s, id, ifn) { var x = (s.devs[id].st.run.ifs[ifn] || {}).ospf6 || {}, h = x.hello || 10; return { hello: h, dead: x.dead || h * 4 }; }
  function timersOk(s, id, nb) { var a = o6if(s, id, nb.ifn), b = o6if(s, nb.dev, nb.his); return a.hello === b.hello && a.dead === b.dead; }
  function wait(s, id, ifn) { return o6if(s, id, ifn).dead; }
  function rt(s, id, k, d) { var r = s.devs[id] && s.devs[id].st.run.ripng; return (r && r.timers && r.timers[k]) || d; }
  function hold(s, proto, id, ifn) { return proto === 'O' ? o6if(s, id, ifn).dead : rt(s, id, 'invalid', 180); }
  function flush(s, id) { return rt(s, id, 'flush', rt(s, id, 'invalid', 180) + 60); }
  function trig(name) { var h = 0; for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0; return 1 + h % 5; }
  var tick0 = P.tick; P.tick = function () { this.dyn6(); return tick0.apply(this, arguments); };
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
    var Ad = (s._t6 || { O: {} }).O, L = Object.keys(Ad).map(function (k) { return Ad[k]; }).filter(function (a) { return a.id === st.dev; }); if (!L.length) return '';
    function mmss(n) { n = Math.max(0, Math.ceil(n)); return ('0' + Math.floor(n / 60)).slice(-2) + ':' + ('0' + n % 60).slice(-2); }
    return ['Router ID        Pri  State           DTime  Interface  Router IP'].concat(L.map(function (a) { var t = o6if(s, st.dev, a.ifn), w = s.now - a.since;
      var stt = a.lost !== undefined ? 'full' : w >= t.dead ? 'full' : w >= 1 ? '2way' : 'init';
      var dt = a.lost !== undefined ? t.dead - (s.now - a.lost) : t.dead - (w % t.hello);
      return rp(rid(s, a.dev), 17) + '1    ' + rp(stt + (stt === 'full' ? '/dr' : ''), 16) + rp(mmss(dt), 7) + rp(a.ifn, 11) + a.nh; })).join('\n'); }, 'Соседи OSPFv3');
  S.cmd('gi sub lo', 'ipv6 ospf hello-interval <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return 'Syntax error: Illegal parameter';
    (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { (st.cand.ifs[k].ospf6 = st.cand.ifs[k].ospf6 || {}).hello = a[0]; }); touch(st); }, 'Интервал hello OSPFv3');
  S.cmd('gi sub lo', 'ipv6 ospf dead-interval <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return 'Syntax error: Illegal parameter';
    (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { (st.cand.ifs[k].ospf6 = st.cand.ifs[k].ospf6 || {}).dead = a[0]; }); touch(st); }, 'Интервал dead OSPFv3');
  ['update', 'invalid', 'flush'].forEach(function (k) { S.cmd('ripng', 'timers ' + k + ' <n>', function (st, a) { var r = rng(st); (r.timers = r.timers || {})[k] = a[0]; touch(st); }, 'Таймер ' + k + ' RIPng'); });
})(typeof window !== 'undefined' ? window : global);
