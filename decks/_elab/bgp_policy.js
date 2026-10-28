/* Политики BGP на ESR (справочник ESR-Series CLI 1.23): маршрутные карты, списки префиксов, атрибуты.
   route-map NAME → rule N → (config-route-map-rule)#:
     match ip address A/L [eq|le|ge N [le N]] · match ip address object-group NAME [eq|le|ge …] · match as-path [begin|contain|end] AS… | empty | regex R
     match community СПИСОК | regex R · action permit | deny
     action set local-preference N | increment N | decrement N · action set metric bgp N | increment N | decrement N
     action set as-path prepend AS… · action set community СПИСОК | no-advertise | no-export · action add/remove community … · action set origin igp|egp|incomplete
   ip prefix-list NAME → (config-pl)#: permit|deny A/L [eq|le|ge N [le N]] · permit|deny object-group NAME
   Сосед: address-family ipv4 unicast → route-map NAME in|out, prefix-list NAME in|out.
   Порядок: правила по номеру, первое совпавшее решает; не совпало ни одно — запрет (в маршрутной карте и в списке префиксов).
   Атрибуты: LOCAL_PREF (100) — только внутри AS; MED — соседней AS, дальше не уходит; community no-export — не за пределы AS, no-advertise — никому.
   Упрощения: список community в match — совпадение, если у маршрута есть все перечисленные; weight, extcommunity, network … route-map не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, IP = EL.ip;
  function touch(st) { st.pending = true; }
  function rule(st) { var p = st.ctx.split('|'); return st.cand.rmaps[p[0]].rules[p[1]]; }
  function bad() { return 'Syntax error: Illegal parameter'; }
  function cmd(modes, pat, fn, d) { S.cmd(modes, pat, fn, d); var c = S.T.pop(); S.T.unshift(c); return c; }
  // A/L [eq N | le N | ge N [le N]]
  function pfx(a, rest) { var c = IP.parseCidr(a); if (!c) return null; var w = String(rest || '').trim().split(/\s+/).filter(Boolean), o = { net: IP.netOf(c.ip, c.len), len: c.len };
    for (var i = 0; i < w.length; i += 2) { var k = w[i], v = +w[i + 1]; if (!/^(eq|le|ge)$/.test(k) || !(v >= 1 && v <= 32)) return null; o[k] = v; } return o; }
  function pfxTxt(o) { return (o.og ? 'object-group ' + o.og : o.net) + (o.eq ? ' eq ' + o.eq : '') + (o.ge ? ' ge ' + o.ge : '') + (o.le ? ' le ' + o.le : ''); }
  function pfxHit(o, net, c) {                      // net 'A/L' попадает в описание o
    var q = net.split('/'), L = +q[1], bases = o.og ? (((c.og || {}).net || {})[o.og] || { items: [] }).items.map(function (x) { return x[2]; }).filter(function (t) { return /\//.test(t); }) : [o.net];
    return bases.some(function (b) { var p = b.split('/'), bl = +p[1]; if (!IP.sameNet(q[0], p[0], bl) || L < bl) return false;
      if (o.eq) return L === o.eq; if (o.ge || o.le) return L >= (o.ge || bl) && L <= (o.le || 32); return L === bl; });
  }
  // ---------------------------------------------------------------- route-map: условия и действия для BGP
  cmd('rmapr', 'match ip address object-group <w>', function (st, a) { rule(st).pfx = { og: a[0] }; touch(st); }, 'Префиксы из object-group network');
  cmd('rmapr', 'match ip address object-group <w> <rest>', function (st, a) { var o = pfx('0.0.0.0/0', a[1]); if (!o) return bad(); o.og = a[0]; delete o.net; rule(st).pfx = o; touch(st); });
  cmd('rmapr', 'match ip address <w>', function (st, a) { var o = pfx(a[0]); if (!o) return bad(); rule(st).pfx = o; touch(st); }, 'Префикс A/L [eq|le|ge N]');
  cmd('rmapr', 'match ip address <w> <rest>', function (st, a) { var o = pfx(a[0], a[1]); if (!o) return bad(); rule(st).pfx = o; touch(st); });
  cmd('rmapr', 'no match ip address', function (st) { delete rule(st).pfx; touch(st); });
  cmd('rmapr', 'match as-path <rest>', function (st, a) { var w = a[0].trim().split(/\s+/), how = /^(begin|contain|end|empty|regex)$/.test(w[0]) ? w.shift() : 'contain';
    if (how === 'regex') { try { new RegExp(w.join(' ')); } catch (e) { return bad(); } }
    else if (how !== 'empty' && (!w.length || w.some(function (x) { return !/^\d+$/.test(x); }))) return bad();
    rule(st).asp = { how: how, v: how === 'regex' ? w.join(' ') : w.map(Number) }; touch(st); }, 'AS_PATH: begin | contain | end AS… | empty | regex');
  cmd('rmapr', 'no match as-path', function (st) { delete rule(st).asp; touch(st); });
  cmd('rmapr', 'match community <rest>', function (st, a) { var w = a[0].trim(); rule(st).mcom = /^regex /.test(w) ? { re: w.slice(6) } : { all: w.split(/[\s,]+/) }; touch(st); }, 'Community маршрута');
  cmd('rmapr', 'no match community', function (st) { delete rule(st).mcom; touch(st); });
  function num(how, v) { return how === 'increment' || how === 'decrement' ? { how: how, v: +v } : { v: +how }; }
  cmd('rmapr', 'action set local-preference <rest>', function (st, a) { var w = a[0].trim().split(/\s+/); if (!/^(\d+|increment|decrement)$/.test(w[0]) || (w[1] && !/^\d+$/.test(w[1]))) return bad();
    rule(st).lp = num(w[0], w[1]); touch(st); }, 'LOCAL_PREF (внутри AS, больше — лучше)');
  cmd('rmapr', 'action set metric bgp <rest>', function (st, a) { var w = a[0].trim().split(/\s+/); if (!/^(\d+|increment|decrement)$/.test(w[0])) return bad();
    rule(st).med = num(w[0], w[1]); touch(st); }, 'MED (соседней AS, меньше — лучше)');
  cmd('rmapr', 'action set as-path prepend <rest>', function (st, a) { var w = a[0].replace(/,/g, ' ').trim().split(/\s+/); if (w.some(function (x) { return !/^\d+$/.test(x); })) return bad();
    rule(st).prep = w.map(Number); touch(st); }, 'Удлинить AS_PATH');
  ['set', 'add', 'remove'].forEach(function (k) {
    cmd('rmapr', 'action ' + k + ' community <rest>', function (st, a) { (rule(st).com = rule(st).com || {})[k] = a[0].trim().split(/[\s,]+/); touch(st); }, { set: 'Заменить community', add: 'Добавить community', remove: 'Убрать community' }[k]); });
  cmd('rmapr', 'action set origin <w>', function (st, a) { var o = { igp: 'i', egp: 'e', incomplete: '?' }[a[0]]; if (!o) return bad(); rule(st).org = o; touch(st); }, 'ORIGIN: igp | egp | incomplete');
  // ---------------------------------------------------------------- prefix-list
  S.PROMPT.pl = '(config-pl)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('pl'); });
  function plist(st) { return st.cand.plists[st.ctx]; }
  cmd('config', 'ip prefix-list <w>', function (st, a) { if (!/^[\w.-]{1,31}$/.test(a[0])) return bad(); var L = st.cand.plists = st.cand.plists || {}; L[a[0]] = L[a[0]] || [];
    st.mode = 'pl'; st.ctx = a[0]; touch(st); }, 'Список префиксов для фильтрации маршрутов');
  cmd('config', 'no ip prefix-list <w>', function (st, a) { if (st.cand.plists) delete st.cand.plists[a[0]]; touch(st); });
  ['permit', 'deny'].forEach(function (act) {
    cmd('pl', act + ' object-group <w>', function (st, a) { plist(st).push({ act: act, og: a[0] }); touch(st); });
    cmd('pl', act + ' <w>', function (st, a) { var o = pfx(a[0]); if (!o) return bad(); o.act = act; plist(st).push(o); touch(st); }, act === 'permit' ? 'Разрешить префикс' : 'Запретить префикс');
    cmd('pl', act + ' <w> <rest>', function (st, a) { var o = pfx(a[0], a[1]); if (!o) return bad(); o.act = act; plist(st).push(o); touch(st); }); });
  cmd('pl', 'exit', function (st) { st.mode = 'config'; st.ctx = null; });
  function nb(st) { return st.cand.bgp.nbr[st.ctx]; }
  cmd('bgpnaf', 'prefix-list <w> <w>', function (st, a) { if (a[1] !== 'in' && a[1] !== 'out') return bad(); (nb(st).pl = nb(st).pl || {})[a[1]] = a[0]; touch(st); }, 'Список префиксов in | out');
  cmd('bgpnaf', 'no prefix-list <w>', function (st, a) { if (nb(st).pl) delete nb(st).pl[a[0]]; touch(st); });
  cmd('bgpnaf', 'route-map <w> <w>', function (st, a) { if (a[1] !== 'in' && a[1] !== 'out') return bad(); (nb(st).rmap = nb(st).rmap || {})[a[1]] = a[0]; touch(st); }, 'Маршрутная карта in | out');
  cmd('bgpnaf', 'no route-map <w>', function (st, a) { if (nb(st).rmap) delete nb(st).rmap[a[0]]; touch(st); });
  S.RUNX.push(function (c, o) {
    Object.keys(c.plists || {}).forEach(function (n) { o.push('ip prefix-list ' + n); c.plists[n].forEach(function (x) { o.push('  ' + x.act + ' ' + pfxTxt(x)); }); o.push('exit'); }); });
  // в running-config route-map печатает pbr.js; добавляем строки BGP-условий и действий
  var pbrDump = null; S.RUNX.forEach(function (f, i) { if (/rmaps/.test(String(f))) pbrDump = i; });
  if (pbrDump !== null) { var f0 = S.RUNX[pbrDump]; S.RUNX[pbrDump] = function (c, o) { var n0 = o.length; f0(c, o); var add = [];
    for (var i = n0; i < o.length; i++) { add.push(o[i]); var m = o[i].match(/^route-map (\S+)$/); if (m) var cur = m[1];
      var r = o[i].match(/^  rule (\d+)$/); if (r && cur) { var R = c.rmaps[cur].rules[r[1]]; extra(R).forEach(function (l) { add.push('    ' + l); }); } }
    o.splice.apply(o, [n0, o.length - n0].concat(add)); }; }
  function extra(R) { var L = [];
    if (R.pfx) L.push('match ip address ' + pfxTxt(R.pfx)); if (R.asp) L.push('match as-path ' + (R.asp.how === 'contain' ? '' : R.asp.how + ' ') + (R.asp.how === 'regex' ? R.asp.v : (R.asp.v || []).join(' ')).trim());
    if (R.mcom) L.push('match community ' + (R.mcom.re ? 'regex ' + R.mcom.re : R.mcom.all.join(',')));
    if (R.lp) L.push('action set local-preference ' + (R.lp.how ? R.lp.how + ' ' : '') + R.lp.v); if (R.med) L.push('action set metric bgp ' + (R.med.how ? R.med.how + ' ' : '') + R.med.v);
    if (R.prep) L.push('action set as-path prepend ' + R.prep.join(' '));
    Object.keys(R.com || {}).forEach(function (k) { L.push('action ' + k + ' community ' + R.com[k].join(',')); }); if (R.org) L.push('action set origin ' + { i: 'igp', e: 'egp', '?': 'incomplete' }[R.org]);
    return L; }
  // ---------------------------------------------------------------- применение к маршруту: null — отброшен
  function arith(cur, x) { return x.how === 'increment' ? cur + x.v : x.how === 'decrement' ? Math.max(0, cur - x.v) : x.v; }
  function rmHit(R, net, e, c) {
    if (R.acl) return false;                       // правило PBR — к BGP не относится
    if (R.pfx && !pfxHit(R.pfx, net, c)) return false;
    if (R.asp) { var p = e.path, v = R.asp.v;
      if (R.asp.how === 'empty' && p.length) return false;
      if (R.asp.how === 'begin' && p.slice(0, v.length).join(' ') !== v.join(' ')) return false;
      if (R.asp.how === 'end' && p.slice(-v.length).join(' ') !== v.join(' ')) return false;
      if (R.asp.how === 'contain' && (' ' + p.join(' ') + ' ').indexOf(' ' + v.join(' ') + ' ') < 0) return false;
      if (R.asp.how === 'regex' && !new RegExp(v).test(p.join(' '))) return false; }
    if (R.mcom) { var cm = e.comm || []; if (R.mcom.re ? !cm.some(function (x) { return new RegExp(R.mcom.re).test(x); }) : !R.mcom.all.every(function (x) { return cm.indexOf(x) >= 0; })) return false; }
    return true;
  }
  function applyMap(c, name, net, e, local) {
    var M = (c.rmaps || {})[name]; if (!M) return e;                // карты нет — как в ПО: фильтр не действует
    var ks = Object.keys(M.rules).map(Number).sort(function (a, b) { return a - b; }), hit = null;
    ks.some(function (k) { if (rmHit(M.rules[k], net, e, c)) { hit = M.rules[k]; return true; } return false; });
    if (!hit || hit.act === 'deny') return null;
    var x = EL.clone(e);
    if (hit.lp) x.lp = arith(x.lp === undefined ? 100 : x.lp, hit.lp);
    if (hit.med) x.med = arith(x.med || 0, hit.med);
    if (hit.prep) x.path = hit.prep.concat(x.path);
    if (hit.org) x.origin = hit.org;
    var cm = (x.comm || []).slice(); if (hit.com) { if (hit.com.set) cm = hit.com.set.slice(); if (hit.com.add) hit.com.add.forEach(function (y) { if (cm.indexOf(y) < 0) cm.push(y); });
      if (hit.com.remove) cm = cm.filter(function (y) { return hit.com.remove.indexOf(y) < 0; }); } x.comm = cm;
    void local; return x;
  }
  function applyPl(c, name, net) { var L = (c.plists || {})[name]; if (!L) return true; var hit = null;
    L.some(function (o) { if (pfxHit(o, net, c)) { hit = o; return true; } return false; }); return !!hit && hit.act === 'permit'; }
  // dir 'out' — у отправителя (c — его конфигурация), 'in' — у получателя
  EL.bgpPol = function (c, nbr, dir, net, e) {
    if (nbr.pl && nbr.pl[dir] && !applyPl(c, nbr.pl[dir], net)) return null;
    if (nbr.rmap && nbr.rmap[dir]) return applyMap(c, nbr.rmap[dir], net, e);
    return e;
  };
})(typeof window !== 'undefined' ? window : global);
