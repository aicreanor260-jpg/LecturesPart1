/* Эмулятор сети Eltex — общие утилиты: адреса, исполнение команд по таблице шаблонов, подсказки «?» и Tab.
   Работает и в браузере, и в node (автотест): всё складывается в глобальный объект EL. */
(function (G) {
  'use strict';
  var EL = G.EL = G.EL || {};
  var E = EL.E = G.EltexCLI;          // движок MES из _dk_cli.js

  // ------------------------------------------------------------------ IPv4
  function ip2n(ip) { var p = String(ip).split('.'); if (p.length !== 4) return null;
    var n = 0; for (var i = 0; i < 4; i++) { if (!/^\d{1,3}$/.test(p[i]) || +p[i] > 255) return null; n = n * 256 + (+p[i]); } return n; }
  function n2ip(n) { return [n >>> 24, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join('.'); }
  function maskN(len) { return len === 0 ? 0 : (0xFFFFFFFF << (32 - len)) >>> 0; }
  function len2mask(len) { return n2ip(maskN(len)); }
  function mask2len(m) { var n = ip2n(m); if (n === null) return null; var l = 0; while (l < 32 && (n & (0x80000000 >>> l))) l++;
    return maskN(l) === n ? l : null; }
  function parseCidr(s) {             // "10.0.0.1/24" → {ip, len}
    var m = String(s).match(/^(\d+\.\d+\.\d+\.\d+)\/(\d{1,2})$/);
    if (!m || ip2n(m[1]) === null || +m[2] > 32) return null; return { ip: m[1], len: +m[2] }; }
  function sameNet(a, b, len) { return ((ip2n(a) & maskN(len)) >>> 0) === ((ip2n(b) & maskN(len)) >>> 0); }
  function netOf(ip, len) { return n2ip((ip2n(ip) & maskN(len)) >>> 0) + '/' + len; }
  EL.ip = { ip2n: ip2n, n2ip: n2ip, maskN: maskN, len2mask: len2mask, mask2len: mask2len, parseCidr: parseCidr, sameNet: sameNet, netOf: netOf };

  // ------------------------------------------------------------------ исполнение строки по таблице
  // таблица: [{modes:[..], pat:[..], run(st,args)}]; шаблоны и сопоставление — из движка MES (E.match)
  function lower(toks) { return toks.map(function (t) { return t.toLowerCase(); }); }
  function runTable(table, st, raw) {
    var line = E.normLine(String(raw).trim());
    if (!line) return '';
    var toks = line.split(/\s+/), low = lower(toks);
    var amb = ambiguous(table, st, low);
    if (amb) return st.dialect === '10' ? '% Ambiguous Command' : '% Ambiguous command';
    for (var i = 0; i < table.length; i++) {
      var c = table[i]; if (c.modes.indexOf(st.mode) < 0 || !dlOk(c, st)) continue;
      var args = E.match(c.pat, low);
      if (!args) continue;
      var ri = c.pat.indexOf('<rest>');
      var orig = E.match(c.pat, toks.map(function (t, j) { return (c.pat[j] === '<w>' || (ri >= 0 && j >= ri)) ? t : low[j]; }));
      var r = c.run(st, orig || args, line);
      return r === undefined || r === null ? '' : r;
    }
    if (table.some(function (c) { return c.modes.indexOf(st.mode) >= 0 && dlOk(c, st) && partial(c.pat, low); })) return '% Incomplete command';
    if (table.some(function (c) { return dlOk(c, st) && E.match(c.pat, low); })) return '% Команда недоступна в этом режиме — проверьте приглашение';
    return '% Unrecognized command';
  }
  // неоднозначное сокращение: строку целиком принимают команды с разными ключевыми словами на одной позиции,
  // а слово — не полное ни одного из них (con → configure / confirm). Точное слово выбирает свою команду (как на железе)
  function isKw(p) { return !!p && p.charAt(0) !== '<'; }
  function ambiguous(table, st, low) {
    var M = table.filter(function (c) { return c.modes.indexOf(st.mode) >= 0 && dlOk(c, st) && E.match(c.pat, low); });
    for (var k = 0; k < low.length && M.length > 1; k++) {
      if (M.some(function (c) { return c.pat.indexOf('<rest>') >= 0 && c.pat.indexOf('<rest>') <= k; })) break;
      var kws = []; M.forEach(function (c) { var p = c.pat[k]; if (isKw(p) && kws.indexOf(p) < 0) kws.push(p); });
      if (kws.length < 2) continue;
      var ex = kws.filter(function (p) { return p === low[k] || (p === 'terminal' && low[k] === 't'); })[0];
      if (!ex) return kws;
      M = M.filter(function (c) { return !isKw(c.pat[k]) || c.pat[k] === ex; });
    }
    return null;
  }
  // диалект ветки ПО: команда с dl есть только в этих ветках, с xdl — во всех, кроме этих
  function dlOk(c, st) { var d = st.dialect || '10'; return (!c.dl || c.dl.indexOf(d) >= 0) && (!c.xdl || c.xdl.indexOf(d) < 0); }
  // токены — строгое начало шаблона (команда не дописана)
  function partial(pat, toks) {
    if (toks.length >= pat.length) return false;
    return E.match(pat.slice(0, toks.length), toks) !== null && pat[toks.length] !== '<rest>';
  }

  // ------------------------------------------------------------------ «?» и Tab
  var PH = { '<n>': '<число>', '<w>': 'WORD', '<ip>': 'A.B.C.D', '<if>': 'gigabitethernet 1/0/N', '<list>': '<список VLAN: 10,20-30>',
             '<mask>': 'A.B.C.D | /длина', '<rest>': 'LINE' };
  function tokOk(p, t) {
    if (p.charAt(0) === '<') return E.match([p], [t]) !== null || p === '<rest>';
    return t === p || (t.length >= 2 && p.indexOf(t) === 0) || (p === 'terminal' && t === 't');
  }
  // варианты следующего слова: для строки «sh» → show…, для «show » → running-config, vlan…
  function candidates(table, mode, raw, st) {
    var line = E.normLine(String(raw)), ends = /\s$/.test(line) || !line.trim();
    var toks = line.trim() ? lower(line.trim().split(/\s+/)) : [];
    var part = ends ? '' : toks.pop();
    var out = [], seen = {}, cr = false;
    table.forEach(function (c) {
      if (c.modes.indexOf(mode) < 0 || (st && !dlOk(c, st))) return;
      for (var k = 0; k < toks.length; k++) {
        if (c.pat[k] === '<rest>') return;
        if (k >= c.pat.length || !tokOk(c.pat[k], toks[k])) return;
      }
      if (toks.length === c.pat.length && ends) { cr = true; return; }
      var p = c.pat[toks.length]; if (!p) return;
      if (p.charAt(0) === '<') { if (!part || tokOk(p, part)) { if (!seen[p]) { seen[p] = 1; out.push({ w: PH[p] || p, ph: true, d: c.d || '' }); } } return; }
      if (part && p.indexOf(part) !== 0) return;
      if (!seen[p]) { seen[p] = 1; out.push({ w: p, ph: false, d: toks.length === 0 ? (c.d || '') : '' }); }
    });
    if (cr) out.push({ w: '<cr>', ph: true, d: 'выполнить команду' });
    return { list: out, part: part };
  }
  function help(table, mode, raw, st) {
    var c = candidates(table, mode, raw, st);
    if (!c.list.length) return '% Unrecognized command';
    return c.list.map(function (x) { return '  ' + (x.w + '                        ').slice(0, 24) + x.d; }).join('\n');
  }
  function tab(table, mode, raw, st) {
    var c = candidates(table, mode, raw, st);
    var kw = c.list.filter(function (x) { return !x.ph; });
    if (!c.part || !kw.length) return null;
    if (kw.length === 1) return raw.replace(/\S+$/, kw[0].w) + ' ';
    var exact = kw.filter(function (x) { return x.w === c.part; })[0]; if (exact) return raw.replace(/\S+$/, exact.w) + ' ';
    // несколько вариантов: дописать до самого длинного общего начала (con → conf); дальше — null, и интерфейс покажет варианты, как «?»
    var lcp = kw.reduce(function (a, x) { var i = 0; while (i < a.length && i < x.w.length && a[i] === x.w[i]) i++; return a.slice(0, i); }, kw[0].w);
    return lcp.length > c.part.length ? raw.replace(/\S+$/, lcp) : null;
  }
  EL.cli = { dlOk: dlOk, runTable: runTable, help: help, tab: tab, candidates: candidates };

  // ------------------------------------------------------------------ мелочи
  EL.clone = function (o) { return JSON.parse(JSON.stringify(o)); };
  EL.rnd = function (a, b) { return a + Math.floor(Math.random() * (b - a + 1)); };
  EL.pick = function (a) { return a[EL.rnd(0, a.length - 1)]; };
  EL.mac = function (seed) {           // стабильный MAC по имени устройства/порта, OUI Eltex-подобный
    var h = 0; for (var i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0;
    var b = ['e0', 'd9', 'e3', (h >>> 16 & 255), (h >>> 8 & 255), (h & 255)];
    return b.map(function (x) { return (typeof x === 'number' ? (x + 256).toString(16).slice(1) : x); }).join(':');
  };
})(typeof window !== 'undefined' ? window : global);
