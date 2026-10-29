/* Окно «Отказы» режима «Тест» (движок — faults.js): выбрать отказ (кабель, устройство, ошибка конфигурации),
   «Сравнить» — матрица связности до / сразу после / после схождения, пары, сменившие путь, перестроение STP, маршрутов, VRRP;
   «Единые точки отказа» — перебор всех одиночных отказов порциями, таблица по числу потерянных пар.
   Вход: ПКМ по кабелю или устройству («Отказ: что будет?»), пункт поля и кнопка на вкладке «Файл». В «Работе» окна нет. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc, F = EL.faults;
  function net() { return U.net(); }
  function test() { return U.mode() === 'test'; }
  var SYM = { ok: ['✔', 'var(--ok)', 'связь есть, путь тот же'], lost: ['✖', 'var(--bad)', 'связь потеряна'], reroute: ['↻', '#ffd166', 'связь есть, но другим путём'],
    gained: ['✚', '#7fb4ff', 'связь появилась'], none: ['·', 'var(--dim)', 'связи не было и нет'] };
  var pick = null, routers = false, job = null;

  // ---------------------------------------------------------------- меню и панель
  var items0 = X.items, run0 = X.run, side0 = X.side, click0 = X.sideClick, mode0 = X.onMode;
  X.items = function (k, d) { return items0(k, d) + ((k === 'dev' || k === 'link') && test() ? '<button data-a="fault"><span>⚡</span>Отказ: что будет?</button>' : '') +
    (k === 'field' && test() ? '<button data-a="faults"><span>⚡</span>Отказы и единые точки отказа</button>' : ''); };
  X.run = function (k, a, arg) { run0(k, a, arg); if (a === 'faults') open();
    if (a === 'fault' && k === 'link') { var n = net(), L = n.links[arg]; if (L) open({ k: 'link', key: keyOf(n, arg) }, true); }
    if (a === 'fault' && k === 'dev' && arg) open(arg.type === 'vpc' || arg.type === 'deb' ? null : { k: 'dev', key: arg.name }, true); };
  X.side = function (tab) { return side0(tab) + (tab === 'file' && test() ? '<h4>Отказы</h4><button class="act" data-s="faults">Отказы и единые точки отказа</button>' +
    '<p class="note">Внести отказ (обрыв, выключение, ошибка конфигурации) и посмотреть, кто с кем потерял связь, какие пути перестроились; перебор всех одиночных отказов. Схема не меняется — расчёт на копии.</p>' : ''); };
  X.sideClick = function (a) { click0(a); if (a === 'faults') open(); };
  X.onMode = function (m) { mode0(m); if (m === 'work') { job = null; U.closeWin('faults', true); } };
  function keyOf(n, li) { var l = n.links[li], a = n.devs[l.a.dev].name + ':' + l.a.port, b = n.devs[l.b.dev].name + ':' + l.b.port; return a < b ? a + '—' + b : b + '—' + a; }

  // ---------------------------------------------------------------- окно
  function options(n) {
    var E = F.elements(n), cfg = [];
    n.list().forEach(function (d) { cfg = cfg.concat(F.cfgFor(n, d.name)); });
    var grp = function (t, L) { return L.length ? '<optgroup label="' + esc(t) + '">' + L.map(function (x) { var v = JSON.stringify(x);
      return '<option value="' + esc(v) + '"' + (pick && JSON.stringify(pick) === JSON.stringify(stripL(x)) ? ' selected' : '') + '>' + esc(x.label) + '</option>'; }).join('') + '</optgroup>' : ''; };
    return grp('Кабели', E.filter(function (x) { return x.k === 'link'; })) + grp('Устройства', E.filter(function (x) { return x.k === 'dev'; })) + grp('Ошибки конфигурации', cfg);
  }
  function stripL(x) { var o = {}; Object.keys(x).forEach(function (k) { if (k !== 'label') o[k] = x[k]; }); return o; }
  function open(f, go) {
    if (!test()) return; var n = net();
    if (n.list().filter(function (d) { return n.ifaces(d.id).length; }).length < 2) { U.toast('Нужны хотя бы два узла с IP-адресами'); return; }
    if (f) pick = f;
    var body = document.createElement('div'); body.className = 'cap sim flt';
    body.innerHTML = '<div class="cbar"><select data-g="f" style="max-width:52%">' + options(n) + '</select><button data-c="go">Сравнить</button><button data-c="spof">Единые точки отказа</button>' +
      '<label class="cnt"><input type="checkbox" data-g="r"' + (routers ? ' checked' : '') + '> + адреса маршрутизаторов</label></div><div class="det" style="overflow:auto;flex:1">' +
      '<p>Выберите отказ и нажмите «Сравнить». Матрица — кто кого пингует: <b style="color:var(--ok)">✔</b> как было, <b style="color:var(--bad)">✖</b> связь потеряна, ' +
      '<b style="color:#ffd166">↻</b> другим путём, <b style="color:#7fb4ff">✚</b> появилась. В ячейке «сразу → после схождения» (+1 с и +' + F.CONV + ' с модельного времени).</p></div>';
    U.makeWin('faults', 'Отказы', 'что будет, если…', body, { w: Math.min(980, innerWidth - 40), h: Math.min(560, innerHeight - 120), x: 30, y: 80 });
    var sel = body.querySelector('[data-g=f]'), det = body.querySelector('.det');
    if (!pick && sel.value) pick = stripL(JSON.parse(sel.value));
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('change', function (e) { var g = e.target.dataset.g; if (g === 'f') pick = stripL(JSON.parse(e.target.value)); if (g === 'r') routers = e.target.checked; });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-c]'); if (!b) return;
      if (b.dataset.c === 'go') compare(det); if (b.dataset.c === 'spof') spof(det, body); });
    if (go && pick) compare(det);
  }
  function cell(a, b) {
    if (a === b) { var s = SYM[a]; return '<td title="' + esc(s[2]) + '" style="color:' + s[1] + ';text-align:center">' + s[0] + '</td>'; }
    return '<td title="сразу: ' + esc(SYM[a][2]) + '; после схождения: ' + esc(SYM[b][2]) + '" style="text-align:center"><span style="color:' + SYM[a][1] + '">' + SYM[a][0] +
      '</span>→<span style="color:' + SYM[b][1] + '">' + SYM[b][0] + '</span></td>';
  }
  function compare(det) {
    if (!pick) return; var n = net(), R;
    try { R = F.analyze(n, pick, { routers: routers }); } catch (e) { det.innerHTML = '<p>Не удалось посчитать: ' + esc(e.message) + '</p>'; return; }
    var P = {}; R.pairs.forEach(function (p) { P[p.src + '|' + p.dst] = p; });
    var lost = R.pairs.filter(function (p) { return p.after === 'lost'; }).length, rr = R.pairs.filter(function (p) { return p.after === 'reroute'; }).length,
      tmp = R.pairs.filter(function (p) { return p.now === 'lost' && p.after !== 'lost'; }).length;
    var h = '<p><b>' + esc(labelOf(n, R.fault)) + '</b>: после схождения потеряно пар — <b style="color:var(--bad)">' + lost + '</b>, другим путём — <b style="color:#ffd166">' + rr + '</b>' +
      (tmp ? ', временно (до схождения протоколов) — <b>' + tmp + '</b>' : '') + '.</p>';
    h += '<table><thead><tr><th>откуда \\ куда</th>' + R.nodes.map(function (x) { return '<th>' + esc(x) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      R.nodes.map(function (s) { return '<tr><th>' + esc(s) + '</th>' + R.nodes.map(function (t) { var a = R.before[s] && R.before[s][t]; if (!a) return '<td></td>';
        var p = P[s + '|' + t]; return p ? cell(p.now, p.after) : cell(a.ok ? 'ok' : 'none', a.ok ? 'ok' : 'none'); }).join('') + '</tr>'; }).join('') + '</tbody></table>';
    if (R.pairs.length) h += '<h4>Пары, у которых что-то изменилось</h4><table><thead><tr><th>Откуда → куда</th><th>Сразу</th><th>После схождения</th><th>Путь до</th><th>Путь после / причина</th></tr></thead><tbody>' +
      R.pairs.map(function (p) { return '<tr><td>' + esc(p.src + ' → ' + p.dst) + '</td><td style="color:' + SYM[p.now][1] + '">' + esc(SYM[p.now][2]) + '</td><td style="color:' + SYM[p.after][1] + '">' + esc(SYM[p.after][2]) +
        '</td><td>' + esc(p.path0.join(' – ')) + '</td><td style="white-space:normal">' + esc(p.after === 'lost' ? p.why : p.path2.join(' – ')) + '</td></tr>'; }).join('') + '</tbody></table>';
    h += '<h4>Что перестроилось (после схождения)</h4>' + (R.changes.length ? '<table><thead><tr><th>Что</th><th>Где</th><th>Было</th><th>Стало</th></tr></thead><tbody>' +
      R.changes.map(function (c) { return '<tr><td>' + esc(c.kind) + '</td><td>' + esc(c.what) + '</td><td>' + esc(c.before) + '</td><td>' + esc(c.after) + '</td></tr>'; }).join('') + '</tbody></table>' : '<p>Ничего: STP, маршруты и VRRP не изменились.</p>');
    det.innerHTML = h;
  }
  function labelOf(n, f) { if (f.k === 'link') return 'Обрыв кабеля ' + f.key; if (f.k === 'dev') return 'Выключение ' + f.key; return (f.dev || '') + (f.port ? ' ' + f.port : '') + ': ' + ((F.CFG[f.cfg] || {}).t || ''); }
  function spof(det, body) {
    var n = net(), S = F.spof(n, { routers: routers }), all = S.list.length, me = job = {};
    det.innerHTML = '<p>Перебор одиночных отказов: <b class="pr">0</b> из ' + all + '…</p>';
    (function tick() {
      if (job !== me || !document.body.contains(body)) return;
      var more = S.step(); det.querySelector('.pr').textContent = S.res.length;
      if (more) { setTimeout(tick, 0); return; }
      var L = S.res.slice().sort(function (a, b) { return b.lost.length - a.lost.length || b.rerouted - a.rerouted; }), sp = L.filter(function (r) { return r.spof; });
      det.innerHTML = '<p>Пар со связью в исходной схеме: <b>' + S.total + '</b>. Единых точек отказа: <b style="color:var(--bad)">' + sp.length + '</b> из ' + all + ' элементов.' +
        (sp.length ? ' Их отказ разрывает связь, обходного пути нет.' : ' Любой одиночный отказ схема переживает.') + '</p>' +
        '<table><thead><tr><th>Отказ</th><th>Потеряно пар</th><th>Другим путём</th><th>Кто теряет связь</th></tr></thead><tbody>' +
        L.map(function (r) { return '<tr' + (r.spof ? ' style="color:var(--bad)"' : '') + '><td>' + esc(r.fault.label) + '</td><td>' + r.lost.length + (S.total ? ' (' + Math.round(r.lost.length * 100 / S.total) + ' %)' : '') +
          '</td><td>' + r.rerouted + '</td><td style="white-space:normal">' + esc(r.lost.slice(0, 6).join(', ') + (r.lost.length > 6 ? ' …' : '')) + '</td></tr>'; }).join('') + '</tbody></table>';
    })();
  }
})();
