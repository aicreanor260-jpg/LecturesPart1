/* Руководство к устройству — по вендору и серии модели, никогда не чужого вендора.
   PDF вендора лежат на сервере курса в docs/<вендор>/<файл> (исходники — sources/<вендор>/…, список — EL.MANUAL_PDFS);
   если PDF нет — ссылка на официальную документацию серии (из каталогов sources/<вендор>/catalog и spec), открывается на сайте вендора.
   Обычные MES и ESR Eltex — по-прежнему net.js (docs/mes-*.pdf, docs/esr-cli.pdf); конечным узлам и облаку провайдера руководства нет. */
(function (G) {
  'use strict';
  var EL = G.EL, P = EL.Net.prototype, MODELS = EL.MODELS;
  var SITE = { eltex: 'Eltex', huawei: 'Huawei', cisco: 'Cisco', mikrotik: 'MikroTik', dlink: 'D-Link' };
  var HW = 'https://support.huawei.com/enterprise/en/doc/', PT = 'https://tutorials.ptnetacad.net/help/default/';
  // вендор модели: D-Link-диалект движка Cisco числится в группе D-Link, OLT/ONT Huawei — в группе Huawei
  function vendorOf(model) { var m = MODELS[model] || {};
    if (m.group === 'D-Link') return 'dlink';
    if (m.vendor) return m.vendor;
    return /^Huawei/.test(m.group || '') ? 'huawei' : 'eltex'; }
  // [вендор, модели, руководство]: pdf — путь в sources/<вендор>/ и имя на сервере; site — страница документации
  function pdf(src, file, title) { return { src: src, file: file || src.split('/').pop(), title: title }; }
  function site(url, title, extra) { return { site: url, title: title, extra: extra || [] }; }
  var ROS = { url: 'https://help.mikrotik.com/docs/spaces/ROS/pages/328151/First+Time+Configuration', title: 'RouterOS: первая настройка' };
  var RULES = [
    ['eltex', /FSTEC$/, pdf('esr-fstec/ESR_FSTEС_A4_Series_CLI_1.5.10.pdf', 'esr-fstec-cli-1.5.10.pdf', 'Справочник CLI ESR ФСТЭК 1.5.10')],
    ['eltex', /^ME\d/, pdf('me/ELTEX_ME_Command_Reference_3.13.0.pdf', 'me-command-reference-3.13.0.pdf', 'Справочник команд ME 3.13.0')],
    ['eltex', /^WLC-/, pdf('wifi/WLC-Series_user_manual_1.39.2.pdf', null, 'Руководство WLC 1.39.2')],
    ['eltex', /ESBC/, pdf('voip/ESBC-Series_CLI_1.9.0.pdf', null, 'Справочник CLI ESBC 1.9.0')],
    ['eltex', /^RG-35-WZ$/, pdf('cpe/RG-35-WZ_Wac_user_manual_2.3.0.pdf', null, 'Руководство RG-35-WZ 2.3.0')],
    ['eltex', /^SCS-32$/, pdf('console-servers/SCS-32_CLI_1.1.0.pdf', null, 'Справочник CLI SCS-32 1.1.0')],
    ['eltex', /^TAU-72\.IP$/, pdf('voip/TAU36_72.IP_user_manual_2.23.8.pdf', null, 'Руководство TAU-36/72.IP 2.23.8')],
    ['eltex', /^SMG-1016M$/, pdf('voip/SMG-1016M_SMG-2016_SMG-3016_SMG-3116_user_manual_3.411.0.pdf', 'smg-user-manual-3.411.0.pdf', 'Руководство SMG 3.411.0')],
    ['eltex', /^LTP-[48]X/, pdf('pon/LTP-4X_8X_CLI_3.52.0.pdf', null, 'Справочник CLI LTP-4X/8X 3.52.0')],
    ['eltex', /^LTP-4N$/, pdf('pon/LTP-4(8_16)N_LTX-8(16)_LTX-8(16)_rev.B_LTX-8(16)C_CLI_1.11.5.pdf', 'ltp-n-ltx-cli-1.11.5.pdf', 'Справочник CLI LTP-N/LTX 1.11.5')],
    ['eltex', /^(LTP-(8|16)N|LTX-)/, pdf('pon/LTP-8(16)N_LTX-8(16)_LTX-8(16)_rev.B_LTX-8(16)C_CLI_1.12.0.pdf', 'ltp-n-ltx-cli-1.12.0.pdf', 'Справочник CLI LTP-N/LTX 1.12.0')],
    ['eltex', /^LTE-[28]X$/, pdf('pon/OLT_LTE-8X_2X_manual_3.16.7.pdf', null, 'Руководство LTE-2X/8X 3.16.7')],
    ['eltex', /^MA4000-PX$/, pdf('pon/MA4000-PX_CLI_3.38.1.pdf', null, 'Справочник CLI MA4000-PX 3.38.1')],
    ['eltex', /^MA5(020|160)$/, pdf('pon/MA5020_MA5160_CLI_1.13.0.pdf', null, 'Справочник CLI MA5020/MA5160 1.13.0')],
    ['eltex', /^NTU-1/, pdf('pon/NTU-1_NTU-1C_NTU-1L_NTU-1LC_NTU-1D_3.32.0_user.pdf', null, 'Руководство NTU-1 3.32.0')],
    ['eltex', /^NTX-1/, pdf('pon/NTX-1(F)_user_manual_1.2.4_user.pdf', 'ntx-1-user-manual-1.2.4.pdf', 'Руководство NTX-1(F) 1.2.4')],
    ['eltex', /^NTE-2/, pdf('pon/onu-nte_2_n.pdf', null, 'Руководство NTE-2')],
    ['eltex', /^WEP-30L/, pdf('wifi/WEP-30L_WEP-30L-Z_user_manual_2.14.0.pdf', null, 'Руководство WEP-30L/30L-Z 2.14.0')],
    ['eltex', /^WEP-3L$/, pdf('wifi/WEP-3L_user_manual_2.11.2.pdf', null, 'Руководство WEP-3L 2.11.2')],
    ['eltex', /^WEP-3ax$/, pdf('wifi/WEP-3ax_user_manual_1.17.1.pdf', null, 'Руководство WEP-3ax 1.17.1')],
    ['eltex', /^WEP-500K$/, pdf('wifi/WEP-500K_user_manual_1.4.2.pdf', null, 'Руководство WEP-500K 1.4.2')],
    ['eltex', /^WEP-50L$/, pdf('wifi/WEP-50L_user_manual_3.1.1.pdf', null, 'Руководство WEP-50L 3.1.1')],
    ['eltex', /^WEP-550K$/, pdf('wifi/WEP-550K_user_manual_1.4.2.pdf', null, 'Руководство WEP-550K 1.4.2')],
    ['eltex', /^WOP-20L$/, pdf('wifi/WOP-20L_user_manual_2.11.3.pdf', null, 'Руководство WOP-20L 2.11.3')],
    ['eltex', /^WOP-2L$/, pdf('wifi/WOP-2L_user_manual_2.8.13.pdf', null, 'Руководство WOP-2L 2.8.13')],
    ['eltex', /^WOP-2ac$/, pdf('wifi/WOP-2ac_User_manual_1.25.7.pdf', null, 'Руководство WOP-2ac 1.25.7')],
    ['eltex', /^WOP-30L$/, pdf('wifi/WOP-30L_user_manual_2.14.0.pdf', null, 'Руководство WOP-30L 2.14.0')],
    ['eltex', /^WOP-30LI$/, pdf('wifi/WOP-30LI_user_manual_2.14.0.pdf', null, 'Руководство WOP-30LI 2.14.0')],
    ['eltex', /^WOP-30LS$/, pdf('wifi/WOP-30LS_user_manual_2.14.0.pdf', null, 'Руководство WOP-30LS 2.14.0')],
    ['eltex', /^WOP-3L-EX$/, pdf('wifi/WOP-3L-EX_user_manual_2.11.2.pdf', null, 'Руководство WOP-3L-EX 2.11.2')],
    ['dlink', /^DES-3200/, pdf('docs/legacy/DES-3200_CLI_R4.04.pdf', null, 'CLI Reference DES-3200 R4.04')],
    ['dlink', /^DGS-3000/, pdf('docs/legacy/DGS-3000_B1_CLI_R4.00.pdf', null, 'CLI Reference DGS-3000 R4.00')],
    ['dlink', /^DGS-1510/, pdf('docs/ios/DGS-1510_CLI_v1.81.pdf', null, 'CLI Reference DGS-1510 v1.81')],
    ['dlink', /^DGS-3130/, pdf('docs/ios/DGS-3130_B1_CLI_v1.30.pdf', null, 'CLI Reference DGS-3130 v1.30')],
    ['huawei', /^S[35]700$/, site(HW + 'EDOC1000178165', 'S series: Command Reference')],
    ['huawei', /^AR[12]220$/, site(HW + 'EDOC1100007335', 'AR: Product Documentation')],
    ['huawei', /^CE6881/, site(HW + 'EDOC1100468598', 'CloudEngine: Command Reference')],
    ['huawei', /^USG6510E$/, site(HW + 'EDOC1100149308', 'HiSecEngine USG6000E: Product Documentation')],
    ['huawei', /^(AC6005|AP\d+DN)$/, site(HW + 'EDOC1100064351', 'WLAN AC/AP: Command Reference')],
    ['huawei', /^EG8145V5$/, site('https://e.huawei.com/en/products/optical-terminal/echolife-eg8145v5', 'EchoLife EG8145V5')],
    ['cisco', /^2960/, site(PT + 'commandReference/2960_15.0_SE4.html', 'Catalyst 2960: Command Reference (Packet Tracer)')],
    ['cisco', /^2950/, site(PT + 'commandReference/2950_12.1_EA8.html', 'Catalyst 2950: Command Reference (Packet Tracer)')],
    ['cisco', /^3560/, site(PT + 'commandReference/3560_advip_12.2_46.html', 'Catalyst 3560: Command Reference (Packet Tracer)')],
    ['cisco', /^19\d\d$/, site('https://www.cisco.com/c/en/us/support/routers/1900-series-integrated-services-routers-isr/series.html', 'ISR 1900 Series: документация')],
    ['cisco', /^29\d\d$/, site('https://www.cisco.com/c/en/us/support/routers/2900-series-integrated-services-routers-isr/series.html', 'ISR 2900 Series: документация')],
    ['cisco', /^ISR4\d+$/, site('https://www.cisco.com/c/en/us/support/routers/4000-series-integrated-services-routers-isr/series.html', 'ISR 4000 Series: документация')],
    ['cisco', /^ASA/, site(PT + 'CLI_asa.htm', 'ASA: команды CLI (Packet Tracer)', [{ url: 'https://www.cisco.com/c/en/us/td/docs/security/asa/asa92/configuration/general/asa-general-cli/intro-start.html', title: 'ASA 9.2: CLI Configuration Guide' }])],
    ['mikrotik', /^CHR$/, site('https://help.mikrotik.com/docs/spaces/ROS/pages/18350234/Cloud+Hosted+Router+CHR', 'Cloud Hosted Router (CHR)', [ROS])],
    ['mikrotik', /^hEX RB750Gr3$/, site('https://mikrotik.com/product/RB750Gr3', 'hEX RB750Gr3', [ROS])],
    ['mikrotik', /^RB4011iGS\+RM$/, site('https://mikrotik.com/product/rb4011igs_rm', 'RB4011iGS+RM', [ROS])],
    ['mikrotik', /^CRS326-24G-2S\+$/, site('https://mikrotik.com/product/CRS326-24G-2SplusRM', 'CRS326-24G-2S+', [ROS])]
  ];
  function ruleFor(model) { var v = vendorOf(model);
    for (var i = 0; i < RULES.length; i++) if (RULES[i][0] === v && RULES[i][1].test(model)) return RULES[i]; return null; }
  function plainEltex(d) { var m = MODELS[d.model] || {}; return vendorOf(d.model) === 'eltex' && !m.kind && (d.type === 'mes' || d.type === 'esr'); }
  var base = P.manualFor;
  P.manualFor = function (id) { var d = this.devs[id]; if (!d) return null;
    var v = vendorOf(d.model), r = ruleFor(d.model);
    if (!r) return plainEltex(d) ? Object.assign({ vendor: 'eltex' }, base.call(this, id)) : null;
    var e = r[2];
    if (e.site) return { vendor: v, site: true, url: e.site, title: e.title, extra: e.extra };
    return { vendor: v, url: 'docs/' + v + '/' + e.file, title: e.title, extra: [] };
  };
  EL.vendorOf = vendorOf; EL.SITE_NAMES = SITE;
  // что выложить на сервер: sources/<вендор>/<путь> → /srv/net-cat/docs/<вендор>/<файл>
  EL.MANUAL_PDFS = RULES.filter(function (r) { return r[2].src; }).map(function (r) {
    return { vendor: r[0], src: 'sources/' + r[0] + '/' + r[2].src, file: r[0] + '/' + r[2].file }; });
})(typeof window !== 'undefined' ? window : global);
