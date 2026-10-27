# -*- coding: utf-8 -*-
"""Алгоритм Дейкстры: завершение шага из R1 — метки R3 и R5, R1 посещена, следующая R2."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img  # noqa: F401
from _o5_ikit import line, svg, puck, cross, cloud_icon, rack
from _o5_g1kit import g1icon, g1xpuck, g1t

W, H, TOP = 1672, 941, 148

CSS = """<style>
.ose-sub{position:absolute;left:62px;top:150px;font:700 31px/1.15 "Golos Text",sans-serif;color:#2b3a6b;white-space:nowrap}
.ose-box{position:absolute;border-radius:24px}
.ose-in{position:absolute;background:#fff;border-radius:18px}
.ose-h{position:absolute;font:700 23px/1.22 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.ose-f{position:absolute;left:75px;font:700 36px/1.3 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.ose-f b{color:#ff2e7a}
.ose-f small{font:500 31px/1 "Golos Text",sans-serif}
.ose-lb{position:absolute;height:40px;padding:0 8px;background:#fff;border:3px solid #ff8fbd;border-radius:10px;
  font:800 30px/34px "Golos Text",sans-serif;color:#ff2e7a;text-align:center}
.ose-pl{position:absolute;height:38px;padding:0 7px;background:#ffd6e6;border:2px solid #ff8fbd;border-radius:8px;font:800 26px/34px "Golos Text",sans-serif;color:#1f1a33}
.ose-w{position:absolute;font:700 29px/1 "Golos Text",sans-serif;color:#1f1a33;background:rgba(255,236,244,.92);border-radius:6px;padding:0 3px}
.ose-card{position:absolute;top:690px;height:220px;background:rgba(255,255,255,.97);border:2px solid #efe6ee;border-radius:22px}
.ose-ct{position:absolute;font:700 19px/1.2 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.ose-tb{position:absolute;left:454px;top:766px;border-collapse:collapse;font:700 19px/1 "Golos Text",sans-serif;color:#1f1a33}
.ose-tb th{width:100px;height:52px;background:#ffe0ec;border-right:2px solid #fff}
.ose-tb td{height:74px;text-align:center;background:#fff;border-right:2px solid #f3e6ee;font:600 32px/1 "Golos Text",sans-serif;color:#ff2e7a}
.ose-s{position:absolute;font:500 15px/1.25 "Golos Text",sans-serif;color:#2b2540;white-space:nowrap}
</style>"""


def lb(x, y, w, t):
    return '<div class="ose-lb" style="left:%dpx;top:%dpx;min-width:%dpx">%s</div>' % (x, y, w, t)


def pl(x, y, t):
    return '<div class="ose-pl" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


def wt(x, y, t):
    return '<div class="ose-w" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


def ncirc(n, x, y, c):
    return ('<div class="ab" style="left:%dpx;top:%dpx;width:44px;height:44px;border-radius:50%%;background:%s;'
            'font:800 24px/44px Golos Text,sans-serif;color:#fff;text-align:center">%d</div>' % (x, y, c, n))


P = {"R1": (787, 262), "R5": (1347, 262), "R3": (1073, 408), "R2": (787, 562), "R4": (1347, 562)}


def graph():
    c = {k: (x, y + 25) for k, (x, y) in P.items()}
    o = ['<rect x="505" y="195" width="1147" height="480" rx="24" style="fill:#fbe9f2;opacity:.8"/>',
         cloud_icon(640, 280, 1.0), cloud_icon(1530, 450, .9), rack(530, 380, 70, 150), rack(1560, 230, 66, 140),
         line(c["R1"], c["R3"], "#fff38a", 20), line(c["R1"], c["R5"], "#fff38a", 20)]
    for a, b in [("R1", "R5"), ("R1", "R3"), ("R1", "R2"), ("R2", "R3"), ("R3", "R5"), ("R3", "R4"), ("R5", "R4"), ("R2", "R4")]:
        o.append(line(c[a], c[b], "#1f5fbf", 6))
    for k, (x, y) in P.items():
        o.append(g1xpuck(x, y, 150, "b") if k == "R1" else puck(x, y, 150, "b"))
    return svg("".join(o))


def upd(y, n, head, f, v):
    return ('<div class="step"><div class="ose-box" style="left:38px;top:%dpx;width:440px;height:212px;background:#fff6d6"></div>'
            '%s<div class="ose-h" style="left:125px;top:%dpx">%s</div><div class="ose-in" style="left:52px;top:%dpx;width:375px;height:118px"></div>'
            '<div class="ose-f" style="top:%dpx">%s<br><small>→ метка</small> <b>%s</b></div>%s</div>'
            % (y, ncirc(n, 60, y + 22, "#ff5c9e"), y + 14, head, y + 84, y + 92, f, v, ""))


HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="ose-sub">Обновляем метки R3 и R5, затем отмечаем R1 как посещённую</div>',
    '<div class="step">' + graph() + pl(758, 316, "R1") + lb(762, 196, 50, "0") + svg(cross(787, 216, 22, "#e8245e", 6)) + pl(1318, 316, "R5") + pl(1048, 464, "R3") + pl(758, 624, "R2") + pl(1318, 624, "R4")
    + wt(1055, 236, "15") + wt(912, 320, "10") + wt(1196, 323, "3") + wt(754, 413, "8") + wt(1367, 434, "16")
    + wt(907, 481, "11") + wt(1199, 481, "12") + wt(1055, 581, "16")
    + lb(752, 517, 66, "8") + lb(1311, 517, 74, "<span style=\"font:900 46px/30px Arial\">∞</span>") + '</div>',
    upd(215, 1, "Обновляем метку R3<br>через R1", "R3: <b>0</b> + <b>10</b> = <b>10</b>", "10") + '<div class="step">'
    + lb(1040, 348, 76, "10") + '</div>',
    upd(442, 2, "Обновляем метку R5<br>через R1", "R5: <b>0</b> + <b>15</b> = <b>15</b>", "15") + '<div class="step">'
    + lb(1310, 206, 76, "15") + '</div>',
    '<div class="step"><div class="ose-box" style="left:38px;top:675px;width:388px;height:232px;background:#e3f0fc"></div>'
    + ncirc(3, 60, 692, "#3b8de0")
    + '<div class="ose-h" style="left:128px;top:692px;font-size:24px">Отмечаем R1<br>как посещённую</div>'
    '<div class="ose-in" style="left:52px;top:762px;width:358px;height:82px"></div>'
    '<div class="ose-h" style="left:68px;top:770px;font-weight:500;font-size:21px">Все соседи R1 проверены,<br>метки обновлены.</div></div>',
    '<div class="step"><div class="ose-card" style="left:440px;width:525px"></div>' + g1icon("table", 460, 706, 62, "b")
    + '<div class="ose-ct" style="left:543px;top:718px">Метки после проверки всех соседей R1</div>'
    '<table class="ose-tb"><tr><th>R1</th><th>R2</th><th>R3</th><th>R4</th><th>R5</th></tr>'
    '<tr><td></td><td>8</td><td>10</td><td style="color:#1f1a33;font:900 46px Arial">∞</td><td>15</td></tr></table>'
    + svg(g1t(504, 866, "0", 32, "#ff2e7a", weight=600) + cross(504, 855, 22, "#e8245e", 5)) + '</div>',
    '<div class="step"><div class="ose-card" style="left:978px;width:335px"></div>' + g1icon("arrow", 992, 706, 66, "y")
    + '<div class="ose-ct" style="left:1073px;top:718px">Следующая вершина</div>'
    '<div class="ose-s" style="left:1073px;top:748px;font-size:13.5px">Выбираем непосещённую вершину<br>с наименьшей меткой.</div>'
    '<div class="ose-in" style="left:990px;top:808px;width:310px;height:90px;background:#ffe0ec"></div>'
    '<div class="ose-lb" style="left:1010px;top:826px;height:56px;width:68px;background:#ff2e7a;border-color:#ff2e7a;color:#fff;line-height:50px">R2</div>'
    '<div class="ose-s" style="left:1093px;top:832px;font-size:17px">метка 8 — минимальная<br>среди непосещённых</div></div>',
    '<div class="step"><div class="ose-card" style="left:1325px;width:325px"></div>' + g1icon("bulb", 1342, 708, 62, "p")
    + '<div class="ose-ct" style="left:1425px;top:718px">Вывод</div>'
    '<div class="ose-in" style="left:1338px;top:770px;width:302px;height:132px;background:#fff6c8"></div>'
    '<div class="ose-s" style="left:1358px;top:780px;font-size:17.5px">Минимальное расстояние<br>до R1 окончательно.<br>'
    'Отмечаем R1 как посещённую<br>и переходим к ближайшей<br>непосещённой вершине.</div></div>',
])
