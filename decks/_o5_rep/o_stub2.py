# -*- coding: utf-8 -*-
"""2. Stub (вариант 2): Area 0 -> ABR -> Stub, LSA-3 по умолчанию, LSA-5 не входит. Всё нарисовано в SVG."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_ikit import puck, line, chip, cross, svg, g4_arr, g4_doc, g4_tower, g4_area

W, H, TOP = 1672, 940, 0
INK = "#1f1a33"
BL, PK, YE = "#2f8fe8", "#ff5c9e", "#ffc400"


def pill(cx, cy, w, h, fill, text, fs=40, ink=INK, wt=800, rx=None):
    return ('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="%d" style="fill:%s"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" font-weight="%d" style="fill:%s">%s</text>'
            % (cx - w / 2.0, cy - h / 2.0, w, h, rx if rx is not None else h // 2, fill, cx, cy + fs * .35, fs, wt, ink, text))


def t(x, y, s, fs=22, wt=700, ink=INK, anchor="middle"):
    return ('<text x="%d" y="%d" text-anchor="%s" font-size="%s" font-weight="%d" style="fill:%s">%s</text>'
            % (x, y, anchor, fs, wt, ink, s))


def scene():
    o = [g4_area(30, 300, 760, 400, "b", 70), g4_area(800, 240, 840, 660, "y", 90),
         pill(415, 285, 210, 70, "#cfe4fa", "Area 0", 44), pill(1258, 282, 180, 72, "#ffe14d", "Stub", 46)]
    # линии Area 0
    for a, b in [((300, 400), (515, 430)), ((120, 470), (310, 570)), ((515, 430), (765, 495)),
                 ((310, 570), (765, 505)), ((150, 580), (310, 580))]:
        o.append(line(a, b, "#9fcaf3", 16))
        o.append(line(a, b, "#fff", 3, "14 10"))
    for a, b in [((765, 500), (1480, 385)), ((1480, 385), (1500, 600)), ((765, 500), (1500, 600))]:
        o.append(line(a, b, "#cfe4fa", 14))
    o += [g4_tower(60, 360, 52, 110), g4_tower(122, 340, 56, 125), g4_tower(190, 330, 58, 110),
          g4_tower(258, 350, 48, 90), g4_tower(48, 525, 60, 115)]
    o += [puck(515, 420, 160, "p"), puck(310, 555, 190, "p"), puck(765, 485, 230, "b", "ABR", 36),
          puck(1480, 375, 190, "p"), puck(1500, 590, 200, "p")]
    return svg("".join(o), W, H)


IPS = ["10.1.0.0/16", "10.2.0.0/16", "10.3.0.0/16", "…"]


def card_lsa3():
    o = ['<rect x="176" y="660" width="450" height="232" rx="26" style="fill:#e7f1fc" stroke="#b9d7f6" stroke-width="2.5"/>',
         t(400, 700, "Подробные межобластные", 24), t(400, 732, "маршруты: LSA-3", 24),
         '<rect x="200" y="748" width="404" height="128" rx="18" style="fill:#fff"/>',
         g4_doc(250, 754, 92, "LSA-3", "w", fs=21)]
    for k, s in enumerate(IPS):
        o.append(pill(490, 768 + k * 33, 200, 28, "#cfe3fa", s, 19, "#1d5fb8", 600, 8))
    o.append(g4_arr(620, 735, 745, 595, BL, 9, curve=-50))
    return svg("".join(o), W, H)


def card_lsa12():
    o = ['<rect x="936" y="660" width="404" height="232" rx="26" style="fill:#fff8dd" stroke="#f3dc8a" stroke-width="2.5"/>',
         t(1128, 700, "Внутренняя топология:", 24), t(1128, 732, "LSA-1 и LSA-2", 24),
         '<rect x="980" y="748" width="316" height="128" rx="18" style="fill:#fff"/>',
         g4_doc(1022, 754, 92, "LSA-1", "p", "tri", 21), g4_doc(1176, 754, 92, "LSA-2", "b", "tri", 21),
         g4_arr(1345, 775, 1440, 690, "#ffc400", 9, curve=-40)]
    return svg("".join(o), W, H)


def default_route():
    o = ['<path d="M870 470 L1350 438 L1348 412 L1400 462 L1356 508 L1354 482 L874 514 z" style="fill:%s"/>' % BL,
         '<text x="1120" y="478" text-anchor="middle" font-size="22" font-weight="800" transform="rotate(-3.6 1120 470)" '
         'style="fill:#fff">0.0.0.0/0 • LSA-3 • маршрут по умолчанию</text>']
    return svg("".join(o), W, H)


def unknown():
    o = [g4_arr(1395, 625, 905, 538, BL, 7, dash="16 10", curve=-50),
         pill(1183, 573, 370, 52, "#e8f2fd", "Неизвестный маршрут → к ABR", 21, INK, 700, 16)]
    return svg("".join(o), W, H)


def lsa5():
    o = [pill(667, 208, 336, 54, "#ffd3e2", "LSA-5 не входит в Stub", 23, INK, 700, 16),
         g4_arr(520, 258, 800, 300, PK, 7, dash="14 10"), cross(686, 272, 24, "#f0214f", 11),
         # ASBR, перечёркнутый
         puck(1010, 120, 240, "k", "ASBR", 36),
         '<circle cx="1022" cy="92" r="62" fill="none" stroke="%s" stroke-width="12" opacity=".75"/>' % PK,
         line((982, 52), (1062, 132), PK, 12), line((1062, 52), (982, 132), PK, 12),
         '<path d="M878 52 l6 30 M1150 52 l-8 30" stroke="#f0214f" stroke-width="7" stroke-linecap="round"/>',
         line((1132, 150), (1212, 120), PK, 3, "6 6"),
         '<rect x="1214" y="60" width="424" height="128" rx="22" style="fill:#fde0ea"/>',
         t(1230, 104, "ASBR внутри Stub не размещают:", 23, 800, INK, "start"),
         t(1230, 136, "внешние маршруты не попадут", 22, 400, INK, "start"),
         t(1230, 166, "в область обычным способом", 22, 400, INK, "start")]
    return svg("".join(o), W, H)


HTML = bg("bg3", W, H) + "".join('<div class="step">%s</div>' % s for s in [
    scene(), card_lsa3(), card_lsa12(), default_route(), unknown(), lsa5()])
