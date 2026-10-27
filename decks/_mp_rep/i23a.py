# -*- coding: utf-8 -*-
"""pptx: LSR3 — снятие внешней метки на предпоследнем узле (PHP) — вёрстка поверх чистого фона bgk_05."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 152

CSS = """<style>
.i23-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i23-h{position:absolute;font:900 28px/1 "Rubik",sans-serif;color:#13306e;text-transform:uppercase}
.i23-t{position:absolute;font:500 20px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i23-n{position:absolute;font:900 27px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:200px}
.i23-pk{position:absolute;display:flex;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;background:#fff;height:50px;
 font:700 24px/1 "Golos Text",sans-serif;color:#13306e}
.i23-pk span{display:flex;align-items:center;justify-content:center;border-right:2px solid #1d3f8a}
.i23-pk span:last-child{border-right:0}
.i23-ar{position:absolute;font:900 32px/1 "Golos Text",sans-serif;color:#13306e}
.i23-c{position:absolute;width:112px;height:42px;border:2.5px solid #1d3f8a;border-radius:6px;display:flex;align-items:center;
 justify-content:center;font:700 23px/1 "Golos Text",sans-serif;color:#13306e}
.i23-tb{position:absolute;border-collapse:collapse;font:500 20px/1 "Golos Text",sans-serif;color:#1d2a44;text-align:center;background:#fff}
.i23-tb th{background:#d6ebfb;font-weight:700;height:42px;border:2px solid #1d3f8a}
.i23-tb td{height:42px;border:2px solid #1d3f8a}
.i23-up{animation:i23u 2.6s ease-in-out infinite}
@keyframes i23u{0%,100%{transform:translate(0,0)}50%{transform:translate(4px,-8px)}}
</style>"""

RED, CYAN = "#f2694a", "#3cc3d4"


def pk(x, y, cells):
    s = "".join('<span style="width:%dpx;background:%s">%s</span>' % (w, c, t) for t, c, w in cells)
    return '<div class="i23-pk" style="left:%dpx;top:%dpx">%s</div>' % (x, y, s)


def ar(x):
    return '<div class="i23-ar" style="left:%dpx;top:398px">→</div>' % x


def cell(x, y, t, col):
    return '<div class="i23-c" style="left:%dpx;top:%dpx;background:%s">%s</div>' % (x, y, col, t)


HTML = CSS + bg("bgk_05") + "".join([
    '<div class="step">',
    '<div class="i23-p" style="left:246px;top:160px;width:1178px;height:94px"></div>',
    '<div class="i23-t" style="left:288px;top:172px;width:1120px;font:500 29px/1.25 Golos Text,sans-serif;color:#13306e">'
    '<b style="font-weight:800">LSR3 — предпоследний узел пути LSP1 перед LER2.</b><br>'
    'Вместо замены метки он выполняет <b style="color:#f2694a;font-weight:800">Pop</b> — удаляет верхнюю метку '
    '<b style="color:#1aa6b7;font-weight:800">132</b>.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i23-p" style="left:246px;top:270px;width:1124px;height:298px"></div>',
    '<div style="position:absolute;left:464px;top:308px;width:744px;height:26px;border:2px solid #1d3f8a;border-bottom:0"></div>',
    '<div class="i23-t" style="left:628px;top:282px;width:416px;text-align:center;background:#fdf8ea;font:800 22px/30px Golos Text,sans-serif;color:#13306e">'
    'Завершение внешнего пути LSP1</div>',
    '<div style="position:absolute;left:738px;top:336px;width:196px;height:196px;border-radius:50%;background:radial-gradient(#c8f2dc,rgba(200,242,220,0) 70%)"></div>',
    img("i23a_rt.png", "left:394px;top:380px;width:124px"),
    img("i23a_rt.png", "left:774px;top:378px;width:124px"),
    img("i23a_rt.png", "left:1150px;top:378px;width:124px"),
    ar(522), pk(562, 390, [("132", CYAN, 54), ("315", RED, 54), ("IP", "#fff", 56)]), ar(740),
    ar(904), pk(960, 390, [("315", RED, 60), ("IP", "#fff", 68)]), ar(1094),
    '<div class="i23-up" style="position:absolute;left:862px;top:322px;width:50px;height:36px;background:#3cc3d4;border:2.5px solid #1d3f8a;'
    'border-radius:5px;transform:rotate(-8deg);font:700 21px/34px Golos Text,sans-serif;color:#13306e;text-align:center">132</div>',
    '<div class="i23-t" style="left:936px;top:328px;font-weight:600;color:#13306e">Удаляется</div>',
    '<div class="i23-t" style="left:828px;top:346px;font:900 34px/1 Golos Text;color:#13306e">↗</div>',
    '<div class="i23-n" style="left:356px;top:468px">LSR2</div>',
    '<div class="i23-n" style="left:736px;top:462px">LSR3</div>',
    '<div style="position:absolute;left:768px;top:492px;width:136px;height:38px;background:#f2694a;border-radius:12px;'
    'font:700 25px/38px Golos Text,sans-serif;color:#fff;text-align:center">Pop 132</div>',
    '<div class="i23-n" style="left:1112px;top:468px">LER2</div>',
    '<div class="i23-t" style="left:1060px;top:500px;width:304px;text-align:center;font-weight:600;color:#13306e">Продолжение по LSP3</div>',
    '<div class="i23-t" style="left:600px;top:538px;width:476px;text-align:center;font-size:18px;color:#13306e">Верхняя метка показана слева.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i23-p" style="left:246px;top:584px;width:588px;height:230px"></div>',
    '<div class="i23-h" style="left:274px;top:596px">Как изменяется стек</div>',
    '<div class="i23-t" style="left:300px;top:632px;width:150px;text-align:center;font-weight:800;font-size:22px;color:#13306e">До</div>',
    '<div class="i23-t" style="left:600px;top:632px;width:150px;text-align:center;font-weight:800;font-size:22px;color:#13306e">После</div>',
    cell(296, 664, "132", CYAN), cell(296, 708, "315", RED), cell(296, 752, "IP", "#fff"),
    '<div class="i23-t" style="left:420px;top:676px;font-size:18px">LSP1</div><div class="i23-t" style="left:420px;top:718px;font-size:18px">LSP3</div>',
    '<div class="i23-t" style="left:500px;top:676px;font:800 23px/1 Golos Text;color:#f2694a">Pop</div>',
    '<div class="i23-t" style="left:492px;top:700px;font:900 40px/1 Golos Text;color:#f2694a">→</div>',
    cell(588, 676, "315", RED), cell(588, 724, "IP", "#fff"),
    '<div class="i23-t" style="left:698px;top:688px;font-size:17px">Новая вершина</div>',
    '</div>',
    '<div class="step">',
    '<div class="i23-p" style="left:846px;top:584px;width:524px;height:230px"></div>',
    '<div class="i23-h" style="left:868px;top:596px">Запись в  таблице LSR3</div>',
    '<table class="i23-tb" style="left:864px;top:636px;width:490px"><tr><th>Вход</th><th>Метка</th><th>Выход</th><th>Действие</th></tr>'
    '<tr><td>S0</td><td>132</td><td>S1</td><td style="font-weight:700">Pop</td></tr></table>',
    '<div style="position:absolute;left:864px;top:734px;width:490px;height:66px;background:#d6ebfb;border-radius:10px"></div>',
    '<div class="i23-t" style="left:890px;top:740px;width:460px;font-size:19px;color:#13306e"><b style="font-weight:700">PHP — Penultimate Hop Popping</b><br>'
    'Снятие метки на предпоследнем узле.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i23-p" style="left:322px;top:830px;width:1030px;height:86px;border-radius:16px"></div>',
    '<div class="i23-t" style="left:322px;top:840px;width:1030px;text-align:center;font:800 26px/1.2 Golos Text,sans-serif;color:#13306e">'
    'Метка <span style="color:#1aa6b7">132</span> удалена. Метка <span style="color:#f2694a">315</span> пути LSP3 становится верхней.<br>'
    '<span style="font-weight:500;font-size:22px">Пакет остаётся MPLS-пакетом: в стеке ещё есть метка.</span></div>',
    '</div>',
])
