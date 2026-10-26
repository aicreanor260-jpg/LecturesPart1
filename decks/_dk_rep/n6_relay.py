# -*- coding: utf-8 -*-
"""2.6: DHCP Relay — DHCP-ретранслятор (вёрстка на чистом фоне)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 40

CSS = """<style>
.n6rl-p{position:absolute;box-sizing:border-box;border-radius:16px;border:1.5px solid rgba(92,190,255,.6);
  background:linear-gradient(160deg,rgba(16,40,90,.72),rgba(6,14,36,.88));box-shadow:0 0 22px rgba(58,160,255,.3)}
.n6rl-dash{position:absolute;box-sizing:border-box;border:1.5px dashed rgba(150,190,240,.35);border-radius:12px}
.n6rl-t{position:absolute;white-space:nowrap;font:800 27px/1.15 Montserrat,sans-serif;color:#fff}
.n6rl-s{position:absolute;white-space:nowrap;font:400 19px/1.3 "Golos Text",sans-serif;color:#b9d2f5}
.n6rl-l{position:absolute;white-space:nowrap;font:600 19px/1.25 "Golos Text",sans-serif;color:#fff;text-align:center}
.n6rl-tag{position:absolute;box-sizing:border-box;border-radius:12px;font:600 18px/1.2 "Golos Text",sans-serif;color:#fff;padding:10px 12px 10px 86px}
.n6rl-ad{position:absolute;box-sizing:border-box;border-radius:12px;font:700 18px/1.25 Montserrat,sans-serif;color:#10101a;padding:12px 10px 0 108px}
.n6rl-dot{position:absolute;width:14px;height:14px;margin:-7px;border-radius:50%;offset-rotate:0deg}
.n6rl-go1{background:#ffb03a;box-shadow:0 0 14px #ff8a3d;offset-path:path("M275 465H760");animation:n6rlm 2.4s linear infinite}
.n6rl-go2{background:#5cd2ff;box-shadow:0 0 14px #3aa0ff;offset-path:path("M980 453H1395");animation:n6rlm 2.4s linear infinite .8s}
.n6rl-go3{background:#6ee07a;box-shadow:0 0 14px #6ee07a;offset-path:path("M1395 486H985M1200 486V598Q1200 610 1188 610H262Q250 610 250 598V545");animation:n6rlm 4s linear infinite 1.6s}
@keyframes n6rlm{from{offset-distance:0%;opacity:1}90%{opacity:1}to{offset-distance:100%;opacity:0}}
</style>"""

SVG = """<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941">
<defs><filter id="n6rlg"><feGaussianBlur stdDeviation="3"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g filter="url(#n6rlg)" fill="none" stroke-width="4" stroke-linecap="round">
<path d="M275 465H352M342 455l12 10-12 10" stroke="#ff9a3d"/>
<path d="M575 453H762M750 441l14 12-14 12" stroke="#ff9a3d"/>
<path d="M980 453H1395M1381 441l14 12-14 12" stroke="#5cd2ff"/>
<path d="M1395 486H985M999 474l-14 12 14 12" stroke="#6ee07a"/>
<path d="M1200 586V598Q1200 610 1188 610H262Q250 610 250 598V545M238 558l12-14 12 14" stroke="#6ee07a"/>
</g></svg>"""

HTML = CSS + bg("bgk_net") + "".join([
    # шапка
    '<div class="step"><div class="n6rl-p" style="left:38px;top:42px;width:1596px;height:190px;background:linear-gradient(160deg,rgba(16,40,90,.55),rgba(6,14,36,.75))"></div>'
    '<div class="n6rl-s" style="left:78px;top:138px;font:500 27px/1.3 \'Golos Text\',sans-serif;color:#8fb4ff">'
    'Позволяет клиентам в разных подсетях получать IP-адреса<br>с централизованного DHCP-сервера.</div>'
    '<div class="n6rl-p" style="left:1005px;top:62px;width:614px;height:156px"></div>'
    + img("n6_relay_bulb.png", "left:1024px;top:82px;width:96px") +
    '<div class="n6rl-t" style="left:1143px;top:78px;font-size:21px">Почему нужен DHCP Relay?</div>'
    '<div class="n6rl-s" style="left:1143px;top:111px;font-size:16.5px">DHCP-запрос от клиента — это широковещательный<br>'
    '<b style="color:#fff">broadcast</b>, который не проходит через маршрутизатор.<br>Relay принимает запрос в локальной подсети<br>'
    'и пересылает его на DHCP-сервер как <b style="color:#fff">unicast</b>.</div></div>',
    # подсеть клиента
    '<div class="step"><div class="n6rl-p" style="left:38px;top:250px;width:646px;height:396px"></div>'
    '<div class="n6rl-dash" style="left:56px;top:264px;width:600px;height:370px"></div>'
    '<div class="n6rl-t" style="left:78px;top:272px;font-size:25px">Подсеть клиента / VLAN 10</div>'
    '<div class="n6rl-s" style="left:78px;top:308px;font-size:18px">Клиенты получают IP-адреса<br>через DHCP Relay</div>'
    + img("n6_relay_pc.png", "left:92px;top:412px;width:180px") + img("n6_relay_sw.png", "left:362px;top:432px;width:208px") +
    '<div class="n6rl-l" style="left:96px;top:570px">Клиент (ПК)</div>'
    '<div class="n6rl-l" style="left:400px;top:522px;font-weight:600">Коммутатор<br><span style="font-weight:400">(VLAN 10)</span></div>'
    '<div class="n6rl-tag" style="left:340px;top:343px;width:288px;height:80px;border:2px solid #ff8a3d;background:rgba(90,36,8,.82);'
    'box-shadow:0 0 18px rgba(255,138,61,.5);padding-left:88px;font-size:17px">DHCP-запрос:<br>broadcast — только<br>внутри подсети</div>'
    + img("n6_relay_bc.png", "left:354px;top:360px;width:58px") + '</div>',
    # relay
    '<div class="step"><div class="n6rl-p" style="left:718px;top:250px;width:322px;height:396px"></div>'
    '<div class="n6rl-t" style="left:718px;top:274px;width:322px;text-align:center;font-size:31px">DHCP Relay</div>'
    '<div class="n6rl-s" style="left:718px;top:316px;width:322px;text-align:center">Принимает broadcast<br>и пересылает запрос дальше</div>'
    + img("n6_relay_rt.png", "left:772px;top:382px;width:208px") +
    '<div class="n6rl-l" style="left:718px;top:550px;width:322px;font-weight:500">Маршрутизатор<br>или L3-коммутатор</div></div>',
    # подсеть сервера
    '<div class="step"><div class="n6rl-p" style="left:1075px;top:250px;width:560px;height:396px"></div>'
    '<div class="n6rl-dash" style="left:1102px;top:264px;width:516px;height:370px"></div>'
    '<div class="n6rl-t" style="right:78px;top:272px;font-size:25px;text-align:right">Подсеть DHCP-сервера</div>'
    '<div class="n6rl-s" style="right:78px;top:310px;font-size:18px;text-align:right">Централизованное управление<br>IP-адресами</div>'
    + img("n6_relay_srv.png", "left:1402px;top:382px;width:160px") +
    '<div class="n6rl-l" style="left:1380px;top:570px;width:228px">Централизованный<br>DHCP-сервер</div></div>',
    # потоки
    '<div class="step">' + SVG +
    '<div class="n6rl-tag" style="left:1071px;top:376px;width:230px;height:58px;border:2px solid #3aa0ff;background:rgba(10,40,96,.9);'
    'box-shadow:0 0 16px rgba(58,160,255,.55);padding:16px 0 0 72px">Запрос: unicast</div>'
    + img("n6_relay_ui.png", "left:1092px;top:388px;width:32px") +
    '<div class="n6rl-tag" style="left:1071px;top:500px;width:282px;height:84px;border:2px solid #6ee07a;background:rgba(10,56,30,.9);'
    'box-shadow:0 0 16px rgba(110,224,122,.5);padding:10px 0 0 72px;font-size:17px">Ответ DHCP<br>возвращается клиенту<br>через Relay</div>'
    + img("n6_relay_ai.png", "left:1090px;top:512px;width:36px") +
    '<div class="n6rl-dot n6rl-go1"></div><div class="n6rl-dot n6rl-go2"></div><div class="n6rl-dot n6rl-go3"></div></div>',
    # пул
    '<div class="step"><div class="n6rl-p" style="left:38px;top:668px;width:546px;height:228px"></div>'
    '<div class="n6rl-t" style="left:70px;top:694px;font-size:29px">Как сервер выбирает пул?</div>'
    + img("n6_relay_doc.png", "left:74px;top:748px;width:102px") +
    '<div class="n6rl-s" style="left:197px;top:756px;font-size:21px">Relay передаёт адрес исходной<br>подсети (<b style="color:#fff">giaddr</b>). '
    'Сервер выбирает<br>соответствующий пул IP-адресов.</div></div>',
    # преимущества
    '<div class="step"><div class="n6rl-p" style="left:608px;top:668px;width:1027px;height:242px"></div>'
    '<div class="n6rl-t" style="left:636px;top:676px;font-size:22px">Преимущества DHCP Relay</div>'
    '<div class="n6rl-p" style="left:635px;top:714px;width:313px;height:178px;border-color:rgba(255,201,74,.4);box-shadow:none"></div>'
    '<div class="n6rl-ad" style="left:635px;top:714px;width:313px;height:88px;background:#ffc94a">Один сервер<br>для нескольких<br>подсетей</div>'
    + img("n6_relay_i1.png", "left:652px;top:726px;width:72px") +
    '<div class="n6rl-s" style="left:659px;top:812px;font-size:17.5px">Клиенты в разных VLAN<br>получают IP-адреса<br>с одного DHCP-сервера.</div>'
    '<div class="n6rl-p" style="left:966px;top:714px;width:313px;height:178px;border-color:rgba(255,138,61,.4);box-shadow:none"></div>'
    '<div class="n6rl-ad" style="left:966px;top:714px;width:313px;height:88px;background:#ff8a4a;padding-top:20px">Адресация<br>централизована</div>'
    + img("n6_relay_i2.png", "left:992px;top:726px;width:56px") +
    '<div class="n6rl-s" style="left:991px;top:812px;font-size:17.5px">Единое управление<br>пулами, настройками<br>и политиками.</div>'
    '<div class="n6rl-p" style="left:1297px;top:714px;width:316px;height:178px;border-color:rgba(110,224,122,.4);box-shadow:none"></div>'
    '<div class="n6rl-ad" style="left:1297px;top:714px;width:316px;height:88px;background:#7ee86a;font-size:16.5px;white-space:nowrap">Relay настраивают<br>на маршрутизаторе<br>или L3-коммутаторе</div>'
    + img("n6_relay_i3.png", "left:1318px;top:726px;width:68px") +
    '<div class="n6rl-s" style="left:1321px;top:812px;font-size:17.5px">Указывают IP-адрес<br>DHCP-сервера и включают<br>функцию DHCP Relay.</div></div>',
])
