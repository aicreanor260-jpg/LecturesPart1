# -*- coding: utf-8 -*-
"""pptx: Режимы развёртывания SR — без контроллера и с контроллером, фон bgk_10."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 115

CSS = """<style>
.i70-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i70-hd{position:absolute;height:44px;border-radius:22px;font:800 30px/44px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i70-t{position:absolute;font:500 19px/1.15 "Golos Text",sans-serif;color:#1d2a44}
.i70-n{position:absolute;font:800 20px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:80px}
.i70-l{position:absolute;font:600 17px/1.2 "Golos Text",sans-serif;color:#13306e}
.i70-ft{position:absolute;border-radius:16px;font:800 21px/1.15 "Golos Text",sans-serif;color:#13306e;text-align:center;display:flex;align-items:center;justify-content:center}
.i70-pl{position:absolute;background:#c6ebdd;border-radius:14px;font:800 22px/40px "Golos Text",sans-serif;color:#13306e;text-align:center}
.i70-ic{position:absolute;width:54px;height:54px;border-radius:50%;background:#dcefe9}
.i70-fly{animation:i70f 2.6s ease-in-out infinite}
@keyframes i70f{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
</style>"""

M = ('<marker id="i70m%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
     '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>')


def net(dx, dy):
    pts = {"R1": (352, 350), "R2": (530, 282), "R3": (704, 350), "R4": (530, 400)}
    out = ['<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><g style="stroke:#1d3f8a;stroke-width:2.5">']
    for a, b in (("R1", "R2"), ("R2", "R3"), ("R1", "R4"), ("R4", "R3")):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x1 + 38 + dx, y1 + 22 + dy, x2 + 38 + dx, y2 + 22 + dy))
    out.append('</g></svg>')
    for n, (x, y) in pts.items():
        out.append(img("i70a_rt.png", "left:%dpx;top:%dpx;width:76px" % (x + dx, y + dy)))
        ny = y + dy + (56 if n != "R2" else 52)
        out.append('<div class="i70-n" style="left:%dpx;top:%dpx">%s</div>' % (x + dx - 2, ny + (2 if n == "R4" else 0), n))
    return "".join(out)


def item(x, y, ic, text, ty=None):
    return ('<div class="i70-ic" style="left:%dpx;top:%dpx"></div>' % (x, y) + img(ic, "left:%dpx;top:%dpx;width:58px" % (x - 2, y - 2)) +
            '<div class="i70-t" style="left:%dpx;top:%dpx">%s</div>' % (x + 70, ty if ty else y + 14, text))


HTML = CSS + bg("bgk_10") + "".join([
    '<div class="step">',
    '<div class="i70-p" style="left:266px;top:126px;width:586px;height:592px"></div>',
    '<div class="i70-hd" style="left:342px;top:140px;width:452px;background:#c6ebdd">Без контроллера</div>',
    img("i70a_cli.png", "left:528px;top:193px;width:76px"),
    '<div class="i70-l" style="left:616px;top:208px;font-size:19px;font-weight:500">— CLI / локальная<br>&nbsp;&nbsp;&nbsp;настройка</div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' + M % ("a", "#1d3f8a") + '</defs>'
    '<g style="stroke:#1d3f8a;stroke-width:2;stroke-dasharray:6 4">'
    '<line x1="534" y1="236" x2="388" y2="344" marker-end="url(#i70ma)"/><line x1="598" y1="236" x2="744" y2="344" marker-end="url(#i70ma)"/>'
    '<line x1="566" y1="254" x2="566" y2="276" marker-end="url(#i70ma)" marker-start="url(#i70ma)"/></g></svg>',
    net(0, 0),
    item(318, 475, "i70a_ic1.png", "Устройства обмениваются топологией<br>и SID через IGP", 480),
    item(318, 537, "i70a_ic2.png", "Входной узел выбирает путь или<br>использует заданную SR Policy", 542),
    item(318, 590, "i70a_ic3.png", "Настройка выполняется на устройствах"),
    '<div class="i70-ft" style="left:292px;top:652px;width:546px;height:56px;background:#c6ebdd">Подходит для распределённого управления.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i70-p" style="left:866px;top:126px;width:580px;height:592px"></div>',
    '<div class="i70-hd" style="left:920px;top:140px;width:444px;background:#f9b9a8">С контроллером</div>',
    img("i70a_ctl.png", "left:1103px;top:193px;width:81px"),
    '<div class="i70-l" style="left:1200px;top:212px;font-size:20px;font-weight:800">Контроллер / PCE</div>',
    '<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' +
    M % ("r", "#e8402c") + M % ("o", "#f0a020") + M % ("b", "#1f7ad6") + '</defs>'
    '<line x1="1104" y1="232" x2="962" y2="364" style="stroke:#e8402c;stroke-width:2;stroke-dasharray:6 4" marker-end="url(#i70mr)" marker-start="url(#i70mr)"/>'
    '<line x1="1124" y1="264" x2="1124" y2="308" style="stroke:#f0a020;stroke-width:3" marker-end="url(#i70mo)" marker-start="url(#i70mo)"/>'
    '<line x1="1184" y1="232" x2="1338" y2="362" style="stroke:#1f7ad6;stroke-width:2;stroke-dasharray:6 4" marker-end="url(#i70mb)"/>'
    '</svg>',
    '<div class="i70-l" style="left:930px;top:266px;color:#e8402c;font-size:19px;font-weight:800;text-align:center">PCEP:<br>SR Policy</div>',
    '<div class="i70-l" style="left:1140px;top:258px;font-weight:500">BGP-LS:<br>топология</div>',
    '<div class="i70-l" style="left:1286px;top:266px;color:#1f7ad6;font-size:19px;font-weight:800">NETCONF:<br>конфигурация</div>',
    net(578, 16),
    item(908, 485, "i70a_ic4.png", "Собирает топологию и сведения о ресурсах"),
    item(908, 537, "i70a_ic2.png", "Рассчитывает пути с учётом требований услуг"),
    item(908, 590, "i70a_ic3.png", "Передаёт политику входному узлу"),
    '<div class="i70-ft" style="left:890px;top:650px;width:540px;height:58px;background:#f9b9a8">Удобен для централизованной оптимизации<br>и автоматизации.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i70-p" style="left:290px;top:728px;width:1142px;height:88px;border-radius:12px"></div>',
    '<div style="position:absolute;left:316px;top:734px;width:202px;height:30px;border-radius:8px;background:#13306e;'
    'font:800 20px/30px Golos Text,sans-serif;color:#fff;text-align:center">Краткий словарь</div>',
    '<div class="i70-pl" style="left:390px;top:768px;width:120px">PCEP</div>',
    '<div class="i70-t" style="left:524px;top:764px;font-size:17px;line-height:1.3">— протокол взаимодействия PCE<br>&nbsp;&nbsp;&nbsp;с клиентом расчёта пути.</div>',
    '<div style="position:absolute;left:894px;top:752px;width:2px;height:54px;background:#1d3f8a"></div>',
    '<div class="i70-pl" style="left:928px;top:760px;width:134px">NETCONF</div>',
    '<div class="i70-t" style="left:1078px;top:764px;font-size:17px;line-height:1.3">— протокол управления<br>&nbsp;&nbsp;&nbsp;конфигурацией сетевых устройств.</div>',
    '</div>',
    '<div class="step">',
    '<div class="i70-p" style="left:314px;top:826px;width:1118px;height:62px;background:#fbd77a;border-color:#e3b23c;border-radius:12px"></div>',
    '<div class="i70-fly" style="position:absolute;left:0;top:0">' + img("i70a_ex.png", "left:348px;top:830px;width:54px") + '</div>',
    '<div class="i70-t" style="left:420px;top:832px;width:1000px;text-align:center;font:800 20.5px/1.25 Golos Text,sans-serif;color:#13306e">'
    'Контроллер может вести учёт ресурсов, но SR сам по себе не резервирует полосу<br>и не гарантирует QoS.</div>',
    '<div style="position:absolute;left:520px;top:896px;width:696px;height:34px;border-radius:17px;background:#cfe6fb;'
    'font:700 17.5px/34px Golos Text,sans-serif;color:#13306e;text-align:center">Выбор режима зависит от масштаба сети и задач управления.</div>',
    '</div>',
])
