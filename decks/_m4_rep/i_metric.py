# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 196

CSS = """<style>
.m4x-met-p{position:absolute;box-sizing:border-box;background:rgba(5,32,26,.8);border:1.5px solid #d9b45a;
  box-shadow:0 0 18px rgba(240,199,94,.35),inset 0 0 22px rgba(240,199,94,.1)}
.m4x-met-g{position:absolute;white-space:nowrap;font-family:"Playfair Display",serif;font-weight:700;
  background:linear-gradient(180deg,#fff0b0,#e0b04a 60%,#b98a2e);-webkit-background-clip:text;background-clip:text;color:transparent}
.m4x-met-i{position:absolute;box-sizing:border-box;left:78px;width:457px;height:89px;border:1.5px solid rgba(217,180,90,.85);border-radius:12px;background:rgba(6,40,34,.75)}
.m4x-met-i b{position:absolute;left:132px;font:600 21px/1 "Golos Text",sans-serif;color:#f4f6ea;white-space:nowrap}
.m4x-met-i span{position:absolute;left:132px;font:400 15.5px/1.2 "Golos Text",sans-serif;color:#d4e2d8;white-space:nowrap}
.m4x-met-i svg{position:absolute;left:28px;top:16px}
.m4x-met-i svg *{fill:none;stroke:#f0c75e;stroke-width:2;stroke-linejoin:round}
.m4x-met-pill{position:absolute;box-sizing:border-box;border:1.5px solid #e9c864;border-radius:8px;background:rgba(6,38,32,.9);text-align:center;
  font:400 23px/1 "Golos Text",sans-serif;color:#f4f6ea;box-shadow:0 0 10px rgba(240,199,94,.4)}
.m4x-met-pill b{font-weight:700;font-size:32px;color:#f6d77a;margin-left:4px}
.m4x-met-lab{position:absolute;text-align:center;font:400 22px/25px "Golos Text",sans-serif;color:#f0f5ee;white-space:nowrap}
.m4x-met-sv path{fill:none}
.m4x-met-dash{stroke:#7fe8d0;stroke-width:2.5;stroke-dasharray:12 8;animation:m4xmetd 1.4s linear infinite}
@keyframes m4xmetd{to{stroke-dashoffset:-40}}
</style>"""

IC = {
    "org": '<svg width="56" height="56" viewBox="0 0 56 56"><rect x="19" y="4" width="18" height="14"/><rect x="3" y="38" width="18" height="14"/><rect x="35" y="38" width="18" height="14"/><path d="M28 18v10M12 38v-10h32v10"/></svg>',
    "doc": '<svg width="56" height="56" viewBox="0 0 56 56"><path d="M12 4h24l10 10v38H12z"/><path d="M36 4v10h10M19 24h20M19 31h20M19 38h20M19 45h12"/></svg>',
    "gear": '<svg width="56" height="56" viewBox="0 0 56 56"><circle cx="28" cy="28" r="8"/><path d="M24 4h8l2 6 6 3 6-2 5 7-4 5v6l4 5-5 7-6-2-6 3-2 6h-8l-2-6-6-3-6 2-5-7 4-5v-6l-4-5 5-7 6 2 6-3z"/></svg>',
    "cloud": '<svg width="56" height="56" viewBox="0 0 56 56"><path d="M14 44a10 10 0 0 1-1-20 14 14 0 0 1 27-3 11 11 0 0 1 3 23z"/></svg>',
}
items = [("org", "Подключённые сети", "Сети, напрямую подключённые<br>к маршрутизатору", 262),
         ("doc", "Статический маршрут", "Заданный вручную<br>администратором", 362),
         ("gear", "RIP · OSPF · BGP", "Динамические маршруты<br>от протоколов маршрутизации", 462),
         ("cloud", "DHCP · L2TP · OpenVPN", "Маршруты, полученные<br>от других сервисов", 563)]
left = ""
for k, t, s, y in items:
    left += ('<div class="m4x-met-i" style="top:%dpx">%s<b style="top:14px">%s</b><span style="top:41px">%s</span></div>' % (y, IC[k], t, s))

SV = ('<svg class="m4x-met-sv" style="position:absolute;left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941">'
      '<defs><filter id="m4xmetg"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
      '<g filter="url(#m4xmetg)" stroke="#f0c75e" stroke-width="5" fill="none"><path d="M706 382 C735 335 770 310 812 296"/>'
      '<path d="M930 271 L1055 271"/><path d="M1256 280 C1330 288 1400 320 1440 372"/></g>'
      '<g fill="#f0c75e"><polygon points="796,296 822,286 812,312"/><polygon points="1040,257 1064,271 1040,285"/><polygon points="1385,318 1412,326 1396,348"/></g>'
      '<path d="M1068 271 L1150 271" stroke="#f0c75e" stroke-width="5" style="filter:drop-shadow(0 0 5px #f0c75e)"/>'
      '<g class="m4x-met-dash" fill="none"><path class="m4x-met-dash" d="M745 416 L855 416"/><path class="m4x-met-dash" d="M948 416 L1142 416"/>'
      '<path class="m4x-met-dash" d="M1238 416 L1398 416"/>'
      '<path class="m4x-met-dash" d="M745 448 C770 520 800 538 836 540"/><path class="m4x-met-dash" d="M934 547 L1180 551"/>'
      '<path class="m4x-met-dash" d="M1278 545 C1340 535 1390 500 1418 462"/></g>'
      '<g fill="#7fe8d0"><polygon points="1396,404 1414,416 1396,428"/><polygon points="1404,468 1412,448 1428,462"/></g>'
      '<path d="M1442 388 C1415 360 1432 330 1470 340 C1485 318 1535 322 1548 340 C1575 330 1620 340 1620 372 C1662 378 1660 440 1620 450 C1610 475 1560 482 1545 470 C1520 485 1475 482 1465 462 C1430 462 1410 425 1442 388Z" '
      'fill="rgba(60,120,100,.55)" stroke="#f0c75e" stroke-width="2.5" style="filter:drop-shadow(0 0 10px #f0c75e)"/></svg>')

HTML = CSS + bg() + "".join([
    '<div class="step"><div class="m4x-met-p" style="left:48px;top:198px;width:515px;height:468px;border-radius:14px"></div>'
    '<div class="m4x-met-g" style="left:83px;top:206px;font-size:34px">Откуда берутся маршруты</div></div>',
    ''.join('<div class="step">%s</div>' % ('<div class="m4x-met-i" style="top:%dpx">%s<b style="top:14px">%s</b><span style="top:41px">%s</span></div>' % (y, IC[k], t, s))
            for k, t, s, y in items),
    '<div class="step">' + SV
    + img("i_metric_rs.png", "left:608px;top:368px")
    + '<div class="m4x-met-lab" style="left:580px;top:475px;width:200px">Исходный<br>маршрутизатор</div></div>',
    '<div class="step">' + img("i_metric_a1.png", "left:826px;top:244px") + img("i_metric_a2.png", "left:1155px;top:244px")
    + '<div class="m4x-met-pill" style="left:955px;top:207px;width:183px;height:44px;line-height:42px">Метрика <b>10</b></div></div>',
    '<div class="step">' + img("i_metric_b1.png", "left:850px;top:384px") + img("i_metric_b2.png", "left:1140px;top:384px")
    + '<div class="m4x-met-pill" style="left:968px;top:361px;width:156px;height:38px;line-height:36px;font-size:21px">Метрика <b style="font-size:27px">20</b></div></div>',
    '<div class="step">' + img("i_metric_c1.png", "left:834px;top:506px") + img("i_metric_c2.png", "left:1178px;top:514px")
    + '<div class="m4x-met-pill" style="left:968px;top:499px;width:156px;height:38px;line-height:36px;font-size:21px">Метрика <b style="font-size:27px">30</b></div></div>',
    '<div class="step"><div class="m4x-met-g" style="left:1465px;top:384px;width:155px;font-size:28px;font-weight:700;line-height:31px;text-align:center;white-space:normal;left:1466px;width:156px;-webkit-text-fill-color:#f4f6ea;background:none;color:#f4f6ea">Сеть<br>назначения</div></div>',
    '<div class="step"><div class="m4x-met-p" style="left:663px;top:631px;width:612px;height:93px;border-radius:46px"></div>'
    + img("i_metric_bulb.png", "left:706px;top:638px")
    + '<div class="m4x-met-g" style="left:800px;top:646px;width:430px;text-align:center;white-space:normal;font-size:28px;line-height:31px;-webkit-text-fill-color:#f4f6ea;background:none;color:#f4f6ea">Метрика помогает протоколу выбрать лучший путь.</div></div>',
])
