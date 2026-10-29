/* «Найди неисправность» со стыками D-Link (T.D1–T.D2): старый CLI DES-3200 с Eltex MES и Cisco-подобный DGS-1510 с Cisco 2960.
   Ловушки: у DES-3200 VLAN задаётся списками tagged/untagged портов, а не режимом порта; у DGS-1510 порт по умолчанию hybrid (DTP нет). */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, L = EL.labs;
  function ios(lines) { return ['enable', 'configure terminal'].concat(lines, ['end']); }
  function iosFix(lines) { return ['configure terminal'].concat(lines, ['end']); }
  function dgs(lines) { return ['configure terminal'].concat(lines, ['end']); }
  function mes(lines) { return ['enable', 'configure'].concat(lines, ['end']); }
  function mesFix(lines) { return ['configure'].concat(lines, ['end']); }
  function vpc(ip) { return ['ip ' + ip + '/24']; }

  var D1 = {
    id: 'T.D1', title: 'Поиск неисправности: D-Link DES-3200 (старый CLI) и Eltex MES — транк',
    goal: 'PC1 (порт 1 DES-3200) и PC2 (за MES) в одной VLAN, связь через порт 25 DES-3200 (tagged). Связи нет. Найдите и исправьте одну ошибку. ' +
      'Помните: в старом CLI D-Link порты включаются в VLAN командой config vlan ИМЯ add tagged|untagged СПИСОК.',
    gen: function () { return { v: R(10, 99), a: R(1, 200), fault: R(0, 3) }; },
    build: function (net, p) {
      var d = net.add('DES-3200-28', 'SW1', 300, 220), m = net.add('MES2300-24', 'SW2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(d.id, '25', m.id, 'gi1/0/24'); net.connect(a.id, 'eth0', d.id, '1'); net.connect(b.id, 'eth0', m.id, 'gi1/0/1');
      var v = p.v, f = p.fault, A = '192.168.' + p.a;
      L.apply(net, {
        SW1: ['create vlan v' + v + ' tag ' + (f === 3 ? v + 1 : v), 'config vlan default delete 1-24'].concat(f === 1 ? [] : ['config vlan v' + v + ' add untagged 1-24'], f === 0 ? [] : ['config vlan v' + v + ' add tagged 25-26']),
        SW2: mes(['hostname SW2', 'vlan database', 'vlan ' + v, 'exit', 'interface gi1/0/1', 'switchport access vlan ' + v, 'exit', 'interface gi1/0/24', 'switchport mode trunk'].concat(f === 2 ? [] : ['switchport trunk allowed vlan add ' + v], ['exit'])),
        PC1: vpc(A + '.10'), PC2: vpc(A + '.20') });
    },
    tasks: function (p) { var A = '192.168.' + p.a; return [{ t: 'PC1 (' + A + '.10) пингует PC2 (' + A + '.20)', ok: function (n) { return n.reach('PC1', A + '.20'); } }]; },
    sol: function (p) { var v = p.v; return [
      { SW1: ['config vlan v' + v + ' add tagged 25-26'] },
      { SW1: ['config vlan v' + v + ' add untagged 1-24'] },
      { SW2: mesFix(['interface gi1/0/24', 'switchport trunk allowed vlan add ' + v, 'exit']) },
      { SW1: ['delete vlan v' + v, 'create vlan v' + v + ' tag ' + v, 'config vlan v' + v + ' add untagged 1-24', 'config vlan v' + v + ' add tagged 25-26'] }][p.fault]; },
    hint: function (p) { return ['show vlan на SW1 — в списке Tagged Ports VLAN ' + p.v + ' есть порт 25?', 'show vlan на SW1 — где порт 1 (Untagged)?', 'show interfaces switchport gi1/0/24 на SW2',
      'show vlan на SW1 — какой VID у VLAN v' + p.v + '?'][p.fault]; }
  };

  var D2 = {
    id: 'T.D2', title: 'Поиск неисправности: D-Link DGS-1510 (Cisco-подобный CLI) и Cisco 2960',
    goal: 'PC1 (за DGS-1510) и PC2 (за Cisco 2960) в одной VLAN, связь через транк eth1/0/25 — Gi0/1. Связи нет. Найдите и исправьте одну ошибку. ' +
      'Помните: порт D-Link по умолчанию в режиме hybrid, DTP у D-Link нет.',
    gen: function () { return { v: R(10, 99), a: R(1, 200), fault: R(0, 2) }; },
    build: function (net, p) {
      var d = net.add('DGS-1510-28X', 'SW1', 300, 220), c = net.add('2960-24TT', 'S2', 640, 220), a = net.add('VPC', 'PC1', 300, 420), b = net.add('VPC', 'PC2', 640, 420);
      net.connect(d.id, 'eth1/0/25', c.id, 'gi0/1'); net.connect(a.id, 'eth0', d.id, 'eth1/0/1'); net.connect(b.id, 'eth0', c.id, 'fa0/1');
      var v = p.v, f = p.fault, A = '192.168.' + p.a;
      L.apply(net, {
        SW1: dgs(['snmp-server name SW1', 'vlan ' + v, 'exit', 'interface eth1/0/1', 'switchport mode access', 'switchport access vlan ' + (f === 1 ? 1 : v), 'interface eth1/0/25'].concat(f === 0 ? [] : ['switchport mode trunk'],
          f === 2 ? ['switchport trunk allowed vlan remove ' + v] : [])),
        S2: ios(['hostname S2', 'vlan ' + v, 'exit', 'interface fa0/1', 'switchport mode access', 'switchport access vlan ' + v, 'interface gi0/1', 'switchport mode trunk']),
        PC1: vpc(A + '.10'), PC2: vpc(A + '.20') });
    },
    tasks: function (p) { var A = '192.168.' + p.a; return [{ t: 'PC1 (' + A + '.10) пингует PC2 (' + A + '.20)', ok: function (n) { return n.reach('PC1', A + '.20'); } }]; },
    sol: function (p) { var v = p.v; return [
      { SW1: dgs(['interface eth1/0/25', 'switchport mode trunk']) },
      { SW1: dgs(['interface eth1/0/1', 'switchport access vlan ' + v]) },
      { SW1: dgs(['interface eth1/0/25', 'switchport trunk allowed vlan add ' + v]) }][p.fault]; },
    hint: function (p) { return ['show vlan на SW1 — eth1/0/25 в VLAN ' + p.v + '? Режим порта по умолчанию — hybrid', 'show vlan на SW1 — в какой VLAN eth1/0/1?', 'show running-config на SW1 — allowed vlan на eth1/0/25'][p.fault]; }
  };
  void iosFix;
  L.LABS.push(D1, D2);
})(typeof window !== 'undefined' ? window : global);
