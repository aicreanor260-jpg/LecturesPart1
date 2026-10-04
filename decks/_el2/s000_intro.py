# -*- coding: utf-8 -*-
"""Титул и цели лекции — в стилистике курса (как в остальных деках)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from _el2_lib import ico

SLIDES = []


def ab(l, t, w=None, extra=""):
    s = f"position:absolute;left:{l}px;top:{t}px;"
    if w: s += f"width:{w}px;"
    return s + extra


# ======================================================= титул
def title():
    o = [f'<div class="ab" style="{ab(1020, 120, 820)}height:860px;opacity:.97">'
         + "".join(f'<img src="assets/dev/{n}" style="position:absolute;left:{l}px;top:{t}px;width:{w}px;'
                   f'filter:drop-shadow(0 26px 46px rgba(30,60,130,.22))">'
                   for n, l, t, w in [("esr-3300.webp", -40, 40, 760), ("mes2424p.webp", 30, 250, 700),
                                      ("mes1428.webp", 110, 450, 640), ("wep-3ax.webp", 430, 600, 230)])
         + '</div>']
    o += ['<div class="ab" style="left:120px;top:250px;width:900px">'
          '<div class="kick" style="font-size:30px;letter-spacing:7px">ОС-2</div>'
          '<h1 class="t left" style="font-size:104px;text-align:left;margin-top:18px;line-height:.96">'
          'Сетевые<br>устройства</h1>'
          '<div style="width:140px;height:6px;border-radius:4px;background:var(--blue);margin:34px 0 30px"></div>'
          '<p class="b" style="font-size:28px;max-width:720px;color:var(--dim)">'
          'Методы доступа и подключения, модельный ряд маршрутизаторов, коммутаторов и беспроводных устройств, '
          'режимы и команды операционной системы</p>'
          '<p class="b" style="font-size:24px;margin-top:40px;color:var(--navy);font-weight:600">'
          'Ананко Софья Михайловна<br>Качур Анна Юрьевна</p></div>']
    return "".join(o)


SLIDES.append(("p000a", "Титул", title()))


# ======================================================= цели лекции
def goals():
    items = [("net", "Протоколы и устройства", "Методы доступа и подключения сетевых устройств к компьютерной сети"),
             ("router", "Модельный ряд", "Маршрутизаторы ESR, коммутаторы MES и беспроводные устройства Eltex"),
             ("term", "Операционная система", "Иерархия режимов командной строки и структура команд"),
             ("reload", "Загрузка и настройка", "Процедура загрузки устройства, файлы конфигурации и базовая настройка")]
    o = ['<h1 class="t ab ctr-x" style="top:90px;width:1500px">Цель лекции</h1>',
         '<p class="b ab ctr-x" style="top:186px;width:1100px;text-align:center;font-size:26px;color:var(--dim)">'
         'В данной лекции будет рассмотрено</p>']
    for i, (icn, t, d) in enumerate(items):
        l = 120 + (i % 2) * 860
        top = 300 + (i // 2) * 320
        o.append(f'<div class="card" data-s="{i + 1}" style="{ab(l, top, 800)}height:260px;padding:34px 38px">'
                 f'<div style="display:flex;gap:24px;align-items:center">'
                 f'<span class="mono" style="font-size:46px;font-weight:700;color:#b9cdf0">0{i + 1}</span>'
                 f'{ico(icn)}'
                 f'<div style="font-size:30px;font-weight:700;color:var(--navy);text-transform:uppercase;'
                 f'line-height:1.1">{t}</div></div>'
                 f'<p class="b" style="margin-top:22px;font-size:24px">{d}</p></div>')
    return "".join(o)


SLIDES.append(("p000b", "Цель лекции", goals()))
