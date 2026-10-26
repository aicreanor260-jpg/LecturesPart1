# -*- coding: utf-8 -*-
"""Алгоритм Дейкстры — шаг 1 из R1: обновление меток, таблица статусов."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.odu-sub{position:absolute;left:52px;top:150px;font:600 30px/1.15 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap;z-index:5}
.odu-box{position:absolute;background:rgba(255,255,255,.97);border:2px solid #f1e6ee;border-radius:24px}
.odu-pill{position:absolute;background:#ffc6dd;border-radius:14px;font:800 27px/1 "Golos Text",sans-serif;color:#1f1a33;padding:10px 20px}
.odu-k{position:absolute;left:52px;width:44px;height:44px;border-radius:50%;background:#ffd6e6;display:flex;align-items:center;
  justify-content:center;font:800 22px/1 "Golos Text",sans-serif;color:#1f1a33}
.odu-t{position:absolute;left:128px;font:500 20px/1.25 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odu-t s{text-decoration:none;display:inline-block;background:#ffd6e6;border-radius:8px;padding:2px 10px;margin-right:8px}
.odu-t u{text-decoration:none;display:inline-block;background:#d6eafc;border-radius:8px;padding:2px 8px}
.odu-t q{quotes:none;background:#ffe58a;border-radius:6px;padding:0 5px}
.odu-tb{position:absolute;left:44px;top:650px;border-collapse:separate;border-spacing:4px;font:500 20px/1 "Golos Text",sans-serif;color:#1f1a33}
.odu-tb th{font:700 17px/1 "Golos Text",sans-serif;height:38px;background:#f2f2f6}
.odu-tb td{height:44px;text-align:center;border-radius:8px}
.odu-tb td:first-child{font-weight:800}
.odu-tb td.c{background:#fff;border-bottom:1px solid #eee;font-weight:800;font-size:22px}
.odu-b{position:absolute;display:flex;align-items:center;justify-content:center;font:800 26px/1 "Golos Text",sans-serif;color:#1f1a33;
  background:#fff;border-radius:10px}
.odu-s{position:absolute;padding:6px 16px;border-radius:12px;font:700 20px/1 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
.odu-note{position:absolute;left:1290px;top:146px;width:345px;padding:8px 18px;background:#ffe14d;border-radius:14px;
  font:700 22px/1.15 "Golos Text",sans-serif;color:#1f1a33;transform:rotate(-3deg);box-shadow:3px 4px 0 rgba(0,0,0,.08)}
.odu-rule{position:absolute;left:700px;top:808px;width:770px;height:110px;background:rgba(255,255,255,.97);border-radius:26px}
.odu-rh{position:absolute;left:806px;top:822px;background:#ffe58a;border-radius:10px;padding:5px 14px;font:700 20px/1 "Golos Text",sans-serif;color:#1f1a33}
.odu-rt{position:absolute;left:818px;top:862px;font:500 19.5px/1.25 "Golos Text",sans-serif;color:#1f1a33;white-space:nowrap}
</style>"""


def b(x, y, w, h, t, bc, extra=""):
    return ('<div class="odu-b" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border:3px solid %s;%s">%s</div>'
            % (x, y, w, h, bc, extra, t))


def s(x, y, t, c):
    return '<div class="odu-s" style="left:%dpx;top:%dpx;background:%s">%s</div>' % (x, y, c, t)


def k(n, y, text):
    return ('<div class="odu-k" style="top:%dpx">%d</div><div class="odu-t" style="top:%dpx">%s</div>' % (y, n, y - 6 if "<br>" in text else y + 8, text))


ROWS = [("R1", "#ffd6e6", "0", "посещена", "#ffd6e6"), ("R2", "#ffd6e6", "2", "следующая", "#ffe14d"),
        ("R3", "#d6eafc", "5", "не посещена", "#d6eafc"), ("R4", "#d6eafc", "<span style=\"font-size:34px\">∞</span>", "не посещена", "#d6eafc")]
TABLE = ('<table class="odu-tb"><tr><th style="width:132px">Вершина</th><th style="width:206px">Метка после шага 1</th>'
         '<th style="width:192px">Статус</th></tr>'
         + "".join('<tr><td style="background:%s">%s</td><td class="c">%s</td><td><span class="odu-s" style="position:static;'
                   'display:block;background:%s;font-weight:500;padding:9px 0">%s</span></td></tr>' % (c1, r, m, c2, st)
                   for r, c1, m, st, c2 in ROWS) + '</table>')

HTML = CSS + bg("bg5", W, H) + "".join([
    '<div class="odu-sub">Обновление меток и выбор следующей вершины</div>',
    img("o_dij_update_scene.png", "left:620px;top:200px;width:1038px;border-radius:24px"),
    '<div class="odu-note">Граф без отрицательных весов рёбер <span style="color:#ff4f9a">♥</span></div>',
    '<div class="step"><div class="odu-box" style="left:35px;top:200px;width:565px;height:380px"></div>'
    + img("o_dij_update_n01.png", "left:40px;top:210px;width:85px")
    + '<div class="odu-pill" style="left:128px;top:217px">Шаг 1. Старт из R1</div>'
    + k(1, 280, "Помечаем R1 как корневую вершину.<br>Её метка — <q>0.</q>")
    + k(2, 344, "Рассматриваем всех соседей R1<br>и вычисляем длину пути.") + '</div>',
    '<div class="step">' + k(3, 398, "К R2: &nbsp;<s>0 + 2 = 2.</s> Заменяем метку <b style='font:900 26px/1 Arial;vertical-align:-2px'>∞</b> &nbsp;на &nbsp;<u>2</u>")
    + k(4, 452, "К R3: &nbsp;<s>0 + 5 = 5.</s> Заменяем метку <b style='font:900 26px/1 Arial;vertical-align:-2px'>∞</b> &nbsp;на &nbsp;<u>5</u>")
    + b(1015, 180, 70, 56, "0", "#1f1a33", "background:#ffe14d;font-size:32px") + s(1112, 202, "посещена", "#ffc6dd")
    + b(798, 546, 74, 48, "2", "#ffd84a", "font-size:30px") + b(1322, 546, 74, 48, "5", "#7fb6f0", "font-size:30px") + '</div>',
    '<div class="step">' + k(5, 512, "После проверки всех соседей<br>отмечаем R1 как посещённую.")
    + s(760, 600, "следующая", "#ffc6dd") + s(1284, 600, "не посещена", "#d6eafc")
    + b(1058, 726, 80, 46, "∞", "#ffffff", "font-size:46px") + s(1022, 780, "не посещена", "#d6eafc") + '</div>',
    '<div class="step"><div class="odu-box" style="left:35px;top:592px;width:565px;height:320px"></div>'
    '<div class="odu-pill" style="left:46px;top:602px;width:542px;padding:9px 20px;font-size:26px">Таблица меток и статусов</div>'
    + TABLE + '</div>',
    '<div class="step"><div class="odu-rule"></div>' + img("o_dij_update_gear.png", "left:695px;top:815px;width:105px")
    + '<div class="odu-rh">Правило обновления метки</div><div class="odu-rt">Если новая длина меньше текущей метки соседа —<br>'
    'заменяем метку.</div></div>',
])
