/* OpenVPN: удостоверяющий центр на Debian (easy-rsa 3, openvpn --genkey, openssl x509), сервер и клиент на ESR (справочник ESR-Series CLI 1.23),
   клиент на Debian (openvpn --config, systemctl start openvpn-client@ИМЯ).
   Debian: cd, pwd, cp [-r]; make-cadir ~/ca или cp -r /usr/share/easy-rsa ~/ca; в каталоге: ./easyrsa init-pki | build-ca [nopass] | gen-req ИМЯ [nopass] |
     sign-req server|client ИМЯ | build-server-full|build-client-full ИМЯ [nopass] | gen-dh | revoke ИМЯ | gen-crl; openvpn --genkey secret ta.key;
     openssl x509 -in Ф -noout -subject|-issuer|-text.
   ESR: copy tftp://A:/Ф crypto:cert|private-key|crl|dh|ta/ИМЯ;
     remote-access openvpn ИМЯ → (config-openvpn-server)#: network A/L, port N (1194), protocol udp|tcp, tunnel ip|ethernet, crypto ca|cert|private-key|dh|crl|ta ИМЯ,
       encryption algorithm, authentication algorithm, redirect-gateway, route A/L, dns-server A, client-isolation, duplicate-cn, client-max N, security-zone, enable;
       username CN → (config-openvpn-server-user)#: ip address A, subnet A/L (сеть за клиентом), enable;
     tunnel openvpn N → (config-openvpn)#: remote address A [port N], protocol, tunnel ip|ethernet, crypto ca|cert|private-key|ta ИМЯ, encryption algorithm,
       authentication algorithm, route-nopull, ip firewall disable, security-zone, enable.  show remote-access status openvpn, show tunnels status.
   Проверки при подключении (журнал — трасса и сообщения): связь с сервером по UDP/TCP, общий ключ ta (HMAC), сертификат сервера подписан CA клиента
   (и для Debian с remote-cert-tls server — это сертификат сервера), сертификат клиента подписан CA сервера, ключ подходит к сертификату, CRL,
   совпадение шифра, хеша и режима туннеля; адрес из network (или ip address пользователя), PUSH: route, redirect-gateway, dns-server.
   Упрощения: режим ethernet (L2) не моделируется; шифрование и сроки действия сертификатов не моделируются; Debian — только клиент. */
(function (G) {
  'use strict';
  var EL = G.EL, S = EL.esr, P = EL.Net.prototype, H = EL.hosts, IP = EL.ip;
  var B64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
  function b64e(s) { s = unescape(encodeURIComponent(s)); var o = '';
    for (var i = 0; i < s.length; i += 3) { var a = s.charCodeAt(i), b = s.charCodeAt(i + 1), c = s.charCodeAt(i + 2), n = (a << 16) | ((b || 0) << 8) | (c || 0);
      o += B64.charAt(n >> 18 & 63) + B64.charAt(n >> 12 & 63) + (isNaN(b) ? '=' : B64.charAt(n >> 6 & 63)) + (isNaN(c) ? '=' : B64.charAt(n & 63)); } return o; }
  function b64d(s) { s = String(s).replace(/[^A-Za-z0-9+/]/g, ''); var o = '';
    for (var i = 0; i < s.length; i += 4) { var n = (B64.indexOf(s[i]) << 18) | (B64.indexOf(s[i + 1]) << 12) | ((B64.indexOf(s[i + 2]) & 63) << 6) | (B64.indexOf(s[i + 3]) & 63);
      o += String.fromCharCode(n >> 16 & 255); if (s[i + 2]) o += String.fromCharCode(n >> 8 & 255); if (s[i + 3]) o += String.fromCharCode(n & 255); }
    try { return decodeURIComponent(escape(o)); } catch (e) { return ''; } }
  function pem(kind, obj) { var b = b64e(JSON.stringify(obj)), o = ['-----BEGIN ' + kind + '-----']; for (var i = 0; i < b.length; i += 64) o.push(b.slice(i, i + 64)); o.push('-----END ' + kind + '-----'); return o.join('\n') + '\n'; }
  function unpem(text) { var m = String(text || '').match(/-----BEGIN ([A-Z0-9 ]+)-----([\s\S]*?)-----END \1-----/); if (!m) return null;
    try { var o = JSON.parse(b64d(m[2])); o._kind = m[1]; return o; } catch (e) { return null; } }
  EL.unpem = unpem;
  var UID = 0; function uid() { UID++; return (Date.now().toString(36) + Math.random().toString(36).slice(2, 8) + UID).slice(-12); }
  function home(u) { return u === 'root' ? '/root' : '/home/' + u; }
  function cwd(st) { return st.cwd || home(st.user); }
  function norm(p) { var o = []; p.split('/').forEach(function (x) { if (!x || x === '.') return; if (x === '..') o.pop(); else o.push(x); }); return '/' + o.join('/'); }
  function abs(st, p) { p = String(p || ''); if (p === '~' || p.indexOf('~/') === 0) p = home(st.user) + p.slice(1); return norm(p.charAt(0) === '/' ? p : cwd(st) + '/' + p); }
  function isDir(st, p) { return Object.keys(st.files).some(function (k) { return k.indexOf(p + '/') === 0; }) || (st.dirs || {})[p]; }
  function mkdir(st, p) { st.dirs = st.dirs || {}; st.dirs[p] = true; }

  // ================================================================ Debian: cd, pwd, cp и относительные пути
  var REL = /^(cat|ls|nano|vi|vim|rm|touch|mkdir|chmod|head|tail|less|more)$/;
  // ---------------------------------------------------------------- easy-rsa
  function pkiOf(st) { return cwd(st) + '/pki'; }
  function haveEasy(st) { return st.files[cwd(st) + '/easyrsa'] !== undefined; }
  function F(st, p, v) { if (v !== undefined) st.files[p] = v; return st.files[p]; }
  function idx(st, pki) { return String(F(st, pki + '/index.txt') || '').split('\n').filter(Boolean).map(function (l) { var w = l.split('\t'); return { st: w[0], serial: w[1], cn: w[2] }; }); }
  function ask(st, qs, done) {            // последовательные вопросы: [{p, def, secret, check(v)→ошибка|null}]
    var ans = [], i = 0;
    st.ssh = { prompt: function () { return qs[i].p; }, exec: function (line) { var v = String(line).trim(); if (v === '' && qs[i].def !== undefined) v = qs[i].def;
      var err = qs[i].check ? qs[i].check(v, ans) : null; if (err === 'abort') { st.ssh = null; return '\nAborting without confirmation.'; }
      if (err) return err; ans.push(v); i++; if (i < qs.length) return ''; st.ssh = null; return done(ans); } };
    return null; }
  function chain(st, list, done) {        // вопросы по очереди; пустой список — сразу done
    if (!list.length) return done([]);
    var r = ask(st, list, done); return r === null ? '' : r; }
  function caPass(st, pki, qs) { var pp = (st.keyPass || {})[pki + '/private/ca.key']; if (pp) qs.push({ p: 'Enter pass phrase for ' + pki + '/private/ca.key:', check: function (v) { return v === pp ? null : 'unable to load CA private key\nEasy-RSA error:\n\nFailed to sign'; } }); }
  function newKey(st, path, cn) { var kid = uid(); F(st, path, pem('PRIVATE KEY', { kid: kid, cn: cn })); return kid; }
  function sign(st, pki, name, type) {
    var req = unpem(F(st, pki + '/reqs/' + name + '.req')), ca = unpem(F(st, pki + '/ca.crt'));
    var ser = ('0' + (parseInt(F(st, pki + '/serial') || '1', 16)).toString(16).toUpperCase()).slice(-2);
    F(st, pki + '/serial', ('0' + (parseInt(ser, 16) + 1).toString(16).toUpperCase()).slice(-2));
    F(st, pki + '/issued/' + name + '.crt', pem('CERTIFICATE', { cn: req.cn, type: type, serial: ser, issuer: ca.id, issuerCn: ca.cn, kid: req.kid }));
    F(st, pki + '/index.txt', (F(st, pki + '/index.txt') || '') + 'V\t' + ser + '\t' + req.cn + '\n');
    return ['Using configuration from ' + pki + '/easy-rsa-' + (100 + parseInt(ser, 16)) + '.tmp', 'Check that the request matches the signature', 'Signature ok',
      'The Subject\'s Distinguished Name is as follows', 'commonName            :ASN.1 12:\'' + req.cn + '\'', 'Certificate is to be certified until ' + until(825) + ' GMT (825 days)', '',
      'Write out database with 1 new entries', 'Data Base Updated', '', 'Certificate created at: ' + pki + '/issued/' + name + '.crt'].join('\n'); }
  function until(days) { var d = new Date(Date.now() + days * 864e5), M = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return M[d.getUTCMonth()] + ' ' + d.getUTCDate() + ' ' + d.toISOString().slice(11, 19) + ' ' + d.getUTCFullYear(); }
  var SSL = 'Using SSL: openssl OpenSSL 1.1.1n  15 Mar 2022';
  function genOut(kind) { return 'Generating a RSA private key\n.....+++++\n.....................+++++\nwriting new private key to \'' + kind + '\'\n-----'; }
  function easyrsa(st, w) {
    var pki = pkiOf(st), cmd = w[0], nopass = w.indexOf('nopass') >= 0, nm = w.filter(function (x, i) { return i > 0 && x !== 'nopass'; });
    var need = function () { return F(st, pki + '/.init') === undefined ? 'Easy-RSA error:\n\nEASYRSA_PKI does not exist (perhaps you need to run init-pki)?\nExpected to find the EASYRSA_PKI at: ' + pki + '\n\nRun easyrsa without commands for usage and command help.' : null; };
    var needCa = function () { return need() || (F(st, pki + '/ca.crt') === undefined ? 'Easy-RSA error:\n\nEASYRSA_PKI does not contain a CA (ca.crt) — run build-ca first.' : null); };
    if (!cmd) return 'Easy-RSA 3 usage and overview\n\nUSAGE: easyrsa [options] COMMAND [command-options]\n\nA list of commands is shown below:\n  init-pki\n  build-ca [ cmd-opts ]\n  gen-dh\n  gen-req <filename_base> [ cmd-opts ]\n  sign-req <type> <filename_base>\n  build-client-full <filename_base> [ cmd-opts ]\n  build-server-full <filename_base> [ cmd-opts ]\n  revoke <filename_base> [cmd-opts]\n  gen-crl';
    if (cmd === 'init-pki') { Object.keys(st.files).forEach(function (k) { if (k.indexOf(pki + '/') === 0) delete st.files[k]; });
      F(st, pki + '/.init', ''); ['private', 'reqs', 'issued'].forEach(function (d) { mkdir(st, pki + '/' + d); }); mkdir(st, pki);
      return '\ninit-pki complete; you may now create a CA or requests.\nYour newly created PKI dir is: ' + pki + '\n'; }
    if (cmd === 'build-ca') { var e = need(); if (e) return e; if (F(st, pki + '/ca.crt') !== undefined) return 'Easy-RSA error:\n\nUnable to create a CA as you already seem to have one set up.\nIf you intended to start a new CA, run init-pki first.';
      var qs = []; if (!nopass) qs.push({ p: 'Enter New CA Key Passphrase: ', check: function (v) { return v.length < 4 ? 'You must type in 4 to 1023 characters' : null; } }, { p: 'Re-Enter New CA Key Passphrase: ', check: function (v, a) { return v === a[0] ? null : 'Verify failure\nEasy-RSA error:\n\nFailed to build the CA'; } });
      qs.push({ p: 'Common Name (eg: your user, host, or server name) [Easy-RSA CA]:', def: 'Easy-RSA CA' });
      return SSL + '\n' + genOut(pki + '/private/ca.key') + '\nYou are about to be asked to enter information that will be incorporated\ninto your certificate request.\n-----\n' + chain(st, qs, function (a) {
        var cn = a[a.length - 1], kid = newKey(st, pki + '/private/ca.key', cn), id = uid(); if (!nopass) { st.keyPass = st.keyPass || {}; st.keyPass[pki + '/private/ca.key'] = a[0]; }
        F(st, pki + '/ca.crt', pem('CERTIFICATE', { cn: cn, type: 'ca', id: id, issuer: id, issuerCn: cn, kid: kid, serial: '00' })); F(st, pki + '/serial', '01'); F(st, pki + '/index.txt', '');
        return '\nCA creation complete and you may now import and sign cert requests.\nYour new CA certificate file for publishing is at:\n' + pki + '/ca.crt\n'; }); }
    if (cmd === 'gen-req') { var e2 = need(); if (e2) return e2; if (!nm[0]) return 'Easy-RSA error:\n\nError: gen-req must have a file base as the first argument.';
      if (F(st, pki + '/reqs/' + nm[0] + '.req') !== undefined) return 'Easy-RSA error:\n\nRequest file already exists. Aborting build to avoid overwriting this file.\nIf you wish to continue, please use a different name.\nConflicting file found at:\n* ' + pki + '/reqs/' + nm[0] + '.req';
      var q2 = []; if (!nopass) q2.push({ p: 'Enter PEM pass phrase:' }, { p: 'Verifying - Enter PEM pass phrase:', check: function (v, a) { return v === a[0] ? null : 'Verify failure'; } });
      q2.push({ p: 'Common Name (eg: your user, host, or server name) [' + nm[0] + ']:', def: nm[0] });
      return SSL + '\n' + genOut(pki + '/private/' + nm[0] + '.key') + '\n' + chain(st, q2, function (a) { var cn = a[a.length - 1], kid = newKey(st, pki + '/private/' + nm[0] + '.key', cn);
        if (!nopass) { st.keyPass = st.keyPass || {}; st.keyPass[pki + '/private/' + nm[0] + '.key'] = a[0]; }
        F(st, pki + '/reqs/' + nm[0] + '.req', pem('CERTIFICATE REQUEST', { cn: cn, kid: kid }));
        return '\nKeypair and certificate request completed. Your files are:\nreq: ' + pki + '/reqs/' + nm[0] + '.req\nkey: ' + pki + '/private/' + nm[0] + '.key\n'; }); }
    if (cmd === 'sign-req') { var e3 = needCa(); if (e3) return e3; var ty = nm[0], n2 = nm[1]; if (!/^(server|client)$/.test(ty || '')) return 'Easy-RSA error:\n\nUnknown cert type \'' + (ty || '') + '\'';
      if (F(st, pki + '/reqs/' + n2 + '.req') === undefined) return 'Easy-RSA error:\n\nNo request found for the input: \'' + n2 + '\'\nExpected to find the request at: ' + pki + '/reqs/' + n2 + '.req';
      if (F(st, pki + '/issued/' + n2 + '.crt') !== undefined) return 'Easy-RSA error:\n\nCannot sign this request for \'' + n2 + '\'.\nConflicting certificate already exists at:\n* ' + pki + '/issued/' + n2 + '.crt';
      var rq = unpem(F(st, pki + '/reqs/' + n2 + '.req')), q3 = [{ p: '  Confirm request details: ', check: function (v) { return v === 'yes' ? null : 'abort'; } }]; caPass(st, pki, q3);
      return SSL + '\n\n\nYou are about to sign the following certificate.\nPlease check over the details shown below for accuracy. Note that this request\nhas not been cryptographically verified. Please be sure it came from a trusted\nsource or that you have verified the request checksum with the sender.\n\nRequest subject, to be signed as a ' + ty + ' certificate for 825 days:\n\nsubject=\n    commonName                = ' + rq.cn + '\n\n\nType the word \'yes\' to continue, or any other input to abort.\n' +
        chain(st, q3, function () { return sign(st, pki, n2, ty); }); }
    if (cmd === 'build-server-full' || cmd === 'build-client-full') { var e4 = needCa(); if (e4) return e4; var ty2 = cmd.split('-')[1], n3 = nm[0];
      if (!n3) return 'Easy-RSA error:\n\nError: didn\'t find a file base name as the first argument.';
      if (F(st, pki + '/issued/' + n3 + '.crt') !== undefined || F(st, pki + '/reqs/' + n3 + '.req') !== undefined) return 'Easy-RSA error:\n\nRequest file already exists. Aborting build to avoid overwriting this file.\nConflicting file found at:\n* ' + pki + '/reqs/' + n3 + '.req';
      var q4 = []; if (!nopass) q4.push({ p: 'Enter PEM pass phrase:' }, { p: 'Verifying - Enter PEM pass phrase:', check: function (v, a) { return v === a[0] ? null : 'Verify failure'; } }); caPass(st, pki, q4);
      return SSL + '\n' + genOut(pki + '/private/' + n3 + '.key') + '\n' + chain(st, q4, function (a) { var kid = newKey(st, pki + '/private/' + n3 + '.key', n3);
        if (!nopass) { st.keyPass = st.keyPass || {}; st.keyPass[pki + '/private/' + n3 + '.key'] = a[0]; }
        F(st, pki + '/reqs/' + n3 + '.req', pem('CERTIFICATE REQUEST', { cn: n3, kid: kid })); return sign(st, pki, n3, ty2); }); }
    if (cmd === 'gen-dh') { var e5 = need(); if (e5) return e5; F(st, pki + '/dh.pem', pem('DH PARAMETERS', { dh: uid(), bits: 2048 }));
      return SSL + '\nGenerating DH parameters, 2048 bit long safe prime, generator 2\nThis is going to take a long time\n.......+.....+..........++*++*++*++*\n\nDH parameters of size 2048 created at ' + pki + '/dh.pem\n'; }
    if (cmd === 'revoke') { var e6 = needCa(); if (e6) return e6; var c6 = unpem(F(st, pki + '/issued/' + nm[0] + '.crt'));
      if (!c6) return 'Easy-RSA error:\n\nUnable to revoke as the input file is not a valid certificate. Unexpected\ninput in file: ' + pki + '/issued/' + nm[0] + '.crt';
      var q6 = [{ p: '  Continue with revocation: ', check: function (v) { return v === 'yes' ? null : 'abort'; } }]; caPass(st, pki, q6);
      return '\n\nPlease confirm you wish to revoke the certificate with the following subject:\n\nsubject=\n    commonName                = ' + c6.cn + '\n\n\nType the word \'yes\' to continue, or any other input to abort.\n' +
        chain(st, q6, function () { F(st, pki + '/index.txt', String(F(st, pki + '/index.txt')).replace('V\t' + c6.serial + '\t', 'R\t' + c6.serial + '\t'));
          return 'Using configuration from ' + pki + '/easy-rsa-revoke.tmp\nRevoking Certificate ' + c6.serial + '.\nData Base Updated\n\nIMPORTANT!!!\n\nRevocation was successful. You must run gen-crl and upload a CRL to your\ninfrastructure in order to prevent the revoked cert from being accepted.\n'; }); }
    if (cmd === 'gen-crl') { var e7 = needCa(); if (e7) return e7; var q7 = []; caPass(st, pki, q7);
      return chain(st, q7, function () { var ca = unpem(F(st, pki + '/ca.crt')); F(st, pki + '/crl.pem', pem('X509 CRL', { ca: ca.id, revoked: idx(st, pki).filter(function (x) { return x.st === 'R'; }).map(function (x) { return x.serial; }) }));
        return 'Using configuration from ' + pki + '/easy-rsa-crl.tmp\n\nAn updated CRL has been created.\nCRL file: ' + pki + '/crl.pem\n'; }); }
    return 'Easy-RSA error:\n\nUnknown command \'' + cmd + '\'. Run without commands for usage help.';
  }
  function x509(st, t) { var f = t[t.indexOf('-in') + 1], c = unpem(st.files[abs(st, f || '')]);
    if (t.indexOf('-in') < 0 || st.files[abs(st, f)] === undefined) return 'Can\'t open ' + (f || '') + ' for reading, No such file or directory';
    if (!c || c._kind !== 'CERTIFICATE') return 'unable to load certificate';
    var o = []; if (t.indexOf('-subject') >= 0) o.push('subject=CN = ' + c.cn); if (t.indexOf('-issuer') >= 0) o.push('issuer=CN = ' + c.issuerCn);
    if (t.indexOf('-serial') >= 0) o.push('serial=' + c.serial);
    if (t.indexOf('-text') >= 0) o.push('Certificate:', '    Data:', '        Version: 3 (0x2)', '        Serial Number: ' + c.serial, '        Signature Algorithm: sha256WithRSAEncryption',
      '        Issuer: CN = ' + c.issuerCn, '        Validity', '            Not After : ' + until(c.type === 'ca' ? 3650 : 825) + ' GMT', '        Subject: CN = ' + c.cn,
      '        X509v3 extensions:', '            X509v3 Basic Constraints: ', '                CA:' + (c.type === 'ca' ? 'TRUE' : 'FALSE'),
      '            X509v3 Extended Key Usage: ', '                ' + (c.type === 'server' ? 'TLS Web Server Authentication' : c.type === 'client' ? 'TLS Web Client Authentication' : '—'));
    return o.join('\n'); }

  // ================================================================ ESR: настройка
  var M = { ovs: '(config-openvpn-server)#', ovsu: '(config-openvpn-server-user)#', ovc: '(config-openvpn)#' };
  Object.keys(M).forEach(function (k) { S.PROMPT[k] = M[k]; });
  S.T.forEach(function (c) { if (c.pat.length === 1 && c.pat[0] === 'end') c.modes = c.modes.concat(Object.keys(M)); });
  function touch(st) { st.pending = true; }
  function bad() { return 'Syntax error: Illegal parameter'; }
  function O(c) { return c.ovpn || (c.ovpn = { srv: {}, cli: {} }); }
  function sv(st) { return O(st.cand).srv[st.ovS]; }
  function cl(st) { return O(st.cand).cli[st.ovC]; }
  function ob(st) { return st.mode === 'ovc' ? cl(st) : sv(st); }
  var ENC = ['des', 'blowfish128', 'aes128', 'des-ede', 'aes192', '3des', 'desx', 'aes256'];
  var AUTHS = 'md4 rsa-md4 md5 rsa-md5 mdc2 rsa-mdc2 sha sha1 rsa-sha rsa-sha1 rsa-sha1-2 dsa dsa-sha dsa-sha1 dsa-sha1-old ripemd160 rsa-ripemd160 ecdsa-with-sha1 sha-224 rsa-sha-224 sha-256 rsa-sha-256 sha-384 rsa-sha-384 sha-512 rsa-sha-512 whirlpool cleartext'.split(' ');
  S.cmd('config', 'remote-access openvpn <w>', function (st, a) { var L = O(st.cand).srv; if (!L[a[0]]) { L[a[0]] = { users: {}, routes: [], crypto: {} }; touch(st); } st.mode = 'ovs'; st.ovS = a[0]; }, 'Сервер OpenVPN');
  S.cmd('config', 'no remote-access openvpn <w>', function (st, a) { delete O(st.cand).srv[a[0]]; touch(st); });
  S.cmd('config', 'tunnel openvpn <n>', function (st, a) { if (a[0] < 1 || a[0] > 10) return bad(); var L = O(st.cand).cli; if (!L[a[0]]) { L[a[0]] = { crypto: {} }; touch(st); } st.mode = 'ovc'; st.ovC = a[0]; }, 'Клиент OpenVPN');
  S.cmd('config', 'no tunnel openvpn <n>', function (st, a) { delete O(st.cand).cli[a[0]]; touch(st); });
  S.cmd('ovs ovc', 'exit', function (st) { st.mode = 'config'; });
  S.cmd('ovsu', 'exit', function (st) { st.mode = 'ovs'; });
  S.cmd('ovs', 'network <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c || c.len < 16 || c.len > 29) return bad(); sv(st).net = IP.netOf(c.ip, c.len); touch(st); }, 'Сеть туннелей A/L (16..29)');
  S.cmd('ovs', 'port <n>', function (st, a) { if (a[0] < 1 || a[0] > 65535) return bad(); sv(st).port = a[0]; touch(st); }, 'Порт (1194)');
  S.cmd('ovs ovc', 'protocol <w>', function (st, a) { if (!/^(tcp|udp)$/.test(a[0])) return bad(); ob(st).proto = a[0]; touch(st); }, 'udp | tcp');
  S.cmd('ovs ovc', 'tunnel <w>', function (st, a) { if (!/^(ip|ethernet)$/.test(a[0])) return bad(); ob(st).tun = a[0]; touch(st); }, 'ip — точка-точка, ethernet — L2');
  ['ca', 'cert', 'private-key', 'dh', 'crl', 'ta'].forEach(function (k) {
    S.cmd(k === 'dh' || k === 'crl' ? 'ovs' : 'ovs ovc', 'crypto ' + k + ' <w>', function (st, a) { ob(st).crypto[k] = a[0]; touch(st); }, { ca: 'Сертификат CA', cert: 'Свой сертификат', 'private-key': 'Свой закрытый ключ', dh: 'Параметры Диффи-Хеллмана', crl: 'Список отозванных', ta: 'Ключ HMAC (tls-auth)' }[k]);
    S.cmd(k === 'dh' || k === 'crl' ? 'ovs' : 'ovs ovc', 'no crypto ' + k, function (st) { delete ob(st).crypto[k]; touch(st); }); });
  S.cmd('ovs ovc', 'encryption algorithm <w>', function (st, a) { if (ENC.indexOf(a[0]) < 0) return bad(); ob(st).enc = a[0]; touch(st); }, ENC.join(' | '));
  S.cmd('ovs ovc', 'no encryption algorithm', function (st) { delete ob(st).enc; touch(st); });
  S.cmd('ovs ovc', 'authentication algorithm <w>', function (st, a) { if (AUTHS.indexOf(a[0]) < 0) return bad(); ob(st).auth = a[0]; touch(st); }, 'Хеш HMAC: sha | sha-256 | md5 …');
  S.cmd('ovs ovc', 'no authentication algorithm', function (st) { delete ob(st).auth; touch(st); });
  S.cmd('ovs', 'redirect-gateway', function (st) { sv(st).redir = true; touch(st); }, 'Маршрут по умолчанию клиентам — в туннель');
  S.cmd('ovs', 'no redirect-gateway', function (st) { sv(st).redir = false; touch(st); });
  S.cmd('ovs', 'route <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return bad(); var n = IP.netOf(c.ip, c.len); if (sv(st).routes.indexOf(n) < 0) sv(st).routes.push(n); touch(st); }, 'Анонсировать клиентам сеть A/L');
  S.cmd('ovs', 'no route <w>', function (st, a) { var c = IP.parseCidr(a[0]); sv(st).routes = sv(st).routes.filter(function (x) { return !c || x !== IP.netOf(c.ip, c.len); }); touch(st); });
  S.cmd('ovs', 'dns-server <ip>', function (st, a) { sv(st).dns = a[0]; touch(st); }, 'DNS для клиентов');
  S.cmd('ovs', 'client-isolation', function (st) { sv(st).iso = true; touch(st); }, 'Запретить обмен между клиентами');
  S.cmd('ovs', 'no client-isolation', function (st) { sv(st).iso = false; touch(st); });
  S.cmd('ovs', 'duplicate-cn', function (st) { sv(st).dup = true; touch(st); }, 'Разрешить несколько клиентов с одним CN');
  S.cmd('ovs', 'no duplicate-cn', function (st) { sv(st).dup = false; touch(st); });
  S.cmd('ovs', 'client-max <n>', function (st, a) { sv(st).max = a[0]; touch(st); }, 'Максимум клиентов');
  S.cmd('ovs', 'username <w>', function (st, a) { var u = sv(st).users; u[a[0]] = u[a[0]] || { on: true }; st.ovU = a[0]; st.mode = 'ovsu'; touch(st); }, 'Настройки клиента по CN сертификата');
  S.cmd('ovs', 'no username <w>', function (st, a) { delete sv(st).users[a[0]]; touch(st); });
  S.cmd('ovsu', 'ip address <ip>', function (st, a) { sv(st).users[st.ovU].ip = a[0]; touch(st); }, 'Постоянный адрес клиента');
  S.cmd('ovsu', 'no ip address', function (st) { delete sv(st).users[st.ovU].ip; touch(st); });
  S.cmd('ovsu', 'subnet <w>', function (st, a) { var c = IP.parseCidr(a[0]); if (!c) return bad(); sv(st).users[st.ovU].subnet = IP.netOf(c.ip, c.len); touch(st); }, 'Сеть за клиентом A/L');
  S.cmd('ovsu', 'no subnet', function (st) { delete sv(st).users[st.ovU].subnet; touch(st); });
  S.cmd('ovsu', 'enable', function (st) { sv(st).users[st.ovU].on = true; touch(st); }, 'Разрешить клиента');
  S.cmd('ovsu', 'no enable', function (st) { sv(st).users[st.ovU].on = false; touch(st); });
  S.cmd('ovc', 'remote address <ip>', function (st, a) { cl(st).remote = a[0]; touch(st); }, 'Адрес сервера');
  S.cmd('ovc', 'remote address <ip> port <n>', function (st, a) { cl(st).remote = a[0]; cl(st).rport = a[1]; touch(st); });
  S.cmd('ovc', 'route-nopull', function (st) { cl(st).nopull = true; touch(st); }, 'Не принимать маршруты от сервера');
  S.cmd('ovc', 'no route-nopull', function (st) { cl(st).nopull = false; touch(st); });
  S.cmd('ovc', 'ip firewall disable', function (st) { cl(st).fwOff = true; touch(st); }, 'Не проверять межсетевым экраном');
  S.cmd('ovc', 'no ip firewall disable', function (st) { cl(st).fwOff = false; touch(st); });
  S.cmd('ovs ovc', 'security-zone <w>', function (st, a) { if (!(st.cand.zones || {})[a[0]]) return '% Зона ' + a[0] + ' не создана — security zone ' + a[0]; ob(st).zone = a[0]; touch(st); }, 'Зона безопасности');
  S.cmd('ovs ovc', 'no security-zone', function (st) { delete ob(st).zone; touch(st); });
  S.cmd('ovs ovc', 'description <rest>', function (st, a) { ob(st).desc = a[0].replace(/^"|"$/g, ''); touch(st); }, 'Описание');
  S.cmd('ovs ovc', 'enable', function (st) { ob(st).on = true; touch(st); }, 'Включить');
  S.cmd('ovs ovc', 'no enable', function (st) { ob(st).on = false; touch(st); });
  S.RUNX.push(function (c, out) { var x = c.ovpn; if (!x) return;
    function cr(o) { ['ca', 'cert', 'private-key', 'dh', 'crl', 'ta'].forEach(function (k) { if (o.crypto[k]) out.push('  crypto ' + k + ' ' + o.crypto[k]); }); }
    Object.keys(x.srv).sort().forEach(function (k) { var s = x.srv[k]; out.push('remote-access openvpn ' + k); if (s.desc) out.push('  description "' + s.desc + '"');
      if (s.zone) out.push('  security-zone ' + s.zone); if (s.net) out.push('  network ' + s.net); if (s.port) out.push('  port ' + s.port); if (s.proto) out.push('  protocol ' + s.proto);
      if (s.tun) out.push('  tunnel ' + s.tun); cr(s); if (s.enc) out.push('  encryption algorithm ' + s.enc); if (s.auth) out.push('  authentication algorithm ' + s.auth);
      if (s.redir) out.push('  redirect-gateway'); s.routes.forEach(function (r) { out.push('  route ' + r); }); if (s.dns) out.push('  dns-server ' + s.dns);
      if (s.iso) out.push('  client-isolation'); if (s.dup) out.push('  duplicate-cn'); if (s.max) out.push('  client-max ' + s.max);
      Object.keys(s.users).sort().forEach(function (u) { var y = s.users[u]; out.push('  username ' + u); if (y.ip) out.push('    ip address ' + y.ip); if (y.subnet) out.push('    subnet ' + y.subnet);
        if (!y.on) out.push('    no enable'); out.push('  exit'); });
      if (s.on) out.push('  enable'); out.push('exit'); });
    Object.keys(x.cli).sort().forEach(function (k) { var s = x.cli[k]; out.push('tunnel openvpn ' + k); if (s.desc) out.push('  description "' + s.desc + '"');
      if (s.fwOff) out.push('  ip firewall disable'); if (s.zone) out.push('  security-zone ' + s.zone); if (s.remote) out.push('  remote address ' + s.remote + (s.rport ? ' port ' + s.rport : ''));
      if (s.proto) out.push('  protocol ' + s.proto); if (s.tun) out.push('  tunnel ' + s.tun); cr(s); if (s.enc) out.push('  encryption algorithm ' + s.enc);
      if (s.auth) out.push('  authentication algorithm ' + s.auth); if (s.nopull) out.push('  route-nopull'); if (s.on) out.push('  enable'); out.push('exit'); }); });

  // ================================================================ подключение
  var CIPH = { des: 'DES-CBC', blowfish128: 'BF-CBC', aes128: 'AES-128-CBC', 'des-ede': 'DES-EDE-CBC', aes192: 'AES-192-CBC', '3des': 'DES-EDE3-CBC', desx: 'DESX-CBC', aes256: 'AES-256-CBC' };
  function cipherN(x) { if (!x) return 'none'; x = String(x).toLowerCase(); for (var k in CIPH) if (k === x || CIPH[k].toLowerCase() === x) return CIPH[k]; return x.toUpperCase(); }
  function authN(x) { if (!x) return 'SHA1'; x = String(x).toLowerCase().replace(/^rsa-/, '').replace(/-/g, ''); if (x === 'sha') x = 'sha1'; if (x === 'cleartext') return 'none'; return x.toUpperCase(); }
  function esrFile(d, kind, name) { var c = d.st.crypto || {}; return name ? (c[kind] || {})[name] : undefined; }
  function srvOf(net, dev) {            // нормализованные серверы ESR на устройстве
    var d = net.devs[dev]; if (!d || d.type !== 'esr' || d.sub === 'me' || d.off || !(d.st.run.ovpn)) return [];
    var x = d.st.run.ovpn.srv; return Object.keys(x).map(function (k) { var s = x[k], cr = s.crypto;
      var o = { dev: dev, name: k, s: s, port: s.port || 1194, proto: s.proto || 'udp', tun: s.tun || null, on: !!s.on,
        ca: unpem(esrFile(d, 'cert', cr.ca)), cert: unpem(esrFile(d, 'cert', cr.cert)), key: unpem(esrFile(d, 'private-key', cr['private-key'])), dh: unpem(esrFile(d, 'dh', cr.dh)),
        crl: cr.crl ? unpem(esrFile(d, 'crl', cr.crl)) : null, ta: cr.ta ? esrFile(d, 'ta', cr.ta) : null, enc: cipherN(s.enc), auth: authN(s.auth) };
      o.why = !s.net ? 'не задан network' : !s.tun ? 'не задан tunnel ip|ethernet' : ['ca', 'cert', 'private-key', 'dh'].map(function (q) { return !cr[q] ? 'не задан crypto ' + q : !(q === 'ca' ? o.ca : q === 'cert' ? o.cert : q === 'dh' ? o.dh : o.key) ? 'нет файла crypto:' + (q === 'ca' || q === 'cert' ? 'cert' : q) + '/' + cr[q] : null; }).filter(Boolean)[0] ||
        (cr.ta && !o.ta ? 'нет файла crypto:ta/' + cr.ta : null) || (cr.crl && !o.crl ? 'нет файла crypto:crl/' + cr.crl : null) || (o.cert.kid !== o.key.kid ? 'закрытый ключ не подходит к сертификату сервера' : null) || null;
      return o; }); }
  EL.listensX = (function (lx0) { return function (d, proto, port) {
    if (d.type === 'esr' && d.st.net && srvOf(d.st.net, d.id).some(function (o) { return o.on && !o.why && o.proto === proto && o.port === port; })) return true;
    return lx0 ? lx0(d, proto, port) : undefined; }; })(EL.listensX);
  // клиенты: ESR tunnel openvpn N и Debian (st.ovpnUp)
  function clients(net) { var o = [];
    Object.keys(net.devs).forEach(function (id) { var d = net.devs[id]; if (d.off) return;
      if (d.type === 'esr' && d.sub !== 'me' && d.st.run.ovpn) Object.keys(d.st.run.ovpn.cli).sort().forEach(function (k) { var x = d.st.run.ovpn.cli[k], cr = x.crypto;
        o.push({ dev: id, k: 'openvpn ' + k, ifn: 'openvpn' + k, on: !!x.on, remote: x.remote, port: x.rport || 1194, proto: x.proto || 'udp', tun: x.tun || 'ip', nopull: !!x.nopull,
          ca: unpem(esrFile(d, 'cert', cr.ca)), cert: unpem(esrFile(d, 'cert', cr.cert)), key: unpem(esrFile(d, 'private-key', cr['private-key'])), ta: cr.ta ? esrFile(d, 'ta', cr.ta) : null,
          enc: cipherN(x.enc), auth: authN(x.auth), fw: !x.fwOff, rct: false, ncp: false,
          miss: ['ca', 'cert', 'private-key'].map(function (q) { return !cr[q] ? 'не задан crypto ' + q : !esrFile(d, q === 'private-key' ? 'private-key' : 'cert', cr[q]) ? 'нет файла crypto:' + (q === 'private-key' ? 'private-key' : 'cert') + '/' + cr[q] : null; }).filter(Boolean)[0] ||
            (cr.ta && !esrFile(d, 'ta', cr.ta) ? 'нет файла crypto:ta/' + cr.ta : null) || (!x.remote ? 'не задан remote address' : null) }); });
      if (d.type === 'deb' && d.st.ovpnUp) Object.keys(d.st.ovpnUp).sort().forEach(function (k) { var x = d.st.ovpnUp[k]; o.push(Object.assign({ dev: id, k: k, on: true, fw: false }, x)); });
    }); return o; }
  function sameTa(a, b) { return String(a || '').replace(/\s+/g, '') === String(b || '').replace(/\s+/g, ''); }
  function connect(net, c, used) {
    var log = [], ol = [], me = net.devs[c.dev].name;
    function step(t) { log.push({ k: 'route', t: t }); }
    function fail(why, l) { log.push({ k: 'drop', t: why }); if (l) ol.push.apply(ol, l); return { err: why, log: log, ol: ol }; }
    if (!c.on) return fail(c.k + ' выключен (enable)');
    if (c.miss) return fail(me + ' ' + c.k + ': ' + c.miss, ['Options error: ' + c.miss]);
    if (c.tun === 'ethernet') return fail('tunnel ethernet (L2) в эмуляторе не моделируется — используйте tunnel ip / dev tun');
    if (c.key && c.cert && c.key.kid !== c.cert.kid) return fail(me + ': закрытый ключ клиента не подходит к его сертификату', ['Cannot load private key file: key values mismatch', 'Exiting due to fatal error']);
    ol.push('OpenVPN 2.5.1 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [MH/PKTINFO] [AEAD]', 'TCP/UDP: Preserving recently used remote address: [AF_INET]' + c.remote + ':' + c.port);
    step(me + ' → ' + c.remote + ':' + c.port + ' (' + c.proto.toUpperCase() + '): TLS-рукопожатие OpenVPN — P_CONTROL_HARD_RESET_CLIENT');
    var ct = [], f = net.send(c.dev, { src: null, dst: c.remote, proto: c.proto, dport: c.port, sport: 50111 }, log, ct);
    if (!f.ok) return fail('сервер ' + c.remote + ' недоступен', ['TLS Error: TLS key negotiation failed to occur within 60 seconds (check your network connectivity)', 'TLS Error: TLS handshake failed']);
    var S0 = srvOf(net, f.dev), s = S0.filter(function (o) { return o.port === c.port && o.proto === c.proto; })[0], sd = net.devs[f.dev], sn = sd.name;
    if (!s) { var other = S0[0]; return fail(sn + ': на ' + c.proto.toUpperCase() + ' ' + c.port + ' нет OpenVPN-сервера' + (other ? ' (сервер ' + other.name + ' слушает ' + other.proto.toUpperCase() + ' ' + other.port + ')' : ''),
      c.proto === 'tcp' ? ['TCP: connect to [AF_INET]' + c.remote + ':' + c.port + ' failed: Connection refused'] : ['TLS Error: TLS key negotiation failed to occur within 60 seconds (check your network connectivity)']); }
    if (!s.on) return fail(sn + ': remote-access openvpn ' + s.name + ' выключен (enable)', ['TLS Error: TLS key negotiation failed to occur within 60 seconds (check your network connectivity)']);
    if (s.why) return fail(sn + ': сервер ' + s.name + ' не запущен — ' + s.why, ['TLS Error: TLS key negotiation failed to occur within 60 seconds (check your network connectivity)']);
    var b = net.send(f.dev, { src: c.remote, dst: f.pk.src, proto: c.proto, reply: true, sport: c.port, rport: 50111 }, log, ct);
    if (!b.ok || b.dev !== c.dev) return fail('ответ ' + sn + ' не вернулся к ' + me, ['TLS Error: TLS key negotiation failed to occur within 60 seconds (check your network connectivity)']);
    if (!!s.ta !== !!c.ta || (s.ta && !sameTa(s.ta, c.ta))) return fail('tls-auth: ' + (!c.ta ? 'у сервера задан ключ ta, у клиента нет' : !s.ta ? 'у клиента задан ключ ta, у сервера нет' : 'ключи ta клиента и сервера разные') + ' — сервер молча отбрасывает пакеты (HMAC)',
      ['TLS Error: TLS key negotiation failed to occur within 60 seconds (check your network connectivity)', 'TLS Error: TLS handshake failed']);
    ol.push('TLS: Initial packet from [AF_INET]' + c.remote + ':' + c.port);
    if (s.ta) step('tls-auth: подпись HMAC ключом ta совпала');
    if (!c.ca || c.ca.type !== 'ca' || s.cert.issuer !== c.ca.id) return fail(me + ': сертификат сервера (CN=' + s.cert.cn + ') подписан не тем CA, что в crypto ca / ca клиента — VERIFY ERROR',
      ['VERIFY ERROR: depth=0, error=unable to get local issuer certificate: CN=' + s.cert.cn, 'OpenSSL: error:1416F086:SSL routines:tls_process_server_certificate:certificate verify failed', 'TLS_ERROR: BIO read tls_read_plaintext error', 'TLS Error: TLS handshake failed']);
    ol.push('VERIFY OK: depth=1, CN=' + c.ca.cn);
    if (c.rct && s.cert.type !== 'server') return fail(me + ': remote-cert-tls server — сертификат CN=' + s.cert.cn + ' выпущен не как серверный (sign-req server / build-server-full)',
      ['VERIFY KU ERROR', 'OpenSSL: error:1416F086:SSL routines:tls_process_server_certificate:certificate verify failed', 'TLS Error: TLS handshake failed']);
    ol.push('VERIFY OK: depth=0, CN=' + s.cert.cn);
    step(me + ': сертификат сервера CN=' + s.cert.cn + ' проверен по CA «' + c.ca.cn + '»');
    if (!c.cert) return fail(me + ': нет сертификата клиента', ['TLS Error: TLS handshake failed']);
    if (c.cert.issuer !== s.ca.id) return fail(sn + ': сертификат клиента CN=' + c.cert.cn + ' подписан не CA сервера (crypto ca) — сервер отклоняет', ['TLS Error: TLS handshake failed']);
    if (s.crl) { if (s.crl.ca !== s.ca.id) return fail(sn + ': CRL выпущен другим CA — проверка CRL не проходит, клиенты не принимаются', ['TLS Error: TLS handshake failed']);
      if (s.crl.revoked.indexOf(c.cert.serial) >= 0) return fail(sn + ': сертификат клиента CN=' + c.cert.cn + ' (serial ' + c.cert.serial + ') отозван — есть в CRL', ['TLS Error: TLS handshake failed']); }
    step(sn + ': сертификат клиента CN=' + c.cert.cn + ' проверен по CA «' + s.ca.cn + '»' + (s.crl ? ', в CRL его нет' : ''));
    ol.push('Control Channel: TLSv1.3, cipher TLSv1.3 TLS_AES_256_GCM_SHA384, peer certificate: 2048 bit RSA, signature: RSA-SHA256', '[' + s.cert.cn + '] Peer Connection Initiated with [AF_INET]' + c.remote + ':' + c.port);
    var u = s.s.users[c.cert.cn]; if (u && !u.on) return fail(sn + ': username ' + c.cert.cn + ' выключен (no enable)', ['AUTH: Received control message: AUTH_FAILED']);
    if ((s.tun || 'ip') !== c.tun) return fail('режим туннеля: у сервера tunnel ' + s.tun + ', у клиента ' + c.tun, ['WARNING: \'dev-type\' is used inconsistently']);
    var enc = c.ncp ? s.enc : c.enc;
    if (enc !== s.enc) return fail('шифрование: у сервера ' + s.enc + ', у клиента ' + c.enc + ' — пакеты данных не расшифровываются', ['Authenticate/Decrypt packet error: cipher final failed']);
    if (c.auth !== s.auth) return fail('хеш HMAC: у сервера ' + s.auth + ', у клиента ' + c.auth + ' — пакеты данных отбрасываются', ['Authenticate/Decrypt packet error: packet HMAC authentication failed']);
    var used2 = used[f.dev + '|' + s.name] || (used[f.dev + '|' + s.name] = { ips: {}, cn: {}, n: 0 });
    if (used2.cn[c.cert.cn] && !s.s.dup) return fail(sn + ': уже есть сессия с CN=' + c.cert.cn + ' — без duplicate-cn второй клиент с тем же сертификатом не пускается', ['AUTH: Received control message: AUTH_FAILED']);
    if (s.s.max && used2.n >= s.s.max) return fail(sn + ': достигнут client-max ' + s.s.max);
    var nw = s.s.net.split('/'), base = IP.ip2n(nw[0]), len = +nw[1], srvIp = IP.n2ip(base + 1), ip = u && u.ip ? u.ip : null;
    if (ip && (!IP.sameNet(ip, nw[0], len) || used2.ips[ip])) return fail(sn + ': ip address ' + ip + ' пользователя ' + c.cert.cn + ' вне network или занят');
    for (var n = base + 2; !ip && n < base + Math.pow(2, 32 - len) - 1; n++) { var a = IP.n2ip(n); if (!used2.ips[a] && !Object.keys(s.s.users).some(function (k) { return s.s.users[k].ip === a; })) ip = a; }
    if (!ip) return fail(sn + ': адреса в network ' + s.s.net + ' закончились');
    used2.ips[ip] = true; used2.cn[c.cert.cn] = true; used2.n++;
    var push = ['route-gateway ' + srvIp, 'topology subnet', 'ifconfig ' + ip + ' ' + IP.len2mask(len)].concat(s.s.routes.map(function (r) { var p = r.split('/'); return 'route ' + p[0] + ' ' + IP.len2mask(+p[1]); }));
    if (s.s.redir) push.unshift('redirect-gateway def1'); if (s.s.dns) push.push('dhcp-option DNS ' + s.s.dns);
    ol.push('SENT CONTROL [' + s.cert.cn + ']: \'PUSH_REQUEST\' (status=1)', 'PUSH: Received control message: \'PUSH_REPLY,' + push.join(',') + '\'', 'Data Channel: cipher \'' + enc + '\', auth \'' + s.auth + '\'',
      'TUN/TAP device ' + (c.dev && net.devs[c.dev].type === 'deb' ? 'tun0' : c.ifn) + ' opened', 'net_addr_v4_add: ' + ip + '/' + len, 'Initialization Sequence Completed');
    step('PUSH_REPLY: адрес ' + ip + '/' + len + ', шлюз ' + srvIp + (c.nopull ? ' (route-nopull — маршруты сервера не приняты)' : (s.s.routes.length ? ', маршруты ' + s.s.routes.join(', ') : '') + (s.s.redir ? ', маршрут по умолчанию — в туннель' : '')));
    step(c.k + ' поднят: ' + ip + ', шифр ' + enc + ', HMAC ' + s.auth);
    return { ok: true, srv: f.dev, prof: s.name, cn: c.cert.cn, ip: ip, len: len, gw: srvIp, out: c.remote, cip: f.pk.src, port: c.port, proto: c.proto,
      routes: c.nopull ? [] : s.s.routes.slice(), redir: !c.nopull && !!s.s.redir, iroute: u && u.subnet || null, iso: !!s.s.iso, enc: enc, log: log, ol: ol,
      nh: (net.lookup(c.dev, c.remote) || {}).nh, uifn: ((net.lookup(c.dev, c.remote) || {}).iface || {}).name };
  }
  P.ovSess = function () {
    if (this._ov && this._ov.gen === this.gen && this._ov.now === this.now) return this._ov.t;
    if (this._ovBusy) return {};
    var s = this, t = {}, used = {}; this._ovBusy = true;
    try { clients(this).forEach(function (c) { var kick = (s._ovKick || {})[c.dev + '|' + c.k]; (t[c.dev] = t[c.dev] || {})[c.k] = kick && s.now < kick ? { err: 'сессия разорвана сервером', log: [], ol: [] } : Object.assign(connect(s, c, used), { c: c }); }); }
    finally { this._ovBusy = false; }
    this._ov = { gen: this.gen, now: this.now, t: t }; return t;
  };
  function ok(net) { var t = net.ovSess(), o = []; Object.keys(t).forEach(function (id) { Object.keys(t[id]).forEach(function (k) { if (t[id][k].ok) o.push({ cli: id, k: k, x: t[id][k] }); }); }); return o; }
  function cliIf(e, net) { return net.devs[e.cli].type === 'deb' ? (e.x.c.ifn || 'tun0') : 'openvpn' + e.k.split(' ')[1]; }
  function srvIf(e) { return 'openvpn-' + e.x.prof; }

  var if0 = P.ifaces;
  P.ifaces = function (id) { var o = if0.apply(this, arguments); if (this._ovBusy) return o; var s = this, done = {};
    ok(this).forEach(function (e) {
      if (e.cli === id) o.push({ name: cliIf(e, s), ip: e.x.ip, len: e.x.len, port: null, tag: null, tun: 'ovpn', ov: e, fw: e.x.c.fw });
      if (e.x.srv === id && !done[e.x.prof]) { done[e.x.prof] = true; o.push({ name: srvIf(e), ip: e.x.gw, len: e.x.len, port: null, tag: null, tun: 'ovpn', ovs: e.x.prof, fw: true }); } });
    return o; };
  var rt0 = P.routes;
  P.routes = function (id) { var o = rt0.apply(this, arguments); if (this._ovBusy) return o; var s = this;
    ok(this).forEach(function (e) {
      if (e.cli === id) { var nm = cliIf(e, s); e.x.routes.forEach(function (r) { o.push({ p: 'S', net: r, len: +r.split('/')[1], nh: e.x.gw, ifn: nm, ad: 1, m: 0, vrf: null }); });
        if (e.x.redir) { o.unshift({ p: 'S', net: '0.0.0.0/0', len: 0, nh: e.x.gw, ifn: nm, ad: 1, m: 0, vrf: null }); if (e.x.uifn) o.push({ p: 'S', net: e.x.out + '/32', len: 32, nh: e.x.nh, ifn: e.x.uifn, ad: 1, m: 0, vrf: null }); } }
      if (e.x.srv === id && e.x.iroute) o.push({ p: 'S', net: e.x.iroute, len: +e.x.iroute.split('/')[1], nh: e.x.ip, ifn: srvIf(e), ad: 1, m: 0, vrf: null }); });
    return o; };
  var z0 = EL.fwZoneOf;
  EL.fwZoneOf = function (c, ifname) { var n = String(ifname), m = n.match(/^openvpn(\d+)$/), q = n.match(/^openvpn-(.+)$/);
    if (m && c.ovpn && c.ovpn.cli[m[1]]) return c.ovpn.cli[m[1]].zone || null; if (q && c.ovpn && c.ovpn.srv[q[1]]) return c.ovpn.srv[q[1]].zone || null; return z0(c, ifname); };
  var tun0 = P.tunnel;
  P.tunnel = function (cur, r, pk, steps, ct) { var f0 = r.iface; if (!f0.ov && !f0.ovs) return tun0.apply(this, arguments);
    var s = this, me = this.devs[cur].name, e, toSrv = !!f0.ov;
    if (toSrv) e = f0.ov;
    else { var L = ok(this).filter(function (x) { return x.x.srv === cur && x.x.prof === f0.ovs; });
      e = L.filter(function (x) { return x.x.ip === pk.dst; })[0] || L.filter(function (x) { return x.x.iroute && IP.sameNet(pk.dst, x.x.iroute.split('/')[0], +x.x.iroute.split('/')[1]); })[0];
      if (!e) { steps.push({ k: 'drop', t: me + ': ' + f0.name + ' — нет подключённого клиента OpenVPN с адресом ' + pk.dst + ' (или с subnet, куда входит этот адрес)' }); return { ok: false }; } }
    var peer = toSrv ? e.x.srv : e.cli, src = toSrv ? e.x.cip : e.x.out, dst = toSrv ? e.x.out : e.x.cip;
    steps.push({ k: 'route', t: me + ': ' + f0.name + ' — пакет ' + pk.src + ' → ' + pk.dst + ' зашифрован (' + e.x.enc + ') и упакован в ' + e.x.proto.toUpperCase() + ', внешний заголовок ' + src + ' → ' + dst + ':' + (toSrv ? e.x.port : 50111) });
    var outer = { src: src, dst: dst, proto: e.x.proto, dport: toSrv ? e.x.port : 50111, sport: toSrv ? 50111 : e.x.port, inner: { src: pk.src, dst: pk.dst, proto: pk.proto, reply: !!pk.reply } };
    var o, bs = this._ovBusy; this._ovBusy = true; try { o = this.send(cur, outer, steps, ct); } finally { this._ovBusy = bs; }
    if (!o.ok || o.dev !== peer) { steps.push({ k: 'drop', t: 'пакет OpenVPN не дошёл до ' + this.devs[peer].name }); return { ok: false }; }
    var pf = this.ifaces(peer).filter(function (q) { return toSrv ? q.ovs === e.x.prof : (q.ov && q.ov.k === e.k); })[0];
    if (toSrv && e.x.iso && ok(this).some(function (x) { return x.x.srv === peer && x.x.prof === e.x.prof && x.x.ip === pk.dst; })) {
      steps.push({ k: 'drop', t: this.devs[peer].name + ': client-isolation — обмен между клиентами OpenVPN запрещён' }); return { ok: false }; }
    steps.push({ k: 'route', t: this.devs[peer].name + ': ' + pf.name + ' — расшифровано, внутри ' + pk.src + ' → ' + pk.dst });
    if (this.devs[peer].type === 'esr') { var fw = this.fwPass(peer, pf, pk, ct, { src: pk.src, dst: pk.dst }); if (fw.t) steps.push({ k: fw.ok ? 'route' : 'drop', t: fw.t }); if (!fw.ok) return { ok: false }; }
    void s; return { ok: true, dev: peer, ip: pf.ip, inIf: pf };
  };

  // ================================================================ ESR: show и события
  function rp(x, n) { x = String(x); while (x.length < n) x += ' '; return x; }
  function meOf(st) { var n = st.net; return n ? Object.keys(n.devs).filter(function (k) { return n.devs[k].st === st; })[0] : null; }
  var rs = S.T.filter(function (c) { return c.pat.join(' ') === 'show remote-access status <w>'; })[0];
  if (rs) { var rs0 = rs.run; rs.run = function (st, a) { if (a[0] !== 'openvpn') return rs0.apply(this, arguments); var n = st.net, me = meOf(st);
    var L = n ? ok(n).filter(function (e) { return e.x.srv === me; }) : [];
    return ['User               IP-address       Server', '----------------   ---------------  --------------------------------------'].concat(L.map(function (e) { return rp(e.x.cn, 19) + rp(e.x.ip, 17) + 'openvpn(' + e.x.prof + ')'; }), ['Count sessions: ' + L.length]).join('\n'); }; }
  var tst = S.T.filter(function (c) { return c.pat.join(' ') === 'show tunnels status'; })[0];
  if (tst) { var run0 = tst.run; tst.run = function (st) { var out = run0.apply(this, arguments), n = st.net; if (!n || !st.run.ovpn) return out;
    var t = n.ovSess()[meOf(st)] || {};
    Object.keys(st.run.ovpn.cli).sort().forEach(function (k) { var x = st.run.ovpn.cli[k], e = t['openvpn ' + k] || {};
      out += '\n' + rp('openvpn ' + k, 11) + rp(e.ok ? 'Up' : 'Down', 18) + rp('1500', 9) + rp(e.ok ? e.ip : '--', 19) + rp(x.remote || '--', 19) + (e.ok ? 'connected' : (e.err || '--')); });
    return out; }; }
  S.cmd('priv', 'clear remote-access session openvpn', function (st) { var n = st.net, me = meOf(st), K = n._ovKick || (n._ovKick = {});
    ok(n).filter(function (e) { return e.x.srv === me; }).forEach(function (e) { K[e.cli + '|' + e.k] = n.now + 30; }); n.gen++; }, 'Разорвать сессии OpenVPN');
  EL.evX.push({
    snap: function (s, o) { var t = s.ovSess(); Object.keys(t).forEach(function (id) { Object.keys(t[id]).forEach(function (k) { var e = t[id][k]; o['OV|' + id + '|' + k] = e.ok ? 'Up ' + e.ip : 'Down ' + e.err; }); }); },
    ev: function (q, a, b, s) { if (q[0] !== 'OV' || !b) return null; var up = /^Up/.test(b), was = /^Up/.test(a || ''); if (!up && !was && a !== undefined) return null;
      var e = (s.ovSess()[q[1]] || {})[q[2]]; if (e && s.onTrace) { try { s.onTrace({ ok: !!e.ok, steps: e.log || [] }, q[1], q[2]); } catch (x) { void x; } }
      return { k: 'ovpn', msg: q[2] + ': ' + (up ? 'соединение установлено, адрес ' + b.slice(3) : was ? 'соединение разорвано — ' + b.slice(5) : 'не удалось подключиться — ' + b.slice(5)) }; } });

  // ================================================================ Debian: клиент OpenVPN
  function inline(text, tag) { var m = String(text).match(new RegExp('<' + tag + '>([\\s\\S]*?)</' + tag + '>')); return m ? m[1] : null; }
  function parseCli(st, f) {
    var text = st.files[f], o = { opt: {} }, dir = f.replace(/\/[^/]*$/, ''); if (text === undefined) return { err: 'Options error: In [CMD-LINE]:1: Error opening configuration file: ' + f };
    var body = String(text).replace(/<(ca|cert|key|tls-auth|tls-crypt)>[\s\S]*?<\/\1>/g, '');
    body.split('\n').forEach(function (l) { l = l.replace(/[#;].*/, '').trim(); if (!l) return; var w = l.split(/\s+/); o.opt[w[0]] = w.slice(1); });
    function file(k) { var inl = inline(text, k); if (inl !== null) return inl; var v = o.opt[k]; if (!v) return null; var p = v[0].charAt(0) === '/' ? v[0] : dir + '/' + v[0]; return st.files[p] === undefined ? { missing: p } : st.files[p]; }
    if (!o.opt.client && !o.opt.remote) return { err: 'Options error: в конфигурации нет client / remote — эмулятор поддерживает OpenVPN-клиент' };
    var rm = o.opt.remote || []; if (!rm[0]) return { err: 'Options error: нет remote A [порт]' };
    var r = { remote: rm[0], port: +(rm[1] || (o.opt.port || [])[0] || 1194), proto: ((o.opt.proto || ['udp'])[0]).replace(/-client$/, ''), tun: /^tap/.test((o.opt.dev || ['tun'])[0]) ? 'ethernet' : 'ip',
      ifn: (o.opt.dev || ['tun'])[0].replace(/^tun$/, 'tun0').replace(/^tap$/, 'tap0'), nopull: !!o.opt['route-nopull'], rct: (o.opt['remote-cert-tls'] || [])[0] === 'server' };
    var miss = null; ['ca', 'cert', 'key'].forEach(function (k) { var v = file(k); if (v === null) miss = miss || 'не задан ' + k; else if (v.missing) miss = miss || 'нет файла ' + v.missing; else r[k === 'key' ? 'key' : k] = unpem(v); });
    var ta = file('tls-auth') || file('tls-crypt'); if (ta && ta.missing) miss = miss || 'нет файла ' + ta.missing; else r.ta = ta;
    r.miss = miss; var ci = (o.opt.cipher || [])[0]; r.ncp = !ci; r.enc = cipherN(ci || 'aes256'); r.auth = authN((o.opt.auth || [])[0]);
    return r; }
  function ovUp(st, f, name) {
    if (st.user !== 'root') return 'ERROR: Cannot open TUN/TAP dev /dev/net/tun: Permission denied (errno=13)';
    var r = parseCli(st, f); if (r.err) return r.err;
    st.ovpnUp = st.ovpnUp || {}; var k = name || 'openvpn'; st.ovpnUp[k] = Object.assign(r, { k: k }); st.net.gen++;
    var e = (st.net.ovSess()[st.net.order.filter(function (id) { return st.net.devs[id].st === st; })[0]] || {})[k] || {};
    return e.ol ? e.ol.join('\n') : ''; }
  function ovEntry(st, k) { var id = Object.keys(st.net.devs).filter(function (x) { return st.net.devs[x].st === st; })[0]; return (st.net.ovSess()[id] || {})[k] || null; }
  function sh(raw, st) {                  // относительные пути и ~ для файловых команд
    var t = String(raw).trim().split(/\s+/); if (!REL.test(t[0])) return raw;
    var any = false; for (var i = 1; i < t.length; i++) if (!/^-/.test(t[i]) && t[i].charAt(0) !== '/' && !/^\d+$|^[ugoa]*[+=-][rwxXst]+$/.test(t[i])) { t[i] = abs(st, t[i]); any = true; }
    if (t[0] === 'ls' && t.filter(function (x, j) { return j > 0 && !/^-/.test(x); }).length === 0 && st.cwd) { t.push(st.cwd); any = true; }
    return any ? t.join(' ') : raw; }
  var deb0 = H.debExec;
  H.debExec = function (st, raw, ui) {
    if (!st.user || st.ssh || !st.net) return deb0.apply(this, arguments);
    var line = String(raw).trim(), t = line.split(/\s+/), c = t[0];
    if (c === 'cd') { var to = t[1] ? abs(st, t[1]) : home(st.user); if (to !== '/' && !isDir(st, to) && to !== home(st.user)) return '-bash: cd: ' + t[1] + ': No such file or directory';
      st.cwd = to === home(st.user) ? null : to; return ''; }
    if (c === 'pwd') return cwd(st);
    if (c === 'make-cadir' && t[1]) { var dd = abs(st, t[1]); if (isDir(st, dd)) return 'mkdir: cannot create directory \'' + t[1] + '\': File exists';
      F(st, dd + '/easyrsa', '#!/bin/sh\n# Easy-RSA 3'); F(st, dd + '/vars', '# Easy-RSA 3 vars file\n#set_var EASYRSA_KEY_SIZE 2048\n'); return ''; }
    if (c === 'cp' && t.length >= 3) { var rec = t.indexOf('-r') > 0 || t.indexOf('-a') > 0, args = t.slice(1).filter(function (x) { return !/^-/.test(x); }), from = abs(st, args[0]), dst = abs(st, args[1]);
      if (from === '/usr/share/easy-rsa' || from === '/usr/share/easy-rsa/') { if (!rec) return 'cp: -r not specified; omitting directory \'' + args[0] + '\''; var tgt = isDir(st, dst) ? dst + '/easy-rsa' : dst;
        F(st, tgt + '/easyrsa', '#!/bin/sh\n# Easy-RSA 3'); F(st, tgt + '/vars.example', '#set_var EASYRSA_KEY_SIZE 2048\n'); return ''; }
      if (!/^\/(tmp|home|root|tftp|etc\/openvpn)/.test(dst) && st.user !== 'root') return 'cp: cannot create regular file \'' + args[1] + '\': Permission denied';
      if (st.files[from] === undefined) return isDir(st, from) ? (rec ? (function () { Object.keys(st.files).filter(function (k) { return k.indexOf(from + '/') === 0; }).forEach(function (k) { st.files[(isDir(st, dst) ? dst + '/' + from.split('/').pop() : dst) + k.slice(from.length)] = st.files[k]; }); return ''; })() : 'cp: -r not specified; omitting directory \'' + args[0] + '\'')
        : 'cp: cannot stat \'' + args[0] + '\': No such file or directory';
      st.files[isDir(st, dst) || /\/$/.test(args[1]) ? dst + '/' + from.split('/').pop() : dst] = st.files[from]; return ''; }
    if ((c === './easyrsa' || c === 'easyrsa' || /\/easyrsa$/.test(c))) { if (c === './easyrsa' && !haveEasy(st)) return '-bash: ./easyrsa: No such file or directory'; return easyrsa(st, t.slice(1)); }
    if (c === 'openvpn' && t[1] === '--genkey') { var fn = t[t.length - 1]; if (fn === '--genkey' || fn === 'secret' || fn === '--secret') return 'Options error: --genkey: нужен файл';
      F(st, abs(st, fn), '#\n# 2048 bit OpenVPN static key\n#\n-----BEGIN OpenVPN Static key V1-----\n' + (function () { var o = []; for (var i = 0; i < 16; i++) o.push(Math.random().toString(16).slice(2, 10) + Math.random().toString(16).slice(2, 10) + Math.random().toString(16).slice(2, 10) + Math.random().toString(16).slice(2, 10)); return o.join('\n'); })() + '\n-----END OpenVPN Static key V1-----\n');
      return /^--genkey$/.test(t[1]) && t[2] === '--secret' ? 'WARNING: Using --genkey --secret filename is DEPRECATED.  Use --genkey secret filename instead.' : ''; }
    if (c === 'openvpn' && t.indexOf('--config') > 0) { var cf = abs(st, t[t.indexOf('--config') + 1]); return ovUp(st, cf, 'openvpn'); }
    var sc = line.match(/^systemctl\s+(start|stop|restart|status)\s+openvpn-client@(\w+)(\.service)?$/);
    if (sc) { var k = 'openvpn-client@' + sc[2]; st.ovpnUp = st.ovpnUp || {};
      if (sc[1] === 'stop' || sc[1] === 'restart') { delete st.ovpnUp[k]; st.net.gen++; if (sc[1] === 'stop') return ''; }
      if (sc[1] === 'status') { var e = ovEntry(st, k); return '● ' + k + '.service - OpenVPN tunnel for ' + sc[2] + '\n     Active: ' + (st.ovpnUp[k] ? 'active (running)' : 'inactive (dead)') + (e ? '\n\n' + e.ol.slice(-6).join('\n') : ''); }
      if (st.user !== 'root') return 'Failed to start ' + k + '.service: Access denied';
      var res = ovUp(st, '/etc/openvpn/client/' + sc[2] + '.conf', k); return /Options error/.test(res) ? 'Job for ' + k + '.service failed because the control process exited with error code.' : ''; }
    if (c === 'journalctl' && /openvpn-client@\w+/.test(line)) { var k2 = line.match(/openvpn-client@\w+/)[0], e2 = ovEntry(st, k2); return e2 ? e2.ol.join('\n') : '-- No entries --'; }
    if (c === 'openssl' && t[1] === 'x509') return x509(st, t);
    if (c === 'pkill' && t[1] === 'openvpn' || c === 'killall' && t[1] === 'openvpn') { if (st.ovpnUp) { delete st.ovpnUp.openvpn; st.net.gen++; } return ''; }
    var r = deb0.call(this, st, sh(raw, st), ui);
    if (/^ip\s+a(ddr)?(\s+show)?$/.test(line)) { var id = Object.keys(st.net.devs).filter(function (x) { return st.net.devs[x].st === st; })[0];
      ok(st.net).filter(function (e) { return e.cli === id; }).forEach(function (e) { r += '\n9: ' + cliIf(e, st.net) + ': <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UNKNOWN group default qlen 500\n    link/none\n    inet ' + e.x.ip + '/' + e.x.len + ' scope global ' + cliIf(e, st.net) + '\n       valid_lft forever preferred_lft forever'; }); }
    return r;
  };
  var pr0 = H.debPrompt;
  H.debPrompt = function (st) { var p = pr0.apply(this, arguments); if (st.ssh || !st.user || !st.cwd) return p;
    var h = home(st.user), d = st.cwd.indexOf(h + '/') === 0 ? '~' + st.cwd.slice(h.length) : st.cwd; return p.replace(':~', ':' + d); };
})(typeof window !== 'undefined' ? window : global);
