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

# слайды, где анимация объясняет суть: шаги листаются вручную; остальные проигрываются сами
MANUAL = {"p020", "p054", "p045", "p001", "p016", "p060", "p024", "p058", "p059", "p011",
          "p074", "p067", "p026", "p077", "p014", "p047", "p028", "p053", "p055", "p041",
          "p039", "p009", "p019", "p072", "p029", "p034", "p033", "p036"}

import re
def bump(html):
    """мелкий текст крупнее: всё, что меньше 18px, поднимаем"""
    return re.sub(r'font-size:(\d+(?:\.\d+)?)px',
                  lambda m: 'font-size:%spx' % (max(18.0, float(m.group(1))) if float(m.group(1)) < 18 else m.group(1)),
                  html)

SKIP = {"p037"}  # заменён титулом
order = [r for r in ORDER if r in found] + sorted(r for r in found if r not in ORDER and r not in SKIP)
slides = []
for r in order:
    label, html = found[r]
    slides.append((label, bump(html), "0" if r in MANUAL else "1"))
n, size = build(slides, str(HERE / "eltex-devices-2.html"),
                assets_dir=str(HERE / "_el2assets"), bg="bg.jpg", ftl="aura_tl.png", fbr="aura_br.png")
print(f"{n} слайдов, {size/1024/1024:.1f} МБ")
print("нет в ORDER:", [r for r in found if r not in ORDER])
