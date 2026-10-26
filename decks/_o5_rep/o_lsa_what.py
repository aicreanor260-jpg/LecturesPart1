# -*- coding: utf-8 -*-
"""LSA: запись о состоянии канала — 4 шага, заголовок LSA, пример топологии."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 208
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %dpx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


CSS = """<style>
.olw-card{position:absolute;background:rgba(255,255,255,.9);border:2px solid #eee6f0;border-radius:22px}
.olw-n{position:absolute;width:60px;height:60px;border-radius:50%;font:800 34px/60px 'Golos Text',sans-serif;text-align:center;color:#1f1a33}
.olw-d{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:10px;vertical-align:1px}
.olw-row b{font-weight:800}
</style>"""


def step(n, x, w, ncol, pill, title, ty, para, crop, cx, cw, cy=380, over=""):
    return ('<div class="step">' + '<div class="olw-card" style="left:%dpx;top:218px;width:%dpx;height:490px"></div>' % (x, w)
            + B(x + 8, 226, w - 16, 62, pill, 31)
            + '<div class="olw-n" style="left:%dpx;top:227px;background:%s">%d</div>' % (x + 14, ncol, n)
            + T(x + 84, ty, w - 86, 19.5, title, 800, lh=1.15, ex="white-space:nowrap;letter-spacing:-.01em")
            + T(x + 22, 296, w - 28, 16.5, para, 400, lh=1.24)
            + img(crop, "left:%dpx;top:%dpx;width:%dpx" % (cx, cy, cw)) + over + '</div>')


ROWS = [("Тип LSA", "#ffe1ec"), ("Link State ID", "#ddeeff"), ("Advertising Router", "#fff1c2"),
        ("Номер<br>последовательности", "#ffe1ec"), ("Контрольная сумма", "#ddeeff")]


def right():
    h = ['<div class="olw-card" style="left:1294px;top:212px;width:356px;height:508px"></div>',
         T(1312, 220, 220, 36, "Заголовок LSA", 700, f="Oswald", lh=1.1, ex="white-space:nowrap"),
         '<div class="ab" style="position:absolute;left:1312px;top:280px;width:320px;border-top:2px dashed #cfc6d6"></div>']
    for i, (t, c) in enumerate(ROWS):
        y = 292 + i * 60
        h.append(B(1308, y, 328, 54, c, 16))
        h.append(img("o_lsa_what_i%d.png" % (i + 1), "left:1312px;top:%dpx;height:54px" % y))
        h.append(T(1404, y + (15 if "<br>" not in t else 3), 230, 20, t, 800, lh=1.2, ex="class='olw-row'"))
    h.append(B(1308, 596, 328, 116, "#fff6d6", 16))
    h.append(img("o_lsa_what_bulb.png", "left:1314px;top:604px;width:44px"))
    h.append(T(1362, 600, 272, 15, "Значение <b>Link State ID</b> зависит от типа LSA: это может быть <b>Router ID</b>, "
               "адрес сети или адрес интерфейса DR. Оно не всегда содержит номер сети и маску.", 400, lh=1.32))
    note = ('<div class="ab" style="position:absolute;left:1528px;top:206px;width:120px;padding:6px 8px;background:#ffe36e;'
            'border-radius:8px;transform:rotate(-5deg);box-shadow:3px 4px 0 rgba(0,0,0,.08);font:600 12.5px/1.22 \'Golos Text\','
            'sans-serif;color:#1f1a33">LSA —<br>не запись<br>в таблице<br>маршрутизации. <span style="color:#ff4f9a">&#9829;</span></div>')
    return '<div class="step">' + "".join(h) + '</div><div class="step"><div>' + note + '</div></div>'


FACTS = ('<div class="ab" style="position:absolute;left:62px;top:586px;width:230px;height:118px;background:#fff;border:2.5px solid #9ec8f5;'
         'border-radius:12px;padding:8px 14px;font:500 17px/1.38 \'Golos Text\',sans-serif;color:#1f1a33">'
         '<b style="font-weight:800">LSA содержит факты:</b><br><i class="olw-d" style="background:#1f1a33"></i>о маршрутизаторе<br>'
         '<i class="olw-d" style="background:#2f8fe8"></i>о сети (транзитной)<br><i class="olw-d" style="background:#ffd23f"></i>о маршруте</div>')


def bars(y, c):
    return ('<i class="olw-d" style="position:absolute;left:1054px;top:%dpx;background:%s"></i>' % (y, c)
            + B(1080, y + 1, 72, 10, "#d9d6e0", 5) + B(1162, y + 1, 76, 10, "#d9d6e0", 5))


TOPO = (T(1062, 522, 150, 16, "Топология из LSA", 700, ex="text-align:center;background:#eef5ff;border-radius:12px;padding:2px 0")
        + '<div class="ab" style="position:absolute;left:1030px;top:578px;width:236px;height:122px;background:#fff;'
          'border:2.5px solid #2a2440;border-radius:8px"></div>'
        + B(1038, 584, 220, 26, "#e6f0ff", 6) + T(1038, 587, 220, 16, "Таблица маршрутизации", 700, ex="text-align:center")
        + bars(622, "#ff8fb8") + bars(645, "#4aa3f0") + bars(668, "#ffd23f"))

BAND = ('<div class="step"><div class="olw-card" style="left:22px;top:734px;width:1628px;height:192px"></div>'
        + img("o_lsa_what_band.png", "left:40px;top:740px;width:1605px")
        + '<div class="ab" style="position:absolute;left:30px;top:752px;width:13px;height:13px;border-radius:50%;background:#ff4f9a"></div>'
        + T(52, 748, 340, 34, "ПРИМЕР ТОПОЛОГИИ OSPF", 700, f="Oswald", lh=1.1, ex="white-space:nowrap;transform:scaleX(.86);transform-origin:0 0")
        + T(500, 758, 220, 19, "<b style='font-weight:700'>Обычная область</b><br>(Область 0.0.0.1)", 400, ex="text-align:center")
        + T(920, 756, 280, 16, "<b style='font-weight:700;font-size:18px'>Area 0</b><br><b style='font-weight:700'>(Область 0.0.0.0 - магистраль)</b>", 400, ex="text-align:center")
        + T(1335, 758, 220, 19, "<b style='font-weight:700'>Другая область</b><br>(Область 0.0.0.5)", 400, ex="text-align:center")
        + T(95, 832, 150, 18, "<b style='font-weight:700'>Внешняя сеть</b><br>например, ISP", 400, ex="text-align:center")
        + T(335, 885, 80, 22, "ASBR", 700, ex="text-align:center")
        + T(770, 885, 80, 22, "ABR", 700, ex="text-align:center")
        + T(1233, 885, 80, 22, "ABR", 700, ex="text-align:center") + '</div>')

FACTS = ('<div class="ab" style="position:absolute;left:62px;top:586px;width:230px;height:118px;background:#fff;border:2.5px solid #9ec8f5;'
         'border-radius:12px;padding:8px 14px;font:500 17px/1.38 \'Golos Text\',sans-serif;color:#1f1a33">'
         '<b style="font-weight:800">LSA содержит факты:</b><br><i class="olw-d" style="background:#1f1a33"></i>о маршрутизаторе<br>'
         '<i class="olw-d" style="background:#2f8fe8"></i>о сети (транзитной)<br><i class="olw-d" style="background:#ffd23f"></i>о маршруте</div>')


def bars(y, c):
    return ('<i class="olw-d" style="position:absolute;left:1054px;top:%dpx;background:%s"></i>' % (y, c)
            + B(1080, y + 1, 72, 10, "#d9d6e0", 5) + B(1162, y + 1, 76, 10, "#d9d6e0", 5))


TOPO = (T(1062, 522, 150, 16, "Топология из LSA", 700, ex="text-align:center;background:#eef5ff;border-radius:12px;padding:2px 0")
        + '<div class="ab" style="position:absolute;left:1030px;top:578px;width:236px;height:122px;background:#fff;'
          'border:2.5px solid #2a2440;border-radius:8px"></div>'
        + B(1038, 584, 220, 26, "#e6f0ff", 6) + T(1038, 587, 220, 16, "Таблица маршрутизации", 700, ex="text-align:center")
        + bars(622, "#ff8fb8") + bars(645, "#4aa3f0") + bars(668, "#ffd23f"))

BAND = ('<div class="step"><div class="olw-card" style="left:22px;top:734px;width:1628px;height:192px"></div>'
        + img("o_lsa_what_band.png", "left:40px;top:740px;width:1605px")
        + '<div class="ab" style="position:absolute;left:30px;top:752px;width:13px;height:13px;border-radius:50%;background:#ff4f9a"></div>'
        + T(52, 748, 340, 34, "ПРИМЕР ТОПОЛОГИИ OSPF", 700, f="Oswald", lh=1.1, ex="white-space:nowrap;transform:scaleX(.86);transform-origin:0 0")
        + T(500, 758, 220, 19, "<b style='font-weight:700'>Обычная область</b><br>(Область 0.0.0.1)", 400, ex="text-align:center")
        + T(920, 756, 280, 16, "<b style='font-weight:700;font-size:18px'>Area 0</b><br><b style='font-weight:700'>(Область 0.0.0.0 - магистраль)</b>", 400, ex="text-align:center")
        + T(1335, 758, 220, 19, "<b style='font-weight:700'>Другая область</b><br>(Область 0.0.0.5)", 400, ex="text-align:center")
        + T(95, 832, 150, 18, "<b style='font-weight:700'>Внешняя сеть</b><br>например, ISP", 400, ex="text-align:center")
        + T(335, 885, 80, 22, "ASBR", 700, ex="text-align:center")
        + T(770, 885, 80, 22, "ABR", 700, ex="text-align:center")
        + T(1233, 885, 80, 22, "ABR", 700, ex="text-align:center") + '</div>')

HTML = CSS + bg("bg7", W, H) + "".join([
    step(1, 30, 316, "#ff7aa8", "#ffe1ec", "Маршрутизатор<br>формирует LSA", 233,
         "Создает объявление о своих линках, сети или маршруте.", "o_lsa_what_c1.png", 32, 313, over=FACTS),
    step(2, 352, 312, "#5aaaf2", "#ddeeff", "LSU переносит LSA", 244,
         "LSA упаковывается в&nbsp;LSU (Link State Update) и рассылается соседям по OSPF.", "o_lsa_what_c2.png", 345, 345, 386),
    step(3, 672, 306, "#ffd23f", "#fff1c2", "Маршрутизатор<br>сохраняет LSA в LSDB", 233,
         "Полученные LSA проверяются и сохраняются в базе данных состояния каналов (LSDB).", "o_lsa_what_c3.png", 690, 295, 368),
    step(4, 990, 290, "#ff7aa8", "#ffe1ec", "SPF рассчитывает<br>маршруты", 233,
         "На основе LSDB строится топология, выполняется алгоритм SPF, и формируется таблица маршрутизации.",
         "o_lsa_what_c4.png", 985, 300, over=TOPO),
    right(), BAND])
