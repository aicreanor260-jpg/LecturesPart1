/* Ветка 10.x (MES14xx/24xx/3400/37xx, ПО 10.4.6): сверка с прошивкой и руководством 10.4.6.
   Общий движок коммутатора (_dk_cli.js) пишет часть команд синтаксисом ветки 6.x — в диалекте 10 их нет, вместо них:
   write memory → write startup-config;  ip default-gateway → ip route 0.0.0.0 0.0.0.0 <next-hop>;  clock timezone → clock utc-offset;
   show version / show system → show system information, show system id;  show arp → show ip arp;  clear arp-cache → clear ip arp;
   show mac address-table → show mac-address-table;  clear mac address-table dynamic → clear mac-address-table dynamic;
   show ports monitor → show monitor session {<id>|all} [detail];  vlan database → vlan 10,20 прямо в config;
   terminal datadump, ip ssh server, ip http server, line: login-attempts / history size — в 10.x нет;
   switchport trunk allowed vlan add/remove — в 10.x нет: trunk пропускает все VLAN, выбор VLAN — switchport mode general +
   switchport general allowed vlan add … tagged. Лабы NTF2 (методички на синтаксисе 6.x) идут на MES2300-24, ветка 6.x.
   Storm-control 10.x (единица обязательна) — в l2sec.js. Модуль грузится после всех модулей MES, чтобы закрыть их команды. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, CMDS = E.CMDS, CFG = E.CFG;
  function find(pat) { return CMDS.filter(function (c) { return c.pat.join(' ') === pat; }); }
  function run(pat) { var c = find(pat).filter(function (x) { return !x.dl || x.dl.indexOf('10') >= 0; })[0]; return c ? c.run : function () { return ''; }; }
  function cmd(modes, pat, fn, d) { var n = CMDS.length; E.cmd(modes, pat, fn); var c = CMDS.splice(n, 1)[0]; c.dl = ['10']; if (d) c.d = d; CMDS.unshift(c); return c; }
  function both(pat, fn, d) { cmd('priv', pat, fn, d); cmd(CFG, 'do ' + pat, fn); }

  // старые обработчики — до закрытия, чтобы формы 10.x делали то же самое
  var verRun = run('show version'), sysRun = run('show system'), arpRun = run('show arp'), arpClr = run('clear arp-cache'),
      macRun = run('show mac address-table'), macAge = run('show mac address-table aging-time'), macClr = run('clear mac address-table dynamic'), monRun = run('show monitor session <n>');

  // ---------------------------------------------------------------- закрыть в диалекте 10
  var CLOSED = ['write memory', 'ip default-gateway <ip>', 'no ip default-gateway', 'clock timezone <w> <w>', 'no clock timezone',
    'terminal datadump', 'terminal no datadump', 'vlan database', 'ip ssh server', 'no ip ssh server', 'ip http server', 'no ip http server',
    'login-attempts <n>', 'history size <n>',
    'switchport trunk allowed vlan add <list>', 'switchport trunk allowed vlan remove <list>'];   // 10.x: trunk пропускает все VLAN, выбор — mode general
  ['show version', 'show system', 'show arp', 'clear arp-cache', 'show mac address-table', 'show mac address-table aging-time',
    'clear mac address-table dynamic', 'show ports monitor'].forEach(function (p) { CLOSED.push(p, 'do ' + p); });
  CLOSED.forEach(function (p) { find(p).forEach(function (c) { if (!c.dl || c.dl.indexOf('10') >= 0) c.xdl = (c.xdl || []).concat('10'); }); });
  EL.mes10 = { closed: CLOSED };
  // 10.x: порт trunk передаёт с тегом все VLAN коммутатора (кроме native) — отмечаем порт при переводе в trunk
  find('switchport mode trunk').forEach(function (c) { var r0 = c.run;
    c.run = function (st) { var r = r0.apply(this, arguments); if ((st.dialect || '10') === '10' && st.ctx && st.ctx.ports)
      st.ctx.ports.forEach(function (k) { var p = st.ports[k] || (st.pos || {})[k]; if (p) p.allAll = true; }); return r; }; });

  // ---------------------------------------------------------------- варианты 10.x
  cmd('priv', 'write startup-config', function (st) { return EL.mes.save(st); }, 'Сохранить конфигурацию');
  cmd('config', 'clock utc-offset <w>', function (st, a) { var h = +a[0];
    if (!/^[+-]?\d{1,2}$/.test(a[0]) || h < -12 || h > 14) return '% Смещение от UTC: -12..+14';
    delete st.tzn; st.tzo = h; }, 'Смещение от UTC (часовой пояс)');
  cmd('config', 'no clock utc-offset', function (st) { delete st.tzn; delete st.tzo; });
  both('show system information', function (st) { return sysRun(st); }, 'Сведения о системе и ПО');
  both('show system id', function (st) { var b = String(st.bmac || '').replace(/:/g, '').toUpperCase();
    return 'Unit    Serial number\n----    -------------\n1       ES' + (b.slice(-8) || '00000000'); }, 'Серийный номер');
  both('show ip arp', function (st) { return arpRun(st); }, 'ARP-таблица');
  both('show ip arp <rest>', function (st) { return arpRun(st); });
  both('clear ip arp', function (st) { return arpClr(st); }, 'Очистить ARP-таблицу');
  both('show mac-address-table', function (st) { return macRun(st); }, 'Таблица MAC-адресов');
  // параметры show mac-address-table по руководству 10.4.6; «show mac address-table» (6.x) сюда не попадает
  var MACW = ['aging-time', 'vlan', 'interface', 'address', 'static', 'dynamic', 'count', 'multicast'];
  both('show mac-address-table <rest>', function (st, a) { var w = String(a[0]).split(/\s+/)[0].toLowerCase();
    if (MACW.indexOf(w) < 0) return '% Invalid input detected'; return w === 'aging-time' ? macAge(st) : macRun(st); });
  both('clear mac-address-table dynamic', function (st) { return macClr(st); }, 'Очистить динамические MAC-записи');
  both('clear mac-address-table dynamic <rest>', function (st) { return macClr(st); });
  both('show monitor session all', function (st) { var m = st.mon || {}, k = Object.keys(m);
    return k.length ? k.map(function (n) { return monRun(st, [+n]); }).join('\n\n') : '% Сессии зеркалирования не настроены'; }, 'Все сессии зеркалирования');
  both('show monitor session <n> detail', function (st, a) { return monRun(st, [a[0]]); });
  both('show monitor session all detail', function (st) { var m = st.mon || {};
    return Object.keys(m).map(function (n) { return monRun(st, [+n]); }).join('\n\n') || '% Сессии зеркалирования не настроены'; });

  // ---------------------------------------------------------------- running-config 10.x
  // общий движок пишет блок «vlan database» и строки ветки 6.x — в 10.x VLAN задаются из config, шлюз — маршрутом
  E.RUNX.push(function (st, o) {
    if (st.dialect && st.dialect !== '10') return;
    var out = [], inDb = false;
    o.forEach(function (l) {
      if (l === 'vlan database') { inDb = true; return; }
      if (inDb) { if (l === 'exit') { inDb = false; return; }
        var m = l.match(/^ vlan (\d+) name (.+)$/); if (m) { out.push('vlan ' + m[1], ' name ' + m[2], 'exit'); return; }
        out.push(l.replace(/^ /, ''), 'exit'); return; }
      var g = l.match(/^ip default-gateway (\S+)$/); if (g) { out.push('ip route 0.0.0.0 0.0.0.0 ' + g[1]); return; }
      if (l === 'ip ssh server' || l === 'no ip http server' || /^ (login-attempts|history size) /.test(l)) return;
      out.push(l);
    });
    // статические маршруты коммутатора (ip route NET MASK NH) — в running-config, чтобы конфигурация восстанавливалась целиком
    (st.routes || []).forEach(function (r) { var c = EL.ip.parseCidr(r.net); if (c) out.push('ip route ' + c.ip + ' ' + EL.ip.len2mask(c.len) + ' ' + r.nh); });
    if (st.tzo !== undefined && !st.tzn) out.push('clock utc-offset ' + (st.tzo >= 0 ? '+' : '') + st.tzo);
    o.length = 0; out.forEach(function (l) { o.push(l); });
  });
})(typeof window !== 'undefined' ? window : global);
