# -*- coding: utf-8 -*-
"""Типы областей OSPF: таблица — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 188
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


ROWS = [  # высота, фон ячейки 1, название, что получает, внешние
    (74, "#fdeaf2", "Backbone ·<br>Area 0", "Маршруты для<br>связи областей",
     "Магистральная область;<br>межобластной обмен через ABR"),
    (75, "#e8f3fd", "Standard ·<br>обычная", "Внутренние, межобластные<br>и внешние маршруты",
     "Внешние маршруты Type 5;<br>ASBR разрешён"),
    (83, "#fef8e2", "Stub ·<br>тупиковая", "Внутренние и межобластные;<br>обычно default route",
     "Type 5 не принимает;<br>ASBR для внешних маршрутов<br>не размещают"),
    (76, "#f2ecfc", "Totally Stubby", "Внутренние маршруты<br>и default route",
     "Подробные межобластные<br>и внешние маршруты ограничены"),
    (88, "#e9f8ee", "NSSA", "Внутренние и межобластные<br>маршруты",
     "Локальный ASBR вводит внешние<br>через Type 7; ABR может<br>перевести Type 7 в Type 5"),
    (88, "#fdeaf2", "Totally NSSA", "Внутренние маршруты;<br>обычно default route",
     "Локальный ASBR вводит внешние<br>через Type 7; подробные<br>межобластные маршруты ограничены"),
]


def table():
    out, y = [], 316
    for i, (h, f, a, b, c) in enumerate(ROWS):
        out += ['<div class="step">',
                box(37, y, 228, h, f, 14, "border:2px solid #fff"),
                img("o_area_table_i%d.png" % (i + 1), "left:44px;top:%dpx;width:72px" % (y + 4)),
                tx(128, y, 140, a, "700 19.5px/1.2", "height:%dpx;display:flex;align-items:center;white-space:nowrap" % h),
                box(272, y, 283, h, "rgba(255,255,255,.95)", 14, "border:2px solid #efeef3"),
                tx(290, y, 265, b, "400 18px/1.25", "height:%dpx;display:flex;align-items:center;white-space:nowrap" % h),
                box(562, y, 340, h, "rgba(255,255,255,.95)", 14, "border:2px solid #efeef3"),
                tx(580, y, 322, c, "400 17px/1.25", "height:%dpx;display:flex;align-items:center;white-space:nowrap" % h),
                '</div>']
        y += h + 7
    return "".join(out)


def lb(x, y, w, t, f="700 21px/1.2"):
    return tx(x, y, w, t, f, "text-align:center;white-space:nowrap")


def abr(x, y, t):
    return pl(x, y, 92, 32, t, "linear-gradient(#56a7ef,#2f7fd8)", "700 20px/1", 16, "color:#fff")


HTML = bg("bg4", W, H) + "".join([
    tx(58, 193, 840, "Какие маршруты получает каждая область", "600 37px/1.2", "white-space:nowrap"),
    box(37, 255, 225, 54, "#fbd3e3", 14), tx(62, 270, 200, "Тип области", "700 21px/1.2"),
    box(268, 255, 285, 54, "#d5e8fb", 14), tx(291, 270, 260, "Что получает", "700 21px/1.2"),
    box(560, 255, 338, 54, "#fdeea8", 14), tx(580, 270, 320, "Внешние маршруты / ASBR", "700 21px/1.2"),
    table(),
    '<div class="step">',
    box(37, 847, 868, 66, "rgba(255,255,255,.95)", 16, "border:2px solid #e6eef6"),
    img("o_area_table_inf.png", "left:40px;top:852px;width:50px"),
    tx(108, 856, 790, "<ul style='margin:0;padding-left:20px'><li>Totally Stubby и Totally NSSA — расширения "
       "производителя, не отдельные базовые типы RFC 2328.</li><li>Маршрут по умолчанию зависит от конфигурации "
       "области.</li></ul>", "400 14.5px/1.5", "white-space:nowrap"),
    '</div><div class="step">',
    img("o_area_table_net.png", "left:905px;top:190px;width:747px"),
    pl(1110, 210, 155, 52, "<span>ASBR<br><small style='font-weight:500;font-size:15px'>(в области NSSA)</small></span>",
       "#fff", "700 19px/1.1", 18, "border:2px solid #9ad6b4"),
    lb(985, 341, 118, "NSSA<br>Area 0.0.0.4"),
    pl(1173, 318, 197, 62, "Type 7 → Type 5<br>(на ABR)", "#fbb9d4", "600 20px/1.2", 22),
    lb(1452, 313, 136, "Totally NSSA<br>Area 0.0.0.5", "700 20px/1.2"),
    abr(1078, 428, "ABR-1"), abr(1330, 428, "ABR-2"), abr(1062, 643, "ABR-3"), abr(1370, 646, "ABR-4"),
    lb(1472, 565, 126, "Standard<br>Area 0.0.0.1", "700 20px/1.2"),
    lb(1180, 603, 146, "<b>Area 0.0.0.0</b><br><span style='font-weight:500'>магистраль</span>", "700 21px/1.15"),
    lb(1008, 825, 150, "Totally Stubby<br>Area 0.0.0.3", "700 21px/1.2"),
    lb(1447, 825, 120, "Stub<br>Area 0.0.0.2", "700 21px/1.2"),
    '</div>',
])
