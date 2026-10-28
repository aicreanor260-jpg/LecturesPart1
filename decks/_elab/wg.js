/* WireGuard: ESR (справочник ESR-Series CLI 1.23) и Debian (wireguard-tools).
   Ключи: Debian — wg genkey, wg pubkey (конвейер: wg genkey | tee priv | wg pubkey > pub); на ESR ключи загружаются файлами:
     copy tftp://A:/ФАЙЛ crypto:private-key/ИМЯ | crypto:public-key/ИМЯ (delete crypto:… — удалить).
   ESR-туннель: tunnel wireguard N → (config-wireguard)#: ip address A/L, port P, private-key ИМЯ, mtu, description, ip firewall disable,
     security-zone, enable; peer N → (config-wireguard-tunnel-peer)#: public-key ИМЯ, remote address A, remote port P,
     subnet OBJECT-GROUP (разрешённые адреса), keepalive timeout С, description, enable.
   ESR-сервер: remote-access wireguard ИМЯ → (config-wireguard-server)#: local-address A/L, port, private-key, mtu, dns-server, security-zone, enable;
     peer N → (config-wireguard-server-peer)#: public-key, subnet, description, enable.  show remote-access status | configuration wireguard.
   Debian: /etc/wireguard/wg0.conf ([Interface] Address, PrivateKey, ListenPort; [Peer] PublicKey, Endpoint, AllowedIPs, PersistentKeepalive),
     wg-quick up|down wg0, systemctl start|stop wg-quick@wg0, wg show [wg0], ip addr — с wg0.
   Модель: криптомаршрутизация — пакет в туннель уходит тому пиру, чьи разрешённые адреса (subnet / AllowedIPs) содержат получателя;
   рукопожатие начинает сторона, у которой задан адрес пира (remote address / Endpoint) — по UDP на его порт; пир должен знать открытый ключ
   инициатора, а свой закрытый ключ — соответствовать открытому, который знает инициатор. Сторона без адреса пира (сервер) отвечает только
   после рукопожатия и запоминает адрес клиента. Принятый пакет отбрасывается, если источник не входит в разрешённые адреса пира.
   Упрощения: шифрование и таймеры повторных рукопожатий не моделируются; рукопожатие действует, пока жива конфигурация. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, H = EL.hosts, IP = EL.ip;
  var B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', PORT = 51820;
  function rnd(seed, n) { var o = '', h = 2166136261, i = 0, s = String(seed);
    while (o.length < n) { var x = s + '#' + (i++); for (var j = 0; j < x.length; j++) { h ^= x.charCodeAt(j); h = Math.imul(h, 16777619); }
      var v = h >>> 0; for (var k = 0; k < 5; k++) { o += B64.charAt(v & 63); v >>>= 6; } } return o.slice(0, n); }
  var CNT = 0;
  function genkey() { CNT++; return rnd('wg|' + Date.now() + '|' + Math.random() + '|' + CNT, 42) + 'A='; }
  function isKey(k) { return /^[A-Za-z0-9+/]{42}[AEIMQUYcgkosw048]=$/.test(String(k || '').trim()); }
  function pubOf(k) { k = String(k || '').trim(); return isKey(k) ? rnd('wgpub|' + k, 42) + 'Q=' : null; }
  EL.wgPub = pubOf;
  function cidrR(s) { var c = IP.parseCidr(String(s).trim()); if (!c) return null; var n = (IP.ip2n(c.ip) & IP.maskN(c.len)) >>> 0;
    return [n, (n | (~IP.maskN(c.len) >>> 0)) >>> 0, c.ip + '/' + c.len]; }
  function inR(L, ip) { var n = IP.ip2n(ip); return (L || []).some(function (r) { return n >= r[0] && n <= r[1]; }); }
  function ogR(c, name) { var g = c.og && c.og.net[name]; return g ? g.items.map(function (x) { return [IP.ip2n(x[0]), IP.ip2n(x[1]), String(x[2]).replace(/^ip (prefix|address-range) /, '')]; }) : []; }
  function touch(st) { st.pending = true; }
  function bad() { return 'Syntax error: Illegal parameter'; }

  // ---------------------------------------------------------------- ESR: ключи через TFTP
  function store(st) { return st.crypto || (st.crypto = { 'private-key': {}, 'public-key': {} }); }
  var cp = S.T.filter(function (c) { return c.pat.join(' ') === 'copy <w> <w>'; })[0];
  if (cp) { var cp0 = cp.run; cp.run = function (st, a) {
    var m = String(a[1]).match(/^crypto:(private-key|public-key)\/([\w.\-]{1,31})$/); if (!m) return cp0.apply(this, arguments);
    var u = String(a[0]).match(/^tftp:\/\/(\d+\.\d+\.\d+\.\d+):?\/(.+)$/); if (!u) return '% Источник: tftp://A.B.C.D:/имя_файла';
    if (!st.net) return ''; var r = st.net.request(st.dev, u[1], 'udp', 69);
    if (!r.ok) return '% Ошибка передачи по TFTP: ' + (r.why === 'Connection refused' ? 'на ' + u[1] + ' не запущен TFTP-сервер' : 'сервер ' + u[1] + ' недоступен');
    var f = st.net.devs[r.dev].st.files['/tftp/' + u[2]]; if (f === undefined) return '% Ошибка передачи по TFTP: File not found';
    store(st)[m[1]][m[2]] = String(f).trim(); st.net.gen++;
    return '|******************************************| 100% (' + f.length + 'B)\nSuccess!'; }; }
  S.cmd('priv', 'delete <w>', function (st, a) { var m = String(a[0]).match(/^crypto:(private-key|public-key)\/(.+)$/); if (!m) return '% Удалить можно crypto:private-key/ИМЯ или crypto:public-key/ИМЯ';
    var L = store(st)[m[1]]; if (!(m[2] in L)) return '% Файл ' + a[0] + ' не найден'; delete L[m[2]]; }, 'Удалить файл ключа');
  function key(st, kind, name) { var v = name && store(st)[kind][name]; return v ? String(v).trim() : null; }

  // ---------------------------------------------------------------- ESR: настройка
  var M = { wgt: '(config-wireguard)#', wgtp: '(config-wireguard-tunnel-peer)#', wgs: '(config-wireguard-server)#', wgsp: '(config-wireguard-server-peer)#' };
  Object.keys(M).forEach(function (k) { S.PROMPT[k] = M[k]; });
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes = c.modes.concat(Object.keys(M)); });
  function W(c) { return c.wg || (c.wg = { tun: {}, srv: {} }); }
  function T(st) { return W(st.cand).tun[st.wgT]; }
  function SV(st) { return W(st.cand).srv[st.wgS]; }
  function obj(st) { return st.mode === 'wgt' ? T(st) : st.mode === 'wgs' ? SV(st) : st.mode === 'wgtp' ? T(st).peers[st.wgP] : SV(st).peers[st.wgP]; }
  S.cmd('config', 'tunnel wireguard <n>', function (st, a) { if (a[0] < 1 || a[0] > 10) return bad(); var L = W(st.cand).tun;
    if (!L[a[0]]) { L[a[0]] = { peers: {} }; touch(st); } st.mode = 'wgt'; st.wgT = a[0]; }, 'Туннель WireGuard');
  S.cmd('config', 'no tunnel wireguard <n>', function (st, a) { delete W(st.cand).tun[a[0]]; touch(st); });
  S.cmd('config', 'remote-access wireguard <w>', function (st, a) { var L = W(st.cand).srv;
    if (!L[a[0]]) { L[a[0]] = { peers: {} }; touch(st); } st.mode = 'wgs'; st.wgS = a[0]; }, 'Сервер удалённого доступа WireGuard');
  S.cmd('config', 'no remote-access wireguard <w>', function (st, a) { delete W(st.cand).srv[a[0]]; touch(st); });
  S.cmd('wgt wgs', 'peer <n>', function (st, a) { if (a[0] < 1 || a[0] > 16) return bad(); var o = st.mode === 'wgt' ? T(st) : SV(st);
    o.peers[a[0]] = o.peers[a[0]] || {}; st.wgP = a[0]; st.mode = st.mode + 'p'; touch(st); }, 'Пир (разрешённый собеседник)');
  S.cmd('wgt wgs', 'no peer <n>', function (st, a) { delete (st.mode === 'wgt' ? T(st) : SV(st)).peers[a[0]]; touch(st); });
  S.cmd('wgt wgs', 'exit', function (st) { st.mode = 'config'; });
  S.cmd('wgtp wgsp', 'exit', function (st) { st.mode = st.mode.slice(0, 3); });
  S.cmd('wgt', 'ip address <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return bad(); T(st).ip = a[0]; touch(st); }, 'Адрес туннеля A/L');
  S.cmd('wgt', 'no ip address', function (st) { delete T(st).ip; touch(st); });
  S.cmd('wgs', 'local-address <w>', function (st, a) { if (!IP.parseCidr(a[0])) return bad(); SV(st).local = a[0]; touch(st); }, 'Адрес сервера и сеть клиентов A/L');
  S.cmd('wgs', 'dns-server <rest>', function (st, a) { SV(st).dns = a[0].replace(/\s+/g, ''); touch(st); }, 'DNS-серверы для клиентов');
  S.cmd('wgt wgs', 'port <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return bad(); obj(st).port = a[0]; touch(st); }, 'UDP-порт');
  S.cmd('wgt wgs', 'no port', function (st) { delete obj(st).port; touch(st); });
  S.cmd('wgt wgs', 'private-key <w>', function (st, a) { obj(st).priv = a[0]; touch(st); }, 'Закрытый ключ (crypto:private-key/ИМЯ)');
  S.cmd('wgt wgs', 'no private-key', function (st) { delete obj(st).priv; touch(st); });
  S.cmd('wgt wgs', 'mtu <n>', function (st, a) { if (a[0] < 1280 || a[0] > 1500) return bad(); obj(st).mtu = a[0]; touch(st); }, 'MTU');
  S.cmd('wgt', 'ip firewall disable', function (st) { T(st).fwOff = true; touch(st); }, 'Не проверять межсетевым экраном');
  S.cmd('wgt', 'no ip firewall disable', function (st) { T(st).fwOff = false; touch(st); });
  S.cmd('wgt wgs', 'security-zone <w>', function (st, a) { if (!(st.cand.zones || {})[a[0]]) return '% Зона ' + a[0] + ' не создана — security zone ' + a[0]; obj(st).zone = a[0]; touch(st); }, 'Зона безопасности');
  S.cmd('wgt wgs', 'no security-zone', function (st) { delete obj(st).zone; touch(st); });
  S.cmd('wgtp wgsp', 'public-key <w>', function (st, a) { obj(st).pub = a[0]; touch(st); }, 'Открытый ключ пира (crypto:public-key/ИМЯ)');
  S.cmd('wgtp wgsp', 'no public-key', function (st) { delete obj(st).pub; touch(st); });
  S.cmd('wgtp wgsp', 'subnet <w>', function (st, a) { obj(st).subnet = a[0]; touch(st); }, 'Разрешённые адреса (object-group network)');
  S.cmd('wgtp wgsp', 'no subnet', function (st) { delete obj(st).subnet; touch(st); });
  S.cmd('wgtp', 'remote address <ip>', function (st, a) { obj(st).remote = a[0]; touch(st); }, 'Адрес пира');
  S.cmd('wgtp', 'no remote address', function (st) { delete obj(st).remote; touch(st); });
  S.cmd('wgtp', 'remote port <n>', function (st, a) { obj(st).rport = a[0]; touch(st); }, 'UDP-порт пира');
  S.cmd('wgtp', 'keepalive timeout <n>', function (st, a) { obj(st).ka = a[0]; touch(st); }, 'Keepalive, с');
  S.cmd('wgtp', 'no keepalive timeout', function (st) { delete obj(st).ka; touch(st); });
  S.cmd('wgt wgs wgtp wgsp', 'description <rest>', function (st, a) { obj(st).desc = a[0].replace(/^"|"$/g, ''); touch(st); }, 'Описание');
  S.cmd('wgt wgs wgtp wgsp', 'enable', function (st) { obj(st).on = true; touch(st); }, 'Включить');
  S.cmd('wgt wgs wgtp wgsp', 'no enable', function (st) { obj(st).on = false; touch(st); });
  S.RUNX.push(function (c, out) { var w = c.wg; if (!w) return;
    function peers(L, cli) { Object.keys(L).sort(function (a, b) { return a - b; }).forEach(function (n) { var p = L[n]; out.push('  peer ' + n);
      if (p.desc) out.push('    description "' + p.desc + '"'); if (p.pub) out.push('    public-key ' + p.pub);
      if (cli && p.remote) out.push('    remote address ' + p.remote); if (cli && p.rport) out.push('    remote port ' + p.rport);
      if (p.subnet) out.push('    subnet ' + p.subnet); if (cli && p.ka) out.push('    keepalive timeout ' + p.ka); if (p.on) out.push('    enable'); out.push('  exit'); }); }
    Object.keys(w.tun).sort().forEach(function (n) { var t = w.tun[n]; out.push('tunnel wireguard ' + n); if (t.desc) out.push('  description "' + t.desc + '"');
      if (t.fwOff) out.push('  ip firewall disable'); if (t.zone) out.push('  security-zone ' + t.zone); if (t.ip) out.push('  ip address ' + t.ip);
      if (t.port) out.push('  port ' + t.port); if (t.priv) out.push('  private-key ' + t.priv); if (t.mtu) out.push('  mtu ' + t.mtu); peers(t.peers, true);
      if (t.on) out.push('  enable'); out.push('exit'); });
    Object.keys(w.srv).sort().forEach(function (n) { var t = w.srv[n]; out.push('remote-access wireguard ' + n); if (t.desc) out.push('  description "' + t.desc + '"');
      if (t.zone) out.push('  security-zone ' + t.zone); if (t.local) out.push('  local-address ' + t.local); if (t.port) out.push('  port ' + t.port);
      if (t.priv) out.push('  private-key ' + t.priv); if (t.mtu) out.push('  mtu ' + t.mtu); if (t.dns) out.push('  dns-server ' + t.dns); peers(t.peers, false);
      if (t.on) out.push('  enable'); out.push('exit'); }); });

  // ---------------------------------------------------------------- точки WireGuard во всей сети
  // ep: {dev, name, ip, len, priv, pub, port, peers: [{id, pub, ep: {ip, port}|null, allowed: [[n1,n2,txt]], ka}], fw, zone, kind, why}
  function eps(net) {
    if (net._wgE && net._wgE.gen === net.gen) return net._wgE.t;
    var o = [];
    Object.keys(net.devs).forEach(function (id) { var d = net.devs[id]; if (d.off) return;
      if (d.type === 'esr' && d.sub !== 'me' && d.st.run.wg) { var c = d.st.run, w = c.wg;
        Object.keys(w.tun).forEach(function (n) { var t = w.tun[n]; if (!t.on || !t.ip) return; var cc = IP.parseCidr(t.ip), pk = key(d.st, 'private-key', t.priv);
          o.push({ dev: id, name: 'wg' + n, ip: cc.ip, len: cc.len, priv: pk, pub: pubOf(pk), port: t.port || PORT, fw: !t.fwOff, zone: t.zone || null, kind: 'tun', cfg: 'tunnel wireguard ' + n,
            why: !t.priv ? 'не задан private-key' : !pk ? 'нет ключа crypto:private-key/' + t.priv + ' (copy tftp://… crypto:private-key/' + t.priv + ')' : !isKey(pk) ? 'crypto:private-key/' + t.priv + ' — не ключ WireGuard' : null,
            peers: Object.keys(t.peers).filter(function (k) { return t.peers[k].on; }).map(function (k) { var p = t.peers[k], pb = key(d.st, 'public-key', p.pub);
              return { id: 'peer ' + k, pub: pb, ep: p.remote ? { ip: p.remote, port: p.rport || PORT } : null, allowed: p.subnet ? ogR(c, p.subnet) : [], ka: p.ka || 0,
                why: !p.pub ? 'не задан public-key' : !pb ? 'нет ключа crypto:public-key/' + p.pub : null }; }) }); });
        Object.keys(w.srv).forEach(function (n) { var t = w.srv[n]; if (!t.on || !t.local) return; var cc = IP.parseCidr(t.local), pk = key(d.st, 'private-key', t.priv);
          o.push({ dev: id, name: 'wg-' + n, ip: cc.ip, len: cc.len, priv: pk, pub: pubOf(pk), port: t.port || PORT, fw: true, zone: t.zone || null, kind: 'srv', cfg: 'remote-access wireguard ' + n, srv: n,
            why: !t.priv ? 'не задан private-key' : !pk ? 'нет ключа crypto:private-key/' + t.priv : null,
            peers: Object.keys(t.peers).filter(function (k) { return t.peers[k].on; }).map(function (k) { var p = t.peers[k], pb = key(d.st, 'public-key', p.pub);
              return { id: 'peer ' + k, pub: pb, ep: null, allowed: p.subnet ? ogR(c, p.subnet) : [], ka: 0, why: !p.pub ? 'не задан public-key' : !pb ? 'нет ключа crypto:public-key/' + p.pub : null }; }) }); }); }
      if (d.type === 'deb' && d.st.wgUp) Object.keys(d.st.wgUp).forEach(function (nm) { var x = d.st.wgUp[nm];
        o.push({ dev: id, name: nm, ip: x.ip, len: x.len, priv: x.priv, pub: pubOf(x.priv), port: x.port, fw: false, kind: 'deb', peers: x.peers, why: isKey(x.priv) ? null : 'PrivateKey — не ключ WireGuard' }); });
    });
    net._wgE = { gen: net.gen, t: o }; return o;
  }
  EL.wgEps = eps;
  function hsKey(a, p) { return a.dev + '|' + a.name + '|' + p.id; }
  // рукопожатие от a через пир p: {ok, b, bp, why, steps}
  function handshake(net, a, p, steps) {
    if (a.why) return { why: net.devs[a.dev].name + ' ' + a.name + ': ' + a.why };
    if (p.why) return { why: net.devs[a.dev].name + ' ' + a.name + ' ' + p.id + ': ' + p.why };
    var ep = p.ep || (net._wgLearn || {})[hsKey(a, p)];
    if (!ep) return { why: net.devs[a.dev].name + ': у ' + p.id + ' нет адреса (remote address / Endpoint), а сам пир ещё не подключался — отправлять некуда' };
    var bs = net._wgBusy; net._wgBusy = true; var r;
    var cl = net.ctLast; try { r = net.request(a.dev, ep.ip, 'udp', ep.port); } finally { net._wgBusy = bs; net.ctLast = cl; }
    if (steps) r.steps.forEach(function (x) { steps.push(x); });
    var B = eps(net).filter(function (e) { return e.dev === r.dev && e.port === ep.port; })[0];
    if (!r.ok) return { why: 'рукопожатие: UDP ' + ep.ip + ':' + ep.port + ' — ' + (r.why === 'Connection refused' ? 'на этом порту нет WireGuard' : 'нет связи') };
    if (!B) return { why: 'рукопожатие: на ' + ep.ip + ':' + ep.port + ' нет WireGuard' };
    if (B.why) return { why: net.devs[B.dev].name + ' ' + B.name + ': ' + B.why };
    if (B.pub !== p.pub) return { why: 'рукопожатие: открытый ключ ' + p.id + ' у ' + net.devs[a.dev].name + ' не совпадает с ключом ' + net.devs[B.dev].name + ' ' + B.name + ' — Handshake Initiation отброшено' };
    var bp = B.peers.filter(function (q) { return q.pub === a.pub; })[0];
    if (!bp) return { why: net.devs[B.dev].name + ' ' + B.name + ': нет пира с открытым ключом ' + net.devs[a.dev].name + ' — рукопожатие отвергнуто' };
    var L = net._wgLearn || (net._wgLearn = {}), hs = net._wgHs || (net._wgHs = {});
    var src = (net.lookup(a.dev, ep.ip) || { iface: {} }).iface.ip;
    L[hsKey(B, bp)] = { ip: src, port: a.port }; hs[hsKey(a, p)] = hs[hsKey(B, bp)] = net.now;
    return { ok: true, b: B, bp: bp };
  }
  EL.listensX = (function (lx0) { return function (d, proto, port) {
    if (proto === 'udp' && d.st && d.st.net && eps(d.st.net).some(function (e) { return e.dev === d.id && e.port === port; })) return true;
    return lx0 ? lx0(d, proto, port) : undefined; }; })(EL.listensX);
  function peerFor(a, dst) { return a.peers.filter(function (p) { return inR(p.allowed, dst); })[0] || null; }

  // ---------------------------------------------------------------- интерфейсы, маршруты, пересылка
  var if0 = P.ifaces;
  P.ifaces = function (id) { var o = if0.apply(this, arguments); if (this._wgBusy) return o;
    eps(this).forEach(function (e) { if (e.dev === id) o.push({ name: e.name, ip: e.ip, len: e.len, port: null, tag: null, tun: 'wg', wg: e, fw: e.fw }); });
    return o; };
  var rt0 = P.routes;
  P.routes = function (id) { var o = rt0.apply(this, arguments); if (this._wgBusy) return o; var s = this;
    eps(this).forEach(function (e) { if (e.dev !== id || e.kind === 'tun') return;
      e.peers.forEach(function (p) { p.allowed.forEach(function (r) { var len = 32 - Math.round(Math.log(r[1] - r[0] + 1) / Math.LN2);
        if (e.kind === 'srv' && IP.sameNet(IP.n2ip(r[0]), e.ip, e.len) && len >= e.len) return;
        var R = { p: 'S', net: IP.n2ip(r[0]) + '/' + len, len: len, nh: null, ifn: e.name, ad: 1, m: 0, vrf: null };
        if (len === 0) { o.unshift(R); if (p.ep) { var g = s.devs[id].st.gw; if (g) o.push({ p: 'S', net: p.ep.ip + '/32', len: 32, nh: g, ifn: (if0.call(s, id)[0] || {}).name, ad: 1, m: 0, vrf: null }); } }
        else o.push(R); }); }); });
    return o; };
  var z0 = EL.fwZoneOf;
  EL.fwZoneOf = function (c, ifname) { var n = String(ifname), m = n.match(/^wg(\d+)$/), q = n.match(/^wg-(.+)$/);
    if (m && c.wg && c.wg.tun[m[1]]) return c.wg.tun[m[1]].zone || null; if (q && c.wg && c.wg.srv[q[1]]) return c.wg.srv[q[1]].zone || null; return z0(c, ifname); };
  var tun0 = P.tunnel;
  P.tunnel = function (cur, r, pk, steps, ct) { var a = r.iface.wg; if (!a) return tun0.apply(this, arguments);
    var me = this.devs[cur].name, p = peerFor(a, pk.dst);
    if (!p) { steps.push({ k: 'drop', t: me + ': ' + a.name + ' — нет пира, у которого ' + pk.dst + ' в разрешённых адресах (subnet / AllowedIPs) — пакет отброшен' }); return { ok: false }; }
    var hs = handshake(this, a, p, null);
    if (!hs.ok) { steps.push({ k: 'drop', t: hs.why }); return { ok: false }; }
    var B = hs.b, bp = hs.bp, ep = p.ep || this._wgLearn[hsKey(a, p)];
    steps.push({ k: 'route', t: me + ': ' + a.name + ' — получатель ' + pk.dst + ' в разрешённых адресах ' + p.id + '; пакет зашифрован и упакован в UDP ' + a.port + ' → ' + ep.ip + ':' + ep.port });
    var outer = { src: null, dst: ep.ip, proto: 'udp', dport: ep.port, sport: a.port, inner: { src: pk.src, dst: pk.dst, proto: pk.proto, reply: !!pk.reply } };
    var o, bs = this._wgBusy; this._wgBusy = true; try { o = this.send(cur, outer, steps, ct); } finally { this._wgBusy = bs; }
    if (!o.ok || o.dev !== B.dev) { steps.push({ k: 'drop', t: 'UDP-пакет WireGuard не дошёл до ' + this.devs[B.dev].name }); return { ok: false }; }
    var bn = this.devs[B.dev].name;
    if (!inR(bp.allowed, pk.src)) { steps.push({ k: 'drop', t: bn + ': ' + B.name + ' — источник ' + pk.src + ' не в разрешённых адресах ' + bp.id + ' (subnet / AllowedIPs) — пакет отброшен' }); return { ok: false }; }
    var C = this._wgCnt || (this._wgCnt = {}), sz = pk.size || 84; (C[hsKey(a, p)] = C[hsKey(a, p)] || { tx: 0, rx: 0 }).tx += sz; (C[hsKey(B, bp)] = C[hsKey(B, bp)] || { tx: 0, rx: 0 }).rx += sz;
    var bf = this.ifaces(B.dev).filter(function (f) { return f.wg && f.name === B.name; })[0];
    steps.push({ k: 'route', t: bn + ': ' + B.name + ' — расшифровано, ключ ' + bp.id + ' верный, источник ' + pk.src + ' разрешён — внутри ' + pk.src + ' → ' + pk.dst });
    if (this.devs[B.dev].type === 'esr') { var fw = this.fwPass(B.dev, bf, pk, ct, { src: pk.src, dst: pk.dst }); if (fw.t) steps.push({ k: fw.ok ? 'route' : 'drop', t: fw.t }); if (!fw.ok) return { ok: false }; }
    return { ok: true, dev: B.dev, ip: bf.ip, inIf: bf };
  };
  // keepalive: при каждом шаге времени и после команд — рукопожатие от тех, у кого задан адрес пира и keepalive
  function ka(net) { if (net._wgKa) return; net._wgKa = true;
    try { eps(net).forEach(function (a) { a.peers.forEach(function (p) { if (p.ep && p.ka) handshake(net, a, p, null); }); }); } finally { net._wgKa = false; } }
  var tk0 = P.tick; P.tick = function () { var r = tk0.apply(this, arguments); ka(this); return r; };
  var ex0 = P.exec; P.exec = function () { var r = ex0.apply(this, arguments); ka(this); return r; };

  // ---------------------------------------------------------------- ESR: show
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function ago(net, k) { var t = (net._wgHs || {})[k]; return t === undefined ? null : Math.max(0, Math.round(net.now - t)); }
  var tst = S.T.filter(function (c) { return c.pat.join(' ') === 'show tunnels status'; })[0];
  if (tst) { var run0 = tst.run; tst.run = function (st) { var out = run0.apply(this, arguments), n = st.net; if (!n || !st.run.wg) return out;
    Object.keys(st.run.wg.tun).sort().forEach(function (k) { var t = st.run.wg.tun[k]; out += '\n' + rp('wireguard ' + k, 11) + rp(t.on ? 'Up' : 'Down', 18) + rp(String(t.mtu || 1420), 9) + rp(t.ip || '--', 19) + rp('--', 19) + (t.on && n ? 'port ' + (t.port || PORT) : '--'); });
    return out; }; }
  function meOf(st) { var n = st.net; return n ? Object.keys(n.devs).filter(function (k) { return n.devs[k].st === st; })[0] : null; }
  S.cmd('priv', 'show wireguard peers', function (st) { var n = st.net, me = meOf(st); if (!n) return '';
    var o = []; eps(n).filter(function (e) { return e.dev === me; }).forEach(function (e) {
      o.push(e.cfg + ' (' + e.name + '): public key ' + (e.pub || '--') + ', port ' + e.port + (e.why ? ' — ' + e.why : ''));
      e.peers.forEach(function (p) { var ep = p.ep || (n._wgLearn || {})[hsKey(e, p)], h = ago(n, hsKey(e, p)), c = (n._wgCnt || {})[hsKey(e, p)] || { tx: 0, rx: 0 };
        o.push('  ' + p.id + ': endpoint ' + (ep ? ep.ip + ':' + ep.port : '(none)') + ', subnet ' + (p.allowed.map(function (r) { return r[2]; }).join(', ') || '(none)') +
          ', latest handshake ' + (h === null ? 'never' : h + ' s ago') + ', transfer ' + c.rx + ' B received, ' + c.tx + ' B sent' + (p.why ? ' — ' + p.why : '')); }); });
    return o.join('\n') || 'WireGuard не настроен'; }, 'Пиры WireGuard: адрес, рукопожатие, трафик');
  var rs = S.T.filter(function (c) { return c.pat.join(' ') === 'show remote-access status <w>'; })[0];
  if (rs) { var rs0 = rs.run; rs.run = function (st, a) { if (a[0] !== 'wireguard') return rs0.apply(this, arguments); var n = st.net, me = meOf(st), L = [];
    if (n) eps(n).filter(function (e) { return e.dev === me && e.kind === 'srv'; }).forEach(function (e) { e.peers.forEach(function (p) { var h = ago(n, hsKey(e, p)); if (h === null) return;
      L.push(rp(p.id, 19) + rp((p.allowed[0] ? IP.n2ip(p.allowed[0][0]) : '--'), 17) + 'wireguard(' + e.srv + ')'); }); });
    return ['User               IP-address       Server', '----------------   ---------------  --------------------------------------'].concat(L, ['Count sessions: ' + L.length]).join('\n'); }; }

  // ---------------------------------------------------------------- Debian: wg, wg-quick
  function parseConf(text) { var o = { peers: [] }, cur = null, err = null;
    String(text || '').split('\n').forEach(function (l, i) { l = l.replace(/#.*/, '').trim(); if (!l) return;
      if (/^\[Interface\]$/i.test(l)) { cur = o; return; } if (/^\[Peer\]$/i.test(l)) { cur = { allowed: [] }; o.peers.push(cur); return; }
      var m = l.match(/^(\w+)\s*=\s*(.+)$/); if (!m || !cur) { err = err || 'Line unrecognized: `' + l + '\' (строка ' + (i + 1) + ')'; return; }
      var k = m[1].toLowerCase(), v = m[2].trim();
      if (cur === o) { if (k === 'address') o.addr = v.split(',')[0].trim(); else if (k === 'privatekey') o.priv = v; else if (k === 'listenport') o.port = +v; else if (k === 'dns') o.dns = v; }
      else { if (k === 'publickey') cur.pub = v; else if (k === 'endpoint') { var e = v.match(/^(\d+\.\d+\.\d+\.\d+):(\d+)$/); if (e) cur.ep = { ip: e[1], port: +e[2] }; else err = err || 'Invalid endpoint: ' + v; }
        else if (k === 'allowedips') v.split(',').forEach(function (x) { var r = cidrR(x); if (r) cur.allowed.push(r); else err = err || 'Invalid AllowedIPs: ' + x; });
        else if (k === 'persistentkeepalive') cur.ka = +v; } });
    return err ? { err: err } : o; }
  function quickUp(st, nm) {
    if (st.user !== 'root') return 'wg-quick must be run as root. Please enter the password for ' + st.user + ' to continue:';
    st.wgUp = st.wgUp || {}; if (st.wgUp[nm]) return 'wg-quick: `' + nm + '\' already exists';
    var f = '/etc/wireguard/' + nm + '.conf'; if (st.files[f] === undefined) return 'wg-quick: `' + f + '\' does not exist';
    var c = parseConf(st.files[f]); if (c.err) return '[#] ip link add ' + nm + ' type wireguard\n' + c.err + '\nConfiguration parsing error\n[#] ip link delete dev ' + nm;
    var a = IP.parseCidr(c.addr || ''); if (!a) return 'wg-quick: в [Interface] нет Address = A/L';
    if (!isKey(c.priv)) return '[#] ip link add ' + nm + ' type wireguard\nKey is not the correct length or format: `' + (c.priv || '') + '\'\nConfiguration parsing error\n[#] ip link delete dev ' + nm;
    st.wgUp[nm] = { ip: a.ip, len: a.len, priv: c.priv.trim(), port: c.port || PORT,
      peers: c.peers.map(function (p, i) { return { id: 'peer ' + (p.pub ? p.pub.slice(0, 8) + '…' : i + 1), pub: isKey(p.pub) ? p.pub.trim() : null, ep: p.ep || null, allowed: p.allowed, ka: p.ka || 0,
        why: !p.pub ? 'нет PublicKey' : !isKey(p.pub) ? 'PublicKey — не ключ WireGuard' : null }; }) };
    if (st.net) st.net.gen++;
    var o = ['[#] ip link add ' + nm + ' type wireguard', '[#] wg setconf ' + nm + ' /dev/fd/63', '[#] ip -4 address add ' + c.addr + ' dev ' + nm, '[#] ip link set mtu 1420 up dev ' + nm];
    c.peers.forEach(function (p) { p.allowed.forEach(function (r) { if (!IP.sameNet(IP.n2ip(r[0]), a.ip, a.len) || +r[2].split('/')[1] < a.len) o.push('[#] ip -4 route add ' + r[2] + ' dev ' + nm); }); });
    return o.join('\n'); }
  function quickDown(st, nm) { if (!st.wgUp || !st.wgUp[nm]) return 'wg-quick: `' + nm + '\' is not a WireGuard interface'; delete st.wgUp[nm]; if (st.net) st.net.gen++; return '[#] ip link delete dev ' + nm; }
  function wgShow(st, nm) { var n = st.net, me = n ? Object.keys(n.devs).filter(function (k) { return n.devs[k].st === st; })[0] : null, o = [];
    (n ? eps(n) : []).filter(function (e) { return e.dev === me && (!nm || e.name === nm); }).forEach(function (e) {
      o.push('interface: ' + e.name, '  public key: ' + e.pub, '  private key: (hidden)', '  listening port: ' + e.port, '');
      e.peers.forEach(function (p) { var ep = p.ep || (n._wgLearn || {})[hsKey(e, p)], h = ago(n, hsKey(e, p)), c = (n._wgCnt || {})[hsKey(e, p)];
        o.push('peer: ' + (p.pub || '(нет ключа)')); if (ep) o.push('  endpoint: ' + ep.ip + ':' + ep.port);
        o.push('  allowed ips: ' + (p.allowed.map(function (r) { return r[2]; }).join(', ') || '(none)'));
        if (h !== null) o.push('  latest handshake: ' + (h ? h + ' seconds ago' : 'Now')); if (c) o.push('  transfer: ' + c.rx + ' B received, ' + c.tx + ' B sent');
        if (p.ka) o.push('  persistent keepalive: every ' + p.ka + ' seconds'); o.push(''); }); });
    return o.join('\n').replace(/\n+$/, ''); }
  function pipeline(st, line) {          // wg genkey | tee F | wg pubkey > G ;  wg pubkey < F > G ;  cat F | wg pubkey
    var segs = line.replace(/^umask\s+\d+\s*;\s*/, '').split('|').map(function (x) { return x.trim(); }), data = null, out = null;
    for (var i = 0; i < segs.length; i++) { var s = segs[i], to = null, from = null, m;
      if ((m = s.match(/\s>\s*(\S+)$/))) { to = m[1]; s = s.slice(0, m.index).trim(); }
      if ((m = s.match(/\s<\s*(\S+)$/))) { from = m[1]; s = s.slice(0, m.index).trim(); }
      if (from !== null) { if (st.files[from] === undefined) return '-bash: ' + from + ': No such file or directory'; data = st.files[from]; }
      var w = s.split(/\s+/);
      if (w[0] === 'wg' && w[1] === 'genkey') data = genkey() + '\n';
      else if (w[0] === 'wg' && w[1] === 'pubkey') { var pb = pubOf(data); if (!pb) return 'Key is not the correct length or format'; data = pb + '\n'; }
      else if (w[0] === 'tee' && w[1]) { if (!writable(st, w[1])) return 'tee: ' + w[1] + ': Permission denied'; st.files[w[1]] = data; }
      else if (w[0] === 'cat' && w[1]) { if (st.files[w[1]] === undefined) return 'cat: ' + w[1] + ': No such file or directory'; data = st.files[w[1]]; }
      else return null;
      if (to) { if (!writable(st, to)) return '-bash: ' + to + ': Permission denied'; st.files[to] = data; data = ''; }
      out = data; }
    return String(out || '').replace(/\n$/, ''); }
  function writable(st, f) { return st.user === 'root' || f.indexOf('/home/' + st.user + '/') === 0 || f.indexOf('/tmp/') === 0; }
  var deb0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    if (!st.user || st.ssh || !st.net) return deb0.apply(this, arguments);
    var line = String(raw).trim(), t = line.split(/\s+/), c = t[0];
    if (/(^|\|\s*|;\s*)wg (genkey|pubkey)\b/.test(line)) { var pr = pipeline(st, line); if (pr !== null) return pr; }
    if (c === 'wg-quick' && /^(up|down)$/.test(t[1] || '') && t[2]) return t[1] === 'up' ? quickUp(st, t[2]) : quickDown(st, t[2]);
    var sc = line.match(/^systemctl\s+(start|stop|restart|enable --now)\s+wg-quick@(\w+)(\.service)?$/);
    if (sc) { if (sc[1] === 'stop') { quickDown(st, sc[2]); return ''; } if (sc[1] === 'restart') quickDown(st, sc[2]); var u = quickUp(st, sc[2]);
      return /^\[#\][^\n]*\n\[#\] wg setconf/.test(u) ? '' : 'Job for wg-quick@' + sc[2] + '.service failed because the control process exited with error code.'; }
    if (c === 'wg' && (t.length === 1 || t[1] === 'show')) return wgShow(st, t[2]);
    var r = deb0.apply(this, arguments);
    if (/^ip\s+a(ddr)?(\s+show)?$/.test(line) && st.wgUp) Object.keys(st.wgUp).forEach(function (nm, i) { var x = st.wgUp[nm];
      r += '\n' + (3 + i) + ': ' + nm + ': <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000\n    link/none\n    inet ' + x.ip + '/' + x.len + ' scope global ' + nm + '\n       valid_lft forever preferred_lft forever'; });
    return r;
  };
})(typeof window !== 'undefined' ? window : global);
