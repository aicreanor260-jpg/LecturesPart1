/* Физический уровень: кабель/трансивер, автосогласование, скорость и дуплекс.
   MES (руководства 10.4.6 и 6.6.8.8): speed 10|100|1000|10000, duplex full|half (по умолчанию full), negotiation / no negotiation (по умолчанию включено).
   ESR (справочник 1.23): speed <10M|100M|1000M|10G|25G|40G|auto> <full-duplex|half-duplex>, no speed (по умолчанию auto).
   Кабель линка: медь (RJ-45; в порт SFP+ — через медный модуль 1000BASE-T), оптика SFP 1G, оптика SFP+ 10G.
   Правила: медь — скорость согласуется (максимум 1G); оптика — скорость модуля, медный порт gi оптику не принимает, SFP+ 10G в порт 1G — нет линка.
   Одна сторона принудительно (без автосогласования), другая auto — auto-сторона определяет скорость, но выбирает half-duplex (как в стандарте 802.3):
   несовпадение дуплекса — линк есть, но на full-стороне растут FCS-ошибки, на half-стороне — поздние коллизии. Разные принудительные скорости — линка нет.
   Упрощение: кадры при несовпадении дуплекса не теряются (потери не моделируются), только ошибки в счётчиках. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, S = EL.esr, P = EL.Net.prototype, CMDS = E.CMDS;
  var CAB = { cu: 'Медь (RJ-45)', sfp1g: 'Оптика SFP 1G', sfp10g: 'Оптика SFP+ 10G' };
  EL.CABLES = CAB;
  function xg(port) { return /^(te|tw|fo|hu)/.test(port) || /^1\/0\//.test(port); }       // порт SFP+ и выше (MES 8.x — 1/0/N, 10G)
  function maxOf(port) { return xg(port) ? 10000 : 1000; }
  // настройки порта: auto или принудительно
  function cfg(net, id, port) {
    var d = net.devs[id];
    if (d.type === 'mes') { var p = d.st.ports[port] || {}; return p.neg === false ? { auto: false, speed: p.speed || maxOf(port), duplex: p.duplex || 'full' } : { auto: true }; }
    if (d.type === 'esr') { var x = d.st.run.ifs[port] || {}; return x.speed ? { auto: false, speed: x.speed, duplex: x.duplex || 'full' } : { auto: true }; }
    return { auto: true };
  }
  P.defaultCable = function (a, ap, b, bp) { return xg(ap) && xg(bp) ? 'sfp10g' : 'cu'; };
  // результат согласования на линке: {up, speed, dup: {devId: full|half}, mismatch, why}
  P.phys = function (id, port) {
    var pr = this.peer(id, port); if (!pr) return { up: false, why: 'нет кабеля' };
    var l = this.links[pr.li], cab = l.cab || this.defaultCable(l.a.dev, l.a.port, l.b.dev, l.b.port);
    var A = { id: id, port: port, c: cfg(this, id, port) }, B = { id: pr.dev, port: pr.port, c: cfg(this, pr.dev, pr.port) }, out = { dup: {} };
    if (cab !== 'cu') {
      var fs = cab === 'sfp10g' ? 10000 : 1000;
      var bad = [A, B].filter(function (x) { return !xg(x.port); })[0];
      if (bad) return { up: false, why: CAB[cab] + ': порт ' + bad.port + ' — медный, оптический модуль в него не вставить' };
      if (fs > Math.min(maxOf(A.port), maxOf(B.port))) return { up: false, why: 'модуль ' + CAB[cab] + ' не работает в порту 1G' };
      var f2 = [A, B].filter(function (x) { return !x.c.auto && x.c.speed !== fs; })[0];
      if (f2) return { up: false, why: 'на ' + f2.port + ' задана скорость ' + f2.c.speed + ', а оптика работает только на ' + fs };
      out.up = true; out.speed = fs; out.dup[A.id] = out.dup[B.id] = 'full'; out.cab = cab; return out;
    }
    var mx = Math.min(1000, maxOf(A.port), maxOf(B.port));
    var over = [A, B].filter(function (x) { return !x.c.auto && x.c.speed > mx; })[0];
    if (over) return { up: false, why: 'скорость ' + over.c.speed + ' на ' + over.port + ' по меди невозможна' };
    if (A.c.auto && B.c.auto) { out.speed = mx; out.dup[A.id] = out.dup[B.id] = 'full'; }
    else if (!A.c.auto && !B.c.auto) {
      if (A.c.speed !== B.c.speed) return { up: false, why: 'разные принудительные скорости: ' + A.c.speed + ' и ' + B.c.speed };
      out.speed = A.c.speed; out.dup[A.id] = A.c.duplex; out.dup[B.id] = B.c.duplex;
    } else {
      var F = A.c.auto ? B : A, Au = A.c.auto ? A : B;
      if (F.c.speed === 1000) return { up: false, why: '1000BASE-T требует автосогласования, а на ' + F.port + ' оно выключено' };
      out.speed = F.c.speed; out.dup[F.id] = F.c.duplex; out.dup[Au.id] = 'half';     // параллельное определение: скорость — да, дуплекс — half
    }
    if (A.id === B.id) out.dup[A.id] = 'full';
    out.up = true; out.cab = cab; out.mismatch = out.dup[A.id] !== out.dup[B.id]; return out;
  };
  var linkUp0 = P.linkUp;
  P.linkUp = function (id, port) { return linkUp0.call(this, id, port) && this.phys(id, port).up; };
  // ошибки при несовпадении дуплекса: каждый кадр по такому линку — FCS-ошибка у full-стороны, поздняя коллизия у half-стороны
  var seg0 = P.countSeg;
  P.countSeg = function (sg) {
    var r = seg0.apply(this, arguments), l = this.links[sg.li]; if (!l) return r;
    var ph = this.phys(l.a.dev, l.a.port); if (!ph.up || !ph.mismatch) return r;
    var s = this; [[l.a.dev, l.a.port], [l.b.dev, l.b.port]].forEach(function (e) { var c = s.ctrOf(e[0], e[1]); if (ph.dup[e[0]] === 'full') c.ie++; else c.oe++; });
    return r;
  };
  // кабель на линке: при прокладке и в файле схемы
  var con0 = P.connect;
  P.connect = function (a, ap, b, bp, cab) { var r = con0.call(this, a, ap, b, bp); if (!r && cab && CAB[cab]) this.links[this.links.length - 1].cab = cab; return r; };
  var json0 = P.toJSON;
  P.toJSON = function () { var j = json0.call(this), s = this; j.links.forEach(function (x, i) { if (s.links[i].cab) x.push(s.links[i].cab); }); return j; };
  var from0 = EL.Net.fromJSON;
  EL.Net.fromJSON = function (j) { var n = from0(j); (j.links || []).forEach(function (l) { if (!l[4] || !CAB[l[4]]) return;
    var a = n.byName(l[0]), b = n.byName(l[2]); n.links.forEach(function (x) { if (x.a.dev === (a && a.id) && x.a.port === l[1] && x.b.dev === (b && b.id) && x.b.port === l[3]) x.cab = l[4]; }); }); return n; };

  // ---------------------------------------------------------------- MES
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k]; }).filter(Boolean) : null; }
  function each(st, f) { var p = ports(st); if (!p) return '% Команда доступна в настройке порта'; p.forEach(f); }
  mcmd(['10', '6'], 'if range', 'speed <n>', function (st, a) { if ([10, 100, 1000, 10000].indexOf(a[0]) < 0) return '% Invalid input'; return each(st, function (p) { p.speed = a[0]; }); }, 'Скорость порта (при no negotiation)');
  mcmd(['10', '6'], 'if range', 'no speed', function (st) { return each(st, function (p) { delete p.speed; }); });
  mcmd(['10', '6'], 'if range', 'duplex <w>', function (st, a) { if (a[0] !== 'full' && a[0] !== 'half') return '% Invalid input'; return each(st, function (p) { p.duplex = a[0]; }); }, 'Дуплекс full | half');
  mcmd(['10', '6'], 'if range', 'no duplex', function (st) { return each(st, function (p) { delete p.duplex; }); });
  mcmd(['10', '6'], 'if range', 'negotiation', function (st) { return each(st, function (p) { delete p.neg; }); }, 'Включить автосогласование');
  mcmd(['10', '6'], 'if range', 'no negotiation', function (st) { return each(st, function (p) { p.neg = false; }); }, 'Выключить автосогласование');
  E.PORTX.push(function (st, k, p, d) { if (p.speed) d.push(' speed ' + p.speed); if (p.duplex && p.duplex !== 'full') d.push(' duplex ' + p.duplex); if (p.neg === false) d.push(' no negotiation'); });
  // show interfaces status — формат руководства 6.6.8.8
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function mesStatus(st) {
    var s = st.net, o = ['                                             Flow Link          Back   Mdix', 'Port     Type         Duplex  Speed Neg      ctrl State       Pressure Mode    Port Mode',
      '-------- ------------ ------  ----- -------- ---- ----------- -------- ------- --------------------'];
    Object.keys(st.ports).forEach(function (k) { var p = st.ports[k], ph = s ? s.phys(st.dev, k) : { up: false }, up = !p.shut && s && s.linkUp(st.dev, k);
      var ty = xg(k) ? '10G-Fiber' : '1G-Copper', md = p.mode === 'access' ? 'Access' : p.mode === 'trunk' ? 'Trunk' : 'General';
      o.push(rp(k, 9) + rp(ty, 13) + (up ? rp(ph.dup[st.dev] === 'half' ? 'Half' : 'Full', 8) + rp(ph.speed, 6) + rp(p.neg === false ? 'Disabled' : 'Enabled', 9) + 'Off  ' + rp('Up', 12) + 'Disabled Off     '
        : rp('  --', 8) + rp('  --', 6) + rp('   --', 9) + ' --  ' + rp(p.shut ? 'Down (Adm)' : 'Down', 12) + '   --     --     ') + md); });
    return o.join('\n');
  }
  ['', 'do '].forEach(function (pre) { mcmd(['10', '6'], pre ? E.CFG : 'priv', pre + 'show interfaces status', mesStatus, 'Состояние портов'); });
  // ---------------------------------------------------------------- ESR
  var SP = { '10m': 10, '100m': 100, '1000m': 1000, '10g': 10000, '25g': 25000, '40g': 40000 };
  function eeach(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k], k); }); st.pending = true; }
  S.cmd('gi', 'speed <w> <w>', function (st, a) { var sp = SP[a[0].toLowerCase()];
    if (!sp || (a[1] !== 'full-duplex' && a[1] !== 'half-duplex')) return 'Syntax error: Illegal parameter';
    var bad = null; eeach(st, function (x, k) { if (sp > maxOf(k)) bad = 'Syntax error: Illegal parameter'; else { x.speed = sp; x.duplex = a[1] === 'full-duplex' ? 'full' : 'half'; } }); return bad; }, 'Скорость и дуплекс');
  S.cmd('gi', 'speed auto', function (st) { eeach(st, function (x) { delete x.speed; delete x.duplex; }); }, 'Автосогласование');
  S.cmd('gi', 'no speed', function (st) { eeach(st, function (x) { delete x.speed; delete x.duplex; }); });
  S.RUNX.push(function (c, o) { Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k]; if (!x.speed) return;
    var t = { 10: '10M', 100: '100M', 1000: '1000M', 10000: '10G', 25000: '25G', 40000: '40G' }[x.speed];
    o.push('interface ' + S.longIf(k), '  speed ' + t + ' ' + (x.duplex === 'half' ? 'half-duplex' : 'full-duplex'), 'exit'); }); });
  // MES/ESR show interfaces <порт> и сводка в console.js берут скорость отсюда
  P.physText = function (id, port) { var ph = this.phys(id, port); return ph.up ? (ph.dup[id] === 'half' ? 'Half' : 'Full') + '-duplex, ' + ph.speed + 'Mbps' : 'Duplex unknown, speed unknown'; };
})(typeof window !== 'undefined' ? window : global);
