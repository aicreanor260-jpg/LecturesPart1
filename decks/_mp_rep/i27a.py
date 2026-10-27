# -*- coding: utf-8 -*-
"""pptx: протокол LDP — запрос метки у соседа ниже по потоку (Downstream on Demand) — вёрстка поверх чистого фона bgk_02."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 172

CSS = """<style>
.i27-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i27-h{position:absolute;font:800 27px/1 "Rubik",sans-serif;color:#13306e}
.i27-t{position:absolute;font:500 21px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i27-n{position:absolute;font:800 25px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:140px}
.i27-role{position:absolute;width:186px;height:50px;background:#c9ecf8;border-radius:18px;font:500 18px/1.2 "Golos Text",sans-serif;
 color:#13306e;text-align:center;display:flex;align-items:center;justify-content:center}
.i27-ar{position:absolute;height:3px}
.i27-ar::after{content:"";position:absolute;top:-7px;border:8px solid transparent}
.i27-r::after{right:-2px;border-left:12px solid currentColor;border-right:0}
.i27-l::after{left:-2px;border-right:12px solid currentColor;border-left:0}
.i27-tb{position:absolute;border-collapse:collapse;font:700 19px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;background:#fff}
.i27-tb td{height:42px;border:2px solid #1d3f8a}
.i27-go{animation:i27g 2.8s ease-in-out infinite}
@keyframes i27g{0%,100%{opacity:1}50%{opacity:.45}}
</style>"""


def ar(x, y, w, col, d="r", cls=""):
    return '<div class="i27-ar i27-%s %s" style="left:%dpx;top:%dpx;width:%dpx;background:%s;color:%s"></div>' % (d, cls, x, y, w, col, col)


HTML = CSS + bg("bgk_02") + "".join([
    '<div class="step">',
    '<div class="i27-p" style="left:238px;top:186px;width:1182px;height:86px"></div>',
    '<div class="i27-t" style="left:266px;top:196px;width:1140px;font-size:23px;line-height:1.45">'
    '<b style="font-weight:800;color:#13306e">Условие:</b> между LSR1 и LSR2 уже установлен сеанс LDP. В таблице маршрутизации LSR1 '
    'появился маршрут к сети 132.100.0.0, следующий хопн — LSR2.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i27-p" style="left:238px;top:290px;width:1182px;height:332px"></div>',
    '<div class="i27-h" style="left:266px;top:306px;font-size:30px">Режим Downstream on Demand — распределение меток по запросу</div>',
    '<div style="position:absolute;left:390px;top:385px;width:20px;height:28px;border-left:3px solid #13306e;border-top:3px solid #13306e;'
    'border-radius:16px 0 0 0"></div>',
    ar(406, 385, 780, "#13306e"),
    '<div class="i27-t" style="left:560px;top:362px;width:370px;text-align:center;font-weight:600;font-size:20px;color:#13306e">'
    'Направление передачи данных</div>',
    img("i27a_rt.png", "left:324px;top:413px;width:134px"),
    img("i27a_rt.png", "left:952px;top:413px;width:134px"),
    '<div class="i27-n" style="left:320px;top:506px">LSR1</div><div class="i27-n" style="left:950px;top:506px">LSR2</div>',
    '<div class="i27-role" style="left:298px;top:538px">Upstream —<br>выше по потоку</div>',
    '<div class="i27-role" style="left:930px;top:538px">Downstream —<br>ниже по потоку</div>',
    '<div class="i27-t" style="left:464px;top:420px;width:476px;text-align:center;font-size:20px;color:#e23434">'
    '<b style="font-weight:800">Label Request:</b> запрашивает метку для FEC</div>',
    ar(468, 452, 474, "#e23434", "r", "i27-go"),
    ar(470, 478, 470, "#1e9a5a", "l", "i27-go"),
    '<div class="i27-t" style="left:440px;top:488px;width:524px;white-space:nowrap;text-align:center;font-size:20px;color:#1e8a4a">'
    '<b style="font-weight:800">Label Mapping:</b> сообщает привязку FEC → метка</div>',
    ar(1096, 452, 60, "#13306e"),
    '<div style="position:absolute;left:1170px;top:396px;width:240px;height:116px;background:#dff1fd;border:3px solid #2a7fd4;border-radius:60px;'
    'font:600 22px/1.25 Golos Text,sans-serif;color:#13306e;text-align:center;padding-top:28px;box-sizing:border-box">Сеть назначения<br>'
    '<b style="font-size:25px;font-weight:800">132.100.0.0</b></div>',
    '<div class="i27-t" style="left:238px;top:590px;width:1182px;text-align:center;font-size:18px;color:#13306e">'
    'Upstream и downstream определяются относительно конкретной сети назначения.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i27-p" style="left:250px;top:640px;width:588px;height:228px"></div>',
    '<div class="i27-h" style="left:276px;top:652px">Почему метку выбирает LSR2?</div>',
    '<div class="i27-t" style="left:276px;top:688px;width:540px;font-size:20.5px;line-height:1.2">Именно LSR2 будет принимать пакет с этой меткой '
    'и по ней определять FEC. Поэтому он выделяет свободное значение в своём пространстве меток и сообщает его LSR1.</div>',
    '<div style="position:absolute;left:268px;top:796px;width:552px;height:62px;background:#cdeedd;border-radius:12px"></div>',
    img("i27a_db.png", "left:284px;top:804px;width:46px"),
    '<div class="i27-t" style="left:340px;top:802px;width:470px;font-size:19px;font-weight:600;line-height:1.25;color:#13306e">'
    'Пространство меток может быть общим<br>для устройства или отдельным для интерфейса.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i27-p" style="left:852px;top:640px;width:592px;height:228px"></div>',
    '<div class="i27-h" style="left:874px;top:652px">Сообщение Label Request</div>',
    '<table class="i27-tb" style="left:872px;top:690px;width:554px"><tr><td style="background:#d6ebfb;width:276px">Запрос метки (0x0401)</td>'
    '<td style="background:#d6ebfb">Длина сообщения</td></tr><tr><td colspan="2">Идентификатор сообщения</td></tr>'
    '<tr><td colspan="2" style="background:#d6ebfb">FEC TLV — запрашиваемый класс пересылки</td></tr></table>',
    '<div class="i27-t" style="left:874px;top:834px;font-size:20px">Запрос указывает FEC, для которого требуется метка.</div>',
    '</div>',
    '<div class="step">',
    '<div style="position:absolute;left:160px;top:880px;width:1338px;height:46px;background:#fde27a;border:3px solid #1f63c6;border-radius:12px"></div>',
    img("i27a_bulb.png", "left:204px;top:884px;width:38px"),
    '<div class="i27-t" style="left:256px;top:893px;font-size:17.5px;font-weight:600;color:#13306e">Для других сетей назначения роли соседей могут отличаться. '
    'LDP также поддерживает объявления меток без предварительного запроса.</div>',
    '</div>',
])
