/* Конечные узлы: VPC (как в pnetlab/VPCS) и компьютер Debian (ip, ifup/ifdown, nano interfaces, ping, ssh). */
(function (G) {
  'use strict';
  var EL = G.EL, IP = EL.ip;

  // ================================================================ VPC
  function vpc(name) { return { kind: 'vpc', name: name, ip: null, len: 24, gw: null }; }
  function vpcExec(st, raw) {
    var t = String(raw).trim().split(/\s+/), c = (t[0] || '').toLowerCase();
    if (!c) return '';
    if (c === '?' || c === 'help') return ['ip ARG ... [OPTION]   Настроить адрес: ip 10.0.0.2/24 10.0.0.1',
      'show [ip]             Показать настройки', 'ping HOST             Проверить связность', 'trace HOST            Трассировка',
      'arp                   ARP-таблица', 'clear ip              Сбросить адрес'].join('\n');
    if (c === 'ip') {
      if (t[1] === 'dhcp') return 'DDORA — DHCP-сервер не ответил (DHCP появится на следующем этапе эмулятора)';
      var cidr = IP.parseCidr(t[1] || ''), ip = t[1], len = 24, gw = t[2];
      if (cidr) { ip = cidr.ip; len = cidr.len; }
      else if (t[2] && IP.mask2len(t[2]) !== null) { len = IP.mask2len(t[2]); gw = t[3]; }
      if (!ip || IP.ip2n(ip) === null) return 'Invalid address';
      if (gw && IP.ip2n(gw) === null) return 'Invalid gateway';
      if (gw && !IP.sameNet(ip, gw, len)) return 'Gateway ' + gw + ' не в подсети ' + IP.netOf(ip, len);
      st.ip = ip; st.len = len; st.gw = gw || null;
      return 'Checking for duplicate address...\n' + st.name + ' : ' + ip + ' ' + IP.len2mask(len) + (gw ? ' gateway ' + gw : '');
    }
    if (c === 'clear' && t[1] === 'ip') { st.ip = null; st.gw = null; return 'IPv4 address/mask, gateway, DNS, and DHCP cleared'; }
    if (c === 'show' || c === 'sh') return ['NAME        : ' + st.name, 'IP/MASK     : ' + (st.ip ? st.ip + '/' + st.len : '0.0.0.0/0'),
      'GATEWAY     : ' + (st.gw || '0.0.0.0'), 'MAC         : ' + EL.mac(st.name + 'eth0'), 'LPORT       : 20000'].join('\n');
    if (c === 'ping') { if (!t[1]) return 'Usage: ping HOST'; return st.net ? st.net.pingText(st.dev, t[1], 'vpc') : ''; }
    if (c === 'trace' || c === 'tracert') return st.net ? st.net.traceText(st.dev, t[1] || '') : '';
    if (c === 'arp') return st.net ? st.net.arpText(st.dev) : '';
    return 'Bad command: "' + raw.trim() + '". Use ? for help.';
  }
  function vpcPrompt(st) { return st.name + '> '; }

  // ================================================================ Debian
  var IFDEF = ['# This file describes the network interfaces available on your system', '# and how to activate them. For more information, see interfaces(5).', '',
    'source /etc/network/interfaces.d/*', '', '# The loopback network interface', 'auto lo', 'iface lo inet loopback', '',
    '# The primary network interface', 'allow-hotplug ens3', 'iface ens3 inet dhcp', ''].join('\n');
  function deb(name) {
    return { kind: 'deb', name: name, host: 'debian', user: null, login: 'user', up: false, ip: null, len: 24, gw: null,
             files: { '/etc/network/interfaces': IFDEF }, accounts: { root: 'toor', user: 'user' }, ssh: null };
  }
  function debPrompt(st) {
    if (st.ssh) return st.ssh.prompt();
    if (!st.user) return st.login === 'user' ? st.host + ' login: ' : 'Password: ';
    return st.user + '@' + st.host + ':~' + (st.user === 'root' ? '# ' : '$ ');
  }
  function parseIfaces(text) {                // берём блок «iface ens3 inet static»
    var r = { auto: false, mode: null, ip: null, len: 24, gw: null };
    var lines = text.split('\n').map(function (l) { return l.replace(/#.*/, '').trim(); }).filter(Boolean), inb = false;
    lines.forEach(function (l) {
      var w = l.split(/\s+/);
      if (w[0] === 'auto' || w[0] === 'allow-hotplug') { if (w.indexOf('ens3') > 0) r.auto = true; return; }
      if (w[0] === 'iface') { inb = w[1] === 'ens3'; if (inb) r.mode = w[3]; return; }
      if (!inb) return;
      if (w[0] === 'address') { var c = IP.parseCidr(w[1]); if (c) { r.ip = c.ip; r.len = c.len; } else r.ip = w[1]; }
      if (w[0] === 'netmask' && IP.mask2len(w[1]) !== null) r.len = IP.mask2len(w[1]);
      if (w[0] === 'gateway') r.gw = w[1];
    });
    return r;
  }
  function ipA(st) {
    var mac = EL.mac(st.name + 'ens3'), o = ['1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000',
      '    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00', '    inet 127.0.0.1/8 scope host lo', '       valid_lft forever preferred_lft forever',
      '2: ens3: <BROADCAST,MULTICAST' + (st.up ? ',UP,LOWER_UP' : '') + '> mtu 1500 qdisc ' + (st.up ? 'pfifo_fast state UP' : 'noop state DOWN') + ' group default qlen 1000',
      '    link/ether ' + mac + ' brd ff:ff:ff:ff:ff:ff', '    altname enp0s3'];
    if (st.ip) o.push('    inet ' + st.ip + '/' + st.len + ' brd ' + IP.n2ip((IP.ip2n(st.ip) | (~IP.maskN(st.len) >>> 0)) >>> 0) + ' scope global ens3',
                      '       valid_lft forever preferred_lft forever');
    return o.join('\n');
  }
  function debExec(st, raw, ui) {
    if (st.ssh) return st.ssh.exec(raw);
    var line = String(raw);
    if (!st.user) {                             // вход в систему
      if (st.login === 'user') { st.pendingUser = line.trim(); st.login = 'pw'; return null; }
      st.login = 'user';
      if (st.accounts[st.pendingUser] && st.accounts[st.pendingUser] === line.trim()) {
        st.user = st.pendingUser;
        return 'Linux debian 5.10.0-23-amd64 #1 SMP Debian 5.10.179-1 x86_64\n\nThe programs included with the Debian GNU/Linux system are free software.';
      }
      return '\nLogin incorrect';
    }
    var t = line.trim().split(/\s+/), c = t[0];
    if (!c) return '';
    var root = st.user === 'root';
    function needRoot() { return root ? null : c + ': Operation not permitted (нужны права root: su - или sudo)'; }
    if (c === 'sudo') { if (!t[1]) return 'usage: sudo command'; var u = st.user; st.user = 'root'; var r = debExec(st, t.slice(1).join(' '), ui); st.user = u; return r; }
    if (c === 'su') { st.user = 'root'; return null; }
    if (c === 'exit' || c === 'logout') { st.user = null; st.login = 'user'; return 'logout'; }
    if (c === 'clear') { if (ui) ui.clear(); return ''; }
    if (c === 'hostname') return st.host;
    if (c === 'whoami') return st.user;
    if (c === 'ip') {
      var sub = t[1] || '';
      if (/^a(ddr(ess)?)?$/.test(sub) && (!t[2] || t[2] === 'show')) return ipA(st);
      if (/^a(ddr(ess)?)?$/.test(sub) && t[2] === 'add') {
        var e = needRoot(); if (e) return e;
        var cc = IP.parseCidr(t[3] || ''); if (!cc) return 'Error: any valid prefix is expected rather than "' + (t[3] || '') + '".';
        if (t[4] !== 'dev' || t[5] !== 'ens3') return 'Cannot find device "' + (t[5] || '') + '"';
        if (st.ip === cc.ip) return 'RTNETLINK answers: File exists';
        st.ip = cc.ip; st.len = cc.len; return '';
      }
      if (/^a(ddr(ess)?)?$/.test(sub) && (t[2] === 'del' || t[2] === 'flush')) { var e2 = needRoot(); if (e2) return e2; st.ip = null; st.gw = null; return ''; }
      if (sub === 'link' && t[2] === 'set') { var e3 = needRoot(); if (e3) return e3;
        if (t[3] !== 'ens3') return 'Cannot find device "' + (t[3] || '') + '"'; st.up = t[4] === 'up'; return ''; }
      if (/^r(oute)?$/.test(sub) && !t[2]) {
        var o = []; if (st.gw && st.up) o.push('default via ' + st.gw + ' dev ens3');
        if (st.ip && st.up) o.push(IP.netOf(st.ip, st.len) + ' dev ens3 proto kernel scope link src ' + st.ip);
        return o.join('\n');
      }
      if (/^r(oute)?$/.test(sub) && t[2] === 'add') { var e4 = needRoot(); if (e4) return e4;
        if (t[3] !== 'default' || t[4] !== 'via' || IP.ip2n(t[5] || '') === null) return 'Пример: ip route add default via 192.168.100.1';
        if (!st.ip || !IP.sameNet(st.ip, t[5], st.len)) return 'Error: Nexthop has invalid gateway.';
        st.gw = t[5]; return ''; }
      if (/^r(oute)?$/.test(sub) && t[2] === 'del') { st.gw = null; return ''; }
      return 'Object "' + sub + '" is unknown, try "ip help".';
    }
    if (c === 'ifup' || c === 'ifdown') {
      var e5 = needRoot(); if (e5) return e5;
      if (t[1] !== 'ens3') return c + ': unknown interface ' + (t[1] || '');
      var cfg = parseIfaces(st.files['/etc/network/interfaces']);
      if (c === 'ifdown') { if (!st.up) return 'ifdown: interface ens3 not configured'; st.up = false; st.ip = null; st.gw = null; return ''; }
      if (cfg.mode === 'dhcp') { st.up = true; return 'Internet Systems Consortium DHCP Client 4.4.1\nListening on LPF/ens3\nDHCPDISCOVER on ens3 to 255.255.255.255 port 67\nNo DHCPOFFERS received.\nNo working leases in persistent database - sleeping.'; }
      if (cfg.mode !== 'static') return 'ifup: no configuration for ens3 (в /etc/network/interfaces нет «iface ens3 inet static»)';
      if (!cfg.ip || IP.ip2n(cfg.ip) === null) return 'ifup: missing or invalid address for ens3';
      st.up = true; st.ip = cfg.ip; st.len = cfg.len; st.gw = cfg.gw && IP.sameNet(cfg.ip, cfg.gw, cfg.len) ? cfg.gw : null; return '';
    }
    if (c === 'cat') { var f = st.files[t[1]]; return f === undefined ? 'cat: ' + (t[1] || '') + ': No such file or directory' : f; }
    if (c === 'nano' || c === 'vi' || c === 'vim') {
      if (!t[1]) return 'Укажите файл: nano /etc/network/interfaces';
      if (t[1].indexOf('/etc/') === 0 && !root) return '[ Нет прав на запись: войдите как root ]';
      if (ui) ui.edit(t[1], st.files[t[1]] || '', function (txt) { st.files[t[1]] = txt; });
      else return 'nano: нужен экран (в автотесте не используется)';
      return '';
    }
    if (c === 'ping') { var dst = t.slice(1).filter(function (x) { return /^\d+\.\d+\.\d+\.\d+$/.test(x); })[0];
      if (!dst) return 'ping: usage error: Destination address required';
      return st.net ? st.net.pingText(st.dev, dst, 'linux') : ''; }
    if (c === 'traceroute') return st.net ? st.net.traceText(st.dev, t[1] || '') : '';
    if (c === 'ssh') {
      var m = (t[1] || '').match(/^([^@]+)@(\d+\.\d+\.\d+\.\d+)$/);
      if (!m) return 'usage: ssh user@A.B.C.D';
      return st.net ? st.net.sshOpen(st, m[1], m[2]) : '';
    }
    if (c === 'help' || c === '?') return 'Доступно: ip a | ip addr add A.B.C.D/N dev ens3 | ip link set ens3 up | ip route [add default via GW]\n' +
      'nano /etc/network/interfaces | cat ФАЙЛ | ifup/ifdown ens3 | ping A.B.C.D | traceroute A.B.C.D | ssh user@A.B.C.D | su | exit';
    return '-bash: ' + c + ': command not found';
  }

  EL.hosts = { vpc: vpc, vpcExec: vpcExec, vpcPrompt: vpcPrompt, deb: deb, debExec: debExec, debPrompt: debPrompt, parseIfaces: parseIfaces };
})(typeof window !== 'undefined' ? window : global);
