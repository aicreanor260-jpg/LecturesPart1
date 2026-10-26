# -*- coding: utf-8 -*-
"""VLAN: широковещательный ARP-запрос в домене L2 — вёрстка на чистом фоне."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 172

CSS = """<style>
.var-p{position:absolute;background:#fdf6e3;border:5px solid #fff;outline:3px solid #14324e;box-shadow:5px 5px 0 #000}
.var-dom{position:absolute;left:40px;top:190px;width:1048px;height:500px;border:3px dashed #14324e}
.var-h{position:absolute;font:800 32px/1 "Golos Text",sans-serif;color:#14324e;white-space:nowrap}
.var-lb{position:absolute;background:#fbefc8;font:700 18px/1.15 "Golos Text",sans-serif;text-align:center;color:#14324e;padding:4px 10px}
.var-ip{position:absolute;width:92px;background:#fbefc8;border:2px solid #e8d9a8;font:700 17px/26px "Golos Text",sans-serif;text-align:center}
.var-ip.me{background:#ffd0d0;border-color:#e04040}
.var-bub{position:absolute;left:990px;top:497px;width:125px;background:#fff;border:3px solid #14324e;border-radius:10px;
  font:700 17px/1.3 "Golos Text",sans-serif;text-align:center;padding:4px}
.var-k{position:absolute;font:700 30px/1.2 "Golos Text",sans-serif;color:#14324e}
.var-v{position:absolute;background:#fbefc8;border:3px solid #e8d9a8;font:800 50px/76px "Golos Text",sans-serif;text-align:center;color:#111}
.var-v2{position:absolute;background:#e3f4fb;border:3px solid #7fc8e6;font:800 36px/62px "Golos Text",sans-serif;text-align:center;color:#14324e}
.var-t{position:absolute;font:700 23px/1.3 "Golos Text",sans-serif;color:#14324e}
.var-w{position:absolute;left:350px;top:796px;width:1020px;height:72px;background:#fbd4d4;font:700 23px/1.3 "Golos Text",sans-serif;
  color:#d81e1e;padding:6px 16px;box-sizing:border-box}
.var-fn{position:absolute;left:1205px;top:884px;width:445px;background:#fff;border:2px solid #14324e;font:600 14px/26px "Golos Text",sans-serif;text-align:center;color:#14324e}
.var-svg{position:absolute;left:0;top:0;width:1672px;height:941px}
.var-svg line{stroke:#111;stroke-width:4}
.var-svg .ar{stroke:#ff6a1a;stroke-width:5;marker-end:url(#varm)}
.var-e{animation:vare 1.4s ease-in-out infinite}
@keyframes vare{50%{transform:translateY(-5px)}}
.var-hl{animation:varh 1.2s steps(2) infinite}
@keyframes varh{50%{filter:drop-shadow(0 0 8px #ff6a1a)}}
</style>"""

ACC = [(135, "L2-коммутатор<br>доступа 1", 122), (493, "L2-коммутатор<br>доступа 2", 482), (848, "L2-коммутатор<br>доступа 3", 838)]
PCS = [(73, "10.10.1.1"), (180, "10.10.1.2"), (287, "10.10.1.3"), (431, "10.10.1.7"), (538, "10.10.1.8"), (645, "10.10.1.9"),
       (783, "10.10.1.4"), (890, "10.10.1.6")]


def svg():
    s = ('<svg class="var-svg" viewBox="0 0 1672 941"><defs><marker id="varm" markerWidth="5" markerHeight="5" refX="3" refY="2.5" orient="auto">'
         '<path d="M0,0 L5,2.5 L0,5z" fill="#ff6a1a"/></marker></defs>'
         '<line x1="470" y1="330" x2="300" y2="405"/><line x1="668" y1="330" x2="830" y2="405"/><line x1="570" y1="345" x2="570" y2="395"/>')
    for x, dst in ((210, (103, 209, 316)), (568, (460, 567, 674)), (924, (813, 920, 1025))):
        for d in dst:
            s += '<line x1="%d" y1="495" x2="%d" y2="580"/>' % (x + (d - x) // 3, d)
    s += ('<line class="ar" x1="455" y1="322" x2="300" y2="385"/><line class="ar" x1="690" y1="320" x2="830" y2="385"/>'
          '<line class="ar" x1="570" y1="348" x2="570" y2="392"/>')
    for x, dst in ((210, (103, 209, 316)), (568, (460, 567, 674)), (924, (813, 920))):
        for d in dst:
            s += '<line class="ar" x1="%d" y1="505" x2="%d" y2="575"/>' % (x + (d - x) // 3, d - (d - x) // 8)
    s += '<line class="ar" x1="995" y1="575" x2="960" y2="502"/>'
    return s + "</svg>"


ENV = [(370, 327), (722, 327), (552, 355), (114, 520), (192, 520), (270, 520), (472, 520), (552, 520), (632, 520),
       (826, 520), (902, 520), (960, 530)]

left = ('<div class="var-p" style="left:22px;top:178px;width:1083px;height:527px"></div><div class="var-dom"></div>'
        '<div class="var-h" style="left:68px;top:198px">Один широковещательный домен L2</div>'
        '<div class="var-lb" style="left:480px;top:236px">Центральный<br>L2-коммутатор</div>'
        + "".join('<div class="var-lb" style="left:%dpx;top:396px">%s</div>' % (lx, t) for _, t, lx in ACC))
net = ('<div class="step">' + svg() + img("v_arp_sw.png", "left:470px;top:288px;width:200px")
       + "".join(img("v_arp_asw.png", "left:%dpx;top:448px;width:156px" % x) for x, _, _ in ACC)
       + "".join(img("v_arp_pc.png", "left:%dpx;top:576px;width:64px" % x)
                 + '<div class="var-ip" style="left:%dpx;top:648px">%s</div>' % (x - 16, ip) for x, ip in PCS)
       + img("v_arp_pch.png", "left:990px;top:573px;width:70px", "ab var-hl")
       + '<div class="var-ip me" style="left:977px;top:648px">10.10.1.5</div>'
       + '<div class="var-bub">У кого IP<br>10.10.1.6?</div>'
       + "".join(img("v_arp_env.png", "left:%dpx;top:%dpx;width:40px" % e, "ab var-e") for e in ENV) + '</div>')


def card(y, h, bgc, inner):
    return ('<div class="step"><div class="var-p" style="left:1122px;top:%dpx;width:528px;height:%dpx;background:%s"></div>%s</div>'
            % (y, h, bgc, inner))


HTML = CSS + bg("bgk_ground") + "".join([
    left, net,
    card(180, 160, "#fdf6e3", img("v_arp_q.png", "left:1146px;top:212px;width:102px")
         + '<div class="var-k" style="left:1270px;top:202px">Искомый IP в ARP:</div>'
           '<div class="var-v" style="left:1268px;top:250px;width:360px">10.10.1.6</div>'),
    card(358, 162, "#eaf6ee", img("v_arp_env2.png", "left:1143px;top:398px;width:104px")
         + '<div class="var-k" style="left:1270px;top:382px">MAC назначения кадра:</div>'
           '<div class="var-v2" style="left:1268px;top:428px;width:362px">FF:FF:FF:FF:FF:FF</div>'),
    card(536, 166, "#e3f4fb", img("v_arp_mon.png", "left:1145px;top:562px;width:97px")
         + '<div class="var-k" style="left:1272px;top:558px;font-size:32px">Запрос получают<br>все остальные узлы<br>данного VLAN.</div>'),
    '<div class="step"><div class="var-p" style="left:215px;top:718px;width:1180px;height:162px"></div>'
    '<div class="var-t" style="left:250px;top:732px;width:1100px;font-size:25px">Копии кадров занимают полосу каналов, а устройства тратят ресурсы на обработку.</div>'
    + img("v_arp_ex.png", "left:255px;top:792px;width:79px")
    + '<div class="var-w">Большой объём широковещательного трафика может перегрузить сеть и снизить полезную пропускную способность.</div></div>',
    '<div class="step"><div class="var-fn">* Один обычный ARP-запрос не вызывает перегрузку.</div></div>',
])
