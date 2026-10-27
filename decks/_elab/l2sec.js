/* Защита L2 на MES (руководства 10.4.6 и 6.6.8.8):
   DHCP snooping — ip dhcp snooping, ip dhcp snooping vlan N; доверенный порт: 10.x — port-security-state trusted (+ set port-role uplink),
     6.x — ip dhcp snooping trust. Ответы DHCP-сервера с недоверенного порта отбрасываются (защита от чужого DHCP-сервера);
     выданные адреса записываются в базу соответствий (show ip dhcp snooping binding).
   ARP inspection — 10.x: ip arp inspection enable, ip arp inspection vlan N; 6.x: ip arp inspection, ip arp inspection vlan N, ip arp inspection trust.
     На недоверенном порту ARP пропускается, только если пара IP–MAC есть в базе DHCP snooping (статический адрес ПК — ARP отброшен).
   Storm-control — storm-control broadcast level N, storm-control broadcast action shutdown (10.x), storm-control broadcast level N (6.x):
     при широковещательном шторме (петля без STP) порт с действием shutdown выключается (err-disable) и петля разрывается.
   Упрощения: опция 82, verify mac-address, ip source guard, пороги pps/kbps не моделируются (шторм — либо есть, либо нет). */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, P = EL.Net.prototype, CMDS = E.CMDS, CFG = E.CFG;
  function mcmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k]; }).filter(Boolean) : null; }
  function each(st, f) { var p = ports(st); if (!p) return '% Команда доступна в настройке порта'; p.forEach(f); }
  function sec(st) { return st.l2s || (st.l2s = { dhcp: false, dvl: [], dai: false, avl: [], bind: [] }); }
  function addV(L, v) { if (L.indexOf(v) < 0) L.push(v); L.sort(function (a, b) { return a - b; }); }
  function delV(L, v) { var i = L.indexOf(v); if (i >= 0) L.splice(i, 1); }
  // ---------------------------------------------------------------- команды
  mcmd(['10', '6'], 'config', 'ip dhcp snooping', function (st) { sec(st).dhcp = true; }, 'Включить DHCP snooping');
  mcmd(['10', '6'], 'config', 'no ip dhcp snooping', function (st) { sec(st).dhcp = false; });
  mcmd(['10', '6'], 'config', 'ip dhcp snooping vlan <n>', function (st, a) { addV(sec(st).dvl, a[0]); }, 'DHCP snooping в VLAN');
  mcmd(['10', '6'], 'config', 'no ip dhcp snooping vlan <n>', function (st, a) { delV(sec(st).dvl, a[0]); });
  mcmd(['10'], 'config', 'ip arp inspection enable', function (st) { sec(st).dai = true; }, 'Включить ARP inspection');
  mcmd(['10'], 'config', 'ip arp inspection disable', function (st) { sec(st).dai = false; });
  mcmd(['6'], 'config', 'ip arp inspection', function (st) { sec(st).dai = true; }, 'Включить ARP inspection');
  mcmd(['6'], 'config', 'no ip arp inspection', function (st) { sec(st).dai = false; });
  mcmd(['10', '6'], 'config', 'ip arp inspection vlan <n>', function (st, a) { addV(sec(st).avl, a[0]); }, 'ARP inspection в VLAN');
  mcmd(['10', '6'], 'config', 'no ip arp inspection vlan <n>', function (st, a) { delV(sec(st).avl, a[0]); });
  mcmd(['10'], 'if range', 'port-security-state trusted', function (st) { return each(st, function (p) { p.trust = true; }); }, 'Доверенный порт (DHCP snooping, ARP inspection)');
  mcmd(['10'], 'if range', 'no port-security-state', function (st) { return each(st, function (p) { delete p.trust; }); });
  mcmd(['10'], 'if range', 'set port-role <w>', function (st, a) { if (a[0] !== 'uplink' && a[0] !== 'downlink') return '% Invalid input'; return each(st, function (p) { p.role = a[0]; }); }, 'Роль порта uplink | downlink');
  mcmd(['6'], 'if range', 'ip dhcp snooping trust', function (st) { return each(st, function (p) { p.trust = true; }); }, 'Доверенный порт DHCP snooping');
  mcmd(['6'], 'if range', 'no ip dhcp snooping trust', function (st) { return each(st, function (p) { delete p.trust; }); });
  mcmd(['6'], 'if range', 'ip arp inspection trust', function (st) { return each(st, function (p) { p.atrust = true; }); }, 'Доверенный порт ARP inspection');
  mcmd(['6'], 'if range', 'no ip arp inspection trust', function (st) { return each(st, function (p) { delete p.atrust; }); });
  mcmd(['10', '6'], 'if range', 'storm-control broadcast level <n>', function (st, a) { return each(st, function (p) { p.storm = p.storm || {}; p.storm.level = a[0]; }); }, 'Контроль широковещательного трафика');
  mcmd(['10', '6'], 'if range', 'no storm-control broadcast level', function (st) { return each(st, function (p) { delete p.storm; }); });
  mcmd(['10'], 'if range', 'storm-control broadcast action <w>', function (st, a) { if (['shutdown', 'trap', 'trap-and-shutdown'].indexOf(a[0]) < 0) return '% Invalid input';
    return each(st, function (p) { p.storm = p.storm || {}; p.storm.act = a[0]; }); }, 'Действие при шторме');
  mcmd(['10'], 'if range', 'no storm-control broadcast action', function (st) { return each(st, function (p) { if (p.storm) delete p.storm.act; }); });
  function bindText(st) { var b = sec(st).bind;
    var o = ['   MAC Address        IP Address      Lease (sec)   Type          VLAN  Interface', '------------------- --------------- ------------- ------------- ----- ---------'];
    b.forEach(function (x) { o.push(rp(x.mac, 20) + rp(x.ip, 16) + rp(86400, 14) + rp('learned', 14) + rp(x.vlan, 6) + x.port); });
    return o.concat(['', 'Total number of binding: ' + b.length]).join('\n'); }
  ['', 'do '].forEach(function (pre) { var m = pre ? CFG : 'priv';
    mcmd(['10', '6'], m, pre + 'show ip dhcp snooping binding', bindText, 'База соответствий DHCP snooping');
    mcmd(['10', '6'], m, pre + 'show ip dhcp snooping', function (st) { var s = sec(st); return 'DHCP snooping is ' + (s.dhcp ? 'Enabled' : 'Disabled') + '\nDHCP snooping is configured on following VLANs: ' + (s.dvl.join(', ') || '') +
      '\nTrusted interfaces: ' + Object.keys(st.ports).filter(function (k) { return st.ports[k].trust; }).join(', '); }, 'Состояние DHCP snooping');
    mcmd(['10', '6'], m, pre + 'show ip arp inspection', function (st) { var s = sec(st); return 'ARP Inspection is ' + (s.dai ? 'Enabled' : 'Disabled') + '\nVLANs: ' + (s.avl.join(', ') || ''); }, 'Состояние ARP inspection');
  });
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  E.RUNX.push(function (st, o) { var s = st.l2s; if (!s) return;
    if (s.dhcp) o.push('ip dhcp snooping'); s.dvl.forEach(function (v) { o.push('ip dhcp snooping vlan ' + v); });
    if (s.dai) o.push(st.dialect === '6' ? 'ip arp inspection' : 'ip arp inspection enable'); s.avl.forEach(function (v) { o.push('ip arp inspection vlan ' + v); }); });
  E.PORTX.push(function (st, k, p, d) {
    if (p.trust) d.push(st.dialect === '6' ? ' ip dhcp snooping trust' : ' port-security-state trusted'); if (p.role) d.push(' set port-role ' + p.role);
    if (p.atrust) d.push(' ip arp inspection trust');
    if (p.storm) { if (p.storm.level) d.push(' storm-control broadcast level ' + p.storm.level); if (p.storm.act) d.push(' storm-control broadcast action ' + p.storm.act); } });

  // ---------------------------------------------------------------- поведение
  function trusted(st, p, kind) { var x = st.ports[p] || {}; return kind === 'arp' && st.dialect === '6' ? !!x.atrust : !!x.trust; }
  function vlanOf(s, dev, port, tag) { var L = s.lportOf(dev, port); if (!L) return null; var c = L.cfg; return tag !== null && tag !== undefined ? tag : c.mode === 'access' ? c.access : c.mode === 'trunk' ? c.native : c.pvid; }
  function physPort(s, sg, side) { var l = s.links[sg.li]; return l ? (l.a.dev === side ? l.a.port : l.b.port) : null; }
  // DHCP snooping: ответ сервера идёт обратно по пути запроса; на каждом MES он входит через порт, которым запрос ушёл к серверу
  P.snoopReply = function (path) {
    var s = this;
    for (var i = 0; i < path.length; i++) { var sg = path[i], d = s.devs[sg.from]; if (!d || d.type !== 'mes') continue;
      var st = d.st, c = st.l2s; if (!c || !c.dhcp) continue; var port = physPort(s, sg, sg.from), v = vlanOf(s, sg.from, port, sg.tag);
      if (c.dvl.indexOf(v) < 0) continue;
      if (!trusted(st, port, 'dhcp')) return d.name + ': DHCP snooping — ответ DHCP-сервера пришёл на недоверенный порт ' + port + ' (VLAN ' + v + ') и отброшен';
    }
    return null;
  };
  P.snoopBind = function (path, mac, ip) {
    var s = this;
    path.forEach(function (sg) { var d = s.devs[sg.to]; if (!d || d.type !== 'mes') return; var c = d.st.l2s; if (!c || !c.dhcp) return;
      var port = physPort(s, sg, sg.to), v = vlanOf(s, sg.to, port, sg.tag); if (c.dvl.indexOf(v) < 0 || trusted(d.st, port, 'dhcp')) return;
      c.bind = c.bind.filter(function (b) { return b.mac !== mac; }); c.bind.push({ mac: mac, ip: ip, vlan: v, port: port }); });
  };
  // ARP inspection: проверка на входе MES (через macIn — туда приходит каждый кадр отправителя)
  var macIn0 = P.macIn;
  P.macIn = function (dev, port, v, mac) {
    var ip = this._arpSip, d = this.devs[dev];
    if (ip && d && d.type === 'mes') { var c = d.st.l2s;
      if (c && c.dai && c.avl.indexOf(v) >= 0 && !trusted(d.st, port, 'arp') &&
          !c.bind.some(function (b) { return b.mac === mac && b.ip === ip && b.vlan === v; }))
        return d.name + ': ARP inspection — ' + ip + ' / ' + mac + ' нет в базе DHCP snooping, порт ' + port + ' недоверенный (VLAN ' + v + ') — ARP отброшен'; }
    return macIn0.apply(this, arguments);
  };
  // storm-control: шторм выключает порт с action shutdown
  P.stormControl = function (segs) {
    var s = this, hit = [];
    (segs || []).forEach(function (sg) { var d = s.devs[sg.to]; if (!d || d.type !== 'mes') return; var port = physPort(s, sg, sg.to), p = d.st.ports[port];
      if (p && p.storm && p.storm.level && /shutdown/.test(p.storm.act || '') && !p.shut) { p.shut = true; p.errdis = 'storm-control'; hit.push(d.name + ' ' + port); } });
    if (hit.length) this.gen++;
    return hit;
  };
})(typeof window !== 'undefined' ? window : global);
