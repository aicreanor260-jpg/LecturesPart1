# -*- coding: utf-8 -*-
"""pptx: инжиниринг трафика — strict / loose — вёрстка поверх bgk_28."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 110

CSS = """<style>
.i56-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i56-h{position:absolute;font:900 30px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i56-t{position:absolute;font:500 20px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i56-b{position:absolute;font:800 26px/1.25 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i56-bar{position:absolute;border-radius:14px;font:800 30px/50px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i56-ft{position:absolute;border-radius:14px;font:700 20px/44px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i56-n{position:absolute;font:800 22px/1 "Golos Text",sans-serif;color:#13306e;width:100px;text-align:center}
.i56-ar{position:absolute;height:4px}
.i56-ar::after{content:"";position:absolute;right:-4px;top:-7px;border:9px solid transparent;border-left:14px solid currentColor;border-right:0}
.i56-vs{position:absolute;width:0;border-left:2px solid #6d7c99;height:86px}
.i56-glow{animation:i56g 2.4s ease-in-out infinite}
@keyframes i56g{0%,100%{opacity:1}50%{opacity:.8}}
</style>"""


def ar(x, y, w, c):
    return '<div class="i56-ar" style="left:%dpx;top:%dpx;width:%dpx;color:%s;background:%s"></div>' % (x, y, w, c, c)


def rt(x, y, w=95):
    return img("i56a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


def nm(x, y, t):
    return '<div class="i56-n" style="left:%dpx;top:%dpx">%s</div>' % (x, y, t)


WHO = [(200, "i56a_c1.png", "Входной LER", "инициирует установление<br>туннеля"),
       (640, "i56a_c2.png", "Расчёт пути", "входной LER, внешняя система<br>или администратор"),
       (1105, "i56a_c3.png", "Сигнализация", "RSVP-TE устанавливает LSP")]

HTML = CSS + bg("bgk_28") + "".join([
    '<div class="step">',
    '<div class="i56-p" style="left:172px;top:116px;width:1330px;height:88px"></div>',
    '<div class="i56-b" style="left:172px;top:126px;width:1330px;font-weight:600"><b style="font-weight:900">MPLS TE</b> '
    'направляет трафик по LSP с учётом ресурсов сети и заданных ограничений.<br>Такие LSP называют TE-туннелями.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i56-p" style="left:172px;top:214px;width:1330px;height:210px"></div>',
    '<div class="i56-h" style="left:188px;top:228px">КТО ЗАДАЁТ ПУТЬ</div>',
    "".join(img(ic, "left:%dpx;top:260px;width:100px" % x)
            + '<div class="i56-t" style="left:%dpx;top:270px;font:800 25px/1 Golos Text;color:#13306e">%s</div>' % (x + 118, t)
            + '<div class="i56-t" style="left:%dpx;top:306px;font-size:19px">%s</div>' % (x + 118, s)
            for x, ic, t, s in WHO),
    '<div class="i56-vs" style="left:600px;top:268px"></div><div class="i56-vs" style="left:1078px;top:268px"></div>',
    '<div class="i56-ft" style="left:192px;top:366px;width:1292px;height:44px;background:#cfeee2;font-weight:500"></div>',
    img("i56a_doc.png", "left:430px;top:368px;width:42px"),
    '<div class="i56-t" style="left:492px;top:377px;font-size:20px"><b style="font-weight:800;color:#13306e">OSPF-TE / IS-IS-TE</b> '
    'распространяют характеристики каналов для расчёта пути</div>',
    '</div>',
    # strict
    '<div class="step">',
    '<div class="i56-p" style="left:214px;top:436px;width:620px;height:310px"></div>',
    '<div class="i56-bar" style="left:224px;top:444px;width:600px;background:#f8c4b4">Строгий маршрут • Strict</div>',
    '<div class="i56-t" style="left:214px;top:500px;width:620px;text-align:center">Задана вся последовательность соседних узлов.</div>',
    rt(250, 567), rt(404, 567), rt(554, 567), rt(704, 567),
    ar(346, 600, 54, "#ef6a48"), ar(498, 600, 52, "#ef6a48"), ar(650, 600, 50, "#ef6a48"),
    nm(248, 644, "LER1"), nm(402, 644, "LSR1"), nm(552, 644, "LSR2"), nm(702, 644, "LER2"),
    '<div class="i56-ft" style="left:232px;top:692px;width:586px;background:#f8d3c8">Каждый переход задан явно.</div>',
    '</div>',
    # loose
    '<div class="step">',
    '<div class="i56-p" style="left:846px;top:436px;width:656px;height:310px"></div>',
    '<div class="i56-bar" style="left:856px;top:444px;width:636px;background:#bfe8d8">Свободный маршрут • Loose</div>',
    '<div class="i56-t" style="left:846px;top:500px;width:656px;text-align:center">Заданы только обязательные опорные узлы.</div>',
    img("i56a_cloud.png", "left:962px;top:535px;width:310px", "ab i56-glow"),
    rt(864, 567), ar(952, 600, 36, "#1d4f6e"), ar(1240, 600, 34, "#1d4f6e"),
    rt(1280, 567), ar(1370, 600, 28, "#ef6a48"), rt(1400, 567, 80),
    nm(858, 638, "LER1"), nm(1272, 638, "LSR2"), nm(1388, 638, "LER2"),
    '<div class="i56-ft" style="left:862px;top:690px;width:580px;background:#cfeee2">Путь между опорными узлами уточняется в сети.</div>',
    '</div>',
    # итог
    '<div class="step">',
    '<div class="i56-p" style="left:278px;top:760px;width:1128px;height:122px"></div>',
    img("i56a_bulb.png", "left:296px;top:773px;width:98px"),
    '<div class="i56-t" style="left:414px;top:780px;font:800 27px/1 Golos Text;color:#13306e">Главное отличие от обычного LDP</div>',
    '<div class="i56-t" style="left:414px;top:818px;font-size:19px">ТЕ-туннель строится по выбранному маршруту<br>'
    'с ограничениями; обычный LDP следует маршрутам IGP.</div>',
    '<div class="i56-vs" style="left:962px;top:782px;height:80px"></div>',
    img("i56a_loop.png", "left:978px;top:788px;width:174px"),
    '<div class="i56-t" style="left:1168px;top:788px;font-size:19px;color:#13306e">Один явный маршрут<br>может сочетать строгие<br>и свободные участки.</div>',
    '</div>',
])
