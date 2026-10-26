# -*- coding: utf-8 -*-
"""python -X utf8 _o5_shots.py [from to] → _o5_figprev/shots/NNN.png и листы sheetK.jpg (все шаги раскрыты)."""
import pathlib
import sys

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).resolve().parent
OUT = D / "_o5_figprev" / "shots"
OUT.mkdir(parents=True, exist_ok=True)
a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (1, 10 ** 6)
with sync_playwright() as pw:
    br = pw.chromium.launch(channel="chrome")
    pg = br.new_page(viewport={"width": 1600, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto((D / "ospf-2-5.html").as_uri())
    pg.wait_for_timeout(1500)
    pg.add_style_tag(content=".step{opacity:1!important;transform:none!important}[data-ph]{opacity:1!important}")
    n = pg.evaluate("document.querySelectorAll('section.slide').length")
    labs = pg.evaluate("[...document.querySelectorAll('section.slide')].map(s=>s.dataset.label)")
    files = []
    for k in range(max(1, a), min(n, b) + 1):
        pg.evaluate("k=>document.querySelectorAll('#tocg .tocit')[k].click()", k - 1)
        pg.wait_for_timeout(450)
        f = OUT / ("%03d.png" % k)
        pg.screenshot(path=str(f))
        files.append((k, f))
    br.close()
print("слайдов", n, "ошибки JS:", errs[:5])
W, H, C = 520, 292, 4
for i in range(0, len(files), 16):
    part = files[i:i + 16]
    sh = Image.new("RGB", (W * C, (H + 18) * ((len(part) + C - 1) // C)), "white")
    d = ImageDraw.Draw(sh)
    for j, (k, f) in enumerate(part):
        im = Image.open(f).convert("RGB").resize((W, H))
        x, y = (j % C) * W, (j // C) * (H + 18)
        sh.paste(im, (x, y))
        d.text((x + 3, y + H + 2), "%d %s" % (k, labs[k - 1][:60]), fill="red")
    sh.save(OUT / ("sheet%02d.jpg" % (part[0][0])), quality=82)
print("листы:", sorted(p.name for p in OUT.glob("sheet*.jpg")))
