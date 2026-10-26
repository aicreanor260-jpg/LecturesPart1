/* Симулятор CLI маршрутизатора Eltex ESR для тренажёра деки «Протокол OSPF» (по pptx «OSPF 2 5»).
   Режимы и приглашения как в pptx: esr# → config → esr(config)# → router ospf N → esr(config-ospf)# →
   area A → esr(config-ospf-area)#; interface gigabitethernet 1/0/N → esr(config-if-gi)#.
   Задания случайные, проверяется итоговое состояние; «Отправить Hello» — установится ли соседство с соседом. */
(function () {
  'use strict';
  var NPORTS = 8;

  function fresh() {
    var ifs = {};
    for (var i = 1; i <= NPORTS; i++) ifs['gi1/0/' + i] = { ip: null, inst: null, area: null, ospf: false, net: 'broadcast',
      md5: false, key: null, cost: null, prio: null, hello: null, dead: null, mtuIgn: false };
    return { host: 'esr', mode: 'priv', ctx: null, ospf: {}, ifs: ifs, log: false, dirty: false, committed: false, confirmed: false };
  }
  var PROMPT = { priv: '#', config: '(config)#', ospf: '(config-ospf)#', area: '(config-ospf-area)#', 'if': '(config-if-gi)#' };
  function prompt(st) { return st.host + PROMPT[st.mode]; }
  function isIp(t) { return /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/.test(t) && t.split('.').every(function (o) { return +o <= 255; }); }

  var CMDS = [];
  function cmd(modes, pat, run) { CMDS.push({ modes: modes.split(' '), pat: pat.split(' '), run: run }); }
  var ANY = 'priv config ospf area if', CFG = 'config ospf area if';

  function match(pat, toks) {
    var args = [], i = 0;
    for (var k = 0; k < pat.length; k++) {
      var p = pat[k], t = toks[i];
      if (t === undefined) return null;
      if (p === '<n>') { if (!/^\d+$/.test(t)) return null; args.push(+t); i++; continue; }
      if (p === '<w>') { args.push(t); i++; continue; }
      if (p === '<ip>') { if (!isIp(t)) return null; args.push(t); i++; continue; }
      if (p === '<pfx>') { var m = t.match(/^(\d+\.\d+\.\d+\.\d+)\/(\d{1,2})$/); if (!m || !isIp(m[1]) || +m[2] > 32) return null; args.push(t); i++; continue; }
      if (p === '<if>') { var g = t.match(/^gi1\/0\/(\d+)$/); if (!g || +g[1] < 1 || +g[1] > NPORTS) return null; args.push('gi1/0/' + g[1]); i++; continue; }
      if (t === p || (t.length >= 2 && p.indexOf(t) === 0)) { i++; continue; }
      return null;
    }
    return i === toks.length ? args : null;
  }
  function chg(st) { st.dirty = true; st.committed = false; st.confirmed = false; }
  function proc(st) { return st.ospf[st.ctx.pid]; }

  // --- режимы
  cmd('priv', 'configure', function (st) { st.mode = 'config'; });
  cmd('priv', 'config', function (st) { st.mode = 'config'; });
  cmd('config', 'exit', function (st) { st.mode = 'priv'; st.ctx = null; });
  cmd('ospf', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  cmd('area', 'exit', function (st) { st.mode = 'ospf'; st.ctx = { pid: st.ctx.pid }; });
  cmd('if', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  cmd(CFG, 'end', function (st) { st.mode = 'priv'; st.ctx = null; });
  cmd('priv', 'exit', function () { return '% Сессия остаётся открытой (тренажёр)'; });
  cmd(ANY, 'commit', function (st) { if (!st.dirty) return 'Nothing to commit'; st.committed = true;
    return 'Configuration has been successfully applied and saved to flash. Commit timer started, changes will be reverted in 600 seconds.'; });
  cmd(ANY, 'confirm', function (st) { if (!st.committed) return '% Нет изменений, ожидающих подтверждения — сначала commit';
    st.confirmed = true; st.dirty = false; return 'Configuration has been confirmed. Commit timer canceled.'; });

  // --- процесс OSPF
  cmd('config', 'router ospf log-adjacency-changes', function (st) { st.log = true; chg(st); });
  cmd('config', 'router ospf <n>', function (st, a) {
    if (a[0] < 1 || a[0] > 65535) return '% Номер процесса 1–65535';
    if (!st.ospf[a[0]]) st.ospf[a[0]] = { rid: null, enabled: false, areas: {}, areaOrder: [], redist: [], pref: null, maxp: null, opaqueOff: false };
    st.mode = 'ospf'; st.ctx = { pid: a[0] }; chg(st); });
  cmd('config', 'no router ospf <n>', function (st, a) { if (!st.ospf[a[0]]) return '% Процесс не найден'; delete st.ospf[a[0]]; chg(st); });
  cmd('ospf', 'router-id <ip>', function (st, a) { proc(st).rid = a[0]; chg(st); });
  cmd('ospf', 'area <ip>', function (st, a) {
    var P = proc(st); if (!P.areas[a[0]]) { P.areas[a[0]] = { enabled: false, type: 'normal', nosum: false, nets: [] }; P.areaOrder.push(a[0]); }
    st.mode = 'area'; st.ctx = { pid: st.ctx.pid, area: a[0] }; chg(st); });
  cmd('ospf', 'enable', function (st) {
    var P = proc(st), any = P.areaOrder.some(function (k) { return P.areas[k].enabled; });
    if (!any) return '% Пока ни одна area не активирована, OSPF процесс активировать невозможно';
    P.enabled = true; chg(st); });
  cmd('ospf', 'no enable', function (st) { proc(st).enabled = false; chg(st); });
  ['connected', 'static', 'rip', 'ospf', 'bgp', 'isis'].forEach(function (r) {
    cmd('ospf', 'redistribute ' + r, function (st) { var P = proc(st); if (P.redist.indexOf(r) < 0) P.redist.push(r); chg(st); });
  });
  cmd('ospf', 'preference <n>', function (st, a) { if (a[0] < 1 || a[0] > 255) return '% Значение 1–255'; proc(st).pref = a[0]; chg(st); });
  cmd('ospf', 'opaque-lsa disable', function (st) { proc(st).opaqueOff = true; chg(st); });
  cmd('ospf', 'no opaque-lsa disable', function (st) { proc(st).opaqueOff = false; chg(st); });
  cmd('ospf', 'maximum-paths <n>', function (st, a) { if (a[0] < 1 || a[0] > 32) return '% Значение 1–32'; proc(st).maxp = a[0]; chg(st); });

  // --- область
  function ar(st) { return st.ospf[st.ctx.pid].areas[st.ctx.area]; }
  cmd('area', 'enable', function (st) { ar(st).enabled = true; chg(st); });
  cmd('area', 'no enable', function (st) { ar(st).enabled = false; chg(st); });
  cmd('area', 'area-type normal', function (st) { if (st.ctx.area === '0.0.0.0') return '% Backbone area не может быть stub/nssa';
    ar(st).type = 'normal'; ar(st).nosum = false; chg(st); });
  cmd('area', 'area-type stub', function (st) { if (st.ctx.area === '0.0.0.0') return '% Backbone area не может быть stub/nssa';
    ar(st).type = 'stub'; ar(st).nosum = false; chg(st); });
  cmd('area', 'area-type stub no-summary', function (st) { if (st.ctx.area === '0.0.0.0') return '% Backbone area не может быть stub/nssa';
    ar(st).type = 'stub'; ar(st).nosum = true; chg(st); });
  cmd('area', 'area-type nssa', function (st) { if (st.ctx.area === '0.0.0.0') return '% Backbone area не может быть stub/nssa';
    ar(st).type = 'nssa'; ar(st).nosum = false; chg(st); });
  cmd('area', 'area-type nssa no-summary', function (st) { if (st.ctx.area === '0.0.0.0') return '% Backbone area не может быть stub/nssa';
    ar(st).type = 'nssa'; ar(st).nosum = true; chg(st); });
  cmd('area', 'network <pfx>', function (st, a) { var A = ar(st); if (A.nets.indexOf(a[0]) < 0) A.nets.push(a[0]); chg(st); });

  // --- интерфейс
  cmd('config', 'interface <if>', function (st, a) { st.mode = 'if'; st.ctx = { ifn: a[0] }; });
  function I(st) { return st.ifs[st.ctx.ifn]; }
  cmd('if', 'ip address <pfx>', function (st, a) { I(st).ip = a[0]; chg(st); });
  cmd('if', 'ip ospf instance <n>', function (st, a) { if (!st.ospf[a[0]]) return '% OSPF процесс ' + a[0] + ' не создан';
    I(st).inst = a[0]; chg(st); });
  cmd('if', 'ip ospf area <ip>', function (st, a) { I(st).area = a[0]; chg(st); });
  cmd('if', 'ip ospf', function (st) { var i = I(st); if (!i.area) i.area = '0.0.0.0'; i.ospf = true; chg(st); });
  cmd('if', 'no ip ospf', function (st) { I(st).ospf = false; chg(st); });
  [['broadcast', 'broadcast'], ['non-broadcast', 'non-broadcast'], ['point-to-multipoint', 'point-to-multipoint'],
   ['point-to-point', 'point-to-point']].forEach(function (n) {
    cmd('if', 'ip ospf network ' + n[0], function (st) { I(st).net = n[1]; chg(st); });
  });
  cmd('if', 'ip ospf authentication algorithm md5', function (st) { I(st).md5 = true; chg(st); });
  cmd('if', 'ip ospf authentication key ascii-text <w>', function (st, a) {
    if (a[0].length < 8 || a[0].length > 16) return '% Ключ задаётся длиной от 8 до 16 символов'; I(st).key = a[0]; chg(st); });
  cmd('if', 'ip ospf cost <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return '% Значение 1–65535'; I(st).cost = a[0]; chg(st); });
  cmd('if', 'ip ospf priority <n>', function (st, a) { if (a[0] > 255) return '% Значение 0–255'; I(st).prio = a[0]; chg(st); });
  cmd('if', 'ip ospf hello-interval <n>', function (st, a) { if (a[0] < 1 || a[0] > 255) return '% Значение 1–255'; I(st).hello = a[0]; chg(st); });
  cmd('if', 'ip ospf dead-interval <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return '% Значение 1–65535'; I(st).dead = a[0]; chg(st); });
  cmd('if', 'ip ospf mtu-ignore', function (st) { I(st).mtuIgn = true; chg(st); });

  // --- show
  function showRun(st) {
    var o = [];
    if (st.log) o.push('router ospf log-adjacency-changes');
    Object.keys(st.ospf).forEach(function (pid) {
      var P = st.ospf[pid]; o.push('router ospf ' + pid);
      if (P.rid) o.push('  router-id ' + P.rid);
      if (P.pref) o.push('  preference ' + P.pref);
      if (P.maxp) o.push('  maximum-paths ' + P.maxp);
      if (P.opaqueOff) o.push('  opaque-lsa disable');
      P.redist.forEach(function (r) { o.push('  redistribute ' + r); });
      P.areaOrder.forEach(function (k) {
        var A = P.areas[k]; o.push('  area ' + k);
        if (A.type !== 'normal') o.push('    area-type ' + A.type + (A.nosum ? ' no-summary' : ''));
        A.nets.forEach(function (n) { o.push('    network ' + n); });
        if (A.enabled) o.push('    enable');
        o.push('  exit');
      });
      if (P.enabled) o.push('  enable');
      o.push('exit');
    });
    Object.keys(st.ifs).forEach(function (k) {
      var i = st.ifs[k], d = [];
      if (i.ip) d.push('  ip address ' + i.ip);
      if (i.inst) d.push('  ip ospf instance ' + i.inst);
      if (i.net !== 'broadcast') d.push('  ip ospf network ' + i.net);
      if (i.area && (i.ospf || i.inst)) d.push('  ip ospf area ' + i.area);
      if (i.md5) d.push('  ip ospf authentication algorithm md5');
      if (i.key) d.push('  ip ospf authentication key ascii-text encrypted ' + i.key.replace(/./g, '*'));
      if (i.cost) d.push('  ip ospf cost ' + i.cost);
      if (i.prio !== null) d.push('  ip ospf priority ' + i.prio);
      if (i.hello) d.push('  ip ospf hello-interval ' + i.hello);
      if (i.dead) d.push('  ip ospf dead-interval ' + i.dead);
      if (i.mtuIgn) d.push('  ip ospf mtu-ignore');
      if (i.ospf) d.push('  ip ospf');
      if (d.length) { o.push('interface gigabitethernet ' + k.slice(2)); o.push.apply(o, d); o.push('exit'); }
    });
    return o.length ? o.join('\n') : '';
  }
  ['', 'do '].forEach(function (pre) {
    var m = pre ? CFG : 'priv';
    cmd(m, pre + 'show running-config routing ospf', function (st) { return showRun(st); });
    cmd(m, pre + 'show running-config', function (st) { return showRun(st); });
    cmd(m, pre + 'show ip ospf neighbors', function () { return 'Нажмите «Отправить Hello» — тренажёр покажет, установится ли соседство.'; });
  });

  function normLine(s) { return s.replace(/\b(?:g|gi|gig|giga|gigabit|gigabitethernet)\s*(?=\d+\/\d+\/\d+)/ig, 'gi'); }
  function exec(st, raw) {
    var line = normLine(raw.trim()); if (!line) return '';
    var toks = line.split(/\s+/), low = toks.map(function (t) { return t.toLowerCase(); });
    for (var i = 0; i < CMDS.length; i++) {
      var c = CMDS[i]; if (c.modes.indexOf(st.mode) < 0) continue;
      var args = match(c.pat, low);
      if (args) {
        var orig = match(c.pat, toks.map(function (t, j) { return c.pat[j] === '<w>' ? t : low[j]; }));
        return c.run(st, orig || args) || '';
      }
    }
    var other = CMDS.some(function (c) { return match(c.pat, low); });
    return other ? '% Команда недоступна в этом режиме — проверьте приглашение' : '% Unrecognized command';
  }

  // ------------------------------------------------------------------ задания
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  function rid() { var n = rnd(1, 9); return n + '.' + n + '.' + n + '.' + n; }
  function area() { return pick(['0.0.0.0', '0.0.0.1', '0.0.0.2', '1.1.1.1', '8.0.0.0']); }
  function areaNB() { return pick(['0.0.0.1', '0.0.0.2', '0.0.0.5', '1.1.1.1', '8.0.0.0']); }
  function okAll(st) { return st.confirmed; }
  function procOk(s, p) { var P = s.ospf[p.pid]; return P && P.rid === p.rid && P.areas[p.a] && P.areas[p.a].enabled && P.enabled; }
  function ifOk(s, p) { var i = s.ifs['gi1/0/' + p.g]; return i.inst === p.pid && i.area === p.a && i.ospf; }
  function setupProc(s, p) { s.ospf[p.pid] = { rid: p.rid, enabled: true, areas: {}, areaOrder: [p.a], redist: [], pref: null, maxp: null, opaqueOff: false };
    s.ospf[p.pid].areas[p.a] = { enabled: true, type: 'normal', nosum: false, nets: [] }; }
  function ifLines(p, extra) { return ['interface gigabitethernet 1/0/' + p.g, 'ip ospf instance ' + p.pid, 'ip ospf area ' + p.a]
    .concat(extra || []).concat(['ip ospf', 'exit']); }
  function procLines(p, areaExtra) { return ['router ospf ' + p.pid, 'router-id ' + p.rid, 'area ' + p.a].concat(areaExtra || [])
    .concat(['enable', 'exit', 'enable', 'exit']); }

  // сосед: проверка условий из pptx (сл. 84): маски/сеть, таймеры, тип сети, commit/confirm, enable, аутентификация
  function hello(s, p, nb) {
    var i = s.ifs['gi1/0/' + p.g], P = s.ospf[i.inst], r = [];
    function add(ok, t) { r.push({ ok: ok, t: t }); }
    if (!P) { add(false, 'Hello не отправлен: интерфейс не привязан к процессу OSPF (ip ospf instance)'); return r; }
    if (!i.ospf) { add(false, 'Hello не отправлен: OSPF на интерфейсе не включён (ip ospf)'); return r; }
    if (!P.areas[i.area] || !P.areas[i.area].enabled || !P.enabled) { add(false, 'Hello не отправлен: забыли применить enable (область или процесс)'); return r; }
    if (!s.confirmed) { add(false, 'Hello не отправлен: забыли применить и подтвердить конфигурацию (commit/confirm)'); return r; }
    add(true, 'Hello отправлен с gi1/0/' + p.g + ' на 224.0.0.5, router-id ' + (P.rid || '—') + ', area ' + i.area);
    var h = i.hello || (i.net === 'non-broadcast' ? 30 : 10), d = i.dead || (i.net === 'non-broadcast' ? 120 : 40);
    var bad = [];
    if (i.area !== nb.area) bad.push('номер области не совпадает (' + i.area + ' ≠ ' + nb.area + ')');
    if (h !== nb.hello || d !== nb.dead) bad.push('таймеры приветствия или смерти не совпадают (' + h + '/' + d + ' ≠ ' + nb.hello + '/' + nb.dead + ')');
    if (i.net !== nb.net) bad.push('типы сети OSPF не совпадают (' + i.net + ' ≠ ' + nb.net + ')');
    if (!!i.md5 !== !!nb.key || (nb.key && i.key !== nb.key)) bad.push('пароль аутентификации не совпадает');
    if (P.areas[i.area] && P.areas[i.area].type !== (nb.type || 'normal')) bad.push('тип области не совпадает');
    if (bad.length) { bad.forEach(function (b) { add(false, 'Соседство не установится: ' + b); }); return r; }
    add(true, 'Hello от соседа ' + nb.rid + ' принят: Init → 2-Way → ExStart → Exchange → Loading → Full');
    return r;
  }

  var TASKS = [
    // 0. создание процесса (сл. 75)
    { gen: function () { return { pid: rnd(1, 999), rid: rid(), a: area() }; },
      text: function (p) { return 'Создайте процесс OSPF <b>' + p.pid + '</b>, задайте router-id <b>' + p.rid + '</b>, создайте и включите область <b>' +
        p.a + '</b>, затем включите процесс. Примените и подтвердите конфигурацию.'; },
      sol: function (p) { return ['config'].concat(procLines(p)).concat(['commit', 'confirm']); },
      checks: function (p) { return [['Процесс ' + p.pid + ' с router-id ' + p.rid, function (s) { return s.ospf[p.pid] && s.ospf[p.pid].rid === p.rid; }],
        ['Область ' + p.a + ' создана и включена (enable)', function (s) { var P = s.ospf[p.pid]; return P && P.areas[p.a] && P.areas[p.a].enabled; }],
        ['Процесс включён (enable)', function (s) { return s.ospf[p.pid] && s.ospf[p.pid].enabled; }],
        ['commit и confirm', okAll]]; } },
    // 1. включение на интерфейсе (сл. 77)
    { gen: function () { return { pid: rnd(1, 999), rid: rid(), a: area(), g: rnd(1, NPORTS) }; },
      setup: function (p, s) { setupProc(s, p); s.dirty = false; },
      text: function (p) { return 'Процесс OSPF <b>' + p.pid + '</b> с областью <b>' + p.a + '</b> уже создан. Включите OSPF на интерфейсе <b>gi1/0/' + p.g +
        '</b>: привяжите процесс, укажите область, активируйте OSPF. Примените и подтвердите.'; },
      sol: function (p) { return ['config'].concat(ifLines(p)).concat(['commit', 'confirm']); },
      checks: function (p) { var k = 'gi1/0/' + p.g; return [['ip ospf instance ' + p.pid, function (s) { return s.ifs[k].inst === p.pid; }],
        ['ip ospf area ' + p.a, function (s) { return s.ifs[k].area === p.a; }],
        ['ip ospf', function (s) { return s.ifs[k].ospf; }], ['commit и confirm', okAll]]; },
      send: function (p, s) { return hello(s, p, { rid: '2.2.2.2', area: p.a, hello: 10, dead: 40, net: 'broadcast' }); } },
    // 2. минимальная конфигурация point-to-point (сл. 78)
    { gen: function () { var n = rnd(1, 2); return { pid: 100, rid: n + '.' + n + '.' + n + '.' + n, nr: (3 - n) + '.' + (3 - n) + '.' + (3 - n) + '.' + (3 - n), a: '8.0.0.0', g: 1, me: 'ESR-' + n }; },
      text: function (p) { return 'Вы — <b>' + p.me + '</b>. Как в примере pptx: процесс <b>' + p.pid + '</b>, router-id <b>' + p.rid + '</b>, область <b>' + p.a +
        '</b>; на <b>gi1/0/' + p.g + '</b> — instance, тип сети <b>point-to-point</b>, area и ip ospf. Сосед уже настроен так же (router-id ' + p.nr + ').'; },
      sol: function (p) { return ['config'].concat(procLines(p)).concat(ifLines(p, ['ip ospf network point-to-point'])).concat(['commit', 'confirm']); },
      checks: function (p) { return [['Процесс, router-id, область ' + p.a + ' включены', function (s) { return procOk(s, p); }],
        ['gi1/0/1: instance ' + p.pid + ', area ' + p.a + ', ip ospf', function (s) { return ifOk(s, p); }],
        ['gi1/0/1: ip ospf network point-to-point', function (s) { return s.ifs['gi1/0/1'].net === 'point-to-point'; }],
        ['commit и confirm', okAll]]; },
      send: function (p, s) { return hello(s, p, { rid: p.nr, area: p.a, hello: 10, dead: 40, net: 'point-to-point' }); } },
    // 3. тип области (сл. 76)
    { gen: function () { var t = pick([['stub', false, 'Stub'], ['nssa', false, 'NSSA'], ['nssa', true, 'Totally NSSA']]);
        return { pid: rnd(1, 999), rid: rid(), a: areaNB(), t: t[0], ns: t[1], name: t[2] }; },
      text: function (p) { return 'Создайте процесс <b>' + p.pid + '</b> (router-id <b>' + p.rid + '</b>) и область <b>' + p.a + '</b> типа <b>' + p.name +
        '</b> командой area-type. Включите область и процесс, примените и подтвердите.'; },
      sol: function (p) { return ['config'].concat(procLines(p, ['area-type ' + p.t + (p.ns ? ' no-summary' : '')])).concat(['commit', 'confirm']); },
      checks: function (p) { return [['Процесс включён, область ' + p.a + ' включена', function (s) { return procOk(s, p); }],
        ['area-type ' + p.t + (p.ns ? ' no-summary' : ''), function (s) { var A = s.ospf[p.pid] && s.ospf[p.pid].areas[p.a];
          return A && A.type === p.t && A.nosum === p.ns; }], ['commit и confirm', okAll]]; } },
    // 4. аутентификация md5 (сл. 79)
    { gen: function () { return { pid: rnd(1, 999), rid: rid(), a: area(), g: rnd(1, NPORTS), key: pick(['ELTEXPAS', 'ospfkey77', 'Secret2025', 'net0spf!']) }; },
      setup: function (p, s) { setupProc(s, p); var i = s.ifs['gi1/0/' + p.g]; i.inst = p.pid; i.area = p.a; i.ospf = true; s.dirty = false; s.confirmed = true; },
      text: function (p) { return 'На <b>gi1/0/' + p.g + '</b> OSPF уже включён. Сосед требует аутентификацию <b>md5</b> с ключом <b>' + p.key +
        '</b>. Настройте её на интерфейсе, примените и подтвердите.'; },
      sol: function (p) { return ['config', 'interface gigabitethernet 1/0/' + p.g, 'ip ospf authentication algorithm md5',
        'ip ospf authentication key ascii-text ' + p.key, 'exit', 'commit', 'confirm']; },
      checks: function (p) { var k = 'gi1/0/' + p.g; return [['ip ospf authentication algorithm md5', function (s) { return s.ifs[k].md5; }],
        ['ключ ' + p.key, function (s) { return s.ifs[k].key === p.key; }], ['commit и confirm', okAll]]; },
      send: function (p, s) { return hello(s, p, { rid: '2.2.2.2', area: p.a, hello: 10, dead: 40, net: 'broadcast', key: p.key }); } },
    // 5. таймеры (сл. 83)
    { gen: function () { var h = pick([5, 15, 20, 30]); return { pid: rnd(1, 999), rid: rid(), a: area(), g: rnd(1, NPORTS), h: h, d: h * 4 }; },
      setup: function (p, s) { setupProc(s, p); var i = s.ifs['gi1/0/' + p.g]; i.inst = p.pid; i.area = p.a; i.ospf = true; s.dirty = false; s.confirmed = true; },
      text: function (p) { return 'Сосед за <b>gi1/0/' + p.g + '</b> — маршрутизатор другого вендора с HELLO-интервалом <b>' + p.h +
        '</b> с. Согласуйте таймеры по правилу «DEAD = 4 × HELLO», примените и подтвердите.'; },
      sol: function (p) { return ['config', 'interface gigabitethernet 1/0/' + p.g, 'ip ospf hello-interval ' + p.h, 'ip ospf dead-interval ' + p.d, 'exit', 'commit', 'confirm']; },
      checks: function (p) { var k = 'gi1/0/' + p.g; return [['ip ospf hello-interval ' + p.h, function (s) { return s.ifs[k].hello === p.h; }],
        ['ip ospf dead-interval ' + p.d, function (s) { return s.ifs[k].dead === p.d; }], ['commit и confirm', okAll]]; },
      send: function (p, s) { return hello(s, p, { rid: '2.2.2.2', area: p.a, hello: p.h, dead: p.d, net: 'broadcast' }); } },
    // 6. приоритет и стоимость (сл. 79)
    { gen: function () { return { pid: rnd(1, 999), rid: rid(), a: area(), g: rnd(1, NPORTS), pr: pick([0, 0, 200, 255]), c: pick([5, 10, 20, 64]) }; },
      setup: function (p, s) { setupProc(s, p); var i = s.ifs['gi1/0/' + p.g]; i.inst = p.pid; i.area = p.a; i.ospf = true; s.dirty = false; s.confirmed = true; },
      text: function (p) { return 'На <b>gi1/0/' + p.g + '</b> задайте стоимость канала <b>' + p.c + '</b> и приоритет <b>' + p.pr + '</b>' +
        (p.pr === 0 ? ' — маршрутизатор не должен участвовать в выборе DR' : ' — чтобы чаще становиться DR') + '. Примените и подтвердите.'; },
      sol: function (p) { return ['config', 'interface gigabitethernet 1/0/' + p.g, 'ip ospf cost ' + p.c, 'ip ospf priority ' + p.pr, 'exit', 'commit', 'confirm']; },
      checks: function (p) { var k = 'gi1/0/' + p.g; return [['ip ospf cost ' + p.c, function (s) { return s.ifs[k].cost === p.c; }],
        ['ip ospf priority ' + p.pr, function (s) { return s.ifs[k].prio === p.pr; }], ['commit и confirm', okAll]]; } },
    // 7. объявление сетей (сл. 81–82)
    { gen: function () { return { pid: 777, rid: '7.7.7.7', a: '0.0.0.0', net: pick(['203.0.113.0/24', '198.51.100.0/24', '192.168.10.0/24']) }; },
      text: function (p) { return 'Как в примере pptx: процесс <b>' + p.pid + '</b>, router-id <b>' + p.rid + '</b>, в области <b>' + p.a +
        '</b> объявите сеть <b>' + p.net + '</b> командой network, включите область; в процессе включите <b>redistribute connected</b> и сам процесс. Примените и подтвердите.'; },
      sol: function (p) { return ['config', 'router ospf ' + p.pid, 'router-id ' + p.rid, 'area ' + p.a, 'network ' + p.net, 'enable', 'exit',
        'redistribute connected', 'enable', 'exit', 'commit', 'confirm']; },
      checks: function (p) { return [['network ' + p.net + ' в area ' + p.a, function (s) { var P = s.ospf[p.pid]; return P && P.areas[p.a] && P.areas[p.a].nets.indexOf(p.net) >= 0; }],
        ['Процесс, router-id, область включены', function (s) { return procOk(s, p); }],
        ['redistribute connected', function (s) { return s.ospf[p.pid] && s.ospf[p.pid].redist.indexOf('connected') >= 0; }],
        ['commit и confirm', okAll]]; } }
  ];

  // ------------------------------------------------------------------ виджет
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function init(box) {
    var pool = (box.dataset.pool || '').split(',').map(Number);
    var out = box.querySelector('.cs-out'), inp = box.querySelector('.cs-in input'), pr = box.querySelector('.cs-pr');
    var taskEl = box.querySelector('.cs-task'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol');
    var sendB = box.querySelector('[data-cs=send]');
    var st, T, P, hist = [], hi = 0, last = -1;
    function print(t, cls) { var d = document.createElement('div'); d.className = cls || ''; d.innerHTML = esc(t); out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function newTask() {
      var k; do { k = pool[rnd(0, pool.length - 1)]; } while (pool.length > 1 && k === last); last = k;
      T = TASKS[k]; P = T.gen(); st = fresh(); if (T.setup) T.setup(P, st);
      taskEl.innerHTML = T.text(P); res.innerHTML = ''; sol.style.display = 'none'; sol.textContent = T.sol(P).join('\n');
      out.innerHTML = ''; print('Eltex ESR · консоль. Режим privileged.', 'cs-sys'); pr.textContent = prompt(st);
      sendB.style.display = T.send ? '' : 'none';
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        var v = inp.value; print(prompt(st) + ' ' + v, 'cs-cmd'); hist.push(v); hi = hist.length;
        var r = exec(st, v); if (r) print(r, /^%/.test(r) ? 'cs-err' : ''); inp.value = ''; pr.textContent = prompt(st) + ' ';
        e.preventDefault();
      } else if (e.key === 'ArrowUp') { if (hi > 0) { hi--; inp.value = hist[hi]; } e.preventDefault(); }
      else if (e.key === 'ArrowDown') { if (hi < hist.length) { hi++; inp.value = hist[hi] || ''; } e.preventDefault(); }
      e.stopPropagation();
    });
    out.addEventListener('click', function () { inp.focus(); });
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cs]'); if (!b) return;
      var a = b.dataset.cs;
      if (a === 'new') newTask();
      if (a === 'sol') sol.style.display = sol.style.display === 'none' ? 'block' : 'none';
      if (a === 'check') {
        var cs = T.checks(P), ok = 0;
        res.innerHTML = cs.map(function (c) { var y = !!c[1](st); if (y) ok++; return '<div class="' + (y ? 'ok' : 'no') + '">' + (y ? '✓ ' : '✗ ') + c[0] + '</div>'; }).join('') +
          '<div class="cs-sum ' + (ok === cs.length ? 'ok' : 'no') + '">' + (ok === cs.length ? 'Задание выполнено' : 'Выполнено ' + ok + ' из ' + cs.length) + '</div>';
      }
      if (a === 'send') {
        res.innerHTML = '<div class="cs-send">' + T.send(P, st).map(function (x) {
          return '<div class="' + (x.ok ? 'ok' : 'no') + '"><span class="env">✉</span> ' + esc(x.t) + '</div>'; }).join('') + '</div>';
      }
    });
    newTask();
  }
  window.O5CLI = { TASKS: TASKS, fresh: fresh, exec: exec, prompt: prompt };
  document.querySelectorAll('.o5sim').forEach(init);
})();
