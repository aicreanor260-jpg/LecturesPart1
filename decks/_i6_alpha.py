# -*- coding: utf-8 -*-
"""Прозрачный фон вырезок инфографик 2.6: тёмный фон, связанный с краем, — заливкой от краёв в alpha=0, край растушёван.
    python _i6_alpha.py → правит _dk_rep/crops/n6_*.png на месте (повторный запуск безопасен)."""
import glob
import os
from collections import deque

from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
LUM = 62  # тёмно-синий фон инфографик


def clear(path):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    px = im.load()
    if all(px[x, y][3] < 255 for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))):
        return False
    bgm = Image.new("L", (w, h), 0)
    m = bgm.load()
    q = deque((x, y) for x in range(w) for y in (0, h - 1))
    q.extend((x, y) for y in range(h) for x in (0, w - 1))
    while q:
        x, y = q.popleft()
        if m[x, y]:
            continue
        r, g, b, a = px[x, y]
        if max(r, g, b) > LUM:
            continue
        m[x, y] = 255
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not m[nx, ny]:
                q.append((nx, ny))
    soft = bgm.filter(ImageFilter.GaussianBlur(2))
    alpha = im.getchannel("A")
    alpha = Image.eval(Image.merge("L", [alpha]), lambda v: v)
    from PIL import ImageChops
    im.putalpha(ImageChops.multiply(alpha, Image.eval(soft, lambda v: 255 - v)))
    im.save(path)
    return True


if __name__ == "__main__":
    n = sum(clear(f) for f in glob.glob(os.path.join(HERE, "_dk_rep", "crops", "n6_*.png")))
    print("обработано", n)
