/* Расширенный CLI коммутаторов MES (сверено с руководствами 10.4.6 и 6.6.8.8):
   port security (10.x: switchport port-security …, 6.x/4.x: port security …), статические MAC-записи,
   spanning-tree portfast / bpduguard, show version / system / clock / users / interfaces description,
   show running-config interface, clock set / timezone, traceroute, LLDP-соседи у MES.
   Поведение моделируется: port security режет кадры с чужих MAC, BPDU guard выключает порт при BPDU. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, S = EL.esr, IP = EL.ip, P = EL.Net.prototype, CMDS = E.CMDS, CFG = E.CFG;

  function cmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k] || (st.pos || {})[k]; }).filter(Boolean) : null; }
  function each(st, f) { var p = ports(st); if (!p) return '% Команда доступна в настройке порта'; p.forEach(f); }
  function normMac(w) {
    var h = String(w).toLowerCase().replace(/[^0-9a-f]/g, '');
    return h.length === 12 ? h.match(/../g).join(':') : null;
  }
  var VER = { '10': '10.4.6', '8': '8.4.0.7', '6': '6.6.8.8', '4': '4.0.23' };
  function branch(st) { var m = EL.MODELS[st.net ? st.net.devs[st.dev].model : ''] || {}, sw = m.fw || m.sw || '';
    return /4\.x/.test(sw) ? '4' : st.dialect; }
  function uptime(st) {
    var d = st.net && st.net.devs[st.dev], s = d ? Math.max(0, Math.floor(st.net.now - (d.boot || 0))) : 0, p2 = function (n) { return ('0' + n).slice(-2); };
    return Math.floor(s / 86400) + ',' + p2(Math.floor(s / 3600) % 24) + ':' + p2(Math.floor(s / 60) % 60) + ':' + p2(s % 60);
  }

  // ================================================================ port security
  // настройки на логическом порту: cfg.psec = { on, max, mode: lock|max-addresses|secure-…, act }
  function psec(st) { return function (p) { return p.psec || (p.psec = { on: false, max: st.dialect === '10' ? 8192 : 1, mode: 'lock', act: st.dialect === '10' ? 'restrict' : 'discard', lock: [] }); }; }
  function psecOn(st, on) {
    return each(st, function (p) { var c = psec(st)(p); c.on = on;
      if (on && st.net) {   // в режиме lock порт оставляет за собой уже выученные адреса и больше не учит
        var t = st.net.mac[st.dev], names = st.ctx.ports;
        c.lock = Object.keys(t).filter(function (k) { return names.indexOf(t[k].port) >= 0; }).map(function (k) { t[k].sec = true; return t[k].vlan + '|' + t[k].mac; });
      } });
  }
  // 10.x
  cmd(['10'], 'if range', 'switchport port-security enable', function (st) { return psecOn(st, true); }, 'Включить port security');
  cmd(['10'], 'if range', 'no switchport port-security enable', function (st) { return psecOn(st, false); });
  cmd(['10'], 'if range', 'switchport port-security mac-limit <n>', function (st, a) {
    if (a[0] > 8192) return '% Допустимо 0..8192'; return each(st, function (p) { psec(st)(p).max = a[0]; }); }, 'Сколько MAC-адресов разрешено на порту');
  cmd(['10'], 'if range', 'no switchport port-security mac-limit', function (st) { return each(st, function (p) { psec(st)(p).max = 8192; }); });
  cmd(['10'], 'if range', 'switchport port-security mode <w>', function (st, a) {
    var m = a[0].toLowerCase(), ok = ['max-addresses', 'lock', 'secure-delete-on-reset', 'secure-permanent'];
    if (ok.indexOf(m) < 0) return '% Режим: ' + ok.join(' | '); return each(st, function (p) { psec(st)(p).mode = m; }); }, 'Режим port security');
  cmd(['10'], 'if range', 'switchport port-security violation <w>', function (st, a) {
    var m = a[0].toLowerCase(), ok = ['restrict', 'protect', 'discard-shutdown'];
    if (ok.indexOf(m) < 0) return '% Действие: ' + ok.join(' | '); return each(st, function (p) { psec(st)(p).act = m; }); }, 'Что делать с кадром от чужого MAC');
  // 6.x / 4.x
  cmd(['6'], 'if range', 'port security', function (st) { return psecOn(st, true); }, 'Включить port security');
  cmd(['6'], 'if range', 'no port security', function (st) { return psecOn(st, false); });
  cmd(['6'], 'if range', 'port security max <n>', function (st, a) {
    if (a[0] > 32768) return '% Допустимо 0..32768'; return each(st, function (p) { psec(st)(p).max = a[0]; }); }, 'Сколько MAC-адресов разрешено');
  cmd(['6'], 'if range', 'no port security max', function (st) { return each(st, function (p) { psec(st)(p).max = 1; }); });
  cmd(['6'], 'if range', 'port security mode <rest>', function (st, a) {
    var m = a[0].toLowerCase().replace(/\s+/g, ' '), map = { 'lock': 'lock', 'max-addresses': 'max-addresses', 'secure permanent': 'secure-permanent', 'secure delete-on-reset': 'secure-delete-on-reset' };
    if (!map[m]) return '% Режим: lock | max-addresses | secure permanent | secure delete-on-reset';
    return each(st, function (p) { psec(st)(p).mode = map[m]; }); }, 'Режим port security');
  ['forward', 'discard', 'discard-shutdown'].forEach(function (act) {
    cmd(['6'], 'if range', 'port security ' + act, function (st) { return each(st, function (p) { psec(st)(p).act = act; psec(st)(p).on = true; }); }, 'Действие при нарушении');
  });
  function psecText(st) {
    var o = ['Port       Status    Mode                    Max   Action            Learned'], s = st.net, t = s ? s.mac[st.dev] : {};
    Object.keys(st.ports).concat(Object.keys(st.pos || {})).forEach(function (k) { var p = st.ports[k] || st.pos[k], c = p.psec; if (!c) return;
      var n = Object.keys(t).filter(function (x) { return t[x].port === k && t[x].sec; }).length;
      o.push((k + '           ').slice(0, 11) + ((c.on ? 'Enabled' : 'Disabled') + '          ').slice(0, 10) + (c.mode + '                        ').slice(0, 24) +
             (c.max + '      ').slice(0, 6) + (c.act + '                  ').slice(0, 18) + n + (p.errdis === 'port-security' ? '  (порт выключен: нарушение)' : '')); });
    return o.length > 1 ? o.join('\n') : '% Port security не настроен ни на одном порту';
  }
  ['', 'do '].forEach(function (pre) { var m = pre ? CFG : 'priv';
    cmd(['10'], m, pre + 'show port-security', psecText, 'Состояние port security');
    cmd(['6'], m, pre + 'show ports security', psecText, 'Состояние port security'); });

  // проверка кадра на входе порта: null — пропустить, строка — причина отбрасывания
  P.macIn = function (dev, port, v, mac) {
    var s = this, d = s.devs[dev], st = d.st, key = v + '|' + mac, t = s.mac[dev];
    if (d.type !== 'mes') { t[key] = { vlan: v, mac: mac, port: port, t: s.now }; return null; }
    if ((st.smac || {})[key]) return null;                       // статическая запись: не переучиваем
    var cfg = st.ports[port] || (st.pos || {})[port], c = cfg && cfg.psec;
    if (!c || !c.on) { t[key] = { vlan: v, mac: mac, port: port, t: s.now }; return null; }
    var mine = Object.keys(t).filter(function (k) { return t[k].port === port && t[k].sec; });
    if (t[key] && t[key].port === port && t[key].sec) { t[key].t = s.now; return null; }
    var ok = c.mode === 'lock' ? false : mine.length < c.max;
    if (ok) { t[key] = { vlan: v, mac: mac, port: port, t: s.now, sec: true }; return null; }
    if (c.act === 'forward') return null;                         // 6.x: пропустить, но не учить
    var why = d.name + ': port security на ' + port + ' — MAC ' + mac + ' не разрешён (' + (c.mode === 'lock' ? 'режим lock: новые адреса не учатся' :
      'лимит ' + c.max + ' адрес(а) исчерпан') + '), кадр отброшен';
    if (c.act === 'discard-shutdown') { cfg.shut = true; cfg.errdis = 'port-security'; s.gen++;
      why += '; порт выключен (discard-shutdown) — включить: shutdown, no shutdown'; }
    if (c.act === 'restrict' && st.log) st.log.push('%PORT_SECURITY-W-VIOLATION: ' + port + ' ' + mac);
    return why;
  };

  // ================================================================ STP: portfast и BPDU guard
  cmd(['10', '6'], 'if range', 'spanning-tree portfast', function (st) { return each(st, function (p) { p.portfast = true; }); }, 'Порт к конечному узлу: сразу в forwarding');
  cmd(['10', '6'], 'if range', 'no spanning-tree portfast', function (st) { return each(st, function (p) { p.portfast = false; }); });
  cmd(['10', '6'], 'if range', 'spanning-tree bpduguard enable', function (st) { return each(st, function (p) { p.bpduGuard = true; }); }, 'Выключить порт, если придёт BPDU');
  cmd(['10', '6'], 'if range', 'spanning-tree bpduguard disable', function (st) { return each(st, function (p) { p.bpduGuard = false; }); });
  cmd(['10', '6'], 'if range', 'no spanning-tree bpduguard', function (st) { return each(st, function (p) { p.bpduGuard = false; }); });
  // BPDU приходят от соседа-коммутатора с включённым STP; порт с bpduguard при этом выключается (err-disable)
  P.bpduGuard = function () {
    var s = this, hit = false;
    s.order.forEach(function (id) { var d = s.devs[id]; if (d.type !== 'mes' || d.off) return;
      Object.keys(d.st.ports).forEach(function (k) { var p = d.st.ports[k]; if (!p.bpduGuard || p.shut) return;
        var pr = s.peer(id, k); if (!pr) return; var nd = s.devs[pr.dev];
        if (nd.off || nd.type !== 'mes' || (nd.st.stp && nd.st.stp.on === false) || nd.st.ports[pr.port].shut || nd.st.ports[pr.port].stpOff) return;
        p.shut = true; p.errdis = 'bpduguard'; hit = true;
        if (d.st.log) d.st.log.push('%STP-W-BPDUGUARD: BPDU received on ' + k + ', port disabled'); });
    });
    return hit;
  };
  // no shutdown снимает err-disable
  CMDS.filter(function (c) { return c.pat.join(' ') === 'no shutdown'; }).forEach(function (c) {
    var run = c.run; c.run = function (st, a) { var p = ports(st); if (p) p.forEach(function (x) { delete x.errdis; }); return run(st, a); }; });

  // ================================================================ статические MAC-записи
  function addStatic(st, mac, v, ifw) {
    var m = normMac(mac); if (!m) return '% MAC в формате 00:11:22:33:44:55 / 0011.2233.4455';
    if (!st.vlans[v]) return '% VLAN ' + v + ' не создана';
    var r = E.ifList(String(ifw).trim().replace(/\s+/g, "")), k = r && r.length === 1 ? r[0] : null;
    if (!k) { var w = String(ifw).trim().toLowerCase().replace(/^(gigabitethernet|gi)\s*/, 'gi').replace(/^(tengigabitethernet|te)\s*/, 'te').replace(/^(fastethernet|fa)\s*/, 'fa').replace(/^port-channel\s*/, 'po');
      k = st.ports[w] || (st.pos || {})[w] ? w : null; }
    if (!k) return '% Нет такого порта: ' + ifw;
    st.smac = st.smac || {}; st.smac[v + '|' + m] = { vlan: v, mac: m, port: k };
    if (st.net) delete st.net.mac[st.dev][v + '|' + m];
  }
  cmd(['10'], 'config', 'mac-address-table static unicast <w> vlan <n> interface <rest>', function (st, a) {
    return addStatic(st, a[0], a[1], a[2].replace(/\s+status\s+.*$/i, '')); }, 'Статическая MAC-запись');
  cmd(['10'], 'config', 'no mac-address-table static unicast <w> vlan <n>', function (st, a) { var m = normMac(a[0]); if (st.smac) delete st.smac[a[1] + '|' + m]; });
  cmd(['6'], 'config', 'mac address-table static <w> vlan <n> interface <rest>', function (st, a) {
    return addStatic(st, a[0], a[1], a[2].replace(/\s+(permanent|delete-on-reset|delete-on-timeout|secure)$/i, '')); }, 'Статическая MAC-запись');
  cmd(['6'], 'config', 'no mac address-table static <w> vlan <n>', function (st, a) { var m = normMac(a[0]); if (st.smac) delete st.smac[a[1] + '|' + m]; });

  // ================================================================ время, версия, пользователи
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], DOW = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  function mesNow(st) { return EL.clock.now() + (st.clk || 0); }
  function clockText(st) {
    var tz = st.tzo || 0, d = new Date(mesNow(st) + tz * 3600e3), p2 = function (n) { return ('0' + n).slice(-2); };
    return p2(d.getUTCHours()) + ':' + p2(d.getUTCMinutes()) + ':' + p2(d.getUTCSeconds()) + ' ' + (st.tzn || 'UTC') + ' ' + DOW[d.getUTCDay()] + ' ' +
      MON[d.getUTCMonth()] + ' ' + d.getUTCDate() + ' ' + d.getUTCFullYear() + '\nTime source is ' + (st.sntp && st.sntp.length ? 'sntp' : 'static');
  }
  cmd(['10', '6'], 'priv', 'clock set <w> <n> <w> <n>', function (st, a) {
    var t = a[0].match(/^(\d{1,2}):(\d{2}):(\d{2})$/), mo = MON.map(function (m) { return m.toLowerCase(); }).indexOf(a[2].toLowerCase().slice(0, 3));
    if (!t || +t[1] > 23 || +t[2] > 59 || +t[3] > 59) return '% Время: hh:mm:ss';
    if (mo < 0) return '% Месяц: Jan..Dec'; if (a[1] < 1 || a[1] > 31) return '% День: 1..31'; if (a[3] < 2000 || a[3] > 2037) return '% Год: 2000..2037';
    st.clk = Date.UTC(a[3], mo, a[1], +t[1], +t[2], +t[3]) - (st.tzo || 0) * 3600e3 - EL.clock.now(); }, 'Установить время: hh:mm:ss день месяц год');
  cmd(['10', '6'], 'config', 'clock timezone <w> <w>', function (st, a) {
    var h = +a[1]; if (!/^[+-]?\d{1,2}$/.test(a[1]) || h < -12 || h > 14) return '% Смещение: -12..+14';
    st.tzn = a[0]; st.tzo = h; }, 'Часовой пояс: имя смещение');
  cmd(['10', '6'], 'config', 'no clock timezone', function (st) { delete st.tzn; delete st.tzo; });
  function version(st) {
    var d = st.net ? st.net.devs[st.dev] : { model: 'MES' }, m = EL.MODELS[d.model] || {}, b = branch(st);
    return 'Active-image: flash://system/images/image' + (b === '8' ? '.stk' : '1.bin') + '\n  Version: ' + VER[b] +
      '\n\nSW version    ' + VER[b] + '\nHW version    ' + d.model +
      '\nSystem MAC    ' + (st.bmac || '') + '\nUptime        ' + uptime(st) + (m.full ? '\nDescription   ' + m.full : '');
  }
  function users(st) {
    return '    Username        Protocol    Location\n--------------- ------------ -----------------------\n' +
      '     ' + (Object.keys(st.users)[0] || 'admin') + '          Serial      0.0.0.0';
  }
  function descText(st) {
    var o = ['Port         Description', '------------ ----------------------------------'];
    Object.keys(st.ports).concat(Object.keys(st.pos || {})).forEach(function (k) { var p = st.ports[k] || st.pos[k]; if (p.desc) o.push((k + '             ').slice(0, 13) + p.desc); });
    return o.length > 2 ? o.join('\n') : o.concat(['(описаний нет — description в настройке порта)']).join('\n');
  }
  function runIf(st, w) {
    var k = (E.ifList(String(w).trim().replace(/\s+/g, "")) || [])[0] || String(w).toLowerCase().replace(/\s+/g, '');
    if (!st.ports[k] && !(st.pos || {})[k]) return '% Нет такого интерфейса: ' + w;
    var lines = E.showRun(st).split('\n'), long = 'interface ' + E.longIf(k).replace(' ', ''), out = [], on = false;
    lines.forEach(function (l) { if (l === long) on = true; if (on) out.push(l); if (on && l === 'exit') on = false; });
    return out.length ? out.join('\n') : long + '\nexit';
  }
  function lldpMes(st) {
    var s = st.net; if (!s) return '';
    if (st.lldp === false) return '% LLDP выключен — ' + (st.dialect === '6' ? 'lldp run' : 'set lldp enable');
    var o = [];
    Object.keys(st.ports).forEach(function (k) { var pr = s.peer(st.dev, k); if (!pr || !s.linkUp(st.dev, k)) return;
      var nd = s.devs[pr.dev], name = null, cap = null;
      if (nd.type === 'mes' && nd.st.lldp !== false) { name = nd.st.host; cap = 'B'; }
      if (nd.type === 'esr' && nd.st.run.lldp && (nd.st.run.ifs[pr.port] || {}).lldpTx) { name = nd.st.run.host; cap = 'R'; }
      if (!name) return;
      o.push((k + '          ').slice(0, 11) + ((nd.type === 'mes' ? nd.st.bmac : EL.mac(name + 'sys')) + '    ').slice(0, 20) + (pr.port + '           ').slice(0, 12) +
             (name + '               ').slice(0, 16) + (cap + '             ').slice(0, 14) + (s.lldpTtl ? s.lldpTtl(st.dev, k) : 120)); });
    return ['  Port     Device ID          Port ID     System Name     Capabilities  TTL', '--------- ----------------- ----------- --------------- ------------- ---']
      .concat(o.length ? o : ['% Соседей нет (у соседа выключен LLDP или нет линка)']).join('\n');
  }
  function shows(pre, m) {
    cmd(['10', '6', '8'], m, pre + 'show version', version, 'Версия ПО и оборудования');
    cmd(['10', '6', '8'], m, pre + 'show system', function (st) { return version(st) + '\nSystem Name   ' + st.host + '\nPorts         ' + Object.keys(st.ports).length; }, 'Сведения о системе');
    cmd(['10', '6'], m, pre + 'show clock', clockText, 'Текущее время');
    cmd(['10', '6', '8'], m, pre + 'show users', users, 'Кто подключён');
    cmd(['10', '6'], m, pre + 'show interfaces description', descText, 'Описания портов');
    cmd(['10', '6'], m, pre + 'show running-config interface <rest>', function (st, a) { return runIf(st, a[0]); }, 'Конфигурация одного порта');
    cmd(['10', '6'], m, pre + 'show lldp neighbors', lldpMes, 'Соседи LLDP');
  }
  shows('', 'priv'); shows('do ', CFG);
  cmd(['10'], 'priv', 'traceroute <ip>', function (st, a) { return st.net ? st.net.traceText(st.dev, a[0]) : ''; }, 'Маршрут до узла');
  cmd(['6'], 'priv', 'traceroute ip <ip>', function (st, a) { return st.net ? st.net.traceText(st.dev, a[0]) : ''; }, 'Маршрут до узла');

  // running-config: статические MAC, часовой пояс, port security и STP на портах
  E.RUNX.push(function (st, o) {
    if (st.tzn) o.push('clock timezone ' + st.tzn + ' ' + (st.tzo >= 0 ? '+' : '') + st.tzo);
    Object.keys(st.smac || {}).forEach(function (k) { var x = st.smac[k], ifl = 'interface ' + E.longIf(x.port);
      o.push(st.dialect === '6' ? 'mac address-table static ' + x.mac + ' vlan ' + x.vlan + ' ' + ifl + ' permanent'
                                : 'mac-address-table static unicast ' + x.mac + ' vlan ' + x.vlan + ' ' + ifl + ' status permanent'); });
  });
  E.PORTX.push(function (st, k, p, d) { var c = p.psec;
      if (p.portfast) d.push(st.dialect === '8' ? ' spanning-tree edgeport' : ' spanning-tree portfast');
      if (p.bpduGuard) d.push(' spanning-tree bpduguard enable');
      if (c && c.on) { if (st.dialect === '6') { d.push(' port security'); if (c.max !== 1) d.push(' port security max ' + c.max);
          if (c.mode !== 'lock') d.push(' port security mode ' + c.mode.replace('secure-', 'secure ')); if (c.act !== 'discard') d.push(' port security ' + c.act); }
        else { d.push(' switchport port-security enable'); if (c.max !== 8192) d.push(' switchport port-security mac-limit ' + c.max);
          if (c.mode !== 'lock') d.push(' switchport port-security mode ' + c.mode); if (c.act !== 'restrict') d.push(' switchport port-security violation ' + c.act); } }
  });

  // ================================================================ ESR: версия, описания, LLDP видит MES
  S.cmd('priv', 'show version', function (st) { return 'Boot version:\n  1.24.2\nSW version (active):\n  1.24.2\nSW version (inactive):\n  1.23.1\nUptime: ' + uptime(st); }, 'Версия ПО');
  S.cmd('priv', 'show interfaces description', function (st) {
    var o = ['Interface             Admin   Link    Description', '--------------------  ------  ------  ------------------------------'];
    Object.keys(st.run.ifs).forEach(function (k) { var x = st.run.ifs[k];
      o.push((k + '                      ').slice(0, 22) + ((x.shut ? 'Down' : 'Up') + '        ').slice(0, 8) +
             ((st.net && st.net.linked(st.dev, k.split('.')[0]) && !x.shut ? 'Up' : 'Down') + '        ').slice(0, 8) + (x.desc || '--')); });
    return o.join('\n'); }, 'Описания интерфейсов');
  var esrLldp = P.lldpText;
  P.lldpText = function (id) {
    var out = esrLldp.call(this, id), s = this, c = this.devs[id].st.run, extra = [];
    if (!c || !c.lldp) return out;
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k]; if (k.indexOf('.') > 0 || !x.lldpRx) return;
      var pr = s.peer(id, k); if (!pr || !s.linkUp(id, k)) return; var nd = s.devs[pr.dev];
      if (nd.type !== 'mes' || nd.st.lldp === false) return;
      extra.push((k + '          ').slice(0, 10) + (nd.st.bmac + '   ').slice(0, 20) + (pr.port + '          ').slice(0, 12) + (nd.st.host + '              ').slice(0, 15) + 'B             ' + (s.lldpTtl ? s.lldpTtl(id, k) : 120)); });
    if (!extra.length) return out;
    return out.replace(/\n% Соседей нет[^\n]*$/, '') + '\n' + extra.join('\n');
  };

  // время работы: отсчёт от включения/перезагрузки
  var reboot0 = P.reboot, add0 = P.add;
  P.add = function () { var d = add0.apply(this, arguments); d.boot = this.now; return d; };
  P.reboot = function (id) { var r = reboot0.apply(this, arguments); if (this.devs[id]) this.devs[id].boot = this.now; return r; };
})(typeof window !== 'undefined' ? window : global);
