# -*- coding: utf-8 -*-
"""Алгоритм Дейкстры — 4 шага, пример графа R1..R4, легенда."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 160

CSS = """<style>
.odi-sub{position:absolute;z-index:5;left:82px;top:168px;font:700 30px/1.15 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odi-c{position:absolute;left:40px;width:565px;background:rgba(255,255,255,.96);border:2px solid #eee6f0;border-radius:22px}
.odi-tag{position:absolute;left:252px;padding:3px 16px;border-radius:12px;font:800 23px/1.2 "Golos Text",sans-serif;color:#1f1a33}
.odi-t{position:absolute;left:252px;font:500 18.8px/1.27 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odi-n{position:absolute;display:flex;align-items:center;justify-content:center;font:800 32px/1 "Golos Text",sans-serif;color:#1f1a33;border-radius:12px}
.odi-w{position:absolute;width:42px;height:42px;border-radius:50%;background:#fff;border:3px solid;display:flex;align-items:center;
  justify-content:center;font:800 26px/1 "Golos Text",sans-serif;color:#1f1a33}
.odi-pl{position:absolute;padding:2px 10px;border:3px solid #1f1a33;border-radius:10px;background:#fff;font:800 26px/1.1 "Golos Text",sans-serif;color:#1f1a33}
.odi-call{position:absolute;left:1122px;top:184px;width:158px;height:64px;background:#fff;border:3px solid #ff8fbd;border-radius:12px;
  font:800 19px/1.1 "Golos Text",sans-serif;color:#1f1a33;text-align:center;padding-top:8px}
.odi-ex{position:absolute;left:700px;top:706px;width:732px;height:100px;background:rgba(255,255,255,.97);border:3px solid #ffb6d3;border-radius:22px}
.odi-ext{position:absolute;left:730px;font:500 21px/1.2 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odi-ext em{font-style:italic;font-weight:800}
.odi-pm{background:#ffc6dd;border-radius:10px;padding:1px 12px;font-weight:800;margin-right:14px}
.odi-bar{position:absolute;left:15px;top:828px;width:1642px;height:104px;background:#fff;border-radius:24px}
.odi-bt{position:absolute;top:856px;font:500 16.5px/1.3 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odi-bt b{font-weight:800}
.odi-bn{position:absolute;left:805px;top:848px;font:500 15px/1.4 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odi-bn i,.odi-bn b{font-weight:800}
</style>"""


def card(y, h, n, tag, tc, text):
    return ('<div class="step"><div class="odi-c" style="top:%dpx;height:%dpx"></div>%s'
            '<div class="odi-tag" style="top:%dpx;background:%s">%s</div><div class="odi-t" style="top:%dpx">%s</div></div>'
            % (y, h, img("o_dij_intro_c%d.png" % n, "left:50px;top:%dpx;width:190px" % {1: 232, 2: 375, 3: 518, 4: 676}[n]),
               y + 16, tc, tag, y + 62, text))


def nb(x, y, w, h, t, bc, bgc):
    return ('<div class="odi-n" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border:3px solid %s;background:%s">%s</div>'
            % (x, y, w, h, bc, bgc, t))


def wt(x, y, t, c):
    return '<div class="odi-w" style="left:%dpx;top:%dpx;border-color:%s">%s</div>' % (x, y, c, t)


def pl(x, y, t):
    return '<div class="odi-pl" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="odi-sub">Как маршрутизатор строит дерево кратчайших путей SPF</div>',
    card(222, 138, 1, "Старт", "#ffc6dd", "Все вершины непосещённые.<br>Корень — R1: метка 0;<br>остальные метки — ∞."),
    card(367, 135, 2, "Выбор", "#cfe6fb", "Выбери непосещённую вершину<br>с минимальной меткой."),
    card(510, 150, 3, "Пересчёт", "#ffe58a", "Проверь её соседей: новая метка =<br>метка вершины + вес ребра.<br>Если путь короче — обнови метку."),
    card(668, 140, 4, "Повтор", "#cfe6fb", "Отметь вершину посещённой<br>и повторяй шаги, пока не будут<br>посещены все вершины."),
    '<div class="step">' + img("o_dij_intro_scene.png", "left:615px;top:212px;width:1043px;border-radius:24px")
    + img("o_dij_intro_top.png", "left:862px;top:100px;width:796px")
    + pl(1006, 281, "R1") + pl(746, 494, "R2") + pl(1471, 494, "R3") + pl(1103, 623, "R4") + '</div>',
    '<div class="step">' + wt(860, 357, 2, "#ffd84a") + wt(1254, 345, 5, "#7fb6f0") + wt(914, 533, 1, "#ffd84a")
    + wt(1322, 527, 1, "#ffd84a") + '</div>',
    '<div class="step">' + nb(1018, 178, 58, 50, 0, "#1f1a33", "#ffc6dd") + '<div class="odi-call">R1 — корень<br>(0)</div>'
    + nb(762, 394, 52, 46, 2, "#1f1a33", "#ffe14d") + nb(1112, 518, 52, 46, 3, "#1f1a33", "#ffe14d")
    + nb(1468, 399, 52, 46, 4, "#1f1a33", "#ffe14d") + '</div>',
    '<div class="step"><div class="odi-ex"></div>'
    '<div class="odi-ext" style="top:729px;left:732px"><span class="odi-pm">Пример:</span>R1—R2 =&nbsp; 2; R1—R3 = 5; R2—R4 = 1; R4—R3 = 1.</div>'
    '<div class="odi-ext" style="top:762px"><b>Кратчайший путь до R3:</b> <em>R1→R2→R4→R3,</em> суммарная стоимость <b>4.</b></div></div>',
    '<div class="step"><div class="odi-bar"></div>'
    + img("o_dij_intro_b1.png", "left:45px;top:838px;width:95px") + img("o_dij_intro_b2.png", "left:278px;top:838px;width:82px")
    + img("o_dij_intro_b3.png", "left:455px;top:838px;width:83px") + img("o_dij_intro_b4.png", "left:700px;top:838px;width:90px")
    + '<div class="odi-bt" style="left:140px"><b>Вершина —</b><br>маршрутизатор</div>'
    '<div class="odi-bt" style="left:376px"><b>Ребро —</b><br>канал</div>'
    '<div class="odi-bt" style="left:546px"><b>Вес ребра —</b><br>метрика</div>'
    '<div class="odi-bn"><i>OSPF</i> использует <b>SPF</b> для выбора маршрутов и создания таблицы маршрутизации.<br>'
    'Алгоритм также применяется в <b>IS-IS</b>. Работает при неотрицательных весах рёбер.<br>'
    'Эдсгер Дейкстра предложил алгоритм в <b>1959</b> году.</div></div>',
])
