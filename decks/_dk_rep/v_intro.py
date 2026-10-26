# -*- coding: utf-8 -*-
"""VLAN: один широковещательный домен L2, ARP-рассылка — вёрстка на чистом фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 145

CSS = """<style>
.vin-p{position:absolute;background:#fdf6e3;border:5px solid #3a1606;box-shadow:5px 5px 0 #000}
.vin-dom{position:absolute;left:160px;top:205px;width:1000px;height:440px;border:4px dashed #2a8ab0}
.vin-rib{position:absolute;background:#1d7fa8;color:#fff;border:4px solid #0d3550;box-shadow:5px 5px 0 #000;
  font:800 30px/1 "Golos Text",sans-serif;padding:10px 54px;white-space:nowrap}
.vin-lb{position:absolute;background:#14324e;color:#fff;font:800 22px/1 "Golos Text",sans-serif;padding:5px 14px}
.vin-ip{position:absolute;font:700 20px/1 "Golos Text",sans-serif;color:#111}
.vin-t{position:absolute;font:700 23px/1.3 "Golos Text",sans-serif;color:#1a1a1a}
.vin-n{position:absolute;width:58px;height:58px;border-radius:50%;background:#ffc52a;border:4px solid #3a1606;
  font:800 34px/50px "Golos Text",sans-serif;text-align:center;color:#3a1606}
.vin-bub{position:absolute;left:1015px;top:395px;width:145px;background:#ffe14a;border:4px solid #3a1606;
  font:700 19px/1.25 "Golos Text",sans-serif;text-align:center;padding:6px 4px;box-shadow:4px 4px 0 #000}
.vin-mac{position:absolute;left:768px;top:684px;width:350px;height:50px;background:#ffe14a;border:4px solid #3a1606;
  font:800 32px/44px "Golos Text",sans-serif;text-align:center;color:#111}
.vin-foot{position:absolute;left:312px;top:768px;width:1050px;height:125px;background:#1f5a2a;border:5px solid #0d2a12;
  box-shadow:5px 5px 0 #000}
.vin-ft{position:absolute;left:487px;top:788px;font:700 32px/1.35 "Golos Text",sans-serif;color:#fff}
.vin-ft b{color:#ffe14a}
.vin-svg{position:absolute;left:0;top:0;width:1672px;height:941px}
.vin-svg line{stroke:#14324e;stroke-width:4}
.vin-svg .up{stroke:#fff;stroke-width:3}
.vin-a{fill:#ffc52a;stroke:#c8501e;stroke-width:2;animation:vinb 1s steps(2) infinite}
@keyframes vinb{50%{opacity:.35}}
.vin-hl{animation:vinh 1.2s steps(2) infinite}
@keyframes vinh{50%{filter:brightness(1.3) drop-shadow(0 0 8px #ff9a00)}}
</style>"""

SW = [(585, 275, 130), (255, 410, 130), (580, 410, 130), (885, 410, 130)]
PCS = [183, 280, 375, 508, 603, 698, 817, 912]


def arrow(x, y, ang):
    return ('<polygon class="vin-a" transform="translate(%d %d) rotate(%d)" points="-14,-6 2,-6 2,-14 16,0 2,14 2,6 -14,6"/>'
            % (x, y, ang))


def tree():
    s = '<svg class="vin-svg" viewBox="0 0 1672 941">'
    for x in (335, 650, 960):
        s += '<line x1="650" y1="315" x2="%d" y2="420"/>' % x
    for cx in (320, 645, 950):
        for dx in (-105, 0, 95):
            s += '<line x1="%d" y1="460" x2="%d" y2="535"/>' % (cx, cx + dx)
    s += "".join(arrow(x, y, a) for x, y, a in [
        (372, 340, 200), (460, 322, 195), (538, 308, 190), (775, 310, 10), (858, 325, 15), (942, 340, 20), (637, 365, 90),
        (225, 490, 125), (295, 510, 90), (400, 490, 55), (548, 490, 125), (618, 510, 90), (720, 490, 55),
        (855, 490, 125), (928, 510, 90), (1003, 510, 45)])
    return s + "</svg>"


left = ('<div class="vin-p" style="left:118px;top:155px;width:1440px;height:500px"></div>'
        '<div class="vin-dom"></div>'
        '<div class="vin-rib" style="left:325px;top:172px">Один широковещательный домен L2</div>')
net = ('<div class="step">' + tree()
       + "".join(img("v_intro_sw.png", "left:%dpx;top:%dpx;width:%dpx" % s) for s in SW)
       + '<div class="vin-lb" style="left:612px;top:240px">SW L2</div>'
       + "".join('<div class="vin-lb" style="left:%dpx;top:378px">SW L2</div>' % x for x in (272, 602, 905))
       + "".join(img("v_intro_pc.png", "left:%dpx;top:530px;width:72px" % x) for x in PCS)
       + img("v_intro_pch.png", "left:1008px;top:523px;width:79px", "ab vin-hl")
       + '<div class="vin-ip" style="left:897px;top:616px">10.10.1.6</div>'
       + '<div class="vin-ip" style="left:1016px;top:616px">10.10.1.5</div>'
       + '<div class="vin-bub">ARP-запрос:<br>у кого IP<br>10.10.1.6?</div></div>')


def side(y, n, ico, txt, tx):
    return ('<div class="step"><div class="vin-p" style="left:1183px;top:%dpx;width:358px;height:%dpx;border-color:#1d7fa8"></div>'
            '<div class="vin-n" style="left:1196px;top:%dpx">%d</div>%s'
            '<div class="vin-t" style="left:%dpx;top:%dpx;width:185px;font-size:21px">%s</div></div>'
            % (y, 128 if n == 1 else 135, y + 22, n, ico, tx, y + 22, txt))


HTML = CSS + bg("bgk_ground") + "".join([
    left, net,
    side(185, 1, img("v_intro_i1.png", "left:1263px;top:216px;width:74px"), "10.10.1.5 ищет MAC-адрес узла 10.10.1.6", 1350),
    side(337, 2, img("v_intro_i2.png", "left:1263px;top:352px;width:99px"), "ARP-запрос получает вся локальная сеть", 1366),
    side(497, 3, img("v_intro_i3.png", "left:1266px;top:526px;width:71px"), "Отвечает только узел с IP 10.10.1.6", 1352),
    '<div class="step"><div class="vin-p" style="left:310px;top:668px;width:1050px;height:80px;background:#e3f4fb;border-color:#1d7fa8"></div>'
    + img("v_intro_fr.png", "left:343px;top:680px;width:149px")
    + '<div class="vin-t" style="left:505px;top:692px;font-size:30px">MAC назначения:</div>'
    '<div class="vin-mac">FF:FF:FF:FF:FF:FF</div></div>',
    '<div class="step"><div class="vin-foot"></div>' + img("v_intro_star.png", "left:352px;top:788px;width:96px")
    + '<div class="vin-ft">Коммутатор передаёт широковещательный<br>кадр во все порты <b>того же VLAN</b>, кроме входного.</div></div>',
])
