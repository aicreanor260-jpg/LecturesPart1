/* Автопрогон: для каждой лабы и каждого случайного задания генерирует N вариантов, вводит решение в CLI и проверяет.
   Запуск: node decks/_elab/test.js [N]  (по умолчанию 12) */
'use strict';
var fs = require('fs'), path = require('path'), vm = require('vm');
var D = __dirname, N = +process.argv[2] || 12;
global.window = global;
['../_dk_cli.js', 'common.js', 'esr.js', 'esr_svc.js', 'esr_more.js', 'esr_ops.js', 'mesx.js', 'mes_l2.js', 'mes_dialects.js', 'hosts.js', 'catalog.js', 'net.js', 'tables.js', 'labs.js', 'labs_routing.js', 'labs_services.js', 'labs_l2.js', 'labs_ops.js', 'labs_exam.js'].forEach(function (f) {
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
  var r2 = n.ping(v[0].id, '10.0.0.2');
  chk('таблицы: повторный ping без ARP-запроса', r2.ok && !r2.steps.some(function (x) { return x.k === 'arp'; }));
  var r3 = n.ping(v[0].id, '10.0.0.3');
  chk('таблицы: разные VLAN — не доходит', !r3.ok && r3.why === 'Host unreachable' && !n.macRows(s.id).some(function (x) { return x.mac === m3; }));
  EL.labs.apply(n, { SW1: ['configure', 'interface gi1/0/2', 'switchport access vlan 20', 'end'] });
  var r4 = n.ping(v[0].id, '10.0.0.2'), r5 = n.ping(v[0].id, '10.0.0.2');
  chk('таблицы: устаревшая ARP-запись после смены VLAN', !r4.ok && !n.arp[v[0].id]['10.0.0.2'] && !r5.ok && r5.why === 'Host unreachable');
  chk('таблицы: show mac address-table / show arp', /Learnt/.test(n.exec(s.id, 'show mac address-table')) && /10\.0\.0\.1/.test(n.exec(v[1].id, 'arp')));
  console.log('✓ таблицы ARP и MAC');
})();

console.log('\nИтого прогонов: ' + total + ', ошибок: ' + fail);
process.exit(fail ? 1 : 0);
