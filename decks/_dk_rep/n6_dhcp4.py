# -*- coding: utf-8 -*-
"""Четыре этапа работы DHCP: ленты DISCOVER/OFFER/REQUEST/ACK с полями, ветка DHCPNAK."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 30

CSS = """<style>
.n6d4-pan{position:absolute;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.75);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35)}
.n6d4-t{position:absolute;font:400 22px/1.3 "Golos Text",sans-serif;color:#b9d2f5}
.n6d4-h{position:absolute;font:800 34px/1 Montserrat,sans-serif;color:#fff}
.n6d4-band{position:absolute;left:390px;width:900px;height:58px;border-radius:29px 10px 10px 29px;box-shadow:0 0 22px var(--c)}
.n6d4-band .n{position:absolute;left:12px;top:6px;width:46px;height:46px;border-radius:50%;background:#141a2e;
  font:800 30px/46px Montserrat,sans-serif;color:var(--c);text-align:center}
.n6d4-band h4{position:absolute;left:92px;top:11px;margin:0;font:900 34px/1 Montserrat,sans-serif;color:#141414}
.n6d4-band p{position:absolute;margin:0;font:500 19px/1.2 "Golos Text",sans-serif;color:#141414}
.n6d4-cell{position:absolute;height:64px;background:rgba(6,14,36,.85);border:1.5px solid rgba(92,190,255,.4);border-radius:10px;
  font:400 15px/1.3 "Golos Text",sans-serif;color:#b9d2f5;white-space:nowrap}
.n6d4-cell b{display:block;font:500 15px/1.35 "JetBrains Mono",monospace;color:#fff}
.n6d4-cell .k{position:absolute;top:10px}
.n6d4-cell i{position:absolute;top:8px;width:1px;height:48px;background:rgba(92,190,255,.4)}
.n6d4-w{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6d4-w .fl{stroke-width:5;fill:none;stroke-dasharray:16 10;animation:n6d4d 1s linear infinite}
@keyframes n6d4d{to{stroke-dashoffset:-52}}
.n6d4-red{position:absolute;height:96px;background:linear-gradient(160deg,rgba(70,10,20,.8),rgba(20,4,10,.9));
  border:1.5px solid #ff5a6a;border-radius:14px;box-shadow:0 0 20px rgba(255,90,106,.45)}
.n6d4-red h4{position:absolute;margin:0;font:800 21px/1.1 Montserrat,sans-serif;color:#fff}
.n6d4-red p{position:absolute;margin:0;font:400 16px/1.25 "Golos Text",sans-serif;color:#d8b9c0}
.n6d4-nak{animation:n6d4p 1.6s ease-in-out infinite}
@keyframes n6d4p{50%{box-shadow:0 0 6px rgba(255,90,106,.2)}}
</style>"""


def cells(y, parts):
    """parts: [(x, w, html)] — ячейки строки параметров."""
    return "".join('<div class="n6d4-cell" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (x, y, w, h) for x, w, h in parts)


BC = lambda c: ('<svg width="56" height="44" viewBox="0 0 56 44" style="position:absolute;left:14px;top:10px">'
                '<circle cx="28" cy="22" r="6" style="fill:none;stroke:%s;stroke-width:4"/>'
                '<path d="M18 12a14 14 0 0 0 0 20M38 12a14 14 0 0 1 0 20M10 5a24 24 0 0 0 0 34M46 5a24 24 0 0 1 0 34" style="fill:none;stroke:%s;stroke-width:4;stroke-linecap:round"/></svg>') % (c, c)
DB = ('<svg width="40" height="46" viewBox="0 0 40 46" style="position:absolute;left:30px;top:9px"><ellipse cx="20" cy="8" rx="17" ry="6" style="fill:#ff8a3d"/>'
      '<path d="M3 14c0 8 34 8 34 0v8c0 8-34 8-34 0zM3 28c0 8 34 8 34 0v8c0 8-34 8-34 0z" style="fill:#ff8a3d"/></svg>')
CLK = lambda c: ('<svg width="42" height="42" viewBox="0 0 42 42" style="position:absolute;left:18px;top:11px"><circle cx="21" cy="21" r="17" style="fill:none;stroke:%s;stroke-width:3.5"/>'
                 '<path d="M21 11v10l7 5" style="fill:none;stroke:%s;stroke-width:3.5;stroke-linecap:round"/></svg>') % (c, c)
OK = ('<svg width="44" height="44" viewBox="0 0 44 44" style="position:absolute;left:22px;top:10px"><circle cx="22" cy="22" r="18" style="fill:none;stroke:#6ee07a;stroke-width:3.5"/>'
      '<path d="M13 22l6 6 12-12" style="fill:none;stroke:#6ee07a;stroke-width:4;stroke-linecap:round"/></svg>')
GEAR = ('<svg width="44" height="44" viewBox="0 0 24 24" style="position:absolute;left:16px;top:10px"><path style="fill:#3aa0ff" d="M19.4 13a7.6 7.6 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.4 7.4 0 0 0-1.7-1L15 3h-4l-.4 2.9a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.5L6.6 11a7.6 7.6 0 0 0 0 2l-2.1 1.6 2 3.5 2.5-1c.5.4 1.1.7 1.7 1L11 21h4l.4-2.9c.6-.3 1.2-.6 1.7-1l2.5 1 2-3.5zM13 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z"/></svg>')


def addr_row(y, c):
    return cells(y, [
        (452, 288, BC(c) + '<span class="k" style="left:94px">Широковещательный<br>запрос</span>'),
        (756, 534, '<span class="k" style="left:18px">IP-источник:<b>0.0.0.0</b></span><i style="left:142px"></i>'
                   '<span class="k" style="left:174px">IP-назначение:<b>255.255.255.255</b></span><i style="left:326px"></i>'
                   '<span class="k" style="left:352px">MAC клиента:<b>00:1A:2B:3C:4D:5E</b></span>'),
    ])


def band(n, y, c, name, txt, tx):
    return ('<div class="n6d4-band" style="top:%dpx;background:linear-gradient(90deg,%s 0 45%%,%s);--c:%s"><div class="n">%d</div>'
            '<h4>%s</h4><p style="left:%dpx;top:%dpx">%s</p></div>') % (
        y, c, c, c, n, name, tx, 18 if "<br>" not in txt else 6, txt)


def flow(y, c, right):
    if right:
        d = '<path class="fl" d="M352 %d H1320" style="stroke:%s"/><polygon points="1336,%d 1310,%d 1310,%d" style="fill:%s"/>' % (y, c, y, y - 16, y + 16, c)
    else:
        d = '<path class="fl" d="M1325 %d H368" style="stroke:%s"/><polygon points="348,%d 374,%d 374,%d" style="fill:%s"/>' % (y, c, y, y - 16, y + 16, c)
    return '<svg class="n6d4-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 6px %s)">%s</svg>' % (c, d)


HTML = CSS + bg("bgk_space") + "".join([
    '<div class="n6d4-pan" style="left:38px;top:18px;width:1596px;height:138px"></div>'
    '<div class="n6d4-t" style="left:74px;top:66px;font:700 31px/1.1 Montserrat,sans-serif;color:#7fb2ff">Автоматическое получение IPv4-адреса и параметров сети</div>'
    '<div style="position:absolute;left:1162px;top:52px;width:2px;height:78px;background:rgba(92,190,255,.4)"></div>'
    '<div class="n6d4-t" style="left:1190px;top:50px;font-size:19.5px">DHCP — протокол, который автоматически<br>назначает IP-адрес и параметры сети<br>устройствам в сети.</div>',
    '<div class="step"><div class="n6d4-pan" style="left:30px;top:172px;width:308px;height:576px"></div>'
    '<div class="n6d4-h" style="left:62px;top:204px">DHCP-клиент</div>'
    '<div class="n6d4-t" style="left:62px;top:254px">Устройство, которое<br>получает параметры<br>сети автоматически</div>'
    + img("n6_dhcp4_nb.png", "left:38px;top:368px;width:300px")
    + '<div class="n6d4-pan" style="left:1340px;top:172px;width:306px;height:576px"></div>'
    '<div class="n6d4-h" style="left:1376px;top:204px">DHCP-сервер</div>'
    '<div class="n6d4-t" style="left:1376px;top:254px">Сервер, который<br>выдаёт IP-адреса<br>и параметры сети<br>из пула</div>'
    + img("n6_dhcp4_srv.png", "left:1352px;top:385px;width:290px")
    + '<div style="position:absolute;left:350px;top:212px;width:978px;height:494px;border:1.5px solid rgba(92,190,255,.45);border-radius:12px"></div></div>',
    '<div class="step">' + flow(214, "#ffc94a", True) + band(1, 174, "#ffc94a", "DHCPDISCOVER", "Клиент ищет DHCP-сервер", 452)
    + addr_row(240, "#ffc94a") + '</div>',
    '<div class="step">' + flow(372, "#ff8a3d", False)
    + band(2, 332, "#ff8a3d", "DHCPOFFER", "Сервер предлагает свободный IPv4-адрес<br>из пула и параметры сети", 382)
    + cells(404, [(452, 552, DB + '<span class="k" style="left:104px">Пул адресов<br>на DHCP-сервере</span><i style="left:266px"></i>'
                   '<span class="k" style="left:290px">Например:<b style="color:#ffc94a;font-family:Golos Text,sans-serif">192.168.1.100 – 192.168.1.200</b></span>'),
                  (1020, 268, CLK("#ff8a3d") + '<span class="k" style="left:86px;font-size:17px">Срок аренды:<br><span style="color:#fff">например, 8 дней</span></span>')])
    + '</div>',
    '<div class="step">' + flow(538, "#b77bff", True)
    + band(3, 498, "#b77bff", "DHCPREQUEST", "Клиент выбирает предложение<br>и сообщает об этом серверам", 404)
    + addr_row(566, "#b77bff") + '</div>',
    '<div class="step">' + flow(692, "#6ee07a", False)
    + band(4, 654, "#6ee07a", "DHCPACK", "Сервер подтверждает выдачу адреса клиенту", 376)
    + cells(728, [(452, 302, OK + '<span class="k" style="left:86px;font-size:15.5px">Назначенный IPv4-адрес:<b style="color:#5cd2ff">192.168.1.101</b></span>'),
                  (770, 256, GEAR + '<span class="k" style="left:78px">Параметры сети:<br><span style="color:#fff">маска, шлюз, DNS и др.</span></span>'),
                  (1040, 248, CLK("#6ee07a") + '<span class="k" style="left:80px;font-size:17px">Срок аренды:<br><span style="color:#fff">например, 8 дней</span></span>')])
    + '</div>',
    '<div class="step"><svg class="n6d4-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 5px #ff5a6a)">'
    '<path class="fl" d="M256 856 H182 V772" style="stroke:#ff5a6a;stroke-width:3"/><polygon points="182,752 170,774 194,774" style="fill:#ff5a6a"/>'
    '<path class="fl" d="M1418 856 H1496 V712" style="stroke:#ff5a6a;stroke-width:3"/>'
    '<path d="M712 860 H756M1004 860 H1048" style="stroke:#ff5a6a;stroke-width:4"/>'
    '<polygon points="770,860 752,850 752,870" style="fill:#ff5a6a"/><polygon points="1062,860 1044,850 1044,870" style="fill:#ff5a6a"/></svg>'
    '<div class="n6d4-red" style="left:256px;top:812px;width:446px">'
    '<svg width="62" height="62" viewBox="0 0 62 62" style="position:absolute;left:26px;top:17px"><circle cx="31" cy="31" r="27" style="fill:none;stroke:#ff5a6a;stroke-width:5"/><path d="M31 16v20" style="stroke:#ff5a6a;stroke-width:6;stroke-linecap:round"/><circle cx="31" cy="45" r="3.6" style="fill:#ff5a6a"/></svg>'
    '<h4 style="left:114px;top:14px">Адрес недоступен</h4><p style="left:114px;top:44px">Выбранный адрес уже используется<br>или больше не доступен</p></div>'
    '<div class="n6d4-red n6d4-nak" style="left:776px;top:826px;width:218px;height:66px;background:rgba(90,10,20,.85)">'
    '<h4 style="left:0;width:218px;text-align:center;top:16px;font-size:34px;color:#ff5a6a">DHCPNAK</h4></div>'
    '<div class="n6d4-red" style="left:1072px;top:812px;width:344px">'
    '<svg width="58" height="58" viewBox="0 0 24 24" style="position:absolute;left:28px;top:19px"><path d="M20 12a8 8 0 0 1-14.3 4.9M4 12a8 8 0 0 1 14.3-4.9" style="fill:none;stroke:#ff5a6a;stroke-width:2.4;stroke-linecap:round"/><path d="M18.8 3.5v4h-4M5.2 20.5v-4h4" style="fill:none;stroke:#ff5a6a;stroke-width:2.4;stroke-linecap:round"/></svg>'
    '<h4 style="left:120px;top:12px">Клиент начинает<br>процесс заново</h4><p style="left:120px;top:66px;font-size:14.5px">Повторяет DHCPDISCOVER</p></div></div>',
])
