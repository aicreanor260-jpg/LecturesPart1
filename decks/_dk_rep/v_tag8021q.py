# -*- coding: utf-8 -*-
"""VLAN: тегирование кадров Ethernet — IEEE 802.1Q (нетегированный/тегированный кадр) — вёрстка на чистом фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.vtq-p{position:absolute;border:4px solid #3a1606;box-shadow:5px 5px 0 #000}
.vtq-d{font:600 28px/1.22 "Golos Text",sans-serif;color:#14324e;padding:10px 32px;box-sizing:border-box}
.vtq-d b{color:#c8102e;font-weight:800}.vtq-d b.big{font-size:38px}
.vtq-lb{position:absolute;left:113px;width:374px;height:44px;background:#14324e;color:#fff;font:800 27px/44px "Golos Text",sans-serif;padding-left:28px;box-sizing:border-box}
.vtq-row{position:absolute;left:106px;width:1459px;height:75px;display:flex;border:4px solid #14324e;box-shadow:4px 4px 0 #000;box-sizing:border-box}
.vtq-row div{border-right:3px solid #14324e;font:800 25px/1.05 "Golos Text",sans-serif;color:#14324e;text-align:center;display:flex;flex-direction:column;justify-content:center}
.vtq-row div:last-child{border-right:0}
.vtq-row small{font:700 20px/1.2 "Golos Text",sans-serif;margin-top:3px}
.vtq-row .tg{background:#ffd84a;outline:4px solid #3a1606;font-size:30px;position:relative;z-index:1}
.vtq-y{position:absolute;left:730px;top:415px;width:495px;height:45px;background:#ffe14a;border:4px solid #3a1606;font:800 23px/37px "Golos Text",sans-serif;text-align:center;color:#3a1606}
.vtq-z{position:absolute;left:532px;top:598px;width:608px;height:182px;background:#fff3b8;border:4px dashed #e0a800;border-radius:14px}
.vtq-f{position:absolute;top:614px;height:104px;background:#ffd84a;border:4px solid #3a1606;border-radius:6px;text-align:center;font:800 27px/1 "Golos Text",sans-serif;color:#14324e;padding-top:12px;box-sizing:border-box}
.vtq-f span{display:block;margin:10px 20px 0;background:#fff3c8;border-radius:6px;font:600 24px/38px "Golos Text",sans-serif}
.vtq-f span.s{font-size:19px;line-height:1.1;padding:3px 0}
.vtq-eq{position:absolute;left:532px;top:730px;width:608px;text-align:center;font:800 31px/1 "Golos Text",sans-serif;color:#14324e}
.vtq-bt{position:absolute;left:262px;top:800px;width:1148px;height:105px;background:#d8f5b0;border:4px solid #3a1606;box-shadow:5px 5px 0 #000}
.vtq-t{position:absolute;font:700 26px/1.3 "Golos Text",sans-serif;color:#14324e}
.vtq-svg{position:absolute;left:0;top:0;width:1672px;height:941px}
.vtq-arr{animation:vtqa 1s ease-in-out infinite}
@keyframes vtqa{50%{transform:translateY(8px)}}
</style>"""


def row(top, cells):
    return ('<div class="vtq-row" style="top:%dpx">' % top
            + "".join('<div class="%s" style="width:%dpx;background:%s">%s</div>' % (k, w, c, t) for w, c, t, k in cells) + '</div>')


B, G, P, V = "#a8dcf2", "#a8ecd0", "#f8a8cc", "#c8b8f4"
U = [(284, B, "Destination MAC<small>6 байт</small>", ""), (270, G, "Source MAC<small>6 байт</small>", ""),
     (178, P, "EtherType<small>2 байта</small>", ""), (535, V, "Данные", ""), (192, B, "FCS<small>4 байта</small>", "")]
T = [(282, B, "Destination MAC<small>6 байт</small>", ""), (240, G, "Source MAC<small>6 байт</small>", ""),
     (242, "#ffd84a", "Тег 802.1Q<small>4 байта</small>", "tg"), (182, P, "EtherType<small>2 байта</small>", ""),
     (321, V, "Данные", ""), (192, B, "FCS<small>4 байта</small>", "")]

HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="step"><div class="vtq-p vtq-d" style="left:200px;top:160px;width:1010px;height:102px;background:#fdf6e3">'
    '<b class="big">Тегирование</b> — добавление в кадр <b>Ethernet</b> метки 802.1Q, которая указывает принадлежность кадра к VLAN.</div>'
    '<div class="vtq-p" style="left:1228px;top:160px;width:302px;height:102px;background:#ead8f8"></div>'
    + img("v_tag8021q_tag.png", "left:1238px;top:178px;width:76px")
    + '<div class="vtq-t" style="left:1330px;top:180px;color:#3a2a80">tag —<br>метка, ярлык</div></div>',
    '<div class="step"><div class="vtq-lb" style="top:280px">Нетегированный кадр</div>' + row(322, U) + '</div>',
    '<div class="step"><div class="vtq-arr">' + img("v_tag8021q_arr.png", "left:650px;top:403px;width:72px") + '</div>'
    '<div class="vtq-y">Добавляем метку после Source MAC</div></div>',
    '<div class="step"><div class="vtq-lb" style="top:443px">Тегированный кадр</div>' + row(487, T) + '</div>',
    '<div class="step"><svg class="vtq-svg" viewBox="0 0 1672 941"><path d="M630 562 L540 600 M870 562 L1130 600" stroke="#3a1606" stroke-width="4" stroke-dasharray="10 6" fill="none"/></svg>'
    '<div class="vtq-z"></div>'
    '<div class="vtq-f" style="left:552px;width:276px">TPID — 16 бит<span>0x8100</span></div>'
    '<div class="vtq-f" style="left:838px;width:284px">TCI — 16 бит<span class="s">Приоритет и<br>идентификатор VLAN</span></div>'
    '<div class="vtq-eq">16 + 16 = 32 бита = 4 байта</div></div>',
    '<div class="step"><div class="vtq-bt"></div>' + img("v_tag8021q_ok.png", "left:298px;top:812px;width:82px")
    + '<div class="vtq-t" style="left:398px;top:816px">С меткой 802.1Q — тегированный кадр.<br>Без метки — нетегированный.</div>'
    '<div style="position:absolute;left:940px;top:815px;height:72px;border-left:3px solid #3a1606"></div>'
    + img("v_tag8021q_bulb.png", "left:958px;top:812px;width:64px")
    + '<div class="vtq-t" style="left:1035px;top:810px;font-size:22px">Метка позволяет различать<br>трафик разных VLAN<br>в общем канале.</div></div>',
])
