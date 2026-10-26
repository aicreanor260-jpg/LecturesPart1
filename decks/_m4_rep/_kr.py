# -*- coding: utf-8 -*-
"""Общие мелочи для вёрсток i_subnets/i_based/i_routing/i_decision/i_table_a (префикс p — в именах классов)."""

def css(p):
    return """<style>
.%(p)s-pn{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(14,58,44,.78),rgba(6,32,24,.8));
 border:2px solid rgba(240,199,94,.78);border-radius:16px;box-shadow:0 0 20px rgba(240,199,94,.28),inset 0 0 26px rgba(240,199,94,.10)}
.%(p)s-g{position:absolute;font-family:"Playfair Display",serif;font-weight:800;
 background:linear-gradient(180deg,#fff2c4,#f0c75e 55%%,#b8862a);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 2px 5px rgba(0,0,0,.6));white-space:nowrap}
.%(p)s-t{position:absolute;font:500 24px/1.3 "Golos Text",sans-serif;color:#f4ecd2;text-shadow:0 1px 4px rgba(0,0,0,.7)}
.%(p)s-lb{position:absolute;box-sizing:border-box;border:1.6px solid rgba(240,199,94,.85);border-radius:9px;background:rgba(6,34,26,.72);
 font:500 20px/1.2 "Golos Text",sans-serif;color:#f4ecd2;text-align:center;display:flex;align-items:center;justify-content:center}
.%(p)s-bd{position:absolute;width:64px;height:24px;background:linear-gradient(180deg,#ffe27a,#f0c030);color:#2a2000;
 font:800 22px/24px "Golos Text",sans-serif;text-align:center;transform:skew(-14deg);box-shadow:0 0 10px rgba(240,199,94,.6)}
.%(p)s-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none;overflow:visible}
.%(p)s-cl{font-family:"Golos Text",sans-serif;font-weight:700;fill:#f4ecd2;text-anchor:middle}
</style>""" % {"p": p}

def defs(p):
    mk = lambda i, c: ('<marker id="%s-%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
                       '<path d="M0 0L10 5L0 10z" fill="%s"/></marker>' % (p, i, c))
    return ('<defs>' + mk("ah", "#f6d36a") + mk("ahb", "#3fd6b0") + mk("ahs", "#f4ecd2") +
            '<radialGradient id="%(p)s-cg" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#7a9f76"/><stop offset=".55" stop-color="#357558"/><stop offset="1" stop-color="#1f4f3e"/></radialGradient>'
            '<filter id="%(p)s-gl" filterUnits="userSpaceOnUse" x="-50" y="-50" width="1800" height="1050"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>' % {"p": p})

_CIRC = [(52, 76, 30), (96, 52, 42), (148, 66, 36), (100, 88, 30), (70, 92, 24), (130, 92, 24)]

def cloud_at(p, cx, cy, wid, label=None, fs=32, dy=8, sub=None):
    """Облако (SVG) с золотой каймой; центр (cx,cy), видимая ширина wid, высота ~0.65*wid."""
    s = wid / 170.0
    c = "".join('<circle cx="%d" cy="%d" r="%d"/>' % t for t in _CIRC)
    body = ('<g fill="#f0c75e" stroke="#f0c75e" stroke-width="5" filter="url(#%s-gl)" opacity=".9">%s</g><g fill="url(#%s-cg)">%s</g>' % (p, c, p, c))
    if label:
        body += '<text class="%s-cl" x="100" y="%.1f" style="font-size:%.1fpx">%s</text>' % (p, 60 + dy / s, fs / s, label)
    return ('<svg style="position:absolute;left:%dpx;top:%dpx;overflow:visible" width="%d" height="%d" viewBox="0 0 200 120">%s</svg>'
            % (round(cx - 103 * s), round(cy - 60 * s), round(200 * s), round(120 * s), body))

def cloud_box(p, x, y, w, h):
    """Облако, растянутое в прямоугольник (x,y,w,h) - видимые габариты."""
    sx, sy = w / 170.0, h / 112.0
    c = "".join('<circle cx="%d" cy="%d" r="%d"/>' % t for t in _CIRC)
    body = ('<g fill="#f0c75e" stroke="#f0c75e" stroke-width="5" filter="url(#%s-gl)" opacity=".9">%s</g><g fill="url(#%s-cg)">%s</g>' % (p, c, p, c))
    return ('<svg style="position:absolute;left:%dpx;top:%dpx;overflow:visible" width="%d" height="%d" viewBox="0 0 200 120" preserveAspectRatio="none">%s</svg>'
            % (round(x - 18 * sx), round(y - 4 * sy), round(200 * sx), round(120 * sy), body))
