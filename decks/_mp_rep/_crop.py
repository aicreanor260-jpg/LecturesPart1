# -*- coding: utf-8 -*-
"""python _mp_rep/_crop.py <имя> x0 y0 x1 y1 <имя>_что.png [key] — вырезка из оригинала _mp_src/<имя>.png (1672×941).
key — убрать фон-цвет вокруг (вырезка с прозрачностью по заливке от углов, допуск 38)."""
import sys, pathlib
from PIL import Image, ImageDraw
D = pathlib.Path(__file__).resolve().parent.parent
n, x0, y0, x1, y1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
c = Image.open(D / "_mp_src" / f"{n}.png").convert("RGBA").crop((x0, y0, x1, y1))
if len(sys.argv) > 7 and sys.argv[7] == "key":
    w, h = c.size
    for pt in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        ImageDraw.floodfill(c, pt, (0, 0, 0, 0), thresh=38)
c.save(D / "_mp_rep" / "crops" / out); print(out, c.size)
