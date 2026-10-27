/* MSTP-экземпляры на MES (руководства 10.4.6 и 6.6.8.8, режим spanning-tree mode mst):
   spanning-tree mst configuration → (config-mst)#: instance N vlan СПИСОК, name, revision;
   spanning-tree mst N priority P (кратно 4096); на порту spanning-tree mst N cost C; show spanning-tree mst N.
   У каждого экземпляра своё дерево: свой корень по приоритету экземпляра и своя стоимость портов — разные VLAN могут
   блокироваться на разных портах (балансировка). VLAN без экземпляра идут по CIST (экземпляр 0, обычные настройки STP).
   Упрощение: совпадение имени/ревизии/привязок региона не проверяется — все коммутаторы считаются одним регионом. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, P = EL.Net.prototype, CMDS = E.CMDS;
  E.PROMPT.mst = '(config-mst)#';
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k] || (st.pos || {})[k]; }).filter(Boolean) : null; }
  function each(st, f) { var p = ports(st); if (!p) return '% Команда доступна в настройке порта'; p.forEach(f); }
  function M(st) { return st.mst || (st.mst = { inst: {}, name: null, rev: 0 }); }
  function inst(st, k) { var m = M(st); return m.inst[k] || (m.inst[k] = { vlans: [] }); }
  var D = ['10', '6'];
  mcmd(D, 'config', 'spanning-tree mst configuration', function (st) { M(st); st.mode = 'mst'; st.ctx = null; }, 'Настройка MSTP: экземпляры и VLAN');
  mcmd(D, 'mst', 'instance <n> vlan <list>', function (st, a) { if (a[0] < 1 || a[0] > 63) return '% Invalid input';
    var m = M(st); Object.keys(m.inst).forEach(function (k) { m.inst[k].vlans = m.inst[k].vlans.filter(function (v) { return a[1].indexOf(v) < 0; }); });
    var I = inst(st, a[0]); a[1].forEach(function (v) { if (I.vlans.indexOf(v) < 0) I.vlans.push(v); }); I.vlans.sort(function (x, y) { return x - y; }); }, 'Привязать VLAN к экземпляру');
  mcmd(D, 'mst', 'no instance <n> vlan <list>', function (st, a) { var I = M(st).inst[a[0]]; if (I) I.vlans = I.vlans.filter(function (v) { return a[1].indexOf(v) < 0; }); });
  mcmd(D, 'mst', 'name <w>', function (st, a) { M(st).name = a[0]; }, 'Имя конфигурации MST');
  mcmd(D, 'mst', 'no name', function (st) { M(st).name = null; });
  mcmd(D, 'mst', 'revision <n>', function (st, a) { if (a[0] > 65535) return '% Invalid input'; M(st).rev = a[0]; }, 'Номер ревизии');
  mcmd(D, 'mst', 'no revision', function (st) { M(st).rev = 0; });
  mcmd(D, 'mst', 'exit', function (st) { st.mode = 'config'; });
  mcmd(D, 'mst', 'end', function (st) { st.mode = 'priv'; });
  mcmd(D, 'config', 'spanning-tree mst <n> priority <n>', function (st, a) { if (a[0] < 1 || a[0] > 63 || a[1] > 61440 || a[1] % 4096) return '% Приоритет 0–61440, кратный 4096';
    inst(st, a[0]).prio = a[1]; }, 'Приоритет моста в экземпляре');
  mcmd(D, 'config', 'no spanning-tree mst <n> priority', function (st, a) { var I = M(st).inst[a[0]]; if (I) delete I.prio; });
  mcmd(D, 'if range', 'spanning-tree mst <n> cost <n>', function (st, a) { if (a[0] < 1 || a[0] > 63 || a[1] < 1 || a[1] > 200000000) return '% Invalid input';
    return each(st, function (p) { (p.mstCost = p.mstCost || {})[a[0]] = a[1]; }); }, 'Стоимость порта в экземпляре');
  mcmd(D, 'if range', 'no spanning-tree mst <n> cost', function (st, a) { return each(st, function (p) { if (p.mstCost) delete p.mstCost[a[0]]; }); });
  mcmd(D, 'if range', 'spanning-tree mst <n> port-priority <n>', function (st, a) { if (a[1] > 240 || a[1] % 16) return '% Приоритет 0–240, кратный 16';
    return each(st, function (p) { (p.mstPrio = p.mstPrio || {})[a[0]] = a[1]; }); }, 'Приоритет порта в экземпляре');
  E.RUNX.push(function (st, o) { var m = st.mst; if (!m) return;
    var ks = Object.keys(m.inst).filter(function (k) { return m.inst[k].vlans.length; });
    if (ks.length || m.name || m.rev) { o.push('spanning-tree mst configuration'); ks.forEach(function (k) { o.push(' instance ' + k + ' vlan ' + E.fmtList(m.inst[k].vlans)); });
      if (m.name) o.push(' name ' + m.name); if (m.rev) o.push(' revision ' + m.rev); o.push('exit'); }
    Object.keys(m.inst).forEach(function (k) { if (m.inst[k].prio !== undefined) o.push('spanning-tree mst ' + k + ' priority ' + m.inst[k].prio); }); });
  E.PORTX.push(function (st, k, p, d) { Object.keys(p.mstCost || {}).forEach(function (i) { d.push(' spanning-tree mst ' + i + ' cost ' + p.mstCost[i]); });
    Object.keys(p.mstPrio || {}).forEach(function (i) { d.push(' spanning-tree mst ' + i + ' port-priority ' + p.mstPrio[i]); }); });

  // show spanning-tree mst N
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  P.mstText = function (id, k) {
    var d = this.devs[id], st = d.st, m = st.mst || { inst: {} }, I = m.inst[k];
    if ((st.stp || {}).mode !== 'mst') return '% Режим STP не MSTP (spanning-tree mode mst)';
    if (!I || !I.vlans.length) return '% Экземпляр ' + k + ' не создан (spanning-tree mst configuration → instance ' + k + ' vlan …)';
    var t = this.stp(k)[id] || {}, R = this._stpK[k].root[id], rd = this.devs[R].st, rb = (rd.mst && rd.mst.inst[k] && rd.mst.inst[k].prio !== undefined) ? rd.mst.inst[k].prio : (rd.stp || {}).prio;
    var me = I.prio !== undefined ? I.prio : (st.stp || {}).prio, s = this;
    var o = ['###### MST ' + k + ' Vlans Mapped: ' + E.fmtList(I.vlans), 'CST Root ID      Priority    ' + rb, '                 Address     ' + rd.bmac];
    o.push(R === id ? '                 This switch is root for this instance' : '                 Cost        ' + this._stpK[k].dist[id]);
    o.push('Bridge ID        Priority    ' + me, '                 Address     ' + st.bmac, '', 'Interfaces', ' Name       State   Prio.Nbr  Cost      Sts   Role   Type', ' ---------- ------- --------- --------- ----- ------ ----------');
    this.lports(id).forEach(function (L) { var r = t[L.name]; if (!r) return;
      var c = (L.cfg.mstCost && L.cfg.mstCost[k]) || L.cfg.stpCost || (L.name.indexOf('po') === 0 ? 10000 : 20000), pr = (L.cfg.mstPrio && L.cfg.mstPrio[k]) || 128;
      o.push(' ' + rp(L.name, 11) + 'enabled ' + rp(pr + '.' + L.name.split('/').pop(), 10) + rp(c, 10) + (r.fwd ? 'Frw   ' : 'Dsc   ') + rp(r.role, 7) + 'P2p'); });
    void s; return o.join('\n');
  };
  ['', 'do '].forEach(function (pre) { mcmd(D, pre ? E.CFG : 'priv', pre + 'show spanning-tree mst <n>', function (st, a) { return st.net ? st.net.mstText(st.dev, a[0]) : ''; }, 'Состояние экземпляра MSTP');
    mcmd(D, pre ? E.CFG : 'priv', pre + 'show spanning-tree mst configuration', function (st) { var m = st.mst || { inst: {} };
      return ['Name      ' + (m.name || ''), 'Revision  ' + (m.rev || 0), 'Instance  Vlans mapped', '--------  ------------------'].concat(
        Object.keys(m.inst).filter(function (k) { return m.inst[k].vlans.length; }).map(function (k) { return rp(k, 10) + E.fmtList(m.inst[k].vlans); })).join('\n'); }, 'Конфигурация MSTP'); });
})(typeof window !== 'undefined' ? window : global);
