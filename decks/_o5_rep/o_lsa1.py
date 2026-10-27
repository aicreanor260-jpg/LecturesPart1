# -*- coding: utf-8 -*-
"""Типы записей OSPF. LSA-1: Router LSA — Area 0.0.0.1, таблица соединений R1, свойства."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import puck, line, cross, svg, cloud_icon, g4_arr, g4_area, g4_icon, g4_glyph_at, g4_ico, FADE

W, H, TOP = 1536, 1024, 58
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


C = "text-align:center;white-space:nowrap"
NW = "white-space:nowrap"
CSS = """<style>
.ol1-tb{position:absolute;left:382px;top:598px;border-collapse:separate;border-spacing:3px;font:500 15px/1.25 'Golos Text',sans-serif;color:#1f1a33}
.ol1-tb td{background:#fff;border-radius:6px;padding:0 10px;vertical-align:middle;white-space:nowrap}
.ol1-tb tr:first-child td{background:#cfe6fb;text-align:center;font-weight:600;height:54px}
.ol1-tb small{font-size:13px;font-weight:400}
.ol1-hl{background:linear-gradient(transparent 55%,#fff1a0 55%)}
</style>"""


def scene_svg():
    o = ['<rect x="1132" y="62" width="390" height="382" rx="40" style="fill:#d9dce6;fill-opacity:.85" stroke="#9aa0b2" '
         'stroke-width="3" stroke-dasharray="12 8"/>',
         '<rect x="1160" y="76" width="350" height="76" rx="30" style="fill:#3a3f55"/>',
         g4_area(405, 108, 715, 332, "b", 50),
         cloud_icon(498, 352, 1.5, "#e8f3fe", "#7fb6ee"),
         line((570, 330), (640, 330), "#2f8fe8", 6), line((820, 330), (935, 330), "#2f8fe8", 6),
         line((1088, 320), (1150, 310), "#2b2f3d", 5), line((1290, 320), (1350, 340), "#2b2f3d", 5),
         g4_arr(790, 368, 1095, 408, "#ff5c9e", 4, dash="12 8", curve=-20), cross(1030, 404, 14, "#e8245e", 6),
         puck(730, 305, 190, "p", "R1", 30), puck(1012, 315, 160, "b", "R2", 28), puck(1215, 300, 150, "k", "ABR", 26),
         puck(1420, 345, 140, "b"), cloud_icon(1435, 275, 1.6, "#ffffff", "#c7d0dc"),
         '<text x="1428" y="262" text-anchor="middle" font-size="26" font-weight="900" style="fill:#2b2f3d">...</text>',
         '<rect x="672" y="205" width="118" height="58" rx="10" style="fill:#fff" stroke="#ff8fb8" stroke-width="3"/>',
         '<rect x="954" y="205" width="118" height="58" rx="10" style="fill:#fff" stroke="#8fbff0" stroke-width="3"/>',
         line((731, 263), (731, 285), "#ff8fb8", 3), line((1013, 263), (1013, 290), "#8fbff0", 3),
         '<rect x="1105" y="366" width="175" height="84" rx="12" style="fill:#fff" stroke="#ff8fb8" stroke-width="3" transform="rotate(-4 1190 408)"/>']
    return svg("".join(o), W, H)


SCENE = ('<div class="step">' + scene_svg()
         + T(640, 108, 268, 38, "Area 0.0.0.1", 700, c="#fff", ex=C + ";background:#2f7fe0;border-radius:26px;padding:4px 0")
         + T(676, 210, 110, 15, "Router ID<br><b style='font-size:21px'>1.1.1.1</b>", 500, lh=1.15, ex="text-align:center")
         + T(958, 210, 110, 15, "Router ID<br><b style='font-size:21px'>2.2.2.2</b>", 500, lh=1.15, ex="text-align:center")
         + T(560, 362, 82, 18, "cost 10", 700, ex=C + ";background:#ffe36e;border-radius:12px")
         + T(840, 362, 72, 18, "cost 5", 700, ex=C + ";background:#ffe36e;border-radius:12px")
         + T(424, 388, 152, 18, "192.168.10.0/24", 700, ex=C)
         + T(1182, 80, 300, 21, "другая область —<br>LSA-1 сюда не <span style='color:#ff6fa8'>передаётся</span>", 500, c="#fff", lh=1.2)
         + T(1120, 376, 150, 16, "LSA-1<br>не передаётся<br>в другие области", 600, c="#e8336f", lh=1.15) + '</div>')

GIRL = ('<div class="step">' + img("o_lsa1_girl.png", "left:0;top:218px;width:372px")
        + '<div class="ab" style="position:absolute;left:46px;top:596px;width:220px;transform:rotate(-9deg);'
          'font:500 21px/1.22 \'Golos Text\',sans-serif;color:#1f1a33">LSA-1<br>описывает связи<br>и параметры<br>маршрутизатора,<br>'
          'а не просто<br>список IP-сетей <span style="color:#ff4f9a">&#9829;</span></div></div>')

TBL = ('<table class="ol1-tb"><tr><td style="width:166px">Сосед / сеть<br><small>(конечная точка)</small></td>'
       '<td style="width:150px">Тип соединения</td><td style="width:100px">Стоимость<br>(cost)</td><td style="width:202px">Пример параметров</td></tr>'
       '<tr><td style="height:78px;padding-left:64px;font-size:13.5px;font-weight:600">Сеть<br>192.168.10.0/24</td>'
       '<td><b style="font-weight:600">Stub Network</b><br><small>(подключённая сеть)</small></td>'
       '<td style="text-align:center;font:700 22px Golos Text">10</td><td>Network Type: Stub<br>Link ID: 192.168.10.0<br>Link Data: 255.255.255.0</td></tr>'
       '<tr><td style="height:78px;padding-left:76px;font-size:16px;font-weight:600">R2<br>(2.2.2.2)</td>'
       '<td><b style="font-weight:600">Point-to-Point</b><br><small>(к соседу R2)</small></td>'
       '<td style="text-align:center;font:700 22px Golos Text">5</td><td>Link ID: 2.2.2.2<br>Link Data: 2.2.2.2<br>(тип сети P2P)</td></tr></table>')

PANEL = ('<div class="step">' + B(365, 460, 690, 476, "rgba(255,255,255,.95)", 22, "border:2.5px solid #ffc4d8")
         + B(368, 463, 660, 56, "#ff8fb8", 20, "border-radius:20px 40px 0 0")
         + T(396, 466, 400, 36, "LSA-1: ТОПОЛОГИЯ R1", 700, c="#fff", f="Oswald", ex=NW)
         + T(392, 528, 330, 26, "<span style='color:#ff4f9a'>&#10022;</span> Link State ID = 1.1.1.1", 700, ex=NW)
         + T(414, 562, 300, 18, "(Router ID автора)", 600, ex=NW)
         + T(734, 490, 312, 15, "Внутри LSA-1 перечислены<br>OSPF-соединения R1 и их параметры<br>(стоимость, тип сети и др.),<br>"
             "а не список IP-сетей.", 400, lh=1.32, ex=NW + ";background:#ffe1ec;border-radius:16px;padding:10px 14px;box-sizing:border-box;height:100px")
         + svg(g4_glyph_at("doc", 1022, 572, 40, "#2f8fe8", 2), W, H)
         + TBL + svg(cloud_icon(412, 708, .58, "#d6eafd", "#3f86d8") + puck(412, 780, 50, "b"), W, H)
         + B(382, 840, 658, 80, "#ffe1ec", 16) + svg(g4_glyph_at("bulb", 420, 880, 46, "#1f1a33", 2), W, H)
         + T(482, 857, 540, 18, "LSA-1 описывает связи и параметры маршрутизатора,<br>а не просто список IP-сетей", 500, c="#c2185b", lh=1.35, ex=NW)
         + '</div>')

CARDS = ["Содержит OSPF-соединения<br>маршрутизатора в области<br><span class='ol1-hl'>и их стоимость</span>",
         "Отдельная LSA-1 создаётся<br>для каждой подключённой<br>области",
         "<span class='ol1-hl'>Link State ID = Router ID автора</span>",
         "<span class='ol1-hl'>Распространяется только</span><br><span class='ol1-hl'>внутри своей области</span>",
         "ABR не пересылает LSA-1<br><span style='color:#1f5fae'>в другие области</span>"]


II = ["list", "pin", "users", "radio", "ban"]
JJ = ["link", "tree", "users", "redo", "ban"]
JC = ["#ff5c9e", "#2f8fe8", "#2f8fe8", "#2f8fe8", "#ff3d6e"]


def cards():
    out = []
    for i, t in enumerate(CARDS):
        cy = [512, 615, 712, 808, 905][i]
        out.append('<div class="step">' + B(1070, cy - 46, 454, 92, "rgba(255,255,255,.93)", 46, "border:2px solid #ece6ef")
                   + g4_icon(II[i], 1080, cy - 42, 84, ["p", "b", "y", "p", "b"][i])
                   + T(1178, cy - 11 * (t.count("<br>") + 1), 270, 17.5, t, 600, lh=1.2, ex=NW)
                   + svg(g4_glyph_at(JJ[i], 1486, cy, 38, JC[i], 2.2), W, H) + '</div>')
    return "".join(out)


FOOT = ('<div class="step">' + B(430, 955, 826, 50, "#e4dcfa", 25) + svg(g4_glyph_at("book", 478, 980, 40, "#2f8fe8", 2), W, H)
        + T(516, 966, 730, 18.5, "В <b style='font-weight:700'>OSPFv3</b> объявления о префиксах IPv6 организованы иначе, чем в OSPFv2.", 500, ex=NW)
        + '</div>')

HTML = CSS + bg("bg2", W, H) + SCENE + GIRL + PANEL + cards() + FOOT
