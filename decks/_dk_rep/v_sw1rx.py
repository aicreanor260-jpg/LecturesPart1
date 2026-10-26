# -*- coding: utf-8 -*-
"""Приём кадра на SW1: PVID, изучение MAC источника — вёрстка на чистом фоне."""
P = "vsr"
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
W, H, TOP = 1672, 941, 130
PXT = '<div class="vsr-px" style="font-size:34px;margin-bottom:6px">%s</div>'


def card(x, w, n, col, title, text):
    return S(B(x, 485, w, 140), HD(x + 22, 500, 80, 80, n, col, 54), T(x + 132, 498, w - 150, PXT % title + text, 24,
             "letter-spacing:.02em"))


HTML = css() + bg("bgk_sky") + "".join([
    S(I("v_sw1rx_pc.png", 218, 148, 230),
      HD(158, 292, 335, 72, "ПК1<br><span style='font:700 21px Golos Text'>MAC: 00:11:22:33:44:01</span>", "#fff3c4", 32, True,
         "white-space:normal;line-height:1.05")),
    S(LN(492, 291, 480, 12, "#2f6fd8", "#7fb0ff"), I("v_sw1rx_arr.png", 968, 262, 74, "@mv"),
      HD(520, 190, 490, 52, "Нетегированный Ethernet-кадр", "#fff3c4", 25, True)),
    S(I("v_sw1rx_sw.png", 1052, 242, 480),
      HD(1050, 152, 246, 72, "Gi0/1 · General<br>PVID 10", "#e4d8ff", 25, True, "white-space:normal"),
      HD(1432, 140, 172, 118, "VLAN 10<br><span style='font:600 18px Golos Text'>Внутренний учёт</span>", "#c8f5ec", 30, True,
         "white-space:normal")),
    S(F(208, 388, 72, [("MAC ПК2", 273, "#ff9aa8"), ("MAC ПК1", 240, "#a8d4ff"), ("EtherType", 238, "#ffe27a"),
                       ("Даные", 258, "#a8f0c8"), ("FCS", 255, "#d4b8ff")], 28)),
    card(92, 725, "1", "#1f9a7a", "Определение VLAN", "По PVID 10 входного порта SW1<br>относит кадр к VLAN 10."),
    card(840, 740, "2", "#7a3fc8", "Изучение MAC источника", "SW1 запоминает, что ПК1 доступен<br>через Gi0/1 в VLAN 10."),
    S(HD(140, 638, 1310, 54, "MAC-таблица SW1", "#173a9a", 36, st="justify-content:flex-start;padding-left:30px"),
      TB(140, 692, ["VID", "MAC-address", "Interface", "Type"], [("10", "00:11:22:33:44:01", "Gi0/1", "Dynamic")],
         [200, 485, 368, 257], 24)),
    S(B(150, 800, 1270, 115, "background:#ffe27a"), I("v_sw1rx_star.png", 168, 810, 96),
      T(280, 815, 1130, "PVID определяет VLAN входящего нетегированного кадра.<br>"
                        "Принадлежность к VLAN внутри коммутатора учитывается служебно.", 30, "font-weight:800;line-height:1.35")),
])
