# -*- coding: utf-8 -*-
"""Элементы инфографик OSPF 2.5, нарисованные в SVG (вместо вырезок): шайба-маршрутизатор как у автора,
плашки, линии, облака-области, легенда, иконки. Вырезками остаются только персонажи (девушки, котики)."""
from _ospf_lib import blob, legend, bubble, globe, rack, cloud_icon, arrow_defs, txt  # noqa: F401  (реэкспорт)

PUCK = {"p": ("#ffd6e7", "#f7a9c9", "#e05a97"), "b": ("#d6eafd", "#9fcaf3", "#3f86d8"),
        "g": ("#d9f3e3", "#a5dfbd", "#2f9e62"), "y": ("#fff1c2", "#ffd96b", "#c99a00"),
        "v": ("#e6defb", "#c4b2f4", "#7a5bd8"), "k": ("#e9ecf2", "#c3c9d4", "#6b7385")}


def puck(x, y, w=110, tone="p", label=None, fs=None):
    """Маршрутизатор-шайба: верх с эмблемой-стрелками, боковина с портами и подписью (центр верха — x, y)."""
    top, side, out = PUCK[tone]
    rx, ry, h = w / 2.0, w * .2, w * .26
    s = []
    s.append('<path d="M%.1f %.1f v%.1f a%.1f %.1f 0 0 0 %.1f 0 v%.1f" fill="%s" stroke="%s" stroke-width="2.4"/>'
             % (x - rx, y, h, rx, ry, 2 * rx, -h, side, out))
    s.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="2.4"/>'
             % (x, y, rx, ry, top, out))
    e = w * .13  # эмблема: 4 стрелки
    s.append('<g stroke="#fff" stroke-width="%.1f" stroke-linecap="round" fill="none">'
             '<path d="M%.1f %.1f h%.1f M%.1f %.1f v%.1f"/>'
             '<path d="M%.1f %.1f l-%.1f %.1f l%.1f %.1f M%.1f %.1f l%.1f %.1f l-%.1f %.1f"/></g>'
             % (w * .028, x - e * 1.4, y, e * 2.8, x, y - e * .62, e * 1.24,
                x - e * .9, y - e * .3, e * .5, e * .3, e * .5, e * .3,
                x + e * .9, y - e * .3, e * .5, e * .3, e * .5, e * .3))
    s.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity=".55"/>' % (x, y, e * 1.9, e * .9, out))
    for k in (-1, 1):  # порты на боковине
        px = x + k * rx * .72 - w * .07
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="#2a2f3d"/>'
                 % (px, y + h * .35, w * .14, h * .5))
    if label:
        f = fs or w * .17
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="800" style="fill:#1b1f2a">%s</text>'
                 % (x, y + h * .95, f, label))
    return '<g>%s</g>' % "".join(s)


def line(a, b, col="#2b2f3d", w=5, dash=None, mk=None, both=False):
    """Отрезок a→b; mk — маркер из arrow_defs (ap, ab, ay, ag, av, ak)."""
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    m = (' marker-end="url(#m_%s)"' % mk if mk else "") + (' marker-start="url(#m_%s)"' % mk if both else "")
    return ('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none"%s%s/>'
            % (a[0], a[1], b[0], b[1], col, w, d, m))


def chip(x, y, text, fill="#ffd23a", ink="#1f1a33", fs=18, w=None, h=None, r=8):
    """Плашка с текстом, центр — x, y."""
    w = w or int(len(text) * fs * .62) + 22
    h = h or int(fs * 1.7)
    return ('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="%d" fill="%s"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" font-weight="800" style="fill:%s">%s</text>'
            % (x - w / 2.0, y - h / 2.0, w, h, r, fill, x, y + fs * .36, fs, ink, text))


def cross(x, y, r=17, col="#e8245e", w=8):
    return ('<path d="M%.1f %.1f l%.1f %.1f M%.1f %.1f l-%.1f %.1f" stroke="%s" stroke-width="%d" stroke-linecap="round"/>'
            % (x - r, y - r, 2 * r, 2 * r, x + r, y - r, 2 * r, 2 * r, col, w))


def okbadge(x, y, lines, fill="#3b9eff", fs=17, w=230):
    """Выноска «✓ текст» (lines — список строк), левый верх — x, y."""
    h = 22 + len(lines) * (fs + 5)
    t = "".join('<text x="%.1f" y="%.1f" font-size="%d" font-weight="700" style="fill:#fff">%s</text>'
                % (x + 58, y + 14 + (i + 1) * (fs + 3), fs, s) for i, s in enumerate(lines))
    return ('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="16" fill="%s"/>'
            '<circle cx="%.1f" cy="%.1f" r="15" fill="#fff"/><path d="M%.1f %.1f l6 6 10 -11" stroke="%s" '
            'stroke-width="4" fill="none" stroke-linecap="round"/>%s'
            % (x, y, w, h, fill, x + 30, y + h / 2.0, x + 22, y + h / 2.0, fill, t))


def svg(body, W=1672, H=941, cls="o5i"):
    """Холст на всю инфографику (координаты = пиксели оригинала)."""
    return ('<svg class="ab %s" style="left:0;top:0;overflow:visible" width="%d" height="%d" viewBox="0 0 %d %d" '
            'font-family="Golos Text,sans-serif">%s%s</svg>' % (cls, W, H, W, H, arrow_defs(), body))


# иконки 24×24 для кружков в карточках
ICO = {
    "map": '<circle cx="12" cy="5.5" r="2.6"/><circle cx="5.5" cy="17.5" r="2.6"/><circle cx="18.5" cy="17.5" r="2.6"/>'
           '<path d="M10.8 7.8 6.8 15.2M13.2 7.8l4 7.4M8.1 17.5h7.8"/>',
    "bolt": '<path d="M13.5 2.5 5 13.5h6.5L10.5 21.5 19 10.5h-6.5z"/>',
    "bell": '<path d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
    "tree": '<circle cx="12" cy="5" r="2.6"/><circle cx="6" cy="18.5" r="2.6"/><circle cx="18" cy="18.5" r="2.6"/>'
            '<path d="M12 7.6V12M12 12H6v3.9M12 12h6v3.9"/>',
    "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    "db": '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/>',
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>',
    "warn": '<path d="M12 3 2.5 20h19z"/><path d="M12 9.5v5M12 17.5v.2"/>',
    "clock": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.5V12l3 2"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "shield": '<path d="M12 2.8 4.5 5.8v5.6c0 4.6 3.2 8.4 7.5 9.8 4.3-1.4 7.5-5.2 7.5-9.8V5.8z"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1.3"/><circle cx="4.5" cy="12" r="1.3"/><circle cx="4.5" cy="18" r="1.3"/>',
    "globe": '<circle cx="12" cy="12" r="8.6"/><path d="M3.4 12h17.2M12 3.4c2.6 2.6 2.6 14.6 0 17.2M12 3.4c-2.6 2.6-2.6 14.6 0 17.2"/>',
}
ICOFILL = {"p": "#ff8fbf", "b": "#8cc4f5", "y": "#ffd23a", "g": "#7fd6a2", "v": "#b9a4f2"}


def icon(name, x, y, d=96, tone="p"):
    """Кружок-иконка как HTML-элемент (left/top = x, y)."""
    return ('<svg class="ab" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx" viewBox="0 0 96 96">'
            '<circle cx="48" cy="48" r="46" fill="%s"/><g transform="translate(22 22) scale(2.15)" fill="none" '
            'stroke="#1f1a33" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">%s</g></svg>'
            % (x, y, d, d, ICOFILL[tone], ICO[name]))


# мягкая маска для вырезки персонажа (края растворяются в фоне)
FADE = ("-webkit-mask:linear-gradient(90deg,transparent,#000 22%),linear-gradient(180deg,transparent,#000 18%);"
        "-webkit-mask-composite:source-in;mask:linear-gradient(90deg,transparent,#000 22%),"
        "linear-gradient(180deg,transparent,#000 18%);mask-composite:intersect")


# ---- группа g4 (stub2 / tstub_nssa / summar / lsa_what / lsa_spread / lsa_what2 / lsa1 / lsa2) ----
import math as _g4m

G4ICO = {
    "eyeoff": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/><path d="M4 20 20 4"/>',
    "ban": '<circle cx="12" cy="12" r="8.6"/><path d="M5.9 5.9l12.2 12.2"/>',
    "redo": '<path d="M18.5 12a6.5 6.5 0 1 1-2-4.7"/><path d="M17 3.5v4.2h-4.2"/>',
    "layers": '<path d="M12 3 3 8l9 5 9-5z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "hash": '<path d="M9.5 3.5 7.5 20.5M16.5 3.5l-2 17M4 9h16.5M3.5 15H20"/>',
    "router": '<ellipse cx="12" cy="13" rx="9" ry="3.6"/><path d="M3 13v3c0 2 4 3.6 9 3.6s9-1.6 9-3.6v-3M8 9.5V4M16 9.5V4"/>',
    "users": '<circle cx="12" cy="8" r="3"/><circle cx="5.5" cy="9.5" r="2.3"/><circle cx="18.5" cy="9.5" r="2.3"/>'
             '<path d="M6.5 19a5.5 5.5 0 0 1 11 0zM1.8 18a4 4 0 0 1 5-3.6M22.2 18a4 4 0 0 0-5-3.6"/>',
    "pin": '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    "bulb": '<path d="M9 17.5h6M9.8 20.5h4.4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.3 1 2.1h5c0-.8.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "excl": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7v6.5M12 16.5v.3"/>',
    "book": '<path d="M3 5.5c3-1 6-1 9 1 3-2 6-2 9-1v13c-3-1-6-1-9 1-3-2-6-2-9-1z"/><path d="M12 6.5v13"/>',
    "doc": '<path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14 3v5h5M9 12h7M9 15.5h7M9 9h3"/>',
    "tri": '<circle cx="12" cy="5.5" r="2.4"/><circle cx="5.5" cy="17.5" r="2.4"/><circle cx="18.5" cy="17.5" r="2.4"/>'
           '<path d="M10.8 7.6 6.7 15.4M13.2 7.6l4.1 7.8M7.9 17.5h8.2"/>',
    "cloud": '<path d="M7 18.5h10.5a4 4 0 0 0 .6-8 6 6 0 0 0-11.4-1.3A4.7 4.7 0 0 0 7 18.5z"/>',
    "drum": '<ellipse cx="12" cy="9" rx="8.5" ry="3.5"/><path d="M3.5 9v6c0 1.9 3.8 3.5 8.5 3.5s8.5-1.6 8.5-3.5V9M7 11.5l10 4M17 11.5l-10 4"/>',
    "box": '<rect x="4" y="5" width="16" height="14" rx="3"/><path d="M4 10h16"/>',
    "radio": '<circle cx="12" cy="12" r="2"/><path d="M8 8a5.6 5.6 0 0 0 0 8M16 8a5.6 5.6 0 0 1 0 8M5 5a10 10 0 0 0 0 14M19 5a10 10 0 0 1 0 14"/>',
    "srv": '<rect x="4" y="3.5" width="16" height="7" rx="2"/><rect x="4" y="13.5" width="16" height="7" rx="2"/><path d="M7.5 7h2M7.5 17h2"/>',
}
G4FILL = {"p": "#ffb3cf", "b": "#b9dafa", "y": "#ffe27a", "g": "#a9e5c0", "v": "#d8cbfa", "w": "#ffffff", "k": "#e6e8ee"}


def g4_glyph(name):
    return G4ICO.get(name) or ICO[name]


def g4_ico(name, cx, cy, d=80, tone="p", ink="#1f1a33"):
    """Кружок-иконка внутри общего svg (центр cx, cy)."""
    s = d / 24.0 * .56
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:%s"/><g transform="translate(%.1f %.1f) scale(%.3f)" fill="none" '
            'stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">%s</g>'
            % (cx, cy, d / 2.0, G4FILL.get(tone, tone), cx - 12 * s, cy - 12 * s, s, ink, g4_glyph(name)))


def g4_glyph_at(name, cx, cy, size=40, ink="#1f1a33", sw=2):
    s = size / 24.0
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round">%s</g>' % (cx - 12 * s, cy - 12 * s, s, ink, sw, g4_glyph(name)))


def g4_arr(x1, y1, x2, y2, col="#ff5c9e", w=6, head=None, dash=None, both=False, curve=0):
    """Стрелка любого цвета: линия (или дуга с прогибом curve) + треугольные наконечники."""
    head = head or w * 3.2
    if curve:
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        L = _g4m.hypot(x2 - x1, y2 - y1) or 1
        cx, cy = mx - (y2 - y1) / L * curve, my + (x2 - x1) / L * curve
    else:
        cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0

    def tip(px, py, qx, qy):
        a = _g4m.atan2(py - qy, px - qx)
        b1 = (px - head * _g4m.cos(a - .45), py - head * _g4m.sin(a - .45))
        b2 = (px - head * _g4m.cos(a + .45), py - head * _g4m.sin(a + .45))
        return '<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f z" style="fill:%s"/>' % (px, py, b1[0], b1[1], b2[0], b2[1], col)

    def back(px, py, qx, qy):
        L = _g4m.hypot(px - qx, py - qy) or 1
        return px - (px - qx) / L * head * .7, py - (py - qy) / L * head * .7
    ex, ey = back(x2, y2, cx, cy)
    sx, sy = back(x1, y1, cx, cy) if both else (x1, y1)
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    o = ('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"%s/>'
         % (sx, sy, cx, cy, ex, ey, col, w, d)) + tip(x2, y2, cx, cy)
    if both:
        o += tip(x1, y1, cx, cy)
    return o


def g4_doc(x, y, w=70, label="", tone="p", glyph="lines", fs=None):
    """Документ с загнутым углом (левый верх x, y); glyph: lines | tri | none."""
    h = w * 1.25
    fill, edge = {"p": ("#ffe3ee", "#e05a97"), "b": ("#e3f0fd", "#3f86d8"), "y": ("#fff4c4", "#c99a00"),
                  "w": ("#ffffff", "#2b2f3d")}[tone]
    c = w * .28
    o = ['<path d="M%.1f %.1f h%.1f l%.1f %.1f v%.1f h%.1f z" style="fill:%s" stroke="#1f1a33" stroke-width="3" '
         'stroke-linejoin="round"/>' % (x, y, w - c, c, c, h - c, -w, fill),
         '<path d="M%.1f %.1f v%.1f h%.1f" fill="none" stroke="#1f1a33" stroke-width="3" stroke-linejoin="round"/>'
         % (x + w - c, y, c, c)]
    if glyph == "lines":
        for i in range(4):
            o.append('<path d="M%.1f %.1f h%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
                     % (x + w * .18, y + h * (.22 + i * .13), w * (.5 if i == 0 else .62), edge, w * .06))
    elif glyph == "tri":
        cx, cy, r = x + w / 2.0, y + h * .38, w * .2
        o.append('<g stroke="%s" stroke-width="%.1f" style="fill:#fff"><path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f z" fill="none"/>'
                 '<circle cx="%.1f" cy="%.1f" r="%.1f"/><circle cx="%.1f" cy="%.1f" r="%.1f"/><circle cx="%.1f" cy="%.1f" r="%.1f"/></g>'
                 % (edge, w * .045, cx, cy - r, cx - r, cy + r * .8, cx + r, cy + r * .8,
                    cx, cy - r, w * .08, cx - r, cy + r * .8, w * .08, cx + r, cy + r * .8, w * .08))
    if label:
        f = fs or w * .26
        o.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="800" style="fill:#1f1a33">%s</text>'
                 % (x + w / 2.0, y + h * .9, f, label))
    return "".join(o)


def g4_db(cx, y, w=150, n=3, label="", tone="b"):
    """База данных из n «шайб» (центр cx, верх y)."""
    top, side, out = PUCK[tone]
    rx, ry, h = w / 2.0, w * .17, w * .3
    o = []
    for i in reversed(range(n)):
        yy = y + i * h
        o.append('<path d="M%.1f %.1f v%.1f a%.1f %.1f 0 0 0 %.1f 0 v%.1f" style="fill:%s" stroke="%s" stroke-width="2.6"/>'
                 % (cx - rx, yy, h, rx, ry, 2 * rx, -h, side, out))
        o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" style="fill:%s" stroke="%s" stroke-width="2.6"/>'
                 % (cx, yy, rx, ry, top, out))
    if label:
        o.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="900" style="fill:#1f1a33">%s</text>'
                 % (cx, y + h * 1.5, w * .2, label))
    return "".join(o)


def g4_tower(x, y, w=46, h=86):
    """Серверная башня (левый верх x, y)."""
    o = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" style="fill:#3a3f55" stroke="#22263a" stroke-width="2"/>'
         % (x, y, w, h)]
    for i in range(int((h - 14) // 14)):
        yy = y + 9 + i * 14
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="8" rx="2" style="fill:#262a3c"/>' % (x + 6, yy, w - 12))
        o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="3" rx="1.5" style="fill:#7fd0ff"/>' % (x + 9, yy + 2.5, w * .3))
    return "".join(o)


def g4_area(x, y, w, h, tone="p", r=40):
    """Область-«подложка» с пунктирной рамкой (прямоугольник со скруглением)."""
    fill, edge = {"p": ("#fde3ee", "#f29cc2"), "b": ("#e0eefc", "#8fbff0"), "y": ("#fff4cf", "#efcf6a"),
                  "k": ("#eceef3", "#b9bfcc"), "g": ("#e3f6ea", "#86d3a8")}[tone]
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" style="fill:%s;fill-opacity:.85" stroke="%s" '
            'stroke-width="3" stroke-dasharray="12 8"/>' % (x, y, w, h, r, fill, edge))


def g4_icon(name, x, y, d=60, tone="p", ink="#1f1a33"):
    """Кружок-иконка как HTML-элемент (left/top = x, y), любые имена из G4ICO/ICO."""
    return ('<svg class="ab" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx" viewBox="0 0 100 100">%s</svg>'
            % (x, y, d, d, g4_ico(name, 50, 50, 98, tone, ink)))
