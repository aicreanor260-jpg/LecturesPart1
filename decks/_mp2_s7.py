# -*- coding: utf-8 -*-
"""MPLS 2.9 v2 — pptx 45, 47–55: RSVP-TE и статические записи, сравнение LDP/RSVP-TE, мониторинг LSP, LSP Ping,
трассировка, BFD (pptx 41–44 и 46 пустые). Текст pptx дословно (из _mp_s2/_mp_s3), заголовки блоков и подписи схем —
из инфографик автора i45a, i47a…i55a; схемы — живой вёрсткой по шагам."""
from _mp2_kit import slide, step, panel, row, pk, node, arrow, ico
from _mp_s3 import ping_scene

CSS = r"""
.slide.m2>.m2in.s7hl>h1.m2t,.slide.m2>.m2in.s7hl>.m2sub{padding-left:clamp(90px,9vw,170px)}
.s7net{position:relative;width:100%}
.s7net>svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.s7net>.s7at{position:absolute;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;text-align:center;
 white-space:nowrap}
.s7net>.s7at strong{font:900 clamp(14px,1.2vw,23px)/1.05 "Golos Text",sans-serif;color:#13306e}
.s7net>.s7at small{font:600 clamp(11px,.9vw,17px)/1.15 "Golos Text",sans-serif;color:#33476e}
.s7pill{display:inline-block;padding:2px 14px;border-radius:14px;font:700 clamp(12px,1vw,19px)/1.5 "Golos Text",sans-serif;color:#1d2a44}
.s7ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:.5em}
.s7ol li{display:flex;gap:.6em;align-items:flex-start}
.s7ol li>i{flex:none;display:inline-grid;place-items:center;width:1.55em;height:1.55em;border-radius:50%;color:#fff;font:900 1em/1 "Golos Text",sans-serif;
 font-style:normal;margin-top:.05em}
.s7ol.gr li>i{background:#1f9a64}.s7ol.rd li>i{background:#f2694a}.s7ol.bl li>i{background:#2a7fd8}
.s7st{display:flex;flex-direction:column;gap:2px}
.m2p.or .step+.step{margin-top:.5em}
.s7st>div:first-child{display:flex;align-items:center;gap:10px;font:900 clamp(15px,1.35vw,26px)/1.1 "Golos Text",sans-serif;color:#13306e}
.s7st>div:first-child>i{flex:none;display:inline-grid;place-items:center;width:1.6em;height:1.6em;border-radius:50%;color:#fff;font-style:normal}
.s7lb{display:inline-block;padding:0 .5em;border:2px solid #1d3f8a;border-radius:5px;font:800 clamp(14px,1.2vw,23px)/1.5 "Golos Text",sans-serif;
 background:#f2694a;color:#1d1d1d}
.s7lb.g{background:#c4ecd2;border-color:#2e9a62}.s7lb.r{background:#f9b5a6;border-color:#e2342b}
.s7ln{flex:1 1 0;min-width:18px;height:4px;background:#1b8a77;position:relative;align-self:center}
.s7ln::after{content:"";position:absolute;right:-3px;top:-7px;border:9px solid transparent;border-left:13px solid currentColor;border-right:0}
.s7ln{color:#1b8a77}.s7ln.r{background:#e2342b;color:#e2342b}.s7ln.d{background:repeating-linear-gradient(90deg,#9aa6b8 0 10px,transparent 10px 17px);color:#9aa6b8}
.s7ln.k{background:#13306e;color:#13306e}
.s7lc{display:flex;align-items:center;gap:6px}
.s7lc>.m2nd{flex:none}
.s7flow{display:flex;align-items:center;gap:10px;font:700 clamp(14px,1.2vw,23px)/1.3 "Golos Text",sans-serif}
.s7flow>.s7ln{flex:1 1 0}
.s7nest{border:3px solid #13306e;border-radius:14px;padding:6px 14px 12px;font:800 clamp(16px,1.45vw,28px)/1.3 "Golos Text",sans-serif;color:#13306e}
.s7nest em{font-style:normal;font-weight:900;font-size:1.15em}
.s7nest span{font-weight:600}
.s7q{display:inline-grid;place-items:center;width:1.5em;height:1.5em;border-radius:50%;background:#13633f;color:#fff;font-weight:900;flex:none}
.s7card{display:flex;gap:12px;align-items:flex-start}
.s7card>.ico{flex:none}
.s7task{margin-top:.4em;padding:3px 10px;border-radius:10px;font-weight:600}
.s7tr{display:grid;grid-template-columns:clamp(120px,11vw,200px) 1fr;gap:6px 12px;align-items:center}
.s7tr>.s7tl{background:#c4e8e0;border-radius:12px;text-align:center;font:900 clamp(14px,1.25vw,24px)/2 "Golos Text",sans-serif;color:#13306e}
.s7tr>.s7tz{position:relative;height:clamp(46px,4.3vw,80px);background:rgba(214,236,251,.6);border-radius:12px}
.s7tz>*{position:absolute}
.s7tz .s7a{height:4px;top:38%}
.s7tz .s7a::after{content:"";position:absolute;right:-3px;top:-7px;border:9px solid transparent;border-left:13px solid currentColor;border-right:0}
.s7tz .s7a.l::after{right:auto;left:-3px;border-left:0;border-right:13px solid currentColor}
.s7tz .s7a.rq{background:#1f63c6;color:#1f63c6}.s7tz .s7a.rp{background:#2a9a4a;color:#2a9a4a;top:76%}
.s7tz .s7a.to{background:repeating-linear-gradient(90deg,#ec4a2c 0 10px,transparent 10px 17px);color:#ec4a2c}
.s7tz b{font:800 clamp(12px,1.05vw,20px)/1 "Golos Text",sans-serif;transform:translateX(-50%);white-space:nowrap}
.s7tz .ico{transform:translate(-50%,-50%)}
.s7env{display:inline-block;vertical-align:middle;margin:0 2px}
.s7seq{display:flex;align-items:stretch;gap:10px}
.s7seq>div{flex:1 1 0;display:flex;align-items:center;gap:12px;border-radius:16px;padding:8px 14px;
 font:800 clamp(14px,1.3vw,25px)/1.25 "Golos Text",sans-serif;color:#13306e}
.s7seq>span{align-self:center;font:900 clamp(18px,1.8vw,34px)/1 sans-serif;color:#24577a}
.s7x{color:#e2342b;font:900 clamp(22px,2.2vw,42px)/1 sans-serif}
"""

# ---------------------------------------------------------------- общие кирпичики


def net(nodes, links, h, extra=""):
    """Сеть живой вёрсткой: nodes = [(x%, y%, html)], links = [(x1,y1,x2,y2, цвет, толщина, пунктир)] в %."""
    ln = "".join('<line x1="%g%%" y1="%g%%" x2="%g%%" y2="%g%%" style="stroke:%s;stroke-width:%g;stroke-linecap:round"%s/>'
                 % (a, b, c, d, col, w, ' stroke-dasharray="10 8"' if dash else "") for a, b, c, d, col, w, dash in links)
    at = "".join('<div class="s7at" style="left:%g%%;top:%g%%">%s</div>' % (x, y, html) for x, y, html in nodes)
    return '<div class="s7net" style="height:%s"><svg>%s</svg>%s%s</div>' % (h, ln, at, extra)


def rt(name, sub="", img="i45a_rt.png", h=50):
    s = '<small>%s</small>' % sub if sub else ""
    return ico(img, h) + '<strong>%s</strong>%s' % (name, s)


def ol(items, cls="gr"):
    return '<ol class="s7ol %s">%s</ol>' % (cls, "".join('<li><i>%d</i><span>%s</span></li>' % (i, x)
                                                        for i, x in enumerate(items, 1)))


def stp(n, col, title, text):
    """Шаг из инфографики: номер + заголовок-пилюля, под ним текст pptx."""
    return '<div class="s7st"><div><i style="background:%s">%d</i>%s</div><div class="m2b">%s</div></div>' % (col, n, title, text)


def lb(s, cls=""):
    return '<span class="s7lb %s">%s</span>' % (cls, s)


def ln(cls=""):
    return '<span class="s7ln %s"></span>' % cls


def lsp_chain(rt_img="i52a_rt.png", labs=("105", "177", "210"), cloud="i49a_cloud.png", subs=("Входной LER", "", "", "Выходной LER"),
              lcls=("", "", ""), lncls=("", "", "", "k"), last_img=None, mid_img=None):
    """LSR1 →105→ LSR4 →177→ LSR7 →210→ LSR8 → 105.0.0.0 (рисунок LSP Ping pptx 49–53)."""
    names = ("LSR1", "LSR4", "LSR7", "LSR8")
    imgs = (rt_img, rt_img, mid_img or rt_img, last_img or rt_img)
    out = []
    for i, nm in enumerate(names):
        out.append(node(ico(imgs[i], 46), nm, subs[i]))
        if i < 3:
            out.append(ln(lncls[i]) + lb(labs[i], lcls[i]) + ln(lncls[i]))
        else:
            out.append(ln(lncls[3]))
    out.append(ico(cloud, 66))
    return '<div class="s7lc">%s</div>' % "".join(out)


def bulb(text, img="i47a_bulb.png", bg="#f9e48a"):
    return ('<div class="m2note" style="background:%s;border-color:#1f63c6;display:flex;align-items:center;justify-content:center;gap:12px">'
            '%s<span>%s</span></div>' % (bg, ico(img, 34), text))


def build():
    b45()
    b47()
    b48()
    b49()
    b50()
    b51()
    b52()
    b54()
    b55()


# ---------------------------------------------------------------- pptx 45
def b45():
    T = "Протокол <em>RSVP-TE</em>"
    G, GR = "#2fbf94", "#b9bcc4"
    n45 = net([(8, 40, rt("R1")), (50, 14, rt("R2", img="i45a_rt.png", h=44)), (31, 70, rt("R3", h=44)),
               (69, 70, rt("R5", h=44)), (92, 40, rt("R4"))],
              [(8, 34, 50, 10, GR, 5, 0), (50, 10, 92, 34, GR, 5, 0),
               (8, 34, 31, 64, G, 7, 0), (31, 64, 69, 64, G, 7, 0), (69, 64, 92, 34, G, 7, 0)], "clamp(150px,15vw,270px)",
              )
    pills_top = '<div style="text-align:center"><span class="s7pill" style="background:#dcdfe6">Меньшая метрика • недостаточно свободной полосы</span></div>'
    pills_bot = '<div style="text-align:center"><span class="s7pill" style="background:#bfe9d6">TE-туннель • больше метрика, достаточно ресурсов</span></div>'
    pr = (step('<div class="s7flow" style="color:#1b8a77">%s<b>Path: R1 → R3 → R5 → R4</b>%s</div>' % (ln(), ln()))
          + step('<div class="s7flow" style="color:#e2342b">%s<b>Resv: R4 → R5 → R3 → R1</b>%s</div>'
                 % ('<span class="s7ln r" style="transform:scaleX(-1)"></span>', '<span class="s7ln r" style="transform:scaleX(-1)"></span>')))
    left = panel("RSVP-TE — сигнализация пути с ограничениями",
                 "<p><b>RSVP-TE — расширение RSVP для инжиниринга трафика</b>, то есть для организации передачи по путям с заданными "
                 "ограничениями.</p><p>Например, между R1 и R4 есть два пути:</p>" + pills_top + n45 + pills_bot + pr +
                 "<p>Обычная маршрутизация может выбирать первый путь. Для определённого потока можно создать <b>TE-туннель по "
                 "второму пути</b>.</p>", num="1")
    right = panel("Процесс выглядит так:", "".join([
        step(stp(1, "#20b48c", "Выбрать путь", "Входной маршрутизатор рассчитывает путь с учётом ограничений или использует "
                                               "заданный администратором.")),
        step(stp(2, "#f2694a", "Path — вперёд", "Вдоль пути отправляется сообщение <b>Path</b> с параметрами запроса.")),
        step(stp(3, "#20b48c", "Resv — обратно", "В обратном направлении проходит сообщение <b>Resv</b>: согласуются метки и "
                                                 "резервируются запрошенные ресурсы.")),
        step(stp(4, "#f2694a", "Установить записи", "На LSR устанавливаются записи, обеспечивающие продвижение пакетов по "
                                                    "туннелю.")),
    ]), "or", num="2")
    slide("pptx 45 · RSVP-TE", "bgk_17", T, "".join([
        '<div class="m2row"><div style="flex:1.45 1 0;min-width:0">%s</div><div style="flex:1 1 0;min-width:0">%s</div></div>'
        % (step(left), right),
        step('<div class="m2note" style="background:#c4e8e0;border-color:#1b8a77;display:flex;align-items:center;gap:14px;'
             'text-align:left">%s<span><b>Сведения о ресурсах:</b> OSPF-TE / IS-IS-TE. <b>RSVP-TE сигнализирует выбранный путь и '
             'организует необходимое состояние на устройствах.</b> Для расчёта пути могут использоваться сведения о ресурсах, '
             'распространяемые расширениями OSPF-TE или IS-IS-TE.</span></div>' % ico("i45a_db.png", 40)),
    ]))

    chain = ('<div class="s7lc" style="justify-content:center;gap:10px">%s%s%s%s%s%s%s</div>' % (
        '<span class="m2pk" style="font-size:clamp(17px,1.6vw,30px)"><b>245</b><i>IP</i></span>', ln(),
        node(ico("i45a_rt.png", 70), "R2"),
        '<div style="flex:1.6 1 0;display:flex;flex-direction:column;align-items:stretch;gap:4px;text-align:center">'
        '<b class="m2cap">Swap 245 → 256</b>%s</div>' % ln(),
        '<span class="m2pk" style="font-size:clamp(17px,1.6vw,30px)"><b>256</b><i>IP</i></span>', ln(),
        node(ico("i45a_rt.png", 70), "R3")))
    tbl = ('<table class="m2tbl" style="margin-top:10px;font-size:clamp(15px,1.3vw,25px)"><tr><th>Узел</th><th>Входная метка</th>'
           '<th>Действие</th><th>Следующий узел</th></tr><tr><td>R2</td><td>245</td><td>Заменить на 256</td><td>R3</td></tr></table>')
    slide("pptx 45 · Статические записи", "bgk_17", T, "".join([
        row(step(panel("Статическое формирование таблиц",
                       '<div class="m2big"><p>Записи можно создавать и вручную. Администратор задаёт:</p>'
                       + ol(["входную метку;", "выходной интерфейс и следующий узел;", "действие над меткой."], "bl")
                       + "</div>", num="1")),
            step(panel("Пример: правило на R2",
                       '<div class="m2big">Например, на R2 вручную устанавливается правило: <b>«245 → заменить на 256 → передать к '
                       'R3»</b>. При этом на R3 должна существовать согласованная запись для метки <b>256</b>.</div>', "or",
                       num="2"))),
        step(panel("", chain + tbl, "tint")),
        step('<div class="m2note">Статические записи не требуют <b>динамического распределения меток</b> для этих правил, но при '
             'изменении топологии администратору необходимо <b>самостоятельно поддерживать их согласованность</b>.</div>'),
    ]))


# ---------------------------------------------------------------- pptx 47
def b47():
    T = "Сравнение. Как работает <em>LDP</em> и <em>RSVP-TE</em>"
    SUB = "Оба создают правила MPLS-пересылки, но по-разному определяют LSP"

    def n47(col, top, call, cbg):
        hi = [(12, 50, 50, 16, col, 7, 0), (50, 16, 88, 50, col, 7, 0)] if top else [(12, 50, 50, 84, col, 7, 0), (50, 84, 88, 50, col, 7, 0)]
        lo = [(12, 50, 50, 84, "#7d8aa0", 3, 0), (50, 84, 88, 50, "#7d8aa0", 3, 0)] if top else \
             [(12, 50, 50, 16, "#7d8aa0", 3, 0), (50, 16, 88, 50, "#7d8aa0", 3, 0)]
        cx = '<span class="s7pill" style="position:absolute;right:0;%s;background:%s;text-align:center;line-height:1.25">%s</span>' % (
            "top:0" if top else "bottom:0", cbg, call)
        return net([(12, 50, rt("R1", h=58)), (50, 16, rt("R2", h=58)), (50, 84, rt("R3", h=58)), (88, 50, rt("R4", h=58))],
                   lo + hi, "clamp(220px,20vw,390px)", cx)

    ldp = panel('LDP <span class="m2pill gr">метки вдоль IP-маршрута</span>',
                '<div class="m2big">' + ol(["Маршрутизация определяет следующий хоп к FEC.",
                    "Соседи обмениваются привязками FEC → метка: Label Mapping; при DoD — после Label Request.",
                    "LSR связывает входную метку с выходной меткой и следующим хопом."], "gr") + "</div>"
                + n47("#2fbf6a", True, "Обычно по лучшему<br>пути IGP", "#c4ead6"), "gr", num="1")
    rsvp = panel('RSVP-TE <span class="m2pill or">сигнализация TE-туннеля</span>',
                 '<div class="m2big">' + ol(["Входной узел получает заданный путь или рассчитывает его с учётом ограничений.",
                     "Path проходит от входа к выходу по выбранному пути.",
                     "Resv идёт обратно: передаёт метки и подтверждает резервирование при наличии ресурсов."], "rd") + "</div>"
                 + n47("#e2342b", False, "Может отличаться от<br>кратчайшего пути <b>IGP</b>", "#f9b5a6"), "rd", num="2")
    slide("pptx 47 · LDP и RSVP-TE", "bgk_12", T, row(step(ldp), step(rsvp)), sub=SUB)

    t1 = ('<table class="m2tbl" style="font-size:clamp(15px,1.3vw,25px)"><tr><th>Способ</th><th>Как определяется путь</th>'
          '<th>Как появляются правила с метками</th></tr>'
          '<tr><td><b>LDP</b></td><td>Обычно следует маршрутам IGP</td><td>Через обмен соответствиями меток и FEC</td></tr>'
          '<tr><td><b>RSVP-TE</b></td><td>Выбирается с учётом ограничений TE</td><td>Через сигнализацию туннеля</td></tr>'
          '<tr><td><b>Статические записи</b></td><td>Задаётся администратором</td><td>Настраиваются вручную на устройствах</td></tr>'
          '</table>')
    rows = [("Выбор пути", "Обычно следует IP-маршрутам IGP", "Путь задан или рассчитан с ограничениями TE"),
            ("Обмен", "Привязки FEC ↔ метка между соседями", "Path → к выходу; Resv → ко входу"),
            ("Ресурсы", "Не резервирует полосу сам по себе", "Может резервировать запрошенную полосу"),
            ("Состояние на узлах", "Для FEC и привязок меток", "Для конкретного TE-LSP"),
            ("Типичная задача", "Базовый MPLS-транспорт", "Управление путями и распределением трафика")]
    t2 = ('<table class="m2tbl" style="font-size:clamp(14px,1.2vw,23px)"><tr><th>Критерий</th><th style="background:#2f9e5b">LDP</th>'
          '<th style="background:#e2563c">RSVP-TE</th></tr>%s</table>'
          % "".join("<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>" % r for r in rows))
    slide("pptx 47 · Сравнение", "bgk_12", T, "".join([
        step(panel("Как определяется путь и появляются правила", t1, num="1")),
        step(panel("Критерии", t2, "tint", num="2")),
        step(bulb("<b>RSVP-TE сигнализирует путь, а не рассчитывает его сам.</b> Резервирование полосы не заменяет QoS.")),
    ]), sub=SUB)


# ---------------------------------------------------------------- pptx 48
def b48():
    T = "Мониторинг состояния путей <em>LSP</em>"
    avail = ('<div style="display:flex;align-items:center;gap:12px;background:#f5dc8a;border:2px solid #c9a23a;border-radius:16px;'
             'padding:8px 14px;flex:none">%s<div class="m2b" style="line-height:1.25">Пример требований<br>к готовности:<br>'
             '<b style="font-size:1.4em">99,9–99,999 %%</b></div></div>' % ico("i48a_gear.png", 70))
    oam = panel('OAM <span style="text-transform:none;font-weight:700">— эксплуатация, администрирование и техническое обслуживание</span>',
                '<div style="display:flex;gap:16px;align-items:center"><div class="m2b" style="flex:1">Наличие встроенных в '
                'транспортную технологию средств мониторинга состояния соединений и локализации ошибок (то есть средств <b>ОАМ</b> - '
                'эксплуатация, администрирование и техническое обслуживание сети.) является необходимым условием для того, чтобы она '
                'претендовала на статус технологии операторского класса. В противном случае ее трудно будет использовать операторам '
                'сетей, которым нужно обеспечивать своих многочисленных клиентов транспортным сервисом с высоким коэффициентом '
                'готовности (в пределах 0,999-0,99999), как это принято в телекоммуникационных сетях.</div>%s</div>' % avail, num="1")
    RED, BL = "#e2342b", "#2a7fd8"
    ipnet = net([(8, 50, rt("R1", img="i52a_rt.png", h=40)), (45, 18, rt("R2", img="i52a_rt.png", h=40)),
                 (45, 82, rt("R3", img="i52a_rt.png", h=40)), (88, 50, rt("R4", img="i52a_rt.png", h=40)),
                 (66, 30, '<span class="s7x">✕</span>'),
                 (45, -6, '<span class="s7pill" style="background:#f2694a;color:#fff">Проверяемый LSP</span>'),
                 (66, 104, '<span class="s7pill" style="background:#cfe6fb;color:#13306e">Возможный обход по IP</span>')],
                [(8, 45, 45, 14, RED, 5, 0), (45, 14, 88, 45, RED, 5, 1), (8, 55, 45, 78, BL, 5, 1), (45, 78, 88, 55, BL, 5, 1)],
                "clamp(130px,12vw,220px)")
    why = panel("Почему обычного IP ping недостаточно?",
                '<div style="display:flex;gap:18px;align-items:center"><div class="m2b" style="flex:1.3">Первоначально технология '
                'MPLS не имела таких встроенных средств, полагаясь на такие средства стека TCP/IP, как утилиты ping и traceroute. '
                'Однако классические утилиты ping и traceroute стека TCP/IP не дают корректной информации о состоянии путей LSP, так '
                'как они могут переноситься как вдоль, так и в обход этих путей с помощью обычной техники продвижения пакетов '
                'протокола IP.</div><div style="flex:1;padding:18px 0">%s</div>'
                '<div style="flex:none;background:#c4e8e0;border-radius:18px;padding:14px 18px;text-align:center;'
                'font:900 clamp(17px,1.6vw,30px)/1.2 Golos Text,sans-serif;color:#13306e">IP доступен<br>'
                '<span style="color:#e2342b">≠</span><br>LSP исправен</div></div>' % ipnet, "rd", num="2")
    slide("pptx 48 · OAM", "bgk_23", T, step(oam) + step(why), safe="sr")

    def card(img, h, title, hbg, text, task):
        return panel("", '<div class="s7card">%s<div><div class="m2h" style="margin:0 0 4px">%s</div><div class="m2b">%s</div>'
                         '<div class="m2b s7task" style="background:%s"><b>Задача:</b> %s</div></div></div>'
                     % (ico(img, h), title, text, hbg, task))
    slide("pptx 48 · LSP Ping и BFD", "bgk_23", T, "".join([
        step(panel("", '<div class="m2big">Поэтому позднее был разработан специальный протокол <b>LSP Ping</b>, который позволяет '
                       'как тестировать работоспособность LSP (режим ping), так и локализовывать отказы (режим traceroute). Кроме '
                       'того, для мониторинга состояния LSP можно применять более экономичный, чем LSP Ping, протокол '
                       'двунаправленного обнаружения ошибок продвижения.</div>', "or")),
        row(step(card("i48a_ic1.png", 56, "LSP Ping", "#c4e8e0",
                      "Проверяет работоспособность пути и соответствие пересылки указанному FEC.", "проверить LSP.")),
            step(card("i48a_ic2.png", 56, "LSP Traceroute", "#f9d0c4",
                      "Поэтапно исследует путь и помогает определить участок, где нарушена передача.", "локализовать проблему.")),
            step(card("i48a_ic3.png", 56, "BFD для LSP", "#f5dc8a",
                      "Лёгкие периодические сообщения позволяют быстро обнаруживать потерю связности. Скорость зависит от "
                      "настроенных таймеров и возможностей устройств.", "непрерывно обнаруживать отказ."))),
        step(bulb("<b>LSP Ping / Traceroute</b> — диагностика. <b>BFD</b> — быстрое обнаружение потери связности.", "i48a_bulb.png")),
    ]), safe="sr")


# ---------------------------------------------------------------- pptx 49
TT = "Тестирование путей <em>LSP</em>"


def b49():
    hdr = ('<div style="display:flex;align-items:center;gap:14px;justify-content:center;margin-bottom:16px">'
           '<span style="display:inline-flex;border:2px solid #1d3f8a;font:700 clamp(13px,1.15vw,22px)/1.15 Golos Text,sans-serif;'
           'color:#13306e;text-align:center"><span style="background:#f2694a;padding:3px 12px">Метка<br>105</span>'
           '<span style="background:#fff;padding:3px 12px;border-left:2px solid #1d3f8a">IP / UDP<br>…</span>'
           '<span style="background:#bfe0fa;padding:3px 14px;border-left:2px solid #1d3f8a;align-self:stretch;display:grid;'
           'place-items:center">Echo Request</span></span><span class="m2cap">Проверяемая FEC: 105.0.0.0</span></div>')
    req = '<div class="m2cap" style="color:#1b7a6a">Echo Request — по проверяемому LSP1 →</div>'
    rep = step('<div class="m2cap" style="color:#e2493c;margin-top:4px">← Echo Reply — ответ выходного LER</div>'
               '<div class="m2cap" style="font-weight:600;font-size:clamp(12px,.95vw,18px)">Обратный ответ может идти по IP-маршруту, '
               'отличному от LSP.</div>')
    scheme = panel("Проверка LSP1 к сети 105.0.0.0", hdr + '<div class="m2zone"><span class="m2zl">MPLS-сеть</span>' + req
                   + lsp_chain() + "</div>" + rep, "tint")

    def sc3(n, col, t, x):
        return step(panel("", stp(n, col, t, x)))
    slide("pptx 49 · LSP Ping", "bgk_09", TT, "".join([
        step(panel("LSP Ping", '<div class="m2b">В протоколе LSP Ping для тестирования '
                   'состояния LSP применяется техника, близкая к механизму работы утилиты ping протокола IP. Она заключается в том, '
                   'что протокол LSP Ping отправляет вдоль тестируемого пути LSP сообщение <b>Echo Request</b>. Если такое сообщение '
                   'доходит до устройства LER, которое является конечным узлом тестируемого пути LSP, оно отвечает сообщением '
                   '<b>Echo Reply</b>. Получение исходным узлом такого сообщения означает, что путь LSP работоспособен. Описанная '
                   'схема работы аналогична схеме работы утилиты ping протокола IP, однако она имеет свои особенности, которые мы '
                   'поясним на примере сети.</div>', num="1")),
        step(scheme),
    ]), sub="LSP Ping проверяет передачу по конкретному LSP и соответствие пути проверяемому классу FEC.")
    slide("pptx 49 · Пример сети", "bgk_09", TT, "".join([
        '<div style="flex:1;min-height:0;display:flex">%s</div>' % ping_scene(False),
        row(sc3(1, "#e2493c", "Отправить запрос", "Входной LER направляет Echo Request вдоль тестируемого LSP."),
            sc3(2, "#e2493c", "Проверить FEC", "Выходной LER проверяет, что он является конечным узлом для указанной FEC."),
            sc3(3, "#e2493c", "Получить ответ", "Успешный Echo Reply подтверждает результат проверки LSP.")),
        step('<div class="m2note" style="background:#c4e8e0;border-color:#13633f"><b>Важно проверить успешный код ответа, а не только '
             'факт получения Echo Reply.</b> Отсутствие ответа может быть связано и с проблемой обратного пути.</div>'),
    ]))


# ---------------------------------------------------------------- pptx 50
def b50():
    SUB = "Что находится внутри Echo Request"
    nest = (step('<div class="s7nest" style="background:#f68e74">MPLS: <span>метка</span> <em>105</em>'
                 + step('<div class="s7nest" style="background:#bfe9d6;margin-top:6px">IP: <span>SA — адрес LSR1; DA —</span> '
                        '<em>127.0.0.1</em>'
                        + step('<div class="s7nest" style="background:#bfe0fa;margin-top:6px">UDP'
                               '<div class="s7nest" style="background:#fff;margin-top:6px;border-width:2px">Echo Request: '
                               '<span>FEC</span> <em>105.0.0.0</em></div></div>') + '</div>') + '</div>'))
    chain = step(panel("", '<div class="m2zone"><span class="m2zl">LSP1</span>'
                       + lsp_chain(cloud="i50a_cloud.png", subs=("Отправитель", "", "", "Выходной LER"))
                       + '<div class="m2cap">Метки меняются на каждом участке; DA и FEC сохраняются.</div></div>', "tint"))
    slide("pptx 50 · Echo Request", "bgk_07", TT, "".join([
        row(step(panel("Echo Request", '<div class="m2b" style="font-size:clamp(14px,1.18vw,23px)">В этом примере устройство LSR1 '
                       'тестирует состояние пути LSP1, который заканчивается на устройстве LSR8 (для этого пути оно является '
                       'устройством LER). Для тестирования пути LSP1 устройство LSR1 отправляет MPLS-пакет с меткой <b>105</b> — эта '
                       'метка соответствует пути LSP1 на линии между устройствами LSR1 и LSR4. Сообщение Echo Request вкладывается в '
                       'UDP-сообщение, которое, в свою очередь, вкладывается в IP-пакет. На схеме показаны только значимые для '
                       'изучения протокола LSP Ping поля: метка MPLS-кадра, IP-адрес источника (SA), IP-адрес назначения (DA), а '
                       'также поле FEC, которое идентифицирует тестируемый путь LSP. В нашем примере это IP-адрес сети 105.0.0.0, к '
                       'которой ведет путь LSP1.</div>', num="1")),
            '<div style="display:flex;flex-direction:column;justify-content:center">%s</div>' % nest),
        chain,
    ]), safe="sr", sub=SUB)

    def q(title, html, cls=""):
        return panel('<span class="s7q">?</span>' + title, '<div class="m2b">%s</div>' % html, cls)
    slide("pptx 50 · Адрес 127.0.0.1 и поле FEC", "bgk_07", TT, "".join([
        row(step(q("Зачем DA = 127.0.0.1?",
                   "Адрес назначения в IP-пакете, который переносит сообщение Echo Request, равен <b>127.0.0.1</b>, то есть является "
                   "адресом обратной петли стека протоколов IP каждого узла. О причине использования такого необычного адреса "
                   "назначения (а не, скажем, IP-адреса интерфейса конечного узла тестируемого пути LSP) мы расскажем позже, а пока "
                   "заметим, что адрес 127.0.0.1 должен работать правильно, так как в процессе передачи запроса по сети для его "
                   "продвижения используются <b>MPLS-метки, а не IP-адрес назначения</b>.")),
            step(q("На конечном узле",
                   "При приходе на конечный узел IP-пакет освобождается от заголовка MPLS (это также может произойти на предыдущем "
                   "хопе, если применяется техника PHP) и обрабатывается на основе IP-адреса. Так как адрес 127.0.0.1 указывает на "
                   "собственный узел, то пакет передается <b>собственному стеку TCP/IP</b>, где он распознается как UDP-пакет "
                   "протокола LSP Ping и обрабатывается соответственно.", "or"))),
        step(q("Зачем поле FEC?",
               "Поле FEC посылается в запросе Echo Request для того, чтобы конечный узел пути мог <b>сравнить указанное в пакете "
               "значение FEC со значением из его собственной базы данных</b> для пути, по которому пришел кадр запроса.", "gr")),
        step('<div class="m2note" style="display:flex;align-items:center;justify-content:center;gap:12px;background:#fdf8ea;'
             'border-color:#1f63c6">%s<span><b>MPLS-заголовок снимается на выходе или на предыдущем хопе при PHP.</b></span></div>'
             % ico("i50a_gear.png", 34)),
    ]), safe="sr", sub=SUB)


# ---------------------------------------------------------------- pptx 51
def b51():
    SUB = "Проверка FEC и возврат Echo Reply"
    fec = ('<span style="flex:none;background:#fbefc4;border:2px solid #1d3f8a;border-radius:6px;padding:4px 10px;text-align:center;'
           'font:700 clamp(14px,1.2vw,23px)/1.2 Golos Text,sans-serif;color:#13306e">Проверка<br>FEC '
           '<span style="color:#22a33a;font-weight:900">✓</span></span>')
    rts = [node(ico("i52a_rt.png", 74), "LSR1", "Инициатор<br>проверки"), node(ico("i52a_rt.png", 74), "LSR"),
           node(ico("i52a_rt.png", 74), "LSR"), node(ico("i52a_rt.png", 74), "LSR8", "Конечный узел<br>LSP")]
    chain = '<div class="s7lc">%s%s%s%s%s%s%s%s</div>' % (rts[0], ln("r"), rts[1], ln("r"), rts[2], ln("r"), rts[3], ln("k") + fec)
    scheme = panel("", '<div class="m2h" style="justify-content:center;margin-bottom:22px">Запрос — по проверяемому LSP; ответ — по IP</div>'
                   '<div class="m2zone" style="padding:18px 16px 14px"><span class="m2zl">Проверяемый однонаправленный LSP</span>'
                   '<div class="m2cap" style="color:#e2342b">Echo Request + FEC →</div>' + chain + "</div>"
                   + step('<div style="margin:8px auto 0;width:70%;border:3px dashed #1f63c6;border-top:0;border-radius:0 0 30px 30px;'
                          'text-align:center;padding:4px 0 6px"><b class="m2cap" style="color:#1f63c6">← Echo Reply: UDP в IP-пакете'
                          '</b> &nbsp;<span class="m2pill bl">IP-сеть</span></div>'), "tint")
    slide("pptx 51 · Проверка FEC", "bgk_02", TT, "".join([
        step(panel("", '<div class="m2big">Такой механизм позволяет отслеживать ситуации, когда запрос вследствие каких-то ошибок '
                       'приходит не по тому пути, который тестируется. В том случае, когда запрос благополучно доходит до конечного '
                       'узла пути, и тот убеждается, что полученный запрос пришел по нужному пути (то есть <b>полученное значение FEC '
                       'совпадает со значением FEC из базы данных конечного узла</b>), он отправляет ответ Echo Reply узлу, '
                       'выполнившему запрос. В нашем случае узел LSR8 отправляет ответ Echo Reply узлу LSR1.</div>', num="1")),
        step(scheme),
        step('<div class="m2note" style="background:#fdf8ea;border-color:#1f63c6">Конечный узел LSR8 проверяет, что указанный в '
             'Echo Request FEC соответствует завершению проверяемого LSP на этом узле. При успешной проверке он формирует '
             '<b>Echo Reply с кодом результата</b>.</div>'),
    ]), sub=SUB)

    def card(n, col, title, text):
        return step(panel("", stp(n, col, title, text)))
    slide("pptx 51 · Echo Reply по IP", "bgk_02", TT, "".join([
        step(panel("Обратный маршрут", '<div class="m2big">Сообщение Echo Reply посылается уже <b>не по пути LSP, а как обычное '
                   'UDP-сообщение, вложенное в IP-пакет</b>. Если вспомнить, что пути LSP являются однонаправленными, станет понятно, '
                   'что это единственное гарантированное решение, так как обратного пути от LSR8 к LSR1 может и не существовать. '
                   'Теперь посмотрим, что происходит в том случае, когда по какой-то причине путь LSP поврежден.</div>', "or", num="2")),
        row(card(1, "#4fb08a", "Проверка назначения", "Узел проверяет FEC и возвращает код результата: достижение узла само по "
                                                      "себе ещё не означает успех теста."),
            card(2, "#f2694a", "Обратный маршрут", "В рассматриваемом режиме ответ идёт по обычной IP-маршрутизации. Обратный LSP "
                                                   "не требуется, но нужна IP-достижимость LSR1."),
            card(3, "#3d8fe6", "Если ответа нет", "Возможен сбой LSP, обратного IP-пути или обработки запроса. Для локализации "
                                                  "используют LSP Traceroute и дополнительные проверки.")),
        step(bulb("<b>Успешный Echo Reply</b> подтверждает результат конкретной проверки. Отсутствие ответа требует диагностики.",
                  "i51a_bulb.png", "#f5d24a")),
    ]), sub=SUB)


# ---------------------------------------------------------------- pptx 52, 53
T52 = ("В этой ситуации LSR7 не может отправить MPLS-кадр по назначению, как того требует метка 177, а отбрасывает заголовок MPLS и "
       "старается обработать кадр как IP-пакет. Как и в случае исправного пути, адрес 127.0.0.1 требует передачи пакета локальному "
       "стеку TCP/IP. Именно этого эффекта и добивались разработчики протокола LSP Ping, выбирая в качестве адреса назначения этот "
       "специальный адрес. Узел LSR7 обрабатывает сообщение Echo Request и отправляет сообщение Echo Reply узлу LSR1 с информацией "
       "об обнаруженной ошибке.")


def b52():
    SUB = "LSP Ping: обнаружение ошибки на LSR7"
    chain = lsp_chain(cloud="i52a_cloud.png", subs=("", "", "", ""), lcls=("g", "g", "r"), lncls=("", "", "d", "k"),
                      mid_img="i52a_red.png", last_img="i52a_gray.png")
    chain = chain.replace(lb("210", "r") + ln("d"), lb("210", "r") + '<span class="s7x">✕</span>' + ln("d"))
    scheme = panel("", '<div class="m2zone"><span class="m2zl">LSP1</span>'
                   '<div style="text-align:center;margin:4px 0"><span class="s7lb r" style="padding:0 14px">Метка: 177 | DA: 127.0.0.1 | '
                   'FEC: 105.0.0.0</span></div>' + chain + "</div>"
                   + step('<div class="m2cap" style="margin-top:6px"><span class="s7lb r" style="font-size:inherit">← Echo Reply: '
                          '<span style="color:#b01a14">информация об ошибке</span></span></div><div class="m2cap" style="font-weight:600">'
                          'Ответ возвращается по IP-маршруту; он может отличаться от пути запроса.</div>'), "tint")

    def card(n, title, text):
        return step(panel("", stp(n, "#4fb08a", title, text)))
    slide("pptx 52 · Неисправный путь", "bgk_16", TT, "".join([
        step(panel("", '<div class="m2b" style="font-size:clamp(15px,1.3vw,25px)">%s</div>' % T52, "rd")),
        step(scheme),
        row(card(1, "Сбой продвижения", "В этом примере LSR7 не может продолжить передачу по LSP1."),
            card(2, "Локальная обработка запроса", "После снятия MPLS-заголовка адрес DA = 127.0.0.1 направляет запрос локальному "
                                                   "обработчику LSP Ping."),
            card(3, "Сообщение об ошибке", "LSR7 обрабатывает Echo Request и отправляет Echo Reply узлу LSR1 с кодом обнаруженной "
                                           "ошибки.")),
        step('<div class="m2note" style="text-align:left"><b style="color:#d0281f">Пример обработки диагностического запроса:</b> '
             'обычный MPLS-пакет при ошибке не обязан переходить на IP-продвижение.</div>'),
    ]), sub=SUB)
    slide("pptx 53 · Неисправный путь: схема", "bgk_16", TT,
          '<div class="m2row" style="flex:1;min-height:0"><div style="flex:.62 1 0;min-width:0">%s</div>'
          '<div style="flex:1.38 1 0;min-width:0;display:flex">%s</div></div>'
          % (step(panel("Сбой продвижения на LSR7", '<div class="m2b">%s</div>' % T52, "rd")), ping_scene(True)), sub=SUB)


# ---------------------------------------------------------------- pptx 54
def b54():
    T = "Трассировка путей <em>LSP</em>"
    SUB = "LSP Ping в режиме traceroute: проверяем путь по хопам"
    X = (10, 30, 50, 70, 90)
    head = net([(X[0], 40, rt("LER1", "(источник)", "i54a_rt.png", 44)), (X[1], 40, rt("LSR1", img="i54a_rt.png", h=44)),
                (X[2], 40, rt("LSR2", img="i54a_rt.png", h=44)), (X[3], 40, rt("LSR3", img="i54a_rt.png", h=44)),
                (X[4], 40, rt("LER2", "(конец LSP)", "i54a_rt.png", h=44)), (60, 22, '<span class="s7x">✕</span>'),
                (60, -4, '<b class="m2cap" style="color:#ec4a2c">Пример отказа</b>')],
               [(X[0], 22, X[2], 22, "#bfe6d6", 10, 0), (X[2], 22, X[3], 22, "#f08a60", 4, 1), (X[3], 22, X[4], 22, "#bfe6d6", 10, 0)],
               "clamp(80px,7vw,130px)")
    sm = lambda x: ico("i54a_rt.png", 30, style="left:%g%%;top:38%%" % x)

    def tr(k, to, ok=True):
        a, b = X[0], X[to]
        if ok:
            body = (sm(a) + sm(b) + '<span class="s7a rq" style="left:%g%%;width:%g%%"></span>' % (a + 3, b - a - 6)
                    + '<b style="left:%g%%;top:4%%;color:#1f63c6">Echo Request (TTL=%d)</b>' % ((a + b) / 2.0, k)
                    + '<span class="s7a rp l" style="left:%g%%;width:%g%%"></span>' % (a + 3, b - a - 6)
                    + '<b style="left:%g%%;top:84%%;color:#2a9a4a;background:rgba(232,244,252,.95);padding:0 6px">Echo Reply</b>' % ((a + b) / 2.0))
        else:
            body = (sm(a) + sm(b) + '<span class="s7a rq" style="left:%g%%;width:%g%%"></span>' % (a + 3, b - a - 6)
                    + '<b style="left:%g%%;top:4%%;color:#1f63c6">Echo Request (TTL=%d)</b>' % ((a + b) / 2.0, k)
                    + '<span class="s7a rq" style="left:%g%%;width:5%%"></span>' % (b + 3)
                    + '<span class="s7x" style="left:%g%%;top:14%%;transform:translateX(-50%%)">✕</span>' % (b + 11)
                    + '<span class="s7a to" style="left:%g%%;width:8%%"></span>' % (b + 14)
                    + '<b style="left:%g%%;top:54%%;color:#ec4a2c">Нет ответа • тайм-аут</b>' % (b + 22))
        return step('<div class="s7tr"><div class="s7tl">MPLS TTL = %d</div><div class="s7tz">%s</div></div>' % (k, body))
    diag = '<div class="s7tr"><div></div><div>%s</div></div>' % head + tr(1, 1) + tr(2, 2) + tr(3, 2, False) + step(
        '<div class="m2cap" style="display:flex;align-items:center;justify-content:center;gap:8px;margin-top:4px">%s Echo Reply '
        'возвращается к источнику по IP.</div>' % ico("i54a_info.png", 26))
    slide("pptx 54 · Трассировка LSP", "bgk_19", T, "".join([
        step(panel("", '<div class="m2b" style="font-size:clamp(15px,1.3vw,25px)">При неисправном состоянии какого-то отрезка пути LSP сообщение об ошибке не всегда может '
                       'быть отправлено промежуточным устройством LSP. Возможна и такая ситуация, когда ответ на запрос Echo Request '
                       'просто не приходит — <b>сеть «молчит»</b>, например, потому что отказал промежуточный узел. Для того чтобы '
                       'локализовать отказавший элемент сети (узел или соединение), протокол LSP Ping может работать в <b>режиме '
                       'трассировки пути LSP</b>.</div>', num="1")),
        panel("Как работает трассировка", '<div style="display:flex;flex-direction:column;gap:8px">%s</div>' % diag, "tint"),
    ]), safe="s7hl", sub=SUB)

    def card(n, col, img, title, text):
        return step(panel("", '<div class="s7card">%s<div>%s</div></div>' % (ico(img, 58), stp(n, col, title, text))))
    slide("pptx 54 · TTL в заголовке MPLS", "bgk_19", T, "".join([
        step(panel("Режим трассировки", '<div class="m2b" style="font-size:clamp(15px,1.32vw,25px)">Этот режим аналогичен режиму '
                   'работы утилиты traceroute стека TCP/IP и в нем используется тот же механизм, заключающийся в посылке серии '
                   'сообщений Echo Request с монотонно возрастающим от 1 значением поля <b>TTL</b>. Разница состоит в том, что это '
                   'поле указывается не в IP-пакете, как при использовании IP-утилиты traceroute, а в <b>заголовке MPLS</b> (который '
                   'также имеет поле TTL). Дальнейшее поведение протокола LSP Ping в режиме трассировки очевидно — MPLS-кадр с '
                   'нулевым значением TTL передается «наверх» протоколу LSP Ping того промежуточного узла, который после вычитания '
                   'единицы из значения этого поля получил нулевой результат. Протокол реагирует на такую ситуацию отправкой '
                   'сообщения Echo Reply начальному узлу тестируемого пути.</div>', "or", num="2")),
        row(card(1, "#2a7fd8", "i54a_ttl.png", "Увеличиваем TTL", "Источник отправляет Echo Request с MPLS TTL = 1, 2, 3..."),
            card(2, "#3cba86", "i54a_hop.png", "Получаем ответы", "На каждом хопе TTL уменьшается. При его истечении запрос "
                                                                 "обрабатывается локально; узел формирует Echo Reply."),
            card(3, "#f08a60", "i54a_mag.png", "Сужаем поиск", "Последний ответивший узел и последующие тайм-ауты указывают "
                                                               "область возможной неисправности.")),
        row(step('<div class="m2note" style="background:#e3f4ec;border-color:#9fcfc0;display:flex;align-items:center;gap:12px;'
                 'text-align:left;height:100%%;box-sizing:border-box">%s<span><b>Используется TTL заголовка MPLS, а не IP TTL.</b>'
                 '</span></div>' % ico("i54a_gear.png", 44)),
            step('<div class="m2note" style="display:flex;align-items:center;gap:12px;text-align:left;height:100%%;box-sizing:border-box">'
                 '%s<span><b>Нет ответа ≠ точное доказательство отказа:</b> возможны фильтрация или проблема обратного IP-пути.'
                 '</span></div>' % ico("i54a_excl.png", 44))),
    ]), safe="s7hl", sub=SUB)


# ---------------------------------------------------------------- pptx 55
def b55():
    T = "Протокол двунаправленного обнаружения <em>ошибок продвижения</em>"
    env = ico("i55a_env.png", 26, "s7env")
    fwd = ('<div class="s7flow" style="color:#1aa58a">%s%s%s%s%s%s</div>'
           % ('<span class="s7ln" style="color:#1aa58a;background:#1aa58a"></span>', env, env,
              '<span class="s7ln" style="color:#1aa58a;background:#1aa58a"></span>', env, env))
    bwd = ('<div class="s7flow" style="transform:scaleX(-1)">%s%s%s%s%s%s</div>'
           % ('<span class="s7ln k"></span>', env, env, '<span class="s7ln k"></span>', env, env))
    diag = ('<div style="display:flex;align-items:center;gap:10px">%s<div style="flex:1;display:flex;flex-direction:column;gap:8px">'
            '<div style="text-align:center"><span class="s7pill" style="background:#a6e3cf;color:#13306e">Контролируемый LSP: BFD Control →'
            '</span></div>%s%s<div style="text-align:center"><span class="s7pill" style="background:#14396e;color:#fff">Обратный канал: '
            '← BFD Control</span></div></div>%s</div>'
            % (node(ico("i55a_rt.png", 70), "LER1"), step(fwd), step(bwd), node(ico("i55a_rt.png", 70), "LER2")))
    slide("pptx 55 · BFD", "bgk_01", T, "".join([
        row(step(panel('BFD и LSP Ping',
                       '<div class="m2b" style="font-size:clamp(14px,1.17vw,22.5px)">Протокол двунаправленного обнаружения ошибок '
                       'продвижения (<b>Bidirectional Forwarding Detection, BFD</b>) разработан как «облегченная» альтернатива '
                       'протоколу LSP Ping для постоянного мониторинга состояния пути LSP. Такой постоянный мониторинг требуется, '
                       'например, в тех случаях, когда основной путь защищен резервным путем и необходим какой-то механизм, который, с '
                       'одной стороны, может быстро выявить отказ пути, а с другой — не перегружает сеть тестовыми сообщениями и '
                       'трудоемкими проверками. Протокол LSP Ping удовлетворяет первому условию, то есть может использоваться для '
                       'постоянного тестирования состояния пути путем периодической отправки сообщений Echo Request. Однако обработка '
                       'этих сообщений конечным узлом пути довольно трудоемка, так как требует сравнения значения FEC в каждом '
                       'пришедшем запросе со значением из базы данных.</div>', num="1")),
            step(panel("Обратное направление", '<div class="m2b" style="font-size:clamp(14px,1.17vw,22.5px)">Протокол BFD гораздо '
                       'проще, чем LSP Ping. Однако он не способен локализовать отказавший элемент сети, а только показывает, '
                       'работоспособен некоторый путь LSP или нет. Название протокола говорит о том, что он проверяет состояние '
                       'соединения между двумя узлами в обоих направлениях. Так как пути MPLS однонаправленные, то для работы '
                       'протокола BFD необходима <b>пара путей LSP</b>, соединяющих два узла в обоих направлениях.</div>', "or",
                       num="2"))),
        step(panel("Постоянный контроль между двумя конечными узлами", diag
                   + '<div class="m2cap" style="margin-top:6px">BFD контролирует доступность; причину и точное место отказа ищут '
                     'другими средствами.</div>', "tint")),
    ]))

    seq = ('<div class="s7seq"><div style="background:#d3eee4">%s Пакеты поступают</div><span>→</span>'
           '<div style="background:#f9d3cc">%s Нет пакетов в течение времени обнаружения</div><span>→</span>'
           '<div style="background:#f9d3cc">%s Состояние Down → сигнал механизмам защиты</div></div>'
           % (ico("i55a_m1.png", 40), ico("i55a_m2.png", 46), ico("i55a_m3.png", 50)))
    slide("pptx 55 · BFD: сообщения Hello", "bgk_01", T, "".join([
        step(panel("Сообщения Hello", '<div class="m2b" style="font-size:clamp(15px,1.3vw,25px)">Каждый из двух конечных узлов, на которых для мониторинга определенного '
                   'пути LSP развернут протокол BFD, периодически посылает по этому пути сообщения <b>Hello</b>. Получение сообщений '
                   'Hello от соседа означает работоспособность пути в одном определенном направлении. Неполучение сообщения Hello в '
                   'течение определенного времени означает отказ пути в этом направлении, что и фиксирует протокол BFD. Информацию '
                   'об отказе пути могут немедленно использовать другие протоколы стека MPLS, например рассматриваемые далее '
                   'протоколы защиты пути.</div>', num="3")),
        step(seq),
        step(panel("Работа в MPLS", '<div class="s7card">%s<div class="m2b" style="font-size:clamp(15px,1.3vw,25px)">Протокол BFD посылает сообщения Hello в '
                   'UDP-сообщениях, которые, в свою очередь, упаковываются в IP-пакеты и снабжаются заголовками MPLS. Протокол BFD '
                   'может использоваться не только для мониторинга путей MPLS, он разработан как универсальный протокол тестирования '
                   'двунаправленных соединений. Обычно для инициализации сеанса BFD служит протокол LSP Ping, который переносит по '
                   'пути идентификаторы сеанса BFD.</div></div>' % ico("i55a_c2.png", 70), "gr", num="4")),
        step('<div class="m2note" style="background:#d3f0dc;border-color:#2f9e5b;display:flex;align-items:center;justify-content:center;'
             'gap:12px">%s<b>BFD обнаруживает отказ; переключение трафика выполняет настроенный механизм защиты.</b></div>'
             % ico("i55a_ok.png", 34)),
    ]))
