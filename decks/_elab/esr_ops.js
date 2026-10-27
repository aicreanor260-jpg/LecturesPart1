/* ESR для лаб 10.1, 10.2, 10.4: LLDP, отправка syslog на сервер, копирование конфигурации на TFTP и архив по commit.
   MES для лабы 10.3: зеркалирование портов (monitor session). */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, S = EL.esr, cmd = S.cmd, E = EL.E;
  function touch(st) { st.pending = true; }
  S.PROMPT.slog = '(config-syslog-host)#'; S.PROMPT.arch = '(config-archive)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('slog', 'arch'); });
  cmd('slog arch', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });

  // ---------------------------------------------------------------- LLDP
  cmd('config', 'lldp enable', function (st) { st.cand.lldp = true; touch(st); }, 'Включить LLDP');
  cmd('config', 'no lldp enable', function (st) { st.cand.lldp = false; touch(st); });
  function each(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }
  cmd('gi', 'lldp receive', function (st) { each(st, function (x) { x.lldpRx = true; }); }, 'Принимать LLDPDU');
  cmd('gi', 'no lldp receive', function (st) { each(st, function (x) { x.lldpRx = false; }); });
  cmd('gi', 'lldp transmit', function (st) { each(st, function (x) { x.lldpTx = true; }); }, 'Рассылать LLDPDU');
  cmd('gi', 'no lldp transmit', function (st) { each(st, function (x) { x.lldpTx = false; }); });
  cmd('priv', 'show lldp neighbors', function (st) { return st.net ? st.net.lldpText(st.dev) : ''; }, 'Соседи LLDP');
  cmd('priv', 'show system', function (st) { return 'System type:           Eltex vESR Virtual Service Router\nSystem name:           ' + st.run.host +
    '\nSoftware version:      1.24.2\nSystem MAC address:    ' + EL.mac(st.run.host + 'sys') + '\nSerial number:         VESRA' + EL.E.hash(st.dev || 'x').slice(0, 6).toUpperCase(); }, 'Сведения о системе');

  // ---------------------------------------------------------------- syslog
  function hosts(st) { return st.cand.syslog || (st.cand.syslog = {}); }
  cmd('config', 'syslog host <w>', function (st, a) { var H = hosts(st); if (!H[a[0]]) H[a[0]] = { src: null, ip: null, proto: 'udp', port: 514, sev: 'info' };
    touch(st); st.mode = 'slog'; st.ctx = a[0]; }, 'Удалённый syslog-сервер');
  cmd('config', 'no syslog host <w>', function (st, a) { delete hosts(st)[a[0]]; touch(st); });
  function h(st) { return st.cand.syslog[st.ctx]; }
  cmd('slog', 'source-address <ip>', function (st, a) { h(st).src = a[0]; touch(st); }, 'Адрес источника');
  cmd('slog', 'remote-address <ip>', function (st, a) { h(st).ip = a[0]; touch(st); }, 'Адрес сервера');
  cmd('slog', 'transport <w>', function (st, a) { var t = a[0].toLowerCase(); if (t !== 'udp' && t !== 'tcp') return '% udp | tcp'; h(st).proto = t; touch(st); }, 'Транспорт');
  cmd('slog', 'port <n>', function (st, a) { h(st).port = a[0]; touch(st); }, 'Порт');
  cmd('slog', 'severity <w>', function (st, a) { var L = ['emerg', 'alert', 'crit', 'error', 'warning', 'notice', 'info', 'debug'];
    if (L.indexOf(a[0].toLowerCase()) < 0) return '% Уровень: ' + L.join(' | '); h(st).sev = a[0].toLowerCase(); touch(st); }, 'Минимальная важность');

  // ---------------------------------------------------------------- TFTP: copy и archive
  function tftp(url) { var m = String(url).match(/^tftp:\/\/(\d+\.\d+\.\d+\.\d+):?\/(.+)$/); return m ? { ip: m[1], file: m[2] } : null; }
  cmd('priv', 'copy <w> <w>', function (st, a) {
    var src = a[0].toLowerCase(), dst = tftp(a[1]);
    if (src !== 'system:running-config' && src !== 'running-config') return '% Источник: system:running-config';
    if (!dst) return '% Назначение: tftp://A.B.C.D:/имя_файла';
    if (!st.net) return '';
    var r = st.net.tftpPut(st.dev, dst.ip, dst.file, S.showRun(st));
    return r.ok ? '|******************************************| 100% (' + r.size + 'B)\nSuccess!' : '% Ошибка передачи по TFTP: ' + r.why; }, 'Копировать конфигурацию');
  cmd('config', 'archive', function (st) { st.cand.archive = st.cand.archive || { type: 'local', path: null, byCommit: false }; touch(st); st.mode = 'arch'; }, 'Архив конфигураций');
  cmd('arch', 'type <w>', function (st, a) { var t = a[0].toLowerCase(); if (t !== 'remote' && t !== 'local') return '% local | remote'; st.cand.archive.type = t; touch(st); }, 'Где хранить');
  cmd('arch', 'path <w>', function (st, a) { if (!tftp(a[0])) return '% Формат: tftp://A.B.C.D:/имя_файла'; st.cand.archive.path = a[0]; touch(st); }, 'Путь на сервере');
  cmd('arch', 'by-commit', function (st) { st.cand.archive.byCommit = true; touch(st); }, 'Сохранять при каждом commit');
  cmd('arch', 'no by-commit', function (st) { st.cand.archive.byCommit = false; touch(st); });
  EL.tftpUrl = tftp;

  S.RUNX.push(function (c, o) {
    if (c.lldp) o.push('lldp enable');
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k], d = [];
      if (x.lldpRx) d.push('  lldp receive'); if (x.lldpTx) d.push('  lldp transmit');
      if (d.length) o.push('interface ' + S.longIf(k), d.join('\n'), 'exit'); });
    Object.keys(c.syslog || {}).forEach(function (n) { var x = c.syslog[n]; o.push('syslog host ' + n);
      if (x.src) o.push('  source-address ' + x.src); if (x.ip) o.push('  remote-address ' + x.ip);
      o.push('  transport ' + x.proto, '  port ' + x.port, '  severity ' + x.sev, 'exit'); });
    if (c.archive) { o.push('archive', '  type ' + c.archive.type); if (c.archive.path) o.push('  path ' + c.archive.path); if (c.archive.byCommit) o.push('  by-commit'); o.push('exit'); }
  });

  // ---------------------------------------------------------------- MES: зеркалирование портов
  function ms(st) { return st.mon || (st.mon = {}); }
  E.cmd('config', 'monitor session <n> destination interface <if>', function (st, a) {
    if (a[0] < 1 || a[0] > 4) return '% Номер сессии 1–4'; if (!st.ports[a[1][0]]) return '% Такого порта нет на устройстве';
    var m = ms(st); m[a[0]] = m[a[0]] || { src: {} }; m[a[0]].dst = a[1][0]; });
  E.cmd('config', 'monitor session <n> source interface <if>', function (st, a) { return addSrc(st, a[0], a[1], 'both'); });
  E.cmd('config', 'monitor session <n> source interface <if> <w>', function (st, a) {
    var d = a[2].toLowerCase(); if (['rx', 'tx', 'both'].indexOf(d) < 0) return '% Направление: rx | tx | both'; return addSrc(st, a[0], a[1], d); });
  function addSrc(st, n, ports, dir) {
    if (n < 1 || n > 4) return '% Номер сессии 1–4';
    if (ports.some(function (k) { return !st.ports[k]; })) return '% Такого порта нет на устройстве';
    var m = ms(st); m[n] = m[n] || { src: {} }; ports.forEach(function (k) { m[n].src[k] = dir; });
  }
  E.cmd('config', 'no monitor session <n>', function (st, a) { delete ms(st)[a[0]]; });
  function showMon(st, n) { var m = (st.mon || {})[n];
    if (!m) return '% Сессия ' + n + ' не настроена';
    return 'Session ' + n + '\n  Destination port: ' + (m.dst || '-') + '\n  Source ports:\n' +
      Object.keys(m.src).map(function (k) { return '    ' + k + '  ' + m.src[k]; }).join('\n'); }
  E.cmd('priv', 'show monitor session <n>', function (st, a) { return showMon(st, a[0]); });
  E.cmd(E.CFG, 'do show monitor session <n>', function (st, a) { return showMon(st, a[0]); });
})(typeof window !== 'undefined' ? window : global);
