/* ESR для лаб 7.1 и 8.3: списки доступа (ip access-list extended, service-acl input), telnet-сервер, VRRP. */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip, S = EL.esr, cmd = S.cmd;
  function touch(st) { st.pending = true; }
  S.PROMPT.acl = '(config-acl)#'; S.PROMPT.aclr = '(config-acl-rule)#';
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes.push('acl', 'aclr'); });
  cmd('acl aclr', 'exit', function (st) { if (st.mode === 'aclr') { st.mode = 'acl'; st.ctx = st.aclName; } else { st.mode = 'config'; st.ctx = null; } });

  // ---------------------------------------------------------------- telnet
  cmd('config', 'ip telnet server', function (st) { st.cand.telnet = true; touch(st); }, 'Включить Telnet-сервер');
  cmd('config', 'no ip telnet server', function (st) { st.cand.telnet = false; touch(st); });

  // ---------------------------------------------------------------- ACL
  function acls(st) { return st.cand.acls || (st.cand.acls = {}); }
  cmd('config', 'ip access-list extended <w>', function (st, a) { var A = acls(st); if (!A[a[0]]) A[a[0]] = { rules: {} };
    touch(st); st.mode = 'acl'; st.ctx = st.aclName = a[0]; }, 'Расширенный список доступа');
  cmd('config', 'no ip access-list extended <w>', function (st, a) { delete acls(st)[a[0]]; touch(st); });
  cmd('acl', 'rule <n>', function (st, a) { var L = acls(st)[st.aclName]; if (!L.rules[a[0]]) L.rules[a[0]] = { on: false, act: null };
    touch(st); st.mode = 'aclr'; st.ctx = a[0]; }, 'Правило');
  cmd('acl', 'no rule <n>', function (st, a) { delete acls(st)[st.aclName].rules[a[0]]; touch(st); });
  function rule(st) { return acls(st)[st.aclName].rules[st.ctx]; }
  cmd('aclr', 'action permit', function (st) { rule(st).act = 'permit'; touch(st); }, 'Разрешить');
  cmd('aclr', 'action deny', function (st) { rule(st).act = 'deny'; touch(st); }, 'Запретить');
  cmd('aclr', 'match protocol <w>', function (st, a) { var p = a[0].toLowerCase();
    if (['tcp', 'udp', 'icmp', 'any'].indexOf(p) < 0) return '% Протокол: tcp | udp | icmp | any'; rule(st).proto = p; touch(st); }, 'Протокол');
  cmd('aclr', 'match destination-port port-range <w>', function (st, a) { var m = String(a[0]).match(/^(\d+)(?:-(\d+))?$/);
    if (!m) return '% Порт или диапазон: 23 или 20-23'; rule(st).dport = [+m[1], +(m[2] || m[1])]; touch(st); }, 'Порт назначения');
  function rng(s) { var m = String(s).match(/^(\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+)$/); if (m) return [m[1], m[2]];
    var c = IP.parseCidr(s); if (c) { var n = IP.ip2n(c.ip) & IP.maskN(c.len); return [IP.n2ip(n >>> 0), IP.n2ip((n | ~IP.maskN(c.len)) >>> 0)]; } return null; }
  cmd('aclr', 'match source-address address-range <w>', function (st, a) { var r = rng(a[0]); if (!r) return '% Формат: A.B.C.D-A.B.C.D';
    rule(st).src = r; touch(st); }, 'Адрес источника');
  cmd('aclr', 'match destination-address address-range <w>', function (st, a) { var r = rng(a[0]); if (!r) return '% Формат: A.B.C.D-A.B.C.D';
    rule(st).dst = r; touch(st); }, 'Адрес назначения');
  cmd('aclr', 'enable', function (st) { if (!rule(st).act) return '% Сначала задайте action permit | deny'; rule(st).on = true; touch(st); }, 'Включить правило');
  cmd('aclr', 'no enable', function (st) { rule(st).on = false; touch(st); });
  function eachIf(st, f) { (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { f(st.cand.ifs[k]); }); touch(st); }
  cmd('gi sub', 'service-acl input <w>', function (st, a) { if (!acls(st)[a[0]]) return '% Список доступа ' + a[0] + ' не создан';
    eachIf(st, function (x) { x.acl = a[0]; }); }, 'Назначить список доступа на вход');
  cmd('gi sub', 'no service-acl input', function (st) { eachIf(st, function (x) { delete x.acl; }); });
  cmd('priv', 'show ip access-list <w>', function (st, a) { var L = (st.run.acls || {})[a[0]]; if (!L) return '% Список не найден';
    return Object.keys(L.rules).sort(function (x, y) { return x - y; }).map(function (k) { var r = L.rules[k];
      return 'rule ' + k + ': ' + (r.act || '-') + (r.proto ? ' ' + r.proto : '') + (r.dport ? ' dport ' + r.dport.join('-') : '') +
        (r.src ? ' src ' + r.src.join('-') : '') + (r.dst ? ' dst ' + r.dst.join('-') : '') + (r.on ? '' : '  (выключено)'); }).join('\n') +
      '\n(не совпало ни одно правило — пакет отбрасывается)'; });

  // ---------------------------------------------------------------- VRRP
  function vr(st) { var o = []; (Array.isArray(st.ctx) ? st.ctx : [st.ctx]).forEach(function (k) { var x = st.cand.ifs[k]; x.vrrp = x.vrrp || { prio: 100 }; o.push(x.vrrp); }); return o; }
  cmd('gi sub', 'vrrp id <n>', function (st, a) { if (a[0] < 1 || a[0] > 255) return '% Идентификатор 1–255'; vr(st).forEach(function (v) { v.id = a[0]; }); touch(st); }, 'Идентификатор VRRP');
  cmd('gi sub', 'vrrp ip <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return '% Формат: vrrp ip A.B.C.D/длина';
    vr(st).forEach(function (v) { v.ip = c.ip + '/' + c.len; }); touch(st); }, 'Виртуальный IP-адрес');
  cmd('gi sub', 'vrrp priority <n>', function (st, a) { if (a[0] < 1 || a[0] > 254) return '% Приоритет 1–254'; vr(st).forEach(function (v) { v.prio = a[0]; }); touch(st); }, 'Приоритет');
  cmd('gi sub', 'vrrp', function (st) { var bad = vr(st).some(function (v) { return !v.id || !v.ip; });
    if (bad) return '% Сначала vrrp id и vrrp ip'; vr(st).forEach(function (v) { v.on = true; }); touch(st); }, 'Запустить VRRP на интерфейсе');
  cmd('gi sub', 'no vrrp', function (st) { vr(st).forEach(function (v) { v.on = false; }); touch(st); });
  cmd('priv', 'show vrrp', function (st) { return st.net ? st.net.vrrpText(st.dev) : ''; }, 'Состояние VRRP');

  S.RUNX.push(function (c, o) {
    if (c.telnet) o.push('ip telnet server');
    Object.keys(c.acls || {}).forEach(function (n) { var L = c.acls[n]; o.push('ip access-list extended ' + n);
      Object.keys(L.rules).forEach(function (k) { var r = L.rules[k]; o.push('  rule ' + k); if (r.act) o.push('    action ' + r.act);
        if (r.proto) o.push('    match protocol ' + r.proto); if (r.dport) o.push('    match destination-port port-range ' + (r.dport[0] === r.dport[1] ? r.dport[0] : r.dport.join('-')));
        if (r.src) o.push('    match source-address address-range ' + r.src.join('-')); if (r.dst) o.push('    match destination-address address-range ' + r.dst.join('-'));
        if (r.on) o.push('    enable'); o.push('  exit'); });
      o.push('exit'); });
    Object.keys(c.ifs).forEach(function (k) { var x = c.ifs[k], d = [];
      if (x.acl) d.push('  service-acl input ' + x.acl);
      if (x.vrrp) { if (x.vrrp.id) d.push('  vrrp id ' + x.vrrp.id); if (x.vrrp.ip) d.push('  vrrp ip ' + x.vrrp.ip);
        if (x.vrrp.prio !== 100) d.push('  vrrp priority ' + x.vrrp.prio); if (x.vrrp.on) d.push('  vrrp'); }
      if (d.length) o.push('interface ' + S.longIf(k), d.join('\n'), 'exit'); });
  });

  // проверка входящего пакета списком доступа: true — пропустить
  EL.aclPass = function (L, pk) {
    if (!L) return { ok: true };
    var ks = Object.keys(L.rules).map(Number).sort(function (a, b) { return a - b; });
    for (var i = 0; i < ks.length; i++) {
      var r = L.rules[ks[i]]; if (!r.on) continue;
      if (r.proto && r.proto !== 'any' && r.proto !== pk.proto) continue;
      if (r.dport && !(pk.dport >= r.dport[0] && pk.dport <= r.dport[1])) continue;
      if (r.src && !(IP.ip2n(pk.src) >= IP.ip2n(r.src[0]) && IP.ip2n(pk.src) <= IP.ip2n(r.src[1]))) continue;
      if (r.dst && !(IP.ip2n(pk.dst) >= IP.ip2n(r.dst[0]) && IP.ip2n(pk.dst) <= IP.ip2n(r.dst[1]))) continue;
      return { ok: r.act === 'permit', rule: ks[i] };
    }
    return { ok: false, rule: null };
  };
})(typeof window !== 'undefined' ? window : global);
