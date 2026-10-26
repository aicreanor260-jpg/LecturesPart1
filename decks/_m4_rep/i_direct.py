# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _m4_replib import bg, img
W, H, TOP = 1672, 941, 120

CSS = """<style>
.m4x-dir-p{position:absolute;box-sizing:border-box;background:rgba(6,34,28,.86);border:1.5px solid #d9b45a;border-radius:16px;
  box-shadow:0 0 18px rgba(240,199,94,.35),inset 0 0 22px rgba(240,199,94,.12)}
.m4x-dir-g{background:linear-gradient(180deg,#fff0b0,#e0b04a 55%,#b98a2e);-webkit-background-clip:text;background-clip:text;color:transparent;
  font-family:"Playfair Display",serif;font-weight:800;position:absolute;white-space:nowrap}
.m4x-dir-t{position:absolute;font:400 22px/1.1 "Golos Text",sans-serif;color:#e8f3ea;white-space:nowrap}
.m4x-dir-m{position:absolute;font:400 18px/1 "Golos Text",sans-serif;color:#e8f3ea;white-space:nowrap}
.m4x-dir-ov{position:absolute;box-sizing:border-box;border:2.5px solid #e9c864;border-radius:50%;background:rgba(10,60,50,.55);
  box-shadow:0 0 14px #3fd6b0,inset 0 0 12px rgba(63,214,176,.55);text-align:center;font:400 21px/1 "Golos Text",sans-serif;color:#f2f6ef}
.m4x-dir-b{position:absolute;box-sizing:border-box;border:1.5px solid #53e07a;border-radius:6px;background:rgba(10,50,30,.85);
  font:400 19px/27px "Golos Text",sans-serif;color:#d6f5dc;padding-left:34px;box-shadow:0 0 8px rgba(83,224,122,.4)}
.m4x-dir-b i,.m4x-dir-s i{position:absolute;border-radius:50%;background:radial-gradient(circle at 40% 35%,#d8ffd0,#4be06a 55%,#1f9a3a);box-shadow:0 0 12px #5dff7a}
.m4x-dir-s{position:absolute;box-sizing:border-box;border:1.5px solid #d9b45a;border-radius:10px;background:rgba(8,44,34,.9);
  box-shadow:0 0 14px rgba(240,199,94,.3);text-align:center}
.m4x-dir-s .a{position:absolute;left:104px;top:14px;font:400 22px/1 "Golos Text",sans-serif;color:#f2f6ef}
.m4x-dir-s .u{position:absolute;left:106px;top:42px;font:600 22px/1 "Golos Text",sans-serif;color:#4be06a}
.m4x-dir-s .c{position:absolute;left:0;right:0;top:73px;font:400 20px/25px "Golos Text",sans-serif;color:#e8f3ea}
.m4x-dir-tb{position:absolute;box-sizing:border-box;border:1.5px solid #c9a24d;background:rgba(7,40,40,.8);font:400 21px/1.15 "Golos Text",sans-serif;color:#f0f5ee;
  display:flex;align-items:center;justify-content:center;text-align:center;white-space:nowrap}
.m4x-dir-sv path{fill:none;stroke:#f0c75e;stroke-width:2.5;filter:drop-shadow(0 0 5px #f0c75e)}
.m4x-dir-sv circle{fill:#fff4c0;filter:drop-shadow(0 0 6px #f0c75e)}
</style>"""


def T(x, y, s, cls="m4x-dir-t", extra=""):
    return '<div class="%s" style="left:%dpx;top:%dpx;%s">%s</div>' % (cls, x, y, extra, s)


def ov(cx, cy, rx, ry, s):
    return ('<div class="m4x-dir-ov" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;line-height:%dpx">%s</div>'
            % (cx - rx, cy - ry, 2 * rx, 2 * ry, 2 * ry, s))


def badge(x, y, w, s):
    return ('<div class="m4x-dir-b" style="left:%dpx;top:%dpx;width:%dpx;height:30px">'
            '<i style="left:6px;top:5px;width:18px;height:18px"></i>%s</div>' % (x, y, w, s))


def status(x, w, gi, net):
    return ('<div class="m4x-dir-s" style="left:%dpx;top:475px;width:%dpx;height:128px">'
            '<i style="left:49px;top:15px;width:30px;height:30px"></i>'
            '<div class="a">%s</div><div class="u">up/up</div><div class="c">Подключён к сети<br>%s</div></div>' % (x, w, gi, net))


rows = [("192.168.10.0/24", "Gi1/0/1", 312), ("192.168.20.0/24", "Gi1/0/2", 391), ("203.0.113.0/24", "Gi1/0/3", 470)]
cells = ""
for dest, gi, y in rows:
    cells += ('<div class="m4x-dir-tb" style="left:1018px;top:%dpx;width:231px;height:80px">Прямое подключение</div>'
              '<div class="m4x-dir-tb" style="left:1248px;top:%dpx;width:230px;height:80px">%s</div>'
              '<div class="m4x-dir-tb" style="left:1477px;top:%dpx;width:163px;height:80px">%s</div>') % (y, y, dest, y, gi)

SV = ('<svg class="m4x-dir-sv" style="position:absolute;left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941">'
      '<path d="M136 279 L335 326"/><path d="M136 413 L335 352"/><path d="M136 279 L335 345" opacity=".5"/>'
      '<path d="M442 343 L610 343"/><path d="M719 343 L890 343"/>'
      '<circle cx="136" cy="279" r="6"/><circle cx="136" cy="413" r="6"/><circle cx="332" cy="326" r="5"/><circle cx="332" cy="352" r="5"/>'
      '<circle cx="442" cy="343" r="5"/><circle cx="608" cy="343" r="5"/><circle cx="719" cy="343" r="5"/><circle cx="890" cy="343" r="6"/></svg>')

HTML = CSS + bg() + "".join([
    '<div class="step"><div class="m4x-dir-p" style="left:28px;top:148px;width:962px;height:469px"></div>'
    '<div class="m4x-dir-p" style="left:60px;top:145px;width:355px;height:50px;border-radius:10px"></div>'
    '<div class="m4x-dir-g" style="left:96px;top:152px;font-size:31px;letter-spacing:1px">ТОПОЛОГИЯ СЕТИ</div></div>',
    '<div class="step">' + SV
    + ov(245, 277, 98, 30, "192.168.10.0/24") + ov(245, 404, 98, 30, "192.168.20.0/24")
    + ov(532, 325, 90, 27, "203.0.113.0/24") + ov(805, 322, 90, 27, "192.168.30.0/24")
    + img("i_direct_pc1.png", "left:48px;top:228px") + img("i_direct_pc2.png", "left:48px;top:368px")
    + img("i_direct_pc3.png", "left:892px;top:298px")
    + img("i_direct_r1.png", "left:336px;top:296px") + img("i_direct_r2.png", "left:614px;top:296px")
    + T(68, 307, "ПК1", extra="font-size:24px") + T(68, 444, "ПК2", extra="font-size:24px") + T(911, 373, "ПК3", extra="font-size:24px")
    + T(373, 241, "Gi1/0/1", "m4x-dir-m") + badge(362, 265, 90, "up/up")
    + T(473, 360, "Gi1/0/3", "m4x-dir-m") + badge(443, 386, 94, "up/up")
    + T(550, 362, "Gi1/0/1", "m4x-dir-m") + T(350, 395, "Gi1/0/2", "m4x-dir-m")
    + T(720, 360, "Gi1/0/2", "m4x-dir-m") + '</div>',
    '<div class="step">' + status(110, 241, "Gi1/0/1", "192.168.10.0/24") + status(389, 249, "Gi1/0/2", "192.168.20.0/24")
    + status(671, 247, "Gi1/0/3", "203.0.113.0/24") + '</div>',
    '<div class="step"><div class="m4x-dir-p" style="left:1010px;top:148px;width:640px;height:472px"></div>'
    '<div class="m4x-dir-g" style="left:1060px;top:153px;font-size:35px;font-weight:700">Таблица маршрутизации R1</div>'
    '<div style="position:absolute;left:1018px;top:203px;width:622px;height:1px;background:#c9a24d"></div>'
    '<div class="m4x-dir-tb" style="left:1018px;top:222px;width:231px;height:91px;font-size:22px">Протокол</div>'
    '<div class="m4x-dir-tb" style="left:1248px;top:222px;width:230px;height:91px;font-size:22px">Назначение/маска</div>'
    '<div class="m4x-dir-tb" style="left:1477px;top:222px;width:163px;height:91px;font-size:22px">Исходящий<br>интерфейс</div>'
    + cells + '</div>',
    '<div class="step"><div class="m4x-dir-p" style="left:33px;top:650px;width:1605px;height:155px;border-radius:8px"></div>'
    + img("i_direct_doc.png", "left:60px;top:662px")
    + '<div style="position:absolute;left:211px;top:668px;font:400 22.5px/31.5px \'Golos Text\',sans-serif;color:#eef4e8;white-space:nowrap;letter-spacing:.3px">'
    'Маршруты с прямым подключением формируются активными интерфейсами маршрутизатора, на которых настроены<br>'
    'IP-адрес и маска подсети (длина префикса). Напрямую подключённая сеть добавляется в таблицу маршрутизации,<br>'
    'если интерфейс находится в состоянии up/up. Каждый интерфейс сохраняет сведения о том сегменте сети, к которому<br>'
    'он подключён.</div></div>',
    '<div class="step"><div class="m4x-dir-p" style="left:185px;top:825px;width:1300px;height:72px;border-radius:12px"></div>'
    + img("i_direct_bulb.png", "left:299px;top:814px")
    + '<div class="m4x-dir-g" style="left:415px;top:838px;font-size:33px;font-weight:700">Интерфейс up/up &#8594; сеть добавлена в таблицу маршрутизации</div></div>',
])
