# -*- coding: utf-8 -*-
"""Вёрстка инфографик деки MPLS 2.9 поверх чистых фонов: _mp_rep/<имя>.py (W, H, HTML[, TOP]).
Имя = имя инфографики (i05a …). Если файла нет — в деке остаётся картинка."""
import base64
import importlib.util
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(HERE, "_mp_rep")
_cache = {}


def _uri(path, q=82):
    if path not in _cache:
        if path.endswith(".webp"):
            with open(path, "rb") as fh:
                data = fh.read()
        else:
            from PIL import Image
            buf = io.BytesIO()
            Image.open(path).save(buf, "WEBP", quality=q, method=5)
            data = buf.getvalue()
        _cache[path] = "data:image/webp;base64," + base64.b64encode(data).decode()
    return _cache[path]


def bg(name):
    """Чистый фон комплекта на весь холст 1672×941: bg('bgk_07') (список — _mp_rep/BGLIST.md)."""
    p = os.path.join(HERE, "_mp_assets", name + ".webp")
    return '<img class="ab mpbg" src="%s" style="left:0;top:0;width:1672px;height:941px" alt="">' % _uri(p)


def img(file, style="", cls="ab"):
    """Вырезка из оригинала: _mp_rep/crops/<file>."""
    return '<img class="%s" src="%s" style="%s" alt="">' % (cls, _uri(os.path.join(REP, "crops", file)), style)


def exists(name):
    return os.path.exists(os.path.join(REP, name + ".py"))


def rep_html(name):
    f = os.path.join(REP, name + ".py")
    if not os.path.exists(f):
        return None
    spec = importlib.util.spec_from_file_location("mprep_" + name, f)
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
        m.W, m.H, m.HTML
    except Exception as e:  # правка вёрстки не должна валить сборку
        print("ОШИБКА вёрстки", name, e)
        return None
    top = getattr(m, "TOP", 0)
    return ('<div class="mprep" data-rep="%s"><div class="mprepc" style="width:%dpx;height:%dpx">'
            '<div style="position:relative;width:%dpx;height:%dpx;margin-top:-%dpx">%s</div></div></div>'
            % (name, m.W, m.H - top, m.W, m.H, top, m.HTML))


CSS = r"""
.mprep{flex:1 1 auto;min-height:0;position:relative;overflow:hidden;border-radius:16px}
.mprepc{position:absolute;left:0;top:0;transform-origin:0 0;overflow:hidden;border-radius:16px;
 box-shadow:0 8px 0 rgba(21,80,168,.3),0 14px 30px rgba(10,40,90,.3);font-family:"Golos Text",sans-serif;color:#1d2a44}
.mprepc *{box-sizing:border-box}
.mprepc .ab{position:absolute}
"""

JS = r"""
(function(){
  function fit(){document.querySelectorAll('.slide.on .mprep').forEach(function(r){
    var c=r.firstElementChild,W=c.offsetWidth,H=c.offsetHeight,rw=r.clientWidth,rh=r.clientHeight;
    if(!rw||!rh)return;var s=Math.min(rw/W,rh/H);
    c.style.transform='translate('+((rw-W*s)/2)+'px,'+((rh-H*s)/2)+'px) scale('+s+')';});}
  window.addEventListener('resize',fit);
  new MutationObserver(fit).observe(document.getElementById('stage'),{subtree:true,attributes:true,attributeFilter:['class']});
  setTimeout(fit,50);
})();
"""
