# -*- coding: utf-8 -*-
"""pptx: Общая информация о сегментной маршрутизации (SR) — фон bgk_03."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 230

CSS = """<style>
.i67-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:20px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i67-h{position:absolute;font:800 22px/1.15 "Golos Text",sans-serif;color:#13306e}
.i67-t{position:absolute;font:500 19.5px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i67-n{position:absolute;font:800 21px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:180px}
.i67-rq{position:absolute;left:146px;width:188px;height:46px;border-radius:12px;font:500 19px/46px "Golos Text",sans-serif;color:#13306e;padding-left:72px;box-sizing:border-box}
.i67-sid{position:absolute;display:flex;left:720px;top:288px;height:46px;border:3px solid #1d3f8a;border-radius:4px;overflow:hidden;
 font:700 19px/40px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i67-sid div{width:88px;border-right:2px solid #1d3f8a}.i67-sid div:last-child{width:118px;border:0;background:#fdf6e4}
.i67-fly{animation:i67f 2.8s ease-in-out infinite}
@keyframes i67f{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
</style>"""


def rt(x, name, w=120):
    return img("i67a_rt.png", "left:%dpx;top:368px;width:%dpx" % (x, w)) + \
        '<div class="i67-n" style="left:%dpx;top:458px">%s</div>' % (x + w // 2 - 90, name)


def card(x, w, ic, head, text):
    return ('<div class="i67-p" style="left:%dpx;top:586px;width:%dpx;height:196px;border-radius:14px"></div>' % (x, w) +
            img(ic, "left:%dpx;top:608px;width:86px" % (x + 10)) +
            '<div class="i67-h" style="left:%dpx;top:612px">%s</div>' % (x + 106, head) +
            '<div class="i67-t" style="left:%dpx;top:651px">%s</div>' % (x + 106, text))


M = ('<marker id="i67m" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto">'
     '<path d="M0 0L10 5L0 10z" style="fill:#1d4f6e"/></marker>')


def ar(x1, x2, y):
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:#1d4f6e;stroke-width:5" marker-end="url(#i67m)"/>' % (x1, y, x2, y)


HTML = CSS + bg("bgk_03") + "".join([
    '<div class="step">',
    '<div class="i67-p" style="left:96px;top:252px;width:1480px;height:318px"></div>',
    '<div style="position:absolute;left:124px;top:268px;width:232px;height:250px;background:#e0efe6;border-radius:18px"></div>',
    '<div class="i67-h" style="left:124px;top:282px;width:232px;text-align:center">Требования<br>услуги</div>',
    '<div class="i67-rq" style="top:340px;background:#f9c8bd">Задержка</div>',
    '<div class="i67-rq" style="top:396px;background:#bfe5cd">Полоса</div>',
    '<div class="i67-rq" style="top:454px;background:#bfdcf5">Потери</div>',
    img("i67a_ic1.png", "left:160px;top:344px;width:42px"), img("i67a_ic2.png", "left:160px;top:400px;width:42px"),
    img("i67a_ic3.png", "left:160px;top:458px;width:42px"),
    img("i67a_pc.png", "left:418px;top:318px;width:184px"),
    '<div class="i67-n" style="left:400px;top:460px;width:220px;font-size:23px">Расчёт пути</div>',
    '<div class="i67-t" style="left:380px;top:488px;width:260px;text-align:center;font-size:18px">Топология + телеметрия</div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' + M + '</defs>' +
    ar(358, 410, 400) + ar(606, 672, 400) + ar(830, 918, 408) + ar(1070, 1156, 408) + ar(1306, 1388, 408) +
    '<path d="M762 488 V506 H1464 V488" style="fill:none;stroke:#1d3f8a;stroke-width:2"/>'
    '<path d="M694 276 H1128 V350 H772 L760 362 L748 350 H694 Z" style="fill:#fdf8ea;stroke:#1d3f8a;stroke-width:2"/>'
    '</svg>',
    '</div>',
    '<div class="step">',
    rt(698, "Входной узел"), rt(940, "Сегмент 1", 116), rt(1178, "Сегмент 2", 114), rt(1408, "Выход", 114),
    '<div class="i67-fly" style="position:absolute;left:0;top:0"><div class="i67-sid">'
    '<div style="background:#f68a5c">SID 1</div><div style="background:#bfe5cd">SID 2</div>'
    '<div style="background:#a9d3f5">SID 3</div><div>Данные</div></div></div>',
    '<div style="position:absolute;left:646px;top:522px;width:896px;height:36px;background:#cfeee4;border-radius:10px;'
    'font:700 19.5px/36px Golos Text,sans-serif;color:#13306e;text-align:center">Входной узел задаёт список сегментов; сеть выполняет их последовательно.</div>',
    '</div>',
    '<div class="step">', card(158, 450, "i67a_gear.png", "1. Расширение протоколов",
                               "OSPF, IS-IS и BGP с расширениями<br>распространяют SID. В SR-MPLS<br>это позволяет обойтись без LDP<br>"
                               "и RSVP-TE для сигнализации<br>SR-путей."), '</div>',
    '<div class="step">', card(618, 450, "i67a_sign.png", "2. Управление от источника",
                               "Путь задаётся на входном узле<br>списком сегментов. Его может<br>рассчитать сам узел<br>или контроллер."), '</div>',
    '<div class="step">', card(1078, 476, "i67a_tgt.png", "3. Путь под требования услуги",
                               "Контроллер учитывает топологию,<br>доступные ресурсы и измерения<br>и выбирает путь по заданным<br>ограничениям."), '</div>',
    '<div class="step">',
    '<div class="i67-p" style="left:242px;top:796px;width:1186px;height:80px;border-radius:14px"></div>',
    img("i67a_bulb.png", "left:306px;top:806px;width:64px"),
    '<div class="i67-h" style="left:386px;top:814px;font-size:21px">SID — идентификатор сегмента. SR-MPLS кодирует сегменты метками MPLS, SRv6 — IPv6 SID.</div>',
    '<div class="i67-t" style="left:542px;top:845px;font-size:16.5px">Выбор пути под требования не заменяет настройку механизмов QoS.</div>',
    '</div>',
])
