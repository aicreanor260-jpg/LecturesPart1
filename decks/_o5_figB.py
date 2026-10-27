# -*- coding: utf-8 -*-
"""Схемы pptx «OSPF 2.5» — области OSPF и распространение LSA (слайды 30–53), перерисованные в кавайном стиле.
Экспорт: FIGS = {"sNN_imageK": функция}. Логика и подписи — строго как на картинках pptx."""
from _o5_figlib import (router, cloudsvg, blob, scene, T, box, fig, svg_only, INK, SOFT, PINK, BLUE)

GL = "#8e98ab"
DEFS = ('<marker id="o5g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>'
        '<marker id="o5p" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
        'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>' % (GL, PINK))

NBT = {"b": ("#e8f2fd", "#a9cdf3", "#1f4f8a"), "p": ("#fde7f0", "#f2a8c6", "#a3245c"),
       "y": ("#fff4d2", "#efd27a", "#7a5a00"), "g": ("#e4f6ea", "#9fd8b3", "#1d6e43"),
       "v": ("#efe9fb", "#c9b6f2", "#563ab0")}


def ml(cx, cy, s, size=20, col=INK, w=700, lh=1.25, mono=False):
    """Многострочный текст ('|' — перенос), центрирован по вертикали вокруг cy."""
    lines = s.split("|")
    y0 = cy - (len(lines) - 1) * size * lh / 2 + size * .36
    return "".join(T(cx, y0 + i * size * lh, t, size, col, w, mono=mono) for i, t in enumerate(lines))


def nb(cx, cy, w, h, s, tone="b", size=21):
    f, st, ink = NBT[tone]
    return box(cx - w / 2, cy - h / 2, w, h, f, st, r=18, sw=2.5) + ml(cx, cy, s, size, ink)


def ed(pts, head=True, dash=False, col=GL, mk="o5g", w=2.8):
    d = "M" + " L".join("%.1f %.1f" % p for p in pts)
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linejoin="round" stroke-linecap="round"%s%s/>'
            % (d, col, w, ' stroke-dasharray="5 6"' if dash else "", ' marker-end="url(#%s)"' % mk if head else ""))


def ep(cx, cy, s, size=17):
    lines = s.split("|")
    w = max(len(t) for t in lines) * size * .56 + 30
    h = len(lines) * size * 1.25 + 14
    return box(cx - w / 2, cy - h / 2, w, h, "#fff", "#c9d6e6", r=h / 2 if len(lines) == 1 else 16, sw=2) + \
        ml(cx, cy, s, size, "#1f4f8a", 700)


def grp(x, y, w, h, title, size=19):
    return (box(x, y, w, h, "rgba(255,255,255,.55)", "#d4dae4", r=16, sw=2, extra=' stroke-dasharray="7 6"')
            + T(x + w / 2, y + 28, title, size, SOFT, 800))


def rt(x, y, label, w=104, tone="b"):
    """Роутер с центром корпуса (x, y): линии подводим к (x, y)."""
    return router(x, y - w * .135, w, tone, label=label)


# ================================================================ s30: три области, ISP, ASBR, BR, ABR, IR
def s30_image37():
    R = {"ir1": (85, 225), "ir2": (245, 170), "asbr": (405, 225), "isp": (410, 70), "br1": (650, 120),
         "br2": (650, 330), "abr": (905, 225), "i1": (1060, 150), "i2": (1225, 225), "i3": (1060, 335)}
    o = [blob(215, 235, 225, 120, "b", seed=1, dash=False), blob(655, 228, 235, 165, "y", seed=2, dash=False),
         blob(1100, 230, 195, 135, "g", seed=3, dash=False), cloudsvg(410, 62, 130, 76, tone="v")]
    for a, b in [("ir1", "ir2"), ("ir2", "asbr"), ("asbr", "isp"), ("asbr", "br1"), ("asbr", "abr"), ("asbr", "br2"),
                 ("br1", "abr"), ("br2", "abr"), ("abr", "i1"), ("abr", "i3"), ("i1", "i2"), ("i3", "i2")]:
        o.append(ed([R[a], R[b]], head=False, col="#3a3550", w=4))
    o.append(cloudsvg(410, 62, 130, 76, label="ISP", tone="v", fs=22))
    o += [T(250, 280, "AREA 0.0.0.1", 24, INK, 800), T(655, 200, "AREA 0.0.0.0", 24, INK, 800),
          T(1090, 240, "AREA 0.0.0.5", 24, INK, 800)]
    for k, lab in [("ir1", "IR"), ("ir2", "IR"), ("asbr", "ASBR"), ("br1", "BR"), ("br2", "BR"), ("abr", "ABR"),
                   ("i1", "IR"), ("i2", "IR"), ("i3", "IR")]:
        o.append(rt(R[k][0], R[k][1], lab))
    return fig("0 0 1320 420", "".join(o), DEFS)


# ================================================================ s32: цепочка областей
def s32_image40():
    xs = [(140, 260, "Area 0.0.0.1|обычная область"), (405, 150, "ABR"), (670, 260, "Area 0.0.0.0|магистраль"),
          (935, 150, "ABR"), (1200, 260, "Area 0.0.0.2|Stub")]
    o = [ed([(270, 90), (330, 90)], False), ed([(480, 90), (540, 90)], False),
         ed([(800, 90), (860, 90)], False), ed([(1010, 90), (1070, 90)], False)]
    for cx, w, s in xs:
        o.append(nb(cx, 90, w, 96, s))
    return fig("0 0 1340 180", "".join(o), DEFS)


# ================================================================ s33: AS 64511 и типы областей
def s33_image42():
    R = {"l2": (350, 115), "r1": (195, 270), "asbr": (370, 275), "r2": (365, 395), "abr": (800, 355),
         "r3": (800, 470), "abr2": (1075, 280), "r4": (1040, 440), "r5": (1225, 270)}
    o = ['<ellipse cx="700" cy="410" rx="640" ry="215" fill="#eef0f5" stroke="#c9cfdb" stroke-width="3"/>',
         blob(250, 100, 190, 72, "b", seed=4, dash=False),
         blob(610, 300, 210, 95, "y", seed=5, dash=False).replace("#fef6dc", "#ffffff").replace("#efcf6a", "#d6dbe4"),
         blob(215, 305, 185, 80, "v", seed=6, dash=False), blob(350, 445, 135, 95, "b", seed=7, dash=False),
         blob(790, 510, 145, 95, "p", seed=8, dash=False), blob(1010, 370, 180, 115, "y", seed=9, dash=False),
         blob(1225, 320, 95, 82, "g", seed=10, dash=False)]
    for a, b in [("l2", "asbr"), ("r1", "asbr"), ("asbr", "r2"), ("asbr", "abr"), ("abr", "r3"), ("abr", "abr2"),
                 ("abr", "r4"), ("r4", "abr2"), ("abr2", "r5")]:
        o.append(ed([R[a], R[b]], head=False, col="#3a3550", w=4))
    o += [T(190, 45, "AS 64500", 22, INK, 800), ml(170, 105, "ISP|IS-IS", 21, INK, 800),
          ml(185, 345, "Not-So-Stubby area, NSSA|Area 0.0.0.4", 20, INK, 800),
          ml(345, 495, "Totally NSSA|Area 0.0.0.5", 20, INK, 800),
          ml(600, 375, "Backbone area|Area 0.0.0.0", 20, INK, 800),
          ml(790, 560, "Totally Stubby area|Area 0.0.0.3", 20, INK, 800),
          ml(960, 345, "Standard area|Area 0.0.0.1", 20, INK, 800),
          ml(1240, 345, "Stub area|Area 0.0.0.2", 20, INK, 800), T(560, 595, "AS 64511", 22, INK, 800)]
    for k, lab in [("l2", "L2"), ("r1", "R-1"), ("asbr", "ASBR-1"), ("r2", "R-2"), ("abr", "ABR-1"), ("r3", "R-3"),
                   ("abr2", "ABR-2"), ("r4", "R-4"), ("r5", "R-5")]:
        o.append(rt(R[k][0], R[k][1], lab, 100))
    return fig("0 0 1360 640", "".join(o), DEFS)


# ================================================================ s37 / s50: внешняя сеть → ASBR → ABR-1 → ABR-2 → IR
def _chain3(ext, g1, g2, g3):
    o = [grp(300, 20, 480, 250, g1), grp(810, 140, 240, 130, g2), grp(1080, 140, 270, 130, g3),
         ed([(250, 100), (325, 100)]), ed([(450, 100), (470, 100)], False),
         ed([(400, 135), (400, 220), (515, 220)], False), ed([(685, 220), (865, 220)], False),
         ed([(995, 220), (1095, 220)], False),
         nb(135, 100, 230, 84, ext), nb(390, 100, 120, 70, "ASBR"), nb(615, 100, 290, 70, "Внутренний маршрутизатор"),
         nb(600, 220, 170, 70, "ABR-1"), nb(930, 220, 130, 70, "ABR-2"),
         nb(1215, 220, 240, 84, "Внутренний|маршрутизатор")]
    return fig("0 0 1360 290", "".join(o), DEFS)


def s37_image48():
    return _chain3("Внешняя сеть|например, ISP", "Область 0.0.0.1 · обычная", "Область 0.0.0.0 · магистраль",
                   "Область 0.0.0.5 · обычная")


def s50_image77():
    return _chain3("Внешняя сеть", "NSSA", "Area 0 · магистраль", "Stub")


# ================================================================ s38: кто создаёт LSA и куда
def s38_image50():
    L = [(60, "Маршрутизаторы области|создают LSA-1"), (200, "DR общей сети|создаёт LSA-2"),
         (340, "ABR создаёт LSA-3|о сетях других областей"), (470, "ASBR создаёт LSA-5|о внешних маршрутах")]
    o = [ed([(400, 60), (925, 60)]), ed([(400, 200), (880, 200), (880, 95), (925, 95)]),
         ed([(400, 340), (925, 340)]), ed([(400, 470), (925, 470)])]
    for y, s in L:
        o.append(nb(230, y, 340, 96, s))
    o += [ep(645, 60, "только внутри своей области"), ep(645, 200, "только внутри своей области"),
          ep(645, 340, "передаёт сведения между|областями"), ep(645, 470, "распространяет по областям,|принимающим LSA-5"),
          nb(1080, 78, 300, 96, "LSDB этой области"), nb(1080, 340, 300, 96, "LSDB соседней области"),
          nb(1080, 470, 300, 96, "Остальная OSPF-сеть")]
    return fig("0 0 1260 530", "".join(o), DEFS)


# ================================================================ s39_52: LSA-1 не уходит в Area 0
def s39_image52():
    o = [ed([(380, 70), (410, 70), (410, 95), (440, 95)]), ed([(390, 210), (410, 210), (410, 125), (440, 125)]),
         ed([(680, 110), (1050, 110)], dash=True),
         nb(230, 70, 300, 80, "R1 создаёт LSA-1"), nb(230, 210, 320, 96, "R2 создаёт собственный|LSA-1"),
         nb(560, 110, 240, 80, "LSDB Area 0.0.0.1"), ep(865, 110, "LSA-1 не переносится в Area 0"),
         nb(1170, 110, 230, 80, "LSDB Area 0")]
    return fig("0 0 1300 270", "".join(o), DEFS)


# ================================================================ s40_55: DR создаёт один LSA-2
def s40_image55():
    o = [ed([(270, 60), (330, 60), (330, 175), (395, 175)], False), ed([(270, 190), (395, 190)], False),
         ed([(270, 315), (330, 315), (330, 205), (395, 205)], False), ed([(270, 350), (945, 350)]),
         nb(170, 60, 200, 80, "R1"), nb(170, 190, 200, 80, "R3"), nb(170, 330, 200, 80, "R2 · DR"),
         nb(560, 190, 330, 80, "Общий Ethernet-сегмент"), ep(610, 350, "создаёт один LSA-2|со списком Router ID"),
         nb(1075, 345, 260, 84, "LSDB области")]
    return fig("0 0 1240 400", "".join(o), DEFS)


# ================================================================ s42: LSA-1 → ABR-1 → LSA-4
def s42_image61():
    o = [ed([(210, 80), (595, 80)]), ed([(720, 80), (1085, 80)]), ed([(1240, 80), (1285, 80)]),
         nb(110, 80, 200, 90, "ASBR|Router ID: R"), ep(400, 80, "LSA-1 показывает, что это ASBR"),
         nb(660, 80, 120, 76, "ABR-1"), ep(900, 80, "LSA-4|«ASBR R доступен через меня»"),
         nb(1165, 80, 150, 76, "Область 0"), nb(1395, 80, 210, 76, "Другие области")]
    return fig("0 0 1510 160", "".join(o), DEFS)


# ================================================================ s45_67: NSSA, LSA-7 → LSA-5
def s45_image67():
    o = [grp(290, 30, 560, 170, "Область NSSA"),
         ed([(260, 130), (315, 130)]), ed([(555, 130), (735, 130)]), ed([(865, 130), (1185, 130)]),
         nb(140, 130, 240, 76, "Внешний источник"), nb(435, 130, 240, 76, "ASBR внутри NSSA"),
         ep(650, 130, "LSA-7"), nb(800, 130, 130, 76, "ABR"),
         ep(1020, 130, "подходящий LSA-7|преобразуется в LSA-5"), nb(1335, 130, 290, 76, "Остальная OSPF-сеть")]
    return fig("0 0 1500 220", "".join(o), DEFS)


# ================================================================ s46: OSPFv3 Link-LSA / Intra-Area-Prefix
def s46_image70():
    o = [ed([(420, 80), (885, 80)]), ed([(420, 110), (470, 110), (470, 270), (885, 270)]),
         nb(230, 95, 380, 100, "Маршрутизатор OSPFv3", size=23),
         ep(660, 80, "Link-LSA · адрес и префиксы|канала", 18), ep(660, 270, "Intra-Area-Prefix LSA ·|IPv6-префиксы", 18),
         nb(1060, 85, 340, 100, "Только соседям на этом|канале", size=23),
         nb(1060, 270, 340, 100, "Маршрутизаторы этой|области", size=23)]
    return fig("0 0 1250 340", "".join(o), DEFS)


# ================================================================ s52: Standard Area 1 → Area 0 → Standard Area 2
def s52_image83():
    o = [grp(10, 20, 640, 170, "Standard Area 1"), grp(880, 20, 180, 170, "Area 0"),
         grp(1290, 20, 310, 170, "Standard Area 2"),
         ed([(260, 120), (505, 120)]), ed([(630, 120), (895, 120)]), ed([(1040, 120), (1305, 120)]),
         nb(140, 120, 240, 84, "Внутренний|маршрутизатор"), ep(385, 120, "LSA-1 / при необходимости|LSA-2", 14),
         nb(570, 120, 120, 70, "ABR-1"), ep(765, 120, "LSA-3 · сеть из Area 1"),
         nb(970, 120, 140, 70, "ABR-2"), ep(1175, 120, "LSA-3 · сеть из Area 1"),
         nb(1445, 120, 260, 84, "Внутренний|маршрутизатор")]
    return fig("0 0 1610 200", "".join(o), DEFS)


# ================================================================ s53: Stub — LSA-3 0.0.0.0/0
def s53_image85():
    o = [grp(10, 20, 860, 230, "Stub"),
         ed([(250, 105), (535, 105)]), ed([(580, 158), (580, 205), (170, 205), (170, 162)]),
         ed([(820, 120), (1195, 120)], False),
         nb(140, 120, 220, 84, "ABR"), nb(680, 120, 280, 84, "Маршрутизатор Stub"),
         ep(400, 105, "LSA-3: 0.0.0.0/0"), ep(380, 205, "LSA-1 и LSA-2 внутри области"),
         ep(1005, 120, "неизвестные маршруты — к|ABR"), nb(1300, 120, 200, 80, "Другие сети")]
    return fig("0 0 1410 260", "".join(o), DEFS)


# ================================================================ полосы LSA по областям
LCOL = {1: ("#2fae6a", "#fff"), 2: ("#86c64a", "#fff"), 3: ("#2f8fe8", "#fff"), 4: ("#b0713f", "#fff"),
        5: ("#ef4a4a", "#fff"), 7: ("#f2b705", "#fff"), 0: ("#dfe6ee", INK)}
AX = [(150, 330), (510, 330), (870, 330)]                       # области: x, ширина
ATONE = {"y": ("#fff3cf", "#efd27a"), "g": ("#e3f5e8", "#9fd8b3"), "b": ("#e3f0fd", "#a9cdf3"),
         "p": ("#fde3ea", "#f2a8bf"), "v": ("#efe6f8", "#c9b3ea"), "P": ("#f5bccb", "#e07f9b"),
         "V": ("#d9c6f0", "#a88bd8")}


def band(x1, x2, y, label, kind, d, ph=None, h=40, size=20):
    """Лента-стрелка: d = 'r' | 'l' | 'both'. kind — номер LSA (0 — серая)."""
    f, ink = LCOL[kind]
    hd, nd, hh, wing = 26, 14, h / 2, 7
    if d == "both":
        pts = [(x1, y), (x1 + hd, y - hh - wing), (x1 + hd, y - hh), (x2 - hd, y - hh), (x2 - hd, y - hh - wing),
               (x2, y), (x2 - hd, y + hh + wing), (x2 - hd, y + hh), (x1 + hd, y + hh), (x1 + hd, y + hh + wing)]
    elif d == "r":
        pts = [(x1, y - hh), (x2 - hd, y - hh), (x2, y), (x2 - hd, y + hh), (x1, y + hh), (x1 + nd, y)]
    else:
        pts = [(x2, y - hh), (x1 + hd, y - hh), (x1, y), (x1 + hd, y + hh), (x2, y + hh), (x2 - nd, y)]
    st = "#9aa8b8" if kind == 0 else f
    poly = ('<polygon points="%s" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
            % (" ".join("%.1f,%.1f" % p for p in pts), f, st))
    g = poly + T((x1 + x2) / 2, y + size * .36, label, size, ink, 800)
    if ph is None:
        return "<g>%s</g>" % g
    dx = {"r": -40, "l": 40, "both": 0}[d]
    return ('<g data-ph="%d" class="mv" style="--x0:%dpx">%s</g>' % (ph, dx, g))


def lane(y0, h, areas, dr=True, ir2=False, isp=True):
    """Цепочка ISP — ASBR — ABR-1 — ABR-2 — IR. areas = [(тон, заголовок, подпись)] ×3."""
    ly = y0 + 100
    o = []
    for (x, w), (tone, t1, t2) in zip(AX, areas):
        f, st = ATONE[tone]
        o.append(box(x, y0, w, h, f, st, r=22, sw=2.5))
        o.append(T(x + w / 2, y0 + 34, t1, 23, INK, 800) + T(x + w / 2, y0 + 62, t2, 22, INK, 800))
    o.append(ed([(165, ly), (1165, ly)], False, col="#2a2540", w=5))
    if ir2:
        o.append(ed([(1010, y0 + 185), (1165, ly)], False, col="#2a2540", w=5))
    if isp:
        o.append(cloudsvg(78, ly + 2, 150, 110, label="ISP", tone="v", fs=24))
    if dr:
        o.append(T(415, ly - 14, "DR", 22, "#e0245e", 900) + T(775, ly - 14, "DR", 22, "#e0245e", 900))
    for x, lab in [(165, "ASBR"), (495, "ABR-1"), (855, "ABR-2"), (1165, "IR")]:
        o.append(rt(x, ly, lab, 110))
    if ir2:
        o.append(rt(1010, y0 + 185, "IR", 110))
    return "".join(o)


STD3 = [("y", "Area 0.0.0.1", "Standard"), ("g", "Area 0.0.0.0", "Backbone"), ("b", "Area 0.0.0.5", "Standard")]


def _ax(i, a=22, b=22):
    x, w = AX[i]
    return x + a, x + w - b


def s39_image53():
    o = [lane(10, 260, STD3, dr=False)]
    for i in range(3):
        o.append(band(*_ax(i), 215, "LSA-1", 1, "both", ph=i + 1))
    return scene(svg_only("0 0 1220 280", "".join(o), DEFS),
                 ["Area 0.0.0.1, 0.0.0.0 и 0.0.0.5: ISP — ASBR — ABR-1 — ABR-2 — IR",
                  "LSA-1 — внутри Area 0.0.0.1", "LSA-1 — внутри Area 0.0.0.0", "LSA-1 — внутри Area 0.0.0.5"])


def s40_image56():
    o = [lane(10, 270, STD3, ir2=True)]
    for i in range(2):
        o.append(band(*_ax(i), 215, "LSA-2", 2, "l", ph=i + 1))
    return scene(svg_only("0 0 1220 290", "".join(o), DEFS),
                 ["DR в Area 0.0.0.1 и в Area 0.0.0.0", "LSA-2 — внутри Area 0.0.0.1", "LSA-2 — внутри Area 0.0.0.0"])


def s41_image59():
    o = [lane(10, 300, STD3)]
    o += [band(340, 485, 205, "LSA-3", 3, "l", ph=1), band(505, 650, 205, "LSA-3", 3, "r", ph=1),
          band(700, 845, 260, "LSA-3", 3, "l", ph=2), band(880, 1025, 260, "LSA-3", 3, "r", ph=2)]
    return scene(svg_only("0 0 1220 320", "".join(o), DEFS),
                 ["Area 0.0.0.1 — ABR-1 — Area 0.0.0.0 — ABR-2 — Area 0.0.0.5",
                  "LSA-3 от ABR-1: в Area 0.0.0.1 и в Area 0.0.0.0", "LSA-3 от ABR-2: в Area 0.0.0.0 и в Area 0.0.0.5"])


def s43_image64():
    o = [lane(10, 260, STD3)]
    for i in range(3):
        o.append(band(*_ax(i, 50, 60), 215, "LSA-5", 5, "r", ph=i + 1))
    return scene(svg_only("0 0 1220 280", "".join(o), DEFS),
                 ["Внешние маршруты от ISP приходят на ASBR", "LSA-5 — в Area 0.0.0.1", "LSA-5 — в Area 0.0.0.0",
                  "LSA-5 — в Area 0.0.0.5"])


def s45_image68():
    o = [lane(10, 260, [("p", "Area 0.0.0.10", "NSSA"), STD3[1], STD3[2]])]
    o += [band(*_ax(0, 50, 60), 215, "LSA-7", 7, "r", ph=1), band(*_ax(1, 50, 60), 215, "LSA-5", 5, "r", ph=2),
          band(*_ax(2, 50, 60), 215, "LSA-5", 5, "r", ph=3)]
    return scene(svg_only("0 0 1220 280", "".join(o), DEFS),
                 ["Внешние маршруты от ISP приходят на ASBR в NSSA", "LSA-7 — в Area 0.0.0.10 (NSSA)",
                  "LSA-5 — в Area 0.0.0.0", "LSA-5 — в Area 0.0.0.5"])


# ================================================================ s49: сетка 2×3, полосы по типам
def s49_image75():
    H = 400
    top = [("p", "Area 0.0.0.10", "NSSA"), ("g", "Area 0.0.0.0", "Backbone"), ("v", "Area 0.0.0.15", "STUB")]
    bot = [("P", "Area 0.0.0.20", "Totally NSSA"), ("g", "Area 0.0.0.0", "Backbone"),
           ("V", "Area 0.0.0.25", "Totally STUBBY")]
    o = [lane(10, H, top), lane(440, H, bot)]
    ph = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 7: 6}
    ys = [180, 232, 284, 336, 388]
    bb = [(1, "LSA-1"), (2, "LSA-2"), (3, "LSA-3"), (4, "LSA-4"), (5, "LSA-5")]
    for y0 in (10, 440):
        for (k, s), y in zip(bb, ys):
            o.append(band(*_ax(1), y0 + y - 10, s, k, "both", ph=ph[k], h=38))
    for y0 in (10, 440):
        o.append(band(*_ax(0), y0 + 170, "LSA-1", 1, "both", ph=1, h=38))
        o.append(band(*_ax(0), y0 + 222, "LSA-2", 2, "both", ph=2, h=38))
        o.append(band(*_ax(2), y0 + 170, "LSA-1", 1, "both", ph=1, h=38))
        o.append(band(*_ax(2), y0 + 222, "LSA-2", 2, "both", ph=2, h=38))
    # верхний ряд: NSSA и STUB — межобластные LSA-3 проходят, LSA-4/LSA-5 нет
    o.append(band(*_ax(0), 10 + 274, "LSA-3 IA", 3, "l", ph=3, h=38, size=18))
    o.append(band(*_ax(0), 10 + 326, "LSA-7 0.0.0.0/0 (от ABR)", 7, "l", ph=6, h=38, size=18))
    o.append(band(*_ax(0), 10 + 378, "LSA-7 от ASBR → ABR", 7, "r", ph=6, h=38, size=18))
    o.append(band(*_ax(2, 12, 12), 10 + 274, "LSA-3 IA + 0.0.0.0/0", 3, "r", ph=3, h=38, size=18))
    # нижний ряд: Totally NSSA и Totally STUBBY — только LSA-3 с маршрутом по умолчанию
    o.append(band(*_ax(0), 440 + 274, "LSA-3 0.0.0.0/0", 3, "l", ph=3, h=38, size=18))
    o.append(band(*_ax(0), 440 + 378, "LSA-7 от ASBR → ABR", 7, "r", ph=6, h=38, size=18))
    o.append(band(*_ax(2, 12, 12), 440 + 274, "LSA-3 0.0.0.0/0", 3, "r", ph=3, h=38, size=18))
    return scene(svg_only("0 0 1220 850", "".join(o), DEFS),
                 ["NSSA — Backbone — STUB и Totally NSSA — Backbone — Totally STUBBY",
                  "LSA-1 — во всех областях", "LSA-2 — во всех областях",
                  "LSA-3 — межобластные маршруты; в STUB с ними приходит 0.0.0.0/0, в Totally-областях — только 0.0.0.0/0",
                  "LSA-4 — только в Backbone: в STUB и NSSA-области не передаётся",
                  "LSA-5 — только в Backbone", "LSA-7 — только внутри NSSA и Totally NSSA: от ASBR к ABR, который переводит его в LSA-5; в NSSA ABR может дать 0.0.0.0/0 через LSA-7"])


# ================================================================ диаграммы-последовательности
def seq(names, xs, msgs, caps, W):
    """msgs: (тип, i, j, текст); тип 'm' — сообщение, 'd' — пунктир, 's' — к себе."""
    top, step = 120, 88
    H = top + 40 + step * len(msgs) + 70
    o = []
    for x in xs:
        o.append(ed([(x, 70), (x, H - 70)], False, col="#c3cad6", w=3))
    for n, x in zip(names, xs):
        w = max(170, len(n) * 12 + 40)
        o.append(nb(x, 40, w, 60, n, size=19) + nb(x, H - 40, w, 60, n, size=19))
    for k, (t, i, j, s) in enumerate(msgs):
        y = top + 40 + step * k
        g = []
        if t == "s":
            x = xs[i]
            g.append('<path d="M%.1f %.1f h34 a14 14 0 0 1 0 28 h-30" fill="none" stroke="%s" stroke-width="3" '
                     'marker-end="url(#o5p)"/>' % (x, y - 4, PINK))
            g.append(ml(x, y - 30, s, 19, INK, 700))
        else:
            x1, x2 = xs[i], xs[j]
            g.append(ed([(x1, y), (x2 - 6, y)], dash=(t == "d"), col=PINK, mk="o5p", w=3))
            n = len(s.split("|"))
            g.append(ml((x1 + x2) / 2, y - 16 - (n - 1) * 12, s, 19, INK, 700))
        o.append('<g data-ph="%d">%s</g>' % (k + 1, "".join(g)))
    return scene(svg_only("0 0 %d %d" % (W, H), "".join(o), DEFS), caps)


def s41_image58():
    m = [("s", 0, 0, "Узнаёт префикс из своей области"), ("m", 0, 1, "LSA-3 · «этот префикс доступен»"),
         ("m", 1, 2, "LSA-3 · объявление в своей области"), ("s", 2, 2, "Выбирает маршрут через ABR")]
    return seq(["ABR-1", "ABR-2", "Маршрутизатор другой области"], [200, 640, 1080], m,
               ["ABR-1, ABR-2 и маршрутизатор другой области"] + [x[3] for x in m], 1300)


def s43_image63():
    m = [("d", 0, 1, "Внешний маршрут"), ("m", 1, 2, "LSA-5 · объявление внешнего префикса"),
         ("m", 2, 3, "Передаёт LSA-5 в область,|принимающую внешние маршруты"), ("s", 3, 3, "Устанавливает внешний маршрут")]
    return seq(["Внешний источник", "ASBR", "ABR", "Маршрутизатор другой области"], [130, 420, 800, 1170], m,
               ["Внешний источник, ASBR, ABR и маршрутизатор другой области"]
               + [x[3].replace("|", " ") for x in m], 1360)


def s51_image81():
    m = [("s", 0, 0, "LSA-1 отмечает маршрутизатор как ASBR"), ("m", 0, 1, "LSA-7 · внешний маршрут внутри NSSA"),
         ("s", 1, 1, "Преобразует подходящий LSA-7 в LSA-5"), ("m", 1, 2, "LSA-5 · внешний маршрут в магистрали"),
         ("m", 2, 3, "LSA-3 · маршрут по умолчанию в Stub")]
    return seq(["ASBR в NSSA", "ABR-1", "ABR-2", "Маршрутизатор в Stub"], [250, 590, 915, 1225], m,
               ["ASBR в NSSA, ABR-1, ABR-2 и маршрутизатор в Stub"] + [x[3] for x in m], 1380)


FIGS = {k: v for k, v in globals().items() if k[:1] == "s" and "_image" in k and callable(v)}
