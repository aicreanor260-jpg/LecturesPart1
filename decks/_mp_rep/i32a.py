# -*- coding: utf-8 -*-
"""pptx: IntServ и RSVP — ресурсы для микропотока вдоль пути. Фон bgk_20 (Пугало слева, герои справа)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 212

CSS = """<style>
.i32-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i32-c{position:absolute;background:#fdf8ea;border-radius:18px;box-shadow:0 4px 0 rgba(21,80,168,.2)}
.i32-n{position:absolute;font:800 22px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i32-t{position:absolute;font:500 20px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i32-t b{display:block;font:800 26px/1.3 "Golos Text";white-space:nowrap,sans-serif;color:#13306e;margin-bottom:4px}
.i32-lab{position:absolute;font:700 21px/30px "Golos Text",sans-serif;padding:0 12px;background:#fdf8ea}
.i32-bub{position:absolute;background:#d6ebfb;border-radius:16px;font:500 20px/1.3 "Golos Text",sans-serif;color:#13306e;text-align:center;padding:12px 16px}
.i32-bub::after{content:"";position:absolute;left:90px;bottom:-16px;border:9px solid transparent;border-top:12px solid #d6ebfb;border-bottom:0}
.i32-fly{animation:i32f 3s ease-in-out infinite}
@keyframes i32f{0%,100%{transform:translateX(0)}50%{transform:translateX(12px)}}
</style>"""

SVG = ('<svg class="ab" style="left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941">'
       '<line x1="352" y1="444" x2="1350" y2="444" stroke="#1d3f8a" stroke-width="2"/></svg>')


def arrow(y, color, rev=False):
    a, b = (1296, 416) if rev else (414, 1296)
    m = "M%d,%dl%d,-12v24z" % (b, y, -20 if not rev else 20)
    return ('<svg class="ab" style="left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941">'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="6"/>'
            '<path d="M%d,%dl%d,-12v24z" fill="%s"/></svg>') % (a, y, b - (20 if not rev else -20), y, color,
                                                                 b, y, -24 if not rev else 24, color)


def rt(x, name):
    return '<div class="i32-n" style="left:%dpx;top:384px;width:112px">%s</div>' % (x, name) + \
        img("i32a_rt.png", "left:%dpx;top:408px;width:112px" % x) + \
        img("i32a_buf.png", "left:%dpx;top:490px;width:140px" % (x - 8)) + \
        '<div class="i32-n" style="left:%dpx;top:542px;width:220px">Полоса + буфер</div>' % (x - 54)


def card(x, ico, head, txt, w=456):
    return '<div class="i32-c" style="left:%dpx;top:610px;width:%dpx;height:176px"></div>' % (x, w) + \
        img(ico, "left:%dpx;top:628px;width:102px" % (x + 18)) + \
        '<div class="i32-t" style="left:%dpx;top:628px;width:%dpx"><b>%s</b>%s</div>' % (x + 136, w - 150, head, txt)


HTML = CSS + bg("bgk_20") + "".join([
    '<div class="step">',
    '<div class="i32-p" style="left:136px;top:222px;width:1398px;height:372px"></div>',
    SVG,
    img("i32a_pc1.png", "left:188px;top:352px;width:170px"), img("i32a_pc2.png", "left:1338px;top:352px;width:170px"),
    '<div class="i32-n" style="left:168px;top:500px;width:220px">Приложение-<br>отправитель</div>',
    '<div class="i32-n" style="left:1312px;top:500px;width:220px">Приложение-<br>получатель</div>',
    rt(512, "R1"), rt(794, "R2"), rt(1070, "R3"),
    '<div class="i32-bub" style="left:156px;top:250px;width:186px;white-space:nowrap">API: запрос QoS<br>от приложения</div>',
    '</div>',
    '<div class="step">', arrow(272, "#f2694a"),
    '<div class="i32-lab" style="left:688px;top:252px;color:#f2694a">Path → сведения о потоке</div>', '</div>',
    '<div class="step">', arrow(310, "#13457e", True),
    '<div class="i32-lab" style="left:668px;top:294px;color:#13306e">Resv ← запрос резервирования</div>', '</div>',
    '<div class="step">', '<div class="i32-fly">', arrow(354, "#3cb48a"), '</div>',
    '<div class="i32-lab" style="left:588px;top:338px;color:#2f9a6e">Данные → после успешного резервирования</div>', '</div>',
    '<div class="step">',
    card(112, "i32a_ic1.png", "Что резервируется", "Пропускная способность<br>интерфейсов и ресурсы<br>буферов."),
    card(584, "i32a_ic2.png", "Кто согласует", "RSVP передаёт сигнальные сообщения. Каждый маршрутизатор проверяет "
         "ресурсы и политику QoS."),
    card(1054, "i32a_ic3.png", "Где обеспечивается QoS", "На всех маршрутизаторах вдоль пути конкретного потока.", 422),
    '</div>',
    '<div class="step">',
    '<div class="i32-c" style="left:112px;top:800px;width:1216px;height:100px"></div>',
    img("i32a_ex.png", "left:128px;top:808px;width:82px"),
    '<div class="i32-t" style="left:224px;top:816px;width:1100px;font-size:20px;white-space:nowrap"><span style="font:800 23px Golos Text,sans-serif;color:#13306e">'
    'Резервирование однонаправленное:</span> для обмена в обе стороны нужны два отдельных резервирования.<br>'
    '<span style="font-size:18px;color:#3b4660">Резервирование возможно, если хватает ресурсов и разрешает политика сети.</span></div>',
    '</div>',
])
