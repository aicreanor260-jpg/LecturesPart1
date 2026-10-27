# -*- coding: utf-8 -*-
"""pptx: RSVP — направления, маршруты и мягкое состояние. Фон bgk_09 (Кальцифер и Наусика справа, Дзидзи слева)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 126

CSS = """<style>
.i36-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i36-h{position:absolute;font:800 30px/1 "Golos Text",sans-serif;color:#13306e}
.i36-t{position:absolute;font:500 21px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i36-l{position:absolute;font:800 21px/1 "Golos Text",sans-serif}
.i36-s{position:absolute;font:700 17px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:120px}
.i36-fly{animation:i36f 3s ease-in-out infinite}
@keyframes i36f{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
</style>"""

R, G, B = "#f2694a", "#2a9d5e", "#13306e"


def ln(x1, y1, x2, y2, c, w=4, extra=""):
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%d" %s/>' % (x1, y1, x2, y2, c, w, extra)


def head(x2, y, c, rev=False):
    d = -1 if not rev else 1
    return '<path d="M%d,%dl%d,-9v18z" fill="%s"/>' % (x2, y, 16 * d, c)


def svg(body):
    return '<svg class="ab" style="left:0;top:0" width="1672" height="941" viewBox="0 0 1672 941">%s</svg>' % body


HTML = CSS + bg("bgk_09") + "".join([
    # ---- два направления
    '<div class="step">',
    '<div class="i36-p" style="left:84px;top:134px;width:744px;height:302px"></div>',
    '<div class="i36-h" style="left:110px;top:154px">Два направления — два резервирования</div>',
    img("i36a_lta.png", "left:110px;top:235px;width:140px"), img("i36a_ltb.png", "left:660px;top:235px;width:140px"),
    svg(ln(260, 262, 626, 262, G, 9) + '<path d="M648,262l-26,-17v34z" fill="%s"/>' % G +
        ln(282, 305, 648, 305, R, 9) + '<path d="M260,305l26,-17v34z" fill="%s"/>' % R),
    '<div class="i36-l" style="left:330px;top:224px;color:%s">Резервирование A → B</div>' % G,
    '<div class="i36-l" style="left:330px;top:324px;color:%s">Резервирование B → A</div>' % R,
    '<div class="i36-t" style="left:110px;top:390px">Для обратного потока источник и получатель меняются ролями.</div>',
    '</div>',
    # ---- маршрут
    '<div class="step">',
    '<div class="i36-p" style="left:846px;top:134px;width:744px;height:302px"></div>',
    '<div class="i36-h" style="left:876px;top:152px">Резервирование связано с маршрутом</div>',
    '<div class="i36-t" style="left:876px;top:196px;width:700px">Path следует маршруту данных, а Resv возвращается по этому<br>'
    'пути в обратном направлении. Ресурсы резервируются<br>на тех узлах, через которые идёт поток.</div>',
    img("i36a_lta.png", "left:868px;top:310px;width:114px"), img("i36a_ltb.png", "left:1460px;top:310px;width:114px"),
    "".join(img("i36a_rt.png", "left:%dpx;top:318px;width:84px" % x) for x in (1045, 1188, 1324)),
    svg("".join(ln(a, 342, b - 14, 342, G) + head(b, 342, G) + ln(a + 14, 382, b, 382, R) + head(a, 382, R, True)
                for a, b in ((984, 1044), (1130, 1188), (1272, 1324), (1410, 1466)))),
    '<div class="i36-l" style="left:1144px;top:296px;color:%s">Path / данные</div>' % G,
    '<div class="i36-l" style="left:1182px;top:398px;color:%s">Resv</div>' % R,
    '</div>',
    # ---- soft state
    '<div class="step">',
    '<div class="i36-p" style="left:128px;top:458px;width:700px;height:292px"></div>',
    '<div class="i36-h" style="left:152px;top:474px">Мягкое состояние — soft state</div>',
    svg(ln(176, 595, 500, 595, B, 3) + ln(500, 595, 596, 595, G, 3) + ln(596, 595, 768, 595, R, 3, 'stroke-dasharray="10 7"')
        + '<path d="M786,595l-18,-9v18z" fill="%s"/>' % B + ln(520, 556, 658, 556, G, 3, 'stroke-dasharray="10 7"')
        + ln(596, 586, 596, 604, B, 2) + ln(694, 586, 694, 604, B, 2)),
    "".join(img("i36a_ref.png", "left:%dpx;top:520px;width:70px" % x) +
            '<div class="i36-s" style="left:%dpx;top:607px">Path / Resv</div>' % (x - 25) for x in (200, 326, 452)),
    img("i36a_tmr.png", "left:658px;top:512px;width:94px"),
    '<div class="i36-s" style="left:636px;top:610px">Тайм-аут</div>',
    '<div class="i36-t" style="left:196px;top:652px;width:620px">Сообщения Path и Resv периодически обновляют состояние. '
    'Если обновления прекращаются, по тайм-ауту состояние удаляется и ресурсы освобождаются.</div>',
    '</div>',
    # ---- явная отмена
    '<div class="step">',
    '<div class="i36-p" style="left:846px;top:458px;width:656px;height:292px"></div>',
    '<div class="i36-h" style="left:878px;top:474px">Явная отмена</div>',
    img("i36a_pt.png", "left:946px;top:513px;width:98px"), img("i36a_rtr.png", "left:946px;top:590px;width:98px"),
    '<div class="i36-t" style="left:1066px;top:538px"><span style="font-weight:800;color:#13306e">PathTear</span> — со стороны источника</div>',
    '<div class="i36-t" style="left:1066px;top:612px"><span style="font-weight:800;color:#13306e">ResvTear</span> — со стороны получателя</div>',
    '<div class="i36-t" style="left:878px;top:672px;width:610px">Сообщения отмены удаляют соответствующее состояние<br>без ожидания тайм-аута.</div>',
    '</div>',
    # ---- RSVP-TE
    '<div class="step">',
    '<div class="i36-p" style="left:264px;top:766px;width:1150px;height:126px"></div>',
    img("i36a_sign.png", "left:298px;top:778px;width:102px"),
    '<div class="i36-t" style="left:426px;top:782px;width:980px"><span style="font:900 26px/1.4 Rubik,sans-serif;color:#13306e">От RSVP к RSVP-TE</span><br>'
    'Обычный RSVP следует IP-маршрутизации и сам не выбирает путь для инжиниринга трафика.<br>'
    'Расширение RSVP-TE используется в MPLS для сигнализации TE-путей.</div>',
    '</div>',
])
