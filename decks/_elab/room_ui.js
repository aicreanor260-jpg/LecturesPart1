/* Комнаты: несколько студентов собирают одну схему. Модель — на сервере (net-cat-rooms), браузер только показывает и шлёт действия.
   Окно «Комната» (кнопка «👥 Комната» на нижней панели): создать (название, лаба или пустая схема), войти по коду, приглашения, свои комнаты;
   в комнате — код, участники (кто за каким устройством), пункты лабы, «Выйти из комнаты», «Закрыть комнату» (владелец).
   Протокол (тот же сокет, net_ws.js): room.create / room.join / room.leave / room.close / focus → room.view {id, code, name, lab, owner, members, view},
   room.patch {seq, by, patch:{view}, out:[{dev, echo, text, prompt}]}, room.members, room.err, room.invite, room.closed, room.local {out:[{dev, tab}]}.
   view = {time, devs:[{id, name, model, type, x, y, off, ports}], links:[{i, a, pa, b, pb}], lab} — всегда целиком; локально строится только
   картинка (EL.Net без выполнения команд): добавление, перемещение, удаление, кабели, питание, переименование, выбор лабы, команды консоли
   и Tab уходят на сервер действием act. Консоль устройства общая: вывод (echo — команда с приглашением, text — ответ) приходит всем.
   На схеме у устройства — цветная метка с логином того, кто сейчас за ним (focus при открытии консоли или выборе устройства).
   Перед входом в комнату своя работа сохраняется на сервер; выход из комнаты — перезагрузка и возврат к своей работе. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc, WS = EL.ws;
  if (!WS || !WS.site) return;
  var R = EL.room = { id: null }, S2L = {}, L2S = {}, links = [], prompts = {}, lastFocus = null, pending = null;
  function net() { return U.net(); }
  function inRoom() { return !!R.id; }
  var COL = ['#6fe3ea', '#ffc65c', '#c99bff', '#7dffb0', '#ff8a7a', '#8fb4ff', '#f5a6e6', '#b8f06a'];
  function colOf(login) { var h = 0; String(login).split('').forEach(function (c) { h = (h * 31 + c.charCodeAt(0)) >>> 0; }); return COL[h % COL.length]; }

  // ---------------------------------------------------------------- картинка схемы из view (без выполнения команд)
  function sync(view) {
    var n = net(), seen = {};
    if (!R.net) { n = new EL.Net(); R.net = n; S2L = {}; L2S = {}; U.setNet(n); }
    n.now = view.time || n.now;
    (view.devs || []).forEach(function (v) { seen[v.id] = 1; var lid = S2L[v.id], d = lid && n.devs[lid];
      if (!d) { try { d = n.add(v.model, v.name, v.x, v.y); } catch (er) { d = n.add(v.model, null, v.x, v.y); } S2L[v.id] = d.id; L2S[d.id] = v.id; }
      d.x = v.x; d.y = v.y; d.off = !!v.off; if (v.prompt !== undefined) prompts[d.id] = v.prompt; if (d.name !== v.name && !n.byName(v.name)) n.rename(d.id, v.name); });
    Object.keys(S2L).forEach(function (sid) { if (seen[sid]) return; var lid = S2L[sid]; if (n.devs[lid]) n.remove(lid); delete L2S[lid]; delete S2L[sid]; });
    n.links = []; links = [];
    (view.links || []).forEach(function (l) { var a = S2L[l.a], b = S2L[l.b]; if (!a || !b) return; var er = n.connect(a, l.pa, b, l.pb, l.cab); if (!er) links.push(l.i); });
    n.gen++; R.lab = view.lab || null; U.draw(); U.refresh(); paintRoom(); n.list().forEach(function (d) { U.setPr(d.id); });
  }
  function out(L) { (L || []).forEach(function (o) { var id = S2L[o.dev]; if (!id) return;
    if (o.prompt !== undefined) prompts[id] = o.prompt;
    if (o.echo) U.tlog(id, o.echo, 'c'); if (o.text) U.tlog(id, String(o.text).replace(/\n$/, ''), /^%|Error|not found|Unknown|incorrect/i.test(o.text) ? 'e' : '');
    U.setPr(id); }); }

  // ---------------------------------------------------------------- перехваты действий интерфейса
  function act(a) { if (inRoom() && R.watch) { U.toast('Только просмотр'); return; } WS.send({ t: 'act', a: a }); }
  X.roomAct = function (a) { if (!inRoom()) return false; var b = EL.clone(a);
    ['dev', 'id', 'a', 'b'].forEach(function (k) { if (b[k] !== undefined && L2S[b[k]]) b[k] = L2S[b[k]]; });
    if (b.k === 'link.del') b.i = links[a.i];
    act(b); return true; };
  X.roomRun = function (id, line) { if (!inRoom()) return false; if (L2S[id]) act({ k: 'cli', dev: L2S[id], line: String(line).slice(0, 500) }); return true; };
  X.roomTab = function (id, line) { if (!inRoom()) return false; if (L2S[id]) act({ k: 'tab', dev: L2S[id], line: line }); return true; };
  X.roomPrompt = function (id) { return inRoom() ? (prompts[id] !== undefined ? prompts[id] : '') : null; };
  // кто за каким устройством: выбор устройства или открытая консоль → focus
  setInterval(function () { if (!inRoom() || R.watch) return; var a = document.querySelector('.ctab.on'), id = a ? a.getAttribute('data-id') : null;
    var f = id && L2S[id] ? L2S[id] : null; if (f !== lastFocus) { lastFocus = f; WS.send({ t: 'focus', dev: f }); } }, 700);
  var od = X.onDraw; X.onDraw = function () { od(); var g = document.getElementById('gc'); if (!g || !inRoom()) return;
    (R.members || []).forEach(function (m, k) { var id = m.dev && S2L[m.dev], d = id && net().devs[id]; if (!d) return;
      var c = colOf(m.login), w = String(m.login).length * 7.6 + 16, off = (R.members.filter(function (x, j) { return j < k && x.dev === m.dev; }).length) * 20;
      var t = U.el('g', { 'class': 'rtag', transform: 'translate(' + d.x + ',' + (d.y - 58 - off) + ')' }, g);
      U.el('rect', { x: -w / 2, y: -10, width: w, height: 18, rx: 9, style: 'fill:' + c }, t); U.el('text', { y: 3 }, t).textContent = m.login; }); };

  // ---------------------------------------------------------------- сообщения сервера
  WS.on('welcome', function (m) { R.invites = m.invites || []; R.myRooms = m.myRooms || []; paintBtn(); if (/^room:/.test(WS.watch || '')) R.watch = true; });
  WS.on('room.invite', function (m) { R.invites = (R.invites || []).concat([m]); paintBtn(); U.toast('Приглашение в комнату «' + (m.name || m.code) + '»'); if (U.wins.room) paintRoom(); });
  WS.on('room.view', function (m) { var first = !R.id; R.id = m.id; R.code = m.code; R.name = m.name; R.owner = m.owner; R.members = m.members || []; R.watch = !!m.watch || /^room:/.test(WS.watch || '');
    if (first) { U.setAutoOff(true); if (R.watch) U.setReadOnly(true); }
    sync(m.view || {}); paintBtn(); if (first) { U.toast((R.watch ? 'Просмотр комнаты «' : 'Вы в комнате «') + (m.name || m.code) + '»'); openRoom(); } });
  WS.on('room.patch', function (m) { if (!inRoom()) return; if (m.patch && m.patch.view) sync(m.patch.view); out(m.out); });
  WS.on('room.members', function (m) { R.members = m.members || []; U.draw(); paintRoom(); });
  WS.on('room.local', function (m) { (m.out || []).forEach(function (o) { var id = S2L[o.dev]; if (!id || o.tab === undefined || o.tab === null) return;   // ответ на Tab — в строку ввода этой консоли
    var tw = U.wins['t' + id] || U.wins.cons, x = tw && tw.el.querySelector('.inp input'); if (x) x.value = o.tab; }); });
  WS.on('room.err', function (m) { U.toast('Комната: ' + (m.error || 'ошибка')); var cs = document.querySelector('.roomw .cs'); if (cs) cs.textContent = m.error || 'ошибка'; });
  WS.on('room.closed', function (m) { U.toast('Комната закрыта' + (m.why ? ': ' + m.why : '')); leaveLocal(); });

  function leaveLocal() { R.id = null; R.net = null; setTimeout(function () { location.hash = ''; location.reload(); }, 600); }
  function enter(o) { var go = function () { WS.send(o); }; if (EL.serverSave && !R.watch) EL.serverSave().then(go); else go(); }

  // ---------------------------------------------------------------- окно и кнопка
  var bt = document.createElement('button'); bt.className = 'term-btn room-btn'; bt.id = 'bRoom'; bt.title = 'Совместная схема: комнаты';
  var after = document.getElementById('bMsg') || document.getElementById('bPdu') || document.getElementById('bTerm'); if (after) after.parentNode.insertBefore(bt, after.nextSibling);
  bt.addEventListener('click', openRoom);
  function paintBtn() { bt.textContent = inRoom() ? '👥 ' + (R.name || R.code) : '👥 Комната' + ((R.invites || []).length ? ' (' + R.invites.length + ')' : ''); bt.classList.toggle('on', inRoom()); }
  paintBtn();
  function labOpts() { return '<option value="">Пустая схема</option>' + EL.labs.LABS.map(function (l) { return '<option value="' + esc(l.id) + '">' + esc(l.id + ' — ' + l.title) + '</option>'; }).join(''); }
  function paintRoom() { var w = U.wins.room; if (!w) return; var b = w.el.querySelector('.roomw'); if (b) b.innerHTML = html(); }
  function html() {
    if (inRoom()) { var me = WS.you() && WS.you().login, L = R.lab;
      return '<div class="k">Комната' + (R.watch ? ' · только просмотр' : '') + '</div><h2>' + esc(R.name || '') + '</h2><p>Код для входа: <b class="code">' + esc(R.code || '') + '</b> — сообщите его одногруппникам.</p>' +
        '<h3>Участники</h3>' + (R.members || []).map(function (m) { var id = m.dev && S2L[m.dev], d = id && net().devs[id];
          return '<div class="mem"><i style="background:' + colOf(m.login) + '"></i><b>' + esc(m.login) + (m.login === me ? ' (вы)' : '') + (m.login === R.owner ? ' · владелец' : '') + '</b><span>' + (d ? 'за ' + esc(d.name) : 'смотрит схему') + '</span></div>'; }).join('') +
        (L ? '<h3>Лаба ' + esc(L.id) + ' · ' + esc(L.title || '') + ' — ' + (L.done || []).length + '/' + L.total + '</h3><ol class="rt">' + (L.tasks || []).map(function (t, i) { return '<li' + ((L.done || []).indexOf(i + 1) >= 0 ? ' class="ok"' : '') + '>' + esc(t.t || t) + '</li>'; }).join('') + '</ol>' : '') +
        (R.watch ? '' : '<div class="row"><button data-r="leave">Выйти из комнаты</button>' + (R.owner === me ? '<button data-r="close">Закрыть комнату</button>' : '') + '</div>') + '<span class="cs"></span>'; }
    return '<div class="k">Совместная схема</div><p>Несколько студентов собирают одну схему: каждый видит изменения и консоли других вживую. Ваша работа перед входом сохраняется.</p>' +
      '<h3>Создать комнату</h3><input class="q" data-f="name" placeholder="Название: Группа 21-1, бригада 2" maxlength="60"><select class="q" data-f="lab">' + labOpts() + '</select><div class="row"><button class="pri" data-r="create">Создать</button></div>' +
      '<h3>Войти по коду</h3><div class="row"><input class="q" data-f="code" placeholder="код комнаты" maxlength="16"><button class="pri" data-r="join">Войти</button></div>' +
      ((R.invites || []).length ? '<h3>Приглашения</h3>' + R.invites.map(function (v) { return '<div class="mem"><b>' + esc(v.name || v.code) + '</b><span>' + esc(v.lab ? 'лаба ' + v.lab : '') + '</span><button data-r="jc" data-code="' + esc(v.code) + '">Войти</button></div>'; }).join('') : '') +
      ((R.myRooms || []).length ? '<h3>Мои комнаты</h3>' + R.myRooms.map(function (v) { return '<div class="mem"><b>' + esc(v.name || v.code) + '</b><span>' + esc(v.code || '') + '</span><button data-r="jc" data-code="' + esc(v.code) + '">Войти</button></div>'; }).join('') : '') + '<span class="cs"></span>'; }
  function openRoom() {
    var body = document.createElement('div'); body.className = 'pad roomw'; body.innerHTML = html();
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-r]'); if (!b) return; var r = b.dataset.r, v = function (k) { var x = body.querySelector('[data-f="' + k + '"]'); return x ? x.value.trim() : ''; };
      if (r === 'create') { if (!v('name')) { body.querySelector('.cs').textContent = 'Укажите название'; return; } enter({ t: 'room.create', name: v('name'), lab: v('lab') }); }
      if (r === 'join') { if (!v('code')) { body.querySelector('.cs').textContent = 'Введите код'; return; } enter({ t: 'room.join', code: v('code') }); }
      if (r === 'jc') enter({ t: 'room.join', code: b.dataset.code });
      if (r === 'leave') { WS.send({ t: 'room.leave' }); leaveLocal(); }
      if (r === 'close' && confirm('Закрыть комнату для всех?')) WS.send({ t: 'room.close', id: R.id }); });
    U.makeWin('room', 'Комната', inRoom() ? R.code : 'совместная схема', body, { w: 440, h: Math.min(600, innerHeight - 140) });
  }
  EL.roomOpen = openRoom;
})();
