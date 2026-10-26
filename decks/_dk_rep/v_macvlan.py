# -*- coding: utf-8 -*-
"""MAC-based VLAN: MAC источника → MAC-группа → VLAN, правила и свойства — вёрстка на чистом фоне."""
P = "vmv"
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
W, H, TOP = 1672, 941, 85
BOLD = "font-family:Golos Text;font-weight:800"
DOT = '<span style="position:absolute;left:-26px;top:7px;width:14px;height:14px;border-radius:50%%;background:%s"></span>'
STEPS = [(1, 165, 46, "Прочитать MAC источника"), (2, 226, 66, "Найти совпадение<br>в правилах"), (3, 305, 46, "Отнести кадр к VLAN группы")]
STEP_FS = {1: 21, 2: 21, 3: 19}
ARR = ('<div class="vmv-mv"><svg class="ab" style="left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941">'
       '<path d="M%d 272h50v-14l26 22l-26 22v-14h-50z" fill="#e3262e" stroke="#7a0a0a" stroke-width="3"/></svg></div>')


def bl(x, y, w, col, items, fs, gap):
    return "".join(T(x, y + i * gap, w, DOT % col + t, fs, "line-height:1.12;font-weight:700") for i, t in enumerate(items))


def steps():
    out = []
    for n, y, h, t in STEPS:
        out.append(HD(1075, y + h // 2 - 23, 46, 46, str(n), "#ffc81e", 26, True, "border-radius:50%;border-width:3px;box-shadow:3px 3px 0 #000"))
        out.append(HD(1135, y, 308, h, t, "#fff8e6", STEP_FS[n], True, "justify-content:flex-start;padding-left:14px;text-align:left;"
                      + BOLD + ";white-space:normal;line-height:1.1"))
    return "".join(out)


HTML = css() + bg("bgk_falls") + "".join([
    S(HD(505, 92, 662, 54, "MAC&nbsp; источника&nbsp; →&nbsp; MAC-группа&nbsp; →&nbsp; VLAN", "#fff8e6", 29, True),
      HD(302, 165, 114, 42, "ПК1", "#fff", 24, True), I("v_macvlan_pc.png", 288, 212, 154),
      HD(243, 318, 255, 40, "MAC: 00:11:22:33:44:01", "#fff", 19, True, BOLD)),
    S(ARR % 462, HD(518, 202, 202, 44, "Без тега 802.1Q", "#fff", 21, True, BOLD), I("v_macvlan_fr.png", 553, 252, 114)),
    S(ARR % 672, I("v_macvlan_sw.png", 742, 248, 310),
      HD(770, 173, 255, 78, "VLAN 10 •<br>внутренний учёт", "#d8161c", 25, st="border-color:#ffc81e;white-space:normal;line-height:1.1")),
    S(steps()),
    S(B(228, 375, 1218, 190, "background:#fff;border-color:#8a1010;border-width:5px"),
      HD(228, 375, 1218, 52, "Настроенные правила MAC-based VLAN", "#c8161c", 32, st="border-color:#8a1010"),
      TB(266, 432, ["MAC-адрес источника", "MAC-группа", "VLAN"],
         [("00:11:22:33:44:01", "Группа 1", "10"), ("00:11:22:33:44:02", "Группа 2", "20")], [468, 397, 275], 23, "#dfe6f0",
         "box-shadow:none;border-width:3px")),
    S(B(85, 578, 515, 210, "background:#fff;border-color:#1a6a1a"), HD(85, 578, 515, 50, "Гибкость при смене порта", "#23962e", 27),
      I("v_macvlan_c1.png", 112, 628, 466),
      T(138, 698, 60, "ПК1", 21, "font-weight:800"), T(258, 696, 70, "Gi0/1", 21, "font-weight:800"),
      T(381, 696, 70, "Gi0/5", 21, "font-weight:800"),
      T(146, 728, 440, "MAC не изменился — VLAN сохраняется<br>на портах с настроенными правилами.", 20, "font-weight:800;line-height:1.2")),
    S(B(615, 578, 465, 210, "background:#fff;border-color:#0a6a6a"), HD(615, 578, 465, 50, "MAC-группы", "#14a3a0", 30),
      I("v_macvlan_c2.png", 622, 628, 156),
      bl(814, 634, 262, "#14a3a0", ["Одна группа привязана<br>к VLAN", "Группы могут включать<br>диапазоны MAC",
                                    "Применяются к физическим<br>портам и LAG."], 18, 50)),
    S(B(1094, 578, 494, 210, "background:#f3ecff;border-color:#4a1f8a"), HD(1094, 578, 494, 50, "Риск подмены MAC", "#7a3fc8", 30),
      I("v_macvlan_sh.png", 1122, 636, 126),
      bl(1304, 642, 280, "#e3262e", ["MAC-адрес можно<br>подделать.", "Сам по себе метод<br>не подтверждает<br>личность устройства."], 21, 56)),
    S(HD(285, 800, 1105, 80, "Нетегированный кадр классифицируется по MAC источника<br>и настроенным правилам.", "#ffe14a", 28, True,
         BOLD + ";white-space:normal;line-height:1.1;padding-left:60px"),
      I("v_macvlan_star.png", 312, 804, 70),
      T(470, 896, 740, "Возможности и поведение при отсутствии совпадения зависят от оборудования и настройки.", 14,
        "background:#3a4a6a;color:#fff;text-align:center;padding:8px 0 8px 40px;border:2px solid #fff;font-weight:500"),
      I("v_macvlan_i.png", 484, 898, 34)),
])
