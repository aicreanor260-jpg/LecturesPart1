# -*- coding: utf-8 -*-
"""MPLS 2.9 v2 — pptx 13–19 (FEC, PHP, MPLS-метка, стек, Push/Swap/Pop, таблицы MPLS).
Текст pptx дословно (из _mp_s1.py), разнесён по смысловым блокам; заголовки блоков и схемы — из инфографик i13a…i19a."""
from _mp2_kit import slide, step, panel, row as _row, pk, node, arrow, ico


def row(*items):
    return _row(*items, cls="s3eq")

TF = "Класс эквивалентности <em>пересылки</em>"
TM = "<em>MPLS</em>-метка"
TT = "Таблицы <em>MPLS</em>"


# ---------------------------------------------------------------- мелкие блоки
def box(html, cls="", style=""):
    return '<div class="s3bx %s" style="%s">%s</div>' % (cls, style, html)


def tag(text):
    """Адрес пакета — бирка как в i13a."""
    return '<span class="s3tag">%s</span>' % text


def bar(cells, cls=""):
    """Горизонтальная полоса полей: [(текст, цвет, flex)]."""
    return '<div class="s3bar %s">%s</div>' % (cls, "".join(
        '<div style="background:%s;flex:%s">%s</div>' % (c, f, t) for t, c, f in cells))


def stack(cells, cls=""):
    """Стек меток (вершина сверху): [(текст, цвет)]."""
    return '<div class="s3st %s">%s</div>' % (cls, "".join('<b style="background:%s">%s</b>' % (c, t) for t, c in cells))


RED, BLU, YEL, WHT, GRN, TEAL = "#f7a99a", "#a8d2f8", "#fbd56a", "#fff", "#7fd6a0", "#a9e3d6"


def rt_op(name, op, img="i14a_rt.png"):
    return node(ico(img, 50), name, '<span class="m2pill or">%s</span>' % op)


# ---------------------------------------------------------------- pptx 13
def fec_chain():
    """Классификация на входном LER (i13a): адреса → LER → база FEC → проверка → FEC → FTN → метка → LSP."""
    a = arrow()
    pkts = '<div class="s3pkts">%s%s</div>' % (tag("192.0.2.10"), tag("192.0.2.20"))
    ler = node(ico("i13a_rt.png", 92), "LER", "Входной узел")
    cls = "".join([
        step(box(ico("i13a_db.png", 44) + "<span>База<br>классов FEC</span>")),
        step(a + box(ico("i13a_mg.png", 44) + "<span>Проверка<br>признаков<br>пакета</span>")),
        step(a + box("FEC:<br>192.0.2.0/24", "s3fec")),
        step(a + box("FTN", "s3ftn")),
        step(a + '<span class="m2flt">%s</span>' % pk(["100"])),
    ])
    zone = ('<div class="m2zone s3cz"><span class="m2zl">Классификация</span><div class="m2chain" style="align-items:center;'
            'justify-content:flex-start;gap:4px">%s</div></div>' % cls)
    lsp = step('<div class="s3lsp"><div class="m2cap">Выбранный LSP</div><div class="s3brk"></div><div class="m2chain" '
               'style="align-items:center;gap:2px">%s%s%s%s%s<b>…</b></div></div>' % (
                   ico("i13a_rts.png", 54), arrow(), ico("i13a_rts.png", 54), arrow(), ico("i13a_rts.png", 54)))
    return ('<div class="m2chain" style="align-items:center;gap:6px">%s%s%s%s%s</div>'
            '<div class="m2cap" style="margin-top:8px">LER определяет FEC и связывает его с путём LSP.</div>'
            % (step(pkts + a), step(ler), a, zone, '<div style="display:flex;align-items:center">%s%s</div>' % (a, lsp)))


def feat(img, html):
    return step('<div class="s3ft">%s<p>%s</p></div>' % (ico(img, 54), html))


def build_13():
    slide("pptx 13 · FEC", "bgk_25", "Класс эквивалентности пересылки <em>(FEC)</em>", "".join([
        row(
            step(panel("", '<div class="s3xl"><b>Класс эквивалентности пересылки (FEC)</b> — класс множества пакетов, имеющих '
                       "одинаковый признак для пересылки относительно текущего узла MPLS-домена. Все потоки, принадлежащие одному "
                       "классу (одному FEC), используют один LSP. Пакеты одного FEC пересылаются одинаково в сети MPLS.</div>"),
                 "s3w2"),
            step(panel("Простейший случай", '<div class="s3xl">В простейшем случае FEC — это <b>пакеты, адресованные одной '
                       "IP-подсети</b>.</div>", "gr tint"))),
        panel("Классификация на входном LER", fec_chain(), "tint", num="1"),
    ]), safe="sr", sub="Forwarding Equivalence Class")

    slide("pptx 13 · Признаки FEC", "bgk_25", "Класс эквивалентности пересылки <em>(FEC)</em>", "".join([
        step(panel("", '<div class="m2big">В LER существует <b>база данных классов FEC</b>; каждый класс описывается набором '
                   "элементов, а каждый элемент описывает признаки, на основании которых входящий пакет относят к тому или иному "
                   "классу. Классификация FEC может выполняться различными способами. Вот несколько примеров:</div>")),
        panel("По каким признакам выбирают FEC", '<div class="s3fts">%s</div>' % "".join([
            feat("i13a_c1.png", "<b>На основании IP-адреса назначения.</b> Это наиболее близкий к принципам работы IP-сетей "
                 "подход, который состоит в том, что для каждого префикса сети назначения, имеющегося в таблице LER-маршрутизации, "
                 "создается отдельный класс FEC. Протокол LDP, который мы далее рассмотрим, полностью автоматизирует процесс "
                 "создания классов FEC по этому способу."),
            feat("i13a_c4.png", "<b>В соответствии с требованиями инжиниринга трафика.</b> Классы выбираются таким образом, чтобы "
                 "добиться баланса загрузки каналов сети."),
            feat("i13a_c2.png", "<b>В соответствии с требованиями VPN.</b> Для конкретной виртуальной частной сети клиента "
                 "создается отдельный класс FEC."),
            feat("i13a_c5.png", "<b>По типам приложений.</b> Например, трафик IP-телефонии (RTP) составляет один класс FEC, а "
                 "веб-трафик — другой."),
            feat("i13a_c3.png", "<b>По интерфейсу</b>, с которого получен пакет."),
            feat("i13a_c6.png", "<b>По MAC-адресу назначения кадра</b>, если это кадр Ethernet."),
        ]), num="2"),
    ]), safe="sr", sub="Forwarding Equivalence Class")

    def ftn_row(fec, lab):
        return step('<div class="s3map">%s%s%s%s<span class="m2flt">%s</span></div>' % (
            box(fec, "s3fec", "min-width:13em"), arrow(), box("FTN", "s3ftn"), arrow(), pk([lab])))

    slide("pptx 13 · FTN", "bgk_25", "Класс эквивалентности пересылки <em>(FEC)</em>", "".join([
        step(panel("", '<div class="s3xl">Как видно из приведенных примеров, при классификации трафика в MPLS могут '
                   "использоваться признаки не только из заголовка IP-пакета, но и многие другие, включая информацию "
                   "<b>канального (MAC-адрес)</b> и <b>физического (интерфейс)</b> уровней.</div>")),
        row(
            step(panel('<span class="s3ftnb">FTN</span> FEC To Next Hop',
                       '<div class="s3xl">После принятия решения о принадлежности пакета к определенному классу FEC его нужно '
                       "связать с существующим путем LSP. Для этой операции LER использует таблицу <b>FTN (FEC To Next hop</b> — "
                       "отображение класса FEC на следующий хоп).</div>"
                       '<div class="m2cap" style="margin-top:10px">Связывает класс FEC со следующим хопом и операцией с меткой.</div>',
                       "or", num="3")),
            step(panel("Пример соответствия FEC и меток",
                       '<table class="m2tbl s3big"><tr><th>Признаки FEC</th><th>Метка</th></tr>'
                       "<tr><td>123.20.0.0/16; 195.14.0.0/16</td><td><b>106</b></td></tr>"
                       "<tr><td>194.20.0.0/24; eth1</td><td><b>107</b></td></tr></table>"
                       + ftn_row("123.20.0.0/16; 195.14.0.0/16", "106") + ftn_row("194.20.0.0/24; eth1", "107"),
                       "tint"))),
    ]), safe="sr", sub="Forwarding Equivalence Class")


# ---------------------------------------------------------------- pptx 14
def php_chain():
    """Пример i14a: один уровень меток, PHP на предпоследнем LSR, IP-поиск на выходном LER."""
    a = arrow()
    ipn = lambda t: node(ico("i14a_ip.png", 44), t)
    parts = [
        step(ipn("IP-пакет<br>(без метки)") + a),
        step(rt_op("Входной<br>LER", "Push") + a + '<span class="m2flt">%s</span>' % pk(["100"]) + a),
        step(rt_op("Транзитный<br>LSR", "Swap") + a + '<span class="m2flt">%s</span>' % pk(["200"]) + a),
        step(rt_op("Предпоследний<br>LSR", "Pop (PHP)") + a + '<span class="m2flt">%s</span>' % pk([]) + a),
        step(rt_op("Выходной<br>LER", "IP-поиск") + a + ipn("Следующая<br>IP-сеть")),
    ]
    return ('<div class="m2zone" style="padding-top:18px;margin-top:16px"><span class="m2zl">MPLS-домен</span>'
            '<div class="m2chain s3php">%s</div></div>' % "".join(parts))


def build_14():
    sub = "Назначение метки и удаление на предпоследнем хопе (PHP)"
    slide("pptx 14 · LER и LSR", "bgk_18", TF, "".join([
        step(panel("На входе в MPLS-домен", '<div class="s3xl">На основании таблицы <b>FTN</b> каждому входящему пакету '
                   "назначается соответствующая метка, после чего этот пакет становится неразличим в домене MPLS от других "
                   "пакетов того же класса FEC, все они продвигаются по одному и тому же пути внутри домена.</div>", num="1")),
        row(
            step(panel("", '<div class="s3ic">%s<div><div class="m2h">LER: классификация пакетов</div><div class="m2big">'
                       "Сложная настройка и конфигурирование выполняются <b>только в LER</b>,</div></div></div>"
                       % ico("i14a_ic1.png", 110), "tint")),
            step(panel("", '<div class="s3ic">%s<div><div class="m2h">LSR: продвижение по метке</div><div class="m2big">'
                       "а все промежуточные устройства LSR выполняют <b>простую работу</b>, продвигая пакет в соответствии с "
                       "техникой виртуального канала.</div></div></div>" % ico("i14a_ic2.png", 110), "tint"))),
        step(panel("", '<div class="s3xl"><b>Выходное устройство LER удаляет метку</b> и передает пакет в следующую сеть уже в '
                   "стандартной форме IP-пакета. Таким образом, технология <b>MPLS остается прозрачной</b> для остальных "
                   "IP-сетей.</div>", "gr")),
    ]), safe="sl sr", sub=sub)

    slide("pptx 14 · PHP", "bgk_18", TF, "".join([
        step(panel("PHP — Penultimate Hop Popping", '<div class="s3cols s3php-t">'
                   "<p>Обычно в MPLS-сетях используется усовершенствованный по сравнению с описанным алгоритм обработки "
                   "пакетов. Усовершенствование заключается в том, что <b>удаление метки выполняет не последнее на пути "
                   "устройство, а предпоследнее</b>.</p><p>Действительно, после того как предпоследнее устройство определит "
                   "на основе значения метки следующий хоп, метка в MPLS-кадре уже не нужна, так как последнее устройство, то "
                   "есть выходное устройство LER, будет продвигать пакет на основе значения IP-адреса.</p>"
                   "<p>Это небольшое изменение алгоритма продвижения кадра позволяет <b>сэкономить одну операцию</b> над "
                   "MPLS-кадром. В противном случае последнее вдоль пути устройство должно было бы удалить метку, а уже затем "
                   "выполнить просмотр таблицы IP-маршрутизации.</p><p>Эта техника получила название техники удаления метки "
                   "на предпоследнем хопе (<b>Penultimate Hop Popping, PHP</b>).</p></div>", "or", num="2")),
        panel("Пример: один уровень меток и обычная IP-передача на выходе", php_chain(), "tint"),
        row(
            step('<div class="m2note s3sm1">Без PHP метка снимается на выходном LER. Для внешних IP-сетей <b>MPLS остаётся '
                 "прозрачной</b>.</div>"),
            step('<div class="m2note s3sm1" style="background:#d6ebfb;border-color:#1f63c6">При стеке меток PHP удаляет '
                 "<b>верхнюю метку</b>; под ней может оставаться другая.</div>")),
    ]), safe="sl sr", sub=sub)


# ---------------------------------------------------------------- pptx 15
def build_15():
    slide("pptx 15 · MPLS-метка", "bgk_01", TM, "".join([
        step(panel("", '<div class="m2big"><b>MPLS-метка (MPLS-Label)</b> — короткий идентификатор фиксированной длины '
                   "(<b>20 бит</b>), значимый только локально. Метка определяет FEC, к которому принадлежит пакет. В некоторых "
                   "случаях, например при балансировке нагрузки, один FEC может быть сопоставлен с несколькими входящими метками. "
                   "Однако <b>каждая метка на устройстве представляет только один FEC</b>.</div>"
                   '<div class="s3hl">Значение метки: 20 бит.&nbsp; Весь MPLS-заголовок: 32 бита = 4 байта.</div>', num="1")),
        step(panel("Где расположен MPLS-заголовок",
                   '<div class="m2big" style="margin-bottom:12px">MPLS-метка передается вместе с IP-пакетом в составе '
                   "<b>4‑байтового MPLS-заголовка</b>. MPLS-заголовок располагается между заголовками канального и сетевого "
                   "уровней.</div>"
                   + bar([("Заголовок L2", BLU, "0 0 22%"), ("MPLS-заголовок • 4 байта", RED, "0 0 32%"),
                          ("IP-заголовок", TEAL, "0 0 21%"), ("Данные", "#fbe7a6", "1")], "s3pulse2")
                   + '<div class="s3brace" style="margin-left:22%;width:53%"><span>Между заголовками канального и сетевого '
                     "уровней</span></div>", "tint", num="2")),
    ]), safe="s3pad")

    def fld(name, col, html):
        return step('<div class="s3fd"><span class="s3tg" style="background:%s">%s</span><p>%s</p></div>' % (col, name, html))

    slide("pptx 15 · Формат заголовка", "bgk_01", TM, "".join([
        panel("Формат MPLS-заголовка",
              '<div class="s3brace s3top"><span>32 бита (4 байта)</span></div>'
              + bar([("Label", RED, "20"), ("TC", TEAL, "3"), ("S", YEL, "1"), ("TTL", BLU, "8")], "s3fmt")
              + bar([("20 бит", "transparent", "20"), ("3 бита", "transparent", "3"), ("1 бит", "transparent", "1"),
                     ("8 бит", "transparent", "8")], "s3bits"), "tint"),
        panel("", '<div class="s3fds">%s</div>' % "".join([
            fld("Label — 20 бит", RED, "<b>Label</b> — 20‑битное значение MPLS-метки — от 0 до 1&nbsp;048&nbsp;575;"),
            fld("TC — 3 бита", TEAL, "<b>TC</b> — 3‑битное поле, используемое для указания класса трафика и применения "
                "политик качества обслуживания при возникновении перегрузки;"),
            fld("S — 1 бит", YEL, "<b>S</b> — 1‑битное значение, указывающее на нижнюю часть стека меток. MPLS поддерживает "
                "вложение нескольких меток. Если поле S равно 1, метка находится в нижней части стека;"),
            fld("TTL — 8 бит", BLU, "<b>TTL</b> — время жизни (8 бит), роль и функция аналогичны полю TTL в IP‑пакетах."),
        ]) + step('<div class="m2cap s3line">MPLS поддерживает стек из нескольких меток; каждой соответствует отдельный '
                  "4-байтовый заголовок.</div>")),
    ]), safe="s3pad")


# ---------------------------------------------------------------- pptx 16
def build_16():
    stk = ('<div class="s3brace s3top" style="margin-left:22%;width:50%"><span>Стек MPLS-меток</span></div>'
           + bar([("Заголовок L2", BLU, "0 0 22%"), ("Верхняя метка", RED, "0 0 25%"), ("Нижняя метка", YEL, "0 0 25%"),
                  ("IP-пакет", WHT, "1")])
           + '<div class="s3sbit"><span style="left:34.5%">S = 0</span><span style="left:59.5%">S = 1</span></div>'
           + '<div class="s3ops"><b>↑</b> Push / Swap / Pop</div>')
    rng = lambda v, c, t: step('<div class="s3rng"><span style="background:%s">%s</span><p>%s</p></div>' % (c, v, t))
    slide("pptx 16 · Стек меток", "bgk_27", TM, "".join([
        step(panel("Стек меток: принцип LIFO",
                   '<div class="s3xl" style="margin-bottom:14px">MPLS-метки в стеке обрабатываются сверху стека по принципу '
                   "<b>LIFO (Last‑In, First‑Out)</b> (последняя добавленная метка обрабатывается первой).</div>" + stk, num="1")),
        panel("Диапазоны значений",
              '<div class="s3xl" style="margin-bottom:10px">Пространство всех значений MPLS-меток можно разделить на два '
              "диапазона:</div>"
              + rng("0–15", "#f2694a", "<b>0–15</b>: специальные служебные метки:")
              + rng("16–1 048 575", YEL, "<b>16–1048575</b>: метки для динамического выделения протоколами LDP и MP-BGP."),
              "tint", num="2"),
    ]), safe="sl s3padr")

    rows = [
        ["0", "IPv4 Explicit NULL", "Показывает, что метку нужно удалить, дальнейшая пересылка будет выполняться по IPv4."],
        ["1", "Router Alert", "Пакет требует обработки локальным ПО, аналогично опции Router Alert в IP."],
        ["2", "IPv6 Explicit NULL", "Показывает, что метку нужно удалить, дальнейшая пересылка будет выполняться по IPv6."],
        ["3", "Implicit NULL", "Указывает предпоследнему LSR удалить метку перед отправкой трафика на Egress-LER."],
        ["4–13", "Reserved", "Зарезервировано."],
        ["14", "OAM Router Alert", "Для пакетов OAM (мониторинг LSP)."],
        ["15", "Reserved", "Зарезервировано."],
        ["16–1048575", "Dynamic assignment", "Диапазон меток для динамического выделения протоколами LDP и MP-BGP."]]
    tb = '<table class="m2tbl s3big s3vt"><tr><th>Значение метки</th><th>Название</th><th>Назначение</th></tr>%s</table>' % "".join(
        "<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>" % tuple(r) for r in rows)
    slide("pptx 16 · Таблица значений", "bgk_27", TM, panel("Таблица значений MPLS-меток", tb, num="3"), safe="sl s3padr")


# ---------------------------------------------------------------- pptx 17
def build_17():
    def card(head, before, after, txt, note, extra=""):
        return step(panel(head, '<div class="s3ba s3stk"><div class="s3col"><span class="m2pill bl">До</span>%s</div>'
                          '<span class="m2ar" style="margin:0 0 30px">→</span><div class="s3col"><span class="m2pill bl">После</span>%s</div>%s</div>'
                          '<p class="s3ct">%s</p><div class="s3cn">%s</div>' % (stack(before), stack(after, "s3drop"), extra, txt, note),
                          "s3card"))

    slide("pptx 17 · Push, Swap, Pop", "bgk_08", TM, "".join([
        step(panel("", '<div class="m2big">Над метками выполняются следующие операции, задаваемые в <b>поле действий таблицы '
                   "продвижения</b>:</div>")),
        row(
            card("Push — добавить", [("50", BLU), ("IP", WHT)], [("100", RED), ("50", BLU), ("IP", WHT)],
                 "<b>Push</b> — поместить метку в стек. В случае пустого стека эта операция означает простое присвоение метки "
                 "пакету. Если же в стеке уже имеются метки, в результате этой операции новая метка сдвигает «старые» в глубь "
                 "стека, сама оказываясь на вершине.",
                 'Пустой стек: IP → [<span style="color:#e2332a">100</span> | IP]'),
            card("Swap — заменить", [("100", RED), ("50", BLU), ("IP", WHT)], [("200", YEL), ("50", BLU), ("IP", WHT)],
                 "<b>Swap</b> — заменить текущую метку новой.", "Глубина стека сохраняется."),
            card("Pop — снять", [("200", YEL), ("50", BLU), ("IP", WHT)], [("50", BLU), ("IP", WHT)],
                 "<b>Pop</b> — выталкивание (удаление) верхней метки, в результате все остальные метки стека поднимаются на "
                 "один уровень.", "Если меток больше нет — открыт IP-пакет.",
                 '<span class="s3fly">%s</span>' % stack([("200", YEL)]))),
        step('<div class="m2p s3sum"><div>Push: +1 метка <i>•</i> Swap: замена верхней <i>•</i> Pop: −1 метка</div>'
             "<small>Вершина стека — метка, обрабатываемая первой.</small></div>"),
    ]), safe="sr", sub="Операции над стеком меток: Push, Swap и Pop")


# ---------------------------------------------------------------- pptx 18
def build_18():
    rt = lambda: ico("i18a_rt.png", 56)
    ldp = ('<div class="m2chain s3net">%s<span class="s3ex">⇄</span>%s<span class="s3ex">⇄</span>%s</div>'
           '<div class="m2cap">Обмен соответствиями FEC ↔ метка</div>' % (rt(), rt(), rt()))
    rsvp = ('<div class="s3rsvp"><span class="s3lspl">LSP (заданный путь)</span><span class="s3bw">%s Требуемая полоса '
            'пропускания</span></div><div class="m2chain s3net s3te">%s<span class="s3ra">→</span>%s<span class="s3ra">→</span>%s</div>'
            '<div class="m2cap">Сигнализация выбранного LSP</div>' % (ico("i18a_g.png", 30, style="display:inline;vertical-align:middle"),
                                                                     rt(), rt(), rt()))
    res = '<div class="m2chain" style="align-items:center;justify-content:center;gap:28px">%s%s%s%s%s</div>' % (
        step(node(ico("i18a_docs.png", 56), "Служебный обмен")), arrow(),
        step(node(ico("i18a_db.png", 56), "База меток (LIB)")), arrow(),
        step(node(ico("i18a_tb.png", 56), "Таблица продвижения (LFIB)")))
    slide("pptx 18 · Сигнальные протоколы", "bgk_23", TT, "".join([
        step(panel("", '<div class="m2big">Рассматриваемые таблицы для каждого устройства LSR формируются <b>сигнальным '
                   "протоколом</b>. В MPLS используется два различных сигнальных протокола: протокол распределения меток "
                   "(<b>Label Distribution Protocol, LDP</b>) и модификация уже знакомого нам протокола резервирования ресурсов "
                   "<b>RSVP</b>.</div>")),
        row(
            step(panel('LDP <span class="m2pill gr">Протокол распределения меток</span>',
                       '<p class="s3sm">Label Distribution Protocol</p>' + ldp, "gr", num="1")),
            step(panel('RSVP-TE <span class="m2pill or">RSVP с расширениями для MPLS TE</span>',
                       '<p class="s3sm">Resource Reservation Protocol — Traffic Engineering</p>' + rsvp, "or", num="2"))),
        panel("Результат на LSR", res + '<div class="m2cap" style="margin-top:6px">На основе полученных меток и маршрутов '
              "формируются записи для пересылки пакетов.</div>", "tint"),
    ]), safe="s3r18", sub="Сигнальные протоколы и формирование таблиц")


# ---------------------------------------------------------------- pptx 19
def build_19():
    tb = ('<table class="m2tbl s3big s3ft19"><tr><th>Входной интерфейс</th><th>Метка</th><th>Следующий хоп</th><th>Действия</th></tr>'
          '<tr class="s3r1"><td>S0</td><td>245</td><td>S1</td><td>256</td></tr>'
          '<tr class="s3r2"><td>S0</td><td>27</td><td>S2</td><td>45</td></tr>'
          "<tr><td>...</td><td>...</td><td>...</td><td>...</td></tr></table>")

    def ex(cls, title, a, b, si, so, txt):
        return step(panel(title, '<div class="m2chain s3ex19" style="align-items:center;justify-content:center;gap:10px">'
                          '%s%s<div class="m2nd"><span class="m2pill %s">Swap</span>%s</div>%s%s</div><p class="s3q">%s</p>' % (
                              node(pk([a], cls), si), arrow(), "or" if cls == "s3o" else "gr", ico("i19a_rt.png", 62), arrow(),
                              node('<span class="m2flt">%s</span>' % pk([b], cls), so), txt), "tint"))

    slide("pptx 19 · Таблица продвижения", "bgk_09", TT, "".join([
        step(panel("", '<div class="m2big"><b>Таблица продвижения MPLS определяет, куда передать пакет с полученной меткой и '
                   "какое действие выполнить над этой меткой.</b> Согласованные записи на нескольких маршрутизаторах образуют "
                   "путь через MPLS-сеть.</div>")),
        step(panel("Упрощённая таблица продвижения", tb, num="1")),
        '<div class="s3sub">Как читаются строки</div>',
        row(
            ex("s3o", "1. Заменить 245 на 256 и отправить через S1", "245", "256", "S0", "S1",
               "Первая строка означает: <b>«Если на интерфейс S0 поступил пакет с меткой 245, заменить её на 256 и отправить "
               "пакет через S1»</b>."),
            ex("s3g", "2. Заменить 27 на 45 и отправить через S2", "27", "45", "S0", "S2",
               "Вторая строка: <b>«Если на интерфейс S0 поступил пакет с меткой 27, заменить её на 45 и отправить через "
               "S2»</b>.")),
    ]), safe="sr")

    op = lambda img, n, t, c: '<div class="s3op" style="background:%s">%s<div><b>%s —</b><br>%s</div></div>' % (c, ico(img, 84), n, t)
    slide("pptx 19 · Поле действий", "bgk_09", TT, "".join([
        step(panel("Упрощённая таблица", '<div class="s3xl">В этой упрощённой таблице:</div><div class="s3xl">• <b>«Следующий хоп»</b> '
                   "обозначает выходной интерфейс.</div><div class=\"s3xl\">• <b>«Действие»</b> содержит новое значение "
                   "метки, то есть подразумевает операцию <b>Swap — замену метки</b>.</div>", num="1")),
        step(panel("Поле действий описывает операцию, а не только число",
                   '<div class="s3xl">Но действие может заключаться и в <b>добавлении метки — Push</b>, или <b>снятии верхней '
                   "метки — Pop</b>. Поэтому поле действий в общем случае описывает операцию, а не только новое число.</div>"
                   '<div class="m2row s3ops3" style="margin-top:16px">%s%s%s</div>' % (
                       op("i19a_p1.png", "Push", "добавить метку в стек", "#fbe0d6"),
                       op("i19a_p2.png", "Swap", "заменить верхнюю метку", "#d9f0e4"),
                       op("i19a_p3.png", "Pop", "снять верхнюю метку", "#dbeaf8"))
                   + '<div class="m2cap" style="margin-top:14px;font-size:clamp(15px,1.4vw,27px)">В общем случае запись содержит '
                     "операцию и необходимые параметры: например, <b>Swap 256</b>.</div>", "or", num="2")),
    ]), safe="sr s3pr19")


def build():
    build_13()
    build_14()
    build_15()
    build_16()
    build_17()
    build_18()
    build_19()


CSS = r"""
.m2in.s3pad{padding-left:clamp(120px,13vw,250px)!important;padding-right:clamp(150px,19vw,360px)!important}
.m2in.s3padr{padding-right:clamp(130px,15vw,290px)!important}
.m2in.s3pr19{padding-right:clamp(140px,17vw,330px)!important}
.s3sub{font:900 clamp(17px,1.55vw,30px)/1.1 "Rubik",sans-serif;color:#fff;text-transform:uppercase;text-shadow:0 2px 0 #1550a8,0 3px 8px rgba(10,40,90,.5);margin-bottom:-4px}
.m2in.s3r18{padding-right:clamp(150px,21vw,400px)!important}
.m2row>.s3w2{flex:2 1 0}
.s3bx{display:flex;align-items:center;gap:6px;border:2px solid #1d3f8a;border-radius:8px;background:#fff;padding:8px 10px;
 font:700 clamp(13px,1.2vw,23px)/1.15 "Golos Text",sans-serif;color:#13306e;text-align:center;justify-content:center;min-height:3.6em}
.s3bx .ico{flex:none}
.s3bx.s3fec{background:#f7a99a}.s3bx.s3ftn{background:#8cc8f0;font-size:clamp(15px,1.3vw,25px);font-weight:900}
.s3tag{display:block;margin:4px 0;border:2px solid #1d3f8a;border-left:8px solid #8cbde6;border-radius:3px;background:#fff;
 font:600 clamp(14px,1.25vw,24px)/1.8 "Golos Text",sans-serif;color:#13306e;padding:0 10px;white-space:nowrap}
.s3pkts{display:flex;flex-direction:column}
.m2chain>.step:has(.s3pkts){display:flex;align-items:center}
.s3cz{padding:26px 8px 16px;flex:0 1 auto}
.s3cz .s3bx{padding:6px 8px}
.s3cz .m2chain>.step{align-items:center}
.s3lsp{display:flex;flex-direction:column;align-items:stretch}
.s3lsp .s3brk{height:8px;border:2px solid #1d3f8a;border-bottom:0;border-radius:6px 6px 0 0;margin:2px 4px 4px}
.s3lsp b{font:900 22px/1 sans-serif;color:#13306e}
.s3lsp .m2ar{margin-top:0;font-size:clamp(14px,1.2vw,22px)}
.s3fts{display:grid;grid-template-columns:1fr 1fr;gap:12px 26px}
.s3ft{display:flex;gap:12px;align-items:flex-start}
.s3ft p{margin:0;font:500 clamp(15px,1.35vw,26px)/1.35 "Golos Text",sans-serif}
.s3ft .ico{flex:none}
.s3ftnb{display:inline-block;background:#2a78d0;color:#fff;border-radius:8px;padding:0 12px;text-transform:none}
.s3map{display:flex;align-items:center;gap:8px;margin-top:16px}
.s3map .s3bx{font-size:clamp(14px,1.3vw,25px);min-height:0}
.s3map .m2ar,.s3php .m2ar,.s3cz .m2ar,.s3ex19 .m2ar{margin-top:0}
.m2tbl.s3big{font-size:clamp(15px,1.4vw,27px)}
.m2tbl.s3big td,.m2tbl.s3big th{padding:9px 12px}
.s3xl{font:600 clamp(18px,1.75vw,34px)/1.4 "Golos Text",sans-serif}.s3xl b{color:#123a7a;font-weight:800}
.s3cols{columns:2;column-gap:32px}
.s3php-t p{font:500 clamp(14px,1.22vw,23px)/1.38 "Golos Text",sans-serif;margin:0 0 .35em!important}
.s3php-t b{color:#123a7a;font-weight:800}
.m2note.s3sm1{font-size:clamp(12px,1.02vw,19px);padding:5px 10px}.s3cols p{break-inside:avoid-column}
.s3php{align-items:center;justify-content:space-between}
.s3php .m2nd strong{font-size:clamp(13px,1.1vw,21px);white-space:nowrap}
.s3php .m2nd small{margin-top:4px}
.s3ic{display:flex;gap:16px;align-items:flex-start}.s3ic .ico{flex:none}
.s3hl{margin-top:12px;background:#fbc0b0;border-radius:10px;padding:6px 16px;font:800 clamp(15px,1.4vw,27px)/1.4 "Golos Text",sans-serif;color:#13306e}
.s3bar{display:flex;border:3px solid #1d3f8a;border-radius:10px;overflow:hidden}
.s3bar>div{padding:10px 6px;text-align:center;font:800 clamp(14px,1.3vw,25px)/1.2 "Golos Text",sans-serif;color:#13306e;
 border-right:2px solid #1d3f8a;min-width:0}
.s3bar>div:last-child{border-right:0}
.s3bar.s3fmt>div{padding:20px 4px;font-size:clamp(18px,2vw,38px)}
.s3bar.s3bits{border:0;margin-top:4px}.s3bar.s3bits>div{border:0;padding:0;font-weight:700;white-space:nowrap;overflow:visible}
.s3brace{position:relative;height:16px;border:2px solid #1d3f8a;border-top:0;margin-top:4px;text-align:center}
.s3brace>span{position:relative;top:6px;background:rgba(214,236,251,1);padding:0 12px;font:700 clamp(13px,1.15vw,22px)/1.2 "Golos Text",sans-serif;color:#13306e}
.s3brace.s3top{border-top:2px solid #1d3f8a;border-bottom:0;margin:6px 0 6px}
.s3brace.s3top>span{top:-14px}
.m2p:not(.tint) .s3brace>span{background:#fdf8ea}
.s3fds{display:grid;grid-template-columns:1fr 1fr;gap:12px 28px}
.s3fd p{margin:4px 0 0;font:500 clamp(16px,1.5vw,29px)/1.4 "Golos Text",sans-serif}
.s3tg{display:inline-block;border-radius:10px;padding:2px 14px;font:800 clamp(16px,1.5vw,29px)/1.4 "Golos Text",sans-serif;color:#13306e}
.s3line{border-top:2px solid #1d3f8a;margin-top:12px;padding-top:8px}
.s3sbit{position:relative;height:1.6em;font:700 clamp(14px,1.2vw,23px)/1.6 "Golos Text",sans-serif;color:#13306e}
.s3sbit>span{position:absolute;transform:translateX(-50%)}
.s3ops{margin-left:22%;font:800 clamp(15px,1.3vw,25px)/1.2 "Golos Text",sans-serif;color:#13306e}
.s3ops b{font-size:1.4em;color:#1d3f8a;margin-right:6px}
.s3rng{display:flex;align-items:center;gap:16px;background:#ccefea;border-radius:14px;padding:8px 14px;margin-top:8px}
.s3rng>span{flex:none;border-radius:10px;padding:4px 18px;font:900 clamp(17px,1.6vw,30px)/1.3 "Golos Text",sans-serif;color:#1d1d1d}
.s3rng p{margin:0;font:600 clamp(15px,1.4vw,26px)/1.35 "Golos Text",sans-serif}
.m2tbl.s3vt td:first-child,.m2tbl.s3vt th:first-child{text-align:center;white-space:nowrap}
.m2tbl.s3vt td{padding:5px 10px}
.s3card .m2h{justify-content:center;background:#ccefea;border-radius:14px;padding:5px}
.s3ba{display:flex;justify-content:space-around;align-items:flex-end;gap:10px}
.s3stk{margin:2px 0 4px;position:relative;align-items:flex-end}
.s3col{display:flex;flex-direction:column;align-items:center;justify-content:space-between;gap:8px;height:calc(3 * clamp(16px,1.5vw,29px) * 1.6 + 2.6em + 22px)}
.s3st{display:inline-flex;flex-direction:column;border:3px solid #1d3f8a;border-radius:8px;overflow:hidden;min-width:4.2em;
 box-shadow:0 6px 0 rgba(21,80,168,.18)}
.s3st b{display:block;text-align:center;font:800 clamp(16px,1.5vw,29px)/1.6 "Golos Text",sans-serif;color:#13306e;border-top:2px solid #1d3f8a}
.s3st b:first-child{border-top:0}
.s3fly{position:absolute;right:-6px;top:38px;animation:s3up 2.4s ease-in-out infinite}
@keyframes s3up{50%{transform:translateY(-6px) rotate(-4deg)}}
.s3ct{margin:4px 0 6px;text-align:center;font:500 clamp(14px,1.2vw,23px)/1.3 "Golos Text",sans-serif}
.s3cn{background:#d6f3e0;border-radius:12px;padding:4px 10px;text-align:center;font:700 clamp(13px,1.1vw,21px)/1.4 "Golos Text",sans-serif;color:#13306e}
.s3card{height:100%;box-sizing:border-box;display:flex;flex-direction:column}
.s3card .m2b{flex:1;display:flex;flex-direction:column}.s3card .s3cn{margin-top:auto}
.m2row.s3eq>.step{display:flex;flex-direction:column}.m2row.s3eq>.step>.m2p{flex:1}
.s3sum{text-align:center;padding:8px 16px}
.s3sum>div{font:900 clamp(18px,1.8vw,34px)/1.3 "Golos Text",sans-serif;color:#13306e}
.s3sum i{font-style:normal;color:#f29a2e;margin:0 .4em}
.s3sum small{font:500 clamp(14px,1.2vw,23px)/1.3 "Golos Text",sans-serif}
.s3sm{margin:-4px 0 6px!important;font:600 clamp(13px,1.05vw,20px)/1.2 "Golos Text",sans-serif;color:#33476e}
.s3net{align-items:center;justify-content:center;gap:12px;margin:6px 0}
.s3ex{font:900 clamp(24px,2.4vw,46px)/1 sans-serif;color:#1f8a6a}
.s3ra{font:900 clamp(24px,2.4vw,46px)/1 sans-serif;color:#e2332a}
.s3te{background:linear-gradient(90deg,rgba(242,105,74,.12),rgba(242,105,74,.38));border-radius:12px;padding:4px 10px}
.s3rsvp{display:flex;justify-content:center;align-items:center;gap:18px;flex-wrap:wrap}
.s3lspl{background:#f9b8a8;border-radius:8px;padding:2px 12px;font:700 clamp(13px,1.1vw,21px)/1.5 "Golos Text",sans-serif;color:#13306e}
.s3bw{font:700 clamp(12px,1vw,19px)/1.2 "Golos Text",sans-serif;color:#13306e}
.m2pk.s3o b{background:#f7845f}.m2pk.s3g b{background:#7fd6a0}
.m2tbl.s3ft19 td{font-weight:700}
.m2tbl.s3big.s3ft19 td,.m2tbl.s3big.s3ft19 th{padding:4px 14px}
.m2tbl.s3ft19 tr.s3r1 td{background:#fbd6cc}.m2tbl.s3ft19 tr.s3r2 td{background:#cdeedd}
.s3q{margin:8px 0 0!important;font:500 clamp(15px,1.35vw,26px)/1.35 "Golos Text",sans-serif}
.s3ex19 .m2nd .m2pill{margin-bottom:4px}
.s3op{display:flex;align-items:center;gap:16px;border-radius:14px;padding:16px 20px;font:500 clamp(15px,1.4vw,27px)/1.3 "Golos Text",sans-serif;color:#13306e}
.s3op b{font:900 clamp(19px,1.9vw,36px)/1.2 "Golos Text",sans-serif}
.s3op .ico{flex:none}
"""
