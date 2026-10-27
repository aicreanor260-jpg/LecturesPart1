# -*- coding: utf-8 -*-
"""2. Stub: ABR объявляет 0.0.0.0/0 как LSA-3, LSA-5 не входит, ASBR в Stub не размещают."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_g3kit import svg, puck, line, rect, cloud, path, head, ic, ban, cross, rack, laptop, pc, asbr_puck, cloud_icon

WD, H2 = 1774, 887
RED, BL = "#e8245e", "#2f86e6"
CI = [("map", "b"), ("doc", "y"), ("arrow", "b"), ("back", "b"), ("ban", "p"), None]


def scene():
    o = [cloud(330, 455, 640, 300, "p"), cloud_icon(560, 210, 1.1, "#fff", "#e6dff0"), cloud_icon(680, 600, .8, "#fff", "#e6dff0"),
         '<rect x="1035" y="98" width="700" height="534" rx="30" style="fill:rgba(255,243,200,.6)" stroke="#f3d24a" '
         'stroke-width="3" stroke-dasharray="10 8"/>', cloud(1390, 470, 560, 260, "y", False),
         rack(58, 388, 74, 116), rack(112, 440, 74, 116), rack(160, 404, 64, 104),
         path("M540 455 C620 440 660 440 715 445", "#f48fbd", 14), path("M540 455 C620 440 660 440 715 445", "#fde3ee", 6),
         path("M215 520 C300 545 360 540 420 520", "#f48fbd", 10)]
    for d in ["M1460 350 H1520 V310 H1560", "M1520 350 V420 H1600", "M1510 540 H1540 V460", "M1540 540 H1600 V560"]:
        o.append(path(d, BL, 5))
    o += [laptop(1640, 318, 128, "p"), rack(1625, 365, 74, 126), pc(1620, 600, 1.15),
          path("M800 365 V182", RED, 6, "14 10"), head(800, 170, -90, RED, 12),
          path("M840 360 Q850 210 860 190 Q875 140 905 135", RED, 6, "12 10"), cross(895, 215, 22, RED, 8),
          path("M935 185 Q960 225 940 240", RED, 3),
          path("M905 377 H1250", BL, 22), head(1285, 377, 0, BL, 22),
          path("M905 512 H1265", "#ffd23a", 14), head(1295, 512, 0, "#ffd23a", 16),
          path("M1312 545 H975 Q900 545 900 505", BL, 12), head(895, 488, -95, BL, 16),
          path("M1418 382 Q1440 420 1425 455", BL, 6), head(1423, 465, 100, BL, 9), head(1418, 376, -110, BL, 9),
          puck(425, 440, 240, "p", "R0", 34), puck(812, 420, 200, "b", "ABR", 30), puck(1378, 318, 188, "b", "R1", 28),
          puck(1408, 502, 188, "b", "R2", 28), asbr_puck(760, 92, 150), ban(975, 155, 30, RED)]
    return svg("".join(o), WD, H2)


def cico(i, ix):
    if CI[i] is None:
        return svg(asbr_puck(ix + 48, 698, 86), WD, H2)
    return svg(ic(CI[i][0], ix + 46, 712, 88, CI[i][1]), WD, H2)

W, H, TOP = 1774, 887, 0
N = "o_stub_"

CSS = """<style>
.st-p{position:absolute;border-radius:16px;text-align:center;color:#1f1a33;font:600 25px/1.2 Oswald,sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.st-c{position:absolute;top:658px;height:194px;border-radius:16px}
.st-ch{position:absolute;font:600 20px/1.25 Oswald,sans-serif;color:#1f1a33;white-space:nowrap}
.st-ct{position:absolute;font:400 18px/1.28 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
</style>"""


def p(x0, y0, x1, y1, col, html, extra=""):
    return '<div class="st-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        x0, y0, x1 - x0, y1 - y0, col, extra, html)


CARDS = [  # x0, x1, цвет, иконка x, заголовок (x,y), текст (x,y)
    (40, 320, "#e3effb", 46, "LSA-1 и LSA-2 •<br>внутри Stub", 150, 682, "Полная внутренняя<br>топология области<br>(маршрутизаторы и сети)", 70, 765),
    (335, 612, "#fff6d6", 340, "LSA-3 • сети<br>других областей", 442, 682, "Подробные<br>межобластные маршруты,<br>полученные от ABR", 364, 765),
    (628, 905, "#e3effb", 632, "ABR объявляет<br>0.0.0.0/0 как LSA-3", 726, 676, "В Stub анонсируется<br>маршрут по умолчанию<br>для всех неизвестных<br>направлений", 657, 748),
    (920, 1182, "#e3effb", 924, "Неизвестный<br>маршрут → к ABR", 1016, 676, "Пакеты к сетям,<br>которых нет в таблице,<br>отправляются на ABR<br>по маршруту 0.0.0.0/0", 950, 748),
    (1198, 1455, "#fde6ee", 1203, "LSA-5 не входит<br>в Stub", 1300, 682, "Внешние маршруты<br>(LSA-5) в область<br>не распространяются", 1228, 756),
    (1468, 1740, "#eceef3", 1473, "ASBR в Stub<br>не размещают:", 1590, 676, "внешние маршруты<br>не попадут в область<br>обычным способом", 1544, 756),
]


def card(i, c):
    x0, x1, col, ix, ht, hx, hy, tt, tx, ty = c
    return ('<div class="st-c" style="left:%dpx;width:%dpx;background:%s"></div>' % (x0, x1 - x0, col)
            + cico(i, ix)
            + '<div class="st-ch" style="left:%dpx;top:%dpx">%s</div>' % (hx, hy, ht)
            + '<div class="st-ct" style="left:%dpx;top:%dpx">%s</div>' % (tx, ty, tt))


HTML = CSS + bg("bg3", W, H) + "".join([
    '<div class="step">' + scene()
    + p(50, 34, 508, 212, "#fff", "")
    + p(56, 210, 478, 310, "#fff", "Stub получает внутреннюю<br>топологию и подробные<br>межобластные маршруты",
        "font:500 28px/1.17 'Golos Text',sans-serif;align-items:flex-start;text-align:left;padding-left:4px")
    + p(490, 252, 700, 350, "#fbc3d9", "<span style='font-size:44px;font-weight:700;line-height:1.05'>Area 0</span>(магистраль)", "font-size:27px;border-radius:24px")
    + '</div>',
    '<div class="step">'
    + p(1395, 128, 1725, 190, "#d6e8fb", "LSA-1 и LSA-2 • внутри Stub", "font-size:26px")
    + p(1544, 570, 1712, 620, "#ffe14d", "<span style='font-size:40px;font-weight:700'>Stub</span>", "border-radius:12px")
    + '</div>',
    '<div class="step">'
    + p(932, 336, 1226, 406, "#b8dbf8", "0.0.0.0/0 • LSA-3 •<br>маршрут по умолчанию", "line-height:1.15")
    + p(588, 528, 878, 610, "#b8dbf8", "ABR объявляет<br>0.0.0.0/0 как LSA-3", "font-size:30px;line-height:1.15")
    + '</div>',
    '<div class="step">'
    + p(992, 442, 1296, 488, "#fff1b0", "LSA-3 • сети других областей", "font-size:23px")
    + '</div>',
    '<div class="step">'
    + p(936, 564, 1298, 606, "#dcecfb", "Неизвестный маршрут → к ABR", "font-size:25px")
    + '</div>',
    '<div class="step">'
    + p(900, 50, 1234, 120, "#ffd3e2", "<span><b style='font-size:30px'>LSA-5</b> не входит в Stub</span>", "font-size:27px")
    + '</div>',
    '<div class="step">' + "".join(card(i, c) for i, c in enumerate(CARDS)) + '</div>',
])
