/* Таймеры служб по модельному времени (net.now).
   NAT на ESR: трансляция — запись conntrack; живёт по таймаутам сессий (ip firewall sessions …-timeout,
     справочник ESR 1.23: icmp 30, udp-wait 30, udp-assured 180, tcp-connect 60, tcp-estabilished 120, tcp-disconnect 30, generic 60 с),
     каждый новый пакет потока продлевает её. show ip nat translations — формат справочника (Prot / Inside / Outside / Pkts / Bytes).
   Упрощения: размер пакета условный (ICMP 84 байта — как в примере справочника, UDP 60, TCP 60);
     одна запись на поток «протокол + адреса» без портов. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype;
  var TO = { icmp: 30, 'udp-wait': 30, 'udp-assured': 180, 'tcp-connect': 60, 'tcp-estabilished': 120, 'tcp-disconnect': 30, generic: 60 };
  var KEEP_OPEN = [22, 23], BYTES = { icmp: 84, udp: 60, tcp: 60 };
  function toOf(net, dev, x) { var c = net.devs[dev].st.run; return ((c && c.fwto) || {})[x.to] || TO[x.to]; }
  function natLeft(net, dev, x) { return toOf(net, dev, x) - (net.now - x.t); }
  function stateTo(proto, ok, dport) {
    if (proto === 'icmp') return 'icmp';
    if (proto === 'udp') return ok ? 'udp-assured' : 'udp-wait';
    if (proto === 'tcp') return !ok ? 'tcp-connect' : KEEP_OPEN.indexOf(dport) >= 0 ? 'tcp-estabilished' : 'tcp-disconnect';
    return 'generic';
  }

  // ---------------------------------------------------------------- NAT: таблица трансляций
  var req0 = P.request;
  P.request = function (src, dst, proto, dport) {
    var r = req0.apply(this, arguments), s = this, T = s.natTab = s.natTab || {};
    (s.ctLast || []).forEach(function (c) {
      if (c.kind !== 's' && c.kind !== 'd') return;
      var row = c.kind === 's' ? { p: c.proto, is: c.orig, id: c.peer, os: c.pub, od: c.peer } : { p: c.proto, is: c.client, id: c.target, os: c.client, od: c.pub };
      var L = T[c.dev] = T[c.dev] || [], k = [row.p, row.is, row.id, row.os, row.od].join('|'), x = L.filter(function (y) { return y.k === k; })[0];
      var n = r.ok ? 2 : 1;
      if (!x) { x = { k: k, row: row, pk: 0, by: 0 }; L.push(x); }
      x.pk += n; x.by += n * (BYTES[row.p] || 60); x.t = s.now; x.to = stateTo(row.p, r.ok, dport);
    });
    return r;
  };
  var tick0 = P.tick;
  P.tick = function () {
    var g = tick0.apply(this, arguments), s = this;
    Object.keys(s.natTab || {}).forEach(function (id) { s.natTab[id] = s.natTab[id].filter(function (x) { return natLeft(s, id, x) > 0; }); });
    return g;
  };
  function pad(v, n) { v = String(v); while (v.length < n) v += ' '; return v; }
  function natText(st, proto) {
    var L = ((st.net && st.net.natTab) || {})[st.dev] || [];
    L = L.filter(function (x) { return !proto || x.row.p === proto; });
    var o = [pad('Prot', 5) + pad('Inside source', 17) + pad('Inside destination', 19) + pad('Outside source', 17) + pad('Outside destination', 20) + pad('Pkts', 6) + 'Bytes',
      '---- ---------------- ------------------ ---------------- ------------------- ----- -----'];
    L.forEach(function (x) { var w = x.row; o.push(pad(w.p, 5) + pad(w.is, 17) + pad(w.id, 19) + pad(w.os, 17) + pad(w.od, 20) + pad(x.pk, 6) + x.by); });
    return o.join('\n');
  }
  function scmd(modes, pat, fn, d) { S.cmd(modes, pat, fn, d); var c = S.T.pop(); S.T.unshift(c); return c; }
  scmd('priv', 'show ip nat translations', function (st) { return natText(st); }, 'Трансляции NAT (живут по таймаутам ip firewall sessions)');
  scmd('priv', 'show ip nat translations protocol <w>', function (st, a) { return natText(st, a[0].toLowerCase()); });
  // ---------------------------------------------------------------- LLDP: TTL соседа = timer × hold-multiplier, отсчёт между LLDPDU
  // ESR: lldp timer 1..32768 (30), lldp hold-multiplier 1..10 (4); MES 10.x: lldp transmit-interval 5..32768, lldp holdtime-multiplier 2..10;
  // MES 6.x: lldp timer 5..32768, lldp hold-multiplier 2..10. Новый сосед, смена имени — LLDPDU сразу, TTL снова полный.
  function lldpPar(d) { var c = d.type === 'esr' ? d.st.run : d.st; return { tm: c.lldpTimer || 30, hm: c.lldpHold || 4 }; }
  P.lldpTtl = function (id, port) {
    var pr = this.peer(id, port); if (!pr) return 0;
    var nd = this.devs[pr.dev], q = lldpPar(nd), ttl = Math.min(65535, q.tm * q.hm), K = this._lldp = this._lldp || {};
    var sig = pr.dev + '|' + pr.port + '|' + (nd.type === 'esr' ? nd.st.run.host : nd.st.host) + '|' + q.tm + '|' + q.hm, k = id + '|' + port;
    if (!K[k] || K[k].sig !== sig) K[k] = { sig: sig, t0: this.now };
    return ttl - Math.floor((this.now - K[k].t0) % q.tm);
  };
  var tick1 = P.tick;
  P.tick = function () { var s = this, K = s._lldp || {};          // линк упал — сведения о соседе на порту удаляются
    Object.keys(K).forEach(function (k) { var p = k.split('|'); if (!s.devs[p[0]] || !s.linkUp(p[0], p[1])) delete K[k]; });
    return tick1.apply(this, arguments); };
  function rng(lo, hi, f) { return function (st, a) { var n = +a[0]; if (!/^\d+$/.test(a[0]) || n < lo || n > hi) return '% Допустимо ' + lo + '..' + hi; f(st, n); }; }
  function etouch(st) { st.pending = true; }
  S.cmd('config', 'lldp timer <w>', rng(1, 32768, function (st, n) { st.cand.lldpTimer = n; etouch(st); }), 'Период отправки LLDPDU, с (по умолчанию 30)');
  S.cmd('config', 'no lldp timer', function (st) { delete st.cand.lldpTimer; etouch(st); });
  S.cmd('config', 'lldp hold-multiplier <w>', rng(1, 10, function (st, n) { st.cand.lldpHold = n; etouch(st); }), 'Сколько периодов хранить сведения о соседе (по умолчанию 4)');
  S.cmd('config', 'no lldp hold-multiplier', function (st) { delete st.cand.lldpHold; etouch(st); });
  S.RUNX.push(function (c, o) { if (c.lldpTimer) o.push('lldp timer ' + c.lldpTimer); if (c.lldpHold) o.push('lldp hold-multiplier ' + c.lldpHold); });
  var E = EL.E, CMDS = E.CMDS;
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  mcmd(['10'], 'config', 'lldp transmit-interval <w>', rng(5, 32768, function (st, n) { st.lldpTimer = n; }), 'Период отправки LLDPDU, с (по умолчанию 30)');
  mcmd(['10'], 'config', 'no lldp transmit-interval', function (st) { delete st.lldpTimer; });
  mcmd(['10'], 'config', 'lldp holdtime-multiplier <w>', rng(2, 10, function (st, n) { st.lldpHold = n; }), 'Множитель TTL (по умолчанию 4)');
  mcmd(['10'], 'config', 'no lldp holdtime-multiplier', function (st) { delete st.lldpHold; });
  mcmd(['6'], 'config', 'lldp timer <w>', rng(5, 32768, function (st, n) { st.lldpTimer = n; }), 'Период отправки LLDPDU, с (по умолчанию 30)');
  mcmd(['6'], 'config', 'no lldp timer', function (st) { delete st.lldpTimer; });
  mcmd(['6'], 'config', 'lldp hold-multiplier <w>', rng(2, 10, function (st, n) { st.lldpHold = n; }), 'Множитель TTL (по умолчанию 4)');
  mcmd(['6'], 'config', 'no lldp hold-multiplier', function (st) { delete st.lldpHold; });
  E.RUNX.push(function (st, o) {
    if (st.lldpTimer) o.push((st.dialect === '6' ? 'lldp timer ' : 'lldp transmit-interval ') + st.lldpTimer);
    if (st.lldpHold) o.push((st.dialect === '6' ? 'lldp hold-multiplier ' : 'lldp holdtime-multiplier ') + st.lldpHold); });

  // ---------------------------------------------------------------- LACP: партнёр перестал слать LACPDU (линк жив) — порт ещё
  // timeout в агрегате: short — 3 с (LACPDU раз в 1 с × 3), long — 90 с (раз в 30 с × 3); падение линка — сразу
  // 10.x и 6.x: lacp timeout long|short на порту (по умолчанию long); 8.x: [no] lacp actor admin state longtimeout
  function lacpTo(c) { return c && c.lacpTo === 'short' ? 3 : 90; }
  var lp0 = P.lports;
  P.lports = function (id) {
    var out = lp0.apply(this, arguments), d = this.devs[id], st = d.st, s = this, K = (this._lacp = this._lacp || {});
    if (!st.pos) return out;
    var inAgg = {}; out.forEach(function (L) { if (L.name.indexOf('po') === 0) L.members.forEach(function (p) { inAgg[p] = L; }); });
    this.portsOf(d).forEach(function (p) {
      var x = st.ports[p], k = id + '|' + p; if (!x || !x.cg || x.cg.mode === 'on') { delete K[k]; return; }
      if (inAgg[p]) { K[k] = s.now; return; }
      if (K[k] === undefined || !s.linkUp(id, p) || s.now - K[k] >= lacpTo(x)) { delete K[k]; return; }
      var nm = 'po' + x.cg.id, L = out.filter(function (l) { return l.name === nm; })[0];      // ещё в агрегате: LACPDU партнёра не устарели
      if (!L) { if (!st.pos[nm]) return; L = { name: nm, cfg: st.pos[nm], members: [], down: [] }; out = out.filter(function (l) { return l.name !== p; }).concat([L]); }
      else out = out.filter(function (l) { return l.name !== p; });
      L.members.push(p); L.stale = (L.stale || []).concat([p]);
    });
    return out;
  };
  P.lacpLeft = function (id, p) { var k = id + '|' + p, K = this._lacp || {}, x = this.devs[id].st.ports[p];
    this.lports(id); return K[k] === undefined ? null : Math.max(0, lacpTo(x) - (this.now - K[k])); };
  function lacpSync(s) { s.order.forEach(function (id) { var d = s.devs[id]; if (d.type === 'mes' && d.st.pos) s.lports(id); }); }
  var ex1 = P.exec;
  P.exec = function () { lacpSync(this); return ex1.apply(this, arguments); };
  var tick2 = P.tick;
  P.tick = function () { lacpSync(this); return tick2.apply(this, arguments); };
  function mports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k]; }).filter(Boolean) : null; }
  function each(st, f) { var p = mports(st); if (!p) return '% Команда для физического порта'; p.forEach(f); }
  mcmd(['10', '6'], 'if range', 'lacp timeout <w>', function (st, a) { var m = a[0].toLowerCase(); if (m !== 'long' && m !== 'short') return '% Таймаут: long | short';
    return each(st, function (p) { if (m === 'short') p.lacpTo = 'short'; else delete p.lacpTo; }); }, 'Таймаут LACP: short — 3 с, long — 90 с');
  mcmd(['10', '6'], 'if range', 'no lacp timeout', function (st) { return each(st, function (p) { delete p.lacpTo; }); });
  mcmd(['8'], 'if range', 'lacp actor admin state longtimeout', function (st) { return each(st, function (p) { delete p.lacpTo; }); }, 'Длинный таймаут LACP (90 с)');
  mcmd(['8'], 'if range', 'no lacp actor admin state longtimeout', function (st) { return each(st, function (p) { p.lacpTo = 'short'; }); }, 'Короткий таймаут LACP (3 с)');
  E.PORTX.push(function (st, k, p, d) { if (p.lacpTo === 'short') d.push(st.dialect === '8' ? ' no lacp actor admin state longtimeout' : ' lacp timeout short'); });

  P.natLeft = function (dev, i) { var x = ((this.natTab || {})[dev] || [])[i]; return x ? Math.max(0, Math.ceil(natLeft(this, dev, x))) : null; };
})(typeof window !== 'undefined' ? window : global);
