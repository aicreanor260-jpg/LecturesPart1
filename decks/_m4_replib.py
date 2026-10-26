# -*- coding: utf-8 -*-
"""Вёрстка инфографик деки 2.4 поверх чистого фона: _m4_rep/<имя>.py (W, H, HTML[, TOP])."""
import base64
import importlib.util
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(HERE, "_m4_rep")
_cache = {}


def _uri(path, q=84):
    if path not in _cache:
        from PIL import Image
        buf = io.BytesIO()
        Image.open(path).save(buf, "WEBP", quality=q, method=5)
        _cache[path] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[path]


def bg(name="bg_main"):
    """Чистый фон 1672×941 (небо + город из инфографик комплекта)."""
    uri = _uri(os.path.join(HERE, "_m4_assets", name + ".webp"), 80)
    return '<img class="ab" src="%s" style="position:absolute;left:0;top:0;width:1672px;height:941px" alt="">' % uri


def img(file, style=""):
    """Вырезка из _m4_rep/crops/<file> (PNG с прозрачным фоном)."""
    return '<img class="ab" src="%s" style="position:absolute;%s" alt="">' % (_uri(os.path.join(REP, "crops", file)), style)


def rep_html(name):
    f = os.path.join(REP, name + ".py")
    if not os.path.exists(f):
        return None
    spec = importlib.util.spec_from_file_location("m4rep_" + name, f)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
        m.W, m.H, m.HTML
    except Exception as e:  # правка одной вёрстки не должна валить сборку
        print("ОШИБКА вёрстки", name, e)
        return None
    top = getattr(m, "TOP", 0)
    return ('<div class="rep dkrep" data-rep="%s"><div class="repc" style="width:%dpx;height:%dpx;overflow:hidden">'
            '<div style="position:relative;width:%dpx;height:%dpx;margin-top:-%dpx">%s</div></div></div>'
            % (name, m.W, m.H - top, m.W, m.H, top, m.HTML))
