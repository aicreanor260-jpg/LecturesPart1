# -*- coding: utf-8 -*-
"""Типы записей OSPF — LSA-5: AS External LSA. Внешний маршрут, введённый в OSPF."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_g5kit import svg, rtr, path, fat, blob, cloud_icon, server, laptop, globe, cross, doccard, ico, monitor

W, H, TOP = 1672, 941, 192
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


C = "text-align:center;white-space:nowrap"
BB = "<b style='font-weight:700'>%s</b>"


def pill(x, y, w, s, t, bgc, wt=700, ex=""):
    return T(x, y, w, s, t, wt, ex=C + ";background:%s;border-radius:18px;padding:4px 0;%s" % (bgc, ex))


PK, K = "#ff5c9e", "#ff8fbf"


def base():
    o = [blob(180, 450, 165, 150, "p", seed=3), blob(845, 420, 230, 160, "b", seed=1),
         blob(1440, 380, 220, 140, "b", seed=4)]
    o += [server(x, y, 52, 96) for x, y in ((60, 360), (118, 340), (200, 380), (255, 420))]
    o += [globe(150, 470, 52), cloud_icon(160, 560, 1.6)]
    o += [path("M845 345 L830 455 M845 345 L1090 420 M830 455 L1090 420", K, 5),
          path("M1420 330 L1560 300 M1420 330 L1560 400 M1420 330 L1450 445", K, 5)]
    o += [rtr(845, 340, 120, "b"), rtr(830, 450, 120, "b"), rtr(1420, 325, 110, "b"), rtr(1450, 440, 110, "b"),
          server(1540, 270, 60, 90), laptop(1580, 420, 80, "b")]
    return o


SC1 = svg("".join(base()) + fat((255, 430), (380, 440), PK, 18, 18))
SC2 = svg(rtr(475, 420, 170, "p", "OSPF", 4, 20))
SC3 = svg(fat((560, 440), (760, 440), PK, 14, 16) + doccard(580, 365, 48, "p") + fat((930, 440), (1000, 430), PK, 14, 16)
          + '<rect x="565" y="358" width="190" height="64" rx="14" fill="#fff" opacity=".85"/>' + doccard(578, 362, 50, "p"))
SC4 = svg(rtr(1090, 410, 150, "b") + fat((1165, 410), (1420, 395), PK, 12, 16)
          + '<rect x="1200" y="358" width="190" height="64" rx="14" fill="#fff" opacity=".85"/>' + doccard(1212, 362, 50, "p"))
SC5 = svg(blob(985, 670, 210, 95, "y", seed=2) + blob(1440, 650, 215, 105, "y", seed=5)
          + path("M1240 450 Q1250 560 1060 650", PK, 5, "12 9", "ap") + path("M1250 445 Q1300 540 1215 630", PK, 5, "12 9", "ap")
          + path("M1260 435 Q1440 470 1490 580", PK, 5, "12 9", "ap") + cross(1290, 545, 14) + cross(1462, 545, 14)
          + rtr(1030, 690, 110, "p") + laptop(1130, 720, 70, "b") + rtr(1310, 680, 110, "p") + server(1420, 690, 70, 48)
          + '<circle cx="878" cy="600" r="16" fill="#fff" stroke="#e8245e" stroke-width="5"/><path d="M867 589 L889 611" stroke="#e8245e" stroke-width="5"/>'
          + '<circle cx="1350" cy="585" r="16" fill="#fff" stroke="#e8245e" stroke-width="5"/><path d="M1339 574 L1361 596" stroke="#e8245e" stroke-width="5"/>')


S1 = ('<div class="step">' + SC1
      + pill(58, 222, 252, 20, "Другая автономная<br>система / внешние сети", "#ffd0e0", 600, "line-height:1.3")
      + T(206, 312, 100, 14, "Например,<br>Интернет или<br>другая AS", 500, lh=1.2, ex="text-align:center;transform:rotate(-6deg)")
      + T(68, 540, 200, 19, "Внешний префикс<br><b style='font-size:23px;font-weight:700'>198.51.100.0/24</b>", 400, lh=1.3, ex=C)
      + '</div>')
S2 = ('<div class="step"><div>' + SC2
      + T(372, 226, 236, 19, "ASBR создаёт LSA-5<br>для внешнего префикса<br><b style='font-weight:700'>198.51.100.0/24</b>", 600, lh=1.25,
          ex=C + ";transform:rotate(-5deg);background:#ffe36e;border-radius:16px;padding:6px 0")
      + pill(438, 503, 74, 23, "ASBR", "#ffc4d8", ex="padding:0")
      + T(348, 543, 255, 18, "Вводит внешние маршруты<br>в OSPF и генерирует LSA-5", 400, lh=1.3, ex=C) + '</div></div>')
S3 = ('<div class="step"><div>' + SC3 + T(636, 364, 110, 21, BB % "LSA-5" + "<br><span style='font-size:14px'>198.51.100.0/24</span>", 400,
                                      c="#c2185b", lh=1.25, ex="white-space:nowrap")
      + T(788, 222, 114, 21, "OSPF<br>Area 0", 600, lh=1.25, ex=C) + '</div></div>')
S4 = ('<div class="step"><div>' + SC4 + T(1060, 486, 70, 23, "ABR", 700, ex=C)
      + T(975, 521, 255, 16, "распространяет LSA-5 дальше,<br>обычно не создаёт его заново", 400, lh=1.32, ex=C + ";background:#e3f0fd;border-radius:14px;padding:4px 0")
      + T(1272, 364, 115, 21, BB % "LSA-5" + "<br><span style='font-size:14px'>198.51.100.0/24</span>", 400, c="#c2185b",
          lh=1.25, ex="white-space:nowrap")
      + T(1312, 211, 200, 20, "Обычная область<br>Area 0.0.0.2", 600, lh=1.25, ex=C) + '</div></div>')
S5 = ('<div class="step"><div>' + SC5 + T(907, 583, 60, 23, "Stub", 700, ex="white-space:nowrap")
      + T(845, 630, 120, 17, "LSA-5<br>не принимает", 500, lh=1.25, ex="white-space:nowrap")
      + T(1384, 566, 70, 23, "NSSA", 700, ex="white-space:nowrap")
      + T(1385, 598, 265, 16, BB % "LSA-5 не принимает" + "<br>по обычным правилам;<br>локальные внешние маршруты<br>вводятся через "
          + BB % "LSA-7", 500, lh=1.3, ex="white-space:nowrap") + '</div></div>')

NOTE = ('<div class="step"><div><div class="ab" style="position:absolute;left:1546px;top:196px;width:118px;padding:6px 6px;background:#ffe36e;'
        'border-radius:8px;transform:rotate(-6deg);font:600 12.5px/1.25 \'Golos Text\',sans-serif;color:#1f1a33;text-align:center">'
        'Маршруты из других сетей попадают в OSPF через ASBR <span style="color:#ff4f9a">&#9829;</span></div></div></div>')

CARDS = [("ASBR создаёт LSA-5<br>для внешнего префикса",
          "ASBR формирует LSA-5 и вводит<br>в OSPF маршруты из других автономных<br>систем и внешних источников."),
         ("Link State ID обозначает<br>внешний префикс",
          "В LSA-5 поле Link State ID содержит<br>адрес внешнего префикса<br>(например, 198.51.100.0/24)."),
         ("LSA-5 содержит метрику<br>и тип внешней метрики",
          "В объявлении указывается метрика<br>и тип внешней метрики:  E1 или E2,<br>которые влияют на выбор маршрута."),
         ("Суммирование внешних<br>объявлений можно настроить",
          "ASBR (или ABR) может суммировать<br>внешние маршруты, если это подходит<br>топологии и поддерживается.")]
XS = [32, 442, 848, 1262]


def cards():
    out = ['<div class="step">' + B(22, 762, 1628, 166, "rgba(255,255,255,.94)", 22, "border:2px solid #ece6ef") + '</div>']
    for i, ((h, p), x) in enumerate(zip(CARDS, XS)):
        out.append('<div class="step">' + ico(["doc", "ip", "gear", "tree"][i], x, 778, 82, ["#ffc2dc", "#cfe6fb", "#ffd23a", "#ffc2dc"][i], "#1f1a33", 2)
                   + T(x + 100, 784, 300, 18, h, 700, lh=1.25, ex="white-space:nowrap")
                   + T(x + 102, 848, 300, 14.5, p, 400, lh=1.4, ex="white-space:nowrap") + '</div>')
    return '<div class="step">' + "".join(out).replace('<div class="step">', "<div>") + "</div>"


HTML = bg("bg4", W, H) + S1 + S2 + S3 + S4 + S5 + NOTE + cards()
