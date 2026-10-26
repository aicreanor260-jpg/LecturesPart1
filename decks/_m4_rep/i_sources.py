# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 125

CSS = """<style>
.m4x-src-p{position:absolute;box-sizing:border-box;border:1.5px solid rgba(240,199,94,.55);border-radius:26px;
  background:linear-gradient(180deg,rgba(14,70,52,.55),rgba(5,32,24,.78));box-shadow:0 0 22px rgba(240,199,94,.18),inset 0 0 40px rgba(0,0,0,.35)}
.m4x-src-h{position:absolute;text-align:center;font:800 29px/1 "Playfair Display",serif;white-space:nowrap;
  background:linear-gradient(180deg,#fff0b8,#e8b84a 55%,#b88a2a);-webkit-background-clip:text;background-clip:text;color:transparent}
.m4x-src-hb{font-size:42px;text-transform:uppercase}
.m4x-src-t{position:absolute;text-align:center;font:500 25px/31px "Golos Text",sans-serif;color:#f1ead2}
.m4x-src-pill{position:absolute;box-sizing:border-box;border:1.5px solid rgba(240,199,94,.7);border-radius:14px;background:rgba(4,36,28,.85);
  text-align:center;font:900 38px/54px "Playfair Display",serif;color:#f6e3a0;box-shadow:0 0 12px rgba(240,199,94,.18)}
.m4x-src-tab{position:absolute;left:91px;top:583px;width:1491px;height:255px;box-sizing:border-box;border:1.5px solid rgba(240,199,94,.6);border-radius:14px;overflow:hidden;
  background:rgba(4,34,26,.8)}
.m4x-src-hd{position:absolute;left:0;top:0;width:100%;height:38px;background:linear-gradient(180deg,#14604a,#0b3f31);border-bottom:1px solid rgba(240,199,94,.6)}
.m4x-src-row{position:absolute;left:0;width:100%;height:36px;border-bottom:1px solid rgba(240,199,94,.4)}
.m4x-src-c1{position:absolute;left:0;width:565px;text-align:center;font:800 28px/36px "Playfair Display",serif;color:#f6e3a0}
.m4x-src-c2{position:absolute;left:757px;font:500 25px/36px "Golos Text",sans-serif;color:#f1ead2}
.m4x-src-vl{position:absolute;left:565px;top:0;width:1px;height:100%;background:rgba(240,199,94,.55)}
.m4x-src-hd .m4x-src-c1,.m4x-src-hd .m4x-src-c2{font:700 24px/38px "Golos Text",sans-serif;color:#f6e3a0}
.m4x-src-dia{position:absolute;width:11px;height:11px;background:#f0c75e;transform:rotate(45deg);box-shadow:0 0 8px #f0c75e}
.m4x-src-ln{position:absolute;height:1px;background:linear-gradient(90deg,transparent,rgba(240,199,94,.6),transparent)}
.m4x-src-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
</style>"""


def divider(cx, y, half):
    return ('<div class="m4x-src-ln" style="left:%dpx;top:%dpx;width:%dpx"></div><div class="m4x-src-dia" style="left:%dpx;top:%dpx"></div>'
            % (cx - half, y, 2 * half, cx - 5, y - 5))


def head(cx, title):
    return '<div class="m4x-src-h" style="left:%dpx;width:600px;margin-left:-300px;top:148px">%s</div>' % (cx, title)


def panel(x, y, w, h, r=26):
    return '<div class="m4x-src-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:%dpx"></div>' % (x, y, w, h, r)


def pill(x, w, code):
    return '<div class="m4x-src-pill" style="left:%dpx;top:428px;width:%dpx;height:56px">%s</div>' % (x, w, code)


def im(n, x, y, w):
    return img("i_sources_%s.png" % n, "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


def colblock(px, pw, title, svg, imgs, text, ty, pl):
    cx = px + pw // 2
    return ('<div class="step">' + panel(px, 133, pw, 367) + head(cx, title) + divider(cx, 196, 200) + imgs
            + '<svg class="m4x-src-sv" viewBox="0 0 1672 941">' + svg + '</svg>'
            + '<div class="m4x-src-t" style="left:%dpx;width:%dpx;top:%dpx">%s</div>' % (px, pw, ty, text) + pl + '</div>')


GL = 'style="filter:drop-shadow(0 0 5px #3fd6b0)"'
c1 = colblock(47, 520, "Прямое подключение",
    '<line x1="258" y1="283" x2="425" y2="283" stroke="#3fd6b0" stroke-width="4" ' + GL + '/>'
    '<g stroke="#3fd6b0" stroke-linecap="round" opacity=".6"><line x1="455" y1="268" x2="545" y2="268" stroke-width="2"/>'
    '<line x1="455" y1="283" x2="548" y2="283" stroke-width="3"/><line x1="455" y1="298" x2="540" y2="298" stroke-width="2"/></g>',
    im("r1", 100, 225, 170) + im("lens", 405, 245, 150),
    "Интерфейс настроен<br>и активен", 352, pill(227, 168, "C"))
c2 = colblock(585, 504, "Статический маршрут",
    '<g fill="#3fd6b0" ' + GL + '><circle cx="808" cy="280" r="4"/><circle cx="828" cy="280" r="4"/><circle cx="848" cy="280" r="4"/><circle cx="868" cy="280" r="4"/></g>',
    im("r2", 635, 225, 160) + im("doc", 875, 210, 140),
    "Настроен вручную,<br>выходной интерфейс активен", 354, pill(757, 161, "S"))
c3 = colblock(1107, 522, "Динамическая маршрутизация",
    '<defs><marker id="m4xsa" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#3fd6b0"/></marker></defs>'
    '<line x1="1298" y1="252" x2="1425" y2="252" stroke="#3fd6b0" stroke-width="4" marker-end="url(#m4xsa)" ' + GL + '/>'
    '<line x1="1432" y1="308" x2="1305" y2="308" stroke="#3fd6b0" stroke-width="4" marker-end="url(#m4xsa)" ' + GL + '/>'
    '<g fill="#e8f7f0"><circle cx="1297" cy="280" r="4"/><circle cx="1322" cy="280" r="4"/><circle cx="1347" cy="280" r="4"/>'
    '<circle cx="1372" cy="280" r="4"/><circle cx="1397" cy="280" r="4"/><circle cx="1436" cy="280" r="4"/></g>',
    im("r3", 1140, 230, 145) + im("r4", 1448, 230, 147),
    "Сеть изучена протоколом<br>маршрутизации", 355,
    '<div class="m4x-src-pill" style="left:1174px;top:428px;width:389px;height:56px;display:flex;justify-content:space-around;padding:0 50px"><span>R</span><span>O</span><span>i</span><span>B</span></div>')

rows = [("C", "Прямое подключение"), ("S", "Статический маршрут"), ("R", "RIP"), ("O", "OSPF"), ("i", "IS-IS"), ("B", "BGP")]
tab = ('<div class="m4x-src-tab"><div class="m4x-src-hd"><div class="m4x-src-c1">Код</div><div class="m4x-src-c2">Источник</div></div>'
       + "".join('<div class="m4x-src-row" style="top:%dpx"><div class="m4x-src-c1">%s</div><div class="m4x-src-c2">%s</div></div>'
                 % (38 + i * 36, a, b) for i, (a, b) in enumerate(rows))
       + '<div class="m4x-src-vl"></div></div>')
codes = ('<div class="step">' + panel(47, 520, 1580, 332)
         + '<div class="m4x-src-h m4x-src-hb" style="left:837px;width:900px;margin-left:-450px;top:520px">Коды источников</div>'
         + divider(837, 569, 380) + tab + '</div>')
foot = ('<div class="step">' + panel(47, 862, 1580, 49, 20)
        + '<div class="m4x-src-t" style="left:47px;width:1580px;top:870px;line-height:34px">Код показывает, каким способом получен маршрут.</div></div>')

HTML = CSS + bg() + "".join([c1, c2, c3, codes, foot])
