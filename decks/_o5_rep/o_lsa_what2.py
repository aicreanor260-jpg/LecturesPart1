# -*- coding: utf-8 -*-
"""LSA: запись о состоянии канала (вариант 2) — топология областей, 4 шага, заголовок LSA, LSA ≠ RIB."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _o5_replib import bg, img

W, H, TOP = 1536, 1024, 138
INK = "#1f1a33"


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
</style>"""

TOPLBL = "".join([
    T(400, 149, 270, 17, "Область 0.0.0.1 – обычная", 700, c="#ff3d8b", ex=C),
    T(570, 190, 120, 12.5, "Внутренний<br>маршрутизатор", 500, ex="text-align:center"),
    T(66, 235, 150, 17, "Внешняя сеть<br>например, ISP", 700, c="#1f5fae", ex="text-align:center"),
    T(313, 279, 60, 17, "ASBR", 700, ex=C),
    T(622, 341, 70, 17, "ABR-1", 700, ex=C),
    T(830, 213, 245, 16, "Область 0.0.0.0 – магистраль", 700, ex=C),
    T(913, 341, 70, 17, "ABR-2", 700, ex=C),
    T(1145, 151, 260, 17, "Область 0.0.0.5 – обычная", 700, ex=C),
    T(1198, 190, 120, 12.5, "Внутренний<br>маршрутизатор", 500, ex="text-align:center"),
])
NOTE = ('<div class="ab" style="position:absolute;left:782px;top:142px;width:300px;padding:5px 10px;background:#ffe36e;'
        'border-radius:8px;transform:rotate(-2deg);font:600 13.5px/1.25 \'Golos Text\',sans-serif;color:#1f1a33;text-align:center">'
        'Объявления LSA позволяют всем маршрутизаторам видеть одинаковую карту сети <span style="color:#ff4f9a">&#9829;</span></div>')


def col(n, x, w, ncol, title, ty, ts, para, py, crop, cx, cy, cw, extra=""):
    return ('<div class="step"><div class="ow2-card" style="left:%dpx;top:378px;width:%dpx;height:410px"></div>' % (x, w) + extra
            + '<div class="ow2-n" style="left:%dpx;top:374px;background:%s">%d</div>' % (x + 8, ncol, n)
            + T(x + 92, ty, w - 92, ts, title, 600, f="Oswald", lh=1.12, ex="white-space:nowrap")
            + T(x + 14, py, w - 10, 16.5, para, 400, lh=1.26, ex="white-space:nowrap")
            + img(crop, "left:%dpx;top:%dpx;width:%dpx" % (cx, cy, cw)) + '</div>')


def arrow(x):
    return T(x, 412, 30, 34, "&#10095;", 700, c="#ff4f9a")


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
    '<div class="step">' + img("o_lsa_what2_top.png", "left:0;top:138px;width:1536px") + TOPLBL + NOTE + '</div>',
    col(1, 16, 366, "#ff4f9a", "Маршрутизатор<br>формирует LSA", 392, 25,
        "При изменении состояния<br>канала маршрутизатор создаёт<br>LSA со сведениями о маршрутизаторе,<br>сети или маршруте.", 460,
        "o_lsa_what2_c1.png", 18, 546, 362) + arrow(384),
    col(2, 412, 324, "#2f8fe8", "LSA передаётся<br>в пакете LSU", 392, 25,
        "LSA инкапсулируется в пакет<br><b style='font-weight:600'>Link State Update (LSU)</b><br>и распространяется по области<br>(или между областями).", 460, "o_lsa_what2_c2.png", 385, 548, 350) + arrow(738),
    col(3, 764, 334, "#ffd23f", "Принимающие<br>маршрутизаторы<br>сохраняют LSA в базе LSDB", 386, 20,
        "Получив LSU, маршрутизаторы<br>проверяют актуальность LSA<br>и сохраняют её в базе данных<br>состояния каналов (LSDB).", 470,
        "o_lsa_what2_c3.png", 735, 552, 360) + arrow(1098),
    col(4, 1126, 404, "#2f8fe8", "Алгоритм SPF<br>рассчитывает маршруты", 392, 25,
        "На основе полной и актуальной<br>базы LSDB маршрутизатор выполняет<br>алгоритм SPF и строит таблицу<br>маршрутизации.", 458,
        "o_lsa_what2_c4.png", 1080, 545, 456, img("o_lsa_what2_hair.png", "left:1442px;top:438px;width:94px")),
    '<div class="step"><div class="ow2-card" style="left:16px;top:794px;width:640px;height:212px"></div>'
    + img("o_lsa_what2_doc.png", "left:20px;top:798px;width:72px") + T(98, 806, 160, 25, "Заголовок LSA", 600, f="Oswald", ex="white-space:nowrap")
    + img("o_lsa_what2_cat.png", "left:55px;top:868px;width:195px")
    + '<div class="ab" style="position:absolute;left:64px;top:850px;white-space:nowrap;padding:4px 8px;background:#ffd6e5;border-radius:10px;'
      'transform:rotate(-5deg);font:500 12.5px/1.25 \'Golos Text\',sans-serif;color:#1f1a33">Каждая LSA имеет заголовок<br>с основными полями.</div>'
    + TB + '</div>',
    '<div class="step"><div class="ow2-card" style="left:662px;top:794px;width:342px;height:212px"></div>'
    + img("o_lsa_what2_bulb.png", "left:672px;top:800px;width:56px")
    + T(738, 814, 262, 18, "Link State ID зависит от типа LSA", 600, f="Oswald", ex="white-space:nowrap")
    + T(672, 862, 280, 14.5, "Link State ID зависит от типа LSA:<br>это может быть <span class='ow2-hl'>Router ID, адрес сети<br>"
        "или адрес интерфейса DR.</span>", 400, lh=1.32)
    + T(672, 926, 260, 14.5, "Он не всегда содержит номер сети<br>и маску.", 400, lh=1.32)
    + img("o_lsa_what2_doc2.png", "left:930px;top:890px;width:70px") + '</div>',
    '<div class="step"><div class="ow2-card" style="left:1010px;top:794px;width:518px;height:212px"></div>'
    + img("o_lsa_what2_ex.png", "left:1018px;top:795px;width:67px")
    + T(1092, 804, 420, 26, "LSA — не запись<br>в таблице маршрутизации", 600, c="#ff3d8b", f="Oswald", lh=1.1, ex="white-space:nowrap")
    + T(1024, 868, 240, 12, "LSA хранится в базе LSDB и содержит информацию о состоянии каналов "
        "(маршрутизаторах, сетях, связях).", 400, lh=1.35)
    + T(1024, 922, 240, 12, "Записи в таблице маршрутизации (RIB) создаются отдельно — на основе LSDB "
        "после выполнения <b style='font-weight:600'>алгоритма SPF</b>.", 400, lh=1.35)
    + img("o_lsa_what2_ne.png", "left:1258px;top:875px;width:114px") + RIB + '</div>',
])
