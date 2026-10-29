/* Лабораторные 6.1–6.4: DHCP-сервер, DHCP relay, Source/Destination NAT, NTP. Добавляются перед лабой поиска неисправности. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, PK = EL.pick, IP = EL.ip;

  function dev(n, name) { var d = n.byName(name); return d ? d.st : null; }
  function run(n, name) { return dev(n, name).run; }
  function ifs(list) { return list.reduce(function (o, x) { return o.concat(['interface gigabitethernet 1/0/' + x[0], 'ip address ' + x[1], 'ip firewall disable', 'exit']); }, []); }
  function ipsOk(n, name, list) { var f = run(n, name).ifs; return list.every(function (x) { var y = f['gi1/0/' + x[0]]; return y && y.ip === x[1] && !y.fw; }); }
  function committed(n, names) { return names.every(function (x) { var s = dev(n, x); return !s.pending && !s.unconfirmed && (s.commits || 0) > 0; }); }
  function hasRoute(n, name, net, nh) { return run(n, name).routes.some(function (r) { return r.net === net && r.nh === nh; }); }
  function place(net, items) { var o = {}; items.forEach(function (x) { o[x[0]] = net.add(x[1], x[0], x[2], x[3]); }); return o; }
  function wire(net, o, links) { links.forEach(function (l) { net.connect(o[l[0]].id, l[1], o[l[2]].id, l[3]); }); }
  function inPool(ip, a, b) { var n = IP.ip2n(ip); return ip && n >= IP.ip2n(a) && n <= IP.ip2n(b); }
  function debStatic(ip, gw) { return ['ip link set ens3 up', 'ip addr add ' + ip + ' dev ens3', 'ip route add default via ' + gw]; }
  function debOk(n, name, ip, gw) { var s = dev(n, name); return s.up && s.ip + '/' + s.len === ip && s.gw === gw; }
  function pool(n, r, name) { var d = run(n, r).dhcp; return d && d.pools[name]; }
  // «одно действие — один пункт»
  function ifT(r, list) { return list.map(function (x) { return { t: r + ' gi1/0/' + x[0] + ': ' + x[1] + ', экран отключён', ok: function (n) { return ipsOk(n, r, [x]); } }; }); }
  function comT(rs) { return rs.map(function (r) { return { t: r + ': всё применено (commit + confirm)', ok: function (n) { return committed(n, [r]); } }; }); }
  function vpcT(v, ip, gw) { return { t: v + ': ' + ip + '/24, шлюз ' + gw, ok: function (n) { var d = dev(n, v); return d.ip === ip && d.gw === gw; } }; }
  function debT(v, ip, gw) { return { t: v + ' (root/toor): ens3 ' + ip + ', шлюз ' + gw, ok: function (n) { return debOk(n, v, ip, gw); } }; }

  var LABS = [
    // ------------------------------------------------------------ 6.1
    { id: '6.1', title: 'DHCP-сервер на маршрутизаторе',
      goal: 'R1 раздаёт адреса компьютерам за коммутатором. Пошаговая трасса покажет обмен DISCOVER → OFFER → REQUEST → ACK.',
      gen: function () { return { x: R(10, 250), lo: PK([100, 50, 20]), lease: PK(['0:1:0', '0:0:30', '1:0:0']) }; },
      build: function (net) {
        var o = place(net, [['R1', 'vESR', 500, 110], ['SW1', 'MES2300-24', 500, 320], ['VPC1', 'VPC', 220, 500], ['VPC2', 'VPC', 500, 540], ['VPC3', 'VPC', 780, 500]]);
        wire(net, o, [['R1', 'gi1/0/1', 'SW1', 'gi1/0/1'], ['VPC1', 'eth0', 'SW1', 'gi1/0/10'], ['VPC2', 'eth0', 'SW1', 'gi1/0/11'], ['VPC3', 'eth0', 'SW1', 'gi1/0/12']]); },
      net: function (p) { var A = '192.168.' + p.x; return { A: A, a: A + '.' + p.lo, b: A + '.' + (p.lo + 100), pool: 'DHCP-' + p.x }; },
      tasks: function (p) { var N = this.net(p); return [
        { t: 'Имя R1 (hostname R1, затем commit + confirm)', ok: function (n) { return run(n, 'R1').host === 'R1'; } }].concat(ifT('R1', [[1, N.A + '.1/24']]), [
        { t: 'ip dhcp-server — DHCP-сервер включён', ok: function (n) { var c = run(n, 'R1'); return !!c.dhcp && c.dhcp.on; } },
        { t: 'Пул ' + N.pool + ': network ' + N.A + '.0/24', ok: function (n) { var q = pool(n, 'R1', N.pool); return !!q && q.net === N.A + '.0/24'; } },
        { t: 'Пул ' + N.pool + ': address-range ' + N.a + '-' + N.b, ok: function (n) { var q = pool(n, 'R1', N.pool); return !!q && !!q.range && q.range[0] === N.a && q.range[1] === N.b; } },
        { t: 'Пул ' + N.pool + ': default-router ' + N.A + '.1', ok: function (n) { var q = pool(n, 'R1', N.pool); return !!q && q.gw === N.A + '.1'; } },
        { t: 'Пул ' + N.pool + ': аренда ' + p.lease, ok: function (n) { var q = pool(n, 'R1', N.pool); return !!q && q.lease === p.lease; } },
        { t: 'Применено: commit + confirm', ok: function (n) { return committed(n, ['R1']); } }],
        ['VPC1', 'VPC2', 'VPC3'].map(function (v) { return { t: v + ' получил адрес по DHCP (ip dhcp) из ' + N.a + '–' + N.b, ok: function (n) { var s = dev(n, v); return s.dhcp && inPool(s.ip, N.a, N.b) && s.gw === N.A + '.1'; } }; }), [
        { t: 'VPC1 пингует VPC3', ok: function (n) { var v3 = dev(n, 'VPC3').ip; return !!v3 && n.reach('VPC1', v3); } },
        { t: 'VPC3 пингует шлюз ' + N.A + '.1', ok: function (n) { return n.reach('VPC3', N.A + '.1'); } }]); },
      sol: function (p) { var N = this.net(p); return {
        R1: ['configure', 'hostname R1'].concat(ifs([[1, N.A + '.1/24']]), ['ip dhcp-server', 'ip dhcp-server pool ' + N.pool, 'network ' + N.A + '.0/24',
             'address-range ' + N.a + '-' + N.b, 'default-router ' + N.A + '.1', 'default-lease-time ' + p.lease, 'exit', 'do commit', 'do confirm', 'end']),
        VPC1: ['ip dhcp', 'show ip'], VPC2: ['ip dhcp'], VPC3: ['ip dhcp', 'ping ' + N.A + '.1'],
        'R1 ': ['show ip dhcp binding'] }; } },

    // ------------------------------------------------------------ 6.2
    { id: '6.2', title: 'DHCP relay: сервер за двумя маршрутизаторами',
      goal: 'Адреса раздаёт R-DHCP, а компьютеры подключены к R1. R1 работает ретранслятором: ловит широковещательный DISCOVER и пересылает его серверу unicast-ом, указывая giaddr — по нему сервер выбирает пул.',
      gen: function () { return { lo: PK([100, 50, 150]) }; },
      build: function (net) {
        var o = place(net, [['VPC1', 'VPC', 90, 180], ['VPC2', 'VPC', 90, 440], ['R1', 'vESR', 330, 310], ['R2', 'vESR', 610, 310], ['R-DHCP', 'vESR', 880, 310]]);
        wire(net, o, [['VPC1', 'eth0', 'R1', 'gi1/0/2'], ['VPC2', 'eth0', 'R1', 'gi1/0/3'], ['R1', 'gi1/0/1', 'R2', 'gi1/0/1'], ['R2', 'gi1/0/2', 'R-DHCP', 'gi1/0/1']]); },
      tasks: function (p) { var a = p.lo, b = p.lo + 100; return [
        ].concat(ifT('R1', [[1, '192.168.10.1/30'], [2, '10.10.10.1/24'], [3, '172.16.10.1/24']]), ifT('R2', [[1, '192.168.10.2/30'], [2, '192.168.100.1/30']]), ifT('R-DHCP', [[1, '192.168.100.2/30']]), [
        { t: 'R-DHCP: ip dhcp-server включён', ok: function (n) { var c = run(n, 'R-DHCP'); return !!c.dhcp && c.dhcp.on; } },
        { t: 'R-DHCP: пул DHCP-10 — network 10.10.10.0/24, диапазон 10.10.10.' + a + '–' + b + ', шлюз 10.10.10.1', ok: function (n) { var x = pool(n, 'R-DHCP', 'DHCP-10');
            return !!x && x.net === '10.10.10.0/24' && !!x.range && x.range[0] === '10.10.10.' + a && x.gw === '10.10.10.1'; } },
        { t: 'R-DHCP: пул DHCP-172 — network 172.16.10.0/24, диапазон 172.16.10.' + a + '–' + b + ', шлюз 172.16.10.1', ok: function (n) { var y = pool(n, 'R-DHCP', 'DHCP-172');
            return !!y && y.net === '172.16.10.0/24' && !!y.range && y.range[0] === '172.16.10.' + a && y.gw === '172.16.10.1'; } },
        { t: 'R1: ip dhcp-relay', ok: function (n) { return !!run(n, 'R1').relay; } },
        { t: 'R1 gi1/0/2: ip helper-address 192.168.100.2', ok: function (n) { return run(n, 'R1').ifs['gi1/0/2'].helper === '192.168.100.2'; } },
        { t: 'R1 gi1/0/3: ip helper-address 192.168.100.2', ok: function (n) { return run(n, 'R1').ifs['gi1/0/3'].helper === '192.168.100.2'; } },
        { t: 'R1: маршрут 0.0.0.0/0 через 192.168.10.2', ok: function (n) { return hasRoute(n, 'R1', '0.0.0.0/0', '192.168.10.2'); } },
        { t: 'R-DHCP: маршрут 0.0.0.0/0 через 192.168.100.1', ok: function (n) { return hasRoute(n, 'R-DHCP', '0.0.0.0/0', '192.168.100.1'); } },
        { t: 'R2: маршрут до 10.10.10.0/24 через 192.168.10.1', ok: function (n) { return hasRoute(n, 'R2', '10.10.10.0/24', '192.168.10.1'); } },
        { t: 'R2: маршрут до 172.16.10.0/24 через 192.168.10.1', ok: function (n) { return hasRoute(n, 'R2', '172.16.10.0/24', '192.168.10.1'); } }], comT(['R1', 'R2', 'R-DHCP']), [
        { t: 'VPC1 получил адрес по DHCP из 10.10.10.' + a + '–' + b, ok: function (n) { var v1 = dev(n, 'VPC1'); return v1.dhcp && inPool(v1.ip, '10.10.10.' + a, '10.10.10.' + b); } },
        { t: 'VPC2 получил адрес по DHCP из 172.16.10.' + a + '–' + b, ok: function (n) { var v2 = dev(n, 'VPC2'); return v2.dhcp && inPool(v2.ip, '172.16.10.' + a, '172.16.10.' + b); } },
        { t: 'VPC1 пингует VPC2', ok: function (n) { var v2 = dev(n, 'VPC2').ip; return !!v2 && n.reach('VPC1', v2); } },
        { t: 'VPC2 пингует сервер 192.168.100.2', ok: function (n) { return n.reach('VPC2', '192.168.100.2'); } }]); },
      sol: function (p) { var a = p.lo, b = p.lo + 100; return {
        'R-DHCP': ['configure', 'hostname R-DHCP'].concat(ifs([[1, '192.168.100.2/30']]), ['ip dhcp-server',
          'ip dhcp-server pool DHCP-10', 'network 10.10.10.0/24', 'address-range 10.10.10.' + a + '-10.10.10.' + b, 'default-router 10.10.10.1', 'default-lease-time 0:0:30', 'exit',
          'ip dhcp-server pool DHCP-172', 'network 172.16.10.0/24', 'address-range 172.16.10.' + a + '-172.16.10.' + b, 'default-router 172.16.10.1', 'exit',
          'ip route 0.0.0.0/0 192.168.100.1', 'do commit', 'do confirm', 'end']),
        R2: ['configure', 'hostname R2'].concat(ifs([[1, '192.168.10.2/30'], [2, '192.168.100.1/30']]),
          ['ip route 10.10.10.0/24 192.168.10.1', 'ip route 172.16.10.0/24 192.168.10.1', 'do commit', 'do confirm', 'end']),
        R1: ['configure', 'hostname R1'].concat(ifs([[1, '192.168.10.1/30'], [2, '10.10.10.1/24'], [3, '172.16.10.1/24']]), ['ip dhcp-relay',
          'interface gigabitethernet 1/0/2', 'ip helper-address 192.168.100.2', 'exit', 'interface gigabitethernet 1/0/3', 'ip helper-address 192.168.100.2', 'exit',
          'ip route 0.0.0.0/0 192.168.10.2', 'do commit', 'do confirm', 'end']),
        VPC1: ['ip dhcp'], VPC2: ['ip dhcp', 'ping 192.168.100.2'] }; } },

    // ------------------------------------------------------------ 6.3
    { id: '6.3', title: 'Source NAT и Destination NAT',
      goal: 'Две одинаковые частные сети 192.168.1.0/24 за R1 и R2 выходят в «интернет» (ISP) под адресом внешнего интерфейса — Source NAT. На R2 веб-сервер публикуется наружу по TCP 80 — Destination NAT. Docker-браузер за R1 открывает сайт по внешнему адресу R2.',
      gen: function () { return { y: R(10, 99) }; },
      build: function (net) {
        var o = place(net, [['R1', 'vESR', 330, 330], ['ISP', 'vESR', 500, 110], ['R2', 'vESR', 670, 330], ['SW1', 'MES2300-24', 260, 470], ['SW2', 'MES2300-24', 740, 470],
                            ['Docker', 'Docker', 60, 470], ['VPC1', 'VPC', 260, 595], ['VPC2', 'VPC', 740, 595], ['Server', 'Debian-server', 940, 470]]);
        wire(net, o, [['R1', 'gi1/0/1', 'ISP', 'gi1/0/1'], ['R2', 'gi1/0/1', 'ISP', 'gi1/0/2'], ['R1', 'gi1/0/3', 'SW1', 'gi1/0/1'], ['R2', 'gi1/0/3', 'SW2', 'gi1/0/1'],
                      ['Docker', 'ens3', 'SW1', 'gi1/0/3'], ['VPC1', 'eth0', 'SW1', 'gi1/0/2'], ['VPC2', 'eth0', 'SW2', 'gi1/0/2'], ['Server', 'ens3', 'SW2', 'gi1/0/12']]); },
      net: function (p) { var Y = '10.' + p.y; return { r1: Y + '.10.2', isp1: Y + '.10.1', r2: Y + '.50.2', isp2: Y + '.50.1', Y: Y }; },
      tasks: function (p) { var N = this.net(p); return [
        ].concat(ifT('R1', [[1, N.r1 + '/30'], [3, '192.168.1.1/24']]), ifT('R2', [[1, N.r2 + '/30'], [3, '192.168.1.1/24']]), ifT('ISP', [[1, N.isp1 + '/30'], [2, N.isp2 + '/30']]), [
        vpcT('VPC1', '192.168.1.100', '192.168.1.1'), vpcT('VPC2', '192.168.1.10', '192.168.1.1'), debT('Docker', '192.168.1.25/24', '192.168.1.1'), debT('Server', '192.168.1.100/24', '192.168.1.1'),
        { t: 'R1: маршрут по умолчанию на ISP (' + N.isp1 + ')', ok: function (n) { return hasRoute(n, 'R1', '0.0.0.0/0', N.isp1); } },
        { t: 'R2: маршрут по умолчанию на ISP (' + N.isp2 + ')', ok: function (n) { return hasRoute(n, 'R2', '0.0.0.0/0', N.isp2); } }],
        ['R1', 'R2'].map(function (r) { return { t: r + ': Source NAT — ruleset SNAT, to interface gi1/0/1, rule 10: 192.168.1.1-192.168.1.254 → action source-nat interface, enable', ok: function (n) {
            var s = run(n, r).snat, x = s && s.rulesets.SNAT, q = x && x.rules[10];
            return !!x && x.ifn === 'gi1/0/1' && !!q && q.on && q.act === 'interface' && !!q.src && q.src[0] === '192.168.1.1' && q.src[1] === '192.168.1.254'; } }; }), [
        { t: 'VPC1 пингует ISP ' + N.isp1 + ' (без NAT ответ не вернулся бы — у ISP нет маршрута в 192.168.1.0/24)', ok: function (n) { return n.reach('VPC1', N.isp1); } },
        { t: 'VPC2 пингует ISP ' + N.isp1, ok: function (n) { return n.reach('VPC2', N.isp1); } },
        { t: 'Destination NAT на R2: ruleset Dest_NAT from interface gi1/0/1, rule 10 — tcp, порт 80 → netmap 192.168.1.100/32, enable', ok: function (n) {
            var d = run(n, 'R2').dnat, x = d && d.rulesets.Dest_NAT, q = x && x.rules[10];
            return x && x.ifn === 'gi1/0/1' && q && q.on && q.proto === 'tcp' && q.dport && q.dport[0] === 80 && q.to === '192.168.1.100'; } },
        { t: 'Docker открывает сайт http://' + N.r2 + ' (open http://' + N.r2 + ')', ok: function (n) { return n.http('Docker', N.r2, 80); } }], comT(['R1', 'R2', 'ISP'])); },
      sol: function (p) { var N = this.net(p);
        var snat = ['nat source', 'ruleset SNAT', 'to interface gigabitethernet 1/0/1', 'rule 10', 'match source-address address-range 192.168.1.1-192.168.1.254',
                    'action source-nat interface', 'enable', 'exit', 'exit', 'exit'];
        return {
          ISP: ['configure', 'hostname ISP'].concat(ifs([[1, N.isp1 + '/30'], [2, N.isp2 + '/30']]), ['do commit', 'do confirm', 'end']),
          R1: ['configure', 'hostname R1'].concat(ifs([[1, N.r1 + '/30'], [3, '192.168.1.1/24']]), snat, ['ip route 0.0.0.0/0 ' + N.isp1, 'do commit', 'do confirm', 'end']),
          R2: ['configure', 'hostname R2'].concat(ifs([[1, N.r2 + '/30'], [3, '192.168.1.1/24']]), snat, ['ip route 0.0.0.0/0 ' + N.isp2,
               'nat destination', 'ruleset Dest_NAT', 'from interface gigabitethernet 1/0/1', 'rule 10', 'match protocol tcp', 'match destination-port port-range 80',
               'action destination-nat netmap 192.168.1.100/32', 'enable', 'exit', 'exit', 'exit', 'do commit', 'do confirm', 'end']),
          VPC1: ['ip 192.168.1.100/24 192.168.1.1', 'ping ' + N.isp1], VPC2: ['ip 192.168.1.10/24 192.168.1.1'],
          Server: ['root', 'toor'].concat(debStatic('192.168.1.100/24', '192.168.1.1'), ['systemctl status apache2']),
          Docker: debStatic('192.168.1.25/24', '192.168.1.1').concat(['open http://' + N.r2]) }; } },

    // ------------------------------------------------------------ 6.4
    { id: '6.4', title: 'Синхронизация времени по NTP',
      goal: 'На сервере Debian своя дата и свой часовой пояс. vESR синхронизируется с ним по NTP, затем на vESR выставляется тот же пояс — и show date совпадает с date на сервере.',
      gen: function () { return { tz: PK([3, 7, 8, 10]), y: PK([2010, 2015, 2020]), m: R(1, 12), d: R(1, 28), h: R(0, 23) }; },
      build: function (net, p) {
        var o = place(net, [['vESR', 'vESR', 330, 320], ['Server', 'Debian-server', 700, 320]]);
        wire(net, o, [['vESR', 'gi1/0/1', 'Server', 'ens3']]);
        o.Server.st.tz = p.tz; },
      when: function (p) { return p.y + '-' + ('0' + p.m).slice(-2) + '-' + ('0' + p.d).slice(-2) + ' ' + ('0' + p.h).slice(-2) + ':00:00'; },
      tasks: function (p) { var W = this.when(p), target = Date.UTC(p.y, p.m - 1, p.d, p.h) - p.tz * 3600e3; return [
        ].concat(ifT('vESR', [[1, '192.168.1.1/24']]), [debT('Server', '192.168.1.10/24', '192.168.1.1'),
        { t: 'На сервере выставьте время ' + W + ' (местное, пояс GMT+' + p.tz + '): timedatectl set-ntp false, затем set-time', ok: function (n) {
            var s = dev(n, 'Server'); return Math.abs(EL.clock.now() + s.clk - target) < 6 * 3600e3; } },
        { t: 'vESR: ntp enable, ntp server 192.168.1.10 (minpoll 1, maxpoll 4)', ok: function (n) { var c = run(n, 'vESR').ntp, x = c && c.servers['192.168.1.10'];
            return c && c.on && x && x.minpoll === 1 && x.maxpoll === 4; } },
        { t: 'vESR синхронизирован с сервером (show ntp peers — звёздочка у 192.168.1.10)', ok: function (n) {
            var pr = n.ntpPeer(n.byName('vESR').id); return !!pr && pr.utc !== null; } },
        { t: 'Часовой пояс vESR совпадает с сервером: clock timezone gmt +' + p.tz + ' — тогда show date = date на сервере', ok: function (n) { return run(n, 'vESR').tz === '+' + p.tz; } },
        { t: 'Применено: commit + confirm', ok: function (n) { return committed(n, ['vESR']); } }]); },
      sol: function (p) { return {
        Server: ['root', 'toor'].concat(debStatic('192.168.1.10/24', '192.168.1.1'), ['systemctl status chronyd', 'timedatectl set-ntp false',
                 "timedatectl set-time '" + this.when(p) + "'", 'timedatectl set-ntp true', 'systemctl restart chronyd', 'date']),
        vESR: ['configure'].concat(ifs([[1, '192.168.1.1/24']]), ['ntp enable', 'ntp server 192.168.1.10', 'minpoll 1', 'maxpoll 4', 'exit',
               'clock timezone gmt +' + p.tz, 'do commit', 'do confirm', 'end', 'show ntp peers', 'show date']) }; } }
  ];
  // служебные ключи 'R1 ' в 6.1 — команды после настройки ПК
  LABS[0].sol = (function (base) { return function (p) { var o = base.call(this, p), x = o['R1 ']; delete o['R1 ']; o.R1 = o.R1.concat(x); return o; }; })(LABS[0].sol);

  var all = EL.labs.LABS, at = all.map(function (l) { return l.id; }).indexOf('T.1');
  Array.prototype.splice.apply(all, [at < 0 ? all.length : at, 0].concat(LABS));
})(typeof window !== 'undefined' ? window : global);
