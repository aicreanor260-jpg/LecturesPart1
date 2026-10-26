# -*- coding: utf-8 -*-
"""Тренажёр CLI маршрутизатора Eltex ESR для деки 2.6: живая консоль, случайные задания, проверка (движок — _i6_cli.js)."""
import os

from _sw_lib import slide, head, sc, grow, col

JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_i6_cli.js"), encoding="utf-8").read()

# 0 DHCP-сервер · 1 DHCP-ретранслятор · 2 DHCP-клиент · 3 Source NAT · 4 Destination NAT · 5 NTP
NAMES = ["DHCP-сервер", "DHCP-ретранслятор", "DHCP-клиент", "Source NAT", "Destination NAT", "NTP"]


def sim(pool):
    return (
        '<div class="clisim6" data-deck="i6" data-pool="%s">'
        '<div class="cs-side"><div class="cs-h">Задание</div><div class="cs-task"></div>'
        '<div class="cs-btns"><button data-cs="new">↻ Обновить задание</button><button data-cs="check">Проверить</button>'
        '<button data-cs="send" class="alt">Отправить пакет</button><button data-cs="sol" class="sec">Решение</button></div>'
        '<div class="cs-res"></div><pre class="cli cs-sol" style="display:none"></pre></div>'
        '<div class="cs-term"><div class="cs-bar"><i></i><i></i><i></i><span>Console · Eltex ESR</span></div>'
        '<div class="cs-out"></div><label class="cs-in"><span class="cs-pr"></span>'
        '<input type="text" spellcheck="false" autocomplete="off" placeholder="введите команду и нажмите Enter"></label></div></div>'
    ) % ",".join(str(i) for i in pool)


def sim_slide(label, title, sub, pool):
    slide(label, sc(head(title, sub), grow("g", col(sim(pool)))))


CSS = ".clisim6{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:16px;flex:1 1 auto;min-height:0}"
# остальные стили консоли (.cs-*) — из _dk_cli.CSS, его подключает _dk_build
