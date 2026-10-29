/* «Найди неисправность» на оборудовании Huawei USG, WLAN (AC + Fit AP) и OLT (спецификации sources/huawei/spec/usg.md, wlan.md, olt.md).
   Схема уже настроена, в ней одна ошибка (fault) из типичных: интерфейс вне зоны, правило без action, нет nat-policy; AP не допущена,
   нет capwap source interface, AP вне VLAN управления; плата не подтверждена, C-VLAN service-port не совпадает с gem mapping, нет native-vlan.
   Студент ищет её командами display и ping и исправляет. Решение (sol) — исправление ровно этой ошибки. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, L = EL.labs;
  function esr(lines) { return ['configure'].concat(lines, ['end', 'commit', 'confirm']); }
  function hw(lines) { return ['system-view'].concat(lines, ['return']); }
  function vpc(ip, gw) { return ['ip ' + ip + '/24' + (gw ? ' ' + gw : '')]; }

  var H6 = {
    id: 'T.H6', title: 'Поиск неисправности: межсетевой экран Huawei USG6510E',
    goal: 'PC1 в зоне trust выходит в Интернет к WEB через FW (Easy IP в адрес GE0/0/2). Связи нет. Найдите и исправьте одну ошибку. ' +
      'Помните: интерфейс вне зоны не передаёт трафик, между зонами по умолчанию deny, правило без action не действует.',
    gen: function () { return { a: R(1, 200), fault: R(0, 4) }; },
    build: function (net, p) {
      var f = net.add('USG6510E', 'FW', 420, 220), o = net.add('vESR', 'ISP', 680, 220), a = net.add('VPC', 'PC1', 160, 220), w = net.add('VPC', 'WEB', 680, 420);
      net.connect(f.id, 'GE0/0/1', a.id, 'eth0'); net.connect(f.id, 'GE0/0/2', o.id, 'gi1/0/1'); net.connect(w.id, 'eth0', o.id, 'gi1/0/2');
      var A = '192.168.' + p.a, k = p.fault;
      L.apply(net, {
        FW: hw(['sysname FW', 'interface GigabitEthernet0/0/1', 'ip address ' + A + '.1 24', 'quit', 'interface GigabitEthernet0/0/2', 'ip address 203.0.113.2 24', 'quit']
          .concat(k === 0 ? [] : ['firewall zone trust', 'add interface GigabitEthernet0/0/1', 'quit'], ['firewall zone untrust', 'add interface GigabitEthernet0/0/2', 'quit'],
            k === 4 ? [] : ['ip route-static 0.0.0.0 0.0.0.0 203.0.113.1'],
            ['security-policy', 'rule name lan_out', 'source-zone trust', 'destination-zone ' + (k === 1 ? 'dmz' : 'untrust'), 'source-address ' + A + '.0 24'], k === 3 ? [] : ['action permit'], ['quit', 'quit'],
            k === 2 ? [] : ['nat-policy', 'rule name lan_nat', 'source-zone trust', 'destination-zone untrust', 'source-address ' + A + '.0 24', 'action source-nat easy-ip', 'quit', 'quit'])),
        ISP: esr(['hostname ISP', 'interface gi1/0/1', 'ip address 203.0.113.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 198.51.100.1/24', 'ip firewall disable', 'exit']),
        PC1: vpc(A + '.10', A + '.1'), WEB: vpc('198.51.100.10', '198.51.100.1') });
    },
    tasks: function () { return [{ t: 'PC1 пингует WEB (198.51.100.10)', ok: function (n) { return n.reach('PC1', '198.51.100.10'); } }]; },
    sol: function (p) { var A = '192.168.' + p.a; return [
      { FW: hw(['firewall zone trust', 'add interface GigabitEthernet0/0/1']) },
      { FW: hw(['security-policy', 'rule name lan_out', 'undo destination-zone dmz', 'destination-zone untrust']) },
      { FW: hw(['nat-policy', 'rule name lan_nat', 'source-zone trust', 'destination-zone untrust', 'source-address ' + A + '.0 24', 'action source-nat easy-ip']) },
      { FW: hw(['security-policy', 'rule name lan_out', 'action permit']) },
      { FW: hw(['ip route-static 0.0.0.0 0.0.0.0 203.0.113.1']) }][p.fault]; },
    hint: function (p) { return ['display zone: в какой зоне GigabitEthernet0/0/1?', 'display security-policy rule name lan_out: куда смотрит destination-zone?',
      'display nat-policy rule all: есть ли правило source-nat для LAN? Знает ли ISP сеть ' + '192.168.' + p.a + '.0?', 'display security-policy rule all: какое ACTION у lan_out?',
      'display ip routing-table на FW: есть ли маршрут по умолчанию?'][p.fault]; }
  };

  var H7 = {
    id: 'T.H7', title: 'Поиск неисправности: Huawei AC6005 и Fit AP',
    goal: 'Точка доступа AP1 должна выйти в сеть на контроллере AC (display ap all — State nor). VLAN управления 100: AC — DHCP-сервер для AP (Vlanif100), ' +
      'S1 — коммутатор доступа (порт к AP: trunk, PVID 100). AP не в сети. Найдите и исправьте одну ошибку.',
    gen: function () { return { fault: R(0, 4) }; },
    build: function (net, p) {
      var c = net.add('AC6005', 'AC', 420, 160), s = net.add('S5700', 'S1', 420, 320), a = net.add('AP5030DN', 'AP1', 420, 480);
      net.connect(c.id, 'GE0/0/1', s.id, 'GE0/0/24'); net.connect(a.id, 'LAN', s.id, 'GE0/0/1');
      var k = p.fault, mac = EL.hwlan.apMac(a), bad = mac.slice(0, -1) + (mac.slice(-1) === '0' ? '1' : '0');
      L.apply(net, {
        S1: hw(['sysname S1', 'vlan batch 100', 'interface GigabitEthernet0/0/24', 'port link-type trunk', 'port trunk allow-pass vlan 100', 'quit',
          'interface GigabitEthernet0/0/1', 'port link-type trunk'].concat(k === 2 ? [] : ['port trunk pvid vlan 100'], ['port trunk allow-pass vlan 100'])),
        AC: hw(['sysname AC', 'vlan batch 100', 'interface GigabitEthernet0/0/1', 'port link-type trunk'].concat(k === 4 ? [] : ['port trunk allow-pass vlan 100'], ['quit',
          'dhcp enable', 'interface Vlanif100', 'ip address 10.23.100.1 24'], k === 3 ? [] : ['dhcp select interface'], ['quit'], k === 1 ? [] : ['capwap source interface vlanif100'],
          ['wlan', 'ap auth-mode mac-auth', 'ap-id 0 ap-mac ' + (k === 0 ? bad : mac), 'ap-name area_1', 'quit'])) });
    },
    tasks: function () { return [{ t: 'AP1 на AC в состоянии normal (display ap all)', ok: function (n) { n.hwapSync(); var c = n.byName('AC'); var on = c && c.st.vrp.online || {};
      return Object.keys(on).some(function (m) { return on[m].state === 'normal'; }); } }]; },
    sol: function (p) { return [
      { AC: hw(['wlan', 'ap-confirm all']) },
      { AC: hw(['capwap source interface vlanif100']) },
      { S1: hw(['interface GigabitEthernet0/0/1', 'port trunk pvid vlan 100']) },
      { AC: hw(['interface Vlanif100', 'dhcp select interface']) },
      { AC: hw(['interface GigabitEthernet0/0/1', 'port trunk allow-pass vlan 100']) }][p.fault]; },
    hint: function (p) { return ['display ap unauthorized record на AC: какой MAC у AP1, а какой задан в ap-id 0?', 'display capwap configuration: задан ли Source interface?',
      'display port vlan на S1: какой PVID у GE0/0/1 (кадры AP — без тега)?', 'display current-configuration interface Vlanif100: выдаёт ли AC адреса (dhcp select)?',
      'display port vlan на AC: разрешена ли VLAN 100 на GE0/0/1?'][p.fault]; }
  };

  var H8 = {
    id: 'T.H8', title: 'Поиск неисправности: OLT Huawei MA5600T',
    goal: 'ПК за ONT (порт ETH1, без тега) должен видеть BRAS через OLT: C-VLAN 35, S-VLAN 2000, uplink 0/19/0. Связи нет. Найдите и исправьте одну ошибку. ' +
      'Цепочка: плата Normal → line-profile (gem mapping … vlan 35) + srv-profile → ont add → native-vlan → vlan 2000 + port vlan → service-port … user-vlan 35.',
    gen: function () { return { fault: R(0, 4) }; },
    build: function (net, p) {
      var o = net.add('MA5600T', 'OLT', 420, 220), t = net.add('EG8145V5', 'ONT1', 160, 220), pc = net.add('VPC', 'PC', 160, 420), s = net.add('S5700', 'S1', 680, 220), b = net.add('VPC', 'BRAS', 680, 420);
      net.connect(o.id, '0/5/0', t.id, 'PON'); net.connect(t.id, 'ETH1', pc.id, 'eth0'); net.connect(o.id, '0/19/0', s.id, 'GE0/0/1'); net.connect(s.id, 'GE0/0/2', b.id, 'eth0');
      var k = p.fault, sn = t.st.hwSn;
      L.apply(net, {
        OLT: ['enable', 'config', 'sysname OLT'].concat(k === 0 ? [] : ['board confirm 0'], ['dba-profile add profile-id 15 type4 max 4096',
          'ont-lineprofile gpon profile-id 10 profile-name ftth_hsi', 'tcont 10 dba-profile-id 15', 'gem add 10 eth tcont 10', 'mapping-mode vlan', 'gem mapping 10 1 vlan 35', 'commit', 'quit',
          'ont-srvprofile gpon profile-id 10 profile-name HG824x', 'ont-port eth 4 pots 2 catv 1', 'port vlan eth 1 35', 'commit', 'quit',
          'interface gpon 0/5', 'ont add 0 3 sn-auth ' + sn + ' omci ont-lineprofile-id 10 ont-srvprofile-id 10'], k === 2 ? [] : ['ont port native-vlan 0 3 eth 1 vlan 35'], ['quit',
          'vlan 2000 smart'], k === 3 ? [] : ['port vlan 2000 0/19 0'], ['service-port 1 vlan 2000 gpon 0/5/0 ont 3 gemport 10 multi-service user-vlan ' + (k === 1 ? 36 : 35), 'quit']),
        S1: hw(['sysname S1', 'vlan batch 2000', 'interface GigabitEthernet0/0/1', 'port link-type trunk', 'port trunk allow-pass vlan 2000', 'interface GigabitEthernet0/0/2', 'port link-type access', 'port default vlan 2000']),
        PC: ['ip 10.35.0.10/24'], BRAS: ['ip 10.35.0.1/24'] });
      if (k === 4) { var c = o.st.hwo.c; c.onts['0/5/0/3'].on = false; }   // ONT деактивирована (Control flag deactive)
    },
    tasks: function () { return [{ t: 'ПК за ONT пингует BRAS (10.35.0.1)', ok: function (n) { return n.reach('PC', '10.35.0.1'); } }]; },
    sol: function (p) { var fix = [['board confirm 0'], ['undo service-port 1', 'service-port 1 vlan 2000 gpon 0/5/0 ont 3 gemport 10 multi-service user-vlan 35'],
      ['interface gpon 0/5', 'ont port native-vlan 0 3 eth 1 vlan 35', 'quit'], ['port vlan 2000 0/19 0'], ['interface gpon 0/5', 'ont activate 0 3', 'quit']][p.fault];
      return { OLT: ['enable', 'config'].concat(fix, ['quit']) }; },
    hint: function (p) { return ['display board 0: в каком состоянии плата 5 (Auto_find → board confirm)?', 'display ont-lineprofile gpon profile-id 10 и display service-port all: совпадает ли user-vlan с VLAN в gem mapping?',
      'ПК шлёт кадры без тега: задан ли ont port native-vlan для ETH1?', 'display vlan 2000: есть ли в VLAN uplink-порт 0/19/0?', 'display ont info 0 all: Control flag — active?'][p.fault]; }
  };
  L.LABS.push(H6, H7, H8);
})(typeof window !== 'undefined' ? window : global);
