/* Программы «Рабочего стола» конечных узлов (VPC, Debian, Docker) — сетевая часть (окна — desk_ui.js).
   Настройка IP: статический адрес / DHCP, маска, шлюз, DNS — то же состояние, что у команд: VPC — ip, ip dhcp, ip dns;
     Debian — /etc/network/interfaces (iface ens3 inet static|dhcp), /etc/resolv.conf и поднятый ens3.
   Веб-браузер: имя → DNS, запрос TCP 80 (https:// — TCP 443) к серверу; страница — /var/www/html/index.html сервера (apache2),
     без файла — стандартная страница «It works!». HTTPS — если на сервере включён SSL (вкладка «Службы»).
   FTP-клиент: TCP 21, сервер vsftpd на Debian, вход — учётные записи сервера (как у vsftpd: локальные пользователи), каталог — домашний
     (/root, /home/ИМЯ); ls, get, put, delete. Файлы клиента — «Документы» (Debian — домашний каталог, у VPC — свои).
   Почта: SMTP (TCP 25, postfix) — письмо кладётся в ящик получателя на сервере (ИМЯ@домен, ящик — учётная запись сервера);
     POP3 (TCP 110, dovecot) — вход учётной записью, письма забираются и удаляются с сервера.
   Telnet / SSH-клиент — проверка TCP 23 / 22 до устройства и окно терминала к нему.
   Генератор трафика — поток ICMP / UDP / TCP (адрес, порт, размер, частота, длительность) через симуляцию во времени (sim.js). */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, H = EL.hosts, IP = EL.ip;
  // службы Debian: FTP, SMTP, POP3 (на сервере включены, на рабочей станции — нет)
  var deb0 = H.deb;
  H.deb = function (name, o) { var st = deb0.apply(this, arguments), on = !!(o && o.web);
    st.svc.vsftpd = on; st.svc.postfix = on; st.svc.dovecot = on; st.mail = {}; st.srv = { https: false, domain: null }; return st; };
  EL.listensX = (function (lx0) { return function (d, proto, port) {
    if (d.type === 'deb' && proto === 'tcp') { var v = d.st.svc || {};
      if (port === 21) return !!v.vsftpd; if (port === 25) return !!v.postfix; if (port === 110) return !!v.dovecot;
      if (port === 443) return !!(v.apache2 && d.st.srv && d.st.srv.https); }
    return lx0 ? lx0(d, proto, port) : undefined; }; })(EL.listensX);
  function host(d) { return d && (d.type === 'vpc' || d.type === 'deb') && !d.sub; }
  EL.isHost = host;

  // ---------------------------------------------------------------- настройка IP
  P.ipCfg = function (id) { var d = this.devs[id], st = d.st;
    var dns = d.type === 'vpc' ? st.dns || '' : (((st.files || {})['/etc/resolv.conf'] || '').match(/^\s*nameserver\s+(\S+)/m) || [])[1] || '';
    var dh = d.type === 'vpc' ? !!st.dhcp : H.parseIfaces(st.files['/etc/network/interfaces'] || '').mode === 'dhcp';
    return { mode: dh ? 'dhcp' : 'static', ip: st.ip || '', mask: st.ip ? IP.len2mask(st.len) : '', gw: st.gw || '', dns: dns }; };
  P.ipSet = function (id, c) {
    var d = this.devs[id], st = d.st, len = IP.mask2len(c.mask || '');
    if (c.dns && IP.ip2n(c.dns) === null) return { ok: false, msg: 'Неверный адрес DNS-сервера' };
    if (c.mode === 'static') {
      if (IP.ip2n(c.ip || '') === null) return { ok: false, msg: 'Неверный IP-адрес' };
      if (len === null || len === 0) return { ok: false, msg: 'Неверная маска подсети' };
      if (c.gw && IP.ip2n(c.gw) === null) return { ok: false, msg: 'Неверный адрес шлюза' };
      if (c.gw && !IP.sameNet(c.ip, c.gw, len)) return { ok: false, msg: 'Шлюз ' + c.gw + ' не в подсети ' + IP.netOf(c.ip, len) };
    }
    var r = { ok: true, msg: 'Настройки применены' };
    if (d.type === 'vpc') {
      if (c.mode === 'dhcp') { var o = H.vpcExec(st, 'ip dhcp'); r = { ok: /DORA/.test(o), msg: /DORA/.test(o) ? 'DHCP: ' + o.replace(/^DD?ORA /, '') : 'DHCP-сервер не ответил' }; }
      else { st.ip = c.ip; st.len = len; st.gw = c.gw || null; st.dhcp = false; }
      st.dns = c.dns || null;
    } else {
      var f = st.files, keep = (f['/etc/network/interfaces'] || '').split('\n# The primary network interface')[0];
      f['/etc/network/interfaces'] = keep + '\n# The primary network interface\n' + (c.mode === 'dhcp' ? 'allow-hotplug ens3\niface ens3 inet dhcp\n'
        : 'auto ens3\niface ens3 inet static\n    address ' + c.ip + '/' + len + '\n' + (c.gw ? '    gateway ' + c.gw + '\n' : ''));
      f['/etc/resolv.conf'] = c.dns ? 'nameserver ' + c.dns + '\n' : '';
      if (c.mode === 'dhcp') { var dh = this.dhcp(id); if (this.onTrace) this.onTrace({ ok: dh.ok, steps: dh.steps }, id, 'DHCP');
        if (dh.ok) { st.up = true; st.ip = dh.ip; st.len = dh.len; st.gw = dh.gw || null; r.msg = 'DHCP: ' + dh.ip + '/' + dh.len + (dh.gw ? ', шлюз ' + dh.gw : ''); }
        else { st.ip = null; st.gw = null; r = { ok: false, msg: 'DHCP-сервер не ответил' }; } }
      else { st.up = true; st.ip = c.ip; st.len = len; st.gw = c.gw || null; }
    }
    this.gen++; return r; };

  // ---------------------------------------------------------------- общее: имя → адрес, запрос к службе
  function reach(net, id, name, proto, port) {
    var rs = net.resolve ? net.resolve(id, name) : { ip: name };
    if (!rs.ip) return { ok: false, why: rs.err === 'nx' ? 'имя ' + name + ' не найдено (DNS)' : rs.err === 'noserver' ? 'не задан DNS-сервер — имя ' + name + ' не разрешить' : 'DNS-сервер не отвечает' };
    var r = net.request(id, rs.ip, proto, port); if (net.onTrace) net.onTrace(r, id, rs.ip + ':' + port);
    if (!r.ok) return { ok: false, ip: rs.ip, why: r.why === 'Connection refused' ? 'на ' + rs.ip + ' порт ' + port + ' закрыт (служба не запущена)' : 'нет связи с ' + rs.ip, steps: r.steps };
    return { ok: true, ip: rs.ip, srv: net.devs[r.dev], steps: r.steps };
  }
  EL.appReach = reach;
  function home(user) { return user === 'root' ? '/root' : '/home/' + user; }

  // ---------------------------------------------------------------- веб-браузер
  var PAGE = '<!doctype html><html><head><meta charset="utf-8"><title>Apache2 Debian Default Page</title></head><body style="font-family:sans-serif">' +
    '<h1>It works!</h1><p>Это стандартная страница веб-сервера Apache2 на Debian. Замените файл /var/www/html/index.html.</p></body></html>';
  EL.webDefault = PAGE;
  P.httpGet = function (id, url) {
    var m = String(url || '').trim().match(/^(?:(https?):\/\/)?([^\/:\s]+)(?::(\d+))?(\/\S*)?$/);
    if (!m) return { ok: false, why: 'неверный адрес' };
    var sec = m[1] === 'https', port = +(m[3] || (sec ? 443 : 80)), r = reach(this, id, m[2], 'tcp', port);
    if (!r.ok) return r;
    var s = r.srv, path = m[4] && m[4] !== '/' ? m[4] : '/index.html';
    if (s.type === 'deb') { var f = (s.st.files || {})['/var/www/html' + path];
      if (f === undefined && path === '/index.html') f = PAGE;
      return f === undefined ? { ok: true, code: 404, ip: r.ip, html: '<h1>Not Found</h1><p>The requested URL ' + path.replace(/[<>&]/g, '') + ' was not found on this server.</p>' }
        : { ok: true, code: 200, ip: r.ip, html: f, sec: sec, srv: s.name }; }
    return { ok: true, code: 200, ip: r.ip, html: '<h1>' + s.model + '</h1><p>Веб-интерфейс устройства ' + s.name + '</p>', dev: s.id };
  };

  // ---------------------------------------------------------------- документы клиента
  P.docs = function (id) { var d = this.devs[id], st = d.st;
    if (d.type === 'vpc') { st.docs = st.docs || {}; return { list: function () { return Object.keys(st.docs).sort(); }, get: function (n) { return st.docs[n]; }, put: function (n, t) { st.docs[n] = t; }, del: function (n) { delete st.docs[n]; } }; }
    var dir = home(st.user && st.user !== 'root' ? st.user : 'root') + '/';
    return { dir: dir, list: function () { return Object.keys(st.files).filter(function (k) { return k.indexOf(dir) === 0 && k.slice(dir.length).indexOf('/') < 0; }).map(function (k) { return k.slice(dir.length); }).sort(); },
             get: function (n) { return st.files[dir + n]; }, put: function (n, t) { st.files[dir + n] = t; }, del: function (n) { delete st.files[dir + n]; } }; };

  // ---------------------------------------------------------------- FTP-клиент
  P.ftp = function (id, srv, user, pw, op, name) {
    var r = reach(this, id, srv, 'tcp', 21); if (!r.ok) return r;
    var s = r.srv; if (s.type !== 'deb') return { ok: false, why: '530 Login incorrect' };
    if (!s.st.accounts[user] || s.st.accounts[user] !== pw) return { ok: false, why: '530 Login incorrect.' };
    var dir = home(user) + '/', F = s.st.files, D = this.docs(id), base = String(name || '').replace(/^.*\//, '');
    if (op === 'ls') return { ok: true, files: Object.keys(F).filter(function (k) { return k.indexOf(dir) === 0 && k.slice(dir.length).indexOf('/') < 0; }).map(function (k) { return { name: k.slice(dir.length), size: F[k].length }; }), msg: '230 Login successful.' };
    if (!base) return { ok: false, why: 'не указано имя файла' };
    if (op === 'get') { if (F[dir + base] === undefined) return { ok: false, why: '550 Failed to open file.' }; D.put(base, F[dir + base]); return { ok: true, msg: '226 Transfer complete. ' + base + ' → Документы (' + F[dir + base].length + ' байт)' }; }
    if (op === 'put') { var t = D.get(base); if (t === undefined) return { ok: false, why: 'нет файла ' + base + ' в Документах' }; F[dir + base] = t; return { ok: true, msg: '226 Transfer complete. ' + base + ' → ' + s.name + ':' + dir + base }; }
    if (op === 'delete') { if (F[dir + base] === undefined) return { ok: false, why: '550 Delete operation failed.' }; delete F[dir + base]; return { ok: true, msg: '250 Delete operation successful.' }; }
    return { ok: false, why: '500 Unknown command.' };
  };

  // ---------------------------------------------------------------- почта: SMTP и POP3
  P.mailSend = function (id, c, msg) {
    var to = String(msg.to || '').trim().match(/^([^@\s]+)@(\S+)$/); if (!to) return { ok: false, why: 'адрес получателя — ИМЯ@домен' };
    if (!/^[^@\s]+@\S+$/.test(c.from || '')) return { ok: false, why: 'в настройках не задан свой адрес (ИМЯ@домен)' };
    var r = reach(this, id, c.smtp, 'tcp', 25); if (!r.ok) return r;
    var s = r.srv; if (s.type !== 'deb') return { ok: false, why: '554 Transaction failed' };
    var dom = s.st.srv && s.st.srv.domain;
    if (dom && to[2].toLowerCase() !== dom.toLowerCase()) return { ok: false, why: '554 5.7.1 <' + msg.to + '>: Relay access denied (сервер обслуживает домен ' + dom + ')' };
    if (!s.st.accounts[to[1]]) return { ok: false, why: '550 5.1.1 <' + msg.to + '>: Recipient address rejected: User unknown' };
    (s.st.mail[to[1]] = s.st.mail[to[1]] || []).push({ from: c.from, to: msg.to, subj: msg.subj || '', body: msg.body || '', t: this.now || 0 });
    return { ok: true, msg: '250 2.0.0 Ok: queued — письмо доставлено в ящик ' + to[1] + ' на ' + s.name };
  };
  P.mailRecv = function (id, c) {
    var r = reach(this, id, c.pop3, 'tcp', 110); if (!r.ok) return r;
    var s = r.srv; if (s.type !== 'deb') return { ok: false, why: '-ERR' };
    if (!s.st.accounts[c.user] || s.st.accounts[c.user] !== c.pw) return { ok: false, why: '-ERR [AUTH] Authentication failed.' };
    var L = s.st.mail[c.user] || []; s.st.mail[c.user] = [];
    return { ok: true, msgs: L, msg: '+OK ' + L.length + ' сообщ.' };
  };

  // ---------------------------------------------------------------- Telnet / SSH, генератор трафика
  P.remote = function (id, proto, hostName) { var r = reach(this, id, hostName, 'tcp', proto === 'ssh' ? 22 : 23); if (!r.ok) return r;
    return { ok: true, dev: r.srv.id, ip: r.ip }; };
  // поток генератора: {proto: 'icmp'|'udp'|'tcp', dst, port, size, rate, dur} → итог симуляции
  P.trafficGen = function (id, g) {
    var rs = this.resolve ? this.resolve(id, g.dst) : { ip: g.dst }; if (!rs.ip) return { ok: false, why: 'имя ' + g.dst + ' не разрешено' };
    var size = Math.max(28, Math.min(9000, g.size | 0 || 64)), rate = Math.max(1, Math.min(20000, +g.rate || 10)), dur = Math.max(0.01, Math.min(5, +g.dur || 1));
    var fl = g.proto === 'icmp' ? { kind: 'ping', src: id, dst: rs.ip, size: size, count: Math.max(1, Math.min(200, Math.round(rate * dur))), interval: 1 / rate }
      : { kind: 'udp', src: id, dst: rs.ip, size: size, rate: rate, dur: dur, proto: g.proto, port: +g.port || 0 };
    if (g.proto !== 'icmp' && fl.port) { var rq = this.request(id, rs.ip, g.proto, fl.port);
      if (!rq.ok && rq.why !== 'Connection refused') return { ok: false, why: 'нет связи с ' + rs.ip }; fl.refused = !rq.ok; }
    var r = this.simulate([fl], {}), f = r.flows[0]; this.gen++;
    return { ok: true, flow: fl, res: f, sim: r, refused: fl.refused };
  };
  // ---------------------------------------------------------------- PDU (как Simple / Complex PDU в Packet Tracer)
  // простой: ICMP echo от src к первому адресу получателя; сложный: {proto icmp|udp|tcp, dst, port, size, count, interval}
  P.pduDst = function (id) { var f = this.ifaces(id)[0]; return f ? f.ip : null; };
  P.pdu = function (src, o) {
    var dst = o.dst, proto = o.proto || 'icmp', d = this.devs[src];
    if (!d || d.off) return { ok: false, why: 'источник выключен', r: { ok: false, steps: [] } };
    if (!this.ifaces(src).length) return { ok: false, why: 'у источника нет IP-адреса', r: { ok: false, steps: [] } };
    if (IP.ip2n(dst || '') === null) return { ok: false, why: 'у получателя нет IP-адреса', r: { ok: false, steps: [] } };
    var r = proto === 'icmp' ? this.ping(src, dst) : this.request(src, dst, proto, +o.port || (proto === 'tcp' ? 80 : 9));
    var hit = r.ok || (proto === 'udp' && r.why === 'Connection refused');      // UDP: датаграмма дошла до узла, даже если порт не слушают
    var res = { ok: hit, r: r, why: hit ? '' : r.why === 'Connection refused' ? 'TCP ' + o.port + ': соединение отклонено (служба не запущена)' : r.why || 'не доставлено', sent: 1, recv: hit ? 1 : 0 };
    var cnt = Math.max(1, Math.min(100, +o.count || 1));
    if (cnt > 1 && hit && proto !== 'tcp' && this.simulate) {
      var f = this.simulate([proto === 'icmp' ? { kind: 'ping', src: src, dst: dst, size: +o.size || 56, count: cnt, interval: Math.max(0.001, +o.interval || 1) }
        : { kind: 'udp', src: src, dst: dst, size: +o.size || 56, rate: 1 / Math.max(0.001, +o.interval || 1), dur: cnt * Math.max(0.001, +o.interval || 1) }], {}).flows[0];
      res.sent = f.sent; res.recv = f.recv; res.ok = f.recv === f.sent; if (!res.ok) res.why = 'потеряно ' + (f.sent - f.recv) + ' из ' + f.sent;
    } else if (cnt > 1) { res.sent = cnt; res.recv = hit ? cnt : 0; }
    this.gen++; return res;
  };
})(typeof window !== 'undefined' ? window : global);
