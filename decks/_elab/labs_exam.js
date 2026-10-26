/* Итоговый практический экзамен NTF-2, задание «Вариант 1» на трёх топологиях из пакета Eltex (Final Exam 1–3.unl).
   E.1 — точно по таблице адресов задания. E.2 и E.3 — те же 16 пунктов на других схемах: роли и адреса выводятся
   из связей по правилам задания (R1 + VPC1 слева, R7 + VPC2 справа, перед R7 — граничный маршрутизатор с DHCP и NAT,
   остальные — WAN на OSPF 250, NTP-сервер за одним из маршрутизаторов WAN). */
(function (G) {
  'use strict';
  var EL = G.EL, R = EL.rnd;

  // топологии из Final Exam N.unl: [устройство, порт, устройство, порт]; координаты — с холста pnetlab (масштаб под эмулятор)
  var TOPO = {
    1: { pos: { R1: [207, 312], R2: [426, 312], R3: [657, 213], R4: [672, 414], R5: [912, 303], R6: [1065, 303], R7: [1245, 303], VPC1: [51, 318], VPC2: [1416, 309], NTP: [840, 432] },
         links: [['R1', 1, 'R2', 3], ['R1', 3, 'VPC1'], ['R2', 1, 'R3', 3], ['R2', 2, 'R4', 3], ['R3', 1, 'R5', 1], ['R4', 1, 'R5', 2], ['R4', 2, 'NTP'],
                 ['R5', 3, 'R6', 1], ['R6', 3, 'R7', 1], ['R7', 2, 'VPC2']] },
    2: { pos: { R1: [291, 237], R2: [468, 237], R3: [636, 234], R4: [792, 105], R5: [795, 312], R6: [978, 228], R7: [1170, 225], NTP: [597, 93], VPC1: [126, 243], VPC2: [1362, 231] },
         links: [['R1', 1, 'R2', 3], ['R1', 3, 'VPC1'], ['R2', 1, 'R3', 3], ['R3', 1, 'R4', 3], ['R3', 2, 'R5', 3], ['R4', 1, 'R6', 1], ['R4', 2, 'NTP'],
                 ['R5', 1, 'R6', 2], ['R6', 3, 'R7', 1], ['R7', 3, 'VPC2']] },
    3: { pos: { R1: [237, 255], R2: [390, 129], R3: [387, 354], R4: [591, 249], R5: [792, 369], R6: [792, 117], R7: [975, 243], VPC1: [36, 261], VPC2: [1158, 249], NTP: [738, 249] },
         links: [['R1', 1, 'R2', 3], ['R1', 3, 'VPC1'], ['R2', 1, 'R4', 3], ['R2', 2, 'R3', 1], ['R2', 4, 'R6', 1], ['R3', 2, 'R4', 2], ['R3', 3, 'R5', 1],
                 ['R4', 4, 'NTP'], ['R5', 2, 'R6', 2], ['R5', 3, 'R7', 1], ['R7', 3, 'VPC2']] }
  };
  // адреса Варианта 1 (таблица задания) для E.1: «R2:3» → адрес
  var V1 = { 'R1:1': '192.168.100.2/30', 'R2:1': '172.16.10.9/30', 'R2:2': '172.16.10.2/30', 'R2:3': '192.168.100.1/30', 'R3:1': '172.16.10.21/30',
             'R3:3': '172.16.10.10/30', 'R4:1': '172.16.10.33/30', 'R4:2': '10.10.100.2/24', 'R4:3': '172.16.10.1/30', 'R5:1': '172.16.10.22/30',
             'R5:2': '172.16.10.34/30', 'R5:3': '10.10.50.1/30', 'R6:1': '10.10.50.2/30', 'R6:3': '10.10.200.1/30', 'R7:1': '10.10.200.2/30', 'R7:2': '192.168.200.1/24' };
  var RS = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7'];

  // план: роли, адреса, OSPF, маршруты — из связей
  function plan(k) {
    var T = TOPO[k], ip = {}, nb = {}, lan7 = null, srv = null;
    RS.forEach(function (r) { nb[r] = []; });
    T.links.forEach(function (l) { if (l[3] !== undefined) { nb[l[0]].push([l[1], l[2], l[3]]); nb[l[2]].push([l[3], l[0], l[1]]); } });
    var r7up = nb.R7[0], B = r7up[1];                           // граничный маршрутизатор перед R7
    var wan = RS.filter(function (r) { return r !== 'R1' && r !== 'R7' && r !== B; });
    T.links.forEach(function (l) { if (l[2] === 'NTP') srv = [l[0], l[1]]; if (l[0] === 'R7' && l[2] === 'VPC2') lan7 = l[1]; });
    var r1up = nb.R1[0];
    if (k === 1) Object.keys(V1).forEach(function (x) { ip[x] = V1[x]; });
    else {
      ip['R1:' + r1up[0]] = '192.168.100.2/30'; ip[r1up[1] + ':' + r1up[2]] = '192.168.100.1/30';
      ip['R7:' + r7up[0]] = '10.10.200.2/30'; ip[B + ':' + r7up[2]] = '10.10.200.1/30';
      ip['R7:' + lan7] = '192.168.200.1/24'; ip[srv[0] + ':' + srv[1]] = '10.10.100.2/24';
      var t = 0, b = 0;
      T.links.forEach(function (l) {
        if (l[3] === undefined || l[0] === 'R1' || l[0] === 'R7' || l[2] === 'R7') return;
        var bLink = l[0] === B || l[2] === B, w = bLink ? (l[0] === B ? [l[2], l[3], l[0], l[1]] : l) : l;
        var base = bLink ? '10.10.50.' + (4 * b++) : '172.16.10.' + (4 * t++), o = +base.split('.')[3];
        ip[w[0] + ':' + w[1]] = base.replace(/\d+$/, o + 1) + '/30'; ip[w[2] + ':' + w[3]] = base.replace(/\d+$/, o + 2) + '/30';
      });
    }
    var bUp = nb[B].filter(function (x) { return x[1] !== 'R7'; })[0];      // выход B в WAN (маршрут по умолчанию, NAT)
    var adjB = nb[B].filter(function (x) { return x[1] !== 'R7'; }).map(function (x) { return [x[1], ip[B + ':' + x[0]].split('/')[0]]; });
    var passive = {};                                                         // в WAN пассивные: к R1, к серверу, к B
    wan.forEach(function (r) { passive[r] = nb[r].filter(function (x) { return x[1] === 'R1' || x[1] === B; }).map(function (x) { return x[0]; });
      if (srv[0] === r) passive[r].push(srv[1]); });
    return { ip: ip, B: B, wan: wan, srv: srv, lan7: lan7, r7up: r7up, bUp: bUp, adjB: adjB, passive: passive, nb: nb,
             r1gw: ip[r1up[1] + ':' + r1up[2]].split('/')[0], srvGw: ip[srv[0] + ':' + srv[1]].split('/')[0],
             bGw: ip[bUp[1] + ':' + bUp[2]].split('/')[0] };
  }
  function ifacesOf(P, r) { return Object.keys(P.ip).filter(function (x) { return x.split(':')[0] === r; }).map(function (x) { return [+x.split(':')[1], P.ip[x]]; })
    .sort(function (a, b) { return a[0] - b[0]; }); }

  function dev(n, name) { var d = n.byName(name); return d ? d.st : null; }
  function run(n, name) { return dev(n, name).run; }
  function name(p, r) { return 'student-' + p.x + '-' + r; }

  function makeExam(k) {
    return {
      id: 'E.' + k, title: 'Экзамен NTF-2, Вариант 1 — топология ' + k + (k === 1 ? ' (как в задании)' : ''),
      goal: (k === 1 ? 'Итоговое практическое задание курса NTF-2, Вариант 1: схема и таблица адресов — из задания.'
                     : 'Задание Варианта 1 на топологии Final Exam ' + k + ' из пакета Eltex. Адреса выведены по правилам задания: 192.168.100.0/30 — R1 к WAN, 172.16.10.x/30 — каналы WAN, ' +
                       '10.10.50.x/30 — к граничному ' + plan(k).B + ', 10.10.200.0/30 — ' + plan(k).B + '–R7, 10.10.100.0/24 — NTP-сервер.') +
            ' X — ваш номер слушателя. Не забудьте ip firewall disable на интерфейсах.',
      gen: function () { var x = ('0' + R(1, 30)).slice(-2); return { x: x }; },
      build: function (net) {
        var T = TOPO[k], o = {};
        var xs = Object.keys(T.pos).map(function (n) { return T.pos[n][0]; }), ys = Object.keys(T.pos).map(function (n) { return T.pos[n][1]; });
        var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
        Object.keys(T.pos).forEach(function (n) { var p = T.pos[n], x = 70 + (p[0] - x0) / (x1 - x0) * 860, y = 110 + (p[1] - y0) / (y1 - y0) * 400;
          o[n] = net.add(n === 'NTP' ? 'Debian-server' : n.indexOf('VPC') === 0 ? 'VPC' : 'vESR', n, x, y); });
        o.NTP.st.tz = 7;
        T.links.forEach(function (l) { net.connect(o[l[0]].id, 'gi1/0/' + l[1], o[l[2]].id, l[3] === undefined ? (l[2] === 'NTP' ? 'ens3' : 'eth0') : 'gi1/0/' + l[3]); });
      },
      plan: function () { return plan(k); },
      tasks: function (p) { var P = plan(k), X = p.x, B = P.B;
        function ipOk(n, r) { var f = run(n, r).ifs; return ifacesOf(P, r).every(function (q) { var y = f['gi1/0/' + q[0]]; return y && y.ip === q[1] && !y.fw; }); }
        function ospfOk(n, r, i) { var c = run(n, r), o = c.ospf, id = r.slice(1) + '.' + r.slice(1) + '.' + r.slice(1) + '.' + r.slice(1);
          if (!o || o.id !== 250 || !o.on || o.rid !== id || !o.areas['0.0.0.0'] || !o.areas['0.0.0.0'].on) return false;
          return ifacesOf(P, r).every(function (q) { var x = c.ifs['gi1/0/' + q[0]].ospf; return x && x.on && x.inst === 250 && x.area === '0.0.0.0' &&
            !!x.passive === (P.passive[r].indexOf(q[0]) >= 0); }); }
        function snatOk(c, ifn, a, b) { var s = c.snat; if (!s) return false;
          return Object.keys(s.rulesets).some(function (k2) { var rs = s.rulesets[k2]; return rs.ifn === ifn && Object.keys(rs.rules).some(function (q) {
            var x = rs.rules[q]; return x.on && x.act === 'interface' && x.src && x.src[0] === a && x.src[1] === b; }); }); }
        function hasRoute(n, r, net, nh) { return run(n, r).routes.some(function (x) { return x.net === net && x.nh === nh; }); }
        var ntpR = RS.filter(function (r) { return r !== 'R7'; });
        return [
          { t: '1. Имена student-' + X + '-R1 … student-' + X + '-R7', ok: function (n) { return RS.every(function (r) { return run(n, r).host === name(p, r); }); } },
          { t: '2. IP-адреса по таблице на R1–R7, межсетевой экран отключён', ok: function (n) { return RS.every(function (r) { return ipOk(n, r); }); } },
          { t: '3. Пользователь student' + X + ' / studentpass' + X + ', privilege 14 на всех', ok: function (n) { return RS.every(function (r) {
              var u = run(n, r).users['student' + X]; return u && u.pw === 'studentpass' + X && u.priv === 14; }); } },
          { t: '4. R1: VLAN 100, gi1/0/3 — mode switchport, access VLAN 100', ok: function (n) { var c = run(n, 'R1'), x = c.ifs['gi1/0/3'];
              return (c.vlans || {})[100] && x.sw && x.sw.vlan === 100 && x.sw.mode === 'access'; } },
          { t: '5. R1: Bridge 100 — VLAN 100, 192.168.220.1/24, экран отключён, enable', ok: function (n) { var b = (run(n, 'R1').bridges || {})[100];
              return b && b.vlan === 100 && b.ip === '192.168.220.1/24' && !b.fw && b.on; } },
          { t: '6. R1: маршрут по умолчанию через ' + P.r1gw, ok: function (n) { return hasRoute(n, 'R1', '0.0.0.0/0', P.r1gw); } },
          { t: '7. Часовой пояс GMT +7 на всех', ok: function (n) { return RS.every(function (r) { return run(n, r).tz === '+7'; }); } },
          { t: '8. NTP на R1–R6: сервер 10.10.100.100, minpoll 5 (2⁵ = 32 с), синхронизация есть', ok: function (n) { return ntpR.every(function (r) {
              var c = run(n, r).ntp, s = c && c.servers['10.10.100.100']; if (!c || !c.on || !s || s.minpoll !== 5) return false;
              var pr = n.ntpPeer(n.byName(r).id); return pr && pr.utc !== null; }); } },
          { t: '9. R1: Source NAT на gi1/0/1 для 192.168.220.1–192.168.220.254', ok: function (n) { return snatOk(run(n, 'R1'), 'gi1/0/1', '192.168.220.1', '192.168.220.254'); } },
          { t: '10. OSPF 250, область 0.0.0.0 на ' + P.wan.join(', ') + ': Router ID N.N.N.N, все рабочие интерфейсы в процессе, пассивные — к R1, к ' + B + ' и к серверу',
            ok: function (n) { return P.wan.every(function (r) { return ospfOk(n, r); }); } },
          { t: '11. ' + P.adjB.map(function (a) { return a[0]; }).join(' и ') + ': маршрут 192.168.200.0/24 через ' + P.adjB.map(function (a) { return a[1]; }).join(' / '),
            ok: function (n) { return P.adjB.every(function (a) { return hasRoute(n, a[0], '192.168.200.0/24', a[1]); }); } },
          { t: '12. ' + B + ': DHCP-сервер, пул DHCP-C200 — 192.168.200.0/24, 192.168.200.10–40, аренда 15 минут (0:0:15), шлюз 192.168.200.1', ok: function (n) {
              var c = run(n, B), q = c.dhcp && c.dhcp.pools['DHCP-C200'];
              return c.dhcp && c.dhcp.on && q && q.net === '192.168.200.0/24' && q.range && q.range[0] === '192.168.200.10' && q.range[1] === '192.168.200.40' &&
                     q.lease === '0:0:15' && q.gw === '192.168.200.1'; } },
          { t: '13. ' + B + ': маршрут по умолчанию через ' + P.bGw + ' и 192.168.200.0/24 через 10.10.200.2', ok: function (n) {
              return hasRoute(n, B, '0.0.0.0/0', P.bGw) && hasRoute(n, B, '192.168.200.0/24', '10.10.200.2'); } },
          { t: '14. ' + B + ': Source NAT на gi1/0/' + P.bUp[0] + ' для 192.168.200.1–192.168.200.254', ok: function (n) {
              return snatOk(run(n, B), 'gi1/0/' + P.bUp[0], '192.168.200.1', '192.168.200.254'); } },
          { t: '15. R7: DHCP relay (helper 10.10.200.1 на gi1/0/' + P.lan7 + '), маршрут по умолчанию через 10.10.200.1', ok: function (n) { var c = run(n, 'R7');
              return c.relay && c.ifs['gi1/0/' + P.lan7].helper === '10.10.200.1' && hasRoute(n, 'R7', '0.0.0.0/0', '10.10.200.1'); } },
          { t: '16. VPC2 получил адрес по DHCP (192.168.200.10–40); VPC1 — 192.168.220.2/24', ok: function (n) { var v = dev(n, 'VPC2'), a = EL.ip.ip2n(v.ip || '0.0.0.0');
              return v.dhcp && a >= EL.ip.ip2n('192.168.200.10') && a <= EL.ip.ip2n('192.168.200.40') && dev(n, 'VPC1').ip === '192.168.220.2'; } },
          { t: 'Проверка: VPC1 и VPC2 пингуют NTP-сервер 10.10.100.100; всё применено (commit + confirm)', ok: function (n) {
              return n.reach('VPC1', '10.10.100.100') && n.reach('VPC2', '10.10.100.100') &&
                     RS.every(function (r) { var s = dev(n, r); return !s.pending && !s.unconfirmed; }); } }]; },
      sol: function (p) { var P = plan(k), X = p.x, B = P.B, o = {};
        RS.forEach(function (r) {
          var c = ['configure', 'hostname ' + name(p, r), 'username student' + X, 'password studentpass' + X, 'privilege 14', 'exit', 'clock timezone gmt +7'];
          ifacesOf(P, r).forEach(function (q) { c.push('interface gigabitethernet 1/0/' + q[0], 'ip address ' + q[1], 'ip firewall disable', 'exit'); });
          if (r === 'R1') c = c.concat(['vlan 100', 'exit', 'interface gigabitethernet 1/0/3', 'mode switchport', 'switchport mode access', 'switchport access vlan 100', 'exit',
            'bridge 100', 'vlan 100', 'ip firewall disable', 'ip address 192.168.220.1/24', 'enable', 'exit', 'ip route 0.0.0.0/0 ' + P.r1gw,
            'nat source', 'ruleset SNAT', 'to interface gigabitethernet 1/0/1', 'rule 10', 'match source-address address-range 192.168.220.1-192.168.220.254',
            'action source-nat interface', 'enable', 'exit', 'exit', 'exit']);
          if (P.wan.indexOf(r) >= 0) {
            var id = r.slice(1) + '.' + r.slice(1) + '.' + r.slice(1) + '.' + r.slice(1);
            c = c.concat(['router ospf 250', 'router-id ' + id, 'area 0.0.0.0', 'enable', 'exit', 'enable', 'exit']);
            ifacesOf(P, r).forEach(function (q) { c.push('interface gigabitethernet 1/0/' + q[0], 'ip ospf instance 250', 'ip ospf area 0.0.0.0', 'ip ospf');
              if (P.passive[r].indexOf(q[0]) >= 0) c.push('ip ospf passive-interface'); c.push('exit'); });
            P.adjB.forEach(function (a) { if (a[0] === r) c.push('ip route 192.168.200.0/24 ' + a[1]); });
          }
          if (r === B) c = c.concat(['ip dhcp-server', 'ip dhcp-server pool DHCP-C200', 'network 192.168.200.0/24', 'address-range 192.168.200.10-192.168.200.40',
            'default-lease-time 0:0:15', 'default-router 192.168.200.1', 'exit', 'ip route 0.0.0.0/0 ' + P.bGw, 'ip route 192.168.200.0/24 10.10.200.2',
            'nat source', 'ruleset SNAT', 'to interface gigabitethernet 1/0/' + P.bUp[0], 'rule 10', 'match source-address address-range 192.168.200.1-192.168.200.254',
            'action source-nat interface', 'enable', 'exit', 'exit', 'exit']);
          if (r === 'R7') c = c.concat(['ip dhcp-relay', 'interface gigabitethernet 1/0/' + P.lan7, 'ip helper-address 10.10.200.1', 'exit', 'ip route 0.0.0.0/0 10.10.200.1']);
          if (r !== 'R7') c = c.concat(['ntp enable', 'ntp server 10.10.100.100', 'minpoll 5', 'exit']);
          o[r] = c.concat(['do commit', 'do confirm', 'end']);
        });
        o.NTP = ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.10.100.100/24 dev ens3', 'ip route add default via ' + P.srvGw];
        o.VPC1 = ['ip 192.168.220.2/24 192.168.220.1', 'ping 10.10.100.100'];
        o.VPC2 = ['ip dhcp', 'ping 10.10.100.100'];
        return o; }
    };
  }
  var all = EL.labs.LABS, at = all.map(function (l) { return l.id; }).indexOf('T.1');
  Array.prototype.splice.apply(all, [at < 0 ? all.length : at, 0].concat([makeExam(1), makeExam(2), makeExam(3)]));
})(typeof window !== 'undefined' ? window : global);
