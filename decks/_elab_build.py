# -*- coding: utf-8 -*-
"""Сборка эмулятора сети Eltex: decks/_elab/* + движок MES _dk_cli.js → один офлайн-файл decks/eltex-cli.html.
Перед записью прогоняет автотест (node decks/_elab/test.js) и node --check по итоговому скрипту."""
import os
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "_elab")
ORDER = ["../_dk_cli.js", "common.js", "esr.js", "esr_svc.js", "esr_more.js", "esr_ops.js", "mesx.js", "mes_l2.js", "mes_dialects.js", "hosts.js", "catalog.js", "net.js", "tables.js", "aging.js", "mes_full.js", "esr_fw.js", "rt_timers.js", "console.js", "frames.js", "ipv6.js", "ipv6_rt.js", "slaac.js", "dhcp6.js", "dns.js", "tunnel.js", "ipsec.js", "physics.js", "l2sec.js", "qinq.js", "mstp.js", "stp_timers.js", "dhcp_timers.js", "svc_timers.js", "snmp.js", "aaa.js", "ra.js", "wg.js", "ovpn.js", "vrf.js", "reload.js", "pbr.js", "bfd.js", "bgp.js", "bgp_policy.js", "l2tp.js", "dot1x.js", "igmp.js", "pim.js", "stack.js", "mtu.js", "scs.js", "ssh.js", "wlc.js", "olt.js", "lte.js", "tau.js", "esbc.js", "cpe.js", "cables.js", "linkprops.js", "isp.js", "simexp.js", "simnb.js", "apps.js", "srv.js", "me.js", "me_mpls.js", "security.js", "huawei.js", "huawei_s.js", "huawei_ar.js", "faults.js", "cisco.js", "cisco_sw.js", "cisco_rt.js", "cisco_asa.js", "mes10.js", "sim.js", "qos.js", "pt.js", "labs.js", "labs_routing.js", "labs_services.js", "labs_l2.js", "labs_ops.js", "labs_exam.js", "labs_faults.js", "labs_mixed.js", "labs_cisco.js", "ui.js", "ui_tools.js", "sim_ui.js", "sim_res.js", "cpe_ui.js", "desk_ui.js", "simpy_ui.js", "srv_ui.js", "pdu_ui.js", "zones_ui.js", "linkprops_ui.js", "isp_ui.js", "net_ws.js", "room_ui.js", "pt_ui.js", "faults_ui.js"]


def read(p):
    with open(os.path.join(SRC, p), encoding="utf-8") as f:
        return f.read()


def main():
    js = "\n".join(read(p) for p in ORDER)
    page = read("page.html")
    helpsrc = '<template id="helpSrc">' + read("help.html") + "</template>\n"
    helpsrc = read("icons.svg") + helpsrc    # иконки устройств: готовый SVG-спрайт (символы #ic-*, перекрашенные объёмные иконки атласа)
    html = page.replace("/*__JS__*/", js.replace("</script", "<\\/script")).replace("<script>\n", helpsrc + "<script>\n", 1)
    tmp = os.path.join(SRC, "_bundle.js")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    try:
        subprocess.run(["node", "--check", tmp], check=True)
    finally:
        os.remove(tmp)
    subprocess.run(["node", os.path.join(SRC, "test.js"), "12"], check=True)
    # безголовый движок для сервера комнат: тот же порядок, что в test.js (ядро без DOM)
    import json, re
    tl = re.search(r"\[('\.\./_dk_cli\.js'[^\]]+)\]", read("test.js")).group(1)
    eng = [x.strip().strip("'") for x in tl.split(",")]
    with open(os.path.join(SRC, "engine_files.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"files": eng, "note": "ядро эмулятора без DOM: загружать по порядку в vm с global.window = global (как test.js)"}, f, ensure_ascii=False, indent=1)
    out = os.path.join(D, "eltex-cli.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("OK", out, round(len(html.encode("utf-8")) / 1024), "КБ")


if __name__ == "__main__":
    sys.exit(main())
