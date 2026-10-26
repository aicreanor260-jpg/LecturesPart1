# -*- coding: utf-8 -*-
"""VLAN: режимы работы портов Access/Trunk/General/Customer — вёрстка на пиксельном фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 148

CSS = """<style>
.vmo{position:absolute;box-sizing:border-box}
.vmo-card{background:#fdf7e6;border:5px solid;box-shadow:5px 5px 0 #000}
.vmo-hd{color:#fff;font:700 46px/62px "Pixelify Sans",monospace;padding-left:26px;white-space:nowrap;text-shadow:3px 3px 0 rgba(0,0,0,.35)}
.vmo-hd small{font:700 27px "Pixelify Sans",monospace;margin-left:10px}
.vmo-t{font:600 23px/1.3 "Golos Text",sans-serif;color:#1a1a2a}
.vmo-pill{font:600 20px/36px "Golos Text",sans-serif;text-align:center;color:#1a1a2a}
.vmo-mono{font:700 20px/36px "Golos Text",sans-serif;text-align:center;color:#1a1a2a}
.vmo-tag{color:#fff;font:800 19px/30px "Golos Text",sans-serif;text-align:center;border:2px solid #000}
.vmo-fly{animation:vmof 2.4s ease-in-out infinite}
@keyframes vmof{50%{transform:translateX(14px)}}
.vmo-foot{background:#3fae3a;border:5px solid #1d6e1a;box-shadow:5px 5px 0 #000;color:#fff;
  font:800 28px/48px "Golos Text",sans-serif;text-align:center;text-shadow:2px 2px 0 #1d4a1a}
</style>"""


def box(x, y, w, h, cls, inner="", st=""):
    return '<div class="vmo %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def env(x, y, w, cls="vmo"):
    h = int(w * .7)
    return ('<svg class="%s" style="left:%dpx;top:%dpx" width="%d" height="%d" viewBox="0 0 70 49">'
            '<rect x="2" y="2" width="66" height="45" fill="#fff" stroke="#222" stroke-width="3"/>'
            '<path d="M2 2 L35 28 L68 2" fill="none" stroke="#222" stroke-width="3"/></svg>' % (cls, x, y, w, h))


def arrow(x1, y, x2, col, both=False):
    a = '<marker id="vmoa%s" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>' % (col[1:], col)
    return ('<svg class="vmo" style="left:0;top:0;overflow:visible" width="1" height="1"><defs>%s</defs>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="7" marker-end="url(#vmoa%s)"%s/></svg>'
            % (a, x1, y, x2, y, col, col[1:], (' marker-start="url(#vmoa%s)"' % col[1:]) if both else ""))


def card(x, y, col, title, sub, body):
    return ('<div class="step">' + box(x, y, 644, 290, "vmo-card", "", "border-color:%s" % col)
            + box(x + 10, y + 10, 624, 62, "vmo-hd", "%s<small>— %s</small>" % (title, sub), "background:%s" % col)
            + body + '</div>')


ACCESS = card(188, 208, "#3fae3a", "ACCESS", "интерфейс доступа",
    box(225, 284, 600, 34, "vmo-t", "Одна VLAN. Обычно кадры передаются без тега.")
    + img("v_modes_pc.png", "left:245px;top:330px;width:135px")
    + arrow(375, 392, 560, "#2fae3a")
    + '<div class="vmo-fly" style="position:absolute;left:0;top:0">' + env(440, 367, 70) + '</div>'
    + img("v_modes_sw.png", "left:568px;top:353px;width:219px")
    + box(395, 438, 260, 38, "vmo-mono", "VLAN 10, untagged", "background:#cdeec9;border-radius:18px"))

TRUNK = card(845, 208, "#1aa6a6", "TRUNK", "несколько VLAN",
    box(886, 280, 580, 64, "vmo-t", "Тегированный трафик разных VLAN.<br>Native VLAN может передаваться без тега.")
    + img("v_modes_swl.png", "left:868px;top:363px;width:148px")
    + img("v_modes_swr.png", "left:1341px;top:363px;width:131px")
    + arrow(1030, 405, 1330, "#22b8c8", True)
    + env(1062, 388, 58) + env(1140, 388, 58) + env(1230, 388, 58)
    + box(1070, 354, 44, 30, "vmo-tag", "10", "background:#e8413c")
    + box(1148, 354, 44, 30, "vmo-tag", "20", "background:#2a8ee8")
    + box(1210, 350, 112, 28, "vmo-t", "Native VLAN", "font-size:14px;line-height:24px;text-align:center;background:#fff;border:2px solid #000;border-radius:8px")
    + box(958, 443, 430, 36, "vmo-mono", "switchport trunk native vlan &lt;VID&gt;", "background:#d8f3f8;border:2px solid #22b8c8;border-radius:18px;font-size:19px"))

GENERAL = card(188, 508, "#7a3fc8", "GENERAL", "гибкий режим 802.1Q",
    box(228, 582, 590, 64, "vmo-t", "Принимает tagged и untagged кадры.<br>Тегирование задаётся отдельно для VLAN.")
    + env(256, 662, 72)
    + arrow(343, 693, 392, "#9a5ad8") + arrow(632, 693, 585, "#9a5ad8")
    + img("v_modes_swg.png", "left:398px;top:652px;width:179px")
    + env(642, 677, 66) + env(723, 677, 66)
    + box(654, 652, 44, 30, "vmo-tag", "10", "background:#e8413c")
    + box(735, 652, 44, 30, "vmo-tag", "20", "background:#2a8ee8")
    + box(230, 718, 124, 34, "vmo-pill", "Untagged", "background:#ddd;border-radius:16px;font-weight:700;line-height:34px")
    + box(652, 722, 130, 34, "vmo-pill", "Tagged", "background:#e3d3f6;border-radius:16px;font-weight:700;line-height:34px")
    + box(228, 762, 572, 36, "vmo-pill", "PVID — VLAN для нетегированного входящего трафика", "background:#ece0fb;border:2px solid #9a5ad8;border-radius:18px;font-size:18px;line-height:32px"))

CUSTOMER = card(845, 508, "#f0503c", "CUSTOMER", "интерфейс Q-in-Q",
    box(878, 582, 580, 64, "vmo-t", "К клиентскому кадру добавляется внешний тег провайдера.")
    + env(916, 664, 108)
    + box(950, 648, 42, 30, "vmo-tag", "20", "background:#2a8ee8")
    + arrow(1055, 690, 1125, "#f0644c")
    + box(1154, 650, 302, 82, "vmo", "", "background:#fff;border:4px solid #333;box-shadow:4px 4px 0 #000")
    + box(1170, 665, 84, 52, "vmo-tag", "S-tag", "background:#e8413c;line-height:48px;font-size:22px")
    + box(1256, 665, 80, 52, "vmo-tag", "C-tag", "background:#2a8ee8;line-height:48px;font-size:22px")
    + box(1338, 665, 102, 52, "vmo-t", "Данные", "line-height:52px;text-align:center;font-weight:700;background:#eef;border:2px solid #000")
    + box(870, 724, 200, 58, "vmo-pill", "Клиентский кадр<br>(C-tag)", "background:#dde7f5;border-radius:12px;line-height:24px;padding-top:4px")
    + box(1117, 745, 342, 40, "vmo-pill", "Два тега: <b style='color:#d8301e'>S-VLAN + C-VLAN</b>", "background:#fbd3cc;border-radius:18px;line-height:40px"))

HTML = CSS + bg("bgk_ground") + "".join([
    box(445, 155, 780, 38, "vmo-pill", "Названия и возможности режимов зависят от модели коммутатора",
        "background:#e6f2ff;border:3px solid #6a9ad8;border-radius:19px;line-height:32px"),
    ACCESS, TRUNK, GENERAL, CUSTOMER,
    '<div class="step">' + box(272, 822, 1132, 58, "vmo-foot", "Режим порта определяет, какие VLAN и форматы кадров он обслуживает.")
    + box(580, 874, 515, 38, "vmo-pill", "Untagged — без тега &nbsp;•&nbsp; Tagged — с тегом",
          "background:#fdf7e6;border:3px solid #1d6e1a;border-radius:10px;line-height:32px") + '</div>',
])
