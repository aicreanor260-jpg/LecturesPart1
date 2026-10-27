# -*- coding: utf-8 -*-
"""LSA-2 — Network LSA: сеть с множественным доступом, DR, список Router ID."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg
from _o5_ikit import puck, line, svg, g4_arr, g4_area, g4_icon, g4_glyph_at, g4_doc, g4_tower

W, H, TOP = 1536, 1024, 226
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


C = "text-align:center;white-space:nowrap"
CSS = """<style>
.ol2-card{position:absolute;left:1002px;width:492px;background:rgba(255,255,255,.92);border:2px solid #ece6ef;border-radius:22px}
.ol2-row{position:absolute;left:412px;width:214px;height:30px;background:#fff;border:1.5px solid #f0d4e0;border-radius:15px;
  font:500 17px/28px 'Golos Text',sans-serif;color:#1f1a33}
.ol2-row img{position:absolute;left:12px;top:3px;width:28px}
.ol2-row span{position:absolute;left:66px}
</style>"""

def scene_svg():
    o = [g4_area(70, 260, 900, 330, "p", 60),
         '<rect x="112" y="482" width="800" height="84" rx="22" style="fill:#d6eafd" stroke="#8fbff0" stroke-width="3"/>']
    for x in (140, 175, 210, 800, 835, 870):
        o.append('<rect x="%d" y="534" width="24" height="18" rx="3" style="fill:#2a2f3d"/>' % x)
    for x, c in ((238, "#3f86d8"), (517, "#e05a97"), (785, "#3f86d8")):
        o.append(line((x, 430), (x, 494), c, 12))
    o += [puck(238, 375, 200, "b", "R1", 30), puck(517, 360, 210, "p", "R2", 30), puck(785, 375, 200, "b", "R3", 30),
          g4_arr(517, 562, 517, 612, "#ff5c9e", 10)]
    return svg("".join(o), W, H)


def lsdb_svg():
    o = ['<path d="M690 790 h270 l-20 40 h-270 z" style="fill:#dcebfd"/>',
         g4_tower(740, 712, 110, 96), g4_tower(815, 730, 115, 96),
         '<rect x="730" y="660" width="210" height="40" rx="20" style="fill:#d6eafd" stroke="#8fbff0" stroke-width="2.5"/>',
         g4_arr(652, 745, 720, 745, "#ffc400", 12)]
    return svg("".join(o), W, H)


CARDS = [("<b>Создаёт DR</b> —<br>назначенный маршрутизатор", 1),
         ("<b>Содержит Router ID</b><br>маршрутизаторов с полным<br>соседством с DR", 2),
         ("<b>Стоимость соединений</b><br>указывается в <b>LSA-1</b>,<br>а не в <b>LSA-2</b>", 3),
         ("<b>Распространяется</b> только<br>внутри своей области", 4),
         ("<b>Link State ID</b> — IP-адрес<br>интерфейса DR", 5),
         ("<b>Advertising Router</b> —<br>Router ID DR", 6)]


def cards():
    out = []
    for i, (t, n) in enumerate(CARDS):
        y = 232 + i * 106
        out.append('<div class="step"><div class="ol2-card" style="top:%dpx;height:100px"></div>' % y
                   + g4_icon(["router", "users", "db", "globe", "pin", "gear"][n - 1], 1014, y + 5, 90, "pbybpy"[n - 1])
                   + T(1122, y + (12 if t.count("<br>") > 1 else 22), 368, 21 if t.count("<br>") < 2 else 19.5,
                       t.replace("<b>", "<b style='font-weight:700'>"), 400, lh=1.25, ex="white-space:nowrap")
                   + '</div>')
    return ('<div class="step">' + "".join(out[:3]).replace('<div class="step">', "<div>") + '</div><div class="step">'
            + "".join(out[3:]).replace('<div class="step">', "<div>") + "</div>")


def rrow(y, t):
    return ('<div class="ol2-row" style="top:%dpx"><svg style="position:absolute;left:10px;top:2px" width="34" height="24" '
            'viewBox="0 0 34 24">%s</svg><span>%s</span></div>' % (y, puck(17, 8, 30, "b"), t))


LSA2 = ('<div class="ab" style="position:absolute;left:388px;top:624px;width:264px;height:234px;background:#fff;'
        'border:3px solid #ff7aa8;border-radius:16px"></div>'
        + B(391, 627, 258, 42, "#ff9cc0", 13, "border-radius:13px 13px 0 0")
        + svg(g4_doc(398, 608, 46, "", "p"), W, H)
        + T(452, 630, 150, 29, "LSA-2", 700, c="#fff", ex=C)
        + T(392, 670, 256, 16, "Список Router ID<br>маршрутизаторов<br>с полным соседством с DR", 600, lh=1.22, ex="text-align:center")
        + rrow(738, "R1") + rrow(773, "R2 &nbsp;(DR)") + rrow(810, "R3"))

SCENE = ('<div class="step">' + scene_svg()
         + T(124, 266, 214, 20, "Одна область OSPF", 500, ex=C + ";background:#ffd6e5;border-radius:14px;padding:2px 0")
         + T(480, 282, 74, 26, "DR", 700, ex=C + ";background:#ffe36e;border-radius:10px;padding:1px 0")
         + T(362, 508, 310, 21, "Общий Ethernet-сегмент", 600, ex=C) + '</div>'
         + '<div class="step"><div>'
         + T(560, 570, 140, 18, "Создаёт<br>один LSA-2", 600, lh=1.2,
             ex="background:#fff;border:2px solid #ffc0d6;border-radius:24px;padding:4px 0 4px 18px;box-sizing:border-box")
         + lsdb_svg() + LSA2 + T(740, 668, 190, 20, "LSDB области", 600, ex=C) + '</div></div>')

FOOT = ('<div class="step">' + B(42, 885, 712, 106, "#ffe78a", 30) + g4_icon("bulb", 62, 893, 90, "#1f1a33", "#ffd23a")
        + T(184, 900, 520, 27, "Применяется в Ethernet<br>и соответствующих сетях NBMA", 600, lh=1.2, ex="white-space:nowrap")
        + '</div><div class="step">' + B(815, 885, 680, 106, "#dcebfd", 30) + g4_icon("excl", 840, 893, 90, "w")
        + T(978, 905, 500, 24, "На соединении точка-точка<br>LSA-2 обычно не нужен", 400, lh=1.3, ex="white-space:nowrap") + '</div>')

HTML = CSS + bg("bg5", W, H) + SCENE + cards() + FOOT
