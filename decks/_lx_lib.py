# -*- coding: utf-8 -*-
# Библиотека деки «Linux»: стиль «оранжевая лампа», компоненты, движок.
import base64, io, json, pathlib, re, html
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).parent
PPTX = pathlib.Path(r"C:/Users/anank/Downloads/linux.pptx")  # исходник: картинки берутся из ppt/media

# ---------------------------------------------------------------- images
_cache = {}
def _img(name):
    if name not in _cache:
        import zipfile
        _cache[name] = Image.open(io.BytesIO(zipfile.ZipFile(PPTX).read("ppt/media/" + name))).convert("RGB")
    return _cache[name]

def b64(im, q=88, fmt="WEBP"):
    b = io.BytesIO(); im.save(b, fmt, quality=q, method=6)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()

def crop(name, box, w=620, q=88, erase=()):
    """Иллюстрация из инфографики (енот, пингвин, 3D-объекты) — вырезается как есть.
    erase — прямоугольники (в координатах исходника), закрашиваемые фоном: убрать попавший в кадр текст."""
    im = _img(name).crop(tuple(int(v) for v in box))
    if erase:
        from PIL import ImageDraw
        dr = ImageDraw.Draw(im)
        for x0, y0, x1, y1 in erase:
            dr.rectangle((x0 - box[0], y0 - box[1], x1 - box[0], y1 - box[1]), fill=(10, 10, 12))
        im = im.filter(ImageFilter.SMOOTH) if False else im
    if im.width > w or im.height > w:
        im.thumbnail((w, w), Image.LANCZOS)
    return b64(im, q)

def whole(name, w=1600, q=86):
    im = _img(name).copy(); im.thumbnail((w, w), Image.LANCZOS)
    return b64(im, q)

def esc(s):
    return html.escape(s, quote=False)

def rich(s):
    """<o>..</o> — оранжевое слово, <c>..</c> — моноширинный фрагмент."""
    if s is None: return ""
    s = s.replace("<o>", '<b class="o">').replace("</o>", "</b>")
    s = s.replace("<c>", '<code class="c">').replace("</c>", "</code>")
    return s

# ---------------------------------------------------------------- components
def head(runs, sub=None, tag=None):
    t = f'<span class="tag">{tag}</span>' if tag else ""
    h = " ".join(f'<span class="{c}">{x}</span>' for x, c in runs)
    s = f'<p class="sub">{sub}</p>' if sub else ""
    return f'<header class="sh">{t}<h2>{h}</h2>{s}</header>'

def P(*paras, cls="p"):
    return "".join(f'<p class="{cls}" data-s="1">{rich(t)}</p>' for t in paras)

def bullets(items, cls=""):
    return f'<ul class="bul {cls}">' + "".join(
        f'<li data-s="1" style="--dl:{i*70}ms">{rich(t)}</li>' for i, t in enumerate(items)) + '</ul>'

def defs(items, cls=""):
    """[(термин, пояснение)] — термин оранжевым моноширинным/жирным."""
    return f'<dl class="defs {cls}">' + "".join(
        f'<div class="df" data-s="1" style="--dl:{i*60}ms"><dt>{rich(a)}</dt><dd>{rich(b)}</dd></div>' for i, (a, b) in enumerate(items)) + '</dl>'

def num(n):
    return f'<span class="nm">{n}</span>'

def card(body, num_=None, title=None, sub=None, cls="", big=False, dl=None):
    nh = ""
    if big and num_:
        nh = f'<div class="ch big">{num(num_)}<div><h3 class="cmdh">{title}</h3>' + (f'<span class="cs">{sub}</span>' if sub else "") + '</div></div>'
    elif num_ or title:
        nb = f'<span class="nb">{num_}</span>' if num_ else ""
        nh = f'<div class="ch">{nb}<div>' + (f'<h3>{title}</h3>' if title else "") + (f'<span class="cs">{sub}</span>' if sub else "") + '</div></div>'
    st = f' style="--dl:{dl}ms"' if dl is not None else ""
    return f'<div class="card {cls}" data-s="1"{st}>{nh}{body}</div>'

def info(text, kind="i", cls=""):
    ic = {"i": '<span class="ii">i</span>', "q": '<span class="iq">“</span>', "w": '<span class="ii w">!</span>'}[kind]
    tail = '<span class="iq end">”</span>' if kind == "q" else ""
    return f'<div class="info {kind} {cls}" data-s="1">{ic}<div>{rich(text)}</div>{tail}</div>'

def syntax(rows, cls=""):
    r = "".join(f'<div class="sr"><span class="sl">{a}</span><code><b class="o">{esc(b)}</b> {esc(c)}</code></div>' for a, b, c in rows)
    return f'<div class="syn {cls}" data-s="1">{r}</div>'

def circle(n):
    return f'<span class="cn">{n}</span>'

def tagpill(icon, text):
    return f'<span class="pill">{ICON.get(icon, ICON["dot"])}<span>{text}</span></span>'

# --- terminal -----------------------------------------------------------
_PROMPT = re.compile(r"^([^@\s]+@[^:\s]+)(:)([^$#]*)([$#])$")
def _prompt(p):
    m = _PROMPT.match(p.strip())
    if not m: return f'<span class="pu">{esc(p)}</span>'
    u, c, path, d = m.groups()
    return f'<span class="pu">{esc(u)}{c}</span><span class="pp">{esc(path)}</span><span class="pu">{d}</span>'

def _cmd(cmd):
    parts = re.split(r"(\s+)", cmd)
    out, first = [], True
    for tok in parts:
        if not tok: continue
        if tok.isspace(): out.append(tok); continue
        if first: out.append(f'<span class="tc">{esc(tok)}</span>'); first = False
        elif tok.startswith("-") or re.fullmatch(r"[0-7]{3,4}|\d{8,}|[ugoa]*[+=-][rwx]+(,[ugoa]*[+=-][rwx]+)*", tok):
            out.append(f'<span class="tf">{esc(tok)}</span>')
        elif tok in ("|", ">", ">>", "&&"): out.append(f'<span class="tc">{esc(tok)}</span>')
        else: out.append(f'<span class="ta">{esc(tok)}</span>')
    return "".join(out)

def term(lines, title=None, cls="", cps=48):
    """lines: [{"p","cmd"} | {"out"} | {"ls":[..],"cols":n}]. Команды печатаются посимвольно при показе слайда."""
    t, rows = 0, []
    for ln in lines:
        if "cmd" in ln or "p" in ln:
            cmd = re.sub(r"</?o>", "", ln.get("cmd", "")).replace("█", "").rstrip(); n = max(1, len(cmd))
            dur = int(n * 1000 / cps)
            pr = ln.get("p") or ""
            rows.append(f'<div class="tl pl" style="--t:{t}ms">{_prompt(pr) + " " if pr else ""}<span class="ty" style="--n:{n};--tt:{dur}ms">{_cmd(cmd)}</span></div>')
            t += dur + 260
        elif "ls" in ln:
            cols = ln.get("cols", 4)
            items = "".join(f'<span class="{ "lx" if re.search(r"[.](txt|md|png|jpg|zip|pdf|mp4|c|sh|conf|cfg|log)$", x) and not ln.get("allblue") else "ld"}">{esc(x)}</span>' for x in ln["ls"])
            rows.append(f'<div class="tl lsg" style="--t:{t}ms;--cols:{cols}">{items}</div>')
            t += 160
        else:
            o = ln.get("out", "")
            rows.append(f'<div class="tl out" style="--t:{t}ms">{_out(o)}</div>')
            t += 120
    tt = f'<span class="tt">{title}</span>' if title else ""
    return (f'<div class="term {cls}" data-s="1" data-dur="{t}" style="--tb:__TB__ms"><div class="tbar"><i></i><i></i><i></i>{tt}</div>'
            f'<div class="tbody">{"".join(rows)}<span class="caret" style="--t:{t}ms"></span></div></div>')

def _out(o):
    e = esc(o).replace("&lt;o&gt;", '<span class="tc">').replace("&lt;/o&gt;", "</span>") if o else "&nbsp;"
    # права доступа в выводе ls -l — оранжевым
    e = re.sub(r"^([-dl][rwx-]{9})", r'<span class="tf">\1</span>', e)
    return e

def ls_out(items, cols=4):
    return {"ls": items, "cols": cols}

# --- art ------------------------------------------------------------------
def art(src, cls="", alt=""):
    return f'<figure class="art {cls}" data-s="1"><img src="{src}" alt="{alt}" decoding="async"></figure>'

def photo(src, cap=""):
    c = f'<figcaption>{cap}</figcaption>' if cap else ""
    return f'<figure class="card ph" data-s="1"><img src="{src}" alt="{cap or "Инфографика"}" decoding="async">{c}</figure>'

# --- icons (тонкий оранжевый контур) ----------------------------------------
def _i(d): return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true">{d}</svg>'
ICON = {
    "dot": _i('<circle cx="12" cy="12" r="4"/>'),
    "desktop": _i('<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/>'),
    "monitor": _i('<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4"/>'),
    "server": _i('<rect x="4" y="3" width="16" height="6" rx="1"/><rect x="4" y="11" width="16" height="6" rx="1"/><path d="M8 6h.01M8 14h.01M4 20h16"/>'),
    "shield": _i('<path d="M12 3l7 3v5c0 4.5-3 8.3-7 10-4-1.7-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>'),
    "gear": _i('<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>'),
    "refresh": _i('<path d="M20 11a8 8 0 0 0-14.9-3M4 13a8 8 0 0 0 14.9 3"/><path d="M4 4v4h4M20 20v-4h-4"/>'),
    "bolt": _i('<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>'),
    "code": _i('<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>'),
    "folder": _i('<path d="M3 6a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/>'),
    "file": _i('<path d="M6 2h8l5 5v15H6z"/><path d="M14 2v5h5"/>'),
    "files": _i('<path d="M8 2h7l4 4v12H8z"/><path d="M15 2v4h4M5 6v16h11"/>'),
    "clock": _i('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "calendar": _i('<rect x="3" y="5" width="18" height="16" rx="1.5"/><path d="M3 10h18M8 3v4M16 3v4M7 14h2M11 14h2M15 14h2M7 17h2M11 17h2"/>'),
    "terminal": _i('<rect x="3" y="4" width="18" height="16" rx="1.5"/><path d="M7 9l3 3-3 3M12 15h5"/>'),
    "search": _i('<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>'),
    "trash": _i('<path d="M4 7h16M9 7V4h6v3M6 7l1 14h10l1-14"/>'),
    "link": _i('<path d="M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1"/><path d="M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1"/>'),
    "download": _i('<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>'),
    "lock": _i('<rect x="5" y="11" width="14" height="10" rx="1.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>'),
    "user": _i('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
    "users": _i('<circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 13.5a7 7 0 0 1 4 6.5"/>'),
    "globe": _i('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
    "cpu": _i('<rect x="6" y="6" width="12" height="12" rx="1"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>'),
    "disk": _i('<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>'),
    "list": _i('<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>'),
    "eye": _i('<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>'),
    "pen": _i('<path d="M4 20l4-1L19 8l-3-3L5 16z"/>'),
    "play": _i('<path d="M7 4l12 8-12 8z"/>'),
    "book": _i('<path d="M4 4h6a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4zM20 4h-6a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h6z"/>'),
    "cloud": _i('<path d="M7 18a5 5 0 0 1-.6-10A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9z"/>'),
    "chip": _i('<rect x="6" y="6" width="12" height="12" rx="1"/><rect x="9" y="9" width="6" height="6"/>'),
    "grad": _i('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2 9 2 12 0v-5"/>'),
    "check": _i('<path d="M5 12l5 5 9-10"/>'),
    "x": _i('<path d="M6 6l12 12M18 6L6 18"/>'),
    "arrow": _i('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "copy": _i('<rect x="8" y="8" width="12" height="12" rx="1"/><path d="M16 8V4H4v12h4"/>'),
    "move": _i('<path d="M12 3v18M3 12h18M12 3l-3 3M12 3l3 3M12 21l-3-3M12 21l3-3M3 12l3-3M3 12l3 3M21 12l-3-3M21 12l-3 3"/>'),
    "sort": _i('<path d="M7 4v16M4 17l3 3 3-3M14 6h7M14 12h5M14 18h3"/>'),
    "hash": _i('<path d="M5 9h15M4 15h15M10 3L8 21M16 3l-2 18"/>'),
    "echo": _i('<path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16 9a4 4 0 0 1 0 6M19 6a8 8 0 0 1 0 12"/>'),
    "broom": _i('<path d="M14 3l-4 9M6 12h8l2 9H4z"/>'),
    "log": _i('<path d="M6 2h8l5 5v15H6z"/><path d="M9 12h7M9 16h7M9 8h3"/>'),
}

# ---------------------------------------------------------------- slides registry
S = []
def slide(label, body, cls=""):
    S.append((label, body, cls))

# ---------------------------------------------------------------- CSS
CSS = r"""
:root{--bg:#0a0a0c;--panel:#121316;--panel-2:#17181c;--edge:rgba(255,138,20,.28);--edge-hot:rgba(255,138,20,.75);
  --orange:#ff8a14;--orange-2:#ffb35c;--ember:#e2560f;--ink:#f4f1ec;--dim:#9b9691;--term-bg:#0d0f12;--term-blue:#5aa9e6;--term-green:#7fd66f;
  --f:"Segoe UI Variable Text","Segoe UI","Inter","Helvetica Neue",Arial,system-ui,sans-serif;
  --fh:"Segoe UI Black","Segoe UI","Inter","Arial Black",system-ui,sans-serif;
  --mono:"JetBrains Mono","Cascadia Mono","Cascadia Code","Consolas","DejaVu Sans Mono",ui-monospace,monospace;
  --ez:cubic-bezier(.22,.7,.3,1);color-scheme:dark}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:clamp(13px,min(1vw,1.8vh),27px)}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--ink);font-family:var(--f)}
code,.mono{font-family:var(--mono)}
b{font-weight:700}.o{color:var(--orange)}
/* ---- фон: свечение + перспективная сетка + искры ---- */
#deco{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
#deco i{position:absolute;border-radius:50%;filter:blur(70px);background:var(--ember)}
#deco i:nth-child(1){width:46vw;height:30vw;left:-10vw;top:-14vw;opacity:.28}
#deco i:nth-child(2){width:40vw;height:34vw;right:-12vw;top:18vh;opacity:.22}
#deco i:nth-child(3){width:60vw;height:18vw;left:20vw;bottom:-10vw;opacity:.3;background:#ff8a14}
#deco svg{position:absolute;left:0;bottom:0;width:100%;height:46%;opacity:.12}
#deco svg line{stroke:#ff8a14;stroke-width:1}
#deco u{position:absolute;width:3px;height:3px;border-radius:50%;background:#ffb35c;box-shadow:0 0 6px 2px rgba(255,138,20,.8)}
#prog{position:fixed;left:0;top:0;height:3px;width:100%;z-index:30;background:rgba(255,138,20,.12)}
#prog i{display:block;height:100%;width:0;background:var(--orange);box-shadow:0 0 10px var(--orange);transition:width .3s var(--ez)}
/* ---- каркас ---- */
.slide{position:fixed;inset:0;z-index:1;display:none}.slide.on{display:block}
.sc{height:100%;overflow-y:auto;overflow-x:hidden;display:flex;flex-direction:column;padding:clamp(18px,4.2vh,56px) clamp(16px,4.2vw,90px) calc(4.6rem + 12px);scrollbar-width:thin;scrollbar-color:var(--edge) transparent}
.wrap{margin:auto;width:100%;max-width:104rem;position:relative}
.sh{margin-bottom:1.25rem;position:relative;z-index:2}
.tag{display:inline-block;border:1px solid var(--edge);border-radius:6px;font-size:11px;letter-spacing:.14em;padding:.35em .9em;color:var(--ink);text-transform:uppercase;margin-bottom:.8rem;background:rgba(18,19,22,.6)}
h2{font-family:var(--fh);font-size:3.1rem;line-height:1;font-weight:900;letter-spacing:-.02em;text-transform:uppercase;color:var(--ink)}
h2 .o{color:var(--orange);text-shadow:0 0 28px rgba(255,138,20,.35)}
h2 .l{text-transform:none}
.sub{font-size:1.3rem;color:var(--dim);margin-top:.45rem;line-height:1.35}
h3{font-size:1.12rem;font-weight:800;line-height:1.25;color:var(--ink)}
.p{font-size:1.14rem;line-height:1.55;margin-bottom:.8rem;max-width:72ch;color:#e3ded7}
.p.lg{font-size:1.3rem;max-width:none}.p.sm{font-size:1rem}
.dim{color:var(--dim)}
code.c{font-family:var(--mono);color:var(--orange);font-size:.95em}
/* ---- сетки ---- */
.g2,.g3,.g4,.g5,.two,.tl2,.tr2{display:grid;grid-template-columns:minmax(0,1fr);gap:1rem}
.two{gap:1.4rem 2.2rem;align-items:center}
.col{display:flex;flex-direction:column;gap:1rem}
.mt{margin-top:1rem}.mt2{margin-top:1.6rem}
.sec{font-size:1rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;margin:1.3rem 0 .7rem;color:var(--ink)}
/* ---- карточки ---- */
.card{position:relative;background:var(--panel);border:1px solid var(--edge);border-radius:12px;padding:1.1rem 1.2rem;
  background-image:radial-gradient(120% 60% at 50% -10%,rgba(255,138,20,.12),transparent 60%);box-shadow:0 0 0 1px rgba(0,0,0,.4),0 10px 40px rgba(0,0,0,.35);transition:border-color .25s,box-shadow .25s}
.card:hover{border-color:var(--edge-hot);box-shadow:0 0 24px rgba(255,138,20,.18)}
.card.hot{border-color:var(--edge-hot);box-shadow:0 0 30px rgba(255,138,20,.22)}
.card.flat{background-image:none}
.card>*+*{margin-top:.75rem}
.ch{display:flex;gap:.8rem;align-items:flex-start}
.ch h3{margin-top:.1rem}
.cs{display:block;color:var(--orange);font-weight:700;font-size:.98rem;margin-top:.15rem}
.nb{flex:none;display:inline-grid;place-items:center;min-width:2.1em;height:2.1em;border:1px solid var(--edge-hot);border-radius:6px;color:var(--orange);font-weight:800;font-family:var(--mono);font-size:.95rem;background:rgba(255,138,20,.08)}
.ch.big{align-items:center;gap:1rem;padding-bottom:.75rem;border-bottom:1px solid var(--edge)}
.nm{font-family:var(--fh);font-size:3.3rem;font-weight:900;line-height:.9;color:var(--orange);letter-spacing:-.03em;padding-right:1rem;border-right:1px solid var(--edge)}
.cmdh{font-family:var(--mono);font-size:1.9rem;font-weight:700;text-transform:none}
.card .t{font-size:1.02rem;line-height:1.5;color:#e3ded7}
.card .t.sm{font-size:.93rem}
.pill{display:inline-flex;align-items:center;gap:.6rem;border:1px solid var(--edge-hot);border-radius:8px;padding:.45rem .9rem;font-size:.9rem;background:rgba(10,10,12,.55)}
.ic{width:1.35em;height:1.35em;flex:none;fill:none;stroke:var(--orange);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.bigic .ic{width:3rem;height:3rem;stroke-width:1.3;filter:drop-shadow(0 0 8px rgba(255,138,20,.5))}
.cn{flex:none;display:inline-grid;place-items:center;width:2.3rem;height:2.3rem;border:1.5px solid var(--orange);border-radius:50%;color:var(--orange);font-weight:800;font-size:1.15rem;background:transparent}
.stp{display:flex;gap:.8rem;align-items:flex-start}.stp h3{color:var(--orange)}.stp p{font-size:.95rem;line-height:1.45;color:#dcd6ce;margin-top:.25rem}
.foot{display:flex;gap:.9rem;align-items:center;font-size:.95rem;line-height:1.4}
/* ---- списки ---- */
.bul{list-style:none;display:flex;flex-direction:column;gap:.6rem}
.bul li{position:relative;padding-left:1.4rem;font-size:1.08rem;line-height:1.5}
.bul li::before{content:"";position:absolute;left:0;top:.55em;width:.5em;height:.5em;border-radius:2px;background:var(--orange);box-shadow:0 0 8px rgba(255,138,20,.7)}
.bul.sm li{font-size:.96rem}
.defs{display:grid;grid-template-columns:minmax(0,1fr);gap:.55rem}
.df{display:grid;grid-template-columns:minmax(9rem,max-content) minmax(0,1fr);gap:1rem;align-items:baseline;padding:.6rem .9rem;background:var(--panel);border:1px solid var(--edge);border-radius:10px}
.df dt{font-family:var(--mono);color:var(--orange);font-weight:700;font-size:1rem}
.df dd{font-size:.98rem;line-height:1.45;color:#e3ded7}
.defs.words .df dt{font-family:var(--f);font-weight:800}
/* ---- терминал ---- */
.term{background:var(--term-bg);border:1px solid rgba(255,255,255,.08);border-radius:8px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,.5),0 0 0 1px rgba(255,138,20,.06)}
.tbar{display:flex;align-items:center;gap:7px;padding:9px 12px;background:#15171b;border-bottom:1px solid rgba(255,255,255,.06)}
.tbar i{width:11px;height:11px;border-radius:50%;background:#ff5f57}.tbar i:nth-child(2){background:#febc2e}.tbar i:nth-child(3){background:#28c840}
.tt{margin-left:auto;margin-right:auto;font-family:var(--mono);font-size:12px;color:var(--dim);transform:translateX(-22px)}
.tbody{padding:.8rem 1rem .9rem;font-family:var(--mono);font-size:14px;line-height:1.55;color:var(--ink);white-space:pre;overflow-x:auto;position:relative}
.big-t .tbody{font-size:16px}
.pu{color:#cfcac3}.pp{color:var(--orange)}
.tc{color:var(--orange)}.tf{color:var(--orange-2)}.ta{color:var(--ink)}
.lsg{display:grid;grid-template-columns:repeat(var(--cols),max-content);column-gap:2.2em}
.ld{color:var(--term-blue)}.lx{color:var(--ink)}
.ty{display:inline-block;vertical-align:bottom;white-space:pre;overflow:hidden}
.caret{display:inline-block;width:.6em;height:1.1em;background:var(--orange);vertical-align:text-bottom;opacity:0}
/* печать команд: включается классом .go на слайде */
.go .term .tl{animation:tlIn .01s linear both;animation-delay:calc(var(--tb) + var(--t))}
.go .term .ty{animation:type var(--tt) steps(var(--n)) both;animation-delay:calc(var(--tb) + var(--t))}
.go .term .caret{animation:blink 1s steps(1) infinite;animation-delay:calc(var(--tb) + var(--t))}
@keyframes tlIn{from{visibility:hidden}to{visibility:visible}}
@keyframes type{from{max-width:0}99%{max-width:calc(var(--n) * 1ch)}to{max-width:none}}
@keyframes blink{0%{opacity:1}50%{opacity:0}}
/* ---- инфо / цитата ---- */
.info{display:flex;gap:1rem;align-items:center;background:var(--panel-2);border:1px solid var(--edge);border-radius:10px;padding:.8rem 1.1rem;font-size:1rem;line-height:1.45}
.ii{flex:none;display:inline-grid;place-items:center;width:2.2rem;height:2.2rem;border-radius:50%;background:var(--orange);color:#fff;font-family:Georgia,serif;font-weight:900;font-style:italic;font-size:1.25rem;box-shadow:0 0 16px rgba(255,138,20,.55)}
.ii.w{font-style:normal;font-family:var(--f)}
.iq{flex:none;font-family:Georgia,serif;font-size:3rem;line-height:.6;color:var(--orange);font-weight:900;align-self:flex-start;padding-top:.5rem}
.iq.end{align-self:flex-end;padding:0 0 .1rem}
.info.q{font-size:1.2rem}
/* ---- синтаксис ---- */
.syn{border:1px solid var(--edge);border-radius:10px;background:rgba(18,19,22,.75);overflow:hidden}
.sr{display:grid;grid-template-columns:8.5rem minmax(0,1fr);gap:1rem;padding:.7rem 1.1rem;align-items:baseline}
.sr+.sr{border-top:1px solid var(--edge)}
.sl{color:var(--orange);font-weight:800}
.syn code{font-size:1.08rem;color:var(--ink);white-space:pre-wrap;word-break:break-all}
/* ---- иллюстрации из инфографик ---- */
.art{margin:0;display:grid;place-items:center;position:relative}
.art img{display:block;max-width:100%;height:auto;max-height:62vh;
  -webkit-mask-image:radial-gradient(ellipse 72% 70% at 50% 50%,#000 58%,transparent 100%);mask-image:radial-gradient(ellipse 72% 70% at 50% 50%,#000 58%,transparent 100%)}
.art.soft img{-webkit-mask-image:radial-gradient(ellipse 60% 60% at 50% 50%,#000 45%,transparent 100%);mask-image:radial-gradient(ellipse 60% 60% at 50% 50%,#000 45%,transparent 100%)}
.art.raw img{-webkit-mask-image:none;mask-image:none;border-radius:10px}
.art.sm img{max-height:34vh}.art.xs img{max-height:22vh}.art.lg img{max-height:74vh}
.logo img{-webkit-mask-image:none;mask-image:none;border-radius:8px;max-height:9rem}
.ph{padding:.5rem;margin:0}.ph img{display:block;width:100%;height:auto;max-height:66vh;object-fit:contain;border-radius:8px;cursor:zoom-in}
.ph figcaption{font-size:.85rem;color:var(--dim);padding:.45rem .3rem 0}
#lb{position:fixed;inset:0;z-index:80;background:rgba(6,6,8,.96);display:grid;place-items:center;padding:12px;cursor:zoom-out}#lb[hidden]{display:none}#lb img{max-width:100%;max-height:100%;object-fit:contain}
/* ---- таблица ---- */
.tw{overflow-x:auto;border:1px solid var(--edge);border-radius:12px;background:var(--panel)}
.tbl{width:100%;border-collapse:collapse;font-size:1rem}
.tbl th,.tbl td{text-align:left;padding:.55rem .9rem;border-bottom:1px solid rgba(255,138,20,.14);vertical-align:top}
.tbl thead th{color:var(--orange);font-weight:800;text-transform:uppercase;font-size:.8rem;letter-spacing:.08em}
.tbl td:first-child{font-family:var(--mono);color:var(--orange-2)}
.tbl tr:last-child td{border-bottom:0}
.tbl .m{font-family:var(--mono)}
/* ---- reveal ---- */
[data-s]{opacity:0;transform:translateY(12px);transition:opacity 320ms var(--ez) var(--dl,0ms),transform 320ms var(--ez) var(--dl,0ms),border-color .25s,box-shadow .25s}
[data-s].in{opacity:1;transform:none}
.ni,.ni *{transition:none!important}
/* ---- титул ---- */
.tslide .sc{padding:0}.tslide .wrap{max-width:none;height:100%;margin:0}
.title{height:100%;display:grid;grid-template-columns:minmax(0,1fr);align-items:center;padding:0 clamp(16px,7vw,150px);gap:1rem}
.title h1{font-family:var(--fh);font-size:clamp(3.4rem,10vw,9.5rem);line-height:.9;font-weight:900;letter-spacing:-.03em;text-transform:uppercase}
.title h1 .o{color:var(--orange);text-shadow:0 0 50px rgba(255,138,20,.45)}
.title .lead{font-size:1.5rem;color:var(--dim);margin:1rem 0 2rem;max-width:30ch;line-height:1.35}
.authors{font-size:1.05rem;line-height:1.7;color:var(--ink)}
.authors span{color:var(--dim)}
/* ---- слои архитектуры ---- */
.layers{display:flex;flex-direction:column;gap:.55rem}
.lay{display:grid;grid-template-columns:3.4rem minmax(0,1fr);gap:1rem;align-items:center;padding:.8rem 1rem;border:1px solid var(--edge);border-radius:10px;background:var(--panel);position:relative}
.lay .ic{width:2.4rem;height:2.4rem}
.lay b{display:block;font-size:1.08rem;margin-bottom:.15rem}
.lay span{font-size:.93rem;color:#d9d3cb;line-height:1.4}
.lay.core{border-color:var(--edge-hot);box-shadow:0 0 26px rgba(255,138,20,.25)}
/* ---- дерево каталогов ---- */
.tree{font-family:var(--mono);font-size:1rem;line-height:1.75}
.tree .d{color:var(--term-blue)}.tree .r{color:var(--orange);font-weight:700}
.tree .x{color:var(--dim);font-family:var(--f);font-size:.9rem}
/* ---- права ---- */
.perm{display:flex;gap:.3rem;font-family:var(--mono);font-size:2.2rem;font-weight:700;flex-wrap:wrap}
.perm span{display:inline-grid;place-items:center;width:1.4em;height:1.6em;border:1px solid var(--edge);border-radius:6px;background:var(--term-bg)}
.perm .ft{color:var(--term-blue)}.perm .u{color:var(--orange)}.perm .g{color:var(--orange-2)}.perm .t{color:var(--ink)}
.perm .gap{border:0;background:none;width:.4em}
.plab{display:flex;gap:.3rem;font-size:.85rem;color:var(--dim);flex-wrap:wrap}
.calc{display:grid;grid-template-columns:auto repeat(3,minmax(0,1fr));gap:.5rem .8rem;align-items:center}
.calc .hd{font-weight:800;color:var(--orange);text-align:center;font-size:.95rem}
.calc label{display:flex;justify-content:center}
.calc input{width:1.6rem;height:1.6rem;accent-color:var(--orange);cursor:pointer}
.calc .rl{font-family:var(--mono);font-weight:700}
.cres{display:flex;gap:1.5rem;flex-wrap:wrap;align-items:baseline;margin-top:.9rem}
.cres b{font-family:var(--mono);font-size:2.4rem;color:var(--orange)}
.cres span{font-family:var(--mono);font-size:1.6rem}
.btn{font:inherit;font-size:.92rem;font-weight:700;padding:.55rem 1rem;border:1px solid var(--edge-hot);border-radius:8px;background:rgba(18,19,22,.9);color:var(--ink);cursor:pointer;transition:background .15s,border-color .15s}
.btn:hover{background:rgba(255,138,20,.14)}.btn:active{background:rgba(255,138,20,.28)}
.btn.pri{background:var(--orange);color:#140900;border-color:var(--orange)}
.btn:focus-visible,.opt:focus-visible,#nav button:focus-visible,.ovi:focus-visible,input:focus-visible{outline:2px solid var(--orange-2);outline-offset:2px}
.opts{display:grid;grid-template-columns:minmax(0,1fr);gap:.55rem}
.opt{font:inherit;text-align:left;font-size:1rem;padding:.7rem 1rem;border:1px solid var(--edge);border-radius:10px;background:var(--panel-2);color:var(--ink);cursor:pointer}
.opt:hover{border-color:var(--edge-hot)}
.opt.ok{border-color:var(--term-green);background:rgba(127,214,111,.12)}.opt.no{border-color:#ff5f57;background:rgba(255,95,87,.12)}
.tq{font-size:1.3rem;line-height:1.4;margin-bottom:1rem}
.tres{min-height:2.6rem;font-size:1rem;line-height:1.45;margin:.6rem 0 .8rem}.tres.ok{color:var(--term-green)}.tres.no{color:#ff8a80}
.qtop{display:flex;justify-content:space-between;color:var(--dim);margin-bottom:.6rem;font-family:var(--mono)}
.trow{display:flex;gap:.7rem;flex-wrap:wrap}
/* ---- навигация ---- */
#nav{position:fixed;z-index:40;left:50%;bottom:12px;transform:translateX(-50%);display:flex;align-items:center;gap:.3rem;background:rgba(14,14,17,.92);border:1px solid var(--edge);border-radius:10px;padding:.35rem .5rem;font-size:14px}
#nav button{font:inherit;font-size:13px;font-weight:700;border:0;border-radius:6px;background:transparent;color:var(--ink);padding:.42rem .65rem;cursor:pointer;display:inline-flex;align-items:center;gap:.35rem}
#nav button:hover{background:rgba(255,138,20,.14)}#nav button:disabled{opacity:.35}
#nav svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}
.nsep{width:1px;height:22px;background:var(--edge);margin:0 .2rem}
#ind{font-family:var(--mono);font-size:13px;padding:0 .4rem;white-space:nowrap}
#ov{position:fixed;inset:0;z-index:60;background:rgba(8,8,10,.97);overflow:auto;padding:clamp(16px,5vh,60px) clamp(16px,6vw,120px)}
#ov h2{margin-bottom:1.2rem;font-size:2rem}
.ovg{display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:.6rem}
.ovi{font:inherit;text-align:left;display:flex;gap:.8rem;align-items:center;padding:.7rem .9rem;background:var(--panel);border:1px solid var(--edge);border-radius:10px;cursor:pointer;color:var(--ink);font-size:.95rem}
.ovi:hover,.ovi.cur{border-color:var(--edge-hot)}.ovi .mono{color:var(--orange);font-weight:800;width:2rem}
@media (min-width:768px){.g2{grid-template-columns:repeat(2,minmax(0,1fr))}.g3{grid-template-columns:repeat(3,minmax(0,1fr))}.g4{grid-template-columns:repeat(2,minmax(0,1fr))}.g5{grid-template-columns:repeat(3,minmax(0,1fr))}
  .title{grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr)}}
@media (min-width:1200px){.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.g5{grid-template-columns:repeat(5,minmax(0,1fr))}
  .two{grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr)}.tl2{grid-template-columns:minmax(0,1.35fr) minmax(0,.65fr);align-items:center}.tr2{grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr);align-items:center}
  .defs.c2{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:767px){html{font-size:15px}h2{font-size:1.9rem}.sub{font-size:1.05rem}.sc{padding-bottom:8rem}.nm{font-size:2.4rem}.cmdh{font-size:1.4rem}
  .df{grid-template-columns:minmax(0,1fr);gap:.2rem}.tbody{font-size:12.5px}#nav{flex-wrap:wrap;justify-content:center;width:calc(100% - 32px)}.lbl2{display:none}
  .title h1{font-size:3.4rem}.perm{font-size:1.5rem}.sr{grid-template-columns:minmax(0,1fr);gap:.2rem}}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation-duration:.01ms!important;animation-delay:0ms!important}}
"""

def deco():
    lines = []
    # перспективная сетка: горизонт вверху svg, линии сходятся к центру
    for k in range(-14, 15):
        lines.append(f'<line x1="{500 + k*18}" y1="0" x2="{500 + k*140}" y2="400"/>')
    y = 4
    while y < 400:
        lines.append(f'<line x1="0" y1="{y:.1f}" x2="1000" y2="{y:.1f}"/>'); y = y * 1.45 + 6
    sparks = [(8, 22), (17, 64), (29, 12), (41, 80), (57, 30), (66, 71), (74, 16), (83, 55), (91, 84), (95, 34), (36, 48), (52, 90)]
    sp = "".join(f'<u style="left:{x}%;top:{y}%;opacity:{.35 + (i % 4) * .15:.2f}"></u>' for i, (x, y) in enumerate(sparks))
    return ('<div id="deco" aria-hidden="true"><i></i><i></i><i></i>'
            f'<svg viewBox="0 0 1000 400" preserveAspectRatio="none">{"".join(lines)}</svg>{sp}</div>')

JS = r"""
(function(){
'use strict';
var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
var slides=$$('.slide'), N=slides.length, cur=0, tm=null;
function show(sl,instant){
  var els=$$('[data-s]',sl);
  if(instant){ sl.classList.add('ni'); els.forEach(function(e){e.classList.add('in')}); void sl.offsetWidth; sl.classList.remove('ni'); return; }
  els.forEach(function(e){e.classList.remove('in')}); sl.classList.remove('go'); void sl.offsetWidth;
  tm=setTimeout(function(){ els.forEach(function(e){e.classList.add('in')}); sl.classList.add('go'); },60);
}
function play(){ clearTimeout(tm); show(slides[cur],false); }
function go(i){
  i=Math.max(0,Math.min(N-1,i)); clearTimeout(tm);
  slides.forEach(function(s){s.classList.remove('on','go')}); cur=i; var sl=slides[cur]; sl.classList.add('on');
  var sc=$('.sc',sl); if(sc) sc.scrollTop=0;
  fit(sl); play();
  try{ history.replaceState(null,'','#'+(cur+1)); }catch(e){}
  $('#ind').textContent=(cur+1)+' / '+N; $('#prog i').style.width=((cur+1)/N*100)+'%';
  $('#b-prev').disabled=cur===0; $('#b-next').disabled=cur===N-1;
}
/* вписать слайд в экран: на широких экранах уменьшаем масштаб, на телефоне — прокрутка */
function fit(sl){
  var w=$('.wrap',sl), sc=$('.sc',sl); if(!w||!sc) return; w.style.zoom='';
  if(window.innerWidth<900) return;
  var cs=getComputedStyle(sc), P=parseFloat(cs.paddingTop)+parseFloat(cs.paddingBottom), C=sc.scrollHeight-P, H=sc.clientHeight-P;
  if(C>H+2) w.style.zoom=Math.max(.55,H/C*.99).toFixed(3);
}
var rzT=null; window.addEventListener('resize',function(){ clearTimeout(rzT); rzT=setTimeout(function(){ fit(slides[cur]); },120); });
function next(){ if(cur<N-1) go(cur+1); } function prev(){ if(cur>0) go(cur-1); }
$('#b-prev').onclick=prev; $('#b-next').onclick=next; $('#b-play').onclick=play;
var ov=$('#ov'), ovg=$('.ovg',ov);
slides.forEach(function(s,k){ var b=document.createElement('button'); b.className='ovi'; b.type='button';
  b.innerHTML='<span class="mono">'+(k+1)+'</span><span></span>'; b.lastChild.textContent=s.dataset.label;
  b.onclick=function(){ ov.hidden=true; go(k); }; ovg.appendChild(b); });
function openOv(){ ov.hidden=false; $$('.ovi',ov).forEach(function(b,k){b.classList.toggle('cur',k===cur)}); var c=$('.ovi.cur',ov); if(c)c.focus(); }
$('#b-ov').onclick=openOv;
var lb=$('#lb'); $$('.ph img').forEach(function(im){ im.addEventListener('click',function(){ $('img',lb).src=im.src; lb.hidden=false; }); });
lb.onclick=function(){ lb.hidden=true; };
var dbuf='', dtm=null;
document.addEventListener('keydown',function(e){
  var t=e.target, tag=t.tagName;
  if(e.ctrlKey||e.metaKey||e.altKey) return;
  if(tag==='INPUT'&&t.type!=='checkbox'&&t.type!=='range') return;
  if(!lb.hidden){ if(e.key==='Escape'||e.key===' '||e.key==='Enter'){ e.preventDefault(); lb.hidden=true; } return; }
  if(e.key==='Escape'){ e.preventDefault(); ov.hidden?openOv():(ov.hidden=true); return; }
  if(!ov.hidden) return;
  switch(e.key){
    case 'ArrowRight': case 'ArrowDown': case 'PageDown': e.preventDefault(); next(); return;
    case 'ArrowLeft': case 'ArrowUp': case 'PageUp': e.preventDefault(); prev(); return;
    case ' ': if(tag==='BUTTON'||tag==='INPUT') return; e.preventDefault(); next(); return;
    case 'Home': e.preventDefault(); go(0); return;
    case 'End': e.preventDefault(); go(N-1); return;
  }
  var k=e.key.toLowerCase(); if(k==='r'||k==='к'){ play(); return; }
  if(/^[0-9]$/.test(e.key)){ dbuf+=e.key; clearTimeout(dtm); dtm=setTimeout(function(){ var n=parseInt(dbuf,10); dbuf=''; if(n>=1&&n<=N) go(n-1); },550); }
});
var lastWheel=0;
window.addEventListener('wheel',function(e){
  if(!ov.hidden) return; var sc=$('.sc',slides[cur]); if(!sc) return; var dy=e.deltaY; if(Math.abs(dy)<4) return;
  if(dy>0 && sc.scrollTop+sc.clientHeight<sc.scrollHeight-2) return; if(dy<0 && sc.scrollTop>0) return;
  if(e.target.closest&&e.target.closest('.tbody,.tw')&&Math.abs(e.deltaX)>Math.abs(dy)) return;
  var now=Date.now(); if(now-lastWheel<420) return; lastWheel=now; dy>0?next():prev();
},{passive:true});
var tx=0,ty=0,tt=0;
window.addEventListener('touchstart',function(e){ var p=e.changedTouches[0]; tx=p.clientX; ty=p.clientY; tt=Date.now(); },{passive:true});
window.addEventListener('touchend',function(e){ var p=e.changedTouches[0], dx=p.clientX-tx, dy=p.clientY-ty;
  if(Date.now()-tt>700||Math.abs(dx)<60||Math.abs(dx)<Math.abs(dy)*1.4) return; if(e.target.closest&&e.target.closest('.tbody,.tw,input')) return; dx<0?next():prev(); },{passive:true});
__EXTRA__
window.addEventListener('hashchange',function(){ var n=parseInt((location.hash||'').slice(1),10); if(n>=1&&n<=N&&n-1!==cur) go(n-1); });
var h=parseInt((location.hash||'').slice(1),10);
go(h>=1&&h<=N?h-1:0);
})();
"""

ICON_L = '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>'
ICON_R = '<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>'

def _stagger(body):
    """Терминалы на слайде печатаются друг за другом: подставляем базовую задержку."""
    clock = [650]
    def rep(m):
        dur = int(m.group(1)); base = clock[0]; clock[0] += 380
        return f'data-dur="{dur}" style="--tb:{base}ms"'
    return re.sub(r'data-dur="(\d+)" style="--tb:__TB__ms"', rep, body)

def _auto_dl(body):
    """Каскад появления: каждому [data-s] без явного --dl — задержка по порядку."""
    k = [0]
    def rep(m):
        k[0] += 1
        if "--dl" in m.group(0): return m.group(0)
        return m.group(0).replace('data-s="1"', f'data-s="1" style="--dl:{min(k[0]*55, 900)}ms"', 1) if 'style="' not in m.group(0) else m.group(0)
    return re.sub(r'<[a-z0-9]+ [^>]*data-s="1"[^>]*>', rep, body)

def render(out_path, title, extra_js=""):
    out = ['<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
           f'<title>{title}</title><style>' + CSS + '</style></head><body>' + deco() + '<div id="prog"><i></i></div><main>']
    for label, body, cls in S:
        out.append(f'<section class="slide {cls}" data-label="{label}"><div class="sc"><div class="wrap">{_auto_dl(_stagger(body))}</div></div></section>')
    out.append('</main><nav id="nav" aria-label="Навигация">'
               f'<button id="b-prev" type="button" aria-label="Предыдущий слайд">{ICON_L}</button><span id="ind"></span>'
               f'<button id="b-next" type="button" aria-label="Следующий слайд">{ICON_R}</button><span class="nsep"></span>'
               '<button id="b-play" type="button" title="Клавиша R"><svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 0 2.5-5.8M4 4v5h5"/></svg><span class="lbl2">Повторить анимацию</span></button>'
               '<button id="b-ov" type="button" title="Esc"><svg viewBox="0 0 24 24"><path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z"/></svg><span class="lbl2">Содержание</span></button></nav>'
               '<div id="lb" hidden role="dialog" aria-label="Изображение во весь экран"><img alt=""></div><div id="ov" hidden><h2>Содержание</h2><div class="ovg"></div></div>')
    out.append('<script>' + JS.replace("__EXTRA__", extra_js) + '</script></body></html>')
    pathlib.Path(out_path).write_text("".join(out), encoding="utf-8")
    print(len(S), "slides", pathlib.Path(out_path).stat().st_size, "bytes")
