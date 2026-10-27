# -*- coding: utf-8 -*-
"""Схемы деки «Протокол RIP» (2.5.1) в стиле инфографик автора: мятные панели, бирюзовые
маршрутизаторы-«шайбы», пастельные облака сетей. Все схемы перерисованы с картинок pptx:
те же устройства, интерфейсы, сети и метрики. Цвет текста — через style (правило дек по pptx)."""

from _sw_lib import uid, _esc

INK = "#17463a"
SOFT = "#4f7a6d"
TEAL = "#2c8f80"
GRN = "#1f8a55"
RED = "#d6336c"
BLUE = "#3d6fd6"
AMB = "#e0a800"
CLOUD = {"blue": ("#dbe9ff", "#8fb1ea"), "green": ("#d9f3df", "#86c99a"), "red": ("#ffd9dc", "#ee9aa3"),
         "violet": ("#e9e0fb", "#b8a3e6"), "orange": ("#ffe3c4", "#f0b170"), "yellow": ("#fff3c4", "#e8cf6e"),
         "mint": ("#d8f5ec", "#84cdb7")}


def ph(n, only=False):
    if n is None:
        return ""
    return ' data-ph="%d"%s' % (n, " data-ph-only" if only else "")


def t(x, y, s, size=16, col=INK, w=700, anchor="middle", mono=False, extra=""):
    fam = "font-family:JetBrains Mono,Consolas,monospace;" if mono else ""
    return ('<text x="%g" y="%g" text-anchor="%s" font-size="%g" font-weight="%d" style="fill:%s;%s"%s>%s</text>'
            % (x, y, anchor, size, w, col, fam, extra, s))


def defs():
    k = uid("rp")
    return k, ("""<defs>
<linearGradient id="%(k)sr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2fae9b"/><stop offset="1" stop-color="#16756d"/></linearGradient>
<linearGradient id="%(k)st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ee6d2"/><stop offset="1" stop-color="#36b8a4"/></linearGradient>
<marker id="%(k)sag" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="15" refY="9" orient="auto-start-reverse"><path d="M0 0L18 9L0 18z" fill="%(g)s"/></marker>
<marker id="%(k)sab" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="15" refY="9" orient="auto-start-reverse"><path d="M0 0L18 9L0 18z" fill="%(b)s"/></marker>
<marker id="%(k)sar" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="15" refY="9" orient="auto-start-reverse"><path d="M0 0L18 9L0 18z" fill="%(r)s"/></marker>
<marker id="%(k)sat" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="15" refY="9" orient="auto-start-reverse"><path d="M0 0L18 9L0 18z" fill="%(t)s"/></marker>
</defs>""" % {"k": k, "g": GRN, "b": BLUE, "r": RED, "t": TEAL})


class Fig(object):
    """Сборщик одной SVG-схемы: маркеры и градиенты с уникальными id."""

    def __init__(self, w=1200, h=560):
        self.w, self.h = w, h
        self.k, self.d = defs()
        self.wires, self.back, self.front = [], [], []

    def svg(self):
        return ('<svg class="fig rpfig" viewBox="0 0 %d %d">%s%s%s</svg>'
                % (self.w, self.h, self.d, "".join(self.wires) + "".join(self.back), "".join(self.front)))

    # --------------------------------------------------------------- устройства
    def router(self, x, y, name, s=1.0, p=None, col=None):
        """Маршрутизатор-«шайба» как на инфографиках; (x, y) — центр."""
        rw, rh, bh = 62 * s, 20 * s, 30 * s
        top = "url(#%st)" % self.k
        body = col or "url(#%sr)" % self.k
        g = ['<g%s>' % ph(p)]
        g.append('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="rgba(15,92,71,.16)"/>' % (x, y + bh + 6 * s, rw + 4, rh))
        g.append('<path d="M%g %g v%g a%g %g 0 0 0 %g 0 v%g z" fill="%s"/>'
                 % (x - rw, y, bh, rw, rh, 2 * rw, -bh, body))
        g.append('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s" stroke="#a6f0e2" stroke-width="1.2"/>' % (x, y, rw, rh, top))
        a = 13 * s  # четыре белые стрелки на крышке
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x1, y1 = x + dx * 5 * s, y + dy * 3 * s
            x2, y2 = x + dx * (a + 16 * s), y + dy * (a * .55 + 3 * s)
            g.append('<path d="M%g %gL%g %g" stroke="#fff" stroke-width="%g" stroke-linecap="round"/>' % (x1, y1, x2, y2, 3.4 * s))
            hx, hy = (x2, y2)
            if dx:
                g.append('<path d="M%g %gl%g %gl0 %gz" fill="#fff"/>' % (hx + dx * 6 * s, hy, -dx * 8 * s, -5 * s, 10 * s))
            else:
                g.append('<path d="M%g %gl%g %gl%g 0z" fill="#fff"/>' % (hx, hy + dy * 5 * s, -6 * s, -dy * 6 * s, 12 * s))
        for i in range(3):
            g.append('<circle cx="%g" cy="%g" r="%g" fill="#9dff8a"/>' % (x + rw - 18 * s + i * 7 * s, y + bh * .62, 2.3 * s))
        if name:
            g.append(t(x, y + bh + rh + 22 * s, name, 20 * s, INK, 900))
        g.append("</g>")
        self.front.append("".join(g))

    def switch(self, x, y, name, p=None):
        g = ['<g%s>' % ph(p)]
        g.append('<path d="M%g %g l30 -22 h96 l-30 22 z" fill="#d7f1ea" stroke="#1d5e53" stroke-width="2"/>' % (x - 63, y - 4))
        g.append('<rect x="%g" y="%g" width="96" height="26" fill="url(#%sr)" stroke="#1d5e53" stroke-width="2"/>' % (x - 63, y - 4, self.k))
        g.append('<path d="M%g %g l30 -22 v26 l-30 22z" fill="#1f6f63" stroke="#1d5e53" stroke-width="2"/>' % (x + 33, y - 4))
        for i in range(4):
            g.append('<path d="M%g %gh20" stroke="#fff" stroke-width="3" stroke-linecap="round"/>' % (x - 34 + (i % 2) * 18, y - 18 + i * 3))
        g.append(t(x - 15, y + 46, name, 18, INK, 900))
        g.append("</g>")
        self.front.append("".join(g))

    def cloud(self, x, y, w, h, lines, tone="mint", p=None, size=17):
        """Сеть — мягкая капсула с адресом (непрозрачная: провод уходит под неё)."""
        f, s = CLOUD[tone]
        hh = min(h, len(lines) * size * 1.3 + size * 1.1)
        g = ['<g%s>' % ph(p),
             '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="2.4"/>'
             % (x - w / 2, y - hh / 2, w, hh, min(hh / 2, 22), f, s)]
        y0 = y - (len(lines) - 1) * size * .62 + size * .35
        for i, ln in enumerate(lines):
            g.append(t(x, y0 + i * size * 1.22, ln, size, INK, 800 if i == 0 else 700))
        g.append("</g>")
        self.back.append("".join(g))

    # --------------------------------------------------------------- линии и подписи
    def wire(self, x1, y1, x2, y2, col="#2b3b36", w=4, dash=False, p=None):
        d = ' stroke-dasharray="10 8"' if dash else ""
        self.wires.append('<path d="M%g %gL%g %g" stroke="%s" stroke-width="%g" stroke-linecap="round"%s%s/>'
                         % (x1, y1, x2, y2, col, w, d, ph(p)))

    def label(self, x, y, s, size=15, col=INK, w=800, anchor="middle", p=None, mono=False, only=False):
        a = ph(p, only)
        self.front.append('<g%s>%s</g>' % (a, t(x, y, s, size, col, w, anchor, mono)) if a else t(x, y, s, size, col, w, anchor, mono))

    def pill(self, x, y, s, col=TEAL, p=None, size=15, fill="#ffffff", txtcol=None, only=False, mono=False):
        w = max(54, len(s) * size * .6 + 24)
        self.front.append('<g%s><rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="2.2"/>%s</g>'
                          % (ph(p, only), x - w / 2, y - size * .95, w, size * 1.9, size * .95, fill, col,
                             t(x, y + size * .36, s, size, txtcol or col, 800, mono=mono)))

    def arrow(self, x1, y1, x2, y2, col="b", w=4, p=None, only=False, both=False, flow=False):
        c = {"g": GRN, "b": BLUE, "r": RED, "t": TEAL}[col]
        m = "url(#%sa%s)" % (self.k, col)
        st = ' marker-start="%s"' % m if both else ""
        cls = ' class="flow"' if flow else ""
        self.front.append('<path d="M%g %gL%g %g" stroke="%s" stroke-width="%g" fill="none" marker-end="%s"%s%s%s/>'
                          % (x1, y1, x2, y2, c, w, m, st, cls, ph(p, only)))

    def envelope(self, x, y, p=None, only=False):
        """Пакет обновления — жёлтый «конверт» со следом, как на рисунках pptx."""
        self.front.append('<g%s><path d="M%g %g h46 l-14 22 h-46 z" fill="#f2c200" stroke="#a88600" stroke-width="1.5"/>'
                          '<path d="M%g %gh30M%g %gh22M%g %gh26" stroke="#9aa" stroke-width="2"/></g>'
                          % (ph(p, only), x - 16, y - 11, x - 82, y - 9, x - 76, y - 1, x - 84, y + 7))

    def cross(self, x, y, s=26, p=None):
        self.front.append('<g%s><path d="M%g %gL%g %gM%g %gL%g %g" stroke="%s" stroke-width="6" stroke-linecap="round"/></g>'
                          % (ph(p), x - s, y - s, x + s, y + s, x + s, y - s, x - s, y + s, RED))

    def raw(self, html, front=True):
        (self.front if front else self.back).append(html)

    # --------------------------------------------------------------- таблицы
    def table(self, x, y, cols, rows, widths, p=None, title="", rh=30, size=15, hdr="#dff3ec", border="#1d5e53"):
        """rows: [(cells, kind, ph)] — kind: '' обычная, 'new' красная (новая запись), 'hl' подсветка."""
        W = sum(widths)
        g = ['<g%s>' % ph(p)]
        yy = y
        if title:
            g.append(t(x + W / 2.0, yy - 10, title, size, INK, 800))
        g.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="%s" stroke-width="2"/>' % (x, yy, W, rh, hdr, border))
        cx = x
        for c, wd in zip(cols, widths):
            g.append(t(cx + wd / 2.0, yy + rh * .66, c, size, INK, 800))
            cx += wd
        for r in rows:
            cells, kind, rp = (list(r) + ["", None][len(r) - 1:])[:3]
            yy += rh
            fill = {"hl": "#fff2c2", "g": "#c9f0d6", "o": "#ffe0b3"}.get(kind, "#ffffff")
            g.append('<g%s>' % ph(rp))
            g.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, yy, W, rh, fill, border))
            cx = x
            for c, wd in zip(cells, widths):
                col = RED if kind == "new" else INK
                g.append(t(cx + wd / 2.0, yy + rh * .67, c, size, col, 700 if kind != "new" else 800))
                cx += wd
            g.append("</g>")
        cx = x
        for wd in widths[:-1]:
            cx += wd
            g.append('<path d="M%g %gV%g" stroke="%s" stroke-width="1.6"/>' % (cx, y, yy + rh, border))
        g.append("</g>")
        self.front.append("".join(g))
        return yy + rh


def wrap(svg):
    return '<div class="figwrap dkpanel rppanel">%s</div>' % svg


# ====================================================================== pptx 3 · вектор и расстояние
def vector_hops():
    f = Fig(1200, 330)
    f.cloud(110, 165, 200, 110, ["LAN1"], "blue", size=22)
    f.cloud(1090, 165, 200, 110, ["LAN2"], "violet", size=22)
    f.cloud(420, 160, 270, 96, ["1 Переход (Hop)"], "green", size=20)
    f.cloud(780, 160, 270, 96, ["2 Переход (Hop)"], "red", size=20)
    f.wire(200, 160, 1000, 160, w=5)
    for x, n in ((250, "R1"), (600, "R2"), (950, "R3")):
        f.router(x, 140, n, 1.0)
    f.label(600, 40, "Вектор = Направление", 21)
    f.arrow(300, 58, 900, 58, "b", 6)
    f.label(600, 268, "Расстояние = Переход (Hop)", 21)
    f.arrow(300, 282, 590, 282, "b", 6)
    f.arrow(610, 282, 900, 282, "b", 6)
    f.label(600, 318, "Чем мешьше количество переходов, тем приоритетнее маршрут.", 20, INK, 700)
    return wrap(f.svg())


# ====================================================================== pptx 5 · протокол ↔ таблица
def proto_table():
    f = Fig(1200, 420)
    for x, tone, fill in ((250, "orange", "#ffe3c4"), (950, "violet", "#e9e0fb")):
        f.raw('<rect x="%g" y="20" width="240" height="70" rx="6" fill="#ffe3c4" stroke="#e09a4f" stroke-width="2.4"/>' % (x - 120), False)
        f.label(x, 50, "Протокол", 21)
        f.label(x, 76, "маршрутизации", 21)
        f.raw('<rect x="%g" y="140" width="240" height="70" rx="6" fill="%s" stroke="#8fa6d8" stroke-width="2.4"/>'
              % (x - 120, "#dbe9ff" if x < 600 else fill), False)
        f.label(x, 170, "Таблица", 21)
        f.label(x, 196, "маршрутизации", 21)
        for y1, y2 in ((92, 136), (212, 262)):
            f.arrow(x - 14, y1, x - 14, y2, "b", 7)
            f.arrow(x + 14, y2, x + 14, y1, "b", 7)
    f.arrow(400, 70, 800, 70, "b", 6, both=True)
    f.envelope(640, 28)
    f.label(600, 112, "Обновление", 21)
    f.cloud(110, 320, 210, 90, ["192.168.10.0/24"], "blue", size=19)
    f.cloud(1090, 320, 210, 90, ["192.168.20.0/24"], "violet", size=19)
    f.wire(250, 312, 950, 312, w=5)
    f.router(250, 296, "R1")
    f.router(950, 296, "R2")
    f.label(600, 300, "203.0.113.0/24", 20)
    return wrap(f.svg())
