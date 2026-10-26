/* Автопрогон: для каждой лабы и каждого случайного задания генерирует N вариантов, вводит решение в CLI и проверяет.
   Запуск: node decks/_elab/test.js [N]  (по умолчанию 12) */
'use strict';
var fs = require('fs'), path = require('path'), vm = require('vm');
var D = __dirname, N = +process.argv[2] || 12;
global.window = global;
['../_dk_cli.js', 'common.js', 'esr.js', 'esr_svc.js', 'mesx.js', 'hosts.js', 'catalog.js', 'net.js', 'labs.js', 'labs_routing.js', 'labs_services.js', 'labs_exam.js'].forEach(function (f) {
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

console.log('\nИтого прогонов: ' + total + ', ошибок: ' + fail);
process.exit(fail ? 1 : 0);
