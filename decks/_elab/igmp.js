/* IGMP snooping на MES (руководства 10.4.6 и 6.6.8.8): ip igmp snooping; ip igmp snooping vlan N;
   порт к маршрутизатору мультикаста: 10.x — ip igmp snooping vlan N mrouter gigabitethernet 1/0/24, 6.x — … mrouter interface gigabitethernet 1/0/24;
   show ip igmp snooping groups, show ip igmp snooping mrouter.
   Узел вступает в группу — Debian: ip addr add 239.1.1.1/32 dev ens3 autojoin (отправляет IGMP Report, коммутатор запоминает порт);
   ip addr del 239.1.1.1/32 dev ens3 — выход (IGMP Leave). Групповой трафик — Debian: ping 239.1.1.1.
   Без snooping групповой кадр рассылается во все порты VLAN (как широковещательный); со snooping — только в порты участников группы и mrouter.
   Упрощения: querier и таймеры членства не моделируются; ответов на групповой ping нет (как у Linux по умолчанию, icmp_echo_ignore_broadcasts). */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, P = EL.Net.prototype, CMDS = E.CMDS, H = EL.hosts, IP = EL.ip;
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function G2(st) { return st.igmp || (st.igmp = { on: false, vl: [], mr: {}, grp: {} }); }
  var D = ['10', '6'];
  mcmd(D, 'config', 'ip igmp snooping', function (st) { G2(st).on = true; }, 'Включить IGMP snooping');
  mcmd(D, 'config', 'no ip igmp snooping', function (st) { G2(st).on = false; });
  mcmd(D, 'config', 'ip igmp snooping vlan <n>', function (st, a) { var g = G2(st); if (g.vl.indexOf(a[0]) < 0) g.vl.push(a[0]); }, 'IGMP snooping в VLAN');
  mcmd(D, 'config', 'no ip igmp snooping vlan <n>', function (st, a) { var g = G2(st); g.vl = g.vl.filter(function (v) { return v !== a[0]; }); });
  function mr(st, v, L) { var g = G2(st); g.mr[v] = (g.mr[v] || []).concat(L).filter(function (x, i, A) { return A.indexOf(x) === i; }); }
  mcmd(['10'], 'config', 'ip igmp snooping vlan <n> mrouter <if>', function (st, a) { mr(st, a[0], a[1]); }, 'Порт к маршрутизатору мультикаста');
  mcmd(['6'], 'config', 'ip igmp snooping vlan <n> mrouter interface <if>', function (st, a) { mr(st, a[0], a[1]); }, 'Порт к маршрутизатору мультикаста');
  E.RUNX.push(function (st, o) { var g = st.igmp; if (!g) return; if (g.on) o.push('ip igmp snooping');
    g.vl.forEach(function (v) { o.push('ip igmp snooping vlan ' + v); (g.mr[v] || []).forEach(function (p) { o.push('ip igmp snooping vlan ' + v + ' mrouter ' + (st.dialect === '6' ? 'interface ' : '') + E.longIf(p)); }); }); });
  function on(st, v) { var g = st.igmp; return !!g && g.on && g.vl.indexOf(v) >= 0; }
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  ['', 'do '].forEach(function (pre) { var m = pre ? E.CFG : 'priv';
    mcmd(D, m, pre + 'show ip igmp snooping groups', function (st) { var g = G2(st), o = ['Vlan   Group Address    Ports', '----   --------------   ------------------------'];
      Object.keys(g.grp).forEach(function (k) { var q = k.split('|'); if (!on(st, +q[0])) return; o.push(rp(q[0], 7) + rp(q[1], 17) + g.grp[k].join(', ')); }); return o.join('\n'); }, 'Группы IGMP snooping');
    mcmd(D, m, pre + 'show ip igmp snooping mrouter', function (st) { var g = G2(st);
      return ['Vlan   Ports', '----   ------------------------'].concat(Object.keys(g.mr).map(function (v) { return rp(v, 7) + g.mr[v].join(', '); })).join('\n'); }, 'Порты mrouter'); });

  // ---------------------------------------------------------------- модель: отчёт IGMP и групповая рассылка
  var macIn0 = P.macIn;
  P.macIn = function (dev, port, v, mac) {
    var j = this._igmp, d = this.devs[dev];
    if (j && d && d.type === 'mes' && on(d.st, v)) { var g = G2(d.st), k = v + '|' + j.group, L = g.grp[k] || [];
      if (j.join) { if (L.indexOf(port) < 0) L = L.concat([port]); } else L = L.filter(function (x) { return x !== port; });
      if (L.length) g.grp[k] = L; else delete g.grp[k]; }
    return macIn0.apply(this, arguments);
  };
  P.mcBlock = function (dev, v, lname) {
    var m = this._mc, d = this.devs[dev]; if (!m || !d || d.type !== 'mes' || !on(d.st, v)) return false;
    var g = G2(d.st); return (g.grp[v + '|' + m] || []).indexOf(lname) < 0 && (g.mr[v] || []).indexOf(lname) < 0;
  };
  function mmac(g) { var n = IP.ip2n(g) & 0x7fffff, p = function (x) { return ('0' + x.toString(16)).slice(-2); }; return '01:00:5e:' + p(n >> 16) + ':' + p((n >> 8) & 255) + ':' + p(n & 255); }
  function hostIf(s, id) { var d = s.devs[id]; return d.type === 'vpc' ? { name: 'eth0', port: 'eth0', tag: null, ip: d.st.ip } : { name: 'ens3', port: 'ens3', tag: null, ip: d.st.ip }; }
  P.igmpReport = function (id, group, join) {
    var s = this, f = hostIf(s, id), steps = s.stepLog();
    s._igmp = { group: group, join: join }; var fl; try { fl = s.flood(id, f, EL.mac(s.devs[id].name + f.port)); } finally { s._igmp = null; }
    steps.push({ k: 'arp', segs: fl.segs, t: s.devs[id].name + ': IGMP ' + (join ? 'Membership Report' : 'Leave Group') + ' ' + group + ' — коммутаторы со snooping запомнили порт',
      f: { type: 'ip', mcast: true, smac: EL.mac(s.devs[id].name + f.port), dmac: mmac(join ? group : '224.0.0.2'), src: f.ip || '0.0.0.0', dst: join ? group : '224.0.0.2', proto: 'igmp', ttl: 1 } });
    if (s.countSteps) s.countSteps(steps, 'udp');
    return steps;
  };
  P.mcastSend = function (id, group) {
    var s = this, f = hostIf(s, id), steps = s.stepLog(), mac = EL.mac(s.devs[id].name + f.port);
    s._mc = group; var fl; try { fl = s.flood(id, f, mac); } finally { s._mc = null; }
    var got = fl.eps.filter(function (e) { var h = s.devs[e.dev]; return h.type === 'deb' && (h.st.mgroups || []).indexOf(group) >= 0; }).map(function (e) { return s.devs[e.dev].name; });
    var all = fl.eps.map(function (e) { return s.devs[e.dev].name; }).filter(function (x, i, A) { return A.indexOf(x) === i; });
    steps.push({ k: 'arp', segs: fl.segs, notes: fl.notes, t: s.devs[id].name + ': групповой кадр ICMP → ' + group + ' (MAC ' + mmac(group) + '). Кадр дошёл до: ' + (all.join(', ') || 'никого') +
      '; участники группы: ' + (got.join(', ') || 'нет'), f: { type: 'ip', mcast: true, smac: mac, dmac: mmac(group), src: f.ip, dst: group, proto: 'icmp', ttl: 1 } });
    if (s.countSteps) s.countSteps(steps, 'icmp');
    return { ok: got.length > 0, steps: steps, got: got, all: all };
  };
  // ---------------------------------------------------------------- Debian
  var deb0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    var line = String(raw).trim();
    if (!st.user || st.ssh || !st.net) return deb0.apply(this, arguments);
    var m = line.match(/^ip\s+(?:address|addr|a)\s+(add|del)\s+(\d+\.\d+\.\d+\.\d+)\/32\s+dev\s+ens3(\s+autojoin)?$/);
    if (m && IP.ip2n(m[2]) !== null && (IP.ip2n(m[2]) >>> 28) === 14) {
      if (st.user !== 'root') return 'RTNETLINK answers: Operation not permitted';
      var L = st.mgroups || [];
      if (m[1] === 'add') { if (L.indexOf(m[2]) >= 0) return 'RTNETLINK answers: File exists'; st.mgroups = L.concat([m[2]]); if (m[3]) st.net.igmpReport(st.dev, m[2], true); }
      else { st.mgroups = L.filter(function (x) { return x !== m[2]; }); st.net.igmpReport(st.dev, m[2], false); }
      st.net.gen++; return ''; }
    var p = line.match(/^ping\s+(?:-c\s*\d+\s+)?(\d+\.\d+\.\d+\.\d+)$/);
    if (p && (IP.ip2n(p[1]) >>> 28) === 14) { if (!st.up || !st.ip) return 'ping: connect: Network is unreachable';
      var r = st.net.mcastSend(st.dev, p[1]); if (st.net.onTrace) st.net.onTrace({ ok: r.ok, steps: r.steps }, st.dev, p[1]);
      return ['PING ' + p[1] + ' (' + p[1] + ') 56(84) bytes of data.', '', '--- ' + p[1] + ' ping statistics ---', '4 packets transmitted, 0 received, 100% packet loss, time 3004ms'].join('\n'); }
    return deb0.apply(this, arguments);
  };
})(typeof window !== 'undefined' ? window : global);
