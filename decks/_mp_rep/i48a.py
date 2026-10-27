# -*- coding: utf-8 -*-
"""pptx: мониторинг состояния путей LSP (OAM, LSP Ping/Traceroute, BFD) — вёрстка поверх bgk_23."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 112

CSS = """<style>
.i48-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i48-h{position:absolute;font:900 31px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i48-t{position:absolute;font:500 22px/1.42 "Golos Text",sans-serif;color:#1d2a44}
.i48-n{position:absolute;font:900 22px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:60px}
.i48-pill{position:absolute;border-radius:12px;font:500 18px/34px "Golos Text",sans-serif;text-align:center;white-space:nowrap}
.i48-ch{position:absolute;border-radius:22px;height:62px;font:900 30px/62px "Rubik",sans-serif;color:#13306e;padding-left:96px;box-sizing:border-box}
.i48-task{position:absolute;border-radius:12px;font:500 19px/56px "Golos Text",sans-serif;color:#1d2a44;text-align:center;white-space:nowrap}
.i48-dash{stroke-dasharray:10 8;animation:i48d 1.2s linear infinite}
@keyframes i48d{to{stroke-dashoffset:-18}}
</style>"""


def rt(x, y, name, nx, ny):
    return img("i45a_rt.png", "left:%dpx;top:%dpx;width:98px" % (x, y)) + \
        '<div class="i48-n" style="left:%dpx;top:%dpx">%s</div>' % (nx - 30, ny, name)


def card(x, w, bgc, ic, icw, title, text, task, tbg, tsz=21, tfs=19):
    return '<div class="step">' + \
        '<div class="i48-p" style="left:%dpx;top:572px;width:%dpx;height:258px;border-width:2px"></div>' % (x, w) + \
        '<div class="i48-ch" style="left:%dpx;top:584px;width:%dpx;background:%s">%s</div>' % (x + 18, w - 40, bgc, title) + \
        img(ic, "left:%dpx;top:582px;width:%dpx" % (x + 20, icw)) + \
        '<div class="i48-t" style="left:%dpx;top:656px;width:%dpx;font-size:%dpx;line-height:1.36">%s</div>' % (x + 30, w - 40, tsz, text) + \
        '<div class="i48-task" style="left:%dpx;top:%dpx;width:%dpx;background:%s;font-size:%dpx"><b>Задача:</b> %s</div>' % (
            x + 46 if tsz > 19 else x + 18, 756 if tsz > 19 else 780, w - 92 if tsz > 19 else w - 40, tbg, tfs, task) + \
        '</div>'


SVG = ('<svg style="position:absolute;left:0;top:0" width="1672" height="941"><defs>'
       '<marker id="i48r" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto">'
       '<path d="M0,0 L16,8 L0,16z" style="fill:#f2694a"/></marker>'
       '<marker id="i48b" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto">'
       '<path d="M0,0 L16,8 L0,16z" style="fill:#1f63c6"/></marker></defs>'
       '<path d="M736,404 Q780,380 838,378" style="fill:none;stroke:#f2694a;stroke-width:3" marker-end="url(#i48r)"/>'
       '<path class="i48-dash" d="M938,380 L1030,382" style="fill:none;stroke:#f2694a;stroke-width:3"/>'
       '<path class="i48-dash" d="M1060,384 Q1110,388 1142,404" style="fill:none;stroke:#f2694a;stroke-width:3" marker-end="url(#i48r)"/>'
       '<path class="i48-dash" d="M734,446 Q800,478 884,482" style="fill:none;stroke:#1f63c6;stroke-width:3" marker-end="url(#i48b)"/>'
       '<path class="i48-dash" d="M990,480 Q1080,474 1144,442" style="fill:none;stroke:#1f63c6;stroke-width:3" marker-end="url(#i48b)"/>'
       '<text x="1046" y="396" style="fill:#c0281f;font:900 40px Golos Text,sans-serif" text-anchor="middle">✕</text>'
       '</svg>')

HTML = CSS + bg("bgk_23") + "".join([
    '<div class="step">',
    '<div class="i48-p" style="left:152px;top:118px;width:1370px;height:168px"></div>',
    '<div class="i48-h" style="left:178px;top:134px">OAM <span style="font-size:28px">— эксплуатация, администрирование и техническое '
    'обслуживание</span></div>',
    '<div class="i48-t" style="left:178px;top:184px;width:960px;font-size:23px">Оператору нужно не только передавать трафик, но и проверять<br>'
    'доступность LSP, обнаруживать отказы и локализовывать неисправности.</div>',
    '<div class="i48-t" style="left:1146px;top:180px;width:356px;height:96px;background:#f5dc8a;border:2px solid #c9a23a;border-radius:16px;'
    'padding:8px 0 0 114px;box-sizing:border-box;font-size:19px;line-height:1.25">Пример требований<br>к готовности:<br>'
    '<b style="font-size:27px">99,9–99,999 %</b></div>',
    img("i48a_gear.png", "left:1164px;top:188px;width:82px"),
    '</div>',
    '<div class="step">',
    '<div class="i48-p" style="left:98px;top:302px;width:1476px;height:254px"></div>',
    '<div class="i48-h" style="left:124px;top:320px">Почему обычного IP ping недостаточно?</div>',
    '<div class="i48-t" style="left:126px;top:380px;width:500px;font-size:23px">Успешный IP ping подтверждает<br>IP-достижимость, но не '
    'гарантирует<br>исправность конкретного LSP:<br>пакет может пройти по другому пути.</div>',
    SVG,
    rt(633, 386, "R1", 682, 466), rt(842, 352, "R2", 888, 420), rt(892, 448, "R3", 940, 518), rt(1146, 386, "R4", 1197, 460),
    '<div class="i48-pill" style="left:910px;top:320px;width:190px;background:#f2694a;color:#fff">Проверяемый LSP</div>',
    '<div class="i48-pill" style="left:982px;top:508px;width:232px;background:#cfe6fb;color:#13306e">Возможный обход по IP</div>',
    '<div style="position:absolute;left:1272px;top:342px;width:2px;height:182px;background:#1d3f8a"></div>',
    '<div class="i48-t" style="left:1302px;top:342px;width:242px;height:182px;background:#c4e8e0;border-radius:18px;text-align:center;'
    'font:900 26px/1.15 Golos Text,sans-serif;color:#13306e;padding-top:76px;box-sizing:border-box">IP доступен<br>'
    '<span style="color:#e2342b">≠</span><br>LSP исправен</div>',
    '<div class="i48-t" style="left:1394px;top:356px;width:56px;height:56px;border-radius:50%;background:#f5d24a;border:3px solid #13306e;'
    'box-sizing:border-box;text-align:center;font:900 32px/50px Golos Text">!</div>',
    '</div>',
    card(182, 414, "#bfe9d6", "i48a_ic1.png", 80, "LSP Ping",
         "Проверяет работоспособность пути и соответствие пересылки указанному FEC.", "проверить LSP.", "#c4e8e0"),
    card(604, 386, "#f9b5a6", "i48a_ic2.png", 92, "LSP Traceroute",
         "Поэтапно исследует путь и помогает определить участок, где нарушена передача.", "локализовать проблему.", "#f9d0c4", 21, 18),
    card(998, 426, "#f5dc8a", "i48a_ic3.png", 84, "BFD для LSP",
         "Лёгкие периодические сообщения позволяют быстро обнаруживать потерю связности. Скорость зависит от настроенных таймеров и "
         "возможностей устройств.", "непрерывно обнаруживать отказ.", "#f5dc8a", 18, 17),
    '<div class="step">',
    '<div class="i48-t" style="left:232px;top:848px;width:1210px;height:60px;background:#f9e48a;border:2px solid #1f63c6;border-radius:30px;'
    'text-align:center;font:500 25px/56px Golos Text,sans-serif;color:#13306e;white-space:nowrap;padding-left:60px;box-sizing:border-box">'
    '<b>LSP Ping / Traceroute</b> — диагностика.&nbsp; <b>BFD</b> — быстрое обнаружение потери связности.</div>',
    img("i48a_bulb.png", "left:282px;top:850px;width:56px"),
    '</div>',
])
