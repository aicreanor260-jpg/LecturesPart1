# -*- coding: utf-8 -*-
"""Создание учётной записи: три атрибута, правила имени, пользователь по умолчанию."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 200

CSS = """<style>
.bus-card{position:absolute;top:450px;height:378px;background:rgba(255,255,255,.95);border:3px solid #2a0a2a;
  box-shadow:9px 9px 0 rgba(255,46,147,.55)}
.bus-rib{position:absolute;top:470px;background:#ff2e93;color:#fff;font:italic 900 34px/1 Rubik,sans-serif;text-transform:uppercase;
  padding:12px 22px;transform:skew(-8deg);box-shadow:5px 5px 0 #2a0a2a;white-space:nowrap;letter-spacing:-.01em}
.bus-row{position:absolute;background:#f3e6f6;border-radius:12px;font:600 22px/1.15 "Golos Text",sans-serif;color:#1a0a1a}
.bus-tx{position:absolute;font:600 22px/1.15 "Golos Text",sans-serif;color:#1a0a1a}
.bus-in{position:absolute;background:#fff;border:2px solid #b9a6c4;border-radius:8px;font:500 24px/40px "Golos Text",sans-serif;
  padding-left:16px;color:#1a0a1a}
.bus-in em{float:right;margin-right:16px;font-style:normal}
.bus-n{position:absolute;width:50px;height:50px;border-radius:50%;background:#ff2e93;color:#fff;font:900 26px/50px Rubik,sans-serif;text-align:center}
.bus-code{position:absolute;left:728px;top:687px;width:300px;height:44px;border:3px solid #3fe6ff;border-radius:6px;background:#fff;
  font:500 25px/44px monospace;text-align:center;color:#1a0a1a;box-shadow:0 0 10px #3fe6ff}
.bus-warn{position:absolute;left:1128px;top:714px;width:510px;height:96px;background:#e4f6fd;border:2px solid #3fe6ff;border-radius:12px}
.bus-foot{position:absolute;left:300px;top:850px;width:1160px;height:66px;background:#eafaff;border:3px solid #2a0a2a;transform:skew(-6deg);
  box-shadow:6px 6px 0 rgba(255,46,147,.5);font:800 30px/60px "Golos Text",sans-serif;color:#1a0a1a;text-align:center;padding-left:60px;box-sizing:border-box}
.bus-blink{animation:busb 1.6s step-end infinite}
@keyframes busb{50%{opacity:.3}}
</style>"""

ATTRS = [(540, "Имя<br>пользователя", ""), (628, "Пароль", "●●●●●●●"), (716, "Уровень<br>привилегии", "<em>▼</em>")]
RULES = [(538, 70, 1, "Латинские буквы, спецсимволы<br>и пробелы"), (618, 126, 2, "Пробел в имени: используйте<br>кавычки"),
         (752, 60, 3, "Admin1 ≠ admin1 — регистр важен")]
DEFLT = [(548, "Имя:", "admin"), (598, "Пароль по умолчанию:", "admin"), (648, "Привилегия:", "15")]


def attrs():
    s = ""
    for y, t, v in ATTRS:
        ty = y + (14 if "<br>" in t else 28)
        s += ('<div class="bus-row" style="left:38px;top:%dpx;width:540px;height:80px"></div>'
              '<div class="bus-tx" style="left:138px;top:%dpx">%s</div>'
              '<div class="bus-in" style="left:312px;top:%dpx;width:228px;height:42px">%s</div>') % (y, ty, t, y + 18, v)
    return s + img("b_users_ico.png", "left:48px;top:545px;width:74px")


def rules():
    s = ""
    for y, h, n, t in RULES:
        ny = 628 if n == 2 else y + (h - 50) // 2
        ty = y + 12 if n != 3 else y + 18
        s += ('<div class="bus-row" style="left:642px;top:%dpx;width:448px;height:%dpx"></div>'
              '<div class="bus-n" style="left:646px;top:%dpx">%d</div>'
              '<div class="bus-tx" style="left:726px;top:%dpx">%s</div>') % (y, h, ny, n, ty, t)
    return s + '<div class="bus-code">"Network Admin"</div>'


def deflt():
    s = '<div class="bus-row" style="left:1134px;top:538px;width:504px;height:160px;background:#fbe0ef"></div>'
    for y, k, v in DEFLT:
        s += ('<div class="bus-tx" style="left:1160px;top:%dpx;line-height:40px">%s</div>'
              '<div class="bus-in" style="left:1418px;top:%dpx;width:174px;height:38px;border:0;line-height:38px">%s</div>') % (y, k, y, v)
    return s


HTML = CSS + bg("bgk_point") + "".join([
    '<div class="step">' + img("b_users_panel.png", "left:1300px;top:180px;width:295px") + '</div>',
    '<div class="step"><div class="bus-card" style="left:20px;width:582px"></div><div class="bus-rib" style="left:52px">Три атрибута</div>' + attrs() + '</div>',
    '<div class="step"><div class="bus-card" style="left:618px;width:494px"></div><div class="bus-rib" style="left:632px">Правила имени</div>' + rules() + '</div>',
    '<div class="step"><div class="bus-card" style="left:1124px;width:530px"></div>'
    '<div class="bus-rib" style="left:1146px;font-size:28px">Пользователь по умолчанию</div>' + deflt() + '</div>',
    '<div class="step"><div class="bus-warn"></div>' + img("b_users_warn.png", "left:1140px;top:722px;width:88px", "ab bus-blink")
    + '<div class="bus-tx" style="left:1232px;top:726px;font-size:20px;width:400px">После создания новой учётной записи с privilege 15 встроенный admin перестаёт действовать</div></div>',
    '<div class="step"><div class="bus-foot">Замените пароль по умолчанию на надёжный уникальный</div>'
    + img("b_users_shield.png", "left:280px;top:820px;width:115px") + '</div>',
])
