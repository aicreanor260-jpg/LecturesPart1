# -*- coding: utf-8 -*-
"""Недостатки протоколов по состоянию каналов — память, ЦП, полоса."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img  # noqa: F401
from _o5_ikit import puck, line, svg, rack, cloud_icon
from _o5_g1kit import g1icon, g1cyl, g1ram, g1cpu, g1env, g1warn, g1clock, g1graph, g1monitor, g1antpuck

W, H, TOP = 1672, 941, 272

CSS = """<style>
.ocn-c{position:absolute;left:35px;width:945px;border:2px solid;border-radius:24px;background:rgba(255,255,255,.95)}
.ocn-h{position:absolute;left:205px;font:700 40px/1 Oswald,sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.9);transform-origin:0 0}
.ocn-t{position:absolute;left:205px;width:420px;white-space:nowrap;font:500 20.5px/1.3 "Golos Text",sans-serif;color:#2b2540}
</style>"""


def card(y, h, bc, ico, iy, pic, head, text):
    return ('<div class="step"><div class="ocn-c" style="top:%dpx;height:%dpx;border-color:%s"></div>%s%s'
            '<div class="ocn-h" style="top:%dpx">%s</div><div class="ocn-t" style="top:%dpx">%s</div></div>'
            % (y, h, bc, ico, svg(pic), y + 30, head, y + 76, text))


ENV = [("#ffd6e7", "#e05a97"), ("#cfe6fb", "#3f86d8"), ("#fff1c2", "#c99a00")]


def pic_ram():
    return (g1cyl(625, 318, 105, 150, "#eef0f6", "#6b7385", "#8cc4f5") + g1ram(700, 345, 170, 36, "#ff8fbf", -28)
            + g1ram(735, 395, 190, 36, "#8cc4f5", -8) + g1ram(690, 435, 180, 36, "#ff8fbf", 4))


def pic_cpu():
    return ('<rect x="760" y="518" width="200" height="150" rx="14" style="fill:#f4f8ff;stroke:#cfe0f5" stroke-width="2"/>'
            + g1graph(785, 545, .95) + g1clock(930, 540, 24) + g1cpu(660, 610, 120))


def pic_bw():
    o = [line((690, 845), (915, 845), "#2a2f3d", 16), line((690, 845), (915, 845), "#ffd23a", 5, "14 10")]
    for i in range(9):
        f, e = ENV[i % 3]
        o.append(g1env(705 + i * 25, 845 + (-14 if i % 2 else 12), 34, f, e, (-15, 10, -5, 18, -12)[i % 5]))
    o += [g1warn(815, 770, 58), puck(672, 830, 88, "p"), puck(930, 830, 88, "b")]
    return "".join(o)


def art():
    o = [rack(1555, 320, 90, 200), rack(1565, 560, 90, 200),
         g1monitor(995, 330, 290, 190, g1graph(1040, 370, .95)),
         g1monitor(1305, 300, 240, 160, "".join('<rect x="1325" y="%d" width="%d" height="9" rx="4" style="fill:%s"/>'
                                                  % (322 + i * 20, (150, 110, 180, 90, 140, 120)[i], ("#8cc4f5", "#ff8fbf")[i % 2]) for i in range(6))),
         cloud_icon(1120, 300, .8)]
    cols = ["#8cc4f5", "#ff8fbf", "#ffd23a", "#8cc4f5", "#ff8fbf"]
    for i, c in enumerate(cols):
        x0 = 1220 + i * 50
        o.append('<path d="M%d 690 C%d 780 %d 830 %d 940" fill="none" style="stroke:%s" stroke-width="14" stroke-linecap="round"/>'
                 % (x0, x0, x0 - 160 + i * 70, x0 - 220 + i * 90, c))
    o.append(g1antpuck(1320, 640, 300, "p"))
    for i, (x, y, r) in enumerate([(1060, 640, -20), (1110, 720, 12), (1050, 810, -8), (1190, 860, 15), (1420, 800, -12),
                                   (1500, 880, 20), (1100, 900, 5), (1480, 720, -18)]):
        f, e = ENV[i % 3]
        o.append(g1env(x, y, 54, f, e, r))
    return svg("".join(o))


HTML = CSS + bg("bg8", W, H) + "".join([
    '<div class="step">' + art() + '</div>',
    card(290, 200, "#ffd4e6", g1icon("ram", 52, 316, 140, "p"), 0, pic_ram(),
         "Память", "Для базы данных состояния<br>каналов и дерева кратчайших<br>путей SPF нужны дополнительные<br>ресурсы памяти."),
    card(505, 190, "#cfe6fb", g1icon("cpu", 52, 530, 140, "b"), 0, pic_cpu(),
         "Обработка ЦП", "Алгоритм SPF требует больше<br>времени ЦП, так как строит<br>полную карту топологии."),
    card(708, 200, "#fff0b8", g1icon("swap", 52, 738, 140, "y"), 0, pic_bw(),
         "Полоса пропускания", "Обмен пакетами Hello и лавинная<br>рассылка LSP при первом запуске<br>могут перегружать нестабильные сети<br>с низкой пропускной способностью."),
])
