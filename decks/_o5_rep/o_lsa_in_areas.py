# -*- coding: utf-8 -*-
"""Какие LSA передаются в областях OSPF: карточки LSA + схема Area 0 / Area 1 / Area 2 / NSSA."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_g5kit import svg, rtr, puck, path, blob, cloud_icon, server, laptop, wifi, ico, sico, FADE

W, H, TOP = 1672, 941, 0
N = "o_lsa_in_areas_"

CSS = """<style>
.la-c{position:absolute;top:8px;width:192px;height:236px;border-radius:16px;border:2px solid rgba(255,255,255,.9)}
.la-ct{position:absolute;font:700 28px/1 "Golos Text",sans-serif;color:#1f1a33}
.la-cs{position:absolute;font:700 15px/1.1 "Golos Text",sans-serif;color:#1f1a33;width:180px}
.la-cd{position:absolute;font:400 10.3px/1.42 "Golos Text",sans-serif;color:#2a2440;width:116px}
.la-cy{position:absolute;width:176px;height:68px;background:#ffe24d;border-radius:14px;font:700 12.5px/1.28 "Golos Text",sans-serif;
 color:#1f1a33;display:flex;align-items:center;padding:0 14px}
.la-p{position:absolute;border-radius:14px;text-align:center;color:#1f1a33;font:500 14px/1.2 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.la-p b{font-weight:800;font-size:18px;line-height:1.1}
.la-box{position:absolute;background:rgba(255,255,255,.95);border:2px solid #ebe6f2;border-radius:14px}
.la-bh{position:absolute;font:800 18px/1.15 "Golos Text",sans-serif;color:#1f1a33}
.la-bt{position:absolute;font:400 14px/1.32 "Golos Text",sans-serif;color:#1f1a33}
.la-lg{position:absolute;font:400 10px/18.3px "Golos Text",sans-serif;color:#1f1a33}
</style>"""

CARDS = [  # x, фон, заголовок, подпись, описание, жёлтая плашка
    (442, "#ffd3e3", "LSA-1", "Связи маршрутизатора", "Содержит данные о линках, интерфейсах и стоимости.",
     "Распространяется только внутри своей области."),
    (643, "#cfe6fb", "LSA-2", "Общая сеть и DR", "Описывает мультидоступные сети и выбор DR.",
     "Распространяется только внутри своей области."),
    (843, "#fff1b0", "LSA-3", "Сеть в другой области", "ABR объявляет сети, доступные в других областях.",
     "Распространяется между областями (но не дальше ASBR)."),
    (1044, "#e3d2fa", "LSA-4", "Путь к ASBR", "ABR сообщает межобластной путь к ASBR (его RID).",
     "Распространяется между областями (до ASBR)."),
    (1244, "#cfe6fb", "LSA-5", "Внешний маршрут",
     "Создаётся ASBR для внешних сетей. ABR распространяет это же объявление в другие стандартные области.",
     "Распространяется между областями."),
    (1450, "#ffd3e3", "LSA-7", "Внешний маршрут<br>в NSSA", "Создаётся ASBR в NSSA для внешних сетей.",
     "Распространяется только внутри NSSA. На ABR может быть преобразован в LSA-5."),
]


GM = ("-webkit-mask:linear-gradient(270deg,transparent,#000 38%),linear-gradient(180deg,transparent,#000 12%);"
      "-webkit-mask-composite:source-in;mask:linear-gradient(270deg,transparent,#000 38%),linear-gradient(180deg,transparent,#000 12%);"
      "mask-composite:intersect")
K, BL, YL, VI, PK = "#3a3f55", "#3f9be8", "#ffc21a", "#a463f0", "#ff4f9a"


def scene():
    o = [blob(470, 420, 175, 125, "p", seed=1), blob(935, 390, 265, 150, "b", seed=2), blob(1445, 415, 205, 125, "p", seed=3),
         blob(880, 770, 340, 150, "y", seed=4), cloud_icon(515, 672, 1.9, "#fff", "#5aa9ee"), cloud_icon(728, 850, 1.85, "#fff", "#5aa9ee"),
         wifi(165, 360, 1.1), wifi(770, 765, 1.1)]
    o += [path("M330 420 L400 450 M415 460 L555 520 M415 460 V520 H700 M700 440 L870 470 M990 470 L1160 440 M1160 440 L1475 460 "
               "M1475 460 L1590 440 M555 520 L700 445 M935 640 V500 M880 800 L935 650", BL, 4)]
    o += [laptop(330, 425, 80, "b"), laptop(1600, 440, 80, "b"), server(840, 430, 46, 76), server(898, 418, 50, 88), server(960, 430, 46, 76)]
    o += [rtr(415, 440, 110, "p"), rtr(555, 505, 100, "b"), rtr(700, 418, 120, "b"), rtr(1160, 418, 120, "b"), rtr(1478, 445, 110, "p"),
          rtr(937, 615, 110, "b"), rtr(880, 790, 125, "p")]
    return svg("".join(o))


ARR1 = svg(path("M440 400 A22 22 0 0 1 440 360", PK, 4, mk="ap") + path("M625 362 A24 24 0 0 1 625 400", PK, 4, mk="ap")
           + path("M1278 395 A24 24 0 0 1 1278 362", PK, 4, mk="ap") + path("M1455 362 A24 24 0 0 1 1455 400", PK, 4, mk="ap"))
ARR2 = svg(path("M840 352 Q790 360 760 388", YL, 7, mk="ay") + path("M1025 352 Q1075 360 1105 388", YL, 7, mk="ay")
           + path("M855 408 Q810 405 768 418", VI, 7, mk="av") + path("M1010 408 Q1060 405 1095 418", VI, 7, mk="av")
           + path("M893 540 V520", YL, 7, mk="ay") + path("M968 540 V520", VI, 7, mk="av"))
ARR3 = svg(path("M505 640 Q495 580 530 545", BL, 6, mk="ab"))
ARR4 = svg(path("M1015 720 Q1012 640 1025 605", BL, 7, mk="ab") + path("M937 770 V700", PK, 6, mk="ap") + path("M985 765 L955 765", PK, 6, mk="ap"))
LEGI = svg(puck(1395, 812, 40, "p") + rtr(1395, 858, 40, "b") + rtr(1395, 900, 40, "p"))


def card(i, c):
    x, col, t, s, d, y = c
    big = i == 5
    return ('<div class="step"><div class="la-c" style="left:%dpx;background:%s"></div>' % (x, col)
            + '<div class="la-ct" style="left:%dpx;top:22px">%s</div>' % (x + 14, t)
            + '<div class="la-cs" style="left:%dpx;top:%dpx">%s</div>' % (x + 14, 50 if big else 54, s)
            + ico(["game", "fork", "pin", "list", "globe", "doc"][i], x + 10, 92, 56, "#ffffffcc", "#1f1a33", 2.2)
            + '<div class="la-cd" style="left:%dpx;top:96px">%s</div>' % (x + 76, d)
            + '<div class="la-cy" style="left:%dpx;top:%dpx">%s</div></div>' % (x + 8, 164 if big else 166, y))


def p(x0, y0, x1, y1, col, html, extra=""):
    return '<div class="la-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        x0, y0, x1 - x0, y1 - y0, col, extra, html)


LEG = ["#ff4f9a", "#ff4f9a", "#ffc21a", "#a463f0", "#2f8fe8", "#ff4f9a"]
LEGT = ["LSA-1 (внутри области)", "LSA-2 (внутри области)", "LSA-3 (между областями)", "LSA-4 (между областями)",
        "LSA-5 (между областями)", "LSA-7 (только в NSSA)"]

HTML = CSS + bg("bg4", W, H) + "".join([
    '<div class="step">' + img(N + "girl.png", "left:0;top:360px;width:400px;" + GM) + scene()
    + p(40, 246, 420, 298, "rgba(255,255,255,.96)", "Типы LSA и их распространение<br>между областями",
        "font:500 22px/1.15 'Golos Text',sans-serif;align-items:flex-start;text-align:left;padding-left:6px")
    + p(375, 293, 552, 347, "#ffc7dc", "<b style='font-size:26px'>Area 1</b>(обычная область)", "font-size:17px;border-radius:24px")
    + p(1385, 286, 1560, 341, "#ffc7dc", "<b style='font-size:26px'>Area 2</b>(обычная область)", "font-size:17px;border-radius:24px")
    + p(830, 255, 1035, 312, "#d6e9fb", "<b style='font-size:32px;color:#2167c4'>Area 0</b>(магистральная область)", "font-size:16px;font-weight:700")
    + p(372, 484, 472, 521, "#fbe0ec", "<b>R1</b>(внутренний)")
    + p(1428, 490, 1540, 529, "#fbe0ec", "<b>R2</b>(внутренний)")
    + p(652, 466, 752, 504, "#d9ebfb", "<b>ABR-1</b>(Area 1 ↔ 0)")
    + p(1110, 467, 1212, 505, "#d9ebfb", "<b>ABR-2</b>(Area 2 ↔ 0)")
    + p(884, 671, 994, 709, "#d9ebfb", "<b>ABR-3</b>(Area 0 ↔ NSSA)", "font-size:13px")
    + p(946, 808, 1060, 853, "#fff1b8", "<b style='font-size:19px'>ASBR-NSSA</b>(в NSSA)", "align-items:flex-start;font-size:16px")
    + p(666, 656, 872, 713, "#fff1b8", "<b style='font-size:26px'>NSSA</b>(не совсем обычная область)", "font-weight:700;font-size:14px")
    + p(434, 643, 596, 692, "#fff", "<b style='font-size:15px'>Внешняя сеть</b>(например, Интернет)")
    + p(656, 822, 800, 866, "#fff", "<b style='font-size:15px'>Внешняя сеть</b>(например, филиал)")
    + p(368, 724, 516, 828, "#fff", "Разные<br>типы LSA —<br>разные области<br>и правила<br>распространения",
        "font-size:15px;align-items:flex-start;text-align:left;transform:rotate(-4deg)")
    + '</div>',
    "".join(card(i, c) for i, c in enumerate(CARDS)),
    '<div class="step">' + ARR1
    + p(458, 358, 610, 409, "#ff5c9c", "<b style='color:#fff'>LSA-1, LSA-2</b><span style='color:#fff'>только в Area 1</span>")
    + p(1292, 355, 1440, 406, "#ff5c9c", "<b style='color:#fff'>LSA-1, LSA-2</b><span style='color:#fff'>только в Area 2</span>")
    + '</div>',
    '<div class="step">' + ARR2
    + p(836, 322, 1028, 370, "#ffd84d", "<b>LSA-3</b>сети из других областей")
    + p(854, 385, 1010, 428, "#d4b2f8", "<b>LSA-4</b>путь к ASBR")
    + p(785, 541, 928, 582, "#ffd84d", "<b>LSA-3</b>сети из других областей", "font-size:12px")
    + p(956, 541, 1072, 588, "#c79cf5", "<b>LSA-4</b>путь к ASBR")
    + '</div>',
    '<div class="step">' + ARR3
    + p(527, 543, 722, 613, "#c3e1fa", "<b>LSA-5</b>внешний маршрут<br>(создаёт ASBR-1)")
    + '</div>',
    '<div class="step">' + ARR4
    + p(990, 722, 1162, 796, "#ffc4da", "<b>LSA-7</b>внешний маршрут<br>(создаёт ASBR-NSSA)", "align-items:flex-start;text-align:left;padding-left:12px")
    + p(1032, 608, 1200, 681, "#c3e1fa", "<b style='font-size:16px;color:#2167c4'>Преобразование<br>LSA-7 → LSA-5</b><span style='color:#2167c4'>на ABR-3</span>",
        "align-items:flex-start;text-align:left;padding-left:18px")
    + '</div>',
    '<div class="step"><div class="la-box" style="left:1245px;top:540px;width:408px;height:108px"></div>'
    + svg('<path d="M1281 551 l18 32 h-36 z" style="fill:#ffd6e5" stroke="#e8245e" stroke-width="3" stroke-linejoin="round"/><path d="M1281 562 v10" stroke="#e8245e" stroke-width="3.5" stroke-linecap="round"/><circle cx="1281" cy="577" r="2" fill="#e8245e"/>')
    + '<div class="la-bh" style="left:1314px;top:548px">LSA-4 — не маршрут по умолчанию</div>'
    + '<div class="la-bt" style="left:1314px;top:572px">LSA-4 сообщает только путь к ASBR (его Router ID).<br>Маршрут по умолчанию обычно объявляется<br>'
      'через LSA-3. В NSSA способ объявления default<br>зависит от настройки: LSA-3 или LSA-7.</div>'
    + '<div class="la-box" style="left:1245px;top:655px;width:408px;height:115px"></div>'
    + ico("gear", 1258, 665, 42, "#cfe6fb", "#1f1a33", 2.4)
    + '<div class="la-bh" style="left:1314px;top:664px">NSSA и Totally NSSA сохраняют<br>собственные внешние маршруты</div>'
    + '<div class="la-bt" style="left:1314px;top:709px">ASBR в NSSA объявляет их через LSA-7.<br>Default нужен для сетей, о которых область<br>не получает подробных сведений.</div>'
    + '</div>',
    '<div class="step"><div class="la-box" style="left:1190px;top:785px;width:465px;height:146px;border-style:dashed"></div>'
    + '<div class="la-bt" style="left:1204px;top:792px;font-size:11px;font-weight:700">Условные обозначения</div>'
    + '<svg class="ab" style="left:1200px;top:808px" width="36" height="110">'
    + "".join('<path d="M2 %d H22" stroke="%s" stroke-width="3.5" marker-end="url(#laar%d)"/>'
              '<defs><marker id="laar%d" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0 0L6 3L0 6z" fill="%s"/></marker></defs>'
              % (8 + k * 18.3, c, k, k, c) for k, c in enumerate(LEG)) + '</svg>'
    + '<div class="la-lg" style="left:1236px;top:807px">' + "<br>".join(LEGT) + '</div>'
    + LEGI
    + '<div class="la-lg" style="left:1428px;top:801px;line-height:1.15"><b>Маршрутизатор</b><br>(обычный)</div>'
    + '<div class="la-lg" style="left:1428px;top:842px;line-height:1.15"><b>ABR</b><br>(пограничный<br>маршрутизатор областей)</div>'
    + '<div class="la-lg" style="left:1428px;top:884px;line-height:1.15"><b>ASBR</b><br>(маршрутизатор<br>внешних сетей)</div>'
    + '</div>',
])
