# -*- coding: utf-8 -*-
"""Состояния соседства OSPF — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_g2kit import (svg, g2_rtr, g2_doc, g2_db, g2_arrow, g2_path, g2_rays, g2_lbl, g2_icon_html, line)
from _o5_ikit import FADE

W, H, TOP = 1672, 941, 296
K = "#1f1a33"
PK, BL, YL = "#ffa9cb", "#5aa9ee", "#fdd84a"

def box(x, y, w, h, fill, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, fill, r, ex))


def fnt(f):
    """'700 30px/1 Oswald' -> Oswald, иначе Golos Text."""
    if f.endswith(" Oswald"):
        return f[:-7] + " Oswald,sans-serif"
    return f + " 'Golos Text',sans-serif"


def tx(x, y, w, html, f="500 26px/1.3", ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%s;color:%s;%s">%s</div>'
            % (x, y, w, fnt(f), K, ex, html))


def pl(x, y, w, h, html, fill, f="700 26px/1.2", r=16, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;display:flex;align-items:center;justify-content:center;text-align:center;'
            'font:%s;color:%s;%s">%s</div>' % (x, y, w, h, fill, r, fnt(f), K, ex, html))


CARDS = [  # x0, x1, номер-цвет, фон, имя, текст, y текста
    (17, 222, "#ff7fb0", "#fde9f1", "Down", "Hello ещё<br>не получен", 724),
    (236, 428, BL, "#eaf4fd", "Init", "Hello получен", 724),
    (441, 708, YL, "#fff8dc", "2-Way", "Маршрутизаторы<br>увидели друг друга", 676),
    (722, 940, "#ff7fb0", "#fde9f1", "ExStart", "Согласование<br>обмена", 715),
    (954, 1191, BL, "#eaf4fd", "Exchange", "Обмен описаниями<br>баз данных DBD", 719),
    (1205, 1432, YL, "#fff8dc", "Loading", "Запрос<br>недостающих LSA", 717),
    (1446, 1658, "#ff7fb0", "#fde9f1", "Full", "Базы состояний<br>каналов<br>синхронизированы", 706),
]
ARX = [202, 412, 690, 922, 1172, 1414]


def _pair(xb, xp, y, w=85):
    return g2_rtr(xb, y, w, "b", ah=w * .75) + g2_rtr(xp, y, w, "p", ah=w * .75)


def _bub(x, y, w, h, fill="#fff", edge="#3a3f55"):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" style="fill:%s;stroke:%s" stroke-width="3"/>'
            '<path d="M%d %d l-8 16 l20 -16" style="fill:%s;stroke:%s" stroke-width="3" stroke-linejoin="round"/>'
            '<path d="M%d %d h16" style="stroke:%s" stroke-width="4"/>'
            % (x, y, w, h, h // 2, fill, edge, x + 18, y + h - 1, fill, edge, x + 16, y + h - 1, fill))


ILL = [
    g2_rtr(115, 615, 150, "k", ah=95) + _bub(140, 532, 74, 46)
    + "".join('<circle cx="%d" cy="555" r="5" style="fill:#3a3f55"/>' % (161 + 16 * k) for k in range(3)),
    _pair(288, 380, 640, 78) + _bub(286, 548, 86, 62, "#d6eafd", "#9fcaf3")
    + '<text x="329" y="574" text-anchor="middle" font-size="20" font-weight="700" style="fill:#1f1a33">Hello</text>'
    + g2_arrow(312, 592, 348, 592, "#1d5fa8", 4, 10),
    _pair(507, 640, 615, 92) + g2_arrow(548, 560, 602, 560, BL, 7, 16) + g2_arrow(602, 585, 548, 585, "#ff7fb0", 7, 16)
    + g2_rays(575, 545, "#ffd23a", 8, 22, (-60, -90, -120)),
    _pair(775, 892, 640, 82) + g2_doc(831, 560, 48)
    + g2_path("M772 600 Q775 560 803 548", BL, 5, "ab") + g2_path("M858 548 Q890 560 890 598", "#ff7fb0", 5, "ap")
    + g2_rays(870, 528, "#ffd23a", 6, 18, (-40, -70)),
    _pair(1010, 1135, 650, 82) + g2_lbl(1052, 556, "DBD", "#fff", 17, 56, 34) + g2_lbl(1092, 590, "DBD", "#fff", 17, 56, 34)
    + '<rect x="1024" y="539" width="56" height="34" rx="8" fill="none" stroke="#3a3f55" stroke-width="2.5"/>'
      '<rect x="1064" y="573" width="56" height="34" rx="8" fill="none" stroke="#3a3f55" stroke-width="2.5"/>'
    + g2_path("M1050 642 H1095", BL, 5, "ab", None, True) + g2_rays(1120, 540, "#ffd23a", 6, 18, (-40, -70)),
    _pair(1255, 1385, 650, 82) + '<rect x="1288" y="532" width="60" height="70" rx="6" style="fill:#fff;stroke:#3a3f55" stroke-width="3"/>'
    + '<text x="1318" y="563" text-anchor="middle" font-size="20" font-weight="800" style="fill:#1f1a33">LSA</text>'
    + '<path d="M1298 578h40M1298 588h28" stroke="#ffb3d1" stroke-width="4" stroke-linecap="round"/>'
    + g2_arrow(1295, 615, 1350, 615, "#ff7fb0", 5, 12) + g2_arrow(1350, 632, 1295, 632, BL, 5, 12)
    + g2_rays(1318, 540, "#ffd23a", 40, 54, (-30, -150)),
    _pair(1497, 1610, 655, 76) + g2_db(1552, 548, 54, "b", 3)
    + g2_path("M1530 648 H1575", BL, 5, "ab", None, True)
    + g2_rays(1552, 585, "#ffd23a", 48, 64, (-20, -55, -125, -160)) + g2_rays(1552, 640, "#ffd23a", 34, 46, (80, 100)),
]


def card(i, c):
    x0, x1, nc, fill, name, t, ty = c
    w = x1 - x0
    out = [
        '<div class="step">',
        box(x0, 437, w, 380, fill, 18, "border:2px solid rgba(255,255,255,.95)"),
        pl(x0 + 14, 455, 54, 54, str(i + 1), nc, "700 30px/1", 27, "color:#fff"),
        tx(x0 + 92, 461, w - 92, name, "600 34px/1 Oswald"),
        svg(ILL[i]),
        tx(x0, ty, w, t, "400 22px/1.22", "text-align:center"),
    ]
    if i:
        out.append(svg(g2_arrow(ARX[i - 1] + 4, 575, ARX[i - 1] + 44, 575, "#ff7fb0" if i % 2 else BL, 9, 20)))
    if i == 2:
        out += [box(447, 748, 256, 64, "#fdec86", 14),
                g2_icon_html("bulb", 452, 758, 40, "#ffd23a"),
                tx(497, 755, 210, "В общей Ethernet-сети<br>выбираются DR и BDR.", "500 19px/1.22 Oswald")]
    out.append('</div>')
    return "".join(out)


HTML = bg("bg2", W, H) + "".join([
    tx(38, 304, 560, "От обнаружения маршрутизатора<br>до синхронизации баз данных", "600 29px/1.2"),
    '<div class="step">',
    svg(line((885, 372), (1296, 372), "#8cc4f5", 7) + line((1030, 372), (1296, 372), "#ff9cc4", 7)
        + '<rect x="900" y="344" width="130" height="56" rx="10" style="fill:#e3ecf8;stroke:#7c8db0" stroke-width="3"/>'
        + "".join('<rect x="%d" y="362" width="14" height="14" rx="2" style="fill:#2a2f3d"/>' % (912 + 22 * k) for k in range(5))),
    img("o_nbr_states_cat.png", "left:1050px;top:309px;width:190px;" + FADE),
    pl(602, 330, 283, 85, "R1 — BDR<br>203.0.113.1/24", "#dcecfb", "600 26px/1.2", 16,
       "border:2px solid #9ccaf3;color:#1d5fa8"),
    pl(1296, 330, 286, 85, "R2 — DR<br>203.0.113.2/24", "#fde3ee", "600 26px/1.2", 16,
       "border:2px solid #f7a8c8;color:#a3134f"),
    '</div>',
    "".join(card(i, c) for i, c in enumerate(CARDS)),
    '<div class="step">',
    box(372, 847, 896, 66, "#eef6fd", 33, "border:2px solid #b8d9f5"),
    g2_icon_html("info", 384, 849, 60, "#3a8ff0", "#fff", 2.4),
    tx(497, 867, 760, "На соединении точка-точка выбор DR/BDR обычно не требуется.", "400 22px/1.2"),
    '</div>',
])
