# -*- coding: utf-8 -*-
"""pptx 3: MPLS — как проходит пакет; вёрстка поверх чистого фона bgk_11."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 285

CSS = """<style>
.i03-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i03-h{position:absolute;font:900 36px/1 "Rubik",sans-serif;color:#13306e}
.i03-t{position:absolute;font:600 22px/1.25 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i03-n{position:absolute;font:900 28px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:200px}
.i03-ar{position:absolute;height:3px;background:#24577a}
.i03-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #24577a;border-right:0}
.i03-pk{position:absolute;display:flex;height:50px;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;font:700 25px/44px "Golos Text",sans-serif}
.i03-pk b{background:#f2694a;color:#1d1d1d;padding:0 10px;font-weight:700}.i03-pk i{background:#fff;color:#1d3f8a;padding:0 16px;font-style:normal}
.i03-mpls{position:absolute;background:#bfe9e4;border-radius:30px}
.i03-row{position:absolute;border-top:2px solid #1d3f8a}
.i03-ch{position:absolute;font:900 33px/1 "Rubik",sans-serif;color:#fff}
.i03-c{position:absolute;font:500 23px/1.3 "Golos Text",sans-serif;color:#fff}
.i03-c p{margin:0 0 12px}
.i03-sep{position:absolute;width:3px;background:rgba(255,255,255,.8)}
.i03-fly{animation:i03f 3s ease-in-out infinite}
@keyframes i03f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def ar(x, y, w):
    return '<div class="i03-ar" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x, y, w)


def rt(x, name, sub):
    return img("i03a_rt.png", "left:%dpx;top:430px;width:126px" % x) + \
        '<div class="i03-n" style="left:%dpx;top:530px">%s</div>' % (x - 37, name) + \
        '<div class="i03-t" style="left:%dpx;top:563px;width:240px">%s</div>' % (x - 57, sub)


def ip(x):
    return img("i03a_ip.png", "left:%dpx;top:442px;width:128px" % x) + \
        '<div class="i03-t" style="left:%dpx;top:512px;width:160px">IP-пакет<br>(без метки)</div>' % (x - 16)


def pk(x, lab):
    return '<div class="i03-pk i03-fly" style="left:%dpx;top:449px"><b>%s</b><i>IP</i></div>' % (x, lab)


def col(x, ic, h, lines):
    return img(ic, "left:%dpx;top:710px;width:136px" % x) + \
        '<div class="i03-ch" style="left:%dpx;top:720px">%s</div>' % (x + 158, h) + \
        '<div class="i03-c" style="left:%dpx;top:770px;width:420px;white-space:nowrap">%s</div>' % (x + 158, "".join("<p>%s</p>" % l for l in lines))


HTML = CSS + bg("bgk_11") + "".join([
    '<div class="step">',
    '<div class="i03-p" style="left:48px;top:296px;width:1576px;height:378px"></div>',
    '<div class="i03-h" style="left:74px;top:318px">КАК ПРОХОДИТ ПАКЕТ</div>',
    '<div class="i03-mpls" style="left:252px;top:368px;width:1168px;height:246px"></div>',
    '<div class="i03-row" style="left:352px;top:395px;width:962px;height:16px;border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a"></div>',
    '<div class="i03-t" style="left:742px;top:378px;width:190px;background:#bfe9e4;font:800 28px/34px Golos Text,sans-serif;color:#13306e">MPLS-сеть</div>',
    ip(80), ar(212, 474, 62),
    rt(286, "LER", "Добавляет метку"), rt(646, "LSR", "Меняет метку"),
    rt(954, "LSR", "Меняет метку"), rt(1266, "LER", "Удаляет метку"),
    ar(414, 474, 40), pk(464, "100"), ar(616, 474, 26),
    ar(778, 474, 22), pk(806, "200"), ar(934, 474, 18),
    ar(1086, 474, 24), pk(1116, "300"), ar(1242, 474, 22),
    ar(1396, 474, 64), ip(1470),
    '</div>',
    '<div class="step">',
    '<div class="i03-row" style="left:350px;top:640px;width:976px;height:14px;border-top:0;border-bottom:2px solid #1d3f8a;'
    'border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a;top:626px"></div>',
    '<div class="i03-t" style="left:620px;top:625px;width:430px;background:#fdf8ea;font:800 23px/30px Golos Text,sans-serif;color:#13306e">'
    'LSP — путь коммутации по меткам</div>',
    '</div>',
    '<div class="step">',
    col(82, "i03a_ic1.png", "ОСНОВА", ["Виртуальные каналы + TCP/IP", "Применение в магистральных<br>IP-сетях"]),
    '<div class="i03-sep" style="left:590px;top:712px;height:180px"></div>',
    '</div>',
    '<div class="step">',
    col(619, "i03a_ic2.png", "ПЕРЕСЫЛКА", ["Поиск по метке внутри<br>MPLS-сети", "Метки: статически или<br>через LDP / RSVP-TE"]),
    '<div class="i03-sep" style="left:1080px;top:712px;height:180px"></div>',
    '</div>',
    '<div class="step">',
    col(1115, "i03a_ic3.png", "ВОЗМОЖНОСТИ", ["Туннелирование трафика", "Поддержка QoS и управления<br>трафиком"]),
    '</div>',
])
