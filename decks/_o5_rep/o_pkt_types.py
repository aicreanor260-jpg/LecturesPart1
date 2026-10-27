# -*- coding: utf-8 -*-
"""Типы пакетов OSPF — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import FADE
from _o5_g2kit import svg, g2_rtr, g2_doc, g2_db, g2_arrow, g2_win, g2_chk, g2_rays, g2_path

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


FADE2 = ("-webkit-mask:linear-gradient(90deg,transparent,#000 18%,#000 82%,transparent);"
         "mask:linear-gradient(90deg,transparent,#000 18%,#000 82%,transparent)")
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


def _wifi(x, y, col="#ff7fb0"):
    return "".join('<path d="M%.1f %.1f a%d %d 0 0 1 %d 0" fill="none" style="stroke:%s" stroke-width="7" stroke-linecap="round"/>'
                   % (x - r, y, r, r * .8, 2 * r, col) for r in (16, 32, 48))


def _lsa(x, y):
    return ('<rect x="%d" y="%d" width="46" height="56" rx="6" style="fill:#fff;stroke:#e05a97" stroke-width="2.5"/>'
            '<path d="M%d %d l10 -12 8 8 6 -6 10 10z" style="fill:#8cc4f5"/>'
            '<text x="%d" y="%d" text-anchor="middle" font-size="13" font-weight="800" style="fill:#1f1a33">LSA</text>'
            % (x, y, x + 6, y + 30, x + 23, y + 48))


ILL = [
    g2_rtr(110, 545, 120, "p", "R1", ah=55) + g2_rtr(250, 545, 110, "b", "R2", ah=50) + _wifi(182, 505)
    + '<text x="80" y="500" font-size="40" font-weight="900" style="fill:#ff4f9a">!</text>'
      '<text x="282" y="495" font-size="40" font-weight="900" style="fill:#ff4f9a">!</text>',
    g2_db(422, 515, 82, "b", 3) + g2_db(598, 515, 82, "p", 3) + g2_doc(447, 478, 40) + g2_doc(560, 478, 40)
    + g2_arrow(475, 535, 545, 535, "#ff7fb0", 7, 16) + g2_arrow(545, 562, 475, 562, "#3a8ff0", 7, 16)
    + '<path d="M512 470 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z" style="fill:#ffd23a"/>',
    g2_doc(750, 545, 70, "#3a3f55", "#fff", "#8cc4f5") + g2_arrow(800, 545, 860, 545, "#ff4f9a", 8, 18)
    + g2_db(915, 500, 92, "b", 3) + '<text x="935" y="480" font-size="38" font-weight="900" style="fill:#ff4f9a">!</text>',
    '<rect x="1035" y="485" width="210" height="125" rx="10" style="fill:#e9eef6;stroke:#9aa6bd" stroke-width="2.5" transform="rotate(-6 1140 547)"/>'
    + g2_win(1058, 465, 215, 150, "LSU", "p", 0, _lsa(1073, 528) + _lsa(1142, 528) + _lsa(1211, 528))
    + '<path d="M1300 520 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z" style="fill:#ffd23a"/>',
    g2_win(1395, 470, 225, 135, "LSAck", "p", -8, g2_chk(1508, 560, 30, "#2fbf6a"))
    + g2_rays(1380, 545, "#ffd23a", 10, 30, (160, 185, 210)),
]


def card(i, c):
    x, col, fill, n, t, pill, pw, d, dy = c
    return "".join([
        '<div class="step">',
        box(x, 326, 315, 448, fill, 22, "border:2px solid rgba(255,255,255,.9);box-shadow:0 4px 14px rgba(47,143,232,.10)"),
        pl(x + 14, 344, 62, 62, n, col, "700 30px/1 Oswald", 31),
        tx(x + 94, 345, 225, t, OS),
        pl(x + 92, 410, pw, 42, pill, col, "600 32px/1 Oswald", 21),
        svg(ILL[i]),
        tx(x + 24, dy, 290, d, "400 21px/1.27"),
        '</div>'])


FLOW = [("Hello", 92, PK), ("DBD", 342, BL), ("LSR", 578, YL), ("LSU", 828, PK), ("LSAck", 1078, BL)]

HTML = bg("bg5", W, H) + "".join([
    tx(64, 203, 680, "Обнаружение соседей и обмен данными<br>маршрутизации", "600 29px/1.08"),
    img("o_pkt_types_girl2.png", "left:690px;top:196px;width:515px;" + FADE2),
    svg(g2_rtr(1330, 262, 150, "p", ah=60) + g2_rtr(1500, 258, 150, "b", ah=60)),
    "".join(card(i, c) for i, c in enumerate(CARDS)),
    '<div class="step">',
    box(35, 790, 1263, 120, "#fde6f0", 22),
    "".join(pl(x, 818, 172, 64, t, c, "600 34px/1 Oswald", 32) for t, x, c in FLOW),
    "".join(tx(x, 822, 60, "&#10140;", "700 46px/1", "color:#ff4f9a") for x in (280, 513, 757, 1006)),
    svg(g2_rays(70, 850, "#ffd23a", 14, 32, (-160, -195, 160))),
    '</div><div class="step">',
    box(1322, 790, 318, 120, "rgba(255,255,255,.92)", 20, "border:2px dashed #f5a3c4"),
    pl(1337, 812, 52, 52, "!", "#fddc4a", "800 32px/1", 26),
    tx(1408, 801, 230, "<b>LSU</b> может содержать<br>до 11 типов LSA;<br>обычно используются<br>типы 1–5 и 7.",
       "500 17px/1.3"),
    '</div>',
])
