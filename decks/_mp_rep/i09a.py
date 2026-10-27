# -*- coding: utf-8 -*-
"""pptx 9: упрощённая архитектура стандартного IP-маршрутизатора; вёрстка поверх чистого фона bgk_19."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 170

CSS = """<style>
.i09-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.22)}
.i09-h{position:absolute;font:500 31px/1 "Golos Text",sans-serif;color:#13306e;white-space:nowrap}
.i09-h b{font:900 42px/1 "Rubik",sans-serif}
.i09-a{position:absolute;background:#cdeee5;border-radius:30px}
.i09-b{position:absolute;border:3px solid #1f63c6;border-radius:14px;text-align:center;box-sizing:border-box;
 font:600 21px/1.15 "Golos Text",sans-serif;color:#13306e;padding-top:8px}
.i09-b.k{font-weight:800;font-size:24px}
.i09-x{position:absolute;font:500 18px/1.34 "Golos Text",sans-serif;color:#1d2a44;white-space:nowrap}
.i09-x b{font-weight:800;color:#13306e}
.i09-x ul{margin:0;padding:0;list-style:none}.i09-x li::before{content:"";display:inline-block;width:11px;height:11px;border-radius:50%;
 background:#1f8fc6;margin:0 14px 0 4px}
.i09-n{position:absolute;width:30px;height:30px;border-radius:50%;background:#1fa2b8;color:#fff;font:900 19px/30px "Golos Text",sans-serif;text-align:center}
.i09-tr{position:absolute;font:800 19px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center;width:110px}
.i09-ar{position:absolute;height:3px;background:#13306e}
.i09-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #13306e;border-right:0}
.i09-ar.d::before{content:"";position:absolute;left:-2px;top:-7px;border:8px solid transparent;border-right:12px solid #13306e;border-left:0}
.i09-dn{position:absolute;width:3px;background:#13306e}
.i09-dn::after{content:"";position:absolute;left:-7px;bottom:-2px;border:8px solid transparent;border-top:12px solid #13306e;border-bottom:0}
.i09-spin{animation:i09s 6s linear infinite}
@keyframes i09s{to{transform:rotate(360deg)}}
</style>"""


def box(x, y, w, h, col, txt, k=False):
    return '<div class="i09-b%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s">%s</div>' % (
        " k" if k else "", x, y, w, h, col, txt)


def ar(x, y, w, d=False):
    return '<div class="i09-ar%s" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (" d" if d else "", x, y, w)


def dn(x, y, h):
    return '<div class="i09-dn" style="left:%dpx;top:%dpx;height:%dpx"></div>' % (x, y, h)


def num(n, y, txt):
    return '<div class="i09-n" style="left:908px;top:%dpx">%d</div>' % (y, n) + \
        '<div class="i09-x" style="left:950px;top:%dpx;font-size:17px">%s</div>' % (y - 4, txt)


HTML = CSS + bg("bgk_19") + "".join([
    '<div class="step">',
    '<div class="i09-p" style="left:36px;top:178px;width:1600px;height:412px"></div>',
    '<div class="i09-h" style="left:62px;top:188px"><b>1. Управление</b> — определяет, куда передавать пакеты</div>',
    '<div class="i09-a" style="left:55px;top:240px;width:826px;height:326px"></div>',
    box(72, 262, 204, 130, "#d7ecfa", "Другие<br>маршрутизаторы"), img("i09a_rt.png", "left:130px;top:328px;width:90px"),
    box(342, 262, 246, 116, "#f6977a", "Протоколы<br>маршрутизации:<br>RIP, OSPF, IS-IS", True),
    box(655, 262, 210, 130, "#d7ecfa", "Другие<br>маршрутизаторы"), img("i09a_rt.png", "left:716px;top:328px;width:90px"),
    ar(282, 320, 54, True), ar(596, 320, 52, True), dn(462, 380, 40),
    box(322, 428, 286, 120, "#fde49e", "Таблица<br>маршрутизации", True), img("i09a_tb.png", "left:428px;top:490px;width:74px"),
    '</div>',
    '<div class="step">',
    '<div class="i09-x" style="left:908px;top:236px">Верхняя часть схемы отвечает за получение сведений о сетях<br>и выбор маршрутов.</div>',
    '<div class="i09-x" style="left:908px;top:290px"><b>Протоколы маршрутизации RIP, OSPF, IS-IS</b> обмениваются служебными<br>'
    'сообщениями с другими маршрутизаторами. На основе полученных сведений<br>маршрутизатор выбирает лучшие маршруты и вносит их в таблицу маршрутизации.</div>',
    '<div class="i09-x" style="left:908px;top:374px"><b>В ней указывается:</b><ul>'
    '<li><b>сеть назначения</b>;</li><li><b>следующий маршрутизатор</b> — next hop;</li>'
    '<li><b>выходной интерфейс</b>;</li><li><b>параметры,</b> по которым выбирается маршрут.</li></ul></div>',
    '<div class="i09-x" style="left:908px;top:508px">Таблица также содержит напрямую подключённые сети и может включать<br>'
    'статические маршруты, заданные администратором. Все перечисленные<br>протоколы одновременно запускать необязательно.</div>',
    '</div>',
    '<div class="step">',
    '<div class="ab" style="left:462px;top:588px;width:3px;height:28px;background:#13306e"></div>',
    '<div class="i09-p" style="left:36px;top:612px;width:1390px;height:302px"></div>',
    '<div class="i09-h" style="left:55px;top:625px"><b>2. Продвижение данных</b> — передаёт конкретный пакет</div>',
    '<div class="i09-a" style="left:55px;top:675px;width:826px;height:206px"></div>',
    dn(464, 675, 38),
    '<div class="i09-tr" style="left:50px;top:736px">Входящий<br>трафик</div>', ar(156, 760, 28),
    box(188, 716, 156, 106, "#d7ecfa", "Входной<br>интерфейс"), img("i09a_nic.png", "left:210px;top:776px;width:112px"),
    ar(347, 760, 26),
    box(376, 716, 182, 106, "#f6977a", "IP-продвижение"),
    '<div class="ab" style="left:445px;top:768px;width:50px;height:50px">', img("i09a_gear.png", "left:0;top:0;width:50px", "ab i09-spin"), '</div>',
    ar(561, 760, 26),
    box(590, 716, 156, 106, "#d7ecfa", "Выходной<br>интерфейс"), img("i09a_nic.png", "left:614px;top:776px;width:112px"),
    ar(750, 760, 26), '<div class="i09-tr" style="left:774px;top:736px">Исходящий<br>трафик</div>',
    '</div>',
    '<div class="step">',
    '<div class="i09-x" style="left:908px;top:666px"><b>Нижняя часть схемы</b> использует уже подготовленную<br>информацию о маршрутах:</div>',
    num(1, 718, "<b>Входной интерфейс</b> принимает кадр. Маршрутизатор<br>извлекает из него IP-пакет."),
    num(2, 768, "Блок <b>IP-продвижения</b> читает IP-адрес назначения<br>и находит наиболее специфичный подходящий маршрут."),
    num(3, 818, "Маршрутизатор уменьшает TTL пакета и определяет<br>следующий узел и выходной интерфейс."),
    num(4, 868, "Пакет помещается в новый кадр, подходящий для выходного<br>канала, и отправляется через выходной интерфейс."),
    '</div>',
])
