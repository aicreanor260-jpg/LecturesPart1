# -*- coding: utf-8 -*-
"""Как области OSPF соединяются — вёрстка поверх чистого фона."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1672, 941, 122
K = "#1f1a33"

def box(x, y, w, h, fill, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, fill, r, ex))


def fnt(f):
    """'700 30px/1 Oswald' -> Oswald, иначе Golos Text."""
    if f.endswith(" Oswald"):
        return f[:-7] + " Oswald,sans-serif"
    return f + " 'Golos Text',sans-serif"


def tx(x, y, w, html, f="500 26px/1.3", ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%s;color:%s;%s">%s</div>'
            % (x, y, w, fnt(f), K, ex, html))


def pl(x, y, w, h, html, fill, f="700 26px/1.2", r=16, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;display:flex;align-items:center;justify-content:center;text-align:center;'
            'font:%s;color:%s;%s">%s</div>' % (x, y, w, h, fill, r, fnt(f), K, ex, html))


def sub(x, w, n, nc, ico, iw, html):
    return (box(x, 775, w, 95, "rgba(255,255,255,.96)", 18, "border:2px solid #f3e9ef")
            + img(ico, "left:%dpx;top:790px;width:%dpx" % (x + 10, iw))
            + pl(x + 13, 804, 44, 44, n, nc, "700 26px/1", 22)
            + tx(x + iw + 18, 793, w - iw - 22, html, "400 15.5px/1.3", "white-space:nowrap"))


HTML = bg("bg4", W, H) + "".join([
    tx(68, 127, 1100, "Area 0 — магистраль между остальными областями", "600 36px/1.2", "white-space:nowrap"),
    img("o_areas_join_cloud.png", "left:1420px;top:125px;width:245px"),
    '<div class="step">',
    img("o_areas_join_net.png", "left:12px;top:172px;width:1650px"),
    pl(118, 182, 280, 72, "Area 0.0.0.1<br>обычная область", "#d9ecfc", "700 23px/1.2", 18, "border:2px solid #9fcdf3"),
    pl(682, 190, 310, 72, "Area 0 • 0.0.0.0<br>магистраль", "#fdd9e8", "700 25px/1.2", 18, "border:2px solid #f6a8c8"),
    pl(1328, 162, 247, 72, "Area 0.0.0.2<br>Stub", "#d8f3dc", "700 23px/1.2", 18, "border:2px solid #9ad8a8"),
    pl(455, 264, 80, 36, "ABR", "#cfe6fb", "700 22px/1", 12, "border:2px solid #6cb2ee"),
    pl(1137, 264, 80, 36, "ABR", "#cfe6fb", "700 22px/1", 12, "border:2px solid #6cb2ee"),
    pl(793, 329, 92, 38, "ASBR", "#fde272", "700 22px/1", 12, "border:2px solid #f1c232"),
    '</div><div class="step">',
    box(25, 475, 563, 210, "#eef6fe", 22, "border:2px solid #c9e2f8"),
    img("o_areas_join_abr.png", "left:38px;top:505px;width:172px"),
    pl(212, 492, 103, 40, "ABR", "#b9dcfa", "700 26px/1", 20),
    tx(220, 538, 360, "соединяет Area 0 с другими<br>областями, хранит отдельную LSDB<br>для каждой подключённой области<br>"
       "и передаёт сводные сведения<br>о маршрутах.", "400 19.5px/1.2"),
    '</div><div class="step">',
    img("o_areas_join_srv.png", "left:600px;top:440px;width:465px"),
    pl(877, 470, 153, 50, "ввод внешних<br>маршрутов", "#fde67a", "700 17px/1.15", 10),
    pl(682, 600, 308, 70, "IS-IS / статические<br>маршруты", "#e6dcfa", "600 24px/1.15", 18, "border:2px solid #c2b0ee"),
    '</div><div class="step">',
    box(1087, 475, 563, 210, "#fef1f6", 22, "border:2px solid #f8cfe0"),
    img("o_areas_join_asbr.png", "left:1100px;top:500px;width:168px"),
    pl(1275, 492, 115, 40, "ASBR", "#fbb1cf", "700 26px/1", 20),
    tx(1282, 538, 360, "вводит в OSPF маршруты из других<br>протоколов или источников.<br>ABR связывает области; ASBR вводит"
       "<br>внешние маршруты. Один<br>маршрутизатор может совмещать<br>обе роли.", "400 19.5px/1.2",
       "white-space:nowrap"),
    '</div><div class="step">',
    box(25, 700, 1180, 182, "rgba(255,255,255,.85)", 22, "border:2px solid #f6e3ec"),
    pl(40, 712, 672, 50, "Что меняется при делении на области?", "#fbbfd6", "800 29px/1", 20),
    sub(42, 378, "1", "#fbb6cf", "o_areas_join_c1.png", 130,
        "Полная топология хранится<br>в <b>LSDB</b> своей области<br>и областей подключения."),
    sub(435, 362, "2", "#b5d8f7", "o_areas_join_c2.png", 133,
        "Внутренние изменения<br>сначала распространяются<br>в пределах области."),
    sub(810, 382, "3", "#b7e7bf", "o_areas_join_c3.png", 125,
        "<b>ABR</b> сообщает другим областям<br>о доступных сетях, а не передаёт<br>всю внутреннюю топологию."),
    '</div><div class="step">',
    box(1216, 703, 432, 97, "#fdf3c8", 18, "border:2px solid #f6e3a0"),
    img("o_areas_join_t1.png", "left:1225px;top:715px;width:75px"),
    tx(1308, 714, 340, "В некоторых конфигурациях<br>маршрутизаторы могут получать маршрут<br>по умолчанию вместо множества"
       "<br>подробных маршрутов.", "400 14px/1.27", "white-space:nowrap"),
    box(1216, 810, 432, 75, "#fdf3c8", 18, "border:2px solid #f6e3a0"),
    img("o_areas_join_t2.png", "left:1225px;top:818px;width:75px"),
    tx(1308, 820, 340, "Ориентиры “до 50 маршрутизаторов<br>в области” и “до 3 областей на маршрутизатор” —"
       "<br>учебные рекомендации, не ограничения OSPF.", "400 14px/1.27", "white-space:nowrap"),
    box(25, 892, 1623, 40, "#eef6fd", 20, "border:2px solid #d3e7f8"),
    img("o_areas_join_i.png", "left:268px;top:896px;width:36px"),
    tx(314, 902, 1320, "Размер области зависит от топологии, оборудования и частоты изменений. Деление не гарантирует "
       "заданного сокращения памяти или загрузки ЦП.", "400 14px/1.3", "white-space:nowrap"),
    '</div>',
])
