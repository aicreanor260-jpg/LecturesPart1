/* QinQ на MES 6.x (руководство 6.6.8.8): switchport mode customer, switchport customer vlan N.
   Клиентский порт принимает любой кадр (с тегом или без) и помещает его в S-VLAN N — тег клиента сохраняется внутри (двойной тег);
   по trunk провайдера кадр идёт с внешним тегом N и внутренним тегом клиента, на клиентском порту другой стороны S-тег снимается.
   В захвате на trunk видно VLAN «S/C» и два заголовка 802.1Q. В руководстве 10.4.6 есть только Selective Q-in-Q — для ветки 10 не моделируется. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, CMDS = E.CMDS;
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k]; }).filter(Boolean) : null; }
  function each(st, f) { var p = ports(st); if (!p) return '% Команда доступна в настройке порта'; p.forEach(f); }
  mcmd(['6'], 'if range', 'switchport mode customer', function (st) { return each(st, function (p) { p.mode = 'customer'; if (!p.cvlan) p.cvlan = 1; }); }, 'Клиентский порт QinQ');
  mcmd(['6'], 'if range', 'switchport customer vlan <n>', function (st, a) { if (a[0] < 1 || a[0] > 4094) return '% Invalid input';
    return each(st, function (p) { p.cvlan = a[0]; }); }, 'S-VLAN клиентского порта');
  mcmd(['6'], 'if range', 'no switchport customer vlan', function (st) { return each(st, function (p) { p.cvlan = 1; }); });
  E.PORTX.push(function (st, k, p, d) { if (p.mode === 'customer') { d.push(' switchport mode customer'); if (p.cvlan !== 1) d.push(' switchport customer vlan ' + p.cvlan); } });
})(typeof window !== 'undefined' ? window : global);
