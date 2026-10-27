/* PBR — маршрутизация по политике на ESR (справочник ESR-Series CLI 1.23):
   route-map <NAME> → (config-route-map)#: rule <ORDER> → (config-route-map-rule)#: match ip access-group <ACL>,
   action set ip next-hop <NEXTHOP>, action deny (пакет идёт по обычной таблице), enable;
   на интерфейсе: ip policy route-map <NAME>. Пакет, пришедший на такой интерфейс и попавший под ACL правила
   (permit в ip access-list extended), уходит на заданный next-hop мимо таблицы маршрутов; next-hop должен быть
   в подключённой сети. Не подошло ни одно правило — обычная маршрутизация. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, IP = EL.ip;
  S.PROMPT.rmap = '(config-route-map)#'; S.PROMPT.rmapr = '(config-route-map-rule)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('rmap', 'rmapr'); });
  function touch(st) { st.pending = true; }
  function rm(st) { var p = st.ctx.split('|'); return st.cand.rmaps[p[0]]; }
  function rule(st) { var p = st.ctx.split('|'); return st.cand.rmaps[p[0]].rules[p[1]]; }
  S.cmd('config', 'route-map <w>', function (st, a) { if (!/^[\w.-]{1,31}$/.test(a[0])) return 'Syntax error: Illegal parameter';
    var M = st.cand.rmaps = st.cand.rmaps || {}; M[a[0]] = M[a[0]] || { rules: {} }; touch(st); st.mode = 'rmap'; st.ctx = a[0]; }, 'Маршрутная карта (PBR)');
  S.cmd('config', 'no route-map <w>', function (st, a) { if (st.cand.rmaps) delete st.cand.rmaps[a[0]]; touch(st); });
  S.cmd('rmap', 'rule <n>', function (st, a) { if (a[0] < 1 || a[0] > 10000) return 'Syntax error: Illegal parameter';
    var R = rm(st).rules; R[a[0]] = R[a[0]] || { act: 'permit', on: false }; touch(st); st.mode = 'rmapr'; st.ctx = st.ctx + '|' + a[0]; }, 'Правило маршрутной карты');
  S.cmd('rmap', 'no rule <n>', function (st, a) { delete rm(st).rules[a[0]]; touch(st); });
  S.cmd('rmapr', 'match ip access-group <w>', function (st, a) { rule(st).acl = a[0]; touch(st); }, 'Пакеты, разрешённые этим ACL');
  S.cmd('rmapr', 'no match ip access-group', function (st) { delete rule(st).acl; touch(st); });
  S.cmd('rmapr', 'action set ip next-hop <ip>', function (st, a) { var r = rule(st); r.nh = a[0]; r.act = 'permit'; touch(st); }, 'Отправить на этот next-hop');
  S.cmd('rmapr', 'no action set ip next-hop', function (st) { delete rule(st).nh; touch(st); });
  S.cmd('rmapr', 'action deny', function (st) { rule(st).act = 'deny'; touch(st); }, 'Не применять политику (обычный маршрут)');
  S.cmd('rmapr', 'action permit', function (st) { rule(st).act = 'permit'; touch(st); });
  S.cmd('rmapr', 'enable', function (st) { rule(st).on = true; touch(st); }, 'Включить правило');
  S.cmd('rmapr', 'no enable', function (st) { rule(st).on = false; touch(st); });
  S.cmd('rmapr', 'exit', function (st) { st.mode = 'rmap'; st.ctx = st.ctx.split('|')[0]; });
  S.cmd('rmap', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  S.cmd('gi sub gre vti', 'ip policy route-map <w>', function (st, a) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { st.cand.ifs[k].pbr = a[0]; }); touch(st); }, 'Маршрутизация по политике на входе');
  S.cmd('gi sub gre vti', 'no ip policy route-map', function (st) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { delete st.cand.ifs[k].pbr; }); touch(st); });
  S.RUNX.push(function (c, o) {
    Object.keys(c.rmaps || {}).forEach(function (n) { o.push('route-map ' + n);
      Object.keys(c.rmaps[n].rules).map(Number).sort(function (a, b) { return a - b; }).forEach(function (k) { var r = c.rmaps[n].rules[k]; o.push('  rule ' + k);
        if (r.acl) o.push('    match ip access-group ' + r.acl); if (r.act === 'deny') o.push('    action deny'); if (r.nh) o.push('    action set ip next-hop ' + r.nh);
        if (r.on) o.push('    enable'); o.push('  exit'); }); o.push('exit'); });
    Object.keys(c.ifs).forEach(function (k) { if (c.ifs[k].pbr) o.push((c.ifs[k].tun ? 'tunnel ' + c.ifs[k].tun + ' ' + k.slice(3) : 'interface ' + S.longIf(k)), '  ip policy route-map ' + c.ifs[k].pbr, 'exit'); });
  });
  // поиск маршрута: сначала политика входного интерфейса
  var lookup0 = P.lookup;
  P.lookup = function (id, dst) {
    var cx = this._pkCtx, d = this.devs[id];
    if (cx && cx.dev === id && cx.inIf && d.type === 'esr') {
      var c = d.st.run, x = c.ifs[cx.inIf.name.split(':')[0]], M = x && x.pbr && (c.rmaps || {})[x.pbr];
      if (M) { var ks = Object.keys(M.rules).map(Number).sort(function (a, b) { return a - b; });
        for (var i = 0; i < ks.length; i++) { var r = M.rules[ks[i]]; if (!r.on) continue;
          if (r.acl && !EL.aclPass((c.acls || {})[r.acl], cx.pk).ok) continue;
          if (r.act === 'deny' || !r.nh) break;
          var out = this.ifaces(id).filter(function (f) { return (f.port !== null || f.br || f.tun) && IP.sameNet(r.nh, f.ip, f.len); })[0];
          if (!out) break;            // next-hop недоступен — обычная маршрутизация
          return { iface: out, nh: r.nh, r: { p: 'P', net: dst + '/32' }, pbr: 'политика ' + x.pbr + ' (rule ' + ks[i] + (r.acl ? ', ACL ' + r.acl : '') + ') — пакет ' + cx.pk.src + ' → ' + dst + ' отправлен на next-hop ' + r.nh + ' мимо таблицы маршрутов' }; } }
    }
    return lookup0.apply(this, arguments);
  };
})(typeof window !== 'undefined' ? window : global);
