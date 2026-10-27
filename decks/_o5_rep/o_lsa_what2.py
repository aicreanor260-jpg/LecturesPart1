# -*- coding: utf-8 -*-
"""LSA: запись о состоянии канала (вариант 2) — топология областей, 4 шага, заголовок LSA, LSA ≠ RIB.
Схемы — SVG; вырезки только девушка и котик."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img
from _o5_ikit import (puck, line, svg, cloud_icon, g4_arr, g4_area, g4_icon, g4_doc, g4_db, g4_tower,
                      g4_glyph_at, g4_ico, FADE)

W, H, TOP = 1536, 1024, 138
INK = "#1f1a33"
PK, BL = "#ff5c9e", "#2f8fe8"


def T(x, y, w, s, html, wt=500, c=INK, f="Golos Text", lh=1.2, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;font:%d %spx/%s \'%s\',sans-serif;'
            'color:%s;%s">%s</div>' % (x, y, w, wt, s, lh, f, c, ex, html))


def B(x, y, w, h, bgc, r=18, ex=""):
    return ('<div class="ab" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;'
            'border-radius:%dpx;%s"></div>' % (x, y, w, h, bgc, r, ex))


C = "text-align:center;white-space:nowrap"
CSS = """<style>
.ow2-card{position:absolute;background:rgba(255,255,255,.82);border:2px solid #ece6ef;border-radius:22px}
.ow2-n{position:absolute;width:76px;height:76px;border-radius:50%;font:800 46px/76px 'Golos Text',sans-serif;text-align:center;color:#fff}
.ow2-tb td{padding:0 10px;height:27px;border-bottom:1.5px solid #e6dbe4}
.ow2-rib td{padding:0 4px;height:20px;border:1px solid #b9d3f2;font-size:10.5px}
.ow2-hl{background:#fff1a0;border-radius:4px}
.ow2-bub{position:absolute;padding:5px 12px;border-radius:16px;font:600 13px/1.2 'Golos Text',sans-serif;color:#1f1a33;white-space:nowrap}
</style>"""


def topo():
    o = [g4_area(285, 145, 485, 215, "p", 30), g4_area(785, 200, 300, 160, "b", 30), g4_area(1090, 145, 430, 215, "y", 30),
         cloud_icon(125, 262, 2.0, "#e8f3fe", "#7fb6ee"), g4_glyph_at("globe", 138, 205, 44, BL, 2.2)]
    for a, b, c in [((222, 245), (310, 240), BL), ((400, 240), (452, 235), BL), ((480, 260), (650, 305), PK),
                    ((350, 245), (630, 300), BL), ((715, 305), (955, 300), BL), ((1015, 300), (1240, 270), BL)]:
        o.append(line(a, b, c, 5))
    o += ['<rect x="305" y="220" width="100" height="44" rx="8" style="fill:#c9ced8" stroke="#6b7385" stroke-width="2.5"/>'
          + "".join('<rect x="%d" y="232" width="14" height="12" rx="2" style="fill:#2a2f3d"/>' % (318 + i * 20) for i in range(4)),
          puck(495, 232, 110, "p"), puck(655, 300, 130, "b"), puck(950, 296, 130, "b"), puck(1250, 262, 190, "p"),
          g4_tower(1405, 180, 40, 74), g4_tower(1450, 190, 40, 70),
          '<rect x="1388" y="282" width="80" height="50" rx="5" style="fill:#3a3f55"/><rect x="1394" y="288" width="68" height="38" rx="3" style="fill:#9fcaf3"/>'
          '<path d="M1378 334 h100 l-8 10 h-84 z" style="fill:#c3c9d4"/>']
    return svg("".join(o), W, H)


TOPLBL = "".join([
    T(400, 149, 270, 17, "Область 0.0.0.1 – обычная", 700, c="#ff3d8b", ex=C),
    T(565, 186, 120, 12.5, "Внутренний<br>маршрутизатор", 500, ex="text-align:center;background:#fff;border-radius:10px;padding:3px 0"),
    T(66, 238, 150, 17, "Внешняя сеть<br>например, ISP", 700, c="#1f5fae", ex="text-align:center"),
    T(318, 279, 70, 17, "ASBR", 700, ex=C + ";background:#fff;border-radius:10px"),
    T(620, 340, 70, 17, "ABR-1", 700, ex=C + ";background:#d6eafd;border-radius:10px"),
    T(812, 213, 245, 16, "Область 0.0.0.0 – магистраль", 700, ex=C),
    T(915, 340, 70, 17, "ABR-2", 700, ex=C + ";background:#d6eafd;border-radius:10px"),
    T(1120, 151, 260, 17, "Область 0.0.0.5 – обычная", 700, ex=C),
    T(1192, 182, 120, 12.5, "Внутренний<br>маршрутизатор", 500, ex="text-align:center;background:#fff;border-radius:10px;padding:3px 0"),
])
NOTE = ('<div class="ab" style="position:absolute;left:782px;top:142px;width:300px;padding:5px 10px;background:#ffe36e;'
        'border-radius:8px;transform:rotate(-2deg);font:600 13.5px/1.25 \'Golos Text\',sans-serif;color:#1f1a33;text-align:center">'
        'Объявления LSA позволяют всем маршрутизаторам видеть одинаковую карту сети <span style="color:#ff4f9a">&#9829;</span></div>')


def col(n, x, w, ncol, title, ty, ts, para, py, scene, extra=""):
    return ('<div class="step"><div class="ow2-card" style="left:%dpx;top:378px;width:%dpx;height:410px"></div>' % (x, w)
            + '<div class="ow2-n" style="left:%dpx;top:374px;background:%s">%d</div>' % (x + 8, ncol, n)
            + T(x + 92, ty, w - 92, ts, title, 600, f="Oswald", lh=1.12, ex="white-space:nowrap")
            + T(x + 14, py, w - 10, 16.5, para, 400, lh=1.26, ex="white-space:nowrap")
            + svg(scene, W, H) + extra + '</div>')


def arrow(x):
    return T(x, 412, 30, 34, "&#10095;", 700, c="#ff4f9a")


SC1 = (puck(185, 690, 230, "p") + g4_ico("map", 112, 580, 44, "b") + g4_ico("tri", 64, 640, 40, "y")
       + g4_ico("list", 262, 645, 40, "p"))
BUB1 = ('<div class="ow2-bub" style="left:132px;top:560px;background:#d6eafd">Сведения<br>о маршрутизаторе</div>'
        '<div class="ow2-bub" style="left:84px;top:622px;background:#ffe9a0;padding-left:8px">Сведения<br>о сети</div>'
        '<div class="ow2-bub" style="left:282px;top:626px;background:#ffd6e5;padding-left:8px">Сведения<br>о маршруте</div>')
SC2 = (g4_doc(500, 575, 74, "", "b") + g4_doc(530, 585, 74, "LSA", "w", "tri", 18) + g4_doc(585, 590, 66, "", "w")
       + '<path d="M470 640 h200 v110 h-200 z" style="fill:#ffc9dd" stroke="#e05a97" stroke-width="3" stroke-linejoin="round"/>'
       + '<path d="M470 640 l100 62 l100 -62" fill="none" stroke="#e05a97" stroke-width="3"/>'
       + '<text x="590" y="735" text-anchor="middle" font-size="34" font-weight="900" style="fill:#1f1a33">LSU</text>'
       + g4_arr(410, 700, 462, 700, PK, 9) + g4_arr(680, 660, 728, 640, PK, 9))
SC3 = (g4_db(930, 640, 120, 2, "", "b")
       + '<text x="930" y="730" text-anchor="middle" font-size="22" font-weight="900" style="fill:#1f1a33">LSDB</text>'
       + puck(800, 590, 82, "p") + puck(1050, 590, 82, "b") + puck(800, 735, 82, "p") + puck(1050, 735, 82, "b")
       + g4_doc(910, 562, 38, "LSA", "w", "none", 11) + g4_doc(788, 640, 38, "LSA", "w", "none", 11)
       + g4_doc(1040, 640, 38, "LSA", "w", "none", 11)
       + g4_arr(930, 615, 930, 635, PK, 5) + g4_arr(835, 662, 868, 668, PK, 5) + g4_arr(1024, 662, 992, 668, PK, 5)
       + g4_arr(838, 722, 870, 708, PK, 5) + g4_arr(1012, 722, 990, 708, PK, 5))
SC4 = ('<rect x="1134" y="568" width="226" height="180" rx="12" style="fill:#2b2f3d"/>'
       '<rect x="1142" y="578" width="210" height="160" rx="6" style="fill:#eaf3fd"/>'
       '<path d="M1220 748 h60 l10 22 h-80 z" style="fill:#3a3f55"/>'
       + g4_db(1166, 625, 44, 2, "", "b")
       + '<text x="1166" y="690" text-anchor="middle" font-size="14" font-weight="800" style="fill:#1f1a33">LSDB</text>'
       + g4_arr(1191, 645, 1206, 645, BL, 3) + g4_glyph_at("gear", 1222, 640, 30, BL, 2.4)
       + '<text x="1222" y="676" text-anchor="middle" font-size="14" font-weight="800" style="fill:#1f1a33">SPF</text>')
TAB4 = ('<div class="ab" style="position:absolute;left:1244px;top:600px;width:104px;font:700 10px \'Golos Text\',sans-serif;'
        'color:#1f1a33;text-align:center">Таблица маршрутизации<table class="ow2-rib" style="margin-top:3px;border-collapse:collapse;'
        'width:100%;background:#fff;font-weight:500"><tr style="background:#dcecff"><td>Сеть</td><td style="white-space:nowrap">'
        'Следующий хоп</td></tr><tr><td>0.0.0.0/0</td><td>ASBR</td></tr><tr><td>0.0.1/24</td><td>ABR-1</td></tr>'
        '<tr><td>0.0.0.5/24</td><td>ABR-2</td></tr><tr><td>...</td><td>...</td></tr></table></div>').replace("10.5px", "9px")

HDR = [("Тип LSA", "1"), ("Link State ID", "192.168.1.1"), ("Advertising Router", "1.1.1.1"),
       ("Номер последовательности", "0x80000001"), ("Контрольная сумма", "0x1A2B")]
TB = ('<div class="ab" style="position:absolute;left:252px;top:782px;width:366px;height:206px;background:#fff;border:3px solid #ff8fb8;'
      'border-radius:14px;box-shadow:6px 6px 0 rgba(255,143,184,.35)">'
      '<div style="background:#ffd0e0;border-radius:10px 10px 0 0;font:600 19px/32px \'Golos Text\',sans-serif;text-align:center">LSA Header</div>'
      '<table class="ow2-tb" style="border-collapse:collapse;width:100%;font:500 15.5px \'Golos Text\',sans-serif;color:#1f1a33">'
      + "".join('<tr><td>%s</td><td style="text-align:center;border-left:1.5px solid #e6dbe4">%s</td></tr>' % r for r in HDR)
      + '</table></div>')
RIB = ('<div class="ab" style="position:absolute;left:1366px;top:868px;width:140px;font:700 12px \'Golos Text\',sans-serif;color:#1f5fae;'
       'text-align:center">Маршрут в RIB<table class="ow2-rib" style="margin-top:6px;border-collapse:collapse;width:100%;background:#fff;'
       'color:#1f1a33;font-weight:500"><tr style="background:#dcecff"><td>Сеть</td><td style="white-space:nowrap">Следующий хоп</td></tr>'
       '<tr><td>0.0.0.0/0</td><td>ASBR</td></tr><tr><td>0.0.0.5/24</td><td>ABR-2</td></tr><tr><td>...</td><td>...</td></tr></table></div>')

HTML = CSS + bg("bg2", W, H) + "".join([
    '<div class="step">' + topo() + TOPLBL + NOTE + '</div>',
    col(1, 16, 366, "#ff4f9a", "Маршрутизатор<br>формирует LSA", 392, 25,
        "При изменении состояния<br>канала маршрутизатор создаёт<br>LSA со сведениями о маршрутизаторе,<br>сети или маршруте.", 460,
        SC1, BUB1) + arrow(384),
    col(2, 412, 324, "#2f8fe8", "LSA передаётся<br>в пакете LSU", 392, 25,
        "LSA инкапсулируется в пакет<br><b style='font-weight:600'>Link State Update (LSU)</b><br>и распространяется по области<br>(или между областями).", 460, SC2) + arrow(738),
    col(3, 764, 334, "#ffd23f", "Принимающие<br>маршрутизаторы<br>сохраняют LSA в базе LSDB", 386, 20,
        "Получив LSU, маршрутизаторы<br>проверяют актуальность LSA<br>и сохраняют её в базе данных<br>состояния каналов (LSDB).", 470,
        SC3) + arrow(1098),
    col(4, 1126, 404, "#2f8fe8", "Алгоритм SPF<br>рассчитывает маршруты", 392, 25,
        "На основе полной и актуальной<br>базы LSDB маршрутизатор выполняет<br>алгоритм SPF и строит таблицу<br>маршрутизации.", 458,
        SC4, TAB4 + img("o_lsa_what2_girl.png", "left:1380px;top:524px;width:150px;" + FADE)),
    '<div class="step"><div class="ow2-card" style="left:16px;top:794px;width:640px;height:212px"></div>'
    + g4_icon("doc", 26, 802, 62, "b") + T(98, 806, 160, 25, "Заголовок LSA", 600, f="Oswald", ex="white-space:nowrap")
    + img("o_lsa_what2_kitty.png", "left:60px;top:893px;width:166px;" + FADE)
    + '<div class="ab" style="position:absolute;left:64px;top:850px;white-space:nowrap;padding:4px 8px;background:#ffd6e5;border-radius:10px;'
      'transform:rotate(-5deg);font:500 12.5px/1.25 \'Golos Text\',sans-serif;color:#1f1a33">Каждая LSA имеет заголовок<br>с основными полями.</div>'
    + TB + '</div>',
    '<div class="step"><div class="ow2-card" style="left:662px;top:794px;width:342px;height:212px"></div>'
    + g4_icon("bulb", 672, 802, 56, "y")
    + T(738, 814, 262, 18, "Link State ID зависит от типа LSA", 600, f="Oswald", ex="white-space:nowrap")
    + T(672, 862, 280, 14.5, "Link State ID зависит от типа LSA:<br>это может быть <span class='ow2-hl'>Router ID, адрес сети<br>"
        "или адрес интерфейса DR.</span>", 400, lh=1.32)
    + T(672, 926, 260, 14.5, "Он не всегда содержит номер сети<br>и маску.", 400, lh=1.32)
    + svg(g4_doc(938, 900, 52, "", "b"), W, H) + '</div>',
    '<div class="step"><div class="ow2-card" style="left:1010px;top:794px;width:518px;height:212px"></div>'
    + g4_icon("excl", 1020, 800, 60, "#ff4f8a", "#fff")
    + T(1092, 804, 420, 26, "LSA — не запись<br>в таблице маршрутизации", 600, c="#ff3d8b", f="Oswald", lh=1.1, ex="white-space:nowrap")
    + T(1024, 868, 240, 12, "LSA хранится в базе LSDB и содержит информацию о состоянии каналов "
        "(маршрутизаторах, сетях, связях).", 400, lh=1.35)
    + T(1024, 922, 240, 12, "Записи в таблице маршрутизации (RIB) создаются отдельно — на основе LSDB "
        "после выполнения <b style='font-weight:600'>алгоритма SPF</b>.", 400, lh=1.35)
    + svg(g4_doc(1268, 880, 60, "LSA", "b", "none", 17)
          + '<text x="1350" y="944" text-anchor="middle" font-size="58" font-weight="800" style="fill:#2f8fe8">≠</text>', W, H)
    + RIB + '</div>',
])
