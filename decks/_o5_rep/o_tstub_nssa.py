# -*- coding: utf-8 -*-
"""Типы областей OSPF — Totally Stubby, NSSA, Totally NSSA + сравнение."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1942, 809, 118
N = "o_tstub_nssa_"

CSS = """<style>
.tn-pan{position:absolute;top:125px;height:563px;border-radius:20px;border:2px solid}
.tn-num{position:absolute;top:140px;width:44px;height:44px;border-radius:50%;font:700 28px/44px Oswald,sans-serif;text-align:center}
.tn-h{position:absolute;top:134px;font:700 42px/1.15 Oswald,sans-serif;color:#1f1a33;white-space:nowrap}
.tn-t{position:absolute;font:400 17.5px/1.25 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.tn-p{position:absolute;border-radius:10px;text-align:center;color:#1f1a33;font:600 14px/1.2 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.tn-row{position:absolute;height:66px;background:#fff;border:1.5px solid #ece7f1;border-radius:33px}
.tn-rt{position:absolute;font:400 14px/1.25 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.tn-cmp{position:absolute;top:702px;height:94px;border-radius:14px}
.tn-ok,.tn-no{display:inline-block;width:17px;height:17px;border-radius:50%;color:#fff;font:700 12px/17px sans-serif;text-align:center;margin-right:10px}
.tn-ok{background:#2fb24c}.tn-no{background:#ef3b5b}
</style>"""


def p(x0, y0, x1, y1, col, html, extra=""):
    return '<div class="tn-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        x0, y0, x1 - x0, y1 - y0, col, extra, html)


def t(x, y, html, extra=""):
    return '<div class="tn-t" style="left:%dpx;top:%dpx;%s">%s</div>' % (x, y, extra, html)


def row(x0, y, x1, ico, ix, iy, text, tx, ty):
    return ('<div class="tn-row" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x0, y, x1 - x0)
            + img(N + ico + ".png", "left:%dpx;top:%dpx" % (ix, iy))
            + '<div class="tn-rt" style="left:%dpx;top:%dpx">%s</div>' % (tx, ty, text))


def head(x0, x1, col, bd, nc, n, title, hx):
    return ('<div class="tn-pan" style="left:%dpx;width:%dpx;background:%s;border-color:%s"></div>' % (x0, x1 - x0, col, bd)
            + '<div class="tn-num" style="left:%dpx;background:%s;color:%s">%s</div>' % (x0 + 18, nc, "#fff" if n != "3" else "#1f1a33", n)
            + '<div class="tn-h" style="left:%dpx">%s</div>' % (hx, title))


PK, BL, YL, GR = "#ffc4d8", "#cfe4fa", "#ffe14d", "#e9e9ee"
AREA = "font:700 17px/1 'Golos Text',sans-serif;color:#d63c7a;background:#fbd3e3"

HTML = CSS + bg("bg7", W, H) + "".join([
    # 1. Totally Stubby
    '<div class="step">' + head(15, 642, "#fff6f9", "#f6bdd2", "#ff5c9c", "1", "TOTALLY STUBBY", 95)
    + p(374, 140, 626, 204, "#fff0a8", "Расширение, распространённое<br>в реализации производителей;<br>не отдельный базовый тип RFC 2328.",
        "font:400 13px/1.3 'Golos Text',sans-serif;align-items:flex-start;text-align:left;padding-left:10px")
    + t(34, 202, "Внутри области <b>только внутренние маршруты</b>.<br>Внешний доступ — через маршрут по умолчанию.")
    + img(N + "p1.png", "left:28px;top:262px;width:614px")
    + p(56, 290, 212, 368, "#fff", "Внутренний<br>маршрутизатор<br>знает внутреннюю<br>топологию области.", "font-weight:500;align-items:flex-start;text-align:left;padding-left:4px")
    + p(238, 288, 420, 340, "#fbc0d6", "Внутренние<br>маршруты (LSA-1, LSA-2)")
    + p(530, 289, 618, 347, "#d7e9fb", "Остальные<br>области<br>OSPF", "font-size:15px;line-height:1.15")
    + p(412, 455, 526, 512, "#ffe78a", "Маршрут<br>по умолчанию<br>(0.0.0.0/0)", "font-size:13px")
    + p(145, 492, 340, 518, "", "Область Totally Stubby", AREA)
    + row(42, 548, 618, "a1", 50, 546, "<b>ABR</b> не передаёт подробные<br>межобластные и внешние маршруты,<br>а даёт маршрут по умолчанию.", 150, 552)
    + row(42, 622, 618, "a2", 50, 622, "<b>ASBR</b> внутри области <b style='background:#ffe94d'>не размещают</b>.", 150, 640)
    + '</div>',
    # 2. NSSA
    '<div class="step">' + head(650, 1270, "#f3f9ff", "#9fcbf2", "#2f8fe8", "2", "NSSA", 732)
    + t(672, 186, "В области есть ASBR, который объявляет локальные<br>внешний маршруты. Обычные LSA-5 извне не поступают.")
    + img(N + "p2.png", "left:654px;top:244px;width:612px")
    + p(668, 266, 790, 320, GR, "Внешняя сеть<br>(например,<br>(Интернет)", "font-size:13px;border-radius:24px")
    + p(893, 264, 1012, 300, BL, "Внутренний<br>маршрутизатор", "font-size:13px")
    + p(1062, 252, 1212, 306, YL, "Преобразование<br>подходящего LSA-7<br>в LSA-5", "font-size:13px")
    + p(742, 326, 890, 368, PK, "Локальные внешние<br>маршруты")
    + p(812, 386, 890, 456, PK, "<b style='color:#d63c7a;font-size:16px'>LSA-7</b><span style='font-size:11px;font-weight:400'>(локальные<br>внешние<br>маршруты)</span>")
    + p(1127, 315, 1256, 358, PK, "<b style='color:#d63c7a;font-size:16px'>LSA-5</b>(в другие области)", "font-size:13px")
    + p(1030, 455, 1146, 512, BL, "Маршрут<br>по умолчанию<br>(0.0.0.0/0)", "font-size:13px")
    + p(1160, 430, 1262, 489, "#eef5fd", "Остальные<br>области<br>OSPF", "font-size:15px;line-height:1.15")
    + p(825, 492, 952, 518, "", "Область NSSA", AREA)
    + row(660, 530, 948, "b1", 662, 530, "Обычные <b>LSA-5</b><br>извне <b>не поступают</b><br>в область NSSA.", 738, 535)
    + row(958, 530, 1258, "b2", 960, 530, "<b>ABR</b> может преобразовать<br>подходящий LSA-7 в LSA-5<br>для обычных областей.", 1038, 535)
    + row(660, 608, 948, "b3", 662, 608, "Внутри области есть <b>ASBR</b>,<br>который объявляет локальные<br>внешние маршруты через LSA-7.", 738, 614)
    + row(958, 608, 1258, "b4", 960, 608, "Маршрут по умолчанию помогает<br>достигать направлений, сведений<br>о которых внутри области нет.", 1038, 614)
    + '</div>',
    # 3. Totally NSSA
    '<div class="step">' + head(1280, 1930, "#fffbe8", "#f6e27a", "#ffe14d", "3", "TOTALLY NSSA", 1360)
    + t(1298, 186, "Сочетает свойства totally stubby и NSSA:<br>скрыты межобластные маршруты, но сохраняются локальные внешние.")
    + img(N + "p3.png", "left:1284px;top:244px;width:644px")
    + p(1286, 268, 1392, 330, GR, "Внешняя сеть<br>(например,<br>(Интернет)", "font-size:13px;border-radius:24px")
    + p(1518, 264, 1630, 300, BL, "Внутренний<br>маршрутизатор", "font-size:13px")
    + p(1660, 250, 1846, 308, YL, "Подробные<br>межобластные маршруты<br>обычно скрыты", "font-size:13px")
    + p(1370, 334, 1508, 372, PK, "Локальные<br>внешние маршруты")
    + p(1442, 390, 1520, 458, PK, "<b style='color:#d63c7a;font-size:16px'>LSA-7</b><span style='font-size:11px;font-weight:400'>(локальные<br>внешние<br>маршруты)</span>")
    + p(1764, 318, 1858, 372, "#ffd6e4", "<b style='color:#d63c7a;font-size:16px'>LSA-5</b><span style='color:#d63c7a'>(не поступают<br>в область)</span>", "font-size:12px")
    + p(1680, 455, 1796, 512, BL, "Маршрут<br>по умолчанию<br>(0.0.0.0/0)", "font-size:13px")
    + p(1820, 432, 1922, 490, "#fffbe8", "Остальные<br>области<br>OSPF", "font-size:15px;line-height:1.15")
    + p(1438, 492, 1620, 518, "", "Область Totally NSSA", AREA)
    + row(1290, 532, 1628, "c1", 1293, 530, "Подробные межобластные маршруты<br><b>обычно скрыты</b>.", 1374, 545)
    + row(1636, 532, 1920, "c2", 1638, 530, "<b>LSA-5</b> из остальной<br>OSPF-сети не поступают.", 1718, 545)
    + row(1290, 606, 1628, "c3", 1293, 606, "Локальный <b>ASBR</b> сохраняет<br>объявления LSA-7.", 1374, 618)
    + row(1636, 606, 1920, "c4", 1638, 606, "Остальные направления<br>достигаются через маршрут<br>по умолчанию.", 1718, 612)
    + '</div>',
    # сравнение
    '<div class="step"><div class="tn-h" style="left:34px;top:712px;font-size:50px;transform:scaleX(.8);transform-origin:left">СРАВНЕНИЕ</div>'
    + '<div class="tn-cmp" style="left:232px;width:400px;background:#fde6ee"></div>' + img(N + "r1.png", "left:252px;top:722px")
    + t(412, 706, "<b>Totally Stubby</b>", "font:600 21px/1.2 Oswald,sans-serif")
    + t(358, 738, "<span class='tn-no'>✕</span>Без ASBR.<br><span class='tn-no'>✕</span>Без локальных внешних маршрутов<br>"
                  "<span style='margin-left:27px'>(нет LSA-7).</span>", "font-size:14px")
    + '<div class="tn-cmp" style="left:670px;width:375px;background:#e3effb"></div>' + img(N + "r2.png", "left:688px;top:722px")
    + t(875, 706, "<b>NSSA</b>", "font:600 21px/1.2 Oswald,sans-serif")
    + t(796, 738, "<span class='tn-ok'>✓</span>Есть ASBR.<br><span class='tn-ok'>✓</span>Локальные внешние маршруты<br>"
                  "<span style='margin-left:27px'>сохраняются как LSA-7.</span>", "font-size:14px")
    + '<div class="tn-cmp" style="left:1080px;width:405px;background:#fff6d2"></div>' + img(N + "r3.png", "left:1098px;top:722px")
    + t(1263, 706, "<b>Totally NSSA</b>", "font:600 21px/1.2 Oswald,sans-serif")
    + t(1206, 738, "<span class='tn-ok'>✓</span>Есть ASBR.<br><span class='tn-ok'>✓</span>Локальные внешние маршруты<br>"
                   "<span style='margin-left:27px'>сохраняются как LSA-7.</span>", "font-size:14px")
    + '</div>',
    '<div class="step"><div class="tn-cmp" style="left:1508px;width:422px;background:#fcd6e5;border-radius:40px"></div>'
    + img(N + "bulb.png", "left:1522px;top:704px")
    + t(1598, 708, "Недостающие направления —<br>через default route.", "font:600 25px/1.35 Oswald,sans-serif")
    + '</div>',
])
