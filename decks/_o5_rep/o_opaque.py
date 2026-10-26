# -*- coding: utf-8 -*-
"""Opaque LSA в OSPFv2: Type 9 / 10 / 11 — область распространения."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1536, 1024, 182
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


NW = "white-space:nowrap"
C = "text-align:center;white-space:nowrap"


def row(y, h, pill, pw, pc, text, tw, scene, sx, sy, deco, dx, dy, extra=""):
    return ('<div class="step">' + B(30, y, 1476, h, "rgba(255,255,255,.8)", 24, "border:2px solid #ece6ef")
            + img(scene, "left:%dpx;top:%dpx" % (sx, sy)) + extra
            + T(44, y + 10, pw, 38, pill, 700, f="Oswald", ex=NW + ";background:%s;border-radius:34px;padding:6px 30px;box-sizing:border-box;"
                "letter-spacing:-.01em" % pc)
            + img(deco, "left:%dpx;top:%dpx" % (dx, dy))
            + T(44, y + 86, tw, 27, text, 400, lh=1.25,
                ex=NW + ";background:#fff;border:2px solid #ece6ef;border-radius:18px;padding:12px 28px;box-sizing:border-box;height:90px")
            + '</div>')


def lbl(x, y, w, s, t, bgc):
    return T(x, y, w, s, t, 700, ex=C + ";background:%s;border-radius:14px;padding:2px 0" % bgc)


S3L = (lbl(783, 623, 174, 22, "OSPF domain", "#e0eefc") + lbl(566, 681, 86, 18, "Area 1", "#ffd0e0")
       + lbl(823, 681, 84, 18, "Area 0", "#cfe6fb") + lbl(1073, 681, 89, 18, "Area 2", "#ffd0e0")
       + lbl(1343, 632, 104, 17, "Stub Area", "#fff1b0") + lbl(1353, 756, 89, 17, "NSSA", "#d9ebfc"))

NOTE = ('<div class="step"><div><div class="ab" style="position:absolute;left:1316px;top:196px;width:184px;padding:10px 12px;'
        'background:#ffe36e;border-radius:16px;font:500 15px/1.3 \'Golos Text\',sans-serif;color:#1f1a33">'
        'Opaque LSA передают данные для приложений и расширений OSPF; промежуточные маршрутизаторы не обязаны понимать их содержимое'
        '</div></div></div>')

FOOT = ('<div class="step">' + B(30, 874, 1476, 118, "#ffe1ec", 28, "border:2px solid #ffc2d6")
        + img("o_opaque_warn.png", "left:52px;top:880px;width:110px")
        + T(196, 906, 290, 33, "Не путайте Type 9:", 700, f="Oswald", ex=NW)
        + T(495, 897, 370, 33, "OSPFv2 — Opaque LSA", 700, f="Oswald", ex=C + ";background:#ffb3cd;border-radius:31px;padding:10px 0")
        + T(874, 905, 26, 33, "&bull;", 700, ex=NW)
        + T(905, 897, 520, 33, "OSPFv3 — Intra-Area-Prefix LSA", 700, f="Oswald",
            ex=C + ";background:#bcdcfb;border-radius:31px;padding:10px 0") + '</div>')

HTML = bg("bg7", W, H) + "".join([
    row(190, 192, "Type 9 &bull; link-local", 366, "#ffc4d8", "Только в пределах<br>одного канала", 410, "o_opaque_s1.png", 462, 190,
        "o_opaque_d1.png", 410, 195),
    row(392, 214, "Type 10 &bull; area scope", 392, "#c9e2fc", "Только внутри своей<br>области", 410, "o_opaque_s2.png", 462, 392,
        "o_opaque_d2.png", 432, 395, lbl(878, 402, 140, 25, "Area 0", "#ffc4d8")),
    row(614, 248, "Type 11 &bull; AS scope", 356, "#ffe36e", "По OSPF-системе,<br>кроме Stub и NSSA", 368, "o_opaque_s3.png", 420, 614,
        "o_opaque_d3.png", 398, 620, S3L),
    NOTE, FOOT])
