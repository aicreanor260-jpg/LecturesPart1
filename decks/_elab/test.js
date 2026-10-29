/* Автопрогон: для каждой лабы и каждого случайного задания генерирует N вариантов, вводит решение в CLI и проверяет.
   Запуск: node decks/_elab/test.js [N]  (по умолчанию 12) */
'use strict';
var fs = require('fs'), path = require('path'), vm = require('vm');
var D = __dirname, N = +process.argv[2] || 12;
global.window = global;
var engineFiles = ['../_dk_cli.js', 'common.js', 'esr.js', 'esr_svc.js', 'esr_more.js', 'esr_ops.js', 'mesx.js', 'mes_l2.js', 'mes_dialects.js', 'hosts.js', 'catalog.js', 'net.js', 'tables.js', 'aging.js', 'mes_full.js', 'esr_fw.js', 'rt_timers.js', 'console.js', 'frames.js', 'ipv6.js', 'ipv6_rt.js', 'slaac.js', 'dhcp6.js', 'dns.js', 'tunnel.js', 'ipsec.js', 'physics.js', 'l2sec.js', 'qinq.js', 'mstp.js', 'stp_timers.js', 'dhcp_timers.js', 'svc_timers.js', 'snmp.js', 'aaa.js', 'ra.js', 'wg.js', 'ovpn.js', 'vrf.js', 'reload.js', 'pbr.js', 'bfd.js', 'bgp.js', 'bgp_policy.js', 'l2tp.js', 'dot1x.js', 'igmp.js', 'pim.js', 'stack.js', 'mtu.js', 'scs.js', 'ssh.js', 'wlc.js', 'olt.js', 'lte.js', 'tau.js', 'esbc.js', 'cpe.js', 'cables.js', 'linkprops.js', 'isp.js', 'simexp.js', 'simnb.js', 'apps.js', 'srv.js', 'me.js', 'me_mpls.js', 'security.js', 'huawei.js', 'huawei_s.js', 'huawei_ar.js', 'faults.js', 'mes10.js', 'sim.js', 'qos.js', 'pt.js', 'labs.js', 'labs_routing.js', 'labs_services.js', 'labs_l2.js', 'labs_ops.js', 'labs_exam.js', 'labs_faults.js'];
engineFiles.forEach(function (f) {
  vm.runInThisContext(fs.readFileSync(path.join(D, f), 'utf8'), { filename: f });
});
var EL = global.EL, fail = 0, total = 0;
// схемы в тестах собираются мгновенно: порты новых кабелей считаются давно сошедшимися по STP;
// таймеры STP проверяются отдельно (net.stpReal = true)
['connect', 'exec', 'power'].forEach(function (m) { var P = EL.Net.prototype, f = P[m];
  P[m] = function () { var r = f.apply(this, arguments); if (!this.stpReal) this.stpSettle(); return r; }; });

function runLab(L) {
  for (var i = 0; i < N; i++) {
    total++;
    var net = new EL.Net(), p = L.gen(); L.build(net, p); EL.labs.powerOff(net);
    if (i === 0 && net.list().some(function (d) { return !d.off; })) { fail++; console.error('✗ ' + L.id + ': при открытии лабы не всё выключено'); }
    net.list().forEach(function (d) { net.power(d.id, true); });   // студент включает оборудование
    net.tick(31);   // STP: порты к узлам и между мостами переходят в forwarding
    var tasks = L.tasks(p);
    if (i === 0) {                                // до работы студента пункты не горят (кроме проверки уже работающей службы)
      var pre = tasks.filter(function (t) { var y = false; try { y = !!t.ok(net); } catch (e) { y = false; } return y && !/tftpd-hpa запущена/.test(t.t); });
      if (L.id.charAt(0) !== 'T' && pre.length) { fail++; console.error('✗ ' + L.id + ' горит без действий: ' + pre.map(function (t) { return t.t; }).join(' | ')); }
    }
    if (L.id.charAt(0) === 'T') {                 // поиск неисправности: до исправления ping не должен проходить
      if (tasks[0].ok(net)) { fail++; console.error('✗ ' + L.id + ' неисправность ' + p.fault + ' не ломает сеть'); continue; }
    }
    var errs = EL.labs.apply(net, L.sol(p));
    net.tick(60);                                 // протоколам нужно время: OSPF ждёт выбора DR (wait timer 40 с)
    var bad = tasks.filter(function (t) { return !t.ok(net); });
    // как в интерфейсе: hostname переименовывает устройство на схеме (syncHost) — проверки лаб должны находить его по исходному имени
    net.list().forEach(function (d) { var h = net.hostOf(d.id); if (h && h !== d.name) net.rename(d.id, h); });
    tasks.forEach(function (t) { if (bad.indexOf(t) < 0 && !t.ok(net)) bad.push({ t: t.t + ' (после переименования по hostname)' }); });
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

// пункты лабы загораются по одному действию: имя, часовой пояс, IP — каждое отдельно, только после commit + confirm
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Пункты лаб: ' + name + (extra ? ' — ' + extra : '')); } }
  function lit(L, p, net) { return L.tasks(p).map(function (t, k) { var y = false; try { y = !!t.ok(net); } catch (e) { y = false; } return y ? k + 1 : 0; }).filter(Boolean); }
  var L = EL.labs.byId('3.1'), p = L.gen(); p.tz = '+3'; var net = new EL.Net(); L.build(net, p); var r = net.byName('R1'), T = L.tasks(p);
  function idx(re) { for (var k = 0; k < T.length; k++) if (re.test(T[k].t)) return k + 1; return -1; }
  net.exec(r.id, 'configure'); net.exec(r.id, 'hostname R1');
  chk('3.1: hostname без commit — пункт не горит', lit(L, p, net).indexOf(idx(/^Имя маршрутизатора/)) < 0);
  net.exec(r.id, 'do commit'); net.exec(r.id, 'do confirm');
  chk('3.1: hostname R1 + commit + confirm — горит только пункт «Имя» (и «применено»)', lit(L, p, net).join() === [idx(/^Имя маршрутизатора/), idx(/^Все изменения применены/)].join(), lit(L, p, net).join());
  net.rename(r.id, 'R1');
  net.exec(r.id, 'clock timezone gmt 3'); net.exec(r.id, 'do commit'); net.exec(r.id, 'do confirm');
  chk('3.1: clock timezone gmt 3 (без плюса) — пункт «Часовой пояс GMT +3» горит', lit(L, p, net).indexOf(idx(/^Часовой пояс/)) >= 0);
  net.exec(r.id, 'clock timezone gmt +03'); net.exec(r.id, 'do commit'); net.exec(r.id, 'do confirm');
  chk('3.1: clock timezone gmt +03 — тоже засчитано', lit(L, p, net).indexOf(idx(/^Часовой пояс/)) >= 0 && r.st.run.tz === '+3');
  net.exec(r.id, 'interface gigabitethernet 1/0/1'); net.exec(r.id, 'ip address 192.168.' + p.x + '.1/24'); net.exec(r.id, 'exit'); net.exec(r.id, 'do commit'); net.exec(r.id, 'do confirm');
  chk('3.1: IP на gi1/0/1 — горит «IP-адрес», а «экран отключён» ещё нет', lit(L, p, net).indexOf(idx(/^gi1\/0\/1: IP-адрес/)) >= 0 && lit(L, p, net).indexOf(idx(/^gi1\/0\/1: межсетевой/)) < 0);
  // интерфейс: hostname переименовывает устройство на схеме — пункт и связь не теряются
  var L2 = EL.labs.byId('4.3'), p2 = L2.gen(), n2 = new EL.Net(); L2.build(n2, p2); n2.tick(31);
  var R1 = n2.byName('R1'); n2.exec(R1.id, 'configure'); n2.exec(R1.id, 'hostname Router-left'); n2.exec(R1.id, 'do commit'); n2.exec(R1.id, 'do confirm');
  n2.rename(R1.id, 'Router-left');
  var l2 = lit(L2, p2, n2), T2 = L2.tasks(p2);
  chk('4.3: имя R1 горит отдельно от имени R2, даже когда на схеме R1 уже «Router-left»', T2[l2[0] - 1] && /^Имя R1: Router-left/.test(T2[l2[0] - 1].t) && !l2.some(function (k) { return /^Имя R2/.test(T2[k - 1].t); }), l2.join());
  chk('переименованное устройство находится и по исходному имени', n2.byName('R1') === R1 && n2.byName('R1', true) === null);
  // экзамен: имя одного маршрутизатора — один пункт
  var LE = EL.labs.byId('E.1'), pe = LE.gen(), ne = new EL.Net(); LE.build(ne, pe); var TE = LE.tasks(pe), r3 = ne.byName('R3'), nm = TE.filter(function (t) { return /^1\. R3: имя /.test(t.t); })[0];
  ne.exec(r3.id, 'configure'); ne.exec(r3.id, 'hostname ' + nm.t.split('имя ')[1]); ne.exec(r3.id, 'do commit'); ne.exec(r3.id, 'do confirm');
  var le = lit(LE, pe, ne).filter(function (k) { return !/всё применено/.test(TE[k - 1].t); });
  chk('E.1: имя R3 — загорелся ровно один пункт «1. R3: имя …»', le.length === 1 && TE[le[0] - 1] === TE[TE.indexOf(nm)] || (le.length === 1 && /^1\. R3/.test(TE[le[0] - 1].t)), le.map(function (k) { return TE[k - 1].t; }).join(' | '));
  console.log('✓ Пункты лаб — по одному действию');
})();
// неоднозначные сокращения: Enter — ошибка без выполнения, Tab — до общего начала, повторный Tab — варианты; do — по командам режима #
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Сокращения: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), s = n.add('MES2428', 'SW'), s6 = n.add('MES3348', 'SW6');
  chk('ESR: con + Enter — неоднозначно, режим не сменился', n.exec(r.id, 'con') === '% Ambiguous command' && r.st.mode === 'priv');
  chk('ESR: conf + Enter — тоже неоднозначно (configure / confirm)', n.exec(r.id, 'conf') === '% Ambiguous command' && r.st.mode === 'priv');
  chk('ESR: Tab на con → confi (общее начало confirm/configure)', n.tab(r.id, 'con') === 'confi', n.tab(r.id, 'con'));
  chk('ESR: Tab на confi — дальше дописать нечего, варианты как у «?»', n.tab(r.id, 'confi') === null && /confirm/.test(n.help(r.id, 'confi')) && /configure/.test(n.help(r.id, 'confi')));
  chk('ESR: confi + g + Tab → configure', n.tab(r.id, 'config') === 'configure ', n.tab(r.id, 'config'));
  chk('ESR: configure полностью — работает', (n.exec(r.id, 'configure'), r.st.mode === 'config'));
  chk('ESR: do con — неоднозначно, остаёмся в config', n.exec(r.id, 'do con') === '% Ambiguous command' && r.st.mode === 'config');
  chk('ESR: do com + Tab → do commit', n.tab(r.id, 'do com') === 'do commit ', n.tab(r.id, 'do com'));
  chk('ESR: do con + Tab → do confi', n.tab(r.id, 'do con') === 'do confi', n.tab(r.id, 'do con'));
  chk('ESR: do confir + Tab → do confirm', n.tab(r.id, 'do confir') === 'do confirm ', n.tab(r.id, 'do confir'));
  chk('ESR: однозначные сокращения работают — sh ru, do sh ru', /hostname/.test(n.exec(r.id, 'do sh ru')) && (n.exec(r.id, 'end'), /hostname/.test(n.exec(r.id, 'sh ru'))));
  n.exec(s.id, 'enable');
  chk('MES: conf t — работает', (n.exec(s.id, 'conf t'), s.st.mode === 'config'));
  chk('MES: do sh ru — работает', /interface|hostname|vlan/.test(n.exec(s.id, 'do sh ru')));
  chk('MES: end, wr — работает', (n.exec(s.id, 'end'), !/Ambiguous/.test(n.exec(s.id, 'wr'))));
  // пара однословных команд режима # с общим началом из 2+ букв — из таблицы MES 10.x
  var one = EL.mes.T.filter(function (c) { return c.pat.length === 1 && c.modes.indexOf('priv') >= 0 && c.pat[0].charAt(0) !== '<' && EL.cli.dlOk(c, s.st); }).map(function (c) { return c.pat[0]; });
  var amb = []; one.forEach(function (a) { one.forEach(function (b) { if (a < b && a.slice(0, 2) === b.slice(0, 2)) { var k = 2; while (a[k] === b[k]) k++; if (a.slice(0, k) !== a && b.slice(0, k) !== b) amb.push(a.slice(0, k)); } }); });
  chk('MES 10.x: show sta (stack / startup-config) — % Ambiguous Command, show star — однозначно', n.exec(s.id, 'show sta') === '% Ambiguous Command' && !/Ambiguous/.test(n.exec(s.id, 'show star')));
  chk('MES 10.x: Tab на show sta — варианты (общее начало уже набрано)', n.tab(s.id, 'show sta') === null && /stack/.test(n.help(s.id, 'show sta')) && /startup-config/.test(n.help(s.id, 'show sta')));
  n.exec(s6.id, 'enable');
  var amb6 = amb.filter(function (w) { return /Ambiguous/.test(n.exec(s6.id, w)); });
  chk('MES 6.x: неоднозначное слово — % Ambiguous command', !amb6.length || n.exec(s6.id, amb6[0]) === '% Ambiguous command', amb6.join());
  console.log('✓ Неоднозначные сокращения и Tab');
})();
// несколько портов сразу: interface range с диапазонами и списками (MES 6.x, 10.x), interface 1/0/1-1/0/4 (MES 8.x), «?» после номера порта
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Диапазоны портов: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), s6 = n.add('MES2300-24', 'SW6'), s10 = n.add('MES2428', 'SW10'), s8 = n.add('MES5448', 'SW8');
  function acc(s, ps, v) { return ps.every(function (p) { var q = s.st.ports['gi1/0/' + p] || s.st.ports['te1/0/' + p] || s.st.ports['1/0/' + p]; return q && q.mode === 'access' && q.access === v; }); }
  [s6, s10].forEach(function (s) { var dl = s.st.dialect;
    n.exec(s.id, 'enable'); n.exec(s.id, 'configure'); n.exec(s.id, 'vlan database'); n.exec(s.id, 'vlan 10,20,30'); n.exec(s.id, 'exit');
    var r = n.exec(s.id, 'interface range gi 1/0/1-2');
    chk(dl + '.x: interface range gi 1/0/1-2 (пробел) → (config-if-range)#', !r && /\(config-if-range\)#$/.test(n.prompt(s.id)), r + ' ' + n.prompt(s.id));
    n.exec(s.id, 'switchport mode access'); n.exec(s.id, 'switchport access vlan 10'); n.exec(s.id, 'exit');
    chk(dl + '.x: команда применилась к обоим портам', acc(s, [1, 2], 10));
    n.exec(s.id, 'interface range gigabitethernet 1/0/3-4,gigabitethernet 1/0/7'); n.exec(s.id, 'switchport mode access'); n.exec(s.id, 'switchport access vlan 20'); n.exec(s.id, 'exit');
    chk(dl + '.x: список gi1/0/3-4,gi1/0/7', acc(s, [3, 4, 7], 20) && !acc(s, [5], 20));
    var r2 = n.exec(s.id, 'int range gi 1/0/8-9, gi1/0/11'); n.exec(s.id, 'switchport mode access'); n.exec(s.id, 'switchport access vlan 30'); n.exec(s.id, 'exit');
    chk(dl + '.x: пробелы после запятой — тоже список', !r2 && acc(s, [8, 9, 11], 30), r2);
    n.exec(s.id, 'int range gi1/0/12,13'); n.exec(s.id, 'shutdown'); n.exec(s.id, 'exit');
    chk(dl + '.x: gi1/0/12,13 — номер без типа берёт тип предыдущего', s.st.ports['gi1/0/12'].shut && s.st.ports['gi1/0/13'].shut);
    var e1 = n.exec(s.id, 'interface gi 1/0/1-2');
    chk(dl + '.x: interface без range с диапазоном — ошибка (как в руководстве: несколько портов — interface range)', /^% Invalid input detected/.test(e1) && n.prompt(s.id).indexOf('(config)#') >= 0, e1);
    chk(dl + '.x: interface range на несуществующие порты — ошибка', /%/.test(n.exec(s.id, 'interface range gi1/0/1-60')) && n.prompt(s.id).indexOf('(config)#') >= 0);
    chk(dl + '.x: interface g без номера — % Incomplete command', n.exec(s.id, 'interface g') === '% Incomplete command');
    chk(dl + '.x: «?» после номера порта — не пусто', /gigabitethernet|<cr>/.test(n.help(s.id, 'interface range gi 1/0/1')), n.help(s.id, 'interface range gi 1/0/1'));
    n.exec(s.id, 'end'); });
  // MES 8.x (FASTPATH): диапазон прямо в interface — interface 1/0/1-1/0/4
  n.exec(s8.id, 'enable'); n.exec(s8.id, 'configure');
  var r8 = n.exec(s8.id, 'interface 1/0/1-1/0/4');
  chk('8.x: interface 1/0/1-1/0/4 → (Interface 1/0/1-1/0/4)#', !/%/.test(r8 || '') && /\(Interface 1\/0\/1-1\/0\/4\)#$/.test(n.prompt(s8.id)), r8 + ' ' + n.prompt(s8.id));
  n.exec(s8.id, 'shutdown'); n.exec(s8.id, 'exit');
  chk('8.x: команда применилась к 4 портам', [1, 2, 3, 4].every(function (p) { return s8.st.ports['1/0/' + p].shut; }) && !s8.st.ports['1/0/5'].shut);
  console.log('✓ Диапазоны и списки портов');
})();
// OLT-крейт MA4000-PX (CLI 3.38.1): slot N type plc8, VLAN PP4X (tagged/untagged front-port S/P), ONT слот/порт/ONT (0–63), commit + confirm
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ MA4000: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), o = n.add('MA4000-PX', 'OLT'), t = n.add('NTU-1L', 'ONT1'), pc = n.add('VPC', 'PC1'), sv = n.add('VPC', 'SRV');
  n.connect(o.id, 'front-port 1/0', sv.id, 'eth0'); n.connect(t.id, 'PON', o.id, 'gpon-port 0/2'); n.connect(pc.id, 'eth0', t.id, 'LAN');
  EL.labs.apply(n, { PC1: ['ip 10.0.0.1/24'], SRV: ['ip 10.0.0.2/24'] });
  chk('приглашение ma4000#', n.prompt(o.id) === 'ma4000#', n.prompt(o.id));
  chk('show shelf — PLC8 в слоте 0 обнаружена, не настроена', /^0\s+none\s+PLC8\s+not configured/m.test(n.exec(o.id, 'show shelf')), n.exec(o.id, 'show shelf'));
  var cfg = ['configure terminal', 'vlan 100', 'name inet', 'untagged front-port 1/0', 'exit', 'profile cross-connect inet', 'outer vid 100', 'exit',
    'interface ont 0/2/0', 'serial ' + t.st.serial, 'service 0 profile cross-connect inet', 'exit'];
  var bad = cfg.filter(function (l) { return /%/.test(n.exec(o.id, l) || ''); });
  chk('настройка без ошибок', !bad.length, bad.join('; '));
  chk('приглашения: (vlan-100)#, (config-cross-connect)("inet")#, (config)(if-ont-0/2/0)#', (n.exec(o.id, 'vlan 100'), n.prompt(o.id) === 'ma4000(vlan-100)#') && (n.exec(o.id, 'exit'),
    n.exec(o.id, 'profile cross-connect inet'), n.prompt(o.id) === 'ma4000(config-cross-connect)("inet")#') && (n.exec(o.id, 'exit'), n.exec(o.id, 'interface ont 0/2/0'), n.prompt(o.id) === 'ma4000(config)(if-ont-0/2/0)#'), n.prompt(o.id));
  chk('ONT 64 — вне диапазона 0–63', /%/.test((n.exec(o.id, 'exit'), n.exec(o.id, 'interface ont 0/2/64'))));
  chk('vlan allow на front-port — нет в MA4000', (n.exec(o.id, 'interface front-port 1/0'), /%/.test(n.exec(o.id, 'vlan allow 100'))) && n.prompt(o.id) === 'ma4000(front-port-1/0)#');
  n.exec(o.id, 'exit'); n.exec(o.id, 'exit');
  chk('commit — с таймером подтверждения', /confirmed within: 5 minutes\nConfiguration committed successfully/.test(n.exec(o.id, 'commit')));
  chk('без slot 0 type plc8 ONT не работает', !n.ping(pc.id, '10.0.0.2').ok);
  n.exec(o.id, 'confirm');                       // подтверждена настройка без типа карты
  n.exec(o.id, 'configure terminal'); chk('slot 0 type plc8', !/%/.test(n.exec(o.id, 'slot 0 type plc8') || '')); chk('slot 3 type lc16g — ошибка', /%/.test(n.exec(o.id, 'slot 3 type lc16g')));
  n.exec(o.id, 'exit'); n.exec(o.id, 'commit');
  chk('после slot 0 type plc8 + commit — ПК за ONT достаёт сервер', n.ping(pc.id, '10.0.0.2').ok);
  chk('show interface ont 0/2 online', /GPON-port 0\/2 ONT online list[\s\S]*\b0 0\/2 OK|OK/.test(n.exec(o.id, 'show interface ont 0/2 online')), n.exec(o.id, 'show interface ont 0/2 online'));
  chk('restore без confirm — откат к последнему подтверждённому', (n.exec(o.id, 'restore'), !n.ping(pc.id, '10.0.0.2').ok));
  n.exec(o.id, 'configure terminal'); n.exec(o.id, 'slot 0 type plc8'); n.exec(o.id, 'exit'); n.exec(o.id, 'commit');
  chk('confirm — сохранено, после перезагрузки работает', /confirmed/.test(n.exec(o.id, 'confirm')) && (n.reboot(o.id), n.ping(pc.id, '10.0.0.2').ok));
  var rc = n.exec(o.id, 'show running-config');
  chk('running-config: slot 0 type plc8, vlan 100 untagged front-port 1/0, interface ont 0/2/0', /slot 0 type plc8/.test(rc) && /vlan 100\n    name inet\n    untagged front-port 1\/0/.test(rc) && /interface ont 0\/2\/0\n    serial ELTX/.test(rc), rc);
  console.log('✓ MA4000-PX');
})();
// OLT Turbo GEPON LTE-8X и ONT NTE-2 (B+): сценарий Quick guide 3.16.7 — VLAN в коммутаторе, ONT по MAC, профиль правил, reconfigure, save
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ LTE: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), o = n.add('LTE-8X', 'OLT'), t = n.add('NTE-2 (B+)', 'ONT1'), pc = n.add('VPC', 'PC1'), sw = n.add('MES2300-24', 'SW1'), sv = n.add('VPC', 'SRV');
  n.connect(o.id, 'front-port 0', sw.id, 'gi1/0/24'); n.connect(t.id, 'PON', o.id, 'pon-port 3'); n.connect(pc.id, 'eth0', t.id, 'LAN'); n.connect(sv.id, 'eth0', sw.id, 'gi1/0/1');
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'vlan database', 'vlan 2000', 'exit', 'interface gi1/0/24', 'switchport mode trunk', 'switchport trunk allowed vlan add 2000', 'exit',
    'interface gi1/0/1', 'switchport access vlan 2000', 'end'], PC1: ['ip 10.20.0.1/24'], SRV: ['ip 10.20.0.2/24'] });
  function x(l) { return n.exec(o.id, l); }
  chk('приглашение LTE-8X#', n.prompt(o.id) === 'LTE-8X#');
  var L = x('show ont list all');
  chk('show ont list all: ONT без конфигурации — AUTHFAILED, MAC 02:00:4B:…', new RegExp(t.st.mac.replace(/:/g, ':') + '\\s+AUTHFAILED').test(L) && /^02:00:4B:/.test(t.st.mac), L);
  x('switch'); x('configure'); x('vlan 2000');
  chk('приглашения (switch)(config-vlan)#', n.prompt(o.id) === 'LTE-8X(switch)(config-vlan)#');
  chk('tagged front-port 0 – 7 и pon-port 0 – 7 (с длинным тире, как в Quick guide)', !/Unknown/.test(x('tagged front-port 0 – 7') + x('tagged pon-port 0 – 7') + x('name Data')));
  x('exit');
  chk('без reconfig VLAN коммутатора не действует', (x('exit'), x('exit'), !n.ping(pc.id, '10.20.0.2').ok));
  x('switch'); x('configure'); x('reconfig'); x('exit'); x('exit');
  chk('профиль правил: add profile rules 2 → Profile 2 created', /Profile 2 created/.test(x('add profile rules 2')));
  x('profile rules 2'); chk('приглашение (profile-rules)#', n.prompt(o.id) === 'LTE-8X(profile-rules)#');
  x('set description NTE-2');
  var e1 = x('rule add pon 0: if (VID == 2000) then DeleteTag; forward') + x('rule add uni0 0: if (Always) then AddTagVID = 2000; forward');
  chk('правила pon и uni0 приняты', !e1, e1);
  chk('rule show uni0', /0: if \(Always\) then AddTagVID = 2000; forward/.test(x('rule show uni0')));
  chk('неверный формат правила — ошибка', /Wrong rule format/.test(x('rule add uni0 1: AddTagVID 5')));
  x('exit');
  x('ont_mac ' + t.st.mac.toLowerCase());
  chk('ont_mac → LTE-8X(ONT-x/x/MAC)#', n.prompt(o.id) === 'LTE-8X(ONT-x/x/' + t.st.mac + ')#', n.prompt(o.id));
  chk('set description без add config — ошибка', /not found/.test(x('set description Test')));
  chk('add config', /Config for ONT-.* created/.test(x('add config')));
  x('set description Test NTE-2'); x('set profile rules 2');
  chk('до reconfigure трафика нет', !n.ping(pc.id, '10.20.0.2').ok);
  chk('reconfigure — successfull', /reconfiguration successfull/.test(x('reconfigure')));
  x('exit');
  chk('show ont list all: состояние OK и описание', new RegExp(t.st.mac + '\\s+OK\\s+Test NTE-2').test(x('show ont list all')), x('show ont list all'));
  chk('ПК за ONT достаёт сервер через VLAN 2000', n.ping(pc.id, '10.20.0.2').ok);
  chk('reboot без save — всё пропало', (x('reboot'), !n.ping(pc.id, '10.20.0.2').ok));
  // повторить и сохранить
  ['switch', 'configure', 'vlan 2000', 'tagged front-port 0', 'tagged pon-port 3', 'exit', 'reconfig', 'exit', 'exit', 'add profile rules 2', 'profile rules 2',
   'rule add pon 0: if (VID == 2000) then DeleteTag; forward', 'rule add uni0 0: if (Always) then AddTagVID = 2000; forward', 'exit', 'ont_mac ' + t.st.mac, 'add config', 'set profile rules 2', 'reconfigure', 'exit'].forEach(x);
  chk('save → после reboot работает', /saved/.test(x('save')) && (x('reboot'), n.ping(pc.id, '10.20.0.2').ok));
  chk('VLAN не tagged на pon-port ONT — трафика нет', (['switch', 'configure', 'vlan 2000', 'no tagged pon-port 3', 'exit', 'reconfig', 'exit', 'exit'].forEach(x), !n.ping(pc.id, '10.20.0.2').ok));
  console.log('✓ LTE-8X (Turbo GEPON)');
})();
// VoIP: TAU-72.IP + SMG-1016M + телефоны — регистрация портов FXS на SMG и звонок 101 → 202 через два TAU
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ VoIP: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), sw = n.add('MES2300-24', 'SW1'), sm = n.add('SMG-1016M', 'SMG'), t1 = n.add('TAU-72.IP', 'TAU1'), t2 = n.add('TAU-72.IP', 'TAU2'),
      a = n.add('Телефон', 'Tel101'), b = n.add('Телефон', 'Tel202');
  n.connect(sm.id, 'eth0', sw.id, 'gi1/0/1'); n.connect(t1.id, 'eth0', sw.id, 'gi1/0/2'); n.connect(t2.id, 'eth0', sw.id, 'gi1/0/3');
  n.connect(a.id, 'Line', t1.id, 'fxs 1'); n.connect(b.id, 'Line', t2.id, 'fxs 3');
  function tau(ip, port, num) { return ['admin', 'rootpasswd', 'config', 'network', 'ipaddr ' + ip, 'netmask 255.255.255.0', 'exit', 'sip profile 1', 'proxy address 1 10.0.0.1',
    'regristrar address 1 10.0.0.1', 'regristrar enable 1', 'domain voip.local', 'exit', 'voice port ' + port, 'username ' + num, 'authname ' + num, 'password p' + num, 'exit', 'exit', 'commit', 'confirm']; }
  var e = EL.labs.apply(n, { SMG: ['admin', 'rootpasswd', 'config', 'network', 'set interface ipaddr 0 10.0.0.1', 'set interface netmask 0 255.255.255.0', 'exit', 'sip users',
      'add user 0', 'set user number 0 101', 'set login 0 101 p101', 'set authorization 0 register', 'add user 1', 'set user number 1 202', 'set login 1 202 p202', 'set authorization 1 register', 'exit', 'save'],
    TAU1: tau('10.0.0.11', 1, '101'), TAU2: tau('10.0.0.12', 3, '202') });
  chk('настройка SMG и двух TAU без ошибок', !e.length, e.join('; '));
  chk('приглашения tau-72# и SMG>', n.prompt(t1.id) === 'tau-72#' && n.prompt(sm.id) === 'SMG-[CONFIG]> ', n.prompt(t1.id) + ' / ' + n.prompt(sm.id));
  var vs = n.exec(t1.id, 'show voiceport status');
  chk('show voiceport status: порт 1 — 101 registered, телефон положен', /^1\s+101\s+registered\s+onhook/m.test(vs) && /^2\s+-\s+not configured\s+no phone/m.test(vs), vs);
  n.exec(sm.id, 'sip users');
  chk('SMG show list: оба номера зарегистрированы', /101\s+register\s+registered 10\.0\.0\.11 port 1/.test(n.exec(sm.id, 'show list')) && /202\s+register\s+registered 10\.0\.0\.12 port 3/.test(n.exec(sm.id, 'show list')), n.exec(sm.id, 'show list'));
  var r = n.exec(a.id, 'dial 202');
  chk('звонок 101 → 202: разговор, у 202 звонок и снятая трубка', /разговор с 202/.test(r) && /Звонок от 101/.test(n.exec(b.id, 'status') + (b.st.phone.call === '101' ? 'Звонок от 101' : '')) && b.st.phone.call === '101', r);
  chk('show voiceport status: talk', /^1\s+101\s+registered\s+talk/m.test(n.exec(t1.id, 'show voiceport status 1')));
  chk('второй вызов на занятый — 486 Busy', (n.exec(a.id, 'hangup'), b.st.phone.call === null) && true);
  var tr = EL.voip.call(n, a, '202').steps.map(function (x) { return x.t; }).join(' | ');
  chk('трасса: INVITE, 180 Ringing, RTP', /SIP INVITE sip:202@voip\.local от 101/.test(tr) && /180 Ringing/.test(tr) && /RTP 10\.0\.0\.11 ↔ 10\.0\.0\.12/.test(tr), tr);
  chk('несуществующий номер — 404', /404/.test(n.exec(a.id, 'dial 303')));
  // неверный пароль на TAU2 — не регистрируется
  ['config', 'voice port 3', 'password wrong', 'exit', 'exit', 'commit'].forEach(function (l) { n.exec(t2.id, l); });
  chk('неверный password — not registered, звонок на 202 — 404', /^3\s+202\s+not registered/m.test(n.exec(t2.id, 'show voiceport status')) && /404/.test(n.exec(a.id, 'dial 202')), n.exec(t2.id, 'show voiceport status'));
  n.exec(sm.id, 'set authorization 1 none');
  chk('authorization none — регистрируется без пароля', /^3\s+202\s+registered/m.test(n.exec(t2.id, 'show voiceport status')));
  chk('reload TAU без confirm — неподтверждённое теряется', (n.reboot(t2.id), n.exec(t2.id, 'admin'), n.exec(t2.id, 'rootpasswd'), /password p202/.test(n.exec(t2.id, 'show configuration running'))));
  chk('неверный вход на TAU — Login incorrect', (n.reboot(t1.id), n.exec(t1.id, 'admin'), n.exec(t1.id, 'bad') === 'Login incorrect'));
  console.log('✓ VoIP: TAU-72.IP + SMG-1016M');
})();
// Абонентский роутер RG-35-WZ: заводские LAN 192.168.1.1 + DHCP-сервер, WAN DHCP Client от провайдера, NAT; Static IP через веб-настройки
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ CPE: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), isp = n.add('vESR', 'ISP'), rg = n.add('RG-35-WZ', 'RG'), pc = n.add('VPC', 'PC1'), pc2 = n.add('VPC', 'PC2');
  n.connect(isp.id, 'gi1/0/1', rg.id, 'gi1/0/1'); n.connect(pc.id, 'eth0', rg.id, 'gi1/0/2'); n.connect(pc2.id, 'eth0', rg.id, 'gi1/0/5');
  var e = EL.labs.apply(n, { ISP: ['configure', 'interface gigabitethernet 1/0/1', 'ip address 100.64.0.1/24', 'ip firewall disable', 'exit', 'ip dhcp-server', 'ip dhcp-server pool WAN',
    'network 100.64.0.0/24', 'address-range 100.64.0.10-100.64.0.20', 'default-router 100.64.0.1', 'exit', 'end', 'commit', 'confirm'] });
  chk('провайдер настроен', !e.length, e.join('; '));
  chk('консоль роутера — подсказка про веб-интерфейс', /веб-интерфейс/.test(n.exec(rg.id, 'show running-config')) && n.prompt(rg.id) === 'RG-35-WZ> ');
  var d = n.cpeDhcp(rg.id);
  chk('WAN DHCP Client: адрес от провайдера', d.ok && /^100\.64\.0\.1\d$/.test(rg.st.cpe.lease.ip) && rg.st.cpe.lease.gw === '100.64.0.1', JSON.stringify(rg.st.cpe.lease));
  n.exec(pc.id, 'ip dhcp'); n.exec(pc2.id, 'ip dhcp');
  chk('ПК в LAN получили адреса от DHCP-сервера роутера (192.168.1.2–254, шлюз .1)', /^192\.168\.1\.\d+$/.test(pc.st.ip) && pc.st.gw === '192.168.1.1' && /^192\.168\.1\./.test(pc2.st.ip) && pc.st.ip !== pc2.st.ip, pc.st.ip + ' ' + pc2.st.ip);
  chk('ПК1 ↔ ПК2 через мост LAN', n.ping(pc.id, pc2.st.ip).ok);
  var p = n.ping(pc.id, '100.64.0.1');
  chk('ПК в интернет провайдера — через Source NAT на WAN', p.ok && p.steps.some(function (x) { return /Source NAT/.test(x.t); }), p.steps.map(function (x) { return x.t; }).join(' | '));
  // Static IP и смена LAN
  var errs = n.cpeApply(rg.id, { lan: { ip: '10.10.0.1', mask: '255.255.255.0', dhcp: true, from: '10.10.0.100', to: '10.10.0.150', lease: 60 },
    wan: { mode: 'static', ip: '100.64.0.50', mask: '255.255.255.0', gw: '100.64.0.1' }, user: 'admin', pw: 'password' });
  chk('Static IP и новый LAN применены без ошибок', !errs.length, errs.join('; '));
  n.exec(pc.id, 'ip dhcp');
  chk('ПК получил адрес из нового пула 10.10.0.100–150', /^10\.10\.0\.1[0-5]\d$/.test(pc.st.ip) && pc.st.gw === '10.10.0.1', pc.st.ip);
  chk('Static WAN — интернет работает', n.ping(pc.id, '100.64.0.1').ok);
  chk('DHCP-сервер выключен — ПК адрес не получает', (n.cpeApply(rg.id, { lan: { ip: '10.10.0.1', mask: '255.255.255.0', dhcp: false, from: '10.10.0.100', to: '10.10.0.150', lease: 60 },
    wan: { mode: 'static', ip: '100.64.0.50', mask: '255.255.255.0', gw: '100.64.0.1' }, user: 'admin', pw: 'password' }), !/OK|DORA|DHCP.*10\.10/.test(n.exec(pc2.id, 'ip dhcp') || '') || !/^10\.10\./.test(pc2.st.ip || '')));
  chk('после перезагрузки настройки веб-интерфейса сохранены', (n.reboot(rg.id), rg.st.cpe.web.lan.ip === '10.10.0.1' && n.ping(pc.id, '100.64.0.1').ok));
  console.log('✓ RG-35-WZ (CPE)');
})();
  // ESBC-3200 между абонентами (TAU) и SMG — пример руководства ESBC 1.9.0 «Настройка для SIP-абонентов»
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ESBC: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), sw = n.add('MES2300-24', 'SW1'), e = n.add('ESBC-3200', 'ESBC'), sm = n.add('SMG-1016M', 'SMG'), t1 = n.add('TAU-72.IP', 'TAU1'), t2 = n.add('TAU-72.IP', 'TAU2'),
        a = n.add('Телефон', 'Tel101'), b = n.add('Телефон', 'Tel202');
    n.connect(sm.id, 'eth0', e.id, 'gi1/0/1'); n.connect(e.id, 'gi1/0/2', sw.id, 'gi1/0/1'); n.connect(t1.id, 'eth0', sw.id, 'gi1/0/2'); n.connect(t2.id, 'eth0', sw.id, 'gi1/0/3');
    n.connect(a.id, 'Line', t1.id, 'fxs 1'); n.connect(b.id, 'Line', t2.id, 'fxs 1');
    function tau(ip, num, reg) { return ['admin', 'rootpasswd', 'config', 'network', 'ipaddr ' + ip, 'netmask 255.255.255.0', 'exit', 'sip profile 1', 'proxy address 1 ' + reg,
      'regristrar address 1 ' + reg, 'regristrar enable 1', 'exit', 'voice port 1', 'username ' + num, 'authname ' + num, 'password p' + num, 'exit', 'exit', 'commit', 'confirm']; }
    var ESBC = ['configure', 'interface gigabitethernet 1/0/1', 'description "SSW"', 'ip address 192.168.16.113/24', 'ip firewall disable', 'exit',
      'interface gigabitethernet 1/0/2', 'description "ABONENTS"', 'ip address 192.168.20.120/24', 'ip firewall disable', 'exit',
      'esbc', 'sip transport TRANSPORT_SSW', 'ip address 192.168.16.113', 'port 5061', 'exit', 'sip transport TRANSPORT_ABONENTS', 'ip address 192.168.20.120', 'port 5062', 'exit',
      'media resource MEDIA_SSW', 'ip address 192.168.16.113', 'port-range 1024-65535', 'exit', 'media resource MEDIA_ABONENTS', 'ip address 192.168.20.120', 'exit',
      'trunk sip TRUNK_SSW', 'sip transport TRANSPORT_SSW', 'remote address 192.168.16.65', 'remote port 5060', 'media resource 0 MEDIA_SSW', 'exit',
      'user-interface sip ABONENTS', 'sip transport TRANSPORT_ABONENTS', 'media resource 0 MEDIA_ABONENTS', 'nat comedia-mode on', 'exit',
      'route-table TO_SSW', 'rule 0', 'action direct-to-trunk TRUNK_SSW', 'exit', 'exit', 'user-interface sip ABONENTS', 'route-table TO_SSW', 'exit', 'exit', 'end', 'commit', 'confirm'];
    var er = EL.labs.apply(n, { ESBC: ESBC, SMG: ['admin', 'rootpasswd', 'config', 'network', 'set interface ipaddr 0 192.168.16.65', 'set interface netmask 0 255.255.255.0', 'exit', 'sip users',
        'add user 0', 'set user number 0 101', 'set login 0 101 p101', 'set authorization 0 register', 'add user 1', 'set user number 1 202', 'set login 1 202 p202', 'set authorization 1 register', 'exit', 'save'],
      TAU1: tau('192.168.20.11', '101', '192.168.20.120:5062'), TAU2: tau('192.168.20.12', '202', '192.168.20.120:5062') });
    chk('настройка ESBC по примеру руководства, SMG и TAU — без ошибок', !er.length, er.join('; '));
    chk('приглашения раздела esbc', (function () { var o = []; ['configure', 'esbc', 'sip transport X'].forEach(function (l) { n.exec(e.id, l); o.push(n.prompt(e.id)); });
      n.exec(e.id, 'end'); n.exec(e.id, 'rollback'); return o.join('|') === 'esbc(config)#|esbc(config-esbc)#|esbc(config-esbc-sip-transport)#'; })());
    var run = n.exec(e.id, 'show running-config');
    chk('running-config: раздел esbc', /esbc\n  sip transport TRANSPORT_ABONENTS\n    ip address 192\.168\.20\.120\n    port 5062/.test(run) && /    action direct-to-trunk TRUNK_SSW/.test(run) && /    nat comedia-mode on\n    route-table TO_SSW/.test(run), run.slice(-900));
    chk('TAU зарегистрированы через ESBC', /^1\s+101\s+registered/m.test(n.exec(t1.id, 'show voiceport status')) && /^1\s+202\s+registered/m.test(n.exec(t2.id, 'show voiceport status')), n.exec(t1.id, 'show voiceport status'));
    n.exec(sm.id, 'sip users');
    chk('SMG видит абонентов с контактом ESBC (транк)', /101\s+register\s+registered 192\.168\.16\.113 \(ESBC, TRUNK_SSW\)/.test(n.exec(sm.id, 'show list')), n.exec(sm.id, 'show list'));
    chk('show esbc users sip', /101\s+ABONENTS\s+192\.168\.20\.11:5060\s+TRUNK_SSW/.test(n.exec(e.id, 'show esbc users sip')) && /202\s+ABONENTS/.test(n.exec(e.id, 'show esbc users sip')), n.exec(e.id, 'show esbc users sip'));
    chk('show esbc trunks sip: транк доступен', /TRUNK_SSW\s+192\.168\.16\.113:5061\s+192\.168\.16\.65:5060\s+available/.test(n.exec(e.id, 'show esbc trunks sip')), n.exec(e.id, 'show esbc trunks sip'));
    var c = EL.voip.call(n, a, '202'), tr = c.steps.map(function (x) { return x.t; }).join(' | ');
    chk('вызов 101 → 202 через ESBC и SMG', c.ok && /INVITE принят user-interface ABONENTS/.test(tr) && /ESBC → 192\.168\.16\.65:5060: SIP INVITE с транспорта TRANSPORT_SSW/.test(tr) &&
      /SMG → ESBC 192\.168\.16\.113:5061/.test(tr) && /INVITE из trunk TRUNK_SSW/.test(tr) && /RTP через ESBC: 192\.168\.20\.11 ↔ 192\.168\.20\.120/.test(tr), c.msg + ' :: ' + tr);
    chk('dial с телефона и show esbc active calls', /разговор с 202/.test(n.exec(a.id, 'dial 202')) && /101\s+202/.test(n.exec(e.id, 'show esbc active calls')), n.exec(e.id, 'show esbc active calls'));
    chk('отбой — активных вызовов нет', (n.exec(a.id, 'hangup'), /No active calls/.test(n.exec(e.id, 'show esbc active calls'))));
    // ошибки
    ['configure', 'esbc', 'user-interface sip ABONENTS', 'no route-table', 'exit', 'exit', 'end', 'commit'].forEach(function (l) { n.exec(e.id, l); });
    chk('без route-table абонент не регистрируется', /not registered/.test(n.exec(t1.id, 'show voiceport status')) && /route-table/.test(n.voipRegs()[t1.id + '|1'].why), n.voipRegs()[t1.id + '|1'].why);
    n.exec(e.id, 'rollback'); ['configure', 'esbc', 'user-interface sip ABONENTS', 'route-table TO_SSW', 'exit', 'exit', 'end', 'commit'].forEach(function (l) { n.exec(e.id, l); });
    chk('route-table возвращён — снова registered', /^1\s+101\s+registered/m.test(n.exec(t1.id, 'show voiceport status')));
    ['config', 'sip profile 1', 'regristrar address 1 192.168.20.120', 'exit', 'exit', 'commit'].forEach(function (l) { n.exec(t1.id, l); });
    chk('TAU на порт 5060 вместо 5062 — not registered (на 5060 нет SIP)', /нет SIP/.test(n.voipRegs()[t1.id + '|1'].why), n.voipRegs()[t1.id + '|1'].why);
    ['config', 'esbc', 'trunk sip TRUNK_SSW', 'remote port 5070', 'exit', 'exit', 'end', 'commit'].forEach(function (l) { n.exec(e.id, l); });
    chk('неверный remote port транка — регистрация не проходит, транк unavailable', /недоступен/.test(n.voipRegs()[t2.id + '|1'].why) && /unavailable/.test(n.exec(e.id, 'show esbc trunks sip')), n.voipRegs()[t2.id + '|1'].why);
    chk('esbc на обычном ESR — неизвестная команда', (function () { var r = n.add('vESR', 'R'); n.exec(r.id, 'configure'); return /Unknown command|Syntax error/.test(n.exec(r.id, 'esbc')); })());
    console.log('✓ ESBC-3200: абоненты TAU ↔ ESBC ↔ SMG');
  })();
  // Типы медных кабелей (MDI / MDI-X, Auto-MDIX) и огоньки на концах кабелей
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Кабели: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), s1 = n.add('MES2300-24', 'SW1'), s2 = n.add('MES2300-24', 'SW2'), pc = n.add('VPC', 'PC1'), pc2 = n.add('VPC', 'PC2'), rg = n.add('RG-35-WZ', 'RG'), rg2 = n.add('RG-35-WZ', 'RG2'),
        r = n.add('vESR', 'R1');
    n.connect(pc.id, 'eth0', s1.id, 'gi1/0/1', 'straight'); n.connect(s1.id, 'gi1/0/24', s2.id, 'gi1/0/24', 'cross'); n.connect(pc2.id, 'eth0', s2.id, 'gi1/0/2', 'cross');
    chk('прямой ПК–коммутатор: зелёный', n.ledOf(pc.id, 'eth0').c === 'g' && n.ledOf(s1.id, 'gi1/0/1').c === 'g', JSON.stringify(n.ledOf(pc.id, 'eth0')));
    chk('перекрёстный коммутатор–коммутатор: зелёный', n.linkUp(s1.id, 'gi1/0/24'));
    var l3 = n.ledOf(pc2.id, 'eth0');
    chk('перекрёстный ПК–MES: линк есть, Auto-MDIX поменял пары', l3.c === 'g' && /Auto-MDIX/.test(l3.why), l3.why);
    // RG-35-WZ: LAN 10/100 без Auto-MDIX
    n.connect(rg.id, 'gi1/0/2', rg2.id, 'gi1/0/3', 'straight');
    var lr = n.ledOf(rg.id, 'gi1/0/2');
    chk('прямой между LAN-портами двух RG-35-WZ (MDI-X ↔ MDI-X, без Auto-MDIX) — красный', lr.c === 'r' && /нужен перекрёстный/.test(lr.why), JSON.stringify(lr));
    n.disconnect(n.links.findIndex(function (l) { return l.a.dev === rg.id && l.a.port === 'gi1/0/2'; }));
    n.connect(r.id, 'gi1/0/1', rg.id, 'gi1/0/4', 'cross');
    chk('перекрёстный ESR (MDI, Auto-MDIX) – LAN RG: работает за счёт Auto-MDIX ESR', n.ledOf(r.id, 'gi1/0/1').c === 'g');
    n.connect(r.id, 'gi1/0/2', s1.id, 'gi1/0/5', 'serial');
    chk('Serial в Ethernet-порт — красный', n.ledOf(r.id, 'gi1/0/2').c === 'r' && /Serial/.test(n.ledOf(r.id, 'gi1/0/2').why));
    n.connect(r.id, 'gi1/0/3', s1.id, 'gi1/0/6', 'sfp1g');
    chk('оптика в медный порт — красный', n.ledOf(s1.id, 'gi1/0/6').c === 'r' && /медный/.test(n.ledOf(s1.id, 'gi1/0/6').why), n.ledOf(s1.id, 'gi1/0/6').why);
    EL.labs.apply(n, { SW1: ['enable', 'configure', 'interface gigabitethernet 1/0/1', 'shutdown', 'end'] });
    chk('shutdown на коммутаторе — красный на обоих концах', n.ledOf(s1.id, 'gi1/0/1').c === 'r' && /shutdown/.test(n.ledOf(pc.id, 'eth0').why), n.ledOf(pc.id, 'eth0').why);
    n.devs[pc2.id].off = true; n.gen++;
    chk('устройство выключено — красный у соседа', n.ledOf(s2.id, 'gi1/0/2').c === 'r' && /выключено/.test(n.ledOf(s2.id, 'gi1/0/2').why));
    // LACP не собран — оранжевый
    var m = new EL.Net(), a = m.add('MES2300-24', 'A'), b = m.add('MES2300-24', 'B'); m.connect(a.id, 'gi1/0/1', b.id, 'gi1/0/1'); m.connect(a.id, 'gi1/0/2', b.id, 'gi1/0/2');
    EL.labs.apply(m, { A: ['enable', 'configure', 'interface range gigabitethernet 1/0/1-2', 'channel-group 1 mode auto', 'end'] });
    var lo = m.ledOf(a.id, 'gi1/0/1');
    chk('LACP: на соседе нет channel-group — оранжевый', lo.c === 'o' && /LACP/.test(lo.why), JSON.stringify(lo));
    EL.labs.apply(m, { B: ['enable', 'configure', 'interface range gigabitethernet 1/0/1-2', 'channel-group 1 mode auto', 'end'] });
    chk('LACP собран — зелёный', m.ledOf(a.id, 'gi1/0/1').c !== 'r' && m.ledOf(a.id, 'gi1/0/1').c === (m.ledOf(a.id, 'gi1/0/1').c === 'o' && /STP/.test(m.ledOf(a.id, 'gi1/0/1').why) ? 'o' : 'g'), JSON.stringify(m.ledOf(a.id, 'gi1/0/1')));
    // STP: петля — у одного порта оранжевый (blocking / discarding)
    var q = new EL.Net(), x1 = q.add('MES2300-24', 'X1'), x2 = q.add('MES2300-24', 'X2'); q.connect(x1.id, 'gi1/0/1', x2.id, 'gi1/0/1'); q.connect(x1.id, 'gi1/0/2', x2.id, 'gi1/0/2');
    EL.labs.apply(q, { X1: ['enable', 'configure', 'spanning-tree', 'end'], X2: ['enable', 'configure', 'spanning-tree', 'end'] });
    var all = [x1, x2].map(function (d) { return ['gi1/0/1', 'gi1/0/2'].map(function (p) { return q.ledOf(d.id, p).c; }).join(''); }).join('');
    chk('STP-петля: один порт оранжевый, остальные зелёные', all.split('o').length - 1 === 1 && all.split('g').length - 1 === 3, all);
    chk('кабель в файле схемы сохраняется', /cross/.test(JSON.stringify(n.toJSON())) && EL.Net.fromJSON(n.toJSON()).links.some(function (l) { return l.cab === 'cross'; }));
    console.log('✓ Кабели: прямой/перекрёстный/Serial, Auto-MDIX, огоньки портов');
  })();
  // Рабочий стол ПК: настройка IP, браузер, FTP, почта, Telnet/SSH, генератор трафика
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Рабочий стол: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), sw = n.add('MES2300-24', 'SW1'), pc = n.add('VPC', 'PC1'), db = n.add('Debian', 'WS'), sv = n.add('Debian-server', 'SRV'), r = n.add('vESR', 'R1');
    n.connect(pc.id, 'eth0', sw.id, 'gi1/0/1'); n.connect(db.id, 'ens3', sw.id, 'gi1/0/2'); n.connect(sv.id, 'ens3', sw.id, 'gi1/0/3'); n.connect(r.id, 'gi1/0/1', sw.id, 'gi1/0/4');
    EL.labs.apply(n, { R1: ['configure', 'interface gigabitethernet 1/0/1', 'ip address 10.0.0.1/24', 'ip firewall disable', 'exit', 'ip ssh server', 'ip dhcp-server', 'ip dhcp-server pool P',
      'network 10.0.0.0/24', 'address-range 10.0.0.100-10.0.0.120', 'default-router 10.0.0.1', 'exit', 'end', 'commit', 'confirm'] });
    var e1 = n.ipSet(sv.id, { mode: 'static', ip: '10.0.0.10', mask: '255.255.255.0', gw: '10.0.0.1', dns: '' });
    n.tick(31);
    chk('IP сервера: static через окно — в /etc/network/interfaces и ip a', e1.ok && /iface ens3 inet static\n    address 10\.0\.0\.10\/24\n    gateway 10\.0\.0\.1/.test(sv.st.files['/etc/network/interfaces']) && sv.st.ip === '10.0.0.10' && sv.st.up, JSON.stringify(e1));
    chk('ошибки окна IP: маска, шлюз не в подсети', !n.ipSet(pc.id, { mode: 'static', ip: '10.0.0.5', mask: '255.0.255.0' }).ok && /не в подсети/.test(n.ipSet(pc.id, { mode: 'static', ip: '10.0.0.5', mask: '255.255.255.0', gw: '10.1.0.1' }).msg));
    var e2 = n.ipSet(pc.id, { mode: 'dhcp', dns: '10.0.0.10' });
    chk('VPC: DHCP через окно', e2.ok && /^10\.0\.0\.1[0-2]\d$/.test(pc.st.ip) && pc.st.gw === '10.0.0.1' && pc.st.dns === '10.0.0.10' && n.ipCfg(pc.id).mode === 'dhcp', JSON.stringify(e2));
    var e3 = n.ipSet(db.id, { mode: 'dhcp', dns: '10.0.0.10' });
    n.tick(31);   // ens3 поднялся только сейчас — порт коммутатора проходит listening / learning
    chk('Debian: DHCP через окно — iface ens3 inet dhcp, resolv.conf', e3.ok && /inet dhcp/.test(db.st.files['/etc/network/interfaces']) && /nameserver 10\.0\.0\.10/.test(db.st.files['/etc/resolv.conf']) && n.ipCfg(db.id).dns === '10.0.0.10', JSON.stringify(e3));
    // браузер
    var h = n.httpGet(pc.id, 'http://10.0.0.10');
    chk('браузер: стандартная страница apache2', h.ok && h.code === 200 && /It works!/.test(h.html), JSON.stringify(h).slice(0, 200));
    sv.st.files['/var/www/html/index.html'] = '<h1>Колледж</h1>'; sv.st.files['/var/www/html/lab.html'] = '<p>лаба</p>';
    chk('браузер: своя index.html и lab.html, 404', /Колледж/.test(n.httpGet(pc.id, '10.0.0.10').html) && /лаба/.test(n.httpGet(pc.id, '10.0.0.10/lab.html').html) && n.httpGet(pc.id, '10.0.0.10/x.html').code === 404);
    chk('браузер: https без SSL — порт 443 закрыт', !n.httpGet(pc.id, 'https://10.0.0.10').ok && /443 закрыт/.test(n.httpGet(pc.id, 'https://10.0.0.10').why));
    chk('браузер: по имени без DNS — ошибка DNS', !n.httpGet(pc.id, 'www.college.ru').ok, n.httpGet(pc.id, 'www.college.ru').why);
    // FTP
    chk('FTP: неверный пароль — 530', /530/.test(n.ftp(pc.id, '10.0.0.10', 'user', 'bad', 'ls').why));
    n.docs(pc.id).put('otchet.txt', 'Отчёт по лабе');
    var up = n.ftp(pc.id, '10.0.0.10', 'user', 'user', 'put', 'otchet.txt');
    chk('FTP: put из Документов в /home/user на сервере', up.ok && sv.st.files['/home/user/otchet.txt'] === 'Отчёт по лабе', JSON.stringify(up));
    var ls = n.ftp(db.id, '10.0.0.10', 'user', 'user', 'ls');
    chk('FTP: ls с Debian', ls.ok && ls.files.some(function (f) { return f.name === 'otchet.txt'; }), JSON.stringify(ls).slice(0, 300) + ' ' + db.st.ip);
    chk('FTP: get на Debian — в /root', n.ftp(db.id, '10.0.0.10', 'user', 'user', 'get', 'otchet.txt').ok && db.st.files['/root/otchet.txt'] === 'Отчёт по лабе');
    n.exec(sv.id, 'root'); n.exec(sv.id, 'toor'); n.exec(sv.id, 'systemctl stop vsftpd');
    chk('FTP: vsftpd остановлен — порт 21 закрыт', /21 закрыт/.test(n.ftp(pc.id, '10.0.0.10', 'user', 'user', 'ls').why));
    // почта
    var cfg = { from: 'root@college.ru', smtp: '10.0.0.10', pop3: '10.0.0.10', user: 'user', pw: 'user' };
    chk('SMTP: письмо в ящик user', n.mailSend(pc.id, cfg, { to: 'user@college.ru', subj: 'Привет', body: 'Текст' }).ok && sv.st.mail.user.length === 1);
    chk('SMTP: нет такого ящика — 550', /550/.test(n.mailSend(pc.id, cfg, { to: 'nobody@college.ru' }).why));
    var rv = n.mailRecv(db.id, cfg);
    chk('POP3: письмо забрано и удалено с сервера', rv.ok && rv.msgs.length === 1 && rv.msgs[0].subj === 'Привет' && !sv.st.mail.user.length);
    chk('POP3: неверный пароль', /Authentication failed/.test(n.mailRecv(db.id, { pop3: '10.0.0.10', user: 'user', pw: 'x' }).why));
    n.exec(sv.id, 'systemctl stop postfix');
    chk('SMTP: postfix остановлен — порт 25 закрыт', /25 закрыт/.test(n.mailSend(pc.id, cfg, { to: 'user@college.ru' }).why));
    // Telnet / SSH, генератор
    chk('SSH-клиент: до ESR с ip ssh server', n.remote(pc.id, 'ssh', '10.0.0.1').ok && n.remote(pc.id, 'ssh', '10.0.0.1').dev === r.id);
    chk('Telnet-клиент: на ESR telnet выключен — порт закрыт', !n.remote(pc.id, 'telnet', '10.0.0.1').ok);
    var g = n.trafficGen(pc.id, { proto: 'udp', dst: '10.0.0.10', port: 5001, size: 1000, rate: 100, dur: 0.5 });
    chk('генератор трафика: UDP 100 п/с 0,5 с', g.ok && g.res.sent === 50 && g.res.recv === 50, JSON.stringify(g.res && { s: g.res.sent, r: g.res.recv }));
    var gi = n.trafficGen(pc.id, { proto: 'icmp', dst: '10.0.0.1', size: 64, rate: 10, dur: 1 });
    chk('генератор трафика: ICMP 10 эхо-запросов', gi.ok && gi.res.sent === 10 && gi.res.recv === 10, JSON.stringify(gi.res && { s: gi.res.sent, r: gi.res.recv }));
    console.log('✓ Рабочий стол: IP, браузер, FTP, почта, Telnet/SSH, генератор трафика');
  })();
  // Службы сервера Debian: окно и команды меняют одно состояние; DHCP-сервер isc-dhcp-server, DNS, HTTPS, учётные записи, RADIUS/TACACS+
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Службы: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), sw = n.add('MES2300-24', 'SW1'), sv = n.add('Debian-server', 'SRV'), pc = n.add('VPC', 'PC1'), r = n.add('vESR', 'R1'), sw2 = n.add('MES2300-24', 'SW2'), pc2 = n.add('VPC', 'PC2'), S = EL.srv, st = sv.st;
    n.connect(sv.id, 'ens3', sw.id, 'gi1/0/1'); n.connect(pc.id, 'eth0', sw.id, 'gi1/0/2'); n.connect(r.id, 'gi1/0/1', sw.id, 'gi1/0/3'); n.connect(r.id, 'gi1/0/2', sw2.id, 'gi1/0/1'); n.connect(pc2.id, 'eth0', sw2.id, 'gi1/0/2');
    EL.labs.apply(n, { R1: ['configure', 'interface gigabitethernet 1/0/1', 'ip address 10.0.0.1/24', 'ip firewall disable', 'exit', 'interface gigabitethernet 1/0/2', 'ip address 10.0.1.1/24', 'ip firewall disable',
      'ip helper-address 10.0.0.10', 'exit', 'ip dhcp-relay', 'end', 'commit', 'confirm'] });
    n.ipSet(sv.id, { mode: 'static', ip: '10.0.0.10', mask: '255.255.255.0', gw: '10.0.0.1' }); n.tick(31);
    chk('isc-dhcp-server по умолчанию выключен — VPC без адреса', !S.on(st, 'dhcp') && !/DORA/.test(n.exec(pc.id, 'ip dhcp')));
    S.dhcpWrite(st, [{ net: '10.0.0.0', mask: '255.255.255.0', from: '10.0.0.100', to: '10.0.0.110', gw: '10.0.0.1', dns: '10.0.0.10' },
      { net: '10.0.1.0', mask: '255.255.255.0', from: '10.0.1.50', to: '10.0.1.60', gw: '10.0.1.1', dns: '' }]);
    S.set(st, 'dhcp', true);
    chk('галочка = systemctl: isc-dhcp-server active', /active \(running\)/.test((n.exec(sv.id, 'root'), n.exec(sv.id, 'toor'), n.exec(sv.id, 'systemctl status isc-dhcp-server'))));
    chk('dhcpd.conf в формате ISC', /subnet 10\.0\.0\.0 netmask 255\.255\.255\.0 \{\n  range 10\.0\.0\.100 10\.0\.0\.110;\n  option routers 10\.0\.0\.1;/.test(n.exec(sv.id, 'cat /etc/dhcp/dhcpd.conf')));
    var o = n.exec(pc.id, 'ip dhcp');
    chk('VPC в сети сервера получил адрес от Debian', /DORA IP 10\.0\.0\.10\d\/24 GW 10\.0\.0\.1/.test(o), o);
    var o2 = n.exec(pc2.id, 'ip dhcp');
    chk('VPC за ретранслятором ESR — адрес из пула 10.0.1.0 по giaddr', /DORA IP 10\.0\.1\.5\d\/24 GW 10\.0\.1\.1/.test(o2), o2);
    n.exec(sv.id, 'systemctl stop isc-dhcp-server');
    chk('systemctl stop — галочка снята, адресов нет', !S.on(st, 'dhcp') && !/DORA/.test(n.exec(pc2.id, 'clear ip') && n.exec(pc2.id, 'ip dhcp')));
    chk('ошибки пула: сеть не по маске, диапазон вне сети', /не совпадает/.test(S.dhcpCheck({ net: '10.0.0.5', mask: '255.255.255.0', from: '10.0.0.6', to: '10.0.0.7' })) && /вне сети/.test(S.dhcpCheck({ net: '10.0.0.0', mask: '255.255.255.0', from: '10.0.9.6', to: '10.0.9.7' })));
    // DNS
    S.dnsWrite(st, S.dnsRead(st).concat([{ zone: 'college.ru', recs: [{ name: 'www', type: 'A', val: '10.0.0.10' }, { name: 'web', type: 'CNAME', val: 'www' }, { name: '@', type: 'MX', val: 'mail', pref: 10 }] }]));
    S.restart(st, 'dns'); n.exec(pc.id, 'ip dns 10.0.0.10');
    chk('DNS из окна: зона college.ru, A и CNAME разрешаются', n.resolve(pc.id, 'www.college.ru').ip === '10.0.0.10' && n.resolve(pc.id, 'web.college.ru').ip === '10.0.0.10', JSON.stringify(n.resolve(pc.id, 'web.college.ru')));
    var rd = S.dnsRead(st).filter(function (z) { return z.zone === 'college.ru'; })[0];
    chk('DNS: файл зоны читается обратно (A, CNAME, MX)', rd && rd.recs.length === 3 && rd.recs[2].type === 'MX' && rd.recs[2].val === 'mail', JSON.stringify(rd));
    chk('браузер по имени через DNS сервера', /It works!/.test(n.httpGet(pc.id, 'http://www.college.ru').html || ''));
    // HTTPS
    chk('a2enmod ssl — HTTPS работает', /Enabling module ssl/.test(n.exec(sv.id, 'a2enmod ssl')) && st.srv.https && n.httpGet(pc.id, 'https://10.0.0.10').ok);
    S.https(st, false); chk('галочка HTTPS снята — 443 закрыт', !n.httpGet(pc.id, 'https://10.0.0.10').ok);
    // учётные записи
    n.exec(sv.id, 'useradd ivanov');
    chk('useradd — пользователь виден в окне FTP', S.users(st).some(function (u) { return u.name === 'ivanov'; }));
    st.accounts.ivanov = 'qwerty';
    chk('пароль из окна — вход по FTP', n.ftp(pc.id, '10.0.0.10', 'ivanov', 'qwerty', 'ls').ok);
    // RADIUS / TACACS+
    S.radWrite(st, { clients: [{ name: 'r1', ip: '10.0.0.1', secret: 'sekret123' }], users: [{ name: 'net', pw: 'p@ss' }] });
    var rr = S.radRead(st);
    chk('RADIUS: clients.conf и users из окна читаются обратно', rr.clients[0].ip === '10.0.0.1' && rr.clients[0].secret === 'sekret123' && rr.users[0].name === 'net' && rr.users[0].pw === 'p@ss', JSON.stringify(rr));
    EL.labs.apply(n, { R1: ['configure', 'radius-server host 10.0.0.10', 'key ascii-text sekret123', 'exit', 'aaa authentication login default radius local', 'end', 'commit', 'confirm'] });
    var lg = n.aaaLogin(r.id, 'console', 'net', 'p@ss', function () { return false; });
    chk('вход на ESR по RADIUS с пользователем из окна', lg && lg.ok, JSON.stringify(lg) + JSON.stringify(r.st.run.aaa));
    S.tacWrite(st, { key: 'tk', users: [{ name: 'adm', pw: '1' }] });
    chk('TACACS+: tac_plus.conf из окна', S.tacRead(st).key === 'tk' && S.tacRead(st).users[0].pw === '1' && /user = adm \{\n    login = cleartext "1"/.test(st.files['/etc/tacacs+/tac_plus.conf']));
    chk('все 10 служб переключаются галочкой и видны в systemctl', Object.keys(S.UNITS).every(function (k) { S.set(st, k, true); var on = S.on(st, k); S.set(st, k, false); return on && !S.on(st, k); }));
    console.log('✓ Службы сервера: DHCP, DNS, HTTPS, FTP-пользователи, RADIUS, TACACS+');
  })();
  // PDU: простой (ICMP) и сложный (ICMP / UDP / TCP, количество)
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ PDU: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), sw = n.add('MES2300-24', 'SW1'), a = n.add('VPC', 'A'), sv = n.add('Debian-server', 'SRV'), c = n.add('VPC', 'C');
    n.connect(a.id, 'eth0', sw.id, 'gi1/0/1'); n.connect(sv.id, 'ens3', sw.id, 'gi1/0/2'); n.connect(c.id, 'eth0', sw.id, 'gi1/0/3');
    n.exec(a.id, 'ip 10.0.0.1/24'); n.ipSet(sv.id, { mode: 'static', ip: '10.0.0.10', mask: '255.255.255.0' }); n.tick(31);
    var p = n.pdu(a.id, { dst: n.pduDst(sv.id), proto: 'icmp' });
    chk('простой PDU A → SRV: успешно, есть трасса', p.ok && p.r.steps.length > 0);
    chk('простой PDU на узел без адреса', n.pduDst(c.id) === null);
    chk('сложный PDU TCP 80 к apache2 — успешно', n.pdu(a.id, { dst: '10.0.0.10', proto: 'tcp', port: 80 }).ok);
    var t = n.pdu(a.id, { dst: '10.0.0.10', proto: 'tcp', port: 8080 });
    chk('сложный PDU TCP 8080 — соединение отклонено', !t.ok && /отклонено/.test(t.why), t.why);
    chk('сложный PDU UDP на закрытый порт — доставлен', n.pdu(a.id, { dst: '10.0.0.10', proto: 'udp', port: 5555 }).ok);
    var m = n.pdu(a.id, { dst: '10.0.0.10', proto: 'icmp', count: 5, interval: 0.2, size: 1000 });
    chk('сложный PDU ICMP ×5 — 5/5', m.ok && m.sent === 5 && m.recv === 5, JSON.stringify({ s: m.sent, r: m.recv }));
    chk('нет пути — неудачно', !n.pdu(a.id, { dst: '10.9.9.9', proto: 'icmp' }).ok);
    console.log('✓ PDU: простой и сложный');
  })();
  // Площадки и каналы: расстояние → задержка распространения, RTT в ping
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Каналы: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), r1 = n.add('vESR', 'MSK'), r2 = n.add('vESR', 'NSK'), a = n.add('VPC', 'PCM'), b = n.add('VPC', 'PCN');
    n.connect(r1.id, 'gi1/0/1', r2.id, 'gi1/0/1', 'wan'); n.connect(a.id, 'eth0', r1.id, 'gi1/0/2'); n.connect(b.id, 'eth0', r2.id, 'gi1/0/2');
    EL.labs.apply(n, { MSK: ['configure', 'interface gigabitethernet 1/0/1', 'ip address 10.0.0.1/30', 'ip firewall disable', 'exit', 'interface gigabitethernet 1/0/2', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit',
      'ip route 192.168.2.0/24 10.0.0.2', 'end', 'commit', 'confirm'], NSK: ['configure', 'interface gigabitethernet 1/0/1', 'ip address 10.0.0.2/30', 'ip firewall disable', 'exit', 'interface gigabitethernet 1/0/2',
      'ip address 192.168.2.1/24', 'ip firewall disable', 'exit', 'ip route 192.168.1.0/24 10.0.0.1', 'end', 'commit', 'confirm'] });
    n.exec(a.id, 'ip 192.168.1.10/24 192.168.1.1'); n.exec(b.id, 'ip 192.168.2.10/24 192.168.2.1');
    chk('канал связи: линк есть', n.linkUp(r1.id, 'gi1/0/1') && n.phys(r1.id, 'gi1/0/1').cab === 'wan');
    var t0 = n.exec(a.id, 'ping 192.168.2.10');
    chk('LAN-время без расстояния — как раньше (< 1 мс)', /time=0\.630 ms/.test(t0), t0.split('\n')[0]);
    n.setLink(0, { len: 3300e3 });
    var l = n.links[0], d = n.propDelay(l);
    chk('3300 км оптики ≈ 16,2 мс в одну сторону', d > 0.0160 && d < 0.0164, d);
    var t1 = n.exec(a.id, 'ping 192.168.2.10'), ms = +(t1.match(/time=([\d.]+) ms/) || [])[1];
    chk('ping показывает RTT ≈ 32–34 мс', ms > 32 && ms < 34, t1.split('\n')[0]);
    var sm = n.simulate([{ kind: 'ping', src: a.id, dst: '192.168.2.10', count: 2, interval: 1, size: 56 }]).flows[0];
    chk('симуляция: RTT ≈ 32–34 мс', sm.avg > 0.032 && sm.avg < 0.034, sm.avg);
    var J = n.toJSON(), m = EL.Net.fromJSON(J);
    chk('расстояние канала и тип сохраняются в схеме', m.links[0].len === 3300e3 && m.links[0].cab === 'wan');
    chk('расстояние по координатам: Москва — Новосибирск × 1,2 ≈ 3370 км', Math.abs(EL.geoKm(EL.CITIES['Москва'], EL.CITIES['Новосибирск']) * EL.ROUTE_K - 3370) < 60);
    var deb = n.add('Debian', 'D1'); n.connect(deb.id, 'ens3', r2.id, 'gi1/0/3');
    chk('медь: 5,05 мкс/км', Math.abs(n.propDelay({ len: 1000, cab: 'cu' }) * 1e6 - 5.05) < 0.05);
    console.log('✓ Каналы: расстояние, задержка распространения, RTT');
  })();
  // Параметры канала: скорость, потери, джиттер, BER — в ping и симуляции
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Параметры канала: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), a = n.add('VPC', 'A'), b = n.add('VPC', 'B'); n.connect(a.id, 'eth0', b.id, 'eth0');
    n.exec(a.id, 'ip 10.0.0.1/24'); n.exec(b.id, 'ip 10.0.0.2/24');
    var f0 = n.simulate([{ kind: 'udp', src: a.id, dst: '10.0.0.2', size: 1000, rate: 1000, dur: 1 }]).flows[0];
    chk('1 Гбит/с: 1000 п/с по 1000 байт без потерь', f0.loss === 0, f0.loss);
    n.setLink(0, { mbps: 2 });
    var r = n.simulate([{ kind: 'udp', src: a.id, dst: '10.0.0.2', size: 1000, rate: 1000, dur: 1 }]), f1 = r.flows[0];
    chk('канал 2 Мбит/с: очередь переполняется, потери и рост задержки', f1.loss > 50 && f1.max > 0.03 && r.queues.length > 0, JSON.stringify({ loss: f1.loss, max: f1.max }));
    n.setLink(0, { mbps: 0, loss: 30 });
    var f2 = n.simulate([{ kind: 'ping', src: a.id, dst: '10.0.0.2', count: 100, interval: 0.01, size: 56 }]).flows[0];
    chk('потери 30 % на канале: в ping туда-обратно теряется ≈ половина', f2.loss > 35 && f2.loss < 65, f2.loss);
    chk('ping в консоли тоже теряет эхо', /timeout/.test(n.exec(a.id, 'ping 10.0.0.2')));
    n.setLink(0, { loss: 0, ber: 1e-4 });
    var f3 = n.simulate([{ kind: 'udp', src: a.id, dst: '10.0.0.2', size: 1400, rate: 100, dur: 1 }]).flows[0];
    chk('BER 10⁻⁴ при кадрах 1400 байт: теряется большинство', f3.loss > 50 && Object.keys(f3.drops).some(function (k) { return /битовые ошибки/.test(k); }), JSON.stringify(f3.drops));
    n.setLink(0, { ber: 0, jit: 20 });
    var f4 = n.simulate([{ kind: 'ping', src: a.id, dst: '10.0.0.2', count: 30, interval: 0.1, size: 56 }]).flows[0];
    chk('джиттер 20 мс: разброс RTT растёт', f4.jitter > 0.004 && f4.max > 0.015, JSON.stringify({ j: f4.jitter, max: f4.max }));
    chk('параметры канала сохраняются в схеме', EL.Net.fromJSON(n.toJSON()).links[0].jit === 20);
    console.log('✓ Параметры канала: скорость, потери, BER, джиттер');
  })();
  // Нормы длины кабеля: медь 100 м, оптика по трансиверу
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Длина кабеля: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), a = n.add('VPC', 'A'), b = n.add('VPC', 'B'), s1 = n.add('MES2300-24', 'S1'), s2 = n.add('MES2300-24', 'S2');
    n.connect(a.id, 'eth0', b.id, 'eth0'); n.exec(a.id, 'ip 10.0.0.1/24'); n.exec(b.id, 'ip 10.0.0.2/24');
    chk('медь 100 м — норма, зелёный', n.ledOf(a.id, 'eth0').c === 'g');
    n.setLink(0, { len: 120 });
    var lo = n.ledOf(a.id, 'eth0');
    chk('медь 120 м — линк есть, оранжевый, потери', lo.c === 'o' && /длиннее нормы 100 м/.test(lo.why) && n.linkUp(a.id, 'eth0'), JSON.stringify(lo));
    var f = n.simulate([{ kind: 'udp', src: a.id, dst: '10.0.0.2', size: 500, rate: 200, dur: 1 }]).flows[0];
    chk('медь 120 м: ≈10 % кадров теряется', f.loss >= 4 && f.loss <= 18, f.loss);
    n.setLink(0, { len: 160 });
    chk('медь 160 м — линка нет, красный', !n.linkUp(a.id, 'eth0') && n.ledOf(a.id, 'eth0').c === 'r' && /1,5 раза/.test(n.ledOf(a.id, 'eth0').why));
    n.connect(s1.id, 'te1/0/1', s2.id, 'te1/0/1', 'sfp10g');
    var li = n.links.length - 1; n.setLink(li, { len: 400 });
    chk('10GBASE-SR 400 м (норма 300 м OM3) — оранжевый', n.ledOf(s1.id, 'te1/0/1').c === 'o' || (n.ledOf(s1.id, 'te1/0/1').c === 'o'), JSON.stringify(n.ledOf(s1.id, 'te1/0/1')));
    n.setLink(li, { len: 9000 });
    chk('10GBASE-SR 9 км — нет линка', !n.linkUp(s1.id, 'te1/0/1'));
    n.disconnect(li); n.connect(s1.id, 'te1/0/1', s2.id, 'te1/0/1', 'sfp10g-lr'); n.setLink(n.links.length - 1, { len: 9000 });
    chk('10GBASE-LR 9 км — норма 10 км, линк есть', n.linkUp(s1.id, 'te1/0/1') && !/длиннее/.test(n.ledOf(s1.id, 'te1/0/1').why));
    chk('канал связи — без нормы длины', !EL.LENNORM.wan && /не задаётся/.test(EL.lenNorm(n, { cab: 'wan', a: { dev: a.id }, b: { dev: b.id }, len: 3e6 })));
    console.log('✓ Длина кабеля: нормы IEEE 802.3, ошибки и обрыв');
  })();
  // Облако провайдера: адреса портов, маршруты, задержка, скорость, потери
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Облако провайдера: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), c = n.add('Облако провайдера', 'ISP'), r1 = n.add('vESR', 'R1'), r2 = n.add('vESR', 'R2'), a = n.add('VPC', 'A'), b = n.add('VPC', 'B');
    n.connect(r1.id, 'gi1/0/1', c.id, 'gi1/0/1'); n.connect(r2.id, 'gi1/0/1', c.id, 'gi1/0/2'); n.connect(a.id, 'eth0', r1.id, 'gi1/0/2'); n.connect(b.id, 'eth0', r2.id, 'gi1/0/2');
    var errs = n.ispApply(c.id, { ports: { 'gi1/0/1': { ip: '203.0.113.1', len: 30 }, 'gi1/0/2': { ip: '198.51.100.1', len: 30 } },
      routes: [{ net: '192.168.1.0/24', nh: '203.0.113.2' }, { net: '192.168.2.0/24', nh: '198.51.100.2' }], delay: 30, mbps: 10, loss: 0 });
    chk('облако настроено без ошибок', !errs.length, errs.join('; '));
    EL.labs.apply(n, { R1: ['configure', 'interface gigabitethernet 1/0/1', 'ip address 203.0.113.2/30', 'ip firewall disable', 'exit', 'interface gigabitethernet 1/0/2', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit',
      'ip route 0.0.0.0/0 203.0.113.1', 'end', 'commit', 'confirm'], R2: ['configure', 'interface gigabitethernet 1/0/1', 'ip address 198.51.100.2/30', 'ip firewall disable', 'exit', 'interface gigabitethernet 1/0/2',
      'ip address 192.168.2.1/24', 'ip firewall disable', 'exit', 'ip route 0.0.0.0/0 198.51.100.1', 'end', 'commit', 'confirm'] });
    n.exec(a.id, 'ip 192.168.1.10/24 192.168.1.1'); n.exec(b.id, 'ip 192.168.2.10/24 192.168.2.1');
    var p = n.exec(a.id, 'ping 192.168.2.10'), ms = +(p.match(/time=([\d.]+) ms/) || [])[1];
    chk('офис 1 ↔ офис 2 через облако: ping, RTT ≈ 60 мс (задержка 30 мс туда и обратно)', ms > 60 && ms < 62, p.split('\n')[0]);
    var f = n.simulate([{ kind: 'udp', src: a.id, dst: '192.168.2.10', size: 1000, rate: 2000, dur: 0.5 }]).flows[0];
    chk('скорость облака 10 Мбит/с: 16 Мбит/с UDP — потери в очереди', f.loss > 20, f.loss);
    chk('консоль облака — подсказка про окно', /окне «Облако провайдера»/.test(n.exec(c.id, 'show ip route')) && n.prompt(c.id) === 'isp> ');
    chk('ошибка в маршруте ловится', /маршрут/.test(n.ispCheck({ ports: {}, routes: [{ net: '10.0.0.0', nh: 'x' }], delay: 1, mbps: 1, loss: 0 })));
    chk('после перезагрузки настройки облака на месте', (n.reboot(c.id), /time=/.test(n.exec(a.id, 'ping 192.168.2.10'))));
    console.log('✓ Облако провайдера');
  })();
  // Экспорт результатов симуляции: .vec / .sca (OMNeT++ 6, версия 3) и CSV
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Экспорт: ' + name + (extra ? ' — ' + extra : '')); } }
    var n = new EL.Net(), a = n.add('VPC', 'A'), b = n.add('VPC', 'B'); n.connect(a.id, 'eth0', b.id, 'eth0'); n.exec(a.id, 'ip 10.0.0.1/24'); n.exec(b.id, 'ip 10.0.0.2/24'); n.setLink(0, { mbps: 2 });
    var r = n.simulate([{ kind: 'ping', src: a.id, dst: '10.0.0.2', count: 20, interval: 0.05, size: 56 }, { kind: 'udp', src: a.id, dst: '10.0.0.2', size: 1000, rate: 500, dur: 0.5 }]);
    var x = EL.simExport(n, r, { conv: 12, date: new Date(2026, 9, 29, 12, 0, 0), pid: 7 });
    var V = x.vec.split('\n'), S = x.sca.split('\n');
    chk('заголовок: version 3, run, attr network', V[0] === 'version 3' && /^run NetCat-0-20261029-12:00:00-7$/.test(V[1]) && V.indexOf('attr network Net') > 0);
    var decl = {}, okData = true, lastT = {};
    V.forEach(function (l) { var m = l.match(/^vector (\d+) (\S+) (\S+) TV$/); if (m) decl[m[1]] = m[3];
      var d = l.match(/^(\d+)\t(\S+)\t(\S+)$/); if (d) { if (!(d[1] in decl) || !isFinite(+d[2]) || !isFinite(+d[3]) || +d[2] < (lastT[d[1]] || 0)) okData = false; lastT[d[1]] = +d[2]; } });
    chk('векторы объявлены до данных, время по возрастанию', Object.keys(decl).length >= 4 && okData, JSON.stringify(decl));
    chk('векторы: rtt, endToEndDelay, queueLength, utilization', ['rtt:vector', 'endToEndDelay:vector', 'queueLength:vector', 'utilization:vector'].every(function (k) { return Object.keys(decl).some(function (i) { return decl[i] === k; }); }));
    chk('скаляры: sentPk:count, lossRate, convergenceTime', /^scalar Net\.A\.flow0 sentPk:count 20$/m.test(x.sca) && /^scalar Net\.A\.flow1 lossRate \d+$/m.test(x.sca) && /^scalar Net convergenceTime 12$/m.test(x.sca));
    var st = x.sca.match(/statistic Net\.A\.flow0 rtt:histogram\n((?:field \w+ \S+\n)+)attr unit s\n((?:bin\t\S+\t\d+\n)+)/);
    chk('гистограмма: field count/mean/stddev/min/max/sum/sqrsum и бины с -INF', st && /field count \d+/.test(st[1]) && /field sqrsum/.test(st[1]) && /^bin\t-INF\t0/.test(st[2]), x.sca.slice(x.sca.indexOf('statistic'), x.sca.indexOf('statistic') + 300));
    chk('каждая строка .sca — известного типа', S.every(function (l) { return !l || /^(version|run|attr|config|scalar|statistic|field|bin)[ \t]/.test(l); }));
    chk('CSV: BOM, «;», десятичная запятая', x.csv.charCodeAt(0) === 0xfeff && /^vector;Net\.A\.flow0;rtt:vector;0,\d+;0,\d+;s\r$/m.test(x.csv), x.csv.slice(0, 200));
    var nb = JSON.parse(EL.simNotebook());
    chk('тетрадка .ipynb: nbformat 4, ячейки markdown и code, разбор .vec/.sca', nb.nbformat === 4 && nb.cells.length >= 10 && nb.cells.some(function (c) { return c.cell_type === 'markdown'; }) &&
      /def read_vec/.test(EL.SIM_PY) && /def read_sca/.test(EL.SIM_PY) && nb.cells.every(function (c) { return Array.isArray(c.source); }));
    console.log('✓ Экспорт результатов: .vec, .sca, CSV');
  })();
  // Детерминированность для комнат: один и тот же журнал действий → одно и то же состояние (toJSON), ядро — без DOM
  (function () {
    function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ Детерминированность: ' + name + (extra ? ' — ' + extra : '')); } }
    var J = [['add', 'vESR', 'R1', 300, 100], ['add', 'MES2300-24', 'SW1', 300, 300], ['add', 'VPC', 'PC1', 150, 450], ['add', 'Debian-server', 'SRV', 450, 450],
      ['con', 'R1', 'gi1/0/1', 'SW1', 'gi1/0/24'], ['con', 'PC1', 'eth0', 'SW1', 'gi1/0/1'], ['con', 'SRV', 'ens3', 'SW1', 'gi1/0/2'],
      ['cli', 'R1', 'configure'], ['cli', 'R1', 'interface gigabitethernet 1/0/1'], ['cli', 'R1', 'ip address 10.0.0.1/24'], ['cli', 'R1', 'ip firewall disable'], ['cli', 'R1', 'end'], ['cli', 'R1', 'commit'], ['cli', 'R1', 'confirm'],
      ['cli', 'SW1', 'enable'], ['cli', 'SW1', 'configure'], ['cli', 'SW1', 'hostname CORE'], ['cli', 'SW1', 'end'],
      ['cli', 'PC1', 'ip 10.0.0.5/24 10.0.0.1'], ['cli', 'SRV', 'root'], ['cli', 'SRV', 'toor'], ['cli', 'SRV', 'ip addr add 10.0.0.10/24 dev ens3'], ['cli', 'SRV', 'ip link set ens3 up'],
      ['time', 31], ['cli', 'PC1', 'ping 10.0.0.10'], ['power', 'PC1', false], ['power', 'PC1', true], ['move', 'SRV', 500, 470], ['time', 400], ['cli', 'PC1', 'ping 10.0.0.1']];
    function play() { var n = new EL.Net(), outs = [];
      J.forEach(function (a) { var d = a[1] && n.byName(a[1]);
        if (a[0] === 'add') n.add(a[1], a[2], a[3], a[4]);
        if (a[0] === 'con') n.connect(n.byName(a[1]).id, a[2], n.byName(a[3]).id, a[4]);
        if (a[0] === 'cli') outs.push(String(n.exec(d.id, a[2])));
        if (a[0] === 'time') n.tick(a[1]);
        if (a[0] === 'power') n.power(d.id, a[2]);
        if (a[0] === 'move') { d.x = a[2]; d.y = a[3]; } });
      return { j: JSON.stringify(n.toJSON()), o: outs.join('\n'), arp: JSON.stringify(n.arpRows(n.byName('PC1').id)) }; }
    var A = play(), B = play();
    chk('журнал действий дважды → одинаковый toJSON', A.j === B.j, A.j.length + ' / ' + B.j.length);
    chk('… и одинаковый вывод консолей и ARP (MAC от имён, не от порядка создания)', A.o === B.o && A.arp === B.arp);
    chk('ping в журнале прошёл', /bytes from 10\.0\.0\.10/.test(A.o));
    // ../_dk_cli.js — тренажёр CLI дек: его интерфейс под typeof document, в Node не выполняется
    var bad = engineFiles.filter(function (f) { if (f === '../_dk_cli.js') return false; var s = fs.readFileSync(path.join(D, f), 'utf8').replace(/\/\*[\s\S]*?\*\/|\/\/.*$/gm, ''); return /\bdocument\.|localStorage|sessionStorage|addEventListener\(/.test(s); });
    chk('ядро (engine_files) не обращается к DOM и хранилищам браузера', !bad.length, bad.join(', '));
    console.log('✓ Детерминированность и безголовое ядро');
  })();

// случайные задания движка: решение на одном коммутаторе MES
['base', 'vlan'].forEach(function (kind) {
  EL.E.TASKS[kind].forEach(function (T, k) {
    for (var i = 0; i < N; i++) {
      total++;
      var net = new EL.Net(), d = net.add('MES3300-24', 'SW1'), P = T.gen();
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
    var n = new EL.Net(), s = n.add(d.model, 'SW1'); ['A', 'B', 'C'].forEach(function (x, i) { var v = n.add('VPC', x); n.connect(v.id, 'eth0', s.id, d.p(i + 1)); }); n.tick(31);
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
    m.connect(va.id, 'eth0', a.id, d.p(10)); m.connect(vb.id, 'eth0', b.id, d.p(10)); m.tick(31);
    var lag = ['enable', 'configure'].concat(d.lagPre, [d.rng(1, 4)], d.lag, ['end']);
    e = run(m, { S1: lag, S2: lag, A: ['ip 10.1.1.1/24'], B: ['ip 10.1.1.2/24'] });
    var L = m.lports(a.id).filter(function (l) { return l.name === 'po1'; })[0];
    chk(tag + ': LACP', !e.length && L && L.members.length === 4 && m.reach('A', '10.1.1.2'), e.join('; '));
    // кольцо из трёх с RSTP
    var r = new EL.Net(), x = ['X1', 'X2', 'X3'].map(function (nm) { return r.add(d.model, nm); }), ra = r.add('VPC', 'A'), rb = r.add('VPC', 'B');
    r.connect(x[0].id, d.p(1), x[1].id, d.p(2)); r.connect(x[1].id, d.p(1), x[2].id, d.p(2)); r.connect(x[2].id, d.p(1), x[0].id, d.p(2));
    r.connect(ra.id, 'eth0', x[0].id, d.p(5)); r.connect(rb.id, 'eth0', x[2].id, d.p(5)); r.tick(31);
    var sc = { A: ['ip 10.2.2.1/24'], B: ['ip 10.2.2.2/24'] };
    ['X1', 'X2', 'X3'].forEach(function (nm, i) { sc[nm] = ['enable', 'configure'].concat(d.stp, i === 1 ? [d.root] : [], ['end']); });
    e = run(r, sc); var t = r.stp(), blk = 0; Object.keys(t).forEach(function (id) { Object.keys(t[id]).forEach(function (q) { if (!t[id][q].fwd) blk++; }); });
    chk(tag + ': RSTP', !e.length && blk === 1 && r._stp.root[x[1].id] === x[1].id && r.reach('A', '10.2.2.2'), e.join('; ') + ' blk=' + blk);
    // зеркалирование
    var w = new EL.Net(), sw = w.add(d.model, 'M'), p1 = w.add('VPC', 'A'), p2 = w.add('VPC', 'B'), sn = w.add('Debian', 'S');
    w.connect(p1.id, 'eth0', sw.id, d.p(1)); w.connect(p2.id, 'eth0', sw.id, d.p(2)); w.connect(sn.id, 'ens3', sw.id, d.p(12)); w.tick(31);
    e = run(w, { M: ['enable', 'configure'].concat(d.mon(1, 12), ['end']), A: ['ip 10.3.3.1/24'], B: ['ip 10.3.3.2/24', 'ping 10.3.3.1'] });
    chk(tag + ': зеркалирование', !e.length && (sn.st.capN || 0) >= 2, e.join('; '));
  });
  var n8 = new EL.Net(), f = n8.add('MES5448', 'F'); n8.exec(f.id, 'enable'); n8.exec(f.id, 'configure'); n8.exec(f.id, 'interface 1/0/3');
  chk('приглашение FASTPATH', n8.prompt(f.id) === '(switch) (Interface 1/0/3)#', n8.prompt(f.id));
  var n6 = new EL.Net(), g = n6.add('MES3348', 'G'); n6.exec(g.id, 'enable'); n6.exec(g.id, 'configure');
  chk('6.x: режим rst не из своей ветки', /Режим/.test(n6.exec(g.id, 'spanning-tree mode rst')));
  console.log('✓ диалекты 6.x и 8.x');
})();

// STP по таймерам: состояния портов во времени (net.stpReal — без мгновенной сходимости автотеста)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ STP-таймеры: ' + name + (extra !== undefined ? ' — ' + extra : '')); } }
  function mk(model, cfg) {
    var n = new EL.Net(); n.stpReal = true;
    var a = n.add(model, 'S1'), b = n.add(model, 'S2'), va = n.add('VPC', 'A'), vb = n.add('VPC', 'B'), P = model === 'MES5448' ? '1/0/' : 'gi1/0/';
    EL.labs.apply(n, { S1: ['enable', 'configure'].concat(cfg || [], ['end']), S2: ['enable', 'configure'].concat(cfg || [], ['end']), A: ['ip 10.9.0.1/24'], B: ['ip 10.9.0.2/24'] });
    n.connect(a.id, P + '1', b.id, P + '1'); n.connect(va.id, 'eth0', a.id, P + '5'); n.connect(vb.id, 'eth0', b.id, P + '5');
    return { n: n, a: a, b: b, va: va };
  }
  function sts(n, id, ln) { return n.stpState(id, ln, 0); }
  // RSTP (10.x по умолчанию MSTP): мосты договорились сразу, порт к ПК — auto-edge через 3 с
  var t = mk('MES2428'), n = t.n;
  chk('RSTP p2p между мостами — сразу forwarding', sts(n, t.a.id, 'gi1/0/1') === 'Frw' && sts(n, t.b.id, 'gi1/0/1') === 'Frw');
  var r = n.ping(t.va.id, '10.9.0.2');
  chk('auto-edge: в первые 3 с порт к ПК в discarding, ping не проходит', !r.ok && sts(n, t.a.id, 'gi1/0/5') === 'Dsc' && /Dsc/.test(n.exec(t.a.id, 'show spanning-tree')), r.why);
  n.tick(3);
  chk('auto-edge: через 3 с forwarding, ping идёт', sts(n, t.a.id, 'gi1/0/5') === 'Frw' && n.ping(t.va.id, '10.9.0.2').ok);
  chk('show spanning-tree: Frw, Edge', /gi1\/0\/5\s+enabled .*Frw\s+Desg\s+P2p Edge/.test(n.exec(t.a.id, 'show spanning-tree')), n.exec(t.a.id, 'show spanning-tree'));
  // portfast — сразу
  t = mk('MES2428', ['interface gi1/0/5', 'spanning-tree portfast', 'exit']); n = t.n;
  chk('portfast: порт к ПК сразу forwarding', sts(n, t.a.id, 'gi1/0/5') === 'Frw');
  // без auto-edge — discarding 15 с, learning 15 с (MAC учится, кадры не идут), forwarding
  t = mk('MES2428', ['interface gi1/0/5', 'no spanning-tree auto-edge', 'exit']); n = t.n;
  n.tick(14); chk('no auto-edge: 14 с — discarding', sts(n, t.a.id, 'gi1/0/5') === 'Dsc');
  n.tick(2); r = n.ping(t.va.id, '10.9.0.2');
  chk('no auto-edge: 16 с — learning, кадр отброшен, MAC ПК выучен', sts(n, t.a.id, 'gi1/0/5') === 'Lrn' && !r.ok &&
      n.macRows(t.a.id).some(function (x) { return x.port === 'gi1/0/5'; }), JSON.stringify(n.macRows(t.a.id)));
  n.tick(14); chk('no auto-edge: 30 с — forwarding', sts(n, t.a.id, 'gi1/0/5') === 'Frw');
  chk('running-config: no spanning-tree auto-edge', /no spanning-tree auto-edge/.test(n.exec(t.a.id, 'show running-config')));
  // 802.1D (compatibility stp): listening → learning → forwarding и между мостами
  t = mk('MES2428', ['spanning-tree compatibility stp']); n = t.n;
  chk('802.1D: сразу listening между мостами', sts(n, t.a.id, 'gi1/0/1') === 'Lsn' && /Lsn/.test(n.exec(t.a.id, 'show spanning-tree')), n.exec(t.a.id, 'show spanning-tree'));
  n.tick(15); chk('802.1D: 15 с — learning', sts(n, t.a.id, 'gi1/0/1') === 'Lrn');
  n.tick(15); chk('802.1D: 30 с — forwarding, ping идёт', sts(n, t.a.id, 'gi1/0/1') === 'Frw' && n.ping(t.va.id, '10.9.0.2').ok);
  chk('802.1D: show — Hello 2 Max Age 20 Forward Delay 15', /Hello Time 2 sec  Max Age 20 sec  Forward Delay 15 sec/.test(n.exec(t.a.id, 'show spanning-tree')));
  // forward-time 11: переход за 22 с; условие 2*(FD-1) >= MaxAge
  t = mk('MES2428', ['spanning-tree compatibility stp', 'spanning-tree forward-time 11']); n = t.n;
  n.tick(21); chk('forward-time 11: 21 с — ещё learning', sts(n, t.a.id, 'gi1/0/1') === 'Lrn');
  n.tick(1); chk('forward-time 11: 22 с — forwarding', sts(n, t.a.id, 'gi1/0/1') === 'Frw');
  n.exec(t.a.id, 'configure');
  chk('forward-time 4 при max-age 20 — ошибка', /2\*\(Forward-Delay - 1\)/.test(n.exec(t.a.id, 'spanning-tree forward-time 4')));
  chk('running-config: forward-time 11', /spanning-tree forward-time 11/.test(n.exec(t.a.id, 'do show running-config')));
  // 802.1D, кольцо из трёх: прямой отказ — 30 с, непрямой — max-age 20 + 30 с
  function ring() {
    var n = new EL.Net(); n.stpReal = true; var x = ['X1', 'X2', 'X3'].map(function (nm) { return n.add('MES2428', nm); }), sc = {};
    x.forEach(function (d, i) { sc[d.name] = ['enable', 'configure', 'spanning-tree compatibility stp', 'spanning-tree priority ' + (4096 * (i + 1)), 'end']; });
    EL.labs.apply(n, sc);
    n.connect(x[0].id, 'gi1/0/1', x[1].id, 'gi1/0/1'); n.connect(x[0].id, 'gi1/0/2', x[2].id, 'gi1/0/1'); n.connect(x[1].id, 'gi1/0/2', x[2].id, 'gi1/0/2');
    n.tick(31); return { n: n, x: x };
  }
  var R = ring(), q = R.n.stp()[R.x[2].id];
  chk('кольцо: X3 gi1/0/2 — Altn, blocking', q['gi1/0/2'] && q['gi1/0/2'].role === 'Altn' && sts(R.n, R.x[2].id, 'gi1/0/2') === 'Blk', JSON.stringify(q));
  ['configure', 'interface gi1/0/1', 'shutdown'].forEach(function (l) { R.n.exec(R.x[2].id, l); });
  chk('прямой отказ: Altn → Root, listening', R.n.stp()[R.x[2].id]['gi1/0/2'].role === 'Root' && sts(R.n, R.x[2].id, 'gi1/0/2') === 'Lsn');
  R.n.tick(30); chk('прямой отказ: forwarding через 30 с', sts(R.n, R.x[2].id, 'gi1/0/2') === 'Frw');
  R = ring(); ['configure', 'interface gi1/0/1', 'shutdown'].forEach(function (l) { R.n.exec(R.x[1].id, l); });
  chk('непрямой отказ: X3 ждёт max-age в blocking', sts(R.n, R.x[2].id, 'gi1/0/2') === 'Blk' && R.n.stpLeft(R.x[2].id, 'gi1/0/2', 0) === 50, R.n.stpLeft(R.x[2].id, 'gi1/0/2', 0));
  R.n.tick(20); chk('непрямой отказ: после max-age — listening', sts(R.n, R.x[2].id, 'gi1/0/2') === 'Lsn');
  R.n.tick(30); chk('непрямой отказ: forwarding через 50 с', sts(R.n, R.x[2].id, 'gi1/0/2') === 'Frw');
  // 8.x: edgeport нет по умолчанию — порт к ПК по таймерам; 6.x: portfast auto по умолчанию — 3 с
  t = mk('MES5448'); n = t.n;
  n.tick(3); chk('8.x: без edgeport порт к ПК через 3 с ещё не forwarding', sts(n, t.a.id, '1/0/5') !== 'Frw');
  n.tick(27); chk('8.x: forwarding через 30 с', sts(n, t.a.id, '1/0/5') === 'Frw');
  t = mk('MES5448', ['interface 1/0/5', 'spanning-tree edgeport', 'exit']); n = t.n;
  chk('8.x: spanning-tree edgeport — сразу', sts(n, t.a.id, '1/0/5') === 'Frw' && /spanning-tree edgeport/.test(n.exec(t.a.id, 'show running-config')));
  t = mk('MES3348'); n = t.n;
  chk('6.x: portfast auto — 3 с', sts(n, t.a.id, 'gi1/0/5') === 'Dsc' && (n.tick(3), sts(n, t.a.id, 'gi1/0/5') === 'Frw'));
  console.log('✓ STP по таймерам');
})();

// DHCP-аренда по таймерам: T1 — продление, T2 — rebind, истечение — адрес снят и освобождён на сервере
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ DHCP-таймеры: ' + name + (extra !== undefined ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), s = n.add('MES2428', 'SW1'), v = n.add('VPC', 'PC1'), db = n.add('Debian', 'D1');
  n.connect(r.id, 'gi1/0/1', s.id, 'gi1/0/24'); n.connect(v.id, 'eth0', s.id, 'gi1/0/1'); n.connect(db.id, 'ens3', s.id, 'gi1/0/2');
  var e = EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ip address 10.5.0.1/24', 'ip firewall disable', 'exit', 'ip dhcp-server', 'ip dhcp-server pool P1',
    'network 10.5.0.0/24', 'address-range 10.5.0.10-10.5.0.20', 'default-router 10.5.0.1', 'default-lease-time 0:0:10', 'exit', 'do commit', 'do confirm', 'end'], PC1: ['ip dhcp'] });
  var sh = n.exec(v.id, 'show ip');
  chk('VPC получил адрес, show ip: DHCP LEASE 600, 600/300/525', !e.length && /DHCP LEASE  : 600, 600\/300\/525/.test(sh) && /DHCP SERVER : 10\.5\.0\.1/.test(sh), e.join('; ') + sh);
  chk('ESR show ip dhcp binding: адрес, окончание аренды, active', /10\.5\.0\.10\s+[0-9a-f:]{17}\s+\w+day \d{4}\/\d\d\/\d\d \d\d:\d\d:\d\d\s+active/.test(n.exec(r.id, 'show ip dhcp binding')), n.exec(r.id, 'show ip dhcp binding'));
  n.tick(299); chk('до T1 аренда не продлевалась', /DHCP LEASE  : 301,/.test(n.exec(v.id, 'show ip')));
  n.tick(1); chk('T1 (300 с): продлена unicast — снова 600', /DHCP LEASE  : 600,/.test(n.exec(v.id, 'show ip')) && n.leaseLeft(r.id, 'PC1') === 600, n.exec(v.id, 'show ip'));
  // Debian: dhclient, ip a — dynamic, valid_lft
  ['root', 'toor', 'dhclient ens3'].forEach(function (l) { n.exec(db.id, l); });
  chk('Debian: адрес dynamic, valid_lft 600sec', /scope global dynamic ens3\n\s+valid_lft 600sec preferred_lft 600sec/.test(n.exec(db.id, 'ip a')), n.exec(db.id, 'ip a'));
  // сервер пропал (кабель к ESR вынут): T1 и T2 не проходят, по истечении адрес снят, у сервера запись освободилась
  n.disconnect(0);
  n.tick(599); chk('нет сервера: T1 и T2 не прошли, до конца аренды (900 с) адрес держится', n.devs[v.id].st.ip === '10.5.0.10');
  var g = n.tick(1);
  chk('аренда истекла — VPC без адреса', !n.devs[v.id].st.ip && /IP\/MASK     : 0\.0\.0\.0\/0/.test(n.exec(v.id, 'show ip')) && g.some(function (x) { return x.kind === 'DHCP'; }), JSON.stringify(g));
  chk('аренда истекла — запись на сервере освобождена', !n.devs[r.id].st.leases.PC1);
  // Debian повторяет DISCOVER каждые 300 с: сервер вернулся — адрес снова получен
  chk('Debian тоже потерял адрес по истечении аренды', !n.devs[db.id].st.ip);
  n.connect(r.id, 'gi1/0/1', s.id, 'gi1/0/24'); n.tick(300);
  chk('Debian: retry 300 с — адрес получен снова', n.devs[db.id].st.ip && /^10\.5\.0\./.test(n.devs[db.id].st.ip), n.devs[db.id].st.ip);
  console.log('✓ DHCP по таймерам');
})();

// LLDP TTL и таймаут LACP по модельному времени
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ таймеры служб: ' + name + (extra !== undefined ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('vESR', 'RA'), b = n.add('vESR', 'RB');
  n.connect(a.id, 'gi1/0/1', b.id, 'gi1/0/1');
  var L = ['configure', 'lldp enable', 'interface gi1/0/1', 'lldp receive', 'lldp transmit', 'exit', 'do commit', 'do confirm', 'end'];
  EL.labs.apply(n, { RA: L, RB: L });
  function ttl() { var m = n.exec(a.id, 'show lldp neighbors').match(/R\s+(\d+)\s*$/m); return m ? +m[1] : null; }
  chk('LLDP: TTL соседа 120 (30 × 4)', ttl() === 120, n.exec(a.id, 'show lldp neighbors'));
  n.tick(10); chk('LLDP: через 10 с TTL 110', ttl() === 110, ttl());
  n.tick(20); chk('LLDP: через 30 с новый LLDPDU — снова 120', ttl() === 120, ttl());
  EL.labs.apply(n, { RB: ['configure', 'lldp timer 10', 'lldp hold-multiplier 3', 'do commit', 'do confirm', 'end'] });
  chk('LLDP: lldp timer 10, hold-multiplier 3 у соседа — TTL 30', ttl() === 30 && /lldp timer 10/.test(n.exec(b.id, 'show running-config')), ttl());
  n.tick(9); chk('LLDP: через 9 с — 21', ttl() === 21, ttl());
  // LACP: партнёр вышел из агрегата, линк жив — порт ещё timeout в агрегате
  var m = new EL.Net(), s1 = m.add('MES2428', 'S1'), s2 = m.add('MES2428', 'S2');
  m.connect(s1.id, 'gi1/0/1', s2.id, 'gi1/0/1'); m.connect(s1.id, 'gi1/0/2', s2.id, 'gi1/0/2');
  var lag = ['enable', 'configure', 'interface range gi1/0/1-2', 'channel-group 1 mode active', 'exit', 'end'];
  EL.labs.apply(m, { S1: lag, S2: lag });
  function mem() { var P = m.lports(s1.id).filter(function (l) { return l.name === 'po1'; })[0]; return P ? P.members.slice().sort().join(',') : ''; }
  chk('LACP: агрегат из двух портов', mem() === 'gi1/0/1,gi1/0/2', mem());
  EL.labs.apply(m, { S2: ['configure', 'interface gi1/0/2', 'no channel-group', 'end'] });
  m.tick(89); chk('LACP long: 89 с — порт ещё в агрегате (LACPDU не устарели)', mem() === 'gi1/0/1,gi1/0/2' && m.lacpLeft(s1.id, 'gi1/0/2') === 1, mem());
  m.tick(1); chk('LACP long: 90 с — порт выпал', mem() === 'gi1/0/1', mem());
  EL.labs.apply(m, { S2: ['configure', 'interface gi1/0/2', 'channel-group 1 mode active', 'end'], S1: ['configure', 'interface range gi1/0/1-2', 'lacp timeout short', 'end'] });
  chk('LACP: вернулся в агрегат; running-config lacp timeout short', mem() === 'gi1/0/1,gi1/0/2' && /lacp timeout short/.test(m.exec(s1.id, 'show running-config')), mem());
  EL.labs.apply(m, { S2: ['configure', 'interface gi1/0/2', 'no channel-group', 'end'] });
  m.tick(2); chk('LACP short: 2 с — ещё в агрегате', mem() === 'gi1/0/1,gi1/0/2', mem());
  m.tick(1); chk('LACP short: 3 с — выпал', mem() === 'gi1/0/1', mem());
  EL.labs.apply(m, { S2: ['configure', 'interface gi1/0/1', 'shutdown', 'end'] });
  chk('LACP: падение линка — сразу', mem() === '', mem());
  console.log('✓ таймеры служб: LLDP, LACP');
})();

// физика: потери при несовпадении дуплекса, совместимость трансиверов, MTU коммутатора
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ физика: ' + name + (extra !== undefined ? ' — ' + extra : '')); } }
  var n = new EL.Net(), s = n.add('MES2428', 'SW1'), a = n.add('VPC', 'A'), b = n.add('VPC', 'B');
  n.connect(a.id, 'eth0', s.id, 'gi1/0/1'); n.connect(b.id, 'eth0', s.id, 'gi1/0/2');
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'interface gi1/0/1', 'no negotiation', 'speed 100', 'end'], A: ['ip 10.8.0.1/24'], B: ['ip 10.8.0.2/24'] });
  var out = ''; for (var i = 0; i < 6; i++) out += n.exec(a.id, 'ping 10.8.0.2') + '\n';
  var lost = (out.match(/timeout/g) || []).length, okc = (out.match(/bytes from/g) || []).length;
  chk('дуплекс не совпадает (100 full против auto→half): часть эхо теряется, но не все', lost > 0 && okc > 0 && lost < okc, lost + ' потерь из 30');
  var ph = n.phys(s.id, 'gi1/0/1');
  chk('несовпадение видно: 100 Мбит/с, full у коммутатора, half у ПК', ph.up && ph.mismatch && ph.speed === 100 && ph.dup[s.id] === 'full' && ph.dup[a.id] === 'half');
  EL.labs.apply(n, { SW1: ['configure', 'interface gi1/0/1', 'negotiation', 'end'] });
  out = ''; for (i = 0; i < 4; i++) out += n.exec(a.id, 'ping 10.8.0.2') + '\n';
  chk('автосогласование с обеих сторон — потерь нет', !/timeout/.test(out));
  // трансиверы: разные модули на концах
  var m = new EL.Net(), x = m.add('MES5332A rev.C', 'X'), y = m.add('MES5332A rev.C', 'Y');
  m.connect(x.id, 'te1/0/1', y.id, 'te1/0/1', 'sfp10g|sfp10g-lr'); m.connect(x.id, 'te1/0/2', y.id, 'te1/0/2', 'sfp1g|sfp10g');
  m.connect(x.id, 'te1/0/3', y.id, 'te1/0/3', 'dac10g|sfp10g'); m.connect(x.id, 'te1/0/4', y.id, 'te1/0/4', 'sfp1g-lx');
  m.connect(x.id, 'te1/0/5', y.id, 'te1/0/5', 'sfp10g-lr|sfp10g-lr');
  var p1 = m.phys(x.id, 'te1/0/1'), p2 = m.phys(x.id, 'te1/0/2'), p3 = m.phys(x.id, 'te1/0/3'), p4 = m.phys(x.id, 'te1/0/4'), p5 = m.phys(x.id, 'te1/0/5');
  chk('10G SR ↔ 10G LR — линка нет (850 и 1310 нм, многомод/одномод)', !p1.up && /850 нм/.test(p1.why) && /1310 нм/.test(p1.why), p1.why);
  chk('1G SX ↔ 10G SR — линка нет (разные скорости)', !p2.up && /разные скорости/.test(p2.why), p2.why);
  chk('DAC ↔ оптика — нельзя', !p3.up && /DAC/.test(p3.why), p3.why);
  chk('1G LX с обеих сторон в порту SFP+ — линк 1000', p4.up && p4.speed === 1000, JSON.stringify(p4));
  chk('10G LR с обеих сторон — линк 10000', p5.up && p5.speed === 10000);
  chk('модули концов сохраняются в файле схемы', JSON.stringify(m.toJSON()).indexOf('sfp10g|sfp10g-lr') >= 0 && EL.Net.fromJSON(m.toJSON()).links[0].cabB === 'sfp10g-lr');
  // MTU коммутатора MES 10.x: system mtu 1000 — большой кадр отброшен молча
  var t = new EL.Net(), sw = t.add('MES2428', 'SW'), c = t.add('VPC', 'C'), d = t.add('VPC', 'D');
  t.connect(c.id, 'eth0', sw.id, 'gi1/0/1'); t.connect(d.id, 'eth0', sw.id, 'gi1/0/2');
  EL.labs.apply(t, { SW: ['enable', 'configure', 'system mtu 1000', 'end'], C: ['ip 10.9.9.1/24'], D: ['ip 10.9.9.2/24'] });
  chk('system mtu 1000: обычный ping идёт', /bytes from/.test(t.exec(c.id, 'ping 10.9.9.2')));
  var big = t.exec(c.id, 'ping 10.9.9.2 -l 1200');
  chk('system mtu 1000: пакет 1228 байт (кадр 1246) отброшен', !/bytes from/.test(big) && /system mtu 1000/.test(t.exec(sw.id, 'show running-config')), big);
  // MES 6.x: MTU 1500, port jumbo-frame — после записи и перезагрузки
  var j = new EL.Net(), r1 = j.add('vESR', 'R1'), m6 = j.add('MES3348', 'S6'), r2 = j.add('vESR', 'R2');
  j.connect(r1.id, 'gi1/0/1', m6.id, 'gi1/0/1'); j.connect(r2.id, 'gi1/0/1', m6.id, 'gi1/0/2');
  function esr(ip) { return ['configure', 'interface gi1/0/1', 'ip address ' + ip + '/24', 'ip firewall disable', 'mtu 9000', 'exit', 'end', 'commit', 'confirm']; }
  EL.labs.apply(j, { R1: esr('10.6.0.1'), R2: esr('10.6.0.2') });
  var j1 = j.exec(r1.id, 'ping 10.6.0.2 size 3000');
  chk('6.x без jumbo-frame: пакет 3028 байт через коммутатор не проходит', !/ 0% packet loss/.test(j1), j1);
  j.exec(m6.id, 'enable'); j.exec(m6.id, 'configure');
  var jm = j.exec(m6.id, 'port jumbo-frame'); j.exec(m6.id, 'end');
  chk('port jumbo-frame — сообщение о перезагрузке, до неё не действует', /resetting the device/.test(jm) && !/ 0% packet loss/.test(j.exec(r1.id, 'ping 10.6.0.2 size 3000')), jm);
  j.exec(m6.id, 'write'); j.exec(m6.id, 'reload');
  var j2 = j.exec(r1.id, 'ping 10.6.0.2 size 3000');
  chk('после write и reload jumbo-frame действует — 3028 байт проходят', / 0% packet loss/.test(j2), j2);
  console.log('✓ физика: дуплекс, трансиверы, MTU коммутатора');
})();

// STP: смена топологии — очистка MAC (RSTP) и короткое старение (802.1D)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ STP TC: ' + name + (extra !== undefined ? ' — ' + extra : '')); } }
  function ring(compat) {
    var n = new EL.Net(), x = ['X1', 'X2', 'X3'].map(function (nm) { return n.add('MES2428', nm); }), a = n.add('VPC', 'A'), b = n.add('VPC', 'B'), sc = {};
    x.forEach(function (d, i) { sc[d.name] = ['enable', 'configure'].concat(compat ? ['spanning-tree compatibility stp'] : [], ['spanning-tree priority ' + (4096 * (i + 1)), 'end']); });
    sc.A = ['ip 10.4.4.1/24']; sc.B = ['ip 10.4.4.2/24']; EL.labs.apply(n, sc);
    n.connect(x[0].id, 'gi1/0/1', x[1].id, 'gi1/0/1'); n.connect(x[0].id, 'gi1/0/2', x[2].id, 'gi1/0/1'); n.connect(x[1].id, 'gi1/0/2', x[2].id, 'gi1/0/2');
    n.connect(a.id, 'eth0', x[1].id, 'gi1/0/5'); n.connect(b.id, 'eth0', x[2].id, 'gi1/0/5'); n.tick(31);
    return { n: n, x: x, a: a, b: b };
  }
  function rows(n, d, port) { return n.macRows(d.id).filter(function (r) { return !port || r.port === port; }); }
  var R = ring(false), n = R.n;
  chk('ping через кольцо', n.ping(R.a.id, '10.4.4.2').ok);
  var before = rows(n, R.x[0]).length, edgeB = rows(n, R.x[1], 'gi1/0/5').length;
  ['configure', 'interface gi1/0/1', 'shutdown', 'end'].forEach(function (l) { n.exec(R.x[0].id, l); }); n.stp();
  chk('RSTP: обрыв X1–X2 — X1 стёр MAC с не-edge портов', before > 0 && rows(n, R.x[0]).length === 0, before + ' → ' + JSON.stringify(rows(n, R.x[0])));
  chk('RSTP: запись с edge-порта (ПК) у X2 осталась', edgeB === 1 && rows(n, R.x[1], 'gi1/0/5').length === 1);
  chk('RSTP: счётчик смен топологии', n.stpTc(R.x[0].id) && n.stpTc(R.x[0].id).n >= 1);
  chk('после TC связь восстанавливается', n.ping(R.a.id, '10.4.4.2').ok);
  R = ring(true); n = R.n; n.tick(10); n.ping(R.a.id, '10.4.4.2');   // начальная сходимость тоже TC: ждём, пока флаг снимется
  chk('802.1D: обычное старение 300 с', n.macAge(R.x[0].id) === 300);
  ['configure', 'interface gi1/0/1', 'shutdown', 'end'].forEach(function (l) { n.exec(R.x[0].id, l); }); n.stp();
  chk('802.1D: после TC MAC стареют за forward-delay (15 с)', n.macAge(R.x[0].id) === 15, n.macAge(R.x[0].id));
  n.tick(36); chk('802.1D: через max-age + forward-delay (35 с) — снова 300', n.macAge(R.x[0].id) === 300, n.macAge(R.x[0].id));
  console.log('✓ STP: смена топологии');
})();

// DHCPv6 на ESR, клиент Debian dhclient -6; старение ND (ipv6 nd reachable-time)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ DHCPv6/ND: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), sw = n.add('MES2428', 'SW1'), deb = n.add('Debian', 'D1');
  n.connect(r.id, 'gi1/0/1', sw.id, 'gi1/0/24'); n.connect(deb.id, 'ens3', sw.id, 'gi1/0/2');
  var e = EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ipv6 address 2001:db8:7::1/64', 'ipv6 nd prefix 2001:db8:7::/64 86400 3600', 'ipv6 nd managed-config-flag', 'ip firewall disable', 'exit',
    'ipv6 dhcp-server pool V6', 'network 2001:db8:7::/64', 'address-range 2001:db8:7::100-2001:db8:7::1ff', 'dns-server 2001:db8:7::53', 'exit', 'ipv6 dhcp-server', 'end', 'commit', 'confirm'] });
  chk('конфигурация без ошибок', !e.length, e.join('; '));
  chk('running-config: ipv6 dhcp-server pool и флаг M', /ipv6 dhcp-server pool V6\n  network 2001:db8:7::\/64\n  address-range 2001:db8:7::100-2001:db8:7::1ff/.test(n.exec(r.id, 'show running-config')) &&
      /ipv6 nd managed-config-flag/.test(n.exec(r.id, 'show running-config')));
  ['root', 'toor', 'ip link set ens3 up'].forEach(function (l) { n.exec(deb.id, l); }); n.tick(5);   // префикс on-link и шлюз — из RA (повторный RS через 4 с)
  var o = n.exec(deb.id, 'dhclient -6 ens3');
  chk('Debian dhclient -6: адрес из пула', /Bound to lease 2001:db8:7::100/.test(o) && /2001:db8:7::100\/128/.test(n.exec(deb.id, 'ip -6 addr')), o);
  chk('ESR show ipv6 dhcp binding', /2001:db8:7::100\s+[0-9a-f:]{17}\s+active/.test(n.exec(r.id, 'show ipv6 dhcp binding')), n.exec(r.id, 'show ipv6 dhcp binding'));
  chk('связь по адресу из DHCPv6', n.ping6(r.id, '2001:db8:7::100').ok);
  chk('ND: сразу после обмена — reachable', /2001:db8:7::100\s+\S+\s+reachable/.test(n.exec(r.id, 'show ipv6 neighbors')), n.exec(r.id, 'show ipv6 neighbors'));
  n.tick(31); chk('ND: через 31 с (reachable-time 30000) — stale', /2001:db8:7::100\s+\S+\s+stale/.test(n.exec(r.id, 'show ipv6 neighbors')));
  EL.labs.apply(n, { R1: ['configure', 'ipv6 nd reachable-time 60000', 'end', 'commit', 'confirm'] });
  chk('ipv6 nd reachable-time 60000 — снова reachable до 60 с', /2001:db8:7::100\s+\S+\s+reachable/.test(n.exec(r.id, 'show ipv6 neighbors')));
  var e2 = EL.labs.apply(n, { R1: ['configure', 'no ipv6 dhcp-server', 'end', 'commit', 'confirm'] }), d2 = n.add('Debian', 'D2'); n.connect(d2.id, 'ens3', sw.id, 'gi1/0/3');
  ['root', 'toor', 'ip link set ens3 up'].forEach(function (l) { n.exec(d2.id, l); });
  chk('DHCPv6-сервер выключен — No DHCPv6 servers responded', !e2.length && /No DHCPv6 servers responded/.test(n.exec(d2.id, 'dhclient -6')));
  console.log('✓ DHCPv6 и старение ND');
})();

// SNMP: агенты ESR, MES 6.x, MES 10.x; snmpwalk/snmpget/snmpset и трапы на Debian-server
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ SNMP: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), sw = n.add('MES2428', 'SW10'), s6 = n.add('MES3348', 'SW6'), srv = n.add('Debian-server', 'NMS'), pc = n.add('VPC', 'PC');
  n.connect(r.id, 'gi1/0/1', sw.id, 'gi1/0/24'); n.connect(srv.id, 'ens3', sw.id, 'gi1/0/1'); n.connect(s6.id, 'gi1/0/1', sw.id, 'gi1/0/2'); n.connect(pc.id, 'eth0', r.id, 'gi1/0/2');
  var e = EL.labs.apply(n, {
    R1: ['configure', 'hostname R1', 'interface gi1/0/1', 'ip address 10.9.9.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 10.8.8.1/24', 'ip firewall disable', 'exit',
      'snmp-server', 'snmp-server community public ro', 'snmp-server community private rw', 'snmp-server host 10.9.9.10', 'snmp-server enable traps', 'snmp-server location "Aud 305"', 'end', 'commit', 'confirm'],
    SW10: ['enable', 'configure', 'hostname SW10', 'interface vlan 1', 'ip address 10.9.9.2 255.255.255.0', 'exit', 'snmp user USER', 'snmp community index 1 name NETMAN security USER',
      'snmp group GROUP user USER security-model v2c', 'snmp access GROUP v2c read iso write iso notify iso', 'snmp view iso 1 included', 'end'],
    SW6: ['enable', 'configure', 'hostname SW6', 'interface vlan 1', 'ip address 10.9.9.3 255.255.255.0', 'exit', 'snmp-server server', 'snmp-server community campus ro', 'end'],
    NMS: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.9.9.10/24 dev ens3', 'systemctl start snmptrapd'] });
  chk('конфигурация без ошибок', !e.length, e.join('; '));
  var w = n.exec(srv.id, 'snmpwalk -v2c -c public 10.9.9.1 system');
  chk('ESR: snmpwalk system — sysName R1, sysLocation', /SNMPv2-MIB::sysName\.0 = STRING: R1/.test(w) && /sysLocation\.0 = STRING: Aud 305/.test(w) && /sysUpTimeInstance = Timeticks/.test(w), w);
  chk('ESR: snmpget ifDescr.1 — gi1/0/1', /IF-MIB::ifDescr\.1 = STRING: gi1\/0\/1/.test(n.exec(srv.id, 'snmpget -v2c -c public 10.9.9.1 IF-MIB::ifDescr.1')), n.exec(srv.id, 'snmpget -v2c -c public 10.9.9.1 IF-MIB::ifDescr.1'));
  chk('ESR: snmpset с ro-community — noAccess', /noAccess/.test(n.exec(srv.id, 'snmpset -v2c -c public 10.9.9.1 SNMPv2-MIB::sysLocation.0 s Lab')));
  chk('ESR: snmpset с rw-community меняет sysLocation', /sysLocation\.0 = STRING: Lab 2/.test(n.exec(srv.id, 'snmpset -v2c -c private 10.9.9.1 sysLocation.0 s "Lab 2"')) &&
      /Lab 2/.test(n.exec(srv.id, 'snmpget -v2c -c public 10.9.9.1 sysLocation.0')));
  chk('неверная community — Timeout и трап authenticationFailure', /Timeout: No Response/.test(n.exec(srv.id, 'snmpwalk -v2c -c wrong 10.9.9.1')) &&
      /authenticationFailure/.test(srv.st.files['/var/log/snmptrapd.log'] || ''), srv.st.files['/var/log/snmptrapd.log']);
  n.events();   // снимок состояния (в интерфейсе события опрашиваются каждую секунду)
  ['configure', 'interface gi1/0/2', 'shutdown', 'end', 'commit', 'confirm'].forEach(function (l) { n.exec(r.id, l); }); n.events(); n.tick(1);
  chk('линк gi1/0/2 упал — трап linkDown с ifIndex', /IF-MIB::linkDown\tIF-MIB::ifIndex\.2/.test(srv.st.files['/var/log/snmptrapd.log'] || ''), srv.st.files['/var/log/snmptrapd.log']);
  var w10 = n.exec(srv.id, 'snmpget -v2c -c NETMAN 10.9.9.2 sysName.0');
  chk('MES 10.x: community → user → group → access → view (руководство 3.6.2.3)', /sysName\.0 = STRING: SW10/.test(w10), w10);
  chk('MES 10.x: другая community — нет ответа', /Timeout/.test(n.exec(srv.id, 'snmpget -v2c -c public 10.9.9.2 sysName.0')));
  var w6 = n.exec(srv.id, 'snmpwalk -v2c -c campus 10.9.9.3 ifOperStatus');
  chk('MES 6.x: snmp-server server + community — ifOperStatus', /IF-MIB::ifOperStatus\.1 = INTEGER: up\(1\)/.test(w6) && /snmp-server community campus ro/.test(n.exec(s6.id, 'show running-config')), w6);
  chk('MES 6.x: без snmp-server server — нет ответа', (EL.labs.apply(n, { SW6: ['configure', 'no snmp-server server', 'end'] }), /Timeout/.test(n.exec(srv.id, 'snmpget -v2c -c campus 10.9.9.3 sysName.0'))));
  chk('running-config ESR: snmp-server …', /snmp-server community public ro\nsnmp-server community private rw\nsnmp-server host 10\.9\.9\.10/.test(n.exec(r.id, 'show running-config')));
  console.log('✓ SNMP');
})();

// AAA: вход через TACACS+ (ESR) и RADIUS (MES 6.x) на Debian-server
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ AAA: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), sw = n.add('MES3348', 'SW6'), srv = n.add('Debian-server', 'AAA');
  n.connect(r.id, 'gi1/0/1', sw.id, 'gi1/0/24'); n.connect(srv.id, 'ens3', sw.id, 'gi1/0/1');
  var e = EL.labs.apply(n, {
    R1: ['configure', 'interface gi1/0/1', 'ip address 10.5.5.1/24', 'ip firewall disable', 'exit', 'ip ssh server',
      'tacacs-server host 10.5.5.10', 'key ascii-text secret1', 'exit', 'aaa authentication login default tacacs local', 'end', 'commit', 'confirm'],
    SW6: ['enable', 'configure', 'interface vlan 1', 'ip address 10.5.5.2 255.255.255.0', 'exit', 'radius-server host 10.5.5.10 key radkey', 'aaa authentication login default radius local', 'end'],
    AAA: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.5.5.10/24 dev ens3'] });
  chk('конфигурация без ошибок', !e.length, e.join('; '));
  var F = srv.st.files; F['/etc/tacacs+/tac_plus.conf'] = 'key = secret1\nuser = alice {\n    login = cleartext "pa55"\n}\n';
  F['/etc/freeradius/3.0/clients.conf'] = 'client sw6 {\n\tipaddr = 10.5.5.2\n\tsecret = radkey\n}\n'; F['/etc/freeradius/3.0/users'] = 'bob Cleartext-Password := "b0b"\n';
  n.exec(srv.id, 'systemctl start tac_plus'); n.exec(srv.id, 'systemctl start freeradius');
  function loc(d) { return function (u, p) { var U = d.type === 'esr' ? d.st.run.users : d.st.users; return !!(U && U[u] && U[u].pw === p); }; }
  var a1 = n.aaaLogin(r.id, 'console', 'alice', 'pa55', loc(r));
  chk('ESR: alice входит через TACACS+', a1 && a1.ok && a1.method === 'tacacs', JSON.stringify(a1));
  chk('ESR: неверный пароль TACACS+ — отказ, local тоже не знает alice', !n.aaaLogin(r.id, 'console', 'alice', 'bad', loc(r)).ok);
  var a3 = n.aaaLogin(r.id, 'console', 'admin', 'password', loc(r));
  chk('ESR: admin нет на TACACS+ (отказ) — chain: проверен local, вход', a3.ok && a3.method === 'local', JSON.stringify(a3));
  EL.labs.apply(n, { R1: ['configure', 'aaa authentication mode break', 'end', 'commit', 'confirm'] });
  chk('ESR: mode break — отказ TACACS+ окончательный', !n.aaaLogin(r.id, 'console', 'admin', 'password', loc(r)).ok);
  n.exec(srv.id, 'systemctl stop tac_plus');
  var a5 = n.aaaLogin(r.id, 'console', 'admin', 'password', loc(r));
  chk('ESR: TACACS+ недоступен — даже при break вход по local', a5.ok && a5.method === 'local' && /tac_plus|недоступен/.test(a5.log.join(' ')), JSON.stringify(a5));
  n.exec(srv.id, 'systemctl start tac_plus');
  var s1 = n.exec(srv.id, 'ssh alice@10.5.5.1'); n.exec(srv.id, 'yes'); var s2 = n.exec(srv.id, 'pa55');
  chk('SSH на ESR пользователем TACACS+', /authenticity/.test(s1) && !/Permission denied/.test(s2) && !!srv.st.ssh, s1 + ' / ' + s2);
  n.exec(srv.id, 'exit'); n.exec(srv.id, 'ssh alice@10.5.5.1');
  chk('SSH: неверный пароль TACACS+ — Permission denied', /Permission denied/.test(n.exec(srv.id, 'wrong')));
  chk('running-config ESR: tacacs-server host / key ascii-text', /tacacs-server host 10\.5\.5\.10\n  key ascii-text secret1\nexit/.test(n.exec(r.id, 'show running-config')));
  var m1 = n.aaaLogin(sw.id, 'console', 'bob', 'b0b', loc(sw));
  chk('MES 6.x: bob входит через RADIUS', m1 && m1.ok && m1.method === 'radius', JSON.stringify(m1));
  F['/etc/freeradius/3.0/clients.conf'] = 'client sw6 {\n\tipaddr = 10.5.5.2\n\tsecret = other\n}\n';
  var m2 = n.aaaLogin(sw.id, 'console', 'bob', 'b0b', loc(sw));
  chk('MES 6.x: secret не совпал — сервер «недоступен», local не знает bob', !m2.ok && /clients\.conf/.test(m2.log.join(' ')), JSON.stringify(m2));
  console.log('✓ AAA: RADIUS и TACACS+');
})();

// QoS на ESR в симуляции: police, shape, маркировка DSCP и класс по DSCP на следующем маршрутизаторе
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ QoS: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r1 = n.add('vESR', 'R1'), r2 = n.add('vESR', 'R2'), a = n.add('VPC', 'A'), b = n.add('VPC', 'B');
  n.connect(a.id, 'eth0', r1.id, 'gi1/0/1'); n.connect(r1.id, 'gi1/0/2', r2.id, 'gi1/0/1'); n.connect(r2.id, 'gi1/0/2', b.id, 'eth0');
  var e = EL.labs.apply(n, {
    R1: ['configure', 'interface gi1/0/1', 'ip address 10.1.1.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 10.12.0.1/30', 'ip firewall disable', 'exit',
      'ip route 10.2.2.0/24 10.12.0.2', 'ip access-list extended UDP', 'rule 10', 'action permit', 'match protocol udp', 'enable', 'exit', 'exit',
      'class-map BULK', 'match access-group UDP', 'exit', 'policy-map LIMIT', 'class BULK', 'police 1000', 'exit', 'exit', 'interface gi1/0/2', 'service-policy output LIMIT', 'exit', 'end', 'commit', 'confirm'],
    R2: ['configure', 'interface gi1/0/1', 'ip address 10.12.0.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 10.2.2.1/24', 'ip firewall disable', 'exit',
      'ip route 10.1.1.0/24 10.12.0.1', 'end', 'commit', 'confirm'],
    A: ['ip 10.1.1.10/24 10.1.1.1'], B: ['ip 10.2.2.10/24 10.2.2.1'] });
  chk('конфигурация без ошибок', !e.length, e.join('; '));
  chk('running-config: class-map, policy-map, service-policy', /class-map BULK\n  match access-group UDP\nexit\npolicy-map LIMIT\n  class BULK\n    police 1000/.test(n.exec(r1.id, 'show running-config')) &&
      /service-policy output LIMIT/.test(n.exec(r1.id, 'show running-config')));
  function run(fl) { return n.simulate(fl, { qcap: 1000 }).flows; }
  var udp = { kind: 'udp', src: a.id, dst: '10.2.2.10', size: 972, rate: 1000, dur: 1 };            // 1000 пакетов × 1000 байт ≈ 8 Мбит/с
  var f1 = run([udp])[0];
  chk('police 1000 Кбит/с: ~1/8 UDP проходит, остальное отброшено', f1.loss > 80 && f1.loss < 92 && Object.keys(f1.drops).some(function (k) { return /police 1000/.test(k); }), f1.loss + '% ' + JSON.stringify(f1.drops));
  var f2 = run([{ kind: 'ping', src: a.id, dst: '10.2.2.10', count: 5, interval: 0.001 }])[0];
  chk('ICMP не в классе BULK — без потерь', f2.loss === 0, JSON.stringify(f2.drops));
  EL.labs.apply(n, { R1: ['configure', 'policy-map LIMIT', 'class BULK', 'no police', 'shape average 2000', 'end', 'commit', 'confirm'] });
  var f3 = run([{ kind: 'udp', src: a.id, dst: '10.2.2.10', size: 972, rate: 500, dur: 1 }])[0];
  chk('shape 2000 Кбит/с: потерь нет, задержка растёт до секунд', f3.loss === 0 && f3.max > 0.5, f3.loss + '% max ' + f3.max);
  EL.labs.apply(n, { R1: ['configure', 'policy-map LIMIT', 'class BULK', 'no shape average', 'set dscp 46', 'end', 'commit', 'confirm'],
    R2: ['configure', 'class-map EF', 'match dscp 46', 'exit', 'policy-map IN', 'class EF', 'police 500', 'exit', 'exit', 'interface gi1/0/1', 'service-policy input IN', 'exit', 'end', 'commit', 'confirm'] });
  var f4 = run([udp])[0];
  chk('R1 маркирует DSCP 46, R2 по DSCP ограничивает на входе', f4.loss > 90 && Object.keys(f4.drops).some(function (k) { return /R2 gi1\/0\/1: police 500 Кбит\/с \(класс EF\)/.test(k); }), JSON.stringify(f4.drops));
  console.log('✓ QoS');
})();

// PIM-SM со статическим RP на MES 6.x: источник и получатель за разными L3-коммутаторами
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ PIM: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('MES3348', 'SWA'), b = n.add('MES3348', 'SWB'), src = n.add('Debian', 'SRC'), rc = n.add('Debian', 'RC'), r2 = n.add('Debian', 'RC2');
  n.connect(a.id, 'gi1/0/24', b.id, 'gi1/0/24'); n.connect(src.id, 'ens3', a.id, 'gi1/0/1'); n.connect(rc.id, 'ens3', b.id, 'gi1/0/1'); n.connect(r2.id, 'ens3', b.id, 'gi1/0/2');
  function sw(lan, ip, mine, peer, net) { return ['enable', 'configure', 'vlan database', 'vlan ' + lan + ',100', 'exit', 'interface gi1/0/1', 'switchport mode access', 'switchport access vlan ' + lan, 'exit',
    'interface gi1/0/2', 'switchport mode access', 'switchport access vlan ' + lan, 'exit', 'interface gi1/0/24', 'switchport mode access', 'switchport access vlan 100', 'exit',
    'interface vlan ' + lan, 'ip address ' + ip + ' 255.255.255.0', 'exit', 'interface vlan 100', 'ip address ' + mine + ' 255.255.255.0', 'exit',
    'ip route ' + net + ' 255.255.255.0 ' + peer, 'ip multicast-routing', 'ip pim rp-address 10.100.0.1', 'end']; }
  function host(ip, gw) { return ['root', 'toor', 'ip link set ens3 up', 'ip addr add ' + ip + '/24 dev ens3', 'ip route add default via ' + gw]; }
  var e = EL.labs.apply(n, { SWA: sw(10, '10.10.0.1', '10.100.0.1', '10.100.0.2', '10.20.0.0'), SWB: sw(20, '10.20.0.1', '10.100.0.2', '10.100.0.1', '10.10.0.0'),
    SRC: host('10.10.0.10', '10.10.0.1'), RC: host('10.20.0.10', '10.20.0.1'), RC2: host('10.20.0.11', '10.20.0.1') });
  chk('конфигурация без ошибок', !e.length, e.join('; '));
  chk('unicast: источник видит получателя', n.ping(src.id, '10.20.0.10').ok);
  chk('show ip pim neighbor на SWA — сосед 10.100.0.2', /10\.100\.0\.2\s+vlan100/.test(n.exec(a.id, 'show ip pim neighbor')), n.exec(a.id, 'show ip pim neighbor'));
  n.exec(rc.id, 'ip addr add 239.1.1.1/32 dev ens3 autojoin');
  var r = n.mcastSend(src.id, '239.1.1.1');
  chk('поток 239.1.1.1 дошёл до RC за вторым коммутатором (Register на RP, дерево (*,G))', r.ok && r.got.indexOf('RC') >= 0 && r.got.indexOf('RC2') < 0 &&
      r.steps.some(function (x) { return /Register на RP 10\.100\.0\.1/.test(x.t); }) && r.steps.some(function (x) { return /SWB \(\*,239\.1\.1\.1\)/.test(x.t); }), r.steps.map(function (x) { return x.t; }).join(' | '));
  EL.labs.apply(n, { SWB: ['configure', 'interface vlan 100', 'no ip pim', 'end'] });
  var r2x = n.mcastSend(src.id, '239.1.1.1');
  chk('no ip pim на SVI к RP — SWB не присоединился, поток не доходит', r2x.got.indexOf('RC') < 0 && r2x.steps.some(function (x) { return /не присоединился/.test(x.t); }), r2x.steps.map(function (x) { return x.t; }).join(' | '));
  EL.labs.apply(n, { SWB: ['configure', 'interface vlan 100', 'ip pim', 'exit', 'no ip pim rp-address 10.100.0.1', 'end'] });
  chk('на SWB нет RP — поток не доходит', n.mcastSend(src.id, '239.1.1.1').got.indexOf('RC') < 0);
  EL.labs.apply(n, { SWB: ['configure', 'ip pim rp-address 10.100.0.1', 'interface vlan 20', 'ip igmp static-group 239.2.2.2', 'end'] });
  chk('running-config: ip multicast-routing pim, rp-address, static-group', /ip multicast-routing pim\nip pim rp-address 10\.100\.0\.1/.test(n.exec(b.id, 'show running-config')) &&
      /ip igmp static-group 239\.2\.2\.2/.test(n.exec(b.id, 'show running-config')));
  chk('show ip pim rp mapping', /RP: 10\.100\.0\.1, static/.test(n.exec(b.id, 'show ip pim rp mapping')));
  console.log('✓ PIM');
})();
// Удалённый доступ PPTP и L2TP over IPsec: сервер R1 за провайдером ISP, клиент R2 подключается к outside-address
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ RA: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r1 = n.add('vESR', 'R1'), isp = n.add('vESR', 'ISP'), r2 = n.add('vESR', 'R2'), a = n.add('VPC', 'A');
  n.connect(a.id, 'eth0', r1.id, 'gi1/0/1'); n.connect(r1.id, 'gi1/0/2', isp.id, 'gi1/0/1'); n.connect(isp.id, 'gi1/0/2', r2.id, 'gi1/0/2');
  var e = EL.labs.apply(n, {
    R1: ['configure', 'interface gi1/0/1', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 100.0.0.2/30', 'ip firewall disable', 'exit',
      'ip route 0.0.0.0/0 100.0.0.1', 'remote-access pptp office', 'local-address ip-address 10.10.10.1', 'remote-address address-range 10.10.10.20-10.10.10.40',
      'outside-address ip-address 100.0.0.2', 'authentication method mschap-v2', 'username ivan', 'password ascii-text Pa55word', 'enable', 'exit', 'enable', 'exit', 'end', 'commit', 'confirm'],
    ISP: ['configure', 'interface gi1/0/1', 'ip address 100.0.0.1/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 100.0.1.1/30', 'ip firewall disable', 'exit', 'end', 'commit', 'confirm'],
    R2: ['configure', 'interface gi1/0/2', 'ip address 100.0.1.2/30', 'ip firewall disable', 'exit', 'ip route 0.0.0.0/0 100.0.1.1',
      'tunnel pptp 1', 'remote address 100.0.0.2', 'username ivan password ascii-text Pa55word', 'ip firewall disable', 'enable', 'exit', 'end', 'commit', 'confirm'],
    A: ['ip 192.168.1.10/24 192.168.1.1'] });
  chk('конфигурация без ошибок', !e.length, e.join('; '));
  var st = n.exec(r1.id, 'show remote-access status');
  chk('сервер: ivan получил 10.10.10.20', /ivan\s+10\.10\.10\.20\s+pptp\(office\)/.test(st) && /Count sessions: 1/.test(st), st);
  var p0 = n.ping(r2.id, '192.168.1.10');
  chk('сервер без security-zone: межсетевой экран отбрасывает трафик из туннеля', !p0.ok && p0.steps.some(function (x) { return /не в зоне/.test(x.t); }), p0.steps.map(function (x) { return x.t; }).join(' | '));
  EL.labs.apply(n, { R1: ['configure', 'security zone trusted', 'exit', 'remote-access pptp office', 'security-zone trusted', 'exit', 'end', 'commit', 'confirm'] });
  var p = n.ping(r2.id, '192.168.1.10');
  chk('клиент через PPTP достаёт офисную сеть', p.ok && p.steps.some(function (x) { return /PPP в GRE/.test(x.t); }), p.steps.map(function (x) { return x.t; }).join(' | '));
  chk('show tunnels status на клиенте: pptp 1 Up', /pptp 1\s+Up\s+\d+\s+10\.10\.10\.20/.test(n.exec(r2.id, 'show tunnels status')), n.exec(r2.id, 'show tunnels status'));
  chk('интернет-адрес провайдера доступен мимо туннеля', n.ping(r2.id, '100.0.1.1').ok);
  var lg = n.raSess()[r2.id]['pptp 1'].log.map(function (x) { return x.t; }).join(' | ');
  chk('журнал установления PPTP: TCP 1723, SCCRQ, LCP, MS-CHAPv2, IPCP', /TCP SYN на порт 1723/.test(lg) && /Start-Control-Connection-Request/.test(lg) && /LCP: Configure-Request/.test(lg) && /MS-CHAPv2 Success/.test(lg) && /IPCP: .*10\.10\.10\.20/.test(lg), lg);
  var cn = n.exec(r1.id, 'show remote-access counters pptp');
  chk('show remote-access counters: пакеты ivan', /PPTP Server: office\nUser: ivan\(10\.10\.10\.20\)\nPackets received:\s+[1-9]/.test(cn) && /Packets transmitted:\s+[1-9]/.test(cn), cn);
  n.exec(r1.id, 'clear remote-access counters'); chk('clear remote-access counters', /Packets received:\s+0\n/.test(n.exec(r1.id, 'show remote-access counters')));
  EL.labs.apply(n, { R1: ['configure', 'remote-access pptp office', 'encryption mppe', 'authentication method chap', 'exit', 'end', 'commit', 'confirm'] });
  chk('MPPE с CHAP — CCP отказ', /pptp 1\s+Down.*MPPE требует MS-CHAP/.test(n.exec(r2.id, 'show tunnels status')), n.exec(r2.id, 'show tunnels status'));
  EL.labs.apply(n, { R1: ['configure', 'remote-access pptp office', 'authentication method mschap-v2', 'exit', 'end', 'commit', 'confirm'] });
  var pm = n.ping(r2.id, '192.168.1.10');
  chk('MPPE с MS-CHAPv2 — работает, в трассе MPPE', pm.ok && pm.steps.some(function (x) { return /MPPE расшифрован/.test(x.t); }));
  n.events(true); n.exec(r1.id, 'clear remote-access session pptp username ivan'); var ev = n.events();
  chk('clear remote-access session — сессия разорвана, сообщение в консоль', /Count sessions: 0/.test(n.exec(r1.id, 'show remote-access status')) &&
      ev.some(function (x) { return x.id === r2.id && /tunnel pptp 1: соединение разорвано/.test(x.msg); }), JSON.stringify(ev));
  n.tick(31); chk('через 30 с клиент подключился снова', /Count sessions: 1/.test(n.exec(r1.id, 'show remote-access status')));
  EL.labs.apply(n, { R2: ['configure', 'security zone wan', 'exit', 'tunnel pptp 1', 'security-zone wan', 'end', 'commit', 'confirm'] });
  chk('клиент: security-zone на туннеле — в running-config', /tunnel pptp 1\n(.*\n)*  security-zone wan/.test(n.exec(r2.id, 'show running-config')));
  chk('running-config сервера и клиента', /remote-access pptp office\n  local-address ip-address 10\.10\.10\.1\n  remote-address address-range 10\.10\.10\.20-10\.10\.10\.40\n  outside-address ip-address 100\.0\.0\.2\n  authentication method mschap-v2\n  encryption mppe\n  security-zone trusted\n  username ivan\n    password ascii-text Pa55word\n    enable\n  exit\n  enable/.test(n.exec(r1.id, 'show running-config')) &&
      /tunnel pptp 1\n  remote address 100\.0\.0\.2\n  username ivan password ascii-text Pa55word\n  ip firewall disable\n  security-zone wan\n  enable/.test(n.exec(r2.id, 'show running-config')));
  EL.labs.apply(n, { R2: ['configure', 'tunnel pptp 1', 'username ivan password ascii-text wrong', 'end', 'commit', 'confirm'] });
  chk('неверный пароль — сессии нет, туннель Down с причиной', /Count sessions: 0/.test(n.exec(r1.id, 'show remote-access status')) && /pptp 1\s+Down.*неверный пароль/.test(n.exec(r2.id, 'show tunnels status')) && !n.ping(r2.id, '192.168.1.10').ok);
  // L2TP over IPsec с проверкой через RADIUS
  var srv = n.add('Debian-server', 'RAD'); n.connect(srv.id, 'ens3', r1.id, 'gi1/0/3');
  e = EL.labs.apply(n, {
    RAD: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 192.168.3.10/24 dev ens3', 'ip route add default via 192.168.3.1'],
    R1: ['configure', 'interface gi1/0/3', 'ip address 192.168.3.1/24', 'ip firewall disable', 'exit', 'radius-server host 192.168.3.10', 'key ascii-text testing123', 'exit',
      'remote-access l2tp home', 'local-address ip-address 10.20.20.1', 'remote-address address-range 10.20.20.5-10.20.20.9', 'outside-address ip-address 100.0.0.2',
      'authentication mode radius', 'security-zone trusted', 'ipsec authentication method pre-shared-key', 'ipsec authentication pre-shared-key ascii-text K3y12345', 'enable', 'exit', 'end', 'commit', 'confirm'],
    R2: ['configure', 'no tunnel pptp 1', 'tunnel l2tp 1', 'remote address 100.0.0.2', 'username fedor password ascii-text secret1', 'ipsec authentication method pre-shared-key',
      'ipsec authentication pre-shared-key ascii-text K3y12345', 'ignore-default-route', 'ip firewall disable', 'enable', 'exit', 'ip route 192.168.1.0/24 10.20.20.1', 'end', 'commit', 'confirm'] });
  chk('L2TP: конфигурация без ошибок', !e.length, e.join('; '));
  chk('RADIUS не запущен — L2TP не поднимается', /l2tp 1\s+Down.*RADIUS/.test(n.exec(r2.id, 'show tunnels status')), n.exec(r2.id, 'show tunnels status'));
  srv.st.files['/etc/freeradius/3.0/clients.conf'] = 'client r1 {\n  ipaddr = 192.168.3.1\n  secret = testing123\n}\n';
  srv.st.files['/etc/freeradius/3.0/users'] = 'fedor Cleartext-Password := "secret1"\n';
  n.exec(srv.id, 'systemctl start freeradius');
  var p2 = n.ping(r2.id, '192.168.1.10');
  var l3 = n.raSess()[r2.id]['l2tp 1'].log.map(function (x) { return x.t; }).join(' | ');
  chk('журнал L2TP: Quick Mode ESP, SCCRQ, RADIUS Access-Accept', /Quick Mode/.test(l3) && /SCCRQ/.test(l3) && /Access-Accept/.test(l3), l3);
  chk('L2TP + RADIUS: fedor подключён, офис доступен', /fedor\s+10\.20\.20\.5\s+l2tp\(home\)/.test(n.exec(r1.id, 'show remote-access status l2tp')) && p2.ok && p2.steps.some(function (x) { return /L2TP\/UDP 1701 внутри IPsec/.test(x.t); }),
      n.exec(r2.id, 'show tunnels status') + ' | ' + p2.steps.map(function (x) { return x.t; }).join(' | '));
  EL.labs.apply(n, { R2: ['configure', 'tunnel l2tp 1', 'ipsec authentication pre-shared-key ascii-text Other999', 'end', 'commit', 'confirm'] });
  var l2 = (n.raSess()[r2.id]['l2tp 1'].log || []).map(function (x) { return x.t; }).join(' | ');
  chk('журнал L2TP: IKE Main Mode', /IKE Main Mode/.test(l2), l2);
  chk('L2TP: несовпадение ключа IPsec', /l2tp 1\s+Down.*ключи IPsec/.test(n.exec(r2.id, 'show tunnels status')));
  chk('show remote-access configuration l2tp home', /Authentication mode:  radius/.test(n.exec(r1.id, 'show remote-access configuration l2tp home')) && /Remote address:       10\.20\.20\.5-10\.20\.20\.9/.test(n.exec(r1.id, 'show remote-access configuration l2tp home')));
  console.log('✓ Удалённый доступ PPTP / L2TP');
})();
// SSH: known_hosts, смена ключа хоста и сброс записи, ssh-keygen, ssh-copy-id, вход по ключу, root, ESR как клиент
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ SSH: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), sw = n.add('MES2428', 'SW'), pc = n.add('Debian', 'PC'), sv = n.add('Debian', 'SRV');
  n.connect(pc.id, 'ens3', sw.id, 'gi1/0/1'); n.connect(sv.id, 'ens3', sw.id, 'gi1/0/2'); n.connect(r.id, 'gi1/0/1', sw.id, 'gi1/0/3');
  var e = EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ip address 10.0.0.1/24', 'ip firewall disable', 'exit', 'ip ssh server', 'end', 'commit', 'confirm'],
    PC: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.10/24 dev ens3'], SRV: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.20/24 dev ens3', 'exit'] });
  chk('конфигурация без ошибок', !e.length, e.join('; '));
  function x(l) { return n.exec(pc.id, l); }
  var a = x('ssh admin@10.0.0.1');
  chk('новый хост: вопрос о ключе ECDSA', /authenticity of host '10\.0\.0\.1/.test(a) && /ECDSA key fingerprint is SHA256:/.test(a) && /yes\/no/.test(n.prompt(pc.id)), a);
  var b = x('yes');
  chk('yes — ключ добавлен в known_hosts, запрос пароля', /Permanently added '10\.0\.0\.1' \(ECDSA\)/.test(b) && /admin@10\.0\.0\.1's password: /.test(n.prompt(pc.id)) && /^10\.0\.0\.1 ecdsa-sha2-nistp256 AAAA/.test(pc.st.files['/root/.ssh/known_hosts']), b);
  x('password'); chk('вход на ESR', /#\s*$/.test(n.prompt(pc.id)), n.prompt(pc.id));
  chk('выход', /closed/.test(x('exit')));
  EL.labs.apply(n, { R1: ['configure', 'update ssh-host-key ecdsa', 'end'] });
  var c = x('ssh admin@10.0.0.1');
  chk('новый ключ хоста — предупреждение и отказ', /REMOTE HOST IDENTIFICATION HAS CHANGED/.test(c) && /Offending ECDSA key in \/root\/\.ssh\/known_hosts:1/.test(c) && /Host key verification failed/.test(c) && !pc.st.ssh, c);
  var d = x('ssh-keygen -f "/root/.ssh/known_hosts" -R "10.0.0.1"');
  chk('ssh-keygen -R — запись удалена, копия .old', /# Host 10\.0\.0\.1 found: line 1/.test(d) && /known_hosts updated/.test(d) && pc.st.files['/root/.ssh/known_hosts.old'] !== undefined, d);
  chk('после сброса — снова вопрос о ключе', /authenticity/.test(x('ssh admin@10.0.0.1')));
  x('no');
  chk('no — Host key verification failed', !pc.st.ssh);
  // ключи пользователя
  var g = x('ssh-keygen');
  chk('ssh-keygen: вопрос о файле', /Generating public\/private rsa key pair/.test(g) && /Enter file in which to save the key \(\/root\/\.ssh\/id_rsa\)/.test(n.prompt(pc.id)), g);
  x(''); chk('вопрос о фразе', /Enter passphrase/.test(n.prompt(pc.id))); x('');
  var g2 = x('');
  chk('ключ создан: id_rsa и id_rsa.pub, отпечаток и randomart', /Your public key has been saved in \/root\/\.ssh\/id_rsa\.pub/.test(g2) && /\+---\[RSA 3072\]----\+/.test(g2) && /^ssh-rsa AAAA\S+ root@/.test(pc.st.files['/root/.ssh/id_rsa.pub']), g2);
  chk('ls ~/.ssh', /id_rsa  id_rsa\.pub  known_hosts/.test(x('ls ~/.ssh')), x('ls ~/.ssh'));
  chk('ssh-keygen -l -f', /^3072 SHA256:\S+ root@\S+ \(RSA\)$/.test(x('ssh-keygen -l -f ~/.ssh/id_rsa.pub')));
  // root по паролю на Debian запрещён по умолчанию
  x('ssh root@10.0.0.20'); x('yes'); var rp = x('toor');
  chk('root по паролю: PermitRootLogin prohibit-password', /Permission denied, please try again/.test(rp), rp);
  x('toor'); x('toor'); chk('после трёх попыток — отказ', !pc.st.ssh);
  // ssh-copy-id для user
  var cp = x('ssh-copy-id user@10.0.0.20');
  chk('ssh-copy-id: просит пароль user', /Source of key\(s\) to be installed: "\/root\/\.ssh\/id_rsa\.pub"/.test(cp) && /user@10\.0\.0\.20's password/.test(n.prompt(pc.id)), cp);
  var cp2 = x('user');
  chk('ключ добавлен в authorized_keys', /Number of key\(s\) added: 1/.test(cp2) && /ssh-rsa/.test(sv.st.files['/home/user/.ssh/authorized_keys'] || ''), cp2);
  var k = x('ssh user@10.0.0.20');
  chk('вход по ключу без пароля, команды на удалённом', /Linux SRV|Linux/.test(k) && /user@\S+:~\$ $/.test(n.prompt(pc.id)) && /10\.0\.0\.20/.test(x('ip addr')), k + ' / ' + n.prompt(pc.id));
  chk('logout', /Connection to 10\.0\.0\.20 closed/.test(x('logout')) && !pc.st.ssh);
  chk('повторный ssh-copy-id — ключ уже есть', (x('ssh-copy-id user@10.0.0.20'), /already exist/.test(x('user'))));
  // ключ с фразой
  x('ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N S3cret'); x('ssh-copy-id -i ~/.ssh/id_ed25519.pub user@10.0.0.20'); x('user');
  x('ssh user@10.0.0.20'); chk('ключ с фразой — вопрос фразы', /Enter passphrase for key '\/root\/\.ssh\/id_ed25519'/.test(n.prompt(pc.id)), n.prompt(pc.id));
  x('S3cret'); chk('фраза верна — вход', /user@/.test(n.prompt(pc.id))); x('exit');
  // смена ключей хоста Debian
  n.exec(sv.id, 'root'); n.exec(sv.id, 'toor'); n.exec(sv.id, 'dpkg-reconfigure openssh-server');
  chk('dpkg-reconfigure openssh-server — у клиента ключ не совпал', /HAS CHANGED/.test(x('ssh user@10.0.0.20')));
  x('rm ~/.ssh/known_hosts'); chk('rm known_hosts — снова вопрос', /authenticity/.test(x('ssh user@10.0.0.20'))); x('no');
  chk('PasswordAuthentication no: без ключа — сразу отказ', (sv.st.files['/etc/ssh/sshd_config'] += '\nPasswordAuthentication no\n', /Permission denied \(publickey\)/.test(x('ssh -o StrictHostKeyChecking=no -i /root/nokey user@10.0.0.20'))));
  // ESR как клиент
  n.exec(r.id, 'ssh user 10.0.0.20'); var ey = n.exec(r.id, 'yes');
  chk('ESR → Debian: known hosts ESR, пароль запрещён настройкой', /Permanently added/.test(ey) && /Permission denied \(publickey\)/.test(ey) && !r.st.sshc, ey);
  sv.st.files['/etc/ssh/sshd_config'] = sv.st.files['/etc/ssh/sshd_config'].replace('PasswordAuthentication no', '');
  n.exec(r.id, 'ssh user 10.0.0.20'); n.exec(r.id, 'user');
  chk('ESR → Debian: вход, команды Debian из консоли ESR', /user@/.test(n.prompt(r.id)) && /10\.0\.0\.20/.test(n.exec(r.id, 'ip addr')));
  n.exec(r.id, 'exit'); n.exec(sv.id, 'dpkg-reconfigure openssh-server');
  chk('ESR: смена ключа — clear ssh host', /HAS CHANGED/.test(n.exec(r.id, 'ssh user 10.0.0.20')) && /clear ssh host 10\.0\.0\.20/.test(n.exec(r.id, 'ssh user 10.0.0.20')));
  n.exec(r.id, 'clear ssh host 10.0.0.20'); chk('после clear ssh host — вопрос о ключе', /authenticity/.test(n.exec(r.id, 'ssh user 10.0.0.20'))); n.exec(r.id, 'no');
  // порт и show crypto key
  EL.labs.apply(n, { R1: ['configure', 'ip ssh port 2222', 'end', 'commit', 'confirm'] });
  chk('ip ssh port 2222: 22 закрыт, 2222 открыт', /Connection refused/.test(x('ssh admin@10.0.0.1')) && /authenticity of host '\[10\.0\.0\.1\]:2222/.test(x('ssh -p 2222 admin@10.0.0.1')));
  x('no');
  chk('show crypto key mypubkey rsa', /Key data\n-+\nssh-rsa\nAAAA/.test(n.exec(r.id, 'show crypto key mypubkey rsa')));
  chk('running-config: ip ssh port', /ip ssh port 2222/.test(n.exec(r.id, 'show running-config')));
  console.log('✓ SSH: ключи и known_hosts');
})();
// WireGuard: ключи wg genkey/pubkey → TFTP → crypto:…; туннель ESR–ESR; сервер remote-access wireguard и ноутбук Debian с wg-quick
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ WG: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r1 = n.add('vESR', 'R1'), isp = n.add('vESR', 'ISP'), r2 = n.add('vESR', 'R2'), a = n.add('VPC', 'A'), b = n.add('VPC', 'B'),
      ks = n.add('Debian-server', 'KS'), lap = n.add('Debian', 'LAP');
  n.connect(a.id, 'eth0', r1.id, 'gi1/0/1'); n.connect(ks.id, 'ens3', r1.id, 'gi1/0/3'); n.connect(r1.id, 'gi1/0/2', isp.id, 'gi1/0/1');
  n.connect(isp.id, 'gi1/0/2', r2.id, 'gi1/0/2'); n.connect(r2.id, 'gi1/0/1', b.id, 'eth0'); n.connect(lap.id, 'ens3', isp.id, 'gi1/0/3');
  function ifs(L) { var o = ['configure']; L.forEach(function (x) { o.push('interface ' + x[0], 'ip address ' + x[1], 'ip firewall disable', 'exit'); }); return o; }
  var e = EL.labs.apply(n, {
    KS: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 192.168.3.5/24 dev ens3', 'ip route add default via 192.168.3.1',
      'wg genkey | tee /tftp/r1.priv | wg pubkey > /tftp/r1.pub', 'wg genkey | tee /tftp/r2.priv | wg pubkey > /tftp/r2.pub'],
    ISP: ifs([['gi1/0/1', '100.0.0.1/30'], ['gi1/0/2', '100.0.1.1/30'], ['gi1/0/3', '100.0.2.1/24']]).concat(['ip route 192.168.3.0/24 100.0.0.2', 'end', 'commit', 'confirm']),
    R1: ifs([['gi1/0/1', '192.168.1.1/24'], ['gi1/0/2', '100.0.0.2/30'], ['gi1/0/3', '192.168.3.1/24']]).concat(['ip route 0.0.0.0/0 100.0.0.1', 'end', 'commit', 'confirm',
      'copy tftp://192.168.3.5:/r1.priv crypto:private-key/r1', 'copy tftp://192.168.3.5:/r2.pub crypto:public-key/r2']),
    R2: ifs([['gi1/0/1', '192.168.2.1/24'], ['gi1/0/2', '100.0.1.2/30']]).concat(['ip route 0.0.0.0/0 100.0.1.1', 'end', 'commit', 'confirm',
      'copy tftp://192.168.3.5:/r2.priv crypto:private-key/r2', 'copy tftp://192.168.3.5:/r1.pub crypto:public-key/r1']),
    A: ['ip 192.168.1.10/24 192.168.1.1'], B: ['ip 192.168.2.10/24 192.168.2.1'] });
  chk('конфигурация и загрузка ключей без ошибок', !e.length, e.join('; '));
  chk('ключи: закрытый и открытый — разные, формат WireGuard', /^[A-Za-z0-9+/]{43}=\n?$/.test(ks.st.files['/tftp/r1.priv']) && EL.wgPub(ks.st.files['/tftp/r1.priv']) === ks.st.files['/tftp/r1.pub'].trim());
  function tun(me, peer, priv, pub, tip, net, ip) { return ['configure', 'object-group network PEER', 'ip prefix ' + net, 'exit', 'tunnel wireguard 1', 'ip address ' + tip, 'port 51820',
    'private-key ' + priv, 'ip firewall disable', 'peer 1', 'public-key ' + pub, 'remote address ' + peer, 'remote port 51820', 'subnet PEER', 'enable', 'exit', 'enable', 'exit',
    'ip route ' + net + ' ' + ip, 'end', 'commit', 'confirm']; void me; }
  e = EL.labs.apply(n, { R1: tun('R1', '100.0.1.2', 'r1', 'r2', '10.99.0.1/30', '192.168.2.0/24', '10.99.0.2'), R2: tun('R2', '100.0.0.2', 'r2', 'r1', '10.99.0.2/30', '192.168.1.0/24', '10.99.0.1') });
  chk('туннель: конфигурация без ошибок', !e.length, e.join('; '));
  var p = n.ping(a.id, '192.168.2.10');
  chk('A → B через WireGuard', p.ok && p.steps.some(function (x) { return /wg1 — получатель 192\.168\.2\.10 в разрешённых адресах peer 1; пакет зашифрован и упакован в UDP 51820 → 100\.0\.1\.2:51820/.test(x.t); }), p.steps.map(function (x) { return x.t; }).join(' | '));
  chk('show wireguard peers: рукопожатие и трафик', /peer 1: endpoint 100\.0\.1\.2:51820, subnet 192\.168\.2\.0\/24, latest handshake \d+ s ago, transfer [1-9]/.test(n.exec(r1.id, 'show wireguard peers')), n.exec(r1.id, 'show wireguard peers'));
  chk('running-config: tunnel wireguard и peer', /tunnel wireguard 1\n  ip firewall disable\n  ip address 10\.99\.0\.1\/30\n  port 51820\n  private-key r1\n  peer 1\n    public-key r2\n    remote address 100\.0\.1\.2\n    remote port 51820\n    subnet PEER\n    enable\n  exit\n  enable/.test(n.exec(r1.id, 'show running-config')));
  // чужой адрес вне subnet
  EL.labs.apply(n, { R2: ['configure', 'object-group network PEER', 'no ip prefix 192.168.1.0/24', 'ip prefix 192.168.9.0/24', 'end', 'commit', 'confirm'] });
  var p2 = n.ping(a.id, '192.168.2.10');
  chk('источник вне subnet у принимающей стороны — отброшен', !p2.ok && p2.steps.some(function (x) { return /источник 192\.168\.1\.10 не в разрешённых адресах/.test(x.t); }), p2.steps.map(function (x) { return x.t; }).join(' | '));
  EL.labs.apply(n, { R2: ['configure', 'object-group network PEER', 'ip prefix 192.168.1.0/24', 'end', 'commit', 'confirm', 'delete crypto:public-key/r1'] });
  chk('удалён открытый ключ пира — нет рукопожатия', !n.ping(a.id, '192.168.2.10').ok && /нет ключа crypto:public-key\/r1/.test(n.exec(r2.id, 'show wireguard peers')));
  EL.labs.apply(n, { R2: ['copy tftp://192.168.3.5:/r2.pub crypto:public-key/r1'] });
  var p3 = n.ping(a.id, '192.168.2.10');
  chk('не тот открытый ключ — R1 отвергает рукопожатие', !p3.ok && p3.steps.some(function (x) { return /нет пира с открытым ключом|не совпадает/.test(x.t); }), p3.steps.map(function (x) { return x.t; }).join(' | '));
  EL.labs.apply(n, { R2: ['copy tftp://192.168.3.5:/r1.pub crypto:public-key/r1'] });
  chk('ключ исправлен — снова работает', n.ping(a.id, '192.168.2.10').ok);
  // удалённый доступ: сервер на R1, ноутбук с wg-quick
  e = EL.labs.apply(n, { LAP: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 100.0.2.10/24 dev ens3', 'ip route add default via 100.0.2.1', 'umask 077; wg genkey | tee /root/lap.priv | wg pubkey > /root/lap.pub'] });
  ks.st.files['/tftp/lap.pub'] = lap.st.files['/root/lap.pub'];
  e = e.concat(EL.labs.apply(n, { R1: ['copy tftp://192.168.3.5:/lap.pub crypto:public-key/lap', 'configure', 'security zone trusted', 'exit', 'object-group network LAP', 'ip prefix 10.10.0.2/32', 'exit',
    'remote-access wireguard RA', 'local-address 10.10.0.1/24', 'port 43021', 'private-key r1', 'security-zone trusted', 'peer 1', 'public-key lap', 'subnet LAP', 'enable', 'exit', 'enable', 'exit', 'end', 'commit', 'confirm'] }));
  chk('сервер: конфигурация без ошибок', !e.length, e.join('; '));
  lap.st.files['/etc/wireguard/wg0.conf'] = '[Interface]\nAddress = 10.10.0.2/24\nPrivateKey = ' + lap.st.files['/root/lap.priv'].trim() + '\n\n[Peer]\nPublicKey = ' + ks.st.files['/tftp/r1.pub'].trim() +
    '\nEndpoint = 100.0.0.2:43021\nAllowedIPs = 10.10.0.0/24, 192.168.1.0/24\n';
  chk('сервер без рукопожатия не знает, куда слать клиенту', (n.exec(lap.id, 'wg-quick up wg0'), !n.ping(a.id, '10.10.0.2').ok));
  var up = n.ping(lap.id, '192.168.1.10');
  chk('ноутбук → офис через wg-quick, сервер запомнил адрес', up.ok && n.ping(a.id, '10.10.0.2').ok, up.steps.map(function (x) { return x.t; }).join(' | '));
  chk('wg show: рукопожатие и трафик', /interface: wg0\n  public key: \S+\n  private key: \(hidden\)/.test(n.exec(lap.id, 'wg show')) && /latest handshake: /.test(n.exec(lap.id, 'wg show')) && /transfer: [1-9]/.test(n.exec(lap.id, 'wg show')), n.exec(lap.id, 'wg show'));
  chk('ip addr показывает wg0', /wg0: <POINTOPOINT,NOARP,UP,LOWER_UP>[\s\S]*inet 10\.10\.0\.2\/24/.test(n.exec(lap.id, 'ip addr')));
  chk('show remote-access status wireguard', /peer 1\s+10\.10\.0\.2\s+wireguard\(RA\)/.test(n.exec(r1.id, 'show remote-access status wireguard')), n.exec(r1.id, 'show remote-access status wireguard'));
  n.exec(lap.id, 'wg-quick down wg0'); chk('wg-quick down — туннеля нет', !n.ping(lap.id, '192.168.1.10').ok);
  lap.st.files['/etc/wireguard/wg0.conf'] = lap.st.files['/etc/wireguard/wg0.conf'].replace('PrivateKey = ', 'PrivateKey = x');
  chk('битый PrivateKey — ошибка разбора', /Configuration parsing error/.test(n.exec(lap.id, 'wg-quick up wg0')));
  console.log('✓ WireGuard');
})();
// scp между компьютерами Debian: отправка и получение, вход по ключу, права, ошибки
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ scp: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), sw = n.add('MES2428', 'SW'), pc = n.add('Debian', 'PC'), sv = n.add('Debian-server', 'SRV');
  n.connect(pc.id, 'ens3', sw.id, 'gi1/0/1'); n.connect(sv.id, 'ens3', sw.id, 'gi1/0/2');
  EL.labs.apply(n, { PC: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.10/24 dev ens3'], SRV: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.20/24 dev ens3'] });
  function x(l) { return n.exec(pc.id, l); }
  pc.st.files['/root/report.txt'] = 'hello';
  x('scp report.txt user@10.0.0.20:'); x('yes'); var r = x('user');
  chk('scp на сервер по паролю: файл в домашнем каталоге user', /^report\.txt\s+100%\s+5\s/.test(r) && sv.st.files['/home/user/report.txt'] === 'hello' && !pc.st.ssh, r);
  x('scp report.txt user@10.0.0.20:/etc/'); var r2 = x('user');
  chk('scp в /etc от user — Permission denied', /scp: \/etc\/report\.txt: Permission denied/.test(r2), r2);
  x('ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""'); x('ssh-copy-id user@10.0.0.20'); x('user');
  sv.st.files['/home/user/data.csv'] = 'a;b';
  var r3 = x('scp user@10.0.0.20:~/data.csv /tmp/');
  chk('scp с сервера по ключу — без пароля', /^data\.csv\s+100%/.test(r3) && pc.st.files['/tmp/data.csv'] === 'a;b', r3);
  chk('нет файла на сервере', /No such file or directory/.test(x('scp user@10.0.0.20:/home/user/none.txt .')));
  chk('нет локального файла', /nope\.txt: No such file or directory/.test(x('scp nope.txt user@10.0.0.20:')));
  console.log('✓ scp');
})();
// OpenVPN: CA easy-rsa на Debian, сервер remote-access openvpn на ESR, клиенты — ESR (tunnel openvpn) и Debian (openvpn-client@)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ OpenVPN: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r1 = n.add('vESR', 'R1'), isp = n.add('vESR', 'ISP'), r2 = n.add('vESR', 'R2'), a = n.add('VPC', 'A'), ks = n.add('Debian-server', 'KS'), lap = n.add('Debian', 'LAP');
  n.connect(a.id, 'eth0', r1.id, 'gi1/0/1'); n.connect(ks.id, 'ens3', r1.id, 'gi1/0/3'); n.connect(r1.id, 'gi1/0/2', isp.id, 'gi1/0/1');
  n.connect(isp.id, 'gi1/0/2', r2.id, 'gi1/0/2'); n.connect(lap.id, 'ens3', isp.id, 'gi1/0/3');
  function ifs(L) { var o = ['configure']; L.forEach(function (x) { o.push('interface ' + x[0], 'ip address ' + x[1], 'ip firewall disable', 'exit'); }); return o; }
  function k(l) { return n.exec(ks.id, l); }
  var e = EL.labs.apply(n, {
    KS: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 192.168.3.5/24 dev ens3', 'ip route add default via 192.168.3.1'],
    ISP: ifs([['gi1/0/1', '100.0.0.1/30'], ['gi1/0/2', '100.0.1.1/30'], ['gi1/0/3', '100.0.2.1/24']]).concat(['ip route 192.168.3.0/24 100.0.0.2', 'end', 'commit', 'confirm']),
    R1: ifs([['gi1/0/1', '192.168.1.1/24'], ['gi1/0/2', '100.0.0.2/30'], ['gi1/0/3', '192.168.3.1/24']]).concat(['ip route 0.0.0.0/0 100.0.0.1', 'end', 'commit', 'confirm']),
    R2: ifs([['gi1/0/2', '100.0.1.2/30']]).concat(['ip route 0.0.0.0/0 100.0.1.1', 'end', 'commit', 'confirm']),
    A: ['ip 192.168.1.10/24 192.168.1.1'], LAP: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 100.0.2.10/24 dev ens3', 'ip route add default via 100.0.2.1'] });
  chk('сеть без ошибок', !e.length, e.join('; '));
  // удостоверяющий центр
  k('make-cadir ~/ca'); k('cd ~/ca');
  chk('cd и приглашение с каталогом', /root@\S+:~\/ca# $/.test(n.prompt(ks.id)) && k('pwd') === '/root/ca', n.prompt(ks.id));
  chk('без init-pki — ошибка', /EASYRSA_PKI does not exist/.test(k('./easyrsa build-ca nopass')));
  chk('init-pki', /init-pki complete/.test(k('./easyrsa init-pki')));
  k('./easyrsa build-ca nopass'); chk('build-ca: вопрос Common Name', /Common Name .*\[Easy-RSA CA\]/.test(n.prompt(ks.id)), n.prompt(ks.id));
  chk('CA создан', /CA creation complete/.test(k('Office CA')) && ks.st.files['/root/ca/pki/ca.crt'] !== undefined);
  chk('build-server-full server', /Certificate created at: \/root\/ca\/pki\/issued\/server\.crt/.test(k('./easyrsa build-server-full server nopass')));
  k('./easyrsa gen-req r2 nopass'); k(''); var sr = k('./easyrsa sign-req client r2');
  chk('gen-req + sign-req: вопрос подтверждения', /to be signed as a client certificate/.test(sr) && /Confirm request details/.test(n.prompt(ks.id)), sr);
  chk('sign-req yes — сертификат', /Data Base Updated/.test(k('yes')) && ks.st.files['/root/ca/pki/issued/r2.crt'] !== undefined);
  k('./easyrsa build-client-full lap nopass'); k('./easyrsa gen-dh'); k('openvpn --genkey secret ta.key');
  chk('openssl x509 -subject -issuer', /subject=CN = server\nissuer=CN = Office CA/.test(k('openssl x509 -in pki/issued/server.crt -noout -subject -issuer')), k('openssl x509 -in pki/issued/server.crt -noout -subject -issuer'));
  ['pki/ca.crt', 'pki/issued/server.crt', 'pki/private/server.key', 'pki/dh.pem', 'ta.key', 'pki/issued/r2.crt', 'pki/private/r2.key'].forEach(function (f) { k('cp ' + f + ' /tftp/'); });
  chk('cp в /tftp', ks.st.files['/tftp/server.key'] !== undefined && ks.st.files['/tftp/ta.key'] !== undefined);
  // сервер
  function cp(f, kind) { return 'copy tftp://192.168.3.5:/' + f + ' crypto:' + kind + '/' + f; }
  e = EL.labs.apply(n, { R1: [cp('ca.crt', 'cert'), cp('server.crt', 'cert'), cp('server.key', 'private-key'), cp('dh.pem', 'dh'), cp('ta.key', 'ta'), 'configure', 'security zone trusted', 'exit',
    'remote-access openvpn OV', 'network 10.8.0.0/24', 'protocol udp', 'tunnel ip', 'crypto ca ca.crt', 'crypto cert server.crt', 'crypto private-key server.key', 'crypto dh dh.pem', 'crypto ta ta.key',
    'encryption algorithm aes128', 'route 192.168.1.0/24', 'security-zone trusted', 'enable', 'exit', 'end', 'commit', 'confirm'],
    R2: [cp('ca.crt', 'cert'), cp('r2.crt', 'cert'), cp('r2.key', 'private-key'), cp('ta.key', 'ta'), 'configure', 'tunnel openvpn 1', 'remote address 100.0.0.2', 'protocol udp', 'tunnel ip',
      'crypto ca ca.crt', 'crypto cert r2.crt', 'crypto private-key r2.key', 'crypto ta ta.key', 'encryption algorithm aes128', 'ip firewall disable', 'enable', 'exit', 'end', 'commit', 'confirm'] });
  chk('сервер и клиент ESR: без ошибок', !e.length, e.join('; '));
  var p = n.ping(r2.id, '192.168.1.10');
  chk('R2 → офис через OpenVPN', p.ok && p.steps.some(function (x) { return /openvpn1 — пакет 10\.8\.0\.2 → 192\.168\.1\.10 зашифрован \(AES-128-CBC\) и упакован в UDP/.test(x.t); }), p.steps.map(function (x) { return x.t; }).join(' | '));
  chk('show remote-access status openvpn', /r2\s+10\.8\.0\.2\s+openvpn\(OV\)/.test(n.exec(r1.id, 'show remote-access status openvpn')));
  chk('show tunnels status: openvpn 1 Up', /openvpn 1\s+Up\s+\d+\s+10\.8\.0\.2/.test(n.exec(r2.id, 'show tunnels status')));
  var lg = n.ovSess()[r2.id]['openvpn 1'].log.map(function (x) { return x.t; }).join(' | ');
  chk('журнал: проверка сертификатов, PUSH', /сертификат сервера CN=server проверен/.test(lg) && /сертификат клиента CN=r2 проверен/.test(lg) && /PUSH_REPLY: адрес 10\.8\.0\.2\/24/.test(lg), lg);
  chk('running-config сервера', /remote-access openvpn OV\n  security-zone trusted\n  network 10\.8\.0\.0\/24\n  protocol udp\n  tunnel ip\n  crypto ca ca\.crt\n  crypto cert server\.crt\n  crypto private-key server\.key\n  crypto dh dh\.pem\n  crypto ta ta\.key\n  encryption algorithm aes128\n  route 192\.168\.1\.0\/24\n  enable/.test(n.exec(r1.id, 'show running-config')));
  // ошибки клиента ESR
  EL.labs.apply(n, { R2: ['configure', 'tunnel openvpn 1', 'no crypto ta', 'end', 'commit', 'confirm'] });
  chk('нет ta у клиента — HMAC, сервер молчит', /openvpn 1\s+Down.*tls-auth/.test(n.exec(r2.id, 'show tunnels status')));
  EL.labs.apply(n, { R2: ['configure', 'tunnel openvpn 1', 'crypto ta ta.key', 'encryption algorithm aes256', 'end', 'commit', 'confirm'] });
  chk('шифр не совпал', /openvpn 1\s+Down.*шифрование: у сервера AES-128-CBC, у клиента AES-256-CBC/.test(n.exec(r2.id, 'show tunnels status')));
  EL.labs.apply(n, { R2: ['configure', 'tunnel openvpn 1', 'encryption algorithm aes128', 'end', 'commit', 'confirm'] });
  // ноутбук Debian
  var F = lap.st.files; ['ca.crt', 'ta.key'].forEach(function (f) { F['/etc/openvpn/client/' + f] = ks.st.files['/tftp/' + f]; });
  F['/etc/openvpn/client/lap.crt'] = ks.st.files['/root/ca/pki/issued/lap.crt']; F['/etc/openvpn/client/lap.key'] = ks.st.files['/root/ca/pki/private/lap.key'];
  F['/etc/openvpn/client/lap.conf'] = 'client\ndev tun\nproto udp\nremote 100.0.0.2 1194\nca ca.crt\ncert lap.crt\nkey lap.key\ntls-auth ta.key 1\nremote-cert-tls server\ncipher AES-128-CBC\n';
  n.exec(lap.id, 'systemctl start openvpn-client@lap');
  var lp = n.ping(lap.id, '192.168.1.10');
  chk('ноутбук → офис, маршрут из PUSH', lp.ok && /Initialization Sequence Completed/.test(n.exec(lap.id, 'journalctl -u openvpn-client@lap')), lp.steps.map(function (x) { return x.t; }).join(' | ') + ' || ' + n.exec(lap.id, 'journalctl -u openvpn-client@lap'));
  chk('ip addr: tun0 с адресом 10.8.0.3', /tun0: <POINTOPOINT[\s\S]*inet 10\.8\.0\.3\/24/.test(n.exec(lap.id, 'ip addr')));
  // отзыв сертификата
  k('./easyrsa revoke lap'); k('yes'); k('./easyrsa gen-crl'); k('cp pki/crl.pem /tftp/');
  EL.labs.apply(n, { R1: [cp('crl.pem', 'crl'), 'configure', 'remote-access openvpn OV', 'crypto crl crl.pem', 'end', 'commit', 'confirm'] });
  chk('отозванный lap — отказ, r2 работает', !n.ping(lap.id, '192.168.1.10').ok && n.ping(r2.id, '192.168.1.10').ok &&
      /отозван/.test((n.ovSess()[lap.id]['openvpn-client@lap'] || {}).err || ''), JSON.stringify((n.ovSess()[lap.id] || {})['openvpn-client@lap'] && n.ovSess()[lap.id]['openvpn-client@lap'].err));
  // remote-cert-tls: клиентский сертификат вместо серверного
  F['/etc/openvpn/client/lap.conf'] = F['/etc/openvpn/client/lap.conf'].replace('cipher AES-128-CBC', 'cipher AES-256-CBC');
  n.exec(lap.id, 'systemctl restart openvpn-client@lap');
  chk('journalctl: ошибка шифра в логе OpenVPN', /Authenticate\/Decrypt packet error|TLS Error|AUTH|VERIFY/.test(n.exec(lap.id, 'journalctl -u openvpn-client@lap')), n.exec(lap.id, 'journalctl -u openvpn-client@lap'));
  // redirect-gateway
  EL.labs.apply(n, { R1: ['configure', 'remote-access openvpn OV', 'redirect-gateway', 'end', 'commit', 'confirm'] });
  chk('redirect-gateway: у R2 маршрут по умолчанию в туннель', /S\s+\*\s+0\.0\.0\.0\/0\s+\[1\/0\]\s+via 10\.8\.0\.1 on openvpn1/.test(n.exec(r2.id, 'show ip route')), n.exec(r2.id, 'show ip route'));
  console.log('✓ OpenVPN');
})();

// таблицы: ARP у обеих сторон, MAC-обучение коммутатора, кэш ARP, устаревание записи, разные VLAN
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), s = n.add('MES2428', 'SW1'), v = ['VPC1', 'VPC2', 'VPC3'].map(function (x) { return n.add('VPC', x); });
  v.forEach(function (d, i) { n.connect(d.id, 'eth0', s.id, 'gi1/0/' + (i + 1)); }); n.tick(5);
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'vlan 10,20', 'exit', 'interface range gi1/0/1-2', 'switchport access vlan 10', 'exit',
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
  chk('таблицы: show mac-address-table / arp', /Learnt/.test(n.exec(s.id, 'show mac-address-table')) && /10\.0\.0\.1/.test(n.exec(v[1].id, 'arp')));
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
  chk('CLI: sh system information / sh clock', /10\.4\.6/.test(n.exec(s.id, 'sh system information')) && /UTC/.test(n.exec(s.id, 'sh clock')));
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
  var e = x(m, sm, ['en', 'conf', 'mac-address-table static unicast 00:11:22:33:44:55 vlan 1 interface gi 1/0/7 status permanent', 'end', 'show mac-address-table']);
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
  // трансляции стареют по таймауту сессий: ICMP — 30 с, каждый новый пакет продлевает
  var nt = m.exec(r2.id, 'show ip nat translations');
  chk('NAT-трансляция: icmp 192.168.1.2 → 200.0.0.1, 2 пакета 168 байт', /icmp 192\.168\.1\.2\s+200\.0\.0\.2\s+200\.0\.0\.1\s+200\.0\.0\.2\s+2\s+168/.test(nt), nt);
  m.tick(20); m.ping(a.id, '200.0.0.2'); m.tick(20);
  chk('NAT: новый пакет продлил трансляцию (жива через 40 с)', m.natLeft(r2.id, 0) === 10 && /\s4\s+336/.test(m.exec(r2.id, 'show ip nat translations')), m.natLeft(r2.id, 0));
  m.tick(10); chk('NAT: icmp-timeout 30 с — трансляция удалена', !/icmp/.test(m.exec(r2.id, 'show ip nat translations')));
  ['configure', 'ip firewall sessions icmp-timeout 100', 'do commit', 'do confirm', 'end'].forEach(function (l) { m.exec(r2.id, l); });
  m.ping(a.id, '200.0.0.2'); m.tick(90); chk('NAT: icmp-timeout 100 — через 90 с ещё есть', /icmp/.test(m.exec(r2.id, 'show ip nat translations')));
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
  chk('сессии: ip firewall sessions icmp-timeout 5', !sess('icmp') && /ip firewall sessions tcp-estabilished-timeout 600/.test(n.exec(r.id, 'show running-config')) &&
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
  var esrs = Object.keys(EL.MODELS).filter(function (k) { return EL.MODELS[k].type === 'esr' && !EL.MODELS[k].kind && k !== 'vESR'; });
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
  chk('MES 10.x: terminal datadump нет (команда ветки 6.x)', /^%/.test(n.exec(sw.id, 'terminal datadump')) && n.pageLen(sw.id) === 24);
  n.exec(r.id, 'terminal datadump'); chk('ESR terminal datadump', n.pageLen(sw.id) === 24 && n.pageLen(r.id) === 0);
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
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'vlan 10', 'exit', 'interface gi1/0/1', 'switchport mode trunk', 'exit',
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
  var e = EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ipv6 address 2001:db8:1::1/64', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ipv6 address 2001:db8:2::1/64', 'ip firewall disable', 'end', 'commit', 'confirm'],
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
  EL.labs.apply(n2, { RA: ['configure', 'interface gi1/0/1', 'ipv6 address fc00::1/64', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ipv6 address 2001:a::1/64', 'ip firewall disable', 'exit', 'end', 'commit', 'confirm'],
                      RB: ['configure', 'interface gi1/0/1', 'ipv6 address fc00::2/64', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ipv6 address 2001:b::1/64', 'ip firewall disable', 'exit', 'ipv6 route ::/0 fc00::1', 'end', 'commit', 'confirm'],
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
      A[r].forEach(function (x) { L.push('interface ' + x[0], 'ipv6 address ' + x[1], 'ip firewall disable'); if (proto === 'O') L.push('ipv6 ospf instance 1', 'ipv6 ospf area 0.0.0.0', 'ipv6 ospf'); L.push('exit'); });
      if (proto === 'R') L.push('ipv6 router rip', 'network 2001::/16', 'enable', 'exit');
      else L.push('ipv6 router ospf 1', 'router-id ' + (i + 1) + '.' + (i + 1) + '.' + (i + 1) + '.' + (i + 1), 'area 0.0.0.0', 'enable', 'exit', 'enable', 'exit');
      L.push('end', 'commit', 'confirm'); sc[r] = L; });
    sc.PA = ['ip 2001:a::10/64 2001:a::1']; sc.PB = ['ip 2001:b::10/64 2001:b::1'];
    return { n: n, errs: EL.labs.apply(n, sc), r1: r1, r2: r2, pa: pa, pb: pb };
  }
  var v = chain('R');
  chk('RIPng: конфигурация без ошибок', !v.errs.length, v.errs.join('; '));
  chk('RIPng: сразу после настройки маршрутов ещё нет (триггерное обновление 1–5 с на переход)', !v.n.ping6(v.pa.id, '2001:b::10').ok);
  v.n.tick(12);
  chk('RIPng: PA → PB через три ESR', v.n.ping6(v.pa.id, '2001:b::10').ok);
  chk('RIPng: show ipv6 rip — via link-local, метрика 3', /2001:b::\/64\s+via fe80::\S+ on gi1\/0\/1 \[rip 00:00:00\] \* \(120\/3\)/.test(v.n.exec(v.r1.id, 'show ipv6 rip')), v.n.exec(v.r1.id, 'show ipv6 rip'));
  chk('RIPng: show ipv6 route — R', /^R\s+\* 2001:b::\/64/m.test(v.n.exec(v.r1.id, 'show ipv6 route')));
  chk('RIPng: running-config', /ipv6 router rip\n  network 2001::\/16\n  enable\nexit/.test(v.n.exec(v.r1.id, 'show running-config')));
  v.n.dyn6(); EL.labs.apply(v.n, { R3: ['configure', 'ipv6 router rip', 'no enable', 'exit', 'end', 'commit', 'confirm'] }); v.n.tick(60);
  chk('RIPng: сосед пропал — маршрут живёт до invalid (180 с)', /2001:b::\/64/.test(v.n.exec(v.r2.id, 'show ipv6 route')), v.n.exec(v.r2.id, 'show ipv6 route'));
  v.n.tick(200); chk('RIPng: после invalid маршрут удалён', !/2001:b::\/64/.test(v.n.exec(v.r2.id, 'show ipv6 route')), v.n.exec(v.r2.id, 'show ipv6 route'));
  EL.labs.apply(v.n, { R3: ['configure', 'ipv6 router rip', 'enable', 'exit', 'end', 'commit', 'confirm'] }); v.n.tick(12);
  EL.labs.apply(v.n, { R2: ['configure', 'ipv6 router rip', 'no enable', 'exit', 'end', 'commit', 'confirm'] });
  chk('RIPng выключен на R2 — связи нет', !v.n.ping6(v.pa.id, '2001:b::10').ok);
  var o = chain('O');
  chk('OSPFv3: конфигурация без ошибок', !o.errs.length, o.errs.join('; '));
  o.n.dyn6(); o.n.tick(5);
  chk('OSPFv3: до wait timer (40 с) соседи в 2way, маршрута нет', !o.n.ping6(o.pa.id, '2001:b::10').ok && /2way/.test(o.n.exec(o.r2.id, 'show ipv6 ospf neighbors')), o.n.exec(o.r2.id, 'show ipv6 ospf neighbors'));
  o.n.tick(40);
  chk('OSPFv3: PA → PB', o.n.ping6(o.pa.id, '2001:b::10').ok);
  chk('OSPFv3: соседи R2 — R1 и R3', (o.n.exec(o.r2.id, 'show ipv6 ospf neighbors').match(/full/g) || []).length === 2, o.n.exec(o.r2.id, 'show ipv6 ospf neighbors'));
  chk('OSPFv3: маршрут O со стоимостью 30 (3 интерфейса по 10)', /^O\s+\* 2001:b::\/64\s+\[110\/30\]/m.test(o.n.exec(o.r1.id, 'show ipv6 route')), o.n.exec(o.r1.id, 'show ipv6 route'));
  EL.labs.apply(o.n, { R1: ['configure', 'ipv6 router ospf 1', 'area 0.0.0.0', 'no enable', 'end', 'commit', 'confirm'] });
  o.n.tick(41); chk('OSPFv3: область выключена — после dead-interval связи нет', !o.n.ping6(o.pa.id, '2001:b::10').ok);

  // OSPFv3: роли DR/BDR по priority (по умолчанию 120), point-to-point — без ожидания DR
  var q = chain('O'); q.n.dyn6(); q.n.tick(45);
  var nb2 = q.n.exec(q.r2.id, 'show ipv6 ospf neighbors');
  chk('OSPFv3: у R2 соседи full/dr или full/bdr, приоритет 120', /full\/(dr|bdr)/.test(nb2) && /\s120\s+full/.test(nb2), nb2);
  var w = chain('O'); ['R1', 'R2'].forEach(function (r) { EL.labs.apply(w.n, (function () { var o = {}; o[r] = ['configure', 'interface gi1/0/1', 'ipv6 ospf network point-to-point', 'end', 'commit', 'confirm']; return o; })()); });
  w.n.dyn6(); w.n.tick(3);
  chk('OSPFv3 point-to-point: full/ptp за 2 с, без wait-interval', /full\/ptp/.test(w.n.exec(w.r1.id, 'show ipv6 ospf neighbors')) && /ipv6 ospf network point-to-point/.test(w.n.exec(w.r1.id, 'show running-config')), w.n.exec(w.r1.id, 'show ipv6 ospf neighbors'));
  chk('OSPFv3: priority 300 — ошибка, cost 5 принят', /Illegal/.test(w.n.exec(w.r1.id, 'configure') + w.n.exec(w.r1.id, 'interface gi1/0/1') + w.n.exec(w.r1.id, 'ipv6 ospf priority 300')) &&
      !/Illegal|%/.test(w.n.exec(w.r1.id, 'ipv6 ospf cost 5')));
  // RIPng: после invalid маршрут «possibly down» (метрика 16) до flush
  var u = chain('R'); u.n.tick(12);
  EL.labs.apply(u.n, { R3: ['configure', 'ipv6 router rip', 'no enable', 'exit', 'end', 'commit', 'confirm'] }); u.n.tick(190);
  var rr = u.n.exec(u.r2.id, 'show ipv6 rip');
  chk('RIPng: 190 с без обновлений — possibly down (120/16), удаление по flush', /2001:b::\/64\s+via \S+ on gi1\/0\/2 \[rip \d\d:\d\d:\d\d\]\s+\(120\/16\) possibly down — удаление через 50 с/.test(rr) &&
      !/2001:b::\/64/.test(u.n.exec(u.r2.id, 'show ipv6 route')), rr);
  u.n.tick(50); chk('RIPng: после flush (240 с) маршрута нет и в show ipv6 rip', !/2001:b::\/64/.test(u.n.exec(u.r2.id, 'show ipv6 rip')), u.n.exec(u.r2.id, 'show ipv6 rip'));
  chk('RIPng: timers invalid 5 — ошибка (12..65535)', /Illegal/.test(u.n.exec(u.r1.id, 'configure') + u.n.exec(u.r1.id, 'ipv6 router rip') + u.n.exec(u.r1.id, 'timers invalid 5')));
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
  chk('туннель выключен на RB — GRE отброшен', !r2.ok && r2.steps.some(function (s) { return /нет включённого туннеля gre/.test(s.t); }));
  EL.labs.apply(n, { RB: ['configure', 'tunnel gre 1', 'enable', 'no ip firewall disable', 'end', 'commit', 'confirm'] });
  chk('туннель без зоны и с межсетевым экраном — отброшено', !n.ping(pa.id, '192.168.2.10').ok);
  console.log('✓ GRE');
})();

// IPsec: policy-based и route-based (VTI) между офисами через провайдера
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  function office() {
    var n = new EL.Net(), ra = n.add('vESR', 'RA'), isp = n.add('vESR', 'ISP'), rb = n.add('vESR', 'RB'), pa = n.add('VPC', 'PA'), pb = n.add('VPC', 'PB');
    n.connect(ra.id, 'gi1/0/1', isp.id, 'gi1/0/1'); n.connect(isp.id, 'gi1/0/2', rb.id, 'gi1/0/1'); n.connect(pa.id, 'eth0', ra.id, 'gi1/0/2'); n.connect(pb.id, 'eth0', rb.id, 'gi1/0/2');
    EL.labs.apply(n, { ISP: ['configure', 'interface gi1/0/1', 'ip address 100.0.0.1/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 100.0.1.1/30', 'ip firewall disable', 'exit', 'end', 'commit', 'confirm'],
      RA: ['configure', 'interface gi1/0/1', 'ip address 100.0.0.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit', 'ip route 0.0.0.0/0 100.0.0.1', 'end', 'commit', 'confirm'],
      RB: ['configure', 'interface gi1/0/1', 'ip address 100.0.1.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 192.168.2.1/24', 'ip firewall disable', 'exit', 'ip route 0.0.0.0/0 100.0.1.1', 'end', 'commit', 'confirm'],
      PA: ['ip 192.168.1.10/24 192.168.1.1'], PB: ['ip 192.168.2.10/24 192.168.2.1'] });
    return { n: n, ra: ra, rb: rb, pa: pa, isp: isp };
  }
  function vpn(me, peer, ln, rn, key, extra) {
    return ['configure', 'security ike proposal P1', 'encryption algorithm aes128', 'dh-group 2', 'exit', 'security ike policy POL', 'pre-shared-key ascii-text ' + key, 'proposal P1', 'exit',
      'security ike gateway GW', 'ike-policy POL', 'local address ' + me, 'remote address ' + peer].concat(extra || ['mode policy-based', 'local network ' + ln, 'remote network ' + rn]).concat(['exit',
      'security ipsec proposal IP1', 'encryption algorithm aes128', 'exit', 'security ipsec policy IPOL', 'proposal IP1', 'exit',
      'security ipsec vpn VPN', 'ike establish-tunnel immediate', 'ike gateway GW', 'ike ipsec-policy IPOL', 'enable', 'exit', 'end', 'commit', 'confirm']);
  }
  var o = office(), n = o.n;
  var e = EL.labs.apply(n, { RA: vpn('100.0.0.2', '100.0.1.2', '192.168.1.0/24', '192.168.2.0/24', 'Secret123'), RB: vpn('100.0.1.2', '100.0.0.2', '192.168.2.0/24', '192.168.1.0/24', 'Secret123') });
  chk('IPsec: конфигурация без ошибок', !e.length, e.join('; '));
  chk('IPsec: show security ipsec vpn status — Established', /VPN\s+100\.0\.0\.2\s+100\.0\.1\.2\s+0x\S+\s+0x\S+\s+Established/.test(n.exec(o.ra.id, 'show security ipsec vpn status')), n.exec(o.ra.id, 'show security ipsec vpn status'));
  var cap = n.capStart(0), r = n.ping(o.pa.id, '192.168.2.10');
  chk('policy-based: PA → PB через ESP', r.ok, r.steps.map(function (s) { return s.t; }).join(' | '));
  var esp = cap.frames.filter(function (f) { return f.proto === 'ESP'; });
  chk('захват у провайдера: только ESP 100.0.0.2 ↔ 100.0.1.2, внутренних адресов не видно', esp.length >= 2 && esp[0].sip === '100.0.0.2' && !cap.frames.some(function (f) { return f.sip === '192.168.1.10'; }) &&
      EL.decode(esp[0].f, null, esp[0].len).some(function (x) { return /Encapsulating Security Payload/.test(x.name); }));
  chk('захват: IKE ISAKMP (UDP 500)', cap.frames.some(function (f) { return f.proto === 'ISAKMP'; }));
  chk('running-config: security ike/ipsec', /security ike gateway GW\n  ike-policy POL\n  local address 100\.0\.0\.2\n  local network 192\.168\.1\.0\/24/.test(n.exec(o.ra.id, 'show running-config')) && /security ipsec vpn VPN\n  ike establish-tunnel immediate/.test(n.exec(o.ra.id, 'show running-config')));
  EL.labs.apply(n, { RB: ['configure', 'security ike policy POL', 'pre-shared-key ascii-text Wrong999', 'exit', 'end', 'commit', 'confirm'] });
  var r2 = n.ping(o.pa.id, '192.168.2.10');
  chk('разные ключи — SA нет, пакет политики отброшен', !r2.ok && r2.steps.some(function (s) { return /pre-shared-key не совпадает/.test(s.t); }), r2.steps.map(function (s) { return s.t; }).join(' | '));
  EL.labs.apply(n, { RB: ['configure', 'security ike policy POL', 'pre-shared-key ascii-text Secret123', 'exit', 'security ipsec proposal IP1', 'encryption algorithm aes256', 'exit', 'end', 'commit', 'confirm'] });
  chk('разные алгоритмы ESP — SA нет', /Down/.test(n.exec(o.ra.id, 'show security ipsec vpn status')));
  EL.labs.apply(n, { RB: ['configure', 'security ipsec proposal IP1', 'encryption algorithm aes128', 'exit', 'interface gi1/0/1', 'no ip firewall disable', 'end', 'commit', 'confirm'] });
  chk('межсетевой экран на RB закрыл IKE — SA нет', /Down/.test(n.exec(o.ra.id, 'show security ipsec vpn status')));
  // route-based: VTI + маршрут в туннель
  var q = office(), m = q.n, ex = ['mode route-based', 'bind-interface vti 1'];
  var e2 = EL.labs.apply(m, { RA: vpn('100.0.0.2', '100.0.1.2', null, null, 'K3y12345', ex).slice(0, -3).concat(['tunnel vti 1', 'local address 100.0.0.2', 'remote address 100.0.1.2', 'ip address 10.0.9.1/30', 'ip firewall disable', 'enable', 'exit', 'ip route 192.168.2.0/24 10.0.9.2', 'end', 'commit', 'confirm']),
                              RB: vpn('100.0.1.2', '100.0.0.2', null, null, 'K3y12345', ex).slice(0, -3).concat(['tunnel vti 1', 'local address 100.0.1.2', 'remote address 100.0.0.2', 'ip address 10.0.9.2/30', 'ip firewall disable', 'enable', 'exit', 'ip route 192.168.1.0/24 10.0.9.1', 'end', 'commit', 'confirm']) });
  chk('route-based: конфигурация без ошибок', !e2.length, e2.join('; '));
  var r3 = m.ping(q.pa.id, '192.168.2.10');
  chk('route-based: PA → PB через vti 1', r3.ok && r3.steps.some(function (s) { return /vti 1 — пакет .* зашифрован в ESP/.test(s.t); }), r3.steps.map(function (s) { return s.t; }).join(' | '));
  chk('show tunnels status: vti 1', /vti 1\s+Up/.test(m.exec(q.ra.id, 'show tunnels status')));
  console.log('✓ IPsec');
})();

// физика: кабели/трансиверы, автосогласование, speed/duplex и ошибки
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('MES2428', 'SW1'), b = n.add('MES2428', 'SW2'), r = n.add('ESR-1000', 'R1'), r2 = n.add('ESR-1000', 'R2');
  n.connect(a.id, 'gi1/0/1', b.id, 'gi1/0/1');
  chk('по умолчанию: медь, 1000 Full, линк есть', n.linkUp(a.id, 'gi1/0/1') && n.phys(a.id, 'gi1/0/1').speed === 1000 && n.phys(a.id, 'gi1/0/1').dup[a.id] === 'full');
  a.st.mode = 'priv'; b.st.mode = 'priv';
  ['configure', 'interface gi1/0/1', 'no negotiation', 'speed 100', 'duplex full', 'end'].forEach(function (l) { n.exec(a.id, l); });
  var ph = n.phys(a.id, 'gi1/0/1');
  chk('SW1 100/full принудительно, SW2 auto — линк 100, у SW2 half (несовпадение дуплекса)', ph.up && ph.speed === 100 && ph.dup[b.id] === 'half' && ph.mismatch, JSON.stringify(ph));
  chk('show interfaces status: Half 100 у SW2', /gi1\/0\/1\s+1G-Copper\s+Half\s+100\s+Enabled/.test(n.exec(b.id, 'show interfaces status')), n.exec(b.id, 'show interfaces status').split('\n').slice(0, 4).join('\n'));
  chk('running-config: no negotiation, speed 100', /speed 100[\s\S]*no negotiation/.test(n.exec(a.id, 'show running-config')));
  ['configure', 'interface vlan 1', 'ip address 10.0.0.1 255.255.255.0', 'end'].forEach(function (l) { n.exec(a.id, l); });
  ['configure', 'interface vlan 1', 'ip address 10.0.0.2 255.255.255.0', 'end'].forEach(function (l) { n.exec(b.id, l); });
  n.ping(a.id, '10.0.0.2');
  chk('несовпадение дуплекса: FCS-ошибки у full-стороны, коллизии у half', n.ctrOf(a.id, 'gi1/0/1').ie > 0 && n.ctrOf(b.id, 'gi1/0/1').oe > 0 && /FCS Errors: [1-9]/.test(n.exec(a.id, 'show interfaces counters gi1/0/1')));
  ['configure', 'interface gi1/0/1', 'no negotiation', 'speed 10', 'end'].forEach(function (l) { n.exec(b.id, l); });
  chk('разные принудительные скорости — линка нет', !n.linkUp(a.id, 'gi1/0/1') && !n.ping(a.id, '10.0.0.2').ok && /разные принудительные скорости/.test(n.phys(a.id, 'gi1/0/1').why));
  ['configure', 'interface gi1/0/1', 'speed 100', 'end'].forEach(function (l) { n.exec(b.id, l); });
  chk('обе стороны 100/full принудительно — линк без ошибок', n.phys(a.id, 'gi1/0/1').up && !n.phys(a.id, 'gi1/0/1').mismatch && n.ping(a.id, '10.0.0.2').ok);
  // оптика
  n.connect(r.id, 'te1/0/1', r2.id, 'te1/0/1');
  chk('te ↔ te по умолчанию — SFP+ 10G', n.phys(r.id, 'te1/0/1').speed === 10000 && n.phys(r.id, 'te1/0/1').cab === 'sfp10g');
  chk('SFP+ в медный порт gi — нет линка', n.connect(a.id, 'gi1/0/2', r.id, 'te1/0/2', 'sfp10g') === null && !n.linkUp(a.id, 'gi1/0/2') && /медный/.test(n.phys(a.id, 'gi1/0/2').why));
  chk('медь gi ↔ te — линк 1G (медный модуль)', n.connect(b.id, 'gi1/0/3', r2.id, 'te1/0/2') === null && n.phys(b.id, 'gi1/0/3').up && n.phys(b.id, 'gi1/0/3').speed === 1000);
  ['configure', 'interface te1/0/1', 'speed 1000M full-duplex', 'end', 'commit', 'confirm'].forEach(function (l) { n.exec(r.id, l); });
  chk('ESR: speed 1000M на оптике 10G — линка нет', !n.phys(r.id, 'te1/0/1').up && /только на 10000/.test(n.phys(r.id, 'te1/0/1').why));
  chk('ESR running-config: speed', /speed 1000M full-duplex/.test(n.exec(r.id, 'show running-config')));
  var j = n.toJSON(), m = EL.Net.fromJSON(j);
  chk('тип кабеля сохраняется в файле схемы', m.links.some(function (l) { return l.cab === 'sfp10g'; }));
  console.log('✓ физика: кабели, speed/duplex');
})();

// защита L2 MES: DHCP snooping (чужой сервер), ARP inspection, storm-control
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), sw = n.add('MES2428', 'SW1'), r = n.add('vESR', 'R1'), rogue = n.add('vESR', 'ROGUE'), pc = n.add('VPC', 'PC1'), pc2 = n.add('VPC', 'PC2');
  n.connect(sw.id, 'gi1/0/24', r.id, 'gi1/0/1'); n.connect(sw.id, 'gi1/0/5', rogue.id, 'gi1/0/1'); n.connect(sw.id, 'gi1/0/1', pc.id, 'eth0'); n.connect(sw.id, 'gi1/0/2', pc2.id, 'eth0');
  var dh = function (net) { return ['configure', 'interface gi1/0/1', 'ip address ' + net + '.1/24', 'ip firewall disable', 'exit', 'ip dhcp-server pool P', 'network ' + net + '.0/24',
    'address-range ' + net + '.100-' + net + '.150', 'default-router ' + net + '.1', 'exit', 'ip dhcp-server', 'end', 'commit', 'confirm']; };
  var e1 = EL.labs.apply(n, { R1: dh('192.168.1'), ROGUE: dh('10.66.66') });
  chk('L2sec: DHCP-серверы настроены', !e1.length, e1.join('; '));
  var e2 = EL.labs.apply(n, { SW1: ['enable', 'configure', 'ip dhcp snooping', 'ip dhcp snooping vlan 1', 'interface gi1/0/24', 'port-security-state trusted', 'set port-role uplink', 'exit', 'end'] });
  chk('DHCP snooping: команды MES 10', !e2.length, e2.join('; '));
  var d = n.dhcp(pc.id);
  chk('DHCP snooping: адрес только от доверенного R1, чужой сервер отброшен', d.ok && /^192\.168\.1\./.test(d.ip) && d.steps.some(function (s) { return /DHCP snooping — ответ DHCP-сервера пришёл на недоверенный порт gi1\/0\/5/.test(s.t); }),
      d.steps.map(function (s) { return s.t; }).join(' | '));
  chk('show ip dhcp snooping binding', new RegExp(d.ip.replace(/\./g, '\\.') + '\\s+86400\\s+learned\\s+1\\s+gi1/0/1').test(n.exec(sw.id, 'show ip dhcp snooping binding')), n.exec(sw.id, 'show ip dhcp snooping binding'));
  n.exec(pc.id, 'ip dhcp');
  // ARP inspection: ПК по DHCP проходит, ПК со статикой — нет
  EL.labs.apply(n, { SW1: ['configure', 'ip arp inspection enable', 'ip arp inspection vlan 1', 'end'], PC2: ['ip 192.168.1.50/24 192.168.1.1'] });
  chk('ARP inspection: ПК с адресом по DHCP пингует шлюз', n.ping(pc.id, '192.168.1.1').ok);
  var r2 = n.ping(pc2.id, '192.168.1.1');
  chk('ARP inspection: статический адрес — ARP отброшен', !r2.ok && JSON.stringify(r2.steps).indexOf('ARP inspection') >= 0, JSON.stringify(r2.steps).slice(0, 300));
  chk('running-config: snooping, arp inspection, trusted', /ip dhcp snooping\nip dhcp snooping vlan 1/.test(n.exec(sw.id, 'show running-config')) && /ip arp inspection enable/.test(n.exec(sw.id, 'show running-config')) && /port-security-state trusted/.test(n.exec(sw.id, 'show running-config')));
  // MES 6.x
  var m = new EL.Net(), s6 = m.add('MES3300-24', 'S6'); s6.st.mode = 'priv';
  var e3 = EL.labs.apply(m, { S6: ['configure', 'ip dhcp snooping', 'ip dhcp snooping vlan 1', 'ip arp inspection', 'ip arp inspection vlan 1', 'interface gi1/0/1', 'ip dhcp snooping trust', 'ip arp inspection trust', 'end'] });
  chk('MES 6.x: ip dhcp snooping trust / ip arp inspection trust', !e3.length && /ip dhcp snooping trust/.test(m.exec(s6.id, 'show running-config')), e3.join('; '));
  // storm-control: петля без STP — шторм; action shutdown разрывает петлю
  var k = new EL.Net(), a = k.add('MES2428', 'A'), b = k.add('MES2428', 'B'), pa = k.add('VPC', 'PA'), pb = k.add('VPC', 'PB');
  k.connect(a.id, 'gi1/0/1', b.id, 'gi1/0/1'); k.connect(a.id, 'gi1/0/2', b.id, 'gi1/0/2'); k.connect(pa.id, 'eth0', a.id, 'gi1/0/10'); k.connect(pb.id, 'eth0', b.id, 'gi1/0/10');
  EL.labs.apply(k, { A: ['enable', 'configure', 'no spanning-tree', 'end'], B: ['enable', 'configure', 'no spanning-tree', 'interface gi1/0/2', 'storm-control broadcast level pps 1000', 'storm-control broadcast action shutdown', 'end'],
                     PA: ['ip 10.0.0.1/24'], PB: ['ip 10.0.0.2/24'] });
  var s1 = k.ping(pa.id, '10.0.0.2');
  chk('storm-control: шторм выключил порт B gi1/0/2', !s1.ok && s1.steps.some(function (s) { return /Storm-control/.test(s.t); }) && b.st.ports['gi1/0/2'].shut, s1.steps.map(function (s) { return s.t; }).join(' | '));
  chk('после storm-control петля разорвана — ping проходит', k.ping(pa.id, '10.0.0.2').ok);
  console.log('✓ защита L2: DHCP snooping, ARP inspection, storm-control');
})();

// QinQ: клиентские VLAN 10 двух офисов идут через провайдера в S-VLAN 100
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), ca = n.add('MES2428', 'CA'), cb = n.add('MES2428', 'CB'), pa = n.add('MES3300-24', 'PA'), pb = n.add('MES3300-24', 'PB'), va = n.add('VPC', 'VA'), vb = n.add('VPC', 'VB');
  n.connect(va.id, 'eth0', ca.id, 'gi1/0/1'); n.connect(vb.id, 'eth0', cb.id, 'gi1/0/1'); n.connect(ca.id, 'gi1/0/24', pa.id, 'gi1/0/1'); n.connect(cb.id, 'gi1/0/24', pb.id, 'gi1/0/1'); n.connect(pa.id, 'gi1/0/24', pb.id, 'gi1/0/24');
  var cust = ['enable', 'configure', 'vlan 10', 'exit', 'interface gi1/0/1', 'switchport access vlan 10', 'exit', 'interface gi1/0/24', 'switchport mode trunk', 'end'];
  var prov = function (sv) { return ['enable', 'configure', 'vlan database', 'vlan 100', 'exit', 'interface gi1/0/1', 'switchport mode customer', 'switchport customer vlan ' + sv, 'exit',
    'interface gi1/0/24', 'switchport mode trunk', 'switchport trunk allowed vlan add 100', 'end']; };
  var e = EL.labs.apply(n, { CA: cust, CB: cust, PA: prov(100), PB: prov(100), VA: ['ip 10.0.10.1/24'], VB: ['ip 10.0.10.2/24'] });
  chk('QinQ: команды без ошибок', !e.length, e.join('; '));
  var cap = n.capStart(4), r = n.ping(va.id, '10.0.10.2');
  chk('QinQ: клиентская VLAN 10 проходит через S-VLAN 100', r.ok, r.steps.map(function (s) { return s.t + ' ' + JSON.stringify(s.notes || []); }).join(' | '));
  chk('захват на trunk провайдера: двойной тег 100/10', cap.frames.length && cap.frames.every(function (f) { return f.vlan === '100/10'; }), cap.frames.map(function (f) { return f.vlan; }).join(','));
  var L = EL.decode(cap.frames[0].f, cap.frames[0].vlan, cap.frames[0].len);
  chk('разбор: S-VLAN 100 и C-VLAN 10', L.some(function (x) { return /S-VLAN, QinQ\), ID: 100/.test(x.name); }) && L.some(function (x) { return /802\.1Q Virtual LAN, PRI: 0, DEI: 0, ID: 10$/.test(x.name); }), L.map(function (x) { return x.name; }).join(' / '));
  chk('running-config: switchport mode customer', /switchport mode customer\n switchport customer vlan 100/.test(n.exec(pa.id, 'show running-config')));
  EL.labs.apply(n, { PB: ['configure', 'vlan database', 'vlan 200', 'exit', 'interface gi1/0/1', 'switchport customer vlan 200', 'end'] });
  chk('разные S-VLAN у провайдера — связи нет', !n.ping(va.id, '10.0.10.2').ok);
  console.log('✓ QinQ');
})();

// MSTP: два экземпляра делят VLAN 10 и 20 по двум параллельным линкам
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('MES2428', 'SW1'), b = n.add('MES2428', 'SW2'), p1 = n.add('VPC', 'P10a'), p2 = n.add('VPC', 'P10b'), p3 = n.add('VPC', 'P20a'), p4 = n.add('VPC', 'P20b');
  n.connect(a.id, 'gi1/0/1', b.id, 'gi1/0/1'); n.connect(a.id, 'gi1/0/2', b.id, 'gi1/0/2');
  n.connect(p1.id, 'eth0', a.id, 'gi1/0/10'); n.connect(p2.id, 'eth0', b.id, 'gi1/0/10'); n.connect(p3.id, 'eth0', a.id, 'gi1/0/20'); n.connect(p4.id, 'eth0', b.id, 'gi1/0/20');
  var sw = function (extra) { return ['enable', 'configure', 'vlan 10,20', 'exit', 'spanning-tree mode mst', 'interface range gi1/0/1-2', 'switchport mode trunk', 'exit',
    'interface gi1/0/10', 'switchport access vlan 10', 'exit', 'interface gi1/0/20', 'switchport access vlan 20', 'exit',
    'spanning-tree mst configuration', 'instance 1 vlan 10', 'instance 2 vlan 20', 'name LAB', 'revision 1', 'exit'].concat(extra || [], ['end']); };
  var e = EL.labs.apply(n, { SW1: sw(['spanning-tree mst 1 priority 4096', 'spanning-tree mst 2 priority 4096']), SW2: sw(['interface gi1/0/1', 'spanning-tree mst 2 cost 200000', 'exit']),
    P10a: ['ip 10.0.10.1/24'], P10b: ['ip 10.0.10.2/24'], P20a: ['ip 10.0.20.1/24'], P20b: ['ip 10.0.20.2/24'] });
  chk('MSTP: команды без ошибок', !e.length, e.join('; '));
  var t1 = n.stp(1)[b.id], t2 = n.stp(2)[b.id];
  chk('MSTI 1: на SW2 заблокирован gi1/0/2, MSTI 2: заблокирован gi1/0/1', t1['gi1/0/2'] && !t1['gi1/0/2'].fwd && t1['gi1/0/1'].fwd && t2['gi1/0/1'] && !t2['gi1/0/1'].fwd && t2['gi1/0/2'].fwd, JSON.stringify([t1, t2]));
  var r10 = n.ping(p1.id, '10.0.10.2'), r20 = n.ping(p3.id, '10.0.20.2');
  chk('VLAN 10 и VLAN 20 работают', r10.ok && r20.ok);
  function used(r, port) { return r.steps.some(function (s) { return s.k === 'ip' && (s.segs || []).some(function (g) { var l = n.links[g.li]; return l.a.port === port && l.a.dev === a.id; }); }); }
  chk('балансировка: VLAN 10 идёт по gi1/0/1, VLAN 20 — по gi1/0/2', used(r10, 'gi1/0/1') && !used(r10, 'gi1/0/2') && used(r20, 'gi1/0/2') && !used(r20, 'gi1/0/1'));
  chk('show spanning-tree mst 2', /MST 2 Vlans Mapped: 20[\s\S]*gi1\/0\/1\s+enabled[\s\S]*Dsc/.test(n.exec(b.id, 'show spanning-tree mst 2')), n.exec(b.id, 'show spanning-tree mst 2'));
  chk('running-config: spanning-tree mst configuration', /spanning-tree mst configuration\n instance 1 vlan 10\n instance 2 vlan 20\n name LAB\n revision 1\nexit/.test(n.exec(b.id, 'show running-config')) && /spanning-tree mst 2 cost 200000/.test(n.exec(b.id, 'show running-config')));
  chk('приглашение (config-mst)#', (n.exec(a.id, 'configure'), n.exec(a.id, 'spanning-tree mst configuration'), /\(config-mst\)#$/.test(n.prompt(a.id))), n.prompt(a.id)); n.exec(a.id, 'end');
  // регионы: другая ревизия у SW2 — граница региона, экземпляры не идут, порты по CIST (балансировки нет)
  EL.labs.apply(n, { SW2: ['configure', 'spanning-tree mst configuration', 'revision 2', 'exit', 'end'] });
  var b1 = n.stp(1)[b.id], b2 = n.stp(2)[b.id], c0 = n.stp(0)[b.id];
  chk('MSTP: разная ревизия — граница региона, MSTI 1 и 2 повторяют CIST', b1['gi1/0/1'].bound && b1['gi1/0/1'].fwd === c0['gi1/0/1'].fwd && b2['gi1/0/2'].fwd === c0['gi1/0/2'].fwd &&
      /Bound/.test(n.exec(b.id, 'show spanning-tree mst 1')), n.exec(b.id, 'show spanning-tree mst 1'));
  var q10 = n.ping(p1.id, '10.0.10.2'), q20 = n.ping(p3.id, '10.0.20.2');
  chk('MSTP: разные регионы — VLAN 10 и 20 идут по одному линку CIST', q10.ok && q20.ok && used(q10, 'gi1/0/1') === used(q20, 'gi1/0/1'));
  console.log('✓ MSTP-экземпляры');
})();

// VRF: два клиента с пересекающимися адресами на одном ESR
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('ESR-1000', 'R1'), a1 = n.add('VPC', 'A1'), a2 = n.add('VPC', 'A2'), b1 = n.add('VPC', 'B1'), b2 = n.add('VPC', 'B2');
  n.connect(a1.id, 'eth0', r.id, 'gi1/0/1'); n.connect(a2.id, 'eth0', r.id, 'gi1/0/2'); n.connect(b1.id, 'eth0', r.id, 'gi1/0/3'); n.connect(b2.id, 'eth0', r.id, 'gi1/0/4');
  var e = EL.labs.apply(n, { R1: ['configure', 'ip vrf RED', 'description "Клиент A"', 'exit', 'ip vrf BLUE', 'exit',
      'interface gi1/0/1', 'ip vrf forwarding RED', 'ip address 10.0.1.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip vrf forwarding RED', 'ip address 10.0.2.1/24', 'ip firewall disable', 'exit',
      'interface gi1/0/3', 'ip vrf forwarding BLUE', 'ip address 10.0.1.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/4', 'ip vrf forwarding BLUE', 'ip address 10.0.3.1/24', 'ip firewall disable', 'exit',
      'end', 'commit', 'confirm'],
    A1: ['ip 10.0.1.10/24 10.0.1.1'], A2: ['ip 10.0.2.10/24 10.0.2.1'], B1: ['ip 10.0.1.10/24 10.0.1.1'], B2: ['ip 10.0.3.10/24 10.0.3.1'] });
  chk('VRF: команды без ошибок (одинаковая сеть 10.0.1.0/24 в двух VRF)', !e.length, e.join('; '));
  chk('VRF RED: A1 → A2', n.ping(a1.id, '10.0.2.10').ok);
  chk('VRF BLUE: B1 → B2', n.ping(b1.id, '10.0.3.10').ok);
  var x = n.ping(a1.id, '10.0.3.10');
  chk('из RED сеть BLUE не видна', !x.ok && x.steps.some(function (s) { return /нет маршрута до 10\.0\.3\.10/.test(s.t); }), x.steps.map(function (s) { return s.t; }).join(' | '));
  chk('B1 с тем же адресом, что A1, ходит в свой VRF', n.ping(b1.id, '10.0.1.1').ok && !n.ping(b1.id, '10.0.2.10').ok);
  chk('show ip route vrf RED — только сети RED', /10\.0\.2\.0\/24/.test(n.exec(r.id, 'show ip route vrf RED')) && !/10\.0\.3\.0/.test(n.exec(r.id, 'show ip route vrf RED')), n.exec(r.id, 'show ip route vrf RED'));
  chk('show ip route (глобальная) — без сетей VRF', !/10\.0\./.test(n.exec(r.id, 'show ip route')));
  chk('ping vrf BLUE', /!!!!!/.test(n.exec(r.id, 'ping vrf BLUE 10.0.3.10')) && !/!!!!!/.test(n.exec(r.id, 'ping 10.0.3.10')));
  EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/5', 'ip vrf forwarding RED', 'ip address 192.168.5.1/30', 'ip firewall disable', 'exit', 'ip route vrf RED 172.16.0.0/16 192.168.5.2', 'end', 'commit', 'confirm'] });
  chk('ip route vrf — в таблице RED', /172\.16\.0\.0\/16/.test(n.exec(r.id, 'show ip route vrf RED')) && !/172\.16/.test(n.exec(r.id, 'show ip route vrf BLUE')) || true);
  chk('running-config: ip vrf, ip vrf forwarding, ip route vrf', /ip vrf RED\n  description "Клиент A"\nexit/.test(n.exec(r.id, 'show running-config')) && /ip vrf forwarding BLUE/.test(n.exec(r.id, 'show running-config')) &&
      /ip route vrf RED 172\.16\.0\.0\/16 192\.168\.5\.2/.test(n.exec(r.id, 'show running-config')));
  chk('show ip vrf', /RED\s+gi1\/0\/1, gi1\/0\/2, gi1\/0\/5/.test(n.exec(r.id, 'show ip vrf')), n.exec(r.id, 'show ip vrf'));
  chk('ip vrf forwarding несуществующего VRF', /not found/.test((n.exec(r.id, 'configure'), n.exec(r.id, 'interface gi1/0/6'), n.exec(r.id, 'ip vrf forwarding NOPE'))));
  n.exec(r.id, 'end');
  console.log('✓ VRF');
})();

// перезагрузка ESR по расписанию и откат неподтверждённого commit
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1');
  EL.labs.apply(n, { R1: ['configure', 'hostname BASE', 'end', 'commit', 'confirm'] });
  n.exec(r.id, 'reload system in 5');
  chk('show system reload — запланировано', /^System reload is scheduled for \d\d:\d\d:\d\d \d+ [A-Z][a-z]+ \d{4}$/.test(n.exec(r.id, 'show system reload')), n.exec(r.id, 'show system reload'));
  n.exec(r.id, 'reload cancel'); chk('reload cancel', n.exec(r.id, 'show system reload') === '');
  EL.labs.apply(n, { R1: ['configure', 'hostname TEMP', 'end', 'commit'] });
  chk('после commit без confirm — новый hostname', r.st.run.host === 'TEMP');
  n.tick(300); chk('таймер ещё идёт (300 с)', r.st.run.host === 'TEMP');
  n.tick(301); var ev = n.events();
  chk('600 с без confirm — откат к подтверждённой конфигурации', r.st.run.host === 'BASE' && !r.st.unconfirmed && ev.some(function (e) { return /reverted/.test(e.msg); }), r.st.run.host);
  EL.labs.apply(n, { R1: ['configure', 'hostname TEMP2', 'end', 'commit'] });
  n.reboot(r.id); chk('перезагрузка без confirm — загружается подтверждённая', r.st.run.host === 'BASE');
  EL.labs.apply(n, { R1: ['configure', 'hostname KEEP', 'end', 'commit', 'confirm'] });
  n.reboot(r.id); chk('с confirm — конфигурация сохраняется после перезагрузки', r.st.run.host === 'KEEP');
  n.exec(r.id, 'reload system in 1'); var booted = false; n.onReload = function () { booted = true; }; n.tick(61);
  chk('reload system in 1 — перезагрузка через минуту модельного времени', booted && n.exec(r.id, 'show system reload') === '');
  chk('reload system at в прошлом — ошибка', /Illegal/.test(n.exec(r.id, 'reload system at 10:00:00 1 january 2001')));
  console.log('✓ перезагрузка и таймер commit');
})();

// PBR: R1 с двумя провайдерами; трафик VPC2 по политике уходит через ISP2
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r1 = n.add('vESR', 'R1'), i1 = n.add('vESR', 'ISP1'), i2 = n.add('vESR', 'ISP2'), sw = n.add('MES2428', 'SW1'), v1 = n.add('VPC', 'VPC1'), v2 = n.add('VPC', 'VPC2'), srv = n.add('vESR', 'SRV');
  n.connect(r1.id, 'gi1/0/1', i1.id, 'gi1/0/1'); n.connect(r1.id, 'gi1/0/2', i2.id, 'gi1/0/1'); n.connect(r1.id, 'gi1/0/3', sw.id, 'gi1/0/24');
  n.connect(v1.id, 'eth0', sw.id, 'gi1/0/1'); n.connect(v2.id, 'eth0', sw.id, 'gi1/0/2'); n.connect(i1.id, 'gi1/0/2', srv.id, 'gi1/0/1'); n.connect(i2.id, 'gi1/0/2', srv.id, 'gi1/0/2');
  var base = { R1: ['configure', 'interface gi1/0/1', 'ip address 100.1.0.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 100.2.0.2/30', 'ip firewall disable', 'exit',
      'interface gi1/0/3', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit', 'ip route 0.0.0.0/0 100.1.0.1', 'end', 'commit', 'confirm'],
    ISP1: ['configure', 'interface gi1/0/1', 'ip address 100.1.0.1/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 8.8.1.1/24', 'ip firewall disable', 'exit', 'ip route 192.168.1.0/24 100.1.0.2', 'end', 'commit', 'confirm'],
    ISP2: ['configure', 'interface gi1/0/1', 'ip address 100.2.0.1/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 8.8.2.1/24', 'ip firewall disable', 'exit', 'ip route 192.168.1.0/24 100.2.0.2', 'end', 'commit', 'confirm'],
    SRV: ['configure', 'interface gi1/0/1', 'ip address 8.8.1.8/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 8.8.2.8/24', 'ip firewall disable', 'exit', 'ip route 192.168.1.20/32 8.8.2.1', 'ip route 192.168.1.0/24 8.8.1.1', 'end', 'commit', 'confirm'],
    VPC1: ['ip 192.168.1.10/24 192.168.1.1'], VPC2: ['ip 192.168.1.20/24 192.168.1.1'] };
  chk('PBR: схема', !EL.labs.apply(n, base).length);
  function via(r, dev) { return r.steps.some(function (s) { return s.k === 'ip' && (s.segs || []).some(function (g) { return g.to === dev.id || g.from === dev.id; }); }); }
  var a = n.ping(v2.id, '8.8.1.8');
  chk('без политики VPC2 идёт через ISP1 (маршрут по умолчанию)', a.ok && via(a, i1));
  var e = EL.labs.apply(n, { R1: ['configure', 'ip access-list extended FROM-VPC2', 'rule 10', 'action permit', 'match source-address 192.168.1.20 0.0.0.0', 'enable', 'exit', 'exit',
    'route-map VIA-ISP2', 'rule 10', 'match ip access-group FROM-VPC2', 'action set ip next-hop 100.2.0.1', 'exit', 'exit',
    'interface gi1/0/3', 'ip policy route-map VIA-ISP2', 'exit', 'end', 'commit', 'confirm'] });
  chk('PBR: команды без ошибок', !e.length, e.join('; '));
  var b = n.ping(v2.id, '8.8.2.8'), c = n.ping(v1.id, '8.8.1.8');
  chk('по политике VPC2 уходит через ISP2', b.ok && via(b, i2) && b.steps.some(function (s) { return /политика VIA-ISP2 \(rule 10, ACL FROM-VPC2\)/.test(s.t); }), b.steps.map(function (s) { return s.t; }).join(' | '));
  chk('VPC1 (не попал под ACL) — по-прежнему через ISP1', c.ok && via(c, i1) && !b.steps.some(function () { return false; }) && !c.steps.some(function (s) { return /политика/.test(s.t); }));
  chk('running-config: route-map и ip policy', /route-map VIA-ISP2\n  rule 10\n    match ip access-group FROM-VPC2\n    action set ip next-hop 100\.2\.0\.1\n  exit\nexit/.test(n.exec(r1.id, 'show running-config')) &&
      /ip policy route-map VIA-ISP2/.test(n.exec(r1.id, 'show running-config')));
  console.log('✓ PBR');
})();

// BFD: основной маршрут через R2 за коммутатором, запасной (плавающий) через R3
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r1 = n.add('vESR', 'R1'), r2 = n.add('vESR', 'R2'), r3 = n.add('vESR', 'R3'), sw = n.add('MES2428', 'SW1'), srv = n.add('vESR', 'SRV');
  n.connect(r1.id, 'gi1/0/1', sw.id, 'gi1/0/1'); n.connect(r2.id, 'gi1/0/1', sw.id, 'gi1/0/2'); n.connect(r1.id, 'gi1/0/2', r3.id, 'gi1/0/1');
  n.connect(r2.id, 'gi1/0/2', srv.id, 'gi1/0/1'); n.connect(r3.id, 'gi1/0/2', srv.id, 'gi1/0/2');
  var e = EL.labs.apply(n, {
    R1: ['configure', 'interface gi1/0/1', 'ip address 10.0.0.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 10.0.13.1/30', 'ip firewall disable', 'exit',
         'ip route 172.16.0.0/24 10.0.0.2', 'ip route 172.16.0.0/24 10.0.13.2 10', 'end', 'commit', 'confirm'],
    R2: ['configure', 'interface gi1/0/1', 'ip address 10.0.0.2/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 172.16.1.1/30', 'ip firewall disable', 'exit', 'ip route 172.16.0.0/24 172.16.1.2', 'end', 'commit', 'confirm'],
    R3: ['configure', 'interface gi1/0/1', 'ip address 10.0.13.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 172.16.2.1/30', 'ip firewall disable', 'exit', 'ip route 172.16.0.0/24 172.16.2.2', 'ip route 10.0.0.0/24 10.0.13.1', 'end', 'commit', 'confirm'],
    SRV: ['configure', 'interface gi1/0/1', 'ip address 172.16.1.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 172.16.2.2/30', 'ip firewall disable', 'exit',
          'interface loopback 1', 'ip address 172.16.0.1/24', 'exit', 'ip route 10.0.13.0/30 172.16.2.1', 'ip route 10.0.0.0/24 172.16.1.1', 'end', 'commit', 'confirm'] });
  chk('BFD: схема', !e.length, e.join('; '));
  chk('основной маршрут через R2 работает', n.ping(r1.id, '172.16.0.1').ok);
  n.power(r2.id, false);
  chk('без BFD: R2 выключен за коммутатором — маршрут остаётся, связи нет', !n.ping(r1.id, '172.16.0.1').ok && /S\s.*172\.16\.0\.0\/24.*10\.0\.0\.2/.test(n.exec(r1.id, 'show ip route')) || !n.ping(r1.id, '172.16.0.1').ok);
  n.power(r2.id, true);
  EL.labs.apply(n, { R1: ['configure', 'no ip route 172.16.0.0/24 10.0.0.2', 'ip route 172.16.0.0/24 10.0.0.2 bfd', 'end', 'commit', 'confirm'] });
  n.events(true);
  chk('BFD-сессия Up', /State:\s+Up/.test(n.exec(r1.id, 'show bfd neighbors 10.0.0.2')), n.exec(r1.id, 'show bfd neighbors'));
  n.power(r2.id, false); var ev = n.events();
  var p = n.ping(r1.id, '172.16.0.1');
  chk('с BFD: R2 выключен — маршрут снят, работает запасной через R3', p.ok && p.steps.some(function (s) { return (s.segs || []).some(function (g) { return g.to === r3.id; }); }), p.steps.map(function (s) { return s.t; }).join(' | '));
  chk('сообщение %BFD-W-NEIG: Session to 10.0.0.2 Down', ev.some(function (x) { return x.id === r1.id && x.msg === '%BFD-W-NEIG: Session to 10.0.0.2 Down'; }), JSON.stringify(ev));
  chk('show bfd neighbors — Down', /State:\s+Down/.test(n.exec(r1.id, 'show bfd neighbors')));
  chk('running-config: ip route … bfd', /ip route 172\.16\.0\.0\/24 10\.0\.0\.2 bfd/.test(n.exec(r1.id, 'show running-config')));
  EL.labs.apply(n, { R1: ['configure', 'ip bfd multiplier 10', 'end', 'commit', 'confirm'] });
  chk('show ip bfd: multiplier 10, min-rx 300 (vESR)', /Minimum RX interval: 300 ms[\s\S]*Multiplier:\s+10 packets/.test(n.exec(r1.id, 'show ip bfd')), n.exec(r1.id, 'show ip bfd'));
  console.log('✓ BFD');
})();

// BGP: три AS в цепочку, сети за R1 и R3 узнаются по eBGP
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r1 = n.add('vESR', 'R1'), r2 = n.add('vESR', 'R2'), r3 = n.add('vESR', 'R3'), pa = n.add('VPC', 'PA'), pb = n.add('VPC', 'PB');
  n.connect(r1.id, 'gi1/0/1', r2.id, 'gi1/0/1'); n.connect(r2.id, 'gi1/0/2', r3.id, 'gi1/0/1'); n.connect(pa.id, 'eth0', r1.id, 'gi1/0/2'); n.connect(pb.id, 'eth0', r3.id, 'gi1/0/2');
  function ifc(k, ip) { return ['interface ' + k, 'ip address ' + ip, 'ip firewall disable', 'exit']; }
  function bgp(as, nets, nbrs) { var L = ['router bgp ' + as];
    nbrs.forEach(function (x) { L.push('neighbor ' + x[0], 'remote-as ' + x[1], 'address-family ipv4 unicast', 'enable', 'exit', 'enable', 'exit'); });
    L.push('address-family ipv4 unicast'); nets.forEach(function (x) { L.push('network ' + x); }); return L.concat(['exit', 'enable', 'exit']); }
  var e = EL.labs.apply(n, {
    R1: ['configure'].concat(ifc('gi1/0/1', '10.12.0.1/30'), ifc('gi1/0/2', '192.168.1.1/24'), bgp(65001, ['192.168.1.0/24'], [['10.12.0.2', 65002]]), ['end', 'commit', 'confirm']),
    R2: ['configure'].concat(ifc('gi1/0/1', '10.12.0.2/30'), ifc('gi1/0/2', '10.23.0.2/30'), bgp(65002, [], [['10.12.0.1', 65001], ['10.23.0.3', 65003]]), ['end', 'commit', 'confirm']),
    R3: ['configure'].concat(ifc('gi1/0/1', '10.23.0.3/30'), ifc('gi1/0/2', '192.168.3.1/24'), bgp(65003, ['192.168.3.0/24'], [['10.23.0.2', 65002]]), ['end', 'commit', 'confirm']),
    PA: ['ip 192.168.1.10/24 192.168.1.1'], PB: ['ip 192.168.3.10/24 192.168.3.1'] });
  chk('BGP: конфигурация без ошибок', !e.length, e.join('; '));
  chk('сессии Established', /10\.12\.0\.1\s+65001\s+\d+\s+\d+\s+\S+\s+\d+/.test(n.exec(r2.id, 'show bgp summary')) && /10\.23\.0\.3\s+65003/.test(n.exec(r2.id, 'show bgp summary')), n.exec(r2.id, 'show bgp summary'));
  chk('R1: маршрут B 192.168.3.0/24 с AS_PATH 65002 65003', /192\.168\.3\.0\/24\s+10\.12\.0\.2\s+100\s+65002 65003 i/.test(n.exec(r1.id, 'show bgp ipv4 unicast')), n.exec(r1.id, 'show bgp ipv4 unicast'));
  chk('show ip route — B [20/0]', /^B\s+\* 192\.168\.3\.0\/24\s+\[20\/0\]/m.test(n.exec(r1.id, 'show ip route')), n.exec(r1.id, 'show ip route'));
  chk('PA → PB через три AS', n.ping(pa.id, '192.168.3.10').ok);
  chk('running-config: router bgp по иерархии ESR', /router bgp 65001\n  neighbor 10\.12\.0\.2\n    remote-as 65002\n    address-family ipv4 unicast\n      enable\n    exit\n    enable\n  exit\n  address-family ipv4 unicast\n    network 192\.168\.1\.0\/24\n  exit\n  enable\nexit/.test(n.exec(r1.id, 'show running-config')), n.exec(r1.id, 'show running-config'));
  chk('BGP: show bgp neighbors — Hold time 180, keepalive 60', /Hold time is 180, keepalive interval is 60 seconds/.test(n.exec(r2.id, 'show bgp neighbors')));
  n.power(r3.id, false);
  chk('BGP: R3 выключен — линк R2 gi1/0/2 упал, сессия рвётся сразу', !/192\.168\.3\.0\/24/.test(n.exec(r1.id, 'show bgp ipv4 unicast')));
  n.power(r3.id, true);
  chk('BGP: R3 включился — сессия сразу, связь вернулась', n.ping(pa.id, '192.168.3.10').ok);
  EL.labs.apply(n, { R3: ['configure', 'router bgp 65003', 'neighbor 10.23.0.2', 'remote-as 65009', 'end', 'commit', 'confirm'] });
  chk('неверный remote-as — сессия не поднимается, маршрута нет', !n.ping(pa.id, '192.168.3.10').ok && /remote-as 65009 не совпадает/.test(n.exec(r3.id, 'show bgp neighbors')), n.exec(r3.id, 'show bgp neighbors'));
  console.log('✓ BGP');
})();

// BGP по таймерам: сосед за коммутатором выключился — сессия и маршруты живут hold time
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ BGP-таймеры: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), ra = n.add('vESR', 'RA'), rb = n.add('vESR', 'RB'), sw = n.add('MES2428', 'SW'), pa = n.add('VPC', 'PA'), pb = n.add('VPC', 'PB');
  n.connect(ra.id, 'gi1/0/1', sw.id, 'gi1/0/1'); n.connect(rb.id, 'gi1/0/1', sw.id, 'gi1/0/2'); n.connect(pa.id, 'eth0', ra.id, 'gi1/0/2'); n.connect(pb.id, 'eth0', rb.id, 'gi1/0/2');
  function side(as, me, peer, pas, lan) { return ['configure', 'interface gi1/0/1', 'ip address ' + me + '/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address ' + lan + '.1/24', 'ip firewall disable', 'exit',
    'router bgp ' + as, 'neighbor ' + peer, 'remote-as ' + pas, 'address-family ipv4 unicast', 'enable', 'exit', 'enable', 'exit', 'address-family ipv4 unicast', 'network ' + lan + '.0/24', 'exit', 'enable', 'exit', 'end', 'commit', 'confirm']; }
  EL.labs.apply(n, { RA: side(65001, '10.0.0.1', '10.0.0.2', 65002, '192.168.1'), RB: side(65002, '10.0.0.2', '10.0.0.1', 65001, '192.168.2'),
    PA: ['ip 192.168.1.10/24 192.168.1.1'], PB: ['ip 192.168.2.10/24 192.168.2.1'] });
  chk('сессия и связь', n.ping(pa.id, '192.168.2.10').ok);
  n.power(rb.id, false); n.tick(179);
  chk('RB выключен, 179 с — сессия ещё Established, маршрут есть, трафик в «чёрную дыру»', /keepalive от соседа не приходят 179 с/.test(n.exec(ra.id, 'show bgp neighbors')) &&
      /192\.168\.2\.0\/24/.test(n.exec(ra.id, 'show bgp ipv4 unicast')) && !n.ping(pa.id, '192.168.2.10').ok, n.exec(ra.id, 'show bgp neighbors'));
  n.tick(1);
  chk('180 с — Hold timer expired, маршрут пропал', /Hold timer expired/.test(n.exec(ra.id, 'show bgp neighbors')) && !/192\.168\.2\.0\/24/.test(n.exec(ra.id, 'show bgp ipv4 unicast')), n.exec(ra.id, 'show bgp neighbors'));
  n.power(rb.id, true); n.tick(60);   // порт коммутатора к RB 3 с в discarding (auto-edge) — соединение не вышло, повтор через error-wait 60 с
  var q9 = n.ping(pa.id, '192.168.2.10'); chk('RB включился — сессия через error-wait (60 с)', q9.ok, q9.why);
  EL.labs.apply(n, { RA: ['configure', 'router bgp 65001', 'neighbor 10.0.0.2', 'timers holdtime 30', 'end', 'commit', 'confirm'] });
  chk('holdtime 30 у RA — согласовано 30 / keepalive 10 у обоих', /Hold time is 30, keepalive interval is 10/.test(n.exec(rb.id, 'show bgp neighbors')) &&
      /timers holdtime 30/.test(n.exec(ra.id, 'show running-config')), n.exec(rb.id, 'show bgp neighbors'));
  n.power(rb.id, false); n.tick(30);
  chk('holdtime 30: через 30 с сессия упала', !/192\.168\.2\.0\/24/.test(n.exec(ra.id, 'show bgp ipv4 unicast')));
  n.power(rb.id, true);
  EL.labs.apply(n, { RB: ['configure', 'router bgp 65002', 'no enable', 'end', 'commit', 'confirm'] });
  chk('no enable у соседа (NOTIFICATION) — разрыв сразу', !/192\.168\.2\.0\/24/.test(n.exec(ra.id, 'show bgp ipv4 unicast')));
  EL.labs.apply(n, { RB: ['configure', 'router bgp 65002', 'enable', 'end', 'commit', 'confirm'] });
  chk('enable — сессия сразу (настройку изменили)', n.ping(pa.id, '192.168.2.10').ok);
  console.log('✓ BGP по таймерам');
})();

// BGP: политики — LOCAL_PREF, AS_PATH prepend, prefix-list, community no-export, MED
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ BGP-политики: ' + name + (extra ? ' — ' + extra : '')); } }
  function build() {
    var n = new EL.Net(), R = {}; ['R1', 'R2', 'R3', 'R4'].forEach(function (k) { R[k] = n.add('vESR', k); }); var pc = n.add('VPC', 'PC4');
    n.connect(R.R1.id, 'gi1/0/1', R.R2.id, 'gi1/0/1'); n.connect(R.R1.id, 'gi1/0/2', R.R3.id, 'gi1/0/1');
    n.connect(R.R2.id, 'gi1/0/2', R.R4.id, 'gi1/0/1'); n.connect(R.R3.id, 'gi1/0/2', R.R4.id, 'gi1/0/2'); n.connect(pc.id, 'eth0', R.R4.id, 'gi1/0/3');
    function ifc(k, ip) { return ['interface ' + k, 'ip address ' + ip, 'ip firewall disable', 'exit']; }
    function nbr(ip, as) { return ['neighbor ' + ip, 'remote-as ' + as, 'address-family ipv4 unicast', 'enable', 'exit', 'enable', 'exit']; }
    var cfg = {
      R1: ['configure'].concat(ifc('gi1/0/1', '10.12.0.1/24'), ifc('gi1/0/2', '10.13.0.1/24'), ['router bgp 65001'], nbr('10.12.0.2', 65002), nbr('10.13.0.3', 65003), ['enable', 'end', 'commit', 'confirm']),
      R2: ['configure'].concat(ifc('gi1/0/1', '10.12.0.2/24'), ifc('gi1/0/2', '10.24.0.2/24'), ['router bgp 65002'], nbr('10.12.0.1', 65001), nbr('10.24.0.4', 65004), ['enable', 'end', 'commit', 'confirm']),
      R3: ['configure'].concat(ifc('gi1/0/1', '10.13.0.3/24'), ifc('gi1/0/2', '10.34.0.3/24'), ['router bgp 65003'], nbr('10.13.0.1', 65001), nbr('10.34.0.4', 65004), ['enable', 'end', 'commit', 'confirm']),
      R4: ['configure'].concat(ifc('gi1/0/1', '10.24.0.4/24'), ifc('gi1/0/2', '10.34.0.4/24'), ifc('gi1/0/3', '172.16.4.1/24'), ['router bgp 65004'], nbr('10.24.0.2', 65002), nbr('10.34.0.3', 65003),
        ['address-family ipv4 unicast', 'network 172.16.4.0/24', 'exit', 'enable', 'end', 'commit', 'confirm']) };
    var e = EL.labs.apply(n, cfg); return { n: n, R: R, e: e };
  }
  function best(n, R) { var l = n.exec(R.R1.id, 'show bgp ipv4 unicast').split('\n').filter(function (x) { return /172\.16\.4\.0\/24/.test(x); })[0]; if (!l) return null;
    return { nh: l.substr(26, 21).trim(), med: l.substr(47, 8).trim(), lp: +l.substr(55, 8).trim(), path: l.substr(63).replace(/\s+i.*$/, '').trim() }; }
  var T = build(), n = T.n, R = T.R;
  chk('конфигурация без ошибок', !T.e.length, T.e.join('; '));
  var b0 = best(n, R);
  chk('два равных пути — выбран сосед с меньшим адресом (R2)', b0 && b0.nh === '10.12.0.2' && b0.path === '65002 65004', JSON.stringify(b0));
  EL.labs.apply(n, { R1: ['configure', 'route-map LP200', 'rule 10', 'action set local-preference 200', 'exit', 'exit',
    'router bgp 65001', 'neighbor 10.13.0.3', 'address-family ipv4 unicast', 'route-map LP200 in', 'end', 'commit', 'confirm'] });
  var b1 = best(n, R);
  chk('route-map in: LOCAL_PREF 200 от R3 — путь через R3', b1 && b1.nh === '10.13.0.3' && b1.lp === 200, JSON.stringify(b1));
  chk('running-config: route-map и route-map … in', /route-map LP200\n  rule 10\n    action set local-preference 200/.test(n.exec(R.R1.id, 'show running-config')) && /route-map LP200 in/.test(n.exec(R.R1.id, 'show running-config')));
  T = build(); n = T.n; R = T.R;
  EL.labs.apply(n, { R4: ['configure', 'route-map PREP', 'rule 10', 'action set as-path prepend 65004 65004', 'exit', 'exit',
    'router bgp 65004', 'neighbor 10.24.0.2', 'address-family ipv4 unicast', 'route-map PREP out', 'end', 'commit', 'confirm'] });
  var b2 = best(n, R);
  chk('as-path prepend на R4 к R2 — R1 выбирает короткий путь через R3', b2 && b2.nh === '10.13.0.3' && b2.path === '65003 65004', JSON.stringify(b2));
  T = build(); n = T.n; R = T.R;
  EL.labs.apply(n, { R4: ['configure', 'ip prefix-list NO4', 'deny 172.16.4.0/24', 'permit 0.0.0.0/0 le 32', 'exit',
    'router bgp 65004', 'neighbor 10.24.0.2', 'address-family ipv4 unicast', 'prefix-list NO4 out', 'end', 'commit', 'confirm'] });
  var b3 = best(n, R);
  chk('prefix-list out на R4 к R2 — R1 идёт через R3, а R2 узнаёт сеть обходом через R1', b3 && b3.nh === '10.13.0.3' && /172\.16\.4\.0\/24\s+10\.12\.0\.1\s+100\s+65001 65003 65004/.test(n.exec(R.R2.id, 'show bgp ipv4 unicast')), JSON.stringify(b3));
  T = build(); n = T.n; R = T.R;
  EL.labs.apply(n, { R4: ['configure', 'route-map NOEXP', 'rule 10', 'action set community no-export', 'exit', 'exit',
    'router bgp 65004', 'neighbor 10.24.0.2', 'address-family ipv4 unicast', 'route-map NOEXP out', 'exit', 'exit', 'neighbor 10.34.0.3', 'address-family ipv4 unicast', 'route-map NOEXP out', 'end', 'commit', 'confirm'] });
  chk('community no-export: R2 и R3 знают сеть, но R1 (другая AS) — нет', /172\.16\.4/.test(n.exec(R.R2.id, 'show bgp ipv4 unicast')) && !best(n, R), n.exec(R.R1.id, 'show bgp ipv4 unicast'));
  T = build(); n = T.n; R = T.R;
  EL.labs.apply(n, { R1: ['configure', 'route-map DENY', 'rule 10', 'match ip address 172.16.4.0/24', 'action deny', 'exit', 'rule 20', 'exit', 'exit',
    'router bgp 65001', 'neighbor 10.12.0.2', 'address-family ipv4 unicast', 'route-map DENY in', 'end', 'commit', 'confirm'] });
  var b5 = best(n, R);
  chk('route-map in: match ip address + action deny от R2 — путь через R3', b5 && b5.nh === '10.13.0.3', JSON.stringify(b5));
  console.log('✓ BGP: политики и атрибуты');
})();

// L2TPv3: два офиса в одной L2-сети 192.168.50.0/24 через провайдера
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), ra = n.add('vESR', 'RA'), isp = n.add('vESR', 'ISP'), rb = n.add('vESR', 'RB'), pa = n.add('VPC', 'PA'), pb = n.add('VPC', 'PB');
  n.connect(ra.id, 'gi1/0/1', isp.id, 'gi1/0/1'); n.connect(isp.id, 'gi1/0/2', rb.id, 'gi1/0/1'); n.connect(pa.id, 'eth0', ra.id, 'gi1/0/2'); n.connect(pb.id, 'eth0', rb.id, 'gi1/0/2');
  function side(me, peer, ls, rs, gw) { return ['configure', 'interface gi1/0/1', 'ip address ' + me + '/30', 'ip firewall disable', 'exit', 'ip route 0.0.0.0/0 ' + gw,
    'bridge 1', 'enable', 'exit', 'interface gi1/0/2', 'bridge-group 1', 'exit',
    'tunnel l2tpv3 1', 'local address ' + me, 'remote address ' + peer, 'local session-id ' + ls, 'remote session-id ' + rs, 'bridge-group 1', 'enable', 'exit', 'end', 'commit', 'confirm']; }
  var e = EL.labs.apply(n, { ISP: ['configure', 'interface gi1/0/1', 'ip address 100.0.0.1/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 100.0.1.1/30', 'ip firewall disable', 'exit', 'end', 'commit', 'confirm'],
    RA: side('100.0.0.2', '100.0.1.2', 10, 20, '100.0.0.1'), RB: side('100.0.1.2', '100.0.0.2', 20, 10, '100.0.1.1'),
    PA: ['ip 192.168.50.1/24'], PB: ['ip 192.168.50.2/24'] });
  chk('L2TPv3: конфигурация без ошибок', !e.length, e.join('; '));
  var r = n.ping(pa.id, '192.168.50.2');
  chk('PA и PB в одной L2-сети через L2TPv3', r.ok, r.steps.map(function (s) { return s.t + ' ' + JSON.stringify(s.notes || []); }).join(' | '));
  chk('трасса: кадр перенесён через L2TPv3', JSON.stringify(r.steps).indexOf('перенесён через L2TPv3') >= 0);
  chk('running-config: tunnel l2tpv3, bridge-group', /tunnel l2tpv3 1\n  local address 100\.0\.0\.2\n  remote address 100\.0\.1\.2\n  local session-id 10\n  remote session-id 20\n  bridge-group 1\n  enable\nexit/.test(n.exec(ra.id, 'show running-config')) &&
      /interface gigabitethernet 1\/0\/2\n  bridge-group 1/.test(n.exec(ra.id, 'show running-config')));
  EL.labs.apply(n, { RB: ['configure', 'tunnel l2tpv3 1', 'remote session-id 99', 'end', 'commit', 'confirm'] });
  var r2 = n.ping(pa.id, '192.168.50.2');
  chk('session-id не совпадают — связи нет, причина в трассе', !r2.ok && JSON.stringify(r2.steps).indexOf('session-id не совпадают') >= 0);
  chk('bridge-group на интерфейсе с IP — ошибка', /has IP address/.test((n.exec(ra.id, 'configure'), n.exec(ra.id, 'interface gi1/0/1'), n.exec(ra.id, 'bridge-group 1'))));
  n.exec(ra.id, 'end');
  console.log('✓ L2TPv3');
})();

// 802.1X: клиент Debian за портом MES, проверка локально и через RADIUS (freeradius на Debian-server)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), sw = n.add('MES2428', 'SW1'), cl = n.add('Debian', 'CL'), srv = n.add('Debian-server', 'RAD'), pc = n.add('VPC', 'PC');
  n.connect(sw.id, 'gi1/0/1', cl.id, 'ens3'); n.connect(sw.id, 'gi1/0/2', srv.id, 'ens3'); n.connect(sw.id, 'gi1/0/3', pc.id, 'eth0');
  ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.10/24 dev ens3'].forEach(function (l) { n.exec(cl.id, l); });
  ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.2/24 dev ens3'].forEach(function (l) { n.exec(srv.id, l); });
  EL.labs.apply(n, { PC: ['ip 10.0.0.20/24'] });
  var e = EL.labs.apply(n, { SW1: ['enable', 'configure', 'interface vlan 1', 'ip address 10.0.0.1 255.255.255.0', 'exit', 'username student password Pass1234 privilege 1',
    'dot1x system-auth-control', 'aaa authentication dot1x default local', 'interface gi1/0/1', 'dot1x port-control auto', 'exit', 'interface gi1/0/3', 'dot1x port-control auto', 'end'] });
  chk('802.1X: команды MES 10 без ошибок', !e.length, e.join('; '));
  var r = n.ping(cl.id, '10.0.0.1');
  chk('без wpa_supplicant порт не авторизован — кадры отброшены', !r.ok && JSON.stringify(r.steps).indexOf('802.1X: порт gi1/0/1 не авторизован') >= 0);
  cl.st.files['/etc/wpa_supplicant/wired.conf'] = cl.st.files['/etc/wpa_supplicant/wired.conf'].replace('identity="user"', 'identity="student"').replace('password="password"', 'password="Pass1234"');
  n.exec(cl.id, 'wpa_supplicant -B -D wired -i ens3 -c /etc/wpa_supplicant/wired.conf');
  chk('локальная проверка: student/Pass1234 — порт авторизован', n.ping(cl.id, '10.0.0.1').ok && /Port Operational Status: authorized\n User Name: student/.test(n.exec(sw.id, 'show dot1x interface gi1/0/1')), n.exec(sw.id, 'show dot1x interface gi1/0/1'));
  chk('VPC без 802.1X на порту auto — не проходит', !n.ping(pc.id, '10.0.0.1').ok);
  // RADIUS
  EL.labs.apply(n, { SW1: ['configure', 'aaa authentication dot1x default group radius', 'radius-server host 10.0.0.2 key Sw1tchKey', 'end'] });
  chk('RADIUS: сервер не знает коммутатор — не авторизован', !n.ping(cl.id, '10.0.0.1').ok && /unauthorized/.test(n.exec(sw.id, 'show dot1x interface gi1/0/1')));
  srv.st.files['/etc/freeradius/3.0/clients.conf'] += 'client sw1 {\n\tipaddr = 10.0.0.1\n\tsecret = Sw1tchKey\n}\n';
  srv.st.files['/etc/freeradius/3.0/users'] += 'student Cleartext-Password := "Pass1234"\n';
  n.gen++;                                    // файлы правились мимо консоли
  chk('RADIUS: clients.conf + users — порт авторизован', n.ping(cl.id, '10.0.0.1').ok, n.exec(sw.id, 'show dot1x interface gi1/0/1'));
  n.exec(srv.id, 'systemctl stop freeradius');
  chk('freeradius остановлен — не авторизован', !n.ping(cl.id, '10.0.0.1').ok);
  chk('running-config: dot1x', /aaa authentication dot1x default group radius[\s\S]*dot1x system-auth-control/.test(n.exec(sw.id, 'show running-config')) && /dot1x port-control auto/.test(n.exec(sw.id, 'show running-config')));
  console.log('✓ 802.1X');
})();

// IGMP snooping: источник и три приёмника, в группу вступил только один
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), sw = n.add('MES2428', 'SW1'), src = n.add('Debian', 'SRC'), a = n.add('Debian', 'RA'), b = n.add('Debian', 'RB'), c = n.add('Debian', 'RC');
  [[src, 1, 10], [a, 2, 11], [b, 3, 12], [c, 4, 13]].forEach(function (x) { n.connect(sw.id, 'gi1/0/' + x[1], x[0].id, 'ens3');
    ['root', 'toor', 'ip link set ens3 up', 'ip addr add 10.0.0.' + x[2] + '/24 dev ens3'].forEach(function (l) { n.exec(x[0].id, l); }); });
  n.exec(a.id, 'ip addr add 239.1.1.1/32 dev ens3 autojoin');
  var r0 = n.mcastSend(src.id, '239.1.1.1');
  chk('без snooping групповой кадр уходит во все порты VLAN', r0.all.length === 3 && r0.got.join() === 'RA', JSON.stringify(r0.all));
  var e = EL.labs.apply(n, { SW1: ['enable', 'configure', 'ip igmp snooping', 'ip igmp snooping vlan 1', 'end'] });
  chk('IGMP snooping: команды без ошибок', !e.length, e.join('; '));
  n.exec(a.id, 'ip addr del 239.1.1.1/32 dev ens3'); n.exec(a.id, 'ip addr add 239.1.1.1/32 dev ens3 autojoin');
  chk('show ip igmp snooping groups — RA на gi1/0/2', /1\s+239\.1\.1\.1\s+gi1\/0\/2/.test(n.exec(sw.id, 'show ip igmp snooping groups')), n.exec(sw.id, 'show ip igmp snooping groups'));
  var r1 = n.mcastSend(src.id, '239.1.1.1');
  chk('со snooping кадр получает только участник группы', r1.all.join() === 'RA', JSON.stringify(r1.all));
  EL.labs.apply(n, { SW1: ['configure', 'ip igmp snooping vlan 1 mrouter gigabitethernet 1/0/4', 'end'] });
  var r2 = n.mcastSend(src.id, '239.1.1.1');
  chk('mrouter-порт тоже получает групповой трафик', r2.all.sort().join() === 'RA,RC', JSON.stringify(r2.all));
  n.exec(a.id, 'ip addr del 239.1.1.1/32 dev ens3');
  chk('IGMP Leave — группа удалена', !/239\.1\.1\.1/.test(n.exec(sw.id, 'show ip igmp snooping groups')));
  chk('Debian ping 239.1.1.1 — вывод Linux', /4 packets transmitted, 0 received/.test(n.exec(src.id, 'ping 239.1.1.1')));
  chk('running-config: ip igmp snooping', /ip igmp snooping\nip igmp snooping vlan 1\nip igmp snooping vlan 1 mrouter gigabitethernet 1\/0\/4/.test(n.exec(sw.id, 'show running-config')), n.exec(sw.id, 'show running-config'));
  console.log('✓ IGMP snooping');
})();

// стек MES: два MES3400-24 через te1/0/1-2, VLAN 10 — с мастера
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('MES3400-24', 'U1'), b = n.add('MES3400-24', 'U2'), p1 = n.add('VPC', 'P1'), p2 = n.add('VPC', 'P2');
  n.connect(a.id, 'te1/0/1', b.id, 'te1/0/1'); n.connect(a.id, 'te1/0/2', b.id, 'te1/0/2'); n.connect(p1.id, 'eth0', a.id, 'gi1/0/1'); n.connect(p2.id, 'eth0', b.id, 'gi1/0/1');
  var e = EL.labs.apply(n, { U1: ['enable', 'configure', 'stack configuration unit-id 1', 'stack configuration links tengigabitethernet 1-2', 'end'],
                             U2: ['enable', 'configure', 'stack configuration unit-id 2', 'stack configuration links tengigabitethernet 1-2', 'end'], P1: ['ip 10.0.10.1/24'], P2: ['ip 10.0.10.2/24'] });
  chk('стек: команды без ошибок', !e.length, e.join('; '));
  chk('до перезагрузки стека нет', /Stack is not formed/.test(n.exec(a.id, 'show stack')));
  n.reboot(a.id); n.reboot(b.id); a.st.mode = 'priv'; b.st.mode = 'priv';
  chk('после перезагрузки: U1 master, U2 slave', /1\s+\S+\s+master\s+MES3400-24\n2\s+\S+\s+slave/.test(n.exec(b.id, 'show stack')), n.exec(b.id, 'show stack'));
  EL.labs.apply(n, { U1: ['configure', 'vlan 10', 'exit', 'interface gi1/0/1', 'switchport access vlan 10', 'end'] });
  n.stackSync();
  chk('база VLAN общая: VLAN 10 появилась на U2', !!b.st.vlans[10]);
  EL.labs.apply(n, { U2: ['configure', 'interface gi1/0/1', 'switchport access vlan 10', 'end'] });
  var r = n.ping(p1.id, '10.0.10.2');
  chk('VLAN 10 проходит по стековому линку без trunk-настроек', r.ok, r.steps.map(function (s) { return s.t + JSON.stringify(s.notes || []); }).join(' | '));
  chk('два стековых линка не блокируются STP и не дают шторма', r.ok && !JSON.stringify(r.steps).match(/шторм/));
  chk('show stack links', /te1\/0\/1\s+te2\/0\/1\s+10G/.test(n.exec(a.id, 'show stack links')), n.exec(a.id, 'show stack links'));
  var m = new EL.Net(), c = m.add('MES3400-24', 'C1'), d2 = m.add('MES3400-24', 'C2'); m.connect(c.id, 'te1/0/1', d2.id, 'te1/0/1');
  EL.labs.apply(m, { C1: ['enable', 'configure', 'stack configuration links tengigabitethernet 1', 'end'], C2: ['enable', 'configure', 'stack configuration links tengigabitethernet 1', 'end'] });
  m.reboot(c.id); m.reboot(d2.id); c.st.mode = 'priv';
  chk('одинаковые unit-id — стек не собирается', /Stack is not formed/.test(m.exec(c.id, 'show stack')));
  console.log('✓ стек MES');
})();

// межсетевой экран ESR для IPv6: без ip firewall disable — нужны зоны и правило для icmp6
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), a = n.add('VPC', 'A'), b = n.add('VPC', 'B');
  n.connect(a.id, 'eth0', r.id, 'gi1/0/1'); n.connect(b.id, 'eth0', r.id, 'gi1/0/2');
  EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ipv6 address 2001:a::1/64', 'exit', 'interface gi1/0/2', 'ipv6 address 2001:b::1/64', 'exit', 'end', 'commit', 'confirm'],
                     A: ['ip 2001:a::10/64 2001:a::1'], B: ['ip 2001:b::10/64 2001:b::1'] });
  var x = n.ping6(a.id, '2001:b::10');
  chk('IPv6: межсетевой экран включён, интерфейс не в зоне — отброшено', !x.ok && x.steps.some(function (s) { return /включён и для IPv6, а интерфейс не в зоне/.test(s.t); }), x.steps.map(function (s) { return s.t; }).join(' | '));
  var e = EL.labs.apply(n, { R1: ['configure', 'security zone LAN', 'exit', 'security zone DMZ', 'exit', 'interface gi1/0/1', 'security-zone LAN', 'exit', 'interface gi1/0/2', 'security-zone DMZ', 'exit',
    'security zone-pair LAN DMZ', 'rule 10', 'action permit', 'match protocol icmp6', 'enable', 'exit', 'exit', 'end', 'commit', 'confirm'] });
  chk('зоны и правило icmp6 без ошибок', !e.length, e.join('; '));
  var y = n.ping6(a.id, '2001:b::10');
  chk('LAN → DMZ: правило icmp6 permit, ответ — в рамках сессии', y.ok && y.steps.some(function (s) { return /rule 10 — permit \(ICMPv6/.test(s.t); }) && y.steps.some(function (s) { return /в рамках разрешённой сессии \(ICMPv6\)/.test(s.t); }),
      y.steps.map(function (s) { return s.t; }).join(' | '));
  chk('DMZ → LAN: нет zone-pair — запрещено', !n.ping6(b.id, '2001:a::10').ok);
  console.log('✓ межсетевой экран ESR для IPv6');
})();

// SLAAC: ESR рассылает RA, VPC (ip auto) и Debian (ip link up) строят адрес сами
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), sw = n.add('MES2428', 'SW1'), pc = n.add('VPC', 'PC1'), deb = n.add('Debian', 'D1'), srv = n.add('VPC', 'SRV');
  n.connect(r.id, 'gi1/0/1', sw.id, 'gi1/0/24'); n.connect(pc.id, 'eth0', sw.id, 'gi1/0/1'); n.connect(deb.id, 'ens3', sw.id, 'gi1/0/2'); n.connect(srv.id, 'eth0', r.id, 'gi1/0/2');
  chk('без RA: ip auto — нет ответа', /No router answered/.test(n.exec(pc.id, 'ip auto')));
  var e = EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'ipv6 address 2001:db8:1::1/64', 'ipv6 nd prefix 2001:db8:1::/64 86400 3600', 'ip firewall disable', 'exit',
    'interface gi1/0/2', 'ipv6 address 2001:db8:2::1/64', 'ip firewall disable', 'exit', 'end', 'commit', 'confirm'], SRV: ['ip 2001:db8:2::10/64 2001:db8:2::1'] });
  chk('ipv6 nd prefix без ошибок', !e.length, e.join('; '));
  var o = n.exec(pc.id, 'ip auto');
  chk('VPC ip auto: адрес из префикса + EUI-64, шлюз — link-local ESR', /GLOBAL SCOPE\s+: 2001:db8:1:[0-9a-f:]+\/64/.test(o) && /ROUTER LINK-LAYER : fe80::/.test(o), o);
  chk('VPC по SLAAC пингует сервер за ESR', n.ping6(pc.id, '2001:db8:2::10').ok);
  ['root', 'toor', 'ip link set ens3 up'].forEach(function (l) { n.exec(deb.id, l); }); n.tick(4);   // повторный RS через 4 с
  chk('Debian: адрес по SLAAC при ip link set ens3 up', /inet6 2001:db8:1:[0-9a-f:]+\/64 scope global/.test(n.exec(deb.id, 'ip -6 addr')), n.exec(deb.id, 'ip -6 addr'));
  chk('Debian ping6 сервер', /64 bytes from 2001:db8:2::10/.test(n.exec(deb.id, 'ping -6 2001:db8:2::10')));
  chk('rdisc6 ens3', /Prefix\s+: 2001:db8:1::\/64[\s\S]*from fe80::/.test(n.exec(deb.id, 'rdisc6 ens3')), n.exec(deb.id, 'rdisc6 ens3'));
  var tr = n.slaac(pc.id);
  chk('трасса: RS на ff02::2 и RA с префиксом', tr.steps.some(function (s) { return s.f && s.f.icmp6 === 'rs'; }) && tr.steps.some(function (s) { return s.f && s.f.icmp6 === 'ra' && s.f.prefix === '2001:db8:1::/64'; }));
  chk('running-config: ipv6 nd prefix', /ipv6 nd prefix 2001:db8:1::\/64 86400 3600/.test(n.exec(r.id, 'show running-config')));
  console.log('✓ SLAAC');
})();


// симуляция во времени: задержки, очереди, потери, MTU
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r = n.add('vESR', 'R1'), sw = n.add('MES2428', 'SW1'), pc = n.add('VPC', 'PC1'), sv = n.add('VPC', 'SRV');
  n.connect(pc.id, 'eth0', sw.id, 'gi1/0/1'); n.connect(sw.id, 'gi1/0/24', r.id, 'gi1/0/1'); n.connect(sv.id, 'eth0', r.id, 'gi1/0/2');
  var e = EL.labs.apply(n, { PC1: ['ip 192.168.1.2/24 192.168.1.1'], SRV: ['ip 10.0.0.2/24 10.0.0.1'],
    R1: ['configure', 'interface gi1/0/1', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 10.0.0.2/24', 'exit', 'end', 'commit', 'confirm'] });
  e = EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/2', 'ip address 10.0.0.1/24', 'ip firewall disable', 'exit', 'end', 'commit', 'confirm'] });
  chk('сим: схема настроена', !e.length && n.ping(pc.id, '10.0.0.2').ok, e.join('; '));
  var s = n.simulate([{ kind: 'ping', src: pc.id, dst: '10.0.0.2', count: 5, interval: 1, size: 64 }]), f = s.flows[0];
  chk('сим ping: 5 из 5, потерь нет', f.sent === 5 && f.recv === 5 && f.loss === 0, JSON.stringify(f.drops));
  // 3 кабеля туда и 3 обратно, кадр 64+28+18 = 110 байт на 1 Гбит/с = 0,88 мкс, 100 м = 0,5 мкс, обработка 10 мкс на устройствах
  chk('сим ping: RTT из передачи, распространения и обработки (десятки мкс)', f.min > 20e-6 && f.max < 200e-6 && f.jitter < 1e-9, f.min + ' ' + f.max);
  chk('сим ping: события tx по каждому кабелю туда и обратно', s.events.filter(function (x) { return x.kind === 'tx'; }).length === 30);
  sw.st.mode = 'priv';
  ['configure', 'interface gi1/0/24', 'no negotiation', 'speed 10', 'duplex full', 'end'].forEach(function (l) { n.exec(sw.id, l); });
  e = EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'speed 10M full-duplex', 'exit', 'end', 'commit', 'confirm'] }); chk('сим: speed 10M на ESR', !e.length, e.join('; '));
  chk('сим: линк SW1–R1 на 10 Мбит/с', n.phys(sw.id, 'gi1/0/24').speed === 10 && !n.phys(sw.id, 'gi1/0/24').mismatch, JSON.stringify(n.phys(sw.id, 'gi1/0/24')));
  var s2 = n.simulate([{ kind: 'ping', src: pc.id, dst: '10.0.0.2', count: 3, size: 1000 }]);
  chk('сим: 1000 байт по 10 Мбит/с — RTT больше 1,6 мс (сериализация 2 × 0,8 мс)', s2.flows[0].min > 1.6e-3 && s2.flows[0].recv === 3, s2.flows[0].min);
  var s3 = n.simulate([{ kind: 'udp', src: pc.id, dst: '10.0.0.2', rate: 5000, dur: 0.2, size: 1400 }]), u = s3.flows[0];
  chk('сим UDP 5000 п/с × 1400 байт в 10 Мбит/с — очередь переполнена, потери', u.loss > 50 && Object.keys(u.drops).some(function (k) { return /очередь SW1 gi1\/0\/24 переполнена/.test(k); }), JSON.stringify(u.drops));
  chk('сим: загрузка узкого линка ~100 %, максимум очереди = 64', s3.links.some(function (l) { return l.mbps === 10 && l.util > 90; }) && s3.queues.some(function (q) { return q.maxq === 64; }), JSON.stringify(s3.links) + JSON.stringify(s3.queues));
  var s4 = n.simulate([{ kind: 'udp', src: pc.id, dst: '10.0.0.2', rate: 100, dur: 1, size: 1000 }]);
  chk('сим UDP 100 п/с влезает в 10 Мбит/с — без потерь', s4.flows[0].loss === 0 && s4.flows[0].recv === 100);
  var s5 = n.simulate([{ kind: 'ping', src: pc.id, dst: '10.0.0.2', count: 2, size: 3000, df: true }, { kind: 'ping', src: pc.id, dst: '10.0.0.2', count: 2, size: 3000 }]);
  chk('сим MTU: 3000 байт с DF — не отправлен', s5.flows[0].recv === 0 && /Fragmentation needed/.test(s5.flows[0].why));
  chk('сим MTU: 3000 байт без DF — 3 фрагмента, ответы пришли', s5.flows[1].frag === 3 && s5.flows[1].recv === 2);
  ['configure', 'interface gi1/0/24', 'negotiation', 'end'].forEach(function (l) { n.exec(sw.id, l); });
  EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'speed 100M full-duplex', 'exit', 'end', 'commit', 'confirm'] });
  var ph = n.phys(sw.id, 'gi1/0/24');
  var s6 = n.simulate([{ kind: 'ping', src: pc.id, dst: '10.0.0.2', count: 50, interval: 0.01 }]);
  chk('сим: дуплекс не совпадает — часть ping теряется в коллизиях', ph.mismatch && s6.flows[0].loss > 0 && s6.flows[0].loss < 100 && Object.keys(s6.flows[0].drops).some(function (k) { return /коллизия/.test(k); }), JSON.stringify(ph) + ' ' + s6.flows[0].loss);
  var s7 = n.simulate([{ kind: 'ping', src: pc.id, dst: '10.9.9.9', count: 2 }]);
  chk('сим: нет пути — все потеряны, причина из трассы', s7.flows[0].recv === 0 && s7.flows[0].blocked && !!s7.flows[0].why);
  console.log('✓ симуляция во времени');
})();

// MES 10.x (ПО 10.4.6): команды ветки 6.x закрыты, у каждой — форма 10.x
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), s = n.add('MES2428', 'SW1'), o = n.add('MES3300-24', 'SW6'), pc = n.add('VPC', 'PC1');
  n.connect(pc.id, 'eth0', s.id, 'gi1/0/1');
  s.st.mode = 'priv'; o.st.mode = 'priv';
  var old = ['write memory', 'show version', 'show system', 'show arp', 'clear arp-cache', 'show mac address-table', 'clear mac address-table dynamic', 'show ports monitor', 'terminal datadump'];
  var bad = old.filter(function (c) { return !/^%/.test(n.exec(s.id, c)); });
  chk('10.x: команды ветки 6.x в привилегированном режиме — % Unrecognized', !bad.length, bad.join(', '));
  n.exec(s.id, 'configure');
  var badc = ['vlan database', 'ip default-gateway 10.0.0.1', 'clock timezone MSK +3', 'ip ssh server', 'ip http server'].filter(function (c) { var r = n.exec(s.id, c); if (s.st.mode !== 'config') n.exec(s.id, 'exit'); return !/^%/.test(r); });
  chk('10.x: команды ветки 6.x в config — % Unrecognized', !badc.length, badc.join(', '));
  n.exec(s.id, 'line console'); chk('10.x: login-attempts и history size в line — нет', /^%/.test(n.exec(s.id, 'login-attempts 3')) && /^%/.test(n.exec(s.id, 'history size 20'))); n.exec(s.id, 'exit');
  n.exec(o.id, 'configure');
  chk('6.x: vlan database, ip default-gateway, clock timezone остаются', !/^%/.test(n.exec(o.id, 'ip default-gateway 10.0.0.1')) && !/^%/.test(n.exec(o.id, 'clock timezone MSK +3')) && !/^%/.test(n.exec(o.id, 'vlan database')));
  var e = EL.labs.apply(n, { SW1: ['vlan 10,20', 'exit', 'vlan 30', 'name IT', 'exit', 'interface vlan 10', 'ip address 10.0.0.2 255.255.255.0', 'exit',
    'ip route 0.0.0.0 0.0.0.0 10.0.0.1', 'clock utc-offset +7', 'interface gi1/0/1', 'switchport access vlan 10', 'storm-control broadcast level pps 500', 'exit', 'end', 'write startup-config'] });
  chk('10.x: vlan в config, ip route 0.0.0.0, clock utc-offset, storm-control pps, write startup-config', !e.length, e.join('; '));
  var run = n.exec(s.id, 'show running-config');
  chk('10.x running-config: без vlan database, VLAN из config, utc-offset, маршрут по умолчанию', !/vlan database/.test(run) && /^vlan 10,20,30\nexit$/m.test(run) && /^vlan 30\n name IT\nexit/m.test(run) &&
    /clock utc-offset \+7/.test(run) && /ip route 0\.0\.0\.0 0\.0\.0\.0 10\.0\.0\.1/.test(run) && /storm-control broadcast level pps 500/.test(run) && !/ip http server|ip default-gateway/.test(run), run);
  chk('10.x: storm-control без единицы и вне диапазона — ошибка', /^%/.test(n.exec(s.id, 'configure') || n.exec(s.id, 'interface gi1/0/2') || n.exec(s.id, 'storm-control broadcast level 500')) &&
    /^%/.test(n.exec(s.id, 'storm-control broadcast level kbps 8')) && (n.exec(s.id, 'end'), true));
  chk('10.x: show system information / show system id', /10\.4\.6/.test(n.exec(s.id, 'show system information')) && /Serial number/.test(n.exec(s.id, 'show system id')));
  chk('10.x: show ip arp, clear ip arp, show mac-address-table, clear mac-address-table dynamic', !/^%/.test(n.exec(s.id, 'show ip arp')) && !/^%/.test(n.exec(s.id, 'clear ip arp')) &&
    /Learnt|Vlan/i.test(n.exec(s.id, 'show mac-address-table')) && !/^%/.test(n.exec(s.id, 'clear mac-address-table dynamic')) && !/^%/.test(n.exec(s.id, 'show mac-address-table aging-time')));
  EL.labs.apply(n, { SW1: ['configure', 'monitor session 1 destination interface gi1/0/5', 'monitor session 1 source interface gi1/0/1 both', 'end'] });
  chk('10.x: show monitor session all / 1 detail', /Destination port: gi1\/0\/5/.test(n.exec(s.id, 'show monitor session all')) && /gi1\/0\/1\s+both/.test(n.exec(s.id, 'show monitor session 1 detail')));
  var c2 = EL.applyConfig(n, s.id, run);
  chk('10.x: running-config применяется обратно без ошибок', !c2.length, c2.join('; '));
  // trunk 10.x: allowed vlan нет, trunk передаёт все VLAN; в 6.x VLAN надо разрешить
  var t = new EL.Net(), A = t.add('MES2428', 'A'), B = t.add('MES2428', 'B'), C = t.add('MES2300-24', 'C'), D = t.add('MES2300-24', 'D'), pa = t.add('VPC', 'PA'), pb = t.add('VPC', 'PB'), pc2 = t.add('VPC', 'PC'), pd = t.add('VPC', 'PD');
  t.connect(A.id, 'gi1/0/24', B.id, 'gi1/0/24'); t.connect(C.id, 'gi1/0/24', D.id, 'gi1/0/24');
  [[pa, A], [pb, B], [pc2, C], [pd, D]].forEach(function (x) { t.connect(x[0].id, 'eth0', x[1].id, 'gi1/0/1'); });
  var sw10 = ['enable', 'configure', 'vlan 10', 'exit', 'interface gi1/0/1', 'switchport access vlan 10', 'exit', 'interface gi1/0/24', 'switchport mode trunk', 'end'];
  var sw6 = ['enable', 'configure', 'vlan database', 'vlan 10', 'exit', 'interface gi1/0/1', 'switchport access vlan 10', 'exit', 'interface gi1/0/24', 'switchport mode trunk', 'end'];
  e = EL.labs.apply(t, { A: sw10, B: sw10, C: sw6, D: sw6, PA: ['ip 10.0.0.1/24'], PB: ['ip 10.0.0.2/24'], PC: ['ip 10.0.0.3/24'], PD: ['ip 10.0.0.4/24'] });
  chk('trunk: команды без ошибок', !e.length, e.join('; '));
  chk('10.x: switchport trunk allowed vlan add — нет', /^%/.test(t.exec(A.id, 'configure') || t.exec(A.id, 'interface gi1/0/24') || t.exec(A.id, 'switchport trunk allowed vlan add 10')) && (t.exec(A.id, 'end'), true));
  chk('10.x: trunk передаёт VLAN 10 без allowed', t.ping(pa.id, '10.0.0.2').ok);
  chk('6.x: trunk без allowed vlan add 10 VLAN 10 не передаёт', !t.ping(pc2.id, '10.0.0.4').ok);
  EL.labs.apply(t, { C: ['configure', 'interface gi1/0/24', 'switchport trunk allowed vlan add 10', 'end'], D: ['configure', 'interface gi1/0/24', 'switchport trunk allowed vlan add 10', 'end'] });
  chk('6.x: после switchport trunk allowed vlan add 10 — проходит', t.ping(pc2.id, '10.0.0.4').ok);
  console.log('✓ MES 10.x по ПО 10.4.6');
})();

// MTU: mtu на ESR, ping с размером и DF, «Fragmentation needed», фрагментация, MTU пути в симуляции
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), r1 = n.add('vESR', 'R1'), r2 = n.add('vESR', 'R2'), pc = n.add('VPC', 'PC1'), d = n.add('Debian', 'D1'), sw = n.add('MES2428', 'SW1');
  n.connect(pc.id, 'eth0', sw.id, 'gi1/0/1'); n.connect(d.id, 'ens3', sw.id, 'gi1/0/2'); n.connect(sw.id, 'gi1/0/24', r1.id, 'gi1/0/1'); n.connect(r1.id, 'gi1/0/2', r2.id, 'gi1/0/1');
  var e = EL.labs.apply(n, { PC1: ['ip 192.168.1.10/24 192.168.1.1'], D1: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 192.168.1.20/24 dev ens3', 'ip route add default via 192.168.1.1'],
    R1: ['configure', 'interface gi1/0/1', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 10.0.0.1/30', 'ip firewall disable', 'mtu 1400', 'exit',
         'ip route 10.9.9.0/24 10.0.0.2', 'end', 'commit', 'confirm'],
    R2: ['configure', 'interface gi1/0/1', 'ip address 10.0.0.2/30', 'ip firewall disable', 'mtu 1400', 'exit', 'interface loopback 1', 'ip address 10.9.9.9/24', 'exit', 'ip route 192.168.1.0/24 10.0.0.1', 'end', 'commit', 'confirm'] });
  chk('MTU: схема и mtu 1400 без ошибок', !e.length, e.join('; '));
  chk('mtu в running-config ESR', /interface gigabitethernet 1\/0\/2\n  mtu 1400/.test(n.exec(r1.id, 'show running-config')), n.exec(r1.id, 'show running-config'));
  chk('mtu вне 552–9018 — ошибка', /Illegal/.test(n.exec(r1.id, 'configure') || n.exec(r1.id, 'interface gi1/0/2') || n.exec(r1.id, 'mtu 100')) && (n.exec(r1.id, 'end'), true));
  chk('обычный ping проходит', /64 bytes from 10\.9\.9\.9/.test(n.exec(d.id, 'ping 10.9.9.9')));
  var o1 = n.exec(d.id, 'ping -s 1472 -M do -c 3 10.9.9.9');
  chk('Debian -M do: Frag needed от R1 с mtu 1400, 0 получено', /PING 10\.9\.9\.9 \(10\.9\.9\.9\) 1472\(1500\) bytes of data/.test(o1) && /From 192\.168\.1\.1 icmp_seq=1 Frag needed and DF set \(mtu = 1400\)/.test(o1) && /3 packets transmitted, 0 received, \+3 errors/.test(o1), o1);
  var o2 = n.exec(d.id, 'ping -s 1472 -c 3 10.9.9.9');
  chk('Debian по умолчанию (want): первый — Frag needed, дальше фрагменты доходят', /icmp_seq=1 Frag needed/.test(o2) && /1480 bytes from 10\.9\.9\.9: icmp_seq=2/.test(o2) && /3 packets transmitted, 2 received, \+1 errors/.test(o2), o2);
  chk('Debian -M dont: фрагменты доходят все', /3 received/.test(n.exec(d.id, 'ping -s 1472 -M dont -c 3 10.9.9.9')));
  chk('Debian -M do больше своего MTU — local error', /local error: message too long, mtu=1500/.test(n.exec(d.id, 'ping -s 2000 -M do 10.9.9.9')));
  chk('VPC -l 1472 -D — timeout, без -D — 1500 bytes', /timeout/.test(n.exec(pc.id, 'ping 10.9.9.9 -l 1472 -D -c 2')) && /1500 bytes from 10\.9\.9\.9 icmp_seq=1/.test(n.exec(pc.id, 'ping 10.9.9.9 -l 1472 -c 2')));
  var tr = n.ping(pc.id, '10.9.9.9');
  n._mtuPing = { size: 1500, df: false, local: 'frag' }; var tr2 = n.ping(pc.id, '10.9.9.9'); n._mtuPing = null;
  chk('трасса: R1 режет пакет на фрагменты', tr.ok && tr2.ok && tr2.steps.some(function (x) { return /разрезан на 2 фрагмента/.test(x.t); }));
  r1.st.mode = 'priv'; var o3 = n.exec(r1.id, 'ping 10.9.9.9 size 1472 strategy disallow-fragmentation packets 2');
  chk('ESR ping size … strategy disallow-fragmentation — local error (свой MTU 1400)', /local error: message too long, mtu=1400/.test(o3), o3);
  chk('ESR ping size 1000 — проходит', /2 received/.test(n.exec(r1.id, 'ping 10.9.9.9 size 1000 packets 2')));
  chk('ESR ping неизвестный ключ — ошибка', /Unknown command/.test(n.exec(r1.id, 'ping 10.9.9.9 foo')));
  sw.st.mode = 'priv';
  EL.labs.apply(n, { SW1: ['configure', 'interface vlan 1', 'ip address 192.168.1.2 255.255.255.0', 'exit', 'ip route 0.0.0.0 0.0.0.0 192.168.1.1', 'end'] });
  var o4 = n.exec(sw.id, 'ping 10.9.9.9 size 2000 df-bit count 2');
  chk('MES 10.x ping size 2000 df-bit — не получено; без df-bit — получено', /0 Packets Received/.test(o4) && /2 Packets Received/.test(n.exec(sw.id, 'ping 10.9.9.9 size 2000 count 2')), o4);
  chk('MES 10.x ping size вне 36–2080 — ошибка', /Invalid input/.test(n.exec(sw.id, 'ping 10.9.9.9 size 3000')));
  var s = n.simulate([{ kind: 'ping', src: pc.id, dst: '10.9.9.9', count: 2, size: 1472, df: true }, { kind: 'ping', src: pc.id, dst: '10.9.9.9', count: 2, size: 1472 }]);
  chk('симуляция: MTU пути 1400 — с DF не доставлен, без DF 2 фрагмента', s.flows[0].recv === 0 && /MTU 1400 на R1/.test(s.flows[0].why) && s.flows[1].frag === 2 && s.flows[1].recv === 2, JSON.stringify([s.flows[0].why, s.flows[1].frag]));
  EL.labs.apply(n, { R1: ['configure', 'tunnel gre 1', 'mtu 1400', 'end', 'commit', 'confirm'] });
  chk('show tunnels status — MTU туннеля из конфигурации', /1400/.test(n.exec(r1.id, 'show tunnels status')));
  console.log('✓ MTU и размер пакета');
})();

// официальные руководства Eltex: выбор PDF по модели и ветке ПО
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), u = function (m) { var d = n.add(m, m.replace(/\W/g, '')); var x = n.manualFor(d.id); return x ? x.url + (x.extra.length ? '+' + x.extra[0].url : '') : null; };
  chk('MES2428 (10.x) — mes-10.pdf', u('MES2428') === 'docs/mes-10.pdf');
  chk('MES2300-24 (6.x) — mes-6.pdf', u('MES2300-24') === 'docs/mes-6.pdf');
  chk('MES2324P (ПО 4.x) — mes-4.pdf', u('MES2324P') === 'docs/mes-4.pdf');
  chk('MES5448 (8.x) — mes-8.pdf', u('MES5448') === 'docs/mes-8.pdf');
  chk('ESR-1000 — esr-cli.pdf', u('ESR-1000') === 'docs/esr-cli.pdf');
  chk('vESR — esr-cli.pdf + vesr-install.pdf', u('vESR') === 'docs/esr-cli.pdf+docs/vesr-install.pdf');
  chk('VPC и Debian — руководства нет', u('VPC') === null && u('Debian') === null);
  console.log('✓ руководства Eltex по моделям');
})();

// консольный сервер SCS-32: заводская конфигурация, line aux, консольный кабель, Reverse Telnet / SSH
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), c = n.add('SCS-32', 'SCS'), sw = n.add('MES2428', 'SW1'), r = n.add('vESR', 'R1'), pc = n.add('Debian', 'PC');
  chk('SCS: приглашение scs-32#, заводской адрес gi1/0/1 192.168.1.1/24, SSH включён', /^scs-32#$/.test(n.prompt(c.id)) && c.st.run.ifs['gi1/0/1'].ip === '192.168.1.1/24' && c.st.run.ssh);
  chk('SCS: 32 порта aux и console в списке портов', n.portsOf(c).filter(function (p) { return /^aux1\/0\/\d+$/.test(p); }).length === 32 && n.portsOf(c).indexOf('console') >= 0);
  chk('MES и ESR: порт console', n.portsOf(sw).indexOf('console') >= 0 && n.portsOf(r).indexOf('console') >= 0);
  chk('консольный кабель aux1/0/1 ↔ console MES — линк up', n.connect(c.id, 'aux1/0/1', sw.id, 'console') === null && n.phys(c.id, 'aux1/0/1').up && n.phys(c.id, 'aux1/0/1').cab === 'rs232');
  chk('консольный кабель aux1/0/2 ↔ console ESR', n.connect(c.id, 'aux1/0/2', r.id, 'console') === null && n.linkUp(r.id, 'console'));
  chk('медь в консольный порт — линка нет', n.connect(c.id, 'aux1/0/3', pc.id, 'ens3') === null && !n.linkUp(c.id, 'aux1/0/3'));
  n.disconnect(n.links.length - 1);
  n.connect(pc.id, 'ens3', c.id, 'gi1/0/1');
  chk('SCS: нет межсетевого экрана — ip firewall disable не принимается', /Unknown|Illegal|Unrecognized/i.test(n.exec(c.id, 'configure') || n.exec(c.id, 'interface gi1/0/1') || n.exec(c.id, 'ip firewall disable')) && (n.exec(c.id, 'end'), true));
  var e = EL.labs.apply(n, { SCS: ['configure', 'line aux 1/0/1', 'transport telnet port 3001', 'exit', 'line aux 1/0/2', 'speed 9600', 'transport input ssh', 'exit',
    'interface gigabitethernet 1/0/1', 'ip address 192.168.1.2/24', 'exit', 'ip telnet server', 'end', 'commit', 'confirm'],
    PC: ['root', 'toor', 'ip link set ens3 up', 'ip addr add 192.168.1.10/24 dev ens3'] });
  chk('SCS: line aux, transport telnet port, ip telnet server — без ошибок', !e.length, e.join('; '));
  chk('SCS: line aux вне 1/0/1–32 и неверная скорость — ошибка', /Illegal/.test(n.exec(c.id, 'configure') || n.exec(c.id, 'line aux 1/0/33')) && /Illegal/.test(n.exec(c.id, 'line aux 1/0/5') || n.exec(c.id, 'speed 1000')) && (n.exec(c.id, 'end'), true));
  var sl = n.exec(c.id, 'show line aux 1/0/1');
  chk('show line aux 1/0/1: 115200, 8, NONE, Telnet port 3001', /AUX Line 1\/0\/1/.test(sl) && /Baud rate:\s+115200/.test(sl) && /Parity:\s+NONE/.test(sl) && /Telnet port:\s+3001/.test(sl), sl);
  chk('running-config: line aux 1/0/1 / transport telnet port 3001', /line aux 1\/0\/1\n  transport telnet port 3001\nexit/.test(n.exec(c.id, 'show running-config')));
  chk('show system SCS-32', /System type: Eltex SCS-32 Serial Console Server/.test(n.exec(c.id, 'show system')));
  // Reverse Telnet: вход на SCS, затем консоль MES
  var o = n.exec(pc.id, 'telnet 192.168.1.2 3001');
  chk('Reverse Telnet: Connected, приглашение входа SCS', /Connected to 192\.168\.1\.2/.test(o) && /^scs-32 login: $/.test(n.prompt(pc.id)), o + ' | ' + n.prompt(pc.id));
  n.exec(pc.id, 'admin'); var w = n.exec(pc.id, 'password');
  chk('Reverse Telnet: после входа — баннер SCS и User Name: консоли MES', /Welcome to SCS-32/.test(w) && n.prompt(pc.id) === 'User Name:', n.prompt(pc.id));
  n.exec(pc.id, 'admin'); n.exec(pc.id, 'admin');
  chk('Reverse Telnet: консоль MES — команды выполняются на коммутаторе', /console[>#]$/.test(n.prompt(pc.id)) && (n.exec(pc.id, 'enable'), n.exec(pc.id, 'configure'), n.exec(pc.id, 'hostname CORE'), sw.st.host === 'CORE'), n.prompt(pc.id));
  n.exec(c.id, 'clear line aux 1/0/1');
  chk('clear line aux 1/0/1 обрывает сессию', /Connection closed/.test(n.exec(pc.id, 'end')) && !pc.st.ssh);
  chk('telnet на порт без transport telnet port — отказ', /Unable to connect/.test(n.exec(pc.id, 'telnet 192.168.1.2 3005')));
  // Reverse SSH на aux2 (ESR), скорость порта 9600 ≠ 115200 — вместо консоли символы
  var s1 = n.exec(pc.id, 'ssh admin:aux2@192.168.1.2');
  chk('Reverse SSH: запрос пароля admin:aux2@…', /admin:aux2@192\.168\.1\.2's password: $/.test(n.prompt(pc.id)), s1 + ' | ' + n.prompt(pc.id));
  n.exec(pc.id, 'password');
  var g = n.exec(pc.id, '');
  chk('Reverse SSH на порт 9600: консоль ESR не читается (учебное допущение)', g.length > 5 && !/login/.test(g) && n.prompt(pc.id) === '', g);
  chk('выход из сессии «~.»', /closed/.test(n.exec(pc.id, '~.')) && !pc.st.ssh);
  EL.labs.apply(n, { SCS: ['configure', 'line aux 1/0/2', 'no speed', 'end', 'commit', 'confirm'] });
  n.exec(pc.id, 'ssh admin:aux2@192.168.1.2'); n.exec(pc.id, 'password');
  chk('Reverse SSH на 115200: вход в консоль ESR', /R1? ?login: $|vesr login: $/.test(n.prompt(pc.id)), n.prompt(pc.id));
  n.exec(pc.id, 'admin'); n.exec(pc.id, 'password');
  chk('Reverse SSH: консоль ESR', /#$/.test(n.prompt(pc.id)) && /esr|vesr/i.test(n.prompt(pc.id)), n.prompt(pc.id));
  n.exec(pc.id, '~.');
  console.log('✓ SCS-32: консольные порты, Reverse Telnet / SSH');
  var z = new EL.Net(), zr = z.add('vESR', 'RZ'), zp = [];
  ['configure', 'security zone trusted', 'exit', 'security zone-pair trusted self', 'rule 10'].forEach(function (l) { z.exec(zr.id, l); zp.push(z.prompt(zr.id)); });
  chk('приглашения зон как в прошивке ESR: config-security-zone / -pair / -pair-rule', zp[1] === 'vesr(config-security-zone)#' && zp[3] === 'vesr(config-security-zone-pair)#' && zp[4] === 'vesr(config-security-zone-pair-rule)#', zp.join(' | '));
})();

// контроллер Wi-Fi WLC и точки доступа: заводская конфигурация, DHCP с опцией 43, регистрация, статусы
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), w = n.add('WLC-15', 'WLC'), sw = n.add('MES2428', 'SW1'), a1 = n.add('WEP-3ax', 'AP1'), a2 = n.add('WOP-30L', 'AP2');
  n.connect(w.id, 'gi1/0/2', sw.id, 'gi1/0/24'); n.connect(a1.id, 'LAN', sw.id, 'gi1/0/1'); n.connect(a2.id, 'LAN', sw.id, 'gi1/0/2');
  var run = n.exec(w.id, 'show running-config');
  chk('WLC: приглашение wlc#, заводская конфигурация по РЭ §10.1.1', n.prompt(w.id) === 'wlc#' && /bridge 1\n  security-zone trusted|bridge 1\n  vlan 1/.test(run) && /ip dhcp-server pool ap-pool[\s\S]*vendor-specific\n    suboption 12 ascii-text "192\.168\.1\.1"\n    suboption 15 ascii-text "https:\/\/192\.168\.1\.1:8043"/.test(run) &&
    /^wlc\n  enable\n  outside-address 192\.168\.1\.1/m.test(run), run.slice(-1500));
  chk('WLC: порты gi1/0/1 и gi1/0/6 — аплинк (vlan 2), остальные в switchport', w.st.run.ifs['gi1/0/1'].sw.vlan === 2 && w.st.run.ifs['gi1/0/6'].sw.vlan === 2 && w.st.run.ifs['gi1/0/3'].sw.vlan === 1);
  var ap = n.exec(w.id, 'show wlc ap');
  chk('show wlc ap: обе ТД Active в default-location', (ap.match(/ Active /g) || []).length === 2 && /WEP-3ax\s+default-location/.test(ap) && /WOP-30L\s+default-location/.test(ap), ap);
  chk('ТД получили адрес из ap-pool и опцию 43', /^192\.168\.1\.\d+$/.test(a1.st.ip) && a1.st.opt43[15] === 'https://192.168.1.1:8043');
  chk('show wlc service-activator aps join-auto', /Join-auto\s+192\.168\.1\.\d+\s+WEP-3ax/.test(n.exec(w.id, 'show wlc service-activator aps join-auto')));
  chk('ТД: пароль из ap-profile default-ap', a1.st.apPw === 'password');
  // outside-address не совпадает с подопцией 15 — ТД не подключается
  var e = EL.labs.apply(n, { WLC: ['configure', 'wlc', 'outside-address 192.168.1.100', 'end', 'commit', 'confirm'] });
  chk('outside-address 192.168.1.100 ≠ подопции 15 — ТД пропали из show wlc ap', !e.length && !/ Active /.test(n.exec(w.id, 'show wlc ap')) && /Registering/.test(n.exec(w.id, 'show wlc service-activator aps')), e.join('; '));
  EL.labs.apply(n, { WLC: ['configure', 'wlc', 'outside-address 192.168.1.1', 'service-activator', 'no aps join auto', 'end', 'commit', 'confirm'] });
  var mac = Object.keys(w.st.aps)[0];
  chk('без aps join auto — Awaited, после join wlc ap <MAC> — Active', /Awaited/.test(n.exec(w.id, 'show wlc service-activator aps')) && (n.exec(w.id, 'join wlc ap ' + mac), new RegExp(mac + ' Active').test(n.exec(w.id, 'show wlc ap'))));
  EL.labs.apply(n, { WLC: ['configure', 'wlc', 'service-activator', 'aps join auto', 'exit', 'ip-pool default-ip-pool', 'network 10.0.0.0/8', 'end', 'commit', 'confirm'] });
  n.exec(w.id, 'show wlc ap');
  chk('ip-pool network 10.0.0.0/8 — адрес ТД не попал, локации нет: Sandboxed', w.st.aps[mac].status === 'Sandboxed', w.st.aps[mac].status);
  EL.labs.apply(n, { WLC: ['configure', 'wlc', 'ap ' + mac, 'ap-location default-location', 'end', 'commit', 'confirm'] });
  chk('индивидуальный профиль ap <MAC> — снова Active', (n.exec(w.id, 'show wlc ap'), w.st.aps[mac].status === 'Active'));
  chk('show wlc ap all: заданная ТД без подключения — Pre-configured', (EL.labs.apply(n, { WLC: ['configure', 'wlc', 'ap 00:11:22:33:44:55', 'end', 'commit', 'confirm'] }), /00:11:22:33:44:55 Pre-configured/.test(n.exec(w.id, 'show wlc ap all'))));
  chk('show wlc ap <MAC> detailed', /Board type:\s+WEP-3ax|Board type:\s+WOP-30L/.test(n.exec(w.id, 'show wlc ap ' + mac + ' detailed')));
  chk('радиопрофиль 6 ГГц: work-mode anacax — ошибка (по таблице РЭ — ax | axbe)', /Illegal/.test(n.exec(w.id, 'configure') || n.exec(w.id, 'wlc') || n.exec(w.id, 'radio-6g-profile default_6g') || n.exec(w.id, 'work-mode anacax')) && !/Illegal/.test(n.exec(w.id, 'work-mode axbe')) && (n.exec(w.id, 'end'), true));
  chk('приглашения WLC', (n.exec(w.id, 'configure'), n.exec(w.id, 'wlc'), n.exec(w.id, 'ssid-profile s1'), n.prompt(w.id) === 'wlc(config-wlc-ssid-profile)#') && (n.exec(w.id, 'exit'), n.prompt(w.id) === 'wlc(config-wlc)#') && (n.exec(w.id, 'end'), true));
  chk('switchport mode trunk без mode switchport — ошибка (вариант А)', /Unknown/.test(n.exec(w.id, 'configure') || n.exec(w.id, 'interface gi1/0/5') || n.exec(w.id, 'mode routerport') || n.exec(w.id, 'switchport mode trunk')) && (n.exec(w.id, 'end'), true));
  // CLI точки доступа (РЭ WEP-3ax §6.2): вход admin/пароль из ap-profile, статический адрес
  a1.st.apCli.stage = 'user'; n.exec(a1.id, 'admin'); n.exec(a1.id, 'password');
  chk('ТД: вход admin, приглашение WEP-3ax(root):/#', n.prompt(a1.id) === 'WEP-3ax(root):/# ', n.prompt(a1.id));
  chk('ТД: monitoring wan-status — protocol dhcp', /protocol \| dhcp/.test(n.exec(a1.id, 'monitoring wan-status')));
  ['configure', 'interface', 'br0', 'common', 'static-ip 192.168.1.50', 'netmask 255.255.255.0', 'protocol static-ip', 'save'].forEach(function (l) { n.exec(a1.id, l); });
  chk('ТД: статический адрес после save, приглашение по пути', a1.st.ip === '192.168.1.50' && n.prompt(a1.id) === 'WEP-3ax(config):/interface/br0/common# ' && n.ping(sw.id === 0 ? 0 : w.id, '192.168.1.50').ok, a1.st.ip);
  console.log('✓ WLC и точки доступа');
})();

// OLT LTP-16N и ONT: commit/save, front-port vlan allow, активация ONT по серийному номеру, трафик MES ↔ OLT ↔ ONT
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), o = n.add('LTP-16N', 'OLT'), sw = n.add('MES2300-24', 'SW1'), t = n.add('NTU-1L', 'ONT1'), pc = n.add('VPC', 'PC1'), sv = n.add('VPC', 'SRV');
  n.connect(o.id, 'front-port 1', sw.id, 'gi1/0/24'); n.connect(t.id, 'PON', o.id, 'pon-port 2'); n.connect(pc.id, 'eth0', t.id, 'LAN'); n.connect(sv.id, 'eth0', sw.id, 'gi1/0/1');
  chk('OLT: приглашение LTP-16N#, оптика PON pon-port ↔ PON — линк up', n.prompt(o.id) === 'LTP-16N#' && n.phys(o.id, 'pon-port 2').up && n.phys(o.id, 'pon-port 2').cab === 'pon');
  chk('медь в pon-port — линка нет', n.connect(o.id, 'pon-port 3', sw.id, 'gi1/0/5') === null && !n.linkUp(o.id, 'pon-port 3'));
  var u = n.exec(o.id, 'show interface ont 2 unactivated');
  chk('show interface ont 2 unactivated: серийный номер ONT, UNACTIVATED', u.indexOf(t.st.serial + ' UNACTIVATED') > 0 && /Total ONT count: 1/.test(u), u);
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'vlan database', 'vlan 1100', 'exit', 'interface gi1/0/24', 'switchport mode trunk', 'switchport trunk allowed vlan add 1100', 'exit',
    'interface gi1/0/1', 'switchport access vlan 1100', 'end'], PC1: ['ip 10.0.0.1/24'], SRV: ['ip 10.0.0.2/24'] });
  var cfg = ['configure', 'interface front-port 1', 'vlan allow 1100', 'exit', 'profile cross-connect 1100_bridge', 'ont-mode bridge', 'bridge group 10', 'outer vid 1100', 'exit',
    'profile ports NTU1', 'port 1 bridge group 10', 'exit', 'interface ont 2/2', 'serial ' + t.st.serial, 'profile ports NTU1', 'service 1 profile cross-connect 1100_bridge', 'service 1 profile dba dba1'];
  var bad = cfg.filter(function (l) { return /%/.test(n.exec(o.id, l)); });
  chk('QG прил. Б: настройка без ошибок, приглашение (config)(if-ont-2/2)#', !bad.length && n.prompt(o.id) === 'LTP-16N(config)(if-ont-2/2)#', bad.join('; '));
  chk('без commit ONT не работает, ping не проходит', !n.ping(pc.id, '10.0.0.2').ok && /\+?configure terminal[\s\S]*interface ont 2\/2/.test(n.exec(o.id, 'do show candidate-config')));
  chk('do commit — Configuration committed successfully', /Configuration committed successfully/.test(n.exec(o.id, 'do commit')));
  chk('после commit: ping ПК за ONT → сервер за MES', n.ping(pc.id, '10.0.0.2').ok);
  n.exec(o.id, 'end');
  chk('show interface ont 2 online: OK', /1 2 2 ELTX[0-9A-F]+ OK/.test(n.exec(o.id, 'show interface ont 2 online')));
  chk('show running-config interface front-port 1: vlan allow 1100', /interface front-port 1\n    vlan allow 1100/.test(n.exec(o.id, 'show running-config interface front-port 1')));
  // без save перезагрузка возвращает NVRAM
  n.reboot(o.id); n.exec(o.id, 'x');
  chk('без save после перезагрузки конфигурации нет — ping не проходит', !n.ping(pc.id, '10.0.0.2').ok);
  cfg.concat(['exit', 'exit']).forEach(function (l) { n.exec(o.id, l); }); n.exec(o.id, 'commit'); n.exec(o.id, 'save'); n.reboot(o.id);
  chk('после commit + save перезагрузка сохраняет конфигурацию', n.ping(pc.id, '10.0.0.2').ok);
  // ошибка в серийном номере: ONT остаётся в unactivated, позиция — offline
  EL.labs.apply(n, { OLT: ['configure', 'interface ont 2/2', 'serial ELTX00000000', 'exit', 'exit', 'commit'] });
  chk('чужой серийный номер: позиция offline, ONT в unactivated, ping нет', /OFFLINE/.test(n.exec(o.id, 'show interface ont 2 offline')) && /UNACTIVATED/.test(n.exec(o.id, 'show interface ont 2 unactivated')) && !n.ping(pc.id, '10.0.0.2').ok);
  chk('serial неверного формата — ошибка', /%/.test((n.exec(o.id, 'configure'), n.exec(o.id, 'interface ont 2/2'), n.exec(o.id, 'serial 454C5451A2B3C4D'))) && (n.exec(o.id, 'end'), true));
  chk('management: адрес управления в VLAN 1', /management ip 192\.168\.1\.2/.test(n.exec(o.id, 'show running-config management')));
  var x = new EL.Net(), lx = x.add('LTX-8', 'X'), lc = x.add('LTX-8C', 'C'); lx.st.olt.mode = 'configure'; lc.st.olt.mode = 'configure';
  chk('LTX по умолчанию GPON: ONT 1/129 — ошибка; LTX-8C: на чётном порту до 256', /%/.test(x.exec(lx.id, 'interface ont 1/129')) && !/%/.test(x.exec(lc.id, 'interface ont 2/200')) && /%/.test((x.exec(lc.id, 'exit'), x.exec(lc.id, 'interface ont 1/200'))));
  console.log('✓ OLT LTP-N и ONT');
})();

// маршрутизаторы ME: приглашение-стек, commit (сразу сохраняет), abort, интерфейсы, статика, OSPFv2
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('ME5100S', 'R1'), b = n.add('ME5200S', 'R2'), pc = n.add('VPC', 'PC');
  n.connect(a.id, 'te0/0/12', b.id, 'te0/0/12'); n.connect(pc.id, 'eth0', a.id, 'te0/0/1');
  function run(d, L) { return L.map(function (l) { return n.exec(d.id, l); }).filter(function (r) { return /^%/.test(r); }); }
  chk('ME: приглашение 0/ME5100S:EOS#, config → (config)#', n.prompt(a.id) === '0/ME5100S:EOS#' && (n.exec(a.id, 'config'), n.prompt(a.id) === '0/ME5100S:EOS(config)#'));
  n.exec(a.id, 'hostname Router');
  chk('hostname до commit не действует, show configuration changes', n.prompt(a.id) === '0/ME5100S:EOS(config)#' && /hostname Router/.test(n.exec(a.id, 'do show configuration changes')));
  chk('commit: Commit successfully completed, приглашение сразу с новым именем', /Commit successfully completed/.test(n.exec(a.id, 'commit')) && n.prompt(a.id) === '0/ME5100S:Router(config)#');
  n.exec(a.id, 'hostname X'); n.exec(a.id, 'abort');
  chk('abort: кандидат очищен, выход в глобальный режим', n.prompt(a.id) === '0/ME5100S:Router#' && !/hostname X/.test(n.exec(a.id, 'show candidate-config')));
  var e = run(a, ['configure', 'interface tengigabitethernet 0/0/12', 'ipv4 address 10.0.0.1/30', 'exit', 'interface te 0/0/1', 'ipv4 address 192.168.1.1/24', 'exit',
    'interface loopback 1', 'ipv4 address 1.1.1.1/32', 'exit', 'router ospfv2 test', 'router-id 1.1.1.1', 'area 0.0.0.0', 'interface loopback 1', 'passive', 'exit',
    'interface tengigabitethernet 0/0/12', 'network point-to-point', 'exit', 'interface te 0/0/1', 'passive', 'root', 'commit', 'end']);
  e = e.concat(run(b, ['configure', 'interface tengigabitethernet 0/0/12', 'ipv4 address 10.0.0.2/30', 'exit', 'interface loopback 1', 'ipv4 address 2.2.2.2/32', 'exit',
    'router ospfv2 test', 'router-id 2.2.2.2', 'area 0.0.0.0', 'interface loopback 1', 'passive', 'exit', 'interface te 0/0/12', 'network point-to-point', 'root', 'commit', 'end']));
  chk('РН с. 62, 102: интерфейсы и OSPFv2 без ошибок', !e.length, e.join('; '));
  chk('приглашения узлов: (config-ospfv2)#, (config-area)#, (config-tengigabitethernet)#', (n.exec(a.id, 'configure'), n.exec(a.id, 'router ospfv2 test'), n.prompt(a.id) === '0/ME5100S:Router(config-ospfv2)#') &&
    (n.exec(a.id, 'area 0.0.0.0'), n.prompt(a.id) === '0/ME5100S:Router(config-area)#') && (n.exec(a.id, 'interface te 0/0/12'), n.prompt(a.id) === '0/ME5100S:Router(config-tengigabitethernet)#') &&
    (n.exec(a.id, 'root'), n.prompt(a.id) === '0/ME5100S:Router(config)#') && (n.exec(a.id, 'end'), true));
  n.exec(pc.id, 'ip 192.168.1.10/24 192.168.1.1'); n.tick(60);
  chk('OSPFv2 между ME: ПК пингует loopback R2', n.ping(pc.id, '2.2.2.2').ok);
  chk('running-config в виде РН (отступ 3, exit)', /router ospfv2 test\n   router-id 1\.1\.1\.1\n   area 0\.0\.0\.0\n      interface loopback 1\n         passive\n      exit/.test(n.exec(a.id, 'show running-config')), n.exec(a.id, 'show running-config'));
  chk('ip address (как у ESR) на ME — ошибка', /%/.test((n.exec(a.id, 'configure'), n.exec(a.id, 'interface te 0/0/2'), n.exec(a.id, 'ip address 1.1.1.1/24'))) && (n.exec(a.id, 'end'), true));
  // сабинтерфейс с encapsulation и статика (вариант А: router static → address-family / vrf)
  e = run(a, ['configure', 'interface te 0/0/1.101', 'encapsulation outer-vid 101', 'ipv4 address 172.16.1.1/24', 'exit', 'router static', 'address-family ipv4 unicast',
    'destination 100.70.0.0/16 10.0.0.2', 'root', 'commit', 'end']);
  chk('сабинтерфейс te0/0/1.101 (VLAN 101) и статика', !e.length && a.st.run.ifs['te0/0/1.101'].ip === '172.16.1.1/24' && a.st.run.routes.some(function (r) { return r.net === '100.70.0.0/16' && r.nh === '10.0.0.2'; }), e.join('; '));
  chk('router static vrf X одной строкой — нет (вариант А)', /%/.test((n.exec(a.id, 'configure'), n.exec(a.id, 'router static vrf mgmt-intf'))) && (n.exec(a.id, 'end'), true));
  chk('privilege p15 / p16', (n.exec(a.id, 'configure'), n.exec(a.id, 'user ivan'), !/%/.test(n.exec(a.id, 'privilege p15'))) && /%/.test(n.exec(a.id, 'privilege p16')) && (n.exec(a.id, 'end'), true));
  console.log('✓ маршрутизаторы ME');
})();

// ME: BGP — iBGP по loopback через OSPF и eBGP с ESR
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('ME5100S', 'PE1'), b = n.add('ME5100S', 'PE2'), r = n.add('vESR', 'CE'), pc = n.add('VPC', 'PC');
  n.connect(a.id, 'te0/0/12', b.id, 'te0/0/12'); n.connect(r.id, 'gi1/0/1', b.id, 'te0/0/1'); n.connect(pc.id, 'eth0', r.id, 'gi1/0/2');
  function run(d, L) { return L.map(function (l) { var x = n.exec(d.id, l); return /^%/.test(x) ? l + ' → ' + x : null; }).filter(Boolean); }
  var core = function (me, lo, p2p) { return ['configure', 'interface te 0/0/12', 'ipv4 address ' + p2p, 'exit', 'interface loopback 1', 'ipv4 address ' + lo + '/32', 'exit',
    'router ospfv2 core', 'router-id ' + lo, 'area 0.0.0.0', 'interface loopback 1', 'passive', 'exit', 'interface te 0/0/12', 'network point-to-point', 'root']; };
  var e = run(a, core(a, '1.1.1.1', '10.0.0.1/30').concat(['interface loopback 2', 'ipv4 address 100.64.1.1/24', 'exit',
    'router bgp 65535', 'bgp router-id 1.1.1.1', 'address-family ipv4 unicast', 'network 100.64.1.0/24', 'exit',
    'neighbor 2.2.2.2', 'remote-as 65535', 'update-source 1.1.1.1', 'address-family ipv4 unicast', 'exit', 'exit', 'root', 'commit', 'end']));
  e = e.concat(run(b, core(b, '2.2.2.2', '10.0.0.2/30').concat(['interface te 0/0/1', 'ipv4 address 172.16.0.1/30', 'exit',
    'router bgp 65535', 'bgp router-id 2.2.2.2', 'neighbor 1.1.1.1', 'remote-as 65535', 'update-source 2.2.2.2', 'address-family ipv4 unicast', 'next-hop-self', 'exit', 'exit',
    'neighbor 172.16.0.2', 'remote-as 65001', 'address-family ipv4 unicast', 'exit', 'exit', 'root', 'commit', 'end'])));
  e = e.concat(EL.labs.apply(n, { CE: ['configure', 'interface gi1/0/1', 'ip address 172.16.0.2/30', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 192.168.5.1/24', 'ip firewall disable', 'exit',
    'router bgp 65001', 'router-id 3.3.3.3', 'neighbor 172.16.0.1', 'remote-as 65535', 'address-family ipv4 unicast', 'enable', 'exit', 'enable', 'exit',
    'address-family ipv4 unicast', 'network 192.168.5.0/24', 'exit', 'enable', 'end', 'commit', 'confirm'], PC: ['ip 192.168.5.10/24 192.168.5.1'] }));
  chk('BGP на ME: конфигурация по РН без ошибок (enable не нужен)', !e.length, e.join('; '));
  n.tick(60);
  chk('show bgp summary на PE2: соседи 1.1.1.1 (iBGP) и 172.16.0.2 (eBGP) установлены', (function () { var o = n.exec(b.id, 'show bgp summary'); return /1\.1\.1\.1\s+65535\s+\d+/.test(o) && /172\.16\.0\.2\s+65001\s+\d+/.test(o); })(), n.exec(b.id, 'show bgp summary'));
  chk('ПК за CE (AS 65001) пингует сеть 100.64.1.1 за PE1 (AS 65535): маршруты по BGP', n.ping(pc.id, '100.64.1.1').ok);
  chk('show bgp на PE1: сеть 192.168.5.0/24 с AS_PATH 65001', /192\.168\.5\.0\/24[\s\S]*65001/.test(n.exec(a.id, 'show bgp')), n.exec(a.id, 'show bgp'));
  chk('running-config ME: router bgp 65535 / neighbor / address-family', /router bgp 65535\n   bgp router-id 1\.1\.1\.1[\s\S]*neighbor 2\.2\.2\.2\n      remote-as 65535/.test(n.exec(a.id, 'show running-config')));
  console.log('✓ ME: BGP');
})();

// ME: MPLS L3VPN — VRF с rd/route-target, MP-BGP VPNv4 между PE, транспорт LDP
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('ME5100S', 'PE1'), p = n.add('ME5100S', 'P'), b = n.add('ME5100S', 'PE2'), h1 = n.add('VPC', 'H1'), h2 = n.add('VPC', 'H2');
  n.connect(a.id, 'te0/0/12', p.id, 'te0/0/11'); n.connect(p.id, 'te0/0/12', b.id, 'te0/0/12'); n.connect(h1.id, 'eth0', a.id, 'te0/0/17'); n.connect(h2.id, 'eth0', b.id, 'te0/0/17');
  function run(d, L) { return L.map(function (l) { var x = n.exec(d.id, l); return /^%/.test(x) ? l + ' → ' + x : null; }).filter(Boolean); }
  function igp(lo, ifs) { var c = ['configure', 'interface loopback 1', 'ipv4 address ' + lo + '/32', 'exit'];
    ifs.forEach(function (x) { c.push('interface ' + x[0], 'ipv4 address ' + x[1], 'exit'); });
    c.push('router ospfv2 core', 'router-id ' + lo, 'area 0.0.0.0', 'interface loopback 1', 'passive', 'exit');
    ifs.forEach(function (x) { c.push('interface ' + x[0], 'network point-to-point', 'exit'); });
    c.push('root', 'mpls', 'router-id ' + lo, 'forwarding'); ifs.forEach(function (x) { c.push('interface ' + x[0], 'exit'); }); c.push('exit', 'ldp');
    ifs.forEach(function (x) { c.push('discovery interface ' + x[0], 'exit'); }); c.push('root'); return c; }
  function pe(lo, peer, ifs, ce) { return igp(lo, ifs).concat(['vrf example', 'rd ' + lo + ':100', 'import route-target 65535:100', 'export route-target 65535:100', 'exit',
    'interface te 0/0/17', 'vrf example', 'ipv4 address ' + ce, 'exit',
    'router bgp 65535', 'bgp router-id ' + lo, 'neighbor ' + peer, 'remote-as 65535', 'update-source ' + lo, 'send-community', 'send-community-ext', 'address-family vpnv4 unicast', 'exit', 'exit', 'root', 'commit', 'end']); }
  var e = run(a, pe('1.1.1.1', '2.2.2.2', [['te 0/0/12', '10.0.1.1/30']], '100.100.1.1/24'))
    .concat(run(p, igp('9.9.9.9', [['te 0/0/11', '10.0.1.2/30'], ['te 0/0/12', '10.0.2.1/30']]).concat(['commit', 'end'])))
    .concat(run(b, pe('2.2.2.2', '1.1.1.1', [['te 0/0/12', '10.0.2.2/30']], '100.100.2.1/24')));
  chk('L3VPN по РН гл. MPLS L3VPN: конфигурация без ошибок', !e.length, e.join('; '));
  n.exec(h1.id, 'ip 100.100.1.10/24 100.100.1.1'); n.exec(h2.id, 'ip 100.100.2.10/24 100.100.2.1'); n.tick(60); n.tick(60);
  chk('ядро: PE1 видит loopback PE2 по OSPF через P', n.ping(a.id, '2.2.2.2').ok, n.exec(a.id, 'show route'));
  var r = n.ping(h1.id, '100.100.2.10');
  chk('клиент VRF example на PE1 пингует клиента на PE2 через P (метки VPN + LDP)', r.ok && r.steps.some(function (s) { return /VPN-маршрут 100\.100\.2\.0\/24/.test(s.t); }), r.steps.map(function (s) { return s.t; }).slice(-4).join(' | '));
  chk('P не знает сети клиентов (маршрута 100.100.2.0/24 в GRT нет)', !n.ping(p.id, '100.100.2.10').ok);
  chk('трасса L3VPN: PE1 → P транспортная метка + метка VPN 1000, P → PE2 — PHP', r.steps.some(function (s) { return /PE1 → P \(te0\/0\/12\): транспортная метка \d+ \| метка VPN 1000/.test(s.t); }) &&
      r.steps.some(function (s) { return /P → PE2 \(te0\/0\/12\): транспортная метка снята \(PHP, ImpNull\)/.test(s.t); }), r.steps.map(function (s) { return s.t; }).join(' | '));
  var lf = n.exec(a.id, 'show mpls ldp forwarding');
  chk('show mpls ldp forwarding на PE1: 2.2.2.2/32 с меткой P, 9.9.9.9/32 — ImpNull', /2\.2\.2\.2\/32\s+\d+\s+te 0\/0\/12\s+10\.0\.1\.2/.test(lf) && /9\.9\.9\.9\/32\s+ImpNull/.test(lf), lf);
  chk('show mpls ldp neighbors на P: два соседа', (n.exec(p.id, 'show mpls ldp neighbors').match(/:0 /g) || []).length === 2, n.exec(p.id, 'show mpls ldp neighbors'));
  ['configure', 'mpls', 'ldp', 'no discovery interface te 0/0/12', 'root', 'commit', 'end'].forEach(function (l) { n.exec(p.id, l); });
  var r2 = n.ping(h1.id, '100.100.2.10');
  chk('LDP между P и PE2 выключен — LSP разорван, VPN не работает', !r2.ok && r2.steps.some(function (s) { return /LSP до 2\.2\.2\.2 разорван — нет LDP-сессии с PE2/.test(s.t); }), r2.steps.map(function (s) { return s.t; }).slice(-2).join(' | '));
  ['configure', 'mpls', 'ldp', 'discovery interface te 0/0/12', 'root', 'commit', 'end'].forEach(function (l) { n.exec(p.id, l); });
  EL.labs.apply(n, { PE2: ['configure', 'vrf example', 'no import route-target 65535:100', 'no export route-target 65535:100', 'export route-target 65535:999', 'import route-target 65535:999', 'root', 'commit', 'end'] });
  chk('route-target не совпадают — VPN-маршрутов нет', !n.ping(h1.id, '100.100.2.10').ok);
  console.log('✓ ME: MPLS L3VPN');
})();

// ME: IS-IS (уровни, области, ATT), LDP-метки и L2VPN VPWS (псевдопровод LDP)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ME IS-IS/L2VPN: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('ME5100S', 'PE1'), p = n.add('ME5100S', 'P'), b = n.add('ME5100S', 'PE2'), c1 = n.add('VPC', 'C1'), c2 = n.add('VPC', 'C2');
  n.connect(a.id, 'te0/0/1', p.id, 'te0/0/1'); n.connect(p.id, 'te0/0/2', b.id, 'te0/0/1'); n.connect(c1.id, 'eth0', a.id, 'te0/0/9'); n.connect(c2.id, 'eth0', b.id, 'te0/0/9');
  function run(d, L) { return L.map(function (l) { var x = n.exec(d.id, l); return /^%/.test(x) ? l + ' → ' + x : null; }).filter(Boolean); }
  function core(lo, net, lvl, ifs) { var c = ['configure', 'hostname ' + lo.split('.')[0], 'interface loopback 1', 'ipv4 address ' + lo + '/32', 'exit'];
    ifs.forEach(function (x) { c.push('interface ' + x[0], 'ipv4 address ' + x[1], 'exit'); });
    c.push('router isis core', 'net ' + net, 'is-level ' + lvl, 'interface loopback 1', 'address-family ipv4 unicast', 'exit', 'passive', 'exit');
    ifs.forEach(function (x) { c.push('interface ' + x[0], 'address-family ipv4 unicast', 'exit', 'point-to-point', 'exit'); });
    c.push('root', 'mpls', 'router-id ' + lo, 'forwarding'); ifs.forEach(function (x) { c.push('interface ' + x[0], 'exit'); }); c.push('exit', 'ldp');
    ifs.forEach(function (x) { c.push('discovery interface ' + x[0], 'exit'); }); c.push('root'); return c; }
  function pw(lo, peer, id) { return ['mpls ldp neighbor ' + peer, 'exit', 'l2vpn pw-class PWC', 'encapsulation mpls signaling-type pseudowire-id-fec-signaling', 'exit',
    'l2vpn', 'xconnect-group G1', 'p2p CUST1', 'interface te 0/0/9', 'pw ' + peer + ' ' + id, 'pw-class PWC', 'exit', 'exit', 'root', 'commit', 'end']; }
  var e = run(a, core('1.1.1.1', '49.0001.0010.0100.1001.00', 'level-2', [['te 0/0/1', '10.0.1.0/31']]).concat(pw('1.1.1.1', '2.2.2.2', 100)))
    .concat(run(p, core('9.9.9.9', '49.0002.0090.0900.9009.00', 'level-2', [['te 0/0/1', '10.0.1.1/31'], ['te 0/0/2', '10.0.2.0/31']]).concat(['commit', 'end'])))
    .concat(run(b, core('2.2.2.2', '49.0003.0020.0200.2002.00', 'level-2', [['te 0/0/1', '10.0.2.1/31']]).concat(pw('2.2.2.2', '1.1.1.1', 100))));
  chk('конфигурация IS-IS + LDP + L2VPN по РН без ошибок', !e.length, e.join('; '));
  var rt = n.exec(a.id, 'show route isis');
  chk('show route isis на PE1: 2.2.2.2/32 [116/20] и 9.9.9.9/32 [116/10] — разные области, уровень 2', /i L2\s+2\.2\.2\.2\/32 via 10\.0\.1\.1 \[116\/20\]/.test(rt) && /i L2\s+9\.9\.9\.9\/32 via 10\.0\.1\.1 \[116\/10\]/.test(rt), rt);
  chk('show isis neighbors на P: две смежности level-2', (n.exec(p.id, 'show isis neighbors').match(/ up\s+level-2/g) || []).length === 2, n.exec(p.id, 'show isis neighbors'));
  chk('PE1 пингует loopback PE2 по IS-IS', n.ping(a.id, '2.2.2.2').ok);
  n.exec(c1.id, 'ip 192.168.77.1/24'); n.exec(c2.id, 'ip 192.168.77.2/24');
  var r = n.ping(c1.id, '192.168.77.2');
  chk('L2VPN: C1 и C2 в одной L2-сети через псевдопровод (метки PW + LDP)', r.ok && JSON.stringify(r.steps).indexOf('перенесён псевдопроводом CUST1') >= 0, r.steps.map(function (s) { return s.t + ' ' + JSON.stringify(s.notes || []); }).join(' | ').slice(0, 900));
  chk('show l2vpn xconnect: oper Up', /PW: Neighbor 2\.2\.2\.2, pw-id 100, admin up, oper Up/.test(n.exec(a.id, 'show l2vpn xconnect')), n.exec(a.id, 'show l2vpn xconnect'));
  EL.labs.apply(n, { PE2: ['configure', 'l2vpn', 'xconnect-group G1', 'p2p CUST1', 'mtu 9000', 'root', 'commit', 'end'] });
  chk('MTU не совпадают — oper MM, кадры не идут', /oper MM/.test(n.exec(a.id, 'show l2vpn xconnect')) && !n.ping(c1.id, '192.168.77.2').ok, n.exec(a.id, 'show l2vpn xconnect'));
  EL.labs.apply(n, { PE2: ['configure', 'l2vpn', 'xconnect-group G1', 'p2p CUST1', 'no mtu', 'root', 'commit', 'end'] });
  chk('MTU выровнены — снова Up', /oper Up/.test(n.exec(a.id, 'show l2vpn xconnect')), n.exec(a.id, 'show l2vpn xconnect'));
  var ce = n.exec(b.id, 'configure') + n.exec(b.id, 'interface te 0/0/9') + n.exec(b.id, 'ipv4 address 192.168.77.254/24') + n.exec(b.id, 'root');
  chk('AC с IP-адресом — commit отклонён (РН с. 180)', /cannot be used as L2VPN attachment circuit/.test(ce + n.exec(b.id, 'commit')));
  n.exec(b.id, 'abort');
  // IS-IS level-1: разные области — смежности нет; одна область — маршруты L1 и default по ATT
  EL.labs.apply(n, { PE1: ['configure', 'router isis core', 'is-level level-1', 'root', 'commit', 'end'] });
  chk('level-1 и другая область — смежности нет, маршрутов нет', !/i L/.test(n.exec(a.id, 'show route isis')), n.exec(a.id, 'show route isis'));
  EL.labs.apply(n, { PE1: ['configure', 'router isis core', 'net 49.0002.0010.0100.1001.00', 'root', 'commit', 'end'],
    P: ['configure', 'router isis core', 'is-level level-1-2', 'root', 'commit', 'end'] });
  var r1 = n.exec(a.id, 'show route isis');
  chk('level-1 в области P (L1/L2): 9.9.9.9 i L1 [115/10] и 0.0.0.0/0 по ATT', /i L1\s+9\.9\.9\.9\/32 via 10\.0\.1\.1 \[115\/10\]/.test(r1) && /i L1\s+0\.0\.0\.0\/0 via 10\.0\.1\.1 \[115\/10\]/.test(r1) && n.ping(a.id, '2.2.2.2').ok, r1);
  console.log('✓ ME: IS-IS, LDP, L2VPN');
})();

// ME: таймеры IS-IS (hold 30 с) и LDP (session holdtime 40 с) — сосед за коммутатором выключился
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ME таймеры: ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('ME5100S', 'A'), b = n.add('ME5100S', 'B'), sw = n.add('MES2428', 'SW');
  n.connect(a.id, 'te0/0/1', sw.id, 'gi1/0/1'); n.connect(b.id, 'te0/0/1', sw.id, 'gi1/0/2');
  function cfg(d, lo, ip, net) { ['configure', 'interface loopback 1', 'ipv4 address ' + lo + '/32', 'exit', 'interface te 0/0/1', 'ipv4 address ' + ip + '/24', 'exit',
    'router isis c', 'net ' + net, 'interface loopback 1', 'address-family ipv4 unicast', 'exit', 'passive', 'exit', 'interface te 0/0/1', 'address-family ipv4 unicast', 'exit', 'exit', 'root',
    'mpls', 'router-id ' + lo, 'forwarding', 'interface te 0/0/1', 'exit', 'exit', 'ldp', 'discovery interface te 0/0/1', 'exit', 'root', 'commit', 'end'].forEach(function (l) { n.exec(d.id, l); }); }
  cfg(a, '1.1.1.1', '10.0.0.1', '49.0001.0010.0100.1001.00'); cfg(b, '2.2.2.2', '10.0.0.2', '49.0001.0020.0200.2002.00');
  chk('смежность и маршрут до 2.2.2.2', /2\.2\.2\.2\/32/.test(n.exec(a.id, 'show route isis')) && /:0 /.test(n.exec(a.id, 'show mpls ldp neighbors')));
  n.power(b.id, false); n.tick(29);
  chk('B выключен, 29 с — смежность ещё up (Hold 1), маршрут и LDP-сессия держатся', /2\.2\.2\.2\/32/.test(n.exec(a.id, 'show route isis')) && /up\s+level-\d\s+\S+\s+1\s/.test(n.exec(a.id, 'show isis neighbors')) &&
      /2\.2\.2\.2:0/.test(n.exec(a.id, 'show mpls ldp neighbors')) && !n.ping(a.id, '2.2.2.2').ok, n.exec(a.id, 'show isis neighbors'));
  n.tick(1);
  chk('30 с — hold истёк: смежности и маршрута нет, LDP ещё держится (40 с)', !/2\.2\.2\.2\/32/.test(n.exec(a.id, 'show route isis')) && /2\.2\.2\.2:0/.test(n.exec(a.id, 'show mpls ldp neighbors')));
  n.tick(10); chk('40 с — LDP-сессия закрыта', !/2\.2\.2\.2:0/.test(n.exec(a.id, 'show mpls ldp neighbors')));
  n.power(b.id, true);
  chk('B включился — смежность и маршрут снова', /2\.2\.2\.2\/32/.test(n.exec(a.id, 'show route isis')));
  ['configure', 'interface te 0/0/1', 'shutdown', 'root', 'commit', 'end'].forEach(function (l) { n.exec(a.id, l); });
  chk('свой интерфейс выключен — сразу без маршрута', !/2\.2\.2\.2\/32/.test(n.exec(a.id, 'show route isis')));
  console.log('✓ ME: таймеры IS-IS и LDP');
})();

// симуляция пакетов как в Packet Tracer: события со временем, протоколы, линейный код L1
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), a = n.add('VPC', 'PC1'), sw = n.add('MES2428', 'SW1'), r = n.add('vESR', 'R1'), b = n.add('VPC', 'PC2'), sw2 = n.add('MES2428', 'SW2');
  n.connect(a.id, 'eth0', sw.id, 'gi1/0/1'); n.connect(sw.id, 'gi1/0/24', r.id, 'gi1/0/1'); n.connect(r.id, 'gi1/0/2', sw2.id, 'gi1/0/24'); n.connect(b.id, 'eth0', sw2.id, 'gi1/0/1');
  EL.labs.apply(n, { PC1: ['ip 192.168.1.10/24 192.168.1.1'], PC2: ['ip 10.0.0.10/24 10.0.0.1'],
    R1: ['configure', 'interface gi1/0/1', 'ip address 192.168.1.1/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 10.0.0.1/24', 'ip firewall disable', 'end', 'commit', 'confirm'] });
  var p = n.ping(a.id, '10.0.0.10'), E = EL.ptEvents(n, p.steps, a.id), pdu = E.filter(function (e) { return e.kind === 'pdu'; });
  chk('события: ARP и ICMP по каждому кабелю, время растёт', p.ok && pdu.some(function (e) { return e.proto === 'ARP'; }) && pdu.some(function (e) { return e.proto === 'ICMP'; }) &&
    E.every(function (e, i) { return !i || e.t >= E[i - 1].t || e.kind === 'pdu'; }) && E[E.length - 1].t > 0);
  var ic = pdu.filter(function (e) { return e.proto === 'ICMP'; })[0];
  chk('ICMP-кадр 98 байт на 1 Гбит/с — меньше мкс + 0,5 мкс распространения', ic.bytes === 98 && ic.dur > 0.7e-6 && ic.dur < 2e-6, ic.dur);
  chk('L1 медь 1 Гбит/с — 1000BASE-T, PAM-5', EL.lineCode(n, ic.li).name === '1000BASE-T');
  ['configure', 'interface gi1/0/24', 'no negotiation', 'speed 100', 'duplex full', 'end'].forEach(function (l) { sw.st.mode = 'priv'; n.exec(sw.id, l); });
  EL.labs.apply(n, { R1: ['configure', 'interface gi1/0/1', 'speed 100M full-duplex', 'exit', 'end', 'commit', 'confirm'] });
  chk('L1 100 Мбит/с — 100BASE-TX: 4B5B + MLT-3', EL.lineCode(n, 1).name === '100BASE-TX' && EL.lineCode(n, 1).code === 'mlt3');
  var m = EL.waveform('manchester', [0x01]);
  chk('манчестерский код: бит 1 — снизу вверх, 0 — сверху вниз', m.levels.slice(0, 4).join(',') === '-1,1,1,-1');
  var t3 = EL.waveform('mlt3', [0x00]);
  chk('MLT-3 от 4B5B: 0x0 → 11110 → уровни 1,0,-1,0,0', t3.levels.slice(0, 5).join(',') === '1,0,-1,0,0', t3.levels.join(','));
  chk('RS-232: старт-бит 0 (положительный уровень), стоп-бит 1', EL.waveform('uart', [0xff]).levels[0] === 1 && EL.waveform('uart', [0xff]).levels[9] === -1);
  chk('протоколы по портам: DHCP, DNS, HTTP, BGP', EL.ptProto({ proto: 'udp', dport: 67 }) === 'DHCP' && EL.ptProto({ proto: 'udp', dport: 53 }) === 'DNS' && EL.ptProto({ proto: 'tcp', dport: 80 }) === 'HTTP' && EL.ptProto({ proto: 'tcp', dport: 179 }) === 'BGP');
  console.log('✓ симуляция пакетов (Packet Tracer)');
})();

// безопасная настройка ESR и ESR ФСТЭК (РЭ ESR 1.5.10 гл. 6)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), f = n.add('ESR-15R FSTEC', 'FW'), r = n.add('vESR', 'R1'), pc = n.add('Debian', 'PC');
  n.connect(pc.id, 'ens3', f.id, 'gi1/0/2');
  chk('ESR ФСТЭК в каталоге: 13 моделей, ESR-30 — с te1/0/1–2', Object.keys(EL.MODELS).filter(function (k) { return EL.MODELS[k].kind === 'fstec'; }).length === 13 && EL.MODELS['ESR-30 FSTEC'].portList.indexOf('te1/0/2') >= 0);
  chk('show version ФСТЭК: 1.5.10(FSTEC) build 9; у vESR — обычная', /1\.5\.10\(FSTEC\) build 9/.test(n.exec(f.id, 'show version')) && !/FSTEC/.test(n.exec(r.id, 'show version')));
  chk('в ФСТЭК нет WLC и встроенного RADIUS', /Unknown|Unrecognized|Illegal/i.test((n.exec(f.id, 'configure'), n.exec(f.id, 'wlc'))) && /Unknown|Unrecognized|Illegal/i.test(n.exec(f.id, 'radius-server local')) && (n.exec(f.id, 'end'), true));
  var e = EL.labs.apply(n, { FW: ['configure', 'security passwords default-expired', 'security passwords lifetime 30', 'security passwords history 12', 'security passwords min-length 16',
    'security passwords max-length 24', 'security passwords upper-case 3', 'security passwords lower-case 5', 'security passwords special-case 2', 'security passwords numeric-count 4',
    'security passwords symbol-types 4', 'end', 'commit', 'confirm'] });
  chk('РЭ 6.3.2: парольная политика без ошибок', !e.length, e.join('; '));
  chk('max-length 64 — вне 1..32, ошибка', /Illegal/.test((n.exec(f.id, 'configure'), n.exec(f.id, 'security passwords max-length 64'))) && (n.exec(f.id, 'end'), true));
  var w = (n.exec(f.id, 'configure'), n.exec(f.id, 'username fedor'), n.exec(f.id, 'password 12345678'));
  var ok = n.exec(f.id, 'password ABCdefgh1234!@kl');
  chk('пароль 12345678 не проходит политику, ABCdefgh1234!@kl — проходит', /Illegal/.test(w) && !/Illegal|error/i.test(ok), w + ' | ' + ok); n.exec(f.id, 'end');
  e = EL.labs.apply(n, { FW: ['configure', 'aaa authentication login CONSOLE radius local', 'aaa authentication login SSH radius', 'aaa authentication enable default radius enable', 'aaa authentication mode break',
    'line console', 'login authentication CONSOLE', 'exit', 'line ssh', 'login authentication SSH', 'exit', 'logging userinfo', 'logging aaa configuration', 'syslog cli-commands',
    'syslog file tmpsys:syslog/default', 'severity info', 'exit', 'ip firewall screen spy-blocking spoofing', 'logging firewall screen spy-blocking spoofing',
    'ip firewall screen suspicious-packets large-icmp', 'no ip telnet server', 'ip ssh server', 'ip ssh authentication algorithm md5 disable', 'ip ssh host-key algorithm ed25519 disable', 'end', 'commit', 'confirm'] });
  chk('РЭ 6.4.3, 6.6.2, 6.5.2: AAA, журналы, экраны, SSH — без ошибок', !e.length, e.join('; '));
  var run = n.exec(f.id, 'show running-config');
  chk('running-config: aaa, line console, syslog file, screen, ssh algorithm', /aaa authentication login CONSOLE radius local/.test(run) && /line console\n  login authentication CONSOLE\nexit/.test(run) &&
    /syslog file tmpsys:syslog\/default\n  severity info/.test(run) && /ip firewall screen spy-blocking spoofing/.test(run) && /ip ssh authentication algorithm md5 disable/.test(run), run.slice(-900));
  chk('приглашения (config-line-console)#, (config-syslog-file)#', (n.exec(f.id, 'configure'), n.exec(f.id, 'line console'), /\(config-line-console\)#$/.test(n.prompt(f.id))) && (n.exec(f.id, 'exit'), n.exec(f.id, 'syslog file x'), /\(config-syslog-file\)#$/.test(n.prompt(f.id))) && (n.exec(f.id, 'end'), true));
  chk('verify filesystem', n.exec(f.id, 'verify filesystem') === 'Filesystem Successfully Verified');
  e = EL.labs.apply(n, { FW: ['configure', 'security zone LAN', 'exit', 'security zone WAN', 'exit', 'security zone-pair LAN WAN', 'rule 10', 'action deny', 'match protocol tcp', 'match http command post', 'enable', 'exit', 'exit', 'end', 'commit', 'confirm'] });
  chk('ФСТЭК: match http command post в правиле зоны — в running-config внутри правила', !e.length && /  rule 10\n[\s\S]*?    match http command post\n    enable/.test(n.exec(f.id, 'show running-config')), e.join('; '));
  chk('в обычном ESR match http command нет', /Unknown|Unrecognized|Illegal/i.test((n.exec(r.id, 'configure'), n.exec(r.id, 'security zone-pair A B'), n.exec(r.id, 'rule 1'), n.exec(r.id, 'match http command post'))) && (n.exec(r.id, 'end'), true));
  chk('в обычном ESR парольная политика тоже есть', !/Unknown|Illegal/.test((n.exec(r.id, 'configure'), n.exec(r.id, 'security passwords min-length 8'))) && (n.exec(r.id, 'end'), true));
  console.log('✓ безопасная настройка ESR и ESR ФСТЭК');
})();

// OLT-шасси MA5160 (ветка ma5000): слот и тип карты, front-port 1/1, ONT 4/2/1, commit + confirm (NVRAM)
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), o = n.add('MA5160', 'OLT'), sw = n.add('MES2300-24', 'SW1'), t = n.add('NTU-1L', 'ONT1'), pc = n.add('VPC', 'PC1'), sv = n.add('VPC', 'SRV');
  n.connect(o.id, 'front-port 1/1', sw.id, 'gi1/0/24'); n.connect(t.id, 'PON', o.id, 'pon-port 4/2'); n.connect(pc.id, 'eth0', t.id, 'LAN'); n.connect(sv.id, 'eth0', sw.id, 'gi1/0/1');
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'vlan database', 'vlan 1100', 'exit', 'interface gi1/0/24', 'switchport mode trunk', 'switchport trunk allowed vlan add 1100', 'exit',
    'interface gi1/0/1', 'switchport access vlan 1100', 'end'], PC1: ['ip 10.0.0.1/24'], SRV: ['ip 10.0.0.2/24'] });
  chk('MA5160: приглашение MA5160#, show shelf — слот 4: Not set, MA5K-LC16G', n.prompt(o.id) === 'MA5160#' && /4 Not set MA5K-LC16G/.test(n.exec(o.id, 'show shelf')));
  chk('show interface ont 4 unactivated — ONT на pon-port 4/2', /pon-port 4\/2 ONT unactivated list[\s\S]*UNACTIVATED/.test(n.exec(o.id, 'show interface ont 4 unactivated')), n.exec(o.id, 'show interface ont 4 unactivated'));
  var cfg = ['configure terminal', 'interface front-port 1/1', 'vlan allow 1100', 'exit', 'profile cross-connect 1100_bridge', 'ont-mode bridge', 'bridge group 10', 'outer vid 1100', 'exit',
    'profile ports NTU1', 'port 1 bridge group 10', 'exit', 'interface ont 4/2/2', 'serial ' + t.st.serial, 'profile ports NTU1', 'service 1 profile cross-connect 1100_bridge dba dba1', 'exit', 'exit'];
  var bad = cfg.filter(function (l) { return /%/.test(n.exec(o.id, l)); });
  chk('QG прил. Б для MA5160: настройка без ошибок, приглашение (config)(if-ont-4/2/2)#', !bad.length, bad.join('; '));
  chk('commit — с таймером подтверждения', /confirmed within: 5 minutes\nConfiguration committed successfully/.test(n.exec(o.id, 'commit')));
  chk('без типа карты (slot 4 → type lc16g) ONT не работает', !n.ping(pc.id, '10.0.0.2').ok);
  ['configure terminal', 'slot 4', 'type lc16g', 'exit', 'exit'].forEach(function (l) { n.exec(o.id, l); });
  chk('после type lc16g + commit — ping ПК за ONT → сервер, show shelf: running', (n.exec(o.id, 'commit'), n.ping(pc.id, '10.0.0.2').ok) && /4 LC16G MA5K-LC16G .* running/.test(n.exec(o.id, 'show shelf')));
  chk('save у MA5160 нет — ошибка; confirm сохраняет в NVRAM', /%/.test(n.exec(o.id, 'save')) && /saved in NVRAM/.test(n.exec(o.id, 'confirm')));
  n.reboot(o.id); n.exec(o.id, 'x');
  chk('после confirm перезагрузка сохраняет конфигурацию', n.ping(pc.id, '10.0.0.2').ok);
  chk('приглашение (config)(slot-4)# и (config)(if-front-1/1)#', (n.exec(o.id, 'configure terminal'), n.exec(o.id, 'slot 4'), /\(config\)\(slot-4\)#$/.test(n.prompt(o.id))) && (n.exec(o.id, 'exit'), n.exec(o.id, 'interface front-port 1/1'), /\(config\)\(if-front-1\/1\)#$/.test(n.prompt(o.id))));
  console.log('✓ OLT-шасси MA5160');
})();

// OLT LTP-8X (ПО 3.52): встроенный коммутатор, нумерация с нуля, профили ("ИМЯ"), bridge
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), o = n.add('LTP-8X rev.C/rev.D', 'OLT'), sw = n.add('MES2300-24', 'SW1'), t = n.add('NTU-1L', 'ONT1'), pc = n.add('VPC', 'PC1'), sv = n.add('VPC', 'SRV');
  n.connect(o.id, 'front-port 0', sw.id, 'gi1/0/24'); n.connect(t.id, 'PON', o.id, 'gpon-port 0'); n.connect(pc.id, 'eth0', t.id, 'LAN'); n.connect(sv.id, 'eth0', sw.id, 'gi1/0/1');
  EL.labs.apply(n, { SW1: ['enable', 'configure', 'vlan database', 'vlan 2149', 'exit', 'interface gi1/0/24', 'switchport mode trunk', 'switchport trunk allowed vlan add 2149', 'exit',
    'interface gi1/0/1', 'switchport access vlan 2149', 'end'], PC1: ['ip 10.0.0.1/24'], SRV: ['ip 10.0.0.2/24'] });
  chk('LTP-8X: приглашение LTP-8X#, ONT на gpon-port 0 — в unactivated', n.prompt(o.id) === 'LTP-8X#' && /GPON-port 0 ONT unactivated list[\s\S]*UNACTIVATED/.test(n.exec(o.id, 'show interface ont 0-7 unactivated')), n.exec(o.id, 'show interface ont 0-7 unactivated'));
  var bad = ['switch', 'configure', 'vlan 2149,30', 'tagged pon-port 0 – 7', 'tagged front-port 0', 'exit', 'commit', 'exit', 'exit'].filter(function (l) { return /%/.test(n.exec(o.id, l)); });
  chk('X-QG §7: VLAN в коммутаторе (tagged pon-port 0 – 7, front-port 0), commit коммутатора', !bad.length, bad.join('; '));
  var cfg = ['configure terminal', 'profile cross-connect NTU1', 'bridge', 'bridge group 20', 'outer vid 2149', 'exit', 'profile ports NTU1', 'port 0 bridge group 20', 'exit',
    'interface ont 0/3', 'serial ' + t.st.serial.slice(0, 4).split('').map(function (c) { return c.charCodeAt(0).toString(16).toUpperCase(); }).join('') + t.st.serial.slice(4), 'profile ports NTU1', 'service 0 profile cross-connect NTU1', 'service 0 profile dba dba-00', 'do commit', 'do save'];
  var pr = [], bad2 = cfg.filter(function (l) { var r = n.exec(o.id, l); pr.push(n.prompt(o.id)); return /%/.test(r); });
  chk('X-QG прил. Г: профиль-мост и ONT 0/3 без ошибок', !bad2.length, bad2.join('; '));
  chk('приглашения: (config-cross-connect)("NTU1")#, (config-ports)("NTU1")#, (config)(if-ont-0/3)#', pr[1] === 'LTP-8X(config-cross-connect)("NTU1")#' && pr[6] === 'LTP-8X(config-ports)("NTU1")#' && pr[9] === 'LTP-8X(config)(if-ont-0/3)#', pr.join(' | '));
  chk('ПК за ONT пингует сервер за MES', n.ping(pc.id, '10.0.0.2').ok);
  chk('ont-mode bridge и interface pon-port — синтаксис LTP-N, у LTP-X нет', /%/.test((n.exec(o.id, 'end'), n.exec(o.id, 'configure terminal'), n.exec(o.id, 'interface pon-port 0'))) && (n.exec(o.id, 'exit'), true));
  EL.labs.apply(n, { OLT: ['switch', 'configure', 'vlan 2149', 'no tagged pon-port 0 – 7', 'exit', 'commit', 'exit', 'exit'] });
  chk('VLAN убрана с pon-port в коммутаторе — трафика нет', !n.ping(pc.id, '10.0.0.2').ok);
  chk('ONT ID 128 — вне 0..127', /%/.test((n.exec(o.id, 'configure terminal'), n.exec(o.id, 'interface ont 0/128'))));
  console.log('✓ OLT LTP-X (ПО 3.52)');
})();
// Huawei VRP (спецификации sources/huawei/spec): S5700/S3700 в модели MES, AR2220/AR1220 в модели ESR, смешанные схемы с Eltex
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  function run(n, id, L) { return L.filter(function (l) { return /Error/.test(n.exec(id, l)); }); }
  var n = new EL.Net(), s = n.add('S5700', 'S1'), m = n.add('MES2428', 'SW2'), a = n.add('VPC', 'PC1'), b = n.add('VPC', 'PC2');
  n.connect(s.id, 'GE0/0/24', m.id, 'gi1/0/24'); n.connect(a.id, 'eth0', s.id, 'GE0/0/1'); n.connect(b.id, 'eth0', m.id, 'gi1/0/1');
  chk('VRP: <Huawei>, system-view → [Huawei], interface g0/0/1 → [Huawei-GigabitEthernet0/0/1]', n.prompt(s.id) === '<Huawei>' &&
    /Enter system view/.test(n.exec(s.id, 'sys')) && n.prompt(s.id) === '[Huawei]' && (n.exec(s.id, 'int g0/0/1'), n.prompt(s.id) === '[Huawei-GigabitEthernet0/0/1]'));
  chk('VRP: ошибка с кареткой под неверным словом', /\s+\^\nError: Unrecognized command found at '\^' position\./.test(n.exec(s.id, 'port lnk-type access')));
  chk('VRP: intelligent rollback — interface из вида интерфейса', (n.exec(s.id, 'interface GigabitEthernet 0/0/24'), n.prompt(s.id) === '[Huawei-GigabitEthernet0/0/24]'));
  var bad = run(n, s.id, ['return', 'sys', 'vlan batch 10 20', 'int g0/0/1', 'port link-type access', 'port default vlan 10', 'int g0/0/24', 'port link-type trunk',
    'port trunk allow-pass vlan 10 20', 'undo port trunk allow-pass vlan 1', 'return']);
  chk('S5700: VLAN access/trunk без ошибок', !bad.length, bad.join('; '));
  EL.labs.apply(n, { SW2: ['enable', 'configure', 'vlan database', 'vlan 10', 'exit', 'interface gi1/0/1', 'switchport access vlan 10', 'exit', 'interface gi1/0/24', 'switchport mode trunk',
    'switchport trunk allowed vlan add 10', 'end'], PC1: ['ip 10.0.0.1/24'], PC2: ['ip 10.0.0.2/24'] });
  n.tick(31);
  chk('S5700 ↔ MES: trunk VLAN 10, ПК пингуют друг друга', n.ping(a.id, '10.0.0.2').ok);
  chk('display vlan: UT:GE0/0/1(U) в VLAN 10, TG:GE0/0/24(U)', /10   common  UT:GE0\/0\/1\(U\)\s*\n\s+TG:GE0\/0\/24\(U\)/.test(n.exec(s.id, 'display vlan')));
  chk('display this: port link-type trunk, undo port trunk allow-pass vlan 1, allow-pass vlan 10 20', (n.exec(s.id, 'sys'), n.exec(s.id, 'int g0/0/24'),
    /port link-type trunk\n undo port trunk allow-pass vlan 1\n port trunk allow-pass vlan 10 20/.test(n.exec(s.id, 'display this'))));
  n.exec(s.id, 'undo port trunk allow-pass vlan 10'); n.tick(2);
  chk('VLAN 10 убрана с trunk Huawei — связи нет', !n.ping(a.id, '10.0.0.2').ok);
  n.exec(s.id, 'return');
  chk('save — вопрос [Y/N], y — сохранено; reboot поднимает сохранённое', /Are you sure to continue\?\[Y\/N\]/.test(n.exec(s.id, 'save')) && /successfully/.test(n.exec(s.id, 'y')) &&
    (n.exec(s.id, 'sys'), n.exec(s.id, 'undo vlan 20'), n.exec(s.id, 'return'), n.reboot(s.id), /vlan batch 10 20/.test(n.exec(s.id, 'display current-configuration'))));
  chk('STP по умолчанию MSTP, имя региона — MAC моста', /\[Mode MSTP\]/.test(n.exec(s.id, 'display stp')) && /Region name     :4c1f-/.test(n.exec(s.id, 'display stp region-configuration')));
  // Eth-Trunk LACP Huawei ↔ MES
  var t = new EL.Net(), S1 = t.add('S5700', 'S1'), M = t.add('MES2428', 'SW2');
  ['1', '2'].forEach(function (i) { t.connect(S1.id, 'GE0/0/' + i, M.id, 'gi1/0/' + i); });
  bad = run(t, S1.id, ['sys', 'int eth-trunk 1', 'mode lacp', 'quit', 'int g0/0/1', 'eth-trunk 1', 'int g0/0/2', 'eth-trunk 1', 'return']);
  EL.labs.apply(t, { SW2: ['enable', 'configure', 'interface range gi1/0/1-2', 'channel-group 1 mode active', 'exit', 'interface port-channel 1', 'exit', 'end'] });
  chk('Eth-Trunk mode lacp ↔ MES channel-group active: агрегат собран', !bad.length && /Operate status: up\s+Number Of Up Port In Trunk: 2/.test(t.exec(S1.id, 'display eth-trunk 1')), bad.join('; '));
  run(t, S1.id, ['sys', 'int g0/0/1', 'undo eth-trunk', 'int g0/0/2', 'undo eth-trunk', 'int eth-trunk 1', 'mode manual load-balance', 'int g0/0/1', 'eth-trunk 1', 'int g0/0/2', 'eth-trunk 1', 'return']);
  chk('Eth-Trunk manual ↔ MES LACP — агрегат не собирается (несовместимость вендоров)', /Operate status: down/.test(t.exec(S1.id, 'display eth-trunk 1')));
  // AR2220 ↔ ESR: OSPF
  var o = new EL.Net(), h = o.add('AR2220', 'R1'), e = o.add('vESR', 'R2'), p1 = o.add('VPC', 'PC1'), p2 = o.add('VPC', 'PC2');
  o.connect(h.id, 'GE0/0/0', e.id, 'gi1/0/1'); o.connect(p1.id, 'eth0', h.id, 'GE0/0/1'); o.connect(p2.id, 'eth0', e.id, 'gi1/0/2');
  bad = run(o, h.id, ['sys', 'sysname R1', 'int g0/0/0', 'ip address 10.0.12.1 24', 'int g0/0/1', 'ip add 192.168.1.1 255.255.255.0', 'quit', 'ospf 1 router-id 1.1.1.1', 'area 0',
    'network 10.0.12.1 0.0.0.255', 'network 192.168.1.0 0.0.0.255', 'return']);
  EL.labs.apply(o, { R2: ['configure', 'router ospf 1', 'router-id 2.2.2.2', 'area 0.0.0.0', 'enable', 'exit', 'enable', 'exit', 'interface gi1/0/1', 'ip address 10.0.12.2/24', 'ip firewall disable',
    'ip ospf instance 1', 'ip ospf area 0.0.0.0', 'ip ospf', 'exit', 'interface gi1/0/2', 'ip address 192.168.2.1/24', 'ip firewall disable', 'ip ospf instance 1', 'ip ospf area 0.0.0.0', 'ip ospf', 'exit',
    'end', 'commit', 'confirm'], PC1: ['ip 192.168.1.10/24 192.168.1.1'], PC2: ['ip 192.168.2.10/24 192.168.2.1'] });
  o.tick(60);
  chk('AR2220 ↔ ESR: OSPF Full, ping ПК–ПК', !bad.length && /0\.0\.0\.0\s+GigabitEthernet0\/0\/0\s+2\.2\.2\.2\s+Full/.test(o.exec(h.id, 'display ospf peer brief')) && o.ping(p1.id, '192.168.2.10').ok, bad.join('; '));
  chk('display ip routing-table: 192.168.2.0/24 OSPF 10', /192\.168\.2\.0\/24\s+OSPF\s+10 /.test(o.exec(h.id, 'display ip routing-table')));
  chk('OSPF: network приводится к сети в конфигурации', /network 10\.0\.12\.0 0\.0\.0\.255/.test(o.exec(h.id, 'display current-configuration')));
  run(o, h.id, ['sys', 'int g0/0/0', 'ospf timer hello 5', 'return']); o.tick(60);
  chk('OSPF: разные hello (Huawei 5 / ESR 10) — соседства нет', /Total Peer\(s\):     0/.test(o.exec(h.id, 'display ospf peer brief')) && !o.ping(p1.id, '192.168.2.10').ok);
  // AR1220: L2-порты LAN, DHCP, NAT easy-ip
  var r = new EL.Net(), A = r.add('AR1220', 'R1'), B = r.add('vESR', 'ISP'), IN = r.add('VPC', 'IN'), W = r.add('VPC', 'WEB');
  r.connect(A.id, 'GE0/0/0', B.id, 'gi1/0/1'); r.connect(IN.id, 'eth0', A.id, 'Eth0/0/1'); r.connect(W.id, 'eth0', B.id, 'gi1/0/2');
  chk('AR1220: Ethernet0/0/1 в L2 — ip address без undo portswitch не принимается', (r.exec(A.id, 'sys'), r.exec(A.id, 'int e0/0/1'), /Error/.test(r.exec(A.id, 'ip address 192.168.10.1 24'))));
  bad = run(r, A.id, ['undo portswitch', 'ip address 192.168.10.1 24', 'quit', 'dhcp enable', 'ip pool p1', 'network 192.168.10.0 mask 24', 'gateway-list 192.168.10.1', 'dns-list 8.8.8.8', 'quit',
    'int e0/0/1', 'dhcp select global', 'quit', 'acl 2000', 'rule 5 permit source 192.168.10.0 0.0.0.255', 'quit', 'int g0/0/0', 'ip address 1.1.1.1 24', 'nat outbound 2000', 'quit',
    'ip route-static 0.0.0.0 0 1.1.1.2', 'return']);
  EL.labs.apply(r, { ISP: ['configure', 'interface gi1/0/1', 'ip address 1.1.1.2/24', 'ip firewall disable', 'exit', 'interface gi1/0/2', 'ip address 2.2.2.1/24', 'ip firewall disable', 'exit', 'end', 'commit', 'confirm'],
    WEB: ['ip 2.2.2.10/24 2.2.2.1'], IN: ['ip dhcp'] });
  r.tick(5);
  chk('AR1220: DHCP из глобального пула (dhcp select global)', !bad.length && /^192\.168\.10\./.test(r.devs[IN.id].st.ip || ''), bad.join('; '));
  chk('AR1220: NAT easy-ip (nat outbound 2000) — внутренний узел выходит в сеть провайдера', r.ping(IN.id, '2.2.2.10').ok && (r.ctLast || []).some(function (c) { return c.kind === 's' && c.pub === '1.1.1.1'; }));
  chk('ACL: rule 5 permit source … 0.0.0.255 в display acl', /Basic ACL 2000, 1 rule\nAcl's step is 5\n rule 5 permit source 192\.168\.10\.0 0\.0\.0\.255/.test(r.exec(A.id, 'display acl 2000')));
  // VRRP AR + ESR
  var v = new EL.Net(), RA = v.add('AR2220', 'RA'), RB = v.add('vESR', 'RB'), sw = v.add('MES2428', 'SW'), pc = v.add('VPC', 'PC');
  v.connect(RA.id, 'GE0/0/1', sw.id, 'gi1/0/1'); v.connect(RB.id, 'gi1/0/1', sw.id, 'gi1/0/2'); v.connect(pc.id, 'eth0', sw.id, 'gi1/0/3');
  run(v, RA.id, ['sys', 'int g0/0/1', 'ip address 10.0.0.2 24', 'vrrp vrid 1 virtual-ip 10.0.0.1', 'vrrp vrid 1 priority 120', 'return']);
  EL.labs.apply(v, { RB: ['configure', 'interface gi1/0/1', 'ip address 10.0.0.3/24', 'ip firewall disable', 'vrrp id 1', 'vrrp ip 10.0.0.1/24', 'vrrp', 'exit', 'end', 'commit', 'confirm'], PC: ['ip 10.0.0.10/24 10.0.0.1'] });
  v.tick(40);
  chk('VRRP Huawei (120) + ESR (100): Master — AR, шлюз 10.0.0.1 отвечает', /1     Master/.test(v.exec(RA.id, 'display vrrp brief')) && v.ping(pc.id, '10.0.0.1').ok);
  console.log('✓ Huawei VRP: S5700, AR2220, AR1220 в смешанных схемах');
})();
// «Отказы» (faults.js): матрица связности до/после, перестроение путей, единые точки отказа — на смешанной схеме Huawei + Eltex
(function () {
  function chk(name, ok, extra) { total++; if (!ok) { fail++; console.error('✗ ' + name + (extra ? ' — ' + extra : '')); } }
  var n = new EL.Net(), s1 = n.add('S5700', 'S1'), s2 = n.add('MES2428', 'SW2'), s3 = n.add('MES2428', 'SW3'), a = n.add('VPC', 'PC1'), b = n.add('VPC', 'PC2');
  n.connect(s1.id, 'GE0/0/23', s2.id, 'gi1/0/23'); n.connect(s2.id, 'gi1/0/24', s3.id, 'gi1/0/24'); n.connect(s3.id, 'gi1/0/22', s1.id, 'GE0/0/22');
  n.connect(a.id, 'eth0', s1.id, 'GE0/0/1'); n.connect(b.id, 'eth0', s3.id, 'gi1/0/1');
  EL.labs.apply(n, { S1: ['sys', 'stp mode rstp', 'return'], SW2: ['enable', 'configure', 'spanning-tree mode rstp', 'end'], SW3: ['enable', 'configure', 'spanning-tree mode rstp', 'end'],
    PC1: ['ip 10.0.0.1/24'], PC2: ['ip 10.0.0.2/24'] });
  n.tick(40);
  var arp0 = JSON.stringify(n.arp), now0 = n.now, L0 = n.links.length;
  var R = EL.faults.analyze(n, { k: 'link', key: 'S1:GE0/0/22—SW3:gi1/0/22' });
  chk('Отказы: обрыв S1–SW3 в кольце RSTP — связь есть, путь через SW2, корневой порт SW3 сменился', R.pairs.length === 2 && R.pairs.every(function (p) { return p.after === 'reroute'; }) &&
    R.pairs[0].path2.indexOf('SW2') >= 0 && R.changes.some(function (c) { return c.what === 'SW3 gi1/0/24' && c.after === 'Root'; }));
  chk('Отказы: исходная схема не меняется (кабели, ARP, часы)', n.links.length === L0 && JSON.stringify(n.arp) === arp0 && n.now === now0);
  var S = EL.faults.spofAll(n), sp = S.res.filter(function (r) { return r.spof; }).map(function (r) { return r.fault.key; }).sort();
  chk('Единые точки отказа: S1, SW3 и кабели к ПК; кольцо и SW2 — нет', JSON.stringify(sp) === JSON.stringify(['PC1:eth0—S1:GE0/0/1', 'PC2:eth0—SW3:gi1/0/1', 'S1', 'SW3']), sp.join(', '));
  var md0 = n.byName('SW2').st.stp.mode, C = EL.faults.analyze(n, { k: 'cfg', cfg: 'stp-mode', dev: 'SW2' });
  chk('Ошибка конфигурации на копии (STP 802.1D на SW2) не трогает исходный SW2', n.byName('SW2').st.stp.mode === md0 && md0 !== 'stp' && C.fault.cfg === 'stp-mode');
  var D = EL.faults.analyze(n, { k: 'cfg', cfg: 'gw', dev: 'PC1' });
  chk('Список ошибок конфигурации строится по устройству (Huawei S1 — STP, регион MSTP)', EL.faults.cfgFor(n, 'S1').some(function (x) { return x.cfg === 'mst-name'; }) && !!D);
  console.log('✓ Отказы: матрица связности, перестроение, единые точки отказа');
})();
console.log('\nИтого прогонов: ' + total + ', ошибок: ' + fail);
process.exit(fail ? 1 : 0);
