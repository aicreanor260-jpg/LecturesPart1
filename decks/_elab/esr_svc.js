/* Сервисы ESR для лаб 6.x: DHCP-сервер, DHCP relay, Source/Destination NAT, NTP-клиент + модель часов.
   Синтаксис — по лабораторным NTF2 (6.1–6.4) и справочнику ESR-Series CLI. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, S = EL.esr, cmd = S.cmd;

  // ---------------------------------------------------------------- часы: у каждого устройства смещение от «мирового» времени
  var MON = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек'];
  var DOW = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
  function p2(n) { return ('0' + n).slice(-2); }
  EL.clock = {
    tzMs: function (tz) { return tz ? (+tz) * 3600e3 : 0; },
    fmt: function (ms) { var d = new Date(ms);
      return d.getUTCFullYear() + '-' + p2(d.getUTCMonth() + 1) + '-' + p2(d.getUTCDate()) + ' ' + p2(d.getUTCHours()) + ':' + p2(d.getUTCMinutes()) + ':' + p2(d.getUTCSeconds()); },
    linux: function (ms, tz) { var d = new Date(ms + tz * 3600e3);
      return DOW[d.getUTCDay()] + ' ' + p2(d.getUTCDate()) + ' ' + MON[d.getUTCMonth()] + ' ' + d.getUTCFullYear() + ' ' + p2(d.getUTCHours()) + ':' +
             p2(d.getUTCMinutes()) + ':' + p2(d.getUTCSeconds()) + ' ' + (tz >= 0 ? '+' : '-') + p2(Math.abs(tz)); }
  };

  ['dhcp', 'snat', 'snatrs', 'snatr', 'dnat', 'dnatrs', 'dnatr', 'ntps'].forEach(function (m) { S.PROMPT[m] = null; });
  S.PROMPT.dhcp = '(config-dhcp-server)#'; S.PROMPT.snat = '(config-snat)#'; S.PROMPT.snatrs = '(config-snat-ruleset)#';
  S.PROMPT.snatr = '(config-snat-rule)#'; S.PROMPT.dnat = '(config-dnat)#'; S.PROMPT.dnatrs = '(config-dnat-ruleset)#';
  S.PROMPT.dnatr = '(config-dnat-rule)#'; S.PROMPT.ntps = '(config-ntp-server)#';
  var NEW = 'dhcp snat snatrs snatr dnat dnatrs dnatr ntps';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes = c.modes.concat(NEW.split(' ')); });
  function touch(st) { st.pending = true; }
  var UP = { dhcp: 'config', snat: 'config', snatrs: 'snat', snatr: 'snatrs', dnat: 'config', dnatrs: 'dnat', dnatr: 'dnatrs', ntps: 'config' };
  cmd(NEW, 'exit', function (st) { st.mode = UP[st.mode]; st.ctx = st.mode === 'snatrs' || st.mode === 'dnatrs' ? st.natRs : null; }, 'Выход на уровень выше');
  function range(s) {                         // "192.168.1.1-192.168.1.254" → [a, b]
    var m = String(s).match(/^(\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+)$/);
    if (!m || IP.ip2n(m[1]) === null || IP.ip2n(m[2]) === null || IP.ip2n(m[1]) > IP.ip2n(m[2])) return null;
    return [m[1], m[2]];
  }
  function ifArg(st, w) { var n = EL.esr.ifName(w); return n && !n.range && st.cand.ifs[n.name] ? n.name : null; }

  // ---------------------------------------------------------------- DHCP-сервер
  function dh(st) { return st.cand.dhcp || (st.cand.dhcp = { on: false, pools: {} }); }
  cmd('config', 'ip dhcp-server', function (st) { dh(st).on = true; touch(st); }, 'Включить DHCP-сервер');
  cmd('config', 'no ip dhcp-server', function (st) { dh(st).on = false; touch(st); });
  cmd('config', 'ip dhcp-server pool <w>', function (st, a) { var d = dh(st);
    if (!d.pools[a[0]]) d.pools[a[0]] = { net: null, range: null, gw: null, dns: null, lease: null };
    touch(st); st.mode = 'dhcp'; st.ctx = a[0]; }, 'Пул адресов DHCP');
  cmd('config', 'no ip dhcp-server pool <w>', function (st, a) { delete dh(st).pools[a[0]]; touch(st); });
  function pool(st) { return st.cand.dhcp.pools[st.ctx]; }
  cmd('dhcp', 'network <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return '% Формат: network A.B.C.D/длина';
    pool(st).net = IP.netOf(c.ip, c.len); touch(st); }, 'Сеть пула');
  cmd('dhcp', 'address-range <w>', function (st, a) { var r = range(a[0]); if (!r) return '% Формат: address-range A.B.C.D-A.B.C.D';
    pool(st).range = r; touch(st); }, 'Диапазон выдаваемых адресов');
  cmd('dhcp', 'default-router <ip>', function (st, a) { pool(st).gw = a[0]; touch(st); }, 'Шлюз по умолчанию для клиентов');
  cmd('dhcp', 'dns-server <ip>', function (st, a) { pool(st).dns = a[0]; touch(st); }, 'DNS-сервер для клиентов');
  cmd('dhcp', 'default-lease-time <w>', function (st, a) { if (!/^\d+:\d+:\d+$/.test(a[0])) return '% Формат: дни:часы:минуты, например 0:1:0';
    pool(st).lease = a[0]; touch(st); }, 'Время аренды');
  cmd('priv', 'show ip dhcp binding', function (st) {
    var L = st.leases || {}, ks = Object.keys(L);
    return ['IP address       MAC address         Lease expires   State', '---------------- ------------------- --------------- ------']
      .concat(ks.map(function (k) { return (L[k] + '                 ').slice(0, 17) + EL.mac(k + 'eth0') + '   00:59:58        Active'; })).join('\n') +
      (ks.length ? '' : '\n% Выданных адресов нет'); }, 'Выданные адреса DHCP');
  cmd('priv', 'show ip dhcp server pool', function (st) { var d = st.run.dhcp;
    if (!d) return '% DHCP-сервер не настроен';
    return Object.keys(d.pools).map(function (k) { var p = d.pools[k];
      return 'Pool ' + k + '\n  network ' + (p.net || '-') + '\n  address-range ' + (p.range ? p.range.join('-') : '-') + '\n  default-router ' + (p.gw || '-'); }).join('\n'); });

  // ---------------------------------------------------------------- DHCP relay
  cmd('config', 'ip dhcp-relay', function (st) { st.cand.relay = true; touch(st); }, 'Включить DHCP-ретранслятор');
  cmd('config', 'no ip dhcp-relay', function (st) { st.cand.relay = false; touch(st); });
  cmd('gi sub', 'ip helper-address <ip>', function (st, a) {
    (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { st.cand.ifs[k].helper = a[0]; }); touch(st); }, 'Адрес DHCP-сервера для ретрансляции');
  cmd('gi sub', 'no ip helper-address', function (st) {
    (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { delete st.cand.ifs[k].helper; }); touch(st); });

  // ---------------------------------------------------------------- NAT
  function nat(st, k) { return st.cand[k] || (st.cand[k] = { rulesets: {} }); }
  cmd('config', 'nat source', function (st) { nat(st, 'snat'); touch(st); st.mode = 'snat'; }, 'Source NAT');
  cmd('config', 'nat destination', function (st) { nat(st, 'dnat'); touch(st); st.mode = 'dnat'; }, 'Destination NAT');
  cmd('snat dnat', 'ruleset <w>', function (st, a) { var k = st.mode, n = nat(st, k);
    if (!n.rulesets[a[0]]) n.rulesets[a[0]] = { ifn: null, rules: {} };
    touch(st); st.mode = k + 'rs'; st.ctx = st.natRs = a[0]; }, 'Набор правил');
  function rs(st) { return st.cand[st.mode.slice(0, 4)].rulesets[st.natRs]; }
  cmd('snatrs', 'to interface <w>', function (st, a) { var n = ifArg(st, a[0]); if (!n) return '% Неверный интерфейс';
    rs(st).ifn = n; touch(st); }, 'Интерфейс, куда уходит трафик');
  cmd('dnatrs', 'from interface <w>', function (st, a) { var n = ifArg(st, a[0]); if (!n) return '% Неверный интерфейс';
    rs(st).ifn = n; touch(st); }, 'Интерфейс, откуда приходит трафик');
  cmd('snatrs dnatrs', 'rule <n>', function (st, a) { var r = rs(st);
    if (!r.rules[a[0]]) r.rules[a[0]] = { on: false };
    touch(st); st.mode = st.mode.slice(0, 4) + 'r'; st.ctx = a[0]; }, 'Правило');
  function rule(st) { return st.cand[st.mode.slice(0, 4)].rulesets[st.natRs].rules[st.ctx]; }
  cmd('snatr dnatr', 'match source-address address-range <w>', function (st, a) { var r = range(a[0]);
    if (!r) return '% Формат: A.B.C.D-A.B.C.D'; rule(st).src = r; touch(st); }, 'Условие: адрес источника');
  cmd('snatr dnatr', 'match destination-address address-range <w>', function (st, a) { var r = range(a[0]);
    if (!r) return '% Формат: A.B.C.D-A.B.C.D'; rule(st).dst = r; touch(st); }, 'Условие: адрес назначения');
  cmd('snatr dnatr', 'match protocol <w>', function (st, a) { var p = a[0].toLowerCase();
    if (['tcp', 'udp', 'icmp', 'any'].indexOf(p) < 0) return '% Протокол: tcp | udp | icmp | any'; rule(st).proto = p; touch(st); }, 'Условие: протокол');
  cmd('snatr dnatr', 'match destination-port port-range <w>', function (st, a) {
    var m = String(a[0]).match(/^(\d+)(?:-(\d+))?$/); if (!m) return '% Порт или диапазон: 80 или 8000-8080';
    rule(st).dport = [+m[1], +(m[2] || m[1])]; touch(st); }, 'Условие: порт назначения');
  cmd('snatr', 'action source-nat interface', function (st) { rule(st).act = 'interface'; touch(st); }, 'Подменять источник адресом выходного интерфейса');
  cmd('dnatr', 'action destination-nat netmap <w>', function (st, a) { var c = IP.parseCidr(a[0]);
    if (!c) return '% Формат: netmap A.B.C.D/32'; rule(st).to = c.ip; touch(st); }, 'Куда перенаправить');
  cmd('snatr dnatr', 'enable', function (st) { rule(st).on = true; touch(st); }, 'Включить правило');
  cmd('snatr dnatr', 'no enable', function (st) { rule(st).on = false; touch(st); });
  cmd('priv', 'show ip nat translations', function (st) {
    var ct = (st.net && st.net.ctLast || []).filter(function (c) { return c.dev === st.dev; });
    return ['Prot  Inside source         Outside source        Type', '----  --------------------  --------------------  ----']
      .concat(ct.map(function (c) { return (c.proto + '    ').slice(0, 6) + (c.kind === 's' ? c.orig + ' → ' + c.pub : c.pub + ' → ' + c.target) + '   ' + (c.kind === 's' ? 'SNAT' : 'DNAT'); }))
      .join('\n') + (ct.length ? '' : '\n% Трансляций нет — отправьте трафик (ping) через маршрутизатор'); }, 'Последние трансляции NAT');

  // ---------------------------------------------------------------- NTP
  function ntp(st) { return st.cand.ntp || (st.cand.ntp = { on: false, servers: {} }); }
  cmd('config', 'ntp enable', function (st) { ntp(st).on = true; touch(st); }, 'Включить NTP-клиент');
  cmd('config', 'no ntp enable', function (st) { ntp(st).on = false; touch(st); });
  cmd('config', 'ntp server <ip>', function (st, a) { var n = ntp(st); if (!n.servers[a[0]]) n.servers[a[0]] = { minpoll: 6, maxpoll: 10 };
    touch(st); st.mode = 'ntps'; st.ctx = a[0]; }, 'NTP-сервер');
  cmd('config', 'no ntp server <ip>', function (st, a) { delete ntp(st).servers[a[0]]; touch(st); });
  cmd('ntps', 'minpoll <n>', function (st, a) { if (a[0] < 1 || a[0] > 10) return '% Значение 1–10 (степень двойки, секунды)';
    st.cand.ntp.servers[st.ctx].minpoll = a[0]; touch(st); }, 'Минимальный интервал опроса 2^N с');
  cmd('ntps', 'maxpoll <n>', function (st, a) { if (a[0] < 1 || a[0] > 10) return '% Значение 1–10';
    st.cand.ntp.servers[st.ctx].maxpoll = a[0]; touch(st); }, 'Максимальный интервал опроса 2^N с');
  cmd('ntps', 'prefer', function (st) { st.cand.ntp.servers[st.ctx].prefer = true; touch(st); });
  cmd('priv', 'show ntp peers', function (st) { return st.net ? st.net.ntpText(st.dev) : ''; }, 'Состояние NTP');

  // ---------------------------------------------------------------- running-config
  S.RUNX.push(function (c, o) {
    if (c.dhcp) { if (c.dhcp.on) o.push('ip dhcp-server');
      Object.keys(c.dhcp.pools).forEach(function (k) { var p = c.dhcp.pools[k]; o.push('ip dhcp-server pool ' + k);
        if (p.net) o.push('  network ' + p.net); if (p.range) o.push('  address-range ' + p.range.join('-'));
        if (p.gw) o.push('  default-router ' + p.gw); if (p.dns) o.push('  dns-server ' + p.dns); if (p.lease) o.push('  default-lease-time ' + p.lease); o.push('exit'); }); }
    if (c.relay) o.push('ip dhcp-relay');
    [['snat', 'nat source', 'to'], ['dnat', 'nat destination', 'from']].forEach(function (k) { var n = c[k[0]]; if (!n) return;
      o.push(k[1]);
      Object.keys(n.rulesets).forEach(function (r) { var x = n.rulesets[r]; o.push('  ruleset ' + r);
        if (x.ifn) o.push('    ' + k[2] + ' interface ' + S.longIf(x.ifn));
        Object.keys(x.rules).forEach(function (q) { var y = x.rules[q]; o.push('    rule ' + q);
          if (y.proto) o.push('      match protocol ' + y.proto); if (y.src) o.push('      match source-address address-range ' + y.src.join('-'));
          if (y.dst) o.push('      match destination-address address-range ' + y.dst.join('-'));
          if (y.dport) o.push('      match destination-port port-range ' + (y.dport[0] === y.dport[1] ? y.dport[0] : y.dport.join('-')));
          if (y.act) o.push('      action source-nat interface'); if (y.to) o.push('      action destination-nat netmap ' + y.to + '/32');
          if (y.on) o.push('      enable'); o.push('    exit'); });
        o.push('  exit'); });
      o.push('exit'); });
    if (c.ntp) { if (c.ntp.on) o.push('ntp enable');
      Object.keys(c.ntp.servers).forEach(function (k) { var x = c.ntp.servers[k]; o.push('ntp server ' + k, '  minpoll ' + x.minpoll, '  maxpoll ' + x.maxpoll, 'exit'); }); }
  });

  // ---------------------------------------------------------------- switchport и Bridge (экзамен NTF2: R1 gi1/0/3 + Bridge 100)
  S.PROMPT.evlan = '(config-vlan)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('evlan'); });
  cmd('evlan', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  cmd('config', 'vlan <list>', function (st, a) {
    if (a[0].some(function (v) { return v < 2 || v > 4094; })) return '% VLAN 2–4094';
    st.cand.vlans = st.cand.vlans || {}; a[0].forEach(function (v) { st.cand.vlans[v] = true; }); touch(st); st.mode = 'evlan'; st.ctx = a[0]; }, 'Создать VLAN');
  cmd('config', 'no vlan <list>', function (st, a) { st.cand.vlans = st.cand.vlans || {}; a[0].forEach(function (v) { delete st.cand.vlans[v]; }); touch(st); });
  function each(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }
  cmd('gi', 'mode switchport', function (st) { each(st, function (x) { x.sw = x.sw || { vlan: 1 }; x.ip = null; }); }, 'Порт в режим коммутатора');
  cmd('gi', 'mode routerport', function (st) { each(st, function (x) { delete x.sw; }); }, 'Порт в режим маршрутизатора');
  cmd('gi', 'switchport mode access', function (st) {
    if ((Array.isArray(st.ctx) ? st.ctx : [st.ctx]).some(function (k) { return !st.cand.ifs[k].sw; })) return '% Сначала mode switchport';
    each(st, function (x) { x.sw.mode = 'access'; }); }, 'Режим access');
  cmd('gi', 'switchport access vlan <n>', function (st, a) {
    if ((Array.isArray(st.ctx) ? st.ctx : [st.ctx]).some(function (k) { return !st.cand.ifs[k].sw; })) return '% Сначала mode switchport';
    if (!(st.cand.vlans || {})[a[0]] && a[0] !== 1) return '% VLAN ' + a[0] + ' не создана';
    each(st, function (x) { x.sw.vlan = a[0]; }); }, 'VLAN порта');
  cmd('config', 'bridge <n>', function (st, a) {
    st.cand.bridges[a[0]] = st.cand.bridges[a[0]] || { vlan: null, ip: null, fw: true, on: false };
    touch(st); st.mode = 'bridge'; st.ctx = a[0]; }, 'Интерфейс Bridge');
  cmd('config', 'no bridge <n>', function (st, a) { delete st.cand.bridges[a[0]]; touch(st); });
  function br(st) { return st.cand.bridges[st.ctx]; }
  cmd('bridge', 'vlan <n>', function (st, a) { br(st).vlan = a[0]; touch(st); }, 'Привязать VLAN к мосту');
  cmd('bridge', 'ip address <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return '% Формат: A.B.C.D/длина';
    br(st).ip = c.ip + '/' + c.len; touch(st); }, 'IP-адрес моста');
  cmd('bridge', 'ip firewall disable', function (st) { br(st).fw = false; touch(st); }, 'Отключить межсетевой экран');
  cmd('bridge', 'enable', function (st) { br(st).on = true; touch(st); }, 'Включить мост');
  cmd('bridge', 'no enable', function (st) { br(st).on = false; touch(st); });
  S.RUNX.push(function (c, o) {
    var vl = Object.keys(c.vlans || {}); if (vl.length) o.push('vlan ' + vl.join(','), 'exit');
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k]; if (!x.sw) return;
      o.push('interface ' + S.longIf(k), '  mode switchport', '  switchport access vlan ' + x.sw.vlan, 'exit'); });
    Object.keys(c.bridges || {}).forEach(function (k) { var b = c.bridges[k]; o.push('bridge ' + k);
      if (b.vlan) o.push('  vlan ' + b.vlan); if (!b.fw) o.push('  ip firewall disable'); if (b.ip) o.push('  ip address ' + b.ip); if (b.on) o.push('  enable'); o.push('exit'); });
  });
})(typeof window !== 'undefined' ? window : global);
