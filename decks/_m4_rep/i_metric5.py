# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 146

CSS = """<style>
.m4x-m5-p{position:absolute;box-sizing:border-box;border:1.5px solid rgba(217,180,90,.85);border-radius:20px;
  background:rgba(7,38,32,.93);box-shadow:0 0 16px rgba(240,199,94,.28),inset 0 0 24px rgba(240,199,94,.06)}
.m4x-m5-h{position:absolute;text-align:center;font:700 33px/1.3 "Playfair Display",serif;white-space:nowrap;
  background:linear-gradient(180deg,#fff0b0,#e0b04a 60%,#b98a2e);-webkit-background-clip:text;background-clip:text;color:transparent}
.m4x-m5-t{position:absolute;text-align:center;font:400 24px/30px "Playfair Display",serif;color:#f1ead0;white-space:nowrap}
.m4x-m5-d{position:absolute;width:11px;height:11px;border-radius:50%;background:#f0c75e;box-shadow:0 0 10px #f0c75e;margin:-5px 0 0 -5px}
.m4x-m5-sv *{fill:none}
.m4x-m5-sv .g{stroke:#e9b94f;stroke-width:2.2}
.m4x-m5-sv .t{stroke:#3fd6b0;stroke-width:2.5;filter:drop-shadow(0 0 4px #3fd6b0)}
</style>"""


def panel(x1, y1, x2, y2, title, tx, txt, ty, lines, cx):
    return ('<div class="m4x-m5-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
            '<div class="m4x-m5-h" style="left:%dpx;top:%dpx;width:%dpx;margin-left:-%dpx">%s</div>'
            '<svg style="position:absolute;left:%dpx;top:%dpx" width="180" height="14" viewBox="0 0 180 14"><path d="M0 7H80M100 7H180" stroke="rgba(217,180,90,.5)" stroke-width="1"/>'
            '<path d="M90 2l5 5-5 5-5-5z" fill="#e9b94f"/></svg>'
            '<div class="m4x-m5-t" style="left:%dpx;top:%dpx;width:%dpx;margin-left:-%dpx">%s</div>'
            % (x1, y1, x2 - x1, y2 - y1, cx, y1 + 18, 480, 240, title, cx - 90, y1 + 62, cx, ty, 480, 240, txt))


def dot(x, y):
    return '<div class="m4x-m5-d" style="left:%dpx;top:%dpx"></div>' % (x, y)


def svg(body):
    return '<svg class="m4x-m5-sv" style="position:absolute;left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941">%s</svg>' % body


def plus(x, y):
    return ('<circle cx="%d" cy="%d" r="17" fill="#0a2a24" stroke="#e9b94f" stroke-width="2.5"/>'
            '<path d="M%d %dh16M%d %dv16" stroke="#f0c75e" stroke-width="3"/>' % (x, y, x - 8, y, x, y - 8))


p1 = svg('<path class="g" d="M180 342L221 310M180 342L221 360M221 310L268 295M221 360L268 378M352 290L398 310M352 380L398 360M398 310L446 333M398 360L446 337"/>')
p1 += dot(221, 310) + dot(221, 360) + dot(398, 310) + dot(398, 360)
p2 = svg('<path class="t" d="M716 322L738 289H938L962 322M716 335H962M716 350L738 377H938L962 350M738 333H938"/>'
         + plus(837, 289) + plus(837, 333) + plus(837, 377))
p2 += dot(738, 289) + dot(938, 289) + dot(738, 333) + dot(938, 333) + dot(738, 377) + dot(938, 377)
p3 = svg('<path class="t" d="M1253 334H1326M1422 334H1494"/>') + dot(1281, 334) + dot(1466, 334)
p4 = svg('<path class="t" d="M270 660H398M490 660H618"/>') + dot(298, 660) + dot(368, 660) + dot(520, 660) + dot(589, 660)

R = lambda n, x, y: img("i_metric5_%s.png" % n, "left:%dpx;top:%dpx" % (x, y))

HTML = CSS + bg() + "".join([
    '<div class="step">' + panel(55, 167, 566, 503, "1. Длина маршрута", 0, "Число переходов между<br>маршрутизаторами", 427, 0, 310)
    + p1 + R("r11", 90, 306) + R("r12", 266, 258) + R("r13", 266, 352) + R("r14", 440, 306) + '</div>',
    '<div class="step">' + panel(589, 167, 1096, 503, "2. Стоимость", 0, "Сумма назначенных<br>стоимостей каналов", 427, 0, 842)
    + p2 + R("r21", 614, 294) + R("r22", 956, 294) + '</div>',
    '<div class="step">' + panel(1124, 167, 1622, 503, "3. Надёжность", 0, "Устойчивость и доступность<br>канала", 427, 0, 1374)
    + p3 + R("r31", 1152, 294) + R("r32", 1490, 294) + R("shield", 1322, 272) + '</div>',
    '<div class="step">' + panel(55, 523, 826, 799, "4. Задержка", 0, "Время доставки пакета<br>до узла назначения", 722, 0, 440)
    + p4 + R("r41", 166, 616) + R("r42", 612, 616) + R("watch", 392, 598) + '</div>',
    '<div class="step">' + panel(848, 523, 1622, 799, "5. Полоса пропускания", 0, "Максимальная скорость<br>передачи по каналу", 724, 0, 1240)
    + R("r51", 946, 616) + R("r52", 1426, 616) + R("tube", 1060, 618) + '</div>',
    '<div class="step"><div class="m4x-m5-p" style="left:55px;top:820px;width:1567px;height:76px;border-radius:14px;background:rgba(7,38,32,.9)"></div>'
    '<div class="m4x-m5-t" style="left:55px;top:840px;width:1567px;font-size:22.5px;letter-spacing:.2px">'
    'Метрика может учитывать одну или несколько характеристик пути. Правила расчёта зависят от протокола маршрутизации.</div></div>',
])
