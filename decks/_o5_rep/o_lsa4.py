# -*- coding: utf-8 -*-
"""LSA-4 — ASBR Summary LSA: ABR сообщает другим областям, как добраться до ASBR. Схема — SVG, персонажей нет."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_g5kit import T, P, ico, svg, rtr as puck, blob, path, cloud_icon, globe, stx, C

W, H, TOP = 1672, 941, 206
K, BL, PK = "#3a3f55", "#3b9eff", "#ff5c9e"


def base():
    o = ['<rect x="30" y="236" width="760" height="404" rx="60" style="fill:#fde3ee" opacity=".85"/>',
         '<rect x="770" y="214" width="880" height="214" rx="60" style="fill:#e1effd" opacity=".9"/>',
         '<rect x="990" y="436" width="660" height="204" rx="60" style="fill:#fff3c4" opacity=".9"/>',
         cloud_icon(205, 455, 2.6), globe(205, 375, 26)]
    o += [path("M330 470 L505 470", K, 6), path("M720 455 L790 432", K, 6),
          path("M1315 300 L1540 325", K, 5), path("M1540 325 L1540 410", K, 4),
          path("M1330 545 L1510 578", K, 5)]
    o += [puck(610, 440, 220, "p"), puck(1300, 296, 130, "b"), puck(1540, 322, 120, "b"),
          puck(1330, 540, 130, "b"), puck(1510, 574, 120, "b")]
    return o


S1 = ('<div class="step">' + svg("".join(base()) + path("M335 420 L470 440", PK, 7, "16 10", "ap"))
      + P(345, 272, 216, 50, 32, "Область 1", "#ffb3cd")
      + T(100, 405, 206, 25, "<b style='font-weight:700'>Внешняя сеть</b><br>BGP / IS-IS /<br>статические", 400, lh=1.22,
          ex="text-align:center")
      + P(362, 366, 128, 46, 30, "LSA-5", "#ffc4d8")
      + P(528, 538, 184, 72, 28, "ASBR<span style='font-size:22px;font-weight:400'>Router ID R</span>", "#fff", r=14, ex="line-height:1.15")
      + '</div>')
S2 = ('<div class="step">' + svg(puck(885, 400, 210, "b"))
      + P(822, 508, 134, 44, 28, "ABR-1", "#eef6ff")
      + P(845, 222, 178, 82, 25, "ABR создаёт<br><b style='font-weight:700;font-size:29px'>LSA-4</b>", "#ffe36e", 600,
          ex="line-height:1.15") + '</div>')
S3 = ('<div class="step">' + svg(path("M985 380 Q1040 310 1215 300", BL, 6, "14 10", "ab"))
      + P(1050, 279, 106, 38, 27, "LSA-4", "#9fcbf7")
      + T(1030, 320, 180, 19, "ASBR R доступен<br>через ABR-1", 500, ex="text-align:center;transform:rotate(-9deg)")
      + P(1395, 210, 150, 44, 28, "Область 0", "#bcdcfb", c="#1f5fae") + '</div>')
S4 = ('<div class="step">' + svg(path("M1000 462 Q1150 470 1255 520", BL, 6, "14 10", "ab"))
      + P(1110, 455, 106, 38, 27, "LSA-4", "#9fcbf7")
      + T(1060, 506, 180, 19, "ASBR R доступен<br>через ABR-1", 500, ex="text-align:center;transform:rotate(-9deg)")
      + P(1365, 436, 252, 44, 28, "Другие области", "#ffe36e") + '</div>')

CARDS = [("Сообщает,<br>как добраться<br>до ASBR", "#ffe8ef", 600, 23, "pin", "p"),
         ("ASBR вводит<br>в OSPF внешние<br>маршруты: BGP,<br>IS-IS или статические", "#e3f0fe", 500, 21, "globe", "b"),
         ("LSA-5 объявляет<br>внешнюю сеть;<br>LSA-4 помогает<br>найти ASBR", "#fff5cc", 500, 22, "doc", "y"),
         ("LSA-4 создаёт<br>ABR для других<br>областей", "#ffe8ef", 500, 23, "gear", "p"),
         ("Link State ID —<br>Router ID ASBR", "#e3f0fe", 400, 23, "user", "b"),
         ("Advertising Router —<br>Router ID ABR", "#fff5cc", 400, 21, "user", "y"),
         ("Флаг Е в LSA-1<br>отмечает<br>маршрутизатор-ASBR", "#ffe8ef", 500, 21, "flag", "p")]
XS = [(36, 210), (258, 234), (500, 238), (744, 214), (968, 196), (1176, 208), (1394, 248)]
NC2 = {"p": "#c2185b", "b": "#1f5fae", "y": "#8a5a00"}
NC = {"p": "#ff8fbf", "b": "#8cc4f5", "y": "#ffd23a"}


def cards():
    out = []
    for i, ((t, c, wt, s, ic, tn), (x, w)) in enumerate(zip(CARDS, XS)):
        out.append('<div>' + P(x, 652, w, 254, 1, "", c, r=20)
                   + P(x + 12, 664, 40, 40, 19, "%02d" % (i + 1), NC[tn], 800, r=20)
                   + ico(ic, x + w // 2 - 38, 670, 86, "#ffffffcc", ink=NC2[tn], sw=2.3)
                   + T(x + 16, 772, w - 20, s - 1.5, t, wt, lh=1.3, ex="white-space:nowrap;letter-spacing:-.01em") + '</div>')
    return '<div class="step">' + "".join(out) + "</div>"


HTML = bg("bg4", W, H) + S1 + S2 + S3 + S4 + cards()
