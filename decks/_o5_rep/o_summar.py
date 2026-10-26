# -*- coding: utf-8 -*-
"""Суммирование и типы маршрутов OSPF: 10.1.0.0/22 через ABR, 172.16.0.0/14 через ASBR, коды O/O IA/O E1/O E2."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1536, 1024, 124
N = "o_summar_"

CSS = """<style>
.sm-p{position:absolute;border-radius:12px;text-align:center;color:#1f1a33;font:600 19px/1.2 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.sm-m{font:500 16px/1 "JetBrains Mono",monospace!important}
.sm-h{position:absolute;left:42px;top:512px;font:700 64px/1 Oswald,sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.74);transform-origin:left}
.sm-row{position:absolute;left:32px;width:660px;height:72px;background:rgba(255,255,255,.95);border:1.5px solid #ece7f1;border-radius:16px}
.sm-code{position:absolute;left:136px;width:128px;height:56px;border-radius:28px;font:700 32px/56px Oswald,sans-serif;text-align:center;color:#1f1a33}
.sm-t{position:absolute;left:288px;font:400 19px/1.3 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.sm-term{position:absolute;left:722px;top:578px;width:556px;height:172px;background:#141a33;border-radius:10px;border:2px solid #3b4870;
 font:400 15px/30px "JetBrains Mono",monospace;color:#d8e2ff;padding:6px 18px;white-space:pre}
.sm-term b{font-family:Oswald,sans-serif;font-size:22px;font-weight:600}
.sm-f{position:absolute;top:928px;height:62px;border-radius:20px;font:400 19px/62px "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.sm-f b{font-size:22px}
</style>"""


def p(x0, y0, x1, y1, col, html, extra="", cls=""):
    return '<div class="sm-p %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        cls, x0, y0, x1 - x0, y1 - y0, col, extra, html)


PFX = "#fde6ef"
ROWS = [(598, "i1", "#fcd3e3", "O", "<b>O</b> — маршрут внутри области"),
        (676, "i2", "#d3e7fb", "O IA", "<b>O IA</b> — межобластной маршрут<br>через ABR"),
        (756, "i3", "#ffe983", "O E1", "<b>O E1</b> — внешний маршрут:<br>внешняя метрика + стоимость пути OSPF"),
        (836, "i4", "#c9dcfb", "O E2", "<b>O E2</b> — внешний маршрут:<br>учитывается внешняя метрика")]

TERM = ("R# sh ip route\n"
        "<b style='color:#ff6fa8'>O</b>      10.1.1.0/24  [110/10]  via 10.0.0.2, 00:00:12\n"
        "<b style='color:#5fb0ff'>O IA</b> 10.2.0.0/16  [110/20]  via 10.0.0.1, 00:00:32\n"
        "<b style='color:#ffd84a'>O E1</b> 172.16.0.0/16 [110/110] via 10.0.0.5, 00:01:12\n"
        "<b style='color:#5fb0ff'>O E2</b> 172.17.0.0/16 [110/20]  via 10.0.0.5, 00:01:45")

HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="step">' + img(N + "top.png", "left:22px;top:118px;width:1494px")
    + p(88, 148, 222, 174, PFX, "10.1.1.0/24", cls="sm-m") + p(72, 263, 208, 290, PFX, "10.1.2.0/24", cls="sm-m")
    + p(82, 370, 206, 396, PFX, "10.1.3.0/24", cls="sm-m") + p(205, 450, 328, 476, PFX, "10.1.4.0/24", cls="sm-m")
    + p(380, 430, 578, 478, "#fbd3e3", "Область 1", "font:700 25px/1 Oswald,sans-serif;border-radius:24px")
    + '</div>',
    '<div class="step">'
    + p(400, 124, 664, 222, "#ffe94d", "Несколько непрерывных<br>сетей → один маршрут<br>с короткой маской",
        "font:500 22px/1.2 Oswald,sans-serif;align-items:flex-start;text-align:left;padding-left:10px")
    + p(410, 290, 545, 330, PFX, "10.1.0.0/22", "font:700 23px/1 Oswald,sans-serif")
    + '</div>',
    '<div class="step">'
    + p(635, 206, 925, 244, "#ffe14d", "<span><b style='font:700 22px Oswald,sans-serif'>ABR</b> • внутренние сети • LSA-3</span>", "font-size:16px")
    + p(776, 288, 924, 324, "#eef6ff", "10.1.0.0/22", "font:700 22px/1 Oswald,sans-serif")
    + p(800, 323, 875, 348, "#2f8fe8", "<span style='color:#fff'>LSA-3</span>", "font:600 18px/1 Oswald,sans-serif;border-radius:6px")
    + p(700, 430, 868, 478, "#cfe4fa", "Область 0", "font:700 25px/1 Oswald,sans-serif;border-radius:24px")
    + '</div>',
    '<div class="step">'
    + p(988, 206, 1266, 244, "#ffe14d", "<span><b style='font:700 22px Oswald,sans-serif'>ASBR</b> • внешние сети • LSA-5</span>", "font-size:16px")
    + p(1126, 288, 1258, 352, "#fff1a0", "172.16.0.0/14<br>LSA-5", "font:700 20px/1.4 Oswald,sans-serif")
    + p(1345, 118, 1498, 153, "#ffe14d", "Внешние сети", "font:600 19px/1 Oswald,sans-serif")
    + p(1382, 178, 1500, 208, PFX, "172.16.0.0/16", "font:600 15px/1 Oswald,sans-serif")
    + p(1388, 272, 1500, 302, PFX, "172.17.0.0/16", "font:600 15px/1 Oswald,sans-serif")
    + p(1385, 366, 1500, 396, PFX, "172.18.0.0/16", "font:600 15px/1 Oswald,sans-serif")
    + '</div>',
    '<div class="step">'
    + p(972, 408, 1338, 472, "#fff1b0", "Суммирование включают настройкой;<br>внутри области его не выполняют",
        "font:500 19px/1.3 Oswald,sans-serif;align-items:flex-start;text-align:left;padding-left:8px")
    + '</div>',
    '<div class="step"><div class="sm-h">КОДЫ МАРШРУТОВ В ТАБЛИЦЕ</div>'
    + "".join('<div class="sm-row" style="top:%dpx"></div>' % y + img(N + i + ".png", "left:36px;top:%dpx" % y)
              + '<div class="sm-code" style="top:%dpx;background:%s">%s</div>' % (y + 6, c, k)
              + '<div class="sm-t" style="top:%dpx">%s</div>' % (y + (18 if "<br>" not in t else 8), t)
              for y, i, c, k, t in ROWS)
    + '</div>',
    '<div class="step">' + img(N + "room.png", "left:708px;top:512px;width:810px")
    + p(722, 527, 1238, 576, "#cde3f8", "Пример вывода таблицы маршрутизации", "font:700 22px/1 'Golos Text',sans-serif;border-radius:22px")
    + '<div class="sm-term">' + TERM + '</div>'
    + '</div>',
    '<div class="step">'
    + '<div class="sm-f" style="left:32px;width:480px;background:#fde0ea;padding-left:148px"><b>LSA-1/2</b> — внутренняя топология</div>'
    + img(N + "d1.png", "left:102px;top:934px")
    + '<div class="sm-f" style="left:555px;width:408px;background:#dcecfb;padding-left:107px"><b>LSA-3</b> — сети других областей</div>'
    + img(N + "d2.png", "left:586px;top:934px")
    + '<div class="sm-f" style="left:1014px;width:446px;background:#fff1b0;padding-left:103px"><b>LSA-5</b> — внешние маршруты</div>'
    + img(N + "d3.png", "left:1034px;top:934px")
    + '</div>',
])
