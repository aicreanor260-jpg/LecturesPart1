# -*- coding: utf-8 -*-
"""Слайд «Схема сети: интернет и три офиса» — собственный SVG вместо растровой картинки.

Модуль грузится после s_fix.py и перекрывает ref p027.
Содержание схемы — по тексту лекции (слайд 4 исходного pptx).
Кегли подписей заданы с запасом: сборщик поднимает всё, что мельче 21px.
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

SLIDES = []

INK = "#2b3356"
DIM = "#6b7196"
BLUE = "#5a7df0"
PINK = "#c08ad8"
LINE = "#a5aedd"
CAP = 21          # кегль подписи под устройством
LEAD = 24         # кегль названия узла


def _plate(x, y, w, h, r=14, fill="url(#gDev)"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
            f'stroke="#b9b2dd" stroke-width="1.6" filter="url(#soft)"/>')


def _cap(x, y, text, size=CAP, col=DIM, weight=400, anchor="middle"):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{col}" '
            f'font-weight="{weight}">{text}</text>')


def router(cx, cy, w=118, h=50):
    x, y = cx - w / 2, cy - h / 2
    a = cx - 28
    return (_plate(x, y, w, h, 14)
            + f'<path d="M{a} {cy - 9}h38m0 0l-10-8m10 8l-10 8" stroke="{BLUE}" stroke-width="2.8" fill="none" '
              f'stroke-linecap="round" stroke-linejoin="round"/>'
            + f'<path d="M{a + 38} {cy + 9}h-38m0 0l10-8m-10 8l10 8" stroke="{BLUE}" stroke-width="2.8" fill="none" '
              f'stroke-linecap="round" stroke-linejoin="round"/>')


def switch(cx, cy, w=130, h=42):
    x, y = cx - w / 2, cy - h / 2
    g = [_plate(x, y, w, h, 12)]
    for i in range(8):
        px = x + 16 + i * ((w - 32) / 8)
        g.append(f'<rect x="{px:.1f}" y="{cy + 3}" width="8" height="10" rx="2" fill="#b7b0da"/>')
    g.append(f'<path d="M{x + 20} {cy - 8}h{w - 40}" stroke="{BLUE}" stroke-width="2.8" stroke-linecap="round"/>')
    return "".join(g)


def pc(cx, cy, w=72, h=46):
    x, y = cx - w / 2, cy - h / 2
    return (_plate(x, y, w, h - 12, 8)
            + f'<rect x="{cx - 9}" y="{y + h - 14}" width="18" height="8" fill="#c4bde4"/>'
            + f'<rect x="{cx - 25}" y="{y + h - 7}" width="50" height="7" rx="3.5" fill="#b7b0da"/>')


def laptop(cx, cy, w=82, h=46):
    x, y = cx - w / 2, cy - h / 2
    return (_plate(x + 8, y, w - 16, h - 13, 7)
            + f'<path d="M{x} {y + h - 10}h{w}l-8 10h-{w - 16}z" fill="#ddd7f2" stroke="#b9b2dd" stroke-width="1.4"/>')


def printer(cx, cy, w=70, h=48):
    x, y = cx - w / 2, cy - h / 2
    return (f'<rect x="{x + 14}" y="{y}" width="{w - 28}" height="12" rx="3" fill="#ece7f8" '
            f'stroke="#b9b2dd" stroke-width="1.4"/>'
            + _plate(x, y + 11, w, h - 24, 8)
            + f'<rect x="{x + 14}" y="{y + h - 15}" width="{w - 28}" height="15" rx="3" fill="#fff" '
              f'stroke="#b9b2dd" stroke-width="1.4"/>')


def phone(cx, cy, w=60, h=46):
    x, y = cx - w / 2, cy - h / 2
    return (_plate(x, y + 13, w, h - 13, 8)
            + f'<path d="M{x + 7} {y + 13}q{w / 2 - 7} -19 {w - 14} 0" stroke="#b7b0da" stroke-width="5" '
              f'fill="none" stroke-linecap="round"/>'
            + f'<rect x="{x + 11}" y="{y + 21}" width="{w - 22}" height="11" rx="3" fill="#ddd7f2"/>')


def server(cx, cy, w=58, h=82):
    x, y = cx - w / 2, cy - h / 2
    g = [_plate(x, y, w, h, 10)]
    for i in range(4):
        g.append(f'<rect x="{x + 10}" y="{y + 11 + i * 17}" width="{w - 22}" height="9" rx="3" fill="#ddd7f2"/>')
        g.append(f'<circle cx="{x + w - 14}" cy="{y + 15.5 + i * 17}" r="2.6" fill="{BLUE}"/>')
    return "".join(g)


def modem(cx, cy, w=100, h=36):
    x, y = cx - w / 2, cy - h / 2
    return (_plate(x, y, w, h, 11)
            + f'<path d="M{x + 18} {cy}q10 -10 21 0t21 0t21 0" stroke="{BLUE}" stroke-width="2.8" fill="none" '
              f'stroke-linecap="round"/>')


def cloud(cx, cy, label, rx=118, ry=50):
    return ("".join([
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#gCloud)" stroke="#b9b2dd" '
        f'stroke-width="1.6" filter="url(#soft)"/>',
        f'<ellipse cx="{cx - rx * .42}" cy="{cy - ry * .32}" rx="{rx * .42}" ry="{ry * .60}" fill="url(#gCloud)"/>',
        f'<ellipse cx="{cx + rx * .40}" cy="{cy - ry * .26}" rx="{rx * .38}" ry="{ry * .54}" fill="url(#gCloud)"/>',
        _cap(cx, cy + 8, label, 24, INK, 700)]))


def wifi(cx, cy):
    return "".join(
        f'<path d="M{cx - r} {cy}a{r} {r} 0 0 1 {2 * r} 0" stroke="{BLUE}" stroke-width="2.6" fill="none" '
        f'opacity="{0.9 - i * 0.22:.2f}"/>' for i, r in enumerate((14, 24, 34)))


def link(d, step, dash=False, col=LINE, w=2.8):
    da = ' stroke-dasharray="10 8"' if dash else ""
    return (f'<path class="dr" data-s="{step}" pathLength="1" d="{d}" stroke="{col}" stroke-width="{w}" '
            f'fill="none" stroke-linecap="round" stroke-linejoin="round"{da}/>')


def node(cx, cy, glyph, label, step, dy=None, sub=None):
    """Устройство с подписью под ним."""
    dy = dy if dy is not None else 42
    g = [f'<g data-s="{step}">', glyph, _cap(cx, cy + dy, label, CAP, DIM, 500)]
    if sub:
        g.append(_cap(cx, cy + dy + 26, sub, CAP, DIM, 400))
    g.append("</g>")
    return "".join(g)


def panel(x, y, w, h, title, step):
    return (f'<g data-s="{step}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="rgba(255,255,255,.58)" '
            f'stroke="#c3bde3" stroke-width="1.6"/>'
            f'{_cap(x + w / 2, y + 44, title, 27, INK, 700)}</g>')


def p027():
    o = ['<h1 class="t ab" style="left:90px;top:34px;text-align:left;width:1400px">Схема сети</h1>',
         '<div class="sub ab" style="left:94px;top:116px;text-align:left;font-size:24px">'
         'Интернет и три офиса компании</div>']

    s = ['<svg class="ab" style="left:0;top:0;width:1920px;height:1240px;overflow:visible" '
         'viewBox="0 0 1920 1240">',
         '<defs>'
         '<linearGradient id="gDev" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ebe6fa"/></linearGradient>'
         '<linearGradient id="gCloud" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e6effc"/></linearGradient>'
         '<filter id="soft" x="-40%" y="-40%" width="180%" height="180%">'
         '<feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#6f68aa" flood-opacity=".22"/>'
         '</filter></defs>']

    # ---------------- верхняя полоса
    s.append(f'<g data-s="1">{cloud(360, 232, "Интернет")}</g>')
    s.append(node(720, 232, router(720, 232), "Маршрутизатор", 1, 48, "интернет-провайдера"))
    s.append(f'<g data-s="1">{cloud(1200, 232, "Сеть компании", 134)}</g>')
    s.append(node(1600, 232, router(1600, 232), "Маршрутизатор", 1, 48, "закрытой и резервной сети"))
    s.append(link("M478 232H661", 1))
    s.append(link("M779 232H1066", 1))
    s.append(link("M1334 232H1541", 1))

    # ---------------- магистрали вниз: провайдер (сплошная) и резерв (штрих)
    PR, RS = 386, 416     # две горизонтальные полосы
    s.append(link(f"M720 257V{PR}", 5))
    s.append(link(f"M130 {PR}H1560 M130 {PR}V560H261 M780 {PR}V560H931 M1310 {PR}V580H1450", 5))
    s.append(link(f"M1600 257V{RS}", 6, dash=True, col=PINK))
    s.append(link(f"M165 {RS}H1600 M165 {RS}V600H261 M815 {RS}V600H931", 6, dash=True, col=PINK))
    s.append(_cap(1700, PR + 6, "провайдер", CAP, LINE, 700, "start"))
    s.append(_cap(1700, RS + 8, "резервная сеть", CAP, PINK, 700, "start"))

    # ---------------- панели офисов
    s.append(panel(90, 470, 620, 690, "Сеть «Центральный офис»", 2))
    s.append(panel(740, 470, 500, 690, "Сеть «Филиал»", 3))
    s.append(panel(1270, 470, 560, 690, "Сеть «Домашний офис»", 4))

    # ---------------- центральный офис
    s.append(node(320, 560, router(320, 560), "Маршрутизатор", 2))
    s.append(node(560, 566, server(560, 566), "Сервер", 2, 60))
    s.append(node(250, 720, switch(250, 720), "Коммутатор L3", 2))
    s.append(node(520, 720, switch(520, 720), "Коммутатор L3", 2))
    s.append(node(230, 880, switch(230, 880), "Коммутатор L2", 2))
    s.append(node(540, 880, switch(540, 880), "Коммутатор L2", 2))
    s.append(link("M320 585V660 M320 660H250V699 M320 660H520V699", 2))
    s.append(link("M560 607V660H520", 2))
    s.append(link("M250 741V820H230V859 M520 741V820H540V859", 2))
    s.append(link("M250 741V822H540V859", 2, dash=True, col=PINK))
    s.append(link("M520 741V822H230V859", 2, dash=True, col=PINK))
    for cx, fn, lb in ((175, pc, "ПК"), (315, printer, "Принтер"),
                       (455, phone, "Телефон"), (610, pc, "ПК")):
        s.append(node(cx, 1040, fn(cx, 1040), lb, 2, 46))
    s.append(link("M230 901V990H175V1017 M230 990H315V1017 M540 901V990H455V1017 M540 990H610V1017", 2))

    # ---------------- филиал
    s.append(node(990, 560, router(990, 560), "Маршрутизатор", 3))
    s.append(node(990, 730, switch(990, 730), "Коммутатор L2", 3))
    s.append(link("M990 585V709", 3))
    for cx, fn, lb, dy in ((820, server, "Сервер", 60), (915, pc, "ПК", 46),
                           (1050, printer, "Принтер", 46), (1165, phone, "Телефон", 46)):
        s.append(node(cx, 1040, fn(cx, 1040), lb, 3, dy))
    s.append(link("M990 751V980H820V999 M990 980H915V1017 M990 980H1050V1017 M990 980H1165V1017", 3))

    # ---------------- домашний офис
    s.append(node(1500, 580, modem(1500, 580), "Модем", 4, 40))
    s.append(node(1500, 730, router(1500, 730), "Маршрутизатор", 4))
    s.append(link("M1500 598V705", 4))
    
    s.append(node(1370, 1040, pc(1370, 1040), "ПК", 4, 46))
    s.append(node(1520, 1040, printer(1520, 1040), "Принтер", 4, 46))
    s.append(node(1720, 1040, laptop(1720, 1040), "Ноутбук", 4, 46))
    s.append(link("M1500 755V980H1370V1017 M1500 980H1520V1017", 4))
    s.append(f'<g data-s="4">{wifi(1720, 975)}</g>')
    s.append(link("M1559 730H1720V940", 4, dash=True, col=BLUE))
    s.append("</svg>")
    o.append("".join(s))

    o.append('<div class="note ab" data-s="7" style="left:90px;top:1200px;width:1740px;font-size:22px">'
             '<span style="color:var(--blue);font-weight:700">Резервирование.</span>&nbsp;'
             'Коммутаторы 2-го уровня подключены к коммутаторам 3-го уровня дополнительными связями, '
             'а маршрутизаторы центрального офиса и филиала имеют по два подключения: к маршрутизатору '
             'интернет-провайдера и к маршрутизатору закрытой резервной сети компании.</div>')
    return "".join(o)


SLIDES.append(("p027", "Схема сети: интернет и три офиса", p027()))
