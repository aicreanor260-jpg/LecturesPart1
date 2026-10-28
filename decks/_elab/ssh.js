/* SSH: ключи хостов, known_hosts, ключи пользователей (OpenSSH на Debian, справочник ESR-Series CLI 1.23).
   Debian (клиент): ssh [-p ПОРТ] [-i КЛЮЧ] [-l ИМЯ] [-o StrictHostKeyChecking=yes|no|accept-new] [-o UserKnownHostsFile=Ф] ИМЯ@A;
     ~/.ssh/known_hosts — запомненные ключи серверов: новый сервер — вопрос yes/no, сменился ключ — предупреждение и отказ,
     пока старую запись не удалить: ssh-keygen -R A (или -f Ф -R A), rm ~/.ssh/known_hosts, nano;
     ssh-keygen [-t rsa|ecdsa|ed25519] [-b БИТ] [-f Ф] [-N ФРАЗА] [-C КОММЕНТАРИЙ] [-q] — пара ключей с вопросами о файле и парольной фразе;
     ssh-keygen -l -f Ф — отпечаток; ssh-keygen -A — создать недостающие ключи хоста; ssh-copy-id [-i Ф.pub] [-p П] ИМЯ@A — ключ в authorized_keys.
   Debian (сервер): sshd — вход по паролю или по ключу из ~/.ssh/authorized_keys; /etc/ssh/sshd_config: PermitRootLogin (по умолчанию
     prohibit-password — root только по ключу), PasswordAuthentication, PubkeyAuthentication, Port; ключи хоста /etc/ssh/ssh_host_*_key(.pub),
     dpkg-reconfigure openssh-server — новые ключи хоста.
   ESR: ip ssh server, ip ssh port N, update ssh-host-key rsa|ecdsa|ed25519|dsa [N], show crypto key mypubkey rsa|ecdsa|ed25519|dsa,
     ssh ИМЯ A [port N] (клиент, свои known hosts), clear ssh host A [port N].  MES: crypto key generate rsa — новый ключ хоста.
   scp [-P ПОРТ] [-i КЛЮЧ] ФАЙЛ ИМЯ@A:[ПУТЬ] | ИМЯ@A:ПУТЬ ФАЙЛ — копирование между компьютерами Debian (по паролю или ключу).
   Упрощения: known_hosts без хеширования имён; агент ssh-agent, сертификаты и scp -r не моделируются; ключ хоста ESR/Debian для клиента — ECDSA, MES — RSA. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, H = EL.hosts, E = EL.E;
  var B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
  function rnd(seed, n) {                     // детерминированная строка base64 длины n
    var o = '', h = 2166136261, i = 0, s = String(seed);
    while (o.length < n) { var x = s + '#' + (i++); for (var j = 0; j < x.length; j++) { h ^= x.charCodeAt(j); h = Math.imul(h, 16777619); }
      var v = h >>> 0; for (var k = 0; k < 5; k++) { o += B64.charAt(v & 63); v >>>= 6; } }
    return o.slice(0, n);
  }
  var ALG = { rsa: { name: 'ssh-rsa', up: 'RSA', pre: 'AAAAB3NzaC1yc2EAAAADAQABAAABgQ', len: 360, bits: 3072 },
              ecdsa: { name: 'ecdsa-sha2-nistp256', up: 'ECDSA', pre: 'AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBB', len: 88, bits: 256 },
              ed25519: { name: 'ssh-ed25519', up: 'ED25519', pre: 'AAAAC3NzaC1lZDI1NTE5AAAAI', len: 43, bits: 256 },
              dsa: { name: 'ssh-dss', up: 'DSA', pre: 'AAAAB3NzaC1kc3MAAACBA', len: 400, bits: 1024 } };
  function hkAlg(d) { return d.type === 'mes' ? 'rsa' : 'ecdsa'; }
  function hostKey(d, alg) {                  // ключ хоста устройства: меняется при новой генерации и у другого устройства с тем же адресом
    alg = alg || hkAlg(d); var g = ((d.st.hk || {})[alg]) || 0, seed = d.id + '|' + alg + '|' + g, a = ALG[alg];
    return { alg: alg, line: a.name + ' ' + a.pre + rnd(seed, a.len), fp: 'SHA256:' + rnd('fp' + seed, 43), up: a.up };
  }
  EL.hostKey = hostKey;
  function regen(st, alg) { st.hk = st.hk || {}; st.hk[alg] = (st.hk[alg] || 0) + 1; }
  function home(u) { return u === 'root' ? '/root' : '/home/' + u; }
  function tilde(line, u) { return line.replace(/(^|[\s=",'])~(?=\/|$|\s)/g, function (m, p) { return p + home(u); }); }
  function sshd(st) { var f = st.files['/etc/ssh/sshd_config'], o = { root: 'prohibit-password', pw: true, pub: true, port: 22 };
    String(f || '').split('\n').forEach(function (l) { var m = l.replace(/#.*/, '').trim().split(/\s+/); if (!m[0]) return;
      if (/^PermitRootLogin$/i.test(m[0])) o.root = m[1]; if (/^PasswordAuthentication$/i.test(m[0])) o.pw = m[1] !== 'no';
      if (/^PubkeyAuthentication$/i.test(m[0])) o.pub = m[1] !== 'no'; if (/^Port$/i.test(m[0])) o.port = +m[1] || 22; });
    return o; }
  var SSHD = 'Include /etc/ssh/sshd_config.d/*.conf\n\n#Port 22\n#ListenAddress 0.0.0.0\n\n#PermitRootLogin prohibit-password\n#PubkeyAuthentication yes\n' +
             '#AuthorizedKeysFile .ssh/authorized_keys\n\n#PasswordAuthentication yes\n\nUsePAM yes\nX11Forwarding yes\nPrintMotd no\nSubsystem sftp /usr/lib/openssh/sftp-server\n';
  function debHostFiles(d) { var f = d.st.files; if (d.st.hkInit) return; d.st.hkInit = true;
    if (f['/etc/ssh/sshd_config'] === undefined) f['/etc/ssh/sshd_config'] = SSHD; hkWrite(d); }
  function hkWrite(d) { var f = d.st.files; ['rsa', 'ecdsa', 'ed25519'].forEach(function (a) { var k = hostKey(d, a);
    f['/etc/ssh/ssh_host_' + a + '_key'] = privText(d.id + 'host' + a + ((d.st.hk || {})[a] || 0)); f['/etc/ssh/ssh_host_' + a + '_key.pub'] = k.line + ' root@' + d.st.host; }); }
  function privText(seed) { var b = rnd(seed, 280), o = ['-----BEGIN OPENSSH PRIVATE KEY-----']; for (var i = 0; i < b.length; i += 70) o.push(b.slice(i, i + 70)); o.push('-----END OPENSSH PRIVATE KEY-----'); return o.join('\n'); }
  function randomart(fp, label, bits) {      // «пьяный слон» по отпечатку
    var W = 17, Hh = 9, f = [], x = 8, y = 4, sym = ' .o+=*BOX@%&#/^';
    for (var i = 0; i < W * Hh; i++) f.push(0);
    for (var c = 0; c < fp.length; c++) { var v = B64.indexOf(fp.charAt(c)); if (v < 0) continue;
      for (var k = 0; k < 3; k++) { var b = (v >> (k * 2)) & 3; x = Math.max(0, Math.min(W - 1, x + (b & 1 ? 1 : -1))); y = Math.max(0, Math.min(Hh - 1, y + (b & 2 ? 1 : -1))); f[y * W + x]++; } }
    var top = '+---[' + label + ' ' + bits + ']'; while (top.length < W + 1) top += '-'; top += '+';
    var o = [top]; for (var r = 0; r < Hh; r++) { var s = '|'; for (var q = 0; q < W; q++) { var n = r * W + q;
      s += n === 4 * W + 8 ? 'S' : n === y * W + x ? 'E' : sym.charAt(Math.min(f[n], sym.length - 3)); } o.push(s + '|'); }
    o.push('+----[SHA256]-----+'); return o.join('\n');
  }

  // ---------------------------------------------------------------- known_hosts
  function hostTok(ip, port) { return port && port !== 22 ? '[' + ip + ']:' + port : ip; }
  function khFind(text, tok) { var L = String(text || '').split('\n'), r = null;
    L.forEach(function (l, i) { var w = l.trim().split(/\s+/); if (!w[0] || w[0].charAt(0) === '#') return;
      if (w[0].split(',').indexOf(tok) >= 0 && !r) r = { n: i + 1, line: w.slice(1, 3).join(' ') }; });
    return r; }
  function khDeb(st, file) { return { get: function () { return st.files[file]; }, file: file,
    add: function (l) { var t = st.files[file]; st.files[file] = (t && t.replace(/\n?$/, '\n') || '') + l + '\n'; } }; }
  function khEsr(st) { st.known = st.known || {}; return { get: function () { var o = st.known; return Object.keys(o).map(function (k) { return k + ' ' + o[k]; }).join('\n'); },
    file: 'known hosts', add: function (l) { var w = l.split(' '); st.known[w[0]] = w.slice(1).join(' '); } }; }
  function changed(tok, key, kh, hit, esr) {
    return ['@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', '@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @',
      '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', 'IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!',
      'Someone could be eavesdropping on you right now (man-in-the-middle attack)!', 'It is also possible that a host key has just been changed.',
      'The fingerprint for the ' + key.up + ' key sent by the remote host is', key.fp + '.', 'Please contact your system administrator.',
      'Add correct host key in ' + kh.file + ' to get rid of this message.', 'Offending ' + key.up + ' key in ' + kh.file + ':' + hit.n,
      esr ? '  remove with: clear ssh host ' + tok.replace(/^\[|\]:\d+$/g, '') : '  remove with:\n  ssh-keygen -f "' + kh.file + '" -R "' + tok + '"',
      key.up + ' host key for ' + tok + ' has changed and you have requested strict checking.', 'Host key verification failed.'].join('\n');
  }

  // ---------------------------------------------------------------- сессия SSH (hst — состояние клиента: Debian или держатель сессии ESR)
  // o: {port, ident: [файлы ключей], strict, kh, copy: файл .pub для ssh-copy-id, cfiles: файлы клиента}
  var so0 = P.sshOpen;                        // Reverse SSH на SCS (scs.js): ИМЯ:auxN@A
  P.sshOpen = function (hst, user, ip, o) {
    if (/:/.test(user)) return so0.apply(this, arguments);
    o = o || {}; var s = this, port = o.port || 22, src = hst.dev;
    var r = this.request(src, ip, 'tcp', port), tag = 'ssh: connect to host ' + ip + ' port ' + port + ': ';
    if (!r.ok) return tag + (r.why === 'Connection refused' ? 'Connection refused' : r.why === 'Request timed out' ? 'Connection timed out' : 'No route to host');
    var d = this.devs[r.dev || this.owner(ip)], st = d.st;
    if (d.type === 'deb') { debHostFiles(d); if (!st.files['/etc/ssh/ssh_host_ecdsa_key']) return 'kex_exchange_identification: read: Connection reset by peer\nConnection reset by ' + ip + ' port ' + port; }
    var on = d.type === 'esr' ? st.run.ssh : d.type === 'mes' ? st.ssh && st.rsa : d.type === 'deb' ? !!(st.svc || {}).ssh : false;
    if (!on) return tag + 'Connection refused';
    var key = hostKey(d), tok = hostTok(ip, port), kh = o.kh || khDeb(hst, home(hst.user || 'root') + '/.ssh/known_hosts'), hit = khFind(kh.get(), tok), out = [];
    var sess = { stage: 'auth', mode: 'priv', ctx: null, tries: 0, inner: null };
    if (hit && hit.line !== key.line.split(' ').slice(0, 2).join(' ')) return changed(tok, key, kh, hit, !!o.esr);
    function addKh() { kh.add(tok + ' ' + key.line.split(' ').slice(0, 2).join(' ')); return 'Warning: Permanently added \'' + tok + '\' (' + key.up + ') to the list of known hosts.'; }
    if (!hit) { if (o.strict === 'yes') return 'No ' + key.up + ' host key is known for ' + tok + ' and you have requested strict checking.\nHost key verification failed.';
      if (o.strict === 'no' || o.strict === 'accept-new') out.push(addKh()); else sess.stage = 'hk'; }
    // вход по ключу (Debian → Debian)
    var cfg = d.type === 'deb' ? sshd(st) : null, rootBad = d.type === 'deb' && user === 'root' && !/^yes$/i.test(cfg.root);
    if (d.type === 'deb' && !st.accounts[user]) rootBad = false;
    var pub = null;
    if (d.type === 'deb' && cfg.pub && o.cfiles) { var ak = String(st.files[home(user) + '/.ssh/authorized_keys'] || '');
      (o.ident || []).some(function (f) { var p = o.cfiles[f + '.pub']; if (!p || o.cfiles[f] === undefined) return false; var kp = p.split(/\s+/).slice(0, 2).join(' ');
        if (ak.split('\n').some(function (l) { return l.indexOf(kp) >= 0; })) { pub = f; return true; } return false; }); }
    var phrase = pub ? (hst.keyPass || {})[pub] : null;
    function pwPrompt() { return phrase ? 'Enter passphrase for key \'' + pub + '\': ' : user + '@' + ip + '\'s password: '; }
    function close(msg) { hst.ssh = null; return msg; }
    function denied() { return close(user + '@' + ip + ': Permission denied (publickey' + (d.type === 'deb' && !cfg.pw ? '' : ',password') + ').'); }
    function login() {
      sess.stage = 'cli';
      if (o.copy) return copyKey();
      if (o.after) return close(d.type === 'deb' ? o.after(st, user) : 'scp: на ' + ip + ' (' + d.model + ') нет командной оболочки Linux — копирование файлов по scp здесь не моделируется');
      if (d.type === 'esr') s.syslog(d.id, 'login.log', 'sshd: %AAA-I-LOGIN: user ' + user + ' logged in via ssh from ' + (s.ifaces(src)[0] || { ip: '?' }).ip);
      if (d.type === 'deb') return 'Linux ' + st.host + ' 5.10.0-23-amd64 #1 SMP Debian 5.10.179-1 x86_64\n\nLast login: from ' + ((s.ifaces(src)[0] || {}).ip || '?');
      var b = d.type === 'esr' ? st.run.banner : st.banner, x = []; if (b && b.login) x.push(b.login); if (b && b.exec) x.push(b.exec); return x.join('\n');
    }
    function copyKey() {
      if (d.type !== 'deb') return close('/usr/bin/ssh-copy-id: ERROR: на ' + ip + ' не командная оболочка Linux (' + d.model + ') — ключ не установлен, на ' + d.model + ' ключ задаётся в его CLI');
      var f = home(user) + '/.ssh/authorized_keys', cur = String(st.files[f] || ''), kp = o.copy.split(/\s+/).slice(0, 2).join(' ');
      if (cur.indexOf(kp) >= 0) return close('\n/usr/bin/ssh-copy-id: WARNING: All keys were skipped because they already exist on the remote system.\n\t\t(if you think this is a mistake, you may want to use -f option)');
      st.files[f] = (cur && cur.replace(/\n?$/, '\n') || '') + o.copy.trim() + '\n';
      return close('\nNumber of key(s) added: 1\n\nNow try logging into the machine, with:   "ssh ' + (port !== 22 ? "-p '" + port + "' " : '') + '\'' + user + '@' + ip + '\'"\nand check to make sure that only the key(s) you wanted were added.');
    }
    function pwOk(p) {
      if (d.type === 'deb') { if (rootBad || !cfg.pw) return false; return !!st.accounts[user] && st.accounts[user] === p; }
      var users = d.type === 'esr' ? st.run.users : st.users, u = users[user];
      var aa = s.aaaLogin ? s.aaaLogin(d.id, 'ssh', user, p, function (uu, pp) { var x = users[uu]; return !!x && x.pw === pp; }) : null;   // RADIUS/TACACS+ (aaa.js)
      return aa ? aa.ok : !!u && u.pw === p;
    }
    function afterHk() {                      // после проверки ключа хоста: ключ пользователя без фразы — сразу внутрь
      if (pub && !phrase) { var m = login(); return o.copy ? '' : m; }
      if (d.type === 'deb' && !pub && !cfg.pw) return denied();
      return null;
    }
    function swapCli(fn) { var m = st.mode, c = st.ctx; st.mode = sess.mode; st.ctx = sess.ctx; var r2 = fn(); sess.mode = st.mode; sess.ctx = st.ctx; st.mode = m; st.ctx = c; return r2; }
    function swapDeb(fn) { var u = st.user, z = st.ssh; st.user = user; st.ssh = sess.inner; try { return fn(); } finally { sess.inner = st.ssh; st.user = u; st.ssh = z; } }
    sess.prompt = function () {
      if (sess.stage === 'hk') return 'Are you sure you want to continue connecting (yes/no/[fingerprint])? ';
      if (sess.stage === 'auth') return pwPrompt();
      if (d.type === 'deb') return swapDeb(function () { return H.debPrompt(st); });
      return swapCli(function () { return d.type === 'esr' ? EL.esr.prompt(st) : EL.mes.prompt(st); });
    };
    sess.exec = function (line) {
      var l = String(line).trim();
      if (sess.stage === 'hk') {
        if (l === 'yes' || l === key.fp) { var w = addKh(); sess.stage = 'auth'; var a = afterHk(); return a === null ? w : w + (a ? '\n' + a : ''); }
        if (l === 'no') return close('Host key verification failed.');
        return 'Please type \'yes\', \'no\' or the fingerprint: ';
      }
      if (sess.stage === 'auth') {
        if (phrase) { if (l === phrase) return login(); sess.tries++; return sess.tries >= 3 ? denied() : ''; }
        if (pwOk(l)) return login();
        if (++sess.tries >= 3) return denied();
        return 'Permission denied, please try again.';
      }
      if (sess.inner || d.type === 'deb') {
        if (!sess.inner && /^(exit|logout)$/.test(l)) return close('logout\nConnection to ' + ip + ' closed.');
        return swapDeb(function () { return H.debExec(st, line); });
      }
      if (/^exit$/i.test(l) && (sess.mode === 'priv' || sess.mode === 'user')) return close('Connection to ' + ip + ' closed.');
      return swapCli(function () { return d.type === 'esr' ? EL.esr.exec(st, line) : EL.mes.exec(st, line); });
    };
    hst.ssh = sess;
    if (sess.stage === 'hk') return 'The authenticity of host \'' + tok + ' (' + ip + ')\' can\'t be established.\n' + key.up + ' key fingerprint is ' + key.fp + '.\nThis key is not known by any other names';
    var a2 = afterHk(); if (a2 !== null) out.push(a2);
    return out.join('\n');
  };

  // ---------------------------------------------------------------- Debian: ssh, ssh-keygen, ssh-copy-id, rm, служебное
  function args(t, val) { var o = { opt: {}, o: {}, pos: [] };
    for (var i = 1; i < t.length; i++) { var w = t[i];
      if (/^-[a-zA-Z]$/.test(w) && val.indexOf(w.charAt(1)) >= 0 && i + 1 < t.length) { if (w === '-o') { var m = t[++i].split('='); o.o[m[0]] = m.slice(1).join('='); } else o.opt[w.charAt(1)] = t[++i].replace(/^(["'])(.*)\1$/, '$2'); }
      else if (/^-[a-zA-Z]+$/.test(w)) w.slice(1).split('').forEach(function (c) { o.opt[c] = true; });
      else o.pos.push(w); }
    return o; }
  function idents(st) { var h = home(st.user); return ['id_ed25519', 'id_ecdsa', 'id_rsa'].map(function (n) { return h + '/.ssh/' + n; }); }
  function fpOf(pubLine) { return 'SHA256:' + rnd('fp' + pubLine.split(/\s+/).slice(0, 2).join(' '), 43); }
  function keygen(st, a) {
    var t = a.opt.t || 'rsa'; if (!ALG[t] || t === 'dsa') return 'unknown key type ' + t;
    var bits = +(a.opt.b || (t === 'rsa' ? 3072 : 256)), h = home(st.user), def = h + '/.ssh/id_' + t, file = a.opt.f, pass = a.opt.N, me = st.user + '@' + st.host;
    var q = { stage: file ? 'ow' : 'file' }, quiet = !!a.opt.q, head = quiet ? [] : ['Generating public/private ' + t + ' key pair.'];
    function finish() { st.ssh = null; var line = ALG[t].name + ' ' + ALG[t].pre + rnd(file + Math.random(), ALG[t].len) + ' ' + (a.opt.C || me);
      if (file.indexOf(h + '/.ssh/') === 0 && !Object.keys(st.files).some(function (k) { return k.indexOf(h + '/.ssh/') === 0; })) head.push('Created directory \'' + h + '/.ssh\'.');
      st.files[file] = privText(line); st.files[file + '.pub'] = line; st.keyPass = st.keyPass || {}; if (pass) st.keyPass[file] = pass; else delete st.keyPass[file];
      if (quiet) return head.join('\n');
      return head.concat(['Your identification has been saved in ' + file, 'Your public key has been saved in ' + file + '.pub', 'The key fingerprint is:', fpOf(line) + ' ' + (a.opt.C || me),
        'The key\'s randomart image is:', randomart(fpOf(line), ALG[t].up, bits)]).join('\n'); }
    function next() {
      if (q.stage === 'ow') { if (st.files[file] !== undefined) return null; q.stage = 'pw'; }
      if (q.stage === 'pw' && pass !== undefined) return finish();
      return null; }
    st.ssh = { prompt: function () { return q.stage === 'file' ? 'Enter file in which to save the key (' + def + '): ' : q.stage === 'ow' ? file + ' already exists.\nOverwrite (y/n)? '
        : q.stage === 'pw' ? 'Enter passphrase (empty for no passphrase): ' : 'Enter same passphrase again: '; },
      exec: function (line) { var l = String(line).trim(), r;
        if (q.stage === 'file') { file = tilde(l, st.user) || def; q.stage = 'ow'; head = []; r = next(); return r === null ? '' : r; }
        if (q.stage === 'ow') { if (!/^y/i.test(l)) { st.ssh = null; return ''; } q.stage = 'pw'; r = next(); return r === null ? '' : r; }
        if (q.stage === 'pw') { q.p1 = l; q.stage = 'pw2'; return ''; }
        if (l !== q.p1) { q.stage = 'pw'; return 'Passphrases do not match.  Try again.'; }
        pass = l; return finish(); } };
    if (!file) return head.join('\n');
    var r0 = next(); if (r0 !== null) return r0;
    return head.join('\n');
  }
  function khRemove(st, host, f) {
    var text = st.files[f]; if (text === undefined) return 'do_known_hosts: hostkeys_foreach failed for ' + f + ': No such file or directory';
    var L = text.split('\n'), keep = [], found = [];
    L.forEach(function (l, i) { var w = l.trim().split(/\s+/); if (w[0] && w[0].split(',').indexOf(host) >= 0) found.push(i + 1); else keep.push(l); });
    if (!found.length) return 'Host ' + host + ' not found in ' + f;
    st.files[f + '.old'] = text; st.files[f] = keep.join('\n');
    return found.map(function (n) { return '# Host ' + host + ' found: line ' + n; }).join('\n') + '\n' + f + ' updated.\nOriginal contents retained as ' + f + '.old';
  }
  var deb0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    if (!st.user || st.ssh || !st.net) return deb0.apply(this, arguments);
    var line = tilde(String(raw).trim(), st.user), t = line.split(/\s+/), c = t[0], a;
    if (c === 'ssh' && t.length > 1 && !/:/.test(t[t.length - 1].split('@')[0])) {
      a = args(t, 'pilo'); var tg = a.pos[0] || '', m = tg.match(/^(?:([^@]+)@)?(\d+\.\d+\.\d+\.\d+)$/); if (!m) return deb0.apply(this, arguments);
      var me = st.net.devs[st.dev]; debHostFiles(me);
      var kf = a.o.UserKnownHostsFile, kh = kf ? (kf === '/dev/null' ? { get: function () { return ''; }, add: function () {}, file: '/dev/null' } : khDeb(st, kf)) : null;
      return st.net.sshOpen(st, m[1] || a.opt.l || st.user, m[2], { port: +(a.opt.p || 22), ident: a.opt.i ? [a.opt.i.replace(/\.pub$/, '')] : idents(st), strict: a.o.StrictHostKeyChecking, kh: kh, cfiles: st.files });
    }
    if (c === 'scp') { a = args(t, 'Pi'); if (a.pos.length !== 2) return 'usage: scp [-P port] [-i identity_file] source ... target';
      var rs = function (x) { var m = x.match(/^(?:([^@:]+)@)?(\d+\.\d+\.\d+\.\d+):(.*)$/); return m ? { user: m[1] || st.user, ip: m[2], path: m[3] } : null; };
      var A = rs(a.pos[0]), B = rs(a.pos[1]); if (!!A === !!B) return 'scp: один из путей должен быть удалённым — ИМЯ@A.B.C.D:ПУТЬ';
      var R0 = A || B, put = !!B, abs = function (pth, u) { pth = String(pth || '').replace(/^~(\/|$)/, ''); return !pth || pth === '.' ? home(u) : pth.charAt(0) === '/' ? pth : home(u) + '/' + pth; };
      var lp = abs(put ? a.pos[0] : a.pos[1], st.user);
      if (put && st.files[lp] === undefined) return a.pos[0] + ': No such file or directory';
      var after = function (ts, u) {
        var isDir = function (F, x) { return Object.keys(F).some(function (k) { return k.indexOf(x.replace(/\/$/, '') + '/') === 0; }) || /\/$/.test(x); };
        var base = function (x) { return x.split('/').pop(); }, rp2 = abs(R0.path, u), src = put ? st.files : ts.files, dstF = put ? ts.files : st.files, from = put ? lp : rp2, to = put ? rp2 : lp;
        if (src[from] === undefined) return 'scp: ' + from + ': No such file or directory';
        if (isDir(dstF, to) || to === home(put ? u : st.user)) to = to.replace(/\/$/, '') + '/' + base(from);
        var who = put ? u : st.user; if (who !== 'root' && to.indexOf(home(who) + '/') !== 0 && to.indexOf('/tmp/') !== 0) return 'scp: ' + to + ': Permission denied';
        dstF[to] = src[from]; var sz = String(src[from]).length, nm = base(from); while (nm.length < 46) nm += ' ';
        return nm + '100%  ' + sz + '    ' + (sz / 1024 * 40).toFixed(1) + 'KB/s   00:00'; };
      return st.net.sshOpen(st, R0.user, R0.ip, { port: +(a.opt.P || 22), ident: a.opt.i ? [a.opt.i.replace(/\.pub$/, '')] : idents(st), cfiles: st.files, after: after }); }
    if (c === 'ssh-copy-id') { a = args(t, 'ip'); var m2 = (a.pos[0] || '').match(/^(?:([^@]+)@)?(\d+\.\d+\.\d+\.\d+)$/); if (!m2) return 'Usage: /usr/bin/ssh-copy-id [-i [identity_file]] [-p port] [user@]hostname';
      var pf = a.opt.i ? (/\.pub$/.test(a.opt.i) ? a.opt.i : a.opt.i + '.pub') : idents(st).map(function (x) { return x + '.pub'; }).filter(function (x) { return st.files[x] !== undefined; })[0];
      if (!pf || st.files[pf] === undefined) return '/usr/bin/ssh-copy-id: ERROR: No identities found';
      var head = '/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "' + pf + '"\n/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed\n' +
                 '/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys';
      var r = st.net.sshOpen(st, m2[1] || st.user, m2[2], { port: +(a.opt.p || 22), copy: st.files[pf], ident: [], cfiles: st.files });
      return head + (r ? '\n' + r : ''); }
    if (c === 'ssh-keygen') { a = args(t, 'fbtNCR');
      if (a.opt.R) return khRemove(st, a.opt.R, a.opt.f || home(st.user) + '/.ssh/known_hosts');
      if (a.opt.l) { var f = a.opt.f; if (!f) return 'Enter file in which the key is (' + home(st.user) + '/.ssh/id_rsa): '; var p = st.files[/\.pub$/.test(f) ? f : f + '.pub'];
        if (p === undefined) return f + ': No such file or directory'; var w = p.split(/\s+/), al = Object.keys(ALG).filter(function (k) { return ALG[k].name === w[0]; })[0] || 'rsa';
        return ALG[al].bits + ' ' + fpOf(p) + ' ' + (w[2] || 'no comment') + ' (' + ALG[al].up + ')'; }
      if (a.opt.A) { if (st.user !== 'root') return 'ssh-keygen: generating new host keys: Permission denied';
        var dd = st.net.devs[st.dev], miss = ['rsa', 'ecdsa', 'ed25519'].filter(function (k) { return st.files['/etc/ssh/ssh_host_' + k + '_key'] === undefined; });
        if (!miss.length) return ''; miss.forEach(function (k) { regen(st, k); }); hkWrite(dd); return 'ssh-keygen: generating new host keys: ' + miss.map(function (k) { return ALG[k].up; }).join(' '); }
      if (a.opt.f && st.user !== 'root' && a.opt.f.indexOf(home(st.user)) !== 0 && a.opt.f.indexOf('/tmp/') !== 0) return 'Saving key "' + a.opt.f + '" failed: Permission denied';
      return keygen(st, a); }
    if (c === 'dpkg-reconfigure' && t[1] === 'openssh-server') { if (st.user !== 'root') return 'dpkg-reconfigure: must be run as root';
      var d2 = st.net.devs[st.dev]; ['rsa', 'ecdsa', 'ed25519'].forEach(function (k) { regen(st, k); }); hkWrite(d2);
      return 'Creating SSH2 RSA key; this may take some time ...\nCreating SSH2 ECDSA key; this may take some time ...\nCreating SSH2 ED25519 key; this may take some time ...'; }
    if (c === 'rm' && t.length > 1) { var fs = t.slice(1).filter(function (x) { return !/^-/.test(x); }), force = t.some(function (x) { return /^-\w*f/.test(x); }), err = [];
      if (st.user !== 'root' && fs.some(function (x) { return x.indexOf(home(st.user)) !== 0 && x.indexOf('/tmp/') !== 0; })) return 'rm: cannot remove: Permission denied';
      fs.forEach(function (x) { var re = new RegExp('^' + x.replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '[^/]*') + '$'), hit = Object.keys(st.files).filter(function (k) { return re.test(k); });
        if (!hit.length && !force) err.push('rm: cannot remove \'' + x + '\': No such file or directory'); hit.forEach(function (k) { delete st.files[k]; }); });
      return err.join('\n'); }
    if ((c === 'mkdir' || c === 'chmod' || c === 'touch') && t.length > 1) { if (c === 'touch') t.slice(1).forEach(function (x) { if (st.files[x] === undefined) st.files[x] = ''; }); return ''; }
    if (/^(cat|nano|vi|vim|ls)$/.test(c) && /\/etc\/ssh/.test(line)) debHostFiles(st.net.devs[st.dev]);
    if (c === 'ls' && /\.ssh/.test(line)) { var dir = (t.filter(function (x, i) { return i > 0 && !/^-/.test(x); })[0] || '').replace(/\/$/, ''), L = Object.keys(st.files).filter(function (k) { return k.indexOf(dir + '/') === 0; })
      .map(function (k) { return k.slice(dir.length + 1); }).filter(function (k) { return k.indexOf('/') < 0; }).sort();
      return L.length ? L.join('  ') : (Object.keys(st.files).some(function (k) { return k.indexOf(dir) === 0; }) ? '' : 'ls: cannot access \'' + dir + '\': No such file or directory'); }
    return deb0.call(this, st, line === String(raw).trim() ? raw : line, ui);
  };

  // ---------------------------------------------------------------- ESR: сервер и клиент
  S.cmd('config', 'ip ssh port <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return 'Syntax error: Illegal parameter'; st.cand.sshPort = a[0] === 22 ? undefined : a[0]; st.pending = true; }, 'TCP-порт SSH-сервера');
  S.cmd('config', 'no ip ssh port', function (st) { delete st.cand.sshPort; st.pending = true; });
  S.RUNX.push(function (c, o) { if (c.sshPort) o.push('ip ssh port ' + c.sshPort); });
  EL.listensX = (function (lx0) { return function (d, proto, port) {
    if (d.type === 'esr' && proto === 'tcp' && d.st.run && d.st.run.sshPort) { if (port === d.st.run.sshPort) return !!d.st.run.ssh; if (port === 22) return false; }
    if (d.type === 'deb' && proto === 'tcp') { var c = sshd(d.st); if (c.port !== 22 && port === 22) return false; if (port === c.port && c.port !== 22) return !!(d.st.svc || {}).ssh; }
    return lx0 ? lx0(d, proto, port) : undefined; }; })(EL.listensX);
  ['rsa', 'ecdsa', 'ed25519', 'dsa'].forEach(function (k) {
    S.cmd('config', 'update ssh-host-key ' + k, function (st) { regen(st, k); }, 'Новая пара ключей хоста ' + ALG[k].up);
    if (k !== 'dsa') S.cmd('config', 'update ssh-host-key ' + k + ' <n>', function (st, a) { var ok = k === 'rsa' ? a[0] >= 1024 && a[0] <= 2048 : k === 'ecdsa' ? [256, 384, 521].indexOf(a[0]) >= 0 : a[0] >= 256 && a[0] <= 2048;
      if (!ok) return 'Syntax error: Illegal parameter'; regen(st, k); });
    S.cmd('priv', 'show crypto key mypubkey ' + k + (k === 'ecdsa' ? ' <n>' : ''), function (st) { var d = { id: devId(st), st: st, type: 'esr' }, w = hostKey(d, k).line.split(' ');
      var b = w[1], o = ['Key data', '------------------------------------------------------------', w[0]]; for (var i = 0; i < b.length; i += 60) o.push(b.slice(i, i + 60));
      o[o.length - 1] += ' root@' + st.run.host; return o.join('\n'); }, 'Открытый ключ хоста ' + ALG[k].up);
  });
  function devId(st) { var n = st.net; return n ? Object.keys(n.devs).filter(function (k) { return n.devs[k].st === st; })[0] : 'esr'; }
  function esrSsh(st, user, ip, port) { var n = st.net; if (!n) return '';
    var hold = { dev: devId(st), ssh: null }; st.sshc = hold;
    var r = n.sshOpen(hold, user, ip, { port: port, kh: khEsr(st), esr: true }); if (!hold.ssh) st.sshc = null; return r; }
  S.cmd('priv user', 'ssh <w> <ip>', function (st, a) { return esrSsh(st, a[0], a[1], 22); }, 'Подключиться по SSH');
  S.cmd('priv user', 'ssh <w> <ip> port <n>', function (st, a) { return esrSsh(st, a[0], a[1], a[2]); });
  S.cmd('priv', 'clear ssh host <ip>', function (st, a) { delete (st.known || {})[a[0]]; }, 'Забыть ключ SSH удалённого хоста');
  S.cmd('priv', 'clear ssh host <ip> port <n>', function (st, a) { delete (st.known || {})[hostTok(a[0], a[1])]; });
  var ex0 = P.exec, pr0 = P.prompt;
  P.exec = function (id, line) { var d = this.devs[id], h = d && d.type === 'esr' && d.st.sshc;
    if (h && h.ssh) { var r = h.ssh.exec(line); if (!h.ssh) d.st.sshc = null; this.gen++; return r; } return ex0.apply(this, arguments); };
  P.prompt = function (id) { var d = this.devs[id], h = d && d.type === 'esr' && d.st.sshc; return h && h.ssh ? h.ssh.prompt() : pr0.apply(this, arguments); };
  // MES: повторная crypto key generate rsa — новый ключ хоста
  (EL.mes.T || []).forEach(function (c) { if (c.pat.join(' ') !== 'crypto key generate rsa') return; var r0 = c.run;
    c.run = function (st) { if (st.rsa) regen(st, 'rsa'); return r0.apply(this, arguments); }; });
})(typeof window !== 'undefined' ? window : global);
