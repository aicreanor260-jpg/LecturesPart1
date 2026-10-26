/* Лабораторные 4.3, 5.1, 5.2, 5.3 — маршрутизация на ESR: статика, суммарный и плавающий маршрут, RIP, OSPF.
   Подключаются к EL.labs.LABS перед лабой поиска неисправности. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, PK = EL.pick;

  function dev(n, name) { var d = n.byName(name); return d ? d.st : null; }
  function run(n, name) { return dev(n, name).run; }
  function ifs(list) {                         // [[порт, адрес], …] → команды ESR
    return list.reduce(function (o, x) { return o.concat(['interface gigabitethernet 1/0/' + x[0], 'ip address ' + x[1], 'ip firewall disable', 'exit']); }, []);
  }
  function ipsOk(n, name, list) { var f = run(n, name).ifs;
    return list.every(function (x) { var y = f['gi1/0/' + x[0]]; return y && y.ip === x[1] && !y.fw; }); }
  function vpcOk(n, name, ip, gw) { var s = dev(n, name); return s.ip === ip.split('/')[0] && s.len === +ip.split('/')[1] && s.gw === gw; }
  function committed(n, names) { return names.every(function (x) { var s = dev(n, x); return !s.pending && !s.unconfirmed; }); }
  function hasRoute(n, name, net, nh, ad) { return run(n, name).routes.some(function (r) { return r.net === net && r.nh === nh && (ad === undefined || (r.ad || 1) === ad); }); }
  function bestProto(n, name, net) { var d = n.byName(name), r = n.best(d.id)[net]; return r ? r.p : null; }
  function linkDown(n, a, ap) { return !n.linkUp(n.byName(a).id, 'gi1/0/' + ap); }
  function via(n, src, dst, name) { var d = n.byName(src), r = n.ping(d.id, dst), x = n.byName(name);
    return r.ok && (r.hops || []).some(function (h) { return h.dev === x.id; }); }
  function place(net, items) { var o = {}; items.forEach(function (x) { o[x[0]] = net.add(x[1], x[0], x[2], x[3]); }); return o; }
  function wire(net, o, links) { links.forEach(function (l) { net.connect(o[l[0]].id, l[1], o[l[2]].id, l[3]); }); }
  function vpcCmd(ip, gw) { return ['ip ' + ip + ' ' + gw]; }

  // треугольник R1–R2–R3 из лаб 5.2 и 5.3 (адреса — по таблице 5.2.1)
  var TRI = {
    R1: [[1, '192.168.100.1/30'], [2, '172.16.100.1/30'], [3, '192.168.0.1/23']],
    R2: [[1, '10.10.100.2/30'], [2, '192.168.100.2/30'], [3, '10.10.0.1/23']],
    R3: [[1, '172.16.100.2/30'], [2, '10.10.100.1/30'], [3, '172.16.0.1/23']],
    NAME: { R1: 'Router-left', R2: 'Router-right', R3: 'Router-up' },
    VPC: { VPC1: ['192.168.1.0/23', '192.168.0.1'], VPC2: ['10.10.1.0/23', '10.10.0.1'], VPC3: ['172.16.1.0/23', '172.16.0.1'] },
    LAN: { R1: '192.168.0.0/23', R2: '10.10.0.0/23', R3: '172.16.0.0/23' },
    // варианты разрыва: [маршрутизатор, порт, текст]
    CUT: [['R1', 1, 'R1 — R2'], ['R1', 2, 'R1 — R3'], ['R2', 1, 'R2 — R3']]
  };
  function triBuild(net) {
    var o = place(net, [['R1', 'vESR', 260, 430], ['R2', 'vESR', 740, 430], ['R3', 'vESR', 500, 230],
                        ['VPC1', 'VPC', 90, 540], ['VPC2', 'VPC', 910, 540], ['VPC3', 'VPC', 500, 80]]);
    wire(net, o, [['R1', 'gi1/0/1', 'R2', 'gi1/0/2'], ['R1', 'gi1/0/2', 'R3', 'gi1/0/1'], ['R2', 'gi1/0/1', 'R3', 'gi1/0/2'],
                  ['VPC1', 'eth0', 'R1', 'gi1/0/3'], ['VPC2', 'eth0', 'R2', 'gi1/0/3'], ['VPC3', 'eth0', 'R3', 'gi1/0/3']]);
  }
  function triBaseTasks() { return [
    { t: 'Имена Router-left, Router-right, Router-up и адреса по таблице 5.2.1 (экран отключён)', ok: function (n) {
        return ['R1', 'R2', 'R3'].every(function (r) { return run(n, r).host === TRI.NAME[r] && ipsOk(n, r, TRI[r]); }); } },
    { t: 'VPC1 192.168.1.0/23 (шлюз 192.168.0.1), VPC2 10.10.1.0/23 (10.10.0.1), VPC3 172.16.1.0/23 (172.16.0.1)', ok: function (n) {
        return Object.keys(TRI.VPC).every(function (v) { return vpcOk(n, v, TRI.VPC[v][0], TRI.VPC[v][1]); }); } }]; }
  function triEndTasks(p) { var c = TRI.CUT[p.cut]; return [
    { t: 'Разорвите соединение ' + c[2] + ' (shutdown на ' + c[0] + ' gi1/0/' + c[1] + ' или удалите кабель)', ok: function (n) { return linkDown(n, c[0], c[1]); } },
    { t: 'После разрыва все ПК по-прежнему пингуют друг друга (маршрут перестроился)', ok: function (n) {
        return n.reach('VPC1', '10.10.1.0') && n.reach('VPC1', '172.16.1.0') && n.reach('VPC2', '172.16.1.0'); } },
    { t: 'Всё применено: commit + confirm на трёх маршрутизаторах', ok: function (n) { return committed(n, ['R1', 'R2', 'R3']); } }]; }
  function triSol(p, proto) {
    var o = {};
    ['R1', 'R2', 'R3'].forEach(function (r, i) {
      var c = ['configure', 'hostname ' + TRI.NAME[r]].concat(ifs(TRI[r]));
      if (proto === 'rip') c = c.concat(['router rip', 'network ' + TRI.LAN[r], 'passive-interface gigabitethernet 1/0/3', 'enable', 'exit']);
      else c = c.concat(['router ospf 250', 'router-id ' + (i + 1) + '.' + (i + 1) + '.' + (i + 1) + '.' + (i + 1), 'area 0.0.0.0', 'enable', 'exit', 'enable', 'exit',
                         'interface gigabitethernet 1/0/1-3', 'ip ospf instance 250', 'ip ospf area 0.0.0.0', 'ip ospf', 'exit',
                         'interface gigabitethernet 1/0/3', 'ip ospf passive-interface', 'exit']);
      o[r] = c.concat(['do commit', 'do confirm', 'end', 'show ip route']);
    });
    Object.keys(TRI.VPC).forEach(function (v) { o[v] = vpcCmd(TRI.VPC[v][0], TRI.VPC[v][1]); });
    var cut = TRI.CUT[p.cut];
    o[cut[0]] = o[cut[0]].concat(['configure', 'interface gigabitethernet 1/0/' + cut[1], 'shutdown', 'exit', 'do commit', 'do confirm', 'end', 'show ip route']);
    o.VPC1 = o.VPC1.concat(['ping 10.10.1.0', 'trace 10.10.1.0']);
    return o;
  }

  var LABS = [
    // ------------------------------------------------------------ 4.3
    { id: '4.3', title: 'Статическая маршрутизация',
      goal: 'Два маршрутизатора и шесть ПК. Сначала связать сети маршрутами по умолчанию, затем заменить их маршрутами до конкретных сетей и посмотреть, что будет, если один маршрут удалить.',
      gen: function () { return { a: PK([10, 40, 70, 100]), b: PK([40, 110, 140, 170]) }; },
      build: function (net) {
        var o = place(net, [['R1', 'vESR', 360, 300], ['R2', 'vESR', 640, 300], ['VPC1', 'VPC', 110, 110], ['VPC2', 'VPC', 90, 300], ['VPC3', 'VPC', 110, 500],
                            ['VPC4', 'VPC', 890, 110], ['VPC5', 'VPC', 910, 300], ['VPC6', 'VPC', 890, 500]]);
        wire(net, o, [['R1', 'gi1/0/1', 'R2', 'gi1/0/1'], ['VPC1', 'eth0', 'R1', 'gi1/0/2'], ['VPC2', 'eth0', 'R1', 'gi1/0/3'], ['VPC3', 'eth0', 'R1', 'gi1/0/4'],
                      ['VPC4', 'eth0', 'R2', 'gi1/0/2'], ['VPC5', 'eth0', 'R2', 'gi1/0/3'], ['VPC6', 'eth0', 'R2', 'gi1/0/4']]); },
      nets: function (p) { var L = [0, 1, 2].map(function (i) { return '172.16.' + (p.a + i * 10); }), Rr = [0, 1, 2].map(function (i) { return '10.10.' + (p.b + i * 10); });
        return { L: L, R: Rr, r1: [[1, '192.168.100.1/30']].concat(L.map(function (x, i) { return [i + 2, x + '.1/24']; })),
                 r2: [[1, '192.168.100.2/30']].concat(Rr.map(function (x, i) { return [i + 2, x + '.1/24']; })) }; },
      tasks: function (p) { var N = this.nets(p); return [
        { t: 'Имена: R1 — Router-left, R2 — Router-right', ok: function (n) { return run(n, 'R1').host === 'Router-left' && run(n, 'R2').host === 'Router-right'; } },
        { t: 'R1: gi1/0/1 192.168.100.1/30, gi1/0/2–4 — ' + N.L.map(function (x) { return x + '.1/24'; }).join(', '), ok: function (n) { return ipsOk(n, 'R1', N.r1); } },
        { t: 'R2: gi1/0/1 192.168.100.2/30, gi1/0/2–4 — ' + N.R.map(function (x) { return x + '.1/24'; }).join(', '), ok: function (n) { return ipsOk(n, 'R2', N.r2); } },
        { t: 'VPC1–3: ' + N.L.map(function (x, i) { return x + '.' + (i + 1) * 10; }).join(', ') + '; VPC4–6: ' + N.R.map(function (x, i) { return x + '.' + (i + 1) * 10; }).join(', ') + ' (/24, шлюз .1)',
          ok: function (n) { return N.L.every(function (x, i) { return vpcOk(n, 'VPC' + (i + 1), x + '.' + (i + 1) * 10 + '/24', x + '.1'); }) &&
                                     N.R.every(function (x, i) { return vpcOk(n, 'VPC' + (i + 4), x + '.' + (i + 1) * 10 + '/24', x + '.1'); }); } },
        { t: 'R2: маршрут по умолчанию 0.0.0.0/0 через 192.168.100.1', ok: function (n) { return hasRoute(n, 'R2', '0.0.0.0/0', '192.168.100.1'); } },
        { t: 'R1: маршрут по умолчанию удалён, вместо него — маршруты до ' + N.R[1] + '.0/24 и ' + N.R[2] + '.0/24, а маршрут до ' + N.R[0] + '.0/24 удалён',
          ok: function (n) { return !hasRoute(n, 'R1', '0.0.0.0/0', '192.168.100.2') && hasRoute(n, 'R1', N.R[1] + '.0/24', '192.168.100.2') &&
                                    hasRoute(n, 'R1', N.R[2] + '.0/24', '192.168.100.2') && !hasRoute(n, 'R1', N.R[0] + '.0/24', '192.168.100.2'); } },
        { t: 'Проверка: VPC3 → VPC5 пингуется, VPC3 → VPC4 — нет (у R1 нет маршрута)', ok: function (n) {
            return n.reach('VPC3', N.R[1] + '.20') && !n.reach('VPC3', N.R[0] + '.10'); } },
        { t: 'Всё применено: commit + confirm на R1 и R2', ok: function (n) { return committed(n, ['R1', 'R2']); } }]; },
      sol: function (p) { var N = this.nets(p), o = {
        R1: ['configure', 'hostname Router-left'].concat(ifs(N.r1), ['ip route 0.0.0.0/0 192.168.100.2', 'do commit', 'do confirm', 'do show ip route',
             'no ip route 0.0.0.0/0 192.168.100.2'], N.R.map(function (x) { return 'ip route ' + x + '.0/24 192.168.100.2'; }),
             ['do commit', 'do confirm', 'no ip route ' + N.R[0] + '.0/24 192.168.100.2', 'do commit', 'do confirm', 'end', 'show ip route']),
        R2: ['configure', 'hostname Router-right'].concat(ifs(N.r2), ['ip route 0.0.0.0/0 192.168.100.1', 'do commit', 'do confirm', 'end', 'show ip route']) };
        N.L.forEach(function (x, i) { o['VPC' + (i + 1)] = vpcCmd(x + '.' + (i + 1) * 10 + '/24', x + '.1'); });
        N.R.forEach(function (x, i) { o['VPC' + (i + 4)] = vpcCmd(x + '.' + (i + 1) * 10 + '/24', x + '.1'); });
        o.VPC3 = o.VPC3.concat(['ping ' + N.R[1] + '.20', 'ping ' + N.R[0] + '.10']);
        return o; } },

    // ------------------------------------------------------------ 5.1
    { id: '5.1', title: 'Суммарный и плавающий статические маршруты',
      goal: 'Три маршрутизатора в кольце. Связать сети R1 и R2 одним суммарным маршрутом /23, а через R3 проложить резервный плавающий маршрут с метрикой 10. Разорвать R1 — R2 и убедиться, что трафик пошёл через R3.',
      gen: function () { return { x: R(10, 99) }; },
      build: function (net) {
        var o = place(net, [['R1', 'vESR', 300, 200], ['R2', 'vESR', 700, 200], ['R3', 'vESR', 500, 440],
                            ['VPC1', 'VPC', 90, 110], ['VPC2', 'VPC', 90, 330], ['VPC3', 'VPC', 910, 110], ['VPC4', 'VPC', 910, 330]]);
        wire(net, o, [['R1', 'gi1/0/1', 'R2', 'gi1/0/1'], ['R1', 'gi1/0/4', 'R3', 'gi1/0/2'], ['R2', 'gi1/0/4', 'R3', 'gi1/0/1'],
                      ['VPC1', 'eth0', 'R1', 'gi1/0/2'], ['VPC2', 'eth0', 'R1', 'gi1/0/3'], ['VPC3', 'eth0', 'R2', 'gi1/0/2'], ['VPC4', 'eth0', 'R2', 'gi1/0/3']]); },
      nets: function (p) { var X = '10.' + p.x; return { X: X,
        r1: [[1, '192.168.100.1/30'], [2, X + '.0.1/24'], [3, X + '.1.1/24'], [4, X + '.100.1/30']],
        r2: [[1, '192.168.100.2/30'], [2, X + '.10.1/24'], [3, X + '.11.1/24'], [4, '172.16.200.2/30']],
        r3: [[1, '172.16.200.1/30'], [2, X + '.100.2/30']] }; },
      tasks: function (p) { var N = this.nets(p), X = N.X; return [
        { t: 'Имена Router-left, Router-right, Router-down; адреса R1, R2, R3 по схеме (сеть ' + X + '.x.x)', ok: function (n) {
            return run(n, 'R1').host === 'Router-left' && run(n, 'R2').host === 'Router-right' && run(n, 'R3').host === 'Router-down' &&
                   ipsOk(n, 'R1', N.r1) && ipsOk(n, 'R2', N.r2) && ipsOk(n, 'R3', N.r3); } },
        { t: 'VPC1 ' + X + '.0.10, VPC2 ' + X + '.1.20, VPC3 ' + X + '.10.10, VPC4 ' + X + '.11.20 (/24, шлюз .1)', ok: function (n) {
            return vpcOk(n, 'VPC1', X + '.0.10/24', X + '.0.1') && vpcOk(n, 'VPC2', X + '.1.20/24', X + '.1.1') &&
                   vpcOk(n, 'VPC3', X + '.10.10/24', X + '.10.1') && vpcOk(n, 'VPC4', X + '.11.20/24', X + '.11.1'); } },
        { t: 'Суммарные маршруты: R1 — ' + X + '.10.0/23 через 192.168.100.2, R2 — ' + X + '.0.0/23 через 192.168.100.1', ok: function (n) {
            return hasRoute(n, 'R1', X + '.10.0/23', '192.168.100.2', 1) && hasRoute(n, 'R2', X + '.0.0/23', '192.168.100.1', 1); } },
        { t: 'Плавающие маршруты с метрикой 10 через R3: R1 → ' + X + '.100.2, R2 → 172.16.200.1', ok: function (n) {
            return hasRoute(n, 'R1', X + '.10.0/23', X + '.100.2', 10) && hasRoute(n, 'R2', X + '.0.0/23', '172.16.200.1', 10); } },
        { t: 'R3: маршруты до четырёх сетей ПК', ok: function (n) {
            return hasRoute(n, 'R3', X + '.0.0/24', X + '.100.1') && hasRoute(n, 'R3', X + '.1.0/24', X + '.100.1') &&
                   hasRoute(n, 'R3', X + '.10.0/24', '172.16.200.2') && hasRoute(n, 'R3', X + '.11.0/24', '172.16.200.2'); } },
        { t: 'Разорвите R1 — R2 (shutdown gi1/0/1 на R1 или удалите кабель)', ok: function (n) { return linkDown(n, 'R1', 1); } },
        { t: 'VPC1 → VPC4 пингуется, и путь идёт через R3 (плавающий маршрут вступил в силу)', ok: function (n) { return via(n, 'VPC1', X + '.11.20', 'R3'); } },
        { t: 'Всё применено: commit + confirm', ok: function (n) { return committed(n, ['R1', 'R2', 'R3']); } }]; },
      sol: function (p) { var N = this.nets(p), X = N.X; return {
        R1: ['configure', 'hostname Router-left'].concat(ifs(N.r1), ['ip route ' + X + '.10.0/23 192.168.100.2', 'ip route ' + X + '.10.0/23 ' + X + '.100.2 10',
             'do commit', 'do confirm', 'do show ip route all', 'end']),
        R2: ['configure', 'hostname Router-right'].concat(ifs(N.r2), ['ip route ' + X + '.0.0/23 192.168.100.1', 'ip route ' + X + '.0.0/23 172.16.200.1 10',
             'do commit', 'do confirm', 'end']),
        R3: ['configure', 'hostname Router-down'].concat(ifs(N.r3), ['ip route ' + X + '.0.0/24 ' + X + '.100.1', 'ip route ' + X + '.1.0/24 ' + X + '.100.1',
             'ip route ' + X + '.10.0/24 172.16.200.2', 'ip route ' + X + '.11.0/24 172.16.200.2', 'do commit', 'do confirm', 'end']),
        VPC1: vpcCmd(X + '.0.10/24', X + '.0.1'), VPC2: vpcCmd(X + '.1.20/24', X + '.1.1'),
        VPC3: vpcCmd(X + '.10.10/24', X + '.10.1'), VPC4: vpcCmd(X + '.11.20/24', X + '.11.1'),
        'R1 ': [] }; },
      after: function (p) { return { R1: ['configure', 'interface gigabitethernet 1/0/1', 'shutdown', 'exit', 'do commit', 'do confirm', 'end', 'show ip route all'],
                                     VPC1: ['trace ' + '10.' + p.x + '.11.20'] }; } },

    // ------------------------------------------------------------ 5.2
    { id: '5.2', title: 'Динамическая маршрутизация: RIP',
      goal: 'Три маршрутизатора в треугольнике. Каждый анонсирует по RIP только свою сеть ПК, интерфейсы к ПК пассивные. После разрыва одного из каналов маршруты должны перестроиться сами.',
      gen: function () { return { cut: R(0, 2) }; },
      build: triBuild,
      tasks: function (p) { return triBaseTasks().concat([
        { t: 'RIP на каждом: router rip, network своей сети (/23), enable', ok: function (n) { return ['R1', 'R2', 'R3'].every(function (r) {
            var c = run(n, r).rip; return c && c.on && c.nets.indexOf(TRI.LAN[r]) >= 0; }); } },
        { t: 'gi1/0/3 (к ПК) — passive-interface на всех трёх', ok: function (n) { return ['R1', 'R2', 'R3'].every(function (r) {
            var c = run(n, r).rip; return c && c.passive.indexOf('gi1/0/3') >= 0; }); } },
        { t: 'В таблице R1 есть маршруты R (RIP) до 10.10.0.0/23 и 172.16.0.0/23', ok: function (n) {
            return bestProto(n, 'R1', '10.10.0.0/23') === 'R' && bestProto(n, 'R1', '172.16.0.0/23') === 'R'; } }], triEndTasks(p)); },
      sol: function (p) { return triSol(p, 'rip'); } },

    // ------------------------------------------------------------ 5.3
    { id: '5.3', title: 'Динамическая маршрутизация: OSPF',
      goal: 'Та же схема, что в 5.2, но OSPF: процесс 250, Router ID 1.1.1.1/2.2.2.2/3.3.3.3, область 0.0.0.0, интерфейсы привязаны к процессу, gi1/0/3 пассивный.',
      gen: function () { return { cut: R(0, 2) }; },
      build: triBuild,
      tasks: function (p) { return triBaseTasks().concat([
        { t: 'router ospf 250 с router-id 1.1.1.1 / 2.2.2.2 / 3.3.3.3, область 0.0.0.0 активна, процесс включён', ok: function (n) {
            return ['R1', 'R2', 'R3'].every(function (r, i) { var o = run(n, r).ospf, k = i + 1;
              return o && o.id === 250 && o.on && o.rid === k + '.' + k + '.' + k + '.' + k && o.areas['0.0.0.0'] && o.areas['0.0.0.0'].on; }); } },
        { t: 'gi1/0/1–3: ip ospf instance 250, ip ospf area 0.0.0.0, ip ospf; gi1/0/3 — passive', ok: function (n) {
            return ['R1', 'R2', 'R3'].every(function (r) { var f = run(n, r).ifs;
              return [1, 2, 3].every(function (k) { var o = f['gi1/0/' + k].ospf; return o && o.on && o.inst === 250 && o.area === '0.0.0.0'; }) &&
                     f['gi1/0/3'].ospf.passive; }); } },
        { t: 'В таблице R1 есть маршруты O (OSPF) до 10.10.0.0/23 и 172.16.0.0/23', ok: function (n) {
            return bestProto(n, 'R1', '10.10.0.0/23') === 'O' && bestProto(n, 'R1', '172.16.0.0/23') === 'O'; } }], triEndTasks(p)); },
      sol: function (p) { return triSol(p, 'ospf'); } }
  ];

  // в 5.1 разрыв — отдельный шаг после основной настройки
  LABS[1].sol = (function (base) { return function (p) {
    var o = base.call(this, p), a = this.after(p); delete o['R1 '];
    Object.keys(a).forEach(function (k) { o[k] = (o[k] || []).concat(a[k]); });
    return o; }; })(LABS[1].sol);

  var all = EL.labs.LABS, at = all.map(function (l) { return l.id; }).indexOf('T.1');
  Array.prototype.splice.apply(all, [at < 0 ? all.length : at, 0].concat(LABS));
})(typeof window !== 'undefined' ? window : global);
