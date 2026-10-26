# -*- coding: utf-8 -*-
"""Блоки деки 2.4: слайд «как в pptx», конфигурация с приглушённым приглашением, консоль, таблицы, инфографики."""
import base64
import os
import re

from _sw_lib import SL, slide, head, sc, grow, col, card, p, li, step, _esc
from _dk_kit import term, frame, flow, txt  # noqa: F401  (переиспользуем блоки 2.2)

HERE = os.path.dirname(os.path.abspath(__file__))
ADIR = os.path.join(HERE, "_m4_assets")
_cache = {}

_PROMPT = re.compile(r"^(\s*[A-Za-z0-9_\-]+(?:\([a-z\-]+\))?#)(.*)$")


_SRC = {}
_TX = {}


def src(n):
    """Абзацы текста слайда pptx n — дословно (выгрузка _m4_src.json)."""
    if not _SRC:
        import json
        _SRC.update(json.load(open(os.path.join(HERE, "_m4_src.json"), encoding="utf-8")))
    return list(_SRC[str(n)])


def tx(n):
    """Расшифровка картинок слайда pptx n (_m4_tx.json): список фигур."""
    if not _TX:
        import json
        _TX.update(json.load(open(os.path.join(HERE, "_m4_tx.json"), encoding="utf-8")))
    return _TX[str(n)]["figs"]


def items(s):
    """Склеенный в pptx нумерованный список «…:1. …2. …» → (вступление, [пункты]). Текст не меняется."""
    parts = re.split(r"(?:(?<=[^\d.][.;:!?»)])|(?<=[а-яa-z]))\s*(?=\d\.\s?[А-ЯA-Z«])", s)
    head_, rest = parts[0], parts[1:]
    if re.match(r"^\d\.\s?", head_):
        head_, rest = "", parts
    if not rest:
        return s, []
    return head_, [re.sub(r"^\d\.\s?", "", x).strip() for x in rest]


def bullets(s):
    """Пункты, склеенные через «•»."""
    return [x.strip() for x in s.split("•") if x.strip()]


def T(n, idx):
    """Терминал из расшифровки: фигура idx слайда n."""
    f = tx(n)[idx]
    L = [l for l in f["lines"] if "Рис." not in l and "Рисун" not in l and not l.startswith(("---", "(разрыв", "[разрыв"))]
    w = max(len(l) for l in L) if L else 0
    h = term(L)
    return h.replace('class="cli term"', 'class="cli term wide"') if w > 95 else h


def b64(name):
    if name not in _cache:
        with open(os.path.join(ADIR, name + ".webp"), "rb") as fh:
            _cache[name] = "data:image/webp;base64," + base64.b64encode(fh.read()).decode()
    return _cache[name]


def conf(lines, title=""):
    """Команды: приглашение (R1(config-if-gi)#) приглушено, команда подсвечена; прочие строки — как есть."""
    out = []
    for ln in lines:
        m = _PROMPT.match(ln)
        if m:
            out.append('<span class="p">%s</span><span class="k">%s</span>' % (_esc(m.group(1)), _esc(m.group(2))))
        else:
            out.append(_esc(ln))
    t = '<div class="clih">%s</div>' % _esc(title) if title else ""
    return '%s<pre class="cli">%s</pre>' % (t, "\n".join(out))


def tbl(cols, rows, hl=(), title=""):
    th = "".join("<th>%s</th>" % c for c in cols)
    tr = "".join('<tr%s>%s</tr>' % (' class="hl"' if i in hl else "", "".join("<td>%s</td>" % c for c in r))
                 for i, r in enumerate(rows))
    tt = '<div class="mt-t">%s</div>' % title if title else ""
    return '%s<div class="tw mt m4tbl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (tt, th, tr)


def fig(svg):
    return '<div class="figwrap m4p">%s</div>' % svg


def pack(text, per=850):
    """Разбить длинный абзац pptx на куски по границам предложений (текст не меняется)."""
    ss = re.split(r"(?<=[.!?…])\s+(?=[А-ЯA-Z«(])", text)
    out, cur = [], ""
    for s in ss:
        if cur and len(cur) + len(s) > per:
            out.append(cur)
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        out.append(cur)
    return out


def long_slides(label, title, texts, right=None, per=900, layout="g2", rights=None):
    """Текст слайда pptx целиком; если не влезает — несколько слайдов с тем же заголовком, по порядку.
    right — блоки справа на первом слайде; rights — список блоков по страницам."""
    if right or rights:
        per = min(per, 600)
    else:
        per = min(per, 1100)
    chunks = []
    for t_ in texts:
        chunks += pack(t_, per)
    pages, cur, n = [], [], 0
    for c in chunks:
        if cur and n + len(c) > per * 1.1:
            pages.append(cur)
            cur, n = [], 0
        cur.append(c)
        n += len(c)
    if cur:
        pages.append(cur)
    tones = ["cy", "mg", "lm", "am"]
    for i, pg in enumerate(pages):
        r = rights[i] if rights and i < len(rights) else (right if i == 0 else None)
        lab = label if i == 0 else "%s · %d" % (label, i + 1)
        left = [card("", p(c), tones[(i + j) % 4]) for j, c in enumerate(pg)]
        pslide(lab, title, left, r if r else None, layout)


def scn(svg, caps):
    """Пошаговая сцена (кнопки «Назад/Вперёд»): элементы с data-ph появляются по шагам."""
    from _sw_lib import scene
    return scene(svg, caps)


def card_list(title, intro, its, tone="cy"):
    body = (p(intro) if intro else "") + li(its)
    return card(title, body, tone)


def rep(name):
    import _m4_replib
    r = _m4_replib.rep_html(name)
    if r:
        return r
    return '<div class="pic"><img src="%s" alt="" loading="lazy"></div>' % b64(name)


def info(label, title, name):
    """Инфографика автора сразу за своим слайдом: вёрстка на чистом фоне (_m4_rep/<name>.py)."""
    slide(label, sc(head(title), grow("g", col(rep(name)))))


def pslide(label, title, left, right=None, layout="g2", sub=""):
    L = col(*[step(b) for b in left])
    body = grow("g", L) if right is None else grow(layout, L, col(*[step(b) for b in right]))
    slide(label, sc(head(title, sub), body))
