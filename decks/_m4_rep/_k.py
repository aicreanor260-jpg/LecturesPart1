# -*- coding: utf-8 -*-
"""Общие кирпичики вёрстки инфографик 2.4 (префикс классов задаёт файл)."""
GOLD = "#f0c75e"; TEAL = "#3fd6b0"


def css(p):
    return """<style>
.%(p)s-pn{position:absolute;box-sizing:border-box;border:1.6px solid rgba(240,199,94,.72);border-radius:22px;
 background:linear-gradient(160deg,rgba(14,62,50,.62),rgba(6,32,26,.74));box-shadow:0 0 16px rgba(240,199,94,.28),inset 0 0 22px rgba(240,199,94,.10)}
.%(p)s-pn.b{border-color:rgba(63,214,255,.7);box-shadow:0 0 16px rgba(63,214,255,.3),inset 0 0 20px rgba(63,214,255,.12);background:linear-gradient(160deg,rgba(20,90,110,.55),rgba(8,40,52,.72))}
.%(p)s-g{font-variant-numeric:lining-nums;position:absolute;font-family:"Playfair Display",serif;font-weight:800;text-transform:uppercase;white-space:nowrap;text-align:center;
 background:linear-gradient(180deg,#fff0b8 0%%,#f0c75e 55%%,#b98a2c 100%%);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 2px 6px rgba(0,0,0,.6))}
.%(p)s-s{font-variant-numeric:lining-nums;position:absolute;font-family:"Playfair Display",serif;font-weight:600;color:#f6ebc8;text-align:center;white-space:nowrap;text-shadow:0 2px 5px rgba(0,0,0,.7)}
.%(p)s-t{position:absolute;font-family:"Golos Text",sans-serif;font-weight:500;color:#ecf5ee;text-align:center;white-space:nowrap;text-shadow:0 1px 4px rgba(0,0,0,.7)}
.%(p)s-m{position:absolute;font-family:"JetBrains Mono",monospace;color:#e7efe2;text-align:center;white-space:nowrap}
.%(p)s-hl{position:absolute;box-sizing:border-box;border:2px solid #f0c75e;border-radius:6px;background:linear-gradient(90deg,rgba(240,199,94,.28),rgba(240,199,94,.12));box-shadow:0 0 14px rgba(240,199,94,.7)}
.%(p)s-hl.b{border-color:#3fe6ff;background:rgba(63,230,255,.22);box-shadow:0 0 14px rgba(63,230,255,.7)}
.%(p)s-ln{position:absolute;background:rgba(240,199,94,.35)}
.%(p)s-svg{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none;overflow:visible}
.%(p)s-svg .fl{fill:none;stroke-linecap:round;stroke-dasharray:9 7;animation:%(p)sd 1.4s linear infinite}
@keyframes %(p)sd{to{stroke-dashoffset:-32}}
</style>""" % {"p": p}


def box(p, x, y, w, h, cls="", st=""):
    return '<div class="%s-pn %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s"></div>' % (p, cls, x, y, w, h, st)


def tx(p, kind, x, y, text, size, w=None, st="", center=True):
    """Текст; x — центр (center=True) или левый край. y — верх строки."""
    wd = w or 700
    left = x - wd / 2 if center else x
    al = "" if center else "text-align:left;"
    return ('<div class="%s-%s" style="left:%dpx;top:%dpx;width:%dpx;font-size:%dpx;line-height:1.15;%s%s">%s</div>'
            % (p, kind, left, y, wd, size, al, st, text))


def grid(p, x, y, cols, rows, rowh, size=17, hdr=None, hdrh=None, hl=(), hlcls="", mono=False, lines=True, aligns=None):
    """Таблица абсолютными ячейками. cols — границы по x (len=n+1, абсолют), rows — строки (y — верх первой)."""
    out = []
    cls = "m" if mono else "t"
    yy = y
    allrows = []
    if hdr:
        allrows.append((hdr, hdrh or rowh, True))
    for r in rows:
        allrows.append((r, rowh, False))
    ri = 0
    for r, h, ish in allrows:
        idx = None if ish else ri
        if not ish:
            ri += 1
        if idx in hl:
            out.append('<div class="%s-hl %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>' % (p, hlcls, cols[0], yy + 1, cols[-1] - cols[0], h - 2))
        for i, c in enumerate(r):
            w = cols[i + 1] - cols[i]
            fs = size
            out.append('<div class="%s-%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;line-height:%dpx;font-size:%dpx;%s">%s</div>'
                       % (p, cls, cols[i], yy, w, h, h, fs, ("font-weight:600;color:#f6ebc8;" if ish else ""), c))
        if lines:
            out.append('<div class="%s-ln" style="left:%dpx;top:%dpx;width:%dpx;height:1px"></div>' % (p, cols[0], yy + h, cols[-1] - cols[0]))
        yy += h
    if lines:
        for c in cols:
            out.append('<div class="%s-ln" style="left:%dpx;top:%dpx;width:1px;height:%dpx"></div>' % (p, c, y, yy - y))
    return "".join(out)


def step(*parts):
    return '<div class="step">' + "".join(parts) + "</div>"


def svg(p, body, defs=True):
    d = ('<defs><filter id="%sgl" x="-20%%" y="-20%%" width="140%%" height="140%%"><feGaussianBlur stdDeviation="3" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         '<marker id="%sag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#f0c75e"/></marker>'
         '<marker id="%sab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#3fd6b0"/></marker>'
         '<marker id="%sas" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#c9d1cf"/></marker>'
         '</defs>') % (p, p, p, p)
    return '<svg class="%s-svg" viewBox="0 0 1672 941">%s%s</svg>' % (p, d, body)


def path(p, d, col="g", w=3.2, both=False, dash=False):
    c = {"g": "#f0c75e", "b": "#3fd6b0", "s": "#c9d1cf", "r": "#ff6b5e"}[col]
    m = {"g": "ag", "b": "ab", "s": "as", "r": "ag"}[col]
    ms = ' marker-end="url(#%s%s)"' % (p, m)
    if both:
        ms += ' marker-start="url(#%s%s)"' % (p, m)
    cl = ' class="fl"' if dash else ""
    return '<path%s d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" filter="url(#%sgl)"%s/>' % (cl, d, c, w, p, ms)
