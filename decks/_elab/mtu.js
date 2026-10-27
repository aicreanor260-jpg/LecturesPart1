/* MTU и размер пакета в консоли (синтаксис — дерево команд прошивки ESR 1.40.4 и шаблоны прошивки MES 10.4.6):
   ESR: на интерфейсе/саб-интерфейсе mtu 552..9018 (по умолчанию 1500), на туннеле GRE/VTI mtu 552..10000 (GRE по умолчанию 1476);
        ping A.B.C.D [size 1..65468] [packets N] [strategy disallow-fragmentation | discovery-pmtu | allow-fragmentation].
   MES 10.x: ping A.B.C.D [size 36..2080] [df-bit] [count 1..10].   VPC: ping A.B.C.D [-l размер] [-D] [-c N].
   Debian: ping [-s размер] [-M do|want|dont] [-c N] A.B.C.D.
   Размер — данные ICMP; IP-пакет = размер + 28. Пакет больше MTU выходного интерфейса: без DF режется на фрагменты,
   с DF отбрасывается, маршрутизатор отвечает ICMP «Fragmentation needed» (тип 3, код 4) со своим MTU.
   Стратегии как в Linux: do — DF и запрет даже своей фрагментации; want (по умолчанию у ESR и Debian) — DF в сети,
   после «Fragmentation needed» узел запоминает MTU пути и дальше режет пакет сам; dont — DF не ставится.
   У VPC и MES по умолчанию DF не ставится (-D / df-bit — ставится).
   Упрощения: MTU коммутатора MES (mtu, system mtu — размер кадра L2) не моделируется, у хостов MTU 1500;
   накладные расходы инкапсуляции внутри туннеля учтены только через MTU туннеля. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, E = EL.E, P = EL.Net.prototype, CMDS = E.CMDS;
  var DEF = 1500, GRE = 1476;
  function touch(st) { st.pending = true; }
  function ifs(st) { return (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).map(function (k) { return st.cand.ifs[k]; }).filter(Boolean); }
  function setMtu(lo, hi) { return function (st, a) { if (a[0] < lo || a[0] > hi) return 'Syntax error: Illegal parameter'; ifs(st).forEach(function (x) { x.mtu = a[0]; }); touch(st); }; }
  S.cmd('gi sub', 'mtu <n>', setMtu(552, 9018), 'MTU интерфейса (552–9018, по умолчанию 1500)');
  S.cmd('gre vti', 'mtu <n>', setMtu(552, 10000), 'MTU туннеля (552–10000)');
  S.cmd('gi sub gre vti', 'no mtu', function (st) { ifs(st).forEach(function (x) { delete x.mtu; }); touch(st); });
  S.RUNX.push(function (c, o) { Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k]; if (!x.mtu) return;
    o.push(x.tun ? 'tunnel ' + x.tun + ' ' + k.slice(3) : 'interface ' + S.longIf(k), '  mtu ' + x.mtu, 'exit'); }); });

  // MTU выходного интерфейса
  P.ifMtu = function (id, iface) {
    var d = this.devs[id]; if (d.type !== 'esr') return DEF;
    var x = d.st.run.ifs[iface.name.split(':')[0]] || {};
    return x.mtu || (x.tun === 'gre' ? GRE : DEF);
  };
  // проверка в P.send: контекст _mtuPing = {size, df, local: 'frag'|'err', probe, hit, min}
  P.mtuCheck = function (cur, iface, inIf, pk, steps, src) {
    var c = this._mtuPing; if (!c) return null;
    var m = this.ifMtu(cur, iface), d = this.devs[cur], size = c.size;
    c.min = Math.min(c.min || 1e9, m);
    if (size <= m) return null;
    var local = cur === src, df = c.df && !(local && (c.local === 'frag' || pk.reply));
    if (!df) {
      var n = Math.ceil((size - 20) / (Math.floor((m - 20) / 8) * 8));
      if (!c.probe) steps.push({ k: 'route', t: d.name + ': пакет ' + size + ' байт больше MTU ' + m + ' на ' + iface.name.split(':')[0] + ' — разрезан на ' + n + ' фрагмента(ов), собирает получатель' });
      return null;
    }
    c.hit = c.hit || { dev: cur, ip: inIf ? inIf.ip : null, mtu: m, local: local };
    if (c.probe) return null;
    steps.push({ k: 'drop', t: local ? d.name + ': пакет ' + size + ' байт больше MTU ' + m + ' своего интерфейса, а фрагментация запрещена — не отправлен (message too long)'
      : d.name + ': пакет ' + size + ' байт больше MTU ' + m + ' на ' + iface.name.split(':')[0] + ', стоит флаг DF — отброшен; отправителю ушёл ICMP «Fragmentation needed» (тип 3, код 4, MTU ' + m + ')' });
    return { ok: false, why: local ? 'Message too long' : 'Frag needed', pk: pk };
  };

  // ping с размером и флагом DF: o = {size, mode: do|want|dont, count}
  P.pingSized = function (id, dst, style, o) {
    var s = this, cnt = o.count, total = o.size + 28;
    function attempt(df, local) { var c = s._mtuPing = { size: total, df: df, local: local }, r;
      try { r = s.ping(id, dst); } finally { s._mtuPing = null; } return { r: r, hit: c.hit || null }; }
    var res = [], a, hit = null, localErr = false;
    if (EL.ip.ip2n(dst) === null) return this.pingText(id, dst, style);
    s.pmtu = s.pmtu || {}; var key = id + '|' + dst, known = s.pmtu[key];
    if (o.mode === 'dont' || (o.mode === 'want' && known)) { a = attempt(false, 'frag'); for (var i = 0; i < cnt; i++) res.push(a.r.ok ? 'ok' : 'lost'); }
    else {
      a = attempt(true, o.mode === 'do' ? 'err' : 'frag'); hit = a.hit;
      if (hit && hit.local) localErr = true;
      else if (hit && o.mode === 'want') {                  // узнали MTU пути — дальше режем сами
        s.pmtu[key] = hit.mtu; res.push('frag'); var b = attempt(false, 'frag'); for (var j = 1; j < cnt; j++) res.push(b.r.ok ? 'ok' : 'lost'); a = b;
      } else for (var k = 0; k < cnt; k++) res.push(a.r.ok ? 'ok' : hit ? 'frag' : 'lost');
    }
    if (this.onTrace) this.onTrace(a.r, id, dst);
    var ok = res.filter(function (x) { return x === 'ok'; }).length, err = res.filter(function (x) { return x === 'frag'; }).length, hops = (a.r.hops || []).length;
    var mtu = hit ? hit.mtu : DEF, from = hit && hit.ip ? hit.ip : dst, loss = Math.round((cnt - ok) / cnt * 100);
    if (style === 'linux' || style === 'esr') {
      if (localErr) return (style === 'esr' ? 'PING ' + dst + ' (' + dst + ') ' + o.size + '(' + total + ') bytes of data.\n' : '') + 'ping: local error: message too long, mtu=' + mtu;
      var L = ['PING ' + dst + ' (' + dst + ') ' + o.size + '(' + total + ') bytes of data.'];
      res.forEach(function (x, i) { if (x === 'ok') L.push((o.size + 8) + ' bytes from ' + dst + ': icmp_seq=' + (i + 1) + ' ttl=' + (64 - hops + 1) + ' time=0.' + (600 + i * 37) + ' ms');
        if (x === 'frag') L.push('From ' + from + ' icmp_seq=' + (i + 1) + ' Frag needed and DF set (mtu = ' + mtu + ')'); });
      L.push('', '--- ' + dst + ' ping statistics ---', cnt + ' packets transmitted, ' + ok + ' received, ' + (err ? '+' + err + ' errors, ' : '') + loss + '% packet loss, time ' + (cnt - 1) * 1001 + 'ms');
      return L.join('\n');
    }
    if (style === 'vpc') return res.map(function (x, i) { return x === 'ok' ? total + ' bytes from ' + dst + ' icmp_seq=' + (i + 1) + ' ttl=' + (64 - hops + 1) + ' time=' + (0.5 + (i + 1) * 0.13).toFixed(3) + ' ms'
      : dst + ' icmp_seq=' + (i + 1) + ' timeout'; }).join('\n');
    var M = res.map(function (x) { return x === 'ok' ? 'Reply Received From :' + dst + ', TimeTaken : 1 msecs' : 'Reply Not Received From : ' + dst + ', Timeout : 5 secs'; });
    return M.concat(['', '--- ' + dst + ' Ping Statistics ---', cnt + ' Packets Transmitted, ' + ok + ' Packets Received, ' + loss + '% Packets Loss']).join('\n');
  };

  // ---------------------------------------------------------------- ESR: ping A.B.C.D size … strategy … packets …
  var STR = { 'disallow-fragmentation': 'do', 'discovery-pmtu': 'want', 'allow-fragmentation': 'dont' };
  var SKIP = { ttl: 1, timeout: 1, interval: 1, source: 1, data: 1, dscp: 1 };
  S.cmd('priv', 'ping <ip> <rest>', function (st, a) {
    var w = String(a[1]).trim().split(/\s+/), o = { size: 56, mode: 'want', count: 5 };
    for (var i = 0; i < w.length; i++) { var k = w[i].toLowerCase(), v = w[i + 1];
      if (k === 'size') { if (!/^\d+$/.test(v || '') || +v < 1 || +v > 65468) return 'Syntax error: Illegal parameter'; o.size = +v; i++; }
      else if (k === 'packets') { if (!/^\d+$/.test(v || '') || +v < 1) return 'Syntax error: Illegal parameter'; o.count = Math.min(+v, 100); i++; }
      else if (k === 'strategy') { if (!STR[v]) return 'Syntax error: Illegal parameter'; o.mode = STR[v]; i++; }
      else if (k === 'detailed') continue;
      else if (SKIP[k] && v) i++;
      else return 'Syntax error: Unknown command'; }
    return st.net ? st.net.pingSized(st.dev, a[0], 'esr', o) : ''; }, 'Ping с размером (size), числом (packets) и стратегией DF (strategy)');

  // ---------------------------------------------------------------- MES 10.x: ping A.B.C.D [size N] [df-bit] [count N]
  function mcmd(modes, pat, fn, d) { var n = CMDS.length; E.cmd(modes, pat, fn); var c = CMDS.splice(n, 1)[0]; c.dl = ['10']; if (d) c.d = d; CMDS.unshift(c); return c; }
  function mesPing(st, a) {
    var w = String(a[1]).trim().split(/\s+/), o = { size: 56, mode: 'dont', count: 5 };
    for (var i = 0; i < w.length; i++) { var k = w[i].toLowerCase(), v = w[i + 1];
      if (k === 'size') { if (!/^\d+$/.test(v || '') || +v < 36 || +v > 2080) return '% Invalid input detected'; o.size = +v; i++; }
      else if (k === 'count' || k === 'repeat') { if (!/^\d+$/.test(v || '') || +v < 1 || +v > 10) return '% Invalid input detected'; o.count = +v; i++; }
      else if (k === 'df-bit') o.mode = 'do';
      else if ((k === 'timeout' || k === 'source' || k === 'data') && v) i++;
      else if (k === 'validate') continue;
      else return '% Invalid input detected'; }
    return st.net ? st.net.pingSized(st.dev, a[0], 'mes', o) : '% Нет сети';
  }
  mcmd('user priv', 'ping <ip> <rest>', mesPing, 'Ping: size 36–2080, df-bit, count 1–10');
  mcmd(E.CFG, 'do ping <ip> <rest>', mesPing);

  // ---------------------------------------------------------------- VPC и Debian: разбор ключей (hosts.js вызывает EL.pingArgs)
  EL.pingArgs = function (t, style) {
    var o = { size: 56, mode: style === 'vpc' ? 'dont' : 'want', count: style === 'vpc' ? 5 : 4 }, dst = null, sized = false;
    for (var i = 0; i < t.length; i++) { var x = t[i], v = t[i + 1];
      if (/^\d+\.\d+\.\d+\.\d+$/.test(x)) dst = x;
      else if (style === 'vpc' && x === '-l' && /^\d+$/.test(v || '')) { o.size = +v; sized = true; i++; }
      else if (style === 'vpc' && x === '-D') { o.mode = 'do'; sized = true; }
      else if (style === 'linux' && x === '-s' && /^\d+$/.test(v || '')) { o.size = +v; sized = true; i++; }
      else if (style === 'linux' && x === '-M' && /^(do|want|dont)$/.test(v || '')) { o.mode = v; sized = true; i++; }
      else if (x === '-c' && /^\d+$/.test(v || '')) { o.count = Math.max(1, Math.min(+v, 100)); sized = true; i++; } }
    return { dst: dst, opt: sized ? o : null };
  };
})(typeof window !== 'undefined' ? window : global);
