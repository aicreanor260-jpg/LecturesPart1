# -*- coding: utf-8 -*-
"""VLAN: магистральные порты — trunk 802.1Q между SW1 и SW2, три шага — вёрстка на пиксельном фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 116

CSS = """<style>
.vt1{position:absolute;box-sizing:border-box}
.vt1-pan{background:#fdf7e6;border:5px solid #1a2a5a;box-shadow:5px 5px 0 #000;border-radius:14px}
.vt1-dom{font:700 17px/1.15 "Golos Text",sans-serif;text-align:center;border:2px solid;border-radius:6px;padding-top:2px}
.vt1-pc{color:#fff;font:800 19px/30px "Golos Text",sans-serif;text-align:center;border-radius:5px}
.vt1-nt{background:#fff;border:2px solid #1a2a5a;border-radius:6px;font:700 16px/26px "Golos Text",sans-serif;text-align:center;color:#1a1a2a}
.vt1-vid{color:#fff;font:800 19px/30px "Golos Text",sans-serif;text-align:center;border-radius:4px;border:2px solid #000}
.vt1-al{white-space:nowrap;background:#fff;border:3px solid #1a2a5a;font:700 17px/1 "Golos Text",sans-serif;text-align:center;padding-top:8px}
.vt1-al div{background:#c6efd8;margin:9px 8px 0;line-height:28px}
.vt1-trk{background:#0d1a3a;color:#fff;font:700 29px/40px "Pixelify Sans",monospace;text-align:center;border-radius:6px}
.vt1-c{border:5px solid;border-radius:12px;box-shadow:5px 5px 0 #000}
.vt1-h{font:700 30px/1 "Pixelify Sans",monospace;color:#111}
.vt1-t{font:500 19px/1.18 "Golos Text",sans-serif;color:#1a1a2a}
.vt1-coin{width:76px;height:76px;border-radius:50%;background:#ffc21a;border:5px solid #3a1606;font:900 40px/66px "Golos Text",sans-serif;text-align:center;color:#3a1606;box-shadow:inset -6px -6px 0 #e08a00}
.vt1-foot{background:#3fae3a;border:5px solid #1d6e1a;box-shadow:5px 5px 0 #000;color:#fff;border-radius:24px;
  font:800 23px/52px "Golos Text",sans-serif;text-align:center;text-shadow:2px 2px 0 #1d4a1a}
.vt1-fl{animation:vt1f 2.2s ease-in-out infinite}
@keyframes vt1f{50%{transform:translateY(-6px)}}
</style>"""


def box(x, y, w, h, cls, inner="", st=""):
    return '<div class="vt1 %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def env(x, y, w, fill="#fff"):
    return ('<svg class="vt1" style="left:%dpx;top:%dpx" width="%d" height="%d" viewBox="0 0 70 49">'
            '<rect x="2" y="2" width="66" height="45" fill="%s" stroke="#222" stroke-width="3"/>'
            '<path d="M2 2 L35 28 L68 2" fill="none" stroke="#222" stroke-width="3"/></svg>' % (x, y, w, int(w * .7), fill))


def side(x, y, col, bgc, dom, pc, pimg, ex, ey):
    return (box(x, y, 284, 46, "vt1-dom", dom, "color:%s;border-color:%s;background:%s" % (col, col, bgc))
            + box(x, y + 46, 222, 104, "vt1", "", "background:%s" % bgc)
            + img(pimg, "left:%dpx;top:%dpx;width:72px" % (x + 98, y + 50))
            + box(x + 64, y + 118, 136, 30, "vt1-pc", pc, "background:%s" % col)
            + env(ex, ey, 46) + box(ex - 22, ey + 34, 86, 28, "vt1-nt", "Без тега"))


LINES = ('<svg class="vt1" style="left:0;top:0" width="1672" height="941">'
         '<g stroke="#1a2a5a" stroke-width="4" fill="none"><path d="M265 280 H410 L510 330"/><path d="M265 438 H405 L510 370"/>'
         '<path d="M1405 280 H1262 L1165 330"/><path d="M1405 438 H1262 L1165 370"/></g>'
         '<g stroke-width="5"><line x1="655" y1="328" x2="1025" y2="328" stroke="#e83a3a"/><line x1="655" y1="336" x2="1025" y2="336" stroke="#ffcc22"/>'
         '<line x1="655" y1="344" x2="1025" y2="344" stroke="#2a6ae8"/><line x1="655" y1="352" x2="1025" y2="352" stroke="#8a4ad8"/></g></svg>')


def card(x, w, col, bgc, n, title, text):
    return ('<div class="step">' + box(x, 543, w, 158, "vt1-c", "", "border-color:%s;background:%s" % (col, bgc))
            + box(x + 14, 552, 76, 76, "vt1-coin", str(n))
            + box(x + 116, 563, w - 130, 34, "vt1-h", title) + box(x + 116, 602, w - 130, 96, "vt1-t", text) + '</div>')


HTML = CSS + bg("bgk_ground") + "".join([
    box(425, 120, 822, 58, "vt1", "<b>Trunk:</b>&nbsp; несколько&nbsp; VLAN по одному физическому каналу",
        "background:#fdf7e6;border:5px solid #1a3a8a;border-radius:16px;box-shadow:4px 4px 0 #000;font:600 24px/48px 'Golos Text',sans-serif;text-align:center"),
    box(70, 190, 1535, 352, "vt1-pan"),
    '<div class="step">' + LINES
    + side(104, 212, "#d8202c", "#fbe0e0", "Один широковещательный<br>домен VLAN 10", "ПК, VLAN 10", "v_trunk1_pcr.png", 407, 256)
    + side(104, 372, "#1a6ad8", "#ddebfb", "Отдельный домен VLAN 20", "ПК, VLAN 20", "v_trunk1_pcb.png", 404, 414).replace("height:46px", "height:44px;line-height:38px", 1)
    + side(1286, 212, "#d8202c", "#fbe0e0", "Один широковещательный<br>домен VLAN 10", "ПК, VLAN 10", "v_trunk1_pcr.png", 1224, 256).replace("left:1384px", "left:1400px")
    + side(1286, 372, "#1a6ad8", "#ddebfb", "Отдельный домен VLAN 20", "ПК, VLAN 20", "v_trunk1_pcb.png", 1224, 414).replace("height:46px", "height:44px;line-height:38px", 1)
    + '</div>',
    '<div class="step">' + img("v_trunk1_sw1.png", "left:498px;top:288px;width:164px")
    + img("v_trunk1_sw2.png", "left:1016px;top:288px;width:158px")
    + box(493, 402, 182, 70, "vt1-al", "Allowed: 10, 20, 99<div>Native:&nbsp; 99</div>")
    + box(1000, 402, 180, 70, "vt1-al", "Allowed: 10, 20, 99<div>Native:&nbsp; 99</div>")
    + box(716, 318, 240, 44, "vt1-trk", "TRUNK&nbsp; 802.1Q") + '</div>',
    '<div class="step"><div class="vt1-fl" style="position:absolute;left:0;top:0">'
    + env(732, 220, 72, "#f7b6b8") + env(864, 222, 70, "#bcdcf8") + '</div>'
    + box(723, 274, 90, 30, "vt1-vid", "VID 10", "background:#d8202c")
    + box(855, 274, 90, 30, "vt1-vid", "VID 20", "background:#1a6ad8")
    + env(808, 364, 56) + box(704, 405, 264, 34, "vt1-nt", "Native VLAN 99 — без тега", "font-size:18px;line-height:30px")
    + env(740, 458, 62, "#d6c6f4") + box(735, 504, 74, 28, "vt1-vid", "VID 30", "background:#5a2aa8;font-size:17px;line-height:24px")
    + img("v_trunk1_x.png", "left:806px;top:453px;width:51px")
    + box(850, 462, 140, 36, "vt1-nt", "VLAN не разрешена", "background:#eadcfb;border-color:#b89ae8;color:#5a2aa8;font-size:13px;line-height:32px")
    + '</div>',
    card(188, 415, "#1a8a8a", "#d5f3ef", 1, "Приём tagged", "Принимаются кадры<br>разрешённых VLAN.<br>Остальные отбрасываются."),
    card(622, 437, "#7a3fc8", "#ebe0fb", 2, "Native VLAN", "Нетегированный входящий<br>кадр относится к Native VLAN.<br>В этом примере она передаётся<br>без тега."),
    card(1078, 408, "#d8303a", "#fbe0e0", 3, "Передача", "Теги разрешённых VLAN<br>сохраняются. Исключение —<br>нетегированная Native VLAN."),
    '<div class="step">' + box(235, 712, 1210, 78, "vt1-pan", "", "border-color:#1a6a5a;border-radius:10px")
    + img("v_trunk1_swi.png", "left:253px;top:723px;width:99px")
    + box(384, 724, 440, 60, "vt1-t", "<b style='font-size:22px'>Access между коммутаторами:</b><br>отдельный канал для каждой VLAN")
    + '<div class="vt1" style="left:845px;top:722px;width:3px;height:58px;background:#1a2a5a"></div>'
    + img("v_trunk1_cab.png", "left:903px;top:733px;width:151px")
    + box(1084, 724, 350, 60, "vt1-t", "<b style='font-size:22px'>Trunk:</b><br>один канал для нескольких VLAN") + '</div>',
    '<div class="step">' + box(205, 804, 1270, 58, "vt1-foot", "★&nbsp; Устройства одной VLAN на разных коммутаторах остаются в одном широковещательном домене.")
    + box(425, 870, 822, 46, "vt1-t", "<b style='color:#e08a00'>!</b>&nbsp; Native VLAN должна совпадать на обоих концах. Её тегирование зависит от настроек устройства.",
          "background:#fdf7e6;border:3px solid #1a2a5a;border-radius:8px;font-size:16px;line-height:40px;text-align:center") + '</div>',
])
