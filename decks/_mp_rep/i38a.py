# -*- coding: utf-8 -*-
"""pptx: RSVP-TE — подготовка к установлению LSP и отправка Path. Фон bgk_01 (белый волк справа)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 162

CSS = """<style>
.i38-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i38-h{position:absolute;font:800 31px/1 "Golos Text",sans-serif;color:#13306e}
.i38-num{position:absolute;width:64px;height:64px;border-radius:50%;background:#f2694a;color:#fff;font:900 32px/64px "Rubik",sans-serif;text-align:center}
.i38-t{position:absolute;font:500 19px/1.35 "Golos Text",sans-serif;color:#1d2a44}
.i38-mint{position:absolute;background:#c6ece4;border-radius:14px}
.i38-n{position:absolute;font:800 30px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:180px}
.i38-n small{display:block;font:500 21px/1.4 "Golos Text",sans-serif}
.i38-st{position:absolute;background:#c6ece4;border-radius:10px;font:500 21px/44px "Golos Text",sans-serif;color:#13306e;text-align:center;width:212px}
.i38-path{position:absolute;background:#fcd6cc;border-radius:6px;font:600 27px/44px "Golos Text",sans-serif;color:#e2564a;text-align:center;width:112px}
.i38-ar{position:absolute;height:4px;background:#f2694a}
.i38-ar::after{content:"";position:absolute;right:-2px;top:-8px;border:10px solid transparent;border-left:14px solid #f2694a;border-right:0}
.i38-fly{animation:i38f 2.6s ease-in-out infinite}
@keyframes i38f{0%,100%{transform:translateX(0)}50%{transform:translateX(10px)}}
</style>"""


def rt(x, name, sub="", st=False):
    s = '<div class="i38-st" style="left:%dpx;top:618px">%s</div>' % (x + 18, "Состояние пути") if st else ""
    return img("i38a_rt.png", "left:%dpx;top:482px;width:134px" % x) + \
        '<div class="i38-n" style="left:%dpx;top:592px">%s%s</div>' % (x - 23, name, "<small>%s</small>" % sub if sub else "") + s


HTML = CSS + bg("bgk_01") + "".join([
    '<div class="step">',
    '<div class="i38-p" style="left:56px;top:168px;width:842px;height:184px"></div>',
    '<div class="i38-num" style="left:76px;top:178px">1.</div>',
    '<div class="i38-h" style="left:160px;top:188px">Сведения о сети → TED</div>',
    '<div class="i38-t" style="left:148px;top:238px">OSPF-TE или IS-IS-TE распространяет<br>топологию и характеристики каналов.</div>',
    img("i38a_ted.png", "left:546px;top:220px;width:96px"),
    '<div class="i38-mint" style="left:652px;top:214px;width:230px;height:128px"></div>',
    '<div class="i38-t" style="left:664px;top:222px;font-size:17px;line-height:1.38">Метрики<br>'
    '&nbsp;•&nbsp; доступная для<br>&nbsp;&nbsp;&nbsp;&nbsp;резервирования полоса<br>&nbsp;•&nbsp; административные<br>&nbsp;&nbsp;&nbsp;&nbsp;характеристики</div>',
    '</div>',
    '<div class="step">',
    '<div class="i38-p" style="left:912px;top:168px;width:704px;height:184px"></div>',
    '<div class="i38-num" style="left:930px;top:178px">2.</div>',
    '<div class="i38-h" style="left:1012px;top:188px">Расчёт пути на LER1</div>',
    '<div class="i38-t" style="left:1012px;top:228px;font-size:18px">Назначение: LER2.<br>Требуемая полоса: 100 Мбит/с.</div>',
    '<div class="i38-t" style="left:984px;top:284px;font-size:18px">CSPF исключает неподходящие участки<br>и выбирает кратчайший допустимый путь.</div>',
    '<div class="i38-mint" style="left:1370px;top:240px;width:232px;height:72px"></div>',
    img("i38a_gear.png", "left:1376px;top:255px;width:44px"),
    '<div class="i38-t" style="left:1428px;top:254px;font-size:16px;line-height:1.3">Путь можно задать<br>и административно.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i38-p" style="left:180px;top:366px;width:1312px;height:524px"></div>',
    '<div class="i38-num" style="left:204px;top:380px">3.</div>',
    '<div class="i38-h" style="left:300px;top:394px;font-size:36px;font-family:Golos Text,sans-serif;font-weight:800">LER1 формирует и отправляет Path</div>',
    rt(310, "LER1", "Входной"), rt(630, "LSR1", st=True), rt(940, "LSR2", st=True), rt(1264, "LER2", "Выходной"),
    '</div>',
    '<div class="step">',
    "".join('<div class="i38-fly" style="position:absolute;left:0;top:0"><div class="i38-path" style="left:%dpx;top:488px">Path</div>'
            '<div class="i38-ar" style="left:%dpx;top:540px;width:%dpx"></div></div>' % (px, ax, aw)
            for px, ax, aw in ((480, 450, 168), (796, 770, 160), (1110, 1080, 172))),
    '</div>',
    '<div class="step">',
    '<div class="i38-mint" style="left:424px;top:692px;width:882px;height:92px"></div>',
    '<div class="i38-t" style="left:424px;top:702px;width:882px;text-align:center;font-size:21px;color:#13306e">'
    '<span style="font:800 30px/1.3 Golos Text,sans-serif">ERO: LSR1 → LSR2 → LER2</span><br>Строгие переходы: через указанные соседние устройства</div>',
    '<div class="i38-t" style="left:344px;top:814px;width:1054px;height:54px;background:#d6ebfb;border-radius:12px;text-align:center;'
    'font:600 18px/54px Golos Text,sans-serif;color:#13306e">Path создаёт состояние пути. Метки и резервирование согласуются при прохождении Resv обратно.</div>',
    '</div>',
])
