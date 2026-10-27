# -*- coding: utf-8 -*-
"""Протокол OSPF — обзор: принцип, параметры, версии, компоненты, область."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import puck, line, svg, blob, rack, cloud_icon, FADE
from _o5_g1kit import g1icon, g1antpuck, G1FADE

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


R = {"R1": (790, 300), "R2": (1110, 270), "R3": (1150, 440), "R4": (1420, 500), "R5": (1555, 660), "R6": (1260, 690)}
LB = "#7fb6ea"


def scene():
    o = [blob(960, 330, 300, 140, "p", seed=1), blob(1430, 600, 215, 175, "b", seed=2),
         rack(1470, 205, 74, 130), rack(1555, 225, 74, 130), cloud_icon(1380, 240, .8), cloud_icon(1620, 400, .6)]
    for a, b in [("R1", "R2"), ("R1", "R3"), ("R2", "R3"), ("R4", "R6"), ("R6", "R5")]:
        o.append(line(R[a], R[b], LB, 7))
    o += [line((1215, 475), (1350, 505), "#fff38a", 18), line((1215, 475), (1340, 505), "#ff5c9e", 7, mk="ap"),
          line((1460, 555), (1520, 625), "#fff38a", 18), line((1462, 557), (1515, 620), "#ff5c9e", 7, mk="ap", both=True)]
    for n, (x, y) in R.items():
        o.append(g1antpuck(x, y, 150, "p" if n < "R4" else "b", n))
    return svg("".join(o))


HTML = CSS + bg("bg7", W, H) + "".join([
    '<div class="oov-sub">Кратчайший путь в <i>сети</i></div>',
    '<div class="step">' + scene() + img("o_overview_girl.png", "left:565px;top:425px;width:520px;" + G1FADE)
    + '<div class="oov-pill">Area 0</div><div class="oov-pill" style="left:1460px;top:395px;background:#cfe6fb">Area 1</div></div>',
    card(35, 270, 524, 166, g1icon("map", 50, 285, 96, "p"), "Принцип",
         "Бесклассовая внутренняя маршрутизация • состояние каналов • кратчайший путь • разделение на области", 300),
    card(35, 452, 524, 204, g1icon("gear", 50, 465, 96, "b"), "Параметры",
         '<span style="font-size:21px">IP-протокол: 89 •<br>Preference: 150 •<br>IP multicast: 224.0.0.5 / 224.0.0.6</span>'
         '<hr><small>MAC multicast: 01-00-5E-00-00-05 /<br>01-00-5E-00-00-06</small>', 400),
    card(35, 670, 524, 130, g1icon("doc", 50, 682, 96, "y"), "Версии",
         "OSPFv2 — IPv4 •<br>OSPFv3 — IPv6 и расширения<br>для IPv4", 360),
    card(35, 815, 938, 104, g1icon("db", 50, 822, 96, "p"), "Компоненты",
         "3 базы данных • 5 типов пакетов • 7 состояний • 4 типа маршрутизаторов •<br>"
         "6 типов областей • 11 типов записей LSDB • 4 типа сетей • 3 роли маршрутизаторов", 830),
    card(988, 815, 652, 104, g1icon("net", 1003, 822, 96, "b"), "Область",
         "Общая база состояния каналов • собственные IP-сети •<br>рекомендуется до 50 маршрутизаторов", 560),
])
