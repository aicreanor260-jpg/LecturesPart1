# -*- coding: utf-8 -*-
"""2.6: Inside global — внутренний глобальный адрес (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 140

CSS = """<style>
.n6ig-p{position:absolute;box-sizing:border-box;border-radius:14px;border:1.5px solid rgba(92,190,255,.6);
  background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));box-shadow:0 0 22px rgba(58,160,255,.3)}
.n6ig-t{position:absolute;white-space:nowrap;font:700 17.5px/1.2 Montserrat,sans-serif;color:#fff}
.n6ig-s{position:absolute;white-space:nowrap;font:400 17px/1.4 "Golos Text",sans-serif;color:#b9d2f5}
.n6ig-k{position:absolute;box-sizing:border-box;border-radius:8px;border:1px solid rgba(92,190,255,.35);background:rgba(4,12,32,.7);
  font:400 16.5px/1.45 "Golos Text",sans-serif;color:#d6e4fa;padding:6px 12px;white-space:nowrap}
.n6ig-k em{font-style:normal;color:#5cd2ff;font-weight:700}
.n6ig-k .ip{font:700 18px/1 "JetBrains Mono",monospace}
.n6ig-fly{position:absolute;width:16px;height:12px;margin:-6px -8px;border-radius:3px}
.n6ig-bl{background:#7fe0ff;box-shadow:0 0 12px #3aa0ff}
.n6ig-vi{background:#d6a8ff;box-shadow:0 0 12px #b77bff}
.n6ig-m1{offset-path:path("M262 420H690M916 420H1400");animation:n6igm 3.6s linear infinite}
.n6ig-m2{offset-path:path("M1472 545V612H1000M620 612H245V545");animation:n6igm 3.6s linear infinite 1.8s}
@keyframes n6igm{from{offset-distance:0%}to{offset-distance:100%}}
</style>"""

ENVSVG = '<svg viewBox="0 0 44 30" style="position:absolute;left:%dpx;top:%dpx;width:44px;height:30px"><rect x="1.5" y="1.5" width="41" height="27" rx="3" ' \
         'style="fill:%s;stroke:%s" stroke-width="3"/><path d="M3 4L22 18L41 4" fill="none" style="stroke:%s" stroke-width="3"/></svg>'


def env(x, y, blue=True):
    c = ("#123a7a", "#7fe0ff") if blue else ("#3a1f78", "#d6a8ff")
    return ENVSVG % (x - 22, y - 15, c[0], c[1], c[1])


def panel(x, y, w, h, title, rows):
    return ('<div class="n6ig-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>' % (x, y, w, h)
            + '<div class="n6ig-t" style="left:%dpx;top:%dpx">%s</div>' % (x + 20, y + 12, title)
            + '<div class="n6ig-k" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (x + 10, y + (60 if "<br>" in title else 42), w - 20, rows))


HTML = CSS + bg("bgk_globe") + "".join([
    '<div class="step"><div class="n6ig-p" style="left:34px;top:40px;width:1604px;height:648px;background:rgba(8,18,44,.4);box-shadow:none"></div>'
    '<div class="n6ig-s" style="left:78px;top:145px;font:500 27px/1.3 \'Golos Text\',sans-serif;color:#9fb6e0">'
    'Публичный адрес, под которым внутреннее устройство<br>представлено во внешней сети.</div></div>',
    # концы
    '<div class="step"><div class="n6ig-p" style="left:46px;top:232px;width:258px;height:452px"></div>'
    '<div class="n6ig-t" style="left:46px;top:256px;width:258px;text-align:center;font-size:21px">Внутренняя сеть</div>'
    '<div class="n6ig-s" style="left:46px;top:286px;width:258px;text-align:center">Частный IP</div>'
    + img("n6_ig_lap.png", "left:78px;top:348px;width:236px") +
    '<div class="n6ig-t" style="left:46px;top:538px;width:222px;text-align:center">Компьютер</div>'
    '<div class="n6ig-t" style="left:46px;top:566px;width:222px;text-align:center;font:700 22px/1.2 \'JetBrains Mono\',monospace">192.168.1.10</div>'
    '<div class="n6ig-p" style="left:1378px;top:232px;width:248px;height:452px"></div>'
    '<div class="n6ig-t" style="left:1378px;top:256px;width:248px;text-align:center;font-size:21px">Интернет</div>'
    '<div class="n6ig-s" style="left:1378px;top:286px;width:248px;text-align:center">Внешний сервер</div>'
    + img("n6_ig_srv.png", "left:1425px;top:328px;width:167px") + '</div>',
    # исходящий
    '<div class="step"><svg style="position:absolute;left:0;top:0;width:1672px;height:941px" fill="none" stroke-width="4">'
    '<path d="M262 420H690M916 420H1400" stroke="#5cd2ff" style="filter:drop-shadow(0 0 5px #3aa0ff)"/>'
    '<path d="M680 408l18 12-18 12M1396 408l18 12-18 12" stroke="#5cd2ff"/></svg>'
    + img("n6_ig_rt.png", "left:702px;top:308px;width:213px") +
    '<div class="n6ig-t" style="left:784px;top:302px;font-size:22px">NAT</div>'
    + panel(363, 242, 296, 156, "Исходящий пакет<br>до NAT",
            'Источник:&nbsp; <em class="ip">192.168.1.10</em><br>Назначение:&nbsp; внешний сервер<br>Данные: …')
    + env(512, 420) + '<div class="n6ig-fly n6ig-bl n6ig-m1"></div></div>',
    '<div class="step">' + panel(950, 235, 302, 166, "Исходящий пакет<br>после NAT",
                                 'Источник:&nbsp;&nbsp; <em>публичный адрес<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;маршрутизатора</em>'
                                 '<br>Назначение:&nbsp; внешний сервер<br>Данные: …')
    + env(1130, 420) +
    '<div class="n6ig-p" style="left:980px;top:438px;width:369px;height:56px;border:2px solid #3ad6c8;background:rgba(8,50,60,.85)"></div>'
    '<div class="n6ig-t" style="left:980px;top:445px;width:369px;text-align:center;font:600 17px/1.25 \'Golos Text\',sans-serif">'
    'Именно этот публичный адрес<br>видит внешний сервер как источник.</div></div>',
    # ответ
    '<div class="step"><svg style="position:absolute;left:0;top:0;width:1672px;height:941px" fill="none" stroke-width="4">'
    '<path d="M1472 545V612H1355M1060 612H998M624 612H610M342 612H245V545" stroke="#b77bff" style="filter:drop-shadow(0 0 5px #b77bff)"/>'
    '<path d="M270 604l-12 8 12 8" stroke="#b77bff"/></svg>'
    + panel(1060, 510, 294, 162, "Ответный пакет от сервера",
            'Источник:&nbsp;&nbsp;&nbsp; внешний сервер<br>Назначение:&nbsp; <em>публичный адрес<br>'
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;маршрутизатора</em><br>Данные: …')
    + env(1032, 614, False) + '<div class="n6ig-fly n6ig-vi n6ig-m2"></div></div>',
    # таблица
    '<div class="step"><div class="n6ig-p" style="left:625px;top:498px;width:372px;height:186px"></div>'
    '<div class="n6ig-t" style="left:625px;top:510px;width:372px;text-align:center">Таблица соответствий NAT</div>'
    '<table style="position:absolute;left:636px;top:540px;width:350px;border-collapse:collapse;font:400 12.5px/1.2 \'Golos Text\',sans-serif;color:#b9d2f5">'
    '<tr style="height:30px"><td style="border:1px solid rgba(92,190,255,.35);text-align:center">Публичный адрес</td>'
    '<td style="border:1px solid rgba(92,190,255,.35);width:60px"></td><td style="border:1px solid rgba(92,190,255,.35);text-align:center">Внутренний адрес</td></tr>'
    '<tr style="height:54px"><td style="border:1px solid rgba(92,190,255,.35);text-align:center;color:#5cd2ff;font-weight:700">публичный адрес<br>маршрутизатора</td>'
    '<td style="border:1px solid rgba(92,190,255,.35);text-align:center;color:#fff;font-size:22px">&#8596;</td>'
    '<td style="border:1px solid rgba(92,190,255,.35);text-align:center;color:#fff;font:500 17px \'JetBrains Mono\',monospace">192.168.1.10</td></tr></table>'
    '<div class="n6ig-s" style="left:625px;top:636px;width:372px;text-align:center;font-size:15.5px;line-height:1.3">'
    'NAT определяет получателя<br>и пересылает ответ.</div></div>',
    '<div class="step">' + panel(342, 513, 268, 152, "Пакет после NAT<br>к внутреннему компьютеру",
                                 'Источник:&nbsp;&nbsp;&nbsp; внешний сервер<br>Назначение:&nbsp; <em class="ip">192.168.1.10</em><br>Данные: …')
    + env(312, 618, False) + '</div>',
    # низ
    '<div class="step"><div class="n6ig-p" style="left:34px;top:717px;width:527px;height:182px"></div>'
    + img("n6_ig_glob.png", "left:56px;top:738px;width:126px") +
    '<div class="n6ig-t" style="left:193px;top:738px;font:800 34px/1.1 Montserrat,sans-serif">Inside global</div>'
    '<div class="n6ig-s" style="left:199px;top:786px;font-size:20.5px">Публичный адрес, под которым<br>внутреннее устройство<br>представлено во внешней сети.</div>'
    '<div class="n6ig-p" style="left:570px;top:717px;width:454px;height:182px"></div>'
    + img("n6_ig_shield.png", "left:596px;top:738px;width:102px") +
    '<div class="n6ig-t" style="left:728px;top:738px;font-size:22px">Что делает NAT</div>'
    '<div class="n6ig-s" style="left:729px;top:772px;font-size:17.5px;line-height:1.3">Подменяет исходный<br>частный адрес на публичный,<br>'
    'запоминает соответствие<br>и возвращает ответы<br>нужному устройству.</div>'
    '<div class="n6ig-p" style="left:1033px;top:717px;width:605px;height:182px"></div>'
    + img("n6_ig_lg.png", "left:1052px;top:768px;width:240px") +
    '<div style="position:absolute;left:1309px;top:738px;width:316px;height:140px;border-radius:12px;background:#8fdcff;box-shadow:0 0 22px rgba(92,210,255,.5)"></div>'
    '<div class="n6ig-t" style="left:1340px;top:758px;font:800 24px/1.3 Montserrat,sans-serif;color:#0c1a4a">Адрес внутреннего<br>компьютера для<br>внешнего мира.</div></div>',
])
