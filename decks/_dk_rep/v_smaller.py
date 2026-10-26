# -*- coding: utf-8 -*-
"""VLAN: меньше домен — меньше лишнего трафика (сегменты за устройством L3) — вёрстка на чистом фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 182

CSS = """<style>
.vsm-p{position:absolute;background:#fdf6e3;border:5px solid #fff;outline:3px solid #3a1606;box-shadow:5px 5px 0 #000}
.vsm-s{position:absolute;left:322px;width:663px;border:2px dashed;border-radius:12px}
.vsm-tag{position:absolute;color:#fff;font:800 24px/1 "Golos Text",sans-serif;padding:8px 22px;border-radius:6px}
.vsm-ip{position:absolute;font:700 19px/1.1 "Golos Text",sans-serif;text-align:center;color:#111}
.vsm-ip i{font-style:normal;font-size:16px}
.vsm-bub{position:absolute;left:172px;top:262px;width:136px;background:#fff;border:3px solid #ff6a1a;border-radius:8px;
  font:700 18px/1.1 "Golos Text",sans-serif;text-align:center;color:#c0280e;padding:5px 2px}
.vsm-l3{position:absolute;left:146px;top:484px;width:148px;background:#14324e;color:#fff;font:700 21px/1.1 "Golos Text",sans-serif;text-align:center;padding:5px 0;border-radius:6px}
.vsm-c{position:absolute;left:1018px;width:522px;background:#fdf6e3;border:4px solid #fff;outline:3px solid #3a1606;box-shadow:5px 5px 0 #000}
.vsm-ib{position:absolute;left:1038px;width:125px;border-radius:8px}
.vsm-t{position:absolute;left:1190px;width:340px;font:800 29px/1.1 "Golos Text",sans-serif;color:#14324e}
.vsm-foot{position:absolute;left:300px;top:755px;width:1068px;height:110px;background:#2e8a2a;border:5px solid #0d3a12;box-shadow:5px 5px 0 #000}
.vsm-ft{position:absolute;left:445px;top:770px;font:800 34px/1.15 "Golos Text",sans-serif;color:#ffe14a;-webkit-text-stroke:1px #3a1606}
.vsm-info{position:absolute;left:330px;top:882px;width:1015px;height:42px;background:#fff;border:3px solid #0d3a12;font:600 17px/36px "Golos Text",sans-serif;white-space:nowrap;color:#14324e;padding-left:56px;box-sizing:border-box}
.vsm-svg{position:absolute;left:0;top:0;width:1672px;height:941px}
.vsm-svg path{fill:none;stroke-width:5}
.vsm-svg .ar{stroke:#ff6a1a;stroke-width:4;marker-end:url(#vsmm)}
.vsm-x{animation:vsmx 1s steps(2) infinite}
@keyframes vsmx{50%{transform:scale(1.2)}}
.vsm-e{animation:vsme 1.3s ease-in-out infinite}
@keyframes vsme{50%{transform:translateX(-8px)}}
</style>"""

SEG = [(215, 165, "#2e9e3a", "#eaf7e4", "Сегмент 1", 338),
       (395, 137, "#e0403a", "#fbe4e0", "Сегмент 2", 372),
       (548, 137, "#1f5ad8", "#e2effc", "Сегмент 3", 372)]


def svg():
    return ('<svg class="vsm-svg" viewBox="0 0 1672 941"><defs><marker id="vsmm" markerWidth="5" markerHeight="5" refX="3" refY="2.5" orient="auto">'
            '<path d="M0,0 L5,2.5 L0,5z" fill="#ff6a1a"/></marker></defs>'
            '<path stroke="#2e9e3a" d="M250 410 L290 398 L340 398 L340 325 L400 325 M480 325 L880 325"/>'
            '<path stroke="#e0403a" d="M262 438 L345 438 L345 492 L430 492 M515 475 L900 475"/>'
            '<path stroke="#1f5ad8" d="M255 462 L322 462 L322 640 L430 640 M515 625 L900 625"/>'
            '<path class="ar" d="M565 312 L492 312"/><path class="ar" d="M630 296 L685 296"/><path class="ar" d="M870 312 L770 312"/></svg>')


def seg(i):
    t, h, c, b, lab, tx = SEG[i]
    y = [325, 475, 625][i]
    pcs = (566, 698, 875) if i == 0 else (610, 745, 880)
    sw = "left:381px;top:288px;width:106px" if i == 0 else "left:420px;top:%dpx;width:106px" % (y - 25)
    extra = ""
    if i == 0:
        extra = ('<div class="vsm-ip" style="left:672px;top:230px">10.10.1.5<br><i>(отправитель)</i></div>'
                 '<div class="vsm-ip" style="left:848px;top:230px">10.10.1.6<br><i>(искомый узел)</i></div>'
                 + img("v_smaller_env.png", "left:596px;top:260px;width:42px", "ab vsm-e")
                 + img("v_smaller_env.png", "left:515px;top:280px;width:38px;filter:hue-rotate(25deg) saturate(.6)", "ab vsm-e")
                 + img("v_smaller_env.png", "left:812px;top:280px;width:38px;filter:hue-rotate(25deg) saturate(.6)", "ab vsm-e"))
    return ('<div class="step"><div class="vsm-tag" style="left:%dpx;top:%dpx;background:%s">%s</div>' % (tx, t + 12, c, lab)
            + img("v_smaller_sw.png", sw)
            + "".join(img("v_smaller_pc.png", "left:%dpx;top:%dpx;width:64px" % (x, y - 35 if i == 0 else y - 38)) for x in pcs)
            + extra + '</div>')


def card(y, h, ico, icol, txt):
    return ('<div class="step"><div class="vsm-c" style="top:%dpx;height:%dpx"></div>'
            '<div class="vsm-ib" style="top:%dpx;height:%dpx;background:%s"></div>%s'
            '<div class="vsm-t" style="top:%dpx">%s</div></div>' % (y, h, y + 12, h - 24, icol, ico, y + 28, txt))


HTML = CSS + bg("bgk_ground") + "".join([
    '<div class="vsm-p" style="left:132px;top:190px;width:870px;height:515px"></div>'
    + "".join('<div class="vsm-s" style="top:%dpx;height:%dpx;border-color:%s;background:%s"></div>' % (t, h, c, b) for t, h, c, b, _, _ in SEG)
    + svg() + img("v_smaller_r.png", "left:148px;top:398px;width:119px")
    + '<div class="vsm-l3">Устройство<br>L3</div>',
    seg(0), seg(1), seg(2),
    '<div class="step"><div class="vsm-bub">Broadcast дальше не проходит</div>'
    + img("v_smaller_x.png", "left:266px;top:378px;width:44px", "ab vsm-x") + '</div>',
    card(192, 130, img("v_smaller_i1.png", "left:1038px;top:205px;width:125px"), "#7fe0b0", "Рассылка ограничена одним сегментом"),
    card(338, 137, img("v_smaller_i2.png", "left:1038px;top:348px;width:125px"), "#fbd0c0", "Меньше устройств обрабатывают лишние кадры"),
    card(492, 140, img("v_smaller_i3.png", "left:1038px;top:503px;width:125px"), "#8fd8f5",
         "<span style='font-size:27px'>Снижается нагрузка на каналы и конечные узлы</span>"),
    '<div class="step"><div class="vsm-c" style="top:648px;height:90px;width:492px"></div>'
    + img("v_smaller_i4.png", "left:1036px;top:655px;width:102px")
    + '<div class="vsm-t" style="left:1155px;top:663px;font:600 23px/1.35 Golos Text,sans-serif">VLAN позволяют создать такое разделение <b style="color:#1f5ad8">логически</b></div></div>',
    '<div class="step"><div class="vsm-foot"></div>' + img("v_smaller_mush.png", "left:326px;top:772px;width:86px")
    + '<div class="vsm-ft">Разделение сети уменьшает область<br>распространения широковещательного трафика</div></div>',
    '<div class="step"><div class="vsm-info">Многоадресный трафик между сегментами передаётся только при настроенной multicast-маршрутизации.</div>'
    + img("v_smaller_info.png", "left:336px;top:883px;width:41px") + '</div>',
])
