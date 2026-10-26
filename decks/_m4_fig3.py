# -*- coding: utf-8 -*-
"""Схемы pptx 2.4 (слайды 62–75): примеры таблицы R1 и путь пакета ПК1 → R1 → R2 → R3 → ПК2."""
import _m4_svg as S
from _m4_svg import GOLD, GOLD2, TEAL, RED, BLUE, SOFT


def _wrap(body, vb):
    return S.fig(body, vb)


# ---------------------------------------------------------------- сеть примеров (pptx 62–66)
def topo_ex(route=None, extra=""):
    """route: список точек пути пакета [(x,y),…] для сцены; каждый отрезок — свой шаг."""
    o = [S.link(150, 60, 265, 80), S.link(150, 170, 265, 92), S.link(335, 95, 450, 210, pb="Gi1/0/1", ib=".1"),
         S.link(150, 380, 265, 380), S.link(335, 370, 450, 250, pb="Gi1/0/2", ib=".1"),
         S.link(500, 230, 700, 230, pa="Gi1/0/3", ia=".1", pb="Gi1/0/1", ib=".2", lab="203.0.113.0/24", lab_dy=-28),
         S.link(750, 210, 865, 90, ia=".1"), S.link(750, 250, 865, 370, ia=".1"),
         S.link(935, 80, 1050, 80), S.link(935, 380, 1050, 380),
         S.pc(100, 50, "ПК1", [".254"]), S.pc(100, 165, "ПК2", [".35"]), S.switch(300, 85, w=70, h=32),
         S.t(300, 30, "192.168.10.0/24", 15, GOLD2, 800),
         S.pc(100, 370, "ПК3", [".254"]), S.switch(300, 380, w=70, h=32), S.t(210, 455, "192.168.20.0/24", 15, GOLD2, 800),
         S.router(475, 230, "R1"), S.router(725, 230, "R2"),
         S.switch(900, 80, w=70, h=32), S.pc(1100, 70, "ПК4", [".254"]), S.t(990, 30, "10.10.10.0/24", 15, GOLD2, 800),
         S.switch(900, 380, w=70, h=32), S.pc(1100, 370, "ПК5", [".254"]), S.t(990, 455, "10.10.20.0/24", 15, GOLD2, 800)]
    if route:
        for i in range(len(route) - 1):
            (x1, y1), (x2, y2) = route[i], route[i + 1]
            o.append(S.arrow(x1, y1, x2, y2, RED, w=4, p=i + 1))
    return _wrap("".join(o) + extra, "0 0 1200 470")


# точки маршрутов примеров 1–4
P_PC1, P_SW1, P_R1, P_SW3, P_PC3, P_R2, P_SW5, P_PC5 = (150, 40), (300, 60), (470, 200), (300, 350), (150, 350), (720, 200), (900, 350), (1050, 350)


# ---------------------------------------------------------------- путь пакета (pptx 72–75)
ZONES = [(10, 300, "#f0c75e", "1", "10.10.0.0/24"), (300, 570, "#9be37a", "2", "10.20.0.0/24"),
         (570, 860, "#6cb8ff", "3", "10.30.0.0/24"), (860, 1190, "#c9b3ff", "4", "10.40.0.0/24")]
XS = {"ПК1": 70, "R1": 300, "R2": 570, "R3": 860, "ПК2": 1130}


def path_topo(at, arrows=(), ph_from=None):
    """at — у какого устройства пакет; arrows — номера зон со стрелками."""
    o = []
    for x1, x2, c, n, net in ZONES:
        o.append('<ellipse cx="%g" cy="120" rx="%g" ry="80" fill="%s" fill-opacity=".10" stroke="%s" stroke-dasharray="7 5"/>'
                 % ((x1 + x2) / 2.0, (x2 - x1) / 2.0, c, c))
        o.append(S.t((x1 + x2) / 2.0, 30, net, 14, c, 900))
        o.append('<circle cx="%g" cy="196" r="13" fill="#03140f" stroke="%s" stroke-width="2"/>' % ((x1 + x2) / 2.0, c))
        o.append(S.t((x1 + x2) / 2.0, 201, n, 14, c, 900))
    o += [S.link(110, 120, 270, 120, ia="10.10.0.10/24", ib="10.10.0.1/24"),
          S.link(330, 120, 540, 120, ia="10.20.0.1/24", ib="10.20.0.2/24"),
          S.link(600, 120, 830, 120, ia="10.30.0.1/24", ib="10.30.0.2/24", lab="E1", lab_dy=-26),
          S.link(890, 120, 1090, 120, ia="10.40.0.1/24", ib="10.40.0.10/24"),
          S.t(130, 160, "AA:AA", 12, TEAL, 800, mono=True), S.t(250, 160, "AA:11", 12, TEAL, 800, mono=True),
          S.t(350, 160, "BB:22", 12, TEAL, 800, mono=True), S.t(520, 160, "CC:33", 12, TEAL, 800, mono=True),
          S.t(910, 160, "DD:44", 12, TEAL, 800, mono=True), S.t(1070, 160, "BB:BB", 12, TEAL, 800, mono=True),
          S.pc(XS["ПК1"], 110, "ПК1"), S.router(XS["R1"], 120, "R1"), S.router(XS["R2"], 120, "R2"),
          S.router(XS["R3"], 120, "R3"), S.pc(XS["ПК2"], 110, "ПК2")]
    for z in arrows:
        x1, x2 = ZONES[int(z) - 1][0], ZONES[int(z) - 1][1]
        o.append(S.arrow(x1 + 70, 80, x2 - 70, 80, BLUE, w=4))
    x = XS[at]
    o.append('<g><rect x="%g" y="52" width="46" height="30" rx="5" fill="%s" stroke="#2a1e06" stroke-width="2"/>%s</g>'
             % (x - 23, GOLD, S.t(x, 72, "IP", 13, "#1a1206", 900)))
    return _wrap("".join(o), "0 0 1200 220")


def frame_l2l3(vals):
    """Поля кадра pptx: vals = (MAC назн., MAC ист.)."""
    names = ["МАС-адрес назначения", "МАС-адрес источника", "Тип, длина, значение", "IP-адрес источника", "IP-адрес назначения",
             "Протокол", "Данные", "Концевая метка"]
    v = list(vals) + ["0x800", "10.10.0.10", "10.40.0.10", "TCP", "TCP-сегмент", "CRC"]
    cols = [S.F_PAY] * 3 + ["#ffb36b"] * 3 + ["#9fd3ff", "#fff1a8"]
    o = [S.t(300, 18, "Заголовок Ethernet-кадра 2 уровня", 14, GOLD2, 800), S.t(760, 18, "Заголовок IP-пакета 3 уровня", 14, GOLD2, 800)]
    x = 10
    for nm, val, c in zip(names, v, cols):
        o.append('<rect x="%g" y="28" width="143" height="44" rx="5" fill="%s" stroke="#2a1e06"/>' % (x, c))
        words = nm.split(" ")
        o.append(S.t(x + 71, 46, " ".join(words[:2]), 11, "#1a1206", 800))
        o.append(S.t(x + 71, 62, " ".join(words[2:]), 11, "#1a1206", 800))
        o.append('<rect x="%g" y="74" width="143" height="34" rx="5" fill="rgba(4,22,16,.95)" stroke="%s"/>' % (x, c))
        o.append(S.t(x + 71, 97, val, 15, "#fff", 800, mono=True))
        x += 147
    return _wrap("".join(o), "0 0 1190 115")


# ---------------------------------------------------------------- модель OSI на пути (pptx 71)
def osi_path():
    L = [("7 Уровень Приложения", "#b49cff"), ("6 Уровень Представления", "#8fa3c9"), ("5 Сеансовый Уровень", "#57d6c0"),
         ("4 Транспортный Уровень", "#57d6c0"), ("3 Сетевой Уровень", "#ffb98a"), ("2 Канальный Уровень", "#ffd06b"),
         ("1 Физический Уровень", "#fff08a")]
    xs = [20, 260, 500, 740, 980]
    o = []
    for i, x in enumerate(xs):
        full = i in (0, 4)
        for k, (nm, c) in enumerate(L):
            if not full and k < 4:
                continue
            y = 10 + k * 40
            o.append('<rect x="%g" y="%g" width="200" height="34" rx="6" fill="%s" stroke="#2a1e06"/>' % (x, y, c))
            o.append(S.t(x + 100, y + 22, nm, 12.5, "#1a1206", 800))
        nm = ["ПК1", "R1", "R2", "R3", "ПК2"][i]
        o.append(S.t(x + 100, 316, nm, 16, GOLD2, 900))
        if i < 4:
            o.append(S.arrow(x + 205, 310, xs[i + 1] - 5, 310, BLUE, w=3.5))
    return _wrap("".join(o), "0 0 1200 330")
