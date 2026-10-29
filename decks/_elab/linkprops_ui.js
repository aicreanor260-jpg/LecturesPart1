/* Окно «Свойства канала» (ПКМ по кабелю) и «Карта площадок» (ПКМ по полю): площадки — зоны с городом или координатами,
   каналы между ними — с расстоянием, км, и задержкой распространения. */
(function () {
  'use strict';
  var EL = window.EL, U = window.ELUI, X = EL.uiX, esc = U.esc;
  function net() { return U.net(); }
  function fmtT(s) { return (s < 1e-3 ? (s * 1e6).toFixed(1) + ' мкс' : (s * 1e3).toFixed(s < 0.1 ? 3 : 1) + ' мс').replace('.', ','); }
  function km(m) { return m >= 1000 ? (m / 1000).toLocaleString('ru-RU', { maximumFractionDigits: 1 }) + ' км' : m + ' м'; }
  var items0 = X.items, run0 = X.run;
  X.items = function (k, d) { return items0(k, d) + (k === 'link' ? '<button data-a="lprops"><span>⇿</span>Свойства канала…</button>' : '') +
    (k === 'field' ? '<button data-a="map"><span>🗺</span>Карта площадок</button>' : ''); };
  X.run = function (k, a, arg) { run0(k, a, arg); if (k === 'link' && a === 'lprops') openLink(arg); if (k === 'field' && a === 'map') openMap(); };
  // площадка (зона) кабеля: зона, в которой лежит устройство конца
  function zoneOf(d) { return ((net().zones || []).filter(function (z) { return EL.zoneInside(z, d.x, d.y) || (z.members || []).indexOf(d.name) >= 0; })[0]) || null; }
  function coords(z) { return z && z.geo ? z.geo : null; }
  function geoLen(l) { var n = net(), a = coords(zoneOf(n.devs[l.a.dev])), b = coords(zoneOf(n.devs[l.b.dev])); return a && b ? Math.round(EL.geoKm(a, b) * EL.ROUTE_K) : null; }
  EL.linkGeoKm = geoLen;

  // ---------------------------------------------------------------- свойства канала
  function openLink(i) {
    var n = net(), l = n.links[i]; if (!l) return; var body = document.createElement('div'); body.className = 'pad lprop';
    function render() {
      var cab = n.cabOf(l), wan = cab === 'wan', ph = n.phys(l.a.dev, l.a.port), g = geoLen(l), len = n.lenOf(l);
      body.innerHTML = '<div class="k">' + esc(n.devs[l.a.dev].name + ' ' + l.a.port + ' ↔ ' + n.devs[l.b.dev].name + ' ' + l.b.port) + '</div><p>' + esc(n.cableText ? n.cableText(l) : EL.CABLES[cab]) + '</p>' +
        (wan ? '<label>Расстояние, км</label><div class="row"><input class="q" data-f="km" type="number" min="0.001" step="any" value="' + (len / 1000) + '">' +
          (g ? '<button data-c="geo">По площадкам: ' + g + ' км</button>' : '') + '</div>' : '<label>Длина кабеля, м</label><input class="q" data-f="len" type="number" min="0.5" step="any" value="' + len + '">') +
        (EL.linkParams ? EL.linkParams(l, ph) : '') +
        '<div class="row"><button class="pri" data-c="ok">Сохранить</button><span class="cs"></span></div>' +
        '<p class="cs2">Распространение в одну сторону: <b>' + fmtT(n.propDelay(l)) + '</b> (' + (EL.propSpeed(cab) > 2e8 ? 'оптика ≈ 4,9 мкс/км' : 'медь ≈ 5,05 мкс/км') + ')' +
        (ph.up ? ' · линк ' + (ph.speed >= 1000 ? ph.speed / 1000 + ' Гбит/с' : ph.speed + ' Мбит/с') : ' · нет линка: ' + esc(ph.why || '')) + '</p>' +
        (EL.lenNorm ? '<p class="cs2">' + esc(EL.lenNorm(n, l)) + '</p>' : '');
    }
    body.addEventListener('keydown', function (e) { e.stopPropagation(); });
    body.addEventListener('click', function (e) { var b = e.target.closest('[data-c]'); if (!b) return;
      if (b.dataset.c === 'geo') { body.querySelector('[data-f="km"]').value = geoLen(l); return; }
      if (b.dataset.c !== 'ok') return;
      var o = {}, f = function (k) { var x = body.querySelector('[data-f="' + k + '"]'); return x ? x.value.trim() : null; };
      if (f('km') !== null) o.len = Math.round(parseFloat(String(f('km')).replace(',', '.')) * 1000);
      if (f('len') !== null) o.len = parseFloat(String(f('len')).replace(',', '.'));
      if (!(o.len > 0) || o.len > 4e7) { body.querySelector('.cs').textContent = 'Длина — положительное число'; return; }
      if (EL.linkParamsRead) { var bad = EL.linkParamsRead(body, o); if (bad) { body.querySelector('.cs').textContent = bad; return; } }
      n.setLink(n.links.indexOf(l), o); render(); body.querySelector('.cs').textContent = 'Сохранено'; U.draw(); });
    render();
    U.makeWin('lprop', 'Свойства канала', n.devs[l.a.dev].name + ' ↔ ' + n.devs[l.b.dev].name, body, { w: 420, h: Math.min(560, innerHeight - 140) });
  }

  // ---------------------------------------------------------------- город / координаты площадки (окно зоны)
  EL.zoneFields = function (z) { var g = z.geo || ['', ''], city = z.city || '';
    return '<label>Площадка: город</label><select class="q" data-f="city"><option value="">— не задан —</option>' + Object.keys(EL.CITIES).map(function (c) {
      return '<option' + (c === city ? ' selected' : '') + '>' + esc(c) + '</option>'; }).join('') + '<option value="*"' + (city === '*' ? ' selected' : '') + '>Свои координаты</option></select>' +
      '<div class="row"><input class="q" data-f="lat" placeholder="широта" value="' + (city === '*' ? g[0] : '') + '"><input class="q" data-f="lon" placeholder="долгота" value="' + (city === '*' ? g[1] : '') + '"></div>'; };
  EL.zoneSave = function (z, body) { var c = body.querySelector('[data-f="city"]').value, la = parseFloat(body.querySelector('[data-f="lat"]').value), lo = parseFloat(body.querySelector('[data-f="lon"]').value);
    if (!c) { delete z.city; delete z.geo; return; }
    if (c === '*') { if (isFinite(la) && isFinite(lo) && Math.abs(la) <= 90 && Math.abs(lo) <= 180) { z.city = '*'; z.geo = [la, lo]; } return; }
    z.city = c; z.geo = EL.CITIES[c].slice(); };

  // ---------------------------------------------------------------- карта площадок: города по координатам, каналы с расстоянием и задержкой
  function openMap() {
    var n = net(), Z = (n.zones || []).filter(function (z) { return z.geo; }), body = document.createElement('div'); body.className = 'pad mapw';
    var ch = []; n.links.forEach(function (l, i) { var za = zoneOf(n.devs[l.a.dev]), zb = zoneOf(n.devs[l.b.dev]); if (za && zb && za !== zb) ch.push({ i: i, l: l, a: za, b: zb }); });
    if (!Z.length) { body.innerHTML = '<p>Площадок нет. Создайте зоны (ПКМ по полю → «Зона») и задайте им город или координаты в окне зоны; устройства разных площадок соедините кабелем «Канал связи» и задайте расстояние (или «По площадкам»).</p>'; }
    else {
      var la = Z.map(function (z) { return z.geo[0]; }), lo = Z.map(function (z) { return z.geo[1]; }), W = 560, H = 260, pad = 90;
      var x0 = Math.min.apply(null, lo) - 2, x1 = Math.max.apply(null, lo) + 2, y0 = Math.min.apply(null, la) - 2, y1 = Math.max.apply(null, la) + 2;
      var px = function (g) { return pad + (g[1] - x0) / (x1 - x0 || 1) * (W - 2 * pad); }, py = function (g) { return H - pad - (g[0] - y0) / (y1 - y0 || 1) * (H - 2 * pad); };
      var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="msvg">' + ch.filter(function (c) { return c.a.geo && c.b.geo; }).map(function (c) {
        var A = c.a.geo, B = c.b.geo, mx = (px(A) + px(B)) / 2, my = (py(A) + py(B)) / 2;
        return '<line x1="' + px(A) + '" y1="' + py(A) + '" x2="' + px(B) + '" y2="' + py(B) + '"/><text x="' + mx + '" y="' + (my - 6) + '" class="mk">' + km(n.lenOf(c.l)) + ' · ' + fmtT(n.propDelay(c.l)) + '</text>'; }).join('') +
        Z.map(function (z) { return '<circle cx="' + px(z.geo) + '" cy="' + py(z.geo) + '" r="7" style="fill:' + z.c + '"/><text x="' + px(z.geo) + '" y="' + (py(z.geo) + 22) + '" class="mt">' + esc(z.t) + (z.city && z.city !== '*' && z.city !== z.t ? ' · ' + esc(z.city) : '') + '</text>'; }).join('') + '</svg>';
      body.innerHTML = svg + '<table class="mtab"><thead><tr><th>Канал</th><th>Кабель</th><th>Длина</th><th>Задержка ↦</th><th>По площадкам</th></tr></thead><tbody>' +
        (ch.map(function (c) { var g = geoLen(c.l); return '<tr data-i="' + c.i + '"><td>' + esc(c.a.t + ' ↔ ' + c.b.t) + '</td><td>' + esc(n.cabOf(c.l) === 'wan' ? 'канал связи' : n.cabOf(c.l)) + '</td><td>' + km(n.lenOf(c.l)) +
          '</td><td>' + fmtT(n.propDelay(c.l)) + '</td><td>' + (g ? g + ' км' : '—') + '</td></tr>'; }).join('') || '<tr><td colspan="5">Кабелей между площадками нет</td></tr>') + '</tbody></table>' +
        '<p class="cs2">Задержка — распространение в одну сторону; RTT ping — вдвое больше плюс передача. «По площадкам» — по дуге × ' + String(EL.ROUTE_K).replace('.', ',') + ' (трасса кабеля длиннее прямой). Щелчок по строке — свойства канала.</p>';
    }
    body.addEventListener('click', function (e) { var tr = e.target.closest('tr[data-i]'); if (tr) openLink(+tr.dataset.i); });
    U.makeWin('map', 'Карта площадок', 'расстояния и задержки', body, { w: 640, h: Math.min(600, innerHeight - 120) });
  }
  // подпись длины на длинных кабелях
  var od = X.onDraw; X.onDraw = function () { od(); var n = net(), g = document.getElementById('gp'); if (!g) return;
    n.links.forEach(function (l, i) { if (n.lenOf(l) < 1000 && n.cabOf(l) !== 'wan') return; var a = n.devs[l.a.dev], b = n.devs[l.b.dev], o = U.linkOff(i);
      var t = U.el('text', { 'class': 'lkm', x: (a.x + b.x) / 2 + o.x, y: (a.y + b.y) / 2 + o.y - 8 }, g); t.textContent = km(n.lenOf(l)); }); };
  EL.openMap = openMap; EL.openLinkProps = openLink;
})();
