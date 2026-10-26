# -*- coding: utf-8 -*-
"""VLAN: нетегированный трафик на trunk — приём в Native VLAN 30, выход access/trunk — вёрстка на пиксельном фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 148

CSS = """<style>
.vnt{position:absolute;box-sizing:border-box}
.vnt-pan{background:#fdf7e6;border:5px solid #1a2a5a;box-shadow:5px 5px 0 #000;border-radius:12px}
.vnt-rib{color:#fff;font:700 31px/50px "Pixelify Sans",monospace;padding-left:28px;white-space:nowrap;clip-path:polygon(0 0,95% 0,100% 100%,0 100%)}
.vnt-p{font:700 22px/40px "Golos Text",sans-serif;text-align:center;border-radius:8px;color:#1a1a2a}
.vnt-t{font:600 26px/1.35 "Golos Text",sans-serif;color:#1a2a5a}
.vnt-b{border:3px solid #1a2a5a;border-radius:10px;font:700 23px/1.15 "Golos Text",sans-serif;text-align:center;padding-top:6px;color:#111}
.vnt-vid{color:#fff;font:800 19px/32px "Golos Text",sans-serif;text-align:center;border:2px solid #000;border-radius:4px;clip-path:polygon(12% 0,100% 0,100% 100%,12% 100%,0 50%);padding-left:8px}
.vnt-foot{background:#3fae3a;border:5px solid #1d6e1a;box-shadow:5px 5px 0 #000;color:#fff;border-radius:10px;
  font:800 32px/62px "Golos Text",sans-serif;text-align:center;text-shadow:2px 2px 0 #1d4a1a}
.vnt-go{animation:vntg 2.4s ease-in-out infinite}
@keyframes vntg{50%{transform:translateX(16px)}}
</style>"""


def box(x, y, w, h, cls, inner="", st=""):
    return '<div class="vnt %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def env(x, y, w):
    return ('<svg class="vnt" style="left:%dpx;top:%dpx" width="%d" height="%d" viewBox="0 0 70 49">'
            '<rect x="2" y="2" width="66" height="45" fill="#eef4fc" stroke="#2a3a6a" stroke-width="3"/>'
            '<path d="M2 2 L35 28 L68 2" fill="none" stroke="#2a3a6a" stroke-width="3"/></svg>' % (x, y, w, int(w * .7)))


def arr(x1, y, x2, col):
    return ('<svg class="vnt" style="left:0;top:0;overflow:visible" width="1" height="1"><defs><marker id="vnta%s" viewBox="0 0 10 10" refX="5" refY="5" '
            'markerWidth="3.4" markerHeight="3.4" orient="auto"><path d="M0 0L10 5L0 10z" fill="%s"/></marker></defs>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="9" marker-end="url(#vnta%s)"/></svg>' % (col[1:], col, x1, y, x2, y, col, col[1:]))


VC = {"10": "#c6f0f8", "20": "#e6d3fb", "30": "#ffd84a"}
GR, RD = "#3aa83a", "#e8303a"


def acc_row(y, v, ok):
    s = box(170, y, 136, 44, "vnt-p", "VLAN " + v, "background:%s" % VC[v]) + env(330, y - 2, 60)
    if ok:
        return (s + arr(412, y + 22, 452, GR) + img("v_native_trunk_ok.png", "left:473px;top:%dpx;width:61px" % (y - 8))
                + env(558, y - 6, 74) + box(646, y - 2, 160, 48, "vnt-p", "Без тега", "background:#fbf0d0;text-align:left;padding-left:14px"))
    return (s + arr(412, y + 22, 452, RD) + img("v_native_trunk_x.png", "left:473px;top:%dpx;width:61px" % (y - 8))
            + box(556, y - 2, 250, 48, "vnt-p", "Не передаётся", "background:#fbd8d8;color:#d8202c;text-align:left;padding-left:16px"))


def trk_row(y, v, vid, txt):
    s = box(872, y, 136, 46, "vnt-p", "VLAN " + v, "background:%s" % VC[v]) + env(1032, y - 4, 60) + arr(1118, y + 22, 1158, GR) + env(1182, y - 8, 76)
    if vid:
        s += box(1246, y + 4, 92, 34, "vnt-vid", "VID " + v, "background:%s" % vid)
        return s + box(1356, y - 2, 150, 46, "vnt-p", txt, "background:#e6eef2;text-align:left;padding-left:14px")
    return s + box(1272, y - 2, 236, 46, "vnt-p", txt, "background:#eef2f4;font-size:20px")


HTML = CSS + bg("bgk_ground") + "".join([
    box(160, 155, 1352, 52, "vnt-pan", "", "border-radius:14px")
    + box(210, 160, 226, 42, "vnt-p", "Native VLAN", "background:#4ad8d8;font-size:27px;line-height:42px;border-radius:4px")
    + box(445, 160, 1050, 42, "vnt-t", "— VLAN, к которой относится нетегированный кадр на входе trunk-порта.", "font-size:23px;line-height:42px"),
    '<div class="step">' + box(142, 218, 1390, 240, "vnt-pan")
    + box(147, 223, 436, 50, "vnt-rib", "Приём на trunk-порт", "background:#7a3fc8")
    + '<div class="vnt-go" style="position:absolute;left:0;top:0">' + env(336, 292, 124) + '</div>'
    + box(298, 384, 200, 46, "vnt-b", "Без тега", "background:#fff;border-color:#c8a86a;border-radius:12px;font-size:26px;padding-top:4px")
    + arr(505, 348, 625, "#e8303a")
    + img("v_native_trunk_sw.png", "left:658px;top:298px;width:369px")
    + box(714, 229, 244, 64, "vnt-b", "Trunk:<br>Native VLAN 30", "background:#5ae0e8;font-size:24px")
    + box(714, 384, 274, 64, "vnt-b", "Принадлежность:<br><span style='font-size:27px'>VLAN 30</span>", "background:#ffd23a;font-size:23px")
    + box(1120, 265, 375, 150, "vnt-t", "VLAN определяется<br>по настройке порта,<br>а не по метке в кадре.", "background:#ddeefb;border-radius:14px;padding:22px 0 0 36px") + '</div>',
    '<div class="step">' + box(142, 468, 690, 335, "vnt-pan")
    + box(147, 473, 510, 50, "vnt-rib", "Выход ACCESS VLAN 10", "background:#e8343a")
    + acc_row(566, "10", True) + acc_row(638, "20", False) + acc_row(710, "30", False) + '</div>',
    '<div class="step">' + box(842, 468, 690, 335, "vnt-pan")
    + box(847, 473, 470, 50, "vnt-rib", "Выход&nbsp; TRUNK", "background:#7a3fc8")
    + box(872, 531, 390, 36, "vnt-p", "Tagged: VLAN 10, 20 (A10, A20)", "background:#5ae0e8;border:2px solid #1a2a5a;line-height:32px;font-size:20px")
    + box(1274, 531, 234, 36, "vnt-p", "Native: VLAN 30", "background:#ffd23a;border:2px solid #1a2a5a;line-height:32px;font-size:20px")
    + trk_row(586, "10", "#e8303a", "С тегом") + trk_row(651, "20", "#1a6ad8", "С тегом")
    + trk_row(718, "30", None, "Без тега: Native VLAN")
    + box(1280, 756, 236, 48, "vnt-b", "Тег 802.1Q удаляется;<br>FCS пересчитывается.", "background:#fde8f4;border-color:#d84ab8;font-size:15px;padding-top:4px;font-weight:600") + '</div>',
    '<div class="step">' + box(296, 818, 1080, 70, "vnt-foot", "VLAN 10 и 20 — с тегом. Native VLAN 30 — без тега.")
    + box(305, 890, 1062, 44, "vnt-t", "ⓘ&nbsp; Показан режим native untagged. Native VLAN должна совпадать на обоих концах trunk; её тегирование зависит от настроек.",
          "background:#fdf7e6;border:3px solid #1a2a5a;border-radius:8px;font-size:16px;line-height:38px;text-align:center") + '</div>',
])
