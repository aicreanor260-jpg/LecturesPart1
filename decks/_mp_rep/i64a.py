# -*- coding: utf-8 -*-
"""pptx: Использование иерархии меток для быстрой защиты — схема и стек меток, фон bgk_12."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 140

CSS = """<style>
.i64-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i64-h{position:absolute;font:900 28px/1 "Rubik",sans-serif;color:#13306e}
.i64-t{position:absolute;font:500 21px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i64-sub{position:absolute;font:500 24px/1.4 "Golos Text",sans-serif;color:#fff;text-shadow:0 2px 4px rgba(0,40,100,.55)}
.i64-n{position:absolute;font:800 24px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:120px}
.i64-l{position:absolute;font:800 24px/1 "Golos Text",sans-serif;color:#13306e}
.i64-y{position:absolute;background:#ffd25a;border-radius:10px;font:700 19px/34px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i64-g{position:absolute;background:#c9eedc;border-radius:8px;font:800 21px/34px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i64-c{position:absolute;background:#d3f1e8;border:2px solid #bfe3d6;border-radius:16px}
.i64-cn{position:absolute;font:900 34px/1 "Rubik",sans-serif;color:#13306e}
.i64-st{position:absolute;width:104px;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;font:800 23px/36px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i64-st div{border-top:2px solid #1d3f8a}.i64-st div:first-child{border-top:0}
.i64-gr{background:#5fd39c}.i64-rd{background:#f2694a}.i64-ip{background:#fdf0cf}
.i64-arw{position:absolute;font:900 46px/1 "Golos Text",sans-serif;color:#24577a}
.i64-fly{animation:i64f 2.4s ease-in-out infinite}
@keyframes i64f{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
</style>"""


def rt(x, name, y=365, w=100):
    return img("i64a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w)) + \
        '<div class="i64-n" style="left:%dpx;top:%dpx">%s</div>' % (x + w // 2 - 60, y + 78, name)


def st(x, y, cells):
    return '<div class="i64-st i64-fly" style="left:%dpx;top:%dpx">%s</div>' % (
        x, y, "".join('<div class="i64-%s">%s</div>' % (c, t) for c, t in cells))


def card(x, w, name, text, cells, sy):
    return ('<div class="i64-c" style="left:%dpx;top:576px;width:%dpx;height:148px"></div>' % (x, w) +
            '<div class="i64-cn" style="left:%dpx;top:598px">%s</div>' % (x + 50, name) +
            '<div class="i64-t" style="left:%dpx;top:644px;font-weight:600">%s</div>' % (x + 50, text) +
            st(x + w - 130, sy, cells))


HTML = CSS + bg("bgk_12") + "".join([
    '<div class="i64-sub" style="left:224px;top:146px">При отказе линии пакет направляется в заранее подготовленный обходной LSP.<br>'
    'Внешняя метка ведёт по обходу, внутренняя сохраняет основной путь.</div>',
    # схема
    '<div class="step">',
    '<div class="i64-p" style="left:244px;top:230px;width:1350px;height:284px"></div>',
    '<div class="i64-h" style="left:266px;top:246px">СХЕМА РАБОТЫ</div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941">'
    '<line x1="500" y1="400" x2="714" y2="400" style="stroke:#1d3f8a;stroke-width:4"/>'
    '<line x1="1166" y1="400" x2="1382" y2="400" style="stroke:#1d3f8a;stroke-width:4"/>'
    '<line x1="808" y1="400" x2="1074" y2="400" style="stroke:#e8402c;stroke-width:4;stroke-dasharray:12 8"/>'
    '<line x1="780" y1="370" x2="896" y2="310" style="stroke:#27c08a;stroke-width:6;stroke-dasharray:10 6"/>'
    '<line x1="982" y1="310" x2="1104" y2="372" style="stroke:#27c08a;stroke-width:6;stroke-dasharray:10 6"/>'
    '</svg>',
    rt(402, "LSR1"), rt(711, "LSR2"), rt(1071, "LSR7"), rt(1380, "LSR8"),
    img("i64a_rt.png", "left:890px;top:272px;width:96px"),
    '<div class="i64-n" style="left:878px;top:246px">LSR3</div>',
    '<div class="i64-g" style="left:880px;top:342px;width:116px">B-LSP1</div>',
    '<div class="i64-l" style="left:594px;top:368px">15</div>', '<div class="i64-l" style="left:1282px;top:368px">21</div>',
    '<div class="i64-l" style="left:818px;top:308px">7</div>', '<div class="i64-l" style="left:1058px;top:308px">8</div>',
    '<div class="i64-l" style="left:924px;top:418px">17</div>',
    '<div class="i64-l" style="left:922px;top:380px;color:#e8402c;font-size:30px">✕</div>',
    '<div class="i64-l" style="left:876px;top:442px;color:#e8402c;font-size:19px">Отказ линии</div>',
    '<div class="i64-y" style="left:668px;top:468px;width:184px">Начало обхода</div>',
    '<div class="i64-y" style="left:1026px;top:468px;width:196px">Возврат в LSP1</div>',
    '</div>',
    # стек
    '<div class="step">',
    '<div class="i64-p" style="left:322px;top:526px;width:1272px;height:288px"></div>',
    '<div class="i64-h" style="left:350px;top:538px;font-size:26px">КАК МЕНЯЕТСЯ СТЕК МЕТОК</div>',
    card(352, 372, "LSR2", "Swap 15 → 17,<br>затем Push 7", [("gr", "7"), ("rd", "17"), ("ip", "IP")], 592),
    '<div class="i64-arw" style="left:732px;top:634px">➞</div>',
    card(784, 358, "LSR3", "Swap внешней<br>метки 7 → 8", [("gr", "8"), ("rd", "17"), ("ip", "IP")], 592),
    '<div class="i64-arw" style="left:1152px;top:634px">➞</div>',
    card(1206, 364, "LSR7", "Pop 8, затем<br>Swap 17 → 21", [("rd", "21"), ("ip", "IP")], 604),
    '<div style="position:absolute;left:416px;top:740px;width:1098px;height:60px;border:2px dashed #b9c3cf;border-radius:10px"></div>',
    '<div class="i64-t" style="left:416px;top:746px;width:1098px;text-align:center;font-size:19px;line-height:1.3">'
    'Вершина стека — сверху. В этом примере внешняя метка снимается на LSR7.<br>'
    '<span style="color:#e8402c;font-weight:800">Внутренняя метка 17 на всём обходе неизменна.</span></div>',
    '</div>',
    # низ
    '<div class="step">',
    '<div class="i64-p" style="left:350px;top:826px;width:708px;height:94px;background:#fff1c4;border-color:#e3b23c;border-radius:14px"></div>',
    img("i64a_sh.png", "left:360px;top:834px;width:82px"),
    '<div class="i64-t" style="left:454px;top:846px;font-size:21px;line-height:1.25"><b style="font-weight:900;font-size:26px;color:#13306e">Быстрая защита:</b>'
    ' LSR2 переключает трафик<br>локально, не дожидаясь полного пересчёта маршрутов.</div>',
    '<div class="i64-p" style="left:1070px;top:826px;width:572px;height:94px;background:#e9f0f8;border-color:#7aa3d8;border-radius:14px"></div>',
    img("i64a_inf.png", "left:1086px;top:844px;width:56px"),
    '<div class="i64-t" style="left:1154px;top:840px;font-size:16px;line-height:1.3">Числа сохранены как условные обозначения исходного<br>'
    'рисунка. В реальном MPLS значения 0–15 зарезервированы;<br>для обычных меток используют значения от 16.</div>',
    '</div>',
])
