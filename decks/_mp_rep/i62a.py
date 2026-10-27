# -*- coding: utf-8 -*-
"""pptx: отказоустойчивость путей MPLS — сходимость IGP — вёрстка поверх bgk_13."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 132

CSS = """<style>
.i62-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i62-h{position:absolute;font:900 31px/1 "Rubik",sans-serif;color:#13306e;white-space:nowrap}
.i62-t{position:absolute;font:500 19px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i62-n{position:absolute;font:800 24px/1 "Golos Text",sans-serif;color:#13306e;width:110px;text-align:center;white-space:nowrap}
.i62-st{position:absolute;top:524px;height:72px;border:2px solid #9cc4ec;border-radius:12px;background:#fdf8ea}
.i62-num{position:absolute;top:540px;width:40px;height:40px;border-radius:50%;background:#ec6a52;color:#fff;font:900 22px/40px "Rubik";text-align:center}
.i62-ar{position:absolute;font:900 26px/1 "Golos Text";color:#13306e;top:546px}
.i62-red{animation:i62r 1.4s ease-in-out infinite}
@keyframes i62r{0%,100%{opacity:1}50%{opacity:.35}}
.i62-new{stroke-dasharray:14 8;animation:i62d 1s linear infinite}
@keyframes i62d{to{stroke-dashoffset:-22}}
</style>"""


def rt(x, y, w=106):
    return img("i62a_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w))


STEPS = [(226, 270, "i62a_s1.png", "Обнаружение<br>отказа", True), (526, 346, "i62a_s2.png", "OSPF / IS-IS<br>обновляет топологию", False),
         (902, 282, "i62a_s3.png", "Расчёт нового<br>next hop", True), (1214, 326, "i62a_s4.png", "Обновление<br>MPLS-продвижения", True)]

SVG = ('<svg class="ab" style="left:0;top:0;width:1672px;height:941px;overflow:visible" viewBox="0 0 1672 941"><defs>'
       '<marker id="i62g" markerWidth="5" markerHeight="5" refX="3" refY="2.5" orient="auto"><path d="M0,0L5,2.5L0,5z" style="fill:#7d8ca4"/></marker>'
       '<marker id="i62e" markerWidth="5" markerHeight="5" refX="3" refY="2.5" orient="auto"><path d="M0,0L5,2.5L0,5z" style="fill:#16b08a"/></marker>'
       '</defs>'
       '<line x1="372" y1="359" x2="780" y2="359" style="stroke:#7d8ca4;stroke-width:5" marker-end="url(#i62g)"/>'
       '<line x1="894" y1="359" x2="1060" y2="359" style="stroke:#7d8ca4;stroke-width:5"/>'
       '<line x1="1106" y1="359" x2="1276" y2="359" style="stroke:#7d8ca4;stroke-width:5" marker-end="url(#i62g)"/>'
       '<g class="step"><path class="i62-new" d="M386,398 C520,390 480,462 594,462" style="fill:none;stroke:#16b08a;stroke-width:6" marker-end="url(#i62e)"/>'
       '<line class="i62-new" x1="716" y1="484" x2="958" y2="484" style="stroke:#16b08a;stroke-width:6" marker-end="url(#i62e)"/>'
       '<path class="i62-new" d="M1082,460 C1190,460 1180,396 1284,396" style="fill:none;stroke:#16b08a;stroke-width:6" marker-end="url(#i62e)"/></g>'
       '</svg>')

HTML = CSS + bg("bgk_13") + "".join([
    '<div class="step">',
    '<div class="i62-p" style="left:162px;top:138px;width:1348px;height:120px"></div>',
    '<div class="i62-t" style="left:190px;top:154px;font-size:26px;line-height:1.2"><b style="font:900 32px Rubik;color:#13306e">Цель</b> — '
    'восстановить передачу трафика<br>после отказа интерфейса, линии связи<br>или маршрутизатора LSR.</div>',
    '<div style="position:absolute;left:792px;top:156px;height:86px;border-left:2px solid #13306e"></div>',
    img("i62a_if.png", "left:862px;top:148px;width:136px"), img("i62a_ln.png", "left:1078px;top:148px;width:160px"),
    img("i62a_nd.png", "left:1315px;top:148px;width:127px"),
    '<div class="i62-n" style="left:874px;top:224px;width:110px">Интерфейс</div>',
    '<div class="i62-n" style="left:1102px;top:228px;width:110px">Линия связи</div>',
    '<div class="i62-n" style="left:1326px;top:224px">Узел LSR</div>',
    '</div>',
    '<div class="step">',
    '<div class="i62-p" style="left:162px;top:270px;width:1348px;height:384px"></div>',
    '<div class="i62-h" style="left:188px;top:284px">Базовый механизм: сходимость IGP</div>',
    '<div style="position:absolute;left:218px;top:322px;width:174px;height:126px;background:#c6ecdc;border-radius:14px"></div>',
    '<div style="position:absolute;left:1282px;top:322px;width:174px;height:126px;background:#c6ecdc;border-radius:14px"></div>',
    SVG,
    rt(252, 338), rt(788, 330, 100), rt(1314, 338), rt(602, 426, 104), rt(970, 426, 104),
    '<div class="i62-n" style="left:250px;top:420px">LER1</div><div class="i62-n" style="left:782px;top:396px">LSR1</div>',
    '<div class="i62-n" style="left:1312px;top:420px">LER2</div><div class="i62-n" style="left:600px;top:494px">LSR2</div>',
    '<div class="i62-n" style="left:968px;top:494px">LSR3</div>',
    '<div class="i62-t i62-red" style="left:1056px;top:330px;font:900 52px/1 Rubik;color:#e2453a">✕</div>',
    '<div class="i62-t" style="left:1010px;top:306px;font:700 22px/1 Golos Text;color:#e2453a">Отказ линии</div>',
    '<div class="i62-t" style="left:730px;top:428px;width:216px;text-align:center;font:800 22px/1.1 Golos Text;color:#16a080">'
    'Новый путь<br>после сходимости</div>',
    '</div>',
    '<div class="step">',
    "".join('<div class="i62-st" style="left:%dpx;width:%dpx"></div>' % (x, w)
            + '<div class="i62-num" style="left:%dpx">%d</div>' % (x + 14, k + 1)
            + img(ic, "left:%dpx;top:538px;width:46px" % (x + 68))
            + '<div class="i62-t" style="left:%dpx;top:536px;font-size:18px;line-height:1.3;%s">%s</div>'
            % (x + 122, "font-weight:700;color:#13306e" if b else "", t)
            for k, (x, w, ic, t, b) in enumerate(STEPS)),
    '<div class="i62-ar" style="left:500px">→</div><div class="i62-ar" style="left:876px">→</div><div class="i62-ar" style="left:1188px">→</div>',
    '<div style="position:absolute;left:226px;top:604px;width:1272px;height:40px;background:#d6e8f4;border-radius:12px"></div>',
    '<div class="i62-t" style="left:226px;top:613px;width:1272px;text-align:center;color:#13306e">'
    'LDP-путь следует маршрутам IGP; для нового next hop используются соответствующие метки.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i62-p" style="left:298px;top:668px;width:684px;height:182px"></div>',
    '<div class="i62-h" style="left:320px;top:678px;font-size:26px">От чего зависит время восстановления</div>',
    img("i62a_lst.png", "left:318px;top:712px;width:54px"),
    '<div class="i62-t" style="left:386px;top:722px;font-size:17px;line-height:42px">Обнаружение отказа и таймеры<br>'
    'Сходимость протокола маршрутизации<br>Топология и установка записей продвижения</div>',
    '<div style="position:absolute;left:760px;top:716px;height:114px;border-left:2px solid #6d7c99"></div>',
    '<div style="position:absolute;left:770px;top:716px;width:196px;height:114px;background:#fbe08a;border-radius:12px"></div>',
    '<div class="i62-t" style="left:784px;top:732px;font:800 21px/1.25 Golos Text;color:#13306e">Единого<br>фиксированного<br>времени нет.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i62-p" style="left:994px;top:668px;width:636px;height:182px"></div>',
    '<div class="i62-h" style="left:1020px;top:678px;font-size:26px">Как ускорить защиту</div>',
    img("i62a_sh.png", "left:1016px;top:718px;width:98px"),
    '<div class="i62-t" style="left:1134px;top:724px;font-size:20px">Для MPLS/LDP возможна локальная защита<br>'
    '<b style="font-weight:800;color:#13306e">IP FRR</b>, например <b style="font-weight:800;color:#13306e">LFA</b>, с заранее рассчитанным<br>резервным next hop.</div>',
    '<div class="i62-t" style="left:1134px;top:816px;font-size:14px">Применимость зависит от топологии и поддержки оборудования.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i62-p" style="left:232px;top:862px;width:1376px;height:58px;background:#c6ecdc;border-color:#9fd3b4"></div>',
    img("i62a_bulb.png", "left:280px;top:868px;width:44px"),
    '<div class="i62-t" style="left:338px;top:880px;font-size:20px;color:#13306e"><b style="font-weight:800">Восстановление:</b> путь рассчитывается после отказа.</div>',
    '<div style="position:absolute;left:924px;top:872px;height:40px;border-left:2px solid #13306e"></div>',
    img("i62a_sh2.png", "left:956px;top:870px;width:41px"),
    '<div class="i62-t" style="left:1018px;top:880px;font-size:20px;color:#13306e"><b style="font-weight:800">Быстрая защита:</b> резерв подготавливается заранее.</div>',
    '</div>',
])
