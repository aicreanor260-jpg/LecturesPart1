# -*- coding: utf-8 -*-
"""Чистые фоны деки «IP-сервисы 2.6 (по pptx)» в стиле инфографик автора: тёмно-синий космос, звёзды,
неоновое свечение, глобус с сеткой. В комплекте «NAT 2.6» папки ФОН нет — фоны строятся здесь.

    python _i6_mkbg.py → _i6_assets/bg_main.webp, bg_cover.webp, bgk_space.webp, bgk_globe.webp, bgk_net.webp
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_i6_assets")


def base(w, h, seed):
    rnd = random.Random(seed)
    im = Image.new("RGB", (w, h))
    px = im.load()
    for y in range(h):
        t = y / float(h)
        r, g, b = int(4 + 6 * t), int(9 + 14 * t), int(26 + 30 * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    glow = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(glow)
    for cx, cy, rad, col in [(.18, .25, .42, (20, 70, 170)), (.82, .78, .5, (10, 90, 200)), (.55, .05, .3, (60, 40, 150))]:
        d.ellipse([w * cx - w * rad, h * cy - w * rad * .6, w * cx + w * rad, h * cy + w * rad * .6], fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(w / 9))
    im = _add(im, glow, .32)
    st = ImageDraw.Draw(im)
    for _ in range(int(w * h / 2600)):
        x, y = rnd.random() * w, rnd.random() * h
        v = rnd.randint(90, 230)
        rr = rnd.choice([0, 0, 0, 1])
        st.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(v - 30, v - 10, v))
    return im


def _add(a, b, k):
    from PIL import ImageChops
    return ImageChops.add(a, Image.eval(b, lambda v: int(v * k)))


def globe(im, cx, cy, r):
    """Глобус: тёмный шар, неоновый ободок, параллели и меридианы."""
    w, h = im.size
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(6, 22, 60, 235))
    for k in range(1, 9):
        a = math.pi * k / 9
        ry = r * math.cos(a)
        rx = r * math.sin(a)
        yy = cy - r * math.cos(a)
        d.ellipse([cx - rx, yy - rx * .12, cx + rx, yy + rx * .12], outline=(60, 150, 255, 70), width=2)
        _ = ry
    for k in range(-4, 5):
        rx = abs(r * math.sin(math.pi * k / 10))
        d.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=(60, 150, 255, 60), width=2)
    rnd = random.Random(7)
    for _ in range(220):
        a = rnd.random() * 2 * math.pi
        q = math.sqrt(rnd.random()) * r * .96
        x, y = cx + q * math.cos(a), cy + q * math.sin(a)
        d.ellipse([x - 1.6, y - 1.6, x + 1.6, y + 1.6], fill=(120, 200, 255, 150))
    rim = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(rim)
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(80, 190, 255, 255), width=10)
    rim = rim.filter(ImageFilter.GaussianBlur(14))
    lay.alpha_composite(rim)
    d2 = ImageDraw.Draw(lay)
    d2.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 220, 255, 230), width=3)
    im = im.convert("RGBA")
    im.alpha_composite(lay)
    return im.convert("RGB")


def net(im, seed, n=26):
    """Тонкая сеть светящихся узлов и линий."""
    w, h = im.size
    rnd = random.Random(seed)
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    pts = [(rnd.random() * w, rnd.random() * h) for _ in range(n)]
    for i, a in enumerate(pts):
        for b in pts[i + 1:]:
            if math.hypot(a[0] - b[0], a[1] - b[1]) < w * .16:
                d.line([a, b], fill=(70, 160, 255, 46), width=2)
    for x, y in pts:
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(140, 210, 255, 160))
    im = im.convert("RGBA")
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(.6)))
    return im.convert("RGB")


def save(im, name, q=80):
    im.save(os.path.join(OUT, name + ".webp"), "WEBP", quality=q, method=6)
    print(name, im.size)


def main():
    os.makedirs(OUT, exist_ok=True)
    W, H = 1672, 941
    space = base(W, H, 1)
    save(space, "bgk_space")
    save(globe(base(W, H, 2), int(W * .86), int(H * 1.12), int(H * .62)), "bgk_globe")
    save(net(base(W, H, 3), 5), "bgk_net")
    big = base(1920, 1080, 4)
    save(net(big, 9, 30), "bg_main", 76)
    save(globe(base(1920, 1080, 6), 1480, 620, 520), "bg_cover", 80)


if __name__ == "__main__":
    main()
