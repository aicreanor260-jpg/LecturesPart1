# -*- coding: utf-8 -*-
"""Схемы деки RIP 2.5.1, часть 2: три маршрутизатора с таблицами, граф и кольцо Беллмана–Форда,
отказы канала и маршрутизатора, формат RIPv2, топология примера настройки — по рисункам pptx."""

from _sw_lib import _esc
from _rp1_fig import Fig, wrap, ph, t, INK, RED, GRN, TEAL, BLUE

_T3 = [("192.168.10.0/24", "blue"), ("192.168.20.0/24", "green"), ("192.168.30.0/24", "red"), ("192.168.40.0/24", "violet")]


# ====================================================================== pptx 6–11 · три маршрутизатора
def topo3(tables, updates=None, top_arrow=None, stage=None):
    """tables: 3 списка строк (сеть, интерфейс, переход[, kind[, ph]]); updates: (цвет, шаг)."""
    f = Fig(1200, 430)
    y = 140
    xs = (300, 640, 980)
    f.cloud(95, y, 186, 70, [_T3[0][0]], _T3[0][1], size=17)
    f.cloud(470, y, 220, 70, [_T3[1][0]], _T3[1][1], size=17)
    f.cloud(810, y, 220, 70, [_T3[2][0]], _T3[2][1], size=17)
    f.cloud(1112, y, 176, 66, [_T3[3][0]], _T3[3][1], size=15)
    f.wire(150, y, 1060, y, w=4)
    for x, n in zip(xs, ("R1", "R2", "R3")):
        f.router(x, y - 16, n, .74)
    for x, s in ((222, "gi1/0/2"), (378, "gi1/0/1"), (562, "gi1/0/1"), (720, "gi1/0/2"), (902, "gi1/0/2"), (1058, "gi1/0/1")):
        f.label(x, y + 36, s, 16)
    if updates:
        col, p = updates
        for x1, x2 in ((330, 610), (670, 950)):
            f.envelope((x1 + x2) / 2 + 40, 42, p)
            f.arrow(x1, 70, x2, 70, col, 5, p, both=True)
            f.label((x1 + x2) / 2, 92, "Обновление", 15, INK, 700, p=p)
    if top_arrow:
        f.arrow(240, 66, 1000, 66, "r", 5, top_arrow[1], both=True)
        f.label(620, 50, top_arrow[0], 18, INK, 800, p=top_arrow[1])
    widths = (150, 104, 82)
    for x, rows in zip(xs, tables):
        x0 = x - 168
        f.raw('<path d="M%g %gL%g %gL%g %gz" fill="#dff3ec" stroke="#8fc9b8" stroke-width="1.5"%s/>'
              % (x, y + 46, x0, 250, x0 + 336, 250, ph(stage)), False)
        rr = [((r[0], r[1], r[2]), r[3] if len(r) > 3 else "", r[4] if len(r) > 4 else None) for r in rows]
        rr += [(("", "", ""), "", None)] * (4 - len(rows))
        f.table(x0, 250, ("Сеть", "Интерфейс", "Переход"), rr, widths, stage, size=16, rh=33)
    return wrap(f.svg())


# ====================================================================== pptx 13 · граф кольца
def bf_graph():
    """Рёбра как на рисунке pptx: R1–R2 = 4, R2–R3 = 2, R3–R4 = 3, R4–R1 = 10; оценки по проходам."""
    f = Fig(1200, 440)
    pos = {"R1": (330, 110), "R2": (870, 110), "R3": (870, 320), "R4": (330, 320)}
    for a, b, w in (("R1", "R2", "4"), ("R2", "R3", "2"), ("R3", "R4", "3"), ("R4", "R1", "10")):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        f.wire(x1, y1 + 14, x2, y2 + 14, "#7aa99c", 5)
        f.pill((x1 + x2) / 2.0, (y1 + y2) / 2.0 + 20, w, TEAL, size=28)
    for n, (x, y) in pos.items():
        f.router(x, y, n, 1.15)
    est = {"R1": ["0", "0", "0", "0"], "R2": ["∞", "4", "4", "4"], "R3": ["∞", "∞", "6", "6"], "R4": ["∞", "10", "10", "9"]}
    dx = {"R1": -175, "R2": 175, "R3": 175, "R4": -175}
    for n, vals in est.items():
        x, y = pos[n]
        for i, v in enumerate(vals):
            col = RED if i and v != vals[i - 1] else GRN
            f.pill(x + dx[n], y + 14, v, col, p=i, only=i < 3, size=30)
    f.label(600, 420, "Оценка расстояния от R1 — рядом с каждой вершиной", 22, INK, 700)
    return wrap(f.svg())


# ====================================================================== pptx 14–17 · кольцо R1–R4
def ring():
    f = Fig(1180, 500)
    P = {"R1": (450, 110), "R2": (850, 110), "R3": (850, 370), "R4": (450, 370)}
    f.cloud(270, 85, 250, 70, ["192.168.10.0/24"], "orange", size=20)
    f.cloud(1030, 85, 250, 70, ["192.168.20.0/24"], "green", size=20)
    f.cloud(1030, 405, 250, 70, ["192.168.30.0/24"], "red", size=20)
    f.cloud(270, 405, 250, 70, ["192.168.40.0/24"], "blue", size=20)
    for a, b in (("R1", "R2"), ("R2", "R3"), ("R3", "R4"), ("R4", "R1")):
        (x1, y1), (x2, y2) = P[a], P[b]
        f.wire(x1, y1 + 10, x2, y2 + 10, w=4)
    for n, (x, y) in P.items():
        f.wire(x, y + 4, x + (-100 if x < 600 else 100), y + (-20 if y < 200 else 30), w=4)
        f.router(x, y, n, .9)
    L = f.label
    L(650, 98, "192.0.2.0/30", 21)
    L(520, 140, "Gi1/0/1", 19); L(780, 140, "Gi1/0/2", 19)
    L(450, 52, "Gi1/0/3", 19); L(850, 52, "Gi1/0/3", 19)
    L(400, 182, "Gi1/0/2", 19); L(905, 182, "Gi1/0/1", 19)
    L(400, 328, "Gi1/0/1", 19); L(905, 328, "Gi1/0/2", 19)
    L(520, 404, "Gi1/0/2", 19); L(780, 404, "Gi1/0/1", 19)
    L(450, 462, "Gi1/0/3", 19); L(850, 462, "Gi1/0/3", 19)
    L(650, 432, "198.51.100.0/30", 21)
    f.raw(t(482, 250, "198.18.0.0/30", 20, INK, 800, extra=' transform="rotate(-90 482 250)"'))
    f.raw(t(820, 250, "203.0.113.0/30", 20, INK, 800, extra=' transform="rotate(90 820 250)"'))
    f.arrow(580, 70, 720, 70, "b", 5, both=True)
    f.arrow(410, 210, 410, 300, "b", 5, both=True)
    f.arrow(895, 210, 895, 300, "g", 5, both=True)
    f.arrow(580, 470, 720, 470, "g", 5, both=True)
    f.label(150, 190, "R1 Напрямую", 19)
    f.label(150, 212, "подключенные", 19)
    f.table(8, 228, ("Порт", "Сеть", ""), [(("Gi1/0/1", "192.0.2.0/30", "0"),), (("Gi1/0/2", "198.18.0.0/30", "0"),),
                                          (("Gi1/0/3", "192.168.10.0/24", "0"),)], (84, 168, 34), size=17, rh=32)
    return wrap(f.svg())


# ====================================================================== pptx 18–19 · отказы
def _failure(router_down=False):
    f = Fig(1200, 580)
    R = {"R1": (330, 110, "#2fae5f"), "R3": (870, 110, "#f0a020"), "R2": (330, 430, "#5b9be0"), "R4": (870, 430, "#7b3fb8")}
    f.cloud(95, 110, 180, 90, ["WAN-1"], "blue", size=20)
    f.label(95, 42, "192.168.1.0/24", 18, "#1f5aa8", 900)
    f.wire(180, 120, 270, 120, w=3)
    if router_down:
        f.wire(395, 120, 540, 120, w=3)
        f.wire(660, 120, 805, 120, w=3)
        f.wire(330, 160, 330, 245, w=3)
        f.wire(330, 300, 330, 400, w=3)
        f.switch(600, 120, "SW2")
        f.switch(345, 270, "SW1")
        f.cross(330, 40, 30)
    else:
        f.wire(395, 120, 805, 120, w=3)
        f.wire(330, 160, 330, 400, w=3)
        f.cross(600, 120, 30)
    f.wire(395, 440, 805, 440, w=3)
    f.wire(870, 160, 870, 400, w=3)
    for n, (x, y, c) in R.items():
        f.router(x, y, "", .85, col=c)
        f.label(x - 80, y + 66, n, 21, INK, 900)
    L = f.label
    L(232, 108, "eth0", 17); L(430, 108, "eth3", 17); L(770, 108, "eth1", 17)
    L(300, 180, "eth2", 17); L(905, 180, "eth4", 17); L(905, 395, "eth3", 17)
    L(300, 395, "eth1", 17); L(432, 428, "eth4", 17); L(770, 428, "eth2", 17)
    pw = (64, 128)
    hdr = "#bfe3f3"
    f.table(395, 175, ("Порт", "Адрес"), [(("eth0", "192.168.1.1/24"),), (("eth3", "10.10.13.1/30"),), (("eth2", "10.10.12.1/30"),)], pw, size=13, rh=24, hdr=hdr)
    f.table(935, 160, ("Порт", "Адрес"), [(("eth1", "10.10.13.2/30"),), (("eth4", "10.10.34.1/30"),)], pw, size=13, rh=24, hdr=hdr)
    f.table(395, 495, ("Порт", "Адрес"), [(("eth1", "10.10.12.2/30"),), (("eth4", "10.10.24.1/30"),)], pw, size=13, rh=24, hdr=hdr)
    f.table(935, 495, ("Порт", "Адрес"), [(("eth2", "10.10.24.2/30"),), (("eth3", "10.10.34.2/30"),)], pw, size=13, rh=24, hdr=hdr)
    return f


def link_down():
    """Сцена по этапам 1–4 слайда pptx «Выход из строя канала связи»."""
    f = _failure(False)
    f.pill(600, 60, "Этап 1: eth3 (R1) и eth1 (R3) — down", RED, 1, size=15)
    f.pill(660, 305, "Этап 2: метрика 16 к 10.10.13.0/30", RED, 2, size=15)
    f.arrow(305, 270, 305, 390, "g", 4, 3)
    f.table(80, 250, ("Метрика", "Сеть"), [(("1", "192.168.1.0/24"), "g"), (("15", "10.10.13.0/30"), "g"),
                                           (("1", "10.10.12.0/30"), "g")], (76, 130), 3, size=13, rh=24, hdr="#c9f0d6")
    f.arrow(845, 270, 845, 390, "g", 4, 3)
    f.table(935, 250, ("Метрика", "Сеть"), [(("2", "192.168.1.0/24"), "g"), (("15", "10.10.13.0/30"), "o"),
                                            (("2", "10.10.12.0/30"), "g"), (("1", "10.10.34.0/30"), "o")], (76, 130), 3, size=13, rh=24, hdr="#c9f0d6")
    f.pill(640, 355, "Этап 4: в RIB R2 и R4 — 10.10.13.0/30 с метрикой 16", RED, 4, size=15)
    return wrap(f.svg())


def router_down():
    return wrap(_failure(True).svg())


# ====================================================================== pptx 20–21 · формат RIPv2
def rip_format():
    rows = [[("Command", 1, "h"), ("Version", 1, "h"), ("Unused", 2, "h")],
            [("0xFFFF", 2, "a"), ("Authentication Type", 2, "a")],
            [("Password", 4, "a")],
            [("Address Family Identifier", 2, "r"), ("Route Tag", 2, "r")],
            [("IP Address", 4, "r")], [("Subnet Mask", 4, "r")], [("Next Hop", 4, "r")], [("Metric", 4, "r")]]
    o = ['<div class="rpfmt"><div class="rpbits"><span>0</span><span>8</span><span>16</span><span>31</span></div>']
    for r in rows:
        o.append('<div class="rprow">%s</div>' % "".join(
            '<div class="rpf rpf-%s" style="grid-column:span %d">%s</div>' % (k, n, _esc(s)) for s, n, k in r))
    o.append("</div>")
    cells = (("Команда", "h"), ("Версия", "h"), ("Не использует", "h"), ("0xFFFF", "a"), ("Тип Аутентификации", "a"),
             ("Пароль", "a"), ("AFI", "r"), ("Тэг", "r"), ("Адрес", "r"), ("Маска", "r"), ("Переход", "r"), ("Метрика", "r"))
    strip = ('<div class="rpstrip"><div class="rps h" style="grid-column:span 3">Заголовок</div>'
             '<div class="rps a" style="grid-column:span 3">Аутентификация</div>'
             '<div class="rps r" style="grid-column:span 6">Маршрутная информация</div>'
             + "".join('<div class="rps %s">%s</div>' % (k, s) for s, k in cells) + "</div>")
    return "".join(o) + strip


# ====================================================================== pptx 31–33 · пример настройки
def example_topo():
    f = Fig(1200, 400)
    f.cloud(600, 46, 170, 66, ["ISP"], "violet", size=21)
    f.cloud(112, 205, 205, 120, ["Gi1/0/2", "192.168.10.0/24", "LAN"], "green", size=16)
    f.cloud(1088, 205, 205, 120, ["Gi1/0/2", "192.168.20.0/24", "LAN"], "red", size=16)
    f.cloud(600, 350, 220, 96, ["Gi1/0/3", "192.168.30.0/24", "LAN"], "yellow", size=15)
    for x1, x2 in ((250, 600), (600, 950)):
        f.raw('<rect x="%g" y="186" width="%g" height="40" rx="20" fill="#cfeaf7" stroke="#7bb6d6" stroke-width="2"/>'
              % (x1 + 40, x2 - x1 - 80), False)
    f.wire(190, 205, 1010, 205, w=4)
    f.wire(600, 76, 600, 305, w=4)
    f.router(250, 188, "R1", .8)
    f.router(950, 188, "R2", .8)
    f.router(600, 188, "", .8)
    f.pill(600, 252, "RIP", INK, size=18)
    L = f.label
    L(330, 178, "Gi1/0/1", 15); L(520, 178, "Gi1/0/2", 15); L(680, 178, "Gi1/0/1", 15); L(870, 178, "Gi1/0/1", 15)
    L(425, 178, "RIP", 15, BLUE); L(775, 178, "RIP", 15, BLUE)
    L(310, 248, ".2", 15); L(425, 252, "198.51.100.0/24", 15); L(540, 248, ".1", 15)
    L(660, 248, ".1", 15); L(775, 252, "198.18.0.0/15", 15); L(890, 248, ".2", 15)
    L(200, 252, ".1", 15); L(1000, 252, ".1", 15)
    L(612, 98, ".2", 15, anchor="start"); L(588, 98, "RIP", 15, BLUE, anchor="end")
    L(616, 120, "203.0.113.0/24", 15, anchor="start"); L(616, 140, "Gi1/0/4", 15, anchor="start"); L(588, 140, ".1", 15, anchor="end")
    L(612, 290, ".1", 15, anchor="start")
    return wrap(f.svg())
