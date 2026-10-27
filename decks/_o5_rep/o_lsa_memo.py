# -*- coding: utf-8 -*-
"""Типы записей OSPF — короткая памятка (LSA-1..11)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_g5kit import svg, drum, path, line, blob, cloud_icon, doccard, sico, stx, FADE

W, H, TOP = 1536, 1024, 118
N = "o_lsa_memo_"

CSS = """<style>
.lm-t{position:absolute;color:#1f1a33;font:500 17px/1.3 "Golos Text",sans-serif}
.lm-card{position:absolute;background:rgba(255,255,255,.9);border:2px solid #e9e4f1;border-radius:16px}
.lm-chip{position:absolute;background:#ff5c9c;color:#fff;font:700 21px/34px "Golos Text",sans-serif;padding:0 16px;border-radius:17px}
.lm-chipb{background:#5aa9ee}
.lm-ty{position:absolute;background:#ffe94d;color:#1f1a33;font:700 17px/30px "Golos Text",sans-serif;padding:0 10px;border-radius:12px}
.lm-h{position:absolute;color:#1f1a33;font:800 22px/1.15 "Golos Text",sans-serif;z-index:2}
.lm-box{position:absolute;background:#e3eefb;border-radius:14px;color:#1f1a33;font:500 16px/1.32 "Golos Text",sans-serif;padding:12px 14px}
.lm-band{position:absolute;height:40px;border-radius:20px;font:500 16px/40px "Golos Text",sans-serif;color:#1f1a33;background:#e7f0fb;padding-left:14px;white-space:nowrap}
.lm-band b{display:inline-block;height:40px;padding:0 22px;border-radius:20px;font:700 30px/40px Oswald,sans-serif;color:#1f1a33;margin:0 14px 0 -14px;letter-spacing:.02em}
.lm-note{position:absolute;left:1318px;top:16px;width:178px;height:86px;background:#ffe94d;transform:rotate(-5deg);border-radius:6px;
 font:700 17px/1.25 "Golos Text",sans-serif;color:#1f1a33;padding:10px 14px;box-shadow:3px 3px 0 rgba(0,0,0,.08)}
.lm-ys{position:absolute;left:1292px;top:640px;width:236px;height:352px;background:#fff16a;border-radius:18px}
.lm-yw{position:absolute;background:#fff;border-radius:14px}
</style>"""


def card(x, y, w, h):
    return '<div class="lm-card" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>' % (x, y, w, h)


def chip(x, y, t, blue=False):
    return '<div class="lm-chip%s" style="left:%dpx;top:%dpx">%s</div>' % (" lm-chipb" if blue else "", x, y, t)


def ty(x, y, t):
    return '<div class="lm-ty" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


def h(x, y, t, fs=22):
    return '<div class="lm-h" style="left:%dpx;top:%dpx;font-size:%dpx">%s</div>' % (x, y, fs, t)


def box(x, y, w, hh, t, fs=16):
    return '<div class="lm-box" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;font-size:%dpx">%s</div>' % (x, y, w, hh, fs, t)


def top_card(i, x, title, pic, text):
    return ('<div class="step">' + card(x, 238, 290, 374) + chip(x + 14, 248, "LSA-%d" % i) + ty(x + 206, 251, "Type %d" % i)
            + h(x + 18, 288, title) + S(DIA[pic]) + box(x + 12, 502, 266, 102, text, 15) + '</div>')


def S(b):
    return svg(b, 1536, 1024)


K = "#2b2f3d"


def dr(x, y, t="b", w=62, lab=None, fs=None):
    return drum(x, y, w, t, lab, fs)


def ext(x, y, s=1.0, t="Внешняя|сеть"):
    a, b = t.split("|")
    return cloud_icon(x, y + 12 * s, s, "#fff", "#5aa9ee") + stx(x, y - 6 * s, a, 13 * s, "#1f1a33", 800) + stx(x, y + 10 * s, b, 13 * s, "#1f1a33", 800)


DIA = {
    "d1.png": ('<ellipse cx="170" cy="420" rx="130" ry="60" style="fill:#e3f0fd"/>'
               + "".join(line((170, 420), p, K, 3) for p in ((75, 385), (262, 368), (75, 470), (265, 466)))
               + dr(75, 378) + dr(262, 360) + dr(75, 462) + dr(265, 458) + dr(170, 400, "p", 96, "R1", 18)),
    "d2.png": ('<ellipse cx="470" cy="420" rx="130" ry="60" style="fill:#fde3ee"/>'
               + "".join(line((470, 455), p, K, 3) for p in ((370, 410), (565, 410), (390, 480), (550, 480)))
               + '<path d="M445 455 l50 0 l10 26 h-70 z" fill="#cfd4dd" stroke="#7b8396" stroke-width="2"/>'
               + dr(370, 400) + dr(565, 400) + dr(392, 470, "b", 54) + dr(550, 475, "b", 54)
               + dr(470, 390, "p", 70, "DR", 15) + '<path d="M455 366 l5 -16 l10 10 l10 -10 l5 16 z" fill="#ffd23a" stroke="#c99a00" stroke-width="1.5"/>'),
    "d3.png": ('<ellipse cx="690" cy="425" rx="62" ry="68" style="fill:#cfe6fb"/><ellipse cx="848" cy="425" rx="62" ry="68" style="fill:#fff1b0"/>'
               + stx(688, 375, "Область", 13) + stx(688, 391, "Area 1", 13) + stx(850, 375, "Область", 13) + stx(850, 391, "Area 2", 13)
               + line((668, 432), (870, 432), K, 3) + dr(668, 420) + dr(870, 420) + dr(768, 420, "p", 66) + stx(768, 400, "ABR", 16, "#1f1a33", 800)),
    "d4.png": ('<ellipse cx="975" cy="425" rx="50" ry="75" style="fill:#cfe6fb"/>' + line((972, 392), (1018, 425), K, 3) + line((972, 468), (1018, 425), K, 3)
               + dr(972, 382) + dr(972, 460) + dr(1018, 420, "p", 66) + stx(1022, 404, "ABR", 16, "#1f1a33", 800)
               + path("M1058 428 H1112", "#ff5c9e", 4, "8 5", "ap") + path("M1058 444 H1112", "#3b9eff", 4, "8 5", "ab")
               + line((1158, 395), (1158, 420), K, 3) + dr(1158, 420, "p", 70) + stx(1158, 484, "ASBR", 16, "#1f1a33", 800) + ext(1160, 358, 1.1)),
    "d5.png": (line((1290, 462), (1378, 430), K, 3) + dr(1290, 455) + dr(1378, 422, "p", 72) + stx(1378, 486, "ASBR", 16, "#1f1a33", 800)
               + path("M1430 405 Q1440 420 1418 432", "#ff5c9e", 3.5, mk="ap") + path("M1385 410 Q1390 392 1405 385", K, 3) + ext(1442, 380, 1.05)),
    "d6.png": (line((80, 820), (205, 848), K, 3) + path("M95 833 L178 850", "#3b9eff", 3.5, "8 5", "ab") + path("M110 808 L160 795", "#ff5c9e", 3.5, mk="ap")
               + dr(80, 810, "p", 66) + dr(102, 860, "b", 56) + dr(208, 848, "b", 60)
               + cloud_icon(210, 800, 1.05, "#fff", "#5aa9ee") + sico("people", 192, 774, 34, "#ff5c9e", 2.4)),
    "d7.png": (path("M365 822 L425 810", "#ff5c9e", 3.5, mk="ap") + path("M360 845 L415 860", "#3b9eff", 3.5, "8 5", "ab")
               + dr(332, 818, "p", 64) + stx(334, 872, "ASBR", 14, "#1f1a33", 800) + stx(334, 888, "(NSSA)", 14, "#1f1a33", 800)
               + dr(448, 852, "b", 60) + ext(462, 806, 1.05)),
    "d8.png": (line((590, 838), (700, 838), K, 3) + dr(590, 828, "b", 60) + dr(700, 828, "b", 60) + doccard(564, 770, 34, "p")
               + '<rect x="604" y="770" width="124" height="48" rx="8" fill="#fff" stroke="#e3dbe8" stroke-width="1.5"/>'
               + stx(614, 789, "Link-local: fe80::1", 12.5, "#1f1a33", 500, "start") + stx(614, 808, "Link-local: fe80::2", 12.5, "#1f1a33", 500, "start")),
    "d9.png": ('<rect x="762" y="768" width="168" height="40" rx="10" style="fill:#fde3ee"/>' + doccard(768, 772, 30, "p")
               + stx(810, 795, "2001:db8:1::/64", 13, "#1f1a33", 600, "start") + dr(850, 828, "b", 76)),
    "d10.png": ('<ellipse cx="1040" cy="845" rx="62" ry="28" style="fill:#e3f0fd"/>' + dr(1035, 830, "b", 96)
                + '<rect x="1046" y="770" width="46" height="52" rx="8" style="fill:#ffd6e5"/>' + doccard(1052, 774, 34, "p")),
}


pic_pos = {"d1.png": (30, 335, 275), "d2.png": (330, 335, 275), "d3.png": (630, 340, 280),
           "d4.png": (930, 318, 282), "d5.png": (1230, 330, 280)}

HTML = CSS + bg("bg5", W, H) + "".join([
    img(N + "cat.png", "left:1385px;top:100px;width:151px;" + FADE),
    '<div class="lm-note">Разные типы LSA для разных задач в сети ♡</div>',
    '<div class="lm-t" style="left:60px;top:122px;font-size:18px">LSA (Link-State Advertisement) — типы записей, которые OSPF использует для обмена информацией<br>'
    'о топологии и маршрутах между <u>маршрутизаторами.</u></div>',
    '<div class="step"><div class="lm-band" style="left:30px;top:188px;width:1030px"><b style="background:#ff7fb0;font-size:32px">ОСНОВНЫЕ LSA</b>'
    'Определяют топологию области, межобластные маршруты и внешние маршруты.</div></div>',
    top_card(1, 22, "Мои соединения<br>в области", "d1.png",
             "Описание всех собственных интерфейсов маршрутизатора в данной области (соседи, сети, метрики)."),
    top_card(2, 322, "Маршрутизаторы<br>общей сети и её DR", "d2.png",
             "Информация о маршрутизаторах, подключённых к многодоступной сети, и о том, какой из них является DR."),
    top_card(3, 625, "Сеть доступна<br>в другой области", "d3.png",
             "Анонс сети из одной области в другие области.<br>Генерируется ABR<br>(Area Border Router)."),
    top_card(4, 925, "Путь к ASBR", "d4.png",
             "Информация о том, как достичь ASBR в другой области.<br>Генерируется ABR."),
    top_card(5, 1225, "Внешний маршрут,<br>введённый в OSPF", "d5.png",
             "Описание внешних сетей, введённых в OSPF (например, из других протоколов — BGP, статических маршрутов и т. п.). Генерируется ASBR."),
    # специальные
    '<div class="step">' + card(16, 632, 512, 370)
    + '<div class="lm-band" style="left:26px;top:640px;width:490px;background:#e7f0fb"><b style="background:#8cc4f2">СПЕЦИАЛЬНЫЕ</b>Используются в особых сценариях.</div>'
    + card(26, 688, 238, 304) + chip(36, 694, "LSA-6") + ty(184, 696, "Type 6") + h(40, 727, "MOSPF: multicast", 20)
    + S(DIA["d6.png"])
    + box(32, 900, 226, 86, "Используется MOSPF для распространения информации о мультикаст-группах и членстве в них.", 13.5)
    + card(272, 688, 248, 304) + chip(284, 694, "LSA-7") + ty(436, 696, "Type 7") + h(296, 727, "Внешний маршрут<br>внутри NSSA", 20)
    + S(DIA["d7.png"])
    + box(278, 900, 236, 86, "Описание внешних сетей, введённых в область типа NSSA. Позже может быть преобразован в LSA-5 на границе области.", 13.5)
    + '</div>',
    # OSPFv3
    '<div class="step">' + card(537, 632, 408, 370)
    + '<div class="lm-band" style="left:546px;top:640px;width:390px"><b style="background:#8cc4f2">OSPFv3</b>Специфичные для OSPFv3 типы.</div>'
    + card(546, 688, 196, 304) + chip(558, 692, "Type 8") + h(562, 727, "Link-LSA", 20)
    + S(DIA["d8.png"])
    + box(540, 872, 202, 116, "Сведения о канале и link-local адресах (интерфейсы, параметры канала) для каждого отдельного канала. Действует только на данном канале.", 11.8)
    + card(750, 688, 188, 304) + chip(762, 692, "Type 9") + h(764, 727, "Intra-Area-Prefix", 20)
    + S(DIA["d9.png"])
    + box(756, 872, 180, 116, "Реклама IPv6-префиксов внутри области. Отделён от Link-LSA (Type 8) и содержит адресные префиксы сетей данного маршрутизатора.", 11.8)
    + '</div>',
    # OSPFv2
    '<div class="step">' + card(954, 632, 330, 370)
    + '<div class="lm-band" style="left:962px;top:640px;width:316px;font-size:13px"><b style="background:#8cc4f2">OSPFv2</b>Дополнительная информация.</div>'
    + card(964, 688, 312, 304) + chip(974, 692, "Types 9–11") + h(980, 725, "Opaque LSA", 21)
    + S(DIA["d10.png"])
    + '<div class="lm-yw" style="left:1108px;top:744px;width:166px;height:116px;border:1px solid #e6e6ee"></div>'
    + '<div class="lm-t" style="left:1116px;top:752px;font-size:11.5px;line-height:1.3"><span style="color:#ff5c9c">●</span> <b>Type 9</b> — Link-local scope<br>&nbsp;&nbsp;&nbsp;(на уровне канала)<br>'
      '<span style="color:#ff5c9c">●</span> <b>Type 10</b> — Area scope<br>&nbsp;&nbsp;&nbsp;(в пределах области)<br>'
      '<span style="color:#ff5c9c">●</span> <b>Type 11</b> — AS scope<br>&nbsp;&nbsp;&nbsp;(вся OSPF-система)</div>'
    + box(972, 880, 300, 106, "Используются для передачи дополнительной информации. Область распространения зависит от номера типа — от канала до всей OSPF-системы.", 15.5)
    + '</div>',
    # жёлтый блок
    '<div class="step"><div class="lm-ys"></div>'
    + '<div class="lm-t" style="left:1306px;top:650px;width:40px;height:40px;border-radius:20px;background:#ff5c9c;color:#fff;font:800 28px/40px Golos Text,sans-serif;text-align:center">!</div>'
    + h(1354, 646, "Type 9 зависит<br>от версии:", 21)
    + '<div class="lm-yw" style="left:1302px;top:708px;width:204px;height:110px"></div>' + chip(1314, 720, "OSPFv2", True)
    + h(1316, 758, "Type 9 —<br>Opaque LSA", 19) + S(sico("list", 1446, 738, 46, "#1f1a33", 2.2))
    + '<div class="lm-yw" style="left:1302px;top:832px;width:204px;height:134px"></div>' + chip(1314, 844, "OSPFv3", True)
    + h(1316, 882, "Type 9 —<br>Intra-Area-Prefix<br>LSA", 19) + S(sico("list", 1446, 852, 46, "#1f1a33", 2.2))
    + '</div>',
])
