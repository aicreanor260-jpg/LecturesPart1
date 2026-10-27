/* Сценарии «Найди неисправность» по образцу T.1: схема уже настроена, но в ней одна ошибка из списка (fault),
   студент ищет её командами show / ping / трассой и исправляет. Решение — исправление ровно этой ошибки. */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd, L = EL.labs;
  function apply(net, s) { return L.apply(net, s); }
  function deb(ip, gw) { return ['root', 'toor', 'ip link set ens3 up', 'ip addr add ' + ip + ' dev ens3'].concat(gw ? ['ip route add default via ' + gw] : []); }
  function esr(lines) { return ['configure'].concat(lines, ['end', 'commit', 'confirm']); }

  var T2 = {
    id: 'T.2', title: 'Поиск неисправности: статическая маршрутизация между двумя ESR',
    goal: 'Офис (VPC1 за R1) должен видеть сервер SRV за R2. Маршруты настроены статически, но ping VPC1 → SRV не проходит. Найдите и исправьте одну ошибку.',
    gen: function () { return { a: R(1, 254), b: R(16, 31), fault: R(0, 5) }; },
    build: function (net, p) {
      var r1 = net.add('vESR', 'R1', 300, 200), r2 = net.add('vESR', 'R2', 640, 200), sw = net.add('MES2428', 'SW1', 300, 400), v = net.add('VPC', 'VPC1', 140, 540),
          srv = net.add('Debian-server', 'SRV', 820, 400);
      net.connect(r1.id, 'gi1/0/1', r2.id, 'gi1/0/1'); net.connect(r1.id, 'gi1/0/2', sw.id, 'gi1/0/24'); net.connect(v.id, 'eth0', sw.id, 'gi1/0/1'); net.connect(srv.id, 'ens3', r2.id, 'gi1/0/2');
      var A = '192.168.' + p.a, B = '172.' + p.b + '.0', f = p.fault;
      apply(net, {
        R1: esr(['interface gi1/0/1', 'ip address ' + (f === 5 ? '10.0.21.1/30' : '10.0.12.1/30'), 'ip firewall disable', 'exit',
                 'interface gi1/0/2', 'ip address ' + A + '.1/24', 'ip firewall disable', 'exit', 'ip route ' + B + '.0/24 ' + (f === 0 ? '10.0.12.3' : '10.0.12.2')]),
        R2: esr(['interface gi1/0/1', 'ip address 10.0.12.2/30', 'ip firewall disable'].concat(f === 4 ? ['shutdown'] : []).concat(['exit',
                 'interface gi1/0/2', 'ip address ' + B + '.1/24'], f === 2 ? [] : ['ip firewall disable'], ['exit'], f === 1 ? [] : ['ip route ' + A + '.0/24 10.0.12.1'])),
        VPC1: ['ip ' + A + '.10/24 ' + (f === 3 ? A + '.254' : A + '.1')],
        SRV: deb(B + '.10/24', B + '.1') });
      p.A = A; p.B = B;
    },
    tasks: function (p) { var A = '192.168.' + p.a, B = '172.' + p.b + '.0'; return [
      { t: 'VPC1 (' + A + '.10) пингует SRV (' + B + '.10)', ok: function (n) { return n.reach('VPC1', B + '.10'); } },
      { t: 'R1 пингует SRV, SRV пингует VPC1', ok: function (n) { return n.reach('R1', B + '.10') && n.reach('SRV', A + '.10'); } }]; },
    sol: function (p) { var A = '192.168.' + p.a, B = '172.' + p.b + '.0';
      return [
        { R1: esr(['no ip route ' + B + '.0/24 10.0.12.3', 'ip route ' + B + '.0/24 10.0.12.2']) },
        { R2: esr(['ip route ' + A + '.0/24 10.0.12.1']) },
        { R2: esr(['interface gi1/0/2', 'ip firewall disable', 'exit']) },
        { VPC1: ['ip ' + A + '.10/24 ' + A + '.1'] },
        { R2: esr(['interface gi1/0/1', 'no shutdown', 'exit']) },
        { R1: esr(['interface gi1/0/1', 'ip address 10.0.12.1/30', 'exit']) }][p.fault]; },
    hint: function (p) { return ['show ip route на R1: через какой next-hop идёт сеть сервера и есть ли он в подключённой сети?',
      'Пакет доходит до SRV, а ответ? show ip route на R2 — знает ли он сеть офиса?', 'R2 получает пакет на gi1/0/2 и молчит — посмотрите межсетевой экран интерфейса',
      'show на VPC1 — правильный ли шлюз?', 'show interfaces status на R2 — все ли интерфейсы Up?', 'show ip interfaces на R1 и R2 — в одной ли сети адреса между ними?'][p.fault]; }
  };
  // R1 у сломанного варианта 5 имеет другой адрес — исправление заменяет его
  var noAddr = T2.sol; T2.sol = function (p) { var s = noAddr(p); if (p.fault === 5) s.R1.splice(2, 0, 'no ip address 10.0.21.1/30'); return s; };

  var ZONE = function (B, www) { return '$TTL 604800\n@\tIN\tSOA\tns.lab.local. root.lab.local. (\n\t\t2\t; Serial\n\t\t604800 )\t; Negative Cache TTL\n@\tIN\tNS\tns.lab.local.\nns\tIN\tA\t' + B + '.10\nwww\tIN\tA\t' + www + '\n'; };
  var T3 = {
    id: 'T.3', title: 'Поиск неисправности: DNS — сайт не открывается по имени',
    goal: 'На SRV работает DNS-сервер BIND9 с зоной lab.local и сайт www.lab.local. VPC1 не может выполнить ping www.lab.local. Найдите и исправьте одну ошибку (nslookup на SRV, show на VPC1, трасса).',
    gen: function () { return { a: R(1, 254), b: R(16, 31), fault: R(0, 5) }; },
    build: function (net, p) {
      var r1 = net.add('vESR', 'R1', 460, 200), sw = net.add('MES2428', 'SW1', 300, 400), v = net.add('VPC', 'VPC1', 140, 540), srv = net.add('Debian-server', 'SRV', 720, 400);
      net.connect(r1.id, 'gi1/0/1', sw.id, 'gi1/0/24'); net.connect(v.id, 'eth0', sw.id, 'gi1/0/1'); net.connect(srv.id, 'ens3', r1.id, 'gi1/0/2');
      var A = '192.168.' + p.a, B = '10.' + p.b + '.0', f = p.fault;
      apply(net, { R1: esr(['interface gi1/0/1', 'ip address ' + A + '.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address ' + B + '.1/24'].concat(f === 4 ? [] : ['ip firewall disable'], ['exit'])),
                   VPC1: ['ip ' + A + '.10/24 ' + A + '.1', 'ip dns ' + (f === 0 ? B + '.11' : B + '.10')],
                   SRV: deb(B + '.10/24', f === 5 ? null : B + '.1') });
      var st = srv.st;
      st.files['/etc/bind/named.conf.local'] += 'zone "' + (f === 3 ? 'lab.locl' : 'lab.local') + '" {\n\ttype master;\n\tfile "/etc/bind/db.lab.local";\n};\n';
      st.files['/etc/bind/db.lab.local'] = ZONE(B, f === 2 ? B + '.99' : B + '.10');
      apply(net, { SRV: f === 1 ? ['systemctl stop bind9'] : ['systemctl restart bind9'] });
      p.A = A; p.B = B;
    },
    tasks: function () { return [
      { t: 'VPC1: ping www.lab.local — имя разрешается и сервер отвечает', ok: function (n) { var v = n.byName('VPC1'), tr = n.onTrace; n.onTrace = null;   // проверка не должна открывать трассу
        try { var r = n.resolve(v.id, 'www.lab.local'); return !!r.ip && n.ping(v.id, r.ip).ok; } finally { n.onTrace = tr; } } }]; },
    sol: function (p) { var B = '10.' + p.b + '.0';
      return [
        { VPC1: ['ip dns ' + B + '.10'] },
        { SRV: ['systemctl start bind9'] },
        { SRV: ['sed -i s/' + B + '.99/' + B + '.10/ /etc/bind/db.lab.local', 'systemctl restart bind9'] },
        { SRV: ['sed -i s/lab.locl/lab.local/ /etc/bind/named.conf.local', 'systemctl restart bind9'] },
        { R1: esr(['interface gi1/0/2', 'ip firewall disable', 'exit']) },
        { SRV: ['ip route add default via ' + B + '.1'] }][p.fault]; },
    hint: function (p) { return ['show на VPC1 — какой DNS-сервер указан?', 'systemctl status bind9 на SRV', 'nslookup www.lab.local на SRV — тот ли адрес в ответе? Посмотрите файл зоны',
      'nslookup www.lab.local на SRV отвечает NXDOMAIN — проверьте имя зоны в /etc/bind/named.conf.local', 'Запрос DNS до SRV не доходит — межсетевой экран на R1 gi1/0/2?',
      'Запрос доходит, ответа нет — ip route на SRV: есть ли шлюз по умолчанию?'][p.fault]; }
  };
  L.LABS.push(T2, T3);
})(typeof window !== 'undefined' ? window : global);
