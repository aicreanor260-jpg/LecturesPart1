# -*- coding: utf-8 -*-
"""Нетегированный трафик на trunk: Voice VLAN 100 + Native VLAN 20 — вёрстка на чистом фоне."""
P = "vut"
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
W, H, TOP = 1672, 941, 140
RD, GD = "#e0141c", "#c08a00"
r = lambda s: '<b style="color:%s">%s</b>' % (RD, s)
g = lambda s: '<b style="color:%s">%s</b>' % (GD, s)
DOT = '<span style="position:absolute;left:-34px;top:9px;width:18px;height:18px;border-radius:50%%;background:%s"></span>'


def bullets(x, y, col, items):
    return "".join(T(x + 34, y + i * 72, 720, DOT % col + t, 28, "line-height:1.18") for i, t in enumerate(items))


def badge(n):
    return ('<span style="position:absolute;left:0;top:0;width:44px;height:44px;border-radius:50%;background:#5a3fb0;'
            'color:#fff;font:700 24px/44px Golos Text;text-align:center">' + n + "</span>")


ARR = ('<svg class="ab" style="left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941">'
       '<defs><marker id="vut-a1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">'
       '<path d="M0 0L10 5L0 10z" fill="%s"/></marker></defs>'
       '<line x1="436" y1="%d" x2="690" y2="%d" stroke="%s" stroke-width="5" marker-start="url(#vut-a1)" marker-end="url(#vut-a1)"/>%s</svg>')
HTML = css() + bg("bgk_ground") + "".join([
    S(HD(388, 150, 896, 56, "IP-телефон и ПК: " + r("Voice VLAN 100") + " + " + g("Native VLAN 20"), "#fff", 28, True,
         "font-family:Golos Text;font-weight:800"),
      B(22, 222, 1628, 690, "background:#fff8e6"),
      '<div class="ab" style="left:380px;top:348px;width:730px;height:5px;background:#222"></div>',
      I("v_untag_trunk_sw.png", 155, 270, 230), I("v_untag_trunk_ph.png", 726, 278, 166), I("v_untag_trunk_pc.png", 1106, 278, 162),
      T(350, 364, 100, "Gi0/1", 22, "font-weight:800"),
      T(346, 393, 172, "Trunk:<br>" + r("A100") + ", " + g("N20"), 23,
        "border:3px solid #6a4a20;background:#fff3d8;text-align:center;line-height:1.1;padding:2px 0"),
      T(725, 398, 180, "IP-телефон", 28, "font-family:Pixelify Sans;font-weight:700;text-align:center"),
      T(1130, 393, 120, "PC-A", 28, "font-family:Pixelify Sans;font-weight:700;text-align:center")),
    S(ARR.replace("vut-a1", "vut-r") % ("#d8262c", 292, 292, "#d8262c", ""), I("v_untag_trunk_er.png", 484, 252, 72, "@mv"),
      HD(560, 247, 185, 34, "802.1Q: VID 100", "#d8262c", 20, st="font-family:Golos Text;border-width:2px;box-shadow:none"),
      ARR.replace("vut-a1", "vut-y") % ("#d4960a", 330, 330, "#d4960a",
                                         '<line x1="916" y1="330" x2="1088" y2="330" stroke="#d4960a" stroke-width="5" '
                                         'marker-start="url(#vut-y)" marker-end="url(#vut-y)"/>'),
      I("v_untag_trunk_ey.png", 533, 308, 73, "@mv"), I("v_untag_trunk_ey.png", 963, 298, 73, "@mv"),
      B(1302, 260, 330, 160, "border:3px dashed #555;box-shadow:none;background:transparent"),
      I("v_untag_trunk_er2.png", 1323, 280, 64), I("v_untag_trunk_ey.png", 1323, 350, 64),
      T(1400, 278, 225, r("A100") + " — VLAN 100<br>разрешена с тегом", 20, "line-height:1.2"),
      T(1400, 350, 225, g("N20") + " — native VLAN 20,<br>без тега", 20, "line-height:1.2")),
    S(B(42, 460, 786, 226, "background:#fff;border-color:#a8101a"),
      HD(42, 460, 786, 72, "Voice VLAN 100", "#d8262c", 48, st="border-color:#a8101a"), I("v_untag_trunk_er.png", 88, 470, 74),
      bullets(80, 540, "#e0141c", ["Телефон отправляет и принимает<br>кадры с тегом " + r("VID 100") + ".",
                                    "Приоритет голоса обеспечивается<br>настройками QoS."])),
    S(B(846, 460, 786, 226, "background:#fff;border-color:#8a6400"),
      HD(846, 460, 786, 72, "Data / Native VLAN 20", "#b8860b", 48, st="border-color:#8a6400"), I("v_untag_trunk_ey.png", 896, 470, 74),
      bullets(884, 540, "#d4960a", ["Трафик ПК проходит через телефон<br>без тега.",
                                    "На входе Gi0/1 относится к " + g("VLAN 20") + ";<br>на выходе передаётся без тега."])),
    S(B(42, 700, 1590, 135, "background:#e8e4ff;border-color:#6a5acd"), I("v_untag_trunk_sh.png", 60, 712, 94),
      T(172, 728, 360, "<div class='vut-px' style='font-size:34px'>Native VLAN</div><b>на межкомутаторных trunk</b>", 24),
      "".join('<div class="ab" style="left:%dpx;top:716px;width:2px;height:80px;background:#9a90d8"></div>' % x for x in (532, 862, 1240)),
      T(558, 718, 290, badge("1") + "<div style='padding-left:64px'>Часто по умолчанию —<br>VLAN 1.</div>", 19),
      T(886, 718, 340, badge("2") + "<div style='padding-left:64px'>Выделяют неиспользуемую VLAN без пользовательских access-портов.</div>", 19),
      T(1268, 712, 360, badge("3") + "<div style='padding-left:64px'>Смена native VLAN<br>не блокирует VLAN 1:<br>её исключают из allowed VLAN отдельно.</div>", 19, "line-height:1.2"),
      T(475, 803, 760, "Native VLAN и формат tagged/untagged согласуют с подключённым устройством.", 18, "font-style:italic;font-weight:500")),
    S(HD(42, 848, 1590, 56, "Один кабель к телефону — два вида трафика: <span style='color:#ff2a2a'>голос с тегом</span>, "
                            "<span style='color:#ffe14a'>данные без тега</span>.", "#1f8a2a", 30, st="font-family:Golos Text;font-weight:800"), I("v_untag_trunk_ok.png", 148, 846, 60)),
])
