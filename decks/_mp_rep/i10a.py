# -*- coding: utf-8 -*-
"""pptx 10: архитектура комбинированного устройства LSR; вёрстка поверх чистого фона bgk_22."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 170

CSS = """<style>
.i10-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.22)}
.i10-h{position:absolute;font:900 32px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i10-a{position:absolute;border-radius:30px}
.i10-sec{position:absolute;height:14px;border-top:2px solid #13306e;border-left:2px solid #13306e;border-right:2px solid #13306e}
.i10-sl{position:absolute;font:900 22px/26px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i10-b{position:absolute;background:#fff;border:2px solid #13306e;border-radius:6px;box-sizing:border-box;display:flex;align-items:center;
 justify-content:center;text-align:center;font:700 18.5px/1.2 "Golos Text",sans-serif;color:#13306e}
.i10-x{position:absolute;font:500 18.5px/1.38 "Golos Text",sans-serif;color:#1d2a44;white-space:nowrap}
.i10-x b{font-weight:800;color:#13306e}
.i10-n{position:absolute;width:52px;height:52px;border-radius:50%;background:#13508f;color:#fff;font:900 32px/52px "Rubik",sans-serif;text-align:center}
.i10-tb{position:absolute;border-collapse:collapse;font:500 19px/38px "Golos Text",sans-serif;color:#1d2a44;text-align:center;background:#fff}
.i10-tb td,.i10-tb th{border:2px solid #9fb8c8;padding:0}.i10-tb th{background:#d9efe8;font-weight:700;color:#13306e}
.i10-pk{position:absolute;display:flex;height:46px;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;font:700 23px/40px "Golos Text",sans-serif}
.i10-pk b{background:#f2694a;color:#1d1d1d;padding:0 12px;font-weight:700}.i10-pk i{background:#fff;color:#1d3f8a;padding:0 20px;font-style:normal}
.i10-fly{animation:i10f 3s ease-in-out infinite}
@keyframes i10f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def b(x, y, w, h, t, fs=""):
    return '<div class="i10-b" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx%s">%s</div>' % (x, y, w, h, fs, t)


def card(y, h, w, n, title, ic, ty, txt):
    return ('<div class="step"><div class="i10-p" style="left:1008px;top:%dpx;width:%dpx;height:%dpx"></div>' % (y, w, h) +
            '<div class="i10-n" style="left:1022px;top:%dpx">%s</div>' % (y + 12, n) +
            '<div class="i10-h" style="left:1090px;top:%dpx;font-size:30px">%s</div>' % (y + 14, title) +
            img(ic, "left:1064px;top:%dpx;width:80px" % ty) +
            '<div class="i10-x" style="left:1172px;top:%dpx">%s</div></div>' % (ty + 4, txt))


A = "#13306e"
L = "#2b8de0"
SVG = """<svg class="ab" style="left:0;top:0;width:1672px;height:941px;pointer-events:none" viewBox="0 0 1672 941">
<defs><marker id="i10a-md" markerWidth="4" markerHeight="4" refX="2.5" refY="2" orient="auto-start-reverse"><path d="M0,0L4,2L0,4z" style="fill:%s"/></marker>
<marker id="i10a-ml" markerWidth="4" markerHeight="4" refX="2.5" refY="2" orient="auto"><path d="M0,0L4,2L0,4z" style="fill:%s"/></marker></defs>
<g style="fill:none;stroke:%s;stroke-width:4">
<path d="M390,326 V352" marker-end="url(#i10a-md)"/><path d="M584,334 V384 H532" marker-end="url(#i10a-md)"/>
<path d="M710,334 V360" marker-end="url(#i10a-md)"/><path d="M427,420 V470" marker-end="url(#i10a-md)"/>
<path d="M427,505 V524" marker-end="url(#i10a-md)"/><path d="M683,432 V524" marker-end="url(#i10a-md)"/>
<path d="M816,305 H962" marker-end="url(#i10a-md)" marker-start="url(#i10a-md)"/>
<path d="M72,403 H122" marker-end="url(#i10a-md)"/></g>
<g style="fill:none;stroke:%s;stroke-width:4">
<path d="M150,591 H204" marker-end="url(#i10a-ml)"/><path d="M388,570 L426,550" marker-end="url(#i10a-ml)"/>
<path d="M388,606 L426,626" marker-end="url(#i10a-ml)"/><path d="M646,548 L692,570" marker-end="url(#i10a-ml)"/>
<path d="M646,626 L692,606" marker-end="url(#i10a-ml)"/><path d="M856,596 H954" marker-end="url(#i10a-ml)"/>
<path d="M72,442 H122" marker-end="url(#i10a-ml)"/><path d="M468,866 H636" marker-end="url(#i10a-ml)"/></g></svg>""" % (A, L, A, L)

HTML = CSS + bg("bgk_22") + "".join([
    '<div class="step">',
    '<div class="i10-p" style="left:44px;top:180px;width:954px;height:504px"></div>',
    '<div class="i10-h" style="left:66px;top:192px">УСТРОЙСТВО LSR</div>',
    '<div class="i10-a" style="left:80px;top:228px;width:900px;height:234px;background:#d6efe2"></div>',
    '<div class="i10-sec" style="left:200px;top:245px;width:655px;border-left:0;border-right:0"></div>',
    '<div class="i10-sl" style="left:440px;top:232px;width:200px;background:#d6efe2">УПРАВЛЕНИЕ</div>',
    '<div class="i10-a" style="left:62px;top:472px;width:918px;height:200px;background:#d3ebf7"></div>',
    '<div class="i10-sec" style="left:200px;top:494px;width:664px"></div>',
    '<div class="i10-sl" style="left:365px;top:481px;width:320px;white-space:nowrap;background:#d3ebf7">ПРОДВИЖЕНИЕ ДАННЫХ</div>',
    '<div class="ab" style="left:57px;top:378px;width:213px;height:86px;background:#f3f8f4;border:2px solid #b9c9c0;border-radius:8px"></div>',
    SVG,
    b(228, 265, 272, 60, "Протоколы маршрутизации<br>OSPF, IS-IS"),
    b(560, 273, 236, 60, "Сигнальный протокол<br>LDP / RSVP-TE"),
    '<div class="i10-x" style="left:826px;top:270px;font-size:17px;font-weight:600;color:#13306e">Обмен метками</div>',
    b(298, 358, 224, 60, "Таблица<br>маршрутизации", ";font-size:19.5px"),
    b(620, 368, 245, 62, "Таблица продвижения<br>по меткам (LFIB)", ";font-size:19.5px"),
    '<div class="i10-x" style="left:144px;top:388px;font-size:15px;line-height:1.15;color:#13306e">Управляющая<br>информация</div>',
    '<div class="i10-x" style="left:144px;top:432px;font-size:15px;color:#13306e">Пакеты данных</div>',
    '</div>',
    '<div class="step">',
    '<div class="i10-x" style="left:80px;top:552px;font-size:17px;line-height:1.3">Входящий<br>трафик</div>',
    b(215, 545, 170, 87, ""), img("i10a_rt.png", "left:222px;top:563px;width:56px"),
    '<div class="i10-x" style="left:287px;top:566px;font-weight:700;color:#13306e;line-height:1.25">Входной<br>интерфейс</div>',
    b(432, 527, 211, 44, "IP-продвижение"), b(432, 598, 211, 58, "Продвижение<br>по меткам"),
    b(700, 545, 153, 87, ""), img("i10a_rt.png", "left:708px;top:563px;width:52px"),
    '<div class="i10-x" style="left:763px;top:568px;font-size:17px;font-weight:700;color:#13306e;line-height:1.25">Выходной<br>интерфейс</div>',
    '<div class="i10-x" style="left:878px;top:542px;font-size:17px;line-height:1.3;text-align:center">Исходящий<br>трафик</div>',
    '</div>',
    card(182, 145, 617, "1", "МАРШРУТЫ", "i10a_n1.png", 234,
         "OSPF или IS-IS получают сведения о сети.<br>Выбранные маршруты заносятся в таблицу<br>и служат основой для IP и MPLS."),
    card(342, 163, 617, "2", "СИГНАЛИЗАЦИЯ", "i10a_n2.png", 396,
         "Соседи обмениваются метками<br>и связывают их с направлениями передачи.<br><b>LSP — Label Switched Path:</b><br>"
         "однонаправленный путь коммутации по меткам."),
    card(518, 150, 507, "3", "ПРОДВИЖЕНИЕ ПО МЕТКАМ", "i10a_n3.png", 578,
         "<b>LFIB</b> определяет, как обработать пакет<br>с заданной входной меткой."),
    '<div class="step">',
    '<div class="i10-p" style="left:44px;top:700px;width:1016px;height:200px"></div>',
    '<div class="i10-h" style="left:66px;top:713px">ПРИМЕР ЗАПИСИ LFIB</div>',
    '<table class="i10-tb" style="left:68px;top:752px;width:968px"><tr><th style="width:227px">Входной интерфейс</th>'
    '<th style="width:210px">Входная метка</th><th style="width:245px">Выходной интерфейс</th><th>Действие</th></tr>'
    '<tr><td>Gi0/0</td><td>100</td><td>Gi0/1</td><td>Заменить 100 на 200</td></tr></table>',
    '<div class="i10-pk" style="left:318px;top:842px"><b>100</b><i>IP</i></div>',
    '<div class="i10-pk i10-fly" style="left:660px;top:842px"><b>200</b><i>IP</i></div>',
    '</div>',
])
