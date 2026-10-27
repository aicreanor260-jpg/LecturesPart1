# -*- coding: utf-8 -*-
"""Помощники группы g3 (вёрстки областей OSPF 2.5): SVG-иконки, облака, текст, стрелки."""
from _o5_ikit import ICO, ICOFILL, puck, line, chip, cross, svg, blob  # noqa: F401
from _ospf_lib import laptop, rack, globe, cloud_icon, legend, bubble  # noqa: F401

K = "#1f1a33"
G3ICO = dict(ICO)
G3ICO.update({
    "doc": '<path d="M6 2.8h8.5l4 4V21H6z"/><path d="M14.5 2.8v4h4M9 11h6M9 14.5h6M9 18h4"/>',
    "ban": '<circle cx="12" cy="12" r="8.6"/><path d="M5.9 5.9l12.2 12.2"/>',
    "arrow": '<path d="M3.5 12h16M13 5.5l6.5 6.5-6.5 6.5"/>',
    "back": '<path d="M17 20V9.5H6.5M10.5 5 6 9.5l4.5 4.5"/>',
    "fork": '<circle cx="12" cy="14" r="2.4"/><circle cx="5" cy="20" r="2"/><circle cx="19" cy="20" r="2"/>'
            '<path d="M12 3v8.6M10.3 15.7 6.4 18.7M13.7 15.7l3.9 3"/>',
    "plus": '<path d="M12 4v16M4 12h16"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "check": '<path d="M4.5 12.5l5 5 10-11"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "stack": '<path d="M12 3 3 7.5l9 4.5 9-4.5zM3 12l9 4.5 9-4.5M3 16.5 12 21l9-4.5"/>',
    "cloud": '<path d="M7 18h10a4 4 0 0 0 .5-8 5.5 5.5 0 0 0-10.6-1A4.5 4.5 0 0 0 7 18z"/>',
    "route": '<circle cx="6" cy="18" r="2.4"/><circle cx="18" cy="6" r="2.4"/><path d="M8.4 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.6"/>',
    "bulb": '<path d="M9 17.5h6M10 21h4M8.5 14.5a6 6 0 1 1 7 0c-.8.6-1 1.4-1 3h-5c0-1.6-.2-2.4-1-3z"/>',
    "cap": '<path d="M2.5 9.5 12 5l9.5 4.5L12 14z"/><path d="M6.5 11.5v4.5c3 2.5 8 2.5 11 0v-4.5M21.5 9.5v5"/>',
    "info": '<path d="M12 10.5v7M12 6.8v.4"/>',
    "diamond": '<path d="M12 3.5 20.5 12 12 20.5 3.5 12z"/>',
    "swap": '<path d="M4 8h14M14 4l4 4-4 4M20 16H6M10 12l-4 4 4 4"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12 20 3M16.5 6.5l2.5 2.5M14 9l2 2"/>',
})
FILL = dict(ICOFILL)
FILL.update({"k": "#d5dae3", "w": "#ffffff", "r": "#ff8a9e"})


def T(x, y, s, fs=18, col=K, anchor="middle", w=700, ff=None):
    """Текст SVG; s может содержать '|' — перенос строки."""
    lines = s.split("|")
    f = ' font-family="%s"' % ff if ff else ""
    out = []
    for i, l in enumerate(lines):
        out.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%.1f" font-weight="%d"%s style="fill:%s">%s</text>'
                   % (x, y + i * fs * 1.22, anchor, fs, w, f, col, l))
    return "".join(out)


def ic(name, cx, cy, d=80, tone="p", ink=K):
    """Кружок-иконка внутри SVG (центр cx, cy)."""
    s = d / 96.0
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)"><circle cx="48" cy="48" r="46" style="fill:%s"/>'
            '<g transform="translate(22 22) scale(2.15)" fill="none" stroke="%s" stroke-width="1.9" '
            'stroke-linecap="round" stroke-linejoin="round">%s</g></g>'
            % (cx - d / 2.0, cy - d / 2.0, s, FILL[tone], ink, G3ICO[name]))


def sq(name, cx, cy, d=44, fill="#7cc0f5", ink=K):
    """Квадратная плашка-иконка (как значок ASBR)."""
    s = d / 24.0 * .7
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" style="fill:%s" stroke="%s" stroke-width="2.4"/>'
            '<g transform="translate(%.1f %.1f) scale(%.3f)" fill="none" stroke="%s" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">%s</g>'
            % (cx - d / 2, cy - d / 2, d, d, d * .2, fill, ink, cx - 12 * s, cy - 12 * s, s, ink, G3ICO[name]))


CL = {"p": ("#fde3ee", "#f6b6d1"), "b": ("#dff0fd", "#a9d2f4"), "y": ("#fff3cc", "#f3d77a"),
      "g": ("#e1f6e8", "#9fdcb7"), "v": ("#ece5fb", "#c4b2f4"), "k": ("#eef0f4", "#c9ced8")}


def cloud(cx, cy, w, h, tone="b", edge=True, op=1):
    """Пушистое облако-область: набор кругов на прямоугольном основании."""
    f, e = CL[tone]
    rx, ry = w / 2.0, h / 2.0
    circ = [(-.62, .18, .42), (-.3, -.22, .5), (.12, -.3, .56), (.5, -.08, .48), (.7, .25, .34), (0, .25, .5), (-.75, .4, .26)]
    parts = []
    for dx, dy, r in circ:
        parts.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f"/>' % (cx + dx * rx, cy + dy * ry, r * rx * .78, r * ry * 1.25))
    parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f"/>' % (cx - rx * .85, cy, rx * 1.7, ry * .62, ry * .3))
    g = "".join(parts)
    st = ('<g style="opacity:%s"><g fill="none" stroke="%s" stroke-width="6">%s</g><g style="fill:%s">%s</g></g>'
          % (op, e, g, f, g)) if edge else '<g style="fill:%s;opacity:%s">%s</g>' % (f, op, g)
    return st


def path(d, col=K, w=5, dash=None, mk=None, both=False):
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    m = (' marker-end="url(#m_%s)"' % mk if mk else "") + (' marker-start="url(#m_%s)"' % mk if both else "")
    return '<path d="%s" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" fill="none"%s%s/>' % (d, col, w, da, m)


def head(x, y, ang, col, s=16):
    """Явный треугольник-наконечник (ang — градусы, 0 = вправо)."""
    return ('<path d="M0 0 L-%.1f -%.1f L-%.1f %.1f z" transform="translate(%.1f %.1f) rotate(%.1f)" style="fill:%s"/>'
            % (s * 1.2, s * .7, s * 1.2, s * .7, x, y, ang, col))


def ban(cx, cy, r=26, col="#e8245e"):
    k = r * .68
    return ('<circle cx="%.1f" cy="%.1f" r="%.1f" style="fill:#fff" stroke="%s" stroke-width="%.1f"/>'
            '<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
            % (cx, cy, r, col, r * .28, cx - k, cy - k, cx + k, cy + k, col, r * .28))


def rect(x, y, w, h, fill="#fff", stroke=None, r=16, sw=2.5):
    s = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" style="fill:%s"%s/>' % (x, y, w, h, r, fill, s)


def pc(x, y, s=1.0):
    """Монитор с системником (низ-центр x, y)."""
    return ('<g transform="translate(%.1f %.1f) scale(%.2f)"><rect x="-45" y="-82" width="70" height="52" rx="5" style="fill:#3a3f55"/>'
            '<rect x="-40" y="-77" width="60" height="42" rx="3" style="fill:#bcd9f6"/><path d="M-14 -30h8l3 24h-14z" style="fill:#9aa3b2"/>'
            '<rect x="-30" y="-8" width="40" height="8" rx="3" style="fill:#9aa3b2"/>'
            '<rect x="28" y="-70" width="24" height="70" rx="4" style="fill:#4a4f66"/><circle cx="40" cy="-58" r="3" style="fill:#7fd0ff"/></g>'
            % (x, y, s))


def asbr_puck(cx, cy, w=104):
    """Серый маршрутизатор ASBR, перечёркнутый красным крестом."""
    return puck(cx, cy, w, "k", "ASBR") + cross(cx, cy + w * .1, w * .38, "#e8245e", 9)
