# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _k import css, box, tx, step, svg, path
W, H, TOP = 1672, 941, 78
P = "m4x-o2"
CSS = css(P) + """<style>
.m4x-o2-num{position:absolute;width:58px;height:58px;border-radius:50%;box-sizing:border-box;border:2.5px solid #f0c75e;
 background:radial-gradient(#0b2a22,#04140f);box-shadow:0 0 16px rgba(240,199,94,.7);font:800 38px/52px "Playfair Display",serif;font-variant-numeric:lining-nums;color:#fff0b8;text-align:center}
.m4x-o2-chev{position:absolute;font:300 48px/1 "Golos Text",sans-serif;color:#f0c75e;text-shadow:0 0 8px #f0c75e}
</style>"""


def rt(cx, cy, w=118):
    return img("o2_router.png", "left:%dpx;top:%dpx;width:%dpx" % (cx - w / 2, cy - w * 80 / 118 / 2, w))


def cl(cx, cy, w):
    return img("o2_cloud.png", "left:%dpx;top:%dpx;width:%dpx" % (cx - w / 2, cy - w * 140 / 240 / 2, w))


top = svg(P,
    path(P, "M590 255 C520 190 420 170 335 185", "g", 3.2, True) +
    path(P, "M695 258 C790 215 900 230 995 280", "g", 3.2, True) +
    path(P, "M1100 290 L1290 308", "g", 3.4, True) +
    path(P, "M585 262 C470 262 400 300 335 307", "b", 3) +
    path(P, "M690 262 C740 268 770 290 790 308", "b", 3) +
    path(P, "M995 315 C960 320 920 325 890 322", "b", 3) +
    path(P, "M900 345 C1050 380 1200 360 1285 335", "b", 3) +
    path(P, "M335 420 C500 330 700 400 865 430", "s", 2.6, True) +
    path(P, "M980 425 C1100 420 1200 385 1285 345", "s", 2.6, True))

PW = [(22, 538, 393, 307), (440, 538, 386, 307), (850, 538, 385, 307), (1257, 538, 393, 307)]
heads = [("Один маршрут →", "выбрать его"), ("Одинаковый префикс →", "меньшее preference"),
         ("Равное preference →", "меньший cost"), ("Равные preference", "и cost → оба маршрута")]
cx = [218, 633, 1042, 1454]


def panel(i):
    x, y, w, h = PW[i]
    return (box(P, x, y, w, h, "", "border-radius:26px;background:rgba(6,30,24,.55)") +
            '<div class="m4x-o2-num" style="left:%dpx;top:%dpx">%d</div>' % (cx[i] - 29, 512, i + 1) +
            tx(P, "s", cx[i], 580, heads[i][0], 27, 380) + tx(P, "s", cx[i], 613, heads[i][1], 27, 380))


s1 = (rt(80, 727, 105) + cl(327, 735, 120) + svg(P, path(P, "M135 728 L272 728", "g", 3.4, True)))
s2 = (rt(500, 680, 62) + rt(500, 735, 62) + rt(500, 790, 62) + cl(743, 745, 110) +
      svg(P, path(P, "M535 678 C610 690 650 720 695 740", "g", 3, True) + path(P, "M535 735 L695 740", "s", 2.6, True) +
          path(P, "M535 788 C610 780 650 760 695 745", "s", 2.6, True)))
s3 = (rt(910, 680, 62) + rt(910, 735, 62) + rt(910, 790, 62) + cl(1152, 745, 110) +
      svg(P, path(P, "M945 678 C1020 690 1060 720 1105 740", "g", 3, True) + path(P, "M945 735 L1105 740", "b", 2.6, True) +
          path(P, "M945 788 C1020 780 1060 760 1105 745", "s", 2.6, True)))
s4 = (rt(1330, 700, 72) + rt(1330, 773, 72) + cl(1565, 745, 115) +
      svg(P, path(P, "M1372 698 C1440 700 1480 725 1520 740", "g", 3.2, True) + path(P, "M1372 775 C1440 775 1480 760 1520 748", "g", 3.2, True)))

HTML = CSS + bg() + "".join([
    step(tx(P, "s", 836, 112, "Как маршрут попадает в таблицу маршрутизации", 31, 900, "font-weight:700")),
    step(top, rt(270, 190), rt(270, 305), rt(270, 420), rt(633, 258), rt(840, 325), rt(1047, 293), rt(922, 425), cl(1410, 310, 240)),
    step(panel(0), s1), step(panel(1), s2), step(panel(2), s3), step(panel(3), s4),
    step('<div class="m4x-o2-chev" style="left:420px;top:652px">&#8250;</div><div class="m4x-o2-chev" style="left:830px;top:652px">&#8250;</div><div class="m4x-o2-chev" style="left:1239px;top:652px">&#8250;</div>'),
])
