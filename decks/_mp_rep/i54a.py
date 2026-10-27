# -*- coding: utf-8 -*-
"""pptx: трассировка LSP (LSP Ping traceroute) — вёрстка поверх bgk_19."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i54-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i54-h{position:absolute;font:900 32px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i54-t{position:absolute;font:600 18px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i54-n{position:absolute;font:900 24px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:160px}
.i54-ttl{position:absolute;background:#c8eee3;border-radius:10px;font:800 22px/50px "Golos Text",sans-serif;color:#13306e;width:176px;text-align:center}
.i54-ln{position:absolute;background:rgba(220,236,230,.55);border-radius:12px;height:50px}
.i54-ar{position:absolute;height:3px}
.i54-ar.r::after,.i54-ar.l::before{content:"";position:absolute;top:-6px;border:7px solid transparent}
.i54-ar.r::after{right:-3px;border-left:12px solid currentColor;border-right:0}
.i54-ar.l::before{left:-3px;border-right:12px solid currentColor;border-left:0}
.i54-bl{color:#1f63c6;background:#1f63c6}.i54-gr{color:#2a9a4a;background:#2a9a4a}
.i54-ds{position:absolute;height:0;border-top:3px dashed #f08060}
.i54-x{position:absolute;font:900 50px/1 "Rubik",sans-serif;color:#ec4a2c}
.i54-lab{position:absolute;font:700 18px/1 "Golos Text",sans-serif;white-space:nowrap}
.i54-num{position:absolute;width:52px;height:52px;border-radius:50%;color:#fff;font:900 32px/52px "Rubik";text-align:center}
.i54-vd{position:absolute;width:0;border-left:2px dashed #9aa8b8;opacity:.7}
.i54-fly{animation:i54f 2.6s ease-in-out infinite}
@keyframes i54f{0%,100%{transform:translateX(0)}50%{transform:translateX(12px)}}
</style>"""


def ar(x, y, w, c, d="r"):
    return '<div class="i54-ar %s i54-%s" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (d, c, x, y, w)


def lab(x, y, t, c):
    return '<div class="i54-lab" style="left:%dpx;top:%dpx;color:%s">%s</div>' % (x, y, c, t)


def rt(x, y, w=86):
    return img("i54a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


def sm(x, y):
    return rt(x, y, 54)


NODES = [(392, "LER1", "(источник)"), (640, "LSR1", ""), (878, "LSR2", ""), (1133, "LSR3", ""), (1376, "LER2", "(конец LSP)")]

ROWS = [
    (390, 1, [sm(656, 392), ar(438, 403, 212, "bl"), lab(444, 382, "Echo Request (TTL=1)", "#1f63c6"),
              ar(436, 424, 52, "gr", "l"), '<div class="i54-ar i54-gr" style="left:606px;top:424px;width:46px"></div>', lab(502, 416, "Echo Reply", "#2a9a4a")]),
    (464, 2, [sm(894, 466), ar(438, 480, 450, "bl"), lab(596, 457, "Echo Request (TTL=2)", "#1f63c6"),
              ar(436, 501, 186, "gr", "l"), '<div class="i54-ar i54-gr" style="left:736px;top:501px;width:150px"></div>', lab(633, 493, "Echo Reply", "#2a9a4a")]),
    (538, 3, [sm(894, 542), ar(442, 557, 446, "bl"), lab(628, 534, "Echo Request (TTL=3)", "#1f63c6"),
              ar(955, 557, 42, "bl"), '<div class="i54-x i54-fly" style="left:1004px;top:534px;font-size:44px">✕</div>',
              '<div class="i54-ds" style="left:1050px;top:557px;width:118px"></div>',
              lab(1180, 547, "Нет ответа&nbsp; •&nbsp; тайм-аут", "#ec4a2c")]),
]

CARDS = [
    (280, 344, "#2a7fd8", 1, "Увеличиваем TTL", "i54a_ttl.png", (308, 716, 74), 403, 716, 210,
     "Источник отправляет<br>Echo Request с<br>MPLS TTL = 1, 2, 3..."),
    (634, 404, "#3cba86", 2, "Получаем ответы", "i54a_hop.png", (645, 725, 105), 758, 708, 276,
     "На каждом хопе TTL уменьшается. При его истечении запрос обрабатывается локально; узел формирует Echo Reply."),
    (1050, 402, "#f08a60", 3, "Сужаем поиск", "i54a_mag.png", (1078, 716, 84), 1174, 716, 262,
     "Последний ответивший узел и последующие тайм-ауты указывают область возможной неисправности."),
]

HTML = CSS + bg("bgk_19") + "".join([
    '<div class="i54-p" style="left:142px;top:188px;width:1388px;height:448px"></div>',
    '<div class="step">',
    '<div class="i54-h" style="left:172px;top:202px">КАК РАБОТАЕТ ТРАССИРОВКА</div>',
    '<div style="position:absolute;left:432px;top:240px;width:976px;height:22px;border-top:2px solid #1d3f8a;'
    'border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a"></div>',
    '<div class="i54-t" style="left:820px;top:228px;padding:0 10px;background:#fdf8ea;font:800 20px/24px Golos Text;color:#13306e">LSP (MPLS-сеть)</div>',
    '<div style="position:absolute;left:470px;top:292px;width:410px;height:12px;background:#bfe6d6"></div>',
    '<div style="position:absolute;left:1210px;top:292px;width:170px;height:12px;background:#bfe6d6"></div>',
    '<div class="i54-ds" style="left:962px;top:298px;width:170px"></div>',
    '<div class="i54-x" style="left:1022px;top:278px">✕</div>',
    lab(976, 260, "Пример отказа", "#ec4a2c"),
    "".join(rt(x, 266) + '<div class="i54-n" style="left:%dpx;top:332px">%s<div style="font:500 20px/1 Golos Text">%s</div></div>'
            % (x - 37, n, s) + ('<div class="i54-vd" style="left:%dpx;top:378px;height:200px"></div>' % (x + 43) if n != "LER1" else "")
            for x, n, s in NODES),
    '</div>',
    "".join('<div class="step">' + '<div class="i54-ln" style="left:362px;top:%dpx;width:1136px"></div>' % (y - 4)
            + '<div class="i54-ttl" style="left:174px;top:%dpx">MPLS TTL = %d</div>' % (y - 4, k)
            + sm(374, y + 2) + "".join(rows) + '</div>' for y, k, rows in ROWS),
    '<div class="step">',
    img("i54a_info.png", "left:611px;top:591px;width:38px"),
    '<div class="i54-t" style="left:662px;top:598px;font-weight:700;font-size:19px;color:#13306e">Echo Reply возвращается к источнику по IP.</div>',
    '</div>',
    "".join('<div class="step">'
            + '<div class="i54-p" style="left:%dpx;top:652px;width:%dpx;height:170px"></div>' % (x, w)
            + '<div class="i54-num" style="left:%dpx;top:660px;background:%s">%d</div>' % (x + 14, c, k)
            + '<div class="i54-h" style="left:%dpx;top:672px;font-size:25px">%s</div>' % (x + 84, t)
            + img(ic, "left:%dpx;top:%dpx;width:%dpx" % icx)
            + '<div class="i54-t" style="left:%dpx;top:%dpx;width:%dpx;font-weight:500;font-size:17px">%s</div>' % (tx, ty, tw, body)
            + '</div>' for x, w, c, k, t, ic, icx, tx, ty, tw, body in CARDS),
    '<div class="step">',
    '<div class="i54-p" style="left:306px;top:834px;width:1088px;height:84px;border-color:#9fcfc0;background:#e3f4ec"></div>',
    '<div style="position:absolute;left:792px;top:834px;width:602px;height:84px;background:#fde3d8;border-radius:0 22px 22px 0;'
    'border:3px solid #f2b8a4;border-left:0;box-sizing:border-box"></div>',
    img("i54a_gear.png", "left:333px;top:848px;width:67px"),
    '<div class="i54-t" style="left:414px;top:852px;font-weight:700;color:#13306e">Используется TTL заголовка MPLS,<br>а не IP TTL.</div>',
    '<div style="position:absolute;left:770px;top:850px;height:52px;border-left:2px solid #13306e"></div>',
    img("i54a_excl.png", "left:812px;top:838px;width:70px"),
    '<div class="i54-t" style="left:896px;top:852px;color:#13306e"><b style="font-weight:800">Нет ответа ≠ точное доказательство отказа:</b>'
    '<br>возможны фильтрация или проблема обратного IP-пути.</div>',
    '</div>',
])
