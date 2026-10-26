# -*- coding: utf-8 -*-
"""Участие LSA в сходимости OSPF: LSDB -> SPF -> RIB, области, таблица маршрутизации."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1774, 887, 150
N = "o_lsa_converge_"

CSS = """<style>
.lc-box{position:absolute;background:rgba(255,255,255,.95);border:2px solid #ebe6f1;border-radius:20px}
.lc-n{position:absolute;width:46px;height:46px;border-radius:50%;font:700 28px/46px "Golos Text",sans-serif;text-align:center;color:#1f1a33}
.lc-h{position:absolute;font:800 21px/1.25 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.lc-t{position:absolute;font:400 15.5px/1.3 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.lc-ar{position:absolute;top:218px;font:900 44px/1 sans-serif;color:#ffc81a}
.lc-p{position:absolute;border-radius:10px;text-align:center;font:700 17px/1.15 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.lc-p span{font-size:15px;color:#1f1a33}
.lc-pan{position:absolute;top:537px;height:280px;border-radius:18px;border:2px solid}
.lc-tb{position:absolute;font:400 13px/1.3 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
</style>"""


def p(x0, y0, x1, y1, col, html, color="#1f1a33", extra=""):
    return '<div class="lc-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;color:%s;%s">%s</div>' % (
        x0, y0, x1 - x0, y1 - y0, col, color, extra, html)


def t(x, y, html, cls="lc-t", extra=""):
    return '<div class="%s" style="left:%dpx;top:%dpx;%s">%s</div>' % (cls, x, y, extra, html)


def step(x0, x1, nc, n, title, text, ico, ix, iy):
    return ('<div class="step"><div class="lc-box" style="left:%dpx;top:165px;width:%dpx;height:146px"></div>' % (x0, x1 - x0)
            + '<div class="lc-n" style="left:%dpx;top:180px;background:%s">%s</div>' % (x0 + 14, nc, n)
            + img(N + ico, "left:%dpx;top:%dpx" % (ix, iy)) + t(x0 + 82, 178, title, "lc-h") + t(x0 + 16, 240, text) + '</div>')


def panel(x0, x1, col, bd, nc, n, title, rows):
    out = ('<div class="lc-pan" style="left:%dpx;width:%dpx;background:%s;border-color:%s"></div>' % (x0, x1 - x0, col, bd)
           + '<div class="lc-n" style="left:%dpx;top:546px;background:%s">%s</div>' % (x0 + 18, nc, n)
           + t(x0 + 84, 554, title, "lc-h", "font-size:22px")
           + '<div class="lc-box" style="left:%dpx;top:598px;width:%dpx;height:212px;border-radius:14px;border:0"></div>' % (x0 + 10, x1 - x0 - 20))
    for ico, ix, iy, tx, ty, txt in rows:
        out += img(N + ico, "left:%dpx;top:%dpx" % (ix, iy)) + t(tx, ty, txt, extra="font-size:16.5px")
    return '<div class="step">' + out + '</div>'


TROWS = [("t1", 632, "#fde2ec", "Внутриобластный", "Сети в той же области<br>(по LSA-1/LSA-2)", "O"),
         ("t2", 690, "#dcecfb", "Межобластный", "Сети в других областях<br>(по LSA-3, от ABR)", "O IA"),
         ("t3", 748, "#fff1b8", "Внешний", "Внешние сети<br>(по LSA-5, путь к ASBR через LSA-4)", "O E1 /<br>O E2")]

HTML = CSS + bg("bg5", W, H) + "".join([
    img(N + "girl.png", "left:1232px;top:150px;width:542px"),
    step(25, 407, "#ff79ab", "1", "LSA поступают<br>в LSDB", "Маршрутизаторы обмениваются<br>LSA, формируя единую базу<br>состояния ссылок (LSDB).", "s1.png", 288, 178),
    '<div class="lc-ar" style="left:408px">➜</div>',
    step(458, 823, "#5aa9ee", "2", "Маршрутизатор<br>рассчитывает пути", "Алгоритм SPF строит дерево<br>кратчайших путей по данным<br>из LSDB.", "s2.png", 710, 205),
    '<div class="lc-ar" style="left:826px">➜</div>',
    step(876, 1236, "#ffd52e", "3", "Записи попадают<br>в таблицу маршрутизации", "Рассчитанные маршруты<br>устанавливаются в таблицу<br>маршрутизации (RIB).", "s3.png", 1143, 238),
    '<div class="step">' + img(N + "net.png", "left:22px;top:330px;width:1750px")
    + p(196, 338, 364, 381, "#fde3ec", "Area 1<span>(обычная область)</span>", "#9b1f4f", "font-size:21px")
    + p(612, 338, 836, 381, "#dbeafa", "Area 0<span>(магистральная область)</span>", "#1f1a33", "font-size:21px")
    + p(1014, 338, 1180, 381, "#fff3c8", "Area 2<span>(обычная область)</span>", "#1f1a33", "font-size:21px")
    + p(1630, 430, 1726, 493, "#dcedfc", "Внешние<br>сети<br>(другая AS)", "#1f1a33", "font-size:16px")
    + '</div>',
    '<div class="step">'
    + p(212, 396, 390, 436, "#fde6ef", "LSA-1, LSA-2<span>(только в этой области)</span>", "#ff3d8b")
    + p(1050, 396, 1220, 436, "#fff3c8", "LSA-1, LSA-2<span>(только в этой области)</span>", "#f0a51a")
    + '</div>',
    '<div class="step">'
    + p(650, 391, 794, 431, "#dbeafa", "LSA-3<span style='color:#1d6fd0'>(summary от ABR)</span>", "#1d6fd0")
    + p(1224, 391, 1334, 431, "#fff", "LSA-4<span style='color:#1d6fd0'>(путь к ASBR)</span>", "#1d6fd0")
    + '</div>',
    '<div class="step">'
    + p(1430, 391, 1578, 431, "#fff", "LSA-5<span style='color:#ff3d8b'>(внешний маршрут)</span>", "#ff3d8b")
    + '</div>',
    panel(25, 415, "#fde8f0", "#f6bdd2", "#ff79ab", "1", "Внутри области", [
        ("a1.png", 42, 606, 110, 610, "<b>LSA-1 и LSA-2</b> описывают<br>топологию области."),
        ("a2.png", 42, 678, 110, 678, "<b>SPF</b> строит дерево и рассчитывает<br>intra-area маршруты (к сетям<br>в той же области)."),
        ("a3.png", 42, 752, 110, 758, "Код маршрутов в таблице:<br><b>O</b> (OSPF intra-area).")]),
    panel(428, 815, "#e6f1fc", "#b5d6f4", "#5aa9ee", "2", "Между областями", [
        ("b1.png", 446, 612, 512, 610, "<b>LSA-3</b> сообщает о доступных<br>сетях в других областях."),
        ("b2.png", 446, 682, 512, 678, "<b>ABR</b> передаёт summary (сводную)<br>информацию между областями."),
        ("b3.png", 446, 752, 512, 752, "Код маршрутов в таблице:<br><b>O IA</b> (OSPF inter-area).")]),
    panel(828, 1195, "#fff6d4", "#f3dc7a", "#ffd52e", "3", "Внешние сети", [
        ("c1.png", 842, 610, 910, 600, "<b>LSA-5</b> несёт внешний маршрут<br>(например, из другой AS)."),
        ("c2.png", 842, 666, 910, 650, "<b>LSA-4</b> сообщает путь к <b>ASBR</b>."),
        ("c3.png", 842, 740, 910, 740, "Код маршрутов в таблице:<br><b>O E1 или O E2</b><br>(в зависимости от конфигурации).")])[:-6]
    + '<div class="lc-tb" style="left:906px;top:677px;width:272px;height:48px;background:#ffef9e;border-radius:10px;'
      'padding:6px 0 0 40px;font-size:13px"><span style="position:absolute;left:10px;top:12px;width:20px;height:20px;border-radius:50%;'
      'background:#ff3d8b;color:#fff;font:800 13px/20px sans-serif;text-align:center">!</span>LSA-4 не объявляет межобластную<br>сеть — он помогает найти ASBR.</div></div>',
    '<div class="step"><div class="lc-box" style="left:1207px;top:537px;width:542px;height:280px"></div>'
    + t(1226, 548, "Таблица маршрутизации OSPF (пример)", "lc-h", "font-size:22px")
    + '<div class="lc-box" style="left:1220px;top:585px;width:518px;height:36px;background:#d6e8fa;border:0;border-radius:6px"></div>'
    + t(1236, 592, "<b>Тип маршрута</b>", "lc-tb", "font-size:16px") + t(1430, 592, "<b>Описание</b>", "lc-tb", "font-size:16px")
    + t(1680, 592, "<b>Код</b>", "lc-tb", "font-size:16px")
    + "".join('<div class="lc-box" style="left:1220px;top:%dpx;width:190px;height:50px;background:%s;border:0;border-radius:8px"></div>' % (y - 8, c)
              + img(N + i + ".png", "left:1226px;top:%dpx" % y) + t(1274, y + 6, "<b>%s</b>" % a, "lc-tb", "font-size:15px")
              + t(1430, y - 4, d) .replace('class="lc-t"', 'class="lc-tb"') + t(1676, y, "<b>%s</b>" % k, "lc-tb", "font-size:18px;line-height:1.1")
              for i, y, c, a, d, k in TROWS)
    + '</div>',
    '<div class="step"><div class="lc-box" style="left:25px;top:826px;width:1724px;height:44px;background:#e3effb;border:0;border-radius:22px"></div>'
    + img(N + "bulb.png", "left:163px;top:828px")
    + t(224, 836, "<b>После сходимости</b> таблица содержит лучшие доступные маршруты; <b>Stub-область</b> может использовать маршрут по умолчанию вместо LSA-5. "
        "<span style='color:#ff5c9c'>♥</span>", extra="font-size:19px")
    + '</div>',
])
