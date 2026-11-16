# -*- coding: utf-8 -*-
"""Ручные слайды поверх автосборки pptx: на экране — тезисы и перерисованная схема (SVG / терминал / таблица),
полный текст слайда pptx — в свёрнутом блоке «Текст слайда из лекции» (ничего не теряется).

Спецификация деки (_<key>_man.py):  M = {номер_слайда_pptx: [P(...), P(...)]}  — одна P = один слайд деки.
"""
import re
from _sw_lib import slide, head, sc, grow, col, step, card, li
import _pt_kit as K


def P(l, r=None, t=None, src=True, sub="", stack=False):
    """l — левая колонка (html или список html), r — правая (схема), t — свой заголовок, src — приложить текст pptx."""
    return dict(l=l, r=r, t=t, src=src, sub=sub, stack=stack)


def row(*items):
    """Несколько схем в ряд (для слайдов в одну колонку)."""
    return grow("g2", *[col(x) for x in items])


def pts(items, title="Главное", tone="cy"):
    return card(title, '<ul class="li ptkey">%s</ul>' % "".join("<li>%s</li>" % i for i in items), tone)


def box(html, tone="am", title=""):
    if "<ol" in html:                       # нумерованный список → список деки с номерами (кегль как у тезисов)
        k = [0]

        def num(m):
            k[0] += 1
            return "<li><b>%d.</b> %s</li>" % (k[0], m.group(1))
        html = re.sub(r"<li>(.*?)</li>", num, re.sub(r"<ol[^>]*>", '<ul class="li">', html).replace("</ol>", "</ul>"))
    elif not re.match(r"\s*<(p|ul|ol|div|pre|table)\b", html):
        html = "<p>%s</p>" % html
    if title:
        html = "<p><b>%s</b></p>" % title + html
    return '<div class="c %s">%s</div>' % (tone, html)


def _src(s, _block):
    if not any(sh for sh in s["shapes"]):
        return ""
    return '<details class="ptsrc"><summary>Текст слайда из лекции</summary>%s</details>' % "".join(
        _block(sh, k) for k, sh in enumerate(s["shapes"]) if sh)


def emit(n, s, pages, title, t, adir, _block):
    for pi, pg in enumerate(pages):
        ttl = pg["t"] or title
        left = pg["l"] if isinstance(pg["l"], list) else [pg["l"]]
        if pi == len(pages) - 1 and pg["src"]:
            d = _src(s, _block)
            if d:
                left = left + [d]
        lab = "pptx %d · %s" % (n, re.sub("<[^>]+>", "", ttl))
        if len(pages) > 1:
            lab += " · %d" % (pi + 1)
        if pg["r"] and pg["stack"]:           # длинные команды / вывод — во всю ширину, под тезисами
            right = pg["r"] if isinstance(pg["r"], list) else [pg["r"]]
            body = grow("g", col(*[step(x) for x in left[:-1] + right + left[-1:]] if len(left) > 1 and "ptsrc" in left[-1]
                                 else [step(x) for x in left + right]))
        elif pg["r"]:
            right = pg["r"] if isinstance(pg["r"], list) else [pg["r"]]
            body = grow("g2", col(*[step(x) for x in left]), col(*[step(x) for x in right]))
        else:
            body = grow("g", col(*[step(x) for x in left]))
        slide(lab, sc(head(ttl, pg["sub"]), body))


# ------------------------------------------------------------------ SVG
SWC, PORT, ENV, ENVS = "#2f7fe0", "#1e9b45", "#f6c453", "#9a6b10"


def svg(w, h, inner, cls=""):
    return ('<div class="c ptsvgw %s"><svg class="ptsvg" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
            'font-size="14" fill="currentColor">%s</svg></div>' % (cls, w, h, inner))


def _env(path, t0, d, T, color=ENV):
    """Конверт-кадр едет по path с t0 по t0+d секунд внутри цикла T (повтор бесконечно)."""
    s, e = t0 / T, min((t0 + d) / T, 1)
    kt = "0;%.4f;%.4f;1" % (s, e)
    return ('<g opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0" keyTimes="0;%.4f;%.4f" dur="%ss" '
            'repeatCount="indefinite"/><animateMotion dur="%ss" repeatCount="indefinite" calcMode="linear" keyPoints="0;0;1;1" '
            'keyTimes="%s" path="%s"/><g transform="translate(-12,-8)"><rect width="24" height="16" rx="2" fill="%s" stroke="%s" '
            'stroke-width="1.5"/><path d="M1,1 L12,9 L23,1" fill="none" stroke="%s" stroke-width="1.5"/></g></g>'
            % (s, e, T, T, kt, path, color, ENVS, ENVS))


def _sw(x, y, name, w=110, h=70):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s"/>'
            '<path d="M%d,%d h28 m-6,-5 l6,5 l-6,5 M%d,%d h-28 m6,-5 l-6,5 l6,5" stroke="#fff" stroke-width="2.4" fill="none"/>'
            '<text x="%d" y="%d" text-anchor="middle" fill="#fff" font-weight="800" font-size="18">%s</text>'
            % (x - w // 2, y - h // 2, w, h, SWC, x - 14, y - 12, x + 14, y - 2, x, y + 22, name))


def _pc(x, y, name):
    return ('<rect x="%d" y="%d" width="46" height="32" rx="4" fill="none" stroke="%s" stroke-width="3"/>'
            '<path d="M%d,%d h22 M%d,%d v8" stroke="%s" stroke-width="3"/>'
            '<text x="%d" y="%d" text-anchor="middle" font-weight="800" font-size="17">%s</text>'
            % (x - 23, y - 24, SWC, x - 11, y + 18, x, y + 8, SWC, x, y + 40, name))


def _dot(x, y, lab, dy=-10, anchor="middle"):
    return ('<circle cx="%d" cy="%d" r="6.5" fill="%s"/><text x="%d" y="%d" text-anchor="%s" font-size="16" font-weight="700" class="mono">%s</text>'
            % (x, y, PORT, x, y + dy, anchor, lab))


def _mac(x, y, rows):
    out = ['<text x="%d" y="%d" class="mono" font-size="14" opacity=".7">MAC Address       Ports</text>' % (x, y),
           '<path d="M%d,%d h190" stroke="currentColor" opacity=".35" stroke-dasharray="4 3"/>' % (x, y + 7)]
    for k, (m, p, hl) in enumerate(rows):
        out.append('<text x="%d" y="%d" class="mono" font-size="14" font-weight="%s" %s>%s  %s</text>'
                   % (x, y + 28 + k * 20, 800 if hl else 500, 'fill="#d6336c"' if hl else "", m, p))
    return "".join(out)


# координаты топологии PC-A — SW-1 ═ SW-2 — PC-B
_A, _S1, _S2, _B, _Y = 40, 205, 435, 600, 215
_PT = dict(a=(_A + 26, _Y), g11=(_S1 - 55, _Y), g12=(_S1 + 55, _Y - 20), g13=(_S1 + 55, _Y + 20),
           g22=(_S2 - 55, _Y - 20), g23=(_S2 - 55, _Y + 20), g21=(_S2 + 55, _Y), b=(_B - 26, _Y))
ROUTES = {"A1": "a g11", "1u": "g12 g22", "1d": "g13 g23", "2B": "g21 b", "u1": "g22 g12", "d1": "g23 g13", "B2": "b g21", "1A": "g11 a"}


def route(*keys):
    pts_, out = [], []
    for k in keys:
        for p in ROUTES.get(k, k).split():
            if not pts_ or pts_[-1] != p:
                pts_.append(p)
    return "M" + " L".join("%d,%d" % _PT[p] for p in pts_)


def topo(t1=(), t2=(), po=False, flows=(), T=6, note="", third=False):
    """t1/t2 — строки MAC-таблиц [(mac, порт, выделить)], po — Port-Channel 1, flows — [(route, старт, длительность)]."""
    g = []
    ln = 'stroke="currentColor" stroke-width="2.4" opacity=".75"'
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" %s/>' % (_PT["a"] + _PT["g11"] + (ln,)))
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" %s/>' % (_PT["g12"] + _PT["g22"] + (ln,)))
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" %s/>' % (_PT["g13"] + _PT["g23"] + (ln,)))
    if third:
        g.append('<path d="M%d,%d C%d,%d %d,%d %d,%d" fill="none" %s stroke-dasharray="7 5"/>'
                 % (_S1, _Y + 32, _S1 + 60, _Y + 95, _S2 - 60, _Y + 95, _S2, _Y + 32, ln))
    g.append('<line x1="%d" y1="%d" x2="%d" y2="%d" %s/>' % (_PT["g21"] + _PT["b"] + (ln,)))
    g += [_pc(_A, _Y, "PC-A"), _pc(_B, _Y, "PC-B"), _sw(_S1, _Y, "SW-1"), _sw(_S2, _Y, "SW-2")]
    if po:
        for x in (_S1 + 55, _S2 - 55):
            g.append('<ellipse cx="%d" cy="%d" rx="17" ry="38" fill="#3ddc60" fill-opacity=".55" stroke="#1e9b45" stroke-width="2"/>'
                     '<text x="%d" y="%d" text-anchor="middle" font-weight="800" font-size="12" fill="#0b4d1f">Po1</text>' % (x, _Y, x, _Y + 4))
    g += [_dot(*_PT["g11"], lab="Gi0/1", dy=30), _dot(*_PT["g12"], lab="Gi0/2", dy=-12), _dot(*_PT["g13"], lab="Gi0/3", dy=28),
          _dot(*_PT["g22"], lab="Gi0/2", dy=-12), _dot(*_PT["g23"], lab="Gi0/3", dy=28), _dot(*_PT["g21"], lab="Gi0/1", dy=30)]
    g.append(_mac(8, 34, t1) + _mac(330, 34, t2))
    for r, t0, d in flows:
        g.append(_env(r, t0, d, T))
    if note:
        g.append('<text x="320" y="340" text-anchor="middle" font-weight="800" font-size="17">%s</text>' % note)
    return svg(640, 352, "".join(g))


def bars(rows, w=780):
    """Простые «слои» для схем LLC/MAC/PHY: rows — [(x, y, w, h, текст, пунктир)]"""
    g = []
    for x, y, bw, bh, txt, dash in rows:
        g.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="currentColor" stroke-width="2.2" %s/>'
                 '<text x="%d" y="%d" text-anchor="middle" font-size="16">%s</text>'
                 % (x, y, bw, bh, 'stroke-dasharray="7 5"' if dash else "", x + bw // 2, y + bh // 2 + 6, txt))
    return "".join(g)
