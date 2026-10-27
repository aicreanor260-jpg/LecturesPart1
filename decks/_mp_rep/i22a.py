# -*- coding: utf-8 -*-
"""pptx: два пути на входе LER1, замена верхней метки в LSR2 — вёрстка поверх чистого фона bgk_04."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 156

CSS = """<style>
.i22-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i22-h{position:absolute;font:900 26px/1 "Rubik",sans-serif;color:#13306e;text-transform:uppercase}
.i22-t{position:absolute;font:500 19px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i22-n{position:absolute;font:900 23px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:220px}
.i22-s{position:absolute;font:500 19px/1 "Golos Text",sans-serif;color:#1d2a44;text-align:center;width:220px}
.i22-pk{position:absolute;display:flex;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;background:#fff;
 font:700 20px/1 "Golos Text",sans-serif;color:#13306e}
.i22-pk span{display:flex;align-items:center;justify-content:center;border-right:2px solid #1d3f8a}
.i22-pk span:last-child{border-right:0}
.i22-ar{position:absolute;font:900 30px/1 "Golos Text",sans-serif;color:#13306e}
.i22-tb{position:absolute;border-collapse:collapse;font:500 19px/1 "Golos Text",sans-serif;color:#1d2a44;text-align:center;background:#fff}
.i22-tb th{background:#d6ebfb;font-weight:700;height:38px;border:2px solid #1d3f8a}
.i22-tb td{height:38px;border:2px solid #1d3f8a}
.i22-lb{display:inline-block;padding:0 10px;border-radius:6px;font-weight:800}
.i22-fly{animation:i22f 3s ease-in-out infinite}
@keyframes i22f{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}
</style>"""

RED, CYAN = "#f2694a", "#5bd0f2"


def pk(x, y, cells, h=44, fs=20):
    s = "".join('<span style="width:%dpx;background:%s">%s</span>' % (w, c, t) for t, c, w in cells)
    return '<div class="i22-pk i22-fly" style="left:%dpx;top:%dpx;height:%dpx;font-size:%dpx">%s</div>' % (x, y, h, fs, s)


def node(x, name, sub):
    return img("i22a_rt.png", "left:%dpx;top:380px;width:100px" % x) + \
        '<div class="i22-n" style="left:%dpx;top:454px">%s</div>' % (x - 60, name) + \
        '<div class="i22-s" style="left:%dpx;top:481px">%s</div>' % (x - 60, sub)


def ar(x, y=402):
    return '<div class="i22-ar" style="left:%dpx;top:%dpx">→</div>' % (x, y)


IP = ("IP", "#fff", 50)

HTML = CSS + bg("bgk_04") + "".join([
    '<div class="step">',
    '<div class="i22-p" style="left:120px;top:160px;width:1432px;height:96px"></div>',
    '<div class="i22-t" style="left:152px;top:172px;width:1380px;font:700 29px/1.25 Golos Text,sans-serif;color:#13306e">'
    'В LER1 начинаются два пути: внешний LSP1 и внутренний LSP3.<br>Сначала добавляется метка '
    '<span class="i22-lb" style="background:#f2694a">315</span>, затем поверх неё — метка '
    '<span class="i22-lb" style="background:#5bd0f2">256</span>.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i22-p" style="left:62px;top:272px;width:1544px;height:318px"></div>',
    '<div class="i22-h" style="left:88px;top:290px">LSP1 переносит пакет с внутренней меткой LSP3</div>',
    '<div style="position:absolute;left:180px;top:330px;width:1320px;height:210px;border-radius:110px;background:#c6eee6"></div>',
    '<div style="position:absolute;left:318px;top:350px;width:986px;height:16px;border:2px solid #1d3f8a;border-bottom:0;border-radius:10px 10px 0 0"></div>',
    '<div class="i22-t" style="left:690px;top:336px;width:290px;text-align:center;background:#c6eee6;font:800 22px/30px Golos Text,sans-serif;color:#13306e">'
    'MPLS-домен 1 • LSP1</div>',
    pk(90, 396, [IP], 44), ar(196),
    node(238, "LER1", "Push 315; Push 256"), ar(344),
    pk(380, 396, [("256", CYAN, 50), ("315", RED, 50), IP]), ar(534),
    node(556, "LSR1", "Swap 256 → 272"), ar(656),
    pk(680, 396, [("272", CYAN, 46), ("315", RED, 46), ("IP", "#fff", 44)]), ar(826),
    node(838, "LSR2", "Swap 272 → 132"), ar(936),
    pk(960, 396, [("132", CYAN, 46), ("315", RED, 46), ("IP", "#fff", 40)]), ar(1086),
    node(1106, "LSR3", "Pop 132"), ar(1202),
    pk(1236, 396, [("315", RED, 50), ("IP", "#fff", 44)]), ar(1332),
    node(1356, "LER2", "Далее по LSP3"), ar(1456),
    pk(1492, 396, [IP], 44),
    '<div style="position:absolute;left:300px;top:510px;width:1090px;height:30px;border-bottom:3px dashed #6b6b6b;border-radius:0 0 50% 50%"></div>',
    '<div class="i22-t" style="left:660px;top:524px;width:380px;text-align:center;background:#c6eee6;font-weight:600;color:#555">'
    'LSP3: LER1 → LER2 → LER3 → LER4</div>',
    '<div class="i22-t" style="left:62px;top:562px;width:1544px;text-align:center;font-weight:700;font-size:18px;color:#13306e">'
    'Верхняя метка показана слева. Внутренняя метка 315 сохраняется внутри домена 1.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i22-p" style="left:204px;top:606px;width:632px;height:164px"></div>',
    '<div class="i22-h" style="left:226px;top:618px">Запись на LER1</div>',
    '<table class="i22-tb" style="left:222px;top:652px;width:594px"><tr><th>Вход</th><th>Классификация</th><th>Выход</th><th>Действия</th></tr>'
    '<tr><td>S0</td><td>IP / FEC</td><td>S1</td><td>Push 315; Push 256</td></tr></table>',
    '<div class="i22-t" style="left:224px;top:736px;width:600px;font-size:17px">Порядок важен: 315 — внутренняя, 256 — верхняя.</div>',
    '<div class="i22-p" style="left:852px;top:606px;width:540px;height:164px"></div>',
    '<div class="i22-h" style="left:874px;top:618px">Запись на LSR2</div>',
    '<table class="i22-tb" style="left:872px;top:652px;width:502px"><tr><th>Вход</th><th>Метка</th><th>Выход</th><th>Действие</th></tr>'
    '<tr><td>S0</td><td>272</td><td>S1</td><td>Swap 132</td></tr></table>',
    '<div class="i22-t" style="left:872px;top:736px;width:520px;font-size:16px">LSR2 заменяет только верхнюю метку и отправляет кадр в LSR3.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i22-p" style="left:358px;top:786px;width:936px;height:116px"></div>',
    pk(498, 802, [("272", CYAN, 80), ("315", RED, 82), ("IP", "#fff", 64)], 48, 26),
    '<div class="i22-t" style="left:748px;top:806px;width:200px;font:800 30px/1 Golos Text,sans-serif;color:#13306e">→ LSR2 →</div>',
    pk(946, 802, [("132", CYAN, 76), ("315", RED, 82), ("IP", "#fff", 64)], 48, 26),
    '<div class="i22-t" style="left:358px;top:862px;width:936px;text-align:center;font:700 23px/1 Golos Text,sans-serif;color:#13306e">'
    'Внутренняя метка 315 не изменяется.</div>',
    '</div>',
])
