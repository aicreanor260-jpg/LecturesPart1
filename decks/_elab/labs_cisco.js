/* «Найди неисправность» со стыками Cisco (C.1–C.5): Cisco + Eltex + Huawei. Типичные ловушки Cisco: порт по умолчанию dynamic auto (DTP),
   а у Eltex/Huawei DTP нет — транк не поднимается; интерфейсы маршрутизатора выключены по умолчанию; router-on-a-stick требует
   switchport mode trunk на коммутаторе; RIP Cisco/Huawei по умолчанию шлёт v1; EtherChannel: PAgP ≠ LACP, «on» = manual у Huawei. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, L = EL.labs;
  function ios(lines) { return ['enable', 'configure terminal'].concat(lines, ['end']); }
  function iosFix(lines) { return ['configure terminal'].concat(lines, ['end']); }   // исправление: сессия уже в privileged EXEC
  function hw(lines) { return ['system-view'].concat(lines, ['return']); }
  function mes(lines) { return ['enable', 'configure'].concat(lines, ['end']); }
  function mesFix(lines) { return ['configure'].concat(lines, ['end']); }
  function esr(lines) { return ['configure'].concat(lines, ['end', 'commit', 'confirm']); }
  function vpc(ip, gw) { return ['ip ' + ip + '/24' + (gw ? ' ' + gw : '')]; }

  var C1 = {
    id: 'T.C1', title: 'Поиск неисправности: транк Cisco 2960 — Eltex MES (DTP)',
    goal: 'PC1 (за Cisco 2960) и PC2 (за MES) в одной VLAN, связь через транк. Связи нет. Найдите и исправьте одну ошибку. ' +
      'Помните: порт Cisco по умолчанию — switchport mode dynamic auto (DTP), а Eltex DTP не поддерживает.',
    gen: function () { return { v: R(10, 99), a: R(1, 200), fault: R(0, 3) }; },
    build: function (net, p) {
      var s1 = net.add('2960-24TT', 'S1', 300, 220), s2 = net.add('MES2300-24', 'SW2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(s1.id, 'gi0/1', s2.id, 'gi1/0/24'); net.connect(a.id, 'eth0', s1.id, 'fa0/1'); net.connect(b.id, 'eth0', s2.id, 'gi1/0/1');
      var v = p.v, f = p.fault, A = '192.168.' + p.a;
      L.apply(net, {
        S1: ios(['hostname S1', 'vlan ' + v, 'exit', 'interface fa0/1', 'switchport mode access'].concat(f === 3 ? [] : ['switchport access vlan ' + v],
          ['interface gi0/1'], f === 0 ? [] : ['switchport mode trunk'], f === 1 ? ['switchport trunk allowed vlan 1'] : [])),
        SW2: mes(['hostname SW2', 'vlan database', 'vlan ' + v, 'exit', 'interface gi1/0/1', 'switchport access vlan ' + v, 'exit', 'interface gi1/0/24', 'switchport mode trunk']
          .concat(f === 2 ? [] : ['switchport trunk allowed vlan add ' + v], ['exit'])),
        PC1: vpc(A + '.10'), PC2: vpc(A + '.20') });
    },
    tasks: function (p) { var A = '192.168.' + p.a; return [{ t: 'PC1 (' + A + '.10) пингует PC2 (' + A + '.20)', ok: function (n) { return n.reach('PC1', A + '.20'); } }]; },
    sol: function (p) { var v = p.v; return [
      { S1: iosFix(['interface gi0/1', 'switchport mode trunk']) },
      { S1: iosFix(['interface gi0/1', 'switchport trunk allowed vlan add ' + v]) },
      { SW2: mesFix(['interface gi1/0/24', 'switchport trunk allowed vlan add ' + v, 'exit']) },
      { S1: iosFix(['interface fa0/1', 'switchport access vlan ' + v]) }][p.fault]; },
    hint: function (p) { return ['show interfaces trunk на S1 — есть ли транк? show interfaces gi0/1 switchport: Administrative Mode', 'show interfaces trunk на S1: Vlans allowed on trunk',
      'show interfaces switchport gi1/0/24 на SW2', 'show vlan brief на S1: в какой VLAN Fa0/1?'][p.fault]; }
  };

  var C2 = {
    id: 'T.C2', title: 'Поиск неисправности: OSPF между Cisco 1941 и Huawei AR2220',
    goal: 'R1 (Cisco) и R2 (Huawei) обмениваются маршрутами по OSPF, область 0. PC1 не видит PC2. Найдите и исправьте одну ошибку ' +
      '(интерфейсы Cisco по умолчанию выключены; таймеры, область, wildcard, тип сети и passive-interface должны быть согласованы).',
    gen: function () { return { a: R(1, 99), b: R(100, 199), fault: R(0, 4) }; },
    build: function (net, p) {
      var r1 = net.add('1941', 'R1', 300, 220), r2 = net.add('AR2220', 'R2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(r1.id, 'gi0/0', r2.id, 'GE0/0/0'); net.connect(a.id, 'eth0', r1.id, 'gi0/1'); net.connect(b.id, 'eth0', r2.id, 'GE0/0/1');
      var f = p.fault, A = '192.168.' + p.a, B = '192.168.' + p.b;
      L.apply(net, {
        R1: ios(['hostname R1', 'interface gi0/0', 'ip address 10.0.12.1 255.255.255.252'].concat(f === 4 ? [] : ['no shutdown'], f === 0 ? ['ip ospf hello-interval 5'] : [],
          f === 3 ? ['ip ospf network point-to-point'] : [], ['interface gi0/1', 'ip address ' + A + '.1 255.255.255.0', 'no shutdown', 'router ospf 1', 'router-id 1.1.1.1',
          'network 10.0.12.0 0.0.0.3 area ' + (f === 1 ? '1' : '0'), 'network ' + A + '.0 0.0.0.255 area ' + (f === 1 ? '1' : '0')], f === 2 ? ['passive-interface gi0/0'] : [])),
        R2: hw(['sysname R2', 'interface GigabitEthernet0/0/0', 'ip address 10.0.12.2 30', 'interface GigabitEthernet0/0/1', 'ip address ' + B + '.1 24', 'quit', 'ospf 1 router-id 2.2.2.2', 'area 0',
          'network 10.0.12.0 0.0.0.3', 'network ' + B + '.0 0.0.0.255']),
        PC1: vpc(A + '.10', A + '.1'), PC2: vpc(B + '.10', B + '.1') });
    },
    tasks: function (p) { var B = '192.168.' + p.b; return [{ t: 'PC1 пингует PC2 (' + B + '.10)', ok: function (n) { return n.reach('PC1', B + '.10'); } },
      { t: 'R1 знает сеть ' + B + '.0/24 по OSPF', ok: function (n) { var d = n.byName('R1'); return !!d && n.routes(d.id).some(function (r) { return r.p === 'O' && r.net === B + '.0/24' && !r.dead; }); } }]; },
    sol: function (p) { var A = '192.168.' + p.a; return [
      { R1: iosFix(['interface gi0/0', 'no ip ospf hello-interval']) },
      { R1: iosFix(['router ospf 1', 'no network 10.0.12.0 0.0.0.3 area 1', 'no network ' + A + '.0 0.0.0.255 area 1', 'network 10.0.12.0 0.0.0.3 area 0', 'network ' + A + '.0 0.0.0.255 area 0']) },
      { R1: iosFix(['router ospf 1', 'no passive-interface gi0/0']) },
      { R1: iosFix(['interface gi0/0', 'no ip ospf network']) },
      { R1: iosFix(['interface gi0/0', 'no shutdown']) }][p.fault]; },
    hint: function (p) { return ['show ip ospf neighbor на R1 — пусто? Сравните таймеры hello/dead (show ip ospf interface) с display ospf interface на R2',
      'show running-config | section router на R1 — какая область?', 'show running-config | section router — нет ли passive-interface на линке к R2?',
      'Тип сети: на R1 ip ospf network на gi0/0, на R2 display ospf interface', 'show ip interface brief на R1 — состояние Gi0/0'][p.fault]; }
  };

  var C3 = {
    id: 'T.C3', title: 'Поиск неисправности: router-on-a-stick (Cisco 2911 + Cisco 2960)',
    goal: 'VLAN 10 и 20 маршрутизирует R1 через подынтерфейсы Gi0/1.10 и Gi0/1.20. PC1 (VLAN 10) не видит PC2 (VLAN 20). Найдите и исправьте одну ошибку.',
    gen: function () { return { fault: R(0, 3) }; },
    build: function (net, p) {
      var r = net.add('2911', 'R1', 460, 160), s = net.add('2960-24TT', 'S1', 460, 320), a = net.add('VPC', 'PC1', 300, 480), b = net.add('VPC', 'PC2', 620, 480);
      net.connect(r.id, 'gi0/1', s.id, 'gi0/1'); net.connect(a.id, 'eth0', s.id, 'fa0/1'); net.connect(b.id, 'eth0', s.id, 'fa0/2');
      var f = p.fault;
      L.apply(net, {
        S1: ios(['hostname S1', 'vlan 10', 'vlan 20', 'exit', 'interface fa0/1', 'switchport mode access', 'switchport access vlan 10', 'interface fa0/2', 'switchport mode access', 'switchport access vlan 20',
          'interface gi0/1'].concat(f === 1 ? [] : ['switchport mode trunk'])),
        R1: ios(['hostname R1', 'interface gi0/1'].concat(f === 3 ? [] : ['no shutdown'], ['interface gi0/1.10', 'encapsulation dot1Q ' + (f === 0 ? '100' : '10'), 'ip address 192.168.10.1 255.255.255.0',
          'interface gi0/1.20', 'encapsulation dot1Q 20', 'ip address 192.168.20.1 255.255.255.0'])),
        PC1: vpc('192.168.10.10', f === 2 ? '192.168.10.254' : '192.168.10.1'), PC2: vpc('192.168.20.10', '192.168.20.1') });
    },
    tasks: function () { return [{ t: 'PC1 (192.168.10.10) пингует PC2 (192.168.20.10)', ok: function (n) { return n.reach('PC1', '192.168.20.10'); } }]; },
    sol: function (p) { return [
      { R1: iosFix(['interface gi0/1.10', 'encapsulation dot1Q 10']) },
      { S1: iosFix(['interface gi0/1', 'switchport mode trunk']) },
      { PC1: vpc('192.168.10.10', '192.168.10.1') },
      { R1: iosFix(['interface gi0/1', 'no shutdown']) }][p.fault]; },
    hint: function (p) { return ['show running-config на R1 — какой VLAN у Gi0/1.10?', 'show interfaces trunk на S1 — маршрутизатор DTP не поддерживает, нужен switchport mode trunk',
      'show ip на PC1 — какой шлюз?', 'show ip interface brief на R1 — Gi0/1 administratively down?'][p.fault]; }
  };

  var C4 = {
    id: 'T.C4', title: 'Поиск неисправности: RIP — Cisco, Huawei и Eltex в одной цепочке',
    goal: 'R1 (Cisco 1941) — R2 (Huawei AR2220) — R3 (Eltex ESR), маршруты по RIP. PC1 не видит PC2. Найдите и исправьте одну ошибку. ' +
      'Помните: Cisco и Huawei по умолчанию шлют RIP версии 1, а с version 2 принимают только RIPv2.',
    gen: function () { return { a: R(1, 99), c: R(100, 199), fault: R(0, 2) }; },
    build: function (net, p) {
      var r1 = net.add('1941', 'R1', 200, 220), r2 = net.add('AR2220', 'R2', 460, 220), r3 = net.add('vESR', 'R3', 720, 220), a = net.add('VPC', 'PC1', 200, 420), b = net.add('VPC', 'PC2', 720, 420);
      net.connect(r1.id, 'gi0/0', r2.id, 'GE0/0/0'); net.connect(r2.id, 'GE0/0/1', r3.id, 'gi1/0/1'); net.connect(a.id, 'eth0', r1.id, 'gi0/1'); net.connect(b.id, 'eth0', r3.id, 'gi1/0/2');
      var f = p.fault, A = '192.168.' + p.a, C = '192.168.' + p.c;
      L.apply(net, {
        R1: ios(['hostname R1', 'interface gi0/0', 'ip address 10.0.12.1 255.255.255.252', 'no shutdown', 'interface gi0/1', 'ip address ' + A + '.1 255.255.255.0', 'no shutdown',
          'router rip', 'version 2'].concat(f === 1 ? [] : ['network 10.0.0.0'], ['network ' + A + '.0', 'no auto-summary'], f === 2 ? ['passive-interface gi0/0'] : [])),
        R2: hw(['sysname R2', 'interface GigabitEthernet0/0/0', 'ip address 10.0.12.2 30', 'interface GigabitEthernet0/0/1', 'ip address 10.0.23.1 30', 'quit', 'rip 1']
          .concat(f === 0 ? [] : ['version 2'], ['network 10.0.0.0'])),
        R3: esr(['hostname R3', 'router rip', 'network 10.0.23.0/30', 'network ' + C + '.0/24', 'enable', 'exit', 'interface gi1/0/1', 'ip address 10.0.23.2/30', 'ip firewall disable', 'exit',
          'interface gi1/0/2', 'ip address ' + C + '.1/24', 'ip firewall disable', 'exit']),
        PC1: vpc(A + '.10', A + '.1'), PC2: vpc(C + '.10', C + '.1') });
    },
    tasks: function (p) { var C = '192.168.' + p.c; return [{ t: 'PC1 пингует PC2 (' + C + '.10)', ok: function (n) { return n.reach('PC1', C + '.10'); } }]; },
    sol: function (p) { return [{ R2: hw(['rip 1', 'version 2']) }, { R1: iosFix(['router rip', 'network 10.0.0.0']) }, { R1: iosFix(['router rip', 'no passive-interface gi0/0']) }][p.fault]; },
    hint: function (p) { return ['show ip protocols на R1 — какие версии RIP принимает? display current-configuration на R2 — version?', 'show running-config | section router rip на R1 — все ли сети в RIP?',
      'show ip protocols / show running-config на R1 — passive-interface?'][p.fault]; }
  };

  var C5 = {
    id: 'T.C5', title: 'Поиск неисправности: EtherChannel Cisco 2960 — Eth-Trunk Huawei S5700',
    goal: 'S1 (Cisco) и S2 (Huawei) соединены двумя кабелями в агрегат по LACP, по нему транк. PC1 не видит PC2. Найдите и исправьте одну ошибку. ' +
      'Помните: PAgP (auto/desirable) — протокол только Cisco; LACP у Cisco — active/passive, у Huawei — mode lacp; «on» у Cisco = manual у Huawei.',
    gen: function () { return { v: R(10, 99), a: R(1, 200), fault: R(0, 2) }; },
    build: function (net, p) {
      var s1 = net.add('2960-24TT', 'S1', 300, 220), s2 = net.add('S5700', 'S2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(s1.id, 'fa0/23', s2.id, 'GE0/0/23'); net.connect(s1.id, 'fa0/24', s2.id, 'GE0/0/24'); net.connect(a.id, 'eth0', s1.id, 'fa0/1'); net.connect(b.id, 'eth0', s2.id, 'GE0/0/1');
      var v = p.v, f = p.fault, A = '192.168.' + p.a;
      L.apply(net, {
        S1: ios(['hostname S1', 'vlan ' + v, 'exit', 'interface fa0/1', 'switchport mode access', 'switchport access vlan ' + v, 'interface range fa0/23 - 24', 'switchport mode trunk',
          'channel-group 1 mode ' + (f === 0 ? 'desirable' : f === 1 ? 'on' : 'active'), 'interface port-channel 1', 'switchport mode trunk']),
        S2: hw(['sysname S2', 'vlan batch ' + v, 'interface Eth-Trunk1', 'mode lacp', 'port link-type trunk'].concat(f === 2 ? [] : ['port trunk allow-pass vlan ' + v],
          ['interface GigabitEthernet0/0/23', 'eth-trunk 1', 'interface GigabitEthernet0/0/24', 'eth-trunk 1', 'interface GigabitEthernet0/0/1', 'port link-type access', 'port default vlan ' + v])),
        PC1: vpc(A + '.10'), PC2: vpc(A + '.20') });
    },
    tasks: function (p) { var A = '192.168.' + p.a; return [{ t: 'PC1 (' + A + '.10) пингует PC2 (' + A + '.20)', ok: function (n) { return n.reach('PC1', A + '.20'); } },
      { t: 'Агрегат собран: Po1 (SU) на S1', ok: function (n) { var d = n.byName('S1'); return !!d && /Po1\(SU\)\s+LACP/.test(n.exec(d.id, 'show etherchannel summary')); } }]; },
    sol: function (p) { var v = p.v; return [
      { S1: iosFix(['interface range fa0/23 - 24', 'no channel-group', 'channel-group 1 mode active']) },
      { S1: iosFix(['interface range fa0/23 - 24', 'no channel-group', 'channel-group 1 mode active']) },
      { S2: hw(['interface Eth-Trunk1', 'port trunk allow-pass vlan ' + v]) }][p.fault]; },
    hint: function (p) { return ['show etherchannel summary на S1 — какой протокол у Po1? display eth-trunk 1 на S2', 'show etherchannel summary: Protocol «-» — это on (без LACP), а у S2 mode lacp',
      'display port vlan на S2 — разрешена ли VLAN ' + p.v + ' на Eth-Trunk1?'][p.fault]; }
  };
  function asa(lines) { return ['enable', '', 'configure terminal'].concat(lines, ['end']); }   // enable: пароль пустой — Enter
  var C6 = {
    id: 'T.C6', title: 'Поиск неисправности: межсетевой экран Cisco ASA 5506 между офисом и провайдером (Eltex ESR)',
    goal: 'Узел IN (inside) должен пинговать веб-сервер WEB у провайдера. Связи нет. Найдите и исправьте одну ошибку. Помните: у ASA трафик с высокого уровня ' +
      'безопасности на низкий разрешён, но ответы ICMP возвращаются только при inspect icmp; без nat (inside,outside) провайдер не знает обратного пути.',
    gen: function () { return { a: R(1, 200), fault: R(0, 3) }; },
    build: function (net, p) {
      var f0 = net.add('ASA 5506', 'FW', 460, 220), i = net.add('VPC', 'IN', 260, 400), isp = net.add('vESR', 'ISP', 680, 220), w = net.add('VPC', 'WEB', 680, 400);
      net.connect(f0.id, 'gi1/2', i.id, 'eth0'); net.connect(f0.id, 'gi1/1', isp.id, 'gi1/0/1'); net.connect(w.id, 'eth0', isp.id, 'gi1/0/2');
      var f = p.fault, A = '192.168.' + p.a;
      L.apply(net, {
        FW: asa(['hostname FW', 'interface gi1/1', 'nameif outside', 'ip address 203.0.113.2 255.255.255.0', 'no shutdown', 'interface gi1/2'].concat(f === 2 ? [] : ['nameif inside'],
          ['ip address ' + A + '.1 255.255.255.0', 'no shutdown', 'exit'], f === 3 ? [] : ['route outside 0 0 203.0.113.1'], ['object network INSIDE', 'subnet ' + A + '.0 255.255.255.0'],
          f === 1 ? [] : ['nat (inside,outside) dynamic interface'], ['exit'], f === 0 ? [] : ['policy-map global_policy', 'class inspection_default', 'inspect icmp', 'exit', 'exit'])),
        ISP: esr(['hostname ISP', 'interface gi1/0/1', 'ip address 203.0.113.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 198.51.100.1/24', 'ip firewall disable', 'exit']),
        IN: vpc(A + '.10', A + '.1'), WEB: vpc('198.51.100.10', '198.51.100.1') });
    },
    tasks: function () { return [{ t: 'IN пингует WEB (198.51.100.10)', ok: function (n) { return n.reach('IN', '198.51.100.10'); } }]; },
    sol: function (p) { var A = '192.168.' + p.a; return [
      { FW: ['configure terminal', 'policy-map global_policy', 'class inspection_default', 'inspect icmp', 'end'] },
      { FW: ['configure terminal', 'object network INSIDE', 'nat (inside,outside) dynamic interface', 'end'] },
      { FW: ['configure terminal', 'interface gi1/2', 'nameif inside', 'end'] },
      { FW: ['configure terminal', 'route outside 0 0 203.0.113.1', 'end'] }][p.fault]; void A; },
    hint: function (p) { return ['Путь пакета: запрос ушёл, ответ ICMP отброшен на outside — show running-config | begin policy-map', 'show nat / show xlate на FW — транслируется ли inside?',
      'show nameif на FW — у Gi1/2 нет имени?', 'show route на FW — есть ли маршрут по умолчанию?'][p.fault]; }
  };
  L.LABS.push(C1, C2, C3, C4, C5, C6);
})(typeof window !== 'undefined' ? window : global);
