# -*- coding: utf-8 -*-
"""Тренажёр-консоль маршрутизатора ESR для деки «Протокол OSPF» (движок — _o5_cli.js, вёрстка и CSS — как _dk_cli)."""
import os

from _sw_lib import slide, head, sc, grow, col
from _dk_cli import CSS  # noqa: F401  (общий вид консоли)

JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_o5_cli.js"), encoding="utf-8").read()


def sim(pool):
    return (
        '<div class="clisim o5sim" data-pool="%s">'
        '<div class="cs-side"><div class="cs-h">Задание</div><div class="cs-task"></div>'
        '<div class="cs-btns"><button data-cs="new">↻ Обновить задание</button><button data-cs="check">Проверить</button>'
        '<button data-cs="send" class="alt">Отправить Hello</button><button data-cs="sol" class="sec">Решение</button></div>'
        '<div class="cs-res"></div><pre class="cli cs-sol" style="display:none"></pre></div>'
        '<div class="cs-term"><div class="cs-bar"><i></i><i></i><i></i><span>Console · Eltex ESR</span></div>'
        '<div class="cs-out"></div><label class="cs-in"><span class="cs-pr"></span>'
        '<input type="text" spellcheck="false" autocomplete="off" placeholder="введите команду и нажмите Enter"></label></div></div>'
    ) % ",".join(str(i) for i in pool)


def sim_slide(label, title, sub, pool):
    slide(label, sc(head(title, sub), grow("g", col(sim(pool)))))
