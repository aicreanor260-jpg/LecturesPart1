# -*- coding: utf-8 -*-
"""python _o5_rep/_crop.py <имя> x0 y0 x1 y1 <имя>_что.png [--clear] — вырезка из _o5_src/<имя>.png.
--clear: почти белые/пастельные пиксели по краю делаются прозрачными (заливка от углов)."""
import pathlib
import sys

from PIL import Image, ImageDraw

D = pathlib.Path(__file__).resolve().parent.parent
n, x0, y0, x1, y1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
c = Image.open(D / "_o5_src" / ("%s.png" % n)).convert("RGBA").crop((x0, y0, x1, y1))
if "--clear" in sys.argv:
    for pt in [(0, 0), (c.width - 1, 0), (0, c.height - 1), (c.width - 1, c.height - 1)]:
        ImageDraw.floodfill(c, pt, (0, 0, 0, 0), thresh=60)
c.save(D / "_o5_rep" / "crops" / out)
print(out, c.size)
