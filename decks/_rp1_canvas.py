# -*- coding: utf-8 -*-
"""Вёрстка слайдов RIP 2.5.1 на чистых подложках инфографик (холст 1672×941, масштабируется под экран).
Элементы ставятся в координатах исходной инфографики; иконки — вырезки из инфографик автора."""
import base64
import io
import os

from _sw_lib import SL, _esc

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "_rp1_assets")
_cache = {}

# вырезки иконок из исходных инфографик: имя → (файл, x0, y0, x1, y1)
ICONS = {
    "doc": ("i_general1", 52, 575, 205, 700), "gear": ("i_general1", 52, 712, 205, 830),
    "pin": ("i_general1", 612, 588, 742, 668), "arrow": ("i_general1", 612, 678, 742, 758),
    "people": ("i_general1", 612, 768, 742, 852), "db": ("i_general1", 1125, 575, 1255, 668),
    "bars": ("i_general1", 1125, 680, 1255, 765), "stop": ("i_general1", 1125, 772, 1255, 865),
    "db2": ("i_general2", 455, 550, 540, 610), "clock": ("i_general2", 455, 622, 540, 682),
    "wifi": ("i_general2", 455, 695, 540, 758), "people2": ("i_general2", 455, 770, 540, 840),
    "cog": ("i_general2", 1280, 552, 1355, 610), "scales": ("i_general2", 1280, 620, 1355, 680),
    "db3": ("i_general2", 1280, 700, 1355, 762), "shield": ("i_general2", 1280, 780, 1355, 840),
    "excl": ("i_general2", 62, 788, 102, 828),
    "shieldok": ("i_split", 70, 650, 290, 860), "sync": ("i_split", 1000, 660, 1180, 850),
    "routerx": ("i_loops", 40, 640, 420, 760), "trig": ("i_loops", 450, 625, 825, 800),
    "hold": ("i_loops", 880, 615, 1200, 815), "poison": ("i_loops", 1255, 610, 1640, 765),
    "xchg": ("i_bf", 50, 640, 530, 840), "calc": ("i_bf", 610, 655, 1085, 835), "chg": ("i_bf", 1150, 630, 1630, 820),
    "setup1": ("i_setup", 40, 640, 330, 860), "setup2": ("i_setup", 505, 640, 820, 900),
    "setup3": ("i_setup", 880, 640, 1210, 860), "setup4": ("i_setup", 1300, 640, 1630, 845),
    "check": ("i_setup", 1330, 115, 1385, 170),
}


def _uri(path, crop=None, q=86):
    key = (path, crop)
    if key not in _cache:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        if crop:
            im = im.crop(crop)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=q, method=5)
        _cache[key] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[key]


def plate(name):
    return _uri(os.path.join(SRC, "p_%s.webp" % name), q=84)


def icon(name, w=None, extra=""):
    f, x0, y0, x1, y1 = ICONS[name]
    st = "width:%dpx" % w if w else ""
    return '<img class="cv-ic" src="%s" style="%s;%s" alt="">' % (_uri(os.path.join(SRC, f + ".webp"), (x0, y0, x1, y1)), st, extra)


def at(x, y, w, html, cls="", h=None, step=False, style=""):
    hh = "height:%dpx;" % h if h else ""
    c = ("cv-at " + cls + (" step" if step else "")).strip()
    return '<div class="%s" style="left:%dpx;top:%dpx;width:%dpx;%s%s">%s</div>' % (c, x, y, w, hh, style, html)


def h1(x, y, w, text, size=64):
    return at(x, y, w, text, "cv-h1", style="font-size:%dpx" % size)


def panel(x, y, w, h, title="", body="", step=False, tsize=30):
    t = '<div class="cv-pt" style="font-size:%dpx">%s</div>' % (tsize, title) if title else ""
    return at(x, y, w, t + body, "cv-panel", h=h, step=step)


def row(ic, html, size=19, icw=64, step=False):
    i = icon(ic, icw) if ic else ""
    return '<div class="cv-row%s">%s<div style="font-size:%dpx">%s</div></div>' % (" step" if step else "", i, size, html)


def pill(x, y, w, h, html, kind="g", size=22, step=False):
    return at(x, y, w, html, "cv-pill cv-%s" % kind, h=h, step=step, style="font-size:%dpx" % size)


def term(lines):
    return '<pre class="cv-term">%s</pre>' % "\n".join(_esc(l) for l in lines)


def slide(label, plate_name, items):
    SL.append('<section class="slide rpfs" data-plate="%s" data-label="%s"><div class="rpcv"><div class="rpci" style="background-image:url(%s)">%s'
              '</div></div></section>' % (plate_name, _esc(label), plate(plate_name), "".join(items)))


CSS = r"""
.slide.rpfs{padding:0}
.rpcv{position:absolute;left:0;right:0;top:0;bottom:56px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.rpci{position:relative;flex:none;width:1600px;height:900px;transform-origin:center center}
.cv-at{position:absolute}
.cv-h1{font-family:"Unbounded","Golos Text",sans-serif;font-weight:900;line-height:.98;color:#1f6b4a;text-transform:uppercase;letter-spacing:-.015em}
.cv-sub{font:500 22px/1.35 "Golos Text",sans-serif;color:#2c7357}
.cv-sub b{color:#155a3e}
.cv-panel{background:#fff;border:2px solid #cdeee0;border-radius:22px;box-shadow:0 10px 30px rgba(30,110,80,.12);
 padding:20px 22px;display:flex;flex-direction:column;gap:10px}
.cv-pt{font-family:"Unbounded",sans-serif;font-weight:900;line-height:1.02;color:#1f6b4a;text-transform:uppercase;margin-bottom:4px}
.cv-row{display:flex;gap:14px;align-items:center;background:#f0faf5;border-radius:18px;padding:9px 14px}
.cv-row>div{font-family:"Golos Text",sans-serif;font-weight:500;line-height:1.32;color:#17463a}
.cv-row b{color:#0f4f36;font-weight:800}
.cv-ic{flex:none;border-radius:16px;display:block}
.cv-pill{display:flex;align-items:center;justify-content:center;text-align:center;border-radius:999px;
 font-family:"Golos Text",sans-serif;font-weight:800;line-height:1.15;padding:6px 18px;box-shadow:0 4px 14px rgba(30,110,80,.15)}
.cv-g{background:#d6f3e3;color:#155a3e;border:2px solid #9fdcbe}
.cv-gs{background:#2fae6a;color:#fff;border:2px solid #23915a}
.cv-p{background:#ffe1ec;color:#b02a5c;border:2px solid #f3a3c0}
.cv-v{background:#e4e3ff;color:#3c46a8;border:2px solid #b7b5f0}
.cv-w{background:#fff;color:#17463a;border:2px solid #cdeee0}
.cv-txt{font:500 19px/1.38 "Golos Text",sans-serif;color:#17463a}
.cv-txt b{color:#0f4f36}
.cv-term{font:500 15px/1.42 "JetBrains Mono",monospace;color:#d7f5ea;background:#0e231e;border:2px solid #2c8f80;border-radius:16px;
 padding:14px 16px;margin:0;white-space:pre;overflow:hidden}
"""

JS = r"""
(function(){
  function fit(){var s=Math.min(window.innerWidth/1600,(window.innerHeight-56)/900);
    document.querySelectorAll('.rpci').forEach(function(c){c.style.transform='scale('+s+')';});}
  window.addEventListener('resize',fit);fit();
  /* текст pptx не режется: если слайд не помещается, он плавно уменьшается целиком (не меньше 72 %) */
  function shrink(){document.querySelectorAll('.slide.on>.sc').forEach(function(sc){
    sc.style.zoom=1;var z=1;
    while(z>0.72&&sc.scrollHeight>sc.clientHeight+2){z-=0.02;sc.style.zoom=z;}});}
  new MutationObserver(function(ms){ms.forEach(function(m){if(m.target.classList.contains('on'))shrink();});})
    .observe(document.getElementById('stage'),{subtree:true,attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',shrink);setTimeout(shrink,300);
})();
"""


TONE_ICON = {"cy": "doc", "mg": "sync", "lm": "pin", "am": "clock", "rd": "stop", "": "doc"}


def card(title, body, tone="", icon_name=None):
    """Карточка в стиле инфографик: иконка-плитка из комплекта + заголовок + текст."""
    ic = icon(icon_name or TONE_ICON.get(tone, "doc"), 52)
    h = '<div class="ch">%s<h3>%s</h3></div>' % (ic, title) if title else ""
    if not title:
        return '<div class="c rpc %s"><div class="rpc-row">%s<div class="rpc-b">%s</div></div></div>' % (tone, ic, body)
    return '<div class="c rpc %s">%s%s</div>' % (tone, h, body)


def section_bg_css():
    return """
.rpc .ch .cv-ic{width:46px;border-radius:12px}
.rpc-row{display:flex;gap:14px;align-items:flex-start}
.rpc-row>.cv-ic{width:52px;border-radius:14px;margin-top:2px}
.rpc-b{flex:1;min-width:0}
"""
