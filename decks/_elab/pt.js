/* Симуляция пакетов в стиле Packet Tracer поверх логики оборудования: трасса обмена (ARP, ICMP, DHCP, … — как её строит модель
   сети с правилами MES/ESR/WLC/OLT/ME) превращается в список событий со временем модели. Время кадра на кабеле — как в OMNeT++:
   передача = биты / скорость линка (согласование speed/duplex, тип кабеля), распространение = 100 м / 2·10⁸ м/с, обработка в устройстве 10 мкс.
   L1: линейный код и модуляция по типу кабеля и скорости (стандарты IEEE 802.3, ITU-T G.984, EIA RS-232) и сигнал первых байт кадра.
   Упрощения: сигнал 1000BASE-T показан условно (2 бита → уровень PAM-5, без скремблера и треллис-кода), 8b/10b и 64b/66b — исходные биты
   без кодовых таблиц и скремблера (у 64b/66b — с синхрозаголовком 01); размер кадра — по типу PDU (ARP 60 байт, IP — 14 + IP-пакет). */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype;
  var PROC = 10e-6, PROP = 100 / 2e8;
  // протокол PDU для списка событий
  EL.ptProto = function (f) {
    if (!f) return 'Info';
    if (f.type === 'arp') return 'ARP';
    if (f.type === 'stp') return 'STP';
    if (f.icmp6) return 'ICMPv6';
    if (f.proto === 'esp') return 'ESP'; if (f.proto === 'gre') return 'GRE'; if (f.proto === 'igmp') return 'IGMP';
    if (f.dhcp || (f.proto === 'udp' && (f.dport === 67 || f.dport === 68))) return 'DHCP';
    var port = f.reply ? f.sport : f.dport, M = { udp: { 53: 'DNS', 123: 'NTP', 69: 'TFTP', 514: 'Syslog', 500: 'ISAKMP', 1812: 'RADIUS' }, tcp: { 22: 'SSH', 23: 'Telnet', 80: 'HTTP', 443: 'HTTPS', 179: 'BGP', 8043: 'HTTPS' } };
    if (f.proto === 'icmp') return 'ICMP';
    return (M[f.proto] && M[f.proto][port]) || String(f.proto || 'IP').toUpperCase();
  };
  function bytesOf(f) { if (!f) return 64; if (f.type === 'arp') return 60; var ip = f.size || (f.proto === 'icmp' ? 84 : f.proto === 'tcp' ? 60 : 48); return Math.max(60, 14 + ip); }
  // линейный код кабеля
  EL.lineCode = function (net, li) {
    var l = net.links[li]; if (!l) return null;
    var ph = net.phys(l.a.dev, l.a.port), cab = ph.cab || l.cab || 'cu', sp = ph.speed || 1000;
    if (cab === 'rs232') return { name: 'RS-232', code: 'uart', rate: 115200, bps: 115200, text: 'EIA RS-232, асинхронная передача: старт-бит 0, 8 бит данных младшим вперёд, стоп-бит 1; логическая 1 — отрицательное напряжение, 0 — положительное. 115200 бит/с, 8N1' };
    if (cab === 'pon') return { name: 'GPON', code: 'nrz', bps: 2488.32e6, text: 'ITU-T G.984: вниз 2,488 Гбит/с (λ 1490 нм), вверх 1,244 Гбит/с (λ 1310 нм, TDMA по выделенным окнам); NRZ со скремблированием' };
    if (cab === 'sfp10g' || sp >= 10000) return { name: '10GBASE-R', code: '64b66b', bps: 10.3125e9, text: 'IEEE 802.3 гл. 49: блоки 64b/66b (синхрозаголовок 01 — данные, 10 — управление), самосинхронизирующийся скремблер x⁵⁸+x³⁹+1, NRZ, 10,3125 Гбод' };
    if (cab === 'sfp1g') return { name: '1000BASE-X', code: '8b10b', bps: 1.25e9, text: 'IEEE 802.3 гл. 36: код 8b/10b (каждый байт → 10 бит, баланс единиц и нулей), NRZ, 1,25 Гбод' };
    if (sp <= 10) return { name: '10BASE-T', code: 'manchester', bps: 10e6, text: 'IEEE 802.3 гл. 14: манчестерский код — переход в середине каждого бита: 0 — сверху вниз, 1 — снизу вверх; 10 Мбит/с = 20 Мбод' };
    if (sp <= 100) return { name: '100BASE-TX', code: 'mlt3', bps: 100e6, text: 'IEEE 802.3 гл. 24–25: 4B5B (4 бита → 5) + MLT-3 (1 — шаг по уровням 0, +1, 0, −1; 0 — уровень держится), 125 Мбод по одной паре' };
    return { name: '1000BASE-T', code: 'pam5', bps: 1e9, text: 'IEEE 802.3 гл. 40: 4D-PAM5 — 4 пары одновременно в обе стороны, уровни −2, −1, 0, +1, +2, 125 Мбод на пару, скремблер и треллис-код; рисунок условный' };
  };
  // сигнал первых байт: массив [уровень] по равным интервалам; bits — для подписи
  var B4B5 = ['11110', '01001', '10100', '10101', '01010', '01011', '01110', '01111', '10010', '10011', '10110', '10111', '11010', '11011', '11100', '11101'];
  EL.waveform = function (code, bytes) {
    var bits = []; bytes.forEach(function (b) { for (var i = 0; i < 8; i++) bits.push((b >> i) & 1); });   // Ethernet: младший бит байта первым
    var L = [], lv = 0, seq = [0, 1, 0, -1], k = 0;
    if (code === 'manchester') bits.forEach(function (b) { L.push(b ? -1 : 1, b ? 1 : -1); });
    else if (code === 'mlt3') { var s = ''; bytes.forEach(function (b) { s += B4B5[b & 15] + B4B5[b >> 4]; }); s.split('').forEach(function (c) { if (c === '1') k = (k + 1) % 4; L.push(seq[k]); }); bits = s.split('').map(Number); }
    else if (code === 'pam5') { var map = { '00': -2, '01': -1, '10': 1, '11': 2 }; for (var i = 0; i < bits.length; i += 2) L.push(map['' + bits[i] + bits[i + 1]] / 2); }
    else if (code === '64b66b') { bits = [0, 1].concat(bits); bits.forEach(function (b) { L.push(b ? 1 : -1); }); }
    else if (code === 'uart') { var u = []; bytes.forEach(function (b) { u.push(0); for (var j = 0; j < 8; j++) u.push((b >> j) & 1); u.push(1); }); bits = u; u.forEach(function (b) { L.push(b ? -1 : 1); }); }
    else bits.forEach(function (b) { L.push(b ? 1 : -1); });
    void lv; return { levels: L, bits: bits };
  };
  function macBytes(m) { return String(m || 'ff:ff:ff:ff:ff:ff').split(':').map(function (x) { return parseInt(x, 16) || 0; }); }
  EL.ptBytes = function (f) { return macBytes(f && f.dmac).slice(0, 2); };
  // события из трассы: {t, dur, kind:'pdu'|'info', proto, from, to, li, step, f, text, tag}
  EL.ptEvents = function (net, steps, src) {
    var out = [], t = 0, at = src;
    steps.forEach(function (s, si) {
      if (s.segs && s.segs.length) {
        var bytes = bytesOf(s.f), end = {}, tEnd = t, proto = s.k === 'arp' || s.k === 'arpr' ? 'ARP' : EL.ptProto(s.f);
        s.segs.forEach(function (sg) {
          var start = end[sg.from] !== undefined ? end[sg.from] : t, lc = EL.lineCode(net, sg.li), bps = lc ? (lc.code === 'uart' ? lc.bps * 0.8 : lc.code === '8b10b' ? lc.bps * 0.8 : lc.code === '64b66b' ? lc.bps * 64 / 66 : lc.bps) : 1e9;
          var dur = bytes * 8 / bps + PROP;
          out.push({ t: start, dur: dur, kind: 'pdu', proto: proto, from: sg.from, to: sg.to, li: sg.li, step: si, f: s.f, text: s.t, tag: sg.tag, bytes: bytes });
          end[sg.to] = start + dur + PROC; tEnd = Math.max(tEnd, end[sg.to]); at = sg.to; });
        t = tEnd;
      } else { out.push({ t: t, dur: 0, kind: 'info', proto: s.k === 'drop' ? 'Отброшен' : s.k === 'ok' ? 'Доставлен' : s.k === 'nat' ? 'NAT' : 'Решение', from: at, to: at, step: si, text: s.t }); t += PROC; }
    });
    return out;
  };
})(typeof window !== 'undefined' ? window : global);
