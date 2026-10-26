# -*- coding: utf-8 -*-
"""Подключение через Web-интерфейс: 4 шага, адрес, SVI VLAN 1 — вёрстка на фоне «худи»."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 255

CSS = """<style>
.bwl-b{position:absolute;background:rgba(255,255,255,.96);border:3px solid #2a0a2a;box-shadow:6px 6px 0 rgba(255,46,147,.5);
  font:500 20px/1.3 "Golos Text",sans-serif;color:#1a0a1a;white-space:nowrap}
.bwl-b b{color:#ff2e93;font:800 31px/1.15 "Golos Text",sans-serif;display:block}
.bwl-n{position:absolute;width:56px;height:56px;border-radius:50%;background:#ff2e93;color:#fff;border:3px solid #fff;
  font:900 34px/50px Rubik,sans-serif;text-align:center;box-shadow:3px 3px 0 #2a0a2a}
.bwl-tag{position:absolute;background:#3fe6ff;border:3px solid #2a0a2a;font:900 30px/1 Rubik,sans-serif;color:#1a0a2a;padding:8px 26px 8px 18px;
  clip-path:polygon(6% 0,100% 0,90% 100%,0 100%)}
.bwl-svg{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.bwl-svg .c{fill:none;stroke:#2aa8e8;stroke-width:12;stroke-linecap:round}
.bwl-svg .l{fill:none;stroke:#2a0a2a;stroke-width:3}
.bwl-svg .a{fill:none;stroke:#ff2e93;stroke-width:9;stroke-dasharray:14 10;animation:bwld 1s linear infinite}
@keyframes bwld{to{stroke-dashoffset:-48}}
.bwl-chev{position:absolute;font:900 64px/1 Rubik,sans-serif;color:#3fe6ff;letter-spacing:-6px;animation:bwlm 1.2s ease-in-out infinite}
@keyframes bwlm{50%{transform:translateX(12px)}}
.bwl-info{position:absolute;left:1118px;top:776px;width:528px;height:130px;background:rgba(255,255,255,.96);border:3px solid #3fc8ee;box-shadow:5px 5px 0 rgba(63,200,238,.4)}
.bwl-info ul{margin:0;padding:16px 0 0 30px;list-style:none;font:500 17.5px/1.6 "Golos Text",sans-serif;white-space:nowrap}
.bwl-info li:before{content:"●";color:#2a7ea8;margin-right:12px}
</style>"""

HTML = CSS + bg("bgk_hood") + "".join([
    '<div class="step">' + img("b_web_login_br.png", "left:480px;top:390px;width:495px") +
    img("b_web_login_sw.png", "left:1170px;top:495px;width:485px") +
    '<svg class="bwl-svg" viewBox="0 0 1672 941"><path class="c" d="M975 705 C1080 700 1230 700 1275 650"/>'
    '<path class="l" d="M1420 412 V515"/><path class="l" d="M1525 485 V520"/></svg>'
    '<div class="bwl-tag" style="left:990px;top:532px">HTTP</div><div class="bwl-chev" style="left:980px;top:582px">›››</div></div>',
    '<div class="step"><div class="bwl-b" style="left:498px;top:295px;width:330px;height:76px;padding:10px 0 0 60px;box-sizing:border-box">Откройте браузер<br>и перейдите по адресу</div>'
    '<div class="bwl-n" style="left:478px;top:276px">1</div></div>',
    '<div class="step"><div class="bwl-b" style="left:915px;top:272px;width:372px;height:92px;padding:12px 0 0 104px;box-sizing:border-box">Адрес коммутатора:<b>192.168.1.239</b></div>'
    + img("b_web_login_globe.png", "left:922px;top:278px;width:80px") +
    '<svg class="bwl-svg" viewBox="0 0 1672 941"><path class="a" d="M890 430 C960 480 960 540 880 590"/></svg></div>',
    '<div class="step"><div class="bwl-b" style="left:1340px;top:318px;width:306px;height:92px;padding:8px 0 0 18px;box-sizing:border-box">Управляющий интерфейс:<b>SVI VLAN 1</b></div>'
    '<div class="bwl-tag" style="left:1472px;top:444px;font-size:24px;clip-path:none;padding:6px 12px">VLAN 1</div></div>',
    '<div class="step"><div class="bwl-b" style="left:600px;top:672px;width:372px;height:84px;padding:8px 0 0 58px;box-sizing:border-box">Для первого подключения:<b>admin / admin</b></div>'
    '<div class="bwl-n" style="left:582px;top:652px">2</div></div>',
    '<div class="step"><div class="bwl-b" style="left:86px;top:792px;width:430px;height:110px;padding:24px 0 0 150px;box-sizing:border-box">После входа откройте<br>конфигурацию устройства</div>'
    + img("b_web_login_gear.png", "left:118px;top:798px;width:100px") +
    '<div class="bwl-n" style="left:56px;top:792px">3</div><div class="bwl-chev" style="left:530px;top:818px;color:#ff2e93">››</div></div>',
    '<div class="step"><div class="bwl-b" style="left:624px;top:792px;width:458px;height:110px;padding:10px 0 0 150px;box-sizing:border-box">При первом входе создайте<br>пользователя с <span style="color:#ff2e93;font-weight:800">безопасным<br>паролем</span></div>'
    + img("b_web_login_lock.png", "left:672px;top:798px;width:80px") +
    '<div class="bwl-n" style="left:602px;top:792px">4</div></div>',
    '<div class="step"><div class="bwl-info"><ul><li>Рекомендуется подключить компьютер к порту 1</li>'
    '<li>На старте все порты находятся в VLAN 1</li><li>Внешний вид Web-интерфейса зависит от модели</li></ul></div>'
    + img("b_web_login_i.png", "left:1102px;top:755px;width:60px") + '</div>',
])
