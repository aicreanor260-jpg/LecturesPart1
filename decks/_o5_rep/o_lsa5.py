# -*- coding: utf-8 -*-
"""Типы записей OSPF — LSA-5: AS External LSA. Внешний маршрут, введённый в OSPF."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

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


S1 = ('<div class="step">' + img("o_lsa5_scene.png", "left:15px;top:192px;width:1645px")
      + pill(58, 222, 252, 20, "Другая автономная<br>система / внешние сети", "#ffd0e0", 600, "line-height:1.3")
      + T(206, 312, 100, 14, "Например,<br>Интернет или<br>другая AS", 500, lh=1.2, ex="text-align:center;transform:rotate(-6deg)")
      + T(68, 540, 200, 19, "Внешний префикс<br><b style='font-size:23px;font-weight:700'>198.51.100.0/24</b>", 400, lh=1.3, ex=C)
      + '</div>')
S2 = ('<div class="step"><div>'
      + T(372, 226, 236, 19, "ASBR создаёт LSA-5<br>для внешнего префикса<br><b style='font-weight:700'>198.51.100.0/24</b>", 600, lh=1.25,
          ex=C + ";transform:rotate(-5deg);background:#ffe36e;border-radius:16px;padding:6px 0")
      + pill(438, 503, 74, 23, "ASBR", "#ffc4d8", ex="padding:0")
      + T(348, 543, 255, 18, "Вводит внешние маршруты<br>в OSPF и генерирует LSA-5", 400, lh=1.3, ex=C) + '</div></div>')
S3 = ('<div class="step"><div>' + T(636, 364, 110, 21, BB % "LSA-5" + "<br><span style='font-size:14px'>198.51.100.0/24</span>", 400,
                                      c="#c2185b", lh=1.25, ex="white-space:nowrap")
      + T(788, 222, 114, 21, "OSPF<br>Area 0", 600, lh=1.25, ex=C) + '</div></div>')
S4 = ('<div class="step"><div>' + T(1060, 486, 70, 23, "ABR", 700, ex=C)
      + T(975, 521, 255, 16, "распространяет LSA-5 дальше,<br>обычно не создаёт его заново", 400, lh=1.32, ex=C)
      + T(1272, 364, 115, 21, BB % "LSA-5" + "<br><span style='font-size:14px'>198.51.100.0/24</span>", 400, c="#c2185b",
          lh=1.25, ex="white-space:nowrap")
      + T(1312, 211, 200, 20, "Обычная область<br>Area 0.0.0.2", 600, lh=1.25, ex=C) + '</div></div>')
S5 = ('<div class="step"><div>' + T(907, 583, 60, 23, "Stub", 700, ex="white-space:nowrap")
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
        out.append('<div class="step">' + img("o_lsa5_i%d.png" % (i + 1), "left:%dpx;top:772px;width:86px" % x)
                   + T(x + 100, 784, 300, 18, h, 700, lh=1.25, ex="white-space:nowrap")
                   + T(x + 102, 848, 300, 14.5, p, 400, lh=1.4, ex="white-space:nowrap") + '</div>')
    return '<div class="step">' + "".join(out).replace('<div class="step">', "<div>") + "</div>"


HTML = bg("bg4", W, H) + S1 + S2 + S3 + S4 + S5 + NOTE + cards()
