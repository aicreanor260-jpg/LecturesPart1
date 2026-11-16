/* Тренажёр CLI маршрутизатора Eltex ESR для деки «Списки контроля доступа (ACL)».
   Режимы и приглашения как в pptx: R1# → configure → R1(config)# → ip access-list extended NAME → R1(config-acl)# →
   rule N → R1(config-acl-rule)#; interface gigabitethernet 1/0/N → R1(config-if-gi)#.
   Изменения копятся в кандидат-конфигурации; commit применяет (таймер 600 с), confirm подтверждает.
   Проверка — по применённому состоянию: тестовые пакеты реально прогоняются через ACL на интерфейсе.
   «Отправить пакеты» показывает, какие пакеты пропустит текущая (применённая) конфигурация. */
(function () {
  'use strict';
  function rnd(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[rnd(0, a.length - 1)]; }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  // ------------------------------------------------------------------ состояние
  function blank() {
    var ifs = {};
    for (var i = 1; i <= 4; i++) ifs['gi1/0/' + i] = { ip: null, input: null };
    return { host: 'R1', acls: {}, ifs: ifs };
  }
  function fresh() {
    var c = blank();
    return { cand: c, run: clone(c), mode: 'priv', ctx: null, pending: false, confirmed: true };
  }
  var PROMPT = { priv: '#', config: '(config)#', acl: '(config-acl)#', rule: '(config-acl-rule)#', gi: '(config-if-gi)#' };
  function prompt(st) { return st.cand.host === st.run.host ? st.run.host + PROMPT[st.mode] : st.run.host + PROMPT[st.mode]; }

  // ------------------------------------------------------------------ IP и маски
  function ip2n(s) { var p = s.split('.'); return ((+p[0] << 24) >>> 0) + (+p[1] << 16) + (+p[2] << 8) + (+p[3]); }
  function okIp(s) { return /^\d+\.\d+\.\d+\.\d+$/.test(s) && s.split('.').every(function (o) { return +o <= 255; }); }
  function okMask(s) {
    if (!okIp(s)) return false; var n = ip2n(s), seen0 = false;
    for (var b = 31; b >= 0; b--) { var bit = (n >>> b) & 1; if (bit && seen0) return false; if (!bit) seen0 = true; }
    return true;
  }
  function inNet(ip, net, mask) { var m = ip2n(mask); return ((ip2n(ip) & m) >>> 0) === ((ip2n(net) & m) >>> 0); }
  function okMac(s) { return /^([0-9a-f]{2}:){5}[0-9a-f]{2}$/i.test(s); }
  function macHit(mac, v, m) {
    var a = mac.toLowerCase().split(':'), b = v.toLowerCase().split(':'), k = m.toLowerCase().split(':');
    for (var i = 0; i < 6; i++) if ((parseInt(a[i], 16) & parseInt(k[i], 16)) !== (parseInt(b[i], 16) & parseInt(k[i], 16))) return false;
    return true;
  }
  var PROTOS = ['tcp', 'udp', 'icmp', 'eigrp', 'ospf', 'igmp', 'pim', 'vrrp', 'any'];

  // ------------------------------------------------------------------ команды
  var CMDS = [];
  function cmd(modes, re, run) { CMDS.push({ modes: modes.split(' '), re: re, run: run }); }
  var CFG = 'config acl rule gi';
  function acl(st) { return st.cand.acls[st.ctx.acl]; }
  function rule(st) { return st.cand.acls[st.ctx.acl].rules[st.ctx.rule]; }

  // --- привилегированный режим
  cmd('priv', /^configure( terminal)?$/, function (st) { st.mode = 'config'; });
  cmd('priv', /^commit$/, function (st) {
    if (JSON.stringify(st.cand) === JSON.stringify(st.run)) return 'Nothing to commit in configuration';
    st.run = clone(st.cand); st.pending = true; st.confirmed = false;
    return 'Configuration has been successfully applied and saved to flash. Commit timer started, changes will be reverted in 600 seconds.'; });
  cmd('priv', /^confirm$/, function (st) {
    if (!st.pending) return 'Nothing to confirm in configuration. You must commit some changes first.';
    st.pending = false; st.confirmed = true; return 'Configuration has been confirmed. Commit timer canceled.'; });
  cmd('priv', /^exit$/, function () { return '% Сессия остаётся открытой (тренажёр)'; });
  cmd('priv', /^show ip access-list$/, function (st) { return showList(st.run); });
  cmd('priv', /^show ip access-list (?:extended )?(\S+)$/, function (st, m) {
    var a = st.run.acls[m[1]]; if (!a) return '% Access list "' + m[1] + '" not found'; return showAcl(a); });
  cmd('priv', /^show running-config(?: \| begin access)?$/, function (st, m) { return showRun(st.run, / begin access/.test(m[0])); });
  cmd('priv', /^show candidate-config$/, function (st) { return showRun(st.cand); });
  cmd('priv', /^show run(?:ning-config)? interfaces? (?:gigabitethernet |gi)(1\/0\/[1-4])$/, function (st, m) {
    return showIf(st.run, 'gi' + m[1]); });

  // --- выход
  cmd(CFG, /^exit$/, function (st) {
    if (st.mode === 'rule') { st.mode = 'acl'; st.ctx = { acl: st.ctx.acl }; return; }
    if (st.mode === 'config') { st.mode = 'priv'; st.ctx = null; return; }
    st.mode = 'config'; st.ctx = null; });
  cmd(CFG, /^end$/, function (st) { st.mode = 'priv'; st.ctx = null; });

  // --- глобальная конфигурация
  cmd('config', /^hostname (\S+)$/, function (st, m) { st.cand.host = m[1]; });
  cmd('config', /^ip access-list extended (\S+)$/, function (st, m) {
    if (m[1].length > 31) return '% Имя ACL — не более 31 символа';
    if (!/^[A-Za-z0-9_-]+$/.test(m[1])) return '% Имя ACL — буквы латинского алфавита и цифры';
    if (!st.cand.acls[m[1]]) st.cand.acls[m[1]] = { desc: null, rules: {} };
    st.mode = 'acl'; st.ctx = { acl: m[1] }; });
  cmd('config', /^ip access-list (?:standard )?(\S+)$/, function () {
    return '% Маршрутизаторы ESR поддерживают только расширенные именованные ACL: ip access-list extended NAME'; });
  cmd('config', /^no ip access-list extended (\S+)$/, function (st, m) {
    if (!st.cand.acls[m[1]]) return '% Access list "' + m[1] + '" not found';
    var used = Object.keys(st.cand.ifs).filter(function (k) { return st.cand.ifs[k].input === m[1]; });
    if (used.length) return '% ACL назначен на интерфейс ' + used.join(', ') + ' — сначала no service-acl input';
    delete st.cand.acls[m[1]]; });
  cmd('config', /^interface (?:gigabitethernet ?|gi)1\/0\/([1-4])$/, function (st, m) { st.mode = 'gi'; st.ctx = { ifc: 'gi1/0/' + m[1] }; });
  cmd('config', /^interface (?:gigabitethernet ?|gi)\S+$/, function () { return '% В тренажёре есть интерфейсы gi1/0/1 – gi1/0/4'; });

  // --- режим ACL
  cmd('acl', /^description (.+)$/, function (st, m) {
    var d = m[1].trim(), q = d.match(/^["“”](.*)["“”]$/);
    if (q) d = q[1]; else if (/\s/.test(d)) return '% Текст с пробелами нужно заключать в кавычки';
    if (d.length > 255) return '% Описание — не более 255 символов';
    acl(st).desc = d; });
  cmd('acl', /^no description$/, function (st) { acl(st).desc = null; });
  cmd('acl', /^rule (\d+)$/, function (st, m) {
    var n = +m[1]; if (n < 1 || n > 4094) return '% Номер правила от 1 до 4094';
    if (!acl(st).rules[n]) acl(st).rules[n] = { act: null, m: {}, en: false };
    st.mode = 'rule'; st.ctx = { acl: st.ctx.acl, rule: n }; });
  cmd('acl', /^no rule (\d+)$/, function (st, m) {
    if (!acl(st).rules[+m[1]]) return '% Правило ' + m[1] + ' не найдено'; delete acl(st).rules[+m[1]]; });

  // --- режим правила
  cmd('rule', /^action (permit|deny)$/, function (st, m) { rule(st).act = m[1]; });
  cmd('rule', /^enable$/, function (st) { rule(st).en = true; });
  cmd('rule', /^no enable$/, function (st) { rule(st).en = false; });
  cmd('rule', /^match (source|destination)-address any$/, function (st, m) { delete rule(st).m[m[1][0] + 'ip']; });
  cmd('rule', /^match (source|destination)-address (\S+) (\S+)$/, function (st, m) {
    if (!okIp(m[2])) return '% Неверный IP-адрес'; if (!okMask(m[3])) return '% Неверная маска подсети (например 255.255.255.0)';
    rule(st).m[m[1][0] + 'ip'] = [m[2], m[3]]; });
  cmd('rule', /^match (source|destination)-address (\S+)$/, function () {
    return '% Укажите адрес и маску подсети: match source-address 192.168.5.0 255.255.255.0 (или any)'; });
  cmd('rule', /^match protocol (\S+)$/, function (st, m) {
    var p = m[1].toLowerCase(); if (PROTOS.indexOf(p) < 0) return '% Неизвестный протокол';
    if (p === 'any') delete rule(st).m.proto; else rule(st).m.proto = p; });
  cmd('rule', /^match (source|destination)-port (\d+)$/, function (st, m) {
    if (+m[2] < 1 || +m[2] > 65535) return '% Номер порта от 1 до 65535'; rule(st).m[m[1][0] + 'port'] = +m[2]; });
  cmd('rule', /^match (source|destination)-mac (\S+) (\S+)$/, function (st, m) {
    if (!okMac(m[2]) || !okMac(m[3])) return '% MAC-адрес и маска в виде XX:XX:XX:XX:XX:XX';
    rule(st).m[m[1][0] + 'mac'] = [m[2].toLowerCase(), m[3].toLowerCase()]; });
  cmd('rule', /^match dscp (\d+)$/, function (st, m) { if (+m[1] > 63) return '% DSCP от 0 до 63'; rule(st).m.dscp = +m[1]; });
  cmd('rule', /^no match (source-address|destination-address|protocol|source-port|destination-port|source-mac|destination-mac|dscp)$/,
    function (st, m) {
      var k = { 'source-address': 'sip', 'destination-address': 'dip', protocol: 'proto', 'source-port': 'sport',
                'destination-port': 'dport', 'source-mac': 'smac', 'destination-mac': 'dmac', dscp: 'dscp' }[m[1]];
      if (!(k in rule(st).m)) return '% Условие ' + m[1] + ' не задано'; delete rule(st).m[k]; });

  // --- интерфейс
  cmd('gi', /^service-acl input (\S+)$/, function (st, m) {
    if (!st.cand.acls[m[1]]) return '% Access list "' + m[1] + '" not found';
    st.cand.ifs[st.ctx.ifc].input = m[1]; });
  cmd('gi', /^no service-acl input$/, function (st) { st.cand.ifs[st.ctx.ifc].input = null; });
  cmd('gi', /^ip address (\d+\.\d+\.\d+\.\d+\/\d+)$/, function (st, m) { st.cand.ifs[st.ctx.ifc].ip = m[1]; });

  // ------------------------------------------------------------------ выводы (как в pptx)
  function pad(s, n) { s = String(s); while (s.length < n) s += ' '; return s; }
  function showList(c) {
    var o = ['Name                           Description', '------------------------------ ------------------------------------'];
    Object.keys(c.acls).forEach(function (n) { o.push(pad(n, 31) + (c.acls[n].desc || '')); });
    return o.join('\n');
  }
  function nums(a) { return Object.keys(a.rules).map(Number).sort(function (x, y) { return x - y; }); }
  function showAcl(a) {
    var o = [];
    nums(a).forEach(function (n) {
      var r = a.rules[n], m = r.m;
      o.push(pad('Index:', 27) + n, 'Matching pattern:',
             pad('    Protocol:', 27) + (m.proto || 'any'),
             pad('    Source MAC address:', 27) + (m.smac ? m.smac.join(' ') : 'any'),
             pad('    Source IP address:', 27) + (m.sip ? m.sip.join(' ') : 'any'));
      if (m.sport) o.push(pad('    Source port:', 27) + m.sport);
      o.push('    Destination MAC address: ' + (m.dmac ? m.dmac.join(' ') : 'any'),
             '    Destination IP address:  ' + (m.dip ? m.dip.join(' ') : 'any'));
      if (m.dport) o.push(pad('    Destination port:', 27) + m.dport);
      if ('dscp' in m) o.push(pad('    DSCP:', 27) + m.dscp);
      o.push(pad('Action:', 27) + (r.act ? r.act[0].toUpperCase() + r.act.slice(1) : '-'),
             pad('Status:', 27) + (r.en ? 'Enabled' : 'Disabled'),
             '-------------------------------------------------------');
    });
    return o.length ? o.join('\n') : '(правил нет)';
  }
  function ruleLines(r) {
    var o = [], m = r.m;
    if (r.act) o.push('    action ' + r.act);
    if (m.smac) o.push('    match source-mac ' + m.smac.join(' '));
    if (m.dmac) o.push('    match destination-mac ' + m.dmac.join(' '));
    if (m.sip) o.push('    match source-address ' + m.sip.join(' '));
    if (m.dip) o.push('    match destination-address ' + m.dip.join(' '));
    if (m.proto) o.push('    match protocol ' + m.proto);
    if (m.sport) o.push('    match source-port ' + m.sport);
    if (m.dport) o.push('    match destination-port ' + m.dport);
    if ('dscp' in m) o.push('    match dscp ' + m.dscp);
    if (r.en) o.push('    enable');
    return o;
  }
  function showRun(c, fromAccess) {
    var o = fromAccess ? [] : ['hostname ' + c.host, ''];
    Object.keys(c.acls).forEach(function (n) {
      var a = c.acls[n]; o.push('ip access-list extended ' + n);
      if (a.desc) o.push('  description "' + a.desc + '"');
      nums(a).forEach(function (k) { o.push('  rule ' + k); o = o.concat(ruleLines(a.rules[k])); o.push('  exit'); });
      o.push('exit');
    });
    Object.keys(c.ifs).forEach(function (k) { var s = showIf(c, k); if (s.split('\n').length > 2) o.push(s); });
    return o.join('\n');
  }
  function showIf(c, k) {
    var x = c.ifs[k], o = ['interface gigabitethernet ' + k.slice(2)];
    if (x.input) o.push('  service-acl input ' + x.input);
    if (x.ip) o.push('  ip address ' + x.ip);
    o.push('exit');
    return o.join('\n');
  }

  // ------------------------------------------------------------------ разбор строки
  var KW = ['configure', 'commit', 'confirm', 'show', 'interface', 'exit', 'end', 'description', 'rule', 'action', 'match',
            'enable', 'service-acl', 'access-list', 'extended', 'running-config', 'candidate-config', 'source-address',
            'destination-address', 'protocol', 'source-port', 'destination-port', 'source-mac', 'destination-mac', 'dscp',
            'permit', 'deny', 'input', 'hostname', 'address', 'gigabitethernet', 'terminal', 'interfaces'];
  var FREE = ['description', 'extended', 'input', 'hostname', 'begin'];
  function expand(toks) {
    var out = [], free = false;
    toks.forEach(function (t) {
      if (free) { out.push(t); return; }
      var lt = t.toLowerCase(), hit = null;
      if (KW.indexOf(lt) >= 0) hit = lt;
      else if (lt.length >= 2 && /^[a-z-]+$/.test(lt)) {
        var c = KW.filter(function (k) { return k.indexOf(lt) === 0; });
        if (c.length === 1) hit = c[0];
        if (lt === 'conf' || lt === 'config') hit = 'configure';
        if (lt === 'sh') hit = 'show';
        if (lt === 'int') hit = 'interface';
        if (lt === 'in' && out[out.length - 1] === 'service-acl') hit = 'input';
      }
      if (lt === 'begin') hit = 'begin';
      if (hit === 'ip' || lt === 'ip' || lt === 'no' || lt === 'do' || lt === 'any' || lt === 'run') hit = lt;
      out.push(hit || t);
      if (FREE.indexOf(hit) >= 0) free = true;
    });
    return out;
  }
  function norm(line) {
    var s = line.trim().replace(/\s+/g, ' ').replace(/^\S+?(\([^)]*\))?#\s*/, '');
    if (!s) return '';
    var toks = s.split(' ');
    s = expand(toks).join(' ');
    s = s.replace(/^(interface|show run(?:ning-config)? interfaces?) (?:gigabitethernet|gi) ?(\d)/i, '$1 gi$2');
    return s;
  }
  function run1(st, s) {
    for (var i = 0; i < CMDS.length; i++) {
      var c = CMDS[i], m = s.match(c.re);
      if (m && c.modes.indexOf(st.mode) >= 0) return { r: c.run(st, m) || '' };
    }
    return null;
  }
  function exec(st, line) {
    var s = norm(line);
    if (!s) return '';
    if (/\?$/.test(s)) return help(st, s.replace(/\s*\?$/, ''));
    var doCmd = s.match(/^do (.+)$/);
    if (doCmd && st.mode === 'priv') s = doCmd[1];
    else if (doCmd) {
      var keep = st.mode, ctx = st.ctx; st.mode = 'priv';
      var r = run1(st, doCmd[1]); st.mode = keep; st.ctx = ctx;
      return r ? r.r : '% Unknown command';
    }
    var res = run1(st, s);
    if (res) return res.r;
    for (var j = 0; j < CMDS.length; j++) if (s.match(CMDS[j].re)) return '% Команда недоступна в этом режиме';
    return '% Unknown command';
  }
  function help(st, s) {
    var names = Object.keys(st.cand.acls);
    if (/service-acl input$/.test(s) || /show ip access-list$/.test(s)) {
      var o = /show/.test(s) ? ['  WORD(1-31)  Show information for specific access list', '  >           Copy lines to file',
        '  >>          Copy lines to end of file', '  |           Output modifiers', ''] : ['  WORD(1-31)  Access list name'];
      o.push('  ----objects----'); names.forEach(function (n) { o.push('  ' + n); }); if (/show/.test(s)) o.push('  <cr>');
      return o.join('\n');
    }
    if (st.mode === 'priv') return 'commit  confirm  configure  show  exit';
    if (st.mode === 'config') return 'ip access-list extended  interface  hostname  do  exit  end';
    if (st.mode === 'acl') return 'description  rule  no rule  do  exit  end';
    if (st.mode === 'rule') return 'action  match  no match  enable  no enable  do  exit  end';
    return 'service-acl input  no service-acl input  ip address  do  exit  end';
  }

  // ------------------------------------------------------------------ прогон пакета через ACL
  function evalAcl(a, pk) {
    var ns = nums(a);
    for (var i = 0; i < ns.length; i++) {
      var r = a.rules[ns[i]], m = r.m;
      if (!r.en || !r.act) continue;
      if (m.sip && !inNet(pk.sip, m.sip[0], m.sip[1])) continue;
      if (m.dip && !inNet(pk.dip, m.dip[0], m.dip[1])) continue;
      if (m.proto && m.proto !== pk.proto) continue;
      if (m.sport && m.sport !== pk.sport) continue;
      if (m.dport && m.dport !== pk.dport) continue;
      if (m.smac && !macHit(pk.smac || '00:00:00:00:00:00', m.smac[0], m.smac[1])) continue;
      if ('dscp' in m && m.dscp !== (pk.dscp || 0)) continue;
      return { ok: r.act === 'permit', why: 'Rule ' + ns[i] + ' ' + (r.act === 'permit' ? 'Permit' : 'Deny') };
    }
    return { ok: false, why: 'неявный запрет (implicit deny)' };
  }
  function through(c, ifc, pk) {
    var n = c.ifs[ifc].input;
    if (!n || !c.acls[n]) return { ok: true, why: 'на ' + ifc + ' нет ACL на входе' };
    return evalAcl(c.acls[n], pk);
  }
  function pkName(pk) {
    var p = pk.proto ? pk.proto.toUpperCase() + (pk.dport ? ' ' + pk.dport : '') : '';
    return (pk.label ? pk.label + ': ' : '') + pk.sip + ' → ' + pk.dip + (p ? ' (' + p + (pk.dscp ? ', DSCP ' + pk.dscp : '') + ')' : '');
  }
  function applied(st) { return st.confirmed && !st.pending && JSON.stringify(st.cand) === JSON.stringify(st.run); }
  var A = ['Изменения применены (commit) и подтверждены (confirm)', applied];
  function pkChecks(P) {
    return P.pk.map(function (pk) {
      return [pkName(pk) + ' — ' + (pk.want ? 'пропускается' : 'отбрасывается'),
              function (s) { return through(s.run, P.ifc, pk).ok === pk.want; }];
    });
  }
  function sendPk(P, st) {
    return P.pk.map(function (pk) {
      var r = through(st.run, P.ifc, pk);
      return { ok: r.ok === pk.want, t: pkName(pk) + ': ' + (r.ok ? 'пропущен' : 'отброшен') + ' — ' + r.why +
        (r.ok === pk.want ? '' : ' (а нужно: ' + (pk.want ? 'пропустить' : 'отбросить') + ')') };
    });
  }
  function onIf(P) { return ['ACL ' + P.name + ' назначен на ' + P.ifc + ' (service-acl input)',
                             function (s) { return s.run.ifs[P.ifc].input === P.name; }]; }

  // ------------------------------------------------------------------ готовые списки из pptx (для заданий на редактирование)
  var STD1 = ['configure', 'ip access-list extended StdList1', 'description "Standard ACL test"', 'rule 10', 'action permit',
    'match source-address 192.168.5.20 255.255.255.255', 'enable', 'exit', 'rule 20', 'action deny',
    'match source-address 192.168.5.0 255.255.255.0', 'enable', 'exit', 'rule 30', 'action permit',
    'match source-address any', 'enable', 'exit', 'exit', 'interface gigabitethernet 1/0/1', 'service-acl input StdList1', 'end',
    'commit', 'confirm'];
  var EXT1 = ['configure', 'ip access-list extended ExtList1', 'description "Extended ACL test"', 'rule 10', 'action permit',
    'match source-mac a8:f9:4b:00:00:00 ff:ff:ff:00:00:00', 'match dscp 46', 'enable', 'exit', 'rule 20', 'action deny',
    'match source-address 10.10.1.0 255.255.255.0', 'match protocol tcp', 'match destination-port 80', 'enable', 'exit',
    'rule 30', 'action deny', 'match destination-address 10.10.20.0 255.255.255.0', 'match protocol icmp', 'enable', 'exit',
    'rule 40', 'action permit', 'enable', 'exit', 'exit', 'interface gigabitethernet 1/0/1', 'service-acl input ExtList1', 'end',
    'commit', 'confirm'];
  var WRONG = ['configure', 'ip access-list extended StdList1', 'rule 10', 'action deny',
    'match source-address 192.168.5.0 255.255.255.0', 'enable', 'exit', 'rule 20', 'action permit',
    'match source-address 192.168.5.20 255.255.255.255', 'enable', 'exit', 'rule 30', 'action permit', 'enable', 'exit', 'exit',
    'interface gigabitethernet 1/0/1', 'service-acl input StdList1', 'end', 'commit', 'confirm'];
  function preload(st, lines) { lines.forEach(function (l) { exec(st, l); }); }
  var WEB = '62.109.1.166';
  var DESCS = ['Production standard ACL', 'Office filter', 'RnD protection', 'Finance server access'];

  var TASKS = [
    { // 0 «стандартный» ACL: один узел разрешён, остальная сеть запрещена (pptx 19–23)
      gen: function () { var o = rnd(2, 99), h = rnd(2, 250); return { name: 'StdList' + rnd(1, 9), o: o, h: h, ifc: 'gi1/0/' + rnd(1, 4),
        pk: [{ label: 'узел', sip: '192.168.' + o + '.' + h, dip: WEB, want: true },
             { label: 'сосед', sip: '192.168.' + o + '.' + (h === 250 ? 3 : h + 1), dip: WEB, want: false },
             { label: 'другая сеть', sip: '10.10.' + rnd(1, 9) + '.' + rnd(2, 200), dip: WEB, want: true }] }; },
      text: function (P) { return 'Отделу выделена сеть <b>192.168.' + P.o + '.0/24</b>. Создайте ACL <b>' + P.name + '</b>: разрешите узел ' +
        '<b>192.168.' + P.o + '.' + P.h + '</b>, запретите остальную сеть отдела, весь прочий трафик разрешите. Назначьте ACL на ' +
        '<b>' + P.ifc + '</b> во входящем направлении, примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'ip access-list extended ' + P.name, 'rule 10', 'action permit',
        'match source-address 192.168.' + P.o + '.' + P.h + ' 255.255.255.255', 'enable', 'exit', 'rule 20', 'action deny',
        'match source-address 192.168.' + P.o + '.0 255.255.255.0', 'enable', 'exit', 'rule 30', 'action permit', 'enable', 'exit',
        'exit', 'interface gigabitethernet ' + P.ifc.slice(2), 'service-acl input ' + P.name, 'end', 'commit', 'confirm']; },
      checks: function (P) { return [['Создан ACL ' + P.name, function (s) { return !!s.run.acls[P.name]; }], onIf(P)].concat(pkChecks(P), [A]); },
      send: sendPk
    },
    { // 1 расширенный ACL: HTTP из сети и ICMP в сеть администраторов (pptx 15, 26)
      gen: function () { var a = rnd(1, 9), b = rnd(20, 29); return { name: 'ExtList' + rnd(1, 9), a: a, b: b, ifc: 'gi1/0/' + rnd(1, 4),
        pk: [{ label: 'HTTP', sip: '10.10.' + a + '.25', dip: WEB, proto: 'tcp', dport: 80, want: false },
             { label: 'HTTPS', sip: '10.10.' + a + '.25', dip: WEB, proto: 'tcp', dport: 443, want: true },
             { label: 'ping', sip: '10.10.' + a + '.25', dip: '10.10.' + b + '.7', proto: 'icmp', want: false },
             { label: 'ping', sip: '10.10.' + a + '.25', dip: '8.8.8.8', proto: 'icmp', want: true }] }; },
      text: function (P) { return 'Создайте ACL <b>' + P.name + '</b>: запретите устройствам сети <b>10.10.' + P.a + '.0/24</b> трафик ' +
        '<b>TCP на порт 80</b> (HTTP) в любом направлении, запретите <b>ICMP</b> в сеть администраторов <b>10.10.' + P.b + '.0/24</b>, ' +
        'остальное разрешите. Назначьте на <b>' + P.ifc + '</b> (вход), примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'ip access-list extended ' + P.name, 'rule 10', 'action deny',
        'match source-address 10.10.' + P.a + '.0 255.255.255.0', 'match protocol tcp', 'match destination-port 80', 'enable', 'exit',
        'rule 20', 'action deny', 'match destination-address 10.10.' + P.b + '.0 255.255.255.0', 'match protocol icmp', 'enable', 'exit',
        'rule 30', 'action permit', 'enable', 'exit', 'exit', 'interface gigabitethernet ' + P.ifc.slice(2),
        'service-acl input ' + P.name, 'end', 'commit', 'confirm']; },
      checks: function (P) { return [['Создан ACL ' + P.name, function (s) { return !!s.run.acls[P.name]; }], onIf(P)].concat(pkChecks(P), [A]); },
      send: sendPk
    },
    { // 2 IP-телефоны Eltex (OUI a8:f9:4b, DSCP 46) — правило первым (pptx 21, 26)
      gen: function () { var a = rnd(1, 9); return { name: 'VoiceList' + rnd(1, 9), a: a, ifc: 'gi1/0/' + rnd(1, 4),
        pk: [{ label: 'IP-телефон', sip: '10.10.' + a + '.40', dip: WEB, smac: 'a8:f9:4b:12:34:56', dscp: 46, want: true },
             { label: 'ПК', sip: '10.10.' + a + '.41', dip: WEB, smac: 'aa:bb:cc:33:22:11', want: false },
             { label: 'другая сеть', sip: '172.16.' + rnd(1, 99) + '.5', dip: WEB, smac: 'aa:bb:cc:44:55:66', want: true }] }; },
      text: function (P) { return 'Создайте ACL <b>' + P.name + '</b>: первым правилом разрешите пакеты IP-телефонов Eltex — ' +
        '<b>source-mac a8:f9:4b:00:00:00 ff:ff:ff:00:00:00</b> и <b>DSCP 46</b>; затем запретите всё из сети <b>10.10.' + P.a +
        '.0/24</b>; остальное разрешите. Назначьте на <b>' + P.ifc + '</b> (вход), примените и подтвердите.'; },
      sol: function (P) { return ['configure', 'ip access-list extended ' + P.name, 'rule 10', 'action permit',
        'match source-mac a8:f9:4b:00:00:00 ff:ff:ff:00:00:00', 'match dscp 46', 'enable', 'exit', 'rule 20', 'action deny',
        'match source-address 10.10.' + P.a + '.0 255.255.255.0', 'enable', 'exit', 'rule 30', 'action permit', 'enable', 'exit',
        'exit', 'interface gigabitethernet ' + P.ifc.slice(2), 'service-acl input ' + P.name, 'end', 'commit', 'confirm']; },
      checks: function (P) { return [['Создан ACL ' + P.name, function (s) { return !!s.run.acls[P.name]; }], onIf(P)].concat(pkChecks(P), [A]); },
      send: sendPk
    },
    { // 3 изменение описания (pptx 31)
      gen: function () { return { d: pick(DESCS), name: 'StdList1', ifc: 'gi1/0/1', pk: [] }; },
      setup: function (P, st) { preload(st, STD1); },
      text: function (P) { return 'В конфигурации есть ACL <b>StdList1</b> с описанием «Standard ACL test». Замените описание на ' +
        '<b>' + P.d + '</b>, примените и подтвердите. Проверьте командой show ip access-list.'; },
      sol: function (P) { return ['configure', 'ip access-list extended StdList1', 'description "' + P.d + '"', 'end', 'commit', 'confirm',
        'show ip access-list']; },
      checks: function (P) { return [['Описание StdList1 — «' + P.d + '»', function (s) { return s.run.acls.StdList1 && s.run.acls.StdList1.desc === P.d; }], A]; }
    },
    { // 4 удаление правила (pptx 32)
      gen: function () { return { name: 'StdList1', ifc: 'gi1/0/1',
        pk: [{ label: 'узел', sip: '192.168.5.20', dip: WEB, want: true }, { label: 'сосед', sip: '192.168.5.' + rnd(30, 90), dip: WEB, want: true }] }; },
      setup: function (P, st) { preload(st, STD1); },
      text: function () { return 'ACL <b>StdList1</b> (Rule 10 Permit 192.168.5.20, Rule 20 Deny 192.168.5.0/24, Rule 30 Permit any) ' +
        'назначен на gi1/0/1. Удалите правило <b>Rule 20</b>, примените, подтвердите и проверьте вывод show ip access-list StdList1.'; },
      sol: function () { return ['configure', 'ip access-list extended StdList1', 'no rule 20', 'end', 'commit', 'confirm',
        'show ip access-list StdList1']; },
      checks: function (P) { return [['Rule 20 удалено', function (s) { return s.run.acls.StdList1 && !s.run.acls.StdList1.rules[20]; }],
        ['Rule 10 и Rule 30 на месте', function (s) { var r = s.run.acls.StdList1 && s.run.acls.StdList1.rules; return r && r[10] && r[30]; }]]
        .concat(pkChecks(P), [A]); },
      send: sendPk
    },
    { // 5 деактивация правила (pptx 32)
      gen: function () { return { name: 'ExtList1', ifc: 'gi1/0/1',
        pk: [{ label: 'HTTP', sip: '10.10.1.' + rnd(2, 200), dip: WEB, proto: 'tcp', dport: 80, want: true }] }; },
      setup: function (P, st) { preload(st, EXT1); },
      text: function () { return 'На время теста нужно пропустить HTTP из сети 10.10.1.0/24. Временно <b>деактивируйте</b> правило ' +
        '<b>Rule 20</b> списка <b>ExtList1</b>, не удаляя его. Примените и подтвердите.'; },
      sol: function () { return ['configure', 'ip access-list extended ExtList1', 'rule 20', 'no enable', 'end', 'commit', 'confirm']; },
      checks: function (P) { return [['Rule 20 существует', function (s) { return s.run.acls.ExtList1 && !!s.run.acls.ExtList1.rules[20]; }],
        ['Rule 20 — Status: Disabled', function (s) { var r = s.run.acls.ExtList1 && s.run.acls.ExtList1.rules[20]; return r && !r.en; }]]
        .concat(pkChecks(P), [A]); },
      send: sendPk
    },
    { // 6 удаление условия (pptx 33)
      gen: function () { return { name: 'ExtList1', ifc: 'gi1/0/1',
        pk: [{ label: 'IP-телефон', sip: '10.10.5.40', dip: WEB, smac: 'a8:f9:4b:00:11:22', dscp: 0, want: true }] }; },
      setup: function (P, st) { preload(st, EXT1); },
      text: function () { return 'Измените правило <b>Rule 10</b> списка <b>ExtList1</b> так, чтобы ACL при сравнении <b>не учитывал DSCP</b> ' +
        '(source-mac оставьте). Примените, подтвердите и проверьте show ip access-list ExtList1.'; },
      sol: function () { return ['configure', 'ip access-list extended ExtList1', 'rule 10', 'no match dscp', 'end', 'commit', 'confirm',
        'show ip access-list ExtList1']; },
      checks: function (P) { return [['В Rule 10 нет условия dscp', function (s) { var r = s.run.acls.ExtList1 && s.run.acls.ExtList1.rules[10]; return r && !('dscp' in r.m); }],
        ['В Rule 10 осталось условие source-mac', function (s) { var r = s.run.acls.ExtList1 && s.run.acls.ExtList1.rules[10]; return r && !!r.m.smac; }]]
        .concat(pkChecks(P), [A]); },
      send: sendPk
    },
    { // 7 порядок правил: от частного к общему (pptx 19–20)
      gen: function () { return { name: 'StdList1', ifc: 'gi1/0/1',
        pk: [{ label: 'узел', sip: '192.168.5.20', dip: WEB, want: true }, { label: 'сосед', sip: '192.168.5.' + rnd(30, 90), dip: WEB, want: false },
             { label: 'другая сеть', sip: '10.10.' + rnd(1, 9) + '.9', dip: WEB, want: true }] }; },
      setup: function (P, st) { preload(st, WRONG); },
      text: function () { return 'ACL <b>StdList1</b> собран с ошибкой: Rule 10 Deny 192.168.5.0/24 стоит раньше Rule 20 Permit ' +
        '192.168.5.20, и узел 192.168.5.20 отбрасывается. Не удаляя существующие правила, добавьте правило с меньшим номером, ' +
        'чтобы узел <b>192.168.5.20</b> проходил. Примените и подтвердите.'; },
      sol: function () { return ['configure', 'ip access-list extended StdList1', 'rule 5', 'action permit',
        'match source-address 192.168.5.20 255.255.255.255', 'enable', 'end', 'commit', 'confirm']; },
      checks: function (P) { return [['Правила 10, 20, 30 не удалены', function (s) { var r = s.run.acls.StdList1 && s.run.acls.StdList1.rules; return r && r[10] && r[20] && r[30]; }]]
        .concat(pkChecks(P), [A]); },
      send: sendPk
    }
  ];

  // ------------------------------------------------------------------ виджет
  function init(box) {
    var pool = (box.dataset.pool || '').split(',').map(Number);
    var out = box.querySelector('.cs-out'), inp = box.querySelector('.cs-in input'), pr = box.querySelector('.cs-pr');
    var taskEl = box.querySelector('.cs-task'), res = box.querySelector('.cs-res'), sol = box.querySelector('.cs-sol');
    var sendB = box.querySelector('[data-cs=send]');
    var st, T, P, hist = [], hi = 0, last = -1;
    function print(t, cls) { var d = document.createElement('div'); d.className = cls || ''; d.innerHTML = esc(t); out.appendChild(d); out.scrollTop = out.scrollHeight; }
    function newTask() {
      var k; do { k = pool[rnd(0, pool.length - 1)]; } while (pool.length > 1 && k === last); last = k;
      T = TASKS[k]; P = T.gen(); st = fresh(); if (T.setup) T.setup(P, st);
      st.mode = 'priv'; st.ctx = null;
      taskEl.innerHTML = T.text(P); res.innerHTML = ''; sol.style.display = 'none';
      sol.textContent = T.sol(P).join('\n');
      out.innerHTML = '';
      print('*** Eltex ESR · R1 ***' + (T.setup ? '\nКонфигурация загружена: show running-config' : ''), 'cs-sys');
      pr.textContent = prompt(st);
      sendB.style.display = T.send ? '' : 'none';
    }
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        var v = inp.value; print(prompt(st) + ' ' + v, 'cs-cmd'); if (v.trim()) { hist.push(v); } hi = hist.length;
        var r = exec(st, v); if (r) print(r, /^%/.test(r) ? 'cs-err' : (/^Configuration has been/.test(r) ? 'cs-ok' : ''));
        inp.value = ''; pr.textContent = prompt(st);
        e.preventDefault();
      } else if (e.key === 'ArrowUp') { if (hi > 0) { hi--; inp.value = hist[hi]; } e.preventDefault(); }
      else if (e.key === 'ArrowDown') { if (hi < hist.length) { hi++; inp.value = hist[hi] || ''; } e.preventDefault(); }
      e.stopPropagation();
    });
    out.addEventListener('click', function () { inp.focus(); });
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cs]'); if (!b) return;
      var a = b.dataset.cs;
      if (a === 'new') newTask();
      if (a === 'sol') sol.style.display = sol.style.display === 'none' ? 'block' : 'none';
      if (a === 'check') {
        var cs = T.checks(P), ok = 0;
        res.innerHTML = cs.map(function (c) { var y = !!c[1](st); if (y) ok++; return '<div class="' + (y ? 'ok' : 'no') + '">' + (y ? '✓ ' : '✗ ') + esc(c[0]) + '</div>'; }).join('') +
          (st.pending ? '<div class="exp">⚑ commit выполнен, но не подтверждён — выполните confirm, иначе через 600 с конфигурация откатится</div>' : '') +
          '<div class="cs-sum ' + (ok === cs.length ? 'ok' : 'no') + '">' + (ok === cs.length ? 'Задание выполнено' : 'Выполнено ' + ok + ' из ' + cs.length) + '</div>';
      }
      if (a === 'send') {
        var r = T.send(P, st);
        res.innerHTML = '<div class="cs-send">' + r.map(function (x, i) {
          return '<div class="' + (x.ok ? 'ok' : 'no') + '"><span class="env" style="animation-delay:' + (i * .25) + 's">✉</span> ' + esc(x.t) + '</div>'; }).join('') + '</div>';
      }
    });
    newTask();
  }
  window.ACL_CLI = { TASKS: TASKS, fresh: fresh, exec: exec, prompt: prompt, through: through, applied: applied };
  document.querySelectorAll('.clisim[data-deck=acl]').forEach(init);
})();
