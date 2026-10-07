# -*- coding: utf-8 -*-
"""Перламутровая пастельная подложка «масляная живопись» для деки 2.1."""
import numpy as np, random
from PIL import Image, ImageFilter, ImageDraw

random.seed(21)
W, H = 2304, 1296
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
X, Y = xx / W, yy / H

SPOTS = [
    (0.06, 0.04, 0.30, (255, 223, 190)),
    (0.42, 0.02, 0.26, (255, 241, 203)),
    (0.88, 0.08, 0.28, (240, 224, 253)),
    (0.99, 0.44, 0.30, (223, 229, 253)),
    (0.82, 0.90, 0.34, (205, 221, 247)),
    (0.28, 0.96, 0.34, (186, 205, 236)),
    (0.02, 0.58, 0.30, (223, 235, 252)),
    (0.56, 0.50, 0.38, (252, 245, 251)),
    (0.18, 0.32, 0.22, (253, 234, 222)),
    (0.72, 0.28, 0.22, (246, 237, 255)),
    (0.50, 0.78, 0.26, (221, 226, 246)),
]

acc = np.zeros((H, W, 3), np.float32)
wsum = np.zeros((H, W, 1), np.float32)
for cx, cy, r, col in SPOTS:
    d2 = ((X - cx) * 1.0) ** 2 + ((Y - cy) * (H / W)) ** 2
    w = np.exp(-d2 / (2 * (r * 0.44) ** 2)).astype(np.float32)[:, :, None]
    acc += w * np.array(col, np.float32)
    wsum += w
img = acc / np.clip(wsum, 1e-4, None)
img = img * 0.97 + 255.0 * 0.03

# второй слой — мелкие цветные кляксы «мазков», даёт живописную пестроту
rng2 = np.random.default_rng(3)
blob = np.zeros((H, W, 3), np.float32); bw = np.zeros((H, W, 1), np.float32)
PAINT = [(255,214,176),(255,238,192),(236,216,252),(206,226,250),(205,238,226),(250,214,228),(255,248,230)]
for _ in range(34):
    cx, cy = rng2.random(), rng2.random()
    r = rng2.uniform(0.055, 0.14)
    col = PAINT[rng2.integers(0, len(PAINT))]
    d2 = (X - cx) ** 2 + ((Y - cy) * (H / W)) ** 2
    w = np.exp(-d2 / (2 * (r * 0.6) ** 2)).astype(np.float32)[:, :, None]
    blob += w * np.array(col, np.float32); bw += w
blob = blob / np.clip(bw, 1e-4, None)
k = np.clip(bw / (bw + 0.55), 0, 1) * 0.42
img = img * (1 - k) + blob * k

bg = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22))

# мазки кисти: смещение по синусам
arr = np.asarray(bg).astype(np.float32)
nx = np.zeros((H, W), np.float32); ny = np.zeros((H, W), np.float32)
for f, a, p in ((0.012, 8.0, 0.0), (0.030, 3.6, 1.1), (0.005, 13.0, 2.3)):
    nx += a * np.sin(yy * f + p) * np.cos(xx * f * 0.7 + p)
    ny += a * np.cos(xx * f + p * 1.7) * np.sin(yy * f * 0.8 + p)
sx = np.clip(xx + nx, 0, W - 1).astype(np.int32)
sy = np.clip(yy + ny, 0, H - 1).astype(np.int32)
arr = arr[sy, sx]
arr = np.clip(arr + np.random.default_rng(7).normal(0, 2.6, (H, W, 1)), 0, 255)
bg = Image.fromarray(arr.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))

# искры
sp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(sp, "RGBA")
for _ in range(170):
    x, y = random.random() * W, random.random() * H
    r = random.uniform(1.4, 4.2)
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 250, int(random.uniform(70, 170))))
sp = sp.filter(ImageFilter.GaussianBlur(2.2))
# искры — аддитивным светом
a = np.asarray(bg).astype(np.float32)
spa = np.asarray(sp).astype(np.float32)
a = np.clip(a + spa[:, :, :3] * (spa[:, :, 3:4] / 255.0) * 0.85, 0, 255)
bg = Image.fromarray(a.astype(np.uint8))
bg.save("bg.jpg", quality=88, optimize=True)
print("bg.jpg", bg.size)

def aura(spots, rot):
    S = 1024
    g = np.mgrid[0:S, 0:S].astype(np.float32) / S
    yg, xg = g[0], g[1]
    out = np.zeros((S, S, 4), np.float32)
    for (cx, cy, r, col, a) in spots:
        w = np.exp(-(((xg - cx) ** 2 + (yg - cy) ** 2) / (2 * (r * 0.6) ** 2))).astype(np.float32)
        al = w * a
        out[:, :, :3] += np.array(col, np.float32) * al[:, :, None]
        out[:, :, 3] += al
    al = np.clip(out[:, :, 3], 1e-4, 1.0)
    rgb = out[:, :, :3] / al[:, :, None]
    im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.clip(al * 255, 0, 255)]).astype(np.uint8), "RGBA")
    im = im.filter(ImageFilter.GaussianBlur(26))
    return im.transpose(Image.ROTATE_180) if rot else im

aura([(0.10, 0.08, 0.34, (255, 221, 188), 0.62),
      (0.36, 0.04, 0.26, (253, 240, 200), 0.50),
      (0.04, 0.34, 0.26, (238, 224, 253), 0.46)], False).save("aura_tl.png")
aura([(0.10, 0.08, 0.36, (206, 220, 248), 0.60),
      (0.36, 0.06, 0.26, (235, 221, 250), 0.46),
      (0.05, 0.32, 0.24, (206, 236, 231), 0.42)], True).save("aura_br.png")
print("aura ok")
