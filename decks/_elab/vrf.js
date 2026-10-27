/* VRF на ESR (справочник ESR-Series CLI 1.23): ip vrf <NAME> → (config-vrf)#; на интерфейсе ip vrf forwarding <NAME>;
   ip route vrf <NAME> <SUBNET> <NEXTHOP>; show ip route vrf <NAME>; ping vrf <NAME> <ADDR>.
   У каждого VRF своя таблица маршрутов: пакет, пришедший на интерфейс VRF, ищет маршрут только среди сетей этого VRF —
   одинаковые адреса в разных VRF не мешают друг другу, а сети разных VRF друг друга не видят.
   Упрощения: RIP/OSPF/BGP работают только в глобальной таблице, утечки маршрутов между VRF (route-target, import) нет. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  S.PROMPT.vrf = '(config-vrf)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('vrf'); });
  function touch(st) { st.pending = true; }
  function each(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k], k); }); touch(st); }
  S.cmd('config', 'ip vrf <w>', function (st, a) { if (!/^[\w.-]{1,31}$/.test(a[0])) return 'Syntax error: Illegal parameter';
    var V = st.cand.vrfs = st.cand.vrfs || {}; V[a[0]] = V[a[0]] || {}; touch(st); st.mode = 'vrf'; st.ctx = a[0]; }, 'Создать VRF');
  S.cmd('config', 'no ip vrf <w>', function (st, a) { var V = st.cand.vrfs || {}; delete V[a[0]];
    Object.keys(st.cand.ifs).forEach(function (k) { if (st.cand.ifs[k].vrf === a[0]) delete st.cand.ifs[k].vrf; });
    st.cand.routes = st.cand.routes.filter(function (r) { return r.vrf !== a[0]; }); touch(st); });
  S.cmd('vrf', 'description <rest>', function (st, a) { st.cand.vrfs[st.ctx].desc = a[0].replace(/^["']|["']$/g, ''); touch(st); }, 'Описание VRF');
  S.cmd('vrf', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  var IFM = 'gi sub lo gre vti';
  S.cmd(IFM, 'ip vrf forwarding <w>', function (st, a) { if (!(st.cand.vrfs || {})[a[0]]) return 'Syntax error: VRF ' + a[0] + ' not found';
    each(st, function (x) { x.vrf = a[0]; }); }, 'Интерфейс в VRF');
  S.cmd(IFM, 'no ip vrf forwarding', function (st) { each(st, function (x) { delete x.vrf; }); });
  S.cmd('config', 'ip route vrf <w> <w> <ip>', function (st, a) { return addRoute(st, a[0], a[1], a[2]); }, 'Статический маршрут в VRF');
  S.cmd('config', 'ip route vrf <w> <w> <ip> <n>', function (st, a) { return addRoute(st, a[0], a[1], a[2], a[3]); });
  S.cmd('config', 'no ip route vrf <w> <w> <ip>', function (st, a) { var c = IP.parseCidr(a[1]); if (!c) return 'Syntax error: Illegal parameter';
    var net = IP.netOf(c.ip, c.len); st.cand.routes = st.cand.routes.filter(function (r) { return !(r.vrf === a[0] && r.net === net && r.nh === a[2]); }); touch(st); });
  function addRoute(st, v, cidr, nh, ad) {
    if (!(st.cand.vrfs || {})[v]) return 'Syntax error: VRF ' + v + ' not found';
    var c = IP.parseCidr(cidr); if (!c || (ad !== undefined && (ad < 1 || ad > 255))) return 'Syntax error: Illegal parameter';
    var net = IP.netOf(c.ip, c.len); st.cand.routes = st.cand.routes.filter(function (r) { return !(r.vrf === v && r.net === net && r.nh === nh); });
    st.cand.routes.push({ net: net, nh: nh, ad: ad || 1, vrf: v }); touch(st);
  }
  S.RUNX.push(function (c, o) {
    Object.keys(c.vrfs || {}).forEach(function (v) { o.push('ip vrf ' + v); if (c.vrfs[v].desc) o.push('  description "' + c.vrfs[v].desc + '"'); o.push('exit'); });
    Object.keys(c.ifs).forEach(function (k) { if (c.ifs[k].vrf) o.push((c.ifs[k].tun ? 'tunnel ' + c.ifs[k].tun + ' ' + k.slice(3) : 'interface ' + S.longIf(k)), '  ip vrf forwarding ' + c.ifs[k].vrf, 'exit'); });
  });
  // таблица маршрутов — только своего VRF (глобальная — без VRF)
  var routes0 = P.routes;
  P.routes = function (id) {
    var r = routes0.apply(this, arguments), d = this.devs[id], ctx = this._vrfCtx || null;
    if (d.type !== 'esr') return r;
    return r.filter(function (x) { return (x.vrf || null) === ctx; });
  };
  // RIP/OSPF считаются в глобальной таблице, даже если расчёт запущен из поиска маршрута в VRF
  var dyn0 = P.dyn;
  P.dyn = function () { var o = this._vrfCtx; this._vrfCtx = null; try { return dyn0.apply(this, arguments); } finally { this._vrfCtx = o; } };
  function inVrf(s, st, v, f) { var o = s._vrfCtx; s._vrfCtx = v; try { return f(); } finally { s._vrfCtx = o; } }
  S.cmd('priv', 'show ip route vrf <w>', function (st, a) { if (!st.net) return ''; if (!(st.run.vrfs || {})[a[0]]) return 'Syntax error: VRF ' + a[0] + ' not found';
    return inVrf(st.net, st, a[0], function () { return st.net.routeText(st.dev, false); }); }, 'Таблица маршрутов VRF');
  S.cmd('priv', 'ping vrf <w> <ip>', function (st, a) { var s = st.net; if (!s) return ''; if (!(st.run.vrfs || {})[a[0]]) return 'Syntax error: VRF ' + a[0] + ' not found';
    s._vrfSrc = { dev: st.dev, vrf: a[0] }; try { return s.pingText(st.dev, a[1], 'esr'); } finally { s._vrfSrc = null; } }, 'Ping из VRF');
  S.cmd('priv', 'show ip vrf', function (st) { var V = st.run.vrfs || {};
    return ['Name                             Interfaces', '-------------------------------  ----------------------------------'].concat(Object.keys(V).map(function (v) {
      var ifs = Object.keys(st.run.ifs).filter(function (k) { return st.run.ifs[k].vrf === v; });
      var x = v; while (x.length < 33) x += ' '; return x + ifs.join(', '); })).join('\n'); }, 'Список VRF');
})(typeof window !== 'undefined' ? window : global);
