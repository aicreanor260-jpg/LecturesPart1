/* Модель сети: устройства, кабели, прохождение кадров по VLAN/trunk/general, ARP, маршрутизация, межсетевой экран ESR.
   Каждая отправка пакета возвращает пошаговую трассу — её проигрывает интерфейс («как идут пакеты»). */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, H = EL.hosts;

  // каталог: только модели с CLI, совместимым с движком (MES14xx/24xx/3400/37xx — одна ветка ПО 10.4.x)
  // коммутаторы — из каталога eltex.ru (catalog.js, ветка ПО 10.x: тот же CLI, что у движка); нумерация портов упрощена до gi1/0/1–N
  var MODELS = {};
  Object.keys(EL.CATALOG || {}).forEach(function (k) { MODELS[k] = EL.CATALOG[k]; });
  MODELS.vESR = { type: 'esr', ports: 8, group: 'Маршрутизаторы ESR', note: 'Виртуальный сервисный маршрутизатор, 8 × gigabitethernet' };
  MODELS.VPC = { type: 'vpc', ports: 1, group: 'Конечные узлы', note: 'Виртуальный ПК (как VPCS в pnetlab)' };
  MODELS.Debian = { type: 'deb', ports: 1, group: 'Конечные узлы', note: 'Компьютер с Debian 11: ip, ifup, nano, ping, ssh' };

  function Net() { this.devs = {}; this.order = []; this.links = []; this.mac = {}; this.arp = {}; this.onTrace = null; }
  var P = Net.prototype;

  P.portsOf = function (d) {
    var m = MODELS[d.model];
    if (d.type === 'vpc') return ['eth0'];
    if (d.type === 'deb') return ['ens3'];
    var o = []; for (var i = 1; i <= m.ports; i++) o.push('gi1/0/' + i); return o;
  };
  P.add = function (model, name, x, y) {
    var m = MODELS[model]; if (!m) throw new Error('Нет модели ' + model);
    if (!name) { var n = 1, base = { mes: 'SW', esr: 'R', vpc: 'VPC', deb: 'Debian' }[m.type];
      while (this.byName(base + n)) n++; name = base + n; }
    if (this.byName(name)) throw new Error('Имя ' + name + ' занято');
    var id = 'd' + (++Net.seq);
    var d = { id: id, name: name, model: model, type: m.type, x: x || 0, y: y || 0 };
    if (m.type === 'mes') d.st = EL.mes.fresh(m.ports, 'switch');
    if (m.type === 'esr') d.st = EL.esr.fresh('vesr', m.ports);
    if (m.type === 'vpc') d.st = H.vpc(name);
    if (m.type === 'deb') d.st = H.deb(name);
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
      var out = fs.filter(function (f) { return (f.port !== null || f.vlan) && IP.sameNet(r.nh, f.ip, f.len); })[0];
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
    if (this._dyn && this._dyn.gen === this.gen) return this._dyn.t;
    var s = this, t = {};
    this._dyn = { gen: this.gen, t: t };     // защита от повторного входа: flood не зависит от динамических маршрутов
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
            part.push({ f: f, passive: !!o.passive, area: o.area, cost: o.cost || 1 }); orig.push(IP.netOf(f.ip, f.len));
          }
        });
        if (proto === 'R' && c.rip.redist.indexOf('static') >= 0) c.routes.forEach(function (r) { orig.push(r.net); });
        info[id] = { part: part, nb: [] };
        tab[id] = {}; orig.forEach(function (n) { tab[id][n] = { m: 0, nh: null, ifn: null, own: true }; });
      });
      rs.forEach(function (id) {               // соседи — через L2, как реальные hello/update
        info[id].part.forEach(function (pp) {
          if (pp.passive || pp.f.port === null) return;
          s.flood(id, pp.f).eps.forEach(function (e) {
            var oi = info[e.dev]; if (!oi || e.dev === id) return;
            var op = oi.part.filter(function (q) { return q.f.name === e.iface.name && !q.passive; })[0];
            if (!op || !IP.sameNet(pp.f.ip, e.iface.ip, pp.f.len)) return;
            if (proto === 'O' && op.area !== pp.area) return;
            info[id].nb.push({ dev: e.dev, nh: e.iface.ip, ifn: pp.f.name, cost: proto === 'R' ? 1 : pp.cost });
          });
        });
      });
      for (var round = 0; round < 20; round++) {
        var ch = false;
        rs.forEach(function (id) {
          info[id].nb.forEach(function (nb) {
            Object.keys(tab[nb.dev]).forEach(function (n) {
              var m2 = tab[nb.dev][n].m + nb.cost, cur = tab[id][n];
              if (proto === 'R' && m2 > 15) return;
              if (cur && (cur.own || cur.m <= m2)) return;
              tab[id][n] = { m: m2, nh: nb.nh, ifn: nb.ifn }; ch = true;
            });
          });
        });
        if (!ch) break;
      }
      rs.forEach(function (id) {
        t[id] = (t[id] || []).concat(Object.keys(tab[id]).filter(function (n) { return !tab[id][n].own; }).map(function (n) {
          var x = tab[id][n]; return { p: proto, net: n, len: +n.split('/')[1], nh: x.nh, ifn: x.ifn, ad: proto === 'R' ? 120 : 110, m: x.m }; }));
        if (proto === 'O') s.devs[id]._ospfNb = info[id].nb;
      });
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
    if (d.type === 'mes') return !!d.st.ports[p].shut;
    if (d.type === 'esr') return !!d.st.run.ifs[p].shut;
    if (d.type === 'deb') return !d.st.up;
    return false;
  }
  P.owner = function (ip) {
    var s = this; return this.order.filter(function (id) { return s.ifaces(id).some(function (f) { return f.ip === ip; }); })[0] || null;
  };
  function owns(net, id, ip) { return net.ifaces(id).some(function (f) { return f.ip === ip; }); }

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
  function ingress(st, port, tag) {
    var p = st.ports[port];
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
    var s = this, seen = {}, eps = [], segs = [], notes = [], q = [];
    function send(dev, port, tag, path) {
      var pr = s.peer(dev, port); if (!pr) return;
      var seg = { li: pr.li, from: dev, to: pr.dev, tag: tag };
      segs.push(seg); q.push({ dev: pr.dev, port: pr.port, tag: tag, path: path.concat([seg]) });
    }
    function inMes(dev, inPort, v, path) {
      var st = s.devs[dev].st;
      if (inPort && srcMac) s.mac[dev][v + '|' + srcMac] = { vlan: v, mac: srcMac, port: inPort };
      Object.keys(st.svi).forEach(function (sv) { if (+sv === v && EL.mes.sviUp(st, v) && !(dev === id && f.vlan === v)) {
        var p = st.svi[sv].split('/'); eps.push({ dev: dev, iface: { name: 'vlan' + v, ip: p[0], len: +p[1], vlan: v }, path: path }); } });
      s.portsOf(s.devs[dev]).forEach(function (q2) {
        if (q2 === inPort || !s.linked(dev, q2)) return;
        var e = egress(st.ports[q2], v); if (e) send(dev, q2, e === 't' ? v : null, path);
      });
    }
    if (f.vlan) inMes(id, null, f.vlan, []);
    else if (f.port) send(id, f.port, f.tag, []);
    while (q.length) {
      var it = q.shift(), key = it.dev + '|' + it.port + '|' + it.tag;
      if (seen[key]) continue; seen[key] = 1;
      var d = this.devs[it.dev], nm = d.name;
      if (d.type === 'mes') {
        var r = ingress(d.st, it.port, it.tag);
        if (r.drop) { notes.push(nm + ': ' + r.drop); continue; }
        inMes(it.dev, it.port, r.v, it.path);
      } else if (d.type === 'esr') {
        var phys = d.st.run.ifs[it.port];
        if (phys.shut) { notes.push(nm + ': интерфейс ' + it.port + ' выключен'); continue; }
        var k = it.tag === null ? it.port : it.port + '.' + it.tag, x = d.st.run.ifs[k];
        if (!x) { notes.push(nm + ': нет саб-интерфейса ' + it.port + '.' + it.tag + ' — кадр с тегом ' + it.tag + ' отброшен'); continue; }
        if (!x.ip || x.shut) { notes.push(nm + ': на ' + k + ' нет IP-адреса или он выключен'); continue; }
        var pp = x.ip.split('/');
        eps.push({ dev: it.dev, iface: { name: k, ip: pp[0], len: +pp[1], port: it.port, tag: it.tag, fw: x.fw }, path: it.path });
      } else {
        if (it.tag !== null) { notes.push(nm + ': пришёл кадр с тегом ' + it.tag + ' — ПК тегов не понимает, отброшен'); continue; }
        var hf = this.ifaces(it.dev)[0];
        if (!hf) { notes.push(nm + ': на интерфейсе нет IP-адреса' + (d.type === 'deb' && !d.st.up ? ' (ens3 выключен)' : '')); continue; }
        eps.push({ dev: it.dev, iface: hf, path: it.path });
      }
    }
    return { eps: eps, segs: segs, notes: notes };
  };

  // ------------------------------------------------------------------ отправка IP-пакета (в одну сторону)
  P.send = function (src, dst, steps) {
    var cur = src, ttl = 16, first = null, hops = [];
    while (ttl-- > 0) {
      var cd = this.devs[cur];
      if (owns(this, cur, dst)) return { ok: true, dev: cur, srcIp: first, hops: hops };
      var r = this.lookup(cur, dst);
      if (!r) { steps.push({ k: 'drop', t: cd.name + ': нет маршрута до ' + dst + (cd.type === 'vpc' || cd.type === 'deb' ? ' (не задан шлюз или адрес)' : '') });
        return { ok: false, why: 'Destination net unreachable', first: first }; }
      if (!first) first = r.iface.ip;
      var srcMac = EL.mac(cd.name + (r.iface.port || r.iface.name));
      var fl = this.flood(cur, r.iface, srcMac);
      var ep = fl.eps.filter(function (e) { return e.iface.ip === r.nh; })[0];
      var vl = r.iface.vlan || r.iface.tag;
      steps.push({ k: 'arp', segs: fl.segs, t: cd.name + ' (' + r.iface.name + ', ' + r.iface.ip + '): ARP-запрос «у кого ' + r.nh + '?» — широковещательно' +
        (vl ? ' в VLAN ' + vl : '') + (r.nh !== dst ? ' (это шлюз к ' + dst + ')' : ''), notes: fl.notes });
      if (!ep) { steps.push({ k: 'drop', t: 'Нет ответа на ARP: ' + r.nh + ' недоступен в этом широковещательном домене', notes: fl.notes });
        return { ok: false, why: 'Host unreachable', first: first }; }
      var nd = this.devs[ep.dev];
      this.arp[cur][r.nh] = { mac: EL.mac(nd.name + (ep.iface.port || ep.iface.name)), ifn: r.iface.name };
      var back = ep.path.slice().reverse().map(function (sg) { return { li: sg.li, from: sg.to, to: sg.from, tag: sg.tag }; });
      steps.push({ k: 'arpr', segs: back, t: nd.name + ' (' + ep.iface.name + '): ARP-ответ «' + r.nh + ' — это я, MAC ' + this.arp[cur][r.nh].mac + '»' });
      steps.push({ k: 'ip', segs: ep.path, t: cd.name + ' → ' + nd.name + ': пакет ' + first + ' → ' + dst + ' в кадре до MAC ' + this.arp[cur][r.nh].mac +
        ep.path.filter(function (s) { return s.tag !== null; }).map(function (s) { return ' · тег 802.1Q ' + s.tag; }).filter(function (x, i, a) { return a.indexOf(x) === i; }).join('') });
      if (nd.type === 'esr' && ep.iface.fw) {
        steps.push({ k: 'drop', t: nd.name + ': межсетевой экран на ' + ep.iface.name + ' включён — пакет отброшен (нужна ip firewall disable или зона безопасности)' });
        return { ok: false, why: 'Request timed out', first: first };
      }
      hops.push({ dev: ep.dev, ip: ep.iface.ip });
      cur = ep.dev;
      if (!owns(this, cur, dst) && (nd.type === 'vpc' || nd.type === 'deb')) {
        steps.push({ k: 'drop', t: nd.name + ' получил чужой пакет и не маршрутизирует его' });
        return { ok: false, why: 'Request timed out', first: first };
      }
      if (!owns(this, cur, dst)) steps.push({ k: 'route', t: nd.name + ': адрес ' + dst + ' не мой — ищу маршрут дальше' });
    }
    steps.push({ k: 'drop', t: 'TTL истёк — петля маршрутизации' });
    return { ok: false, why: 'Time to live exceeded', first: first };
  };
  // ping туда и обратно
  P.ping = function (src, dst) {
    var steps = [], d = this.devs[src];
    if (IP.ip2n(dst) === null) return { ok: false, why: 'Bad address', steps: steps };
    if (!this.ifaces(src).length) { steps.push({ k: 'drop', t: d.name + ': нет ни одного IP-адреса' }); return { ok: false, why: 'No IP address', steps: steps }; }
    var f = this.send(src, dst, steps);
    if (!f.ok) return { ok: false, why: f.why, steps: steps };
    if (f.dev === src) return { ok: true, steps: steps, hops: [] };
    steps.push({ k: 'ok', t: this.devs[f.dev].name + ' получил ICMP echo request и отвечает echo reply' });
    var b = this.send(f.dev, f.srcIp, steps);
    if (!b.ok) { steps.push({ k: 'drop', t: 'Ответ не вернулся к ' + d.name + ' — проверьте маршрут/шлюз в обратную сторону' });
      return { ok: false, why: 'Request timed out', steps: steps }; }
    steps.push({ k: 'ok', t: d.name + ' получил echo reply от ' + dst });
    return { ok: true, steps: steps, hops: f.hops };
  };
  P.reach = function (srcName, dst) { var d = this.byName(srcName); return !!d && this.ping(d.id, dst).ok; };

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
    var a = this.arp[id], ks = Object.keys(a);
    return ks.length ? ks.map(function (ip) { return a[ip].mac + '  ' + ip + ' expires in 120 seconds'; }).join('\n') : 'arp table is empty';
  };
  P.macTable = function (id) {
    var t = this.mac[id], o = ['Vlan    Mac Address         Type      Ports', '----    -----------         ----      -----'];
    Object.keys(t).forEach(function (k) { var x = t[k]; o.push((x.vlan + '        ').slice(0, 8) + x.mac + '   Learnt    ' + x.port); });
    return o.join('\n') + '\nTotal Mac Addresses displayed: ' + Object.keys(t).length;
  };

  // ------------------------------------------------------------------ SSH с компьютера Debian
  P.sshOpen = function (hst, user, ip) {
    var s = this, own = this.owner(ip);
    var r = this.ping(hst.dev, ip);
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

  // ------------------------------------------------------------------ сохранение схемы
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
    if (st.askPw) { var a = st.askPw; st.askPw = null; if (line === a.pw) { a.ok(); return ''; } return '% Access denied'; }
    if (/\?\s*$/.test(line) && (d.type === 'mes' || d.type === 'esr')) return this.help(id, line.replace(/\?\s*$/, ''));
    if (d.type === 'mes') return EL.mes.exec(st, line);
    if (d.type === 'esr') return EL.esr.exec(st, line);
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
  P.help = function (id, line) { var t = this.table(id, line); return t ? EL.cli.help(t.T, t.mode, t.raw) : ''; };
  P.tab = function (id, line) { var t = this.table(id, line); if (!t) return null; var r = EL.cli.tab(t.T, t.mode, t.raw); return r === null ? null : (t.pre || '') + r; };

  EL.Net = Net; EL.MODELS = MODELS; EL.egress = egress;
})(typeof window !== 'undefined' ? window : global);
