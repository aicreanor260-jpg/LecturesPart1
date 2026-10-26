# -*- coding: utf-8 -*-
"""VLAN: копирование широковещательного кадра в пределах VLAN 10 (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 108

CSS = """<style>
.vbc-b{position:absolute;box-sizing:border-box;border:4px solid #13245a;box-shadow:5px 5px 0 #000;background:#fff8ea}
.vbc-sub{background:#fff1b8;font:800 32px/50px "Golos Text",sans-serif;color:#13245a;text-align:center}
.vbc-t{position:absolute;font:700 22px/1.15 "Golos Text",sans-serif;color:#13245a;text-align:center}
.vbc-sw{background:#d6dbe4;border-color:#3a4250;clip-path:polygon(0 30px,30px 0,calc(100% - 30px) 0,100% 30px,100% 100%,0 100%);box-shadow:none}
.vbc-port{position:absolute;width:44px;height:58px;box-sizing:border-box;border:4px solid #1a1a1a}
.vbc-ok,.vbc-no{position:absolute;width:52px;height:52px;border-radius:50%;box-sizing:border-box;border:3px solid #fff;
  box-shadow:0 0 0 3px #1a1a1a;color:#fff;font:900 34px/46px "Golos Text",sans-serif;text-align:center}
.vbc-ok{background:#2fae3a}.vbc-no{background:#e8141e}
.vbc-pill{position:absolute;box-sizing:border-box;font:800 21px/34px "Golos Text",sans-serif;padding:0 12px;border-radius:8px}
.vbc-f{position:absolute;top:666px;height:72px;box-sizing:border-box;border:3px solid #13245a;display:flex;flex-direction:column;
  align-items:center;justify-content:center;font:600 21px/1.15 "Golos Text",sans-serif;color:#13245a;text-align:center}
.vbc-f small{font-size:16px;font-weight:500}
.vbc-h{color:#fff;font:800 32px/62px "Golos Text",sans-serif;text-align:center}
.vbc-side{position:absolute;font:800 26px/1.2 "Golos Text",sans-serif;color:#13245a}
.vbc-grn{background:#3fae3a;border-color:#1c4a14;color:#fff;font:800 33px/1.15 "Golos Text",sans-serif;text-align:center;padding-top:12px}
.vbc-grn b{color:#ffe14a}
.vbc-ln{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.vbc-d{stroke-dasharray:10 8;animation:vbcd .9s linear infinite;fill:none;stroke-width:4}
@keyframes vbcd{to{stroke-dashoffset:-36}}
.vbc-pop{animation:vbcp 1.6s ease-in-out infinite}
@keyframes vbcp{50%{transform:translateX(10px)}}
</style>"""


def b(x, y, w, h, cls="", inner="", st=""):
    return '<div class="vbc-b %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def pill(x, y, s, bgc, fg="#fff", st=""):
    return '<div class="vbc-pill" style="left:%dpx;top:%dpx;background:%s;color:%s;%s">%s</div>' % (x, y, bgc, fg, st, s)


def port(x, y, c):
    return '<div class="vbc-port" style="left:%dpx;top:%dpx;background:%s"></div>' % (x, y, c)


FR = [(217, 218, "#d8e9ff", "Destination MAC", "FF:FF:FF:FF:FF:FF"), (435, 212, "#d5f0dc", "Source MAC", "AA:BB:CC:DD:EE:FF"),
      (647, 110, "#e8141e", "TPID", "0x8100"), (757, 90, "#e8141e", "TCI", ""), (847, 166, "#fff0cc", "EtherType", "0x0800"),
      (1013, 308, "#ffdfe2", "Данные", ""), (1321, 134, "#e3ebf5", "FCS1", "")]

TAGGED = "border:2px solid #e86b6b;font-size:18px;line-height:30px"

HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="step">' + b(456, 116, 760, 52, "vbc-sub", "Копирование широковещательного кадра") + '</div>',
    '<div class="step">' + b(62, 180, 1236, 454, "", "", "background:rgba(255,248,234,.96)")
    + img("v_bcast10_env.png", "left:105px;top:312px;width:243px")
    + b(74, 464, 320, 64, "", '<div class="vbc-t" style="position:static;font-size:25px;font-weight:800">Широковещательный<br>кадр</div>', "background:#ffe0e0;border:0;box-shadow:none")
    + b(96, 536, 280, 68, "", '<div class="vbc-t" style="position:static;padding-top:4px;font-size:23px;font-weight:600">MAC назначения:<br>FF:FF:FF:FF:FF:FF</div>', "background:#e6eaf2;border:0;box-shadow:none")
    + '<svg class="vbc-ln"><path d="M358 392h90" stroke="#e8141e" stroke-width="12"/><path d="M446 370l34 22-34 22z" fill="#e8141e"/></svg></div>',
    '<div class="step">' + b(490, 228, 470, 372, "vbc-sw")
    + '<div class="vbc-t" style="left:490px;top:272px;width:470px;font-size:28px;font-weight:800">Коммутатор</div>'
    + pill(504, 330, "VLAN 10", "#e8141e") + port(508, 370, "#c8101a")
    + b(632, 334, 180, 156, "", '<div class="vbc-t" style="position:static;padding-top:24px;font-weight:600">Копирование<br>кадра<br>в пределах<br>VLAN 10</div>',
        "background:#ffe8e8;border:3px dashed #e86b6b;box-shadow:none")
    + '<svg class="vbc-ln"><path class="vbc-d" d="M578 398h44M540 500v-54" stroke="#e8141e"/><path d="M616 390l12 8-12 8zM532 452l8-12 8 12z" fill="#e8141e"/>'
      '<path class="vbc-d" d="M814 370l90-62M814 386h90" stroke="#e8141e"/><path class="vbc-d" d="M814 412l84 52M814 430l84 110" stroke="#1f5fe0"/></svg>'
    + b(430, 516, 254, 64, "", '<div class="vbc-t" style="position:static;padding-top:4px;font-weight:700">Назад во входной<br>порт не отправляется</div>', "background:#ffe8ec;border:0;box-shadow:none")
    + '</div>',
    '<div class="step">' + port(916, 280, "#c8101a") + port(916, 362, "#c8101a")
    + '<div class="vbc-ok" style="left:976px;top:283px">✓</div><div class="vbc-ok" style="left:976px;top:374px">✓</div>'
    + pill(968, 240, "Tagged, VLAN 10", "#fff", "#13245a", TAGGED) + pill(968, 338, "Tagged, VLAN 10", "#fff", "#13245a", TAGGED)
    + '<div class="vbc-pop" style="position:absolute;left:0;top:0">'
    + '<svg class="vbc-ln"><path d="M1040 305h70M1040 398h70" stroke="#e8141e" stroke-width="10"/><path d="M1104 290l26 15-26 15zM1104 383l26 15-26 15z" fill="#e8141e"/></svg>'
    + img("v_bcast10_env2.png", "left:1138px;top:260px;width:134px") + img("v_bcast10_env2.png", "left:1138px;top:354px;width:134px") + '</div></div>',
    '<div class="step">' + port(916, 444, "#1f4fd0") + port(916, 520, "#1f4fd0")
    + '<div class="vbc-no" style="left:978px;top:446px">✕</div><div class="vbc-no" style="left:978px;top:522px">✕</div>'
    + pill(1042, 454, "VLAN 20", "#1f4fd0") + pill(1042, 530, "VLAN 20", "#1f4fd0") + '</div>',
    '<div class="step">' + b(1312, 180, 336, 236, "", "", "background:#ffe8ec")
    + b(1322, 190, 316, 56, "vbc-h", "Красные порты:", "background:#e8141e;border:0;box-shadow:none;line-height:56px")
    + '<div class="vbc-ok" style="left:1334px;top:276px;width:70px;height:70px;font-size:46px;line-height:64px">✓</div>'
    + '<div class="vbc-side" style="left:1414px;top:266px">VLAN 10<br>разрешена —<br><span style="font-size:23px;font-weight:600">копия передаётся.</span></div>'
    + b(1312, 432, 336, 204, "", "", "background:#e6f0ff")
    + b(1322, 442, 316, 56, "vbc-h", "Синие порты:", "background:#1f4fd0;border:0;box-shadow:none;line-height:56px")
    + '<div class="vbc-no" style="left:1334px;top:522px;width:70px;height:70px;font-size:46px;line-height:64px">✕</div>'
    + '<div class="vbc-side" style="left:1424px;top:518px">VLAN 20 —<br>копия не<br>передаётся.</div></div>',
    '<div class="step">' + b(188, 650, 1294, 136)
    + "".join('<div class="vbc-f" style="left:%dpx;width:%dpx;background:%s;%s">%s%s</div>'
              % (x, w, c, "color:#fff;font-weight:800" if c == "#e8141e" else "", n, ("<small>%s</small>" % v) if v else "") for x, w, c, n, v in FR)
    + '<svg class="vbc-ln"><path d="M652 744v8h90l7 8 7-8h84v-8" fill="none" stroke="#d3132a" stroke-width="4"/></svg>'
    + '<div class="vbc-t" style="left:690px;top:762px;color:#d3132a;font-size:19px">Тег 802.1Q</div></div>',
    '<div class="step">' + b(196, 800, 1284, 110, "vbc-grn", "<b>Broadcast</b> передаётся во все разрешённые порты той же VLAN,<br>кроме входного.", "padding-left:80px")
    + img("v_bcast10_star.png", "left:228px;top:812px;width:80px") + '</div>',
])
