# -*- coding: utf-8 -*-
"""pptx 11: архитектура LSR — два способа продвижения данных; вёрстка поверх чистого фона bgk_16."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i11-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.22)}
.i11-h{position:absolute;font:900 32px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i11-a{position:absolute;border-radius:24px}
.i11-ul{position:absolute;margin:0;padding:0;list-style:none;font:500 23px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i11-ul li{padding-left:28px;text-indent:-28px;margin-bottom:8px}
.i11-ul li::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;background:#13306e;margin:0 18px 3px 0}
.i11-t{position:absolute;font:500 21px/1.15 "Golos Text",sans-serif;color:#1d2a44;text-align:center}
.i11-n{position:absolute;font:900 23px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:240px}
.i11-x{position:absolute;font:500 23px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i11-ar{position:absolute;height:3px;background:#24577a}
.i11-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #24577a;border-right:0}
.i11-ar.l::after{right:auto;left:-2px;border-left:0;border-right:12px solid #24577a}
.i11-pk{position:absolute;display:flex;height:46px;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;font:700 23px/40px "Golos Text",sans-serif}
.i11-pk b{background:#f2694a;color:#1d1d1d;padding:0 10px;font-weight:700}.i11-pk i{background:#fff;color:#1d3f8a;padding:0 18px;font-style:normal}
.i11-fly{animation:i11f 3s ease-in-out infinite}
@keyframes i11f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def ar(x, y, w, cls=""):
    return '<div class="i11-ar %s" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (cls, x, y, w)


def rt(x, name, sub):
    return img("i11a_rt2.png", "left:%dpx;top:498px;width:112px" % x) + \
        '<div class="i11-n" style="left:%dpx;top:580px">%s</div>' % (x - 64, name) + \
        '<div class="i11-t" style="left:%dpx;top:608px;width:260px">%s</div>' % (x - 74, sub)


def ip(x):
    return img("i11a_ip.png", "left:%dpx;top:506px;width:112px" % x) + \
        '<div class="i11-t" style="left:%dpx;top:568px;width:150px">IP-пакет<br>(без метки)</div>' % (x - 18)


def pk(x, lab):
    return '<div class="i11-pk i11-fly" style="left:%dpx;top:512px"><b>%s</b><i>IP</i></div>' % (x, lab)


HTML = CSS + bg("bgk_16") + "".join([
    '<div class="step">',
    '<div class="i11-p" style="left:46px;top:155px;width:1326px;height:230px"></div>',
    '<div class="i11-h" style="left:72px;top:172px">КАК ВЫБИРАЕТСЯ ДАЛЬНЕЙШЕЕ ДЕЙСТВИЕ</div>',
    '<div class="i11-a" style="left:88px;top:210px;width:455px;height:160px;background:#d5efe1"></div>',
    '<div class="i11-h" style="left:112px;top:228px;font-size:29px">IP-ПРОДВИЖЕНИЕ</div>',
    '<ul class="i11-ul" style="left:114px;top:270px"><li>Анализ IP-адреса назначения</li>'
    '<li>Выбор следующего узла<br>по таблице IP-продвижения</li></ul>',
    ar(550, 290, 82, "l"), img("i11a_rt.png", "left:636px;top:245px;width:148px"), ar(788, 290, 84),
    '<div class="i11-a" style="left:877px;top:210px;width:479px;height:160px;background:#fcd9cf"></div>',
    '<div class="i11-h" style="left:912px;top:228px;font-size:29px">ПРОДВИЖЕНИЕ ПО МЕТКАМ</div>',
    '<ul class="i11-ul" style="left:904px;top:272px"><li>Анализ верхней метки в стеке MPLS</li>'
    '<li>Выбор операции по таблице LFIB</li></ul>',
    '</div>',
    '<div class="step">',
    '<div class="i11-p" style="left:46px;top:398px;width:1451px;height:286px"></div>',
    '<div class="i11-h" style="left:70px;top:415px">ПРИМЕР ПЕРЕДАЧИ ЧЕРЕЗ MPLS-СЕТЬ</div>',
    '<div class="i11-a" style="left:236px;top:455px;width:1072px;height:186px;background:#bfe9e4"></div>',
    '<div class="ab" style="left:318px;top:474px;width:904px;height:14px;border-top:2px solid #1d3f8a;'
    'border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a"></div>',
    '<div class="i11-t" style="left:690px;top:460px;width:170px;background:#bfe9e4;font:800 26px/32px Golos Text,sans-serif;color:#13306e">MPLS-сеть</div>',
    ip(82), ar(200, 535, 56),
    rt(262, "Входной LER", "Push: добавить 100"), rt(580, "LSR", "Swap: 100 → 200"),
    rt(870, "LSR", "Swap: 200 → 300"), rt(1168, "Выходной LER", "Pop: снять 300"),
    ar(378, 535, 38), pk(424, "100"), ar(552, 535, 24),
    ar(696, 535, 24), pk(726, "200"), ar(852, 535, 16),
    ar(984, 535, 26), pk(1015, "200"), ar(1142, 535, 22),
    ar(1284, 535, 58), ip(1350),
    '<div class="i11-t" style="left:440px;top:652px;width:660px;font-size:19px">Транспортная метка снимается перед выходом из MPLS-сети.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i11-p" style="left:46px;top:698px;width:962px;height:220px"></div>',
    '<div class="i11-h" style="left:70px;top:714px;font-size:30px">ОДНО УСТРОЙСТВО — IP-ТРАФИК И MPLS-ТРАФИК</div>',
    img("i11a_g.png", "left:104px;top:752px;width:80px"),
    '<div class="i11-x" style="left:207px;top:760px">Управление заранее подготавливает маршруты<br>и соответствия меток.</div>',
    img("i11a_a.png", "left:104px;top:832px;width:80px"),
    '<div class="i11-x" style="left:207px;top:842px">Продвижение данных использует готовые таблицы<br>при передаче пакетов.</div>',
    '</div>',
])
