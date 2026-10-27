# -*- coding: utf-8 -*-
"""Помощники группы g5 (LSA-4…LSA-9, Opaque, памятка, LSA в областях, сходимость): HTML-тексты, плашки,
дополнительные иконки и SVG-элементы. Базовые элементы — из _o5_ikit."""
from _o5_ikit import ICO, ICOFILL, puck, line, chip, cross, okbadge, svg, blob, legend, bubble, globe, rack, cloud_icon, FADE  # noqa
from _ospf_lib import laptop  # noqa: F401

INK = "#1f1a33"
NW = "white-space:nowrap"
C = "text-align:center;white-space:nowrap"

G5ICO = dict(ICO)
G5ICO.update({
    "pin": '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    "flag": '<path d="M6 21V3.5M6 4h11l-2.5 4L17 12H6"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4.5 20.5c.8-4 3.8-6 7.5-6s6.7 2 7.5 6z"/>',
    "doc": '<path d="M6 2.8h8.5L19 7.3v13.9H6z"/><path d="M14.5 2.8v4.5H19M9 11h7M9 14.5h7M9 18h5"/>',
    "ip": '<rect x="3.5" y="4.5" width="17" height="15" rx="3"/><path d="M8.5 9v6M12 15V9h2.3a1.8 1.8 0 0 1 0 3.6H12"/>',
    "people": '<circle cx="12" cy="8" r="3"/><circle cx="5.5" cy="10" r="2.3"/><circle cx="18.5" cy="10" r="2.3"/>'
              '<path d="M7 19.5c.5-3.6 2.4-5.4 5-5.4s4.5 1.8 5 5.4zM1.8 18.5c.3-2.5 1.6-3.8 3.7-3.8M22.2 18.5c-.3-2.5-1.6-3.8-3.7-3.8"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3.3-3.3a4 4 0 0 0-5.7-5.7l-1.2 1.2M14 10a4 4 0 0 0-5.7 0L5 13.3A4 4 0 0 0 10.7 19l1.2-1.2"/>',
    "share": '<circle cx="18" cy="5.5" r="2.7"/><circle cx="6" cy="12" r="2.7"/><circle cx="18" cy="18.5" r="2.7"/>'
             '<path d="M8.4 10.7l7.2-3.9M8.4 13.3l7.2 3.9"/>',
    "ban": '<circle cx="12" cy="12" r="8.6"/><path d="M5.9 5.9l12.2 12.2"/>',
    "bulb": '<path d="M9 17.5h6M10 21h4M8.2 14.2A6 6 0 1 1 15.8 14.2c-.8.8-.8 1.6-.8 3.3H9c0-1.7 0-2.5-.8-3.3z"/>',
    "fork": '<circle cx="12" cy="5.5" r="2.4"/><circle cx="5.5" cy="18" r="2.4"/><circle cx="18.5" cy="18" r="2.4"/>'
            '<path d="M12 8v4l-5.3 4M12 12l5.3 4"/>',
    "excl": '<path d="M12 5v9M12 18.3v.2"/>',
    "rtr": '<ellipse cx="12" cy="9" rx="8.5" ry="3.5"/><path d="M3.5 9v5c0 1.9 3.8 3.5 8.5 3.5s8.5-1.6 8.5-3.5V9M9 9h6M12 7.2v3.6"/>',
    "swap": '<path d="M4 8h15l-3.5-3.5M20 16H5l3.5 3.5"/>',
    "cloud": '<path d="M7 18.5h10.5a4 4 0 0 0 .4-8 6 6 0 0 0-11.5-1.3A4.7 4.7 0 0 0 7 18.5z"/>',
    "net": '<circle cx="12" cy="5" r="2.4"/><circle cx="12" cy="19" r="2.4"/><circle cx="4.5" cy="12" r="2.4"/>'
           '<circle cx="19.5" cy="12" r="2.4"/><path d="M12 7.4v9.2M6.9 12h10.2"/>',
    "game": '<rect x="3" y="7" width="18" height="10" rx="4"/><circle cx="8" cy="12" r="1.6"/><circle cx="16" cy="12" r="1.6"/>',
    "pie": '<circle cx="12" cy="12" r="8.6"/><path d="M12 3.4V12l6.1 6.1"/>',
})


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    """Текстовый блок HTML."""
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    """Подложка HTML."""
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


def P(x, y, w, h, s, t, bgc, wt=700, c=INK, r=16, ex=""):
    """Плашка с текстом по центру (flex)."""
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;border-radius:%dpx;'
            'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;white-space:nowrap;'
            'font:%d %spx/1.22 \'Golos Text\',sans-serif;color:%s;%s">%s</div>' % (x, y, w, h, bgc, r, wt, s, c, ex, t))


def ico(name, x, y, d=60, fill="#ff8fbf", ink=INK, sw=1.9):
    """Кружок-иконка HTML (fill — цвет круга или 'none')."""
    f = ICOFILL.get(fill, fill)
    return ('<svg class="ab" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx" viewBox="0 0 96 96">'
            '<circle cx="48" cy="48" r="46" style="fill:%s"/><g transform="translate(22 22) scale(2.15)" fill="none" '
            'stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">%s</g></svg>'
            % (x, y, d, d, f, ink, sw, G5ICO[name]))


def sico(name, x, y, s=40, ink=INK, sw=2):
    """Иконка внутри SVG (без кружка), левый верх — x, y, размер s."""
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round">%s</g>' % (x, y, s / 24.0, ink, sw, G5ICO[name]))


def path(d, col=INK, w=5, dash=None, mk=None, op=1):
    """Произвольная линия-путь (mk — маркер из arrow_defs: ap ab ay ag av ak)."""
    return ('<path d="%s" stroke="%s" stroke-width="%s" fill="none" stroke-linecap="round"%s%s%s/>'
            % (d, col, w, ' stroke-dasharray="%s"' % dash if dash else "", ' marker-end="url(#m_%s)"' % mk if mk else "",
               ' opacity="%s"' % op if op != 1 else ""))


def fat(a, b, col, w=34, head=26, op=1):
    """Толстая стрелка-лента (как у автора) от a к b."""
    import math
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    hw, hh = w / 2.0, w * .95
    bx, by = b[0] - ux * head * 1.4, b[1] - uy * head * 1.4
    pts = [(a[0] + nx * hw, a[1] + ny * hw), (bx + nx * hw, by + ny * hw), (bx + nx * hh, by + ny * hh), b,
           (bx - nx * hh, by - ny * hh), (bx - nx * hw, by - ny * hw), (a[0] - nx * hw, a[1] - ny * hw)]
    return '<path d="M%s z" style="fill:%s" opacity="%s"/>' % (" L".join("%.1f %.1f" % p for p in pts), col, op)


def drum(x, y, w=80, tone="b", label=None, fs=None):
    """Маршрутизатор-цилиндр со стрелками-крестом (как в памятке), центр верха — x, y."""
    top, side, out = {"b": ("#5aa9ee", "#3d8fdc", "#2a6fb8"), "p": ("#ff7fae", "#f2639a", "#c9407a"),
                      "k": ("#cfd4dd", "#b3b9c6", "#7b8396")}[tone]
    rx, ry, h = w / 2.0, w * .22, w * .32
    e = w * .2
    s = ('<path d="M%.1f %.1f v%.1f a%.1f %.1f 0 0 0 %.1f 0 v%.1f" style="fill:%s" stroke="%s" stroke-width="2.2"/>'
         '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" style="fill:%s" stroke="%s" stroke-width="2.2"/>'
         '<g stroke="#fff" stroke-width="%.1f" stroke-linecap="round" fill="none">'
         '<path d="M%.1f %.1f l%.1f %.1f M%.1f %.1f l%.1f %.1f"/></g>'
         % (x - rx, y, h, rx, ry, 2 * rx, -h, side, out, x, y, rx, ry, top, out, w * .04,
            x - e, y - e * .45, 2 * e, e * .9, x + e, y - e * .45, -2 * e, e * .9))
    if label:
        f = fs or w * .2
        s += ('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%.1f" font-weight="800" style="fill:#fff">%s</text>'
              % (x, y + h * .85, f, label))
    return '<g>%s</g>' % s


def server(x, y, w=46, h=80):
    """Сервер-стойка (левый верх)."""
    return rack(x, y, w, h)


def monitor(x, y, w=70, col="#bcd9f6"):
    """Монитор (центр низа подставки)."""
    h = w * .66
    return ('<g><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="#3a3f55"/>'
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" style="fill:%s"/>'
            '<path d="M%.1f %.1f h%.1f l4 %.1f h-%.1f z" fill="#9aa3b2"/></g>'
            % (x - w / 2, y - h - 14, w, h, x - w / 2 + 5, y - h - 9, w - 10, h - 10, col,
               x - 8, y - 14, 16, 14, 24))


def doccard(x, y, s=60, tone="p"):
    """Документ LSA с загнутым углом (левый верх)."""
    f, o = {"p": ("#ffe3ee", "#f2639a"), "b": ("#e3f0fd", "#3d8fdc"), "y": ("#fff4c9", "#d9a400")}[tone]
    k = s / 60.0
    return ('<g transform="translate(%.1f %.1f) scale(%.3f)"><path d="M6 2h32l16 16v40H6z" style="fill:%s" stroke="%s" stroke-width="3"/>'
            '<path d="M38 2v16h16" fill="none" stroke="%s" stroke-width="3"/>'
            '<path d="M14 28h30M14 37h30M14 46h20" stroke="%s" stroke-width="3.4" stroke-linecap="round"/></g>'
            % (x, y, k, f, o, o, o))


def wifi(x, y, s=1.0, col="#ff5c9e"):
    return ('<g transform="translate(%.1f %.1f) scale(%.2f)" fill="none" style="stroke:%s" stroke-width="5" stroke-linecap="round">'
            '<path d="M-26 -8a37 37 0 0 1 52 0M-16 2a23 23 0 0 1 32 0"/><circle cx="0" cy="12" r="3.5" style="fill:%s"/></g>'
            % (x, y, s, col, col))


def stx(x, y, t, fs=16, col=INK, wt=700, anchor="middle"):
    """Текст SVG с цветом через style."""
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" font-weight="%d" style="fill:%s">%s</text>'
            % (x, y, anchor, fs, wt, col, t))


def area(x, y, w, h, fill, edge, r=26, dash="10 8"):
    """Прямоугольная область с пунктиром."""
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" style="fill:%s" stroke="%s" stroke-width="2.4" stroke-dasharray="%s"/>'
            % (x, y, w, h, r, fill, edge, dash))


ANT = {"p": "#e05a97", "b": "#3f86d8", "g": "#2f9e62", "y": "#c99a00", "v": "#7a5bd8", "k": "#6b7385"}


def rtr(x, y, w=110, tone="p", label=None, n=3, fs=None):
    """Шайба-маршрутизатор с антеннами (центр верха — x, y)."""
    c = ANT[tone]
    xs = [-.36, 0, .36] if n == 3 else ([-.3, .3] if n == 2 else [-.4, -.14, .14, .4])
    a = "".join('<path d="M%.1f %.1f V%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
                % (x + k * w, y - w * .02, y - w * .42, c, w * .055) for k in xs)
    return a + puck(x, y, w, tone, label, fs)
