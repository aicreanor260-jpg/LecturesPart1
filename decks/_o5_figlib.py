# -*- coding: utf-8 -*-
"""Общие примитивы схем деки «OSPF 2.5 (по pptx)»: кавайные роутеры-шайбы, облака-области, плашки — из _ospf_lib
(только чтение), плюс обёртки под движок дек 2.2.

ВАЖНО: общий CSS красит `svg.fig text` в var(--ink) (тёмный) — цветной текст задавать через T(...) (style="fill:…").
Пошаговость сцен: атрибут data-ph="N" (виден с шага N), data-ph-only (только на шаге N); сцена — scene(svg, [подписи]).

Предпросмотр: python -X utf8 _o5_figprev.py <модуль> <функция> [аргументы...] → _o5_figprev/<функция>.png
"""
from _ospf_lib import (router, cloudsvg, arrow, link, pill, circ_num, ban, ok, blob, laptop, globe,  # noqa: F401
                       envelope, rack, cat, arrow_defs, bubble, legend, cloud_icon)
from _sw_lib import scene  # noqa: F401

PINK, BLUE, YEL, GRN, VIO, INK, SOFT = "#ff4f9a", "#2f8fe8", "#f2b705", "#2fae6a", "#9b7bf0", "#1f1a33", "#5a5374"


def T(x, y, s, size=16, col=INK, w=700, anchor="middle", mono=False, extra=""):
    fam = ' font-family="JetBrains Mono,monospace"' if mono else ""
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%.1f" font-weight="%d" style="fill:%s"%s%s>%s</text>'
            % (x, y, anchor, size, w, col, fam, extra, s))


def box(x, y, w, h, fill="#fff", stroke="#ffc2dc", r=14, sw=2.5, extra=""):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" stroke="%s" stroke-width="%.1f"%s/>'
            % (x, y, w, h, r, fill, stroke, sw, extra))


def fig(view, body, extra_defs=""):
    """SVG-схема на белой панели деки. view — 'x y w h'."""
    return ('<div class="figwrap o5panel" style="display:flex;min-height:0"><svg class="fig o5fig" viewBox="%s">'
            '<defs>%s%s</defs>%s</svg></div>' % (view, arrow_defs(), extra_defs, body))


def svg_only(view, body, extra_defs=""):
    """SVG без обёртки-панели — для scene(), которая сама даёт панель."""
    return ('<svg class="fig o5fig" viewBox="%s"><defs>%s%s</defs>%s</svg>' % (view, arrow_defs(), extra_defs, body))
