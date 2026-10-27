# -*- coding: utf-8 -*-
"""pptx 4: MPLS — услуги на двух уровнях (L3VPN / L2VPN); вёрстка поверх чистого фона bgk_24."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i04-p{position:absolute;background:#fdf8ea;border:3px solid #f3e6c4;border-radius:24px;box-shadow:0 6px 0 rgba(21,80,168,.22)}
.i04-hd{position:absolute;border-radius:22px;text-align:center;color:#fff}
.i04-hd b{display:block;font:900 62px/1 "Rubik",sans-serif;letter-spacing:.03em;margin-top:6px}
.i04-hd span{display:block;font:700 28px/1.2 "Golos Text",sans-serif;margin-top:4px}
.i04-t{position:absolute;font:500 24px/1.35 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i04-o{position:absolute;font:800 23px/1.1 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i04-ip{position:absolute;font:500 21px/1.1 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i04-cl{position:absolute;background:#eaf6fc;border:3px solid #a9d6ef;border-radius:80px}
.i04-ct{position:absolute;font:700 22px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i04-res{position:absolute;border-radius:18px;font:800 27px/56px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i04-pill{position:absolute;background:#fdf8ea;border-radius:22px;font:700 24px/42px "Golos Text",sans-serif;color:#13306e;text-align:center;box-shadow:0 3px 0 rgba(21,80,168,.25)}
.i04-dar{position:absolute;height:3px;background:#24577a}
.i04-dar::before,.i04-dar::after{content:"";position:absolute;top:-7px;border:8px solid transparent}
.i04-dar::before{left:-2px;border-right:12px solid #24577a;border-left:0}.i04-dar::after{right:-2px;border-left:12px solid #24577a;border-right:0}
.i04-eth{position:absolute;height:10px;border-top:3px solid #e8604f;border-bottom:3px solid #e8604f}
.i04-fly{animation:i04f 3s ease-in-out infinite}
@keyframes i04f{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
</style>"""


def bld(x, flip=False):
    return img("i04a_bld.png", "left:%dpx;top:383px;width:160px%s" % (x, ";transform:scaleX(-1)" if flip else ""))


HTML = CSS + bg("bgk_24") + "".join([
    '<div class="step">',
    '<div class="i04-pill" style="left:452px;top:164px;width:750px;height:42px">MPLS переносит трафик, а VPN определяет вид услуги</div>',
    '</div>',
    # ---- L3VPN
    '<div class="step">',
    '<div class="i04-p" style="left:58px;top:226px;width:782px;height:512px"></div>',
    '<div class="i04-hd" style="left:64px;top:232px;width:770px;height:104px;background:#2f8d86"><b>L3VPN</b><span>Сетевой уровень • IP-пакеты</span></div>',
    bld(70), img("i04a_rt.png", "left:236px;top:423px;width:78px"),
    '<div class="i04-cl" style="left:302px;top:368px;width:296px;height:150px"></div>',
    '<div class="i04-ct" style="left:330px;top:383px;width:240px">Сеть оператора<br>MPLS</div>',
    '<div class="i04-dar" style="left:322px;top:454px;width:76px"></div>',
    img("i04a_ip.png", "left:408px;top:438px;width:86px", "ab i04-fly"),
    '<div class="i04-dar" style="left:508px;top:454px;width:76px"></div>',
    img("i04a_rt.png", "left:590px;top:423px;width:78px"), bld(682, True),
    '<div class="i04-o" style="left:88px;top:496px;width:140px">Офис 1</div>',
    '<div class="i04-ip" style="left:66px;top:521px;width:190px">192.168.10.0/24</div>',
    '<div class="i04-o" style="left:668px;top:496px;width:140px">Офис 2</div>',
    '<div class="i04-ip" style="left:640px;top:521px;width:190px">192.168.20.0/24</div>',
    '<div class="i04-t" style="left:100px;top:552px;width:740px">Оператор маршрутизирует IP-пакеты<br>между подсетями офисов.<br>'
    'Сети клиентов разделены таблицами VRF.</div>',
    '<div class="i04-res" style="left:196px;top:666px;width:620px;height:56px;background:#dcefe7">Клиент получает связь между IP-сетями</div>',
    '</div>',
    # ---- L2VPN
    '<div class="step">',
    '<div class="i04-p" style="left:852px;top:226px;width:772px;height:512px"></div>',
    '<div class="i04-hd" style="left:858px;top:232px;width:760px;height:104px;background:#e8705e"><b>L2VPN</b><span>Канальный уровень • кадры Ethernet</span></div>',
    bld(868), img("i04a_sw.png", "left:962px;top:443px;width:42px"), img("i04a_rt.png", "left:1000px;top:423px;width:78px"),
    '<div class="i04-cl" style="left:1060px;top:362px;width:346px;height:162px"></div>',
    '<div class="i04-ct" style="left:1124px;top:388px;width:240px">Сеть оператора<br>MPLS</div>',
    '<div class="i04-eth" style="left:1082px;top:455px;width:116px"></div>',
    img("i04a_fr.png", "left:1203px;top:443px;width:80px", "ab i04-fly"),
    '<div class="i04-eth" style="left:1286px;top:455px;width:112px"></div>',
    img("i04a_sw.png", "left:1394px;top:443px;width:42px"), img("i04a_rt.png", "left:1430px;top:423px;width:78px"),
    bld(1490, True),
    '<div class="i04-ct" style="left:1070px;top:496px;width:330px;font-size:20px">Виртуальный Ethernet-канал</div>',
    '<div class="i04-o" style="left:866px;top:502px;width:140px">Офис 1</div>',
    '<div class="i04-o" style="left:1486px;top:502px;width:140px">Офис 2</div>',
    '<div class="i04-t" style="left:880px;top:558px;width:720px">Оператор переносит кадры Ethernet.<br>IP-адресацией и маршрутизацией<br>'
    'управляет сама компания.</div>',
    '<div class="i04-res" style="left:874px;top:666px;width:590px;height:56px;background:#fde1d9">Для клиента — словно длинный кабель</div>',
    '</div>',
    '<div class="step">',
    '<div class="i04-pill" style="left:428px;top:800px;width:818px;height:86px;font:700 23px/1.45 Golos Text,sans-serif;padding-top:10px;box-sizing:border-box">'
    'Уровень услуги определяется тем, что получает клиент:<br>IP-связность или Ethernet-соединение.</div>',
    '</div>',
])
