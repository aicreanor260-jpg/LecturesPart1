/* AAA: вход на устройство через RADIUS / TACACS+ (справочник ESR 1.23, руководство MES 6.6.8.8).
   ESR: radius-server host A → (config-radius-server)#: key ascii-text СЕКРЕТ; tacacs-server host A → (config-tacacs-server)#: key ascii-text СЕКРЕТ, port N;
     aaa authentication login default|ИМЯ local|radius|tacacs … (по умолчанию default = local); line console|ssh|telnet → login authentication ИМЯ;
     aaa authentication mode chain (по умолчанию: при отказе — следующий метод) | break (следующий — только если сервер недоступен).
   MES 6.x: radius-server host A key K; tacacs-server host A [key K] [port-number N]; aaa authentication login default|ИМЯ МЕТОДЫ (local, radius, tacacs, none);
     line console|ssh|telnet → login authentication ИМЯ.
   Серверы — Debian-server: freeradius (/etc/freeradius/3.0/clients.conf, users — как для 802.1X) и tac_plus (/etc/tacacs+/tac_plus.conf:
     key = СЕКРЕТ, user = ИМЯ { login = cleartext "ПАРОЛЬ" }), systemctl start|restart freeradius | tac_plus.
   Вход по RADIUS/TACACS+ получает привилегии 15 (как admin). Сервер недоступен (нет маршрута, служба не запущена, ключ не совпал) — следующий метод.
   Упрощения: авторизация команд и accounting только хранятся; таймауты и повторы серверов не моделируются (ответ сразу). */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, E = EL.E, P = EL.Net.prototype, H = EL.hosts, IP = EL.ip, CMDS = E.CMDS;
  function touch(st) { st.pending = true; }
  function bad() { return 'Syntax error: Illegal parameter'; }
  S.PROMPT.aradius = '(config-radius-server)#'; S.PROMPT.atacacs = '(config-tacacs-server)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('aradius', 'atacacs'); });
  function A(st) { return st.cand.aaa || (st.cand.aaa = { radius: {}, tacacs: {} }); }
  ['radius', 'tacacs'].forEach(function (k) { var m = k === 'radius' ? 'aradius' : 'atacacs';
    S.cmd('config', k + '-server host <ip>', function (st, a) { var L = A(st)[k]; L[a[0]] = L[a[0]] || {}; st.mode = m; st.ctx = a[0]; touch(st); }, (k === 'radius' ? 'RADIUS' : 'TACACS+') + '-сервер');
    S.cmd('config', 'no ' + k + '-server host <ip>', function (st, a) { delete A(st)[k][a[0]]; touch(st); });
    S.cmd(m, 'key ascii-text <w>', function (st, a) { var n = a[0].length; if (n > 16 || n < (k === 'radius' ? 8 : 1)) return bad(); A(st)[k][st.ctx].key = a[0]; touch(st); }, 'Общий секрет с сервером');
    S.cmd(m, 'no key', function (st) { delete A(st)[k][st.ctx].key; touch(st); });
    S.cmd(m, 'exit', function (st) { st.mode = 'config'; st.ctx = null; }); });
  S.cmd('atacacs', 'port <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return bad(); A(st).tacacs[st.ctx].port = a[0]; touch(st); }, 'TCP-порт (49)');
  S.RUNX.push(function (c, o) { var x = c.aaa; if (!x) return;
    ['radius', 'tacacs'].forEach(function (k) { Object.keys(x[k]).forEach(function (ip) { var s = x[k][ip]; o.push(k + '-server host ' + ip);
      if (s.key) o.push('  key ascii-text ' + s.key); if (s.port) o.push('  port ' + s.port); o.push('exit'); }); }); });
  // MES 6.x
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function MA(st) { return st.aaa2 || (st.aaa2 = { tacacs: {}, lists: {} }); }   // st.aaa — строка базовой настройки (_dk_cli.js)
  mcmd(['6'], 'config', 'tacacs-server host <ip>', function (st, a) { MA(st).tacacs[a[0]] = {}; }, 'TACACS+-сервер');
  mcmd(['6'], 'config', 'tacacs-server host <ip> <rest>', function (st, a) { var w = a[1].trim().split(/\s+/), o = {};
    for (var i = 0; i < w.length; i++) { if (w[i] === 'key') o.key = w[++i]; else if (w[i] === 'port-number') o.port = +w[++i]; else if (w[i] === 'timeout' || w[i] === 'priority' || w[i] === 'vrf') i++; else if (w[i] !== 'single-connection') return '% Invalid input'; }
    MA(st).tacacs[a[0]] = o; });
  mcmd(['6'], 'config', 'no tacacs-server host <ip>', function (st, a) { delete MA(st).tacacs[a[0]]; });
  mcmd(['6'], 'config', 'aaa authentication login <w> <rest>', function (st, a) { var w = a[1].trim().split(/\s+/);
    if (w.some(function (m) { return !/^(enable|line|local|none|radius|tacacs)$/.test(m); })) return '% Invalid input'; MA(st).lists[a[0]] = w; st.aaa = a[0] + ' ' + w.join(' '); }, 'Методы входа: local radius tacacs none');
  mcmd(['6'], 'config', 'no aaa authentication login <w>', function (st, a) { delete MA(st).lists[a[0]]; if (st.aaa && st.aaa.split(' ')[0] === a[0]) st.aaa = null; });
  // линия: line console|ssh|telnet → login authentication ИМЯ — команда базовой настройки (_dk_cli.js), хранится в st.line[…].auth
  E.RUNX.push(function (st, o) { var x = st.aaa2; if (!x) return;
    Object.keys(x.tacacs).forEach(function (ip) { var s = x.tacacs[ip]; o.push('tacacs-server host ' + ip + (s.key ? ' key ' + s.key : '') + (s.port ? ' port-number ' + s.port : '')); });
    Object.keys(x.lists).forEach(function (n) { var l = n + ' ' + x.lists[n].join(' '); if (l !== st.aaa) o.push('aaa authentication login ' + l); });   // последний список печатает базовая настройка
  });

  // ---------------------------------------------------------------- серверы на Debian
  function srvFile(st, f) { return ((st.files || {})[f]) || ''; }
  function radius(s, srv, nasIp, key, u, p) {
    var st = srv.st; if (!st.svc || !st.svc.freeradius) return { down: 'freeradius не запущен' };
    var cl = srvFile(st, '/etc/freeradius/3.0/clients.conf'), ok = false, re = /client\s+\S+\s*\{([^}]*)\}/g, m;
    while ((m = re.exec(cl))) { var ip = (m[1].match(/ipaddr\s*=\s*(\S+)/) || [])[1], sec = (m[1].match(/secret\s*=\s*(\S+)/) || [])[1], c = ip && (ip.indexOf('/') > 0 ? IP.parseCidr(ip) : { ip: ip, len: 32 });
      if (c && IP.sameNet(nasIp, c.ip, c.len) && sec === key) ok = true; }
    if (!ok) return { down: 'устройство ' + nasIp + ' не описано в clients.conf или secret не совпадает' };
    var hit = srvFile(st, '/etc/freeradius/3.0/users').split('\n').map(function (l) { return l.match(/^\s*"?([^\s"#]+)"?\s+Cleartext-Password\s*:=\s*"([^"]*)"/); }).filter(Boolean).filter(function (x) { return x[1] === u; })[0];
    return hit && hit[2] === p ? { ok: true } : { reject: hit ? 'неверный пароль' : 'нет пользователя ' + u };
  }
  function tacacs(s, srv, key, u, p) {
    var st = srv.st; if (!st.svc || !st.svc.tac_plus) return { down: 'tac_plus не запущен' };
    var f = srvFile(st, '/etc/tacacs+/tac_plus.conf'), k = (f.match(/^\s*key\s*=\s*"?([^"\n]+?)"?\s*$/m) || [])[1];
    if (k !== key) return { down: 'ключ не совпадает с key в tac_plus.conf' };
    var re = /user\s*=\s*(\S+)\s*\{([^}]*)\}/g, m, hit = null; while ((m = re.exec(f))) if (m[1] === u) hit = m[2];
    if (!hit) return { reject: 'нет пользователя ' + u };
    var pw = (hit.match(/login\s*=\s*cleartext\s+"?([^"\s]+)"?/) || [])[1]; return pw === p ? { ok: true } : { reject: 'неверный пароль' };
  }
  function ask(s, id, kind, ip, cfg, u, p) {        // запрос к серверу: связь + проверка
    var r = s.request(id, ip, kind === 'radius' ? 'udp' : 'tcp', kind === 'radius' ? 1812 : (cfg.port || 49));
    if (!r.ok) return { down: (kind === 'radius' ? 'RADIUS' : 'TACACS+') + '-сервер ' + ip + ' недоступен' };
    var srv = s.devs[r.dev]; if (!srv || srv.type !== 'deb') return { down: 'на ' + ip + ' нет сервера' };
    var nas = (s.ifaces(id).filter(function (f) { return IP.sameNet(f.ip, ip, f.len); })[0] || s.ifaces(id)[0] || {}).ip;
    return kind === 'radius' ? radius(s, srv, nas, cfg.key || '', u, p) : tacacs(s, srv, cfg.key || '', u, p);
  }
  var lx0 = EL.listensX;
  EL.listensX = function (d, proto, port) {
    if (d.type === 'deb' && proto === 'udp' && port === 1812) return !!(d.st.svc || {}).freeradius;
    if (d.type === 'deb' && proto === 'tcp' && port === 49) return !!(d.st.svc || {}).tac_plus;
    return lx0 ? lx0(d, proto, port) : undefined; };
  var debF = H.deb; H.deb = function (name, o) { var st = debF.apply(this, arguments); if (st.svc && o && o.web) { st.svc.tac_plus = false;
    st.files['/etc/tacacs+/tac_plus.conf'] = 'key = testing123\n\n# user = ИМЯ {\n#     login = cleartext "ПАРОЛЬ"\n# }\n'; } return st; };

  // ---------------------------------------------------------------- проверка входа: {ok, method, log[]} — null, если AAA не настроен (обычная проверка)
  P.aaaLogin = function (id, line, u, p, local) {
    var s = this, d = s.devs[id], log = [], methods, servers, chain = true;
    if (d.type === 'esr' && d.sub !== 'me') { var c = d.st.run, sp = c.secp || { L: {}, B: {} }, lb = (sp.B['line ' + line] || {})['login authentication'];
      var name = lb ? lb.split(' ').pop() : 'default', def = sp.L['aaa authentication login ' + name];
      methods = def ? def.split(' ').slice(4) : (name === 'default' ? ['local'] : null); if (!methods) return null;
      chain = !/break/.test(sp.L['aaa authentication mode'] || ''); servers = c.aaa || { radius: {}, tacacs: {} }; }
    else if (d.type === 'mes' && d.st.dialect === '6' && d.st.aaa2) { var x = d.st.aaa2, nm = ((d.st.line || {})[line] || {}).auth || 'default'; methods = x.lists[nm]; if (!methods) return null;
      var rd = {}; ((d.st.dot1x || {}).radius || []).forEach(function (r) { rd[r.ip] = { key: r.key }; }); servers = { radius: rd, tacacs: x.tacacs }; }
    else return null;
    if (methods.length === 1 && methods[0] === 'local') return null;
    for (var i = 0; i < methods.length; i++) { var m = methods[i], res = null;
      if (m === 'none') return { ok: true, method: 'none', log: log };
      if (m === 'local') { res = local(u, p) ? { ok: true } : { reject: 'нет такого локального пользователя или неверный пароль' }; }
      if (m === 'line' && d.type === 'mes') { var lp = ((d.st.line || {})[line] || {}).pw; res = lp ? (p === lp ? { ok: true } : { reject: 'неверный пароль линии' }) : { down: 'пароль линии не задан' }; }
      if (m === 'enable' && d.type === 'mes') { var ep = d.st.enablePw || d.st.enable; res = ep ? (p === ep ? { ok: true } : { reject: 'неверный пароль enable' }) : { down: 'пароль enable не задан' }; }
      if (m === 'radius' || m === 'tacacs') { var L = Object.keys(servers[m] || {}); res = { down: 'серверы ' + m + ' не заданы' };
        for (var j = 0; j < L.length; j++) { res = ask(s, id, m, L[j], servers[m][L[j]], u, p); log.push(m + ' ' + L[j] + ': ' + (res.ok ? 'Access-Accept' : res.reject ? 'Access-Reject (' + res.reject + ')' : res.down)); if (!res.down) break; } }
      if (!res) continue;
      if (res.ok) return { ok: true, method: m, log: log };
      if (res.reject && !chain) return { ok: false, method: m, log: log };     // break: отказ — окончательно
    }
    return { ok: false, log: log };
  };
})(typeof window !== 'undefined' ? window : global);
