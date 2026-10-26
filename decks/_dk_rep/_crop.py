# -*- coding: utf-8 -*-
"""python _dk_rep/_crop.py <имя> x0 y0 x1 y1 <имя>_что.png — вырезка из оригинала _dk_src/<имя>.png (1672×941)."""
import sys, pathlib
from PIL import Image
D = pathlib.Path(__file__).resolve().parent.parent
n, x0, y0, x1, y1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
c = Image.open(D / "_dk_src" / f"{n}.png").convert("RGBA").crop((x0, y0, x1, y1))
c.save(D / "_dk_rep" / "crops" / out); print(out, c.size)
