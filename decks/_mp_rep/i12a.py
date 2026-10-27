# -*- coding: utf-8 -*-
"""pptx: Роли маршрутизатора (LER / LSR / CE-PE-P) — вёрстка поверх bgk_12."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i12-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i12-t{position:absolute;font:500 24px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i12-t b{font-weight:800;color:#13306e}
.i12-h{position:absolute;font:800 28px/46px "Golos Text",sans-serif;color:#13306e;padding:0 16px;border-radius:12px}
.i12-pill{display:inline-block;font:800 24px/34px "Golos Text",sans-serif;color:#13306e;padding:0 10px;border-radius:9px}
.i12-c{position:absolute;font:800 22px/1.15 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i12-ar{position:absolute;height:3px;background:#1d3f8a}
.i12-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #1d3f8a;border-right:0}
.i12-pk{position:absolute;display:flex;height:42px;border:2px solid #1d3f8a;border-radius:4px;overflow:hidden;font:600 22px/38px "Golos Text",sans-serif}
.i12-pk b{background:#f2694a;color:#1d1d1d;padding:0 9px;font-weight:600}.i12-pk i{background:#fff;color:#1d3f8a;padding:0 18px;font-style:normal}
.i12-fly{animation:i12f 3s ease-in-out infinite}
@keyframes i12f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
.i12-br{position:absolute;border-top:2px solid #1d3f8a;border-left:2px solid #1d3f8a;border-right:2px solid #1d3f8a;height:10px}
.i12-s{position:absolute;font:500 17.5px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i12-s b{font:800 21px/1.2 "Golos Text",sans-serif;color:#13306e}
</style>"""


def rt(x, y, name, op="", col=""):
    o = ('<div class="i12-c" style="left:%dpx;top:%dpx;width:200px"><span class="i12-pill" style="background:%s">%s</span></div>'
         % (x - 48, y + 104, col, op)) if op else ""
    return img("i12a_rt.png", "left:%dpx;top:%dpx;width:104px" % (x, y)) + \
        '<div class="i12-c" style="left:%dpx;top:%dpx;width:200px">%s</div>' % (x - 48, y + 76, name) + o


def ip(x, y):
    return img("i12a_ip.png", "left:%dpx;top:%dpx;width:94px" % (x, y)) + \
        '<div class="i12-c" style="left:%dpx;top:%dpx;width:130px;font-weight:500;font-size:19px;color:#1d2a44">IP-пакет<br>(без метки)</div>' % (x - 18, y + 48)


def ar(x, y, w):
    return '<div class="i12-ar" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x, y, w)


def pk(x, y, lab):
    return '<div class="i12-pk i12-fly" style="left:%dpx;top:%dpx"><b>%s</b><i>IP</i></div>' % (x, y, lab)


HTML = CSS + bg("bgk_12") + "".join([
    '<div class="step">',
    '<div class="i12-p" style="left:48px;top:156px;width:1176px;height:96px"></div>',
    '<div class="i12-t" style="left:72px;top:166px;width:1140px;font-size:30px"><b>LER (Label Edge Router)</b> — пограничный маршрутизатор, '
    'расположенный<br>на входе или выходе MPLS-сети.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i12-p" style="left:48px;top:262px;width:372px;height:224px"></div>',
    '<div class="i12-h" style="left:64px;top:272px;background:#fbd6cc">Входной LER (Ingress)</div>',
    '<div class="i12-t" style="left:76px;top:326px;width:340px;font-size:22px">Принимает пакет, определяет<br>его FEC и добавляет<br>MPLS-метку — операция<br>'
    '<span class="i12-pill" style="background:#f7a99a;margin-top:6px">Push.</span></div>',
    '<div class="i12-p" style="left:430px;top:262px;width:488px;height:224px"></div>',
    '<div class="i12-h" style="left:446px;top:272px;width:456px;background:#bfe9e4">Транзитный LSR</div>',
    '<div class="i12-t" style="left:452px;top:326px;width:460px;font-size:18.5px">LSR (Label Switching Router) — маршрутизатор, выполняющий '
    'коммутацию по меткам. Внутри MPLS-сети он читает верхнюю метку, находит запись в таблице продвижения и отправляет пакет через '
    'нужный интерфейс. Обычно при этом заменяет метку — операция <span class="i12-pill" style="background:#7ad6cc;font-size:19px;line-height:26px;padding:0 4px">Swap.</span></div>',
    '<div class="i12-p" style="left:928px;top:262px;width:382px;height:224px"></div>',
    '<div class="i12-h" style="left:942px;top:272px;background:#fbe7a6">Выходной LER (Egress)</div>',
    '<div class="i12-t" style="left:956px;top:328px;width:340px">Завершает MPLS-путь<br>и передаёт данные дальше.<br>Метка снимается на нём<br>'
    'или на предыдущем маршрутизаторе.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i12-p" style="left:244px;top:500px;width:1066px;height:226px"></div>',
    '<div style="position:absolute;left:356px;top:526px;width:808px;height:160px;background:#ccefea;border-radius:22px"></div>',
    '<div class="i12-br" style="left:474px;top:542px;width:570px"></div>',
    '<div class="i12-c" style="left:720px;top:516px;width:150px;background:#ccefea;line-height:26px">MPLS-сеть</div>',
    ip(268, 570), ar(368, 593, 40), rt(418, 558, "Ingress LER", "Push", "#f7a99a"),
    ar(528, 593, 20), pk(558, 572, 100), ar(682, 593, 16), rt(704, 558, "LSR", "Swap", "#7ad6cc"),
    ar(814, 593, 20), pk(844, 572, 200), ar(966, 593, 18), rt(994, 558, "Egress LER"),
    ar(1106, 593, 48), ip(1168, 570),
    '<div class="i12-br" style="left:360px;top:708px;width:810px;border-top:0;border-bottom:2px solid #1d3f8a;height:10px;top:700px"></div>',
    '<div class="i12-c" style="left:410px;top:697px;width:730px;white-space:nowrap;background:#fdf8ea;font:600 18px/24px Golos Text,sans-serif">'
    'Снятие метки (Pop) — на выходном LER или предыдущем маршрутизаторе.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i12-p" style="left:334px;top:736px;width:972px;height:180px"></div>',
    '<div class="i12-c" style="left:350px;top:744px;width:940px;background:#d6ebfb;border-radius:14px;font-size:24px;line-height:38px">'
    'В операторских MPLS VPN также используют обозначения CE, PE и P</div>',
    '<div class="i12-s" style="left:360px;top:788px;width:260px"><span class="i12-pill" style="background:#bfe9e4">CE</span> '
    '<b>— Customer Edge</b><br>На стороне клиента. Подключает сеть клиента к оператору; обычно MPLS не требуется.</div>',
    '<div class="i12-s" style="left:662px;top:788px;width:300px;border-left:2px solid #1d3f8a;padding-left:16px"><span class="i12-pill" style="background:#fbe7a6">PE</span> '
    '<b>— Provider Edge</b><br>На границе сети оператора. Подключает клиентов, обеспечивает VPN-сервисы и обработку сервисных меток.</div>',
    '<div class="i12-s" style="left:990px;top:788px;width:290px;border-left:2px solid #1d3f8a;padding-left:16px"><span class="i12-pill" style="background:#fbd6cc">P</span> '
    '<b>— Provider</b><br>Внутри сети оператора. Переносит трафик между PE по транспортным меткам.</div>',
    '</div>',
])
