# -*- coding: utf-8 -*-
"""VLAN: преимущества — 4 карточки (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 108

CSS = """<style>
.vpr-b{position:absolute;box-sizing:border-box;border:5px solid #2a1a0a;box-shadow:5px 5px 0 #000;background:#fff8ea}
.vpr-sub{background:#fff;border-color:#13245a;font:800 28px/50px "Golos Text",sans-serif;color:#13245a;text-align:center}
.vpr-h{position:absolute;box-sizing:border-box;font:800 33px/50px "Golos Text",sans-serif;color:#13245a;padding:0 16px;white-space:nowrap}
.vpr-t{position:absolute;font:500 21px/1.27 "Golos Text",sans-serif;color:#1a1a2a}
.vpr-n{position:absolute;box-sizing:border-box;font:500 19px/1.2 "Golos Text",sans-serif;color:#1a1a2a;padding:8px 18px}
.vpr-grn{background:#3fae3a;border-color:#1c4a14;color:#fff;font:700 29px/56px "Golos Text",sans-serif;text-align:center}
.vpr-grn b{font-family:"Pixelify Sans",sans-serif;font-size:34px}
.vpr-bob{animation:vprb 2.8s ease-in-out infinite}
@keyframes vprb{50%{transform:translateY(-5px)}}
</style>"""


def b(x, y, w, h, cls="", inner="", st=""):
    return '<div class="vpr-b %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def h(x, y, s, c):
    return '<div class="vpr-h" style="left:%dpx;top:%dpx;background:%s">%s</div>' % (x, y, c, s)


def t(x, y, s, cls="vpr-t", st=""):
    return '<div class="%s" style="left:%dpx;top:%dpx;%s">%s</div>' % (cls, x, y, st, s)


def bob(i):
    return '<div class="vpr-bob" style="position:absolute;left:0;top:0">%s</div>' % i


HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="step">' + b(416, 116, 840, 54, "vpr-sub", "Логическое разделение — удобное управление сетью") + '</div>',
    '<div class="step">' + b(84, 188, 744, 290, "", "", "border-color:#3a9a2a")
    + bob(img("v_pros_shield.png", "left:108px;top:203px;width:124px")) + h(240, 216, "Безопасность", "#d8f0d0")
    + t(248, 284, "Изоляция групп<br>пользователей снижает<br>риск нежелательного<br>доступа к данным.")
    + t(114, 402, "Доступ между VLAN контролируют<br>ACL или межсетевой экран.", "vpr-n", "background:#e4f4dc")
    + img("v_pros_sec.png", "left:498px;top:250px;width:314px") + '</div>',
    '<div class="step">' + b(842, 188, 746, 290, "", "", "border-color:#1aa8b8")
    + bob(img("v_pros_env.png", "left:873px;top:208px;width:104px")) + h(988, 216, "Меньше широковещательный домен", "#d6f0f8")
    + t(874, 306, "Broadcast остаётся внутри<br>VLAN: меньше устройств<br>получает и обрабатывает<br>лишние кадры.")
    + img("v_pros_cloud.png", "left:1150px;top:278px;width:412px") + '</div>',
    '<div class="step">' + b(84, 496, 744, 314, "", "", "border-color:#7a3ad0")
    + bob(img("v_pros_gear.png", "left:108px;top:513px;width:114px")) + h(240, 528, "Упрощённое обслуживание", "#eadcff")
    + t(114, 632, "Имена VLAN и группировка<br>портов упрощают настройку,<br>поиск ошибок и подключение<br>пользователей.", "vpr-t", "font-size:20px")
    + img("v_pros_sw.png", "left:418px;top:590px;width:394px") + '</div>',
    '<div class="step">' + b(842, 496, 746, 314, "", "", "border-color:#e0443a")
    + bob(img("v_pros_chart.png", "left:868px;top:513px;width:109px")) + h(988, 528, "Масштабируемость", "#ffdcd6")
    + t(872, 630, "Пользователей одной VLAN<br>можно объединять через<br>несколько коммутаторов<br>независимо от рабочего места.", "vpr-t", "font-size:19px")
    + img("v_pros_trunk.png", "left:1163px;top:588px;width:419px")
    + t(872, 756, "При наличии подходящей сетевой связности.", "vpr-n", "background:#ffe6e2;font-size:17px") + '</div>',
    '<div class="step">' + b(250, 830, 1172, 66, "vpr-grn", "<b>VLAN:</b> изоляция трафика, меньше лишней рассылки и гибкое управление.") + '</div>',
])
