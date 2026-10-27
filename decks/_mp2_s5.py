# -*- coding: utf-8 -*-
"""MPLS 2.9 v2 — pptx 25–31: протокол LDP. Текст pptx дословно (из _mp_s2.py), разнесён по смыслу;
заголовки блоков, пилюли, подписи схем — из инфографик автора i25a…i31a. Сцена рисунка pptx 30 — ldp_scene."""
from _mp2_kit import slide, step, panel, row, pk, node, ico
from _mp_s2 import ldp_scene

TL = "Протокол <em>LDP</em>"
RT = "i30a_rt.png"


# ---------------------------------------------------------------- мелкие блоки живых схем
def rt(name, sub="", h=56):
    return node(ico(RT, h), name, sub)


def ln(lab="", cls="bl", d="r", low=""):
    """Стрелка-связь: подпись над линией, (необязательно) под ней; d — r / l."""
    top = '<span>%s</span>' % lab if lab else ""
    bot = '<small>%s</small>' % low if low else ""
    return '<div class="s5ln %s %s">%s<i></i>%s</div>' % (cls, d, top, bot)


def cl(s, big=False):
    return '<span class="s5cl%s">%s</span>' % (" big" if big else "", s)


def tag(s):
    return '<span class="s5tag">%s</span>' % s


def ch(*parts, cls=""):
    return '<div class="s5ch %s">%s</div>' % (cls, "".join(parts))


def col(*parts, cls="", style=""):
    return '<div class="s5col %s" style="%s">%s</div>' % (cls, style, "".join(parts))


def tb(head, rows, hl=None):
    th = "".join("<th>%s</th>" % h for h in head)
    out = []
    for r in rows:
        out.append("<tr>%s</tr>" % "".join(
            '<td%s>%s</td>' % (' class="s5hl"' if hl and c in hl else "", c) for c in r))
    return '<table class="m2tbl s5tb"><tr>%s</tr>%s</table>' % (th, "".join(out))


def fmt(rows):
    """Формат сообщения LDP (из инфографик): первая строка — две ячейки, дальше — на всю ширину."""
    a, b = rows[0]
    rest = "".join('<tr><td colspan="2">%s</td></tr>' % r for r in rows[1:])
    return '<table class="s5fmt"><tr><td>%s</td><td>%s</td></tr>%s</table>' % (a, b, rest)


def bar(html):
    return '<div class="s5bar">%s</div>' % html


def yl(icon, html):
    return '<div class="s5yl">%s<div>%s</div></div>' % (ico(icon, 40), html)


def card(icon, title, html, h=66):
    return '<div class="s5card">%s<div><div class="s5ct">%s</div>%s</div></div>' % (ico(icon, h), title, html)


def stg(n, s):
    return '<div class="s5stg"><span class="m2n">%d</span>%s</div>' % (n, s)


def head_ico(icon, s, h=44):
    return '<span class="s5hi">%s</span>%s' % (ico(icon, h), s)


ROUTES3 = [["132.100.0.0", "LSR2"], ["105.0.0.0", "LSR4"], ["192.201.103.0", "LSR4"]]


def build():
    # ================================================================ pptx 25
    S25 = "Label Distribution Protocol • протокол распределения меток"
    slide("pptx 25 · LDP", "bgk_26", TL, "".join([
        step(panel("", '<div class="m2big">Протокол распределения меток (<b>Label Distribution Protocol, LDP</b>) позволяет '
                   "автоматически создавать в сети пути LSP в соответствии с существующими в таблицах маршрутизации записях о "
                   "маршрутах в IP-сети.</div>")),
        row(
            step(panel(head_ico("i25a_lay.png", "MPLS IGP"),
                       '<p><span class="m2pill bl">LSP следует пути, выбранному IGP.</span></p>'
                       "<p>Протокол LDP принимает во внимание только те записи таблицы маршрутизации, которые созданы с помощью "
                       "внутренних протоколов маршрутизации, то есть протоколов типа IGP, поэтому режим автоматического создания "
                       "LSP с помощью протокола LDP иногда называют режимом <b>MPLS IGP</b></p>", "tint s5lg")),
            step(panel(head_ico("i25a_gear.png", "MPLS TE"),
                       '<p><span class="m2pill or">Путь может выбираться с учётом ресурсов и ограничений.</span></p>'
                       "<p>(в отличие от режима <b>MPLS TE</b>, когда маршруты выбираются из соображений инжиниринга трафика и не "
                       "совпадают с маршрутами, выбранными внутренними протоколами маршрутизации).</p>", "tint s5lg"))),
        step('<div class="s5flow" style="margin-right:30%%">%s</div>' % "".join([
            ico("i25a_s1.png", 50), "<span><b>IGP</b> выбирает маршрут</span>", '<span class="s5fa">→</span>',
            ico("i25a_s2.png", 50), "<span><b>LDP</b> распространяет метки</span>", '<span class="s5fa">→</span>',
            ico("i25a_s3.png", 50), "<span><b>LSR</b> формирует записи продвижения.</span>"])),
    ]), sub=S25)

    lsp1 = ch(
        step(node(ico("i25a_ip.png", 50), "IP-пакеты", "(без метки)")), step(ln()),
        step(rt("LSR1", h=66)),
        step(ln('<span class="m2flt">%s</span>' % pk([231]), "gr", low="LSP1")),
        step(rt("LSR4", h=66)), step(ln()), step(rt("LSR5", h=66)),
        step(ln(cls="gr")),
        step('<div class="s5stack">%s%s</div>' % (cl("105.0.0.0"), cl("192.201.103.0"))), cls="s5lsp")
    slide("pptx 25 · Один LSP для двух сетей", "bgk_26", TL, row(
        col(
            step(panel("", '<div class="m2big">Все устройства LSR поддерживают сигнальный протокол распределения меток (LDP). '
                       "От устройства LSR1 в сети уже установлен один путь LSP1 — по этому пути идет трафик к сетям "
                       "<b>105.0.0.0</b> и <b>192.201.103.0</b>. Это значит, что таблица FTN (отображающая сети назначения на "
                       "LSP) у LSR1</div>", "or")),
            panel("Пример: один LSP для двух сетей", lsp1 +
                  step(bar("Для сетей 105.0.0.0 и 192.201.103.0 следующий хоп — <b>LSR4.</b>")), "tint"),
            step(panel("Фрагмент FTN на LSR1",
                       tb(["Сети назначения / FEC", "Путь", "Выходная метка"], [["105.0.0.0; 192.201.103.0", "<b>LSP1</b>", "231"]],
                          hl=["231"]) + '<p style="margin-top:8px">Обе сети в данном примере направляются в LSP1.</p>', "s5lg")),
            style="flex:2.1"),
        col(step(panel("Маршруты на LSR1", tb(["Сеть", "Следующий хоп"], ROUTES3), "s5lg"))),
    ), sub=S25)

    # ================================================================ pptx 26
    S26 = "Новая сеть назначения и установление сеанса"
    slide("pptx 26 · Новая сеть назначения", "bgk_31", TL, "".join([
        row(
            step(panel("Исходная ситуация",
                       '<div class="m2big">Метка 231 в этой таблице соответствует пути LSP1. Мы рассмотрим функционирование '
                       "протокола LDP в ситуации, когда в результате работы протоколов маршрутизации или же после ручной "
                       "модификации администратором сети в таблице маршрутизации устройства LSR1 появилась запись о новой сети "
                       "назначения, для которой в сети поставщика услуг еще не проложен путь коммутации по меткам. В нашем случае "
                       "это сеть <b>132.100.0.0</b> и для нее нет записи в таблице FTN.</div>", "s5md", num="1")),
            col(step(panel("Фрагмент таблицы маршрутизации LSR1", tb(["Сеть", "Следующий хоп"], ROUTES3, hl=["132.100.0.0"]),
                           "tint"))), cls="s5r26"),
        step(panel("", '<div class="m2big">В этом случае устройство LSR1 автоматически инициирует процедуру прокладки нового '
                   "пути. Для этого оно запрашивает по протоколу LDP метку для новой сети 132.100.0.0 у маршрутизатора, IP-адрес "
                   "которого в таблице маршрутизации указан для данной сети как адрес следующего хопа.</div>", "or s5md", num="2")),
        step('<div class="m2note" style="margin-right:12%">Однако для того чтобы воспользоваться протоколом LDP, нужно сначала '
             "установить между устройствами LSR <b>сеанс LDP</b>, так как этот протокол работает в режиме установления "
             "соединений.</div>"),
    ]), sub=S26)

    st1 = col(step(stg(1, "Обнаружение соседей")),
              step(ch(rt("LSR1"), '<div class="s5two">%s%s</div>' % (ln("LDP Hello", "ds", "r"), ln("", "ds", "l")), rt("LSR2"),
                      cls="s5dia") + '<div class="s5pc"><span class="s5tag">224.0.0.2 • UDP 646</span></div>'),
              step('<div class="m2b">Сеансы LDP устанавливаются между соседними маршрутизаторами автоматически. Для этого каждое '
                   "устройство LSR, на котором развернут протокол LDP, начинает посылать своим соседям сообщения <b>Hello</b>. "
                   "Эти сообщения посылают по групповому IP-адресу <b>224.0.0.2</b>, который адресуется ко всем маршрутизаторам "
                   "подсети и определенному порту UDP.</div>"))
    st2 = col(step(stg(2, "Установление сеанса")),
              step(ch(rt("LSR1"), '<div class="s5two">%s%s</div>' % (ln("", "bl", "r"), ln("", "bl", "l")), rt("LSR2"),
                      cls="s5dia") + '<div class="s5pc"><span class="s5tag">TCP 646</span></div>'),
              step('<div class="m2b">Если соседний маршрутизатор также поддерживает протокол LDP, то он в ответ устанавливает '
                   "сеанс TCP через порт <b>646</b> (этот порт закреплен за протоколом LDP).</div>"),
              step('<div class="s5gbx">После обнаружения соседи устанавливают TCP-соединение и обмениваются сообщениями '
                   "инициализации LDP.</div>"))
    st3 = col(step(stg(3, "Обмен метками")),
              step('<div class="s5cap">Информация о метках для FEC</div>' +
                   ch(rt("LSR1", h=48), ln(), rt("LSR2", h=48), ln(), rt("LSR3", h=48), ln(), cl("132.100.0.0"), cls="s5dia")),
              step('<div class="m2b">В результате обмена сообщениями Hello все поддерживающие протокол LDP устройства LSR '
                   "обнаруживают своих соседей и устанавливают с ними сеансы.</div>"),
              step('<div class="s5gbx">LSR1 использует метку, полученную от следующего хопа LSR2.</div>'
                   '<div class="s5warn"><b>!</b>В режиме Downstream on Demand отправляется запрос Label Request.</div>'))
    itog = "".join([
        '<div class="s5it">%s<span>%s</span></div>%s' % (ico("i26a_ic%d.png" % i, 44), c, '<span class="s5fa">→</span>' if i < 3 else "")
        for i, c in enumerate(["Hello: UDP 646", "сеанс: TCP 646", "обмен метками", "записи FTN / LFIB"])])
    slide("pptx 26 · Сеанс LDP", "bgk_31", TL, "".join([
        panel("Процесс установления сеанса LDP", '<div class="s5stages">%s%s%s</div>' % (st1, st2, st3)),
        step('<div class="s5flow s5itg"><b class="s5ith">Краткий итог</b>%s</div>' % itog, "s5w78"),
    ]), sub=S26)

    # ================================================================ pptx 27
    S27 = "Запрос метки у соседа ниже по потоку"
    dod = "".join([
        step(ch('<div class="s5dir">%s</div>' % ln("Направление передачи данных", "bl"))),
        ch(step(col(rt("LSR1", h=62), '<div class="s5role">Upstream —<br>выше по потоку</div>', cls="s5ce")),
           step('<div class="s5two">%s%s</div>' % (
               ln("<b>Label Request:</b><br>запрашивает метку для FEC", "rd", "r"),
               ln("", "gr", "l", "<b>Label Mapping:</b><br>сообщает привязку FEC → метка"))),
           step(col(rt("LSR2", h=62), '<div class="s5role">Downstream —<br>ниже по потоку</div>', cls="s5ce")),
           step(ln("", "bl")),
           step(cl("Сеть назначения<br><b>132.100.0.0</b>", True)), cls="s5g27"),
        step('<div class="m2cap">Upstream и downstream определяются относительно конкретной сети назначения.</div>'),
    ])
    slide("pptx 27 · Upstream и downstream", "bgk_02", TL, '<div class="s5mid">%s</div>' % "".join([
        step(panel("", '<div class="m2b"><b>Условие:</b> будем считать, что между устройствами LSR1 и LSR2 установлен сеанс '
                   "LDP. Тогда при обнаружении новой записи в таблице маршрутизации, указывающей на устройство LSR2 в качестве "
                   "следующего хопа, устройство LSR1 просит устройство LSR2 назначить метку для нового пути к сети "
                   "132.100.0.0.</div>")),
        panel("Режим Downstream on Demand — распределение меток по запросу", dod, "tint"),
        step(panel("", "<p>Говорят, что устройство LSR2 находится <b>ниже по потоку (downstream)</b> для устройства LSR1 "
                       "относительно пути к сети 132.100.0.0. Соответственно устройство LSR1 расположено <b>выше по потоку</b> "
                       "для устройства LSR2 относительно сети 132.100.0.0. Естественно, что для других сетей назначения у "
                       "устройства LSR1 имеются другие соседи вниз по потоку, а у устройства LSR2 — другие соседи вверх по "
                       "потоку.</p>", "or")),
        step(yl("i27a_bulb.png", "Для других сетей назначения роли соседей могут отличаться. LDP также поддерживает объявления "
                                  "меток без предварительного запроса.")),
    ]), sub=S27)
    slide("pptx 27 · Почему метку выбирает LSR2", "bgk_19", TL, '<div class="s5r27">%s</div>' % "".join([
        step(panel("Почему метку выбирает LSR2?",
                   "<p>Причина, по которой значение метки для нового пути выбирается <b>соседом ниже по потоку</b>, понятна — "
                   "эта метка, которая имеет локальное значение на двухточечном соединении между соседними устройствами, будет "
                   "использоваться именно этим устройством для того, чтобы понимать, к какому пути LSP относится пришедший "
                   "MPLS-кадр. Поэтому устройство ниже по потоку выбирает уникальное значение метки, исходя из "
                   "неиспользованных значений меток для своего интерфейса, который связывает его с соседом выше по потоку.</p>"
                   + '<div class="s5gbx s5l">%s<span>Пространство меток может быть общим для устройства или отдельным для '
                     'интерфейса.</span></div>' % ico("i27a_db.png", 40), num="1")),
        step(panel("Сообщение Label Request",
                   "<p>Для получения значения метки устройство LSR1 выполняет <b>запрос метки</b> протокола LDP.</p>"
                   + fmt([("Запрос метки (0x0401)", "Длина сообщения"), "Идентификатор сообщения",
                          "FEC TLV — запрашиваемый класс пересылки"])
                   + '<p style="margin-top:8px">Запрос указывает FEC, для которого требуется метка.</p>', "or", num="2")),
    ]), sub=S27, safe="sl")

    # ================================================================ pptx 28
    S28 = 'Передача запроса метки к выходному узлу <span class="m2pill gr" style="margin-left:10px">Режим Downstream on Demand</span>'
    req = ln(tag("Label Request"), "rd", low="FEC: 132.100.0.0")
    edge = ch(
        step(rt("LSR1", "FEC: 132.100.0.0<br>Инициирует запрос", 44)), step(req),
        step(rt("LSR2", "FEC: 132.100.0.0<br>Нет готового LSP: запрашивает<br>метку у следующего хопа", 44)), step(req),
        step(rt("LSR3", "FEC: 132.100.0.0<br>Выходной узел: здесь<br>завершается LSP", 44)),
        step('<div class="s5bord">Граница MPLS-сети<br>оператора</div>'),
        step(ln("Следующий хоп —<br>вне MPLS", "gy")), step(cl("132.100.0.0", True)), cls="s5dia s5top")
    slide("pptx 28 · Запрос идёт к границе", "bgk_03", TL, '<div class="s5c28">%s</div>' % "".join([
        row(
            step(panel("Формат Label Request", fmt([("Запрос метки (0x0401)", "Длина сообщения"), "Идентификатор сообщения",
                                                     "Элемент FEC: 132.100.0.0"]))),
            step(panel("Зачем нужен идентификатор",
                       "<p>Идентификатор сообщения требуется для того, чтобы при получении ответа можно было однозначно "
                       "сопоставить ответ некоторому запросу (устройство может послать несколько запросов до получения ответов "
                       "на каждый из них).</p>"
                       '<p class="s5sm">Идентификаторы относятся к обмену между соседними LSR.</p>', "or"))),
        panel("Как запрос доходит до границы MPLS", edge, "tint"),
        row(
            step(panel("LSR2 проверяет маршрут",
                       "<p>В нашем примере в качестве элемента FEC будет указан адрес <b>132.100.0.0</b>. Устройство LSR2, "
                       "приняв запрос, находит, что у него также нет проложенного пути к сети 132.100.0.0, поэтому оно передает "
                       "LDP-запрос следующему устройству LSR, адрес которого указан в его таблице маршрутизации в качестве "
                       "следующего хопа для сети 132.100.0.0.</p>", num="1")),
            step(panel("LSR3 — конец пути",
                       "<p>В примере таким устройством является <b>LSR3</b>, на котором путь коммутации по меткам должен "
                       "закончиться, так как следующий хоп ведет за пределы MPLS-сети данного оператора.</p>", "gr", num="2")),
            cls="s5w84"),
    ]), sub=S28)

    # ================================================================ pptx 29
    S29 = "LSR3 объявляет метку для сети назначения"
    egr = '<div class="m2zone s5z"><span class="m2zl">MPLS-сеть оператора</span>%s</div>' % ch(
        step(rt("LSR2", h=62)),
        step('<div class="s5two s5wide">%s%s</div>' % (
            ln(tag("Label Mapping: FEC → 231"), "rd", "l"),
            ln('<span class="m2flt">%s</span>' % pk([231]), "bl", "r", "Данные с меткой 231"))),
        step(col('<span class="s5s0">S0</span>' + rt("LSR3", h=62), '<div class="s5role">Egress для<br>данного FEC</div>', cls="s5ce")),
        cls="s5dia")
    slide("pptx 29 · LSR3 объявляет метку", "bgk_13", TL, "".join([
        '<div class="s5r29">%s</div>' % "".join([
            step(panel("", '<div class="m2big">Устройство LSR3, обнаружив, что для пути к сети 132.100.0.0 оно является '
                       "<b>пограничным</b>, назначает для прокладываемого пути метку, еще не занятую его входным интерфейсом S0, "
                       "и сообщает об этой метке устройству LSR2 в LDP-сообщении. Пусть это будет метка <b>231</b>.</div>")),
            panel("", ch(egr, step(ln("IP без метки", "bl")), step(cl("Внешняя<br>IP-сеть<br><b>132.100.0.0</b>", True)),
                         cls="s5dia") +
                  step('<div class="m2cap" style="margin-top:6px">231 — условное значение обычной метки в этом учебном '
                       "примере.</div>"), "tint")]),
        step(panel("Сообщение Label Mapping", row(
            fmt([("Отображение метки (0x0400)", "Длина сообщения"), "Идентификатор сообщения",
                 "FEC TLV — сеть 132.100.0.0", "Generic Label TLV — метка 231"]),
            yl("i29a_bulb.png", "При использовании PHP выходной узел может объявить Implicit NULL (3), чтобы сосед снял "
                                "метку заранее."), cls="s5lm"), "or"), "s5l29"),
    ]), sub=S29)
    slide("pptx 29 · Как LSR3 узнаёт о границе", "bgk_13", TL, "".join([
        step(panel("Как LSR3 определяет роль Egress?",
                   '<div class="m2big">Возникает вопрос, как устройство LSR3 узнает о том, что является последним в сети '
                   "поставщика услуг на пути к сети 132.100.0.0?</div>", "tint"), "s5r29"),
        step(panel(head_ico("i29a_lock.png", "Аутентификация — защита сеанса", 52),
                   '<div class="m2big">Дело в том, что LDP является протоколом, <b>ориентированным на соединение</b>, и при '
                   "установлении логического LDP-соединения возможно применение автоматической аутентификации устройств, так "
                   "что сеансы LDP устанавливаются только между устройствами одного поставщика услуг, который задает для всех "
                   "принадлежащих его сети устройств LSR соответствующую информацию для взаимной аутентификации.</div>",
                   "gr"), "s5l29"),
    ]), sub=S29)

    # ================================================================ pptx 30
    S30 = ('Label Mapping и упорядоченное распределение меток '
           '<span class="m2pill gr" style="margin-left:10px">Ordered Control + Downstream on Demand</span>')
    lsp2 = ch(
        step(rt("LSR1")), step(ln('<span class="m2flt">%s</span>' % pk([199]))),
        step(rt("LSR2", "Swap <b>199</b> → 231")), step(ln('<span class="m2flt">%s</span>' % pk([231]))),
        step(rt("LSR3")), step(ln()),
        step('<div class="s5stack">%s%s%s</div>' % (cl("132.100.0.0"), cl("194.15.17.0"), cl("201.25.10.0"))), cls="s5dia")
    slide("pptx 30 · LSP2 готов", "bgk_15", TL, "".join([
        step(panel("", '<div class="m2big">В свою очередь, LSR2 назначает неиспользуемую его интерфейсом S0 метку и сообщает об '
                   "этом в LDP-сообщении отображения метки устройству LSR1. После этого новый путь коммутации по меткам, ведущий "
                   "от LSR1 к сети 132.100.0.0, считается проложенным, и вдоль него пакеты начинают передаваться уже <b>на основе "
                   "меток и таблиц продвижения</b>, а не IP-адресов и таблиц маршрутизации.</div>")),
        panel("LSP2 готов: данные идут по меткам", lsp2 + step('<div class="s5span"><i></i><b>LSP2</b><i></i></div>'), "tint"),
        step(panel("Запись продвижения LSR2",
                   tb(["Входная метка", "Выходная метка", "Следующий хоп"], [["199", "231", "LSR3"]]) +
                   '<p style="margin-top:8px">Метки локальны: 231 может использоваться на другом узле для другого пути.</p>',
                   "or"), "s5w66"),
    ]), sub=S30)

    slide("pptx 30 · Новый путь LSP2", "bgk_15", TL, "".join([
        step(panel("", "<p>Было бы нерационально прокладывать отдельный путь для каждой сети назначения каждого маршрутизатора. "
                       "Поэтому устройства LSR стараются строить <b>агрегированные пути</b> коммутации по меткам и передавать "
                       "вдоль них пакеты, следующие к некоторому набору сетей. Так устройство LSR1 передает по пути LSP1 пакеты, "
                       "следующие не только к сети 132.100.0.0, но и к сетям 194.15.17.0 и 201.25.10.0, информация о которых "
                       "появилась уже после того, как путь LSP2 был проложен.</p>", "or")),
        row(
            '<div class="s5scn">%s</div>' % ldp_scene(),
            col(step(panel("Маршруты на LSR1", tb(["Сеть", "Следующий хоп"],
                                                  [["132.100.0.0", "LSR2"], ["194.15.17.0", "LSR2"], ["201.25.10.0", "LSR2"],
                                                   ["105.0.0.0", "LSR4"], ["192.201.103.0", "LSR4"]],
                                                  hl=["132.100.0.0", "194.15.17.0", "201.25.10.0"]))),
                step(bar("Несколько сетей могут использовать общий путь при одинаковой обработке.")), cls="s5rc"),
            cls="s5r30"),
    ]), sub=S30)

    order = ch(
        rt("LSR1", h=62),
        step(ln(tag("2. Label Mapping: 199"), "rd", "l")),
        col(rt("LSR2", h=62), cls="s5ce"),
        step(ln(tag("1. Label Mapping: 231"), "rd", "l")),
        rt("LSR3", h=62), cls="s5dia")
    slide("pptx 30 · Упорядоченный режим", "bgk_15", TL, "".join([
        step(panel("", '<div class="m2big">Мы рассмотрели только один режим работы протокола LDP, который носит сложное '
                   "название <b>«Упорядоченный режим управления распределением меток с запросом устройства вниз по "
                   "потоку»</b>.</div>")),
        panel("Сначала — метка от соседа ниже по потоку", order +
              step('<div class="m2cap">Получает метку 231 от LSR3, затем назначает свою метку 199 для LSR1.</div>') +
              step(bar("LSR2 объявляет метку вверх по потоку после получения метки снизу по потоку.")), "tint"),
        step(panel("", "<p>Здесь под упорядоченным режимом понимается такой режим, когда некоторое промежуточное устройство LSR "
                       "<b>не передает метку</b> для нового пути устройству LSR, лежащему выше по потоку, <b>до тех пор, пока не "
                       "получит метку</b> для этого пути от устройства LSR, лежащего ниже по потоку. В нашем случае устройство "
                       "LSR2 ждало получения метки от LSR3 и уже потом передало метку устройству LSR1.</p>", "or"), "s5w78"),
    ]), sub=S30)

    # ================================================================ pptx 31
    S31 = "Два независимых параметра — четыре сочетания"
    ex = ch(rt("LSR1", h=50), step(ln(tag("199"), "rd", "l")), rt("LSR2", h=50), ln(tag("231"), "gy", "l", "ещё не пришла"),
            rt("LSR3", h=50), cls="s5dia")
    slide("pptx 31 · Управление распределением", "bgk_28", TL, "".join([
        step(panel("1. Управление распределением", "".join([
            card("i31a_play.png", "Независимое (Independent)",
                 "<p>Существует и другой режим управления распределением меток, который называется <b>независимым</b>. При "
                 "независимом управлении распределением меток LSR может назначить и передать метку, не дожидаясь прихода "
                 "сообщения от своего соседа, лежащего ниже по потоку.</p>"),
            card("i31a_chain.png", "Упорядоченное (Ordered)",
                 "<p>LSR объявляет метку, когда сам является Egress для FEC или уже получил привязку от следующего хопа.</p>"),
        ]), "s5lg")),
        row(
            step(panel("Пример", "<p>Например, устройство LSR2 могло бы назначить и передать метку <b>199</b> устройству LSR1, "
                                 "не дожидаясь прихода метки <b>231</b> от устройства LSR3.</p>" + ex, "rd")),
            step(panel(head_ico("i31a_tag.png", "Метки локальны", 44),
                       "<p>Так как метки имеют локальное значение, результат изменения режима не изменился бы.</p>"
                       '<p class="s5sm">199 используется на участке LSR1 → LSR2, а 231 — на участке LSR2 → LSR3. Числа могут '
                       "различаться для одного FEC.</p>", "gr")), cls="s5w80"),
    ]), sub=S31)

    slide("pptx 31 · Метод объявления меток", "bgk_28", TL, "".join([
        step(panel("2. Метод объявления меток",
                   "<p>Существует также два метода распределения меток — распределение от лежащего ниже по потоку <b>по "
                   "запросу</b> и <b>без запроса</b>.</p>" + row(
                       card("i31a_doc.png", "По запросу (Downstream on Demand, DoD)",
                            "<p>Привязка FEC → метка передаётся в ответ на Label Request.</p>"),
                       card("i31a_radio.png", "Без запроса (Downstream Unsolicited, DU)",
                            "<p>LSR объявляет привязки подходящим LDP-соседям без предварительного запроса.</p>")))),
        step(panel("", "<p>Для нашего случая это значит, что если бы устройство LSR2 обнаружило в своей таблице маршрутизации "
                       "запись о новой сети 132.100.0.0, оно могло бы назначить метку новому пути и передать ее устройству LSR1 "
                       "<b>без запроса</b>. Так как при этом устройство LSR2 не знает своего соседа выше по потоку (таблица "
                       "маршрутизации не говорит об этом), оно передает эту информацию <b>всем своим соседям</b> по сеансам "
                       "LDP.</p>", "or"), "s5w80"),
        step(panel(head_ico("i31a_sign.png", "Как выбирается путь?", 44),
                   "<p>В этом варианте работы протокола LDP устройства LSR могут получать альтернативные метки для пути к "
                   "некоторой сети; а выбор наилучшего пути осуществляется обычным для IP-маршрутизаторов (которыми устройства "
                   "LSR являются по совместительству) способом — на основании <b>наилучшей метрики</b>, выбираемой протоколом "
                   "маршрутизации.</p>", "gr"), "s5w80"),
    ]), sub=S31)

    slide("pptx 31 · Четыре режима", "bgk_28", TL, "".join([
        step(panel("", '<div class="m2big">Как видно из описания, существует два независимых параметра, которые определяют '
                   "вариант работы протокола LDP: <b>режим управления распределением меток</b> и <b>метод распределения "
                   "меток</b>. Так как каждый параметр имеет два значения, всего существует <b>четыре режима</b> работы "
                   "протокола LDP.</div>")),
        step(panel("Четыре возможных сочетания",
                   tb(["Управление", "По запросу — DoD", "Без запроса — DU"],
                      [["<b>Независимое</b>", "Independent + DoD",
                        'Independent + DU <span class="m2pill gr">Часто используется</span>'],
                       ["<b>Упорядоченное</b>", "Ordered + DoD", "Ordered + DU"]]), "tint"), "s5w80"),
        row(
            step(panel("", "<p>В рамках одного сеанса LDP должен поддерживаться только один из методов распределения меток — по "
                           "запросу или без запроса. В то же время в масштабах сети могут одновременно использоваться оба "
                           "метода.</p>", "gr")),
            step(panel("", "<p>Протокол LDP чаще всего работает в режиме <b>независимого управления</b> распределением меток "
                           "<b>без запроса</b>. Упорядоченное управление распределением меток требуется при прокладке путей LSP, "
                           "необходимых для инжиниринга трафика.</p>", "or")), cls="s5w80"),
        step(yl("i31a_gear.png", "<b>Ordered Control не задаёт маршрут TE.</b> Обычный LDP следует IP-маршрутам; для Traffic "
                                  "Engineering применяют отдельные механизмы."), "s5w80"),
    ]), sub=S31)


CSS = r"""
.s5col{display:flex;flex-direction:column;gap:clamp(8px,1.1vw,18px);min-width:0}
.s5col.s5ce{gap:4px;align-items:center;flex:none}
.s5ch{display:flex;align-items:center;gap:6px}
.s5ch>.step{display:flex;align-items:center;min-width:0}
.s5ch>.step:has(>.s5ln),.s5ch>.s5ln,.s5ch>.step:has(>.s5two){flex:1 1 0}
.s5ch>.step>.s5ln,.s5ch>.step>.s5two{flex:1 1 auto}
.s5ln{flex:1 1 0;min-width:44px;display:flex;flex-direction:column;align-items:stretch;text-align:center;color:#13306e}
.s5ln>span,.s5ln>small{font:700 clamp(12px,1vw,19px)/1.2 "Golos Text",sans-serif;padding:0 6px}
.s5ln>span{margin-bottom:5px}.s5ln>small{margin-top:5px;font-weight:600}
.s5ln b{font-weight:900}
.s5ln>i{display:block;height:4px;background:currentColor;position:relative;margin:0 14px 0 2px}
.s5ln>i::after{content:"";position:absolute;right:-14px;top:-7px;border-style:solid;border-width:9px 0 9px 15px;
 border-color:transparent transparent transparent currentColor}
.s5ln.l>i{margin:0 2px 0 14px}
.s5ln.l>i::after{right:auto;left:-14px;border-width:9px 15px 9px 0;border-color:transparent currentColor transparent transparent}
.s5ln.rd{color:#e2564a}.s5ln.gr{color:#1e9a5a}.s5ln.gy{color:#6b7280}
.s5ln.ds>i{background:repeating-linear-gradient(90deg,currentColor 0 9px,transparent 9px 15px)}
.s5ln .m2pk{font-size:clamp(13px,1.05vw,20px)}
.s5two{display:flex;flex-direction:column;gap:12px;min-width:0}
.s5two.s5wide{min-width:clamp(200px,24vw,460px)}
.s5tag{display:inline-block;background:#f6866b;color:#1d1d1d;border:2px solid #b8342a;border-radius:8px;padding:0 10px;
 font:700 clamp(13px,1.05vw,20px)/1.5 "Golos Text",sans-serif;white-space:nowrap}
.s5cl{display:inline-block;background:#dff1fd;border:3px solid #2a7fd4;border-radius:999px;padding:.3em .9em;flex:none;
 font:800 clamp(13px,1.1vw,21px)/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center;white-space:nowrap}
.s5cl.big{padding:.7em 1.2em;font-weight:600}
.s5cl b{font-weight:900;font-size:1.1em}
.s5stack{display:flex;flex-direction:column;gap:8px;align-items:flex-start}
.s5bar{background:#c6ebe4;border-radius:12px;padding:5px 14px;margin-top:8px;text-align:center;
 font:600 clamp(14px,1.2vw,23px)/1.35 "Golos Text",sans-serif;color:#13306e}
.s5bar b{font-weight:900}
.s5yl{background:#fde27a;border:3px solid #1f63c6;border-radius:14px;display:flex;align-items:center;gap:12px;padding:6px 16px;
 font:600 clamp(14px,1.15vw,22px)/1.35 "Golos Text",sans-serif;color:#13306e}
.s5yl b{font-weight:900}.s5yl .ico{flex:none}
.s5card{display:flex;gap:14px;align-items:center;background:rgba(214,236,251,.75);border-radius:14px;padding:8px 14px;margin-bottom:10px}
.s5card:last-child{margin-bottom:0}
.s5card .ico{flex:none;border-radius:12px}
.s5card p{margin:0}
.s5ct{font:900 clamp(15px,1.35vw,26px)/1.15 "Rubik",sans-serif;color:#13306e;margin-bottom:3px}
.s5hi{display:inline-flex}.s5hi .ico{border-radius:50%}
.s5stages{display:flex;gap:0}
.s5stages>.s5col{flex:1 1 0;padding:0 14px;border-left:2px solid #c9c2ac;gap:10px}
.s5stages>.s5col:first-child{border-left:0;padding-left:0}.s5stages>.s5col:last-child{padding-right:0}
.s5stg{display:flex;align-items:center;gap:10px;background:#c6ebe4;border-radius:999px;padding:3px 16px 3px 3px;
 font:900 clamp(14px,1.2vw,22px)/1.2 "Rubik",sans-serif;text-transform:uppercase;color:#13306e}
.s5stg .m2n{width:1.8em;height:1.8em;background:#f2694a;font-size:1em}
.s5dia{justify-content:center}
.s5pc{text-align:center;margin-top:4px}
.s5cap{text-align:center;font:700 clamp(12px,1vw,19px)/1.2 "Golos Text",sans-serif;color:#13306e;margin-bottom:4px}
.s5gbx{background:#e3f0ee;border-radius:12px;padding:6px 12px;text-align:center;
 font:500 clamp(13px,1.1vw,21px)/1.3 "Golos Text",sans-serif;color:#1d2a44}
.s5gbx.s5l{display:flex;gap:12px;align-items:center;text-align:left;background:#cdeedd;margin-top:8px;font-weight:600;color:#13306e}
.s5gbx .ico{flex:none}
.s5warn{display:flex;gap:12px;align-items:center;background:#fbefb6;border-radius:12px;padding:6px 12px;margin-top:8px;
 font:500 clamp(13px,1.1vw,21px)/1.3 "Golos Text",sans-serif;color:#13306e}
.s5warn>b{flex:none;width:1.8em;height:1.8em;border-radius:50%;background:#f2694a;color:#fff;display:grid;place-items:center;font-weight:900}
.s5flow{display:flex;align-items:center;gap:14px;background:rgba(253,248,234,.96);border:3px solid #1f63c6;border-radius:16px;
 padding:8px 18px;font:500 clamp(14px,1.15vw,22px)/1.25 "Golos Text",sans-serif;color:#1d2a44}
.s5flow b{font-weight:900;color:#13306e}
.s5fa{font:900 clamp(20px,1.8vw,34px)/1 sans-serif;color:#13306e}
.m2p .s5flow{background:none;border:0;padding:0;justify-content:space-between}
.s5it{display:flex;flex-direction:column;align-items:center;gap:4px}
.s5it span{background:#c6ebe4;border-radius:10px;padding:2px 12px;font:600 clamp(13px,1.1vw,21px)/1.3 "Golos Text",sans-serif;color:#13306e}
.s5w78{margin-right:22%}.s5w66{margin-right:34%}.s5w80{margin-right:20%}.s5w84{margin-right:16%}
.s5mid{display:flex;flex-direction:column;gap:clamp(8px,1vw,16px);margin:0 20% 0 18.5%}
.s5role{background:#bfe9e4;border-radius:10px;padding:2px 10px;text-align:center;
 font:600 clamp(12px,1vw,19px)/1.2 "Golos Text",sans-serif;color:#13306e}
.s5dir{flex:1;padding:0 12% 0 6%}
.s5top{align-items:flex-start}.s5top .s5ln{margin-top:20px}.s5top .s5cl{margin-top:6px}
.s5bord{align-self:stretch;border-left:3px dashed #13306e;padding-left:10px;font:700 clamp(12px,1vw,19px)/1.25 "Golos Text",sans-serif;
 color:#13306e;flex:none}
.s5ch>.step:has(>.s5bord){align-self:stretch}
.s5sm{font-size:.9em;border-top:2px solid #13306e;padding-top:6px;margin-top:6px!important}
.s5tb td.s5hl{background:#f6a08c!important;font-weight:800}
.s5tb td,.s5tb th{text-align:center}
.s5fmt{width:100%;border-collapse:collapse;font:600 clamp(13px,1.15vw,22px)/1.3 "Golos Text",sans-serif;color:#13306e;background:#fff}
.s5fmt td{border:2.5px solid #1d3f8a;padding:6px 10px;text-align:center}
.s5fmt tr:nth-child(odd) td{background:#d6ebfb}
.s5z{flex:1;padding-top:22px}
.s5s0{font:800 clamp(13px,1.1vw,21px)/1 "Golos Text",sans-serif;color:#13306e;align-self:flex-start}
.s5r29{display:flex;flex-direction:column;gap:clamp(8px,1vw,16px);margin-right:27%}
.s5l29{margin-left:19%}
.s5f13{flex:1.3 1 0}
.s5span{display:flex;align-items:center;gap:10px;margin:6px 8% 0 4%;font:900 clamp(14px,1.2vw,22px)/1 "Golos Text",sans-serif;color:#13306e}
.s5span i{flex:1;height:2px;background:#1d3f8a}
.s5r30{align-items:flex-start}
.s5r30>.s5scn{flex:1.7 1 0}
.s5r30>.s5rc{flex:1 1 0;margin-right:0}
.s5scn .scene .figwrap{max-height:none}
"""
CSS += r"""
.s5lg .m2b{font-size:clamp(15px,1.42vw,27px)}
.s5md .m2big{font-size:clamp(15px,1.45vw,28px)}
.s5ch>.step:has(>.m2nd),.s5ch>.step:has(>.s5col),.s5ch>.step:has(>.s5cl){flex:none}
.s5mid{margin:0 17.5% 0 17%}
.s5mid .m2b{font-size:clamp(13px,1.15vw,22px)}
.s5mid .m2h{font-size:clamp(15px,1.3vw,25px)}
.s5r27{display:flex;flex-direction:column;gap:clamp(8px,1vw,16px);margin-right:9%}
.s5c28{display:flex;flex-direction:column;gap:clamp(8px,1vw,14px)}
.s5c28 .m2b{font-size:clamp(13px,1.15vw,22px)}
.s5c28 .s5fmt td{padding:3px 10px}
.s5c28 .m2nd small{font-size:clamp(11px,.9vw,17px)}
.s5t29{font-size:clamp(14px,1.3vw,25px)}
.s5itg{justify-content:space-between}
.s5ith{font:900 clamp(15px,1.3vw,25px)/1.1 "Rubik",sans-serif;text-transform:uppercase}
.s5stages .m2b{font-size:clamp(13px,1.12vw,21px)}
"""
CSS += r"""
.s5g27{display:grid;grid-template-columns:auto minmax(0,1fr) auto 56px auto;align-items:center;gap:8px}
.s5g27>.step{display:block;min-width:0}
.s5g27>.step>.s5ln{min-width:0}
.s5lg .m2tbl{font-size:clamp(15px,1.35vw,26px)}
.s5lsp .m2nd strong{font-size:clamp(16px,1.45vw,28px)}
.s5r30>.s5scn{flex:1.45 1 0}
.s5l29 .m2big{font-size:clamp(16px,1.55vw,30px)}
"""
CSS += r"""
.s5z{flex:2.6 1 0!important;min-width:0}
.s5lm{align-items:center}.s5lm>.s5fmt{flex:1.6 1 0}
"""
CSS += r"""
.s5r29 .m2big{font-size:clamp(15px,1.45vw,28px)}
.s5r30>.s5scn{flex:1.32 1 0}
"""
