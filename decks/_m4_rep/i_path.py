# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 172

CSS = """<style>
.m4x-pth-p{position:absolute;box-sizing:border-box;border:2px solid rgba(240,199,94,.75);border-radius:14px;
  background:linear-gradient(180deg,rgba(10,52,40,.78),rgba(4,28,22,.88));box-shadow:0 0 18px rgba(240,199,94,.25)}
.m4x-pth-g{border-color:#3fd6b0;background:linear-gradient(180deg,rgba(14,86,66,.85),rgba(6,50,40,.9));box-shadow:0 0 22px rgba(63,214,176,.45);border-radius:24px}
.m4x-pth-r{border-color:#ff5a3c;background:linear-gradient(180deg,rgba(96,20,14,.88),rgba(52,10,8,.92));box-shadow:0 0 22px rgba(255,90,60,.5);border-radius:18px}
.m4x-pth-ttl{border-radius:12px;background:rgba(6,44,34,.92);border-color:#f0c75e;box-shadow:0 0 10px rgba(240,199,94,.3)}
.m4x-pth-t{position:absolute;font:500 22px/30px "Golos Text",sans-serif;color:#f4efdc;white-space:nowrap}
.m4x-pth-b{font-size:25px;line-height:33px}
.m4x-pth-c{text-align:center}
.m4x-pth-n{color:#3fd6b0;font-weight:700}
.m4x-pth-lb{font:800 25px/30px "Playfair Display",serif;color:#fff}
.m4x-pth-big{font:800 30px/34px "Playfair Display",serif;color:#f6e3a0}
.m4x-pth-z{font:700 27px/34px "Golos Text",sans-serif;color:#fff}
.m4x-pth-s{font-size:20px;line-height:24px}
.m4x-pth-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.m4x-pth-sv .gl{fill:none;stroke:#3fd6b0;stroke-width:3.5;filter:drop-shadow(0 0 6px #3fd6b0)}
.m4x-pth-sv .rd{fill:none;stroke:#ff5a3c;stroke-width:3.5;filter:drop-shadow(0 0 6px #ff5a3c)}
.m4x-pth-sv .rdd{fill:none;stroke:#ff5a3c;stroke-width:3;stroke-dasharray:14 9;filter:drop-shadow(0 0 5px #ff5a3c);animation:m4xpth 1.2s linear infinite}
.m4x-pth-sv .ring{fill:rgba(4,30,24,.35);stroke:#f0c75e;stroke-width:2;filter:drop-shadow(0 0 8px rgba(240,199,94,.6))}
.m4x-pth-sv .ringr{fill:rgba(60,8,6,.4);stroke:#ff5a3c;stroke-width:2.5;filter:drop-shadow(0 0 8px rgba(255,90,60,.7))}
.m4x-pth-sv .dot{fill:#f0c75e;filter:drop-shadow(0 0 5px #f0c75e)}
@keyframes m4xpth{to{stroke-dashoffset:-46}}
</style>"""


def im(n, x, y, w):
    return img("i_path_%s.png" % n, "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


def svg(body):
    return ('<svg class="m4x-pth-sv" viewBox="0 0 1672 941"><defs>'
            '<marker id="m4xpg" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#3fd6b0"/></marker>'
            '<marker id="m4xpr" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#ff5a3c"/></marker></defs>'
            + body + '</svg>')


def t(x, y, s, cls="", w=None):
    st = "left:%dpx;top:%dpx" % (x, y)
    if w:
        st += ";width:%dpx;margin-left:-%dpx" % (w, w // 2)
    return '<div class="m4x-pth-t %s" style="%s">%s</div>' % (("m4x-pth-c " if w else "") + cls, st, s)


def panel(x, y, x2, y2, cls=""):
    return '<div class="m4x-pth-p %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>' % (cls, x, y, x2 - x, y2 - y)


def ring(cx, cy, r=92, red=False):
    return '<circle class="%s" cx="%d" cy="%d" r="%d"/><circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-opacity=".35"/>' % (
        "ringr" if red else "ring", cx, cy, r, cx, cy, r - 9, "#ff5a3c" if red else "#f0c75e")


TV = lambda a, b: '<span class="m4x-pth-n">%s</span>' % b

# цепочка узлов
SEND = ('<div class="step">' + svg(ring(121, 415, 92)) + im("lap", 60, 362, 140) + t(122, 507, "Отправитель", "m4x-pth-lb", 260) + '</div>')


def router(n, cx, ttl, y2=581):
    box = ''
    if ttl == 3:
        box = panel(318, 505, 500, 581, "m4x-pth-ttl") + t(cx, 512, "Вход TTL = <span class='m4x-pth-n'>3</span>", "", 182) + t(cx, 542, "Выход TTL = <span class='m4x-pth-n'>2</span>", "", 182)
    elif ttl == 2:
        box = panel(585, 505, 767, 581, "m4x-pth-ttl") + t(cx, 512, "Вход TTL = <span class='m4x-pth-n'>2</span>", "", 182) + t(cx, 542, "Выход TTL = <span class='m4x-pth-n'>1</span>", "", 182)
    else:
        box = panel(858, 505, 1018, 554, "m4x-pth-ttl") + t(cx, 512, "Вход TTL = <span class='m4x-pth-n'>1</span>", "", 160)
    return ('<div class="step">' + svg(ring(cx, 415, 95)) + im("p%d" % n, cx - 70, 365, 142)
            + t(cx, 468, "R%d" % n, "m4x-pth-lb", 100) + box + '</div>')


R1, R2, R3 = router(1, 410, 3), router(2, 675, 2), router(3, 940, 1)

FLOW = ('<div class="step">' + svg(
    '<path class="gl" d="M214 413H320" marker-end="url(#m4xpg)"/><path class="gl" d="M482 413H590" marker-end="url(#m4xpg)"/><path class="gl" d="M747 413H855" marker-end="url(#m4xpg)"/>'
    '<circle class="dot" cx="212" cy="413" r="6"/><circle class="dot" cx="507" cy="413" r="7"/><circle class="dot" cx="771" cy="413" r="7"/>') + '</div>')

DEST = ('<div class="step">' + svg('<path class="gl" d="M1030 403C1090 400 1100 350 1105 320C1112 305 1150 308 1200 308" marker-end="url(#m4xpg)"/><circle class="dot" cx="1097" cy="358" r="7"/><circle class="dot" cx="1030" cy="403" r="6"/>')
        + panel(1192, 232, 1636, 400, "m4x-pth-g")
        + svg(ring(1275, 310, 56) + ring(1560, 310, 56) + '<path class="gl" d="M1473 309H1497" marker-end="url(#m4xpg)" style="stroke:#fff;stroke-width:3"/>')
        + im("mon", 1240, 280, 70) + im("lapt", 1522, 280, 76)
        + t(1349, 269, "Назначение<br>подключено<br>напрямую", "m4x-pth-s").replace("white-space:nowrap", "")
        + t(1559, 366, "Доставка", "", 150) + '</div>')

DROP = ('<div class="step">' + svg('<path class="rd" d="M1030 428C1085 430 1085 470 1097 480C1112 520 1140 535 1176 535" marker-end="url(#m4xpr)"/><circle class="dot" cx="1097" cy="478" r="7"/><circle class="dot" cx="1030" cy="428" r="6"/>'
        + ring(1232, 534, 56, True) + ring(1404, 535, 56, True) + ring(1575, 535, 56, True)
        + '<path class="rd" d="M1301 534H1335" marker-end="url(#m4xpr)"/><path class="rd" d="M1473 534H1507" marker-end="url(#m4xpr)"/>')
        + im("x", 1200, 508, 65) + im("trash", 1540, 502, 70)
        + t(1404, 520, "TTL = 0", "m4x-pth-z", 120)
        + t(1233, 591, "Нужна ещё<br>одна пересылка", "", 240).replace("white-space:nowrap", "")
        + t(1577, 591, "Пакет<br>отброшен", "", 160) + '</div>')

ICMP = ('<div class="step">' + svg('<path class="rdd" d="M1404 598C1404 650 1380 665 1330 665H718" marker-end="url(#m4xpr)"/>')
        + panel(390, 616, 712, 697, "m4x-pth-r")
        + svg('<circle class="ringr" cx="433" cy="657" r="40"/>') + im("env", 407, 631, 56)
        + t(501, 630, "ICMP Time Exceeded<br>отправителю", "m4x-pth-s", None)
        + svg('<path class="rdd" d="M390 657H215C150 657 128 620 128 580V548" marker-end="url(#m4xpr)"/>') + '</div>')

BOT1 = ('<div class="step">' + panel(50, 752, 1075, 882) + im("gear", 85, 780, 85)
        + t(198, 780, "При каждой пересылке:", "m4x-pth-big", None)
        + t(198, 823, "TTL − 1;&nbsp; контрольная сумма заголовка IPv4 пересчитывается.", "m4x-pth-b", None) + '</div>')
BOT2 = ('<div class="step">' + panel(1097, 752, 1623, 882) + im("doc", 1135, 780, 70)
        + t(1220, 787, "FCS относится к кадру<br>канального уровня.", "m4x-pth-b", None) + '</div>')

HTML = CSS + bg() + "".join([SEND, R1, R2, R3, FLOW, DEST, DROP, ICMP, BOT1, BOT2])
