# -*- coding: utf-8 -*-
"""Конфликт IP-адресов: проверка через ARP — два варианта, DHCPDECLINE, повторное получение."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 36

CSS = """<style>
.n6cf-pan{position:absolute;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.75);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35)}
.n6cf-lbl{position:absolute;height:42px;font:800 23px/42px Montserrat,sans-serif;color:#fff;text-align:center;
  background:rgba(10,22,50,.92);border:1.5px solid rgba(92,190,255,.55);border-radius:10px}
.n6cf-box{position:absolute;border-radius:14px}
.n6cf-box h4{position:absolute;margin:0;font:800 23px/1.15 Montserrat,sans-serif}
.n6cf-box p{position:absolute;margin:0;font:400 17px/1.3 "Golos Text",sans-serif;color:#c9d6ea}
.n6cf-box .m{font:600 21px/1.25 "Golos Text",sans-serif;color:#fff}
.n6cf-g{background:linear-gradient(160deg,rgba(14,60,30,.85),rgba(6,26,14,.9));border:1.5px solid #6ee07a;box-shadow:0 0 20px rgba(110,224,122,.4)}
.n6cf-r{background:linear-gradient(160deg,rgba(80,14,24,.85),rgba(30,6,12,.9));border:1.5px solid #ff5a6a;box-shadow:0 0 20px rgba(255,90,106,.45)}
.n6cf-v{background:linear-gradient(160deg,rgba(70,30,140,.85),rgba(30,12,70,.9));border:1.5px solid #b77bff;box-shadow:0 0 20px rgba(183,123,255,.5)}
.n6cf-w{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6cf-w .fl{fill:none;stroke-width:5;stroke-dasharray:16 9;animation:n6cfd 1s linear infinite}
@keyframes n6cfd{to{stroke-dashoffset:-50}}
.n6cf-ic{position:absolute;border-radius:50%}
.n6cf-pulse{animation:n6cfp 1.8s ease-in-out infinite}
@keyframes n6cfp{50%{box-shadow:0 0 6px rgba(92,190,255,.2)}}
</style>"""

CHK = lambda c, s: ('<svg width="%d" height="%d" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" style="fill:%s"/>'
                    '<path d="M11 20l6 6 12-12" style="fill:none;stroke:#0a1a0e;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round"/></svg>') % (s, s, c)
EXC = ('<svg width="54" height="54" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" style="fill:#ff5a6a"/>'
       '<path d="M20 9v14" style="stroke:#fff;stroke-width:5;stroke-linecap:round"/><circle cx="20" cy="30" r="3" style="fill:#fff"/></svg>')
DOC = ('<svg width="50" height="58" viewBox="0 0 50 58"><path d="M6 4h26l12 12v38H6z" style="fill:#ff6a6a"/>'
       '<path d="M15 28h20M15 36h20M15 44h20" style="stroke:#3a0a10;stroke-width:4;stroke-linecap:round"/></svg>')
CYC = ('<svg width="74" height="74" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" style="fill:#9b5cf0"/>'
       '<path d="M29 20a9 9 0 0 1-16 5.5M11 20a9 9 0 0 1 16-5.5" style="fill:none;stroke:#fff;stroke-width:3;stroke-linecap:round"/>'
       '<path d="M27.5 9.5v5h-5M12.5 30.5v-5h5" style="fill:none;stroke:#fff;stroke-width:3;stroke-linecap:round"/></svg>')
BULB = ('<svg width="76" height="76" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18.5" style="fill:none;stroke:#3aa0ff;stroke-width:1.8"/>'
        '<path d="M15 23c-2-2-3-4-3-6.5a8 8 0 0 1 16 0c0 2.5-1 4.5-3 6.5v3h-10zM16 29h8M17 32h6" style="fill:none;stroke:#3aa0ff;stroke-width:1.9;stroke-linejoin:round"/></svg>')
WARN = ('<svg width="84" height="74" viewBox="0 0 84 74"><path d="M42 4 80 70H4z" style="fill:#ff5a6a;stroke:#ff5a6a;stroke-width:4;stroke-linejoin:round"/>'
        '<path d="M42 26v22" style="stroke:#1a0508;stroke-width:7;stroke-linecap:round"/><circle cx="42" cy="58" r="4.2" style="fill:#1a0508"/></svg>')


def arr(d, pts, c, w=5):
    return '<path class="fl" d="%s" style="stroke:%s;stroke-width:%d"/><polygon points="%s" style="fill:%s"/>' % (d, c, w, pts, c)


HTML = CSS + bg("bgk_net") + "".join([
    '<div class="n6cf-pan" style="left:36px;top:40px;width:1600px;height:198px"></div>'
    '<div style="position:absolute;left:74px;top:166px;font:400 26px/1.22 \'Golos Text\',sans-serif;color:#8fb2df">После получения адреса по DHCP клиент проверяет,<br>не используется ли этот IP-адрес в сети, с помощью ARP.</div>'
    '<div class="n6cf-pan" style="left:1034px;top:46px;width:578px;height:164px;border-color:rgba(92,190,255,.45);box-shadow:none"></div>'
    '<div style="position:absolute;left:1052px;top:66px">' + BULB + '</div>'
    '<div style="position:absolute;left:1150px;top:64px;font:800 21px/1 Montserrat,sans-serif;color:#fff">Зачем нужна проверка?</div>'
    '<div style="position:absolute;left:1150px;top:96px;width:456px;font:400 15px/1.5 \'Golos Text\',sans-serif;color:#b9d2f5">'
    'DHCP-сервер может выдать адрес, который уже используется (например, из-за ошибки, статической настройки или устаревшей информации). Клиент проверяет его с помощью ARP, чтобы избежать конфликта.</div>',
    '<div class="step"><div class="n6cf-pan" style="left:46px;top:252px;width:286px;height:396px;border-color:rgba(92,190,255,.4)"></div>'
    '<div class="n6cf-lbl" style="left:56px;top:254px;width:270px">DHCP-клиент</div>'
    + img("n6_conflict_nb1.png", "left:92px;top:308px;width:246px")
    + '<div class="n6cf-pan" style="left:698px;top:252px;width:276px;height:130px;border-color:rgba(92,190,255,.4)"></div>'
    '<div class="n6cf-lbl" style="left:708px;top:252px;width:256px">DHCP-сервер</div>'
    + img("n6_conflict_srv.png", "left:772px;top:300px;width:126px")
    + '<div class="n6cf-pan" style="left:1338px;top:252px;width:296px;height:290px;border-color:rgba(92,190,255,.4)"></div>'
    '<div class="n6cf-lbl" style="left:1346px;top:254px;width:282px">Другое устройство</div>'
    + img("n6_conflict_nb2.png", "left:1332px;top:308px;width:250px") + '</div>',
    '<div class="step"><div class="n6cf-box n6cf-g" style="left:62px;top:490px;width:262px;height:140px;background:linear-gradient(180deg,#59e06a 0 64px,rgba(6,26,14,.92) 64px)">'
    '<div style="position:absolute;left:18px;top:12px">' + CHK("#0a2a12", 40).replace("#0a1a0e", "#6ee07a") + '</div>'
    '<h4 style="left:80px;top:10px;color:#0a1a0e;font-size:21px">DHCPACK —<br>адрес получен</h4>'
    '<p style="left:20px;top:76px;font-size:18px;color:#fff">Клиент получил IP-адрес<br>например, 192.168.1.101</p></div></div>',
    '<div class="step"><svg class="n6cf-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 6px #3aa0ff)">'
    + arr("M540 420 H368", "342,420 368,406 368,434", "#3aa0ff")
    + arr("M1134 420 H1306", "1332,420 1306,406 1306,434", "#3aa0ff")
    + arr("M540 420 C500 420 490 430 490 448", "490,468 478,448 502,448", "#3aa0ff", 4)
    + arr("M1134 420 C1170 420 1178 430 1178 448", "1178,468 1166,448 1190,448", "#3aa0ff", 4)
    + '</svg><div class="n6cf-pan n6cf-pulse" style="left:538px;top:380px;width:596px;height:70px;border-radius:12px;border-color:#3aa0ff">'
    '<div style="position:absolute;left:0;top:10px;width:596px;text-align:center;font:800 21px/1 Montserrat,sans-serif;color:#fff">ARP-запрос: используется ли адрес 192.168.1.101?</div>'
    '<div style="position:absolute;left:0;top:42px;width:596px;text-align:center;font:400 16.5px/1 \'Golos Text\',sans-serif;color:#b9d2f5">Широковещательный запрос (вся сеть)</div></div></div>',
    '<div class="step"><div class="n6cf-box n6cf-g" style="left:352px;top:478px;width:472px;height:170px">'
    '<div style="position:absolute;left:18px;top:16px">' + CHK("#6ee07a", 50) + '</div>'
    '<h4 style="left:84px;top:18px;color:#6ee07a">Вариант 1: конфликта нет</h4>'
    '<p class="m" style="left:84px;top:52px">Ответа нет → адрес свободен →<br>клиент использует адрес</p>'
    '<p style="left:20px;top:110px">Ни одно устройство не ответило на ARP-запрос.<br>В сети не обнаружен узел с IP 192.168.1.101.</p></div></div>',
    '<div class="step"><div class="n6cf-box n6cf-r" style="left:860px;top:478px;width:538px;height:160px">'
    '<div style="position:absolute;left:20px;top:14px">' + EXC + '</div>'
    '<h4 style="left:94px;top:18px;color:#ff6a7a">Вариант 2: есть конфликт</h4>'
    '<p class="m" style="left:94px;top:52px;font-size:22px">Другое устройство отвечает ARP →<br>адрес уже занят</p>'
    '<p style="left:94px;top:110px;font-size:16px">Устройство, которое уже использует IP 192.168.1.101,<br>отправляет ARP-ответ клиенту.</p></div>'
    '<svg class="n6cf-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 6px #ff5a6a)">'
    + arr("M1476 490 V666 H276", "252,666 278,652 278,680", "#ff5a6a")
    + '</svg><div class="n6cf-box n6cf-r" style="left:852px;top:642px;width:256px;height:62px;border-radius:10px">'
    '<div style="position:absolute;left:0;top:6px;width:256px;text-align:center;font:800 23px/1.05 Montserrat,sans-serif;color:#fff">ARP-ответ</div>'
    '<div style="position:absolute;left:0;top:33px;width:256px;text-align:center;font:400 18px/1.2 \'Golos Text\',sans-serif;color:#fff">(у меня этот адрес)</div></div></div>',
    '<div class="step"><svg class="n6cf-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 6px #ff5a6a)">'
    + arr("M204 636 V720 C204 750 220 756 250 756 H332", "356,756 330,742 330,770", "#ff5a6a")
    + '</svg><div class="n6cf-box n6cf-r" style="left:358px;top:710px;width:530px;height:106px">'
    '<div style="position:absolute;left:28px;top:22px">' + DOC + '</div>'
    '<h4 style="left:98px;top:14px;font-size:27px;color:#fff">DHCPDECLINE</h4>'
    '<p class="m" style="left:98px;top:48px;font-weight:400;font-size:20px">Клиент сообщает о конфликте;<br>сервер должен предложить другой адрес.</p></div></div>',
    '<div class="step"><svg class="n6cf-w" viewBox="0 0 1672 941">'
    '<path class="fl" d="M996 704 V756" style="stroke:#ff5a6a;stroke-width:4"/>'
    + arr("M888 756 H1112", "1138,756 1112,742 1112,770", "#b77bff")
    + '</svg><div class="n6cf-box n6cf-v" style="left:1148px;top:704px;width:408px;height:120px">'
    '<div style="position:absolute;left:24px;top:22px">' + CYC + '</div>'
    '<h4 style="left:122px;top:12px;color:#fff">Получение адреса<br>начинается заново</h4>'
    '<p style="left:122px;top:72px;font-size:16px;color:#e4dcff">Клиент снова запрашивает<br>новый IP-адрес у DHCP-сервера.</p></div></div>',
    '<div class="step"><div class="n6cf-pan" style="left:36px;top:828px;width:1600px;height:98px;border-color:rgba(92,190,255,.4);box-shadow:none">'
    '<div style="position:absolute;left:44px;top:12px">' + WARN + '</div>'
    '<div style="position:absolute;left:158px;top:20px;font:800 25px/1 Montserrat,sans-serif;color:#fff">Одинаковый IP у двух узлов может нарушить доставку данных обоим устройствам.</div>'
    '<div style="position:absolute;left:158px;top:56px;font:400 19.5px/1.2 \'Golos Text\',sans-serif;color:#b9d2f5;white-space:nowrap">При конфликте пакеты могут приходить не тому узлу, соединение будет нестабильным, возможны потери данных и перебои в работе сети.</div></div></div>',
])
