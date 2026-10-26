# -*- coding: utf-8 -*-
"""LSA-7 — NSSA External LSA: ASBR в NSSA создаёт LSA-7, ABR переводит в LSA-5."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 200
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def L(x, y, w, h, s, t, bgc, wt=700, c=INK):
    """Плашка с текстом по центру."""
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;border-radius:18px;'
            'display:flex;align-items:center;justify-content:center;text-align:center;white-space:nowrap;'
            'font:%d %spx/1.22 \'Golos Text\',sans-serif;color:%s">%s</div>' % (x, y, w, h, bgc, wt, s, c, t))


HTML = bg("bg5", W, H) + "".join([
    '<div class="step">' + img("o_lsa7_scene.png", "left:22px;top:205px;width:1628px")
    + L(360, 228, 250, 54, 32, "NSSA", "#ffc4d8") + L(1020, 228, 246, 54, 32, "Area 0", "#bcdcfb")
    + L(1365, 232, 240, 50, 25, "другая область", "#ffe58a")
    + L(54, 420, 122, 58, 22, "Внешние<br>сети", "transparent") + '</div>',
    '<div class="step"><div>' + L(250, 304, 198, 72, 23, "ASBR создаёт<br>LSA-7", "#ffe36e")
    + L(578, 447, 84, 31, 24, "LSA-7", "#ff4f96", c="#fff")
    + L(516, 500, 202, 76, 19.5, "LSA-7<br>распространяется<br>внутри NSSA", "#ffc4d8", 500) + '</div></div>',
    '<div class="step"><div>' + L(712, 268, 248, 100, 21, "ABR переводит<br>подходящие LSA-7<br>в LSA-5", "#bcdcfb", 600)
    + L(1053, 466, 84, 31, 24, "LSA-5", "#3d8ff0", c="#fff") + '</div></div>',
    '<div class="step"><div>' + L(792, 580, 206, 54, 20, "Р-бит и настройки<br>влияют на перевод", "#ffe58a", 600)
    + L(886, 698, 160, 58, 21, "Преобразуются<br>не все LSA-7", "#ffe58a", 600) + '</div></div>',
    '<div class="step"><div>' + L(680, 658, 66, 29, 21, "LSA-5", "#d7eafd", 700, "#2f7fe0")
    + L(522, 718, 248, 52, 16, "LSA-5 не распространяется<br>внутри NSSA", "#ffc4d8", 600) + '</div></div>',
    '<div class="step">' + img("o_lsa7_globe.png", "left:45px;top:800px;width:105px")
    + '<div class="ab" style="position:absolute;left:165px;top:815px;width:930px;height:80px;background:#fff;border:2px solid #ece6ef;'
      'border-radius:40px"></div>'
    + T(194, 836, 880, 28, "Внешние маршруты входят в OSPF через ASBR", 600, ex="white-space:nowrap") + '</div>',
])
