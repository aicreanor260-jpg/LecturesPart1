# -*- coding: utf-8 -*-
"""SVG-примитивы деки 2.4 в стиле инфографик «Маршрутизатор 2.4»:
маршрутизатор — изумрудная «шайба» с золотым ободом и четырьмя стрелками, облака сетей с золотым свечением,
кабели золотые и уходят в свои порты (подпись порта у конца кабеля)."""

GOLD = "#f0c75e"
GOLD2 = "#ffe39a"
TEAL = "#3fd6b0"
RED = "#ff7a5c"
BLUE = "#6cb8ff"
INK = "#fbf3dc"
SOFT = "#d6cfae"
DARK = "#06231a"
SCALE = 1.22  # подписи схем крупнее: проектор


def defs():
    return """<defs>
<radialGradient id="m4rt" cx=".5" cy=".35" r=".7"><stop offset="0" stop-color="#1d5a48"/><stop offset="1" stop-color="#062019"/></radialGradient>
<linearGradient id="m4sw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a5544"/><stop offset="1" stop-color="#05201a"/></linearGradient>
<radialGradient id="m4cl" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#2c6a55"/><stop offset="1" stop-color="#0a2b21"/></radialGradient>
<filter id="m4gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/>
<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<marker id="m4a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#f0c75e"/></marker>
<marker id="m4at" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#3fd6b0"/></marker>
<marker id="m4ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#ff7a5c"/></marker>
<marker id="m4ab" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6cb8ff"/></marker>
</defs>"""


def fig(body, vb="0 0 1200 560"):
    return '<svg class="fig m4" viewBox="%s">%s%s</svg>' % (vb, defs(), body)


def ph(n, only=False):
    if n is None:
        return ""
    return ' data-ph="%d"%s' % (n, " data-ph-only" if only else "")


def t(x, y, s, size=15, col=INK, w=700, anchor="middle", mono=False, p=None):
    size = size * SCALE
    fam = "font-family:JetBrains Mono,Consolas,monospace;" if mono else ""
    return ('<text x="%g" y="%g" text-anchor="%s" style="font-size:%gpx;font-weight:%d;fill:%s;%s"%s>%s</text>'
            % (x, y, anchor, size, w, col, fam, ph(p), s))


def router(x, y, name="", r=34, sub="", col=GOLD, p=None):
    """Маршрутизатор: центр (x,y)."""
    h = r * .55
    o = ['<g%s>' % ph(p)]
    o.append('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="#03140f" stroke="%s" stroke-width="2"/>' % (x, y + h * .55, r, r * .42, col))
    o.append('<rect x="%g" y="%g" width="%g" height="%g" fill="url(#m4rt)"/>' % (x - r, y - h * .45, 2 * r, h))
    o.append('<path d="M%g %gv%g M%g %gv%g" stroke="%s" stroke-width="2"/>' % (x - r, y - h * .45, h, x + r, y - h * .45, h, col))
    o.append('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="url(#m4rt)" stroke="%s" stroke-width="2.4" filter="url(#m4gl)"/>'
             % (x, y - h * .45, r, r * .42, col))
    a = r * .5
    yy = y - h * .45
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        o.append('<path d="M%g %gL%g %g" stroke="#fff" stroke-width="2.2" marker-end="url(#m4a)" opacity=".9"/>'
                 % (x + dx * 4, yy + dy * 2, x + dx * a, yy + dy * a * .42))
    if name:
        o.append(t(x, y + r * .42 + h * .55 + 20, name, 17, GOLD2, 800))
    if sub:
        o.append(t(x, y + r * .42 + h * .55 + 38, sub, 12.5, SOFT, 600, mono=True))
    o.append("</g>")
    return "".join(o)


def switch(x, y, name="", w=110, h=40, l3=False, col=TEAL, p=None):
    """Коммутатор L2 (или L3): центр (x,y)."""
    o = ['<g%s>' % ph(p)]
    o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="7" fill="url(#m4sw)" stroke="%s" stroke-width="2.2" filter="url(#m4gl)"/>'
             % (x - w / 2.0, y - h / 2.0, w, h, col))
    for i, (d, yy) in enumerate(((1, -7), (-1, 7))):
        x0, x1 = (x - 30, x + 30) if d > 0 else (x + 30, x - 30)
        o.append('<path d="M%g %gL%g %g" stroke="#fff" stroke-width="2.2" marker-end="url(#m4at)"/>' % (x0, y + yy, x1, y + yy))
    if l3:
        o.append(t(x + w / 2.0 - 14, y - h / 2.0 + 13, "L3", 11, GOLD2, 900))
    if name:
        o.append(t(x, y + h / 2.0 + 20, name, 15.5, GOLD2, 800))
    o.append("</g>")
    return "".join(o)


def pc(x, y, name="", lines=(), col=GOLD, p=None):
    """Компьютер: центр монитора (x,y); подписи (IP, MAC, шлюз) под ним."""
    o = ['<g%s>' % ph(p)]
    o.append('<rect x="%g" y="%g" width="58" height="38" rx="5" fill="#062019" stroke="%s" stroke-width="2.2"/>' % (x - 29, y - 22, col))
    o.append('<rect x="%g" y="%g" width="48" height="28" rx="2" fill="rgba(63,214,176,.22)"/>' % (x - 24, y - 17))
    o.append('<path d="M%g %gv8M%g %gh30" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (x, y + 16, x - 15, y + 25, col))
    yy = y + 44
    if name:
        o.append(t(x, yy, name, 15, GOLD2, 800))
        yy += 18
    for ln in lines:
        o.append(t(x, yy, ln, 12, SOFT, 600, mono=True))
        yy += 16
    o.append("</g>")
    return "".join(o)


def cloud(x, y, label, w=170, h=78, col=GOLD, p=None, sub=""):
    rx, ry = w / 2.0, h / 2.0
    d = ("M%g %g c-%g 0 -%g -%g -%g -%g c0 -%g %g -%g %g -%g c%g -%g %g -%g %g -%g c%g 0 %g %g %g %g "
         "c%g 0 %g %g %g %g c0 %g -%g %g -%g %gz") % (
        x - rx * .55, y + ry * .75, rx * .45, rx * .45, ry * .55, rx * .45, ry * .55, ry * .5, rx * .3, ry * .55, rx * .5, ry * .55,
        rx * .15, ry * .75, rx * .7, ry * .85, rx * .85, ry * .5, rx * .35, rx * .55, ry * .1, rx * .6, ry * .45,
        rx * .3, rx * .45, ry * .3, rx * .45, ry * .65, ry * .45, rx * .3, ry * .55, rx * .55, ry * .55)
    o = ['<g%s>' % ph(p), '<path d="%s" fill="url(#m4cl)" stroke="%s" stroke-width="2.2" filter="url(#m4gl)"/>' % (d, col)]
    o.append(t(x, y + 6 + (-7 if sub else 0), label, 15, GOLD2, 800))
    if sub:
        o.append(t(x, y + 16, sub, 12, SOFT, 600, mono=True))
    o.append("</g>")
    return "".join(o)


def link(x1, y1, x2, y2, col=GOLD, w=3, dash=False, p=None, pa="", pb="", ia="", ib="", lab="", lab_dy=-10):
    """Кабель от порта к порту: pa/pb — имена портов у концов, ia/ib — IP у концов, lab — подпись сети посередине."""
    da = ' stroke-dasharray="10 7"' if dash else ""
    o = ['<g%s>' % ph(p), '<path d="M%g %gL%g %g" stroke="%s" stroke-width="%g" stroke-linecap="round"%s opacity=".95"/>'
         % (x1, y1, x2, y2, col, w, da)]
    for (px, py, qx, qy, nm, ip) in ((x1, y1, x2, y2, pa, ia), (x2, y2, x1, y1, pb, ib)):
        if not (nm or ip):
            continue
        L = ((qx - px) ** 2 + (qy - py) ** 2) ** .5 or 1
        ux, uy = (qx - px) / L, (qy - py) / L
        ax, ay = px + ux * 46, py + uy * 46
        o.append('<circle cx="%g" cy="%g" r="4.5" fill="%s"/>' % (px + ux * 30, py + uy * 30, col))
        if nm:
            o.append(t(ax - uy * 14, ay + ux * 14 + 4, nm, 12, TEAL, 800, mono=True))
        if ip:
            o.append(t(ax + uy * 14, ay - ux * 14 + 4, ip, 12, SOFT, 700, mono=True))
    if lab:
        o.append(t((x1 + x2) / 2.0, (y1 + y2) / 2.0 + lab_dy, lab, 13.5, GOLD2, 800, mono=True))
    o.append("</g>")
    return "".join(o)


def arrow(x1, y1, x2, y2, col=GOLD, w=3.2, p=None, only=False, dash=False, bow=0):
    mk = {GOLD: "m4a", TEAL: "m4at", RED: "m4ar", BLUE: "m4ab"}.get(col, "m4a")
    da = ' stroke-dasharray="9 6"' if dash else ""
    if bow:
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0 + bow
        d = "M%g %gQ%g %g %g %g" % (x1, y1, mx, my, x2, y2)
    else:
        d = "M%g %gL%g %g" % (x1, y1, x2, y2)
    return ('<path d="%s" stroke="%s" stroke-width="%g" fill="none" marker-end="url(#%s)" class="flow"%s%s/>'
            % (d, col, w, mk, da, ph(p, only)))


def badge(x, y, text, col=GOLD, p=None, only=False, size=14, fill="rgba(4,22,16,.95)"):
    w = max(50, len(text) * size * .6 + 22)
    return ('<g%s><rect x="%g" y="%g" width="%g" height="%g" rx="8" fill="%s" stroke="%s" stroke-width="1.8"/>%s</g>'
            % (ph(p, only), x - w / 2.0, y - size, w, size * 2, fill, col, t(x, y + size * .36, text, size, col, 800)))


def note(x, y, lines, col=GOLD, p=None, only=False, w=360, size=14):
    h = 14 + len(lines) * (size + 6)
    o = ['<g%s>' % ph(p, only), '<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="rgba(4,22,16,.95)" stroke="%s" stroke-width="1.6"/>'
         % (x, y, w, h, col)]
    for i, l in enumerate(lines):
        o.append(t(x + 12, y + 8 + (i + 1) * (size + 6) - 4, l, size, INK, 600, "start"))
    o.append("</g>")
    return "".join(o)


def pkt(x0, y0, x1, y1, label, p, col=GOLD, w=150, h=32, only=True, sub=""):
    """Летящий пакет/кадр: появляется в (x0,y0) на шаге p и уезжает в (x1,y1)."""
    st = "--x0:0px;--y0:0px;--x1:%gpx;--y1:%gpx" % (x1 - x0, y1 - y0)
    o = ['<g class="mv"%s style="%s">' % (ph(p, only), st)]
    o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="7" fill="#1a1405" stroke="%s" stroke-width="2.2" filter="url(#m4gl)"/>'
             % (x0 - w / 2.0, y0 - h / 2.0, w, h, col))
    o.append(t(x0, y0 + (5 if not sub else -2), label, 13, col, 800, mono=True))
    if sub:
        o.append(t(x0, y0 + 12, sub, 10.5, SOFT, 600, mono=True))
    o.append("</g>")
    return "".join(o)


def table(x, y, cols, rows, widths, title="", p=None, hl=(), size=13, col=GOLD):
    """Таблица в SVG (маршруты, ARP): hl — индексы подсвеченных строк."""
    W = sum(widths)
    rh = size + 12
    o = ['<g%s>' % ph(p)]
    y0 = y
    if title:
        o.append(t(x, y + size, title, size + 1, GOLD2, 800, "start"))
        y0 += size + 10
    H = rh * (len(rows) + 1)
    o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="8" fill="rgba(4,22,16,.95)" stroke="%s" stroke-width="1.5"/>' % (x, y0, W, H, col))
    o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="8" fill="rgba(240,199,94,.2)"/>' % (x, y0, W, rh))
    cx = x
    for c, w in zip(cols, widths):
        o.append(t(cx + 8, y0 + rh - 8, c, size - 1, GOLD2, 800, "start"))
        cx += w
    for i, r in enumerate(rows):
        yy = y0 + rh * (i + 1)
        if i in hl:
            o.append('<rect x="%g" y="%g" width="%g" height="%g" fill="rgba(240,199,94,.28)"/>' % (x + 2, yy, W - 4, rh))
        cx = x
        for c, w in zip(r, widths):
            o.append(t(cx + 8, yy + rh - 8, c, size - 1, INK, 600, "start", mono=True))
            cx += w
    o.append("</g>")
    return "".join(o)


def frame(x, y, fields, h=40, p=None, size=13, cap=""):
    """Кадр из цветных полей: fields = [(текст, ширина, цвет)]."""
    o = ['<g%s>' % ph(p)]
    if cap:
        o.append(t(x, y - 8, cap, 13, SOFT, 700, "start"))
    cx = x
    for txt_, w, c in fields:
        o.append('<rect x="%g" y="%g" width="%g" height="%g" rx="5" fill="%s" stroke="#2a1e06" stroke-width="1.5"/>' % (cx, y, w - 3, h, c))
        lines = txt_.split("\n")
        for i, ln in enumerate(lines):
            o.append(t(cx + (w - 3) / 2.0, y + h / 2.0 + 5 + (i - (len(lines) - 1) / 2.0) * (size + 2), ln, size, "#1a1206", 800))
        cx += w
    o.append("</g>")
    return "".join(o)


# цвета полей кадра (как в pptx: payload/IP/MAC/VLAN)
F_PAY = "#f6c9a8"
F_IP = "#ffe39a"
F_MAC = "#bfe8d4"
F_VLAN = "#ff9f8a"
F_TYPE = "#d8c6ff"
F_FCS = "#ffb3b3"
