# -*- coding: utf-8 -*-
"""Типы записей OSPF — LSA-6: Multicast OSPF LSA. Специальное объявление для MOSPF."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1774, 887, 262
INK = "#1f1a33"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


C = "text-align:center;white-space:nowrap"
NW = "white-space:nowrap"

LEFT = [("Определён для MOSPF —", "расширения OSPF для<br>многоадресной маршрутизации", "#ffe8ef", 290, 116),
        ("Сообщает о членстве<br>узлов в multicast-группах", "LSA-6 содержит сведения<br>о членстве в группах multicast.", "#e3f0fe", 420, 136),
        ("В обычном OSPF<br>для маршрутизации<br>IP-трафика между сетями<br>обычно не требуется.", "", "#fff5cc", 570, 134),
        ("Не путать с распространёнными<br>типами LSA-1–5 и LSA-7.", "LSA-6 — это специализированный<br>тип записи, используемый в MOSPF.",
         "#efedf2", 716, 138)]


def left():
    out = []
    for i, (h, p, c, y, hh) in enumerate(LEFT):
        cy = [345, 480, 635, 775][i]
        out.append('<div class="step">' + B(26, y, 428, hh, c, 24)
                   + img("o_lsa6_l%d.png" % (i + 1), "left:38px;top:%dpx;width:92px" % (cy - 45))
                   + T(140, y + (20 if i != 2 else 14), 314, 19 if i == 3 else 20, h, 700, lh=1.25, ex=NW)
                   + (T(140, y + 20 + 25 * (h.count("<br>") + 1), 314, 17.5, p, 400, lh=1.25, ex=NW) if p else "")
                   + '</div>')
    return "".join(out)


def recv(x, y):
    return T(x, y, 160, 16.5, "<b style='font-weight:700'>Узел-получатель</b><br>(член группы)", 400, lh=1.25, ex=C)


SCENE = ('<div class="step">' + img("o_lsa6_scene.png", "left:455px;top:268px;width:695px")
         + T(484, 515, 100, 18, "Источник<br>multicast", 700, lh=1.25, ex=C)
         + T(618, 500, 146, 14.5, "<b style='font-weight:700'>Поток в<br>multicast-группу</b><br>(например, видео)", 400, lh=1.15, ex=C)
         + T(986, 550, 150, 17, "Multicast-группа<br>224.1.1.1", 700, lh=1.25, ex=C) + '</div>'
         + '<div class="step"><div>'
         + T(684, 290, 270, 22, "<span style='font-family:Oswald;font-weight:700'>LSA-6: MULTICAST OSPF LSA</span><br>"
             "<span style='font-size:18px'>Сведения о членстве<br>в группах multicast</span>", 500, lh=1.15, ex=NW + ";transform:rotate(-3deg)")
         + T(980, 292, 150, 15.5, "MOSPF строит<br>дерево доставки<br>multicast-трафика<br>к узлам группы <span style='color:#ff4f9a'>&#9829;</span>",
             600, lh=1.25, ex=NW + ";transform:rotate(8deg)")
         + '</div></div><div class="step"><div>'
         + T(735, 592, 206, 15.5, "Доставка трафика<br>к членам multicast-группы", 500, lh=1.3, ex=C)
         + recv(490, 795) + recv(730, 797) + recv(962, 797) + '</div></div>')

GRID = [("LSA-1", "#ff7aa8", "#ffe8ef", "r1", "Router LSA", "О состоянии<br>и линках<br>маршрутизатора"),
        ("LSA-2", "#5aaaf2", "#e3f0fe", "r2", "Network LSA", "О сетях<br>многодоступного<br>сегмента"),
        ("LSA-3", "#ffd23f", "#fff5cc", "r3", "Summary LSA<br>(для сетей)", "Маршруты<br>к сетям из других<br>областей"),
        ("LSA-4", "#ff7aa8", "#ffe8ef", "r4", "Summary LSA<br>(для ASBR)", "Маршруты<br>к ASBR<br>из других областей")]


def right():
    out = ['<div class="step">' + B(1160, 264, 596, 380, "rgba(255,255,255,.9)", 26, "border:2px solid #e7e9f3")
           + T(1180, 272, 570, 22, "Основные типы записей OSPF <span style='font-size:15px;font-weight:500'>(для обычной маршрутизации)</span>",
               700, f="Golos Text", lh=1.2, ex=NW + ";letter-spacing:-.01em")]
    for i, (lab, c1, c2, ic, nm, ds) in enumerate(GRID):
        x = 1176 + i * 143
        out.append(B(x, 310, 136, 186, c2, 14) + T(x + 8, 314, 120, 22, lab, 700, c="#fff", f="Oswald", ex=C + ";background:%s;border-radius:8px" % c1)
                   + img("o_lsa6_%s.png" % ic, "left:%dpx;top:346px;height:44px" % (x + 40))
                   + T(x, 392, 136, 14.5, nm, 700, lh=1.15, ex=C) + T(x + 8, 430 if "<br>" in nm else 414, 128, 12.5, ds, 400, lh=1.2, ex=NW))
    for i, (lab, c1, ic, nm, ds) in enumerate([("LSA-5", "#5aaaf2", "r5", "AS-External LSA", "Внешние маршруты<br>из других<br>автономных систем"),
                                               ("LSA-7", "#ffd23f", "r7", "NSSA External LSA", "Внешние маршруты<br>в NSSA-области")]):
        x = 1180 + i * 196
        out.append(B(x, 502, 188, 136, "#fff", 14, "border:1.5px solid #ece6ef")
                   + T(x + 26, 506, 136, 22, lab, 700, c="#fff", f="Oswald", ex=C + ";background:%s;border-radius:8px" % c1)
                   + img("o_lsa6_%s.png" % ic, "left:%dpx;top:536px;height:40px" % (x + 74))
                   + T(x, 578, 188, 15, nm, 700, ex=C) + T(x + 16, 598, 170, 12.5, ds, 400, lh=1.2, ex=NW))
    out.append(img("o_lsa6_srv.png", "left:1600px;top:470px;width:150px") + '</div>')
    out.append('<div class="step">' + B(1158, 654, 598, 206, "rgba(255,255,255,.92)", 22, "border:2.5px dashed #ff7aa8")
               + B(1172, 664, 500, 84, "#ffc4d8", 16)
               + img("o_lsa6_doc.png", "left:1178px;top:658px;width:86px")
               + T(1290, 668, 400, 30, "<span style='font-family:Oswald;font-weight:700'>LSA-6: MULTICAST OSPF LSA</span><br>(для MOSPF)", 600,
                   lh=1.2, ex=NW)
               + img("o_lsa6_rt.png", "left:1530px;top:712px;width:215px")
               + img("o_lsa6_ppl.png", "left:1183px;top:762px;width:69px")
               + T(1282, 762, 230, 19.5, "Содержит сведения<br>о членстве в группах<br>multicast", 400, lh=1.25, ex=NW) + '</div>')
    return "".join(out)


HTML = bg("bg5", W, H) + left() + SCENE + right()
