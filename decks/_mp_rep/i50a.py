# -*- coding: utf-8 -*-
"""pptx: что находится внутри Echo Request — вёрстка поверх bgk_07."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 178

CSS = """<style>
.i50-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i50-box{position:absolute;border:3px solid #1d3f8a;border-radius:12px;box-sizing:border-box}
.i50-t{position:absolute;font:500 22px/1.2 "Golos Text",sans-serif;color:#1d2a44;white-space:nowrap}
.i50-k{position:absolute;font:900 31px/1 "Golos Text",sans-serif;color:#13306e;white-space:nowrap}
.i50-k span{font-size:26px;font-weight:600}.i50-k em{font-style:normal;font-size:38px}
.i50-n{position:absolute;font:900 24px/1.05 "Golos Text",sans-serif;color:#13306e;text-align:center;width:180px}
.i50-n small{font-size:20px;font-weight:700}
.i50-lb{position:absolute;width:90px;height:50px;background:#f2694a;border:2px solid #9a2f1c;border-radius:4px;
 font:700 25px/46px "Golos Text",sans-serif;color:#1d1d1d;text-align:center;box-sizing:border-box}
.i50-ar{position:absolute;height:3px;background:#13306e}
.i50-ar::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:12px solid #13306e;border-right:0}
.i50-q{position:absolute;width:90px;height:90px;border-radius:50%;background:#bfe6dd;font:900 56px/90px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i50-fly{animation:i50f 3s ease-in-out infinite}
@keyframes i50f{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
</style>"""


def rt(x, name, sub=""):
    s = "<br><small>%s</small>" % sub if sub else ""
    return img("i45a_rt.png", "left:%dpx;top:516px;width:122px" % x) + \
        '<div class="i50-n" style="left:%dpx;top:604px">%s%s</div>' % (x - 29, name, s)


def ar(x, w):
    return '<div class="i50-ar" style="left:%dpx;top:557px;width:%dpx"></div>' % (x, w)


def lb(x, t):
    return '<div class="i50-fly" style="position:absolute;left:%dpx;top:532px"><div class="i50-lb">%s</div></div>' % (x, t)


def qcard(x, title, text):
    return '<div class="step">' + \
        '<div class="i50-p" style="left:%dpx;top:716px;width:782px;height:154px;border-width:2px"></div>' % x + \
        '<div class="i50-q" style="left:%dpx;top:732px">?</div>' % (x + 46) + \
        '<div class="i50-k" style="left:%dpx;top:734px;font-size:32px">%s</div>' % (x + 166, title) + \
        '<div class="i50-t" style="left:%dpx;top:776px;color:#1f63c6">%s</div>' % (x + 166, text) + '</div>'


HTML = CSS + bg("bgk_07") + "".join([
    '<div class="i50-p" style="left:46px;top:184px;width:1580px;height:520px"></div>',
    '<div class="step">',
    '<div class="i50-box" style="left:238px;top:200px;width:1196px;height:254px;background:#f68e74"></div>',
    '<div class="i50-k" style="left:298px;top:214px">MPLS: <span>метка</span>&nbsp; <em>105</em></div>',
    '</div>',
    '<div class="step">',
    '<div class="i50-box" style="left:284px;top:262px;width:1104px;height:180px;background:#bfe9d6"></div>',
    '<div class="i50-k" style="left:356px;top:272px">IP:&nbsp; <span>SA — адрес LSR1; DA —</span>&nbsp; <em>127.0.0.1</em></div>',
    '</div>',
    '<div class="step">',
    '<div class="i50-box" style="left:344px;top:316px;width:984px;height:116px;background:#bfe0fa"></div>',
    '<div class="i50-k" style="left:420px;top:326px;font-size:30px">UDP</div>',
    '<div class="i50-box" style="left:392px;top:364px;width:888px;height:58px;background:#fff;border-width:2px;border-radius:6px"></div>',
    '<div class="i50-k" style="left:458px;top:376px"><span style="font-size:30px;font-weight:800">Echo Request:</span>&nbsp;&nbsp; '
    'FEC&nbsp; <em>105.0.0.0</em></div>',
    '</div>',
    '<div class="step">',
    '<div style="position:absolute;left:136px;top:472px;width:1400px;height:192px;background:#c4e8e0;border-radius:22px"></div>',
    '<div style="position:absolute;left:266px;top:488px;width:964px;height:20px;border:3px solid #13306e;border-bottom:0;border-radius:12px 12px 0 0"></div>',
    '<div class="i50-k" style="left:770px;top:472px;background:#c4e8e0;padding:0 16px;font-size:28px">LSP1</div>',
    rt(193, "LSR1", "Отправитель"), ar(318, 54), lb(380, "105"), ar(472, 56),
    rt(537, "LSR4"), ar(660, 50), lb(718, "177"), ar(810, 40),
    rt(858, "LSR7"), ar(982, 44), lb(1034, "210"), ar(1126, 40),
    rt(1174, "LSR8", "Выходной LER"), ar(1300, 52),
    img("i50a_cloud.png", "left:1360px;top:525px;width:225px"),
    '<div class="i50-t" style="left:440px;top:672px;font-weight:700;color:#13306e;font-size:22px">Метки меняются на каждом участке; '
    'DA и FEC сохраняются.</div>',
    '</div>',
    qcard(46, "Зачем DA = 127.0.0.1?", "Внутри LSP пакет продвигается по MPLS-меткам.<br>На выходном LER запрос передаётся локальному<br>"
          "стеку IP и обработчику LSP Ping."),
    qcard(842, "Зачем поле FEC?", "LSR8 сравнивает FEC 105.0.0.0 из запроса<br>со своими данными и проверяет, что запрос<br>"
          "пришёл к нужному выходному узлу."),
    '<div class="step">',
    '<div class="i50-t" style="left:198px;top:880px;width:1256px;height:50px;background:#fdf8ea;border:2px solid #1f63c6;border-radius:14px;'
    'box-sizing:border-box;text-align:center;font:700 21px/46px Golos Text,sans-serif;color:#13306e">'
    'MPLS-заголовок снимается на выходе или на предыдущем хопе при PHP.</div>',
    img("i50a_gear.png", "left:350px;top:884px;width:50px"),
    '</div>',
])
