# -*- coding: utf-8 -*-
"""Схемы деки MPLS 2.9 в стиле инфографик (небо Гибли, кремовые панели, синие маршрутизаторы).
Все устройства, метки, интерфейсы и адреса — как на рисунках pptx «2.9. MPLS»."""

from _sw_lib import scene, uid

INK = "#1d2a44"
BLUE = "#1f63c6"
ORG = "#e8742c"
GRN = "#2f9e5b"
RED = "#d9363e"
FS = 1.5  # схемы встраиваются в половину слайда: кегль крупнее, чтобы читалось с проектора
GRY = "#8a97ab"


def t(x, y, s, size=17, col=INK, w=800, anchor="middle", extra=""):
    return ('<text x="%g" y="%g" font-size="%g" font-weight="%d" text-anchor="%s" style="fill:%s"%s>%s</text>'
            % (x, y, size * FS, w, anchor, col, extra, s))


def router(x, y, name="", sub="", col=BLUE, r=30, ph=None, lab_up=False):
    """Маршрутизатор-«цилиндр» как в инфографиках: верх светлый, на крышке стрелки."""
    a = ' data-ph="%d"' % ph if ph is not None else ""
    top = {"#1f63c6": "#8fc3ff", RED: "#ffb3b3", GRY: "#d6dde8", GRN: "#a6e3bd", ORG: "#ffc89e"}.get(col, "#8fc3ff")
    g = ['<g%s>' % a,
         '<path d="M%g %g v16 a%g %g 0 0 0 %g 0 v-16" style="fill:%s;stroke:#0d2f66;stroke-width:2"/>'
         % (x - r, y - 4, r, r * .42, 2 * r, col),
         '<ellipse cx="%g" cy="%g" rx="%g" ry="%g" style="fill:%s;stroke:#0d2f66;stroke-width:2"/>'
         % (x, y - 4, r, r * .42, top),
         '<path d="M%g %g l9 5 M%g %g l-9 5 M%g %g l9 -5 M%g %g l-9 -5" style="stroke:#fff;stroke-width:3;fill:none;stroke-linecap:round"/>'
         % (x - 15, y - 9, x + 15, y - 9, x - 15, y + 1, x + 15, y + 1)]
    ny = y - r * .42 - 16 if lab_up else y + r * .42 + 40
    if name:
        g.append(t(x, ny, name, 18, INK, 900))
    if sub:
        g.append(t(x, ny + 26, sub, 13, "#3a4b6e", 700))
    g.append("</g>")
    return "".join(g)


def link(x1, y1, x2, y2, col="#5d7396", w=4, dash=False, ph=None, arrow=False, cls=""):
    a = ' data-ph="%d"' % ph if ph is not None else ""
    d = ' stroke-dasharray="10 7"' if dash else ""
    m = ' marker-end="url(#mpA%s)"' % col.strip("#") if arrow else ""
    c = ' class="%s"' % cls if cls else ""
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" style="stroke:%s;stroke-width:%g"%s%s%s%s/>'
            % (x1, y1, x2, y2, col, w, d, m, a, c))


def path(d, col=ORG, w=4, dash=False, ph=None, arrow=True):
    a = ' data-ph="%d"' % ph if ph is not None else ""
    ds = ' stroke-dasharray="10 7"' if dash else ""
    m = ' marker-end="url(#mpA%s)"' % col.strip("#") if arrow else ""
    return '<path d="%s" style="fill:none;stroke:%s;stroke-width:%g"%s%s%s/>' % (d, col, w, ds, m, a)


def defs():
    out = []
    for c in (INK, BLUE, ORG, GRN, RED, GRY, "#5d7396"):
        k = c.strip("#")
        out.append('<marker id="mpA%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
                   '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>' % (k, c))
    return "<defs>%s</defs>" % "".join(out)


def box(x, y, w, h, s, fill="#fff", col=INK, size=16, stroke="#0d2f66", ph=None, only=None, rx=8, w8=800):
    a = ' data-ph="%d"' % ph if ph is not None else ""
    if only is not None:
        a = ' data-ph="%d" data-ph-only="1"' % only
    lines = s.split("\n")
    ty = y + h / 2.0 - (len(lines) - 1) * size * .6 + size * .35
    tx = "".join(t(x + w / 2.0, ty + i * size * FS * 1.18, ln, size, col, w8) for i, ln in enumerate(lines))
    return ('<g%s><rect x="%g" y="%g" width="%g" height="%g" rx="%g" style="fill:%s;stroke:%s;stroke-width:2.2"/>%s</g>'
            % (a, x, y, w, h, rx, fill, stroke, tx))


def pkt(x, y, labels, ph=None, only=None, ipw=40):
    """Пакет: [метка][метка]…[IP] — верхняя метка слева (как в инфографиках)."""
    a = ' data-ph="%d"' % ph if ph is not None else ""
    if only is not None:
        a = ' data-ph="%d" data-ph-only="1"' % only
    cols = [ORG, "#f2b134", "#9b7ad6"]
    g = ['<g%s>' % a]
    cx = x
    for i, lb in enumerate(labels):
        w = 16 + 15 * len(str(lb))
        g.append('<rect x="%g" y="%g" width="%g" height="36" rx="4" style="fill:%s;stroke:#5a2a08;stroke-width:2"/>'
                 % (cx, y, w, cols[i % 3]))
        g.append(t(cx + w / 2.0, y + 26, str(lb), 15, "#fff", 900))
        cx += w + 2
    g.append('<rect x="%g" y="%g" width="%g" height="36" rx="4" style="fill:#fff;stroke:#0d2f66;stroke-width:2"/>' % (cx, y, ipw))
    g.append(t(cx + ipw / 2.0, y + 26, "IP", 14, BLUE, 900))
    g.append("</g>")
    return "".join(g)


def cloud(x, y, w, h, fill="#dff0ff", stroke="#7fb3ea", label="", ph=None):
    a = ' data-ph="%d"' % ph if ph is not None else ""
    r = min(w, h) / 2.0
    lab = t(x + w / 2.0, y + 30, label, 17, "#1a4f9c", 900) if label else ""
    return ('<g%s><rect x="%g" y="%g" width="%g" height="%g" rx="%g" style="fill:%s;stroke:%s;stroke-width:3;stroke-dasharray:2 0"/>%s</g>'
            % (a, x, y, w, h, r, fill, stroke, lab))


def netcloud(x, y, s, ph=None):
    """Сеть назначения «облачком» (как 132.100.0.0 / 105.0.0.0 на рисунках pptx)."""
    w = 30 + len(s) * 10.5
    return cloud(x - w / 2.0, y - 22, w, 44, "#fffaf0", "#7fb3ea", "", ph) + t(x, y + 7, s, 17, INK, 900)


def svg(body, vb="0 0 1200 520"):
    return '<svg class="fig mpfig" viewBox="%s" xmlns="http://www.w3.org/2000/svg">%s%s</svg>' % (vb, defs(), body)


def panel(html):
    return '<div class="figwrap mppanel">%s</div>' % html


def sc(body, phases, vb="0 0 1200 520"):
    return scene(svg(body, vb), phases, uid("mp"))
