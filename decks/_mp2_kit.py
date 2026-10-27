# -*- coding: utf-8 -*-
"""Дека MPLS 2.9, подача v2: фон комплекта = фон слайда, текст pptx разнесён по смысловым блокам,
схема инфографики живая и раскрывается по шагам вместе с текстом. Без слайдов-дублей «инфографика»."""
import base64
import os

from _sw_lib import SL, _esc

HERE = os.path.dirname(os.path.abspath(__file__))
CROPS = os.path.join(HERE, "_mp_rep", "crops")
_bg_used = set()
_img = {}


def _b64(path, mime="image/webp"):
    if path not in _img:
        if path.endswith(".png"):
            import io
            from PIL import Image
            buf = io.BytesIO()
            Image.open(path).save(buf, "WEBP", quality=88, method=5)
            data = buf.getvalue()
        else:
            with open(path, "rb") as fh:
                data = fh.read()
        _img[path] = "data:%s;base64,%s" % (mime, base64.b64encode(data).decode())
    return _img[path]


def ico(file, h=64, cls="", style=""):
    """Объёмная иконка/маршрутизатор — вырезка из инфографики автора (_mp_rep/crops)."""
    return '<img class="ico %s" src="%s" style="height:%dpx;%s" alt="">' % (cls, _b64(os.path.join(CROPS, file)), h, style)


def bg_css():
    out = []
    for n in sorted(_bg_used):
        out.append('.slide.%s{background:url(%s) center/cover no-repeat}' % (
            n, _b64(os.path.join(HERE, "_mp_assets", n + ".webp"))))
    return "\n".join(out)


def slide(label, bg, title, body, safe="", sub=""):
    """bg — чистый фон комплекта (bgk_NN); safe — классы безопасной зоны (sr — справа персонаж, sl, sb …)."""
    _bg_used.add(bg)
    s = '<p class="m2sub">%s</p>' % sub if sub else ""
    SL.append('<section class="slide m2 %s" data-label="%s"><div class="m2in %s"><h1 class="m2t">%s</h1>%s%s</div></section>'
              % (bg, _esc(label), safe, title, s, body))


def step(html, cls=""):
    return '<div class="step %s">%s</div>' % (cls, html)


def panel(head, html, cls="", num=""):
    n = '<span class="m2n">%s</span>' % num if num else ""
    h = '<div class="m2h">%s%s</div>' % (n, head) if head else ""
    return '<div class="m2p %s">%s<div class="m2b">%s</div></div>' % (cls, h, html)


def row(*items, cls=""):
    return '<div class="m2row %s">%s</div>' % (cls, "".join(items))


def pk(labels, cls=""):
    """Пакет: метки слева (верхняя — первая), затем IP."""
    lb = "".join('<b>%s</b>' % x for x in labels)
    return '<span class="m2pk %s">%s<i>IP</i></span>' % (cls, lb)


def node(img, name, sub=""):
    s = '<small>%s</small>' % sub if sub else ""
    return '<div class="m2nd">%s<strong>%s</strong>%s</div>' % (img, name, s)


def arrow():
    return '<span class="m2ar">→</span>'


CSS = r"""
#bgimg,#bgfx{display:none!important}
.slide.m2{padding:0}
.slide.m2>.m2in{position:absolute;inset:0;padding:clamp(14px,2vw,34px) clamp(18px,3vw,56px) 72px;display:flex;flex-direction:column;
 gap:clamp(8px,1.1vw,18px);overflow:auto}
.slide.m2>.m2in.sr>h1.m2t{padding-right:clamp(150px,17vw,330px)}
.slide.m2>.m2in.sl{padding-left:clamp(120px,13vw,260px)}
.slide.m2>.m2in.sb{padding-bottom:clamp(110px,16vh,190px)}
h1.m2t{font:900 clamp(26px,2.9vw,56px)/1.05 "Rubik",sans-serif;color:#fff;margin:0;
 text-shadow:0 3px 0 #1550a8,3px 0 0 #1550a8,-3px 0 0 #1550a8,0 -3px 0 #1550a8,2px 2px 0 #1550a8,-2px 2px 0 #1550a8,
 2px -2px 0 #1550a8,-2px -2px 0 #1550a8,0 8px 16px rgba(10,40,90,.35)}
h1.m2t em{font-style:normal;color:#ffe38a}
.m2sub{margin:0;font:700 clamp(15px,1.35vw,26px)/1.3 "Golos Text",sans-serif;color:#fff;text-shadow:0 2px 6px rgba(10,40,90,.6)}
.m2row{display:flex;gap:clamp(8px,1vw,18px);align-items:stretch}
.m2row>*{flex:1 1 0;min-width:0}
.m2p{background:rgba(253,248,234,.96);border:3px solid #1f63c6;border-radius:20px;padding:clamp(10px,1vw,20px) clamp(12px,1.3vw,24px);
 box-shadow:0 6px 0 rgba(21,80,168,.25),0 12px 26px rgba(10,40,90,.18);color:#1d2a44}
.m2p.or{border-color:#e8742c}.m2p.gr{border-color:#2f9e5b}.m2p.rd{border-color:#d9363e}
.m2p.tint{background:rgba(214,236,251,.96)}
.m2h{display:flex;align-items:center;gap:10px;font:900 clamp(17px,1.55vw,30px)/1.1 "Rubik",sans-serif;color:#13306e;
 text-transform:uppercase;margin-bottom:8px}
.m2n{display:inline-grid;place-items:center;width:1.6em;height:1.6em;border-radius:50%;background:#e8742c;color:#fff;font-size:.85em;flex:none}
.m2b{font:500 clamp(14px,1.22vw,24px)/1.4 "Golos Text",sans-serif}
.m2b p{margin:0 0 .45em}.m2b p:last-child{margin:0}
.m2b b{color:#123a7a;font-weight:800}
.m2big{font:600 clamp(17px,1.6vw,31px)/1.4 "Golos Text",sans-serif}
.m2big b{color:#123a7a;font-weight:800}
.m2pk{display:inline-flex;border:3px solid #1d3f8a;border-radius:6px;overflow:hidden;font:800 clamp(14px,1.2vw,23px)/1.7 "Golos Text",sans-serif;
 vertical-align:middle;background:#fff}
.m2pk b{background:#f2694a;color:#1d1d1d;padding:0 .45em;border-right:2px solid #1d3f8a}
.m2pk i{font-style:normal;color:#1d3f8a;padding:0 .6em}
.m2chain{display:flex;align-items:flex-start;justify-content:space-between;gap:6px;flex-wrap:nowrap}
.m2chain>.step{display:flex;align-items:center;gap:6px}
.m2nd{display:flex;flex-direction:column;align-items:center;text-align:center;min-width:0}
.m2nd strong{font:900 clamp(15px,1.3vw,25px)/1.1 "Golos Text",sans-serif;color:#13306e;margin-top:4px}
.m2nd small{font:600 clamp(12px,1vw,19px)/1.2 "Golos Text",sans-serif;color:#33476e}
.m2ar{font:900 clamp(18px,1.8vw,34px)/1 sans-serif;color:#24577a;margin-top:18px}
.m2zone{background:rgba(191,233,228,.85);border-radius:18px;padding:10px 12px 8px;position:relative}
.m2zone>.m2zl{position:absolute;top:-14px;left:50%;transform:translateX(-50%);background:#bfe9e4;padding:0 14px;border-radius:10px;
 font:800 clamp(14px,1.15vw,22px)/28px "Golos Text",sans-serif;color:#13306e;white-space:nowrap}
.m2note{background:#ffe3df;border:2px solid #e2564a;border-radius:12px;padding:6px 14px;text-align:center;
 font:600 clamp(14px,1.25vw,24px)/1.35 "Golos Text",sans-serif;color:#13306e}
.m2note b{font-weight:900}
.m2pill{display:inline-block;padding:2px 12px;border-radius:999px;font:800 clamp(13px,1.05vw,20px)/1.6 "Golos Text",sans-serif}
.m2pill.bl{background:#d6ebfb;color:#13306e}.m2pill.or{background:#ffe0c7;color:#8a3e10}.m2pill.gr{background:#d6f3e0;color:#1b5e36}
.m2cap{font:700 clamp(13px,1.1vw,21px)/1.3 "Golos Text",sans-serif;color:#13306e;text-align:center}
.m2 .ico{display:block;max-width:100%;object-fit:contain}
.m2 .step{transition:opacity .45s,transform .45s}
.m2 .step:not(.vis){opacity:0;transform:translateY(10px)}
.m2flt{animation:m2f 2.6s ease-in-out infinite}
@keyframes m2f{50%{transform:translateY(-4px)}}
.m2tbl{width:100%;border-collapse:collapse;font:500 clamp(13px,1.1vw,21px)/1.35 "Golos Text",sans-serif;color:#1d2a44}
.m2tbl th{background:#1f63c6;color:#fff;text-align:left;padding:6px 10px;font-weight:800}
.m2tbl td{padding:6px 10px;border-top:1px solid #c9d8ef;vertical-align:top}
.m2tbl tr:nth-child(even) td{background:#f3f8ff}
"""
