/* Лабораторные 7.1 (ACL), 8.1 (RSTP), 8.2 (LACP), 8.3 (VRRP). Коммутаторы — настоящий CLI MES, маршрутизаторы — ESR. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, PK = EL.pick;

  function dev(n, name) { var d = n.byName(name); return d ? d.st : null; }
  function run(n, name) { return dev(n, name).run; }
  function ifs(list) { return list.reduce(function (o, x) { return o.concat(['interface gigabitethernet 1/0/' + x[0], 'ip address ' + x[1], 'ip firewall disable', 'exit']); }, []); }
  function ipsOk(n, name, list) { var f = run(n, name).ifs; return list.every(function (x) { var y = f['gi1/0/' + x[0]]; return y && y.ip === x[1] && !y.fw; }); }
  function committed(n, names) { return names.every(function (x) { var s = dev(n, x); return !s.pending && !s.unconfirmed && (s.commits || 0) > 0; }); }
  function place(net, items) { var o = {}; items.forEach(function (x) { o[x[0]] = net.add(x[1], x[0], x[2], x[3]); }); return o; }
  function wire(net, o, links) { links.forEach(function (l) { net.connect(o[l[0]].id, l[1], o[l[2]].id, l[3]); }); }
  function debOk(n, name, ip, gw) { var s = dev(n, name); return s.up && s.ip + '/' + s.len === ip && s.gw === gw; }
  function debIp(ip, gw) { return ['root', 'toor', 'ip link set ens3 up', 'ip addr add ' + ip + ' dev ens3', 'ip route add default via ' + gw]; }
  function tcp(n, src, ip, port) { var d = n.byName(src); return n.request(d.id, ip, 'tcp', port).ok; }
  function aclRule(L, k) { return L && L.rules[k]; }
  // «одно действие — один пункт»
  function ifT(r, list) { return list.map(function (x) { return { t: r + ' gi1/0/' + x[0] + ': ' + x[1] + ', экран отключён', ok: function (n) { return ipsOk(n, r, [x]); } }; }); }
  function debT(v, ip, gw) { return { t: v + ' (root/toor): ens3 ' + ip + ', шлюз ' + gw, ok: function (n) { return debOk(n, v, ip, gw); } }; }
  function vpcIp(v, ip, gw) { return { t: v + ': ' + ip + '/24' + (gw ? ', шлюз ' + gw : ''), ok: function (n) { var d = dev(n, v); return d.ip === ip && (!gw || d.gw === gw); } }; }


  var LABS = [
    // ------------------------------------------------------------ 7.1
    { id: '7.1', title: 'Списки контроля доступа (ACL) на маршрутизаторе',
      goal: 'R1 соединяет три сети. Список Test1 на gi1/0/1 запрещает Telnet, но разрешает SSH и ICMP; Test2 на gi1/0/2 запрещает Telnet, SSH и ICMP; на gi1/0/3 правил нет. ' +
            'Потом в Test2 разрешить ICMP. В трассе видно, каким правилом отброшен пакет — в том числе ответ, пришедший на интерфейс со списком.',
      gen: function () { return { o: PK([0, 1, 2, 3]) }; },
      build: function (net) {
        var o = place(net, [['R1', 'vESR', 500, 300], ['Debian', 'Debian', 170, 160], ['Debian2', 'Debian', 830, 160], ['Debian3', 'Debian', 500, 560]]);
        wire(net, o, [['Debian', 'ens3', 'R1', 'gi1/0/1'], ['Debian2', 'ens3', 'R1', 'gi1/0/2'], ['Debian3', 'ens3', 'R1', 'gi1/0/3']]); },
      net: function (p) { return [10, 20, 30].map(function (x) { return '192.168.' + (x + p.o); }); },
      tasks: function (p) { var N = this.net(p); return [
        ].concat(ifT('R1', N.map(function (x, i) { return [i + 1, x + '.1/24']; })), [
        debT('Debian', N[0] + '.10/24', N[0] + '.1'), debT('Debian2', N[1] + '.20/24', N[1] + '.1'), debT('Debian3', N[2] + '.30/24', N[2] + '.1'),
        { t: 'R1: ip ssh server', ok: function (n) { return !!run(n, 'R1').ssh; } },
        { t: 'R1: ip telnet server', ok: function (n) { return !!run(n, 'R1').telnet; } },
        { t: 'Test1: rule 10 deny tcp 23, rule 20 permit tcp 22, rule 30 permit icmp (все enable)', ok: function (n) { var L = (run(n, 'R1').acls || {}).Test1;
            var a = aclRule(L, 10), b = aclRule(L, 20), c = aclRule(L, 30);
            return a && a.on && a.act === 'deny' && a.proto === 'tcp' && a.dport && a.dport[0] === 23 && b && b.on && b.act === 'permit' && b.dport && b.dport[0] === 22 &&
                   c && c.on && c.act === 'permit' && c.proto === 'icmp'; } },
        { t: 'Test2: rule 10 deny tcp 23, rule 20 deny tcp 22, rule 30 — сначала deny icmp, в конце permit icmp', ok: function (n) { var L = (run(n, 'R1').acls || {}).Test2;
            var a = aclRule(L, 10), b = aclRule(L, 20), c = aclRule(L, 30);
            return a && a.on && a.act === 'deny' && a.dport && a.dport[0] === 23 && b && b.on && b.act === 'deny' && b.dport && b.dport[0] === 22 &&
                   c && c.on && c.act === 'permit' && c.proto === 'icmp'; } },
        { t: 'service-acl input Test1 на gi1/0/1, Test2 на gi1/0/2, на gi1/0/3 — без списка', ok: function (n) { var f = run(n, 'R1').ifs;
            return f['gi1/0/1'].acl === 'Test1' && f['gi1/0/2'].acl === 'Test2' && !f['gi1/0/3'].acl; } },
        { t: 'Применено: commit + confirm', ok: function (n) { return committed(n, ['R1']); } },
        { t: 'Проверка Debian: telnet ' + N[0] + '.1 — нет, ssh и ping — да', ok: function (n) {
            return !tcp(n, 'Debian', N[0] + '.1', 23) && tcp(n, 'Debian', N[0] + '.1', 22) && n.reach('Debian', N[0] + '.1'); } },
        { t: 'Проверка Debian2: telnet и ssh к ' + N[1] + '.1 — нет; ping Debian → Debian2 после разрешения ICMP — да', ok: function (n) {
            return !tcp(n, 'Debian2', N[1] + '.1', 23) && !tcp(n, 'Debian2', N[1] + '.1', 22) && n.reach('Debian', N[1] + '.20'); } },
        { t: 'Проверка Debian3: telnet к ' + N[2] + '.1 работает — на gi1/0/3 списка нет', ok: function (n) { return tcp(n, 'Debian3', N[2] + '.1', 23); } }]); },
      sol: function (p) { var N = this.net(p); return {
        R1: ['configure', 'hostname R1'].concat(ifs(N.map(function (x, i) { return [i + 1, x + '.1/24']; })), ['ip ssh server', 'ip telnet server',
          'ip access-list extended Test1', 'rule 10', 'action deny', 'match protocol tcp', 'match destination-port port-range 23', 'enable', 'exit',
          'rule 20', 'action permit', 'match protocol tcp', 'match destination-port port-range 22', 'enable', 'exit',
          'rule 30', 'action permit', 'match protocol icmp', 'enable', 'exit', 'exit',
          'ip access-list extended Test2', 'rule 10', 'action deny', 'match protocol tcp', 'match destination-port port-range 23', 'enable', 'exit',
          'rule 20', 'action deny', 'match protocol tcp', 'match destination-port port-range 22', 'enable', 'exit',
          'rule 30', 'action deny', 'match protocol icmp', 'enable', 'exit', 'exit',
          'interface gigabitethernet 1/0/1', 'service-acl input Test1', 'exit', 'interface gigabitethernet 1/0/2', 'service-acl input Test2', 'exit',
          'do commit', 'do confirm', 'ip access-list extended Test2', 'rule 30', 'action permit', 'exit', 'exit', 'do commit', 'do confirm', 'end']),
        Debian: debIp(N[0] + '.10/24', N[0] + '.1').concat(['telnet ' + N[0] + '.1', 'ping ' + N[1] + '.20']),
        Debian2: debIp(N[1] + '.20/24', N[1] + '.1').concat(['telnet ' + N[1] + '.1']),
        Debian3: debIp(N[2] + '.30/24', N[2] + '.1').concat(['telnet ' + N[2] + '.1']) }; } },

    // ------------------------------------------------------------ 8.1
    { id: '8.1', title: 'Протокол связующего дерева (RSTP)',
      goal: 'Кольцо из пяти коммутаторов MES. Без STP кадры зацикливаются; с RSTP один порт уходит в Alternate и блокируется. Смените корень приоритетом и посмотрите, как перестроится дерево (show spanning-tree, путь пакета).',
      gen: function () { return { root: R(2, 5) }; },
      build: function (net) {
        var o = place(net, [['vMES1', 'MES2300-24', 240, 130], ['vMES3', 'MES2300-24', 760, 130], ['vMES2', 'MES2300-24', 240, 400], ['vMES4', 'MES2300-24', 620, 470],
                            ['vMES5', 'MES2300-24', 860, 330], ['VPC1', 'VPC', 80, 260], ['VPC2', 'VPC', 920, 560]]);
        wire(net, o, [['vMES1', 'gi1/0/1', 'vMES3', 'gi1/0/12'], ['vMES1', 'gi1/0/12', 'vMES2', 'gi1/0/1'], ['vMES2', 'gi1/0/12', 'vMES4', 'gi1/0/1'],
                      ['vMES3', 'gi1/0/1', 'vMES5', 'gi1/0/12'], ['vMES4', 'gi1/0/12', 'vMES5', 'gi1/0/1'],
                      ['VPC1', 'eth0', 'vMES1', 'gi1/0/5'], ['VPC2', 'eth0', 'vMES5', 'gi1/0/5']]);
        net.list().forEach(function (d) { if (d.type === 'mes') d.st.stp = { on: false, mode: 'mst', prio: 32768 }; });   // старт: STP выключен — студент включает
      },
      tasks: function (p) { var M = ['vMES1', 'vMES2', 'vMES3', 'vMES4', 'vMES5'], rt = 'vMES' + p.root; return [
        ].concat(M.map(function (m) { return { t: 'Имя ' + m + ' (hostname ' + m + ')', ok: function (n) { return dev(n, m).host === m; } }; }), [
        vpcIp('VPC1', '192.168.1.1'), { t: 'VPC2: 192.168.1.2/24 — сейчас ping не проходит: в кольце петля без STP (смотрите трассу)', ok: function (n) { return dev(n, 'VPC2').ip === '192.168.1.2'; } }],
        M.map(function (m) { return { t: m + ': spanning-tree и spanning-tree mode rstp', ok: function (n) { var s = dev(n, m).stp; return !!s && s.on && s.mode === 'rst'; } }; }), [
        { t: 'Корнем сделайте ' + rt + ': spanning-tree priority 16384', ok: function (n) { var d = n.byName(rt); n.stp();
            return dev(n, rt).stp.prio === 16384 && n._stp.root[d.id] === d.id; } },
        { t: 'В кольце ровно один порт в роли Alternate (заблокирован), ping VPC1 → VPC2 проходит', ok: function (n) { var t = n.stp(), c = 0;
            Object.keys(t).forEach(function (id) { Object.keys(t[id]).forEach(function (k) { if (!t[id][k].fwd) c++; }); });
            return c === 1 && n.reach('VPC1', '192.168.1.2'); } }]); },
      sol: function (p) { var o = {};
        ['vMES1', 'vMES2', 'vMES3', 'vMES4', 'vMES5'].forEach(function (m, i) {
          o[m] = ['enable', 'configure', 'hostname ' + m, 'spanning-tree', 'spanning-tree mode rstp'].concat(i + 1 === p.root ? ['spanning-tree priority 16384'] : [], ['end', 'show spanning-tree']); });
        o.VPC1 = ['ip 192.168.1.1/24', 'ping 192.168.1.2']; o.VPC2 = ['ip 192.168.1.2/24'];
        return o; } },

    // ------------------------------------------------------------ 8.2
    { id: '8.2', title: 'Агрегация каналов (LACP)',
      goal: 'Два коммутатора соединены несколькими кабелями. Без агрегации STP оставит работать только один; объедините их в Port-channel 1 по LACP — каналы работают вместе, и связь сохраняется, пока жив хотя бы один кабель.',
      gen: function () { return { k: R(3, 8) }; },
      build: function (net, p) {
        var o = place(net, [['vMES1', 'MES2300-24', 300, 300], ['vMES2', 'MES2300-24', 700, 300], ['VPC1', 'VPC', 120, 500], ['VPC2', 'VPC', 880, 500]]);
        for (var i = 1; i <= p.k; i++) net.connect(o.vMES1.id, 'gi1/0/' + i, o.vMES2.id, 'gi1/0/' + i);
        wire(net, o, [['VPC1', 'eth0', 'vMES1', 'gi1/0/10'], ['VPC2', 'eth0', 'vMES2', 'gi1/0/10']]); },
      tasks: function (p) { var K = p.k, rng = 'gi1/0/1-' + K; return [
        vpcIp('VPC1', '192.168.10.10'), vpcIp('VPC2', '192.168.10.20')].concat(['vMES1', 'vMES2'].map(function (m) { return { t: m + ': interface port-channel 1, порты ' + rng + ' — channel-group 1 mode auto (LACP)',
          ok: function (n) { var s = dev(n, m); if (!s.pos || !s.pos.po1) return false;
            for (var i = 1; i <= K; i++) { var c = s.ports['gi1/0/' + i].cg; if (!c || c.id !== 1 || c.mode !== 'active') return false; } return true; } }; }), [
        { t: 'Отключите на vMES1 все кабели агрегата, кроме одного (shutdown на gi1/0/1-' + (K - 1) + ')', ok: function (n) { var s = dev(n, 'vMES1');
            for (var i = 1; i < K; i++) if (!s.ports['gi1/0/' + i].shut) return false; return !s.ports['gi1/0/' + K].shut; } },
        { t: 'Port-channel 1 собран на оставшемся канале, ping VPC1 → VPC2 проходит (show interfaces channel-group)', ok: function (n) {
            var L = n.lports(n.byName('vMES1').id).filter(function (l) { return l.name === 'po1'; })[0];
            return !!L && L.members.length === 1 && n.reach('VPC1', '192.168.10.20'); } }]); },
      sol: function (p) { var K = p.k, o = {};
        ['vMES1', 'vMES2'].forEach(function (m) {
          o[m] = ['enable', 'configure', 'hostname ' + m, 'interface port-channel 1', 'exit', 'interface range gigabitethernet 1/0/1-' + K,
                  'channel-group 1 mode auto', 'end', 'show interfaces channel-group']; });
        o.VPC1 = ['ip 192.168.10.10/24', 'ping 192.168.10.20']; o.VPC2 = ['ip 192.168.10.20/24'];
        o.vMES1 = o.vMES1.concat(K > 1 ? ['configure', 'interface range gigabitethernet 1/0/1-' + (K - 1), 'shutdown', 'end', 'show interfaces channel-group'] : []);
        return o; } },

    // ------------------------------------------------------------ 8.3
    { id: '8.3', title: 'Резервирование шлюза (VRRP)',
      goal: 'Два маршрутизатора делят один виртуальный адрес шлюза 192.168.10.1. Мастер отвечает за него; при разрыве мастера роль сразу берёт резервный, и ПК этого не замечают.',
      gen: function () { return { id: R(1, 255) }; },
      build: function (net) {
        var o = place(net, [['vESR1', 'vESR', 250, 120], ['vESR2', 'vESR', 750, 120], ['vMES', 'MES2300-24', 500, 330], ['VPC1', 'VPC', 270, 540], ['VPC2', 'VPC', 730, 540]]);
        wire(net, o, [['vESR1', 'gi1/0/1', 'vMES', 'gi1/0/1'], ['vESR2', 'gi1/0/1', 'vMES', 'gi1/0/2'], ['VPC1', 'eth0', 'vMES', 'gi1/0/3'], ['VPC2', 'eth0', 'vMES', 'gi1/0/4']]); },
      tasks: function (p) { var ID = p.id; return [
        ].concat(ifT('vESR1', [[1, '10.10.10.1/30']]), ifT('vESR2', [[1, '10.10.10.2/30']]), [vpcIp('VPC1', '192.168.10.10', '192.168.10.1'), vpcIp('VPC2', '192.168.10.11', '192.168.10.1')],
        ['vESR1', 'vESR2'].map(function (r) { return { t: r + ' gi1/0/1: vrrp id ' + ID + ', vrrp ip 192.168.10.1/24, vrrp', ok: function (n) {
            var v = run(n, r).ifs['gi1/0/1'].vrrp; return !!v && v.on && v.id === ID && v.ip === '192.168.10.1/24'; } }; }), [
        { t: 'Приоритеты: vESR2 — 200 (мастер), vESR1 сначала 210 (становится мастером), затем 180', ok: function (n) {
            return run(n, 'vESR2').ifs['gi1/0/1'].vrrp.prio === 200 && run(n, 'vESR1').ifs['gi1/0/1'].vrrp.prio === 180; } },
        { t: 'Разорвите связь мастера с сетью (shutdown на vMES gi1/0/2) — мастером должен стать vESR1, ping VPC1 → 192.168.10.1 не прерывается', ok: function (n) {
            var v = n.vrrp()[n.byName('vESR1').id]; return dev(n, 'vMES').ports['gi1/0/2'].shut && v && v['gi1/0/1'].master && n.reach('VPC1', '192.168.10.1'); } },
        { t: 'Применено: commit + confirm на обоих', ok: function (n) { return committed(n, ['vESR1', 'vESR2']); } }]); },
      sol: function (p) { var ID = p.id; function r(nm, ip, pr) { return ['configure', 'hostname ' + nm].concat(ifs([[1, ip]]), ['interface gigabitethernet 1/0/1',
          'vrrp id ' + ID, 'vrrp ip 192.168.10.1/24'].concat(pr ? ['vrrp priority ' + pr] : [], ['vrrp', 'exit', 'do commit', 'do confirm', 'end'])); }
        return { vESR2: r('vESR2', '10.10.10.2/30', 200), vESR1: r('vESR1', '10.10.10.1/30', 210).concat(['show vrrp', 'configure', 'interface gigabitethernet 1/0/1',
                   'vrrp priority 180', 'exit', 'do commit', 'do confirm', 'end', 'show vrrp']),
                 VPC1: ['ip 192.168.10.10/24 192.168.10.1'], VPC2: ['ip 192.168.10.11/24 192.168.10.1'],
                 vMES: ['enable', 'configure', 'interface gigabitethernet 1/0/2', 'shutdown', 'end'], 'VPC1 ': ['ping 192.168.10.1'] }; } }
  ];
  LABS[3].sol = (function (base) { return function (p) { var o = base.call(this, p), x = o['VPC1 ']; delete o['VPC1 ']; o.VPC1 = o.VPC1.concat(x); return o; }; })(LABS[3].sol);

  var all = EL.labs.LABS, at = all.map(function (l) { return l.id; }).indexOf('E.1');
  Array.prototype.splice.apply(all, [at < 0 ? all.length : at, 0].concat(LABS));
})(typeof window !== 'undefined' ? window : global);
