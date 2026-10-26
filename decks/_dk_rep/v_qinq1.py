# -*- coding: utf-8 -*-
"""Q-in-Q: кадр клиента → кадр в сети провайдера, поля, три правила — вёрстка на чистом фоне."""
P = "vq1"
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
W, H, TOP = 1672, 941, 155
GR, LT, CB, SY, LB = "#a8b2c0", "#dfe6ee", "#1f6fe0", "#ffc81e", "#a8ccff"
WH = "#fff"
ROW = "#eef2f8"
TT = "<div class='vq1-px' style='font-size:26px;color:#1d1208;text-align:center;padding-top:6px'>%s</div>"
BOLD = "font-family:Golos Text;font-weight:800"


def card(x, title, col, crop, pos, cw, ty, text, extra=""):
    return S(B(x, 604, 462, 192), HD(x, 604, 462, 48, title, col, 26), I(crop, pos[0], pos[1], cw),
             T(x + 8, ty, 446, text, 20, "text-align:center;font-weight:800;line-height:1.15"), extra)


HTML = css() + bg("bgk_hills") + "".join([
    S(HD(435, 163, 800, 50, "Внешняя VLAN провайдера поверх VLAN&nbsp; клиента", "#fff3c4", 27, True),
      B(215, 238, 375, 128), T(215, 240, 375, TT % "Кадр клиента"),
      F(236, 287, 60, [("", 30, GR), ("", 48, LT), ("C-VLAN 10", 170, CB, WH), ("", 50, "#cfe6ff"), ("", 35, GR)], 21)),
    S(I("v_qinq1_arr.png", 601, 288, 66, "@mv"), I("v_qinq1_sw.png", 678, 278, 314, "@fl"),
      HD(712, 230, 250, 46, "Правила по C-VLAN", "#fff3c4", 22, True)),
    S(I("v_qinq1_arr.png", 1001, 288, 66, "@mv"), B(1075, 238, 430, 128), T(1075, 240, 430, TT % "Кадр в сети провайдера"),
      F(1094, 287, 60, [("", 30, GR), ("", 25, LT), ("S-VLAN<br>100", 112, SY), ("C-VLAN<br>10", 112, CB, WH),
                        ("", 80, "#cfe6ff"), ("", 35, GR)], 21)),
    S(HD(100, 385, 186, 72, "Кадр<br>клиента", "#173a7a", 26),
      F(298, 387, 66, [("MAC<br>назначения", 192, ROW), ("MAC<br>источника", 186, ROW), ("C-TAG:<br>VID 10", 187, LB),
                       ("EtherType", 204, ROW), ("Данные", 338, ROW), ("FCS", 165, ROW)], 21)),
    S(HD(92, 465, 198, 72, "В сети<br>провайдера", "#1f7a3a", 26),
      F(300, 466, 66, [("MAC<br>назначения", 192, "#dde2ea"), ("MAC<br>источника", 186, ROW), ("S-TAG:<br>VID 100", 200, SY),
                       ("C-TAG:<br>VID 10", 188, LB), ("EtherType", 186, ROW), ("Данные", 200, ROW), ("FCS", 128, ROW)], 21),
      HD(340, 545, 992, 44, "В примере добавления внешнего тега C-VLAN сохраняется.", "#fff3c4", 21, True, BOLD),
      I("v_qinq1_star.png", 455, 546, 44), I("v_qinq1_star.png", 1188, 546, 44)),
    S(card(132, "Добавление SPVLAN", "#e3262e", "v_qinq1_c1.png", (170, 655), 395, 734,
           "Добавить внешнюю метку<br>S-VLAN провайдера."),
      card(606, "Подмена Customer VLAN", "#23962e", "v_qinq1_c2.png", (640, 655), 395, 720,
           "Заменить C-VLAN<br>согласно правилу.",
           T(715, 764, 243, "C-VLAN 10 → C-VLAN 20", 15, "border:2px solid #3a1606;text-align:center;font-weight:800;padding:2px 0")),
      card(1078, "Запрет трафика", "#7a3fc8", "v_qinq1_c3.png", (1135, 650), 347, 736, "Отбросить кадры,<br>запрещённые правилом.")),
    S(HD(300, 808, 1070, 42, "Подмена и фильтрация зависят от возможностей и настройки оборудования.", "#fff3c4", 19, True, BOLD),
      I("v_qinq1_i.png", 426, 810, 38),
      HD(238, 872, 496, 50, "C-VLAN — Customer VLAN, сеть клиента", CB, 21),
      HD(748, 872, 682, 50, "S-VLAN / SPVLAN — Service Provider’s VLAN, сеть провайдера", SY, 21, True)),
])
