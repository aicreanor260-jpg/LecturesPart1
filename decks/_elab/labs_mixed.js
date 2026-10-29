/* «Найди неисправность» на смешанных схемах Eltex + Huawei (проект sources/huawei/failure-analysis-design.md, H.1–H.5).
   Схема уже настроена, в ней одна ошибка (fault) — чаще всего типичная несостыковка вендоров: trunk Huawei по умолчанию пропускает
   только VLAN 1, Eth-Trunk по умолчанию manual (у MES — LACP), RIP Huawei по умолчанию шлёт v1, тип сети OSPF, адрес VRRP.
   Студент ищет её командами display / show / ping и исправляет. Решение (sol) — исправление ровно этой ошибки. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, L = EL.labs;
  function esr(lines) { return ['configure'].concat(lines, ['end', 'commit', 'confirm']); }
  function mes(lines) { return ['enable', 'configure'].concat(lines, ['end']); }
  function mesFix(lines) { return ['configure'].concat(lines, ['end']); }   // исправление: сессия уже в привилегированном режиме
  function hw(lines) { return ['system-view'].concat(lines, ['return']); }
  function vpc(ip, gw) { return ['ip ' + ip + '/24' + (gw ? ' ' + gw : '')]; }

  var H1 = {
    id: 'T.H1', title: 'Поиск неисправности: trunk между Huawei S5700 и Eltex MES',
    goal: 'PC1 (за S5700) и PC2 (за MES) — в одной VLAN и должны видеть друг друга через trunk. Связи нет. Найдите и исправьте одну ошибку. ' +
      'Помните: у Huawei trunk по умолчанию пропускает только VLAN 1, порт по умолчанию — hybrid.',
    gen: function () { return { v: R(10, 99), a: R(1, 200), fault: R(0, 4) }; },
    build: function (net, p) {
      var s1 = net.add('S5700', 'S1', 300, 220), s2 = net.add('MES2300-24', 'SW2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(s1.id, 'GE0/0/24', s2.id, 'gi1/0/24'); net.connect(a.id, 'eth0', s1.id, 'GE0/0/1'); net.connect(b.id, 'eth0', s2.id, 'gi1/0/1');
      var v = p.v, f = p.fault, A = '192.168.' + p.a;
      var trunk = f === 1 ? [] : ['port link-type trunk'].concat(f === 0 ? [] : ['port trunk allow-pass vlan ' + v], ['undo port trunk allow-pass vlan 1']);
      L.apply(net, {
        S1: hw(['sysname S1'].concat(f === 2 ? [] : ['vlan batch ' + v], ['interface GigabitEthernet0/0/1', 'port link-type access'], f === 4 ? [] : ['port default vlan ' + v],
          ['interface GigabitEthernet0/0/24'], trunk)),
        SW2: mes(['hostname SW2', 'vlan database', 'vlan ' + v, 'exit', 'interface gi1/0/1', 'switchport access vlan ' + v, 'exit', 'interface gi1/0/24', 'switchport mode trunk']
          .concat(f === 3 ? [] : ['switchport trunk allowed vlan add ' + v], ['exit'])),
        PC1: vpc(A + '.10'), PC2: vpc(A + '.20') });
    },
    tasks: function (p) { var A = '192.168.' + p.a; return [{ t: 'PC1 (' + A + '.10) пингует PC2 (' + A + '.20)', ok: function (n) { return n.reach('PC1', A + '.20'); } }]; },
    sol: function (p) { var v = p.v; return [
      { S1: hw(['interface GigabitEthernet0/0/24', 'port trunk allow-pass vlan ' + v]) },
      { S1: hw(['interface GigabitEthernet0/0/24', 'port link-type trunk', 'port trunk allow-pass vlan ' + v, 'undo port trunk allow-pass vlan 1']) },
      { S1: hw(['vlan batch ' + v]) },
      { SW2: mesFix(['interface gi1/0/24', 'switchport trunk allowed vlan add ' + v, 'exit']) },
      { S1: hw(['interface GigabitEthernet0/0/1', 'port default vlan ' + v]) }][p.fault]; },
    hint: function (p) { return ['display port vlan на S1: какие VLAN разрешены на GE0/0/24?', 'display port vlan на S1: какой тип у GE0/0/24 (hybrid по умолчанию)?',
      'display vlan на S1: есть ли VLAN ' + p.v + '?', 'show interfaces switchport gi1/0/24 на SW2', 'display port vlan: PVID порта GE0/0/1 на S1'][p.fault]; }
  };

  var H2 = {
    id: 'T.H2', title: 'Поиск неисправности: OSPF между Huawei AR2220 и Eltex ESR',
    goal: 'R1 (Huawei) и R2 (ESR) обмениваются маршрутами по OSPF, область 0. PC1 не видит PC2. Найдите и исправьте одну ошибку ' +
      '(таймеры hello/dead, область, network с wildcard, тип сети должны совпадать на обоих концах).',
    gen: function () { return { a: R(1, 99), b: R(100, 199), fault: R(0, 4) }; },
    build: function (net, p) {
      var r1 = net.add('AR2220', 'R1', 300, 220), r2 = net.add('vESR', 'R2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(r1.id, 'GE0/0/0', r2.id, 'gi1/0/1'); net.connect(a.id, 'eth0', r1.id, 'GE0/0/1'); net.connect(b.id, 'eth0', r2.id, 'gi1/0/2');
      var f = p.fault, A = '192.168.' + p.a, B = '192.168.' + p.b, ar = f === 1 ? '1' : '0';
      L.apply(net, {
        R1: hw(['sysname R1', 'interface GigabitEthernet0/0/0', 'ip address 10.0.12.1 30'].concat(f === 0 ? ['ospf timer hello 5'] : [], f === 3 ? ['ospf network-type p2p'] : [],
          ['interface GigabitEthernet0/0/1', 'ip address ' + A + '.1 24', 'quit', 'ospf 1 router-id 1.1.1.1', 'area ' + ar, 'network ' + (f === 2 ? '10.0.21.0' : '10.0.12.0') + ' 0.0.0.3',
           'network ' + A + '.0 0.0.0.255'])),
        R2: esr(['hostname R2', 'router ospf 1', 'router-id 2.2.2.2', 'area 0.0.0.0', 'enable', 'exit', 'enable', 'exit',
          'interface gi1/0/1', 'ip address 10.0.12.2/30', 'ip firewall disable', 'ip ospf instance 1', 'ip ospf area 0.0.0.0', 'ip ospf', 'exit',
          'interface gi1/0/2', 'ip address ' + B + '.1/24', 'ip firewall disable'].concat(f === 4 ? [] : ['ip ospf instance 1', 'ip ospf area 0.0.0.0', 'ip ospf'], ['exit'])),
        PC1: vpc(A + '.10', A + '.1'), PC2: vpc(B + '.10', B + '.1') });
    },
    tasks: function (p) { var A = '192.168.' + p.a, B = '192.168.' + p.b; return [
      { t: 'PC1 (' + A + '.10) пингует PC2 (' + B + '.10)', ok: function (n) { return n.reach('PC1', B + '.10'); } },
      { t: 'R1 знает сеть ' + B + '.0/24 по OSPF', ok: function (n) { var d = n.byName('R1'); return !!d && n.routes(d.id).some(function (r) { return r.p === 'O' && r.net === B + '.0/24' && !r.dead; }); } }]; },
    sol: function (p) { var A = '192.168.' + p.a; return [
      { R1: hw(['interface GigabitEthernet0/0/0', 'undo ospf timer hello']) },
      { R1: hw(['ospf 1', 'undo area 1', 'area 0', 'network 10.0.12.0 0.0.0.3', 'network ' + A + '.0 0.0.0.255']) },
      { R1: hw(['ospf 1', 'area 0', 'undo network 10.0.21.0 0.0.0.3', 'network 10.0.12.0 0.0.0.3']) },
      { R1: hw(['interface GigabitEthernet0/0/0', 'undo ospf network-type']) },
      { R2: esr(['interface gi1/0/2', 'ip ospf instance 1', 'ip ospf area 0.0.0.0', 'ip ospf', 'exit']) }][p.fault]; },
    hint: function () { return ['display ospf peer brief на R1 и show ip ospf neighbors на R2 — есть ли соседство? Сравните таймеры hello/dead (display ospf interface)',
      'display current-configuration на R1 — в какой области его сети?', 'display ospf interface на R1 — попал ли GE0/0/0 в OSPF? Проверьте network и wildcard',
      'display ospf interface на R1: тип сети GE0/0/0 и тот же на R2 (show ip ospf interface)', 'display ip routing-table на R1 — какие сети R2 объявляет?'][arguments[0].fault]; }
  };

  var H3 = {
    id: 'T.H3', title: 'Поиск неисправности: агрегат Eth-Trunk (Huawei) и port-channel (Eltex)',
    goal: 'S1 (S5700) и SW2 (MES) соединены двумя кабелями в агрегат, по нему trunk. PC1 не видит PC2. Найдите и исправьте одну ошибку. ' +
      'Помните: у Huawei Eth-Trunk по умолчанию в ручном режиме (manual load-balance), у MES 6.x — channel-group … mode auto (LACP).',
    gen: function () { return { v: R(10, 99), a: R(1, 200), fault: R(0, 2) }; },
    build: function (net, p) {
      var s1 = net.add('S5700', 'S1', 300, 220), s2 = net.add('MES2300-24', 'SW2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(s1.id, 'GE0/0/23', s2.id, 'gi1/0/23'); net.connect(s1.id, 'GE0/0/24', s2.id, 'gi1/0/24');
      net.connect(a.id, 'eth0', s1.id, 'GE0/0/1'); net.connect(b.id, 'eth0', s2.id, 'gi1/0/1');
      var v = p.v, f = p.fault, A = '192.168.' + p.a;
      L.apply(net, {
        S1: hw(['sysname S1', 'vlan batch ' + v, 'interface Eth-Trunk1'].concat(f === 0 ? [] : ['mode lacp'], ['port link-type trunk'], f === 1 ? [] : ['port trunk allow-pass vlan ' + v],
          ['interface GigabitEthernet0/0/23', 'eth-trunk 1', 'interface GigabitEthernet0/0/24', 'eth-trunk 1', 'interface GigabitEthernet0/0/1', 'port link-type access', 'port default vlan ' + v])),
        SW2: mes(['hostname SW2', 'vlan database', 'vlan ' + v, 'exit', 'interface range gi1/0/23-24', 'channel-group 1 mode auto', 'exit', 'interface port-channel 1', 'switchport mode trunk']
          .concat(f === 2 ? [] : ['switchport trunk allowed vlan add ' + v], ['exit', 'interface gi1/0/1', 'switchport access vlan ' + v, 'exit'])),
        PC1: vpc(A + '.10'), PC2: vpc(A + '.20') });
    },
    tasks: function (p) { var A = '192.168.' + p.a; return [{ t: 'PC1 (' + A + '.10) пингует PC2 (' + A + '.20)', ok: function (n) { return n.reach('PC1', A + '.20'); } },
      { t: 'Агрегат собран из двух портов (display eth-trunk 1)', ok: function (n) { var d = n.byName('S1'); return !!d && /Number Of Up Port In Trunk: 2/.test(n.exec(d.id, 'display eth-trunk 1')); } }]; },
    sol: function (p) { var v = p.v; return [
      { S1: hw(['interface GigabitEthernet0/0/23', 'undo eth-trunk', 'interface GigabitEthernet0/0/24', 'undo eth-trunk', 'interface Eth-Trunk1', 'mode lacp',
        'interface GigabitEthernet0/0/23', 'eth-trunk 1', 'interface GigabitEthernet0/0/24', 'eth-trunk 1']) },
      { S1: hw(['interface Eth-Trunk1', 'port trunk allow-pass vlan ' + v]) },
      { SW2: mesFix(['interface port-channel 1', 'switchport trunk allowed vlan add ' + v, 'exit']) }][p.fault]; },
    hint: function (p) { return ['display eth-trunk 1 на S1 — WorkingMode и Operate status; show etherchannel summary на SW2',
      'display port vlan на S1 — какие VLAN разрешены на Eth-Trunk1?', 'show interfaces switchport po1 на SW2'][p.fault]; }
  };

  var H4 = {
    id: 'T.H4', title: 'Поиск неисправности: VRRP на маршрутизаторах Huawei и Eltex',
    goal: 'RA (Huawei AR2220) и RB (Eltex ESR) — общий шлюз 10.0.0.1 по VRRP (группа 1). Шлюз должен оставаться доступным, если выключить любой из них. ' +
      'Проверьте инструментом «Отказы» (Тест) или выключая маршрутизаторы. Найдите и исправьте одну ошибку.',
    gen: function () { return { fault: R(0, 2) }; },
    build: function (net, p) {
      var ra = net.add('AR2220', 'RA', 260, 200), rb = net.add('vESR', 'RB', 660, 200), sw = net.add('MES2300-24', 'SW', 460, 340), pc = net.add('VPC', 'PC', 460, 500);
      net.connect(ra.id, 'GE0/0/1', sw.id, 'gi1/0/1'); net.connect(rb.id, 'gi1/0/1', sw.id, 'gi1/0/2'); net.connect(pc.id, 'eth0', sw.id, 'gi1/0/3');
      var f = p.fault;
      L.apply(net, {
        RA: hw(['sysname RA', 'interface GigabitEthernet0/0/1', 'ip address 10.0.0.2 24', 'vrrp vrid 1 virtual-ip ' + (f === 2 ? '10.0.0.254' : '10.0.0.1'), 'vrrp vrid 1 priority 120']),
        RB: esr(['hostname RB', 'interface gi1/0/1', 'ip address 10.0.0.3/24', 'ip firewall disable', 'vrrp id 1', 'vrrp ip ' + (f === 1 ? '10.0.0.254/24' : '10.0.0.1/24')].concat(f === 0 ? [] : ['vrrp'], ['exit'])),
        SW: mes(['hostname SW']), PC: vpc('10.0.0.10', '10.0.0.1') });
    },
    tasks: function () { return [
      { t: 'Шлюз 10.0.0.1 доступен PC и при отказе RA, и при отказе RB', ok: function (n) {
        return EL.faults.reach(n, { k: 'dev', key: 'RA' }, 'PC', '10.0.0.1') && EL.faults.reach(n, { k: 'dev', key: 'RB' }, 'PC', '10.0.0.1'); } },
      { t: 'PC пингует шлюз 10.0.0.1', ok: function (n) { return n.reach('PC', '10.0.0.1'); } }]; },
    sol: function (p) { return [
      { RB: esr(['interface gi1/0/1', 'vrrp', 'exit']) },
      { RB: esr(['interface gi1/0/1', 'vrrp ip 10.0.0.1/24', 'exit']) },
      { RA: hw(['interface GigabitEthernet0/0/1', 'undo vrrp vrid 1', 'vrrp vrid 1 virtual-ip 10.0.0.1', 'vrrp vrid 1 priority 120']) }][p.fault]; },
    hint: function (p) { return ['show vrrp на RB — запущен ли VRRP на интерфейсе?', 'show vrrp на RB и display vrrp brief на RA — одинаковый ли виртуальный адрес?',
      'display vrrp brief на RA — какой виртуальный адрес у группы 1?'][p.fault]; }
  };

  var H5 = {
    id: 'T.H5', title: 'Поиск неисправности: RIP в цепочке Huawei — Huawei — Eltex',
    goal: 'R1 и R2 — Huawei AR2220, R3 — Eltex ESR; маршруты по RIP. PC1 не видит PC2. Найдите и исправьте одну ошибку. ' +
      'Помните: Huawei по умолчанию шлёт RIP версии 1, а с version 2 принимает только RIPv2; network в RIP Huawei — классовая сеть.',
    gen: function () { return { a: R(1, 99), c: R(100, 199), fault: R(0, 2) }; },
    build: function (net, p) {
      var r1 = net.add('AR2220', 'R1', 200, 220), r2 = net.add('AR2220', 'R2', 460, 220), r3 = net.add('vESR', 'R3', 720, 220), a = net.add('VPC', 'PC1', 200, 420), b = net.add('VPC', 'PC2', 720, 420);
      net.connect(r1.id, 'GE0/0/0', r2.id, 'GE0/0/0'); net.connect(r2.id, 'GE0/0/1', r3.id, 'gi1/0/1'); net.connect(a.id, 'eth0', r1.id, 'GE0/0/1'); net.connect(b.id, 'eth0', r3.id, 'gi1/0/2');
      var f = p.fault, A = '192.168.' + p.a, C = '192.168.' + p.c;
      L.apply(net, {
        R1: hw(['sysname R1', 'interface GigabitEthernet0/0/0', 'ip address 10.0.12.1 30', 'interface GigabitEthernet0/0/1', 'ip address ' + A + '.1 24', 'quit', 'rip 1', 'version 2']
          .concat(f === 1 ? [] : ['network 10.0.0.0'], ['network ' + A + '.0'])),
        R2: hw(['sysname R2', 'interface GigabitEthernet0/0/0', 'ip address 10.0.12.2 30', 'interface GigabitEthernet0/0/1', 'ip address 10.0.23.1 30', 'quit', 'rip 1']
          .concat(f === 0 ? [] : ['version 2'], ['network 10.0.0.0'], f === 2 ? ['silent-interface GigabitEthernet0/0/1'] : [])),
        R3: esr(['hostname R3', 'router rip', 'network 10.0.23.0/30', 'network ' + C + '.0/24', 'enable', 'exit', 'interface gi1/0/1', 'ip address 10.0.23.2/30', 'ip firewall disable', 'exit',
          'interface gi1/0/2', 'ip address ' + C + '.1/24', 'ip firewall disable', 'exit']),
        PC1: vpc(A + '.10', A + '.1'), PC2: vpc(C + '.10', C + '.1') });
    },
    tasks: function (p) { var C = '192.168.' + p.c; return [{ t: 'PC1 пингует PC2 (' + C + '.10)', ok: function (n) { return n.reach('PC1', C + '.10'); } }]; },
    sol: function (p) { var A = '192.168.' + p.a; return [
      { R2: hw(['rip 1', 'version 2']) },
      { R1: hw(['rip 1', 'network 10.0.0.0']) },
      { R2: hw(['rip 1', 'undo silent-interface GigabitEthernet0/0/1']) }][p.fault]; void A; },
    hint: function (p) { return ['display rip 1 route на R1 — приходят ли маршруты от R2? Сравните версии RIP на R1 и R2 (display current-configuration)',
      'display ip routing-table на R2 — знает ли он сеть PC1? Какие сети R1 включил в RIP?', 'display rip 1 route на R2 — есть ли сосед R3? silent-interface?'][p.fault]; }
  };
  L.LABS.push(H1, H2, H3, H4, H5);
})(typeof window !== 'undefined' ? window : global);
