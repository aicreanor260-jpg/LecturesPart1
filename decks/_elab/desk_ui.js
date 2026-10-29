/* «Рабочий стол» конечного узла (VPC, Debian, Docker) — программы как у ПК в Packet Tracer (сетевая часть — apps.js).
   Открывается из меню устройства (ПКМ → «Рабочий стол»). Работает в обоих режимах: это действия пользователя на ПК, а не подсказки. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  function net() { return U.net(); }
  var items0 = X.items, run0 = X.run;
  X.items = function (k, d) { return items0(k, d) + (k === 'dev' && d && EL.isHost(d) ? '<button data-a="desk"><span>🖥</span>Рабочий стол</button>' : ''); };
  X.run = function (k, a, arg) { run0(k, a, arg); if (k === 'dev' && a === 'desk') openDesk(arg.id); };
  var APPS = [['ip', '⚙', 'Настройка IP'], ['cmd', '▣', 'Командная строка'], ['web', '🌐', 'Веб-браузер'], ['ftp', '⇅', 'FTP-клиент'], ['mail', '✉', 'Почта'],
              ['rem', '⌨', 'Telnet / SSH'], ['ed', '✎', 'Текстовый редактор'], ['gen', '≋', 'Генератор трафика']];
  function v(b, f) { var x = b.querySelector('[data-f="' + f + '"]'); return x ? (x.type === 'checkbox' ? x.checked : x.value.trim()) : ''; }
  function inp(f, val, ph, type) { return '<input class="q" data-f="' + f + '" value="' + esc(val === undefined || val === null ? '' : val) + '"' + (ph ? ' placeholder="' + esc(ph) + '"' : '') + (type === 'password' ? ' type="text" autocomplete="off" data-lpignore="true" style="-webkit-text-security:disc"' : type ? ' type="' + type + '"' : '') + ' spellcheck="false">'; }
  function sel(f, opts, cur) { return '<select class="q" data-f="' + f + '">' + opts.map(function (o) { return '<option value="' + o[0] + '"' + (o[0] === cur ? ' selected' : '') + '>' + esc(o[1]) + '</option>'; }).join('') + '</select>'; }
  function say(b, ok, t) { var o = b.querySelector('.cs'); if (o) { o.textContent = t; o.style.color = ok ? 'var(--ok, #7dffb0)' : 'var(--bad, #ff6b62)'; } }

  function openDesk(id) {
    var n = net(), d = n.devs[id]; if (!d) return;
    var body = document.createElement('div'), app = null; body.className = 'pad desk';
    var st = d.st; st.ui = st.ui || {};
    function home() { app = null; body.innerHTML = '<div class="k">' + esc(d.name) + ' · ' + esc(d.model) + '</div><div class="dgrid">' +
      APPS.map(function (a) { return '<button class="dapp" data-app="' + a[0] + '"><i>' + a[1] + '</i><span>' + esc(a[2]) + '</span></button>'; }).join('') + '</div>'; }
    function head(t) { return '<div class="dhead"><button data-c="home">← Рабочий стол</button><b>' + esc(t) + '</b></div>'; }
    var R = {
      ip: function () { var c = n.ipCfg(id);
        return head('Настройка IP') + '<label class="rad"><input type="radio" name="m' + id + '" data-m="static"' + (c.mode === 'static' ? ' checked' : '') + '> Статический</label>' +
          '<label class="rad"><input type="radio" name="m' + id + '" data-m="dhcp"' + (c.mode === 'dhcp' ? ' checked' : '') + '> DHCP</label>' +
          '<label>IP-адрес</label>' + inp('ip', c.ip, '192.168.1.10') + '<label>Маска подсети</label>' + inp('mask', c.mask || '255.255.255.0') +
          '<label>Шлюз по умолчанию</label>' + inp('gw', c.gw) + '<label>DNS-сервер</label>' + inp('dns', c.dns) +
          '<div class="row"><button class="pri" data-c="apply">Применить</button><span class="cs"></span></div>'; },
      web: function () { return head('Веб-браузер') + '<div class="row">' + inp('url', st.ui.url || 'http://', 'http://адрес или имя') + '<button class="pri" data-c="go">Перейти</button></div>' +
        '<div class="cs2 wst"></div><iframe class="wpage" sandbox="" title="страница"></iframe>'; },
      ftp: function () { var f = st.ui.ftp || { srv: '', user: '' };
        return head('FTP-клиент') + '<label>Сервер</label>' + inp('srv', f.srv, 'адрес или имя') + '<label>Пользователь</label>' + inp('user', f.user) + '<label>Пароль</label>' + inp('pw', '', '', 'password') +
          '<div class="row"><button class="pri" data-c="ls">Подключиться (ls)</button><span class="cs"></span></div><div class="flist"></div>'; },
      mail: function () { var m = st.ui.mail || {};
        return head('Почта') + '<details' + (m.from ? '' : ' open') + '><summary>Настройки почты</summary><label>Мой адрес</label>' + inp('from', m.from, 'user@college.ru') +
          '<label>Сервер исходящей почты (SMTP)</label>' + inp('smtp', m.smtp) + '<label>Сервер входящей почты (POP3)</label>' + inp('pop3', m.pop3) +
          '<label>Пользователь</label>' + inp('user', m.user) + '<label>Пароль</label>' + inp('pw', m.pw, '', 'password') + '</details>' +
          '<h2>Новое письмо</h2><label>Кому</label>' + inp('to') + '<label>Тема</label>' + inp('subj') + '<label>Текст</label><textarea class="q" data-f="text" rows="4"></textarea>' +
          '<div class="row"><button class="pri" data-c="send">Отправить</button><button data-c="recv">Получить</button><span class="cs"></span></div>' +
          '<h2>Входящие</h2><div class="inbox">' + inbox() + '</div>'; },
      rem: function () { var r = st.ui.rem || { proto: 'ssh', host: '', user: 'admin' };
        return head('Telnet / SSH') + '<label>Протокол</label>' + sel('proto', [['ssh', 'SSH (TCP 22)'], ['telnet', 'Telnet (TCP 23)']], r.proto) +
          '<label>Адрес или имя</label>' + inp('host', r.host) + '<label>Пользователь (SSH)</label>' + inp('user', r.user) +
          '<div class="row"><button class="pri" data-c="conn">Подключиться</button><span class="cs"></span></div>'; },
      ed: function () { var D = n.docs(id), L = D.list(), cur = st.ui.doc || L[0] || 'новый.txt';
        return head('Текстовый редактор') + '<div class="row">' + sel('doc', L.map(function (x) { return [x, x]; }).concat([['', '— новый файл —']]), L.indexOf(cur) >= 0 ? cur : '') +
          inp('name', cur, 'имя файла') + '</div><textarea class="q ed" data-f="text" rows="12">' + esc(D.get(cur) || '') + '</textarea>' +
          '<div class="row"><button class="pri" data-c="save">Сохранить</button><button data-c="del">Удалить</button><span class="cs"></span></div>' +
          '<p class="cs2">Файлы — в «Документах»' + (D.dir ? ' (' + esc(D.dir) + ')' : '') + '; их можно отправить на сервер FTP-клиентом.</p>'; },
      gen: function () { var g = st.ui.gen || { proto: 'udp', dst: '', port: 5001, size: 512, rate: 100, dur: 1 };
        return head('Генератор трафика') + '<label>Протокол</label>' + sel('proto', [['udp', 'UDP'], ['tcp', 'TCP'], ['icmp', 'ICMP (эхо-запросы)']], g.proto) +
          '<label>Адрес назначения</label>' + inp('dst', g.dst) + '<label>Порт назначения</label>' + inp('port', g.port, '', 'number') +
          '<label>Размер данных, байт</label>' + inp('size', g.size, '', 'number') + '<label>Частота, пакетов/с</label>' + inp('rate', g.rate, '', 'number') +
          '<label>Длительность, с (до 5)</label>' + inp('dur', g.dur, '', 'number') +
          '<div class="row"><button class="pri" data-c="gen">Запустить</button><span class="cs"></span></div><div class="gres"></div>'; }
    };
    function inbox() { var L = st.inbox || []; return L.length ? L.slice().reverse().map(function (m) { return '<div class="mail"><b>' + esc(m.subj || '(без темы)') + '</b> — от ' + esc(m.from) + '<br>' + esc(m.body).replace(/\n/g, '<br>') + '</div>'; }).join('') : '<p class="cs2">Писем нет</p>'; }
    function open(a) { if (a === 'cmd') { U.openTerm(id); return; } app = a; body.innerHTML = R[a](); if (a === 'ftp' && st.ui.ftpPw !== undefined) void 0; }
    function ftpList(res) { var D = n.docs(id), box = body.querySelector('.flist');
      box.innerHTML = '<h2>На сервере</h2>' + (res.files.length ? res.files.map(function (f) { return '<div class="frow"><span>' + esc(f.name) + ' <i>' + f.size + ' Б</i></span><button data-c="get" data-n="' + esc(f.name) + '">Скачать</button><button data-c="rm" data-n="' + esc(f.name) + '">Удалить</button></div>'; }).join('') : '<p class="cs2">Пусто</p>') +
        '<h2>Документы</h2>' + (D.list().length ? D.list().map(function (x) { return '<div class="frow"><span>' + esc(x) + '</span><button data-c="put" data-n="' + esc(x) + '">Загрузить на сервер</button></div>'; }).join('') : '<p class="cs2">Нет файлов (создайте в текстовом редакторе)</p>'); }
    body.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter' && app === 'web' && e.target.dataset.f === 'url') body.querySelector('[data-c="go"]').click(); });
    body.addEventListener('change', function (e) { if (app === 'ed' && e.target.dataset.f === 'doc') { st.ui.doc = e.target.value || ''; body.innerHTML = R.ed(); if (!st.ui.doc) body.querySelector('[data-f="name"]').value = ''; } });
    body.addEventListener('click', function (e) {
      var ap = e.target.closest('[data-app]'); if (ap) { open(ap.dataset.app); return; }
      var b = e.target.closest('[data-c]'); if (!b) return; var c = b.dataset.c;
      if (c === 'home') { home(); return; }
      if (c === 'apply') { var mo = body.querySelector('[data-m]:checked').dataset.m, r = n.ipSet(id, { mode: mo, ip: v(body, 'ip'), mask: v(body, 'mask'), gw: v(body, 'gw'), dns: v(body, 'dns') });
        body.innerHTML = R.ip(); say(body, r.ok, r.msg); U.draw(); U.refresh(); return; }
      if (c === 'go') { var url = v(body, 'url'); st.ui.url = url; var h = n.httpGet(id, url), stl = body.querySelector('.wst'), fr = body.querySelector('.wpage');
        stl.textContent = h.ok ? (h.code === 200 ? '200 OK' : h.code + ' Not Found') + ' · ' + h.ip + (h.srv ? ' (' + h.srv + ')' : '') + (h.sec ? ' · HTTPS' : '') : 'Не удаётся открыть страницу: ' + h.why;
        fr.srcdoc = h.ok ? h.html : '<p style="font-family:sans-serif;color:#555">Не удаётся получить доступ к сайту.<br>' + esc(h.why) + '</p>'; U.draw(); return; }
      if (c === 'ls' || c === 'get' || c === 'put' || c === 'rm') {
        var srv = v(body, 'srv'), user = v(body, 'user'), pw = v(body, 'pw'); st.ui.ftp = { srv: srv, user: user };
        var op = { ls: 'ls', get: 'get', put: 'put', rm: 'delete' }[c], res = n.ftp(id, srv, user, pw, op, b.dataset.n);
        if (!res.ok) { say(body, false, res.why); return; }
        var lst = op === 'ls' ? res : n.ftp(id, srv, user, pw, 'ls'); say(body, true, res.msg); if (lst.ok) ftpList(lst); return; }
      if (c === 'send' || c === 'recv') { var m = { from: v(body, 'from'), smtp: v(body, 'smtp'), pop3: v(body, 'pop3'), user: v(body, 'user'), pw: v(body, 'pw') }; st.ui.mail = m;
        if (c === 'send') { var sr = n.mailSend(id, m, { to: v(body, 'to'), subj: v(body, 'subj'), body: v(body, 'text') }); say(body, sr.ok, sr.ok ? sr.msg : sr.why);
          if (sr.ok) ['to', 'subj', 'text'].forEach(function (f) { body.querySelector('[data-f="' + f + '"]').value = ''; }); return; }
        var rv = n.mailRecv(id, m); if (!rv.ok) { say(body, false, rv.why); return; }
        st.inbox = (st.inbox || []).concat(rv.msgs); body.querySelector('.inbox').innerHTML = inbox(); say(body, true, rv.msg); return; }
      if (c === 'conn') { var rr = { proto: v(body, 'proto'), host: v(body, 'host'), user: v(body, 'user') }; st.ui.rem = rr;
        if (d.type === 'deb') { U.openTerm(id); U.run(id, rr.proto === 'ssh' ? 'ssh ' + (rr.user || 'root') + '@' + rr.host : 'telnet ' + rr.host); say(body, true, 'Команда выполнена в командной строке ' + d.name); return; }
        var cn = n.remote(id, rr.proto, rr.host); if (!cn.ok) { say(body, false, cn.why); return; }
        U.openTerm(cn.dev); say(body, true, (rr.proto === 'ssh' ? 'SSH' : 'Telnet') + '-сеанс с ' + n.devs[cn.dev].name + ' (' + cn.ip + ') — окно терминала открыто'); return; }
      if (c === 'save' || c === 'del') { var D = n.docs(id), nm = v(body, 'name').replace(/[\/\\]/g, '');
        if (!nm) { say(body, false, 'Укажите имя файла'); return; }
        if (c === 'save') { D.put(nm, body.querySelector('[data-f="text"]').value); st.ui.doc = nm; body.innerHTML = R.ed(); say(body, true, 'Сохранено: ' + nm); }
        else { D.del(nm); st.ui.doc = ''; body.innerHTML = R.ed(); say(body, true, 'Удалено: ' + nm); } return; }
      if (c === 'gen') { var g = { proto: v(body, 'proto'), dst: v(body, 'dst'), port: +v(body, 'port'), size: +v(body, 'size'), rate: +v(body, 'rate'), dur: +v(body, 'dur') }; st.ui.gen = g;
        var gr = n.trafficGen(id, g), box = body.querySelector('.gres'); if (!gr.ok) { say(body, false, gr.why); box.innerHTML = ''; return; }
        var f = gr.res, ms = function (x) { return x === undefined || x === null ? '—' : (x * 1e3).toFixed(3) + ' мс'; };
        say(body, f.recv > 0, 'Отправлено ' + f.sent + ', доставлено ' + f.recv + ', потери ' + f.loss + ' %');
        box.innerHTML = '<p>Задержка ' + (g.proto === 'icmp' ? '(RTT)' : '(в одну сторону)') + ': min ' + ms(f.min) + ', avg ' + ms(f.avg) + ', max ' + ms(f.max) + ', джиттер ' + ms(f.jitter) + '</p>' +
          (gr.refused ? '<p class="cs2">На ' + esc(g.dst) + ' порт ' + g.port + ' никто не слушает — датаграммы доходят, но приложение их не принимает.</p>' : '') +
          (U.mode() === 'test' && gr.sim.links.length ? '<p class="cs2">Загрузка: ' + gr.sim.links.map(function (l) { return esc(l.name) + ' ' + l.util.toFixed(1) + ' %'; }).join(', ') + '</p>' : '');
        U.draw(); return; }
    });
    home();
    U.makeWin('desk' + id, 'Рабочий стол', d.name, body, { w: 460, h: Math.min(620, innerHeight - 120) });
  }
  EL.openDesk = openDesk;
})();
