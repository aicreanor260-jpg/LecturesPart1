# -*- coding: utf-8 -*-
"""MPLS 2.9 v2 — pptx 62–71: отказоустойчивость путей, иерархия меток (FRR), проблемы пересылки, сегментная
маршрутизация SR. Текст pptx дословно (из _mp_s3.py), разнесён по смыслу; заголовки блоков и подписи — из инфографик
i62a…i71a; рисунки pptx — сцены prot_all / frr_scene / sr_net / sr_scene / ctrl / svc_paths."""
from _mp2_kit import slide, step, panel, row, node, arrow, ico
from _mp_fig import router, link, box, t, path, svg, BLUE, ORG, GRN, RED, GRY, INK
from _mp_s3 import prot_all, frr_scene, sr_net, sr_scene, ctrl, svc_paths

CSS = r"""
.s9fit svg.mpfig{max-height:var(--h,40vh);width:auto;max-width:100%;margin:0 auto}
.s9fit .scene .figwrap{padding:4px}
.s9w2>*:last-child{flex:1.7 1 0}
.s9w1>*:first-child{flex:1.9 1 0}
.s9li span{font-weight:500!important}
.s9g{display:grid;gap:clamp(8px,1vw,18px)}
.s9ic{display:flex;justify-content:space-around;align-items:flex-end;gap:10px;height:100%}
.s9stk{display:inline-flex;flex-direction:column;border:3px solid #1d3f8a;border-radius:6px;overflow:hidden;min-width:3.6em;
 font:800 clamp(15px,1.3vw,25px)/1.35 "Golos Text",sans-serif;color:#13306e;text-align:center;flex:none;background:#fdf0cf}
.s9stk b{border-top:2px solid #1d3f8a}.s9stk b:first-child{border-top:0}
.s9stk .g{background:#5fd39c}.s9stk .r{background:#f2694a}.s9stk .y{background:#fdf0cf}.s9stk .gg{background:#a8e6c0}
.s9card{display:flex;align-items:center;gap:12px;background:#d3f1e8;border:2px solid #bfe3d6;border-radius:16px;padding:10px 14px;height:100%;box-sizing:border-box}
.s9card h4{margin:0 0 4px;font:900 clamp(20px,1.8vw,34px)/1 "Rubik",sans-serif;color:#13306e}
.s9card p{margin:0;font:600 clamp(14px,1.2vw,23px)/1.3 "Golos Text",sans-serif;color:#1d2a44}
.s9card>div:first-child{flex:1}
.s9cards{display:flex;align-items:stretch;gap:8px}
.s9cards>.step{flex:1 1 0;min-width:0}
.s9cards>.m2ar{align-self:center;margin:0}
.s9sl{display:inline-flex;border:3px solid #1d3f8a;border-radius:6px;overflow:hidden;font:800 clamp(15px,1.3vw,25px)/1.9 "Golos Text",sans-serif;color:#13306e}
.s9sl b{padding:0 .8em;border-left:2px solid #1d3f8a}.s9sl b:first-child{border-left:0}
.s9sl .o{background:#f2876a}.s9sl .g{background:#a8e6c0}.s9sl .b{background:#9fd0f5}.s9sl .w{background:#fff;min-width:5em}
.s9sl .p{background:#d9d4f2}.s9sl .m{background:#e9b8e3}
.s9cloud{display:inline-grid;place-items:center;background:#bfeee0;border:3px solid #7cc9b2;border-radius:40px;padding:6px 18px;
 font:800 clamp(14px,1.2vw,23px)/1.15 "Golos Text",sans-serif;color:#13306e;text-align:center}
.s9li{display:flex;align-items:center;gap:10px;margin:0 0 6px}
.s9li .ico{flex:none}
.s9li span{font:600 clamp(14px,1.15vw,22px)/1.3 "Golos Text",sans-serif}
.s9req{display:flex;flex-direction:column;gap:6px;align-items:stretch}
.s9req span{display:flex;align-items:center;gap:8px;border-radius:10px;padding:2px 12px;font:700 clamp(13px,1.1vw,21px)/1.7 "Golos Text",sans-serif;color:#13306e}
.s9goal{display:flex;align-items:center;gap:16px;background:#1f63c6;border:3px solid #fff;border-radius:18px;padding:8px 20px;
 font:800 clamp(17px,1.6vw,31px)/1.25 "Golos Text",sans-serif;color:#fff;box-shadow:0 6px 0 rgba(21,80,168,.3)}
.s9svc{display:flex;align-items:center;gap:12px;border-radius:16px;padding:8px 14px;border:2px solid}
.s9svc strong{display:block;font:900 clamp(17px,1.5vw,29px)/1.1 "Rubik",sans-serif}
.s9svc span{font:600 clamp(14px,1.15vw,22px)/1.25 "Golos Text",sans-serif}
"""

TO = "Отказоустойчивость путей <em>MPLS</em>"
TH = "Использование иерархии меток для <em>быстрой защиты</em>"
TS = "Реализация пересылки <em>SR</em>"
TD = "Режимы развертывания <em>SR</em>"


def fit(html, h="40vh", cls=""):
    return '<div class="s9fit %s" style="--h:%s">%s</div>' % (cls, h, html)


def fig(body, vb, h="40vh"):
    return fit('<div class="figwrap mppanel">%s</div>' % svg(body, vb), h)


def g(body):
    """Группа SVG, появляющаяся шагом слайда вместе с текстом."""
    return '<g class="step">%s</g>' % body


def stk(cells):
    """Стек меток (вершина сверху): [(класс, текст)]."""
    return '<span class="s9stk">%s</span>' % "".join('<b class="%s">%s</b>' % c for c in cells)


def li(icon, text, h=40):
    return '<div class="s9li">%s<span>%s</span></div>' % (ico(icon, h), text)


def pill(x, y, w, s, fill="#c9eedc", col=INK, size=14):
    return box(x, y, w, 34, s, fill, col, size, stroke=fill, rx=10)


# ---------------------------------------------------------------- схемы
def ldp_fig():
    """Базовый механизм: сходимость IGP (инфографика i62a)."""
    b = ['<rect x="30" y="15" width="170" height="140" rx="18" style="fill:#d3f1e8"/>',
         '<rect x="800" y="15" width="170" height="140" rx="18" style="fill:#d3f1e8"/>',
         link(160, 60, 440, 55, GRY, 4, arrow=True), link(560, 55, 840, 60, GRY, 4, arrow=True)]
    b.append(router(115, 70, "LER1") + router(500, 55, "LSR1") + router(885, 70, "LER2"))
    b.append(router(330, 215, "LSR2") + router(670, 215, "LSR3"))
    b.append(g(t(700, 30, "Отказ линии", 15, RED, 900) + t(700, 72, "✕", 34, RED, 900)))
    b.append(g(path("M140 100 C 220 200, 240 205, 290 210", GRN, 5) + path("M375 215 L620 215", GRN, 5) +
               path("M715 210 C 780 200, 800 160, 860 105", GRN, 5) + t(500, 180, "Новый путь", 14, GRN, 900) +
               t(500, 205, "после сходимости", 14, GRN, 900)))
    return svg("".join(b), "0 0 1000 285")


def mini_line():
    """2. Защита линии — FRR."""
    b = [link(115, 55, 345, 55, GRY, 4, dash=True, arrow=True), t(230, 70, "✕", 30, RED, 900),
         path("M90 85 L190 150", GRN, 5), path("M270 150 L370 85", GRN, 5)]
    b += [router(70, 55, "LSR2"), router(390, 55, "LSR7"), router(230, 150, "LSR3"), pill(160, 215, 140, "B1-LSP1")]
    return svg("".join(b), "0 0 460 255")


def mini_node():
    """3. Защита узла — FRR."""
    b = [link(95, 55, 200, 55, GRY, 4, dash=True), link(260, 55, 365, 55, GRY, 4, dash=True),
         path("M80 85 L190 150", GRN, 5), path("M270 150 L380 85", GRN, 5)]
    b += [router(60, 55, "LSR2"), router(230, 55, "LSR7", col=RED), t(230, 64, "✕", 30, "#fff", 900),
          router(400, 55, "LSR8"), router(230, 150, ""), pill(160, 185, 140, "B2-LSP1")]
    return svg("".join(b), "0 0 460 225")


def mini_path():
    """4. Защита всего пути."""
    b = [path("M80 115 Q120 40 190 40", BLUE, 4), path("M330 40 Q380 40 410 105", BLUE, 4),
         pill(170, 22, 180, "Основной LSP1", "#cfe6fb"),
         path("M95 175 L150 200", GRN, 4), path("M360 200 L405 175", GRN, 4),
         pill(150, 183, 220, "Резервный B3-LSP1")]
    b += [router(70, 140, "LSR1"), router(440, 140, "LSR8")]
    return svg("".join(b), "0 0 510 235")


def frr64():
    """Схема работы (инфографика i64a): основной LSP1 15/17/21, обход B-LSP1 7/8 через LSR3."""
    b = [link(125, 160, 385, 160, INK, 4), link(835, 160, 1075, 160, INK, 4), t(255, 145, "15", 18, INK, 900),
         t(955, 145, "21", 18, INK, 900), link(455, 160, 765, 160, RED, 4, dash=True), t(610, 200, "17", 18, INK, 900)]
    b.append(router(90, 160, "LSR1") + router(420, 160, "LSR2") + router(800, 160, "LSR7") + router(1110, 160, "LSR8"))
    b.append(g(t(610, 172, "✕", 30, RED, 900) + t(610, 232, "Отказ линии", 15, RED, 900)))
    b.append(g(link(445, 135, 575, 75, GRN, 6, dash=True) + link(645, 75, 775, 135, GRN, 6, dash=True) +
               t(490, 90, "7", 18, INK, 900) + t(730, 90, "8", 18, INK, 900) + router(610, 70, "LSR3", lab_up=True) +
               pill(545, 100, 130, "B-LSP1") + pill(330, 240, 180, "Начало обхода", "#ffd25a") +
               pill(710, 240, 180, "Возврат в LSP1", "#ffd25a")))
    return svg("".join(b), "45 5 1110 275")


def vstk(x, y, cells, w=66):
    """Стек меток в SVG (вершина сверху)."""
    cols = {"r": "#f2694a", "g": "#a8e6c0", "y": "#fdf0cf"}
    out = []
    for i, (c, s) in enumerate(cells):
        out.append(box(x, y + i * 38, w, 38, s, cols[c], INK, 15, rx=3))
    return "".join(out)


def frr65():
    """Иерархия меток с PHP (инфографика i65a)."""
    b = ['<path d="M440 40 V25 H780 V40" style="fill:none;stroke:#13306e;stroke-width:3"/>', t(610, 18, "B-LSP1", 16, INK, 900),
         link(135, 250, 375, 250, "#1d5f7a", 4, arrow=True), link(860, 250, 1065, 250, "#1d5f7a", 4, arrow=True),
         link(470, 250, 760, 250, GRY, 4, dash=True, arrow=True), t(610, 262, "✕", 34, RED, 900),
         t(610, 305, "Линия недоступна", 15, RED, 900), box(205, 230, 90, 40, "15", "#fdf0cf", INK, 16),
         box(915, 230, 90, 40, "21", "#fdf0cf", INK, 16)]
    b.append(router(100, 250, "LSR1") + router(420, 250, "LSR2") + router(810, 250, "LSR7") + router(1110, 250, "LSR8"))
    b.append(router(610, 85, "LSR3"))
    b.append(g(path("M440 215 L565 110", GRN, 6) + vstk(380, 50, [("r", "7"), ("g", "17"), ("y", "IP")]) +
               t(300, 95, "Вершина стека: 7", 13, INK, 800)))
    b.append(g(path("M655 110 L790 215", GRN, 6) + vstk(790, 75, [("g", "17"), ("y", "IP")]) +
               t(940, 95, "После PHP: 17", 13, INK, 800)))
    return svg("".join(b), "0 0 1200 320")


# ---------------------------------------------------------------- слайды
def s62():
    slide("pptx 62 · Общая характеристика", "bgk_13", TO, "".join([
        row(step(panel("Цель", '<div class="m2b">MPLS поддерживает несколько механизмов обеспечения отказоустойчивости, или '
                       "в терминах SDH — механизмов автоматического защитного переключения маршрута в случае отказа "
                       "какого-либо элемента сети: <b>интерфейса LSR, линии связи или LSR в целом</b>.</div>", num="1")),
            step(panel("", '<div class="s9ic">%s%s%s</div>' % (node(ico("i62a_if.png", 62), "Интерфейс"),
                                                               node(ico("i62a_ln.png", 62), "Линия связи"),
                                                               node(ico("i62a_nd.png", 62), "Узел LSR")))),
            cls="s9w1"),
        panel("Базовый механизм: сходимость IGP", row(
            step('<div class="m2b">В том случае, когда путь устанавливается с помощью протокола <b>LDP</b>, существует '
                 "единственная возможность защиты пути — его восстановление с помощью распределенного механизма нахождения "
                 "нового пути средствами протоколов маршрутизации. Это абсолютно тот же механизм, который используется в "
                 "IP-сетях при отказе линии или маршрутизатора.</div>"),
            '<div style="flex:1.5">%s</div>' % fit(ldp_fig(), "23vh")), "tint", num="2"),
        row(step(panel("От чего зависит время восстановления",
                       '<div class="m2big">Время восстановления пути зависит от применяемого <b>протокола маршрутизации</b> '
                       "и <b>сложности топологии сети</b>, обычно это <b>десятки секунд или несколько минут</b>.</div>",
                       "or", num="3")),
            step('<div class="m2note" style="height:100%;box-sizing:border-box;display:grid;place-items:center">'
                 '<span><b>Восстановление:</b> путь рассчитывается после отказа.</span></div>')),
    ]), safe="sr")


def s63():
    intro = ("В том случае, когда путь является <b>TE-туннелем</b>, в технологии MPLS разработано несколько механизмов его "
             "восстановления. Эти механизмы иллюстрирует схема, на которой показан основной путь <b>LSP1</b>, соединяющий "
             "устройства <b>LSR1</b> и <b>LSR8</b>. Будем считать, что путь LSP1 является TE-туннелем.")
    slide("pptx 63 · Четыре механизма", "bgk_28", TO, "".join([
        step(panel("Четыре механизма восстановления TE-туннеля", '<div class="m2big">%s</div>' % intro)),
        fit('<div class="figwrap mppanel">%s</div>' % prot_all(), "53vh"),
    ]), sub="")
    m1 = ('<div class="m2chain" style="align-items:center;justify-content:center;gap:10px;margin-bottom:6px">%s%s%s%s%s</div>'
          % (node(ico("i63a_rt.png", 50), "LSR1"), arrow(), '<span class="s9cloud">Новый<br>маршрут</span>', arrow(),
             node(ico("i63a_rt.png", 50), "LSR8")))
    slide("pptx 63 · Восстановление и защита линии", "bgk_28", TO, row(
        step(panel("Восстановление от входного узла", m1 +
                   "<p><b>Восстановление пути его начальным узлом.</b> Традиционное (с помощью протокола маршрутизации) "
                   "повторное нахождение нового пути, обходящего отказавший элемент сети. Отличие от восстановления пути LDP "
                   "заключается только в том, что прокладкой нового пути занимается лишь один узел сети, а именно начальный "
                   "узел пути. В нашем примере это узел LSR1.</p>", num="1")),
        step(panel('Защита линии <span class="m2pill gr">FRR</span>', fit(mini_line(), "17vh") +
                   "<p><b>Защита линии.</b> Такая защита организуется между двумя устройствами LSR, непосредственно "
                   "соединенными линией связи. Обходной маршрут находится заранее, до отказа линии, и заранее прокладывается "
                   "между этими устройствами таким образом, чтобы обойти линию связи в случае ее отказа. В нашем примере такой "
                   "вариант защиты установлен для линии, соединяющей узлы LSR2 и LSR7. Обходной путь <b>B1-LSP1</b> проложен "
                   "через узел LSR3. Защита линии является временной мерой, так как параллельно с началом использования "
                   "обходного пути начальный узел основного пути начинает процедуру его восстановления с помощью протокола "
                   "маршрутизации. После восстановления основного пути использование обходного пути прекращается. Временная "
                   "защита линии не гарантирует TE-туннелю требуемой пропускной способности. Механизм защиты линии работает "
                   "очень быстро, обычно время переключения не превосходит <b>50 мс</b>, то есть сравнимо со временем "
                   "переключения сетей SDH, которые всегда выступают в этой области в качестве эталона. Поэтому механизм "
                   "защиты линии называют <b>быстрой перемаршрутизацией (fast re-route)</b>.</p>", "or", num="2")),
        cls="s9w2"), safe="sr")
    slide("pptx 63 · Защита узла и пути", "bgk_28", TO, "".join([
        row(step(panel('Защита узла <span class="m2pill gr">FRR</span>', fit(mini_node(), "20vh") +
                       "<p><b>Защита узла.</b> Этот механизм очень похож на механизм защиты линии, но отличается тем, что "
                       "обходной путь прокладывается так, чтобы обойти отказавшее устройство LSR (в нашем примере на рисунке "
                       "это устройство <b>LSR7</b>). Все остальные характеристики аналогичны характеристикам защиты линии; "
                       "механизм защиты узла тоже относится к механизмам быстрой перемаршрутизации и тоже является временной "
                       "мерой.</p>", "rd", num="3")),
            step(panel("Защита всего пути", fit(mini_path(), "20vh") +
                       "<p><b>Защита пути.</b> В дополнение к основному пути в сети прокладывается путь, связывающий те же "
                       "конечные устройства, но проходящий по возможности через устройства LSR и линии связи, не встречающиеся "
                       "в основном пути (на рисунке это резервный путь <b>B3-LSP1</b>). Данный механизм самый универсальный, "
                       "но он работает медленнее, чем механизмы защиты линии и узла.</p>", "gr", num="4"))),
        step(panel("", row(li("i63a_gear.png", "<b>Обнаружение:</b> Для быстрого обнаружения отказа основного пути или его "
                                               "части могут использоваться различные механизмы и протоколы: сообщения Hello "
                                               "протокола RSVP, протокол LSP Ping или BFD.", 54),
                           li("i63a_sw.png", "<b>FRR:</b> локальное переключение с целевым временем порядка 50 мс; затем "
                                             "возможна переоптимизация.", 54)), "tint")),
    ]), safe="sr")


def s64():
    slide("pptx 64 · Обходной путь B-LSP1", "bgk_12", TH, "".join([
        row(step(panel("", '<div class="m2b" style="font-size:clamp(15px,1.3vw,25px)">Рассмотрим работу быстрых механизмов защиты на примере защиты линии. Пусть '
                       "для защиты линии <b>LSR2-LSR7</b> в сети проложен обходной путь <b>B-LSP1</b>. На основном пути LSP1 "
                       "для продвижения кадров используется последовательность меток <b>15,17 и 21</b>. На первом участке "
                       "обходного пути B-LSP1 используется метка <b>7</b>, на втором — метка <b>8</b>.</div>")),
            step(panel("", li("i64a_sh.png", "<b>Быстрая защита:</b> LSR2 переключает трафик локально, не дожидаясь полного "
                                             "пересчёта маршрутов.", 48), "or")), cls="s9w1"),
        panel("Схема работы", fit(frr64(), "21vh"), "tint"),
        panel("Как меняется стек меток", '<div class="s9cards">%s%s%s%s%s</div>' % (
            step('<div class="s9card"><div><h4>LSR2</h4><p>Swap 15 → 17,<br>затем Push 7</p></div>%s</div>'
                 % stk([("g", "7"), ("r", "17"), ("y", "IP")])), arrow(),
            step('<div class="s9card"><div><h4>LSR3</h4><p>Swap внешней<br>метки 7 → 8</p></div>%s</div>'
                 % stk([("g", "8"), ("r", "17"), ("y", "IP")])), arrow(),
            step('<div class="s9card"><div><h4>LSR7</h4><p>Pop 8, затем<br>Swap 17 → 21</p></div>%s</div>'
                 % stk([("r", "21"), ("y", "IP")]))) +
              step('<div class="m2cap" style="margin-top:8px">Вершина стека — сверху. В этом примере внешняя метка снимается '
                   'на LSR7. <span style="color:#d9363e">Внутренняя метка 17 на всём обходе неизменна.</span></div>')),
    ]), safe="sr")


def s65():
    slide("pptx 65 · Почему нужна иерархия", "bgk_04", TH, row(
        '<div style="display:flex;flex-direction:column;gap:clamp(8px,1vw,18px);flex:1">%s%s</div>' % (
            step(panel("Если просто заменить 15 на 7",
                       "<p>При отказе линии LSR2-LSR7 устройство LSR2 начинает направлять кадры, поступающие по пути LSP1, в "
                       "обходной путь B-LSP1. Однако если при этом поменять метку <b>15</b> на метку <b>7</b>, как того требует "
                       "обычная логика коммутации меток, то кадр придёт в устройство LSR7 с меткой <b>8</b> (ее установит "
                       "устройство LSR3), которая не соответствует значению метки <b>17</b>, используемой в устройстве LSR7 для "
                       "передачи кадров по пути LSP.</p>", "rd", num="1")),
            step(panel("FRR: иерархия меток",
                       '<p>Для того чтобы устройство LSR7 работало при переходе на обходной путь точно так же, как и при '
                       "нормальной работе основного пути, в технике быстрой защиты применяется <b>иерархия меток</b>.</p>"
                       '<div class="m2note">Внешняя метка ведёт по обходу, внутренняя сохраняет основной LSP</div>',
                       "gr", num="2"))),
        '<div style="flex:1.45;display:flex">%s</div>' % fit(frr_scene(), "62vh", "s9sc")), safe="")
    card = lambda n, h, p: ('<div class="m2p" style="height:100%%;box-sizing:border-box"><div class="m2h"><span class="m2n" '
                            'style="background:#2fbf8f">%s</span>%s</div><div class="m2b">%s</div></div>' % (n, h, p))
    slide("pptx 65 · Стек меток на обходе", "bgk_04", TH, "".join([
        panel("", fit(frr65(), "29vh"), "tint"),
        '<div class="s9g" style="grid-template-columns:1fr 1fr 1fr">%s%s%s</div>' % (
            step(card(1, "LSR2: Swap + Push",
                      "<p>Для этого устройство LSR2, которое реализует механизм защиты линии, заменяет метку 15 в пришедшем "
                      "пакете меткой 17, как если бы линия LSR2-LSR7 не отказывала. Затем устройство LSR2 проталкивает метку "
                      "первого уровня в стек, а на вершину стека помещает метку 7, которая нужна для продвижения кадра по "
                      "обходному пути.</p><p><b>Стек: [7, 17].</b></p>")),
            step(card(2, "LSR3: Pop (PHP)",
                      "<p>Устройство LSR3 является предпоследним устройством обходного пути. Поэтому удаляет верхнюю метку 7 "
                      "и выталкивает на вершину стека метку 17.</p>")),
            step(card(3, "LSR7: продолжение LSP1",
                      "<p>В результате кадр поступает в коммутатор LSR7 с меткой 17, что и требуется для продвижения его "
                      "далее по пути LSP1.</p>"))),
        step('<div class="m2note">Аналогичным образом работает механизм быстрой защиты узла, в нем также используется '
             '<b>иерархия меток</b>.</div>'),
    ]), safe="")


def s66():
    def col(num, ic, head, pic, text, verdict, cls, vcol):
        return step(panel(head, '<div class="m2chain" style="justify-content:center;align-items:center;gap:8px;margin-bottom:8px">'
                          '%s</div><p>%s</p><div class="m2note" style="background:%s;border-color:%s">%s</div>'
                          % (pic, text, vcol[0], vcol[1], verdict), cls, num=num))
    rt = lambda: ico("i66a_rt.png", 44)
    stat = ico("i66a_eng.png", 64) + "".join('<div class="m2nd"><span class="m2pill %s">%s</span>%s</div>' % (c, v, rt())
                                             for c, v in (("or", 100), ("or", 200), ("gr", 300)))
    dyn = rt() + ico("i66a_env.png", 30) + rt() + ico("i66a_env.png", 30) + rt()
    te = ('<div class="m2nd">%s<small>LER</small></div><div style="display:flex;flex-direction:column;gap:6px">'
          '<span class="m2pill or">LSP A →</span><span class="m2pill gr">LSP B →</span></div>'
          '<div style="display:flex;flex-direction:column;gap:2px">%s%s</div>' % (rt(), rt(), rt()))
    slide("pptx 66 · Проблемы пересылки", "bgk_11", "Проблемы пересылки <em>MPLS</em>", "".join([
        step(panel("", '<div class="m2big" style="text-align:center">Распределение меток MPLS выполняется <b>статически</b> или '
                   "<b>динамически</b>. Проблемы заключаются в следующем:</div>")),
        '<div class="s9g" style="grid-template-columns:1fr 1fr 1.4fr">%s%s%s</div>' % (col("1", "", "Статическое распределение", stat,
                "Для статического распределения меток требуется ручная настройка. По мере расширения сети сетевые "
                "топологии также изменяются. Статическая конфигурация меток не отвечает требованиям крупных сетей.",
                "Сложно масштабировать", "rd", ("#ffd9cf", "#e2564a")),
            col("2", "", "Динамическое распределение", dyn,
                "Некоторые протоколы динамического распределения меток не могут вычислять пути и для этого используют IGP. "
                "Кроме того, плоскости управления этих протоколов достаточно сложны. При этом требуется, чтобы устройства "
                "отправляли большое количество сообщений для поддержания статуса однорангового узла и пути. В результате "
                "полоса пропускания канала и ресурсы устройства тратятся впустую.",
                "Автоматизация требует ресурсов", "gr", ("#d3f1e8", "#2f9e5b")),
            col("3", "", "Traffic Engineering", te,
                "Более того, несмотря на поддержку TE, некоторые протоколы распределения меток требуют сложной конфигурации "
                "и не поддерживают балансировку нагрузки. Устройства должны отправлять большое количество пакетов протокола, "
                "чтобы поддерживать правильные пути. Кроме того, поскольку устройства не зависят друг от друга и знают только "
                "свой статус, им необходимо обмениваться пакетами сигнализации, что также приводит к потере полосы "
                "пропускания канала и ресурсов устройства.",
                "Больше возможностей — сложнее управление", "or", ("#ffe9a8", "#e0a21a"))),
        step('<div class="s9goal">%s<span>Задача: уменьшить сложность управления, сохранив гибкость и отказоустойчивость.'
             '</span></div>' % ico("i66a_tgt.png", 52)),
    ]), safe="sr")


def s67():
    req = ('<div class="m2p tint" style="padding:8px 12px;flex:none"><div class="m2cap" style="margin-bottom:6px">Требования<br>услуги'
           '</div><div class="s9req"><span style="background:#ffd3cc">%s Задержка</span><span style="background:#cdeedb">%s Полоса'
           '</span><span style="background:#cfe6fb">%s Потери</span></div></div>'
           % (ico("i67a_ic1.png", 26), ico("i67a_ic2.png", 26), ico("i67a_ic3.png", 26)))
    rt = lambda n: node(ico("i67a_rt.png", 46), n)
    lst = '<span class="s9sl"><b class="o">SID 1</b><b class="g">SID 2</b><b class="b">SID 3</b><b class="w">Данные</b></span>'
    scheme = ('<div class="m2chain" style="align-items:center;gap:10px">%s%s%s%s<div style="flex:1">'
              '<div style="text-align:center;margin-bottom:6px">%s</div><div class="m2chain" style="align-items:center">'
              '%s%s%s%s%s%s%s</div></div></div><div class="m2note" style="margin-top:8px;background:#d3f1e8;border-color:#2f9e5b">'
              'Входной узел задаёт список сегментов; сеть выполняет их последовательно.</div>'
              % (step(req), arrow(), step(node(ico("i67a_pc.png", 60), "Расчёт пути", "Топология + телеметрия")), arrow(),
                 step(lst), step(rt("Входной узел")), arrow(), step(rt("Сегмент 1")), arrow(), step(rt("Сегмент 2")),
                 arrow(), step(rt("Выход"))))
    slide("pptx 67 · Сегментная маршрутизация", "bgk_03", "Общая информация о <em>сегментной маршрутизации</em>", "".join([
        step(panel("", '<div class="m2big">Для решения проблем, связанных с IP-передачей и пересылкой MPLS, был предложен метод '
                   "сегментной маршрутизации (<b>SR</b>). SR вносит следующие улучшения:</div>")),
        panel("", scheme, "tint"),
        '<div class="s9g" style="grid-template-columns:1fr 1fr 1.55fr">%s%s%s</div>' % (step(panel("Расширение протоколов", li("i67a_gear.png", "<b>Расширяет существующие протоколы.</b> Расширенные протоколы <b>IGP и BGP</b> могут "
                                                                             "распределять метки, устраняя необходимость в "
                                                                             "других протоколах распределения меток в сетях.", 56),
                       num="1")),
            step(panel("Управление от источника",
                       li("i67a_sign.png", "<b>Представляет механизм маршрутизации от источника.</b> Механизм маршрутизации от источника позволяет <b>контроллерам централизованно "
                                           "вычислять пути</b>.", 56), "gr", num="2")),
            step(panel("Путь под требования услуги",
                       "<p><b>Позволяет услугам определять сети.</b> Услуги управляют сетями. После того, как к услугам предъявляются определённые требования, например, "
                       "требования к задержке, полосе пропускания и скорости потери пакетов, контроллер собирает информацию, "
                       "например, о топологии сети, использовании полосы пропускания и задержке, и вычисляет явные пути на "
                       "основе этих требований.</p>", "or", num="3"))),
    ]), safe="")


def s68():
    legend = ('<div class="m2chain" style="flex-wrap:wrap;gap:10px 18px;justify-content:flex-start;margin-top:8px">'
              '<span><span class="m2pill bl" style="background:#1f63c6;color:#fff">Node SID</span> — направить к узлу по пути IGP</span>'
              '<span><span class="m2pill or" style="background:#e8742c;color:#fff">Adj-SID</span> — пройти конкретную направленную '
              'смежность</span></div>')
    slide("pptx 68 · SID узлов и каналов", "bgk_13", TS, "".join([
        step(panel("", '<div class="m2big">SR разделяет путь на сегменты и назначает этим сегментам идентификаторы '
                   "(<b>SID</b>).</div>")),
        panel("Пример SID в SR-MPLS", fit('<div class="figwrap mppanel">%s</div>' % svg(sr_net(), "0 0 1200 520"), "38vh")
              + step(legend), "tint"),
        step(panel("", '<div class="m2big">SID назначаются узлам пересылки или смежным каналам. В этом примере SID узлов '
                   "пересылки выражены в виде <b>1600X</b>, где X — это идентификатор узла; SID смежных каналов выражены в "
                   "виде <b>160XX</b>, где XX указывает идентификаторы узлов на обоих концах канала.</div>", "or")),
    ]), safe="sr")
    slide("pptx 68 · SR-MPLS и SRv6", "bgk_13", TS, "".join([
        step(panel("", '<div class="m2big">SID используются для идентификации сегментов. <b>Формат SID зависит от способа '
                   "реализации технологий.</b> Например, SID могут быть метками MPLS, индексами в пространстве меток MPLS или "
                   "заголовками пакетов IPv6. SR, использующие метки MPLS, называют <b>SR-MPLS</b>, а использующие IPv6, — "
                   "<b>SRv6</b>.</div>")),
        row(step(panel("SR-MPLS", '<div style="text-align:center;margin:6px 0 12px"><span class="s9sl"><b class="p">IP</b>'
                       '<b class="o">Метка 16023</b><b class="o">Метка 16035</b><b class="g">Метка 16005</b><b class="p">…</b>'
                       '</span></div><div class="m2big"><b>SID реализуются метками MPLS.</b> Последовательность сегментов '
                       "кодируется стеком меток.</div>", "or")),
            step(panel("SRv6", '<div style="text-align:center;margin:6px 0 12px"><span class="s9sl"><b class="p">IPv6</b>'
                       '<b class="m">SRH (список сегментов)</b><b class="p">…</b><b class="w">Полезные данные</b></span></div>'
                       '<div class="m2big"><b>SID — 128-битный идентификатор</b> в формате IPv6-адреса, связанный с '
                       "определённым действием.</div>", "gr"))),
        step('<div class="s9goal" style="justify-content:center">%s<span>Одна идея SR — разные способы кодирования сегментов.'
             '</span></div>' % ico("i68a_bulb.png", 52)),
    ]), safe="sr")


def s69():
    lst = ('<div style="text-align:center"><span class="s9sl"><b class="o">SID 1</b><b class="g">SID 2</b><b class="b">SID 3</b>'
           '<b class="w">Данные</b></span><div class="m2cap" style="text-align:left;margin:4px 0 0 1.5em">↖ Активный сегмент'
           '</div><div class="m2cap" style="margin-top:6px">SR-MPLS: стек меток; SRv6: IPv6 SID</div></div>')
    slide("pptx 69 · Список сегментов", "bgk_07", TS, "".join([
        row(step(panel("Список сегментов", "<p>SID смежных каналов и сетевых узлов, расположенные в определенном порядке, "
                       "формируют <b>список сегментов</b>, который представляет собой путь пересылки. Список сегментов "
                       "кодируется исходным узлом в заголовке пакета данных и передается вместе с пакетом данных. Основа SR - "
                       "это инструкции, объясняющие куда и как отправлять пакеты.</p>", num="1")),
            step(panel("", lst, "tint")), cls="s9r69"),
        fit(sr_scene(), "42vh", "s9sc"),
    ]), safe="sr")
    card = lambda pic, h, p, bgc: ('<div class="m2p" style="background:%s;height:100%%;box-sizing:border-box;text-align:center">'
                                   '<div style="display:flex;justify-content:center;gap:10px;align-items:center">%s</div>'
                                   '<div class="m2h" style="justify-content:center;text-transform:none;margin:6px 0">%s</div>'
                                   '<div class="m2b">%s</div></div>' % (bgc, pic, h, p))
    r = lambda f="i69a_rt.png": ico(f, 58)
    slide("pptx 69 · Обработка активного сегмента", "bgk_07", TS, "".join([
        step(panel("Как обрабатывается активный сегмент", '<div class="m2big">После получения пакета принимающая сторона '
                   "анализирует список сегментов.</div>", "tint", num="2")),
        '<div class="s9g" style="grid-template-columns:1fr 1fr 1fr">%s%s%s</div>' % (
            step(card(r() + '<span class="m2ar" style="margin:0">⇢</span>' + r("i69a_rtf.png"), "Node-SID: цель ещё не достигнута",
                      "Если верхний SID не идентифицирует локальный узел, узел пересылает пакет следующему узлу в режиме "
                      "многопутевой маршрутизации с равной стоимостью (<b>ECMP</b>).", "rgba(211,241,232,.97)")),
            step(card(r("i69a_rtp.png"), "Node-SID: цель достигнута",
                      "Если верхний SID в списке сегментов идентифицирует локальный узел, узел удаляет SID и продолжает "
                      "выполнять следующие процедуры.", "rgba(255,222,210,.97)")),
            step(card(r() + '<span class="m2ar" style="margin:0">→</span>' + r(), "Adjacency-SID",
                      "На узле-владельце выполнить переход по указанной смежности.", "rgba(214,236,251,.97)"))),
        step(panel("Условный пример списка инструкций", '<div class="m2chain" style="align-items:flex-end;gap:8px">%s%s%s%s%s'
                   '</div>' % (
                       node('<span class="s9sl" style="font-size:.85em"><b class="o">16003</b><b class="w">16035, 16005</b></span>'
                            + r(), "R1"), arrow(),
                       node('<span class="s9sl" style="font-size:.85em"><b class="o">16035</b><b class="w">16005</b></span>'
                            + r(), "R3", "16003: достичь R3"),
                       '<span class="m2cap" style="align-self:center">16035: перейти R3 → R5 →</span>',
                       node('<span class="s9sl" style="font-size:.85em"><b class="o">16005</b></span>' + r(), "R5",
                            "16005: достичь R5")))),
    ]), safe="sr")


def s70():
    no = [("i70a_ic1.png", "Устройства обмениваются топологией и SID через IGP"),
          ("i70a_ic2.png", "Входной узел выбирает путь или использует заданную SR Policy"),
          ("i70a_ic3.png", "Настройка выполняется на устройствах")]
    yes = [("i70a_ic4.png", "Собирает топологию и сведения о ресурсах"),
           ("i70a_ic2.png", "Рассчитывает пути с учётом требований услуг"),
           ("i70a_ic3.png", "Передаёт политику входному узлу")]
    side = lambda items: "".join(li(f, s, 34) for f, s in items)
    slide("pptx 70 · С контроллером и без", "bgk_10", TD, "".join([
        step(panel("", '<div class="m2big">Развертывание SR выполняется <b>с контроллером или без контроллера</b>. Если '
                   "используется контроллер, контроллер собирает информацию, резервирует ресурсы пути, вычисляет пути и "
                   "доставляет результаты исходному узлу. <b>Этот режим является предпочтительным.</b></div>")),
        row(step(panel('Без контроллера', row(fig(ctrl(260, 40, "Администратор", False), "0 0 520 385", "31vh"),
                                              '<div style="align-self:center">%s</div>' % side(no)) +
                       '<div class="m2note" style="background:#d3f1e8;border-color:#2f9e5b">Подходит для распределённого '
                       'управления.</div>', "gr")),
            step(panel('С контроллером', row(fig(ctrl(260, 40, "iMaster NCE", True), "0 0 520 385", "31vh"),
                                             '<div style="align-self:center">%s</div>' % side(yes)) +
                       '<div class="m2note">Удобен для централизованной оптимизации и автоматизации.</div>', "rd"))),
        step(panel("Краткий словарь", row('<div class="m2big"><span class="m2pill gr">PCEP</span>: протокол взаимодействия '
                                          "элементов расчета пути</div>",
                                          '<div class="m2big"><span class="m2pill gr">NETCONF</span>: протокол конфигурации '
                                          "сети</div>"), "tint")),
    ]), safe="sl")


def s71():
    svc = lambda f, h, s, c, bgc: step('<div class="s9svc" style="background:%s;border-color:%s">%s<div><strong style="color:%s">'
                                       '%s</strong><span>%s</span></div></div>' % (bgc, c, ico(f, 54), c, h, s))
    slide("pptx 71 · Пути для услуг", "bgk_28", TD, "".join([
        step(panel("Явные пути для разных услуг", '<div class="m2big">SR можно использовать для простого определения пути '
                   "переадресации пакета. В действующей сети могут быть определены разные пути для различных услуг. В этом "
                   "примере для реализации сети, ориентированной на услуги, определены <b>три явных пути</b> для загрузки "
                   "данных, видео и голосовых услуг. Устройства управляют контроллером, который может быстро предоставить пути "
                   "в реальном времени.</div>")),
        fit(svc_paths(), "36vh", "s9sc"),
        '<div class="s9g" style="grid-template-columns:1fr 1fr 1fr">%s%s%s</div>' % (
            svc("i71a_db.png", "Данные", "высокая доступная полоса", "#2f9e5b", "rgba(220,243,226,.97)"),
            svc("i71a_vid.png", "Видео", "малая задержка", "#d9363e", "rgba(255,226,218,.97)"),
            svc("i71a_tel.png", "Голос", "низкие потери, задержка и джиттер", "#1a7fd1", "rgba(214,236,251,.97)")),
    ]), safe="")


def build():
    s62()
    s63()
    s64()
    s65()
    s66()
    s67()
    s68()
    s69()
    s70()
    s71()
