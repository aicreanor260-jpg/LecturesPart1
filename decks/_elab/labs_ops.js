/* Лабораторные 10.1 (LLDP), 10.2 (syslog), 10.3 (SPAN — зеркалирование на MES), 10.4 (резервные копии конфигурации на TFTP). */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, PK = EL.pick;

  function dev(n, name) { var d = n.byName(name); return d ? d.st : null; }
  function run(n, name) { return dev(n, name).run; }
  function ifs(list) { return list.reduce(function (o, x) { return o.concat(['interface gigabitethernet 1/0/' + x[0], 'ip address ' + x[1], 'ip firewall disable', 'exit']); }, []); }
  function ipsOk(n, name, list) { var f = run(n, name).ifs; return list.every(function (x) { var y = f['gi1/0/' + x[0]]; return y && y.ip === x[1] && !y.fw; }); }
  function committed(n, names) { return names.every(function (x) { var s = dev(n, x); return !s.pending && !s.unconfirmed; }); }
  function place(net, items) { var o = {}; items.forEach(function (x) { o[x[0]] = net.add(x[1], x[0], x[2], x[3]); }); return o; }
  function wire(net, o, links) { links.forEach(function (l) { net.connect(o[l[0]].id, l[1], o[l[2]].id, l[3]); }); }
  function debOk(n, name, ip, gw) { var s = dev(n, name); return s.up && s.ip + '/' + s.len === ip && s.gw === gw; }
  function debIp(ip, gw) { return ['root', 'toor', 'ip link set ens3 up', 'ip addr add ' + ip + ' dev ens3', 'ip route add default via ' + gw]; }
  function srvLab(net) { var o = place(net, [['vESR', 'vESR', 330, 320], ['Server', 'Debian-server', 700, 320]]); wire(net, o, [['vESR', 'gi1/0/1', 'Server', 'ens3']]); }
  function file(n, path) { return dev(n, 'Server').files[path]; }

  var LABS = [
    // ------------------------------------------------------------ 10.1
    { id: '10.1', title: 'Протокол LLDP на маршрутизаторах',
      goal: 'Маршрутизаторы рассказывают соседям о себе: имя, порт, MAC. Включите LLDP, посмотрите соседей, смените имя — сосед увидит новое. Затем отключите рассылку на одном — и он пропадёт у соседа, но сам продолжит видеть его.',
      gen: function () { return { a: R(1, 2) }; },
      build: function (net) { var o = place(net, [['vESR1', 'vESR', 300, 320], ['vESR2', 'vESR', 700, 320]]); wire(net, o, [['vESR1', 'gi1/0/1', 'vESR2', 'gi1/0/1']]); },
      tasks: function (p) { var A = 'vESR' + p.a, B = 'vESR' + (3 - p.a), RA = 'R' + p.a; return [
        { t: 'На обоих: lldp enable; на gi1/0/1 — lldp receive' + ' и lldp transmit (на ' + A + ' рассылку потом выключите)', ok: function (n) {
            return [A, B].every(function (r) { var c = run(n, r); return c.lldp && c.ifs['gi1/0/1'].lldpRx; }) && run(n, B).ifs['gi1/0/1'].lldpTx; } },
        { t: 'Смените имя ' + A + ' на ' + RA + ' — в show lldp neighbors на ' + B + ' появится новое имя', ok: function (n) { return run(n, A).host === RA; } },
        { t: 'На ' + RA + ' (gi1/0/1): no lldp transmit', ok: function (n) { return !run(n, A).ifs['gi1/0/1'].lldpTx; } },
        { t: 'Итог: ' + RA + ' видит соседа ' + B + ', а ' + B + ' соседей не видит', ok: function (n) {
            return n.lldpText(n.byName(A).id).indexOf(run(n, B).host) >= 0 && /Соседей нет/.test(n.lldpText(n.byName(B).id)); } },
        { t: 'Применено: commit + confirm', ok: function (n) { return committed(n, [A, B]); } }]; },
      sol: function (p) { var A = 'vESR' + p.a, B = 'vESR' + (3 - p.a), o = {};
        [A, B].forEach(function (r) { o[r] = ['configure', 'hostname ' + r, 'lldp enable', 'interface gigabitethernet 1/0/1', 'lldp receive', 'lldp transmit', 'exit',
          'do commit', 'do confirm', 'end', 'show lldp neighbors']; });
        o[A] = o[A].concat(['configure', 'hostname R' + p.a, 'interface gigabitethernet 1/0/1', 'no lldp transmit', 'exit', 'do commit', 'do confirm', 'end', 'show lldp neighbors']);
        return o; } },

    // ------------------------------------------------------------ 10.2
    { id: '10.2', title: 'Отправка syslog-сообщений на удалённый сервер',
      goal: 'vESR пишет журнал событий на сервер Debian (rsyslog, UDP 514). Сначала синхронизируйте время по NTP — иначе метки времени в журнале не совпадут. Каждая введённая команда и вход по SSH попадают в /var/log/rsyslog/<имя>/.',
      gen: function () { return { h: PK(['SERVER', 'LOGSRV', 'SYSLOG']), sev: PK(['info', 'notice', 'debug']) }; },
      build: srvLab,
      tasks: function (p) { return [
        { t: 'vESR gi1/0/1 — 192.168.1.1/24; Server (root/toor) — 192.168.1.10/24, шлюз 192.168.1.1', ok: function (n) {
            return ipsOk(n, 'vESR', [[1, '192.168.1.1/24']]) && debOk(n, 'Server', '192.168.1.10/24', '192.168.1.1'); } },
        { t: 'NTP: ntp enable, ntp server 192.168.1.10 (minpoll 1, maxpoll 4), clock timezone gmt +7', ok: function (n) { var c = run(n, 'vESR'), s = c.ntp && c.ntp.servers['192.168.1.10'];
            return c.ntp && c.ntp.on && s && s.minpoll === 1 && s.maxpoll === 4 && c.tz === '+7'; } },
        { t: 'syslog host ' + p.h + ': source-address 192.168.1.1, remote-address 192.168.1.10, transport udp, port 514, severity ' + p.sev, ok: function (n) {
            var x = (run(n, 'vESR').syslog || {})[p.h]; return x && x.src === '192.168.1.1' && x.ip === '192.168.1.10' && x.proto === 'udp' && x.port === 514 && x.sev === p.sev; } },
        { t: 'Применено: commit + confirm', ok: function (n) { return committed(n, ['vESR']); } },
        { t: 'На сервере есть /var/log/rsyslog/vESR/klish.log с командами (ls, cat)', ok: function (n) { var f = file(n, '/var/log/rsyslog/vESR/klish.log');
            return !!f && /CLI-I-CMD/.test(f); } },
        { t: 'Войдите на vESR по SSH с сервера (ip ssh server, ssh admin@192.168.1.1) — появится login.log', ok: function (n) { return !!file(n, '/var/log/rsyslog/vESR/login.log'); } }]; },
      sol: function (p) { return {
        Server: debIp('192.168.1.10/24', '192.168.1.1').concat(['systemctl status chronyd']),
        vESR: ['configure', 'hostname vESR'].concat(ifs([[1, '192.168.1.1/24']]), ['ip ssh server', 'ntp enable', 'ntp server 192.168.1.10', 'minpoll 1', 'maxpoll 4', 'exit',
          'clock timezone gmt +7', 'syslog host ' + p.h, 'source-address 192.168.1.1', 'remote-address 192.168.1.10', 'transport udp', 'port 514', 'severity ' + p.sev, 'exit',
          'do commit', 'do confirm', 'end', 'show ntp peers']),
        'Server #2': ['ls /var/log/rsyslog/', 'ssh admin@192.168.1.1', 'password', 'show date', 'exit', 'ls /var/log/rsyslog/vESR', 'cat /var/log/rsyslog/vESR/login.log'] }; } },

    // ------------------------------------------------------------ 10.3
    { id: '10.3', title: 'Локальное зеркалирование портов (SPAN)',
      goal: 'Копия всего трафика порта, к которому подключён ПК, уходит на порт gi1/0/12 — туда подключён анализатор (Debian, tcpdump). Синтаксис — настоящий MES: monitor session.',
      gen: function () { return { src: R(1, 2) }; },
      build: function (net) {
        var o = place(net, [['vMES1', 'MES2428', 500, 300], ['VPC1', 'VPC', 220, 520], ['VPC2', 'VPC', 780, 520], ['Sniffer', 'Debian', 500, 90]]);
        wire(net, o, [['VPC1', 'eth0', 'vMES1', 'gi1/0/1'], ['VPC2', 'eth0', 'vMES1', 'gi1/0/2'], ['Sniffer', 'ens3', 'vMES1', 'gi1/0/12']]); },
      tasks: function (p) { var S = 'gi1/0/' + p.src; return [
        { t: 'VPC1 192.168.10.10/24, VPC2 192.168.10.20/24', ok: function (n) { return dev(n, 'VPC1').ip === '192.168.10.10' && dev(n, 'VPC2').ip === '192.168.10.20'; } },
        { t: 'monitor session 1 destination interface gi1/0/12', ok: function (n) { var m = (dev(n, 'vMES1').mon || {})[1]; return m && m.dst === 'gi1/0/12'; } },
        { t: 'monitor session 1 source interface ' + S + ' both (зеркалим порт VPC' + p.src + ')', ok: function (n) { var m = (dev(n, 'vMES1').mon || {})[1];
            return m && m.src[S] === 'both'; } },
        { t: 'Ping между VPC1 и VPC2 — анализатор получил копии запросов и ответов (на Sniffer: tcpdump)', ok: function (n) { return (dev(n, 'Sniffer').capN || 0) >= 2; } }]; },
      sol: function (p) { return {
        vMES1: ['enable', 'configure', 'hostname vMES1', 'monitor session 1 destination interface gigabitethernet 1/0/12',
                'monitor session 1 source interface gigabitethernet 1/0/' + p.src + ' both', 'end', 'show monitor session 1'],
        VPC1: ['ip 192.168.10.10/24'], VPC2: ['ip 192.168.10.20/24', 'ping 192.168.10.10'], Sniffer: ['root', 'toor', 'tcpdump'] }; } },

    // ------------------------------------------------------------ 10.4
    { id: '10.4', title: 'Резервные копии конфигурации на TFTP-сервер',
      goal: 'Скопируйте конфигурацию vESR на TFTP-сервер вручную, затем настройте archive: после каждого commit копия уходит на сервер сама.',
      gen: function () { return { f: 'run' + R(1, 99) + '.cfg', b: 'Backup_' + PK(['run', 'cfg', 'R1']) + '.cfg', ban: PK(['Router R1', 'Eltex vESR', 'Lab router']) }; },
      build: srvLab,
      tasks: function (p) { return [
        { t: 'vESR gi1/0/1 — 192.168.1.1/24; Server (root/toor) — 192.168.1.10/24, шлюз 192.168.1.1; служба tftpd-hpa запущена', ok: function (n) {
            return ipsOk(n, 'vESR', [[1, '192.168.1.1/24']]) && debOk(n, 'Server', '192.168.1.10/24', '192.168.1.1') && dev(n, 'Server').svc['tftpd-hpa']; } },
        { t: 'copy system:running-config tftp://192.168.1.10:/' + p.f + ' — файл появился в /tftp', ok: function (n) { return !!file(n, '/tftp/' + p.f); } },
        { t: 'archive: type remote, path tftp://192.168.1.10:/' + p.b + ', by-commit', ok: function (n) { var a = run(n, 'vESR').archive;
            return a && a.type === 'remote' && a.path === 'tftp://192.168.1.10:/' + p.b && a.byCommit; } },
        { t: 'banner login "' + p.ban + '" + commit — свежая копия ' + p.b + ' на сервере содержит баннер', ok: function (n) { var f = file(n, '/tftp/' + p.b);
            return !!f && f.indexOf('banner login "' + p.ban + '"') >= 0; } },
        { t: 'Применено: commit + confirm', ok: function (n) { return committed(n, ['vESR']); } }]; },
      sol: function (p) { return {
        Server: debIp('192.168.1.10/24', '192.168.1.1').concat(['service tftpd-hpa status', 'service tftpd-hpa restart', 'ls /tftp']),
        vESR: ['configure', 'hostname vESR'].concat(ifs([[1, '192.168.1.1/24']]), ['do commit', 'do confirm', 'end', 'copy system:running-config tftp://192.168.1.10:/' + p.f,
          'configure', 'archive', 'type remote', 'path tftp://192.168.1.10:/' + p.b, 'by-commit', 'do commit', 'do confirm', 'exit',
          'banner login "' + p.ban + '"', 'do commit', 'do confirm', 'end']),
        'Server #2': ['ls /tftp', 'cat /tftp/' + p.b] }; } }
  ];

  var all = EL.labs.LABS, at = all.map(function (l) { return l.id; }).indexOf('E.1');
  Array.prototype.splice.apply(all, [at < 0 ? all.length : at, 0].concat(LABS));
})(typeof window !== 'undefined' ? window : global);
