# -*- coding: utf-8 -*-
"""LSA-2 — Network LSA: сеть с множественным доступом, DR, список Router ID."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

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

CARDS = [("<b>Создаёт DR</b> —<br>назначенный маршрутизатор", 1),
         ("<b>Содержит Router ID</b><br>маршрутизатор:ов с полным<br>соседством с DR", 2),
         ("<b>Стоимость соединений</b><br>указывается в <b>LSA-1</b>,<br>а не в <b>LSA-2</b>", 3),
         ("<b>Распространяется</b> только<br>внутри своей области", 4),
         ("<b>Link State ID</b> — IP-адрес<br>интерфейса DR", 5),
         ("<b>Advertising Router</b> —<br>Router ID DR", 6)]


def cards():
    out = []
    for i, (t, n) in enumerate(CARDS):
        y = 232 + i * 106
        out.append('<div class="step"><div class="ol2-card" style="top:%dpx;height:100px"></div>' % y
                   + img("o_lsa2_i%d.png" % n, "left:1012px;top:%dpx;width:92px" % (y + 4))
                   + T(1122, y + (12 if t.count("<br>") > 1 else 22), 368, 21 if t.count("<br>") < 2 else 19.5,
                       t.replace("<b>", "<b style='font-weight:700'>"), 400, lh=1.25, ex="white-space:nowrap")
                   + '</div>')
    return ('<div class="step">' + "".join(out[:3]).replace('<div class="step">', "<div>") + '</div><div class="step">'
            + "".join(out[3:]).replace('<div class="step">', "<div>") + "</div>")


def rrow(y, t):
    return '<div class="ol2-row" style="top:%dpx">%s<span>%s</span></div>' % (y, img("o_lsa2_r.png", "", ""), t)


LSA2 = ('<div class="ab" style="position:absolute;left:388px;top:624px;width:264px;height:234px;background:#fff;'
        'border:3px solid #ff7aa8;border-radius:16px"></div>'
        + B(391, 627, 258, 42, "#ff9cc0", 13, "border-radius:13px 13px 0 0")
        + img("o_lsa2_doc.png", "left:394px;top:606px;width:56px")
        + T(452, 630, 150, 29, "LSA-2", 700, c="#fff", ex=C)
        + T(392, 670, 256, 16, "Список Router ID<br>маршрутизаторов<br>с полным соседством с DR", 600, lh=1.22, ex="text-align:center")
        + rrow(738, "R1") + rrow(773, "R2 &nbsp;(DR)") + rrow(810, "R3"))

SCENE = ('<div class="step">' + img("o_lsa2_scene.png", "left:20px;top:228px;width:962px")
         + T(124, 266, 214, 20, "Одна область OSPF", 500, ex=C + ";background:#ffd6e5;border-radius:14px;padding:2px 0")
         + T(484, 299, 74, 26, "DR", 700, ex=C + ";background:#ffe36e;border-radius:10px;padding:1px 0")
         + T(372, 530, 290, 21, "Общий Ethernet-сегмент", 600, ex=C) + '</div>'
         + '<div class="step"><div>'
         + T(560, 570, 140, 18, "Создаёт<br>один LSA-2", 600, lh=1.2,
             ex="background:#fff;border:2px solid #ffc0d6;border-radius:24px;padding:4px 0 4px 18px;box-sizing:border-box")
         + LSA2 + T(752, 668, 172, 20, "LSDB области", 600, ex=C) + '</div></div>')

FOOT = ('<div class="step">' + B(42, 885, 712, 106, "#ffe78a", 30) + img("o_lsa2_b1.png", "left:62px;top:898px;width:90px")
        + T(184, 900, 520, 27, "Применяется в Ethernet<br>и соответствующих сетях NBMA", 600, lh=1.2, ex="white-space:nowrap")
        + '</div><div class="step">' + B(815, 885, 680, 106, "#dcebfd", 30) + img("o_lsa2_b2.png", "left:840px;top:893px;width:90px")
        + T(978, 905, 500, 24, "На соединении точка-точка<br>LSA-2 обычно не нужен", 400, lh=1.3, ex="white-space:nowrap") + '</div>')

HTML = CSS + bg("bg5", W, H) + SCENE + cards() + FOOT
