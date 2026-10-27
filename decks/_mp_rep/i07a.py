# -*- coding: utf-8 -*-
"""pptx 7: инжиниринг трафика — что может оператор; вёрстка поверх чистого фона bgk_06."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 170

CSS = """<style>
.i07-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.22)}
.i07-t{position:absolute;font:500 36px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i07-t b{font-weight:900;color:#13306e}
.i07-op{position:absolute;font:900 40px/1 "Rubik",sans-serif;color:#fff}
.i07-num{position:absolute;width:78px;height:78px;border-radius:50%;font:900 48px/78px "Rubik",sans-serif;color:#fff;text-align:center}
.i07-c{position:absolute;font:500 28px/1.2 "Golos Text",sans-serif;color:#1d2a44}
.i07-s{position:absolute;font:500 25px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i07-s b{font-weight:800;color:#13306e}
.i07-bob{animation:i07b 3s ease-in-out infinite}
@keyframes i07b{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
</style>"""


def card(x, w, n, col, ic, icx, icw, txt, tx):
    return ('<div class="step">'
            '<div class="i07-p" style="left:%dpx;top:373px;width:%dpx;height:303px"></div>' % (x, w) +
            '<div class="i07-num" style="left:%dpx;top:390px;background:%s">%s</div>' % (x + 26, col, n) +
            '<div class="ab i07-bob" style="left:%dpx;top:385px;width:%dpx">%s</div>' % (icx, icw, img(ic, "position:static;width:%dpx" % icw)) +
            '<div class="i07-c" style="left:%dpx;top:560px">%s</div>' % (tx, txt) + '</div>')


HTML = CSS + bg("bgk_06") + "".join([
    '<div class="step">',
    '<div class="i07-p" style="left:68px;top:180px;width:1538px;height:130px"></div>',
    '<div class="i07-t" style="left:98px;top:196px"><b>Инжиниринг трафика</b> — это управление распределением потоков<br>'
    'по сети с учётом её ресурсов и требований к передаче.</div>',
    '<div class="i07-op" style="left:92px;top:323px">Оператор может:</div>',
    '</div>',
    card(72, 450, "1", "#f0663f", "i07a_c1.png", 200, 295, "Перенести часть потоков<br>с перегруженных линий<br>на менее загруженные", 130),
    card(536, 418, "2", "#1fb3a8", "i07a_c2.png", 625, 300, "Проложить путь с учётом<br>требуемой пропускной<br>способности", 583),
    card(968, 416, "3", "#f6a630", "i07a_c3.png", 1075, 297, "Организовать резервный<br>путь на случай отказа", 1016),
    '<div class="step">',
    '<div class="i07-p" style="left:140px;top:688px;width:1212px;height:222px"></div>',
    '<div class="i07-s" style="left:232px;top:704px;font-size:27px"><b>Детерминированный маршрут</b> даёт возможность направить выбранный поток<br>'
    '<b>по нужной последовательности узлов.</b></div>',
    '<div class="i07-s" style="left:266px;top:790px;font-size:25px">Однако сама фиксация пути ещё не гарантирует полосу, малую задержку<br>'
    'или отсутствие потерь: для этого необходимы соответствующие механизмы<br><b>резервирования ресурсов и QoS.</b></div>',
    '</div>',
])
