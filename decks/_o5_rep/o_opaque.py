# -*- coding: utf-8 -*-
"""Opaque LSA в OSPFv2: Type 9 / 10 / 11 — область распространения."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_g5kit import line, svg, rtr, path, blob, cross, ico, area

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
            + scene + extra
            + T(44, y + 10, pw, 38, pill, 700, f="Oswald", ex=NW + ";background:%s;border-radius:34px;padding:6px 30px;box-sizing:border-box;"
                "letter-spacing:-.01em" % pc)
            + T(44, y + 86, tw, 27, text, 400, lh=1.25,
                ex=NW + ";background:#fff;border:2px solid #ece6ef;border-radius:18px;padding:12px 28px;box-sizing:border-box;height:90px")
            + '</div>')


def S(b):
    return svg(b, 1536, 1024)


PK, GR = "#ff3d8b", "#c9b8d8"
SC1 = S('<path d="M470 360 L1500 360 L1470 300 L520 300 z" style="fill:#fde3ee" opacity=".7"/>'
        + path("M720 330 H1080", "#7fb6ee", 12) + rtr(680, 295, 150, "p", "R1", 2, 24) + rtr(1140, 295, 150, "b", "R2", 2, 24)
        + line((830, 275), (990, 275), PK, 8, mk="ap", both=True))


def mini(x, y, tone, w=78):
    return rtr(x, y, w, tone, None, 2)


SC2 = S('<ellipse cx="950" cy="500" rx="290" ry="98" style="fill:#fde3ee" stroke="#f2639a" stroke-width="2.6" stroke-dasharray="12 9"/>'
        + path("M570 505 L780 470 M1110 470 L1350 505 M780 470 L1110 470 M780 470 L945 560 M1110 470 L945 560", GR, 3)
        + mini(565, 495, "k", 80) + mini(1355, 495, "k", 80) + mini(780, 460, "p", 100) + mini(1115, 460, "p", 100)
        + mini(945, 550, "p", 110) + line((860, 465), (1035, 465), PK, 7, mk="ap", both=True)
        + line((820, 505), (885, 548), PK, 5, mk="ap", both=True)
        + line((1075, 505), (1010, 548), PK, 5, mk="ap", both=True))
SC3 = S('<ellipse cx="850" cy="745" rx="420" ry="105" style="fill:#e3f0fd" opacity=".8" stroke="#8fbff0" stroke-width="2.6"/>'
        + blob(600, 755, 115, 75, "p", seed=1) + blob(860, 755, 120, 80, "b", seed=2) + blob(1110, 755, 115, 75, "p", seed=3)
        + blob(1390, 685, 100, 52, "y", seed=4) + blob(1390, 800, 100, 52, "b", seed=5)
        + "".join(path("M%d %d L%d %d" % a, "#f29cc2", 3) for a in ((545, 735, 655, 735), (545, 735, 600, 785), (655, 735, 600, 785),
                                                                   (1055, 735, 1165, 735), (1055, 735, 1110, 785), (1165, 735, 1110, 785)))
        + path("M800 735 H920 M800 735 L860 790 M920 735 L860 790", "#8fbff0", 3)
        + "".join(mini(x, y, t, 58) for x, y, t in ((545, 735, "p"), (655, 735, "p"), (600, 785, "p"), (800, 735, "b"), (920, 735, "b"),
                                                  (860, 790, "b"), (1055, 735, "p"), (1165, 735, "p"), (1110, 785, "p")))
        + "".join(mini(x, y, "k", 48) for x, y in ((1345, 680), (1440, 680), (1392, 708), (1345, 798), (1440, 798), (1392, 822)))
        + line((694, 740), (764, 740), PK, 4, mk="ap", both=True)
        + line((958, 740), (1018, 740), "#b9a4f2", 4, mk="av", both=True)
        + path("M1295 698 L1232 718", "#9aa3b2", 4, "8 6", mk="ak") + path("M1295 797 L1232 782", "#9aa3b2", 4, "8 6", mk="ak")
        + cross(1272, 690, 11, "#e8245e", 6) + cross(1272, 795, 11, "#e8245e", 6))
WARN = S('<path d="M110 884 L60 972 H160 z" style="fill:#ff7aa8" stroke="#1f1a33" stroke-width="4" stroke-linejoin="round"/>'
         '<path d="M110 912 V945" stroke="#1f1a33" stroke-width="9" stroke-linecap="round"/><circle cx="110" cy="960" r="5.5" fill="#1f1a33"/>')


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
        + WARN
        + T(196, 906, 290, 33, "Не путайте Type 9:", 700, f="Oswald", ex=NW)
        + T(495, 897, 370, 33, "OSPFv2 — Opaque LSA", 700, f="Oswald", ex=C + ";background:#ffb3cd;border-radius:31px;padding:10px 0")
        + T(874, 905, 26, 33, "&bull;", 700, ex=NW)
        + T(905, 897, 520, 33, "OSPFv3 — Intra-Area-Prefix LSA", 700, f="Oswald",
            ex=C + ";background:#bcdcfb;border-radius:31px;padding:10px 0") + '</div>')

HTML = bg("bg7", W, H) + "".join([
    row(190, 192, "Type 9 &bull; link-local", 366, "#ffc4d8", "Только в пределах<br>одного канала", 410, SC1, 462, 190, None, 0, 0),
    row(392, 214, "Type 10 &bull; area scope", 392, "#c9e2fc", "Только внутри своей<br>области", 410, SC2, 462, 392, None, 0, 0, lbl(878, 402, 140, 25, "Area 0", "#ffc4d8")),
    row(614, 248, "Type 11 &bull; AS scope", 356, "#ffe36e", "По OSPF-системе,<br>кроме Stub и NSSA", 368, SC3, 420, 614, None, 0, 0, S3L),
    NOTE, FOOT])
