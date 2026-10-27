# -*- coding: utf-8 -*-
"""pptx: RSVP — состав сигнальных сообщений и параметров потока. Фон bgk_12 (робот Лапуты справа, Пазу и Сита слева)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 206

CSS = """<style>
.i35-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i35-tb{position:absolute;border-collapse:collapse;table-layout:fixed;white-space:nowrap;font:500 20px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i35-tb th{background:#13306e;color:#fff;font-weight:700;height:44px}
.i35-tb td{padding:6px 22px;height:56px;border-bottom:1px solid #b9d9df}
.i35-tb tr:nth-child(odd) td{background:#d4eeea}.i35-tb tr:nth-child(even) td{background:#fdf8ea}
.i35-tb td:first-child{border-right:2px solid #1f63c6}
.i35-tb td:first-child b{font:800 22px/1.2 "Golos Text",sans-serif;color:#13306e;display:block}
.i35-t{position:absolute;white-space:nowrap;font:500 19px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i35-t b{display:block;font:800 25px/1.3 "Golos Text",sans-serif;color:#13306e;margin-bottom:4px}
.i35-y{position:absolute;background:#fbd35b;border:3px solid #1f63c6;border-radius:16px}
</style>"""

ROWS = [("PATH", "Источник → получатель", "Передаёт описание трафика Sender TSpec; создаёт состояние пути<br>для возврата RESV."),
        ("Sender TSpec", "Спецификация трафика", "Характеристики потока: скорость r, глубина ведра b, пиковая скорость p,<br>"
         "минимальная учитываемая единица m и максимальный размер пакета M."),
        ("FlowSpec", "Запрос обслуживания", "Содержит TSpec и, если предусмотрено выбранным сервисом, RSpec —<br>"
         "параметры требуемого обслуживания."),
        ("FilterSpec", "Спецификация фильтра", "Выбирает пакеты, к которым относится резервирование, например<br>по адресу отправителя и порту."),
        ("Дескриптор потока", "", "FlowSpec + FilterSpec: требуемое обслуживание и указание пакетов потока."),
        ("RESV", "Получатель → источник", "Несёт запрос резервирования: стиль резервирования и дескрипторы потоков.<br>"
         "Узлы проверяют ресурсы и политику допуска.")]

HTML = CSS + bg("bgk_12") + "".join([
    '<div class="step">',
    '<div class="i35-p" style="left:216px;top:216px;width:1240px;height:478px"></div>',
    '<table class="i35-tb" style="left:238px;top:228px;width:1198px"><col style="width:308px"><col><tr><th>Элемент</th><th>Что содержит и для чего нужен</th></tr>' +
    "".join('<tr><td><b>%s</b>%s</td><td>%s</td></tr>' % r for r in ROWS) + '</table>',
    '</div>',
    '<div class="step">',
    '<div class="i35-p" style="left:256px;top:710px;width:572px;height:134px"></div>',
    img("i35a_ic1.png", "left:276px;top:718px;width:112px"),
    '<div class="i35-t" style="left:406px;top:724px;width:410px"><b>PATH описывает поток</b>Сообщает, какой трафик будет отправлять<br>'
    'источник. Само по себе ресурсы<br>не резервирует.</div>',
    '<div class="i35-p" style="left:842px;top:710px;width:614px;height:134px"></div>',
    img("i35a_ic2.png", "left:860px;top:718px;width:117px"),
    '<div class="i35-t" style="left:998px;top:724px;width:450px"><b>RESV запрашивает ресурсы</b>Получатель инициирует резервирование;<br>'
    'маршрутизаторы настраивают соответствующие<br>механизмы QoS при принятии запроса.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i35-y" style="left:290px;top:854px;width:1226px;height:72px"></div>',
    img("i35a_gear.png", "left:336px;top:858px;width:78px"),
    '<div class="i35-t" style="left:434px;top:868px;width:1060px;font-weight:800;color:#13306e;font-size:18px">'
    'RSVP — сигнализация. Обслуживание пакетов обеспечивают классификаторы, очереди и планировщики<br>маршрутизаторов.</div>',
    '</div>',
])
