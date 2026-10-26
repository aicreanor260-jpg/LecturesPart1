# -*- coding: utf-8 -*-
"""2.6: Inside local — внутренний локальный адрес (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 30

CSS = """<style>
.n6il-p{position:absolute;box-sizing:border-box;border-radius:18px;border:1.5px solid rgba(92,190,255,.7);
  background:linear-gradient(160deg,rgba(16,40,90,.72),rgba(6,14,36,.88));box-shadow:0 0 22px rgba(58,160,255,.32)}
.n6il-pk{position:absolute;box-sizing:border-box;border-radius:12px;border:2px solid rgba(92,190,255,.8);background:rgba(20,60,130,.85);
  box-shadow:0 0 18px rgba(58,160,255,.5);color:#fff;font:600 17px/1.25 "Golos Text",sans-serif;padding:16px 0 0 78px}
.n6il-pk::after{content:"";position:absolute;left:112px;bottom:-12px;border:10px solid transparent;border-top-color:rgba(92,190,255,.8);border-bottom:0}
.n6il-dot{position:absolute;width:14px;height:14px;margin:-7px;border-radius:50%;background:#7fe0ff;box-shadow:0 0 14px #5cd2ff;
  offset-path:path("M296 644Q360 690 420 660H830M1085 628H1240Q1290 628 1305 600");animation:n6ilm 3.2s linear infinite}
@keyframes n6ilm{from{offset-distance:0%}to{offset-distance:100%}}
</style>"""

CLOUD = """<svg style="position:absolute;left:1285px;top:412px;width:350px;height:200px" viewBox="0 0 350 200">
<defs><linearGradient id="n6ilc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fa6ff"/><stop offset="1" stop-color="#173f8a"/></linearGradient></defs>
<path style="filter:drop-shadow(0 0 10px #3aa0ff)" d="M50 190Q6 190 8 150Q10 112 52 108Q56 62 104 62Q128 18 180 18Q236 18 254 70Q300 64 318 104Q346 118 342 152Q338 190 296 190Z"
 fill="url(#n6ilc)" stroke="#9fd8ff" stroke-width="3"/></svg>"""

HTML = CSS + bg("bgk_net") + "".join([
    '<div class="step"><div class="n6il-p" style="left:40px;top:36px;width:1592px;height:866px;background:rgba(8,18,44,.45);box-shadow:none"></div>'
    '<div style="position:absolute;left:86px;top:62px;white-space:nowrap;font:800 92px/1 Montserrat,sans-serif;color:#fff">Inside local</div>'
    '<div style="position:absolute;left:86px;top:156px;white-space:nowrap;font:800 50px/1 Montserrat,sans-serif;color:#cfe0ff">Внутренний локальный адрес</div>'
    '<div style="position:absolute;left:86px;top:228px;white-space:nowrap;font:500 33px/1.4 \'Golos Text\',sans-serif;color:#b9d2f5">'
    'Обычный IP-адрес устройства внутри локальной сети.<br>Компьютер использует его для связи с другими узлами своей сети.</div></div>',
    # схема
    '<div class="step"><div class="n6il-p" style="left:54px;top:338px;width:1564px;height:424px;background:linear-gradient(160deg,rgba(16,40,90,.5),rgba(6,14,36,.6))"></div>'
    '<div class="n6il-p" style="left:54px;top:338px;width:734px;height:424px;background:rgba(14,40,96,.55)"></div>'
    '<div style="position:absolute;left:54px;top:420px;width:734px;border-top:1.5px solid rgba(92,190,255,.5)"></div>'
    + img("n6_il_home.png", "left:74px;top:348px;width:80px") +
    '<div style="position:absolute;left:178px;top:362px;font:800 30px/1.2 Montserrat,sans-serif;color:#fff">Внутренняя сеть</div>'
    + img("n6_il_lap.png", "left:88px;top:548px;width:284px") + img("n6_il_sw.png", "left:405px;top:578px;width:220px") + '</div>',
    '<div class="step"><div style="position:absolute;left:108px;top:428px;width:413px;height:106px;box-sizing:border-box;border-radius:14px;'
    'background:#7fd8ff;box-shadow:0 0 22px rgba(92,210,255,.6);text-align:center;color:#0c1a4a">'
    '<div style="font:800 46px/1 \'JetBrains Mono\',monospace;margin-top:14px">192.168.1.10</div>'
    '<div style="font:600 21px/1.2 \'Golos Text\',sans-serif;margin-top:8px">IP-адрес компьютера до NAT</div></div>'
    '<svg style="position:absolute;left:180px;top:530px;width:40px;height:52px"><path d="M4 0H36L18 40Z" fill="#7fd8ff"/><circle cx="17" cy="47" r="5" fill="#bff"/></svg></div>',
    # NAT
    '<div class="step">' + img("n6_il_rt.png", "left:802px;top:432px;width:288px") +
    '<div style="position:absolute;left:895px;top:496px;font:800 48px/1 Montserrat,sans-serif;color:#fff">NAT</div>'
    '<div class="n6il-pk" style="left:586px;top:466px;width:244px;height:104px">Источник:<br>'
    '<span style="font:600 21px/1.8 \'JetBrains Mono\',monospace">192.168.1.10</span></div>'
    + img("n6_il_doc.png", "left:598px;top:488px;width:54px") + '</div>',
    # Интернет
    '<div class="step">' + CLOUD + img("n6_il_srv.png", "left:1352px;top:540px;width:243px") +
    '<div style="position:absolute;left:1402px;top:500px;font:800 33px/1 Montserrat,sans-serif;color:#fff">Интернет</div>'
    '<div class="n6il-pk" style="left:1064px;top:462px;width:264px;height:108px">Источник:<br>'
    '<span style="color:#7fe8ff;font-weight:700;font-size:19px">публичный адрес<br>маршрутизатора</span></div>'
    + img("n6_il_doc.png", "left:1080px;top:485px;width:54px") +
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" fill="none" stroke="#5cd2ff" stroke-width="3">'
    '<path d="M296 644Q360 690 420 660M620 628H830M1085 628H1240Q1290 628 1305 600" style="filter:drop-shadow(0 0 5px #3aa0ff)"/>'
    '<path d="M700 600h22M714 592l8 8-8 8M1160 600h22M1174 592l8 8-8 8" stroke-width="3"/></svg>'
    '<div class="n6il-dot"></div></div>',
    # вывод
    '<div class="step"><div style="position:absolute;left:68px;top:782px;width:1536px;height:98px;border-radius:14px;background:#8fdcff;'
    'box-shadow:0 0 26px rgba(92,210,255,.55)"></div>' + img("n6_il_bulb.png", "left:158px;top:788px;width:84px") +
    '<div style="position:absolute;left:296px;top:804px;height:54px;border-left:3px solid #0c1a4a"></div>'
    '<div style="position:absolute;left:336px;top:806px;white-space:nowrap;font:800 39px/1.2 Montserrat,sans-serif;color:#0c1a4a">'
    'Проще говоря: адрес компьютера до выхода наружу.</div></div>',
])
