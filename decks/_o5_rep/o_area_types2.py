# -*- coding: utf-8 -*-
"""Типы областей OSPF: продолжение — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 110
K = "#1f1a33"
P = "o_area_types2_"

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


def c(x, y, w, t, f="700 19px/1.2"):
    return tx(x, y, w, t, f, "text-align:center;white-space:nowrap")


def card(x, w, fill, brd, hfill, n, title):
    return (box(x, 165, w, 495, fill, 22, "border:2px solid %s" % brd)
            + box(x + 14, 178, w - 28, 80, hfill, 22)
            + img(P + "i%d.png" % n, "left:%dpx;top:178px;width:80px" % (x + 22))
            + tx(x + 120, 186, w - 130, title, "700 52px/1.1 Oswald", "white-space:nowrap;transform:scaleX(.86);transform-origin:left"))


def row(x, y, w, h, ico, iw, html, ty):
    return (box(x, y, w, h, "rgba(255,255,255,.96)", 18, "border:2px solid #f0edf2")
            + img(P + ico, "left:%dpx;top:%dpx;width:%dpx" % (x + 8, y + (h - 64) // 2, iw))
            + tx(x + 106, ty, w - 112, html, "400 19.5px/1.22", "white-space:nowrap"))


def diag(n, x, left, lx, asbr, ax, r, rx, abx):
    out = [img(P + "d%d.png" % n, "left:%dpx;top:258px" % (x,)),
           c(lx - 70, 326, 140, left, "700 18px/1.25"), c(abx - 60, 406, 120, "ABR-1"), c(rx - 30, 406, 60, r)]
    if asbr:
        out.append(tx(ax, 266, 70, "ASBR", "700 19px/1.2"))
    return "".join(out)


HTML = bg("bg7", W, H) + "".join([
    tx(55, 113, 700, "Totally Stubby • NSSA • Totally NSSA", "800 31px/1.2", "white-space:nowrap"),
    '<div class="step">',
    card(14, 542, "#fff5f9", "#f9cfe0", "#fde0ec", 1, "Totally Stubby"),
    diag(1, 22, "Totally Stubby<br>area<br><span style='font-weight:400'>Area 0.0.0.3</span>", 116, False, 0,
         "R-3", 222, 347),
    c(405, 327, 115, "Area 0<br><span style='font-weight:400'>(Backbone)</span>", "700 19px/1.25"),
    row(32, 448, 508, 102, "ir11.png", 76, "Внутренние маршруты + маршрут по<br>умолчанию. Подробные межобластные"
        "<br>маршруты обычно не передаются.", 463),
    row(32, 562, 508, 78, "ir12.png", 70, "Расширение производителя,<br>не отдельный базовый тип RFC 2328.", 578),
    '</div><div class="step">',
    card(570, 532, "#f2f8fe", "#c8e1f7", "#d9ebfc", 2, "NSSA"),
    diag(2, 578, "NSSA<br>area<br><span style='font-weight:400'>Area 0.0.0.4</span>", 666, True, 770,
         "R-1", 770, 902),
    c(958, 334, 110, "Area 0<br><span style='font-weight:400'>(Backbone)</span>", "700 19px/1.25"),
    row(588, 445, 500, 108, "ir21.png", 68, "Внешние маршруты изнутри области<br>вводятся <b>ASBR</b> через "
        "<b>LSA Type 7</b>.<br><b>ABR</b> может преобразовать их в <b>LSA Type 5</b><br>для остальной сети.", 452),
    row(588, 563, 500, 85, "ir22.png", 68, "Межобластные маршруты могут поступать<br>в NSSA. Маршрут по умолчанию "
        "зависит<br>от настройки.", 568),
    '</div><div class="step">',
    card(1116, 542, "#fffbea", "#f6e6a6", "#fdf2bf", 3, "Totally NSSA"),
    diag(3, 1124, "Totally NSSA<br>area<br><span style='font-weight:400'>Area 0.0.0.5</span>", 1215, True, 1328,
         "R-2", 1328, 1460),
    c(1516, 334, 112, "Area 0<br><span style='font-weight:400'>(Backbone)</span>", "700 19px/1.25"),
    row(1132, 447, 513, 108, "ir31.png", 74, "<span style='font-size:18px'>Ограничивает подробные межобластные<br>маршруты, но разрешает "
        "локальные внешние<br>маршруты через <b>ASBR</b> и <b>LSA Type 7</b>.<br><b>ABR</b> обычно объявляет "
        "маршрут по умолчанию.</span>", 457),
    row(1132, 567, 513, 81, "ir32.png", 74, "Расширение производителя,<br>не отдельный базовый тип RFC 2328.", 585),
    '</div><div class="step">',
    box(14, 672, 1644, 253, "rgba(255,255,255,.9)", 24, "border:2px solid #cfe4f7"),
    img(P + "vl.png", "left:590px;top:672px;width:1062px"),
    tx(48, 684, 560, "ВИРТУАЛЬНЫЙ КАНАЛ", "700 80px/1.1 Oswald", "white-space:nowrap;transform:scaleX(.68);transform-origin:left"),
    tx(50, 787, 540, "Помогает восстановить логическое подключение<br>к Area 0, если обычное соединение невозможно."
       "<br>Это не отдельная область и не замена<br>нормальной магистральной связности.", "400 21px/1.27",
       "white-space:nowrap"),
    pl(890, 678, 332, 56, "Логическая связь ABR—ABR<br>через общую транзитную область", "#fbc6dc", "700 18px/1.2", 18),
    c(625, 780, 120, "Remote area<br><span style='font-weight:400'>Area 0.0.0.2</span>", "700 18px/1.25"),
    c(779, 849, 60, "ABR-2"), c(985, 854, 118, "R-4<br>Transit area<br><span style='font-weight:400'>(не Area 0)"
                                 "</span>", "700 18px/1.15"),
    c(1219, 856, 60, "ABR-1"), c(1448, 859, 40, "R-3"),
    c(1520, 775, 110, "Area 0<br><span style='font-weight:400'>(Backbone)</span>", "700 19px/1.25"),
    '</div>',
])
