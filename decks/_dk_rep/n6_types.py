# -*- coding: utf-8 -*-
"""2.6: типы преобразования NAT — SNAT и DNAT (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 104

CSS = """<style>
.n6ty-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.6);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.3)}
.n6ty-in{position:absolute;box-sizing:border-box;background:rgba(8,18,40,.72);border:1.5px solid rgba(92,190,255,.35);border-radius:12px}
.n6ty-sub{position:absolute;font:500 31px/1 "Golos Text",sans-serif;color:#b9d2f5;white-space:nowrap}
.n6ty-h{position:absolute;font:800 35px/1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6ty-s2{position:absolute;font:500 29px/1 "Golos Text",sans-serif;color:#a9c4ee;white-space:nowrap}
.n6ty-tg{position:absolute;box-sizing:border-box;height:38px;border:1.5px solid rgba(140,190,255,.5);border-radius:8px;background:rgba(20,34,62,.9);
  font:600 18px/35px "Golos Text",sans-serif;color:#fff;text-align:center;white-space:nowrap}
.n6ty-ip{position:absolute;font:500 18px/1 "JetBrains Mono",monospace;color:#fff;white-space:nowrap}
.n6ty-bt{position:absolute;font:800 21px/1 "Golos Text",sans-serif;color:#fff;white-space:nowrap}
.n6ty-bt small{font:500 13.5px "Golos Text",sans-serif;color:#cfdcf2}
.n6ty-f{position:absolute;box-sizing:border-box;height:50px;border-radius:8px;border:1.5px solid rgba(140,190,255,.45);background:rgba(16,26,48,.9);
  font:500 18px/47px "Golos Text",sans-serif;color:#e6eefc;padding-left:12px;white-space:nowrap}
.n6ty-f span{position:absolute;font:inherit;font-size:16.5px;font-family:"JetBrains Mono",monospace}
.n6ty-y{background:#ffd23a;border-color:#ffe27a;color:#111;font-weight:700;box-shadow:0 0 14px rgba(255,210,58,.5)}
.n6ty-r{background:#ff6a50;border-color:#ff9a80;color:#111;font-weight:700;box-shadow:0 0 14px rgba(255,106,80,.5)}
.n6ty-nat{position:absolute;font:800 22px/1 Montserrat,sans-serif;color:#fff}
.n6ty-ft{position:absolute;font:800 24px/1.25 "Golos Text",sans-serif;white-space:nowrap}
.n6ty-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6ty-fl{stroke-dasharray:12 8;animation:n6tyd 1s linear infinite}
@keyframes n6tyd{to{stroke-dashoffset:-40}}
</style>"""

ARR = '<path class="n6ty-fl" d="M%d %dH%d" stroke="#3ab0ff" stroke-width="4" fill="none"/><path d="M%d %dl-16-10v20z" fill="#3ab8ff"/>'


def arrs(lst):
    return '<svg class="n6ty-sv" viewBox="0 0 1672 941">' + "".join(ARR % (a, y, b - 10, b, y) for a, y, b in lst) + '</svg>'


def tg(x, y, w, t):
    return '<div class="n6ty-tg" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (x, y, w, t)


def ip(x, y, t):
    return '<div class="n6ty-ip" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


def fld(x, y, w, k, v, cls="", vx=140):
    return '<div class="n6ty-f %s" style="left:%dpx;top:%dpx;width:%dpx">%s<span style="left:%dpx">%s</span></div>' % (cls, x, y, w, k, vx, v)


def side(x0, col, ico, title, sub, tags, ips, imgs, arrows, before, after, bt1, bt2, nat, foot_ico, foot, fcol):
    s = '<div class="step"><div class="n6ty-p" style="left:%dpx;top:172px;width:808px;height:726px"></div>' % x0
    s += '<div style="position:absolute;left:%dpx;top:195px;width:118px;height:112px;border-radius:14px;background:%s;box-shadow:0 0 20px %s"></div>' % (x0 + 22, col, col)
    s += img(ico, "left:%dpx;top:195px;width:%dpx" % (x0 + 22, 118))
    s += '<div class="n6ty-h" style="left:%dpx;top:212px">%s</div>' % (x0 + 162, title)
    s += '<div class="n6ty-s2" style="left:%dpx;top:263px">%s</div></div>' % (x0 + 162, sub)
    s += '<div class="step"><div class="n6ty-in" style="left:%dpx;top:322px;width:764px;height:236px"></div>' % (x0 + 22)
    s += "".join(tg(*t) for t in tags) + "".join(ip(*t) for t in ips) + "".join(img(*t) for t in imgs) + arrs(arrows) + '</div>'
    s += ('<div class="step"><div class="n6ty-in" style="left:%dpx;top:575px;width:298px;height:170px"></div>' % (x0 + 22)
          + '<div class="n6ty-in" style="left:%dpx;top:575px;width:298px;height:170px"></div>' % (x0 + 490)
          + '<div class="n6ty-bt" style="left:%dpx;top:590px">%s</div>' % (x0 + 38, bt1)
          + '<div class="n6ty-bt" style="left:%dpx;top:590px">%s</div>' % (x0 + 508, bt2)
          + "".join(fld(*f) for f in before + after)
          + img(nat, "left:%dpx;top:586px;width:121px" % (x0 + 344))
          + '<div class="n6ty-nat" style="left:%dpx;top:710px">NAT</div>' % (x0 + 380)
          + arrs([(x0 + 330, 648, x0 + 372), (x0 + 466, 648, x0 + 510)]) + '</div>')
    s += ('<div class="step"><div class="n6ty-in" style="left:%dpx;top:762px;width:764px;height:110px"></div>' % (x0 + 22)
          + img(foot_ico, "left:%dpx;top:776px;width:84px" % (x0 + 36))
          + '<div class="n6ty-ft" style="left:%dpx;top:%dpx;color:%s">%s</div></div>' % (x0 + 140, 803 if "<br>" not in foot else 788, fcol, foot))
    return s


SNAT = side(22, "#ffd23a", "n6_types_out.png", "SNAT — исходящая трансляция", "Меняется адрес источника",
            [(58, 338, 200, "Локальный узел"), (318, 338, 216, "Маршрутизатор NAT"), (608, 336, 188, "Интернет-сервер")],
            [(100, 524, "192.168.1.10"), (362, 522, "198.51.100.7"), (632, 524, "203.0.113.20")],
            [("n6_types_lap.png", "left:68px;top:395px;width:168px"), ("n6_types_rt.png", "left:343px;top:385px;width:147px"),
             ("n6_types_cloud.png", "left:538px;top:420px;width:134px"), ("n6_types_rack.png", "left:664px;top:385px;width:124px")],
            [(200, 466, 336), (490, 466, 566)],
            [(55, 622, 276, "Источник:", "192.168.1.10", "n6ty-y"), (55, 682, 276, "Назначение:", "203.0.113.20", "", 148)],
            [(523, 622, 273, "Источник:", "198.51.100.7", "n6ty-y"), (523, 682, 273, "Назначение:", "203.0.113.20", "", 148)],
            "До NAT <small>(от локального узла)</small>", "После NAT <small>(в интернет)</small>", "n6_types_nat.png",
            "n6_types_globe.png", "Внешний сервер видит публичный адрес источника", "#ffd23a")

DNAT = side(842, "#ff6a50", "n6_types_in.png", "DNAT — входящая трансляция", "Меняется адрес назначения",
            [(878, 336, 192, "Интернет-клиент"), (1142, 336, 212, "Маршрутизатор NAT"), (1426, 334, 190, "Внутренний сервер")],
            [(914, 526, "203.0.113.50"), (1194, 524, "198.51.100.7"), (1458, 524, "192.168.1.20")],
            [("n6_types_lap2.png", "left:888px;top:398px;width:159px"), ("n6_types_cloud2.png", "left:1016px;top:420px;width:126px"),
             ("n6_types_rt2.png", "left:1173px;top:385px;width:149px"), ("n6_types_srv.png", "left:1456px;top:385px;width:102px")],
            [(1130, 466, 1170), (1322, 466, 1450)],
            [(878, 622, 268, "Источник:", "203.0.113.50", "", 144), (878, 682, 268, "Назначение:", "198.51.100.7", "n6ty-r", 146)],
            [(1342, 622, 276, "Источник:", "203.0.113.50", "", 146), (1342, 682, 276, "Назначение:", "192.168.1.20", "n6ty-r", 146)],
            "До NAT <small>(запрос из интернета)</small>", "После DNAT <small>(к внутреннему серверу)</small>", "n6_types_nat2.png",
            "n6_types_db.png", "Публичный запрос перенаправляется<br>на нужный внутренний ресурс", "#c98bff")

HTML = (CSS + bg("bgk_globe")
        + '<div class="step"><div class="n6ty-sub" style="left:62px;top:118px">Преобразование сетевых адресов для связи локальных и внешних сетей</div></div>'
        + SNAT + DNAT)
