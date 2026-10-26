# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 100

CSS = """<style>
.m4x-trm-p{position:absolute;box-sizing:border-box;border:1.5px solid rgba(240,199,94,.55);border-radius:24px;
  background:linear-gradient(180deg,rgba(14,70,52,.55),rgba(5,32,24,.8));box-shadow:0 0 22px rgba(240,199,94,.18),inset 0 0 40px rgba(0,0,0,.35)}
.m4x-trm-h{position:absolute;text-align:center;font:800 34px/1 "Playfair Display",serif;white-space:nowrap;
  background:linear-gradient(180deg,#fff0b8,#e8b84a 55%,#b88a2a);-webkit-background-clip:text;background-clip:text;color:transparent}
.m4x-trm-t{position:absolute;text-align:center;font:500 25px/30px "Golos Text",sans-serif;color:#f1ead2}
.m4x-trm-sub{position:absolute;left:0;width:1672px;top:105px;text-align:center;font:500 28px/34px "Golos Text",sans-serif;color:#f1ead2}
.m4x-trm-dia{position:absolute;width:10px;height:10px;background:#f0c75e;transform:rotate(45deg);box-shadow:0 0 8px #f0c75e}
.m4x-trm-ln{position:absolute;height:1px;background:linear-gradient(90deg,transparent,rgba(240,199,94,.6),transparent)}
.m4x-trm-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.m4x-trm-sv .g{fill:none;stroke:#e8b84a;stroke-width:2.5}
.m4x-trm-sv .d{fill:#f0c75e}
.m4x-trm-sv .tl{fill:none;stroke:#3fd6b0;stroke-width:2.5;stroke-dasharray:7 6;animation:m4xtrm 1.2s linear infinite}
@keyframes m4xtrm{to{stroke-dashoffset:-26}}
</style>"""


def panel(x, y, w, h, r=24):
    return '<div class="m4x-trm-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:%dpx"></div>' % (x, y, w, h, r)


def head(cx, y, title, half=300):
    return ('<div class="m4x-trm-h" style="left:%dpx;width:700px;margin-left:-350px;top:%dpx">%s</div>'
            '<div class="m4x-trm-ln" style="left:%dpx;top:%dpx;width:%dpx"></div><div class="m4x-trm-dia" style="left:%dpx;top:%dpx"></div>'
            % (cx, y, title, cx - half, y + 52, 2 * half, cx - 5, y + 47))


def im(n, x, y, w):
    return img("i_terms_%s.png" % n, "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


def text(cx, y, s, w=700):
    return '<div class="m4x-trm-t" style="left:%dpx;width:%dpx;margin-left:-%dpx;top:%dpx">%s</div>' % (cx, w, w // 2, y, s)


def svg(body):
    return '<svg class="m4x-trm-sv" viewBox="0 0 1672 941">' + body + '</svg>'


def dots(pts, r=5):
    return "".join('<circle class="d" cx="%d" cy="%d" r="%d"/>' % (x, y, r) for x, y in pts)


A = ('<div class="step">' + panel(52, 162, 774, 331) + head(439, 176, "1. Окончательный маршрут")
     + im("a1", 130, 275, 145) + im("a2", 607, 275, 143)
     + svg('<path class="g" d="M268 321H475M505 321H612"/>'
           '<line x1="372" y1="321" x2="470" y2="321" stroke="#3fd6b0" stroke-width="3.5" style="filter:drop-shadow(0 0 5px #3fd6b0)"/>'
           '<path d="M468 308L492 321L468 334z" fill="#3fd6b0"/>' + dots([(300, 321), (373, 321), (510, 321), (583, 321)]))
     + text(439, 412, "Содержит следующий узел<br>или выходной интерфейс") + '</div>')

B = ('<div class="step">' + panel(846, 162, 775, 331) + head(1233, 176, "2. Маршрут 1-го уровня")
     + im("b0", 1178, 242, 114) + im("b1", 985, 335, 110) + im("b2", 1180, 335, 110) + im("b3", 1375, 335, 110)
     + svg('<path class="g" d="M1185 307H1041V328M1285 307H1429V328M1235 312V330"/>' + dots([(1151, 307), (1318, 307), (1041, 330), (1235, 330), (1429, 330)], 5))
     + text(1233, 426, "Префикс совпадает с классовой сетью<br>или является суперсетью") + '</div>')

C = ('<div class="step">' + panel(52, 514, 774, 316) + head(439, 530, "3. Родительский маршрут 1-го уровня")
     + im("c0", 378, 592, 124) + im("c1", 143, 680, 107) + im("c2", 320, 680, 107) + im("c3", 633, 680, 107)
     + svg('<path class="g" d="M385 656H197V678M495 656H688V678M373 656V678"/>' + dots([(311, 656), (570, 656), (197, 678), (373, 678), (688, 678)], 5)
           + '<path class="tl" d="M427 715H495M555 715H635"/><g fill="#3fd6b0"><circle cx="505" cy="715" r="6"/><circle cx="525" cy="715" r="6"/><circle cx="545" cy="715" r="6"/></g>')
     + text(439, 761, "Объединяет дочерние подсети;<br>сам не задаёт следующий узел") + '</div>')

D = ('<div class="step">' + panel(846, 514, 775, 316) + head(1233, 530, "4. Дочерний маршрут 2-го уровня")
     + im("d0", 1180, 595, 110) + im("d1", 965, 683, 102) + im("d2", 1155, 680, 160) + im("d3", 1403, 683, 102)
     + svg('<path d="M1190 636Q1100 660 1017 660V676M1280 636Q1370 660 1455 660V676" fill="none" stroke="#e8b84a" stroke-width="2.5" stroke-dasharray="8 6"/>'
           + dots([(1017, 678), (1455, 678)], 5) + '<circle cx="1235" cy="681" r="6" fill="#3fd6b0" style="filter:drop-shadow(0 0 6px #3fd6b0)"/>'
           '<ellipse cx="1235" cy="730" rx="72" ry="28" fill="none" stroke="#3fd6b0" stroke-width="2" opacity=".8" style="filter:drop-shadow(0 0 6px #3fd6b0)"/>'
           '<path class="tl" d="M1082 717H1160M1310 717H1420"/><g fill="#3fd6b0"><circle cx="1116" cy="717" r="5"/><circle cx="1355" cy="717" r="5"/></g>')
     + text(1233, 782, "Подсеть внутри родительского маршрута") + '</div>')

LINK = ('<div class="step">' + svg('<path class="g" d="M1235 493V522"/>' + dots([(1235, 495), (1235, 521)], 5)) + '</div>')

FOOT = ('<div class="step">' + panel(56, 849, 1562, 55, 20)
        + '<div class="m4x-trm-t" style="left:56px;width:1562px;top:861px;font-size:30px;line-height:32px">Таблица маршрутизации — иерархическая база данных для быстрого поиска пути.</div></div>')

HTML = CSS + bg() + '<div class="m4x-trm-sub">Иерархия записей ускоряет поиск маршрута и пересылку пакетов</div>' + "".join([A, B, C, D, LINK, FOOT])
