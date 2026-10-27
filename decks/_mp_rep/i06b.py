# -*- coding: utf-8 -*-
"""pptx 6b: IP-передача и виртуальный канал — обычная маршрутизация и MPLS TE; вёрстка поверх bgk_24."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 190
DX = 756  # сдвиг правой схемы

CSS = """<style>
.i6b-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.22)}
.i6b-h{position:absolute;font:900 30px/1 "Rubik",sans-serif;color:#13306e}
.i6b-t{position:absolute;font:500 25px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i6b-t b{font-weight:800;color:#13306e}
.i6b-cl{position:absolute;background:#d7eedd;border-radius:120px}
.i6b-pl{position:absolute;border-radius:16px;text-align:center;font:500 19px/34px "Golos Text",sans-serif;color:#1d2a44}
.i6b-r{position:absolute;font:900 23px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:80px}
.i6b-tag{position:absolute;background:#fdd768;border:2px solid #b8860b;border-radius:6px;font:800 18px/28px "Golos Text",sans-serif;color:#13306e;padding:0 8px}
.i6b-fly{animation:i6bf 2.6s ease-in-out infinite}
@keyframes i6bf{0%,100%{transform:translateX(0)}50%{transform:translateX(6px)}}
</style>"""


def rt(x, y, w, name, lx, ly):
    return img("i06b_rt.png", "left:%dpx;top:%dpx;width:%dpx" % (x, y, w)) + \
        '<div class="i6b-r" style="left:%dpx;top:%dpx">%s</div>' % (lx - 40, ly, name)


def routers(d):
    return "".join([rt(122 + d, 408, 86, "PE1", 160 + d, 476), rt(426 + d, 376, 82, "P1", 466 + d, 437),
                    rt(722 + d, 406, 86, "PE2", 766 + d, 476), rt(306 + d, 470, 80, "P2", 345 + d, 532),
                    rt(518 + d, 470, 80, "P3", 558 + d, 532)])


def orange(d):
    seg = [(206, 426, 236, 414), (292, 412, 330, 406), (390, 401, 425, 396), (508, 401, 570, 405),
           (626, 409, 648, 412), (702, 424, 724, 434)]
    p = "".join('<path d="M%d,%d L%d,%d" marker-end="url(#i6b-mo)"/>' % (a + d, b, c + d, e) for a, b, c, e in seg)
    ips = "".join(img("i06b_ip.png", "left:%dpx;top:%dpx;width:58px" % (x + d, y), "ab i6b-fly")
                  for x, y in [(236, 398), (333, 390), (572, 394), (650, 401)])
    return p, ips


SVG = """<svg class="ab" style="left:0;top:0;width:1672px;height:941px;pointer-events:none" viewBox="0 0 1672 941">
<defs><marker id="i6b-mo" markerWidth="4" markerHeight="4" refX="2.5" refY="2" orient="auto"><path d="M0,0L4,2L0,4z" style="fill:#f0663f"/></marker>
<marker id="i6b-mg" markerWidth="4" markerHeight="4" refX="2.5" refY="2" orient="auto"><path d="M0,0L4,2L0,4z" style="fill:#7d8a80"/></marker>
<marker id="i6b-mt" markerWidth="4" markerHeight="4" refX="2.5" refY="2" orient="auto"><path d="M0,0L4,2L0,4z" style="fill:#1fa760"/></marker></defs>
<g style="fill:none;stroke-width:5;stroke-linecap:round">
<g style="stroke:#f0663f">%s%s</g>
<g style="stroke:#7d8a80"><path d="M196,462 Q212,494 228,497" marker-end="url(#i6b-mg)"/><path d="M288,498 L304,498" marker-end="url(#i6b-mg)"/>
<path d="M386,498 L426,498" marker-end="url(#i6b-mg)"/><path d="M486,498 L516,498" marker-end="url(#i6b-mg)"/>
<path d="M598,498 L624,498" marker-end="url(#i6b-mg)"/><path d="M684,490 Q712,478 734,456" marker-end="url(#i6b-mg)"/></g>
<g style="stroke:#1fa760"><path d="M952,462 Q966,490 982,494" marker-end="url(#i6b-mt)"/><path d="M1050,498 L1064,498" marker-end="url(#i6b-mt)"/>
<path d="M1142,500 L1178,500" marker-end="url(#i6b-mt)"/><path d="M1248,500 L1272,500" marker-end="url(#i6b-mt)"/>
<path d="M1352,498 L1380,496" marker-end="url(#i6b-mt)"/><path d="M1452,490 Q1472,478 1490,458" marker-end="url(#i6b-mt)"/></g>
</g></svg>"""

pL, iL = orange(0)
pR, iR = orange(DX)


def pill(x, y, w, col, txt):
    return '<div class="i6b-pl" style="left:%dpx;top:%dpx;width:%dpx;height:34px;background:%s">%s</div>' % (x, y, w, col, txt)


HTML = CSS + bg("bgk_24") + "".join([
    '<div class="step">',
    '<div class="i6b-p" style="left:116px;top:196px;width:1440px;height:66px"></div>',
    '<div class="i6b-t" style="left:116px;top:212px;width:1446px;text-align:center"><b>Детерминированный маршрут</b> — '
    'заранее определённый путь через сеть для трафика соответствующего LSP.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i6b-p" style="left:80px;top:275px;width:756px;height:442px"></div>',
    '<div class="i6b-p" style="left:840px;top:275px;width:752px;height:442px"></div>',
    '<div class="i6b-h" style="left:102px;top:290px">Обычная IP-маршрутизация</div>',
    '<div class="i6b-h" style="left:868px;top:290px">MPLS Traffic Engineering</div>',
    '<div class="i6b-cl" style="left:104px;top:340px;width:712px;height:250px"></div>',
    '<div class="i6b-cl" style="left:862px;top:340px;width:710px;height:250px"></div>',
    SVG % (pL, pR),
    routers(0), routers(DX), iL, iR,
    "".join(img("i06b_ipg.png", "left:%dpx;top:%dpx;width:58px" % (x, 482), "ab i6b-fly") for x in (230, 428, 626)),
    pill(280, 336, 400, "#f9c8b8", "Путь 1 • метрика 10 • высокая загрузка"),
    pill(1046, 336, 394, "#f9c8b8", "Путь 1 • метрика 10 • высокая загрузка"),
    pill(278, 556, 362, "#cfe9c4", "Путь 2 • метрика 30 • есть ресурс"),
    pill(1024, 556, 380, "#cfe9c4", "Путь 2 • метрика 30 • есть ресурс"),
    '</div>',
    '<div class="step">',
    '<div class="i6b-t" style="left:255px;top:630px;font:800 29px/1.2 Golos Text,sans-serif;color:#13306e">Выбор по метрике: путь 1.</div>',
    '<div class="i6b-t" style="left:255px;top:670px;font-size:18px">Высокая загрузка сама по себе не обязательно меняет метрику.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i6b-tag i6b-fly" style="left:984px;top:483px">MPLS</div>',
    '<div class="i6b-tag i6b-fly" style="left:1182px;top:486px">MPLS</div>',
    '<div class="i6b-tag i6b-fly" style="left:1384px;top:480px">MPLS</div>',
    '<div class="i6b-pl" style="left:1122px;top:590px;width:186px;height:36px;background:#fde072;font-weight:800;color:#13306e;font-size:21px">LSP по пути 2</div>',
    '<div class="i6b-t" style="left:862px;top:638px;width:710px;text-align:center;font:800 28px/1.22 Golos Text,sans-serif;color:#13306e">'
    'MPLS TE позволяет направить часть трафика<br>по пути 2 с учётом ограничений.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i6b-p" style="left:262px;top:744px;width:1138px;height:136px"></div>',
    img("i06b_ex.png", "left:292px;top:765px;width:94px"),
    '<div class="i6b-pl" style="left:388px;top:786px;width:170px;height:60px;line-height:60px;background:#fde58a;'
    'font:900 38px/60px Rubik,sans-serif;color:#13306e">Важно</div>',
    '<div class="ab" style="left:580px;top:770px;width:3px;height:95px;background:#13306e"></div>',
    '<div class="i6b-t" style="left:598px;top:766px;font:800 24px/1.2 Golos Text,sans-serif;color:#13306e">'
    'Не каждый LSP проходит по специально заданному маршруту.</div>',
    '<div class="i6b-t" style="left:598px;top:806px;font-size:22px"><b>LDP:</b> LSP обычно следует путям IP-маршрутизации.</div>',
    '<div class="i6b-t" style="left:598px;top:840px;font-size:22px"><b>MPLS TE:</b> выбор пути с дополнительными ограничениями.</div>',
    '</div>',
])
