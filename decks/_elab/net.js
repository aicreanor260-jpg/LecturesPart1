/* Модель сети: устройства, кабели, прохождение кадров по VLAN/trunk/general, ARP, маршрутизация, межсетевой экран ESR.
   Каждая отправка пакета возвращает пошаговую трассу — её проигрывает интерфейс («как идут пакеты»). */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, H = EL.hosts;

  // каталог: только модели с CLI, совместимым с движком (MES14xx/24xx/3400/37xx — одна ветка ПО 10.4.x)
  // коммутаторы — из каталога eltex.ru (catalog.js, ветка ПО 10.x: тот же CLI, что у движка); нумерация портов упрощена до gi1/0/1–N
  var MODELS = {};
  Object.keys(EL.CATALOG || {}).forEach(function (k) { MODELS[k] = EL.CATALOG[k]; });
  MODELS.vESR = { type: 'esr', ports: 4, group: 'Маршрутизаторы ESR', note: 'Виртуальный сервисный маршрутизатор, 4 × gigabitethernet (как шаблон vESR в pnetlab NTF2)' };
  MODELS.VPC = { type: 'vpc', ports: 1, group: 'Конечные узлы', note: 'Виртуальный ПК (как VPCS в pnetlab)' };
  MODELS.Debian = { type: 'deb', ports: 1, group: 'Конечные узлы', note: 'Компьютер с Debian 11: ip, ifup, nano, ping, ssh, curl' };
  MODELS['Debian-server'] = { type: 'deb', ports: 1, group: 'Конечные узлы', note: 'Сервер Debian: веб-сервер apache2 (80/tcp) и NTP chronyd', opts: { host: 'debian-serv', web: true, tz: 8 } };
  MODELS.Docker = { type: 'deb', ports: 1, group: 'Конечные узлы', note: 'Docker-браузер: open http://A.B.C.D (как pnet-chrome)', opts: { host: 'docker', auto: true, browser: true } };

  function Net() { this.devs = {}; this.order = []; this.links = []; this.mac = {}; this.arp = {}; this.onTrace = null; this.now = 0; }
  var P = Net.prototype;

  P.portsOf = function (d) {
    var m = MODELS[d.model];
    if (d.type === 'vpc') return ['eth0'];
    if (d.type === 'deb') return ['ens3'];
    if (m.portList) return m.portList.slice();
    var o = []; for (var i = 1; i <= m.ports; i++) o.push('gi1/0/' + i); return o;
  };
  P.add = function (model, name, x, y) {
    var m = MODELS[model]; if (!m) throw new Error('Нет модели ' + model);
    if (!name) { var n = 1, base = model === 'Docker' ? 'Docker' : model === 'Debian-server' ? 'Server' : { mes: 'SW', esr: 'R', vpc: 'VPC', deb: 'Debian' }[m.type];
      while (this.byName(base + n)) n++; name = base + n; }
    if (this.byName(name)) throw new Error('Имя ' + name + ' занято');
    var id = 'd' + (++Net.seq);
    var d = { id: id, name: name, model: model, type: m.type, x: x || 0, y: y || 0 };
    if (m.type === 'mes') { d.st = EL.mes.fresh(m.ports, m.dialect === '8' ? 'switch' : 'console', m.portList, m.dialect); d.st.bmac = 'e0:d9:e3:00:00:' + ('0' + (Net.seq + 1).toString(16)).slice(-2); }
    if (m.type === 'esr') d.st = EL.esr.fresh(m.host || 'vesr', m.ports, m.portList);
    if (m.type === 'vpc') d.st = H.vpc(name);
    if (m.type === 'deb') d.st = H.deb(name, m.opts);
    EL.attach(d.st, this, id);
    this.gen++;
    this.devs[id] = d; this.order.push(id); this.mac[id] = {}; this.arp[id] = {};
    return d;
  };
  Net.seq = 0;
  P.byName = function (n) { var s = this; return s.order.map(function (i) { return s.devs[i]; }).filter(function (d) { return d.name === n; })[0] || null; };
  P.list = function () { var s = this; return s.order.map(function (i) { return s.devs[i]; }); };
  P.remove = function (id) {
    this.gen++;
    this.links = this.links.filter(function (l) { return l.a.dev !== id && l.b.dev !== id; });
    delete this.devs[id]; this.order = this.order.filter(function (x) { return x !== id; });
  };
  P.peer = function (dev, port) {
    for (var i = 0; i < this.links.length; i++) { var l = this.links[i];
      if (l.a.dev === dev && l.a.port === port) return { dev: l.b.dev, port: l.b.port, li: i };
      if (l.b.dev === dev && l.b.port === port) return { dev: l.a.dev, port: l.a.port, li: i }; }
    return null;
  };
  P.linked = function (dev, port) { return !!this.peer(dev, port); };
  P.connect = function (a, ap, b, bp) {
    var A = this.devs[a], B = this.devs[b];
    if (!A || !B) return 'Нет такого устройства';
    if (a === b) return 'Нельзя соединить устройство само с собой';
    if (this.portsOf(A).indexOf(ap) < 0 || this.portsOf(B).indexOf(bp) < 0) return 'Нет такого порта';
    if (this.linked(a, ap)) return A.name + ' ' + ap + ' уже занят';
    if (this.linked(b, bp)) return B.name + ' ' + bp + ' уже занят';
    this.gen++;
    this.links.push({ a: { dev: a, port: ap }, b: { dev: b, port: bp } });
    return null;
  };
  P.disconnect = function (li) { this.links.splice(li, 1); this.gen++; };
  P.freePorts = function (id) { var s = this, d = this.devs[id]; return this.portsOf(d).filter(function (p) { return !s.linked(id, p); }); };

  // ------------------------------------------------------------------ L3-интерфейсы и маршруты
  P.ifaces = function (id) {
    var self = this, d = this.devs[id], st = d.st, o = [];
    if (d.type === 'vpc' && st.ip) o.push({ name: 'eth0', ip: st.ip, len: st.len, port: 'eth0', tag: null });
    if (d.type === 'deb' && st.ip && st.up) o.push({ name: 'ens3', ip: st.ip, len: st.len, port: 'ens3', tag: null });
    if (d.type === 'mes') Object.keys(st.svi).forEach(function (v) {
      var p = st.svi[v].split('/'); if (!EL.mes.sviUp(st, +v)) return;
      o.push({ name: 'vlan' + v, ip: p[0], len: +p[1], vlan: +v }); });
    if (d.type === 'esr') Object.keys(st.run.ifs).forEach(function (k) {
      var x = st.run.ifs[k]; if (!x.ip || x.shut) return;
      var ph = k.split('.')[0]; if (k.charAt(0) !== 'l' && (st.run.ifs[ph].shut || !self.linkUp(id, ph))) return;
      var p = x.ip.split('/');
      o.push({ name: k, ip: p[0], len: +p[1], port: k.charAt(0) === 'l' ? null : ph, tag: k.indexOf('.') > 0 ? +k.split('.')[1] : null, fw: x.fw && k.charAt(0) !== 'l' }); });
    if (d.type === 'esr') { var vt = this.vrrp()[id] || {}; Object.keys(vt).forEach(function (k) { var v = vt[k]; if (!v.master) return;
      var base = o.filter(function (f) { return f.name === k; })[0]; if (!base) return; var vp = v.vip.split('/');
      o.push({ name: k + ':vrrp', ip: vp[0], len: +vp[1], port: base.port, tag: base.tag, fw: base.fw, vrrp: true }); }); }
    if (d.type === 'esr') Object.keys(st.run.bridges || {}).forEach(function (k) {   // Bridge N — L3-интерфейс VLAN портов в switchport
      var b = st.run.bridges[k]; if (!b.on || !b.ip || !b.vlan) return; var p = b.ip.split('/');
      o.push({ name: 'bridge' + k, ip: p[0], len: +p[1], port: null, br: b.vlan, fw: b.fw }); });
    return o;
  };
  // все маршруты-кандидаты: C (AD 0), S (AD из команды, по умолчанию 1), R (120), O (110)
  P.routes = function (id) {
    var d = this.devs[id], st = d.st, o = [], fs = this.ifaces(id);
    fs.forEach(function (f) { o.push({ p: 'C', net: IP.netOf(f.ip, f.len), len: f.len, nh: null, ifn: f.name, ad: 0, m: 0 }); });
    var stat = d.type === 'esr' ? st.run.routes : d.type === 'mes' ? st.routes.slice() : [];
    if (d.type === 'mes' && st.gw) stat = stat.concat([{ net: '0.0.0.0/0', nh: st.gw }]);
    if ((d.type === 'vpc' || d.type === 'deb') && st.gw) stat = [{ net: '0.0.0.0/0', nh: st.gw }];
    stat.forEach(function (r) {            // статический маршрут действует, только если шлюз в подключённой работающей сети
      var out = fs.filter(function (f) { return (f.port !== null || f.vlan || f.br) && IP.sameNet(r.nh, f.ip, f.len); })[0];
      o.push({ p: 'S', net: r.net, len: +r.net.split('/')[1], nh: r.nh, ifn: out ? out.name : null, ad: r.ad || 1, m: 0, dead: !out });
    });
    if (d.type === 'esr') (this.dyn()[id] || []).forEach(function (r) { o.push(r); });
    return o;
  };
  function better(a, b) { return !b || a.ad < b.ad || (a.ad === b.ad && a.m < b.m); }
  P.best = function (id, rs) {             // лучший маршрут на каждый префикс
    var by = {};
    (rs || this.routes(id)).forEach(function (r) { if (!r.dead && better(r, by[r.net])) by[r.net] = r; });
    return by;
  };
  P.lookup = function (id, dst) {
    var fs = this.ifaces(id), by = this.best(id), best = null;
    Object.keys(by).forEach(function (k) { var r = by[k];
      if (!IP.sameNet(dst, r.net.split('/')[0], r.len)) return;
      if (!best || r.len > best.len) best = r; });
    if (!best) return null;
    var out = fs.filter(function (f) { return f.name === best.ifn; })[0];
    if (!out) return null;
    return { iface: out, nh: best.nh || dst, r: best };
  };

  // ------------------------------------------------------------------ RIP и OSPF: расчёт по соседствам
  P.gen = 0;
  P.dyn = function () {
    if (this._dyn && this._dyn.gen === this.gen && this._dyn.now === this.now) return this._dyn.t;
    var s = this, t = {};
    this._dyn = { gen: this.gen, now: this.now, t: t };
    s._ospfMis = {};     // защита от повторного входа: flood не зависит от динамических маршрутов
    ['R', 'O'].forEach(function (proto) {
      var rs = s.order.filter(function (id) { var d = s.devs[id]; if (d.type !== 'esr') return false;
        var c = d.st.run; return proto === 'R' ? c.rip && c.rip.on : c.ospf && c.ospf.on; });
      var info = {}, tab = {};
      rs.forEach(function (id) {
        var c = s.devs[id].st.run, fs = s.ifaces(id), part = [], orig = [];
        fs.forEach(function (f) {
          if (proto === 'R') {
            if (f.port === null) return;
            part.push({ f: f, passive: c.rip.passive.indexOf(f.name) >= 0 });
            if (c.rip.redist.indexOf('connected') >= 0 || c.rip.nets.some(function (n) { var p = n.split('/');
              return f.len >= +p[1] && IP.sameNet(f.ip, p[0], +p[1]); })) orig.push(IP.netOf(f.ip, f.len));
          } else {
            var x = c.ifs[f.name], o = x && x.ospf;
            if (!o || !o.on || o.inst !== c.ospf.id || !o.area || !c.ospf.areas[o.area] || !c.ospf.areas[o.area].on) return;
            var hello = o.hello || 10;
            part.push({ f: f, passive: !!o.passive, area: o.area, cost: o.cost || 1, hello: hello, dead: o.dead || hello * 4 }); orig.push(IP.netOf(f.ip, f.len));
          }
        });
        if (proto === 'R' && c.rip.redist.indexOf('static') >= 0) c.routes.forEach(function (r) { orig.push(r.net); });
        info[id] = { part: part, nb: [] };
        tab[id] = {}; orig.forEach(function (n) { tab[id][n] = { m: 0, nh: null, ifn: null, own: true, at: s.originAt ? s.originAt(proto, id, n) : 0 }; });
      });
      rs.forEach(function (id) {               // соседи — через L2, как реальные hello/update
        info[id].part.forEach(function (pp) {
          if (pp.passive || pp.f.port === null) return;
          s.flood(id, pp.f).eps.forEach(function (e) {
            var oi = info[e.dev]; if (!oi || e.dev === id) return;
            var op = oi.part.filter(function (q) { return q.f.name === e.iface.name && !q.passive; })[0];
            if (!op || !IP.sameNet(pp.f.ip, e.iface.ip, pp.f.len)) return;
            if (proto === 'O' && op.area !== pp.area) return;
            if (proto === 'O' && (op.hello !== pp.hello || op.dead !== pp.dead)) {   // hello с другими таймерами отбрасывается
              s._ospfMis[id + '|' + pp.f.name] = { peer: s.devs[e.dev].name, mine: [pp.hello, pp.dead], his: [op.hello, op.dead] }; return; }
            info[id].nb.push({ dev: e.dev, nh: e.iface.ip, ifn: pp.f.name, cost: proto === 'R' ? 1 : pp.cost });
          });
        });
      });
      if (s.timeLayer) s.timeLayer(proto, rs, info, tab);   // таймеры протоколов: какие соседства уже/ещё действуют
      for (var round = 0; round < 20; round++) {
        var ch = false;
        rs.forEach(function (id) {
          info[id].nb.forEach(function (nb) {
            var nt = nb.frozen || tab[nb.dev]; if (!nt) return;
            Object.keys(nt).forEach(function (n) {
              var m2 = nt[n].m + nb.cost, cur = tab[id][n];
              if (proto === 'R' && m2 > 15) return;
              if (cur && (cur.own || cur.m <= m2)) return;
              var at = s.hopAt ? s.hopAt(proto, id, nb, nt[n]) : 0; if (at > s.now) return;   // обновление ещё не дошло
              tab[id][n] = { m: m2, nh: nb.nh, ifn: nb.ifn, via: nb.dev, stale: !!nb.frozen, at: at }; ch = true;
            });
          });
        });
        if (!ch) break;
      }
      rs.forEach(function (id) {
        t[id] = (t[id] || []).concat(Object.keys(tab[id]).filter(function (n) { return !tab[id][n].own; }).map(function (n) {
          var x = tab[id][n]; return { p: proto, net: n, len: +n.split('/')[1], nh: x.nh, ifn: x.ifn, ad: proto === 'R' ? 120 : 110, m: x.m, via: x.via, stale: x.stale }; }));
        if (proto === 'O') s.devs[id]._ospfNb = info[id].nb;
      });
      s._lastTab = s._lastTab || {}; s._lastTab[proto] = s._lastTab[proto] || {};
      rs.forEach(function (id) { s._lastTab[proto][id] = tab[id]; });   // таблицы для «замороженных» соседей, пока не истёк таймер
    });
    return t;
  };
  P.routeText = function (id, all) {
    var all0 = this.routes(id), by = this.best(id, all0), rs = all0.filter(function (r) { return all || (!r.dead && by[r.net] === r); });
    rs.sort(function (a, b) { return a.ad - b.ad || IP.ip2n(a.net.split('/')[0]) - IP.ip2n(b.net.split('/')[0]); });
    var o = [' Codes: C - connected, S - static, R - RIP derived,', '        O - OSPF derived, IA - OSPF inter area route,', '        * - FIB route', ''];
    rs.forEach(function (r) {
      o.push((r.p + '     ').slice(0, 6) + (by[r.net] === r && !r.dead ? '* ' : '  ') + (r.net + '                  ').slice(0, 19) +
             ('[' + r.ad + '/' + r.m + ']            ').slice(0, 13) + (r.nh ? 'via ' + r.nh + ' on ' + (r.ifn || '-') : 'dev ' + r.ifn) +
             (r.p === 'C' ? '  direct' : '') + (r.dead ? '  (шлюз недоступен)' : ''));
    });
    return o.join('\n');
  };
  P.dynText = function (id, proto) {
    var rs = (this.dyn()[id] || []).filter(function (r) { return r.p === proto; });
    if (!rs.length) return '% Маршрутов ' + (proto === 'R' ? 'RIP' : 'OSPF') + ' нет — проверьте enable, network и соседей';
    return rs.map(function (r) { return proto + '  ' + (r.net + '                  ').slice(0, 19) + '[' + r.ad + '/' + r.m + '] via ' + r.nh + ' on ' + r.ifn; }).join('\n');
  };
  P.ospfNbrText = function (id) {
    var s = this; this.dyn(); var nb = this.devs[id]._ospfNb || [];
    if (!nb.length) return '% Соседей OSPF нет';
    return ['Router ID        Pri  State      Dead time   Address          Interface', '---------------- ---- ---------- ----------- ---------------- ---------']
      .concat(nb.map(function (n) { var c = s.devs[n.dev].st.run.ospf;
        return ((c.rid || n.nh) + '                 ').slice(0, 17) + '1    Full/DR    00:00:35    ' + (n.nh + '                 ').slice(0, 17) + n.ifn; })).join('\n');
  };
  // работает ли кабель: на обоих концах порт не выключен
  P.linkUp = function (id, port) {
    var pr = this.peer(id, port); if (!pr) return false;
    return !portShut(this.devs[id], port) && !portShut(this.devs[pr.dev], pr.port);
  };
  function portShut(d, p) {
    if (d.off) return true;
    if (d.type === 'mes') return !!d.st.ports[p].shut;
    if (d.type === 'esr') return !!d.st.run.ifs[p].shut;
    if (d.type === 'deb') return !d.st.up;
    return false;
  }
  P.owner = function (ip) {
    var s = this; return this.order.filter(function (id) { return s.ifaces(id).some(function (f) { return f.ip === ip; }); })[0] || null;
  };
  function owns(net, id, ip) { return net.ifaces(id).some(function (f) { return f.ip === ip; }); }

  // ------------------------------------------------------------------ LACP: логические порты коммутатора (порт или собранный port-channel)
  P.lports = function (id) {
    var d = this.devs[id], st = d.st, s = this, out = [], po = {};
    this.portsOf(d).forEach(function (p) {
      var x = st.ports[p];
      if (!x.cg) { out.push({ name: p, cfg: x, members: [p] }); return; }
      var k = 'po' + x.cg.id; po[k] = po[k] || { name: k, cfg: (st.pos || {})[k], members: [], down: [] };
      var pr = s.peer(id, p), ok = false;
      if (pr && s.linkUp(id, p)) {
        var pd = s.devs[pr.dev], px = pd.type === 'mes' && pd.st.ports[pr.port];
        if (px && px.cg) { var a = x.cg.mode, b = px.cg.mode;
          ok = (a === 'on' && b === 'on') || (a === 'active' && b !== 'on') || (a === 'passive' && b === 'active'); }
      }
      (ok ? po[k].members : po[k].down).push(p);
    });
    Object.keys(po).forEach(function (k) { if (po[k].members.length && po[k].cfg) out.push(po[k]); });
    return out;
  };
  P.lportOf = function (id, port) {
    var L = this.lports(id); for (var i = 0; i < L.length; i++) if (L[i].members.indexOf(port) >= 0) return L[i];
    return null;
  };
  P.lagText = function (id) {
    var st = this.devs[id].st, s = this, ks = Object.keys(st.pos || {});
    if (!ks.length) return '% Port-channel не настроены';
    var L = this.lports(id);
    return ['Group  Port-channel  Protocol  Ports', '-----  ------------  --------  ---------------------------------------']
      .concat(ks.map(function (k) {
        var mem = s.portsOf(s.devs[id]).filter(function (p) { var c = st.ports[p].cg; return c && 'po' + c.id === k; });
        var up = (L.filter(function (l) { return l.name === k; })[0] || { members: [] }).members;
        var proto = mem.length && st.ports[mem[0]].cg.mode === 'on' ? 'Static' : 'LACP';
        return (k.slice(2) + '      ').slice(0, 7) + (k + (up.length ? '(U)' : '(D)') + '            ').slice(0, 14) + (proto + '          ').slice(0, 10) +
               mem.map(function (p) { return p + (up.indexOf(p) >= 0 ? '(P)' : '(D)'); }).join(' '); })).join('\n') + '\n(P) — в агрегате, (D) — не в агрегате';
  };

  // ------------------------------------------------------------------ RSTP: роли и состояния портов
  function bid(st) { var s = st.stp || { prio: 32768 }; return { prio: s.prio, mac: st.bmac }; }
  function bidLess(a, b) { return a.prio !== b.prio ? a.prio < b.prio : a.mac < b.mac; }
  function pnum(n) { if (n.indexOf('po') === 0) return 1000 + +n.slice(2); var pf = { gi: 0, fa: 0, tw: 100, te: 200, fo: 300, hu: 400 }[n.replace(/[\d\/]+$/, '')] || 0;
    return pf + +n.split('/')[2]; }
  P.stp = function () {
    if (this._stp && this._stp.gen === this.gen) return this._stp.t;
    if (this.bpduGuard && this.bpduGuard()) this.gen++;
    var s = this, t = {}, br = this.order.filter(function (id) { var d = s.devs[id]; return d.type === 'mes' && (!d.st.stp || d.st.stp.on !== false); });
    var on = {}; br.forEach(function (id) { on[id] = true; });
    var edges = [];
    br.forEach(function (id) {
      t[id] = {};
      s.lports(id).forEach(function (L) {
        var pr = s.peer(id, L.members[0]); if (!pr || !s.linkUp(id, L.members[0])) return;
        if (L.cfg.stpOff || !on[pr.dev]) { t[id][L.name] = { role: 'Desg', fwd: true }; return; }
        var R = s.lportOf(pr.dev, pr.port); if (!R) return;
        edges.push({ u: id, a: L.name, v: pr.dev, b: R.name, cu: L.cfg.stpCost || (L.name.indexOf('po') === 0 ? 10000 : 20000) });
      });
    });
    var dist = {}, root = {}, done = {};
    br.forEach(function (id) { dist[id] = Infinity; });
    // корень компоненты — минимальный Bridge ID; расстояние — Дейкстра по стоимости принимающего порта
    br.slice().sort(function (a, b) { return bidLess(bid(s.devs[a].st), bid(s.devs[b].st)) ? -1 : 1; }).forEach(function (r) {
      if (dist[r] !== Infinity) return;
      dist[r] = 0; root[r] = r; var q = [r];
      while (q.length) {
        q.sort(function (a, b) { return dist[a] - dist[b]; }); var u = q.shift(); if (done[u]) continue; done[u] = true;
        edges.forEach(function (e) { if (e.u !== u) return; var back = edges.filter(function (x) { return x.u === e.v && x.a === e.b; })[0];
          var c = dist[u] + (back ? back.cu : 20000);
          if (c < dist[e.v]) { dist[e.v] = c; root[e.v] = r; q.push(e.v); } });
      }
    });
    function key(id, port) { var b = bid(s.devs[id].st); return [dist[id], b.prio, b.mac, pnum(port)]; }
    function less(a, b) { for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] < b[i]; return false; }
    var rootPort = {};
    br.forEach(function (id) {
      if (root[id] === id) return;
      var best = null;
      edges.forEach(function (e) { if (e.u !== id) return;
        var cand = [dist[e.v] + e.cu, bid(s.devs[e.v].st).prio, bid(s.devs[e.v].st).mac, pnum(e.b), pnum(e.a)];
        if (!best || less(cand, best.k)) best = { k: cand, port: e.a }; });
      if (best) rootPort[id] = best.port;
    });
    edges.forEach(function (e) {
      if (t[e.u][e.a]) return;
      if (rootPort[e.u] === e.a) { t[e.u][e.a] = { role: 'Root', fwd: true }; return; }
      var mine = key(e.u, e.a), his = key(e.v, e.b);
      if (less(mine, his)) t[e.u][e.a] = { role: 'Desg', fwd: true };
      else t[e.u][e.a] = { role: e.v === e.u ? 'Back' : 'Altn', fwd: false };
    });
    this._stp = { gen: this.gen, t: t, root: root, dist: dist };
    return t;
  };
  P.stpFwd = function (id, lname) {
    var d = this.devs[id]; if (d.st.stp && d.st.stp.on === false) return true;
    var r = (this.stp()[id] || {})[lname]; return !r || r.fwd;
  };
  P.stpText = function (id) {
    var d = this.devs[id], st = d.st, s = this;
    if (st.stp && st.stp.on === false) return 'Spanning tree disabled';
    var t = this.stp()[id] || {}, R = this._stp.root[id], rb = bid(this.devs[R].st), me = bid(st);
    var mode = { stp: 'STP', rst: 'RSTP', mst: 'MSTP', pvst: 'PVST', 'rapid-pvst': 'Rapid-PVST' }[(st.stp || {}).mode || 'mst'];
    var o = ['Spanning tree enabled mode ' + mode, 'Default port cost method:  long', '',
      '  Root ID    Priority    ' + rb.prio, '             Address     ' + rb.mac];
    if (R === id) o.push('             This switch is the root'); else o.push('             Cost        ' + this._stp.dist[id]);
    o.push('             Hello Time 2 sec  Max Age 20 sec  Forward Delay 15 sec', '',
      '  Bridge ID  Priority    ' + me.prio, '             Address     ' + me.mac, '',
      'Interfaces', ' Name       State   Prio.Nbr  Cost      Sts   Role   Type', ' ---------- ------- --------- --------- ----- ------ ----------');
    this.lports(id).forEach(function (L) { var r = t[L.name]; if (!r) return;
      o.push(' ' + (L.name + '          ').slice(0, 11) + 'enabled 128.' + (pnum(L.name) + '    ').slice(0, 5) + ' ' +
             ((L.cfg.stpCost || (L.name.indexOf('po') === 0 ? 10000 : 20000)) + '          ').slice(0, 10) + (r.fwd ? 'Frw   ' : 'Dsc   ') + (r.role + '      ').slice(0, 7) + 'P2p'); });
    return o.join('\n');
  };

  // ------------------------------------------------------------------ VRRP: мастер — наибольший приоритет (при равенстве — больший адрес)
  P.vrrp = function () {
    if (this._vrrp && this._vrrp.gen === this.gen) return this._vrrp.t;
    var s = this, g = {}, t = {};
    this.order.forEach(function (id) { var d = s.devs[id]; if (d.type !== 'esr') return;
      Object.keys(d.st.run.ifs).forEach(function (k) { var x = d.st.run.ifs[k], v = x.vrrp;
        if (!v || !v.on || !v.id || !v.ip || x.shut) return;
        var ph = k.split('.')[0], up = !d.st.run.ifs[ph].shut && s.linkUp(id, ph);
        var key = v.id + '|' + v.ip; (g[key] = g[key] || []).push({ dev: id, ifn: k, prio: v.prio, ip: x.ip ? x.ip.split('/')[0] : '0.0.0.0', up: up, vip: v.ip }); }); });
    Object.keys(g).forEach(function (k) {
      var live = g[k].filter(function (m) { return m.up; });
      live.sort(function (a, b) { return b.prio - a.prio || EL.ip.ip2n(b.ip) - EL.ip.ip2n(a.ip); });
      g[k].forEach(function (m) { (t[m.dev] = t[m.dev] || {})[m.ifn] = { master: live[0] === m, vip: m.vip, id: +k.split('|')[0], prio: m.prio, up: m.up,
        peers: g[k].length, masterDev: live[0] ? live[0].dev : null }; });
    });
    this._vrrp = { gen: this.gen, t: t };
    return t;
  };
  P.vrrpText = function (id) {
    var t = this.vrrp()[id], s = this;
    if (!t) return '% VRRP не настроен (vrrp id, vrrp ip, vrrp на интерфейсе и commit)';
    return [' Virtual router   Virtual IP          Priority  Preemption  State', ' --------------   -----------------   --------  ----------  ------']
      .concat(Object.keys(t).map(function (k) { var v = t[k];
        return ' ' + (v.id + '                 ').slice(0, 17) + (v.vip + '                    ').slice(0, 20) + (v.prio + '          ').slice(0, 10) +
               'Enabled     ' + (!v.up ? 'Init' : v.master ? 'Master' : 'Backup'); })).join('\n');
  };

  // ------------------------------------------------------------------ L2: куда дойдёт кадр
  // egress: как порт коммутатора отправит кадр VLAN v — 'u' без тега, 't' с тегом, null — не отправит
  function egress(p, v) {
    if (p.shut) return null;
    if (p.mode === 'access') return p.access === v ? 'u' : null;
    if (p.mode === 'trunk') return p.native === v ? 'u' : (p.allowed.indexOf(v) >= 0 ? 't' : null);
    if (p.guntag.indexOf(v) >= 0) return 'u';
    return p.gtag.indexOf(v) >= 0 ? 't' : null;
  }
  // ingress: в какую VLAN попадёт входящий кадр (tag=null — без тега); {v} или {drop: причина}
  function ingress(st, port, tag, p) {
    p = p || st.ports[port];
    if (p.shut) return { drop: 'порт ' + port + ' выключен (shutdown)' };
    var v;
    if (tag === null) v = p.mode === 'access' ? p.access : p.mode === 'trunk' ? p.native : p.pvid;
    else {
      if (p.mode === 'access') return { drop: port + ' в режиме access принимает только кадры без тега, пришёл тег ' + tag };
      if (p.mode === 'trunk' && p.allowed.indexOf(tag) < 0 && p.native !== tag) return { drop: 'VLAN ' + tag + ' не разрешена на trunk ' + port };
      if (p.mode === 'general' && p.gtag.indexOf(tag) < 0 && p.guntag.indexOf(tag) < 0) return { drop: 'VLAN ' + tag + ' не разрешена на general-порту ' + port };
      v = tag;
    }
    if (!st.vlans[v]) return { drop: 'VLAN ' + v + ' не создана на коммутаторе' };
    return { v: v };
  }
  // рассылка кадра из L3-интерфейса: список достигнутых интерфейсов + все пройденные отрезки + причины отбрасывания
  P.flood = function (id, f, srcMac) {
    var s = this, seen = {}, eps = [], segs = [], notes = [], q = [], got = {}, storm = false;
    function send(dev, port, tag, path) {
      var pr = s.peer(dev, port); if (!pr) return;
      var seg = { li: pr.li, from: dev, to: pr.dev, tag: tag };
      segs.push(seg); q.push({ dev: pr.dev, port: pr.port, tag: tag, path: path.concat([seg]) });
    }
    function inMes(dev, inPort, v, path) {
      var st = s.devs[dev].st;
      if (inPort && srcMac) { var pv = s.macIn(dev, inPort, v, srcMac); if (pv) { notes.push(pv); return; } }
      var gk = dev + '|' + v; got[gk] = (got[gk] || 0) + 1;
      if (got[gk] > 1) { if (!storm) notes.push(s.devs[dev].name + ': тот же широковещательный кадр пришёл второй раз — петля без STP, широковещательный шторм'); storm = true; return; }
      Object.keys(st.svi).forEach(function (sv) { if (+sv === v && EL.mes.sviUp(st, v) && !(dev === id && f.vlan === v)) {
        var p = st.svi[sv].split('/'); eps.push({ dev: dev, iface: { name: 'vlan' + v, ip: p[0], len: +p[1], vlan: v }, path: path }); } });
      s.lports(dev).forEach(function (L) {           // логические порты: обычный порт или собранный port-channel
        if (L.name === inPort || !s.linked(dev, L.members[0]) || !s.stpFwd(dev, L.name)) return;
        var e = egress(L.cfg, v); if (e) send(dev, L.members[0], e === 't' ? v : null, path);
      });
    }
    function inEsrSw(dev, inPort, v, path) {      // коммутация на ESR: порты switchport одной VLAN + Bridge этой VLAN
      var c = s.devs[dev].st.run;
      Object.keys(c.bridges || {}).forEach(function (k) { var b = c.bridges[k];
        if (b.on && b.ip && b.vlan === v && !(dev === id && f.br === v)) { var p = b.ip.split('/');
          eps.push({ dev: dev, iface: { name: 'bridge' + k, ip: p[0], len: +p[1], port: null, br: v, fw: b.fw }, path: path }); } });
      Object.keys(c.ifs).forEach(function (q2) { var x = c.ifs[q2];
        if (q2 === inPort || !x.sw || x.shut || x.sw.vlan !== v || !s.linked(dev, q2)) return; send(dev, q2, null, path); });
    }
    if (f.br) inEsrSw(id, null, f.br, []);
    else if (f.vlan) inMes(id, null, f.vlan, []);
    else if (f.port) send(id, f.port, f.tag, []);
    while (q.length) {
      var it = q.shift(), key = it.dev + '|' + it.port + '|' + it.tag;
      if (seen[key]) continue; seen[key] = 1;
      var d = this.devs[it.dev], nm = d.name;
      if (d.off) { notes.push(nm + ': устройство выключено'); continue; }
      if (d.type === 'mes') {
        var LP = this.lportOf(it.dev, it.port);
        if (!LP) { notes.push(nm + ': ' + it.port + ' в channel-group, но агрегат не собран (LACP) — порт не передаёт'); continue; }
        if (!this.stpFwd(it.dev, LP.name)) { notes.push(nm + ': ' + LP.name + ' заблокирован STP (роль ' + this.stp()[it.dev][LP.name].role + ') — кадр отброшен'); continue; }
        var r = ingress(d.st, LP.name, it.tag, LP.cfg);
        if (r.drop) { notes.push(nm + ': ' + r.drop); continue; }
        inMes(it.dev, LP.name, r.v, it.path);
      } else if (d.type === 'esr') {
        var phys = d.st.run.ifs[it.port];
        if (phys.shut) { notes.push(nm + ': интерфейс ' + it.port + ' выключен'); continue; }
        if (phys.sw) { if (it.tag !== null) { notes.push(nm + ': ' + it.port + ' (access) — кадр с тегом ' + it.tag + ' отброшен'); continue; }
          inEsrSw(it.dev, it.port, phys.sw.vlan, it.path); continue; }
        var k = it.tag === null ? it.port : it.port + '.' + it.tag, x = d.st.run.ifs[k];
        if (!x) { notes.push(nm + ': нет саб-интерфейса ' + it.port + '.' + it.tag + ' — кадр с тегом ' + it.tag + ' отброшен'); continue; }
        if (!x.ip || x.shut) { notes.push(nm + ': на ' + k + ' нет IP-адреса или он выключен'); continue; }
        var pp = x.ip.split('/');
        eps.push({ dev: it.dev, iface: { name: k, ip: pp[0], len: +pp[1], port: it.port, tag: it.tag, fw: x.fw }, path: it.path });
        var vv = (this.vrrp()[it.dev] || {})[k];
        if (vv && vv.master) { var vp = vv.vip.split('/');
          eps.push({ dev: it.dev, iface: { name: k + ':vrrp', ip: vp[0], len: +vp[1], port: it.port, tag: it.tag, fw: x.fw, vrrp: true }, path: it.path }); }
      } else {
        if (it.tag !== null) { notes.push(nm + ': пришёл кадр с тегом ' + it.tag + ' — ПК тегов не понимает, отброшен'); continue; }
        var hf = this.ifaces(it.dev)[0];
        if (!hf) { notes.push(nm + ': на интерфейсе нет IP-адреса' + (d.type === 'deb' && !d.st.up ? ' (ens3 выключен)' : '')); continue; }
        eps.push({ dev: it.dev, iface: hf, path: it.path });
      }
    }
    return { eps: eps, segs: segs, notes: notes, storm: storm };
  };

  // ------------------------------------------------------------------ отправка IP-пакета (в одну сторону) с NAT
  // pk = {src, dst, proto: 'icmp'|'tcp'|'udp', dport}; ct — таблица трансляций текущего обмена (общая для запроса и ответа)
  function inRange(ip, r) { var n = IP.ip2n(ip); return n >= IP.ip2n(r[0]) && n <= IP.ip2n(r[1]); }
  function natRules(d, kind, ifn) {
    var n = d.st.run[kind], out = [];
    if (!n) return out;
    Object.keys(n.rulesets).forEach(function (k) { var rs = n.rulesets[k]; if (rs.ifn !== ifn) return;
      Object.keys(rs.rules).sort(function (a, b) { return a - b; }).forEach(function (q) { if (rs.rules[q].on) out.push(rs.rules[q]); }); });
    return out;
  }
  function ruleHit(r, pk, c) {
    if (r.src && !inRange(pk.src, r.src)) return false;
    if (r.dst && !inRange(pk.dst, r.dst)) return false;
    if (r.srcOg && !EL.ogNet(c, r.srcOg, pk.src)) return false;
    if (r.dstOg && !EL.ogNet(c, r.dstOg, pk.dst)) return false;
    if (r.dportOg && !EL.ogSvc(c, r.dportOg, pk.dport)) return false;
    if (r.proto && r.proto !== 'any' && r.proto !== pk.proto) return false;
    if (r.dport && !(pk.dport >= r.dport[0] && pk.dport <= r.dport[1])) return false;
    return true;
  }
  P.send = function (src, pk, steps, ct) {
    var cur = src, ttl = 16, hops = [];
    while (ttl-- > 0) {
      var cd = this.devs[cur];
      if (owns(this, cur, pk.dst)) return { ok: true, dev: cur, pk: pk, hops: hops };
      var r = this.lookup(cur, pk.dst);
      if (!r) { steps.push({ k: 'drop', t: cd.name + ': нет маршрута до ' + pk.dst + (cd.type === 'vpc' || cd.type === 'deb' ? ' (не задан шлюз или адрес)' : '') });
        return { ok: false, why: 'Destination net unreachable', pk: pk }; }
      if (!pk.src) pk.src = r.iface.ip;
      // свой трафик маршрутизатора: ответы на него межсетевой экран пропускает (сессия)
      if (cd.type === 'esr' && cur === src) ct.push({ kind: 'fw', dev: cur, self: true, proto: pk.proto, a: [pk.src], b: [pk.dst] });
      if (cd.type === 'esr' && cur !== src) {      // Source NAT на выходе
        var sr = natRules(cd, 'snat', r.iface.name).filter(function (x) { return x.act && ruleHit(x, pk, cd.st.run); })[0];
        if (sr) { ct.push({ dev: cur, kind: 's', orig: pk.src, pub: r.iface.ip, peer: pk.dst, proto: pk.proto });
          steps.push({ k: 'nat', t: cd.name + ': Source NAT на ' + r.iface.name + ' — источник ' + pk.src + ' заменён на ' + r.iface.ip });
          pk.src = r.iface.ip; }
      }
      var srcMac = this.ifMac(cur, r.iface);
      var fl = this.flood(cur, r.iface, srcMac);
      var ep = fl.eps.filter(function (e) { return e.iface.ip === r.nh; })[0];
      if (fl.storm) { steps.push({ k: 'arp', segs: fl.segs, t: cd.name + ': ARP-запрос «у кого ' + r.nh + '?» — широковещательно', notes: fl.notes });
        steps.push({ k: 'drop', t: 'Широковещательный шторм: в сети петля, а STP выключен — кадры бесконечно размножаются, связи нет', notes: fl.notes });
        return { ok: false, why: 'Request timed out', pk: pk }; }
      var vl = r.iface.vlan || r.iface.tag, cached = this.arp[cur][r.nh], dmac = ep ? this.ifMac(ep.dev, ep.iface) : null;
      if (cached && cached.mac === dmac) {        // адрес уже в ARP-кэше — широковещательный запрос не нужен
        steps.push({ k: 'route', t: cd.name + ': ' + r.nh + ' уже есть в ARP-таблице (' + cached.mac + ') — ARP-запрос не нужен, кадр сразу на этот MAC' });
      } else if (cached) {                         // запись устарела: кадр уходит на старый MAC и теряется
        steps.push({ k: 'drop', t: cd.name + ': в ARP-таблице ' + r.nh + ' → ' + cached.mac + ', но кадр на этот MAC не доходит (запись устарела: сменили VLAN, порт или адрес). ' +
          'Запись удалена — следующий ping заново спросит ARP', notes: fl.notes });
        delete this.arp[cur][r.nh];
        return { ok: false, why: 'Request timed out', pk: pk };
      } else {
        steps.push({ k: 'arp', segs: fl.segs, t: cd.name + ' (' + r.iface.name + ', ' + r.iface.ip + ', ' + srcMac + '): ARP-запрос «у кого ' + r.nh + '?» — широковещательно' +
          (vl ? ' в VLAN ' + vl : '') + (r.nh !== pk.dst ? ' (это шлюз к ' + pk.dst + ')' : '') + '. Коммутаторы по пути запомнили ' + srcMac, notes: fl.notes,
          f: { type: 'arp', op: 1, smac: srcMac, dmac: 'ff:ff:ff:ff:ff:ff', sip: r.iface.ip, tip: r.nh } });
        if (!ep) { steps.push({ k: 'drop', t: 'Нет ответа на ARP: ' + r.nh + ' недоступен в этом широковещательном домене (другая VLAN, нет шлюза, кабель или порт выключен)', notes: fl.notes });
          return { ok: false, why: 'Host unreachable', pk: pk }; }
      }
      var nd = this.devs[ep.dev];
      var back = ep.path.slice().reverse().map(function (sg) { return { li: sg.li, from: sg.to, to: sg.from, tag: sg.tag }; });
      var viol = this.learn(back, dmac);
      if (viol) { steps.push({ k: 'drop', segs: back, t: nd.name + ': ARP-ответ отброшен — ' + viol }); return { ok: false, why: 'Host unreachable', pk: pk }; }
      this.arp[cur][r.nh] = { mac: dmac, ifn: r.iface.name, t: this.now };
      this.arp[ep.dev][r.iface.ip] = { mac: srcMac, ifn: ep.iface.name, t: this.now };   // отвечающий тоже запоминает спросившего
      this.learn(ep.path, srcMac);
      if (!cached) steps.push({ k: 'arpr', segs: back, t: nd.name + ' (' + ep.iface.name + '): ARP-ответ «' + r.nh + ' — это я, MAC ' + dmac + '» (unicast). ' +
        nd.name + ' записал ' + r.iface.ip + ' → ' + srcMac + ' в свою ARP-таблицу, коммутаторы запомнили ' + dmac,
        f: { type: 'arp', op: 2, smac: dmac, dmac: srcMac, sip: r.nh, tip: r.iface.ip } });
      steps.push({ k: 'ip', segs: ep.path, t: cd.name + ' → ' + nd.name + ': ' + (pk.proto === 'icmp' ? 'ICMP' : pk.proto.toUpperCase() + ':' + pk.dport) + ' ' +
        pk.src + ' → ' + pk.dst + ' в кадре до MAC ' + this.arp[cur][r.nh].mac +
        ep.path.filter(function (s) { return s.tag !== null; }).map(function (s) { return ' · тег 802.1Q ' + s.tag; }).filter(function (x, i, a) { return a.indexOf(x) === i; }).join(''),
        f: { type: 'ip', smac: srcMac, dmac: this.arp[cur][r.nh].mac, src: pk.src, dst: pk.dst, proto: pk.proto, dport: pk.reply ? pk.rport : pk.dport, sport: pk.sport, reply: !!pk.reply, ttl: 64 - hops.length } });
      this.mirror(ep.path, pk);
      if (nd.type === 'esr' && !ep.iface.fw) {         // входящий список доступа на интерфейсе
        var ax = nd.st.run.ifs[ep.iface.name.split(':')[0]], ar = ax && ax.acl ? EL.aclPass((nd.st.run.acls || {})[ax.acl], pk) : { ok: true };
        if (!ar.ok) { steps.push({ k: 'drop', t: nd.name + ': список доступа ' + ax.acl + ' на ' + ep.iface.name.split(':')[0] + ' отбросил ' +
          (pk.proto === 'icmp' ? 'ICMP' : pk.proto.toUpperCase() + (pk.dport ? ':' + pk.dport : '')) + ' от ' + pk.src + (ar.rule ? ' (rule ' + ar.rule + ', deny)' : ' (не подошло ни одно правило — неявный запрет)') });
          return { ok: false, why: 'Request timed out', pk: pk }; }
      }
      var pre = { src: pk.src, dst: pk.dst };     // адреса до трансляций на этом маршрутизаторе
      if (nd.type === 'esr') {                     // обратная трансляция для ответов и Destination NAT на входе
        var self = this;
        ct.forEach(function (c) {
          if (c.dev !== ep.dev) return;
          if (c.kind === 's' && pk.dst === c.pub && pk.src === c.peer) { steps.push({ k: 'nat', t: nd.name + ': ответ на трансляцию — назначение ' + c.pub + ' возвращено в ' + c.orig }); pk.dst = c.orig; }
          if (c.kind === 'd' && pk.src === c.target && pk.dst === c.client) { steps.push({ k: 'nat', t: nd.name + ': ответ сервера — источник ' + c.target + ' заменён обратно на ' + c.pub }); pk.src = c.pub; }
        });
        var dr = natRules(nd, 'dnat', ep.iface.name).filter(function (x) { return x.to && ruleHit(x, pk, nd.st.run); })[0];
        if (dr && !ct.some(function (c) { return c.dev === ep.dev && c.kind === 'd' && c.client === pk.src && c.target === dr.to; }) && pk.dst !== dr.to) {
          ct.push({ dev: ep.dev, kind: 'd', client: pk.src, pub: pk.dst, target: dr.to, proto: pk.proto });
          steps.push({ k: 'nat', t: nd.name + ': Destination NAT на ' + ep.iface.name + ' — ' + pk.dst + (pk.dport ? ':' + pk.dport : '') + ' перенаправлен на ' + dr.to });
          pk.dst = dr.to;
        }
        void self;
        var fw = this.fwPass(ep.dev, ep.iface, pk, ct, pre);   // межсетевой экран по зонам — после Destination NAT
        if (fw.t) steps.push({ k: fw.ok ? 'route' : 'drop', t: fw.t });
        if (!fw.ok) return { ok: false, why: 'Request timed out', pk: pk };
      }
      hops.push({ dev: ep.dev, ip: ep.iface.ip });
      cur = ep.dev;
      if (!owns(this, cur, pk.dst) && (nd.type === 'vpc' || nd.type === 'deb')) {
        steps.push({ k: 'drop', t: nd.name + ' получил чужой пакет и не маршрутизирует его' });
        return { ok: false, why: 'Request timed out', pk: pk };
      }
      if (!owns(this, cur, pk.dst)) steps.push({ k: 'route', t: nd.name + ': адрес ' + pk.dst + ' не мой — ищу маршрут дальше' });
    }
    steps.push({ k: 'drop', t: 'TTL истёк — петля маршрутизации' });
    return { ok: false, why: 'Time to live exceeded', pk: pk };
  };
  // запрос и ответ: ICMP echo, либо TCP/UDP к службе (curl, NTP)
  P.request = function (src, dst, proto, dport) {
    var steps = this.stepLog(), d = this.devs[src], ct = [];
    this.ctLast = ct;
    if (IP.ip2n(dst) === null) return { ok: false, why: 'Bad address', steps: steps };
    if (!this.ifaces(src).length) { steps.push({ k: 'drop', t: d.name + ': нет ни одного IP-адреса' }); return { ok: false, why: 'No IP address', steps: steps }; }
    Net.eph = ((Net.eph || 0) + 1) % 16000;     // эфемерный порт клиента (для захвата трафика)
    var f = this.send(src, { src: null, dst: dst, proto: proto || 'icmp', dport: dport || null, sport: proto && proto !== 'icmp' ? 49152 + Net.eph : null }, steps, ct);
    if (!f.ok) return { ok: false, why: f.why, steps: steps };
    if (f.dev === src && proto === 'icmp') return { ok: true, steps: steps, hops: [] };
    var fd = this.devs[f.dev];
    if (proto !== 'icmp' && !listens(fd, proto, dport)) {
      steps.push({ k: 'drop', t: fd.name + ': на порту ' + proto.toUpperCase() + ' ' + dport + ' никто не слушает — ответ «соединение отклонено»' });
      return { ok: false, why: 'Connection refused', steps: steps, dev: f.dev };
    }
    steps.push({ k: 'ok', t: fd.name + ' получил ' + (proto === 'icmp' ? 'ICMP echo request и отвечает echo reply' : 'запрос ' + proto.toUpperCase() + ':' + dport + ' и отвечает') });
    var b = this.send(f.dev, { src: f.pk.dst, dst: f.pk.src, proto: proto, dport: null, reply: true, sport: dport || null, rport: f.pk.sport }, steps, ct);
    if (!b.ok || b.dev !== src) { steps.push({ k: 'drop', t: 'Ответ не вернулся к ' + d.name + ' — проверьте маршрут/шлюз/NAT в обратную сторону' });
      return { ok: false, why: 'Request timed out', steps: steps }; }
    steps.push({ k: 'ok', t: d.name + ' получил ответ от ' + dst });
    return { ok: true, steps: steps, hops: f.hops, dev: f.dev };
  };
  function listens(d, proto, port) {
    var s = d.st;
    if (d.type === 'deb') return (proto === 'tcp' && port === 80 && s.svc && s.svc.apache2) || (proto === 'udp' && port === 123 && s.svc && s.svc.chronyd) ||
                                 (proto === 'udp' && port === 514 && s.svc && s.svc.rsyslog) || (proto === 'udp' && port === 69 && s.svc && s.svc['tftpd-hpa']) ||
                                 (proto === 'tcp' && port === 22);
    if (d.type === 'esr') return proto === 'tcp' && ((port === 22 && s.run.ssh) || (port === 23 && s.run.telnet));
    return false;
  }
  P.ping = function (src, dst) { return this.request(src, dst, 'icmp'); };
  P.reach = function (srcName, dst) { var d = this.byName(srcName); return !!d && this.ping(d.id, dst).ok; };
  P.http = function (srcName, dst, port) { var d = this.byName(srcName); return !!d && this.request(d.id, dst, 'tcp', port || 80).ok; };

  // ------------------------------------------------------------------ DHCP: DISCOVER широковещательно, сервер или ретранслятор
  P.dhcp = function (id) {
    var s = this, d = this.devs[id], steps = this.stepLog(), ct = [];
    var port = d.type === 'vpc' ? 'eth0' : 'ens3', cname = d.name;
    var fl = this.flood(id, { port: port, tag: null }, EL.mac(cname + port));
    steps.push({ k: 'arp', segs: fl.segs, t: cname + ': DHCPDISCOVER — широковещательно, src 0.0.0.0 → 255.255.255.255:67', notes: fl.notes,
      f: { type: 'ip', smac: EL.mac(cname + port), dmac: 'ff:ff:ff:ff:ff:ff', src: '0.0.0.0', dst: '255.255.255.255', proto: 'udp', sport: 68, dport: 67, ttl: 64, dhcp: 'Discover' } });
    var lease = null;
    fl.eps.some(function (ep) {
      var rd = s.devs[ep.dev]; if (rd.type !== 'esr') return false;
      var c = rd.st.run;
      var fw = s.fwPass(ep.dev, ep.iface, { src: '0.0.0.0', dst: ep.iface.ip, proto: 'udp', dport: 67 }, []);
      if (!fw.ok) { steps.push({ k: 'drop', t: fw.t + ' — DHCP не принят' }); return false; }
      var own = c.dhcp && c.dhcp.on && poolFor(c, ep.iface.ip);
      if (own) { lease = alloc(rd, own, cname); if (lease) lease.via = null; lease && (lease.server = rd.name); return !!lease; }
      var x = c.ifs[ep.iface.name];
      if (c.relay && x && x.helper) {
        steps.push({ k: 'route', t: rd.name + ': ретранслятор — DISCOVER принят на ' + ep.iface.name + ', giaddr = ' + ep.iface.ip + ', пересылаю на ' + x.helper + ' (unicast)' });
        var f = s.send(ep.dev, { src: null, dst: x.helper, proto: 'udp', dport: 67 }, steps, ct);
        if (!f.ok) { steps.push({ k: 'drop', t: 'Сервер ' + x.helper + ' недостижим с ретранслятора' }); return false; }
        var sd = s.devs[f.dev], sc = sd.type === 'esr' ? sd.st.run : null, pl = sc && sc.dhcp && sc.dhcp.on && poolFor(sc, ep.iface.ip);
        if (!pl) { steps.push({ k: 'drop', t: sd.name + ': нет DHCP-сервера или пула для сети ' + IP.netOf(ep.iface.ip, ep.iface.len) }); return false; }
        steps.push({ k: 'ok', t: sd.name + ': пул ' + pl.name + ' — выбран по giaddr ' + ep.iface.ip });
        var b = s.send(f.dev, { src: null, dst: ep.iface.ip, proto: 'udp', dport: 67 }, steps, ct);
        if (!b.ok || b.dev !== ep.dev) { steps.push({ k: 'drop', t: 'Ответ сервера не дошёл до ретранслятора — нет маршрута к ' + ep.iface.ip }); return false; }
        lease = alloc(sd, pl, cname); if (lease) { lease.server = sd.name; lease.via = rd.name; }
        return !!lease;
      }
      return false;
    });
    if (!lease) { steps.push({ k: 'drop', t: 'DHCPOFFER не пришёл: в этом широковещательном домене нет DHCP-сервера или ретранслятора' });
      return { ok: false, steps: steps }; }
    steps.push({ k: 'ok', t: (lease.via ? lease.via + ' → ' : '') + cname + ': DHCPOFFER ' + lease.ip + '/' + lease.len + ', шлюз ' + (lease.gw || '—') + ' (сервер ' + lease.server + ')' });
    steps.push({ k: 'ok', t: cname + ': DHCPREQUEST → ' + lease.server + ': DHCPACK — адрес закреплён' });
    return { ok: true, steps: steps, ip: lease.ip, len: lease.len, gw: lease.gw };
  };
  function poolFor(c, giaddr) {
    var hit = null;
    Object.keys(c.dhcp.pools).forEach(function (k) { var p = c.dhcp.pools[k];
      if (p.net && p.range && IP.sameNet(giaddr, p.net.split('/')[0], +p.net.split('/')[1])) hit = { name: k, p: p }; });
    return hit;
  }
  function alloc(rd, pl, cname) {
    var st = rd.st, L = st.leases = st.leases || {}, p = pl.p, net = rd.st.net || null;
    if (L[cname] && IP.sameNet(L[cname], p.net.split('/')[0], +p.net.split('/')[1])) return { ip: L[cname], len: +p.net.split('/')[1], gw: p.gw };
    var used = Object.keys(L).map(function (k) { return L[k]; });
    for (var n = IP.ip2n(p.range[0]); n <= IP.ip2n(p.range[1]); n++) {
      var ip = IP.n2ip(n);
      if (used.indexOf(ip) >= 0 || (net && net.owner(ip))) continue;
      L[cname] = ip; return { ip: ip, len: +p.net.split('/')[1], gw: p.gw };
    }
    return null;
  }

  // ------------------------------------------------------------------ время: NTP-клиент ESR
  P.ntpPeer = function (id) {
    var d = this.devs[id], n = d.st.run.ntp;
    if (!n || !n.on) return null;
    var s = this, best = null;
    Object.keys(n.servers).some(function (ip) {
      var r = s.request(id, ip, 'udp', 123);
      if (r.ok) { var sd = s.devs[r.dev]; best = { ip: ip, utc: EL.clock.now() + (sd.st.clk || 0), poll: Math.pow(2, n.servers[ip].maxpoll) }; return true; }
      return false;
    });
    return best || { ip: Object.keys(n.servers)[0], utc: null };
  };
  P.esrUtc = function (id) { var p = this.ntpPeer(id); return p && p.utc !== null ? p.utc : EL.clock.now() + (this.devs[id].st.clk || 0); };
  P.ntpText = function (id) {
    var p = this.ntpPeer(id);
    if (!p) return '% NTP выключен — ntp enable';
    if (!p.ip) return '% NTP-серверы не заданы — ntp server A.B.C.D';
    var ok = p.utc !== null;
    return (ok ? 'Clock is synchronized, stratum 9, reference is ' + p.ip : 'Clock is unsynchronized') + '\n' +
      '     remote                 refid            st  t  when  poll  reach   delay\n' +
      '------------------------- ---------------- --- -- ----- ----- ------ -------\n' +
      (ok ? '*' : ' ') + '    ' + (p.ip + '                    ').slice(0, 20) + (ok ? '127.127.1.1      8   u  1     ' + p.poll + '    255    0.641' : '.INIT.           16  u  -     64    0      0.000');
  };

  // ------------------------------------------------------------------ текстовые выводы
  P.pingText = function (id, dst, style) {
    var r = this.ping(id, dst), n = 5, o = [];
    if (this.onTrace) this.onTrace(r, id, dst);
    if (IP.ip2n(dst) === null) return style === 'linux' ? 'ping: ' + dst + ': Name or service not known' : '% Неверный адрес';
    if (style === 'vpc') { for (var i = 1; i <= n; i++) o.push(r.ok ? '84 bytes from ' + dst + ' icmp_seq=' + i + ' ttl=' + (64 - r.hops.length + 1) + ' time=' + (0.5 + i * 0.13).toFixed(3) + ' ms'
                                                               : (r.why === 'Host unreachable' || r.why === 'No IP address' ? 'host (' + dst + ') not reachable' : dst + ' icmp_seq=' + i + ' timeout'));
      return o.join('\n'); }
    if (style === 'linux') {
      o.push('PING ' + dst + ' (' + dst + ') 56(84) bytes of data.');
      for (var j = 1; j <= 4; j++) if (r.ok) o.push('64 bytes from ' + dst + ': icmp_seq=' + j + ' ttl=' + (64 - r.hops.length + 1) + ' time=0.' + (600 + j * 37) + ' ms');
      if (!r.ok && /unreach/i.test(r.why || '')) o.push('From ' + (this.ifaces(id)[0] || { ip: dst }).ip + ' icmp_seq=1 Destination Host Unreachable');
      if (!r.ok && /No IP/.test(r.why || '')) return 'ping: connect: Network is unreachable';
      o.push('', '--- ' + dst + ' ping statistics ---', '4 packets transmitted, ' + (r.ok ? 4 : 0) + ' received, ' + (r.ok ? '0' : '100') + '% packet loss, time 3004ms');
      return o.join('\n');
    }
    if (style === 'esr') {
      o.push('PING ' + dst + ' (' + dst + ') 56(84) bytes of data.', r.ok ? '!!!!!' : '.....', '--- ' + dst + ' ping statistics ---',
             '5 packets transmitted, ' + (r.ok ? 5 : 0) + ' received, ' + (r.ok ? '0' : '100') + '% packet loss, time 4005ms');
      return o.join('\n');
    }
    for (var k = 1; k <= n; k++) o.push(r.ok ? 'Reply Received From :' + dst + ', TimeTaken : ' + k + ' msecs' : 'Reply Not Received From : ' + dst + ', Timeout : 5 secs');
    o.push('', '--- ' + dst + ' Ping Statistics ---', n + ' Packets Transmitted, ' + (r.ok ? n : 0) + ' Packets Received, ' + (r.ok ? '0' : '100') + '% Packets Loss');
    return o.join('\n');
  };
  P.traceText = function (id, dst) {
    if (IP.ip2n(dst) === null) return 'usage: traceroute A.B.C.D';
    var r = this.ping(id, dst);
    if (this.onTrace) this.onTrace(r, id, dst);
    var o = ['traceroute to ' + dst + ', 30 hops max'];
    (r.hops || []).forEach(function (h, i) { o.push(' ' + (i + 1) + '  ' + h.ip + '  0.' + (400 + i * 90) + ' ms'); });
    if (!r.ok) o.push(' ' + ((r.hops || []).length + 1) + '  * * *');
    return o.join('\n');
  };
  P.arpText = function (id) {
    var s = this, a = this.arp[id], ks = Object.keys(a);
    return ks.length ? ks.map(function (ip) { return a[ip].mac + '  ' + ip + ' expires in ' + s.ttl(id, 'a', a[ip]) + ' seconds'; }).join('\n') : 'arp table is empty';
  };
  P.macTable = function (id) {
    var t = this.mac[id], o = ['Vlan    Mac Address         Type      Ports', '----    -----------         ----      -----'];
    Object.keys(t).forEach(function (k) { var x = t[k]; o.push((x.vlan + '        ').slice(0, 8) + x.mac + '   ' + (x.st ? 'Static ' : x.sec ? 'Secure ' : 'Learnt ') + '   ' + x.port); });
    var sm = this.devs[id].st.smac || {};
    Object.keys(sm).forEach(function (k) { var x = sm[k]; o.push((x.vlan + '        ').slice(0, 8) + x.mac + '   Static    ' + x.port); });
    return o.join('\n') + '\nTotal Mac Addresses displayed: ' + (Object.keys(t).length + Object.keys(sm).length);
  };

  // ------------------------------------------------------------------ SSH с компьютера Debian
  P.sshOpen = function (hst, user, ip) {
    var s = this, own = this.owner(ip);
    var r = this.request(hst.dev, ip, 'tcp', 22);
    if (!r.ok && r.why === 'Connection refused') return 'ssh: connect to host ' + ip + ' port 22: Connection refused';
    if (!r.ok) return 'ssh: connect to host ' + ip + ' port 22: No route to host';
    var d = this.devs[own], st = d.st;
    var on = d.type === 'esr' ? st.run.ssh : d.type === 'mes' ? st.ssh && st.rsa : false;
    if (!on) return 'ssh: connect to host ' + ip + ' port 22: Connection refused';
    var users = d.type === 'esr' ? st.run.users : st.users, banner = d.type === 'esr' ? st.run.banner : st.banner;
    var sess = { stage: 'pw', mode: d.type === 'esr' ? 'priv' : 'priv', ctx: null };
    function swap(fn) { var m = st.mode, c = st.ctx; st.mode = sess.mode; st.ctx = sess.ctx; var r2 = fn(); sess.mode = st.mode; sess.ctx = st.ctx; st.mode = m; st.ctx = c; return r2; }
    sess.prompt = function () {
      if (sess.stage === 'pw') return user + '@' + ip + "'s password: ";
      return swap(function () { return d.type === 'esr' ? EL.esr.prompt(st) : EL.mes.prompt(st); });
    };
    sess.exec = function (line) {
      if (sess.stage === 'pw') {
        var u = users[user];
        if (!u || u.pw !== line.trim()) { hst.ssh = null; return 'Permission denied, please try again.\n' + user + '@' + ip + ': Permission denied (publickey,password).'; }
        sess.stage = 'cli'; var o = [];
        if (d.type === 'esr') s.syslog(own, 'login.log', 'sshd: %AAA-I-LOGIN: user ' + user + ' logged in via ssh from ' + (s.ifaces(hst.dev)[0] || { ip: '?' }).ip);
        if (banner.login) o.push(banner.login);
        if (banner.exec) o.push(banner.exec);
        return o.join('\n');
      }
      if (/^\s*exit\s*$/i.test(line) && (sess.mode === 'priv' || sess.mode === 'user')) { hst.ssh = null; return 'Connection to ' + ip + ' closed.'; }
      return swap(function () { return d.type === 'esr' ? EL.esr.exec(st, line) : EL.mes.exec(st, line); });
    };
    hst.ssh = sess;
    return 'The authenticity of host \'' + ip + ' (' + ip + ')\' can\'t be established.\nECDSA key fingerprint is SHA256:' +
      EL.E.hash(ip).slice(0, 32) + '.\nWarning: Permanently added \'' + ip + '\' (ECDSA) to the list of known hosts.';
  };


  // ------------------------------------------------------------------ LLDP, syslog, TFTP, зеркалирование
  P.lldpText = function (id) {
    var s = this, d = this.devs[id], c = d.st.run, o = [];
    if (!c.lldp) return '% LLDP выключен — lldp enable';
    Object.keys(c.ifs).forEach(function (k) {
      var x = c.ifs[k]; if (k.indexOf('.') > 0 || k.charAt(0) === 'l' || !x.lldpRx) return;
      var pr = s.peer(id, k); if (!pr || !s.linkUp(id, k)) return;
      var nd = s.devs[pr.dev];
      if (nd.type !== 'esr' || !nd.st.run.lldp || !(nd.st.run.ifs[pr.port] || {}).lldpTx) return;
      o.push((k + '          ').slice(0, 10) + (EL.mac(nd.st.run.host + 'sys') + '   ').slice(0, 20) + (pr.port + '          ').slice(0, 12) +
             (nd.st.run.host + '              ').slice(0, 15) + 'R             120');
    });
    return ['Port      Device ID           Port ID     System name    Capabilities  TTL', '--------  ------------------  ----------  -------------  ------------  ---']
      .concat(o.length ? o : ['% Соседей нет: LLDPDU не приходят (lldp enable, lldp receive у нас, lldp transmit у соседа, commit)']).join('\n');
  };
  P.tftpPut = function (id, ip, file, content) {
    var r = this.request(id, ip, 'udp', 69);
    if (!r.ok) return { ok: false, why: r.why === 'Connection refused' ? 'на ' + ip + ' не запущен TFTP-сервер' : 'сервер ' + ip + ' недоступен' };
    this.devs[r.dev].st.files['/tftp/' + file] = content;
    return { ok: true, size: content.length };
  };
  function nowStr() { var d = new Date(); return d.toISOString().slice(0, 19).replace('T', ' '); }
  P.syslog = function (id, file, msg) {
    var s = this, c = this.devs[id].st.run;
    Object.keys(c.syslog || {}).forEach(function (n) { var h = c.syslog[n]; if (!h.ip) return;
      var r = s.request(id, h.ip, h.proto === 'tcp' ? 'tcp' : 'udp', h.port);
      if (!r.ok) return;
      var f = s.devs[r.dev].st.files, k = '/var/log/rsyslog/' + c.host + '/' + file;
      f[k] = (f[k] ? f[k] + '\n' : '') + nowStr() + ' ' + c.host + ' ' + msg; });
  };
  P.afterEsr = function (id, line, out, c0) {
    var st = this.devs[id].st, c = st.run, cmdl = String(line).trim();
    if (cmdl && !/^%/.test(out || '')) this.syslog(id, 'klish.log', 'klish: %CLI-I-CMD: user admin: ' + cmdl);
    if ((st.commits || 0) > c0) {
      this.syslog(id, 'klish.log', 'klish: %CONFIG-I-COMMIT: configuration committed');
      var a = c.archive, u = a && a.byCommit && a.type === 'remote' && a.path && EL.tftpUrl(a.path);
      if (u) this.tftpPut(id, u.ip, u.file, EL.esr.showRun(st));
    }
  };
  P.mirror = function (path, pk) {
    var s = this;
    path.forEach(function (sg) {
      var l = s.links[sg.li]; if (!l) return;
      var fromP = l.a.dev === sg.from ? l.a.port : l.b.port, toP = l.a.dev === sg.to ? l.a.port : l.b.port;
      [[sg.from, fromP, 'tx'], [sg.to, toP, 'rx']].forEach(function (x) {
        var d = s.devs[x[0]]; if (!d || d.type !== 'mes' || !d.st.mon) return;
        Object.keys(d.st.mon).forEach(function (n) { var m = d.st.mon[n], dir = m.src[x[1]];
          if (!m.dst || !dir || (dir !== 'both' && dir !== x[2]) || (d.st.dialect === '8' && !m.on)) return;
          var pr = s.peer(x[0], m.dst); if (!pr) return; var cap = s.devs[pr.dev];
          if (cap.type !== 'deb') return;
          cap.st.capN = (cap.st.capN || 0) + 1;
          cap.st.cap.push(new Date().toTimeString().slice(0, 8) + ' IP ' + pk.src + ' > ' + pk.dst + ': ' +
            (pk.proto === 'icmp' ? 'ICMP echo' : pk.proto.toUpperCase() + (pk.dport ? ' port ' + pk.dport : '')) + '   (копия с ' + d.name + ' ' + x[1] + ', ' + x[2] + ')');
        });
      });
    });
  };


  // MAC интерфейса устройства и обучение коммутаторов на пути кадра
  P.ifMac = function (id, f) {
    var d = this.devs[id];
    if (f.vrrp) { var v = (this.vrrp()[id] || {})[f.name.split(':')[0]];      // виртуальный MAC VRRP: 00:00:5e:00:01:ID
      return '00:00:5e:00:01:' + ('0' + (v ? v.id : 0).toString(16)).slice(-2); }
    return EL.mac(d.name + (f.port || f.name.split(':')[0]));
  };
  P.learn = function (path, mac) {
    var s = this, viol = null;
    path.forEach(function (sg) {
      var d = s.devs[sg.to]; if (!d || d.type !== 'mes' || viol) return;
      var l = s.links[sg.li]; if (!l) return;
      var port = l.a.dev === sg.to ? l.a.port : l.b.port, L = s.lportOf(sg.to, port); if (!L) return;
      var c = L.cfg, v = sg.tag !== null ? sg.tag : (c.mode === 'access' ? c.access : c.mode === 'trunk' ? c.native : c.pvid);
      viol = s.macIn(sg.to, L.name, v, mac);
    });
    return viol;
  };
  // запись MAC отправителя на входном порту; модуль mes_full добавляет port security и статические записи
  P.macIn = function (dev, port, v, mac) { this.mac[dev][v + '|' + mac] = { vlan: v, mac: mac, port: port, t: this.now }; return null; };

  // журнал шагов трассы: к каждому шагу прикладывается, что изменилось в ARP/MAC-таблицах с прошлого шага
  P.tabSnap = function () {
    var s = this, o = {};
    Object.keys(s.arp).forEach(function (d) { Object.keys(s.arp[d]).forEach(function (k) { o['a|' + d + '|' + k] = noT(s.arp[d][k]); }); });
    Object.keys(s.mac).forEach(function (d) { Object.keys(s.mac[d]).forEach(function (k) { o['m|' + d + '|' + k] = noT(s.mac[d][k]); }); });
    return o;
  };
  // время записи (t) в сравнение не входит: обновление таймера — не новая запись
  function noT(x) { return JSON.stringify(x, function (k, v) { return k === 't' ? undefined : v; }); }
  function tabDiff(a, b) {
    var out = [];
    Object.keys(b).forEach(function (k) { if (a[k] !== b[k]) out.push({ k: k, o: a[k] || null, n: b[k] }); });
    Object.keys(a).forEach(function (k) { if (!(k in b)) out.push({ k: k, o: a[k], n: null }); });
    return out;
  }
  P.stepLog = function () {
    var s = this, prev = s.tabSnap(), arr = [];
    function take() { var now = s.tabSnap(), d = tabDiff(prev, now); prev = now; return d; }
    arr.push = function (st) { st.tab = take(); return Array.prototype.push.call(this, st); };
    arr.flush = function () { var d = take(); if (this.length && d.length) this[this.length - 1].tab = this[this.length - 1].tab.concat(d); };
    return arr;
  };
  P.clearTables = function (id) { this.arp[id] = {}; this.mac[id] = {}; };

  // ------------------------------------------------------------------ сохранение схемы
  // питание и перезагрузка (как Start/Stop/Reload в pnetlab)
  P.power = function (id, on) { this.devs[id].off = !on; this.gen++; };
  P.reboot = function (id) {
    var d = this.devs[id], st = d.st;
    if (d.type === 'esr') { st.cand = EL.clone(st.run); st.pending = false; st.unconfirmed = false; st.mode = 'priv'; st.ctx = null; }
    if (d.type === 'mes') { st.mode = 'priv'; EL.mes.exec(st, 'reload'); }
    if (d.type === 'vpc') { st.ip = null; st.gw = null; st.dhcp = false; }
    if (d.type === 'deb') { st.user = st.browser ? 'root' : null; st.login = 'user'; st.ssh = null; st.up = false; st.ip = null; st.gw = null; }
    this.mac[id] = {}; this.arp[id] = {}; d.off = false; this.gen++;
  };
  P.rename = function (id, name) {
    name = String(name || '').trim();
    if (!/^[\w.-]{1,24}$/.test(name)) return 'Имя: латиница, цифры, - _ . (до 24 символов)';
    var o = this.byName(name); if (o && o.id !== id) return 'Имя ' + name + ' уже занято';
    var d = this.devs[id]; d.name = name; if (d.st.kind === 'vpc') d.st.name = name; return null;
  };
  P.toJSON = function () {
    var s = this;
    return { v: 1, devs: this.list().map(function (d) { return { name: d.name, model: d.model, x: d.x, y: d.y, st: d.st }; }),
             links: this.links.map(function (l) { return [s.devs[l.a.dev].name, l.a.port, s.devs[l.b.dev].name, l.b.port]; }) };
  };
  Net.fromJSON = function (j) {
    var n = new Net();
    if (!j || j.v !== 1 || !Array.isArray(j.devs)) throw new Error('Файл не похож на схему эмулятора');
    j.devs.forEach(function (x) { var d = n.add(x.model, x.name, x.x, x.y);
      if (x.st && x.st.kind === d.st.kind || x.st && x.st.kind === undefined) { d.st = x.st; d.st.ssh = null; EL.attach(d.st, n, d.id); } });
    j.links.forEach(function (l) { var a = n.byName(l[0]), b = n.byName(l[2]); if (a && b) n.connect(a.id, l[1], b.id, l[3]); });
    return n;
  };

  // ------------------------------------------------------------------ единая точка ввода команды на устройство
  P.exec = function (id, line, ui) {
    this.gen++;
    var d = this.devs[id], st = d.st;
    if (d.off) return '';
    if (st.askPw) { var a = st.askPw; st.askPw = null; if (line === a.pw) { a.ok(); return ''; } return '% Access denied'; }
    if (/\?\s*$/.test(line) && (d.type === 'mes' || d.type === 'esr')) return this.help(id, line.replace(/\?\s*$/, ''));
    if (d.type === 'mes') return EL.mes.exec(st, line);
    if (d.type === 'esr') { var c0 = st.commits || 0, out = EL.esr.exec(st, line); this.afterEsr(id, line, out, c0); return out; }
    if (d.type === 'vpc') return H.vpcExec(st, line);
    return H.debExec(st, line, ui);
  };
  P.prompt = function (id) {
    var d = this.devs[id], st = d.st;
    if (st.askPw) return 'Password: ';
    if (d.type === 'mes') return EL.mes.prompt(st);
    if (d.type === 'esr') return EL.esr.prompt(st);
    if (d.type === 'vpc') return H.vpcPrompt(st);
    return H.debPrompt(st);
  };
  P.table = function (id, line) {
    var d = this.devs[id];
    if (d.type === 'mes') return { T: EL.mes.T, mode: d.st.mode, raw: line };
    if (d.type === 'esr') { var h = EL.esr.helpTable(d.st, line); return { T: EL.esr.T, mode: h.mode, raw: h.raw, pre: line.slice(0, line.length - h.raw.length) }; }
    if (d.type === 'deb' && d.st.ssh) return null;
    return null;
  };
  P.help = function (id, line) { var t = this.table(id, line); return t ? EL.cli.help(t.T, t.mode, t.raw, this.devs[id].st) : ''; };
  P.tab = function (id, line) { var t = this.table(id, line); if (!t) return null; var r = EL.cli.tab(t.T, t.mode, t.raw, this.devs[id].st); return r === null ? null : (t.pre || '') + r; };

  EL.Net = Net; EL.MODELS = MODELS; EL.egress = egress;
})(typeof window !== 'undefined' ? window : global);
