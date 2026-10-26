# -*- coding: utf-8 -*-
"""General 802.1Q: SW1 → SW2 → ПК2, поля кадра и таблицы коммутации — вёрстка на чистом фоне."""
P = "vg2"
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
W, H, TOP = 1672, 941, 125
R, GR, BL = "#e3262e", "#23962e", "#1f5fc4"
MACS = ["00:11:22:33:44:0%d" % i for i in range(1, 5)]
HEAD_T = ["VID", "MAC-address", "Interface", "Type"]
WID = [100, 270, 166, 172]


def table(x, title, col, ico, ports):
    rows = [(v, m, p, "Dynamic") for v, m, p in zip(("10", "10", "20", "20"), MACS, ports)]
    return (HD(x, 614, 716, 50, title, col, 32, st="padding-left:40px") + I(ico, x + 96, 616, 48) +
            TB(x + 4, 664, HEAD_T, rows, WID, 24, "#cfe6ff"))


LBL = dict(dark=True, st="white-space:normal;line-height:1.1")
HTML = css() + bg("bgk_hills") + "".join([
    S(HD(196, 132, 130, 62, "ПК1<br>VLAN 10", "#fff", 24, **LBL), I("v_general2_pc1.png", 186, 200, 116),
      LN(300, 256, 212, 10, "#4aa3ff", "#bfe2ff"), HD(340, 198, 130, 42, "Без тега", "#eaf6ff", 22, True),
      HD(530, 157, 128, 44, "SW1", "#fff", 26, True), I("v_general2_sw.png", 508, 202, 164)),
    S(LN(668, 234, 334, 16, "#e3262e", "#ff9aa0"), HD(726, 176, 215, 44, "802.1Q · VID 10", "#ffd23a", 24, True),
      HD(690, 262, 290, 44, "Gi0/24 ↔ Gi0/24 · General", "#fff", 21, True),
      HD(1012, 157, 125, 44, "SW2", "#fff", 26, True), I("v_general2_sw.png", 995, 202, 164),
      LN(1158, 256, 222, 10, "#4aa3ff", "#bfe2ff"),
      HD(1172, 196, 184, 58, "Gi0/1 · General ·<br>VLAN 10 untagged", "#eaf6ff", 18, **LBL),
      HD(1345, 132, 135, 62, "ПК2<br>VLAN 10", "#fff", 24, **LBL), I("v_general2_pc2.png", 1373, 200, 119)),
    S(B(60, 328, 516, 172), HD(60, 328, 516, 46, "2. Добавление тега на SW1", R, 27),
      I("v_general2_m1.png", 94, 380, 44),
      T(168, 386, 400, "По MAC ПК2 в VLAN 10 → Gi0/24<div style='height:22px'></div>Добавить тег 802.1Q (VID 10)", 24),
      HD(135, 510, 320, 44, "SW1 → SW2 · с тегом", R, 24),
      F(470, 510, 44, [("MAC ПК2", 178, "#d9c8ff"), ("MAC ПК1", 157, "#cfe8ff"), ("802.1Q: VID 10", 218, "#ffd23a"),
                       ("EtherType", 173, "#ffc8e6"), ("Данные", 197, "#b8f0cf"), ("FCS", 145, "#d9c8ff")], 22)),
    S(B(590, 328, 505, 172), HD(590, 328, 505, 46, "3. Приём на SW2", BL, 27), I("v_general2_m2.png", 628, 372, 40),
      T(696, 374, 395, "По VID 10 определить VLAN<br>PVID не используется<br>Изучение источника: ПК1 → Gi0/24<br>Назначение: ПК2 → Gi0/1", 21, "line-height:1.45")),
    S(B(1110, 328, 500, 172), HD(1110, 328, 500, 46, "4. Снятие тега к ПК2", GR, 27), I("v_general2_m3.png", 1150, 374, 46),
      T(1225, 384, 380, "Gi0/1: VLAN 10 untagged<div style='height:14px'></div>Удалить тег 802.1Q →<br>обычный кадр к ПК2", 24),
      HD(135, 561, 320, 44, "SW2 → ПК2 · без тега", BL, 24),
      F(470, 561, 44, [("MAC ПК2", 187, "#d9c8ff"), ("MAC ПК1", 197, "#cfe8ff"), ("EtherType", 222, "#ffc8e6"),
                       ("Данные", 297, "#b8f0cf"), ("FCS", 165, "#d9c8ff")], 22)),
    S(table(112, "Таблица коммутации SW1", R, "v_general2_mr.png", ("Gi0/1", "Gi0/24", "Gi0/2", "Gi0/24")),
      table(843, "Таблица коммутации SW2", BL, "v_general2_mb.png", ("Gi0/24", "Gi0/1", "Gi0/24", "Gi0/2")),
      I("v_general2_mario.png", 0, 735, 112), I("v_general2_luigi.png", 1560, 730, 112)),
    S(T(500, 852, 670, "После обмена кадрами в обе стороны в своих VLAN", 22,
        "background:#fff3c4;border:3px solid #3a1606;text-align:center;padding:3px 0"),
      T(395, 892, 880, "FCS пересчитывается при изменении тега. MAC-адреса сохраняются.", 21,
        "background:#fff3c4;border:3px solid #3a1606;text-align:center;padding:4px 0")),
])
