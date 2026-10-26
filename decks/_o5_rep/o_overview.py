# -*- coding: utf-8 -*-
"""Протокол OSPF — обзор: принцип, параметры, версии, компоненты, область."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 188

CSS = """<style>
.oov-sub{position:absolute;left:57px;top:196px;font:700 42px/1.1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.oov-sub i{font-style:normal;background:linear-gradient(transparent 62%,#ffe14d 62%,#ffe14d 88%,transparent 88%)}
.oov-c{position:absolute;background:rgba(255,255,255,.94);border:2px solid #f3e6ef;border-radius:22px;box-shadow:0 4px 14px rgba(200,150,190,.18)}
.oov-h{position:absolute;font:800 26px/1.1 "Golos Text",sans-serif;color:#1f1a33}
.oov-t{position:absolute;font:500 19.5px/1.22 "Golos Text",sans-serif;color:#2b2540}
.oov-t hr{border:0;border-top:2px solid #ddd;margin:6px 0 6px}
.oov-t small{font-size:17.5px}
.oov-pill{position:absolute;left:952px;top:202px;background:#ffc6dd;border-radius:14px;padding:2px 16px;font:800 30px/1.2 "Golos Text",sans-serif;color:#1f1a33}
</style>"""


def card(x, y, w, h, ico, head, text, tw=380, ix=50):
    return ('<div class="step"><div class="oov-c" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>%s'
            '<div class="oov-h" style="left:%dpx;top:%dpx">%s</div>'
            '<div class="oov-t" style="left:%dpx;top:%dpx;width:%dpx;white-space:normal">%s</div></div>'
            % (x, y, w, h, ico, x + 138, y + 16, head, x + 138, y + 50, tw, text))


HTML = CSS + bg("bg7", W, H) + "".join([
    '<div class="oov-sub">Кратчайший путь в <i>сети</i></div>',
    '<div class="step">' + img("o_overview_art.png", "left:570px;top:190px;width:1085px;border-radius:0 0 24px 24px")
    + '<div class="oov-pill">Area 0</div></div>',
    card(35, 270, 524, 166, img("o_overview_i1.png", "left:50px;top:285px;width:100px"), "Принцип",
         "Бесклассовая внутренняя маршрутизация • состояние каналов • кратчайший путь • разделение на области", 300),
    card(35, 452, 524, 204, img("o_overview_i2.png", "left:50px;top:465px;width:100px"), "Параметры",
         '<span style="font-size:21px">IP-протокол: 89 •<br>Preference: 150 •<br>IP multicast: 224.0.0.5 / 224.0.0.6</span>'
         '<hr><small>MAC multicast: 01-00-5E-00-00-05 /<br>01-00-5E-00-00-06</small>', 400),
    card(35, 670, 524, 130, img("o_overview_i3.png", "left:50px;top:682px;width:100px"), "Версии",
         "OSPFv2 — IPv4 •<br>OSPFv3 — IPv6 и расширения<br>для IPv4", 360),
    card(35, 815, 938, 104, img("o_overview_i4.png", "left:50px;top:822px;width:95px"), "Компоненты",
         "3 базы данных • 5 типов пакетов • 7 состояний • 4 типа маршрутизаторов •<br>"
         "6 типов областей • 11 типов записей LSDB • 4 типа сетей • 3 роли маршрутизаторов", 830),
    card(988, 815, 652, 104, img("o_overview_i5.png", "left:1003px;top:822px;width:95px"), "Область",
         "Общая база состояния каналов • собственные IP-сети •<br>рекомендуется до 50 маршрутизаторов", 560),
])
