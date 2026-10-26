# -*- coding: utf-8 -*-
"""VLAN: процесс тегирования — добавление метки 802.1Q (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 100

CSS = """<style>
.vtp-b{position:absolute;box-sizing:border-box;border:4px solid #3a1606;box-shadow:5px 5px 0 #000}
.vtp-panel{background:#fff8ea}
.vtp-sub{background:#ffe14a;font:800 34px/54px "Golos Text",sans-serif;color:#2a1206;text-align:center}
.vtp-lab{color:#fff;font:800 34px/52px "Golos Text",sans-serif;text-align:center;border-color:#1a0a04}
.vtp-f{position:absolute;box-sizing:border-box;border:3px solid #3a1606;display:flex;align-items:center;justify-content:center;
  text-align:center;font:700 25px/1.1 "Golos Text",sans-serif;color:#1a0a1a}
.vtp-dm{background:#bcdcff}.vtp-sm{background:#bff0c0}.vtp-et{background:#d7c4ff}.vtp-da{background:#c9e2ff}.vtp-fc{background:#bff0c0}
.vtp-tg{background:#ff7a7a;color:#a00010}
.vtp-note{background:#fff0e0;font:700 25px/44px "Golos Text",sans-serif;text-align:center;color:#2a1206;border-radius:0}
.vtp-cal{background:#fff;border-color:#d3132a;color:#d3132a;font:700 23px/40px "Pixelify Sans",sans-serif;text-align:center}
.vtp-red{color:#d3132a;font:700 24px/1 "Golos Text",sans-serif;position:absolute}
.vtp-msg{background:#fff6dc;font:700 30px/1.25 "Golos Text",sans-serif;text-align:center;color:#1a0a04;padding-top:12px}
.vtp-msg b{color:#d3132a}
.vtp-grn{background:#3fae3a;color:#fff;font:700 31px/56px "Golos Text",sans-serif;text-align:center;border-color:#1c4a14}
.vtp-sm2{background:#fff;font:500 22px/36px "Golos Text",sans-serif;text-align:center;color:#1a0a04}
.vtp-arr{position:absolute;left:584px;top:300px;width:72px;height:78px}
.vtp-cab{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.vtp-pulse{animation:vtpp 1.4s ease-in-out infinite}
@keyframes vtpp{50%{transform:translateY(8px)}}
.vtp-fly{animation:vtpf 2.4s linear infinite}
@keyframes vtpf{0%{transform:translateX(0)}70%,100%{transform:translateX(150px);opacity:0}}
</style>"""

def b(x, y, w, h, cls, inner="", st=""):
    return '<div class="vtp-b %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)

def f(x, w, y, cls, t):
    return '<div class="vtp-f %s" style="left:%dpx;top:%dpx;width:%dpx;height:74px">%s</div>' % (cls, x, y, w, t)

def row(y, fields):
    return "".join(f(x, w, y, c, t) for x, w, c, t in fields)

ROW1 = [(292, 230, "vtp-dm", "Destination<br>MAC"), (522, 230, "vtp-sm", "Source<br>MAC"), (752, 213, "vtp-et", "EtherType"),
        (965, 490, "vtp-da", "Данные"), (1455, 152, "vtp-fc", "FCS")]
ROW2 = [(292, 230, "vtp-dm", "Destination<br>MAC"), (522, 168, "vtp-sm", "Source<br>MAC"), (690, 130, "vtp-tg", "TPID"),
        (820, 128, "vtp-tg", "TCI"), (948, 188, "vtp-et", "EtherType"), (1136, 319, "vtp-da", "Данные"), (1455, 152, "vtp-fc", "FCS")]

HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="step">' + b(545, 106, 582, 62, "vtp-sub", "Добавление метки 802.1Q") + '</div>',
    '<div class="step">' + b(45, 182, 1582, 120, "vtp-panel") + b(66, 203, 206, 60, "vtp-lab", "Без тега", "background:#2b6fd6")
    + row(207, ROW1) + '</div>',
    '<div class="step"><div class="vtp-pulse"><svg class="vtp-arr" viewBox="0 0 72 78"><path d="M24 0h24v40h20L36 76 4 40h20z" fill="#e8141e" stroke="#7a0008" stroke-width="3"/></svg></div>'
    + b(672, 316, 514, 46, "vtp-note", "Тег вставляется после Source MAC") + '</div>',
    '<div class="step">' + b(45, 378, 1582, 174, "vtp-panel") + b(66, 398, 206, 60, "vtp-lab", "С тегом", "background:#e01822")
    + row(403, ROW2)
    + b(668, 494, 132, 42, "vtp-cal", "0x8100") + b(842, 494, 136, 42, "vtp-cal", "VLAN ID")
    + '<svg class="vtp-cab"><path d="M684 542v12h137l8 8 8-8h138v-12" fill="none" stroke="#d3132a" stroke-width="4"/></svg>'
    + b(658, 562, 344, 42, "vtp-panel", '<div class="vtp-red" style="left:24px;top:6px">802.1Q: 32 бита = 4 байта</div>', "border-color:#3a1606") + '</div>',
    '<div class="step">' + img("v_tagproc_sw.png", "left:372px;top:628px;width:770px")
    + b(472, 572, 154, 44, "vtp-cal", "VLAN 10") + '</div>',
    '<div class="step">' + b(300, 732, 1098, 102, "vtp-msg",
      "Коммутатор определяет VLAN по входному порту.<br>Для передачи кадра с меткой <b>добавляется тег 802.1Q.</b>") + '</div>',
    '<div class="step">' + b(404, 824, 878, 58, "vtp-grn", "Тег указывает принадлежность кадра к VLAN.")
    + b(542, 880, 586, 42, "vtp-sm2", "При изменении кадра пересчитывается FCS.") + '</div>',
])
