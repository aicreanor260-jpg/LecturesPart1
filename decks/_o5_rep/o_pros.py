# -*- coding: utf-8 -*-
"""Преимущества протоколов по состоянию каналов — 4 карточки + схема двух областей в SVG; девушка — вырезка."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import puck, line, chip, cross, okbadge, svg, icon, blob, legend, bubble, globe, rack, cloud_icon, FADE

W, H, TOP = 1672, 941, 248

CSS = """<style>
.opr-sub{position:absolute;left:36px;top:256px;font:600 29px/1.1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.opr-c{position:absolute;background:#fff;border:2.5px solid;border-radius:22px;box-shadow:0 4px 14px rgba(200,150,190,.15)}
.opr-h{position:absolute;font:700 40px/1 Oswald,sans-serif;color:#1f1a33;letter-spacing:-.02em;white-space:nowrap;transform:scaleX(.82);transform-origin:0 0}
.opr-t{position:absolute;font:500 17px/1.2 "Golos Text",sans-serif;color:#2b2540}
</style>"""
BC = {"p": "#ffc2dc", "b": "#cfe6fb", "y": "#fff0b8"}
FC = {"p": "#ff8fbf", "b": "#8cc4f5", "y": "#ffd23a"}


def card(x, y, tone, ico, head, text):
    deco = ('<svg class="ab" style="left:%dpx;top:%dpx;width:170px;height:20px" viewBox="0 0 170 20">'
            '<path d="M8 10h28M52 10h108" stroke="%s" stroke-width="9" stroke-linecap="round"/></svg>' % (x + 140, y + 40, FC[tone]))
    return ('<div class="step"><div class="opr-c" style="left:%dpx;top:%dpx;width:365px;height:300px;border-color:%s"></div>'
            '%s%s<div class="opr-h" style="left:%dpx;top:%dpx">%s</div>'
            '<div class="opr-t" style="left:%dpx;top:%dpx;width:332px">%s</div></div>'
            % (x, y, BC[tone], icon(ico, x + 18, y + 16, 96, tone), deco, x + 20, y + 118, head, x + 20, y + 163, text))


Y, YD, K = "#ffcf2e", "#f2b600", "#2b2f3d"
R = {"R1": (880, 345), "R2": (1050, 300), "R3": (885, 490), "R4": (1200, 410), "R5": (1060, 560),
     "R6": (1420, 330), "R7": (1460, 440), "R8": (1330, 560)}


def scene():
    o = [blob(1015, 430, 225, 185, "p", "Область 1", seed=1, lab_y=272, fs=20),
         blob(1420, 430, 190, 170, "b", "Область 2", seed=2, lab_y=282, fs=20),
         globe(1250, 300, 30), cloud_icon(1590, 360, .7)]
    for a, b in [("R4", "R6"), ("R4", "R7"), ("R6", "R7"), ("R7", "R8"), ("R5", "R8")]:
        o.append(line(R[a], R[b], K, 5))
    o += [line((1000, 310), (935, 335), Y, 7, mk="ay"),            # дерево SPF
          line((880, 380), (882, 470), Y, 7, mk="ay", both=True),
          line((925, 510), (1005, 548), Y, 7, mk="ay"),
          line((1080, 325), (1160, 395), "#e8245e", 5), cross(1118, 358),   # сбой R2–R4
          bubble(1185, 296, "Сбой|канала", "p", fs=17),
          line((1145, 405), (935, 355), YD, 6, "12 9", "ay"),       # LSP после изменения
          line((1145, 425), (935, 488), YD, 6, "12 9", "ay"),
          line((1185, 445), (1100, 535), YD, 6, "12 9", "ay"),
          chip(1035, 372, "LSP"), chip(1030, 460, "LSP"), chip(1180, 500, "LSP")]
    for n, (x, y) in R.items():
        o.append(puck(x, y, 104, "p" if n < "R6" else "b", n))
    o.append(okbadge(1432, 500, ["Область 2", "работает стабильно"], w=232))
    o.append(legend(805, 640, [("line", Y, "Дерево кратчайших путей (SPF)"), ("dash", YD, "Распространение LSP"),
                               ("cross", "#e8245e", "Сбой канала"), ("line", K, "Стабильное соединение")], w=335, fs=15))
    return svg("".join(o))


HTML = CSS + bg("bg7", W, H) + "".join([
    '<div class="opr-sub">Точная карта сети и быстрая реакция на изменения</div>',
    '<div class="step">' + scene() + img("o_pros_girl.png", "left:1300px;top:640px;width:372px;" + FADE) + '</div>',
    card(28, 310, "p", "map", "Карта топологии",
         "Каждый маршрутизатор строит общую карту области и вычисляет дерево кратчайших путей SPF."),
    card(412, 310, "b", "bolt", "Быстрая сходимость",
         "Получив LSP, маршрутизатор сразу рассылает его через остальные интерфейсы."),
    card(28, 625, "y", "bell", "Обновления по событию",
         "После исходной рассылки LSP передаются при изменении топологии и содержат сведения об изменившемся канале. "
         "В отличие от регулярных обновлений distance-vector."),
    card(412, 625, "p", "tree", "Иерархия областей",
         "Агрегация маршрутов, меньшие базы LSDB и локализация сбоя внутри области. Другие области не пересчитывают SPF."),
])
