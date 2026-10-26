# -*- coding: utf-8 -*-
"""Вёрстка инфографик дек-спутников поверх чистых фонов: _dk_rep/<имя>.py (W, H, HTML[, TOP])."""
import base64
import importlib.util
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(HERE, "_dk_rep")
_cache = {}


def _webp(path, q=84):
    if path not in _cache:
        from PIL import Image
        buf = io.BytesIO()
        Image.open(path).save(buf, "WEBP", quality=q, method=5)
        _cache[path] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[path]


def bg(name):
    """Чистый фон на весь холст 1672×941: bg('bgk_laptop')."""
    for d in ("_bs_assets", "_vl_assets"):
        p = os.path.join(HERE, d, name + ".webp")
        if os.path.exists(p):
            with open(p, "rb") as fh:
                uri = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()
            return ('<img class="ab dkbg" src="%s" style="left:0;top:0;width:1672px;height:941px" alt="">' % uri)
    raise FileNotFoundError(name)


def img(file, style="", cls="ab"):
    """Вырезка из _dk_rep/crops/<file>."""
    return '<img class="%s" src="%s" style="%s" alt="">' % (cls, _webp(os.path.join(REP, "crops", file)), style)


def rep_html(name):
    f = os.path.join(REP, name + ".py")
    if not os.path.exists(f):
        return None
    spec = importlib.util.spec_from_file_location("dkrep_" + name, f)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
        m.W, m.H, m.HTML
    except Exception as e:  # правка вёрстки не должна валить сборку
        print("ОШИБКА вёрстки", name, e)
        return None
    top = getattr(m, "TOP", 0)
    return ('<div class="rep dkrep" data-rep="%s"><div class="repc" style="width:%dpx;height:%dpx;overflow:hidden">'
            '<div style="position:relative;width:%dpx;height:%dpx;margin-top:-%dpx">%s</div></div></div>'
            % (name, m.W, m.H - top, m.W, m.H, top, m.HTML))
