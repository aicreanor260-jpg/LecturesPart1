/* Службы сервера Debian — общее состояние окна «Службы» (srv_ui.js) и команд Debian: настройки лежат в тех же файлах, галочка «Включено» —
   тот же st.svc, что у systemctl start|stop (запуск и остановка идут через systemctl, перезапуск перечитывает файлы).
   DHCP — isc-dhcp-server, /etc/dhcp/dhcpd.conf: subnet A netmask M { range A B; option routers R; option domain-name-servers D; }
     (выдаёт адреса в своём широковещательном домене и через ретранслятор ESR ip helper-address — пул по giaddr, как у ESR).
   DNS — bind9: /etc/bind/named.conf.local (zone "ИМЯ" { type master; file "/etc/bind/db.ИМЯ"; }) и файлы зон (A, CNAME, MX; MX только хранится).
   HTTP / HTTPS — apache2: /var/www/html/*, HTTPS — включённый SSL (a2enmod ssl, a2ensite default-ssl → TCP 443).
   FTP — vsftpd: пользователи — учётные записи сервера (useradd / passwd / userdel), файлы — домашние каталоги.
   Почта — postfix + dovecot: домен (myhostname/mydomain), ящики — учётные записи.
   TFTP — tftpd-hpa, каталог /tftp; NTP — chronyd; Syslog — rsyslog, журналы /var/log/rsyslog/ИМЯ/*.log;
   RADIUS — freeradius: clients.conf (client ИМЯ { ipaddr, secret }) и users ("ИМЯ" Cleartext-Password := "ПАРОЛЬ");
   TACACS+ — tac_plus: /etc/tacacs+/tac_plus.conf (key = КЛЮЧ, user = ИМЯ { login = cleartext "ПАРОЛЬ" }). */
(function (G) {
  'use strict';
  var EL = G.EL, H = EL.hosts, IP = EL.ip;
  var F = { dhcp: '/etc/dhcp/dhcpd.conf', named: '/etc/bind/named.conf.local', rcl: '/etc/freeradius/3.0/clients.conf', rus: '/etc/freeradius/3.0/users', tac: '/etc/tacacs+/tac_plus.conf' };
  var deb0 = H.deb;
  H.deb = function (name, o) { var st = deb0.apply(this, arguments);
    st.svc['isc-dhcp-server'] = false;
    st.files[F.dhcp] = '# dhcpd.conf\n#\n# subnet 10.0.0.0 netmask 255.255.255.0 {\n#   range 10.0.0.100 10.0.0.150;\n#   option routers 10.0.0.1;\n#   option domain-name-servers 10.0.0.10;\n# }\n';
    if (st.svc.freeradius === undefined) st.svc.freeradius = false; if (st.svc.tac_plus === undefined) st.svc.tac_plus = false; if (st.svc.bind9 === undefined) st.svc.bind9 = false;
    return st; };
  function txt(st, f) { return (st.files || {})[f] || ''; }
  function uncomment(s) { return String(s).replace(/#.*$/gm, ''); }

  // ---------------------------------------------------------------- DHCP (isc-dhcp-server)
  function dhcpRead(st) { var out = [], re = /subnet\s+(\S+)\s+netmask\s+(\S+)\s*\{([^}]*)\}/g, m, s = uncomment(txt(st, F.dhcp));
    while ((m = re.exec(s))) { var b = m[3], rg = b.match(/range\s+(\S+)\s+(\S+?)\s*;/), gw = b.match(/option\s+routers\s+(\S+?)\s*;/), dn = b.match(/option\s+domain-name-servers\s+(\S+?)\s*;/);
      out.push({ net: m[1], mask: m[2], from: rg ? rg[1] : '', to: rg ? rg[2] : '', gw: gw ? gw[1] : '', dns: dn ? dn[1] : '' }); }
    return out; }
  function dhcpWrite(st, L) { st.files[F.dhcp] = '# dhcpd.conf — изменено в окне «Службы»\ndefault-lease-time 600;\nmax-lease-time 7200;\n\n' + L.map(function (p) {
    return 'subnet ' + p.net + ' netmask ' + p.mask + ' {\n  range ' + p.from + ' ' + p.to + ';\n' + (p.gw ? '  option routers ' + p.gw + ';\n' : '') + (p.dns ? '  option domain-name-servers ' + p.dns + ';\n' : '') + '}\n'; }).join('\n'); }
  function dhcpCheck(p) { var len = IP.mask2len(p.mask);
    if (IP.ip2n(p.net) === null || len === null) return 'сеть / маска';
    if (IP.netOf(p.net, len).split('/')[0] !== p.net) return 'адрес сети ' + p.net + ' не совпадает с маской (сеть ' + IP.netOf(p.net, len) + ')';
    if (IP.ip2n(p.from) === null || IP.ip2n(p.to) === null || !IP.sameNet(p.from, p.net, len) || !IP.sameNet(p.to, p.net, len) || IP.ip2n(p.from) > IP.ip2n(p.to)) return 'диапазон адресов вне сети ' + p.net;
    if (p.gw && (IP.ip2n(p.gw) === null || !IP.sameNet(p.gw, p.net, len))) return 'шлюз ' + p.gw + ' не в сети';
    if (p.dns && IP.ip2n(p.dns) === null) return 'адрес DNS';
    return null; }
  // пулы для общей логики DHCP (net.js) — в формате ESR: {dhcp:{on, pools}, ifs, relay}
  EL.debDhcpCfg = function (d) { var st = d.st; if (d.type !== 'deb' || d.off || !st.svc || !st.svc['isc-dhcp-server'] || !st.up) return null;
    var key = txt(st, F.dhcp); if (st._dhcpK !== key) { var pools = {};
      dhcpRead(st).forEach(function (p) { if (dhcpCheck(p)) return; var len = IP.mask2len(p.mask);
        pools['subnet ' + p.net] = { net: p.net + '/' + len, range: [p.from, p.to], gw: p.gw || null, dns: p.dns || null }; });
      st._dhcpK = key; st._dhcpC = { dhcp: { on: true, pools: pools }, ifs: {}, relay: false }; }
    return st._dhcpC; };
  EL.listensX = (function (lx0) { return function (d, proto, port) {
    if (d.type === 'deb' && proto === 'udp' && port === 67) return !!(d.st.svc || {})['isc-dhcp-server'];
    return lx0 ? lx0(d, proto, port) : undefined; }; })(EL.listensX);

  // ---------------------------------------------------------------- DNS (bind9)
  function dnsRead(st) { var conf = uncomment(txt(st, F.named)).replace(/\/\/.*$/gm, ''), out = [], re = /zone\s+"([^"]+)"\s*(?:IN\s*)?\{([^}]*)\}/gi, m;
    while ((m = re.exec(conf))) { var f = (m[2].match(/file\s+"([^"]+)"/i) || [])[1], z = m[1].replace(/\.$/, ''); if (!f) continue;
      var recs = []; txt(st, f).replace(/;.*$/gm, '').split('\n').forEach(function (l) { var t = l.trim().split(/\s+/); if (!t[0] || /^\$/.test(t[0]) || /^\s/.test(l)) return;
        var nm = t.shift(); while (t.length && (/^\d+$/.test(t[0]) || /^IN$/i.test(t[0]))) t.shift(); var ty = (t.shift() || '').toUpperCase();
        if (ty === 'A' || ty === 'CNAME') recs.push({ name: nm, type: ty, val: t[0] || '' });
        if (ty === 'MX') recs.push({ name: nm, type: 'MX', val: t[1] || '', pref: +t[0] || 10 }); });
      out.push({ zone: z, file: f, recs: recs }); }
    return out; }
  function dnsWrite(st, zones) { var keep = txt(st, F.named).split('// --- зоны окна «Службы»')[0].replace(/zone\s+"[^"]+"\s*(?:IN\s*)?\{[^}]*\};?\s*/gi, '');
    st.files[F.named] = keep.replace(/\s+$/, '') + '\n\n// --- зоны окна «Службы»\n' + zones.map(function (z) { return 'zone "' + z.zone + '" {\n\ttype master;\n\tfile "' + (z.file || '/etc/bind/db.' + z.zone) + '";\n};\n'; }).join('');
    zones.forEach(function (z) { var o = z.zone + '.';
      st.files[z.file || '/etc/bind/db.' + z.zone] = '$TTL\t604800\n@\tIN\tSOA\tns.' + o + ' root.' + o + ' ( 2 604800 86400 2419200 604800 )\n@\tIN\tNS\tns.' + o + '\n' +
        z.recs.map(function (r) { return r.name + '\tIN\t' + r.type + '\t' + (r.type === 'MX' ? (r.pref || 10) + '\t' : '') + r.val; }).join('\n') + '\n'; }); }

  // ---------------------------------------------------------------- RADIUS, TACACS+
  function radRead(st) { var cl = [], re = /client\s+(\S+)\s*\{([^}]*)\}/g, m, s = uncomment(txt(st, F.rcl));
    while ((m = re.exec(s))) cl.push({ name: m[1], ip: (m[2].match(/ipaddr\s*=\s*(\S+)/) || [])[1] || '', secret: (m[2].match(/secret\s*=\s*(\S+)/) || [])[1] || '' });
    var us = uncomment(txt(st, F.rus)).split('\n').map(function (l) { return l.match(/^\s*"?([^\s"#]+)"?\s+Cleartext-Password\s*:=\s*"([^"]*)"/); }).filter(Boolean).map(function (x) { return { name: x[1], pw: x[2] }; });
    return { clients: cl, users: us }; }
  function radWrite(st, r) { st.files[F.rcl] = r.clients.map(function (c, i) { return 'client ' + (c.name || 'nas' + (i + 1)) + ' {\n\tipaddr = ' + c.ip + '\n\tsecret = ' + c.secret + '\n}\n'; }).join('');
    st.files[F.rus] = '# имя Cleartext-Password := "пароль"\n' + r.users.map(function (u) { return '"' + u.name + '" Cleartext-Password := "' + u.pw + '"\n'; }).join(''); }
  function tacRead(st) { var s = txt(st, F.tac), us = [], re = /^\s*user\s*=\s*(\S+)\s*\{([^}]*)\}/gm, m;
    while ((m = re.exec(s))) us.push({ name: m[1], pw: (m[2].match(/login\s*=\s*cleartext\s*"([^"]*)"/) || [])[1] || '' });
    return { key: (s.match(/^\s*key\s*=\s*"?([^"\n]+?)"?\s*$/m) || [])[1] || '', users: us }; }
  function tacWrite(st, t) { st.files[F.tac] = 'key = ' + t.key + '\n\n' + t.users.map(function (u) { return 'user = ' + u.name + ' {\n    login = cleartext "' + u.pw + '"\n}\n'; }).join('\n'); }

  // ---------------------------------------------------------------- systemctl от имени root (то же, что ввести в консоли)
  function sysctl(st, verb, svc) { var u = st.user, l = st.login; st.user = 'root'; var r; try { r = H.debExec(st, 'systemctl ' + verb + ' ' + svc); } finally { st.user = u; st.login = l; } if (st.net) st.net.gen++; return r || ''; }
  var UNITS = { dhcp: ['isc-dhcp-server'], dns: ['bind9'], http: ['apache2'], ftp: ['vsftpd'], mail: ['postfix', 'dovecot'], tftp: ['tftpd-hpa'], ntp: ['chronyd'], syslog: ['rsyslog'], radius: ['freeradius'], tacacs: ['tac_plus'] };
  EL.srv = { F: F, UNITS: UNITS, dhcpRead: dhcpRead, dhcpWrite: dhcpWrite, dhcpCheck: dhcpCheck, dnsRead: dnsRead, dnsWrite: dnsWrite, radRead: radRead, radWrite: radWrite, tacRead: tacRead, tacWrite: tacWrite,
    on: function (st, k) { return UNITS[k].every(function (u) { return !!st.svc[u]; }); },
    set: function (st, k, on) { UNITS[k].forEach(function (u) { sysctl(st, on ? 'start' : 'stop', u); }); },
    restart: function (st, k) { if (EL.srv.on(st, k)) UNITS[k].forEach(function (u) { sysctl(st, 'restart', u); }); },
    users: function (st) { return Object.keys(st.accounts).map(function (u) { return { name: u, pw: st.accounts[u] }; }); },
    https: function (st, on) { st.srv.https = !!on; if (st.net) st.net.gen++; } };

  // Debian: a2enmod ssl / a2ensite default-ssl включают HTTPS, a2dismod ssl / a2dissite default-ssl — выключают; useradd, passwd, userdel — учётные записи
  var dx0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    var t = String(raw).trim().split(/\s+/), c = t[0];
    if (st.user && !st.ssh && st.srv) {
      if (/^a2(en|dis)(mod|site)$/.test(c) && /^(ssl|default-ssl)$/.test(t[1] || '')) { if (st.user !== 'root') return 'ERROR: you must be root'; st.srv.https = /en/.test(c);
        return /en/.test(c) ? (t[1] === 'ssl' ? 'Enabling module ssl.' : 'Enabling site default-ssl.') + '\nTo activate the new configuration, you need to run:\n  systemctl restart apache2' : 'Module ' + t[1] + ' disabled.'; }
      if (c === 'useradd' && t[t.length - 1] && !/^-/.test(t[t.length - 1])) { if (st.user !== 'root') return 'useradd: Permission denied.'; var nm = t[t.length - 1];
        if (st.accounts[nm] !== undefined) return "useradd: user '" + nm + "' already exists"; st.accounts[nm] = ''; return ''; }
      if (c === 'userdel' && t[1]) { if (st.user !== 'root') return 'userdel: Permission denied.'; if (st.accounts[t[1]] === undefined) return "userdel: user '" + t[1] + "' does not exist"; delete st.accounts[t[1]]; return ''; }
    }
    return dx0.apply(this, arguments);
  };
})(typeof window !== 'undefined' ? window : global);
