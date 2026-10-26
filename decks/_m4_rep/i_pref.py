# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 118

CSS = """<style>
.m4x-prf-p{position:absolute;box-sizing:border-box;border:1.5px solid rgba(217,180,90,.85);background:rgba(6,34,28,.86);
  box-shadow:0 0 16px rgba(240,199,94,.3),inset 0 0 22px rgba(240,199,94,.08)}
.m4x-prf-g{position:absolute;white-space:nowrap;font-family:"Playfair Display",serif;font-weight:800;
  background:linear-gradient(180deg,#fff0b0,#e0b04a 60%,#b98a2e);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1.3}
.m4x-prf-r{position:absolute;box-sizing:border-box;left:55px;width:343px;height:62px;border:1.8px solid #64d6e8;border-radius:12px;
  background:rgba(8,40,44,.88);box-shadow:0 0 12px rgba(100,214,232,.55)}
.m4x-prf-r.on{border-color:#f0c75e;background:rgba(60,50,10,.7);box-shadow:0 0 16px rgba(240,199,94,.85)}
.m4x-prf-r b{position:absolute;left:111px;font:600 19px/21px "Golos Text",sans-serif;color:#f0f5ee;white-space:nowrap}
.m4x-prf-r em{position:absolute;left:277px;top:8px;width:52px;height:44px;box-sizing:border-box;border:1.8px solid #64d6e8;border-radius:8px;
  text-align:center;font:600 24px/40px "Golos Text",sans-serif;font-style:normal;color:#f4f6ea;background:rgba(10,60,64,.7)}
.m4x-prf-r.on em{border-color:#f0c75e;background:rgba(80,60,10,.6)}
.m4x-prf-c{position:absolute;box-sizing:border-box;height:38px;font:400 19.5px/37px "Golos Text",sans-serif;color:#f0f5ee;border-bottom:1px solid rgba(217,180,90,.45)}
.m4x-prf-bx{position:absolute;box-sizing:border-box;top:600px;height:122px;border:1.5px solid rgba(217,180,90,.85);border-radius:16px;background:rgba(6,34,28,.88);
  box-shadow:0 0 14px rgba(240,199,94,.3)}
.m4x-prf-n{position:absolute;top:608px;width:68px;height:68px;border-radius:50%;box-sizing:border-box;border:2.5px solid #e9c864;
  background:radial-gradient(circle at 40% 35%,#2f8f7d,#0f4a40);text-align:center;font:800 40px/62px "Playfair Display",serif;color:#fff;box-shadow:0 0 14px rgba(240,199,94,.6)}
.m4x-prf-y{position:absolute;font:700 25px/1 "Golos Text",sans-serif;color:#f0c75e;white-space:nowrap}
.m4x-prf-w{position:absolute;font:400 24px/31px "Golos Text",sans-serif;color:#f4f6ea;white-space:nowrap}
.m4x-prf-sv path.l{fill:none;stroke-width:2.8}
</style>"""

rows = [("Напрямую<br>подключённая", "0", 17), ("Статический<br>маршрут", "1", 17), ("DHCP", "40", 0),
        ("Удалённый клиент<br>(PPTP, L2TP, PPPoE)", "50", 15), ("RIP", "100", 0), ("OSPF", "150", 0), ("IS-IS", "160", 0), ("BGP", "170", 0)]
ys = [145, 220, 294, 368, 442, 517, 591, 666]
left = ""
for i, (lab, val, two) in enumerate(rows):
    y = ys[i]
    fs = ' style="top:%dpx;font-size:%s"' % ((9 if two else 20), "16.5px" if two == 15 else "19px")
    left += ('<div class="m4x-prf-r%s" style="top:%dpx"><b%s>%s</b><em>%s</em></div>' % (" on" if i == 0 else "", y, fs, lab, val)
             + img("i_pref_ic%d.png" % i, "left:62px;top:%dpx" % (y + 2)))

tbl = [("Напрямую подключённая", "0"), ("Статический маршрут", "1"), ("DHCP", "40"), ("Удалённый клиент (PPTP, L2TP, PPPoE)", "50"),
       ("RIP", "100"), ("OSPF", "150"), ("IS-IS", "160"), ("BGP", "170")]
t = ('<div class="m4x-prf-c" style="left:1071px;top:229px;width:400px;height:39px;text-align:center;background:rgba(14,70,66,.8);font-weight:600;border-bottom:1px solid #d9b45a">Источник маршрута</div>'
     '<div class="m4x-prf-c" style="left:1471px;top:229px;width:157px;height:39px;text-align:center;background:rgba(14,70,66,.8);font-weight:600;border-left:1px solid rgba(217,180,90,.45);border-bottom:1px solid #d9b45a">Preference</div>')
yy = 268
for i, (a, b) in enumerate(tbl):
    h = 38 if i < 7 else 37
    hl = i == 0
    st = "background:rgba(200,160,30,.5);border:2px solid #f0c75e;" if hl else ""
    t += ('<div class="m4x-prf-c" style="left:1071px;top:%dpx;width:400px;padding-left:18px;%s">%s</div>'
          '<div class="m4x-prf-c" style="left:1471px;top:%dpx;width:157px;text-align:center;border-left:1px solid rgba(217,180,90,.45);%s">%s</div>'
          % (yy, st, a, yy, st, b))
    yy += 37.4

SV = '<svg class="m4x-prf-sv" style="position:absolute;left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941"><defs><filter id="m4xprfg"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
SV += '<path class="l" stroke="#f0c75e" filter="url(#m4xprfg)" fill="none" d="M398 176 C520 176 590 290 600 372"/><polygon fill="#f0c75e" points="590,360 612,378 586,386"/>'
tg = [(250, 392), (324, 398), (399, 404), (473, 418), (548, 436), (622, 456), (697, 472)]
for (y, ty) in [(251, 385), (325, 392), (399, 400), (473, 412), (548, 430), (622, 452), (697, 480)]:
    SV += '<path class="l" stroke="#8fe3f2" opacity=".9" fill="none" d="M398 %d C500 %d 540 %d 580 %d"/>' % (y, y, ty + 10, ty + 14)
    SV += '<polygon fill="#8fe3f2" points="582,%d 566,%d 570,%d"/>' % (ty + 14, ty + 6, ty + 22)
SV += ('<path stroke="#f0c75e" stroke-width="4" fill="none" filter="url(#m4xprfg)" d="M762 438H820"/><polygon fill="#f0c75e" points="820,426 844,438 820,450"/>'
       '<path d="M862 470 C838 440 850 410 880 410 C885 380 925 368 940 392 C962 372 1012 385 1010 420 C1055 420 1062 470 1020 482 C1000 506 955 508 940 494 C915 510 880 500 874 482 C868 480 864 475 862 470Z" '
       'fill="rgba(60,120,100,.5)" stroke="#f0c75e" stroke-width="2.5" style="filter:drop-shadow(0 0 10px #f0c75e)"/></svg>')

HTML = CSS + bg() + "".join([
    '<div class="step"><div style="position:absolute;left:0;width:1672px;top:119px;text-align:center;font:400 26px/30px \'Golos Text\',sans-serif;color:#f4f6ea">'
    'Preference определяет приоритет источника при выборе маршрута.</div></div>',
    '<div class="step">' + left + '</div>',
    '<div class="step">' + SV + img("i_pref_rt.png", "left:574px;top:376px")
    + '<div style="position:absolute;left:576px;top:512px;width:200px;text-align:center;font:600 21px/1 \'Golos Text\',sans-serif;color:#f4f6ea">Маршрутизатор</div>'
    '<div class="m4x-prf-g" style="left:860px;top:405px;width:190px;text-align:center;font-size:26px;font-weight:700;line-height:27px;-webkit-text-fill-color:#f4f6ea;background:none;white-space:normal">Сеть<br>назначения</div></div>',
    '<div class="step"><div class="m4x-prf-p" style="left:1055px;top:172px;width:588px;height:410px;border-radius:16px"></div>'
    '<div class="m4x-prf-g" style="left:1078px;top:184px;font-size:23px;font-weight:700">Значения preference для источников маршрута</div>' + t + '</div>',
    '<div class="step"><div class="m4x-prf-bx" style="left:577px;width:513px"></div><div class="m4x-prf-n" style="left:591px">1</div>'
    '<div class="m4x-prf-y" style="left:678px;top:617px">Внутри протокола:</div>'
    '<div class="m4x-prf-w" style="left:678px;top:651px">выбирается маршрут<br>с наименьшей метрикой.</div>'
    + img("i_pref_bars.png", "left:986px;top:618px") + '</div>',
    '<div class="step"><div class="m4x-prf-bx" style="left:1115px;width:525px"></div><div class="m4x-prf-n" style="left:1126px">2</div>'
    '<div class="m4x-prf-y" style="left:1215px;top:617px">Между источниками:</div>'
    '<div class="m4x-prf-w" style="left:1215px;top:651px">выбирается маршрут<br>с наименьшим preference.</div>'
    + img("i_pref_org.png", "left:1520px;top:622px") + '</div>',
    '<div class="step"><div class="m4x-prf-p" style="left:590px;top:735px;width:1035px;height:75px;border-radius:14px;border-width:2px"></div>'
    '<div class="m4x-prf-g" style="left:590px;top:741px;width:1035px;text-align:center;font-size:44px">Меньше preference &#8594; выше приоритет</div></div>',
])
