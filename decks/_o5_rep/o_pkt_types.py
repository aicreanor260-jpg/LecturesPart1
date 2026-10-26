# -*- coding: utf-8 -*-
"""Типы пакетов OSPF — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 196
K = "#1f1a33"
PK, BL, YL = "#ffa9cb", "#a9d3f7", "#fddc4a"


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


OS = "600 26px/1.1 Oswald"
CARDS = [
    (28, PK, "#fff3f8", "01", "Пакет<br>приветствия —", "Hello", 152,
     "Устанавливает<br>и поддерживает<br>смежность между<br>маршрутизаторами OSPF.", 655),
    (355, BL, "#f2f8fe", "02", "Описание<br>базы данных —", "DBD", 102,
     "Сокращённый список<br>LSDB для сверки баз<br>данных маршрутизаторов<br>области.", 655),
    (680, YL, "#fffbea", "03", "Запрос состояния<br>канала —", "LSR", 92,
     "Запрашивает подробные<br>данные о записи,<br>указанной в DBD.", 655),
    (1005, PK, "#fff3f8", "04", "Обновление<br>состояния канала —", "LSU", 96,
     "Передаёт ответ на LSR<br>и объявляет новые данные;<br>содержит записи LSA.", 655),
    (1330, BL, "#f2f8fe", "05", "Подтверждение<br>состояния канала —", "LSAck", 120,
     "Подтверждает получение<br>пакета LSU.", 672),
]


def card(i, c):
    x, col, fill, n, t, pill, pw, d, dy = c
    return "".join([
        '<div class="step">',
        box(x, 326, 315, 448, fill, 22, "border:2px solid rgba(255,255,255,.9);box-shadow:0 4px 14px rgba(47,143,232,.10)"),
        pl(x + 14, 344, 62, 62, n, col, "700 30px/1 Oswald", 31),
        tx(x + 94, 345, 225, t, OS),
        pl(x + 92, 410, pw, 42, pill, col, "600 32px/1 Oswald", 21),
        img("o_pkt_types_il%d.png" % (i + 1), "left:%dpx;top:445px;width:300px" % (x + 8)),
        tx(x + 24, dy, 290, d, "400 21px/1.27"),
        '</div>'])


FLOW = [("Hello", 92, PK), ("DBD", 342, BL), ("LSR", 578, YL), ("LSU", 828, PK), ("LSAck", 1078, BL)]

HTML = bg("bg5", W, H) + "".join([
    tx(64, 203, 680, "Обнаружение соседей и обмен данными<br>маршрутизации", "600 29px/1.08"),
    img("o_pkt_types_girl.png", "left:640px;top:196px;width:1020px"),
    "".join(card(i, c) for i, c in enumerate(CARDS)),
    '<div class="step">',
    box(35, 790, 1263, 120, "#fde6f0", 22),
    "".join(pl(x, 818, 172, 64, t, c, "600 34px/1 Oswald", 32) for t, x, c in FLOW),
    "".join(tx(x, 822, 60, "&#10140;", "700 46px/1", "color:#ff4f9a") for x in (280, 513, 757, 1006)),
    img("o_pkt_types_d1.png", "left:30px;top:800px;width:50px"),
    '</div><div class="step">',
    box(1322, 790, 318, 120, "rgba(255,255,255,.92)", 20, "border:2px dashed #f5a3c4"),
    pl(1337, 812, 52, 52, "!", "#fddc4a", "800 32px/1", 26),
    tx(1408, 801, 230, "<b>LSU</b> может содержать<br>до 11 типов LSA;<br>обычно используются<br>типы 1–5 и 7.",
       "500 17px/1.3"),
    '</div>',
])
