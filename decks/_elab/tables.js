/* Таблицы устройств в CLI: ARP (все), MAC (коммутаторы), очистка — чтобы студент видел, как они заполняются пакетами. */
(function (G) {
  'use strict';
  var EL = G.EL, E = EL.E, S = EL.esr;

  EL.Net.prototype.arpRows = function (id) {
    var a = this.arp[id]; return Object.keys(a).sort(function (x, y) { return EL.ip.ip2n(x) - EL.ip.ip2n(y); }).map(function (ip) { return { ip: ip, mac: a[ip].mac, ifn: a[ip].ifn }; });
  };
  EL.Net.prototype.macRows = function (id) {
    var t = this.mac[id]; return Object.keys(t).map(function (k) { return t[k]; }).sort(function (x, y) { return x.vlan - y.vlan || (x.port < y.port ? -1 : 1); });
  };
  function arpEsr(st) { var R = st.net.arpRows(st.dev);
    return ['IP address          MAC address         Interface        Type', '------------------- ------------------- ---------------- -------']
      .concat(R.map(function (r) { return (r.ip + '                    ').slice(0, 20) + r.mac + '   ' + (r.ifn + '                 ').slice(0, 17) + 'dynamic'; }))
      .join('\n') + (R.length ? '' : '\n% ARP-таблица пуста — она заполняется, когда через интерфейсы идут пакеты (ping)'); }
  function arpMes(st) { var R = st.net.arpRows(st.dev);
    return ['  Interface   IP address        HW address           Status', '  ---------   ---------------   ------------------   -------']
      .concat(R.map(function (r) { return '  ' + (r.ifn + '            ').slice(0, 12) + (r.ip + '                  ').slice(0, 18) + r.mac + '    dynamic'; }))
      .join('\n') + (R.length ? '' : '\n% ARP-таблица пуста'); }
  S.cmd('priv', 'show arp', function (st) { return st.net ? arpEsr(st) : ''; }, 'ARP-таблица');
  S.cmd('priv', 'clear arp', function (st) { if (st.net) st.net.arp[st.dev] = {}; }, 'Очистить ARP-таблицу');
  ['', 'do '].forEach(function (pre) {
    var m = pre ? E.CFG : 'priv';
    E.cmd(m, pre + 'show arp', function (st) { return st.net ? arpMes(st) : ''; });
    E.cmd(m, pre + 'clear arp-cache', function (st) { if (st.net) st.net.arp[st.dev] = {}; });
    E.cmd(m, pre + 'clear mac address-table dynamic', function (st) { if (st.net) st.net.mac[st.dev] = {}; });
  });
})(typeof window !== 'undefined' ? window : global);
