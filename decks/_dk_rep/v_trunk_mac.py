# -*- coding: utf-8 -*-
"""VLAN: кадр ПК1 -> ПК2 через trunk SW1-SW2, форматы кадров и таблицы MAC — вёрстка на пиксельном фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.vtm{position:absolute;box-sizing:border-box}
.vtm-lab{background:#fdf7e6;border:4px solid #1a1a2a;box-shadow:4px 4px 0 #000;font:600 18px/1.12 "Golos Text",sans-serif;padding-top:4px;white-space:nowrap;text-align:center;color:#111}
.vtm-lab b{font:700 26px/1 "Pixelify Sans",monospace}
.vtm-sw{background:#fdf7e6;border:4px solid #1a1a2a;font:700 30px/40px "Pixelify Sans",monospace;text-align:center}
.vtm-bub{background:#fff;border:3px solid #1a3a6a;border-radius:10px;font:600 20px/1.1 "Golos Text",sans-serif;text-align:center;padding-top:6px}
.vtm-port{border:3px solid;border-radius:8px;font:700 20px/1.1 "Golos Text",sans-serif;text-align:center;padding-top:6px}
.vtm-pan{background:rgba(253,247,230,.95);border:3px solid #e9d9b0}
.vtm-n{width:76px;height:76px;border-radius:50%;color:#fff;font:900 46px/76px "Golos Text",sans-serif;text-align:center}
.vtm-h{font:700 23px/1.2 "Golos Text",sans-serif;color:#111}
.vtm-band{font:600 21px/34px "Golos Text",sans-serif;text-align:center;color:#111}
.vtm-f{display:flex;position:absolute;gap:2px}
.vtm-f div{border:2px solid #4a5a8a;border-radius:4px;font:600 13px/1.15 "Golos Text",sans-serif;text-align:center;display:flex;align-items:center;justify-content:center;height:58px}
.vtm-tb{position:absolute;border-collapse:collapse;font:500 21px/38px "Golos Text",sans-serif;text-align:center;color:#111}
.vtm-tb th{font-weight:700;height:40px}
.vtm-tb td{border-bottom:1px solid #ddd}
.vtm-hd{background:#132a5a;color:#fff;font:700 24px/44px "Golos Text",sans-serif;text-align:center}
.vtm-hd small{font-size:17px}
.vtm-foot{background:#3fae3a;border:5px solid #1d6e1a;box-shadow:5px 5px 0 #000;color:#fff;
  font:800 23px/48px "Golos Text",sans-serif;text-align:center;text-shadow:2px 2px 0 #1d4a1a}
.vtm-go{animation:vtmg 3s ease-in-out infinite}
@keyframes vtmg{50%{transform:translateX(18px)}}
</style>"""


def box(x, y, w, h, cls, inner="", st=""):
    return '<div class="vtm %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def env(x, y, w):
    return ('<svg class="vtm" style="left:%dpx;top:%dpx" width="%d" height="%d" viewBox="0 0 70 49">'
            '<rect x="2" y="2" width="66" height="45" fill="#fff" stroke="#222" stroke-width="3"/>'
            '<path d="M2 2 L35 28 L68 2" fill="none" stroke="#222" stroke-width="3"/></svg>' % (x, y, w, int(w * .7)))


BL, VI, PK, YE = "#cfe6fb", "#e3d6f7", "#f9c8d2", "#f7e4c0"


def frame(x, y, cells):
    return ('<div class="vtm-f" style="left:%dpx;top:%dpx">' % (x, y)
            + "".join('<div style="width:%dpx;background:%s">%s</div>' % (w, c, t) for w, c, t in cells) + '</div>')


def fr(x, tag, fcs, wide):
    m = 132 if wide else 120
    cells = [(m, BL, "MAC ПК2<br>00:11:22:33:44:02"), (m, BL, "MAC ПК1<br>00:11:22:33:44:01")]
    if tag:
        cells.append((62, PK, "<span style='color:#c8202c'>802.1Q<br>VID 10</span>"))
    cells += [(82 if wide else 78, YE, "EtherType"), (82 if wide else 70, YE, "Данные"), (76 if wide else 44, BL, fcs)]
    return frame(x, 525, cells)


def stage(x, w, n, col, bandc, head, band, frm):
    return ('<div class="step">' + box(x, 400, w, 202, "vtm-pan")
            + box(x + 14, 404, 76, 76, "vtm-n", str(n), "background:%s" % col)
            + box(x + 106, 414, w - 110, 60, "vtm-h", head)
            + box(x + 10, 484, w - 20, 36, "vtm-band", band, "background:%s" % bandc) + frm + '</div>')


ROW = '<tr><td>10</td><td>00:11:22:33:44:0%s</td><td>%s</td><td>Dynamic</td></tr>'


def table(x, name, p1, p2):
    return ('<div class="step">' + box(x, 616, 724, 176, "vtm", "", "background:#fdf7e6;border:3px solid #132a5a;border-radius:6px")
            + box(x, 616, 724, 44, "vtm-hd", "Таблица MAC-адресов %s <small>(после двустороннего обмена)</small>" % name)
            + '<table class="vtm-tb" style="left:%dpx;top:664px;width:696px"><tr><th style="background:#c6efd8;width:118px">VID</th>'
              '<th style="background:#cfe6fb;width:216px">MAC-address</th><th style="background:#e3d6f7;width:186px">Interface</th>'
              '<th style="background:#cfe6fb">Type</th></tr>' % (x + 14)
            + ROW % ("1", p1) + ROW % ("2", p2) + '</table></div>')


WIRE = ('<svg class="vtm" style="left:0;top:0" width="1672" height="941">'
        '<g stroke="#b8c4d8" stroke-width="9" fill="none"><path d="M225 292 H505"/><path d="M1168 292 H1445"/></g>'
        '<line x1="715" y1="271" x2="955" y2="271" stroke="#9a4ae8" stroke-width="9" stroke-dasharray="10 5"/></svg>')

HTML = CSS + bg("bgk_sky") + WIRE + "".join([
    '<div class="step">' + box(48, 168, 226, 88, "vtm-lab", "<b>ПК1</b><br>VLAN 10<br>MAC: 00:11:22:33:44:01")
    + img("v_trunk_mac_pc1.png", "left:123px;top:253px;width:109px")
    + box(1400, 168, 226, 88, "vtm-lab", "<b>ПК2</b><br>VLAN 10<br>MAC: 00:11:22:33:44:02")
    + img("v_trunk_mac_pc2.png", "left:1438px;top:253px;width:109px") + '</div>',
    '<div class="step">' + box(524, 176, 172, 44, "vtm-sw", "SW1") + box(976, 176, 172, 44, "vtm-sw", "SW2")
    + img("v_trunk_mac_sw1.png", "left:498px;top:218px;width:219px") + img("v_trunk_mac_sw2.png", "left:953px;top:218px;width:219px")
    + box(482, 302, 114, 86, "vtm-port", "Gi0/1<br>access<br>VLAN 10", "background:#d8f3e3;border-color:#1a8a6a;color:#0f6a4a")
    + box(626, 302, 110, 62, "vtm-port", "Gi0/24<br>trunk", "background:#e9dcfb;border-color:#7a3fc8;color:#3a1a6a")
    + box(940, 302, 108, 62, "vtm-port", "Gi0/24<br>trunk", "background:#e9dcfb;border-color:#7a3fc8;color:#3a1a6a")
    + box(1077, 302, 116, 86, "vtm-port", "Gi0/2<br>access<br>VLAN 10", "background:#d8f3e3;border-color:#1a8a6a;color:#0f6a4a")
    + '</div>',
    '<div class="step">' + box(322, 198, 134, 58, "vtm-bub", "Кадр<br>без тега") + box(1212, 198, 134, 58, "vtm-bub", "Кадр<br>без тега")
    + box(777, 170, 116, 62, "vtm-bub", "802.1Q<br>VID 10", "background:#e8303a;color:#fff;border-color:#8a0a10")
    + '<div class="vtm-go" style="position:absolute;left:0;top:0">' + env(358, 266, 60) + env(1250, 266, 60) + '</div>'
    + env(800, 248, 70) + box(856, 258, 14, 34, "vtm", "", "background:#ff5a7a;border:2px solid #8a0a10") + '</div>',
    stage(6, 550, 1, "#14877a", "#c9eedd", "SW1 принимает кадр без тега<br>и относит его к VLAN 10.", "Кадр на входе в SW1 (access, без тега)", fr(20, False, "FCS", True)),
    stage(566, 540, 2, "#7a1fb8", "#e3d3f6", "<span style='color:#5a1a9a'>На trunk добавляется тег VID 10.<br>SW2 определяет VLAN по тегу.</span>",
          "Кадр в магистрали (trunk, с тегом 802.1Q)", fr(580, True, "FCS1", False)),
    stage(1116, 550, 3, "#14877a", "#c9eedd", "На выходе access SW2 удаляет тег<br>и передаёт кадр ПК2.", "Кадр на выходе из SW2 (access, без тега)", fr(1130, False, "FCS2", True)),
    table(102, "SW1", "Gi0/1", "Gi0/24"),
    table(846, "SW2", "Gi0/24", "Gi0/2"),
    '<div class="step">' + box(478, 805, 790, 44, "vtm", "MAC ПК2 уже известен. MAC источника изучается на входящем порту.",
                               "background:#fde8ec;border-radius:20px;font:600 22px/44px 'Golos Text',sans-serif;text-align:center")
    + box(296, 862, 1080, 58, "vtm-foot", "При добавлении и удалении тега FCS пересчитывается. MAC-адреса сохраняются.") + '</div>',
])
