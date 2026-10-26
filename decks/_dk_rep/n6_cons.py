# -*- coding: utf-8 -*-
"""2.6: недостатки NAT — четыре панели и итог (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 132

CSS = """<style>
.n6co-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.6);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.3)}
.n6co-n{position:absolute;width:64px;height:58px;border-radius:10px;font:800 38px/58px Montserrat,sans-serif;color:#111;text-align:center}
.n6co-h{position:absolute;font:800 33px/1.05 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6co-ib{position:absolute;width:72px;height:72px;border-radius:12px;background:rgba(40,50,70,.75)}
.n6co-t{position:absolute;font:500 17.5px/1.35 "Golos Text",sans-serif;color:#e6eefc;white-space:nowrap}
.n6co-tag{position:absolute;box-sizing:border-box;border:1.5px solid rgba(140,190,255,.55);border-radius:8px;background:rgba(14,26,52,.85);
  font:500 14px/1.25 "Golos Text",sans-serif;color:#dbe6fa;text-align:center;padding:4px 8px;white-space:nowrap}
.n6co-l{position:absolute;font:600 16px/1 "Golos Text",sans-serif;color:#fff;white-space:nowrap}
.n6co-sv{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none;overflow:visible}
.n6co-fl{stroke-dasharray:9 7;animation:n6cod 1s linear infinite}
@keyframes n6cod{to{stroke-dashoffset:-32}}
.n6co-pk{position:absolute;width:20px;height:10px;border-radius:2px;background:#2fe07a;box-shadow:0 0 8px #2fe07a;animation:n6cop 2.4s linear infinite}
@keyframes n6cop{from{transform:translateX(0)}to{transform:translateX(52px);opacity:.2}}
.n6co-x{animation:n6cox 1.4s ease-in-out infinite}
@keyframes n6cox{50%{opacity:.45}}
</style>"""


def panel(x, y, w, h, num, col, title, lines=1):
    t = '<div class="n6co-p" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>' % (x, y, w, h)
    t += '<div class="n6co-n" style="left:%dpx;top:%dpx;background:%s;box-shadow:0 0 14px %s">%s</div>' % (x + 22, y + 16, col, col, num)
    t += '<div class="n6co-h" style="left:%dpx;top:%dpx">%s</div>' % (x + 115, y + (26 if lines == 1 else 18), title)
    return t


def row(x, y, ico, text, ty=0):
    return ('<div class="n6co-ib" style="left:%dpx;top:%dpx"></div>' % (x, y) + img(ico, "left:%dpx;top:%dpx;width:72px" % (x, y))
            + '<div class="n6co-t" style="left:%dpx;top:%dpx">%s</div>' % (x + 86, y + ty, text))


def tag(x, y, w, text, st=""):
    return '<div class="n6co-tag" style="left:%dpx;top:%dpx;width:%dpx;%s">%s</div>' % (x, y, w, st, text)


def lbl(x, y, text):
    return '<div class="n6co-l" style="left:%dpx;top:%dpx">%s</div>' % (x, y, text)


SV = '<svg class="n6co-sv" viewBox="0 0 1672 941">%s</svg>'

P1 = ('<div class="step">' + panel(28, 138, 831, 333, "1", "#ffd84a", "Дополнительная задержка")
      + row(45, 240, "n6_cons_gear.png", "Маршрутизатор анализирует<br>пакет, меняет IPv4- и иногда<br>TCP/UDP-заголовки, затем<br>пересчитывает контрольные суммы", -2)
      + row(45, 360, "n6_cons_clock.png", "Первый пакет может<br>обрабатываться программно<br>и идти медленнее", 8)
      + '<div class="n6co-p" style="left:564px;top:204px;width:172px;height:136px;border-radius:8px;background:rgba(20,40,80,.8)"></div>'
      + '<div style="position:absolute;left:578px;top:216px;font:500 13px/1.25 \'Golos Text\',sans-serif;color:#dbe6fa">'
        '<div style="margin-bottom:12px">&#9635; Анализ пакета</div><div style="margin-bottom:10px">&#9635; Замена адресов<br>&nbsp;&nbsp;&nbsp;&nbsp;(и портов)</div>'
        '<div>&#9635; Пересчёт<br>&nbsp;&nbsp;&nbsp;&nbsp;контрольных сумм</div></div>'
      + img("n6_cons_lap.png", "left:385px;top:352px;width:81px") + img("n6_cons_rt.png", "left:525px;top:330px;width:157px")
      + img("n6_cons_cloud.png", "left:735px;top:330px;width:110px")
      + SV % '<path class="n6co-fl" d="M682 404H728" stroke="#2fe07a" stroke-width="3" fill="none"/><path d="M728 404l-10-6v12z" fill="#2fe07a"/>'
      + '<div class="n6co-pk" style="left:466px;top:377px"></div>'
      + lbl(754, 410, "Интернет") + '</div>')

P2 = ('<div class="step">' + panel(880, 138, 768, 333, "2", "#ff8a6a", "Проблемы с P2P")
      + row(900, 238, "n6_cons_p2p.png", "Прямое соединение<br>между устройствами<br>за разными NAT<br>затруднено", 2)
      + row(900, 358, "n6_cons_pad.png", "VoIP и онлайн-играм<br>могут потребоваться<br>дополнительные<br>настройки", 6)
      + tag(1342, 190, 172, "Прямое соединение<br>затруднено", "border-color:#ff6a5a;color:#ffd8d0")
      + img("n6_cons_lapa.png", "left:1195px;top:265px;width:105px") + img("n6_cons_lapb.png", "left:1540px;top:265px;width:88px")
      + '<div class="n6co-x">' + img("n6_cons_xcloud.png", "left:1360px;top:238px;width:112px") + '</div>'
      + img("n6_cons_srv.png", "left:1372px;top:318px;width:70px")
      + SV % ('<path class="n6co-fl" d="M1360 272C1330 278 1305 285 1290 296M1470 272C1500 278 1520 285 1534 294" stroke="#ff5a4a" stroke-width="3" fill="none"/>'
              '<path class="n6co-fl" d="M1300 336C1330 350 1350 360 1372 355M1442 355C1470 360 1500 345 1520 334" stroke="#4ce060" stroke-width="3" fill="none"/>')
      + tag(1210, 358, 66, "NAT A") + tag(1543, 358, 66, "NAT B")
      + tag(1298, 392, 222, "Иногда требуется<br>дополнительная настройка<br>(например, STUN/TURN)") + '</div>')

P3 = ('<div class="step">' + panel(28, 490, 831, 311, "3", "#b97bff", "Сложнее трассировать")
      + row(45, 595, "n6_cons_pin.png", "При нескольких NAT<br>адреса меняются<br>по пути", 4)
      + row(45, 700, "n6_cons_find.png", "Поиск причины сбоя<br>становится сложнее", 14)
      + tag(340, 583, 124, "Частная сеть<br>(внутренний IP)") + tag(474, 583, 104, "NAT 1<br>(публичный IP)")
      + tag(588, 583, 150, "NAT 2<br>(другой публичный IP)")
      + img("n6_cons_lap3.png", "left:328px;top:645px;width:100px")
      + img("n6_cons_r3.png", "left:438px;top:648px;width:64px") + img("n6_cons_r3.png", "left:538px;top:648px;width:64px")
      + img("n6_cons_r3.png", "left:638px;top:648px;width:64px") + img("n6_cons_cloud.png", "left:735px;top:622px;width:110px")
      + SV % ('<g stroke="#3ad8ff" stroke-width="3" fill="#3ad8ff"><path class="n6co-fl" d="M402 676H432M502 676H532M602 676H632M702 676H730" fill="none"/>'
              '<path d="M438 676l-10-6v12zM538 676l-10-6v12zM638 676l-10-6v12zM736 676l-10-6v12z"/></g>'
              '<path d="M466 712C470 735 520 742 568 742C620 742 668 735 670 712" stroke="#8ab0e0" stroke-width="2" stroke-dasharray="6 5" fill="none"/>'
              '<path d="M568 712V738" stroke="#8ab0e0" stroke-width="2" fill="none"/>')
      + tag(459, 738, 246, "Реальные адреса устройств<br>скрыты за NAT") + lbl(753, 700, "Интернет") + '</div>')

P4 = ('<div class="step">' + panel(880, 490, 768, 311, "4", "#7ef06a", "<span style='font-size:30px'>Ограничения входящих<br>соединений</span>", 2)
      + row(900, 598, "n6_cons_shield.png", "Без настроек NAT входящий<br>TCP- или UDP-трафик может<br>не дойти до устройства", 4)
      + row(900, 700, "n6_cons_gear2.png", "Некоторым протоколам<br>нужна поддержка NAT<br>или переадресация портов", 6)
      + img("n6_cons_inet.png", "left:1385px;top:500px;width:107px") + img("n6_cons_nat.png", "left:1335px;top:636px;width:157px")
      + img("n6_cons_mon.png", "left:1250px;top:718px;width:72px") + img("n6_cons_game.png", "left:1352px;top:702px;width:110px")
      + img("n6_cons_box.png", "left:1492px;top:706px;width:80px")
      + tag(1488, 556, 160, "Работает при настройке<br>(например, переадресация<br>портов)", "font-size:12px;border-color:#5ce06a;color:#d8ffd8;text-align:left")
      + SV % ('<path d="M1415 566V650" stroke="#ff4a4a" stroke-width="3" fill="none"/><path d="M1415 656l-6-10h12z" fill="#ff4a4a"/>'
              '<g class="n6co-x"><circle cx="1415" cy="602" r="15" fill="#c81e2e" stroke="#ff8a8a" stroke-width="2"/>'
              '<path d="M1408 595l14 14M1422 595l-14 14" stroke="#fff" stroke-width="3"/></g>'
              '<path class="n6co-fl" d="M1455 566V622H1520L1538 640V706" stroke="#5ce06a" stroke-width="3" fill="none"/><path d="M1538 712l-6-10h12z" fill="#5ce06a"/>'
              '<path class="n6co-fl" d="M1490 680H1530" stroke="#5ce06a" stroke-width="3" fill="none"/>'
              '<path d="M1335 676H1300C1290 676 1285 690 1285 712" stroke="#ff6a4a" stroke-width="3" fill="none"/><path d="M1285 716l-6-10h12z" fill="#ff6a4a"/>'
              '<circle cx="1568" cy="655" r="17" fill="#22b84a" stroke="#9affb0" stroke-width="2"/><path d="M1560 655l6 6 11-12" stroke="#fff" stroke-width="3.5" fill="none"/>')
      + '</div>')

P5 = ('<div class="step"><div class="n6co-p" style="left:28px;top:819px;width:1620px;height:94px"></div>'
      '<div class="n6co-n" style="left:50px;top:836px;background:#ffd84a;box-shadow:0 0 14px #ffd84a">!</div>'
      '<div class="n6co-h" style="left:150px;top:848px;font-size:30px">NAT может усложнить связь, диагностику и работу приложений.</div></div>')

HTML = CSS + bg("bgk_globe") + P1 + P2 + P3 + P4 + P5
