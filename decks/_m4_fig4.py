# -*- coding: utf-8 -*-
"""Схемы pptx 2.4 (слайды 76–94): маршрутизация между VLAN — традиционный метод, Router-on-a-Stick, коммутатор L3.
Цвета как в тексте/конфигурации pptx: VLAN 10 — красный, VLAN 20 — синий, нетегированный — золото."""
import _m4_svg as S
from _m4_svg import GOLD, GOLD2, TEAL, SOFT

V10 = "#ff6b5c"
V20 = "#6cb8ff"
PCS = {"PC-1": ("10.10.1.15", "AA:BB:CC:33:44:01", "10.10.1.1"), "PC-2": ("10.10.2.10", "AA:BB:CC:33:44:02", "10.10.2.1"),
       "PC-3": ("10.10.1.25", "AA:BB:CC:33:44:03", "10.10.1.1"), "PC-4": ("10.10.2.20", "AA:BB:CC:33:44:04", "10.10.2.1")}


def _wrap(body, vb):
    return S.fig(body, vb)


def _pc(x, y, nm, info=True):
    ip, mac, gw = PCS[nm]
    return S.pc(x, y, nm, ["IP: " + ip, "MAC: " + mac, "DG: " + gw] if info else [])


def frame(x, y, f, tag=None, rev=False, h=34, size=11.5):
    """f = (dest_ip, src_ip, src_mac, dst_mac); tag = 10 | 20 | None."""
    dip, sip, smac, dmac = f
    cells = [("Payload", 70, S.F_PAY), ("Dest IP\n" + dip, 92, S.F_IP), ("Source IP\n" + sip, 92, S.F_IP)]
    if tag:
        cells.append(("VLAN ID\n%d" % tag, 62, V10 if tag == 10 else V20))
    cells += [("Source MAC\n" + smac, 140, S.F_MAC), ("Dest MAC\n" + dmac, 140, S.F_MAC)]
    if rev:
        cells = cells[::-1]
    return S.frame(x, y, cells, h, size=size)


def legend(x, y):
    return ('<g>%s%s%s%s%s%s</g>' % (S.link(x, y, x + 40, y, V10, 4), S.t(x + 50, y + 5, "VLAN 10", 13, V10, 800, "start"),
                                     S.link(x + 140, y, x + 180, y, V20, 4), S.t(x + 190, y + 5, "VLAN 20", 13, V20, 800, "start"),
                                     S.link(x + 280, y, x + 320, y, GOLD, 4), S.t(x + 330, y + 5, "нетегированный трафик", 13, GOLD, 800, "start")))


def trunk(x1, y1, x2, y2, pa="", pb=""):
    dx, dy = (y2 - y1), -(x2 - x1)
    L = (dx * dx + dy * dy) ** .5 or 1
    ox, oy = dx / L * 4, dy / L * 4
    return ('<path d="M%g %gL%g %g" stroke="rgba(255,150,180,.25)" stroke-width="18" stroke-linecap="round"/>' % (x1, y1, x2, y2)
            + S.link(x1 + ox, y1 + oy, x2 + ox, y2 + oy, V10, 3, pa=pa) + S.link(x1 - ox, y1 - oy, x2 - ox, y2 - oy, V20, 3, pb=pb))


# ---------------------------------------------------------------- традиционный метод (pptx 77–83)
def legacy(fr=None, sw="both", leg=True, extra=""):
    """fr = (x, y, f, tag, rev) — кадр на схеме; sw = 'both' | 'sw1' | 'sw2'."""
    o = []
    R = (600, 70)
    o.append(S.t(380, 40, "Gi1/0/1  IP: 10.10.1.1  MAC:AA:BB:CC:11:22:01", 12.5, SOFT, 700, "end", mono=True))
    o.append(S.t(820, 40, "Gi1/0/2  IP: 10.10.2.1  MAC:AA:BB:CC:11:22:02", 12.5, SOFT, 700, "start", mono=True))
    if sw in ("both", "sw1"):
        o += [S.link(570, 90, 330, 220, pa="Gi1/0/1", pb="Fa0/22"),
              S.link(270, 250, 140, 350, V10, pb="", pa="Fa0/1"), S.link(320, 250, 420, 350, V20, pa="Fa0/2"),
              S.switch(300, 235, "L2SW-1"), _pc(130, 390, "PC-1"), _pc(430, 390, "PC-2")]
    if sw in ("both", "sw2"):
        o += [S.link(630, 90, 870, 220, pa="Gi1/0/2", pb="Fa0/22"),
              S.link(880, 250, 780, 350, V10, pa="Fa0/1"), S.link(930, 250, 1060, 350, V20, pa="Fa0/2"),
              S.switch(900, 235, "L2SW-2"), _pc(770, 390, "PC-3"), _pc(1070, 390, "PC-4")]
    if sw == "both":
        o.insert(0, trunk(360, 235, 840, 235, "Fa0/24", "Fa0/24"))
    o.append(S.router(R[0], R[1], "R1"))
    if leg:
        o.append(legend(330, 545))
    if fr:
        x, y, f, tag, rev = fr
        o.append(frame(x, y, f, tag, rev))
    return _wrap("".join(o) + extra, "0 0 1200 560")


# ---------------------------------------------------------------- Router-on-a-Stick (pptx 84–88)
def roas(fr=None, extra=""):
    o = [trunk(340, 260, 840, 260, "Fa0/24", ""),
         '<ellipse cx="880" cy="260" rx="26" ry="40" fill="rgba(255,150,180,.18)" stroke="#ff9fbf" stroke-width="2"/>',
         '<circle cx="880" cy="245" r="7" fill="%s"/><circle cx="880" cy="275" r="7" fill="%s"/>' % (V10, V20),
         S.t(930, 200, "Gi1/0/1.10", 14, V10, 900, "start", mono=True),
         S.t(930, 218, "IP: 10.10.1.1  MAC:A2:BB:CC:11:22:A1", 12, SOFT, 700, "start", mono=True),
         S.t(930, 318, "Gi1/0/1.20", 14, V20, 900, "start", mono=True),
         S.t(930, 336, "IP: 10.10.2.1  MAC:A2:BB:CC:11:22:A2", 12, SOFT, 700, "start", mono=True),
         S.link(270, 250, 150, 140, V10, pa="Fa0/1"), S.link(270, 275, 150, 390, V20, pa="Fa0/2"),
         S.switch(300, 260, "L2SW-1"), S.router(1040, 260, "R1"), _pc(100, 100, "PC-1"), _pc(100, 380, "PC-2")]
    if fr:
        x, y, f, tag, rev = fr
        o.append(frame(x, y, f, tag, rev))
    return _wrap("".join(o) + extra, "0 0 1200 520")


# ---------------------------------------------------------------- коммутатор L3 (pptx 89–94)
def l3(fr=None, arc=False, extra=""):
    o = [trunk(560, 110, 330, 250, "Gi1/0/1", "Fa0/24"), trunk(640, 110, 870, 250, "Gi1/0/2", "Fa0/24"),
         S.link(270, 280, 140, 380, V10, pa="Fa0/1"), S.link(320, 280, 420, 380, V20, pa="Fa0/2"),
         S.link(880, 280, 780, 380, V10, pa="Fa0/1"), S.link(930, 280, 1060, 380, V20, pa="Fa0/2"),
         S.switch(600, 90, "L3SW", l3=True, col=GOLD), S.switch(300, 265, "L2SW-1"), S.switch(900, 265, "L2SW-2"),
         '<circle cx="545" cy="90" r="7" fill="%s"/><circle cx="655" cy="90" r="7" fill="%s"/>' % (V10, V20),
         S.t(530, 40, "VLAN 10", 13, V10, 900, "end"), S.t(530, 58, "IP: 10.10.1.1  MAC:0C:BB:AA:11:22:31", 12, SOFT, 700, "end", mono=True),
         S.t(670, 40, "VLAN 20", 13, V20, 900, "start"), S.t(670, 58, "IP: 10.10.2.1  MAC:0C:BB:AA:11:22:32", 12, SOFT, 700, "start", mono=True),
         _pc(130, 420, "PC-1"), _pc(430, 420, "PC-2"), _pc(770, 420, "PC-3"), _pc(1070, 420, "PC-4")]
    if arc:
        o.append('<path d="M150 400 Q300 60 600 120 Q900 60 1060 400" fill="none" stroke="#b07cff" stroke-width="7" '
                 'marker-end="url(#m4a)" opacity=".85" class="flow" data-ph="1"/>')
    if fr:
        x, y, f, tag, rev = fr
        o.append(frame(x, y, f, tag, rev))
    return _wrap("".join(o) + extra, "0 0 1200 560")


def rtable(rows, hl):
    """«IP Routing Table» из pptx: rows = [(код, сеть, интерфейс)]."""
    return S.fig(S.table(20, 10, ["", "IP Routing Table", ""], [list(r) for r in rows], [60, 220, 160], hl=hl, size=16), "0 0 480 110")
