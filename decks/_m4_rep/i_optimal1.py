# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _m4_replib import bg, img
from _k import css, box, tx, grid, step, svg, path
W, H, TOP = 1672, 941, 266
P = "m4x-o1"
CSS = css(P) + """<style>
.m4x-o1-pill{position:absolute;box-sizing:border-box;border-radius:22px;border:1.5px solid rgba(63,214,255,.75);background:rgba(20,80,100,.55);
 box-shadow:0 0 10px rgba(63,214,255,.4);font:500 17px/1 "Golos Text",sans-serif;color:#eaf6f2;display:flex;align-items:center;gap:9px;padding-left:14px;white-space:nowrap}
.m4x-o1-pill svg{width:26px;height:24px;flex:none}
.m4x-o1-pk{position:absolute;box-sizing:border-box;border-radius:14px;border:2px solid rgba(63,214,255,.8);background:linear-gradient(160deg,rgba(40,130,160,.55),rgba(10,60,80,.7));box-shadow:0 0 16px rgba(63,214,255,.5)}
</style>"""
BARS = '<svg viewBox="0 0 26 24"><g fill="#3fd6ff"><rect x="2" y="12" width="5" height="10"/><rect x="10" y="5" width="5" height="17"/><rect x="18" y="9" width="5" height="13"/></g></svg>'
GAUGE = '<svg viewBox="0 0 26 24"><path d="M3 19A10 10 0 1 1 23 19" fill="none" stroke="#f0c75e" stroke-width="2"/><path d="M13 18L18 9" stroke="#f0c75e" stroke-width="2.4"/></svg>'
DB = '<svg viewBox="0 0 26 24"><g fill="none" stroke="#f6e7a8" stroke-width="2"><ellipse cx="13" cy="5" rx="9" ry="3.2" fill="#f0c75e"/><path d="M4 5v14c0 2 4 3.5 9 3.5s9-1.5 9-3.5V5M4 12c0 2 4 3.5 9 3.5s9-1.5 9-3.5"/></g></svg>'


def pill(x, y, w, h, ico, t):
    return '<div class="m4x-o1-pill" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s%s</div>' % (x, y, w, h, ico, t)


SHARE = '<svg viewBox="0 0 40 40" style="position:absolute;left:%dpx;top:%dpx;width:44px;height:44px"><g fill="none" stroke="#f6e7a8" stroke-width="3"><circle cx="20" cy="8" r="5"/><circle cx="8" cy="31" r="5"/><circle cx="32" cy="31" r="5"/><path d="M17 12L10 27M23 12L30 27M13 31H27"/></g></svg>'
STAR = '<svg viewBox="0 0 40 40" style="position:absolute;left:%dpx;top:%dpx;width:44px;height:44px"><path d="M20 3l5 11 12 1-9 8 3 12-11-7-11 7 3-12-9-8 12-1z" fill="#f0c75e" stroke="#fff0b8" stroke-width="1.5"/></svg>'
DBC = '<svg viewBox="0 0 26 24" style="position:absolute;left:%dpx;top:%dpx;width:46px;height:44px"><g fill="none" stroke="#f6e7a8" stroke-width="2"><ellipse cx="13" cy="5" rx="9" ry="3.2" fill="#f0c75e"/><path d="M4 5v14c0 2 4 3.5 9 3.5s9-1.5 9-3.5V5M4 12c0 2 4 3.5 9 3.5s9-1.5 9-3.5"/></g></svg>'


def small(x, y, ico, h, sub, w=212):
    return (box(P, x, y, w, 70, "", "border-radius:18px") + ico % (x + 20, y + 14) +
            tx(P, "s", x + 76, y + 12, h, 22, 150, "text-align:left;font-weight:700", False) +
            tx(P, "t", x + 76, y + 40, sub, 15, 170, "text-align:left;color:#d9e6dc", False))


HDR = ("Префикс", "Интерфейс", "Preference", "Cost")
tabL = grid(P, 457, 436, [457, 572, 672, 757, 826], [("0.0.0.0/0", "GE0/0", "100", "20"), ("10.1.0.0/16", "GE0/1", "100", "10"),
        ("10.1.1.0/24", "GE0/2", "100", "5"), ("172.16.0.0/16", "GE0/0", "110", "20"), ("192.168.1.0/24", "GE0/3", "100", "10"),
        ("...", "...", "...", "...")], 38.5, 16, hdr=HDR, hdrh=36, hl=(2,))
tabR = grid(P, 1057, 435, [1057, 1148, 1230, 1300, 1360], [("0.0.0.0/0", "GE0/0", "100", "20"), ("10.1.0.0/16", "GE0/1", "100", "10"),
        ("10.1.1.0/24", "GE0/2", "100", "5"), ("172.16.0.0/16", "GE0/0", "110", "20"), ("...", "...", "...", "...")], 36, 13,
        hdr=HDR, hdrh=24, hl=(2,))
m1 = grid(P, 905, 797, [905, 1048, 1153, 1230, 1303], [("10.1.0.0/16", "GE0/1", "100", "10")], 39, 17)
m2 = grid(P, 905, 836, [905, 1048, 1153, 1230, 1303], [("10.1.1.0/24", "GE0/2", "100", "5")], 41, 18, hl=(0,))

wires = svg(P,
    path(P, "M335 523 C250 480 190 425 128 408", "b", 3) +
    path(P, "M303 413 C350 425 385 470 378 520", "g", 3.2) +
    path(P, "M277 508 C310 515 335 530 352 548", "g", 3.2) +
    path(P, "M126 590 C200 592 270 584 318 574", "b", 3.2) +
    path(P, "M277 622 C300 618 322 610 336 600", "g", 3.2) +
    path(P, "M128 712 C210 705 290 665 342 612", "g", 3.2) +
    path(P, "M305 703 C345 690 362 650 370 618", "b", 3.2) +
    path(P, "M443 568 L456 570", "g", 4) +
    path(P, "M1027 512 L1052 512", "g", 4) + path(P, "M1368 520 L1400 520", "g", 4) + path(P, "M1500 520 L1546 520", "g", 4) +
    path(P, "M1430 556 C1420 590 1400 610 1378 645", "g", 3.2))

HTML = CSS + bg() + "".join([
    step(box(P, 8, 272, 838, 660, "", "border-radius:26px"), box(P, 858, 272, 806, 660, "", "border-radius:26px"),
         '<div style="position:absolute;left:849px;top:272px;width:2px;height:669px;background:linear-gradient(#f0c75e,rgba(240,199,94,.2));box-shadow:0 0 10px #f0c75e"></div>'),
    step(tx(P, "g", 320, 290, "Построение таблицы", 40, 560), tx(P, "g", 1195, 290, "Пересылка пакета", 40, 560)),
    step(img("o1_bgp.png", "left:25px;top:355px;width:105px"), img("o1_ospf.png", "left:25px;top:462px;width:105px"),
         img("o1_rip.png", "left:25px;top:566px;width:105px"), img("o1_isis.png", "left:25px;top:668px;width:105px"),
         pill(175, 392, 128, 43, BARS, "AS-PATH"), pill(160, 486, 115, 43, GAUGE, "Cost"),
         pill(140, 598, 137, 43, DB, "Hop&nbsp;count"), pill(175, 683, 128, 43, BARS, "Metric")),
    step(img("o1_router.png", "left:300px;top:520px;width:160px"), tx(P, "t", 381, 631, "Маршрутизатор", 17, 180)),
    step(box(P, 443, 380, 396, 336, "", "border-radius:20px"), tx(P, "s", 642, 396, "Таблица маршрутизации", 22, 380), tabL),
    step(wires),
    step(box(P, 145, 752, 622, 44, "", "border-radius:22px"), tx(P, "s", 456, 760, "Протоколы рассчитывают и обновляют маршруты", 23, 600)),
    step(small(85, 818, SHARE, "Префикс", "Какая сеть"), small(313, 818, STAR, "Preference", "Приоритет маршрута", 244),
         small(577, 818, DBC, "Cost", "Метрика маршрута", 234)),
    step('<div class="m4x-o1-pk" style="left:870px;top:433px;width:153px;height:139px"></div>',
         '<svg viewBox="0 0 40 30" style="position:absolute;left:884px;top:450px;width:40px;height:30px"><rect x="2" y="2" width="36" height="26" rx="3" fill="#3fd6ff"/><path d="M3 4l17 13L37 4" fill="none" stroke="#073" stroke-width="2.4"/></svg>',
         tx(P, "s", 928, 456, "IP-пакет", 19, 120, "text-align:left;font-weight:700", False),
         tx(P, "t", 886, 503, "Адрес назначения:", 14.5, 140, "text-align:left", False),
         tx(P, "s", 886, 526, "10.1.1.42", 23, 130, "text-align:left;font-weight:800", False)),
    step(box(P, 1040, 380, 338, 258, "", "border-radius:18px"), tx(P, "s", 1209, 394, "Таблица маршрутизации", 19, 300), tabR),
    step(img("o1_router_s.png", "left:1400px;top:475px;width:125px"), tx(P, "t", 1452, 559, "GE0/2", 17, 80),
         img("o1_cloud.png", "left:1545px;top:452px;width:125px"), tx(P, "t", 1607, 556, "Сеть", 17, 100), tx(P, "t", 1607, 578, "10.1.1.0/24", 17, 130)),
    step(box(P, 942, 655, 576, 74, "", "border-radius:38px"), img("o1_search.png", "left:942px;top:648px;width:94px"),
         tx(P, "s", 1270, 665, "Самое длинное совпадение префикса", 24, 520), tx(P, "s", 1270, 693, "→ выходной интерфейс", 24, 520)),
    step(box(P, 885, 752, 758, 158, "", "border-radius:22px"), tx(P, "t", 908, 762, "Совпадающие маршруты для 10.1.1.42:", 17, 480, "text-align:left;font-weight:600", False),
         '<div class="m4x-o1-hl b" style="left:905px;top:797px;width:398px;height:39px"></div>', m1, m2,
         tx(P, "s", 1330, 803, "/16", 22, 60, "text-align:left;color:#f0c75e", False), tx(P, "t", 1387, 807, "(совпадает)", 16, 120, "text-align:left", False),
         tx(P, "s", 1330, 845, "/24", 22, 60, "text-align:left;color:#f0c75e", False), tx(P, "t", 1387, 849, "(более длинный префикс)", 16, 260, "text-align:left;color:#f0c75e", False)),
])
