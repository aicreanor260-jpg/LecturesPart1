/* Автопрогон: для каждой лабы и каждого случайного задания генерирует N вариантов, вводит решение в CLI и проверяет.
   Запуск: node decks/_elab/test.js [N]  (по умолчанию 12) */
'use strict';
var fs = require('fs'), path = require('path'), vm = require('vm');
var D = __dirname, N = +process.argv[2] || 12;
global.window = global;
['../_dk_cli.js', 'common.js', 'esr.js', 'esr_svc.js', 'esr_more.js', 'esr_ops.js', 'mesx.js', 'mes_l2.js', 'mes_dialects.js', 'hosts.js', 'catalog.js', 'net.js', 'tables.js', 'aging.js', 'mes_full.js', 'esr_fw.js', 'rt_timers.js', 'console.js', 'frames.js', 'ipv6.js', 'ipv6_rt.js', 'dns.js', 'tunnel.js', 'labs.js', 'labs_routing.js', 'labs_services.js', 'labs_l2.js', 'labs_ops.js', 'labs_exam.js'].forEach(function (f) {
  vm.runInThisContext(fs.readFileSync(path.join(D, f), 'utf8'), { filename: f });
});
var EL = global.EL, fail = 0, total = 0;

function runLab(L) {
  for (var i = 0; i < N; i++) {
    total++;
    var net = new EL.Net(), p = L.gen(); L.build(net, p);
    var tasks = L.tasks(p);
    if (L.id.charAt(0) === 'T') {                 // поиск неисправности: до исправления ping не должен проходить
      if (tasks[0].ok(net)) { fail++; console.error('✗ ' + L.id + ' неисправность ' + p.fault + ' не ломает сеть'); continue; }
    }
    var errs = EL.labs.apply(net, L.sol(p));
    net.tick(60);                                 // протоколам нужно время: OSPF ждёт выбора DR (wait timer 40 с)
    var bad = tasks.filter(function (t) { return !t.ok(net); });
    if (errs.length || bad.length) {
      fail++;
      console.error('✗ ' + L.id + ' вариант ' + JSON.stringify(p));
      errs.forEach(function (e) { console.error('   CLI: ' + e); });
      bad.forEach(function (t) { console.error('   не засчитано: ' + t.t); });
    }
  }
  console.log((fail ? '' : '✓ ') + L.id + ' — ' + L.title);
}
EL.labs.LABS.forEach(runLab);

// случайные задания движка: решение на одном коммутаторе MES
['base', 'vlan'].forEach(function (kind) {
  EL.E.TASKS[kind].forEach(function (T, k) {
    for (var i = 0; i < N; i++) {
      total++;
      var net = new EL.Net(), d = net.add('MES2428', 'SW1'), P = T.gen();
      d.st.mode = 'priv'; if (T.setup) T.setup(P, d.st);
      T.text(P);
      var errs = [];
      T.sol(P).forEach(function (l) { var r = net.exec(d.id, l); if (/^%/.test(r)) errs.push(l + ' → ' + r); });
      var bad = T.checks(P).filter(function (c) { return !c[1](d.st); });
      if (errs.length || bad.length) { fail++; console.error('✗ ' + kind + '#' + k, errs, bad.map(function (c) { return c[0]; })); }
    }
  });
  console.log('✓ задания ' + kind + ': ' + EL.E.TASKS[kind].length + ' шаблонов');
});

// проверки поведения: подсказки, неполная команда, ошибки режима
(function () {
  var net = new EL.Net(), s = net.add('MES2428', 'SW1'), r = net.add('vESR', 'R1');
  var exp = [
    [s.id, 'conf t', '% Команда недоступна в этом режиме — проверьте приглашение'],
    [s.id, 'enable', ''], [s.id, 'show', '% Incomplete command'], [s.id, 'blah', '% Unrecognized command'],
    [r.id, 'configure', ''], [r.id, 'interface gigabitethernet 1/0/9', '% Interface gi1/0/9 not found']];
  exp.forEach(function (e) { total++; var got = net.exec(e[0], e[1]); if (got !== e[2]) { fail++; console.error('✗ «' + e[1] + '» → «' + got + '», ожидалось «' + e[2] + '»'); } });
  total++; if (net.tab(s.id, 'conf') !== 'configure ') { fail++; console.error('✗ Tab: ' + net.tab(s.id, 'conf')); }
  total++; if (!/running-config/.test(net.help(s.id, 'show '))) { fail++; console.error('✗ ? после show'); }
  total++; if (net.prompt(r.id) !== 'vesr(config)#') { fail++; console.error('✗ приглашение ESR ' + net.prompt(r.id)); }
  console.log('✓ поведение CLI');
})();

// диалекты веток ПО: одни и те же задачи на моделях 6.x (MES3348) и 8.x (MES5448) их собственным синтаксисом
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  function run(net, script) { var e = EL.labs.apply(net, script); return e; }
  var D = {
    '6': { model: 'MES3348', p: function (i) { return 'gi1/0/' + i; }, rng: function (a, b) { return 'interface range gigabitethernet 1/0/' + a + '-' + b; },
           one: function (i) { return 'interface gigabitethernet 1/0/' + i; }, vlans: ['configure', 'vlan database', 'vlan 10,20', 'exit'],
           lag: ['channel-group 1 mode auto'], lagPre: [], stp: ['spanning-tree mode rstp'], root: 'spanning-tree priority 4096',
           mon: function (src, dst) { return ['interface gigabitethernet 1/0/' + dst, 'port monitor gigabitethernet 1/0/' + src, 'exit']; } },
    '8': { model: 'MES5448', p: function (i) { return '1/0/' + i; }, rng: function (a, b) { return 'interface 1/0/' + a + '-1/0/' + b; },
           one: function (i) { return 'interface 1/0/' + i; }, vlans: ['vlan database', 'vlan 10,20', 'exit', 'configure'],
           lag: ['addport lag 1'], lagPre: ['port-channel uplink'], stp: ['spanning-tree', 'spanning-tree mode rstp'], root: 'spanning-tree mst priority 0 4096',
           mon: function (src, dst) { return ['monitor session 1 source interface 1/0/' + src, 'monitor session 1 destination interface 1/0/' + dst, 'monitor session 1 mode']; } }
  };
  Object.keys(D).forEach(function (k) {
    var d = D[k], tag = 'диалект ' + k + ' (' + d.model + ')';
    // VLAN + маршрутизация на SVI
    var n = new EL.Net(), s = n.add(d.model, 'SW1'); ['A', 'B', 'C'].forEach(function (x, i) { var v = n.add('VPC', x); n.connect(v.id, 'eth0', s.id, d.p(i + 1)); });
    var e = run(n, { SW1: ['enable'].concat(d.vlans, [d.rng(1, 2), 'switchport mode access', 'switchport access vlan 10', 'exit',
                       d.one(3), 'switchport mode access', 'switchport access vlan 20', 'exit',
                       'interface vlan 10', 'ip address 10.0.10.1 255.255.255.0', 'exit', 'interface vlan 20', 'ip address 10.0.20.1 255.255.255.0', 'end']),
                     A: ['ip 10.0.10.2/24 10.0.10.1'], B: ['ip 10.0.10.3/24 10.0.10.1'], C: ['ip 10.0.20.2/24 10.0.20.1'] });
    chk(tag + ': VLAN и SVI', !e.length && n.reach('A', '10.0.10.3') && n.reach('A', '10.0.20.2'), e.join('; '));
    var sv = n.exec(s.id, 'show vlan');
    chk(tag + ': show vlan', k === '8' ? /VLAN ID[\s\S]*\n10\s/.test(sv) : sv.indexOf(d.p(1).replace(/\d+$/, '')) >= 0, sv.split('\n')[0]);
    // LACP между двумя коммутаторами
    var m = new EL.Net(), a = m.add(d.model, 'S1'), b = m.add(d.model, 'S2'), va = m.add('VPC', 'A'), vb = m.add('VPC', 'B');
    for (var i = 1; i <= 4; i++) m.connect(a.id, d.p(i), b.id, d.p(i));
    m.connect(va.id, 'eth0', a.id, d.p(10)); m.connect(vb.id, 'eth0', b.id, d.p(10));
    var lag = ['enable', 'configure'].concat(d.lagPre, [d.rng(1, 4)], d.lag, ['end']);
    e = run(m, { S1: lag, S2: lag, A: ['ip 10.1.1.1/24'], B: ['ip 10.1.1.2/24'] });
    var L = m.lports(a.id).filter(function (l) { return l.name === 'po1'; })[0];
    chk(tag + ': LACP', !e.length && L && L.members.length === 4 && m.reach('A', '10.1.1.2'), e.join('; '));
    // кольцо из трёх с RSTP
    var r = new EL.Net(), x = ['X1', 'X2', 'X3'].map(function (nm) { return r.add(d.model, nm); }), ra = r.add('VPC', 'A'), rb = r.add('VPC', 'B');
    r.connect(x[0].id, d.p(1), x[1].id, d.p(2)); r.connect(x[1].id, d.p(1), x[2].id, d.p(2)); r.connect(x[2].id, d.p(1), x[0].id, d.p(2));
    r.connect(ra.id, 'eth0', x[0].id, d.p(5)); r.connect(rb.id, 'eth0', x[2].id, d.p(5));
    var sc = { A: ['ip 10.2.2.1/24'], B: ['ip 10.2.2.2/24'] };
    ['X1', 'X2', 'X3'].forEach(function (nm, i) { sc[nm] = ['enable', 'configure'].concat(d.stp, i === 1 ? [d.root] : [], ['end']); });
    e = run(r, sc); var t = r.stp(), blk = 0; Object.keys(t).forEach(function (id) { Object.keys(t[id]).forEach(function (q) { if (!t[id][q].fwd) blk++; }); });
    chk(tag + ': RSTP', !e.length && blk === 1 && r._stp.root[x[1].id] === x[1].id && r.reach('A', '10.2.2.2'), e.join('; ') + ' blk=' + blk);
    // зеркалирование
    var w = new EL.Net(), sw = w.add(d.model, 'M'), p1 = w.add('VPC', 'A'), p2 = w.add('VPC', 'B'), sn = w.add('Debian', 'S');
    w.connect(p1.id, 'eth0', sw.id, d.p(1)); w.connect(p2.id, 'eth0', sw.id, d.p(2)); w.connect(sn.id, 'ens3', sw.id, d.p(12));
    e = run(w, { M: ['enable', 'configure'].concat(d.mon(1, 12), ['end']), A: ['ip 10.3.3.1/24'], B: ['ip 10.3.3.2/24', 'ping 10.3.3.1'] });
    chk(tag + ': зеркалирование', !e.length && (sn.st.capN || 0) >= 2, e.join('; '));
  });
  var n8 = new EL.Net(), f = n8.add('MES5448', 'F'); n8.exec(f.id, 'enable'); n8.exec(f.id, 'configure'); n8.exec(f.id, 'interface 1/0/3');
  chk('приглашение FASTPATH', n8.prompt(f.id) === '(switch) (Interface 1/0/3)#', n8.prompt(f.id));
  var n6 = new EL.Net(), g = n6.add('MES3348', 'G'); n6.exec(g.id, 'enable'); n6.exec(g.id, 'configure');
  chk('6.x: режим rst не из своей ветки', /Режим/.test(n6.exec(g.id, 'spanning-tree mode rst')));
  console.log('✓ диалекты 6.x и 8.x');
})();

// таблицы: ARP у обеих сторон, MAC-обучение коммутатора, кэш ARP, устаревание записи, разные VLAN
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), s = n.add('MES2428', 'SW1'), v = ['VPC1', 'VPC2', 'VPC3'].map(function (x) { return n.add('VPC', x); });
  v.forEach(function (d, i) { n.connect(d.id, 'eth0', s.id, 'gi1/0/' + (i + 1)); });
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'vlan database', 'vlan 10,20', 'exit', 'interface range gi1/0/1-2', 'switchport access vlan 10', 'exit',
                           'interface gi1/0/3', 'switchport access vlan 20', 'end'],
                     VPC1: ['ip 10.0.0.1/24'], VPC2: ['ip 10.0.0.2/24'], VPC3: ['ip 10.0.0.3/24'] });
  var m1 = EL.mac('VPC1eth0'), m2 = EL.mac('VPC2eth0'), m3 = EL.mac('VPC3eth0');
  var r = n.ping(v[0].id, '10.0.0.2');
  chk('таблицы: ping в одной VLAN', r.ok && r.steps.some(function (x) { return x.k === 'arp'; }));
  chk('таблицы: ARP у спросившего и у ответившего', (n.arp[v[0].id]['10.0.0.2'] || {}).mac === m2 && (n.arp[v[1].id]['10.0.0.1'] || {}).mac === m1);
  var mt = n.macRows(s.id);
  chk('таблицы: коммутатор выучил оба MAC в VLAN 10 на своих портах', mt.some(function (x) { return x.mac === m1 && x.port === 'gi1/0/1' && x.vlan === 10; }) &&
      mt.some(function (x) { return x.mac === m2 && x.port === 'gi1/0/2' && x.vlan === 10; }), JSON.stringify(mt));
  r.steps.flush();
  var sa = r.steps.filter(function (x) { return x.k === 'arp'; })[0], sr = r.steps.filter(function (x) { return x.k === 'arpr'; })[0];
  function has(st, key) { return (st.tab || []).some(function (c) { return c.k === key && c.n; }); }
  chk('таблицы по шагам: ARP-запрос — коммутатор выучил MAC VPC1', has(sa, 'm|' + s.id + '|10|' + m1));
  chk('таблицы по шагам: ARP-ответ — записи ARP у обеих сторон', has(sr, 'a|' + v[0].id + '|10.0.0.2') && has(sr, 'a|' + v[1].id + '|10.0.0.1'));
  var r2 = n.ping(v[0].id, '10.0.0.2');
  chk('таблицы по шагам: повторный ping ничего нового не пишет в ARP', !r2.steps.some(function (x) { return (x.tab || []).some(function (c) { return c.k[0] === 'a'; }); }));
  chk('таблицы: повторный ping без ARP-запроса', r2.ok && !r2.steps.some(function (x) { return x.k === 'arp'; }));
  var r3 = n.ping(v[0].id, '10.0.0.3');
  chk('таблицы: разные VLAN — не доходит', !r3.ok && r3.why === 'Host unreachable' && !n.macRows(s.id).some(function (x) { return x.mac === m3; }));
  EL.labs.apply(n, { SW1: ['configure', 'interface gi1/0/2', 'switchport access vlan 20', 'end'] });
  var r4 = n.ping(v[0].id, '10.0.0.2'), r5 = n.ping(v[0].id, '10.0.0.2');
  chk('таблицы: устаревшая ARP-запись после смены VLAN', !r4.ok && !n.arp[v[0].id]['10.0.0.2'] && !r5.ok && r5.why === 'Host unreachable');
  chk('таблицы: show mac address-table / show arp', /Learnt/.test(n.exec(s.id, 'show mac address-table')) && /10\.0\.0\.1/.test(n.exec(v[1].id, 'arp')));
  console.log('✓ таблицы ARP и MAC');
})();

// старение: MAC 300 с, ARP по типу устройства, настройка таймеров, промотка времени
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), s = n.add('MES2428', 'SW1'), a = n.add('VPC', 'A'), b = n.add('Debian', 'B');
  n.connect(a.id, 'eth0', s.id, 'gi1/0/1'); n.connect(b.id, 'ens3', s.id, 'gi1/0/2');
  EL.labs.apply(n, { A: ['ip 10.0.0.1/24'], B: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.2/24 dev ens3'] });
  var r = n.ping(a.id, '10.0.0.2');
  chk('старение: исходный ping', r.ok, r.why);
  chk('старение: VPC показывает остаток 120 с', /expires in 120 seconds/.test(n.exec(a.id, 'arp')), n.exec(a.id, 'arp'));
  n.tick(40);
  chk('старение: Debian через 40 с — STALE', /STALE/.test(n.exec(b.id, 'ip neigh')), n.exec(b.id, 'ip neigh'));
  n.tick(30);
  chk('старение: Debian удалил запись через 60 с', !Object.keys(n.arp[b.id]).length);
  chk('старение: VPC через 70 с ещё помнит (50 с)', /expires in 50 seconds/.test(n.exec(a.id, 'arp')), n.exec(a.id, 'arp'));
  n.tick(60);
  chk('старение: VPC забыл через 120 с', !Object.keys(n.arp[a.id]).length);
  chk('старение: MAC-записи живы до 300 с', n.macRows(s.id).length === 2);
  var g = n.tick(200);
  chk('старение: MAC-записи удалены после 300 с', !n.macRows(s.id).length && g.filter(function (x) { return x.kind === 'MAC'; }).length === 2, JSON.stringify(g));
  var r2 = n.ping(a.id, '10.0.0.2');
  chk('старение: после старения снова ARP-запрос', r2.ok && r2.steps.some(function (x) { return x.k === 'arp'; }));
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'mac-address-table aging-time 20', 'end'] });
  n.tick(21);
  chk('старение: aging-time 20 на 10.x', !n.macRows(s.id).length && /mac-address-table aging-time 20/.test(n.exec(s.id, 'show running-config')));
  chk('старение: диапазон aging-time', /10\.\.400/.test(n.exec(s.id, 'configure') + n.exec(s.id, 'mac-address-table aging-time 5')));
  var n6 = new EL.Net(), x6 = n6.add('MES3348', 'G'); EL.labs.apply(n6, { G: ['enable', 'configure', 'mac address-table aging-time 100', 'arp timeout 500', 'end'] });
  chk('старение: 6.x mac address-table aging-time / arp timeout', x6.st.macAge === 100 && x6.st.arpTo === 500 && n6.arpAge(x6.id) === 500);
  var n8 = new EL.Net(), x8 = n8.add('MES5448', 'F'); EL.labs.apply(n8, { F: ['enable', 'configure', 'bridge aging-time 1000', 'end'] });
  chk('старение: 8.x bridge aging-time, ARP по умолчанию 1200', x8.st.macAge === 1000 && n8.arpAge(x8.id) === 1200 && /1000/.test(n8.exec(x8.id, 'show forwardingdb agetime')));
  var ne = new EL.Net(), e = ne.add('vESR', 'R'); EL.labs.apply(ne, { R: ['configure', 'interface gi1/0/1', 'ip arp reachable-time 6000', 'do commit', 'do confirm', 'end'] });
  chk('старение: ESR ip arp reachable-time', ne.arpAge(e.id, 'gi1/0/1') === 6 && ne.arpAge(e.id, 'gi1/0/2') === 160, ne.arpAge(e.id, 'gi1/0/1') + '/' + e.st.mode);
  console.log('✓ старение MAC и ARP');
})();

// расширенный CLI MES: сокращения, port security, BPDU guard, статические MAC, show-команды
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  function x(n, d, lines) { return lines.map(function (l) { return n.exec(d.id, l); }); }
  // сокращения как на железе
  var n = new EL.Net(), s = n.add('MES2428', 'SW1');
  var o = x(n, s, ['en', 'conf t', 'int gi 1/0/1', 'desc UPLINK', 'sw mode trunk', 'end', 'sh ru', 'sh int desc', 'sh run int gi1/0/1']);
  chk('CLI: int gi 1/0/1, sw mode trunk, sh ru', s.st.ports['gi1/0/1'].mode === 'trunk' && /switchport mode trunk/.test(o[6]) && /description UPLINK/.test(o[6]), o[6]);
  chk('CLI: sh int desc / sh run int', /UPLINK/.test(o[7]) && /^interface gigabitethernet1\/0\/1/.test(o[8]) && /description UPLINK/.test(o[8]), o[8]);
  chk('CLI: sh ver / sh clock', /10\.4\.6/.test(n.exec(s.id, 'sh ver')) && /UTC/.test(n.exec(s.id, 'sh clock')));
  x(n, s, ['clock set 10:20:30 5 Mar 2026']);
  chk('CLI: clock set', /^10:20:3\d UTC Thu Mar 5 2026/.test(n.exec(s.id, 'show clock')), n.exec(s.id, 'show clock'));
  // port security 10.x: на порту разрешён один MAC — второй ПК через хаб не проходит
  var w = new EL.Net(), sw = w.add('MES2428', 'SW'), a = w.add('VPC', 'A'), b = w.add('VPC', 'B'), c = w.add('VPC', 'C');
  w.connect(a.id, 'eth0', sw.id, 'gi1/0/1'); w.connect(b.id, 'eth0', sw.id, 'gi1/0/2'); w.connect(c.id, 'eth0', sw.id, 'gi1/0/3');
  EL.labs.apply(w, { A: ['ip 10.0.0.1/24'], B: ['ip 10.0.0.2/24'], C: ['ip 10.0.0.3/24'],
    SW: ['en', 'conf', 'int gi1/0/2', 'switchport port-security mode max-addresses', 'switchport port-security mac-limit 1', 'switchport port-security enable', 'end'] });
  chk('port security: первый MAC на порту разрешён', w.ping(a.id, '10.0.0.2').ok);
  w.disconnect(1); w.disconnect(1); w.connect(c.id, 'eth0', sw.id, 'gi1/0/2');   // на gi1/0/2 теперь другой ПК
  var r = w.ping(a.id, '10.0.0.3');
  chk('port security: чужой MAC отброшен', !r.ok && r.steps.some(function (st) { return /port security/.test(st.t); }), r.why);
  chk('port security: show port-security и show run', /gi1\/0\/2\s+Enabled\s+max-addresses\s+1/.test(w.exec(sw.id, 'show port-security')) &&
      /switchport port-security enable/.test(w.exec(sw.id, 'show running-config')));
  chk('port security: secure-запись не стареет', (w.tick(1000), w.macRows(sw.id).some(function (e) { return e.sec; })));
  // 6.x: discard-shutdown выключает порт
  var w6 = new EL.Net(), s6 = w6.add('MES3348', 'S'), p1 = w6.add('VPC', 'P1'), p2 = w6.add('VPC', 'P2');
  w6.connect(p1.id, 'eth0', s6.id, s6.st.ports['gi1/0/1'] ? 'gi1/0/1' : Object.keys(s6.st.ports)[0]);
  var k2 = Object.keys(s6.st.ports)[1]; w6.connect(p2.id, 'eth0', s6.id, k2);
  EL.labs.apply(w6, { P1: ['ip 10.1.1.1/24'], P2: ['ip 10.1.1.2/24'], S: ['en', 'conf', 'int ' + k2, 'port security', 'port security discard-shutdown', 'end'] });
  var r6 = w6.ping(p1.id, '10.1.1.2');
  chk('6.x port security lock + discard-shutdown', !r6.ok && s6.st.ports[k2].shut && s6.st.ports[k2].errdis === 'port-security', r6.why + ' ' + JSON.stringify(s6.st.ports[k2].psec));
  // BPDU guard: к порту с защитой подключили коммутатор — порт выключается
  var g = new EL.Net(), g1 = g.add('MES2428', 'G1'), g2 = g.add('MES2428', 'G2');
  EL.labs.apply(g, { G1: ['en', 'conf', 'int gi1/0/5', 'spanning-tree portfast', 'spanning-tree bpduguard enable', 'end'] });
  g.connect(g1.id, 'gi1/0/5', g2.id, 'gi1/0/5'); g.stp();
  chk('BPDU guard выключает порт', g1.st.ports['gi1/0/5'].shut && g1.st.ports['gi1/0/5'].errdis === 'bpduguard' && /bpduguard enable/.test(g.exec(g1.id, 'show running-config')));
  // статическая MAC-запись
  var m = new EL.Net(), sm = m.add('MES2428', 'M');
  var e = x(m, sm, ['en', 'conf', 'mac-address-table static unicast 00:11:22:33:44:55 vlan 1 interface gi 1/0/7 status permanent', 'end', 'show mac address-table']);
  chk('статический MAC (10.x)', /00:11:22:33:44:55\s+Static\s+gi1\/0\/7/.test(e[4]) && isFinite(m.ttl(sm.id, 'm', m.macRows(sm.id)[0])) === false, e[2] + e[4]);
  console.log('✓ расширенный CLI MES');
})();

// межсетевой экран ESR по зонам: object-group, stateful, неявный запрет, self, NAT с object-group
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), pc = n.add('VPC', 'PC1'), sv = n.add('Debian-server', 'Server');
  n.connect(pc.id, 'eth0', r.id, 'gi1/0/1'); n.connect(sv.id, 'ens3', r.id, 'gi1/0/2');
  EL.labs.apply(n, { PC1: ['ip 192.168.1.2/24 192.168.1.1'], Server: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.2/24 dev ens3', 'ip route add default via 10.0.0.1'],
    R1: ['configure', 'interface gi1/0/1', 'ip address 192.168.1.1/24', 'exit', 'interface gi1/0/2', 'ip address 10.0.0.1/24', 'exit', 'do commit', 'do confirm'] });
  var p0 = n.ping(pc.id, '10.0.0.2');
  chk('зоны: без зоны и без ip firewall disable — отброшено', !p0.ok && p0.steps.some(function (s) { return /не в зоне/.test(s.t); }));
  EL.labs.apply(n, { R1: ['configure', 'security zone trusted', 'exit', 'security zone untrusted', 'exit',
    'interface gi1/0/1', 'security-zone trusted', 'exit', 'interface gi1/0/2', 'security-zone untrusted', 'exit',
    'object-group network LAN', 'ip prefix 192.168.1.0/24', 'exit', 'object-group service WEB', 'port-range 80,443', 'exit',
    'security zone-pair trusted untrusted', 'rule 10', 'action permit', 'match protocol tcp', 'match source-address object-group LAN',
    'match destination-port object-group WEB', 'enable', 'exit', 'exit', 'do commit', 'do confirm', 'end'] });
  var h = n.request(pc.id, '10.0.0.2', 'tcp', 80);
  chk('зоны: HTTP из trusted в untrusted по object-group — проходит, ответ пропущен как сессия', h.ok && h.steps.some(function (s) { return /stateful/.test(s.t); }), h.why);
  var p1 = n.ping(pc.id, '10.0.0.2');
  chk('зоны: ICMP не разрешён — неявный запрет', !p1.ok && p1.steps.some(function (s) { return /неявный запрет/.test(s.t); }));
  var p2 = n.ping(sv.id, '192.168.1.2');
  chk('зоны: из untrusted в trusted пары нет — отброшено', !p2.ok && p2.steps.some(function (s) { return /нет security zone-pair untrusted trusted/.test(s.t); }));
  var p3 = n.ping(pc.id, '192.168.1.1');
  chk('зоны: на сам маршрутизатор без пары trusted self — отброшено', !p3.ok);
  EL.labs.apply(n, { R1: ['configure', 'security zone-pair trusted self', 'rule 1', 'action permit', 'match protocol icmp', 'enable', 'exit', 'exit',
    'security zone-pair trusted untrusted', 'rule 20', 'action permit', 'match protocol icmp', 'enable', 'exit', 'exit', 'do commit', 'do confirm', 'end'] });
  chk('зоны: trusted → self (icmp) разрешён', n.ping(pc.id, '192.168.1.1').ok);
  chk('зоны: правило icmp добавлено — ping проходит', n.ping(pc.id, '10.0.0.2').ok);
  chk('зоны: свой трафик маршрутизатора проходит, ответ — по сессии', /bytes from|!!!|ttl/i.test(n.exec(r.id, 'ping 10.0.0.2')) || n.ping(r.id, '10.0.0.2').ok);
  EL.labs.apply(n, { R1: ['configure', 'security zone-pair trusted untrusted', 'rule 5', 'action deny', 'match protocol icmp', 'match destination-address address-range 10.0.0.2', 'enable', 'exit', 'exit', 'do commit', 'do confirm', 'end'] });
  var p4 = n.ping(pc.id, '10.0.0.2');
  chk('зоны: deny с меньшим номером срабатывает раньше permit', !p4.ok && p4.steps.some(function (s) { return /rule 5 — deny/.test(s.t); }));
  var o = ['show security zone', 'show security zone-pair', 'show ip firewall sessions', 'show ip firewall counters', 'show object-group', 'show running-config'].map(function (c) { return n.exec(r.id, c); });
  chk('зоны: show security zone', /trusted\s+gi1\/0\/1/.test(o[0]) && /untrusted\s+gi1\/0\/2/.test(o[0]), o[0]);
  chk('зоны: show security zone-pair', /rule 10: permit, protocol tcp, source-address object-group LAN, destination-port object-group WEB/.test(o[1]), o[1]);
  chk('зоны: show ip firewall sessions / counters', /tcp\s+192\.168\.1\.2/.test(o[2]) && /trusted → untrusted\s+5\s+1/.test(o[3]), o[2] + '\n' + o[3]);
  chk('зоны: show object-group', /object-group network LAN\n  ip prefix 192\.168\.1\.0\/24/.test(o[4]) && /port-range 80,443/.test(o[4]), o[4]);
  chk('зоны: running-config', /security zone-pair trusted untrusted\n  rule 5\n    action deny/.test(o[5]) && /security-zone trusted/.test(o[5]), '');
  n.tick(61);
  chk('зоны: сессии стареют', /Активных сессий нет/.test(n.exec(r.id, 'show ip firewall sessions')));
  // NAT: match source-address object-group
  var m = new EL.Net(), r2 = m.add('vESR', 'R'), a = m.add('VPC', 'A'), b = m.add('VPC', 'B');
  m.connect(a.id, 'eth0', r2.id, 'gi1/0/1'); m.connect(b.id, 'eth0', r2.id, 'gi1/0/2');
  EL.labs.apply(m, { A: ['ip 192.168.1.2/24 192.168.1.1'], B: ['ip 200.0.0.2/24'],
    R: ['configure', 'interface gi1/0/1', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 200.0.0.1/24', 'ip firewall disable', 'exit',
        'object-group network LAN', 'ip prefix 192.168.1.0/24', 'exit',
        'nat source', 'ruleset INET', 'to interface gi1/0/2', 'rule 1', 'match source-address object-group LAN', 'action source-nat interface', 'enable', 'exit', 'exit', 'exit',
        'do commit', 'do confirm', 'end'] });
  var q = m.ping(a.id, '200.0.0.2');
  chk('NAT: match source-address object-group', q.ok && q.steps.some(function (s) { return /Source NAT/.test(s.t); }), q.why);
  console.log('✓ межсетевой экран ESR по зонам и object-group');
})();

// сессии межсетевого экрана по протоколам: состояния и таймауты как в справочнике ESR
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), pc = n.add('Debian', 'PC'), sv = n.add('Debian-server', 'Server');
  n.connect(pc.id, 'ens3', r.id, 'gi1/0/1'); n.connect(sv.id, 'ens3', r.id, 'gi1/0/2');
  EL.labs.apply(n, { PC: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 192.168.1.2/24 dev ens3', 'ip route add default via 192.168.1.1'],
    Server: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.2/24 dev ens3', 'ip route add default via 10.0.0.1'],
    R1: ['configure', 'security zone in', 'exit', 'security zone out', 'exit', 'interface gi1/0/1', 'ip address 192.168.1.1/24', 'security-zone in', 'exit',
         'interface gi1/0/2', 'ip address 10.0.0.1/24', 'security-zone out', 'exit', 'security zone-pair in out',
         'rule 1', 'action permit', 'match protocol icmp', 'enable', 'exit', 'rule 2', 'action permit', 'match protocol tcp', 'enable', 'exit',
         'rule 3', 'action permit', 'match protocol udp', 'enable', 'exit', 'exit', 'do commit', 'do confirm', 'end'] });
  function sess(proto, dport) { return (n.fwSess[r.id] || []).filter(function (x) { return x.proto === proto && (!dport || x.dport === dport); }).pop(); }
  chk('сессии: ICMP — состояние ICMP, таймаут 30 с', n.ping(pc.id, '10.0.0.2').ok && sess('icmp').state === 'ICMP' && /ICMP\s+30$/m.test(n.exec(r.id, 'show ip firewall sessions')),
      n.exec(r.id, 'show ip firewall sessions'));
  var h = n.request(pc.id, '10.0.0.2', 'tcp', 80);
  chk('сессии: HTTP — SYN_SENT → TIME_WAIT (соединение закрыто), 30 с', h.ok && sess('tcp', 80).state === 'TIME_WAIT' && h.steps.some(function (s) { return /SYN_SENT → TIME_WAIT/.test(s.t); }));
  chk('сессии: SSH — ESTABLISHED, 120 с', n.request(pc.id, '10.0.0.2', 'tcp', 22).ok && sess('tcp', 22).state === 'ESTABLISHED' && /ESTABLISHED\s+120$/m.test(n.exec(r.id, 'show ip firewall sessions')));
  var u = n.request(pc.id, '10.0.0.2', 'udp', 123);
  chk('сессии: UDP — UNREPLIED → ASSURED (180 с)', u.ok && sess('udp', 123).state === 'ASSURED');
  n.tick(31);
  chk('сессии: через 31 с ICMP и TIME_WAIT истекли, ESTABLISHED и ASSURED живы', !sess('icmp') && !sess('tcp', 80) && sess('tcp', 22) && sess('udp', 123));
  EL.labs.apply(n, { R1: ['configure', 'security zone-pair in out', 'no rule 3', 'exit', 'do commit', 'do confirm', 'end'] });
  var u2 = n.request(pc.id, '10.0.0.2', 'udp', 123);
  chk('сессии: правило UDP удалили, а поток идёт по живой сессии', u2.ok && u2.steps.some(function (s) { return /уже есть в таблице сессий/.test(s.t); }), u2.why);
  n.tick(181);
  var u3 = n.request(pc.id, '10.0.0.2', 'udp', 123);
  chk('сессии: сессия истекла — UDP упирается в неявный запрет', !u3.ok && u3.steps.some(function (s) { return /неявный запрет/.test(s.t); }));
  EL.labs.apply(n, { R1: ['configure', 'ip firewall sessions icmp-timeout 5', 'ip firewall sessions tcp-estabilished-timeout 600', 'do commit', 'do confirm', 'end'] });
  n.ping(pc.id, '10.0.0.2'); n.tick(6);
  chk('сессии: ip firewall sessions icmp-timeout 5', !sess('icmp') && /icmp-timeout\s+5\s+30/.test(n.exec(r.id, 'show ip firewall sessions timeouts')) &&
      /ip firewall sessions icmp-timeout 5/.test(n.exec(r.id, 'show running-config')));
  console.log('✓ сессии межсетевого экрана по протоколам');
})();

// RIP и OSPF по таймерам: ожидание DR, hello/dead, потеря соседа за коммутатором, invalid/flush
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  // R1 —gi1/0/1— SW —gi1/0/1— R2; у каждого LAN на gi1/0/2 с ПК
  function build(proto, extra) {
    var n = new EL.Net(), r1 = n.add('vESR', 'R1'), r2 = n.add('vESR', 'R2'), sw = n.add('MES2428', 'SW'), a = n.add('VPC', 'A'), b = n.add('VPC', 'B');
    n.connect(r1.id, 'gi1/0/1', sw.id, 'gi1/0/1'); n.connect(r2.id, 'gi1/0/1', sw.id, 'gi1/0/2');
    n.connect(a.id, 'eth0', r1.id, 'gi1/0/2'); n.connect(b.id, 'eth0', r2.id, 'gi1/0/2');
    function cfg(i) {
      var c = ['configure', 'interface gi1/0/1', 'ip address 10.0.0.' + i + '/24', 'ip firewall disable', 'exit',
               'interface gi1/0/2', 'ip address 192.168.' + i + '.1/24', 'ip firewall disable', 'exit'];
      if (proto === 'rip') c = c.concat(['router rip', 'network 10.0.0.0/24', 'network 192.168.' + i + '.0/24', 'enable', 'exit']);
      else c = c.concat(['router ospf 1', 'router-id ' + i + '.' + i + '.' + i + '.' + i, 'area 0.0.0.0', 'enable', 'exit', 'enable', 'exit',
                         'interface gi1/0/1-2', 'ip ospf instance 1', 'ip ospf area 0.0.0.0', 'ip ospf'].concat((extra || {})[i] || [], ['exit']));
      return c.concat(['do commit', 'do confirm', 'end']);
    }
    EL.labs.apply(n, { R1: cfg(1), R2: cfg(2), A: ['ip 192.168.1.2/24 192.168.1.1'], B: ['ip 192.168.2.2/24 192.168.2.1'] });
    return { n: n, r1: r1, r2: r2, a: a, b: b };
  }
  function has(n, id, p, net) { return (n.dyn()[id] || []).some(function (r) { return r.p === p && r.net === net; }); }
  // OSPF на broadcast-сегменте: 2way и ожидание DR 40 с, потом full
  var o = build('ospf'); o.n.dyn();
  o.n.tick(5);
  var t5 = o.n.exec(o.r1.id, 'show ip ospf neighbors');
  chk('OSPF: через 5 с — 2way, ждём выбора DR, маршрутов нет', /2way/.test(t5) && /ожидание выбора DR/.test(t5) && !has(o.n, o.r1.id, 'O', '192.168.2.0/24') && !o.n.ping(o.a.id, '192.168.2.2').ok, t5);
  o.n.tick(40);
  var t45 = o.n.exec(o.r1.id, 'show ip ospf neighbors');
  chk('OSPF: через 45 с — full/dr, маршрут O и связь есть', /full\/(dr|bdr)/.test(t45) && has(o.n, o.r1.id, 'O', '192.168.2.0/24') && o.n.ping(o.a.id, '192.168.2.2').ok, t45);
  chk('OSPF: show ip ospf interface — hello 10, dead 40, priority 128', /Hello timer:\s+10/.test(o.n.exec(o.r1.id, 'show ip ospf interface gi1/0/1')) &&
      /Dead timer:\s+40/.test(o.n.exec(o.r1.id, 'show ip ospf interface gi1/0/1')) && /Priority:\s+128/.test(o.n.exec(o.r1.id, 'show ip ospf interface gi1/0/1')));
  // сосед выключился за коммутатором — линк у R1 жив, ждём dead-interval
  o.n.power(o.r2.id, false); o.n.tick(15);
  var tl = o.n.exec(o.r1.id, 'show ip ospf neighbors');
  chk('OSPF: R2 выключен — 15 с сосед ещё full, маршрут висит (чёрная дыра)', /hello не приходят/.test(tl) && has(o.n, o.r1.id, 'O', '192.168.2.0/24'), tl);
  o.n.tick(26);
  chk('OSPF: после dead-interval 40 с сосед и маршрут удалены', !has(o.n, o.r1.id, 'O', '192.168.2.0/24') && /Соседей OSPF нет/.test(o.n.exec(o.r1.id, 'show ip ospf neighbors')));
  // point-to-point: без ожидания DR
  var p = build('ospf', { 1: ['ip ospf network point-to-point'], 2: ['ip ospf network point-to-point'] }); p.n.dyn(); p.n.tick(3);
  chk('OSPF point-to-point: full/ptp через 3 с', /full\/ptp/.test(p.n.exec(p.r1.id, 'show ip ospf neighbors')) && has(p.n, p.r1.id, 'O', '192.168.2.0/24'));
  // несовпадение hello
  var m = build('ospf', { 2: ['ip ospf hello-interval 5'] }); m.n.dyn(); m.n.tick(60);
  var tm = m.n.exec(m.r1.id, 'show ip ospf neighbors');
  chk('OSPF: hello 10/40 против 5/20 — соседства нет, причина видна', !has(m.n, m.r1.id, 'O', '192.168.2.0/24') && /таймеры hello\/dead 5\/20, а у нас 10\/40/.test(tm), tm);
  // RIP: маршруты сразу, сосед пропал — invalid 180, possibly down до flush 240
  var r = build('rip');
  chk('RIP: в первую секунду маршрута ещё нет — триггерное обновление идёт 1–5 с', !has(r.n, r.r1.id, 'R', '192.168.2.0/24'));
  r.n.tick(6);
  chk('RIP: через 6 с маршрут пришёл', has(r.n, r.r1.id, 'R', '192.168.2.0/24') && r.n.ping(r.a.id, '192.168.2.2').ok);
  r.n.power(r.r2.id, false); r.n.tick(100);
  var rl = r.n.exec(r.r1.id, 'show ip rip');
  chk('RIP: R2 выключен — 100 с маршрут ещё в таблице (invalid 180)', has(r.n, r.r1.id, 'R', '192.168.2.0/24') && /invalid через 80 с/.test(rl), rl);
  r.n.tick(90);
  var rp = r.n.exec(r.r1.id, 'show ip rip');
  chk('RIP: после invalid — possibly down (метрика 16), не используется', !has(r.n, r.r1.id, 'R', '192.168.2.0/24') && /\(120\/16\) possibly down — удаление через 50 с/.test(rp), rp);
  r.n.tick(60);
  chk('RIP: после flush 240 с — удалён', !/possibly down/.test(r.n.exec(r.r1.id, 'show ip rip')));
  // свой интерфейс выключили — маршруты через него уходят сразу
  var q = build('rip'); q.n.tick(6); EL.labs.apply(q.n, { R1: ['configure', 'interface gi1/0/1', 'shutdown', 'exit', 'do commit', 'do confirm', 'end'] });
  chk('RIP: свой интерфейс shutdown — маршрут удалён сразу', !has(q.n, q.r1.id, 'R', '192.168.2.0/24'));
  // timers invalid
  var v = build('rip'); EL.labs.apply(v.n, { R1: ['configure', 'router rip', 'timers invalid 60', 'exit', 'do commit', 'do confirm', 'end'] });
  v.n.tick(6); v.n.power(v.r2.id, false); v.n.tick(61);
  chk('RIP: timers invalid 60 — маршрут недействителен через 60 с', !has(v.n, v.r1.id, 'R', '192.168.2.0/24') && /timers invalid 60/.test(v.n.exec(v.r1.id, 'show running-config')));
  console.log('✓ RIP и OSPF по таймерам');
})();

// линейка ESR из каталога eltex.ru: порты по типам, имена te/twe/fo/hu, связь через 10G
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var esrs = Object.keys(EL.MODELS).filter(function (k) { return EL.MODELS[k].type === 'esr' && k !== 'vESR'; });
  chk('ESR: в каталоге больше 20 моделей', esrs.length > 20, esrs.length);
  esrs.forEach(function (k) { var n = new EL.Net(), d = n.add(k, 'R');
    chk('ESR ' + k + ': порты как в каталоге', Object.keys(d.st.run.ifs).length === EL.MODELS[k].ports && /esr# ?$/.test(n.prompt(d.id) + ' ')); });
  var n = new EL.Net(), a = n.add('ESR-1000', 'A'), b = n.add('ESR-30', 'B');
  chk('ESR-1000: 24 gi + 2 te', a.st.run.ifs['gi1/0/24'] && a.st.run.ifs['te1/0/2'] && !a.st.run.ifs['gi1/0/25']);
  n.connect(a.id, 'te1/0/1', b.id, 'te1/0/2');
  EL.labs.apply(n, { A: ['configure', 'interface tengigabitethernet 1/0/1', 'ip address 10.9.9.1/30', 'ip firewall disable', 'exit', 'do commit', 'do confirm', 'end'],
                     B: ['configure', 'interface te1/0/2', 'ip address 10.9.9.2/30', 'ip firewall disable', 'end', 'commit', 'confirm'] });
  chk('ESR: связь через te1/0/1 — te1/0/2', n.ping(a.id, '10.9.9.2').ok);
  n.exec(a.id, 'configure'); n.exec(a.id, 'interface te1/0/1');
  chk('ESR: приглашение (config-if-te)#', n.prompt(a.id) === 'esr(config-if-te)#', n.prompt(a.id));
  chk('ESR: show running-config — interface tengigabitethernet 1/0/1', /interface tengigabitethernet 1\/0\/1/.test(n.exec(a.id, 'do show running-config')));
  var c = new EL.Net(), x = c.add('ESR-3300', 'X'); c.exec(x.id, 'configure');
  chk('ESR-3300: twentyfivegigabitethernet и hundredgigabitethernet', !c.exec(x.id, 'interface twentyfivegigabitethernet 1/0/4') && c.prompt(x.id) === 'esr(config-if-twe)#' &&
      (c.exec(x.id, 'exit'), !c.exec(x.id, 'interface hundredgigabitethernet 1/0/1')) && c.prompt(x.id) === 'esr(config-if-hu)#', c.prompt(x.id));
  chk('ESR: диапазон и список interface gi1/0/1-2,te1/0/1', (n.exec(a.id, 'exit'), !n.exec(a.id, 'interface gi1/0/1-2,te1/0/1')) && Array.isArray(a.st.ctx) && a.st.ctx.length === 3);
  console.log('✓ линейка ESR (' + esrs.length + ' моделей)');
})();

// живая консоль: фильтры «|», постраничный вывод, системные сообщения, счётчики кадров
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), sw = n.add('MES2428', 'SW1'), r = n.add('vESR', 'R1'), pc = n.add('VPC', 'PC1');
  n.events();
  n.connect(sw.id, 'gi1/0/1', r.id, 'gi1/0/1'); n.connect(sw.id, 'gi1/0/2', pc.id, 'eth0');
  var ev = n.events();
  chk('событие: CFA-6 link status UP на MES 10', ev.some(function (e) { return e.id === sw.id && e.msg === 'CFA-6-Interface gi 1/0/1 link status UP'; }), JSON.stringify(ev));
  chk('событие: ESR тоже видит линк', ev.some(function (e) { return e.id === r.id && /Up:\s+gi1\/0\/1/.test(e.msg); }));
  sw.st.mode = 'priv';
  chk('show logging — запись в буфере', /link status UP/.test(n.exec(sw.id, 'show logging')));
  EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ip address 192.168.1.1/24', 'ip firewall disable', 'end', 'commit', 'confirm'],
                     PC1: ['ip 192.168.1.10/24 192.168.1.1'] });
  chk('ping через коммутатор', n.ping(pc.id, '192.168.1.1').ok);
  var c1 = n.ctrOf(sw.id, 'gi1/0/2'), c2 = n.ctrOf(sw.id, 'gi1/0/1');
  chk('счётчики: ARP-широковещание и unicast приняты на gi1/0/2', c1.ib >= 1 && c1.iu >= 1 && c1.io > 0, JSON.stringify(c1));
  chk('счётчики: отправлено на gi1/0/1', c2.ou >= 1 && c2.ob >= 1, JSON.stringify(c2));
  var cg = n.exec(sw.id, 'show interfaces counters gi1/0/2');
  chk('show interfaces counters gi1/0/2', /InUcastPkts/.test(cg) && /gi1\/0\/2\s+[1-9]/.test(cg) && /FCS Errors: 0/.test(cg), cg);
  chk('show interfaces gi1/0/1 — up', /is up \(connected\)[\s\S]*packets input/.test(n.exec(sw.id, 'show interfaces gigabitethernet 1/0/1')));
  n.exec(sw.id, 'clear counters gi1/0/2');
  chk('clear counters <if>', n.ctrOf(sw.id, 'gi1/0/2').io === 0 && n.ctrOf(sw.id, 'gi1/0/1').oo > 0);
  chk('ESR show interfaces counters gi1/0/1', /Packets received:\s+[1-9]/.test(n.exec(r.id, 'show interfaces counters gigabitethernet 1/0/1')));
  chk('ESR таблица счётчиков', /UC recv[\s\S]*UC sent/.test(n.exec(r.id, 'show interfaces counters')));
  n.exec(r.id, 'clear interfaces counters');
  chk('ESR clear interfaces counters', /Packets received:\s+0/.test(n.exec(r.id, 'show interfaces counters gi1/0/1')));
  var b0 = n.ctrOf(pc.id, 'eth0').im; n.tick(10);
  chk('BPDU раз в 2 с: VPC получает multicast', n.ctrOf(pc.id, 'eth0').im - b0 === 5, n.ctrOf(pc.id, 'eth0').im - b0);
  // фильтры
  var st = n.exec(sw.id, 'show interfaces status | include GI1/0/1');
  chk('MES | include без учёта регистра', st && st.split('\n').every(function (x) { return /gi1\/0\/1/i.test(x); }), st);
  chk('MES | exclude', n.exec(sw.id, 'show interfaces status | exclude gi1/0/1').indexOf('gi1/0/1 ') < 0);
  chk('MES | begin', /^gi1\/0\/5/.test(n.exec(sw.id, 'show interfaces status | begin gi1/0/5')), n.exec(sw.id, 'show interfaces status | begin gi1/0/5').slice(0, 40));
  n.exec(sw.id, 'configure'); n.exec(sw.id, 'interface gi1/0/3'); n.exec(sw.id, 'description UPLINK'); n.exec(sw.id, 'end');
  var sec = n.exec(sw.id, 'show running-config | section 1/0/3');
  chk('MES | section — блок interface до exit', /1\/0\/3[\s\S]*UPLINK[\s\S]*exit$/.test(sec), sec);
  chk('MES | ? — список фильтров', /include[\s\S]*section/.test(n.exec(sw.id, 'show running-config | ?')));
  var ei = n.exec(r.id, 'show interfaces status | include "^gi1/0/1 "');
  chk('ESR | include — регулярное выражение', /^gi1\/0\/1\s/.test(ei) && ei.split('\n').length === 1, ei);
  chk('ESR | count', /^\d+$/.test(n.exec(r.id, 'show running-config | count')));
  chk('ESR | until', n.exec(r.id, 'show running-config | until interface').indexOf('interface') < 0);
  chk('ESR | неизвестный фильтр', n.exec(r.id, 'show running-config | grep x') === 'Syntax error: Unknown command');
  chk('ESR: «|» в кавычках — не фильтр', !n.exec(r.id, 'configure') && !n.exec(r.id, 'interface gi1/0/2') && !n.exec(r.id, 'description "a|b"') && (n.exec(r.id, 'end'), true));
  // постраничный вывод
  chk('страница 24 строки, строки More по руководствам', n.pageLen(sw.id) === 24 && /More: <space>/.test(n.moreText(sw.id)) && /More\? Enter/.test(n.moreText(r.id)));
  n.exec(sw.id, 'terminal datadump'); chk('MES terminal datadump', n.pageLen(sw.id) === 0);
  n.exec(sw.id, 'terminal no datadump'); n.exec(r.id, 'terminal datadump'); chk('ESR terminal datadump', n.pageLen(sw.id) === 24 && n.pageLen(r.id) === 0);
  n.exec(sw.id, 'show running-config | no-more'); chk('| no-more — без страниц', n.pageLen(sw.id) === 0);
  // события: shutdown, logging console
  n.events(true);
  n.exec(sw.id, 'configure'); n.exec(sw.id, 'interface gi1/0/2'); n.exec(sw.id, 'shutdown'); n.exec(sw.id, 'end');
  ev = n.events();
  chk('shutdown → link DOWN', ev.some(function (e) { return e.id === sw.id && e.msg === 'CFA-4-Interface gi 1/0/2 link status DOWN'; }), JSON.stringify(ev));
  n.exec(sw.id, 'configure'); n.exec(sw.id, 'no logging console'); n.exec(sw.id, 'interface gi1/0/2'); n.exec(sw.id, 'no shutdown'); n.exec(sw.id, 'end');
  ev = n.events();
  chk('no logging console — в консоль нет, в буфер есть', !ev.some(function (e) { return e.id === sw.id; }) && /gi 1\/0\/2 link status UP/.test(n.exec(sw.id, 'show logging')) &&
      /no logging console/.test(n.exec(sw.id, 'show running-config')));
  var m6 = n.add('MES3300-24', 'SW6'); n.events(true); n.connect(m6.id, 'gi1/0/1', sw.id, 'gi1/0/3'); ev = n.events();
  chk('MES 6.x: %LINK-I-Up', ev.some(function (e) { return e.id === m6.id && /^%LINK-I-Up:\s+gi1\/0\/1$/.test(e.msg); }), JSON.stringify(ev));
  chk('STP: сообщения о корне/состоянии порта', ev.some(function (e) { return /%STP-W|AST-6-/.test(e.msg); }), JSON.stringify(ev));
  n.power(r.id, false); ev = n.events();
  chk('ESR выключен → у соседа link DOWN', ev.some(function (e) { return e.id === sw.id && /gi 1\/0\/1 link status DOWN/.test(e.msg); }) || /gi 1\/0\/1 link status DOWN/.test(n.exec(sw.id, 'show logging')));
  console.log('✓ живая консоль');
})();

// учебные инструменты: захват трафика на кабеле, разбор кадра по уровням, конфигурации текстом
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), sw = n.add('MES2428', 'SW1'), r = n.add('vESR', 'R1'), pc = n.add('VPC', 'PC1');
  n.connect(sw.id, 'gi1/0/1', r.id, 'gi1/0/1'); n.connect(sw.id, 'gi1/0/2', pc.id, 'eth0');
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'vlan database', 'vlan 10', 'exit', 'interface gi1/0/1', 'switchport mode trunk', 'switchport trunk allowed vlan add 10', 'exit',
                           'interface gi1/0/2', 'switchport access vlan 10', 'end'],
                     R1: ['configure', 'interface gi1/0/1.10', 'ip address 192.168.10.1/24', 'ip firewall disable', 'end', 'commit', 'confirm'],
                     PC1: ['ip 192.168.10.10/24 192.168.10.1'] });
  var capT = n.capStart(0), capA = n.capStart(1);
  chk('ping через транк', n.ping(pc.id, '192.168.10.1').ok);
  var fT = capT.frames, fA = capA.frames;
  chk('захват: ARP-запрос, ответ, ICMP request/reply на кабеле к ПК', ['Who has 192.168.10.1? Tell 192.168.10.10', '192.168.10.1 is at'].every(function (s) { return fA.some(function (f) { return f.info.indexOf(s) === 0; }); }) &&
      fA.some(function (f) { return f.proto === 'ICMP' && /request/.test(f.info); }) && fA.some(function (f) { return f.proto === 'ICMP' && /reply/.test(f.info); }), fA.map(function (f) { return f.info; }).join(' | '));
  chk('захват: на транке кадры с тегом VLAN 10, у ПК без тега', fT.length && fT.every(function (f) { return f.vlan === 10; }) && fA.every(function (f) { return f.vlan === null; }));
  var req = fA.filter(function (f) { return f.proto === 'ICMP' && /request/.test(f.info); })[0], rep = fT.filter(function (f) { return f.proto === 'ICMP' && /reply/.test(f.info); })[0];
  chk('ICMP: MAC отправителя/получателя, TTL 64', req && req.smac === EL.mac('PC1eth0') && req.sip === '192.168.10.10' && req.dip === '192.168.10.1' && req.f.ttl === 64 && rep && rep.sip === '192.168.10.1');
  var L = EL.decode(rep.f, rep.vlan, rep.len);
  chk('разбор: Ethernet II → 802.1Q → IPv4 → ICMP', L.map(function (x) { return x.osi; }).join(',') === 'L1,L2,L2,L3,L3' && /ID: 10/.test(L[2].name) && /Echo \(ping\) reply/.test(JSON.stringify(L[4])), L.map(function (x) { return x.name; }).join(' / '));
  var La = EL.decode(fA[0].f, null, 64);
  chk('разбор ARP: opcode request, Target MAC нули', /request \(1\)/.test(JSON.stringify(La)) && /00:00:00:00:00:00/.test(JSON.stringify(La)));
  n.tick(4);
  chk('захват: BPDU STP с коммутатора', fA.some(function (f) { return f.proto === 'STP' && f.dmac === '01:80:c2:00:00:00' && /Root =/.test(f.info); }) && EL.decode(fA.filter(function (f) { return f.proto === 'STP'; })[0].f, null, 64).some(function (x) { return /Spanning Tree Protocol/.test(x.name); }));
  n.capStop(capA); var k = capA.frames.length; n.ping(pc.id, '192.168.10.1'); chk('остановленный захват не пишет', capA.frames.length === k);
  // TCP: эфемерный порт клиента и SYN/ACK
  var d = n.add('Debian-server', 'SRV'); n.connect(sw.id, 'gi1/0/3', d.id, 'ens3');
  var tcp = n.request(pc.id, '192.168.10.1', 'tcp', 22), tf = tcp.steps.filter(function (s) { return s.f && s.f.proto === 'tcp'; });
  chk('TCP: запрос на 22 с эфемерного порта, ответ с 22', tf.length >= 2 && tf[0].f.sport >= 49152 && tf[0].f.dport === 22 && tf[tf.length - 1].f.sport === 22 && tf[tf.length - 1].f.dport === tf[0].f.sport || !tcp.ok);
  // конфигурации текстом: экспорт → чистые устройства → импорт → тот же running-config
  var txt = EL.exportConfigs(n);
  chk('экспорт: заголовки и конфиги', /! ==== SW1 \(MES2428\) ====/.test(txt) && /! ==== R1 \(vESR\) ====/.test(txt) && /192\.168\.10\.1\/24/.test(txt));
  var m = new EL.Net(), sw2 = m.add('MES2428', 'SW1'), r2 = m.add('vESR', 'R1');
  var errs = EL.importConfigs(m, txt);
  chk('импорт без ошибок', !errs.length, errs.join('; '));
  chk('импорт: тот же running-config MES', EL.cfgText(sw2) === EL.cfgText(sw), EL.cfgText(sw2) + '\n---\n' + EL.cfgText(sw));
  chk('импорт: тот же running-config ESR (применён commit)', EL.cfgText(r2) === EL.cfgText(r), EL.cfgText(r2));
  chk('импорт: неизвестное устройство', EL.importConfigs(m, '! ==== NOPE (x) ====\nhostname a').some(function (e) { return /нет устройства NOPE/.test(e); }));
  console.log('✓ учебные инструменты: захват, разбор, конфигурации');
})();

// IPv6: адреса, ND, статические маршруты, ping через ESR (справочник 1.23)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var A = EL.ip6;
  chk('ip6: сжатие и разбор', A.norm('2001:0db8:0000:0000:0000:0000:0000:0001') === '2001:db8::1' && A.norm('fe80::1:0:0:1') === 'fe80::1:0:0:1' && A.parse('1::2::3') === null && A.norm('::') === '::');
  chk('ip6: EUI-64 и solicited-node', A.eui64('e0:d9:e3:00:00:01') === 'fe80::e2d9:e3ff:fe00:1' && A.snm('2001:db8::abcd:1234') === 'ff02::1:ffcd:1234' && A.mmac('2001:db8::abcd:1234') === '33:33:ff:cd:12:34');
  var n = new EL.Net(), sw = n.add('MES2428', 'SW1'), r = n.add('vESR', 'R1'), p1 = n.add('VPC', 'PC1'), deb = n.add('Debian', 'D1');
  n.connect(sw.id, 'gi1/0/1', r.id, 'gi1/0/1'); n.connect(sw.id, 'gi1/0/2', p1.id, 'eth0'); n.connect(deb.id, 'ens3', r.id, 'gi1/0/2');
  var e = EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ipv6 address 2001:db8:1::1/64', 'exit', 'interface gi1/0/2', 'ipv6 address 2001:db8:2::1/64', 'end', 'commit', 'confirm'],
                             PC1: ['ip 2001:db8:1::10/64 2001:db8:1::1'] });
  chk('ESR ipv6 address без ошибок', !e.length, e.join('; '));
  chk('show ipv6 interfaces: адрес и link-local', /2001:db8:1::1\/64\s+gi1\/0\/1/.test(n.exec(r.id, 'show ipv6 interfaces')) && /fe80::\S+\/64\s+gi1\/0\/1/.test(n.exec(r.id, 'show ipv6 interfaces')));
  chk('show running-config: ipv6 address', /ipv6 address 2001:db8:1::1\/64/.test(n.exec(r.id, 'show running-config')));
  chk('VPC → ESR ping IPv6', /icmp6_seq=1 ttl=64/.test(n.exec(p1.id, 'ping 2001:db8:1::1')), n.exec(p1.id, 'ping 2001:db8:1::1'));
  chk('ESR: таблица соседей IPv6', /2001:db8:1::10\s+\S+/.test(n.exec(r.id, 'show ipv6 neighbors')) || /fe80/.test(n.exec(r.id, 'show ipv6 neighbors')), n.exec(r.id, 'show ipv6 neighbors'));
  chk('MES выучил MAC VPC по IPv6-кадру', Object.keys(n.mac[sw.id]).some(function (k) { return k.indexOf(EL.mac('PC1eth0')) > 0; }));
  // Debian: вход и адрес
  ['root', 'toor', 'ip link set ens3 up', 'ip -6 addr add 2001:db8:2::20/64 dev ens3', 'ip -6 route add default via 2001:db8:2::1'].forEach(function (l) { n.exec(deb.id, l); });
  chk('Debian ip -6 addr', /inet6 2001:db8:2::20\/64 scope global/.test(n.exec(deb.id, 'ip -6 addr')), n.exec(deb.id, 'ip -6 addr'));
  var pp = n.ping6(p1.id, '2001:db8:2::20');
  chk('VPC → Debian через ESR (маршрутизация IPv6)', pp.ok && pp.hops.length === 2, pp.steps.map(function (s) { return s.t; }).join(' | '));
  chk('Debian ping -6 → VPC', /64 bytes from 2001:db8:1::10: icmp_seq=1 ttl=63/.test(n.exec(deb.id, 'ping -6 2001:db8:1::10')), n.exec(deb.id, 'ping -6 2001:db8:1::10'));
  chk('шаги трассы: NS на solicited-node, NA, Hop Limit', pp.steps.some(function (s) { return s.f && s.f.icmp6 === 'ns' && /^ff02::1:ff/.test(s.f.dst); }) || n.ping6(p1.id, '2001:db8:2::21').steps.some(function (s) { return s.f && s.f.icmp6 === 'ns'; }));
  // без шлюза — нет маршрута; другой сети нет — ND без ответа
  n.exec(p1.id, 'ip 2001:db8:1::10/64');
  chk('VPC без шлюза IPv6 — нет маршрута', !n.ping6(p1.id, '2001:db8:2::20').ok);
  chk('ND без ответа — Address unreachable', n.ping6(p1.id, '2001:db8:1::99').why === 'Address unreachable');
  // статический маршрут на ESR и show ipv6 route
  var n2 = new EL.Net(), ra = n2.add('vESR', 'RA'), rb = n2.add('vESR', 'RB'), pa = n2.add('VPC', 'PA'), pb = n2.add('VPC', 'PB');
  n2.connect(ra.id, 'gi1/0/1', rb.id, 'gi1/0/1'); n2.connect(pa.id, 'eth0', ra.id, 'gi1/0/2'); n2.connect(pb.id, 'eth0', rb.id, 'gi1/0/2');
  EL.labs.apply(n2, { RA: ['configure', 'interface gi1/0/1', 'ipv6 address fc00::1/64', 'exit', 'interface gi1/0/2', 'ipv6 address 2001:a::1/64', 'exit', 'end', 'commit', 'confirm'],
                      RB: ['configure', 'interface gi1/0/1', 'ipv6 address fc00::2/64', 'exit', 'interface gi1/0/2', 'ipv6 address 2001:b::1/64', 'exit', 'ipv6 route ::/0 fc00::1', 'end', 'commit', 'confirm'],
                      PA: ['ip 2001:a::10/64 2001:a::1'], PB: ['ip 2001:b::10/64 2001:b::1'] });
  chk('без маршрута на RA — нет связи', !n2.ping6(pa.id, '2001:b::10').ok);
  EL.labs.apply(n2, { RA: ['configure', 'ipv6 route 2001:b::/64 fc00::2', 'end', 'commit', 'confirm'] });
  chk('ipv6 route — связь есть', n2.ping6(pa.id, '2001:b::10').ok);
  chk('show ipv6 route: S и C', /S\s+\* 2001:b::\/64\s+\[1\/0\]\s+via fc00::2 on gi1\/0\/1/.test(n2.exec(ra.id, 'show ipv6 route')) && /C\s+\* fc00::\/64/.test(n2.exec(ra.id, 'show ipv6 route')), n2.exec(ra.id, 'show ipv6 route'));
  chk('ESR ping IPv6 !!!!!', /!!!!!/.test(n2.exec(rb.id, 'ping 2001:a::10')));
  chk('ESR: неверный IPv6', n2.exec(ra.id, 'configure') === '' && /Illegal/.test(n2.exec(ra.id, 'ipv6 route 2001:zz::/64 fc00::2')));
  var st = n2.ping6(pa.id, '2001:b::10').steps.filter(function (s) { return s.k === 'ip' && s.f; })[0];
  var L = EL.decode(st.f, null, 118);
  chk('разбор IPv6: Ethernet 0x86dd → IPv6 → ICMPv6', /0x86dd/.test(JSON.stringify(L[1])) && /Internet Protocol Version 6/.test(L[2].name) && /Message Protocol v6/.test(L[3].name), L.map(function (x) { return x.name; }).join(' / '));
  console.log('✓ IPv6');
})();

// RIPng и OSPFv3 на ESR: три маршрутизатора в цепочку, ПК по краям
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  function chain(proto) {
    var n = new EL.Net(), r1 = n.add('vESR', 'R1'), r2 = n.add('vESR', 'R2'), r3 = n.add('vESR', 'R3'), pa = n.add('VPC', 'PA'), pb = n.add('VPC', 'PB');
    n.connect(r1.id, 'gi1/0/1', r2.id, 'gi1/0/1'); n.connect(r2.id, 'gi1/0/2', r3.id, 'gi1/0/1'); n.connect(pa.id, 'eth0', r1.id, 'gi1/0/2'); n.connect(pb.id, 'eth0', r3.id, 'gi1/0/2');
    var A = { R1: [['gi1/0/1', '2001:12::1/64'], ['gi1/0/2', '2001:a::1/64']], R2: [['gi1/0/1', '2001:12::2/64'], ['gi1/0/2', '2001:23::2/64']], R3: [['gi1/0/1', '2001:23::3/64'], ['gi1/0/2', '2001:b::1/64']] };
    var sc = {};
    Object.keys(A).forEach(function (r, i) { var L = ['configure'];
      A[r].forEach(function (x) { L.push('interface ' + x[0], 'ipv6 address ' + x[1]); if (proto === 'O') L.push('ipv6 ospf instance 1', 'ipv6 ospf area 0.0.0.0', 'ipv6 ospf'); L.push('exit'); });
      if (proto === 'R') L.push('ipv6 router rip', 'network 2001::/16', 'enable', 'exit');
      else L.push('ipv6 router ospf 1', 'router-id ' + (i + 1) + '.' + (i + 1) + '.' + (i + 1) + '.' + (i + 1), 'area 0.0.0.0', 'enable', 'exit', 'enable', 'exit');
      L.push('end', 'commit', 'confirm'); sc[r] = L; });
    sc.PA = ['ip 2001:a::10/64 2001:a::1']; sc.PB = ['ip 2001:b::10/64 2001:b::1'];
    return { n: n, errs: EL.labs.apply(n, sc), r1: r1, r2: r2, pa: pa, pb: pb };
  }
  var v = chain('R');
  chk('RIPng: конфигурация без ошибок', !v.errs.length, v.errs.join('; '));
  chk('RIPng: PA → PB через три ESR', v.n.ping6(v.pa.id, '2001:b::10').ok);
  chk('RIPng: show ipv6 rip — via link-local, метрика 3', /2001:b::\/64\s+via fe80::\S+ on gi1\/0\/1 \[rip 00:00:00\] \* \(120\/3\)/.test(v.n.exec(v.r1.id, 'show ipv6 rip')), v.n.exec(v.r1.id, 'show ipv6 rip'));
  chk('RIPng: show ipv6 route — R', /^R\s+\* 2001:b::\/64/m.test(v.n.exec(v.r1.id, 'show ipv6 route')));
  chk('RIPng: running-config', /ipv6 router rip\n  network 2001::\/16\n  enable\nexit/.test(v.n.exec(v.r1.id, 'show running-config')));
  EL.labs.apply(v.n, { R2: ['configure', 'ipv6 router rip', 'no enable', 'exit', 'end', 'commit', 'confirm'] });
  chk('RIPng выключен на R2 — связи нет', !v.n.ping6(v.pa.id, '2001:b::10').ok);
  var o = chain('O');
  chk('OSPFv3: конфигурация без ошибок', !o.errs.length, o.errs.join('; '));
  chk('OSPFv3: PA → PB', o.n.ping6(o.pa.id, '2001:b::10').ok);
  chk('OSPFv3: соседи R2 — R1 и R3', (o.n.exec(o.r2.id, 'show ipv6 ospf neighbors').match(/full/g) || []).length === 2, o.n.exec(o.r2.id, 'show ipv6 ospf neighbors'));
  chk('OSPFv3: маршрут O', /^O\s+\* 2001:b::\/64\s+\[110\/0\]/m.test(o.n.exec(o.r1.id, 'show ipv6 route')), o.n.exec(o.r1.id, 'show ipv6 route'));
  EL.labs.apply(o.n, { R1: ['configure', 'ipv6 router ospf 1', 'area 0.0.0.0', 'no enable', 'end', 'commit', 'confirm'] });
  chk('OSPFv3: область выключена — связи нет', !o.n.ping6(o.pa.id, '2001:b::10').ok);
  console.log('✓ RIPng и OSPFv3');
})();

// DNS: BIND9 на Debian-server, клиенты Debian, VPC, ESR, MES
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), sw = n.add('MES2428', 'SW1'), r = n.add('vESR', 'R1'), srv = n.add('Debian-server', 'SRV'), pc = n.add('VPC', 'PC1'), cl = n.add('Debian', 'CL'), m6 = n.add('MES3300-24', 'SW6');
  n.connect(sw.id, 'gi1/0/1', r.id, 'gi1/0/1'); n.connect(sw.id, 'gi1/0/2', srv.id, 'ens3'); n.connect(sw.id, 'gi1/0/3', pc.id, 'eth0'); n.connect(sw.id, 'gi1/0/4', cl.id, 'ens3'); n.connect(sw.id, 'gi1/0/5', m6.id, 'gi1/0/1');
  var ex = function (d, L) { return L.map(function (l) { return n.exec(d.id, l); }); };
  EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ip address 10.0.0.1/24', 'ip firewall disable', 'exit', 'domain lookup enable', 'domain name-server 10.0.0.53', 'domain name lab.local',
                          'domain ip host gw.lab.local 10.0.0.1', 'end', 'commit', 'confirm'], PC1: ['ip 10.0.0.20/24 10.0.0.1', 'ip dns 10.0.0.53'],
                     SW1: ['enable', 'configure', 'interface vlan 1', 'ip address 10.0.0.2 255.255.255.0', 'exit', 'ip name-server ipv4 10.0.0.53', 'end'],
                     SW6: ['enable', 'configure', 'interface vlan 1', 'ip address 10.0.0.6 255.255.255.0', 'exit', 'ip name-server 10.0.0.53', 'ip host printer 10.0.0.77', 'end'] });
  ex(srv, ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.53/24 dev ens3']);
  srv.st.files['/etc/bind/named.conf.local'] += 'zone "lab.local" {\n\ttype master;\n\tfile "/etc/bind/db.lab.local";\n};\n';
  srv.st.files['/etc/bind/db.lab.local'] = '$TTL 604800\n@ IN SOA ns.lab.local. root.lab.local. (\n 2 ; Serial\n 604800 )\n@ IN NS ns.lab.local.\nns IN A 10.0.0.53\nwww IN A 10.0.0.53\nftp IN CNAME www\npc1 IN A 10.0.0.20\n';
  ex(cl, ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.30/24 dev ens3']);
  cl.st.files['/etc/resolv.conf'] = 'search lab.local\nnameserver 10.0.0.53\n';
  chk('до restart bind9 зона не загружена: NXDOMAIN', /NXDOMAIN/.test(n.exec(cl.id, 'nslookup www.lab.local')), n.exec(cl.id, 'nslookup www.lab.local'));
  n.exec(srv.id, 'systemctl restart bind9');
  var o = n.exec(cl.id, 'nslookup www.lab.local');
  chk('nslookup: ответ A', /Server:\t\t10\.0\.0\.53[\s\S]*Name:\twww\.lab\.local\nAddress: 10\.0\.0\.53/.test(o), o);
  chk('nslookup: CNAME → A', /Address: 10\.0\.0\.53/.test(n.exec(cl.id, 'nslookup ftp.lab.local')));
  chk('nslookup: короткое имя + search', /Name:\tpc1\.lab\.local\nAddress: 10\.0\.0\.20/.test(n.exec(cl.id, 'nslookup pc1')));
  chk('nslookup: нет имени — NXDOMAIN', /can't find nope\.lab\.local: NXDOMAIN/.test(n.exec(cl.id, 'nslookup nope.lab.local')));
  chk('Debian ping по имени', /^PING www\.lab\.local \(10\.0\.0\.53\)[\s\S]*64 bytes from 10\.0\.0\.53/.test(n.exec(cl.id, 'ping www.lab.local')), n.exec(cl.id, 'ping www.lab.local'));
  chk('Debian curl по имени — Apache', /It works/.test(n.exec(cl.id, 'curl http://www.lab.local/')));
  chk('Debian /etc/hosts раньше DNS', (cl.st.files['/etc/hosts'] += '10.0.0.53 local-only\n', /PING local-only \(10\.0\.0\.53\)/.test(n.exec(cl.id, 'ping local-only'))));
  chk('VPC ping по имени', /www\.lab\.local resolved to 10\.0\.0\.53[\s\S]*84 bytes from 10\.0\.0\.53/.test(n.exec(pc.id, 'ping www.lab.local')), n.exec(pc.id, 'ping www.lab.local'));
  chk('VPC show — DNS', /DNS\s+: 10\.0\.0\.53/.test(n.exec(pc.id, 'show')));
  chk('ESR ping по имени и domain name', /PING www\.lab\.local \(10\.0\.0\.53\)[\s\S]*!!!!!/.test(n.exec(r.id, 'ping www.lab.local')) && /!!!!!/.test(n.exec(r.id, 'ping pc1')), n.exec(r.id, 'ping pc1'));
  chk('ESR domain ip host без сервера', /PING gw\.lab\.local \(10\.0\.0\.1\)/.test(n.exec(r.id, 'ping gw.lab.local')));
  chk('ESR running-config: domain', /domain lookup enable[\s\S]*domain name-server 10\.0\.0\.53/.test(n.exec(r.id, 'show running-config')));
  chk('MES 10 ping по имени', /Reply Received From :10\.0\.0\.53/.test(n.exec(sw.id, 'ping www.lab.local')), n.exec(sw.id, 'ping www.lab.local'));
  chk('MES 10 running-config: ip name-server ipv4', /ip name-server ipv4 10\.0\.0\.53/.test(n.exec(sw.id, 'show running-config')));
  chk('MES 6 ip host', /10\.0\.0\.77/.test(n.exec(m6.id, 'ping printer')) || /Unknown/.test(n.exec(m6.id, 'ping printer')) === false);
  n.exec(srv.id, 'systemctl stop bind9');
  chk('bind9 остановлен — timeout', /no servers could be reached/.test(n.exec(cl.id, 'nslookup www.lab.local')) && /Temporary failure/.test(n.exec(cl.id, 'ping www.lab.local')));
  var cap = n.capStart(1); n.exec(srv.id, 'systemctl start bind9'); n.exec(cl.id, 'nslookup www.lab.local');
  chk('захват: DNS-запрос и ответ', cap.frames.some(function (f) { return f.proto === 'DNS' && /Standard query A www\.lab\.local/.test(f.info); }) &&
      cap.frames.some(function (f) { return /Standard query response A www\.lab\.local A 10\.0\.0\.53/.test(f.info); }), cap.frames.map(function (f) { return f.info; }).join(' | '));
  console.log('✓ DNS');
})();

// GRE: офис A — провайдер — офис B, частные сети связаны туннелем
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), ra = n.add('vESR', 'RA'), isp = n.add('vESR', 'ISP'), rb = n.add('vESR', 'RB'), pa = n.add('VPC', 'PA'), pb = n.add('VPC', 'PB');
  n.connect(ra.id, 'gi1/0/1', isp.id, 'gi1/0/1'); n.connect(isp.id, 'gi1/0/2', rb.id, 'gi1/0/1'); n.connect(pa.id, 'eth0', ra.id, 'gi1/0/2'); n.connect(pb.id, 'eth0', rb.id, 'gi1/0/2');
  var base = { ISP: ['configure', 'interface gi1/0/1', 'ip address 100.0.0.1/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 100.0.1.1/30', 'ip firewall disable', 'exit', 'end', 'commit', 'confirm'],
    RA: ['configure', 'interface gi1/0/1', 'ip address 100.0.0.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit', 'ip route 0.0.0.0/0 100.0.0.1', 'end', 'commit', 'confirm'],
    RB: ['configure', 'interface gi1/0/1', 'ip address 100.0.1.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 192.168.2.1/24', 'ip firewall disable', 'exit', 'ip route 0.0.0.0/0 100.0.1.1', 'end', 'commit', 'confirm'],
    PA: ['ip 192.168.1.10/24 192.168.1.1'], PB: ['ip 192.168.2.10/24 192.168.2.1'] };
  chk('GRE: базовая схема без ошибок', !EL.labs.apply(n, base).length);
  chk('без туннеля частные сети не связаны (у провайдера нет маршрута)', !n.ping(pa.id, '192.168.2.10').ok);
  var e = EL.labs.apply(n, {
    RA: ['configure', 'tunnel gre 1', 'local address 100.0.0.2', 'remote address 100.0.1.2', 'ip address 10.10.10.1/30', 'ip firewall disable', 'enable', 'exit', 'ip route 192.168.2.0/24 10.10.10.2', 'end', 'commit', 'confirm'],
    RB: ['configure', 'tunnel gre 1', 'local address 100.0.1.2', 'remote address 100.0.0.2', 'ip address 10.10.10.2/30', 'ip firewall disable', 'enable', 'exit', 'ip route 192.168.1.0/24 10.10.10.1', 'end', 'commit', 'confirm'] });
  chk('GRE: команды туннеля без ошибок', !e.length, e.join('; '));
  chk('приглашение (config-gre)#', (n.exec(ra.id, 'configure'), n.exec(ra.id, 'tunnel gre 1'), /\(config-gre\)#$/.test(n.prompt(ra.id))), n.prompt(ra.id)); n.exec(ra.id, 'end');
  var cap = n.capStart(0), r = n.ping(pa.id, '192.168.2.10');
  chk('PA → PB через GRE', r.ok, r.steps.map(function (s) { return s.t; }).join(' | '));
  chk('трасса: инкапсуляция и снятие GRE', r.steps.some(function (s) { return /инкапсулирован в GRE/.test(s.t); }) && r.steps.some(function (s) { return /GRE снят/.test(s.t); }));
  var g = cap.frames.filter(function (f) { return f.f.proto === 'gre'; });
  chk('захват у провайдера: внешний 100.0.0.2 → 100.0.1.2, внутри ICMP', g.length >= 2 && g[0].sip === '100.0.0.2' && g[0].dip === '100.0.1.2' && g[0].proto === 'ICMP' && /^GRE · 192\.168\.1\.10 → 192\.168\.2\.10/.test(g[0].info), g.map(function (f) { return f.info; }).join(' | '));
  var L = EL.decode(g[0].f, null, g[0].len);
  chk('разбор: IPv4 (GRE 47) → GRE → внутренний IPv4 → ICMP', /GRE \(47\)/.test(JSON.stringify(L)) && L.some(function (x) { return /Generic Routing Encapsulation/.test(x.name); }) && L.some(function (x) { return /↳ Internet Protocol Version 4, Src: 192\.168\.1\.10/.test(x.name); }), L.map(function (x) { return x.name; }).join(' / '));
  chk('show tunnels status', /gre 1\s+Up\s+1476\s+100\.0\.0\.2\s+100\.0\.1\.2/.test(n.exec(ra.id, 'show tunnels status')), n.exec(ra.id, 'show tunnels status'));
  chk('running-config: tunnel gre 1', /tunnel gre 1\n  ip firewall disable\n  ip address 10\.10\.10\.1\/30\n  local address 100\.0\.0\.2\n  remote address 100\.0\.1\.2\n  enable\nexit/.test(n.exec(ra.id, 'show running-config')), n.exec(ra.id, 'show running-config'));
  EL.labs.apply(n, { RB: ['configure', 'tunnel gre 1', 'no enable', 'end', 'commit', 'confirm'] });
  var r2 = n.ping(pa.id, '192.168.2.10');
  chk('туннель выключен на RB — GRE отброшен', !r2.ok && r2.steps.some(function (s) { return /нет включённого GRE-туннеля/.test(s.t); }));
  EL.labs.apply(n, { RB: ['configure', 'tunnel gre 1', 'enable', 'no ip firewall disable', 'end', 'commit', 'confirm'] });
  chk('туннель без зоны и с межсетевым экраном — отброшено', !n.ping(pa.id, '192.168.2.10').ok);
  console.log('✓ GRE');
})();

console.log('\nИтого прогонов: ' + total + ', ошибок: ' + fail);
process.exit(fail ? 1 : 0);
