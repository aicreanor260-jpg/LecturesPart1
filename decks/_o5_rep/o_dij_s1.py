# -*- coding: utf-8 -*-
"""Алгоритм Дейкстры: первый шаг — старт из R1, метки соседей R2, R3, R5.
Левая колонка поднята на 100px: в оригинале там двухстрочный заголовок, который даёт слайд."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 165
DY = -100  # сдвиг левой колонки

CSS = """<style>
.os1-sub{position:absolute;left:55px;font:700 31px/1.12 "Golos Text",sans-serif;color:#1f1a33}
.os1-box{position:absolute;border-radius:24px}
.os1-row{position:absolute;left:62px;width:450px;height:88px;background:#fff;border-radius:20px}
.os1-f{position:absolute;left:175px;font:700 31px/1.08 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.os1-f b{color:#ff4f9a;font-size:36px}
.os1-lb{position:absolute;background:#ffe0ec;border-radius:16px;text-align:center;font:600 18px/1.1 "Golos Text",sans-serif;color:#c2134d;padding:6px 6px;white-space:nowrap}
.os1-lb b{display:block;font:800 40px/1 "Golos Text",sans-serif}
.os1-w{position:absolute;background:#fff;border-radius:6px;padding:0 4px;font:600 28px/1.1 "Golos Text",sans-serif;color:#1f1a33}
.os1-h{position:absolute;font:700 40px/1 Oswald,sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.86);transform-origin:0 0}
.os1-t{position:absolute;font:500 22px/1.4 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.os1-t i{font-style:normal;background:#ffc6dd;border-radius:6px;padding:0 6px;color:#c2134d;font-weight:800}
.os1-t em{font-style:normal;color:#ff4f9a;font-weight:800;font-size:26px}
</style>"""


def row(y, name, f, v):
    y += DY
    return ('<div class="os1-row" style="top:%dpx"></div>%s<div class="os1-f" style="top:%dpx">%s:<br>%s = <b>%s</b></div>'
            % (y, img("o_dij_s1_ar.png", "left:70px;top:%dpx;width:85px" % (y + 4)), y + 8, name, f, v))


def lb(x, y, w, big, small):
    return '<div class="os1-lb" style="left:%dpx;top:%dpx;width:%dpx"><b>%s</b>%s</div>' % (x, y, w, big, small)


def wt(x, y, t):
    return '<div class="os1-w" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="os1-sub" style="top:%dpx">Стартуем из R1 и обновляем<br>метки соседей</div>' % (290 + DY),
    '<div class="step">' + img("o_dij_s1_g.png", "left:560px;top:160px;width:1105px")
    + wt(1012, 270, "15") + wt(880, 360, "10") + wt(1210, 366, "3") + wt(638, 444, "8") + wt(1424, 456, "16")
    + wt(886, 553, "11") + wt(1198, 551, "12") + wt(1042, 644, "16") + '</div>',
    '<div class="step">' + lb(648, 172, 140, "0", "(посещена)") + '</div>',
    '<div class="step"><div class="os1-box" style="left:48px;top:%dpx;width:480px;height:385px;background:#ffe3ee"></div>'
    '<div class="os1-t" style="left:66px;top:%dpx;font-weight:700;font-size:24px;line-height:1.15">: Вычисляем новые метки<br>&nbsp;&nbsp;для соседей R1</div>'
    % (372 + DY, 384 + DY) + row(452, "R2", "0 + 8", "8") + lb(672, 528, 150, "8", "(следующая)") + '</div>',
    '<div class="step">' + row(553, "R3", "0 + 10", "10") + lb(985, 365, 152, "10", "(не посещена)") + '</div>',
    '<div class="step">' + row(656, "R5", "0 + 15", "15") + lb(1325, 172, 148, "15", "(не посещена)")
    + lb(1365, 528, 150, "<span style=\"font-size:52px\">∞</span>", "(не посещена)") + '</div>',
    '<div class="step"><div class="os1-box" style="left:40px;top:772px;width:695px;height:145px;background:#dcecfb"></div>'
    + img("o_dij_s1_bulb.png", "left:55px;top:790px;width:120px") + img("o_dij_s1_dec.png", "left:590px;top:775px;width:50px")
    + '<div class="os1-h" style="left:195px;top:792px">Правило обновления метки</div>'
    '<div class="os1-t" style="left:195px;top:840px;font-size:23px;line-height:1.35">Метка соседа меняется, если<br>новый путь короче текущего.</div>'
    + img("o_dij_s1_to.png", "left:735px;top:820px;width:60px") + '</div>',
    '<div class="step"><div class="os1-box" style="left:792px;top:772px;width:845px;height:145px;background:#ffe3ee"></div>'
    + img("o_dij_s1_ok.png", "left:815px;top:790px;width:120px")
    + '<div class="os1-h" style="left:955px;top:792px">Итог первого шага</div>'
    '<div class="os1-t" style="left:955px;top:838px">После проверки соседей помечаем <i>R1</i> как посещённую.<br>'
    'Следующая вершина — <i>R2</i> : её метка &nbsp;<em>8</em>&nbsp; минимальна.</div></div>',
])
