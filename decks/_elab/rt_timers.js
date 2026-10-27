/* RIP и OSPF по реальным таймерам (справочник ESR-Series CLI 1.23), время — модельное (net.now):
   RIP:  timers update 30 · invalid 180 · flush 240. Новые маршруты приходят сразу (request/response и триггерные обновления),
         а если сосед замолчал (выключен, RIP снят, обрыв за коммутатором) — маршрут через него живёт до invalid,
         потом «possibly down» (метрика 16) до flush. Свой интерфейс упал — маршруты через него уходят сразу.
   OSPF: ip ospf hello-interval 10 · dead-interval 40 (= 4×hello) · wait timer = dead · priority 128 · network broadcast|point-to-point.
         Соседство: init → 2way → (на broadcast-сегменте без DR — ожидание wait timer 40 с) → exstart → full.
         Hello/dead должны совпадать, иначе соседства нет. Сосед замолчал — остаётся full до истечения dead-interval. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, S = EL.esr, cmd = S.cmd, P = EL.Net.prototype;
  var RIP = { update: 30, invalid: 180 };

  function ripT(c, k) { var t = (c.rip && c.rip.timers) || {}; return k === 'flush' ? (t.flush || (t.invalid || RIP.invalid) + 60) : (t[k] || RIP[k]); }
  function ospfIf(c, ifn) { var o = (c.ifs[ifn] || {}).ospf || {}, h = o.hello || 10;
    return { hello: h, dead: o.dead || h * 4, prio: o.prio === undefined ? 128 : o.prio, net: o.net || 'broadcast' }; }
  function ifAlive(s, id, ifn) { return s.ifaces(id).some(function (f) { return f.name === ifn; }); }
  function rid(s, id) { var c = s.devs[id].st.run; return (c.ospf && c.ospf.rid) || (s.ifaces(id).map(function (f) { return f.ip; }).sort(function (a, b) { return IP.ip2n(b) - IP.ip2n(a); })[0] || '0.0.0.0'); }

  // ---------------------------------------------------------------- слой времени поверх расчёта соседств
  P.timeLayer = function (proto, rs, info, tab) {
    var s = this, now = s.now, A = (s._adj = s._adj || { R: {}, O: {} })[proto], seen = {}, run = {};
    rs.forEach(function (id) { run[id] = true; });
    rs.forEach(function (id) {
      info[id].nb.forEach(function (nb) {
        var k = id + '|' + nb.dev + '|' + nb.ifn; seen[k] = true;
        var r = A[k];
        if (!r || (r.lost !== undefined && now - r.lost >= deadOf(r))) r = A[k] = { id: id, dev: nb.dev, ifn: nb.ifn, nh: nb.nh, cost: nb.cost, since: now };
        delete r.lost; delete r.frozen; r.nh = nb.nh; r.cost = nb.cost;
      });
    });
    function deadOf(r) { var c = s.devs[r.id] && s.devs[r.id].st.run; if (!c) return 0;
      return proto === 'R' ? ripT(c, 'flush') : ospfIf(c, r.ifn).dead; }
    // соседи, от которых перестали приходить hello/update
    Object.keys(A).forEach(function (k) {
      if (seen[k]) return; var r = A[k];
      if (!run[r.id] || !ifAlive(s, r.id, r.ifn)) { delete A[k]; return; }   // свой интерфейс или процесс выключен — сразу
      if (proto === 'O' && r.state !== 'full') { delete A[k]; return; }
      if (r.lost === undefined) { r.lost = now; r.frozen = EL.clone(((s._lastTab || {})[proto] || {})[r.dev] || {}); }
      if (now - r.lost >= deadOf(r)) { delete A[k]; return; }
    });
    // какие соседства уже/ещё участвуют в расчёте
    rs.forEach(function (id) {
      var c = s.devs[id].st.run, keep = [];
      info[id].nb.forEach(function (nb) {
        var r = A[id + '|' + nb.dev + '|' + nb.ifn];
        if (proto === 'O') { r.state = ospfState(s, A, r); if (r.state !== 'full') return; }
        keep.push(nb);
      });
      Object.keys(A).forEach(function (k) { var r = A[k];
        if (r.id !== id || r.lost === undefined) return;
        var limit = proto === 'R' ? ripT(c, 'invalid') : ospfIf(c, r.ifn).dead;
        if (now - r.lost < limit) keep.push({ dev: r.dev, nh: r.nh, ifn: r.ifn, cost: r.cost, frozen: r.frozen });
      });
      info[id].nb = keep;
    });
  };
  // состояние соседа OSPF по времени с момента, когда соседство стало возможным
  function ospfState(s, A, r) {
    if (r.lost !== undefined) return r.state || 'full';
    var c = s.devs[r.id].st.run, t = ospfIf(c, r.ifn), e = s.now - r.since;
    if (e < 1) return 'init';
    if (t.net === 'point-to-point') return e < 2 ? 'exstart' : 'full';
    // на сегменте уже есть DR (кто-то из нас двоих уже в full на этом сегменте) — ожидание не нужно
    var dr = Object.keys(A).some(function (k) { var x = A[k]; return x !== r && x.state === 'full' &&
      ((x.id === r.id && x.ifn === r.ifn) || (x.id === r.dev && sameSeg(s, x, r))); });
    var wait = dr ? 1 : t.dead;
    if (e < wait) return '2way';
    return e < wait + 1 ? 'exstart' : 'full';
  }
  function sameSeg(s, x, r) {
    var f1 = s.ifaces(x.id).filter(function (f) { return f.name === x.ifn; })[0], f2 = s.ifaces(r.id).filter(function (f) { return f.name === r.ifn; })[0];
    return !!(f1 && f2 && f1.len === f2.len && IP.sameNet(f1.ip, f2.ip, f1.len));
  }
  // RIP: новый маршрут уходит соседям триггерным обновлением с задержкой 1–5 с (RFC 2453, 3.10.1) — по переходу на каждом роутере
  P.originAt = function (proto, id, n) {
    if (proto !== 'R') return 0; var o = (this._orig = this._orig || {}), k = id + '|' + n;
    if (o[k] === undefined) o[k] = this.now; return o[k];
  };
  function trigDelay(name) { var h = 0; for (var i = 0; i < name.length; i++) h = (h * 31 + name.charCodeAt(i)) >>> 0; return 1 + h % 5; }
  P.hopAt = function (proto, id, nb, ent) {
    if (proto !== 'R' || nb.frozen) return ent.at || 0;
    var r = ((this._adj || {}).R || {})[id + '|' + nb.dev + '|' + nb.ifn], since = r ? r.since : this.now;
    return Math.max(ent.at || 0, since) + trigDelay(this.devs[nb.dev].name);
  };
  // время тикает — пересчитываем соседства в момент до скачка, чтобы события не «опаздывали»
  var tick0 = P.tick;
  P.tick = function (dt) { this.dyn(); return tick0.call(this, dt); };

  // ---------------------------------------------------------------- роли DR/BDR на сегменте
  function roles(s, id, ifn) {
    var me = s.ifaces(id).filter(function (f) { return f.name === ifn; })[0]; if (!me) return {};
    var A = (s._adj || {}).O || {}, members = {}; members[id] = { prio: ospfIf(s.devs[id].st.run, ifn).prio, rid: rid(s, id) };
    Object.keys(A).forEach(function (k) { var x = A[k]; if (x.id !== id || x.ifn !== ifn || x.state !== 'full') return;
      var xc = s.devs[x.dev] && s.devs[x.dev].st.run; if (!xc) return;
      var xf = (s.ifaces(x.dev).filter(function (f) { return f.ip === x.nh; })[0] || {}).name;
      if (xf) { x.np = ospfIf(xc, xf).prio; x.rid = rid(s, x.dev); }      // запоминаем, пока сосед жив
      members[x.dev] = { prio: x.np === undefined ? 1 : x.np, rid: x.rid || rid(s, x.dev) }; });
    var order = Object.keys(members).filter(function (d) { return members[d].prio > 0; }).sort(function (a, b) {
      return members[b].prio - members[a].prio || IP.ip2n(members[b].rid) - IP.ip2n(members[a].rid); });
    var out = {}; Object.keys(members).forEach(function (d) { out[d] = 'drother'; });
    if (order[0]) out[order[0]] = 'dr'; if (order[1]) out[order[1]] = 'bdr';
    return out;
  }

  // ---------------------------------------------------------------- show ip ospf neighbors / interface
  function mmss(n) { n = Math.max(0, Math.ceil(n)); return ('0' + Math.floor(n / 60)).slice(-2) + ':' + ('0' + n % 60).slice(-2); }
  P.ospfNbrText = function (id) {
    var s = this; s.dyn(); var A = (s._adj || {}).O || {}, c = s.devs[id].st.run, rows = [];
    Object.keys(A).forEach(function (k) { var r = A[k]; if (r.id !== id) return;
      var t = ospfIf(c, r.ifn), rl = t.net === 'point-to-point' ? 'ptp' : (roles(s, id, r.ifn)[r.dev] || 'drother');
      var st = r.state === 'full' ? 'full/' + rl : r.state === '2way' ? '2way/' + (rl === 'dr' || rl === 'bdr' ? rl : 'other') : r.state;
      var dt = r.lost !== undefined ? t.dead - (s.now - r.lost) : t.dead - ((s.now - r.since) % t.hello);
      var nf = (s.ifaces(r.dev).filter(function (f) { return f.ip === r.nh; })[0] || {}).name;
      if (nf) { r.np = ospfIf(s.devs[r.dev].st.run, nf).prio; r.rid = rid(s, r.dev); }
      var np = r.np === undefined ? 1 : r.np;
      rows.push(((r.rid || rid(s, r.dev)) + '              ').slice(0, 13) + (np + '     ').slice(0, 5) + (st + '            ').slice(0, 12) +
                (mmss(dt) + '  ').slice(0, 7) + (r.ifn + '           ').slice(0, 11) + r.nh +
                (r.lost !== undefined ? '   ← hello не приходят, удаление через ' + Math.ceil(t.dead - (s.now - r.lost)) + ' с' : '') +
                (r.state === '2way' && t.net !== 'point-to-point' ? '   ← ожидание выбора DR (wait timer ' + t.dead + ' с), осталось ' + Math.ceil(t.dead - (s.now - r.since)) + ' с' : '')); });
    var mis = Object.keys(s._ospfMis || {}).filter(function (k) { return k.split('|')[0] === id; }).map(function (k) { var m = s._ospfMis[k];
      return '% ' + k.split('|')[1] + ': hello от ' + m.peer + ' отброшены — таймеры hello/dead ' + m.his.join('/') + ', а у нас ' + m.mine.join('/') + ' (должны совпадать)'; });
    if (!rows.length) return ['% Соседей OSPF нет'].concat(mis).join('\n');
    return ['Router ID    Pri  State       DTime  Interface  Router IP'].concat(rows, mis).join('\n');
  };
  function ospfIfText(st, w) {
    var s = st.net, c = st.run, id = st.dev, out = [];
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k], o = x.ospf; if (!o || !o.on) return;
      if (w && S.ifName(w) && S.ifName(w).name !== k) return;
      var t = ospfIf(c, k), f = s ? s.ifaces(id).filter(function (q) { return q.name === k; })[0] : null, rl = s ? roles(s, id, k)[id] : 'down';
      out.push('Interface:                ' + S.longIf(k), 'Internet Address:         ' + (x.ip || '-'), 'Router ID:                ' + (s ? rid(s, id) : '-'),
        'Network Type:             ' + t.net, 'Area:                     ' + (o.area || '-'), 'State:                    ' + (!f ? 'down' : t.net === 'point-to-point' ? 'ptp' : rl),
        'Priority:                 ' + t.prio, 'Cost:                     ' + (o.cost || 1), 'Hello timer:              ' + t.hello,
        'Wait timer:               ' + t.dead, 'Dead timer:               ' + t.dead, 'Retransmit timer:         5', ''); });
    return out.length ? out.join('\n') : '% OSPF не включён ни на одном интерфейсе';
  }
  cmd('priv', 'show ip ospf interface', function (st) { return ospfIfText(st); }, 'Интерфейсы OSPF и таймеры');
  cmd('priv', 'show ip ospf interface <w>', function (st, a) { return ospfIfText(st, a[0]); });

  // ---------------------------------------------------------------- show ip rip с таймерами
  function hms(n) { n = Math.floor(n); var p = function (v) { return ('0' + v).slice(-2); }; return p(Math.floor(n / 3600) % 24) + ':' + p(Math.floor(n / 60) % 60) + ':' + p(n % 60); }
  P.dynText = function (id, proto) {
    var s = this, rs = (this.dyn()[id] || []).filter(function (r) { return r.p === proto; }), c = s.devs[id].st.run, out = [];
    if (proto === 'R') {
      var A = (s._adj || {}).R || {}, upd = ripT(c, 'update');
      rs.forEach(function (r) { var a = A[id + '|' + r.via + '|' + r.ifn], last = a ? (a.lost !== undefined ? a.lost : a.since + Math.floor((s.now - a.since) / upd) * upd) : s.now;
        out.push(r.net + ' via ' + r.nh + ' on ' + r.ifn + ' [rip ' + hms(last) + '] * (' + r.ad + '/' + r.m + ')' +
          (r.stale ? '   ← обновлений нет ' + Math.floor(s.now - a.lost) + ' с, invalid через ' + Math.ceil(ripT(c, 'invalid') - (s.now - a.lost)) + ' с' : '')); });
      // истёк invalid, но не flush: маршрут не используется, анонсируется с метрикой 16
      Object.keys(A).forEach(function (k) { var a = A[k]; if (a.id !== id || a.lost === undefined || s.now - a.lost < ripT(c, 'invalid')) return;
        Object.keys(a.frozen || {}).forEach(function (n) { if (rs.some(function (r) { return r.net === n; }) || (c.ifs && s.ifaces(id).some(function (f) { return IP.netOf(f.ip, f.len) === n; }))) return;
          out.push(n + ' via ' + a.nh + ' on ' + a.ifn + ' [rip ' + hms(a.lost) + ']   (120/16) possibly down — удаление через ' + Math.ceil(ripT(c, 'flush') - (s.now - a.lost)) + ' с (flush)'); }); });
      if (!out.length) return '% Маршрутов RIP нет — проверьте enable, network и соседей';
      return out.join('\n') + '\nТаймеры: update ' + upd + ' · invalid ' + ripT(c, 'invalid') + ' · flush ' + ripT(c, 'flush') + ' с';
    }
    if (!rs.length) return '% Маршрутов OSPF нет — проверьте enable, network и соседей';
    return rs.map(function (r) { return proto + '  ' + (r.net + '                  ').slice(0, 19) + '[' + r.ad + '/' + r.m + '] via ' + r.nh + ' on ' + r.ifn; }).join('\n');
  };

  // ---------------------------------------------------------------- команды
  function touch(st) { st.pending = true; }
  function rip(st) { return st.cand.rip || (st.cand.rip = { on: false, nets: [], passive: [], redist: [] }); }
  ['update', 'invalid', 'flush'].forEach(function (k) {
    cmd('rip', 'timers ' + k + ' <n>', function (st, a) { if (a[0] < 12 || a[0] > 65535) return '% Допустимо 12..65535 с';
      var r = rip(st); r.timers = r.timers || {}; r.timers[k] = a[0]; touch(st); },
      { update: 'Период рассылки обновлений (30 с)', invalid: 'Через сколько без обновлений маршрут недействителен (180 с)', flush: 'Через сколько удалить маршрут (240 с)' }[k]);
    cmd('rip', 'no timers ' + k, function (st) { var r = rip(st); if (r.timers) delete r.timers[k]; touch(st); });
  });
  function eachO(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { var x = st.cand.ifs[k]; x.ospf = x.ospf || {}; f(x.ospf); }); touch(st); }
  cmd('gi sub', 'ip ospf hello-interval <n>', function (st, a) { if (a[0] < 1 || a[0] > 255) return '% Допустимо 1..255 с'; eachO(st, function (o) { o.hello = a[0]; }); }, 'Период hello (10 с)');
  cmd('gi sub', 'no ip ospf hello-interval', function (st) { eachO(st, function (o) { delete o.hello; }); });
  cmd('gi sub', 'ip ospf dead-interval <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return '% Допустимо 1..65535 с'; eachO(st, function (o) { o.dead = a[0]; }); }, 'Сосед считается потерянным без hello (40 с)');
  cmd('gi sub', 'no ip ospf dead-interval', function (st) { eachO(st, function (o) { delete o.dead; }); });
  cmd('gi sub', 'ip ospf priority <n>', function (st, a) { if (a[0] > 255) return '% Допустимо 0..255'; eachO(st, function (o) { o.prio = a[0]; }); }, 'Приоритет в выборах DR (128; 0 — никогда не DR)');
  cmd('gi sub', 'no ip ospf priority', function (st) { eachO(st, function (o) { delete o.prio; }); });
  ['broadcast', 'point-to-point'].forEach(function (t) {
    cmd('gi sub', 'ip ospf network ' + t, function (st) { eachO(st, function (o) { if (t === 'broadcast') delete o.net; else o.net = t; }); }, 'Тип сети OSPF');
  });
  cmd('gi sub', 'no ip ospf network', function (st) { eachO(st, function (o) { delete o.net; }); });
  S.RUNX.push(function (c, o) {
    if (c.rip && c.rip.timers) { var t = c.rip.timers, l = Object.keys(t).map(function (k) { return '  timers ' + k + ' ' + t[k]; });
      if (l.length) o.push('router rip', l.join('\n'), 'exit'); }
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k].ospf, d = []; if (!x) return;
      if (x.hello) d.push('  ip ospf hello-interval ' + x.hello); if (x.dead) d.push('  ip ospf dead-interval ' + x.dead);
      if (x.prio !== undefined) d.push('  ip ospf priority ' + x.prio); if (x.net) d.push('  ip ospf network ' + x.net);
      if (d.length) o.push('interface ' + S.longIf(k), d.join('\n'), 'exit'); });
  });
})(typeof window !== 'undefined' ? window : global);
