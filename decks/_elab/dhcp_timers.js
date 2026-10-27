/* DHCP-аренда по модельному времени (net.now): сервер ESR и клиенты VPC / Debian.
   Длительность — default-lease-time пула (DD:HH:MM), по умолчанию 12 часов (справочник CLI ESR).
   Клиент (RFC 2131): T1 = ½ аренды — DHCPREQUEST серверу unicast (продление);
     не вышло — T2 = ⅞ аренды — DHCPREQUEST широковещательно (rebind, любой сервер, в т.ч. через relay);
     аренда истекла — адрес снимается. Debian (dhclient) после неудачи повторяет DISCOVER через 300 с (retry по умолчанию).
   Сервер: запись show ip dhcp binding живёт до конца аренды и освобождается, если клиент не продлил.
   Упрощения: клиент не просит своё время аренды (берётся default-lease-time); max-lease-time не моделируется;
   VPC при clear ip не шлёт DHCPRELEASE — запись на сервере доживает до конца аренды. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, P = EL.Net.prototype, S = EL.esr;
  var DEF = 12 * 3600, RETRY = 300;

  function dur(pool) { var m = pool && pool.lease && String(pool.lease).match(/^(\d+):(\d+):(\d+)$/);
    return m ? Math.max(60, ((+m[1] * 24 + +m[2]) * 60 + +m[3]) * 60) : DEF; }
  function srvT(st) { return st.leaseT || (st.leaseT = {}); }

  // каждая выдача/продление — запись времени у сервера и у клиента
  var dhcp0 = P.dhcp;
  P.dhcp = function (id) {
    var r = dhcp0.apply(this, arguments), d = this.devs[id];
    if (!r.ok) return r;
    var sd = this.byName(r.server), D = dur(r.pool);
    if (sd) srvT(sd.st)[d.name] = { t0: this.now, dur: D };
    d.st.dl = { srv: sd ? sd.id : null, sip: r.sip || null, ip: r.ip, t0: this.now, dur: D };
    return r;
  };
  P.leaseLeft = function (srvId, cname) { var e = srvT(this.devs[srvId].st)[cname]; return e ? Math.max(0, e.t0 + e.dur - this.now) : null; };

  // ESR с ip dhcp-server принимает DHCPREQUEST на UDP 67 (продление unicast)
  var lx0 = EL.listensX;
  EL.listensX = function (d, proto, port) {
    if (d.type === 'esr' && proto === 'udp' && port === 67 && d.st.run.dhcp && d.st.run.dhcp.on) return true;
    return lx0 ? lx0(d, proto, port) : undefined;
  };

  // ближайшее событие таймеров DHCP не позже end
  function due(s, end) {
    var best = null;
    function at(t, f) { if (t <= end && (!best || t < best.t)) best = { t: t, f: f }; }
    s.order.forEach(function (id) {
      var d = s.devs[id], st = d.st; if (!st) return;
      if (d.type === 'esr') Object.keys(st.leaseT || {}).forEach(function (c) { var e = st.leaseT[c]; at(e.t0 + e.dur, function () { expireSrv(s, d, c); }); });
      var L = st.dl; if (!L || d.off) return;
      if (L.retry !== undefined) { at(L.retry, function () { rediscover(s, d); }); return; }
      if (st.ip !== L.ip) { delete st.dl; return; }                         // адрес сменили вручную — аренда не ведётся
      var t1 = L.t0 + L.dur / 2, t2 = L.t0 + L.dur * 7 / 8, ex = L.t0 + L.dur;
      if (!L.t1done) at(t1, function () { renew(s, d); });
      else if (!L.t2done) at(t2, function () { rebind(s, d); });
      else at(ex, function () { expireCli(s, d); });
    });
    return best;
  }
  function expireSrv(s, d, c) {
    var e = d.st.leaseT[c]; delete d.st.leaseT[c];
    if (d.st.leases && d.st.leases[c]) { s._dhcpGone.push({ dev: d.name, kind: 'DHCP', what: 'аренда ' + d.st.leases[c] + ' (' + c + ') истекла' }); delete d.st.leases[c]; }
    void e;
  }
  function bind(s, d, r) { var st = d.st; st.ip = r.ip; st.len = r.len; st.gw = r.gw || null; if (d.type === 'deb') st.up = true; }
  function renew(s, d) {                         // T1: unicast серверу, выдавшему адрес
    var st = d.st, L = st.dl; L.t1done = true;
    var sd = L.srv && s.devs[L.srv]; if (!sd || sd.off || !L.sip) return;
    var c = sd.st.run.dhcp, ok = c && c.on && Object.keys(c.pools).some(function (k) { var p = c.pools[k];
      return p.net && IP.sameNet(L.ip, p.net.split('/')[0], +p.net.split('/')[1]); });
    if (!ok || !s.request(d.id, L.sip, 'udp', 67).ok) return;
    var p = Object.keys(c.pools).map(function (k) { return c.pools[k]; }).filter(function (p) { return p.net && IP.sameNet(L.ip, p.net.split('/')[0], +p.net.split('/')[1]); })[0];
    var D = dur(p); srvT(sd.st)[d.name] = { t0: s.now, dur: D }; (sd.st.leases = sd.st.leases || {})[d.name] = L.ip;
    st.dl = { srv: L.srv, sip: L.sip, ip: L.ip, t0: s.now, dur: D };
  }
  function rebind(s, d) {                        // T2: широковещательно, ответит любой сервер
    var L = d.st.dl; L.t2done = true;
    var r = s.dhcp(d.id); if (r.ok) bind(s, d, r); else d.st.dl = L;   // неудача: ждём конца аренды
  }
  function expireCli(s, d) {
    var st = d.st; s._dhcpGone.push({ dev: d.name, kind: 'DHCP', what: 'аренда ' + st.ip + ' истекла — адрес снят' });
    st.ip = null; st.gw = null; delete st.dl;
    if (d.type === 'deb') st.dl = { retry: s.now + RETRY };
  }
  function rediscover(s, d) {
    var r = s.dhcp(d.id); if (r.ok) bind(s, d, r); else d.st.dl = { retry: s.now + RETRY };
  }

  var tick0 = P.tick;
  P.tick = function (dt) {                       // часы идут до очередного события аренды, затем дальше
    var s = this, end = this.now + dt, gone = []; s._dhcpGone = [];
    for (var guard = 0; guard < 10000; guard++) {
      var e = due(s, end); if (!e) break;
      gone = gone.concat(tick0.call(this, Math.max(0, e.t - this.now))); e.f();
    }
    gone = gone.concat(tick0.call(this, end - this.now), s._dhcpGone); s._dhcpGone = [];
    return gone;
  };

  // Debian: dhclient без ответа повторяет DISCOVER через 300 с
  var deb0 = EL.hosts.debExec;
  EL.hosts.debExec = function (st, raw) {
    var out = deb0.apply(this, arguments);
    if (st.net && /No DHCPOFFERS received/.test(out || '')) st.dl = { retry: st.net.now + RETRY };
    return out;
  };

  // ESR: show ip dhcp binding — время окончания аренды по часам устройства (формат справочника 1.23)
  function pad(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  var DAY = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  function when(st, sec) { var t = new Date(EL.clock.now() + (st.clk || 0) + sec * 1000), p = function (n) { return ('0' + n).slice(-2); };
    return DAY[t.getUTCDay()] + ' ' + t.getUTCFullYear() + '/' + p(t.getUTCMonth() + 1) + '/' + p(t.getUTCDate()) + ' ' + p(t.getUTCHours()) + ':' + p(t.getUTCMinutes()) + ':' + p(t.getUTCSeconds()); }
  function binding(st, only) {
    var L = st.leases || {}, s = st.net, ks = Object.keys(L).filter(function (k) { return !only || L[k] === only; });
    var o = [pad('IP address', 18) + pad('MAC / Client ID', 62) + pad('Lease expires at', 31) + 'Binding type',
      '----------------- ------------------------------------------------------------- ------------------------------ ------------'];
    ks.forEach(function (k) { var left = s ? s.leaseLeft(st.dev, k) : null;
      o.push(pad(L[k], 18) + pad(EL.mac(k + (s && s.byName(k) && s.byName(k).type === 'deb' ? (s.byName(k).st.port || 'ens3') : 'eth0')), 62) +
        pad(left === null ? '-' : when(st, left), 31) + 'active'); });
    return o.join('\n');
  }
  function scmd(modes, pat, fn, d) { S.cmd(modes, pat, fn, d); var c = S.T.pop(); S.T.unshift(c); return c; }
  scmd('priv', 'show ip dhcp binding', function (st) { return binding(st); }, 'Выданные адреса DHCP и окончание аренды');
  scmd('priv', 'show ip dhcp binding <ip>', function (st, a) { return binding(st, a[0]); });
  scmd('priv', 'clear ip dhcp binding', function (st) { st.leases = {}; st.leaseT = {}; return ''; }, 'Освободить все выданные адреса');
  scmd('priv', 'clear ip dhcp binding <ip>', function (st, a) { var L = st.leases || {};
    Object.keys(L).forEach(function (k) { if (L[k] === a[0]) { delete L[k]; delete srvT(st)[k]; } }); return ''; });

  // VPC: show ip — DHCP SERVER / DHCP LEASE: осталось, аренда/T1/T2 (как VPCS)
  var vpc0 = EL.hosts.vpcExec;
  EL.hosts.vpcExec = function (st, raw) {
    var out = vpc0.apply(this, arguments), L = st.dl;
    if (/^\s*(show|sh)(\s+ip)?\s*$/.test(String(raw)) && L && L.ip === st.ip && st.net) {
      var left = Math.max(0, Math.round(L.t0 + L.dur - st.net.now)), sd = L.srv && st.net.devs[L.srv];
      out = out.replace(/\nMAC /, '\nDHCP SERVER : ' + (L.sip || (sd ? sd.name : '-')) + '\nDHCP LEASE  : ' + left + ', ' + L.dur + '/' + Math.round(L.dur / 2) + '/' + Math.round(L.dur * 7 / 8) + '\nMAC ');
    }
    return out;
  };
  // Debian: ip a — адрес из DHCP помечен dynamic, valid_lft — остаток аренды
  EL.debLft = function (st) { var L = st.dl; if (!L || L.ip !== st.ip || !st.net) return null; return Math.max(0, Math.round(L.t0 + L.dur - st.net.now)); };
})(typeof window !== 'undefined' ? window : global);
