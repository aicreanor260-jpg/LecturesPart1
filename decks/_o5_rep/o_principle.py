# -*- coding: utf-8 -*-
"""Принцип работы протокола link state — 7 этапов + схема областей + настройка OSPF."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import puck, line, cross, svg, blob, chip
from _o5_g1kit import g1icon, g1ico_svg, g1cyl, g1t, G1FADE

W, H, TOP = 1672, 941, 108

CSS = """<style>
.opn-sub{position:absolute;left:64px;top:112px;font:700 34px/1.1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.9);transform-origin:0 0}
.opn-row{position:absolute;left:22px;width:786px;border-radius:26px;border:2px solid rgba(255,255,255,.9)}
.opn-h{position:absolute;left:122px;font:700 22.5px/1.2 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.9);transform-origin:0 0}
.opn-t{position:absolute;left:518px;font:500 14.4px/1.3 "Golos Text",sans-serif;color:#2b2540;white-space:nowrap}
.opn-ar{position:absolute;left:396px;font:900 20px/1 "Golos Text",sans-serif;color:#ff7fb0}
.opn-box{position:absolute;background:rgba(255,255,255,.95);border-radius:22px;box-shadow:0 4px 14px rgba(180,150,200,.18)}
.opn-lg{position:absolute;font:500 13.5px/1.2 "Golos Text",sans-serif;color:#2b2540;white-space:nowrap}
.opn-bub{position:absolute;left:1336px;top:118px;width:236px;padding:10px 14px;background:#ffd6e6;border-radius:18px;
  font:600 19px/1.2 "Comic Sans MS","Golos Text",sans-serif;color:#1f1a33;text-align:center;transform:rotate(-8deg)}
.opn-cfg{position:absolute;left:830px;top:672px;width:815px;height:180px;background:#feedf6;border-radius:24px}
.opn-ch{position:absolute;left:866px;top:695px;font:700 38px/1 Oswald,sans-serif;color:#1f1a33;transform:scaleX(.88);transform-origin:0 0;white-space:nowrap}
.opn-ct{position:absolute;left:866px;top:752px;font:500 14.8px/1.25 "Golos Text",sans-serif;color:#2b2540;white-space:nowrap}
.opn-foot{position:absolute;left:22px;top:858px;width:910px;height:60px;background:rgba(222,238,252,.95);border-radius:30px;
  font:500 17px/60px "Golos Text",sans-serif;color:#1f1a33;padding-left:86px;white-space:nowrap}
</style>"""

ROWS = [
    (162, "#ffe1ee", "Сбор данных", "Каждый маршрутизатор собирает<br>информацию о состоянии своих<br>интерфейсов (каналов)."),
    (255, "#dcecfb", "Обнаружение соседей", "Маршрутизаторы обнаруживают<br>соседей на непосредственно<br>подключенных каналах."),
    (348, "#fff4cf", "Создание пакета<br>состояния канала (LSP)", "Формируется пакет состояния<br>канала (LSP) с информацией<br>о своих интерфейсах и соседях."),
    (443, "#ffe1ee", "Лавинная рассылка LSP", "LSP распространяется (лавинная<br>рассылка) по всей области OSPF<br>ко всем маршрутизаторам."),
    (542, "#dcecfb", "Создание базы данных LSDB", "Каждый маршрутизатор формирует<br>одинаковую базу данных состояния<br>каналов (LSDB) на основе полученных LSP."),
    (640, "#fff4cf", "Расчёт дерева кратчайших<br>путей SPF по алгоритму Дейкстры", "На основе LSDB выполняется расчёт<br>дерева кратчайших путей SPF<br>по алгоритму Дейкстры."),
    (742, "#ffe1ee", "Добавление маршрутов<br>в таблицу маршрутизации", "По результатам SPF наиболее<br>оптимальные маршруты добавляются<br>в таблицу маршрутизации."),
]

NC = ["#ff8fbf", "#6fb3f0", "#ffd23a"]


def num(i, y):
    return ('<div class="ab" style="left:34px;top:%dpx;width:70px;height:70px;border-radius:50%%;background:%s;'
            'box-shadow:inset 0 -5px 0 rgba(0,0,0,.08);font:900 34px/70px Oswald,sans-serif;color:#1f1a33;text-align:center">%d.</div>'
            % (y + 8, NC[i % 3], i + 1))


def wifi(x, y, col="#3f86d8"):
    return "".join('<path d="M%.1f %.1f a%d %d 0 0 1 %d 0" fill="none" style="stroke:%s" stroke-width="3.5" stroke-linecap="round"/>'
                   % (x - r, y, r, r, 2 * r, col) for r in (7, 14, 21))


def doc(x, y, w=46, h=58, lsp=False):
    s = ('<path d="M%.1f %.1f h%.1f l12 12 v%.1f h-%.1f z" style="fill:#fff;stroke:#1f1a33" stroke-width="3" stroke-linejoin="round"/>'
         % (x, y, w - 12, h - 12, w))
    if lsp:
        s += g1t(x + w / 2, y + 26, "LSP", 15, "#1f1a33", weight=900)
        ys = (38, 47)
    else:
        ys = (16, 27, 38, 49)
    return s + "".join('<path d="M%.1f %.1f h%.1f" style="stroke:#1f1a33" stroke-width="3" stroke-linecap="round"/>'
                       % (x + 9, y + k, w - 18) for k in ys)


RICO = [
    lambda c: doc(380, c - 30) + puck(470, c - 6, 66, "p"),
    lambda c: puck(400, c - 4, 62, "b") + puck(470, c - 4, 62, "b") + wifi(435, c - 18),
    lambda c: doc(415, c - 32, 52, 64, True),
    lambda c: puck(450, c - 6, 74, "p") + "".join(line((450 + dx * 22, c - 6 + dy * 14), (450 + dx * 52, c - 6 + dy * 34), "#1f1a33", 3.5, mk="ak")
                                                for dx, dy in ((0, -1), (-1, 0), (1, 0))),
    lambda c: g1cyl(425, c - 36, 56, 72, "#cfe6fb", "#2b4c7e", "#6fb3f0"),
    lambda c: (line((487, c - 22), (470, c + 18), "#1f1a33", 3.5) + line((487, c - 22), (504, c + 18), "#1f1a33", 3.5)
               + '<circle cx="487" cy="%.1f" r="11" style="fill:#ff8fbf;stroke:#1f1a33" stroke-width="3"/>' % (c - 22)
               + '<circle cx="470" cy="%.1f" r="11" style="fill:#6fb3f0;stroke:#1f1a33" stroke-width="3"/>' % (c + 20)
               + '<circle cx="504" cy="%.1f" r="11" style="fill:#6fb3f0;stroke:#1f1a33" stroke-width="3"/>' % (c + 20)
               + '<path d="M494 %.1f v-26 l16 6 -16 6" style="fill:#ff4f7f;stroke:#1f1a33" stroke-width="2.5"/>' % (c - 30)),
    lambda c: doc(398, c - 32, 50, 62) + g1ico_svg("arrow", 470, c + 12, 40, "#ff8fbf"),
]
NET = {"a1": (853, 333), "a2": (980, 268), "a3": (1080, 340), "a4": (967, 425), "b1": (1200, 287), "b2": (1213, 412),
       "c1": (1327, 333), "c2": (1460, 268), "c3": (1580, 333), "c4": (1467, 427)}
BL, PK = "#2f6fe8", "#ff4f9a"


def dbl(a, b, col, off=(0, 0), k=.62):
    (x1, y1), (x2, y2) = NET[a], NET[b]
    mx, my, dx, dy = (x1 + x2) / 2 + off[0], (y1 + y2) / 2 + off[1], (x2 - x1) * k / 2, (y2 - y1) * k / 2
    return '<path d="M%.1f %.1f L%.1f %.1f" style="stroke:%s" stroke-width="3.5" marker-start="url(#opnM%s)" marker-end="url(#opnM%s)"/>' % (
        mx - dx * .5, my - dy * .5, mx + dx * .5, my + dy * .5, col, col[1:], col[1:])


def net():
    o = ['<defs>' + "".join('<marker id="opnM%s" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5" orient="auto-start-reverse">'
                             '<path d="M0,0 L7,3.5 L0,7z" style="fill:%s"/></marker>' % (c[1:], c) for c in (BL, PK)) + '</defs>',
         blob(970, 345, 165, 140, "y", seed=1), blob(1207, 350, 85, 125, "v", seed=3), blob(1455, 345, 185, 140, "b", seed=2),
         chip(970, 222, "Область 1.1.1.1", "#ffe58a", fs=19), chip(1207, 228, "Область 0.0.0.0", "#ddd2fa", fs=17),
         chip(1470, 222, "Область 2.2.2.2", "#c7e2fb", fs=19)]
    for a, b in [("a1", "a2"), ("a2", "a3"), ("a3", "a4"), ("a4", "a1"), ("a3", "b1"), ("a3", "b2"), ("b1", "c1"),
                 ("b2", "c1"), ("c1", "c2"), ("c2", "c3"), ("c3", "c4"), ("c4", "c1")]:
        o.append(line(NET[a], NET[b], "#111", 3.5))
    o.append(cross(1397, 380, 14, "#e8202a", 6))
    o += [dbl("a1", "a2", BL, (-22, -14)), dbl("a2", "a3", PK, (20, -20)), dbl("a4", "a1", PK, (-22, 16)),
          dbl("a3", "a4", BL, (16, 14)), dbl("a3", "b1", PK, (0, -22)), dbl("b2", "a3", PK, (10, 18)),
          dbl("b1", "c1", PK, (0, -20)), dbl("c1", "c2", PK, (-14, -20)), dbl("c2", "c3", PK, (16, -18)),
          dbl("c3", "c4", BL, (18, 16))]
    for n, (x, y) in NET.items():
        o.append(puck(x, y - 12, 84, "b"))
    return svg("".join(o))


def dst():
    return svg(line((1300, 458), (1440, 530), PK, 4, "12 8", "ap") + puck(1500, 565, 110, "b")
               + '<path d="M1525 560 v-58" style="stroke:#1f1a33" stroke-width="3.5"/>'
               + '<path d="M1525 502 l30 10 -30 10z" style="fill:#ff4f7f"/>')


def row(i, y, c, head, text):
    h = 96 if i == 6 else 86
    two = "<br>" in head
    return ('<div class="step"><div class="opn-row" style="top:%dpx;height:%dpx;background:%s"></div>%s%s'
            '<div class="opn-h" style="top:%dpx">%s</div><div class="opn-t" style="top:%dpx">%s</div>%s</div>'
            % (y, h, c, num(i, y), svg(RICO[i](y + h / 2.0)),
               y + (14 if two else 28), head, y + 12, text,
               '<div class="opn-ar" style="top:%dpx">↓</div>' % (y - 14) if i else ""))


LEG = ('<div class="opn-box" style="left:836px;top:518px;width:520px;height:128px"></div>'
       '<svg class="ab" style="left:850px;top:530px" width="500" height="110" viewBox="0 0 500 110">'
       '<defs><marker id="opnA" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto-start-reverse">'
       '<path d="M0,0 L8,4 L0,8z" fill="#2f6fe8"/></marker><marker id="opnB" markerWidth="8" markerHeight="8" refX="4" refY="4" '
       'orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8z" fill="#ff4f9a"/></marker></defs>'
       '<line x1="6" y1="20" x2="44" y2="20" stroke="#2f6fe8" stroke-width="3" marker-start="url(#opnA)" marker-end="url(#opnA)"/>'
       '<line x1="6" y1="78" x2="44" y2="78" stroke="#ff4f9a" stroke-width="3" marker-start="url(#opnB)" marker-end="url(#opnB)"/>'
       '<line x1="248" y1="14" x2="300" y2="14" stroke="#111" stroke-width="3"/>'
       '<path d="M266 38 l16 16 M282 38 l-16 16" stroke="#e8202a" stroke-width="4"/>'
       '<line x1="248" y1="88" x2="296" y2="88" stroke="#ff4f9a" stroke-width="3" stroke-dasharray="9 6"/>'
       '<path d="M296 82 l9 6 l-9 6z" fill="#ff4f9a"/></svg>'
       '<div class="opn-lg" style="left:910px;top:536px">Соседство<br>между маршрутизаторами</div>'
       '<div class="opn-lg" style="left:910px;top:592px">Обмен LSP<br>(состояние каналов)</div>'
       '<div class="opn-lg" style="left:1166px;top:536px">Физический канал</div>'
       '<div class="opn-lg" style="left:1166px;top:568px">Неисправный канал</div>'
       '<div class="opn-lg" style="left:1166px;top:599px">Дерево кратчайших путей SPF<br>к выбранному назначению</div>')

HTML = CSS + bg("bg3", W, H) + "".join(
    ['<div class="opn-sub">Алгоритм SPF Эдсгера Дейкстры</div>']
    + [row(i, *r) for i, r in enumerate(ROWS)]
    + ['<div class="step">' + net()
       + '<div class="opn-bub">Все маршрутизаторы имеют одинаковую карту сети! ♥</div></div>',
       '<div class="step">' + LEG + dst() + '<div class="opn-bub" style="left:1500px;top:445px;width:150px;padding:6px 8px;font-size:16px;transform:rotate(-6deg)">SPF:<br>лучший путь<br>к назначению ♥</div>' + '</div>',
       '<div class="step"><div class="opn-cfg"></div>' + img("o_principle_girl2.png", "left:1240px;top:640px;width:430px;" + G1FADE)
       + '<div class="opn-ch">Настройка OSPF</div><div class="opn-ct">Процесс создают глобально, затем привязывают по номеру<br>'
       'к интерфейсу или туннелю. OSPF активируется на выбранном<br>интерфейсе. Туннель используют в DMVPN. В RIP глобальная<br>'
       'настройка применяется ко всем интерфейсам.</div></div>',
       '<div class="step"><div class="opn-foot"><b>Канал</b> — интерфейс маршрутизатора &nbsp;&nbsp;•&nbsp;&nbsp; '
       '<b>Состояние канала</b> — сведения о связи между интерфейсами</div>'
       + g1icon("bulb", 34, 866, 52, "b") + '</div>'])
