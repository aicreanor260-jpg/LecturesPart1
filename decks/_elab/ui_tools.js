/* Учебные инструменты режима «Тест» поверх ui.js: захват трафика на кабеле (как Wireshark в pnetlab), разбор шага трассы по уровням OSI,
   редактор лабы без кода (схема + текст задания + проверки {ping …} → .json), заметки на схеме, отмена действий на поле (Ctrl+Z),
   экспорт/импорт конфигураций текстом. Заметки и лаба из файла видны и в режиме «Работа». */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  function net() { return U.net(); }
  function test() { return U.mode() === 'test'; }
  function btn(a, ic, t) { return '<button data-a="' + a + '"><span>' + ic + '</span>' + t + '</button>'; }

  // ================================================================== отмена действий на поле
  var stack = [];
  function linkArr(l) { var n = net(); return l ? [n.devs[l.a.dev].name, l.a.port, n.devs[l.b.dev].name, l.b.port] : null; }
  function findLink(a) { var n = net(), A = n.byName(a[0]), B = n.byName(a[2]); if (!A || !B) return -1;
    for (var i = 0; i < n.links.length; i++) { var l = n.links[i];
      if ((l.a.dev === A.id && l.a.port === a[1] && l.b.dev === B.id && l.b.port === a[3]) || (l.b.dev === A.id && l.b.port === a[1] && l.a.dev === B.id && l.a.port === a[3])) return i; }
    return -1; }
  X.linkArr = linkArr;
  X.delOp = function (id) { var n = net(), d = n.devs[id];
    return { k: 'del', dev: { name: d.name, model: d.model, x: d.x, y: d.y, off: !!d.off, st: EL.clone(d.st) },
             links: n.links.filter(function (l) { return l.a.dev === id || l.b.dev === id; }).map(linkArr) }; };
  X.rec = function (op) { if (!op) return; stack.push(op); if (stack.length > 50) stack.shift(); };
  var OPN = { move: 'перемещение', add: 'добавление устройства', del: 'удаление устройства', con: 'новый кабель', dis: 'удаление кабеля', note: 'заметка' };
  X.undo = function () {
    if (!test()) return;
    var op = stack.pop(), n = net(); if (!op) { U.toast('Отменять нечего'); return; }
    var d;
    if (op.k === 'move') { d = n.byName(op.name); if (d) { d.x = op.x; d.y = op.y; } }
    if (op.k === 'add') { d = n.byName(op.name); if (d) { U.closeWin('t' + d.id); U.closeWin('p' + d.id); n.remove(d.id); } }
    if (op.k === 'del') { var v = op.dev; d = n.add(v.model, v.name, v.x, v.y); d.st = EL.clone(v.st); EL.attach(d.st, n, d.id); d.off = v.off;
      op.links.forEach(function (a) { var A = n.byName(a[0]), B = n.byName(a[2]); if (A && B) n.connect(A.id, a[1], B.id, a[3]); }); }
    if (op.k === 'con') { var i = findLink(op.l); if (i >= 0) n.disconnect(i); }
    if (op.k === 'dis') { var A = n.byName(op.l[0]), B = n.byName(op.l[2]); if (A && B) n.connect(A.id, op.l[1], B.id, op.l[3]); }
    if (op.k === 'note') { n.notes = op.before; }
    n.gen++; U.draw(); U.refresh(); U.toast('Отменено: ' + (OPN[op.k] || op.k));
  };

  // ================================================================== меню
  var ITEMS = {
    dev: function () { return test() ? btn('cfg', '⇅', 'Конфигурация текстом…') : ''; },
    link: function () { return test() ? btn('cap', '◉', 'Захват трафика') : ''; },
    field: function () { return test() ? btn('note', '✎', 'Заметка здесь') : ''; }
  };
  X.items = function (k) { return ITEMS[k] ? ITEMS[k]() : ''; };
  X.run = function (k, a, arg) {
    if (k === 'link' && a === 'cap') openCap(arg);
    if (k === 'dev' && a === 'cfg') openCfg(arg.id);
    if (k === 'field' && a === 'note') editNote(null, arg);
  };
  X.onMode = function (m) { if (m === 'work') Object.keys(U.wins).forEach(function (k) { if (/^(cap|cfg|osi|nted|led)/.test(k)) U.closeWin(k, true); }); };

  // ================================================================== захват трафика
  var capSeq = 0;
  function openCap(li) {
    var n = net(), l = n.links[li]; if (!l) return;
    var key = 'cap' + (++capSeq), cap = n.capStart(li), title = n.devs[l.a.dev].name + ' ' + l.a.port + ' ↔ ' + n.devs[l.b.dev].name + ' ' + l.b.port;
    var body = document.createElement('div'); body.className = 'cap';
    body.innerHTML = '<div class="cbar"><button data-c="pause">❚❚ Пауза</button><button data-c="clear">Очистить</button>' +
      '<input placeholder="Фильтр: icmp, arp, !stp, 192.168.1.10, vlan 10…" spellcheck="false"><span class="cnt"></span></div>' +
      '<div class="list"><table><thead><tr><th>No.</th><th>Time</th><th>Src MAC</th><th>Dst MAC</th><th>VLAN</th><th>Type</th><th>Src IP</th><th>Dst IP</th><th>Protocol</th><th>Len</th><th>Info</th></tr></thead><tbody></tbody></table></div>' +
      '<div class="det">Выберите кадр — разбор по уровням. Захват идёт, пока окно открыто: отправьте ping через этот кабель.</div>';
    U.makeWin(key, 'Захват', title, body, { w: Math.min(1040, innerWidth - 40), h: Math.min(560, innerHeight - 120), x: 20, y: 70 });
    var tb = body.querySelector('tbody'), q = body.querySelector('input'), det = body.querySelector('.det'), cnt = body.querySelector('.cnt'), paused = false, selNo = null, pend = false;
    function match(r) { var f = q.value.trim().toLowerCase(); if (!f) return true;
      return f.split(/\s*,\s*|\s+and\s+/).every(function (w) { var neg = w.charAt(0) === '!'; if (neg) w = w.slice(1).trim(); if (!w) return true;
        var hay = [r.proto, r.type, r.sip, r.dip, r.smac, r.dmac, r.info, r.vlan !== null ? 'vlan ' + r.vlan : ''].join(' ').toLowerCase(), hit = hay.indexOf(w) >= 0;
        return neg ? !hit : hit; }); }
    function tr(r) { return '<tr data-no="' + r.no + '" class="p-' + r.proto + (r.no === selNo ? ' on' : '') + '"><td>' + r.no + '</td><td>' + r.t.toFixed(3) + '</td><td>' + r.smac + '</td><td>' + r.dmac + '</td><td>' +
      (r.vlan !== null ? r.vlan : '') + '</td><td>' + r.type + '</td><td>' + (r.sip || '') + '</td><td>' + (r.dip || '') + '</td><td>' + r.proto + '</td><td>' + r.len + '</td><td>' + esc(r.info) + '</td></tr>'; }
    function render() { pend = false; if (!U.wins[key]) return;
      var L = cap.frames.filter(match), lst = body.querySelector('.list'), atEnd = lst.scrollTop + lst.clientHeight >= lst.scrollHeight - 20;
      tb.innerHTML = L.slice(-600).map(tr).join(''); cnt.textContent = L.length + ' / ' + cap.frames.length; if (atEnd) lst.scrollTop = lst.scrollHeight; }
    cap.on = function () { if (!U.wins[key]) { net().capStop(cap); return; } if (!paused && !pend) { pend = true; setTimeout(render, 120); } };
    q.addEventListener('input', render); q.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) {
      var b = e.target.closest('[data-c]');
      if (b && b.dataset.c === 'pause') { paused = !paused; b.textContent = paused ? '▶ Дальше' : '❚❚ Пауза'; if (!paused) render(); }
      if (b && b.dataset.c === 'clear') { cap.frames = []; selNo = null; det.textContent = ''; render(); }
      var row = e.target.closest('tr[data-no]'); if (!row) return;
      selNo = +row.dataset.no; var r = cap.frames.filter(function (x) { return x.no === selNo; })[0]; if (!r) return;
      [].forEach.call(tb.querySelectorAll('tr.on'), function (x) { x.classList.remove('on'); }); row.classList.add('on');
      det.innerHTML = '<div style="padding:0;color:var(--dim)">' + esc(r.from + ' → ' + r.to) + '</div>' + layersHtml(EL.decode(r.f, r.vlan, r.len), true);
    });
    render();
    U.toast('Захват на кабеле ' + title + ' — пока окно открыто');
  }
  function layersHtml(L, open) {
    return L.map(function (x, i) { return '<details' + (open && i > 0 ? ' open' : '') + '><summary><i>' + x.osi + '</i>' + esc(x.name) + '</summary>' +
      x.fields.map(function (f) { return '<div>' + esc(f[0]) + ': ' + esc(String(f[1])) + '</div>'; }).join('') + '</details>'; }).join('');
  }

  // ================================================================== разбор шага трассы по уровням OSI
  var lastStep = null;
  X.onStep = function (s) {
    var box = document.getElementById('trOsi');
    if (!box) { box = document.createElement('div'); box.id = 'trOsi'; box.className = 'osi'; document.getElementById('trNotes').parentNode.appendChild(box);
      box.addEventListener('click', function (e) { if (e.target.closest('[data-o]') && lastStep) openOsi(lastStep); }); }
    lastStep = s && s.f ? s : null;
    if (!lastStep) { box.innerHTML = ''; return; }
    var tags = (s.segs || []).map(function (g) { return g.tag; }).filter(function (t, i, a) { return t !== null && t !== undefined && a.indexOf(t) === i; });
    var L = EL.decode(s.f, tags.length ? tags[0] : null, 0).slice(1);
    box.innerHTML = L.map(function (x) { return '<div><b>' + x.osi + '</b>' + esc(x.name) + '</div>'; }).join('') +
      (tags.length ? '<div><b></b>тег 802.1Q на сегментах: VLAN ' + tags.join(', ') + ' (на access-портах и у ПК кадр без тега)</div>' : '') +
      '<button data-o="1">Разбор подробно</button>';
  };
  function openOsi(s) {
    var tag = (s.segs || []).map(function (g) { return g.tag; }).filter(function (t) { return t !== null && t !== undefined; })[0];
    var body = document.createElement('div'); body.className = 'cap';
    body.innerHTML = '<div class="det" style="border:0">' + '<p style="margin:0 0 6px;color:var(--dim)">' + esc(s.t) + '</p>' + layersHtml(EL.decode(s.f, tag === undefined ? null : tag, 0), true) + '</div>';
    U.closeWin('osi'); U.makeWin('osi', 'Разбор кадра', 'уровни OSI', body, { w: 560, h: Math.min(520, innerHeight - 160) });
  }

  // ================================================================== заметки на схеме
  X.onDraw = function () {
    var g = document.getElementById('gn'), n = net(); if (!g) return; g.innerHTML = '';
    (n.notes || []).forEach(function (o) {
      var lines = String(o.t).split('\n'), w = Math.max.apply(null, lines.map(function (x) { return x.length; })) * 7.6 + 20, h = lines.length * 18 + 12;
      var ng = U.el('g', { 'class': 'note-g', transform: 'translate(' + o.x + ',' + o.y + ')' }, g);
      U.el('rect', { x: 0, y: 0, width: w, height: h, rx: 4 }, ng);
      lines.forEach(function (x, i) { U.el('text', { x: 10, y: 20 + i * 18 }, ng).textContent = x; });
      ng.addEventListener('mousedown', function (e) { e.stopPropagation(); if (e.button !== 0 || !test()) return; dragNote(e, o); });
      ng.addEventListener('dblclick', function (e) { e.stopPropagation(); if (test()) editNote(o); });
      ng.addEventListener('contextmenu', function (e) { e.preventDefault(); e.stopPropagation(); if (test()) editNote(o); });
    });
  };
  function snapNotes() { return EL.clone(net().notes || []); }
  function dragNote(e, o) {
    var p0 = U.toWorld(e.clientX, e.clientY), x0 = o.x, y0 = o.y, before = snapNotes();
    function mv(ev) { var p = U.toWorld(ev.clientX, ev.clientY); o.x = x0 + p.x - p0.x; o.y = y0 + p.y - p0.y; X.onDraw(); }
    function up() { window.removeEventListener('mousemove', mv); window.removeEventListener('mouseup', up); if (o.x !== x0 || o.y !== y0) X.rec({ k: 'note', before: before }); }
    window.addEventListener('mousemove', mv); window.addEventListener('mouseup', up);
  }
  function editNote(o, p) {
    var body = document.createElement('div'); body.className = 'cfgw';
    body.innerHTML = '<textarea spellcheck="false" placeholder="Текст заметки: подпись сети, VLAN, адреса…"></textarea><div class="row"><button class="pri" data-n="ok">Сохранить</button>' +
      (o ? '<button data-n="del">Удалить</button>' : '') + '<button data-n="no">Отмена</button></div>';
    U.closeWin('nted'); U.makeWin('nted', 'Заметка', 'подпись на схеме', body, { w: 420, h: 260 });
    var ta = body.querySelector('textarea'); ta.value = o ? o.t : ''; ta.focus(); ta.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-n]'); if (!b) return; var n = net(), before = snapNotes(), a = b.dataset.n;
      if (a === 'ok' && ta.value.trim()) { if (o) o.t = ta.value.trim(); else (n.notes = n.notes || []).push({ x: p.x, y: p.y, t: ta.value.trim() }); X.rec({ k: 'note', before: before }); }
      if (a === 'del' && o) { n.notes = n.notes.filter(function (x) { return x !== o; }); X.rec({ k: 'note', before: before }); }
      U.closeWin('nted'); X.onDraw(); });
  }

  // ================================================================== лаба из файла: схема + текст задания + проверки
  // задание — по строке; в конце строки можно указать проверку: {ping PC1 192.168.1.1} или {http PC1 10.0.0.5}
  var ulab = null;
  X.saveX = function (j) { var n = net(); if (n.notes && n.notes.length) j.notes = n.notes; if (ulab) j.lab = ulab; };
  X.loadX = function (j) { var n = net(); n.notes = Array.isArray(j.notes) ? j.notes : []; stack = [];
    ulab = j.lab && typeof j.lab === 'object' ? { title: String(j.lab.title || ''), goal: String(j.lab.goal || ''), tasks: (j.lab.tasks || []).map(String) } : null;
    if (ulab) showULab(); };
  function parseTask(t) { var m = String(t).match(/^(.*?)\s*\{\s*(ping|http)\s+(\S+)\s+(\S+)\s*\}\s*$/i); return m ? { t: m[1], chk: { k: m[2].toLowerCase(), from: m[3], to: m[4] } } : { t: t, chk: null }; }
  function showULab() {
    if (!ulab) return; var key = 'ulab', body = document.getElementById('ulabbody');
    if (!U.wins[key]) { body = document.createElement('div'); body.className = 'pad'; body.id = 'ulabbody';
      U.makeWin(key, 'Задание', ulab.title, body, { x: 30, y: 80, w: 470, h: Math.min(560, innerHeight - 160) });
      body.addEventListener('click', function (e) { if (e.target.closest('[data-u="chk"]')) showULab(); }); }
    var ts = ulab.tasks.map(parseTask), ok = 0, hasChk = ts.some(function (x) { return x.chk; });
    var li = ts.map(function (x) { var y = null;
      if (test() && x.chk) { y = x.chk.k === 'ping' ? net().reach(x.chk.from, x.chk.to) : net().http(x.chk.from, x.chk.to); if (y) ok++; }
      return '<li class="' + (y ? 'ok' : '') + '">' + esc(x.t) + '</li>'; }).join('');
    body.innerHTML = '<div class="k">Лабораторная из файла</div><h2>' + esc(ulab.title) + '</h2><p>' + esc(ulab.goal) + '</p><ol>' + li + '</ol>' +
      (test() && hasChk ? '<div class="sum ' + (ok === ts.filter(function (x) { return x.chk; }).length ? 'ok' : '') + '">Проверки: ' + ok + ' из ' + ts.filter(function (x) { return x.chk; }).length +
        '</div><div class="row"><button class="pri" data-u="chk">Проверить</button></div>' : '');
  }
  function openLabEditor() {
    var body = document.createElement('div'), L = ulab || { title: '', goal: '', tasks: [] }; body.className = 'cfgw';
    body.innerHTML = '<label>Название</label><input id="leT" class="q"><label>Цель работы</label><input id="leG" class="q">' +
      '<label>Задания — по одному на строку; проверка в конце строки: {ping PC1 192.168.1.1} или {http PC1 10.0.0.5}</label><textarea id="leS" spellcheck="false"></textarea>' +
      '<div class="row"><button class="pri" data-l="save">Сохранить лабу (.json)</button><button data-l="show">Показать окно задания</button><button data-l="no">Закрыть</button></div>';
    U.closeWin('led'); U.makeWin('led', 'Редактор лабы', 'схема на поле + текст задания', body, { w: 620, h: 520 });
    var t = body.querySelector('#leT'), g = body.querySelector('#leG'), s = body.querySelector('#leS');
    t.value = L.title; g.value = L.goal; s.value = L.tasks.join('\n');
    [t, g, s].forEach(function (x) { x.addEventListener('keydown', function (e) { e.stopPropagation(); }); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-l]'); if (!b) return;
      ulab = { title: t.value.trim() || 'Лабораторная', goal: g.value.trim(), tasks: s.value.split('\n').map(function (x) { return x.trim(); }).filter(Boolean) };
      if (b.dataset.l === 'save') { var j = net().toJSON(); X.saveX(j); download((ulab.title.replace(/[^\wА-Яа-яЁё.-]+/g, '_') || 'lab') + '.json', JSON.stringify(j, null, 1), 'application/json'); }
      if (b.dataset.l === 'show') { U.closeWin('ulab'); showULab(); }
      if (b.dataset.l === 'no') U.closeWin('led'); });
  }
  function download(name, text, type) {
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type: type })); a.download = name;
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
  }

  // ================================================================== конфигурации текстом
  function cfgText(d) { return EL.cfgText(d); }
  function openCfg(id) {
    var n = net(), d = n.devs[id], t = cfgText(d); if (t === null) { U.toast('Конфигурация текстом — для MES и ESR'); return; }
    var body = document.createElement('div'); body.className = 'cfgw';
    body.innerHTML = '<textarea spellcheck="false"></textarea><div class="out-e" style="color:var(--bad);font:500 12px var(--m)"></div>' +
      '<div class="row"><button class="pri" data-g="apply">Применить к ' + esc(d.name) + '</button><button data-g="copy">Копировать</button><button data-g="file">Сохранить .txt</button></div>';
    var key = 'cfg' + id; U.closeWin(key); U.makeWin(key, 'Конфигурация ' + d.name, d.model + ' · running-config', body, { w: 600, h: Math.min(560, innerHeight - 140) });
    var ta = body.querySelector('textarea'), er = body.querySelector('.out-e'); ta.value = t; ta.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-g]'); if (!b) return; var a = b.dataset.g;
      if (a === 'copy') { ta.select(); try { document.execCommand('copy'); U.toast('Скопировано'); } catch (x) { U.toast('Выделено — Ctrl+C'); } }
      if (a === 'file') download(d.name + '.txt', ta.value, 'text/plain');
      if (a === 'apply') { var errs = EL.applyConfig(net(), id, ta.value); er.textContent = errs.join('\n'); ta.value = cfgText(d); U.draw(); U.refresh();
        U.toast(errs.length ? 'Применено с ошибками: ' + errs.length : 'Конфигурация применена'); } });
  }

  // ================================================================== левая панель
  X.side = function (tab) {
    if (tab === 'lab') return '<h4>Лаба из файла</h4><button class="act" data-s="open">Открыть лабу (.json)</button>' + (ulab ? '<button class="act" data-s="ulab">Окно задания: ' + esc(ulab.title) + '</button>' : '') +
      (test() ? '<button class="act" data-s="led">Редактор лабы</button><p class="note">Соберите схему на поле, напишите задание — сохраните .json и раздайте студентам. Строка задания может заканчиваться проверкой {ping PC1 10.0.0.1}.</p>' : '');
    if (tab === 'file') return '<h4>Конфигурации текстом</h4><button class="act" data-s="cfgx">Экспорт всех (.txt)</button><button class="act" data-s="cfgi">Импорт (.txt)</button>' +
      '<p class="note">Текст running-config всех MES и ESR с заголовками «! ==== ИМЯ ====». Импорт применяет каждый блок к устройству с тем же именем. ПКМ по устройству → «Конфигурация текстом» — для одного. Ctrl+Z — отменить действие на поле.</p>';
    return '';
  };
  var fin = document.createElement('input'); fin.type = 'file'; fin.accept = '.txt,text/plain'; fin.hidden = true; document.body.appendChild(fin);
  fin.addEventListener('change', function () { var f = this.files[0]; if (!f) return; var rd = new FileReader();
    rd.onload = function () { var errs = EL.importConfigs(net(), rd.result); U.draw(); U.refresh(); U.toast(errs.length ? 'Импорт: ошибок ' + errs.length + ' — ' + errs[0] : 'Конфигурации применены'); };
    rd.readAsText(f); this.value = ''; });
  X.sideClick = function (a) {
    if (a === 'led') openLabEditor();
    if (a === 'ulab') showULab();
    if (a === 'cfgx') download('configs.txt', EL.exportConfigs(net()), 'text/plain');
    if (a === 'cfgi') fin.click();
  };
})();
