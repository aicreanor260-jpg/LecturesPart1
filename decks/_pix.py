# -*- coding: utf-8 -*-
"""Инфографики STP в пиксельном стиле автора: панели _space.py, перекрашенные под тему th-stp, и свои спрайты
(изометрические коммутаторы, ПК, хаб, значки ролей портов, типовая топология SW-1…SW-5)."""
from _space import page, panel, items, nums, note, grid, stack, icon  # noqa: F401
from _arena import scene, env, show  # noqa: F401

TE, YE, RE, GN, BL, DK = "#1fa595", "#f2b62c", "#e5484d", "#2f9e44", "#2f6fd6", "#173a5e"


def sc(svg, w=1000, h=460):
    return scene(w, h, svg)


def scp(svg, head="", w=1000, h=460):
    return panel(head, sc(svg, w, h), "c", "sc")


def psw(x, y, name="", crown=False, gold=False, w=120, label="below", dim=False):
    top, front = ("#ffd75e", "#e0a91f") if gold else ("#5aa7ff", "#2a6fd0")
    if dim:
        top, front = "#9fb7d6", "#6d87ab"
    h2 = w // 2
    g = ['<g transform="translate(%d,%d)">' % (x, y),
         '<polygon points="%d,-8 %d,-30 %d,-30 %d,-8" fill="%s" stroke="#173a5e" stroke-width="2.4" stroke-linejoin="round"/>' % (-h2, -h2 + 24, h2 - 24, h2, top),
         '<rect x="%d" y="-8" width="%d" height="30" rx="4" fill="%s" stroke="#173a5e" stroke-width="2.4"/>' % (-h2, w, front),
         '<path d="M-14,-22 h22 m-5,-4 l5,4 l-5,4 M14,-15 h-22 m5,-4 l-5,4 l5,4" stroke="#fff" stroke-width="2.2" fill="none"/>']
    g += ['<rect x="%d" y="0" width="9" height="8" fill="#0d2238"/><circle cx="%d" cy="15" r="2" fill="#5dff7a"><animate attributeName="opacity" '
          'values="1;.3;1" dur="%.1fs" repeatCount="indefinite"/></circle>' % (-h2 + 12 + i * 15, -h2 + 16 + i * 15, .7 + i % 3 * .3) for i in range(int((w - 20) / 15))]
    if crown:
        g.append('<path d="M-16,-36 l5,-14 l11,9 l11,-9 l5,14 z" fill="#ffd43b" stroke="#a07415" stroke-width="2"/>')
    if name and label != "none":
        ly = 40 if label == "below" else -44
        g.append('<rect x="-34" y="%d" width="68" height="22" rx="5" fill="#173a5e"/><text x="0" y="%d" text-anchor="middle" fill="#fff" '
                 'font-weight="900" font-size="15">%s</text>' % (ly, ly + 16, name))
    g.append("</g>")
    return "".join(g)


def ppc(x, y, name=""):
    g = ('<g transform="translate(%d,%d)"><rect x="-24" y="-38" width="48" height="34" rx="3" fill="#2a6fd0" stroke="#173a5e" stroke-width="2.4"/>'
         '<rect x="-19" y="-33" width="38" height="24" fill="#9fdcff"/><rect x="-6" y="-4" width="12" height="7" fill="#173a5e"/>'
         '<rect x="-20" y="4" width="40" height="7" rx="2" fill="#173a5e"/>' % (x, y))
    if name:
        g += '<rect x="-30" y="16" width="60" height="22" rx="5" fill="#173a5e"/><text x="0" y="32" text-anchor="middle" fill="#fff" font-weight="900" font-size="14">%s</text>' % name
    return g + "</g>"


def hub(x, y):
    return psw(x, y, "HUB", w=100)


def badge(x, y, role):
    col = {"R": GN, "D": GN, "RP": GN, "DP": BL, "ND": RE, "Alt": RE, "Bck": RE, "Ds": "#111", "BLOCK": RE, "?": "#f08c00"}[role]
    r = 13 if len(role) <= 2 else 17
    return ('<circle cx="%d" cy="%d" r="%d" fill="#fff" stroke="%s" stroke-width="3"/><text x="%d" y="%d" text-anchor="middle" font-weight="900" '
            'font-size="%d" fill="%s">%s</text>' % (x, y, r, col, x, y + 5, 13 if len(role) <= 2 else 11, col, role))


def ln(d, col="#5d6f80", w=5, dash=False, glow=False):
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" %s %s/>' % (
        d, col, w, 'stroke-dasharray="10 8"' if dash else "", 'filter="url(#glw)"' if glow else "")


def lbl(x, y, t, size=14, col="#173a5e", anchor="middle", bold=900):
    return '<text x="%d" y="%d" text-anchor="%s" font-weight="%d" font-size="%d" fill="%s">%s</text>' % (x, y, anchor, bold, size, col, t)


def chip(x, y, t, fill="#fff", stroke=TE, col="#173a5e", size=14):
    w = int(len(t) * size * .58) + 16
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="2"/>' % (x - w // 2, y - size, w, size + 10, fill, stroke)
            + lbl(x, y + 2, t, size, col))


def xx(x, y, s=11, T=None, t0=0):
    m = '<path d="M%d,%d l%d,%d m0,-%d l-%d,%d" stroke="#e5484d" stroke-width="6" stroke-linecap="round"/>' % (x - s, y - s, 2 * s, 2 * s, 2 * s, 2 * s, 2 * s)
    return show(t0, T, None, m) if T else m


def mtab(x, y, title, rows, w=270, T=6, hdr=("MAC-адрес", "Порт")):
    """Таблица в пиксельном стиле: rows — [(c1, c2, t_on|None, выделить)]"""
    R = 28
    g = ['<g transform="translate(%d,%d)"><rect width="%d" height="%d" rx="6" fill="#fffbea" stroke="%s" stroke-width="3"/>' % (x, y, w, 64 + R * max(len(rows), 1), TE),
         '<rect x="3" y="3" width="%d" height="28" fill="%s"/>' % (w - 6, TE) + lbl(w // 2, 23, title, 16, "#fff"),
         lbl(int(w * .32), 50, hdr[0], 13, "#1b5e57", bold=800) + lbl(int(w * .8), 50, hdr[1], 13, "#1b5e57", bold=800)]
    for k, (a, b, t, hl) in enumerate(rows):
        yy = 60 + k * R
        cell = ('<rect x="6" y="%d" width="%d" height="%d" fill="%s"/>' % (yy, w - 12, R - 3, "#ffe89a" if hl else "#eaf8f5")
                + lbl(int(w * .32), yy + 18, a, 13.5, "#173a5e", bold=800) + lbl(int(w * .8), yy + 18, b, 14, "#173a5e"))
        g.append(show(t, T, None, cell) if t is not None else cell)
    return "".join(g) + "</g>"


# ---------------------------------------------------------------- типовая топология
P = {"SW-2": (230, 110), "SW-3": (640, 110), "SW-1": (230, 330), "SW-4": (640, 330), "PC-A": (70, 370), "PC-B": (850, 100), "SW-5": (870, 330)}
PORT = {  # точки подключения кабелей (по сторонам коммутаторов)
    "SW-2.r": (290, 115), "SW-2.b": (230, 135), "SW-3.l": (580, 115), "SW-3.b": (640, 135), "SW-3.r": (700, 112), "SW-3.br": (690, 132),
    "SW-1.t": (230, 302), "SW-1.r": (290, 335), "SW-1.l": (170, 338), "SW-4.l": (580, 335), "SW-4.t": (640, 302), "SW-4.r": (700, 335),
    "SW-5.l": (810, 338), "SW-5.t": (860, 302), "PC-A": (95, 360), "PC-B": (825, 95)}
LINKS = {"12": ("SW-2.b", "SW-1.t"), "23": ("SW-2.r", "SW-3.l"), "34": ("SW-3.b", "SW-4.t"), "14": ("SW-1.r", "SW-4.l"), "A1": ("PC-A", "SW-1.l"),
         "3B": ("SW-3.r", "PC-B"), "45": ("SW-4.r", "SW-5.l"), "35": ("SW-3.br", "SW-5.t")}


def path(*pts_):
    return "M" + " L".join("%d,%d" % (PORT.get(p) or P[p]) for p in pts_)


def square(sw5=False, root=None, links=None, ports=None, roles=None, flows=(), T=6, extra="", dim=()):
    """links — {ключ: цвет|('r',dash)}; ports — {(x,y): подпись}; roles — {(x,y): 'R'|'D'…}; flows — [(path, t0, d)]"""
    links = links or {}
    g = []
    keys = ["12", "23", "34", "14", "A1", "3B"] + (["45", "35"] if sw5 else [])
    for k in keys:
        a, b = LINKS[k]
        st = links.get(k, "#5d6f80")
        col, dash = (st, False) if isinstance(st, str) else st
        g.append(ln(path(a, b), col, 6, dash))
    for nm in ("SW-2", "SW-3", "SW-1", "SW-4") + (("SW-5",) if sw5 else ()):
        g.append(psw(*P[nm], name=nm, crown=(nm == root), gold=(nm == root), dim=nm in dim))
    g += [ppc(*P["PC-A"], name="PC-A"), ppc(*P["PC-B"], name="PC-B")]
    for (x, y), t in (ports or {}).items():
        g.append(lbl(x, y, t, 13, "#173a5e", bold=800))
    for (x, y), r in (roles or {}).items():
        g.append(badge(x, y, r))
    for p_, t0, d in flows:
        g.append(env(p_, t0, d, T))
    return "".join(g) + extra


# стандартные подписи портов из примера pptx (Gi-порты)
GI = {(310, 98): "Gi0/1", (560, 98): "Gi0/1", (712, 98): "Gi0/3", (252, 160): "Gi0/2", (662, 160): "Gi0/2", (252, 290): "Gi0/2",
      (310, 358): "Gi0/3", (560, 358): "Gi0/1", (150, 330): "Gi0/1", (662, 290): "Gi0/2"}

CSS = r"""
.th-stp .sp-pn,.th-stp .sp-nm{background:#fffbea;border:3px solid #1fa595;box-shadow:0 4px 0 #0e6e63,0 6px 14px rgba(0,0,0,.18);border-radius:10px}
.th-stp .sp-ph{color:#173a5e;letter-spacing:.02em;text-transform:none;font-size:calc(clamp(14px,1.2vw,21px)*var(--fz,1));display:flex;align-items:center;gap:8px}
.th-stp .sp-ph::before{content:"";flex:0 0 auto;width:1.05em;height:1.05em;border-radius:50%;border:2.5px solid #222;
 background:linear-gradient(#e5484d 0 46%,#222 46% 56%,#fff 56%);box-shadow:inset 0 0 0 .18em transparent}
.th-stp .sp-it b,.th-stp .sp-nm b{color:#173a5e}.th-stp .sp-it p,.th-stp .sp-nm p,.th-stp .sp-pn>p,.th-stp .sp-pn li{color:#33485c}
.th-stp .sp-ic{background:#e6f7f4;box-shadow:none}
.th-stp .sp-nm i{text-shadow:none;color:#1fa595}
.th-stp .sp-note{background:#fff4c7;border:3px solid #f2b62c;box-shadow:0 4px 0 #b9851a}
.th-stp .sp-note b{color:#173a5e}.th-stp .sp-note small{color:#4b5d6e}
.th-stp .sp-sub{align-self:center;background:#cff3ec;color:#14524b;border:3px solid #1fa595;border-radius:10px;padding:4px 22px;letter-spacing:.02em;
 font-weight:900;margin-top:0}
.th-stp .sp .ar-scene{background:#fffbea;border:3px solid #1fa595;box-shadow:0 4px 0 #0e6e63}
.th-stp .sp-pn.sc .ar-scene{border:0;box-shadow:none}
.th-stp .sp-chip{color:#173a5e;border-color:#1fa595;background:#e6f7f4}
.px-tab{width:100%;border-collapse:collapse;font:700 calc(clamp(12px,1vw,17px)*var(--fz,1))/1.25 var(--f)}
.px-tab th{background:#1fa595;color:#fff;padding:5px 9px;text-align:left}.px-tab td{background:#eaf8f5;color:#173a5e;padding:4px 9px;border-top:2px solid #fffbea}
.px-tab td.c-y{background:#ffe89a}.px-tab td.c-r{background:#ffd9d9;color:#a01818}.px-tab td.c-g{background:#d8f5d0;color:#1d6e1d}
.px-big{font:900 calc(clamp(20px,2vw,34px)*var(--fz,1))/1.1 var(--f);color:#173a5e;text-align:center}
.px-big em{font-style:normal;color:#e5484d}.px-big b{color:#2f9e44}
"""


def tab(head, rows):
    def cell(c):
        if isinstance(c, tuple):
            return '<td class="c-%s">%s</td>' % (c[1], c[0])
        return "<td>%s</td>" % c
    return '<table class="px-tab"><tr>%s</tr>%s</table>' % ("".join("<th>%s</th>" % h for h in head), "".join("<tr>%s</tr>" % "".join(cell(c) for c in r) for r in rows))
