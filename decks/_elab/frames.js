/* Кадры модели для учебных инструментов («Тест»): захват трафика на кабеле (как Wireshark в pnetlab)
   и разбор кадра по уровням OSI (Ethernet / 802.1Q → ARP | IPv4 → ICMP | TCP | UDP, BPDU STP).
   Сведения о кадре кладёт в шаги трассы net.js (поле f): MAC, IP, протокол, порты, TTL. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype;
  var SVC = { 53: 'DNS', 67: 'DHCP', 68: 'DHCP', 69: 'TFTP', 123: 'NTP', 514: 'Syslog', 22: 'SSH', 23: 'TELNET', 80: 'HTTP' };
  var PNUM = { icmp: 1, tcp: 6, udp: 17 };
  var CAP_MAX = 2000;

  // ---------------------------------------------------------------- захват на кабеле
  P.capStart = function (li) { var l = this.links[li]; if (!l) return null;
    var c = (this.caps = this.caps || []).filter(function (x) { return x.link === l; })[0];
    if (!c) { c = { link: l, frames: [], t0: this.now, n: 0 }; this.caps.push(c); } return c; };
  P.capStop = function (cap) { this.caps = (this.caps || []).filter(function (x) { return x !== cap; }); };
  P.capFrame = function (sg, f, size) {
    if (!this.caps || !this.caps.length || !f) return;
    var l = this.links[sg.li], s = this;
    this.caps.forEach(function (c) { if (c.link !== l) return;
      var fr = row(s, c, sg, f, size); c.frames.push(fr); if (c.frames.length > CAP_MAX) c.frames.shift();
      if (c.on) c.on(fr); });
  };
  function row(s, c, sg, f, size) {
    var tag = sg.tag !== null && sg.tag !== undefined ? sg.tag : null;
    return { no: ++c.n, t: Math.max(0, s.now - c.t0), from: s.devs[sg.from] ? s.devs[sg.from].name : '', to: s.devs[sg.to] ? s.devs[sg.to].name : '',
             vlan: tag, len: size, f: f, smac: f.smac, dmac: f.dmac, type: f.type === 'arp' ? 'ARP' : f.type === 'stp' ? 'STP' : 'IPv4',
             sip: f.type === 'arp' ? f.sip : f.src || '', dip: f.type === 'arp' ? f.tip : f.dst || '', proto: proto(f), info: info(f) };
  }
  function proto(f) {
    if (f.type === 'arp') return 'ARP'; if (f.type === 'stp') return 'STP';
    if (f.dhcp) return 'DHCP';
    if (f.proto === 'icmp') return 'ICMP';
    var p = SVC[f.dport] || SVC[f.sport];
    return f.proto === 'udp' && p ? p : f.proto.toUpperCase();
  }
  function info(f) {
    if (f.type === 'arp') return f.op === 1 ? 'Who has ' + f.tip + '? Tell ' + f.sip : f.sip + ' is at ' + f.smac;
    if (f.type === 'stp') return (f.ver === 0 ? 'Conf.' : f.ver === 3 ? 'MST.' : 'RST.') + ' Root = ' + f.rprio + '/0/' + f.rmac + '  Cost = ' + f.cost + '  Port = 0x' + f.port.toString(16);
    if (f.dhcp) return 'DHCP ' + f.dhcp;
    if (f.proto === 'icmp') return 'Echo (ping) ' + (f.reply ? 'reply' : 'request') + '  ttl=' + f.ttl;
    var ports = (f.sport || '?') + ' → ' + (f.dport || '?');
    if (f.proto === 'tcp') return ports + (f.reply ? ' [SYN, ACK]' : ' [SYN]') + ' Seq=0' + (f.reply ? ' Ack=1' : '') + ' Win=64240';
    return ports + ' Len=' + (f.dport === 123 || f.sport === 123 ? 48 : 0);
  }
  EL.frameRow = function (f, tag, size) { return row({ now: 0, devs: {} }, { t0: 0, n: 0 }, { tag: tag }, f, size || 0); };

  // ---------------------------------------------------------------- разбор по уровням
  function hexType(t) { return t === 'arp' ? 'ARP (0x0806)' : 'IPv4 (0x0800)'; }
  EL.decode = function (f, tag, size) {
    var L = [], len = size || 0, tagged = tag !== null && tag !== undefined;
    L.push({ osi: 'L1', name: 'Frame: ' + len + ' bytes on wire', fields: [['Длина кадра', len + ' байт (с FCS)']] });
    if (f.type === 'stp') {
      L.push({ osi: 'L2', name: 'IEEE 802.3 Ethernet, Src: ' + f.smac + ', Dst: 01:80:c2:00:00:00', fields: [['Destination', '01:80:c2:00:00:00 (Spanning-tree-(for-bridges)_00)'], ['Source', f.smac], ['Length', 39]] });
      L.push({ osi: 'L2', name: 'Logical-Link Control', fields: [['DSAP', 'Spanning Tree BPDU (0x42)'], ['SSAP', 'Spanning Tree BPDU (0x42)'], ['Control field', 'U, func=UI (0x03)']] });
      L.push({ osi: 'L2', name: 'Spanning Tree Protocol', fields: [['Protocol Identifier', 'Spanning Tree Protocol (0x0000)'],
        ['Protocol Version Identifier', f.ver === 0 ? 'Spanning Tree (0)' : f.ver === 3 ? 'Multiple Spanning Tree (3)' : 'Rapid Spanning Tree (2)'],
        ['BPDU Type', f.ver === 0 ? 'Configuration (0x00)' : 'Rapid/Multiple Spanning Tree (0x02)'], ['Root Identifier', f.rprio + ' / 0 / ' + f.rmac], ['Root Path Cost', f.cost],
        ['Bridge Identifier', f.bprio + ' / 0 / ' + f.smacB], ['Port identifier', '0x' + f.port.toString(16)], ['Message Age', 0], ['Max Age', 20], ['Hello Time', 2], ['Forward Delay', 15]] });
      return L;
    }
    var eth = [['Destination', f.dmac + (f.dmac === 'ff:ff:ff:ff:ff:ff' ? ' (Broadcast)' : '')], ['Source', f.smac]];
    if (!tagged) eth.push(['Type', hexType(f.type)]); else eth.push(['Type', '802.1Q Virtual LAN (0x8100)']);
    L.push({ osi: 'L2', name: 'Ethernet II, Src: ' + f.smac + ', Dst: ' + f.dmac, fields: eth });
    if (tagged) L.push({ osi: 'L2', name: '802.1Q Virtual LAN, PRI: 0, DEI: 0, ID: ' + tag, fields: [['Priority (PCP)', 0], ['DEI', 0], ['VLAN ID', tag], ['Type', hexType(f.type)]] });
    if (f.type === 'arp') {
      L.push({ osi: 'L2/3', name: 'Address Resolution Protocol (' + (f.op === 1 ? 'request' : 'reply') + ')', fields: [['Hardware type', 'Ethernet (1)'],
        ['Protocol type', 'IPv4 (0x0800)'], ['Hardware size', 6], ['Protocol size', 4], ['Opcode', f.op === 1 ? 'request (1)' : 'reply (2)'],
        ['Sender MAC address', f.smac], ['Sender IP address', f.sip], ['Target MAC address', f.op === 1 ? '00:00:00:00:00:00' : f.dmac], ['Target IP address', f.tip]] });
      return L;
    }
    var ipLen = Math.max(20, len - 18 - (tagged ? 4 : 0));
    L.push({ osi: 'L3', name: 'Internet Protocol Version 4, Src: ' + f.src + ', Dst: ' + f.dst, fields: [['Version', 4], ['Header Length', '20 bytes (5)'],
      ['Differentiated Services Field', '0x00 (DSCP: CS0, ECN: Not-ECT)'], ['Total Length', ipLen], ['Flags', f.proto === 'udp' && f.dhcp ? '0x0' : '0x2, Don\'t fragment'],
      ['Fragment Offset', 0], ['Time to Live', f.ttl], ['Protocol', f.proto.toUpperCase() + ' (' + PNUM[f.proto] + ')'], ['Source Address', f.src], ['Destination Address', f.dst]] });
    if (f.proto === 'icmp') L.push({ osi: 'L3', name: 'Internet Control Message Protocol', fields: [['Type', f.reply ? '0 (Echo (ping) reply)' : '8 (Echo (ping) request)'], ['Code', 0],
      ['Identifier (BE)', 1], ['Sequence Number (BE)', 1], ['Data', (ipLen - 28) + ' bytes']] });
    if (f.proto === 'tcp') L.push({ osi: 'L4', name: 'Transmission Control Protocol, Src Port: ' + f.sport + ', Dst Port: ' + f.dport, fields: [['Source Port', f.sport], ['Destination Port', f.dport],
      ['Sequence Number', '0 (relative)'], ['Acknowledgment Number', f.reply ? '1 (relative)' : 0], ['Flags', f.reply ? '0x012 (SYN, ACK)' : '0x002 (SYN)'], ['Window', 64240]] });
    if (f.proto === 'udp') { L.push({ osi: 'L4', name: 'User Datagram Protocol, Src Port: ' + f.sport + ', Dst Port: ' + f.dport, fields: [['Source Port', f.sport], ['Destination Port', f.dport], ['Length', ipLen - 20]] });
      var app = f.dhcp ? 'DHCP' : SVC[f.dport] || SVC[f.sport];
      if (app && f.dhcp) L.push({ osi: 'L7', name: 'Dynamic Host Configuration Protocol (' + f.dhcp + ')', fields: [['Message type', 'Boot Request (1)'], ['Client MAC address', f.smac], ['Option (53)', 'DHCP Message Type (' + f.dhcp + ')']] });
      else if (app) L.push({ osi: 'L7', name: app, fields: [['Порт службы', f.dport === 123 || f.dport === 514 || f.dport === 69 || f.dport === 53 ? f.dport : f.sport]] }); }
    return L;
  };

  // ---------------------------------------------------------------- BPDU для захвата
  P.capBpdu = function (id, port, lname) {
    if (!this.caps || !this.caps.length) return;
    var pr = this.peer(id, port); if (!pr) return;
    var d = this.devs[id], st = d.st, root = this._stp && this.devs[this._stp.root[id]], rs = root ? root.st : st;
    var mode = (st.stp || {}).mode || 'mst', ver = mode === 'stp' ? 0 : mode === 'mst' ? 3 : 2;
    var num = (lname.match(/(\d+)$/) || [0, 1])[1];
    this.capFrame({ li: pr.li, from: id, to: pr.dev, tag: null }, { type: 'stp', smac: EL.mac(d.name + port), dmac: '01:80:c2:00:00:00', smacB: st.bmac, ver: ver,
      rprio: (rs.stp || { prio: 32768 }).prio, rmac: rs.bmac, bprio: (st.stp || { prio: 32768 }).prio, cost: this._stp ? this._stp.dist[id] || 0 : 0, port: 0x8000 + +num }, 64);
  };

  // ---------------------------------------------------------------- конфигурации текстом (экспорт/импорт)
  EL.cfgText = function (d) { return d.type === 'mes' ? EL.E.showRun(d.st) : d.type === 'esr' ? EL.esr.showRun(d.st) : null; };
  var cfgText = EL.cfgText;
  // применить текст конфигурации, как будто его вставили в консоль: MES — configure … end; ESR — configure … end, commit, confirm
  EL.applyConfig = function (n, id, text) {
    var d = n.devs[id], errs = [], st = d.st; if (d.type !== 'mes' && d.type !== 'esr') return ['конфигурация текстом — только MES и ESR'];
    var lines = String(text).split('\n').map(function (x) { return x.replace(/\s+$/, ''); }).filter(function (x) { return x.trim() && !/^\s*[!#]/.test(x); });
    st.mode = 'priv'; n.exec(id, 'configure');
    lines.forEach(function (l) { var r = n.exec(id, l.trim()); if (typeof r === 'string' && /^(%|Syntax error)/.test(r)) errs.push(d.name + ' «' + l.trim() + '» → ' + r.split('\n')[0]); });
    n.exec(id, 'end'); st.mode = 'priv';
    if (d.type === 'esr') { n.exec(id, 'commit'); n.exec(id, 'confirm'); }
    return errs;
  };
  EL.exportConfigs = function (n) { return n.list().filter(function (d) { return d.type === 'mes' || d.type === 'esr'; })
    .map(function (d) { return '! ==== ' + d.name + ' (' + d.model + ') ====\n' + cfgText(d); }).join('\n\n') + '\n'; };
  EL.importConfigs = function (n, text) {
    var errs = [], parts = String(text).split(/^! ==== (\S+)[^\n]*====\s*$/m);
    for (var i = 1; i < parts.length; i += 2) { var d = n.byName(parts[i]); if (!d) { errs.push('нет устройства ' + parts[i]); continue; } errs = errs.concat(EL.applyConfig(n, d.id, parts[i + 1])); }
    if (parts.length < 3) errs.push('в тексте нет заголовков «! ==== ИМЯ (модель) ====»');
    return errs;
  };
})(typeof window !== 'undefined' ? window : global);
