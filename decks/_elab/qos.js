/* QoS на ESR (справочник ESR-Series CLI 1.23, MQC): классификация, маркировка, ограничение и сглаживание полосы.
   class-map NAME → (config-class-map)#: match access-group ACL · match dscp N · set dscp N
   policy-map NAME → (config-policy-map)#: shape average КБИТ/С [BURST] (на весь интерфейс) · class NAME → (config-class-policy-map)#:
     set dscp N · police КБИТ/С [burst-conforming БАЙТ] [conform-action transmit] [exceed-action drop | set-dscp-transmit N] · shape average КБИТ/С [BURST]
   интерфейс: service-policy input|output NAME (qos enable — хранится).
   Действует в «Симуляции трафика» (sim.js): пакет классифицируется по ACL (протокол, адреса, порт) и DSCP; police — корзина маркеров
   (burst-conforming по умолчанию 1500 байт): лишнее отбрасывается или перемаркируется; shape — пакеты ждут, пока полоса не позволит
   (burst по умолчанию 128000 байт). Маркировка (set dscp) едет с пакетом дальше и видна следующим маршрутизаторам.
   Упрощения: очереди по приоритету (priority-queue, WRR, bandwidth) не моделируются; ping/трасса в консоли QoS не учитывают — только симуляция. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr;
  function touch(st) { st.pending = true; }
  function bad() { return 'Syntax error: Illegal parameter'; }
  var PR = { cmap: '(config-class-map)#', pmap: '(config-policy-map)#', pcls: '(config-class-policy-map)#' };
  Object.keys(PR).forEach(function (k) { S.PROMPT[k] = PR[k]; });
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('cmap', 'pmap', 'pcls'); });
  function Q(st) { return st.cand.qos || (st.cand.qos = { cmaps: {}, pmaps: {} }); }
  function cm(st) { return Q(st).cmaps[st.ctx]; }
  function pc(st) { var p = st.ctx.split('|'); return Q(st).pmaps[p[0]].cls[p[1]]; }
  function pm(st) { return Q(st).pmaps[st.ctx.split('|')[0]]; }
  S.cmd('config', 'class-map <w>', function (st, a) { var C = Q(st).cmaps; C[a[0]] = C[a[0]] || { acl: [], dscp: [] }; st.mode = 'cmap'; st.ctx = a[0]; touch(st); }, 'Класс трафика (QoS)');
  S.cmd('config', 'no class-map <w>', function (st, a) { delete Q(st).cmaps[a[0]]; touch(st); });
  S.cmd('cmap', 'match access-group <w>', function (st, a) { if (cm(st).acl.indexOf(a[0]) < 0) cm(st).acl.push(a[0]); touch(st); }, 'Пакеты, разрешённые списком доступа');
  S.cmd('cmap', 'no match access-group <w>', function (st, a) { cm(st).acl = a[0] === 'all' ? [] : cm(st).acl.filter(function (x) { return x !== a[0]; }); touch(st); });
  S.cmd('cmap', 'match dscp <n>', function (st, a) { if (a[0] > 63) return bad(); if (cm(st).dscp.indexOf(a[0]) < 0) cm(st).dscp.push(a[0]); touch(st); }, 'Пакеты с этим DSCP');
  S.cmd('cmap', 'no match dscp <n>', function (st, a) { cm(st).dscp = cm(st).dscp.filter(function (x) { return x !== a[0]; }); touch(st); });
  S.cmd('cmap', 'set dscp <n>', function (st, a) { if (a[0] > 63) return bad(); cm(st).set = a[0]; touch(st); }, 'Перемаркировать DSCP');
  S.cmd('cmap', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  S.cmd('config', 'policy-map <w>', function (st, a) { var P = Q(st).pmaps; P[a[0]] = P[a[0]] || { cls: {}, order: [] }; st.mode = 'pmap'; st.ctx = a[0]; touch(st); }, 'Политика QoS');
  S.cmd('config', 'no policy-map <w>', function (st, a) { delete Q(st).pmaps[a[0]]; touch(st); });
  S.cmd('pmap', 'class <w>', function (st, a) { var P = pm(st); if (!P.cls[a[0]]) { P.cls[a[0]] = {}; P.order.push(a[0]); } st.mode = 'pcls'; st.ctx = st.ctx + '|' + a[0]; touch(st); }, 'Действия для класса');
  S.cmd('pmap', 'no class <w>', function (st, a) { var P = pm(st); delete P.cls[a[0]]; P.order = P.order.filter(function (x) { return x !== a[0]; }); touch(st); });
  function shape(set) { return function (st, a) { var w = a[0].trim().split(/\s+/); if (w[0] === 'percent') return bad();   // percent — от скорости интерфейса: не моделируется
    var bw = +w[0], b = w[1] ? +w[1] : 128000; if (!(bw >= 1 && bw <= 10000000) || !(b >= 128 && b <= 16000000)) return bad(); set(st, { kbps: bw, burst: b }); touch(st); }; }
  S.cmd('pmap', 'shape average <rest>', shape(function (st, v) { pm(st).shape = v; }), 'Сглаживание всего трафика интерфейса, Кбит/с');
  S.cmd('pcls', 'shape average <rest>', shape(function (st, v) { pc(st).shape = v; }), 'Сглаживание класса, Кбит/с [burst, байт]');
  S.cmd('pcls', 'no shape average', function (st) { delete pc(st).shape; touch(st); });
  S.cmd('pcls', 'set dscp <n>', function (st, a) { if (a[0] > 63) return bad(); pc(st).set = a[0]; touch(st); }, 'Перемаркировать DSCP');
  S.cmd('pcls', 'police <rest>', function (st, a) { var w = a[0].trim().split(/\s+/), o = { kbps: +w[0], burst: 1500, exceed: 'drop' };
    if (!(o.kbps >= 1)) return bad();
    for (var i = 1; i < w.length; i++) { if (w[i] === 'burst-conforming') o.burst = +w[++i]; else if (w[i] === 'conform-action') i++;
      else if (w[i] === 'exceed-action') { var x = w[++i]; if (x === 'drop') o.exceed = 'drop'; else if (x === 'set-dscp-transmit') o.exceed = +w[++i]; else if (x === 'transmit') o.exceed = 'transmit'; else return bad(); }
      else return bad(); }
    pc(st).police = o; touch(st); }, 'Ограничение полосы класса, Кбит/с (лишнее — drop)');
  S.cmd('pcls', 'no police', function (st) { delete pc(st).police; touch(st); });
  S.cmd('pcls', 'exit', function (st) { st.mode = 'pmap'; st.ctx = st.ctx.split('|')[0]; });
  S.cmd('pmap', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  function ifs(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }
  S.cmd('gi sub', 'service-policy <w> <w>', function (st, a) { if (a[0] !== 'input' && a[0] !== 'output') return bad(); if (!Q(st).pmaps[a[1]]) return '% Политика ' + a[1] + ' не создана';
    ifs(st, function (x) { (x.qos = x.qos || {})[a[0]] = a[1]; }); }, 'Политика QoS на вход | выход');
  S.cmd('gi sub', 'no service-policy <w>', function (st, a) { ifs(st, function (x) { if (x.qos) delete x.qos[a[0]]; }); });
  S.cmd('gi sub', 'qos enable', function (st) { ifs(st, function (x) { x.qosOn = true; }); }, 'Включить QoS на интерфейсе');
  S.cmd('gi sub', 'no qos enable', function (st) { ifs(st, function (x) { delete x.qosOn; }); });
  S.RUNX.push(function (c, o) { var q = c.qos; if (!q) return;
    Object.keys(q.cmaps).forEach(function (n) { var x = q.cmaps[n]; o.push('class-map ' + n); x.acl.forEach(function (a) { o.push('  match access-group ' + a); });
      x.dscp.forEach(function (d) { o.push('  match dscp ' + d); }); if (x.set !== undefined) o.push('  set dscp ' + x.set); o.push('exit'); });
    Object.keys(q.pmaps).forEach(function (n) { var P = q.pmaps[n]; o.push('policy-map ' + n); if (P.shape) o.push('  shape average ' + P.shape.kbps + (P.shape.burst !== 128000 ? ' ' + P.shape.burst : ''));
      P.order.forEach(function (k) { var x = P.cls[k]; o.push('  class ' + k); if (x.set !== undefined) o.push('    set dscp ' + x.set);
        if (x.police) o.push('    police ' + x.police.kbps + (x.police.burst !== 1500 ? ' burst-conforming ' + x.police.burst : '') + (x.police.exceed === 'drop' ? '' : x.police.exceed === 'transmit' ? ' exceed-action transmit' : ' exceed-action set-dscp-transmit ' + x.police.exceed));
        if (x.shape) o.push('    shape average ' + x.shape.kbps + (x.shape.burst !== 128000 ? ' ' + x.shape.burst : '')); o.push('  exit'); }); o.push('exit'); });
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k], L = []; if (x.qosOn) L.push('  qos enable'); Object.keys(x.qos || {}).forEach(function (d) { L.push('  service-policy ' + d + ' ' + x.qos[d]); });
      if (L.length) o.push('interface ' + S.longIf(k), L.join('\n'), 'exit'); }); });

  // ---------------------------------------------------------------- в симуляции: классы, маркировка, police, shape
  function classOf(c, P, pk) {                   // первый подошедший класс политики
    var q = c.qos; for (var i = 0; i < P.order.length; i++) { var n = P.order[i], C = q.cmaps[n]; if (!C) continue;
      var hit = (!C.acl.length && !C.dscp.length) || C.acl.some(function (a) { var r = EL.aclPass && EL.aclPass((c.acls || {})[a], pk); return r && r.ok && r.rule !== null; }) ||
        C.dscp.indexOf(pk.dscp || 0) >= 0;
      if (hit) return n; }
    return null;
  }
  function bucket(ctx, key, kbps, burst, t, bytes, shapeIt) {
    var B = ctx[key] = ctx[key] || { tok: burst, last: 0, vt: 0 }, rate = kbps * 1000 / 8;
    if (shapeIt) { B.vt = Math.max(t, B.vt) + bytes / rate; var ahead = B.vt - t - burst / rate; return ahead > 0 ? t + ahead : t; }
    B.tok = Math.min(burst, B.tok + (t - B.last) * rate); B.last = t;
    if (B.tok >= bytes) { B.tok -= bytes; return true; } return false;
  }
  // dir 'input' — пакет вошёл в устройство через ifn, 'output' — уходит через ifn. Возвращает {drop, why} или {t, dscp}
  EL.qosSim = function (net, ctx, dev, ifn, dir, pk, t, bytes) {
    var d = net.devs[dev]; if (!d || d.type !== 'esr') return null; var c = d.st.run, x = c.ifs[ifn], name = x && x.qos && x.qos[dir], P = name && c.qos && c.qos.pmaps[name];
    if (!P) return null;
    var cls = classOf(c, P, pk), out = { t: t, dscp: pk.dscp };
    if (cls) { var A = P.cls[cls], C = c.qos.cmaps[cls];
      if (C && C.set !== undefined) out.dscp = C.set; if (A.set !== undefined) out.dscp = A.set;
      if (A.police) { var ok = bucket(ctx, dev + '|' + ifn + '|' + dir + '|' + cls + '|p', A.police.kbps, A.police.burst, t, bytes, false);
        if (!ok) { if (A.police.exceed === 'drop') return { drop: true, why: d.name + ' ' + ifn + ': police ' + A.police.kbps + ' Кбит/с (класс ' + cls + ') — лишнее отброшено' };
          if (A.police.exceed !== 'transmit') out.dscp = A.police.exceed; } }
      if (A.shape) out.t = Math.max(out.t, bucket(ctx, dev + '|' + ifn + '|' + dir + '|' + cls + '|s', A.shape.kbps, A.shape.burst, out.t, bytes, true)); }
    if (P.shape) out.t = Math.max(out.t, bucket(ctx, dev + '|' + ifn + '|' + dir + '|*|s', P.shape.kbps, P.shape.burst, out.t, bytes, true));
    out.cls = cls; return out;
  };
})(typeof window !== 'undefined' ? window : global);
