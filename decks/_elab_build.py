# -*- coding: utf-8 -*-
"""Сборка эмулятора сети Eltex: decks/_elab/* + движок MES _dk_cli.js → один офлайн-файл decks/eltex-cli.html.
Перед записью прогоняет автотест (node decks/_elab/test.js) и node --check по итоговому скрипту."""
import os
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "_elab")
ORDER = ["../_dk_cli.js", "common.js", "esr.js", "esr_svc.js", "esr_more.js", "esr_ops.js", "mesx.js", "mes_l2.js", "mes_dialects.js", "hosts.js", "catalog.js", "net.js", "tables.js", "aging.js", "mes_full.js", "esr_fw.js", "rt_timers.js", "console.js", "frames.js", "ipv6.js", "ipv6_rt.js", "slaac.js", "dhcp6.js", "dns.js", "tunnel.js", "ipsec.js", "physics.js", "l2sec.js", "qinq.js", "mstp.js", "stp_timers.js", "dhcp_timers.js", "svc_timers.js", "snmp.js", "aaa.js", "vrf.js", "reload.js", "pbr.js", "bfd.js", "bgp.js", "bgp_policy.js", "l2tp.js", "dot1x.js", "igmp.js", "pim.js", "stack.js", "mtu.js", "scs.js", "wlc.js", "olt.js", "me.js", "me_mpls.js", "security.js", "mes10.js", "sim.js", "qos.js", "pt.js", "labs.js", "labs_routing.js", "labs_services.js", "labs_l2.js", "labs_ops.js", "labs_exam.js", "labs_faults.js", "ui.js", "ui_tools.js", "sim_ui.js", "sim_res.js", "pt_ui.js"]


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
    out = os.path.join(D, "eltex-cli.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("OK", out, round(len(html.encode("utf-8")) / 1024), "КБ")


if __name__ == "__main__":
    sys.exit(main())
