# -*- coding: utf-8 -*-
"""Алгоритм Дейкстры: третий шаг — R3 (10), обновляем R4 до 22 и R5 до 13; следующая R5."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 148

CSS = """<style>
.os3-sub{position:absolute;left:64px;top:150px;font:600 31px/1.15 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.os3-b{position:absolute;height:44px;min-width:50px;padding:0 9px;border-radius:12px;font:700 29px/44px "Golos Text",sans-serif;color:#1f1a33;text-align:center}
.os3-w{position:absolute;width:48px;height:48px;border-radius:50%;border:2px solid #fff;font:700 26px/44px "Golos Text",sans-serif;color:#1f1a33;text-align:center}
.os3-ar{position:absolute;font:800 24px/44px "Golos Text",sans-serif;color:#ff2e7a}
.os3-pan{position:absolute;left:1018px;top:192px;width:620px;height:478px;background:rgba(255,255,255,.95);border:2px solid #f1e6ee;border-radius:24px}
.os3-hd{position:absolute;left:1105px;top:150px;padding:9px 22px;background:#ffe14d;border-radius:16px;font:700 27px/1.1 "Golos Text",sans-serif;color:#1f1a33}
.os3-r{position:absolute;left:1035px;width:585px;border-radius:18px}
.os3-t{position:absolute;font:500 20px/1.35 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.os3-t i,.os3-t u{font-style:normal;text-decoration:none;border-radius:6px;padding:0 5px}
.os3-t i{background:#ffd6e6}.os3-t u{background:#ffe58a}
.os3-eq{position:absolute;left:1190px;font:700 26px/40px "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.os3-eq span{display:inline-block;padding:0 10px;border-radius:12px;margin:0 6px}
.os3-bar{position:absolute;left:42px;top:778px;width:945px;height:135px;background:#feef87;border-radius:26px}
.os3-tb{position:absolute;left:1036px;top:722px;border-collapse:collapse;font:500 15px/1 "Golos Text",sans-serif;color:#1f1a33}
.os3-tb th{height:26px;font-weight:700;background:#e6f1fc;border-right:2px solid #fff}
.os3-tb td{height:29px;text-align:center;border-top:1px solid #eee;border-right:1px solid #eee}
.os3-tb td span{display:inline-block;min-width:30px;background:#ffd6e6;border-radius:6px;font-size:17px;padding:2px 0}
</style>"""


def b(x, y, t, c):
    return '<div class="os3-b" style="left:%dpx;top:%dpx;background:%s">%s</div>' % (x, y, c, t)


def w(x, y, t, c="#d6eafc"):
    return '<div class="os3-w" style="left:%dpx;top:%dpx;background:%s">%s</div>' % (x, y, c, t)


def eq(y, a, bb, r):
    return ('<div class="os3-eq" style="top:%dpx"><span style="background:#ffd6e6;margin-left:0">%s</span>+<span style="background:#d6eafc">%s</span>'
            '=<span style="background:#ffe14d">%s</span></div>' % (y, a, bb, r))


ROWS = [("R1", "0", 1, "Посещён"), ("R2", "8", 1, "Посещён"), ("R3", "10", 1, "Посещён"), ("R4", "22", 0, "Не посещён"),
        ("R5", "13", 0, "Не посещён")]
TABLE = ('<table class="os3-tb"><tr><th style="width:172px">Маршрутизатор</th><th style="width:205px">Метка (расстояние)</th>'
         '<th style="width:210px">Статус</th></tr>'
         + "".join('<tr style="background:%s"><td>%s</td><td><span>%s</span></td><td style="text-align:left;padding-left:82px">%s</td></tr>'
                   % ("#fff3b8" if r == "R3" else "#fff", r, m, st) for r, m, ok, st in ROWS) + '</table>'
         + "".join(img("o_dij_s3_%s.png" % ("ck" if i < 3 else "cr"), "left:1435px;top:%dpx;width:27px" % (751 + 29.6 * i))
                   for i in range(5)))

HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="os3-sub">Выбираем R3 с меткой 10 и пересчитываем пути к соседям</div>',
    '<div class="step">' + img("o_dij_s3_g.png", "left:42px;top:205px;width:948px;border-radius:26px")
    + w(489, 282, "15") + w(320, 374, "10") + w(154, 448, "8") + w(325, 531, "11") + w(489, 631, "16") + w(824, 448, "16")
    + b(152, 223, "0", "#ffd6e6") + b(150, 557, "8", "#ffd6e6") + b(476, 371, "10", "#ffe14d") + '</div>',
    '<div class="step">' + w(654, 362, "3", "#fff3a0") + w(654, 527, "12", "#fff3a0")
    + b(790, 223, "15", "#ffd6e6") + '<div class="os3-ar" style="left:850px;top:223px">→</div>' + b(878, 223, "13", "#ffe14d")
    + b(790, 555, "24", "#ffd6e6") + '<div class="os3-ar" style="left:850px;top:555px">→</div>' + b(878, 555, "22", "#ffe14d") + '</div>',
    '<div class="os3-pan"></div><div class="os3-hd">Проверяем соседей R3</div>',
    '<div class="step"><div class="os3-r" style="top:205px;height:85px;background:#ffe3ee"></div>'
    + img("o_dij_s3_r12.png", "left:1055px;top:215px;width:215px")
    + '<div class="os3-t" style="left:1290px;top:218px"><b>R1 и R2 уже посещены</b> —<br>пропускаем.</div></div>',
    '<div class="step"><div class="os3-r" style="top:300px;height:130px;background:#e3f0fc"></div>'
    + img("o_dij_s3_r4.png", "left:1055px;top:325px;width:100px") + eq(314, "10", "12", "22")
    + '<div class="os3-t" style="left:1196px;top:362px">22 меньше <i>24</i> — обновляем<br>метку <b>R4</b> до <u>22</u></div></div>',
    '<div class="step"><div class="os3-r" style="top:442px;height:130px;background:#e3f0fc"></div>'
    + img("o_dij_s3_r5.png", "left:1055px;top:465px;width:100px") + eq(456, "10", "3", "13")
    + '<div class="os3-t" style="left:1196px;top:504px">13 меньше <i>15</i> — обновляем<br>метку <b>R5</b> до <u>13</u></div></div>',
    '<div class="step"><div class="os3-r" style="top:584px;height:78px;background:#ffe3ee"></div>'
    + img("o_dij_s3_r3.png", "left:1050px;top:585px;width:130px")
    + '<div class="os3-t" style="left:1196px;top:596px;line-height:1.2">После проверки соседей <b>помечаем R3</b><br><b>как посещённую.</b></div></div>',
    '<div class="step"><div class="os3-pan" style="top:682px;height:228px"></div>'
    '<div class="os3-t" style="left:1045px;top:686px;font:700 24px/1.4 \'Golos Text\',sans-serif">Метки после шага 3</div>' + TABLE + '</div>',
    '<div class="step"><div class="os3-bar"></div>' + img("o_dij_s3_flag.png", "left:60px;top:795px;width:115px")
    + img("o_dij_s3_arr.png", "left:785px;top:795px;width:175px")
    + '<div class="os3-t" style="left:187px;top:808px;font:700 31px/1.2 \'Golos Text\',sans-serif">Следующая вершина – R5, метка 13.</div>'
    '<div class="os3-t" style="left:187px;top:852px;font-size:22px">Среди непосещённых минимальная метка у R5 (13).</div></div>',
])
