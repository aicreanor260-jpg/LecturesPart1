# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _k import css, box, tx, step, svg, path
W, H, TOP = 1672, 941, 150
P = "m4x-pr"
CSS = css(P) + """<style>
.m4x-pr-num{position:absolute;width:90px;height:90px;border-radius:50%;box-sizing:border-box;border:3px solid #f0c75e;
 background:radial-gradient(#0b2a22,#04140f);box-shadow:0 0 16px rgba(240,199,94,.6),inset 0 0 12px rgba(240,199,94,.3);font:800 58px/82px "Playfair Display",serif;font-variant-numeric:lining-nums;color:#fff0b8;text-align:center}
.m4x-pr-q{position:absolute;font:600 25px/1.2 "Playfair Display",serif;font-variant-numeric:lining-nums;color:#f6ebc8;text-shadow:0 2px 5px rgba(0,0,0,.8);white-space:nowrap}
.m4x-pr-q b{font-weight:800;color:#fff3c8}
.m4x-pr-q span{font-weight:500;color:#ecdfb8}
.m4x-pr-tb{position:absolute;box-sizing:border-box;border:1.6px solid rgba(63,214,176,.8);background:rgba(8,40,36,.85);border-radius:4px;box-shadow:0 0 8px rgba(63,214,176,.4)}
.m4x-pr-tb.y{border-color:rgba(240,199,94,.85);box-shadow:0 0 8px rgba(240,199,94,.4)}
.m4x-pr-tb i{position:absolute;left:10px;right:10px;height:9px;background:#3fd6b0;border-radius:2px;box-shadow:0 0 5px #3fd6b0}
.m4x-pr-tb.y i{background:#f0c75e;box-shadow:0 0 5px #f0c75e}
.m4x-pr-tb i:before{content:"";position:absolute;left:-1px;top:0;width:30%%;height:9px}
</style>""".replace("%%", "%")


def rt(x, y, w):
    return img("p_router.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


def tb(x, y, w, h, cls=""):
    n = max(3, int((h - 10) / 15))
    rows = "".join('<i style="top:%dpx;width:%dpx"></i>' % (6 + k * 14, (w - 20) if k % 2 == 0 else (w - 34)) for k in range(n))
    return '<div class="m4x-pr-tb %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s</div>' % (cls, x, y, w, h, rows)


def q(x, y, html):
    return '<div class="m4x-pr-q" style="left:%dpx;top:%dpx">%s</div>' % (x, y, html)


def num(cx, cy, n):
    return '<div class="m4x-pr-num" style="left:%dpx;top:%dpx">%d</div>' % (cx - 45, cy - 45, n)


def frame(x, y, w, h):
    return (box(P, x, y, w, h, "", "border-radius:14px;border-width:2px;border-color:rgba(240,199,94,.9);background:rgba(0,0,0,.18)"))


def outer(x, y, w, h):
    return box(P, x, y, w, h, "", "border-radius:6px;border-width:2px;background:rgba(2,18,14,.62);box-shadow:0 0 14px rgba(240,199,94,.3),inset 0 0 24px rgba(240,199,94,.12)")


ICON = ["p_trophy.png", "p_db.png", "p_shield.png", "p_bolt.png", "p_gear.png"]
RR = [(268, 372), (385, 487), (500, 603), (617, 722), (737, 847)]
RT = [("Оптимальность", " — выбор лучшего пути"), ("Низкие затраты", " — минимум ресурсов"), ("Стабильность", " — работа при сбоях"),
      ("Быстрая сходимость", " — согласование<br>маршрутов"), ("Гибкость", " — адаптация к изменениям<br>сети")]
right = []
for (a, b), ic, (h, t) in zip(RR, ICON, RT):
    cy = (a + b) // 2
    two = "<br>" in t
    right.append(step(frame(1000, a, 626, b - a), img(ic, "left:1012px;top:%dpx;width:102px" % (cy - 51)),
                      q(1137 if two else 1128, cy - (31 if two else 15), "<b>%s</b><span>%s</span>" % (h, t))))

tri = svg(P, path(P, "M838 645 L742 722", "g", 2.6) + path(P, "M838 645 L915 722", "g", 2.6) + path(P, "M752 762 L872 762", "g", 2.6) +
          '<g fill="#fff0b8"><circle cx="742" cy="716" r="6"/><circle cx="930" cy="716" r="6"/><circle cx="800" cy="762" r="6"/><circle cx="872" cy="762" r="6"/></g>')
p3 = svg(P, '<path d="M445 718 C490 695 540 700 572 712" fill="none" stroke="#3fe6ff" stroke-width="5" stroke-linecap="round" marker-end="url(#m4x-prab)" filter="url(#m4x-prgl)"/>'
         '<path d="M566 790 C540 800 500 800 462 792" fill="none" stroke="#ff6b5e" stroke-width="4" stroke-dasharray="7 6" stroke-linecap="round" marker-end="url(#m4x-prag)" filter="url(#m4x-prgl)"/>'
         '<path d="M502 782 L528 806 M528 782 L502 806" stroke="#ff6b5e" stroke-width="5" stroke-linecap="round"/>')

HTML = CSS + bg() + "".join([
    step(outer(28, 170, 668, 676), outer(978, 170, 670, 676),
         tx(P, "g", 375, 192, "Три принципа", 40, 600, "font-weight:900"), tx(P, "g", 1313, 192, "Требования к алгоритмам", 38, 640, "font-weight:900")),
    step(frame(50, 268, 622, 172), num(100, 340, 1), q(165, 298, "Каждый маршрутизатор<br>выбирает путь по своей<br>таблице"), tb(538, 290, 110, 100), rt(458, 355, 120)),
    step(frame(50, 458, 622, 182), num(100, 543, 2), q(165, 498, "Таблицы разных<br>маршрутизаторов<br>могут различаться"),
         tb(410, 480, 98, 66), tb(545, 480, 98, 66, "y"), rt(408, 548, 104), rt(542, 548, 104)),
    step(frame(50, 656, 622, 192), num(100, 745, 3), q(165, 700, "Прямой маршрут<br>не гарантирует<br>обратного"), rt(368, 725, 92), rt(562, 725, 96), p3),
    step(tri, rt(790, 610, 100), rt(708, 722, 100), rt(872, 722, 100)),
] + right)
