# -*- coding: utf-8 -*-
"""Блоки деки MPLS 2.9: слайд «как в pptx», инфографика автора, таблица, сцена."""
import base64
import re
import os

from _sw_lib import slide, head, sc, grow, col, card, p, li, step, foot, table, _esc  # noqa: F401
from _dk_kit import txt  # noqa: F401
import _mp_fig as F  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
ADIR = os.path.join(HERE, "_mp_assets")
_cache = {}


def b64(name):
    if name not in _cache:
        with open(os.path.join(ADIR, name + ".webp"), "rb") as fh:
            _cache[name] = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()
    return _cache[name]


def info(n, title, sub="", k="a"):
    """Инфографика автора к слайду pptx n — отдельным слайдом сразу за ним."""
    slide("pptx %d · инфографика%s" % (n, "" if k == "a" else " " + k),
          sc(head(title, sub), grow("g", col(_rep_or_pic("i%02d%s" % (n, k))))))


def _rep_or_pic(name):
    import _mp_replib
    r = _mp_replib.rep_html(name)
    if r:
        return r
    return '<div class="pic mppic"><img src="%s" alt="" loading="lazy"></div>' % b64(name)


def ps(label, title, left, right=None, layout="g2", sub=""):
    """Слайд по pptx: слева текст, справа рисунок/таблица; блоки по шагам."""
    L = col(*[step(b) for b in left])
    body = grow("g", L) if right is None else grow(layout, L, col(*[step(b) for b in right]))
    n = len(re.sub(r"<svg.*?</svg>|<[^>]+>", "", "".join(left + (right or [])), flags=re.S))
    fs = "mpfs1" if n < 700 else "mpfs2" if n < 1200 else "mpfs3" if n < 1800 else "mpfs4"
    slide(label, sc(head(title, sub), '<div class="mpfs %s">%s</div>' % (fs, body)))


def tbl(headers, rows, title=""):
    h = '<div class="mt-t">%s</div>' % title if title else ""
    return h + table(headers, rows, "mt")


def fig(html):
    return F.panel(html)
