# -*- coding: utf-8 -*-
"""Подготовка ассетов деки «Маршрутизаторы ESR» (2.3 доп.) из pptx:
    python _er_prep.py <папка распакованного pptx>
Инфографики автора → _er_assets/pNN.webp, фоны (размытая инфографика) → bg_main/bg_cover,
вырезки устройств с прозрачным фоном → dev_*.png."""
import os
import sys

from PIL import Image, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_er_assets")
# слайд pptx → картинка-инфографика (1672×941)
INFO = {3: 2, 4: 3, 5: 4, 6: 6, 7: 7, 11: 9, 18: 13, 19: 14, 20: 16, 29: 23, 30: 25, 31: 27, 32: 28,
        34: 29, 35: 30, 36: 31, 37: 34, 38: 36, 39: 38, 40: 40, 41: 42, 42: 44, 43: 46, 44: 48, 45: 50, 46: 51}
# вырезки: (картинка, рамка)
CROPS = {"dev_pc": (16, (150, 452, 318, 564)), "dev_srv": (44, (1268, 228, 1622, 545))}


def media(src, n):
    return Image.open(os.path.join(src, "ppt", "media", "image%d.png" % n)).convert("RGB")


def cutout(im):
    """Светлый лавандовый фон → прозрачный, с мягким краем."""
    im = im.convert("RGBA")
    px = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, _ = px[x, y]
            lo, hi = min(r, g, b), max(r, g, b)
            if lo > 200 and hi - lo < 60:
                a = max(0, min(255, int((235 - lo) * 255 / 35)))
                px[x, y] = (r, g, b, a)
    return im


def main(src):
    for sl, n in INFO.items():
        media(src, n).save(os.path.join(OUT, "p%02d.webp" % sl), "WEBP", quality=82, method=6)
    bg = media(src, 13).filter(ImageFilter.GaussianBlur(28))
    ImageEnhance.Brightness(bg).enhance(1.04).resize((1600, 900)).save(os.path.join(OUT, "bg_main.webp"), "WEBP", quality=70)
    cov = media(src, 2).filter(ImageFilter.GaussianBlur(10))
    cov.resize((1600, 900)).save(os.path.join(OUT, "bg_cover.webp"), "WEBP", quality=74)
    for name, (n, box) in CROPS.items():
        cutout(media(src, n).crop(box)).save(os.path.join(OUT, name + ".png"))


if __name__ == "__main__":
    main(sys.argv[1])
