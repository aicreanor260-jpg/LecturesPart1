/* Веб-интерфейс абонентского роутера RG-35-WZ: вход (admin / password), «TCP/IP» → «Настройка LAN» и «Настройка WAN» (руководство 2.3.0).
   Открывается из меню устройства («Веб-интерфейс») или с компьютера Debian в LAN: open http://<адрес LAN роутера>. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc, H = EL.hosts;
  function net() { return U.net(); }
  var items0 = X.items, run0 = X.run;
  X.items = function (k, d) { return items0(k, d) + (k === 'dev' && d && EL.isCpe(d) ? '<button data-a="cpeweb"><span>🌐</span>Веб-интерфейс</button>' : ''); };
  X.run = function (k, a, arg) { run0(k, a, arg); if (k === 'dev' && a === 'cpeweb') openWeb(arg.id, null); };
  EL.listensX = (function (lx0) { return function (d, proto, port) { if (EL.isCpe(d) && proto === 'tcp' && port === 80) return true; return lx0 ? lx0(d, proto, port) : undefined; }; })(EL.listensX);
  var deb0 = H.debExec;
  H.debExec = function (st, raw) { var m = String(raw).trim().match(/^(?:open|curl|firefox|xdg-open)\s+(?:https?:\/\/)?(\d+\.\d+\.\d+\.\d+)\/?$/);
    if (m && st.user && !st.ssh && st.net) { var r = EL.cpeAt(st.net, m[1]); if (r && st.net.request(st.dev, m[1], 'tcp', 80).ok) { openWeb(r.id, m[1]); return '[Браузер] http://' + m[1] + '/ — веб-интерфейс ' + r.model + ' (открыт в окне)'; } }
    return deb0.apply(this, arguments); };
  function openWeb(id, via) {
    var n = net(), d = n.devs[id]; if (!d) return; var c = d.st.cpe, key = 'cpe' + id, auth = false;
    var body = document.createElement('div'); body.className = 'pad cpe';
    function render() {
      var w = c.web, L = w.lan, W = w.wan;
      if (!auth) { body.innerHTML = '<div class="k">' + esc(d.model) + (via ? ' · http://' + esc(via) : '') + '</div><h2>Вход</h2><label>Имя пользователя</label><input class="q" data-f="u" value="">' +
        '<label>Пароль</label><input class="q" data-f="p" type="text" style="-webkit-text-security:disc">' +
        '<div class="row"><button class="pri" data-c="login">Войти</button><span class="cs"></span></div>'; return; }
      var lease = c.lease ? c.lease.ip + '/' + c.lease.len + ', шлюз ' + (c.lease.gw || '—') + ' (DHCP-сервер ' + c.lease.server + ')' : 'нет';
      body.innerHTML = '<div class="k">' + esc(d.model) + ' · TCP/IP</div><h2>Настройка LAN</h2>' +
        '<label>IP-адрес</label><input class="q" data-f="lip" value="' + esc(L.ip) + '"><label>Маска подсети</label><input class="q" data-f="lmask" value="' + esc(L.mask) + '">' +
        '<label style="display:block;margin:8px 0"><input type="checkbox" data-f="ldhcp"' + (L.dhcp ? ' checked' : '') + '> DHCP-сервер</label>' +
        '<label>Начальный адрес пула IP-адресов</label><input class="q" data-f="lfrom" value="' + esc(L.from) + '"><label>Конечный адрес пула IP-адресов</label><input class="q" data-f="lto" value="' + esc(L.to) + '">' +
        '<label>Время аренды DHCP, мин</label><input class="q" data-f="llease" value="' + esc(L.lease) + '">' +
        '<h2>Настройка WAN</h2><label>Тип соединения: IPoE</label><select class="q" data-f="wmode"><option value="dhcp"' + (W.mode === 'dhcp' ? ' selected' : '') + '>DHCP Client</option>' +
        '<option value="static"' + (W.mode === 'static' ? ' selected' : '') + '>Static IP</option></select>' +
        '<div data-s="1"' + (W.mode === 'static' ? '' : ' hidden') + '><label>IP-адрес</label><input class="q" data-f="wip" value="' + esc(W.ip) + '"><label>Маска подсети</label><input class="q" data-f="wmask" value="' + esc(W.mask) + '">' +
        '<label>Основной шлюз</label><input class="q" data-f="wgw" value="' + esc(W.gw) + '"></div>' +
        '<p class="cs2">WAN сейчас: ' + esc(W.mode === 'static' ? (W.ip ? W.ip + ', шлюз ' + (W.gw || '—') : 'адрес не задан') : lease) + '</p>' +
        '<div class="row"><button class="pri" data-c="apply">Применить</button>' + (W.mode === 'dhcp' ? '<button data-c="renew">Обновить (DHCP)</button>' : '') + '<span class="cs"></span></div>';
      body.querySelector('[data-f="wmode"]').addEventListener('change', function () { body.querySelector('[data-s]').hidden = this.value !== 'static'; });
    }
    function val(f) { var x = body.querySelector('[data-f="' + f + '"]'); return x ? (x.type === 'checkbox' ? x.checked : x.value.trim()) : null; }
    function ipOk(a) { return EL.ip.ip2n(a) !== null; }
    body.addEventListener('keydown', function (e) { e.stopPropagation(); if (e.key === 'Enter' && !auth) body.querySelector('[data-c="login"]').click(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-c]'); if (!b) return; var out = body.querySelector('.cs');
      if (b.dataset.c === 'login') { if (val('u') === c.web.user && val('p') === c.web.pw) { auth = true; render(); } else out.textContent = 'Неверное имя пользователя или пароль'; return; }
      if (b.dataset.c === 'renew') { var r = n.cpeDhcp(id); if (n.onTrace) n.onTrace({ ok: r.ok, steps: r.steps }, id, 'DHCP WAN'); render(); body.querySelector('.cs').textContent = r.ok ? 'Адрес WAN получен' : 'DHCP-сервер не ответил'; U.draw(); return; }
      if (b.dataset.c === 'apply') {
        var w = { lan: { ip: val('lip'), mask: val('lmask'), dhcp: val('ldhcp'), from: val('lfrom'), to: val('lto'), lease: +val('llease') || 1440 },
                  wan: { mode: val('wmode'), ip: val('wip') || '', mask: val('wmask') || '255.255.255.0', gw: val('wgw') || '' }, user: c.web.user, pw: c.web.pw };
        var bad = [['lip', w.lan.ip], ['lfrom', w.lan.from], ['lto', w.lan.to]].filter(function (x) { return !ipOk(x[1]); }).concat(EL.ip.mask2len(w.lan.mask) === null ? [['lmask']] : [])
          .concat(w.wan.mode === 'static' ? [['wip', w.wan.ip], ['wgw', w.wan.gw]].filter(function (x) { return x[1] && !ipOk(x[1]); }) : []);
        if (bad.length) { out.textContent = 'Проверьте поля: неверный формат адреса или маски'; return; }
        var L = w.lan, len = EL.ip.mask2len(L.mask);
        if (!EL.ip.sameNet(L.from, L.ip, len) || !EL.ip.sameNet(L.to, L.ip, len)) { out.textContent = 'Адреса пула должны попадать в сеть LAN'; return; }
        var errs = n.cpeApply(id, w); if (w.wan.mode === 'dhcp') n.cpeDhcp(id);
        var newIp = L.ip !== (via || L.ip) && via; render(); body.querySelector('.cs').textContent = errs.length ? 'Ошибка: ' + errs[0] : 'Настройки применены' + (newIp ? ' — адрес LAN изменился, откройте http://' + L.ip : '');
        U.draw(); U.refresh(); } });
    render();
    U.makeWin(key, 'Веб-интерфейс', d.name, body, { w: 440, h: Math.min(640, innerHeight - 140) });
  }
  EL.cpeWeb = openWeb;
})();
