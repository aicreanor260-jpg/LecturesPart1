# -*- coding: utf-8 -*-
"""Стоимость OSPF — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import line, svg, cloud_icon
from _o5_g1kit import g1icon, g1antpuck

W, H, TOP = 1672, 941, 212
K = "#1f1a33"
PK, BL, YL = "#fbd1e2", "#cfe5fb", "#fdec9c"


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


CARD = "rgba(255,255,255,.9)"
SH = "box-shadow:0 4px 14px rgba(255,79,154,.12);border:2px solid #f6e3ec"

HTML = bg("bg7", W, H) + "".join([
    tx(70, 222, 720, "Метрика выбора кратчайшего маршрута", "500 33px/1.2", "white-space:nowrap"),
    img("o_cost_girl2.png", "left:790px;top:205px;width:545px;-webkit-mask:linear-gradient(90deg,transparent,#000 15%,#000 85%,transparent);mask:linear-gradient(90deg,transparent,#000 15%,#000 85%,transparent)"),
    svg(g1antpuck(1480, 250, 120, "p") + g1antpuck(1610, 262, 100, "b")),
    '<div class="step">',
    box(25, 308, 732, 464, CARD, 24, SH),
    box(45, 322, 692, 84, "#fdeef4", 20),
    g1icon("gear", 52, 330, 70, "p"),
    tx(148, 326, 560, "Формула расчета стоимости<br>интерфейса OSPF", "800 31px/1.15"),
    '</div><div class="step">',
    box(43, 420, 694, 220, "#fff6fa", 18, "border:2px solid #f6e3ec"),
    pl(63, 467, 222, 113, "Стоимость<br>интерфейса", PK, "700 29px/1.2", 20),
    tx(294, 488, 40, "=", "800 48px/1"),
    pl(345, 438, 371, 72, "эталонная пропускная<br>способность", BL, "600 22px/1.25"),
    box(340, 520, 382, 4, K, 2),
    pl(345, 538, 371, 76, "пропускная способность<br>интерфейса", YL, "600 22px/1.25"),
    '</div><div class="step">',
    box(43, 655, 694, 103, "#fdf09f", 20),
    g1icon("bulb", 70, 672, 84, "y"),
    tx(182, 674, 480, 'По умолчанию эталонная пропускная<br>способность — <span style="background:#f9bfd6;'
       'border-radius:12px;padding:2px 12px;font-weight:800">100 Мбит/с</span>', "500 25px/1.35"),
    '</div><div class="step">',
    box(25, 782, 732, 133, CARD, 22, SH),
    g1icon("map", 46, 800, 100, "b"),
    tx(171, 801, 520, "Каждый интерфейс OSPF имеет<br>стоимость, зависящую от пропускной<br>способности.",
       "500 25px/1.28"),
    '</div><div class="step">',
    box(768, 308, 882, 607, CARD, 24, SH),
    box(788, 325, 840, 74, "#d6e8fa", 22),
    g1icon("net", 800, 330, 64, "b"),
    tx(893, 342, 700, "Пример расчета стоимости маршрута", "800 31px/1.2"),
    svg(cloud_icon(1080, 470, .9, "#dcecfb", "#b9d6f3") + cloud_icon(1350, 500, .8, "#dcecfb", "#b9d6f3") + line((925, 491), (925, 575), "#1f1a33", 3) + line((930, 612), (1530, 612), "#f7a9c9", 6) + g1antpuck(900, 600, 175, "p") + g1antpuck(1212, 600, 175, "b") + g1antpuck(1535, 600, 175, "p")),
    pl(832, 421, 186, 70, "Сеть<br>назначения", PK, "700 22px/1.2"),
    pl(1008, 584, 80, 56, "10", "#fff", "700 31px/1", 28, "border:3px solid #6fb8f0"),
    pl(1335, 584, 80, 56, "64", "#fff", "700 31px/1", 28, "border:3px solid #6fb8f0"),
    pl(857, 673, 84, 42, "R1", PK, "800 26px/1", 12),
    pl(1170, 673, 84, 42, "R2", BL, "800 26px/1", 12),
    pl(1493, 673, 84, 42, "R3", PK, "800 26px/1", 12),
    '</div><div class="step">',
    box(790, 738, 838, 155, "#fbe3ee", 22),
    g1icon("calc", 808, 766, 96, "p"),
    tx(928, 762, 680, "<b>Стоимость маршрута</b> = сумма стоимостей интерфейсов", "500 22px/1.3"),
    pl(1027, 801, 416, 72, "10 + 1 + 64 = 75", "#fde97f", "700 46px/1", 18),
    '</div>',
])
