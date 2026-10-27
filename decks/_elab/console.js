/* Живая консоль MES и ESR (поведение «как на железе»):
   — фильтры вывода «|»: ESR — begin, count, counter, include, exclude, until (справочник ESR-Series CLI 1.23, шаблон — регулярное выражение);
     MES — include "s" [exclude "s2"], exclude, begin, section "s" ["s2" | include "s2" | exclude "s2"], no-more (руководство MES 8.4.0.7, 6.2,
     регистр не учитывается). В руководствах 10.4.6 и 6.6.8.8 фильтры не описаны — для веток 10 и 6 работают так же, как в 8.4;
   — постраничный вывод: длина страницы и строка «More…» по руководствам (ESR 1.23, MES 6.6.8.8, MES 8.4.0.7), terminal datadump / terminal length;
   — системные сообщения о смене состояния порта, STP, OSPF, VRRP: в консоль (logging console) и в буфер (show logging);
     MES 10.x — формат из «Руководства по сообщениям Syslog MES14xx/24xx/3400/37xx» (CFA-…, AST-…);
   — счётчики кадров на портах: считаются по кадрам модели (ARP, IP, BPDU), show interfaces counters, clear counters. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, S = EL.esr, P = EL.Net.prototype, CMDS = E.CMDS, CFG = E.CFG;

  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function rpad(s, n) { s = String(s); while (s.length < n) s += ' '; return s; }
  function lpad(s, n) { s = String(s); while (s.length < n) s = ' ' + s; return s; }
  function isNet(d) { return d && (d.type === 'mes' || d.type === 'esr'); }

  // ================================================================ фильтры вывода
  var KW = { esr: ['begin', 'count', 'counter', 'include', 'exclude', 'until'], mes: ['begin', 'exclude', 'include', 'section', 'no-more'] };
  var KWD = { begin: 'Begin with the line that matches', count: 'Count the number of lines', counter: 'Add line numbers', include: 'Include lines that match',
              exclude: 'Exclude lines that match', until: 'Print up to the line that matches', section: 'Filter a section of output', 'no-more': 'Display without pagination' };
  // первый «|» вне кавычек
  function splitPipe(line) {
    var q = null;
    for (var i = 0; i < line.length; i++) { var ch = line.charAt(i);
      if (q) { if (ch === q) q = null; continue; }
      if (ch === '"' || ch === "'" || ch === '“') { q = ch === '“' ? '”' : ch; continue; }
      if (ch === '|') return { cmd: line.slice(0, i).trim(), filt: line.slice(i + 1) };
    }
    return null;
  }
  // аргументы фильтра: слова и строки в кавычках
  function words(s) { var out = [], re = /"([^"]*)"|'([^']*)'|“([^”]*)”|(\S+)/g, m;
    while ((m = re.exec(s))) out.push(m[1] !== undefined ? m[1] : m[2] !== undefined ? m[2] : m[3] !== undefined ? m[3] : m[4]); return out; }
  function kwOf(kind, w) { if (!w) return null; w = w.toLowerCase(); var L = KW[kind];
    if (L.indexOf(w) >= 0) return w; var c = L.filter(function (k) { return k.indexOf(w) === 0; }); return c.length === 1 ? c[0] : c.length ? 'ambiguous' : null; }
  function esrFilter(lines, a) {
    var k = kwOf('esr', a[0]), pat = a.slice(1).join(' '), re;
    if (!k || k === 'ambiguous') return { err: 'Syntax error: Unknown command' };
    if (k === 'counter') return { lines: lines.map(function (x, i) { return (i + 1) + ': ' + x; }) };
    if (k === 'count') return { lines: [String(lines.length)] };
    if (!pat) return { err: 'Syntax error: Incomplete command' };
    try { re = new RegExp(pat); } catch (e) { return { err: 'Syntax error: Illegal parameter' }; }
    var i = lines.findIndex(function (x) { return re.test(x); });
    if (k === 'include') return { lines: lines.filter(function (x) { return re.test(x); }) };
    if (k === 'exclude') return { lines: lines.filter(function (x) { return !re.test(x); }) };
    if (k === 'begin') return { lines: i < 0 ? [] : lines.slice(i) };
    return { lines: i < 0 ? lines : lines.slice(0, i) };     // until
  }
  function has(x, s) { return x.toLowerCase().indexOf(String(s).toLowerCase()) >= 0; }
  function mesFilter(lines, a) {
    var k = kwOf('mes', a[0]);
    if (!k || k === 'ambiguous') return { err: "% Invalid input detected at '^' marker." };
    if (k === 'no-more') return { lines: lines, noMore: true };
    if (a.length < 2) return { err: '% Incomplete command' };
    var s = a[1], tail = a.slice(2);
    if (k === 'include' && tail[0] && tail[0].toLowerCase() === 'exclude' && tail[1]) return { lines: lines.filter(function (x) { return has(x, s) && !has(x, tail[1]); }) };
    if (k === 'include') return { lines: lines.filter(function (x) { return has(x, s); }) };
    if (k === 'exclude') return { lines: lines.filter(function (x) { return !has(x, s); }) };
    if (k === 'begin') { var i = lines.findIndex(function (x) { return has(x, s); }); return { lines: i < 0 ? [] : lines.slice(i) }; }
    // section "s" ["конец" | include "s2" | exclude "s2"]; конец секции по умолчанию — строка exit
    var endS = null, inc = null, exc = null, out = [], on = false;
    if (tail[0] && /^include$/i.test(tail[0])) inc = tail[1]; else if (tail[0] && /^exclude$/i.test(tail[0])) exc = tail[1]; else if (tail[0]) endS = tail[0];
    lines.forEach(function (x) {
      if (!on && has(x, s)) on = true;
      if (!on) return;
      if ((inc === null || has(x, inc) || has(x, s)) && (exc === null || !has(x, exc))) out.push(x);
      if (endS ? has(x, endS) && !has(x, s) : /^\s*exit\s*$/i.test(x)) on = false;
    });
    return { lines: out };
  }
  // «show … | фильтр»: команда выполняется целиком, затем вывод фильтруется
  var exec0 = P.exec;
  P.exec = function (id, line, ui) {
    var d = this.devs[id]; this.noMore = false;
    if (!isNet(d) || d.off || d.st.askPw) return exec0.apply(this, arguments);
    var sp = splitPipe(String(line)), kind = d.type === 'esr' ? 'esr' : 'mes';
    if (!sp || !sp.cmd) return exec0.apply(this, arguments);
    var a = words(sp.filt);
    if (/\?\s*$/.test(line)) return this.help(id, line.replace(/\?\s*$/, ''));
    var r = exec0.call(this, id, sp.cmd, ui);
    if (!r || /^(%|Syntax error)/.test(r)) return r;
    var f = (kind === 'esr' ? esrFilter : mesFilter)(String(r).split('\n'), a);
    if (f.err) return f.err;
    if (f.noMore) this.noMore = true;
    return f.lines.join('\n');
  };
  var help0 = P.help, tab0 = P.tab;
  function pipeHelp(d, rest) {
    var kind = d.type === 'esr' ? 'esr' : 'mes', a = rest.trim() ? rest.trim().split(/\s+/) : [], ends = /\s$/.test(rest) || !rest.trim();
    if (a.length > (ends ? 0 : 1)) return '  ' + rpad(d.type === 'esr' ? 'WORD' : 'LINE', 24) + (d.type === 'esr' ? 'Regular expression' : 'String to match');
    var part = ends ? '' : (a[0] || '').toLowerCase();
    var L = KW[kind].filter(function (k) { return k.indexOf(part) === 0; });
    return L.length ? L.map(function (k) { return '  ' + rpad(k, 24) + KWD[k]; }).join('\n') : (d.type === 'esr' ? 'Syntax error: Unknown command' : '% Unrecognized command');
  }
  P.help = function (id, line) {
    var d = this.devs[id], sp = isNet(d) && splitPipe(String(line));
    return sp && sp.cmd ? pipeHelp(d, sp.filt) : help0.apply(this, arguments);
  };
  P.tab = function (id, line) {
    var d = this.devs[id], sp = isNet(d) && splitPipe(String(line));
    if (!sp || !sp.cmd) return tab0.apply(this, arguments);
    var m = sp.filt.match(/^\s*(\S+)$/); if (!m) return null;
    var L = KW[d.type === 'esr' ? 'esr' : 'mes'].filter(function (k) { return k.indexOf(m[1].toLowerCase()) === 0; });
    return L.length === 1 ? line.replace(/\S+$/, L[0]) + ' ' : null;
  };

  // ================================================================ постраничный вывод
  // настройки сессии консоли (не сохраняются в конфигурации, сбрасываются при перезагрузке)
  P.term = function (id) { var t = (this._term = this._term || {}); return t[id] || (t[id] = { dd: false, len: 24 }); };
  P.pageLen = function (id) { var d = this.devs[id]; if (!isNet(d) || this.noMore) return 0; var t = this.term(id); return t.dd ? 0 : t.len; };
  P.moreText = function (id) {
    var d = this.devs[id];
    if (d.type === 'esr') return 'More? Enter – next line; Space – next page; Q – quit; R – show the rest.';
    return d.st.dialect === '8' ? '--More-- or (q)uit' : 'More: <space>,  Quit: q or CTRL+Z, One line: <return> ';
  };
  S.cmd('priv', 'terminal datadump', function (st) { if (st.net) st.net.term(st.dev).dd = true; }, 'Вывод без разбиения на страницы');
  S.cmd('priv', 'no terminal datadump', function (st) { if (st.net) st.net.term(st.dev).dd = false; }, 'Постраничный вывод');
  mcmd(['10', '6'], 'user priv', 'terminal datadump', function (st) { if (st.net) st.net.term(st.dev).dd = true; }, 'Вывод без разбиения на страницы');
  mcmd(['10', '6'], 'user priv', 'terminal no datadump', function (st) { if (st.net) st.net.term(st.dev).dd = false; }, 'Постраничный вывод');
  mcmd(['8'], 'priv', 'terminal length <n>', function (st, a) { if (a[0] > 512) return '% Invalid input'; if (st.net) { var t = st.net.term(st.dev); t.len = a[0]; t.dd = a[0] === 0; } }, 'Строк на странице');
  mcmd(['8'], 'priv', 'no terminal length', function (st) { if (st.net) { var t = st.net.term(st.dev); t.len = 24; t.dd = false; } });

  // ================================================================ счётчики кадров на портах
  // размеры кадров (байт, с FCS): ARP — минимальный кадр 64; ICMP echo VPCS/ping 84 байта IP + 18; TCP-сегмент без данных; UDP-служба; BPDU
  var FSZ = { arp: 64, icmp: 102, tcp: 78, udp: 110, bpdu: 64 };
  function ctr(net, id, port) { var c = (net.ctr = net.ctr || {}); c[id] = c[id] || {};
    return c[id][port] || (c[id][port] = { iu: 0, im: 0, ib: 0, io: 0, ou: 0, om: 0, ob: 0, oo: 0, ie: 0, oe: 0, drop: 0 }); }
  P.ctrOf = function (id, port) { return ctr(this, id, port); };
  // кадр прошёл по сегменту: tx на порту отправителя, rx на порту получателя
  P.countSeg = function (sg, cast, size, f) {
    var l = this.links[sg.li]; if (!l) return;
    var fp = l.a.dev === sg.from ? l.a.port : l.b.port, tp = l.a.dev === sg.to ? l.a.port : l.b.port, n = size + (sg.tag !== null && sg.tag !== undefined ? 4 : 0);
    var a = ctr(this, sg.from, fp), b = ctr(this, sg.to, tp);
    a['o' + cast]++; a.oo += n; b['i' + cast]++; b.io += n;
    if (f && this.capFrame) this.capFrame(sg, f, n);
  };
  P.countSteps = function (steps, proto) {
    var s = this;
    (steps || []).forEach(function (st) {
      if (!st.segs || st.counted) return; st.counted = true;
      var v6 = st.f && (st.f.type === 'ip6' || st.f.mcast), cast = st.k === 'arp' ? (v6 ? 'm' : 'b') : 'u', size = v6 ? (st.k === 'ip' ? 118 : 86) : st.f && st.f.dhcp ? 346 : st.k === 'ip' ? FSZ[(st.f && st.f.proto) || proto] || FSZ.icmp : FSZ.arp;
      st.segs.forEach(function (sg) { s.countSeg(sg, cast, size, st.f); });
    });
  };
  var req0 = P.request;
  P.request = function (src, dst, proto) { var r = req0.apply(this, arguments); this.countSteps(r.steps, proto || 'icmp'); return r; };
  var dhcp0 = P.dhcp;
  if (dhcp0) P.dhcp = function () { var r = dhcp0.apply(this, arguments); if (r && r.steps) this.countSteps(r.steps, 'udp'); return r; };
  // BPDU: назначенный порт коммутатора с включённым STP шлёт BPDU раз в Hello Time (2 с)
  var tick0 = P.tick;
  P.tick = function (dt) {
    var g = tick0.apply(this, arguments), s = this, acc = (s._bpduAcc = (s._bpduAcc || 0) + dt), n = Math.floor(acc / 2);
    if (n > 0) { s._bpduAcc = acc - n * 2;
      var t = s.stp();
      s.order.forEach(function (id) { var d = s.devs[id]; if (d.type !== 'mes' || d.off || (d.st.stp && d.st.stp.on === false)) return;
        Object.keys(t[id] || {}).forEach(function (ln) { if (t[id][ln].role !== 'Desg') return;
          var L = s.lports(id).filter(function (x) { return x.name === ln; })[0]; if (!L || L.cfg.stpOff) return;
          var pr = s.peer(id, L.members[0]); if (!pr) return;
          for (var i = 0; i < Math.min(n, 3600); i++) {
            var a = ctr(s, id, L.members[0]), b = ctr(s, pr.dev, pr.port); a.om++; a.oo += FSZ.bpdu; b.im++; b.io += FSZ.bpdu;
            if (s.capBpdu) s.capBpdu(id, L.members[0], ln); } }); });
    }
    if (s.onTick) s.onTick();
    return g;
  };
  // перезагрузка обнуляет счётчики, буфер журнала и настройки сессии
  var reboot0 = P.reboot, power0 = P.power;
  function resetDev(net, id) { if (net.ctr) delete net.ctr[id]; if (net._term) delete net._term[id]; var d = net.devs[id]; if (d && d.st) d.st.logb = []; }
  P.reboot = function (id) { var r = reboot0.apply(this, arguments); resetDev(this, id); return r; };
  P.power = function (id, on) { var r = power0.apply(this, arguments); if (!on) resetDev(this, id); return r; };

  function physPorts(net, id) { var d = net.devs[id]; return d.type === 'mes' ? Object.keys(d.st.ports) : Object.keys(d.st.run.ifs).filter(function (k) { return k.indexOf('.') < 0 && k.indexOf('lo') !== 0; }); }
  // MES: show interfaces counters [порт] — таблицы как в руководстве 6.6.8.8
  function mesCounters(st, list) {
    var s = st.net; if (!s) return '';
    var L = list || physPorts(s, st.dev), one = list && list.length === 1;
    function tab(head, f) { return [rpad('      Port', 17) + head, '---------------- ------------ ------------ ------------ ------------'].concat(L.map(function (p) {
      var c = s.ctrOf(st.dev, p); return rpad('    ' + p, 16) + f(c).map(function (v) { return lpad(v, 13); }).join(''); })); }
    var o = tab('InUcastPkts  InMcastPkts  InBcastPkts    InOctets', function (c) { return [c.iu, c.im, c.ib, c.io]; })
      .concat([''], tab('OutUcastPkts OutMcastPkts OutBcastPkts  OutOctets', function (c) { return [c.ou, c.om, c.ob, c.oo]; }));
    if (one) { var c = s.ctrOf(st.dev, L[0]);
      o.push('', 'Alignment Errors: 0', 'FCS Errors: ' + c.ie, 'Single Collision Frames: 0', 'Multiple Collision Frames: 0', 'SQE Test Errors: 0',
        'Deferred Transmissions: 0', 'Late Collisions: ' + c.oe, 'Excessive Collisions: 0', 'Carrier Sense Errors: 0', 'Oversize Packets: 0',
        'Internal MAC Rx Errors: 0', 'Symbol Errors: 0', 'Received Pause Frames: 0', 'Transmitted Pause Frames: 0'); }
    return o.join('\n');
  }
  // MES: show interfaces <порт> — состояние и статистика порта (формат в руководствах не приведён — сводка по полям руководства)
  function mesIf(st, p) {
    var s = st.net, x = st.ports[p]; if (!x) return '% Interface does not exist';
    var up = s && s.linkUp(st.dev, p), c = s ? s.ctrOf(st.dev, p) : ctr({}, 0, p);
    return [E.longIf(p).replace(' ', '') + ' is ' + (x.shut ? 'administratively down' : up ? 'up (connected)' : 'down (not connected)'),
      '  Hardware is ' + (/^te/.test(p) ? '10G-Fiber' : '1G-Copper') + ', MAC address is ' + EL.mac(st.host + p),
      '  Interface MTU is 1500', '  ' + (s && s.physText ? s.physText(st.dev, p) : 'Duplex unknown, speed unknown') + ', auto negotiation ' + (x.neg === false ? 'disabled' : 'enabled'),
      '  ' + (c.iu + c.im + c.ib) + ' packets input, ' + c.io + ' bytes',
      '  Received ' + c.ib + ' broadcasts, ' + c.im + ' multicasts', '  ' + c.ie + ' input errors, ' + c.ie + ' FCS',
      '  ' + (c.ou + c.om + c.ob) + ' packets output, ' + c.oo + ' bytes', '  ' + c.oe + ' output errors, ' + c.oe + ' collisions'].join('\n');
  }
  function mesClear(st, list) { var s = st.net; if (!s) return; (list || physPorts(s, st.dev)).forEach(function (p) { if (s.ctr && s.ctr[st.dev]) delete s.ctr[st.dev][p]; }); }
  ['', 'do '].forEach(function (pre) { var m = pre ? CFG : 'priv';
    mcmd(['10', '6', '8'], m, pre + 'show interfaces counters', function (st) { return mesCounters(st); }, 'Счётчики кадров на портах');
    mcmd(['10', '6', '8'], m, pre + 'show interfaces counters <if>', function (st, a) {
      var bad = a[0].filter(function (p) { return !st.ports[p]; }); return bad.length ? '% Interface does not exist' : mesCounters(st, a[0]); });
    mcmd(['10', '6', '8'], m, pre + 'show interfaces <if>', function (st, a) { return a[0].map(function (p) { return mesIf(st, p); }).join('\n\n'); }, 'Состояние и статистика порта');
  });
  mcmd(['10', '6', '8'], 'priv', 'clear counters', function (st) { mesClear(st); }, 'Сбросить счётчики');
  mcmd(['10', '6', '8'], 'priv', 'clear counters <if>', function (st, a) { mesClear(st, a[0]); });

  // ESR: show interfaces counters [<IF>] — как в справочнике 1.23
  function esrList(st, w) {
    if (!w) return physPorts(st.net, st.dev);
    var r = S.ifName(w); if (!r) return null;
    var L = r.range || [r.name]; return L.every(function (k) { return st.run.ifs[k]; }) ? L : null;
  }
  function esrCounters(st, w) {
    if (!st.net) return ''; var L = esrList(st, w), s = st.net;
    if (!L) return 'Syntax error: Illegal parameter';
    if (w && L.length === 1) { var c = s.ctrOf(st.dev, L[0].split('.')[0]), rx = c.iu + c.im + c.ib, tx = c.ou + c.om + c.ob;
      return [['Packets received', rx], ['Bytes received', c.io], ['Dropped on receive', c.drop], ['Receive errors', c.ie], ['Multicasts received', c.im],
        ['Receive length errors', 0], ['Receive buffer overflow errors', 0], ['Receive CRC errors', c.ie], ['Receive frame errors', 0], ['Receive FIFO errors', 0],
        ['Receive missed errors', 0], ['Receive compressed', 0], ['Packets transmitted', tx], ['Bytes transmitted', c.oo], ['Dropped on transmit', 0],
        ['Transmit errors', c.oe], ['Transmit aborted errors', 0], ['Transmit carrier errors', 0], ['Transmit FIFO errors', 0], ['Transmit heartbeat errors', 0],
        ['Transmit window errors', 0], ['Transmit comressed', 0], ['Collisions', c.oe]].map(function (x) { return ' ' + rpad(x[0] + ':', 32) + x[1]; }).join('\n'); }
    var H = '-------------   -------------   -------------   -------------';
    return [rpad('Interface', 16) + rpad('UC recv', 16) + rpad('Bytes recv', 16) + rpad('Errors recv', 16) + 'MC recv', H + '   -------------']
      .concat(L.map(function (k) { var c = s.ctrOf(st.dev, k); return rpad(k, 16) + rpad(c.iu, 16) + rpad(c.io, 16) + rpad(c.ie, 16) + (c.im + c.ib); }),
        [rpad('Interface', 16) + rpad('UC sent', 16) + rpad('Bytes sent', 16) + 'Errors sent', H],
        L.map(function (k) { var c = s.ctrOf(st.dev, k); return rpad(k, 16) + rpad(c.ou, 16) + rpad(c.oo, 16) + c.oe; })).join('\n');
  }
  S.cmd('priv', 'show interfaces counters', function (st) { return esrCounters(st); }, 'Счётчики интерфейсов');
  S.cmd('priv', 'show interfaces counters <w>', function (st, a) { return esrCounters(st, a[0]); });
  S.cmd('priv', 'clear interfaces counters', function (st) { if (st.net && st.net.ctr) delete st.net.ctr[st.dev]; }, 'Сбросить счётчики интерфейсов');
  S.cmd('priv', 'clear interfaces counters <w>', function (st, a) { var L = st.net && esrList(st, a[0]); if (!L) return 'Syntax error: Illegal parameter';
    L.forEach(function (k) { if (st.net.ctr && st.net.ctr[st.dev]) delete st.net.ctr[st.dev][k.split('.')[0]]; }); });

  // ================================================================ системные сообщения
  // MES 10.x: CFA/AST по руководству Syslog; MES 6.x/4.x и ESR — формат %МОДУЛЬ-У-СОБЫТИЕ (в руководствах не приведён, условный)
  function sp(p) { return p.replace(/^([a-z]+)/, '$1 '); }
  function fmt(d, ev) {
    if (d.sub === 'olt' || d.sub === 'ont' || d.sub === 'ap') return null;   // формат сообщений OLT/ONT/ТД в источниках не приведён
    var b = d.type === 'mes' ? d.st.dialect : 'esr', p = ev.port;
    if (ev.k === 'link') return b === '10' || b === '8' ? (ev.up ? 'CFA-6-Interface ' + sp(p) + ' link status UP' : 'CFA-4-Interface ' + sp(p) + ' link status DOWN')
                                                          : (ev.up ? '%LINK-I-Up:  ' + p : '%LINK-W-Down:  ' + p);
    if (ev.k === 'stp') return b === '6' ? '%STP-W-PORTSTATUS: ' + p + ': STP status ' + ev.state
      : 'AST-6-' + (ev.mst ? '[Instance 0] ' : '') + 'Interface ' + sp(p) + ' is moved to state ' + ev.state;
    if (ev.k === 'root') return b === '6' ? '%STP-W-ROOT: ' + (ev.me ? 'This switch is the root' : 'Root port ' + p) : 'AST-6-' + (ev.mst ? '[Instance 0] ' : '') +
      (ev.me ? 'This is the root bridge' : 'Interface ' + sp(p) + ' is selected as root port, bridge: ' + ev.bridge);
    if (ev.k === 'bpdug') return b === '6' ? '%STP-W-PORTSTATUS: ' + p + ': BPDU Guard — port is shut down' : 'AST-6-BPDU received on Bpdu Guard enabled edge ' + sp(p) + ' interface';
    if (ev.k === 'ospf') return '%OSPF-I-NEIGHBOR: Neighbor ' + ev.rid + ' on ' + p + ' changed state to ' + ev.state;
    if (ev.k === 'vrrp') return '%VRRP-I-STATE: ' + p + ' VRID ' + ev.vrid + ' changed state to ' + ev.state;
    return '';
  }
  function snap(s) {
    var o = {}, t = s.stp(), vr = s.vrrp();
    s.dyn();
    s.order.forEach(function (id) { var d = s.devs[id]; if (!isNet(d) || d.off) return;
      physPorts(s, id).forEach(function (p) { o['L|' + id + '|' + p] = s.linkUp(id, p) ? 1 : 0;
        if (d.type === 'mes' && d.st.ports[p] && d.st.ports[p].errdis === 'bpduguard') o['B|' + id + '|' + p] = 1; });
      if (d.type === 'mes' && t[id]) { Object.keys(t[id]).forEach(function (ln) { var z = s.stpState ? s.stpState(id, ln, 0) : null;       // состояние по таймерам STP (stp_timers.js)
          o['S|' + id + '|' + ln] = z ? EL.STPN[z].charAt(0).toUpperCase() + EL.STPN[z].slice(1) : t[id][ln].fwd ? 'Forwarding' : 'Discarding';
        if (t[id][ln].role === 'Root') o['R|' + id] = ln; });
        if (s._stp && s._stp.root[id] === id && Object.keys(t[id]).length) o['R|' + id] = '*'; }
      Object.keys(vr[id] || {}).forEach(function (k) { var v = vr[id][k]; o['V|' + id + '|' + k + '|' + v.id] = v.master ? 'Master' : 'Backup'; });
    });
    var A = (s._adj || {}).O || {};
    Object.keys(A).forEach(function (k) { var r = A[k]; o['O|' + r.id + '|' + r.ifn + '|' + r.dev] = r.state === 'full' ? 'Full' : r.state === '2way' ? '2-Way' : r.state === 'exstart' ? 'ExStart' : 'Init'; });
    return o;
  }
  function logLine(s, d, msg) {
    var st = d.st, tz = (st.tzo || 0) * 3600e3, t = new Date(EL.clock.now() + (st.clk || 0) + tz), p2 = function (n) { return ('0' + n).slice(-2); };
    var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var ts = p2(t.getUTCDate()) + '-' + MON[t.getUTCMonth()] + '-' + t.getUTCFullYear() + ' ' + p2(t.getUTCHours()) + ':' + p2(t.getUTCMinutes()) + ':' + p2(t.getUTCSeconds());
    st.logb = (st.logb || []).concat([ts + ' ' + msg]).slice(-200);
    if (d.type === 'esr') s.syslog(d.id, 'messages', msg);
  }
  // сравнение с прошлым снимком: что изменилось — сообщения устройствам; quiet — только запомнить состояние
  P.events = function (quiet) {
    var s = this, now = snap(s), prev = s._ev, out = [];
    s._ev = now;
    if (!prev || quiet) return out;
    Object.keys(now).concat(Object.keys(prev).filter(function (k) { return !(k in now); })).forEach(function (k) {
      var a = prev[k], b = now[k]; if (a === b) return;
      var q = k.split('|'), id = q[1], d = s.devs[id]; if (!d || d.off) return;
      var mst = d.type === 'mes' && (d.st.stp || {}).mode === 'mst', ev = null;
      if (q[0] === 'L') { if (a === undefined && !b) return; ev = { k: 'link', port: q[2], up: !!b }; }
      else if (q[0] === 'B') { if (b) ev = { k: 'bpdug', port: q[2] }; }
      else if (q[0] === 'S') { if (b) ev = { k: 'stp', port: q[2], state: b, mst: mst }; }
      else if (q[0] === 'R') { if (b) ev = { k: 'root', port: b, me: b === '*', mst: mst, bridge: b === '*' ? '' : s.devs[s._stp.root[id]].st.bmac }; }
      else if (q[0] === 'V') { ev = { k: 'vrrp', port: q[2], vrid: q[3], state: b || 'Init' }; }
      else if (q[0] === 'O') { var nb = s.devs[q[3]]; ev = { k: 'ospf', port: q[2], state: b || 'Down',
        rid: nb ? ((nb.st.run.ospf && nb.st.run.ospf.rid) || (s.ifaces(q[3])[0] || {}).ip || q[3]) : q[3] }; }
      if (!ev) return;
      var msg = fmt(d, ev); if (!msg) return;
      (s._evlog = s._evlog || []).push({ t: s.now, dev: d.name, k: ev.k, msg: msg }); if (s._evlog.length > 2000) s._evlog.shift();   // лента событий для «Результатов»
      logLine(s, d, msg);
      if ((d.type === 'esr' ? d.st.run.logcon : d.st.logcon) !== false) out.push({ id: id, msg: msg });
    });
    return out;
  };
  // MES: logging console, show logging; ESR: сообщения идут в консоль (syslog console по умолчанию — info)
  mcmd(['10', '6', '8'], 'config', 'logging console', function (st) { st.logcon = true; }, 'Сообщения на консоль');
  mcmd(['10', '6', '8'], 'config', 'logging console <w>', function (st) { st.logcon = true; });
  mcmd(['10', '6', '8'], 'config', 'no logging console', function (st) { st.logcon = false; }, 'Не выводить сообщения на консоль');
  function showLog(st) { return (st.logb || []).slice().reverse().join('\n'); }
  ['', 'do '].forEach(function (pre) { mcmd(['10', '6', '8'], pre ? CFG : 'user priv', pre + 'show logging', showLog, 'Журнал сообщений'); });
  E.RUNX.push(function (st, o) { if (st.logcon === false) o.push('no logging console'); });
  S.cmd('config', 'no syslog console', function (st) { st.cand.logcon = false; st.pending = true; }, 'Не выводить сообщения на консоль');
  S.cmd('config', 'syslog console', function (st) { st.cand.logcon = true; st.pending = true; }, 'Сообщения syslog на консоль');
  S.RUNX.push(function (c, o) { if (c.logcon === false) o.push('no syslog console'); });
})(typeof window !== 'undefined' ? window : global);
