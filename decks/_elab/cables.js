/* Типы медных кабелей и огоньки на концах кабелей (как светодиоды порта на железе).
   Кабели: «Медь RJ-45, авто» (тип подбирается сам), прямой (straight-through, T568B–T568B), перекрёстный (crossover, T568A–T568B),
   Serial (V.35, для последовательных WAN-портов — в Ethernet-порт не подключается); оптика, DAC, RS-232, RJ-11, PON — в physics.js / scs.js / tau.js / olt.js.
   MDI / MDI-X: порт коммутатора — MDI-X, порт ПК, сервера, маршрутизатора — MDI. Прямой кабель — между MDI и MDI-X, перекрёстный — между одинаковыми.
   Auto-MDIX (порт сам меняет пары приёма и передачи) — достаточно на одном конце. По спецификациям: MES — Auto MDI/MDIX (даташиты MES, в т. ч. 100-мегабитные
   порты MES1428); LAN-порты 10/100BASE-T RG-35-WZ — данных нет, Auto-MDIX не считаем (LAN — MDI-X, WAN — MDI); остальные медные порты без данных
   считаются гигабитными (1000BASE-T) — с Auto-MDIX.
   Огонёк конца кабеля: зелёный — линк есть; оранжевый — линк есть, но порт ещё не передаёт (STP listening / learning / blocking, порт LACP не в агрегате);
   красный — нет линка (устройство или порт выключены, кабель не того типа, несовместимые модули). Огоньки видны в обоих режимах, причина — в «Тесте». */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, CAB = EL.CABLES;
  CAB.cu = 'Медь RJ-45, авто (прямой / перекрёстный подбирается сам)';
  CAB.straight = 'Медь RJ-45, прямой (straight-through, T568B–T568B)';
  CAB.cross = 'Медь RJ-45, перекрёстный (crossover, T568A–T568B)';
  CAB.serial = 'Serial (V.35, DCE–DTE)';
  var COPPER = { straight: 1, cross: 1 };
  function sw(d) { return d.type === 'mes' && d.sub !== 'ont' && d.sub !== 'lte' && d.sub !== 'eont'; }
  function cpeLan(d, port) { return d.sub === 'cpe' && port !== 'gi1/0/1'; }
  // MDI-X — порты коммутаторов и LAN-порты абонентского роутера, MDI — остальные
  function role(d, port) { return sw(d) || cpeLan(d, port) ? 'MDI-X' : 'MDI'; }
  function autoMdix(d, port) { return !cpeLan(d, port); }
  EL.mdi = { role: role, auto: autoMdix };
  var phys0 = P.phys;
  P.phys = function (id, port) {
    var pr = this.peer(id, port); if (!pr) return phys0.apply(this, arguments);
    var l = this.links[pr.li], cab = l.cab;
    if (cab === 'serial') return { up: false, why: 'Serial-кабель (V.35) — для последовательных WAN-портов; в порты ' + port + ' и ' + pr.port + ' он не подключается' };
    if (!COPPER[cab]) return phys0.apply(this, arguments);
    l.cab = 'cu'; var r; try { r = phys0.apply(this, arguments); } finally { l.cab = cab; }
    if (/оптическ|модуль/.test(r.why || '') || r.cab && r.cab !== 'cu') return { up: false, why: CAB[cab] + ': медный кабель в оптический порт не подключается' };
    var a = this.devs[id], b = this.devs[pr.dev], ra = role(a, port), rb = role(b, pr.port), aa = autoMdix(a, port), ab = autoMdix(b, pr.port);
    var need = ra === rb ? 'cross' : 'straight';
    if (need !== cab && !aa && !ab) return { up: false, why: (cab === 'straight' ? 'прямой' : 'перекрёстный') + ' кабель между ' + ra + ' (' + a.name + ' ' + port + ') и ' + rb + ' (' + b.name + ' ' + pr.port +
      '): нужен ' + (need === 'cross' ? 'перекрёстный' : 'прямой') + ', а Auto-MDIX нет ни на одном конце — передача попадает на передачу, линка нет' };
    var o = EL.clone(r); o.cab = cab; if (need !== cab) o.mdix = (aa ? a.name + ' ' + port : b.name + ' ' + pr.port) + ': Auto-MDIX поменял пары'; return o;
  };
  var ct0 = P.cableText;
  P.cableText = function (l) { return COPPER[l.cab] || l.cab === 'serial' ? CAB[l.cab] : ct0.apply(this, arguments); };

  // ---------------------------------------------------------------- огонёк конца кабеля
  function shutWhy(d, p) {
    if (d.type === 'mes') { var x = d.st.ports[p] || {}; return x.shut ? 'порт ' + p + ' выключен' + (x.errdis ? ' (err-disabled: ' + x.errdis + ')' : ' (shutdown)') : null; }
    if (d.type === 'esr') { var y = d.st.run.ifs[p] || {}; return y.shut ? 'порт ' + p + ' выключен (shutdown)' : null; }
    if (d.type === 'deb' && !d.st.up) return 'сетевой интерфейс выключен (ip link set down)';
    return null; }
  P.ledOf = function (id, port) {
    var d = this.devs[id], pr = this.peer(id, port); if (!d || !pr) return null; var b = this.devs[pr.dev];
    if (d.off) return { c: 'r', why: d.name + ' выключено' };
    if (b.off) return { c: 'r', why: 'на другом конце ' + b.name + ' выключено' };
    var w = shutWhy(d, port); if (w) return { c: 'r', why: w };
    w = shutWhy(b, pr.port); if (w) return { c: 'r', why: 'на другом конце (' + b.name + '): ' + w };
    if (!this.linkUp(id, port)) { var ph = this.phys(id, port); return { c: 'r', why: ph.why || 'нет линка' }; }
    if (d.type === 'mes' && d.st.ports && d.st.ports[port]) {
      var L = this.lportOf(id, port);
      if (!L) return { c: 'o', why: 'LACP: порт не собран в агрегат (port-channel не поднят или режимы сторон не совпадают)' };
      var z = this.stpState ? this.stpState(id, L.name, 0) : null;
      if (z && z !== 'Frw') return { c: 'o', why: 'STP: ' + (EL.STPN ? EL.STPN[z] : z) + ' — порт ещё (или уже) не передаёт кадры' };
    }
    var ph2 = this.phys(id, port);
    return { c: 'g', why: 'линк есть' + (ph2.speed ? ', ' + (ph2.speed >= 1000 ? ph2.speed / 1000 + ' Гбит/с' : ph2.speed + ' Мбит/с') : '') + (ph2.dup && ph2.dup[id] ? ', ' + ph2.dup[id] + '-duplex' : '') + (ph2.mdix ? '; ' + ph2.mdix : '') };
  };
})(typeof window !== 'undefined' ? window : global);
