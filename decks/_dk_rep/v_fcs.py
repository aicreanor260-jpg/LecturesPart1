# -*- coding: utf-8 -*-
"""VLAN: пересчёт FCS и передача в зоне VLAN (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 90

CSS = """<style>
.vfc-b{position:absolute;box-sizing:border-box;border:4px solid #1b2f6b;box-shadow:5px 5px 0 #000}
.vfc-panel{background:#fff8ea}
.vfc-sub{background:#fff;font:800 34px/54px "Golos Text",sans-serif;color:#13245a;text-align:center;border-color:#13245a}
.vfc-h{position:absolute;font:800 27px/1 "Golos Text",sans-serif;color:#13245a}
.vfc-f{position:absolute;box-sizing:border-box;border:3px solid #1b2f6b;display:flex;align-items:center;justify-content:center;
  text-align:center;font:600 23px/1.1 "Golos Text",sans-serif;color:#13245a;height:78px;top:230px}
.vfc-t{position:absolute;font:500 21px/1.25 "Golos Text",sans-serif;color:#13245a}
.vfc-y{background:#ffe14a;border-color:#c48a00;text-align:center;font:800 19px/1.15 "Golos Text",sans-serif;color:#2a1206;padding-top:6px}
.vfc-z{background:#eaf6ff;border-color:#9cc8ef}
.vfc-tag{background:#fff;font:700 19px/1.1 "Golos Text",sans-serif;color:#13245a;text-align:center;padding-top:6px;border-width:3px;box-shadow:none}
.vfc-pill{position:absolute;background:#ffe14a;border:2px solid #c48a00;font:700 17px/26px "Golos Text",sans-serif;padding:0 8px}
.vfc-btm{font:700 27px/1.2 "Golos Text",sans-serif;color:#13245a;text-align:center;display:flex;align-items:center;justify-content:center}
.vfc-ln{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.vfc-dash{stroke-dasharray:22 12;animation:vfcd 1s linear infinite}
@keyframes vfcd{to{stroke-dashoffset:-34}}
.vfc-go{animation:vfcg 3s ease-in-out infinite}
@keyframes vfcg{0%{transform:translateX(-90px);opacity:0}15%{opacity:1}85%{opacity:1}100%{transform:translateX(150px);opacity:0}}
.vfc-glow{animation:vfcs 1.6s ease-in-out infinite}
@keyframes vfcs{50%{box-shadow:0 0 24px 8px #ffd400,5px 5px 0 #000}}
</style>"""

def b(x, y, w, h, cls, inner="", st=""):
    return '<div class="vfc-b %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)

def t(x, y, cls, s, st=""):
    return '<div class="%s" style="left:%dpx;top:%dpx;%s">%s</div>' % (cls, x, y, st, s)

FIELDS = [(90, 191, "#cfe6ff", "Destination<br>MAC"), (281, 146, "#c9f0dc", "Source<br>MAC"), (427, 92, "#e8141e", "TPID"),
          (519, 91, "#e8141e", "TCI"), (610, 142, "#dccbff", "EtherType"), (752, 252, "#ffd6dc", "Данные")]

HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="step">' + b(464, 94, 744, 56, "vfc-sub", "Пересчёт FCS и передача в зоне VLAN") + '</div>',
    '<div class="step">' + b(66, 165, 1538, 232, "vfc-panel")
    + t(112, 182, "vfc-h", "Структура кадра после добавления тега")
    + "".join('<div class="vfc-f" style="left:%dpx;width:%dpx;background:%s;%s">%s</div>'
              % (x, w, c, "color:#fff;font-weight:800" if c == "#e8141e" else "", s) for x, w, c, s in FIELDS)
    + '<svg class="vfc-ln"><path d="M428 316v12h86l7 8 7-8h82v-12" fill="none" stroke="#d3132a" stroke-width="4"/></svg>'
    + t(414, 344, "vfc-t", "Тег 802.1Q — 4 байта", "position:absolute;color:#d3132a;font-weight:700") + '</div>',
    '<div class="step">' + b(1006, 230, 134, 78, "vfc-y vfc-glow", '<div style="font:800 25px/64px Golos Text,sans-serif">FCS1</div>', "padding:0")
    + '<svg class="vfc-ln"><path d="M1073 336v-22m-10 12l10-12 10 12" fill="none" stroke="#c48a00" stroke-width="4"/></svg>'
    + b(956, 336, 232, 58, "vfc-y", "Новое значение<br>контрольной суммы") + '</div>',
    '<div class="step">' + b(1163, 196, 422, 166, "vfc-z", "", "box-shadow:none;border-width:3px")
    + img("v_fcs_gear.png", "left:1183px;top:207px;width:69px")
    + t(1268, 226, "vfc-h", "FCS → пересчёт → FCS1", "position:absolute;font-size:24px")
    + t(1186, 278, "vfc-t", "После добавления тега изменилось<br>содержимое кадра — FCS вычисляется<br>&nbsp;&nbsp;заново.", "position:absolute") + '</div>',
    '<div class="step">' + b(70, 418, 1530, 300, "vfc-z", "", "background:rgba(234,246,255,.95)")
    + t(0, 428, "vfc-h", "Зона VLAN — VLAN-enabled area", "position:absolute;width:1672px;text-align:center;font-size:40px")
    + t(0, 474, "vfc-t", "Условная схема обработки и передачи", "position:absolute;width:1672px;text-align:center;font-weight:700")
    + '<svg class="vfc-ln"><path d="M238 603h64" stroke="#e8141e" stroke-width="5"/>'
      '<path class="vfc-dash" d="M578 603h340" stroke="#e8141e" stroke-width="8"/><path d="M915 590l28 13-28 13z" fill="#e8141e"/>'
      '<path d="M1230 578l158-40" stroke="#e8141e" stroke-width="5"/><path d="M1388 538l-18-6 4 18z M1226 580l20-8-4 18z" fill="#e8141e"/>'
      '<path d="M1226 606l140 20" stroke="#1f5fe0" stroke-width="5"/><path d="M1370 627l-18-12-2 18z" fill="#1f5fe0"/></svg>'
    + img("v_fcs_pc1.png", "left:118px;top:550px;width:124px") + img("v_fcs_sw1.png", "left:300px;top:548px;width:278px")
    + img("v_fcs_sw2.png", "left:952px;top:548px;width:274px") + img("v_fcs_srv.png", "left:1388px;top:480px;width:140px")
    + img("v_fcs_pc2.png", "left:1362px;top:588px;width:100px")
    + b(130, 652, 98, 46, "vfc-tag", "ПК<br>VLAN 10", "font-size:17px;padding-top:2px")
    + b(356, 648, 164, 36, "vfc-tag", "Коммутатор 1", "padding-top:4px")
    + b(680, 630, 184, 38, "vfc-tag", "Trunk, VLAN 10", "padding-top:5px")
    + b(1008, 648, 164, 36, "vfc-tag", "Коммутатор 2", "padding-top:4px")
    + b(1226, 634, 112, 58, "vfc-tag", "Access<br>VLAN 10", "border-color:#1f5fe0;font-size:17px")
    + b(1356, 670, 94, 46, "vfc-tag", "ПК<br>VLAN 10", "font-size:17px;padding-top:2px")
    + b(1218, 484, 146, 54, "vfc-tag", "Тегированный<br>кадр", "background:#ffe3e3;border-color:#e8141e;font-size:17px")
    + b(1460, 598, 196, 60, "vfc-tag", "При снятии тега<br>FCS пересчитывается", "background:#fff4d0;border-color:#c48a00;font-size:15px;padding-top:9px")
    + '<div class="vfc-go" style="position:absolute;left:688px;top:530px;width:170px;height:70px">'
    + img("v_fcs_env.png", "left:0;top:14px;width:82px")
    + '<div class="vfc-pill" style="left:36px;top:0;background:#e8141e;color:#fff;border-color:#8a0010">VID 10</div>'
    + '<div class="vfc-pill" style="left:98px;top:28px">FCS1</div></div></div>',
    '<div class="step">' + b(216, 736, 610, 92, "vfc-btm", "Кадр передаётся через порты,<br>разрешённые для его VLAN", "background:#ffecea;border-color:#c0382b;padding-left:110px")
    + img("v_fcs_q.png", "left:242px;top:748px;width:70px")
    + b(846, 736, 610, 92, "vfc-btm", "Формат кадра на выходе<br>зависит от настройки порта", "background:#ece4ff;border-color:#4a2a9a;padding-left:110px")
    + img("v_fcs_gear2.png", "left:900px;top:748px;width:75px") + '</div>',
    '<div class="step">' + b(262, 846, 1148, 74, "vfc-btm", "После изменения кадра его FCS должна соответствовать новому содержимому.", "background:#f2ffe6;border-color:#2a7a1e;padding-left:80px;font-size:24px")
    + img("v_fcs_ok.png", "left:298px;top:855px;width:56px") + '</div>',
])
