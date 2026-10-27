# -*- coding: utf-8 -*-
"""pptx: протокол LDP — передача запроса метки к выходному узлу — вёрстка поверх чистого фона bgk_03.
Пилюля «Режим Downstream on Demand» стоит рядом с заголовком оригинала, поэтому TOP небольшой."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 50

CSS = """<style>
.i28-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i28-h{position:absolute;font:900 31px/1 "Rubik",sans-serif;color:#13306e;text-transform:uppercase}
.i28-t{position:absolute;font:500 21px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i28-c{position:absolute;font:500 19px/1.2 "Golos Text",sans-serif;color:#1d2a44;text-align:center;width:240px}
.i28-n{position:absolute;font:800 25px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:240px}
.i28-lr{position:absolute;width:164px;height:38px;background:#f2694a;border-radius:8px;font:500 21px/38px "Golos Text",sans-serif;
 color:#fff;text-align:center}
.i28-ar{position:absolute;height:3px}
.i28-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid currentColor;border-right:0}
.i28-tb{position:absolute;border-collapse:collapse;font:500 22px/1 "Golos Text",sans-serif;color:#1d2a44;text-align:center;background:#fdf8ea}
.i28-tb td{height:44px;border:2.5px solid #1d3f8a}
.i28-go{animation:i28g 2.6s ease-in-out infinite}
@keyframes i28g{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
</style>"""


def ar(x, y, w, col):
    return '<div class="i28-ar" style="left:%dpx;top:%dpx;width:%dpx;background:%s;color:%s"></div>' % (x, y, w, col, col)


def node(x, name, lines):
    return img("i28a_rt.png", "left:%dpx;top:500px;width:122px" % x) + \
        '<div class="i28-n" style="left:%dpx;top:590px">%s</div>' % (x - 59, name) + \
        '<div class="i28-c" style="left:%dpx;top:620px;line-height:1.3">%s</div>' % (x - 59, lines)


def req(x, y):
    return '<div class="i28-go" style="position:absolute;left:%dpx;top:%dpx;width:164px;height:38px">' % (x, y) + \
        '<div class="i28-lr" style="left:0;top:0">Label Request</div></div>'


HTML = CSS + bg("bgk_03") + "".join([
    '<div class="step">',
    '<div style="position:absolute;left:874px;top:60px;width:484px;height:58px;background:#bfece2;border:3px solid #1f63c6;border-radius:30px;'
    'font:800 27px/58px Golos Text,sans-serif;color:#13306e;text-align:center">Режим Downstream on Demand</div>',
    '</div>',
    '<div class="step">',
    '<div class="i28-p" style="left:48px;top:180px;width:756px;height:212px"></div>',
    '<div class="i28-h" style="left:72px;top:196px">Формат Label Request</div>',
    '<table class="i28-tb" style="left:78px;top:240px;width:698px"><tr><td>Запрос метки (0x0401)</td><td>Длина сообщения</td></tr>'
    '<tr><td colspan="2">Идентификатор сообщения</td></tr><tr><td colspan="2">Элемент FEC: 132.100.0.0</td></tr></table>',
    '<div class="i28-p" style="left:818px;top:180px;width:806px;height:212px"></div>',
    '<div class="i28-h" style="left:842px;top:196px">Зачем нужен идентификатор</div>',
    '<div class="i28-t" style="left:842px;top:242px;width:760px;font-size:24px">Позволяет сопоставить ответ с конкретным запросом, '
    'когда несколько запросов ожидают ответа одновременно.</div>',
    '<div style="position:absolute;left:844px;top:326px;width:750px;height:2px;background:#13306e"></div>',
    '<div class="i28-t" style="left:842px;top:344px;font-size:20px">Идентификаторы относятся к обмену между соседними LSR.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i28-p" style="left:48px;top:406px;width:1478px;height:322px"></div>',
    '<div class="i28-h" style="left:72px;top:422px">Как запрос доходит до границы MPLS</div>',
    '<div style="position:absolute;left:66px;top:452px;width:1092px;height:268px;border-radius:130px;background:#c6ebe4"></div>',
    node(146, "LSR1", "FEC: 132.100.0.0<br>Инициирует запрос"),
    node(518, "LSR2", "FEC: 132.100.0.0<br>Нет готового LSP:<br>запрашивает метку<br>у следующего хопа"),
    node(890, "LSR3", "FEC: 132.100.0.0<br>Выходной узел:<br>здесь завершается LSP"),
    req(312, 500), ar(274, 546, 236, "#f2694a"),
    '<div class="i28-c" style="left:276px;top:558px">FEC: 132.100.0.0</div>',
    req(678, 500), ar(646, 546, 234, "#f2694a"),
    '<div class="i28-c" style="left:642px;top:558px">FEC: 132.100.0.0</div>',
    '<div style="position:absolute;left:1044px;top:430px;width:0;height:208px;border-left:2.5px dashed #13306e"></div>',
    '<div class="i28-t" style="left:1054px;top:424px;width:200px;text-align:center;font-size:19px;font-weight:600;line-height:1.3;color:#13306e">'
    'Граница MPLS-сети<br>оператора</div>',
    '<div class="i28-t" style="left:1080px;top:496px;width:200px;text-align:center;font-size:19px;font-weight:600;line-height:1.25;color:#13306e">'
    'Следующий хоп —<br>вне MPLS</div>',
    ar(1018, 546, 270, "#6b7280"),
    '<div style="position:absolute;left:1296px;top:500px;width:204px;height:110px;background:#dff1fd;border:2.5px solid #2a7fd4;border-radius:56px;'
    'font:600 23px/104px Golos Text,sans-serif;color:#13306e;text-align:center">132.100.0.0</div>',
    '</div>',
    '<div class="step">',
    '<div class="i28-p" style="left:48px;top:742px;width:528px;height:170px"></div>',
    '<div class="i28-h" style="left:72px;top:758px;font-size:28px">LSR2 проверяет маршрут</div>',
    '<div class="i28-t" style="left:72px;top:798px;width:490px">Для FEC 132.100.0.0 следующий хоп — LSR3.</div>',
    '<div class="i28-t" style="left:72px;top:834px;width:490px">Запрос передаётся соседу по установленному сеансу LDP.</div>',
    '<div class="i28-p" style="left:590px;top:742px;width:486px;height:170px"></div>',
    '<div class="i28-h" style="left:618px;top:758px;font-size:28px">LSR3 — конец пути</div>',
    '<div class="i28-t" style="left:618px;top:798px;width:450px;font-size:20px;line-height:1.3">Дальнейший маршрут ведёт за пределы MPLS-сети '
    'оператора.<br>Поэтому путь коммутации по меткам заканчивается на LSR3.</div>',
    '</div>',
])
