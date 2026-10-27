# -*- coding: utf-8 -*-
"""pptx: Реализация пересылки SR — пример SID в SR-MPLS, SR-MPLS и SRv6, фон bgk_13."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 108

CSS = """<style>
.i68-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i68-h{position:absolute;font:900 34px/1 "Rubik",sans-serif;color:#13306e}
.i68-t{position:absolute;font:500 19px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i68-b{position:absolute;font:700 19.5px/1.32 "Golos Text",sans-serif;color:#13306e}
.i68-n{position:absolute;font:800 22px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:100px}
.i68-sid{position:absolute;border-radius:4px;color:#fff;text-align:center;font:600 17px/1.05 "Golos Text",sans-serif;padding:5px 0}
.i68-sid b{display:block;font:700 22px/1.1 "Golos Text",sans-serif}
.i68-ns{background:#1666b4}.i68-as{background:#f05a28}
.i68-pk{position:absolute;display:flex;height:62px;border:3px solid #34508a;border-radius:6px;overflow:hidden;
 font:600 19px/1.05 "Golos Text",sans-serif;color:#13306e;text-align:center}
.i68-pk div{display:flex;flex-direction:column;justify-content:center;border-right:2px solid #34508a}
.i68-pk div:last-child{border-right:0}.i68-pk small{font-size:15px;font-weight:500}
.i68-fly{animation:i68f 2.6s ease-in-out infinite}
@keyframes i68f{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
</style>"""


def rt(x, y, name, ny=None):
    return img("i68a_rt.png", "left:%dpx;top:%dpx;width:92px" % (x, y)) + \
        '<div class="i68-n" style="left:%dpx;top:%dpx">%s</div>' % (x - 4, ny if ny else y + 70, name)


def sid(x, y, w, cls, a, b):
    return '<div class="i68-fly" style="position:absolute;left:0;top:0"><div class="i68-sid %s" style="left:%dpx;top:%dpx;width:%dpx">%s<b>%s</b></div></div>' % (
        cls, x, y, w, a, b)


def pk(x, y, cells):
    return '<div class="i68-pk" style="left:%dpx;top:%dpx">%s</div>' % (x, y, "".join(
        '<div style="width:%dpx;background:%s">%s</div>' % c for c in cells))


M = ('<marker id="i68m" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
     '<path d="M0 0L10 5L0 10z" style="fill:#f05a28"/></marker>')

HTML = CSS + bg("bgk_13") + "".join([
    '<div class="step">',
    '<div class="i68-p" style="left:108px;top:120px;width:1356px;height:62px;border-radius:14px"></div>',
    '<div class="i68-t" style="left:108px;top:134px;width:1356px;text-align:center;font-size:25px;color:#13306e">'
    'SR описывает путь как последовательность сегментов. Каждый сегмент имеет идентификатор <b style="font-weight:800">SID.</b></div>',
    '</div>',
    '<div class="step">',
    '<div class="i68-p" style="left:110px;top:194px;width:1452px;height:384px"></div>',
    '<div class="i68-h" style="left:132px;top:212px">Пример SID в SR-MPLS</div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' + M + '</defs>'
    '<g style="stroke:#1d3f8a;stroke-width:3">'
    '<line x1="296" y1="386" x2="494" y2="386"/><line x1="580" y1="378" x2="796" y2="312"/>'
    '<line x1="580" y1="394" x2="796" y2="440"/><line x1="878" y1="312" x2="1096" y2="378"/>'
    '<line x1="878" y1="440" x2="1096" y2="394"/><line x1="836" y1="338" x2="836" y2="414"/>'
    '<line x1="1182" y1="386" x2="1378" y2="386"/><line x1="538" y1="334" x2="538" y2="356"/>'
    '<line x1="836" y1="256" x2="836" y2="284"/><line x1="1138" y1="334" x2="1138" y2="356"/></g>'
    '<line x1="692" y1="342" x2="782" y2="316" style="stroke:#f05a28;stroke-width:3" marker-end="url(#i68m)"/>'
    '<line x1="1000" y1="320" x2="1086" y2="358" style="stroke:#f05a28;stroke-width:3" marker-end="url(#i68m)"/>'
    '</svg>',
    rt(206, 355, "R1", 424), rt(492, 352, "R2", 424), rt(792, 282, "R3", 350), rt(792, 410, "R4", 474),
    rt(1094, 352, "R5", 424), rt(1378, 352, "R6", 424),
    sid(774, 206, 124, "i68-ns", "Node SID", "16003"), sid(476, 286, 124, "i68-ns", "Node SID", "16002"),
    sid(1076, 286, 126, "i68-ns", "Node SID", "16005"), sid(638, 276, 110, "i68-as", "Adj-SID", "16023"),
    sid(928, 274, 112, "i68-as", "Adj-SID", "16035"),
    '<div style="position:absolute;left:134px;top:498px;width:1404px;height:66px;background:#cfeee8;border-radius:10px"></div>',
    '<div class="i68-sid i68-ns" style="left:156px;top:512px;width:122px;font-size:20px;line-height:26px">Node SID</div>',
    '<div class="i68-t" style="left:290px;top:518px">— направить к узлу по пути IGP</div>',
    '<div style="position:absolute;left:634px;top:510px;width:2px;height:48px;background:#1d3f8a"></div>',
    '<div class="i68-sid i68-as" style="left:672px;top:512px;width:114px;font-size:20px;line-height:26px">Adj-SID</div>',
    '<div class="i68-t" style="left:800px;top:518px">— пройти конкретную направленную смежность</div>',
    '<div style="position:absolute;left:1258px;top:510px;width:2px;height:48px;background:#1d3f8a"></div>',
    '<div class="i68-t" style="left:1288px;top:503px;font-size:16.5px;line-height:1.28">1600X и 160XX — условная<br>нумерация этого примера,<br>а не правило стандарта.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i68-p" style="left:226px;top:592px;width:610px;height:248px"></div>',
    '<div class="i68-h" style="left:250px;top:606px">SR-MPLS</div>',
    pk(248, 652, [(158, "#e3e8f6", "IP<small>(полезные данные)</small>"), (104, "#f68a5c", "Метка<br>16023"),
                  (104, "#f68a5c", "Метка<br>16035"), (104, "#a6e3c4", "Метка<br>16005"), (82, "#dfe3f6", "…")]),
    '<div class="i68-b" style="left:252px;top:731px">SID реализуются метками MPLS.<br>Последовательность сегментов кодируется стеком меток.</div>',
    '<div class="i68-t" style="left:252px;top:794px;font-size:17.5px">Объявленный индекс SID отображается в метку с учётом SRGB.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i68-p" style="left:852px;top:592px;width:612px;height:248px"></div>',
    '<div class="i68-h" style="left:880px;top:606px">SRv6</div>',
    pk(878, 652, [(192, "#ece2f6", "IPv6<small>(базовый заголовок)</small>"), (176, "#e7b6e3", "SRH<small>(список сегментов)</small>"),
                  (52, "#ece2f6", "…"), (130, "#fdf8ea", "<small>Полезные<br>данные</small>")]),
    '<div class="i68-b" style="left:882px;top:731px">SID — 128-битный идентификатор в формате IPv6-адреса,<br>связанный с определённым действием.</div>',
    '<div class="i68-t" style="left:882px;top:788px;font-size:17.5px;line-height:1.3">Активный SID находится в адресе назначения IPv6;<br>список сегментов может передаваться в SRH.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i68-p" style="left:312px;top:856px;width:1048px;height:62px;border-radius:30px"></div>',
    img("i68a_bulb.png", "left:350px;top:853px;width:64px"),
    '<div class="i68-h" style="left:438px;top:870px;font:800 30px/1 Golos Text,sans-serif">Одна идея SR — разные способы кодирования сегментов.</div>',
    '</div>',
])
