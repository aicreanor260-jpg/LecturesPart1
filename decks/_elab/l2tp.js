/* L2TPv3 и bridge-group на ESR (справочник ESR-Series CLI 1.23):
   tunnel l2tpv3 <N> → (config-l2tpv3)#: local address, remote address, local session-id, remote session-id, protocol ip | udp,
   bridge-group <BRIDGE-ID>, enable; на интерфейсе / саб-интерфейсе: bridge-group <BRIDGE-ID>; bridge <N> (ip address, enable) — L3 моста.
   Кадры между интерфейсами одного bridge-group коммутируются (L2-домен), через туннель L2TPv3 переносятся на мост удалённого ESR —
   два офиса оказываются в одной L2-сети. Туннель работает, если у пары зеркальные адреса и session-id и IP-связь между ними есть.
   Упрощения: cookie, порты UDP, MTU туннеля и L2TP (удалённый доступ, PPP) не моделируются; MAC-таблица моста ESR не ведётся. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype;
  S.PROMPT.l2v3 = '(config-l2tpv3)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('l2v3'); });
  function touch(st) { st.pending = true; }
  function T(st) { return st.cand.l2v3[st.ctx]; }
  S.cmd('config', 'tunnel l2tpv3 <n>', function (st, a) { var L = st.cand.l2v3 = st.cand.l2v3 || {};
    L[a[0]] = L[a[0]] || { local: null, remote: null, lsid: null, rsid: null, proto: 'udp', bg: null, on: false }; touch(st); st.mode = 'l2v3'; st.ctx = a[0]; }, 'Туннель L2TPv3');
  S.cmd('config', 'no tunnel l2tpv3 <n>', function (st, a) { if (st.cand.l2v3) delete st.cand.l2v3[a[0]]; touch(st); });
  S.cmd('l2v3', 'local address <ip>', function (st, a) { T(st).local = a[0]; touch(st); }, 'IP-адрес локального шлюза');
  S.cmd('l2v3', 'remote address <ip>', function (st, a) { T(st).remote = a[0]; touch(st); }, 'IP-адрес удалённого шлюза');
  S.cmd('l2v3', 'local session-id <n>', function (st, a) { if (a[0] < 1 || a[0] > 200000) return 'Syntax error: Illegal parameter'; T(st).lsid = a[0]; touch(st); }, 'Свой идентификатор сессии');
  S.cmd('l2v3', 'remote session-id <n>', function (st, a) { if (a[0] < 1 || a[0] > 200000) return 'Syntax error: Illegal parameter'; T(st).rsid = a[0]; touch(st); }, 'Идентификатор сессии на той стороне');
  S.cmd('l2v3', 'protocol <w>', function (st, a) { if (a[0] !== 'ip' && a[0] !== 'udp') return 'Syntax error: Illegal parameter'; T(st).proto = a[0]; touch(st); }, 'Инкапсуляция ip | udp');
  S.cmd('l2v3', 'bridge-group <n>', function (st, a) { T(st).bg = a[0]; touch(st); }, 'Мост, в который входит туннель');
  S.cmd('l2v3', 'no bridge-group', function (st) { T(st).bg = null; touch(st); });
  S.cmd('l2v3', 'enable', function (st) { T(st).on = true; touch(st); }, 'Включить туннель');
  S.cmd('l2v3', 'no enable', function (st) { T(st).on = false; touch(st); });
  S.cmd('l2v3', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  S.cmd('gi sub', 'bridge-group <n>', function (st, a) { var bad = null;
    (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { var x = st.cand.ifs[k]; if (x.ip) bad = 'Syntax error: interface ' + k + ' has IP address'; else x.bg = a[0]; });
    touch(st); return bad; }, 'Интерфейс в L2-домен моста');
  S.cmd('gi sub', 'no bridge-group', function (st) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { delete st.cand.ifs[k].bg; }); touch(st); });
  S.RUNX.push(function (c, o) {
    Object.keys(c.ifs).forEach(function (k) { if (c.ifs[k].bg) o.push('interface ' + S.longIf(k), '  bridge-group ' + c.ifs[k].bg, 'exit'); });
    Object.keys(c.l2v3 || {}).forEach(function (t) { var x = c.l2v3[t]; o.push('tunnel l2tpv3 ' + t);
      if (x.local) o.push('  local address ' + x.local); if (x.remote) o.push('  remote address ' + x.remote); if (x.lsid) o.push('  local session-id ' + x.lsid);
      if (x.rsid) o.push('  remote session-id ' + x.rsid); if (x.proto !== 'udp') o.push('  protocol ' + x.proto); if (x.bg) o.push('  bridge-group ' + x.bg); if (x.on) o.push('  enable'); o.push('exit'); });
  });
  // IP-связь между концами туннеля (без побочных эффектов): по таблицам маршрутов и L2-рассылке
  function reach(s, src, dst) {
    var cur = src;
    for (var i = 0; i < 16; i++) { if (s.ifaces(cur).some(function (f) { return f.ip === dst; })) return true;
      var r = s.lookup(cur, dst); if (!r || r.iface.tun || r.iface.bg) return false;
      var ep = s.flood(cur, r.iface).eps.filter(function (e) { return e.iface.ip === r.nh; })[0]; if (!ep) return false; cur = ep.dev; }
    return false;
  }
  P.l2v3Peer = function (dev, t) {
    var s = this, c = s.devs[dev].st.run, x = (c.l2v3 || {})[t];
    if (!x || !x.local || !x.remote || !x.lsid || !x.rsid) return { why: 'не заданы адреса или session-id' };
    if (!s.ifaces(dev).some(function (f) { return f.ip === x.local; })) return { why: 'local address ' + x.local + ' не принадлежит интерфейсу' };
    var pid = s.owner(x.remote), pd = pid && s.devs[pid]; if (!pd || pd.type !== 'esr' || pd.off) return { why: 'по адресу ' + x.remote + ' нет ESR' };
    var L = pd.st.run.l2v3 || {}, pt = Object.keys(L).filter(function (q) { var y = L[q]; return y.on && y.local === x.remote && y.remote === x.local; })[0];
    if (!pt) return { why: 'на ' + pd.name + ' нет включённого туннеля L2TPv3 с local ' + x.remote + ' remote ' + x.local };
    var y = L[pt]; if (y.lsid !== x.rsid || y.rsid !== x.lsid) return { why: 'session-id не совпадают (у нас ' + x.lsid + '/' + x.rsid + ', у соседа ' + y.lsid + '/' + y.rsid + ')' };
    if (y.proto !== x.proto) return { why: 'разная инкапсуляция: ' + x.proto + ' и ' + y.proto };
    if (!y.bg) return { why: 'на ' + pd.name + ' туннель не в bridge-group' };
    var k = dev + '|' + t, C = s._l2c && s._l2c.gen === s.gen ? s._l2c : (s._l2c = { gen: s.gen });
    if (C[k] === undefined) C[k] = reach(s, dev, x.remote);
    if (!C[k]) return { why: 'нет IP-связи с ' + x.remote };
    return { dev: pid, t: pt, bg: y.bg };
  };
})(typeof window !== 'undefined' ? window : global);
