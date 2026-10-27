# -*- coding: utf-8 -*-
"""pptx: LSP Ping — Echo Request и Echo Reply — вёрстка поверх bgk_09."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 152

CSS = """<style>
.i49-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i49-h{position:absolute;font:900 30px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i49-t{position:absolute;font:500 19px/1.25 "Golos Text",sans-serif;color:#1d2a44;white-space:nowrap}
.i49-n{position:absolute;font:900 22px/1.05 "Golos Text",sans-serif;color:#13306e;text-align:center;width:180px}
.i49-n small{font-size:18px;font-weight:700}
.i49-lb{position:absolute;width:58px;height:34px;background:#f2694a;border:2px solid #9a2f1c;border-radius:3px;
 font:700 20px/30px "Golos Text",sans-serif;color:#1d1d1d;text-align:center;box-sizing:border-box}
.i49-ar{position:absolute;height:3px;background:#1b7a6a}
.i49-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #1b7a6a;border-right:0}
.i49-num{position:absolute;width:56px;height:56px;border-radius:50%;background:#e2493c;color:#fff;font:900 32px/56px "Golos Text",sans-serif;text-align:center}
.i49-fly{animation:i49f 3s ease-in-out infinite}
@keyframes i49f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
.i49-dash{stroke-dasharray:14 9;animation:i49d 1.2s linear infinite}
@keyframes i49d{to{stroke-dashoffset:23}}
</style>"""


def rt(x, name, sub=""):
    s = "<br><small>%s</small>" % sub if sub else ""
    return img("i45a_rt.png", "left:%dpx;top:464px;width:108px" % x) + \
        '<div class="i49-n" style="left:%dpx;top:542px">%s%s</div>' % (x - 36, name, s)


def ar(x, w):
    return '<div class="i49-ar" style="left:%dpx;top:501px;width:%dpx"></div>' % (x, w)


def lb(x, t):
    return '<div class="i49-fly" style="position:absolute;left:%dpx;top:486px"><div class="i49-lb" style="position:static">%s</div></div>' % (x, t)


def stepcard(x, n, title, text):
    return '<div class="step">' + \
        '<div class="i49-p" style="left:%dpx;top:672px;width:376px;height:128px;border-width:2px"></div>' % x + \
        '<div class="i49-num" style="left:%dpx;top:684px">%d</div>' % (x + 14, n) + \
        '<div class="i49-t" style="left:%dpx;top:686px;font:900 22px/1 Golos Text,sans-serif;color:#13306e">%d. %s</div>' % (x + 90, n, title) + \
        '<div class="i49-t" style="left:%dpx;top:718px;font-size:18px">%s</div>' % (x + 90, text) + '</div>'


SVG = ('<svg style="position:absolute;left:0;top:0" width="1672" height="941">'
       '<path d="M250,520 C230,440 330,390 520,400 C640,370 900,380 1100,395 C1260,400 1300,460 1290,520 C1300,600 1150,630 900,622 '
       'C700,640 450,630 330,610 C250,590 240,560 250,520z" style="fill:#c4e8e0;opacity:.85"/>'
       '<path d="M406,470 L406,454 L1190,454 L1190,470" style="fill:none;stroke:#1b7a6a;stroke-width:3"/>'
       '<path d="M1182,462 L1190,474 L1198,462" style="fill:#1b7a6a"/>'
       '<path class="i49-dash" d="M1124,578 Q900,608 700,598 Q560,596 470,576" style="fill:none;stroke:#f2694a;stroke-width:3"/>'
       '<path d="M476,566 L458,574 L474,586z" style="fill:#f2694a"/>'
       '</svg>')

HTML = CSS + bg("bgk_09") + "".join([
    '<div class="step">',
    '<div class="i49-p" style="left:232px;top:164px;width:946px;height:104px;border-radius:16px"></div>',
    '<div class="i49-t" style="left:262px;top:180px;font:700 30px/1.25 Golos Text,sans-serif;color:#13306e">'
    '<b style="font-family:Rubik;font-weight:900">LSP Ping</b> проверяет передачу по конкретному LSP<br>и соответствие пути проверяемому классу FEC.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i49-p" style="left:176px;top:286px;width:1320px;height:360px"></div>',
    '<div class="i49-h" style="left:200px;top:300px">ПРОВЕРКА LSP1 К СЕТИ 105.0.0.0</div>',
    SVG,
    '<div style="position:absolute;left:626px;top:338px;display:flex;height:56px;border:2px solid #1d3f8a;font:700 20px/1.05 Golos Text,sans-serif;'
    'color:#13306e;text-align:center">'
    '<div style="width:114px;background:#f2694a;padding-top:6px;box-sizing:border-box">Метка<br>105</div>'
    '<div style="width:126px;background:#fff;padding-top:6px;box-sizing:border-box;border-left:2px solid #1d3f8a">IP / UDP<br>…</div>'
    '<div style="width:176px;background:#bfe0fa;line-height:54px;border-left:2px solid #1d3f8a">Echo Request</div></div>',
    '<div class="i49-t" style="left:710px;top:400px;font-size:18px">Проверяемая FEC: 105.0.0.0</div>',
    '<div class="i49-t" style="left:380px;top:402px;font:900 22px/1 Golos Text;color:#1b7a6a">MPLS-сеть</div>',
    '<div class="i49-t" style="left:636px;top:436px;background:#c4e8e0;padding:0 8px;font:700 21px/1 Golos Text;color:#1b7a6a">'
    'Echo Request <span style="font-size:18px">— по проверяемому LSP1</span></div>',
    rt(334, "LSR1", "Входной LER"), ar(446, 50), lb(500, "105"), ar(562, 50),
    rt(616, "LSR4"), ar(726, 42), lb(772, "177"), ar(834, 44),
    rt(882, "LSR7"), ar(992, 40), lb(1036, "210"), ar(1098, 48),
    rt(1150, "LSR8", "Выходной LER"), ar(1260, 64),
    img("i49a_cloud.png", "left:1328px;top:450px;width:162px"),
    '</div>',
    '<div class="step">',
    '<div class="i49-t" style="left:646px;top:584px;background:#c4e8e0;padding:0 8px;font:700 21px/1 Golos Text;color:#e2493c">'
    'Echo Reply — ответ выходного LER</div>',
    '<div class="i49-t" style="left:600px;top:614px;font-size:16px;font-weight:600">Обратный ответ может идти по IP-маршруту, отличному от LSP.</div>',
    '</div>',
    stepcard(274, 1, "ОТПРАВИТЬ ЗАПРОС", "Входной LER направляет<br>Echo Request вдоль<br>тестируемого LSP."),
    stepcard(664, 2, "ПРОВЕРИТЬ FEC", "Выходной LER проверяет,<br>что он является конечным узлом<br>для указанной FEC."),
    stepcard(1052, 3, "ПОЛУЧИТЬ ОТВЕТ", "Успешный Echo Reply<br>подтверждает результат<br>проверки LSP."),
    '<div class="step">',
    '<div class="i49-p" style="left:292px;top:814px;width:1090px;height:96px;background:#c4e8e0;border-width:2px;border-radius:16px"></div>',
    '<div class="i49-num" style="left:334px;top:830px;width:64px;height:64px;background:#13633f;font:900 44px/64px Golos Text">!</div>',
    '<div class="i49-t" style="left:420px;top:832px;font:700 22px/1 Golos Text;color:#13306e">Важно проверить успешный код ответа, '
    'а не только факт получения Echo Reply.</div>',
    '<div class="i49-t" style="left:420px;top:868px;font-size:18px">Отсутствие ответа может быть связано и с проблемой обратного пути.</div>',
    '</div>',
])
