# -*- coding: utf-8 -*-
"""pptx: как работают LDP и RSVP-TE — вёрстка поверх bgk_12."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _mp_replib import bg, img

W, H, TOP = 1672, 941, 122

CSS = """<style>
.i47-p{position:absolute;background:#fdf8ea;border:3px solid #1f63c6;border-radius:22px;box-shadow:0 5px 0 rgba(21,80,168,.25)}
.i47-hd{position:absolute;height:50px;border-radius:12px;font:900 32px/50px "Rubik",sans-serif;color:#13306e;text-align:center}
.i47-hd small{font-size:26px}
.i47-t{position:absolute;font:500 18px/1.25 "Golos Text",sans-serif;color:#1d2a44}
.i47-num{position:absolute;width:30px;height:30px;border-radius:50%;color:#fff;font:900 18px/30px "Golos Text",sans-serif;text-align:center}
.i47-n{position:absolute;font:900 20px/1 "Golos Text",sans-serif;color:#13306e;text-align:center;width:50px}
.i47-call{position:absolute;border-radius:12px;font:700 18px/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center;padding:6px 10px}
.i47-tb{position:absolute;border-collapse:collapse;font:500 18px/36px "Golos Text";white-space:nowrap,sans-serif;color:#1d2a44;text-align:left}
.i47-tb td{border-bottom:1px solid #c9c2ad;padding:0 16px}.i47-tb td:first-child{font-weight:700;color:#13306e}
.i47-tb th{font:900 26px/44px "Rubik",sans-serif;color:#13306e;text-align:center}
.i47-dash{stroke-dasharray:14 10;animation:i47d 1.2s linear infinite}
@keyframes i47d{to{stroke-dashoffset:-24}}
</style>"""

NUM = '<div class="i47-num" style="left:%dpx;top:%dpx;background:%s">%d</div>'


def items(x, col, rows):
    out = []
    for i, (y, t) in enumerate(rows):
        out.append(NUM % (x, y, col, i + 1))
        out.append('<div class="i47-t" style="left:%dpx;top:%dpx;width:560px;white-space:nowrap">%s</div>' % (x + 56, y + 2, t))
    return "".join(out)


def net(ox, col, top_or_bot):
    """Схема R1–R4: ox — сдвиг; выделенный путь через R2 (top) или R3 (bot)."""
    pts = {"R1": (378, 464), "R2": (528, 410), "R3": (528, 514), "R4": (678, 464)}
    hi = ["R1", "R2" if top_or_bot == "top" else "R3", "R4"]
    lo = ["R1", "R3" if top_or_bot == "top" else "R2", "R4"]
    svg = ['<svg style="position:absolute;left:0;top:0" width="1672" height="941">',
           '<defs><marker id="i47m%s" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto">'
           '<path d="M0,0 L16,8 L0,16z" style="fill:%s"/></marker>' % (top_or_bot, col),
           '<marker id="i47g%s" markerUnits="userSpaceOnUse" markerWidth="16" markerHeight="16" refX="12" refY="8" orient="auto">'
           '<path d="M0,0 L16,8 L0,16z" style="fill:#555c6e"/></marker></defs>' % top_or_bot]
    for a, b in zip(lo, lo[1:]):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:#555c6e;stroke-width:2.5" marker-end="url(#i47g%s)"/>'
                   % (x1 + ox + 34, y1 + (8 if y2 > y1 else -8), x2 + ox - 38, y2 + (-6 if y2 > y1 else 6), top_or_bot))
    for a, b in zip(hi, hi[1:]):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        svg.append('<line x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s;stroke-width:12;opacity:.3"/>'
                   % (x1 + ox + 34, y1, x2 + ox - 38, y2, col))
        svg.append('<line class="i47-dash" x1="%d" y1="%d" x2="%d" y2="%d" style="stroke:%s;stroke-width:5" marker-end="url(#i47m%s)"/>'
                   % (x1 + ox + 34, y1, x2 + ox - 38, y2, col, top_or_bot))
    svg.append('</svg>')
    out = ["".join(svg)]
    for n, (x, y) in pts.items():
        out.append(img("i45a_rt.png", "left:%dpx;top:%dpx;width:76px" % (x + ox - 38, y - 30)))
        if n in ("R1", "R4"):
            out.append('<div class="i47-n" style="left:%dpx;top:%dpx">%s</div>' % (x + ox + (-85 if n == "R1" else 37), y - 10, n))
        else:
            out.append('<div class="i47-n" style="left:%dpx;top:%dpx">%s</div>' % (x + ox - 25, y + (-50 if n == "R2" else 36), n))
    return "".join(out)


ROWS = [("Выбор пути", "Обычно следует IP-маршрутам IGP", "Путь задан или рассчитан с ограничениями TE"),
        ("Обмен", "Привязки FEC ↔ метка между соседями", "Path → к выходу; Resv → ко входу"),
        ("Ресурсы", "Не резервирует полосу сам по себе", "Может резервировать запрошенную полосу"),
        ("Состояние на узлах", "Для FEC и привязок меток", "Для конкретного TE-LSP"),
        ("Типичная задача", "Базовый MPLS-транспорт", "Управление путями и распределением трафика")]

HTML = CSS + bg("bgk_12") + "".join([
    '<div class="step">',
    '<div class="i47-p" style="left:218px;top:130px;width:618px;height:456px"></div>',
    '<div class="i47-hd" style="left:234px;top:140px;width:588px;background:#bfe9d6">LDP <small>— метки вдоль IP-маршрута</small></div>',
    items(252, "#1f9a64", [(202, "Маршрутизация определяет следующий хоп к FEC."),
                          (242, "Соседи обмениваются привязками FEC → метка:<br>Label Mapping; при DoD — после Label Request."),
                          (304, "LSR связывает входную метку с выходной меткой<br>и следующим хопом.")]),
    net(0, "#2fbf6a", "top"),
    '<div class="i47-call" style="left:588px;top:356px;width:212px;background:#c4ead6">Обычно по лучшему<br>пути IGP</div>',
    '</div>',
    '<div class="step">',
    '<div class="i47-p" style="left:840px;top:130px;width:614px;height:456px"></div>',
    '<div class="i47-hd" style="left:856px;top:140px;width:584px;background:#f9b5a6">RSVP-TE <small>— сигнализация TE-туннеля</small></div>',
    items(868, "#f2694a", [(202, "Входной узел получает заданный путь или рассчитывает<br>его с учётом ограничений."),
                          (260, "Path проходит от входа к выходу по выбранному пути."),
                          (302, "Resv идёт обратно: передаёт метки и подтверждает<br>резервирование при наличии ресурсов.")]),
    net(616, "#e2342b", "bot"),
    '<div class="i47-call" style="left:1206px;top:524px;width:220px;white-space:nowrap;font-size:17px;background:#f9b5a6;font-weight:500">Может отличаться от<br>'
    'кратчайшего пути <b>IGP</b></div>',
    '</div>',
    '<div class="step">',
    '<div class="i47-p" style="left:350px;top:596px;width:1030px;height:250px"></div>',
    '<div style="position:absolute;left:366px;top:606px;width:196px;height:40px;background:#cfe3f3;border-radius:10px"></div>',
    '<div style="position:absolute;left:566px;top:606px;width:374px;height:40px;background:#bfe9d6;border-radius:10px"></div>',
    '<div style="position:absolute;left:944px;top:606px;width:422px;height:40px;background:#f9b5a6;border-radius:10px"></div>',
    '<table class="i47-tb" style="left:366px;top:604px;width:1000px"><colgroup><col style="width:200px"><col style="width:378px">'
    '<col></colgroup><tr><th>Критерий</th><th>LDP</th><th>RSVP-TE</th></tr>' +
    "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in ROWS) + '</table>',
    '</div>',
    '<div class="step">',
    '<div class="i47-t" style="left:358px;top:848px;width:1012px;height:48px;background:#f9e48a;border:2px solid #1f63c6;border-radius:24px;'
    'text-align:center;font:700 18px/44px Golos Text;white-space:nowrap;padding-left:40px;box-sizing:border-box,sans-serif;color:#13306e">RSVP-TE сигнализирует путь, а не рассчитывает его сам. '
    'Резервирование полосы не заменяет QoS.</div>',
    img("i47a_bulb.png", "left:382px;top:852px;width:38px"),
    '</div>',
])
