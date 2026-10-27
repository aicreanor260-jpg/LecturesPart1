# -*- coding: utf-8 -*-
"""pptx: LER2 — замена метки LSP3 и вход в LSP2 (Swap → Push) — вёрстка поверх чистого фона bgk_21."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 158

CSS = """<style>
.i24-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i24-h{position:absolute;font:900 26px/1 "Rubik",sans-serif;color:#13306e}
.i24-t{position:absolute;font:500 19px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i24-bx{position:absolute;background:#c6ebe4;border-radius:18px}
.i24-num{position:absolute;width:34px;height:34px;border-radius:50%;background:#1e8a8a;color:#fff;font:800 20px/34px "Golos Text";text-align:center}
.i24-pk{position:absolute;display:flex;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;background:#fff;
 font:700 25px/1 "Golos Text",sans-serif;color:#13306e}
.i24-pk span{display:flex;align-items:center;justify-content:center;border-right:2px solid #1d3f8a}
.i24-pk span:last-child{border-right:0}
.i24-op{position:absolute;display:flex;align-items:center;justify-content:center;background:#fdd44f;
 clip-path:polygon(0 18%,78% 18%,78% 0,100% 50%,78% 100%,78% 82%,0 82%);font:800 22px/1.05 "Golos Text",sans-serif;color:#13306e;text-align:center;padding-right:24px;z-index:2}
.i24-tb{position:absolute;border-collapse:collapse;font:500 19px/1.2 "Golos Text",sans-serif;color:#1d2a44;text-align:center;background:#fff}
.i24-tb th{background:#d6ebfb;font-weight:600;height:54px;border:2px solid #1d3f8a}
.i24-tb td{height:64px;border:2px solid #1d3f8a}
.i24-y{position:absolute;background:#fde27a;border:3px solid #1f63c6;border-radius:16px}
.i24-fly{animation:i24f 3s ease-in-out infinite}
@keyframes i24f{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}
</style>"""

RED, TEAL = "#f2694a", "#55cfc8"


def pk(x, y, cells, h=58, fs=25, cls=""):
    s = "".join('<span style="width:%dpx;background:%s">%s</span>' % (w, c, t) for t, c, w in cells)
    return '<div class="i24-pk %s" style="left:%dpx;top:%dpx;height:%dpx;font-size:%dpx">%s</div>' % (cls, x, y, h, fs, s)


def stage(x, w, n, title):
    return '<div class="i24-bx" style="left:%dpx;top:336px;width:%dpx;height:176px"></div>' % (x, w) + \
        '<div class="i24-num" style="left:%dpx;top:346px">%s</div>' % (x + 56, n) + \
        '<div class="i24-t" style="left:%dpx;top:351px;font-size:21px;color:#13306e;font-weight:600">%s</div>' % (x + 108, title)


HTML = CSS + bg("bgk_21") + "".join([
    '<div class="step">',
    '<div class="i24-p" style="left:216px;top:166px;width:1236px;height:88px"></div>',
    '<div class="i24-t" style="left:216px;top:176px;width:1236px;text-align:center;font-size:25px;color:#13306e">'
    'LER2 получает на интерфейсе S0 пакет с меткой 315 и обрабатывает его по записи таблицы<br>'
    'продвижения: сначала заменяет 315 на 317, затем добавляет сверху метку 188.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i24-p" style="left:254px;top:268px;width:1170px;height:322px"></div>',
    '<div class="i24-h" style="left:282px;top:284px;font-size:34px">Две операции над стеком: Swap → Push</div>',
    stage(276, 316, "1", "На входе LER2"),
    pk(346, 394, [("315", RED, 78), ("IP", "#fff", 100)]),
    '<div class="i24-t" style="left:276px;top:462px;width:316px;text-align:center;font-size:20px">Метка LSP3: 315</div>',
    '<div class="i24-op" style="left:566px;top:378px;width:160px;height:94px">Swap<br>315 → 317</div>',
    stage(690, 278, "2", "После замены"),
    pk(742, 394, [("317", RED, 76), ("IP", "#fff", 96)]),
    '<div class="i24-t" style="left:690px;top:462px;width:278px;text-align:center;font-size:20px">Метка LSP3: 317</div>',
    '<div class="i24-op" style="left:948px;top:378px;width:132px;height:94px">Push<br>188</div>',
    stage(1054, 354, "3", "На выходе LER2"),
    pk(1112, 390, [("188", TEAL, 72), ("317", RED, 70), ("IP", "#fff", 88)], 56, 25, "i24-fly"),
    '<div class="i24-t" style="left:1124px;top:452px;font-size:16px">S = 0</div><div class="i24-t" style="left:1198px;top:452px;font-size:16px">S = 1</div>',
    '<div class="i24-t" style="left:1062px;top:482px;width:350px;font-size:17px;line-height:1.35">188 — верхняя, транспортная метка LSP2<br>'
    '317 — нижняя метка LSP3</div>',
    '<div style="position:absolute;left:276px;top:542px;width:1130px;height:36px;background:#d6ebfb;border-radius:8px;'
    'font:600 20px/36px Golos Text,sans-serif;color:#13306e;text-align:center">'
    'Верхняя метка показана слева. Метка 317 остаётся под новой меткой 188.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i24-p" style="left:296px;top:604px;width:566px;height:222px"></div>',
    '<div class="i24-h" style="left:318px;top:616px">Запись таблицы продвижения LER2</div>',
    '<table class="i24-tb" style="left:316px;top:652px;width:530px"><tr><th>Входной<br>интерфейс</th><th>Метка</th>'
    '<th>Выходной<br>интерфейс</th><th style="width:180px">Действия</th></tr>'
    '<tr><td>S0</td><td>315</td><td>S1</td><td>Swap 317;<br>Push 188</td></tr></table>',
    '<div class="i24-t" style="left:318px;top:784px;font-size:17px">S0 и S1 — условные обозначения интерфейсов.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i24-p" style="left:876px;top:604px;width:524px;height:222px"></div>',
    '<div class="i24-h" style="left:900px;top:616px">Далее — по пути LSP2</div>',
    '<div class="i24-t" style="left:900px;top:654px;width:100px;text-align:center;font-weight:700;color:#13306e">LER2</div>',
    '<div class="i24-t" style="left:1114px;top:654px;width:100px;text-align:center;font-weight:700;color:#13306e">LER3</div>',
    '<div class="i24-t" style="left:1272px;top:654px;width:100px;text-align:center;font-weight:700;color:#13306e">LSR4</div>',
    img("i24a_rt.png", "left:900px;top:680px;width:94px"),
    img("i24a_rt.png", "left:1124px;top:680px;width:94px"),
    img("i24a_rt.png", "left:1278px;top:680px;width:94px"),
    pk(998, 696, [("188", TEAL, 38), ("317", RED, 36), ("IP", "#fff", 30)], 28, 15, "i24-fly"),
    '<div style="position:absolute;left:1222px;top:710px;width:48px;height:2px;background:#13306e"></div>'
    '<div class="i24-t" style="left:1258px;top:696px;font:900 22px/1 Golos Text">›</div>',
    '<div class="i24-t" style="left:900px;top:752px;width:490px;font-size:16.5px;line-height:1.3">Пакет передаётся в домен 2. Внутренние LSR продвигают '
    'его по верхней метке LSP2; нижняя метка LSP3 сохраняется до завершения транспортного участка.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i24-y" style="left:272px;top:838px;width:1128px;height:80px"></div>',
    img("i24a_bulb.png", "left:306px;top:838px;width:80px"),
    '<div class="i24-t" style="left:422px;top:846px;width:970px;font:600 24px/1.25 Golos Text,sans-serif;color:#13306e">'
    'Добавление новой метки не требует отдельного „перемещения на дно“:<br>операция Push помещает её поверх существующего стека.</div>',
    '</div>',
])
