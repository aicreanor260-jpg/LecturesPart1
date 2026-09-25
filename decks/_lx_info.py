# -*- coding: utf-8 -*-
# Воссоздание инфографики из расшифровки (tr/imageN.json) вёрсткой: панели, терминалы, плашки.
import json, pathlib, re
from _lx_lib import *

TR = pathlib.Path(__file__).parent / "_lx_tr"  # расшифровки инфографик

_NOTE = re.compile(r"\s*[\(\[](?:icon|layout|orange|right|left|wide|code|title|plain|small|handwritten|tilted|as printed|printed|white|grey|gray|bold)[^\]\)]*[\]\)]?\s*$", re.I)
def _clean(b):
    for k in ("text", "info", "sub", "title"):
        v = b.get(k)
        if isinstance(v, str):
            v = _NOTE.sub("", v)
            v = re.sub(r"\s*\[(?:right|left|icon|small|orange|as printed)[^\]]*\]", "", v)
            v = re.sub(r"\s*\((?:icon|layout note|handwritten)[^)]*\)", "", v).strip()
            if k == "info" and re.match(r"^[a-z]", v): v = None
            b[k] = v
    return b
_LD = {}
def load(n):
    if n not in _LD:
        d = json.loads((TR / f"image{n}.json").read_text(encoding="utf-8"))
        d["blocks"] = [_clean(b) for b in d["blocks"]]
        _LD[n] = d
    return json.loads(json.dumps(_LD[n]))

_ICMAP = [("calendar", "calendar"), ("clock", "clock"), ("folder", "folder"), ("files", "files"), ("two", "files"), ("stack", "files"),
          ("file", "file"), ("document", "file"), ("server", "server"), ("rack", "server"), ("monitor", "monitor"), ("desktop", "desktop"),
          ("laptop", "desktop"), ("shield", "shield"), ("lock", "lock"), ("gear", "gear"), ("cog", "gear"), ("refresh", "refresh"),
          ("sync", "refresh"), ("bolt", "bolt"), ("lightning", "bolt"), ("code", "code"), ("</>", "code"), ("search", "search"),
          ("magnif", "search"), ("trash", "trash"), ("bin", "trash"), ("link", "link"), ("chain", "link"), ("download", "download"),
          ("users", "users"), ("group", "users"), ("people", "users"), ("user", "user"), ("person", "user"), ("globe", "globe"),
          ("cloud", "cloud"), ("cpu", "cpu"), ("processor", "cpu"), ("chip", "chip"), ("disk", "disk"), ("database", "disk"),
          ("storage", "disk"), ("list", "list"), ("eye", "eye"), ("terminal", "terminal"), ("copy", "copy"), ("check", "check"),
          ("cap", "grad"), ("graduat", "grad"), ("book", "book"), ("sort", "sort"), ("speaker", "echo"), ("sound", "echo"),
          ("broom", "broom"), ("log", "log"), ("move", "move"), ("arrow", "arrow"), ("pen", "pen"), ("hash", "hash"), ("key", "lock")]

def icon_for(desc, default="dot"):
    if not desc: return ICON[default]
    d = desc.lower()
    for k, v in _ICMAP:
        if k in d: return ICON[v]
    return ICON[default]

def T(s):
    return rich(s) if s else ""

def _is_cmd(t):
    return bool(t) and bool(re.fullmatch(r"[a-z][a-z0-9 _./-]{0,24}", t.strip())) and " " not in t.strip()[:6]

def render_card(b, arts=None, big=None):
    parts = []
    if b.get("text"): parts.append(f'<p class="t">{T(b["text"])}</p>')
    if b.get("bullets"): parts.append(bullets(b["bullets"], "sm"))
    for a in (arts or []): parts.append(a)
    if b.get("terminal"): parts.append(term(b["terminal"]))
    if b.get("info"):
        ic = icon_for(b.get("icon"), "dot") if b.get("icon") else ""
        if ic and b.get("terminal"):
            parts.append(f'<div class="foot"><span class="bigic">{ic}</span><div>{T(b["info"])}</div></div>')
        else:
            parts.append(info(b["info"]))
    if b.get("tag"):
        tg = b["tag"]; parts.append(f'<div>{tagpill(_ic_key(tg.get("icon")), T(tg.get("text")))}</div>')
    n = b.get("num"); title = T(b.get("title")); sub = T(b.get("sub"))
    if big is None: big = bool(n) and len(n) == 2 and _is_cmd(b.get("title") or "")
    if n and len(n) == 1:
        hd = f'<div class="stp">{circle(n)}<div><h3>{title}</h3>' + (f'<p>{sub}</p>' if sub else "") + '</div></div>'
        return card(hd + "".join(parts))
    return card("".join(parts), n, title, sub, big=big)

def _ic_key(desc):
    if not desc: return "dot"
    d = desc.lower()
    for k, v in _ICMAP:
        if k in d: return v
    return "dot"

def render_steps(b):
    out = []
    if b.get("title"): out.append(f'<h3 class="sec">{T(b["title"])}</h3>')
    items = b["items"]; cols = {1: "", 2: "g2", 3: "g3", 4: "g4"}.get(len(items), "g3")
    cards = []
    for it in items:
        body = f'<div class="stp">{circle(it.get("n",""))}<div><h3>{T(it.get("title"))}</h3>' + (f'<p>{T(it.get("text"))}</p>' if it.get("text") else "") + '</div></div>'
        if it.get("terminal"): body += term(it["terminal"])
        if it.get("note"):
            ic = icon_for(it.get("icon"), "check")
            body += f'<div class="foot"><span class="bigic">{ic}</span><div>{T(it["note"])}</div></div>'
        cards.append(card(body))
    out.append(f'<div class="{cols}">{"".join(cards)}</div>')
    return "".join(out)

def render_table(b):
    h = "".join(f"<th>{T(x)}</th>" for x in b.get("head", []))
    rows = "".join("<tr>" + "".join(f"<td>{T(str(c))}</td>" for c in r) + "</tr>" for r in b["rows"])
    return f'<div class="tw" data-s="1"><table class="tbl"><thead><tr>{h}</tr></thead><tbody>{rows}</tbody></table></div>'

def render_block(b, arts=None):
    t = b["type"]
    if t == "card": return render_card(b, arts)
    if t == "steps": return render_steps(b)
    if t == "syntax": return syntax([tuple(r) for r in b["rows"]])
    if t == "info": return info(b["text"], {"i": "i", "quote": "q", "warn": "w"}.get(b.get("kind"), "i"))
    if t == "table": return render_table(b)
    if t == "list":
        if not b.get("items"): return f'<h3 class="sec" data-s="1">{T(b.get("title"))}</h3>'
        return (f'<h3 class="sec" data-s="1">{T(b.get("title"))}</h3>' if b.get("title") else "") + bullets(b["items"])
    if t == "diagram":
        return card(f'<p class="t">{T(b.get("desc"))}</p>')
    raise ValueError(t)

def header(d):
    runs = []
    for x, c in d["title"]:
        if x == "|": continue
        cls = "o" if c == "o" else "w"
        if re.fullmatch(r"[a-z][a-z0-9 -]*", x): cls += " l"
        runs.append((x, cls))
    return head(runs, T(d.get("subtitle")), d.get("tag"))

def arts_of(n, d, idx=None, w=620):
    img = f"image{n}.png"; A = d.get("art", [])
    sel = range(len(A)) if idx is None else idx
    return [crop(img, A[i]["bbox"], w) for i in sel]

def infographic(n, *, hdr_art=0, card_art=None, side=None, cols=None, extra_after="", extra_before="", art_cls="", hide=(), label=None, top_split="tl2"):
    """Типовая раскладка: сверху заголовок+вводный текст слева и иллюстрация справа, ниже сетка карточек, внизу плашки.
    card_art = {индекс_карточки: индекс_art}; side = список блоков (индексы), которые уходят в правую колонку шапки."""
    d = load(n); A = d.get("art", []); img = f"image{n}.png"
    blocks = [b for i, b in enumerate(d["blocks"]) if i not in hide]
    card_art = card_art or {}
    # шапка
    left = [header(d)]
    if d.get("intro"): left.append(P(d["intro"], cls="p lg"))
    right = []
    if hdr_art is not None and hdr_art < len(A):
        right.append(art(crop(img, A[hdr_art]["bbox"], 700), art_cls))
    # блоки до первой карточки/шагов — в шапку
    i = 0; pre = []
    while i < len(blocks) and blocks[i]["type"] in ("syntax", "info") and not (blocks[i]["type"] == "info" and i > 0 and blocks[i-1]["type"] == "card"):
        pre.append(blocks[i]); i += 1
    for k, b in enumerate(pre):
        if side and k in side: right.append(render_block(b))
        else: left.append(render_block(b))
    top = f'<div class="{top_split}"><div class="col">{"".join(left)}</div><div class="col">{"".join(right)}</div></div>' if right else "".join(left)
    # основная часть
    rest = blocks[i:]; out = [top, extra_before]
    cards = [b for b in rest if b["type"] == "card"]
    ncols = cols or {1: "", 2: "g2", 3: "g3", 4: "g4", 5: "g5", 6: "g3", 8: "g4", 10: "g5"}.get(len(cards), "g3")
    ci = 0; buf = []
    def flush():
        if buf: out.append(f'<div class="{ncols} mt">{"".join(buf)}</div>'); buf.clear()
    for b in rest:
        if b["type"] == "card":
            aa = [art(crop(img, A[card_art[ci]]["bbox"], 460), "sm soft")] if ci in card_art else None
            buf.append(render_card(b, aa)); ci += 1
        else:
            flush(); out.append(f'<div class="mt">{render_block(b)}</div>')
    flush(); out.append(extra_after)
    return "".join(out)
