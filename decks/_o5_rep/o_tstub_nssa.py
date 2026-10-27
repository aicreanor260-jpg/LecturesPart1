# -*- coding: utf-8 -*-
"""Типы областей OSPF — Totally Stubby, NSSA, Totally NSSA + сравнение. Схемы и иконки — SVG."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_ikit import puck, line, cross, svg, cloud_icon, g4_arr, g4_area, g4_icon, g4_glyph_at

W, H, TOP = 1942, 809, 118

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


def row(x0, y, x1, ico, tone, text, ty_off=5):
    return ('<div class="tn-row" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x0, y, x1 - x0)
            + g4_icon(ico, x0 + 6, y + 3, 60, tone)
            + '<div class="tn-rt" style="left:%dpx;top:%dpx">%s</div>' % (x0 + 78, y + ty_off, text))


def head(x0, x1, col, bd, nc, n, title, hx):
    return ('<div class="tn-pan" style="left:%dpx;width:%dpx;background:%s;border-color:%s"></div>' % (x0, x1 - x0, col, bd)
            + '<div class="tn-num" style="left:%dpx;background:%s;color:%s">%s</div>' % (x0 + 18, nc, "#fff" if n != "3" else "#1f1a33", n)
            + '<div class="tn-h" style="left:%dpx">%s</div>' % (hx, title))


PK, BL, YL, GR = "#ffc4d8", "#cfe4fa", "#ffe14d", "#e9e9ee"
AREA = "font:700 17px/1 'Golos Text',sans-serif;color:#d63c7a;background:#fbd3e3"
K, PKA, BLA, YA = "#2b2f3d", "#ff5c9e", "#2f8fe8", "#ffc400"


def links(pairs):
    return "".join(line(a, b, K, 2.6) for a, b in pairs)


def diag1():
    R = {"a": (112, 432), "b": (252, 380), "c": (274, 462), "abr": (418, 404), "o1": (546, 372), "o2": (586, 440)}
    o = [g4_area(30, 270, 440, 252, "p", 40),
         '<ellipse cx="560" cy="390" rx="78" ry="125" style="fill:#e3f0fd;fill-opacity:.9"/>',
         links([(R["a"], R["b"]), (R["a"], R["c"]), (R["b"], R["c"]), (R["c"], R["abr"]), (R["b"], R["abr"])]),
         g4_arr(450, 404, 520, 380, K, 3, both=True), g4_arr(450, 414, 556, 446, K, 3, both=True),
         line(R["o1"], R["o2"], K, 2.6)]
    o += [puck(x, y, 76, "b") for k, (x, y) in R.items() if k != "abr"]
    o += [puck(R["abr"][0], R["abr"][1], 84, "b", "ABR", 15),
          g4_arr(405, 484, 360, 484, YA, 7)]
    return svg("".join(o), W, H)


def diag_nssa(dx, total):
    """NSSA (dx=0) и Totally NSSA (dx≈625): облако, ASBR, внутренние, ABR, остальные области."""
    X = lambda x: x + dx  # noqa: E731
    asbr, rin, rmid, abr = (X(756), 432), (X(950), 326), (X(962), 428), (X(1082), 400)
    o = [g4_area(X(690), 262, 455 if not total else 470, 260, "p", 40),
         '<ellipse cx="%d" cy="395" rx="72" ry="118" style="fill:#e3f0fd;fill-opacity:.9"/>' % X(1210 if not total else 1240),
         cloud_icon(X(728), 300, 1.55, "#f1f1f4", "#4a4d5c"),
         line((X(730), 322), (X(745), 400), "#3a3f55", 3),
         links([(asbr, rmid), (rmid, abr), (rin, abr), (rin, (X(870), 380))]),
         g4_arr(X(992), 330, X(1040), 382, PKA, 5), g4_arr(X(895), 425, X(925), 425, PKA, 5),
         g4_arr(X(900), 380, X(930), 350, PKA, 5),
         g4_arr(X(1120), 398, X(1170), 395, K, 3, both=True),
         line((X(1080), 300), (X(1080), 370), "#1f3d8f", 3), g4_arr(X(1104), 300, X(1100), 370, YA, 4),
         g4_arr(X(1030), 482, X(975), 482, BLA, 7)]
    if total:
        o += [g4_arr(X(1150), 380, X(1115), 385, PKA, 4), cross(X(1123), 345, 14, "#e8245e", 6),
              puck(X(1230), 335, 72, "b"), puck(X(1220), 400, 72, "b"), line((X(1230), 345), (X(1220), 400), K, 2.6)]
    else:
        o += [g4_arr(X(1120), 375, X(1160), 360, PKA, 5), puck(X(1218), 392, 72, "b")]
    o += [puck(*asbr, 92, "p", "ASBR", 15), puck(*rin, 78, "b"), puck(*rmid, 78, "b"), puck(*abr, 88, "b", "ABR", 15)]
    return svg("".join(o), W, H)


def cmpp(x, tone):
    return svg(puck(x, 742, 96, tone), W, H)


HTML = CSS + bg("bg7", W, H) + "".join([
    # 1. Totally Stubby
    '<div class="step">' + head(15, 642, "#fff6f9", "#f6bdd2", "#ff5c9c", "1", "TOTALLY STUBBY", 95)
    + p(374, 140, 626, 204, "#fff0a8", "Расширение, распространённое<br>в реализации производителей;<br>не отдельный базовый тип RFC 2328.",
        "font:400 13px/1.3 'Golos Text',sans-serif;align-items:flex-start;text-align:left;padding-left:10px")
    + t(34, 202, "Внутри области <b>только внутренние маршруты</b>.<br>Внешний доступ — через маршрут по умолчанию.")
    + diag1()
    + p(52, 286, 212, 362, "#fff", "Внутренний<br>маршрутизатор<br>знает внутреннюю<br>топологию области.",
        "font-weight:500;align-items:flex-start;text-align:left;padding-left:8px;border:1.5px solid #ddd")
    + p(236, 286, 420, 338, "#fbc0d6", "Внутренние<br>маршруты (LSA-1, LSA-2)")
    + p(512, 280, 610, 338, "transparent", "Остальные<br>области<br>OSPF", "font-size:15px;line-height:1.15")
    + p(412, 456, 526, 512, "#ffe78a", "Маршрут<br>по умолчанию<br>(0.0.0.0/0)", "font-size:13px")
    + p(145, 492, 340, 518, "", "Область Totally Stubby", AREA)
    + row(42, 548, 618, "tri", "p", "<b>ABR</b> не передаёт подробные<br>межобластные и внешние маршруты,<br>а даёт маршрут по умолчанию.", 3)
    + row(42, 622, 618, "drum", "y", "<b>ASBR</b> внутри области <b style='background:#ffe94d'>не размещают</b>.", 22)
    + '</div>',
    # 2. NSSA
    '<div class="step">' + head(650, 1270, "#f3f9ff", "#9fcbf2", "#2f8fe8", "2", "NSSA", 732)
    + t(672, 186, "В области есть ASBR, который объявляет локальные<br>внешние маршруты. Обычные LSA-5 извне не поступают.")
    + diag_nssa(0, False)
    + p(676, 278, 784, 322, "transparent", "Внешняя сеть<br>(например,<br>(Интернет)", "font-size:13px")
    + p(893, 258, 1012, 294, BL, "Внутренний<br>маршрутизатор", "font-size:13px")
    + p(1050, 250, 1212, 300, YL, "Преобразование<br>подходящего LSA-7<br>в LSA-5", "font-size:13px")
    + p(778, 326, 890, 368, PK, "Локальные внешние<br>маршруты", "font-size:13px")
    + p(812, 386, 890, 456, PK, "<b style='color:#d63c7a;font-size:16px'>LSA-7</b><span style='font-size:11px;font-weight:400'>(локальные<br>внешние<br>маршруты)</span>")
    + p(1140, 312, 1262, 352, PK, "<b style='color:#d63c7a;font-size:16px'>LSA-5</b>(в другие области)", "font-size:12px")
    + p(1030, 455, 1146, 512, BL, "Маршрут<br>по умолчанию<br>(0.0.0.0/0)", "font-size:13px")
    + p(1160, 430, 1262, 489, "transparent", "Остальные<br>области<br>OSPF", "font-size:15px;line-height:1.15")
    + p(825, 492, 952, 518, "", "Область NSSA", AREA)
    + row(660, 530, 948, "box", "p", "Обычные <b>LSA-5</b><br>извне <b>не поступают</b><br>в область NSSA.", 3)
    + row(958, 530, 1258, "gear", "y", "<b>ABR</b> может преобразовать<br>подходящий LSA-7 в LSA-5<br>для обычных областей.", 3)
    + row(660, 608, 948, "db", "p", "Внутри области есть <b>ASBR</b>,<br>который объявляет локальные<br>внешние маршруты через LSA-7.", 3)
    + row(958, 608, 1258, "redo", "b", "Маршрут по умолчанию помогает<br>достигать направлений, сведений<br>о которых внутри области нет.", 3)
    + '</div>',
    # 3. Totally NSSA
    '<div class="step">' + head(1280, 1930, "#fffbe8", "#f6e27a", "#ffe14d", "3", "TOTALLY NSSA", 1360)
    + t(1298, 186, "Сочетает свойства totally stubby и NSSA:<br>скрыты межобластные маршруты, но сохраняются локальные внешние.")
    + diag_nssa(625, True)
    + p(1301, 278, 1409, 322, "transparent", "Внешняя сеть<br>(например,<br>(Интернет)", "font-size:13px")
    + p(1518, 258, 1637, 294, BL, "Внутренний<br>маршрутизатор", "font-size:13px")
    + p(1662, 250, 1840, 300, YL, "Подробные<br>межобластные маршруты<br>обычно скрыты", "font-size:13px")
    + p(1403, 326, 1515, 368, PK, "Локальные<br>внешние маршруты", "font-size:13px")
    + p(1437, 386, 1515, 456, PK, "<b style='color:#d63c7a;font-size:16px'>LSA-7</b><span style='font-size:11px;font-weight:400'>(локальные<br>внешние<br>маршруты)</span>")
    + p(1756, 306, 1850, 360, "#ffd6e4", "<b style='color:#d63c7a;font-size:16px'>LSA-5</b><span style='color:#d63c7a'>(не поступают<br>в область)</span>", "font-size:12px")
    + p(1655, 455, 1771, 512, BL, "Маршрут<br>по умолчанию<br>(0.0.0.0/0)", "font-size:13px")
    + p(1818, 432, 1920, 490, "transparent", "Остальные<br>области<br>OSPF", "font-size:15px;line-height:1.15")
    + p(1438, 492, 1620, 518, "", "Область Totally NSSA", AREA)
    + row(1290, 532, 1628, "eyeoff", "p", "Подробные межобластные маршруты<br><b>обычно скрыты</b>.", 13)
    + row(1636, 532, 1920, "ban", "p", "<b>LSA-5</b> из остальной<br>OSPF-сети не поступают.", 13)
    + row(1290, 606, 1628, "gear", "y", "Локальный <b>ASBR</b> сохраняет<br>объявления LSA-7.", 13)
    + row(1636, 606, 1920, "redo", "b", "Остальные направления<br>достигаются через маршрут<br>по умолчанию.", 3)
    + '</div>',
    # сравнение
    '<div class="step"><div class="tn-h" style="left:34px;top:712px;font-size:50px;transform:scaleX(.8);transform-origin:left">СРАВНЕНИЕ</div>'
    + '<div class="tn-cmp" style="left:232px;width:400px;background:#fde6ee"></div>' + cmpp(302, "p")
    + t(412, 706, "<b>Totally Stubby</b>", "font:600 21px/1.2 Oswald,sans-serif")
    + t(358, 738, "<span class='tn-no'>✕</span>Без ASBR.<br><span class='tn-no'>✕</span>Без локальных внешних маршрутов<br>"
                  "<span style='margin-left:27px'>(нет LSA-7).</span>", "font-size:14px")
    + '<div class="tn-cmp" style="left:670px;width:375px;background:#e3effb"></div>' + cmpp(738, "b")
    + t(875, 706, "<b>NSSA</b>", "font:600 21px/1.2 Oswald,sans-serif")
    + t(796, 738, "<span class='tn-ok'>✓</span>Есть ASBR.<br><span class='tn-ok'>✓</span>Локальные внешние маршруты<br>"
                  "<span style='margin-left:27px'>сохраняются как LSA-7.</span>", "font-size:14px")
    + '<div class="tn-cmp" style="left:1080px;width:405px;background:#fff6d2"></div>' + cmpp(1148, "b")
    + t(1263, 706, "<b>Totally NSSA</b>", "font:600 21px/1.2 Oswald,sans-serif")
    + t(1206, 738, "<span class='tn-ok'>✓</span>Есть ASBR.<br><span class='tn-ok'>✓</span>Локальные внешние маршруты<br>"
                   "<span style='margin-left:27px'>сохраняются как LSA-7.</span>", "font-size:14px")
    + '</div>',
    '<div class="step"><div class="tn-cmp" style="left:1508px;width:422px;background:#fcd6e5;border-radius:40px"></div>'
    + svg(g4_glyph_at("bulb", 1556, 750, 62, "#1f1a33", 1.8).replace('fill="none"', 'fill="#ffd23a"', 1), W, H)
    + t(1598, 708, "Недостающие направления —<br>через default route.", "font:600 25px/1.35 Oswald,sans-serif")
    + '</div>',
])
