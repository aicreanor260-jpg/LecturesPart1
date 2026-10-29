/* Окно «Облако провайдера»: адреса портов, статические маршруты, задержка, скорость, потери (ядро — isp.js). */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  function net() { return U.net(); }
  var items0 = X.items, run0 = X.run;
  X.items = function (k, d) { return items0(k, d) + (k === 'dev' && d && EL.isIsp(d) ? '<button data-a="isp"><span>☁</span>Облако провайдера</button>' : ''); };
  X.run = function (k, a, arg) { run0(k, a, arg); if (k === 'dev' && a === 'isp') openIsp(arg.id); };
  function openIsp(id) {
    var n = net(), d = n.devs[id]; if (!d) return; var c = d.st.isp, body = document.createElement('div'); body.className = 'pad ispw';
    function render() {
      c = d.st.isp; var ports = n.portsOf(d).filter(function (p) { return /^gi/.test(p); });
      body.innerHTML = '<div class="k">' + esc(d.name) + ' · сеть оператора</div>' +
        '<table class="stab"><thead><tr><th>Порт</th><th>К кому</th><th>IP-адрес / маска (шлюз для клиента)</th></tr></thead><tbody>' + ports.map(function (p) {
          var x = c.ports[p] || {}, pr = n.peer(id, p); return '<tr><td>' + p + '</td><td>' + esc(pr ? n.devs[pr.dev].name + ' ' + pr.port : '—') + '</td><td><input class="q" data-p="' + p + '" value="' + (x.ip ? x.ip + '/' + x.len : '') + '" placeholder="A.B.C.D/N"></td></tr>'; }).join('') +
        '</tbody></table><h2>Маршруты</h2><textarea class="q" data-f="routes" rows="3" placeholder="10.1.0.0/16 203.0.113.2">' + esc(c.routes.map(function (r) { return r.net + ' ' + r.nh; }).join('\n')) + '</textarea>' +
        '<p class="cs2">Сеть клиента за его маршрутизатором: «сеть/маска следующий-адрес» — по строке. Сети портов облака доступны сами.</p>' +
        '<div class="row"><label style="margin:0">Задержка через облако, мс</label><input class="q" data-f="delay" type="number" min="0" max="2000" step="0.1" value="' + c.delay + '">' +
        '<label style="margin:0">Скорость, Мбит/с</label><input class="q" data-f="mbps" type="number" min="0.1" step="any" value="' + c.mbps + '">' +
        '<label style="margin:0">Потери, %</label><input class="q" data-f="loss" type="number" min="0" max="100" step="0.1" value="' + c.loss + '"></div>' +
        '<div class="row"><button class="pri" data-c="ok">Применить</button><span class="cs"></span></div>' +
        '<p class="cs2">Своё облако оператора — на маршрутизаторах ME с MPLS и L3VPN (ПКМ по полю → «Маршрутизаторы ME»).</p>';
    }
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-c]'); if (!b) return;
      var o = { ports: {}, routes: [], delay: +body.querySelector('[data-f="delay"]').value, mbps: +body.querySelector('[data-f="mbps"]').value, loss: +body.querySelector('[data-f="loss"]').value }, bad = null;
      [].forEach.call(body.querySelectorAll('[data-p]'), function (x) { var v = x.value.trim(); if (!v) return; var q = EL.ip.parseCidr(v); if (!q) { bad = x.dataset.p + ': адрес/маска, например 203.0.113.1/30'; return; } o.ports[x.dataset.p] = { ip: q.ip, len: q.len }; });
      body.querySelector('[data-f="routes"]').value.split('\n').forEach(function (l) { var t = l.trim().split(/\s+/); if (!t[0]) return; o.routes.push({ net: t[0], nh: t[1] || '' }); });
      bad = bad || n.ispCheck(o); var out = body.querySelector('.cs');
      if (bad) { out.textContent = 'Ошибка: ' + bad; out.style.color = 'var(--bad)'; return; }
      var errs = n.ispApply(id, o); render(); out = body.querySelector('.cs');
      out.textContent = errs.length ? 'Ошибка: ' + errs[0] : 'Применено'; out.style.color = errs.length ? 'var(--bad)' : 'var(--ok)'; U.draw(); U.refresh(); });
    render();
    U.makeWin('isp' + id, 'Облако провайдера', d.name, body, { w: 520, h: Math.min(620, innerHeight - 120) });
  }
  EL.openIsp = openIsp;
})();
