# -*- coding: utf-8 -*-
"""Как связаны области OSPF: обычная область -> Area 0 -> Stub, ASBR/ABR, LSA-3/4/5."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

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
            + img(N + pic, "left:%dpx;top:625px;width:%dpx" % (px, pw))
            + '<div class="al-ch" style="left:%dpx">%s</div><div class="al-ct" style="left:%dpx">%s</div></div>'
            % (x + 180, title, x + 180, text))


Y = "#ffe94d"
HTML = CSS + bg("bg7", W, H) + "".join([
    '<div class="step">' + img(N + "scene.png", "left:22px;top:188px;width:1493px")
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
    card(30, 467, "asbr.png", 40, 150, "ASBR", "ASBR вводит в OSPF<br>маршруты из внешнего<br>источника или другого<br>протокола."),
    card(512, 461, "abr.png", 520, 170, "ABR", "ABR соединяет область<br>с Area 0 и передаёт<br>сведения о маршрутах."),
    card(990, 517, "area.png", 995, 175, "Area 0 — магистраль", "Area 0 — магистраль<br>межобластной<br>маршрутизации."),
    '<div class="step"><div class="al-ban"></div>' + img(N + "bulb.png", "left:50px;top:830px;width:110px")
    + '<div class="al-bt">В Stub <span class="al-pk">LSA-4 и LSA-5</span> не распространяются;<br>'
      'ABR объявляет маршрут по умолчанию через <span class="al-bl">LSA-3</span>.</div>'
    + img(N + "cat.png", "left:1225px;top:785px;width:290px")
    + '<div class="al-note">В Stub нет внешних маршрутов и пути к ASBR. Используется default route через LSA-3. <span class="al-pk">♥</span></div></div>',
])
