/* Клиент сервера курса (wss://net-cat.duckdns.org/ws, вход — cookie сайта): работа хранится на сервере, преподаватель видит её вживую.
   Одиночная работа (модель в браузере): hello → welcome {you, msgs, invites, saved}; при открытии лабы (или свободной схемы), если на сервере
   есть сохранение, — «Продолжить с <время>» / «Начать заново» (load → saved); дальше snap (снимок схемы) при изменениях не чаще раза в 5 с
   и по «Сохранить» / «Выйти» / закрытию вкладки; state — пункты лабы; cmd — каждая введённая команда (пароль помечается secret);
   con — новый вывод консолей пачками не чаще 2 раз в секунду (для живого просмотра).
   Сообщения преподавателя: msg → всплывающее окно и история (кнопка «✉» на нижней панели; история приходит в welcome и msgs).
   Просмотр преподавателем: #watch=<логин> → watch; watch.snap — схема студента, watch.con — его консоли; ввод и меню отключены,
   внизу — поле сообщения студенту. Комнаты — room_ui.js (тот же сокет: EL.ws.send, EL.ws.on).
   Не на сайте курса (локальная проверка) клиент не включается. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  var WSURL = (location.search.match(/[?&]wsurl=([^&]+)/) || [])[1];               // локальная проверка: ?wsurl=ws://127.0.0.1:8799
  var SITE = location.hostname === 'net-cat.duckdns.org' || !!WSURL;
  var watchM = location.hash.match(/^#watch=(.+)$/), WATCH = watchM ? decodeURIComponent(watchM[1]) : null;
  var ws = null, ready = false, queue = [], H = {}, you = null, msgs = [], saved = [], lastGen = -1, lastSnap = 0, conBuf = {}, conT = null, labState = '', retry = 0;
  function net() { return U.net(); }
  function curLab() { var li = U.labInfo(); return li ? li.id : 'free'; }
  function send(o) { if (ready && ws && ws.readyState === 1) ws.send(JSON.stringify(o)); else if (queue.length < 200) queue.push(o); }
  function on(t, f) { (H[t] = H[t] || []).push(f); }
  EL.ws = { send: send, on: on, site: SITE, you: function () { return you; }, watch: WATCH };
  if (!SITE) return;
  EL.wsSite = true;

  function connect() {
    try { ws = new WebSocket(WSURL ? decodeURIComponent(WSURL) : (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws'); } catch (e) { return; }
    ws.onopen = function () { ready = true; retry = 0; ws.send(JSON.stringify({ t: 'hello', lab: WATCH ? null : started ? curLab() : startLab || 'free', mode: WATCH ? 'watch' : U.mode() }));
      if (WATCH) ws.send(JSON.stringify(/^room:/.test(WATCH) ? { t: 'watch', room: WATCH.slice(5) } : { t: 'watch', login: WATCH }));
      queue.splice(0).forEach(function (o) { ws.send(JSON.stringify(o)); }); };
    ws.onmessage = function (e) { var m; try { m = JSON.parse(e.data); } catch (er) { return; } (H[m.t] || []).forEach(function (f) { try { f(m); } catch (er) { /* обработчик не должен ронять сокет */ } }); };
    ws.onclose = function (e) { ready = false; if (e.code === 4001 || e.code === 1008) { U.toast('Сессия курса истекла — войдите снова'); return; }
      setTimeout(connect, Math.min(30000, 1000 * Math.pow(2, retry++))); };
  }

  // ---------------------------------------------------------------- приветствие, восстановление работы
  var startLab = null, startFresh = null, started = false, offline = false, live = false;   // live — студент выбрал «Продолжить» / «Начать заново»: до этого ничего не сохраняем
  X.siteStart = function (hashLab, fresh) { startLab = hashLab; startFresh = fresh; U.setAutoOff(true); if (WATCH) { U.setReadOnly(true); return true; }
    setTimeout(function () { if (!started) { started = true; offline = true; U.setAutoOff(false); U.autoOffer(startLab, startFresh); } }, 5000);   // /ws недоступен — тихо работаем как раньше (автосохранение в браузере)
    return true; };
  on('welcome', function (m) { you = m.you || null; msgs = m.msgs || []; saved = m.saved || []; offline = false; paintMsgBtn();
    if (WATCH || started) return; started = true;
    var key = startLab || 'free', hit = saved.filter(function (s) { return s.lab === key; })[0];
    if (!hit) { begin(); return; }
    send({ t: 'load', lab: key }); });
  on('saved', function (m) {
    if (!m.data) { begin(); return; }
    var at = new Date(m.at || Date.now()), p = function (v) { return ('0' + v).slice(-2); }, when = p(at.getDate()) + '.' + p(at.getMonth() + 1) + ' в ' + p(at.getHours()) + ':' + p(at.getMinutes());
    U.ask('На сервере сохранена ваша работа (' + (m.lab === 'free' ? 'свободная схема' : 'лаба ' + m.lab) + ', ' + when + '). Продолжить с этого места?', function () {
      try { U.loadScheme(m.data); if (m.data.now) net().now = m.data.now; U.draw(); lastGen = net().gen; U.toast('Работа восстановлена'); } catch (err) { U.toast('Не удалось восстановить: ' + err.message); startFresh && startFresh(); } go(); }, 'Продолжить с ' + when);
    var w = U.wins.ask, nb = w && w.el.querySelector('[data-q="n"]'); if (nb) nb.textContent = 'Начать заново';
    if (w) w.el.addEventListener('click', function (e) { if (e.target.closest('[data-q="n"],.x,[data-w="close"]')) begin(); }, true); });
  function begin() { if (startLab && startFresh) startFresh(); go(); }
  function go() { U.setAutoOff(false); lastGen = -1; live = true; }

  // ---------------------------------------------------------------- сохранение и журнал
  function snap() { var j = U.snapshot(), s = JSON.stringify(j); if (s.length > 3e6) { U.toast('Схема слишком большая для сохранения на сервер (больше 3 МБ)'); return null; } return j; }
  EL.serverSave = function (j) { if (WATCH || !live) return Promise.resolve(); send({ t: 'snap', lab: curLab(), data: j || snap() }); lastSnap = Date.now(); lastGen = net().gen;
    return new Promise(function (ok) { var t0 = Date.now(); (function wait() { if (!ws || ws.bufferedAmount === 0 || Date.now() - t0 > 3000) ok(); else setTimeout(wait, 50); })(); }); };
  setInterval(function () { if (WATCH || !live || EL.room && EL.room.id) return; var n = net();
    var li = U.labInfo(), st = li ? li.id + ':' + li.done.join(',') + '/' + li.total : 'free'; if (st !== labState) { labState = st; send({ t: 'state', lab: curLab(), mode: U.mode(), done: li ? li.done : [], total: li ? li.total : 0 }); }
    if (n.gen !== lastGen && Date.now() - lastSnap > 5000) { var j = snap(); if (j) { send({ t: 'snap', lab: curLab(), data: j }); lastSnap = Date.now(); } lastGen = n.gen; } }, 1500);
  window.addEventListener('pagehide', function () { if (!WATCH && live && net().gen !== lastGen) { var j = snap(); if (j && ws && ws.readyState === 1) ws.send(JSON.stringify({ t: 'snap', lab: curLab(), data: j })); } });
  var cmd0 = X.onCmd; X.onCmd = function (id, line, secret) { cmd0(id, line, secret); if (WATCH) return; var d = net().devs[id]; if (!d) return;
    send(secret ? { t: 'cmd', name: d.name, line: '***', secret: true } : { t: 'cmd', name: d.name, line: String(line).slice(0, 500) }); };
  var out0 = X.onOut; X.onOut = function (id, text, cls) { out0(id, text, cls); if (WATCH || EL.room && EL.room.id) return; var d = net().devs[id]; if (!d) return;
    conBuf[d.name] = (conBuf[d.name] || '') + text + '\n'; if (!conT) conT = setTimeout(flushCon, 500); };
  function flushCon() { conT = null; Object.keys(conBuf).forEach(function (k) { send({ t: 'con', dev: k, text: conBuf[k].slice(-20000) }); }); conBuf = {}; }

  // ---------------------------------------------------------------- сообщения преподавателя
  var bm = document.createElement('button'); bm.className = 'term-btn msg-btn'; bm.id = 'bMsg'; bm.hidden = true; bm.title = 'Сообщения преподавателя';
  var dock = document.getElementById('bTerm'); if (dock) dock.parentNode.insertBefore(bm, document.getElementById('bPdu') ? document.getElementById('bPdu').nextSibling : dock.nextSibling);
  var unread = 0;
  function paintMsgBtn() { bm.hidden = !msgs.length && !WATCH; bm.textContent = '✉ ' + (WATCH ? 'Написать' : 'Сообщения') + (unread ? ' (' + unread + ')' : ''); bm.classList.toggle('new', !!unread); }
  function fmtAt(a) { var d = new Date(a || Date.now()), p = function (v) { return ('0' + v).slice(-2); }; return p(d.getDate()) + '.' + p(d.getMonth() + 1) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes()); }
  function msgList() { return msgs.length ? msgs.slice().reverse().map(function (m) { return '<div class="mrow"><b>' + esc(m.from || 'Преподаватель') + '</b> <i>' + fmtAt(m.at) + (m.to && /^room:/.test(m.to) ? ' · комнате' : '') + '</i><div>' + esc(m.text).replace(/\n/g, '<br>') + '</div></div>'; }).join('') : '<p class="cs2">Сообщений нет</p>'; }
  function openMsgs() { unread = 0; paintMsgBtn(); var body = document.createElement('div'); body.className = 'pad msgw';
    body.innerHTML = (WATCH ? '<label>Сообщение ' + esc(WATCH) + '</label><textarea class="q" rows="3"></textarea><div class="row"><button class="pri" data-c="send">Отправить</button><span class="cs"></span></div><h2>История</h2>' : '') + '<div class="mlist">' + msgList() + '</div>';
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) { if (!e.target.closest('[data-c="send"]')) return; var ta = body.querySelector('textarea'), t = ta.value.trim(); if (!t) return;
      send({ t: 'msg', to: /^room:/.test(WATCH) ? WATCH : WATCH, text: t.slice(0, 2000) }); ta.value = ''; body.querySelector('.cs').textContent = 'Отправлено'; });
    U.makeWin('msgs', 'Сообщения', WATCH ? 'студенту' : 'от преподавателя', body, { w: 420, h: 380 }); }
  EL.wsMsgs = { open: openMsgs, list: function () { return msgs; }, html: msgList };
  bm.addEventListener('click', openMsgs);
  function popup(m) { var body = document.createElement('div'); body.className = 'pad msgw pop';
    body.innerHTML = '<div class="k">' + esc(m.from || 'Преподаватель') + ' · ' + fmtAt(m.at) + '</div><div class="mtext">' + esc(m.text).replace(/\n/g, '<br>') + '</div><div class="row"><button class="pri" data-c="ok">Понятно</button><button data-c="all">Все сообщения</button></div>';
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-c]'); if (!b) return; U.closeWin('msgpop', true); unread = 0; paintMsgBtn(); if (b.dataset.c === 'all') openMsgs(); });
    U.makeWin('msgpop', 'Сообщение преподавателя', '', body, { w: 400, h: 230, x: innerWidth / 2 - 200, y: 90 }); }
  on('msg', function (m) { msgs.push(m); if (WATCH) { if (U.wins.msgs) U.wins.msgs.el.querySelector('.mlist').innerHTML = msgList(); return; } unread++; paintMsgBtn(); popup(m);
    if (U.wins.msgs) U.wins.msgs.el.querySelector('.mlist').innerHTML = msgList(); });
  on('msgs', function (m) { msgs = m.msgs || msgs; paintMsgBtn(); });

  // ---------------------------------------------------------------- просмотр преподавателем: схема и консоли студента, без ввода
  var wName = {};
  on('watch.snap', function (m) { if (!m.data) { U.toast(WATCH + ': сохранённой работы нет'); return; } try { U.loadScheme(m.data); } catch (er) { U.toast('Не удалось показать схему: ' + er.message); return; }
    wName = {}; net().list().forEach(function (d) { wName[d.name] = d.id; }); U.setReadOnly(true); U.draw(); banner('Просмотр: ' + (m.login || WATCH) + (m.lab && m.lab !== 'free' ? ' · лаба ' + m.lab : '') + (m.at ? ' · ' + fmtAt(m.at) : '')); });
  on('watch.con', function (m) { var id = wName[m.dev]; if (!id) return;
    if (m.tail) U.clearTerm(id);   // хвост консоли при подключении — вместо содержимого
    String(m.text).replace(/\n$/, '').split('\n').forEach(function (l) { U.tlog(id, l, ''); }); });
  on('watch.state', function (m) { banner('Просмотр: ' + (m.login || WATCH) + ' · ' + (m.lab || '') + (m.total ? ' · пункты ' + (m.done || []).length + '/' + m.total : '')); });
  on('watch.inroom', function (m) { banner('Просмотр: ' + WATCH + ' — сейчас в комнате ' + (m.room && (m.room.name || m.room.code) || '')); });
  function banner(t) { var b = document.getElementById('wbar'); if (!b) { b = document.createElement('div'); b.id = 'wbar'; b.className = 'wbar'; document.body.appendChild(b);
      b.addEventListener('click', function (e) { if (e.target.closest('[data-c="msg"]')) openMsgs(); }); }
    b.innerHTML = '<b>👁 ' + esc(t) + '</b><span>только просмотр — ввод и изменения отключены</span><button data-c="msg">✉ Написать</button>'; }
  if (WATCH) { U.setReadOnly(true); paintMsgBtn(); }
  connect();
})();
