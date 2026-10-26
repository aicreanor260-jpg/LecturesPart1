# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _k import css, box, tx, grid, step, svg, path
W, H, TOP = 1672, 941, 104
P = "m4x-me"
CSS = css(P) + """<style>
.m4x-me-num{position:absolute;width:62px;height:62px;border-radius:50%;box-sizing:border-box;border:2.5px solid #f0c75e;background:radial-gradient(#0b2a22,#04140f);
 box-shadow:0 0 14px rgba(240,199,94,.6);font:800 40px/56px "Playfair Display",serif;font-variant-numeric:lining-nums;color:#fff0b8;text-align:center}
.m4x-me-pk{position:absolute;box-sizing:border-box;border:2px solid rgba(120,230,255,.85);border-radius:6px;
 background:linear-gradient(160deg,rgba(80,190,230,.6),rgba(20,90,130,.7));box-shadow:0 0 18px rgba(63,214,255,.55);transform:perspective(500px) rotateY(-9deg) skewY(2deg);
 font-family:"Golos Text",sans-serif;color:#eaf8ff}
.m4x-me-pk div{position:absolute;left:14px;white-space:nowrap;text-shadow:0 1px 3px rgba(0,0,0,.6)}
.m4x-me-fc{position:absolute;box-sizing:border-box;border:1.5px solid rgba(240,199,94,.7);border-radius:6px;background:rgba(8,38,30,.8);
 font:500 13.5px/1.1 "Golos Text",sans-serif;color:#eaf0e6;text-align:center;display:flex;align-items:center;justify-content:center}
.m4x-me-fc.c{background:rgba(40,190,200,.55);border-color:#3fe6ff;font-size:16px}
.m4x-me-ch{position:absolute;font:300 50px/1 "Golos Text",sans-serif;color:#f0c75e;text-shadow:0 0 8px #f0c75e}
.m4x-me-ar{position:absolute;font:300 40px/1 "Golos Text",sans-serif;color:#f0c75e}
</style>"""


def head(cx, ttl, t2=None, x=None, y1=None):
    return '<div class="m4x-me-num" style="left:%dpx;top:%dpx">%s</div>' % (cx - 31, 164, "")


def num(cx, n):
    return '<div class="m4x-me-num" style="left:%dpx;top:%dpx">%d</div>' % (cx - 31, 164, n)


def pk(x, y, w, h, big=True):
    return ('<div class="m4x-me-pk" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"><div style="top:10px;font:600 %dpx \'Golos Text\'">IP-пакет</div>'
            '<div style="top:%dpx;font-size:%dpx">IP источника</div><div style="top:%dpx;font-size:%dpx;font-weight:700">IP назначения</div></div>'
            % (x, y, w, h, 22 if big else 19, h * 0.45, 15 if big else 14, h * 0.68, 18 if big else 16))


def frame_cells(x, y, w, ttl, cells):
    o = box(P, x, y, w, 96, "", "border-radius:10px;background:rgba(6,30,24,.65)") + tx(P, "t", x + 17, y + 8, ttl, 16, 300, "text-align:left;font-weight:500", False)
    for (cx, cw, t, c) in cells:
        o += '<div class="m4x-me-fc %s" style="left:%dpx;top:%dpx;width:%dpx;height:50px">%s</div>' % (c, cx, y + 38, cw, t)
    return o


GLOBE = ('<g><circle cx="1620" cy="470" r="240" fill="rgba(20,90,90,.3)" stroke="#3fd6b0" stroke-width="2" filter="url(#m4x-megl)"/>'
         '<g fill="none" stroke="rgba(240,199,94,.18)" stroke-width="1.2"><ellipse cx="1620" cy="470" rx="120" ry="240"/><ellipse cx="1620" cy="470" rx="240" ry="110"/>'
         '<path d="M1400 390 C1500 360 1560 420 1640 380M1420 520 C1500 560 1580 520 1680 560M1450 440 L1530 470 L1600 430 L1640 500"/></g>'
         '<g fill="#fff0b8"><circle cx="1450" cy="440" r="4"/><circle cx="1530" cy="470" r="4"/><circle cx="1600" cy="430" r="4"/><circle cx="1640" cy="500" r="4"/><circle cx="1500" cy="380" r="3"/><circle cx="1580" cy="550" r="3"/></g></g>')

flows = svg(P,
    GLOBE +
    path(P, "M190 378 C260 372 330 400 413 410", "g", 3.5) + path(P, "M190 392 C260 400 330 430 413 420", "g", 2) +
    path(P, "M190 400 C300 470 400 590 650 590", "g", 3.5) + path(P, "M190 392 C280 440 380 560 650 572", "g", 2) +
    path(P, "M620 425 C650 430 680 435 700 438", "b", 3.5) + path(P, "M972 435 C990 435 1000 410 1012 395", "b", 3.5) +
    path(P, "M1000 590 C1050 580 1030 450 1012 410", "b", 3.5) + path(P, "M1195 385 C1280 380 1340 400 1400 410", "b", 3.5) +
    path(P, "M1195 395 C1280 400 1340 420 1400 430", "b", 2) +
    '<path d="M98 800 L98 800" />' +
    path(P, "M307 798 L383 798", "s", 2) + path(P, "M580 798 L650 798", "s", 2))

tab = grid(P, 710, 337, [710, 858, 962], [("10.0.0.0/8", "eth0"), ("172.16.0.0/12", "eth1"), ("192.168.0.0/16", "xe0"), ("0.0.0.0/0", "xe1")], 30, 15.5,
           hdr=("Сеть назначения", "Интерфейс"), hdrh=28, hl=(2,), hlcls="b", lines=True)

HTML = CSS + bg() + "".join([
    step(flows),
    step(num(75, 1), tx(P, "g", 125, 177, "Приём кадра", 27, 260, "text-align:left", False),
         tx(P, "t", 190, 238, "Входящий Ethernet-кадр", 17.5, 300), tx(P, "t", 190, 259, "с медного порта", 17.5, 300),
         img("m_copper.png", "left:8px;top:285px;width:192px"),
         frame_cells(40, 452, 336, "Ethernet-кадр (входящий)", [(52, 87, "МАС<br>назначения", ""), (143, 85, "МАС<br>источника", ""), (231, 82, "IP-пакет", "c"), (317, 47, "FCS", "")])),
    step('<div class="m4x-me-ch" style="left:352px;top:345px">&#8250;</div>',
         num(415, 2), tx(P, "g", 466, 170, "IP-адрес", 25, 220, "text-align:left", False), tx(P, "g", 466, 198, "назначения", 25, 220, "text-align:left", False),
         tx(P, "t", 518, 243, "Извлечение IP-пакета", 17.5, 300), tx(P, "t", 518, 264, "и анализ адреса", 17.5, 300), pk(413, 338, 207, 137)),
    step('<div class="m4x-me-ch" style="left:644px;top:350px">&#8250;</div>',
         num(713, 3), tx(P, "g", 757, 182, "Поиск маршрута", 24, 300, "text-align:left", False),
         tx(P, "t", 838, 238, "Поиск в таблице", 17.5, 300), tx(P, "t", 838, 259, "маршрутизации", 17.5, 300),
         box(P, 700, 296, 272, 201, "", "border-radius:12px;background:rgba(6,30,24,.78)"),
         '<svg viewBox="0 0 30 30" style="position:absolute;left:719px;top:304px;width:28px;height:28px"><circle cx="12" cy="12" r="8" fill="none" stroke="#3fe6ff" stroke-width="3"/><path d="M18 18L27 27" stroke="#3fe6ff" stroke-width="3.5"/></svg>',
         tx(P, "t", 761, 306, "Таблица маршрутизации", 16, 220, "text-align:left", False), tab),
    step('<div class="m4x-me-ch" style="left:1006px;top:352px">&#8250;</div>',
         num(1060, 4), tx(P, "g", 1113, 170, "Выходной", 25, 220, "text-align:left", False), tx(P, "g", 1113, 198, "интерфейс", 25, 220, "text-align:left", False),
         tx(P, "t", 1180, 262, "Инкапсуляция IP-пакета", 16, 300) + tx(P, "t", 1180, 283, "в новый кадр канального уровня", 16, 300),
         img("m_sfp.png", "left:1005px;top:300px;width:195px"),
         frame_cells(1027, 452, 330, "Новый кадр (выходящий)", [(1038, 86, "МАС<br>назначения", ""), (1128, 82, "МАС<br>источника", ""), (1213, 84, "IP-пакет", "c"), (1301, 46, "FCS", "")])),
    step('<div class="m4x-me-ch" style="left:1326px;top:345px">&#8250;</div>',
         num(1383, 5), tx(P, "g", 1435, 182, "Новый кадр", 27, 240, "text-align:left", False),
         tx(P, "t", 1508, 243, "Передача по оптическому", 17.5, 320), tx(P, "t", 1508, 265, "интерфейсу в сеть назначения", 17.5, 320),
         tx(P, "t", 1542, 442, "Сеть", 16.5, 140), tx(P, "t", 1542, 463, "назначения", 16.5, 140)),
    step(img("m_device.png", "left:625px;top:520px;width:425px")),
    step(box(P, 22, 665, 963, 245, "", "border-radius:26px"), tx(P, "g", 503, 672, "Программная коммутация", 28, 520),
         tx(P, "t", 500, 705, "Обработка каждого пакета процессором", 17.5, 420), pk(105, 742, 200, 113, False),
         '<div class="m4x-me-ar" style="left:340px;top:775px">&#8594;</div>', img("m_chip.png", "left:432px;top:748px;width:138px"),
         '<div class="m4x-me-ar" style="left:608px;top:775px">&#8594;</div>', img("m_port.png", "left:698px;top:748px;width:187px"),
         tx(P, "t", 499, 852, "Поиск в таблице", 17.5, 240), tx(P, "t", 499, 873, "маршрутизации", 17.5, 240),
         tx(P, "t", 790, 852, "Выбор", 17.5, 200), tx(P, "t", 790, 873, "интерфейса", 17.5, 200)),
    step(box(P, 1000, 665, 648, 245, "", "border-radius:26px"), tx(P, "g", 1288, 676, "На скорость влияют:", 25, 480),
         img("m_c1.png", "left:1070px;top:722px;width:112px"), img("m_c2.png", "left:1250px;top:722px;width:122px"), img("m_c3.png", "left:1440px;top:722px;width:132px"),
         tx(P, "t", 1125, 850, "Поиск", 17.5, 180), tx(P, "t", 1125, 872, "маршрута", 17.5, 180), tx(P, "t", 1313, 852, "Память", 17.5, 180),
         tx(P, "t", 1507, 850, "Шина", 17.5, 200), tx(P, "t", 1507, 872, "ввода-вывода", 17.5, 200)),
])
