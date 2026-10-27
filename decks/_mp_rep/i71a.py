# -*- coding: utf-8 -*-
"""pptx: Режимы развёртывания SR — явные пути для разных услуг, фон bgk_28."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 150

CSS = """<style>
.i71-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:18px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i71-t{position:absolute;font:500 19px/1.3 "Golos Text",sans-serif;color:#1d2a44}
.i71-n{position:absolute;font:800 21px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:80px}
.i71-tag{position:absolute;width:166px;height:38px;border-radius:4px;color:#fff;font:600 17.5px/38px "Golos Text",sans-serif;text-align:center}
.i71-mini{position:absolute;top:262px;height:58px;background:#fdf8ea;border:2px solid #b9d9d2;border-radius:10px}
.i71-ms{position:absolute;font:600 15px/1.25 "Golos Text",sans-serif;color:#13306e}
.i71-c{position:absolute;top:648px;height:104px;border:2px solid;border-radius:10px}
.i71-ch{position:absolute;font:800 26px/1 "Golos Text",sans-serif}
.i71-cs{position:absolute;font:500 21px/1.25 "Golos Text",sans-serif}
.i71-run{stroke-dashoffset:0;animation:i71r 1.6s linear infinite}
@keyframes i71r{to{stroke-dashoffset:-36}}
</style>"""

P = {"R1": (520, 490), "R2": (700, 426), "R3": (902, 426), "R4": (1106, 426), "R5": (700, 550), "R6": (902, 550),
     "R7": (1106, 550), "R8": (1296, 490)}
LINKS = [("R1", "R2"), ("R1", "R5"), ("R2", "R3"), ("R2", "R6"), ("R3", "R4"), ("R4", "R8"), ("R5", "R6"), ("R6", "R7"),
         ("R7", "R8"), ("R3", "R6")]
M = ('<marker id="i71m%s" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto">'
     '<path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>')


def path(nodes, dy, col, dash, mid):
    segs = []
    for a, b in zip(nodes, nodes[1:]):
        (x1, y1), (x2, y2) = P[a], P[b]
        k = 0.24
        sx, sy = x1 + (x2 - x1) * k, y1 + (y2 - y1) * k + dy
        ex, ey = x1 + (x2 - x1) * (1 - k), y1 + (y2 - y1) * (1 - k) + dy
        segs.append('<line class="i71-run" x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s;stroke-width:4;stroke-dasharray:%s" '
                    'marker-end="url(#i71m%s)"/>' % (sx, sy, ex, ey, col, dash, mid))
    return "".join(segs)


def network():
    out = ['<svg style="position:absolute;left:0;top:0;width:1672px;height:941px" viewBox="0 0 1672 941"><defs>' +
           M % ("g", "#2fa84f") + M % ("r", "#ee5a3c") + M % ("b", "#1ea0f0") + M % ("k", "#33516e") + '</defs>'
           '<g style="stroke:#1b2533;stroke-width:2.5">']
    for a, b in LINKS:
        (x1, y1), (x2, y2) = P[a], P[b]
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x1, y1, x2, y2))
    out.append('</g>')
    out.append(path(["R1", "R2", "R3", "R4", "R8"], -16, "#2fa84f", "12 6", "g"))
    out.append(path(["R1", "R5", "R3", "R4", "R8"], -4, "#ee5a3c", "14 5 3 5", "r"))
    out.append(path(["R1", "R5", "R6", "R7", "R8"], 12, "#1ea0f0", "36 0", "b"))
    out.append('<line x1="428" y1="446" x2="476" y2="482" style="stroke:#2fa84f;stroke-width:4;stroke-dasharray:12 6" marker-end="url(#i71mg)"/>'
               '<line x1="392" y1="494" x2="474" y2="494" style="stroke:#ee5a3c;stroke-width:4;stroke-dasharray:14 6" marker-end="url(#i71mr)"/>'
               '<line x1="402" y1="544" x2="478" y2="518" style="stroke:#1ea0f0;stroke-width:4" marker-end="url(#i71mb)"/>'
               '<line x1="518" y1="458" x2="552" y2="342" style="stroke:#33516e;stroke-width:2.5;stroke-dasharray:7 5" marker-end="url(#i71mk)"/>'
               '<line x1="884" y1="338" x2="884" y2="392" style="stroke:#33516e;stroke-width:2.5;stroke-dasharray:7 5" marker-end="url(#i71mk)"/>')
    out.append('</svg>')
    for n, (x, y) in P.items():
        out.append(img("i71a_rt.png", "left:%dpx;top:%dpx;width:78px" % (x - 39, y - 27)))
        out.append('<div class="i71-n" style="left:%dpx;top:%dpx">%s</div>' % (x - 40, y + 32, n))
    return "".join(out)


def card(x, w, ic, bgc, bc, col, head, sub):
    return ('<div class="i71-c" style="left:%dpx;width:%dpx;background:%s;border-color:%s"></div>' % (x, w, bgc, bc) +
            img(ic, "left:%dpx;top:660px;width:86px" % (x + 28)) +
            '<div class="i71-ch" style="left:%dpx;top:660px;color:%s">%s</div>' % (x + 142, col, head) +
            '<div class="i71-cs" style="left:%dpx;top:694px;color:%s">%s</div>' % (x + 142, col, sub))


HTML = CSS + bg("bgk_28") + "".join([
    '<div class="step">',
    '<div class="i71-p" style="left:232px;top:160px;width:1206px;height:58px;border-radius:16px"></div>',
    '<div class="i71-t" style="left:232px;top:172px;width:1206px;text-align:center;font:800 28px/1.2 Golos Text,sans-serif;color:#13306e">'
    'SR позволяет задать разные пути для данных, видео и голоса</div>',
    '</div>',
    '<div class="step">',
    '<div class="i71-p" style="left:232px;top:230px;width:1206px;height:536px"></div>',
    '<div style="position:absolute;left:402px;top:246px;width:934px;height:88px;background:#cfeee8;border:2px solid #b9d9d2;border-radius:14px"></div>',
    img("i71a_srv.png", "left:423px;top:253px;width:89px"),
    '<div class="i71-n" style="left:524px;top:276px;width:250px;text-align:left;font-size:27px;white-space:nowrap">Контроллер / PCE</div>',
    '<div class="i71-mini" style="left:772px;width:180px"></div>', img("i71a_s1.png", "left:783px;top:270px;width:41px"),
    '<div class="i71-ms" style="left:832px;top:272px">Получает<br>состояние сети</div>',
    '<div class="i71-mini" style="left:964px;width:150px"></div>', img("i71a_s2.png", "left:973px;top:270px;width:44px"),
    '<div class="i71-ms" style="left:1024px;top:272px">Вычисляет<br>пути</div>',
    '<div class="i71-mini" style="left:1128px;width:196px"></div>', img("i71a_s3.png", "left:1138px;top:270px;width:44px"),
    '<div class="i71-ms" style="left:1190px;top:272px">Передаёт SR Policy<br>входному узлу</div>',
    '<div class="i71-t" style="left:576px;top:348px;font-size:18px;line-height:1.25;color:#13306e">Топология<br>и телеметрия</div>',
    '<div class="i71-t" style="left:908px;top:354px;font-size:18px;color:#13306e">PCEP / NETCONF</div>',
    '</div>',
    '<div class="step">',
    network(),
    '<div class="i71-tag" style="left:258px;top:426px;background:#2fa84f">Загрузка данных</div>',
    '<div class="i71-tag" style="left:258px;top:476px;background:#ee5a3c;width:132px">Видео</div>',
    '<div class="i71-tag" style="left:258px;top:527px;background:#1ea0f0;width:142px">Голос</div>',
    '</div>',
    '<div class="step">',
    '<div style="position:absolute;left:380px;top:630px;width:914px;height:2px;background:#1d3f8a"></div>',
    '<div class="i71-t" style="left:614px;top:618px;padding:0 14px;background:#fdf8ea;font-weight:800;color:#13306e">Упрощённый пример требований услуг</div>',
    card(258, 384, "i71a_db.png", "#e3f3e2", "#4caf50", "#1f7a2f", "Данные", "высокая доступная<br>полоса"),
    card(658, 354, "i71a_vid.png", "#fde0d6", "#ee6a4c", "#c8321b", "Видео", "малая задержка"),
    card(1030, 384, "i71a_tel.png", "#dff0fd", "#3a9be6", "#185a9e", "Голос", "низкие потери,<br>задержка и джиттер"),
    '</div>',
    '<div class="step">',
    '<div class="i71-p" style="left:286px;top:784px;width:1212px;height:128px;border-radius:16px"></div>',
    img("i71a_gear.png", "left:323px;top:798px;width:64px"),
    '<div class="i71-t" style="left:416px;top:800px;font-weight:700;color:#13306e;line-height:1.55">'
    'Контроллер управляет SR-политиками устройств и может пересчитывать пути при изменениях сети.<br>'
    'Входной узел классифицирует трафик и направляет его в соответствующую политику.</div>',
    '<div class="i71-t" style="left:416px;top:870px;font-size:17px;color:#1d4f8a">Выбор пути учитывает требования услуги; гарантии качества требуют ресурсов и настройки QoS.</div>',
    '</div>',
])
