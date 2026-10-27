# -*- coding: utf-8 -*-
"""Типы областей OSPF — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_g2kit import svg, g2_rtr, g2_icon_html, g2_path, g2_rays, blob, globe, cloud_icon, laptop, line, cross

W, H, TOP = 1672, 941, 134
K = "#1f1a33"
NAVY = "background:#1f4f86;color:#fff"

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


def col(x, w, fill, brd, hfill, ico, t1, t2):
    return (box(x, 232, w, 636, fill, 22, "border:2px solid %s" % brd)
            + box(x + 10, 242, w - 20, 88, hfill, 20)
            + g2_icon_html(ico[0], x + 22, 252, 76, ico[1])
            + tx(x + 112, 250, w - 120, t1, "600 42px/1 Oswald", "white-space:nowrap")
            + tx(x + 112, 297, w - 120, t2, "500 25px/1.1", "white-space:nowrap"))


def row(x, y, w, ico, t, s, h=56):
    return (box(x, y, w, h - 4, "rgba(255,255,255,.95)", 16, "border:2px solid #f3eef3")
            + g2_icon_html(ico[0], x + 12, y + 2, 44, ico[1])
            + tx(x + 84, y + 4, w - 90, "<b>%s</b><br>%s" % (t, s), "400 16px/1.28", "white-space:nowrap"))


PL = "#f06aa5"
_D1P = [(284, 548), (184, 650), (401, 650)]
D1 = svg(blob(100, 520, 85, 85, "b", seed=1, dash=False) + blob(480, 520, 85, 85, "y", seed=2, dash=False)
         + blob(295, 630, 205, 120, "p", seed=3, dash=False)
         + "".join(line(_D1P[a], _D1P[b], PL, 5) for a, b in [(0, 1), (0, 2), (1, 2)])
         + line((89, 572), (184, 650), PL, 5) + line((89, 572), (284, 548), PL, 4)
         + line((507, 572), (401, 650), PL, 5) + line((507, 572), (284, 548), PL, 4)
         + g2_rtr(89, 560, 92, "b", ah=40) + g2_rtr(507, 560, 92, "y", ah=40)
         + "".join(g2_rtr(x, y, 100, "p", ah=44) for x, y in _D1P))
D2 = svg(blob(667, 505, 72, 92, "p", seed=1, dash=False) + blob(890, 530, 190, 110, "b", seed=4, dash=False)
         + '<rect x="935" y="415" width="140" height="56" rx="28" style="fill:#fff;stroke:#c8dff5" stroke-width="2"/>'
         + globe(966, 443, 20) + g2_path("M948 480 Q930 505 905 515", "#2fae5a", 4, "ag", "7 6")
         + line((647, 552), (830, 552), "#1f2a44", 4) + line((830, 552), (987, 540), "#5aa9ee", 4)
         + line((830, 552), (936, 590), "#5aa9ee", 4) + line((936, 590), (987, 540), "#5aa9ee", 4)
         + g2_rtr(647, 552, 92, "p", ah=40) + g2_rtr(830, 548, 84, "b", ah=38) + g2_rtr(987, 535, 80, "b", ah=36)
         + g2_rtr(936, 586, 76, "b", ah=34) + laptop(975, 652, 58, "b") + laptop(1040, 622, 58, "b"))
D3 = svg(blob(1180, 520, 70, 72, "p", seed=1, dash=False) + blob(1440, 610, 205, 95, "y", seed=6, dash=False)
         + '<rect x="1505" y="425" width="140" height="78" rx="22" style="fill:#e9ecf2;stroke:#c3c9d4" stroke-width="2"/>'
         + globe(1533, 458, 20, "#5b6275") + cross(1596, 515, 13, "#ff2e63", 6)
         + g2_path("M1596 532 V580", "#ff4f9a", 3.5, "ap", "6 5")
         + g2_path("M1238 520 Q1290 525 1325 565", "#3a8ff0", 4, "ab", "8 6")
         + line((1165, 590), (1332, 605), "#1f2a44", 4) + line((1332, 605), (1449, 628), "#3a8ff0", 4, "8 6")
         + line((1449, 628), (1566, 622), "#3a8ff0", 4, "8 6")
         + g2_rtr(1165, 588, 92, "p", ah=40) + g2_rtr(1332, 600, 84, "y", ah=38) + g2_rtr(1449, 624, 78, "y", ah=34)
         + g2_rtr(1566, 618, 78, "y", ah=34) + laptop(1388, 690, 56, "b") + laptop(1522, 690, 56, "b"))

HTML = bg("bg7", W, H) + "".join([
    tx(113, 137, 900, "Область определяет, какие объявления о маршрутах она принимает", "500 25px/1.2",
       "white-space:nowrap"),
    svg(cloud_icon(1180, 200, 1.1) + cloud_icon(1600, 190, .9) + g2_rtr(1400, 190, 90, "p", "OSPF", ah=30, fs=14)),
    box(45, 175, 840, 42, "rgba(255,255,255,.95)", 21, "border:2px solid #eee6f0"),
    g2_icon_html("book", 60, 178, 38, "#ffffff", "#1f1a33", 2.2),
    tx(118, 184, 760, "<b>LSA</b> — объявление о состоянии канала или маршруте &nbsp;·&nbsp; <b>LSDB</b> — база объявлений",
       "400 19px/1.2", "white-space:nowrap"),
    '<div class="step">',
    col(18, 555, "#fff5f9", "#f8d3e2", "#fde1ec", ("tri", "#ff9cc4"), "Магистральная область",
        "Backbone Area • Area 0.0.0.0"),
    tx(43, 342, 520, "Ядро многообластной сети. Связывает другие<br>области через ABR; содержит объявления,<br>"
       "нужные для межобластной маршрутизации.", "400 21.5px/1.27", "white-space:nowrap"),
    D1,
    tx(50, 473, 115, "Обычная<br>область", "700 18px/1.2", "text-align:center"),
    tx(430, 466, 115, "Тупиковая<br>область", "700 18px/1.2", "text-align:center"),
    pl(134, 572, 58, 30, "ABR", "#1f4f86", "700 19px/1", 8, "color:#fff"),
    pl(404, 572, 58, 30, "ABR", "#1f4f86", "700 19px/1", 8, "color:#fff"),
    pl(225, 706, 142, 40, "Area 0.0.0.0", "#fbc4da", "700 21px/1", 14),
    box(38, 790, 522, 66, "#fde3ee", 20),
    g2_icon_html("key", 50, 798, 54, "#ff8fbf"),
    tx(128, 802, 420, "<b>Area 0</b> — логическая магистраль, а не одна<br>физическая сеть.", "400 17.5px/1.3",
       "white-space:nowrap"),
    '</div><div class="step">',
    col(586, 504, "#f2f8fe", "#c8e1f7", "#dbecfc", ("list", "#9fcdf6"), "Обычная область", "Standard Area"),
    tx(603, 343, 480, "Получает маршруты своей области, маршруты<br>из других областей и внешние маршруты OSPF.",
       "400 20.5px/1.3", "white-space:nowrap"),
    D2,
    pl(612, 434, 110, 56, "Area<br>0.0.0.0", "#fbc4da", "700 20px/1.1", 26),
    tx(990, 425, 80, "Внешние<br>маршруты", "700 14px/1.3"),
    pl(718, 540, 56, 30, "ABR", "#1f4f86", "700 19px/1", 8, "color:#fff"),
    pl(722, 595, 168, 58, "<span><b>Обычная область</b><br><small style='font-weight:400;font-size:13px;white-space:nowrap'>(например, Area 0.0.0.1)"
       "</small></span>", "#cfe6fb", "700 17px/1.25", 28),
    row(603, 682, 472, ("monitor", "#bfe0fb"), "Маршруты своей области", "LSA Type 1 и Type 2 (внутри области)"),
    row(603, 742, 472, ("swap", "#ffc6dd"), "Межобластные маршруты", "LSA Type 3 (из других областей через ABR)"),
    row(603, 802, 472, ("globe", "#a8e6bf"), "Внешние маршруты OSPF",
        "LSA Type 5 (от ASBR, обычно из других областей)"),
    '</div><div class="step">',
    col(1102, 553, "#fffbea", "#f6e6a6", "#fdf2bf", ("ban", "#ffd23a"), "Тупиковая область", "Stub Area"),
    tx(1124, 342, 525, "Не получает обычные внешние объявления LSA Type 5.<br>ABR обычно объявляет маршрут по умолчанию."
       "<br>Получает маршруты из других областей; ASBR для ввода<br>внешних маршрутов здесь не размещают.",
       "400 18.5px/1.2", "white-space:nowrap"),
    D3,
    pl(1140, 474, 90, 46, "Area<br>0.0.0.0", "#fbc4da", "700 18px/1.1", 20),
    tx(1562, 437, 85, "Внешние<br>маршруты<br>Type 5", "700 13px/1.3"),
    tx(1250, 478, 130, "Маршрут<br>по умолчанию<br>0.0.0.0/0", "700 14px/1.2", "color:#1d5fa8;text-align:center"),
    pl(1232, 570, 56, 30, "ABR", "#1f4f86", "700 19px/1", 8, "color:#fff"),
    pl(1385, 513, 176, 58, "<span><b>Тупиковая область</b><br><small style='font-weight:400;font-size:13px;white-space:nowrap'>(например, Area 0.0.0.2)"
       "</small></span>", "#fde58a", "700 16px/1.25", 28),
    row(1120, 700, 520, ("down", "#ffe27a"), "Маршрут по умолчанию", "Обычно объявляется ABR (0.0.0.0/0)", 54),
    row(1120, 755, 520, ("swap", "#ffe27a"), "Межобластные маршруты", "LSA Type 3 (из других областей)", 54),
    row(1120, 810, 520, ("ban", "#ffc6dd"), "Внешние маршруты Type 5", "Не принимаются в тупиковой области", 54),
    '</div><div class="step">',
    box(18, 876, 1637, 52, "rgba(255,255,255,.95)", 26, "border:2px solid #eee6f0"),
    g2_icon_html("tri", 52, 880, 44, "#ffd6e6", "#e05a97"),
    tx(102, 888, 1540, "<b>Трафик между областями проходит через Area 0 и ABR.</b> Stub ограничивает внешнюю "
       "информацию, но сохраняет межобластные маршруты.", "400 20px/1.2", "white-space:nowrap"),
    '</div>',
])
