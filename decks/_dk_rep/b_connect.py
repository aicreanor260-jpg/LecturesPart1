# -*- coding: utf-8 -*-
"""Три способа подключения к коммутатору: консоль, SSH/Telnet, Web."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _dk_replib import bg, img

W, H, TOP = 1672, 941, 280

CSS = """<style>
.bcc-card{position:absolute;top:455px;width:530px;height:372px;background:rgba(255,255,255,.95);border:3px solid #2a0a2a;
  transform:skew(-2deg);box-shadow:9px 9px 0 rgba(255,46,147,.55)}
.bcc-rib{position:absolute;top:470px;background:#ff2e93;color:#fff;font:italic 900 42px/1 Rubik,sans-serif;text-transform:uppercase;
  padding:12px 30px 14px;transform:skew(-8deg);box-shadow:6px 6px 0 #2a0a2a;white-space:nowrap}
.bcc-ar{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none}
.bcc-ar path{fill:none;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.bcc-ar .d{stroke-dasharray:14 10;animation:bccd 1s linear infinite}
@keyframes bccd{to{stroke-dashoffset:-48}}
.bcc-foot{position:absolute;left:312px;top:842px;width:1050px;height:76px;background:#fff;border:3px solid #2a0a2a;border-radius:10px;
  box-shadow:6px 6px 0 rgba(255,46,147,.5);font:500 22px/1.35 "Golos Text",sans-serif;color:#1a0a1a;text-align:center;padding-top:9px;box-sizing:border-box}
.bcc-foot b{color:#ff2e93;font-weight:800}
.bcc-sw{animation:bccf 3.5s ease-in-out infinite}
@keyframes bccf{50%{transform:translateY(-5px)}}
</style>"""


def card(x, title, rx, pic):
    return ('<div class="step"><div class="bcc-card" style="left:%dpx"></div><div class="bcc-rib" style="left:%dpx">%s</div>%s</div>'
            % (x, rx, title, pic))


HTML = CSS + bg("bgk_roof") + "".join([
    '<div class="step">' + img("b_connect_sw.png", "left:430px;top:285px;width:820px", "ab bcc-sw") + '</div>',
    '<div class="step"><svg class="bcc-ar" viewBox="0 0 1672 941">'
    '<path class="d" d="M560 395 C460 380 380 400 352 445" stroke="#ff2e93"/><path d="M332 428 L350 458 L374 432" stroke="#ff2e93"/>'
    '<path class="d" d="M836 458 L836 395" stroke="#3fe6ff"/><path d="M814 410 L836 386 L858 410" stroke="#3fe6ff"/>'
    '<path class="d" d="M1190 390 C1260 395 1310 420 1325 452" stroke="#ff2e93"/><path d="M1304 440 L1328 464 L1344 433" stroke="#ff2e93"/>'
    '</svg></div>',
    card(32, "Консольный порт", 62, img("b_connect_l1.png", "left:65px;top:540px;width:510px")),
    card(605, "SSH / Telnet", 640, img("b_connect_l2.png", "left:630px;top:530px;width:410px")),
    card(1120, "Web-интерфейс", 1148, img("b_connect_l3.png", "left:1170px;top:530px;width:420px")),
    '<div class="step"><div class="bcc-foot"><b>Для консоли и SSH/Telnet:</b> PuTTY • HyperTerminal • Tera Term (Windows) • Minicom (Linux)<br>'
    '<b>Для Web-интерфейса</b> достаточно браузера</div></div>',
])
