/* DNS: сервер BIND9 на Debian (зоны в /etc/bind/named.conf.local и файлах зон, systemctl restart bind9), клиенты:
   Debian — /etc/resolv.conf (nameserver, search), /etc/hosts, nslookup ИМЯ [СЕРВЕР], ping/curl по имени;
   VPC — ip dns A.B.C.D, ping ИМЯ;
   ESR — domain lookup enable, domain name-server, domain name, domain ip host (справочник ESR-Series CLI 1.23), ping ИМЯ;
   MES — 10.x: ip name-server ipv4 A.B.C.D (руководство 10.4.6); 6.x: ip domain lookup, ip name-server, ip domain name, ip host (6.6.8.8).
   Запрос — UDP 53 к серверу по сети (виден в трассе и захвате), ответ — из зоны BIND. Поддерживаются записи A и CNAME. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, E = EL.E, P = EL.Net.prototype, H = EL.hosts, IP = EL.ip, CMDS = E.CMDS, CFG = E.CFG;
  function isIp(x) { return IP.ip2n(x) !== null; }

  // ================================================================ сервер BIND9
  function zones(st) {
    var conf = (st.files || {})['/etc/bind/named.conf.local'] || '', out = {}, re = /zone\s+"([^"]+)"\s*(?:IN\s*)?\{([^}]*)\}/gi, m;
    while ((m = re.exec(conf))) { var f = m[2].match(/file\s+"([^"]+)"/i), z = m[1].replace(/\.$/, '').toLowerCase();
      if (f && /type\s+(master|primary)/i.test(m[2])) out[z] = parseZone(z, (st.files || {})[f[1]] || ''); }
    return out;
  }
  function parseZone(z, text) {
    var origin = z, recs = {}, last = z, body = String(text).replace(/;.*$/gm, '').replace(/\(([^)]*)\)/g, function (x, y) { return y.replace(/\n/g, ' '); });
    body.split('\n').forEach(function (line) {
      if (!line.trim()) return;
      var o = line.match(/^\$ORIGIN\s+(\S+)/i); if (o) { origin = o[1].replace(/\.$/, '').toLowerCase(); return; }
      if (/^\$/.test(line)) return;
      var t = line.trim().split(/\s+/), name = /^\s/.test(line) ? last : t.shift();
      var fq = name === '@' ? origin : /\.$/.test(name) ? name.slice(0, -1).toLowerCase() : (name + '.' + origin).toLowerCase(); last = name;
      while (t.length && (/^\d+$/.test(t[0]) || /^IN$/i.test(t[0]))) t.shift();
      var type = (t.shift() || '').toUpperCase(), data = t[0];
      if (type === 'A' && isIp(data)) (recs[fq] = recs[fq] || {}).a = data;
      if (type === 'CNAME' && data) (recs[fq] = recs[fq] || {}).cname = /\.$/.test(data) ? data.slice(0, -1).toLowerCase() : (data + '.' + origin).toLowerCase();
    });
    return recs;
  }
  // ответ сервера: адрес, null — нет такого имени, false — нет зоны (сервер не авторитетен)
  P.dnsAnswer = function (id, q) {
    var d = this.devs[id]; if (!d || d.type !== 'deb' || !d.st.svc || !d.st.svc.bind9) return false;
    var Z = d.st.bindZones || zones(d.st), name = q.toLowerCase(), hops = 0;
    while (hops++ < 8) {
      var z = Object.keys(Z).filter(function (k) { return name === k || name.slice(-k.length - 1) === '.' + k; }).sort(function (a, b) { return b.length - a.length; })[0];
      if (!z) return hops === 1 ? false : null;
      var r = Z[z][name]; if (!r) return null; if (r.a) return r.a; name = r.cname;
    }
    return null;
  };

  // ================================================================ резолвер
  function hostsFile(text, name) { var ip = null;
    String(text || '').split('\n').forEach(function (l) { var t = l.replace(/#.*$/, '').trim().split(/\s+/); if (isIp(t[0]) && t.slice(1).map(function (x) { return x.toLowerCase(); }).indexOf(name) >= 0 && !ip) ip = t[0]; });
    return ip; }
  function cfg(s, id) {
    var d = s.devs[id], st = d.st;
    if (d.type === 'deb') { var rc = (st.files || {})['/etc/resolv.conf'] || '', sv = [], dom = null;
      rc.split('\n').forEach(function (l) { var m = l.match(/^\s*nameserver\s+(\S+)/); if (m && isIp(m[1])) sv.push(m[1]); var q = l.match(/^\s*(?:search|domain)\s+(\S+)/); if (q) dom = q[1]; });
      return { on: true, servers: sv, dom: dom, local: function (n) { return hostsFile((st.files || {})['/etc/hosts'], n) || (n === 'localhost' ? '127.0.0.1' : null); } }; }
    if (d.type === 'vpc') return { on: true, servers: st.dns ? [st.dns] : [], dom: null, local: function () { return null; } };
    if (d.type === 'esr') { var c = st.run.dns || {}; return { on: !!c.on, servers: c.servers || [], dom: c.dom || null, local: function (n) { return (c.hosts || {})[n] || null; } }; }
    var m2 = st.dns || {}; return { on: m2.lookup !== false, servers: m2.servers || [], dom: m2.dom || null, local: function (n) { return ((m2.hosts || {})[n] || [])[0] || null; } };
  }
  // разрешить имя: {ip} или {err: 'nx' | 'timeout' | 'noserver' | 'off', server}
  P.resolve = function (id, name, server, noLocal) {
    name = String(name).toLowerCase().replace(/\.$/, '');
    if (isIp(name)) return { ip: name };
    var c = cfg(this, id), loc = !noLocal && c.local(name); if (loc) return { ip: loc, local: true };
    if (!c.on && !noLocal) return { err: 'off' };
    var q = name.indexOf('.') < 0 && c.dom ? name + '.' + c.dom : name, L = server ? [server] : c.servers, s = this;
    if (!L.length) return { err: 'noserver', q: q };
    for (var i = 0; i < L.length; i++) {
      var o = s.owner(L[i]), ans = o ? s.dnsAnswer(o.id || o, q) : false;
      s.dnsQ = { q: q, a: ans || null };
      var r; try { r = s.request(id, L[i], 'udp', 53); } finally { s.dnsQ = null; }
      if (s.onTrace) s.onTrace(r, id, 'DNS ' + q);
      if (!r.ok) continue;
      ans = s.dnsAnswer(r.dev, q);
      return ans ? { ip: ans, server: L[i], q: q } : { err: 'nx', server: L[i], q: q };
    }
    return { err: 'timeout', server: L[0], q: q };
  };

  // ================================================================ Debian
  var deb0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    var line = String(raw).trim(), t = line.split(/\s+/), c = t[0];
    if (!st.user || st.ssh || !st.net) return deb0.apply(this, arguments);
    if (c === 'systemctl' && /^(re)?start$|^reload$/.test(t[1] || '') && /^(bind9|named)(\.service)?$/.test(t[2] || '') && st.svc && 'bind9' in st.svc) {
      if (st.user !== 'root') return 'Failed to ' + t[1] + ' bind9.service: Access denied';
      st.svc.bind9 = true; st.bindZones = zones(st); return ''; }
    if (c === 'named-checkzone' && t[1] && t[2]) { var recs = parseZone(t[1].replace(/\.$/, '').toLowerCase(), (st.files || {})[t[2]]);
      if ((st.files || {})[t[2]] === undefined) return 'zone ' + t[1] + '/IN: loading from master file ' + t[2] + ' failed: file not found';
      return 'zone ' + t[1] + '/IN: loaded serial 1\nOK'; void recs; }
    if (c === 'nslookup') { var nm = t[1]; if (!nm) return 'Usage: nslookup NAME [SERVER]';
      var r = st.net.resolve(st.dev, nm, t[2], true), sv = r.server || t[2] || (cfg(st.net, st.dev).servers[0]) || '127.0.0.1';
      if (r.err === 'timeout' || r.err === 'noserver') return ';; connection timed out; no servers could be reached';
      var head = 'Server:\t\t' + sv + '\nAddress:\t' + sv + '#53\n';
      if (r.err === 'nx') return head + '\n** server can\'t find ' + r.q + ': NXDOMAIN';
      return head + '\nName:\t' + (r.q || nm) + '\nAddress: ' + r.ip; }
    if ((c === 'ping' || c === 'curl' || c === 'wget') && t.length > 1) {
      var arg = t.filter(function (x, i) { return i > 0 && !/^-/.test(x); }).pop() || '', host = arg.replace(/^https?:\/\//, '').split(/[/:]/)[0];
      if (host && EL.ip6.parse(arg) === null && !isIp(host) && /^[a-z0-9][a-z0-9.-]*$/i.test(host) && host.indexOf(':') < 0) {
        var rr = st.net.resolve(st.dev, host);
        if (!rr.ip) return c === 'ping' ? 'ping: ' + host + ': ' + (rr.err === 'nx' ? 'Name or service not known' : 'Temporary failure in name resolution')
                                        : 'curl: (6) Could not resolve host: ' + host;
        var out = deb0.call(this, st, line.replace(host, rr.ip), ui);
        return c === 'ping' ? String(out).replace('PING ' + rr.ip + ' (' + rr.ip + ')', 'PING ' + host + ' (' + rr.ip + ')') : out;
      }
    }
    return deb0.apply(this, arguments);
  };
  var debNew = H.deb;
  H.deb = function (name, o) { var st = debNew.apply(this, arguments);
    st.files['/etc/resolv.conf'] = '';
    st.files['/etc/hosts'] = '127.0.0.1\tlocalhost\n127.0.1.1\t' + st.host + '\n';
    if (o && o.web) { st.svc.bind9 = true;
      st.files['/etc/bind/named.conf.local'] = '//\n// Do any local configuration here\n//\n\n// Consider adding the 1918 zones here, if they are not used in your\n// organization\n//include "/etc/bind/zones.rfc1918";\n';
      st.files['/etc/bind/db.local'] = ';\n; BIND data file for local loopback interface\n;\n$TTL\t604800\n@\tIN\tSOA\tlocalhost. root.localhost. (\n\t\t\t      2\t\t; Serial\n\t\t\t 604800\t\t; Refresh\n\t\t\t  86400\t\t; Retry\n\t\t\t2419200\t\t; Expire\n\t\t\t 604800 )\t; Negative Cache TTL\n;\n@\tIN\tNS\tlocalhost.\n@\tIN\tA\t127.0.0.1\n@\tIN\tAAAA\t::1\n'; st.bindZones = zones(st); }
    return st; };

  // ================================================================ VPC
  var vpc0 = H.vpcExec;
  H.vpcExec = function (st, raw) {
    var t = String(raw).trim().split(/\s+/), c = (t[0] || '').toLowerCase();
    if (c === 'ip' && (t[1] || '').toLowerCase() === 'dns') { if (!t[2] || !isIp(t[2])) return 'Invalid address'; st.dns = t[2]; return ''; }
    if (c === 'show' && (!t[1] || t[1] === 'ip')) { var o = vpc0.apply(this, arguments); return st.dns ? o.replace(/(GATEWAY[^\n]*\n)/, '$1DNS         : ' + st.dns + '\n') : o; }
    if (c === 'ping' && t[1] && !isIp(t[1]) && t[1].indexOf(':') < 0 && st.net) {
      var r = st.net.resolve(st.dev, t[1]); if (!r.ip) return 'Cannot resolve ' + t[1];
      return t[1] + ' resolved to ' + r.ip + '\n\n' + vpc0.call(this, st, 'ping ' + r.ip); }
    return vpc0.apply(this, arguments);
  };

  // ================================================================ ESR
  function touch(st) { st.pending = true; }
  function dn(st) { return st.cand.dns || (st.cand.dns = { on: false, servers: [], dom: null, hosts: {} }); }
  S.cmd('config', 'domain lookup enable', function (st) { dn(st).on = true; touch(st); }, 'Включить разрешение DNS-имён');
  S.cmd('config', 'no domain lookup enable', function (st) { dn(st).on = false; touch(st); });
  S.cmd('config', 'domain name-server <ip>', function (st, a) { var d = dn(st); if (d.servers.indexOf(a[0]) < 0) d.servers.push(a[0]); touch(st); }, 'DNS-сервер');
  S.cmd('config', 'no domain name-server <ip>', function (st, a) { var d = dn(st); d.servers = d.servers.filter(function (x) { return x !== a[0]; }); touch(st); });
  S.cmd('config', 'domain name <w>', function (st, a) { dn(st).dom = a[0]; touch(st); }, 'Имя домена');
  S.cmd('config', 'no domain name', function (st) { dn(st).dom = null; touch(st); });
  S.cmd('config', 'domain ip host <w> <ip>', function (st, a) { dn(st).hosts[a[0].toLowerCase()] = a[1]; touch(st); }, 'Статическая DNS-запись');
  S.cmd('config', 'no domain ip host <w> <ip>', function (st, a) { delete dn(st).hosts[a[0].toLowerCase()]; touch(st); });
  S.RUNX.push(function (c, o) { var d = c.dns; if (!d) return;
    Object.keys(d.hosts).forEach(function (h) { o.push('domain ip host ' + h + ' ' + d.hosts[h]); });
    if (d.on) o.push('domain lookup enable'); if (d.dom) o.push('domain name ' + d.dom);
    d.servers.forEach(function (x) { o.push('domain name-server ' + x); }); });
  // ping по имени: команда «ping <w>» (IPv6) расширяется именами
  S.T.forEach(function (c) { if (c.modes.indexOf('priv') >= 0 && c.pat.join(' ') === 'ping <w>') { var run = c.run;
    c.run = function (st, a) { if (a[0].indexOf(':') >= 0 || !st.net) return run(st, a);
      var r = st.net.resolve(st.dev, a[0]); if (!r.ip) return 'ping: unknown host ' + a[0];
      return st.net.pingText(st.dev, r.ip, 'esr').replace('PING ' + r.ip + ' (' + r.ip + ')', 'PING ' + a[0] + ' (' + r.ip + ')'); }; } });

  // ================================================================ MES
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function md(st) { return st.dns || (st.dns = { lookup: true, servers: [], dom: null, hosts: {} }); }
  mcmd(['10'], 'config', 'ip name-server ipv4 <ip>', function (st, a) { var d = md(st); if (d.servers.indexOf(a[0]) < 0) d.servers.push(a[0]); }, 'DNS-сервер');
  mcmd(['10'], 'config', 'no ip name-server ipv4 <ip>', function (st, a) { var d = md(st); d.servers = d.servers.filter(function (x) { return x !== a[0]; }); });
  mcmd(['6'], 'config', 'ip name-server <ip>', function (st, a) { var d = md(st); if (d.servers.indexOf(a[0]) < 0) d.servers.push(a[0]); }, 'DNS-сервер');
  mcmd(['6'], 'config', 'no ip name-server <ip>', function (st, a) { var d = md(st); d.servers = d.servers.filter(function (x) { return x !== a[0]; }); });
  mcmd(['6'], 'config', 'ip domain lookup', function (st) { md(st).lookup = true; }, 'Разрешить DNS');
  mcmd(['6'], 'config', 'no ip domain lookup', function (st) { md(st).lookup = false; });
  mcmd(['6'], 'config', 'ip domain name <w>', function (st, a) { md(st).dom = a[0]; }, 'Домен по умолчанию');
  mcmd(['6'], 'config', 'no ip domain name', function (st) { md(st).dom = null; });
  mcmd(['6'], 'config', 'ip host <w> <ip>', function (st, a) { md(st).hosts[a[0].toLowerCase()] = [a[1]]; }, 'Статическое имя узла');
  mcmd(['6'], 'config', 'no ip host <w>', function (st, a) { delete md(st).hosts[a[0].toLowerCase()]; });
  E.RUNX.push(function (st, o) { var d = st.dns; if (!d) return;
    if (st.dialect === '6') { if (d.lookup === false) o.push('no ip domain lookup'); if (d.dom) o.push('ip domain name ' + d.dom);
      Object.keys(d.hosts).forEach(function (h) { o.push('ip host ' + h + ' ' + d.hosts[h].join(' ')); }); }
    d.servers.forEach(function (x) { o.push(st.dialect === '10' ? 'ip name-server ipv4 ' + x : 'ip name-server ' + x); }); });
  ['', 'do '].forEach(function (pre) { [['priv', ''], ['user', '']].forEach(function (m) { if (pre && m[0] === 'user') return;
    mcmd(['10', '6'], pre ? CFG : m[0], pre + 'ping <w>', function (st, a) { if (!st.net) return '';
      var r = st.net.resolve(st.dev, a[0]); if (!r.ip) return '% Unknown host ' + a[0];
      return st.net.pingText(st.dev, r.ip, 'mes'); }); }); });
})(typeof window !== 'undefined' ? window : global);
