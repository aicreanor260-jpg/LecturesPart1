/* Тренажёр CLI маршрутизатора ESR для деки RIP 2.5.1: режимы и приглашения как в pptx
   (esr# → esr(config)# → esr(config-if-gi)# / esr(config-rip)#), кандидат-конфигурация применяется
   командой commit (do commit), имя в приглашении меняется после commit. Проверка — по применённому состоянию. */
(function () {
  'use strict';
  function fresh() {
    return { host: 'esr', ifs: {}, routes: [], rip: null };
  }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  var PR = { priv: '#', config: '(config)#', 'if': '(config-if-gi)#', rip: '(config-rip)#' };

  function ip2n(s) {
    var p = s.split('.'); if (p.length !== 4) return null;
    var n = 0;
    for (var i = 0; i < 4; i++) { var v = +p[i]; if (!/^\d+$/.test(p[i]) || v > 255) return null; n = n * 256 + v; }
    return n;
  }
  function n2ip(n) { return [n >>> 24 & 255, n >>> 16 & 255, n >>> 8 & 255, n & 255].join('.'); }
  function pfx(s) {            // "198.18.0.1/15" → {ip, len, net}
    var m = /^(\d+\.\d+\.\d+\.\d+)\/(\d+)$/.exec(s || ''); if (!m) return null;
    var ip = ip2n(m[1]), len = +m[2]; if (ip === null || len < 0 || len > 32) return null;
    var mask = len === 0 ? 0 : len === 32 ? 0xFFFFFFFF : (0xFFFFFFFF << (32 - len)) >>> 0;
    return { ip: ip, len: len, net: (ip & mask) >>> 0, str: m[1] + '/' + len, nstr: n2ip((ip & mask) >>> 0) + '/' + len };
  }
  function inNet(ipStr, netStr) {
    var a = pfx(ipStr), b = pfx(netStr); if (!a || !b) return false;
    var mask = b.len === 32 ? 0xFFFFFFFF : (0xFFFFFFFF << (32 - b.len)) >>> 0;
    return ((a.ip & mask) >>> 0) === b.net;
  }
  function ifName(t) {         // gigabitethernet 1/0/1 | gi1/0/1 | gigabitethernet1/0/1
    var m = /^(?:gigabitethernet|gi)\s*(\d+\/\d+\/\d+)$/.exec(t); return m ? m[1] : null;
  }

  // ------------------------------------------------------------------ команды
  function run(sim, line) {
    var st = sim.cand, s = line.trim().replace(/\s+/g, ' '), low = s.toLowerCase(), m;
    if (!s) return '';
    if (/^do /.test(low) && sim.mode !== 'priv') { var md = sim.mode; sim.mode = 'priv'; var r = run(sim, s.slice(3)); sim.mode = md; return r; }
    if (low === 'exit') { sim.mode = sim.mode === 'config' ? 'priv' : sim.mode === 'priv' ? 'priv' : 'config'; sim.ctx = null; return ''; }
    if (low === 'end') { sim.mode = 'priv'; sim.ctx = null; return ''; }
    if (sim.mode === 'priv') {
      if (low === 'config' || low === 'configure' || low === 'configure terminal') { sim.mode = 'config'; return ''; }
      if (low === 'commit') { sim.run = clone(st); sim.confirmed = false; return '(конфигурация применена — подтвердите командой confirm)'; }
      if (low === 'confirm') { if (!sim.run) return '% Нет изменений для подтверждения'; sim.confirmed = true; return '(конфигурация подтверждена)'; }
      if (/^(show|sh) (running-config|run)( routing rip)?$/.test(low)) return showRun(sim.run || fresh(), /rip$/.test(low));
      if (/^(show|sh) ip route$/.test(low)) return showRoute(sim.run || fresh());
      if (/^(show|sh) ip (route rip|rip)$/.test(low)) return '(RIP-маршрутов нет: соседи в тренажёре не подключены)';
      return '% Unknown command';
    }
    if (sim.mode === 'config') {
      if ((m = /^hostname (\S+)$/.exec(s))) { st.host = m[1]; return ''; }
      if ((m = /^interface (.+)$/.exec(low))) { var n = ifName(m[1]); if (!n) return '% Неверное имя интерфейса'; st.ifs[n] = st.ifs[n] || { ip: '', fw: true }; sim.mode = 'if'; sim.ctx = n; return ''; }
      if ((m = /^ip route (\S+) (\S+)$/.exec(low))) { var r1 = pfx(m[1]); if (!r1 || ip2n(m[2]) === null) return '% Неверный адрес'; st.routes.push(r1.nstr + ' ' + m[2]); return ''; }
      if (low === 'router rip') { st.rip = st.rip || { nets: [], passive: [], redist: [], timers: {}, en: false }; sim.mode = 'rip'; return ''; }
      if (low === 'no router rip') { st.rip = null; return ''; }
      return '% Unknown command';
    }
    if (sim.mode === 'if') {
      var it = st.ifs[sim.ctx];
      if ((m = /^ip address (\S+)$/.exec(low))) { var a = pfx(m[1]); if (!a) return '% Неверный адрес: нужен вид A.B.C.D/N'; it.ip = a.str; return ''; }
      if (low === 'ip firewall disable') { it.fw = false; return ''; }
      if (low === 'no ip firewall disable') { it.fw = true; return ''; }
      return '% Unknown command';
    }
    if (sim.mode === 'rip') {
      var R = st.rip;
      if ((m = /^network (\S+)$/.exec(low))) { var nn = pfx(m[1]); if (!nn) return '% Неверная сеть: нужен вид A.B.C.D/N'; if (nn.ip !== nn.net) return '% ' + m[1] + ' — не адрес сети'; if (R.nets.indexOf(nn.nstr) < 0) R.nets.push(nn.nstr); return ''; }
      if ((m = /^no network (\S+)$/.exec(low))) { R.nets = R.nets.filter(function (x) { return x !== m[1]; }); return ''; }
      if ((m = /^passive-interface (.+)$/.exec(low))) { var pi = ifName(m[1]); if (!pi) return '% Неверное имя интерфейса'; if (R.passive.indexOf(pi) < 0) R.passive.push(pi); return ''; }
      if ((m = /^redistribute (static|connected)$/.exec(low))) { if (R.redist.indexOf(m[1]) < 0) R.redist.push(m[1]); return ''; }
      if ((m = /^timers (update|invalid|flush) (\d+)$/.exec(low))) { var v = +m[2]; if (v < 12 || v > 65535) return '% Значение вне диапазона 12-65535'; R.timers[m[1]] = v; return ''; }
      if (low === 'enable') { R.en = true; return ''; }
      if (low === 'no enable') { R.en = false; return ''; }
      return '% Unknown command';
    }
    return '% Unknown command';
  }

  function showRun(c, ripOnly) {
    var o = [];
    if (!ripOnly) {
      o.push('hostname ' + c.host);
      Object.keys(c.ifs).sort().forEach(function (k) {
        var i = c.ifs[k]; o.push('interface gigabitethernet ' + k);
        if (!i.fw) o.push('  ip firewall disable');
        if (i.ip) o.push('  ip address ' + i.ip);
        o.push('exit');
      });
      c.routes.forEach(function (r) { o.push('ip route ' + r); });
    }
    if (c.rip) {
      var R = c.rip; o.push('router rip');
      R.passive.forEach(function (p) { o.push('  passive-interface gigabitethernet ' + p); });
      ['update', 'invalid', 'flush'].forEach(function (t) { if (R.timers[t]) o.push('  timers ' + t + ' ' + R.timers[t]); });
      R.nets.forEach(function (n) { o.push('  network ' + n); });
      R.redist.forEach(function (r) { o.push('  redistribute ' + r); });
      if (R.en) o.push('  enable');
      o.push('exit');
    }
    return o.join('\n') || '(конфигурация пуста)';
  }
  function showRoute(c) {
    var o = [];
    c.routes.forEach(function (r) { var p = r.split(' '); o.push('S     * ' + p[0] + '   [1/0]   via ' + p[1]); });
    Object.keys(c.ifs).sort().forEach(function (k) { var a = pfx(c.ifs[k].ip); if (a) o.push('C     * ' + a.nstr + '   [0/0]   dev gi' + k); });
    return o.join('\n') || '(таблица пуста)';
  }

  // какие интерфейсы рассылают RIP-обновления и какие сети объявляются (по применённой конфигурации)
  function updates(c) {
    if (!c.rip || !c.rip.en) return { err: 'RIP не включён (нет enable в router rip или не выполнен commit)' };
    var out = [], ann = [];
    Object.keys(c.ifs).sort().forEach(function (k) {
      var i = c.ifs[k]; if (!i.ip) return;
      var cov = c.rip.nets.some(function (n) { return inNet(i.ip, n); });
      if (!cov) return;
      ann.push(pfx(i.ip).nstr);
      out.push({ ifn: k, passive: c.rip.passive.indexOf(k) >= 0, fw: i.fw });
    });
    if (c.rip.redist.indexOf('static') >= 0) c.routes.forEach(function (r) { ann.push(r.split(' ')[0] + ' (static)'); });
    return { out: out, ann: ann };
  }

  // ------------------------------------------------------------------ задания
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  var TASKS = [
    function () {   // как R1 / R2 примера pptx
      var h = pick(['R1', 'R2', 'R3', 'R4', 'ESR-1', 'ESR-2']), x = rnd(10, 99), l = rnd(1, 9) * 10, u = pick([15, 20, 30]);
      var g = { host: h, wan: '1/0/1', lan: '1/0/2', wip: '10.' + x + '.0.2/24', wnet: '10.' + x + '.0.0/24',
        lip: '192.168.' + l + '.1/24', u: u };
      return { g: g,
        text: 'Маршрутизатор <b>' + h + '</b>: имя устройства; gi' + g.wan + ' — <b>' + g.wip + '</b>, gi' + g.lan + ' — <b>' + g.lip +
          '</b> (LAN), на обоих firewall отключить. RIP: анонсировать <b>' + g.wnet + '</b>, запретить анонсы в LAN, таймеры ' +
          'update <b>' + u + '</b> / invalid <b>' + 3 * u + '</b> / flush <b>' + 7 * u + '</b>, включить протокол. Применить и подтвердить.',
        sol: ['config', 'hostname ' + h, 'do commit', 'do confirm', 'interface gigabitethernet ' + g.wan, 'ip firewall disable',
          'ip address ' + g.wip, 'exit', 'interface gigabitethernet ' + g.lan, 'ip firewall disable', 'ip address ' + g.lip, 'exit',
          'router rip', 'network ' + g.wnet, 'passive-interface gigabitethernet ' + g.lan, 'timers update ' + u,
          'timers invalid ' + 3 * u, 'timers flush ' + 7 * u, 'enable', 'exit', 'exit', 'commit', 'confirm'] };
    },
    function () {   // как маршрутизатор RIP примера pptx: маршрут по умолчанию и redistribute static
      var h = pick(['RIP', 'CORE', 'EDGE']), a = rnd(11, 99), b = rnd(11, 99), l = rnd(1, 9) * 10;
      var g = { host: h, i1: '1/0/1', i2: '1/0/2', i3: '1/0/3', i4: '1/0/4', ip1: '172.' + (16 + rnd(0, 15)) + '.' + a + '.1/24',
        ip2: '10.' + b + '.0.1/24', ip3: '192.168.' + l + '.1/24', ip4: '203.0.113.1/24', gw: '203.0.113.2' };
      g.n1 = pfx(g.ip1).nstr; g.n2 = pfx(g.ip2).nstr;
      return { g: g,
        text: 'Маршрутизатор <b>' + h + '</b>: gi1/0/1 — <b>' + g.ip1 + '</b>, gi1/0/2 — <b>' + g.ip2 + '</b>, gi1/0/3 — <b>' + g.ip3 +
          '</b> (LAN), gi1/0/4 — <b>' + g.ip4 + '</b> (к ISP), firewall отключить на всех. Маршрут по умолчанию через <b>' + g.gw +
          '</b>. RIP: анонсировать <b>' + g.n1 + '</b>, <b>' + g.n2 + '</b>, <b>203.0.113.0/24</b> и статические маршруты, без анонсов в LAN, включить. Применить и подтвердить.',
        sol: ['config', 'hostname ' + h, 'ip route 0.0.0.0/0 ' + g.gw].concat(
          [[g.i1, g.ip1], [g.i2, g.ip2], [g.i3, g.ip3], [g.i4, g.ip4]].reduce(function (acc, p) {
            return acc.concat(['interface gigabitethernet ' + p[0], 'ip firewall disable', 'ip address ' + p[1], 'exit']); }, []),
          ['router rip', 'network ' + g.n1, 'network ' + g.n2, 'network 203.0.113.0/24', 'redistribute static',
           'passive-interface gigabitethernet 1/0/3', 'enable', 'exit', 'exit', 'commit', 'confirm']) };
    },
    function () {   // два соседа и таймеры
      var h = pick(['R2', 'R5', 'BRANCH']), a = rnd(1, 200), b = rnd(1, 200), u = pick([15, 20, 25, 30]);
      var g = { host: h, ip1: '10.10.' + a + '.1/30', ip2: '10.20.' + b + '.1/30', ip3: '192.168.100.1/24' };
      g.n1 = pfx(g.ip1).nstr; g.n2 = pfx(g.ip2).nstr;
      return { g: g,
        text: 'Маршрутизатор <b>' + h + '</b>: gi1/0/1 — <b>' + g.ip1 + '</b>, gi1/0/2 — <b>' + g.ip2 + '</b>, gi1/0/3 — <b>' + g.ip3 +
          '</b> (LAN), firewall отключить. RIP объявляет обе линии к соседям и LAN, но в LAN обновления не рассылает; update <b>' + u +
          '</b>, invalid <b>' + 3 * u + '</b>, flush <b>' + 7 * u + '</b>. Включить, применить, подтвердить.',
        sol: ['config', 'hostname ' + h].concat(
          [['1/0/1', g.ip1], ['1/0/2', g.ip2], ['1/0/3', g.ip3]].reduce(function (acc, p) {
            return acc.concat(['interface gigabitethernet ' + p[0], 'ip firewall disable', 'ip address ' + p[1], 'exit']); }, []),
          ['router rip', 'network ' + g.n1, 'network ' + g.n2, 'network 192.168.100.0/24', 'passive-interface gigabitethernet 1/0/3',
           'timers update ' + u, 'timers invalid ' + 3 * u, 'timers flush ' + 7 * u, 'enable', 'exit', 'exit', 'commit', 'confirm']) };
    }
  ];

  function checks(sim) {
    var c = sim.run || fresh(), T = sim.task, out = [], R = c.rip || { nets: [], passive: [], redist: [], timers: {}, en: false };
    function ck(ok, s) { out.push([!!ok, s]); }
    // проверки строятся из эталонного решения: применяем его к чистому устройству и сравниваем
    var ref = { mode: 'priv', cand: fresh(), run: null };
    T.sol.forEach(function (l) { run(ref, l); });
    var E = ref.run;
    ck(c.host === E.host, 'имя устройства ' + E.host + ' (после commit)');
    Object.keys(E.ifs).sort().forEach(function (k) {
      var i = c.ifs[k] || {};
      ck(i.ip === E.ifs[k].ip, 'gi' + k + ': ip address ' + E.ifs[k].ip);
      ck(i.fw === false, 'gi' + k + ': ip firewall disable');
    });
    E.routes.forEach(function (r) { ck(c.routes.indexOf(r) >= 0, 'ip route ' + r); });
    E.rip.nets.forEach(function (n) { ck(R.nets.indexOf(n) >= 0, 'network ' + n); });
    ck(R.nets.length === E.rip.nets.length, 'нет лишних network');
    E.rip.passive.forEach(function (p) { ck(R.passive.indexOf(p) >= 0, 'passive-interface gigabitethernet ' + p); });
    E.rip.redist.forEach(function (r) { ck(R.redist.indexOf(r) >= 0, 'redistribute ' + r); });
    Object.keys(E.rip.timers).forEach(function (t) { ck(R.timers[t] === E.rip.timers[t], 'timers ' + t + ' ' + E.rip.timers[t]); });
    ck(R.en, 'enable — процесс RIP запущен');
    ck(sim.confirmed && JSON.stringify(sim.run) === JSON.stringify(sim.cand), 'commit и confirm после всех изменений');
    return out;
  }

  // ------------------------------------------------------------------ интерфейс
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }
  function init(box) {
    var pool = box.dataset.pool.split(',').map(Number), out = box.querySelector('.cs-out'), inp = box.querySelector('input'),
      pr = box.querySelector('.cs-pr'), res = box.querySelector('.cs-res'), solp = box.querySelector('.cs-sol'),
      tk = box.querySelector('.cs-task'), hist = [], hi = 0, sim;
    function prompt() { return (sim.run ? sim.run.host : 'esr') + PR[sim.mode]; }
    function print(s, cls) { var d = document.createElement('div'); if (cls) d.className = cls; d.textContent = s; out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function reset() {
      sim = { mode: 'priv', cand: fresh(), run: null, confirmed: false, ctx: null, task: TASKS[pick(pool)]() };
      tk.innerHTML = sim.task.text; out.innerHTML = ''; res.innerHTML = ''; solp.style.display = 'none';
      solp.textContent = sim.task.sol.join('\n');
      print('ESR — заводская конфигурация. Введите команды; config — режим конфигурации.', 'cs-sys');
      pr.textContent = prompt();
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowUp' && hist.length) { hi = Math.max(0, hi - 1); inp.value = hist[hi]; e.preventDefault(); return; }
      if (e.key === 'ArrowDown' && hist.length) { hi = Math.min(hist.length, hi + 1); inp.value = hist[hi] || ''; e.preventDefault(); return; }
      e.stopPropagation();
      if (e.key !== 'Enter') return;
      var v = inp.value; inp.value = ''; if (v.trim()) { hist.push(v); hi = hist.length; }
      print(prompt() + ' ' + v, 'cs-cmd');
      var r = run(sim, v);
      if (r) print(r, /^%/.test(r) ? 'cs-err' : '');
      pr.textContent = prompt();
    });
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cs]'); if (!b) return;
      var a = b.dataset.cs;
      if (a === 'new') reset();
      if (a === 'sol') solp.style.display = solp.style.display === 'none' ? 'block' : 'none';
      if (a === 'check') {
        var L = checks(sim), ok = L.filter(function (x) { return x[0]; }).length;
        res.innerHTML = L.map(function (x) { return '<div class="' + (x[0] ? 'ok' : 'no') + '">' + (x[0] ? '✓ ' : '✗ ') + esc(x[1]) + '</div>'; }).join('') +
          '<div class="cs-sum ' + (ok === L.length ? 'ok' : 'no') + '">' + (ok === L.length ? 'Задание выполнено' : ok + ' / ' + L.length) + '</div>';
      }
      if (a === 'send') {
        var u = updates(sim.run || fresh());
        if (u.err) { res.innerHTML = '<div class="no">✗ ' + esc(u.err) + '</div>'; return; }
        res.innerHTML = '<div class="cs-send">' + (u.out.length ? u.out.map(function (o) {
          return '<div class="' + (o.passive ? 'exp' : 'ok') + '"><span class="env">✉</span> gi' + o.ifn + ': ' +
            (o.passive ? 'passive-interface — обновления не отправляются' : 'RIP-обновление на 224.0.0.9, UDP 520') + '</div>';
        }).join('') : '<div class="no">Ни один интерфейс не попадает в network</div>') +
          '<div>Объявляемые сети: ' + (u.ann.length ? esc(u.ann.join(', ')) : '—') + '</div></div>';
      }
    });
    reset();
  }
  window.RP1CLI = { run: run, fresh: fresh, TASKS: TASKS, checks: checks };
  document.querySelectorAll('.clisim[data-deck="rp1"]').forEach(init);
})();
