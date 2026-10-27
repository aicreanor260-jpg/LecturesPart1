/* Автопрогон: для каждой лабы и каждого случайного задания генерирует N вариантов, вводит решение в CLI и проверяет.
   Запуск: node decks/_elab/test.js [N]  (по умолчанию 12) */
'use strict';
var fs = require('fs'), path = require('path'), vm = require('vm');
var D = __dirname, N = +process.argv[2] || 12;
global.window = global;
['../_dk_cli.js', 'common.js', 'esr.js', 'esr_svc.js', 'esr_more.js', 'esr_ops.js', 'mesx.js', 'mes_l2.js', 'mes_dialects.js', 'hosts.js', 'catalog.js', 'net.js', 'tables.js', 'aging.js', 'mes_full.js', 'esr_fw.js', 'labs.js', 'labs_routing.js', 'labs_services.js', 'labs_l2.js', 'labs_ops.js', 'labs_exam.js'].forEach(function (f) {
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

console.log('\nИтого прогонов: ' + total + ', ошибок: ' + fail);
process.exit(fail ? 1 : 0);
