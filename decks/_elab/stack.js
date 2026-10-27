/* Стек MES (руководства 10.4.6 и 6.6.8.8): stack configuration unit-id N; stack configuration links tengigabitethernet 1-2;
   no stack configuration; stack persistent-mac; show stack, show stack configuration, show stack links.
   Настройки стека действуют после перезагрузки. Коммутаторы, соединённые стековыми портами (te) с разными unit-id, собираются в стек:
   стековый линк — внутренняя шина (все VLAN, STP его не блокирует), база VLAN общая — берётся у мастера (меньший unit-id).
   Одинаковые unit-id в одном стеке работать не могут (как в руководстве).
   Упрощение: юниты остаются отдельными устройствами на схеме, порты второго юнита настраиваются с его консоли
   (в настоящем стеке — с мастера, порты gi2/0/N); резервирование мастера и NSF не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, P = EL.Net.prototype, CMDS = E.CMDS;
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function SC(st) { return st.stackCfg || (st.stackCfg = { unit: 1, links: [], pmac: true }); }
  var D = ['10', '6'];
  mcmd(D, 'config', 'stack configuration unit-id <n>', function (st, a) { if (a[0] < 1 || a[0] > 8) return '% Invalid input'; SC(st).unit = a[0];
    return 'Unit ID will be changed after reboot'; }, 'Номер юнита в стеке (после перезагрузки)');
  mcmd(D, 'config', 'stack configuration links tengigabitethernet <w>', function (st, a) {
    var m = String(a[0]).match(/^(\d)(?:-(\d))?$/); if (!m) return '% Invalid input'; var L = [], lo = +m[1], hi = +(m[2] || m[1]);
    for (var i = lo; i <= hi; i++) L.push('te1/0/' + i); if (L.length > 2 || L.some(function (p) { return !st.ports[p]; })) return '% Invalid input';
    SC(st).links = L; }, 'Стековые порты (после перезагрузки)');
  mcmd(D, 'config', 'no stack configuration', function (st) { st.stackCfg = { unit: 1, links: [], pmac: true }; });
  mcmd(D, 'config', 'stack persistent-mac', function (st) { SC(st).pmac = true; }, 'Постоянный MAC стека');
  mcmd(D, 'config', 'no stack persistent-mac', function (st) { SC(st).pmac = false; });
  E.RUNX.push(function (st, o) { var c = st.stackCfg; if (!c) return; if (c.unit !== 1) o.push('stack configuration unit-id ' + c.unit);
    if (c.links.length) o.push('stack configuration links tengigabitethernet ' + c.links.map(function (p) { return p.split('/')[2]; }).join('-'));
    if (!c.pmac) o.push('no stack persistent-mac'); });
  // перезагрузка применяет конфигурацию стека
  var reboot0 = P.reboot;
  P.reboot = function (id) { var d = this.devs[id], cfg = d && d.type === 'mes' && d.st.stackCfg ? EL.clone(d.st.stackCfg) : null;
    var r = reboot0.apply(this, arguments); if (d && d.type === 'mes') { if (cfg) d.st.stackCfg = cfg; d.st.stackBoot = cfg ? EL.clone(cfg) : null; } this.gen++; return r; };
  // сборка стека: стековые порты, соединённые со стековыми портами юнита с другим unit-id
  P.stackSync = function () {
    if (this._stk && this._stk.gen === this.gen) return this._stk.t;
    var s = this, mem = {}, links = [], pairs = {};   // pairs: один активный линк на пару юнитов, остальные — резерв
    s.order.forEach(function (id) { var d = s.devs[id]; if (d.type !== 'mes') return;
      Object.keys(d.st.ports).forEach(function (k) { if (d.st.ports[k].stackLink) delete d.st.ports[k].stackLink; }); });
    s.order.forEach(function (id) { var d = s.devs[id], b = d.type === 'mes' && !d.off && d.st.stackBoot; if (!b) return;
      b.links.forEach(function (p) { var pr = s.peer(id, p); if (!pr) return; var nd = s.devs[pr.dev], nb = nd.type === 'mes' && !nd.off && nd.st.stackBoot;
        if (!nb || nb.links.indexOf(pr.port) < 0 || nb.unit === b.unit || d.st.ports[p].shut) return;
        var pk = [id, pr.dev].sort().join('|'), act = !pairs[pk] || pairs[pk] === id + '|' + p || pairs[pk] === pr.dev + '|' + pr.port;
        if (!pairs[pk]) pairs[pk] = id + '|' + p;
        d.st.ports[p].stackLink = act ? 'active' : 'standby'; if (act) links.push([id, p, pr.dev, pr.port]); mem[id] = true; mem[pr.dev] = true; }); });
    // компоненты стека и мастер (меньший unit-id); база VLAN — мастера
    var seen = {}, t = {};
    Object.keys(mem).forEach(function (id) { if (seen[id]) return; var comp = [], q = [id]; seen[id] = true;
      while (q.length) { var u = q.shift(); comp.push(u); links.forEach(function (l) { [[l[0], l[2]], [l[2], l[0]]].forEach(function (e) { if (e[0] === u && !seen[e[1]]) { seen[e[1]] = true; q.push(e[1]); } }); }); }
      comp.sort(function (a, b) { return s.devs[a].st.stackBoot.unit - s.devs[b].st.stackBoot.unit; });
      var master = comp[0];
      comp.forEach(function (u) { t[u] = { master: master, units: comp }; if (u !== master) s.devs[u].st.vlans = EL.clone(s.devs[master].st.vlans); }); });
    this._stk = { gen: this.gen, t: t, links: links };
    return t;
  };
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function showStack(st) { var s = st.net; if (!s) return ''; var t = s.stackSync()[st.dev], b = st.stackBoot || { unit: 1 };
    var units = t ? t.units : [st.dev];
    return ['Unit Id   MAC address         Role      Model', '-------   -----------------   -------   ----------------'].concat(units.map(function (u) { var d = s.devs[u], ub = (d.st.stackBoot || { unit: 1 }).unit;
      return rp(ub, 10) + rp(d.st.bmac, 20) + rp(t ? (t.master === u ? 'master' : 'slave') : 'master', 10) + d.model; })).concat(t ? [] : ['', 'Stack is not formed (unit ' + b.unit + ' standalone)']).join('\n'); }
  ['', 'do '].forEach(function (pre) { var m = pre ? E.CFG : 'priv';
    mcmd(D, m, pre + 'show stack', showStack, 'Юниты стека');
    mcmd(D, m, pre + 'show stack configuration', function (st) { var c = st.stackCfg || { unit: 1, links: [] }, b = st.stackBoot || { unit: 1, links: [] };
      return ['Unit Id   Configured links          Active after reboot', '-------   -----------------------   ----------------------',
        rp(c.unit + (c.unit !== b.unit ? ' (' + b.unit + ' now)' : ''), 10) + rp(c.links.join(', ') || '--', 26) + (b.links.join(', ') || '--')].join('\n'); }, 'Конфигурация стека');
    mcmd(D, m, pre + 'show stack links', function (st) { var s = st.net; if (!s) return ''; s.stackSync(); var L = (s._stk.links || []).filter(function (l) { return l[0] === st.dev; });
      return ['Unit Id     Active Links        Neighbor Links    Operational', '                                                  Link Speed', '-------- -------------------- -------------------- -----------']
        .concat(L.map(function (l) { return rp((st.stackBoot || {}).unit || 1, 9) + rp(l[1], 21) + rp(l[3].replace('1/0', (s.devs[l[2]].st.stackBoot || {}).unit + '/0'), 21) + '10G'; })).join('\n'); }, 'Стековые линки'); });
})(typeof window !== 'undefined' ? window : global);
