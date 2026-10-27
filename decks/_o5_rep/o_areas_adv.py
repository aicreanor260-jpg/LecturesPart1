# -*- coding: utf-8 -*-
"""Как идут объявления между областями OSPF: NSSA -> Area 0 -> обычная область / Stub."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import FADE
from _o5_g3kit import svg, puck, line, rect, cloud, path, cross, laptop, rack, pc, globe, cloud_icon

KB = "#4a9be8"


def doc(x, y, col, w=40):
    h = w * 1.25
    return (rect(x - w / 2, y - h / 2, w, h, "#fff", col, 6, 4)
            + path("M%.1f %.1f h%.1f M%.1f %.1f h%.1f M%.1f %.1f h%.1f" % (x - w * .28, y - h * .12, w * .56, x - w * .28, y + h * .08,
                                                                       w * .56, x - w * .28, y + h * .28, w * .4), col, 3.5))


def zone(x, y, w, h, fill, edge):
    return rect(x, y, w, h, fill, None, 26) + ('<rect x="%d" y="%d" width="%d" height="%d" rx="26" fill="none" stroke="%s" '
                                               'stroke-width="3" stroke-dasharray="3 7" stroke-linecap="round"/>' % (x, y, w, h, edge))


def scene():
    o = [zone(22, 248, 628, 566, "rgba(253,228,238,.78)", "#f08cb6"), zone(665, 238, 345, 576, "rgba(222,238,253,.8)", "#86bdf0"),
         zone(1020, 248, 495, 300, "rgba(255,246,214,.8)", "#efcf55"), zone(1020, 565, 495, 249, "rgba(253,228,238,.8)", "#f08cb6"),
         cloud(260, 715, 470, 150, "b", False), cloud(1260, 470, 420, 140, "b", False), cloud(1265, 755, 420, 110, "b", False),
         cloud_icon(90, 330, .9), cloud_icon(565, 365, .9), cloud_icon(1105, 365, .8), cloud_icon(980, 340, .7)]
    o += [path("M110 475 C130 520 175 525 225 520", KB, 6),
          '<path d="M30 470 C0 440 10 380 60 380 C60 340 120 330 145 360 C175 345 215 370 205 410 C235 420 230 480 190 480 Z" '
          'style="fill:#fff" stroke="#3f7fd0" stroke-width="5"/>', globe(112, 410, 32, "#2f7fd8")]
    # провода в NSSA
    for d in ["M312 560 C300 620 160 600 150 625", "M260 560 V640 L110 690", "M330 560 V700 L262 720", "M350 560 L360 640 L395 690"]:
        o.append(path(d, KB, 4))
    o += [laptop(150, 668, 104, "b"), rack(72, 692, 78, 96), pc(262, 790, 1.05), rack(358, 688, 76, 96)]
    for d in ["M1235 470 L1350 395", "M1260 480 L1400 430", "M1240 480 L1340 520", "M1230 745 L1360 715", "M1250 750 L1410 735"]:
        o.append(path(d, KB, 4))
    o += [laptop(1355, 392, 92, "b"), rack(1405, 368, 76, 120), pc(1335, 540, .9), laptop(1350, 725, 86, "b"), rack(1425, 680, 66, 108)]
    # стрелки
    o += [path("M405 530 H668", "#ff4f93", 26), '<path d="M664 504 L700 530 L664 556 Z" style="fill:#ff4f93"/>',
          path("M875 488 C960 480 1040 478 1118 480", "#2f86e6", 26), '<path d="M1112 454 L1152 480 L1112 506 Z" style="fill:#2f86e6"/>',
          path("M893 525 H1000 V500", "#9cc6ee", 7),
          path("M722 560 C700 610 640 604 470 604", "#ffd23a", 16), '<path d="M474 584 L442 604 L474 624 Z" style="fill:#ffd23a"/>',
          path("M880 555 L1100 702", "#8a8f9c", 7, "12 10"), '<path d="M1092 686 L1118 712 L1084 714 Z" style="fill:#8a8f9c"/>',
          cross(975, 622, 16), path("M632 688 H590", "#8a8f9c", 7, "12 10"), path("M535 630 L505 610", "#8a8f9c", 7, "12 10"),
          cross(556, 673, 16), doc(460, 520, "#ff4f93", 38), doc(1015, 450, "#2f86e6", 40), doc(672, 690, "#1f1a33", 40)]
    o += [puck(312, 492, 186, "p"), puck(793, 500, 178, "b"), puck(1235, 437, 152, "b"), puck(1235, 707, 152, "p")]
    return svg("".join(o), 1536, 1024)

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
    '<div class="step">' + scene()
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
    '<div class="step"><div class="aa-ban"></div><div class="aa-bw"></div>' + img(N + "cat2.png", "left:0;top:828px;width:330px;" + FADE)
    + '<div class="aa-bt"><span class="aa-pk">LSA-7</span> распространяется <span class="aa-pk">внутри NSSA</span>.<br>'
      'ABR преобразует подходящие <span class="aa-pk">LSA-7</span> в <span class="aa-bl">LSA-5</span> для обычных областей.</div></div>',
])
