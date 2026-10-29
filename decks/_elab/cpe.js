/* Абонентский роутер RG-35-WZ (руководство 2.3.0): управление через веб-интерфейс (меню «TCP/IP» → «Настройка LAN», «Настройка WAN»).
   Порты: WAN = gi1/0/1, LAN 1–4 = gi1/0/2–5 (имена ESR — допущение эмулятора; внутри роутер работает на модели ESR: мост LAN, DHCP-сервер, Source NAT).
   Заводские: LAN 192.168.1.1/24, DHCP-сервер включён (пул в руководстве не указан — 192.168.1.2–192.168.1.254), WAN — IPoE DHCP Client, вход admin / password.
   WAN: Static IP (адрес, маска, шлюз) или DHCP Client (адрес и шлюз от DHCP-сервера провайдера, запрос при применении и по кнопке «Обновить»).
   Упрощения: PPPoE, Bridge, VLAN WAN, Wi-Fi, IPv6, TR-069 и телнет-CLI (в руководстве не описана) не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip;
  function isC(d) { return !!d && d.sub === 'cpe'; }
  EL.isCpe = isC;
  var DEF = { lan: { ip: '192.168.1.1', mask: '255.255.255.0', dhcp: true, from: '192.168.1.2', to: '192.168.1.254', lease: 1440 }, wan: { mode: 'dhcp', ip: '', mask: '255.255.255.0', gw: '' }, user: 'admin', pw: 'password' };
  var exE = P.exec;
  function esr(net, id, lines) { var errs = []; lines.forEach(function (l) { var r = exE.call(net, id, l); if (typeof r === 'string' && /Syntax error|^%/.test(r)) errs.push(l + ' → ' + r); }); return errs; }
  // веб-настройки → конфигурация ESR (полностью пересобирается)
  P.cpeApply = function (id, w) {
    var d = this.devs[id], st = d.st, net = this, c = st.cpe; if (w) c.web = EL.clone(w); w = c.web;
    var L = w.lan, len = IP.mask2len(L.mask), wan = w.wan;
    st.mode = 'priv'; var users = st.run.users; st.cand = EL.esr.fresh('RG-35-WZ', 5).cand; st.cand.users = EL.clone(users);   // конфигурация пересобирается с нуля
    var lines = ['configure'];
    lines = lines.concat(['interface gigabitethernet 1/0/1', 'ip firewall disable', wan.mode === 'static' && wan.ip ? 'ip address ' + wan.ip + '/' + IP.mask2len(wan.mask) : 'no ip address', 'exit']);
    lines = lines.concat(['bridge 1', 'ip firewall disable', 'ip address ' + L.ip + '/' + len, 'enable', 'exit']);
    [2, 3, 4, 5].forEach(function (p) { lines.push('interface gigabitethernet 1/0/' + p, 'bridge-group 1', 'exit'); });
    if (L.dhcp) lines = lines.concat(['ip dhcp-server', 'ip dhcp-server pool LAN', 'network ' + IP.netOf(L.ip, len), 'address-range ' + L.from + '-' + L.to, 'default-router ' + L.ip, 'dns-server ' + L.ip, 'exit']);
    lines = lines.concat(['nat source', 'ruleset WAN', 'to interface gigabitethernet 1/0/1', 'rule 10', 'match source-address address-range ' + IP.n2ip(IP.ip2n(IP.netOf(L.ip, len).split('/')[0]) + 1) + '-' +
      IP.n2ip((IP.ip2n(L.ip) | (~IP.maskN(len) >>> 0)) - 1 >>> 0), 'action source-nat interface', 'enable', 'exit', 'exit', 'exit']);
    var gw = wan.mode === 'static' ? wan.gw : (c.lease && c.lease.gw);
    if (wan.mode === 'dhcp' && c.lease) lines = lines.concat(['interface gigabitethernet 1/0/1', 'ip address ' + c.lease.ip + '/' + c.lease.len, 'exit']);
    if (gw) lines.push('ip route 0.0.0.0/0 ' + gw);
    lines = lines.concat(['end', 'commit', 'confirm']);
    var errs = esr(net, id, lines); net.gen++; return errs;
  };
  // DHCP Client на WAN: запрос с порта WAN (как у ПК), адрес и шлюз — в конфигурацию
  P.cpeDhcp = function (id) { var d = this.devs[id], c = d.st.cpe; if (c.web.wan.mode !== 'dhcp') return null;
    d.st.port = 'gi1/0/1'; var r = this.dhcp(id); if (r.ok) { c.lease = { ip: r.ip, len: r.len, gw: r.gw, server: r.server }; this.cpeApply(id); } else c.lease = null;
    return r; };
  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {};
    if (m.kind === 'cpe') { d.sub = 'cpe'; d.st.port = 'gi1/0/1'; d.st.cpe = { web: EL.clone(DEF), lease: null }; d.st.run.users.admin.pw = 'password'; d.st.cand.users.admin.pw = 'password';
      this.cpeApply(d.id); }
    return d; };
  // консоль: CLI роутера в руководстве не описана — настройка через веб-интерфейс
  P.exec = function (id, line) { var d = this.devs[id]; if (isC(d)) { this.gen++; return String(line).trim() ? 'RG-35-WZ: настройка — через веб-интерфейс (ПКМ по роутеру → «Веб-интерфейс» или с ПК в LAN: open http://' + d.st.cpe.web.lan.ip + ')' : ''; }
    return exE.apply(this, arguments); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id]; return isC(d) ? 'RG-35-WZ> ' : pr0.apply(this, arguments); };
  // после перезагрузки — те же веб-настройки (хранятся в устройстве), WAN по DHCP — запрос заново
  var boot0 = P.reboot;
  if (boot0) P.reboot = function (id) { var d = this.devs[id], keep = isC(d) && d.st.cpe; var r = boot0.apply(this, arguments); d = this.devs[id];
    if (keep) { d.sub = 'cpe'; d.st.cpe = keep; d.st.port = 'gi1/0/1'; d.st.run.users.admin.pw = 'password'; d.st.cand.users.admin.pw = 'password'; this.cpeApply(id); if (keep.web.wan.mode === 'dhcp') this.cpeDhcp(id); }
    return r; };
  // Debian в LAN: open http://<адрес LAN> — страница роутера (окно открывает интерфейс эмулятора)
  EL.cpeAt = function (net, ip) { return net.list().filter(function (d) { return isC(d) && d.st.cpe.web.lan.ip === ip; })[0] || null; };
})(typeof window !== 'undefined' ? window : global);
