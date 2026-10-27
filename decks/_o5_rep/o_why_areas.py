# -*- coding: utf-8 -*-
"""Зачем OSPF делят на области — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import FADE
from _o5_g2kit import svg, g2_rtr, g2_db, g2_chip, g2_arrow, g2_icon_html, g2_ic, g2_rays, blob, line

W, H, TOP = 1672, 940, 128
K = "#1f1a33"

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


CARD = "rgba(255,255,255,.88)"
BRD = "border:2px solid #f3e6ee;box-shadow:0 4px 14px rgba(255,79,154,.10)"


def row(x, y, ico, html):
    return (box(x, y, 760, 76, "rgba(255,255,255,.95)", 22, "border:2px solid #f1eef4")
            + g2_icon_html(ico[0], x + 22, y + 3, 70, ico[1])
            + tx(x + 130, y + 9, 620, html, "400 24px/1.25"))


def lab(x, y, w, t, f="700 26px/1"):
    return tx(x, y, w, t, f, "text-align:center")


P1 = [(334, 346), (190, 385), (468, 401), (100, 485), (329, 457), (535, 507), (240, 569), (418, 574)]
M1 = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 4), (2, 4), (2, 5), (3, 6), (4, 6), (4, 7), (5, 7), (6, 7), (1, 6), (2, 7), (3, 4),
      (4, 5), (0, 3), (5, 6)]
NET1 = svg(blob(320, 465, 300, 165, "p", seed=2, dash=False)
           + "".join(line(P1[a], P1[b], "#f06aa5", 3) for a, b in M1)
           + "".join(g2_rtr(x, y, 92, "p", ah=32) for x, y in P1)
           + g2_db(680, 330, 120, "p", 3, "LSDB", 30)
           + g2_arrow(560, 360, 615, 335, "#ff4f9a", 6, 16) + g2_arrow(560, 395, 615, 375, "#ff4f9a", 6, 16)
           + g2_arrow(680, 470, 680, 512, "#ff4f9a", 6, 16) + g2_arrow(585, 545, 625, 565, "#ff4f9a", 6, 16)
           + g2_chip(712, 585, 118, "SPF"))
A0 = [(1148, 379), (1338, 379)]
A1 = [(964, 546), (1104, 530), (1154, 596)]
A2 = [(1388, 541), (1522, 541), (1338, 596)]
NET2 = svg(blob(1240, 380, 215, 85, "p", seed=1, dash=False) + blob(1035, 560, 190, 82, "b", seed=3, dash=False)
           + blob(1455, 560, 190, 82, "y", seed=5, dash=False)
           + line(A0[0], (1243, 410), "#f06aa5", 4) + line((1243, 410), A0[1], "#f06aa5", 4)
           + line((1010, 440), A0[0], "#f06aa5", 4) + line((1478, 440), A0[1], "#f06aa5", 4)
           + line((1010, 440), A1[0], "#f06aa5", 4) + line((1478, 440), A2[1], "#f06aa5", 4)
           + line(A1[0], A1[1], "#5aa9ee", 4) + line(A1[1], A1[2], "#5aa9ee", 4) + line(A1[0], A1[2], "#5aa9ee", 4)
           + line(A2[0], A2[1], "#f2a24a", 4, "8 6") + line(A2[0], A2[2], "#f2a24a", 4, "8 6") + line(A2[1], A2[2], "#f2a24a", 4, "8 6")
           + "".join(g2_rtr(x, y, 84, "p", ah=30) for x, y in A0) + g2_rtr(1243, 412, 50, "p", ant=False)
           + g2_rtr(1010, 440, 84, "b", ah=30) + g2_rtr(1478, 440, 84, "b", ah=30)
           + "".join(g2_rtr(x, y, 80, "b", ah=28) for x, y in A1) + "".join(g2_rtr(x, y, 80, "y", ah=28) for x, y in A2)
           + g2_db(897, 570, 56, "b", 3, "LSDB", 12) + g2_db(1602, 570, 56, "y", 3, "LSDB", 12)
           + g2_rays(1000, 420, "#5aa9ee", 30, 46, (-150, -175, 160)) + g2_rays(1490, 420, "#ffd23a", 40, 56, (-30, -5, 20)))

HTML = bg("bg5", W, H) + "".join([
    tx(55, 134, 860, "Масштабирование и локализация расчётов", "600 35px/1.2", "white-space:nowrap"),
    box(52, 180, 180, 5, "#fdd83a", 3), box(745, 176, 180, 5, "#fdd83a", 3),
    img("o_why_areas_girl2.png", "left:930px;top:128px;width:735px;" + FADE),
    '<div class="step">',
    box(20, 210, 810, 620, CARD, 26, BRD),
    pl(45, 222, 553, 68, "Одна большая область", "#fde0ec", "900 42px/1", 20),
    NET1,
    '</div><div class="step">',
    row(45, 655, ("db", "#ff9cc4"), "Все маршрутизаторы хранят<br>топологию области в LSDB."),
    row(45, 740, ("bars", "#ff9cc4"), "С ростом сети увеличиваются<br>объём базы и затраты на её обработку."),
    '</div><div class="step">',
    box(842, 210, 810, 620, CARD, 26, BRD),
    pl(868, 222, 462, 68, "Иерархия областей", "#d6e9fb", "900 42px/1", 20),
    NET2,
    lab(1200, 314, 110, "Area 0"), lab(1070, 443, 70, "ABR", "700 24px/1"), lab(1347, 443, 70, "ABR", "700 24px/1"),
    lab(925, 599, 110, "Area 1"), lab(1442, 599, 110, "Area 2"),
    '</div><div class="step">',
    row(867, 655, ("share", "#bfe0fb"), "Часть обновлений распространяется<br>в пределах области."),
    row(867, 740, ("gear", "#ffd23a"), "<b>SPF</b> (алгоритм Дейкстры) рассчитывает<br>пути по топологии своей области."),
    '</div><div class="step">',
    box(20, 842, 1632, 86, "#fdf3c4", 24),
    g2_icon_html("warn", 76, 850, 72, "#ffd23a", "#1f1a33", 2.2),
    box(222, 860, 2, 50, "#e8d68a", 1),
    tx(290, 853, 1200, "Изменения могут влиять на маршруты других областей через объявления ABR —<br>"
       "межобластные последствия возможны.", "700 25px/1.25"),
    '</div>',
])
