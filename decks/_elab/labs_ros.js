/* «Найди неисправность» со стыками MikroTik (T.M1–T.M3): RouterOS + Cisco / Eltex / Huawei. Ловушки RouterOS: PVID и VLAN-таблица моста
   начинают работать только после vlan-filtering=yes; masquerade — на out-interface провайдера; OSPF v7 — instance → area → interface-template. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, L = EL.labs;
  function ios(lines) { return ['enable', 'configure terminal'].concat(lines, ['end']); }
  function iosFix(lines) { return ['configure terminal'].concat(lines, ['end']); }
  function hw(lines) { return ['system-view'].concat(lines, ['return']); }
  function esr(lines) { return ['configure'].concat(lines, ['end', 'commit', 'confirm']); }
  function vpc(ip, gw) { return ['ip ' + ip + '/24' + (gw ? ' ' + gw : '')]; }

  var M1 = {
    id: 'T.M1', title: 'Поиск неисправности: мост MikroTik с VLAN-фильтрацией и транк Cisco 2960',
    goal: 'PC1 (за MikroTik CRS326) и PC2 (за Cisco 2960) в VLAN. Связь через транк ether1 — Gi0/1. Связи нет. Найдите и исправьте одну ошибку. ' +
      'Помните: PVID и таблица /interface bridge vlan действуют только после vlan-filtering=yes; у Cisco порт по умолчанию dynamic auto.',
    gen: function () { return { v: R(10, 99), a: R(1, 200), fault: R(0, 3) }; },
    build: function (net, p) {
      var sw = net.add('CRS326-24G-2S+', 'SW1', 300, 220), c = net.add('2960-24TT', 'S2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(sw.id, 'ether1', c.id, 'gi0/1'); net.connect(a.id, 'eth0', sw.id, 'ether2'); net.connect(b.id, 'eth0', c.id, 'fa0/1');
      var v = p.v, f = p.fault, A = '192.168.' + p.a;
      L.apply(net, {
        SW1: ['/system identity set name=SW1', '/interface bridge add name=bridge1', '/interface bridge port add bridge=bridge1 interface=ether1',
          '/interface bridge port add bridge=bridge1 interface=ether2 pvid=' + (f === 2 ? 1 : v), '/interface bridge vlan add bridge=bridge1 tagged=' + (f === 1 ? 'bridge1' : 'ether1') + ' untagged=ether2 vlan-ids=' + v]
          .concat(f === 0 ? [] : ['/interface bridge set bridge1 vlan-filtering=yes']),
        S2: ios(['hostname S2', 'vlan ' + v, 'exit', 'interface fa0/1', 'switchport mode access', 'switchport access vlan ' + v, 'interface gi0/1'].concat(f === 3 ? [] : ['switchport mode trunk'])),
        PC1: vpc(A + '.10'), PC2: vpc(A + '.20') });
    },
    tasks: function (p) { var A = '192.168.' + p.a; return [{ t: 'PC1 (' + A + '.10) пингует PC2 (' + A + '.20)', ok: function (n) { return n.reach('PC1', A + '.20'); } }]; },
    sol: function (p) { var v = p.v; return [
      { SW1: ['/interface bridge set bridge1 vlan-filtering=yes'] },
      { SW1: ['/interface bridge vlan set 0 tagged=ether1'] },
      { SW1: ['/interface bridge port set [find interface=ether2] pvid=' + v] },
      { S2: iosFix(['interface gi0/1', 'switchport mode trunk']) }][p.fault]; },
    hint: function (p) { return ['/interface bridge print на SW1 — vlan-filtering?', '/interface bridge vlan print — какие порты tagged в VLAN ' + p.v + '?',
      '/interface bridge port print — PVID порта ether2', 'show interfaces trunk на S2 — есть ли транк?'][p.fault]; }
  };

  var M2 = {
    id: 'T.M2', title: 'Поиск неисправности: MikroTik hEX — выход офиса в Интернет (NAT, маршрут, firewall)',
    goal: 'PC1 за маршрутизатором R1 (MikroTik hEX) должен пинговать сервер WEB у провайдера (Eltex ESR). Связи нет. Найдите и исправьте одну ошибку.',
    gen: function () { return { a: R(1, 200), fault: R(0, 3) }; },
    build: function (net, p) {
      var r = net.add('hEX RB750Gr3', 'R1', 300, 220), isp = net.add('vESR', 'ISP', 640, 220), a = net.add('VPC', 'PC1', 300, 420), w = net.add('VPC', 'WEB', 640, 420);
      net.connect(r.id, 'ether1', isp.id, 'gi1/0/1'); net.connect(a.id, 'eth0', r.id, 'ether2'); net.connect(w.id, 'eth0', isp.id, 'gi1/0/2');
      var f = p.fault, A = '192.168.' + p.a;
      L.apply(net, {
        R1: ['/system identity set name=R1', '/ip address add address=' + A + '.1/24 interface=ether2', '/ip address add address=203.0.113.2/24 interface=ether1']
          .concat(f === 2 ? [] : ['/ip route add gateway=203.0.113.1'], f === 0 ? [] : ['/ip firewall nat add chain=srcnat out-interface=' + (f === 1 ? 'ether2' : 'ether1') + ' action=masquerade'],
            f === 3 ? ['/ip firewall filter add chain=forward action=drop src-address=' + A + '.0/24'] : []),
        ISP: esr(['hostname ISP', 'interface gi1/0/1', 'ip address 203.0.113.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 198.51.100.1/24', 'ip firewall disable', 'exit']),
        PC1: vpc(A + '.10', A + '.1'), WEB: vpc('198.51.100.10', '198.51.100.1') });
    },
    tasks: function () { return [{ t: 'PC1 пингует WEB (198.51.100.10)', ok: function (n) { return n.reach('PC1', '198.51.100.10'); } }]; },
    sol: function (p) { return [
      { R1: ['/ip firewall nat add chain=srcnat out-interface=ether1 action=masquerade'] },
      { R1: ['/ip firewall nat set 0 out-interface=ether1'] },
      { R1: ['/ip route add gateway=203.0.113.1'] },
      { R1: ['/ip firewall filter remove 0'] }][p.fault]; },
    hint: function (p) { return ['/ip firewall nat print — есть ли masquerade?', '/ip firewall nat print detail — на каком out-interface masquerade?', '/ip route print — есть ли 0.0.0.0/0?',
      '/ip firewall filter print — не режет ли forward?'][p.fault]; }
  };

  var M3 = {
    id: 'T.M3', title: 'Поиск неисправности: OSPF v7 между MikroTik CHR и Huawei AR2220',
    goal: 'R1 (MikroTik CHR) и R2 (Huawei AR2220) обмениваются маршрутами по OSPF, область 0. PC1 не видит PC2. Найдите и исправьте одну ошибку ' +
      '(в RouterOS v7: /routing ospf instance → area → interface-template; тип сети на концах должен совпадать).',
    gen: function () { return { a: R(1, 99), b: R(100, 199), fault: R(0, 2) }; },
    build: function (net, p) {
      var r1 = net.add('CHR', 'R1', 300, 220), r2 = net.add('AR2220', 'R2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(r1.id, 'ether1', r2.id, 'GE0/0/0'); net.connect(a.id, 'eth0', r1.id, 'ether2'); net.connect(b.id, 'eth0', r2.id, 'GE0/0/1');
      var f = p.fault, A = '192.168.' + p.a, B = '192.168.' + p.b;
      L.apply(net, {
        R1: ['/system identity set name=R1', '/ip address add address=10.0.12.1/30 interface=ether1', '/ip address add address=' + A + '.1/24 interface=ether2',
          '/routing ospf instance add name=v2inst version=2 router-id=1.1.1.1', '/routing ospf area add name=backbone_v2 area-id=' + (f === 1 ? '0.0.0.1' : '0.0.0.0') + ' instance=v2inst',
          '/routing ospf interface-template add networks=' + (f === 0 ? '10.0.21.0/30' : '10.0.12.0/30') + ' area=backbone_v2' + (f === 2 ? ' type=ptp' : ''), '/routing ospf interface-template add networks=' + A + '.0/24 area=backbone_v2'],
        R2: hw(['sysname R2', 'interface GigabitEthernet0/0/0', 'ip address 10.0.12.2 30', 'interface GigabitEthernet0/0/1', 'ip address ' + B + '.1 24', 'quit', 'ospf 1 router-id 2.2.2.2', 'area 0',
          'network 10.0.12.0 0.0.0.3', 'network ' + B + '.0 0.0.0.255']),
        PC1: vpc(A + '.10', A + '.1'), PC2: vpc(B + '.10', B + '.1') });
    },
    tasks: function (p) { var B = '192.168.' + p.b; return [{ t: 'PC1 пингует PC2 (' + B + '.10)', ok: function (n) { return n.reach('PC1', B + '.10'); } }]; },
    sol: function (p) { return [
      { R1: ['/routing ospf interface-template set 0 networks=10.0.12.0/30'] },
      { R1: ['/routing ospf area set backbone_v2 area-id=0.0.0.0'] },
      { R1: ['/routing ospf interface-template set 0 type=broadcast'] }][p.fault]; },
    hint: function (p) { return ['/routing ospf interface-template print — какие сети в OSPF?', '/routing ospf area print — area-id?', '/routing ospf interface-template print — type? display ospf interface на R2'][p.fault]; }
  };
  L.LABS.push(M1, M2, M3);
})(typeof window !== 'undefined' ? window : global);
