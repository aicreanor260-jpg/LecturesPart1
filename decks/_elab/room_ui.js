/* Комнаты: несколько студентов собирают одну схему. Модель — на сервере (net-cat-rooms), браузер только показывает и шлёт действия.
   Шапка: «Создать комнату» (название, открытая / закрытая, лаба или пустая схема) и «Комнаты» — комнаты курса с участниками,
   «Подключиться» (открытая) / «Попроситься» (закрытая), вход по коду, приглашения. В комнате — окно «Комната»: ссылка с «Копировать» и таймером
   («действует ещё 1:42» — 2 часа, пока владелец один; при совместной работе не сгорает), «Выпустить новую ссылку», «Пригласить из списка»
   (студенты курса, поиск), участники с цветными метками, пункты лабы, «Выйти» / «Закрыть комнату». Всплывашки: «X зовёт в комнату Y — Принять /
   Отклонить», владельцу закрытой — «X хочет войти — Пустить / Отказать». Ссылка — emulator.html#room=<токен>.
   Протокол (тот же сокет, net_ws.js): room.create {name, lab, open} / room.join {code | id | token} / room.knock {id} / room.leave / room.close / focus /
   room.link.new / room.invite {login} / room.invite.answer {id, accept} / room.knock.answer {login, allow} / students {q} / rooms.list →
   room.view {id, code, name, lab, owner, open, link:{url, token, expires}, members, view}, room.patch {seq, by, patch:{view}, out:[{dev, echo, text, prompt}]},
   room.members, room.link, room.err, room.invite {id, name, lab, from}, room.knock {id, login, name}, room.denied, room.note, room.closed,
   rooms {list}, students {list}, room.local {out:[{dev, tab}]}.
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
  var ROOMHASH = (location.hash.match(/^#room=([\w-]+)$/) || [])[1] || null;     // вход по ссылке приглашения
  EL.roomHash = ROOMHASH;
  WS.on('welcome', function (m) { R.invites = m.invites || []; R.myRooms = m.myRooms || []; paintBtn(); if (/^room:/.test(WS.watch || '')) R.watch = true;
    if (ROOMHASH && !R.id && !R.tried) { R.tried = true; enter({ t: 'room.join', token: ROOMHASH }); } });
  WS.on('room.invite', function (m) { R.invites = (R.invites || []).filter(function (x) { return x.id !== m.id; }).concat([m]); paintBtn(); askInvite(m); paintList(); });
  WS.on('room.knock', function (m) { askKnock(m); });
  WS.on('room.denied', function (m) { if (ROOMHASH && !inRoom()) { U.toast('Владелец не пустил в комнату'); leaveLocal(); return; } U.toast('Владелец не пустил в комнату' + (m.why ? ': ' + m.why : '')); var c = document.querySelector('.roomsw .cs'); if (c) c.textContent = 'Отказано' + (m.why ? ': ' + m.why : ''); });
  WS.on('room.note', function (m) { U.toast(m.text || ''); });
  WS.on('room.view', function (m) { var first = !R.id; R.id = m.id; R.code = m.code; R.name = m.name; R.owner = m.owner; R.members = m.members || []; R.open = m.open !== false;
    if (m.link !== undefined) R.link = m.link; R.watch = !!m.watch || /^room:/.test(WS.watch || '');
    if (first) { U.setAutoOff(true); if (R.watch) U.setReadOnly(true); U.closeWin('rooms', true); U.closeWin('roomnew', true); if (ROOMHASH) history.replaceState(null, '', location.pathname + location.search); }
    sync(m.view || {}); paintBtn(); if (first) { U.toast((R.watch ? 'Просмотр комнаты «' : 'Вы в комнате «') + (m.name || m.code) + '»'); openRoom(); } });
  WS.on('room.patch', function (m) { if (!inRoom()) return; if (m.patch && m.patch.view) sync(m.patch.view); out(m.out); });
  WS.on('room.members', function (m) { R.members = m.members || []; U.draw(); paintRoom(); });
  WS.on('room.link', function (m) { R.link = m.link || null; paintRoom(); });
  WS.on('rooms', function (m) { R.list = m.list || []; paintList(); });
  WS.on('students', function (m) { R.students = m.list || []; paintStudents(); });
  WS.on('room.local', function (m) { (m.out || []).forEach(function (o) { var id = S2L[o.dev]; if (!id || o.tab === undefined || o.tab === null) return;   // ответ на Tab — в строку ввода этой консоли
    var tw = U.wins['t' + id] || U.wins.cons, x = tw && tw.el.querySelector('.inp input'); if (x) x.value = o.tab; }); });
  WS.on('room.err', function (m) { if (ROOMHASH && !inRoom()) { U.toast('Ссылка на комнату недействительна: ' + (m.error || 'ошибка')); leaveLocal(); return; }   // к своей работе
    U.toast('Комната: ' + (m.error || 'ошибка')); [].forEach.call(document.querySelectorAll('.roomw .cs, .roomsw .cs'), function (c) { c.textContent = m.error || 'ошибка'; }); });
  WS.on('room.closed', function (m) { U.toast('Комната закрыта' + (m.why ? ': ' + m.why : '')); leaveLocal(); });

  function leaveLocal() { R.id = null; R.net = null; setTimeout(function () { location.hash = ''; location.reload(); }, 600); }
  function enter(o) { var go = function () { WS.send(o); }; if (EL.serverSave && !R.watch && !inRoom()) EL.serverSave().then(go); else go(); }
  function me() { return WS.you() && WS.you().login; }
  function dot(login) { return '<i class="rdot" style="background:' + colOf(login) + '"></i>'; }

  // ---------------------------------------------------------------- кнопки в шапке
  var hdr = document.getElementById('bFit'), bNew = document.createElement('button'), bList = document.createElement('button');
  bNew.className = 'tbtn room-new'; bNew.id = 'bRoomNew'; bList.className = 'tbtn'; bList.id = 'bRooms'; bList.title = 'Комнаты курса: подключиться, войти по коду, приглашения';
  if (hdr) { hdr.parentNode.insertBefore(bNew, hdr); hdr.parentNode.insertBefore(bList, hdr); }
  bNew.addEventListener('click', function () { if (inRoom()) openRoom(); else openNew(); });
  bList.addEventListener('click', openList);
  function paintBtn() { bNew.textContent = inRoom() ? '👥 ' + (R.name || R.code) : 'Создать комнату'; bNew.title = inRoom() ? 'Комната: ссылка, участники, приглашения' : 'Совместная схема: создать комнату';
    bNew.classList.toggle('on', inRoom()); bList.textContent = 'Комнаты' + ((R.invites || []).length ? ' (' + R.invites.length + ')' : ''); bList.hidden = inRoom() || !!R.watch; }
  paintBtn();
  function labOpts() { return '<option value="">Пустая схема</option>' + EL.labs.LABS.map(function (l) { return '<option value="' + esc(l.id) + '">' + esc(l.id + ' — ' + l.title) + '</option>'; }).join(''); }

  // ---------------------------------------------------------------- «Создать комнату»
  function openNew() {
    var body = document.createElement('div'); body.className = 'pad roomw';
    body.innerHTML = '<div class="k">Совместная схема</div><p>Несколько студентов собирают одну схему и видят изменения и консоли друг друга вживую. Ваша работа перед входом сохраняется.</p>' +
      '<label>Название</label><input class="q" data-f="name" placeholder="Группа 21-1, бригада 2" maxlength="60">' +
      '<label>Доступ</label><label class="rad"><input type="radio" name="ropen" value="1" checked> Открытая — войти может любой студент курса</label>' +
      '<label class="rad"><input type="radio" name="ropen" value="0"> Закрытая — по приглашению или с вашего разрешения</label>' +
      '<label>Схема</label><select class="q" data-f="lab">' + labOpts() + '</select>' +
      '<div class="row"><button class="pri" data-r="create">Создать</button><span class="cs"></span></div>';
    body.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter') body.querySelector('[data-r="create"]').click(); });
    body.addEventListener('click', function (e) { if (!e.target.closest('[data-r="create"]')) return; var nm = body.querySelector('[data-f="name"]').value.trim();
      if (!nm) { body.querySelector('.cs').textContent = 'Укажите название'; return; }
      enter({ t: 'room.create', name: nm.slice(0, 60), lab: body.querySelector('[data-f="lab"]').value, open: body.querySelector('[name="ropen"]:checked').value === '1' });
      body.querySelector('.cs').textContent = 'Создаю…'; });
    U.makeWin('roomnew', 'Создать комнату', 'совместная схема', body, { w: 440, h: 430 });
  }

  // ---------------------------------------------------------------- «Комнаты»: список курса, вход по коду, приглашения
  function listHtml() { var L = R.list;
    return '<div class="row"><input class="q" data-f="code" placeholder="код комнаты" maxlength="16"><button class="pri" data-r="join">Войти по коду</button><button data-r="refresh">Обновить</button></div><span class="cs"></span>' +
      ((R.invites || []).length ? '<h3>Приглашения</h3>' + R.invites.map(function (v) { return '<div class="mem"><b>' + esc(v.name || v.code) + '</b><span>' + esc((v.from ? 'от ' + v.from : '') + (v.lab ? ' · лаба ' + v.lab : '')) + '</span><button class="pri" data-r="acc" data-id="' + esc(v.id) + '">Принять</button><button data-r="dec" data-id="' + esc(v.id) + '">Отклонить</button></div>'; }).join('') : '') +
      '<h3>Комнаты курса</h3>' + (!L ? '<p class="cs2">Загружаю…</p>' : !L.length ? '<p class="cs2">Комнат пока нет — создайте свою.</p>' : L.map(function (r) { var M = r.members || [];
        return '<div class="rrow"><div><b>' + esc(r.name) + '</b> <em class="' + (r.open ? 'op' : 'cl') + '">' + (r.open ? 'открытая' : 'закрытая') + '</em><br><span class="cs2">' + esc((r.lab ? 'лаба ' + r.lab + ' · ' : 'схема · ') + 'владелец ' + (r.owner || '—')) + '</span><div class="rmem">' +
          M.map(function (x) { var l = x.login || x; return '<span>' + dot(l) + esc(l) + '</span>'; }).join('') + (M.length ? '' : '<span class="cs2">никого</span>') + '</div></div>' +
          '<button class="pri" data-r="' + (r.open ? 'jid' : 'knock') + '" data-id="' + esc(r.id) + '">' + (r.open ? 'Подключиться' : 'Попроситься') + '</button></div>'; }).join('')); }
  function paintList() { var w = U.wins.rooms; if (!w) return; var b = w.el.querySelector('.roomsw'); if (b) b.innerHTML = listHtml(); }
  function openList() {
    var body = document.createElement('div'); body.className = 'pad roomsw'; body.innerHTML = listHtml(); WS.send({ t: 'rooms.list' });
    body.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter' && e.target.dataset.f === 'code') body.querySelector('[data-r="join"]').click(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-r]'); if (!b) return; var r = b.dataset.r, cs = body.querySelector('.cs');
      if (r === 'join') { var c = body.querySelector('[data-f="code"]').value.trim(); if (!c) { cs.textContent = 'Введите код'; return; } enter({ t: 'room.join', code: c }); }
      if (r === 'refresh') WS.send({ t: 'rooms.list' });
      if (r === 'jid') enter({ t: 'room.join', id: b.dataset.id });
      if (r === 'knock') { enter({ t: 'room.knock', id: b.dataset.id }); cs.textContent = 'Просьба отправлена владельцу — ждите ответа'; }
      if (r === 'acc' || r === 'dec') answerInvite(b.dataset.id, r === 'acc'); });
    U.makeWin('rooms', 'Комнаты', 'совместная схема', body, { w: 520, h: Math.min(560, innerHeight - 140) });
  }

  // ---------------------------------------------------------------- всплывашки: приглашение и просьба войти
  function answerInvite(id, yes) { R.invites = (R.invites || []).filter(function (x) { return String(x.id) !== String(id); }); paintBtn(); paintList(); U.closeWin('rinv' + id, true);
    if (yes) enter({ t: 'room.invite.answer', id: id, accept: true }); else WS.send({ t: 'room.invite.answer', id: id, accept: false }); }
  function askInvite(m) { if (inRoom() || R.watch) return; var body = document.createElement('div'); body.className = 'pad roomw pop';
    body.innerHTML = '<p class="big"><b>' + esc(m.from || 'Однокурсник') + '</b> зовёт в комнату <b>«' + esc(m.name || m.code) + '»</b>' + (m.lab ? ' (лаба ' + esc(m.lab) + ')' : '') + '</p>' +
      '<div class="row"><button class="pri" data-a="y">Принять</button><button data-a="n">Отклонить</button></div>';
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-a]'); if (b) answerInvite(m.id, b.dataset.a === 'y'); });
    U.makeWin('rinv' + m.id, 'Приглашение в комнату', '', body, { w: 400, h: 190, x: innerWidth / 2 - 200, y: 100 }); }
  function askKnock(m) { var body = document.createElement('div'), key = 'rknock' + m.login; body.className = 'pad roomw pop';
    body.innerHTML = '<p class="big">' + dot(m.login) + '<b>' + esc(m.name || m.login) + '</b> хочет войти в комнату <b>«' + esc(R.name || '') + '»</b></p>' +
      '<div class="row"><button class="pri" data-a="y">Пустить</button><button data-a="n">Отказать</button></div>';
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-a]'); if (!b) return; WS.send({ t: 'room.knock.answer', login: m.login, allow: b.dataset.a === 'y' }); U.closeWin(key, true); });
    U.makeWin(key, 'Просьба войти', '', body, { w: 400, h: 190, x: innerWidth / 2 - 200, y: 120 }); }

  // ---------------------------------------------------------------- окно «Комната» (внутри комнаты)
  function left(ex) { var s = Math.max(0, Math.floor((ex - Date.now()) / 1000)); return Math.floor(s / 3600) + ':' + ('0' + Math.floor(s / 60) % 60).slice(-2) + (s < 3600 ? ':' + ('0' + s % 60).slice(-2) : ''); }
  function linkHtml() { var L = R.link, own = R.owner === me(); if (!L || R.watch) return '';
    return '<h3>Ссылка-приглашение</h3><div class="row"><input class="q lnk" readonly value="' + esc(L.url || '') + '"><button class="pri" data-r="copy">Копировать</button></div>' +
      '<p class="cs2 ttl">' + (L.expires ? 'Действует ещё <b data-left>' + left(L.expires) + '</b> — пока вы в комнате одни; когда работаете вместе, не сгорает.' : 'Не сгорает, пока вы работаете вместе.') + '</p>' +
      (own ? '<button data-r="newlink">Выпустить новую ссылку</button>' : ''); }
  function html() { var L = R.lab, m0 = me();
    return '<div class="k">Комната' + (R.watch ? ' · только просмотр' : '') + '</div><h2>' + esc(R.name || '') + ' <em class="' + (R.open ? 'op' : 'cl') + '">' + (R.open ? 'открытая' : 'закрытая') + '</em></h2>' +
      '<p class="cs2">Код: <b class="code">' + esc(R.code || '') + '</b></p>' + linkHtml() +
      (R.watch ? '' : '<h3>Пригласить из списка</h3><input class="q" data-f="sq" placeholder="поиск: фамилия или логин"><div class="slist"></div>') +
      '<h3>В комнате</h3>' + (R.members || []).map(function (m) { var id = m.dev && S2L[m.dev], d = id && net().devs[id];
        return '<div class="mem">' + dot(m.login) + '<b>' + esc(m.name || m.login) + (m.login === m0 ? ' (вы)' : '') + (m.login === R.owner ? ' · владелец' : '') + '</b><span>' + (d ? 'за ' + esc(d.name) : 'смотрит схему') + '</span></div>'; }).join('') +
      (L ? '<h3>Лаба ' + esc(L.id) + ' · ' + esc(L.title || '') + ' — ' + (L.done || []).length + '/' + L.total + '</h3><ol class="rt">' + (L.tasks || []).map(function (t, i) { return '<li' + ((L.done || []).indexOf(i + 1) >= 0 ? ' class="ok"' : '') + '>' + esc(t.t || t) + '</li>'; }).join('') + '</ol>' : '') +
      (R.watch ? '' : '<div class="row"><button data-r="leave">Выйти из комнаты</button>' + (R.owner === m0 ? '<button data-r="close">Закрыть комнату</button>' : '') + '</div>') + '<span class="cs"></span>'; }
  function paintRoom() { var w = U.wins.room; if (!w) return; var b = w.el.querySelector('.roomw'); if (!b) return; var q = b.querySelector('[data-f="sq"]'), qv = q ? q.value : '', foc = document.activeElement === q;
    b.innerHTML = html(); var q2 = b.querySelector('[data-f="sq"]'); if (q2) { q2.value = qv; if (foc) q2.focus(); } paintStudents(); }
  function paintStudents() { var box = document.querySelector('.roomw .slist'); if (!box) return; var inR = {}; (R.members || []).forEach(function (m) { inR[m.login] = 1; });
    var L = (R.students || []).filter(function (s) { return !inR[s.login]; }).slice(0, 30), I = R.invited || {};
    box.innerHTML = L.map(function (s) { return '<div class="mem">' + dot(s.login) + '<b>' + esc(s.name || s.login) + '</b><span>' + esc(s.login) + (s.online ? ' · в сети' : '') + '</span><button data-r="inv" data-login="' + esc(s.login) + '"' + (I[s.login] ? ' disabled' : '') + '>' + (I[s.login] ? 'Приглашён' : 'Пригласить') + '</button></div>'; }).join('') || (R.students ? '<p class="cs2">Никого не нашлось</p>' : ''); }
  setInterval(function () { var t = document.querySelector('.roomw [data-left]'); if (t && R.link && R.link.expires) t.textContent = left(R.link.expires); }, 1000);
  var sqT = null;
  function openRoom() {
    var body = document.createElement('div'); body.className = 'pad roomw'; body.innerHTML = html();
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('input', function (e) { if (e.target.dataset.f !== 'sq') return; clearTimeout(sqT); var q = e.target.value.trim(); sqT = setTimeout(function () { WS.send({ t: 'students', q: q }); }, 300); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-r]'); if (!b) return; var r = b.dataset.r;
      if (r === 'copy') { var x = body.querySelector('.lnk'); x.select(); var ok = function () { b.textContent = 'Скопировано'; setTimeout(function () { b.textContent = 'Копировать'; }, 1500); };
        if (navigator.clipboard) navigator.clipboard.writeText(x.value).then(ok, function () { document.execCommand('copy'); ok(); }); else { document.execCommand('copy'); ok(); } }
      if (r === 'newlink' && confirm('Старая ссылка перестанет действовать. Выпустить новую?')) WS.send({ t: 'room.link.new' });
      if (r === 'inv') { WS.send({ t: 'room.invite', login: b.dataset.login }); R.invited = R.invited || {}; R.invited[b.dataset.login] = 1; paintStudents(); }
      if (r === 'leave') { WS.send({ t: 'room.leave' }); leaveLocal(); }
      if (r === 'close' && confirm('Закрыть комнату для всех?')) WS.send({ t: 'room.close', id: R.id }); });
    U.makeWin('room', 'Комната', R.code || '', body, { w: 460, h: Math.min(640, innerHeight - 120) });
    paintStudents(); if (!R.watch) WS.send({ t: 'students', q: '' });
  }
  EL.roomOpen = openRoom; EL.roomNew = openNew; EL.roomList = openList;
})();
