# -*- coding: utf-8 -*-
"""NAT: преимущества и ограничения (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 142

YEL, ORA, VIO, GRN, RED = "#ffc94a", "#ff8a3d", "#b77bff", "#6ee07a", "#ff5a6a"

CSS = """<style>
.n6pr-p{position:absolute;box-sizing:border-box;background:linear-gradient(160deg,rgba(16,40,90,.72),rgba(6,14,36,.88));
  border:1.5px solid rgba(92,190,255,.6);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.3)}
.n6pr-c{position:absolute;box-sizing:border-box;background:rgba(8,20,50,.72);border:1.5px solid rgba(92,190,255,.35);border-radius:12px}
.n6pr-n{position:absolute;width:44px;height:52px;border-radius:7px;color:#0a1430;font:800 30px/52px Montserrat,sans-serif;text-align:center}
.n6pr-h{position:absolute;font:800 19px/1.2 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6pr-t{position:absolute;font:400 15px/1.3 "Golos Text",sans-serif;color:#b9d2f5;white-space:nowrap}
.n6pr-s{position:absolute;font:400 13px/1.2 "Golos Text",sans-serif;color:#dbe8ff;white-space:nowrap;text-align:center}
.n6pr-m{position:absolute;font:500 12px/1.25 "Golos Text",sans-serif;color:#fff;white-space:nowrap}
.n6pr-big{position:absolute;font:800 40px/1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6pr-ic{position:absolute;width:58px;height:58px;border-radius:50%;box-sizing:border-box;border:3.5px solid;font:900 34px/50px Montserrat;text-align:center}
.n6pr-wire{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6pr-wire path{fill:none;stroke-width:2.2}
.n6pr-wire .d{stroke-dasharray:6 5;animation:n6prd 1s linear infinite}
@keyframes n6prd{to{stroke-dashoffset:-22}}
.n6pr-x{position:absolute;font:900 26px/1 sans-serif;color:#ff4a5a;text-shadow:0 0 8px #ff4a5a}
.n6pr-ip{position:absolute;box-sizing:border-box;width:172px;height:32px;border:1px solid rgba(92,190,255,.35);border-radius:5px;
  font:500 13px/30px "Golos Text",sans-serif;color:#fff;padding-left:66px}
.n6pr-ip i{position:absolute;left:12px;top:5px;width:38px;height:20px;border-radius:4px;
  background:repeating-linear-gradient(#0000 0 5px,rgba(0,0,0,.35) 5px 7px),var(--c)}
</style>"""

CYAN = "stroke:#5cd2ff"


def card(x, y, w, h, n, col, title, text, ty=0):
    return ('<div class="n6pr-c" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
            '<div class="n6pr-n" style="left:%dpx;top:%dpx;background:%s">%s</div>'
            '<div class="n6pr-h" style="left:%dpx;top:%dpx">%s</div>'
            '<div class="n6pr-t" style="left:%dpx;top:%dpx">%s</div>'
            % (x, y, w, h, x + 12, y + 18, col, n, x + 68, y + 18, title, x + 68, y + 86 + ty if "<br>" in title else y + 60 + ty, text))


def net(x, y, w, h, title):
    return ('<div class="n6pr-c" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:rgba(10,28,64,.7)"></div>'
            '<div class="n6pr-s" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (x, y, w, h, x, y + 8, w, title))


def svg(d):
    return '<svg class="n6pr-wire">%s</svg>' % d


ADV_HEAD = ('<div class="step"><div class="n6pr-p" style="left:22px;top:150px;width:813px;height:768px"></div>'
            '<div class="n6pr-ic" style="left:48px;top:162px;border-color:#6ee07a;color:#6ee07a">&#10003;</div>'
            '<div class="n6pr-big" style="left:128px;top:172px">ПРЕИМУЩЕСТВА</div></div>')

A1 = ('<div class="step">' + card(33, 230, 792, 174, 1, YEL, "Эффективное<br>использование IPv4",
                                  "Много устройств используют<br>ограниченный пул публичных<br>адресов", 0)
      + net(333, 254, 157, 132, "Частная сеть<br>(локальная сеть)") + img("n6_pros_dev.png", "left:345px;top:295px;width:103px")
      + img("n6_pros_rt.png", "left:500px;top:275px;width:102px") + '<div class="n6pr-s" style="left:520px;top:366px;width:60px;font:700 16px Golos Text">NAT</div>'
      + '<div class="n6pr-c" style="left:633px;top:240px;width:180px;height:86px"></div>'
        '<div class="n6pr-s" style="left:633px;top:247px;width:180px;font-weight:700">Пул публичных IP-адресов</div>'
      + img("n6_pros_db.png", "left:655px;top:268px;width:47px")
      + '<div class="n6pr-m" style="left:710px;top:270px">203.0.113.10<br>203.0.113.11<br>203.0.113.12<br>…</div>'
      + img("n6_pros_cl.png", "left:692px;top:325px;width:123px")
      + svg('<path d="M445 310H472L500 330M445 345H472L500 336" style="%s"/><path d="M598 342Q640 342 660 370H692" style="stroke:#ffc94a"/>' % CYAN)
      + '</div>')

A2 = ('<div class="step">' + card(33, 414, 792, 170, 2, ORA, "Гибкость подключения", "Можно использовать<br>разные публичные пулы", 8)
      + net(335, 434, 140, 130, "Частная сеть") + img("n6_pros_dev.png", "left:345px;top:465px;width:103px")
      + img("n6_pros_rt.png", "left:470px;top:462px;width:90px") + '<div class="n6pr-s" style="left:485px;top:548px;width:60px;font:700 16px Golos Text">NAT</div>'
      + '<div class="n6pr-c" style="left:633px;top:418px;width:180px;height:158px"></div>'
        '<div class="n6pr-s" style="left:633px;top:425px;width:180px;font-weight:700">Разные публичные пулы</div>'
        '<div class="n6pr-ip" style="left:637px;top:448px;--c:#ffc94a"><i></i>203.0.113.0/24</div>'
        '<div class="n6pr-ip" style="left:637px;top:485px;--c:#ff8a3d"><i></i>198.51.100.0/24</div>'
        '<div class="n6pr-ip" style="left:637px;top:522px;--c:#b77bff"><i></i>192.0.2.0/24</div>'
        '<div class="n6pr-m" style="left:703px;top:558px">…</div>'
      + svg('<path class="d" d="M538 500Q560 455 630 450" style="stroke:#ffc94a"/><path class="d" d="M548 510Q580 490 630 488" style="stroke:#ff8a3d"/>'
            '<path class="d" d="M548 520Q590 520 630 505" style="stroke:#b77bff"/>') + '</div>')

A3 = ('<div class="step">' + card(33, 594, 792, 158, 3, VIO, "Сохранение<br>внутренней адресации",
                                  "При смене провайдера частные<br>адреса устройств можно<br>оставить прежними", 0)
      + net(343, 614, 195, 126, "Частная сеть") + img("n6_pros_dev3.png", "left:358px;top:645px;width:175px")
      + '<div class="n6pr-s" style="left:340px;top:716px;width:200px;font-size:11px;word-spacing:10px">192.168.1.10 192.168.1.11 192.168.1.12</div>'
      + img("n6_pros_rt.png", "left:560px;top:640px;width:90px") + '<div class="n6pr-s" style="left:574px;top:705px;width:60px;font:700 16px Golos Text">NAT</div>'
      + img("n6_pros_pa.png", "left:686px;top:600px;width:129px") + img("n6_pros_pb.png", "left:686px;top:683px;width:129px")
      + svg('<path d="M372 690H500M538 675H565" style="%s"/><path class="d" d="M640 660Q660 632 686 632M640 685Q660 710 686 712" style="%s"/>'
            % (CYAN, CYAN)) + '</div>')

A4 = ('<div class="step">' + card(33, 762, 792, 148, 4, GRN, "Скрытие внутренних<br>адресов",
                                  "Внешняя сеть не видит<br>частные IP-адреса напрямую", 0)
      + net(337, 770, 196, 126, "Частная сеть") + img("n6_pros_dev3.png", "left:352px;top:800px;width:175px")
      + '<div class="n6pr-s" style="left:336px;top:872px;width:200px;font-size:11px;word-spacing:10px">192.168.1.10 192.168.1.11 192.168.1.12</div>'
      + img("n6_pros_rt.png", "left:550px;top:790px;width:90px") + '<div class="n6pr-s" style="left:563px;top:860px;width:60px;font:700 16px Golos Text">NAT</div>'
      + img("n6_pros_cl.png", "left:696px;top:795px;width:123px")
      + svg('<path d="M366 845H496M533 830H556" style="%s"/><path class="d" d="M636 832H700" style="stroke:#ff5a6a"/>'
            '<circle cx="670" cy="832" r="11" style="fill:#2a0a14;stroke:#ff5a6a;stroke-width:2.5"/>' % CYAN)
      + '<div class="n6pr-x" style="left:662px;top:821px;font-size:18px">&#10005;</div></div>')

LIM_HEAD = ('<div class="step"><div class="n6pr-p" style="left:848px;top:150px;width:802px;height:768px"></div>'
            '<div class="n6pr-ic" style="left:872px;top:162px;border-color:#ff5a6a;color:#ff5a6a">!</div>'
            '<div class="n6pr-big" style="left:952px;top:172px">ОГРАНИЧЕНИЯ</div></div>')

L1 = ('<div class="step">' + card(859, 228, 781, 196, 1, YEL, "Входящие подключения",
                                  "Для доступа извне часто нужна<br>настройка переадресации<br>портов", 0)
      + img("n6_pros_cl2.png", "left:1300px;top:232px;width:135px")
      + img("n6_pros_rt.png", "left:1240px;top:310px;width:96px") + '<div class="n6pr-s" style="left:1255px;top:383px;width:60px;font:700 16px Golos Text">NAT</div>'
      + img("n6_pros_svc.png", "left:1528px;top:312px;width:86px")
      + '<div class="n6pr-s" style="left:1500px;top:382px;width:140px">Сервис<br>(внутренняя сеть)</div>'
      + '<div style="position:absolute;left:1376px;top:362px;width:122px;height:42px;box-sizing:border-box;border:2px solid #ffc94a;border-radius:6px;'
        'background:rgba(30,24,0,.8);font:700 13px/1.15 \'Golos Text\';color:#ffc94a;text-align:center;padding-top:4px">Переадресация<br>портов</div>'
      + svg('<path d="M1232 300H1262L1274 330" style="stroke:#ff5a6a"/><path d="M1366 300V330H1336" style="%s"/>'
            '<path class="d" d="M1376 330H1525" style="stroke:#ff5a6a"/><path d="M1336 370H1376M1498 380L1528 368" style="stroke:#6ee07a"/>' % CYAN)
      + '<div class="n6pr-x" style="left:1421px;top:318px">&#10005;</div></div>')

L2 = ('<div class="step">' + card(859, 432, 781, 180, 2, ORA, "Нарушение сквозного<br>соединения",
                                  "Некоторым приложениям<br>и протоколам нужна<br>дополнительная настройка", 0)
      + img("n6_pros_cl2.png", "left:1330px;top:443px;width:125px")
      + img("n6_pros_lap.png", "left:1180px;top:485px;width:85px") + img("n6_pros_lapr.png", "left:1532px;top:485px;width:83px")
      + img("n6_pros_rt.png", "left:1272px;top:485px;width:70px") + img("n6_pros_rt.png", "left:1450px;top:485px;width:70px")
      + '<div class="n6pr-s" style="left:1276px;top:543px;width:60px;font:700 14px Golos Text">NAT</div>'
        '<div class="n6pr-s" style="left:1454px;top:543px;width:60px;font:700 14px Golos Text">NAT</div>'
        '<div class="n6pr-s" style="left:1180px;top:563px;width:80px">Клиент<br>(за NAT)</div>'
        '<div class="n6pr-s" style="left:1530px;top:563px;width:80px">Сервер<br>(за NAT)</div>'
        '<div class="n6pr-s" style="left:1300px;top:567px;width:200px;color:#6ee07a">Требуется<br>дополнительная настройка</div>'
      + svg('<path class="d" d="M1340 512H1450" style="stroke:#ff5a6a"/><path class="d" d="M1340 545Q1395 575 1450 545" style="stroke:#6ee07a"/>'
            '<path d="M1250 518H1274M1520 518H1540" style="%s"/>' % CYAN)
      + '<div class="n6pr-x" style="left:1384px;top:500px">&#10005;</div></div>')

L3 = ('<div class="step">' + card(859, 620, 781, 196, 3, VIO, "Диагностика и состояние",
                                  "Таблицу трансляций нужно<br>учитывать при поиске<br>сетевых проблем", 0)
      + '<div class="n6pr-c" style="left:1216px;top:628px;width:270px;height:96px;background:rgba(6,14,36,.9)"></div>'
        '<div class="n6pr-s" style="left:1230px;top:634px;font:700 13px Golos Text;text-align:left">Таблица трансляций (NAT)</div>'
        '<div class="n6pr-s" style="left:1230px;top:657px;font-size:11px;text-align:left;word-spacing:2px">Внутренний IP:порт&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Публичный IP:порт</div>'
        '<div class="n6pr-m" style="left:1230px;top:676px;font-size:11.5px">192.168.1.10:52344 &#8594; 203.0.113.10:40001<br>'
        '192.168.1.11:60123 &#8594; 203.0.113.10:40002<br>…&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;…</div>'
      + img("n6_pros_lap2.png", "left:1130px;top:715px;width:65px")
      + '<div class="n6pr-s" style="left:1095px;top:770px;width:130px">Внутренний клиент<br>192.168.1.10</div>'
      + img("n6_pros_rt.png", "left:1270px;top:715px;width:96px") + '<div class="n6pr-s" style="left:1288px;top:784px;width:60px;font:700 16px Golos Text">NAT</div>'
      + img("n6_pros_cl.png", "left:1490px;top:660px;width:123px") + img("n6_pros_q.png", "left:1532px;top:735px;width:48px")
      + '<div class="n6pr-s" style="left:1470px;top:772px;width:160px">При диагностике<br>нужно учитывать NAT</div>'
      + svg('<path d="M1185 745H1272M1360 758H1400" style="%s"/><path class="d" d="M1420 760Q1470 735 1528 748" style="stroke:#b77bff"/>' % CYAN)
      + '<div class="n6pr-x" style="left:1405px;top:748px;font-size:18px">&#10005;</div></div>')

FOOT = ('<div class="step"><div class="n6pr-c" style="left:860px;top:826px;width:780px;height:84px;border-color:rgba(110,224,122,.6);'
        'background:rgba(10,40,30,.75);box-shadow:0 0 18px rgba(110,224,122,.25)"></div>'
        + img("n6_pros_shield.png", "left:878px;top:838px;width:64px") + img("n6_pros_fw.png", "left:1495px;top:838px;width:135px")
        + '<div style="position:absolute;left:988px;top:842px;font:700 22px/1.3 \'Golos Text\',sans-serif;color:#fff;white-space:nowrap">'
          '<span style="color:#6ee07a;font-weight:800">NAT</span> повышает приватность, но сам по себе<br>не заменяет межсетевой экран.</div></div>')

HTML = CSS + bg("bgk_net") + ADV_HEAD + A1 + A2 + A3 + A4 + LIM_HEAD + L1 + L2 + L3 + FOOT
