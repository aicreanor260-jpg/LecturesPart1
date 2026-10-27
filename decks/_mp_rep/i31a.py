# -*- coding: utf-8 -*-
"""pptx: LDP — два независимых параметра, четыре сочетания. Фон bgk_28 (Тоторо с зонтом справа)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 155

CSS = """<style>
.i31-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i31-h{position:absolute;font:900 32px/1 "Rubik",sans-serif;color:#13306e}
.i31-c{position:absolute;white-space:nowrap;border-radius:14px;padding:8px 14px;font:500 17.5px/1.2 "Golos Text",sans-serif;color:#1d2a44}
.i31-c b{display:block;font:800 22px/1.3 "Golos Text",sans-serif;color:#13306e}
.i31-t{position:absolute;font:500 18px/1.22 "Golos Text",sans-serif;color:#1d2a44}
.i31-t b{display:block;font:800 26px/1.3 "Golos Text",sans-serif;color:#13306e}
.i31-tb{position:absolute;border-collapse:collapse;font:500 22px/1 "Golos Text",sans-serif;color:#1d2a44;background:#fdf8ea;
 border:2px solid #1f63c6;border-radius:10px}
.i31-tb th{background:#d6ebfb;font-weight:700;color:#13306e;height:42px;border:1px solid #1f63c6}
.i31-tb td{text-align:center;height:44px;border:1px solid #1f63c6}
.i31-tb td:first-child{font-weight:700;color:#13306e}
.i31-often{display:inline-block;margin-left:18px;background:#1f8a6a;color:#fff;font:600 15px/26px "Golos Text",sans-serif;padding:0 12px;border-radius:8px}
.i31-y{position:absolute;background:#fbd35b;border:3px solid #1f63c6;border-radius:16px;font:500 19px/1.2 "Golos Text",sans-serif;color:#13306e}
.i31-y b{display:block;font:900 25px/1.2 "Rubik",sans-serif}
</style>"""


def card(x, y, w, h, ico, head, txt, color="#d9efee"):
    return img(ico, "left:%dpx;top:%dpx;width:88px" % (x, y + 2)) + \
        '<div class="i31-c" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s"><b>%s</b>%s</div>' % (
            x + 98, y - 2, w, h, color, head, txt)


HTML = CSS + bg("bgk_28") + "".join([
    '<div class="step">',
    '<div class="i31-p" style="left:208px;top:166px;width:640px;height:326px"></div>',
    '<div class="i31-h" style="left:234px;top:180px">1. Управление распределением</div>',
    card(238, 226, 462, 82, "i31a_play.png", "Независимое (Independent)",
         "LSR может объявить свою метку, не дожидаясь<br>метки от downstream-соседа."),
    card(238, 328, 462, 82, "i31a_chain.png", "Упорядоченное (Ordered)",
         "LSR объявляет метку, когда сам является Egress<br>для FEC или уже получил привязку от следующего хопа."),
    '<div class="i31-c" style="left:238px;top:424px;width:562px;height:52px;background:#fad3cc"><span style="font-weight:800;color:#13306e">Пример:</span> '
    'LSR2 может сообщить LSR1 метку 199 раньше,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;чем получит от LSR3 метку 231.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i31-p" style="left:860px;top:166px;width:646px;height:326px"></div>',
    '<div class="i31-h" style="left:884px;top:180px">2. Метод объявления меток</div>',
    card(890, 226, 470, 82, "i31a_doc.png", "По запросу (Downstream on Demand, DoD)",
         "Привязка FEC → метка передаётся в ответ<br>на Label Request."),
    card(890, 328, 470, 82, "i31a_radio.png", "Без запроса (Downstream Unsolicited, DU)",
         "LSR объявляет привязки подходящим LDP-соседям<br>без предварительного запроса."),
    '<div class="i31-c" style="left:886px;top:426px;width:574px;height:50px;background:#c9ecd9;font-size:16.5px">'
    '<span style="font-weight:800;color:#13306e">В одном направлении обмена используется согласованный метод;</span><br>в сети могут сочетаться оба метода.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i31-p" style="left:230px;top:508px;width:1220px;height:196px"></div>',
    '<div class="i31-h" style="left:252px;top:518px">Четыре возможных сочетания</div>',
    '<table class="i31-tb" style="left:248px;top:560px;width:1184px"><tr><th style="width:340px">Управление</th><th style="width:400px">По запросу — DoD</th>'
    '<th>Без запроса — DU</th></tr>'
    '<tr><td>Независимое</td><td>Independent + DoD</td><td style="background:#c9ecd9">Independent + DU<span class="i31-often">Часто используется</span></td></tr>'
    '<tr><td>Упорядоченное</td><td>Ordered + DoD</td><td>Ordered + DU</td></tr></table>',
    '</div>',
    '<div class="step">',
    '<div class="i31-p" style="left:270px;top:718px;width:568px;height:122px"></div>',
    img("i31a_sign.png", "left:286px;top:730px;width:98px"),
    '<div class="i31-t" style="left:398px;top:728px;width:430px"><b>Как выбирается путь?</b>LDP использует следующий хоп из IP-таблицы '
    'пересылки. Получение нескольких привязок не означает выбор по числу метки.</div>',
    '<div class="i31-p" style="left:852px;top:718px;width:578px;height:122px"></div>',
    img("i31a_tag.png", "left:874px;top:730px;width:98px"),
    '<div class="i31-t" style="left:990px;top:728px;width:430px"><b>Метки локальны</b>199 используется на участке LSR1 → LSR2,<br>'
    'а 231 — на участке LSR2 → LSR3.<br>Числа могут различаться для одного FEC.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i31-y" style="left:304px;top:850px;width:1080px;height:72px"></div>',
    img("i31a_gear.png", "left:336px;top:854px;width:62px"),
    '<div class="i31-t" style="left:418px;top:858px;width:960px;color:#13306e"><b style="font-size:25px">Ordered Control не задаёт маршрут TE.</b>'
    'Обычный LDP следует IP-маршрутам; для Traffic Engineering применяют отдельные механизмы.</div>',
    '</div>',
])
