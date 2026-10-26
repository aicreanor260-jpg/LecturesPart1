# -*- coding: utf-8 -*-
"""Схемы деки «IP-сервисы 2.6 (по pptx)»: рисунки pptx перерисованы в стиле инфографик автора —
тёмное стекло, неоновые линии, устройства-вырезки из инфографик. Адреса, порты и подписи — как на рисунках pptx.
Цвет текста SVG — через style (общий CSS красит svg text в белый)."""
import base64
import io
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = os.path.join(HERE, "_i6_assets", "dev")
_cache = {}

BL = "#3aa0ff"   # одноадресная / от сервера (синие стрелки pptx)
RD = "#ff5a6a"   # широковещательная / от клиента (красные стрелки pptx)
CY = "#5cd2ff"
AM = "#ffc94a"
LM = "#6ee07a"
VI = "#b77bff"
INK = "#eaf4ff"
SOFT = "#a9c4ea"
MONO = "JetBrains Mono,Consolas,monospace"


def _uri(name):
    if name not in _cache:
        buf = io.BytesIO()
        Image.open(os.path.join(DEV, name + ".png")).save(buf, "WEBP", quality=86, method=5)
        _cache[name] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[name]


_RATIO = {"laptop": 183 / 284.0, "router": 260 / 292.0, "servers": 182 / 253.0, "switch": 90 / 220.0}


def dev(kind, cx, y, w):
    """Устройство из инфографик: laptop | router | servers | switch; cx — центр, y — верх."""
    h = w * _RATIO[kind]
    return '<image href="%s" x="%g" y="%g" width="%g" height="%g"/>' % (_uri(kind), cx - w / 2.0, y, w, h)


def t(x, y, s, size=18, col=INK, w=700, anchor="middle", mono=False, extra=""):
    fam = "font-family:%s;" % MONO if mono else ""
    return ('<text x="%g" y="%g" text-anchor="%s" style="fill:%s;font-size:%gpx;font-weight:%d;%s"%s>%s</text>'
            % (x, y, anchor, col, size, w, fam, extra, s))


def defs():
    m = "".join('<marker id="i6a%s" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">'
                '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>' % (k, c)
                for k, c in (("b", BL), ("r", RD), ("c", CY), ("a", AM), ("g", LM), ("s", SOFT)))
    return ('<defs>%s<filter id="i6gl" x="-40%%" y="-40%%" width="180%%" height="180%%"><feGaussianBlur stdDeviation="4" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>' % m)


def svg(body, w=1200, h=560):
    return '<svg class="fig i6fig" viewBox="0 0 %d %d">%s%s</svg>' % (w, h, defs(), body)


def wrap(html):
    return '<div class="figwrap i6panel">%s</div>' % html


_MK = {BL: "b", RD: "r", CY: "c", AM: "a", LM: "g", SOFT: "s"}


def line(x1, y1, x2, y2, col=CY, w=3, arrow=False, dash=False, extra=""):
    mk = ' marker-end="url(#i6a%s)"' % _MK.get(col, "c") if arrow else ""
    d = ' stroke-dasharray="10 7"' if dash else ""
    return ('<path d="M%g %gL%g %g" style="stroke:%s;stroke-width:%g;fill:none" stroke-linecap="round"%s%s%s/>'
            % (x1, y1, x2, y2, col, w, mk, d, extra))


def box(x, y, w, h, col=CY, fill="rgba(10,28,66,.88)", r=12, sw=2, extra=""):
    return ('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" style="fill:%s;stroke:%s;stroke-width:%g"%s/>'
            % (x, y, w, h, r, fill, col, sw, extra))


def ph(n, body, only=False):
    return '<g data-ph="%d"%s>%s</g>' % (n, " data-ph-only" if only else "", body)


def cloud(cx, cy, w, label, sub=""):
    h = w * .5
    p = ("M{a} {b}c-40 0-60-50-20-70c0-50 70-70 100-40c20-50 110-55 130 0c50-15 90 30 60 70c30 20 10 60-30 60z"
         .format(a=cx - w * .3, b=cy + h * .25))
    s = w / 300.0
    o = ['<g transform="translate(%g %g) scale(%g) translate(%g %g)">' % (cx, cy, s, -cx, -cy),
         '<path d="%s" style="fill:rgba(40,110,210,.35);stroke:%s;stroke-width:3" filter="url(#i6gl)"/></g>' % (p, CY)]
    o.append(t(cx + w * .02, cy + 4, label, 20 * max(.8, s), "#fff", 800))
    if sub:
        o.append(t(cx + w * .02, cy + 28, sub, 15, SOFT, 600))
    return "".join(o)


# ------------------------------------------------------------------ диаграммы обмена DHCP (pptx 4–7)
def ladder(msgs, left="DHCP-клиент", right="DHCP-сервер", x1=150, x2=690, top=40, gap=96, past=False, dots_top=False,
           times=None, w=1200, ox=0):
    """msgs: (имя, пояснение, 'r'|'l', цвет[, 'out' — стрелка дальше сервера]). times: {индекс: 'T0'}."""
    o = []
    x1 += ox
    x2 += ox
    h = top + 140 + 54 + gap * (len(msgs) - 1) + 44
    o.append(dev("laptop", x1, top, 150))
    o.append(dev("servers", x2, top - 4, 130))
    o.append(t(x1, top + 124, left, 21, "#fff", 800))
    o.append(t(x2, top + 124, right, 21, "#fff", 800))
    y0 = top + 140
    o.append(line(x1, y0, x1, h, SOFT, 3))
    o.append(line(x2, y0, x2, h, SOFT, 3))
    if dots_top:
        o.append(t((x1 + x2) / 2, y0 + 12, ". . .", 20, SOFT, 700))
    for i, m in enumerate(msgs):
        name, sub, d, col = m[:4]
        out = len(m) > 4 and m[4] == "out"
        y = y0 + 54 + gap * i
        a, b = (x1, x2) if d == "r" else (x2, x1)
        if out:
            a, b = (x1, x2 + 170) if d == "r" else (x2 + 170, x1)
        o.append(ph(i + 1, t((x1 + x2) / 2, y - 12, name, 24, "#fff", 800)
                    + line(a, y, b, y, col, 4, True)
                    + t((x1 + x2) / 2, y + 26, sub, 17, SOFT, 600)))
        if times and i in times:
            o.append(ph(i + 1, t(x1 - 26, y + 6, times[i], 20, AM, 800, "end")))
    if past:
        o.append(t((x1 + x2) / 2, h - 6, ". . .", 20, SOFT, 700))
    return o, h


def seq(msgs, **kw):
    o, h = ladder(msgs, **kw)
    w = kw.get("x2", 690) + (250 if any(len(m) > 4 for m in msgs) else 120)
    return svg("".join(o), w, h + 10)


def legend(items):
    return ('<div class="i6leg">%s</div>'
            % "".join('<span><i style="background:%s"></i>%s</span>' % (c, s) for c, s in items))


def lease():
    """pptx 7: слева продление в T0, справа T0 → T1 → истечение → DHCPDISCOVER."""
    left, h1 = ladder([("DHCPREQUEST", "(Принимаю предложенный IPv4-адрес)", "r", BL),
                       ("DHCPACK", "(Подтверждаю принятие IPv4-адреса)", "l", BL)],
                      x1=130, x2=500, gap=100, times={0: "T0"})
    right, h2 = ladder([("DHCPREQUEST", "(Принимаю предложенный IPv4-адрес)", "r", BL),
                        ("DHCPREQUEST", "(Принимаю предложенный IPv4-адрес)", "r", RD),
                        ("DHCPREQUEST", "(Принимаю предложенный IPv4-адрес)", "r", RD),
                        ("DHCPDISCOVER", "(Мне необходим IPv4-адрес)", "r", RD)],
                       x1=710, x2=1080, gap=92, times={0: "T0", 1: "T1", 3: "t"})
    right.append(t(895, 284, ". . .", 20, SOFT, 700))
    return svg("".join(left + right), 1200, max(h1, h2) + 10)


# ------------------------------------------------------------------ pptx 12: DHCP relay
def relay():
    o = [line(150, 190, 1010, 190, CY, 4)]
    o.append(dev("laptop", 150, 100, 190))
    o.append(dev("router", 600, 80, 190))
    o.append(dev("servers", 1030, 90, 170))
    o.append(t(600, 268, "R1", 24, "#fff", 900))
    o.append(t(600, 300, "R1(config)#ip dhcp-relay", 20, AM, 700, mono=True))
    o.append(t(1030, 250, "DHCP-СЕРВЕР", 22, "#fff", 900))
    o.append(t(1030, 278, "203.0.113.254/24", 20, SOFT, 700, mono=True))
    o.append(ph(1, env(355, 112, "broadcast", RD) + line(300, 172, 480, 172, RD, 3, True)))
    o.append(ph(2, env(790, 112, "unicast", BL) + line(710, 172, 900, 172, BL, 3, True)))
    return svg("".join(o), 1200, 330)


def env(cx, y, label, col):
    return ('<g><rect x="%g" y="%g" width="74" height="48" rx="5" style="fill:#f3d68a;stroke:#b8902e;stroke-width:2"/>'
            '<path d="M%g %gl37 24l37-24" style="fill:none;stroke:#b8902e;stroke-width:2"/></g>'
            % (cx - 37, y - 30, cx - 37, y - 30)) + t(cx, y + 38, label, 17, col, 700)


# ------------------------------------------------------------------ pptx 17: внутренняя сеть → NAT → Интернет
def nat_clouds():
    o = [cloud(290, 160, 380, "Внутренняя сеть", "Частные IPv4-адреса"),
         cloud(910, 160, 380, "Интернет", "Публичные IPv4-адреса"),
         dev("router", 600, 70, 170), t(600, 240, "NAT", 24, "#fff", 900),
         '<path d="M330 280h520v-22l60 42-60 42v-22h-520z" style="fill:rgba(255,160,90,.25);stroke:#ff9a4a;stroke-width:2.5"/>',
         t(600, 309, "Преобразование NAT", 22, "#ffd0a8", 800)]
    return svg("".join(o), 1200, 360)


# ------------------------------------------------------------------ pptx 28: SNAT
def pkt(x, y, w, l1, l2, col=AM):
    return (box(x, y, w, 70, col, "rgba(60,44,8,.85)", 10, 2.5)
            + t(x + 14, y + 29, l1, 17, "#fff", 700, "start", True)
            + t(x + 14, y + 55, l2, 17, "#fff", 700, "start", True))


def ntable(x, y, cols, rows, title="", w=None, colw=None, hl=None, col=CY, mark="Соответствие"):
    """Таблица в стиле деки внутри SVG."""
    n = len(cols)
    colw = colw or [(w or 160 * n) / float(n)] * n
    W = sum(colw)
    rh = 38
    o = []
    hy = y
    if title:
        o.append(t(x + W / 2, y + 26, title, 20, "#fff", 800))
        hy = y + 40
    o.append(box(x, hy, W, rh * (len(rows) + 1) + 8, col, "rgba(8,22,54,.92)", 10, 2))
    cx = x
    for i, c in enumerate(cols):
        o.append('<rect x="%g" y="%g" width="%g" height="%g" style="fill:rgba(58,160,255,.35)"/>' % (cx + 4, hy + 4, colw[i] - 8, rh))
        o.append(t(cx + colw[i] / 2, hy + 26, c, 16, "#fff", 800))
        for j, r in enumerate(rows):
            fill = AM if hl is not None and j == hl else INK
            o.append(t(cx + colw[i] / 2, hy + 26 + rh * (j + 1) + 4, r[i], 17, fill, 700, mono=True))
        cx += colw[i]
    if hl is not None and mark:
        o.append(t(x + W + 10, hy + 26 + rh * (hl + 1) + 4, mark, 17, AM, 800, "start"))
    return "".join(o)


def snat():
    o = [line(130, 330, 1000, 330, CY, 4), line(1000, 330, 1060, 420, CY, 4)]
    o.append(ntable(370, 10, ["Inside source", "Inside destination", "outside source", "outside destination"],
                    [["192.0.2.2:53314", "203.0.113.1:80", "198.51.100.1:53314", "203.0.113.1:80"]],
                    "Таблица трансляции", colw=[200, 200, 210, 210]))
    o.append(dev("laptop", 120, 260, 170))
    o.append(t(120, 400, "192.0.2.2", 20, "#fff", 800, mono=True))
    o.append(dev("router", 600, 245, 150))
    o.append(t(600, 395, "R1", 22, "#fff", 900))
    o.append(t(600, 422, "SNAT", 20, AM, 900))
    o.append(t(505, 372, "192.0.2.1", 18, SOFT, 700, mono=True))
    o.append(t(708, 372, "198.51.100.1", 18, SOFT, 700, mono=True))
    o.append(cloud(990, 300, 230, "Интернет"))
    o.append(dev("servers", 1070, 420, 120))
    o.append(t(1070, 530, "203.0.113.1", 20, "#fff", 800, mono=True))
    o.append(ph(1, pkt(185, 190, 330, "SrcIP: 192.0.2.2 port:53314", "DstIP: 203.0.113.1 port: 80")))
    o.append(ph(2, pkt(700, 190, 350, "SrcIP: 198.51.100.1 port:53314", "DstIP: 203.0.113.1 port: 80")))
    return svg("".join(o), 1200, 545)


# ------------------------------------------------------------------ pptx 29–31: частная сеть → NAT → Интернет
HOSTS = ["192.168.1.1/24", "192.168.1.2/24", "192.168.1.3/24"]


def lan(w=1200):
    """Каркас схемы Huawei-примеров pptx 29–31: три узла, коммутатор, NAT 122.1.2.1, Интернет, веб-сервер 200.1.2.3."""
    o = [box(18, 150, 500, 395, CY, "rgba(20,60,120,.18)", 22, 2), t(150, 182, "Частная сеть", 20, "#fff", 800)]
    for i, hst in enumerate(HOSTS):
        y = 210 + i * 112
        o.append(line(160, y + 30, 300, 345, CY, 3))
        o.append(dev("laptop", 110, y, 110))
        o.append(t(110, y + 92, hst, 17, "#fff", 700, mono=True))
    o.append(line(300, 345, 620, 345, CY, 3.5))
    o.append(line(620, 345, 1080, 345, CY, 3.5))
    o.append(dev("switch", 300, 320, 120))
    o.append(t(440, 334, "192.168.1.254", 17, SOFT, 700, mono=True))
    o.append(dev("router", 620, 290, 110))
    o.append(t(620, 405, "NAT", 21, "#fff", 900))
    o.append(t(720, 334, "122.1.2.1", 17, SOFT, 700, mono=True))
    o.append(cloud(860, 345, 170, "Интернет"))
    o.append(dev("servers", 1100, 280, 110))
    o.append(t(1100, 380, "Веб-сервер", 18, "#fff", 800))
    o.append(t(1100, 402, "200.1.2.3", 17, SOFT, 700, mono=True))
    return o


def note(x, y, w, lines, col=AM):
    h = 16 + 25 * len(lines)
    o = [box(x, y, w, h, col, "rgba(60,44,8,.9)", 10, 2)]
    for i, s in enumerate(lines):
        o.append(t(x + 14, y + 30 + 25 * i, s, 17, "#fff", 600, "start"))
    return "".join(o)


def addr(x, y, w, n, lines, col=CY):
    """Плашка «IP-адрес источника / назначения» с номером шага."""
    h = 14 + 25 * len(lines)
    o = ['<circle cx="%g" cy="%g" r="16" style="fill:%s"/>' % (x - 24, y + 18, col), t(x - 24, y + 25, str(n), 19, "#08142e", 900)]
    o.append(box(x, y, w, h, col, "rgba(8,22,54,.92)", 8, 2, ' stroke-dasharray="6 4"'))
    for i, s in enumerate(lines):
        o.append(t(x + 12, y + 28 + 25 * i, s, 16, "#fff", 600, "start"))
    return "".join(o)


def static_nat():
    """pptx 29: статический NAT — таблица сопоставления, затем обмен с веб-сервером и внешним узлом."""
    o = lan()
    o.append(dev("laptop", 1100, 440, 100))
    o.append(line(890, 360, 1060, 470, CY, 3))
    o.append(t(1100, 532, "Внешний узел 202.1.2.3", 17, "#fff", 700))
    o.append(ph(1, ntable(560, 10, ["Частный адрес", "Публичный адрес"],
                          [["192.168.1.1", "122.1.2.1"], ["192.168.1.2", "122.1.2.2"], ["192.168.1.3", "122.1.2.3"]],
                          "Таблица сопоставления NAT", colw=[200, 200]), True))
    o.append(ph(2, addr(60, 20, 330, 1, ["IP-адрес источника: 192.168.1.1", "IP-адрес назначения: 200.1.2.3"], BL)
             + addr(450, 20, 330, 2, ["IP-адрес источника: 122.1.2.1", "IP-адрес назначения: 200.1.2.3"], BL), True))
    o.append(ph(3, addr(450, 20, 330, 3, ["IP-адрес источника: 200.1.2.3", "IP-адрес назначения: 122.1.2.1"], RD)
             + addr(60, 20, 330, 4, ["IP-адрес источника: 200.1.2.3", "IP-адрес назначения: 192.168.1.1"], RD)
             + note(820, 10, 370, ["Адрес источника 192.168.1.1", "преобразуется в 122.1.2.1 для", "доступа в Интернет.",
                                   "IP-адрес назначения 122.1.2.1", "пакета, возвращаемого из Интернета,",
                                   "преобразуется в 192.168.1.1."]), True))
    o.append(ph(4, addr(450, 20, 330, 1, ["IP-адрес источника: 202.1.2.3", "IP-адрес назначения: 122.1.2.3"], RD)
             + addr(60, 20, 330, 2, ["IP-адрес источника: 202.1.2.3", "IP-адрес назначения: 192.168.1.3"], RD), True))
    o.append(ph(5, addr(60, 20, 330, 3, ["IP-адрес источника: 192.168.1.3", "IP-адрес назначения: 202.1.2.3"], BL)
             + addr(450, 20, 330, 4, ["IP-адрес источника: 122.1.2.3", "IP-адрес назначения: 202.1.2.3"], BL)
             + note(820, 10, 370, ["Когда внешний узел отправляет пакет", "для проактивного доступа к 122.1.2.3,",
                                   "выходное устройство посредством NAT", "преобразует адрес назначения пакета",
                                   "в 192.168.1.3. IP-адрес источника",
                                   "пакета, отправленного с 192.168.1.3,", "преобразуется NAT в 122.1.2.3,",
                                   "когда пакет проходит через", "выходное устройство."]), True))
    return svg("".join(o), 1200, 560)


def pool(x, y, rows, title="Пул адресов NAT", hl=None):
    h = 60 + 34 * len(rows)
    o = [box(x, y, 300, h, CY, "rgba(8,22,54,.94)", 10, 2), t(x + 150, y + 30, title, 19, "#fff", 800),
         line(x + 24, y + 44, x + 276, y + 44, SOFT, 1.5, dash=True)]
    for i, r in enumerate(rows):
        a, st = (r if isinstance(r, tuple) else (r, ""))
        c = RD if st == "In Use" else CY
        if hl == i:
            o.append(box(x + 10, y + 52 + 34 * i, 280, 32, AM, "rgba(255,201,74,.22)", 6, 1.5, ' stroke-dasharray="5 4"'))
            o.append(t(x - 8, y + 76 + 34 * i, "Выбор", 18, AM, 800, "end"))
        o.append(t(x + 40, y + 76 + 34 * i, a, 18, c, 700, "start", True))
        if st:
            o.append(t(x + 270, y + 76 + 34 * i, st, 18, c, 700, "end"))
    return "".join(o)


def dyn_nat():
    """pptx 30: пул Not Use → выбор 122.1.2.2 (In Use) и временная таблица → обратное преобразование."""
    o = lan()
    o.append(ph(0, pool(600, 20, [("122.1.2.1", "Not Use"), ("122.1.2.2", "Not Use"), ("122.1.2.3", "Not Use")]), True))
    o.append(ph(1, addr(60, 20, 330, 1, ["IP-адрес источника: 192.168.1.1", "IP-адрес назначения: 200.1.2.3"], BL)
             + pool(440, 10, [("122.1.2.1", "In Use"), ("122.1.2.2", "Not Use"), ("122.1.2.3", "Not Use")], hl=1)
             + note(770, 10, 420, ["Шаг 1.", "Выбирает неиспользуемый адрес в пуле",
                                   "адресов в качестве адреса для последующего",
                                   "преобразования и помечает адрес как In Use."]), True))
    o.append(ph(2, addr(820, 160, 330, 2, ["IP-адрес источника: 122.1.2.2", "IP-адрес назначения: 200.1.2.3"], BL)
             + note(560, 10, 330, ["Шаг 2.", "Создает временную таблицу", "соответствия NAT."])
             + ntable(560, 420, ["Частный адрес", "Публичный адрес"],
                      [["192.168.1.1", "122.1.2.2"], ["192.168.1.2", "122.1.2.1"]], "Таблица сопоставления NAT", colw=[170, 170]), True))
    o.append(ph(3, addr(820, 160, 330, 3, ["IP-адрес источника: 200.1.2.3", "IP-адрес назначения: 122.1.2.2"], RD)
             + ntable(560, 420, ["Частный адрес", "Публичный адрес"],
                      [["192.168.1.1", "122.1.2.2"], ["192.168.1.2", "122.1.2.1"]], "Таблица сопоставления NAT", colw=[170, 170], hl=0)
             + note(420, 10, 400, ["Поиск в таблице сопоставления NAT", "необходимого частного IP-адреса на основе",
                                   "публичного IP-адреса и преобразование", "IP-адреса назначения пакета IP-данных",
                                   "в частный адрес."]), True))
    o.append(ph(4, addr(60, 20, 330, 4, ["IP-адрес источника: 200.1.2.3", "IP-адрес назначения: 192.168.1.1"], RD)
             + ntable(560, 420, ["Частный адрес", "Публичный адрес"],
                      [["192.168.1.1", "122.1.2.2"], ["192.168.1.2", "122.1.2.1"]], "Таблица сопоставления NAT", colw=[170, 170], hl=0), True))
    return svg("".join(o), 1200, 600)


def napt():
    """pptx 31: NAPT — пул, выбор 122.1.2.2, таблица IP:порт, обратное преобразование."""
    o = lan()
    tb = ["Частный IP-адрес:Номер порта", "Публичный IP-адрес:Номер порта"]
    rows = [["192.168.1.1:10321", "122.1.2.2:1025"], ["192.168.1.2:17087", "122.1.2.2:1026"]]
    o.append(ph(0, pool(600, 20, ["122.1.2.1", "122.1.2.2", "122.1.2.3"])
             + ntable(560, 420, tb, rows, "Таблица сопоставления NAT", colw=[300, 300]), True))
    o.append(ph(1, addr(60, 20, 300, 1, ["Источник: 192.168.1.1:10321", "Назначение: 200.1.2.3:80"], BL)
             + pool(400, 10, ["122.1.2.1", "122.1.2.2", "122.1.2.3"], hl=1)
             + note(740, 10, 440, ["Шаг 1.", "Выбирает адрес из пула адресов и преобразует",
                                   "и IP-адрес источника и номер порта."]), True))
    o.append(ph(2, addr(860, 140, 300, 2, ["Источник: 122.1.2.2:1025", "Назначение: 200.1.2.3:80"], BL)
             + note(540, 10, 460, ["Шаг 2.", "Генерирует временную таблицу сопоставления NAT,",
                                   "в которую записывается: [IP-адрес источника:номер",
                                   "порта перед преобразованием], [IP-адрес:номер", "порта после преобразования]."])
             + ntable(560, 420, tb, rows, "Таблица соответствия", colw=[300, 300], hl=0, mark=""), True))
    o.append(ph(3, addr(860, 140, 300, 3, ["Источник: 200.1.2.3:80", "Назначение: 122.1.2.2:1025"], RD)
             + note(420, 10, 470, ["Поиск в таблице сопоставления NAT необходимого",
                                   "частного IP-адреса и номера порта на основе",
                                   "публичного IP-адреса и номера порта и", "преобразование IP-адреса назначения и номера",
                                   "порта пакета IP-данных в частный адрес."])
             + ntable(560, 420, tb, rows, "Таблица сопоставления NAT", colw=[300, 300], hl=0, mark=""), True))
    o.append(ph(4, addr(60, 20, 300, 4, ["Источник: 200.1.2.3:80", "Назначение: 192.168.1.1:10321"], RD)
             + ntable(560, 420, tb, rows, "Таблица сопоставления NAT", colw=[300, 300], hl=0, mark=""), True))
    return svg("".join(o), 1200, 600)


def dnat():
    """pptx 32: R1 198.51.100.1 → Интернет → R2 (DNAT) 203.0.113.1 / 10.10.10.1 → сервер 10.10.10.2."""
    o = [line(110, 160, 1100, 160, CY, 4)]
    o.append(dev("router", 110, 70, 130))
    o.append(t(110, 214, "R1", 20, "#fff", 900))
    o.append(t(110, 240, "198.51.100.1", 18, SOFT, 700, mono=True))
    o.append(cloud(330, 140, 210, "Интернет"))
    o.append(dev("router", 720, 70, 130))
    o.append(t(720, 214, "R2", 20, "#fff", 900))
    o.append(t(720, 240, "DNAT", 18, AM, 900))
    o.append(t(600, 200, "203.0.113.1", 18, SOFT, 700, mono=True))
    o.append(t(850, 200, "10.10.10.1", 18, SOFT, 700, mono=True))
    o.append(dev("servers", 1100, 80, 120))
    o.append(t(1100, 210, "10.10.10.2", 18, "#fff", 800, mono=True))
    o.append(ph(1, pkt(410, 20, 330, "SrcIP: 198.51.100.1 port:53314", "DstIP: 203.0.113.1 port: 80")))
    o.append(ph(2, ntable(450, 270, ["outside destination", "IP"], [["203.0.113.1:80", "10.10.10.2:80"]],
                          "Таблица правил", colw=[200, 200])))
    o.append(ph(3, pkt(790, 20, 330, "SrcIP: 198.51.100.1 port:53314", "DstIP: 10.10.10.2 port: 80")))
    return svg("".join(o), 1200, 410)


# ------------------------------------------------------------------ pptx 41: алгоритм Марзулло
def marzullo():
    X0, K = 150, 140   # 8 → x=150, шаг 1 = 140 px
    o = []

    def X(v):
        return X0 + (v - 8) * K
    for v in range(8, 15):
        o.append(line(X(v), 20, X(v), 400, "rgba(169,196,234,.45)", 1.5, dash=True))
        o.append(t(X(v), 432, str(v), 20, SOFT, 700))
    rows = [("[8, 12]", 8, 12, 10, "10 ± 2", 60), ("[10, 12]", 10, 12, 11, "11 ± 1", 140), ("[11, 13]", 11, 13, 12, "12 ± 1", 220)]
    for i, (lab, a, b, m, s, y) in enumerate(rows):
        o.append(ph(i + 1, t(110, y + 7, lab, 20, "#fff", 700, "end", True) + line(X(a), y, X(b), y, BL, 7)
                    + '<circle cx="%g" cy="%g" r="9" style="fill:%s"/>' % (X(m), y, BL) + t(X(m) + 6, y - 14, s, 20, AM, 800)))
    o.append(ph(4, line(60, 250, 60, 320, BL, 6, True) + t(110, 367, "[11, 12]", 20, "#fff", 700, "end", True)
                + line(X(11), 360, X(12), 360, RD, 7) + '<circle cx="%g" cy="%g" r="9" style="fill:%s"/>' % (X(11.5), 360, RD)
                + t(X(11.5), 342, "11,5 ± 0,5", 21, RD, 800)))
    return svg("".join(o), 1200, 450)


# ------------------------------------------------------------------ pptx 42: иерархия NTP (Stratum)
def stratum():
    o = []
    lv = [(0, 30, "rgba(120,170,255,.16)"), (1, 150, "rgba(110,224,122,.12)"), (2, 280, "rgba(110,224,122,.12)"),
          (3, 410, "rgba(110,224,122,.12)")]
    for n, y, f in lv:
        o.append(ph(n + 1, box(40, y, 1120, 100, SOFT, f, 16, 1.5) + t(70, y + 36, str(n), 30, "#fff", 900, "start")))
    s0 = [380, 600, 820]
    s1 = [380, 600, 820]
    s2 = [270, 490, 710, 930]
    s3 = [180, 360, 540, 720, 900, 1080]
    ph1 = "".join(line(x, 92, x, 152, AM, 3.5, True) for x in s0)
    ph2 = "".join(line(a, 232, b, 282, RD, 3, True) for a, b in [(380, 270), (380, 490), (600, 490), (600, 710), (820, 710), (820, 930)])
    ph3 = "".join(line(a, 362, b, 412, RD, 3, True) for a, b in
                  [(270, 180), (270, 360), (490, 360), (490, 540), (710, 540), (710, 720), (710, 900), (930, 900), (930, 1080)])
    o.append(ph(1, "".join(dev("servers", x, 38, 70) for x in s0)))
    o.append(ph(2, ph1 + "".join(dev("servers", x, 158, 76) for x in s1)
                + line(640, 196, 780, 196, RD, 3, True) + line(780, 196, 640, 196, RD, 3, True)))
    o.append(ph(3, ph2 + "".join(dev("servers", x, 288, 76) for x in s2)
                + "".join(line(a + 45, 326, b - 45, 326, RD, 3, True) + line(b - 45, 326, a + 45, 326, RD, 3, True)
                          for a, b in [(270, 490), (490, 710)])))
    o.append(ph(4, ph3 + "".join(dev("servers", x, 418, 76) for x in s3)
                + "".join(line(a + 45, 456, b - 45, 456, RD, 3, True) + line(b - 45, 456, a + 45, 456, RD, 3, True)
                          for a, b in [(360, 540), (720, 900), (900, 1080)])))
    return svg("".join(o), 1200, 520)


# ------------------------------------------------------------------ pptx 44: топология NTP
def ntp_topo():
    o = [line(240, 130, 960, 130, CY, 4)]
    o.append(dev("router", 200, 40, 160))
    o.append(dev("router", 1000, 40, 160))
    o.append(t(200, 80, "R1", 26, "#fff", 900))
    o.append(t(1000, 80, "NTP", 24, "#fff", 900))
    o.append(t(390, 112, "192.0.2.10/24", 24, "#fff", 800, mono=True))
    o.append(t(810, 112, "192.0.2.1/24", 24, "#fff", 800, mono=True))
    o.append(t(200, 220, "NTP-клиент", 24, "#fff", 800))
    o.append(t(1000, 220, "NTP-сервер", 24, "#fff", 800))
    return svg("".join(o), 1200, 240)


CSS = r"""
.figwrap.i6panel{background:linear-gradient(160deg,rgba(14,34,78,.82),rgba(5,13,34,.92));border:1.5px solid rgba(92,190,255,.75);
 border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35),inset 0 0 30px rgba(58,160,255,.08);padding:12px}
svg.i6fig{width:100%;height:auto;max-height:62vh;display:block}
.i6leg{display:flex;gap:22px;flex-wrap:wrap;font:700 clamp(12px,.95vw,18px)/1.3 var(--f);color:var(--soft);margin-top:4px}
.i6leg i{display:inline-block;width:34px;height:5px;border-radius:3px;margin-right:8px;vertical-align:middle}
"""
