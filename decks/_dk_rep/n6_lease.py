# -*- coding: utf-8 -*-
"""Продление аренды DHCP: шкала 0% / T0=50% / T1=87,5% / 100%, unicast в T0, broadcast в T1, итоги."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 100

CSS = """<style>
.n6ls-pan{position:absolute;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.75);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35)}
.n6ls-mk{position:absolute;height:52px;border-radius:10px;background:rgba(6,14,36,.92);text-align:center;
  font:800 20px/1.05 Montserrat,sans-serif;color:#fff;white-space:nowrap;box-sizing:border-box;padding-top:6px}
.n6ls-w{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6ls-w .fl{fill:none;stroke-width:4;stroke-dasharray:14 9;animation:n6lsd 1s linear infinite}
@keyframes n6lsd{to{stroke-dashoffset:-46}}
.n6ls-t{position:absolute;font:400 18px/1.2 "Golos Text",sans-serif;color:#b9d2f5;text-align:center}
.n6ls-t b{display:block;font:800 19px/1.25 Montserrat,sans-serif;color:#fff}
.n6ls-hd{position:absolute;top:344px;height:68px;border-radius:14px 14px 0 0}
.n6ls-hd .n{position:absolute;left:20px;top:12px;width:46px;height:46px;border-radius:50%;font:800 28px/46px Montserrat,sans-serif;color:#0a1430;text-align:center}
.n6ls-hd h4{position:absolute;left:92px;top:20px;margin:0;font:800 26px/1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6ls-hd p{position:absolute;top:14px;margin:0;font:400 13px/1.4 "Golos Text",sans-serif;color:#d6e2ff}
.n6ls-msg{position:absolute;text-align:center;font:800 23px/1.1 Montserrat,sans-serif}
.n6ls-msg span{display:block;font:500 20px/1.25 "Golos Text",sans-serif}
.n6ls-res{position:absolute;border-radius:14px}
.n6ls-res h4{position:absolute;margin:0;font:800 24px/1.3 Montserrat,sans-serif;color:#fff}
.n6ls-res p{position:absolute;margin:0;font:400 17px/1.35 "Golos Text",sans-serif;color:#d6e2ea}
.n6ls-dot{animation:n6lsp 1.6s ease-in-out infinite}
@keyframes n6lsp{50%{opacity:.35}}
.n6ls-wave{animation:n6lsp 1.4s ease-in-out infinite}
</style>"""


def mark(x, w, txt, pct, c, cx):
    return ('<div class="n6ls-mk" style="left:%dpx;top:%dpx;width:%dpx;border:1.5px solid %s;box-shadow:0 0 14px %s;%s">%s%s</div>'
            '<svg class="n6ls-w" viewBox="0 0 1672 941"><path d="M%d %d V%d" style="stroke:%s;stroke-width:2"/>'
            '<circle class="n6ls-dot" cx="%d" cy="262" r="10" style="fill:%s;stroke:#fff;stroke-width:2.5"/>'
            '<path d="M%d 272 V298" style="stroke:%s;stroke-width:2"/></svg>') % (
        x, 164 if pct else 176, w, c, c, "height:66px" if pct else "line-height:38px;padding-top:6px",
        txt, '<br><span style="color:%s">%s</span>' % (c, pct) if pct else "",
        cx, 230 if pct else 228, 252, c, cx, c, cx, c)


TICKS = "".join('<path d="M%d 264 V272" style="stroke:rgba(150,190,255,.5);stroke-width:2"/>' % x for x in range(180, 1560, 50))
CHK = ('<svg width="%d" height="%d" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" style="fill:#4fdc6a"/>'
       '<path d="M11 20l6 6 12-12" style="fill:none;stroke:#062210;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round"/></svg>')
WARN = ('<svg width="84" height="74" viewBox="0 0 84 74"><path d="M42 5 80 69H4z" style="fill:none;stroke:#ff5a6a;stroke-width:6;stroke-linejoin:round"/>'
        '<path d="M42 27v20" style="stroke:#ff5a6a;stroke-width:7;stroke-linecap:round"/><circle cx="42" cy="57" r="4.2" style="fill:#ff5a6a"/></svg>')

HTML = CSS + bg("bgk_space") + "".join([
    '<div class="n6ls-pan" style="left:26px;top:16px;width:1622px;height:308px;border-color:rgba(92,190,255,.45);box-shadow:none"></div>'
    '<div style="position:absolute;left:62px;top:108px;font:400 29.5px/1.2 \'Golos Text\',sans-serif;color:#8fb2ff;white-space:nowrap">'
    'Клиент периодически запрашивает продление аренды, чтобы продолжать использовать IP-адрес</div>',
    '<div class="step"><svg class="n6ls-w" viewBox="0 0 1672 941"><defs><linearGradient id="n6lsg" gradientUnits="userSpaceOnUse" x1="142" y1="0" x2="1598" y2="0">'
    '<stop offset="0" stop-color="#5cd2ff"/><stop offset=".45" stop-color="#3a7bff"/><stop offset=".75" stop-color="#b77bff"/><stop offset="1" stop-color="#ff6a3d"/></linearGradient></defs>'
    '<path d="M142 262 H1580" style="stroke:url(#n6lsg);stroke-width:4;filter:drop-shadow(0 0 6px #3a7bff)"/>'
    '<polygon points="1598,262 1576,251 1576,273" style="fill:#ff6a3d"/>' + TICKS + '</svg>'
    + mark(48, 222, "Начало аренды", "0%", "#5cd2ff", 142)
    + mark(1406, 222, "Истечение аренды", "100%", "#ff6a3d", 1526)
    + '<div class="n6ls-t" style="left:536px;top:292px;width:600px;font-size:20px">T0 и T1 клиент вычисляет по сроку аренды</div></div>',
    '<div class="step">' + mark(680, 170, "T0 = 50%", "", "#ffc94a", 768) + '</div>',
    '<div class="step">' + mark(1214, 164, "T1 = 87,5%", "", "#b77bff", 1297) + '</div>',
    # блок 1
    '<div class="step"><div class="n6ls-pan" style="left:26px;top:344px;width:804px;height:400px;border-color:rgba(92,190,255,.5)"></div>'
    '<div class="n6ls-hd" style="left:27px;width:802px;background:linear-gradient(90deg,rgba(30,90,200,.75),rgba(16,40,110,.6))">'
    '<div class="n" style="background:#5cd2ff">1</div><h4>В T0 — одноадресный запрос</h4>'
    '<p style="left:542px">Клиент обращается к тому же<br>DHCP-серверу, у которого получил аренду</p></div>'
    + img("n6_lease_nb.png", "left:72px;top:448px;width:176px") + img("n6_lease_srv.png", "left:632px;top:422px;width:140px")
    + '<div class="n6ls-t" style="left:46px;top:588px;width:220px"><b>DHCP-клиент</b>Использует<br>текущий IP-адрес</div>'
    '<div class="n6ls-t" style="left:596px;top:588px;width:220px"><b>DHCP-сервер</b>Тот же сервер,<br>выдавший аренду</div>'
    '<div class="n6ls-msg" style="left:280px;top:438px;width:300px;color:#5cd2ff">DHCPREQUEST<span>(unicast, одноадресный)</span></div>'
    '<svg class="n6ls-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 6px #3aa0ff)"><path class="fl" d="M222 500 H596" style="stroke:#3aa0ff"/>'
    '<polygon points="616,500 594,489 594,511" style="fill:#3aa0ff"/></svg></div>',
    '<div class="step"><svg class="n6ls-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 6px #6ee07a)"><path class="fl" d="M626 546 H282" style="stroke:#6ee07a"/>'
    '<polygon points="262,546 284,535 284,557" style="fill:#6ee07a"/></svg>'
    '<div class="n6ls-msg" style="left:280px;top:560px;width:300px;color:#6ee07a">DHCPACK<span style="color:#8fe09a">(unicast, одноадресный)</span></div>'
    '<div class="n6ls-res" style="left:40px;top:662px;width:776px;height:74px;background:linear-gradient(90deg,rgba(20,90,40,.85),rgba(10,40,24,.85));border:1.5px solid #6ee07a;box-shadow:0 0 16px rgba(110,224,122,.4)">'
    '<div style="position:absolute;left:16px;top:10px">' + CHK % (54, 54) + '</div>'
    '<h4 style="left:88px;top:6px">Сервер подтверждает аренду</h4>'
    '<p style="left:88px;top:40px;font-size:17.5px;color:#fff">Таймеры запускаются заново, клиент продолжает использовать IP-адрес.</p></div></div>',
    # блок 2
    '<div class="step"><div class="n6ls-pan" style="left:846px;top:344px;width:802px;height:400px;border-color:rgba(183,123,255,.55);box-shadow:0 0 22px rgba(183,123,255,.3)"></div>'
    '<div class="n6ls-hd" style="left:847px;width:800px;background:linear-gradient(90deg,rgba(110,60,210,.75),rgba(50,24,120,.6))">'
    '<div class="n" style="background:#b77bff">2</div><h4 style="font-size:24px">В T1 — широковещательный запрос</h4>'
    '<p style="left:574px">Клиент ищет любой доступный<br>DHCP-сервер в сети</p></div>'
    + img("n6_lease_nb2.png", "left:885px;top:455px;width:203px")
    + '<svg class="n6ls-w" viewBox="0 0 1672 941"><g class="n6ls-wave" style="fill:none;stroke:#5cd2ff;stroke-width:2;opacity:.7">'
    '<path d="M1060 530 a30 40 0 0 1 0 60"/><path d="M1080 515 a46 58 0 0 1 0 92"/><path d="M1100 502 a62 74 0 0 1 0 120"/></g></svg>'
    '<div class="n6ls-t" style="left:880px;top:616px;width:200px"><b>DHCP-клиент</b>Использует<br>текущий IP-адрес</div>'
    '<div class="n6ls-msg" style="left:1040px;top:430px;width:380px;color:#c9a6ff">DHCPREQUEST<span style="color:#d8c4ff">(broadcast, широковещательный)</span></div></div>',
    '<div class="step"><svg class="n6ls-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 5px #b77bff)">'
    '<path class="fl" d="M1086 548 L1380 492" style="stroke:#b77bff;stroke-width:3"/><polygon points="1398,488 1376,482 1380,500" style="fill:#b77bff"/>'
    '<path class="fl" d="M1090 562 H1430" style="stroke:#b77bff;stroke-width:3"/><polygon points="1450,562 1428,552 1428,572" style="fill:#b77bff"/>'
    '<path class="fl" d="M1086 578 L1312 630" style="stroke:#b77bff;stroke-width:3"/><polygon points="1330,636 1312,622 1308,640" style="fill:#b77bff"/></svg>'
    + img("n6_lease_s1.png", "left:1412px;top:418px;width:76px") + img("n6_lease_s2.png", "left:1462px;top:518px;width:80px")
    + img("n6_lease_s3.png", "left:1338px;top:588px;width:94px")
    + '<div class="n6ls-t" style="left:1502px;top:434px;text-align:left;color:#fff">Любой<br>DHCP-сервер</div>'
    '<div class="n6ls-t" style="left:1552px;top:540px;text-align:left;color:#fff;font-size:16px">Любой<br>DHCP-сервер</div>'
    '<div class="n6ls-t" style="left:1450px;top:642px;text-align:left;color:#fff">Любой<br>DHCP-сервер</div></div>',
    # итоги
    '<div class="step"><div class="n6ls-res" style="left:26px;top:762px;width:822px;height:150px;background:linear-gradient(120deg,rgba(14,70,30,.85),rgba(6,26,14,.9));border:1.5px solid #6ee07a;box-shadow:0 0 22px rgba(110,224,122,.4)">'
    '<div style="position:absolute;left:28px;top:30px">' + CHK % (88, 88) + '</div>'
    '<h4 style="left:134px;top:26px;font-size:22px">Получен DHCPACK → аренда продлена</h4>'
    '<p style="left:134px;top:72px;width:500px">Таймеры запускаются заново, клиент продолжает использовать тот же IP-адрес.</p></div>'
    + img("n6_lease_ok.png", "left:686px;top:790px;width:140px") + '</div>',
    '<div class="step"><div class="n6ls-res" style="left:866px;top:762px;width:782px;height:150px;background:linear-gradient(120deg,rgba(80,14,24,.85),rgba(30,6,12,.9));border:1.5px solid #ff5a6a;box-shadow:0 0 22px rgba(255,90,106,.4)">'
    '<div style="position:absolute;left:22px;top:30px">' + WARN + '</div>'
    '<h4 style="left:124px;top:14px">Получен DHCPNAK или ответа нет<br>до конца аренды → DHCPDISCOVER</h4>'
    '<p style="left:126px;top:82px">При истечении аренды клиент прекращает<br>использовать этот IP-адрес.</p></div>'
    + img("n6_lease_x.png", "left:1478px;top:792px;width:154px") + '</div>',
])
