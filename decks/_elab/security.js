/* Безопасная настройка ESR (спецификация sources/eltex/spec/esr-fstec.md: РЭ ESR 1.5.10 гл. 6 «Рекомендации по безопасной настройке»,
   справочник CLI 1.5.10, деревья команд прошивок ESR 1.30/1.40 и 1.5.10 ФСТЭК) — для всех ESR и для межсетевых экранов ESR ФСТЭК.
   Парольная политика: security passwords default-expired | lifetime | history | min-length | max-length (1–32) | upper-case | lower-case |
   numeric-count | special-case | symbol-types — новый пароль пользователя проверяется (длина и классы символов).
   AAA: aaa authentication login|enable <ИМЯ> <методы>, aaa authentication mode, attempts max-fail, aaa accounting …, line console|ssh|telnet →
   login authentication, enable authentication, exec-timeout. Журналы: logging userinfo, logging aaa configuration, syslog cli-commands,
   syslog file <ФАЙЛ> → (config-syslog-file)# severity, syslog max-files | file-size | sequence-numbers. SSH: ip ssh <группа> algorithm X disable,
   update ssh-host-key. Защита от атак: ip firewall screen spy-blocking | suspicious-packets | dos-defense …, logging firewall screen …
   Целостность: verify filesystem. ФСТЭК (диалект 'fstec', ПО 1.5.10): нет веб-интерфейса, WLC и встроенного RADIUS; только там —
   match [not] http|ftp command … в правиле зоны, ip|ipv6 firewall screen flow-spec, logging firewall screen flow-spec; show version — 1.5.10(FSTEC).
   Упрощения (в источниках нет): текст ошибки при нарушении парольной политики — общий «Syntax error: Illegal parameter»; методы AAA radius/tacacs/ldap
   хранятся (серверов нет — вход локальный); смена пароля при первом входе (default-expired), блокировка подбора и ротация журналов не моделируются;
   экраны spy-blocking/suspicious-packets хранятся (в модели не бывает таких пакетов); match http/ftp command хранится — что проверяется в трафике, в источниках нет. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, T = S.T;
  function touch(st) { st.pending = true; }
  function scmd(modes, pat, fn, d, dl) { S.cmd(modes, pat, fn, d); var c = T.pop(); if (dl) c.dl = dl; T.unshift(c); return c; }
  var PR = { lcon: '(config-line-console)#', lssh: '(config-line-ssh)#', ltel: '(config-line-telnet)#', slf: '(config-syslog-file)#', ogapp: '(config-object-group-application)#' };
  Object.keys(PR).forEach(function (k) { S.PROMPT[k] = PR[k]; });
  T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') Object.keys(PR).forEach(function (k) { c.modes.push(k); }); });
  // строки конфигурации безопасности: ключ → строка (в порядке ввода), блоки — {header: [строки]}
  function sec(st) { return st.cand.secp || (st.cand.secp = { L: {}, B: {} }); }
  function line(pat, key) { return function (st, a) { var t = pat.split(' '), i = 0; var l = t.map(function (w) { return /^</.test(w) ? a[i++] : w; }).join(' ');
    sec(st).L[key || l] = l; touch(st); }; }
  function no(key) { return function (st) { var L = sec(st).L; Object.keys(L).forEach(function (k) { if (k === key || k.indexOf(key + ' ') === 0) delete L[k]; }); touch(st); }; }
  var PW = { lifetime: [1, 365], history: [1, 15], 'min-length': [1, 32], 'max-length': [1, 32], 'lower-case': [0, 32], 'upper-case': [0, 32], 'numeric-count': [0, 32], 'special-case': [0, 32], 'symbol-types': [1, 4] };
  scmd('config', 'security passwords default-expired', line('security passwords default-expired'), 'Сменить пароль по умолчанию при первом входе');
  scmd('config', 'no security passwords default-expired', no('security passwords default-expired'));
  Object.keys(PW).forEach(function (k) {
    scmd('config', 'security passwords ' + k + ' <n>', function (st, a) { if (a[0] < PW[k][0] || a[0] > PW[k][1]) return 'Syntax error: Illegal parameter';
      sec(st).L['security passwords ' + k] = 'security passwords ' + k + ' ' + a[0]; touch(st); }, 'Парольная политика: ' + k);
    scmd('config', 'no security passwords ' + k, no('security passwords ' + k)); });
  // проверка пароля по политике (действующей конфигурации)
  function pol(st, k) { var l = (st.run.secp || { L: {} }).L['security passwords ' + k]; return l ? +l.split(' ').pop() : null; }
  EL.pwCheck = function (st, pw) {
    var n = function (re) { return (pw.match(re) || []).length; }, c = { 'upper-case': n(/[A-Z]/g), 'lower-case': n(/[a-z]/g), 'numeric-count': n(/[0-9]/g), 'special-case': n(/[^A-Za-z0-9]/g) };
    if (pol(st, 'min-length') && pw.length < pol(st, 'min-length')) return false; if (pol(st, 'max-length') && pw.length > pol(st, 'max-length')) return false;
    if (Object.keys(c).some(function (k) { return pol(st, k) && c[k] < pol(st, k); })) return false;
    var types = Object.keys(c).filter(function (k) { return c[k] > 0; }).length; return !(pol(st, 'symbol-types') && types < pol(st, 'symbol-types'));
  };
  T.filter(function (c) { return c.modes.indexOf('user') >= 0 && c.pat.join(' ') === 'password <w>'; }).forEach(function (c) { var r0 = c.run;
    c.run = function (st, a) { if (!EL.pwCheck(st, String(a[0]))) return 'Syntax error: Illegal parameter'; return r0.apply(this, arguments); }; });
  // AAA, журналы, SSH, экраны — строки конфигурации
  [['aaa authentication login <w> <rest>', 'aaa authentication login'], ['aaa authentication enable <w> <rest>', 'aaa authentication enable'], ['aaa authentication mode <w>', 'aaa authentication mode'],
   ['aaa authentication attempts max-fail <n> <n>', 'aaa authentication attempts'], ['aaa accounting commands stop-only <w>', 'aaa accounting commands'],
   ['aaa accounting login start-stop <w>', 'aaa accounting login'], ['aaa authorization commands <w> <rest>', 'aaa authorization commands'],
   ['enable password <w>', 'enable password'], ['syslog max-files <n>', 'syslog max-files'], ['syslog file-size <n>', 'syslog file-size'],
   ['ip firewall screen dos-defense icmp-threshold <n>', 'ip firewall screen dos-defense icmp-threshold'], ['ip firewall sessions unknown <w>', 'ip firewall sessions unknown'],
   ['ip firewall mode <w>', 'ip firewall mode'], ['privilege <w> level <n> <rest>', null], ['system config-confirm timeout <n>', 'system config-confirm timeout'],
   ['ip firewall screen spy-blocking spoofing exclude <w>', null]].forEach(function (x) {
    scmd('config', x[0], function (st, a, l) { var k = x[1] === null ? l : x[1] + (/ (login|enable) /.test(x[0]) ? ' ' + a[0] : ''); sec(st).L[k] = l; touch(st); });
    if (x[1]) scmd('config', 'no ' + x[1], no(x[1])); });
  ['logging userinfo', 'logging aaa configuration', 'syslog cli-commands', 'syslog sequence-numbers', 'ip firewall screen dos-defense land'].concat(
    ['spoofing', 'syn-fin', 'fin-no-ack', 'tcp-no-flag', 'tcp-all-flags'].map(function (k) { return 'spy-blocking ' + k; }).concat(['icmp-fragment', 'large-icmp', 'unknown-protocols'].map(function (k) { return 'suspicious-packets ' + k; }))
      .reduce(function (o, k) { return o.concat('ip firewall screen ' + k, 'logging firewall screen ' + k); }, [])).forEach(function (p) {
    scmd('config', p, line(p)); scmd('config', 'no ' + p, no(p)); });
  ['authentication', 'encryption', 'key-exchange', 'host-key'].forEach(function (g) {
    scmd('config', 'ip ssh ' + g + ' algorithm <w> disable', line('ip ssh ' + g + ' algorithm <w> disable'), 'Отключить алгоритм SSH');
    scmd('config', 'no ip ssh ' + g + ' algorithm <w> disable', function (st, a) { delete sec(st).L['ip ssh ' + g + ' algorithm ' + a[0] + ' disable']; touch(st); }); });
  // блоки: line console|ssh|telnet, syslog file, object-group application
  function blk(mode, hdr) { return function (st, a) { var h = hdr(a), B = sec(st).B; B[h] = B[h] || {}; touch(st); st.mode = mode; st.ctx = h; }; }
  [['console', 'lcon'], ['ssh', 'lssh'], ['telnet', 'ltel']].forEach(function (x) { scmd('config', 'line ' + x[0], blk(x[1], function () { return 'line ' + x[0]; }), 'Терминальная линия ' + x[0]); });
  scmd('config', 'syslog file <w>', blk('slf', function (a) { return 'syslog file ' + a[0]; }), 'Журнал в файл (tmpsys:…)');
  scmd('config', 'object-group application <w>', blk('ogapp', function (a) { return 'object-group application ' + a[0]; }));
  function bset(key) { return function (st, a, l) { sec(st).B[st.ctx][key] = l; touch(st); }; }
  ['login authentication <w>', 'enable authentication <w>', 'commands authorization <w>', 'exec-timeout <n>'].forEach(function (p) { scmd('lcon lssh ltel', p, bset(p.split(' <')[0])); });
  scmd('slf', 'severity <w>', bset('severity')); scmd('slf', 'match process-name <w>', bset('match process-name')); scmd('ogapp', 'application <w>', function (st, a, l) { sec(st).B[st.ctx][l] = l; touch(st); });
  scmd('lcon lssh ltel slf ogapp', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  // ФСТЭК: правила по командам HTTP/FTP, flow-spec
  function zr(st) { var p = (st.cand.zp || {})[st.zpKey]; return p && p.rules[st.zrN]; }
  ['http', 'ftp'].forEach(function (pr) { (pr === 'http' ? ['get', 'post', 'head', 'put'] : ['get', 'put', 'rmdir', 'mkdir', 'delete']).forEach(function (c) {
    ['', 'not '].forEach(function (ng) { var p = 'match ' + ng + pr + ' command ' + c;
      scmd('zrule', p, function (st) { var r = zr(st); if (!r) return; r.cmds = r.cmds || []; if (r.cmds.indexOf(p) < 0) r.cmds.push(p); touch(st); }, 'Проверка команды ' + pr.toUpperCase() + ' (только ПО ФСТЭК)', ['fstec']);
      scmd('zrule', 'no ' + p, function (st) { var r = zr(st); if (r && r.cmds) r.cmds = r.cmds.filter(function (x) { return x !== p; }); touch(st); }, null, ['fstec']); }); }); });
  ['ip firewall screen flow-spec', 'ipv6 firewall screen flow-spec', 'logging firewall screen flow-spec'].forEach(function (p) { scmd('config', p, line(p), 'Экран по BGP flow-spec (ПО ФСТЭК)', ['fstec']); scmd('config', 'no ' + p, no(p), null, ['fstec']); });
  // просмотр и служебные
  scmd('priv', 'verify filesystem', function () { return 'Filesystem Successfully Verified'; }, 'Проверка целостности файловой системы');
  scmd('priv', 'verify filesystem detailed', function () { return 'Filesystem Successfully Verified'; });
  ['rsa', 'dsa', 'ed25519'].forEach(function (k) { scmd('priv', 'update ssh-host-key ' + k, function () { return ''; }, 'Перегенерировать ключ SSH-сервера'); });
  scmd('priv', 'update ssh-host-key rsa <n>', function () { return ''; }); scmd('priv', 'update ssh-host-key ecdsa <n>', function () { return ''; });
  scmd('priv', 'show users accounts', function (st) { var U = st.run.users || {}; return ['Name                 Privilege', '-------------------- ---------'].concat(Object.keys(U).map(function (u) { return (u + '                     ').slice(0, 21) + U[u].priv; })).join('\n'); }, 'Учётные записи');
  scmd('priv', 'show users blocked', function () { return ''; }, 'Заблокированные после неудачных входов');
  scmd('priv', 'show aaa authentication', function (st) { var L = (st.run.secp || { L: {} }).L; return Object.keys(L).filter(function (k) { return /^aaa /.test(k); }).map(function (k) { return L[k]; }).join('\n'); });
  scmd('priv', 'show syslog configuration', function (st) { var s = st.run.secp || { L: {}, B: {} }; return Object.keys(s.L).filter(function (k) { return /^syslog|^logging/.test(k); }).map(function (k) { return s.L[k]; })
    .concat(Object.keys(s.B).filter(function (h) { return /^syslog file/.test(h); })).join('\n'); });
  // show version ФСТЭК: 1.5.10(FSTEC) build … (FU 1.5.10: build 9 — ESR-15R, остальные 11)
  scmd('priv', 'show version', function (st) { var d = st.net && st.net.devs[st.dev], b = d && /15R/.test(d.model) ? 9 : 11, v = '1.5.10(FSTEC) build ' + b;
    return 'Boot version:\n  ' + v + '\nSW version (active):\n  ' + v + '\nSW version (inactive):\n  ' + v; }, 'Версия ПО', ['fstec']);
  // ESR ФСТЭК: диалект 'fstec' (нет команд WLC и встроенного RADIUS — они только в диалекте 'wlc')
  var P = EL.Net.prototype, add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}; if (m.kind === 'fstec') { d.sub = 'fstec'; d.st.dialect = 'fstec'; } return d; };
  // running-config
  S.RUNX.push(function (c, o) { var s = c.secp; if (s) { Object.keys(s.L).forEach(function (k) { o.push(s.L[k]); });
      Object.keys(s.B).forEach(function (h) { o.push(h); Object.keys(s.B[h]).forEach(function (k) { o.push('  ' + s.B[h][k]); }); o.push('exit'); }); }
    // match http|ftp command — внутрь своего правила, перед enable
    Object.keys(c.zp || {}).forEach(function (k) { var zpx = c.zp[k], i = o.indexOf('security zone-pair ' + zpx.from + ' ' + zpx.to); if (i < 0) return;
      Object.keys(zpx.rules).forEach(function (n) { var r = zpx.rules[n]; if (!r.cmds || !r.cmds.length) return; var j = o.indexOf('  rule ' + n, i); if (j < 0) return;
        var e = j + 1; while (e < o.length && o[e] !== '    enable' && o[e] !== '  exit') e++; o.splice.apply(o, [e, 0].concat(r.cmds.map(function (l) { return '    ' + l; }))); }); }); });
})(typeof window !== 'undefined' ? window : global);
