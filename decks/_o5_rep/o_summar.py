# -*- coding: utf-8 -*-
"""Суммирование и типы маршрутов OSPF: 10.1.0.0/22 через ABR, 172.16.0.0/14 через ASBR, коды O/O IA/O E1/O E2.
Схема, иконки и терминал — HTML+SVG, вырезок нет."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_ikit import puck, line, svg, cloud_icon, g4_arr, g4_area, g4_icon, g4_tower, g4_glyph_at

W, H, TOP = 1536, 1024, 124

CSS = """<style>
.sm-p{position:absolute;border-radius:12px;text-align:center;color:#1f1a33;font:600 19px/1.2 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.sm-m{font:500 16px/1 "JetBrains Mono",monospace!important}
.sm-h{position:absolute;left:42px;top:512px;font:700 64px/1 Oswald,sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.74);transform-origin:left}
.sm-row{position:absolute;left:32px;width:660px;height:72px;background:rgba(255,255,255,.95);border:1.5px solid #ece7f1;border-radius:16px}
.sm-code{position:absolute;left:136px;width:128px;height:56px;border-radius:28px;font:700 32px/56px Oswald,sans-serif;text-align:center;color:#1f1a33}
.sm-t{position:absolute;left:288px;font:400 19px/1.3 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.sm-term{position:absolute;left:722px;top:592px;width:790px;height:318px;background:#141a33;border-radius:12px;border:3px solid #3b4870;
 font:400 19px/58px "JetBrains Mono",monospace;color:#d8e2ff;padding:8px 22px;white-space:pre;box-shadow:8px 8px 0 rgba(47,143,232,.18)}
.sm-term b{font-family:Oswald,sans-serif;font-size:26px;font-weight:600}
.sm-f{position:absolute;top:928px;height:62px;border-radius:20px;font:400 19px/62px "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.sm-f b{font-size:22px}
</style>"""


def p(x0, y0, x1, y1, col, html, extra="", cls=""):
    return '<div class="sm-p %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        cls, x0, y0, x1 - x0, y1 - y0, col, extra, html)


PFX = "#fde6ef"
PK, BL, YE = "#ff5c9e", "#2f8fe8", "#ffc400"


def desk(x, y):
    """Рабочее место: стол, сервер, ноутбук (левый верх x, y)."""
    return ('<path d="M%d %d l90 0 l30 22 l-90 0 z" style="fill:#e9ecf2" stroke="#9aa3b2" stroke-width="2"/>' % (x, y + 52, )
            + g4_tower(x + 10, y + 8, 30, 52)
            + '<rect x="%d" y="%d" width="40" height="28" rx="4" style="fill:#3a3f55"/>'
              '<rect x="%d" y="%d" width="32" height="20" rx="2" style="fill:#9fcaf3"/>' % (x + 52, y + 26, x + 56, y + 30))


def area1():
    o = [g4_area(28, 130, 690, 360, "p", 40), g4_area(726, 130, 560, 360, "b", 40),
         '<rect x="1250" y="120" width="270" height="370" rx="40" style="fill:#fff4cf;fill-opacity:.9"/>']
    ys = [195, 300, 410]
    for y in ys:
        o.append(desk(60, y - 30))
        o.append(line((200, y + 10), (225, y), "#9aa3b2", 3))
    o.append(desk(180, 430 - 30))
    # линии в «воронку»
    for y in ys + [455]:
        o.append('<path d="M%d %d C330 %d 330 300 380 300" fill="none" stroke="#e05a97" stroke-width="3"/>' % (310, y, y))
    o += [puck(262, 190, 96, "b"), puck(276, 296, 96, "b"), puck(278, 404, 96, "b")]
    return svg("".join(o), W, H)


def funnel():
    o = ['<path d="M372 236 L560 270 L560 248 L632 305 L560 362 L560 340 L372 374 z" style="fill:#ff8fbf;fill-opacity:.85"/>',
         puck(662, 280, 150, "b")]
    return svg("".join(o), W, H)


def abr_flow():
    o = [cloud_icon(855, 330, 1.9, "#ffffff", "#9fcaf3"), g4_arr(770, 320, 948, 320, BL, 9)]
    return svg("".join(o), W, H)


def asbr_flow():
    o = [puck(1035, 280, 150, "p"),
         '<path d="M1112 290 L1240 290 L1240 268 L1290 315 L1240 362 L1240 340 L1112 340 z" style="fill:#ffd84a;fill-opacity:.9"/>']
    for y in (190, 285, 378):
        o.append(g4_tower(1305, y - 36, 50, 72))
        o.append(line((1290, 315), (1305, y), "#e05a97", 3))
    return svg("".join(o), W, H)


ROWS = [(598, "tri", "p", "#fcd3e3", "O", "<b>O</b> — маршрут внутри области"),
        (676, "tree", "b", "#d3e7fb", "O IA", "<b>O IA</b> — межобластной маршрут<br>через ABR"),
        (756, "cloud", "y", "#ffe983", "O E1", "<b>O E1</b> — внешний маршрут:<br>внешняя метрика + стоимость пути OSPF"),
        (836, "cloud", "b", "#c9dcfb", "O E2", "<b>O E2</b> — внешний маршрут:<br>учитывается внешняя метрика")]

TERM = ("R# sh ip route\n"
        "<b style='color:#ff6fa8'>O</b>      10.1.1.0/24  [110/10]  via 10.0.0.2, 00:00:12\n"
        "<b style='color:#5fb0ff'>O IA</b> 10.2.0.0/16  [110/20]  via 10.0.0.1, 00:00:32\n"
        "<b style='color:#ffd84a'>O E1</b> 172.16.0.0/16 [110/110] via 10.0.0.5, 00:01:12\n"
        "<b style='color:#5fb0ff'>O E2</b> 172.17.0.0/16 [110/20]  via 10.0.0.5, 00:01:45")


def router_under():
    return svg(puck(1110, 860, 300, "p") + line((1110, 812), (1110, 860), "#3b4870", 4), W, H)


def foot(x, w, bgc, pad, tone, ix, html):
    return ('<div class="sm-f" style="left:%dpx;width:%dpx;background:%s;padding-left:%dpx">%s</div>' % (x, w, bgc, pad, html)
            + g4_icon("doc", ix, 934, 50, tone))


HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="step">' + area1()
    + p(88, 148, 222, 174, PFX, "10.1.1.0/24", cls="sm-m") + p(72, 258, 208, 284, PFX, "10.1.2.0/24", cls="sm-m")
    + p(82, 362, 206, 388, PFX, "10.1.3.0/24", cls="sm-m") + p(205, 458, 328, 484, PFX, "10.1.4.0/24", cls="sm-m")
    + p(380, 430, 578, 478, "#fbd3e3", "Область 1", "font:700 25px/1 Oswald,sans-serif;border-radius:24px")
    + '</div>',
    '<div class="step">' + funnel()
    + p(400, 124, 664, 222, "#ffe94d", "Несколько непрерывных<br>сетей → один маршрут<br>с короткой маской",
        "font:500 22px/1.2 Oswald,sans-serif;align-items:flex-start;text-align:left;padding-left:10px")
    + p(410, 285, 545, 325, PFX, "10.1.0.0/22", "font:700 23px/1 Oswald,sans-serif")
    + '</div>',
    '<div class="step">' + abr_flow()
    + p(635, 206, 925, 244, "#ffe14d", "<span><b style='font:700 22px Oswald,sans-serif'>ABR</b> • внутренние сети • LSA-3</span>", "font-size:16px")
    + p(782, 278, 930, 314, "#eef6ff", "10.1.0.0/22", "font:700 22px/1 Oswald,sans-serif")
    + p(818, 318, 893, 343, "#2f8fe8", "<span style='color:#fff'>LSA-3</span>", "font:600 18px/1 Oswald,sans-serif;border-radius:6px")
    + p(740, 430, 908, 478, "#cfe4fa", "Область 0", "font:700 25px/1 Oswald,sans-serif;border-radius:24px")
    + '</div>',
    '<div class="step">' + asbr_flow()
    + p(988, 206, 1266, 244, "#ffe14d", "<span><b style='font:700 22px Oswald,sans-serif'>ASBR</b> • внешние сети • LSA-5</span>", "font-size:16px")
    + p(1118, 288, 1236, 342, "#fff1a0", "172.16.0.0/14<br>LSA-5", "font:700 18px/1.3 Oswald,sans-serif")
    + p(1345, 128, 1498, 160, "#ffe14d", "Внешние сети", "font:600 19px/1 Oswald,sans-serif")
    + p(1370, 176, 1500, 206, PFX, "172.16.0.0/16", "font:600 15px/1 Oswald,sans-serif")
    + p(1370, 270, 1500, 300, PFX, "172.17.0.0/16", "font:600 15px/1 Oswald,sans-serif")
    + p(1370, 364, 1500, 394, PFX, "172.18.0.0/16", "font:600 15px/1 Oswald,sans-serif")
    + '</div>',
    '<div class="step">'
    + p(918, 408, 1338, 472, "#fff1b0", "Суммирование включают настройкой;<br>внутри области его не выполняют",
        "font:500 19px/1.3 Oswald,sans-serif;align-items:flex-start;text-align:left;padding-left:68px")
    + svg(g4_glyph_at("gear", 950, 440, 40, "#e05a97", 2.4), W, H)
    + '</div>',
    '<div class="step"><div class="sm-h">КОДЫ МАРШРУТОВ В ТАБЛИЦЕ</div>'
    + "".join('<div class="sm-row" style="top:%dpx"></div>' % y + g4_icon(i, 38, y + 4, 64, tone)
              + '<div class="sm-code" style="top:%dpx;background:%s">%s</div>' % (y + 8, c, k)
              + '<div class="sm-t" style="top:%dpx">%s</div>' % (y + (21 if "<br>" not in t else 11), t)
              for y, i, tone, c, k, t in ROWS)
    + '</div>',
    '<div class="step">'
    + p(722, 527, 1238, 576, "#cde3f8", "Пример вывода таблицы маршрутизации", "font:700 22px/1 'Golos Text',sans-serif;border-radius:22px")
    + '<div class="sm-term">' + TERM + '</div>'
    + '</div>',
    '<div class="step">'
    + foot(32, 480, "#fde0ea", 148, "p", 92, "<b>LSA-1/2</b> — внутренняя топология")
    + foot(555, 408, "#dcecfb", 107, "b", 586, "<b>LSA-3</b> — сети других областей")
    + foot(1014, 446, "#fff1b0", 103, "y", 1040, "<b>LSA-5</b> — внешние маршруты")
    + '</div>',
])
