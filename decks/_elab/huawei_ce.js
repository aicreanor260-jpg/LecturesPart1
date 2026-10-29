/* Коммутаторы Huawei CloudEngine (VRP8) — спецификация sources/huawei/spec/ce.md (CloudEngine 9800/8800/6800/5800 V200R024C10).
   Диалект huawei.js / huawei_s.js: двухэтапная конфигурация — команды меняют кандидат, в сеть попадает только после commit
   (BC j005): приглашение [~HUAWEI] — изменений нет, [*HUAWEI] — есть незакоммиченные; новое имя (sysname) — после commit;
   порты 10GE1/0/N и 100GE1/0/N (IM j003), тип порта по умолчанию access (ES j03y), ошибки VRP8 «Error: Incomplete command found at '^' position.» (CR j00a).
   Упрощения (в отчёте): вход без задания пароля консоли (на CE при первом входе его требуют задать), system-view immediately и стек/M-LAG не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, Vr = EL.vrp, P = EL.Net.prototype;
  function range(pre, a, b) { var o = []; for (var i = a; i <= b; i++) o.push(pre + i); return o; }
  EL.MODELS['CE6881-48S6CQ'] = { type: 'mes', kind: 'hw-s', ce: true, portList: range('10GE1/0/', 1, 48).concat(range('100GE1/0/', 1, 6)), ports: 54, group: 'Huawei (как в eNSP)', vendor: 'huawei', host: 'HUAWEI',
    note: 'Коммутатор Huawei CloudEngine CE6881-48S6CQ (VRP8): 48 × 10GE1/0/1–48 + 6 × 100GE1/0/1–6, конфигурация применяется командой commit', login: [{ u: '—', p: '—', a: 'консоль (на устройстве при первом входе задают пароль)' }] };
  function CE(st) { return !!st.vrp && !!st.vrp.ce; }
  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}; if (!m.ce) return d;
    var x = d.st.vrp; x.ce = true; x.run = EL.clone(x.c); Vr.compile(d.st); return d; };
  var c1 = Vr.cmd('*', 'commit', function (st) { var x = st.vrp; if (!CE(st)) return null; x.run = EL.clone(x.c); Vr.compile(st); }, 'Commit configuration');
  c1.ok = CE; c1.cfg = false;
  var c2 = Vr.cmd('*', 'display configuration candidate', function (st) { var x = st.vrp, r0 = x.run; x.run = x.c; try { return Vr.cfgText(st); } finally { x.run = r0; } });
  c2.ok = CE; c2.cfg = false;
  var c3 = Vr.cmd('*', 'clear configuration candidate', function (st) { st.vrp.c = EL.clone(st.vrp.run); });
  c3.ok = CE; c3.cfg = false;
  // save — действующая (закоммиченная) конфигурация
  Vr.T.forEach(function (e) { if (e.p.join(' ') === 'save') { var r0 = e.run; e.run = function (st) { var out = r0.apply(this, arguments), x = st.vrp; if (!CE(st) || !x.ask) return out;
    var y = x.ask.yes; x.ask.yes = function () { var r = y(); x.saved = EL.clone(x.run); return r; }; return out; }; } });
  var rb0 = P.reboot;
  P.reboot = function (id) { var r = rb0.apply(this, arguments), d = this.devs[id]; if (d && d.st.vrp && d.st.vrp.ce) { d.st.vrp.run = EL.clone(d.st.vrp.c); Vr.compile(d.st); } return r; };
})(typeof window !== 'undefined' ? window : global);
