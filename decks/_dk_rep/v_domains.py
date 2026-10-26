# -*- coding: utf-8 -*-
"""VLAN: сеть делится на отдельные широковещательные домены — вёрстка на чистом фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 140

CSS = """<style>
.vdm-p{position:absolute;background:#fdf6e3;border:5px solid #fff;outline:3px solid #3a1606;box-shadow:5px 5px 0 #000}
.vdm-v{position:absolute;left:395px;width:743px;border:3px solid;border-radius:14px}
.vdm-tag{position:absolute;left:410px;color:#fff;font:800 28px/1 "Golos Text",sans-serif;padding:7px 24px;border-radius:6px}
.vdm-lb{position:absolute;left:432px;width:186px;background:#fff;border:3px solid #14324e;border-radius:6px;font:700 20px/30px "Golos Text",sans-serif;text-align:center;color:#14324e}
.vdm-dn{position:absolute;font:700 20px/1 "Golos Text",sans-serif;white-space:nowrap}
.vdm-ip{position:absolute;font:700 19px/1 "Golos Text",sans-serif;color:#111}
.vdm-bub{position:absolute;background:#fff5c8;border:3px solid #3a1606;border-radius:10px;font:700 21px/1.25 "Golos Text",sans-serif;color:#14324e;padding:8px 14px;text-align:center}
.vdm-n{position:absolute;left:1200px;width:72px;height:72px;border-radius:12px;color:#fff;font:800 46px/72px "Golos Text",sans-serif;text-align:center}
.vdm-t{position:absolute;left:1300px;width:325px;font:700 26px/1.25 "Golos Text",sans-serif;color:#14324e}
.vdm-sep{position:absolute;left:1200px;width:415px;border-top:3px dashed #9cc7e6}
.vdm-foot{position:absolute;left:315px;top:775px;width:1040px;height:92px;background:#1f7a2a;border:5px solid #0d3a12;box-shadow:5px 5px 0 #000}
.vdm-ft{position:absolute;left:470px;top:786px;width:860px;font:800 30px/1.25 "Golos Text",sans-serif;color:#fff;text-align:center}
.vdm-ft b{color:#ffe14a}
.vdm-sub{position:absolute;left:335px;top:868px;width:1000px;height:44px;background:#fff;border:3px solid #0d3a12;font:600 18px/38px "Golos Text",sans-serif;text-align:center;color:#14324e}
.vdm-svg{position:absolute;left:0;top:0;width:1672px;height:941px}
.vdm-svg path{fill:none;stroke-width:5}
.vdm-svg .fl{stroke:#f5a623;stroke-width:3;stroke-dasharray:7 6;animation:vdmd 1s linear infinite;marker-end:url(#vdmm)}
@keyframes vdmd{to{stroke-dashoffset:-26}}
.vdm-e{animation:vdme 1.4s ease-in-out infinite}
@keyframes vdme{50%{transform:translateY(-6px)}}
</style>"""

ROWS = [  # (top, h, цвет, фон, метка, y линии, y подписи, текст домена, x домена)
    (185, 192, "#2e9e3a", "#eaf7e4", "VLAN 10", 278, 348, "#2e9e3a", 558),
    (397, 163, "#e0403a", "#fbe4e0", "VLAN 20", 465, 528, "#e0403a", 670),
    (580, 160, "#1f7ae0", "#e2effc", "VLAN 30", 652, 710, "#1f7ae0", 670),
]


def svg():
    s = ('<svg class="vdm-svg" viewBox="0 0 1672 941"><defs><marker id="vdmm" markerWidth="5" markerHeight="5" refX="3" refY="2.5" orient="auto">'
         '<path d="M0,0 L5,2.5 L0,5z" fill="#f5a623"/></marker></defs>'
         '<path stroke="#2e9e3a" d="M240 400 L340 360 L340 278 L470 278"/>'
         '<path stroke="#e0403a" d="M240 432 L340 432 L340 470 L470 470"/>'
         '<path stroke="#1f7ae0" d="M240 465 L302 465 L302 655 L470 655"/>')
    for _, _, c, _, _, y, _, _, _ in ROWS:
        s += '<path stroke="%s" d="M590 %d L1060 %d"/>' % (c, y, y)
    s += ('<path class="fl" d="M600 255 Q670 225 740 238"/><path class="fl" d="M770 255 Q840 225 905 238"/>'
          '<path class="fl" d="M925 255 Q990 225 1030 258"/>')
    return s + "</svg>"


boxes = "".join(
    '<div class="vdm-v" style="top:%dpx;height:%dpx;border-color:%s;background:%s"></div>'
    '<div class="vdm-tag" style="top:%dpx;background:%s">%s</div>' % (t, h, c, b, t - 10, c, lab)
    for t, h, c, b, lab, *_ in ROWS)


def row(i):
    t, h, c, b, lab, y, dy, dc, dx = ROWS[i]
    return ('<div class="step">'
            + img("v_domains_sw.png", "left:456px;top:%dpx;width:144px" % (y - 42))
            + '<div class="vdm-lb" style="top:%dpx">L2-коммутатор</div>' % (y + 25)
            + "".join(img("v_domains_pc.png", "left:%dpx;top:%dpx;width:64px" % (x, y - 30)) for x in (716, 866, 1036))
            + '<div class="vdm-dn" style="left:%dpx;top:%dpx;color:%s">Отдельный широковещательный домен</div>' % (dx, dy, dc)
            + ('<div class="vdm-ip" style="left:702px;top:320px">10.10.1.5</div><div class="vdm-ip" style="left:852px;top:320px">10.10.1.6</div>'
               '<div class="vdm-bub" style="left:755px;top:160px">ARP: у кого IP 10.10.1.6?</div>'
               + "".join(img("v_domains_env.png", "left:%dpx;top:%dpx;width:40px" % e, "ab vdm-e") for e in ((650, 213), (765, 222), (943, 222)))
               if i == 0 else "")
            + '</div>')


def item(n, y, c, txt, sep=True):
    return ('<div class="step"><div class="vdm-n" style="top:%dpx;background:%s">%d</div><div class="vdm-t" style="top:%dpx">%s</div>%s</div>'
            % (y, c, n, y, txt, '<div class="vdm-sep" style="top:%dpx"></div>' % (y + 158) if sep else ""))


HTML = CSS + bg("bgk_sky") + "".join([
    '<div class="vdm-p" style="left:128px;top:148px;width:1034px;height:604px"></div>' + boxes + svg()
    + img("v_domains_r.png", "left:93px;top:378px;width:154px")
    + '<div class="vdm-bub" style="left:66px;top:232px;width:200px;text-align:left">ARP-запрос не пересылается в другие VLAN</div>'
    '<div class="vdm-bub" style="left:64px;top:492px;font-size:23px;background:#fbefc8">Устройство L3</div>',
    row(0), row(1), row(2),
    '<div class="vdm-p" style="left:1178px;top:150px;width:462px;height:562px"></div>'
    + item(1, 196, "#2e9e3a", "Сеть разделяется на отдельные широковещательные домены")
    + item(2, 392, "#e0403a", "Широковещательный трафик остаётся внутри VLAN")
    + item(3, 568, "#1f7ae0", "Для связи между VLAN нужен маршрутизатор или L3-коммутатор", False),
    '<div class="step"><div class="vdm-foot"></div>' + img("v_domains_coin.png", "left:396px;top:788px;width:58px")
    + '<div class="vdm-ft">Разделение на VLAN <b>уменьшает область распространения широковещательного трафика.</b></div>'
    '<div class="vdm-sub">VLAN ограничивают последствия широковещательного шторма, но не устраняют его причину.</div></div>',
])
