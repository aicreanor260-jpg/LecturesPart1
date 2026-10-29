/* Экспорт результатов симуляции в формате OMNeT++ (приложение «Result File Formats», версия 3 — OMNeT++ 6) и CSV для Excel.
   .vec: version 3, run, attr …; vector ID МОДУЛЬ ИМЯ TV + attr unit; строки «ID время значение» (время по возрастанию).
     Векторы: задержка пакетов потока (rtt или endToEndDelay, с), потери потока (packetDropped, 1 на каждый потерянный кадр),
     длина очереди порта (queueLength, кадров), загрузка порта (utilization, % по интервалам).
   .sca: scalar МОДУЛЬ ИМЯ ЗНАЧЕНИЕ (+ attr unit): по потокам отправлено / получено / потеряно, % потерь, RTT min/avg/max, джиттер;
     по кабелям кадры и загрузка; время сходимости протоколов (если было изменение линка); statistic … rtt:histogram — field count, mean,
     stddev, sum, sqrsum, min, max и bin НИЖНЯЯ_ГРАНИЦА КОЛИЧЕСТВО (первый бин — -INF, недобор).
   Модули: Net.<устройство> (поток i — Net.<источник>.flow<i>), порт — Net.<устройство>.<порт с _ вместо />.
   CSV — «тип;модуль;имя;время;значение», десятичная запятая (Excel с русскими настройками). */
(function (G) {
  'use strict';
  var EL = G.EL;
  function q(s) { s = String(s); return /^[A-Za-z0-9_.:\[\]*\-]+$/.test(s) ? s : '"' + s.replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"'; }
  function num(v) { if (!isFinite(v)) return v > 0 ? 'inf' : v < 0 ? '-inf' : 'nan'; return String(+(+v).toPrecision(12)); }
  function mod(net, id, extra) { var d = net.devs[id]; return 'Net.' + (d ? d.name : String(id)).replace(/\s+/g, '_') + (extra ? '.' + extra : ''); }
  function portMod(net, name) { var m = String(name).match(/^(\S+)\s+(.+)$/); return 'Net.' + (m ? m[1] + '.' + m[2].replace(/[\/\s]/g, '_') : String(name).replace(/[\/\s]/g, '_')); }
  function pad2(x) { return ('0' + x).slice(-2); }
  function stamp(d) { return d.getFullYear() + pad2(d.getMonth() + 1) + pad2(d.getDate()) + '-' + pad2(d.getHours()) + ':' + pad2(d.getMinutes()) + ':' + pad2(d.getSeconds()); }
  function header(o) { var dt = stamp(o.date || new Date()), run = 'NetCat-0-' + dt + '-' + (o.pid || 1);
    return ['version 3', 'run ' + run, 'attr configname General', 'attr datetime ' + dt, 'attr experiment NetCat', 'attr inifile ""', 'attr iterationvars ""', 'attr measurement ""',
      'attr network Net', 'attr processid ' + (o.pid || 1), 'attr repetition 0', 'attr replication #0', 'attr resultdir results', 'attr runnumber 0', 'attr seedset 0',
      'config network Net', 'config **.queueCapacity ' + (o.qcap || 64)]; }
  // векторы из ленты событий симуляции
  function vectors(net, r) {
    var V = [], E = r.events.slice().sort(function (a, b) { return a.t - b.t; });
    r.flows.forEach(function (f, i) { var m = mod(net, f.src, 'flow' + i), nm = f.kind === 'ping' ? 'rtt:vector' : 'endToEndDelay:vector';
      V.push({ mod: m, name: nm, unit: 's', pts: E.filter(function (e) { return e.kind === 'deliver' && e.flow === i && e.delay !== undefined && (e.dir === 'bk' || f.kind === 'udp'); }).map(function (e) { return [e.t, e.delay]; }) });
      V.push({ mod: m, name: 'packetDropped:vector', unit: 'pk', pts: E.filter(function (e) { return e.kind === 'drop' && e.flow === i; }).map(function (e) { return [e.t, 1]; }) }); });
    var P = {}; E.forEach(function (e) { if (e.kind === 'tx' && e.port) (P[e.port] = P[e.port] || []).push(e); });
    Object.keys(P).sort().forEach(function (p) { var L = P[p], m = portMod(net, p), bins = 40, bw = (r.tEnd || 1) / bins, busy = [];
      V.push({ mod: m, name: 'queueLength:vector', unit: 'pk', pts: [[0, 0]].concat(L.map(function (e) { return [e.t1, e.q || 0]; })) });
      for (var k = 0; k < bins; k++) busy.push(0);
      L.forEach(function (e) { var a = e.t1, b = e.t1 + (e.tx || 0); for (var k = Math.floor(a / bw); k < bins && k * bw < b; k++) busy[k] += Math.max(0, Math.min(b, (k + 1) * bw) - Math.max(a, k * bw)); });
      V.push({ mod: m, name: 'utilization:vector', unit: '%', pts: busy.map(function (v, k) { return [k * bw, Math.min(100, v / bw * 100)]; }) }); });
    V.forEach(function (v) { var t = -Infinity; v.pts = v.pts.filter(function (p) { if (p[0] < t) return false; t = p[0]; return true; }); });   // время — по возрастанию
    return V; }
  function hist(vals, bins) { if (!vals.length) return null; var mn = Math.min.apply(null, vals), mx = Math.max.apply(null, vals); if (mx === mn) { mx = mn + 1e-6; bins = 1; }
    var w = (mx - mn) / bins, c = []; for (var i = 0; i < bins; i++) c.push(0); vals.forEach(function (v) { c[Math.min(bins - 1, Math.floor((v - mn) / w))]++; });
    var n = vals.length, s = vals.reduce(function (a, b) { return a + b; }, 0), s2 = vals.reduce(function (a, b) { return a + b * b; }, 0), mean = s / n;
    return { count: n, mean: mean, stddev: n > 1 ? Math.sqrt(Math.max(0, (s2 - n * mean * mean) / (n - 1))) : 0, sum: s, sqrsum: s2, min: Math.min.apply(null, vals), max: Math.max.apply(null, vals),
      bins: [['-INF', 0]].concat(c.map(function (x, i) { return [mn + i * w, x]; })) }; }
  function scalars(net, r, o) { var S = [];
    r.flows.forEach(function (f, i) { var m = mod(net, f.src, 'flow' + i);
      S.push([m, 'sentPk:count', f.sent, 'pk'], [m, 'rcvdPk:count', f.recv, 'pk'], [m, 'lostPk:count', f.sent - f.recv, 'pk'], [m, 'lossRate', f.loss, '%']);
      if (f.min !== undefined) S.push([m, (f.kind === 'ping' ? 'rtt' : 'delay') + ':min', f.min, 's'], [m, (f.kind === 'ping' ? 'rtt' : 'delay') + ':mean', f.avg, 's'], [m, (f.kind === 'ping' ? 'rtt' : 'delay') + ':max', f.max, 's'], [m, 'jitter', f.jitter, 's']); });
    r.links.forEach(function (l) { var m = portMod(net, l.name.split(' ↔ ')[0]); S.push([m, 'txFrames:count', l.frames, 'pk'], [m, 'utilization:mean', l.util, '%'], [m, 'datarate', l.mbps * 1e6, 'bps']); });
    (r.queues || []).forEach(function (x) { S.push([portMod(net, x.name), 'queueLength:max', x.maxq, 'pk']); });
    if (o.conv !== undefined && o.conv !== null) S.push(['Net', 'convergenceTime', o.conv, 's']);
    S.push(['Net', 'simDuration', r.tEnd, 's']);
    return S; }
  EL.simExport = function (net, r, o) {
    o = o || {}; var H = header(o), V = vectors(net, r), S = scalars(net, r, o);
    var vec = H.slice(); V.forEach(function (v, id) { vec.push('vector ' + id + ' ' + q(v.mod) + ' ' + q(v.name) + ' TV', 'attr unit ' + q(v.unit)); });
    V.forEach(function (v, id) { v.pts.forEach(function (p) { vec.push(id + '\t' + num(p[0]) + '\t' + num(p[1])); }); });
    var sca = H.slice(); S.forEach(function (s) { sca.push('scalar ' + q(s[0]) + ' ' + q(s[1]) + ' ' + num(s[2]), 'attr unit ' + q(s[3])); });
    r.flows.forEach(function (f, i) { var vals = r.events.filter(function (e) { return e.kind === 'deliver' && e.flow === i && e.delay !== undefined && (e.dir === 'bk' || f.kind === 'udp'); }).map(function (e) { return e.delay; }), h = hist(vals, 16);
      if (!h) return; sca.push('statistic ' + q(mod(net, f.src, 'flow' + i)) + ' ' + q((f.kind === 'ping' ? 'rtt' : 'endToEndDelay') + ':histogram'));
      ['count', 'mean', 'stddev', 'min', 'max', 'sum', 'sqrsum'].forEach(function (k) { sca.push('field ' + k + ' ' + num(h[k])); });
      sca.push('attr unit s'); h.bins.forEach(function (b) { sca.push('bin\t' + (b[0] === '-INF' ? '-INF' : num(b[0])) + '\t' + b[1]); }); });
    var dec = function (v) { return num(v).replace('.', ','); }, csv = ['тип;модуль;имя;время;значение;единица'];
    V.forEach(function (v) { v.pts.forEach(function (p) { csv.push('vector;' + v.mod + ';' + v.name + ';' + dec(p[0]) + ';' + dec(p[1]) + ';' + v.unit); }); });
    S.forEach(function (s) { csv.push('scalar;' + s[0] + ';' + s[1] + ';;' + dec(s[2]) + ';' + s[3]); });
    return { vec: vec.join('\n') + '\n', sca: sca.join('\n') + '\n', csv: '﻿' + csv.join('\r\n') + '\r\n', vectors: V, scalars: S };
  };
})(typeof window !== 'undefined' ? window : global);
