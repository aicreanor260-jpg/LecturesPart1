# -*- coding: utf-8 -*-
"""Недостатки протоколов по состоянию каналов — память, ЦП, полоса."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 272

CSS = """<style>
.ocn-c{position:absolute;left:35px;width:945px;border:2px solid;border-radius:24px;background:rgba(255,255,255,.95)}
.ocn-h{position:absolute;left:205px;font:700 40px/1 Oswald,sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.9);transform-origin:0 0}
.ocn-t{position:absolute;left:205px;width:420px;white-space:nowrap;font:500 20.5px/1.3 "Golos Text",sans-serif;color:#2b2540}
</style>"""


def card(y, h, bc, ico, iy, pic, head, text):
    return ('<div class="step"><div class="ocn-c" style="top:%dpx;height:%dpx;border-color:%s"></div>%s%s'
            '<div class="ocn-h" style="top:%dpx">%s</div><div class="ocn-t" style="top:%dpx">%s</div></div>'
            % (y, h, bc, img(ico, "left:40px;top:%dpx;width:150px" % iy), pic, y + 30, head, y + 76, text))


HTML = CSS + bg("bg8", W, H) + "".join([
    '<div class="step">' + img("o_cons_art.png", "left:975px;top:0;width:697px") + '</div>',
    card(290, 200, "#ffd4e6", "o_cons_i1.png", 310, img("o_cons_ram.png", "left:600px;top:300px;width:260px"),
         "Память", "Для базы данных состояния<br>каналов и дерева кратчайших<br>путей SPF нужны дополнительные<br>ресурсы памяти."),
    card(505, 190, "#cfe6fb", "o_cons_i2.png", 520, img("o_cons_cpu.png", "left:555px;top:505px;width:420px"),
         "Обработка ЦП", "Алгоритм SPF требует больше<br>времени ЦП, так как строит<br>полную карту топологии."),
    card(708, 200, "#fff0b8", "o_cons_i3.png", 720, img("o_cons_bw.png", "left:592px;top:712px;width:408px"),
         "Полоса пропускания", "Обмен пакетами Hello и лавинная<br>рассылка LSP при первом запуске<br>могут перегружать нестабильные сети<br>с низкой пропускной способностью."),
])
