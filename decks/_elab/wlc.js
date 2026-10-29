/* Контроллер Wi-Fi Eltex WLC и точки доступа WEP/WOP (спецификация sources/eltex/spec/wlc.md: РЭ и Troubleshooting guide WLC 1.39.2,
   дерево команд прошивки vWLC 1.39.2, РЭ WEP-3ax 1.17.1). CLI WLC — ESR (диалект 'wlc') плюс режимы config-wlc*, radius-server local,
   softgre-controller, tunnel softgre, DHCP опция 43 (vendor-specific → suboption 12 / 15).
   Точка доступа получает адрес по DHCP вместе с опцией 43; по подопции 15 (https://<адрес>:8043) идёт на контроллер (TCP 8043),
   адрес должен совпадать с outside-address. Дальше: aps join auto — подключение сразу (иначе join wlc ap <MAC>), локация — по ap <MAC>
   или ip-pool (network, по умолчанию 0.0.0.0/0); нет локации — Sandboxed; всё есть — Active, пароль ТД — из ap-profile.
   Заводская конфигурация — по РЭ §10.1.1 (решение автора, вариант А).
   Упрощения (в источниках нет или вне учебной модели — помечено): переходы статусов Registering → … → Active сжаты в один шаг;
   синхронизация времени и сертификаты не проверяются; клиенты Wi-Fi не моделируются (show wlc clients пуст); туннели SoftGRE
   и local-switching только хранятся в конфигурации; trunk на портах WLC хранится, кадры не передаёт; ip address dhcp на мосту
   хранится, адрес не запрашивается; номера правил межсетевого экрана в заводской конфигурации условные; радиоблоки в detailed не выводятся;
   у ТД один порт «LAN» (имя условное), CLI ТД — только настройка IP (РЭ WEP-3ax §6.2). */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, T = S.T, IP = EL.ip;
  function touch(st) { st.pending = true; }
  function scmd(modes, pat, fn, d) { S.cmd(modes, pat, fn, d); var c = T.pop(); c.dl = ['wlc']; T.unshift(c); return c; }
  function isWlc(d) { return !!d && d.sub === 'wlc'; }
  function isAp(d) { return !!d && d.sub === 'ap'; }

  // ---------------------------------------------------------------- дерево конфигурации WLC: блок {L: строки, K: вложенные блоки}
  var PR = { wlc: 'wlc', wrad: 'wlc-radius-profile', wssid: 'wlc-ssid-profile', wapp: 'wlc-ap-profile', wappntp: 'wlc-ap-profile-ntp', wappsvc: 'wlc-ap-profile-services',
    wr2g: 'wlc-radio-2g-profile', wr5g: 'wlc-radio-5g-profile', wr6g: 'wlc-radio-6g-profile', wloc: 'wlc-ap-location', wpool: 'wlc-ip-pool', wsa: 'wlc-service-activator',
    wap: 'wlc-ap', radius: 'radius', rnas: 'radius-nas', rdom: 'radius-domain', ruser: 'radius-user', rvs: 'radius-vserver', rsrv: 'radius-server',
    aaarp: 'aaa-radius-profile', sgc: 'softgre-controller', sgre: 'softgre', dhcpvs: 'dhcp-server-vendor-specific' };
  Object.keys(PR).forEach(function (k) { S.PROMPT[k] = '(config-' + PR[k] + ')#'; });
  T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') Object.keys(PR).forEach(function (k) { c.modes.push(k); }); });
  function root(st) { return st.cand.wtree || (st.cand.wtree = { L: {}, K: {} }); }
  function node(st, path) { var n = root(st); (path || st.ctx.p).forEach(function (h) { n = n.K[h]; }); return n; }
  function text(pat, a) { var i = 0; return pat.split(' ').map(function (w) { return /^</.test(w) ? (Array.isArray(a[i]) ? EL.E.fmtList(a[i++]) : a[i++]) : w; }).join(' '); }
  // вход в блок: из режима parent в child; заголовок блока — строка команды
  function ent(parent, pat, child, check) {
    scmd(parent, pat, function (st, a) { if (check) { var e = check(a); if (e) return e; }
      var h = text(pat, a), base = parent === 'config' ? { p: [], m: [] } : st.ctx, n = node(st, base.p);
      n.K[h] = n.K[h] || { L: {}, K: {} }; touch(st); st.mode = child; st.ctx = { p: base.p.concat(h), m: base.m.concat(parent) }; });
    scmd(parent, 'no ' + pat, function (st, a) { var n = parent === 'config' ? root(st) : node(st); delete n.K[text(pat, a)]; touch(st); });
  }
  // строка внутри блока: ключ — слова до первого параметра (MULTI — несколько значений: band 2g, band 5g …)
  var MULTI = { band: 1, 'ssid-profile': 1, 'service-vlan add': 1, 'radius-server host': 1 };
  function key(pat) { var w = []; pat.split(' ').some(function (x) { if (/^</.test(x)) return true; w.push(x); return false; }); return w.join(' '); }
  function fld(mode, pat, check) {
    var k = key(pat);
    scmd(mode, pat, function (st, a) { if (check) { var e = check(a); if (e) return e; } var t = text(pat, a); node(st).L[MULTI[k] ? t : k] = t; touch(st); });
    if (!/^no /.test(pat)) scmd(mode, 'no ' + k, function (st) { var n = node(st); Object.keys(n.L).forEach(function (x) { if (x === k || x.indexOf(k + ' ') === 0) delete n.L[x]; }); touch(st); });
  }
  function oneOf(L, i) { return function (a) { return L.indexOf(String(a[i || 0])) < 0 ? 'Syntax error: Illegal parameter' : null; }; }
  ent('config', 'wlc', 'wlc'); ent('config', 'radius-server local', 'radius'); ent('config', 'radius-server host <ip>', 'rsrv');
  ent('config', 'aaa radius-profile <w>', 'aaarp'); ent('config', 'softgre-controller', 'sgc');
  ent('config', 'tunnel softgre <n>', 'sgre', function (a) { return a[0] < 1 ? 'Syntax error: Illegal parameter' : null; });
  [['radius-profile', 'wrad'], ['ssid-profile', 'wssid'], ['ap-profile', 'wapp'], ['radio-2g-profile', 'wr2g'], ['radio-5g-profile', 'wr5g'], ['radio-6g-profile', 'wr6g'],
   ['ap-location', 'wloc'], ['ip-pool', 'wpool']].forEach(function (x) { ent('wlc', x[0] + ' <w>', x[1]); });
  ent('wlc', 'service-activator', 'wsa');
  ent('wlc', 'ap <w>', 'wap', function (a) { return /^[0-9a-f]{2}(:[0-9a-f]{2}){5}$/i.test(a[0]) ? null : 'Syntax error: Illegal parameter'; });
  ent('wapp', 'ntp', 'wappntp'); ent('wapp', 'services', 'wappsvc');
  ent('radius', 'nas <w>', 'rnas'); ent('radius', 'domain <w>', 'rdom'); ent('radius', 'virtual-server <w>', 'rvs'); ent('rdom', 'user <w>', 'ruser');
  var TX = ['minimal', 'low', 'middle', 'high', 'maximal'];
  fld('wlc', 'enable'); fld('wlc', 'outside-address <ip>');
  fld('wrad', 'auth-address <w>'); fld('wrad', 'auth-password ascii-text <w>'); fld('wrad', 'domain <w>');
  fld('wssid', 'description <rest>'); fld('wssid', 'ssid <rest>'); fld('wssid', 'vlan-id <n>', function (a) { return a[0] < 1 || a[0] > 4094 ? 'Syntax error: Illegal parameter' : null; });
  fld('wssid', 'security-mode <w>', oneOf(['OWE', 'WPA', 'WPA2', 'WPA2_1X', 'WPA2_WPA3', 'WPA2_WPA3_1X', 'WPA3', 'WPA3_1X', 'WPA_1X', 'WPA_WPA2', 'WPA_WPA2_1X', 'off']));
  fld('wssid', 'radius-profile <w>'); fld('wssid', '802.11kv'); fld('wssid', 'band <w>', oneOf(['2g', '5g', '6g'])); fld('wssid', 'enable');
  fld('wssid', 'local-switching'); fld('wssid', 'key-wpa ascii-text <w>', function (a) { return a[0].length < 8 || a[0].length > 63 ? 'Syntax error: Illegal parameter' : null; });
  fld('wapp', 'password ascii-text <w>'); fld('wappntp', 'auto-config'); fld('wappsvc', 'ip ssh server'); fld('wappsvc', 'ip telnet server'); fld('wappsvc', 'ip http server');
  [['wr2g', ['bg', 'nax', 'bgnax', 'bgnaxbe'], ['20', '40L', '40U']], ['wr5g', ['anacax', 'anacaxbe'], ['20', '40L', '40U', '80', '160']],
   ['wr6g', ['ax', 'axbe'], ['20', '40L', '40U', '80', '160', '320']]].forEach(function (x) {
    fld(x[0], 'limit-channels <w>'); fld(x[0], 'work-mode <w>', oneOf(x[1])); fld(x[0], 'bandwidth <w>', oneOf(x[2])); fld(x[0], 'tx-power <w>', oneOf(TX)); });
  fld('wr5g', 'dfs <w>', oneOf(['auto', 'disabled', 'forced']));
  fld('wloc', 'description <rest>'); fld('wloc', 'radio-2g-profile <w>'); fld('wloc', 'radio-5g-profile <w>'); fld('wloc', 'radio-6g-profile <w>');
  fld('wloc', 'ap-profile <w>'); fld('wloc', 'ssid-profile <w>'); fld('wloc', 'mode tunnel');
  fld('wpool', 'description <rest>'); fld('wpool', 'network <w>', function (a) { return IP.parseCidr(a[0]) ? null : 'Syntax error: Illegal parameter'; }); fld('wpool', 'ap-location <w>');
  fld('wsa', 'aps join auto'); fld('wap', 'ap-location <w>'); fld('wap', 'ap-model <w>'); fld('wap', 'description <rest>');
  fld('radius', 'enable'); fld('rnas', 'key ascii-text <w>'); fld('rnas', 'network <w>'); fld('ruser', 'password ascii-text <w>'); fld('rvs', 'enable');
  fld('rsrv', 'key ascii-text <w>'); fld('aaarp', 'radius-server host <ip>');
  fld('sgc', 'nas-ip-address <ip>'); fld('sgc', 'data-tunnel configuration <w>', oneOf(['local', 'radius', 'wlc'])); fld('sgc', 'aaa radius-profile <w>');
  fld('sgc', 'keepalive-disable'); fld('sgc', 'service-vlan add <list>'); fld('sgc', 'enable');
  fld('sgre', 'mode <w>', oneOf(['data', 'management'])); fld('sgre', 'local address <ip>'); fld('sgre', 'default-profile'); fld('sgre', 'enable');
  scmd(Object.keys(PR).filter(function (k) { return k !== 'dhcpvs'; }).join(' '), 'exit', function (st) {
    var c = st.ctx; if (!c || !c.p || c.p.length < 2) { st.mode = 'config'; st.ctx = null; return; }
    st.mode = c.m[c.m.length - 1]; st.ctx = { p: c.p.slice(0, -1), m: c.m.slice(0, -1) }; });

  // ---------------------------------------------------------------- общие ESR-команды, нужные WLC
  function fl(st) { return st.cand.wflags || (st.cand.wflags = {}); }
  scmd('config', 'ntp master', function (st) { fl(st)['ntp master'] = 1; touch(st); }, 'NTP-сервер для точек доступа');
  scmd('config', 'no ntp broadcast-client enable', function (st) { fl(st)['no ntp broadcast-client enable'] = 1; touch(st); });
  scmd('config', 'ip http server', function (st) { fl(st)['ip http server'] = 1; touch(st); });
  scmd('config', 'ip firewall disable', function (st) { fl(st)['ip firewall disable'] = 1; touch(st); });
  scmd('evlan', 'force-up', function (st) { st.cand.vforce = st.cand.vforce || {}; [].concat(st.ctx).forEach(function (v) { st.cand.vforce[v] = true; }); touch(st); }, 'VLAN всегда в состоянии up');
  function br(st) { return st.cand.bridges[st.ctx]; }
  scmd('bridge', 'ip address dhcp', function (st) { br(st).dhcp = true; br(st).ip = null; touch(st); }, 'Адрес моста по DHCP');
  scmd('bridge', 'no spanning-tree', function (st) { br(st).nostp = true; touch(st); });
  scmd('bridge', 'mtu <n>', function (st, a) { if (a[0] < 552 || a[0] > 9018) return 'Syntax error: Illegal parameter'; br(st).mtu = a[0]; touch(st); }, 'MTU моста');
  scmd('bridge', 'description <rest>', function (st, a) { br(st).desc = a[0]; touch(st); });
  function swAll(st) { return (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).map(function (k) { return st.cand.ifs[k]; }); }
  scmd('gi', 'switchport mode trunk', function (st) { if (swAll(st).some(function (x) { return !x.sw; })) return 'Syntax error: Unknown command';   // А: сначала mode switchport
    swAll(st).forEach(function (x) { x.sw.mode = 'trunk'; x.sw.allowed = x.sw.allowed || []; }); touch(st); }, 'Режим trunk');
  scmd('gi', 'switchport trunk allowed vlan add <list>', function (st, a) { if (swAll(st).some(function (x) { return !x.sw || x.sw.mode !== 'trunk'; })) return 'Syntax error: Unknown command';
    swAll(st).forEach(function (x) { a[0].forEach(function (v) { if (x.sw.allowed.indexOf(v) < 0) x.sw.allowed.push(v); }); }); touch(st); });
  scmd('snatrs', 'to zone <w>', function (st, a) { st.cand.snat.rulesets[st.natRs].zone = a[0]; st.cand.snat.rulesets[st.natRs].ifn = null; touch(st); }, 'Зона, куда уходит трафик');
  scmd('snatr', 'description <rest>', function (st, a) { var rs = st.cand.snat.rulesets[st.natRs], r = rs && rs.rules[st.ctx]; if (r) r.desc = a[0]; touch(st); });
  // DHCP: vendor-specific (опция 43) и option N
  function pool(st) { return st.cand.dhcp.pools[st.ctx]; }
  scmd('dhcp', 'vendor-specific', function (st) { pool(st).vs = pool(st).vs || {}; touch(st); st.mode = 'dhcpvs'; }, 'Опция 43 (vendor specific)');
  scmd('dhcpvs', 'suboption <n> ascii-text <rest>', function (st, a) { if (a[0] > 255) return 'Syntax error: Illegal parameter';
    pool(st).vs[a[0]] = String(a[1]).replace(/^"(.*)"$/, '$1'); touch(st); }, 'Подопция: 12 — адрес туннеля, 15 — URL контроллера');
  scmd('dhcpvs', 'no suboption <n>', function (st, a) { delete pool(st).vs[a[0]]; touch(st); });
  scmd('dhcpvs', 'exit', function (st) { st.mode = 'dhcp'; });
  scmd('dhcp', 'option <n> ip-address <ip>', function (st, a) { if (a[0] > 255) return 'Syntax error: Illegal parameter'; (pool(st).opts = pool(st).opts || {})[a[0]] = a[1]; touch(st); }, 'Опция DHCP (42 — NTP)');

  // running-config: дерево WLC, флаги, дополнения к блокам ESR
  function dump(n, ind, o) { Object.keys(n.L).forEach(function (k) { o.push(ind + n.L[k]); });
    Object.keys(n.K).forEach(function (h) { o.push(ind + h); dump(n.K[h], ind + '  ', o); o.push(ind + 'exit'); }); }
  S.RUNX.push(function (c, o) {
    Object.keys(c.wflags || {}).forEach(function (k) { o.push(k); });
    Object.keys(c.vforce || {}).forEach(function (v) { o.push('vlan ' + v, '  force-up', 'exit'); });
    Object.keys(c.dhcp && c.dhcp.pools || {}).forEach(function (k) { var p = c.dhcp.pools[k], i = o.indexOf('ip dhcp-server pool ' + k); if (i < 0) return;
      var j = i; while (j < o.length && o[j] !== 'exit') j++; var add = [];
      Object.keys(p.opts || {}).forEach(function (q) { add.push('  option ' + q + ' ip-address ' + p.opts[q]); });
      if (p.vs) { add.push('  vendor-specific'); Object.keys(p.vs).forEach(function (q) { add.push('    suboption ' + q + ' ascii-text "' + p.vs[q] + '"'); }); add.push('  exit'); }
      o.splice.apply(o, [j, 0].concat(add)); });
    Object.keys(c.bridges || {}).forEach(function (k) { var b = c.bridges[k], i = o.indexOf('bridge ' + k); if (i < 0) return; var add = [];
      if (b.desc) add.push('  description ' + b.desc); if (b.dhcp) add.push('  ip address dhcp'); if (b.nostp) add.push('  no spanning-tree'); if (b.mtu) add.push('  mtu ' + b.mtu);
      o.splice.apply(o, [i + 1, 0].concat(add)); });
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k]; if (!x.sw || x.sw.mode !== 'trunk') return; var i = o.indexOf('interface ' + S.longIf(k)); if (i < 0) return;
      o.splice(i + 2, 1, '  switchport mode trunk'); if (x.sw.allowed.length) o.splice(i + 3, 0, '  switchport trunk allowed vlan add ' + EL.E.fmtList(x.sw.allowed)); });
    if (c.wtree) dump(c.wtree, '', o);
  });

  // ---------------------------------------------------------------- заводская конфигурация (РЭ §10.1.1, вариант А)
  var UNTR = { 'WLC-15': ['gi1/0/1', 'gi1/0/6'], 'WLC-30': ['gi1/0/1', 'te1/0/1', 'te1/0/2'], 'WLC-3200': ['twe1/0/1', 'twe1/0/2'], 'WLC-3250': ['gi1/0/1', 'twe1/0/1', 'twe1/0/2'], 'WLC-3350': ['gi1/0/1', 'twe1/0/1', 'twe1/0/2'] };
  function factory(model, ports) {
    var c = [], og = [['ssh', '22'], ['dns', '53'], ['dhcp_server', '67'], ['dhcp_client', '68'], ['ntp', '123'], ['netconf', '830'], ['radius_auth', '1812'],
      ['sa', '8043-8044'], ['airtune', '8099'], ['web', '443']];
    og.forEach(function (x) { c.push('object-group service ' + x[0], 'port-range ' + x[1], 'exit'); });
    c.push('security zone users', 'exit', 'security zone trusted', 'exit', 'security zone untrusted', 'exit');
    function pair(a, b, rules) { c.push('security zone-pair ' + a + ' ' + b); rules.forEach(function (r, i) { c.push('rule ' + (i + 1) * 10, 'action permit');
      if (r[0]) c.push('match protocol ' + r[0]); if (r[1]) c.push('match source-port object-group ' + r[1]); if (r[2]) c.push('match destination-port object-group ' + r[2]); c.push('enable', 'exit'); }); c.push('exit'); }
    pair('trusted', 'untrusted', [[]]); pair('trusted', 'trusted', [[]]);
    pair('trusted', 'self', [['tcp', null, 'ssh'], ['icmp'], ['udp', 'dhcp_client', 'dhcp_server'], ['udp', null, 'ntp'], ['tcp', null, 'dns'], ['udp', null, 'dns'], ['tcp', null, 'netconf'],
      ['tcp', null, 'sa'], ['udp', null, 'radius_auth'], ['gre'], ['tcp', null, 'airtune'], ['tcp', null, 'web']]);
    pair('users', 'self', [['icmp'], ['udp', 'dhcp_client', 'dhcp_server'], ['udp', null, 'dns']]);
    pair('untrusted', 'self', [['udp', 'dhcp_server', 'dhcp_client']]); pair('users', 'untrusted', [[]]);
    c.push('nat source', 'ruleset factory', 'to zone untrusted', 'rule 10', 'description "replace \'source ip\' by outgoing interface ip address"', 'action source-nat interface', 'enable', 'exit', 'exit', 'exit');
    c.push('vlan 2', 'exit', 'vlan 3', 'force-up', 'exit',
      'bridge 1', 'vlan 1', 'security-zone trusted', 'ip address 192.168.1.1/24', 'no spanning-tree', 'enable', 'exit',
      'bridge 2', 'vlan 2', 'security-zone untrusted', 'ip address dhcp', 'no spanning-tree', 'enable', 'exit',
      'bridge 3', 'security-zone users', 'ip address 192.168.2.1/24', 'no spanning-tree', 'vlan 3', 'mtu 1458', 'enable', 'exit');
    var un = UNTR[model] || [ports[0]];
    ports.forEach(function (p) { c.push('interface ' + p, 'mode switchport'); if (un.indexOf(p) >= 0) c.push('switchport access vlan 2'); c.push('exit'); });
    c.push('domain lookup enable', 'ip ssh server', 'tunnel softgre 1', 'mode data', 'local address 192.168.1.1', 'default-profile', 'enable', 'exit', 'ntp master', 'ntp enable',
      'ip dhcp-server pool ap-pool', 'network 192.168.1.0/24', 'address-range 192.168.1.2-192.168.1.254', 'default-router 192.168.1.1', 'dns-server 192.168.1.1',
      'vendor-specific', 'suboption 12 ascii-text "192.168.1.1"', 'suboption 15 ascii-text "https://192.168.1.1:8043"', 'exit', 'exit',
      'ip dhcp-server pool users-pool', 'network 192.168.2.0/24', 'address-range 192.168.2.2-192.168.2.254', 'default-router 192.168.2.1', 'dns-server 192.168.2.1', 'exit', 'ip dhcp-server',
      'radius-server local', 'nas ap', 'key ascii-text password', 'network 192.168.1.0/24', 'exit', 'nas local', 'key ascii-text password', 'network 127.0.0.1/32', 'exit',
      'domain default', 'exit', 'virtual-server default', 'enable', 'exit', 'enable', 'exit',
      'radius-server host 127.0.0.1', 'key ascii-text password', 'exit', 'aaa radius-profile default_radius', 'radius-server host 127.0.0.1', 'exit',
      'softgre-controller', 'nas-ip-address 127.0.0.1', 'data-tunnel configuration wlc', 'aaa radius-profile default_radius', 'keepalive-disable', 'service-vlan add 3', 'enable', 'exit',
      'wlc', 'radius-profile default-radius', 'auth-address 192.168.1.1', 'auth-password ascii-text password', 'domain default', 'exit',
      'ssid-profile default-ssid', 'description default-ssid', 'ssid default-ssid', 'vlan-id 3', 'security-mode WPA2_WPA3_1X', 'radius-profile default-radius', '802.11kv',
      'band 2g', 'band 5g', 'band 6g', 'enable', 'exit',
      'ap-profile default-ap', 'password ascii-text password', 'ntp', 'auto-config', 'exit', 'exit',
      'radio-2g-profile default_2g', 'limit-channels 1,6,11', 'work-mode bgnaxbe', 'bandwidth 20', 'tx-power maximal', 'exit',
      'radio-5g-profile default_5g', 'dfs forced', 'limit-channels 36,40,44,48,52,56,60,64', 'work-mode anacaxbe', 'bandwidth 20', 'tx-power maximal', 'exit',
      'radio-6g-profile default_6g', 'exit',
      'ap-location default-location', 'description default-location', 'radio-2g-profile default_2g', 'radio-5g-profile default_5g', 'radio-6g-profile default_6g',
      'ap-profile default-ap', 'ssid-profile default-ssid', 'mode tunnel', 'exit',
      'ip-pool default-ip-pool', 'description default-ip-pool', 'ap-location default-location', 'exit',
      'service-activator', 'aps join auto', 'exit', 'enable', 'outside-address 192.168.1.1', 'end');
    return c;
  }

  // ---------------------------------------------------------------- устройства
  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}, st = d.st;
    if (m.kind === 'wlc') {
      d.sub = 'wlc'; st.dialect = 'wlc'; st.mode = 'priv';
      var bad = []; ['configure'].concat(factory(model, m.portList)).forEach(function (l) { var r = S.exec(st, l); if (r && /^(%|Syntax)/.test(r)) bad.push(l + ' → ' + r); });
      st.cand.wflags = st.cand.wflags || {}; st.run = EL.clone(st.cand); st.pending = false; st.mode = 'priv'; st.ctx = null;
      if (bad.length && G.console) G.console.warn('WLC factory: ' + bad.join('; '));
      st.aps = {}; st.journal = [];
    }
    if (m.kind === 'ap') { d.sub = 'ap'; st.port = 'LAN'; st.up = true; st.apMode = 'dhcp'; st.apPw = 'password'; st.apCli = { stage: 'user', path: [] }; st.apCfg = {}; }
    return d;
  };
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id]; if (isAp(d)) { this.gen++; return d.off ? '' : apExec(this, d, String(line)); } return ex0.apply(this, arguments); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; if (!isAp(d)) return pr0.apply(this, arguments); var c = d.st.apCli;
    if (c.stage === 'user') return d.model + ' login: '; if (c.stage === 'pw') return 'Password: ';
    return d.model + '(' + (c.path.length || c.cfg ? 'config' : 'root') + '):/' + c.path.join('/') + '# '; };

  // ---------------------------------------------------------------- CLI точки доступа (РЭ WEP-3ax §6.2: настройка IP)
  function apExec(net, d, line) {
    var st = d.st, c = st.apCli, w = line.trim().split(/\s+/);
    if (c.stage === 'user') { c.u = line.trim(); c.stage = 'pw'; return ''; }
    if (c.stage === 'pw') { var ok = c.u === 'admin' && line === st.apPw; c.stage = ok ? 'cli' : 'user'; return ok ? '' : 'Login incorrect'; }
    if (!line.trim()) return '';
    var p = c.path.join('/'), cmd = w[0];
    if (cmd === 'exit') { if (c.path.length) c.path.pop(); else if (c.cfg) c.cfg = false; else { c.stage = 'user'; return ''; } return ''; }
    if (cmd === 'end') { c.path = []; c.cfg = false; return ''; }
    if (cmd === 'save') { if (c.pend) { Object.keys(c.pend).forEach(function (k) { st.apCfg[k] = c.pend[k]; }); c.pend = null; apApply(net, d); } return ''; }
    if (cmd === 'show-config') return Object.keys(st.apCfg).map(function (k) { return k + ' ' + st.apCfg[k]; }).join('\n');
    if (!c.cfg && !c.path.length) {
      if (cmd === 'configure') { c.cfg = true; return ''; }
      if (line.trim() === 'monitoring wan-status') return ['Common information:', 'interface | br0', 'mac | ' + EL.mac(EL.macKey(d) + 'LAN'), 'IPv4 information:', 'protocol | ' + (st.apMode === 'dhcp' ? 'dhcp' : 'static-ip'),
        'ip-address | ' + (st.ip || ''), 'netmask | ' + (st.ip ? IP.len2mask(st.len) : ''), 'gateway | ' + (st.gw || '')].join('\n');
      return 'Unknown command';
    }
    var nav = { '': ['interface', 'route'], interface: ['br0'], 'interface/br0': ['common'] };
    if (nav[p] && nav[p].indexOf(cmd) >= 0 && w.length === 1) { c.path.push(cmd); return ''; }
    if (p === 'route' && cmd === 'add' && w[1] === 'default') return '';
    if (p === 'route' && cmd === 'default' && w.length === 1) { c.path.push('default'); return ''; }
    c.pend = c.pend || {};
    var keys = { 'interface/br0/common': ['protocol', 'static-ip', 'netmask', 'dns-server-1', 'dns-server-2'], 'route/default': ['destination', 'netmask', 'gateway'] }[p] || [];
    if (keys.indexOf(cmd) >= 0 && w[1]) {
      if (cmd === 'protocol' && ['static-ip', 'dhcp'].indexOf(w[1]) < 0) return 'Invalid value';
      if (cmd !== 'protocol' && IP.ip2n(w[1]) === null) return 'Invalid value';
      c.pend[p.replace(/\//g, '.') + '.' + cmd] = w[1]; return ''; }
    return 'Unknown command';
  }
  function apApply(net, d) { var st = d.st, g = st.apCfg;
    if (g['interface.br0.common.protocol'] === 'static-ip' && g['interface.br0.common.static-ip']) {
      st.apMode = 'static'; st.ip = g['interface.br0.common.static-ip']; st.len = IP.mask2len(g['interface.br0.common.netmask'] || '255.255.255.0') || 24;
      st.gw = g['route.default.gateway'] || null; st.ap = null; }
    else if (g['interface.br0.common.protocol'] === 'dhcp') { st.apMode = 'dhcp'; st.ip = null; st.ap = null; }
    net.gen++; }

  // ---------------------------------------------------------------- регистрация ТД на контроллере
  // сервис-активатор WLC слушает TCP 8043–8044 (подопция 15: https://<адрес>:8043), когда включён wlc
  var lx0 = EL.listensX;
  EL.listensX = function (d, proto, port) {
    if (isWlc(d) && proto === 'tcp' && (port === 8043 || port === 8044)) { var wt = (d.st.run.wtree || { K: {} }).K.wlc; return !!(wt && wt.L.enable); }
    return lx0 ? lx0(d, proto, port) : undefined;
  };
  function val(n, k) { var t = n && n.L[k]; return t ? t.slice(k.length + 1) : null; }
  function W(d) { return d.st.run.wtree || { L: {}, K: {} }; }
  function sub(n, h) { return n && n.K[h]; }
  P.apSync = function () {
    var s = this;
    this.list().filter(isAp).forEach(function (d) {
      var st = d.st, mac = EL.mac(EL.macKey(d) + 'LAN');
      if (d.off || !s.linkUp(d.id, 'LAN')) { s.list().filter(isWlc).forEach(function (w) { var a = w.st.aps[mac]; if (a && a.status === 'Active') a.status = 'Lost'; }); return; }
      if (st.apMode === 'dhcp' && !st.ip) { var r = s.dhcp(d.id); if (!r.ok) return; st.ip = r.ip; st.len = r.len; st.gw = r.gw || null; st.up = true;
        st.opt43 = r.pool && r.pool.vs ? EL.clone(r.pool.vs) : {}; }
      var url = (st.opt43 || {})[15], m = url && String(url).match(/^https?:\/\/([\d.]+)(?::(\d+))?/); if (!m) return;
      var host = m[1], port = +(m[2] || 443), wid = s.owner(host), w = wid && s.devs[wid]; if (!isWlc(w)) return;
      var rq = s.request(d.id, host, 'tcp', port); if (!rq.ok) return;
      var wt = sub(W(w), 'wlc'), A = w.st.aps[mac] || (w.st.aps[mac] = { mac: mac, since: s.now });
      A.ip = st.ip; A.model = d.model; A.sw = (EL.MODELS[d.model] || {}).swv || '1.0.0'; A.dev = d.id;
      var old = A.status;
      if (!wt || !wt.L.enable) { A.status = 'Registering'; A.sa = 'awaited'; }
      else if (val(wt, 'outside-address') !== host) { A.status = 'Registering'; A.sa = 'registering'; A.why = 'certificate verify failed, reason: Hostname mismatch'; }
      else {
        var sa = sub(wt, 'service-activator'), auto = sa && sa.L['aps join auto'];
        A.sa = auto ? 'join-auto' : A.admin ? 'join-by-admin' : 'awaited';
        if (A.sa === 'awaited') A.status = 'Registering';
        else {
          var apn = sub(wt, 'ap ' + mac), loc = apn && val(apn, 'ap-location');
          if (!loc) Object.keys(wt.K).filter(function (h) { return /^ip-pool /.test(h); }).some(function (h) { var pn = wt.K[h], net = val(pn, 'network') || '0.0.0.0/0', cc = IP.parseCidr(net);
            if (cc && IP.sameNet(st.ip, cc.ip, cc.len) && val(pn, 'ap-location')) { loc = val(pn, 'ap-location'); return true; } return false; });
          var ln = loc && sub(wt, 'ap-location ' + loc);
          if (!ln) { A.status = 'Sandboxed'; A.loc = '--'; }
          else { A.status = 'Active'; A.loc = loc; var prof = sub(wt, 'ap-profile ' + val(ln, 'ap-profile')), pw = val(prof, 'password ascii-text'); if (pw) st.apPw = pw; }
        }
      }
      if (A.status !== old) { A.since = s.now; w.st.journal.push(EL.clock.fmt(EL.clock.now()) + ' AP ' + mac + ' status ' + A.status.toLowerCase() + ', AP model: ' + d.model + ', IP address: ' + st.ip); }
    });
  };
  // ---------------------------------------------------------------- show wlc …
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function up(s, a) { var t = Math.max(0, Math.floor(s.now - (a.since || 0))), p2 = function (n) { return ('0' + n).slice(-2); };
    return p2(Math.floor(t / 86400)) + ',' + p2(Math.floor(t / 3600) % 24) + ':' + p2(Math.floor(t / 60) % 60) + ':' + p2(t % 60); }
  var HEAD = rp('MAC address', 18) + rp('Status', 17) + rp('IP address', 16) + rp('SW version', 17) + rp('Hostname', 31) + rp('Ap-location', 31) + rp('Uptime', 17) + 'Clients',
      HEAD2 = rp('', 18 + 17 + 16 + 17 + 31 + 31 + 17) + '(2g/5g/6g/all)',
      SEP = ['-----------------', '----------------', '---------------', '----------------', '------------------------------', '------------------------------', '----------------', '-------------------'].join(' ');
  function apRows(st, net, all) {
    var A = st.aps || {}, o = Object.keys(A).filter(function (k) { return A[k].status !== 'Registering' && A[k].status !== 'Sandboxed' || all; }).map(function (k) { var a = A[k];
      return rp(a.mac, 18) + rp(a.status, 17) + rp(a.ip || '', 16) + rp(a.sw, 17) + rp(a.model, 31) + rp(a.loc || '--', 31) + rp(up(net, a), 17) + '0/0/-/0'; });
    if (all) { var wt = sub(st.run.wtree || { K: {} }, 'wlc') || { K: {} }; Object.keys(wt.K).forEach(function (h) { var m = h.match(/^ap (\S+)$/); if (m && !A[m[1]])
      o.push(rp(m[1], 18) + rp('Pre-configured', 17) + rp('', 16) + rp('', 17) + rp('', 31) + rp(val(wt.K[h], 'ap-location') || '--', 31) + rp('', 17) + '0/0/-/0'); }); }
    return [HEAD, HEAD2, SEP].concat(o).join('\n');
  }
  function detail(a) { return ['AP ' + a.mac + ':', 'MAC address:           ' + a.mac, 'Status:                ' + a.status, 'Status description:    ' + (a.why || '--'),
    'IP address:            ' + a.ip, 'Board type:            ' + a.model, 'SW version:            ' + a.sw].join('\n'); }
  function sync(st) { if (st.net) st.net.apSync(); }
  scmd('priv', 'show wlc ap', function (st) { sync(st); return apRows(st, st.net, false); }, 'Точки доступа на контроллере');
  scmd('priv', 'show wlc ap all', function (st) { sync(st); return apRows(st, st.net, true); }, 'Подключённые и заданные в конфигурации ТД');
  scmd('priv', 'show wlc ap detailed', function (st) { sync(st); var A = st.aps; return Object.keys(A).map(function (k) { return detail(A[k]); }).join('\n'); });
  scmd('priv', 'show wlc ap <w>', function (st, a) { sync(st); var w = String(a[0]).toLowerCase(), x = st.aps[w];
    if (w === 'all') return apRows(st, st.net, true); if (w === 'detailed') return Object.keys(st.aps).map(function (k) { return detail(st.aps[k]); }).join('\n'); return x ? [HEAD, HEAD2, SEP].concat(apRows(st, st.net).split('\n').filter(function (l) { return l.indexOf(x.mac) === 0; })).join('\n') : ''; });
  scmd('priv', 'show wlc ap <w> detailed', function (st, a) { sync(st); var w = String(a[0]).toLowerCase(), x = st.aps[w];
    if (w === 'all') return Object.keys(st.aps).map(function (k) { return detail(st.aps[k]); }).join('\n'); return x ? detail(x) : ''; });
  var SAST = ['all', 'registering', 'awaited', 'join-by-admin', 'join-auto', 'joined', 'upgrading_fw'];
  function saRows(st, f) { var A = st.aps, cap = function (s) { return s.charAt(0).toUpperCase() + s.slice(1); };
    return [rp('MAC address', 18) + rp('Status', 14) + rp('IP address', 16) + rp('Board type', 17) + rp('SW version', 17) + rp('HW version', 12) + 'Serial number',
      '----------------- ------------- --------------- ---------------- ---------------- ----------- --------------']
      .concat(Object.keys(A).filter(function (k) { return !f || f === 'all' || A[k].sa === f; }).map(function (k) { var a = A[k];
        return rp(a.mac, 18) + rp(cap(a.sa || ''), 14) + rp(a.ip, 16) + rp(a.model, 17) + rp(a.sw, 17) + rp('--', 12) + '--'; })).join('\n'); }
  scmd('priv', 'show wlc service-activator aps', function (st) { sync(st); return saRows(st); }, 'ТД в сервис-активаторе');
  scmd('priv', 'show wlc service-activator aps <w>', function (st, a) { if (SAST.indexOf(a[0]) < 0) return 'Syntax error: Illegal parameter'; sync(st); return saRows(st, a[0]); });
  scmd('priv', 'show wlc configuration warnings', function () { return 'No Message\n---- ' + new Array(80).join('-'); }, 'Предупреждения конфигурации');
  scmd('priv', 'show wlc ap firmware', function () { return rp('Board type', 33) + rp('Min SW version', 33) + 'Current SW version\nFilename'; }, 'ПО точек доступа на контроллере');
  scmd('priv', 'show wlc clients', function () { return ''; }, 'Клиенты Wi-Fi');
  scmd('priv', 'show wlc clients ap <w>', function () { return ''; });
  scmd('priv', 'show wlc journal ap', function (st) { sync(st); return st.journal.join('\n'); }, 'Журнал ТД');
  scmd('priv', 'show wlc journal clients', function () { return ''; });
  scmd('priv', 'renew wlc ap <w>', function (st, a) { if (!/^[0-9a-f]{2}(:[0-9a-f]{2}){5}$|^failed$|^all$/i.test(a[0])) return 'Syntax error: Illegal parameter'; var x = st.aps[String(a[0]).toLowerCase()]; if (x) { x.status = 'Reconnecting'; x.since = st.net ? st.net.now : 0; } sync(st); }, 'Переподключить ТД');
  scmd('priv', 'renew wlc ap failed', function (st) { sync(st); });
  scmd('priv', 'join wlc ap <w>', function (st, a) { var x = st.aps[String(a[0]).toLowerCase()]; if (x) x.admin = true; sync(st); }, 'Допустить ТД вручную');
  scmd('priv', 'join wlc ap', function (st) { Object.keys(st.aps).forEach(function (k) { st.aps[k].admin = true; }); sync(st); });
  scmd('priv', 'show running-config <rest>', function (st, a) { var all = S.showRun(st).split('\n'), want = String(a[0]).trim(), o = [], on = false;
    all.forEach(function (l) { if (!/^\s/.test(l) && l !== 'exit') on = l.indexOf(want) === 0 || (want === 'wlc' && l === 'wlc'); if (on) o.push(l); }); return o.join('\n'); });
})(typeof window !== 'undefined' ? window : global);
