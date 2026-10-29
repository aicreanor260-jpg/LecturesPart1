/* Лабораторные NTF2v2, перенесённые на настоящий синтаксис MES (коммутатор) и ESR (маршрутизатор).
   Каждая лаба: gen() — случайный вариант (номера VLAN, адреса), build() — топология, tasks() — проверки, sol() — решение. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, PK = EL.pick;

  function sw(st) { return st; }
  function dev(net, n) { var d = net.byName(n); return d ? d.st : null; }
  function port(net, n, p) { var s = dev(net, n); return s && s.ports['gi1/0/' + p]; }
  function acc(net, n, ps, v) { return ps.every(function (p) { var q = port(net, n, p); return q && q.mode === 'access' && q.access === v; }); }
  function distinct(k, from) { var o = []; while (o.length < k) { var x = PK(from); if (o.indexOf(x) < 0) o.push(x); } return o; }
  // лаба начинается с выключенным оборудованием (как в pnetlab): студент включает сам — ПКМ → «Включить» или «Включить всё»
  function powerOff(net) { net.list().forEach(function (d) { net.power(d.id, false); }); }
  function apply(net, script) {                 // выполнить команды на устройствах; вернуть ошибки (для автотеста)
    var errs = [];
    Object.keys(script).forEach(function (n) {
      var d = net.byName(n.replace(/\s*#\d+$/, '')); if (!d) { errs.push('нет устройства ' + n); return; }
      script[n].forEach(function (l) { var r = net.exec(d.id, l);
        if (typeof r === 'string' && /^%|Invalid|Bad command|command not found|Error/.test(r)) errs.push(n + ' «' + l + '» → ' + r.split('\n')[0]); });
    });
    return errs;
  }
  var V10 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120];
  // по пункту на каждый ПК: [[имя, адрес, шлюз(, длина)]] — «одно действие — один пункт»
  function vpcs(L) { return L.map(function (x) { return { t: x[0] + ': ' + x[1] + '/' + (x[3] || 24) + ', шлюз ' + x[2], ok: function (n) { var d = dev(n, x[0]); return !!d && d.ip === x[1] && (d.len === undefined || d.len === (x[3] || 24)) && d.gw === x[2]; } }; }); }
  // по пункту на каждое имя: [[устройство, имя]] — для ESR смотрим применённую конфигурацию (после commit), для MES — текущую
  function names(L) { return L.map(function (x) { return { t: 'Имя ' + x[0] + ': ' + x[1] + ' (hostname ' + x[1] + ')', ok: function (n) { var d = dev(n, x[0]); return !!d && (d.run ? d.run.host : d.host) === x[1]; } }; }); }
  EL.labH = { vpcs: vpcs, names: names, dev: dev };

  var LABS = [
    // ------------------------------------------------------------ 2.1
    { id: '2.1', title: 'Создание и удаление VLAN — режимы access и trunk',
      goal: 'Освоить создание, удаление и просмотр VLAN на коммутаторе MES.',
      gen: function () { var v = distinct(5, V10).sort(function (a, b) { return a - b; }); return { v: v }; },
      build: function (net) { net.add('MES2300-24', 'SW1', 420, 260); },
      tasks: function (p) { var v = p.v; return [
        { t: 'Создайте VLAN ' + v.join(', ') + ' (vlan ' + v.join(',') + ' в режиме config) — все пять сразу или по одной', ok: function (n) { var s = dev(n, 'SW1'); return [v[0], v[1], v[2], v[4]].every(function (x) { return s.vlans[x]; }); } },
        { t: 'gi1/0/1–2 → access VLAN ' + v[0], ok: function (n) { return acc(n, 'SW1', [1, 2], v[0]); } },
        { t: 'gi1/0/11–12 → access VLAN ' + v[1], ok: function (n) { return acc(n, 'SW1', [11, 12], v[1]); } },
        { t: 'gi1/0/4–6 → access VLAN ' + v[2], ok: function (n) { return acc(n, 'SW1', [4, 5, 6], v[2]); } },
        { t: 'gi1/0/8–9 → access VLAN ' + v[4], ok: function (n) { return acc(n, 'SW1', [8, 9], v[4]); } },
        { t: 'Порт gi1/0/7 сначала в VLAN ' + v[3] + ', затем удалите VLAN ' + v[3] + ' — порт вернётся в VLAN 1', ok: function (n) { var s = dev(n, 'SW1'); return !!s.vlans[v[0]] && !s.vlans[v[3]] && port(n, 'SW1', 7).access === 1; } },
        { t: 'gi1/0/3 → trunk, разрешены VLAN ' + v[0] + ' и ' + v[1], ok: function (n) { var q = port(n, 'SW1', 3); return q.mode === 'trunk' && q.allowed.indexOf(v[0]) >= 0 && q.allowed.indexOf(v[1]) >= 0; } },
        { t: 'Сохраните конфигурацию (write)', ok: function (n) { return !!dev(n, 'SW1').startup; } }]; },
      sol: function (p) { var v = p.v; return { SW1: ['enable', 'configure', 'vlan ' + v.join(','), 'exit', 'do show vlan',
        'interface range gigabitethernet 1/0/1-2', 'switchport mode access', 'switchport access vlan ' + v[0], 'exit',
        'interface range gigabitethernet 1/0/11-12', 'switchport mode access', 'switchport access vlan ' + v[1], 'exit',
        'interface range gigabitethernet 1/0/4-6', 'switchport mode access', 'switchport access vlan ' + v[2], 'exit',
        'interface gigabitethernet 1/0/7', 'switchport mode access', 'switchport access vlan ' + v[3], 'exit',
        'interface range gigabitethernet 1/0/8-9', 'switchport mode access', 'switchport access vlan ' + v[4], 'exit',
        'do show vlan', 'no vlan ' + v[3], 'do show vlan',
        'interface gigabitethernet 1/0/3', 'switchport mode trunk', 'switchport trunk allowed vlan add ' + v[0] + ',' + v[1], 'end', 'write'] }; } },

    // ------------------------------------------------------------ 3.1
    { id: '3.1', title: 'Базовая настройка маршрутизатора',
      goal: 'Базовая настройка vESR: имя, время, адреса, Loopback, саб-интерфейс, пользователь, SSH, баннеры. Проверка с Debian.',
      gen: function () { return { x: R(1, 254), s: R(10, 99), tz: PK(['+3', '+7', '+10']), city: null }; },
      build: function (net) { var r = net.add('vESR', 'R1', 560, 260), d = net.add('Debian', 'Debian', 240, 260); net.connect(d.id, 'ens3', r.id, 'gi1/0/1'); },
      tasks: function (p) { var a = '192.168.' + p.x, s = '173.16.' + p.s;
        function run(n) { return dev(n, 'R1').run; }
        return [
        { t: 'Имя маршрутизатора R1 (не забудьте do commit и do confirm)', ok: function (n) { return run(n).host === 'R1'; } },
        { t: 'Часовой пояс GMT ' + p.tz + ' (clock timezone gmt ' + p.tz + ')', ok: function (n) { return run(n).tz === p.tz; } },
        { t: 'gi1/0/1: IP-адрес ' + a + '.1/24', ok: function (n) { var x = run(n).ifs['gi1/0/1']; return x.ip === a + '.1/24'; } },
        { t: 'gi1/0/1: межсетевой экран отключён (ip firewall disable)', ok: function (n) { return !run(n).ifs['gi1/0/1'].fw; } },
        { t: 'Loopback 1: 8.8.8.8/32', ok: function (n) { var x = run(n).ifs.lo1; return x && x.ip === '8.8.8.8/32'; } },
        { t: 'Саб-интерфейс gi1/0/1.50: ' + s + '.1/24', ok: function (n) { var x = run(n).ifs['gi1/0/1.50']; return x && x.ip === s + '.1/24'; } },
        { t: 'gi1/0/1.50: межсетевой экран отключён', ok: function (n) { var x = run(n).ifs['gi1/0/1.50']; return x && !x.fw; } },
        { t: 'Пользователь master / eltex, privilege 14', ok: function (n) { var u = run(n).users.master; return u && u.pw === 'eltex' && u.priv === 14; } },
        { t: 'SSH-сервер включён', ok: function (n) { return run(n).ssh; } },
        { t: 'banner login Router-R1', ok: function (n) { return run(n).banner.login === 'Router-R1'; } },
        { t: 'banner exec «Connect Router R1»', ok: function (n) { return run(n).banner.exec === 'Connect Router R1'; } },
        { t: 'Все изменения применены и подтверждены (commit + confirm)', ok: function (n) { var s2 = dev(n, 'R1'); return !s2.pending && !s2.unconfirmed && (s2.commits || 0) > 0; } },
        { t: 'Debian (вход root / toor): ens3 включён, адрес ' + a + '.2/24', ok: function (n) { var d = dev(n, 'Debian'); return d.up && d.ip === a + '.2' && d.len === 24; } },
        { t: 'Debian: шлюз по умолчанию ' + a + '.1', ok: function (n) { return dev(n, 'Debian').gw === a + '.1'; } },
        { t: 'ping с Debian до ' + a + '.1 проходит', ok: function (n) { return n.reach('Debian', a + '.1'); } },
        { t: 'ping с Debian до 8.8.8.8 (Loopback R1) проходит', ok: function (n) { return n.reach('Debian', '8.8.8.8'); } }]; },
      sol: function (p) { var a = '192.168.' + p.x, s = '173.16.' + p.s; return {
        R1: ['configure', 'hostname R1', 'clock timezone gmt ' + p.tz, 'interface gigabitethernet 1/0/1', 'ip address ' + a + '.1/24', 'ip firewall disable', 'exit',
             'interface loopback 1', 'ip address 8.8.8.8/32', 'exit', 'interface gigabitethernet 1/0/1.50', 'ip address ' + s + '.1/24', 'ip firewall disable', 'exit',
             'username master', 'password eltex', 'privilege 14', 'exit', 'ip ssh server', 'banner login Router-R1', 'banner exec "Connect Router R1"',
             'do commit', 'do confirm', 'end', 'set date 11:25:30 11 November 2025', 'show date'],
        Debian: ['root', 'toor', 'ip link set ens3 up', 'ip addr add ' + a + '.2/24 dev ens3', 'ip route add default via ' + a + '.1', 'ping ' + a + '.1'] }; },
      alt: 'На Debian адрес можно задать и как в оригинальной лабе: nano /etc/network/interfaces → iface ens3 inet static / address / netmask / gateway, затем ifdown ens3 и ifup ens3.' },

    // ------------------------------------------------------------ 4.1
    { id: '4.1', title: 'Маршрутизация между VLAN на коммутаторе (SVI)',
      goal: 'Разделить сеть на две VLAN и обеспечить связь между ними через интерфейсы VLAN коммутатора MES (L3-интерфейсы SVI).',
      gen: function () { var v = distinct(2, V10).sort(function (a, b) { return a - b; }); return { v: v, n: [R(1, 99), R(100, 199)] }; },
      build: function (net) { var s = net.add('MES2300-24', 'SW1', 420, 280);
        [['VPC1', 140, 150, 1], ['VPC2', 140, 410, 2], ['VPC3', 700, 150, 11], ['VPC4', 700, 410, 12]].forEach(function (x) {
          var v = net.add('VPC', x[0], x[1], x[2]); net.connect(v.id, 'eth0', s.id, 'gi1/0/' + x[3]); }); },
      tasks: function (p) { var A = '10.' + p.n[0] + '.' + p.n[0], B = '10.' + p.n[1] + '.' + p.n[1], v = p.v; return [
        { t: 'VLAN ' + v[0] + ' создана', ok: function (n) { return !!dev(n, 'SW1').vlans[v[0]]; } },
        { t: 'VLAN ' + v[1] + ' создана', ok: function (n) { return !!dev(n, 'SW1').vlans[v[1]]; } },
        { t: 'gi1/0/1–2 → access VLAN ' + v[0], ok: function (n) { return acc(n, 'SW1', [1, 2], v[0]); } },
        { t: 'gi1/0/11–12 → access VLAN ' + v[1], ok: function (n) { return acc(n, 'SW1', [11, 12], v[1]); } },
        { t: 'interface vlan ' + v[0] + ': ' + A + '.1/24', ok: function (n) { return dev(n, 'SW1').svi[v[0]] === A + '.1/24'; } },
        { t: 'interface vlan ' + v[1] + ': ' + B + '.1/24', ok: function (n) { return dev(n, 'SW1').svi[v[1]] === B + '.1/24'; } }]
        .concat(vpcs([['VPC1', A + '.2', A + '.1'], ['VPC2', A + '.3', A + '.1'], ['VPC3', B + '.2', B + '.1'], ['VPC4', B + '.3', B + '.1']]))
        .concat([
        { t: 'ping VPC1 → VPC2 (внутри VLAN)', ok: function (n) { return n.reach('VPC1', A + '.3'); } },
        { t: 'ping VPC1 → VPC3 (между VLAN через SW1)', ok: function (n) { return n.reach('VPC1', B + '.2'); } },
        { t: 'ping VPC4 → VPC2 (между VLAN через SW1)', ok: function (n) { return n.reach('VPC4', A + '.3'); } }]); },
      sol: function (p) { var A = '10.' + p.n[0] + '.' + p.n[0], B = '10.' + p.n[1] + '.' + p.n[1], v = p.v; return {
        SW1: ['enable', 'configure', 'vlan ' + v[0] + ',' + v[1], 'exit',
              'interface range gigabitethernet 1/0/1-2', 'switchport mode access', 'switchport access vlan ' + v[0], 'exit',
              'interface range gigabitethernet 1/0/11-12', 'switchport mode access', 'switchport access vlan ' + v[1], 'exit',
              'interface vlan ' + v[0], 'ip address ' + A + '.1 255.255.255.0', 'exit', 'interface vlan ' + v[1], 'ip address ' + B + '.1 255.255.255.0', 'end', 'write'],
        VPC1: ['ip ' + A + '.2/24 ' + A + '.1'], VPC2: ['ip ' + A + '.3/24 ' + A + '.1'], VPC3: ['ip ' + B + '.2/24 ' + B + '.1'], VPC4: ['ip ' + B + '.3/24 ' + B + '.1'] }; } },

    // ------------------------------------------------------------ 4.2
    { id: '4.2', title: 'Маршрутизация между VLAN: Router-on-a-Stick',
      goal: 'Коммутатор MES разделяет ПК по VLAN, trunk передаёт обе VLAN на ESR, ESR маршрутизирует через саб-интерфейсы.',
      gen: function () { var v = distinct(2, V10).sort(function (a, b) { return a - b; }); return { v: v, a: R(1, 254), b: R(1, 254) }; },
      build: function (net) { var s = net.add('MES2300-24', 'SW1', 420, 330), r = net.add('vESR', 'R1', 420, 110);
        net.connect(s.id, 'gi1/0/6', r.id, 'gi1/0/1');
        [['VPC1', 140, 230, 1], ['VPC2', 140, 470, 2], ['VPC3', 700, 230, 11], ['VPC4', 700, 470, 12]].forEach(function (x) {
          var v = net.add('VPC', x[0], x[1], x[2]); net.connect(v.id, 'eth0', s.id, 'gi1/0/' + x[3]); }); },
      tasks: function (p) { var A = '192.168.' + p.a, B = '172.16.' + p.b, v = p.v; return [
        { t: 'SW1: gi1/0/1–2 → access VLAN ' + v[0], ok: function (n) { return acc(n, 'SW1', [1, 2], v[0]); } },
        { t: 'SW1: gi1/0/11–12 → access VLAN ' + v[1], ok: function (n) { return acc(n, 'SW1', [11, 12], v[1]); } },
        { t: 'SW1 gi1/0/6 → trunk, разрешены VLAN ' + v[0] + ' и ' + v[1], ok: function (n) { var q = port(n, 'SW1', 6); return q.mode === 'trunk' && q.allowed.indexOf(v[0]) >= 0 && q.allowed.indexOf(v[1]) >= 0; } },
        { t: 'R1: gi1/0/1.' + v[0] + ' = ' + A + '.1/24, экран отключён (после commit + confirm)', ok: function (n) { var x = dev(n, 'R1').run.ifs['gi1/0/1.' + v[0]]; return !!x && x.ip === A + '.1/24' && !x.fw; } },
        { t: 'R1: gi1/0/1.' + v[1] + ' = ' + B + '.1/24, экран отключён (после commit + confirm)', ok: function (n) { var y = dev(n, 'R1').run.ifs['gi1/0/1.' + v[1]]; return !!y && y.ip === B + '.1/24' && !y.fw; } }]
        .concat(vpcs([['VPC1', A + '.2', A + '.1'], ['VPC2', A + '.3', A + '.1'], ['VPC3', B + '.2', B + '.1'], ['VPC4', B + '.3', B + '.1']]))
        .concat([
        { t: 'ping VPC1 → VPC3 через R1', ok: function (n) { return n.reach('VPC1', B + '.2'); } },
        { t: 'ping VPC2 → VPC4 через R1', ok: function (n) { return n.reach('VPC2', B + '.3'); } }]); },
      sol: function (p) { var A = '192.168.' + p.a, B = '172.16.' + p.b, v = p.v; return {
        SW1: ['enable', 'configure', 'vlan ' + v[0] + ',' + v[1], 'exit',
              'interface range gigabitethernet 1/0/1-2', 'switchport mode access', 'switchport access vlan ' + v[0], 'exit',
              'interface range gigabitethernet 1/0/11-12', 'switchport mode access', 'switchport access vlan ' + v[1], 'exit',
              'interface gigabitethernet 1/0/6', 'switchport mode trunk', 'switchport trunk allowed vlan add ' + v[0] + ',' + v[1], 'end', 'write'],
        R1: ['configure', 'interface gigabitethernet 1/0/1.' + v[0], 'ip firewall disable', 'ip address ' + A + '.1/24', 'exit',
             'interface gigabitethernet 1/0/1.' + v[1], 'ip firewall disable', 'ip address ' + B + '.1/24', 'exit', 'do commit', 'do confirm', 'end'],
        VPC1: ['ip ' + A + '.2/24 ' + A + '.1'], VPC2: ['ip ' + A + '.3/24 ' + A + '.1'], VPC3: ['ip ' + B + '.2/24 ' + B + '.1'], VPC4: ['ip ' + B + '.3/24 ' + B + '.1'] }; } },

    // ------------------------------------------------------------ поиск неисправности
    { id: 'T.1', title: 'Поиск неисправности: два коммутатора и Router-on-a-Stick',
      goal: 'Сеть уже настроена, но VPC1 не может достучаться до VPC4. Найдите и исправьте ошибку. Смотрите путь пакета пошагово: где он отбрасывается и почему.',
      gen: function () { var v = distinct(2, V10).sort(function (a, b) { return a - b; });
        return { v: v, a: R(1, 254), b: R(1, 254), fault: R(0, 5) }; },
      build: function (net, p) {
        var s1 = net.add('MES2300-24', 'SW1', 300, 330), s2 = net.add('MES2300-24', 'SW2', 620, 330), r = net.add('vESR', 'R1', 300, 110);
        net.connect(s1.id, 'gi1/0/24', s2.id, 'gi1/0/24'); net.connect(s1.id, 'gi1/0/6', r.id, 'gi1/0/1');
        [['VPC1', s1, 120, 480, 1], ['VPC2', s1, 300, 520, 11], ['VPC3', s2, 620, 520, 1], ['VPC4', s2, 820, 480, 11]].forEach(function (x) {
          var d = net.add('VPC', x[0], x[2], x[3]); net.connect(d.id, 'eth0', x[1].id, 'gi1/0/' + x[4]); });
        var A = '192.168.' + p.a, B = '172.16.' + p.b, v = p.v, f = p.fault;
        var sw = function (acc2, trunks, extra) { return ['enable', 'configure', 'vlan ' + v[0] + ',' + v[1], 'exit',
          'interface gigabitethernet 1/0/1', 'switchport mode access', 'switchport access vlan ' + acc2[0], 'exit',
          'interface gigabitethernet 1/0/11', 'switchport mode access', 'switchport access vlan ' + acc2[1], 'exit']
          .concat(trunks.reduce(function (o, t) { return o.concat(['interface gigabitethernet 1/0/' + t[0], 'switchport mode trunk', 'switchport trunk allowed vlan add ' + t[1], 'exit']); }, []))
          .concat(extra || []).concat(['end']); };
        var both = v[0] + ',' + v[1];
        apply(net, {
          SW1: sw([v[0], v[1]], [[24, both], [6, both]]),
          SW2: sw([v[0], f === 0 ? v[0] : v[1]], [[24, f === 1 ? '' + v[0] : both]]),
          R1: ['configure', 'interface gigabitethernet 1/0/1.' + v[0], 'ip address ' + A + '.1/24', 'ip firewall disable', 'exit',
               'interface gigabitethernet 1/0/1.' + (f === 2 ? v[1] + 1 : v[1]), 'ip address ' + B + '.1/24'].concat(f === 3 ? [] : ['ip firewall disable'])
               .concat(['exit', 'do commit', 'do confirm', 'end']),
          VPC1: ['ip ' + A + '.2/24 ' + A + '.1'], VPC2: ['ip ' + B + '.2/24 ' + B + '.1'], VPC3: ['ip ' + A + '.3/24 ' + A + '.1'],
          VPC4: ['ip ' + B + '.3/24 ' + (f === 4 ? B + '.254' : B + '.1')] });
        if (f === 5) apply(net, { SW1: ['configure', 'interface gigabitethernet 1/0/24', 'shutdown', 'end'] });
        p.A = A; p.B = B;
      },
      tasks: function (p) { var B = '172.16.' + p.b, A = '192.168.' + p.a; return [
        { t: 'VPC1 (' + A + '.2) успешно пингует VPC4 (' + B + '.3)', ok: function (n) { return n.reach('VPC1', B + '.3'); } },
        { t: 'VPC3 → VPC2 тоже работает', ok: function (n) { return n.reach('VPC3', B + '.2'); } },
        { t: 'VPC1 → VPC3 тоже работает', ok: function (n) { return n.reach('VPC1', A + '.3'); } }]; },
      sol: function (p) { var v = p.v, B = '172.16.' + p.b;
        var fix = [
          { SW2: ['configure', 'interface gigabitethernet 1/0/11', 'switchport access vlan ' + v[1], 'end'] },
          { SW2: ['configure', 'interface gigabitethernet 1/0/24', 'switchport trunk allowed vlan add ' + v[1], 'end'] },
          { R1: ['configure', 'no interface gigabitethernet 1/0/1.' + (v[1] + 1), 'interface gigabitethernet 1/0/1.' + v[1], 'ip address ' + B + '.1/24', 'ip firewall disable', 'exit', 'do commit', 'do confirm', 'end'] },
          { R1: ['configure', 'interface gigabitethernet 1/0/1.' + v[1], 'ip firewall disable', 'exit', 'do commit', 'do confirm', 'end'] },
          { VPC4: ['ip ' + B + '.3/24 ' + B + '.1'] },
          { SW1: ['configure', 'interface gigabitethernet 1/0/24', 'no shutdown', 'end'] }][p.fault];
        return fix; },
      hint: function (p) { return ['Проверьте show vlan на SW2 — в какой VLAN порт VPC4?', 'Посмотрите show interfaces switchport gi1/0/24 на обоих коммутаторах — какие VLAN разрешены на trunk?',
        'На R1: show ip interfaces — совпадает ли номер саб-интерфейса с VLAN?', 'R1 получает пакет, но молчит — что с межсетевым экраном на саб-интерфейсе?',
        'show на VPC4 — правильный ли шлюз?', 'show interfaces status на SW1 — все ли порты включены?'][p.fault]; } }
  ];

  // случайные задания из движка дек (TASKS base / vlan) — один коммутатор
  function randomTask(kind) {
    var pool = EL.E.TASKS[kind], k = R(0, pool.length - 1), T = pool[k], P = T.gen();
    return { T: T, P: P, k: k };
  }
  EL.labs = { LABS: LABS, apply: apply, powerOff: powerOff, randomTask: randomTask, byId: function (id) { return LABS.filter(function (l) { return l.id === id; })[0]; } };
})(typeof window !== 'undefined' ? window : global);
