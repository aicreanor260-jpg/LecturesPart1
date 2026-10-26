# -*- coding: utf-8 -*-
"""python -X utf8 _o5_rep/_cmp.py <имя> ... -> _o5_rep/_cmp/<имя>.jpg (сверху оригинал, снизу вёрстка, все шаги видны).
Рендерит только вёрстку (без сборки всей деки), поэтому агенты не мешают друг другу."""
import os
import pathlib
import sys
import tempfile

from PIL import Image
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D))
import _o5_replib as R  # noqa: E402

OUT = D / "_o5_rep" / "_cmp"
OUT.mkdir(exist_ok=True)
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&'
         'family=Golos+Text:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap">')
BASE = ("<style>body{margin:0;background:#fff}.repc *{box-sizing:border-box}.repc .ab{position:absolute}"
        ".step{opacity:1!important;transform:none!important}</style>")

with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 2000, "height": 1200})
    for name in sys.argv[1:]:
        m = R.load(name)
        if m is None:
            print("нет вёрстки", name)
            continue
        top = getattr(m, "TOP", 0)
        html = ('<!doctype html><meta charset="utf-8">%s%s<div class="repc" id="r" style="position:relative;width:%dpx;'
                'height:%dpx;overflow:hidden;font-family:\'Golos Text\',sans-serif"><div style="position:relative;width:%dpx;'
                'height:%dpx;margin-top:-%dpx">%s</div></div>' % (FONTS, BASE, m.W, m.H - top, m.W, m.H, top, m.HTML))
        tmp = pathlib.Path(tempfile.gettempdir()) / ("o5cmp_%d_%s.html" % (os.getpid(), name))
        tmp.write_text(html, encoding="utf-8")
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(1500)
        shot = OUT / ("_%s.png" % name)
        pg.locator("#r").screenshot(path=str(shot))
        a = Image.open(D / "_o5_src" / ("%s.png" % name)).convert("RGB")
        c2 = Image.open(shot).convert("RGB")
        c2 = c2.resize((a.width, round(c2.height * a.width / c2.width)))
        c = Image.new("RGB", (a.width, a.height + 16 + c2.height), "red")
        c.paste(a, (0, 0))
        c.paste(c2, (0, a.height + 16))
        c.thumbnail((1500, 1800))
        c.save(OUT / ("%s.jpg" % name), quality=85)
        shot.unlink()
        tmp.unlink()
        print("ok", name)
    b.close()
