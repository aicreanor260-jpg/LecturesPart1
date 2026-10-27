/* ME: IS-IS, MPLS/LDP, стек меток L3VPN и L2VPN VPWS (спецификация sources/eltex/spec/me.md: РН гл. IS-IS, MPLS, L3VPN, L2VPN; СК 12, 14, 15).
   IS-IS: router isis NAME → net XX.XXXX.XXXX.XXXX.XXXX.00 (область — всё до System ID), is-level level-1|level-1-2|level-2 (по умолчанию level-1-2),
     interface … → address-family ipv4 unicast (без неё интерфейс не анонсируется), passive, level level-N → metric M (по умолчанию 10).
     Смежность L1 — оба умеют L1 и одна область, L2 — оба умеют L2; SPF по уровням; префикс интерфейса — с его метрикой, loopback — 0.
     Маршруты: i L1 (AD 115), i L2 (AD 116, как в примере РН); L1-маршрутизатор получает 0.0.0.0/0 к ближайшему L1/L2 своей области (бит ATT).
   LDP: mpls → router-id, transport-address, forwarding → interface …, ldp → discovery interface …, neighbor ADDR (targeted), mpls ldp neighbor ADDR;
     сессия — discovery на обоих концах линка (или targeted с обеих сторон) и связь между transport-адресами. Метки — на все IGP- и connected-префиксы:
     свой префикс — ImpNull (3; penultimate-hop-popping disable — ExpNull 0), чужой — локальная метка; исходящая метка — локальная метка соседа-next-hop.
     LSP требует LDP-сессию на каждом хопе и mpls forwarding на исходящем интерфейсе.
   L3VPN: пакет VRF идёт со стеком «транспортная метка LDP | метка VPN» хоп за хопом; разрыв LSP — пакет отбрасывается.
   L2VPN: l2vpn → xconnect-group G → p2p NAME → interface AC, pw ADDR ID (pw-class), mtu; l2vpn pw-class → encapsulation mpls …
     Псевдопровод Up: у второго PE такой же pw-id с pw на наш адрес, targeted LDP (mpls ldp neighbor) с обеих сторон, LSP в обе стороны, AC подняты,
     MTU совпадают (иначе MM). Кадры с AC переносятся на AC второго PE (саб-интерфейс AC — со своим outer-vid). AC с IP-адресом — commit отклоняется (РН с. 180).
   Упрощения: номера меток условные (локальные — с 16 по порядку префиксов, метка VPN — 1000 + номер VRF, метка PW — 2000 + pw-id); таймеры IS-IS/LDP
     (hello, hold) не моделируются — смежность поднимается и рвётся сразу; LSP, базы LSDB и TLV не моделируются — show isis database показывает по LSP
     на маршрутизатор; ECMP нет; control-word не сравнивается; backup PW хранится, но не используется. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip, ME = EL.me, X = ME.X, val = ME.val, IFT = ME.IFT, isMe = ME.isMe;
  function shortIf(h) {                                   // 'interface tengigabitethernet 0/0/5' → te0/0/5, 'interface loopback 1' → lo1, 'te0/0/9' → te0/0/9
    var q = String(h).replace(/^interface\s+/, ''); if (/^(te|twe|hu|fo|gi)\d+\/\d+\/\d+(\.\d+)?$/.test(q)) return q;
    var m = String(h).match(/(?:interface\s+)?(\S+)\s+(\S+)$/); if (!m) return null;
    if (m[1] === 'loopback') return 'lo' + m[2];
    var sh = Object.keys(IFT).filter(function (k) { return IFT[k] === m[1]; })[0]; return sh ? sh + m[2] : null;
  }
  function longIf(k) { var m = String(k).match(/^([a-z]+)(.*)$/); return m[1] === 'lo' ? 'loopback ' + m[2] : (IFT[m[1]] || m[1]) + ' ' + m[2]; }
  function shortName(k) { var m = String(k).match(/^([a-z]+)(.*)$/); return m[1] === 'lo' ? 'lo ' + m[2] : m[1] + ' ' + m[2]; }

  // ---------------------------------------------------------------- компиляция дерева кандидата
  X.compile.push(function (st, t, c) {
    c.isis = null; c.ldp = null; c.l2 = null;
    Object.keys(t.K).forEach(function (h) { var m = h.match(/^router isis (\S+)$/); if (!m || c.isis) return; var n = t.K[h], net = val(n, 'net') || '';
      var parts = net.split('.'), I = c.isis = { name: m[1], net: net, sys: parts.slice(-4, -1).join('.'), area: parts.slice(0, -4).join('.'),
        lvl: val(n, 'is-level') || 'level-1-2', host: val(n, 'host-name'), ifs: {} };
      Object.keys(n.K).forEach(function (h2) { if (!/^interface /.test(h2)) return; var k = shortIf(h2), x = n.K[h2]; if (!k) return;
        var met = { 1: 10, 2: 10 }; Object.keys(x.K).forEach(function (h3) { var lm = h3.match(/^level level-([12])$/); if (lm) met[lm[1]] = +(val(x.K[h3], 'metric') || 10); });
        I.ifs[k] = { af: !!x.K['address-family ipv4 unicast'], passive: x.L.indexOf('passive') >= 0, shut: x.L.indexOf('shutdown') >= 0, met: met,
          cl: val(x, 'circuit-level') || null }; }); });
    var mp = t.K.mpls;
    if (mp && mp.K.ldp) { var L = c.ldp = { rid: val(mp, 'router-id'), ta: val(mp, 'transport-address'), php: mp.L.concat(mp.K.ldp.L).indexOf('penultimate-hop-popping disable') < 0,
        fwd: [], disc: [], tn: [] };
      Object.keys((mp.K.forwarding || { K: {} }).K).forEach(function (h) { var k = shortIf(h); if (k) L.fwd.push(k); });
      Object.keys(mp.K.ldp.K).forEach(function (h) { var dm = h.match(/^discovery interface (.+)$/), nm = h.match(/^neighbor (\S+)$/);
        if (dm) { var k = shortIf(dm[1]); if (k) L.disc.push(k); } if (nm) L.tn.push(nm[1]); });
      Object.keys(t.K).forEach(function (h) { var nm = h.match(/^mpls ldp neighbor (\S+)$/); if (nm && L.tn.indexOf(nm[1]) < 0) L.tn.push(nm[1]); }); }
    var l2 = t.K.l2vpn, pwc = {};
    Object.keys(t.K).forEach(function (h) { var m = h.match(/^l2vpn pw-class (\S+)$/); if (m) pwc[m[1]] = t.K[h].L.slice(); });
    if (l2) { c.l2 = { xc: [], pwc: pwc };
      Object.keys(l2.K).forEach(function (h) { var pm = h.match(/^pw-class (\S+)$/); if (pm) pwc[pm[1]] = l2.K[h].L.slice(); });
      Object.keys(l2.K).forEach(function (h) { var gm = h.match(/^xconnect-group (\S+)$/); if (!gm) return;
        Object.keys(l2.K[h].K).forEach(function (h2) { var pm = h2.match(/^p2p (\S+)$/); if (!pm) return; var x = l2.K[h].K[h2], ac = null, pw = null;
          x.L.forEach(function (l) { var im = l.match(/^interface (.+)$/); if (im) ac = shortIf(im[1]); });
          Object.keys(x.K).forEach(function (h3) { var wm = h3.match(/^pw (\S+) (\d+)$/); if (wm) pw = { ip: wm[1], id: +wm[2], cls: val(x.K[h3], 'pw-class') }; });
          var an = ac && ac.indexOf('.') > 0 ? t.K['interface ' + longIf(ac)] : null, vid = an ? parseInt(val(an, 'encapsulation outer-vid'), 10) : null;
          c.l2.xc.push({ grp: gm[1], name: pm[1], ac: ac, vid: isNaN(vid) ? null : vid, pw: pw, mtu: +(val(x, 'mtu') || 1500), mode: val(x, 'transport-mode') || 'ethernet' }); }); }); }
  });
  // AC с IP-адресом в L2VPN не включается (РН с. 180) — commit отклоняется
  X.check.push(function (st, t) {
    var l2 = t.K.l2vpn, bad = null; if (!l2) return null;
    Object.keys(l2.K).forEach(function (h) { if (!/^xconnect-group /.test(h)) return; Object.keys(l2.K[h].K).forEach(function (h2) {
      l2.K[h].K[h2].L.forEach(function (l) { var im = l.match(/^interface (.+)$/); if (!im) return;
        var k = shortIf(im[1]), node = k && t.K['interface ' + longIf(k)];
        if (node && val(node, 'ipv4 address')) bad = im[1]; }); }); });
    return bad ? '% Commit failed: interface ' + bad + ' has IPv4 address and cannot be used as L2VPN attachment circuit' : null;
  });

  // ---------------------------------------------------------------- IS-IS
  function ifOf(s, id, k) { return s.ifaces(id).filter(function (f) { return f.name === k; })[0] || null; }
  function lv(I) { return { 1: I.lvl !== 'level-2', 2: I.lvl !== 'level-1' }; }
  function adjs(s) {                                      // смежности: {id: [{dev, lvl, ifn, nh, met}]}
    var A = {};
    s.order.forEach(function (id) { var d = s.devs[id]; if (!isMe(d) || d.off) return; var I = d.st.run.isis; if (!I || !I.net) return; A[id] = [];
      Object.keys(I.ifs).forEach(function (k) { var x = I.ifs[k]; if (!x.af || x.passive || x.shut || /^lo/.test(k)) return; var f = ifOf(s, id, k); if (!f || f.vrf) return;
        s.flood(id, f).eps.forEach(function (ep) { var pd = s.devs[ep.dev]; if (!isMe(pd) || ep.dev === id) return; var J = pd.st.run.isis; if (!J || !J.net) return;
          var y = J.ifs[ep.iface.name]; if (!y || !y.af || y.passive || y.shut || !IP.sameNet(ep.iface.ip, f.ip, f.len)) return;
          var a = lv(I), b = lv(J);
          [1, 2].forEach(function (L) { if (!a[L] || !b[L]) return; if (L === 1 && I.area !== J.area) return;
            if ((x.cl && x.cl !== 'level-' + L && x.cl !== 'level-1-2') || (y.cl && y.cl !== 'level-' + L && y.cl !== 'level-1-2')) return;
            A[id].push({ dev: ep.dev, lvl: L, ifn: k, nh: ep.iface.ip, met: x.met[L] }); }); }); }); });
    return A;
  }
  function spf(A, src, L) {                               // Дейкстра: dist и первый хоп
    var dist = {}, first = {}, done = {}, q = [src]; dist[src] = 0;
    while (q.length) { q.sort(function (a, b) { return dist[a] - dist[b]; }); var u = q.shift(); if (done[u]) continue; done[u] = true;
      (A[u] || []).forEach(function (e) { if (e.lvl !== L) return; var c = dist[u] + e.met;
        if (dist[e.dev] === undefined || c < dist[e.dev]) { dist[e.dev] = c; first[e.dev] = u === src ? e : first[u]; q.push(e.dev); } }); }
    return { dist: dist, first: first };
  }
  P.isisDyn = function () {
    if (this._isis && this._isis.gen === this.gen) return this._isis;
    var s = this, A = adjs(s), R = {}, pre = {};
    Object.keys(A).forEach(function (id) { var I = s.devs[id].st.run.isis; pre[id] = [];
      Object.keys(I.ifs).forEach(function (k) { var x = I.ifs[k]; if (!x.af || x.shut) return; var f = ifOf(s, id, k); if (!f || f.vrf) return;
        pre[id].push({ net: IP.netOf(f.ip, f.len), len: f.len, m: /^lo/.test(k) ? 0 : x.met }); }); });
    Object.keys(A).forEach(function (id) { var I = s.devs[id].st.run.isis, mine = {}, out = {}; R[id] = [];
      s.ifaces(id).forEach(function (f) { mine[IP.netOf(f.ip, f.len)] = true; });
      [1, 2].forEach(function (L) { if (!lv(I)[L]) return; var sp = spf(A, id, L);
        Object.keys(sp.dist).forEach(function (rid) { if (rid === id) return; var e = sp.first[rid];
          pre[rid].forEach(function (p) { if (mine[p.net]) return; var cost = sp.dist[rid] + (p.m[L] || 0), cur = out[p.net];
            var cand = { p: 'i', lvl: L, net: p.net, len: p.len, nh: e.nh, ifn: e.ifn, ad: L === 1 ? 115 : 116, m: cost };
            if (!cur || cand.ad < cur.ad || (cand.ad === cur.ad && cost < cur.m)) out[p.net] = cand; }); }); });
      if (I.lvl === 'level-1') { var sp1 = spf(A, id, 1), best = null;      // бит ATT: ближайший L1/L2 своей области с L2-смежностями
        Object.keys(sp1.dist).forEach(function (rid) { if (rid === id) return; var J = s.devs[rid].st.run.isis;
          if (J.lvl === 'level-1-2' && (A[rid] || []).some(function (e) { return e.lvl === 2; }) && (!best || sp1.dist[rid] < sp1.dist[best])) best = rid; });
        if (best) out['0.0.0.0/0'] = { p: 'i', lvl: 1, net: '0.0.0.0/0', len: 0, nh: sp1.first[best].nh, ifn: sp1.first[best].ifn, ad: 115, m: sp1.dist[best], att: true }; }
      Object.keys(out).forEach(function (k) { R[id].push(out[k]); }); });
    this._isis = { gen: this.gen, A: A, R: R };
    return this._isis;
  };
  var routes0 = P.routes;
  P.routes = function (id) {
    var r = routes0.apply(this, arguments); if (!isMe(this.devs[id]) || this._vrfCtx || this._isisBusy) return r;
    this._isisBusy = true; try { (this.isisDyn().R[id] || []).forEach(function (x) { r.push(x); }); } finally { this._isisBusy = false; }
    return r;
  };

  // ---------------------------------------------------------------- LDP
  function rid(s, id) { var c = s.devs[id].st.run, L = c.ldp; if (L && L.rid) return L.rid;
    var lo = Object.keys(c.ifs).filter(function (k) { return /^lo/.test(k) && c.ifs[k].ip && !c.ifs[k].vrf; }).map(function (k) { return c.ifs[k].ip.split('/')[0]; });
    return lo.sort(function (a, b) { return IP.ip2n(b) - IP.ip2n(a); })[0] || null; }
  function taddr(s, id) { var L = s.devs[id].st.run.ldp; return (L && L.ta) || rid(s, id); }
  function reach(s, src, dst) {                           // по таблицам маршрутов хоп за хопом, без побочных эффектов
    var cur = src;
    for (var i = 0; i < 16; i++) { if (s.ifaces(cur).some(function (f) { return f.ip === dst; })) return true;
      var r = s.lookup(cur, dst); if (!r || r.iface.tun) return false;
      var ep = s.flood(cur, r.iface).eps.filter(function (e) { return e.iface.ip === (r.nh || dst); })[0]; if (!ep) return false; cur = ep.dev; }
    return false;
  }
  P.ldpDyn = function () {
    if (this._ldp && this._ldp.gen === this.gen) return this._ldp;
    var s = this, ses = {}, lab = {}, me = s.order.filter(function (id) { var d = s.devs[id]; return isMe(d) && !d.off && d.st.run.ldp; });
    function key(a, b) { return a < b ? a + '|' + b : b + '|' + a; }
    me.forEach(function (id) { var L = s.devs[id].st.run.ldp;
      L.disc.forEach(function (k) { var f = ifOf(s, id, k); if (!f || f.vrf) return;
        s.flood(id, f).eps.forEach(function (ep) { var pd = s.devs[ep.dev]; if (!isMe(pd) || ep.dev === id || !pd.st.run.ldp || pd.off) return;
          if (pd.st.run.ldp.disc.indexOf(ep.iface.name) < 0) return;
          var kk = key(id, ep.dev), x = ses[kk] = ses[kk] || { a: id, b: ep.dev, link: [], tgt: false };
          if (!x.link.some(function (q) { return q.dev === id && q.ifn === k; })) x.link.push({ dev: id, ifn: k, nh: ep.iface.ip }); }); });
      L.tn.forEach(function (ip) { var pid = s.owner(ip), pd = pid && s.devs[pid]; if (!pd || !isMe(pd) || !pd.st.run.ldp || pd.off) return;
        var back = pd.st.run.ldp.tn.filter(function (q) { return s.owner(q) === id; })[0]; if (!back) return;
        var kk = key(id, pid); (ses[kk] = ses[kk] || { a: id, b: pid, link: [], tgt: false }).tgt = true; }); });
    Object.keys(ses).forEach(function (kk) { var x = ses[kk], ta = taddr(s, x.a), tb = taddr(s, x.b);
      x.up = !!(ta && tb && reach(s, x.a, tb) && reach(s, x.b, ta)); x.why = x.up ? '' : 'нет связи между transport-адресами ' + ta + ' и ' + tb + ' (TCP 646)'; });
    // локальные метки на IGP- и connected-префиксы глобальной таблицы
    me.forEach(function (id) { var L = s.devs[id].st.run.ldp, by = s.best(id), n = 16, T = lab[id] = {};
      Object.keys(by).sort(function (a, b) { return IP.ip2n(a.split('/')[0]) - IP.ip2n(b.split('/')[0]) || a.length - b.length; }).forEach(function (net) {
        var r = by[net]; if (r.vrf || !/^(C|O|i|R)$/.test(r.p)) return;
        T[net] = r.p === 'C' ? (L.php ? 3 : 0) : n++; }); });
    this._ldp = { gen: this.gen, ses: ses, lab: lab };
    return this._ldp;
  };
  function sess(s, a, b) { var D = s.ldpDyn(), k = a < b ? a + '|' + b : b + '|' + a; return D.ses[k] || null; }
  function lbl(v) { return v === 3 ? 'ImpNull' : v === 0 ? 'ExpNull' : String(v); }
  // исходящая метка для префикса: локальная метка LDP-соседа — next-hop
  P.ldpFwd = function (id, net) {
    var D = this.ldpDyn(), by = this.best(id), r = by[net]; if (!r || !r.nh || r.vrf) return null;
    var nd = this.owner(r.nh), L = this.devs[id].st.run.ldp; if (!nd || !D.lab[nd]) return { net: net, r: r, why: 'next-hop ' + r.nh + ' не LDP-маршрутизатор' };
    var x = sess(this, id, nd); if (!x || !x.up || !x.link.length) return { net: net, r: r, nd: nd, why: 'нет LDP-сессии с ' + this.devs[nd].name };
    var out = D.lab[nd][net]; if (out === undefined) return { net: net, r: r, nd: nd, why: this.devs[nd].name + ' не выделил метку для ' + net };
    if (L.fwd.indexOf(r.ifn) < 0) return { net: net, r: r, nd: nd, label: out, why: 'на ' + r.ifn + ' нет mpls forwarding' };
    return { net: net, r: r, nd: nd, label: out };
  };
  function fecFor(s, id, ip) { var by = s.best(id), best = null; Object.keys(by).forEach(function (k) { var r = by[k];
    if (!r.vrf && IP.sameNet(ip, k.split('/')[0], r.len) && (!best || r.len > best.len)) best = r; }); return best ? best.net : null; }
  // LSP от PE до loopback удалённого PE: хопы с метками; inner — метка сервиса (VPN / PW)
  function lsp(s, src, dst, peer, inner, what) {
    var steps = [], cur = src, guard = 0, nm = function (id) { return s.devs[id].name; };
    if (!s.devs[src].st.run.ldp) { steps.push({ k: 'drop', t: nm(src) + ': MPLS/LDP не настроен — метки для ' + peer + ' нет' }); return { ok: false, steps: steps }; }
    while (cur !== dst && guard++ < 16) {
      var fec = fecFor(s, cur, peer), F = fec && s.ldpFwd(cur, fec);
      if (!F || F.why) { steps.push({ k: 'drop', t: nm(cur) + ': LSP до ' + peer + ' разорван — ' + (F ? F.why : 'нет маршрута') }); return { ok: false, steps: steps }; }
      steps.push({ k: 'route', t: nm(cur) + ' → ' + nm(F.nd) + ' (' + F.r.ifn + '): ' + (F.label === 3 ? 'транспортная метка снята (PHP, ImpNull)' :
        'транспортная метка ' + lbl(F.label)) + (inner !== null ? ' | ' + what + ' ' + inner : '') });
      cur = F.nd;
    }
    if (cur !== dst) { steps.push({ k: 'drop', t: 'LSP до ' + peer + ' не дошёл до ' + nm(dst) }); return { ok: false, steps: steps }; }
    return { ok: true, steps: steps };
  }
  X.lsp = function (s, src, dst, peer, inner) { return lsp(s, src, dst, peer, inner, 'метка VPN'); };
  X.vpnLabel = function (s, dev, vrf) { var v = Object.keys((s.devs[dev].st.run.vpn || { vrfs: {} }).vrfs).sort(); return 1000 + Math.max(0, v.indexOf(vrf)); };

  // ---------------------------------------------------------------- L2VPN: псевдопроводы
  function myAddr(s, id) { return s.ifaces(id).filter(function (f) { return /^lo/.test(f.name) && !f.vrf; }).map(function (f) { return f.ip; }).concat([rid(s, id)]); }
  function acUp(s, id, ac) { if (!ac) return false; var c = s.devs[id].st.run, ph = ac.split('.')[0]; return !!(c.ifs[ph] && !c.ifs[ph].shut && s.linkUp(id, ph)); }
  P.pwState = function (id, xc) {
    var s = this, w = xc.pw; if (!w) return { up: false, why: 'pw не задан' };
    var pid = s.owner(w.ip), pd = pid && s.devs[pid];
    if (!pd || !isMe(pd) || pd.off) return { up: false, why: 'нет PE с адресом ' + w.ip };
    var rx = ((pd.st.run.l2 || { xc: [] }).xc).filter(function (y) { return y.pw && y.pw.id === w.id && myAddr(s, id).indexOf(y.pw.ip) >= 0; })[0];
    if (!rx) return { up: false, why: pd.name + ': нет p2p с pw на наш адрес и pw-id ' + w.id };
    var x = sess(s, id, pid); if (!x || !x.tgt) return { up: false, why: 'нет targeted LDP с ' + w.ip + ' (mpls ldp neighbor на обоих PE)' };
    if (!x.up) return { up: false, why: x.why };
    if (!acUp(s, id, xc.ac)) return { up: false, why: 'AC ' + xc.ac + ' не поднят' };
    if (!acUp(s, pid, rx.ac)) return { up: false, why: pd.name + ': AC ' + rx.ac + ' не поднят' };
    if (rx.mtu !== xc.mtu) return { up: false, mm: true, why: 'MTU не совпадают (' + xc.mtu + ' и ' + rx.mtu + ')' };
    var f = lsp(s, id, pid, w.ip, null), b = lsp(s, pid, id, rx.pw.ip, null);
    if (!f.ok || !b.ok) return { up: false, why: 'нет LSP: ' + ((f.ok ? b : f).steps.slice(-1)[0] || {}).t };
    return { up: true, peer: pid, rx: rx, local: 2000 + w.id, remote: 2000 + w.id };
  };
  // кадр на AC → AC второго PE
  P.acIn = function (dev, port, tag) {
    var d = this.devs[dev]; if (!isMe(d)) return null; var l2 = d.st.run.l2; if (!l2) return null; var s = this;
    var xc = l2.xc.filter(function (x) { return x.ac && x.ac.split('.')[0] === port && (x.ac.indexOf('.') < 0 || (x.vid !== null && x.vid === tag)); })[0];
    if (!xc) return null;
    var stt = s.pwState(dev, xc);
    if (!stt.up) return { notes: [d.name + ': ' + xc.ac + ' — AC псевдопровода ' + xc.name + ', он не работает: ' + stt.why] };
    var L = lsp(s, dev, stt.peer, xc.pw.ip, stt.remote, 'метка PW'), pd = s.devs[stt.peer], rac = stt.rx.ac, rph = rac.split('.')[0];
    var otag = rac.indexOf('.') > 0 ? stt.rx.vid : (xc.ac.indexOf('.') > 0 ? null : tag);   // саб-AC: свой outer-vid; порт-AC: кадр как есть
    return { notes: [d.name + ' → ' + pd.name + ': кадр перенесён псевдопроводом ' + xc.name + ' (pw-id ' + xc.pw.id + '): ' + L.steps.map(function (x) { return x.t; }).join('; ')],
      out: { dev: stt.peer, port: rph, tag: otag } };
  };

  // ---------------------------------------------------------------- show
  function pad(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function age(s, st) { var t = Math.max(0, Math.floor(s.now - ((st.me && st.me.tCommit) || 0))), p = function (v) { return ('0' + v).slice(-2); };
    return p(Math.floor(t / 3600)) + 'h' + p(Math.floor(t / 60) % 60) + 'm' + p(t % 60) + 's'; }
  function date() { return EL.clock.fmt ? EL.clock.fmt(EL.clock.now()) : ''; }
  var CODES = ['   Codes: C - connected, S - static, O - OSPF, B - BGP, L - local', '         IA - OSPF inter area, EA - OSPF intra area',
    '         N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2', '         E1 - OSPF external type 1, E2 - OSPF external type 2',
    '         i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2,', '         LE1 - ISIS level1 external, LE2 - ISIS level2 external', '         BI - BGP internal, BE - BGP external, BV - BGP vpn'];
  function rline(s, st, r) {
    var code = r.p === 'i' ? 'i L' + r.lvl : r.p === 'O' ? 'O EA' : r.p === 'B' ? (r.ad === 20 ? 'B BE' : 'B BI') : r.p;
    if (r.p === 'C' || r.p === 'L') return pad(code, 7) + r.net + ' is directly connected, ' + age(s, st) + ', ' + shortName(r.ifn);
    return pad(code, 7) + r.net + ' via ' + r.nh + ' [' + r.ad + '/' + r.m + '], ' + age(s, st) + (r.ifn ? ', ' + shortName(r.ifn) : '');
  }
  function routeShow(s, st, only) {
    var id = st.dev, all = s.routes(id), by = s.best(id, all), rs = [];
    Object.keys(by).forEach(function (k) { var r = by[k]; if (r.vrf) return;
      if (r.p === 'C' && r.len === 32) { rs.push({ p: 'L', net: r.net, ifn: r.ifn }); return; }        // адрес /32 (loopback) — только L, как в РН
      rs.push(r);
      if (r.p === 'C') { var f = s.ifaces(id).filter(function (q) { return q.name === r.ifn; })[0]; if (f && f.len < 32) rs.push({ p: 'L', net: f.ip + '/32', ifn: f.name }); } });
    rs.sort(function (a, b) { return IP.ip2n(a.net.split('/')[0]) - IP.ip2n(b.net.split('/')[0]) || +a.net.split('/')[1] - +b.net.split('/')[1]; });
    if (only) rs = rs.filter(function (r) { return r.p === only; });
    var o = only === 'i' ? ['   Codes: i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2', '         LE1 - ISIS level1 external, LE2 - ISIS level2 external'] : CODES.slice();
    return [date()].concat(o, rs.map(function (r) { return rline(s, st, r); }), only ? ['Total route count: ' + rs.length] : []).join('\n');
  }
  function isisNb(s, st) { var D = s.isisDyn(), A = D.A[st.dev] || [], I = st.run.isis;
    var o = ['IS-IS Router ' + (I ? I.name : '') + ' adjacency:', 'System Id      Interface              State Type     SNPA            Hold NSF   BFD  Hostname',
      '-------------- ---------------------- ----- -------- --------------- ---- ----- ---- ----------------'];
    A.forEach(function (e) { var J = s.devs[e.dev].st.run.isis; o.push(pad(J.sys, 15) + pad(e.ifn, 23) + pad('up', 6) + pad('level-' + e.lvl, 9) + pad(EL.mac(s.devs[e.dev].name + 'sys').replace(/:/g, '').replace(/(\w{4})(?=\w)/g, '$1.'), 16) +
      pad(30, 5) + pad('true', 6) + pad('none', 5) + (J.host || s.devs[e.dev].st.run.host)); });
    return o.join('\n'); }
  function isisDb(s, st) { var D = s.isisDyn(), I = st.run.isis, o = ['   IS-IS Router ' + I.name];
    [1, 2].forEach(function (L) { if (!lv(I)[L]) return; var ids = Object.keys(D.A).filter(function (id) { return id === st.dev || spf(D.A, st.dev, L).dist[id] !== undefined; })
        .filter(function (id) { return lv(s.devs[id].st.run.isis)[L] && (L === 2 || s.devs[id].st.run.isis.area === I.area); });
      o.push('IS-IS level-' + L + ' link-state database', 'LSP ID                Sequence  Checksum  Lifetime  Length  Attributes', '--------------------- --------- --------- --------- ------- -----------');
      ids.forEach(function (id) { var J = s.devs[id].st.run.isis, h = EL.E.hash(J.sys + L).slice(0, 4);
        o.push(pad(J.sys + '.00-00', 22) + pad('0x' + (0x1000 + (s.gen % 4096)).toString(16), 10) + pad('0x' + h, 10) + pad(1200 - Math.floor(s.now % 900), 10) + pad(66, 8) + 'level-' + L); });
      o.push('Total LSPs: ' + ids.length); });
    return o.join('\n'); }
  function isisMain(s, st) { var I = st.run.isis; if (!I) return '';
    return [date(), '   IS-IS Router ' + I.name, '      System Id: ' + I.sys, '      IS Levels: ' + I.lvl, '      Net: ' + I.net, '      Hostname: ' + (I.host || st.run.host),
      '      LSP refresh-interval: 900 secs', '      LSP max-lifetime: 1200 secs', '      Area-address: ' + I.area].join('\n'); }
  function isisIfs(s, st) { var I = st.run.isis; if (!I) return '';
    return ['Interface              Level      Metric  Passive  AF IPv4', '---------------------- ---------- ------- -------- -------'].concat(Object.keys(I.ifs).map(function (k) { var x = I.ifs[k];
      return pad(shortName(k), 23) + pad(x.cl || I.lvl, 11) + pad(/^lo/.test(k) ? 0 : x.met[I.lvl === 'level-1' ? 1 : 2], 8) + pad(x.passive ? 'yes' : 'no', 9) + (x.af ? 'yes' : 'no'); })).join('\n'); }
  function ldpFwdText(s, st) { var D = s.ldpDyn(), id = st.dev, o = ['Codes:', '   R = Remote LFA FRR backup',
      'Prefix                Label(s) out  Outgoing Interface  Next Hop              flags', '--------------------- ------------- ------------------- --------------------- ------'];
    Object.keys(D.lab[id] || {}).forEach(function (net) { var F = s.ldpFwd(id, net); if (!F || F.why) return;
      o.push(pad(net, 22) + pad(lbl(F.label), 14) + pad(shortName(F.r.ifn), 20) + F.r.nh); });
    return o.join('\n'); }
  function ldpNbText(s, st, detail) { var D = s.ldpDyn(), id = st.dev, o = detail ? [] : [date(), 'Peer                    Up/Down time  Expires    Adjcs  Addrs  Labels  GR', '----------------------- ------------- ---------- ------ ------ ------- ---'];
    Object.keys(D.ses).forEach(function (k) { var x = D.ses[k]; if (x.a !== id && x.b !== id) return; var pid = x.a === id ? x.b : x.a, pr = taddr(s, pid);
      var adj = x.link.filter(function (q) { return q.dev === id; }).length + (x.tgt ? 1 : 0), lb = Object.keys(D.lab[pid] || {}).length, addrs = s.ifaces(pid).filter(function (f) { return !f.vrf; }).length;
      if (!detail) { if (x.up) o.push(pad(pr + ':0', 24) + pad(age(s, st), 14) + pad('33s', 11) + pad(adj, 7) + pad(addrs, 7) + pad(lb, 8) + 'N'); return; }
      o.push('   LDPv1 peer: ' + pr + ':0', '      Current state: ' + (x.up ? 'operational' : 'non-existent (' + x.why + ')'), '      Label distribution method: downstream-unsolicited',
        '      Session holdtime: 40 secs (own 40 secs, peer 40 secs)', '      Established adjacencies:');
      x.link.filter(function (q) { return q.dev === id; }).forEach(function (q) { o.push('         link, ' + q.ifn + ', holdtime: 15 secs, bfd: none (not-required)'); });
      if (x.tgt) o.push('         targeted, with ' + pr + ', holdtime: 45 secs, bfd: none (not-required)');
      o.push('      Labels received from neighbor:'); Object.keys(D.lab[pid] || {}).forEach(function (n) { o.push('         ' + D.lab[pid][n] + ', type: prefix, ' + n); }); });
    return o.join('\n'); }
  function ldpBind(s, st, remote) { var D = s.ldpDyn(), id = st.dev, o = remote ? ['  Prefix                Peer ID                    Label        State                        Type         Interface',
      '  --------------------- -------------------------- ----------- ---------------------------- ----------- ----------'] :
      ['  Prefix                Label        Type', '  --------------------- ------------ ----------'];
    if (!remote) Object.keys(D.lab[id] || {}).forEach(function (n) { o.push('  ' + pad(n, 22) + pad(lbl(D.lab[id][n]), 13) + 'prefix'); });
    else Object.keys(D.ses).forEach(function (k) { var x = D.ses[k]; if (!x.up || (x.a !== id && x.b !== id)) return; var pid = x.a === id ? x.b : x.a;
      Object.keys(D.lab[pid] || {}).forEach(function (n) { var F = s.ldpFwd(id, n), inst = F && !F.why && F.nd === pid;
        o.push('  ' + pad(n, 22) + pad(taddr(s, pid) + ':0', 27) + pad(D.lab[pid][n], 12) + pad(inst ? 'mapping-established' : 'mapping-liberally-retained', 29) + pad('prefix', 12) + (inst ? shortName(F.r.ifn) : '')); }); });
    return o.join('\n'); }
  function ldpPar(s, st) { var L = st.run.ldp; if (!L) return '';
    return ['   LDP Parameters:', '      Router ID: ' + (rid(s, st.dev) || '-'), '      Transport address: ' + (taddr(s, st.dev) || '-'), '   Neighbors:']
      .concat(L.tn.map(function (ip) { return '      Peer address: ' + ip + '\n         Holdtime interval: 45 sec'; }), ['   Interfaces:'],
        L.disc.map(function (k) { return '      Interface ' + longIf(k).replace(/^\w/, function (c) { return c.toUpperCase(); }) + '\n         Holdtime interval: 15 sec'; }), ['   Hello interval: 5 sec']).join('\n'); }
  function l2Text(s, st, name, detail) { var l2 = st.run.l2, id = st.dev; if (!l2) return '';
    var o = ['MM -- mtu mismatch        Up -- up                      GUp -- going up', 'CM -- control-word mismatch Dn -- down                  GDn -- going down',
      'OL -- no outgoing label   ST -- standby                 Lld -- lower layer down'];
    l2.xc.filter(function (x) { return !name || x.name === name || x.grp === name; }).forEach(function (x) { var w = s.pwState(id, x), stt = w.up ? 'Up' : w.mm ? 'MM' : 'Dn';
      o.push('Group ' + x.grp + ', XC ' + x.name + ', mtu ' + x.mtu + ', state Administrative active', 'AC: ' + (x.ac ? longIf(x.ac) : '-'),
        '   AC binding status: ' + (x.ac && acUp(s, id, x.ac) ? 'up' : 'down'), '      PW: Neighbor ' + (x.pw ? x.pw.ip + ', pw-id ' + x.pw.id : '-') + ', admin up, oper ' + stt + (w.up ? '' : '  (' + w.why + ')'));
      if (detail && x.pw) { o.push('         PW class: ' + (x.pw.cls || '-') + ', signaling: pseudowire-id-fec-signaling', '         PSN type: mpls, encapsulation: MPLS',
        '                                            Local                        Remote', pad('Label', 44) + pad(w.up ? w.local : '-', 29) + (w.up ? w.remote : '-'),
        pad('MTU', 44) + pad(x.mtu, 29) + (w.rx ? w.rx.mtu : '-')); } });
    return o.join('\n'); }
  function bgpVpnRoutes(s, st, ip) { var c = st.run, pid = s.owner(ip), pd = pid && s.devs[pid]; if (!pd || !isMe(pd)) return '';
    var pc = pd.st.run, o = ['   BGP router identifier ' + (c.bgp && c.bgp.rid || rid(s, st.dev)) + ', local AS number ' + (c.bgp ? c.bgp.as : '-'), 'Received bgp routes from neighbor: ' + ip,
      'Route Distinguisher    IP Prefix              Next hop          Metric  Rcvd/Lcl label  LocPrf  Weight  Path', '---------------------  ---------------------  ----------------  ------  --------------  ------  ------  ----'], n = 0;
    Object.keys((pc.vpn || { vrfs: {} }).vrfs).forEach(function (V) { var rv = pc.vpn.vrfs[V];
      s.ifaces(pid).filter(function (f) { return f.vrf === V; }).map(function (f) { return IP.netOf(f.ip, f.len); }).concat((pc.routes || []).filter(function (r) { return r.vrf === V; }).map(function (r) { return r.net; }))
        .forEach(function (net) { n++; o.push('u>i ' + pad(rv.rd || '-', 19) + pad(net, 23) + pad(ip, 18) + pad(0, 8) + pad(X.vpnLabel(s, pid, V) + '/-', 16) + pad(100, 8) + pad(0, 8) + '?'); }); });
    o.push('Total paths: ' + n); return o.join('\n'); }
  X.show.push(function (st, line) {
    var s = st.net; if (!s) return null; var m;
    if (line === 'show route') return routeShow(s, st, null);
    if ((m = line.match(/^show route (isis|ospf|static|connected|bgp)$/))) return routeShow(s, st, { isis: 'i', ospf: 'O', static: 'S', connected: 'C', bgp: 'B' }[m[1]]);
    if (line === 'show isis') return isisMain(s, st);
    if (line === 'show isis neighbors') return st.run.isis ? isisNb(s, st) : '';
    if (line === 'show isis database') return st.run.isis ? isisDb(s, st) : '';
    if (line === 'show isis interfaces') return isisIfs(s, st);
    if (line === 'show mpls ldp forwarding') return st.run.ldp ? ldpFwdText(s, st) : '';
    if (line === 'show mpls ldp neighbors') return st.run.ldp ? ldpNbText(s, st, false) : '';
    if (line === 'show mpls ldp neighbors detail') return st.run.ldp ? ldpNbText(s, st, true) : '';
    if (line === 'show mpls ldp bindings') return st.run.ldp ? ldpBind(s, st, false) : '';
    if (line === 'show mpls ldp bindings remote') return st.run.ldp ? ldpBind(s, st, true) : '';
    if (line === 'show mpls ldp parameters') return ldpPar(s, st);
    if (line === 'show l2vpn xconnect') return l2Text(s, st, null, false);
    if ((m = line.match(/^show l2vpn xconnect (p2p-name|group) (\S+)( detail)?$/))) return l2Text(s, st, m[2], !!m[3]);
    if (line === 'show l2vpn summary') { var l2 = st.run.l2 || { xc: [] }, up = l2.xc.filter(function (x) { return s.pwState(st.dev, x).up; }).length;
      return 'Number of groups: ' + Object.keys(l2.xc.reduce(function (a, x) { a[x.grp] = 1; return a; }, {})).length + '\nNumber of xconnects: ' + l2.xc.length + ', Up: ' + up + ', Down: ' + (l2.xc.length - up); }
    if ((m = line.match(/^show bgp vpnv4 unicast neighbors (\S+) routes$/))) return bgpVpnRoutes(s, st, m[1]);
    return null;
  });
})(typeof window !== 'undefined' ? window : global);
