# -*- coding: utf-8 -*-
"""Инфографики автора в теме «космос» (деки иерархии и др.) — вёрсткой и SVG с анимацией.
Стеклянные панели, иконки в кружках, номера 01–08, светящиеся устройства и импульсы по каналам."""
from _arena import scene, show  # noqa: F401  (scene — общий холст с подгонкой и свечением)

C, G, V, R, GR = "#4cc9ff", "#f5b942", "#a46bff", "#ff5a5a", "#3ddc97"
TONE = {"c": C, "g": G, "v": V, "r": R, "e": GR}

# ------------------------------------------------------------------ иконки (линии, 24×24)
IC = {
    "gear": '<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "warn": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18v.5"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "wifi": '<path d="M2 9c5.5-5 14.5-5 20 0M5 12.5c4-3.5 10-3.5 14 0M8.5 16c2-1.6 5-1.6 7 0"/><circle cx="12" cy="19.5" r="1"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "gauge": '<path d="M3 17a9 9 0 1118 0"/><path d="M12 17l5-6"/>',
    "cube": '<path d="M12 2l9 5v10l-9 5-9-5V7z"/><path d="M3 7l9 5 9-5M12 12v10"/>',
    "layers": '<path d="M12 3l10 5-10 5L2 8z"/><path d="M2 13l10 5 10-5M2 17.5l10 5 10-5"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 018 0v4"/>',
    "link": '<path d="M10 14a5 5 0 007 0l3-3a5 5 0 00-7-7l-1 1M14 10a5 5 0 00-7 0l-3 3a5 5 0 007 7l1-1"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 21c0-4 3-6 7-6s7 2 7 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c3 0 5 2 5 5"/>',
    "cloud": '<path d="M7 18h11a4 4 0 000-8 6 6 0 00-11.5-1.5A4.5 4.5 0 007 18z"/>',
    "pin": '<path d="M12 22s7-7 7-12a7 7 0 10-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "plug": '<path d="M9 2v6M15 2v6M6 8h12v4a6 6 0 01-12 0zM12 18v4"/>',
    "share": '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="5" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8 11l8-5M8 13l8 5"/>',
    "x": '<circle cx="12" cy="12" r="9"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7"/>',
    "ok": '<circle cx="12" cy="12" r="9"/><path d="M7.5 12.5l3 3 6-6"/>',
    "branch": '<path d="M12 22V12M12 12L5 5M12 12l7-7M5 5v4M5 5h4M19 5v4M19 5h-4"/>',
    "plan": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M8 8h3v3H8zM13 13h3v3h-3zM11 9.5h4v3.5"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0012 3z"/>',
    "server": '<rect x="4" y="3" width="16" height="7" rx="1.5"/><rect x="4" y="14" width="16" height="7" rx="1.5"/><path d="M7 6.5h.5M7 17.5h.5"/>',
    "route": '<circle cx="12" cy="12" r="9"/><path d="M12 5v14M5 12h14M9 8l3-3 3 3M9 16l3 3 3-3"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "swap": '<path d="M4 8h14l-3-3M20 16H6l3 3"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
    "arrow": '<path d="M5 12h13M13 6l6 6-6 6"/>',
}


def icon(name, tone="c", size=46):
    return ('<span class="sp-ic" style="--t:%s;width:%dpx;height:%dpx"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">%s</svg></span>' % (TONE.get(tone, tone), size, size, IC[name]))


# ------------------------------------------------------------------ HTML-блоки
def panel(head, inner, tone="c", cls=""):
    h = '<h4 class="sp-ph">%s</h4>' % head if head else ""
    return '<div class="sp-pn step %s" style="--t:%s">%s%s</div>' % (cls, TONE.get(tone, tone), h, inner)


def items(rows, tone="c"):
    """rows — [(иконка, заголовок, текст)]"""
    out = []
    for r in rows:
        ic, t, d = (tuple(r) + ("", ""))[:3]
        out.append('<div class="sp-it">%s<div>%s%s</div></div>' % (icon(ic, tone, 40), "<b>%s</b>" % t if t else "", "<p>%s</p>" % d if d else ""))
    return '<div class="sp-its">%s</div>' % "".join(out)


def nums(rows, cols=2, tone="c"):
    """rows — [(заголовок, текст)] → карточки 01, 02 …"""
    out = "".join('<div class="sp-nm step" style="--t:%s"><i>%02d</i><div><b>%s</b><p>%s</p></div></div>' % (TONE.get(tone, tone), k, t, d)
                  for k, (t, d) in enumerate(rows, 1))
    return '<div class="sp-nms" style="grid-template-columns:repeat(%d,1fr)">%s</div>' % (cols, out)


def note(text, ic="info", tone="g", small=""):
    return ('<div class="sp-note step" style="--t:%s">%s<div><b>%s</b>%s</div></div>'
            % (TONE.get(tone, tone), icon(ic, tone, 40), text, "<small>%s</small>" % small if small else ""))


def grid(cols, *kids, rows=""):
    return '<div class="sp-grid" style="grid-template-columns:%s;%s">%s</div>' % (cols, "grid-template-rows:%s" % rows if rows else "", "".join(kids))


def stack(*kids):
    return '<div class="sp-col">%s</div>' % "".join(kids)


def page(sub, body, foot=""):
    return '<div class="ar sp">%s%s%s</div>' % ('<div class="sp-sub">%s</div>' % sub if sub else "", body, foot)


def sc(svg_inner, w=1000, h=420):
    return scene(w, h, svg_inner)


# ------------------------------------------------------------------ спрайты SVG
def rk(x, y, name="", w=150, h=34, tone=C, label="below", stackn=1):
    """Коммутатор-стойка: тёмный металл, порты, голубая полоса; label below|above|right|left|none."""
    g = []
    for k in range(stackn):
        yy = y - h // 2 + k * (h + 4)
        g.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="#141d2e" stroke="#8fa3c2" stroke-width="1.6"/>' % (x - w // 2, yy, w, h))
        n = max(int((w - 30) / 9), 4)
        g.append("".join('<rect x="%.1f" y="%d" width="6" height="5" fill="#04070d" stroke="#53627a" stroke-width=".6"/>' % (x - w / 2 + 8 + i * 9, yy + 8)
                         for i in range(n)))
        g.append("".join('<rect x="%.1f" y="%d" width="6" height="5" fill="#04070d" stroke="#53627a" stroke-width=".6"/>' % (x - w / 2 + 8 + i * 9, yy + 16)
                         for i in range(n)))
        g.append('<rect x="%d" y="%d" width="%d" height="2.5" fill="%s"><animate attributeName="opacity" values="1;.35;1" dur="2.2s" '
                 'repeatCount="indefinite"/></rect>' % (x - w // 2 + 4, yy + h - 6, w - 8, tone))
    if name and label != "none":
        lx, ly = {"below": (x, y + h // 2 + (stackn - 1) * (h + 4) + 18), "above": (x, y - h // 2 - 9), "right": (x + w // 2 + 8, y + 5),
                  "left": (x - w // 2 - 8, y + 5)}[label]
        anc = {"right": "start", "left": "end"}.get(label, "middle")
        g.append('<text x="%d" y="%d" text-anchor="%s" fill="#eaf6ff" font-weight="800" font-size="15">%s</text>' % (lx, ly, anc, name))
    return "".join(g)


def router(x, y, name="", tone=C, r=30):
    return ('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#16243c" stroke="%s" stroke-width="2"/>'
            '<rect x="%d" y="%d" width="%d" height="12" fill="#16243c"/><ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="#1e3354" stroke="%s" stroke-width="2"/>'
            '<path d="M%d,%d h14 m-5,-4 l5,4 l-5,4 M%d,%d h-14 m5,-4 l-5,4 l5,4" stroke="%s" stroke-width="2" fill="none"/>'
            '<text x="%d" y="%d" text-anchor="middle" fill="#eaf6ff" font-weight="800" font-size="15">%s</text>'
            % (x, y + 8, r, r * .42, tone, x - r, y - 4, 2 * r, x, y - 4, r, r * .42, tone, x + 2, y - 4, x - 2, y - 4, tone, x, y + r * .42 + 26, name))


def cloud(x, y, text="Интернет", w=130, tone=C):
    s = w / 130
    return ('<g transform="translate(%d,%d) scale(%.2f)"><path d="M-45,22 h92 a24,24 0 0,0 0,-48 a34,34 0 0,0 -62,-8 a26,26 0 0,0 -30,56 z" '
            'fill="#13253f" stroke="%s" stroke-width="2.4" filter="url(#glw)"/><text x="0" y="7" text-anchor="middle" fill="#eaf6ff" '
            'font-weight="800" font-size="15">%s</text></g>' % (x, y, s, tone, text))


def dev(x, y, kind, name="", tone=C):
    """Оконечные устройства: pc, laptop, printer, phone, cam, ap, tablet, server."""
    p = {
        "pc": '<rect x="-20" y="-24" width="40" height="28" rx="3"/><path d="M-6,8 h12 M0,4 v4"/>',
        "laptop": '<rect x="-16" y="-20" width="32" height="20" rx="2"/><path d="M-22,4 h44 l-4,-4 h-36 z"/>',
        "printer": '<rect x="-18" y="-10" width="36" height="16" rx="3"/><path d="M-11,-10 v-10 h22 v10 M-11,6 v8 h22 v-8"/>',
        "phone": '<rect x="-16" y="-14" width="32" height="24" rx="4"/><path d="M-12,-14 q12,-10 24,0"/><path d="M-6,-6 h4 M2,-6 h4 M-6,0 h4 M2,0 h4"/>',
        "cam": '<rect x="-20" y="-12" width="30" height="16" rx="4"/><path d="M10,-6 l10,-6 v16 l-10,-6 M-12,4 v8"/>',
        "ap": '<ellipse cx="0" cy="0" rx="20" ry="8"/><path d="M-9,-14 q9,-8 18,0 M-5,-20 q5,-5 10,0"/>',
        "tablet": '<rect x="-12" y="-18" width="24" height="34" rx="3"/><path d="M-2,12 h4"/>',
        "server": '<rect x="-22" y="-20" width="44" height="12" rx="2"/><rect x="-22" y="-4" width="44" height="12" rx="2"/><path d="M-16,-14 h3 M-16,2 h3"/>',
    }[kind]
    lab = '<text x="0" y="30" text-anchor="middle" fill="#cfe6ff" font-weight="700" font-size="12.5">%s</text>' % name if name else ""
    return ('<g transform="translate(%d,%d)" fill="#0f1a2c" stroke="%s" stroke-width="2" stroke-linejoin="round" filter="url(#glw)">%s</g>'
            '<g transform="translate(%d,%d)">%s</g>' % (x, y, tone, p, x, y, lab))


def link(d, tone=C, w=3, dash=False, op=1):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" opacity="%.2f" filter="url(#glw)" %s/>'
            % (d, TONE.get(tone, tone), w, op, 'stroke-dasharray="7 6"' if dash else ""))


def pulse(d, t0, dur, T, tone=C, r=5):
    s, e = t0 / T, min((t0 + dur) / T, 1)
    col = TONE.get(tone, tone)
    return ('<circle r="%d" fill="%s" opacity="0" filter="url(#glw)"><animate attributeName="opacity" calcMode="discrete" values="0;1;0" '
            'keyTimes="0;%.4f;%.4f" dur="%ss" repeatCount="indefinite"/><animateMotion dur="%ss" repeatCount="indefinite" calcMode="linear" '
            'keyPoints="0;0;1;1" keyTimes="0;%.4f;%.4f;1" path="%s"/></circle>' % (r, col, s, e, T, T, s, e, d))


def flow(d, tone=C, T=2.4, n=3, w=3, dash=False):
    """Канал со светящимися импульсами, бегущими по нему без конца."""
    return link(d, tone, w, dash) + "".join(pulse(d, k * T / n, T * 0.9, T, tone) for k in range(n))


def tag(x, y, text, tone=C, size=13):
    w = int(len(text) * size * 0.56) + 16
    col = TONE.get(tone, tone)
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="#0c1628" stroke="%s" stroke-width="1.4"/>'
            '<text x="%d" y="%d" text-anchor="middle" fill="#eaf6ff" font-weight="700" font-size="%d">%s</text>'
            % (x - w // 2, y - size, w, size + 10, (size + 10) // 2, col, x, y + 2, size, text))


def box(x, y, w, h, label="", tone=C, dash=True):
    col = TONE.get(tone, tone)
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" fill-opacity=".06" stroke="%s" stroke-width="1.8" %s/>'
            '%s' % (x, y, w, h, col, col, 'stroke-dasharray="7 5"' if dash else "",
                    '<text x="%d" y="%d" text-anchor="middle" fill="#eaf6ff" font-weight="800" font-size="15">%s</text>' % (x + w // 2, y + 20, label) if label else ""))


def lagring(x, y, rx=22, ry=8, tone=C, label="LAG"):
    return ('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="2.2"/>' % (x, y, rx, ry, TONE.get(tone, tone))
            + ('<text x="%d" y="%d" text-anchor="middle" fill="#eaf6ff" font-size="12" font-weight="800">%s</text>' % (x, y - ry - 4, label) if label else ""))


def xm(x, y, s=10, T=None, t0=0):
    m = ('<circle cx="%d" cy="%d" r="%d" fill="#2a0d12" stroke="%s" stroke-width="2.4"/><path d="M%d,%d l%d,%d m0,-%d l-%d,%d" stroke="%s" '
         'stroke-width="2.6"/>' % (x, y, s + 3, R, x - s // 2, y - s // 2, s, s, s, s, s, R))
    return show(t0, T, None, m) if T else m


CSS = r"""
.sp{gap:calc(9px*var(--fz,1))}
.sp-sub{color:#bfe3ff;font:600 calc(clamp(12px,1.05vw,18px)*var(--fz,1))/1.2 var(--f);letter-spacing:.22em;text-transform:none;margin-top:-4px;opacity:.9}
.sp-grid{display:grid;gap:12px;flex:1 1 auto}
.sp-col{display:flex;flex-direction:column;gap:12px}
.sp-pn{background:linear-gradient(180deg,rgba(18,32,58,.78),rgba(8,14,28,.78));border:1.5px solid color-mix(in srgb,var(--t) 55%,transparent);
 border-radius:14px;padding:12px 16px;box-shadow:0 0 18px color-mix(in srgb,var(--t) 22%,transparent),inset 0 0 22px rgba(0,0,0,.35);min-height:0}
.sp-ph{margin:0 0 8px;color:#eaf6ff;font:800 calc(clamp(12px,1vw,17px)*var(--fz,1))/1.2 var(--f);letter-spacing:.2em;text-transform:uppercase}
.sp-pn.sc{padding:6px 8px;display:flex;flex-direction:column}.sp-pn.sc .ar-scene{background:none;border:0;box-shadow:none;flex:1}
.sp-ic{flex:0 0 auto;display:inline-grid;place-items:center;border-radius:50%;color:var(--t);border:1.6px solid var(--t);
 box-shadow:0 0 12px color-mix(in srgb,var(--t) 45%,transparent);background:rgba(6,12,24,.8)}
.sp-ic svg{width:58%;height:58%}
.sp-its{display:flex;flex-direction:column;gap:9px}
.sp-it{display:flex;gap:12px;align-items:center}
.sp-it b{display:block;color:#eaf6ff;font:800 calc(clamp(12.5px,1.05vw,18px)*var(--fz,1))/1.2 var(--f)}
.sp-it p,.sp-nm p,.sp-pn>p{margin:2px 0 0!important;color:#b9cde6;font:500 calc(clamp(11.5px,.95vw,16px)*var(--fz,1))/1.3 var(--f)}
.sp-nms{display:grid;gap:10px}
.sp-nm{display:flex;gap:12px;align-items:flex-start;background:linear-gradient(180deg,rgba(18,32,58,.78),rgba(8,14,28,.78));
 border:1.5px solid color-mix(in srgb,var(--t) 50%,transparent);border-radius:12px;padding:10px 14px}
.sp-nm i{font:800 calc(clamp(22px,2.1vw,38px)*var(--fz,1))/1 var(--f);color:var(--t);font-style:normal;text-shadow:0 0 14px var(--t)}
.sp-nm b{display:block;color:#eaf6ff;font:800 calc(clamp(12.5px,1.05vw,18px)*var(--fz,1))/1.2 var(--f)}
.sp-note{display:flex;gap:14px;align-items:center;border:1.6px solid var(--t);border-radius:14px;padding:9px 16px;
 background:linear-gradient(90deg,rgba(40,28,4,.55),rgba(8,14,28,.8));box-shadow:0 0 20px color-mix(in srgb,var(--t) 30%,transparent)}
.sp-note b{display:block;color:#ffe2a3;font:800 calc(clamp(13px,1.15vw,20px)*var(--fz,1))/1.25 var(--f);letter-spacing:.04em}
.sp-note small{display:block;color:#b9cde6;font:500 calc(clamp(11px,.85vw,14px)*var(--fz,1))/1.3 var(--f);margin-top:2px}
.sp .ar-scene{background:rgba(6,14,30,.35);border:1.5px solid rgba(76,201,255,.35);box-shadow:0 0 18px rgba(76,201,255,.12)}
.sp .ar-scene{flex:1 1 auto;min-height:0}.sp .ar-scene svg{height:auto;max-height:46vh}
.sp-big{font:800 calc(clamp(26px,2.6vw,46px)*var(--fz,1))/1 var(--f);color:var(--t,#f5b942);text-shadow:0 0 16px currentColor}
.sp-chip{display:inline-block;margin:3px 6px 0 0;padding:3px 10px;border:1px solid var(--t,#4cc9ff);border-radius:999px;color:#eaf6ff;
 font:700 calc(clamp(11px,.85vw,14px)*var(--fz,1))/1.3 var(--f)}
"""
CSS += r"""
.sp-pn.tight .sp-nm{padding:5px 12px}.sp-pn.tight .sp-nms{gap:6px}
"""
