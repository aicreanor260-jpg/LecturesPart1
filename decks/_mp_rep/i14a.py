# -*- coding: utf-8 -*-
"""pptx: FEC — назначение метки и PHP — вёрстка поверх bgk_18."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 74

CSS = """<style>
.i14-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i14-h{position:absolute;font:800 32px/1 "Golos Text",sans-serif;color:#13306e}
.i14-t{position:absolute;font:500 22px/1.32 "Golos Text",sans-serif;color:#1d2a44}
.i14-t b{font-weight:800;color:#13306e}
.i14-ic{position:absolute;width:104px;height:104px;border-radius:50%;background:#ccefea}
.i14-c{position:absolute;font:700 20px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i14-pl{position:absolute;font:800 21px/34px "Golos Text",sans-serif;color:#13306e;text-align:center;background:#fbd56a;border-radius:17px}
.i14-ar{position:absolute;height:3px;background:#1d3f8a}
.i14-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #1d3f8a;border-right:0}
.i14-pk{position:absolute;display:flex;height:46px;border:2px solid #1d3f8a;border-radius:3px;overflow:hidden;font:500 23px/42px "Golos Text",sans-serif}
.i14-pk b{background:#f2694a;padding:0 6px;font-weight:500;color:#1d1d1d}.i14-pk i{background:#fff;padding:0 16px 0 14px;font-style:normal;color:#13306e}
.i14-fly{animation:i14f 3s ease-in-out infinite}
@keyframes i14f{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}
</style>"""


def ar(x, y, w):
    return '<div class="i14-ar" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (x, y, w)


def rt(x, name, op):
    return img("i14a_rt.png", "left:%dpx;top:528px;width:100px" % x) + \
        '<div class="i14-c" style="left:%dpx;top:610px;width:240px">%s</div>' % (x - 70, name) + \
        '<div class="i14-pl" style="left:%dpx;top:638px;width:126px">%s</div>' % (x - 13, op)


def ip(x, txt=""):
    t = '<div class="i14-c" style="left:%dpx;top:596px;width:150px;font-weight:500">%s</div>' % (x - 24, txt) if txt else ""
    return img("i14a_ip.png", "left:%dpx;top:540px;width:100px" % x) + t


def pk(x, lab):
    return '<div class="i14-pk i14-fly" style="left:%dpx;top:542px"><b>%s</b><i>IP</i></div>' % (x, lab)


HTML = CSS + bg("bgk_18") + "".join([
    '<div class="step"><div style="position:absolute;left:340px;top:78px;width:1000px;text-align:center;font:800 30px/1.2 Rubik,sans-serif;color:#fffbe8;text-shadow:0 2px 0 #1550a8,0 3px 8px rgba(10,40,90,.5)">Назначение метки и удаление на предпоследнем хопе (PHP)</div></div>',
    '<div class="step">',
    '<div class="i14-p" style="left:284px;top:128px;width:1170px;height:274px"></div>',
    '<div class="i14-h" style="left:316px;top:142px">На входе в MPLS-домен</div>',
    '<div class="i14-t" style="left:316px;top:180px;width:1000px">Входной LER определяет FEC пакета и по таблице <b>FTN</b> выбирает действие:<br>'
    'добавляет метку и направляет пакет в соответствующий LSP. Пакеты одного FEC<br>получаю␣ одинаковое обслуживание при пересылке.</div>'
    .replace("␣", "т"),
    '</div>',
    '<div class="step">',
    '<div class="i14-ic" style="left:312px;top:280px"></div>', img("i14a_ic1.png", "left:310px;top:282px;width:108px"),
    '<div class="i14-t" style="left:440px;top:286px;width:390px;font-size:18px"><b style="font-size:24px">LER: классификация пакетов</b><br>'
    '<span style="display:block;margin-top:12px">Основная логика отнесения пакета<br>к FEC выполняется на границе сети.</span></div>',
    '<div style="position:absolute;left:840px;top:284px;width:2px;height:100px;background:#1d3f8a"></div>',
    '<div class="i14-ic" style="left:868px;top:280px"></div>', img("i14a_ic2.png", "left:866px;top:282px;width:110px"),
    '<div class="i14-t" style="left:998px;top:286px;width:450px;font-size:18px;line-height:1.35"><b style="font-size:24px">LSR: продвижение по метке</b><br>'
    'Промежуточные узлы используют верхнюю<br>метку и таблицу продвижения. При переходе<br>между узлами значение метки может меняться.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i14-p" style="left:284px;top:420px;width:1336px;height:262px"></div>',
    '<div class="i14-h" style="left:316px;top:434px">Пример: один уровень меток и обычная IP-передача на выходе</div>',
    '<div style="position:absolute;left:440px;top:480px;width:1010px;height:192px;background:#ccefea;border-radius:20px"></div>',
    '<div style="position:absolute;left:528px;top:498px;width:824px;height:14px;border:2px solid #1d3f8a;border-bottom:0"></div>',
    '<div class="i14-c" style="left:840px;top:484px;width:200px;background:#ccefea;font-size:23px;line-height:28px">MPLS-домен</div>',
    ip(312, "IP-пакет<br>(без метки)"), ar(418, 565, 40),
    rt(468, "Входной LER", "Push"), ar(574, 565, 30),
    pk(612, 100), ar(728, 565, 22),
    rt(758, "Транзитный LSR", "Swap"), ar(864, 565, 28),
    pk(900, 200), ar(1016, 565, 22),
    rt(1042, "Предпоследний LSR", "Pop (PHP)"), ar(1148, 565, 28),
    ip(1180), ar(1284, 565, 22),
    rt(1310, "Выходной LER", "IP-поиск"), ar(1418, 565, 56),
    ip(1488, "Следующая<br>IP-сеть"),
    '</div>',
    '<div class="step">',
    '<div class="i14-p" style="left:330px;top:702px;width:1290px;height:222px"></div>',
    '<div class="i14-h" style="left:360px;top:714px">PHP — Penultimate Hop Popping</div>',
    '<div class="i14-t" style="left:360px;top:750px;width:1250px;font-size:19px;white-space:nowrap">Предпоследний LSR сначала определяет следующий хоп по метке, '
    'затем снимает её и передаёт пакет выходному LER.<br>В этом примере выходной LER получает обычный IP-пакет и выполняет IP-поиск: '
    'ему не требуется отдельно снимать MPLS-метку.</div>',
    '<div class="i14-t" style="left:358px;top:816px;width:1202px;height:48px;background:#fbe7a6;border-radius:12px;padding-left:74px;'
    'font:700 20px/48px Golos Text,sans-serif;color:#13306e">Без PHP метка снимается на выходном LER. Для внешних IP-сетей MPLS остаётся прозрачной.</div>',
    '<div class="i14-c" style="left:380px;top:822px;width:30px;font-size:30px;line-height:36px">💡</div>',
    '<div class="i14-c" style="left:464px;top:876px;width:28px;height:28px;border-radius:50%;background:#2a5fb0;color:#fff;font:800 18px/28px Golos Text">i</div>',
    '<div class="i14-t" style="left:506px;top:876px;width:900px;font-size:17px;line-height:28px">При стеке меток PHP удаляет верхнюю метку; под ней может оставаться другая.</div>',
    '</div>',
])
