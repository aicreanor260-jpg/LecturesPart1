# -*- coding: utf-8 -*-
"""Подключение к коммутатору через консоль: схема + настройки терминала."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 200

CSS = """<style>
.bcn-lab{position:absolute;background:#ff2e93;color:#fff;font:800 26px/1 "Golos Text",sans-serif;padding:10px 22px;
  transform:skew(-8deg);box-shadow:5px 5px 0 #2a0a2a;white-space:nowrap}
.bcn-pan{position:absolute;left:1102px;top:262px;width:552px;height:510px;background:rgba(255,255,255,.95);border:3px solid #2a0a2a;
  border-radius:16px;box-shadow:9px 9px 0 rgba(255,46,147,.55)}
.bcn-hd{position:absolute;left:1162px;top:226px;background:#2a0a2a;color:#fff;font:800 32px/1 "Golos Text",sans-serif;padding:12px 26px;
  transform:skew(-6deg);box-shadow:5px 5px 0 #ff2e93;white-space:nowrap}
.bcn-row{position:absolute;left:1126px;width:510px;background:#f6e6f3;border-radius:10px;font:700 23px/1.2 "Golos Text",sans-serif;color:#1a0a1a}
.bcn-row i{position:absolute;left:14px;top:50%;margin-top:-23px;width:46px;height:46px;border-radius:50%;background:#ff2e93;color:#fff;
  font:900 28px/46px Rubik,sans-serif;text-align:center;font-style:normal}
.bcn-row span{position:absolute;left:150px;top:50%;transform:translateY(-50%);width:358px;letter-spacing:-.01em}
.bcn-row small{font-weight:500;font-size:19px}
.bcn-sum{position:absolute;left:1140px;top:690px;width:480px;background:#ff2e93;color:#fff;font:italic 900 44px/1 Rubik,sans-serif;
  padding:14px 0;text-align:center;transform:skew(-8deg);box-shadow:6px 6px 0 #2a0a2a}
.bcn-box{position:absolute;top:786px;height:136px;border:3px solid #2a0a2a;border-radius:14px;box-shadow:7px 7px 0 rgba(255,46,147,.45);
  font:500 25px/1.3 "Golos Text",sans-serif;color:#1a0a1a;box-sizing:border-box}
.bcn-box b{font-weight:800}
.bcn-txt{border:0;box-shadow:none;padding-top:14px}
.bcn-pulse{animation:bcnp 1.4s ease-in-out infinite;transform-origin:1380px 720px}
@keyframes bcnp{50%{transform:scale(1.04)}}
</style>"""

ROWS = [(300, 62, "Выберите COM-порт"), (368, 62, "Скорость: 115200 бод"),
        (436, 76, "Данные: 8 бит • Стоп: 1 • Чётность: нет"),
        (520, 76, "<b style='font-size:21px'>Управление потоком: отключено</b><br><small>Аппаратное и программное</small>"),
        (604, 64, "Эмуляция: VT100")]


def rows():
    out = "".join('<div class="bcn-row" style="top:%dpx;height:%dpx"><i>%d</i><span>%s</span></div>' % (y, h, n + 1, t)
                  for n, (y, h, t) in enumerate(ROWS))
    return out + img("b_console_ico.png", "left:1198px;top:300px;width:70px")


HTML = CSS + bg("bgk_white") + "".join([
    '<div class="step">' + img("b_console_lap.png", "left:0;top:370px;width:395px")
    + '<div class="bcn-lab" style="left:40px;top:700px">Ноутбук</div></div>',
    '<div class="step">' + img("b_console_ad.png", "left:355px;top:550px;width:305px")
    + '<div class="bcn-lab" style="left:345px;top:702px">USB ↔ RS-232</div></div>',
    '<div class="step">' + img("b_console_cab.png", "left:630px;top:540px;width:270px")
    + img("b_console_sw.png", "left:640px;top:335px;width:460px")
    + '<div class="bcn-lab" style="left:780px;top:706px">Консольный кабель</div>'
    + '<div class="bcn-lab" style="left:884px;top:570px">Console RJ-45</div></div>',
    '<div class="step"><div class="bcn-pan"></div><div class="bcn-hd">Настройки терминала</div>' + rows() + '</div>',
    '<div class="step"><div class="bcn-pulse"><div class="bcn-sum">115200 • 8N1 • VT100</div></div></div>',
    '<div class="step"><div class="bcn-box" style="left:52px;width:752px;background:#e4f6fd"></div>'
    + img("b_console_nolap.png", "left:85px;top:790px;width:275px")
    + '<div class="bcn-box bcn-txt" style="left:388px;width:400px"><b>Нет RS-232 на ноутбуке?</b><br>Используйте адаптер<br>USB ↔ RS-232.</div></div>',
    '<div class="step"><div class="bcn-box" style="left:812px;width:800px;background:#fbe6f3"></div>'
    + img("b_console_bulb.png", "left:875px;top:790px;width:110px")
    + '<div class="bcn-box bcn-txt" style="left:1006px;width:560px">Даже при поддержке автоопределения скорости рекомендуется задать <b>115200 бод вручную.</b></div></div>',
])
