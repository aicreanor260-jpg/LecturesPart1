# -*- coding: utf-8 -*-
"""Принцип работы DHCP: DISCOVER/OFFER/REQUEST/ACK между клиентом и сервером, пул адресов, домашняя/крупная сеть."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 175

CSS = """<style>
.n6dw-pan{position:absolute;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.75);border-radius:18px;box-shadow:0 0 22px rgba(58,160,255,.35)}
.n6dw-h{position:absolute;font:800 28px/1 Montserrat,sans-serif;color:#fff;text-align:center}
.n6dw-s{position:absolute;font:400 19px/1.25 "Golos Text",sans-serif;color:#b9d2f5;text-align:center}
.n6dw-msg{position:absolute;left:456px;width:430px;height:88px;border-radius:12px;box-shadow:0 0 22px var(--c)}
.n6dw-msg .ic{position:absolute;left:16px;top:16px;width:56px;height:56px;border:3px solid #141414;border-radius:50%;box-sizing:border-box}
.n6dw-msg .bar{position:absolute;left:88px;top:0;width:2px;height:88px;background:rgba(0,0,0,.18)}
.n6dw-msg h4{position:absolute;left:102px;top:14px;margin:0;font:800 27px/1 Montserrat,sans-serif;color:#141414}
.n6dw-msg p{position:absolute;left:102px;top:52px;margin:0;font:500 15px/1.1 "Golos Text",sans-serif;color:#262626;white-space:nowrap}
.n6dw-w{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.n6dw-w line{stroke-width:3.5;stroke-dasharray:14 8;animation:n6dwd 1s linear infinite}
@keyframes n6dwd{to{stroke-dashoffset:-44}}
.n6dw-ip{position:absolute;left:1384px;font:400 20px/36px "Golos Text",sans-serif;color:#fff}
.n6dw-row{position:absolute;left:1326px;width:278px;height:1px;background:rgba(92,190,255,.25)}
.n6dw-sel{position:absolute;left:1329px;top:328px;width:270px;height:38px;border:1.5px solid #6ee07a;border-radius:8px;
  background:rgba(60,160,70,.35);box-shadow:0 0 14px rgba(110,224,122,.6);animation:n6dwp 1.8s ease-in-out infinite}
@keyframes n6dwp{50%{box-shadow:0 0 4px rgba(110,224,122,.2)}}
.n6dw-bt{position:absolute;top:740px;height:156px;border-radius:16px;background:linear-gradient(160deg,rgba(16,40,90,.7),rgba(6,14,36,.88));
  border:1.5px solid rgba(92,190,255,.45);box-shadow:0 0 18px rgba(58,160,255,.25)}
.n6dw-bt .ic{position:absolute;left:26px;top:20px;width:114px;height:114px;border-radius:16px;display:flex;align-items:center;justify-content:center}
.n6dw-bt h4{position:absolute;left:166px;top:40px;margin:0;font:800 30px/1 Montserrat,sans-serif;color:#fff;white-space:nowrap}
.n6dw-bt p{position:absolute;left:166px;top:86px;margin:0;font:400 20px/1.3 "Golos Text",sans-serif;color:#b9d2f5}
</style>"""

ICO = {
    "bc": '<svg viewBox="0 0 50 50" width="50" height="50" style="position:absolute;left:0;top:0"><circle cx="25" cy="25" r="4" fill="#141414"/><path d="M17 17a11 11 0 0 0 0 16M33 17a11 11 0 0 1 0 16M12 12a18 18 0 0 0 0 26M38 12a18 18 0 0 1 0 26" fill="none" stroke="#141414" stroke-width="3"/></svg>',
    "l": '<svg viewBox="0 0 50 50" width="50" height="50" style="position:absolute;left:0;top:0"><path d="M36 25H15M23 16l-9 9 9 9" fill="none" stroke="#141414" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "r": '<svg viewBox="0 0 50 50" width="50" height="50" style="position:absolute;left:0;top:0"><path d="M14 25h21M27 16l9 9-9 9" fill="none" stroke="#141414" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
MSGS = [("DHCPDISCOVER", "Клиент ищет DHCP-сервер", "#ffc94a", "bc", 1, 200),
        ("DHCPOFFER", "Сервер предлагает свободный адрес", "#ff8a3d", "l", -1, 318),
        ("DHCPREQUEST", "Клиент запрашивает предложенный адрес", "#b77bff", "r", 1, 436),
        ("DHCPACK", "Сервер подтверждает назначение адреса", "#6ee07a", "l", -1, 554)]


def msg(name, text, c, ico, d, y):
    cy = y + 44
    if d > 0:
        ln = ('<line x1="340" y1="%d" x2="456" y2="%d" style="stroke:%s"/><line x1="886" y1="%d" x2="995" y2="%d" style="stroke:%s"/>'
              '<polyline points="984,%d 998,%d 984,%d" style="fill:none;stroke:%s;stroke-width:4"/>') % (cy, cy, c, cy, cy, c, cy - 10, cy, cy + 10, c)
    else:
        ln = ('<line x1="358" y1="%d" x2="456" y2="%d" style="stroke:%s"/><line x1="886" y1="%d" x2="1012" y2="%d" style="stroke:%s"/>'
              '<polyline points="368,%d 354,%d 368,%d" style="fill:none;stroke:%s;stroke-width:4"/>') % (cy, cy, c, cy, cy, c, cy - 10, cy, cy + 10, c)
    dots = '<circle cx="340" cy="%d" r="5" style="fill:#fff"/><circle cx="1012" cy="%d" r="5" style="fill:#fff"/>' % (cy, cy)
    return ('<div class="step"><svg class="n6dw-w" viewBox="0 0 1672 941" style="filter:drop-shadow(0 0 6px %s)">%s%s</svg>'
            '<div class="n6dw-msg" style="top:%dpx;background:%s;--c:%s"><div class="ic">%s</div><div class="bar"></div>'
            '<h4>%s</h4><p>%s</p></div></div>') % (c, ln, dots, y, c, c, ICO[ico], name, text)


DEV = ('<svg width="230" height="56" viewBox="0 0 230 56" style="position:absolute;left:104px;top:568px">'
       '<rect x="6" y="6" width="44" height="30" rx="3" fill="none" stroke="#8fb8e8" stroke-width="2.4"/><path d="M0 44h58" stroke="#8fb8e8" stroke-width="2.6"/>'
       '<rect x="88" y="2" width="30" height="50" rx="5" fill="none" stroke="#8fb8e8" stroke-width="2.4"/><path d="M99 46h8" stroke="#8fb8e8" stroke-width="2.4"/>'
       '<rect x="152" y="2" width="30" height="50" rx="3" fill="none" stroke="#8fb8e8" stroke-width="2.4"/><path d="M160 12h14M160 18h14" stroke="#8fb8e8" stroke-width="2"/></svg>')
SRVI = ('<svg width="74" height="64" viewBox="0 0 74 64" style="position:absolute;left:1108px;top:558px">'
        '<rect x="3" y="3" width="68" height="16" rx="4" fill="none" stroke="#5cd2ff" stroke-width="2.6"/>'
        '<rect x="3" y="24" width="68" height="16" rx="4" fill="none" stroke="#5cd2ff" stroke-width="2.6"/>'
        '<rect x="3" y="45" width="68" height="16" rx="4" fill="none" stroke="#5cd2ff" stroke-width="2.6"/>'
        '<path d="M12 11h18M12 32h18M12 53h18" stroke="#5cd2ff" stroke-width="2.6"/></svg>')
GEAR = ('<svg width="44" height="44" viewBox="0 0 24 24"><path fill="none" stroke="#141414" stroke-width="1.8" d="M19.4 13a7.6 7.6 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.4 7.4 0 0 0-1.7-1L15 3h-4l-.4 2.9a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.5L6.6 11a7.6 7.6 0 0 0 0 2l-2.1 1.6 2 3.5 2.5-1c.5.4 1.1.7 1.7 1L11 21h4l.4-2.9c.6-.3 1.2-.6 1.7-1l2.5 1 2-3.5z"/><circle cx="13" cy="12" r="3" fill="none" stroke="#141414" stroke-width="1.8"/></svg>')
HOME = ('<svg width="70" height="70" viewBox="0 0 24 24"><path d="M3 11 12 3l9 8M5 9.5V21h5v-6h4v6h5V9.5" fill="none" stroke="#141414" stroke-width="1.9" stroke-linejoin="round"/></svg>')
STK = ('<svg width="64" height="64" viewBox="0 0 24 24"><rect x="3" y="2.5" width="18" height="5.5" rx="1.6" fill="none" stroke="#141414" stroke-width="1.8"/>'
       '<rect x="3" y="9.3" width="18" height="5.5" rx="1.6" fill="none" stroke="#141414" stroke-width="1.8"/><rect x="3" y="16" width="18" height="5.5" rx="1.6" fill="none" stroke="#141414" stroke-width="1.8"/>'
       '<path d="M6 5.2h4M6 12h4M6 18.8h4" stroke="#141414" stroke-width="1.8"/></svg>')

IPS = ["192.168.1.100", "192.168.1.101", "192.168.1.102", "192.168.1.103", "...", "192.168.1.200"]
pool = "".join('<div class="n6dw-ip" style="top:%dpx;%s">%s</div>' % (
    290 + i * 37, "color:#6ee07a;font-weight:600" if i == 1 else "", t) for i, t in enumerate(IPS))
rows = "".join('<div class="n6dw-row" style="top:%dpx"></div>' % (290 + i * 37) for i in range(1, 6))

HTML = CSS + bg("bgk_space") + "".join([
    '<div class="n6dw-pan" style="left:42px;top:182px;width:1588px;height:536px;border-color:rgba(92,190,255,.35);box-shadow:none"></div>',
    '<div class="step"><div class="n6dw-pan" style="left:64px;top:184px;width:274px;height:512px"></div>'
    + img("n6_dhcp_work_pc.png", "left:98px;top:248px;width:214px")
    + '<div class="n6dw-h" style="left:64px;top:506px;width:274px">DHCP-клиент</div>' + DEV
    + '<div class="n6dw-s" style="left:64px;top:636px;width:274px">Любое устройство<br>в сети</div></div>',
    '<div class="step"><div class="n6dw-pan" style="left:1012px;top:184px;width:268px;height:512px"></div>'
    + img("n6_dhcp_work_srv.png", "left:1038px;top:212px;width:224px")
    + '<div class="n6dw-h" style="left:1012px;top:508px;width:268px">DHCP-сервер</div>' + SRVI
    + '<div class="n6dw-s" style="left:1012px;top:636px;width:268px">Маршрутизатор<br>или отдельный сервер</div></div>',
] + [msg(*m) for m in MSGS] + [
    '<div class="step"><div class="n6dw-pan" style="left:1300px;top:190px;width:328px;height:500px"></div>'
    '<div class="n6dw-h" style="left:1326px;top:206px;text-align:left;font-size:24px">Пул адресов</div>'
    '<div class="n6dw-s" style="left:1328px;top:246px;text-align:left;font-size:19.5px">192.168.1.100 – 192.168.1.200</div>'
    '<div style="position:absolute;left:1324px;top:286px;width:280px;height:226px;border:1px solid rgba(92,190,255,.3);border-radius:8px;background:rgba(6,14,36,.5)"></div>'
    + rows + '<div class="n6dw-sel"></div><div style="position:absolute;left:1344px;top:340px;width:14px;height:14px;border-radius:50%;background:#6ee07a;box-shadow:0 0 8px #6ee07a"></div>' + pool
    + '<div style="position:absolute;left:1326px;top:541px;width:278px;height:2px;background:linear-gradient(90deg,#ffc94a 0 22%,rgba(92,190,255,.4) 22%)"></div>'
    '<div style="position:absolute;left:1326px;top:564px;width:66px;height:66px;border-radius:12px;background:#ffc94a;display:flex;align-items:center;justify-content:center">' + GEAR + '</div>'
    '<div class="n6dw-s" style="left:1420px;top:566px;text-align:left;font-size:18.5px;color:#e4eeff">Сервер выбирает<br><span style="color:#ffc94a;font-weight:700">свободный адрес</span><br>из выделенного<br>диапазона</div></div>',
    '<div class="step"><div class="n6dw-bt" style="left:52px;width:806px"><div class="ic" style="background:#ffc94a">' + HOME + '</div>'
    '<h4>Домашняя сеть</h4><p>DHCP обычно выполняет маршрутизатор</p></div>'
    + img("n6_dhcp_work_rt.png", "left:640px;top:762px;width:200px") + '</div>',
    '<div class="step"><div class="n6dw-bt" style="left:876px;width:750px"><div class="ic" style="background:#b77bff">' + STK + '</div>'
    '<h4 style="font-size:27px">Средняя/крупная сеть</h4><p>Часто используется<br>отдельный сервер</p></div>'
    + img("n6_dhcp_work_rack.png", "left:1398px;top:758px;width:226px") + '</div>',
])
