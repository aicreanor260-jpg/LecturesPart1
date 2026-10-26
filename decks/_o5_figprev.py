# -*- coding: utf-8 -*-
"""python -X utf8 _o5_figprev.py <модуль> <функция> [арг ...] [--ph N] → _o5_figprev/<функция>[_арг].png
Рендерит HTML-блок, который возвращает функция (fig()/scene()), на фоне деки с её CSS. --ph N — показать шаг сцены N
(по умолчанию все шаги сцены видны)."""
import importlib
import os
import pathlib
import sys
import tempfile

from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(D))
OUT = D / "_o5_figprev"
OUT.mkdir(exist_ok=True)

args = sys.argv[1:]
ph = None
if "--ph" in args:
    k = args.index("--ph")
    ph = int(args[k + 1])
    del args[k:k + 2]
mod, fn, rest = args[0], args[1], args[2:]
conv = [int(a) if a.lstrip("-").isdigit() else a for a in rest]
block = getattr(importlib.import_module(mod), fn)(*conv)

import _o5_theme as T  # noqa: E402
from _sw_style import CSS  # noqa: E402
import _sw_fig  # noqa: E402
import _dk_kit  # noqa: E402

show = ("[data-ph]{opacity:1!important}" if ph is None else
        "[data-ph]{opacity:0!important}" + "".join('[data-ph="%d"]{opacity:1!important}' % i for i in range(ph + 1)))
html = ('<!doctype html><meta charset="utf-8">%s<style>%s%s%s%s body{overflow:auto;padding:20px}'
        '.step{opacity:1!important;transform:none!important}%s</style><div id="w" style="width:1500px">%s</div>'
        % (T.FONTS, CSS, _sw_fig.CSS, _dk_kit.CSS, T.css("", ""), show, block))
tmp = pathlib.Path(tempfile.gettempdir()) / ("o5fp_%d.html" % os.getpid())
tmp.write_text(html, encoding="utf-8")
name = fn + ("_" + "_".join(map(str, rest)) if rest else "") + ("_ph%d" % ph if ph is not None else "")
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1560, "height": 1000})
    pg.goto(tmp.as_uri())
    pg.wait_for_timeout(1200)
    pg.locator("#w").screenshot(path=str(OUT / (name + ".png")))
    b.close()
tmp.unlink()
print("ok", OUT / (name + ".png"))
