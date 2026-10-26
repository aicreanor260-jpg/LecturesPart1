# -*- coding: utf-8 -*-
"""Алгоритм Дейкстры: второй шаг — соседи R2 (метка 8), R4 получает 24, R2 посещена."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.os2-sub{position:absolute;left:48px;top:152px;font:600 36px/1.1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.os2-lb{position:absolute;border-radius:12px;text-align:center;font:600 18px/1.15 "Golos Text",sans-serif;color:#1f1a33;padding:4px 8px;white-space:nowrap}
.os2-lb b{display:block;font:800 28px/1 "Golos Text",sans-serif;color:#ff2e7a}
.os2-w{position:absolute;font:600 27px/1 "Golos Text",sans-serif;color:#1f1a33;background:rgba(240,246,255,.9);border-radius:6px;padding:1px 3px}
.os2-col{position:absolute;background:rgba(255,255,255,.96);border:2px solid #efe6ee;border-radius:24px}
.os2-hd{position:absolute;padding:8px 18px;border-radius:14px;font:700 26px/1.1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.os2-c{position:absolute;left:778px;width:448px;border-radius:20px}
.os2-tg{position:absolute;padding:4px 12px;border-radius:12px;background:#ffc6dd;font:800 24px/1.1 "Golos Text",sans-serif;color:#1f1a33}
.os2-t{position:absolute;font:500 20px/1.2 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.os2-t i{font-weight:600}
.os2-k{position:absolute;left:1082px;width:132px;border-radius:12px;text-align:center;font:500 15px/1.2 "Golos Text",sans-serif;color:#1f1a33;padding:5px 0}
.os2-k b{display:block;font:800 25px/1.05 "Golos Text",sans-serif}
.os2-tb{position:absolute;left:1262px;top:226px;border-collapse:collapse;font:700 17px/1 "Golos Text",sans-serif;color:#1f1a33}
.os2-tb th{height:38px;font-weight:700}
.os2-tb td{height:72px;border-top:2px solid #f0eef4;text-align:center;font:600 22px/1 "Golos Text",sans-serif}
.os2-tb td.n{text-align:left;padding-left:88px;font-weight:600}
.os2-bub{position:absolute;left:1300px;top:648px;width:345px;height:110px;background:rgba(255,226,238,.97);border-radius:20px}
</style>"""


def lb(x, y, w, big, small, c):
    return '<div class="os2-lb" style="left:%dpx;top:%dpx;width:%dpx;background:%s"><b>%s</b>%s</div>' % (x, y, w, c, big, small)


def wt(x, y, t):
    return '<div class="os2-w" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


def tg(x, y, t):
    return '<div class="os2-tg" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


def t(x, y, s, extra=""):
    return '<div class="os2-t" style="left:%dpx;top:%dpx;%s">%s</div>' % (x, y, extra, s)


def k(y, small, big, c):
    return '<div class="os2-k" style="top:%dpx;background:%s">%s<b>%s</b></div>' % (y, c, small, big)


INF = '<span style="font:900 34px/26px Arial">∞</span>'
ROWS = [("R1", "0", "посещена", "#d8f5dc", 700), ("R2", "8", "посещена", "#d8f5dc", 700), ("R3", "10", "не посещена", "", 500),
        ("R4", "24", "не посещена", "", 500), ("R5", "15", "не посещена", "", 500)]
TABLE = ('<table class="os2-tb"><tr><th style="width:158px">Маршрутизатор</th><th style="width:82px">Метка</th><th style="width:136px">Статус</th></tr>'
         + "".join('<tr><td class="n">%s</td><td>%s</td><td style="font-size:17px;font-weight:%d;background:%s">%s</td></tr>'
                   % (r, m, fw, c or "transparent", st) for r, m, st, c, fw in ROWS) + '</table>'
         + "".join(img("o_dij_s2_t%d.png" % (i + 1), "left:1272px;top:%dpx;width:78px" % (278 + 72 * i)) for i in range(5)))

HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="os2-sub">Проверяем соседей R2 с меткой 8</div>',
    '<div class="step">' + img("o_dij_s2_g.png", "left:25px;top:205px;width:737px;border-radius:24px")
    + wt(370, 320, "15") + wt(264, 404, "10") + wt(503, 405, "3") + wt(124, 492, "8") + wt(645, 498, "16")
    + wt(249, 570, "11") + wt(499, 578, "12") + wt(372, 671, "16")
    + lb(95, 242, 130, "0", "посещена", "#ffd6e6") + lb(568, 238, 136, "15", "не посещена", "#d6eafc")
    + lb(330, 413, 136, "10", "не посещена", "#ffd6e6") + lb(573, 593, 132, INF, "не посещена", "#d6eafc")
    + lb(92, 575, 128, "8", "текущая", "#ffe14d") + '</div>',
    '<div class="os2-col" style="left:768px;top:180px;width:470px;height:742px"></div>'
    '<div class="os2-hd" style="left:780px;top:194px;background:#ffe14d">Проверяем каждого соседа R2</div>',
    '<div class="step"><div class="os2-c" style="top:252px;height:126px;background:#ffe6ef"></div>'
    + img("o_dij_s2_r1.png", "left:790px;top:272px;width:102px") + tg(904, 266, "R1") + tg(983, 266, "8")
    + t(905, 312, "R1 уже посещена —<br>пропускаем.") + '</div>',
    '<div class="step"><div class="os2-c" style="top:390px;height:205px;background:#e6f1fc"></div>'
    + img("o_dij_s2_r3.png", "left:790px;top:410px;width:102px") + tg(904, 404, "R3")
    + t(905, 452, "<i>8 + 11 = 19</i>", "font-size:24px") + t(905, 488, "Текущая метка 10<br>меньше 19 —<br>оставляем 10.")
    + k(412, "Кандидат:", "19", "#e6e6ea") + k(474, "Текущая:", "10", "#ffd6e6")
    + '<div class="os2-k" style="top:532px;background:#dcf5df;padding-left:42px;text-align:left">Оставляем<b>10</b></div>'
    + img("o_dij_s2_ok2.png", "left:1085px;top:537px;width:36px") + '</div>',
    '<div class="step"><div class="os2-c" style="top:607px;height:188px;background:#fff7d6"></div>'
    + img("o_dij_s2_r4.png", "left:790px;top:628px;width:102px") + tg(904, 622, "R4")
    + t(905, 670, "<i>8 + 16 = 24</i>", "font-size:24px") + t(905, 706, "24 меньше ∞ —<br>устанавливаем<br>метку 24.")
    + k(626, "Было:", INF, "#e6e6ea") + '<div class="os2-t" style="left:1142px;top:690px">↓</div>'
    + k(712, "Стало:", "24", "#ffe14d") + '</div>',
    '<div class="step"><div class="os2-c" style="top:808px;height:105px;background:#e8f7ea"></div>'
    + img("o_dij_s2_r2.png", "left:785px;top:820px;width:97px") + img("o_dij_s2_ok.png", "left:885px;top:825px;width:55px")
    + t(948, 832, "<b>Помечаем R2 как посещённую.</b>", "font-size:19px")
    + t(948, 864, "Все соседи R2 проверены.", "font-size:16px") + img("o_dij_s2_arr.png", "left:1172px;top:860px;width:38px") + '</div>',
    '<div class="step"><div class="os2-col" style="left:1250px;top:148px;width:400px;height:488px"></div>'
    '<div class="os2-hd" style="left:1262px;top:158px;width:376px;background:#ff8fbd;font-size:34px;padding:8px 14px">Метки после шага 2</div>'
    + TABLE + '</div>',
    '<div class="step">' + img("o_dij_s2_art.png", "left:1245px;top:760px;width:417px")
    + '<div class="os2-bub"></div>' + img("o_dij_s2_bulb.png", "left:1300px;top:648px;width:65px")
    + t(1373, 660, "На втором шаге мы<br>обновили метку для R4,<br>используя путь через R2,<br>и пометили R2 как посещенную.",
        "font-size:16.5px") + '</div>',
])
