# -*- coding: utf-8 -*-
"""General/Hybrid: кадры без тега/с тегом, вход/выход, 5 сценариев — вёрстка на чистом фоне."""
P = "vg1"
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
W, H, TOP = 1672, 941, 145
R, GR, BL, OR, PU = "#d8262c", "#23962e", "#1f5fc4", "#f26a1c", "#7a3fc8"
Y = '<span style="color:#ffe14a">%s</span>'


def card(i, x, title, col, tint, text):
    return S(B(x, 466, 318, 368, "background:%s" % tint), HD(x + 10, 476, 298, 46, "%d.&nbsp; %s" % (i, title), col, 20),
             I("v_general1_c%d.png" % i, *CARD_IMG[i - 1]), B(x + 10, 680, 298, 140, "background:#fff;border-width:3px;box-shadow:none"),
             I("v_general1_i%d.png" % i, *ICON[i - 1]), T(x + 104, 690, 212, text, 18, "line-height:1.15"))


CARD_IMG = [(30, 535, 300), (362, 520, 293), (690, 525, 295), (1015, 530, 297), (1345, 525, 300)]
ICON = [(42, 688, 66), (370, 682, 62), (702, 688, 60), (1028, 688, 60), (1352, 690, 66)]
SP = '<div style="height:16px"></div>'
HTML = css() + bg("bgk_hills") + "".join([
    S(HD(375, 155, 920, 56, "General / Hybrid — tagged и untagged на одном порту", "#ffe14a", 31, True)),
    S(B(155, 224, 1360, 232, "background:#eef6ff"),
      '<div class="ab" style="left:236px;top:244px;width:318px;height:200px;background:#dcecff"></div>',
      '<div class="ab" style="left:786px;top:244px;width:322px;height:200px;background:#ffe2e2"></div>',
      HD(248, 248, 296, 46, "Без тега → " + Y % "PVID", "#173a7a", 27),
      HD(800, 248, 295, 46, "С тегом → " + Y % "VLAN ID", "#c4161c", 27),
      I("v_general1_fr.png", 270, 314, 128), I("v_general1_ab.png", 408, 328, 76, "@mv"),
      I("v_general1_sw.png", 488, 292, 354, "@fl"), I("v_general1_ar.png", 846, 328, 70, "@mv"),
      I("v_general1_frq.png", 920, 314, 170)),
    S('<div class="ab" style="left:1136px;top:240px;width:3px;height:200px;background:#9ab"></div>',
      I("v_general1_ag.png", 1156, 248, 68),
      T(1232, 240, 280, '<b class="vg1-px" style="color:#1e8a1e;font-size:28px">Вход:</b><br>нетегированный кадр относится к одной PVID VLAN', 21, "line-height:1.05;font-weight:700"),
      '<div class="ab" style="left:1160px;top:344px;width:330px;height:3px;background:#9ab"></div>',
      I("v_general1_ar2.png", 1156, 358, 68),
      T(1232, 352, 280, '<b class="vg1-px" style="color:#d8262c;font-size:28px">Выход:</b><br>tagged / untagged задаётся для каждой VLAN', 21, "line-height:1.05;font-weight:700")),
    card(1, 18, "IP-телефон + ПК", R, "#ffe4e4", "<b>Данные:</b><br>VLAN 10, без тега" + SP + "<b>Голос:</b><br>VLAN 20, с тегом"),
    card(2, 348, "Точка доступа Wi-Fi", GR, "#e4f7d8", "<b>Управление:</b><br>без тега, PVID" + SP + "<b>SSID:</b><br>VLAN 30 / 40 / 50,<br>с тегами"),
    card(3, 676, "Сервер виртуализации", BL, "#e0eeff", "<b>Управление:</b><br>без тега" + SP + "<b>Трафик ВМ:</b><br>VLAN с тегами"),
    card(4, 1003, "NAS и VLAN-устройства", OR, "#ffe9d8", "<b>Основной доступ:</b><br>без тега" + SP + "<b>Сервисный сегмент:</b><br>с тегом"),
    card(5, 1331, "Гибкие схемы VLAN", PU, "#efe4ff", "<b>Несколько VLAN<br>без тега на выходе</b>" + SP + "Если это поддерживает устройство"),
    S(HD(300, 840, 1070, 46, "PVID — для входа без тега; tagged / untagged — для выхода", "#ffe14a", 30, True),
      I("v_general1_star.png", 322, 840, 42), I("v_general1_star.png", 1308, 840, 42),
      T(470, 893, 750, "Названия режимов и возможности зависят от модели оборудования", 19,
        "background:#3a2a20;color:#fff;text-align:center;padding:6px 0;font-weight:500")),
])
