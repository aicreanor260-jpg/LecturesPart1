# -*- coding: utf-8 -*-
"""Распространение LSA по областям: LSA-1/2, LSA-3, LSA-5, Stub/NSSA."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1536, 1024, 166
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


def pill(cx, y, w, text, bgc, s=21):
    return T(cx - w // 2, y, w, s, text, 700, ex="text-align:center;background:%s;border-radius:14px;padding:2px 0" % bgc)


CSS = """<style>
.ols-row{position:absolute;left:30px;width:1478px;background:rgba(255,255,255,.75);border:2px solid #ece6ef;border-radius:26px}
</style>"""


def row(y, h, card, title, sub, icon, iy, scene, note, ny, nw, nh, ricon, extra=""):
    x0, cw, ch, cy = card
    return ('<div class="step"><div class="ols-row" style="top:%dpx;height:%dpx"></div>' % (y, h)
            + B(x0, cy, cw, ch, title[1], 24)
            + img(icon, "left:46px;top:%dpx;width:90px" % iy)
            + T(152, cy + 18, cw - 120, 46, title[0], 700, f="Oswald", lh=1.1, ex="white-space:nowrap;letter-spacing:-.01em")
            + T(154, cy + 82, cw - 125, 21, sub, 500, lh=1.25, ex="white-space:nowrap")
            + scene + extra
            + T(note[0], ny, nw, note[2], note[1], 500, lh=1.3,
                ex="height:%dpx;background:#fdeea0;border-radius:18px;padding:12px 16px;box-sizing:border-box;white-space:nowrap" % nh)
            + ricon + '</div>')


HTML = CSS + bg("bg7", W, H) + "".join([
    row(172, 182, (36, 394, 160, 182), ("LSA-1 и LSA-2", "#ffe8ef"), "Топология одной<br>области", "o_lsa_spread_i1.png", 200,
        img("o_lsa_spread_s1.png", "left:440px;top:172px;width:672px") + pill(782, 184, 118, "Область 0", "#ffb3cd"),
        (1144, "Распространяются<br>внутри области", 24), 210, 266, 98, img("o_lsa_spread_r1.png", "left:1418px;top:215px;width:84px")),
    row(360, 196, (36, 322, 172, 372), ("LSA-3", "#e3f0fe"), "Сети других<br>областей", "o_lsa_spread_i2.png", 393,
        img("o_lsa_spread_s2.png", "left:362px;top:360px;width:820px") + pill(597, 384, 112, "Область 0", "#ffc4d8", 20)
        + pill(785, 399, 64, "ABR", "#ffe36e", 20) + pill(992, 384, 112, "Область 1", "#cfe5fd", 20),
        (1195, "ABR передаёт<br>сведения между<br>областями", 22), 400, 216, 122, img("o_lsa_spread_r2.png", "left:1418px;top:420px;width:84px")),
    row(564, 172, (34, 330, 150, 576), ("LSA-5", "#fff5cc"), "Внешние маршруты", "o_lsa_spread_i3.png", 593,
        img("o_lsa_spread_s3.png", "left:368px;top:565px;width:808px") + pill(568, 588, 66, "ASBR", "#ffe36e", 20)
        + pill(768, 580, 110, "Область 0", "#ffc4d8", 20) + pill(1032, 580, 110, "Область 1", "#cfe5fd", 20),
        (1180, "Распространяется<br>по областям,<br>принимающим LSA-5", 19.5), 590, 242, 120, img("o_lsa_spread_r3.png", "left:1428px;top:608px;width:74px")),
    '<div class="step"><div class="ols-row" style="top:742px;height:160px"></div>'
    + img("o_lsa_spread_s4.png", "left:30px;top:742px;width:1475px")
    + pill(426, 760, 70, "Stub", "#bcdcfb", 21) + pill(773, 760, 120, "Область 0", "#ffc4d8", 20)
    + pill(1134, 761, 76, "NSSA", "#ffe36e", 21) + '</div>',
    '<div class="step">' + B(54, 910, 1316, 70, "#ffe5ee", 35, "border:2px solid #ffc2d6")
    + img("o_lsa_spread_ex.png", "left:66px;top:918px;width:60px")
    + T(145, 926, 1220, 26, "<b style='font-weight:700'>Stub</b> не принимает LSA-5 <span style='color:#ff4f9a'>&bull;</span> "
        "NSSA использует LSA-7 для локальных внешних маршрутов", 500, ex="white-space:nowrap")
    + img("o_lsa_spread_cat.png", "left:1382px;top:905px;width:123px") + '</div>',
])
