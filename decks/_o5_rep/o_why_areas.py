# -*- coding: utf-8 -*-
"""Зачем OSPF делят на области — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

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
            + img(ico, "left:%dpx;top:%dpx;width:88px" % (x + 17, y))
            + tx(x + 130, y + 9, 620, html, "400 24px/1.25"))


def lab(x, y, w, t, f="700 26px/1"):
    return tx(x, y, w, t, f, "text-align:center")


HTML = bg("bg5", W, H) + "".join([
    tx(55, 134, 860, "Масштабирование и локализация расчётов", "600 35px/1.2", "white-space:nowrap"),
    box(52, 180, 180, 5, "#fdd83a", 3), box(745, 176, 180, 5, "#fdd83a", 3),
    img("o_why_areas_girl.png", "left:940px;top:128px;width:725px"),
    '<div class="step">',
    box(20, 210, 810, 620, CARD, 26, BRD),
    pl(45, 222, 553, 68, "Одна большая область", "#fde0ec", "900 42px/1", 20),
    img("o_why_areas_net1.png", "left:28px;top:292px;width:794px"),
    '</div><div class="step">',
    row(45, 655, "o_why_areas_i1.png", "Все маршрутизаторы хранят<br>топологию области в LSDB."),
    row(45, 740, "o_why_areas_i2.png", "С ростом сети увеличиваются<br>объём базы и затраты на её обработку."),
    '</div><div class="step">',
    box(842, 210, 810, 620, CARD, 26, BRD),
    pl(868, 222, 462, 68, "Иерархия областей", "#d6e9fb", "900 42px/1", 20),
    img("o_why_areas_net2.png", "left:846px;top:292px;width:804px"),
    lab(1200, 314, 110, "Area 0"), lab(1070, 443, 70, "ABR", "700 24px/1"), lab(1347, 443, 70, "ABR", "700 24px/1"),
    lab(925, 599, 110, "Area 1"), lab(1442, 599, 110, "Area 2"),
    '</div><div class="step">',
    row(867, 655, "o_why_areas_i3.png", "Часть обновлений распространяется<br>в пределах области."),
    row(867, 740, "o_why_areas_i4.png", "<b>SPF</b> (алгоритм Дейкстры) рассчитывает<br>пути по топологии своей области."),
    '</div><div class="step">',
    box(20, 842, 1632, 86, "#fdf3c4", 24),
    img("o_why_areas_warn.png", "left:66px;top:848px;width:100px"),
    box(222, 860, 2, 50, "#e8d68a", 1),
    tx(290, 853, 1200, "Изменения могут влиять на маршруты других областей через объявления ABR —<br>"
       "межобластные последствия возможны.", "700 25px/1.25"),
    '</div>',
])
