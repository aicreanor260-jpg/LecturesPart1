/* Диалекты CLI коммутаторов MES по веткам ПО (сверено с руководствами Eltex):
   '10' — MES14xx/24xx/3400/37xx, ПО 10.4 (базовый синтаксис движка);
   '6'  — MES23xx/33xx/35xx/53xx/5400/5500/5600/5700, ПО 6.6 и 4.0 (общий синтаксис):
          spanning-tree mode stp|rstp|mstp, channel-group N mode on|auto, lldp run, port monitor, show interfaces channel-group;
   '8'  — MES5448/MES7048, ПО 8.4 (FASTPATH): приглашения «(host) #», порты 1/0/N, vlan database из привилегированного режима,
          port-channel + addport, vlan participation/tagging/pvid, spanning-tree mst priority, monitor session … mode. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, CMDS = E.CMDS;

  function find(pat) { return CMDS.filter(function (c) { return c.pat.join(' ') === pat; }); }
  function only(pat, dl) { find(pat).forEach(function (c) { c.dl = dl; }); }
  function not(pat, dl) { find(pat).forEach(function (c) { c.xdl = (c.xdl || []).concat(dl); }); }
  function cmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function ports(st) { return st.ctx && st.ctx.ports ? st.ctx.ports.map(function (k) { return st.ports[k] || (st.pos || {})[k]; }) : null; }
  function stp(st) { return st.stp || (st.stp = { on: true, mode: 'mst', prio: 32768 }); }

  // ---------------------------------------------------------------- ветка 10.x: только свои варианты
  only('spanning-tree mode <w>', ['10']);
  only('channel-group <n> mode <w>', ['10']);

  // ---------------------------------------------------------------- ветки 6.x и 4.x
  var STPM = ['stp', 'rstp', 'mstp', 'pvst', 'rapid-pvst'];
  cmd(['6', '8'], 'config', 'spanning-tree mode <w>', function (st, a) { var m = a[0].toLowerCase();
    if (STPM.indexOf(m) < 0) return '% Режим: ' + STPM.join(' | ');
    stp(st).mode = { stp: 'stp', rstp: 'rst', mstp: 'mst', pvst: 'pvst', 'rapid-pvst': 'rapid-pvst' }[m]; }, 'Режим STP');
  cmd(['6'], 'if range', 'channel-group <n> mode <w>', function (st, a) {
    var m = a[1].toLowerCase(); if (m !== 'on' && m !== 'auto') return '% Режим: on (статическая группа) | auto (LACP)';
    if (!st.ctx || !st.ctx.ports || st.ctx.ports.some(function (k) { return !st.ports[k]; })) return '% Команда для физического порта';
    st.pos = st.pos || {}; if (!st.pos['po' + a[0]]) st.pos['po' + a[0]] = { mode: 'access', access: 1, allowed: [], native: 1, pvid: 1, gtag: [], guntag: [1], shut: false };
    st.ctx.ports.forEach(function (k) { st.ports[k].cg = { id: a[0], mode: m === 'auto' ? 'active' : 'on' }; }); }, 'Добавить порт в группу (auto — LACP)');
  cmd(['6'], 'config', 'lldp run', function (st) { st.lldp = true; }, 'Включить LLDP');
  cmd(['6'], 'config', 'no lldp run', function (st) { st.lldp = false; });
  cmd(['10'], 'config', 'set lldp enable', function (st) { st.lldp = true; }, 'Включить LLDP');
  cmd(['10'], 'config', 'set lldp disable', function (st) { st.lldp = false; });
  // 4.x: зеркалирование настраивается на порту-получателе
  function portMon(st, src, dir) {
    if (!st.ctx || !st.ctx.ports || st.ctx.ports.length !== 1) return '% Команда в настройке одного порта-получателя';
    if (src.some(function (k) { return !st.ports[k]; })) return '% Такого порта нет на устройстве';
    var m = (st.mon = st.mon || {}), s = m[9] = m[9] || { src: {} }; s.dst = st.ctx.ports[0]; src.forEach(function (k) { s.src[k] = dir; });
  }
  cmd(['6'], 'if', 'port monitor <if>', function (st, a) { return portMon(st, a[0], 'both'); }, 'Зеркалировать порт сюда');
  cmd(['6'], 'if', 'port monitor <if> <w>', function (st, a) { var d = a[1].toLowerCase(); if (d !== 'rx' && d !== 'tx') return '% rx | tx';
    return portMon(st, a[0], d); });
  cmd(['6'], 'if', 'no port monitor <if>', function (st, a) { var s = (st.mon || {})[9]; if (s) a[0].forEach(function (k) { delete s.src[k]; }); });
  ['', 'do '].forEach(function (pre) {
    cmd(['6'], pre ? E.CFG : 'priv', pre + 'show interfaces channel-group', function (st) { return st.net ? st.net.lagText(st.dev) : ''; });
    cmd(['6', '10'], pre ? E.CFG : 'priv', pre + 'show ports monitor', function (st) { var s = (st.mon || {})[9];
      return s ? 'Destination: ' + s.dst + '\n' + Object.keys(s.src).map(function (k) { return 'Source: ' + k + ' ' + s.src[k]; }).join('\n') : '% Зеркалирование не настроено'; });
  });

  // ---------------------------------------------------------------- ветка 8.x (FASTPATH)
  not('vlan database', ['8']); not('vlan <n>', ['8']); not('vlan <list>', ['8']); not('vlan <n> name <w>', ['8']); not('interface <if>', ['8']);
  not('channel-group <n> mode <w>', ['8']); not('spanning-tree priority <n>', ['8']);
  cmd(['8'], 'priv', 'vlan database', function (st) { st.mode = 'vlan'; st.ctx = null; }, 'Режим базы VLAN');
  cmd(['8'], 'vlan', 'vlan <list>', function (st, a) { if (a[0].some(function (v) { return v < 2 || v > 4093; })) return '% VLAN 2–4093';
    a[0].forEach(function (v) { if (!st.vlans[v]) st.vlans[v] = '-'; }); }, 'Создать VLAN');
  cmd(['8'], 'vlan', 'no vlan <list>', function (st, a) { a[0].forEach(function (v) { if (v === 1) return; delete st.vlans[v];
    Object.keys(st.ports).forEach(function (k) { var p = st.ports[k]; if (p.access === v) p.access = 1; }); }); });
  cmd(['8'], 'vlan', 'vlan name <n> <w>', function (st, a) { if (!st.vlans[a[0]]) return '% VLAN ' + a[0] + ' не существует'; st.vlans[a[0]] = a[1]; }, 'Имя VLAN');
  cmd(['8'], 'vlan', 'exit', function (st) { st.mode = 'priv'; });
  cmd(['8'], 'config', 'interface <if>', function (st, a) {
    if (a[0].some(function (k) { return !st.ports[k]; })) return '% Такого порта нет на устройстве';
    st.mode = a[0].length > 1 ? 'range' : 'if'; st.ctx = { ports: a[0] }; }, 'Настройка порта (диапазон: 1/0/1-1/0/4)');
  cmd(['8'], 'config', 'interface lag <n>', function (st, a) { if (!(st.pos || {})['po' + a[0]]) return '% LAG ' + a[0] + ' не создан — port-channel ИМЯ';
    st.mode = 'if'; st.ctx = { ports: ['po' + a[0]], lag: a[0] }; }, 'Настройка LAG');
  cmd(['8'], 'config', 'port-channel <w>', function (st, a) { st.pos = st.pos || {};
    var n = 1; while (st.pos['po' + n]) n++; if (n > 64) return '% Нет свободных LAG';
    st.pos['po' + n] = { mode: 'general', access: 1, allowed: [], native: 1, pvid: 1, gtag: [], guntag: [1], shut: false, name: a[0], lacp: true };
    return 'LAG ' + n + ' (' + a[0] + ') создан: interface lag ' + n; }, 'Создать LAG');
  cmd(['8'], 'if', 'port-channel static', function (st) { if (!st.ctx || !st.ctx.lag) return '% Команда в настройке LAG'; st.pos['po' + st.ctx.lag].lacp = false;
    Object.keys(st.ports).forEach(function (k) { var c = st.ports[k].cg; if (c && c.id === st.ctx.lag) c.mode = 'on'; }); }, 'Статический LAG без LACP');
  cmd(['8'], 'if', 'no port-channel static', function (st) { if (!st.ctx || !st.ctx.lag) return; st.pos['po' + st.ctx.lag].lacp = true;
    Object.keys(st.ports).forEach(function (k) { var c = st.ports[k].cg; if (c && c.id === st.ctx.lag) c.mode = 'active'; }); });
  function addport(st, n) {
    var po = (st.pos || {})['po' + n]; if (!po) return '% LAG ' + n + ' не создан';
    if (!st.ctx || !st.ctx.ports || st.ctx.ports.some(function (k) { return !st.ports[k]; })) return '% Команда в настройке физического порта';
    st.ctx.ports.forEach(function (k) { st.ports[k].cg = { id: n, mode: po.lacp ? 'active' : 'on' }; });
  }
  cmd(['8'], 'if range', 'addport lag <n>', function (st, a) { return addport(st, a[0]); }, 'Добавить порт в LAG');
  cmd(['8'], 'if range', 'addport <w>', function (st, a) { var m = String(a[0]).match(/^(?:0\/)?3\/(\d+)$/); if (!m) return '% Формат: addport lag N или addport 3/N';
    return addport(st, +m[1]); });
  cmd(['8'], 'if range', 'deleteport lag <n>', function (st) { if (st.ctx && st.ctx.ports) st.ctx.ports.forEach(function (k) { if (st.ports[k]) delete st.ports[k].cg; }); });
  cmd(['8'], 'if range', 'vlan participation include <list>', function (st, a) {
    var bad = a[0].filter(function (v) { return !st.vlans[v]; }); if (bad.length) return '% VLAN ' + E.fmtList(bad) + ' не созданы';
    ports(st).forEach(function (p) { p.mode = 'general'; a[0].forEach(function (v) { if (p.guntag.indexOf(v) < 0 && p.gtag.indexOf(v) < 0) p.guntag.push(v); }); }); }, 'Порт — член VLAN');
  cmd(['8'], 'if range', 'vlan participation exclude <list>', function (st, a) {
    ports(st).forEach(function (p) { p.guntag = p.guntag.filter(function (v) { return a[0].indexOf(v) < 0; }); p.gtag = p.gtag.filter(function (v) { return a[0].indexOf(v) < 0; }); }); });
  cmd(['8'], 'if range', 'vlan tagging <list>', function (st, a) { ports(st).forEach(function (p) { p.mode = 'general';
    a[0].forEach(function (v) { p.guntag = p.guntag.filter(function (x) { return x !== v; }); if (p.gtag.indexOf(v) < 0) p.gtag.push(v); }); }); }, 'Передавать VLAN с тегом');
  cmd(['8'], 'if range', 'vlan pvid <n>', function (st, a) { if (!st.vlans[a[0]]) return '% VLAN ' + a[0] + ' не создана';
    ports(st).forEach(function (p) { p.mode = 'general'; p.pvid = a[0]; }); }, 'VLAN для кадров без тега');
  cmd(['8'], 'config', 'spanning-tree mst priority <n> <n>', function (st, a) { if (a[1] > 61440 || a[1] % 4096) return '% Приоритет 0–61440, кратный 4096';
    stp(st).prio = a[1]; }, 'Приоритет моста (экземпляр 0 — CST)');
  cmd(['8'], 'config', 'monitor session <n> mode', function (st, a) { var m = (st.mon = st.mon || {}); m[a[0]] = m[a[0]] || { src: {} }; m[a[0]].on = true; }, 'Включить сессию зеркалирования');
  cmd(['8'], 'config', 'no monitor session <n> mode', function (st, a) { var m = (st.mon || {})[a[0]]; if (m) m.on = false; });
  cmd(['8'], 'priv', 'copy system:running-config nvram:startup-config', function (st) { return EL.mes.save(st); }, 'Сохранить конфигурацию');
  ['', 'do '].forEach(function (pre) {
    cmd(['8'], pre ? E.CFG : 'priv', pre + 'show port-channel brief', function (st) { return st.net ? st.net.lagText(st.dev) : ''; });
    cmd(['8'], pre ? E.CFG : 'priv', pre + 'show vlan brief', function (st) { return E.showVlan(st); });
  });

  function showVlan8(st) {
    return ['VLAN ID VLAN Name                        VLAN Type', '------- -------------------------------- ---------']
      .concat(Object.keys(st.vlans).map(Number).sort(function (x, y) { return x - y; }).map(function (v) {
        var nm = v === 1 ? 'default' : (st.vlans[v] === '-' ? 'VLAN' + ('000' + v).slice(-4) : st.vlans[v]);
        return (v + '        ').slice(0, 8) + (nm + '                                 ').slice(0, 33) + (v === 1 ? 'Default' : 'Static'); })).join('\n');
  }
  ['', 'do '].forEach(function (pre) { cmd(['8'], pre ? E.CFG : 'priv', pre + 'show vlan', function (st) { return showVlan8(st); }); });

  // ---------------------------------------------------------------- приглашения
  var P8 = { user: ' >', priv: ' #', config: ' (Config)#', vlan: ' (Vlan)#', line: ' (Config-line)#' };
  var base = EL.mes.prompt;
  EL.mes.prompt = function (st) {
    if (st.dialect !== '8') return base(st);
    if (st.mode === 'if' || st.mode === 'range') {
      var c = st.ctx || {}, n = c.svi ? 'vlan ' + c.svi : c.lag ? 'lag ' + c.lag : c.ports.length > 1 ? c.ports[0] + '-' + c.ports[c.ports.length - 1] : c.ports[0];
      return '(' + st.host + ') (Interface ' + n + ')#';
    }
    return '(' + st.host + ')' + (P8[st.mode] || '#');
  };
})(typeof window !== 'undefined' ? window : global);
