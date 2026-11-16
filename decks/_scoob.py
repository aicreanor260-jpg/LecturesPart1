# -*- coding: utf-8 -*-
"""Инфографики WAN / WAN-2 в стиле автора «Скуби-Ду»: панели _space.py, перекрашенные под тему, и мультяшные спрайты
(маршрутизатор-цилиндр, облако, ПК, коммутатор, здание, вышка, сервер). Вставка вместо картинки — emit()."""
from _space import page, panel, items, nums, note, grid, stack, icon  # noqa: F401
from _arena import scene, env, show  # noqa: F401
from _sw_lib import slide, sc as _sc, head, grow

OUT, BLU, LBL, CY, OR, LI, PU, RD = "#2a1b4a", "#3a86e0", "#8ec5ff", "#33c3c0", "#ff9f2e", "#b7e04a", "#8b5cf6", "#e5484d"


def emit(title, html, label=""):
    slide("Инфографика · " + (label or title), _sc(head(title, ""), grow("g", '<div class="arwrap sb">%s</div>' % html)))


def scn(svg, w=1000, h=420):
    return scene(w, h, svg)


def scp(svg, headt="", w=1000, h=420, tone="c"):
    return panel(headt, scn(svg, w, h), tone, "sc")


def lbl(x, y, t, size=15, col=OUT, anchor="middle", bold=900):
    return '<text x="%d" y="%d" text-anchor="%s" font-weight="%d" font-size="%d" fill="%s">%s</text>' % (x, y, anchor, bold, size, col, t)


def chip(x, y, t, fill="#fff6dc", size=14, col=OUT):
    w = int(len(t) * size * .58) + 18
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - w // 2, y - size - 2, w, size + 12, fill, OUT)
            + lbl(x, y + 3, t, size, col))


def rt(x, y, name="", r=30, fill=BLU, top=LBL):
    """Маршрутизатор — мультяшный цилиндр со стрелками."""
    g = ('<g transform="translate(%d,%d)"><path d="M%d,0 v14 a%d,%d 0 0,0 %d,0 v-14" fill="%s" stroke="%s" stroke-width="3"/>'
         '<ellipse cx="0" cy="0" rx="%d" ry="%d" fill="%s" stroke="%s" stroke-width="3"/>'
         '<path d="M-14,-3 l8,-5 m-8,5 l8,5 M-14,-3 h10 M14,3 l-8,-5 m8,5 l-8,5 M14,3 h-10" stroke="#fff" stroke-width="2.6" fill="none"/></g>'
         % (x, y, -r, r, r * .42, 2 * r, fill, OUT, r, r * .42, top, OUT))
    return g + (lbl(x, y + r * .42 + 34, name, 15) if name else "")


def swc(x, y, name="", w=110, fill=BLU):
    g = ('<g transform="translate(%d,%d)"><rect x="%d" y="-14" width="%d" height="28" rx="6" fill="%s" stroke="%s" stroke-width="3"/>%s</g>'
         % (x, y, -w // 2, w, fill, OUT, "".join('<rect x="%d" y="-5" width="8" height="8" fill="#fff"/>' % (-w // 2 + 10 + i * 14) for i in range(int((w - 16) / 14)))))
    return g + (lbl(x, y + 34, name, 14) if name else "")


def cloud(x, y, t="", w=170, fill="#e8f4ff"):
    s = w / 170
    return ('<g transform="translate(%d,%d) scale(%.2f)"><path d="M-62,30 h124 a32,32 0 0,0 0,-64 a45,45 0 0,0 -84,-10 a35,35 0 0,0 -40,74 z" fill="%s" stroke="%s" '
            'stroke-width="3.5"/>%s</g>' % (x, y, s, fill, OUT, lbl(0, 8, t, 17) if t else ""))


def pc(x, y, name=""):
    return ('<g transform="translate(%d,%d)"><rect x="-22" y="-30" width="44" height="30" rx="4" fill="%s" stroke="%s" stroke-width="3"/>'
            '<rect x="-16" y="-25" width="32" height="20" fill="#cfe9ff"/><path d="M-8,8 h16 M0,0 v8" stroke="%s" stroke-width="3"/></g>' % (x, y, BLU, OUT, OUT)
            + (lbl(x, y + 30, name, 13) if name else ""))


def bld(x, y, name="", w=70, h=80, fill="#ffd27a"):
    win = "".join('<rect x="%d" y="%d" width="10" height="10" fill="#ffef9e" stroke="%s" stroke-width="1.5"/>' % (x - w // 2 + 10 + (i % 3) * 20, y - h + 12 + (i // 3) * 20, OUT)
                  for i in range(3 * max(1, (h - 20) // 20)))
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" stroke="%s" stroke-width="3"/>' % (x - w // 2, y - h, w, h, fill, OUT) + win
            + (lbl(x, y + 22, name, 14) if name else ""))


def tower(x, y, name=""):
    return ('<path d="M%d,%d l14,-70 l14,70 M%d,%d h20 M%d,%d h12" stroke="%s" stroke-width="3.5" fill="none"/>'
            '<path d="M%d,%d q-10,-10 0,-20 M%d,%d q10,-10 0,-20" stroke="%s" stroke-width="3" fill="none"/>'
            % (x - 14, y, x - 10, y - 25, x - 6, y - 45, OUT, x - 22, y - 62, x + 22, y - 62, OR) + (lbl(x, y + 22, name, 13) if name else ""))


def srv(x, y, name="", n=3):
    g = "".join('<rect x="%d" y="%d" width="54" height="16" rx="3" fill="#3b3f63" stroke="%s" stroke-width="2.5"/><circle cx="%d" cy="%d" r="3" fill="#5dff7a"/>'
                % (x - 27, y - 16 * (k + 1) - 2 * k, OUT, x + 18, y - 16 * k - 2 * k - 8) for k in range(n))
    return g + (lbl(x, y + 20, name, 13) if name else "")


def ln(d, col=OUT, w=4, dash=False, glow=False):
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" %s %s/>' % (
        d, col, w, 'stroke-dasharray="9 7"' if dash else "", 'filter="url(#glw)"' if glow else "")


def L(*xy):
    return "M" + " L".join("%d,%d" % p for p in xy)


def flow(d, col=OR, T=3, n=2, w=5):
    return ln(d, col, w) + "".join(env(d, k * T / n, T * .8, T) for k in range(n))


def tab(head_, rows, tone=CY):
    def cell(c):
        return '<td class="c-%s">%s</td>' % (c[1], c[0]) if isinstance(c, tuple) else "<td>%s</td>" % c
    return ('<table class="sb-tab" style="--t:%s"><tr>%s</tr>%s</table>' % (tone, "".join("<th>%s</th>" % h for h in head_),
                                                                            "".join("<tr>%s</tr>" % "".join(cell(c) for c in r) for r in rows)))


CSS = r"""
.arwrap{position:relative;height:100%;min-height:0;display:flex;flex-direction:column}.arwrap>.ar{flex:1 1 auto;min-height:0}
.sb .sp-pn,.sb .sp-nm{background:#fff6dc;border:3px solid #2a1b4a;border-radius:16px;box-shadow:0 5px 0 #2a1b4a;color:#2a1b4a}
.sb .sp-ph{margin:-12px -16px 8px;padding:6px 14px;background:var(--t);border-bottom:3px solid #2a1b4a;border-radius:13px 13px 0 0;color:#2a1b4a;
 letter-spacing:.01em;text-transform:none;font:900 calc(clamp(14px,1.25vw,22px)*var(--fz,1))/1.15 var(--f);text-align:center}
.sb .sp-pn.sc .sp-ph{margin:-6px -8px 6px}
.sb .sp-it b,.sb .sp-nm b{color:#2a1b4a}.sb .sp-it p,.sb .sp-nm p,.sb .sp-pn>p,.sb .sp-pn li{color:#3c2f5c}
.sb .sp-ic{background:#fff;box-shadow:none;border:2.5px solid #2a1b4a;color:#ff7a00}
.sb .sp-nm i{text-shadow:none;color:#ff7a00;-webkit-text-stroke:1px #2a1b4a}
.sb .sp-note{background:#d7f27a;border:3px solid #2a1b4a;box-shadow:0 5px 0 #2a1b4a;border-radius:16px}
.sb .sp-note b{color:#2a1b4a}.sb .sp-note small{color:#3c2f5c}
.sb .sp-sub{align-self:center;background:#7b3fe4;color:#fff;border:3px solid #ffd43b;border-radius:999px;padding:4px 24px;letter-spacing:.02em;font-weight:900;margin-top:-2px}
.sb .ar-scene{background:#fff6dc;border:3px solid #2a1b4a;box-shadow:0 5px 0 #2a1b4a;border-radius:16px}
.sb .sp-pn.sc .ar-scene{border:0;box-shadow:none}
.sb .sp-chip{color:#2a1b4a;border:2px solid #2a1b4a;background:#ffd27a}
.sb ul.li li::marker{content:"✿ ";color:#ff7a00}
.sb-tab{width:100%;border-collapse:separate;border-spacing:0;border:3px solid #2a1b4a;border-radius:12px;overflow:hidden;font:800 calc(clamp(12px,1vw,17px)*var(--fz,1))/1.25 var(--f)}
.sb-tab th{background:var(--t);color:#2a1b4a;padding:5px 10px;border-bottom:3px solid #2a1b4a}.sb-tab td{background:#fff6dc;color:#2a1b4a;padding:4px 10px;border-top:1.5px solid #e4d3a6}
.sb-tab td.c-y{background:#ffe48a}.sb-tab td.c-r{background:#ffd0d0}.sb-tab td.c-g{background:#dff5b0}
.sb-big{font:900 calc(clamp(20px,2vw,34px)*var(--fz,1))/1.1 var(--f);color:#2a1b4a;text-align:center}
"""


def css():
    import _arena
    import _space
    return _arena.CSS + _space.CSS + CSS


def js():
    import _arena
    return _arena.JS
CSS += r"""
.sb .sp .ar-scene svg{max-height:41vh}
"""
CSS += r"""
.sb .sp-pn:not(.sc) .ar-scene svg{max-height:25vh}
.sb .sp-pn:not(.sc) .ar-scene{border:0;box-shadow:none;background:none;padding:0}
"""
CSS += r"""
.sb .sp-pn.short .ar-scene svg{max-height:27vh}
"""


def tx_wrap(pslide, TX):
    """Обёртка pslide деки: если метка есть в TX — слайд-тезисы, а исходные блоки pptx — в «Текст слайда из лекции»."""
    from _sw_lib import step, card

    def w(label, title, left, right=None, sub="", layout="g2"):
        if label not in TX:
            return pslide(label, title, left, right, sub, layout)
        sub2, html = TX[label]
        src = '<details class="ptsrc"><summary>Текст слайда из лекции</summary>%s</details>' % "".join(left + (right or []))
        from _sw_lib import slide, sc as _sc, head, grow
        slide(label, _sc(head(title, ""), grow("g", '<div class="arwrap sb">%s%s</div>' % (page(sub2 or sub, html), src))))
    return w


CSS += r"""
.arwrap>details.ptsrc{position:absolute;right:0;top:calc(-1 * clamp(40px,4.4vw,70px));z-index:6;max-width:62%;margin:0}
.arwrap>details.ptsrc>summary{display:inline-block;cursor:pointer;list-style:none;font:700 clamp(11px,.9vw,16px)/1 var(--f);padding:5px 12px;border-radius:999px;
 border:2px solid #2a1b4a;color:#2a1b4a;background:#ffd27a}
.arwrap>details.ptsrc>summary::-webkit-details-marker{display:none}
.arwrap>details.ptsrc[open]{background:#fff8e6;border:3px solid #2a1b4a;border-radius:12px;padding:10px;max-height:72vh;overflow:auto;box-shadow:0 10px 30px rgba(0,0,0,.45)}
"""
CSS += r"""
.sb .sp-pn>p,.sb .sp-pn ul.li li,.sb .sp-nm p,.sb .sp-it p{font-size:calc(clamp(14px,1.3vw,25px)*var(--fz,1))!important;line-height:1.38!important}
.sb .sp-nm b,.sb .sp-it b{font-size:calc(clamp(15px,1.4vw,27px)*var(--fz,1))!important}
.sb .sp-ph{font-size:calc(clamp(15px,1.4vw,26px)*var(--fz,1))!important}
.sb .sp-note b{font-size:calc(clamp(14px,1.3vw,24px)*var(--fz,1))!important}
.sb .sp-note small{font-size:calc(clamp(12px,1vw,18px)*var(--fz,1))!important}
.sb-tab{font-size:calc(clamp(13px,1.15vw,22px)*var(--fz,1))!important}
"""
