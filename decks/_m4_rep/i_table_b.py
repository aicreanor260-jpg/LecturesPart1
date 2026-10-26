# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _k import css, box, tx, grid, step, svg, path
W, H, TOP = 1672, 941, 118
P = "m4x-tb"
CSS = css(P) + """<style>
.m4x-tb-t,.m4x-tb-s{font-family:"Playfair Display",serif!important;font-weight:500;font-variant-numeric:lining-nums}
.m4x-tb-l{font-variant-numeric:lining-nums;position:absolute;font-family:"Playfair Display",serif;font-weight:500;color:#f6ebc8;white-space:nowrap;text-shadow:0 2px 6px rgba(0,0,0,.8)}
</style>"""
CLOUD = ('<path d="M25 55 C10 55 3 40 15 33 C12 18 28 10 40 17 C46 3 70 3 75 18 C92 15 100 35 88 43 C95 55 80 58 75 55 Z" '
         'transform="translate(%d %d) scale(%s %s)" fill="rgba(240,199,94,.16)" stroke="#f0c75e" stroke-width="2.6" vector-effect="non-scaling-stroke" filter="url(#m4x-tbgl)"/>')


def cloud(x, y, w, h):
    return CLOUD % (x, y, w / 100.0, h / 60.0)


def rt(cx, cy, w=140):
    return img("t_router.png", "left:%dpx;top:%dpx;width:%dpx" % (cx - w / 2, cy - w * 110 / 150 / 2, w))


def lab(x, y, t, s=29, w=0):
    return '<div class="m4x-tb-l" style="left:%dpx;top:%dpx;font-size:%dpx%s">%s</div>' % (x, y, s, ";font-weight:700" if w else "", t)


clouds = svg(P,
    cloud(322, 135, 212, 170) + cloud(48, 688, 232, 112) + cloud(562, 688, 232, 112) +
    '<path d="M425 455 L425 312" stroke="#f0c75e" stroke-width="3" filter="url(#m4x-tbgl)"/>'
    '<path d="M350 540 L222 645" stroke="#f0c75e" stroke-width="3" filter="url(#m4x-tbgl)"/>'
    '<path d="M498 540 L625 645" stroke="#f0c75e" stroke-width="3" filter="url(#m4x-tbgl)"/>'
    '<g fill="#fff0b8" filter="url(#m4x-tbgl)"><circle cx="425" cy="312" r="7"/><circle cx="425" cy="455" r="7"/><circle cx="348" cy="541" r="7"/>'
    '<circle cx="500" cy="541" r="7"/><circle cx="222" cy="645" r="7"/><circle cx="625" cy="645" r="7"/></g>')
arrow = svg(P, '<path d="M575 438 C640 410 720 365 815 345" fill="none" stroke="#f0c75e" stroke-width="12" stroke-linecap="round" opacity=".9" filter="url(#m4x-tbgl)"/>'
            '<path d="M785 318 L838 343 L792 375 Z" fill="#f0c75e" filter="url(#m4x-tbgl)"/>')

tab = grid(P, 853, 247, [853, 1137, 1422, 1634], [("11.0.0.0/8", "2.2.2.2", "Gi1/0/0"), ("13.0.0.0/8", "3.3.3.2", "Gi1/0/1"),
           ("14.0.0.0/8", "1.1.1.2", "Gi1/0/2")], 66, 32, hdr=('<span style="font-size:27px">Назначение/маска</span>', '<span style="display:inline-block;line-height:1.2;font-size:27px;vertical-align:middle">Следующий<br>маршрутизатор</span>', '<span style="display:inline-block;line-height:1.2;font-size:27px;vertical-align:middle">Исходящий<br>интерфейс</span>'),
           hdrh=99, hl=(0,))
tab2 = grid(P, 853, 607, [853, 1137, 1422, 1634], [("1.1.1.0/30", "1.1.1.1", "Gi1/0/2"), ("1.1.1.1/32", "127.0.0.1", "Gi1/0/2")], 66, 32)

HTML = CSS + bg() + "".join([
    step(clouds, lab(364, 172, "14.0.0.0/8", 31), lab(98, 737, "11.0.0.0/8", 31), lab(613, 737, "13.0.0.0/8", 31)),
    step(rt(430, 262, 140), rt(423, 505, 148), rt(172, 690, 140), rt(672, 690, 140),
         lab(507, 243, "R4", 33, 1), lab(402, 563, "R2", 33, 1), lab(248, 671, "R1", 33, 1), lab(556, 671, "R3", 33, 1),
         lab(452, 309, "1.1.1.2/30", 29), lab(450, 392, "Gi1/0/2", 29), lab(450, 424, "1.1.1.1/30", 29),
         lab(248, 472, "Gi1/0/0", 29), lab(208, 505, "2.2.2.1/30", 29), lab(515, 482, "Gi1/0/1", 29), lab(515, 514, "3.3.3.1/30", 29),
         lab(98, 601, "2.2.2.2/30", 29), lab(640, 603, "3.3.3.2/30", 29)),
    step(arrow),
    step(box(P, 838, 165, 808, 592, "", "border-radius:28px;border-width:2px"), tx(P, "g", 1245, 182, "Таблица маршрутизации R2", 40, 780, "text-transform:none"),
         '<div style="position:absolute;left:853px;top:247px;width:781px;height:493px;border:1.6px solid rgba(240,199,94,.7);border-radius:20px"></div>',
         tab, tx(P, "s", 1245, 563, ". . .", 28, 200, "font-weight:500"), tab2),
])
