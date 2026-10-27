# -*- coding: utf-8 -*-
"""pptx: Класс эквивалентности пересылки (FEC) — вёрстка поверх bgk_25."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 66

CSS = """<style>
.i13-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i13-t{position:absolute;font:500 22px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i13-t b{font-weight:800;color:#13306e}
.i13-h{position:absolute;font:900 29px/1 "Rubik",sans-serif;color:#13306e}
.i13-c{position:absolute;font:700 19px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i13-bx{position:absolute;border:2px solid #1d3f8a;border-radius:6px;background:#fff;font:600 14px/1.15 "Golos Text",sans-serif;color:#13306e;
 display:flex;align-items:center;justify-content:center;text-align:center}
.i13-ar{position:absolute;height:3px;background:#1d3f8a}
.i13-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #1d3f8a;border-right:0}
.i13-pk{position:absolute;height:40px;border:2px solid #1d3f8a;border-left:8px solid #8cbde6;border-radius:3px;background:#fff;
 font:500 18px/36px "Golos Text",sans-serif;color:#13306e;padding:0 14px}
.i13-lb{position:absolute;display:flex;height:42px;border:2px solid #1d3f8a;border-radius:3px;overflow:hidden;font:600 18px/38px "Golos Text",sans-serif}
.i13-lb b{background:#f2694a;padding:0 8px;font-weight:600;color:#1d1d1d}.i13-lb i{background:#fff;padding:0 10px;font-style:normal;color:#13306e}
.i13-fly{animation:i13f 3s ease-in-out infinite}
@keyframes i13f{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}
.i13-f{position:absolute;font:500 17px/1.2 "Golos Text",sans-serif;color:#1d2a44;width:400px}
.i13-f b{display:block;font:800 21px/1.2 "Golos Text",sans-serif;color:#13306e}
.i13-tb{position:absolute;border-collapse:collapse;font:500 19px/27px "Golos Text",sans-serif;color:#1d2a44;border:2px solid #1d3f8a}
.i13-tb td,.i13-tb th{border-top:2px solid #1d3f8a;padding:0 0 0 64px;text-align:left}
.i13-tb th{background:#bfe9e4;font-weight:700;color:#13306e}
.i13-tb td+td,.i13-tb th+th{border-left:2px solid #1d3f8a;padding-left:12px}
</style>"""


def ar(x, y, w):
    return '<div class="i13-ar" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x, y, w)


def feat(x, y, ic, h, t):
    return img(ic, "left:%dpx;top:%dpx;width:76px" % (x, y)) + \
        '<div class="i13-f" style="left:%dpx;top:%dpx"><b>%s</b>%s</div>' % (x + 106, y + 2, h, t)


HTML = CSS + bg("bgk_25") + "".join([
    '<div class="step"><div style="position:absolute;left:340px;top:72px;width:1000px;white-space:nowrap;text-align:center;font:800 30px/1.2 Rubik,sans-serif;color:#fffbe8;text-shadow:0 2px 0 #1550a8,0 3px 8px rgba(10,40,90,.5)"><span style="display:inline-block;width:180px;height:2px;background:#fffbe8;vertical-align:middle;margin-right:16px"></span>Forwarding Equivalence Class<span style="display:inline-block;width:180px;height:2px;background:#fffbe8;vertical-align:middle;margin-left:16px"></span></div></div>',
    '<div class="step">',
    '<div class="i13-p" style="left:232px;top:118px;width:1222px;height:108px"></div>',
    '<div class="i13-t" style="left:266px;top:128px;width:760px"><b>FEC — группа пакетов с одинаковыми признаками пересылки<br>'
    '&nbsp; &nbsp; &nbsp; &nbsp; относительно текущего узла MPLS-домена.</b><br>&nbsp; &nbsp; &nbsp; &nbsp; Пакеты одного FEC пересылаются одинаковым способом.</div>',
    '<div class="i13-t" style="left:1042px;top:132px;width:398px;height:82px;background:#ccefea;border-radius:14px;padding:10px 20px;line-height:1.2;font-size:21px">'
    '<b>Простейший случай:</b> пакеты,<br>адресованные одной IP-подсети.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i13-p" style="left:212px;top:238px;width:1270px;height:226px"></div>',
    '<div class="i13-h" style="left:238px;top:250px">КЛАССИФИКАЦИЯ НА ВХОДНОМ LER</div>',
    '<div class="i13-pk" style="left:236px;top:304px">192.0.2.10</div>',
    '<div class="i13-pk" style="left:236px;top:372px">192.0.2.20</div>',
    '<svg style="position:absolute;left:356px;top:318px" width="60" height="80"><path d="M0 4 Q30 4 48 26 M0 74 Q30 74 48 46" '
    'style="fill:none;stroke:#1d3f8a;stroke-width:3"/><path d="M40 18 L52 30 L36 32Z M40 54 L52 42 L36 40Z" style="fill:#1d3f8a"/></svg>',
    img("i13a_rt.png", "left:412px;top:326px;width:106px"),
    '<div class="i13-c" style="left:390px;top:398px;width:150px;font:900 26px/1 Golos Text,sans-serif">LER</div>',
    '<div class="i13-c" style="left:390px;top:426px;width:150px;font-weight:500">Входной узел</div>',
    ar(522, 364, 26),
    '<div style="position:absolute;left:540px;top:286px;width:626px;height:140px;background:#ccefea;border-radius:16px"></div>',
    '<div class="i13-c" style="left:600px;top:294px;width:240px;font-size:21px">Классификация</div>',
    '<div class="i13-bx" style="left:554px;top:332px;width:138px;height:66px;justify-content:flex-start;padding-left:58px;text-align:left">База<br>классов FEC</div>',
    img("i13a_db.png", "left:562px;top:340px;width:46px"),
    ar(694, 364, 18),
    '<div class="i13-bx" style="left:716px;top:332px;width:138px;height:66px;justify-content:flex-start;padding-left:58px;text-align:left">Проверка<br>признаков<br>пакета</div>',
    img("i13a_mg.png", "left:722px;top:340px;width:46px"),
    ar(856, 364, 18),
    '<div class="i13-bx" style="left:878px;top:334px;width:102px;height:62px;background:#f7a99a">FEC:<br>192.0.2.0/24</div>',
    ar(982, 364, 18),
    '<div class="i13-bx" style="left:1004px;top:334px;width:54px;height:62px;background:#8cc8f0;font-size:19px;font-weight:700">FTN</div>',
    ar(1060, 364, 18),
    '<div class="i13-lb i13-fly" style="left:1082px;top:344px"><b>100</b><i>IP</i></div>',
    ar(1166, 364, 18),
    '<div style="position:absolute;left:1192px;top:314px;width:254px;height:10px;border:2px solid #1d3f8a;border-bottom:0;border-radius:6px 6px 0 0"></div>',
    '<div class="i13-c" style="left:1192px;top:290px;width:254px">Выбранный LSP</div>',
    img("i13a_rts.png", "left:1190px;top:338px;width:70px"), ar(1262, 364, 22),
    img("i13a_rts.png", "left:1288px;top:338px;width:70px"), ar(1360, 364, 22),
    img("i13a_rts.png", "left:1384px;top:338px;width:70px"),
    '<div class="i13-c" style="left:1452px;top:350px;width:26px">…</div>',
    '<div class="i13-c" style="left:540px;top:432px;width:626px">LER определяет FEC и связывает его с путём LSP.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i13-p" style="left:334px;top:476px;width:1000px;height:266px"></div>',
    '<div class="i13-h" style="left:360px;top:488px">ПО КАКИМ ПРИЗНАКАМ ВЫБИРАЮТ FEC</div>',
    '<div style="position:absolute;left:836px;top:524px;width:2px;height:204px;background:#7ad6cc"></div>',
    feat(368, 518, "i13a_c1.png", "IP-адрес назначения", "Отдельный FEC для префикса;<br>LDP распределяет метки для FEC."),
    feat(368, 598, "i13a_c2.png", "Принадлежность к VPN", "Разделение трафика виртуальных<br>частных сетей клиентов."),
    feat(368, 678, "i13a_c3.png", "Входной интерфейс", "Учитывается интерфейс поступления пакета."),
    feat(868, 518, "i13a_c4.png", "Требования Traffic Engineering", "Классификация для распределения<br>нагрузки по каналам."),
    feat(868, 598, "i13a_c5.png", "Тип приложения", "Например, RTP-трафик и веб-трафик."),
    feat(868, 668, "i13a_c6.png", "MAC-адрес назначения", "Для Ethernet-сервисов учитываются<br>признаки кадра."),
    '</div>',
    '<div class="step">',
    '<div class="i13-p" style="left:334px;top:750px;width:1000px;height:128px"></div>',
    '<div class="i13-h" style="left:362px;top:758px;font:800 25px/1 Golos Text,sans-serif">Пример соответствия FEC и меток</div>',
    '<table class="i13-tb" style="left:404px;top:788px;width:868px"><tr><th style="width:620px">Признаки FEC</th><th>Метка</th></tr>'
    '<tr><td>123.20.0.0/16; 195.14.0.0/16</td><td>106</td></tr><tr><td>194.20.0.0/24; eth1</td><td>107</td></tr></table>',
    '<div class="i13-p" style="left:206px;top:884px;width:1262px;height:52px;border-radius:14px"></div>',
    '<div class="i13-c" style="left:248px;top:892px;width:112px;height:38px;background:#2a78d0;color:#fff;border-radius:8px;font:900 26px/38px Golos Text,sans-serif">FTN</div>',
    '<div class="i13-t" style="left:392px;top:888px;width:620px;border-left:2px solid #1d3f8a;padding-left:26px;font-size:17px;line-height:1.1">'
    '<b style="font-size:20px">FTN — FEC To Next Hop</b><br>Связывает класс FEC со следующим хопом и операцией с меткой.</div>',
    '<div class="i13-t" style="left:1042px;top:888px;width:416px;background:#ccefea;border-radius:10px;padding:2px 22px;font-size:16px;line-height:1.2">'
    'Классификация может учитывать<br>IP-поля, MAC-адреса и входной интерфейс.</div>',
    '</div>',
])
