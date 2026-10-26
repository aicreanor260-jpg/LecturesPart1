# -*- coding: utf-8 -*-
"""VLAN: растегирование — untagging (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 100

CSS = """<style>
.vut-b{position:absolute;box-sizing:border-box;border:4px solid #2a1a4a;box-shadow:5px 5px 0 #000;background:#fff8ea}
.vut-sub{background:#7a2fd0;border-color:#2a0a5a;color:#fff;font:800 38px/58px "Golos Text",sans-serif;text-align:center}
.vut-pill{position:absolute;box-sizing:border-box;border:3px solid #1a1a3a;font:800 22px/38px "Golos Text",sans-serif;text-align:center}
.vut-t{position:absolute;font:700 20px/1 "Golos Text",sans-serif;color:#1a1a3a}
.vut-ic{position:absolute;width:50px;height:50px;border-radius:50%;box-sizing:border-box;border:3px solid #1a1a1a;color:#fff;
  font:900 32px/44px "Golos Text",sans-serif;text-align:center}
.vut-f{position:absolute;box-sizing:border-box;border:3px solid #6a8ac8;display:flex;align-items:center;justify-content:center;
  text-align:center;font:600 20px/1.15 "Golos Text",sans-serif;color:#1a1a3a;height:64px}
.vut-lab{position:absolute;box-sizing:border-box;color:#fff;font:800 28px/54px "Golos Text",sans-serif;text-align:center;border:3px solid #1a1a3a}
.vut-card{font:800 27px/1.3 "Golos Text",sans-serif;color:#1a1a3a;padding:26px 0 0 126px}
.vut-card span{font-weight:700;font-size:25px}
.vut-ln{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.vut-env{animation:vute 2.4s ease-in-out infinite}
@keyframes vute{0%{transform:translateX(-40px);opacity:0}25%{opacity:1}80%,100%{transform:translateX(0);opacity:1}}
.vut-drop{animation:vutd 1.4s ease-in-out infinite}
@keyframes vutd{50%{transform:translateY(6px)}}
</style>"""


def b(x, y, w, h, cls="", inner="", st=""):
    return '<div class="vut-b %s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;%s">%s</div>' % (cls, x, y, w, h, st, inner)


def pill(x, y, w, s, bgc, fg, bc):
    return '<div class="vut-pill" style="left:%dpx;top:%dpx;width:%dpx;background:%s;color:%s;border-color:%s">%s</div>' % (x, y, w, bgc, fg, bc, s)


def t(x, y, s, st=""):
    return '<div class="vut-t" style="left:%dpx;top:%dpx;%s">%s</div>' % (x, y, st, s)


def fields(y, row):
    return "".join('<div class="vut-f" style="left:%dpx;top:%dpx;width:%dpx;background:%s">%s</div>' % (x, y, w, c, s) for x, w, c, s in row)


BEFORE = [(366, 160, "#d6e8ff", "Destination<br>MAC"), (526, 125, "#d6e8ff", "Source<br>MAC"), (651, 84, "#ff8a8a", "TPID"),
          (735, 85, "#ff8a8a", "TCI"), (820, 150, "#d6e8ff", "EtherType"), (970, 334, "#e6d6ff", "Данные"), (1304, 110, "#e8f0ff", "FCS1")]
AFTER = [(387, 175, "#d6e8ff", "Destination<br>MAC"), (562, 152, "#d6e8ff", "Source<br>MAC"), (714, 216, "#d6e8ff", "EtherType"),
         (930, 357, "#e6d6ff", "Данные"), (1287, 128, "#ffe14a", "<b>FCS2</b>")]

HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="step">' + b(518, 108, 636, 62, "vut-sub", "Растегирование — untagging", "background:#7a2fd0") + '</div>',
    '<div class="step">' + b(228, 184, 1216, 652, "", "", "background:rgba(255,248,234,.96)")
    + pill(294, 240, 134, "VLAN 10", "#e8141e", "#fff", "#7a0008")
    + '<div class="vut-env" style="position:absolute;left:298px;top:288px">' + img("v_untag_env.png", "position:static;width:124px") + '</div>'
    + '<svg class="vut-ln"><path d="M436 332h34" stroke="#e8141e" stroke-width="10"/><path d="M466 316l26 16-26 16z" fill="#e8141e"/></svg>'
    + img("v_untag_sw.png", "left:508px;top:263px;width:289px") + '</div>',
    '<div class="step"><svg class="vut-ln"><path d="M792 300h22v-56h34" fill="none" stroke="#e8141e" stroke-width="4"/><path d="M846 236l14 8-14 8z" fill="#e8141e"/>'
    '<path d="M1134 244h40" stroke="#e8141e" stroke-width="4"/><path d="M1172 236l14 8-14 8z" fill="#e8141e"/>'
    '<path d="M1266 248h30" stroke="#a06aa0" stroke-width="4"/><path d="M1294 240l14 8-14 8z" fill="#a06aa0"/></svg>'
    + '<div class="vut-ic" style="left:870px;top:222px;background:#2fae3a">✓</div>'
    + pill(928, 212, 204, "Access VLAN 10", "#ffd6d6", "#1a1a3a", "#e8141e")
    + t(932, 268, "Удаление тега 802.1Q", "font-size:18px") + img("v_untag_env2.png", "left:1186px;top:220px;width:78px")
    + img("v_untag_pc.png", "left:1303px;top:203px;width:109px") + '</div>',
    '<div class="step"><svg class="vut-ln"><path d="M792 330h80M800 360h12v56h60" fill="none" stroke="#1f5fe0" stroke-width="4"/>'
    '<path d="M870 322l14 8-14 8zM870 408l14 8-14 8z" fill="#1f5fe0"/></svg>'
    + '<div class="vut-ic" style="left:900px;top:304px;background:#e8141e">✕</div><div class="vut-ic" style="left:900px;top:392px;background:#e8141e">✕</div>'
    + pill(958, 304, 140, "VLAN 20", "#cfe0ff", "#1a1a3a", "#1f5fe0") + pill(958, 392, 140, "VLAN 20", "#cfe0ff", "#1a1a3a", "#1f5fe0")
    + t(962, 356, "Не передаётся в другую VLAN", "font-size:18px") + t(962, 444, "Не передаётся в другую VLAN", "font-size:18px") + '</div>',
    '<div class="step"><div class="vut-lab" style="left:255px;top:494px;width:100px;background:#6a1fc0">До:</div>'
    + fields(488, BEFORE) + '</div>',
    '<div class="step"><div class="vut-drop" style="position:absolute;left:698px;top:560px"><svg width="34" height="44"><path d="M12 0h10v26h12L17 44 0 26h12z" fill="#8a3ad8"/></svg></div>'
    + t(760, 574, "Тег удалён — FCS пересчитана", "font-size:23px")
    + '<div class="vut-lab" style="left:256px;top:618px;width:118px;background:#1a9a9a">После:</div>'
    + fields(612, AFTER) + '</div>',
    '<div class="step">' + b(250, 700, 580, 122, "vut-card", "Untagging <span>— удаление<br>метки 802.1Q из Ethernet-кадра.</span>",
                             "background:#ddf8fb;border-color:#1a9aa8")
    + img("v_untag_mush.png", "left:266px;top:720px;width:91px")
    + b(846, 700, 576, 122, "vut-card", "Отсутствие разрешения VLAN —<br><span style=\"font-size:21px\">причина фильтрации, а не дефект кадра.</span>",
        "background:#f0e0ff;border-color:#8a3ad8;padding-left:130px;font-size:25px")
    + img("v_untag_star.png", "left:863px;top:720px;width:97px") + '</div>',
    '<div class="step">' + b(210, 846, 818, 66, "", "", "background:#2f8a2a;border-color:#1c4a14")
    + t(314, 868, "Цвета условны. VLAN определяется числовым VLAN ID.", "color:#fff;font-size:24px")
    + img("v_untag_fl.png", "left:236px;top:848px;width:61px")
    + b(1046, 846, 416, 66, "", "", "background:#fff")
    + t(1122, 870, "На tagged-портах метка сохраняется.", "font-size:18px;font-weight:600")
    + img("v_untag_warn.png", "left:1063px;top:856px;width:49px") + '</div>',
])
