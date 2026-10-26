# -*- coding: utf-8 -*-
"""Схемы pptx «OSPF 2.5», слайды 55–86, перерисованные в кавайном стиле деки.
FIGS = {"sNN_imageK": функция} — логика и подписи строго как на картинках pptx."""
import math

from _o5_figlib import (router, cloudsvg, blob, scene, T, box, fig, svg_only,
                        PINK, BLUE, YEL, GRN, INK, SOFT)

ORG = "#ff8a3d"
RED = "#e8202a"
HALO = ' stroke="#fff" stroke-width="6" paint-order="stroke" stroke-linejoin="round"'
_N = [0]


def ln(x1, y1, x2, y2, col=INK, w=4, dash=None, extra=""):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%.1f" fill="none" stroke-linecap="round"%s%s/>'
            % (x1, y1, x2, y2, col, w, d, extra))


def poly(pts, col="#9aa6b2", w=2.5, mk=None):
    m = ' marker-end="url(#%s)"' % mk if mk else ""
    return ('<path d="M%s" stroke="%s" stroke-width="%.1f" fill="none" stroke-linejoin="round"%s/>'
            % (" L".join("%.1f %.1f" % p for p in pts), col, w, m))


def marker(col):
    """Своя стрелка-наконечник нужного цвета (возвращает id, defs)."""
    _N[0] += 1
    mid = "o5c_m%d" % _N[0]
    return mid, ('<marker id="%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.4" markerHeight="4.4" '
                 'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>' % (mid, col))


def arr(x1, y1, x2, y2, mid, col, w=4, both=False, extra=""):
    s = ' marker-start="url(#%s)"' % mid if both else ""
    return ('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%.1f" fill="none" stroke-linecap="round" '
            'marker-end="url(#%s)"%s%s/>' % (x1, y1, x2, y2, col, w, mid, s, extra))


def lbl(x, y, s, size=17, col=INK, anchor="middle", mono=True, w=700):
    return T(x, y, s, size, col, w, anchor, mono, HALO)


def ml(x, y, lines, size=17, col=INK, w=600, lh=1.25):
    """Многострочный текст по центру (x, y)."""
    y0 = y - (len(lines) - 1) * size * lh / 2 + size * .35
    return "".join(T(x, y0 + i * size * lh, s, size, col, w) for i, s in enumerate(lines))


def R(x, y, w=86, tone="b", name=None, nx=0, ny=None, size=20):
    o = router(x, y, w, tone)
    if name:
        o += T(x + nx, y + (ny if ny is not None else w * .75), name, size, INK, 800)
    return o


def cy(y, w=86):
    """Центр корпуса роутера (для концов линий — они уходят за корпус)."""
    return y + w * .14


# ------------------------------------------------------------------ s55: суммирование 10.1.x / 10.0.x с ABR
def s55():
    w = 82
    P = {"L": (110, 230), "T": (450, 90), "B": (450, 340), "A": (700, 205),
         "T2": (960, 90), "E": (1270, 215), "B2": (1010, 340)}
    links = [("L", "T"), ("L", "B"), ("T", "B"), ("T", "A"), ("B", "A"),
             ("A", "T2"), ("A", "B2"), ("T2", "B2"), ("T2", "E"), ("B2", "E")]
    o = [blob(345, 225, 330, 200, "y", seed=1), blob(1055, 225, 320, 200, "p", seed=2)]
    for a, b in links:
        (x1, y1), (x2, y2) = P[a], P[b]
        o.append(ln(x1, cy(y1, w), x2, cy(y2, w), INK, 4))
    for k, (x, y) in P.items():
        o.append(R(x, y, w, "p" if k == "A" else "b"))
    L = [(150, 172, "10.1.5.2/24", "middle"), (120, 312, "10.1.2.2/24", "middle"),
         (360, 66, "10.1.5.1/24", "end"), (540, 66, "10.1.4.2/24", "start"), (462, 168, "10.1.3.2/24", "start"),
         (462, 300, "10.1.3.1/24", "start"), (380, 400, "10.1.2.1/24", "end"), (520, 400, "10.1.1.2/24", "start"),
         (640, 188, "10.1.4.1/24", "end"), (640, 212, "10.1.1.1/24", "end"),
         (762, 188, "10.0.2.1/24", "start"), (762, 212, "10.0.1.1/24", "start"),
         (870, 66, "10.0.2.2/24", "end"), (972, 168, "10.0.5.1/24", "start"), (1050, 66, "10.0.3.2/24", "start"),
         (1270, 160, "10.0.3.1/24", "middle"), (1270, 290, "10.0.4.1/24", "middle"),
         (996, 300, "10.0.5.2/24", "end"), (920, 400, "10.0.1.2/24", "end"), (1100, 400, "10.0.4.2/24", "start")]
    for x, y, s, a in L:
        o.append(lbl(x, y, s, 17, INK, a))
    return fig("0 20 1400 420", "".join(o))


# ------------------------------------------------------------------ s58–61: четыре типа сетей
def _switch(x, y, w=96, h=50):
    return (box(x - w / 2, y - h / 2, w, h, "#8fc7ff", "#2f6fbf", 12, 3) +
            '<path d="M%.1f %.1f h40 m-8 -6 l8 6 l-8 6 M%.1f %.1f h-40 m8 -6 l-8 6 l8 6" stroke="#fff" '
            'stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            % (x - 20, y - 8, x + 20, y + 8))


def _nbma(x, y):
    return cloudsvg(x, y, 170, 64, "NBMA", tone="g", fs=19)


def _isp(x, y):
    return cloudsvg(x, y, 120, 46, "ISP", tone="v", fs=18)


def types(hl="p2p"):
    mb, db = marker(BLUE)
    mo, do = marker(ORG)
    w = 78
    Q = {"p2p": (0, 0), "p2mp": (650, 0), "bma": (0, 450), "nbma": (650, 450)}
    caps = {"p2p": "point-to-point", "p2mp": "point-to-multipoint",
            "bma": "broadcast multiple access", "nbma": "non-broadcast multiple access"}
    parts = {}

    # point-to-point
    o = [ln(325, cy(120, w), 325, cy(300, w)), _isp(325, 45), R(325, 110, w, "b", "R1", 64, 24, 18),
         R(325, 300, w, "b", "R2", 64, 24, 18),
         arr(255, 150, 255, 320, mb, BLUE, 6, True)]
    parts["p2p"] = o
    # point-to-multipoint
    o = [ln(975, cy(110, w), 975, cy(215, w)), ln(780, 345, 1170, 345),
         '<path d="M955 245 Q880 300 820 330" stroke="%s" stroke-width="5" fill="none" stroke-dasharray="12 9"/>' % ORG,
         '<path d="M995 245 Q1070 300 1130 330" stroke="%s" stroke-width="5" fill="none" stroke-dasharray="12 9"/>' % ORG,
         _isp(975, 45), R(975, 110, w, "b", "R1", 64, 24, 18), R(975, 215, w, "b", "R2", 64, 24, 18),
         _nbma(975, 345), R(780, 335, w, "b", "R3", 0, 72, 18), R(1170, 335, w, "b", "R4", 0, 72, 18),
         arr(905, 130, 905, 235, mb, BLUE, 6, True)]
    parts["p2mp"] = o
    # broadcast multiple access
    o = [ln(325, cy(560, w), 325, 760), ln(110, cy(760, w), 540, cy(760, w)),
         _isp(325, 495), R(325, 560, w, "b", "R1", 64, 24, 18), R(325, 660, w, "b", "R2", 64, 24, 18),
         _switch(325, 771), R(110, 760, w, "b", "R3", 0, 72, 18), R(540, 760, w, "b", "R4", 0, 72, 18),
         arr(255, 580, 255, 680, mb, BLUE, 6, True),
         arr(270, 700, 270, 750, mo, ORG, 6), arr(150, 812, 262, 812, mo, ORG, 6), arr(500, 812, 388, 812, mo, ORG, 6)]
    parts["bma"] = o
    # non-broadcast multiple access
    o = [ln(975, cy(560, w), 975, 760), ln(780, cy(760, w), 1170, cy(760, w)),
         _isp(975, 495), R(975, 560, w, "b", "R1", 64, 24, 18), R(975, 660, w, "b", "R2", 64, 24, 18),
         _nbma(975, 772), R(780, 760, w, "b", "R3", 0, 72, 18), R(1170, 760, w, "b", "R4", 0, 72, 18),
         arr(905, 580, 905, 680, mb, BLUE, 6, True),
         arr(918, 700, 918, 752, mb, BLUE, 6), arr(800, 818, 900, 818, mb, BLUE, 6), arr(1150, 818, 1050, 818, mb, BLUE, 6)]
    parts["nbma"] = o

    out = []
    for k, (qx, qy) in Q.items():
        on = k == hl
        frame = box(qx + 12, qy + 8, 626, 434, "#fff4f9" if on else "#ffffff", PINK if on else "#e9eef3",
                    22, 4 if on else 2)
        cap = T(qx + 325, qy + 425, caps[k], 24 if on else 21, PINK if on else INK, 800)
        out.append('<g opacity="%s">%s%s%s</g>' % ("1" if on else ".38", frame, "".join(parts[k]), cap))
    leg = (arr(450, 540, 520, 540, mb, BLUE, 6, True) + T(535, 547, "unicast", 20, BLUE, 700, "start") +
           arr(520, 590, 450, 590, mo, ORG, 6) + T(535, 597, "multicast", 20, ORG, 700, "start"))
    out.append(leg)
    return fig("0 0 1300 900", "".join(out), db + do)


# ------------------------------------------------------------------ s58–61: блок-схемы связей
def _bx(x, y, w, h, lines, size=21):
    return box(x - w / 2, y - h / 2, w, h, "#e3f0fd", "#bcd9f6", 18, 2.5) + ml(x, y, lines, size, "#1f5fae", 700)


def s58_links():
    o = [ln(160, 80, 440, 80, "#9aa6b2", 3), _bx(100, 80, 150, 90, ["R1"]), _bx(500, 80, 150, 90, ["R2"]),
         box(225, 62, 150, 36, "#fff", "#bcd9f6", 18, 2.5), T(300, 87, "один канал", 19, "#1f5fae", 700)]
    return fig("0 20 600 120", "".join(o))


def _fan(left, right_lbl, right2=None, rw=330):
    """Три R слева сходятся в общий узел справа."""
    o = []
    ys = [70, 200, 330]
    cx = 520
    o.append(poly([(150, 70), (210, 70), (210, 180), (cx - rw / 2, 180)]))
    o.append(poly([(150, 200), (cx - rw / 2, 200)]))
    o.append(poly([(150, 330), (210, 330), (210, 220), (cx - rw / 2, 220)]))
    for y, n in zip(ys, left):
        o.append(_bx(90, y, 130, 80, [n]))
    o.append(_bx(cx, 200, rw, 100, right_lbl))
    if right2:
        o.append(poly([(cx + rw / 2, 200), (780, 200)]))
        o.append(_bx(850, 200, 140, 80, [right2]))
    return "".join(o)


def s59_links():
    return fig("0 20 940 360", _fan(["R1", "R2", "R3"], ["Общий Ethernet-сегмент"], "R4"))


def s60_links():
    return fig("0 20 720 360", _fan(["R1", "R2", "R3"], ["Сеть Frame Relay", "без broadcast"]))


def s61_links():
    o = [poly([(270, 60), (330, 60)]),
         poly([(580, 50), (680, 50)]),
         poly([(580, 60), (640, 60), (640, 190), (680, 190)]),
         poly([(580, 70), (620, 70), (620, 330), (680, 330)]),
         _bx(140, 60, 260, 90, ["Центральный", "маршрутизатор"], 19), _bx(455, 60, 250, 90, ["Общая", "транспортная сеть"], 19),
         _bx(770, 50, 180, 80, ["Филиал R2"], 19), _bx(770, 190, 180, 80, ["Филиал R3"], 19),
         _bx(770, 330, 180, 80, ["Филиал R4"], 19)]
    return fig("0 0 880 390", "".join(o))


# ------------------------------------------------------------------ s63: полносвязная сеть и DR
def _pent(ox):
    return {"R1": (ox + 330, 60), "R2": (ox + 570, 220), "R3": (ox + 480, 450),
            "R4": (ox + 180, 450), "R5": (ox + 90, 220)}


def _along(p, q, off, cut1=50, cut2=50):
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    return (x1 + ux * cut1 + nx * off, y1 + uy * cut1 + ny * off,
            x2 - ux * cut2 + nx * off, y2 - uy * cut2 + ny * off)


def _rot_lbl(x1, y1, x2, y2, s, col, side):
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    if ang > 90:
        ang -= 180
    if ang < -90:
        ang += 180
    mx, my = x1 + (x2 - x1) * .30, y1 + (y2 - y1) * .30
    L = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    mx += nx * side
    my += ny * side
    return ('<g transform="translate(%.1f %.1f) rotate(%.1f)">%s</g>'
            % (mx, my, ang, T(0, 6, s, 17, col, 700, "middle", True, HALO)))


def s63():
    mr, dr_ = marker(RED)
    mb, db = marker(BLUE)
    w = 80
    o = []
    for ox, k in ((0, 1), (700, 2)):
        P = _pent(ox)
        sw = (ox + 330, 250)
        for n, (x, y) in P.items():
            o.append(ln(x, cy(y, w), sw[0], sw[1], INK, 4))
        o.append(_switch(sw[0], sw[1], 104, 56))
        o.append(T(sw[0], sw[1] + 52, "SW1", 19, INK, 800))
        for n, (x, y) in P.items():
            o.append(R(x, y, w, "b", n, 0, 66, 19))
    # слева: каждый с каждым (шаг 1)
    P = {k: (x, cy(y, 80)) for k, (x, y) in _pent(0).items()}
    names = list(P)
    mesh = []
    for i in range(5):
        for j in range(i + 1, 5):
            x1, y1, x2, y2 = _along(P[names[i]], P[names[j]], 14, 56, 56)
            mesh.append(arr(x1, y1, x2, y2, mr, RED, 3, True))
    mesh.append(T(330, 400, "n(n-1)/2", 22, BLUE, 800, extra=HALO))
    mesh.append(T(330, 525, "255.255.255.255", 18, RED, 700, mono=True, extra=HALO))
    o.append('<g data-ph="1">%s</g>' % "".join(mesh))
    # справа: DR = R1
    P = {k: (x, cy(y, 80)) for k, (x, y) in _pent(700).items()}
    o.append('<g data-ph="2">%s</g>' % T(960, 40, "DR", 24, RED, 800))
    to_dr, from_dr = [], []
    for n in ("R2", "R3", "R4", "R5"):
        x1, y1, x2, y2 = _along(P[n], P["R1"], 8, 56, 56)
        to_dr.append(arr(x1, y1, x2, y2, mr, RED, 3))
        to_dr.append(_rot_lbl(x1, y1, x2, y2, "224.0.0.6", RED, 20))
        x1, y1, x2, y2 = _along(P["R1"], P[n], 8, 56, 56)
        from_dr.append(arr(x1, y1, x2, y2, mb, BLUE, 3))
        from_dr.append(_rot_lbl(x2, y2, x1, y1, "224.0.0.5", BLUE, -20))
    o.append('<g data-ph="2">%s</g>' % "".join(to_dr))
    o.append('<g data-ph="3">%s</g>' % "".join(from_dr))
    caps = ["Маршрутизаторы OSPF в одном сегменте через SW1",
            "Без DR: смежность каждый с каждым — n(n-1)/2 отношений (20 маршрутизаторов — 190, 50 — 1225)",
            "DR = R1: DROTHER отправляют свои LSA только DR и BDR на адрес 224.0.0.6 (все DR)",
            "DR пересылает объявления LSA всем остальным роутерам на адрес 224.0.0.5 (все маршрутизаторы OSPF)"]
    return scene(svg_only("0 -10 1400 560", "".join(o), dr_ + db), caps)


# ------------------------------------------------------------------ s64: блок-схема выбора DR и router-id
B = '<tspan font-weight="800">%s</tspan>'


def _dia(x, y, lines, w=300, h=180):
    return ('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="#fef6dc" stroke="#efcf6a" stroke-width="3"/>'
            % (x, y - h / 2, x + w / 2, y, x, y + h / 2, x - w / 2, y) + ml(x, y, lines, 18, INK, 500))


def _gb(x, y, w, h, lines, size=18):
    return box(x - w / 2, y - h / 2, w, h, "#e6f7ec", "#86d3a8", 12, 3) + ml(x, y, lines, size, INK, 800)


def s64():
    mk, d = marker(SOFT)
    o = [ml(230, 60, ["ВЫБОР DR В", "BROADCAST ДОМЕНЕ"], 24, INK, 800),
         ml(1000, 60, ["ЧТО ИСПОЛЬЗУЕТСЯ КАК", "ИДЕНТИФИКАТОР"], 24, INK, 800)]
    # левая
    o += [poly([(350, 230), (408, 230)], SOFT, 2.5, mk), T(380, 215, "ДА", 15, INK, 700),
          poly([(200, 320), (200, 400)], SOFT, 2.5, mk), T(170, 360, "НЕТ", 15, INK, 700),
          _dia(200, 230, ["Приоритеты", B % "ip ospf priority", "на интерфейсе", "разные?"], 300, 180),
          _gb(545, 230, 270, 110, ["DR - это маршрутизатор", "с наибольшим", "приоритетом (priority)"]),
          _gb(200, 470, 270, 130, ["DR - это маршрутизатор", "с наибольшим", "идентификатором", "(router-id)"])]
    # правая
    dx, bx = 870, 1240
    ys = [200, 395, 590]
    q = [["Задан ли", B % "router-id", "статически?"], ["Созданы ли", B % "loopback", "интерфейсы?"],
         ["Задан ли", B % "ip-адрес активного", "интерфейса."]]
    bb = [["Использовать заданный", "в качестве router-id"], ["Выбрать наибольший", "IP-адрес Loopback-", "инткерфейса."],
          ["Выбрать наибольший", "IP-адрес интерфейса."]]
    for i, y in enumerate(ys):
        o += [poly([(dx + 150, y), (bx - 150 - 6, y)], SOFT, 2.5, mk), T(dx + 190, y - 14, "ДА", 15, INK, 700)]
        if i < 2:
            o += [poly([(dx, y + 75), (dx, ys[i + 1] - 81)], SOFT, 2.5, mk), T(dx - 32, y + 102, "НЕТ", 15, INK, 700)]
    o += [poly([(bx, 345), (bx, 254)], SOFT, 2.5, mk),
          poly([(bx + 150, 590), (bx + 175, 590), (bx + 175, 200), (bx + 156, 200)], SOFT, 2.5, mk),
          poly([(dx, 665), (dx, 720), (1116, 720)], SOFT, 2.5, mk), T(dx + 100, 708, "НЕТ", 15, INK, 700)]
    for i, y in enumerate(ys):
        o.append(_dia(dx, y, q[i], 300, 150))
        o.append(_gb(bx, y, 300, 96 if i != 1 else 100, bb[i]))
    o.append(_gb(1200, 720, 160, 90, ["Задать IP-", "адрес", "интерфейса"], 17))
    return fig("0 0 1420 780", "".join(o), d)


# ------------------------------------------------------------------ s65: Area 0, R1/R2/R3
def s65():
    mk, d = marker(BLUE)
    w = 90
    o = ['<ellipse cx="600" cy="240" rx="585" ry="228" fill="#f3f8fe" stroke="#8fbff0" stroke-width="3"/>',
         T(600, 85, "Area 0", 26, INK, 800),
         ln(230, 260, 970, 260, INK, 4), ln(320, cy(150, w), 320, 260, INK, 4), ln(880, cy(150, w), 880, 260, INK, 4),
         ln(600, 260, 600, cy(330, w), INK, 4),
         R(320, 150, w, "b"), T(385, 170, "R1", 22, INK, 800, "start"),
         R(880, 150, w, "b"), T(945, 170, "R2", 22, INK, 800, "start"),
         R(600, 330, w, "b"), T(665, 350, "R3", 22, INK, 800, "start"),
         T(210, 62, "ID маршрутизатора:", 21, PINK, 700, "start"), T(210, 90, "1.1.1.1", 21, PINK, 700, "start", True),
         T(800, 62, "ID маршрутизатора:", 21, PINK, 700, "start"), T(800, 90, "2.2.2.2", 21, PINK, 700, "start", True),
         T(500, 410, "ID маршрутизатора :", 21, PINK, 700, "start"), T(500, 438, "3.3.3.3", 21, PINK, 700, "start", True),
         arr(400, 235, 545, 235, mk, BLUE, 4), T(400, 220, "Я 1.1.1.1.", 22, BLUE, 700, "start")]
    return fig("0 0 1200 480", "".join(o), d)


# ------------------------------------------------------------------ s68: RIP в UDP vs OSPF в IP
def s68():
    mk, d = marker(BLUE)
    hb, hp = ("#e3f0fd", "#8fbff0"), ("#fde7f0", "#f29cc2")
    o = [arr(30, 50, 660, 50, mk, BLUE, 4, True), T(345, 36, "IP пакет", 20, INK, 700),
         arr(250, 105, 660, 105, mk, BLUE, 4, True), T(455, 91, "UDP датаграмма", 20, INK, 700),
         box(20, 140, 220, 90, hb[0], hb[1], 0, 3), ml(130, 185, ["Заголовок", "IP"], 20, INK, 800),
         box(240, 140, 220, 90, hb[0], hb[1], 0, 3), ml(350, 185, ["Заголовок", "UDP"], 20, INK, 800),
         box(460, 140, 200, 90, hp[0], hp[1], 0, 3), T(560, 192, "RIP PDU", 20, INK, 800),
         T(130, 265, "20 байт", 19, INK, 700), T(350, 265, "8 байт", 19, INK, 700),
         arr(780, 105, 1250, 105, mk, BLUE, 4, True), T(1015, 91, "IP пакет", 20, INK, 700),
         box(770, 140, 230, 90, hb[0], hb[1], 0, 3), ml(885, 185, ["Заголовок", "IP"], 20, INK, 800),
         box(1000, 140, 250, 90, hp[0], hp[1], 0, 3), T(1125, 192, "OSPF PDU", 20, INK, 800),
         T(885, 265, "20 байт", 19, INK, 700)]
    return fig("0 10 1270 280", "".join(o), d)


# ------------------------------------------------------------------ s69–74: форматы пакетов OSPF
HDR = ("#ffe6d2", "#f0a878")
BOD = ("#dcebfb", "#8fbff0")
TYP = ("#ffb98a", "#e8834a")
X0, BW, RH = 160, 24, 46


def _type(n):
    return 'Type = <tspan style="fill:%s">%s</tspan>' % (RED, n) if n else '<tspan style="fill:%s">Type</tspan>' % RED


def _grid(n, body, y0=40, x0=X0):
    """Сетка 32 бита: заголовок OSPF (5 строк) + строки body [(bits, текст), ...]."""
    rows = [[(8, "Version", HDR), (8, _type(n), TYP), (16, "Packet Length", HDR)],
            [(32, "Router ID", HDR)], [(32, "Area ID", HDR)],
            [(16, "Checksum", HDR), (16, "Authentication Type", HDR)], [(32, "Authentication", HDR)]]
    rows += [[(b, s, BOD) for b, s in r] for r in body]
    o = [T(x0, y0 - 10, "0", 17, INK, 700, mono=True), T(x0 + 8 * BW, y0 - 10, "8", 17, INK, 700, mono=True),
         T(x0 + 16 * BW, y0 - 10, "16", 17, INK, 700, mono=True), T(x0 + 32 * BW, y0 - 10, "31", 17, INK, 700, mono=True)]
    for i, r in enumerate(rows):
        x, y = x0, y0 + i * RH
        for bits, s, (f, st) in r:
            ww = bits * BW
            o.append(box(x, y, ww, RH, f, st, 0, 2.5))
            o.append(T(x + ww / 2, y + RH / 2 + 7, s, 20 if bits > 2 else 15, INK, 800))
            x += ww
    return "".join(o), y0 + len(rows) * RH


def _table(y, cells, x0=10, w=1180, h=74, title=None):
    o = []
    if title:
        o += [box(x0, y, w, 36, HDR[0], HDR[1], 0, 2), T(x0 + w / 2, y + 25, title, 18, INK, 800)]
        y += 36
    cw = w / len(cells)
    for i, (lines, col) in enumerate(cells):
        o.append(box(x0 + i * cw, y, cw, h, col[0], col[1], 0, 2))
        o.append(ml(x0 + i * cw + cw / 2, y + h / 2, lines, 15.5, INK, 800))
    return "".join(o)


def s69():
    g, yb = _grid(0, [])
    tx = X0 + 8 * BW
    o = ['<path d="M%.1f 40 L%.1f 40 L1010 14 L1010 226 Z" fill="#ffd2b0" opacity=".7"/>' % (tx, tx + 8 * BW), g,
         box(1000, 10, 170, 220, "#ffd2b0", TYP[1], 14, 2.5)]
    for i in range(5):
        o.append(T(1030, 48 + i * 40, 'Type = <tspan style="fill:%s">%d</tspan>' % (RED, i + 1), 22, INK, 800, "start"))
    cells = [(["Версия"], HDR), (["Тип"], TYP), (["Длина пакета"], HDR), (["Идентификатор", "маршрутизатора"], HDR),
             (["Идентификатор", "области"], HDR), (["Контрольная", "сумма"], HDR), (["Тип", "аутентификации"], HDR),
             (["Аутентификации"], HDR)]
    o.append(_table(yb + 40, cells, title="Заголовок пакета OSPF"))
    return fig("0 0 1200 %d" % (yb + 160), "".join(o))


def s70():
    mk, d = marker(BLUE)
    g, yb = _grid(1, [[(32, "Network mask")], [(16, "Hello Interval"), (8, "Options"), (8, "Priority")],
                      [(32, "Dead Interval")], [(32, "Designated Router")], [(32, "Backup Designated Router")],
                      [(32, "Neighbor ID")]], x0=250)
    o = [g, arr(215, 44, 215, 40 + 5 * RH - 4, mk, BLUE, 4, True),
         '<g transform="translate(190 %.1f) rotate(-90)">%s</g>' % (40 + 2.5 * RH, T(0, 0, "Заголовок", 20, INK, 700))]
    cells = [(["Заголовок", "OSPF"], HDR), (["Маска", "подсети"], BOD), (["Таймер", "приветствия"], BOD),
             (["Опции"], BOD), (["Приоритет"], BOD), (["Таймер", "смерти"], BOD), (["Адрес DR"], BOD),
             (["Адрес BDR"], BOD), (["ID соседа"], BOD)]
    o.append(_table(yb + 30, cells))
    return fig("0 0 1200 %d" % (yb + 114), "".join(o), d)


def _hdr_only(n, body):
    g, yb = _grid(n, body)
    return fig("100 0 %d %d" % (32 * BW + 120, yb + 16), g)


def s71():
    flags = [(1, c) for c in ("0", "0", "0", "0", "0", "I", "M", "MS")]
    return _hdr_only(2, [[(16, "Interface MTU"), (8, "Options")] + flags, [(32, "DD Sequence Number")]])


def s72():
    return _hdr_only(3, [[(32, "LS Type")], [(32, "Link State ID")], [(32, "Advertising Router")]])


def s73():
    return _hdr_only(4, [[(32, "Number of LSA")], [(32, "LSA Header")], [(32, "LSA Data")]])


def s74():
    return _hdr_only(5, [[(32, "LSA headers")]])


# ------------------------------------------------------------------ s78: ESR-1 — ESR-2, Area 8.0.0.0
def s78():
    mk, d = marker(BLUE)
    w = 110
    o = [box(200, 30, 500, 190, "#ffe6d2", "#f0a878", 18, 2.5),
         T(450, 66, "OSPF", 24, INK, 800), T(450, 205, "Area: 8.0.0.0", 20, INK, 800),
         ln(150, cy(110, w), 750, cy(110, w), INK, 5),
         arr(225, 105, 675, 105, mk, BLUE, 5, True),
         R(150, 110, w, "b"), R(750, 110, w, "b"),
         T(150, 195, "ESR-1", 22, INK, 800), T(750, 195, "ESR-2", 22, INK, 800),
         lbl(215, 160, "Gi1/0/1", 19, INK, "start"), lbl(685, 160, "Gi1/0/1", 19, INK, "end")]
    return fig("70 10 760 220", "".join(o), d)


# ------------------------------------------------------------------ s86: RIP / OSPF Area 1.1.1.1
def s86():
    w = 130
    o = [box(10, 10, 380, 440, "#e6f7ec", "#86d3a8", 22, 3), box(390, 10, 900, 440, "#ffeedd", "#f0a878", 22, 3),
         T(360, 48, "RIP", 24, INK, 800, "end"), T(370, 78, "Gi1/0/1", 20, INK, 800, "end", True),
         T(410, 48, "OSPF", 24, INK, 800, "start"), T(410, 78, "Area: 1.1.1.1", 22, INK, 800, "start"),
         T(370, 425, "Gi1/0/2", 20, INK, 800, "end", True),
         cloudsvg(150, 150, 230, 100, "LAN-31", "192.168.31.0/24", "v", 21),
         cloudsvg(150, 300, 230, 100, "LAN-32", "192.168.32.0/24", "v", 21),
         cloudsvg(1130, 130, 250, 100, "LAN-11", "192.168.11.0/24", "v", 21),
         cloudsvg(1130, 330, 250, 100, "LAN-21", "192.168.21.0/24", "v", 21),
         ln(330, cy(210, w), 860, cy(110, w), INK, 7), ln(330, cy(210, w), 860, cy(310, w), INK, 7),
         R(330, 210, w, "b", "R3", 0, 105, 24), R(860, 110, w, "b", "R1", 0, 105, 24),
         R(860, 310, w, "b", "R2", 0, 105, 24),
         lbl(420, 180, "Gi1/0/5", 20), lbl(425, 215, ".1", 20), lbl(610, 160, "198.51.100.0/24", 20),
         lbl(770, 120, ".2", 20), lbl(430, 270, ".1", 20), lbl(640, 268, "203.0.113.0/24", 20),
         lbl(440, 312, "Gi1/0/15", 20), lbl(770, 360, ".2", 20)]
    return fig("0 0 1300 460", "".join(o))


FIGS = {
    "s55_image88": s55,
    "s58_image93": lambda: types("p2p"),
    "s59_image93": lambda: types("bma"),
    "s60_image93": lambda: types("nbma"),
    "s61_image93": lambda: types("p2mp"),
    "s58_image94": s58_links,
    "s59_image95": s59_links,
    "s60_image96": s60_links,
    "s61_image97": s61_links,
    "s63_image99": s63,
    "s64_image100": s64,
    "s65_image102": s65,
    "s68_image104": s68,
    "s69_image105": s69,
    "s70_image106": s70,
    "s71_image107": s71,
    "s72_image108": s72,
    "s73_image109": s73,
    "s74_image110": s74,
    "s78_image117": s78,
    "s86_image131": s86,
}
