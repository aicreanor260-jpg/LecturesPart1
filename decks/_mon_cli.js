/* Тренажёр CLI маршрутизатора Eltex ESR для деки «Мониторинг и управление». Команды — из pptx:
   lldp enable, lldp receive/transmit; port monitor interface …; syslog file / severity, syslog host / source-address / remote-address /
   transport / port, logging …; archive / type / path / count-backup / time-period / auto / by-commit; ip sla test / icmp-echo /
   frequency / enable, ip sla schedule, ip sla. Применение — commit / confirm. «Проверить в работе» показывает, что произойдёт. */
(function () {
  'use strict';
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  var SEV = ['emerg', 'alert', 'crit', 'error', 'warning', 'notice', 'info', 'debug'];

  function blank() {
    var ifs = {}; for (var i = 1; i <= 4; i++) ifs['gi1/0/' + i] = { rx: true, tx: true, mon: [] };
    ifs['gi1/0/24'] = { rx: true, tx: true, mon: [] };
    return { host: 'esr', lldp: false, ifs: ifs, files: {}, hosts: {}, logging: {}, archive: null, sla: { tests: {}, sched: {}, on: false } };
  }
  function fresh() { var c = blank(); return { cand: c, run: clone(c), mode: 'priv', ctx: null, pending: false, confirmed: true }; }
  var PROMPT = { priv: '#', config: '(config)#', gi: '(config-if-gi)#', sfile: '(config-syslog-file)#', shost: '(config-syslog-host)#',
                 arch: '(config-archive)#', sla: '(config-sla-test)#' };
  function prompt(st) { return st.run.host + PROMPT[st.mode]; }
  function okIp(s) { return /^\d+\.\d+\.\d+\.\d+$/.test(s) && s.split('.').every(function (o) { return +o <= 255; }); }
  function ifk(s) { var m = s.match(/^(?:gigabitethernet ?|gi)(1\/0\/\d+)$/); return m ? 'gi' + m[1] : null; }

  var CMDS = [];
  function cmd(modes, re, run) { CMDS.push({ modes: modes.split(' '), re: re, run: run }); }
  var CFG = 'config gi sfile shost arch sla';
  cmd('priv', /^(?:configure|config|conf)(?: terminal)?$/, function (st) { st.mode = 'config'; });
  cmd('priv', /^commit$/, function (st) {
    if (JSON.stringify(st.cand) === JSON.stringify(st.run)) return 'Nothing to commit in configuration';
    st.run = clone(st.cand); st.pending = true; st.confirmed = false;
    return 'Configuration has been successfully applied and saved to flash. Commit timer started, changes will be reverted in 600 seconds.'; });
  cmd('priv', /^confirm$/, function (st) { if (!st.pending) return 'Nothing to confirm in configuration. You must commit some changes first.';
    st.pending = false; st.confirmed = true; return 'Configuration has been confirmed. Commit timer canceled.'; });
  cmd('priv', /^exit$/, function () { return '% Сессия остаётся открытой (тренажёр)'; });
  cmd('priv', /^(?:show|sh) running-config$/, function (st) { return showRun(st.run); });
  cmd('priv', /^(?:show|sh) running-config mirroring$/, function (st) { return showRun(st.run, 'mirror'); });
  cmd('priv', /^(?:show|sh) syslog configuration$/, function (st) { var c = st.run, o = ['SYSLOG', '', 'File size: 512 (kiB)', 'Number of logs: 3', 'Console: info', '   Files:', '   ~~~~~~'];
    Object.keys(c.files).forEach(function (f, i) { o.push(i + '    ' + f + '    ' + (c.files[f] || 'info')); });
    Object.keys(c.hosts).forEach(function (h) { var x = c.hosts[h]; o.push('Host ' + h + ': ' + (x.remote || '--') + ' ' + (x.transport || 'udp') + ' ' + (x.port || 514)); });
    return o.join('\n'); });
  cmd('priv', /^(?:show|sh) lldp neighbors$/, function (st) {
    var o = ['Local Interface   Chassis Id          Port info        System Name', '---------------   -----------------   --------------   -----------'];
    if (st.run.lldp && st.run.ifs['gi1/0/1'].rx) o.push('gi1/0/1           a8:f9:4b:30:fc:c0   gi1/0/2          MES');
    return o.join('\n'); });
  cmd('priv', /^(?:show|sh) ip sla test configuration(?: (\d+))?$/, function (st) { return JSON.stringify(st.run.sla.tests, null, 1); });
  cmd(CFG, /^exit$/, function (st) { st.mode = st.mode === 'config' ? 'priv' : 'config'; st.ctx = null; });
  cmd(CFG, /^end$/, function (st) { st.mode = 'priv'; st.ctx = null; });
  cmd('config', /^hostname (\S+)$/, function (st, m) { st.cand.host = m[1]; });
  // LLDP
  cmd('config', /^lldp enable$/, function (st) { st.cand.lldp = true; });
  cmd('config', /^no lldp enable$/, function (st) { st.cand.lldp = false; });
  cmd('config', /^lldp run$/, function () { return '% Это команда коммутатора MES. На ESR: lldp enable'; });
  cmd('config', /^interface (\S+(?: \S+)?)$/, function (st, m) { var k = ifk(m[1].replace(' ', ' ')); if (!k || !st.cand.ifs[k]) return '% Такого интерфейса нет: gi1/0/1–4, gi1/0/24';
    st.mode = 'gi'; st.ctx = k; });
  cmd('gi', /^(no )?lldp (receive|transmit)$/, function (st, m) { st.cand.ifs[st.ctx][m[2] === 'receive' ? 'rx' : 'tx'] = !m[1]; });
  // SPAN
  cmd('gi', /^port monitor interface (\S+)(?: (rx|tx))?$/, function (st, m) {
    var k = ifk(m[1]); if (!k || !st.cand.ifs[k]) return '% Неверный интерфейс'; if (k === st.ctx) return '% Нельзя зеркалировать порт сам в себя';
    var mon = st.cand.ifs[st.ctx].mon.filter(function (x) { return x.src !== k; }); mon.push({ src: k, dir: m[2] || 'both' }); st.cand.ifs[st.ctx].mon = mon; });
  cmd('gi', /^no port monitor interface (\S+(?: \S+)?)$/, function (st, m) { var k = ifk(m[1]); st.cand.ifs[st.ctx].mon = st.cand.ifs[st.ctx].mon.filter(function (x) { return x.src !== k; }); });
  // Syslog
  cmd('config', /^syslog file (\S+)$/, function (st, m) { if (!/^(flash|tmpsys):syslog\//.test(m[1])) return '% Путь вида flash:syslog/ИМЯ или tmpsys:syslog/ИМЯ';
    if (!(m[1] in st.cand.files)) st.cand.files[m[1]] = null; st.mode = 'sfile'; st.ctx = m[1]; });
  cmd('sfile', /^severity (\S+)$/, function (st, m) { if (SEV.indexOf(m[1]) < 0) return '% Уровни: ' + SEV.join(', '); st.cand.files[st.ctx] = m[1]; });
  cmd('config', /^syslog host (\S+)$/, function (st, m) { if (!st.cand.hosts[m[1]]) st.cand.hosts[m[1]] = {}; st.mode = 'shost'; st.ctx = m[1]; });
  cmd('shost', /^source[- ]address (\S+)$/, function (st, m) { if (!okIp(m[1])) return '% Неверный IP-адрес'; st.cand.hosts[st.ctx].source = m[1]; });
  cmd('shost', /^remote[- ]address (\S+)$/, function (st, m) { if (!okIp(m[1])) return '% Неверный IP-адрес'; st.cand.hosts[st.ctx].remote = m[1]; });
  cmd('shost', /^transport (udp|tcp)$/, function (st, m) { st.cand.hosts[st.ctx].transport = m[1]; });
  cmd('shost', /^port (\d+)$/, function (st, m) { st.cand.hosts[st.ctx].port = +m[1]; });
  cmd('config', /^logging (login on-failure|syslog configuration|service start-stop|userinfo)$/, function (st, m) { st.cand.logging[m[1]] = true; });
  cmd('config', /^syslog (cli-commands|sequence-numbers|reload debugging)$/, function (st, m) { st.cand.logging['syslog ' + m[1]] = true; });
  // archive
  cmd('config', /^archive$/, function (st) { if (!st.cand.archive) st.cand.archive = { type: null, path: null, count: null, period: null, auto: false, commit: false };
    st.mode = 'arch'; });
  cmd('config', /^type (local|remote|both)$/, function () { return '% Команда type вводится в режиме archive: esr(config)# archive → esr(config-archive)#'; });
  cmd('arch', /^type (local|remote|both)$/, function (st, m) { st.cand.archive.type = m[1]; });
  cmd('arch', /^path (\S+)$/, function (st, m) { if (!/^(tftp|ftp|sftp|scp):\/\//.test(m[1])) return '% Путь: tftp://HOST:/FILE'; st.cand.archive.path = m[1]; });
  cmd('arch', /^count-backup (\d+)$/, function (st, m) { if (+m[1] < 1 || +m[1] > 100) return '% От 1 до 100'; st.cand.archive.count = +m[1]; });
  cmd('arch', /^time-period (\d+)$/, function (st, m) { st.cand.archive.period = +m[1]; });
  cmd('arch', /^auto$/, function (st) { st.cand.archive.auto = true; });
  cmd('arch', /^by-commit$/, function (st) { st.cand.archive.commit = true; });
  // IP SLA
  cmd('config', /^ip sla test (\d+)$/, function (st, m) { var n = +m[1]; if (n < 1 || n > 10000) return '% Номер теста 1-10000';
    if (!st.cand.sla.tests[n]) st.cand.sla.tests[n] = { mode: null, dst: null, src: null, freq: 10, en: false }; st.mode = 'sla'; st.ctx = n; });
  cmd('sla', /^icmp-echo (\S+) source-ip (\S+)(?: num-packets (\d+))?(?: interval (\d+))?$/, function (st, m) {
    if (!okIp(m[1]) || !okIp(m[2])) return '% Неверный IP-адрес'; var t = st.cand.sla.tests[st.ctx]; t.mode = 'icmp'; t.dst = m[1]; t.src = m[2]; });
  cmd('sla', /^udp-jitter (\S+) (\d+) source-ip (\S+)(?: num-packets (\d+))?(?: interval (\d+))?$/, function (st, m) {
    var t = st.cand.sla.tests[st.ctx]; t.mode = 'udp'; t.dst = m[1]; t.port = +m[2]; t.src = m[3]; });
  cmd('sla', /^frequency (\d+)$/, function (st, m) { if (+m[1] < 1 || +m[1] > 604800) return '% Диапазон 1-604800'; st.cand.sla.tests[st.ctx].freq = +m[1]; });
  cmd('sla', /^enable$/, function (st) { st.cand.sla.tests[st.ctx].en = true; });
  cmd('config', /^ip sla schedule (\d+) (?:life forever start-time now|start-time now life forever)$/, function (st, m) {
    if (!st.cand.sla.tests[+m[1]]) return '% Тест ' + m[1] + ' не создан'; st.cand.sla.sched[+m[1]] = true; });
  cmd('config', /^ip sla$/, function (st) { st.cand.sla.on = true; });

  function showRun(c, only) {
    var o = [];
    if (!only) { o.push('hostname ' + c.host, ''); if (c.lldp) o.push('lldp enable'); }
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k], d = [];
      if (!only) { if (!x.rx) d.push('  no lldp receive'); if (!x.tx) d.push('  no lldp transmit'); }
      x.mon.forEach(function (m) { d.push('  port monitor interface gigabitethernet ' + m.src.slice(2) + (m.dir === 'both' ? '' : ' ' + m.dir)); });
      if (d.length) o = o.concat(['interface gigabitethernet ' + k.slice(2)], d, ['exit']); });
    if (only) return o.join('\n');
    Object.keys(c.files).forEach(function (f) { o.push('syslog file ' + f); if (c.files[f]) o.push('  severity ' + c.files[f]); o.push('exit'); });
    Object.keys(c.hosts).forEach(function (h) { var x = c.hosts[h]; o.push('syslog host ' + h);
      if (x.source) o.push('  source-address ' + x.source); if (x.remote) o.push('  remote-address ' + x.remote);
      if (x.transport) o.push('  transport ' + x.transport); if (x.port) o.push('  port ' + x.port); o.push('exit'); });
    Object.keys(c.logging).forEach(function (l) { o.push(/^syslog /.test(l) ? l : 'logging ' + l); });
    if (c.archive) { var a = c.archive; o.push('archive'); if (a.type) o.push('  type ' + a.type); if (a.path) o.push('  path ' + a.path);
      if (a.count) o.push('  count-backup ' + a.count); if (a.period) o.push('  time-period ' + a.period); if (a.auto) o.push('  auto');
      if (a.commit) o.push('  by-commit'); o.push('exit'); }
    Object.keys(c.sla.tests).forEach(function (n) { var t = c.sla.tests[n]; o.push('ip sla test ' + n);
      if (t.mode === 'icmp') o.push('  icmp-echo ' + t.dst + ' source-ip ' + t.src); if (t.mode === 'udp') o.push('  udp-jitter ' + t.dst + ' ' + t.port + ' source-ip ' + t.src);
      if (t.freq !== 10) o.push('  frequency ' + t.freq); if (t.en) o.push('  enable'); o.push('exit'); });
    Object.keys(c.sla.sched).forEach(function (n) { o.push('ip sla schedule ' + n + ' life forever start-time now'); });
    if (c.sla.on) o.push('ip sla');
    return o.join('\n');
  }
  function exec(st, line) {
    var s = line.trim().replace(/\s+/g, ' ').replace(/^\S+?(\([^)]*\))?#\s*/, '');
    if (!s) return '';
    s = s.replace(/^int(?:erface)? /, 'interface ').replace(/(interface|port monitor interface|no port monitor interface) gigabitethernet (\d)/, '$1 gi$2');
    if (/\?$/.test(s)) return 'Команды режима ' + prompt(st) + ' — см. шпаргалку; exit, end, do';
    var d = s.match(/^do (.+)$/);
    if (d) { var keep = st.mode, ctx = st.ctx; st.mode = 'priv'; var r0 = run1(st, d[1]); st.mode = keep; st.ctx = ctx; return r0 === null ? '% Unknown command' : r0; }
    var r = run1(st, s); if (r !== null) return r;
    for (var j = 0; j < CMDS.length; j++) if (s.match(CMDS[j].re)) return '% Команда недоступна в этом режиме';
    return '% Unknown command';
  }
  function run1(st, s) { for (var i = 0; i < CMDS.length; i++) { var c = CMDS[i], m = s.match(c.re); if (m && c.modes.indexOf(st.mode) >= 0) return c.run(st, m) || ''; } return null; }
  function applied(st) { return st.confirmed && !st.pending && JSON.stringify(st.cand) === JSON.stringify(st.run); }
  var A = ['Изменения применены (commit) и подтверждены (confirm)', applied];
  function chk(t, f) { return [t, f]; }

  var TASKS = [
    { // 0 LLDP
      gen: function () { return { end: 'gi1/0/' + rnd(2, 4) }; },
      text: function (P) { return 'Включите LLDP на маршрутизаторе глобально. Порт <b>' + P.end + '</b> смотрит на оконечное устройство — '
        + 'запретите на нём <b>передачу</b> LLDPDU (по pptx), приём оставьте. Примените и подтвердите, проверьте show lldp neighbors.'; },
      sol: function (P) { return ['configure', 'lldp enable', 'interface gigabitethernet ' + P.end.slice(2), 'no lldp transmit', 'end', 'commit', 'confirm', 'show lldp neighbors']; },
      checks: function (P) { return [chk('LLDP включён глобально (lldp enable)', function (s) { return s.run.lldp; }),
        chk('На ' + P.end + ' передача выключена', function (s) { return !s.run.ifs[P.end].tx; }),
        chk('На ' + P.end + ' приём оставлен', function (s) { return s.run.ifs[P.end].rx; }), A]; },
      send: function (P, st) { var c = st.run; return [
        { ok: c.lldp, t: 'gi1/0/1 ↔ MES: ' + (c.lldp ? 'сосед MES виден в show lldp neighbors' : 'LLDP выключен — соседей не видно') },
        { ok: c.lldp && !c.ifs[P.end].tx, t: P.end + ' → оконечное устройство: ' + (c.lldp && c.ifs[P.end].tx ? 'LLDPDU с данными об ESR уходит наружу' : 'сведения об устройстве не раскрываются') }]; } },
    { // 1 SPAN
      gen: function () { var a = rnd(1, 2); return { src: 'gi1/0/' + a, dir: pick(['', 'rx', 'tx']) }; },
      text: function (P) { return 'К порту <b>gi1/0/24</b> подключён ПК3 с Wireshark. Настройте локальное зеркалирование трафика порта <b>' + P.src + '</b>'
        + (P.dir ? ' (только <b>' + (P.dir === 'rx' ? 'входящий' : 'исходящий') + '</b>, ключ ' + P.dir + ')' : ' в обоих направлениях') + ' на gi1/0/24. Примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'interface gigabitethernet 1/0/24', 'port monitor interface gigabitethernet ' + P.src.slice(2) + (P.dir ? ' ' + P.dir : ''), 'end', 'commit', 'confirm', 'show running-config mirroring']; },
      checks: function (P) { return [chk('gi1/0/24 зеркалирует ' + P.src + ' (' + (P.dir || 'rx и tx') + ')', function (s) {
        return s.run.ifs['gi1/0/24'].mon.some(function (m) { return m.src === P.src && m.dir === (P.dir || 'both'); }); }), A]; },
      send: function (P, st) { var m = st.run.ifs['gi1/0/24'].mon.filter(function (x) { return x.src === P.src; })[0];
        return [{ ok: !!m && applied(st), t: 'кадр ПК1 → ПК2 через ' + P.src + ': ' + (m && applied(st) ? 'копия пришла на ПК3 (Wireshark), направление ' + m.dir : 'на gi1/0/24 копии нет') }]; } },
    { // 2 syslog file
      gen: function () { return { name: pick(['ESR', 'CRIT', 'DONTCRIT', 'NET']), fs: pick(['flash', 'tmpsys']), sev: pick(['info', 'crit', 'debug', 'error', 'warning']) }; },
      text: function (P) { return 'Создайте файл системного журнала <b>' + P.fs + ':syslog/' + P.name + '</b>, в который записываются события начиная с уровня <b>'
        + P.sev + '</b>. Включите нумерацию сообщений. Примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'syslog file ' + P.fs + ':syslog/' + P.name, 'severity ' + P.sev, 'exit', 'syslog sequence-numbers', 'end', 'commit', 'confirm', 'show syslog configuration']; },
      checks: function (P) { var f = P.fs + ':syslog/' + P.name; return [chk('Файл ' + f + ', severity ' + P.sev, function (s) { return s.run.files[f] === P.sev; }),
        chk('syslog sequence-numbers', function (s) { return !!s.run.logging['syslog sequence-numbers']; }), A]; },
      send: function (P, st) { var f = P.fs + ':syslog/' + P.name, lv = st.run.files[f]; var ev = pick(['crit', 'error', 'info', 'debug', 'notice']);
        var ok = lv && SEV.indexOf(ev) <= SEV.indexOf(lv); return [{ ok: !!lv, t: 'событие уровня ' + ev + ': ' + (!lv ? 'файла нет — не записано' : (ok ? 'записано в ' + f : 'ниже уровня ' + lv + ' — не записано (так и должно быть)')) }]; } },
    { // 3 syslog host + logging
      gen: function () { var o = rnd(1, 200); return { src: '192.0.2.' + o, dst: '192.0.2.254', name: pick(['SERVER', 'Syslog_SERVER', 'LOGSRV']) }; },
      text: function (P) { return 'Настройте отправку сообщений на syslog-сервер <b>' + P.name + '</b>: адрес ESR <b>' + P.src + '</b>, адрес сервера <b>' + P.dst
        + '</b>, UDP порт 514. Включите регистрацию неудачных аутентификаций и изменений профиля пользователей. Примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'syslog host ' + P.name, 'source-address ' + P.src, 'remote-address ' + P.dst, 'transport udp', 'port 514', 'exit',
        'logging login on-failure', 'logging userinfo', 'end', 'commit', 'confirm']; },
      checks: function (P) { return [chk('syslog host ' + P.name + ': ' + P.src + ' → ' + P.dst + ' udp/514', function (s) { var x = s.run.hosts[P.name];
          return x && x.source === P.src && x.remote === P.dst && x.transport === 'udp' && x.port === 514; }),
        chk('logging login on-failure', function (s) { return !!s.run.logging['login on-failure']; }),
        chk('logging userinfo', function (s) { return !!s.run.logging.userinfo; }), A]; },
      send: function (P, st) { var x = st.run.hosts[P.name], ok = x && x.remote === P.dst && x.port === 514 && st.run.logging['login on-failure'];
        return [{ ok: !!ok, t: 'неверный пароль admin: ' + (ok ? 'сообщение ушло на ' + P.dst + ':514/udp' : 'на сервер ничего не пришло') }]; } },
    { // 4 archive
      gen: function () { return { ip: '203.0.113.' + rnd(2, 254), dir: pick(['esr-example', 'backup', 'cfg']), n: pick([10, 20, 30]) }; },
      text: function (P) { return 'Настройте локальное и удалённое резервное копирование: tftp-сервер <b>' + P.ip + '</b>, папка <b>' + P.dir + '</b>, файл '
        + '<b>' + P.dir + '.cfg</b>; не больше <b>' + P.n + '</b> локальных копий; копия раз в сутки (1440 минут) и при каждом commit. Примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'archive', 'type both', 'path tftp://' + P.ip + ':/' + P.dir + '/' + P.dir + '.cfg', 'count-backup ' + P.n, 'time-period 1440', 'auto', 'by-commit', 'end', 'commit', 'confirm']; },
      checks: function (P) { var a = function (s) { return s.run.archive || {}; }; return [
        chk('type both', function (s) { return a(s).type === 'both'; }),
        chk('path tftp://' + P.ip + ':/' + P.dir + '/…', function (s) { return (a(s).path || '').indexOf('tftp://' + P.ip + ':/' + P.dir + '/') === 0; }),
        chk('count-backup ' + P.n, function (s) { return a(s).count === P.n; }), chk('time-period 1440 и auto', function (s) { return a(s).period === 1440 && a(s).auto; }),
        chk('by-commit', function (s) { return a(s).commit; }), A]; },
      send: function (P, st) { var a = st.run.archive || {}; return [
        { ok: !!a.commit, t: 'commit: ' + (a.commit ? 'копия сохранена' + (a.type !== 'remote' ? ' в flash:backup/' : '') + (a.type !== 'local' && a.path ? ' и на ' + a.path : '') : 'by-commit не включён — копии нет') }]; } },
    { // 5 IP SLA icmp
      gen: function () { return { n: rnd(1, 9), dst: '203.0.113.' + rnd(1, 50), src: '198.51.100.' + rnd(1, 50), f: pick([25, 30, 60]) }; },
      text: function (P) { return 'На SENDER создайте IP SLA тест <b>' + P.n + '</b> в режиме ICMP: адрес назначения <b>' + P.dst + '</b>, источник <b>' + P.src
        + '</b>, интервал между запусками <b>' + P.f + '</b> с. Активируйте тест, задайте график life forever start-time now и запустите IP SLA. Примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'ip sla test ' + P.n, 'icmp-echo ' + P.dst + ' source-ip ' + P.src, 'frequency ' + P.f, 'enable', 'exit',
        'ip sla schedule ' + P.n + ' life forever start-time now', 'ip sla', 'end', 'commit', 'confirm']; },
      checks: function (P) { var t = function (s) { return s.run.sla.tests[P.n] || {}; }; return [
        chk('icmp-echo ' + P.dst + ' source-ip ' + P.src, function (s) { return t(s).mode === 'icmp' && t(s).dst === P.dst && t(s).src === P.src; }),
        chk('frequency ' + P.f, function (s) { return t(s).freq === P.f; }), chk('тест активирован (enable)', function (s) { return t(s).en; }),
        chk('ip sla schedule ' + P.n, function (s) { return !!s.run.sla.sched[P.n]; }), chk('ip sla (запуск)', function (s) { return s.run.sla.on; }), A]; },
      send: function (P, st) { var t = st.run.sla.tests[P.n] || {}, ok = t.en && st.run.sla.sched[P.n] && st.run.sla.on && t.mode === 'icmp';
        return [{ ok: !!ok, t: 'show ip sla test statistics ' + P.n + ': ' + (ok ? 'Test status: Successful, Two-way delay min/avg/max: 6/8/36 milliseconds' : 'тест не выполняется — проверьте enable, schedule и ip sla') }]; } }
  ];

  function init(box) {
    var pool = (box.dataset.pool || '').split(',').map(Number);
    var out = box.querySelector('.cs-out'), inp = box.querySelector('.cs-in input'), pr = box.querySelector('.cs-pr');
    var taskEl = box.querySelector('.cs-task'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol');
    var st, T, P, hist = [], hi = 0, last = -1;
    function print(x, cls) { var d = document.createElement('div'); d.className = cls || ''; d.innerHTML = esc(x); out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function newTask() {
      var k; do { k = pool[rnd(0, pool.length - 1)]; } while (pool.length > 1 && k === last); last = k;
      T = TASKS[k]; P = T.gen(); st = fresh();
      taskEl.innerHTML = T.text(P); res.innerHTML = ''; sol.style.display = 'none'; sol.textContent = T.sol(P).join('\n');
      out.innerHTML = ''; print('*** Eltex ESR ***', 'cs-sys'); pr.textContent = prompt(st);
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var v = inp.value; print(prompt(st) + ' ' + v, 'cs-cmd'); if (v.trim()) hist.push(v); hi = hist.length;
        var r = exec(st, v); if (r) print(r, /^%/.test(r) ? 'cs-err' : ''); inp.value = ''; pr.textContent = prompt(st); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { if (hi > 0) { hi--; inp.value = hist[hi]; } e.preventDefault(); }
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
          '<div class="cs-sum ' + (ok === cs.length ? 'ok' : 'no') + '">' + (ok === cs.length ? 'Задание выполнено' : 'Выполнено ' + ok + ' из ' + cs.length) + '</div>'; }
      if (a === 'send') res.innerHTML = '<div class="cs-send">' + T.send(P, st).map(function (x) { return '<div class="' + (x.ok ? 'ok' : 'no') + '"><span class="env">✉</span> ' + esc(x.t) + '</div>'; }).join('') + '</div>';
    });
    newTask();
  }
  window.MON_CLI = { TASKS: TASKS, fresh: fresh, exec: exec, applied: applied };
  document.querySelectorAll('.clisim[data-deck=mon]').forEach(init);
})();
