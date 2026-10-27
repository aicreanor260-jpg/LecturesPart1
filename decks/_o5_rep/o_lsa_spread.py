# -*- coding: utf-8 -*-
"""Распространение LSA по областям: LSA-1/2, LSA-3, LSA-5, Stub/NSSA. Схемы — SVG; вырезка только котик."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import puck, svg, cloud_icon, cross, g4_arr, g4_ico, g4_glyph_at

W, H, TOP = 1536, 1024, 166
INK = "#1f1a33"
PK, BL, YE, NAVY = "#ff3d8b", "#2f8fe8", "#ffc400", "#1f3d8f"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


def pill(cx, y, w, text, bgc, s=21):
    return T(cx - w // 2, y, w, s, text, 700, ex="text-align:center;background:%s;border-radius:14px;padding:2px 0" % bgc)


def zone(cx, cy, rx, ry, tone):
    fill, edge = {"p": ("#fde3ee", "#f29cc2"), "b": ("#e0eefc", "#8fbff0"), "y": ("#fff4cf", "#efcf6a")}[tone]
    return ('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" style="fill:%s;fill-opacity:.9" stroke="%s" stroke-width="2.5" '
            'stroke-dasharray="9 7"/>' % (cx, cy, rx, ry, fill, edge))


def two(x1, x2, y, col):
    """Пара стрелок туда-обратно между соседями."""
    return g4_arr(x1, y - 9, x2, y - 9, col, 4) + g4_arr(x2, y + 9, x1, y + 9, col, 4)


CSS = """<style>
.ols-row{position:absolute;left:30px;width:1478px;background:rgba(255,255,255,.75);border:2px solid #ece6ef;border-radius:26px}
</style>"""


def row(y, h, card, title, sub, tone, scene, note, ny, nw, nh, ricon):
    x0, cw, ch, cy = card
    return ('<div class="step"><div class="ols-row" style="top:%dpx;height:%dpx"></div>' % (y, h)
            + B(x0, cy, cw, ch, title[1], 24)
            + svg(g4_ico("tri", 91, cy + ch // 2, 90, tone) + scene, W, H)
            + T(152, cy + 18, cw - 120, 46, title[0], 700, f="Oswald", lh=1.1, ex="white-space:nowrap;letter-spacing:-.01em")
            + T(154, cy + 82, cw - 125, 21, sub, 500, lh=1.25, ex="white-space:nowrap")
            + T(note[0], ny, nw, note[2], note[1], 500, lh=1.3,
                ex="height:%dpx;background:#fdeea0;border-radius:18px;padding:12px 16px;box-sizing:border-box;white-space:nowrap" % nh)
            + svg(ricon, W, H) + '</div>')


S1 = (zone(778, 262, 305, 72, "p") + two(626, 720, 262, PK) + two(836, 930, 262, PK)
      + puck(578, 250, 96, "p") + puck(778, 250, 96, "b") + puck(978, 250, 96, "p"))
S2 = (zone(578, 468, 175, 70, "p") + zone(985, 468, 172, 70, "b")
      + two(522, 576, 468, PK) + two(668, 722, 468, PK) + two(842, 896, 468, PK) + two(978, 1036, 468, BL)
      + puck(483, 458, 78, "p") + puck(628, 458, 78, "p") + puck(782, 455, 100, "b") + puck(935, 458, 78, "b")
      + puck(1085, 458, 78, "b"))
S3 = (zone(770, 652, 140, 64, "p") + zone(1030, 652, 120, 64, "b") + cloud_icon(438, 668, 1.15, "#8cc4f5", "#3f86d8")
      + g4_glyph_at("globe", 440, 655, 36, "#fff", 2.2) + g4_arr(492, 658, 520, 658, NAVY, 3)
      + g4_arr(612, 660, 662, 660, PK, 4) + two(740, 790, 660, PK) + g4_arr(880, 655, 935, 655, PK, 4)
      + two(1000, 1050, 660, BL) + '<path d="M1144 660 h22" stroke="#3f86d8" stroke-width="5" stroke-dasharray="3 7" stroke-linecap="round"/>'
      + puck(568, 648, 78, "p") + puck(710, 648, 78, "p") + puck(833, 648, 78, "b") + puck(975, 648, 76, "b")
      + puck(1095, 648, 76, "b"))
S4 = (zone(410, 830, 160, 66, "b") + zone(773, 830, 150, 66, "p") + zone(1125, 830, 165, 66, "y")
      + g4_ico("ban", 100, 825, 110, "v")
      + two(368, 448, 830, "#8cc4f5") + g4_arr(560, 830, 600, 830, PK, 4) + cross(578, 830, 15, "#e8245e", 7)
      + g4_arr(605, 830, 662, 830, PK, 4, both=True) + g4_arr(750, 830, 790, 830, PK, 4, both=True)
      + g4_arr(885, 830, 985, 830, PK, 4, both=True) + g4_arr(1075, 830, 1180, 830, PK, 4, both=True)
      + g4_arr(1272, 830, 1342, 830, NAVY, 3, both=True)
      + puck(318, 818, 82, "b") + puck(492, 818, 82, "b") + puck(708, 818, 78, "p") + puck(838, 818, 78, "b")
      + puck(1030, 818, 82, "b") + puck(1225, 818, 82, "y")
      + cloud_icon(1422, 850, 1.5, "#8cc4f5", "#3f86d8") + g4_glyph_at("globe", 1422, 832, 50, "#fff", 2.2))

HTML = CSS + bg("bg7", W, H) + "".join([
    row(172, 182, (36, 394, 160, 182), ("LSA-1 и LSA-2", "#ffe8ef"), "Топология одной<br>области", "p",
        S1, (1144, "Распространяются<br>внутри области", 24), 210, 266, 98,
        g4_glyph_at("list", 1458, 262, 58, INK, 2.2))[:-6] + ( pill(782, 184, 118, "Область 0", "#ffb3cd") ) + "</div>",
    row(360, 196, (36, 322, 172, 372), ("LSA-3", "#e3f0fe"), "Сети других<br>областей", "b",
        S2, (1195, "ABR передаёт<br>сведения между<br>областями", 22), 400, 216, 122,
        g4_glyph_at("srv", 1458, 462, 58, INK, 2.2))
    [:-6] + ( pill(597, 384, 112, "Область 0", "#ffc4d8", 20) + pill(785, 399, 64, "ABR", "#ffe36e", 20)
             + pill(992, 384, 112, "Область 1", "#cfe5fd", 20) ) + "</div>",
    row(564, 172, (34, 330, 150, 576), ("LSA-5", "#fff5cc"), "Внешние маршруты", "y",
        S3, (1180, "Распространяется<br>по областям,<br>принимающим LSA-5", 19.5), 590, 242, 120,
        g4_glyph_at("globe", 1462, 650, 58, INK, 2.2))
    [:-6] + ( pill(568, 590, 66, "ASBR", "#ffe36e", 20) + pill(768, 580, 110, "Область 0", "#ffc4d8", 20)
             + pill(1032, 580, 110, "Область 1", "#cfe5fd", 20) ) + "</div>",
    '<div class="step"><div class="ols-row" style="top:742px;height:160px"></div>' + svg(S4, W, H)
    + pill(426, 760, 70, "Stub", "#bcdcfb", 21) + pill(773, 760, 120, "Область 0", "#ffc4d8", 20)
    + pill(1134, 761, 76, "NSSA", "#ffe36e", 21) + '</div>',
    '<div class="step">' + B(54, 910, 1316, 70, "#ffe5ee", 35, "border:2px solid #ffc2d6")
    + svg(g4_ico("excl", 96, 945, 58, "#ff4f8a", "#fff"), W, H)
    + T(145, 926, 1220, 26, "<b style='font-weight:700'>Stub</b> не принимает LSA-5 <span style='color:#ff4f9a'>&bull;</span> "
        "NSSA использует LSA-7 для локальных внешних маршрутов", 500, ex="white-space:nowrap")
    + img("o_lsa_spread_cat.png", "left:1382px;top:905px;width:123px") + '</div>',
])
