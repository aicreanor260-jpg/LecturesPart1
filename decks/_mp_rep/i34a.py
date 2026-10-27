# -*- coding: utf-8 -*-
"""pptx: RSVP — этапы 4–7, обработка RESV и пример объединения. Фон bgk_26 (Котобус и Тоторо справа)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 182

CSS = """<style>
.i34-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i34-h{position:absolute;font:800 32px/1 "Golos Text",sans-serif;color:#13306e}
.i34-num{position:absolute;width:46px;height:46px;border-radius:50%;background:#bfe9e4;color:#13306e;font:900 28px/46px "Rubik",sans-serif;text-align:center}
.i34-t{position:absolute;white-space:nowrap;font:500 18px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i34-n{position:absolute;font:800 22px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:100px}
.i34-l{position:absolute;font:800 19px/1 "Golos Text",sans-serif}
.i34-sum{position:absolute;background:#c6ece4;border-radius:22px;font:800 23px/46px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i34-fly{animation:i34f 3s ease-in-out infinite}
@keyframes i34f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""

R, G = "#f2694a", "#2a9d72"


def ln(x1, y1, x2, y2, c):
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="4" marker-end="url(#i34%s)"/>' % (
        x1, y1, x2, y2, c, "r" if c == R else "g")


SVG = ('<svg class="ab" style="left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941"><defs>'
       '<marker id="i34r" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8z" fill="%s"/></marker>'
       '<marker id="i34g" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0L8,4L0,8z" fill="%s"/></marker></defs>'
       % (R, G) + ln(768, 675, 546, 675, R) + ln(546, 698, 766, 698, G)
       + '<path d="M880,668 L916,630" stroke="#1f6f7a" stroke-width="3" fill="none"/><path d="M880,722 L916,742" stroke="#1f6f7a" stroke-width="3" fill="none"/>'
       + ln(1172, 630, 920, 630, R) + ln(916, 652, 1170, 652, G) + ln(1172, 734, 920, 734, R) + ln(916, 758, 1170, 758, G) + '</svg>')


def blk(x, y, n, head, ico, iw, txt, tx):
    return '<div class="i34-p" style="left:%dpx;top:%dpx;width:648px;height:172px"></div>' % (x, y) + \
        '<div class="i34-num" style="left:%dpx;top:%dpx">%s</div>' % (x + 26, y + 12, n) + \
        '<div class="i34-h" style="left:%dpx;top:%dpx">%s</div>' % (x + 92, y + 18, head) + \
        img(ico, "left:%dpx;top:%dpx;width:%dpx" % (x + 28, y + 62, iw)) + \
        '<div class="i34-t" style="left:%dpx;top:%dpx;width:%dpx">%s</div>' % (x + tx, y + 60, 640 - tx, txt)


HTML = CSS + bg("bgk_26") + "".join([
    '<div class="step">',
    blk(184, 192, "4", "Проверка запроса", "i34a_ic4.png", 110, "Маршрутизатор проверяет свободные ресурсы<br>и право на резервирование. "
        "При отказе — ResvErr<br>в сторону получателя; при успехе — RESV дальше<br>к источнику.", 156),
    blk(846, 192, "5", "Настройка QoS", "i34a_ic5.png", 160, "Сохраняется состояние резервирования.<br>Параметры передаются классификатору<br>"
        "и планировщику, учитываются занятые<br>полоса и буферы.", 216),
    '</div>',
    '<div class="step">',
    blk(184, 378, "6", "Объединение запросов", "i34a_ic6.png", 108, "Для одного multicast-потока запросы получателей<br>объединяются на "
        "общем участке дерева.<br>В простом случае выбирается максимальная<br>полоса.", 166),
    blk(846, 378, "7", "Передача данных", "i34a_ic7.png", 112, "После успешного резервирования пакеты потока<br>обслуживаются с "
        "согласованным QoS вдоль пути<br>к получателям.", 204),
    '</div>',
    '<div class="step">',
    '<div class="i34-p" style="left:190px;top:562px;width:1302px;height:322px"></div>',
    '<div class="i34-h" style="left:220px;top:578px;font-size:30px">Пример: один поток — два получателя</div>',
    SVG,
    img("i34a_lt.png", "left:424px;top:646px;width:118px"), '<div class="i34-n" style="left:428px;top:734px">C1</div>',
    img("i34a_rt.png", "left:776px;top:648px;width:116px"), '<div class="i34-n" style="left:782px;top:736px">R1</div>',
    img("i34a_lt.png", "left:1176px;top:596px;width:88px"), '<div class="i34-n" style="left:1170px;top:664px">C2</div>',
    img("i34a_lt.png", "left:1176px;top:714px;width:88px"), '<div class="i34-n" style="left:1170px;top:784px">C3</div>',
    '<div class="i34-l" style="left:590px;top:648px;color:%s">RESV: 5 Мбит/с</div>' % R,
    '<div class="i34-l" style="left:624px;top:710px;color:%s">Данные</div>' % G,
    '<div class="i34-l" style="left:962px;top:602px;color:%s">RESV: 2 Мбит/с</div>' % R,
    '<div class="i34-l" style="left:1000px;top:658px;color:%s">Данные</div>' % G,
    '<div class="i34-l" style="left:962px;top:708px;color:%s">RESV: 5 Мбит/с</div>' % R,
    '<div class="i34-l" style="left:1000px;top:762px;color:%s">Данные</div>' % G,
    '</div>',
    '<div class="step">',
    '<div class="i34-sum" style="left:504px;top:794px;width:678px;height:46px">Общий участок: max(2, 5) = 5 Мбит/с, а не 7 Мбит/с</div>',
    '<div class="i34-t" style="left:190px;top:850px;width:1302px;text-align:center;font-size:17px">'
    'RSVP резервирует ресурсы; IP-пакеты следуют таблице маршрутизации.</div>',
    '</div>',
])
