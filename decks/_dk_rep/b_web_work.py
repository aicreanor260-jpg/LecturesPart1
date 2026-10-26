# -*- coding: utf-8 -*-
"""Подключение по Web-интерфейсу: L2 / L3 / L7 и схема ПК — SW-1 — браузер."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 215

CSS = """<style>
.bww-b{position:absolute;background:rgba(255,255,255,.96);border:3px solid #ff2e93;box-shadow:5px 5px 0 rgba(42,10,42,.35);
  font:800 24px/1.25 "Golos Text",sans-serif;color:#1a0a1a;text-align:center;padding:6px 14px;white-space:nowrap}
.bww-b.blue{border-color:#2aa8e8}
.bww-p{position:absolute;top:556px;height:262px;background:rgba(255,255,255,.95);border:3px solid #2a0a2a;box-shadow:6px 6px 0 rgba(255,46,147,.45)}
.bww-h{position:absolute;font:700 25px/1.2 "Golos Text",sans-serif;color:#1a0a1a;white-space:nowrap}
.bww-h b{color:#ff2e93;font-weight:900}
.bww-n{position:absolute;width:52px;height:52px;border-radius:50%;background:#ff2e93;color:#fff;font:900 32px/52px Rubik,sans-serif;text-align:center}
.bww-svg{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.bww-svg .w{fill:none;stroke:#3fe6ff;stroke-width:7;filter:drop-shadow(0 0 6px #3fe6ff);stroke-dasharray:22 10;animation:bwwd 1s linear infinite}
.bww-svg .k{fill:none;stroke:#2a0a2a;stroke-width:3}
.bww-svg .p{fill:none;stroke:#ff2e93;stroke-width:4}
.bww-svg circle{fill:#ff2e93;stroke:#fff;stroke-width:3}
@keyframes bwwd{to{stroke-dashoffset:-64}}
.bww-f{position:absolute;top:832px;height:76px;font:700 28px/76px "Golos Text",sans-serif;white-space:nowrap}
.bww-f b{font-weight:900;color:#ff2e93}
.bww-f code{font:700 32px "Courier New",monospace;color:#3fe6ff}
</style>"""

HTML = CSS + bg("bgk_roof") + "".join([
    '<div class="step">' + img("b_web_work_girl.png", "left:0;top:200px;width:560px") + '</div>',
    '<div class="step">' + img("b_web_work_pc.png", "left:560px;top:355px;width:162px") +
    img("b_web_work_sw.png", "left:985px;top:340px;width:350px") +
    img("b_web_work_br.png", "left:1432px;top:350px;width:216px") +
    '<svg class="bww-svg" viewBox="0 0 1672 941"><path class="w" d="M712 458 H1020"/><path class="w" d="M1270 452 H1440"/>'
    '<path class="k" d="M670 375 L700 345"/><path class="p" d="M1158 300 V362"/><path class="p" d="M1028 392 V456"/>'
    '<circle cx="1158" cy="364" r="9"/><circle cx="1028" cy="460" r="9"/></svg></div>',
    '<div class="step"><div class="bww-b blue" style="left:516px;top:272px">Администратор:<br>10.10.1.121/24</div>'
    '<div class="bww-b" style="left:808px;top:344px;font-size:21px">Gi1/0/2 — VLAN 20</div>'
    '<div class="bww-b" style="left:1034px;top:216px">SVI VLAN 20:<br>10.10.1.28/24</div>'
    '<div class="bww-b" style="left:1422px;top:282px;font-size:27px;color:#2a0a2a">HTTP • L7</div></div>',
    '<div class="step"><div class="bww-p" style="left:38px;width:544px"></div><div class="bww-n" style="left:58px;top:578px">1</div>'
    '<div class="bww-h" style="left:140px;top:576px"><b>L2:</b> порт включён<br>в VLAN управления 20</div>'
    + img("b_web_work_p1.png", "left:112px;top:655px;width:463px") +
    '<div class="bww-b" style="left:322px;top:746px;font-size:21px">Gi1/0/2 — VLAN 20</div></div>',
    '<div class="step"><div class="bww-p" style="left:592px;width:526px"></div><div class="bww-n" style="left:610px;top:578px">2</div>'
    '<div class="bww-h" style="left:690px;top:576px"><b>L3:</b> оба адреса в подсети<br>10.10.1.0/24</div>'
    + img("b_web_work_p2pc.png", "left:615px;top:652px;width:137px") + img("b_web_work_p2sw.png", "left:952px;top:668px;width:116px") +
    '<svg class="bww-svg" viewBox="0 0 1672 941"><path class="p" d="M760 710 H940 M772 700 L760 710 L772 720 M928 700 L940 710 L928 720"/></svg>'
    '<div class="bww-h" style="left:790px;top:664px;font:800 21px/1 Golos Text,sans-serif;color:#ff2e93">10.10.1.0/24</div>'
    '<div class="bww-h" style="left:612px;top:756px;font-size:21px;text-align:center">Администратор:<br>10.10.1.121/24</div>'
    '<div class="bww-h" style="left:936px;top:756px;font-size:21px;text-align:center">SVI VLAN 20:<br>10.10.1.28/24</div></div>',
    '<div class="step"><div class="bww-p" style="left:1128px;width:516px"></div><div class="bww-n" style="left:1146px;top:578px">3</div>'
    '<div class="bww-h" style="left:1220px;top:576px"><b>L7:</b> доступ к Web-интерфейсу<br>по HTTP</div>'
    + img("b_web_work_p3.png", "left:1182px;top:648px;width:206px") +
    '<div class="bww-b" style="left:1376px;top:682px;font:italic 900 40px/1.1 Rubik,sans-serif;color:#ff2e93;border-width:5px">HTTP • L7</div></div>',
    '<div class="step"><div class="bww-f" style="left:38px;width:786px;background:rgba(255,255,255,.96);border:3px solid #2a0a2a">'
    + img("b_web_work_lock.png", "left:20px;top:8px;width:60px") +
    '<span style="position:absolute;left:160px">Доступ: только пользователь <b>privilege 15</b></span></div>'
    '<div class="bww-f" style="left:836px;width:808px;background:#1d1a3a;border:3px solid #2a0a2a;color:#fff">'
    + img("b_web_work_gear.png", "left:24px;top:4px;width:70px") +
    '<span style="position:absolute;left:132px">Отключить Web: <code>no ip http server</code></span></div></div>',
])
