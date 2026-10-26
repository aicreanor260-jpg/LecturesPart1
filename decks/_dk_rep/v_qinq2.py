# -*- coding: utf-8 -*-
"""Q-in-Q: клиент A → SW1 → SW2 → клиент B, поля кадра на каждом участке, таблицы — вёрстка на чистом фоне."""
P = "vq2"
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

_CSS = """<style>
.@b{position:absolute;box-sizing:border-box;background:#fff8e6;border:4px solid #3a1606;box-shadow:5px 5px 0 #000}
.@h{position:absolute;box-sizing:border-box;display:flex;align-items:center;justify-content:center;gap:10px;color:#fff;
  font:700 28px/1.08 "Pixelify Sans",sans-serif;text-align:center;text-shadow:2px 2px 0 #000;border:4px solid #3a1606;
  box-shadow:5px 5px 0 #000;white-space:nowrap}
.@h.@d{color:#1d1208;text-shadow:none}
.@t{position:absolute;box-sizing:border-box;font:600 24px/1.25 "Golos Text",sans-serif;color:#1d1208}
.@t b{font-weight:800}
.@px{font-family:"Pixelify Sans",sans-serif;font-weight:700}
.@f{position:absolute;display:flex;box-sizing:border-box;border:4px solid #3a1606;box-shadow:5px 5px 0 #000;background:#fff}
.@f>div{display:flex;align-items:center;justify-content:center;text-align:center;font:700 22px/1.1 "Golos Text",sans-serif;
  border-right:3px solid #3a1606;box-sizing:border-box;flex:none}
.@f>div:last-child{border-right:0}
.@tb{position:absolute;border-collapse:collapse;table-layout:fixed;background:#fff;border:4px solid #3a1606;box-shadow:5px 5px 0 #000;
  font:600 22px/1.15 "Golos Text",sans-serif;color:#1d1208;text-align:center}
.@tb td,.@tb th{border:2px solid #7aa7d8;padding:3px 6px}
.@tb th{font-weight:800}
.@mv{animation:@mv 1.1s ease-in-out infinite alternate}
@keyframes @mv{to{transform:translateX(9px)}}
.@fl{animation:@fl 3s ease-in-out infinite}
@keyframes @fl{50%{transform:translateY(-6px)}}
.@bl{animation:@bl 1s steps(2) infinite}
@keyframes @bl{50%{opacity:.35}}
.@ln{position:absolute;background-size:28px 100%;animation:@ln .8s linear infinite}
@keyframes @ln{to{background-position:28px 0}}
</style>"""


def _(s):
    return s.replace("@", P + "-")


def css(extra=""):
    return _(_CSS + extra)


def S(*parts):
    return '<div class="step">' + "".join(parts) + "</div>"


def B(x, y, w, h, st=""):
    return _('<div class="@b" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s"></div>' % (x, y, w, h, st))


def HD(x, y, w, h, html, bgc, fs=28, dark=False, st=""):
    if fs < 26:  # мелкий пиксельный кириллический шрифт нечитаем
        st = "font-family:Golos Text;font-weight:800;" + st
    return (_('<div class="@h%s"' % (" @d" if dark else "")) +
            ' style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:%s;font-size:%dpx;%s"><div>%s</div></div>'
            % (x, y, w, h, bgc, fs, st, html))


def T(x, y, w, html, fs=24, st=""):
    return _('<div class="@t"') + ' style="left:%dpx;top:%dpx;width:%dpx;font-size:%dpx;%s">%s</div>' % (x, y, w, fs, st, html)


def F(x, y, h, cells, fs=22, st=""):
    out = []
    for c in cells:
        t, w = c[0], c[1]
        b = c[2] if len(c) > 2 else "#fff"
        col = c[3] if len(c) > 3 else "#1d1208"
        out.append('<div style="width:%dpx;background:%s;color:%s;font-size:%dpx">%s</div>' % (w, b, col, fs, t))
    return _('<div class="@f"') + ' style="left:%dpx;top:%dpx;height:%dpx;%s">%s</div>' % (x, y, h, st, "".join(out))


def TB(x, y, head, rows, widths, fs=22, thbg="#cfe6ff", st=""):
    cg = "".join('<col style="width:%dpx">' % w for w in widths)
    th = "".join('<th style="background:%s">%s</th>' % (thbg, h) for h in head)
    tr = "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows)
    return (_('<table class="@tb"') + ' style="left:%dpx;top:%dpx;width:%dpx;font-size:%dpx;%s"><colgroup>%s</colgroup>'
            '<tr>%s</tr>%s</table>' % (x, y, sum(widths), fs, st, cg, th, tr))


def I(f, x, y, w, cls=""):
    return img(f, "left:%dpx;top:%dpx;width:%dpx" % (x, y, w), ("ab " + _(cls)).strip())


def LN(x, y, w, h, c1, c2):
    return _('<div class="@ln"') + (' style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border:2px solid #1d1208;'
                                    'background-image:repeating-linear-gradient(90deg,%s 0 14px,%s 14px 28px)"></div>'
                                    % (x, y, w, h, c1, c2))
W, H, TOP = 1672, 941, 95
CB, SY, LC = "#1f6fe0", "#ffc81e", "#4aa8ff"
BOLD = "font-family:Golos Text;font-weight:800"
LBL = dict(dark=True, st="white-space:normal;line-height:1.12")
HEAD_T = ["VID", "MAC-address", "Interface", "Type"]
M1, M2 = "00:11:22:33:44:01", "00:11:22:33:44:02"
ROW1 = [("MAC получателя", 252), ("MAC источника", 264), ("C-VLAN 10", 192, LC), ("EtherType", 198), ("Данные", 266), ("FCS", 148)]
ROW2 = [("MAC получателя", 240), ("MAC источника", 236), ("S-VLAN 30", 168, SY), ("C-VLAN 10", 168, LC), ("EtherType", 168),
        ("Данные", 222), ("FCS", 118)]


def card(x, w, n, title, col, tint, text, dark=False):
    return S(B(x, 328, w, 148, "background:%s;border-color:%s" % (tint, col)),
             HD(x, 328, w, 48, title, col, 21 if len(title) > 16 else 24, dark, "padding-left:70px"),
             HD(x + 4, 324, 66, 56, n, col, 40, dark, "box-shadow:3px 3px 0 #000"),
             T(x + 20, 382, w - 30, text, 23, "text-align:center;line-height:1.2"))


def row(y, lbl, tint, edge, cells):
    return S(B(26, y, 1620, 58, "background:%s;border-color:%s;box-shadow:none" % (tint, edge)),
             T(55, y + 12, 260, lbl, 26, "font-family:Pixelify Sans;font-weight:700"),
             F(314, y + 4, 50, cells, 21, "box-shadow:none;border-width:2px"))


def table(x, title, rows):
    return (HD(x, 690, 784, 40, title, "#a8d8ff", 22, True, BOLD + ";box-shadow:none;border-width:3px") +
            TB(x, 728, HEAD_T, rows, [118, 252, 200, 206], 19, "#e4f2ff", "box-shadow:none;border-width:3px"))


def port(x, t):
    return HD(x, 276, 80, 30, t, "#fff3c4", 16, True, BOLD + ";border-width:2px;box-shadow:2px 2px 0 #000")


HTML = css() + bg("bgk_hills") + "".join([
    S(HD(542, 105, 588, 44, "Внешняя метка 30, внутренняя метка 10", "#fff3c4", 25, True),
      HD(98, 112, 252, 64, "Клиент A<br><span style='font:600 17px Golos Text'>MAC: 00:11:22:33:44:01</span>", "#fff", 24, **LBL),
      HD(1322, 112, 252, 64, "Клиент B<br><span style='font:600 17px Golos Text'>MAC: 00:11:22:33:44:02</span>", "#fff", 24, **LBL),
      LN(190, 236, 272, 10, "#2f8be0", "#8fc8ff"), LN(676, 236, 320, 10, "#ffc81e", "#fff0a0"),
      LN(1216, 236, 60, 10, "#ffc81e", "#fff0a0"), LN(1276, 236, 210, 10, "#2f8be0", "#8fc8ff"),
      I("v_qinq2_mario.png", 118, 188, 84), I("v_qinq2_luigi.png", 1468, 188, 84),
      HD(260, 222, 140, 38, "C-VLAN 10", CB, 20, st=BOLD),
      HD(714, 222, 124, 38, "S-VLAN 30", SY, 19, True, BOLD),
      HD(840, 222, 120, 38, "C-VLAN 10", CB, 19, st=BOLD),
      HD(1272, 222, 140, 38, "C-VLAN 10", CB, 20, st=BOLD),
      HD(465, 172, 218, 38, "SW1 провайдера", "#fff", 21, True), HD(990, 172, 218, 38, "SW2 провайдера", "#fff", 21, True),
      I("v_qinq2_sw.png", 452, 212, 230), I("v_qinq2_sw2.png", 992, 212, 230),
      port(446, "Gi0/11"), port(605, "Gi0/12"), port(989, "Gi0/12"), port(1147, "Gi0/11")),
    card(26, 388, "1", "Приём на SW1", "#e3262e", "#ffe4e4", "Gi0/11: кадр с C-VLAN 10.<br>Правило: добавить<br>S-VLAN 30."),
    row(484, "На входе SW1:", "#dcdcf8", "#8a8ad8", ROW1),
    card(428, 402, "2", "Добавление внешнего тега", "#23962e", "#e4f7d8", "SW1 → Gi0/12: два тега.<br>Коммутация по S-VLAN 30."),
    row(551, "Между SW1 и SW2:", "#fff3c4", "#e8c84a", ROW2),
    card(846, 398, "3", "Приём на SW2", "#1f5fc4", "#e0eeff", "Gi0/12: два тега.<br>По MAC получателя<br>выбран Gi0/11."),
    card(1258, 388, "4", "Выход к клиенту B", SY, "#fff6d0", "Удалить только S-VLAN 30.<br>C-VLAN 10 сохраняется.", True),
    row(618, "На выходе SW2:", "#dcdcf8", "#8a8ad8", ROW1),
    S(table(46, "Таблица коммутации SW1", [("30", M1, "Gi0/11", "Dynamic"), ("30", M2, "Gi0/12", "Dynamic")]),
      table(843, "Таблица коммутации SW2", [("30", M1, "Gi0/12", "Dynamic"), ("30", M2, "Gi0/11", "Dynamic")]),
      T(50, 838, 1572, "После обмена в обе стороны; обучение и коммутация по внешней S-VLAN.", 22,
        "background:#c8f5c8;border:3px solid #3fae3a;text-align:center;font-weight:800;padding:2px 0")),
    S(T(120, 880, 1430, "C-VLAN 10 сохраняется на всём пути. MAC-адреса и данные не меняются. FCS пересчитывается при изменении тегов.", 21,
        "background:#ffc0d8;border:3px solid #3a1606;text-align:center;font-weight:800;padding:8px 0 8px 90px;box-shadow:4px 4px 0 #000"),
      I("v_qinq2_star.png", 142, 872, 66)),
])
