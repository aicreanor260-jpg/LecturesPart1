# -*- coding: utf-8 -*-
"""LSA-4 — ASBR Summary LSA: ABR сообщает другим областям, как добраться до ASBR."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 206
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


C = "text-align:center;white-space:nowrap"


def pill(x, y, w, s, t, bgc, c=INK):
    return T(x, y, w, s, t, 700, c=c, ex=C + ";background:%s;border-radius:16px;padding:3px 0" % bgc)


def rot(x, y, t):
    return T(x, y, 180, 19, t, 500, ex="text-align:center;transform:rotate(-9deg)")


S1 = ('<div class="step">' + img("o_lsa4_scene.png", "left:30px;top:208px;width:1622px")
      + pill(345, 272, 216, 32, "Область 1", "#ffb3cd")
      + T(100, 405, 206, 25, "<b style='font-weight:700'>Внешняя сеть</b><br>BGP / IS-IS /<br>статические", 400, lh=1.22, ex="text-align:center")
      + pill(362, 368, 128, 30, "LSA-5", "#ffc4d8")
      + T(530, 540, 180, 28, "<b style='font-weight:700'>ASBR</b><br><span style='font-size:22px;font-weight:400'>Router ID R</span>", 400, lh=1.15, ex="text-align:center")
      + '</div>')
S2 = ('<div class="step"><div>' + T(822, 510, 134, 28, "ABR-1", 700, ex=C)
      + T(845, 226, 178, 25, "ABR создаёт<br><b style='font-weight:700;font-size:29px'>LSA-4</b>", 600, lh=1.15, ex=C)
      + '</div></div>')
S3 = ('<div class="step"><div>' + pill(1050, 281, 106, 27, "LSA-4", "#9fcbf7")
      + rot(1030, 320, "ASBR R доступен<br>через ABR-1")
      + pill(1395, 214, 150, 28, "Область 0", "#bcdcfb", "#1f5fae") + '</div></div>')
S4 = ('<div class="step"><div>' + pill(1110, 457, 106, 27, "LSA-4", "#9fcbf7")
      + rot(1060, 506, "ASBR R доступен<br>через ABR-1")
      + pill(1365, 440, 252, 28, "Другие области", "#ffe36e") + '</div></div>')

CARDS = [("Сообщает,<br>как добраться<br>до ASBR", "#ffe8ef", 600, 23),
         ("ASBR вводит<br>в OSPF внешние<br>маршруты: BGP,<br>IS-IS или статические", "#e3f0fe", 500, 21),
         ("LSA-5 объявляет<br>внешнюю сеть;<br>LSA-4 помогает<br>найти ASBR", "#fff5cc", 500, 22),
         ("LSA-4 создаёт<br>ABR для других<br>областей", "#ffe8ef", 500, 23),
         ("Link State ID —<br>Router ID ASBR", "#e3f0fe", 400, 23),
         ("Advertising Router —<br>Router ID ABR", "#fff5cc", 400, 21),
         ("Флаг Е в LSA-1<br>отмечает<br>маршрутизатор-ASBR", "#ffe8ef", 500, 21)]
XS = [(36, 210), (258, 234), (500, 238), (744, 214), (968, 196), (1176, 208), (1394, 248)]


def cards():
    out = []
    for i, ((t, c, wt, s), (x, w)) in enumerate(zip(CARDS, XS)):
        out.append('<div class="step">' + B(x, 652, w, 254, c, 20)
                   + img("o_lsa4_c%d.png" % (i + 1), "left:%dpx;top:662px" % [40, 262, 505, 750, 972, 1180, 1398][i])
                   + T(x + 16, 772, w - 20, s - 1.5, t, wt, lh=1.3, ex="white-space:nowrap;letter-spacing:-.01em") + '</div>')
    return '<div class="step">' + "".join(out).replace('<div class="step">', "<div>") + "</div>"


HTML = bg("bg4", W, H) + S1 + S2 + S3 + S4 + cards()
