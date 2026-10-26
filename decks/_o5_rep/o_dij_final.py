# -*- coding: utf-8 -*-
"""Алгоритм Дейкстры: завершение расчёта — шаги 4 (R4) и 5 (R5), итоговые расстояния от R1."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 940, 112

CSS = """<style>
.odf-sub{position:absolute;left:52px;top:118px;font:700 35px/1.1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odf-pl{position:absolute;width:76px;height:38px;border-radius:9px;text-align:center;font:700 27px/38px "Golos Text",sans-serif;color:#1f1a33}
.odf-w{position:absolute;font:700 25px/1 "Golos Text",sans-serif;color:#1f1a33;background:rgba(255,255,255,.85);border-radius:5px;padding:1px 3px}
.odf-tb{position:absolute;left:52px;top:705px;width:765px;height:160px;background:rgba(255,255,255,.96);border-radius:20px}
.odf-th{position:absolute;left:52px;top:705px;width:765px;height:50px;background:#fff0a6;border-radius:20px 20px 0 0;
  font:700 27px/50px "Golos Text",sans-serif;color:#1f1a33;padding-left:27px}
.odf-c{position:absolute;width:144px;text-align:center;background:#ffe3ee;border-radius:8px;color:#1f1a33}
.odf-p{position:absolute;left:850px;width:800px;border-radius:28px;background:rgba(255,255,255,.9);border:2px solid}
.odf-ph{position:absolute;left:920px;height:46px;padding:0 20px 0 18px;border-radius:0 23px 23px 0;font:600 25px/46px "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odf-li{position:absolute;left:890px;font:500 18.5px/1.25 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odf-li:before{content:"";position:absolute;left:0;top:7px;width:12px;height:12px;border-radius:50%;background:var(--d)}
.odf-li span{display:block;padding-left:26px}
.odf-li i{font-style:normal;background:#ffd6e6;border-radius:12px;padding:1px 10px}
.odf-inf{position:absolute;left:845px;top:805px;width:418px;height:72px;background:#fff8d4;border-radius:36px}
.odf-it{position:absolute;left:930px;top:812px;font:500 14.5px/1.3 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odf-ft{position:absolute;left:40px;top:882px;width:1600px;height:42px;background:#e3f0fc;border-radius:21px;
  font:500 18px/42px "Golos Text",sans-serif;color:#1f1a33;padding-left:74px}
</style>"""


def pl(x, y, t, c):
    return '<div class="odf-pl" style="left:%dpx;top:%dpx;background:%s">%s</div>' % (x, y, c, t)


def wt(x, y, t):
    return '<div class="odf-w" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


def li(y, t, d):
    return '<div class="odf-li" style="top:%dpx;--d:%s"><span>%s</span></div>' % (y, d, t)


def node(x, y, n, m, c="#cfe6fb"):
    return pl(x, y, n, c) + pl(x + 3, y + 40, m, "#ffd6e6")


TAB = "".join('<div class="odf-c" style="left:%dpx;top:762px;height:40px;font:700 20px/40px \'Golos Text\',sans-serif">%s</div>'
              '<div class="odf-c" style="left:%dpx;top:808px;height:48px;font:600 28px/48px \'Golos Text\',sans-serif">%s</div>'
              % (62 + 149 * i, r, 62 + 149 * i, v) for i, (r, v) in enumerate(zip(["R1", "R2", "R3", "R4", "R5"], ["0", "8", "10", "22", "13"])))
PK, BL = "#ff4f9a", "#3a8ff0"

HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="odf-sub">Четвёртый и пятый шаги</div>',
    '<div class="step">' + img("o_dij_final_g.png", "left:40px;top:160px;width:800px")
    + wt(415, 270, "15") + wt(298, 352, "10") + wt(560, 345, "3") + wt(148, 435, "8") + wt(710, 435, "16")
    + wt(278, 482, "11") + wt(557, 490, "12") + wt(416, 552, "16")
    + node(140, 193, "R1", "0") + node(657, 195, "R5", "13") + node(397, 347, "R3", "10") + node(139, 616, "R2", "8")
    + node(651, 616, "R4", "22", "#ffe58a") + '</div>',
    '<div class="step"><div class="odf-p" style="top:92px;height:390px;border-color:#ffd6e6"></div>'
    + '<div class="odf-ph" style="top:105px;background:#ffd6e6"><b>Шаг 4:</b> обрабатываем вершину R4 (22)</div>'
    + img("o_dij_final_n4.png", "left:870px;top:105px;width:55px") + img("o_dij_final_g4.png", "left:1225px;top:150px;width:430px")
    + li(162, "Текущая вершина: <b>R4</b><br>(метка 22).", PK)
    + li(216, "Соседи <b>R2</b> и <b>R3</b> уже посещены,<br>проверяем только <b>R5</b>.", PK)
    + li(272, "Вычисляем путь через R4<br>к R5: &nbsp;<i>22 + 16 = 38.</i>", PK)
    + li(331, "Текущая метка <b>R5</b> = 13,<br>и <b>13</b> &lt; <b>38</b>, поэтому метка<br>R5 не изменяется (остаётся 13).", PK)
    + li(415, "Отмечаем вершину <b>R4</b><br>как посещённую.", PK) + '</div>',
    '<div class="step"><div class="odf-p" style="top:497px;height:300px;border-color:#cfe6fb"></div>'
    + '<div class="odf-ph" style="top:510px;background:#cfe6fb"><b>Шаг 5:</b> обрабатываем вершину R5 (13)</div>'
    + img("o_dij_final_n5.png", "left:870px;top:510px;width:55px") + img("o_dij_final_g5.png", "left:1240px;top:548px;width:415px")
    + li(572, "Текущая вершина: <b>R5</b> (метка 13).", BL) + li(606, "Соседи R1, R3 и <b>R4</b> уже посещены.", BL)
    + li(641, "Метка <b>R5</b> остаётся равной 13.", BL) + li(680, "Отмечаем вершину <b>R5</b><br>как посещённую.", BL)
    + li(736, "Алгоритм завершён, так как<br>все вершины посещены.", BL) + '</div>',
    '<div class="step"><div class="odf-inf"></div>' + img("o_dij_final_i.png", "left:845px;top:805px;width:75px")
    + '<div class="odf-it">Если все непосещённые вершины имеют<br>метку ∞, они недостижимы. Алгоритм<br>можно завершить досрочно.</div></div>',
    '<div class="step"><div class="odf-tb"></div><div class="odf-th">Кратчайшие расстояния от R1</div>' + TAB + '</div>',
    '<div class="step"><div class="odf-ft">Полученные кратчайшие пути используются при формировании таблицы маршрутизации.</div>'
    + img("o_dij_final_go.png", "left:40px;top:880px;width:55px") + '</div>',
])
