/* «Отказы» (режим «Тест»; проект sources/huawei/failure-analysis-design.md): внести отказ и вычислить последствия.
   Всё считается на копии схемы (Net.fromJSON + питание и свойства кабелей), исходная схема и её таблицы ARP/MAC/таймеры не меняются.
   Отказы: обрыв кабеля, выключение устройства, выключение порта, ошибка конфигурации (меняет поля модели, поэтому
   одинаково работает для Eltex и Huawei). Результат:
     — матрица связности «кто с кем» между узлами с IP (VPC, Debian, серверы; по желанию — адреса маршрутизаторов и SVI)
       до отказа, сразу после (+1 с) и после схождения (+300 с: RSTP/STP, OSPF dead 40 с, RIP invalid 180 с / flush 240 с);
     — пары, которые потеряли связь, восстановились или пошли другим путём (путь — цепочка устройств по кабелям);
     — что перестроилось: роли портов STP, лучшие маршруты (протокол, next-hop), мастер VRRP, члены агрегатов;
     — единые точки отказа: перебор всех одиночных отказов (кабели и устройства, кроме конечных узлов). */
(function (G) {
  'use strict';
  var EL = G.EL, Net = EL.Net;
  var CONV = 300, STEP = 10;

  // ---------------------------------------------------------------- копия схемы и модельное время
  function copy(net) {
    var c = Net.fromJSON(JSON.parse(JSON.stringify(net.toJSON())));
    net.links.forEach(function (l, i) { var k = c.links[i]; if (!k) return; Object.keys(l).forEach(function (f) { if (f !== 'a' && f !== 'b') k[f] = EL.clone(l[f]); }); });
    net.list().forEach(function (d) { var x = c.byName(d.name, true); if (x && d.off) x.off = true; });
    c.now = 0; c.gen++;
    return c;
  }
  function observe(n) {                          // «опросить» модель: протоколы и STP обновляют своё состояние на текущий момент
    n.gen++; n.dyn();
    n.list().forEach(function (d) { if (d.type !== 'mes' || d.off) return; n.lports(d.id).forEach(function (L) { n.stpSts(d.id, L.name, 0); }); });
    n.vrrp();
  }
  function run(n, sec) { for (var t = 0; t < sec; t += STEP) { n.tick(Math.min(STEP, sec - t)); observe(n); } }
  function warm(net) { var c = copy(net); observe(c); run(c, CONV); return c; }

  // ---------------------------------------------------------------- узлы матрицы и связность
  function nodes(n, routers) {
    var o = [];
    n.list().forEach(function (d) { if (d.off) return; var end = d.type === 'vpc' || d.type === 'deb';
      if (!end && !routers) return;
      n.ifaces(d.id).forEach(function (f, i) { if (f.vrrp || f.tun || /^lo/.test(f.name) && !routers) return; if (end && i > 0) return;
        o.push({ dev: d.name, ip: f.ip, label: end ? d.name : d.name + ' ' + f.ip }); }); });
    return o;
  }
  function linkName(n, li) { var l = n.links[li]; if (!l) return '?'; var a = n.devs[l.a.dev].name + ':' + l.a.port, b = n.devs[l.b.dev].name + ':' + l.b.port; return a < b ? a + '—' + b : b + '—' + a; }
  function pathOf(n, r) {                        // цепочка устройств запроса (кадры IP «туда»)
    var chain = [], links = [];
    (r.steps || []).forEach(function (s) { if (s.k !== 'ip' || !s.f || s.f.reply) return;
      (s.segs || []).forEach(function (g) { var a = n.devs[g.from], b = n.devs[g.to]; if (!a || !b) return;
        if (!chain.length || chain[chain.length - 1] !== a.name) chain.push(a.name); chain.push(b.name); links.push(linkName(n, g.li)); }); });
    return { chain: chain, sig: links.join('|') };
  }
  function matrix(n, N) {
    var M = {};
    N.forEach(function (s) { var sd = n.byName(s.dev, true); M[s.label] = {};
      N.forEach(function (t) { if (s === t || s.dev === t.dev) return;
        var r = sd && !sd.off ? n.ping(sd.id, t.ip) : { ok: false, why: 'устройство выключено', steps: [] }, p = pathOf(n, r);
        var drop = (r.steps || []).filter(function (x) { return x.k === 'drop'; }).pop();
        M[s.label][t.label] = { ok: !!r.ok, why: r.ok ? '' : (drop ? drop.t : r.why || ''), chain: p.chain, sig: p.sig }; }); });
    return M;
  }
  function cmp(a, b) {                           // ok | lost | reroute | gained | none
    if (a.ok && !b.ok) return 'lost'; if (!a.ok && b.ok) return 'gained'; if (!a.ok && !b.ok) return 'none';
    return a.sig === b.sig ? 'ok' : 'reroute';
  }

  // ---------------------------------------------------------------- снимок состояния протоколов
  var ROLE = { Root: 'Root', Desg: 'Designated', Altn: 'Alternate', Back: 'Backup' };
  function snap(n) {
    var o = { stp: {}, rt: {}, vrrp: {}, lag: {} };
    n.list().forEach(function (d) { if (d.off) return;
      if (d.type === 'mes') { var t = n.stp(0)[d.id] || {};
        n.lports(d.id).forEach(function (L) { var r = t[L.name]; if (r && !r.nostp && !r.host) o.stp[d.name + ' ' + L.name] = (ROLE[r.role] || r.role) + (r.fwd ? '' : ' (блок)');
          if (/^po/.test(L.name)) o.lag[d.name + ' ' + L.name] = L.members.length; }); }
      if (d.type === 'esr' || d.type === 'mes') { var all = n.routes(d.id), by = n.best(d.id, all);
        Object.keys(by).forEach(function (k) { var r = by[k]; if (!r || r.p === 'C') return; o.rt[d.name + ' ' + k] = r.p + (r.nh ? ' через ' + r.nh : ''); }); } });
    var v = n.vrrp(); Object.keys(v).forEach(function (id) { Object.keys(v[id]).forEach(function (k) { var x = v[id][k];
      if (x.master) o.vrrp['VRRP ' + x.id + ' (' + x.vip + ')'] = n.devs[id].name; }); });
    return o;
  }
  function diff(a, b) {
    var out = [];
    [['stp', 'STP'], ['rt', 'Маршрут'], ['vrrp', 'Мастер'], ['lag', 'Агрегат']].forEach(function (k) {
      var A = a[k[0]], B = b[k[0]], keys = Object.keys(A).concat(Object.keys(B)).filter(function (x, i, s) { return s.indexOf(x) === i; }).sort();
      keys.forEach(function (x) { if (A[x] === B[x]) return; out.push({ kind: k[1], what: x, before: A[x] === undefined ? '—' : String(A[x]), after: B[x] === undefined ? '—' : String(B[x]) }); }); });
    return out;
  }

  // ---------------------------------------------------------------- отказы
  // элементы, которые можно «сломать»: кабели, устройства, порты; плюс ошибки конфигурации
  function elements(net) {
    var o = [];
    net.links.forEach(function (l, i) { o.push({ k: 'link', key: linkName(net, i), label: 'Обрыв кабеля ' + linkName(net, i) }); });
    net.list().forEach(function (d) { if (d.type !== 'vpc' && d.type !== 'deb') o.push({ k: 'dev', key: d.name, label: 'Выключение ' + d.name }); });
    return o;
  }
  var CFG = {
    'trunk-vlan': { t: 'Trunk: убрать VLAN из разрешённых', ok: function (d, p) { return d.type === 'mes' && (d.st.ports[p] || {}).mode === 'trunk'; },
      f: function (d, p, v) { var x = d.st.ports[p]; v = v || (x.allowed.filter(function (q) { return q !== x.native; })[0]); x.allowed = x.allowed.filter(function (q) { return q !== +v; }); x.allAll = false; } },
    'native': { t: 'Trunk: другой native VLAN / PVID', ok: function (d, p) { return d.type === 'mes' && (d.st.ports[p] || {}).mode === 'trunk'; },
      f: function (d, p) { var x = d.st.ports[p]; x.native = (x.native || 1) === 1 ? 999 : 1; } },
    'access': { t: 'Access: другой VLAN на порту', ok: function (d, p) { return d.type === 'mes' && (d.st.ports[p] || {}).mode === 'access'; },
      f: function (d, p) { var x = d.st.ports[p]; x.access = x.access === 1 ? 999 : 1; } },
    'stp-mode': { t: 'STP: режим 802.1D (stp) вместо RSTP/MSTP', ok: function (d) { return d.type === 'mes'; }, f: function (d) { d.st.stp.mode = 'stp'; } },
    'mst-name': { t: 'MSTP: другое имя региона', ok: function (d) { return d.type === 'mes'; }, f: function (d) { d.st.mst = d.st.mst || { inst: {} }; d.st.mst.name = 'OTHER'; d.st.stp.mode = 'mst'; } },
    'lacp': { t: 'Агрегат: ручной режим (on/manual) вместо LACP', ok: function (d, p) { return d.type === 'mes' && !!(d.st.ports[p] || {}).cg; },
      f: function (d, p) { var id = d.st.ports[p].cg.id; Object.keys(d.st.ports).forEach(function (k) { var c = d.st.ports[k].cg; if (c && c.id === id) c.mode = c.mode === 'on' ? 'active' : 'on'; }); } },
    'ospf-hello': { t: 'OSPF: hello 5 / dead 20 на интерфейсе', ok: function (d, p) { return d.type === 'esr' && !!((d.st.run.ifs[p] || {}).ospf); },
      f: function (d, p) { var o = d.st.run.ifs[p].ospf; o.hello = 5; o.dead = 20; } },
    'ospf-area': { t: 'OSPF: интерфейс в другой области', ok: function (d, p) { return d.type === 'esr' && !!((d.st.run.ifs[p] || {}).ospf); },
      f: function (d, p) { var c = d.st.run, o = c.ifs[p].ospf; o.area = o.area === '0.0.0.1' ? '0.0.0.0' : '0.0.0.1'; c.ospf.areas[o.area] = { on: true }; } },
    'ospf-p2p': { t: 'OSPF: тип сети point-to-point с одной стороны', ok: function (d, p) { return d.type === 'esr' && !!((d.st.run.ifs[p] || {}).ospf); },
      f: function (d, p) { var o = d.st.run.ifs[p].ospf; o.net = o.net === 'point-to-point' ? 'broadcast' : 'point-to-point'; } },
    'gw': { t: 'Узел: неверный шлюз', ok: function (d) { return (d.type === 'vpc' || d.type === 'deb') && !!d.st.gw; },
      f: function (d) { var p = d.st.gw.split('.'); p[3] = +p[3] === 254 ? 253 : 254; d.st.gw = p.join('.'); } }
  };
  function cfgFor(net, name) {                   // какие ошибки конфигурации применимы к устройству (и его портам)
    var d = net.byName(name, true), o = []; if (!d) return o;
    var ports = d.type === 'mes' ? net.portsOf(d).filter(function (p) { return d.st.ports[p]; }) : d.type === 'esr' ? Object.keys(d.st.run.ifs) : [null];
    Object.keys(CFG).forEach(function (k) { var C = CFG[k];
      if (/stp-mode|mst-name|gw/.test(k)) { if (C.ok(d)) o.push({ k: 'cfg', cfg: k, dev: name, label: name + ': ' + C.t }); return; }
      ports.forEach(function (p) { if (p && C.ok(d, p) && net.linked(d.id, p.split('.')[0])) o.push({ k: 'cfg', cfg: k, dev: name, port: p, label: name + ' ' + p + ': ' + C.t }); }); });
    return o;
  }
  function apply(n, F) {
    if (F.k === 'link') { var li = -1; n.links.forEach(function (l, i) { if (linkName(n, i) === F.key) li = i; }); if (li >= 0) n.disconnect(li); }
    if (F.k === 'dev') { var d = n.byName(F.key, true); if (d) n.power(d.id, false); }
    if (F.k === 'port') { var e = n.byName(F.dev, true); if (e && e.type === 'mes' && e.st.ports[F.port]) e.st.ports[F.port].shut = true; if (e && e.type === 'esr' && e.st.run.ifs[F.port]) e.st.run.ifs[F.port].shut = true; }
    if (F.k === 'cfg') { var g = n.byName(F.dev, true); if (g && CFG[F.cfg] && CFG[F.cfg].ok(g, F.port)) CFG[F.cfg].f(g, F.port, F.v); if (g && g.type === 'esr') g.st.cand = EL.clone(g.st.run); }
    n.gen++;
  }

  // ---------------------------------------------------------------- анализ одного отказа
  function analyze(net, F, opt) {
    opt = opt || {};
    var base = warm(net), N = nodes(base, opt.routers), M0 = matrix(base, N), S0 = snap(base);
    apply(base, F); observe(base); run(base, 1);
    var M1 = matrix(base, N), S1 = snap(base);
    run(base, CONV - 1);
    var M2 = matrix(base, N), S2 = snap(base);
    return { fault: F, nodes: N.map(function (x) { return x.label; }), before: M0, now: M1, after: M2,
      pairs: pairs(N, M0, M1, M2), changes: diff(S0, S2), changesNow: diff(S0, S1) };
  }
  function pairs(N, M0, M1, M2) {
    var o = [];
    N.forEach(function (s) { N.forEach(function (t) { var a = M0[s.label][t.label]; if (!a) return; var b = M1[s.label][t.label], c = M2[s.label][t.label];
      var k1 = cmp(a, b), k2 = cmp(a, c); if (k1 === 'ok' && k2 === 'ok' || k1 === 'none' && k2 === 'none') return;
      o.push({ src: s.label, dst: t.label, now: k1, after: k2, path0: a.chain, path2: c.chain, why: c.ok ? '' : c.why }); }); });
    return o;
  }
  // ---------------------------------------------------------------- единые точки отказа: все одиночные отказы
  // шаг за шагом (для интерфейса — порциями): step() возвращает false, когда перебор закончен
  function spof(net, opt) {
    opt = opt || {};
    var base = warm(net), N = nodes(base, opt.routers), M0 = matrix(base, N), E = elements(net), i = 0, res = [], total = 0;
    N.forEach(function (s) { N.forEach(function (t) { var a = M0[s.label][t.label]; if (a && a.ok) total++; }); });
    return { total: total, list: E, res: res, step: function () {
      if (i >= E.length) return false; var F = E[i++], c = warm(net); apply(c, F); observe(c); run(c, CONV);
      var M = matrix(c, N), lost = [], rr = 0;
      N.forEach(function (s) { N.forEach(function (t) { var a = M0[s.label][t.label], b = (M[s.label] || {})[t.label]; if (!a || !a.ok) return;
        if (F.k === 'dev' && (s.dev === F.key || t.dev === F.key)) return;   // адреса самого выключенного устройства не считаются
        if (!b || !b.ok) lost.push(s.label + ' → ' + t.label); else if (b.sig !== a.sig) rr++; }); });
      res.push({ fault: F, lost: lost, rerouted: rr, spof: lost.length > 0 });
      return i < E.length; },
      done: function () { return i >= E.length; } };
  }
  function spofAll(net, opt) { var S = spof(net, opt); while (S.step()) { /* перебор целиком (автотест) */ } return S; }

  // связь src → dst после отказа F и схождения (для проверок лаб: «шлюз переживает отказ маршрутизатора»)
  function reach(net, F, src, dst) { var c = warm(net); if (F) { apply(c, F); observe(c); run(c, CONV); } var d = c.byName(src, true); return !!d && !d.off && c.ping(d.id, dst).ok; }
  EL.faults = { reach: reach, copy: copy, warm: warm, nodes: nodes, matrix: matrix, analyze: analyze, spof: spof, spofAll: spofAll, elements: elements, cfgFor: cfgFor, CFG: CFG, apply: apply, CONV: CONV };
})(typeof window !== 'undefined' ? window : global);
