/* MES для лаб 8.1 и 8.2: связующее дерево (spanning-tree, RSTP) и агрегация каналов (port-channel, LACP).
   Синтаксис — по руководству MES14xx/24xx/3400/37xx, ПО 10.4.6. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, cmd = E.cmd, CFG = E.CFG;
  function stp(st) { return st.stp || (st.stp = { on: true, mode: 'mst', prio: 32768 }); }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k] || st.pos[k]; }) : null; }

  // ---------------------------------------------------------------- STP
  cmd('config', 'spanning-tree', function (st) { stp(st).on = true; });
  cmd('config', 'no spanning-tree', function (st) { stp(st).on = false; });
  cmd('config', 'spanning-tree mode <w>', function (st, a) { var m = a[0].toLowerCase();
    if (['rst', 'mst', 'rapid-pvst'].indexOf(m) < 0) return '% Режим: rst | mst | rapid-pvst'; stp(st).mode = m; });
  cmd('config', 'spanning-tree priority <n>', function (st, a) {
    if (a[0] > 61440 || a[0] % 4096) return '% Приоритет 0–61440, кратный 4096'; stp(st).prio = a[0]; });
  cmd('config', 'no spanning-tree priority', function (st) { stp(st).prio = 32768; });
  cmd('if range', 'spanning-tree cost <n>', function (st, a) { var p = ports(st); if (!p) return '% Команда для порта';
    p.forEach(function (x) { x.stpCost = a[0]; }); });
  cmd('if range', 'no spanning-tree cost', function (st) { var p = ports(st); if (p) p.forEach(function (x) { delete x.stpCost; }); });
  cmd('if range', 'spanning-tree disable', function (st) { var p = ports(st); if (p) p.forEach(function (x) { x.stpOff = true; }); });

  // ---------------------------------------------------------------- port-channel / LACP
  function poFresh() { return { mode: 'access', access: 1, allowed: [], native: 1, pvid: 1, gtag: [], guntag: [1], shut: false }; }
  cmd('config', 'interface port-channel <n>', function (st, a) {
    if (a[0] < 1 || a[0] > 64) return '% Номер группы 1–64';
    st.pos = st.pos || {}; if (!st.pos['po' + a[0]]) st.pos['po' + a[0]] = poFresh();
    st.mode = 'if'; st.ctx = { ports: ['po' + a[0]] }; });
  cmd('config', 'no interface port-channel <n>', function (st, a) { if (st.pos) delete st.pos['po' + a[0]];
    Object.keys(st.ports).forEach(function (k) { var p = st.ports[k]; if (p.cg && p.cg.id === a[0]) delete p.cg; }); });
  cmd('if range', 'channel-group <n> mode <w>', function (st, a) {
    var m = a[1].toLowerCase(); if (['on', 'active', 'passive'].indexOf(m) < 0) return '% Режим: on | active | passive';
    if (!st.ctx || !st.ctx.ports || st.ctx.ports.some(function (k) { return !st.ports[k]; })) return '% Команда для физического порта';
    st.pos = st.pos || {}; if (!st.pos['po' + a[0]]) st.pos['po' + a[0]] = poFresh();
    st.ctx.ports.forEach(function (k) { st.ports[k].cg = { id: a[0], mode: m }; }); });
  cmd('if range', 'no channel-group', function (st) { if (st.ctx && st.ctx.ports) st.ctx.ports.forEach(function (k) { if (st.ports[k]) delete st.ports[k].cg; }); });

  function shows(prefix, modes) {
    cmd(modes, prefix + 'show spanning-tree', function (st) { return st.net ? st.net.stpText(st.dev) : ''; });
    cmd(modes, prefix + 'show spanning-tree active', function (st) { return st.net ? st.net.stpText(st.dev) : ''; });
    cmd(modes, prefix + 'show etherchannel summary', function (st) { return st.net ? st.net.lagText(st.dev) : ''; });
    cmd(modes, prefix + 'show lacp <n>', function (st) { return st.net ? st.net.lagText(st.dev) : ''; });
  }
  shows('', 'priv'); shows('do ', CFG);
})(typeof window !== 'undefined' ? window : global);
