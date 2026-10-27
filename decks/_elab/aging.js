/* Старение записей MAC и ARP по модельному времени сети (net.now, секунды).
   Таймеры по умолчанию — из руководств Eltex:
     MES 10.x  mac-address-table aging-time 10..400 (300),  arp timeout 30..86400 (60000);
     MES 6.x/4.x mac address-table aging-time 10..400 (300), arp timeout 1..40000000 (60000);
     MES 8.x   bridge aging-time 10..1000000 (300),        arp timeout 15..21600 (1200);
     ESR       ip arp reachable-time 5000..100000000 мс на интерфейсе (160000);
     VPC — 120 с, Debian — REACHABLE 30 с, затем STALE, удаление через 60 с. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, S = EL.esr, P = EL.Net.prototype, CMDS = E.CMDS;

  var MAC_AGE = 300, ARP_MES = { '10': 60000, '6': 60000, '8': 1200 }, ARP_ESR_MS = 160000, ARP_VPC = 120, ARP_DEB = 60, DEB_REACH = 30;

  P.macAge = function (id) { var d = this.devs[id]; return d.st.macAge || MAC_AGE; };
  P.arpAge = function (id, ifn) {
    var d = this.devs[id], st = d.st;
    if (d.type === 'mes') return st.arpTo || ARP_MES[st.dialect] || 60000;
    if (d.type === 'esr') { var x = ifn && st.run.ifs[ifn]; return Math.round(((x && x.arpRt) || ARP_ESR_MS) / 1000); }
    return d.type === 'vpc' ? ARP_VPC : ARP_DEB;
  };
  // сколько секунд записи осталось жить
  P.ttl = function (id, kind, e) {
    var age = kind === 'a' ? this.arpAge(id, e.ifn) : this.macAge(id);
    return Math.max(0, Math.ceil(age - (this.now - (e.t === undefined ? this.now : e.t))));
  };
  // состояние записи соседа в Linux: свежая — REACHABLE, старше 30 с — STALE
  P.neighState = function (id, e) { return this.now - (e.t || 0) < DEB_REACH ? 'REACHABLE' : 'STALE'; };

  // ход часов: удаляет истёкшие записи, возвращает список удалённых
  P.tick = function (dt) {
    var s = this, gone = [];
    s.now += dt;
    s.order.forEach(function (id) {
      var d = s.devs[id], a = s.arp[id] || {}, m = s.mac[id] || {};
      Object.keys(a).forEach(function (k) { if (s.ttl(id, 'a', a[k]) <= 0) { gone.push({ dev: d.name, kind: 'ARP', what: k + ' → ' + a[k].mac }); delete a[k]; } });
      Object.keys(m).forEach(function (k) { if (s.ttl(id, 'm', m[k]) <= 0) { gone.push({ dev: d.name, kind: 'MAC', what: m[k].mac + ' (VLAN ' + m[k].vlan + ', ' + m[k].port + ')' }); delete m[k]; } });
    });
    return gone;
  };
  P.clockText = function () {
    var t = Math.floor(this.now), p = function (n) { return ('0' + n).slice(-2); };
    return p(Math.floor(t / 3600)) + ':' + p(Math.floor(t / 60) % 60) + ':' + p(t % 60);
  };

  // ---------------------------------------------------------------- команды MES
  function cmd(dl, modes, pat, run, d) { var n = CMDS.length; E.cmd(modes, pat, run); var c = CMDS.splice(n, 1)[0]; c.dl = dl; if (d) c.d = d; CMDS.unshift(c); return c; }
  function num(v, lo, hi, set) { var n = +v; if (!/^\d+$/.test(v) || n < lo || n > hi) return '% Допустимо ' + lo + '..' + hi; set(n); }
  cmd(['10'], 'config', 'mac-address-table aging-time <w>', function (st, a) { return num(a[0], 10, 400, function (n) { st.macAge = n; }); }, 'Время жизни MAC-записей, с');
  cmd(['10'], 'config', 'no mac-address-table aging-time', function (st) { delete st.macAge; });
  cmd(['6'], 'config', 'mac address-table aging-time <w>', function (st, a) { return num(a[0], 10, 400, function (n) { st.macAge = n; }); }, 'Время жизни MAC-записей, с');
  cmd(['6'], 'config', 'no mac address-table aging-time', function (st) { delete st.macAge; });
  cmd(['8'], 'config', 'bridge aging-time <w>', function (st, a) { return num(a[0], 10, 1000000, function (n) { st.macAge = n; }); }, 'Время жизни MAC-записей, с');
  cmd(['8'], 'config', 'no bridge aging-time', function (st) { delete st.macAge; });
  var ARP_RNG = { '10': [30, 86400], '6': [1, 40000000], '8': [15, 21600] };
  cmd(['10', '6', '8'], 'config', 'arp timeout <w>', function (st, a) { var r = ARP_RNG[st.dialect] || ARP_RNG['10'];
    return num(a[0], r[0], r[1], function (n) { st.arpTo = n; }); }, 'Время жизни ARP-записей, с');
  cmd(['10', '6', '8'], 'config', 'no arp timeout', function (st) { delete st.arpTo; });
  function agingShow(st) { return 'Aging time is ' + (st.macAge || MAC_AGE) + ' sec'; }
  ['', 'do '].forEach(function (pre) {
    var m = pre ? E.CFG : 'priv';
    cmd(['10'], m, pre + 'show mac-address-table aging-time', agingShow);
    cmd(['10', '6'], m, pre + 'show mac address-table aging-time', agingShow);
    cmd(['8'], m, pre + 'show forwardingdb agetime', function (st) { return 'Address Aging Timeout: ' + (st.macAge || MAC_AGE); });
  });
  E.RUNX.push(function (st, o) {
    if (st.macAge) o.push(st.dialect === '8' ? 'bridge aging-time ' + st.macAge : st.dialect === '6' ? 'mac address-table aging-time ' + st.macAge : 'mac-address-table aging-time ' + st.macAge);
    if (st.arpTo) o.push('arp timeout ' + st.arpTo);
  });

  // ---------------------------------------------------------------- команды ESR (на интерфейсе, через commit)
  function ifs(st) { return (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).map(function (k) { return st.cand.ifs[k]; }).filter(Boolean); }
  S.cmd('gi sub bridge', 'ip arp reachable-time <w>', function (st, a) {
    return num(a[0], 5000, 100000000, function (n) { ifs(st).forEach(function (x) { x.arpRt = n; }); st.pending = true; }); }, 'Время жизни ARP-записей, мс');
  S.cmd('gi sub bridge', 'no ip arp reachable-time', function (st) { ifs(st).forEach(function (x) { delete x.arpRt; }); st.pending = true; });
  S.RUNX.push(function (c, o) {
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k]; if (x.arpRt) o.push('interface ' + S.longIf(k), '  ip arp reachable-time ' + x.arpRt, 'exit'); });
  });
})(typeof window !== 'undefined' ? window : global);
