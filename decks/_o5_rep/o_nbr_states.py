# -*- coding: utf-8 -*-
"""Состояния соседства OSPF — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 296
K = "#1f1a33"
PK, BL, YL = "#ffa9cb", "#5aa9ee", "#fdd84a"

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


CARDS = [  # x0, x1, номер-цвет, фон, имя, текст, y текста
    (17, 222, "#ff7fb0", "#fde9f1", "Down", "Hello ещё<br>не получен", 724),
    (236, 428, BL, "#eaf4fd", "Init", "Hello получен", 724),
    (441, 708, YL, "#fff8dc", "2-Way", "Маршрутизаторы<br>увидели друг друга", 676),
    (722, 940, "#ff7fb0", "#fde9f1", "ExStart", "Согласование<br>обмена", 715),
    (954, 1191, BL, "#eaf4fd", "Exchange", "Обмен описаниями<br>баз данных DBD", 719),
    (1205, 1432, YL, "#fff8dc", "Loading", "Запрос<br>недостающих LSA", 717),
    (1446, 1658, "#ff7fb0", "#fde9f1", "Full", "Базы состояний<br>каналов<br>синхронизированы", 706),
]
ARX = [202, 412, 690, 922, 1172, 1414]


def card(i, c):
    x0, x1, nc, fill, name, t, ty = c
    w = x1 - x0
    out = [
        '<div class="step">',
        box(x0, 437, w, 380, fill, 18, "border:2px solid rgba(255,255,255,.95)"),
        pl(x0 + 14, 455, 54, 54, str(i + 1), nc, "700 30px/1", 27, "color:#fff"),
        tx(x0 + 92, 461, w - 92, name, "600 34px/1 Oswald"),
        img("o_nbr_states_il%d.png" % (i + 1), "left:%dpx;top:518px" % (x0 + 6 if i != 2 else 447)),
        tx(x0, ty, w, t, "400 22px/1.22", "text-align:center"),
    ]
    if i:
        out.append(img("o_nbr_states_ar%d.png" % i, "left:%dpx;top:555px;width:50px" % ARX[i - 1]))
    if i == 2:
        out += [box(447, 748, 256, 64, "#fdec86", 14),
                img("o_nbr_states_bulb.png", "left:452px;top:752px;width:40px"),
                tx(497, 755, 210, "В общей Ethernet-сети<br>выбираются DR и BDR.", "500 19px/1.22 Oswald")]
    out.append('</div>')
    return "".join(out)


HTML = bg("bg2", W, H) + "".join([
    tx(38, 304, 560, "От обнаружения маршрутизатора<br>до синхронизации баз данных", "600 29px/1.2"),
    '<div class="step">',
    img("o_nbr_states_top.png", "left:590px;top:292px;width:1075px"),
    pl(602, 330, 283, 85, "R1 — BDR<br>203.0.113.1/24", "#dcecfb", "600 26px/1.2", 16,
       "border:2px solid #9ccaf3;color:#1d5fa8"),
    pl(1296, 330, 286, 85, "R2 — DR<br>203.0.113.2/24", "#fde3ee", "600 26px/1.2", 16,
       "border:2px solid #f7a8c8;color:#a3134f"),
    '</div>',
    "".join(card(i, c) for i, c in enumerate(CARDS)),
    '<div class="step">',
    box(372, 847, 896, 66, "#eef6fd", 33, "border:2px solid #b8d9f5"),
    img("o_nbr_states_i.png", "left:384px;top:853px;width:62px"),
    tx(497, 867, 760, "На соединении точка-точка выбор DR/BDR обычно не требуется.", "400 22px/1.2"),
    '</div>',
])
