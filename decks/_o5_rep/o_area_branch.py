# -*- coding: utf-8 -*-
"""Как выбрать область для филиала — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 134
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


def head(x, y, a, b, size, col):
    return tx(x, y, 400, '%s <span style="color:#2f8fe8">·</span> <span style="color:%s">%s</span>' % (a, col, b),
              "700 %dpx/1 Oswald" % size, "white-space:nowrap;transform:scaleX(.88);transform-origin:left")


def abr(x, y, w=72, h=30, s=21):
    return pl(x, y, w, h, "ABR", "#fbb3cf", "700 %dpx/1" % s, 10)


HTML = bg("bg7", W, H) + "".join([
    tx(58, 143, 600, "Пример сети предприятия", "700 33px/1.2", "white-space:nowrap"),
    '<div class="step">',
    img("o_area_branch_top.png", "left:8px;top:135px;width:1657px"),
    head(52, 226, "Филиал 1", "Standard Area", 31, "#1f5fae"),
    pl(45, 270, 227, 63, "<span style='text-align:left'>Нужны подробные<br>маршруты</span>", "#c4e6fb",
       "600 19px/1.25", 14),
    '</div><div class="step">',
    abr(550, 386), abr(1035, 386),
    tx(700, 362, 270, "Центр · Area 0 ·<br>магистраль", "700 33px/1.2", "text-align:center;white-space:nowrap"),
    '</div><div class="step">',
    head(1127, 228, "Филиал 2", "Stub Area", 31, K),
    pl(1120, 272, 260, 74, "<span style='text-align:left'>Достаточно внутренних<br>маршрутов и маршрута<br>"
       "по умолчанию</span>", "#fde987", "700 18px/1.2", 12),
    '</div><div class="step">',
    box(18, 600, 1637, 320, "rgba(255,255,255,.75)", 26, "border:2px solid #e8e4ee"),
    box(38, 612, 18, 18, "#ff6fa8", 9),
    tx(70, 613, 400, "ПРИМЕР РАБОТЫ ПРИ ИЗМЕНЕНИЯХ", "500 14px/1.2", "white-space:nowrap"),
    img("o_area_branch_bot.png", "left:20px;top:628px;width:1632px"),
    head(62, 651, "Филиал 1", "Standard Area", 24, "#1f5fae"),
    tx(735, 734, 200, "Центр · Area 0 ·<br>магистраль", "700 26px/1.2", "text-align:center;white-space:nowrap"),
    abr(578, 817, 58, 26, 18), abr(1004, 817, 58, 26, 18),
    pl(665, 825, 315, 76, "Если меняется доступность сети,<br>ABR может объявить изменение<br>другим областям", "#fde0ec",
       "600 16.5px/1.25", 14, "border:2px solid #f7b8d1"),
    head(1120, 646, "Филиал 2", "Stub Area", 24, K),
    pl(1350, 622, 283, 73, "<span style='text-align:left'>Изменения внутренней<br>топологии распространяются<br>"
       "в пределах области</span>", "#c4e3fb", "700 16.5px/1.2", 12),
    '</div>',
])
