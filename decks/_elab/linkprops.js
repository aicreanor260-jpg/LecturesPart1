/* Свойства кабеля и канала: длина, расстояние между площадками, скорость, потери, джиттер, битовые ошибки, нормы длины.
   Длина l.len, м (по умолчанию 100 м). «Канал связи» (wan) — канал между площадками (оптика оператора): расстояние, км, без нормы длины;
   задержка распространения = длина / скорость сигнала: оптика (n ≈ 1,47) ≈ 4,9 мкс/км, медь (NVP ≈ 0,66) ≈ 5,05 мкс/км.
   ping показывает RTT: обычное время LAN + распространение и передача по каналам туда и обратно (Москва — Новосибирск ≈ 3300 км ≈ +16 мс в одну сторону).
   Расстояние по координатам площадок: по дуге большого круга × 1,2 (коэффициент трассы кабеля — допущение эмулятора). */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype;
  EL.CABLES.wan = 'Канал связи между площадками (оптика оператора)';
  var FIBER = /^(sfp|pon|wan)/, PROP_F = 2.04e8, PROP_C = 1.98e8;
  function propOf(cab) { return FIBER.test(cab || '') ? PROP_F : PROP_C; }
  P.cabOf = function (l) { return l.cab || this.defaultCable(l.a.dev, l.a.port, l.b.dev, l.b.port); };
  P.lenOf = function (l) { return l.len || 100; };
  P.propDelay = function (l) { return this.lenOf(l) / propOf(this.cabOf(l)); };          // с, в одну сторону
  EL.propSpeed = propOf;
  // «Канал связи» — линк на скорости портов, как медь без MDI (пары и модули — забота оператора)
  var phys0 = P.phys;
  P.phys = function (id, port) {
    var pr = this.peer(id, port); if (!pr) return phys0.apply(this, arguments);
    var l = this.links[pr.li]; if (l.cab !== 'wan') return phys0.apply(this, arguments);
    l.cab = 'cu'; var r; try { r = phys0.apply(this, arguments); } finally { l.cab = 'wan'; }
    if (!r.up && /оптическ|модул|медн/.test(r.why || '')) r = { up: true, speed: 1000, dup: {}, cab: 'wan' }; else r = EL.clone(r);
    r.cab = 'wan'; if (r.up) { r.dup = r.dup || {}; r.dup[id] = r.dup[pr.dev] = 'full'; r.mismatch = false; } return r;
  };
  // задержка пути пакета (шаги трассы ip): передача + распространение по каждому сегменту + обработка в узлах
  P.pathDelay = function (r, bytes) { var s = this, t = 0, b = (bytes || 84) + 18;
    (r && r.steps || []).forEach(function (x) { if (x.k !== 'ip') return; (x.segs || []).forEach(function (g) { var l = s.links[g.li]; if (!l) return;
      var ph = s.phys(l.a.dev, l.a.port), mb = l.mbps || ph.speed || 1000; t += b * 8 / (mb * 1e6) + s.propDelay(l) + 10e-6; }); });
    return t; };
  // добавка к выводу ping, мс: только заметная, от 0,2 мс (каналы, длинные кабели, медленные линии) — короткий LAN остаётся как был
  P.rttExtra = function (r, bytes) { var ms = this.pathDelay(r, bytes) * 1000; return ms >= 0.2 ? ms : 0; };
  // потери эхо на каналах (потери %, битовые ошибки, длина сверх нормы) — повторяемо по номеру эхо
  P.lossHit = function (r, k) { var s = this, p = 1;
    (r && r.steps || []).forEach(function (x) { if (x.k !== 'ip') return; (x.segs || []).forEach(function (g) { var l = s.links[g.li]; if (!l) return; p *= 1 - s.linkLoss(l, 84 + 18); }); });
    var q = 1 - p; if (q <= 0) return false; var h = Math.sin((k + 1) * 12.9898 + (r.steps.length || 1) * 78.233) * 43758.5453; return h - Math.floor(h) < q; };
  // вероятность потери кадра на линке: потери %, BER, длина сверх нормы (linklen.js)
  P.linkLoss = function (l, bytes) { var p = (l.loss || 0) / 100; if (l.ber) p = 1 - (1 - p) * Math.pow(1 - l.ber, (bytes || 100) * 8);
    if (this.lenErr) { var e = this.lenErr(l); if (e) p = 1 - (1 - p) * (1 - e); } return Math.min(1, p); };

  // ---------------------------------------------------------------- сохранение: свойства — пятым элементом кабеля в файле схемы
  var KEYS = ['len', 'mbps', 'loss', 'jit', 'ber'];
  var json0 = P.toJSON;
  P.toJSON = function () { var j = json0.call(this), s = this; j.links.forEach(function (x, i) { var l = s.links[i], o = {};
    KEYS.forEach(function (k) { if (l[k]) o[k] = l[k]; }); if (Object.keys(o).length) { while (x.length < 5) x.push(null); x[5] = o; } }); return j; };
  var from0 = EL.Net.fromJSON;
  EL.Net.fromJSON = function (j) { var n = from0(j); (j.links || []).forEach(function (l) { if (!l[5] || typeof l[5] !== 'object') return;
    var a = n.byName(l[0]), b = n.byName(l[2]); n.links.forEach(function (x) { if (x.a.dev === (a && a.id) && x.a.port === l[1] && x.b.dev === (b && b.id) && x.b.port === l[3])
      KEYS.forEach(function (k) { if (isFinite(l[5][k]) && l[5][k] > 0) x[k] = +l[5][k]; }); }); }); return n; };
  P.setLink = function (li, o) { var l = this.links[li]; if (!l) return; KEYS.forEach(function (k) { if (o[k] === undefined) return; if (o[k] > 0) l[k] = +o[k]; else delete l[k]; }); this.gen++; };

  // ---------------------------------------------------------------- координаты площадок (зоны): расстояние по дуге × коэффициент трассы
  EL.CITIES = { 'Москва': [55.7558, 37.6173], 'Санкт-Петербург': [59.9343, 30.3351], 'Новосибирск': [55.0084, 82.9357], 'Екатеринбург': [56.8389, 60.6057],
    'Казань': [55.7963, 49.1088], 'Нижний Новгород': [56.2965, 43.9361], 'Самара': [53.1959, 50.1002], 'Омск': [54.9885, 73.3242], 'Красноярск': [56.0153, 92.8932],
    'Иркутск': [52.2870, 104.3050], 'Хабаровск': [48.4802, 135.0719], 'Владивосток': [43.1155, 131.8855], 'Ростов-на-Дону': [47.2357, 39.7015], 'Краснодар': [45.0355, 38.9753] };
  EL.ROUTE_K = 1.2;
  EL.geoKm = function (a, b) { var R = 6371, r = Math.PI / 180, dLa = (b[0] - a[0]) * r, dLo = (b[1] - a[1]) * r;
    var h = Math.sin(dLa / 2) * Math.sin(dLa / 2) + Math.cos(a[0] * r) * Math.cos(b[0] * r) * Math.sin(dLo / 2) * Math.sin(dLo / 2); return 2 * R * Math.asin(Math.sqrt(h)); };
})(typeof window !== 'undefined' ? window : global);
