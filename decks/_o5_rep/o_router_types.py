# -*- coding: utf-8 -*-
"""Типы маршрутизаторов OSPF — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 132
K = "#1f1a33"
BL, YL, PK, MN = "#a9d6f8", "#fde26a", "#fdc0da", "#9ee7b8"

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


CARDS = [
    (22, 386, BL, "#ecf6fe", "IR", "Внутренний<br>маршрутизатор", "Internal Router",
     "Все интерфейсы принадлежат<br>одной области. Использует<br>одну LSDB.", 432),
    (420, 402, YL, "#fdf9e9", "BR", "Магистральный<br>маршрутизатор", "Backbone Router",
     "Имеет хотя бы один интерфейс<br>в области 0.0.0.0; не обязательно<br>является ABR.", 432),
    (835, 383, PK, "#fef1f5", "ABR", "Пограничный<br>маршрутизатор области", "Area Border Router",
     "Соединяет одну или несколько<br>областей с областью 0.0.0.0;<br>поддерживает отдельную LSDB<br>"
     "для каждой подключённой области.", 420),
    (1230, 420, MN, "#ecf9f0", "ASBR", "Пограничный маршрутизатор<br>автономной системы",
     "Autonomous System Border Router",
     "Обменивается маршрутной информацией<br>с другими автономными системами или<br>протоколами, "
     "отличными от OSPF; может<br>находиться в любой части домена.", 422),
]


def card(i, c):
    x, w, col, fill, ab, t, en, d, dy = c
    return "".join([
        '<div class="step">',
        box(x, 200, w, 332, fill, 22, "border:2px solid rgba(255,255,255,.95)"),
        pl(x + 14, 208, 100, 100, ab, col, "700 %dpx/1 Oswald" % (46 if len(ab) < 4 else 40), 50),
        tx(x + 132, 218, w - 135, t, "700 20px/1.2", "white-space:nowrap"),
        tx(x + 132, 276, w - 135, en, "400 17px/1.1", "white-space:nowrap"),
        img("o_router_types_r%d.png" % (i + 1), "left:%dpx;top:298px;width:270px" % (x + 70)),
        box(x + 14, 418, w - 28, 104, "rgba(255,255,255,.95)", 16),
        tx(x + 30, dy, w - 40, d, "400 17.5px/1.24", "white-space:nowrap"),
        '</div>'])


def rp(x, y, t, col, w=66):
    return pl(x, y, w, 36, t, col, "600 25px/1 Oswald", 10)


HTML = bg("bg7", W, H) + "".join([
    tx(72, 140, 900, "Четыре роли в маршрутизации между областями", "600 31px/1.2", "white-space:nowrap"),
    box(72, 180, 225, 5, "#ff4f9a", 3),
    img("o_router_types_cat.png", "left:1100px;top:140px;width:565px"),
    "".join(card(i, c) for i, c in enumerate(CARDS)),
    '<div class="step">',
    img("o_router_types_net.png", "left:0;top:540px;width:1665px"),
    rp(113, 727, "IR", "#7cc0f2"), rp(313, 718, "IR", "#7cc0f2"),
    rp(460, 731, "ABR", "#fea1c8", 72), rp(665, 640, "BR", "#fdd84a"), rp(670, 785, "BR", "#fdd84a"),
    rp(895, 734, "ABR", "#fea1c8", 72), rp(1106, 663, "IR", "#7cc0f2"), rp(1082, 782, "IR", "#7cc0f2"),
    rp(1255, 737, "ASBR", "#6fdc9a", 92),
    tx(150, 778, 200, "AREA 0.0.0.1", "700 32px/1 Oswald"),
    tx(636, 813, 200, "AREA 0.0.0.0", "700 30px/1 Oswald"),
    tx(1150, 801, 200, "AREA 0.0.0.5", "700 32px/1 Oswald"),
    pl(1440, 676, 205, 60, "Внешняя сеть /<br>другой протокол", "transparent", "700 19px/1.25", 12),
    '</div><div class="step">',
    box(22, 862, 1628, 60, "#fde9f2", 18, "border:2px solid #f9cfe0"),
    img("o_router_types_bulb.png", "left:36px;top:852px;width:88px"),
    tx(146, 876, 1490, "<b>Роли могут сочетаться:</b> внутренний маршрутизатор области 0 одновременно является BR; "
       "ASBR может быть также IR, BR или ABR.", "400 21.5px/1.2", "white-space:nowrap"),
    '</div>',
])
