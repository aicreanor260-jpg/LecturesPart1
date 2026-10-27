/* Консольный сервер Eltex SCS-32 (спецификация sources/eltex/spec/scs.md: РЭ и справочник CLI SCS-32 1.1.0, дерево команд прошивки 1.1.0).
   CLI — ESR (диалект 'scs'): commit/confirm, interface gi/te, ip ssh/telnet server, username. Своё:
   — 32 консольных порта RS-232: line aux 1/0/N → (config-line-aux)#: speed, databits, stopbits, parity, flowcontrol,
     transport input ssh|telnet|none, transport telnet port N, modem inout, description, exec-timeout, login authentication;
     show line aux [1/0/N], clear line aux 1/0/N; no line aux 1/0/N | all;
   — консольный кабель RS-232 (RJ-45 ↔ RJ-45 прямой): aux1/0/N SCS ↔ порт console коммутатора MES или маршрутизатора ESR;
   — Reverse Telnet: telnet <IP SCS> <transport telnet port> (нужен ip telnet server); Reverse SSH: ssh admin:aux1@<IP SCS> (ip ssh server);
     сначала вход на SCS, затем консоль устройства на порту со своим входом; clear line aux обрывает сессию.
   Межсетевого экрана в SCS нет — ip firewall, security zone, security-zone недоступны.
   Упрощения (в источниках нет — помечено): выход из сессии — строкой «~.»; при скорости порта не 115200 вместо консоли идут
   случайные символы (учебное допущение); блок line aux в running-config — по образцу других блоков; transport input по умолчанию
   разрешает telnet и ssh; aux<N> в Reverse SSH = aux 1/0/N; непривилегированный режим «>» и смена пароля при первом входе не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, T = S.T;
  var SPEED = [300, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200], CON = 115200;
  S.PROMPT.aux = '(config-line-aux)#';
  function touch(st) { st.pending = true; }
  // команды только SCS — в начало таблицы (раньше одноимённых ESR)
  function scmd(modes, pat, fn, d) { S.cmd(modes, pat, fn, d); var c = T.pop(); c.dl = ['scs']; T.unshift(c); return c; }
  // у SCS нет межсетевого экрана
  T.forEach(function (c) { if (/\b(firewall|security|security-zone)\b/.test(c.pat.join(' '))) c.xdl = (c.xdl || []).concat('scs'); });
  T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('aux'); });

  // ---------------------------------------------------------------- устройство и порты
  function isScs(d) { return !!d && d.sub === 'scs'; }
  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {};
    if (m.kind === 'scs') {                          // заводская конфигурация (РЭ 5.1.1): gi1/0/1 192.168.1.1/24, остальные порты выключены, SSH включён
      d.sub = 'scs'; var st = d.st; st.dialect = 'scs'; st.aux = m.aux || 32;
      Object.keys(st.cand.ifs).forEach(function (k) { var x = st.cand.ifs[k]; x.fw = false; x.shut = k !== 'gi1/0/1'; });
      st.cand.ifs['gi1/0/1'].ip = '192.168.1.1/24'; st.cand.ssh = true; st.cand.aux = {};
      st.run = EL.clone(st.cand);
    }
    return d;
  };
  var ports0 = P.portsOf;
  P.portsOf = function (d) {
    var L = ports0.call(this, d);
    if (d.type !== 'mes' && d.type !== 'esr') return L;
    if (isScs(d)) for (var i = 1; i <= (d.st.aux || 32); i++) L.push('aux1/0/' + i);
    return L.concat('console');
  };
  function serial(p) { return p === 'console' || /^aux/.test(p); }
  EL.CABLES.rs232 = 'Консольный RS-232 (RJ-45 ↔ RJ-45)';
  var defc0 = P.defaultCable;
  P.defaultCable = function (a, ap, b, bp) { return serial(ap) || serial(bp) ? 'rs232' : defc0.apply(this, arguments); };
  var phys0 = P.phys;
  P.phys = function (id, port) {
    var pr = this.peer(id, port); if (!pr) return phys0.apply(this, arguments);
    var l = this.links[pr.li], cab = l.cab || this.defaultCable(l.a.dev, l.a.port, l.b.dev, l.b.port);
    if (cab !== 'rs232' && !serial(port) && !serial(pr.port)) return phys0.apply(this, arguments);
    if (cab !== 'rs232') return { up: false, why: 'консольный порт — RS-232, нужен консольный кабель', dup: {} };
    if (!serial(port) || !serial(pr.port)) return { up: false, why: 'консольный кабель соединяет порт aux консольного сервера с портом console', dup: {} };
    if (/^aux/.test(port) === /^aux/.test(pr.port)) return { up: false, why: 'консольный кабель: aux ↔ console', dup: {} };
    return { up: true, cab: 'rs232', speed: 0, dup: {} };
  };

  // ---------------------------------------------------------------- line aux
  function auxKeys(st, w) {
    var m = String(w).match(/^(?:aux)?1\/0\/(\d+)(?:-(\d+))?$/); if (!m) return null;
    var a = +m[1], b = m[2] ? +m[2] : a, n = st.aux || 32; if (a < 1 || b > n || b < a) return null;
    var L = []; for (var i = a; i <= b; i++) L.push('1/0/' + i); return L;
  }
  function lines(st) { return (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).map(function (k) { return st.cand.aux[k]; }).filter(Boolean); }
  function each(st, f) { lines(st).forEach(f); touch(st); }
  function sel(list, map) { return function (st, a) { var v = String(a[0]).toLowerCase(); if (list.indexOf(v) < 0) return 'Syntax error: Illegal parameter';
    each(st, function (x) { map(x, v); }); }; }
  scmd('config', 'line aux <w>', function (st, a) { var K = auxKeys(st, a[0]); if (!K) return 'Syntax error: Illegal parameter';
    st.cand.aux = st.cand.aux || {}; K.forEach(function (k) { st.cand.aux[k] = st.cand.aux[k] || {}; }); touch(st); st.mode = 'aux'; st.ctx = K.length > 1 ? K : K[0]; }, 'Консольный порт RS-232 (1/0/1–1/0/32)');
  scmd('config', 'no line aux all', function (st) { st.cand.aux = {}; touch(st); }, 'Сбросить все консольные порты');
  scmd('config', 'no line aux <w>', function (st, a) { var K = auxKeys(st, a[0]); if (!K) return 'Syntax error: Illegal parameter'; K.forEach(function (k) { delete st.cand.aux[k]; }); touch(st); });
  scmd('aux', 'speed <n>', function (st, a) { if (SPEED.indexOf(a[0]) < 0) return 'Syntax error: Illegal parameter'; each(st, function (x) { x.speed = a[0]; }); }, 'Скорость, бит/с (по умолчанию 115200)');
  scmd('aux', 'databits <n>', function (st, a) { if (a[0] < 7 || a[0] > 8) return 'Syntax error: Illegal parameter'; each(st, function (x) { x.databits = a[0]; }); }, 'Биты данных 7–8');
  scmd('aux', 'stopbits <n>', function (st, a) { if (a[0] < 1 || a[0] > 2) return 'Syntax error: Illegal parameter'; each(st, function (x) { x.stopbits = a[0]; }); }, 'Стоповые биты 1–2');
  scmd('aux', 'parity <w>', sel(['odd', 'even', 'none'], function (x, v) { x.parity = v; }), 'Чётность odd | even | none');
  scmd('aux', 'flowcontrol <w>', sel(['software', 'hardware', 'disabled'], function (x, v) { x.flow = v; }), 'Управление потоком');
  scmd('aux', 'transport input <w>', sel(['ssh', 'telnet', 'none'], function (x, v) { x.input = v; }), 'Доступ Reverse SSH / Telnet');
  scmd('aux', 'transport telnet port <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return 'Syntax error: Illegal parameter';
    if (lines(st).some(function (x) { return x.modem; })) return 'Syntax error: Illegal parameter'; each(st, function (x) { x.tport = a[0]; }); }, 'TCP-порт Reverse Telnet');
  scmd('aux', 'modem inout', function (st) { if (lines(st).some(function (x) { return x.tport; })) return 'Syntax error: Illegal parameter'; each(st, function (x) { x.modem = true; }); }, 'Режим модема');
  scmd('aux', 'description <rest>', function (st, a) { each(st, function (x) { x.desc = a[0]; }); }, 'Описание порта');
  scmd('aux', 'exec-timeout <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return 'Syntax error: Illegal parameter'; each(st, function (x) { x.timeout = a[0]; }); }, 'Тайм-аут сессии, мин');
  scmd('aux', 'login authentication <w>', function (st, a) { each(st, function (x) { x.auth = a[0]; }); }, 'Список аутентификации');
  ['speed', 'databits', 'stopbits', 'parity', 'flowcontrol', 'transport input', 'transport telnet port', 'modem inout', 'description', 'exec-timeout', 'login authentication'].forEach(function (k) {
    var f = { speed: 'speed', databits: 'databits', stopbits: 'stopbits', parity: 'parity', flowcontrol: 'flow', 'transport input': 'input', 'transport telnet port': 'tport',
              'modem inout': 'modem', description: 'desc', 'exec-timeout': 'timeout', 'login authentication': 'auth' }[k];
    scmd('aux', 'no ' + k, function (st) { each(st, function (x) { delete x[f]; }); }); });
  scmd('aux', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });

  function auxShow(k, x) { x = x || {};
    return ['AUX Line ' + k, ' Baud rate:           ' + (x.speed || CON), ' Databits:            ' + (x.databits || 8), ' Parity:              ' + (x.parity || 'none').toUpperCase(),
      ' Stopbits:            ' + (x.stopbits || 1), ' Flowcontrol:         ' + ({ software: 'Software', hardware: 'Hardware' }[x.flow] || 'Disabled'),
      ' Timeout Exec (min):  ' + (x.timeout || 30), ' Telnet port:         ' + (x.tport || '--'), ' Modem mode:          ' + (x.modem ? 'Enabled' : 'Disabled')].join('\n'); }
  function keySort(a, b) { return +a.split('/')[2] - +b.split('/')[2]; }
  scmd('priv', 'show line aux', function (st) { var A = st.run.aux || {}; return Object.keys(A).sort(keySort).map(function (k) { return auxShow(k, A[k]); }).join('\n'); }, 'Настройки консольных портов');
  scmd('priv', 'show line aux <w>', function (st, a) { var K = auxKeys(st, a[0]); if (!K) return 'Syntax error: Illegal parameter';
    return K.map(function (k) { return auxShow(k, (st.run.aux || {})[k]); }).join('\n'); });
  scmd('priv', 'clear line aux <w>', function (st, a) { var K = auxKeys(st, a[0]); if (!K) return 'Syntax error: Illegal parameter';
    if (st.net) K.forEach(function (k) { st.net.scsDrop(st.dev, k); }); }, 'Оборвать сессии на консольном порту');
  // show system / show version — формат справочника CLI SCS-32 (с.76–77, с.86)
  function uptime(st) { var d = st.net && st.net.devs[st.dev], s = d ? Math.max(0, Math.floor(st.net.now - (d.boot || 0))) : 0, p2 = function (n) { return ('0' + n).slice(-2); };
    return p2(Math.floor(s / 86400)) + ',' + p2(Math.floor(s / 3600) % 24) + ':' + p2(Math.floor(s / 60) % 60) + ':' + p2(s % 60); }
  scmd('priv', 'show system', function (st) { var mac = EL.mac(st.run.host + 'sys').toUpperCase();
    return ['System type: Eltex SCS-32 Serial Console Server', 'System name: ' + st.run.host, 'Software version: 1.1.0', 'Hardware version: 1v1',
      'System uptime (d,h:m:s): ' + uptime(st), 'System MAC address: ' + mac].join('\n'); }, 'Сведения о системе');
  scmd('priv', 'show version', function () { return 'Boot version:\n  1.1.0\nSW version:\n  1.1.0\nHW version:\n  1v1'; }, 'Версия ПО');
  S.RUNX.push(function (c, o) { Object.keys(c.aux || {}).sort(keySort).forEach(function (k) { var x = c.aux[k], L = ['line aux ' + k];
    if (x.desc) L.push('  description ' + x.desc); if (x.speed) L.push('  speed ' + x.speed); if (x.databits) L.push('  databits ' + x.databits);
    if (x.parity) L.push('  parity ' + x.parity); if (x.stopbits) L.push('  stopbits ' + x.stopbits); if (x.flow) L.push('  flowcontrol ' + x.flow);
    if (x.input) L.push('  transport input ' + x.input); if (x.tport) L.push('  transport telnet port ' + x.tport); if (x.modem) L.push('  modem inout');
    if (x.timeout) L.push('  exec-timeout ' + x.timeout); if (x.auth) L.push('  login authentication ' + x.auth); o.push.apply(o, L.concat('exit')); }); });

  // ---------------------------------------------------------------- Reverse Telnet / SSH
  // SCS слушает: 22 (ip ssh server), 23 и каждый transport telnet port (ip telnet server)
  var lx0 = EL.listensX;
  EL.listensX = function (d, proto, port) {
    if (!isScs(d) || proto !== 'tcp') return lx0 ? lx0(d, proto, port) : undefined;
    var c = d.st.run; if (port === 22) return !!c.ssh;
    if (!c.telnet) return false; if (port === 23) return true;
    return Object.keys(c.aux || {}).some(function (k) { return c.aux[k].tport === port; });
  };
  function devLogin(d, u, p) { var U = d.type === 'esr' ? d.st.run.users : d.st.users;
    if (d.type === 'mes' && !Object.keys(U || {}).length) return u === 'admin' && p === 'admin';
    return !!(U && U[u] && (U[u].pw === p || (U[u].pwEnc && EL.E.hash(p).slice(0, 30) === U[u].pwEnc))); }
  function noise(n) { var s = ''; for (var i = 0; i < n; i++) s += String.fromCharCode(0xa1 + Math.floor(Math.random() * 90)); return s; }
  // hst — состояние Debian; kind: 'telnet' | 'ssh'; key — порт 1/0/N
  P.scsOpen = function (hst, ip, kind, tport, sshUser) {
    var s = this, own = this.owner(ip), d = own && this.devs[own]; if (!isScs(d)) return null;
    var c = d.st.run, key = null, aux = c.aux || {};
    if (kind === 'telnet') key = Object.keys(aux).filter(function (k) { return aux[k].tport === tport; })[0] || null;
    else { var m = String(sshUser.split(':')[1] || '').match(/^aux(\d+)$/); key = m ? '1/0/' + m[1] : null; }
    var r = this.request(hst.dev, ip, 'tcp', kind === 'telnet' ? tport : 22); if (this.onTrace) this.onTrace(r, hst.dev, ip + ':' + (kind === 'telnet' ? tport : 22));
    if (kind === 'telnet' && !r.ok) return 'Trying ' + ip + '...\ntelnet: Unable to connect to remote host: ' + (r.why === 'Connection refused' ? 'Connection refused' : 'Connection timed out');
    if (kind === 'ssh' && !r.ok) return 'ssh: connect to host ' + ip + ' port 22: ' + (r.why === 'Connection refused' ? 'Connection refused' : 'No route to host');
    var x = key && aux[key], allow = x && (!x.input || x.input === kind);
    var user = kind === 'ssh' ? sshUser.split(':')[0] : null;
    var sess = { scs: own, key: key, stage: kind === 'ssh' ? 'pw' : 'user', closed: false };
    function close(msg) { hst.ssh = null; sess.closed = true; return msg; }
    function target() { var pr = key && s.peer(own, 'aux' + key); if (!pr || !s.phys(own, 'aux' + key).up) return null; var t = s.devs[pr.dev]; return t && !t.off ? t : null; }
    function garbled() { var t = target(); return t && (x.speed || CON) !== CON; }
    function devPrompt(t) { return sess.dstage === 'pw' ? 'Password:' : sess.dstage === 'user' ? (t.type === 'mes' ? 'User Name:' : t.st.run.host + ' login: ') : s.prompt(t.id); }
    sess.prompt = function () {
      if (sess.stage === 'user') return d.st.run.host + ' login: ';
      if (sess.stage === 'pw') return kind === 'ssh' ? user + ':aux' + (key || '').split('/')[2] + '@' + ip + "'s password: " : 'Password: ';
      var t = target(); if (!t || garbled()) return '';
      return devPrompt(t);
    };
    sess.exec = function (raw) {
      var line = String(raw);
      if (sess.closed) return close('Connection closed by foreign host.');
      if (/^\s*~\.\s*$/.test(line)) return close(kind === 'ssh' ? 'Connection to ' + ip + ' closed.' : 'Connection closed.');
      if (sess.stage === 'user') { sess.u = line.trim(); sess.stage = 'pw'; return ''; }
      if (sess.stage === 'pw') {
        var u = kind === 'ssh' ? user : sess.u, U = c.users[u];
        if (!U || U.pw !== line.trim()) { if (kind === 'ssh') return close('Permission denied, please try again.'); sess.stage = 'user'; return 'Login incorrect'; }
        if (!x || !allow) return close(kind === 'ssh' ? 'Connection to ' + ip + ' closed.' : 'Connection closed by foreign host.');
        sess.stage = 'con'; sess.dstage = 'user';
        s.scsSess = s.scsSess || []; s.scsSess.push(sess);
        return kind === 'telnet' ? '\n********************************************\n*  Welcome to SCS-32                *\n********************************************\n' : '';
      }
      var t = target(); if (!t) return '';
      if (garbled()) return noise(12 + line.length);
      if (sess.dstage === 'user') { sess.du = line.trim(); sess.dstage = 'pw'; return ''; }
      if (sess.dstage === 'pw') { var ok = devLogin(t, sess.du, line); sess.dstage = ok ? 'cli' : 'user';
        if (!ok) return t.type === 'esr' ? 'Login incorrect' : '% Authentication failed';
        var bn = t.type === 'esr' ? t.st.run.banner : t.st.banner; return bn && bn.exec ? bn.exec : ''; }
      return s.exec(t.id, line);
    };
    hst.ssh = sess;
    return kind === 'telnet' ? 'Trying ' + ip + '...\nConnected to ' + ip + '.\nEscape character is \'^]\'.' : '';
  };
  // clear line aux: оборвать сессии на порту
  P.scsDrop = function (id, key) { (this.scsSess || []).forEach(function (x) { if (x.scs === id && x.key === key) x.closed = true; });
    this.scsSess = (this.scsSess || []).filter(function (x) { return !x.closed; }); };
  // ssh user:auxN@IP — Reverse SSH
  var ssh0 = P.sshOpen;
  P.sshOpen = function (hst, user, ip) {
    if (/:/.test(user)) { var r = this.scsOpen(hst, ip, 'ssh', null, user); if (r !== null) return r; }
    return ssh0.apply(this, arguments);
  };
})(typeof window !== 'undefined' ? window : global);
