# -*- coding: utf-8 -*-
"""ЭТАЛОН. pptx 5: IP-передача и виртуальный канал — вёрстка поверх чистого фона bgk_07."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 160

CSS = """<style>
.i05-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i05-h{position:absolute;font:900 36px/1 "Rubik",sans-serif;color:#13306e;letter-spacing:.01em}
.i05-tag{position:absolute;background:#d6ebfb;color:#13306e;font:700 19px/34px "Golos Text",sans-serif;padding:0 14px;border-radius:6px}
.i05-t{position:absolute;font:600 22px/1.25 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i05-n{position:absolute;font:900 26px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:120px}
.i05-ar{position:absolute;height:3px;background:#24577a}
.i05-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #24577a;border-right:0}
.i05-pk{position:absolute;display:flex;height:46px;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;font:700 23px/40px "Golos Text",sans-serif}
.i05-pk b{background:#f2694a;color:#1d1d1d;padding:0 10px;font-weight:700}.i05-pk i{background:#fff;color:#1d3f8a;padding:0 18px;font-style:normal}
.i05-mpls{position:absolute;background:#bfe9e4;border-radius:22px}
.i05-row{position:absolute;border-top:2px solid #1d3f8a}
.i05-ex{position:absolute;background:#ffe3df;border:2px solid #e2564a;border-radius:10px;font:600 24px/46px "Golos Text",sans-serif;
 color:#13306e;text-align:center}
.i05-ex b{font-weight:900}
.i05-fly{animation:i05f 3s ease-in-out infinite}
@keyframes i05f{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
</style>"""


def ar(x, y, w):
    return '<div class="i05-ar" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x, y, w)


def rt(x, y, name, sub=""):
    s = '<div class="i05-t" style="left:%dpx;top:%dpx;width:240px;font-size:20px">%s</div>' % (x - 60, y + 108, sub) if sub else ""
    return img("i05a_rt.png", "left:%dpx;top:%dpx;width:120px" % (x, y)) + \
        '<div class="i05-n" style="left:%dpx;top:%dpx">%s</div>' % (x, y + 78, name) + s


def ippk(x, y):
    return img("i05a_ip.png", "left:%dpx;top:%dpx;width:118px" % (x, y)) + \
        '<div class="i05-t" style="left:%dpx;top:%dpx;width:150px">IP-пакет<br>(без метки)</div>' % (x - 16, y + 60)


def pk(x, y, lab):
    return '<div class="i05-pk i05-fly" style="left:%dpx;top:%dpx"><b>%s</b><i>IP</i></div>' % (x, y, lab)


TOP_ROW = [(358, "R1"), (638, "R2"), (920, "R3"), (1200, "R4")]
BOT_ROW = [(296, "R1", "Определяет поток<br>Добавляет метку"), (634, "R2", "Выбирает выход<br>Заменяет метку"),
           (940, "R3", "Выбирает выход<br>Заменяет метку"), (1266, "R4", "Снимает метку")]

HTML = CSS + bg("bgk_07") + "".join([
    # ---- обычная IP-сеть
    '<div class="step">',
    '<div class="i05-p" style="left:52px;top:168px;width:1568px;height:290px"></div>',
    '<div class="i05-h" style="left:80px;top:184px">ОБЫЧНАЯ IP-СЕТЬ</div>',
    ippk(106, 282), ar(232, 309, 112),
    "".join('<div class="i05-tag" style="left:%dpx;top:222px">IP назначения</div>' % (x - 24) +
            '<div class="i05-t" style="left:%dpx;top:250px;width:30px;font:900 26px/26px Golos Text;color:#24577a">↓</div>' % (x + 45)
            + rt(x, 280, n)
            for x, n in TOP_ROW),
    ar(484, 309, 140), ar(764, 309, 140), ar(1046, 309, 140), ar(1328, 309, 120),
    ippk(1462, 282),
    '<div class="i05-t" style="left:240px;top:388px;width:1200px">Каждый маршрутизатор выбирает следующий узел по своей таблице маршрутизации.<br>'
    'Путь складывается из отдельных решений; отправитель не задаёт весь маршрут.</div>',
    '</div>',
    # ---- MPLS: путь LSP
    '<div class="step">',
    '<div class="i05-p" style="left:52px;top:474px;width:1568px;height:340px"></div>',
    '<div class="i05-h" style="left:80px;top:488px">MPLS: ПУТЬ LSP</div>',
    '<div class="i05-mpls" style="left:246px;top:528px;width:1178px;height:206px"></div>',
    '<div class="i05-row" style="left:352px;top:550px;width:968px;height:14px;border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a"></div>',
    '<div class="i05-t" style="left:752px;top:534px;width:170px;background:#bfe9e4;font:800 26px/34px Golos Text,sans-serif;color:#13306e">MPLS-сеть</div>',
    ippk(90, 588), ar(212, 610, 72),
    "".join(rt(x, 578, n, s) for x, n, s in BOT_ROW),
    ar(418, 610, 36), pk(462, 588, 100), ar(600, 610, 22),
    ar(756, 610, 22), pk(790, 588, 200), ar(910, 610, 22),
    ar(1062, 610, 32), pk(1104, 588, 300), ar(1232, 610, 22),
    ar(1388, 610, 74), ippk(1480, 588),
    '</div>',
    '<div class="step">',
    '<div class="i05-row" style="left:362px;top:750px;width:948px;height:12px;border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a"></div>',
    '<div class="i05-t" style="left:620px;top:737px;width:430px;background:#fdf8ea;font:800 21px/26px Golos Text,sans-serif;color:#13306e">'
    'Предварительно сформированный LSP</div>',
    '<div class="i05-ex" style="left:450px;top:772px;width:772px;height:46px">Пример записи: метка <b>100</b> → интерфейс <b>2</b> → '
    'новая метка <b>200</b></div>',
    '</div>',
    # ---- итог
    '<div class="step">',
    '<div class="i05-p" style="left:326px;top:836px;width:1020px;height:78px;border-radius:16px"></div>',
    '<div class="i05-t" style="left:326px;top:844px;width:1020px;font:800 26px/1.2 Golos Text,sans-serif;color:#13306e">'
    'Виртуальный канал — логический путь через общую сеть.<br>Отдельный физический кабель не требуется.</div>',
    '</div>',
])
