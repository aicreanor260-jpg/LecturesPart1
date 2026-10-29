/* Симуляция во времени (как в OMNeT++): дискретные события поверх логики сети.
   Путь пакета берётся из модели (тот же ping/запрос: ARP, VLAN, маршруты, NAT, межсетевой экран), а время считается по каждому кабелю:
   — передача (сериализация) = размер кадра × 8 / скорость линка (из согласования speed/duplex, Мбит/с);
   — распространение = длина кабеля / 2·10⁸ м/с (по умолчанию 100 м); обработка в устройстве — 10 мкс;
   — у каждого выходного порта очередь FIFO (по умолчанию 64 кадра): переполнилась — кадр теряется (drop-tail);
   — несовпадение дуплекса — часть кадров теряется в коллизиях (20 %), кадры считаются и в счётчиках ошибок;
   — MTU — самый узкий интерфейс на пути (mtu на ESR, туннель GRE 1476, иначе 1500): больше — с флагом DF пакет отбрасывается
     («Fragmentation needed»), без DF режется на фрагменты.
   Потоки: ping (интервал, число, размер, DF) и UDP (скорость в пакетах/с, длительность, размер) — RTT, джиттер, потери, загрузка линков.
   Упрощения: путь считается один раз на поток (маршрут во время потока не меняется), ARP и TCP-окна не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype;
  var DEF = { len: 100, prop: 2e8, proc: 10e-6, qcap: 64, mtu: 1500, collide: 0.2 };
  EL.SIM = DEF;
  // путь в одну сторону: отрезки кадров IP (шаги 'ip' трассы) в порядке прохождения
  function ipSegs(steps, reply) {
    var out = [], seenOk = false;
    steps.forEach(function (s) { if (s.k === 'ok' && /получил/.test(s.t) && !seenOk) seenOk = true;
      if (s.k === 'ip' && s.f && !!s.f.reply === !!reply) (s.segs || []).forEach(function (g) { out.push({ li: g.li, from: g.from, to: g.to, tag: g.tag }); }); });
    return out;
  }
  function rng(seed) { var x = seed >>> 0 || 1; return function () { x ^= x << 13; x >>>= 0; x ^= x >> 17; x ^= x << 5; x >>>= 0; return x / 4294967296; }; }
  // скорость и дуплекс кабеля сегмента
  function linkInfo(net, sg) { var l = net.links[sg.li]; if (!l) return null; var ph = net.phys ? net.phys(l.a.dev, l.a.port) : { up: true, speed: 1000, dup: {} };
    return { l: l, mbps: Math.min(ph.speed || 1000, net.linkCap ? net.linkCap(l) : l.mbps || 1e9), mismatch: !!ph.mismatch, len: l.len || DEF.len, prop: EL.propSpeed ? EL.propSpeed(net.cabOf ? net.cabOf(l) : l.cab) : DEF.prop, port: l.a.dev === sg.from ? l.a.port : l.b.port }; }
  /* flows: [{kind:'ping'|'udp', src, dst, size, count, interval, df, rate, dur, start}]; opt: {len, qcap, until}
     → {events:[{t, kind:'tx'|'drop'|'rx'|'deliver', flow, pkt, seg, t0, t1}], stats} */
  P.simulate = function (flows, opt) {
    opt = opt || {}; var s = this, ev = [], q = [], ports = {}, rand = rng(opt.seed || 7), links = {}, res = [];
    function push(e) { var i = q.length; q.push(e); while (i > 0) { var p = (i - 1) >> 1; if (q[p].t <= q[i].t) break; var t = q[p]; q[p] = q[i]; q[i] = t; i = p; } }
    function pop() { var top = q[0], last = q.pop(); if (q.length) { q[0] = last; var i = 0; for (;;) { var a = 2 * i + 1, b = a + 1, m = i;
      if (a < q.length && q[a].t < q[m].t) m = a; if (b < q.length && q[b].t < q[m].t) m = b; if (m === i) break; var t = q[m]; q[m] = q[i]; q[i] = t; i = m; } } return top; }
    flows.forEach(function (fl, fi) {
      var st = { flow: fi, kind: fl.kind, src: fl.src, dst: fl.dst, sent: 0, recv: 0, rtt: [], drops: {}, frag: 1, why: null };
      res.push(st);
      var size = Math.max(28, fl.size || 64), ipLen = size + 28;
      // путь и его MTU: проба с размером пакета — mtu.js отмечает самый узкий интерфейс (без отбрасывания)
      var pr = s._mtuPing = { size: ipLen, df: !!fl.df, local: 'err', probe: true }, r;
      try { r = fl.kind === 'udp' ? s.request(fl.src, fl.dst, 'udp', fl.port || 5001) : s.ping(fl.src, fl.dst); } finally { s._mtuPing = null; }
      var mtu = Math.min(opt.mtu || DEF.mtu, pr.min || 1e9);
      var fw = ipSegs(r.steps, false), bk = fl.kind === 'ping' ? ipSegs(r.steps, true) : [];
      // UDP идёт в одну сторону: годится и «Connection refused» — пакет дошёл до получателя, просто его там никто не слушает
      var reached = fl.kind === 'udp' ? (r.ok || r.dev !== undefined) : r.ok;
      if (!fw.length || !reached) { st.why = r.why || 'нет пути'; st.blocked = true; }
      if (ipLen > mtu) { if (fl.df) { st.why = 'Пакет ' + ipLen + ' байт больше MTU ' + mtu + (pr.hit && !pr.hit.local ? ' на ' + s.devs[pr.hit.dev].name : '') + ' при DF — «Fragmentation needed», не доставлен'; st.blocked = true; } else st.frag = Math.ceil((ipLen - 20) / (mtu - 20)); }
      st.fw = fw; st.bk = bk;
      var ip0 = (r.steps || []).filter(function (x) { return x.f && x.f.src && x.k === 'ip'; })[0];          // поля пакета для QoS (qos.js)
      st.pk = { proto: fl.kind === 'udp' ? 'udp' : 'icmp', src: ip0 ? ip0.f.src : ((s.ifaces(fl.src)[0] || {}).ip), dst: fl.dst, dport: fl.kind === 'udp' ? (fl.port || 5001) : null };
      var n = fl.kind === 'udp' ? Math.floor((fl.dur || 1) * (fl.rate || 100)) : (fl.count || 5), gap = fl.kind === 'udp' ? 1 / (fl.rate || 100) : (fl.interval || 1);
      for (var k = 0; k < n; k++) { st.sent++; if (st.blocked) { st.drops[st.why] = (st.drops[st.why] || 0) + 1; continue; }
        var t0 = (fl.start || 0) + k * gap, frBytes = Math.min(ipLen, mtu) + 18;
        for (var f = 0; f < st.frag; f++) push({ t: t0, kind: 'arrive', flow: fi, pkt: k, frag: f, dir: 'fw', i: 0, dscp: fl.dscp || 0, bytes: f === st.frag - 1 && st.frag > 1 ? (ipLen - (mtu - 20) * (st.frag - 1)) + 20 + 18 : frBytes, born: t0 }); }
    });
    var got = {}, MAXEV = 200000, guard = 0, qctx = {};
    while (q.length && guard++ < MAXEV) {
      var e = pop(), st = res[e.flow], path = e.dir === 'fw' ? st.fw : st.bk;
      if (opt.until && e.t > opt.until) break;
      if (e.i >= path.length) {                                   // дошёл до получателя
        var key = e.flow + '|' + e.pkt + '|' + e.dir; got[key] = (got[key] || 0) + 1;
        if (got[key] < st.frag) continue;                         // ждём все фрагменты
        ev.push({ t: e.t, kind: 'deliver', flow: e.flow, pkt: e.pkt, dir: e.dir, delay: e.t - e.born, node: (path.length ? s.devs[path[path.length - 1].to] : s.devs[st.src] || {}).name });
        if (e.dir === 'fw' && st.kind === 'ping') { for (var f2 = 0; f2 < st.frag; f2++) push({ t: e.t + DEF.proc, kind: 'arrive', flow: e.flow, pkt: e.pkt, frag: f2, dir: 'bk', i: 0, bytes: e.bytes, born: e.born, dscp: e.dscp }); }
        else { st.recv++; st.rtt.push(e.t - e.born); }           // ping — RTT, UDP — задержка в одну сторону
        continue;
      }
      var sg = path[e.i], li = linkInfo(s, sg); if (!li) { st.drops['кабель удалён'] = (st.drops['кабель удалён'] || 0) + 1; continue; }
      var pk = sg.li + '|' + sg.from, P2 = ports[pk] || (ports[pk] = { busy: 0, wait: [], maxq: 0, name: s.devs[sg.from].name + ' ' + li.port });
      var t = e.t + (e.i === 0 && e.dir === 'fw' ? 0 : DEF.proc);
      if (EL.qosSim && st.pk) {                                  // QoS: политика на входе (интерфейс прихода) и на выходе (li.port)
        var pkq = { proto: st.pk.proto, src: e.dir === 'fw' ? st.pk.src : st.pk.dst, dst: e.dir === 'fw' ? st.pk.dst : st.pk.src, dport: st.pk.dport, dscp: e.dscp || 0 }, qs = [];
        if (e.i > 0) { var pv = path[e.i - 1], pl = s.links[pv.li]; if (pl) qs.push([pl.a.dev === pv.to ? pl.a.port : pl.b.port, 'input']); }
        qs.push([li.port, 'output']); var qdrop = null;
        qs.forEach(function (q) { if (qdrop) return; var qr = EL.qosSim(s, qctx, sg.from, q[0], q[1], pkq, t, e.bytes); if (!qr) return; if (qr.drop) { qdrop = qr.why; return; } t = qr.t; pkq.dscp = qr.dscp; });
        if (qdrop) { st.drops[qdrop] = (st.drops[qdrop] || 0) + 1; ev.push({ t: t, kind: 'drop', flow: e.flow, pkt: e.pkt, seg: sg, why: qdrop }); continue; }
        e.dscp = pkq.dscp; }
      P2.wait = P2.wait.filter(function (x) { return x > t; });
      if (P2.wait.length >= (opt.qcap || DEF.qcap)) { var w = 'очередь ' + P2.name + ' переполнена'; st.drops[w] = (st.drops[w] || 0) + 1;
        ev.push({ t: t, kind: 'drop', flow: e.flow, pkt: e.pkt, seg: sg, why: w }); continue; }
      var t1 = Math.max(t, P2.busy), tx = e.bytes * 8 / (li.mbps * 1e6), t2 = t1 + tx, t3 = t2 + (opt.len || li.len) / li.prop;
      P2.busy = t2; P2.wait.push(t1); P2.maxq = Math.max(P2.maxq, P2.wait.length);
      var L = links[sg.li] || (links[sg.li] = { bits: 0, frames: 0, mbps: li.mbps, name: s.devs[li.l.a.dev].name + ' ' + li.l.a.port + ' ↔ ' + s.devs[li.l.b.dev].name + ' ' + li.l.b.port });
      L.bits += e.bytes * 8; L.frames++;
      if (li.mismatch && rand() < DEF.collide) { var wc = 'коллизия на ' + L.name + ' (дуплекс не совпадает)'; st.drops[wc] = (st.drops[wc] || 0) + 1;
        ev.push({ t: t1, kind: 'drop', flow: e.flow, pkt: e.pkt, seg: sg, why: wc, t1: t1, t2: t3 }); continue; }
      var lp = s.linkLoss ? s.linkLoss(li.l, e.bytes) : 0;           // параметры канала (linkprops.js): потери %, BER, длина сверх нормы
      if (lp && rand() < lp) { var wl = (li.l.ber && !li.l.loss ? 'битовые ошибки (BER ' + li.l.ber + ') на ' : 'потери на ') + L.name; st.drops[wl] = (st.drops[wl] || 0) + 1;
        ev.push({ t: t1, kind: 'drop', flow: e.flow, pkt: e.pkt, seg: sg, why: wl, t1: t1, t2: t3 }); continue; }
      if (li.l.jit) t3 += rand() * li.l.jit / 1000;
      if (s.extraDelay) t3 += s.extraDelay(li.l);                    // облако провайдера (isp.js): половина задержки на каждом кабеле к облаку                 // джиттер канала: случайная добавка к задержке 0…jit мс
      ev.push({ t: t1, kind: 'tx', flow: e.flow, pkt: e.pkt, seg: sg, t1: t1, t2: t3, tx: tx, dir: e.dir, frag: e.frag, bytes: e.bytes, q: P2.wait.length, port: P2.name });
      push({ t: t3, kind: 'arrive', flow: e.flow, pkt: e.pkt, frag: e.frag, dir: e.dir, i: e.i + 1, bytes: e.bytes, born: e.born, dscp: e.dscp });
    }
    var tEnd = ev.reduce(function (m, x) { return Math.max(m, x.t2 || x.t); }, 0) || 1;
    res.forEach(function (st) { var r = st.rtt.slice(); st.loss = st.sent ? Math.round((st.sent - st.recv) / st.sent * 100) : 0;
      if (r.length) { st.min = Math.min.apply(null, r); st.max = Math.max.apply(null, r); st.avg = r.reduce(function (a, b) { return a + b; }, 0) / r.length;
        var d = 0; for (var i = 1; i < r.length; i++) d += Math.abs(r[i] - r[i - 1]); st.jitter = r.length > 1 ? d / (r.length - 1) : 0; } });
    var lk = Object.keys(links).map(function (k) { var x = links[k]; return { li: +k, name: x.name, frames: x.frames, util: Math.min(100, x.bits / tEnd / (x.mbps * 1e6) * 100), mbps: x.mbps }; });
    var pq = Object.keys(ports).map(function (k) { return { name: ports[k].name, maxq: ports[k].maxq }; }).filter(function (x) { return x.maxq > 1; });
    var out = { events: ev, flows: res, links: lk, queues: pq, tEnd: tEnd, truncated: guard >= MAXEV };
    if (!opt.probe) this._simLast = out;      // «Свойства»: загрузка портов по последней симуляции
    return out;
  };
})(typeof window !== 'undefined' ? window : global);
