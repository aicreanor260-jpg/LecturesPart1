# -*- coding: utf-8 -*-
"""pptx: Таблицы MPLS — упрощённая таблица продвижения — вёрстка поверх bgk_09."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 132

CSS = """<style>
.i19-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i19-h{position:absolute;font:800 33px/1 "Golos Text",sans-serif;color:#13306e}
.i19-t{position:absolute;font:500 23px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i19-tb{position:absolute;border-collapse:separate;border-spacing:0;border:3px solid #13306e;border-radius:10px;overflow:hidden;
 font:500 25px/50px "Golos Text",sans-serif;color:#13306e}
.i19-tb th{background:#13306e;color:#fff;font:700 20px/52px "Golos Text",sans-serif}
.i19-tb td{text-align:center;border-top:2px solid #13306e}.i19-tb td:first-child{text-align:left;padding-left:18px}
.i19-tb td+td,.i19-tb th+th{border-left:2px solid #13306e}
.i19-row{position:absolute;border-radius:12px}
.i19-s{position:absolute;font:800 20px/1 "Golos Text",sans-serif;color:#13306e}
.i19-sw{position:absolute;font:800 20px/30px "Golos Text",sans-serif;color:#13306e;text-align:center;border-radius:15px;width:96px}
.i19-pk{position:absolute;display:flex;height:46px;border:2px solid #1d3f8a;border-left:6px solid #1d3f8a;border-radius:3px;overflow:hidden;font:500 24px/42px "Golos Text",sans-serif}
.i19-pk b{padding:0 10px;font-weight:500;color:#1d1d1d;border-right:2px solid #1d3f8a}.i19-pk i{background:#fff;padding:0 22px 0 18px;font-style:normal;color:#13306e}
.i19-ar{position:absolute;height:3px;background:#1d3f8a}
.i19-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #1d3f8a;border-right:0}
.i19-c{position:absolute;font:700 20px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:80px}
.i19-op{position:absolute;height:84px;border-radius:12px;display:flex;align-items:center;padding-left:22px;gap:26px}
.i19-op div{font:500 17px/1.3 "Golos Text",sans-serif;color:#1d2a44}.i19-op b{display:block;font:800 25px/1.2 "Golos Text",sans-serif;color:#13306e}
.i19-fly{animation:i19f 3s ease-in-out infinite}
@keyframes i19f{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}
</style>"""


def example(y, bg_, col, title, a, b, si, so):
    return "".join([
        '<div class="i19-row" style="left:884px;top:%dpx;width:544px;height:150px;background:%s"></div>' % (y, bg_),
        '<div class="i19-s" style="left:898px;top:%dpx">%s</div>' % (y + 10, title),
        '<div class="i19-sw" style="left:1114px;top:%dpx;background:%s">Swap</div>' % (y + 36, col),
        '<div class="i19-pk" style="left:916px;top:%dpx"><b style="background:%s">%s</b><i>IP</i></div>' % (y + 70, col, a),
        '<div class="i19-c" style="left:942px;top:%dpx">%s</div>' % (y + 124, si),
        '<div class="i19-ar" style="left:1064px;top:%dpx;width:40px"></div>' % (y + 92),
        img("i19a_rt.png", "left:1114px;top:%dpx;width:96px" % (y + 68)),
        '<div class="i19-ar" style="left:1222px;top:%dpx;width:50px"></div>' % (y + 92),
        '<div class="i19-pk i19-fly" style="left:1282px;top:%dpx"><b style="background:%s">%s</b><i>IP</i></div>' % (y + 70, col, b),
        '<div class="i19-c" style="left:1308px;top:%dpx">%s</div>' % (y + 124, so)])


def op(x, w, bgc, ic, name, t):
    return '<div class="i19-op" style="left:%dpx;top:752px;width:%dpx;background:%s">' % (x, w, bgc) + \
        img(ic, "position:static;width:62px") + '<div><b>%s —</b>%s</div></div>' % (name, t)


HTML = CSS + bg("bgk_09") + "".join([
    '<div class="step">',
    '<div class="i19-p" style="left:48px;top:138px;width:1414px;height:142px"></div>',
    '<div class="i19-t" style="left:74px;top:150px;width:1380px;font:800 29px/1.3 Golos Text,sans-serif;color:#13306e">'
    'Таблица продвижения MPLS определяет, куда передать пакет с полученной меткой<br>и какое действие выполнить над этой меткой.</div>',
    '<div class="i19-t" style="left:74px;top:230px;width:1380px;font-size:27px">Согласованные записи на нескольких маршрутизаторах образуют путь через MPLS-сеть.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i19-p" style="left:48px;top:296px;width:802px;height:382px"></div>',
    '<div class="i19-h" style="left:76px;top:312px">Упрощённая таблица продвижения</div>',
    '<table class="i19-tb" style="left:72px;top:366px;width:760px"><tr><th style="width:236px">Входной интерфейс</th><th style="width:158px">Метка</th>'
    '<th style="width:206px">Следующий хоп</th><th>Действия</th></tr>'
    '<tr style="background:#fbd6cc"><td>S0</td><td>245</td><td>S1</td><td>256</td></tr>'
    '<tr style="background:#cdeedd"><td>S0</td><td>27</td><td>S2</td><td>45</td></tr>'
    '<tr style="background:#fff"><td>…</td><td>…</td><td>…</td><td>…</td></tr></table>',
    '<div class="i19-t" style="left:82px;top:588px;width:760px;font-size:21px;line-height:1.55">„Следующий хоп“ в этом примере — выходной интерфейс.<br>'
    'Число в поле „Действия“ — новая метка; подразумевается Swap.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i19-p" style="left:866px;top:296px;width:580px;height:382px"></div>',
    '<div class="i19-h" style="left:890px;top:312px">Как читаются строки</div>',
    example(358, "#fbe0d6", "#f7845f", "1. Заменить 245 на 256 и отправить через S1", 245, 256, "S0", "S1"),
    example(518, "#d9f0e4", "#7fd6a0", "2. Заменить 27 на 45 и отправить через S2", 27, 45, "S0", "S2"),
    '</div>',
    '<div class="step">',
    '<div class="i19-p" style="left:250px;top:694px;width:1010px;height:196px"></div>',
    '<div class="i19-h" style="left:272px;top:708px;font-size:28px">Поле действий описывает операцию, а не только число</div>',
    op(272, 314, "#fbe0d6", "i19a_p1.png", "Push", "добавить метку в стек"),
    op(598, 332, "#d9f0e4", "i19a_p2.png", "Swap", "заменить верхнюю метку"),
    op(942, 300, "#dbeaf8", "i19a_p3.png", "Pop", "снять верхнюю метку"),
    '<div class="i19-t" style="left:272px;top:848px;width:980px;font-size:20.5px">В общем случае запись содержит операцию и необходимые параметры: '
    'например, <b>Swap 256</b>.</div>',
    '</div>',
])
