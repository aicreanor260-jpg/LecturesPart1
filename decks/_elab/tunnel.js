/* GRE-туннели ESR (справочник ESR-Series CLI 1.23): tunnel gre <N> → (config-gre)#: local address, remote address, ip address,
   ip firewall disable | security-zone, description, enable; show tunnels status. Обозначение туннеля — gre N.
   Пакет, ушедший в туннель, инкапсулируется: внешний IPv4 local → remote, протокол 47 (GRE), и идёт по сети как обычный пакет
   (ARP, маршруты, NAT, межсетевой экран на пути); на удалённом ESR с зеркальным туннелем GRE снимается.
   Упрощения: keepalive нет (туннель Up, если включён и задан), RIP/OSPF через туннель не строят соседство — маршруты в туннель статические. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  S.PROMPT.gre = '(config-gre)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('gre'); });
  // команды IP-интерфейса, которые есть и у туннеля
  var OK = /^(no )?(ip address|ip firewall disable|security-zone|description|ip ospf|ip rip)\b/;
  S.T.forEach(function (c) { if (c.modes.indexOf('sub') >= 0 && OK.test(c.pat.join(' ')) && c.modes.indexOf('gre') < 0) c.modes.push('gre'); });
  function touch(st) { st.pending = true; }
  function cur(st) { return st.cand.ifs[st.ctx]; }
  S.cmd('config', 'tunnel gre <n>', function (st, a) {
    if (a[0] < 1 || a[0] > 1000) return 'Syntax error: Illegal parameter';
    var k = 'gre' + a[0]; if (!st.cand.ifs[k]) { st.cand.ifs[k] = { ip: null, fw: true, shut: false, tun: 'gre', on: false, local: null, remote: null }; touch(st); }
    st.mode = 'gre'; st.ctx = k; }, 'GRE-туннель');
  S.cmd('config', 'no tunnel gre <n>', function (st, a) { delete st.cand.ifs['gre' + a[0]]; touch(st); });
  S.cmd('gre', 'local address <ip>', function (st, a) { cur(st).local = a[0]; touch(st); }, 'IP-адрес локального шлюза');
  S.cmd('gre', 'no local address', function (st) { cur(st).local = null; touch(st); });
  S.cmd('gre', 'remote address <ip>', function (st, a) { cur(st).remote = a[0]; touch(st); }, 'IP-адрес удалённого шлюза');
  S.cmd('gre', 'no remote address', function (st) { cur(st).remote = null; touch(st); });
  S.cmd('gre', 'enable', function (st) { cur(st).on = true; touch(st); }, 'Включить туннель');
  S.cmd('gre', 'no enable', function (st) { cur(st).on = false; touch(st); });
  S.cmd('gre', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  S.cmd('priv', 'show tunnels status', function (st) {
    var s = st.net, o = ['Tunnel     Admin state        MTU      Local IP           Remote IP          Uptime', '------      ----------       -----    ------------       -----------        ---------------'];
    Object.keys(st.run.ifs).filter(function (k) { return st.run.ifs[k].tun; }).forEach(function (k) { var x = st.run.ifs[k];
      o.push(rp('gre ' + k.slice(3), 11) + rp(x.on ? 'Up' : 'Down', 18) + rp('1476', 9) + rp(x.local || '--', 19) + rp(x.remote || '--', 19) + (x.on && s ? up(s.now) : '--')); });
    return o.join('\n'); }, 'Состояние туннелей');
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function up(n) { n = Math.floor(n); return Math.floor(n / 60) + ' minute' + (Math.floor(n / 60) === 1 ? '' : 's') + ' and ' + n % 60 + ' seconds'; }

  // ---------------------------------------------------------------- инкапсуляция при пересылке
  P.tunnel = function (cur, r, pk, steps, ct) {
    var s = this, d = this.devs[cur], k = r.iface.name, x = d.st.run.ifs[k];
    if ((this._tunDepth || 0) > 2) { steps.push({ k: 'drop', t: d.name + ': рекурсивная маршрутизация — адрес удалённого конца туннеля доступен только через сам туннель' }); return { ok: false }; }
    if (!this.ifaces(cur).some(function (f) { return f.ip === x.local && !f.tun; })) { steps.push({ k: 'drop', t: d.name + ': local address ' + x.local + ' туннеля gre ' + k.slice(3) + ' не принадлежит ни одному интерфейсу' }); return { ok: false }; }
    steps.push({ k: 'route', t: d.name + ': маршрут через туннель gre ' + k.slice(3) + ' — пакет ' + pk.src + ' → ' + pk.dst + ' инкапсулирован в GRE: внешний заголовок ' + x.local + ' → ' + x.remote + ' (протокол 47)' });
    var outer = { src: x.local, dst: x.remote, proto: 'gre', dport: null, inner: { src: pk.src, dst: pk.dst, proto: pk.proto, reply: !!pk.reply, dport: pk.dport, sport: pk.sport } };
    this._tunDepth = (this._tunDepth || 0) + 1;
    var o; try { o = this.send(cur, outer, steps, ct); } finally { this._tunDepth--; }
    if (!o.ok) { steps.push({ k: 'drop', t: 'GRE-пакет не дошёл до удалённого конца ' + x.remote }); return { ok: false }; }
    var pd = this.devs[o.dev], pk2 = pd.type === 'esr' ? Object.keys(pd.st.run.ifs).filter(function (q) { var y = pd.st.run.ifs[q];
      return y.tun === 'gre' && y.on && y.local === x.remote && y.remote === x.local && y.ip; })[0] : null;
    if (!pk2) { steps.push({ k: 'drop', t: pd.name + ': нет включённого GRE-туннеля с local ' + x.remote + ' и remote ' + x.local + ' — GRE-пакет отброшен' }); return { ok: false }; }
    var y = pd.st.run.ifs[pk2], tf = { name: pk2, ip: y.ip.split('/')[0], fw: y.fw };
    var fw = this.fwPass(o.dev, tf, pk, ct, { src: pk.src, dst: pk.dst });
    if (fw.t) steps.push({ k: fw.ok ? 'route' : 'drop', t: fw.t });
    if (!fw.ok) return { ok: false };
    steps.push({ k: 'route', t: pd.name + ': GRE снят на gre ' + pk2.slice(3) + ' — внутри ' + pk.src + ' → ' + pk.dst });
    void s; return { ok: true, dev: o.dev, ip: tf.ip };
  };
})(typeof window !== 'undefined' ? window : global);
