/* 802.1X на MES (руководства 10.4.6 и 6.6.8.8): dot1x system-auth-control; на порту dot1x port-control auto | force-authorized | force-unauthorized
   (по умолчанию force-authorized), dot1x host-mode; база: 10.x — aaa authentication dot1x default group radius | local (по умолчанию local),
   6.x — aaa authentication dot1x default radius | none (по умолчанию radius); radius-server host A.B.C.D key K; show dot1x interface gi1/0/1.
   Клиент — Debian: wpa_supplicant -B -D wired -i ens3 -c /etc/wpa_supplicant/wired.conf (identity / password в конфиге).
   RADIUS-сервер — Debian-server с freeradius: /etc/freeradius/3.0/clients.conf (client … { ipaddr, secret }), /etc/freeradius/3.0/users
   (имя Cleartext-Password := "пароль"), systemctl restart freeradius.
   Неавторизованный порт (auto) пропускает только EAPOL — остальные кадры отбрасываются (видно в трассе). VPC 802.1X не умеет.
   Упрощения: EAP-методы, таймеры повторной аутентификации, guest VLAN, MAC-аутентификация не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, P = EL.Net.prototype, CMDS = E.CMDS, H = EL.hosts, IP = EL.ip;
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k]; }).filter(Boolean) : null; }
  function each(st, f) { var p = ports(st); if (!p) return '% Команда доступна в настройке порта'; p.forEach(f); }
  function X(st) { return st.dot1x || (st.dot1x = { on: false, method: null, radius: [] }); }
  var D = ['10', '6'];
  mcmd(D, 'config', 'dot1x system-auth-control', function (st) { X(st).on = true; }, 'Включить 802.1X на коммутаторе');
  mcmd(D, 'config', 'no dot1x system-auth-control', function (st) { X(st).on = false; });
  mcmd(['10'], 'config', 'aaa authentication dot1x default group radius', function (st) { X(st).method = 'radius'; }, 'Проверять клиентов на RADIUS');
  mcmd(['10'], 'config', 'aaa authentication dot1x default local', function (st) { X(st).method = 'local'; }, 'Проверять по локальным пользователям');
  mcmd(['6'], 'config', 'aaa authentication dot1x default <w>', function (st, a) { if (a[0] !== 'radius' && a[0] !== 'none') return '% Invalid input'; X(st).method = a[0]; }, 'radius | none');
  mcmd(D, 'config', 'no aaa authentication dot1x default', function (st) { X(st).method = null; });
  function addR(st, ip, key) { var L = X(st).radius.filter(function (r) { return r.ip !== ip; }); L.push({ ip: ip, key: key || '' }); X(st).radius = L; }
  mcmd(D, 'config', 'radius-server host <ip>', function (st, a) { addR(st, a[0]); }, 'RADIUS-сервер');
  mcmd(D, 'config', 'radius-server host <ip> key <w>', function (st, a) { addR(st, a[0], a[1]); });
  mcmd(D, 'config', 'no radius-server host <ip>', function (st, a) { X(st).radius = X(st).radius.filter(function (r) { return r.ip !== a[0]; }); });
  mcmd(D, 'if range', 'dot1x port-control <w>', function (st, a) { if (['auto', 'force-authorized', 'force-unauthorized'].indexOf(a[0]) < 0) return '% Invalid input';
    return each(st, function (p) { p.dot1x = a[0]; }); }, 'Режим 802.1X порта');
  mcmd(D, 'if range', 'no dot1x port-control', function (st) { return each(st, function (p) { delete p.dot1x; }); });
  mcmd(D, 'if range', 'dot1x host-mode <w>', function (st, a) { return each(st, function (p) { p.dot1xHost = a[0]; }); }, 'multi-host | multi-session');
  E.RUNX.push(function (st, o) { var x = st.dot1x; if (!x) return;
    x.radius.forEach(function (r) { o.push('radius-server host ' + r.ip + (r.key ? ' key ' + r.key : '')); });
    if (x.method) o.push(st.dialect === '6' ? 'aaa authentication dot1x default ' + x.method : 'aaa authentication dot1x default ' + (x.method === 'radius' ? 'group radius' : 'local'));
    if (x.on) o.push('dot1x system-auth-control'); });
  E.PORTX.push(function (st, k, p, d) { if (p.dot1x) d.push(' dot1x port-control ' + p.dot1x); if (p.dot1xHost) d.push(' dot1x host-mode ' + p.dot1xHost); });

  // ---------------------------------------------------------------- клиент и RADIUS-сервер на Debian
  var deb0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    var line = String(raw).trim();
    if (!st.user || st.ssh) return deb0.apply(this, arguments);
    var m = line.match(/^wpa_supplicant\s+(.*)$/);
    if (m) { if (st.user !== 'root') return 'Could not open control interface: Operation not permitted';
      var c = (m[1].match(/-c\s*(\S+)/) || [])[1], i = (m[1].match(/-i\s*(\S+)/) || [])[1];
      if (i !== 'ens3') return 'Could not read interface ' + (i || '') + ' flags: No such device';
      var f = c && (st.files || {})[c]; if (f === undefined) return "Failed to open config file '" + (c || '') + "', error: No such file or directory";
      var id = (f.match(/identity\s*=\s*"([^"]*)"/) || [])[1], pw = (f.match(/password\s*=\s*"([^"]*)"/) || [])[1];
      if (!id) return 'Line 1: missing identity'; st.wpa = { id: id, pw: pw || '' }; if (st.net) st.net.gen++;
      return /-B/.test(m[1]) ? '' : 'Successfully initialized wpa_supplicant'; }
    if (/^(pkill|killall)\s+wpa_supplicant$/.test(line)) { delete st.wpa; if (st.net) st.net.gen++; return ''; }
    return deb0.apply(this, arguments);
  };
  var debNew = H.deb;
  H.deb = function (name, o) { var st = debNew.apply(this, arguments);
    st.files['/etc/wpa_supplicant/wired.conf'] = 'ctrl_interface=/var/run/wpa_supplicant\nap_scan=0\nnetwork={\n\tkey_mgmt=IEEE8021X\n\teap=MD5\n\tidentity="user"\n\tpassword="password"\n}\n';
    if (o && o.web) { st.svc.freeradius = true;
      st.files['/etc/freeradius/3.0/clients.conf'] = 'client localhost {\n\tipaddr = 127.0.0.1\n\tsecret = testing123\n}\n';
      st.files['/etc/freeradius/3.0/users'] = '# имя Cleartext-Password := "пароль"\n'; }
    return st; };
  function radiusCheck(s, srvId, nasIp, key, id, pw) {
    var d = s.devs[srvId], st = d && d.st; if (!d || d.type !== 'deb' || !st.svc || !st.svc.freeradius) return 'RADIUS-сервер не отвечает (freeradius не запущен)';
    var cl = (st.files || {})['/etc/freeradius/3.0/clients.conf'] || '', ok = false, re = /client\s+\S+\s*\{([^}]*)\}/g, m;
    while ((m = re.exec(cl))) { var ip = (m[1].match(/ipaddr\s*=\s*(\S+)/) || [])[1], sec = (m[1].match(/secret\s*=\s*(\S+)/) || [])[1];
      var c = ip && (ip.indexOf('/') > 0 ? IP.parseCidr(ip) : { ip: ip, len: 32 });
      if (c && IP.sameNet(nasIp, c.ip, c.len) && sec === key) ok = true; }
    if (!ok) return 'RADIUS: коммутатор ' + nasIp + ' не описан в clients.conf или secret не совпадает с key';
    var us = (st.files || {})['/etc/freeradius/3.0/users'] || '', hit = us.split('\n').map(function (l) { return l.match(/^\s*"?([^\s"#]+)"?\s+Cleartext-Password\s*:=\s*"([^"]*)"/); }).filter(Boolean)
      .filter(function (x) { return x[1] === id; })[0];
    if (!hit) return 'RADIUS: пользователя ' + id + ' нет в users — Access-Reject';
    return hit[2] === pw ? null : 'RADIUS: неверный пароль ' + id + ' — Access-Reject';
  }
  // путь без побочных эффектов: от коммутатора до сервера (на время проверки 802.1X не мешает)
  function reach(s, src, dst) { var cur = src;
    for (var i = 0; i < 16; i++) { if (s.ifaces(cur).some(function (f) { return f.ip === dst; })) return cur;
      var r = s.lookup(cur, dst); if (!r) return null; var ep = s.flood(cur, r.iface).eps.filter(function (e) { return e.iface.ip === r.nh; })[0]; if (!ep) return null; cur = ep.dev; }
    return null; }
  // состояние порта: null — пропускает, строка — причина отбрасывания
  P.dot1xState = function (dev, port) {
    var d = this.devs[dev], st = d.st, x = st.dot1x, p = st.ports[port]; if (!x || !x.on || !p || !p.dot1x || p.dot1x === 'force-authorized') return { ok: true };
    if (p.dot1x === 'force-unauthorized') return { ok: false, why: 'порт в режиме force-unauthorized' };
    var C = this._d1c && this._d1c.gen === this.gen ? this._d1c : (this._d1c = { gen: this.gen, t: {} }), k = dev + '|' + port;
    if (C.t[k]) return C.t[k];
    var s = this, pr = s.peer(dev, port), h = pr && s.devs[pr.dev], res;
    if (!h || h.type !== 'deb' || !h.st.wpa || !h.st.up) res = { ok: false, why: 'клиент не прошёл 802.1X (нет wpa_supplicant на подключённом узле)' };
    else { var me = x.method || (st.dialect === '6' ? 'radius' : 'local'), w = h.st.wpa;
      if (me === 'none') res = { ok: true, user: w.id };
      else if (me === 'local') { var u = (st.users || {})[w.id]; res = u && u.pw === w.pw ? { ok: true, user: w.id } : { ok: false, why: 'локальная проверка: неверное имя или пароль ' + w.id }; }
      else { res = { ok: false, why: 'нет RADIUS-сервера (radius-server host)' };
        s._d1busy = true;
        try { for (var i = 0; i < x.radius.length; i++) { var r = x.radius[i], srv = reach(s, dev, r.ip);
          if (!srv) { res = { ok: false, why: 'RADIUS-сервер ' + r.ip + ' недоступен' }; continue; }
          var nas = (s.lookup(dev, r.ip) || { iface: {} }).iface.ip, e = radiusCheck(s, srv, nas, r.key, w.id, w.pw);
          res = e ? { ok: false, why: e } : { ok: true, user: w.id, server: r.ip }; break; } }
        finally { s._d1busy = false; } } }
    C.t[k] = res; return res;
  };
  P.dot1xBlock = function (dev, port) { if (this._d1busy) return null; var r = this.dot1xState(dev, port); return r.ok ? null : '802.1X: порт ' + port + ' не авторизован — ' + r.why; };
  ['', 'do '].forEach(function (pre) { mcmd(D, pre ? E.CFG : 'priv', pre + 'show dot1x interface <if>', function (st, a) { var x = st.dot1x || {}, p = a[0][0], q = st.ports[p] || {};
    var r = st.net ? st.net.dot1xState(st.dev, p) : { ok: true };
    return ['Authentication is ' + (x.on ? 'enabled' : 'disabled'), 'Authenticating Servers: ' + ((x.method || (st.dialect === '6' ? 'radius' : 'local')) === 'radius' ? 'Radius' : 'Local'), '',
      p, ' Host mode: ' + (q.dot1xHost || 'multi-host'), ' Port Administrated Status: ' + (q.dot1x || 'force-authorized'), ' Guest VLAN: disabled', ' Open access: disabled', ' Server timeout: 30 sec',
      ' Port Operational Status: ' + (r.ok ? 'authorized' : 'unauthorized*') + (r.user ? '\n User Name: ' + r.user : '')].join('\n'); }, 'Состояние 802.1X порта'); });
})(typeof window !== 'undefined' ? window : global);
