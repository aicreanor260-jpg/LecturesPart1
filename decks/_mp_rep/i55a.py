# -*- coding: utf-8 -*-
"""pptx: протокол BFD — вёрстка поверх bgk_01."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 200

CSS = """<style>
.i55-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i55-h{position:absolute;font:900 34px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i55-t{position:absolute;font:500 19px/1.28 "Golos Text",sans-serif;color:#1d2a44}
.i55-n{position:absolute;font:900 28px/1 "Golos Text",sans-serif;color:#13306e}
.i55-pill{position:absolute;border-radius:20px;font:600 22px/40px "Golos Text",sans-serif;text-align:center}
.i55-ln{position:absolute;height:4px}
.i55-ln.r::after,.i55-ln.l::before{content:"";position:absolute;top:-8px;border:10px solid transparent}
.i55-ln.r::after{right:-4px;border-left:16px solid currentColor;border-right:0}
.i55-ln.l::before{left:-4px;border-right:16px solid currentColor;border-left:0}
.i55-st{position:absolute;border-radius:14px;height:96px}
.i55-big{position:absolute;font:600 23px/1.25 "Golos Text",sans-serif;color:#13306e}
.i55-arw{position:absolute;font:900 42px/1 "Golos Text";color:#13306e}
.i55-env{animation:i55e 3s linear infinite}
@keyframes i55e{0%{transform:translateX(-12px)}50%{transform:translateX(12px)}100%{transform:translateX(-12px)}}
</style>"""


def env(x, y):
    return img("i55a_env.png", "left:%dpx;top:%dpx;width:46px" % (x, y), "ab i55-env")


CARDS = [
    (48, 520, "i55a_c1.png", 60, "BFD и LSP Ping",
     "LSP Ping проверяет соответствие<br>FEC и помогает диагностике.<br>BFD выполняет частый контроль<br>"
     "доступности с меньшими затратами<br>на обработку."),
    (580, 512, "i55a_c2.png", 592, "Работа в MPLS",
     "Для показанного режима:<br>MPLS → IP → UDP → BFD Control.<br>LSP Ping может использоваться<br>"
     "для начальной проверки FEC<br>и запуска BFD-сеанса."),
    (1104, 520, "i55a_c3.png", 1116, "Обратное направление",
     "Нужен обратный канал для<br>контрольного обмена.<br>Это может быть обратный LSP<br>"
     "или IP-маршрут — в зависимости<br>от режима."),
]

HTML = CSS + bg("bgk_01") + "".join([
    '<div class="i55-p" style="left:22px;top:205px;width:1600px;height:458px"></div>',
    '<div class="step">',
    '<div class="i55-h" style="left:68px;top:220px">Постоянный контроль между двумя конечными узлами</div>',
    '<div style="position:absolute;left:136px;top:272px;width:1398px;height:232px;background:#d3eee4;border-radius:30px"></div>',
    '<div class="i55-pill" style="left:592px;top:274px;width:486px;background:#a6e3cf;color:#13306e">Контролируемый LSP: BFD Control →</div>',
    img("i55a_rt.png", "left:160px;top:326px;width:142px"),
    img("i55a_rt.png", "left:1372px;top:326px;width:142px"),
    img("i55a_rt.png", "left:776px;top:310px;width:116px"),
    img("i55a_rt.png", "left:776px;top:386px;width:116px"),
    '<div class="i55-n" style="left:198px;top:438px">LER1</div><div class="i55-n" style="left:1406px;top:440px">LER2</div>',
    '<div class="i55-t" style="left:900px;top:358px;font-weight:600;font-size:18px">Транзитный узел</div>',
    '<div class="i55-t" style="left:900px;top:433px;font-weight:600;font-size:18px">Транзитный узел</div>',
    '</div>',
    '<div class="step">',
    '<div class="i55-ln r" style="left:298px;top:343px;width:462px;color:#1aa58a;background:#1aa58a"></div>',
    '<div class="i55-ln r" style="left:892px;top:343px;width:478px;color:#1aa58a;background:#1aa58a"></div>',
    env(408, 330), env(558, 330), env(1068, 330), env(1222, 330),
    '</div>',
    '<div class="step">',
    '<div class="i55-ln l" style="left:306px;top:414px;width:470px;color:#13306e;background:#13306e"></div>',
    '<div class="i55-ln l" style="left:902px;top:414px;width:476px;color:#13306e;background:#13306e"></div>',
    env(468, 402), env(634, 402), env(998, 402), env(1158, 402),
    '<div class="i55-pill" style="left:648px;top:464px;width:394px;background:#14396e;color:#fff">Обратный канал: ← BFD Control</div>',
    '<div class="i55-t" style="left:136px;top:516px;width:1398px;text-align:center;font:700 22px/1 Golos Text;color:#13306e">'
    'BFD контролирует доступность; причину и точное место отказа ищут другими средствами.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i55-st" style="left:66px;top:555px;width:458px;background:#d3eee4"></div>',
    img("i55a_m1.png", "left:88px;top:576px;width:118px"),
    '<div class="i55-big" style="left:242px;top:590px">Пакеты поступают</div>',
    '<div class="i55-arw" style="left:538px;top:586px">→</div>',
    '<div class="i55-st" style="left:594px;top:555px;width:468px;background:#f9d3cc"></div>',
    img("i55a_m2.png", "left:636px;top:572px;width:100px"),
    '<div class="i55-big" style="left:760px;top:576px">Нет пакетов в течение<br>времени обнаружения</div>',
    '<div class="i55-arw" style="left:1074px;top:586px">→</div>',
    '<div class="i55-st" style="left:1130px;top:555px;width:476px;background:#f9d3cc"></div>',
    img("i55a_m3.png", "left:1158px;top:562px;width:90px"),
    '<div class="i55-big" style="left:1268px;top:576px">Состояние Down →<br>сигнал механизмам защиты</div>',
    '</div>',
    "".join('<div class="step">'
            + '<div class="i55-p" style="left:%dpx;top:676px;width:%dpx;height:176px"></div>' % (x, w)
            + img(ic, "left:%dpx;top:688px;width:108px" % ix)
            + '<div class="i55-h" style="left:%dpx;top:688px;font-size:27px">%s</div>' % (x + 136, t)
            + '<div class="i55-t" style="left:%dpx;top:722px">%s</div>' % (x + 136, body)
            + '</div>' for x, w, ic, ix, t, body in CARDS),
    '<div class="step">',
    '<div class="i55-p" style="left:150px;top:864px;width:1370px;height:62px;background:#d3f0dc;border-color:#9fd3b4;border-radius:14px"></div>',
    img("i55a_ok.png", "left:246px;top:874px;width:52px"),
    '<div class="i55-t" style="left:320px;top:882px;font:800 23px/1 Golos Text;color:#13306e">'
    'BFD обнаруживает отказ; переключение трафика выполняет настроенный механизм защиты.</div>',
    '</div>',
])
