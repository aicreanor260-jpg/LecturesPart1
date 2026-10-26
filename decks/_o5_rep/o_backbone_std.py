# -*- coding: utf-8 -*-
"""Разберём каждую область — Backbone и Standard: Area 1 / Area 0 / Area 2 и типы LSA."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1774, 887, 95
N = "o_backbone_std_"

CSS = """<style>
.bs-p{position:absolute;border-radius:14px;text-align:center;color:#1f1a33;font:500 17px/1.2 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.bs-p b{font:700 26px/1.1 Oswald,sans-serif}
.bs-big{font:700 40px/1 Oswald,sans-serif!important}
.bs-sec{position:absolute;left:12px;top:615px;width:1290px;height:262px;background:rgba(255,255,255,.93);border:2px solid #ece7f2;border-radius:18px}
.bs-c{position:absolute;top:655px;height:212px;background:#fff;border:2px solid #efeaf4;border-radius:14px;overflow:hidden}
.bs-ch{position:absolute;left:0;top:0;right:0;height:90px}
.bs-ct{position:absolute;font:700 25px/1 Oswald,sans-serif}
.bs-cs{position:absolute;font:600 14px/1.25 "Golos Text",sans-serif;color:#1f1a33}
.bs-ul{position:absolute;font:400 12.3px/1.25 "Golos Text",sans-serif;color:#1f1a33;margin:0;padding-left:16px}
.bs-ul li{margin-bottom:8px}
.bs-imp{position:absolute;left:1310px;top:612px;width:454px;height:265px;background:#fde2ec;border-radius:20px}
</style>"""


def p(x0, y0, x1, y1, col, html, extra=""):
    return '<div class="bs-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        x0, y0, x1 - x0, y1 - y0, col, extra, html)


CARDS = [  # x, w, шапка, цвет заголовка, заголовок, подпись, иконка(x,y,w), док(x,y), пункты
    (22, 244, "#fde0ea", "#ff3d8b", "LSA-1", "Соединения<br>маршрутизатора", ("h1", 188, 666, 72), ("d1", 28, 760),
     ["Список интерфейсов и соседей маршрутизатора.", "Распространяется только в пределах своей области."]),
    (275, 242, "#dcecfb", "#1f1a33", "LSA-2", "Общая сеть<br>и выбранный DR", ("h2", 395, 706, 107), ("d2", 280, 760),
     ["Информация об общей Ethernet-сети и о выбранном DR (Designated Router).", "Распространяется только в пределах своей области."]),
    (525, 244, "#dcecfb", "#1f1a33", "LSA-3", "Доступная сеть<br>в другой области", ("h3", 676, 676, 64), ("d3", 530, 760),
     ["ABR объявляет сети из своей области в другие области.", "Используется для достижения сетей в других областях."]),
    (778, 256, "#ece0fc", "#8a3fe0", "LSA-4", "Путь к ASBR", ("h4", 918, 664, 92), ("d4", 784, 748),
     ["ABR объявляет путь к ASBR, если ASBR находится в другой области.", "Помогает найти ASBR для получения внешних маршрутов (LSA-5)."]),
    (1042, 250, "#dff3e3", "#1f1a33", "LSA-5", "Внешний маршрут", ("h5", 1206, 684, 66), ("d5", 1048, 746),
     ["Создаётся ASBR для внешних маршрутов (например, из Интернета).", "Распространяется через все стандартные области (OSPF), ABR не создаёт его заново."]),
]


def card(c):
    x, w, hc, tc, t, s, ico, doc, items = c
    two = "<br>" in s
    return ('<div class="bs-c" style="left:%dpx;width:%dpx"><div class="bs-ch" style="background:%s"></div></div>' % (x, w, hc)
            + '<div class="bs-ct" style="left:%dpx;top:668px;color:%s">%s</div>' % (x + 32, tc, t)
            + img(N + ico[0] + ".png", "left:%dpx;top:%dpx;width:%dpx" % ico[1:])
            + '<div class="bs-cs" style="left:%dpx;top:%dpx">%s</div>' % (x + 32, 698 if two else 700, s)
            + img(N + doc[0] + ".png", "left:%dpx;top:%dpx;width:36px" % doc[1:])
            + '<ul class="bs-ul" style="left:%dpx;top:%dpx;width:%dpx">%s</ul>' % (
                x + 52, doc[2] + 2, w - 58, "".join("<li>%s</li>" % i for i in items)))


HTML = CSS + bg("bg2", W, H) + "".join([
    p(455, 100, 1285, 141, "#fbd0e0", "Как работают области OSPF и какие LSA в них распространяются", "font:600 24px/1 'Golos Text',sans-serif;border-radius:20px"),
    '<div class="step">' + img(N + "scene.png", "left:10px;top:140px;width:1756px")
    + p(148, 148, 312, 206, "#ffc2d8", "<b class='bs-big'>Area 1</b>", "border-radius:22px")
    + p(314, 150, 506, 204, "#fde3ee", "Обычная область<br>(standard area)", "align-items:flex-start;text-align:left;padding-left:18px")
    + p(738, 154, 896, 208, "#ffe066", "<b class='bs-big'>Area 0</b>", "border-radius:22px")
    + p(898, 154, 1116, 206, "#fff1b0", "Магистральная область<br>(backbone)", "align-items:flex-start;text-align:left;padding-left:8px")
    + p(1298, 150, 1458, 206, "#b9dbf8", "<b class='bs-big'>Area 2</b>", "border-radius:22px")
    + p(1460, 150, 1640, 206, "#dcecfb", "Обычная область<br>(standard area)", "align-items:flex-start;text-align:left;padding-left:8px")
    + p(14, 296, 130, 380, "#fff", "<span style='font-weight:700'>Внешняя<br>сеть</span>(например,<br>Интернет)",
        "align-items:flex-start;text-align:left;padding-left:22px;font-size:15px")
    + p(386, 414, 494, 456, "#fbe6ef", "<span style='font-weight:600'>Ethernet-сеть</span>(общая сеть)", "font-size:15px")
    + p(1418, 399, 1530, 441, "#e8f1fb", "<span style='font-weight:600'>Ethernet-сеть</span>(общая сеть)", "font-size:15px")
    + '</div>',
    '<div class="step">'
    + p(153, 218, 362, 294, "#ffe94d", "<span style='font-weight:600;font-size:17px'>ASBR вводит внешний<br>маршрут и создаёт</span><b>LSA-5</b>",
        "align-items:flex-start;text-align:left;padding-left:14px")
    + p(104, 475, 222, 533, "#ffcfe0", "<b>LSA-1</b>(только в Area 1)", "font-size:12px")
    + p(382, 485, 500, 541, "#d3e7fb", "<b>LSA-2</b>(только в Area 1)", "font-size:12px")
    + p(1320, 480, 1440, 536, "#ffcfe0", "<b>LSA-1</b>(только в Area 2)", "font-size:12px")
    + p(1528, 478, 1646, 536, "#d3e7fb", "<b>LSA-2</b>(только в Area 2)", "font-size:12px")
    + '</div>',
    '<div class="step">'
    + p(598, 250, 712, 302, "#fff", "<b>ABR-1</b>(Area 1 ↔ 0)")
    + p(1122, 250, 1246, 302, "#fff", "<b>ABR-2</b>(Area 0 ↔ 2)")
    + p(860, 224, 966, 262, "#7cc0f5", "<b style='color:#1f1a33'>LSA-3</b>", "border-radius:10px")
    + p(788, 262, 1040, 306, "#d8eafb", "ABR объявляет доступную<br>сеть из другой области")
    + p(860, 432, 968, 470, "#c99cf5", "<b>LSA-4</b>", "border-radius:10px")
    + p(838, 470, 996, 520, "#ead9fc", "ABR объявляет<br>путь к ASBR")
    + '</div>',
    '<div class="step">'
    + p(700, 537, 1062, 566, "#fdf7e2", "<b style='color:#1f9a3a;font-size:22px'>LSA-5 — внешний маршрут от ASBR</b>")
    + p(675, 570, 1112, 603, "#22b04a", "<span style='color:#fff'>ABR распространяет LSA-5, не создавая заново</span>", "border-radius:17px")
    + '</div>',
    '<div class="step"><div class="bs-sec"></div>'
    + '<div class="bs-p" style="left:22px;top:620px;height:34px;font:700 28px/1 Oswald,sans-serif;justify-content:flex-start;flex-direction:row">'
      '<span style="color:#ff5c9c;font-size:22px;margin-right:8px">●</span>Типы LSA в OSPF</div>'
    + "".join(card(c) for c in CARDS) + '</div>',
    '<div class="step"><div class="bs-imp"></div>' + img(N + "warn.png", "left:1318px;top:626px;width:84px")
    + '<div class="bs-p" style="left:1408px;top:640px;height:60px;font:700 50px/1 Oswald,sans-serif;color:#ff3d8b">ВАЖНО!</div>'
    + img(N + "cat.png", "left:1585px;top:618px;width:163px")
    + '<div class="bs-p" style="left:1334px;top:704px;width:350px;height:86px;background:#ffe94d;border-radius:8px;'
      'font:600 21px/1.3 Oswald,sans-serif;align-items:flex-start;text-align:left;padding-left:12px">'
      '<span>LSA-1 и LSA-2 <span style="color:#d7186a">не проходят</span><br>через Area 0 — они описывают<br>топологию только своей области.</span></div>'
    + '<div class="bs-p" style="left:1354px;top:808px;font-size:17px;align-items:flex-start;text-align:left"><span>Через магистральную область (Area 0)<br>'
      'между ABR передаются <b style="font:700 17px Golos Text">LSA-3, LSA-4</b>&nbsp;и <b style="font:700 17px Golos Text">LSA-5.</b></span></div>'
    + '</div>',
])
