/* RIPng и OSPFv3 на ESR (справочник ESR-Series CLI 1.23):
   RIPng — ipv6 router rip → (config-ripng)#: network X::/len, redistribute connected, enable; show ipv6 rip.
   OSPFv3 — ipv6 router ospf <ID> → (config-ipv6-ospf)#: router-id, area <ID> → (config-ipv6-ospf-area)#: enable; enable;
            на интерфейсе: ipv6 ospf instance <ID>, ipv6 ospf area <ID>, ipv6 ospf; show ipv6 ospf neighbors.
   Соседи — ESR в одном сегменте с адресами из одной IPv6-сети; next-hop — link-local соседа (как в RIPng/OSPFv3).
   Таймеры (модельное время net.now, как rt_timers.js для IPv4):
     RIPng — timers update 30 · invalid 180 · flush 240 (12..65535); новый маршрут — триггерное обновление 1–5 с на переход; сосед замолчал —
       маршрут живёт до invalid, затем «possibly down» (метрика 16) до flush; свой интерфейс упал — сразу.
     OSPFv3 — ipv6 ospf hello-interval 10 (1..255) · dead-interval 40 · wait-interval 40 · priority 120 (0..255) · network broadcast|point-to-point · cost;
       соседство init → 2way → (broadcast без DR — wait-interval) → exstart → full; hello/dead должны совпадать; сосед замолчал — full до dead.
   Упрощения: одна область OSPFv3; стоимость интерфейса по умолчанию 10 (auto-cost от полосы не считается); типы non-broadcast и point-to-multipoint
   не моделируются. */
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
      if (x.inst) d.push('  ipv6 ospf instance ' + x.inst); if (x.hello) d.push('  ipv6 ospf hello-interval ' + x.hello); if (x.dead) d.push('  ipv6 ospf dead-interval ' + x.dead); if (x.wait) d.push('  ipv6 ospf wait-interval ' + x.wait);
      if (x.prio !== undefined) d.push('  ipv6 ospf priority ' + x.prio); if (x.net) d.push('  ipv6 ospf network ' + x.net); if (x.cost) d.push('  ipv6 ospf cost ' + x.cost); if (x.area) d.push('  ipv6 ospf area ' + x.area); if (x.on) d.push('  ipv6 ospf');
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
        a.id = id; a.dev = nb.dev; a.ifn = nb.ifn; a.nh = nb.nh; a.his = nb.his; if (proto === 'O') a.full = s.now - a.since >= o6wait(s, Ad, a); return true; }); });
      Object.keys(Ad).forEach(function (k) { if (seenK[k]) return; var a = Ad[k]; if (a.lost === undefined) { a.lost = s.now;
          if (proto === 'R') (s._dead6 = s._dead6 || {})[k] = (((s._last6 || { R: {} }).R[a.id]) || []).filter(function (r) { return r.via === k; }); }
        if (s.now - a.lost >= (proto === 'R' ? flush(s, a.id) : hold(s, proto, a.id, a.ifn))) delete Ad[k]; });
      rs.forEach(function (id) { info[id].nb = info[id].nb.filter(function (nb) { var a = Ad[id + '|' + nb.dev + '|' + nb.ifn];
        return s.now - a.since >= (proto === 'O' ? o6wait(s, Ad, a) : trig(s.devs[nb.dev].name)); }); });
      // RIPng — вектор расстояний (метрика = переходы, 16 — недостижимо); OSPFv3 — кратчайший путь, стоимость интерфейса 10
      var step = proto === 'R' ? 1 : 10, lim = proto === 'R' ? 15 : 1e9, ad = proto === 'R' ? 120 : 110;
      rs.forEach(function (id) {
        var dist = {}, first = {}, q = [{ id: id, m: 0, via: null }], seen = {};
        while (q.length) { q.sort(function (a, b) { return a.m - b.m; }); var u = q.shift(); if (seen[u.id]) continue; seen[u.id] = true;
          if (u.id !== id) info[u.id].own.forEach(function (n) { if (dist[n] === undefined || u.m < dist[n]) { dist[n] = u.m; first[n] = u.via; } });
          info[u.id].nb.forEach(function (nb) { if (!info[nb.dev] || seen[nb.dev]) return;
            var back = info[nb.dev].nb.some(function (x) { return x.dev === u.id; }); if (!back) return;
            var st2 = proto === 'R' ? 1 : o6if(s, u.id, nb.ifn).cost;
            if (u.m + st2 <= lim) q.push({ id: nb.dev, m: u.m + st2, via: u.via || nb }); }); }
        var mine = s.ifaces6(id).filter(function (f) { return !f.ll; }).map(function (f) { return A.netOf(f.ip, f.len); });
        Object.keys(dist).forEach(function (n) { if (mine.indexOf(n) >= 0 || !first[n]) return;
          (t[id] = t[id] || []).push({ p: proto, net: n, len: +n.split('/')[1], nh: first[n].nh, ifn: first[n].ifn, ad: ad, m: proto === 'R' ? dist[n] + 1 : dist[n] + ownCost(s, n, info), via: id + '|' + first[n].dev + '|' + first[n].ifn }); });
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
  function o6if(s, id, ifn) { var x = (s.devs[id].st.run.ifs[ifn] || {}).ospf6 || {}, h = x.hello || 10, d = x.dead || h * 4;
    return { hello: h, dead: d, wait: x.wait || d, prio: x.prio === undefined ? 120 : x.prio, net: x.net || 'broadcast', cost: x.cost || 10 }; }
  // время до full: point-to-point — 2 с; broadcast — wait-interval, если на сегменте ещё нет DR (никто из двоих не в full на нём)
  function o6wait(s, Ad, a) { var t = o6if(s, a.id, a.ifn); if (t.net === 'point-to-point') return 2;
    var dr = Object.keys(Ad).some(function (k) { var x = Ad[k]; return x !== a && x.full && ((x.id === a.id && x.ifn === a.ifn) || (x.id === a.dev && x.ifn === a.his)); });
    return dr ? 2 : t.wait + 1; }
  // стоимость префикса = стоимость интерфейса, на котором он анонсирован (OSPFv3 intra-area prefix)
  function ownCost(s, n, info) { var c = 10; Object.keys(info).some(function (id) { return s.ifaces6(id).some(function (f) { if (!f.ll && A.netOf(f.ip, f.len) === n) { c = o6if(s, id, f.name).cost; return true; } return false; }); }); return c; }
  function timersOk(s, id, nb) { var a = o6if(s, id, nb.ifn), b = o6if(s, nb.dev, nb.his); return a.hello === b.hello && a.dead === b.dead; }
  function wait(s, id, ifn) { return o6if(s, id, ifn).dead; }
  function rt(s, id, k, d) { var r = s.devs[id] && s.devs[id].st.run.ripng; return (r && r.timers && r.timers[k]) || d; }
  function hold(s, proto, id, ifn) { return proto === 'O' ? o6if(s, id, ifn).dead : rt(s, id, 'invalid', 180); }
  function flush(s, id) { return rt(s, id, 'flush', rt(s, id, 'invalid', 180) + 60); }
  function trig(name) { var h = 0; for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0; return 1 + h % 5; }
  var tick0 = P.tick; P.tick = function () { this.dyn6(); return tick0.apply(this, arguments); };
  var ex6 = P.exec; P.exec = function () { this.dyn6(); return ex6.apply(this, arguments); };   // снимок до изменения: от него считаются invalid/dead
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
  function hms(n) { n = Math.max(0, Math.floor(n)); var p = function (v) { return ('0' + v).slice(-2); }; return p(Math.floor(n / 3600) % 24) + ':' + p(Math.floor(n / 60) % 60) + ':' + p(n % 60); }
  // RIPng: время последнего обновления от соседа; после invalid — «possibly down» (метрика 16) до flush
  S.cmd('priv', 'show ipv6 rip', function (st) { var s = st.net; if (!s) return ''; var rs = (s.dyn6()[st.dev] || []).filter(function (r) { return r.p === 'R'; }),
      Ad = (s._t6 || { R: {} }).R, upd = rt(s, st.dev, 'update', 30), out = [];
    rs.forEach(function (r) { var a = Ad[r.via], last = a ? (a.lost !== undefined ? a.lost : a.since + Math.floor((s.now - a.since) / upd) * upd) : s.now;
      out.push(rp(r.net, 16) + 'via ' + r.nh + ' on ' + r.ifn + ' [rip ' + hms(last) + '] * (120/' + r.m + ')' +
        (r.stale ? '   ← обновлений нет ' + Math.floor(s.now - a.lost) + ' с, invalid через ' + Math.ceil(rt(s, st.dev, 'invalid', 180) - (s.now - a.lost)) + ' с' : '')); });
    Object.keys(Ad).forEach(function (k) { var a = Ad[k]; if (a.id !== st.dev || a.lost === undefined || s.now - a.lost < rt(s, st.dev, 'invalid', 180)) return;
      (((s._dead6 || {})[k]) || []).forEach(function (r) { if (rs.some(function (x) { return x.net === r.net; })) return;
        out.push(rp(r.net, 16) + 'via ' + a.nh + ' on ' + a.ifn + ' [rip ' + hms(a.lost) + ']   (120/16) possibly down — удаление через ' + Math.ceil(flush(s, st.dev) - (s.now - a.lost)) + ' с (flush)'); }); });
    return out.join('\n'); }, 'Таблица маршрутов RIPng');
  // OSPFv3: роли DR/BDR на сегменте — наибольший priority, затем router-id; priority 0 — никогда не DR
  function roles6(s, Ad, id, ifn) { var m = {}; m[id] = { p: o6if(s, id, ifn).prio, r: rid(s, id) };
    Object.keys(Ad).forEach(function (k) { var a = Ad[k]; if (a.id !== id || a.ifn !== ifn || !a.full) return; m[a.dev] = { p: o6if(s, a.dev, a.his).prio, r: rid(s, a.dev) }; });
    var o = Object.keys(m).filter(function (d) { return m[d].p > 0; }).sort(function (x, y) { return m[y].p - m[x].p || IP.ip2n(m[y].r) - IP.ip2n(m[x].r); }), out = {};
    Object.keys(m).forEach(function (d) { out[d] = 'drother'; }); if (o[0]) out[o[0]] = 'dr'; if (o[1]) out[o[1]] = 'bdr'; return out; }
  S.cmd('priv', 'show ipv6 ospf neighbors', function (st) { var s = st.net; if (!s) return ''; s.dyn6();
    var Ad = (s._t6 || { O: {} }).O, L = Object.keys(Ad).map(function (k) { return Ad[k]; }).filter(function (a) { return a.id === st.dev; }); if (!L.length) return '';
    function mmss(n) { n = Math.max(0, Math.ceil(n)); return ('0' + Math.floor(n / 60)).slice(-2) + ':' + ('0' + n % 60).slice(-2); }
    return ['Router ID        Pri  State           DTime  Interface  Router IP'].concat(L.map(function (a) { var t = o6if(s, st.dev, a.ifn), w = s.now - a.since, need = o6wait(s, Ad, a);
      var rl = t.net === 'point-to-point' ? 'ptp' : roles6(s, Ad, st.dev, a.ifn)[a.dev] || 'drother';
      var stt = a.lost !== undefined || a.full ? 'full/' + rl : w < 1 ? 'init' : w >= need - 1 ? 'exstart' : '2way' + (rl === 'dr' || rl === 'bdr' ? '/' + rl : '/other');
      var dt = a.lost !== undefined ? t.dead - (s.now - a.lost) : t.dead - (w % t.hello);
      return rp(rid(s, a.dev), 17) + rp(o6if(s, a.dev, a.his || a.ifn).prio, 5) + rp(stt, 16) + rp(mmss(dt), 7) + rp(a.ifn, 11) + a.nh +
        (a.lost !== undefined ? '   ← hello не приходят, удаление через ' + Math.ceil(t.dead - (s.now - a.lost)) + ' с' : '') +
        (!a.full && a.lost === undefined && t.net !== 'point-to-point' ? '   ← ожидание выбора DR (wait-interval ' + t.wait + ' с), осталось ' + Math.max(0, Math.ceil(need - w)) + ' с' : ''); })).join('\n'); }, 'Соседи OSPFv3');
  function each6(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k].ospf6 = st.cand.ifs[k].ospf6 || {}); }); touch(st); }
  [['hello-interval', 'hello', 1, 255, 'Интервал hello OSPFv3, с (10)'], ['dead-interval', 'dead', 1, 65535, 'Интервал dead OSPFv3, с (40)'],
   ['wait-interval', 'wait', 1, 65535, 'Ожидание выбора DR, с (40)'], ['priority', 'prio', 0, 255, 'Приоритет в выборах DR (120; 0 — никогда)'], ['cost', 'cost', 1, 65535, 'Стоимость интерфейса']].forEach(function (c) {
    S.cmd('gi sub lo', 'ipv6 ospf ' + c[0] + ' <n>', function (st, a) { if (a[0] < c[2] || a[0] > c[3]) return 'Syntax error: Illegal parameter'; each6(st, function (o) { o[c[1]] = a[0]; }); }, c[4]);
    S.cmd('gi sub lo', 'no ipv6 ospf ' + c[0], function (st) { each6(st, function (o) { delete o[c[1]]; }); }); });
  S.cmd('gi sub lo', 'ipv6 ospf network <w>', function (st, a) { var t = a[0].toLowerCase(); if (['broadcast', 'point-to-point'].indexOf(t) < 0) return 'Syntax error: Illegal parameter';
    each6(st, function (o) { if (t === 'broadcast') delete o.net; else o.net = t; }); }, 'Тип сети OSPFv3: broadcast | point-to-point');
  S.cmd('gi sub lo', 'no ipv6 ospf network', function (st) { each6(st, function (o) { delete o.net; }); });
  ['update', 'invalid', 'flush'].forEach(function (k) {
    S.cmd('ripng', 'timers ' + k + ' <n>', function (st, a) { if (a[0] < 12 || a[0] > 65535) return 'Syntax error: Illegal parameter'; var r = rng(st); (r.timers = r.timers || {})[k] = a[0]; touch(st); },
      { update: 'Период обновлений RIPng, с (30)', invalid: 'Маршрут недействителен без обновлений, с (180)', flush: 'Удаление маршрута, с (240)' }[k]);
    S.cmd('ripng', 'no timers ' + k, function (st) { var r = rng(st); if (r.timers) delete r.timers[k]; touch(st); }); });
})(typeof window !== 'undefined' ? window : global);
