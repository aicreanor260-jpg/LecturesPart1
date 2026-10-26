# -*- coding: utf-8 -*-
"""Вёрстка инфографик деки «OSPF 2.5 (по pptx)» поверх чистых фонов: _o5_rep/<имя>.py (W, H, HTML[, TOP]).
Оригиналы — _o5_src/<имя>.png, вырезки — _o5_rep/crops/, фоны — _ospf_assets/bg/bg1..bg8.webp (кавайные облака)."""
import base64
import importlib.util
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(HERE, "_o5_rep")
SRC = os.path.join(HERE, "_o5_src")
BG = os.path.join(HERE, "_ospf_assets", "bg")
_cache = {}


def _webp(path, q=84):
    if path not in _cache:
        from PIL import Image
        buf = io.BytesIO()
        Image.open(path).save(buf, "WEBP", quality=q, method=5)
        _cache[path] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[path]


def bg(name, w=1672, h=941):
    """Чистый фон на весь холст: bg('bg2') — облака с городом, bg5 — розово-голубые облака, bg7 — светлый туман,
    bg1/bg8 — комната с окном слева/справа, bg3 — облачные ярусы, bg4 — облака с городом по краям, bg6 — насыщенный город."""
    p = os.path.join(BG, name + ".webp")
    key = ("bg", p)
    if key not in _cache:
        with open(p, "rb") as fh:
            _cache[key] = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()
    return ('<img class="ab dkbg" src="%s" style="left:0;top:0;width:%dpx;height:%dpx;object-fit:cover" alt="">'
            % (_cache[key], w, h))


def img(file, style="", cls="ab"):
    """Вырезка из _o5_rep/crops/<file>."""
    return '<img class="%s" src="%s" style="%s" alt="">' % (cls, _webp(os.path.join(REP, "crops", file)), style)


def load(name):
    f = os.path.join(REP, name + ".py")
    if not os.path.exists(f):
        return None
    spec = importlib.util.spec_from_file_location("o5rep_" + name, f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.W, m.H, m.HTML
    return m


def rep_html(name):
    try:
        m = load(name)
    except Exception as e:  # правка одной вёрстки не должна валить сборку
        print("ОШИБКА вёрстки", name, e)
        return None
    if m is None:
        return None
    top = getattr(m, "TOP", 0)
    return ('<div class="rep dkrep o5rep" data-rep="%s"><div class="repc" style="width:%dpx;height:%dpx;overflow:hidden">'
            '<div style="position:relative;width:%dpx;height:%dpx;margin-top:-%dpx">%s</div></div></div>'
            % (name, m.W, m.H - top, m.W, m.H, top, m.HTML))


def src_html(name):
    """Запасной вариант, пока вёрстки нет: оригинал картинкой."""
    return '<div class="pic"><img src="%s" alt="" loading="lazy"></div>' % _webp(os.path.join(SRC, name + ".png"), 80)
