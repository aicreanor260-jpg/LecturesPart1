# -*- coding: utf-8 -*-
"""Сборка двух дек-спутников «Коммутации 2.2» на её движке:

    python _dk_build.py base   → bazovye-nastrojki.html  (розовый комикс-город)
    python _dk_build.py vlan   → vlan.html               (пиксельный платформер)
    python _dk_build.py        → обе

Слайды берутся из модулей _sw_s5…_sw_s7 (+ вставки _sw_fig) — дека kommutaciya.html не меняется.
Старые неоновые инфографики подменяются новыми из комплектов «2.2 Базовые настройки» и «2.2 VLAN»,
палитра движка перекрашивается функцией recolor(), поверх — CSS темы из _dk_theme.
"""
import base64
import colorsys
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import _sw_lib as L  # noqa: E402

_orig_pic = L.pic
_cache = {}
OVR = {}       # старое имя картинки → новое (задаётся темой)
ADIR = [""]    # папка ассетов текущей деки


def nb64(name):
    key = (ADIR[0], name)
    if key not in _cache:
        with open(os.path.join(HERE, ADIR[0], name + ".webp"), "rb") as fh:
            _cache[key] = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()
    return _cache[key]


def npic(name, cap=""):
    import _dk_replib
    r = _dk_replib.rep_html(name)
    if r:
        return "<!--norc-->" + r + "<!--/norc-->"
    c = '<div class="piccap">%s</div>' % cap if cap else ""
    return '<div class="pic"><img src="%s" alt="" loading="lazy"></div>%s' % (nb64(name), c)


def _pic(name, cap=""):
    if name in OVR:
        return npic(OVR[name], cap)
    return _orig_pic(name, cap)


L.pic = _pic  # до импорта модулей слайдов: они делают from _sw_lib import pic


def info_slide(label, title, name, sub=""):
    return ('<section class="slide" data-label="%s">%s</section>'
            % (L._esc(label), L.sc(L.head(title, sub), L.grow("g", npic(name)))))


def scene_theme(key):
    """Сцены SVG в стиле деки: ПК — рисунок из инфографик, кабели за устройствами, сплошные."""
    import _sw_svg as S
    import _dk_replib
    if not hasattr(S, "_orig"):
        S._orig = {"pc": S.pc, "link": S.link, "fig": S.fig, "switch": S.switch}
    o = S._orig
    uri = _dk_replib._webp(os.path.join(HERE, "_dk_rep", "crops", "dev_%s_pc.png" % key))
    dark = "#0a1440" if key == "vlan" else "#2a0a2a"

    def pc(x, y, name, mac="", col=S.CY, vlan=""):
        g = ['<g>', '<image href="%s" x="%g" y="%g" width="104" height="82" preserveAspectRatio="xMidYMid meet"/>'
             % (uri, x - 52, y - 4)]
        w = max(70, len(name) * 10 + 20)
        g.append('<rect x="%g" y="%g" width="%g" height="24" fill="%s" stroke="%s" stroke-width="2.5" class="dkpill"/>'
                 % (x - w / 2.0, y + 82, w, dark, col))
        g.append(S.txt(x, y + 99, name, 14, "#fff", 800))
        if mac:
            g.append(S.txt(x, y + 124, mac, 12, "#fff", 700, mono=True))
        if vlan:
            g.append(S.txt(x, y + 140, vlan, 12, col, 800))
        g.append("</g>")
        return "".join(g)

    def link(x1, y1, x2, y2, col=S.CY, w=2.4, op=.5, dash=False, extra=""):
        return o["link"](x1, y1, x2, y2, col, max(w, 3.5), 1, dash, ' class="lnk"' + extra)

    def fig(body, vb="0 0 1200 560", cls="fig"):
        lnk = re.findall(r'<path [^>]*class="lnk"[^>]*/>', body)
        for l in lnk:
            body = body.replace(l, "", 1)
        # <b> внутри SVG ломает разбор HTML — жирный через tspan
        body = re.sub(r"<b>(.*?)</b>", r'<tspan font-weight="900"></tspan>', body)
        return o["fig"]("".join(lnk) + body, vb, cls + " dkfig")

    def switch(x, y, w=380, h=74, ports=8, label="Коммутатор", col=S.CY, pid=None, names=None):
        svg, pts = o["switch"](x, y, w, h, ports, "", col, pid, names)
        lab = S.txt(x + 16, y + 26, label, 14, "#fff", 800, "start")
        return svg.replace("</g>", lab + "</g>", 1) if label else svg, pts

    S.pc, S.link, S.fig, S.switch = pc, link, fig, switch


def collect():
    """Полный список слайдов коммутации (как в kommutaciya.html)."""
    del L.SL[:]
    for m in ["_sw_s1", "_sw_s2", "_sw_s3", "_sw_s4", "_sw_s5", "_sw_s6", "_sw_s7", "_sw_s8"]:
        mod = __import__(m)
        mod.build()
    import _sw_fig
    _sw_fig.apply()
    return list(L.SL)


def label(s):
    return re.search(r'data-label="([^"]*)"', s).group(1)


def cut(slides, first, stop):
    labs = [label(s) for s in slides]
    a = labs.index(first)
    b = labs.index(stop, a)
    return slides[a:b]


def insert_after(slides, extra):
    """extra: {label: [html, ...]} — вставить после первого слайда с таким label."""
    out = []
    for s in slides:
        out.append(s)
        out.extend(extra.pop(label(s), []))
    if extra:
        raise SystemExit("не найдены слайды для вставки: %s" % list(extra))
    return out


def replace_slide(slides, lab, html):
    return [html if label(s) == lab else s for s in slides]


def dedupe(slides):
    """Повторный data-label (рисунок из pptx к той же теме) получает пометку «· рис.»."""
    seen, out = set(), []
    for s in slides:
        lab = label(s)
        if lab in seen:
            s = s.replace('data-label="%s"' % lab, 'data-label="%s · рис."' % lab, 1)
        seen.add(lab)
        out.append(s)
    return out


# ----------------------------------------------------------------- перекраска
_HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
_RGB = re.compile(r"rgb(a?)\((\d+),\s*(\d+),\s*(\d+)")


def recolor(text, fn):
    """Применить fn(r,g,b)->(r,g,b) ко всем цветам вне data:-URI."""
    def hx(m):
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        r, g, b = fn(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        return "#%02x%02x%02x" % (r, g, b)

    def rg(m):
        r, g, b = fn(int(m.group(2)), int(m.group(3)), int(m.group(4)))
        return "rgb%s(%d,%d,%d" % (m.group(1), r, g, b)

    parts = re.split(r'(data:[^"\')\s]+|<!--norc-->.*?<!--/norc-->)', text, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = _RGB.sub(rg, _HEX.sub(hx, parts[i]))
    return "".join(parts)


def hue_map(rules):
    """rules: список (h_from, h_to, h_new, sat_mul). Оттенки в градусах."""
    def fn(r, g, b):
        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        hd = h * 360
        if s < .12:
            return r, g, b
        for a, z, nh, sm in rules:
            if a <= hd <= z:
                nr, ng, nb = colorsys.hls_to_rgb((nh % 360) / 360.0, l, min(1, s * sm))
                return int(round(nr * 255)), int(round(ng * 255)), int(round(nb * 255))
        return r, g, b
    return fn


# ----------------------------------------------------------------- сборка
def build(key):
    import _dk_theme as T
    import _dk_extra as X
    from _sw_style import CSS
    from _sw_engine import JS
    import _sw_fig
    import _sw_build
    import _dk_kit
    import _vl_fig
    import _bs_fig

    cfg = T.THEMES[key]
    OVR.clear()
    OVR.update(cfg["ovr"])
    ADIR[0] = cfg["adir"]
    scene_theme(key)
    # слайды строго по порядку pptx: модуль деки (_bs_deck / _vl_deck)
    del L.SL[:]
    __import__(cfg["deck"]).build()
    body = list(L.SL)

    del L.SL[:]
    getattr(X, key + "_head")()
    head_sl = list(L.SL)
    del L.SL[:]
    getattr(X, key + "_tail")()
    tail_sl = list(L.SL)
    slides = dedupe(head_sl + body + tail_sl)
    fn = hue_map(cfg["hues"])

    css = recolor(CSS + _sw_fig.CSS, fn) + T.REP_CSS + T.common_css(nb64("bg_main"), nb64("bg_cover")) + cfg["css"] + T.SCENE_CSS[key] + _dk_kit.CSS + _vl_fig.CSS + _bs_fig.CSS
    html_sl = recolor("\n".join(slides), fn)
    hud = _sw_build.HUD
    js = recolor(JS + _sw_fig.JS, fn)
    html = (
        '<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>%s</title>\n%s\n<style>%s</style>\n</head>\n<body class=\"th-%s\">\n"
        '<div id="bgimg"></div><div id="bgfx"></div>\n<div id="stage">\n%s\n</div>\n%s\n'
        "<script>%s</script>\n</body>\n</html>\n"
        % (cfg["title"], cfg["fonts"], css, key, html_sl, hud, js))
    out = os.environ.get("DK_OUT") or os.path.join(HERE, cfg["out"])
    with io.open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("готово: %s — %d слайдов, %.2f МБ" % (out, len(slides), os.path.getsize(out) / 1048576.0))


if __name__ == "__main__":
    keys = sys.argv[1:] or ["base", "vlan"]
    for k in keys:
        build(k)
