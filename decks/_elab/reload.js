/* Перезагрузка и таймер commit на ESR (справочник ESR-Series CLI 1.23):
   reload system — сразу; reload system in <MINUTES> | <HOUR>:<MINUTES>; reload system at <ЧЧ:ММ:СС> <день> <месяц> <год>; reload cancel;
   show system reload → «System reload is scheduled for 13:02:02 10 August 2022». Время — модельное (часы в шапке).
   commit применяет конфигурацию и запускает таймер 600 с: без confirm конфигурация возвращается к последней подтверждённой —
   по истечении таймера и при перезагрузке (как на ESR: «Commit timer started, changes will be reverted in 600 seconds»).
   MES: reload спрашивает подтверждение (руководство 6.6.8.8) — в ui.js. Текст сообщения об откате по таймеру в справочнике не приведён (условный). */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype;
  var MON = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];
  var COMMIT_TIMER = 600;
  function devNow(st) { var s = st.net; return s ? s.esrUtc(st.dev) + EL.clock.tzMs(st.run.tz) : Date.now(); }
  S.cmd('priv', 'reload system in <w>', function (st, a) {
    var m = a[0].match(/^(?:(\d{1,3}):)?(\d{1,4})$/); if (!m || !st.net) return 'Syntax error: Illegal parameter';
    var sec = ((m[1] ? +m[1] * 60 : 0) + +m[2]) * 60; if (!sec) return 'Syntax error: Illegal parameter';
    st.reloadAt = st.net.now + sec; }, 'Перезагрузить через N минут (или ЧЧ:ММ)');
  S.cmd('priv', 'reload system at <w> <n> <w> <n>', function (st, a) {
    var t = a[0].match(/^(\d{1,2}):(\d{2}):(\d{2})$/), mo = MON.indexOf(String(a[2]).toLowerCase());
    if (!t || +t[1] > 23 || +t[2] > 59 || +t[3] > 59 || mo < 0 || a[1] < 1 || a[1] > 31 || a[3] < 2001 || a[3] > 2037 || !st.net) return 'Syntax error: Illegal parameter';
    var target = Date.UTC(a[3], mo, a[1], +t[1], +t[2], +t[3]), dt = Math.round((target - devNow(st)) / 1000);
    if (dt <= 0) return 'Syntax error: Illegal parameter';
    st.reloadAt = st.net.now + dt; }, 'Перезагрузить в заданное время');
  S.cmd('priv', 'reload cancel', function (st) { delete st.reloadAt; }, 'Отменить запланированную перезагрузку');
  S.cmd('priv', 'show system reload', function (st) {
    if (st.reloadAt === undefined || !st.net) return '';
    var d = new Date(devNow(st) + (st.reloadAt - st.net.now) * 1000), p = function (n) { return ('0' + n).slice(-2); };
    return 'System reload is scheduled for ' + p(d.getUTCHours()) + ':' + p(d.getUTCMinutes()) + ':' + p(d.getUTCSeconds()) + ' ' + d.getUTCDate() + ' ' +
      MON[d.getUTCMonth()].charAt(0).toUpperCase() + MON[d.getUTCMonth()].slice(1) + ' ' + d.getUTCFullYear(); }, 'Запланированная перезагрузка');

  // commit: запомнить последнюю подтверждённую конфигурацию и время запуска таймера
  S.T.forEach(function (c) { if (c.pat.join(' ') !== 'commit') return; var run = c.run;
    c.run = function (st, a) { var was = st.unconfirmed, prev = EL.clone(st.run), r = run(st, a);
      if (st.unconfirmed) { if (!was || !st.saved) st.saved = prev; st.commitAt = st.net ? st.net.now : 0; } return r; }; });
  // перезагрузка без confirm — загружается последняя подтверждённая конфигурация
  var reboot0 = P.reboot;
  P.reboot = function (id) { var d = this.devs[id];
    if (d && d.type === 'esr') { if (d.st.unconfirmed && d.st.saved) d.st.run = EL.clone(d.st.saved); delete d.st.reloadAt; }
    return reboot0.apply(this, arguments); };
  // время: запланированная перезагрузка и истечение таймера commit
  var tick0 = P.tick;
  P.tick = function (dt) {
    var g = tick0.apply(this, arguments), s = this;
    s.order.forEach(function (id) { var d = s.devs[id]; if (!d || d.type !== 'esr' || d.off) return; var st = d.st;
      if (st.unconfirmed && st.saved && st.commitAt !== undefined && s.now - st.commitAt >= COMMIT_TIMER) {
        st.run = EL.clone(st.saved); st.cand = EL.clone(st.saved); st.unconfirmed = false; st.pending = false; s.gen++;
        (s._pend = s._pend || []).push({ id: id, msg: 'Commit timer expired, configuration reverted' }); }
      if (st.reloadAt !== undefined && s.now >= st.reloadAt) { delete st.reloadAt;
        (s._pend = s._pend || []).push({ id: id, msg: 'System is going to reboot...' });
        if (s.onReload) s.onReload(id); else s.reboot(id); } });
    return g;
  };
  var events0 = P.events;
  P.events = function () { var out = events0.apply(this, arguments), p = this._pend || []; this._pend = []; return p.concat(out); };
})(typeof window !== 'undefined' ? window : global);
