# -*- coding: utf-8 -*-
"""Алгоритм Дейкстры: завершение шага из R1 — метки R3 и R5, R1 посещена, следующая R2."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

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


def upd(y, n, head, f, v):
    return ('<div class="step"><div class="ose-box" style="left:38px;top:%dpx;width:440px;height:212px;background:#fff6d6"></div>'
            '%s<div class="ose-h" style="left:125px;top:%dpx">%s</div><div class="ose-in" style="left:52px;top:%dpx;width:375px;height:118px"></div>'
            '<div class="ose-f" style="top:%dpx">%s<br><small>→ метка</small> <b>%s</b></div>%s</div>'
            % (y, img("o_dij_s1end_n%d.png" % n, "left:58px;top:%dpx;width:50px" % (y + 23)), y + 14, head, y + 84, y + 92, f, v,
               img("o_dij_s1end_d.png", "left:425px;top:%dpx;width:45px" % (y + 55))))


HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="ose-sub">Обновляем метки R3 и R5, затем отмечаем R1 как посещённую</div>',
    '<div class="step">' + img("o_dij_s1end_g.png", "left:505px;top:195px;width:1147px;border-radius:24px")
    + pl(1318, 316, "R5") + pl(1048, 464, "R3") + pl(758, 624, "R2") + pl(1318, 624, "R4")
    + wt(1055, 236, "15") + wt(912, 320, "10") + wt(1196, 323, "3") + wt(754, 413, "8") + wt(1367, 434, "16")
    + wt(907, 481, "11") + wt(1199, 481, "12") + wt(1055, 581, "16")
    + lb(752, 517, 66, "8") + lb(1311, 517, 74, "<span style=\"font:900 46px/30px Arial\">∞</span>") + '</div>',
    upd(215, 1, "Обновляем метку R3<br>через R1", "R3: <b>0</b> + <b>10</b> = <b>10</b>", "10") + '<div class="step">'
    + lb(1040, 348, 76, "10") + '</div>',
    upd(442, 2, "Обновляем метку R5<br>через R1", "R5: <b>0</b> + <b>15</b> = <b>15</b>", "15") + '<div class="step">'
    + lb(1310, 206, 76, "15") + '</div>',
    '<div class="step"><div class="ose-box" style="left:38px;top:675px;width:388px;height:232px;background:#e3f0fc"></div>'
    + img("o_dij_s1end_n3.png", "left:58px;top:692px;width:50px")
    + '<div class="ose-h" style="left:128px;top:692px;font-size:24px">Отмечаем R1<br>как посещённую</div>'
    '<div class="ose-in" style="left:52px;top:762px;width:358px;height:82px"></div>'
    '<div class="ose-h" style="left:68px;top:770px;font-weight:500;font-size:21px">Все соседи R1 проверены,<br>метки обновлены.</div></div>',
    '<div class="step"><div class="ose-card" style="left:440px;width:525px"></div>' + img("o_dij_s1end_tab.png", "left:455px;top:705px;width:70px")
    + '<div class="ose-ct" style="left:543px;top:718px">Метки после проверки всех соседей R1</div>'
    '<table class="ose-tb"><tr><th>R1</th><th>R2</th><th>R3</th><th>R4</th><th>R5</th></tr>'
    '<tr><td></td><td>8</td><td>10</td><td style="color:#1f1a33;font:900 46px Arial">∞</td><td>15</td></tr></table>'
    + img("o_dij_s1end_x0.png", "left:470px;top:825px;width:75px") + '</div>',
    '<div class="step"><div class="ose-card" style="left:978px;width:335px"></div>' + img("o_dij_s1end_go.png", "left:985px;top:700px;width:80px")
    + '<div class="ose-ct" style="left:1073px;top:718px">Следующая вершина</div>'
    '<div class="ose-s" style="left:1073px;top:748px;font-size:13.5px">Выбираем непосещённую вершину<br>с наименьшей меткой.</div>'
    '<div class="ose-in" style="left:990px;top:808px;width:310px;height:90px;background:#ffe0ec"></div>'
    '<div class="ose-lb" style="left:1010px;top:826px;height:56px;width:68px;background:#ff2e7a;border-color:#ff2e7a;color:#fff;line-height:50px">R2</div>'
    '<div class="ose-s" style="left:1093px;top:832px;font-size:17px">метка 8 — минимальная<br>среди непосещённых</div></div>',
    '<div class="step"><div class="ose-card" style="left:1325px;width:325px"></div>' + img("o_dij_s1end_bulb.png", "left:1335px;top:705px;width:70px")
    + '<div class="ose-ct" style="left:1425px;top:718px">Вывод</div>'
    '<div class="ose-in" style="left:1338px;top:770px;width:302px;height:132px;background:#fff6c8"></div>'
    '<div class="ose-s" style="left:1358px;top:780px;font-size:17.5px">Минимальное расстояние<br>до R1 окончательно.<br>'
    'Отмечаем R1 как посещённую<br>и переходим к ближайшей<br>непосещённой вершине.</div></div>',
])
