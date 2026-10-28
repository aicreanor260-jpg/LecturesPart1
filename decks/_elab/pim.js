/* Многоадресная маршрутизация PIM-SM на MES 6.x (руководство 6.6.8.8, раздел 5.18: пример «PIM SM со статическим RP»).
   config: ip multicast-routing [pim] · ip pim rp-address A [ГРУППА/ДЛИНА] ; interface vlan N: ip pim (включён по умолчанию), no ip pim, ip pim dr-priority N,
   ip igmp static-group G. Показ: show ip pim neighbor, show ip pim interface, show ip pim rp mapping.
   Как работает: узлы вступают в группу IGMP-отчётом (Debian: ip addr add 239.1.1.1/32 dev ens3 autojoin) — маршрутизатор с PIM на SVI этой VLAN
   знает получателей; источник (Debian: ping 239.1.1.1) шлёт поток — первый маршрутизатор в его VLAN регистрирует его на RP (unicast),
   маршрутизаторы получателей присоединяются к дереву (*,G) к RP по обратному пути (RPF) через PIM-соседей; поток доставляется в VLAN получателей
   (с IGMP snooping — только в порты участников). ESR в справочнике 1.23 PIM не имеет; у MES 10.x в шаблонах прошивки — только set ip pim, без RP.
   Упрощения: только статический RP (без BSR и кандидатов), переход на дерево источника (SPT) и DR-выборы не моделируются, таймеры PIM нет;
   форматы show — условные (в руководстве нет примеров). */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, P = EL.Net.prototype, CMDS = E.CMDS, H = EL.hosts, IP = EL.ip;
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function PM(st) { return st.pim || (st.pim = { on: false, rp: [], off: {}, dr: {}, sg: {} }); }
  var D = ['6'];
  mcmd(D, 'config', 'ip multicast-routing', function (st) { PM(st).on = true; }, 'Многоадресная маршрутизация (PIM)');
  mcmd(D, 'config', 'ip multicast-routing pim', function (st) { PM(st).on = true; });
  mcmd(D, 'config', 'no ip multicast-routing', function (st) { PM(st).on = false; });
  mcmd(D, 'config', 'no ip multicast-routing pim', function (st) { PM(st).on = false; });
  mcmd(D, 'config', 'ip pim rp-address <ip>', function (st, a) { var L = PM(st).rp.filter(function (r) { return !(r.ip === a[0] && !r.grp); }); L.push({ ip: a[0], grp: null }); PM(st).rp = L; }, 'Статический RP');
  mcmd(D, 'config', 'ip pim rp-address <ip> <w>', function (st, a) { var c = IP.parseCidr(a[1]); if (!c || (IP.ip2n(c.ip) >>> 28) !== 14) return '% Invalid input';
    var g = IP.netOf(c.ip, c.len); PM(st).rp = PM(st).rp.filter(function (r) { return !(r.ip === a[0] && r.grp === g); }).concat([{ ip: a[0], grp: g }]); });
  mcmd(D, 'config', 'no ip pim rp-address <ip>', function (st, a) { PM(st).rp = PM(st).rp.filter(function (r) { return r.ip !== a[0]; }); });
  function svi(st) { return st.ctx && st.ctx.svi; }
  mcmd(D, 'if', 'ip pim', function (st) { if (!svi(st)) return '% Команда доступна на интерфейсе VLAN'; delete PM(st).off[svi(st)]; }, 'PIM на интерфейсе (включён по умолчанию)');
  mcmd(D, 'if', 'no ip pim', function (st) { if (!svi(st)) return '% Команда доступна на интерфейсе VLAN'; PM(st).off[svi(st)] = true; });
  mcmd(D, 'if', 'ip pim dr-priority <n>', function (st, a) { if (!svi(st)) return '% Команда доступна на интерфейсе VLAN'; PM(st).dr[svi(st)] = a[0]; }, 'Приоритет DR');
  mcmd(D, 'if', 'ip igmp static-group <ip>', function (st, a) { if (!svi(st)) return '% Команда доступна на интерфейсе VLAN'; var L = PM(st).sg[svi(st)] = PM(st).sg[svi(st)] || [];
    if (L.indexOf(a[0]) < 0) L.push(a[0]); }, 'Статическое членство в группе');
  mcmd(D, 'if', 'no ip igmp static-group <ip>', function (st, a) { var v = svi(st); if (v && PM(st).sg[v]) PM(st).sg[v] = PM(st).sg[v].filter(function (x) { return x !== a[0]; }); });
  E.RUNX.push(function (st, o) { var p = st.pim; if (!p) return; if (p.on) o.push('ip multicast-routing pim'); p.rp.forEach(function (r) { o.push('ip pim rp-address ' + r.ip + (r.grp ? ' ' + r.grp : '')); });
    Object.keys(st.svi).forEach(function (v) { var L = []; if (p.off[v]) L.push(' no ip pim'); if (p.dr[v]) L.push(' ip pim dr-priority ' + p.dr[v]); (p.sg[v] || []).forEach(function (g) { L.push(' ip igmp static-group ' + g); });
      if (L.length) o.push('interface vlan ' + v, L.join('\n'), 'exit'); }); });

  // ---------------------------------------------------------------- модель
  function pimDev(d) { return d && !d.off && d.type === 'mes' && d.st.pim && d.st.pim.on; }
  function sviOf(s, id, name) { var m = String(name).match(/^vlan(\d+)$/); return m ? +m[1] : null; }
  function pimIf(s, id, ifn) { var d = s.devs[id], v = sviOf(s, id, ifn); return pimDev(d) && v !== null && !d.st.pim.off[v]; }
  function rpFor(st, g) { var best = null; (st.pim ? st.pim.rp : []).forEach(function (r) { var q = r.grp ? r.grp.split('/') : ['224.0.0.0', 4];
    if (IP.sameNet(g, q[0], +q[1]) && (!best || +q[1] > best.len)) best = { ip: r.ip, len: +q[1] }; }); return best ? best.ip : null; }
  P.pimNbrs = function (id) {                     // соседи: маршрутизаторы с PIM в той же сети SVI
    var s = this, out = [];
    s.ifaces(id).forEach(function (f) { if (!pimIf(s, id, f.name)) return;
      s.flood(id, f).eps.forEach(function (ep) { if (ep.dev === id || !pimIf(s, ep.dev, ep.iface.name) || !IP.sameNet(ep.iface.ip, f.ip, f.len)) return;
        out.push({ dev: ep.dev, ip: ep.iface.ip, ifn: f.name, nifn: ep.iface.name }); }); });
    return out;
  };
  // путь по RPF от маршрутизатора к RP через PIM-соседей: [устройства] или {why}
  function rpf(s, id, rp) { var path = [id], cur = id;
    for (var i = 0; i < 16; i++) { if (s.ifaces(cur).some(function (f) { return f.ip === rp; })) return { path: path };
      var r = s.lookup(cur, rp); if (!r) return { why: s.devs[cur].name + ': нет маршрута до RP ' + rp };
      if (!pimIf(s, cur, r.iface.name)) return { why: s.devs[cur].name + ': на ' + r.iface.name + ' (к RP) PIM выключен' };
      var nb = s.pimNbrs(cur).filter(function (x) { return x.ip === r.nh; })[0]; if (!nb) return { why: s.devs[cur].name + ': next-hop ' + r.nh + ' к RP — не PIM-сосед' };
      cur = nb.dev; path.push(cur); }
    return { why: 'путь до RP слишком длинный' };
  }
  function receivers(s, id, g) {                 // VLAN маршрутизатора, где есть участники группы (IGMP или static-group)
    var d = s.devs[id], out = [];
    s.ifaces(id).forEach(function (f) { var v = sviOf(s, id, f.name); if (v === null || !pimIf(s, id, f.name)) return;
      var st0 = (d.st.pim.sg[v] || []).indexOf(g) >= 0;
      var hosts = s.flood(id, f).eps.filter(function (ep) { var h = s.devs[ep.dev]; return h.type === 'deb' && (h.st.mgroups || []).indexOf(g) >= 0; });
      if (st0 || hosts.length) out.push({ f: f, v: v }); });
    return out;
  }
  var send0 = P.mcastSend;
  P.mcastSend = function (id, group) {
    var r = send0.apply(this, arguments), s = this, steps = r.steps, src = s.devs[id], f = { name: 'ens3', port: src.st.port || 'ens3', tag: null, ip: src.st.ip };
    var fhr = s.flood(id, f).eps.filter(function (ep) { return pimIf(s, ep.dev, ep.iface.name) && src.st.ip && IP.sameNet(src.st.ip, ep.iface.ip, ep.iface.len); })[0];
    if (!fhr) return r;
    var F = s.devs[fhr.dev], rp = rpFor(F.st, group);
    if (!rp) { steps.push({ k: 'drop', t: 'PIM: на ' + F.name + ' нет RP для группы ' + group + ' (ip pim rp-address)' }); return r; }
    if (!s.ifaces(fhr.dev).some(function (x) { return x.ip === rp; }) && !s.lookup(fhr.dev, rp)) { steps.push({ k: 'drop', t: 'PIM: ' + F.name + ' не может зарегистрировать источник — нет маршрута до RP ' + rp }); return r; }
    steps.push({ k: 'route', t: 'PIM: ' + F.name + ' — первый маршрутизатор источника ' + src.st.ip + ', Register на RP ' + rp + ' (поток (' + src.st.ip + ', ' + group + '))' });
    var got = r.got.slice(), seen = {};
    s.order.forEach(function (rid) { if (!pimDev(s.devs[rid])) return; var R = s.devs[rid];
      receivers(s, rid, group).forEach(function (x) { if (rid === fhr.dev && x.v === sviOf(s, rid, fhr.iface.name)) return;
        if (rpFor(R.st, group) !== rp) { steps.push({ k: 'drop', t: 'PIM: ' + R.name + ' — RP для ' + group + ' другой или не задан (у первого маршрутизатора ' + rp + ')' }); return; }
        var a = rpf(s, rid, rp), b = rpf(s, fhr.dev, rp);
        if (a.why || b.why) { steps.push({ k: 'drop', t: 'PIM: ' + R.name + ' не присоединился к дереву: ' + (a.why || b.why) }); return; }
        s._mc = group; var fl; try { fl = s.flood(rid, x.f, s.ifMac(rid, x.f)); } finally { s._mc = null; }
        var hs = fl.eps.filter(function (e) { var h = s.devs[e.dev]; return h.type === 'deb' && (h.st.mgroups || []).indexOf(group) >= 0; }).map(function (e) { return s.devs[e.dev].name; });
        hs.forEach(function (h) { if (got.indexOf(h) < 0 && !seen[h]) { seen[h] = 1; got.push(h); } });
        steps.push({ k: 'ok', segs: fl.segs, t: 'PIM: ' + R.name + ' (*,' + group + ') — дерево к RP: ' + a.path.map(function (q) { return s.devs[q].name; }).join(' → ') + '; поток в VLAN ' + x.v + ': ' + (hs.join(', ') || 'участников за snooping нет') }); }); });
    return { ok: got.length > 0, steps: steps, got: got, all: r.all };
  };
  // ---------------------------------------------------------------- show
  function pad(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  ['', 'do '].forEach(function (pre) { var m = pre ? E.CFG : 'priv';
    mcmd(D, m, pre + 'show ip pim neighbor', function (st) { var s = st.net; if (!s) return ''; var L = s.pimNbrs(st.dev);
      return [pad('Neighbor Address', 18) + pad('Interface', 12) + 'DR Priority'].concat(L.map(function (x) { var d = s.devs[x.dev], v = sviOf(s, x.dev, x.nifn);
        return pad(x.ip, 18) + pad(x.ifn, 12) + ((d.st.pim.dr || {})[v] || 1); })).join('\n'); }, 'PIM-соседи');
    mcmd(D, m, pre + 'show ip pim interface', function (st) { var s = st.net, p = st.pim || { off: {} };
      return [pad('Interface', 12) + pad('Address', 18) + pad('PIM', 6) + 'Neighbors'].concat(Object.keys(st.svi).map(function (v) { var on = p.on && !p.off[v];
        return pad('vlan ' + v, 12) + pad(st.svi[v].split('/')[0], 18) + pad(on ? 'on' : 'off', 6) + (s && on ? s.pimNbrs(st.dev).filter(function (x) { return x.ifn === 'vlan' + v; }).length : 0); })).join('\n'); }, 'Интерфейсы PIM');
    mcmd(D, m, pre + 'show ip pim rp mapping', function (st) { var p = st.pim; if (!p || !p.rp.length) return '% RP не задан';
      return p.rp.map(function (r) { return 'Group(s): ' + (r.grp || '224.0.0.0/4') + '\n  RP: ' + r.ip + ', static'; }).join('\n'); }, 'RP для групп'); });
  void H;
})(typeof window !== 'undefined' ? window : global);
