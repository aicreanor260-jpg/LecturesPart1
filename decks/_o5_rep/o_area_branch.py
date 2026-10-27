# -*- coding: utf-8 -*-
"""Как выбрать область для филиала — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_g3kit import svg, puck, line, cloud, path, cross, rack, laptop, globe, T
from _o5_g3kit import head as ahead

BL, PK, YL, GR = "#4a9be8", "#ee5f9c", "#f2b600", "#2fae5a"


def links(pairs, col, w=6):
    return "".join(line(a, b, col, w) for a, b in pairs)


def top():
    o = [cloud(285, 420, 560, 300, "b"), cloud(1395, 445, 560, 290, "y"), cloud(840, 385, 640, 400, "p"),
         rack(630, 300, 62, 70), rack(706, 258, 82, 106), rack(796, 250, 88, 114), rack(892, 276, 78, 88), rack(978, 306, 60, 62),
         rack(96, 352, 70, 84), rack(70, 458, 58, 80), rack(132, 458, 58, 80), laptop(205, 470, 64, "p"), laptop(230, 548, 80, "p"),
         rack(1560, 462, 64, 84), rack(1488, 520, 52, 46)]
    o.append(links([((275, 425), (400, 520)), ((330, 420), (535, 465)), ((440, 520), (535, 470)), ((200, 425), (120, 445)),
                    ((215, 435), (165, 470)), ((340, 520), (250, 520))], BL))
    o.append(links([((630, 470), (760, 520)), ((1025, 470), (910, 520))], PK, 7))
    o.append(links([((1120, 465), (1310, 430)), ((1120, 470), (1200, 515)), ((1365, 430), (1270, 515)), ((1410, 430), (1450, 520)),
                    ((1300, 515), (1400, 520)), ((1490, 520), (1540, 505))], YL))
    o += [puck(275, 400, 150, "b", "R1"), puck(400, 497, 130, "b", "R2"), puck(585, 442, 124, "p"), puck(1070, 442, 124, "p"),
          puck(835, 495, 172, "p"), puck(1365, 405, 118, "y", "R2"), puck(1255, 490, 128, "y", "R1"), puck(1440, 495, 118, "y", "R2")]
    # опционально: NSSA
    o += ['<rect x="1400" y="142" width="258" height="196" rx="18" style="fill:rgba(255,255,255,.93)" stroke="%s" '
          'stroke-width="3" stroke-dasharray="6 6"/>' % GR,
          '<rect x="1412" y="152" width="234" height="34" rx="12" style="fill:#d9f3e3"/>',
          T(1529, 176, "Опционально: NSSA", 20, "#1f1a33", "middle", 800),
          T(1414, 208, "Если филиал вводит|собственные внешние|маршруты — рассмотреть|NSSA с локальным ASBR.", 15.5, "#1f1a33", "start", 500),
          puck(1500, 290, 70, "g", "R3"), globe(1620, 286, 18, "#2f7fd8"), path("M1545 300 Q1590 300 1605 302", GR, 3),
          '<rect x="1556" y="314" width="62" height="20" rx="10" style="fill:#fff" stroke="%s" stroke-width="2"/>' % GR,
          T(1587, 329, "ASBR", 13, "#1f1a33", "middle", 800),
          path("M1462 318 C1455 335 1458 342 1462 345", GR, 4, "6 7"), path("M1460 355 V318", GR, 4, "6 7"),
          '<circle cx="1460" cy="360" r="7" style="fill:%s"/>' % GR]
    return svg("".join(o))


def bot():
    o = [cloud(260, 780, 480, 220, "b"), cloud(1380, 790, 560, 220, "y"), cloud(830, 760, 560, 230, "p"),
         rack(752, 668, 52, 56), rack(812, 660, 60, 66), rack(880, 670, 50, 54), rack(94, 718, 60, 70), rack(96, 795, 52, 68),
         rack(152, 795, 52, 68), laptop(190, 790, 54, "p"), laptop(240, 845, 66, "p"), rack(1520, 700, 58, 80), rack(1468, 830, 44, 50)]
    o.append(links([((265, 760), (395, 820)), ((310, 760), (560, 795)), ((440, 820), (560, 798)), ((200, 760), (150, 780))], BL))
    o.append(line((655, 795), (985, 795), PK, 6))
    o.append(links([((1080, 790), (1240, 742)), ((1080, 795), (1240, 835))], YL))
    o += [cross(1163, 788, 14), puck(265, 738, 118, "b", "R2"), puck(395, 800, 118, "b", "R3"), puck(605, 775, 106, "p"),
          puck(1030, 775, 106, "p"), puck(1285, 718, 100, "y", "R1"), puck(1290, 815, 100, "y", "R2"), puck(1470, 790, 108, "y", "R2"),
          path("M1350 725 Q1420 725 1450 765", "#2f86e6", 4), ahead(1455, 775, 60, "#2f86e6", 8),
          path("M1455 840 Q1420 860 1360 850", "#2f86e6", 4), ahead(1352, 848, 175, "#2f86e6", 8),
          path("M520 858 H650", PK, 4), ahead(512, 858, 180, PK, 8), ahead(658, 858, 0, PK, 8),
          path("M995 858 H1080", PK, 4), ahead(987, 858, 180, PK, 8), path("M1090 858 H1120", PK, 4, "8 7"),
          ahead(1130, 858, 0, PK, 8)]
    return svg("".join(o))

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
    top(),
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
    bot(),
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
