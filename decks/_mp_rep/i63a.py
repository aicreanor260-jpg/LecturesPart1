# -*- coding: utf-8 -*-
"""pptx: Отказоустойчивость путей MPLS — четыре механизма восстановления TE-туннеля, фон bgk_28."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 160

CSS = """<style>
.i63-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i63-h{position:absolute;font:900 32px/1 "Rubik",sans-serif;color:#13306e}
.i63-t{position:absolute;font:500 21px/1.27 "Golos Text",sans-serif;color:#1d2a44}
.i63-n{position:absolute;font:800 22px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:110px}
.i63-pl{position:absolute;background:#c9eedc;border-radius:10px;font:700 21px/38px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i63-bl{position:absolute;background:#cfe8fb;border:2px solid #7cc0f0;border-radius:12px;font:600 20px/34px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i63-x{position:absolute;font:900 40px/1 "Golos Text",sans-serif;color:#e8402c}
.i63-b{position:absolute;font:800 22px/1 "Golos Text",sans-serif;color:#13306e}
.i63-s{position:absolute;font:500 17px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i63-fly{animation:i63f 2.6s ease-in-out infinite}
@keyframes i63f{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
</style>"""


def mk(mid, col):
    return ('<marker id="%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
            '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>' % (mid, col))


def svg(body, marks):
    return ('<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941">'
            '<defs>' + "".join(mk(m, c) for m, c in marks) + '</defs>' + body + '</svg>')


def rt(x, y, w, name, red=False):
    return img("i63a_rtx.png" if red else "i63a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w)) + \
        ('<div class="i63-n" style="left:%dpx;top:%dpx">%s</div>' % (x + w // 2 - 55, y + int(w * 0.7) + 6, name) if name else "")


HTML = CSS + bg("bgk_28") + "".join([
    # 1
    '<div class="step">',
    '<div class="i63-p" style="left:148px;top:174px;width:690px;height:296px"></div>',
    '<div class="i63-h" style="left:176px;top:188px">1. Восстановление от входного узла</div>',
    rt(240, 243, 100, "LSR1"), rt(678, 243, 100, "LSR8"),
    '<svg style="position:absolute;left:408px;top:236px;width:204px;height:90px" viewBox="0 0 204 90">'
    '<path d="M30 78 Q4 76 8 54 Q2 30 30 30 Q36 6 70 12 Q90 -2 116 10 Q150 2 160 26 Q198 28 194 54 Q198 80 166 78 Z" '
    'style="fill:#bfe9e4;stroke:#3aa18f;stroke-width:3"/></svg>',
    '<div class="i63-n" style="left:440px;top:258px;width:140px;font-size:21px;line-height:1.2">Новый<br>маршрут</div>',
    svg('<line x1="344" y1="278" x2="400" y2="278" style="stroke:#1d3f8a;stroke-width:4" marker-end="url(#i63a1)"/>'
        '<line x1="614" y1="278" x2="670" y2="278" style="stroke:#1d3f8a;stroke-width:4" marker-end="url(#i63a1)"/>',
        [("i63a1", "#1d3f8a")]),
    '<div class="i63-t" style="left:182px;top:348px">После отказа LSR1 рассчитывает новый допустимый путь<br>и устанавливает LSP через RSVP-TE.</div>',
    '<div style="position:absolute;left:176px;top:414px;width:646px;height:44px;background:#fbd3cb;border-radius:12px"></div>',
    img("i63a_clk.png", "left:186px;top:416px;width:40px"),
    '<div class="i63-t" style="left:238px;top:425px;font-size:16.5px">Скорость зависит от обнаружения отказа, расчёта и сигнализации.</div>',
    '</div>',
    # 2
    '<div class="step">',
    '<div class="i63-p" style="left:852px;top:174px;width:686px;height:296px"></div>',
    '<div class="i63-h" style="left:880px;top:188px">2. Защита линии — FRR</div>',
    rt(904, 245, 90, "LSR2"), rt(1196, 245, 90, "LSR7"), rt(1048, 325, 92, "LSR3"),
    svg('<line x1="1000" y1="272" x2="1188" y2="272" style="stroke:#a9a9a9;stroke-width:4;stroke-dasharray:10 7" marker-end="url(#i63a2)"/>'
        '<path d="M984 304 Q1004 344 1040 352" style="fill:none;stroke:#27ae7e;stroke-width:5" marker-end="url(#i63a3)"/>'
        '<path d="M1146 352 Q1182 340 1200 306" style="fill:none;stroke:#27ae7e;stroke-width:5" marker-end="url(#i63a3)"/>',
        [("i63a2", "#a9a9a9"), ("i63a3", "#27ae7e")]),
    '<div class="i63-x" style="left:1080px;top:252px">✕</div>',
    '<div class="i63-pl" style="left:1034px;top:420px;width:138px">B1-LSP1</div>',
    '<div class="i63-t" style="left:1310px;top:266px;font-size:18.5px">Заранее<br>подготовленный обход<br>защищает линию<br>LSR2–LSR7.</div>',
    '</div>',
    # 3
    '<div class="step">',
    '<div class="i63-p" style="left:156px;top:486px;width:682px;height:258px"></div>',
    '<div class="i63-h" style="left:186px;top:500px">3. Защита узла — FRR</div>',
    rt(212, 557, 86, "LSR2"), rt(352, 555, 88, "LSR7", True), rt(492, 557, 84, "LSR8"), rt(360, 645, 72, ""),
    svg('<line x1="302" y1="586" x2="350" y2="586" style="stroke:#a9a9a9;stroke-width:4;stroke-dasharray:8 6"/>'
        '<line x1="444" y1="586" x2="490" y2="586" style="stroke:#a9a9a9;stroke-width:4;stroke-dasharray:8 6"/>'
        '<path d="M282 640 Q300 670 352 672" style="fill:none;stroke:#27ae7e;stroke-width:5" marker-end="url(#i63a4)"/>'
        '<path d="M438 668 Q490 664 508 622" style="fill:none;stroke:#27ae7e;stroke-width:5" marker-end="url(#i63a4)"/>',
        [("i63a4", "#27ae7e")]),
    '<div class="i63-pl" style="left:334px;top:694px;width:134px">B2-LSP1</div>',
    '<div class="i63-t" style="left:596px;top:566px;font-size:20px">Локальный обход<br>исключает отказавший<br>LSR7 и возвращает<br>трафик на путь ниже<br>по потоку.</div>',
    '</div>',
    # 4
    '<div class="step">',
    '<div class="i63-p" style="left:852px;top:486px;width:686px;height:258px"></div>',
    '<div class="i63-h" style="left:880px;top:500px">4. Защита всего пути</div>',
    rt(872, 600, 86, "LSR1"), rt(1198, 600, 82, "LSR8"),
    svg('<path d="M930 594 Q950 572 990 568" style="fill:none;stroke:#1f63c6;stroke-width:4" marker-end="url(#i63a5)"/>'
        '<path d="M1170 570 Q1210 580 1222 598" style="fill:none;stroke:#1f63c6;stroke-width:4"/>'
        '<line x1="944" y1="672" x2="970" y2="684" style="stroke:#27ae7e;stroke-width:5" marker-end="url(#i63a6)"/>'
        '<line x1="1188" y1="684" x2="1208" y2="670" style="stroke:#27ae7e;stroke-width:5" marker-end="url(#i63a6)"/>',
        [("i63a5", "#1f63c6"), ("i63a6", "#27ae7e")]),
    '<div class="i63-bl" style="left:996px;top:550px;width:166px">Основной LSP1</div>',
    '<div class="i63-pl" style="left:976px;top:664px;width:208px;font-size:20px">Резервный B3-LSP1</div>',
    '<div class="i63-t" style="left:1292px;top:584px;font-size:18px">Резервный LSP соединяет<br>те же конечные узлы<br>и по возможности<br>не разделяет с основным<br>линии и узлы.</div>',
    '</div>',
    # итог
    '<div class="step">',
    '<div class="i63-p" style="left:298px;top:762px;width:1258px;height:150px;border-radius:16px"></div>',
    '<div style="position:absolute;left:716px;top:782px;width:2px;height:112px;background:#7aa3d8"></div>',
    '<div style="position:absolute;left:1122px;top:782px;width:2px;height:112px;background:#7aa3d8"></div>',
    '<div class="i63-fly" style="position:absolute;left:0;top:0">',
    img("i63a_gear.png", "left:366px;top:778px;width:96px"), img("i63a_sw.png", "left:733px;top:778px;width:96px"),
    img("i63a_db.png", "left:1143px;top:778px;width:96px"), '</div>',
    '<div class="i63-b" style="left:480px;top:786px">Обнаружение:</div>',
    '<div class="i63-s" style="left:480px;top:816px">BFD, LSP Ping, RSVP Hello —<br>в зависимости от отказа<br>и настройки.</div>',
    '<div class="i63-b" style="left:848px;top:786px">FRR:</div>',
    '<div class="i63-s" style="left:848px;top:812px">локальное переключение<br>с целевым временем порядка<br>50 мс; затем возможна<br>переоптимизация.</div>',
    '<div class="i63-b" style="left:1256px;top:786px">Защита полосы</div>',
    '<div class="i63-s" style="left:1256px;top:816px">зависит от резервирования<br>ресурсов на обходном пути.</div>',
    '</div>',
])
