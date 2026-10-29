/* Окно «Службы» сервера Debian (как вкладка Services у сервера в Packet Tracer): включение галочкой и настройка в окошке.
   Всё пишется в те же файлы и st.svc, что меняют команды Debian (srv.js), — что включено галочкой, видно в systemctl status, и наоборот. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc, S = EL.srv;
  function net() { return U.net(); }
  var items0 = X.items, run0 = X.run;
  function srvHost(d) { return d && d.type === 'deb' && d.model !== 'Docker'; }
  X.items = function (k, d) { return items0(k, d) + (k === 'dev' && srvHost(d) ? '<button data-a="srv"><span>⚙</span>Службы</button>' : ''); };
  X.run = function (k, a, arg) { run0(k, a, arg); if (k === 'dev' && a === 'srv') openSrv(arg.id); };
  var LIST = [['dhcp', 'DHCP'], ['dns', 'DNS'], ['http', 'HTTP / HTTPS'], ['ftp', 'FTP'], ['mail', 'Почта'], ['tftp', 'TFTP'], ['ntp', 'NTP'], ['syslog', 'Syslog'], ['radius', 'RADIUS'], ['tacacs', 'TACACS+']];
  // таблица с полями ввода: cols [[ключ, заголовок, ширина]], rows — массив объектов
  function tbl(name, cols, rows) { rows = rows.length ? rows : [{}]; return '<table class="stab" data-t="' + name + '"><thead><tr>' + cols.map(function (c) { return '<th>' + esc(c[1]) + '</th>'; }).join('') + '<th></th></tr></thead><tbody>' +
    rows.map(function (r, i) { return '<tr data-r="' + i + '">' + cols.map(function (c) { return '<td><input class="q" data-k="' + c[0] + '" value="' + esc(r[c[0]] === undefined ? '' : r[c[0]]) + '" spellcheck="false"></td>'; }).join('') +
      '<td><button data-c="delrow" title="Удалить">✕</button></td></tr>'; }).join('') + '</tbody></table><button data-c="addrow" data-t2="' + name + '">+ Строка</button>'; }
  function rowsOf(box, name) { return [].map.call(box.querySelectorAll('table[data-t="' + name + '"] tbody tr'), function (tr) { var o = {};
    [].forEach.call(tr.querySelectorAll('[data-k]'), function (x) { o[x.dataset.k] = x.value.trim(); }); return o; }).filter(function (o) { return Object.keys(o).some(function (k) { return o[k]; }); }); }
  function files(st, dir) { return Object.keys(st.files).filter(function (k) { return k.indexOf(dir) === 0; }).sort(); }

  function openSrv(id) {
    var n = net(), d = n.devs[id]; if (!d) return; var st = d.st, cur = 'dhcp', pick = {};
    var body = document.createElement('div'); body.className = 'pad srvw';
    function render() {
      body.innerHTML = '<div class="k">' + esc(d.name) + ' · службы</div><div class="scols"><div class="slist">' + LIST.map(function (s) {
        return '<button data-s="' + s[0] + '"' + (s[0] === cur ? ' class="on"' : '') + '><i class="' + (S.on(st, s[0]) ? 'up' : '') + '"></i>' + esc(s[1]) + '</button>'; }).join('') + '</div><div class="spane">' + pane() + '</div></div>';
    }
    function head(t) { return '<div class="dhead"><b>' + esc(t) + '</b><label class="rad"><input type="checkbox" data-c="tog"' + (S.on(st, cur) ? ' checked' : '') + '> Включено</label></div>' +
      '<p class="cs2">' + S.UNITS[cur].map(function (u) { return 'systemctl status ' + u + ': ' + (st.svc[u] ? 'active (running)' : 'inactive (dead)'); }).join('<br>') + '</p>'; }
    function save(t) { return '<div class="row"><button class="pri" data-c="save">' + (t || 'Сохранить и перезапустить') + '</button><span class="cs"></span></div>'; }
    function pane() {
      var P = {
        dhcp: function () { return head('DHCP — isc-dhcp-server') + '<p class="cs2">/etc/dhcp/dhcpd.conf · адреса выдаются в сети сервера и через ретранслятор (ip helper-address на ESR)</p>' +
          tbl('pool', [['net', 'Сеть', '96px'], ['mask', 'Маска', '104px'], ['from', 'Начало', '96px'], ['to', 'Конец', '96px'], ['gw', 'Шлюз', '96px'], ['dns', 'DNS', '96px']], S.dhcpRead(st)) + save(); },
        dns: function () { var Z = S.dnsRead(st), z = Z.filter(function (x) { return x.zone === pick.zone; })[0] || Z[0];
          return head('DNS — bind9') + '<p class="cs2">/etc/bind/named.conf.local и файлы зон · записи A, CNAME, MX</p><div class="row"><select class="q" data-f="zone">' +
            Z.map(function (x) { return '<option' + (z && x.zone === z.zone ? ' selected' : '') + '>' + esc(x.zone) + '</option>'; }).join('') + '</select><input class="q" data-f="nz" placeholder="новая зона: college.ru"><button data-c="addzone">+ Зона</button></div>' +
            (z ? tbl('rec', [['name', 'Имя (@ — сама зона)', '130px'], ['type', 'Тип A/CNAME/MX', '70px'], ['val', 'Значение', '140px'], ['pref', 'MX-приоритет', '50px']], z.recs) + save() : '<p class="cs2">Зон нет — добавьте зону.</p>'); },
        http: function () { var L = files(st, '/var/www/html/'), f = pick.web || L[0] || '/var/www/html/index.html';
          return head('HTTP / HTTPS — apache2') + '<label class="rad"><input type="checkbox" data-c="https"' + (st.srv.https ? ' checked' : '') + '> HTTPS (TCP 443, a2enmod ssl)</label>' +
            '<div class="row"><select class="q" data-f="web">' + L.concat(L.indexOf(f) < 0 ? [f] : []).map(function (x) { return '<option' + (x === f ? ' selected' : '') + '>' + esc(x) + '</option>'; }).join('') + '</select>' +
            '<input class="q" data-f="nf" placeholder="новый файл: lab.html"><button data-c="newfile">+ Файл</button></div>' +
            '<textarea class="q" data-f="page" rows="9">' + esc(st.files[f] !== undefined ? st.files[f] : EL.webDefault) + '</textarea>' + save('Сохранить страницу') + '<button data-c="delfile">Удалить файл</button>'; },
        ftp: function () { return head('FTP — vsftpd') + '<p class="cs2">Пользователи — учётные записи сервера (их же видят вход в консоль, SSH, POP3); каталог — домашний (/root, /home/ИМЯ).</p>' +
          tbl('usr', [['name', 'Пользователь', '130px'], ['pw', 'Пароль', '130px']], S.users(st)) + save('Сохранить пользователей') +
          '<h2>Файлы</h2>' + (files(st, '/home/').concat(files(st, '/root/')).map(function (k) { return '<div class="frow"><span>' + esc(k) + ' <i>' + st.files[k].length + ' Б</i></span><button data-c="rmf" data-n="' + esc(k) + '">Удалить</button></div>'; }).join('') || '<p class="cs2">Нет файлов</p>'); },
        mail: function () { return head('Почта — postfix (SMTP) + dovecot (POP3)') + '<label>Домен</label><input class="q" data-f="dom" value="' + esc(st.srv.domain || '') + '" placeholder="college.ru (пусто — любой)">' + save('Сохранить домен') +
          '<h2>Ящики</h2><p class="cs2">Ящик — учётная запись сервера (добавляются на вкладке FTP или useradd).</p>' + S.users(st).map(function (u) { return '<div class="frow"><span>' + esc(u.name) + (st.srv.domain ? '@' + esc(st.srv.domain) : '') + '</span><i>' + ((st.mail[u.name] || []).length) + ' писем</i></div>'; }).join(''); },
        tftp: function () { var L = files(st, '/tftp/'); return head('TFTP — tftpd-hpa') + '<p class="cs2">Каталог /tftp (copy … tftp://адрес:/файл на ESR и MES).</p>' +
          (L.map(function (k) { return '<div class="frow"><span>' + esc(k) + ' <i>' + st.files[k].length + ' Б</i></span><button data-c="view" data-n="' + esc(k) + '">Открыть</button><button data-c="rmf" data-n="' + esc(k) + '">Удалить</button></div>'; }).join('') || '<p class="cs2">Файлов нет</p>') + '<pre class="sview"></pre>'; },
        ntp: function () { return head('NTP — chronyd') + '<p>Время сервера: <b>' + esc(EL.clock.linux(EL.clock.now() + st.clk, st.tz)) + '</b></p><p class="cs2">Сервер отвечает на UDP 123, если chronyd запущен. Время меняется в консоли: date, timedatectl.</p>'; },
        syslog: function () { var L = files(st, '/var/log/rsyslog/'); return head('Syslog — rsyslog') + '<p class="cs2">Сообщения устройств (UDP 514) — /var/log/rsyslog/ИМЯ/*.log</p>' +
          (L.map(function (k) { return '<div class="frow"><span>' + esc(k) + ' <i>' + st.files[k].split('\n').filter(Boolean).length + ' строк</i></span><button data-c="view" data-n="' + esc(k) + '">Открыть</button><button data-c="rmf" data-n="' + esc(k) + '">Очистить</button></div>'; }).join('') || '<p class="cs2">Журнал пуст</p>') + '<pre class="sview"></pre>'; },
        radius: function () { var r = S.radRead(st); return head('RADIUS — freeradius') + '<h2>Клиенты (NAS)</h2>' + tbl('cl', [['name', 'Имя', '90px'], ['ip', 'IP-адрес', '120px'], ['secret', 'Ключ (secret)', '120px']], r.clients) +
          '<h2>Пользователи</h2>' + tbl('ru', [['name', 'Имя', '130px'], ['pw', 'Пароль', '130px']], r.users) + save(); },
        tacacs: function () { var t = S.tacRead(st); return head('TACACS+ — tac_plus') + '<label>Ключ (key)</label><input class="q" data-f="key" value="' + esc(t.key) + '">' +
          '<h2>Пользователи</h2>' + tbl('tu', [['name', 'Имя', '130px'], ['pw', 'Пароль', '130px']], t.users) + save(); }
      };
      return P[cur]();
    }
    function say(ok, t) { var o = body.querySelector('.cs'); if (o) { o.textContent = t; o.style.color = ok ? 'var(--ok)' : 'var(--bad)'; } }
    function done(t) { S.restart(st, cur); render(); say(true, t || 'Сохранено'); U.draw(); }
    function v(f) { var x = body.querySelector('[data-f="' + f + '"]'); return x ? x.value.trim() : ''; }
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('change', function (e) { var t = e.target;
      if (t.dataset.c === 'tog') { S.set(st, cur, t.checked); render(); U.draw(); }
      if (t.dataset.c === 'https') { S.https(st, t.checked); render(); }
      if (t.dataset.f === 'zone') { pick.zone = t.value; render(); }
      if (t.dataset.f === 'web') { pick.web = t.value; render(); } });
    body.addEventListener('click', function (e) {
      var sb = e.target.closest('[data-s]'); if (sb) { cur = sb.dataset.s; render(); return; }
      var b = e.target.closest('button[data-c]'); if (!b) return; var c = b.dataset.c;
      if (c === 'addrow') { var tb = body.querySelector('table[data-t="' + b.dataset.t2 + '"] tbody'), tr = tb.rows[0] ? tb.rows[0].cloneNode(true) : null;
        if (!tr) { render(); return; } [].forEach.call(tr.querySelectorAll('input'), function (x) { x.value = ''; }); tb.appendChild(tr); return; }
      if (c === 'delrow') { var r = b.closest('tr'); if (r.parentNode.rows.length > 1) r.remove(); else [].forEach.call(r.querySelectorAll('input'), function (x) { x.value = ''; }); return; }
      if (c === 'view') { body.querySelector('.sview').textContent = st.files[b.dataset.n] || ''; return; }
      if (c === 'rmf') { if (/^\/var\/log\//.test(b.dataset.n)) st.files[b.dataset.n] = ''; else delete st.files[b.dataset.n]; render(); return; }
      if (c === 'addzone') { var nz = v('nz').toLowerCase().replace(/\.$/, ''); if (!/^[a-z0-9-]+(\.[a-z0-9-]+)+$/.test(nz)) { say(false, 'Имя зоны: college.ru'); return; }
        var Z = S.dnsRead(st); if (!Z.some(function (z) { return z.zone === nz; })) Z.push({ zone: nz, recs: [{ name: 'ns', type: 'A', val: st.ip || '127.0.0.1' }] });
        S.dnsWrite(st, Z); pick.zone = nz; done('Зона ' + nz + ' добавлена'); return; }
      if (c === 'newfile') { var nf = v('nf').replace(/^.*\//, ''); if (!/^[\w.-]+$/.test(nf)) { say(false, 'Имя файла: lab.html'); return; }
        var k = '/var/www/html/' + nf; if (st.files[k] === undefined) st.files[k] = '<h1>' + nf + '</h1>\n'; pick.web = k; render(); return; }
      if (c === 'delfile') { var w = v('web'); delete st.files[w]; pick.web = null; render(); return; }
      if (c !== 'save') return;
      if (cur === 'dhcp') { var L = rowsOf(body, 'pool'), bad = L.map(S.dhcpCheck).filter(Boolean)[0]; if (bad) { say(false, 'Ошибка: ' + bad); return; } S.dhcpWrite(st, L); done(); }
      if (cur === 'dns') { var z = v('zone'), R = rowsOf(body, 'rec').map(function (r) { return { name: r.name || '@', type: (r.type || 'A').toUpperCase(), val: r.val, pref: +r.pref || 10 }; });
        var bd = R.filter(function (r) { return ['A', 'CNAME', 'MX'].indexOf(r.type) < 0 || !r.val || (r.type === 'A' && EL.ip.ip2n(r.val) === null); })[0];
        if (bd) { say(false, 'Ошибка в записи ' + bd.name + ': тип A/CNAME/MX и значение (для A — IPv4)'); return; }
        S.dnsWrite(st, S.dnsRead(st).map(function (x) { return x.zone === z ? { zone: x.zone, file: x.file, recs: R } : x; })); pick.zone = z; done(); }
      if (cur === 'http') { st.files[v('web')] = body.querySelector('[data-f="page"]').value; pick.web = v('web'); done('Страница сохранена'); }
      if (cur === 'ftp') { var Us = rowsOf(body, 'usr').filter(function (u) { return /^[a-z_][a-z0-9_-]*$/i.test(u.name); }), A = {};
        Us.forEach(function (u) { A[u.name] = u.pw; }); if (A.root === undefined) A.root = st.accounts.root; st.accounts = A; done('Учётные записи сохранены'); }
      if (cur === 'mail') { var dm = v('dom').toLowerCase(); if (dm && !/^[a-z0-9-]+(\.[a-z0-9-]+)+$/.test(dm)) { say(false, 'Домен: college.ru'); return; } st.srv.domain = dm || null; done(); }
      if (cur === 'radius') { S.radWrite(st, { clients: rowsOf(body, 'cl'), users: rowsOf(body, 'ru') }); done(); }
      if (cur === 'tacacs') { if (!v('key')) { say(false, 'Нужен ключ'); return; } S.tacWrite(st, { key: v('key'), users: rowsOf(body, 'tu') }); done(); }
    });
    render();
    U.makeWin('srv' + id, 'Службы', d.name, body, { w: 760, h: Math.min(600, innerHeight - 120) });
  }
  EL.openSrv = openSrv;
})();
