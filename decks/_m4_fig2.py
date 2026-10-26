# -*- coding: utf-8 -*-
"""Схемы pptx 2.4 (слайды 32–61) в стиле деки."""
import _m4_svg as S
from _m4_svg import GOLD, GOLD2, TEAL, BLUE, SOFT, INK

ORG = "#ffae5c"


def _wrap(body, vb):
    return S.fig(body, vb)


# ---------------------------------------------------------------- ПК1 — R1 — R2 (— ПК2) (pptx 38–40, 48)
def topo_line(pc2=False, ports=False, arrows=None):
    o = [S.link(150, 120, 400, 120, lab="192.168.10.0/24", pb="gi1/0/1" if ports else "", ib=".1" if ports else ""),
         S.link(456, 120, 764, 120, ia=".1", ib=".2", lab="203.0.113.0/24", pa="gi1/0/2" if ports else "", lab_dy=-26),
         S.pc(100, 110, "ПК1"), S.router(420, 120, "R1"), S.router(800, 120, "R2")]
    if pc2:
        o.insert(0, S.link(836, 120, 1050, 120, lab="192.168.20.0/24"))
        o.append(S.pc(1100, 110, "ПК2"))
    if arrows == "pkt":
        o += [S.pkt(150, 60, 400, 60, "пакет", 1, w=80), S.pkt(470, 60, 760, 60, "пакет", 2, w=80),
              S.pkt(850, 60, 1050, 60, "пакет", 3, w=80)]
    if arrows == "def":
        o += [S.arrow(470, 70, 750, 70, BLUE, p=1), S.t(610, 55, "Статический маршрут", 14, BLUE, 800, p=1),
              S.arrow(470, 175, 750, 175, TEAL, p=2), S.t(610, 205, "0.0.0.0/0", 14, TEAL, 800, p=2)]
    return _wrap("".join(o), "0 0 1200 230")


# ---------------------------------------------------------------- 4 сети за R1 и R2 (pptx 41, 53–55, 62–66)
def topo_big(ports=True, extra="", r2ports=False):
    o = [S.link(150, 80, 265, 80), S.link(335, 90, 450, 210, pb="Gi1/0/1" if ports else "", ib=".1"),
         S.link(150, 380, 265, 380), S.link(335, 370, 450, 250, pb="Gi1/0/2" if ports else "", ib=".1"),
         S.link(500, 230, 700, 230, pa="Gi1/0/3" if ports else "", ia=".1", ib=".2", pb="Gi1/0/1" if r2ports else "",
                lab="203.0.113.0/24", lab_dy=-26),
         S.link(750, 210, 865, 90, ia=".1"), S.link(750, 250, 865, 370, ia=".1"),
         S.link(935, 80, 1050, 80), S.link(935, 380, 1050, 380),
         S.pc(100, 70, "ПК1", [".254"]), S.switch(300, 80, w=70, h=32), S.t(210, 40, "192.168.10.0/24", 15, GOLD2, 800),
         S.pc(100, 370, "ПК2", [".254"]), S.switch(300, 380, w=70, h=32), S.t(210, 455, "192.168.20.0/24", 15, GOLD2, 800),
         S.router(475, 230, "R1"), S.router(725, 230, "R2"),
         S.switch(900, 80, w=70, h=32), S.pc(1100, 70, "ПК3", [".254"]), S.t(990, 40, "10.10.10.0/24", 15, GOLD2, 800),
         S.switch(900, 380, w=70, h=32), S.pc(1100, 370, "ПК4", [".254"]), S.t(990, 455, "10.10.20.0/24", 15, GOLD2, 800)]
    return _wrap("".join(o) + extra, "0 0 1200 470")


# ---------------------------------------------------------------- автономные системы (pptx 43)
def topo_as():
    P = {"a1": (330, 110), "a2": (170, 170), "a3": (190, 330), "a4": (360, 360), "ab": (500, 230),
         "bb": (720, 230), "b1": (880, 130), "b2": (960, 300)}
    o = ['<ellipse cx="340" cy="240" rx="270" ry="200" fill="rgba(255,174,92,.10)" stroke="%s" stroke-width="2"/>' % ORG,
         '<ellipse cx="850" cy="230" rx="220" ry="180" fill="rgba(63,214,176,.10)" stroke="%s" stroke-width="2"/>' % TEAL,
         S.t(300, 455, "AS 65540", 17, ORG, 900), S.t(300, 480, "IGP: RIP, OSPF, IS-IS, iBGP", 14, SOFT, 700),
         S.t(870, 440, "AS 65545", 17, TEAL, 900), S.t(870, 465, "IGP: RIP, OSPF, IS-IS, iBGP", 14, SOFT, 700),
         S.t(610, 205, "EGP: eBGP", 16, GOLD2, 900)]
    for a, b in (("a2", "a1"), ("a1", "ab"), ("a2", "a3"), ("a3", "a4"), ("a4", "ab"), ("ab", "bb"), ("bb", "b1"),
                 ("b1", "b2"), ("bb", "b2")):
        o.append(S.link(P[a][0], P[a][1], P[b][0], P[b][1], w=4 if a == "ab" else 3))
    for x, y in P.values():
        o.append(S.router(x, y, r=28))
    return _wrap("".join(o), "0 0 1200 495")


# ---------------------------------------------------------------- тупиковые сети (pptx 47)
def topo_stub():
    o = ['<rect x="20" y="20" width="380" height="170" rx="14" fill="rgba(255,174,92,.10)" stroke="%s" stroke-dasharray="7 5"/>' % ORG,
         '<rect x="20" y="250" width="380" height="170" rx="14" fill="rgba(240,199,94,.10)" stroke="%s" stroke-dasharray="7 5"/>' % GOLD,
         S.t(40, 48, "Тупиковать сеть", 15, ORG, 800, "start"), S.t(210, 178, "172.16.0.0/16", 15, GOLD2, 800),
         S.t(40, 278, "Тупиковать сеть", 15, GOLD2, 800, "start"), S.t(210, 408, "172.19.0.0/16", 15, GOLD2, 800),
         S.link(140, 110, 245, 110), S.link(315, 120, 520, 210), S.link(140, 340, 245, 340), S.link(315, 330, 520, 230),
         S.link(570, 220, 820, 220, ia=".1", ib=".2", lab="203.0.113.0/30", lab_dy=-24), S.link(880, 220, 1000, 220),
         S.pc(90, 100, "ПК1"), S.switch(280, 110, w=70, h=32), S.pc(90, 330, "ПК1"), S.switch(280, 340, w=70, h=32),
         S.router(545, 220, "R1"), S.router(850, 220, "R2"), S.cloud(1090, 220, "Другие сети", 160, 70),
         S.t(545, 110, "Тупиковый маршрутизатор", 15, GOLD2, 800), S.arrow(545, 120, 545, 178)]
    return _wrap("".join(o), "0 0 1200 440")


# ---------------------------------------------------------------- RIB → FIB (pptx 36)
def rib_fib():
    o = []
    for x, nm in ((260, "OSPF"), (450, "RIP"), (640, "..."), (830, "BGP")):
        o.append(S.badge(x, 50, nm, ORG, size=17))
        o.append(S.arrow(x, 72, x, 150))
    o += [S.t(250, 120, "10.0.0.0/8 via 172.16.0.1", 13, SOFT, 700, "end", mono=True),
          S.t(845, 105, "10.0.0.0/8 via 192.168.0.1", 13, SOFT, 700, "start", mono=True),
          S.t(845, 125, "10.0.0.0/16 via 192.168.0.2", 13, SOFT, 700, "start", mono=True),
          '<rect x="200" y="160" width="700" height="80" rx="12" fill="rgba(255,174,92,.18)" stroke="%s" stroke-width="2"/>' % ORG,
          S.t(550, 212, "RIB", 26, ORG, 900), S.arrow(550, 242, 550, 322),
          S.t(540, 278, "10.0.0.0/8 via 172.16.0.1", 13, SOFT, 700, "end", mono=True),
          S.t(540, 298, "10.0.0.0/16 via 192.168.0.2", 13, SOFT, 700, "end", mono=True),
          '<rect x="300" y="330" width="500" height="80" rx="12" fill="rgba(108,184,255,.18)" stroke="%s" stroke-width="2"/>' % BLUE,
          S.t(550, 382, "FIB", 26, BLUE, 900),
          S.t(110, 340, "traffic", 15, SOFT, 700), S.t(110, 365, "Dst 10.1.1.1", 13, INK, 700, mono=True),
          S.t(110, 395, "Dst 10.0.1.1", 13, INK, 700, mono=True), S.arrow(180, 375, 295, 370, BLUE, p=1),
          S.arrow(805, 350, 940, 350, BLUE, p=2), S.t(950, 345, "Dst 10.1.1.1", 13, INK, 700, "start", mono=True),
          S.t(950, 363, "via 172.16.0.1", 13, GOLD2, 700, "start", mono=True, p=2),
          S.arrow(805, 395, 940, 395, BLUE, p=3), S.t(950, 395, "Dst 10.0.1.1", 13, INK, 700, "start", mono=True),
          S.t(950, 413, "via 192.168.0.2", 13, GOLD2, 700, "start", mono=True, p=3)]
    return _wrap("".join(o), "0 0 1200 440")


# ---------------------------------------------------------------- программная коммутация (pptx 32)
def soft_switch():
    o = ['<rect x="200" y="30" width="800" height="380" rx="26" fill="rgba(240,199,94,.10)" stroke="%s" stroke-width="2"/>' % GOLD,
         '<rect x="240" y="70" width="90" height="300" rx="8" fill="rgba(255,150,180,.22)" stroke="#ff9fbf"/>',
         S.t(285, 300, "Входной", 13, "#ffc1d6", 800), S.t(285, 318, "интерфейс", 13, "#ffc1d6", 800),
         '<rect x="870" y="70" width="90" height="300" rx="8" fill="rgba(190,160,255,.22)" stroke="#c9b3ff"/>',
         S.t(915, 300, "Выходной", 13, "#d8c6ff", 800), S.t(915, 318, "интерфейс", 13, "#d8c6ff", 800),
         '<rect x="370" y="60" width="460" height="100" rx="10" fill="rgba(155,227,122,.2)" stroke="#9be37a"/>',
         S.t(600, 100, "Уровень управления", 17, "#c9f2b4", 900), S.t(600, 128, "Центральный процессор", 14, SOFT, 700),
         '<rect x="370" y="290" width="460" height="90" rx="10" fill="rgba(255,174,92,.2)" stroke="%s"/>' % ORG,
         S.t(600, 342, "Уровень пересылки пакетов", 17, "#ffd2a8", 900)]
    for i, y in enumerate((200, 228, 256)):
        k = i * 26
        col = (GOLD, TEAL, BLUE)[i]
        o.append('<path d="M60 %g H%g V%g H%g V%g H1140" fill="none" stroke="%s" stroke-width="3" marker-end="url(#m4a)" data-ph="%d"/>'
                 % (y, 400 + k, 175 + k * .6, 800 - k, y, col, i + 1))
        o.append(S.t(110, y - 6, "Пакет №%d" % (i + 1), 13, INK, 700))
        o.append(S.t(1090, y - 6, "Пакет №%d" % (i + 1), 13, INK, 700))
    return _wrap("".join(o), "0 0 1200 430")


# ---------------------------------------------------------------- иерархия маршрутов (pptx 58–60)
def _rowblock(x, y, kind, pref, w=(170, 190, 230), parent=False):
    o = ['<rect x="%g" y="%g" width="%g" height="38" rx="7" fill="rgba(108,184,255,.18)" stroke="%s"/>' % (x, y, w[0], BLUE),
         S.t(x + w[0] / 2.0, y + 25, kind, 14, "#cfe6ff", 800),
         '<rect x="%g" y="%g" width="%g" height="38" rx="7" fill="rgba(240,199,94,.18)" stroke="%s"/>' % (x + w[0] + 10, y, w[1], GOLD),
         S.t(x + w[0] + 10 + w[1] / 2.0, y + 25, pref, 14, GOLD2, 800, mono=True)]
    if not parent:
        x2 = x + w[0] + w[1] + 120
        o += [S.arrow(x + w[0] + w[1] + 14, y + 19, x2 - 4, y + 19), S.t((x + w[0] + w[1] + x2) / 2.0 + 6, y + 10, "Окончательный маршрут", 11, SOFT, 700),
              '<rect x="%g" y="%g" width="%g" height="38" rx="7" fill="rgba(155,227,122,.18)" stroke="#9be37a"/>' % (x2, y, w[2]),
              S.t(x2 + w[2] / 2.0, y + 25, "Путь/Интерфейс", 14, "#c9f2b4", 800)]
    return "".join(o)


def levels(parent=False):
    hdr = [S.t(120, 30, "Маршрут 1-го уровня", 15, GOLD2, 900), S.t(880, 30, "IP-адрес следующего перехода", 13, SOFT, 700),
           S.t(880, 48, "и/или выходной интрефейс", 13, SOFT, 700)]
    o = hdr + [_rowblock(20, 70, "Сеть", "10.10.10.0/24"), _rowblock(20, 130, "Суперсеть", "10.10.0.0/16"),
               _rowblock(20, 190, "По умолчанию", "0.0.0.0/0")]
    h = 250
    if parent:
        o += ['<rect x="20" y="270" width="170" height="38" rx="7" fill="rgba(255,174,92,.2)" stroke="%s"/>' % ORG,
              S.t(105, 262, "Родительский маршрут", 13, ORG, 800), S.t(105, 295, "Сеть", 14, "#ffd2a8", 800),
              '<rect x="20" y="340" width="170" height="38" rx="7" fill="rgba(190,160,255,.2)" stroke="#c9b3ff"/>',
              S.t(105, 332, "Дочерний маршрут", 13, "#d8c6ff", 800), S.t(105, 365, "Подсеть", 14, "#e6dbff", 800),
              S.arrow(105, 310, 105, 336, ORG),
              S.t(300, 295, "10.20.0.0/16", 14, TEAL, 800, mono=True), S.t(300, 330, "210.7.222.0", 14, TEAL, 800, mono=True),
              S.t(420, 285, "10.20.1.0/24 / ... / 10.20.40.0/24 / ... / 10.20.70.0/24", 13, TEAL, 700, "start", mono=True),
              S.t(420, 330, "210.7.222.1/30; 210.7.222.5/30; 210.7.222.9/30; 210.7.222.13/30", 13, TEAL, 700, "start", mono=True),
              S.arrow(860, 300, 930, 300), '<rect x="935" y="281" width="230" height="38" rx="7" fill="rgba(155,227,122,.18)" stroke="#9be37a"/>',
              S.t(1050, 306, "Путь/Интерфейс", 14, "#c9f2b4", 800)]
        h = 400
    return _wrap("".join(o), "0 0 1200 %d" % h)
