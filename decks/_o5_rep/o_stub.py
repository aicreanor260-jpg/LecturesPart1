# -*- coding: utf-8 -*-
"""2. Stub: ABR объявляет 0.0.0.0/0 как LSA-3, LSA-5 не входит, ASBR в Stub не размещают."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

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
            + img(N + "i%d.png" % i, "left:%dpx;top:%dpx" % (ix, 666 if i not in (2, 3) else (662 if i == 2 else 666)))
            + '<div class="st-ch" style="left:%dpx;top:%dpx">%s</div>' % (hx, hy, ht)
            + '<div class="st-ct" style="left:%dpx;top:%dpx">%s</div>' % (tx, ty, tt))


HTML = CSS + bg("bg3", W, H) + "".join([
    '<div class="step">' + img(N + "scene.png", "left:40px;top:25px;width:1705px")
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
