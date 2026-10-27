# -*- coding: utf-8 -*-
"""2. Stub (вариант 2): Area 0 -> ABR -> Stub, LSA-3 по умолчанию, LSA-5 не входит."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 940, 0
N = "o_stub2_"

CSS = """<style>
.s2-p{position:absolute;border-radius:16px;text-align:center;color:#1f1a33;font:700 21px/1.3 "Golos Text",sans-serif;
 display:flex;flex-direction:column;justify-content:center;align-items:center;white-space:nowrap}
.s2-ip{font:500 20px/1 "JetBrains Mono",monospace;color:#1d5fb8;border-radius:8px}
</style>"""


def p(x0, y0, x1, y1, col, html, extra=""):
    return '<div class="s2-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;%s">%s</div>' % (
        x0, y0, x1 - x0, y1 - y0, col, extra, html)


IPS = ["10.1.0.0/16", "10.2.0.0/16", "10.3.0.0/16", "…"]

HTML = CSS + bg("bg3", W, H) + "".join([
    '<div class="step">' + img(N + "scene.png", "left:25px;top:25px;width:1625px")
    + p(52, 36, 478, 222, "#fff", "")
    + p(312, 250, 520, 316, "#cfe4fa", "<span style='font-size:46px;font-weight:700'>Area 0</span>", "border-radius:28px")
    + p(1168, 245, 1345, 318, "#ffe14d", "<span style='font-size:48px;font-weight:700'>Stub</span>", "border-radius:28px")
    + '</div>',
    '<div class="step">'
    + p(226, 672, 576, 740, "#dcecfb", "Подробные межобластные<br>маршруты: LSA-3")
    + "".join(p(390, 752 + k * 33, 590, 781 + k * 33, "#c9e1fa", s, "", ).replace('class="s2-p"', 'class="s2-p s2-ip"')
              for k, s in enumerate(IPS))
    + '</div>',
    '<div class="step">'
    + p(976, 672, 1286, 740, "#fff6cf", "Внутренняя топология:<br>LSA-1 и LSA-2")
    + '</div>',
    '<div class="step">'
    + p(895, 430, 1348, 478, "#2f8fe8", "<span style='color:#fff'>0.0.0.0/0 • LSA-3 • маршрут по умолчанию</span>", "transform:rotate(-1.5deg);border-radius:6px")
    + '</div>',
    '<div class="step">'
    + p(1000, 548, 1366, 600, "#e8f2fd", "Неизвестный маршрут → к ABR", "font-size:20px")
    + '</div>',
    '<div class="step">'
    + p(498, 182, 836, 236, "#ffd3e2", "LSA-5 не входит в Stub", "font-size:20px")
    + p(1216, 62, 1638, 188, "#fde0ea", "<span><b>ASBR внутри Stub не размещают:</b><br>"
        "<span style='font:400 23px/1.3 Golos Text,sans-serif'>внешние маршруты не попадут<br>в область обычным способом</span></span>",
        "align-items:flex-start;text-align:left;padding-left:14px")
    + '</div>',
])
