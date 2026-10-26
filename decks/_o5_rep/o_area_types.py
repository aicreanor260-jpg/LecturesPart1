# -*- coding: utf-8 -*-
"""Типы областей OSPF — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

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
            + img(ico, "left:%dpx;top:248px;width:84px" % (x + 18))
            + tx(x + 112, 250, w - 120, t1, "600 42px/1 Oswald", "white-space:nowrap")
            + tx(x + 112, 297, w - 120, t2, "500 25px/1.1", "white-space:nowrap"))


def row(x, y, w, ico, t, s, h=56):
    return (box(x, y, w, h - 4, "rgba(255,255,255,.95)", 16, "border:2px solid #f3eef3")
            + img(ico, "left:%dpx;top:%dpx;width:76px" % (x + 4, y - 2))
            + tx(x + 84, y + 4, w - 90, "<b>%s</b><br>%s" % (t, s), "400 16px/1.28", "white-space:nowrap"))


HTML = bg("bg7", W, H) + "".join([
    tx(113, 137, 900, "Область определяет, какие объявления о маршрутах она принимает", "500 25px/1.2",
       "white-space:nowrap"),
    img("o_area_types_rt.png", "left:975px;top:138px;width:690px"),
    box(45, 175, 840, 42, "rgba(255,255,255,.95)", 21, "border:2px solid #eee6f0"),
    img("o_area_types_book.png", "left:58px;top:178px;width:44px"),
    tx(118, 184, 760, "<b>LSA</b> — объявление о состоянии канала или маршруте &nbsp;·&nbsp; <b>LSDB</b> — база объявлений",
       "400 19px/1.2", "white-space:nowrap"),
    '<div class="step">',
    col(18, 555, "#fff5f9", "#f8d3e2", "#fde1ec", "o_area_types_h1.png", "Магистральная область",
        "Backbone Area • Area 0.0.0.0"),
    tx(43, 342, 520, "Ядро многообластной сети. Связывает другие<br>области через ABR; содержит объявления,<br>"
       "нужные для межобластной маршрутизации.", "400 21.5px/1.27", "white-space:nowrap"),
    img("o_area_types_d1.png", "left:22px;top:440px;width:550px"),
    tx(50, 473, 115, "Обычная<br>область", "700 18px/1.2", "text-align:center"),
    tx(430, 466, 115, "Тупиковая<br>область", "700 18px/1.2", "text-align:center"),
    pl(134, 572, 58, 30, "ABR", "#1f4f86", "700 19px/1", 8, "color:#fff"),
    pl(404, 572, 58, 30, "ABR", "#1f4f86", "700 19px/1", 8, "color:#fff"),
    pl(225, 706, 142, 40, "Area 0.0.0.0", "#fbc4da", "700 21px/1", 14),
    box(38, 790, 522, 66, "#fde3ee", 20),
    img("o_area_types_key.png", "left:38px;top:792px;width:74px"),
    tx(128, 802, 420, "<b>Area 0</b> — логическая магистраль, а не одна<br>физическая сеть.", "400 17.5px/1.3",
       "white-space:nowrap"),
    '</div><div class="step">',
    col(586, 504, "#f2f8fe", "#c8e1f7", "#dbecfc", "o_area_types_h2.png", "Обычная область", "Standard Area"),
    tx(603, 343, 480, "Получает маршруты своей области, маршруты<br>из других областей и внешние маршруты OSPF.",
       "400 20.5px/1.3", "white-space:nowrap"),
    img("o_area_types_d2.png", "left:590px;top:410px;width:498px"),
    pl(612, 434, 110, 56, "Area<br>0.0.0.0", "#fbc4da", "700 20px/1.1", 26),
    tx(990, 425, 80, "Внешние<br>маршруты", "700 14px/1.3"),
    pl(718, 540, 56, 30, "ABR", "#1f4f86", "700 19px/1", 8, "color:#fff"),
    pl(722, 595, 168, 58, "<span><b>Обычная область</b><br><small style='font-weight:400;font-size:13px;white-space:nowrap'>(например, Area 0.0.0.1)"
       "</small></span>", "#cfe6fb", "700 17px/1.25", 28),
    row(603, 682, 472, "o_area_types_r20.png", "Маршруты своей области", "LSA Type 1 и Type 2 (внутри области)"),
    row(603, 742, 472, "o_area_types_r21.png", "Межобластные маршруты", "LSA Type 3 (из других областей через ABR)"),
    row(603, 802, 472, "o_area_types_r22.png", "Внешние маршруты OSPF",
        "LSA Type 5 (от ASBR, обычно из других областей)"),
    '</div><div class="step">',
    col(1102, 553, "#fffbea", "#f6e6a6", "#fdf2bf", "o_area_types_h3.png", "Тупиковая область", "Stub Area"),
    tx(1124, 342, 525, "Не получает обычные внешние объявления LSA Type 5.<br>ABR обычно объявляет маршрут по умолчанию."
       "<br>Получает маршруты из других областей; ASBR для ввода<br>внешних маршрутов здесь не размещают.",
       "400 18.5px/1.2", "white-space:nowrap"),
    img("o_area_types_d3.png", "left:1108px;top:430px;width:544px"),
    pl(1140, 474, 90, 46, "Area<br>0.0.0.0", "#fbc4da", "700 18px/1.1", 20),
    tx(1562, 437, 85, "Внешние<br>маршруты<br>Type 5", "700 13px/1.3"),
    pl(1232, 570, 56, 30, "ABR", "#1f4f86", "700 19px/1", 8, "color:#fff"),
    pl(1385, 513, 176, 58, "<span><b>Тупиковая область</b><br><small style='font-weight:400;font-size:13px;white-space:nowrap'>(например, Area 0.0.0.2)"
       "</small></span>", "#fde58a", "700 16px/1.25", 28),
    row(1120, 700, 520, "o_area_types_r30.png", "Маршрут по умолчанию", "Обычно объявляется ABR (0.0.0.0/0)", 54),
    row(1120, 755, 520, "o_area_types_r31.png", "Межобластные маршруты", "LSA Type 3 (из других областей)", 54),
    row(1120, 810, 520, "o_area_types_r32.png", "Внешние маршруты Type 5", "Не принимаются в тупиковой области", 54),
    '</div><div class="step">',
    box(18, 876, 1637, 52, "rgba(255,255,255,.95)", 26, "border:2px solid #eee6f0"),
    img("o_area_types_f.png", "left:40px;top:878px;width:58px"),
    tx(102, 888, 1540, "<b>Трафик между областями проходит через Area 0 и ABR.</b> Stub ограничивает внешнюю "
       "информацию, но сохраняет межобластные маршруты.", "400 20px/1.2", "white-space:nowrap"),
    '</div>',
])
