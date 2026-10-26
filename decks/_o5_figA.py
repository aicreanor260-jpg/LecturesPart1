# -*- coding: utf-8 -*-
"""Схемы pptx «OSPF 2.5», перерисованные в кавайном стиле деки (часть A: слайды 6–29).

FIGS = {"sNN_imageK": функция}; prev(key) — для _o5_figprev.py:
    python -X utf8 _o5_figprev.py _o5_figA prev s09_image8 --ph 1
Логика, подписи, адреса и метрики — дословно по картинкам `_o5_pptx/<ключ>.png`.
"""
import math

from _o5_figlib import (router, cloudsvg, scene, fig, svg_only, T, box,
                        PINK, BLUE, YEL, GRN, INK, SOFT)

RED = "#e5355a"
ORG = "#f0802a"
CAB = "#f59fc4"        # кабель (розовый)
CAB2 = "#8fbff0"       # кабель (голубой)


# ============================================================ общие примитивы
def rt(x, y, w=86, tone="b", name=None, fs=22, name_dy=None):
    """Роутер, (x, y) — центр корпуса; имя крупно под корпусом."""
    h = w * 0.27
    s = router(x, y - h / 2, w=w, tone=tone)
    if name:
        dy = name_dy if name_dy is not None else h / 2 + w * 0.16 + fs + 2
        s += T(x, y + dy, name, fs, INK, 800)
    return s


def edge_pt(x, y, w, tx, ty):
    """Точка на краю корпуса роутера (центр x,y) в сторону (tx,ty)."""
    a, b = w / 2 + 2, w * 0.30
    dx, dy = tx - x, ty - y
    k = 1 / math.sqrt((dx / a) ** 2 + (dy / b) ** 2) if (dx or dy) else 0
    return x + dx * k, y + dy * k


def cable(p1, p2, w1=None, w2=None, col=CAB, sw=5):
    """Кабель между двумя точками; если задан w — обрезаем по краю роутера."""
    (x1, y1), (x2, y2) = p1, p2
    a = edge_pt(x1, y1, w1, x2, y2) if w1 else (x1, y1)
    b = edge_pt(x2, y2, w2, x1, y1) if w2 else (x2, y2)
    return ('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%d" stroke-linecap="round" fill="none"/>'
            % (a + b + (col, sw)))


def darrow(x1, y1, x2, y2, tone="b", sw=4, start=True, end=True, extra=""):
    ms = ' marker-start="url(#m_%s)"' % ("a" + tone) if start else ""
    me = ' marker-end="url(#m_%s)"' % ("a" + tone) if end else ""
    col = {"b": "#3b9eff", "g": "#3fc47c", "p": "#ff5c9e", "k": "#121212"}[tone]
    return ('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%d" stroke-linecap="round" fill="none"%s%s%s/>'
            % (x1, y1, x2, y2, col, sw, ms, me, extra))


def par_arrow(p1, p2, off, cut=58, tone="b", both=True, sw=4):
    """Стрелка параллельно отрезку p1→p2, сдвинутая на off по нормали."""
    (x1, y1), (x2, y2) = p1, p2
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    return darrow(x1 + ux * cut + nx * off, y1 + uy * cut + ny * off,
                  x2 - ux * cut + nx * off, y2 - uy * cut + ny * off, tone, sw, start=both)


def tagr(x, y, text, tone="y", ang=0, fs=17):
    """Плашка-пакет («Привет, я R1», «R1 LSP»), повёрнутая на ang."""
    fill, st = {"y": ("#fff3c4", "#efcf6a"), "g": ("#e6f7ec", "#86d3a8")}[tone]
    w = len(text) * fs * 0.58 + 22
    h = fs * 1.75
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f)">%s%s</g>'
            % (x, y, ang, box(-w / 2, -h / 2, w, h, fill, st, r=8, sw=2.2),
               T(0, fs * 0.36, text, fs, INK, 800)))


def lines(x, y, rows, fs=18, col=INK, w=600, anchor="start", lh=None, mono=False):
    lh = lh or fs * 1.3
    return "".join(T(x, y + i * lh, r, fs, col, w, anchor, mono) for i, r in enumerate(rows))


def table(x, y, cws, rh, rows, fs=18, head_fill="#e3f0fd", colors=None, ph_cols=None):
    """Таблица SVG. rows[0] — шапка. colors(r, c) -> цвет текста. ph_cols={c: шаг} — столбец появляется с шага."""
    o = []
    W, H = sum(cws), rh * len(rows)
    o.append(box(x, y, W, H, "#fff", "#9fc6ee", r=12, sw=2.5))
    o.append('<path d="M%.1f %.1f h%.1f v%.1f h%.1f Z" fill="%s"/>' % (x + 1.5, y + rh, W - 3, -rh + 12, -W + 3, head_fill))
    o.append(box(x + 1.5, y + 1.5, W - 3, rh - 1.5, head_fill, "none", r=11, sw=0))
    for i in range(1, len(rows)):
        o.append('<path d="M%.1f %.1f h%.1f" stroke="#cfe2f6" stroke-width="2"/>' % (x, y + rh * i, W))
    cx = x
    for c in cws[:-1]:
        cx += c
        o.append('<path d="M%.1f %.1f v%.1f" stroke="#cfe2f6" stroke-width="2"/>' % (cx, y, H))
    for r, row in enumerate(rows):
        cx = x
        for c, (cw, cell) in enumerate(zip(cws, row)):
            col = colors(r, c) if (colors and r) else INK
            t = T(cx + cw / 2, y + rh * r + rh / 2 + fs * 0.36, cell, fs, col, 800 if r == 0 else 700)
            if ph_cols and c in ph_cols and r:
                t = '<g data-ph="%d">%s</g>' % (ph_cols[c], t)
            o.append(t)
            cx += cw
    return "".join(o)


def ph(n, s, only=False):
    return '<g data-ph="%d"%s>%s</g>' % (n, " data-ph-only" if only else "", s)


# ============================================================ s06: три области
def f_s06():
    S = 2.0
    N = {"A": (40, 72), "B": (136, 30), "C": (232, 70), "D": (112, 123), "E": (188, 122),
         "F": (290, 22), "H": (290, 120), "G": (348, 70),
         "I": (445, 25), "J": (540, 63), "K": (420, 120), "L": (497, 120)}
    N = {k: (v[0] * S + 20, v[1] * S + 40) for k, v in N.items()}
    w = 74
    o = [cloudsvg(300, 200, 560, 300, tone="y"), cloudsvg(600, 190, 220, 340, tone="v"),
         cloudsvg(940, 195, 560, 320, tone="g")]
    o.append(T(330, 225, "Область 1.1.1.1", 24, INK, 800))
    o.append(T(600, 212, "Область 0.0.0.0", 17, INK, 800))
    o.append(T(930, 230, "Область 2.2.2.2", 24, INK, 800))
    links = [("A", "B", "b"), ("B", "C", "b"), ("A", "D", "b"), ("D", "E", "b"), ("E", "C", "b"),
             ("C", "F", "b"), ("F", "G", "b"), ("C", "H", "b"), ("H", "G", "b"),
             ("G", "I", "g"), ("I", "J", "g"), ("J", "L", "g"), ("L", "K", "g"), ("G", "K", None)]
    offs = {"A": 1, "B": 1, "C": 1}
    for a, b, tone in links:
        o.append(cable(N[a], N[b], w, w, col="#3a3550", sw=4))
    for a, b, tone in links:
        if tone:
            pa, pb = N[a], N[b]
            mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
            # стрелка — снаружи кольца (от центра своей области)
            cx = 330 if a in "ABCDE" and b in "ABCDE" else (600 if tone == "b" else 930)
            L = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
            nx, ny = -(pb[1] - pa[1]) / L, (pb[0] - pa[0]) / L
            sgn = 1 if (mx + nx - cx) ** 2 + (my + ny - 205) ** 2 > (mx - cx) ** 2 + (my - 205) ** 2 else -1
            o.append(par_arrow(pa, pb, 22 * sgn, cut=50, tone=tone))
    # красный крест на канале G–K
    gx, gy = N["G"]
    kx, ky = N["K"]
    mx, my = gx + (kx - gx) * 0.42, gy + (ky - gy) * 0.42
    o.append('<path d="M%.1f %.1f l26 26 M%.1f %.1f l-26 26" stroke="%s" stroke-width="7" stroke-linecap="round"/>'
             % (mx - 13, my - 13, mx + 13, my - 13, RED))
    for k, (x, y) in N.items():
        o.append(rt(x, y, w, "b"))
    return fig("0 -30 1200 410", "".join(o))


# ============================================================ Дейкстра
DN = {"R1": (120, 105), "R5": (600, 105), "R3": (360, 228), "R2": (120, 390), "R4": (600, 390)}
DE = [("R1", "R5", 15, (360, 88)), ("R1", "R3", 10, (228, 186)), ("R3", "R5", 3, (488, 150)),
      ("R1", "R2", 8, (90, 255)), ("R2", "R3", 11, (228, 290)), ("R3", "R4", 12, (492, 290)),
      ("R5", "R4", 16, (632, 255)), ("R2", "R4", 16, (360, 374))]
DW = 100
LPOS = {"R1": (120, 20), "R5": (600, 20), "R3": (285, 145), "R2": (40, 360), "R4": (680, 360)}


def _weight(a, b):
    for e in DE:
        if {e[0], e[1]} == {a, b}:
            return e
    raise KeyError((a, b))


def _dbase():
    o = []
    for a, b, wgt, (lx, ly) in DE:
        o.append(cable(DN[a], DN[b], DW, DW, col="#3a3550", sw=4))
    for a, b, wgt, (lx, ly) in DE:
        o.append(T(lx, ly + 9, str(wgt), 26, INK, 800))
    for k, (x, y) in DN.items():
        o.append(rt(x, y, DW, "b", k, 24))
    return "".join(o)


def _circ(x, y, r=21, col=RED):
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="3.2"/>' % (x, y, r, col)


def _xmark(x, y, s, col, sw):
    return ('<path d="M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
            % (x - s, y - s, x + s, y + s, x + s, y - s, x - s, y + s, col, sw))


def _dstate(st):
    """st: lab{узел: текст}, circ{узлы с обведённой меткой}, old{узел: зачёркнутое значение},
    vis{посещённые}, cur — текущий, edge=(откуда, куда, сторона стрелки)."""
    o = []
    lab, circ, old = st.get("lab", {}), st.get("circ", set()), st.get("old", {})
    for k, (x, y) in DN.items():
        if k not in lab:
            continue
        lx, ly = LPOS[k]
        if k in old:
            o.append(T(lx - 4, ly + 9, old[k], 26, RED, 800))
            o.append(_xmark(lx - 4, ly, 14, BLUE, 4))
            lx += 44
        o.append(T(lx, ly + 9, lab[k], 26, RED, 800))
        if k in circ or k in old:
            o.append(_circ(lx, ly, 22))
    if st.get("edge"):
        a, b, side = st["edge"]
        e = _weight(a, b)
        o.append(_circ(e[3][0], e[3][1], 22))
        o.append(par_arrow(DN[a], DN[b], 30 * side, cut=70, tone="p", both=False, sw=5))
    for k in st.get("vis", ()):
        x, y = DN[k]
        o.append(_xmark(x, y - 4, 40, RED, 9))
    if st.get("cur"):
        x, y = DN[st["cur"]]
        o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="6"/>'
                 % (x, y - 2, DW * 0.74, DW * 0.52, RED))
    return "".join(o)


INF = "∞"


def _dscene(states, caps):
    body = _dbase() + "".join(ph(i, _dstate(s), only=True) for i, s in enumerate(states))
    return scene(svg_only("0 -15 760 475", body), caps)


def f_s09():
    allinf = {"R1": "0", "R2": INF, "R3": INF, "R4": INF, "R5": INF}
    return _dscene([
        {},
        {"lab": allinf, "cur": "R1"},
        {"lab": dict(allinf, R2="8"), "cur": "R1", "edge": ("R1", "R2", 1)},
    ], ["Граф: маршрутизаторы R1–R5 и стоимости каналов",
        "Старт в R1: метка 0, у остальных — ∞",
        "R1 → R2: 0 + 8 = 8 < ∞ — метка R2 = 8"])


def f_s10():
    base = {"R1": "0", "R2": "8", "R3": "10", "R4": INF, "R5": INF}
    return _dscene([
        {"lab": base, "cur": "R1", "edge": ("R1", "R3", 1)},
        {"lab": dict(base, R5="15"), "cur": "R1", "edge": ("R1", "R5", -1)},
        {"lab": dict(base, R5="15"), "vis": {"R1"}},
    ], ["R1 → R3: 0 + 10 = 10 — метка R3 = 10",
        "R1 → R5: 0 + 15 = 15 — метка R5 = 15",
        "Все соседи R1 просмотрены — R1 вычёркиваем"])


def f_s11():
    base = {"R1": "0", "R2": "8", "R3": "10", "R4": INF, "R5": "15"}
    return _dscene([
        {"lab": base, "circ": {"R2", "R3"}, "vis": {"R1"}, "cur": "R2", "edge": ("R2", "R3", 1)},
        {"lab": dict(base, R4="24"), "vis": {"R1"}, "cur": "R2", "edge": ("R2", "R4", -1)},
    ], ["Текущий R2 (метка 8). R2 → R3: 8 + 11 = 19 > 10 — метка R3 остаётся 10",
        "R2 → R4: 8 + 16 = 24 < ∞ — метка R4 = 24"])


def f_s12():
    base = {"R1": "0", "R2": "8", "R3": "10", "R4": "22", "R5": "15"}
    return _dscene([
        {"lab": base, "old": {"R4": "24"}, "circ": {"R3"}, "vis": {"R1", "R2"}, "cur": "R3",
         "edge": ("R3", "R4", 1)},
        {"lab": dict(base, R5="13"), "old": {"R5": "15"}, "circ": {"R3"}, "vis": {"R1", "R2"}, "cur": "R3",
         "edge": ("R3", "R5", -1)},
    ], ["Текущий R3 (метка 10). R3 → R4: 10 + 12 = 22 < 24 — метка R4 = 22",
        "R3 → R5: 10 + 3 = 13 < 15 — метка R5 = 13"])


def f_s13():
    base = {"R1": "0", "R2": "8", "R3": "10", "R4": "22", "R5": "13"}
    return _dscene([
        {"lab": base, "circ": {"R4", "R5"}, "vis": {"R1", "R2", "R3"}, "cur": "R4", "edge": ("R4", "R5", -1)},
        {"lab": base, "vis": {"R1", "R2", "R3", "R4"}, "cur": "R5"},
        {"lab": base, "vis": {"R1", "R2", "R3", "R4", "R5"}},
    ], ["Текущий R4 (метка 22). R4 → R5: 22 + 16 = 38 > 13 — метка R5 остаётся 13",
        "R4 вычеркнут, текущий R5",
        "Все вершины просмотрены: R2 = 8, R3 = 10, R5 = 13, R4 = 22"])


# ============================================================ s14: стоимость
def f_s14():
    o = []
    for x0, title in [(10, "Стоимость интерфейса OSPF"), (720, "Общая стоимость пути OSPF")]:
        o.append(box(x0, 10, 670, 500, "#fff", "#9fc6ee", r=20, sw=2.5))
        o.append(box(x0 + 2, 12, 666, 54, "#e3f0fd", "none", r=18, sw=0))
        o.append(T(x0 + 335, 48, title, 26, "#1f6fc4", 800))
    # левая панель
    cx, cy = 300, 225
    o.append(cable((70, cy), (cx, cy), None, 70, col="#3a3550", sw=4))
    o.append(cable((cx, cy), (560, cy), 70, None, col="#3a3550", sw=4))
    o.append(cable((cx, 95), (cx, cy), None, 70, col="#3a3550", sw=4))
    o.append(rt(cx, cy, 70, "b"))
    o.append(lines(318, 112, ["Последовательный", "интерфейс (1,544 Мбит / с)"], 21))
    o.append(T(318, 172, "Стоимость по умолчанию = 64", 18, SOFT, 700, "start"))
    o.append(lines(180, 285, ["Интерфейс FE", "Стоимость по", "умолчанию = 1"], 20, anchor="middle"))
    o.append(lines(450, 285, ["Интерфейс GE", "Стоимость по", "умолчанию = 1"], 20, anchor="middle"))
    o.append(T(40, 420, "•", 22, PINK, 800, "start"))
    o.append(lines(62, 420, ["Каждый интерфейс OSPF имеет", "определенную стоимость, зависящую от",
                             "пропускной способности."], 20, col="#7a5a00"))
    # правая панель
    ys = 245
    R = [(800, "R1"), (1060, "R2"), (1310, "R3")]
    o.append(cable((800, 130), (800, ys), None, 70, col="#3a3550", sw=4))
    o.append(T(830, 120, "1.1.1.0/24", 21, INK, 700))
    o.append(cable(R[0][:1] + (ys,), (1060, ys), 70, 70, col="#3a3550", sw=4))
    o.append(cable((1060, ys), (1310, ys), 70, 70, col="#3a3550", sw=4))
    for x, n in R:
        o.append(rt(x, ys, 70, "b", n, 22))
    o.append(lines(785, 165, ["Стоимость", "= 10"], 21, anchor="end"))
    o.append(T(930, 230, "Стоимость = 1", 20, PINK, 800))
    o.append(T(1185, 230, "Стоимость = 64", 20, PINK, 800))
    o.append(T(750, 420, "•", 22, PINK, 800, "start"))
    o.append(lines(772, 420, ["В таблице маршрутизации R3 стоимость маршрута", "OSPF до 1.1.1.0/24 составляет 75",
                              "(10 + 1 + 64)."], 20, col="#7a5a00"))
    return fig("0 0 1400 520", "".join(o))


# ============================================================ топология R1..R5 (s15_image20, s17, s18, s20)
TN = {"R1": (260, 100), "R2": (820, 100), "R5": (540, 235), "R4": (260, 430), "R3": (820, 430)}
TW = 84
LANS = {"LAN1": ((95, 98), "192.168.1.0/24", "y", "R1"), "LAN2": ((985, 98), "192.168.2.0/24", "g", "R2"),
        "LAN5": ((735, 232), "192.168.5.0/24", "v", "R5"), "LAN4": ((95, 432), "192.168.4.0/24", "b", "R4"),
        "LAN3": ((985, 432), "192.168.3.0/24", "y", "R3")}
TLINKS = [("R1", "R2", "20", (540, 84), "203.0.113.0/30", (540, 55)),
          ("R2", "R3", "10", (848, 270), "203.0.113.4/30", (905, 300)),
          ("R4", "R3", "10", (540, 418), "203.0.113.8/30", (540, 470)),
          ("R1", "R4", "20", (285, 260), "203.0.113.12/30", (175, 290)),
          ("R1", "R5", "5", (378, 188), "203.0.113.16/30", (430, 150)),
          ("R4", "R5", "10", (370, 340), "203.0.113.20/30", (470, 345))]
LANMET = {"LAN1": (205, 82), "LAN2": (875, 82), "LAN5": (615, 220), "LAN4": (205, 415), "LAN3": (875, 415)}


def _topo(lan_labels=True, all_labels=True):
    o = []
    for n, ((x, y), net, tone, r) in LANS.items():
        o.append(cable((x, y), TN[r], None, TW, col=CAB2, sw=5))
    for a, b, *_ in TLINKS:
        o.append(cable(TN[a], TN[b], TW, TW, col=CAB, sw=5))
    for n, ((x, y), net, tone, r) in LANS.items():
        show = lan_labels or n == "LAN1"
        o.append(cloudsvg(x, y, 175, 86, n if show else None, net if show else None, tone, fs=19))
        if all_labels or n == "LAN1":
            o.append(T(LANMET[n][0], LANMET[n][1], "1", 20, RED, 800))
    for a, b, met, mp, net, np_ in TLINKS:
        if all_labels or "R1" in (a, b):
            o.append(T(mp[0], mp[1], met, 20, RED, 800))
            o.append(T(np_[0], np_[1], net, 19, INK, 700))
    for k, (x, y) in TN.items():
        o.append(rt(x, y, TW, "b", k, 21))
    return "".join(o)


def f_s20():
    return fig("0 0 1080 490", _topo())


def f_s15_20():
    return fig("0 0 1080 490", _topo())


# ============================================================ s15_image21: R1, его сети и таблица
R1NET = [["Сеть", "IP-адрес", "Интерфейс", "Метрика", "Сосед"],
         ["192.168.1.0/24", "192.168.1.1", "gi1/0/1", "1", "?"],
         ["203.0.113.0/30", "203.0.113.1", "gi1/0/2", "20", "?"],
         ["203.0.113.12/30", "203.0.113.13", "gi1/0/4", "20", "?"],
         ["203.0.113.16/30", "203.0.113.17", "gi1/0/5", "5", "?"]]
CWS = [230, 190, 160, 130, 120]


def _r1_table(x, y, rows, colors, ph_cols=None):
    o = [rt(x, y + 120, 96, "b", "R1", 22)]
    tx = x + 150
    o.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="#e3f0fd" stroke="#9fc6ee" stroke-width="2"/>'
             % (x + 52, y + 120, tx, y, tx, y + 5 * 48))
    o.append(table(tx, y, CWS, 48, rows, 19, colors=colors, ph_cols=ph_cols))
    return "".join(o)


def f_s15_21():
    o = []
    rx, ry = 330, 90
    o.append(cable((150, ry), (rx, ry), None, TW, col=CAB2, sw=5))
    o.append(cable((rx, ry), (1050, ry), TW, None, col=CAB, sw=5))
    o.append(cable((rx, ry), (rx, 330), TW, None, col=CAB, sw=5))
    o.append(cable((rx, ry), (650, 270), TW, None, col=CAB, sw=5))
    o.append(cloudsvg(130, 85, 200, 96, "LAN1", "192.168.1.0/24", "y", fs=20))
    o.append(rt(rx, ry, TW, "b", "R1", 21))
    o.append(T(250, 40, "gi1/0/1", 20, INK, 700))
    o.append(T(250, 76, "1", 20, RED, 800))
    o.append(T(420, 70, "gi1/0/2", 20, INK, 700, "start"))
    o.append(T(760, 70, "20", 20, RED, 800))
    o.append(T(850, 122, "203.0.113.0/30", 20, INK, 700))
    o.append(T(300, 210, "gi1/0/4", 20, INK, 700, extra=' transform="rotate(-90 300 210)"'))
    o.append(T(370, 260, "203.0.113.12/30", 20, INK, 700, extra=' transform="rotate(-90 370 260)"'))
    o.append(T(285, 280, "20", 20, RED, 800))
    o.append(T(560, 175, "203.0.113.16/30", 20, INK, 700, extra=' transform="rotate(30 560 175)"'))
    o.append(T(450, 200, "gi1/0/5", 20, INK, 700, extra=' transform="rotate(30 450 200)"'))
    o.append(T(500, 222, "5", 20, RED, 800))

    def col(r, c):
        return RED if c == 0 or c == 3 else INK
    o.append(_r1_table(60, 380, R1NET, col))
    return fig("0 0 1080 640", "".join(o))


# ============================================================ s16: hello — сцена
def f_s16():
    N = {"R1": (330, 120), "R2": (1000, 120), "R5": (680, 285), "R4": (330, 470)}
    o = []
    o.append(cable((150, 118), N["R1"], None, TW, col=CAB2, sw=5))
    for b in ("R2", "R5", "R4"):
        o.append(cable(N["R1"], N[b], TW, TW, col=CAB, sw=5))
    o.append(cloudsvg(130, 118, 200, 96, "LAN1", "192.168.1.0/24", "y", fs=20))
    o.append(T(250, 105, "1", 20, RED, 800))
    o.append(T(800, 152, "203.0.113.0/30", 20, INK, 700))
    o.append(T(530, 180, "203.0.113.16/30", 19, INK, 700, extra=' transform="rotate(25 530 180)"'))
    o.append(T(530, 252, "5", 20, RED, 800))
    o.append(T(368, 300, "203.0.113.12/30", 19, INK, 700, extra=' transform="rotate(-90 368 300)"'))
    for k, (x, y) in N.items():
        o.append(rt(x, y, TW, "b", k, 21))
    # шаг 1: R1 рассылает «Привет, я R1»
    s1 = [tagr(250, 40, "Привет, я R1", "y"), tagr(820, 40, "Привет, я R1", "y"),
          tagr(255, 400, "Привет, я R1", "y", -90), tagr(640, 360, "Привет, я R1", "y", 27),
          darrow(410, 60, 900, 60, "b", 4, start=False),
          darrow(305, 200, 305, 445, "b", 4, start=False),
          darrow(410, 205, 660, 345, "b", 4, start=False)]
    o.append(ph(1, "".join(s1)))
    # шаг 2: ответы R2, R4, R5
    s2 = [tagr(600, 40, "Привет, я R2", "g"), tagr(255, 240, "Привет, я R4", "g", -90),
          tagr(480, 300, "Привет, я R5", "g", 27),
          darrow(410, 60, 900, 60, "b", 4, end=False),
          darrow(305, 200, 305, 445, "b", 4, end=False),
          darrow(410, 205, 660, 345, "b", 4, end=False),
          T(655, 82, "20", 20, RED, 800), T(282, 330, "20", 20, RED, 800)]
    o.append(ph(2, "".join(s2)))
    rows = [["Сеть", "IP-адрес", "Интерфейс", "Метрика", "Сосед"],
            ["192.168.1.0/24", "192.168.1.1", "gi1/0/1", "1", "нет"],
            ["203.0.113.0/30", "203.0.113.1", "gi1/0/2", "20", "R2"],
            ["203.0.113.12/30", "203.0.113.13", "gi1/0/4", "20", "R4"],
            ["203.0.113.16/30", "203.0.113.17", "gi1/0/5", "5", "R5"]]

    def col(r, c):
        return RED if c == 4 else INK
    o.append(_r1_table(60, 560, rows, col, ph_cols={4: 2}))
    return scene(svg_only("0 0 1080 820", "".join(o)),
                 ["R1 и его соседи по каналам gi1/0/1, gi1/0/2, gi1/0/4, gi1/0/5",
                  "R1 отправляет «Привет, я R1» из всех своих интерфейсов",
                  "R2, R4 и R5 отвечают своими hello — столбец «Сосед» заполнен; за gi1/0/1 соседа нет"])


# ============================================================ s17: R1 LSP
def f_s17():
    o = [_topo(lan_labels=False, all_labels=False), tagr(260, 20, "R1 LSP", "y")]
    rows = [["Сеть", "Интерфейс", "Метрика", "Сосед"],
            ["192.168.1.0/24", "gi1/0/1", "1", "нет"],
            ["203.0.113.0/30", "gi1/0/2", "20", "R2"],
            ["203.0.113.12/30", "gi1/0/4", "20", "R4"],
            ["203.0.113.16/30", "gi1/0/5", "5", "R5"]]
    x0, y0 = 250, 545
    o.append('<path d="M%.1f %.1f h620 l-70 300 h-620 Z" fill="#ffe9a8" stroke="#efcf6a" stroke-width="2.5"/>'
             % (x0 + 30, y0))
    o.append(T(x0 + 305, y0 + 34, "R1 LSP", 24, INK, 800))
    o.append(table(x0 + 25, y0 + 52, [200, 150, 120, 100], 46, rows, 19, head_fill="#fff3c4"))
    return fig("-20 -10 1110 860", "".join(o))


# ============================================================ s18: лавинная рассылка LSP — сцена
def f_s18():
    o = [_topo()]

    def lsp(a, b, t=0.62, side=1, off=34, step=1):
        (x1, y1), (x2, y2) = TN[a], TN[b]
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = -uy * side, ux * side
        ang = math.degrees(math.atan2(uy, ux))
        if ang > 90:
            ang -= 180
        if ang < -90:
            ang += 180
        px, py = x1 + (x2 - x1) * t + nx * off, y1 + (y2 - y1) * t + ny * off
        s = tagr(px, py, "R1 LSP", "y", ang)
        s += darrow(x1 + ux * 70 + nx * (off + 26), y1 + uy * 70 + ny * (off + 26),
                    x2 - ux * 70 + nx * (off + 26), y2 - uy * 70 + ny * (off + 26), "p", 4, start=False)
        return ph(step, s)
    o.append(lsp("R1", "R2", side=-1, off=34, t=0.8))
    o.append(lsp("R1", "R5", side=1, off=34))
    o.append(lsp("R1", "R4", side=1, off=-62))
    o.append(lsp("R2", "R3", side=1, off=40, step=2))
    o.append(lsp("R4", "R3", side=1, off=-34, step=2))
    o.append(lsp("R4", "R5", side=-1, off=-34, t=0.35, step=2))
    return scene(svg_only("0 -10 1080 500", "".join(o)),
                 ["Топология: R1–R5 и сети LAN1–LAN5",
                  "R1 отправляет свой LSP соседям R2, R5 и R4",
                  "Соседи пересылают R1 LSP дальше — LSP R1 есть у всех маршрутизаторов"])


# ============================================================ s22: базы данных / сообщения / алгоритм
def f_s22():
    o = []
    bands = [(0, "Базы\nданных", "#fff4d6", "#efcf6a"), (190, "Сообщения", "#e6f7ec", "#86d3a8"),
             (380, "Алгоритм", "#e3f0fd", "#8fbff0")]
    for y, name, fill, st in bands:
        o.append(box(4, y + 4, 1152, 178, fill, st, r=20, sw=3))
        ls = name.split("\n")
        o.append(lines(100, y + 100 - (len(ls) - 1) * 14, ls, 28, INK, 800, "middle", lh=32))
    db = ["OSPF создаёт и поддерживает:", "- База данных соседей", "- База данных состояния каналов",
          "- Таблица маршрутизации"]
    alg = ["Буду использовать Алгоритм Дейкстры,", "чтобы найти оптимальные маршруты и",
           "добавить их в таблицу маршрутизации"]
    for x in (210, 690):
        o.append(box(x, 22, 440, 140, "#ffe39a", "#f2b705", r=16, sw=2.5))
        o.append(lines(x + 22, 56, db, 19, INK, 800, lh=28))
        o.append(box(x, 402, 440, 140, "#cfe4fb", "#4f97e6", r=16, sw=2.5))
        o.append(lines(x + 220, 446, alg, 19, INK, 800, "middle", lh=30))
    R = [(290, "R1"), (1060, "R2")]
    for x, n in R:
        o.append(darrow(x, 218, x, 170, "b", 5, start=False))
        o.append(darrow(x, 398, x, 338, "b", 5, start=False))
    o.append(box(440, 210, 300, 150, "#c6efd6", "#3fc47c", r=16, sw=2.5))
    o.append(lines(590, 240, ["Hello-пакет", "Пакет  Database Description", "Пакет Link State Request",
                              "Пакет Link State Update", "Link State Acknowledgment"], 18, INK, 800, "middle", lh=27))
    o.append(darrow(345, 285, 432, 285, "b", 5))
    o.append(darrow(748, 285, 1000, 285, "b", 5))
    for x, n in R:
        o.append(rt(x, 280, 80, "b", n, 20))
    return fig("0 0 1160 570", "".join(o))


# ============================================================ s24: R1·BDR — сегмент — R2·DR
def f_s24():
    o = [cable((330, 80), (430, 80), col=CAB2, sw=4), cable((770, 80), (870, 80), col=CAB2, sw=4)]
    for x, w, a, b in [(20, 310, "R1 · BDR", "203.0.113.1/24"), (430, 340, "Общий сегмент Ethernet", "203.0.113.0/24"),
                       (870, 310, "R2 · DR", "203.0.113.2/24")]:
        o.append(box(x, 20, w, 120, "#e3f0fd", "#8fbff0", r=24, sw=2.5))
        o.append(T(x + w / 2, 72, a, 24, "#1f4f9a", 800))
        o.append(T(x + w / 2, 106, b, 22, "#1f4f9a", 700))
    return fig("0 0 1200 160", "".join(o))


# ============================================================ s25: последовательность Hello…FULL — сцена
def f_s25():
    X = [190, 600, 1010]
    names = ["R1 · BDR", "Ethernet-сегмент", "R2 · DR"]
    rows = [("m", 0, 1, "Hello · Router ID R1 · 224.0.0.5"),
            ("m", 1, 2, "Hello от R1"),
            ("m", 2, 1, "Hello · Router ID R2 · список соседей"),
            ("m", 1, 0, "Hello от R2, в списке есть R1"),
            ("b", 0, 0, "Двусторонняя связь · TWO-WAY"),
            ("m", 2, 0, "DBD · краткое содержание базы состояний каналов"),
            ("m", 0, 2, "DBD · краткое содержание своей базы"),
            ("b", 0, 0, "Сравнение сведений · EXCHANGE"),
            ("m", 0, 2, "LSR · запрос недостающих или устаревших LSA"),
            ("m", 2, 0, "LSU · передача LSA"),
            ("m", 0, 2, "LSAck · подтверждение получения LSA"),
            ("b", 0, 0, "Базы синхронизированы · FULL")]
    top, step = 100, 56
    bottom = top + step * len(rows) + 30
    o = []
    for x, n in zip(X, names):
        o.append('<path d="M%.1f %.1f V%.1f" stroke="#b9c4d6" stroke-width="3"/>' % (x, top - 20, bottom))
    for y in (20, bottom):
        for x, n in zip(X, names):
            o.append(box(x - 130, y, 260, 62, "#e3f0fd", "#8fbff0", r=14, sw=2.5))
            o.append(T(x, y + 39, n, 22, "#1f4f9a", 800))
    for i, (k, a, b, t) in enumerate(rows):
        y = top + 40 + i * step
        if k == "m":
            s = darrow(X[a], y, X[b], y, "p" if a < b else "b", 4, start=False)
            s += T((X[a] + X[b]) / 2, y - 12, t, 20, INK, 700)
        else:
            s = box(X[0] - 120, y - 30, X[2] - X[0] + 240, 46, "#e6f7ec", "#3fc47c", r=12, sw=2.5)
            s += T(X[1], y + 1, t, 21, "#1d8a51", 800)
        o.append(ph(i + 1, s))
    caps = ["R1 (BDR) и R2 (DR) на общем Ethernet-сегменте"] + [r[3] for r in rows]
    return scene(svg_only("0 0 1200 %d" % (bottom + 90), "".join(o)), caps)


# ============================================================ s27–s29: обмен R1 ↔ R2
XL, XR = 440, 990


def _pair(ids, top_lab):
    o = []
    for x, n, lab, anc, nx in [(XL, "R1", top_lab[0], "start", XL - 70), (XR, "R2", top_lab[1], "start", XR + 70)]:
        o.append(lines(x - 110, 30, lab, 21, INK, 700))
    o.append(cable((XL, 110), (XR, 110), 84, 84, col=CAB, sw=5))
    o.append(rt(XL, 110, 84, "b"))
    o.append(rt(XR, 110, 84, "b"))
    o.append(T(XL - 72, 118, "R1", 24, INK, 800, "end"))
    o.append(T(XR + 72, 118, "R2", 24, INK, 800, "start"))
    return "".join(o)


def _life(y2):
    return "".join('<path d="M%.1f 140 V%.1f" stroke="%s" stroke-width="3" stroke-dasharray="8 6"/>'
                   % (x, y2, "#8fd0f5") for x in (XL, XR))


def _msg(y, rows, right, bold=None):
    """Сообщение: rows — строки подписи над стрелкой; right=True — R1→R2."""
    fs, lh = 19, 25
    o = []
    y0 = y - 12 - lh * (len(rows) - 1)
    for i, r in enumerate(rows):
        w = 800 if (bold is not None and i == 0) else 600
        if right:
            o.append(T(XL + 14, y0 + i * lh, r, fs, INK, w, "start"))
        else:
            o.append(T(XR - 14, y0 + i * lh, r, fs, INK, w, "end"))
    o.append(darrow(XL, y, XR, y, "p", 4, start=False) if right else darrow(XR, y, XL, y, "p", 4, start=False))
    return "".join(o)


def _side(x, y, rows, anchor, head=None, fs=18):
    o = []
    if head:
        o.append(lines(x, y, head, 22, ORG, 700, anchor, lh=28))
        y += 28 * len(head) + 8
    o.append(lines(x, y, rows, fs, INK, 600, anchor, lh=fs * 1.3))
    return "".join(o)


def _bubble(x, y, rows):
    return (box(x - 130, y, 260, 84, "#e8f6fd", "#5bbbe8", r=40, sw=2.5)
            + lines(x, y + 26, rows, 18, INK, 700, "middle", lh=24))


def f_s27():
    o = [_pair(None, (["Зона 1.1.1.1"], ["Зона 2.2.2.2"])), _life(660)]
    o.append(ph(1, _msg(230, ["Пакеты Hello", "Я - 1.1.1.1. Я не знаю, кто есть в этом", "канале."], True)
                + T(XR + 18, 222, "Init (<tspan style=\"fill:%s\">Инициирование</tspan>)" % ORG, 22, INK, 700, "start")
                + _side(XR + 18, 258, ["Обнаружен R1 (1.1.1.1), добавлен", "в список соседей. Статус R1 в",
                                       "таблице соседей – Init."], "start")))
    o.append(ph(2, _msg(350, ["Пакеты Hello", "Я - 2.2.2.2. Я нашел соседа 1.1.1.1."], False)
                + _side(XL - 30, 340, ["Обнаружен R2 (2.2.2.2),", "добавлен в список соседей.", "Поскольку R2 меня",
                                       "обнаружил, я установил", "статус 2-way для R2 в", "таблице соседей."],
                        "end", head=["2-way"])))
    o.append(ph(3, _msg(510, ["Пакеты Hello", "Я -1.1.1.1. Я нашел соседа 2.2.2.2."], True)
                + _side(XR + 18, 510, ["Поскольку R1 нашел меня, я", "меняю статус для 1.1.1.1 на",
                                       "2-way в таблице соседей."], "start", head=["2-way"])))
    o.append(ph(4, box(XL + 140, 570, 200, 52, "#e8f6fd", "#5bbbe8", r=12, sw=2.5)
                + T(XL + 240, 603, "Мы соседи.", 21, INK, 700)))
    return scene(svg_only("0 0 1400 680", "".join(o)),
                 ["R1 и R2 на одном канале", "R1 → R2: Hello — R2 переходит в Init",
                  "R2 → R1: Hello со списком соседей — R1 ставит 2-way", "R1 → R2: Hello — R2 ставит 2-way",
                  "Мы соседи."])


def f_s28():
    o = [_pair(None, (["ID маршрутизатора:", "1.1.1.1"], ["ID маршрутизатора:", "2.2.2.2"])), _life(760)]
    o.append(ph(1, _msg(230, ["DD (содержимое пусто, порядковый номер – X.)",
                              "Я ведущий (master), мой ID маршрутизатора – 1.1.1.1."], True)
                + T(XL - 14, 237, "Ex-start (Начало обмена", 21, ORG, 700, "end")
                + T(XR + 18, 237, "Ex-start", 22, ORG, 700, "start")))
    o.append(ph(2, _msg(340, ["DD (содержимое пусто, порядковый номер – Y.)",
                              "Я ведущий (master), мой ID маршрутизатора 2.2.2.2."], False)
                + lines(XL - 14, 312, ["Exchange", "(обмен)", "(Ведущим становится R2,так",
                                       "как его ID маршрутизатора", "больше.)"], 20, ORG, 700, "end", lh=26)))
    o.append(ph(3, _msg(450, ["DD (порядковый номер Y)", "Это общая информация по LSA в моей базе LSDB."], True)
                + _side(XR + 18, 470, ["На фазе Exchange обе стороны", "обмениваются пакетами DD для",
                                       "описания собственных LSA."], "start", head=["Exchange", "(обмен)"])))
    o.append(ph(4, _msg(550, ["DD (порядковый номер Y + 1 в возрастающем порядке)",
                              "Это общая информация по LSA в моей базе LSDB."], False)))
    o.append(ph(5, _msg(660, ["DD (порядковый номер Y+1)", "Подтверждает пакет DD, отправленный ведущим",
                              "маршрутизатором."], True)))
    o.append(ph(6, _bubble(XL, 690, ["Я знаю, что", "содержится в LSDB", "маршрутизатора R2."])
                + _bubble(XR, 690, ["Я знаю, что", "содержится в LSDB", "маршрутизатора R1."])))
    return scene(svg_only("0 0 1400 790", "".join(o)),
                 ["R1 (ID 1.1.1.1) и R2 (ID 2.2.2.2)", "R1 → R2: пустой DD, «я ведущий» — Ex-start",
                  "R2 → R1: пустой DD, «я ведущий» — ведущим становится R2", "R1 → R2: DD с порядковым номером Y — Exchange",
                  "R2 → R1: DD с номером Y + 1", "R1 → R2: DD (Y+1) подтверждает пакет ведущего",
                  "Каждый знает, что содержится в LSDB соседа"])


def f_s29():
    o = [_pair(None, (["ID маршрутизатора:", "1.1.1.1"], ["ID маршрутизатора:", "2.2.2.2"])), _life(640)]
    o.append(ph(1, _msg(240, ["LSR", "Я хочу запросить полную информацию о xx", "LSA."], True, bold=0)
                + T(XL - 20, 248, "Loading", 22, ORG, 700, "end") + T(XR + 20, 248, "Loading", 22, ORG, 700, "start")))
    o.append(ph(2, _msg(340, ["LSU", "Это полная информация о запрошенном LSA."], False, bold=0)))
    o.append(ph(3, _msg(420, ["LS ACK", "Подтверждает получение LSU и xx LSA,", "переданного в LSU."], True, bold=0)))
    o.append(ph(4, _msg(510, ["LSR", "Я хочу запросить полную информацию о yyy", "LSA."], True, bold=0)))
    o.append(ph(5, T((XL + XR) / 2, 570, "• • •", 26, SOFT, 800)
                + T(XL - 20, 572, "Full", 22, ORG, 700, "end") + T(XR + 20, 572, "Full", 22, ORG, 700, "start")
                + _bubble(XL, 600, ["LSDB R1 и R2", "синхронизированы."])
                + _bubble(XR, 600, ["LSDB R1 и R2", "синхронизированы."])))
    return scene(svg_only("0 0 1400 700", "".join(o)),
                 ["R1 (ID 1.1.1.1) и R2 (ID 2.2.2.2)", "R1 → R2: LSR — запрос полной информации о xx LSA (Loading)",
                  "R2 → R1: LSU — полная информация о запрошенном LSA", "R1 → R2: LS ACK — подтверждение получения",
                  "R1 → R2: LSR — запрос о yyy LSA", "… Full: LSDB R1 и R2 синхронизированы"])


FIGS = {
    "s06_image4": f_s06,
    "s09_image8": f_s09, "s10_image10": f_s10, "s11_image12": f_s11, "s12_image14": f_s12, "s13_image16": f_s13,
    "s14_image18": f_s14,
    "s15_image20": f_s15_20, "s15_image21": f_s15_21,
    "s16_image22": f_s16, "s17_image23": f_s17, "s18_image24": f_s18, "s20_image26": f_s20,
    "s22_image29": f_s22, "s24_image31": f_s24, "s25_image33": f_s25,
    "s27_image34": f_s27, "s28_image35": f_s28, "s29_image36": f_s29,
}


def prev(key):
    return FIGS[key]()
