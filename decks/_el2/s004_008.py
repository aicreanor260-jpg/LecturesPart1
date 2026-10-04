# -*- coding: utf-8 -*-
"""Слайды по референсам p004, p005, p007, p008."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from _el2_lib import ico, arrow_svg

SLIDES = []


def ab(l, t, w=None, extra=""):
    s = f"position:absolute;left:{l}px;top:{t}px;"
    if w: s += f"width:{w}px;"
    return s + extra


def layer(*parts):
    return ('<svg class="ab" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" '
            'viewBox="0 0 1920 1080">' + "".join(parts) + '</svg>')


# ======================================================= стекирование (p004)
def stacking():
    o = ['<h1 class="t ab ctr-x" style="top:24px;width:1700px">Стекирование и производительность коммутаторов</h1>']

    feats = [("stack", "До 8 физических устройств"), ("switch", "1 логический коммутатор"),
             ("gear", "Общее управление и больше портов")]
    o.append(f'<div class="card" data-s="1" style="{ab(70, 110, 880)}height:300px">'
             '<div class="ch">Как работает стек</div>'
             '<img class="cut ab" src="assets/p004_stack.jpg" style="left:28px;top:78px;width:470px">'
             + "".join(f'<div class="ab" style="left:540px;top:{86 + i * 72}px;width:320px;display:flex;gap:14px;'
                       f'align-items:center">{ico(icn, "sm")}<p class="b sm">{t}</p></div>'
                       for i, (icn, t) in enumerate(feats)) + '</div>')

    o.append(f'<div class="card" data-s="2" style="{ab(980, 110, 870)}height:300px">'
             '<div class="ch nb" style="color:var(--navy)">Uplink-интерфейс</div>'
             '<p class="b sm">Высокоскоростной интерфейс для подключения к вышестоящему коммутатору или маршрутизатору.</p>'
             '<p class="b sm" style="margin-top:8px">Благодаря SFP-модулям может использовать разные типы соединений.</p>'
             '<div style="display:flex;gap:12px;margin-top:12px">'
             + "".join(f'<span class="chip" style="font-size:18px;padding:6px 14px">{c}</span>'
                       for c in ["E1", "10 Gigabit Ethernet", "оптоволокно"]) + '</div>'
             '<div style="display:flex;gap:46px;margin-top:16px">'
             f'<div style="display:flex;gap:14px;align-items:center">{ico("link", "sm")}'
             '<div><div class="b sm dim">Ethernet-порт:</div>'
             '<div class="mono" style="font-size:26px;font-weight:700;color:var(--navy)">100 Мбит/с</div></div></div>'
             f'<div style="display:flex;gap:14px;align-items:center">{ico("bolt", "sm")}'
             '<div><div class="b sm dim">Uplink:</div>'
             '<div class="mono" style="font-size:26px;font-weight:700;color:var(--blue)">1 Гбит/с</div></div></div>'
             '</div></div>')

    def variant(l, title, img, img_style, items, s):
        return (f'<div class="card" data-s="{s}" style="{ab(l, 440, 560)}height:440px">'
                f'<div class="ch sm">{title}</div>'
                f'<img class="cut ab" src="assets/{img}" style="{img_style}">'
                + "".join(f'<div class="ab" style="left:28px;top:{240 + i * 48}px;width:500px;display:flex;gap:12px;'
                          f'align-items:center">{ico(icn, "sm")}<p class="b sm">{t}</p></div>'
                          for i, (icn, t) in enumerate(items)) + '</div>')

    o.append(variant(70, "Стек: 2 × 24 порта", "p004_two.jpg", "left:26px;top:76px;width:500px",
                     [("server", "2 × 1 RU = 2 RU"), ("power", "2 розетки 220 В"),
                      ("link", "48 абонентских портов"), ("chart", "48 × 100 Мбит/с = 4,8 Гбит/с")], 3))
    o.append(variant(1290, "Один коммутатор: 48 портов", "p004_one.jpg", "left:60px;top:86px;width:440px",
                     [("server", "1 RU"), ("power", "1 розетка 220 В"),
                      ("link", "48 абонентских портов"), ("chart", "48 × 100 Мбит/с = 4,8 Гбит/с")], 5))

    rows = [("Место в стойке", "2 RU", "1 RU", True), ("Питание", "2 розетки", "1 розетка", True),
            ("Порты", "48", "48", False), ("Пропускная способность портов", "4,8 Гбит/с", "4,8 Гбит/с", False),
            ("Стоимость", "300", "250", False), ("Цена порта", "6,25", "5,21", True)]
    tr = "".join(f'<tr><td>{a}</td><td style="text-align:center">{b}</td>'
                 f'<td style="text-align:center" class="{"hl" if hl else ""}">{c}</td></tr>' for a, b, c, hl in rows)
    o.append(f'<div class="card" data-s="4" style="{ab(660, 440, 600)}height:440px">'
             '<div class="ch sm nb" style="justify-content:center">Сравнение параметров</div>'
             '<table class="tbl" style="font-size:18px"><thead><tr><th>Показатель</th>'
             '<th class="b2" style="text-align:center">Стек 2 × 24</th>'
             '<th class="b3" style="text-align:center">Один × 48</th></tr></thead>'
             f'<tbody>{tr}</tbody></table>'
             '<div style="display:flex;gap:12px;align-items:center;margin-top:14px">'
             '<span style="width:34px;height:20px;border-radius:6px;background:#d8f3e6;display:block"></span>'
             '<span class="b sm dim">Лучший результат по данному показателю</span></div></div>')

    o.append(f'<div class="card" data-s="6" style="{ab(70, 910, 1780)}height:140px;padding:22px 30px">'
             '<div style="display:flex;gap:46px;align-items:center">'
             '<div style="font-size:30px;font-weight:800;color:var(--navy);text-transform:uppercase;width:270px">'
             'Две разные скорости</div>'
             f'<div style="display:flex;gap:16px;align-items:center;flex:1">{ico("speed", "sm")}'
             '<div><div style="font-size:21px;font-weight:800;color:var(--navy);text-transform:uppercase">Скорость пересылки</div>'
             '<p class="b sm dim">Производительность всего коммутатора: объём данных, обрабатываемых за секунду.</p></div></div>'
             f'<div style="display:flex;gap:16px;align-items:center;flex:1">{ico("snow", "sm")}'
             '<div><div style="font-size:21px;font-weight:800;color:var(--navy);text-transform:uppercase">Скорость порта</div>'
             '<p class="b sm dim">Скорость передачи данных каждого Ethernet-порта: 100 Мбит/с, 1, 10 или 100 Гбит/с.</p></div></div>'
             '</div></div>')
    return "".join(o)


SLIDES.append(("p004", "Стекирование и производительность коммутаторов", stacking()))


# ======================================================= ESR-200 задняя панель (p005)
def esr200_back():
    o = ['<div class="ab" style="left:96px;top:56px"><div class="big">ESR-200</div>'
         '<div class="kick" style="margin-top:6px">Задняя панель</div></div>',
         f'<img class="cut ab" src="assets/esr200_back.jpg" style="{ab(190, 330, 1540)}">']

    def call(l, n, title, txt, icn, s):
        return (f'<div class="card" data-s="{s}" style="{ab(l, 700, 520)}display:flex;gap:18px;align-items:flex-start">'
                f'<span class="badge">{n}</span><div style="flex:1">'
                f'<div style="font-size:25px;font-weight:800;color:var(--navy);text-transform:uppercase;line-height:1.2">{title}</div>'
                f'<div style="display:flex;gap:16px;align-items:center;margin-top:14px">{ico(icn, "sm")}'
                f'<p class="b sm dim">{txt}</p></div></div></div>')

    o += [call(170, 1, "Клемма для заземления устройства",
               "Используется для подключения маршрутизатора к контуру заземления.", "ground", 1),
          call(950, 2, "Вентиляционный модуль",
               "Обеспечивает эффективное охлаждение устройства и стабильную работу системы.", "fan", 2)]
    o.append(layer(
        '<path class="dr" data-s="1" pathLength="1" d="M250 560 L250 640 L430 640 L430 700" stroke="var(--blue)" stroke-width="4" fill="none"/>',
        '<path class="dr" data-s="2" pathLength="1" d="M1060 560 L1060 640 L1210 640 L1210 700" stroke="var(--blue)" stroke-width="4" fill="none"/>',
        '<path class="dr" data-s="2" pathLength="1" d="M1270 560 L1270 640 L1210 640" stroke="var(--blue)" stroke-width="4" fill="none"/>'))
    return "".join(o)


SLIDES.append(("p005", "ESR-200: задняя панель", esr200_back()))


# ======================================================= MES2424P задняя панель (p007)
def mes2424p_back():
    o = ['<div class="ab" style="left:96px;top:56px"><div class="big">MES2424P</div>'
         '<div class="kick" style="margin-top:6px">Задняя панель</div></div>',
         f'<img class="cut ab" src="assets/p007_mes2424p_back.jpg" style="{ab(200, 320, 1520)}">']

    def call(l, n, title, txt, icn, s):
        return (f'<div class="card" data-s="{s}" style="{ab(l, 700, 500)}display:flex;gap:18px;align-items:flex-start">'
                f'<span class="badge">{n}</span><div style="flex:1">'
                f'<div style="font-size:25px;font-weight:800;color:var(--navy);text-transform:uppercase">{title}</div>'
                f'<div style="display:flex;gap:16px;align-items:center;margin-top:14px">{ico(icn, "sm")}'
                f'<p class="b sm dim">{txt}</p></div></div></div>')

    o += [call(600, 1, "Вентиляторы", "Охлаждение устройства", "fan", 1),
          call(1180, 2, "Клемма заземления", "Клемма для заземления устройства", "ground", 2)]
    o.append(layer(
        '<path class="dr" data-s="1" pathLength="1" d="M760 540 L760 640 L850 640 L850 700" stroke="var(--blue)" stroke-width="4" fill="none"/>',
        '<path class="dr" data-s="1" pathLength="1" d="M1060 540 L1060 640 L850 640" stroke="var(--blue)" stroke-width="4" fill="none"/>',
        '<path class="dr" data-s="2" pathLength="1" d="M1620 560 L1620 640 L1430 640 L1430 700" stroke="var(--blue)" stroke-width="4" fill="none"/>'))
    return "".join(o)


SLIDES.append(("p007", "MES2424P: задняя панель", mes2424p_back()))


# ======================================================= коммутаторы ЦОД (p008)
def dc_switches():
    o = ['<h1 class="t ab ctr-x" style="top:24px;width:1700px">Коммутаторы центра обработки данных</h1>',
         '<div class="sub ab ctr-x" style="top:102px">ЦОД</div>']

    tags = [("speed", "1G · 10G · 40G · 100G"), ("server", "Top-of-rack"), ("stack", "End-of-row"),
            ("gear", "Неблокируемая матрица"), ("cloud", "EVPN / VXLAN"), ("clock", "Минимальная задержка")]
    for i, (icn, t) in enumerate(tags):
        o.append(f'<div class="ab" data-s="1" style="left:{95 + i * 292}px;top:158px;width:270px;text-align:center;'
                 f'--dl:{i * 70}ms">'
                 f'<div style="display:flex;justify-content:center">{ico(icn, "sm")}</div>'
                 f'<div style="margin-top:10px;font-size:18px;font-weight:700;color:var(--navy);text-transform:uppercase;'
                 f'line-height:1.25">{t}</div></div>')

    for i, (img, name) in enumerate([("p008_sw1.jpg", "MES5600-24"), ("p008_sw2.jpg", "MES5400-24"),
                                     ("p008_sw3.jpg", "MES5410-48")]):
        o.append(f'<div class="card" data-s="{2 + i}" style="{ab(70 + i * 600, 320, 560)}height:230px;padding:18px">'
                 f'<img class="cut" src="assets/{img}" style="width:100%">'
                 f'<div class="mono ab" style="left:0;right:0;bottom:16px;text-align:center;font-size:27px;'
                 f'font-weight:800;color:var(--navy)">{name}</div></div>')

    o.append(f'<img class="ph ab" data-s="5" src="assets/p008_racks.jpg" style="{ab(70, 590, 1150)}">')
    for i, (icn, t) in enumerate([("arrows", "Front-to-back"), ("shield", "Резервирование питания"),
                                  ("gear", "Горячая замена"), ("chart", "Мониторинг оборудования")]):
        o.append(f'<div class="card" data-s="6" style="{ab(1270 + (i % 2) * 300, 630 + (i // 2) * 170, 280)}'
                 f'height:150px;padding:16px;text-align:center;--dl:{i * 80}ms">'
                 f'<div style="display:flex;justify-content:center">{ico(icn, "sm")}</div>'
                 f'<div style="margin-top:10px;font-size:18px;font-weight:700;color:var(--navy);text-transform:uppercase;'
                 f'line-height:1.25">{t}</div></div>')
    return "".join(o)


SLIDES.append(("p008", "Коммутаторы центра обработки данных", dc_switches()))
