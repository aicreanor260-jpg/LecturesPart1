# -*- coding: utf-8 -*-
"""Типы записей OSPF — LSA-8 и LSA-9: номер типа зависит от версии протокола (OSPFv2 / OSPFv3)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_g5kit import svg, rtr, drum, path, line, laptop, monitor, ico, wifi, cloud_icon, FADE

W, H, TOP = 1774, 887, 150
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


ICS = {0: ("bulb", "#ffe36e"), 1: ("gear", "#8cc4f5"), 2: ("doc", "#ffc2dc"), 6: ("people", "#ffc2dc"), 7: ("share", "#bcdcfb"),
       8: ("ban", "#ffe36e"), 9: ("bulb", "#ffffff"), 10: ("link", "#ffc2dc"), 11: ("tree", "#bcdcfb"), 12: ("list", "#ffe36e"),
       13: ("excl", "#ff5c9e"), 14: ("globe", "#bcdcfb")}


def I(k, x, y, w=None):
    """Значок-кружок вместо вырезки."""
    if k in (3, 4):
        return P2(x + 4, y + 4, 64, str(k - 2), "#ff5c9e" if k == 3 else "#3b9eff")
    if k == 5:
        return svg('<path d="M%d %d l38 66 h-76 z" style="fill:#ffe36e" stroke="#1f1a33" stroke-width="5" stroke-linejoin="round"/>'
                   '<path d="M%d %d v22" stroke="#1f1a33" stroke-width="8" stroke-linecap="round"/><circle cx="%d" cy="%d" r="4.5" fill="#1f1a33"/>'
                   % (x + 44, y + 10, x + 44, y + 36, x + 44, y + 68), 1774, 887)
    n, f = ICS[k]
    d = {9: 50, 13: 52}.get(k, 66 if k < 6 else 60)
    return ico(n, x, y, d, f, "#fff" if k == 13 else "#1f1a33", 2.2)


def P2(x, y, d, t, col):
    return ('<div class="ab" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:50%%;background:%s;color:#fff;'
            'font:700 34px/%dpx Golos Text,sans-serif;text-align:center;border:4px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,.12)">%s</div>'
            % (x, y, d, d, col, d - 8, t))


def pic():
    o = ['<ellipse cx="655" cy="640" rx="190" ry="210" style="fill:#fde3ee" opacity=".75"/>',
         monitor(560, 440, 110, "#cfe6fb"), monitor(770, 450, 140, "#9fcaf3"), wifi(770, 340, .7, "#fff"),
         '<text x="770" y="392" text-anchor="middle" font-size="26" font-weight="800" style="fill:#fff">IPv4</text>',
         '<path d="M500 580 L660 510 L820 580 L660 650 z" style="fill:#fff3f8" stroke="#c9407a" stroke-width="3"/>'
         '<path d="M500 580 V670 L660 740 V650 z" style="fill:#ffd6e5" stroke="#c9407a" stroke-width="3"/>'
         '<path d="M660 650 V740 L820 670 V580 z" style="fill:#f7b8d0" stroke="#c9407a" stroke-width="3"/>'
         '<text x="742" y="676" text-anchor="middle" font-size="30" font-weight="800" transform="rotate(-23 742 676)" style="fill:#2f7fe0">OSPFv2</text>']
    for i in range(5):
        x, y = 515 + i * 27, 615 + i * 12
        o.append('<path d="M%d %d l18 8 v16 l-18 -8 z" fill="#2a2f3d"/>' % (x, y))
    o += [path("M535 660 Q490 720 520 770", "#7fb6ee", 8), path("M590 690 Q600 760 650 800", "#ff8fbf", 8),
          path("M720 715 Q760 750 770 790", "#7fb6ee", 8), laptop(520, 830, 100, "b"), monitor(650, 868, 110, "#bcd9f6"),
          laptop(785, 840, 90, "p")]
    return svg("".join(o), 1774, 887)


RM = ("-webkit-mask:radial-gradient(ellipse 50% 50% at 50% 50%,#000 62%,transparent 100%);"
      "mask:radial-gradient(ellipse 50% 50% at 50% 50%,#000 62%,transparent 100%)")
NW = "white-space:nowrap"
C = "text-align:center;white-space:nowrap"
CSS = """<style>
.o89-hy{background:#ffe36e;border-radius:6px;padding:0 4px}
.o89-hb{background:#bcdcfb;border-radius:6px;padding:0 4px}
.o89-hp{background:#ffc4d8;border-radius:6px;padding:0 4px}
.o89 b{font-weight:700}
</style>"""

INFO = [(60, 50, 350, "<b>LSA (Link-State Advertisement)</b> —<br>это типы записей, которые<br>распространяются в OSPF."),
        (420, 412, 316, "<b>Разные версии</b> OSPF<br>используют разные наборы<br>типов и значения номеров."),
        (750, 740, 330, "LSA содержат информацию<br>о топологии, префиксах и других<br>данных о сети.")]


def top():
    out = ['<div class="step o89">']
    for i, (ix, bx, bw, t) in enumerate(INFO):
        out.append(B(bx, 160, bw, 82, "rgba(255,255,255,.92)", 41, "border:2px solid #ece6ef") + I(i, ix, 165)
                   + T(ix + 78, 176, bw - 90, 13.5, t, 400, lh=1.3, ex=NW))
    out.append(img("o_lsa89_girl2.png", "left:1400px;top:150px;height:100px;" + RM))
    out.append('<div class="ab" style="position:absolute;left:1600px;top:156px;padding:6px 14px;background:#ffe36e;border-radius:8px;'
               'transform:rotate(-5deg);font:600 18px/1.25 \'Golos Text\',sans-serif;color:#1f1a33;white-space:nowrap">'
               'Одна тема —<br>две версии<br>протокола <span style="color:#ff4f9a">&#9829;</span></div>')
    return "".join(out) + '</div>'


V2 = ('<div class="step o89">' + B(20, 254, 836, 618, "rgba(255,255,255,.9)", 26, "border:2.5px solid #9ec8f5")
      + pic() + img("o_lsa89_cat.png", "left:590px;top:430px;width:145px;" + RM)
      + B(36, 264, 604, 80, "#d6e9fd", 40) + T(70, 266, 300, 70, "OSPFv2", 800, ex=NW)
      + T(388, 278, 250, 22, "Базовая версия OSPF<br>для IPv4", 400, lh=1.15, ex=NW)
      + '<div class="ab" style="position:absolute;left:292px;top:752px;padding:6px 14px;background:#ffe36e;border-radius:8px;'
        'transform:rotate(-12deg);font:600 18px/1.3 \'Golos Text\',sans-serif;white-space:nowrap">Классический OSPF<br>Всё ещё широко<br>'
        'используется <span style="color:#ff4f9a">&#9829;</span></div>'
      + '</div><div class="step o89">'
      + B(36, 362, 420, 92, "#fff", 22, "border:2px solid #ece6ef") + I(3, 45, 375)
      + T(132, 376, 330, 23, "<b>Базовый RFC 2328</b><br>определяет типы <span class='o89-hy'><b>LSA 1–5</b></span>", 500, lh=1.35, ex=NW)
      + B(36, 466, 420, 120, "#fff", 22, "border:2px solid #ece6ef") + I(4, 45, 480)
      + T(132, 480, 330, 23, "Позже добавлены <span class='o89-hb'><b>LSA-7</b></span><br>для NSSA и Opaque LSA<br>"
          "<span class='o89-hy'><b>типов 9, 10, 11</b></span>", 500, lh=1.35, ex=NW)
      + '</div><div class="step o89">'
      + B(36, 604, 420, 124, "#ffe1ec", 22) + I(5, 42, 618)
      + T(146, 624, 310, 23, "<b>Не считайте</b> <span class='o89-hp'><b>LSA-8</b></span><br>обычным типом базового<br>набора OSPFv2.", 500,
          lh=1.35, ex=NW) + '</div>')

T8 = [(6, 548, "Сообщает соседям на канале<br><b>link-local</b> адрес автора<br>и префиксы этого канала."),
      (7, 612, "<b>Область распространения</b> —<br>только этот канал."),
      (8, 675, "<b>Через ABR</b> в другие области<br>не передаётся.")]
T9 = [(10, 580, "Связывает IPv6-префиксы<br>с маршрутизатором или транзитной<br>сетью."),
      (11, 650, "Распространяется <b>внутри области.</b>"),
      (12, 714, "В OSPFv3 сведения о префиксах<br><b>вынесены в отдельные объявления.</b>")]

V3 = ('<div class="step o89">' + B(874, 254, 882, 618, "rgba(255,255,255,.9)", 26, "border:2.5px solid #ffb3cd")
      + B(888, 264, 550, 80, "#ffd6e5", 40) + T(924, 266, 300, 70, "OSPFv3", 800, ex=NW)
      + T(1268, 278, 170, 22, "Версия OSPF<br>для IPv6", 400, lh=1.15, ex=NW)
      + B(1526, 264, 218, 80, "#fff", 22, "border:2px solid #ece6ef") + I(14, 1530, 270)
      + T(1610, 276, 140, 14.5, "Работает с IPv6<br>и имеет другую<br>структуру LSA", 400, lh=1.2, ex=NW)
      + '</div><div class="step o89">'
      + B(888, 352, 420, 448, "#fff", 22, "border:2px solid #d6e9fd") + B(888, 352, 420, 46, "#cfe6fb", 22)
      + T(920, 358, 380, 26, "<b>Тип 8 — Link-LSA</b>", 500, ex=NW)
      + svg(path("M985 478 H1215", "#7fb6ee", 16) + rtr(970, 462, 110, "b", "R1", 2, 20) + rtr(1230, 462, 110, "p", "R2", 2, 20), 1774, 887)
      + T(1036, 414, 140, 17.5, "Канал<br>(link-local)", 600, c="#1f5fae", lh=1.2, ex=C)
      + T(1040, 502, 124, 15, "link-local<br>fe80::/64", 600, c="#1f5fae", lh=1.1, ex=C)
      + "".join(I(k, 910, y) + T(1000, y + 6, 300, 15.5, t, 400, lh=1.25, ex=NW) for k, y, t in T8)
      + B(898, 740, 402, 56, "#fff", 14, "border:2px dashed #ffb3cd") + I(9, 912, 742)
      + T(976, 744, 320, 14.5, "Формирование не определяется<br>простым условием \"на канале больше<br>одного маршрутизатора\".", 500,
          lh=1.15, ex=NW)
      + '</div><div class="step o89">'
      + B(1320, 352, 426, 448, "#fff", 22, "border:2px solid #ffd6e5") + B(1320, 352, 426, 46, "#ffd6e5", 22)
      + T(1346, 358, 400, 26, "<b>Тип 9 — Intra-Area-Prefix LSA</b>", 500, ex=NW)
      + svg('<ellipse cx="1610" cy="442" rx="105" ry="34" style="fill:#ffd6e5"/>' + path("M1418 490 V522 H1490", "#1f1a33", 4)
                + path("M1480 470 Q1520 470 1545 495", "#ff5c9e", 5, mk="ap") + rtr(1418, 462, 110, "b", "R1", 2, 20)
                + '<rect x="1490" y="508" width="66" height="26" rx="6" style="fill:#e3f0fd" stroke="#3f86d8" stroke-width="2.4"/>'
                + '<rect x="1566" y="502" width="86" height="32" rx="6" style="fill:#bcdcfb" stroke="#3f86d8" stroke-width="2.4"/>', 1774, 887)
      + T(1530, 432, 160, 17, "<b>2001:db8:1::/64</b>", 500, ex=C)
      + T(1458, 543, 160, 13, "Связан с Router LSA<br>или Network LSA", 500, c="#1f5fae", lh=1.15, ex=C)
      + "".join(I(k, 1335, y) + T(1424, y + 12, 320, 15.5, t, 400, lh=1.25, ex=NW) for k, y, t in T9)
      + '</div><div class="step o89">' + B(888, 808, 858, 58, "#ffe78a", 29) + I(13, 908, 808)
      + T(1008, 812, 720, 21, "<b>OSPFv3 изменил структуру LSA:</b><br><span style='font-size:16.5px'>названия и значения типов "
          "нельзя переносить из OSPFv2 напрямую.</span>", 500, lh=1.12, ex=NW) + '</div>')

HTML = CSS + bg("bg5", W, H) + top() + V2 + V3
