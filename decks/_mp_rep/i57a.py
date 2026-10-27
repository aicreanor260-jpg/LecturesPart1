# -*- coding: utf-8 -*-
"""pptx: туннель 1 — строгий маршрут и проверка ресурсов — вёрстка поверх bgk_11."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 210

CSS = """<style>
.i57-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i57-h{position:absolute;font:900 36px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i57-t{position:absolute;font:500 22px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i57-n{position:absolute;font:800 26px/1 "Golos Text",sans-serif;color:#13306e;width:130px;text-align:center}
.i57-bw{position:absolute;background:#17734a;color:#fff;border-radius:22px;font:600 21px/40px "Golos Text",sans-serif;padding:0 14px 0 6px;white-space:nowrap}
.i57-bw i{display:inline-block;width:30px;height:30px;border-radius:50%;background:#fff;color:#17734a;font:900 20px/30px "Golos Text";
 text-align:center;font-style:normal;margin-right:8px;vertical-align:-1px}
.i57-ar{position:absolute;height:4px;background:#ef6a48;color:#ef6a48}
.i57-ar::after{content:"";position:absolute;right:-4px;top:-8px;border:10px solid transparent;border-left:16px solid currentColor;border-right:0}
.i57-br{position:absolute;height:20px;border:2px solid #1d3f8a;border-bottom:0}
.i57-br.d{border-top:0;border-bottom:0;height:0;border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a}
.i57-num{position:absolute;width:62px;height:62px;border-radius:50%;background:#ec6a52;color:#fff;font:900 30px/62px "Rubik";text-align:center}
.i57-run{animation:i57r 2.2s ease-in-out infinite}
@keyframes i57r{0%,100%{transform:translateX(-6px)}50%{transform:translateX(6px)}}
</style>"""


def rt(x):
    return img("i57a_rt.png", "left:%dpx;top:372px;width:132px" % x)


NODES = [(418, "LER1"), (696, "LSR1"), (944, "LSR2"), (1192, "LSR3"), (1462, "LER3")]
BW = [556, 802, 1048, 1298]
CARDS = [
    (40, "1.", "Выбор пути", "i57a_map.png", (58, 676, 154), 232, 680,
     "Заданы входной, выходной<br>и все промежуточные узлы.<br>Каждый переход строгий —<br>к указанному соседу."),
    (582, "2.", "Сигнализация RSVP-TE", "i57a_doc.png", (612, 682, 106), 746, 684,
     "При установлении LSP<br>устройства вдоль пути<br>проверяют доступную<br>для резервирования полосу."),
    (1110, "3.", "Условие успеха", "i57a_ok.png", (1162, 682, 110), 1294, 668,
     "Туннель устанавливается,<br>если все участки допускают<br>резервирование 10 Мбит/с.<br>При отказе на участке<br>установление не завершается."),
]

HTML = CSS + bg("bgk_11") + "".join([
    '<div class="i57-p" style="left:34px;top:222px;width:1604px;height:366px"></div>',
    '<div class="step">',
    '<div class="i57-h" style="left:70px;top:240px">Все переходы заданы заранее</div>',
    img("i57a_admin.png", "left:52px;top:302px;width:256px"),
    '<div class="i57-t" style="left:68px;top:454px;font-size:25px;line-height:1.2">Администратор или<br>внешняя система<br>задаёт маршрут<br>и полосу</div>',
    '<div class="i57-ar" style="left:306px;top:402px;width:72px;background:#13306e;color:#13306e"></div>',
    '<div style="position:absolute;left:392px;top:290px;width:1224px;height:284px;background:#c9eee3;border-radius:34px"></div>',
    '</div>',
    '<div class="step">',
    '<div class="i57-br" style="left:486px;top:320px;width:1042px"></div>',
    '<div class="i57-t" style="left:796px;top:298px;padding:0 14px;background:#c9eee3;font:800 30px/40px Golos Text;color:#13306e">'
    'Туннель 1 — 10 Мбит/с</div>',
    "".join(rt(x) + '<div class="i57-n" style="left:%dpx;top:478px">%s</div>' % (x, n) for x, n in NODES),
    "".join('<div class="i57-ar" style="left:%dpx;top:424px;width:%dpx"></div>' % (x, w) for x, w in [(556, 128), (828, 104), (1076, 106), (1322, 126)]),
    '</div>',
    '<div class="step">',
    "".join('<div class="i57-bw" style="left:%dpx;top:352px"><i>✓</i>≥ 10 Мбит/с</div>' % x for x in BW),
    '<div style="position:absolute;left:486px;top:532px;width:1042px;height:22px;border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a"></div>',
    '<div style="position:absolute;left:486px;top:543px;width:1042px;border-top:2px solid #1d3f8a"></div>',
    '<div class="i57-t" style="left:740px;top:528px;padding:0 16px;background:#c9eee3;font:800 25px/30px Golos Text;color:#13306e">'
    'LER1 → LSR1 → LSR2 → LSR3 → LER3</div>',
    '</div>',
    "".join('<div class="step">'
            + '<div class="i57-p" style="left:%dpx;top:602px;width:%dpx;height:218px"></div>' % (x, 526)
            + '<div class="i57-num" style="left:%dpx;top:608px">%s</div>' % (x + 26, k)
            + '<div class="i57-h" style="left:%dpx;top:624px;font-size:30px">%s</div>' % (x + 112, t)
            + img(ic, "left:%dpx;top:%dpx;width:%dpx" % icx)
            + '<div class="i57-t" style="left:%dpx;top:%dpx">%s</div>' % (tx, ty, body)
            + '</div>' for x, k, t, ic, icx, tx, ty, body in CARDS),
    '<div class="step">',
    '<div class="i57-p" style="left:124px;top:834px;width:1424px;height:80px;background:#fbf2c8;border-color:#e8d27a"></div>',
    img("i57a_bulb.png", "left:148px;top:838px;width:64px", "ab i57-run"),
    '<div class="i57-t" style="left:228px;top:846px;font:800 24px/1.25 Golos Text;color:#13306e">'
    'Доступная полоса TE — ресурс для резервирования, а не мгновенно свободная скорость интерфейса.<br>'
    '<span style="font-weight:500;font-size:21px;color:#1d2a44">Выбор маршрута внешней системой не отменяет проверку ресурсов в сети.</span></div>',
    '</div>',
])
