# -*- coding: utf-8 -*-
"""pptx 8: базовые принципы и механизмы MPLS — IP- и MPLS-передача; вёрстка поверх чистого фона bgk_10."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 140

CSS = """<style>
.i08-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:24px;box-shadow:0 5px 0 rgba(21,80,168,.22)}
.i08-a{position:absolute;border-radius:28px}
.i08-h{position:absolute;font:900 32px/1 "Rubik",sans-serif;color:#13306e}
.i08-ul{position:absolute;margin:0;padding:0;list-style:none;font:500 22px/30px "Golos Text",sans-serif;color:#1d2a44}
.i08-ul li::before{content:"";display:inline-block;width:15px;height:15px;border-radius:50%;margin-right:16px;background:var(--d)}
.i08-t{position:absolute;font:500 20px/1.15 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i08-x{position:absolute;font:500 22px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i08-ar{position:absolute;height:3px;background:#24577a}
.i08-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #24577a;border-right:0}
.i08-pk{position:absolute;display:flex;height:50px;border:3px solid #1d3f8a;border-radius:5px;overflow:hidden;font:700 25px/44px "Golos Text",sans-serif}
.i08-pk b{background:#f2694a;color:#1d1d1d;padding:0 10px;font-weight:700}.i08-pk i{background:#fff;color:#1d3f8a;padding:0 14px;font-style:normal}
.i08-fly{animation:i08f 3s ease-in-out infinite}
@keyframes i08f{0%,100%{transform:translateX(0)}50%{transform:translateX(7px)}}
</style>"""


def ar(x, y, w):
    return '<div class="i08-ar" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x, y, w)


def ul(x, col, items):
    return '<ul class="i08-ul" style="left:%dpx;top:280px;--d:%s">%s</ul>' % (x, col, "".join("<li>%s</li>" % i for i in items))


def lab(x, txt):
    return '<div class="i08-t" style="left:%dpx;top:472px;width:150px">%s</div>' % (x, txt)


HTML = CSS + bg("bgk_10") + "".join([
    '<div class="step">',
    '<div class="i08-p" style="left:252px;top:150px;width:1190px;height:430px"></div>',
    '<div class="i08-a" style="left:274px;top:222px;width:552px;height:346px;background:#d6efe6"></div>',
    '<div class="i08-a" style="left:845px;top:222px;width:580px;height:346px;background:#fbdcd2"></div>',
    '<div class="ab" style="left:512px;top:186px;width:683px;height:36px;border:3px solid #1d3f8a;border-bottom:0;border-radius:4px 4px 0 0"></div>',
    img("i08a_rt.png", "left:755px;top:145px;width:160px"),
    '<div class="i08-t" style="left:690px;top:250px;width:290px;font:800 24px/1.15 Golos Text,sans-serif;color:#13306e">Маршрутизатор<br>с поддержкой MPLS</div>',
    '<div class="i08-h" style="left:410px;top:240px">IP-ПЕРЕДАЧА</div>',
    ul(312, "#1f9c8a", ["Дейтаграммный способ", "Поиск по IP-адресу назначения", "Таблица IP-маршрутизации"]),
    img("i08a_ip.png", "left:294px;top:405px;width:114px", "ab i08-fly"), lab(276, "IP-пакет<br>(без метки)"),
    ar(410, 438, 34), img("i08a_t1.png", "left:445px;top:378px;width:191px"), ar(640, 438, 36),
    img("i08a_ip.png", "left:682px;top:405px;width:114px"), lab(664, "IP-пакет<br>(без метки)"),
    '</div>',
    '<div class="step">',
    '<div class="i08-h" style="left:1040px;top:240px">MPLS-ПЕРЕДАЧА</div>',
    ul(998, "#e8554a", ["Механизм виртуальных каналов", "Поиск по метке MPLS", "Таблица MPLS-продвижения"]),
    '<div class="i08-pk i08-fly" style="left:863px;top:410px"><b>100</b><i>IP</i></div>', lab(858, "MPLS-пакет<br>(с меткой)"),
    ar(1005, 438, 34), img("i08a_t2.png", "left:1045px;top:378px;width:191px"), ar(1240, 438, 36),
    '<div class="i08-pk" style="left:1284px;top:410px"><b>200</b><i>IP</i></div>', lab(1276, "MPLS-пакет<br>(с меткой)"),
    '<div class="ab" style="left:902px;top:530px;width:474px;height:22px;border-left:3px solid #1d3f8a;border-right:3px solid #1d3f8a;'
    'background:linear-gradient(#1d3f8a,#1d3f8a) 0 10px/100% 3px no-repeat"></div>',
    '<div class="i08-t" style="left:1024px;top:528px;width:232px;background:#fbdcd2;font:800 21px/26px Golos Text,sans-serif;color:#13306e">'
    'Продвижение по LSP</div>',
    '</div>',
    '<div class="step">',
    '<div class="i08-p" style="left:228px;top:598px;width:1140px;height:224px"></div>',
    '<div class="i08-h" style="left:248px;top:614px;font-size:28px">КАК ФОРМИРУЮТСЯ ТАБЛИЦЫ</div>',
    '<div class="i08-a" style="left:246px;top:650px;width:1104px;height:72px;border-radius:12px;background:#dcefef"></div>',
    '<div class="i08-a" style="left:246px;top:738px;width:1104px;height:76px;border-radius:12px;background:#dff0e4"></div>',
    img("i08a_topo.png", "left:252px;top:648px;width:168px"), img("i08a_doc.png", "left:298px;top:738px;width:102px"),
    '<div class="i08-x" style="left:454px;top:658px">Протоколы маршрутизации определяют топологию сети<br>и формируют таблицу IP-маршрутизации.</div>',
    '<div class="i08-x" style="left:454px;top:746px">Информация о маршрутах и механизмы распределения меток<br>используются для построения таблиц MPLS-продвижения.</div>',
    img("i08a_t1.png", "left:1162px;top:620px;width:146px"), img("i08a_t2.png", "left:1162px;top:722px;width:146px"),
    '</div>',
    '<div class="step">',
    '<div class="i08-p" style="left:325px;top:836px;width:1003px;height:90px"></div>',
    img("i08a_bulb.png", "left:352px;top:838px;width:90px"),
    '<div class="i08-t" style="left:440px;top:848px;width:888px;font:800 27px/1.2 Golos Text,sans-serif;color:#13306e">'
    'Способ продвижения пакета выбирается в зависимости<br>от конфигурации MPLS и параметров трафика.</div>',
    '</div>',
])
