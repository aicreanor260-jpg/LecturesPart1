/* Тренажёр CLI маршрутизатора Eltex ESR: GRE-туннель (дека «WAN на основе Ethernet»).
   Команды — те, что перечислены в pptx: local address, remote address, description, mode (ip | ethernet), ip address,
   bridge-group, key, enable; применение commit / confirm. Вход в режим туннеля: tunnel gre N → R1(config-gre)#.
   Вторая сторона (R2) уже настроена — её параметры в задании. «Отправить ping» проверяет, поднимется ли туннель. */
(function () {
  'use strict';
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  function blank() { return { host: 'R1', ifs: { 'gi1/0/1': { ip: null }, 'gi1/0/2': { ip: null } }, gre: {} }; }
  function fresh() { var c = blank(); return { cand: c, run: clone(c), mode: 'priv', ctx: null, pending: false, confirmed: true }; }
  var PROMPT = { priv: '#', config: '(config)#', gre: '(config-gre)#', gi: '(config-if-gi)#' };
  function prompt(st) { return st.run.host + PROMPT[st.mode]; }
  function okIp(s) { return /^\d+\.\d+\.\d+\.\d+$/.test(s) && s.split('.').every(function (o) { return +o <= 255; }); }
  function ip2n(s) { var p = s.split('.'); return ((+p[0] << 24) >>> 0) + (+p[1] << 16) + (+p[2] << 8) + (+p[3]); }
  function sameNet(a, b, len) { var m = len ? (0xffffffff << (32 - len)) >>> 0 : 0; return ((ip2n(a) & m) >>> 0) === ((ip2n(b) & m) >>> 0); }

  var CMDS = [];
  function cmd(modes, re, run) { CMDS.push({ modes: modes.split(' '), re: re, run: run }); }
  var CFG = 'config gre gi';
  function t(st) { return st.cand.gre[st.ctx]; }

  cmd('priv', /^(?:configure|conf|config)(?: terminal)?$/, function (st) { st.mode = 'config'; });
  cmd('priv', /^commit$/, function (st) {
    if (JSON.stringify(st.cand) === JSON.stringify(st.run)) return 'Nothing to commit in configuration';
    st.run = clone(st.cand); st.pending = true; st.confirmed = false;
    return 'Configuration has been successfully applied and saved to flash. Commit timer started, changes will be reverted in 600 seconds.'; });
  cmd('priv', /^confirm$/, function (st) {
    if (!st.pending) return 'Nothing to confirm in configuration. You must commit some changes first.';
    st.pending = false; st.confirmed = true; return 'Configuration has been confirmed. Commit timer canceled.'; });
  cmd('priv', /^exit$/, function () { return '% Сессия остаётся открытой (тренажёр)'; });
  cmd('priv', /^(?:show|sh) running-config$/, function (st) { return showRun(st.run); });
  cmd('priv', /^(?:show|sh) candidate-config$/, function (st) { return showRun(st.cand); });
  cmd('priv', /^(?:show|sh) tunnels status$/, function (st) {
    var o = ['Tunnel          Admin    Link     Local address    Remote address', '              state    state', '------------    -----    -----    -------------    --------------'];
    Object.keys(st.run.gre).forEach(function (n) { var x = st.run.gre[n];
      o.push(('gre ' + n + '            ').slice(0, 16) + (x.en ? 'Up       ' : 'Down     ') + (up(st, n).ok ? 'Up       ' : 'Down     ') +
             ((x.local || '--') + '                 ').slice(0, 17) + (x.remote || '--')); });
    return o.join('\n'); });
  cmd(CFG, /^exit$/, function (st) { st.mode = st.mode === 'config' ? 'priv' : 'config'; st.ctx = null; });
  cmd(CFG, /^end$/, function (st) { st.mode = 'priv'; st.ctx = null; });
  cmd('config', /^hostname (\S+)$/, function (st, m) { st.cand.host = m[1]; });
  cmd('config', /^tunnel gre (\d+)$/, function (st, m) {
    var n = +m[1]; if (n < 1 || n > 1000) return '% Номер туннеля от 1';
    if (!st.cand.gre[n]) st.cand.gre[n] = { local: null, remote: null, ip: null, mode: 'ip', bridge: null, key: null, desc: null, en: false };
    st.mode = 'gre'; st.ctx = n; });
  cmd('config', /^no tunnel gre (\d+)$/, function (st, m) { if (!st.cand.gre[+m[1]]) return '% Туннель не найден'; delete st.cand.gre[+m[1]]; });
  cmd('config', /^interface (?:gigabitethernet ?|gi)1\/0\/([12])$/, function (st, m) { st.mode = 'gi'; st.ctx = 'gi1/0/' + m[1]; });
  cmd('gi', /^ip address (\d+\.\d+\.\d+\.\d+)\/(\d+)$/, function (st, m) { st.cand.ifs[st.ctx].ip = m[1] + '/' + m[2]; });
  cmd('gre', /^local address (\S+)$/, function (st, m) { if (!okIp(m[1])) return '% Неверный IP-адрес'; t(st).local = m[1]; });
  cmd('gre', /^remote address (\S+)$/, function (st, m) { if (!okIp(m[1])) return '% Неверный IP-адрес'; t(st).remote = m[1]; });
  cmd('gre', /^ip address (\d+\.\d+\.\d+\.\d+)\/(\d+)$/, function (st, m) {
    if (!okIp(m[1]) || +m[2] > 32) return '% Неверный адрес';
    if (t(st).mode === 'ethernet') return '% В режиме ethernet IP-адрес не задаётся — используйте bridge-group';
    t(st).ip = m[1] + '/' + m[2]; });
  cmd('gre', /^ip address \S+$/, function () { return '% Адрес указывается с префиксом: ip address 192.0.2.1/30'; });
  cmd('gre', /^mode (ip|ethernet)$/, function (st, m) { t(st).mode = m[1]; if (m[1] === 'ethernet') t(st).ip = null; else t(st).bridge = null; });
  cmd('gre', /^bridge-group (\d+)$/, function (st, m) {
    if (t(st).mode !== 'ethernet') return '% bridge-group используется в режиме ethernet (mode ethernet)'; t(st).bridge = +m[1]; });
  cmd('gre', /^key (\d+)$/, function (st, m) { var k = +m[1]; if (k < 1 || k > 2000000) return '% Ключ от 1 до 2 000 000'; t(st).key = k; });
  cmd('gre', /^no key$/, function (st) { t(st).key = null; });
  cmd('gre', /^description (.+)$/, function (st, m) { t(st).desc = m[1].replace(/^"(.*)"$/, '$1'); });
  cmd('gre', /^enable$/, function (st) { t(st).enable = true; t(st).en = true; delete t(st).enable; });
  cmd('gre', /^no enable$/, function (st) { t(st).en = false; });

  function showRun(c) {
    var o = ['hostname ' + c.host, ''];
    Object.keys(c.ifs).forEach(function (k) { if (c.ifs[k].ip) o.push('interface gigabitethernet ' + k.slice(2), '  ip address ' + c.ifs[k].ip, 'exit'); });
    Object.keys(c.gre).forEach(function (n) { var x = c.gre[n]; o.push('tunnel gre ' + n);
      if (x.desc) o.push('  description "' + x.desc + '"');
      if (x.mode === 'ethernet') o.push('  mode ethernet');
      if (x.key) o.push('  key ' + x.key);
      if (x.local) o.push('  local address ' + x.local);
      if (x.remote) o.push('  remote address ' + x.remote);
      if (x.ip) o.push('  ip address ' + x.ip);
      if (x.bridge) o.push('  bridge-group ' + x.bridge);
      if (x.en) o.push('  enable');
      o.push('exit'); });
    return o.join('\n');
  }
  function exec(st, line) {
    var s = line.trim().replace(/\s+/g, ' ').replace(/^\S+?(\([^)]*\))?#\s*/, '');
    if (!s) return '';
    s = s.replace(/^int(?:erface)? (?:gigabitethernet ?|gi)(\d)/i, 'interface gi$1');
    if (/\?$/.test(s)) return help(st);
    var d = s.match(/^do (.+)$/);
    if (d) { var keep = st.mode, ctx = st.ctx; st.mode = 'priv'; var r0 = run1(st, d[1]); st.mode = keep; st.ctx = ctx; return r0 === null ? '% Unknown command' : r0; }
    var r = run1(st, s); if (r !== null) return r;
    for (var j = 0; j < CMDS.length; j++) if (s.match(CMDS[j].re)) return '% Команда недоступна в этом режиме';
    return '% Unknown command';
  }
  function run1(st, s) {
    for (var i = 0; i < CMDS.length; i++) { var c = CMDS[i], m = s.match(c.re); if (m && c.modes.indexOf(st.mode) >= 0) return c.run(st, m) || ''; }
    return null;
  }
  function help(st) {
    if (st.mode === 'priv') return 'commit  confirm  configure  show running-config  show tunnels status  exit';
    if (st.mode === 'config') return 'tunnel gre N  interface gigabitethernet 1/0/N  hostname  do  exit  end';
    if (st.mode === 'gre') return 'local address  remote address  description  mode ip|ethernet  ip address  bridge-group  key  enable  exit';
    return 'ip address  exit  end';
  }

  // ------------------------------------------------------------------ поднимется ли туннель (R2 настроен по заданию)
  function up(st, n) {
    var P = st.peer, x = st.run.gre[n];
    if (!P || !x) return { ok: false, why: 'туннель не создан' };
    var wan = st.run.ifs['gi1/0/1'].ip;
    if (!x.en) return { ok: false, why: 'туннель не включён (enable)' };
    if (!x.local || !x.remote) return { ok: false, why: 'не заданы local address и remote address' };
    if (wan && x.local !== wan.split('/')[0]) return { ok: false, why: 'local address не совпадает с адресом R1 на gi1/0/1 (' + wan.split('/')[0] + ')' };
    if (x.local === P.remoteWan && x.remote === P.r1Wan) return { ok: false, why: 'local и remote перепутаны местами' };
    if (x.local !== P.r1Wan) return { ok: false, why: 'R2 ждёт туннель с адреса ' + P.r1Wan };
    if (x.remote !== P.remoteWan) return { ok: false, why: 'remote address должен быть адресом R2 — ' + P.remoteWan };
    if ((x.key || null) !== (P.key || null)) return { ok: false, why: P.key ? 'ключ не совпадает с R2 (key ' + P.key + ') — R2 отбрасывает GRE-пакеты' : 'на R2 ключ не настроен, а на R1 задан key — пакеты отбрасываются' };
    if (P.mode === 'ethernet') {
      if (x.mode !== 'ethernet') return { ok: false, why: 'на R2 туннель в режиме ethernet — нужен mode ethernet' };
      if (x.bridge !== P.bridge) return { ok: false, why: 'нужна bridge-group ' + P.bridge };
      return { ok: true, why: 'L2-туннель Up, кадры bridge-group ' + P.bridge + ' проходят' };
    }
    if (x.mode !== 'ip') return { ok: false, why: 'на R2 туннель в режиме ip' };
    if (!x.ip) return { ok: false, why: 'не задан ip address внутри туннеля' };
    var a = x.ip.split('/'), len = +a[1];
    if (a[0] === P.tunIp) return { ok: false, why: 'адрес ' + a[0] + ' уже занят на R2' };
    if (!sameNet(a[0], P.tunIp, len) || len !== P.tunLen) return { ok: false, why: 'адрес туннеля не в одной сети с R2 (' + P.tunIp + '/' + P.tunLen + ')' };
    return { ok: true, why: 'эхо-ответ от ' + P.tunIp + ' получен через туннель gre ' + n };
  }
  function applied(st) { return st.confirmed && !st.pending && JSON.stringify(st.cand) === JSON.stringify(st.run); }
  var A = ['Изменения применены (commit) и подтверждены (confirm)', applied];

  function gen(withKey, eth) {
    var o = rnd(1, 200), r = rnd(1, 200), n = rnd(1, 9), b = rnd(0, 63) * 4;
    return { n: n, r1Wan: '203.0.113.' + o, remoteWan: '198.18.0.' + r, tunIp: '192.0.2.' + (b + 2), mine: '192.0.2.' + (b + 1), tunLen: 30,
             key: withKey ? rnd(10, 999999) : null, mode: eth ? 'ethernet' : 'ip', bridge: eth ? rnd(1, 9) : null };
  }
  function base(P, st) { st.peer = P; exec(st, 'configure'); exec(st, 'interface gigabitethernet 1/0/1'); exec(st, 'ip address ' + P.r1Wan + '/24');
    exec(st, 'end'); exec(st, 'commit'); exec(st, 'confirm'); }
  function peerText(P) {
    return '<br>R1: gi1/0/1 = <b>' + P.r1Wan + '/24</b> (уже настроен). R2: WAN <b>' + P.remoteWan + '</b>' +
      (P.mode === 'ethernet' ? ', туннель в режиме <b>ethernet</b>, bridge-group <b>' + P.bridge + '</b>' : ', адрес в туннеле <b>' + P.tunIp + '/30</b>') +
      (P.key ? ', key <b>' + P.key + '</b>' : '') + '.';
  }
  function upCheck(P) { return ['Туннель gre ' + P.n + ' поднимается с R2', function (s) { return up(s, P.n).ok; }]; }
  function sendUp(P, st) { var r = up(st, P.n); return [{ ok: r.ok, t: (P.mode === 'ethernet' ? 'кадр через L2-туннель: ' : 'ping ' + P.tunIp + ': ') + r.why }]; }

  var TASKS = [
    { gen: function () { return gen(false, false); }, setup: base,
      text: function (P) { return 'Постройте GRE-туннель <b>' + P.n + '</b> от R1 к R2 в режиме ip, адрес R1 внутри туннеля — <b>' + P.mine +
        '/30</b>. Включите туннель, примените и подтвердите.' + peerText(P); },
      sol: function (P) { return ['configure', 'tunnel gre ' + P.n, 'local address ' + P.r1Wan, 'remote address ' + P.remoteWan,
        'ip address ' + P.mine + '/30', 'enable', 'end', 'commit', 'confirm']; },
      checks: function (P) { return [upCheck(P), A]; }, send: sendUp },
    { gen: function () { return gen(true, false); }, setup: base,
      text: function (P) { return 'Постройте GRE-туннель <b>' + P.n + '</b> к R2 с <b>ключом</b>, как на R2, и описанием <b>to-R2</b>. Адрес R1 '
        + 'внутри туннеля — <b>' + P.mine + '/30</b>.' + peerText(P); },
      sol: function (P) { return ['configure', 'tunnel gre ' + P.n, 'description to-R2', 'key ' + P.key, 'local address ' + P.r1Wan,
        'remote address ' + P.remoteWan, 'ip address ' + P.mine + '/30', 'enable', 'end', 'commit', 'confirm']; },
      checks: function (P) { return [['Описание to-R2', function (s) { var x = s.run.gre[P.n]; return x && x.desc === 'to-R2'; }], upCheck(P), A]; },
      send: sendUp },
    { gen: function () { return gen(false, true); }, setup: base,
      text: function (P) { return 'Постройте L2-туннель GRE <b>' + P.n + '</b> (Ethernet over GRE) к R2: режим <b>ethernet</b> и привязка к '
        + 'широковещательному домену через bridge-group, как на R2.' + peerText(P); },
      sol: function (P) { return ['configure', 'tunnel gre ' + P.n, 'mode ethernet', 'local address ' + P.r1Wan, 'remote address ' + P.remoteWan,
        'bridge-group ' + P.bridge, 'enable', 'end', 'commit', 'confirm']; },
      checks: function (P) { return [['Режим ethernet', function (s) { var x = s.run.gre[P.n]; return x && x.mode === 'ethernet'; }], upCheck(P), A]; },
      send: sendUp },
    { gen: function () { var P = gen(true, false); P.old = P.key + rnd(1, 999); return P; },
      setup: function (P, st) { base(P, st); ['configure', 'tunnel gre ' + P.n, 'key ' + P.old, 'local address ' + P.r1Wan, 'remote address ' + P.remoteWan,
        'ip address ' + P.mine + '/30', 'enable', 'end', 'commit', 'confirm'].forEach(function (l) { exec(st, l); }); },
      text: function (P) { return 'Туннель gre <b>' + P.n + '</b> настроен, но ping до R2 не проходит: на R2 сменили ключ на <b>' + P.key +
        '</b>. Исправьте ключ на R1, примените и подтвердите. Проверьте кнопкой «Отправить ping».' + peerText(P); },
      sol: function (P) { return ['configure', 'tunnel gre ' + P.n, 'key ' + P.key, 'end', 'commit', 'confirm']; },
      checks: function (P) { return [upCheck(P), A]; }, send: sendUp },
    { gen: function () { return gen(false, false); },
      setup: function (P, st) { base(P, st); ['configure', 'tunnel gre ' + P.n, 'local address ' + P.r1Wan, 'ip address ' + P.mine + '/30', 'end',
        'commit', 'confirm'].forEach(function (l) { exec(st, l); }); },
      text: function (P) { return 'Туннель gre <b>' + P.n + '</b> «висит» в состоянии Down. Посмотрите show running-config и show tunnels status, '
        + 'найдите, чего не хватает (по pptx — обязательные команды и enable), исправьте, примените и подтвердите.' + peerText(P); },
      sol: function (P) { return ['configure', 'tunnel gre ' + P.n, 'remote address ' + P.remoteWan, 'enable', 'end', 'commit', 'confirm']; },
      checks: function (P) { return [upCheck(P), A]; }, send: sendUp }
  ];

  function init(box) {
    var pool = (box.dataset.pool || '').split(',').map(Number);
    var out = box.querySelector('.cs-out'), inp = box.querySelector('.cs-in input'), pr = box.querySelector('.cs-pr');
    var taskEl = box.querySelector('.cs-task'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol');
    var st, T, P, hist = [], hi = 0, last = -1;
    function print(x, cls) { var d = document.createElement('div'); d.className = cls || ''; d.innerHTML = esc(x); out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function newTask() {
      var k; do { k = pool[rnd(0, pool.length - 1)]; } while (pool.length > 1 && k === last); last = k;
      T = TASKS[k]; P = T.gen(); st = fresh(); T.setup(P, st); st.mode = 'priv'; st.ctx = null;
      taskEl.innerHTML = T.text(P); res.innerHTML = ''; sol.style.display = 'none'; sol.textContent = T.sol(P).join('\n');
      out.innerHTML = ''; print('*** Eltex ESR · R1 ***\nКонфигурация загружена: show running-config', 'cs-sys'); pr.textContent = prompt(st);
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        var v = inp.value; print(prompt(st) + ' ' + v, 'cs-cmd'); if (v.trim()) hist.push(v); hi = hist.length;
        var r = exec(st, v); if (r) print(r, /^%/.test(r) ? 'cs-err' : ''); inp.value = ''; pr.textContent = prompt(st); e.preventDefault();
      } else if (e.key === 'ArrowUp') { if (hi > 0) { hi--; inp.value = hist[hi]; } e.preventDefault(); }
      else if (e.key === 'ArrowDown') { if (hi < hist.length) { hi++; inp.value = hist[hi] || ''; } e.preventDefault(); }
      e.stopPropagation();
    });
    out.addEventListener('click', function () { inp.focus(); });
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cs]'); if (!b) return; var a = b.dataset.cs;
      if (a === 'new') newTask();
      if (a === 'sol') sol.style.display = sol.style.display === 'none' ? 'block' : 'none';
      if (a === 'check') { var cs = T.checks(P), ok = 0;
        res.innerHTML = cs.map(function (c) { var y = !!c[1](st); if (y) ok++; return '<div class="' + (y ? 'ok' : 'no') + '">' + (y ? '✓ ' : '✗ ') + esc(c[0]) + '</div>'; }).join('') +
          (up(st, P.n).ok ? '' : '<div class="exp">⚑ ' + esc(up(st, P.n).why) + '</div>') +
          '<div class="cs-sum ' + (ok === cs.length ? 'ok' : 'no') + '">' + (ok === cs.length ? 'Задание выполнено' : 'Выполнено ' + ok + ' из ' + cs.length) + '</div>'; }
      if (a === 'send') { res.innerHTML = '<div class="cs-send">' + T.send(P, st).map(function (x) {
        return '<div class="' + (x.ok ? 'ok' : 'no') + '"><span class="env">✉</span> ' + esc(x.t) + '</div>'; }).join('') + '</div>'; }
    });
    newTask();
  }
  window.GRE_CLI = { TASKS: TASKS, fresh: fresh, exec: exec, up: up, applied: applied };
  document.querySelectorAll('.clisim[data-deck=gre]').forEach(init);
})();
