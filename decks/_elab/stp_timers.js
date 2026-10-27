/* STP/RSTP по таймерам: состояния портов во времени (модельные часы net.now, как aging.js и rt_timers.js).
   Роли портов считает P.stp (net.js) мгновенно; здесь — путь порта к forwarding:
     802.1D (mode stp/pvst, на 10.x — spanning-tree compatibility stp):
       blocking → listening (forward-time) → learning (forward-time) → forwarding;
       непрямой отказ (корневой порт жив, но корень пропал) — сначала ждём max-age, потом listening;
     RSTP/MSTP: порт между двумя RSTP-мостами по p2p — proposal/agreement, сразу forwarding;
       к мосту 802.1D или по shared — discarding (forward-time) → learning (forward-time) → forwarding;
     порт к конечному узлу: portfast (8.x — edgeport) — сразу; авто-определение (10.x spanning-tree auto-edge,
       6.x spanning-tree portfast auto — по умолчанию) — через 3 с без BPDU; иначе — по таймерам.
   Кадры идут только в forwarding; в learning MAC отправителя учится, кадр отбрасывается.
   Таймеры и ограничения — по руководствам MES 10.4.6, 6.6.8.8, 8.4.0.7:
     forward-time 4..30 (15), hello-time 1..10 (2; на 8.x глобальной команды нет), max-age 6..40 (20),
     2*(Forward-Delay - 1) >= Max-Age >= 2*(Hello-Time + 1).
   Упрощения: proposal/agreement — мгновенно (в железе — миллисекунды); TCN и сброс MAC-таблицы
   при смене топологии не моделируются; hello-time влияет только на вывод show. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, P = EL.Net.prototype, CMDS = E.CMDS;
  var FD = 15, MA = 20, HELLO = 2, EDGE_DELAY = 3;
  EL.STPN = { Frw: 'forwarding', Dsc: 'discarding', Lrn: 'learning', Blk: 'blocking', Lsn: 'listening' };

  P.stpTimers = function (st) { var s = st.stp || {}; return { fd: s.fd || FD, ma: s.ma || MA, hello: s.hello || HELLO }; };
  function legacy(st) { var s = st.stp || {}; return s.mode === 'stp' || s.mode === 'pvst' || s.compat === 'stp'; }
  function autoEdge(st, cfg) { return st.dialect !== '8' && !cfg.noAutoEdge; }
  function lp(net, id, ln) { return net.lports(id).filter(function (x) { return x.name === ln; })[0] || { cfg: {}, members: [ln] }; }

  // план перехода порта в forwarding: [[состояние, секунд], …]; пустой — сразу
  function plan(net, id, ln, r, prev, oldDev, newDev) {
    if (r.nostp) return [];
    var st = net.devs[id].st, L = lp(net, id, ln), cfg = L.cfg || {}, tm = net.stpTimers(st), leg = legacy(st);
    var wait = leg ? 'Lsn' : 'Dsc', timers = [[wait, tm.fd], ['Lrn', tm.fd]];
    if (cfg.portfast) return [];
    if (r.host) return autoEdge(st, cfg) ? [[wait, EDGE_DELAY]] : timers;
    var pr = net.peer(id, L.members[0]), peerLeg = pr ? legacy(net.devs[pr.dev].st) : false;
    if (!leg && !peerLeg && cfg.linkType !== 'shared') return [];          // proposal/agreement
    if (!leg) return timers;
    // 802.1D: заблокированный порт хранит BPDU соседа max-age; если свой корневой порт не падал (непрямой отказ),
    // худшие BPDU игнорируются, пока сохранённая информация не устареет, — затем listening/learning
    var oldRoot = Object.keys(oldDev || {}).filter(function (k) { return oldDev[k].role === 'Root'; })[0];
    if (prev && !prev.fwd && !(oldRoot && !newDev[oldRoot])) return [['Blk', tm.ma]].concat(timers);
    return timers;
  }
  function track(net, k, t) {
    var PS = net._ps || (net._ps = {}), old = PS[k] || {}, nw = {};
    Object.keys(t).forEach(function (id) {
      var o = old[id] || {}, n = nw[id] = {};
      Object.keys(t[id]).forEach(function (ln) {
        var r = t[id][ln], p = o[ln];
        if (p && p.fwd === r.fwd) { n[ln] = { fwd: p.fwd, role: r.role, t0: p.t0, plan: p.plan, leg: p.leg }; return; }
        n[ln] = { fwd: r.fwd, role: r.role, t0: net.now, plan: r.fwd ? plan(net, id, ln, r, p, o, t[id]) : [], leg: legacy(net.devs[id].st) };
      });
    });
    PS[k] = nw;
  }
  var stp0 = P.stp;
  P.stp = function (k) {
    k = k || 0; var c = k ? (this._stpK || {})[k] : this._stp, fresh = !(c && c.gen === this.gen);
    var t = stp0.call(this, k); if (fresh) track(this, k, t); return t;
  };
  function entry(net, id, ln, k) { net.stp(k); var e = ((net._ps || {})[k || 0] || {})[id]; return e ? e[ln] : null; }
  P.stpState = function (id, ln, k) {
    var e = entry(this, id, ln, k); if (!e) return null;
    if (!e.fwd) return e.leg ? 'Blk' : 'Dsc';
    var el = this.now - e.t0;
    for (var i = 0; i < e.plan.length; i++) { if (el < e.plan[i][1]) return e.plan[i][0]; el -= e.plan[i][1]; }
    return 'Frw';
  };
  P.stpLeft = function (id, ln, k) {
    var e = entry(this, id, ln, k); if (!e || !e.fwd) return 0;
    var all = e.plan.reduce(function (a, x) { return a + x[1]; }, 0); return Math.max(0, Math.ceil(all - (this.now - e.t0)));
  };
  P.stpSts = function (id, ln, k) { return this.stpState(id, ln, k) || 'Frw'; };
  P.stpType = function (id, L, r) { var c = L.cfg || {}, st = this.devs[id].st;
    var edge = c.portfast || (r.host && autoEdge(st, c));
    return (c.linkType === 'shared' ? 'Shr' : 'P2p') + (edge ? ' Edge' : '') + (legacy(st) ? ' (STP)' : ''); };

  // «кабели подключены давно»: текущие переходы считаются завершёнными (автотест собирает схему мгновенно)
  P.stpSettle = function () { this.stpSync(); var PS = this._ps || {};
    Object.keys(PS).forEach(function (k) { Object.keys(PS[k]).forEach(function (id) { Object.keys(PS[k][id]).forEach(function (ln) {
      var e = PS[k][id][ln]; PS[k][id][ln] = { fwd: e.fwd, role: e.role, t0: -1e9, plan: e.plan, leg: e.leg }; }); }); }); };
  // синхронизация: смена топологии фиксируется в момент модельного времени, когда она произошла
  P.stpSync = function () {
    var s = this, ks = { 0: 1 };
    this.order.forEach(function (id) { var st = s.devs[id].st; if (s.devs[id].type === 'mes' && st.mst && (st.stp || {}).mode === 'mst') Object.keys(st.mst.inst).forEach(function (k) { ks[k] = 1; }); });
    Object.keys(ks).forEach(function (k) { s.stp(+k); });
  };
  ['exec', 'connect', 'disconnect', 'power', 'remove'].forEach(function (m) { var f = P[m];
    P[m] = function () { var r = f.apply(this, arguments); this.stpSync(); return r; }; });
  var tick0 = P.tick;
  P.tick = function () {                         // состояние порта выводится из net.now − t0, поэтому прыжок часов не теряет переходов
    this.stpSync(); return tick0.apply(this, arguments);
  };

  // ---------------------------------------------------------------- команды MES
  function cmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function stp(st) { return st.stp || (st.stp = { on: true, mode: 'mst', prio: 32768 }); }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k] || (st.pos || {})[k]; }) : null; }
  function each(st, f) { var p = ports(st); if (!p) return '% Команда доступна в настройке порта'; p.forEach(f); if (st.net) st.net.gen++; }
  function setT(key, lo, hi) {
    return function (st, a) { var n = +a[0]; if (!/^\d+$/.test(a[0]) || n < lo || n > hi) return '% Допустимо ' + lo + '..' + hi;
      var s = stp(st), was = s[key]; s[key] = n; var tm = P.stpTimers(st);
      if (!(2 * (tm.fd - 1) >= tm.ma && tm.ma >= 2 * (tm.hello + 1))) { if (was === undefined) delete s[key]; else s[key] = was;
        return '% Нарушено условие 2*(Forward-Delay - 1) >= Max-Age >= 2*(Hello-Time + 1)'; } };
  }
  function unset(key) { return function (st) { var s = stp(st), was = s[key]; delete s[key]; var tm = P.stpTimers(st);
    if (!(2 * (tm.fd - 1) >= tm.ma && tm.ma >= 2 * (tm.hello + 1))) { s[key] = was; return '% Нарушено условие 2*(Forward-Delay - 1) >= Max-Age >= 2*(Hello-Time + 1)'; } }; }
  cmd(['10', '6', '8'], 'config', 'spanning-tree forward-time <w>', setT('fd', 4, 30), 'Forward Delay: время listening/learning, с (по умолчанию 15)');
  cmd(['10', '6', '8'], 'config', 'no spanning-tree forward-time', unset('fd'));
  cmd(['10', '6', '8'], 'config', 'spanning-tree max-age <w>', setT('ma', 6, 40), 'Max Age: время жизни BPDU-информации, с (по умолчанию 20)');
  cmd(['10', '6', '8'], 'config', 'no spanning-tree max-age', unset('ma'));
  cmd(['10', '6'], 'config', 'spanning-tree hello-time <w>', setT('hello', 1, 10), 'Hello Time: период BPDU, с (по умолчанию 2)');
  cmd(['10', '6'], 'config', 'no spanning-tree hello-time', unset('hello'));
  cmd(['10'], 'config', 'spanning-tree compatibility <w>', function (st, a) { var m = a[0].toLowerCase();
    if (['stp', 'rst', 'mst'].indexOf(m) < 0) return '% Режим совместимости: stp | rst | mst';
    if (m === 'stp') stp(st).compat = 'stp'; else delete stp(st).compat; }, 'Совместимость: stp — работать как 802.1D (таймеры)');
  cmd(['10'], 'config', 'no spanning-tree compatibility', function (st) { delete stp(st).compat; });
  cmd(['10'], 'if range', 'spanning-tree auto-edge', function (st) { return each(st, function (p) { delete p.noAutoEdge; }); }, 'Авто-определение клиентского порта (3 с без BPDU)');
  cmd(['10'], 'if range', 'no spanning-tree auto-edge', function (st) { return each(st, function (p) { p.noAutoEdge = true; }); });
  cmd(['6'], 'if range', 'spanning-tree portfast auto', function (st) { return each(st, function (p) { p.portfast = false; delete p.noAutoEdge; }); }, 'Portfast с задержкой 3 с (по умолчанию)');
  cmd(['8'], 'if range', 'spanning-tree edgeport', function (st) { return each(st, function (p) { p.portfast = true; }); }, 'Порт к конечному узлу: сразу в forwarding');
  cmd(['8'], 'if range', 'no spanning-tree edgeport', function (st) { return each(st, function (p) { p.portfast = false; }); });
  cmd(['10', '6'], 'if range', 'spanning-tree link-type <w>', function (st, a) { var m = a[0].toLowerCase();
    if (['point-to-point', 'shared'].indexOf(m) < 0) return '% Тип: point-to-point | shared';
    return each(st, function (p) { if (m === 'shared') p.linkType = 'shared'; else delete p.linkType; }); }, 'Тип связи: shared — без быстрого перехода RSTP');
  cmd(['10', '6'], 'if range', 'no spanning-tree link-type', function (st) { return each(st, function (p) { delete p.linkType; }); });

  E.RUNX.push(function (st, o) { var s = st.stp; if (!s) return;
    if (s.compat) o.push('spanning-tree compatibility ' + s.compat);
    if (s.fd) o.push('spanning-tree forward-time ' + s.fd);
    if (s.hello) o.push('spanning-tree hello-time ' + s.hello);
    if (s.ma) o.push('spanning-tree max-age ' + s.ma); });
  E.PORTX.push(function (st, k, p, d) {
    if (p.noAutoEdge) d.push(' no spanning-tree auto-edge');
    if (p.linkType) d.push(' spanning-tree link-type ' + p.linkType); });
})(typeof window !== 'undefined' ? window : global);
