# -*- coding: utf-8 -*-
"""Преимущества протоколов по состоянию каналов — 4 карточки + схема областей."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 248

CSS = """<style>
.opr-sub{position:absolute;left:36px;top:256px;font:600 29px/1.1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.opr-c{position:absolute;background:#fff;border:2px solid;border-radius:22px;box-shadow:0 4px 14px rgba(200,150,190,.15)}
.opr-h{position:absolute;font:700 40px/1 Oswald,sans-serif;color:#1f1a33;letter-spacing:-.02em;white-space:nowrap;transform:scaleX(.82);transform-origin:0 0}
.opr-t{position:absolute;font:500 18.5px/1.2 "Golos Text",sans-serif;color:#2b2540}
</style>"""


def card(x, y, w, h, bc, strip, sh, head, text, hy):
    return ('<div class="step"><div class="opr-c" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-color:%s"></div>'
            '%s<div class="opr-h" style="left:%dpx;top:%dpx">%s</div>'
            '<div class="opr-t" style="left:%dpx;top:%dpx;width:310px">%s</div></div>'
            % (x, y, w, h, bc, img(strip, "left:%dpx;top:%dpx;width:350px" % (x + 12, y + 8 if sh else y + 7)),
               x + 20, hy, head, x + 20, hy + 46, text))


HTML = CSS + bg("bg7", W, H) + "".join([
    '<div class="opr-sub">Точная карта сети и быстрая реакция на изменения</div>',
    '<div class="step">' + img("o_pros_art.png", "left:944px;top:240px;width:714px") + '</div>',
    card(28, 310, 365, 300, "#ffd4e6", "o_pros_a.png", 1, "Карта топологии",
         "Каждый маршрутизатор строит общую карту области и вычисляет дерево кратчайших путей SPF.", 425),
    card(412, 310, 365, 300, "#cfe6fb", "o_pros_b.png", 1, "Быстрая сходимость",
         "Получив LSP, маршрутизатор сразу рассылает его через остальные интерфейсы.", 425),
    card(28, 625, 365, 298, "#fff0b8", "o_pros_c.png", 0, "Обновления по событию",
         "После исходной рассылки LSP передаются при изменении топологии и содержат сведения об изменившемся канале. "
         "В отличие от регулярных обновлений distance-vector.", 722),
    card(412, 625, 365, 298, "#ffd4e6", "o_pros_d.png", 0, "Иерархия областей",
         "Агрегация маршрутов, меньшие базы LSDB и локализация сбоя внутри области. Другие области не пересчитывают SPF.", 728),
])
