# -*- coding: utf-8 -*-
"""Автосборка слайдов деки прямо из pptx (порядок слайдов = порядок pptx, текст дословно):
заголовок слайда — из плейсхолдера title; каждая текстовая фигура — свой блок; маркированные абзацы — список;
строки с приглашением CLI (R1#, SW1(config)#, console# …) — блок конфигурации; маленькие картинки pptx (схемы, консоль) —
панель рядом с текстом; большие (инфографики автора) — во весь слайд сразу за своим слайдом.
Перегруженный слайд делится на несколько с тем же заголовком (· 2, · 3)."""
import html
import io
import os
import re
import zipfile

from _sw_lib import slide, sc, head, grow, col, step, card, _esc
import _pt_kit as K

HERE = os.path.dirname(os.path.abspath(__file__))
BIG = 1000000                       # инфографика автора — больше 1 МБ
_PROMPT = re.compile(r"^\s*[\w.\-]+(\([\w\-]+\))?#")


def _runs(p):
    out = []
    for r in re.findall(r"<a:r>.*?</a:r>|<a:br/>", p, re.S):
        if r == "<a:br/>":
            out.append("\n")
            continue
        t = html.unescape("".join(re.findall(r"<a:t>([^<]*)</a:t>", r)))
        if not t:
            continue
        b = re.search(r'<a:rPr[^>]*\sb="1"', r) is not None
        out.append(("<b>%s</b>" % _esc(t)) if b and t.strip() else _esc(t))
    s = "".join(out).replace("</b><b>", "")
    # колонтитул учебника, попавший в текст pptx («…60АкадемияЕLTEх…»), — убираем (вопрос автору в списке)
    return re.sub(r"\d{0,3}\s*Академия\s*[EЕ][LlЛл][TtТт][EeЕе][XxХх]\)?", " ", s)


def parse(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    slides = sorted([n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=lambda n: int(re.findall(r"\d+", n)[-1]))
    out = []
    for s in slides:
        x = z.read(s).decode("utf8")
        rels = {}
        rp = s.replace("slides/", "slides/_rels/") + ".rels"
        if rp in names:
            for m in re.finditer(r'Id="([^"]+)"[^>]*Target="([^"]+)"', z.read(rp).decode("utf8")):
                rels[m.group(1)] = m.group(2)
        title, shapes, imgs = "", [], []
        for sp in re.findall(r"<p:sp>.*?</p:sp>", x, re.S):
            is_title = re.search(r'<p:ph[^>]*type="(title|ctrTitle)"', sp) is not None
            paras = []
            for p in re.findall(r"<a:p>.*?</a:p>|<a:p .*?</a:p>", sp, re.S):
                t = _runs(p).strip()
                if not t:
                    continue
                bullet = bool(re.search(r"<a:bu(Char|AutoNum)", p)) and not re.search(r"<a:buNone", p)
                paras.append({"t": t, "b": bullet})
            if not paras:
                continue
            if is_title and not title:
                title = " ".join(q["t"] for q in paras).replace("\n", " ")
            else:
                shapes.append(paras)
        for rid in re.findall(r'r:embed="([^"]+)"', x):
            tg = rels.get(rid, "")
            if "media" in tg:
                fn = os.path.basename(tg)
                imgs.append((os.path.splitext(fn)[0], z.getinfo("ppt/media/" + fn).file_size))
        def short(q):
            t = K._plain(q["t"]).strip()
            return 0 < len(t) < 85 and not t.endswith((".", ":", ";", ",")) and "\n" not in t
        if not title:   # отдельная короткая фигура-заголовок
            for k, sh in enumerate(shapes):
                if len(sh) == 1 and short(sh[0]):
                    title = K._plain(shapes.pop(k)[0]["t"]).strip()
                    break
        if not title and shapes and len(shapes[0]) > 1 and short(shapes[0][0]):   # заголовок — первый абзац текста
            title = K._plain(shapes[0].pop(0)["t"]).strip()
        out.append({"title": title, "shapes": shapes, "imgs": imgs})
    return out


def assets(path, adir):
    """Картинки pptx → _<deck>_assets/imageN.webp (один раз)."""
    from PIL import Image
    d = os.path.join(HERE, adir)
    os.makedirs(d, exist_ok=True)
    z = zipfile.ZipFile(path)
    for n in z.namelist():
        if not n.startswith("ppt/media/"):
            continue
        o = os.path.join(d, os.path.splitext(os.path.basename(n))[0] + ".webp")
        if os.path.exists(o):
            continue
        try:
            im = Image.open(io.BytesIO(z.read(n)))
        except Exception:
            continue
        big = z.getinfo(n).file_size > BIG
        im = im.convert("RGB" if big else "RGBA")
        if im.width > 1672:
            im = im.resize((1672, round(im.height * 1672 / im.width)), Image.LANCZOS)
        im.save(o, "WEBP", quality=84 if big else 92, method=6)


# ---------------------------------------------------------------- отрисовка
TONES = ["cy", "am", "lm", "mg"]


def _block(paras, k):
    """Одна текстовая фигура pptx → карточка: абзацы, список, конфигурация CLI."""
    parts, lst, cli = [], [], []

    def flush():
        if lst:
            parts.append('<ul class="li">%s</ul>' % "".join("<li>%s</li>" % i for i in lst))
            del lst[:]
        if cli:
            parts.append(K.conf([K._plain(c) for c in cli], ""))
            del cli[:]
    for q in paras:
        for line in q["t"].split("\n"):
            line = line.strip()
            if not line:
                continue
            if _PROMPT.match(K._plain(line)):
                if lst:
                    flush()
                cli.append(html.unescape(line))
                continue
            if cli:
                flush()
            if q["b"]:
                lst.append(line)
            else:
                flush()
                parts.append("<p>%s</p>" % line)
    flush()
    return '<div class="c %s">%s</div>' % (TONES[k % len(TONES)], "".join(parts))


def _weight(paras):
    return sum(len(K._plain(q["t"])) for q in paras)


def render(slides, adir, titles=None, budget=1300, skip=(1,), man=None):
    """slides — из parse(); titles — {номер: заголовок с <em>} для красоты; skip — номера слайдов pptx, которые не выводить (титул)."""
    titles = titles or {}
    last_title = ""
    for n, s in enumerate(slides, 1):
        if n in skip:
            continue
        t = s["title"] or last_title
        last_title = t
        title = titles.get(n) or _esc(t)
        if man and n in man:                # ручная выжимка: тезисы + перерисованная схема; полный текст pptx — свёрнут
            import _pt_man
            _pt_man.emit(n, s, man[n], title, t, adir, _block)
            if any(pg.get("raw") for pg in man[n]):      # инфографика автора уже повторена вёрсткой
                continue
            for i in dict.fromkeys(i for i, sz in s["imgs"] if sz > BIG):
                K.info(adir, i, "pptx %d · %s · %s" % (n, K._plain(t), i))
            continue
        small = [i for i, sz in s["imgs"] if sz <= BIG]
        big = [i for i, sz in s["imgs"] if sz > BIG]
        small = list(dict.fromkeys(small))
        # делим фигуры на страницы по объёму текста
        pages, cur, w = [], [], 0
        for sh in s["shapes"]:
            sw_ = _weight(sh)
            if cur and w + sw_ > budget:
                pages.append(cur)
                cur, w = [], 0
            cur.append(sh)
            w += sw_
        if cur or not pages:
            pages.append(cur)
        for pi, pg in enumerate(pages):
            lab = "%s · %d" % (K._plain(t), pi + 1) if len(pages) > 1 else K._plain(t)
            lab = "pptx %d · %s" % (n, lab)
            blocks = [_block(sh, k) for k, sh in enumerate(pg)]
            pics = [K.pic(adir, i) for i in small] if pi == len(pages) - 1 else []
            if not blocks and not pics:
                continue
            if pics and blocks:
                body = grow("g2", col(*[step(b) for b in blocks]), col(*[step(x) for x in pics]))
            elif len(blocks) > 1 and sum(_weight(sh) for sh in pg) > 450:
                half = (len(blocks) + 1) // 2
                body = grow("g2", col(*[step(b) for b in blocks[:half]]), col(*[step(b) for b in blocks[half:]]))
            else:
                body = grow("g", col(*[step(b) for b in (blocks or pics)]))
            slide(lab, sc(head(title), body))
        for i in dict.fromkeys(big):
            K.info(adir, i, "pptx %d · %s · %s" % (n, K._plain(t), i))
