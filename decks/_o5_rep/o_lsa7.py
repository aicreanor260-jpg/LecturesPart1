# -*- coding: utf-8 -*-
"""LSA-7 — NSSA External LSA: ASBR в NSSA создаёт LSA-7, ABR переводит в LSA-5. Схема — SVG, персонажей нет."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_g5kit import T, P, ico, svg, rtr, path, fat, area, cloud_icon, server, laptop, sico

W, H, TOP = 1672, 941, 200
INK = "#1f1a33"


def L(x, y, w, h, s, t, bgc, wt=700, c=INK, ex=""):
    return P(x, y, w, h, s, t, bgc, wt, c, r=18, ex=ex)


def base():
    o = [area(125, 215, 720, 575, "#fde3ee", "#f29cc2"), area(865, 215, 455, 575, "#e3f0fd", "#8fbff0"),
         area(1330, 215, 310, 575, "#fff3c4", "#efcf6a"), cloud_icon(115, 450, 2.2, "#f3eefb", "#c9b8ea")]
    for x in (200, 315, 430):  # ЛВС за ASBR
        o.append(path("M375 520 V570 H%d V610" % x, "#ff5c9e", 4))
    o += [laptop(x, 690, 84, "b") for x in (200, 315, 430)]
    o += [path("M1000 560 L1200 470 M1000 560 L1250 640 M1060 430 L1250 640", "#8fbff0", 4)]
    o += [server(x, y, 60, 104) for x, y in ((1115, 330), (1200, 350), (990, 510), (1110, 545), (1190, 590))]
    o += [path("M1480 520 L1420 640 M1480 520 L1560 610", "#8fbff0", 4), laptop(1420, 720, 84, "b"),
          laptop(1565, 690, 80, "b"), server(1340, 330, 58, 100)]
    o += [rtr(375, 465, 220, "p", "ASBR", 4, 26), rtr(1500, 480, 200, "b")]
    return o


HTML = bg("bg5", W, H) + "".join([
    '<div class="step">' + svg("".join(base()) + fat((180, 465), (258, 465), "#5aaaf2", 30, 18))
    + L(360, 228, 250, 54, 32, "NSSA", "#ffc4d8") + L(1020, 228, 246, 54, 32, "Area 0", "#bcdcfb")
    + L(1365, 232, 240, 50, 25, "другая область", "#ffe58a")
    + L(54, 420, 122, 58, 22, "Внешние<br>сети", "transparent") + '</div>',
    '<div class="step">' + svg(fat((495, 462), (745, 462), "#ff4f96", 42, 30))
    + L(250, 304, 198, 72, 23, "ASBR создаёт<br>LSA-7", "#ffe36e")
    + L(578, 447, 84, 31, 24, "LSA-7", "transparent", c="#fff")
    + L(516, 500, 202, 76, 19.5, "LSA-7<br>распространяется<br>внутри NSSA", "#ffc4d8", 500) + '</div>',
    '<div class="step">' + svg(rtr(850, 465, 210, "b", "ABR", 4, 26) + fat((965, 480), (1225, 480), "#3d8ff0", 46, 32)
                               + path("M1225 480 H1400", "#8fbff0", 10, op=.7))
    + L(712, 268, 248, 100, 21, "ABR переводит<br>подходящие LSA-7<br>в LSA-5", "#bcdcfb", 600)
    + L(1053, 466, 84, 31, 24, "LSA-5", "transparent", c="#fff") + '</div>',
    '<div class="step">' + svg(path("M890 640 V668", "#c99a00", 6, mk="ay"))
    + L(722, 572, 290, 70, 20, "Р-бит и настройки<br>влияют на перевод", "#ffe58a", 600, ex="padding-left:52px")
    + ico("gear", 732, 584, 46, "#ffffff", "#2f7fe0", 2.4)
    + L(796, 680, 290, 84, 21, "Преобразуются<br>не все LSA-7", "#ffe58a", 600, ex="padding-left:56px")
    + ico("pie", 810, 698, 50, "#ffffff", INK, 2.4) + '</div>',
    '<div class="step">' + svg(path("M780 668 H530", "#ff4f96", 6, "14 10", "ap")
                               + '<circle cx="632" cy="664" r="30" fill="#fff" stroke="#e8245e" stroke-width="9"/>'
                               + path("M611 643 L653 685", "#e8245e", 9))
    + L(668, 650, 108, 36, 21, "LSA-5", "#d7eafd", 700, "#2f7fe0")
    + L(516, 708, 258, 62, 16, "LSA-5 не распространяется<br>внутри NSSA", "#ffc4d8", 600) + '</div>',
    '<div class="step">' + ico("globe", 45, 800, 105, "#ff9cc4", INK, 2)
    + '<div class="ab" style="position:absolute;left:165px;top:815px;width:930px;height:80px;background:#fff;border:2px solid #ece6ef;'
      'border-radius:40px"></div>'
    + T(194, 836, 880, 28, "Внешние маршруты входят в OSPF через ASBR", 600, ex="white-space:nowrap") + '</div>',
])
