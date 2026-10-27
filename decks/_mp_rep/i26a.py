# -*- coding: utf-8 -*-
"""pptx: протокол LDP — новая сеть назначения и установление сеанса — вёрстка поверх чистого фона bgk_31.
Плашка «Исходная ситуация» стоит справа от заголовка оригинала, поэтому TOP маленький."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 40

CSS = """<style>
.i26-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i26-h{position:absolute;font:900 29px/1 "Rubik",sans-serif;color:#13306e;text-transform:uppercase}
.i26-t{position:absolute;font:500 21px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i26-n{position:absolute;font:800 21px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:110px}
.i26-bar{position:absolute;height:46px;background:#c6ebe4;border-radius:23px;font:800 23px/46px "Rubik",sans-serif;color:#13306e;
 text-transform:uppercase;padding-left:92px;white-space:nowrap;font-size:22px}
.i26-num{position:absolute;width:62px;height:62px;border-radius:50%;background:#f2694a;color:#fff;font:800 34px/62px "Golos Text";text-align:center}
.i26-pill{position:absolute;height:40px;background:#f6866b;border-radius:16px;font:700 22px/40px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i26-bx{position:absolute;background:#e3f0ee;border-radius:16px;font:500 21px/1.25 "Golos Text",sans-serif;color:#1d2a44;
 display:flex;align-items:center;justify-content:center;text-align:center}
.i26-dot{display:inline-block;width:20px;height:20px;border-radius:50%;background:#f2694a;margin-right:16px;vertical-align:-2px}
.i26-tb{position:absolute;border-collapse:collapse;font:500 21px/1 "Golos Text",sans-serif;color:#1d2a44;background:#fff}
.i26-tb th{background:#c6ebe4;font-weight:700;height:46px;border:2px solid #1d3f8a}
.i26-tb td{height:37px;border:2px solid #1d3f8a}
.i26-cap{position:absolute;width:120px;height:62px;background:#c6ebe4;border-radius:10px;font:500 20px/1.2 "Golos Text",sans-serif;
 color:#13306e;display:flex;align-items:center;justify-content:center;text-align:center}
.i26-hl{animation:i26h 2.4s ease-in-out infinite}
@keyframes i26h{0%,100%{opacity:1}50%{opacity:.35}}
</style>"""


def rt(x, y, name, w=104):
    return img("i26a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w)) + \
        '<div class="i26-n" style="left:%dpx;top:%dpx">%s</div>' % (x + (w - 110) // 2, y + 82, name)


def line(x, y, w, style, l=True, r=True):
    a = '<span style="position:absolute;%s:-4px;top:-8px;font:900 18px/1 Golos Text;color:#13306e">%s</span>'
    s = (a % ("left", "◀") if l else "") + (a % ("right", "▶") if r else "")
    return '<div style="position:absolute;left:%dpx;top:%dpx;width:%dpx;border-top:%s">%s</div>' % (x, y, w, style, s)


HTML = CSS + bg("bgk_31") + "".join([
    '<div class="step">',
    '<div class="i26-p" style="left:874px;top:52px;width:752px;height:160px"></div>',
    '<div class="i26-h" style="left:898px;top:64px">Исходная ситуация</div>',
    '<div class="i26-t" style="left:898px;top:104px;width:720px;line-height:1.6">'
    '<span class="i26-dot"></span>Метка 231 уже используется для LSP1.<br>'
    '<span class="i26-dot"></span>В таблице маршрутизации LSR1 появилась сеть 132.100.0.0.<br>'
    '<span class="i26-dot"></span>Следующий хоп — LSR2; записи для этой сети в FTN пока нет.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i26-p" style="left:46px;top:226px;width:1580px;height:432px"></div>',
    '<div class="i26-h" style="left:74px;top:238px">Процесс установления сеанса LDP</div>',
    '<div style="position:absolute;left:536px;top:286px;width:2px;height:350px;background:#c9c2ac"></div>',
    '<div style="position:absolute;left:986px;top:286px;width:2px;height:350px;background:#c9c2ac"></div>',
    '<div class="i26-bar" style="left:76px;top:284px;width:350px;padding-left:92px">Обнаружение соседей</div>',
    '<div class="i26-num" style="left:82px;top:276px">1</div>',
    rt(100, 378, "LSR1"), rt(394, 378, "LSR2"),
    '<div class="i26-t" style="left:254px;top:368px">LDP Hello</div>',
    line(216, 404, 168, "2.5px dashed #13306e"), line(216, 426, 168, "2.5px dashed #13306e"),
    '<div class="i26-pill" style="left:178px;top:492px;width:244px">224.0.0.2 • UDP 646</div>',
    '<div class="i26-bx" style="left:76px;top:548px;width:446px;height:96px">Соседние LSR с включённым LDP<br>обмениваются Hello.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i26-bar" style="left:556px;top:284px;width:320px">Установление сеанса</div>',
    '<div class="i26-num" style="left:560px;top:276px">2</div>',
    rt(588, 378, "LSR1"), rt(834, 378, "LSR2"),
    line(704, 418, 120, "2.5px solid #13306e"),
    '<div class="i26-pill" style="left:682px;top:488px;width:170px">TCP 646</div>',
    '<div class="i26-bx" style="left:556px;top:536px;width:416px;height:110px">После обнаружения соседи<br>устанавливают TCP-соединение<br>'
    'и обмениваются сообщениями<br>инициализации LDP.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i26-bar" style="left:1006px;top:282px;width:500px">Обмен метками</div>',
    '<div class="i26-num" style="left:1010px;top:274px">3</div>',
    '<div class="i26-t" style="left:1130px;top:338px;width:250px;text-align:center;font-size:19px;font-weight:700;line-height:1.2;color:#13306e">'
    'Информация о метках<br>для FEC</div>',
    '<div style="position:absolute;left:1066px;top:384px;width:330px;height:22px;border:2px dashed #13306e;border-bottom:0;border-radius:50% 50% 0 0"></div>',
    rt(1012, 394, "LSR1", 94), rt(1166, 394, "LSR2", 94), rt(1326, 394, "LSR3", 94),
    line(1108, 428, 56, "2.5px solid #13306e"), line(1262, 428, 62, "2.5px solid #13306e"),
    line(1422, 428, 34, "2.5px solid #13306e", False),
    '<div style="position:absolute;left:1456px;top:384px;width:156px;height:86px;background:#e9f6fd;border:3px solid #1d3f8a;border-radius:44px;'
    'font:700 19px/80px Golos Text,sans-serif;color:#13306e;text-align:center">132.100.0.0</div>',
    '<div class="i26-bx" style="left:1046px;top:498px;width:508px;height:66px">LSR1 использует метку, полученную<br>от следующего хопа LSR2.</div>',
    '<div style="position:absolute;left:1050px;top:570px;width:488px;height:76px;background:#fbefb6;border-radius:12px"></div>',
    '<div class="i26-hl" style="position:absolute;left:1066px;top:584px;width:46px;height:46px;border-radius:50%;background:#f2694a;'
    'font:900 30px/46px Golos Text;color:#fff;text-align:center">!</div>',
    '<div class="i26-t" style="left:1126px;top:582px;width:410px;font-size:20px">В режиме Downstream on Demand<br>отправляется запрос Label Request.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i26-p" style="left:46px;top:674px;width:546px;height:226px"></div>',
    '<div class="i26-h" style="left:70px;top:690px;font-size:19.5px">Фрагмент таблицы маршрутизации LSR1</div>',
    '<table class="i26-tb" style="left:74px;top:724px;width:496px"><tr><th>Сеть</th><th>Следующий хоп</th></tr>'
    '<tr><td style="padding-left:18px">132.100.0.0</td><td style="text-align:center">LSR2</td></tr>'
    '<tr><td style="padding-left:18px">105.0.0.0</td><td style="text-align:center">LSR4</td></tr>'
    '<tr><td style="padding-left:18px">192.201.103.0</td><td style="text-align:center">LSR4</td></tr></table>',
    '</div>',
    '<div class="step">',
    '<div class="i26-p" style="left:606px;top:674px;width:602px;height:226px"></div>',
    '<div class="i26-h" style="left:630px;top:688px">Краткий итог</div>',
    "".join(img("i26a_ic%d.png" % i, "left:%dpx;top:720px;width:88px" % (638 + i * 146)) +
            '<div class="i26-cap" style="left:%dpx;top:812px">%s</div>' % (622 + i * 146, c)
            for i, c in enumerate(["Hello:<br>UDP 646", "сеанс:<br>TCP 646", "обмен<br>метками", "записи<br>FTN / LFIB"])),
    "".join('<div class="i26-t" style="left:%dpx;top:744px;font:900 30px/1 Golos Text;color:#13306e">→</div>' % (734 + i * 146)
            for i in range(3)),
    '</div>',
])
