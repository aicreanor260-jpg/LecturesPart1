# -*- coding: utf-8 -*-
"""pptx: Иерархия меток для быстрой защиты (FRR, PHP на обходе) — фон bgk_04 (уточки и Камадзи)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 160

CSS = """<style>
.i65-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i65-t{position:absolute;font:500 21px/1.42 "Golos Text",sans-serif;color:#1d2a44}
.i65-n{position:absolute;font:800 27px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:160px}
.i65-l{position:absolute;font:700 21px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i65-st{position:absolute;width:62px;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;font:700 23px/34px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i65-st div{border-top:2px solid #1d3f8a}.i65-st div:first-child{border-top:0}
.i65-r{background:#f2694a}.i65-g{background:#a9e6b9}.i65-i{background:#fdf6e4}
.i65-lb{position:absolute;display:flex;height:42px;border:3px solid #1d3f8a;border-radius:5px;background:#fdf6e4;font:700 24px/36px "Golos Text",sans-serif;color:#13306e}
.i65-lb span{width:12px;border-right:3px solid #1d3f8a;background:#cfe4f5}.i65-lb i{font-style:normal;padding:0 26px}
.i65-c{position:absolute;font:900 34px/1 "Rubik",sans-serif;color:#13306e;width:62px;height:62px;border-radius:50%;background:#5fcfa6;text-align:center;line-height:62px}
.i65-ch{position:absolute;font:800 25px/1 "Golos Text",sans-serif;color:#13306e}
.i65-fly{animation:i65f 2.6s ease-in-out infinite}
@keyframes i65f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def rt(x, y, name, w=134):
    return img("i65a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w)) + \
        '<div class="i65-n" style="left:%dpx;top:%dpx">%s</div>' % (x + w // 2 - 80, y + 100, name)


def stk(x, y, cells):
    return '<div class="i65-st" style="left:%dpx;top:%dpx">%s</div>' % (
        x, y, "".join('<div class="i65-%s">%s</div>' % (c, t) for c, t in cells))


def lb(x, y, v):
    return '<div class="i65-fly" style="position:absolute;left:0;top:0"><div class="i65-lb" style="left:%dpx;top:%dpx">' \
           '<span></span><i>%s</i></div></div>' % (x, y, v)


def card(x, num, head, text):
    return ('<div class="i65-p" style="left:%dpx;top:594px;width:438px;height:178px;border-radius:16px"></div>' % x +
            '<div class="i65-c" style="left:%dpx;top:604px">%s</div>' % (x + 22, num) +
            '<div class="i65-ch" style="left:%dpx;top:620px">%s</div>' % (x + 100, head) +
            '<div class="i65-t" style="left:%dpx;top:664px;font-size:19.5px">%s</div>' % (x + 100, text))


M = ('<marker id="i65m%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
     '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>')

HTML = CSS + bg("bgk_04") + "".join([
    '<div class="step">',
    '<div class="i65-p" style="left:92px;top:180px;width:1488px;height:390px"></div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' +
    M % ("a", "#1d6b78") + M % ("b", "#27c08a") + M % ("c", "#8a8a8a") + '</defs>'
    '<line x1="310" y1="468" x2="376" y2="468" style="stroke:#1d6b78;stroke-width:4"/>'
    '<line x1="478" y1="468" x2="532" y2="468" style="stroke:#1d6b78;stroke-width:4" marker-end="url(#i65ma)"/>'
    '<line x1="1148" y1="468" x2="1214" y2="468" style="stroke:#1d6b78;stroke-width:4"/>'
    '<line x1="1316" y1="468" x2="1370" y2="468" style="stroke:#1d6b78;stroke-width:4" marker-end="url(#i65ma)"/>'
    '<line x1="672" y1="468" x2="1004" y2="468" style="stroke:#8a8a8a;stroke-width:4;stroke-dasharray:14 8" marker-end="url(#i65mc)"/>'
    '<line x1="606" y1="418" x2="650" y2="380" style="stroke:#27c08a;stroke-width:6" marker-end="url(#i65mb)"/>'
    '<line x1="724" y1="346" x2="780" y2="296" style="stroke:#27c08a;stroke-width:6" marker-end="url(#i65mb)"/>'
    '<line x1="906" y1="296" x2="968" y2="350" style="stroke:#27c08a;stroke-width:6"/>'
    '<line x1="1022" y1="392" x2="1058" y2="420" style="stroke:#27c08a;stroke-width:6" marker-end="url(#i65mb)"/>'
    '<path d="M660 230 V246 H1026 V230" style="fill:none;stroke:#1d3f8a;stroke-width:3"/>'
    '<path d="M612 316 Q620 336 640 334" style="fill:none;stroke:#1d3f8a;stroke-width:2" marker-end="url(#i65ma)"/>'
    '<path d="M1074 314 Q1062 330 1046 332" style="fill:none;stroke:#1d3f8a;stroke-width:2" marker-end="url(#i65ma)"/>'
    '</svg>',
    rt(172, 424, "LSR1"), rt(538, 424, "LSR2"), rt(1014, 424, "LSR7"), rt(1372, 424, "LSR8"),
    rt(788, 248, "LSR3", 114),
    '<div class="i65-l" style="left:770px;top:194px;width:150px;font-size:25px;font-weight:800">B-LSP1</div>',
    lb(378, 446, "15"), lb(1216, 448, "21"),
    stk(656, 286, [("r", "7"), ("g", "17"), ("i", "IP")]),
    stk(972, 312, [("g", "17"), ("i", "IP")]),
    '<div class="i65-l" style="left:492px;top:260px;width:140px">Вершина<br>стека: 7</div>',
    '<div class="i65-l" style="left:1046px;top:276px;width:160px">После PHP: 17</div>',
    '<div class="i65-l" style="left:802px;top:440px;color:#e8402c;font-size:52px">✕</div>',
    '<div class="i65-l" style="left:730px;top:504px;width:240px;color:#e8402c;font-weight:800">Линия недоступна</div>',
    '</div>',
    '<div class="step">', card(184, "1", "LSR2: Swap + Push",
                               "Заменяет 15 на 17, затем<br>добавляет внешнюю метку 7.<br><b style='font-weight:800'>Стек: [7, 17].</b>"), '</div>',
    '<div class="step">', card(636, "2", "LSR3: Pop (PHP)",
                               "Предпоследний узел обходного<br>пути снимает метку 7.<br>На вершине остаётся 17."), '</div>',
    '<div class="step">', card(1060, "3", "LSR7: продолжение LSP1",
                               "Получает ожидаемую метку 17,<br>заменяет её на 21 и передаёт<br>пакет к LSR8."), '</div>',
    '<div class="step">',
    '<div class="i65-p" style="left:276px;top:794px;width:1132px;height:92px;border-radius:16px;border-width:0"></div>',
    img("i65a_inf.png", "left:300px;top:812px;width:52px"),
    '<div class="i65-t" style="left:372px;top:818px;font-size:16px;line-height:1.4">Без PHP внешняя метка могла бы смениться с 7 на 8 и снималась бы на выходе обхода.<br>'
    'В показанном варианте применяется PHP.</div>',
    '<div style="position:absolute;left:1102px;top:812px;width:3px;height:56px;background:#1d3f8a"></div>',
    '<div class="i65-st" style="left:1124px;top:812px;width:40px;line-height:15px;font-size:10px">'
    '<div class="i65-r">&nbsp;</div><div class="i65-g">&nbsp;</div><div class="i65-i">&nbsp;</div></div>',
    '<div class="i65-t" style="left:1184px;top:818px;font-size:16px;line-height:1.4">Стек записан<br>от вершины к основанию.</div>',
    '</div>',
])
