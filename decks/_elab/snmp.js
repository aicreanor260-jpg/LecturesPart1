/* SNMP: агент на ESR и MES, менеджер и приёмник трапов на Debian.
   ESR (справочник CLI 1.23): snmp-server · snmp-server community NAME [ro|rw] [ADDR] [v1|v2c] · snmp-server host ADDR · snmp-server enable traps ·
     snmp-server location / contact. Запросы к самому ESR проходят межсетевой экран (zone-pair … self, UDP 161).
   MES 6.x (руководство 6.6.8.8): snmp-server server · snmp-server community NAME [ro|rw|su] [ADDR] · snmp-server host ADDR [traps|informs] [version 1|2c] COMMUNITY ·
     snmp-server enable traps · snmp-server location / contact.
   MES 10.x (руководство 10.4.6, раздел 3.6.2.3): snmp-server enable|disable (включён) · snmp user U · snmp community index N name NAME security U ·
     snmp group G user U security-model v2c · snmp access G v2c read V write V notify V · snmp view V OID included ·
     snmp targetaddr T param P ADDR taglist TAG · snmp targetparams P user U security-model v2c message-processing v2c · snmp notify N tag TAG type Trap.
   Debian (net-snmp): snmpwalk / snmpget / snmpset -v1|-v2c -c COMMUNITY ADDR [OID]; приём трапов — systemctl start snmptrapd, журнал /var/log/snmptrapd.log.
   MIB: system (sysDescr, sysObjectID, sysUpTime, sysContact, sysName, sysLocation) и interfaces (ifNumber, ifTable: ifIndex, ifDescr, ifType, ifMtu, ifSpeed,
     ifPhysAddress, ifAdminStatus, ifOperStatus, ifInOctets, ifInUcastPkts, ifOutOctets, ifOutUcastPkts). snmpset (rw) меняет sysContact/sysName/sysLocation.
   Трапы: coldStart (включение), linkDown / linkUp (линк порта), authenticationFailure (неверная community).
   Упрощения: SNMPv3 (user с auth/priv) только хранится; view проверяется по наличию, без масок OID; MES 10.x — доступ по community, чья security-группа
   имеет access с read (write — для snmpset); OID предприятия Eltex (sysObjectID) — 1.3.6.1.4.1.35265 без номера модели. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, E = EL.E, P = EL.Net.prototype, H = EL.hosts, IP = EL.ip, CMDS = E.CMDS;
  function bad() { return 'Syntax error: Illegal parameter'; }
  function touch(st) { st.pending = true; }
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  // ---------------------------------------------------------------- ESR
  function ES(st) { return st.cand.snmp || (st.cand.snmp = { on: false, com: {}, hosts: [], traps: false }); }
  S.cmd('config', 'snmp-server', function (st) { ES(st).on = true; touch(st); }, 'Включить SNMP-агент');
  S.cmd('config', 'no snmp-server', function (st) { ES(st).on = false; touch(st); });
  S.cmd('config', 'snmp-server community <w>', function (st, a) { ES(st).com[a[0]] = { rw: false }; touch(st); }, 'Community (ro по умолчанию)');
  S.cmd('config', 'snmp-server community <w> <rest>', function (st, a) { var w = a[1].trim().split(/\s+/), o = { rw: false };
    for (var i = 0; i < w.length; i++) { if (w[i] === 'ro' || w[i] === 'rw') o.rw = w[i] === 'rw'; else if (w[i] === 'v1' || w[i] === 'v2c') o.ver = w[i]; else if (IP.ip2n(w[i]) !== null) o.addr = w[i]; else return bad(); }
    ES(st).com[a[0]] = o; touch(st); });
  S.cmd('config', 'no snmp-server community <w>', function (st, a) { delete ES(st).com[a[0]]; touch(st); });
  S.cmd('config', 'snmp-server host <ip>', function (st, a) { var h = ES(st).hosts; if (h.indexOf(a[0]) < 0) h.push(a[0]); touch(st); }, 'Куда слать трапы');
  S.cmd('config', 'no snmp-server host <ip>', function (st, a) { ES(st).hosts = ES(st).hosts.filter(function (x) { return x !== a[0]; }); touch(st); });
  S.cmd('config', 'snmp-server enable traps', function (st) { ES(st).traps = true; touch(st); }, 'Отправлять трапы');
  S.cmd('config', 'no snmp-server enable traps', function (st) { ES(st).traps = false; touch(st); });
  ['location', 'contact'].forEach(function (k) {
    S.cmd('config', 'snmp-server ' + k + ' <rest>', function (st, a) { ES(st)[k] = a[0].replace(/^"|"$/g, ''); touch(st); }, k === 'location' ? 'Местоположение (sysLocation)' : 'Контакт (sysContact)');
    S.cmd('config', 'no snmp-server ' + k, function (st) { delete ES(st)[k]; touch(st); }); });
  S.RUNX.push(function (c, o) { var s = c.snmp; if (!s) return;
    Object.keys(s.com).forEach(function (n) { var x = s.com[n]; o.push('snmp-server community ' + n + (x.rw ? ' rw' : ' ro') + (x.addr ? ' ' + x.addr : '') + (x.ver ? ' ' + x.ver : '')); });
    s.hosts.forEach(function (h) { o.push('snmp-server host ' + h); }); if (s.location) o.push('snmp-server location ' + s.location); if (s.contact) o.push('snmp-server contact ' + s.contact);
    if (s.traps) o.push('snmp-server enable traps'); if (s.on) o.push('snmp-server'); });
  // ---------------------------------------------------------------- MES 6.x
  function MS(st) { return st.snmp || (st.snmp = { on: st.dialect === '10', com: {}, hosts: [], traps: false, users: {}, groups: {}, access: {}, views: {}, taddr: {}, tparams: {}, notify: {} }); }
  mcmd(['6'], 'config', 'snmp-server server', function (st) { MS(st).on = true; }, 'Включить SNMP');
  mcmd(['6'], 'config', 'no snmp-server server', function (st) { MS(st).on = false; });
  mcmd(['6'], 'config', 'snmp-server community <w>', function (st, a) { MS(st).com[a[0]] = { rw: false }; }, 'Community (ro по умолчанию)');
  mcmd(['6'], 'config', 'snmp-server community <w> <rest>', function (st, a) { var w = a[1].trim().split(/\s+/), o = { rw: false };
    for (var i = 0; i < w.length; i++) { if (/^(ro|rw|su)$/.test(w[i])) o.rw = w[i] !== 'ro'; else if (IP.ip2n(w[i]) !== null) o.addr = w[i]; else if (w[i] === 'mask' || w[i] === 'view') i++; else return '% Invalid input'; }
    MS(st).com[a[0]] = o; });
  mcmd(['6'], 'config', 'no snmp-server community <w>', function (st, a) { delete MS(st).com[a[0]]; });
  mcmd(['6'], 'config', 'snmp-server host <ip> <rest>', function (st, a) { var w = a[1].trim().split(/\s+/), com = w[w.length - 1];
    MS(st).hosts = MS(st).hosts.filter(function (h) { return h.ip !== a[0]; }).concat([{ ip: a[0], com: com, inform: w.indexOf('informs') >= 0 }]); }, 'Получатель трапов: … [version 2c] COMMUNITY');
  mcmd(['6'], 'config', 'no snmp-server host <ip>', function (st, a) { MS(st).hosts = MS(st).hosts.filter(function (h) { return h.ip !== a[0]; }); });
  mcmd(['6', '10'], 'config', 'snmp-server enable traps', function (st) { MS(st).traps = true; }, 'Отправлять трапы');
  mcmd(['6', '10'], 'config', 'no snmp-server enable traps', function (st) { MS(st).traps = false; });
  ['location', 'contact'].forEach(function (k) {
    mcmd(['6', '10'], 'config', 'snmp-server ' + k + ' <rest>', function (st, a) { MS(st)[k] = a[0].replace(/^"|"$/g, ''); });
    mcmd(['6', '10'], 'config', 'no snmp-server ' + k, function (st) { delete MS(st)[k]; }); });
  // ---------------------------------------------------------------- MES 10.x
  mcmd(['10'], 'config', 'snmp-server enable', function (st) { MS(st).on = true; }, 'Включить SNMP-сервер (включён по умолчанию)');
  mcmd(['10'], 'config', 'snmp-server disable', function (st) { MS(st).on = false; }, 'Выключить SNMP-сервер');
  mcmd(['10'], 'config', 'snmp user <w>', function (st, a) { MS(st).users[a[0]] = {}; }, 'Пользователь SNMP');
  mcmd(['10'], 'config', 'snmp user <w> <rest>', function (st, a) { MS(st).users[a[0]] = { v3: a[1] }; });
  mcmd(['10'], 'config', 'snmp community index <n> name <w> security <w>', function (st, a) { MS(st).com[a[1]] = { idx: a[0], sec: a[2] }; }, 'Community → пользователь');
  mcmd(['10'], 'config', 'no snmp community index <n>', function (st, a) { var c = MS(st).com; Object.keys(c).forEach(function (k) { if (c[k].idx === a[0]) delete c[k]; }); });
  mcmd(['10'], 'config', 'snmp group <w> user <w> security-model <w>', function (st, a) { MS(st).groups[a[1]] = a[0]; }, 'Пользователь → группа');
  mcmd(['10'], 'config', 'snmp access <w> <w> <rest>', function (st, a) { var w = a[1] === 'v3' ? a[2].split(/\s+/).slice(1) : a[2].trim().split(/\s+/), o = {};
    for (var i = 0; i + 1 < w.length; i += 2) o[w[i]] = w[i + 1] === 'none' ? null : w[i + 1]; MS(st).access[a[0]] = o; }, 'Права группы: read V write V notify V');
  mcmd(['10'], 'config', 'snmp view <w> <w> <w>', function (st, a) { MS(st).views[a[0]] = { oid: a[1], inc: a[2] === 'included' }; }, 'Представление (дерево OID)');
  mcmd(['10'], 'config', 'snmp targetaddr <w> param <w> <ip> <rest>', function (st, a) { var m = a[3].match(/taglist (\S+)/); MS(st).taddr[a[0]] = { param: a[1], ip: a[2], tag: m ? m[1] : null }; }, 'Получатель трапов');
  mcmd(['10'], 'config', 'snmp targetaddr <w> param <w> <ip>', function (st, a) { MS(st).taddr[a[0]] = { param: a[1], ip: a[2], tag: null }; });
  mcmd(['10'], 'config', 'snmp targetparams <w> user <w> <rest>', function (st, a) { MS(st).tparams[a[0]] = { user: a[1] }; }, 'Параметры отправки трапов');
  mcmd(['10'], 'config', 'snmp notify <w> tag <w> type <w>', function (st, a) { MS(st).notify[a[0]] = { tag: a[1], type: a[2] }; }, 'Какие трапы и куда (по тегу)');
  E.RUNX.push(function (st, o) { var s = st.snmp; if (!s) return;
    if (st.dialect === '6') { if (s.on) o.push('snmp-server server');
      Object.keys(s.com).forEach(function (n) { var x = s.com[n]; o.push('snmp-server community ' + n + (x.rw ? ' rw' : ' ro') + (x.addr ? ' ' + x.addr : '')); });
      s.hosts.forEach(function (h) { o.push('snmp-server host ' + h.ip + (h.inform ? ' informs' : ' traps') + ' version 2c ' + h.com); }); }
    else { if (!s.on) o.push('snmp-server disable');
      Object.keys(s.users).forEach(function (u) { o.push('snmp user ' + u + (s.users[u].v3 ? ' ' + s.users[u].v3 : '')); });
      Object.keys(s.com).forEach(function (n) { o.push('snmp community index ' + s.com[n].idx + ' name ' + n + ' security ' + s.com[n].sec); });
      Object.keys(s.groups).forEach(function (u) { o.push('snmp group ' + s.groups[u] + ' user ' + u + ' security-model v2c'); });
      Object.keys(s.access).forEach(function (g) { var x = s.access[g]; o.push('snmp access ' + g + ' v2c' + ['read', 'write', 'notify'].map(function (k) { return k in x ? ' ' + k + ' ' + (x[k] || 'none') : ''; }).join('')); });
      Object.keys(s.views).forEach(function (v) { o.push('snmp view ' + v + ' ' + s.views[v].oid + (s.views[v].inc ? ' included' : ' excluded')); });
      Object.keys(s.taddr).forEach(function (t) { var x = s.taddr[t]; o.push('snmp targetaddr ' + t + ' param ' + x.param + ' ' + x.ip + (x.tag ? ' taglist ' + x.tag : '')); });
      Object.keys(s.tparams).forEach(function (p) { o.push('snmp targetparams ' + p + ' user ' + s.tparams[p].user + ' security-model v2c message-processing v2c'); });
      Object.keys(s.notify).forEach(function (n) { o.push('snmp notify ' + n + ' tag ' + s.notify[n].tag + ' type ' + s.notify[n].type); }); }
    if (s.location) o.push('snmp-server location ' + s.location); if (s.contact) o.push('snmp-server contact ' + s.contact); if (s.traps) o.push('snmp-server enable traps'); });

  // ---------------------------------------------------------------- агент: конфигурация, права, MIB
  function agent(d) { if (d.off) return null; if (d.type === 'esr' && d.sub !== 'me') { var c = d.st.run.snmp; return c && c.on ? { c: c, esr: true } : null; }
    if (d.type === 'mes') { var m = d.st.snmp || (d.st.dialect === '10' ? { on: true, com: {} } : null); return m && m.on ? { c: m, esr: false } : null; } return null; }
  function rights(d, A, com, src) {             // null — community не подходит; иначе {rw}
    var x = A.c.com[com]; if (!x) return null; if (x.addr && x.addr !== src) return null;
    if (d.type === 'mes' && d.st.dialect === '10') { var g = (A.c.groups || {})[x.sec], ac = g && (A.c.access || {})[g]; if (!ac || !ac.read || !(A.c.views || {})[ac.read]) return null;
      return { rw: !!(ac.write && A.c.views[ac.write]) }; }
    return { rw: !!x.rw };
  }
  var lx0 = EL.listensX;
  EL.listensX = function (d, proto, port) { if (proto === 'udp' && port === 161 && (d.type === 'esr' || d.type === 'mes')) return !!agent(d);
    if (proto === 'udp' && port === 162 && d.type === 'deb') return !!(d.st.svc || {}).snmptrapd;      // приёмник трапов
    return lx0 ? lx0(d, proto, port) : undefined; };
  function ifList(s, id) { var d = s.devs[id]; return d.type === 'mes' ? Object.keys(d.st.ports) : Object.keys(d.st.run.ifs).filter(function (k) { return k.indexOf('.') < 0; }); }
  function host(d) { return d.type === 'esr' ? d.st.run.host : d.st.host; }
  function mib(s, id) {                          // [[OID, имя, тип, значение]] по возрастанию OID
    var d = s.devs[id], A = agent(d), m = EL.MODELS[d.model] || {}, up = Math.max(0, Math.floor((s.now - (d.boot || 0)) * 100)), o = [];
    o.push(['1.3.6.1.2.1.1.1.0', 'SNMPv2-MIB::sysDescr.0', 'STRING', 'Eltex ' + d.model + (m.sw ? ', ' + m.sw : '')]);
    o.push(['1.3.6.1.2.1.1.2.0', 'SNMPv2-MIB::sysObjectID.0', 'OID', 'SNMPv2-SMI::enterprises.35265']);
    o.push(['1.3.6.1.2.1.1.3.0', 'DISMAN-EVENT-MIB::sysUpTimeInstance', 'Timeticks', '(' + up + ') ' + Math.floor(up / 8640000) + ' days, ' + new Date(up * 10).toISOString().slice(11, 22)]);
    o.push(['1.3.6.1.2.1.1.4.0', 'SNMPv2-MIB::sysContact.0', 'STRING', A.c.contact || '']);
    o.push(['1.3.6.1.2.1.1.5.0', 'SNMPv2-MIB::sysName.0', 'STRING', host(d)]);
    o.push(['1.3.6.1.2.1.1.6.0', 'SNMPv2-MIB::sysLocation.0', 'STRING', A.c.location || '']);
    var L = ifList(s, id); o.push(['1.3.6.1.2.1.2.1.0', 'IF-MIB::ifNumber.0', 'INTEGER', String(L.length)]);
    var COL = [[1, 'ifIndex', 'INTEGER'], [2, 'ifDescr', 'STRING'], [3, 'ifType', 'INTEGER'], [4, 'ifMtu', 'INTEGER'], [5, 'ifSpeed', 'Gauge32'], [6, 'ifPhysAddress', 'STRING'],
      [7, 'ifAdminStatus', 'INTEGER'], [8, 'ifOperStatus', 'INTEGER'], [10, 'ifInOctets', 'Counter32'], [11, 'ifInUcastPkts', 'Counter32'], [16, 'ifOutOctets', 'Counter32'], [17, 'ifOutUcastPkts', 'Counter32']];
    COL.forEach(function (cl) { L.forEach(function (p, i) { var ix = i + 1, c = s.ctrOf(id, p), ph = s.phys ? s.phys(id, p) : { up: false }, shut = d.type === 'mes' ? (d.st.ports[p] || {}).shut : (d.st.run.ifs[p] || {}).shut;
      var v = { 1: ix, 2: p, 3: 'ethernetCsmacd(6)', 4: 1500, 5: ph.up ? ph.speed * 1e6 : 0, 6: s.ifMac ? s.ifMac(id, { name: p, port: p }).replace(/(^|:)0/g, '$1') : '', 7: shut ? 'down(2)' : 'up(1)',
        8: s.linkUp(id, p) ? 'up(1)' : 'down(2)', 10: c.io, 11: c.iu, 16: c.oo, 17: c.ou }[cl[0]];
      o.push(['1.3.6.1.2.1.2.2.1.' + cl[0] + '.' + ix, 'IF-MIB::' + cl[1] + '.' + ix, cl[2], String(v)]); }); });
    return o;
  }
  var NAMES = { system: '1.3.6.1.2.1.1', interfaces: '1.3.6.1.2.1.2', iftable: '1.3.6.1.2.1.2.2', sysdescr: '1.3.6.1.2.1.1.1', sysuptime: '1.3.6.1.2.1.1.3', syscontact: '1.3.6.1.2.1.1.4',
    sysname: '1.3.6.1.2.1.1.5', syslocation: '1.3.6.1.2.1.1.6', ifdescr: '1.3.6.1.2.1.2.2.1.2', ifoperstatus: '1.3.6.1.2.1.2.2.1.8', ifinoctets: '1.3.6.1.2.1.2.2.1.10', ifoutoctets: '1.3.6.1.2.1.2.2.1.16' };
  function oidOf(w) { if (!w) return '1.3.6.1.2.1'; var q = String(w).replace(/^\./, '').replace(/^(SNMPv2-MIB|IF-MIB|DISMAN-EVENT-MIB)::/i, ''), m = q.match(/^([A-Za-z]+)(\.[\d.]+)?$/);
    if (m && NAMES[m[1].toLowerCase()]) return NAMES[m[1].toLowerCase()] + (m[2] || ''); if (/^sysUpTimeInstance$/i.test(q)) return '1.3.6.1.2.1.1.3.0'; return /^[\d.]+$/.test(q) ? q.replace(/^iso/, '1') : null; }

  // ---------------------------------------------------------------- трапы: события устройства → snmptrapd на сервере
  function trapDest(d, A) { if (!A.c.traps) return [];
    if (A.esr) return (A.c.hosts || []).map(function (h) { return { ip: h, com: Object.keys(A.c.com)[0] || 'public' }; });
    if (d.st.dialect === '6') return (A.c.hosts || []).map(function (h) { return { ip: h.ip, com: h.com }; });
    var tags = Object.keys(A.c.notify || {}).map(function (n) { return A.c.notify[n].tag; });
    return Object.keys(A.c.taddr || {}).map(function (t) { return A.c.taddr[t]; }).filter(function (x) { return !x.tag || tags.indexOf(x.tag) >= 0; }).map(function (x) { return { ip: x.ip, com: 'public' }; }); }
  P.snmpTrap = function (id, what, extra) {
    var s = this, d = s.devs[id], A = d && agent(d); if (!A) return;
    trapDest(d, A).forEach(function (t) { var r = s.request(id, t.ip, 'udp', 162); if (!r || !r.ok) return; var sd = s.devs[r.dev]; if (!sd || sd.type !== 'deb' || !(sd.st.svc || {}).snmptrapd) return;
      var f = sd.st.files = sd.st.files || {}, k = '/var/log/snmptrapd.log', src = (s.ifaces(id)[0] || {}).ip || '?';
      f[k] = (f[k] ? f[k] + '\n' : '') + EL.clock.fmt(EL.clock.now()) + ' ' + host(d) + ' [UDP: [' + src + ']:161->[' + t.ip + ']:162]:\nDISMAN-EVENT-MIB::sysUpTimeInstance = Timeticks: (' +
        Math.floor((s.now - (d.boot || 0)) * 100) + ')\tSNMPv2-MIB::snmpTrapOID.0 = OID: ' + what + (extra ? '\t' + extra : '') + '\tcommunity ' + t.com; }); };
  // события линка — из ленты событий консоли (console.js пишет _evlog): каждое новое событие link → trap
  var tick0 = P.tick; P.tick = function () { var r = tick0.apply(this, arguments); flush(this); return r; };
  var ex0 = P.exec; P.exec = function () { var r = ex0.apply(this, arguments); flush(this); return r; };
  function flush(s) { var L = s._evlog || []; if (s._snmpEv === undefined) s._snmpEv = L.length;
    for (var i = s._snmpEv; i < L.length; i++) { var e = L[i]; if (e.k !== 'link') continue; var d = s.byName(e.dev); if (!d) continue;
      var m = e.msg.match(/(gi|te|fa|tw|twe|fo|hu)\s?(\d+\/\d+\/\d+)/), port = m ? m[1] + m[2] : null, idx = port ? ifList(s, d.id).indexOf(port) + 1 : 0;
      s.snmpTrap(d.id, /DOWN|Down/.test(e.msg) ? 'IF-MIB::linkDown' : 'IF-MIB::linkUp', idx ? 'IF-MIB::ifIndex.' + idx + ' = INTEGER: ' + idx : ''); }
    s._snmpEv = L.length; }
  var pw0 = P.power; P.power = function (id, on) { var r = pw0.apply(this, arguments); if (on) this.snmpTrap(id, 'SNMPv2-MIB::coldStart'); return r; };

  // ---------------------------------------------------------------- Debian: net-snmp
  function req(st, ip, com, ver) {               // {err} или {d, A, rw}
    var s = st.net, r = s.request(st.dev, ip, 'udp', 161);
    if (!r.ok) return { err: 'Timeout: No Response from ' + ip + '.' };
    var d = s.devs[r.dev], A = agent(d); if (!A) return { err: 'Timeout: No Response from ' + ip + '.' };
    var src = (s.ifaces(st.dev)[0] || {}).ip, R = rights(d, A, com, src);
    if (!R || (A.c.com[com] && A.c.com[com].ver && ver && A.c.com[com].ver !== ver)) { s.snmpTrap(d.id, 'SNMPv2-MIB::authenticationFailure'); return { err: 'Timeout: No Response from ' + ip + '.' }; }
    return { d: d, A: A, rw: R.rw };
  }
  function line(x) { return x[1] + ' = ' + x[2] + ': ' + (x[2] === 'STRING' ? x[3] : x[3]); }
  function parse(t) { var o = { ver: null, com: null, args: [] }; for (var i = 1; i < t.length; i++) { if (t[i] === '-v') o.ver = 'v' + t[++i]; else if (/^-v/.test(t[i])) o.ver = 'v' + t[i].slice(2);
    else if (t[i] === '-c') o.com = t[++i]; else if (/^-c./.test(t[i])) o.com = t[i].slice(2); else if (/^-O/.test(t[i])) { /* формат вывода */ } else o.args.push(t[i]); } return o; }
  var deb0 = H.debExec;
  H.debExec = function (st, raw) {
    var line0 = String(raw).trim(), t = line0.split(/\s+/), c = t[0];
    if (st.user && !st.ssh && st.net && /^snmp(walk|get|set|bulkwalk)$/.test(c)) {
      var o = parse(t); if (!o.ver || !o.com || !o.args[0]) return 'USAGE: ' + c + ' [OPTIONS] AGENT [OID]\n  -v 1|2c   версия SNMP\n  -c COMMUNITY   строка сообщества';
      if (!st.up) return 'Timeout: No Response from ' + o.args[0] + '.';
      var q = req(st, o.args[0], o.com, o.ver === 'v2' ? 'v2c' : o.ver); if (q.err) return q.err;
      var M = mib(st.net, q.d.id), oid = oidOf(o.args[1]); if (oid === null) return o.args[1] + ': Unknown Object Identifier';
      if (c === 'snmpget') { var x = M.filter(function (r) { return r[0] === oid; })[0]; return x ? line(x) : o.args[1] + ' = No Such Instance currently exists at this OID'; }
      if (c === 'snmpset') { if (!q.rw) return 'Error in packet.\nReason: noAccess'; var v = o.args.slice(3).join(' ').replace(/^"|"$/g, ''), k = { '1.3.6.1.2.1.1.4.0': 'contact', '1.3.6.1.2.1.1.5.0': 'host', '1.3.6.1.2.1.1.6.0': 'location' }[oid];
        if (!k || o.args[2] !== 's') return 'Error in packet.\nReason: notWritable (That object does not support modification)';
        if (k === 'host') st.net.setHost(q.d.id, v); else { q.A.c[k] = v; if (q.A.esr) { q.d.st.cand.snmp = q.d.st.cand.snmp || EL.clone(q.A.c); q.d.st.cand.snmp[k] = v; } }
        st.net.gen++; return line(M.filter(function (r) { return r[0] === oid; })[0].slice(0, 3).concat([v])); }
      var rows = M.filter(function (r) { return r[0] === oid || r[0].indexOf(oid + '.') === 0; });
      return rows.length ? rows.map(line).join('\n') : (o.args[1] || '') + ' = No more variables left in this MIB View (It is past the end of the MIB tree)';
    }
    return deb0.apply(this, arguments);
  };
  var debF = H.deb; H.deb = function () { var st = debF.apply(this, arguments); if (st.svc) st.svc.snmptrapd = false; return st; };
  // show snmp (ESR) — сводка
  S.cmd('priv', 'show snmp', function (st) { var c = st.run.snmp; if (!c || !c.on) return '% SNMP-агент выключен — snmp-server';
    return ['SNMP agent: enabled', 'Communities: ' + Object.keys(c.com).map(function (n) { return n + (c.com[n].rw ? ' (rw)' : ' (ro)'); }).join(', '),
      'Trap hosts: ' + (c.hosts.join(', ') || '—') + (c.traps ? '' : ' (traps disabled)'), 'Location: ' + (c.location || '—'), 'Contact: ' + (c.contact || '—')].join('\n'); }, 'Настройки SNMP');
})(typeof window !== 'undefined' ? window : global);
