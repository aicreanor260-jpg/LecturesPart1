/* «Облако провайдера» — готовая сеть оператора между площадками: порты gi1/0/1–8 с адресами (шлюзы для клиентов), статические маршруты,
   задержка через облако, скорость и потери. Внутри — модель ESR (маршрутизация, ARP, трасса), настройка — в окне «Облако провайдера» (ПКМ).
   Задержка делится поровну на вход и выход (кабели к облаку), скорость — ограничение каналов к облаку, потери — на проход через облако.
   Своё облако оператора — на маршрутизаторах ME с MPLS и L3VPN (раздел «Маршрутизаторы ME»). */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip;
  var PORTS = []; for (var i = 1; i <= 8; i++) PORTS.push('gi1/0/' + i);
  EL.MODELS['Облако провайдера'] = { type: 'esr', kind: 'isp', ports: 8, portList: PORTS, group: 'Провайдер', host: 'isp',
    note: 'готовая сеть оператора: адреса портов, маршруты, задержка, скорость, потери — в окне «Облако провайдера» (ПКМ)' };
  function isI(d) { return !!d && d.sub === 'isp'; }
  EL.isIsp = isI;
  var DEF = { ports: {}, routes: [], delay: 20, mbps: 100, loss: 0 };
  var exE = P.exec;
  function esr(net, id, lines) { var errs = []; lines.forEach(function (l) { var r = exE.call(net, id, l); if (typeof r === 'string' && /Syntax error|^%/.test(r)) errs.push(l + ' → ' + r); }); return errs; }
  // настройки окна → конфигурация ESR (пересобирается целиком)
  P.ispApply = function (id, c) {
    var d = this.devs[id], st = d.st; if (c) st.isp = EL.clone(c); c = st.isp;
    st.mode = 'priv'; var users = st.run.users; st.cand = EL.esr.fresh('isp', 8, PORTS).cand; st.cand.users = EL.clone(users);
    var L = ['configure'];
    PORTS.forEach(function (p) { var x = c.ports[p]; L.push('interface gigabitethernet ' + p.slice(2), 'ip firewall disable'); if (x && x.ip) L.push('ip address ' + x.ip + '/' + x.len); L.push('exit'); });
    c.routes.forEach(function (r) { L.push('ip route ' + r.net + ' ' + r.nh); });
    L.push('end', 'commit', 'confirm');
    var errs = esr(this, id, L); this.gen++; return errs;
  };
  P.ispCheck = function (c) {
    var bad = null;
    Object.keys(c.ports).forEach(function (p) { var x = c.ports[p]; if (!bad && x.ip && (IP.ip2n(x.ip) === null || !(x.len >= 1 && x.len <= 32))) bad = p + ': адрес и маска'; });
    c.routes.forEach(function (r) { var q = IP.parseCidr(r.net); if (!bad && (!q || IP.ip2n(r.nh) === null)) bad = 'маршрут ' + r.net + ' через ' + r.nh; });
    if (!bad && !(c.delay >= 0 && c.delay <= 2000)) bad = 'задержка 0–2000 мс'; if (!bad && !(c.mbps > 0)) bad = 'скорость';
    if (!bad && !(c.loss >= 0 && c.loss <= 100)) bad = 'потери 0–100 %'; return bad; };
  var add0 = P.add;
  P.add = function (model) { var d = add0.apply(this, arguments), m = EL.MODELS[model] || {};
    if (m.kind === 'isp') { d.sub = 'isp'; d.st.isp = EL.clone(DEF); this.ispApply(d.id); } return d; };
  P.exec = function (id, line) { var d = this.devs[id]; if (isI(d)) { this.gen++; return String(line).trim() ? 'Облако провайдера: настройка — в окне «Облако провайдера» (ПКМ по облаку)' : ''; }
    return exE.apply(this, arguments); };
  var pr0 = P.prompt; P.prompt = function (id) { return isI(this.devs[id]) ? 'isp> ' : pr0.apply(this, arguments); };
  var boot0 = P.reboot;
  if (boot0) P.reboot = function (id) { var d = this.devs[id], keep = isI(d) && d.st.isp; var r = boot0.apply(this, arguments); d = this.devs[id];
    if (keep) { d.sub = 'isp'; d.st.isp = keep; this.ispApply(id); } return r; };
  // проход через облако: половина задержки и половина потерь — на каждом кабеле к облаку, скорость — предел канала
  function ends(net, l) { return [net.devs[l.a.dev], net.devs[l.b.dev]].filter(isI); }
  P.extraDelay = function (l) { return ends(this, l).reduce(function (t, d) { return t + (d.st.isp.delay || 0) / 2000; }, 0); };
  P.linkCap = function (l) { return ends(this, l).reduce(function (m, d) { return Math.min(m, d.st.isp.mbps || 1e9); }, l.mbps || 1e9); };
  var ll0 = P.linkLoss;
  if (ll0) P.linkLoss = function (l, bytes) { var p = ll0.apply(this, arguments);
    ends(this, l).forEach(function (d) { var q = (d.st.isp.loss || 0) / 100; if (q) p = 1 - (1 - p) * Math.sqrt(1 - q); }); return Math.min(1, p); };
})(typeof window !== 'undefined' ? window : global);
