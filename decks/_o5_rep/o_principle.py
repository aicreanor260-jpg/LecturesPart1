# -*- coding: utf-8 -*-
"""Принцип работы протокола link state — 7 этапов + схема областей + настройка OSPF."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 108

CSS = """<style>
.opn-sub{position:absolute;left:64px;top:112px;font:700 34px/1.1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.9);transform-origin:0 0}
.opn-row{position:absolute;left:22px;width:786px;border-radius:26px;border:2px solid rgba(255,255,255,.9)}
.opn-h{position:absolute;left:122px;font:700 22.5px/1.2 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap;transform:scaleX(.9);transform-origin:0 0}
.opn-t{position:absolute;left:518px;font:500 15px/1.3 "Golos Text",sans-serif;color:#2b2540;white-space:nowrap}
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

IX = [365, 370, 412, 385, 428, 436, 415]


def row(i, y, c, head, text):
    h = 96 if i == 6 else 86
    two = "<br>" in head
    return ('<div class="step"><div class="opn-row" style="top:%dpx;height:%dpx;background:%s"></div>%s%s'
            '<div class="opn-h" style="top:%dpx">%s</div><div class="opn-t" style="top:%dpx">%s</div>%s</div>'
            % (y, h, c, img("o_principle_n%d.png" % (i + 1), "left:30px;top:%dpx;width:75px" % (y + 5)),
               img("o_principle_i%d.png" % (i + 1), "left:%dpx;top:%dpx;width:%dpx" % (IX[i], y + 2, 512 - IX[i])),
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
    + ['<div class="step">' + img("o_principle_net.png", "left:820px;top:140px;width:830px")
       + '<div class="opn-bub">Все маршрутизаторы имеют одинаковую карту сети! ♥</div></div>',
       '<div class="step">' + LEG + img("o_principle_dst.png", "left:1365px;top:455px;width:295px") + '</div>',
       '<div class="step"><div class="opn-cfg"></div>' + img("o_principle_girl.png", "left:1320px;top:630px;width:340px")
       + '<div class="opn-ch">Настройка OSPF</div><div class="opn-ct">Процесс создают глобально, затем привязывают по номеру<br>'
       'к интерфейсу или туннелю. OSPF активируется на выбранном<br>интерфейсе. Туннель используют в DMVPN. В RIP глобальная<br>'
       'настройка применяется ко всем интерфейсам.</div></div>',
       '<div class="step"><div class="opn-foot"><b>Канал</b> — интерфейс маршрутизатора &nbsp;&nbsp;•&nbsp;&nbsp; '
       '<b>Состояние канала</b> — сведения о связи между интерфейсами</div>'
       + img("o_principle_bulb.png", "left:25px;top:862px;width:65px") + '</div>'])
