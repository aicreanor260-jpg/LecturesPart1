# -*- coding: utf-8 -*-
"""DHCP для IPv4: сервер раздаёт параметры ПК, ноутбуку, принтеру; динамическая vs статическая адресация."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i6_replib import bg, img

W, H, TOP = 1672, 941, 205

CSS = """<style>
.n6dh-pan{position:absolute;background:linear-gradient(160deg,rgba(16,40,90,.78),rgba(6,14,36,.9));
  border:1.5px solid rgba(92,190,255,.75);border-radius:16px;box-shadow:0 0 22px rgba(58,160,255,.35)}
.n6dh-lead{left:84px;top:220px;width:888px;height:74px;font:500 29px/74px "Golos Text",sans-serif;color:#fff;padding-left:106px;box-sizing:border-box}
.n6dh-lead svg{position:absolute;left:26px;top:15px}
.n6dh-tag{position:absolute;height:44px;border-radius:9px;font:600 18px/44px "Golos Text",sans-serif;color:#141a2e;
  padding-left:58px;white-space:nowrap;box-sizing:border-box;box-shadow:0 0 14px rgba(0,0,0,.35)}
.n6dh-tag svg{position:absolute;left:16px;top:9px}
.n6dh-lbl{position:absolute;height:40px;font:800 22px/40px Montserrat,sans-serif;color:#fff;text-align:center;
  background:rgba(6,14,36,.9);border:1.5px solid rgba(92,190,255,.75);border-radius:10px;box-shadow:0 0 14px rgba(58,160,255,.35)}
.n6dh-big{position:absolute;top:686px;height:204px;border-radius:18px;box-shadow:0 0 26px rgba(255,201,74,.35)}
.n6dh-big .ic{position:absolute;left:38px;top:32px;width:144px;height:144px;border-radius:20px}
.n6dh-big .sep{position:absolute;left:218px;top:30px;width:2px;height:146px;background:rgba(40,20,0,.35)}
.n6dh-big h4{position:absolute;left:256px;top:34px;margin:0;font:800 34px/1 Montserrat,sans-serif;color:#141414}
.n6dh-big p{position:absolute;left:256px;top:86px;margin:0;font:500 25px/1.3 "Golos Text",sans-serif;color:#2a1c10}
.n6dh-w{position:absolute;left:0;top:0;width:1672px;height:941px;pointer-events:none;overflow:visible}
.n6dh-w path{fill:none;stroke:#5cd2ff;stroke-width:4;filter:drop-shadow(0 0 6px #3aa0ff);stroke-dasharray:12 8;animation:n6dhd 1.1s linear infinite}
.n6dh-w polygon{fill:#5cd2ff;filter:drop-shadow(0 0 6px #3aa0ff)}
@keyframes n6dhd{to{stroke-dashoffset:-40}}
.n6dh-srv{animation:n6dhf 3.4s ease-in-out infinite}
@keyframes n6dhf{50%{transform:translateY(-6px)}}
.n6dh-ring{position:absolute;left:668px;top:540px;width:330px;height:66px;border:3px solid rgba(92,190,255,.8);border-radius:50%;
  box-shadow:0 0 18px #3aa0ff;animation:n6dhp 2.2s ease-in-out infinite}
@keyframes n6dhp{50%{opacity:.4}}
</style>"""

ICO = {
    "ip": '<svg width="28" height="26" viewBox="0 0 28 26"><rect x="2" y="2" width="24" height="16" rx="2" fill="none" stroke="#141a2e" stroke-width="2.6"/><path d="M10 24h8M14 18v6" stroke="#141a2e" stroke-width="2.6"/></svg>',
    "mask": '<svg width="28" height="26" viewBox="0 0 28 26"><circle cx="14" cy="5" r="3.5" fill="none" stroke="#141a2e" stroke-width="2.4"/><circle cx="5" cy="21" r="3.5" fill="none" stroke="#141a2e" stroke-width="2.4"/><circle cx="23" cy="21" r="3.5" fill="none" stroke="#141a2e" stroke-width="2.4"/><path d="M12 8 7 18M16 8l5 10M9 21h10" stroke="#141a2e" stroke-width="2.4"/></svg>',
    "dns": '<svg width="28" height="26" viewBox="0 0 28 26"><rect x="3" y="2" width="22" height="6" rx="1.5" fill="none" stroke="#141a2e" stroke-width="2.4"/><rect x="3" y="10" width="22" height="6" rx="1.5" fill="none" stroke="#141a2e" stroke-width="2.4"/><rect x="3" y="18" width="22" height="6" rx="1.5" fill="none" stroke="#141a2e" stroke-width="2.4"/></svg>',
    "gw": '<svg width="28" height="26" viewBox="0 0 28 26"><rect x="2" y="14" width="24" height="9" rx="2" fill="none" stroke="#141a2e" stroke-width="2.4"/><path d="M14 14V4M10 4h8" stroke="#141a2e" stroke-width="2.4"/><circle cx="8" cy="18.5" r="1.5" fill="#141a2e"/></svg>',
}
TAGS = [("ip", "IPv4-адрес", "#ffc94a"), ("mask", "Маска подсети", "#ff8a3d"),
        ("dns", "DNS-сервер", "#b77bff"), ("gw", "Шлюз по умолчанию", "#8fdcff")]


def tags(x):
    out = ""
    for i, (k, t, c) in enumerate(TAGS):
        w = 244 if k == "gw" else 222
        out += '<div class="n6dh-tag" style="left:%dpx;top:%dpx;width:%dpx;background:%s">%s%s</div>' % (
            x, 315 + i * 54, w, c, ICO[k], t)
    return '<div class="step">' + out + '</div>'


def arrow(d, tip):
    return '<path d="%s"/><polygon points="%s"/>' % (d, tip)


WIRES = ('<svg class="n6dh-w" viewBox="0 0 1672 941">'
         + arrow("M400 390 L360 390", "340,390 362,378 362,402")
         + arrow("M640 392 C700 392 690 440 740 440", "")
         + arrow("M930 440 C990 440 980 392 1030 392", "1048,392 1026,380 1026,404")
         + arrow("M1282 392 L1370 392", "1392,392 1370,380 1370,404")
         + arrow("M1340 565 C1060 565 1060 482 960 482", "938,482 960,470 960,494")
         + arrow("M1040 520 C1060 565 1100 565 1330 565", "1352,565 1330,553 1330,577")
         + '</svg>')

GEAR = ('<svg width="54" height="44" viewBox="0 0 24 24"><path fill="#5cd2ff" d="M19.4 13a7.6 7.6 0 0 0 0-2l2.1-1.6-2-3.5-2.5 1a7.4 7.4 0 0 0-1.7-1L15 3h-4l-.4 2.9a7.4 7.4 0 0 0-1.7 1l-2.5-1-2 3.5L6.6 11a7.6 7.6 0 0 0 0 2l-2.1 1.6 2 3.5 2.5-1c.5.4 1.1.7 1.7 1L11 21h4l.4-2.9c.6-.3 1.2-.6 1.7-1l2.5 1 2-3.5zM13 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z"/></svg>')
NET = ('<svg width="110" height="110" viewBox="0 0 24 24"><circle cx="12" cy="4.5" r="2.6" fill="none" stroke="#141414" stroke-width="1.8"/>'
       '<circle cx="5" cy="18.5" r="2.6" fill="none" stroke="#141414" stroke-width="1.8"/><circle cx="19" cy="18.5" r="2.6" fill="none" stroke="#141414" stroke-width="1.8"/>'
       '<path d="M10.7 6.8 6.3 16.2M13.3 6.8l4.4 9.4M7.6 18.5h8.8" stroke="#141414" stroke-width="1.8"/></svg>')
STACK = ('<svg width="96" height="96" viewBox="0 0 24 24"><rect x="3" y="2.5" width="18" height="5.5" rx="1.6" fill="#141414"/>'
         '<rect x="3" y="9.3" width="18" height="5.5" rx="1.6" fill="#141414"/><rect x="3" y="16" width="18" height="5.5" rx="1.6" fill="#141414"/>'
         '<circle cx="6.5" cy="5.25" r="1" fill="#ff8a6a"/><circle cx="6.5" cy="12" r="1" fill="#ff8a6a"/><circle cx="6.5" cy="18.8" r="1" fill="#ff8a6a"/></svg>')

HTML = CSS + bg("bgk_globe") + "".join([
    '<div class="step"><div class="n6dh-pan n6dh-lead">' + GEAR + 'Автоматически назначает узлу сетевые параметры.</div></div>',
    '<div class="step"><div class="n6dh-ring"></div><div class="n6dh-srv">' + img("n6_dhcp_srv.png", "left:728px;top:322px;width:210px") + '</div>'
    '<div class="n6dh-lbl" style="left:706px;top:606px;width:260px;height:46px;line-height:46px;font-size:27px">DHCP-сервер</div></div>',
    tags(408), tags(1053),
    '<div class="step">' + WIRES + '</div>',
    '<div class="step">' + img("n6_dhcp_pc.png", "left:82px;top:345px;width:256px")
    + '<div class="n6dh-lbl" style="left:120px;top:546px;width:160px">ПК</div>'
    + img("n6_dhcp_nb.png", "left:1392px;top:310px;width:222px")
    + '<div class="n6dh-lbl" style="left:1450px;top:453px;width:154px">Ноутбук</div>'
    + img("n6_dhcp_pr.png", "left:1360px;top:510px;width:218px")
    + '<div class="n6dh-lbl" style="left:1416px;top:635px;width:162px">Принтер</div></div>',
    '<div class="step"><div class="n6dh-big" style="left:36px;width:786px;background:linear-gradient(100deg,#ffd84a,#e8f56a 70%,#c8f07a)">'
    '<div class="ic" style="background:#ffc12e;display:flex;align-items:center;justify-content:center">' + NET + '</div><div class="sep"></div>'
    '<h4>Динамическая адресация</h4><p>Для больших сетей и&nbsp;меняющегося числа устройств. Меньше ручных ошибок и&nbsp;нагрузки на&nbsp;администратора.</p></div></div>',
    '<div class="step"><div class="n6dh-big" style="left:850px;width:786px;background:linear-gradient(100deg,#ff8a5a,#ffa070 60%,#ff9a8a);box-shadow:0 0 26px rgba(255,138,61,.4)">'
    '<div class="ic" style="background:#f26a4a;display:flex;align-items:center;justify-content:center">' + STACK + '</div><div class="sep"></div>'
    '<h4>Статическая адресация</h4><p>Параметры задают вручную.<br>Обычно — для серверов и&nbsp;принтеров.</p></div></div>',
])
