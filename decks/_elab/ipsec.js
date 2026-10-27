/* IPsec VPN на ESR (справочник ESR-Series CLI 1.23, «Управление VPN»):
   security ike proposal → encryption algorithm (по умолчанию 3des), authentication algorithm (sha1), dh-group (1);
   security ike policy → pre-shared-key ascii-text, proposal; security ike gateway → ike-policy, local address, remote address,
   mode policy-based | route-based, local network / remote network (policy-based), bind-interface vti N (route-based);
   security ipsec proposal → encryption algorithm (3des), authentication algorithm (sha1); security ipsec policy → proposal;
   security ipsec vpn → ike establish-tunnel by-request | route | immediate, ike gateway, ike ipsec-policy, enable;
   tunnel vti N → local address, remote address, ip address, enable; show security ipsec vpn status.
   SA устанавливается, если у пары ESR зеркальные шлюзы, одинаковый ключ и алгоритмы, и UDP 500 (IKE) проходит по сети
   (межсетевой экран на пути и на самих ESR тоже проверяется). Трафик в туннеле — ESP (протокол 50), содержимое в захвате не видно.
   Упрощения: IKEv1/v2 не различаются, lifetime/rekey/DPD не моделируются, NAT-T нет. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  var M = { ikeprop: '(config-ike-proposal)#', ikepol: '(config-ike-policy)#', ikegw: '(config-ike-gw)#', ipprop: '(config-ipsec-proposal)#',
            ippol: '(config-ipsec-policy)#', ipvpn: '(config-ipsec-vpn)#', vti: '(config-vti)#' };
  Object.keys(M).forEach(function (k) { S.PROMPT[k] = M[k]; });
  var ALL = Object.keys(M).join(' ');
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') Object.keys(M).forEach(function (k) { c.modes.push(k); }); });
  var OK = /^(no )?(ip address|ip firewall disable|security-zone|description|ip ospf|ip rip)\b/;
  S.T.forEach(function (c) { if (c.modes.indexOf('sub') >= 0 && OK.test(c.pat.join(' ')) && c.modes.indexOf('vti') < 0) c.modes.push('vti'); });
  function touch(st) { st.pending = true; }
  function sec(c) { return c.sec || (c.sec = { ikeProp: {}, ikePol: {}, ikeGw: {}, ipProp: {}, ipPol: {}, vpn: {} }); }
  function obj(st) { var p = st.ctx.split('|'); return sec(st.cand)[p[0]][p[1]]; }
  function enter(kind, mode, init) { return function (st, a) { var t = sec(st.cand)[kind]; if (!t[a[0]]) t[a[0]] = init(); touch(st); st.mode = mode; st.ctx = kind + '|' + a[0]; }; }
  function del(kind) { return function (st, a) { delete sec(st.cand)[kind][a[0]]; touch(st); }; }
  S.cmd('config', 'security ike proposal <w>', enter('ikeProp', 'ikeprop', function () { return {}; }), 'Профиль IKE');
  S.cmd('config', 'security ike policy <w>', enter('ikePol', 'ikepol', function () { return {}; }), 'Политика IKE');
  S.cmd('config', 'security ike gateway <w>', enter('ikeGw', 'ikegw', function () { return { mode: 'policy-based' }; }), 'Шлюз IKE');
  S.cmd('config', 'security ipsec proposal <w>', enter('ipProp', 'ipprop', function () { return {}; }), 'Профиль IPsec');
  S.cmd('config', 'security ipsec policy <w>', enter('ipPol', 'ippol', function () { return {}; }), 'Политика IPsec');
  S.cmd('config', 'security ipsec vpn <w>', enter('vpn', 'ipvpn', function () { return { on: false, est: 'by-request' }; }), 'IPsec VPN');
  [['ike proposal', 'ikeProp'], ['ike policy', 'ikePol'], ['ike gateway', 'ikeGw'], ['ipsec proposal', 'ipProp'], ['ipsec policy', 'ipPol'], ['ipsec vpn', 'vpn']].forEach(function (x) {
    S.cmd('config', 'no security ' + x[0] + ' <w>', del(x[1])); });
  function set(f) { return function (st, a) { var r = f(obj(st), a); touch(st); return r; }; }
  var ENC = ['des', '3des', 'blowfish128', 'blowfish192', 'blowfish256', 'aes128', 'aes192', 'aes256', 'aes128ctr', 'aes192ctr', 'aes256ctr', 'camellia128', 'camellia192', 'camellia256', 'null'];
  var AUTH = ['md5', 'sha1', 'sha2-256', 'sha2-384', 'sha2-512'];
  S.cmd('ikeprop ipprop', 'encryption algorithm <w>', set(function (o, a) { if (ENC.indexOf(a[0]) < 0) return 'Syntax error: Illegal parameter'; o.enc = a[0]; }), 'Алгоритм шифрования');
  S.cmd('ikeprop ipprop', 'authentication algorithm <w>', set(function (o, a) { if (AUTH.indexOf(a[0]) < 0) return 'Syntax error: Illegal parameter'; o.auth = a[0]; }), 'Алгоритм аутентификации');
  S.cmd('ikeprop', 'dh-group <n>', set(function (o, a) { if ([1, 2, 5].indexOf(a[0]) < 0 && (a[0] < 14 || a[0] > 31)) return 'Syntax error: Illegal parameter'; o.dh = a[0]; }), 'Группа Диффи-Хеллмана');
  S.cmd('ikepol', 'pre-shared-key ascii-text <w>', set(function (o, a) { o.psk = a[0]; }), 'Общий ключ');
  S.cmd('ikepol ippol', 'proposal <w>', set(function (o, a) { o.prop = a[0]; }), 'Привязать профиль');
  S.cmd('ikegw', 'ike-policy <w>', set(function (o, a) { o.pol = a[0]; }), 'Политика IKE');
  S.cmd('ikegw', 'local address <ip>', set(function (o, a) { o.local = a[0]; }), 'Адрес локального шлюза');
  S.cmd('ikegw', 'remote address <ip>', set(function (o, a) { o.remote = a[0]; }), 'Адрес удалённого шлюза');
  S.cmd('ikegw', 'mode <w>', set(function (o, a) { if (a[0] !== 'policy-based' && a[0] !== 'route-based') return 'Syntax error: Illegal parameter'; o.mode = a[0]; }), 'policy-based | route-based');
  S.cmd('ikegw', 'local network <w>', set(function (o, a) { var c = IP.parseCidr(a[0]); if (!c) return 'Syntax error: Illegal parameter'; o.lnet = IP.netOf(c.ip, c.len); }), 'Локальная подсеть');
  S.cmd('ikegw', 'remote network <w>', set(function (o, a) { var c = IP.parseCidr(a[0]); if (!c) return 'Syntax error: Illegal parameter'; o.rnet = IP.netOf(c.ip, c.len); }), 'Удалённая подсеть');
  S.cmd('ikegw', 'bind-interface vti <n>', set(function (o, a) { o.vti = a[0]; }), 'Туннель VTI (route-based)');
  S.cmd('ipvpn', 'ike establish-tunnel <w>', set(function (o, a) { if (['by-request', 'route', 'immediate'].indexOf(a[0]) < 0) return 'Syntax error: Illegal parameter'; o.est = a[0]; }), 'Режим активации');
  S.cmd('ipvpn', 'ike gateway <w>', set(function (o, a) { o.gw = a[0]; }), 'Шлюз IKE');
  S.cmd('ipvpn', 'ike ipsec-policy <w>', set(function (o, a) { o.pol = a[0]; }), 'Политика IPsec');
  S.cmd('ipvpn', 'enable', set(function (o) { o.on = true; }), 'Включить VPN');
  S.cmd('ipvpn', 'no enable', set(function (o) { o.on = false; }));
  S.cmd(ALL, 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  // tunnel vti N — как GRE, но содержимое шифруется
  S.cmd('config', 'tunnel vti <n>', function (st, a) { var k = 'vti' + a[0];
    if (!st.cand.ifs[k]) { st.cand.ifs[k] = { ip: null, fw: true, shut: false, tun: 'vti', on: false, local: null, remote: null }; touch(st); }
    st.mode = 'vti'; st.ctx = k; }, 'Туннель VTI');
  S.cmd('config', 'no tunnel vti <n>', function (st, a) { delete st.cand.ifs['vti' + a[0]]; touch(st); });
  S.cmd('vti', 'local address <ip>', function (st, a) { st.cand.ifs[st.ctx].local = a[0]; touch(st); }, 'IP-адрес локального шлюза');
  S.cmd('vti', 'remote address <ip>', function (st, a) { st.cand.ifs[st.ctx].remote = a[0]; touch(st); }, 'IP-адрес удалённого шлюза');
  S.cmd('vti', 'enable', function (st) { st.cand.ifs[st.ctx].on = true; touch(st); }, 'Включить туннель');
  S.cmd('vti', 'no enable', function (st) { st.cand.ifs[st.ctx].on = false; touch(st); });

  S.RUNX.push(function (c, o) { var s = c.sec; if (!s) return;
    function blk(head, x, lines) { o.push(head); lines.filter(Boolean).forEach(function (l) { o.push('  ' + l); }); o.push('exit'); void x; }
    Object.keys(s.ikeProp).forEach(function (n) { var x = s.ikeProp[n]; blk('security ike proposal ' + n, x, [x.auth && 'authentication algorithm ' + x.auth, x.enc && 'encryption algorithm ' + x.enc, x.dh && 'dh-group ' + x.dh]); });
    Object.keys(s.ikePol).forEach(function (n) { var x = s.ikePol[n]; blk('security ike policy ' + n, x, [x.psk && 'pre-shared-key ascii-text encrypted ' + EL.E.hash(x.psk).slice(0, 16), x.prop && 'proposal ' + x.prop]); });
    Object.keys(s.ikeGw).forEach(function (n) { var x = s.ikeGw[n]; blk('security ike gateway ' + n, x, [x.pol && 'ike-policy ' + x.pol, x.local && 'local address ' + x.local,
      x.lnet && 'local network ' + x.lnet, x.remote && 'remote address ' + x.remote, x.rnet && 'remote network ' + x.rnet, 'mode ' + x.mode, x.vti && 'bind-interface vti ' + x.vti]); });
    Object.keys(s.ipProp).forEach(function (n) { var x = s.ipProp[n]; blk('security ipsec proposal ' + n, x, [x.auth && 'authentication algorithm ' + x.auth, x.enc && 'encryption algorithm ' + x.enc]); });
    Object.keys(s.ipPol).forEach(function (n) { var x = s.ipPol[n]; blk('security ipsec policy ' + n, x, [x.prop && 'proposal ' + x.prop]); });
    Object.keys(s.vpn).forEach(function (n) { var x = s.vpn[n]; blk('security ipsec vpn ' + n, x, [x.est !== 'by-request' && 'ike establish-tunnel ' + x.est, x.gw && 'ike gateway ' + x.gw, x.pol && 'ike ipsec-policy ' + x.pol, x.on && 'enable']); });
  });
  // pre-shared-key из running-config при импорте конфигурации — хеш, ключ не восстанавливается
  S.cmd('ikepol', 'pre-shared-key ascii-text encrypted <w>', set(function (o, a) { o.pskEnc = a[0]; }));

  // ---------------------------------------------------------------- установление SA
  function full(c, vname) {      // параметры VPN с подставленными значениями по умолчанию
    var s = c.sec, v = s && s.vpn[vname]; if (!v) return { why: 'нет VPN ' + vname };
    var gw = s.ikeGw[v.gw]; if (!gw) return { why: 'не задан ike gateway' };
    var pol = s.ikePol[gw.pol]; if (!pol) return { why: 'у шлюза ' + v.gw + ' нет ike-policy' };
    var ip = s.ipPol[v.pol]; if (!ip) return { why: 'не задана ike ipsec-policy' };
    var ikp = s.ikeProp[pol.prop] || {}, ipp = s.ipProp[ip.prop] || {};
    if (!pol.prop || !s.ikeProp[pol.prop]) return { why: 'в политике IKE нет proposal' };
    if (!ip.prop || !s.ipProp[ip.prop]) return { why: 'в политике IPsec нет proposal' };
    return { v: v, gw: gw, psk: pol.psk || pol.pskEnc || null, ike: [ikp.enc || '3des', ikp.auth || 'sha1', ikp.dh || 1].join('/'), esp: [ipp.enc || '3des', ipp.auth || 'sha1'].join('/') };
  }
  P.ipsecSA = function (id, vname) {
    var s = this, d = this.devs[id], c = d.st.run, a = full(c, vname);
    if (!a.v) return { ok: false, why: a.why };
    if (!a.v.on) return { ok: false, why: 'VPN выключен (нет enable)' };
    if (!a.gw.local || !a.gw.remote) return { ok: false, why: 'у шлюза не задан local или remote address' };
    if (!a.psk) return { ok: false, why: 'не задан pre-shared-key' };
    var pid = this.owner(a.gw.remote), pd = pid && this.devs[pid];
    if (!pd || pd.type !== 'esr') return { ok: false, why: 'по адресу ' + a.gw.remote + ' нет маршрутизатора ESR' };
    var pv = Object.keys((pd.st.run.sec || {}).vpn || {}).map(function (n) { return { n: n, f: full(pd.st.run, n) }; })
      .filter(function (x) { return x.f.v && x.f.v.on && x.f.gw.local === a.gw.remote && x.f.gw.remote === a.gw.local; })[0];
    if (!pv) return { ok: false, why: pd.name + ': нет включённого VPN со шлюзом local ' + a.gw.remote + ' remote ' + a.gw.local };
    var b = pv.f;
    if (a.v.est === 'by-request' && b.v.est === 'by-request') return { ok: false, why: 'обе стороны ждут встречного соединения (ike establish-tunnel by-request)' };
    if (a.gw.mode !== b.gw.mode) return { ok: false, why: 'режимы шлюзов разные: ' + a.gw.mode + ' и ' + b.gw.mode };
    if (a.psk !== b.psk) return { ok: false, why: 'pre-shared-key не совпадает — IKE аутентификация не прошла' };
    if (a.ike !== b.ike) return { ok: false, why: 'IKE proposal не совпадает: ' + a.ike + ' и ' + b.ike + ' (шифрование/аутентификация/DH)' };
    if (a.esp !== b.esp) return { ok: false, why: 'IPsec proposal не совпадает: ' + a.esp + ' и ' + b.esp };
    if (a.gw.mode === 'policy-based' && (a.gw.lnet !== b.gw.rnet || a.gw.rnet !== b.gw.lnet)) return { ok: false, why: 'подсети политик не зеркальны: ' + a.gw.lnet + '→' + a.gw.rnet + ' и ' + b.gw.lnet + '→' + b.gw.rnet };
    var r = this.request(id, a.gw.remote, 'udp', 500);
    if (!r.ok) return { ok: false, why: 'IKE (UDP 500) до ' + a.gw.remote + ' не проходит — ' + (r.why || 'нет ответа'), steps: r.steps };
    return { ok: true, peer: pid, pv: pv.n, a: a, b: b };
  };
  P.vtiSA = function (id, n) {
    var c = this.devs[id].st.run, s = c.sec || { vpn: {}, ikeGw: {} }, self = this, why = 'нет VPN с ike gateway bind-interface vti ' + n;
    var hit = Object.keys(s.vpn).filter(function (v) { var gw = s.ikeGw[s.vpn[v].gw]; return gw && gw.mode === 'route-based' && gw.vti === n; });
    for (var i = 0; i < hit.length; i++) { var r = self.ipsecSA(id, hit[i]); if (r.ok) return r; why = r.why; }
    return { ok: false, why: why };
  };
  // policy-based: пакет из local network в remote network уходит в ESP к удалённому шлюзу
  P.ipsecForward = function (cur, pk, steps, ct) {
    if (pk.proto === 'esp' || pk.proto === 'gre' || this._ipsecIn) return null;
    var d = this.devs[cur], s = (d.st.run.sec || {}), self = this;
    var vn = Object.keys(s.vpn || {}).filter(function (n) { var f = full(d.st.run, n); return f.v && f.v.on && f.gw.mode === 'policy-based' && f.gw.lnet && f.gw.rnet &&
      IP.sameNet(pk.src, f.gw.lnet.split('/')[0], +f.gw.lnet.split('/')[1]) && IP.sameNet(pk.dst, f.gw.rnet.split('/')[0], +f.gw.rnet.split('/')[1]); })[0];
    if (!vn) return null;
    var sa = this.ipsecSA(cur, vn);
    if (!sa.ok) { steps.push({ k: 'drop', t: d.name + ': пакет ' + pk.src + ' → ' + pk.dst + ' попадает в политику VPN ' + vn + ', но IPsec SA не установлена: ' + sa.why }); return { ok: false }; }
    var gw = sa.a.gw;
    steps.push({ k: 'route', t: d.name + ': политика VPN ' + vn + ' (' + gw.lnet + ' → ' + gw.rnet + ') — пакет зашифрован в ESP: внешний заголовок ' + gw.local + ' → ' + gw.remote + ' (протокол 50, ' + sa.a.esp + ')' });
    var outer = { src: gw.local, dst: gw.remote, proto: 'esp', dport: null, inner: { src: pk.src, dst: pk.dst, proto: pk.proto, reply: !!pk.reply, dport: pk.dport, sport: pk.sport }, spi: spi(d.name + vn) };
    this._ipsecIn = true; var o; try { o = this.send(cur, outer, steps, ct); } finally { this._ipsecIn = false; }
    if (!o.ok || o.dev !== sa.peer) { steps.push({ k: 'drop', t: 'ESP-пакет не дошёл до ' + gw.remote }); return { ok: false }; }
    var pd = this.devs[o.dev];
    steps.push({ k: 'route', t: pd.name + ': ESP расшифрован (VPN ' + sa.pv + ') — внутри ' + pk.src + ' → ' + pk.dst });
    void self; return { ok: true, dev: o.dev, ip: gw.remote };
  };
  function spi(x) { return '0x' + EL.E.hash(x).slice(0, 8); }
  S.cmd('priv', 'show security ipsec vpn status', function (st) {
    var s = st.net, c = st.run, V = Object.keys((c.sec || {}).vpn || {}); if (!s) return '';
    var o = ['Name      Local host   Remote host  Initiator spi       Responder spi        State', '--------- ------------ ------------ ---------------     ---------------      ------'];
    V.forEach(function (n) { var f = full(c, n), r = s.ipsecSA(st.dev, n), gw = f.gw || {};
      o.push(rp(n, 10) + rp(gw.local || '--', 13) + rp(gw.remote || '--', 13) + rp(r.ok ? '0x' + EL.E.hash(n + 'i').slice(0, 16) : '--', 20) + rp(r.ok ? '0x' + EL.E.hash(n + 'r').slice(0, 16) : '--', 21) + (r.ok ? 'Established' : 'Down')); });
    return o.join('\n'); }, 'Состояние IPsec VPN');
  S.cmd('priv', 'show security ipsec vpn status <w>', function (st, a) { var s = st.net; if (!s) return '';
    var r = s.ipsecSA(st.dev, a[0]); return a[0] + ': ' + (r.ok ? 'Established' : 'Down — ' + r.why); });
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
})(typeof window !== 'undefined' ? window : global);
