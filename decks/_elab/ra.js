/* Удалённый доступ PPTP и L2TP over IPsec на ESR (справочник ESR-Series CLI 1.23).
   Сервер: remote-access pptp|l2tp ИМЯ → (config-pptp-server)# / (config-l2tp-server)#: local-address ip-address A | object-group G,
     remote-address address-range A-B | object-group G, outside-address ip-address A | interface IF | object-group G,
     authentication mode local | radius, authentication method chap|mschap|mschap-v2|eap|pap, dns-servers object-group G, mtu N, description,
     (L2TP) ipsec authentication method pre-shared-key, ipsec authentication pre-shared-key ascii-text КЛЮЧ,
     username ИМЯ → (config-pptp-user)# / (config-l2tp-user)#: password ascii-text ПАРОЛЬ, enable; enable.
   Клиент: tunnel pptp|l2tp N → (config-pptp)# / (config-l2tp)#: remote address A, username ИМЯ password ascii-text ПАРОЛЬ,
     (L2TP) ipsec authentication method pre-shared-key, ipsec authentication pre-shared-key ascii-text КЛЮЧ, ignore-default-route, mtu N, description, enable.
   show remote-access status | configuration pptp|l2tp ИМЯ; на клиенте туннель — в show tunnels status.
   Соединение: клиент шлёт запрос на outside-address сервера (PPTP — TCP 1723, L2TP — UDP 1701 внутри IPsec) по обычной сети
   (маршруты, NAT, межсетевой экран на пути), сервер проверяет ключ IPsec (L2TP), логин и пароль (локально или через RADIUS),
   выдаёт адрес из remote-address; у клиента — интерфейс pptp N / l2tp N с этим адресом, сосед — local-address сервера.
   Без ignore-default-route маршрут по умолчанию уходит в туннель, а до outside-address сервера остаётся маршрут через провайдера.
   Упрощения: шифрование MPPE/ESP и согласование PPP (LCP, IPCP) не показываются по шагам; межсетевой экран на интерфейсах
   удалённого доступа не проверяется (как ip firewall disable); счётчики сессий не ведутся. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  var PORT = { pptp: ['tcp', 1723], l2tp: ['udp', 1701] };
  var M = { rasp: '(config-pptp-server)#', rasl: '(config-l2tp-server)#', rup: '(config-pptp-user)#', rul: '(config-l2tp-user)#',
            rcp: '(config-pptp)#', rcl: '(config-l2tp)#' };
  Object.keys(M).forEach(function (k) { S.PROMPT[k] = M[k]; });
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes = c.modes.concat(Object.keys(M)); });
  function touch(st) { st.pending = true; }
  function bad() { return 'Syntax error: Illegal parameter'; }
  function R(c) { return c.ra || (c.ra = { srv: {}, cli: {} }); }
  function srv(st) { return R(st.cand).srv[st.raSrv]; }
  function cli(st) { return R(st.cand).cli[st.raCli]; }

  // ---------------------------------------------------------------- сервер
  ['pptp', 'l2tp'].forEach(function (T) {
    var m = T === 'pptp' ? 'rasp' : 'rasl', mu = T === 'pptp' ? 'rup' : 'rul', mc = T === 'pptp' ? 'rcp' : 'rcl';
    S.cmd('config', 'remote-access ' + T + ' <w>', function (st, a) { var k = T + ' ' + a[0], L = R(st.cand).srv;
      if (!L[k]) { L[k] = { type: T, name: a[0], users: {}, auth: 'local', method: 'chap' }; touch(st); }
      st.mode = m; st.raSrv = k; }, 'Сервер удалённого доступа ' + T.toUpperCase());
    S.cmd('config', 'no remote-access ' + T + ' <w>', function (st, a) { delete R(st.cand).srv[T + ' ' + a[0]]; touch(st); });
    S.cmd(m, 'username <w>', function (st, a) { var u = srv(st).users; u[a[0]] = u[a[0]] || { pw: null, on: false }; st.raUser = a[0]; st.mode = mu; touch(st); }, 'Пользователь удалённого доступа');
    S.cmd(m, 'no username <w>', function (st, a) { delete srv(st).users[a[0]]; touch(st); });
    S.cmd(mu, 'password ascii-text <w>', function (st, a) { if (a[0].length > 64) return bad(); srv(st).users[st.raUser].pw = a[0]; touch(st); }, 'Пароль пользователя');
    S.cmd(mu, 'no password', function (st) { srv(st).users[st.raUser].pw = null; touch(st); });
    S.cmd(mu, 'enable', function (st) { srv(st).users[st.raUser].on = true; touch(st); }, 'Включить пользователя');
    S.cmd(mu, 'no enable', function (st) { srv(st).users[st.raUser].on = false; touch(st); });
    S.cmd(mu, 'exit', function (st) { st.mode = m; st.raUser = null; });
    S.cmd(m, 'exit', function (st) { st.mode = 'config'; st.raSrv = null; });
    S.cmd(mc, 'exit', function (st) { st.mode = 'config'; st.raCli = null; });
    // клиент
    S.cmd('config', 'tunnel ' + T + ' <n>', function (st, a) { if (a[0] < 1 || a[0] > 10) return bad(); var k = T + ' ' + a[0], L = R(st.cand).cli;
      if (!L[k]) { L[k] = { type: T, n: a[0] }; touch(st); } st.mode = mc; st.raCli = k; }, 'Клиент удалённого доступа ' + T.toUpperCase());
    S.cmd('config', 'no tunnel ' + T + ' <n>', function (st, a) { delete R(st.cand).cli[T + ' ' + a[0]]; touch(st); });
  });
  var SRV = 'rasp rasl', CLI = 'rcp rcl';
  function ref(kind) { return function (st, a) { srv(st)[kind] = { og: a[0] }; touch(st); }; }
  S.cmd(SRV, 'local-address ip-address <ip>', function (st, a) { srv(st).local = { ip: a[0] }; touch(st); }, 'Адрес сервера в туннелях');
  S.cmd(SRV, 'local-address object-group <w>', ref('local'), 'Адрес сервера в туннелях (object-group)');
  S.cmd(SRV, 'remote-address address-range <w>', function (st, a) { var m = a[0].match(/^(\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+)$/);
    if (!m || IP.ip2n(m[1]) === null || IP.ip2n(m[2]) === null || IP.ip2n(m[1]) > IP.ip2n(m[2])) return bad(); srv(st).remote = { r: [m[1], m[2]] }; touch(st); }, 'Пул адресов клиентов A-B');
  S.cmd(SRV, 'remote-address object-group <w>', ref('remote'), 'Пул адресов клиентов (object-group)');
  S.cmd(SRV, 'outside-address ip-address <ip>', function (st, a) { srv(st).outside = { ip: a[0] }; touch(st); }, 'Адрес, на который подключаются клиенты');
  S.cmd(SRV, 'outside-address object-group <w>', ref('outside'), 'Адрес для подключения (object-group)');
  S.cmd(SRV, 'outside-address interface <rest>', function (st, a) { var k = S.ifName(a[0]); if (!k || !st.cand.ifs[k]) return bad(); srv(st).outside = { ifn: k }; touch(st); }, 'Адрес интерфейса для подключения');
  S.cmd(SRV, 'authentication mode <w>', function (st, a) { if (!/^(local|radius)$/.test(a[0])) return bad(); srv(st).auth = a[0]; touch(st); }, 'Проверка пользователей: local | radius');
  S.cmd(SRV, 'authentication method <w>', function (st, a) { if (!/^(chap|mschap|mschap-v2|eap|pap)$/.test(a[0])) return bad(); srv(st).method = a[0]; touch(st); }, 'Метод аутентификации PPP');
  S.cmd(SRV, 'dns-servers object-group <w>', function (st, a) { srv(st).dns = a[0]; touch(st); }, 'DNS-серверы для клиентов');
  S.cmd(SRV + ' ' + CLI, 'mtu <n>', function (st, a) { if (a[0] < 1280 || a[0] > 1500) return bad(); (st.raSrv && st.mode.charAt(1) === 'a' ? srv(st) : cli(st)).mtu = a[0]; touch(st); }, 'MTU туннелей');
  S.cmd(SRV + ' ' + CLI, 'description <rest>', function (st, a) { (st.mode.charAt(1) === 'a' ? srv(st) : cli(st)).desc = a[0].replace(/^"|"$/g, ''); touch(st); }, 'Описание');
  S.cmd(SRV + ' ' + CLI, 'enable', function (st) { (st.mode.charAt(1) === 'a' ? srv(st) : cli(st)).on = true; touch(st); }, 'Включить');
  S.cmd(SRV + ' ' + CLI, 'no enable', function (st) { (st.mode.charAt(1) === 'a' ? srv(st) : cli(st)).on = false; touch(st); });
  function o(st) { return st.mode.charAt(1) === 'a' ? srv(st) : cli(st); }
  S.cmd('rasl rcl', 'ipsec authentication method pre-shared-key', function (st) { o(st).psm = true; touch(st); }, 'IPsec: аутентификация по общему ключу');
  S.cmd('rasl rcl', 'ipsec authentication pre-shared-key ascii-text <w>', function (st, a) { if (a[0].length > 64) return bad(); o(st).psk = a[0]; touch(st); }, 'IPsec: общий ключ');
  S.cmd('rasl rcl', 'no ipsec authentication pre-shared-key', function (st) { o(st).psk = null; touch(st); });
  S.cmd(CLI, 'remote address <ip>', function (st, a) { cli(st).remote = a[0]; touch(st); }, 'Адрес сервера удалённого доступа');
  S.cmd(CLI, 'no remote address', function (st) { cli(st).remote = null; touch(st); });
  S.cmd(CLI, 'username <w> password ascii-text <w>', function (st, a) { cli(st).user = a[0]; cli(st).pw = a[1]; touch(st); }, 'Логин и пароль для подключения');
  S.cmd(CLI, 'no username <w>', function (st) { cli(st).user = cli(st).pw = null; touch(st); });
  S.cmd(CLI, 'ignore-default-route', function (st) { cli(st).noDef = true; touch(st); }, 'Не ставить маршрут по умолчанию в туннель');
  S.cmd(CLI, 'no ignore-default-route', function (st) { cli(st).noDef = false; touch(st); });

  S.RUNX.push(function (c, out) { var x = c.ra; if (!x) return;
    Object.keys(x.srv).sort().forEach(function (k) { var s = x.srv[k], ad = function (v) { return v.og ? 'object-group ' + v.og : v.ifn ? 'interface ' + S.longIf(v.ifn) : v.r ? 'address-range ' + v.r.join('-') : 'ip-address ' + v.ip; };
      out.push('remote-access ' + k); if (s.desc) out.push('  description "' + s.desc + '"');
      if (s.local) out.push('  local-address ' + ad(s.local)); if (s.remote) out.push('  remote-address ' + ad(s.remote)); if (s.outside) out.push('  outside-address ' + ad(s.outside));
      if (s.auth !== 'local') out.push('  authentication mode ' + s.auth); if (s.method !== 'chap') out.push('  authentication method ' + s.method);
      if (s.dns) out.push('  dns-servers object-group ' + s.dns); if (s.mtu) out.push('  mtu ' + s.mtu);
      if (s.psm) out.push('  ipsec authentication method pre-shared-key'); if (s.psk) out.push('  ipsec authentication pre-shared-key ascii-text ' + s.psk);
      Object.keys(s.users).forEach(function (u) { var y = s.users[u]; out.push('  username ' + u); if (y.pw) out.push('    password ascii-text ' + y.pw); if (y.on) out.push('    enable'); out.push('  exit'); });
      if (s.on) out.push('  enable'); out.push('exit'); });
    Object.keys(x.cli).sort().forEach(function (k) { var s = x.cli[k]; out.push('tunnel ' + k); if (s.desc) out.push('  description "' + s.desc + '"');
      if (s.remote) out.push('  remote address ' + s.remote); if (s.user) out.push('  username ' + s.user + ' password ascii-text ' + s.pw);
      if (s.psm) out.push('  ipsec authentication method pre-shared-key'); if (s.psk) out.push('  ipsec authentication pre-shared-key ascii-text ' + s.psk);
      if (s.noDef) out.push('  ignore-default-route'); if (s.mtu) out.push('  mtu ' + s.mtu); if (s.on) out.push('  enable'); out.push('exit'); }); });

  // ---------------------------------------------------------------- установление сессий
  function addr(net, id, c, v) {          // адрес из ip-address / object-group / interface
    if (!v) return null; if (v.ip) return v.ip; if (v.og) { var g = c.og && c.og.net[v.og]; return g && g.items[0] ? g.items[0][0] : null; }
    if (v.ifn) { var f = net.ifaces(id).filter(function (q) { return q.name === v.ifn; })[0]; return f ? f.ip : null; } return null;
  }
  function pool(c, v) { if (!v) return []; if (v.r) return [v.r]; var g = c.og && c.og.net[v.og]; return g ? g.items.map(function (x) { return [x[0], x[1]]; }) : []; }
  function server(net, dev, T, ip) {      // профиль сервера на устройстве, принимающий подключения на ip
    var d = net.devs[dev]; if (!d || d.type !== 'esr' || d.sub === 'me' || d.off) return null; var x = (d.st.run.ra || {}).srv || {};
    return Object.keys(x).map(function (k) { return x[k]; }).filter(function (s) { return s.type === T && addr(net, dev, d.st.run, s.outside) === ip; })[0] || null;
  }
  EL.listensX = (function (lx0) { return function (d, proto, port) {
    if (d.type === 'esr' && d.st.run && d.st.run.ra) { var on = Object.keys(d.st.run.ra.srv).some(function (k) { var s = d.st.run.ra.srv[k]; return s.on && PORT[s.type][0] === proto && PORT[s.type][1] === port; }); if (on) return true; }
    return lx0 ? lx0(d, proto, port) : undefined; }; })(EL.listensX);

  function connect(net, id, k, x, used) {
    var T = x.type, me = net.devs[id].name, pr = PORT[T];
    if (!x.on) return { err: 'туннель выключен (enable)' };
    if (!x.remote) return { err: 'не задан remote address' };
    if (!x.user) return { err: 'не заданы username и password' };
    var lu = net.lookup(id, x.remote); if (!lu) return { err: 'нет маршрута до сервера ' + x.remote };
    var steps = [], ct = [], f = net.send(id, { src: null, dst: x.remote, proto: pr[0], dport: pr[1], sport: 49999 }, steps, ct);
    if (!f.ok) return { err: 'сервер ' + x.remote + ' недоступен: ' + (steps.filter(function (q) { return q.k === 'drop'; }).map(function (q) { return q.t; }).pop() || f.why) };
    var s = server(net, f.dev, T, x.remote), sd = net.devs[f.dev];
    if (!s) return { err: sd.name + ' (' + x.remote + ') не принимает ' + T.toUpperCase() + ': нет remote-access ' + T + ' с outside-address ' + x.remote };
    if (!s.on) return { err: sd.name + ': remote-access ' + T + ' ' + s.name + ' выключен (enable)' };
    var b = net.send(f.dev, { src: x.remote, dst: f.pk.src, proto: pr[0], reply: true, sport: pr[1], rport: 49999 }, steps, ct);
    if (!b.ok || b.dev !== id) return { err: 'ответ сервера ' + x.remote + ' не вернулся к ' + me };
    if (T === 'l2tp') { if (!s.psm || !s.psk) return { err: sd.name + ': на сервере не задан ключ IPsec (ipsec authentication pre-shared-key)' };
      if (!x.psk) return { err: 'не задан ключ IPsec клиента' }; if (x.psk !== s.psk) return { err: 'IKE: ключи IPsec клиента и сервера не совпадают' }; }
    if (s.auth === 'radius') { var c = sd.st.run, L = Object.keys((c.aaa || {}).radius || {}), res = { down: 'на сервере не задан radius-server host' };
      for (var i = 0; i < L.length && EL.aaaAsk; i++) { res = EL.aaaAsk(net, f.dev, 'radius', L[i], c.aaa.radius[L[i]], x.user, x.pw); if (!res.down) break; }
      if (!res.ok) return { err: 'RADIUS: ' + (res.reject || res.down) }; }
    else { var u = s.users[x.user]; if (!u) return { err: sd.name + ': нет пользователя ' + x.user + ' в remote-access ' + T + ' ' + s.name };
      if (!u.on) return { err: sd.name + ': пользователь ' + x.user + ' выключен (enable)' }; if (u.pw !== x.pw) return { err: sd.name + ': неверный пароль пользователя ' + x.user }; }
    var loc = addr(net, f.dev, sd.st.run, s.local); if (!loc) return { err: sd.name + ': не задан local-address' };
    var rg = pool(sd.st.run, s.remote), ip = null;
    rg.some(function (r) { for (var n = IP.ip2n(r[0]); n <= IP.ip2n(r[1]); n++) { var a = IP.n2ip(n >>> 0); if (a !== loc && !used[f.dev + '/' + a]) { ip = a; return true; } } return false; });
    if (!ip) return { err: sd.name + ': ' + (rg.length ? 'пул remote-address исчерпан' : 'не задан remote-address') };
    used[f.dev + '/' + ip] = true;
    return { ok: true, srv: f.dev, prof: s.name, user: x.user, ip: ip, peer: loc, cip: f.pk.src, out: x.remote, nh: lu.nh, ifn: lu.iface.name, mtu: x.mtu || s.mtu || (T === 'pptp' ? 1460 : 1400) };
  }
  P.raSess = function () {
    if (this._ra && this._ra.gen === this.gen && this._ra.now === this.now) return this._ra.t;
    if (this._raBusy) return {};
    var s = this, t = {}, used = {}; this._raBusy = true;
    try { Object.keys(this.devs).forEach(function (id) { var d = s.devs[id]; if (d.type !== 'esr' || d.sub === 'me' || d.off || !d.st.run.ra) return;
      var L = d.st.run.ra.cli; Object.keys(L).sort().forEach(function (k) { (t[id] = t[id] || {})[k] = connect(s, id, k, L[k], used); }); }); }
    finally { this._raBusy = false; }
    this._ra = { gen: this.gen, now: this.now, t: t }; return t;
  };
  function ok(net) { var t = net.raSess(), o = []; Object.keys(t).forEach(function (id) { Object.keys(t[id]).forEach(function (k) { if (t[id][k].ok) o.push({ cli: id, k: k, x: t[id][k] }); }); }); return o; }

  var if0 = P.ifaces;
  P.ifaces = function (id) { var o = if0.apply(this, arguments); if (this._raBusy || this.devs[id].type !== 'esr') return o;
    ok(this).forEach(function (e) {
      if (e.cli === id) o.push({ name: e.k.replace(' ', ''), ip: e.x.ip, len: 32, port: null, tag: null, tun: e.k.split(' ')[0], ra: e, fw: false });
      if (e.x.srv === id) o.push({ name: e.k.split(' ')[0] + '-' + e.x.prof + '-' + e.x.user, ip: e.x.peer, len: 32, port: null, tag: null, tun: 'ras', ra: e, fw: false }); });
    return o; };
  var rt0 = P.routes;
  P.routes = function (id) { var o = rt0.apply(this, arguments); if (this._raBusy || this.devs[id].type !== 'esr') return o;
    ok(this).forEach(function (e) { var nm = e.k.replace(' ', '');
      if (e.cli === id) { o.push({ p: 'C', net: e.x.peer + '/32', len: 32, nh: null, ifn: nm, ad: 0, m: 0, vrf: null });
        o.forEach(function (r) { if (r.p === 'S' && r.dead && r.nh === e.x.peer) { r.dead = false; r.ifn = nm; } });
        var cf = (this.devs[id].st.run.ra.cli[e.k] || {}); if (!cf.noDef) { o.unshift({ p: 'S', net: '0.0.0.0/0', len: 0, nh: e.x.peer, ifn: nm, ad: 1, m: 0, vrf: null });
          o.push({ p: 'S', net: e.x.out + '/32', len: 32, nh: e.x.nh, ifn: e.x.ifn, ad: 1, m: 0, vrf: null }); } }
      if (e.x.srv === id) o.push({ p: 'C', net: e.x.ip + '/32', len: 32, nh: null, ifn: e.k.split(' ')[0] + '-' + e.x.prof + '-' + e.x.user, ad: 0, m: 0, vrf: null }); }, this);
    return o; };

  var tun0 = P.tunnel;
  P.tunnel = function (cur, r, pk, steps, ct) { var e = r.iface.ra; if (!e) return tun0.apply(this, arguments);
    var toSrv = e.cli === cur, T = e.k.split(' ')[0], d = this.devs[cur], peer = toSrv ? e.x.srv : e.cli;
    var src = toSrv ? e.x.cip : e.x.out, dst = toSrv ? e.x.out : e.x.cip, how = T === 'pptp' ? 'PPP в GRE (протокол 47)' : 'PPP в L2TP/UDP 1701 внутри IPsec ESP (протокол 50)';
    steps.push({ k: 'route', t: d.name + ': маршрут через ' + r.iface.name + ' — пакет ' + pk.src + ' → ' + pk.dst + ' упакован: ' + how + ', внешний заголовок ' + src + ' → ' + dst });
    var outer = { src: src, dst: dst, proto: T === 'pptp' ? 'gre' : 'esp', dport: null, inner: { src: pk.src, dst: pk.dst, proto: pk.proto, reply: !!pk.reply, dport: pk.dport, sport: pk.sport } };
    var o; this._raBusy = true; try { o = this.send(cur, outer, steps, ct); } finally { this._raBusy = false; }
    if (!o.ok || o.dev !== peer) { steps.push({ k: 'drop', t: T.toUpperCase() + '-пакет не дошёл до ' + this.devs[peer].name }); return { ok: false }; }
    var pf = this.ifaces(peer).filter(function (f) { return f.ra && f.ra.cli === e.cli && f.ra.k === e.k; })[0];
    steps.push({ k: 'route', t: this.devs[peer].name + ': ' + T.toUpperCase() + ' снят на ' + pf.name + ' — внутри ' + pk.src + ' → ' + pk.dst });
    return { ok: true, dev: peer, ip: pf.ip, inIf: pf };
  };

  // ---------------------------------------------------------------- show
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  S.cmd('priv', 'show remote-access status', function (st) { return status(st, null); }, 'Подключённые пользователи');
  S.cmd('priv', 'show remote-access status <w>', function (st, a) { if (!/^(pptp|l2tp|openvpn|wireguard)$/.test(a[0])) return bad(); return status(st, a[0]); });
  function status(st, T) { var net = st.net, me = net && Object.keys(net.devs).filter(function (k) { return net.devs[k].st === st; })[0];
    var L = net ? ok(net).filter(function (e) { return e.x.srv === me && (!T || e.k.split(' ')[0] === T); }) : [];
    var o = ['User               IP-address       Server', '----------------   ---------------  --------------------------------------'];
    L.forEach(function (e) { o.push(rp(e.x.user, 19) + rp(e.x.ip, 17) + e.k.split(' ')[0] + '(' + e.x.prof + ')'); });
    o.push('Count sessions: ' + L.length); return o.join('\n'); }
  S.cmd('priv', 'show remote-access configuration <w> <w>', function (st, a) { var s = (st.run.ra || { srv: {} }).srv[a[0] + ' ' + a[1]];
    if (!s) return '% Профиль ' + a[0] + ' ' + a[1] + ' не найден';
    var v = function (x) { return !x ? '--' : x.og ? x.og : x.r ? x.r.join('-') : x.ifn ? S.longIf(x.ifn) : x.ip; };
    var o = ['State:                ' + (s.on ? 'Enabled' : 'Disabled'), 'Description:          ' + (s.desc || '--'), 'Authentication mode:  ' + s.auth,
      'Authentication method: ' + s.method, 'MTU:                  ' + (s.mtu || 1500), 'Local address:        ' + v(s.local), 'Remote address:       ' + v(s.remote),
      'Outside address:      ' + v(s.outside), 'DNS server:           ' + (s.dns || '--')];
    if (s.type === 'l2tp') o.push('IPsec PSK:            ' + (s.psk ? 'configured' : '--'));
    o.push('', '   Users', '   ~~~~~', '#   Name                 State', '--- -------------------- --------');
    Object.keys(s.users).forEach(function (u, i) { o.push(rp(i, 4) + rp(u, 21) + (s.users[u].on ? 'Enabled' : 'Disabled')); });
    return o.join('\n'); }, 'Настройки профиля удалённого доступа');
  var tst = S.T.filter(function (c) { return c.pat.join(' ') === 'show tunnels status'; })[0];
  if (tst) { var run0 = tst.run; tst.run = function (st) { var out = run0.apply(this, arguments), net = st.net; if (!net || !st.run.ra) return out;
    var me = Object.keys(net.devs).filter(function (k) { return net.devs[k].st === st; })[0], t = net.raSess()[me] || {};
    Object.keys(st.run.ra.cli).sort().forEach(function (k) { var x = st.run.ra.cli[k], e = t[k] || {};
      out += '\n' + rp(k, 11) + rp(e.ok ? 'Up' : 'Down', 18) + rp(String(e.mtu || x.mtu || '--'), 9) + rp(e.ok ? e.ip : '--', 19) + rp(x.remote || '--', 19) + (e.ok ? 'connected' : (e.err || '--')); });
    return out; }; }
})(typeof window !== 'undefined' ? window : global);
