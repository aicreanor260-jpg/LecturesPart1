# -*- coding: utf-8 -*-
"""Сборка деки «Сетевые устройства 2.1» из модулей _el2/sNNN_NNN.py."""
import sys, pathlib, importlib, glob, os

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "_el2"))
from _el2_lib import build  # noqa: E402

try:
    from order import ORDER  # _el2/order.py: список ref в порядке лекции
except Exception:
    ORDER = []

mods = sorted(os.path.basename(p)[:-3] for p in glob.glob(str(HERE / "_el2" / "s*.py")))
found = {}
for name in mods:
    m = importlib.import_module(name)
    for ref, label, html in m.SLIDES:
        if ref in found:
            print("дубль:", ref, "в", name)
        found[ref] = (label, html)

order = [r for r in ORDER if r in found] + sorted(r for r in found if r not in ORDER)
slides = [found[r] for r in order]
n, size = build(slides, str(HERE / "eltex-devices-2.html"),
                assets_dir=str(HERE / "_el2assets"), bg="bg.jpg", ftl="frost_tl.png", fbr="frost_br.png")
print(f"{n} слайдов, {size/1024/1024:.1f} МБ")
print("нет в ORDER:", [r for r in found if r not in ORDER])
