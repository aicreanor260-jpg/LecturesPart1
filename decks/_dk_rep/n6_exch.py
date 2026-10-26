# -*- coding: utf-8 -*-
"""NAT: как адреса выглядят в одном обмене — запрос и ответ (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img as _img

W, H, TOP = 1672, 941, 104

FADE = (";-webkit-mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 45%,transparent 100%)"
        ";mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 45%,transparent 100%)")


def img(f, st):
    return _img(f, st)


CSS = """<style>
.n6ex-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.75);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35)}
.n6ex-n{position:absolute;width:48px;height:48px;border-radius:50%;box-sizing:border-box;border:3px solid #5cd2ff;
  background:#0c2a66;color:#fff;font:800 28px/42px Montserrat,sans-serif;text-align:center;box-shadow:0 0 14px #3aa0ff}
.n6ex-h{position:absolute;font:800 28px/1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6ex-s{position:absolute;font:400 18px/1 "Golos Text",sans-serif;color:#b9d2f5;white-space:nowrap}
.n6ex-lb{position:absolute;box-sizing:border-box;text-align:center;font:700 22px/1.3 "Golos Text",sans-serif;color:#fff;
  background:rgba(8,22,56,.9);border:1.5px solid rgba(92,190,255,.5);border-radius:10px;padding-top:8px}
.n6ex-lb span{font:700 25px/1.2 "Golos Text",sans-serif}
.n6ex-pk{position:absolute;box-sizing:border-box;border-radius:8px;background:rgba(6,16,40,.92);padding:6px}
.n6ex-row{display:flex;gap:4px;margin-top:4px}
.n6ex-row:first-child{margin-top:0}
.n6ex-k{width:120px;height:40px;border-radius:5px;background:#3aa0ff;color:#0a1430;font:700 16px/40px "Golos Text",sans-serif;text-align:center}
.n6ex-k.r{background:#b77bff}
.n6ex-v{flex:1;height:40px;border-radius:5px;background:#9fdcff;color:#0a1430;font:600 22px/40px "Golos Text",sans-serif;text-align:center}
.n6ex-v.r{background:#dcc4ff}
.n6ex-cap{height:30px;margin:-6px -6px 6px;border-radius:7px 7px 0 0;color:#1a0c00;font:800 19px/30px Montserrat,sans-serif;text-align:center}
.n6ex-ok{position:absolute;box-sizing:border-box;border-radius:10px;background:#6ee07a;color:#0a2a10;
  font:700 16px/1.2 "Golos Text",sans-serif;white-space:nowrap;display:flex;align-items:center;gap:12px;padding:0 14px}
.n6ex-ok i{flex:none;width:34px;height:34px;border-radius:50%;background:#0a2a10;color:#6ee07a;font:900 22px/34px sans-serif;
  text-align:center;font-style:normal}
.n6ex-wire{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6ex-wire .fl{fill:none;stroke:#5cd2ff;stroke-width:4;filter:drop-shadow(0 0 6px #3aa0ff);stroke-dasharray:14 8;animation:n6exd 1s linear infinite}
.n6ex-wire .bk{animation-direction:reverse}
.n6ex-wire .ah{fill:#5cd2ff}
@keyframes n6exd{to{stroke-dashoffset:-44}}
.n6ex-c{position:absolute;box-sizing:border-box;border-radius:8px;background:rgba(6,16,40,.92);border:1px solid rgba(92,190,255,.3)}
.n6ex-ct{height:50px;border-radius:7px 7px 0 0;font:700 22px/1.05 "Golos Text",sans-serif;color:#0a1430;padding:4px 10px 0}
.n6ex-ct span{display:block;font:700 16px/1.1 "Golos Text",sans-serif}
.n6ex-cd{white-space:nowrap;font:400 13px/1.3 "Golos Text",sans-serif;color:#b9d2f5;padding:8px 12px}
</style>"""


def pk(x, y, w, s, d, cap="", capc="", rs=False):
    head = '<div class="n6ex-cap" style="background:%s">%s</div>' % (capc, cap) if cap else ""
    bd = "border:2.5px solid %s;" % capc if cap else "border:1.5px solid rgba(92,190,255,.5);"
    return ('<div class="n6ex-pk" style="left:%dpx;top:%dpx;width:%dpx;%s">%s'
            '<div class="n6ex-row"><div class="n6ex-k">Отправитель</div><div class="n6ex-v">%s</div></div>'
            '<div class="n6ex-row"><div class="n6ex-k r">Получатель</div><div class="n6ex-v r">%s</div></div></div>'
            % (x, y, w, bd, head, s, d))


def node(x, y, w, name, ip):
    return '<div class="n6ex-lb" style="left:%dpx;top:%dpx;width:%dpx;height:70px">%s<br><span>%s</span></div>' % (x, y, w, name, ip)


def card(x, w, col, ip, name, desc):
    return ('<div class="n6ex-c" style="left:%dpx;top:770px;width:%dpx;height:132px"><div class="n6ex-ct" style="background:%s">%s'
            '<span>%s</span></div><div class="n6ex-cd">%s</div></div>' % (x, w, col, ip, name, desc))


ROW1 = ('<div class="step"><div class="n6ex-p" style="left:40px;top:110px;width:1590px;height:310px"></div>'
        '<div class="n6ex-n" style="left:62px;top:122px">1</div>'
        '<div class="n6ex-h" style="left:134px;top:122px">Исходящий пакет (к сайту)</div>'
        '<div class="n6ex-s" style="left:136px;top:156px">Компьютер отправляет запрос на сервер в интернете</div>'
        + img("n6_exch_pc.png", "left:62px;top:198px;width:240px")
        + img("n6_exch_rt.png", "left:732px;top:188px;width:200px")
        + img("n6_exch_srv.png", "left:1378px;top:152px;width:234px")
        + node(62, 337, 250, "Компьютер", "192.168.1.10")
        + '<div class="n6ex-lb" style="left:704px;top:333px;width:262px;height:50px;padding-top:12px">Маршрутизатор NAT</div>'
        + node(1365, 337, 245, "Сервер", "203.0.113.20")
        + '<svg class="n6ex-wire"><path class="fl" d="M232 270H360M678 270H726M928 270H980M1300 270H1370"/>'
          '<path class="ah" d="M356 258l20 12-20 12zM722 258l20 12-20 12zM976 258l20 12-20 12zM1366 258l20 12-20 12z"/></svg></div>')
PK1 = ('<div class="step">' + pk(380, 190, 298, "192.168.1.10", "203.0.113.20", "ДО NAT", "#ffc94a") + '</div>'
       '<div class="step">' + pk(994, 176, 306, "198.51.100.7", "203.0.113.20", "ПОСЛЕ NAT", "#ff8a3d")
       + '<div class="n6ex-ok" style="left:994px;top:322px;width:306px;height:62px"><i>&#10003;</i>Адрес компьютера заменён;<br>адрес сайта прежний</div></div>')
ROW2 = ('<div class="step"><div class="n6ex-p" style="left:40px;top:432px;width:1590px;height:304px"></div>'
        '<div class="n6ex-n" style="left:62px;top:448px">2</div>'
        '<div class="n6ex-h" style="left:136px;top:450px">ОТВЕТ СЕРВЕРА</div>'
        '<div class="n6ex-s" style="left:138px;top:481px">Сервер отправляет ответ на внешний адрес маршрутизатора</div>'
        + img("n6_exch_pc.png", "left:62px;top:522px;width:240px")
        + img("n6_exch_rt.png", "left:740px;top:530px;width:200px")
        + img("n6_exch_srv.png", "left:1378px;top:464px;width:234px")
        + node(62, 656, 250, "Компьютер", "192.168.1.10")
        + '<div class="n6ex-lb" style="left:710px;top:666px;width:265px;height:50px;padding-top:12px">Маршрутизатор NAT</div>'
        + node(1365, 656, 245, "Сервер", "203.0.113.20")
        + '<svg class="n6ex-wire"><path class="fl bk" d="M250 591H372M680 591H736M948 591H1008M1306 591H1370"/>'
          '<path class="ah" d="M256 579l-20 12 20 12zM702 579l-20 12 20 12zM1026 579l-20 12 20 12zM1328 579l-20 12 20 12z"/></svg></div>')
PK2 = ('<div class="step">' + pk(1010, 522, 290, "203.0.113.20", "192.168.1.10") + '</div>'
       '<div class="step"><div class="n6ex-c" style="left:708px;top:453px;width:268px;height:122px;border-color:rgba(92,190,255,.6)"></div>'
       '<div style="position:absolute;left:708px;top:462px;width:268px;text-align:center;font:700 20px/1 \'Golos Text\',sans-serif;color:#fff">Таблица NAT</div>'
       '<div style="position:absolute;left:717px;top:492px;width:250px;height:36px;box-sizing:border-box;border:1px solid rgba(92,190,255,.6);'
       'border-radius:6px;font:500 15px/34px \'JetBrains Mono\',monospace;color:#fff;text-align:center">198.51.100.7 &#8596; 192.168.1.10</div>'
       '<div style="position:absolute;left:708px;top:533px;width:268px;text-align:center;font:400 14px/1.25 \'Golos Text\',sans-serif;color:#b9d2f5">'
       'Поиск и перевод<br>адреса назначения</div></div>'
       '<div class="step">' + pk(374, 522, 304, "203.0.113.20", "198.51.100.7")
       + '<div class="n6ex-ok" style="left:405px;top:643px;width:276px;height:42px"><i>&#10003;</i>Получатель: 192.168.1.10</div>'
       '<svg class="n6ex-wire"><path d="M681 664q30 0 40-22h20" fill="none" stroke="#6ee07a" stroke-width="2"/></svg></div>')
LEG = ('<div class="step"><div class="n6ex-p" style="left:40px;top:748px;width:1590px;height:168px"></div>'
       '<div class="n6ex-h" style="left:62px;top:760px;font:700 25px Montserrat,sans-serif">Пояснение адресов</div>'
       + card(405, 170, "#9fdcff", "192.168.1.10", "", "Адрес компьютера<br>в локальной сети<br>(частный адрес)")
       + card(586, 220, "#ffc94a", "198.51.100.7", "Inside global",
              "Внешний адрес<br>маршрутизатора NAT<br><span style='font-size:12px'>(под которым виден компьютер<br>в интернете)</span>")
       + card(817, 236, "#b77bff", "203.0.113.20", "Outside local",
              "Адрес сервера, каким его видит<br>внутренняя сеть (в этом примере<br>такой же, как глобальный)")
       + card(1065, 225, "#6ee07a", "203.0.113.20", "Outside global",
              "Реальный адрес сервера<br>в интернете (в этом примере<br>такой же, как outside local)")
       + '<div class="n6ex-c" style="left:1310px;top:765px;width:302px;height:110px;border-color:rgba(92,190,255,.5)"></div>'
       '<div style="position:absolute;left:1328px;top:782px;width:38px;height:38px;border-radius:50%;border:2.5px solid #5cd2ff;'
       'color:#5cd2ff;font:800 24px/36px Montserrat,sans-serif;text-align:center;box-sizing:border-box">i</div>'
       '<div style="position:absolute;left:1390px;top:778px;font:400 15px/1.4 \'Golos Text\',sans-serif;color:#fff;white-space:nowrap">'
       '<span style="font-size:17px">В этом простом примере</span><br>адрес сервера одинаковый:<br>Outside local = Outside global =<br>203.0.113.20</div></div>')

HTML = CSS + bg("bgk_space") + ROW1 + PK1 + ROW2 + PK2 + LEG
