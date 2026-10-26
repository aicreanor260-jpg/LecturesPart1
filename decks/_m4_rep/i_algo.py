# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 222

CSS = """<style>
.m4x-alg-c{position:absolute;box-sizing:border-box;top:238px;height:447px;border:1.5px solid #d9b45a;border-radius:70px 70px 40px 40px;
  background:rgba(5,32,26,.72);box-shadow:0 0 20px rgba(240,199,94,.4),inset 0 0 26px rgba(240,199,94,.15)}
.m4x-alg-n{position:absolute;width:52px;height:52px;border-radius:50%;box-sizing:border-box;border:2px solid #e9c864;background:#06231d;
  box-shadow:0 0 14px rgba(240,199,94,.6);text:center;text-align:center;font:800 32px/48px "Playfair Display",serif;color:#f6d77a}
.m4x-alg-h{position:absolute;text-align:center;font:700 26px/1.12 "Playfair Display",serif;white-space:nowrap;
  background:linear-gradient(180deg,#fff0b0,#e0b04a 60%,#b98a2e);-webkit-background-clip:text;background-clip:text;color:transparent}
.m4x-alg-t{position:absolute;text-align:center;font:400 20px/24px "Golos Text",sans-serif;color:#eaf2e8;white-space:nowrap}
.m4x-alg-ring{position:absolute;box-sizing:border-box;border:1.5px solid rgba(240,199,94,.8);border-radius:50%;box-shadow:0 0 14px rgba(240,199,94,.4)}
.m4x-alg-pk{position:absolute;box-sizing:border-box;left:440px;top:386px;width:166px;height:142px;border:2px solid #7fe8e0;border-radius:10px;
  background:rgba(30,90,95,.55);box-shadow:0 0 16px rgba(80,220,230,.5)}
.m4x-alg-tb{position:absolute;box-sizing:border-box;left:700px;top:348px;width:276px;height:204px;border:1.5px solid #d9b45a;border-radius:14px;background:rgba(6,34,28,.85)}
.m4x-alg-tb div{position:absolute;font:400 18px/1 "Golos Text",sans-serif;color:#f0f5ee;white-space:nowrap}
.m4x-alg-ln{position:absolute;background:rgba(217,180,90,.6)}
.m4x-alg-o{position:absolute;box-sizing:border-box;left:1038px;width:254px;height:42px;border-radius:8px;font:400 21px/42px "Golos Text",sans-serif;padding-left:24px;color:#8fa59b}
.m4x-alg-warn{position:absolute;left:398px;top:716px;width:876px;height:82px;box-sizing:border-box;border:1.5px solid #d9b45a;border-radius:41px;
  background:rgba(5,32,26,.85);box-shadow:0 0 18px rgba(240,199,94,.4)}
.m4x-alg-ar path{fill:#f0c75e;filter:drop-shadow(0 0 8px #f0c75e)}
</style>"""

def T(x, y, w, s, cls="m4x-alg-t"):
    return '<div class="%s" style="left:%dpx;top:%dpx;width:%dpx;margin-left:-%dpx">%s</div>' % (cls, x, y, w, w // 2, s)

def arrow(x, y):
    return ('<svg class="m4x-alg-ar" style="position:absolute;left:%dpx;top:%dpx" width="62" height="56" viewBox="0 0 62 56">'
            '<path d="M2 17 Q22 14 30 12 L30 0 L60 28 L30 56 L30 44 Q20 42 2 39 Q10 28 2 17Z"/></svg>' % (x, y))

def card(x, w, n, cx, head, hy):
    return ('<div class="m4x-alg-c" style="left:%dpx;width:%dpx"></div><div class="m4x-alg-n" style="left:%dpx;top:232px">%d</div>%s'
            % (x, w, cx - 26, n, T(cx, hy, 300, head, "m4x-alg-h")))

rows = [("192.168.1.0/24", "gi1/0/1", 419), ("192.168.0.0/16", "gi1/0/2", 455), ("10.0.0.0/8", "gi1/0/3", 491), ("0.0.0.0/0", "gi1/0/4", 527)]
tb = ('<div style="left:46px;top:20px">Префикс</div><div style="left:158px;top:12px;line-height:16px;text-align:center;width:112px">Выход /<br>следующий узел</div>'
      '<div class="m4x-alg-ln" style="left:0;top:50px;width:276px;height:1px"></div>')
tb = tb.replace('left:46px;top:20px', 'left:46px;top:20px').replace('left:158px;top:12px;line-height:16px;text-align:center;width:112px', 'left:155px;top:12px;line-height:15px;font-size:15px;text-align:center;width:118px')
for p, g, y in rows:
    yy = y - 348 - 9
    tb += ('<div style="left:22px;top:%dpx">%s</div><div style="left:187px;top:%dpx;color:#cfe0d6">%s</div>'
           '<div class="m4x-alg-ln" style="left:0;top:%dpx;width:276px;height:1px"></div>') % (yy, p, yy, g, yy + 27)
tb += '<div class="m4x-alg-ln" style="left:155px;top:0;width:1px;height:204px"></div>'

HTML = CSS + bg() + "".join([
    '<div class="step">' + card(28, 315, 1, 184, "Пакет поступает", 291)
    + img("i_algo_pkt.png", "left:0;top:385px") + T(184, 600, 300, "Входной<br>интерфейс") + arrow(335, 420) + '</div>',
    '<div class="step">' + card(358, 310, 2, 511, "Адрес назначения", 291)
    + '<div class="m4x-alg-ring" style="left:398px;top:346px;width:226px;height:226px"></div>'
    + '<div class="m4x-alg-pk"></div>'
    + '<div style="position:absolute;left:470px;top:396px;font:400 18px/1 \'Golos Text\',sans-serif;color:#9fb8b0">IP src</div>'
    + '<div style="position:absolute;left:442px;top:424px;width:158px;height:56px;background:rgba(10,50,50,.8);border-top:1px solid #7fe8e0;border-bottom:1px solid #7fe8e0"></div>'
    + '<div style="position:absolute;left:470px;top:430px;font:400 18px/1 \'Golos Text\',sans-serif;color:#f0f5ee">IP dst</div>'
    + '<div style="position:absolute;left:469px;top:452px;font:600 22px/1 \'Golos Text\',sans-serif;color:#fff;letter-spacing:.2px">192.168.1.42</div>'
    + '<div style="position:absolute;left:470px;top:498px;font:400 17px/1 \'Golos Text\',sans-serif;color:#9fb8b0">Прочие поля</div>'
    + T(511, 586, 300, "Извлечь IP-адрес<br>назначения<br>из заголовка") + arrow(640, 425) + '</div>',
    '<div class="step">' + card(683, 309, 3, 837, "Поиск в таблице", 291)
    + '<div class="m4x-alg-tb">' + tb + '</div>'
    + img("i_algo_lens.png", "left:812px;top:528px") + T(838, 592, 200, "Найти все<br>подходящие<br>маршруты") + arrow(978, 425) + '</div>',
    '<div class="step">' + card(1010, 310, 4, 1162, "Самое длинное<br>совпадение", 290)
    + '<div style="position:absolute;left:1030px;top:352px;width:270px;height:210px;border-radius:14px;border:1.5px solid rgba(217,180,90,.5);background:rgba(6,30,26,.7)"></div>'
    + '<div style="position:absolute;left:1078px;top:370px;font:400 17px/1 \'Golos Text\',sans-serif;color:#d8e6dc">IP назначения:</div>'
    + '<div style="position:absolute;left:1078px;top:390px;font:700 24px/1 \'Golos Text\',sans-serif;color:#fff">192.168.1.42</div>'
    + '<div class="m4x-alg-o" style="top:431px;border:2px solid #f0d27a;background:rgba(40,70,50,.7);color:#f4f6ea;box-shadow:0 0 12px rgba(240,199,94,.6)">192.168.1.0/24<span style="position:absolute;right:12px;color:#fff">&#10003;</span></div>'
    + '<div class="m4x-alg-o" style="top:473px">192.168.0.0/16<span style="position:absolute;right:12px;top:11px;width:20px;height:20px;box-sizing:border-box;border:2px solid #8fa59b;border-radius:50%"></span></div>'
    + '<div class="m4x-alg-o" style="top:514px">0.0.0.0/0<span style="position:absolute;right:12px;top:11px;width:20px;height:20px;box-sizing:border-box;border:2px solid #8fa59b;border-radius:50%"></span></div>'
    + T(1164, 588, 300, "Выбирается наиболее<br>специфичный префикс<br>(самое длинное совпадение)").replace("22px/25px", "19.5px/23px")
    + arrow(1296, 425) + '</div>',
    '<div class="step">' + card(1336, 309, 5, 1488, "Пересылка", 291)
    + '<div class="m4x-alg-ring" style="left:1384px;top:352px;width:210px;height:210px;opacity:.7"></div>'
    + img("i_algo_rt.png", "left:1328px;top:416px") + img("i_algo_cube.png", "left:1520px;top:425px")
    + T(1490, 575, 300, "Выходной интерфейс.<br>Новая инкапсуляция<br>в кадр канального<br>уровня").replace("22px/25px", "19.5px/23px") + '</div>',
    '<div class="step"><div class="m4x-alg-warn"></div>'
    '<div style="position:absolute;left:421px;top:731px;width:44px;height:52px;box-sizing:border-box;border:2px solid #f0c75e;border-radius:50%;width:48px;height:48px;text-align:center;font:800 32px/44px \'Playfair Display\',serif;color:#f6d77a">!</div>'
    '<div style="position:absolute;left:503px;top:728px;font:600 23px/1.2 \'Golos Text\',sans-serif;color:#f4f6ea;white-space:nowrap">Нет подходящего маршрута — пакет отбрасывается.</div>'
    '<div style="position:absolute;left:503px;top:762px;font:400 17px/1.2 \'Golos Text\',sans-serif;color:#e0e8de;white-space:nowrap">Маршрут по умолчанию 0.0.0.0/0 считается подходящим, когда он присутствует.</div></div>',
])
