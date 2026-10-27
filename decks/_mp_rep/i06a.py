# -*- coding: utf-8 -*-
"""pptx 6: чем обычная IP-передача отличается от передачи по виртуальному каналу; вёрстка поверх bgk_30."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i06-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.22)}
.i06-t{position:absolute;font:500 26px/1.35 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i06-t b{font-weight:800;color:#13306e}
.i06-pl{position:absolute;border-radius:14px;text-align:center;font:500 19px/1.2 "Golos Text",sans-serif;color:#1d2a44;padding-top:6px;box-sizing:border-box}
.i06-pl b{display:block;font:800 23px/1.2 "Golos Text",sans-serif;color:#13306e}
.i06-r{position:absolute;font:900 25px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:80px}
.i06-bar{position:absolute;display:flex;height:22px;border:2px solid #1d3f8a;border-radius:3px;background:#fff;overflow:hidden}
.i06-bar i{flex:1;border-left:2px solid #1d3f8a}.i06-bar i:first-child{border-left:0}
.i06-ch{position:absolute;font:900 22px/1.1 "Rubik",sans-serif;color:#13306e}
.i06-cx{position:absolute;font:500 19px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i06-fly{animation:i06f 2.6s ease-in-out infinite}
@keyframes i06f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def bar(x, y, n, col, w):
    cells = '<i style="background:%s"></i>' % col + "<i></i>" * (n - 1)
    return '<div class="i06-bar i06-fly" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (x, y, w, cells)


def rt(x, y, w, name, lx, ly):
    return img("i06a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w)) + \
        '<div class="i06-r" style="left:%dpx;top:%dpx">%s</div>' % (lx - 40, ly, name)


SVG_O = """<svg class="ab" style="left:0;top:0;width:1672px;height:941px;pointer-events:none" viewBox="0 0 1672 941">
<defs><marker id="i06a-mo" markerWidth="4" markerHeight="4" refX="2.5" refY="2" orient="auto"><path d="M0,0L4,2L0,4z" style="fill:#f0662f"/></marker></defs>
<g style="fill:none;stroke:#f0662f;stroke-width:5;stroke-linecap:round">
<path d="M536,394 L612,384"/><path d="M708,380 L776,378" marker-end="url(#i06a-mo)"/>
<path d="M890,378 L966,380"/><path d="M1060,384 L1130,398" marker-end="url(#i06a-mo)"/></g>
<path d="M512,348 V306 H630 M1048,306 H1162 V348" style="fill:none;stroke:#f0663f;stroke-width:2.5"/></svg>"""

SVG_T = """<svg class="ab" style="left:0;top:0;width:1672px;height:941px;pointer-events:none" viewBox="0 0 1672 941">
<defs><marker id="i06a-mt" markerWidth="4" markerHeight="4" refX="2.5" refY="2" orient="auto"><path d="M0,0L4,2L0,4z" style="fill:#1f9c8a"/></marker></defs>
<g style="fill:none;stroke:#1f9c8a;stroke-width:5;stroke-linecap:round">
<path d="M518,446 Q536,476 560,484"/><path d="M632,488 Q645,494 652,500" marker-end="url(#i06a-mt)"/>
<path d="M762,502 L796,502"/><path d="M878,502 L906,502" marker-end="url(#i06a-mt)"/>
<path d="M1018,512 Q1032,506 1044,496"/><path d="M1112,482 L1150,452" marker-end="url(#i06a-mt)"/></g>
<path d="M512,490 V590 H630 M1048,590 H1162 V490" style="fill:none;stroke:#1f9c8a;stroke-width:2.5"/></svg>"""

HTML = CSS + bg("bgk_30") + "".join([
    '<div class="step">',
    '<div class="i06-p" style="left:280px;top:156px;width:1110px;height:90px"></div>',
    '<div class="i06-t" style="left:280px;top:166px;width:1116px"><b>Детерминированный маршрут</b> — заранее определённый путь через сеть,<br>'
    'которому следует трафик, направленный в соответствующий LSP.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i06-p" style="left:280px;top:262px;width:1110px;height:372px"></div>',
    SVG_O,
    '<div class="i06-pl" style="left:630px;top:274px;width:418px;height:60px;background:#fbd8c9"><b>Обычная IP-маршрутизация</b>'
    'Меньшая метрика • высокая загрузка</div>',
    rt(410, 358, 122, "R1", 470, 455), rt(786, 343, 100, "R2", 836, 420), rt(1142, 358, 122, "R4", 1202, 455),
    bar(616, 368, 4, "#f0662f", 88), bar(970, 368, 4, "#f0662f", 88),
    '</div>',
    '<div class="step">',
    SVG_T,
    rt(662, 473, 96, "R3", 710, 543), rt(916, 473, 96, "R5", 963, 543),
    bar(564, 472, 3, "#2fb39b", 66), bar(800, 490, 4, "#2fb39b", 76), bar(1044, 472, 3, "#2fb39b", 66),
    '<div class="i06-pl" style="left:630px;top:566px;width:418px;height:60px;background:#cdeee4"><b>LSP с MPLS TE</b>'
    'Большая метрика • свободная полоса</div>',
    '</div>',
    '<div class="step">',
    '<div class="i06-p" style="left:284px;top:648px;width:524px;height:134px"></div>',
    img("i06a_ic1.png", "left:302px;top:664px;width:104px"),
    '<div class="i06-ch" style="left:418px;top:665px">ОБЫЧНАЯ IP-МАРШРУТИЗАЦИЯ</div>',
    '<div class="i06-cx" style="left:418px;top:698px">Выбирает путь по метрике.<br>Высокая загрузка сама по себе<br>не обязательно меняет метрику.</div>',
    '<div class="i06-p" style="left:822px;top:648px;width:568px;height:134px"></div>',
    img("i06a_ic2.png", "left:842px;top:664px;width:104px"),
    '<div class="i06-ch" style="left:966px;top:677px">MPLS TRAFFIC ENGINEERING</div>',
    '<div class="i06-cx" style="left:964px;top:712px">Позволяет построить LSP по второму пути<br>и направить туда часть трафика.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i06-p" style="left:312px;top:795px;width:1048px;height:120px;background:#fdf3d6"></div>',
    img("i06a_ic3.png", "left:342px;top:800px;width:94px"),
    '<div class="i06-ch" style="left:455px;top:813px;font-size:27px">НЕ КАЖДЫЙ LSP — СПЕЦИАГЬНО ЗАДАННЫЙ ПУТЬ</div>',
    '<div class="i06-cx" style="left:455px;top:850px;font-size:21px">LSP, построенный с помощью LDP, обычно следует путям IP-маршрутизации.<br>'
    'Для выбора пути с дополнительными ограничениями применяют MPLS TE.</div>',
    '</div>',
])
