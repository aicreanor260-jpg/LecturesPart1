/* VoIP: абонентский шлюз TAU-72.IP (руководство 2.23.8), цифровой шлюз SMG-1016M с SIP-регистратором (руководство 3.411.0) и аналоговый телефон —
   один сценарий: телефоны на портах FXS TAU регистрируются на SMG и звонят друг другу.
   TAU (вход admin / rootpasswd): tau-72# → config → tau-72(config)#: network → (config-net)#: ipaddr, netmask, gateway;
     sip profile N → (config-sip-profile)#: proxy address 1 A, regristrar address 1 A, regristrar enable 1 (так в прошивке), domain;
     voice port N → (config-voice-port)#: username, authname, password, displayname, profile sip N, disable / no disable; commit, confirm; show voiceport status;
     show configuration candidate | running.
   SMG (вход admin / rootpasswd): SMG> config → SMG-[CONFIG]>: network → SMG-[CONFIG]-NETWORK>: set interface ipaddr 0 A, set interface netmask 0 M, set gateway A;
     sip users → SMG-[CONFIG]-SIP-USERS>: add user N, set user number N НОМЕР, set login N ЛОГИН ПАРОЛЬ, set authorization N none|register|register_and_invite,
     show user N, show list; save. Изменения действуют сразу, save — в энергонезависимую память.
   Телефон (консоль трубки): dial НОМЕР — снять трубку и набрать, hangup — положить; входящий вызов — звонок, трубка снимается автоматически.
   Регистрация: TAU шлёт REGISTER на UDP 5060 регистратора; SMG принимает номер из своей базы (с проверкой логина и пароля, если authorization не none).
   Вызов: INVITE на SMG → поиск зарегистрированного номера → INVITE на TAU вызываемого → звонок → 200 OK → речь RTP напрямую TAU ↔ TAU.
   Упрощения: на TAU порты FXS 1–8 (у TAU-72 их 72), Ethernet-порт — eth0; кодеки, DTMF, ДВО, план нумерации, транки SMG и E1 не моделируются. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, IP = EL.ip;
  function isT(d) { return !!d && d.sub === 'tau'; }
  function isS(d) { return !!d && d.sub === 'smg'; }
  function isPh(d) { return !!d && d.sub === 'phone'; }
  EL.CABLES.rj11 = 'Телефонный кабель (RJ-11)';
  var dc0 = P.defaultCable;
  P.defaultCable = function (a, ap, b, bp) { return /^fxs \d+$|^Line$/.test(ap) || /^fxs \d+$|^Line$/.test(bp) ? 'rj11' : dc0.apply(this, arguments); };
  var add0 = P.add;
  P.add = function (model) {
    var d = add0.apply(this, arguments), m = EL.MODELS[model] || {}, st = d.st;
    if (m.kind === 'tau') { d.sub = 'tau'; st.ip = '192.168.1.2'; st.len = 24; st.gw = null; var c = { net: { ip: '192.168.1.2', mask: '255.255.255.0', gw: '' }, sip: { 1: {} }, ports: {} };
      st.voip = { kind: 'tau', host: m.host || 'tau-72', mode: 'login', ctx: null, user: null, cand: c, run: EL.clone(c), nv: EL.clone(c) }; }
    if (m.kind === 'smg') { d.sub = 'smg'; st.ip = '192.168.1.2'; st.len = 24; st.gw = null;
      st.voip = { kind: 'smg', mode: 'login', ctx: null, user: null, cfg: { net: { ip: '192.168.1.2', mask: '255.255.255.0', gw: '' }, users: {} }, nv: null }; }
    if (m.kind === 'phone') { d.sub = 'phone'; st.phone = { off: true, call: null, log: [] }; }
    return d;
  };
  function apply(st, net) { var n = net; st.ip = n.ip; st.len = IP.mask2len(n.mask) || 24; st.gw = n.gw || null; }
  function fxs(st) { var net = st.net, d = net && net.devs[devOf(net, st)]; return d ? net.portsOf(d).filter(function (k) { return /^fxs /.test(k); }) : []; }
  function devOf(net, st) { return Object.keys(net.devs).filter(function (k) { return net.devs[k].st === st; })[0]; }

  // ---------------------------------------------------------------- регистрация и вызовы
  function phoneOf(net, tau, n) { var pr = net.peer(tau.id, 'fxs ' + n), d = pr && net.devs[pr.dev]; return isPh(d) && !d.off ? d : null; }
  P.voipRegs = function () {
    if (this._vr && this._vr.gen === this.gen && this._vr.now === this.now) return this._vr.t;
    var s = this, t = {}; this._vr = { gen: this.gen, now: this.now, t: t };
    this.list().filter(isT).forEach(function (d) { if (d.off) return; var c = d.st.voip.run;
      Object.keys(c.ports).forEach(function (n) { var p = c.ports[n], sp = c.sip[p.sip || 1] || {}, key = d.id + '|' + n, steps = [];
        function res(ok, why) { t[key] = { ok: ok, why: why, tau: d.id, port: +n, num: p.user, steps: steps }; }
        if (p.off) return res(false, 'порт выключен (disable)');
        if (!p.user) return res(false, 'не задан username (номер)');
        if (!sp.regOn || !sp.reg) return res(false, 'в sip profile ' + (p.sip || 1) + ' не включена регистрация (regristrar address 1 / regristrar enable 1)');
        steps.push({ k: 'route', t: d.name + ' → ' + sp.reg + ': SIP REGISTER sip:' + p.user + '@' + (sp.domain || sp.reg) + ' (UDP 5060)' });
        var r = s.request(d.id, sp.reg, 'udp', 5060); r.steps.forEach(function (x) { steps.push(x); });
        if (!r.ok) return res(false, 'регистратор ' + sp.reg + ' недоступен (' + (r.why === 'Connection refused' ? 'на UDP 5060 нет SIP' : 'нет связи') + ')');
        var sm = s.devs[r.dev]; if (!isS(sm)) return res(false, sp.reg + ' — не SIP-регистратор');
        var U = sm.st.voip.cfg.users, u = Object.keys(U).map(function (k) { return U[k]; }).filter(function (x) { return x.num === p.user; })[0];
        if (!u) { steps.push({ k: 'drop', t: sm.name + ': 404 Not Found — номера ' + p.user + ' нет в базе SIP-абонентов' }); return res(false, 'на SMG нет абонента с номером ' + p.user); }
        if (u.auth && u.auth !== 'none') { steps.push({ k: 'route', t: sm.name + ': 401 Unauthorized — запрос логина и пароля (digest)' });
          if (u.login !== (p.authname || p.user) || u.pw !== p.pw) { steps.push({ k: 'drop', t: sm.name + ': 403 Forbidden — неверный логин или пароль' }); return res(false, 'SMG отклонил: неверный authname / password'); } }
        steps.push({ k: 'ok', t: sm.name + ': 200 OK — номер ' + p.user + ' зарегистрирован' });
        t[key] = { ok: true, tau: d.id, port: +n, num: p.user, smg: sm.id, steps: steps, auth: u.auth }; }); });
    return t;
  };
  function regByNum(net, smg, num) { var t = net.voipRegs(); return Object.keys(t).map(function (k) { return t[k]; }).filter(function (r) { return r.ok && r.smg === smg && r.num === num; })[0] || null; }
  function call(net, ph, num) {
    var steps = [], pr = null, tau = null, n = null;
    net.list().filter(isT).some(function (d) { return net.portsOf(d).some(function (k) { var m = k.match(/^fxs (\d+)$/); if (!m) return false;
      var q = net.peer(d.id, k); if (q && q.dev === ph.id) { tau = d; n = +m[1]; return true; } return false; }); });
    if (!tau || tau.off) return { ok: false, msg: 'тишина — телефон не подключён к порту FXS включённого шлюза', steps: steps };
    var me = net.voipRegs()[tau.id + '|' + n];
    if (!me || !me.ok) return { ok: false, msg: 'тишина — порт ' + n + ' не зарегистрирован: ' + (me ? me.why : 'порт не настроен (voice port ' + n + ')'), steps: steps };
    steps.push({ k: 'route', t: ph.name + ': трубка снята, гудок; набран ' + num });
    var sp = tau.st.voip.run.sip[tau.st.voip.run.ports[n].sip || 1], sm = net.devs[me.smg];
    steps.push({ k: 'route', t: tau.name + ' → ' + sp.reg + ': SIP INVITE sip:' + num + '@' + (sp.domain || sp.reg) + ' от ' + me.num });
    var r1 = net.request(tau.id, sp.reg, 'udp', 5060); r1.steps.forEach(function (x) { steps.push(x); });
    if (!r1.ok) return { ok: false, msg: 'короткие гудки — нет связи с ' + sp.reg, steps: steps };
    if (me.auth === 'register_and_invite') steps.push({ k: 'route', t: sm.name + ': 401 — повторный INVITE с логином и паролем' });
    var dst = regByNum(net, sm.id, num);
    if (!dst) { steps.push({ k: 'drop', t: sm.name + ': 404 Not Found — номер ' + num + ' не зарегистрирован' }); return { ok: false, msg: 'короткие гудки (404) — номер ' + num + ' недоступен', steps: steps }; }
    var dt = net.devs[dst.tau];
    steps.push({ k: 'route', t: sm.name + ' → ' + dt.name + ': SIP INVITE на порт ' + dst.port + ' (номер ' + num + ')' });
    var r2 = net.request(sm.id, dt.st.ip, 'udp', 5060); r2.steps.forEach(function (x) { steps.push(x); });
    if (!r2.ok) return { ok: false, msg: 'короткие гудки — SMG не достучался до ' + dt.name, steps: steps };
    var to = phoneOf(net, dt, dst.port);
    if (!to) { steps.push({ k: 'drop', t: dt.name + ': на порту FXS ' + dst.port + ' нет телефона — 480 Temporarily Unavailable' }); return { ok: false, msg: 'короткие гудки — абонент недоступен', steps: steps }; }
    if (to.st.phone.call) { steps.push({ k: 'drop', t: dt.name + ': 486 Busy Here' }); return { ok: false, msg: 'занято (486 Busy Here)', steps: steps }; }
    if (to === ph) return { ok: false, msg: 'занято — вы звоните себе', steps: steps };
    steps.push({ k: 'route', t: dt.name + ': 180 Ringing — звонит ' + to.name + '; трубка снята → 200 OK → ACK' });
    var r3 = net.request(tau.id, dt.st.ip, 'udp', 5004); r3.steps.forEach(function (x) { steps.push(x); });
    if (!r3.ok) { steps.push({ k: 'drop', t: 'RTP ' + tau.name + ' ↔ ' + dt.name + ' не проходит — разговор без звука' }); return { ok: false, msg: 'соединились, но не слышно друг друга — нет прямой связи RTP между шлюзами', steps: steps, to: to }; }
    steps.push({ k: 'ok', t: 'RTP ' + tau.st.ip + ' ↔ ' + dt.st.ip + ' — разговор установлен' });
    return { ok: true, msg: 'разговор с ' + num + ' (' + to.name + ')', steps: steps, to: to, from: me.num };
  }
  EL.listensX = (function (lx0) { return function (d, proto, port) {
    if (proto === 'udp' && (port === 5060 || port === 5004) && (d.sub === 'smg' || d.sub === 'tau')) return port === 5060 || d.sub === 'tau';
    return lx0 ? lx0(d, proto, port) : undefined; }; })(EL.listensX);

  // ---------------------------------------------------------------- CLI TAU и SMG
  function login(st, line, host) { var v = st.voip, l = String(line).trim();
    if (v.mode === 'login') { v.user = l; v.mode = 'pw'; return ''; }
    if (v.mode === 'pw') { var ok = v.user === 'admin' && l === 'rootpasswd'; v.mode = ok ? 'root' : 'login'; return ok ? '' : 'Login incorrect'; }
    return null; }
  var ERR = 'Unknown command';
  function tauExec(st, raw) {
    var v = st.voip, c = v.cand, l = String(raw).trim(), w = l.split(/\s+/), lo = l.toLowerCase(), m, r = login(st, l); if (r !== null) return r;
    if (!l) return '';
    if (/^(exit|quit)$/.test(lo)) { v.mode = v.mode === 'root' ? 'login' : v.mode === 'config' ? 'root' : 'config'; v.ctx = null; return ''; }
    if (/^end$/.test(lo)) { v.mode = 'root'; v.ctx = null; return ''; }
    var dm = lo.match(/^do (.+)$/); if (dm) { var md = v.mode; v.mode = 'root'; var rr = tauExec(st, l.slice(3)); v.mode = md; return rr; }
    if (v.mode === 'root') {
      if (/^conf(ig(ure)?)?$/.test(lo)) { v.mode = 'config'; return ''; }
      if (lo === 'commit') { v.run = EL.clone(c); apply(st, v.run.net); if (st.net) st.net.gen++; return 'Configuration committed. Confirm it within 600 seconds (confirm)'; }
      if (lo === 'confirm') { v.nv = EL.clone(v.run); return 'Configuration confirmed'; }
      if (lo === 'rollback') { v.cand = EL.clone(v.run); return ''; }
      if (/^show configuration (candidate|running)$/.test(lo)) return cfgText(lo.split(' ')[2] === 'running' ? v.run : c);
      if ((m = lo.match(/^show voiceport status( (\d+))?$/))) return vpStatus(st, m[2]);
      if (lo === 'show ipaddr' || lo === 'show network') return 'IP address: ' + v.run.net.ip + '\nNetmask: ' + v.run.net.mask + '\nGateway: ' + (v.run.net.gw || '-');
      return ERR; }
    if (v.mode === 'config') {
      if (lo === 'network') { v.mode = 'net'; return ''; }
      if ((m = lo.match(/^sip profile (\d+)$/))) { if (+m[1] < 1 || +m[1] > 8) return ERR; c.sip[m[1]] = c.sip[m[1]] || {}; v.mode = 'sipp'; v.ctx = m[1]; return ''; }
      if ((m = lo.match(/^voice port (\d+)$/))) { if (+m[1] < 1 || fxs(st).indexOf('fxs ' + m[1]) < 0) return 'Wrong port number (1-' + fxs(st).length + ')';
        c.ports[m[1]] = c.ports[m[1]] || { sip: 1 }; v.mode = 'vp'; v.ctx = m[1]; return ''; }
      return ERR; }
    if (v.mode === 'net') {
      if ((m = l.match(/^ipaddr (\d+\.\d+\.\d+\.\d+)$/))) { c.net.ip = m[1]; return ''; }
      if ((m = l.match(/^netmask (\d+\.\d+\.\d+\.\d+)$/))) { if (IP.mask2len(m[1]) === null) return ERR; c.net.mask = m[1]; return ''; }
      if ((m = l.match(/^gateway (\d+\.\d+\.\d+\.\d+)$/))) { c.net.gw = m[1]; return ''; }
      return ERR; }
    if (v.mode === 'sipp') { var s = c.sip[v.ctx];
      if ((m = l.match(/^proxy address 1 (\S+)$/))) { s.proxy = m[1].replace(/:\d+$/, ''); return ''; }
      if ((m = l.match(/^regristrar address 1 (\S+)$/))) { s.reg = m[1].replace(/:\d+$/, ''); return ''; }
      if (lo === 'regristrar enable 1') { s.regOn = true; return ''; }
      if (lo === 'no regristrar enable 1') { s.regOn = false; return ''; }
      if ((m = l.match(/^domain (\S+)$/))) { s.domain = m[1]; return ''; }
      if (/^(proxy mode|expires|auth mode|codec|dtmfmode|regristrar interval)\b/.test(lo)) return '';
      return ERR; }
    if (v.mode === 'vp') { var p = c.ports[v.ctx];
      if ((m = l.match(/^username (\S+)$/))) { p.user = m[1]; return ''; }
      if ((m = l.match(/^authname (\S+)$/))) { p.authname = m[1]; return ''; }
      if ((m = l.match(/^password (\S+)$/))) { p.pw = m[1]; return ''; }
      if ((m = l.match(/^displayname (.+)$/))) { p.disp = m[1]; return ''; }
      if ((m = lo.match(/^profile sip (\d+)$/))) { p.sip = +m[1]; return ''; }
      if (lo === 'disable') { p.off = true; return ''; } if (lo === 'no disable') { p.off = false; return ''; }
      if (/^(profile voice|callerid|flash|hybrid|custom|pgs_avs)\b/.test(lo)) return '';
      return ERR; }
    return ERR;
  }
  function cfgText(c) { var o = ['network', '  ipaddr ' + c.net.ip, '  netmask ' + c.net.mask]; if (c.net.gw) o.push('  gateway ' + c.net.gw); o.push('exit');
    Object.keys(c.sip).forEach(function (k) { var s = c.sip[k]; if (!s.reg && !s.proxy && !s.domain) return; o.push('sip profile ' + k); if (s.proxy) o.push('  proxy address 1 ' + s.proxy);
      if (s.reg) o.push('  regristrar address 1 ' + s.reg); if (s.regOn) o.push('  regristrar enable 1'); if (s.domain) o.push('  domain ' + s.domain); o.push('exit'); });
    Object.keys(c.ports).sort(function (a, b) { return a - b; }).forEach(function (k) { var p = c.ports[k]; o.push('voice port ' + k); if (p.user) o.push('  username ' + p.user);
      if (p.authname) o.push('  authname ' + p.authname); if (p.pw) o.push('  password ' + p.pw); if (p.sip && p.sip !== 1) o.push('  profile sip ' + p.sip); if (p.off) o.push('  disable'); o.push('exit'); });
    return o.join('\n'); }
  function vpStatus(st, one) { var net = st.net; if (!net) return ''; var id = devOf(net, st), t = net.voipRegs(), o = ['Port  Number          Registration     Line'];
    fxs(st).forEach(function (k) { var n = k.split(' ')[1]; if (one && one !== n) return;
      var r = t[id + '|' + n], ph = phoneOf(net, net.devs[id], n), call = ph && ph.st.phone.call;
      o.push((n + '     ').slice(0, 6) + ((r && r.num || '-') + '                ').slice(0, 16) + ((r ? (r.ok ? 'registered' : 'not registered') : 'not configured') + '                 ').slice(0, 17) +
        (!ph ? 'no phone' : call ? 'talk' : 'onhook')); });
    return o.join('\n'); }
  function smgExec(st, raw) {
    var v = st.voip, c = v.cfg, l = String(raw).trim(), lo = l.toLowerCase(), m, r = login(st, l); if (r !== null) return r;
    if (!l) return '';
    if (/^(exit|quit)$/.test(lo)) { v.mode = { root: 'login', config: 'root', net: 'config', users: 'config' }[v.mode]; return ''; }
    if (v.mode === 'root') { if (lo === 'config') { v.mode = 'config'; return 'Entering configuration mode.'; } if (lo === 'sh') return ''; return ERR; }
    if (v.mode === 'config') {
      if (lo === 'network') { v.mode = 'net'; return 'Entering Network mode.'; }
      if (lo === 'sip users') { v.mode = 'users'; return 'Entering SIP-Users mode.'; }
      if (lo === 'save') { v.nv = EL.clone(c); return 'Configuration saved.'; }
      return ERR; }
    if (v.mode === 'net') {
      if ((m = l.match(/^set interface ipaddr 0 (\d+\.\d+\.\d+\.\d+)$/))) { c.net.ip = m[1]; apply(st, c.net); if (st.net) st.net.gen++; return ''; }
      if ((m = l.match(/^set interface netmask 0 (\d+\.\d+\.\d+\.\d+)$/))) { if (IP.mask2len(m[1]) === null) return ERR; c.net.mask = m[1]; apply(st, c.net); if (st.net) st.net.gen++; return ''; }
      if ((m = l.match(/^set gateway (\d+\.\d+\.\d+\.\d+)$/))) { c.net.gw = m[1]; apply(st, c.net); if (st.net) st.net.gen++; return ''; }
      if (/^show (interface|net-interfaces)/.test(lo)) return 'Interface 0: ' + c.net.ip + ' / ' + c.net.mask + (c.net.gw ? ', gateway ' + c.net.gw : '');
      return ERR; }
    if (v.mode === 'users') { var U = c.users, gen = function () { if (st.net) st.net.gen++; return ''; };
      if ((m = lo.match(/^add user (\d+)$/))) { if (+m[1] > 1999) return ERR; if (U[m[1]]) return 'User ' + m[1] + ' already exists'; U[m[1]] = { auth: 'none' }; return gen(); }
      if ((m = lo.match(/^remove user (\d+)$/))) { delete U[m[1]]; return gen(); }
      if ((m = l.match(/^set user number (\d+) (\S+)$/))) { if (!U[m[1]]) return 'User ' + m[1] + ' not found'; U[m[1]].num = m[2]; return gen(); }
      if ((m = l.match(/^set login (\d+) (\S+) (\S+)$/))) { if (!U[m[1]]) return 'User ' + m[1] + ' not found'; U[m[1]].login = m[2]; U[m[1]].pw = m[3]; return gen(); }
      if ((m = lo.match(/^set authorization (\d+) (none|register|register_and_invite)$/))) { if (!U[m[1]]) return 'User ' + m[1] + ' not found'; U[m[1]].auth = m[2]; return gen(); }
      if ((m = lo.match(/^show user (\d+)$/))) { var u = U[m[1]]; if (!u) return 'User ' + m[1] + ' not found';
        return ['User ' + m[1] + ':', 'Number: ' + (u.num || '-'), 'Login: ' + (u.login || '-'), 'Authorization: ' + u.auth, 'Registration: ' + (regNum(st, u.num) ? 'registered (' + regNum(st, u.num) + ')' : 'not registered')].join('\n'); }
      if (lo === 'show list') return ['ID    Number          Authorization        Registration'].concat(Object.keys(U).map(function (k) { var u = U[k];
        return (k + '      ').slice(0, 6) + ((u.num || '-') + '                ').slice(0, 16) + (u.auth + '                     ').slice(0, 21) + (regNum(st, u.num) ? 'registered ' + regNum(st, u.num) : '-'); })).join('\n');
      return ERR; }
    return ERR;
  }
  function regNum(st, num) { var net = st.net; if (!net || !num) return null; var r = regByNum(net, devOf(net, st), num); return r ? net.devs[r.tau].st.ip + ' port ' + r.port : null; }
  function phoneExec(net, d, raw) { var ph = d.st.phone, l = String(raw).trim(), m;
    if (!l) return '';
    if ((m = l.match(/^(?:dial\s+)?(\d{2,15})$/i))) { if (ph.call) return 'Сначала положите трубку (hangup)';
      var r = call(net, d, m[1]); if (net.onTrace) net.onTrace({ ok: r.ok, steps: r.steps }, d.id, 'SIP ' + m[1]);
      if (r.ok) { ph.call = m[1]; r.to.st.phone.call = r.from; r.to.st.phone.log.push('Звонок от ' + r.from + ' — трубка снята, идёт разговор'); net.gen++; }
      return r.msg; }
    if (/^hangup$/i.test(l)) { if (!ph.call) return 'Трубка уже положена'; var other = net.list().filter(function (x) { return isPh(x) && x !== d && x.st.phone.call; });
      other.forEach(function (x) { x.st.phone.call = null; x.st.phone.log.push('Собеседник положил трубку — отбой'); }); ph.call = null; net.gen++; return 'Трубка положена'; }
    if (/^status$/i.test(l)) return ph.call ? 'Разговор: ' + ph.call : 'Трубка положена' + (ph.log.length ? '\n' + ph.log.slice(-3).join('\n') : '');
    if (/^(help|\?)$/.test(l)) return 'dial НОМЕР (или просто номер) — набрать; hangup — положить трубку; status — состояние';
    return 'dial НОМЕР — набрать номер; hangup — положить трубку';
  }
  var ex0 = P.exec;
  P.exec = function (id, line) { var d = this.devs[id];
    if (isT(d) || isS(d)) { this.gen++; if (d.off) return ''; return isT(d) ? tauExec(d.st, line) : smgExec(d.st, line); }
    if (isPh(d)) { if (d.off) return ''; var out = phoneExec(this, d, line), lg = d.st.phone.log.splice(0); return lg.concat(out ? [out] : []).join('\n'); }
    return ex0.apply(this, arguments); };
  var pr0 = P.prompt;
  P.prompt = function (id) { var d = this.devs[id];
    if (isT(d) || isS(d)) { var v = d.st.voip; if (v.mode === 'login') return (isT(d) ? v.host : 'smg') + ' login: '; if (v.mode === 'pw') return 'Password: ';
      if (isT(d)) return v.host + ({ root: '#', config: '(config)#', net: '(config-net)#', sipp: '(config-sip-profile)#', vp: '(config-voice-port)#' }[v.mode]);
      return { root: 'SMG> ', config: 'SMG-[CONFIG]> ', net: 'SMG-[CONFIG]-NETWORK> ', users: 'SMG-[CONFIG]-SIP-USERS> ' }[v.mode]; }
    if (isPh(d)) return d.st.phone.call ? 'Телефон (разговор: ' + d.st.phone.call + ')> ' : 'Телефон> ';
    return pr0.apply(this, arguments); };
  // reload: TAU — подтверждённая конфигурация, SMG — сохранённая (save)
  var boot0 = P.reboot;
  if (boot0) P.reboot = function (id) { var d = this.devs[id], keep = d && d.st.voip; var r = boot0.apply(this, arguments); d = this.devs[id];
    if (keep && (isT(d) || isS(d))) { if (isT(d)) { keep.run = EL.clone(keep.nv); keep.cand = EL.clone(keep.nv); apply(d.st, keep.run.net); }
      else if (keep.nv) { keep.cfg = EL.clone(keep.nv); apply(d.st, keep.cfg.net); } keep.mode = 'login'; d.st.voip = keep; } this.gen++; return r; };
  EL.voip = { call: call };
})(typeof window !== 'undefined' ? window : global);
