# -*- coding: utf-8 -*-
"""Как идут объявления между областями OSPF: NSSA -> Area 0 -> обычная область / Stub."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1536, 1024, 220
N = "o_areas_adv_"

CSS = """<style>
.aa-p{position:absolute;border-radius:14px;text-align:center;color:#1f1a33;font:700 20px/1.2 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.aa-o{font-family:Oswald,sans-serif;font-weight:600}
.aa-pk{color:#ff3d8b}.aa-bl{color:#1d6fd0}
.aa-ban{position:absolute;left:22px;top:842px;width:1495px;height:160px;background:#fbd3e3;border-radius:22px}
.aa-bw{position:absolute;left:330px;top:858px;width:1170px;height:128px;background:#fff;border-radius:18px;border:2px solid #f6b9d0}
.aa-bt{position:absolute;left:450px;top:868px;font:600 34px/1.35 Oswald,sans-serif;color:#1f1a33;white-space:nowrap}
</style>"""


def p(x0, y0, x1, y1, col, html, extra=""):
    return '<div class="aa-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        x0, y0, x1 - x0, y1 - y0, col, extra, html)


Y = "#ffe57a"
HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="step">' + img(N + "scene.png", "left:12px;top:210px;width:1512px")
    + p(246, 223, 420, 272, "#ff5c9c", "<span style='color:#fff;font-size:36px'>NSSA</span>", "border-radius:24px")
    + p(742, 226, 924, 268, "#7cbaf5", "<span style='color:#fff;font-size:30px'>Area 0</span>", "border-radius:22px")
    + p(1142, 238, 1438, 279, "#ffe14d", "<span style='font-size:28px'>Обычная область</span>", "border-radius:22px")
    + p(1216, 565, 1362, 611, "#ff5c9c", "<span style='color:#fff;font-size:32px'>Stub</span>", "border-radius:22px")
    + p(52, 444, 168, 500, "#fff", "Внешняя<br>сеть", "font-size:21px")
    + '</div>',
    '<div class="step">'
    + p(180, 281, 494, 334, "#fff", "NSSA: LSA-7 — локальные<br>внешние маршруты", "font-size:19px;line-height:1.3")
    + p(232, 362, 398, 424, Y, "<span class='aa-o' style='font-size:22px;line-height:1.3'>ASBR-NSSA<br>создаёт LSA-7</span>")
    + p(242, 586, 364, 615, "#fff", "ASBR-NSSA", "font-size:19px")
    + p(427, 419, 628, 489, "#ffd0e0", "Распространяется<br>только внутри<br>NSSA", "font-weight:600;font-size:17px;line-height:1.25")
    + p(489, 504, 557, 536, "#fde3ec", "<span class='aa-pk aa-o' style='font-size:22px'>LSA-7</span>")
    + '</div>',
    '<div class="step">'
    + p(756, 275, 914, 303, "#fff", "магистраль", "font-size:19px")
    + p(740, 345, 912, 412, Y, "<span class='aa-o' style='font-size:19px;line-height:1.25'>Подходящий LSA-7<br>преобразуется<br>в LSA-5</span>", "transform:rotate(-4deg)")
    + p(744, 586, 858, 615, "#fff", "ABR-NSSA", "font-size:19px")
    + '</div>',
    '<div class="step">'
    + p(1124, 281, 1448, 313, "#fff", "принимает LSA-5", "font-size:19px")
    + p(1044, 430, 1122, 463, "#e2f0fd", "<span class='aa-bl aa-o' style='font-size:22px'>LSA-5</span>")
    + '</div>',
    '<div class="step">'
    + p(1222, 613, 1452, 646, "#fff", "не принимает LSA-5", "font-size:19px")
    + p(1048, 590, 1184, 650, "#ffd6e4", "<span class='aa-o' style='font-size:18px;line-height:1.3'>LSA-5 сюда<br>не передаётся</span>")
    + '</div>',
    '<div class="step">'
    + p(702, 655, 920, 726, Y, "<span class='aa-o' style='font-size:17px;line-height:1.3;text-align:left'>Default в NSSA:<br>"
      "<span class='aa-pk'>LSA-3</span> или <span class='aa-pk'>LSA-7</span> —<br>зависит от конфигурации</span>",
        "align-items:flex-start;padding-left:4px")
    + '</div>',
    '<div class="step"><div class="aa-ban"></div><div class="aa-bw"></div>' + img(N + "cat.png", "left:0;top:828px;width:330px")
    + '<div class="aa-bt"><span class="aa-pk">LSA-7</span> распространяется <span class="aa-pk">внутри NSSA</span>.<br>'
      'ABR преобразует подходящие <span class="aa-pk">LSA-7</span> в <span class="aa-bl">LSA-5</span> для обычных областей.</div></div>',
])
