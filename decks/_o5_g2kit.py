# -*- coding: utf-8 -*-
"""Группа g2 (Дейкстра, состояния соседства, пакеты, типы маршрутизаторов/областей): дополнительные SVG-элементы
поверх _o5_ikit. Все координаты — пиксели оригинала 1672×941 (рисуется внутри svg() из _o5_ikit)."""
from _o5_ikit import puck, line, chip, cross, svg, blob, globe, cloud_icon, txt, ICO  # noqa: F401
from _ospf_lib import laptop  # noqa: F401

from _o5_ikit import PUCK as _PUCK

K = "#1f1a33"
_PUCK.setdefault("B", ("#9fd2fd", "#62acf2", "#2a6fc4"))   # насыщенный синий (Дейкстра)
_PUCK.setdefault("P", ("#ffc2dc", "#ff8fbf", "#d63f86"))
PINK, BLUE, YEL = "#ff4f9a", "#3a8ff0", "#ffd23a"
OUT = {"B": "#2a6fc4", "P": "#d63f86", "p": "#e05a97", "b": "#3f86d8", "g": "#2f9e62", "y": "#c99a00", "v": "#7a5bd8", "k": "#6b7385"}


def g2_rtr(x, y, w=110, tone="b", label=None, ant=True, check=False, glow=None, fs=None, ah=None):
    """Шайба с антеннами; check — розовая галочка справа; glow — цвет свечения под шайбой."""
    s = []
    if glow:
        s.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" style="fill:%s" opacity=".55"/>'
                 % (x, y + w * .2, w * .72, w * .48, glow))
    if ant:
        a = ah or w * .6
        for k in (-1, 1):
            s.append('<path d="M%.1f %.1f V%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
                     % (x + k * w * .33, y + w * .05, y - a, OUT[tone], w * .055))
    s.append(puck(x, y, w, tone, label, fs))
    if check:
        s.append(g2_chk(x + w * .45, y + w * .3, w * .14))
    return "".join(s)


def g2_chk(x, y, r=15, col=PINK):
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:%s" stroke="#fff" stroke-width="%.1f"/>'
            '<path d="M%.1f %.1f l%.1f %.1f l%.1f %.1f" stroke="#fff" stroke-width="%.1f" fill="none" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
            % (x, y, r, col, r * .18, x - r * .45, y, r * .32, r * .35, r * .6, -r * .65, r * .24))


def g2_ring(x, y, r=11, col=BLUE):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" style="stroke:%s" stroke-width="2.6"/>' % (x, y, r, col)


def g2_wc(x, y, t, r=24, col="#8cc4f5", fs=None, fill="#fff"):
    """Кружок-вес ребра."""
    f = fs or r * 1.05
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:%s;stroke:%s" stroke-width="3"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="800" style="fill:%s">%s</text>'
            % (x, y, r, fill, col, x, y + f * .36, f, K, t))


def g2_lbl(x, y, t, fill="#fff", fs=18, w=None, h=None, r=8, ink=K, weight=800):
    """Плашка с текстом (центр x, y)."""
    w = w or int(len(t) * fs * .62) + 18
    h = h or int(fs * 1.55)
    return ('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="%d" style="fill:%s"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="%d" style="fill:%s">%s</text>'
            % (x - w / 2.0, y - h / 2.0, w, h, r, fill, x, y + fs * .36, fs, weight, ink, t))


def g2_doc(x, y, w=50, edge="#3a3f55", fill="#fff", lines="#8cc4f5"):
    """Документ с загнутым углом (центр x, y)."""
    h = w * 1.25
    x0, y0, c = x - w / 2, y - h / 2, w * .28
    ln = "".join('<path d="M%.1f %.1f h%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
                 % (x0 + w * .2, y0 + h * (.38 + .15 * i), w * (.6 if i < 3 else .4), lines, w * .07) for i in range(4))
    return ('<path d="M%.1f %.1f h%.1f l%.1f %.1f v%.1f h%.1f z" style="fill:%s" stroke="%s" stroke-width="%.1f" '
            'stroke-linejoin="round"/><path d="M%.1f %.1f v%.1f h%.1f" fill="none" stroke="%s" stroke-width="%.1f"/>%s'
            % (x0, y0, w - c, c, c, h - c, -w, fill, edge, w * .05, x0 + w - c, y0, c, c, edge, w * .05, ln))


DBT = {"b": ("#9fd0fb", "#3f86d8", "#d6eafd"), "p": ("#ffb3d1", "#e05a97", "#ffe0ec"),
       "y": ("#ffe27a", "#c99a00", "#fff4c4")}


def g2_db(x, y, w=80, tone="b", tiers=3, label=None, fs=None):
    """Стопка-цилиндр (центр верха x, y)."""
    body, edge, top = DBT[tone]
    ry, th = w * .2, w * .32
    s = []
    for i in range(tiers - 1, -1, -1):
        yy = y + i * th
        s.append('<path d="M%.1f %.1f v%.1f a%.1f %.1f 0 0 0 %.1f 0 v%.1f" style="fill:%s;stroke:%s" stroke-width="%.1f"/>'
                 % (x - w / 2, yy, th, w / 2, ry, w, -th, body, edge, w * .035))
        s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:#fff"/>' % (x + w * .3, yy + th * .75, w * .035))
    s.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" style="fill:%s;stroke:%s" stroke-width="%.1f"/>'
             % (x, y, w / 2, ry, top, edge, w * .035))
    if label:
        f = fs or w * .2
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="900" style="fill:%s">%s</text>'
                 % (x, y + tiers * th - f * .1, f, K, label))
    return "".join(s)


def g2_win(x, y, w, h, title, tone="p", rot=0, body=""):
    """Окошко-«пакет» с шапкой (левый верх x, y)."""
    top, side, out = {"p": ("#ffd6e7", "#f7a9c9", "#e05a97"), "b": ("#d6eafd", "#9fcaf3", "#3f86d8")}[tone]
    return ('<g transform="rotate(%.1f %.1f %.1f)"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="12" '
            'style="fill:%s;stroke:%s" stroke-width="3"/><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" style="fill:%s"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="900" style="fill:%s">%s</text>%s</g>'
            % (rot, x + w / 2, y + h / 2, x, y, w, h, top, out, x + 6, y + 6, w - 12, h * .26, side,
               x + w / 2, y + h * .2 + 2, h * .16, K, title, body))


def g2_path(d, col=PINK, w=5, mk=None, dash=None, both=False):
    m = (' marker-end="url(#m_%s)"' % mk if mk else "") + (' marker-start="url(#m_%s)"' % mk if both else "")
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path d="%s" fill="none" style="stroke:%s" stroke-width="%s" stroke-linecap="round"%s%s/>'
            % (d, col, w, da, m))


def g2_arrow(x1, y1, x2, y2, col=PINK, w=6, head=14):
    """Стрелка со своим наконечником нужного цвета."""
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(a), y2 - head * math.sin(a)
    px, py = -math.sin(a) * head * .62, math.cos(a) * head * .62
    return ('<path d="M%.1f %.1f L%.1f %.1f" style="stroke:%s" stroke-width="%s" stroke-linecap="round"/>'
            '<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f z" style="fill:%s"/>'
            % (x1, y1, bx, by, col, w, x2, y2, bx + px, by + py, bx - px, by - py, col))


def g2_rays(x, y, col=YEL, r1=14, r2=26, angs=(-60, -90, -120), w=4):
    import math
    return "".join('<path d="M%.1f %.1f L%.1f %.1f" style="stroke:%s" stroke-width="%d" stroke-linecap="round"/>'
                   % (x + r1 * math.cos(math.radians(a)), y + r1 * math.sin(math.radians(a)),
                      x + r2 * math.cos(math.radians(a)), y + r2 * math.sin(math.radians(a)), col, w) for a in angs)


def g2_chip(x, y, w=130, label="SPF"):
    """Микросхема (центр x, y)."""
    h = w
    pins = "".join('<path d="M%.1f %.1f v%.1f M%.1f %.1f v%.1f M%.1f %.1f h%.1f M%.1f %.1f h%.1f" stroke="#2b2f3d" '
                   'stroke-width="%.1f"/>' % (x - w * .3 + i * w * .2, y - h / 2 - w * .1, w * .1,
                                              x - w * .3 + i * w * .2, y + h / 2, w * .1,
                                              x - w / 2 - w * .1, y - h * .3 + i * h * .2, w * .1,
                                              x + w / 2, y - h * .3 + i * h * .2, w * .1, w * .045) for i in range(4))
    return ('%s<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="12" style="fill:#3a3f55"/>'
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" style="fill:#ffd6e7"/>'
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="900" style="fill:%s">%s</text>'
            % (pins, x - w / 2, y - h / 2, w, h, x - w * .36, y - h * .36, w * .72, h * .72, x, y + w * .1, w * .26, K, label))


XICO = dict(ICO)
XICO.update({
    "bars": '<path d="M6 19V13M12 19V8M18 19V4" stroke-width="3.6"/>',
    "share": '<circle cx="17" cy="5.5" r="2.6"/><circle cx="6.5" cy="12" r="2.6"/><circle cx="17" cy="18.5" r="2.6"/>'
             '<path d="M8.8 10.8 14.7 6.8M8.8 13.2l5.9 4"/>',
    "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M9 20h6M12 16v4"/>',
    "swap": '<path d="M4 8h15l-4-4M20 16H5l4 4"/>',
    "down": '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    "ban": '<circle cx="12" cy="12" r="8.6"/><path d="M5.9 5.9l12.2 12.2"/>',
    "key": '<circle cx="8" cy="8" r="4.6"/><path d="M11.3 11.3 20 20M16.5 16.5l2.5-2.5M14 14l2-2"/>',
    "tri": '<circle cx="12" cy="5" r="2.6"/><circle cx="5" cy="18" r="2.6"/><circle cx="19" cy="18" r="2.6"/>'
           '<path d="M10.7 7.3 6.3 15.7M13.3 7.3l4.4 8.4M7.6 18h8.8"/>',
    "flag": '<path d="M6 21V4M6 4h11l-2.5 4 2.5 4H6"/>',
    "info": '<path d="M12 10.5v7M12 6.5v.3" stroke-width="3"/>',
    "bulb": '<path d="M9 17.5h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "go": '<path d="M5 12h13M13 6l6 6-6 6" stroke-width="2.6"/>',
    "excl": '<path d="M12 5v9M12 18.5v.3" stroke-width="3.2"/>',
    "book": '<path d="M12 6c-2-1.6-5-2-8-1.5v14c3-.5 6 0 8 1.5 2-1.5 5-2 8-1.5v-14c-3-.5-6-.1-8 1.5zM12 6v14"/>',
})


def g2_ic(name, cx, cy, r=40, fill="#ff8fbf", ink=K, sw=1.9):
    """Кружок-иконка внутри SVG (центр cx, cy)."""
    s = r * 2 / 96.0 * 2.5
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:%s"/><g transform="translate(%.1f %.1f) scale(%.3f)" '
            'fill="none" style="stroke:%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round">%s</g>'
            % (cx, cy, r, fill, cx - 12 * s, cy - 12 * s, s, ink, sw, XICO[name]))


def g2_svgat(x, y, w, h, body, vb=None):
    """Небольшой SVG-элемент в HTML (left/top = x, y); vb — viewBox (по умолчанию 0 0 w h)."""
    return ('<svg class="ab" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;overflow:visible" viewBox="%s" '
            'font-family="Golos Text,sans-serif">%s</svg>' % (x, y, w, h, vb or "0 0 %d %d" % (w, h), body))


def g2_icon_html(name, x, y, d=80, fill="#ff8fbf", ink=K, sw=1.9):
    return g2_svgat(x, y, d, d, g2_ic(name, d / 2.0, d / 2.0, d / 2.0, fill, ink, sw))
