# -*- coding: utf-8 -*-
"""Как связаны области OSPF: обычная область -> Area 0 -> Stub, ASBR/ABR, LSA-3/4/5."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import FADE
from _o5_g3kit import svg, puck, rect, path, head, ic, globe, cloud_icon

PK, BL = "#ff4f93", "#2f86e6"


def xc(x, y, r=15):
    k = r * .45
    return ('<circle cx="%d" cy="%d" r="%d" style="fill:#ff3d6e" stroke="#fff" stroke-width="3"/>'
            '<path d="M%.1f %.1f l%.1f %.1f M%.1f %.1f l-%.1f %.1f" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
            % (x, y, r, x - k, y - k, 2 * k, 2 * k, x + k, y - k, 2 * k, 2 * k))


def scene():
    o = [rect(205, 193, 510, 400, "rgba(253,222,235,.85)", None, 24), rect(722, 195, 363, 398, "rgba(220,236,252,.85)", None, 24),
         rect(1092, 195, 420, 398, "rgba(255,243,200,.85)", None, 24), cloud_icon(775, 280, .6), cloud_icon(985, 300, .6),
         '<path d="M45 380 C10 370 15 320 55 318 C55 280 115 270 135 300 C165 285 205 310 195 345 C215 360 205 395 175 395 L60 395 Z" '
         'style="fill:#fff" stroke="#1f1a33" stroke-width="4"/>', globe(110, 318, 28, "#2f7fd8"),
         path("M175 400 C180 430 205 438 228 438", BL, 6), head(240, 438, 0, BL, 9),
         path("M400 440 H612", PK, 5, "14 10"), head(626, 440, 0, PK, 9),
         path("M762 437 H978", BL, 5, "14 10"), head(992, 437, 0, BL, 9),
         path("M762 468 H822 M948 468 H978", BL, 5, "14 10"), head(992, 468, 0, BL, 9),
         path("M1140 437 H1332", BL, 5, "14 10"), head(1346, 437, 0, BL, 9),
         path("M322 356 V384", PK, 3), head(322, 394, 90, PK, 6), path("M697 368 V392", PK, 3), head(697, 402, 90, PK, 6),
         path("M1065 368 V392", BL, 3), head(1065, 402, 90, BL, 6), path("M322 512 V500", PK, 3), head(322, 494, -90, PK, 6),
         path("M1122 468 H1180 M1122 468 V566 H1180 M1122 523 H1300", PK, 3.5, "9 7"),
         xc(1308, 470), xc(1316, 523), xc(1305, 573)]
    o += [puck(322, 418, 150, "b", "R1", 22), puck(697, 420, 128, "b", "R2", 20), puck(1065, 420, 138, "b", "R4", 21),
          puck(1415, 425, 132, "p", "R5", 20)]
    return svg("".join(o), 1536, 1024)


def badge(cx, tone, lab, extra=""):
    bgc = {"p": "#fde0ec", "b": "#dcecfc"}[tone]
    return svg('<circle cx="%d" cy="705" r="72" style="fill:%s"/>' % (cx, bgc) + extra
               + puck(cx, 688, 112, tone, lab, 17), 1536, 1024)

W, H, TOP = 1536, 1024, 180
N = "o_areas_link_"

CSS = """<style>
.al-p{position:absolute;border-radius:12px;text-align:center;color:#1f1a33;font:600 15px/1.2 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.al-p b{font:700 22px/1.1 Oswald,sans-serif}
.al-pk{color:#ff3d8b}.al-bl{color:#1d6fd0}
.al-card{position:absolute;top:612px;height:190px;background:rgba(255,255,255,.95);border:2px solid #e8e4ef;border-radius:16px}
.al-ch{position:absolute;top:632px;font:700 34px/1.1 Oswald,sans-serif;color:#1f1a33}
.al-ct{position:absolute;top:678px;font:400 21px/1.3 "Golos Text",sans-serif;color:#1f1a33}
.al-ban{position:absolute;left:34px;top:815px;width:1475px;height:165px;background:#fbd3e3;border-radius:16px}
.al-bt{position:absolute;left:186px;top:842px;font:700 35px/1.4 Oswald,sans-serif;color:#1f1a33;white-space:nowrap}
.al-note{position:absolute;left:998px;top:828px;width:220px;height:120px;background:#ffe94d;transform:rotate(5deg);border-radius:8px;
 font:500 17px/1.3 "Golos Text",sans-serif;color:#1f1a33;padding:10px 14px}
</style>"""


def p(x0, y0, x1, y1, col, html, extra=""):
    return '<div class="al-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        x0, y0, x1 - x0, y1 - y0, col, extra, html)


def card(x, w, pic, px, pw, title, text):
    return ('<div class="step"><div class="al-card" style="left:%dpx;width:%dpx"></div>' % (x, w)
            + pic
            + '<div class="al-ch" style="left:%dpx">%s</div><div class="al-ct" style="left:%dpx">%s</div></div>'
            % (x + 180, title, x + 180, text))


Y = "#ffe94d"
HTML = CSS + bg("bg7", W, H) + "".join([
    '<div class="step">' + scene()
    + p(306, 199, 600, 258, "#fbc6dc", "<b>Обычная область</b>(не Stub и не NSSA)")
    + p(792, 199, 1080, 250, "#bcdcf8", "<b>Area 0 • магистраль</b>")
    + p(1198, 199, 1442, 258, "#fde88a", "<b>Stub</b>(тупиковая область)")
    + p(52, 356, 186, 386, "#fff", "<b style='font-size:19px'>Внешняя сеть</b>")
    + p(34, 426, 194, 568, "#ececf0", "Например,<br>Интернет или<br>другой протокол<br>(статические,<br>BGP и т.д.)",
        "font:400 17px/1.3 Golos Text;align-items:flex-start;text-align:left;padding-left:16px")
    + '</div>',
    '<div class="step">'
    + p(278, 315, 370, 353, "#ff5c9c", "<b style='color:#fff'>ASBR</b>")
    + p(404, 279, 562, 382, Y, "<span style='font:600 18px/1.25 Oswald'>ASBR вводит<br>в OSPF внешний<br>маршрут как</span>"
        "<b class='al-pk' style='font-size:24px'>LSA-5</b>", "align-items:flex-start;text-align:left;padding-left:8px")
    + p(222, 521, 457, 555, "#ffcfe0", "<span><b class='al-pk' style='font-size:20px'>LSA-5</b> • внешний маршрут</span>")
    + p(226, 557, 460, 580, "#fde4ee", "(например, маршрут в Интернет)", "font-weight:400")
    + p(487, 411, 553, 441, "#fbd3e2", "<b class='al-pk'>LSA-5</b>")
    + '</div>',
    '<div class="step">'
    + p(651, 327, 750, 366, "#ffc4da", "<b>ABR-1</b>")
    + p(1013, 327, 1112, 366, "#b9daf7", "<b>ABR-2</b>")
    + p(789, 373, 961, 421, "#eaf4fd", "<b class='al-bl'>LSA-3</b>сеть другой области", "border:2px solid #7ab5ee")
    + p(826, 455, 944, 507, "#eaf4fd", "<b class='al-bl'>LSA-4</b>путь к ASBR", "border:2px solid #7ab5ee")
    + '</div>',
    '<div class="step">'
    + p(1138, 371, 1354, 420, "#eaf4fd", "<span><b class='al-bl' style='font-size:20px'>LSA-3</b> • маршрут по умолчанию</span>(0.0.0.0/0)",
        "border:2px solid #7ab5ee;font-size:13px")
    + p(1280, 282, 1490, 356, Y, "<span style='font:600 18px/1.3 Oswald'>ABR объявляет<br>маршрут по умолчанию<br>через <b class='al-pk' style='font-size:18px'>LSA-3</b></span>",
        "align-items:flex-start;text-align:left;padding-left:10px")
    + p(1186, 456, 1290, 518, "#ffd6e4", "<b class='al-pk' style='font-size:19px'>LSA-5</b>не проходит<br>в Stub", "font-weight:500")
    + p(1186, 537, 1290, 599, "#ffd6e4", "<b class='al-pk' style='font-size:19px'>LSA-4</b>не проходит<br>в Stub", "font-weight:500")
    + '</div>',
    card(30, 467, badge(112, "p", "ASBR"), 40, 150, "ASBR", "ASBR вводит в OSPF<br>маршруты из внешнего<br>источника или другого<br>протокола."),
    card(512, 461, badge(598, "b", "ABR"), 520, 170, "ABR", "ABR соединяет область<br>с Area 0 и передаёт<br>сведения о маршрутах."),
    card(990, 517, badge(1085, "p", "Area", cloud_icon(1090, 655, .5, "#fff", "#8cc4f5")), 995, 175, "Area 0 — магистраль", "Area 0 — магистраль<br>межобластной<br>маршрутизации."),
    '<div class="step"><div class="al-ban"></div>' + svg(ic("bulb", 105, 885, 104, "y"), 1536, 1024)
    + '<div class="al-bt">В Stub <span class="al-pk">LSA-4 и LSA-5</span> не распространяются;<br>'
      'ABR объявляет маршрут по умолчанию через <span class="al-bl">LSA-3</span>.</div>'
    + img(N + "cat2.png", "left:1235px;top:790px;width:280px;" + FADE)
    + '<div class="al-note">В Stub нет внешних маршрутов и пути к ASBR. Используется default route через LSA-3. <span class="al-pk">♥</span></div></div>',
])
