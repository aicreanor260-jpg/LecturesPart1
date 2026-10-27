# -*- coding: utf-8 -*-
"""MPLS 2.9 v2 — pptx 20–24: продвижение MPLS-кадра, домены, LSP3. Текст pptx дословно (из _mp_s1.py),
заголовки блоков, подписи и выводы — из инфографик автора i20a…i24a."""
from _mp2_kit import slide, step, panel, row, node, arrow, ico
from _mp_s1 import two_domains
from _mp_fig import sc

TP = "Продвижение <em>MPLS-кадра</em>"
IP = ("IP", "w")


# ---------------------------------------------------------------- мелкие блоки
def spk(cells, cls=""):
    """Пакет со стеком меток: верхняя метка слева; цвет ячейки: c — LSP1/LSP2, r — LSP3, t — транспортная, w — IP."""
    return '<span class="s4pk %s">%s</span>' % (cls, "".join('<b class="%s">%s</b>' % (c, t) for t, c in cells))


def hop(name, op="", img="i20a_rt.png", h=56):
    return node(ico(img, h), name, op)


def fly(html, back=False):
    a = '<span class="m2ar">←</span>' if back else arrow()
    return a + '<span class="m2flt">%s</span>' % html + a


def chain(parts, rev=False, style=""):
    """Каждый кусок — шаг: узел + стрелка + пакет за ним."""
    return '<div class="m2chain s4ch %s" style="%s">%s</div>' % ("s4rev" if rev else "", style, "".join(step(p) for p in parts))


def tbl(head, rows):
    h = "".join("<th>%s</th>" % x for x in head)
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % x for x in r) for r in rows)
    return '<table class="m2tbl s4tb"><tr>%s</tr>%s</table>' % (h, b)


def hd_ico(img, text):
    return '<span class="s4hi">%s</span>%s' % (ico(img, 40), text)


def bulb(text, img="i21a_bulb.png"):
    return '<div class="s4y">%s<span>%s</span></div>' % (ico(img, 52), text)


LTH = ["Устройство", "Входной интерфейс", "Метка", "Следующий хоп", "Действия"]


def build():
    # ================================================================ pptx 20
    slide("pptx 20 · Одноуровневый путь", "bgk_20", TP, "".join([
        row(
            step(panel("", '<div class="m2big">Продвижение MPLS-кадра всегда происходит на основе метки, находящейся в данный '
                           "момент на <b>вершине стека</b>. Рассмотрим сначала продвижение MPLS-кадра по одноуровневому пути в "
                           "MPLS-сети.</div>", num="")),
            step(panel('Одноуровневый LSP',
                       '<p><span class="m2pill gr">одна MPLS-метка, без вложенных путей</span></p><p><b>Одноуровневый путь MPLS</b> — это путь без вложенности: пакет передаётся с одной MPLS-меткой, а '
                       'не со стеком из нескольких меток.</p>', "gr")), cls="s4top"),
        step(panel("", '<div class="m2big" style="margin-bottom:8px">Сеть состоит из <b>трех MPLS-доменов</b>. На рисунке '
                       "показаны путь <b>LSP1</b> в домене 1 и путь <b>LSP2</b> в домене 2.</div>"
                   + '<div class="s4sc">%s</div>' % sc(two_domains(False), [
                       "IP-пакет (вход) приходит на LER1", "LER1: Push 256", "LSR1: 256 → 272", "LSR2: 272 → 132",
                       "LSR3 (предпоследний): Pop", "LER2 продвигает по IP-адресу → LER3", "LER3: Push 188 (LSP2)",
                       "LSR4: 188 → 112", "LSR5: 112 → 101", "LSR6: Pop → LER4, IP-пакет (выход)"], "0 0 1200 520"),
                   "tint")),
    ]))

    rt = "i20a_rt.png"
    slide("pptx 20 · LSP1 в домене 1", "bgk_20", TP, "".join([
        step(panel("", "<p>LSP1 соединяет устройства <b>LER1</b> и <b>LER2</b>, проходя через устройства LSR1, LSR2 и LSR3. Пусть "
                       "начальной меткой пути LSP1 является метка <b>256</b>, которая была присвоена пакету пограничным "
                       "устройством LER1. На основании этой метки пакет поступает на устройство LSR1, которое по своей таблице "
                       "продвижения определяет новое значение метки пакета (<b>272</b>) и переправляет его на вход LSR2.</p>"
                       "<p>Устройство LSR2, действуя аналогично, присваивает пакету новое значение метки (<b>132</b>) и передает "
                       "его на вход LSR3. Устройство LSR3, будучи предпоследним устройством в пути LSP1, выполняет операцию "
                       "<b>Pop</b> и удаляет метку из стека. Устройство LER2 продвигает пакет уже на основании <b>IP-адреса</b>.</p>")),
        panel("", '<div class="m2zone"><span class="m2zl">MPLS-домен 1 • LSP1</span>' + chain([
            node(ico("i03a_ip.png", 44), "IP-пакет", "(вход)") + arrow(),
            hop("LER1", "Push 256", rt) + fly(spk([("256", "r")])),
            hop("LSR1", "Swap 272", rt) + fly(spk([("272", "r")])),
            hop("LSR2", "Swap 132", rt) + fly(spk([("132", "r")])),
            hop("LSR3", "Pop", rt) + fly(spk([IP])),
            hop("LER2", "IP-пересылка", rt)]) + "</div>", "tint"),
        row(
            step(panel("", tbl(LTH, [["LER1 · добавление метки", "S0", "IP / FEC", "S1", "Push 256"],
                                     ["LSR1", "S0", "256", "S1", "Swap 272"], ["LSR2", "S0", "272", "S1", "Swap 132"],
                                     ["LSR3", "S0", "132", "S1", "Pop"]])
                       + '<div class="m2cap s4l">S0 — входной интерфейс; S1 — выходной интерфейс. Обозначения условные.</div>')),
            step(panel(hd_ico("i20a_tag.png", "Снятие метки на предпоследнем узле"),
                       "<p>LSR3 и LSR6 выполняют Pop. LER2 и LER4 получают IP-пакет без метки.</p>", "or")), cls="s4r21"),
    ]))

    slide("pptx 20 · Сшивание путей", "bgk_20", TP, "".join([
        step(panel("", "<p>На рисунке также показан путь <b>LSP2</b> в домене 2. Он соединяет устройства LER3 и LER4, проходя "
                       "через устройства LSR4, LSR5 и LSR6, и определяется последовательностью меток <b>188,112,101</b>. Для "
                       "того чтобы IP-пакеты могли передаваться на основе техники MPLS не только внутри каждого домена, но и "
                       "между доменами (например, между устройствами LER1 и LER4), существует <b>два принципиально разных "
                       "решения</b>.</p>")),
        panel("", '<div class="m2zone" style="background:rgba(205,238,228,.9)"><span class="m2zl" style="background:#cdeee4">'
                  "MPLS-домен 2 • LSP2</span>" + chain([
                      '<span class="s4in">IP без метки<br>от LER2 ↓</span>' + hop("LER3", "Push 188", rt) + fly(spk([("188", "r")]), True),
                      hop("LSR4", "Swap 112", rt) + fly(spk([("112", "r")]), True),
                      hop("LSR5", "Swap 101", rt) + fly(spk([("101", "r")]), True),
                      hop("LSR6", "Pop", rt) + fly(spk([IP]), True),
                      hop("LER4", "IP-пересылка", rt) + '<span class="m2ar">←</span>'
                      + node(ico("i03a_ip.png", 44), "IP-пакет", "(выход)")], rev=True) + "</div>", "tint"),
        row(
            step(panel(hd_ico("i20a_ch.png", "Между доменами: сшивание LSP"),
                       "<p><b>Первое решение</b> состоит в том, что между LER1 и LER4 устанавливается одноуровневый путь "
                       "коммутации по меткам, соединяющий пути LSP1 и LSP2 (которые в этом случае становятся одним путем). Это "
                       "простое, на первый взгляд, решение, называемое <b>сшиванием путей LSP</b>, плохо работает в том случае, "
                       "когда MPLS-домены принадлежат разным поставщикам услуг, не позволяя им действовать независимо друг от "
                       "друга.</p>", "rd")),
            step(panel("", tbl(LTH, [["LER3 · добавление метки", "S0", "IP / FEC", "S1", "Push 188"],
                                     ["LSR4", "S0", "188", "S1", "Swap 112"], ["LSR5", "S0", "112", "S1", "Swap 101"],
                                     ["LSR6", "S0", "101", "S1", "Pop"]])
                       + '<div class="m2cap s4l">LER2 и LER4 получают IP-пакет без метки и выполняют IP-пересылку.<br>'
                         "Показаны отдельные LSP1 и LSP2, без сшивания.</div>"))),
    ]))

    # ================================================================ pptx 21
    S21 = "Многоуровневый путь: LSP внутри LSP"
    sm = lambda img, n: "".join(ico(img, 54) + ('<span class="s4a">→</span>' if i < n - 1 else "") for i in range(n))
    lsp3 = ('<div class="s4l3">' + step('<div class="s4br"><span>LSP3</span></div>') +
            '<div class="m2chain" style="align-items:center;gap:8px">'
            + node(ico("i21a_rt.png", 84), "LER1") + '<span class="s4a g">→</span>'
            + '<div class="m2zone s4z g"><span class="m2zl">LSP1 — MPLS-домен 1</span>%s</div>' % sm("i21a_rg.png", 3)
            + '<span class="s4a g">→</span>' + node(ico("i21a_rt.png", 84), "LER2") + '<span class="s4ln"></span>'
            + node(ico("i21a_rt.png", 84), "LER3") + '<span class="s4a">→</span>'
            + '<div class="m2zone s4z b"><span class="m2zl">LSP2 — MPLS-домен 2</span>%s</div>' % sm("i21a_rb.png", 3)
            + '<span class="s4a">→</span>' + node(ico("i21a_rt2.png", 84), "LER4") + "</div>"
            + step('<div class="m2cap">На уровне LSP3 внутренние LSR доменов скрыты: логические хопы — LER1 → LER2 → LER3 → '
                   "LER4.</div>") + "</div>")
    slide("pptx 21 · Многоуровневый путь", "bgk_14", TP, "".join([
        step(panel("", '<div class="m2big">Вторым более перспективным решением является применение <b>многоуровневого '
                       "подхода</b> к соединению двух MPLS-доменов, принадлежащих, возможно, разным поставщикам услуг.</div>")),
        step(panel("Многоуровневый путь MPLS", '<div class="m2big"><b>Многоуровневый путь MPLS — это передача пакета по '
                   "вложенным путям: один LSP проходит внутри другого LSP.</b> Для этого поверх уже имеющейся метки добавляют "
                   "ещё одну.</div>", "or", num="1")),
        panel("LSP3: логический путь между пограничными узлами", lsp3, "tint"),
    ]), safe="sr", sub=S21)

    items = ["Входной LER назначает метку LSP3.",
             "Для пересечения домена поверх неё добавляется транспортная метка локального LSP.",
             "Внутренние LSR обрабатывают только верхнюю метку.",
             "После снятия транспортной метки снова доступна метка LSP3."]
    stack = ('<div class="s4li">%s</div>' % "".join('<p><span class="m2n">%d</span>%s</p>' % (i + 1, s) for i, s in enumerate(items))
             + '<div class="s4bar m2flt"><b class="t">Транспортная<br>метка<i>S = 0</i></b><b class="r">Метка LSP3<i>S = 1</i></b>'
               '<b class="w">IP-пакет</b></div>')
    slide("pptx 21 · Два уровня пути", "bgk_14", TP, "".join([
        step(panel("Два уровня пути", '<div class="m2big">Для реализации второго подхода в нашем примере нужно создать путь '
                   "коммутации по меткам второго уровня (<b>LSP3</b>), соединяющий устройства LER1 и LER4. Этот путь определяет "
                   "последовательность хопов <b>между доменами</b>, а не между внутренними устройствами LSR каждого домена. "
                   "Так, LSP3 состоит из хопов <b>LER1 — LER2 — LER3 — LSR4</b>. В этом отношении многоуровневый подход MPLS "
                   "концептуально очень близок подходу протокола <b>BGP</b>, определяющего путь между автономными системами. "
                   "Рассмотрим более детально, как работает технология MPLS в случае путей коммутации по меткам двух "
                   "уровней.</div>", num="2")),
        row(
            step(panel("Как работает стек", stack, "tint")),
            step('<div class="s4col">%s%s</div>' % (
                panel("", "<p>LSP3 задаёт последовательность пограничных узлов. LSP1 и LSP2 обеспечивают передачу внутри "
                          "отдельных доменов.</p><p>Аналогия с BGP — разделение междоменного пути и внутренней топологии. Это "
                          "концептуальное сходство, а не тождество механизмов.</p>", "gr"),
                bulb("Продвижение всегда выполняется по текущей верхней метке стека.")))),
    ]), safe="sr", sub=S21)

    # ================================================================ pptx 22
    S22 = "Два пути на входе LER1 • замена верхней метки в LSR2"
    r2 = "i22a_rt.png"
    slide("pptx 22 · LER1: два пути", "bgk_04", TP, "".join([
        step(panel("", '<div class="m2big">В устройстве LER1 начинаются два пути — <b>LSP1</b> и <b>LSP3</b> (последний показан '
                       "на рисунке серым цветом), что обеспечивается соответствующей записью в таблице продвижения устройства "
                       "LER1.</div>")),
        panel("LSP1 переносит пакет с внутренней меткой LSP3",
              '<div class="m2zone" style="padding-top:18px"><span class="m2zl">MPLS-домен 1 • LSP1</span>' + chain([
                  spk([IP]) + arrow(),
                  hop("LER1", "Push 315; Push 256", r2, 50) + fly(spk([("256", "cy"), ("315", "r"), IP])),
                  hop("LSR1", "Swap 256 → 272", r2, 50) + fly(spk([("272", "cy"), ("315", "r"), IP])),
                  hop("LSR2", "Swap 272 → 132", r2, 50) + fly(spk([("132", "cy"), ("315", "r"), IP])),
                  hop("LSR3", "Pop 132", r2, 50) + fly(spk([("315", "r"), IP])),
                  hop("LER2", "Далее по LSP3", r2, 50)], style="align-items:center")
              + step('<div class="s4dash"><span>LSP3: LER1 → LER2 → LER3 → LER4</span></div>') + "</div>"
              + step('<div class="m2cap" style="margin-top:6px">Верхняя метка показана слева. Внутренняя метка 315 сохраняется '
                     "внутри домена 1.</div>"), "tint"),
        row(
            step(panel("Запись на LER1", tbl(["Вход", "Классификация", "Выход", "Действия"],
                                             [["S0", "IP / FEC", "S1", "Push 315; Push 256"]])
                       + '<div class="m2cap s4l">Порядок важен: 315 — внутренняя, 256 — верхняя.</div>', "or")),
            step('<div class="m2note s4n"><div>В LER1 начинаются два пути: внешний LSP1 и внутренний LSP3.<br>Сначала добавляется '
                 'метка %s, затем поверх неё — метка %s.</div></div>' % (spk([("315", "r")]), spk([("256", "cy")]))), cls="s4r21"),
    ]), sub=S22)

    slide("pptx 22 · LSR1 и LSR2", "bgk_04", TP, "".join([
        step(panel("", '<div class="m2big">Аналогичные действия выполняет устройство <b>LSR2</b>, которое заменяет метку меткой '
                       "<b>132</b> и отправляет кадр следующему по пути устройству LSR3.</div>")),
        row(
            step(panel("Запись в таблице продвижения LSR1",
                       tbl(["Входной интерфейс", "Метка", "Следующий хоп", "Действия"],
                           [["…", "…", "…", "…"], ["S0", "256", "S1", "272"], ["…", "…", "…", "…"]])
                       + '<div class="m2cap s4l">Число в поле «Действия» означает замену верхней метки.</div>', "", num="1")),
            step(panel("Запись на LSR2", tbl(["Вход", "Метка", "Выход", "Действие"], [["S0", "272", "S1", "Swap 132"]])
                       + '<div class="m2cap s4l">LSR2 заменяет только верхнюю метку и отправляет кадр в LSR3.</div>', "or",
                       num="2"))),
        step(panel("", '<div class="s4tr">%s<span class="s4arw">→</span>%s<span class="s4arw">→</span>%s</div>'
                       '<div class="m2cap s4big">Внутренняя метка 315 не изменяется.</div>' % (
                           spk([("272", "cy"), ("315", "r"), IP], "xl"), node(ico(r2, 60), "LSR2"),
                           spk([("132", "cy"), ("315", "r"), IP], "xl")), "tint")),
    ]), sub=S22)

    # ================================================================ pptx 23
    S23 = "LSR3: снятие внешней метки на предпоследнем узле"
    r3 = "i23a_rt.png"
    cell = lambda t, c: '<b class="%s">%s</b>' % (c, t)
    slide("pptx 23 · LSR3 и PHP", "bgk_05", TP, "".join([
        step(panel("", '<div class="m2big">Работа устройства LSR3 несколько отличается от работы устройств LSR1 и LSR2, так как оно '
                       "является <b>предпоследним</b> устройством LSR для пути LSP1. В соответствии с записью в таблице "
                       "продвижения устройство LSR3 выполняет выталкивание (<b>Pop</b>) из стека метки 132, относящейся к пути "
                       "LSP1, выполняя операцию <b>PHP</b>. В результате верхней меткой стека становится метка <b>315</b>, "
                       "принадлежащая пути LSP3.</div>")),
        panel("Завершение внешнего пути LSP1", chain([
            hop("LSR2", "", r3, 104) + fly(spk([("132", "cy"), ("315", "r"), IP], "xl")),
            '<div class="s4pop">%s<span class="s4off">%s<em>Удаляется</em></span><span class="m2pill or s4pp">Pop 132</span></div>'
            % (node(ico(r3, 104), "LSR3"), spk([("132", "cy")], "xl")) + fly(spk([("315", "r"), IP], "xl")),
            hop("LER2", "Продолжение по LSP3", r3, 104)], style="align-items:center;justify-content:space-around")
              + '<div class="m2cap">Верхняя метка показана слева.</div>', "tint s4big23"),
        step('<div class="m2note s4bn">Метка <b>132</b> удалена. Метка <b>315</b> пути LSP3 становится верхней. Пакет остаётся '
             "MPLS-пакетом: в стеке ещё есть метка.</div>"),
    ]), safe="s4rr", sub=S23)
    slide("pptx 23 · Стек после Pop", "bgk_05", TP, "".join([
        row(
            step(panel("Как изменяется стек", '<div class="s4st"><div><h4>До</h4><div class="s4cl">%s%s%s</div>'
                       '<small>LSP1 · LSP3</small></div><div class="s4op">Pop<br>→</div><div><h4>После</h4>'
                       '<div class="s4cl">%s%s</div><small>Новая вершина</small></div></div>' % (
                           cell("132", "cy"), cell("315", "r"), cell("IP", "w"), cell("315", "r"), cell("IP", "w")))),
            step(panel("Запись в таблице LSR3", tbl(["Вход", "Метка", "Выход", "Действие"], [["S0", "132", "S1", "<b>Pop</b>"]])
                       + '<div class="s4php"><b>PHP — Penultimate Hop Popping</b><br>Снятие метки на предпоследнем узле.</div>',
                       "or")), cls="s4h"),
    ]), safe="s4rr", sub=S23)

    # ================================================================ pptx 24
    S24 = "LER2: замена метки LSP3 и вход в LSP2"

    def stg(n, head, pkt, cap):
        return '<div class="s4stg"><div class="s4sh"><span class="m2n">%s</span>%s</div>%s<div class="m2cap">%s</div></div>' % (
            n, head, pkt, cap)

    slide("pptx 24 · LER2: Swap и Push", "bgk_21", TP, "".join([
        step(panel("", '<div class="m2big">Устройство <b>LER2</b> продвигает поступивший на его входной интерфейс S0 кадр на '
                       "основе своей записи таблицы продвижения. Устройство LER2 сначала <b>заменяет метку 315</b> пути LSP3 "
                       "значением <b>317</b>, затем проталкивает ее на дно стека и <b>помещает на вершину стека метку 188</b>, "
                       "которая является меткой пути LSP2, внутреннего для домена 2.</div>")),
        panel("Две операции над стеком: Swap → Push", '<div class="s4ops">' + "".join([
            step(stg(1, "На входе LER2", spk([("315", "r"), IP], "xl"), "Метка LSP3: 315")),
            step('<div class="s4yop">Swap<br>315 → 317</div>'),
            step(stg(2, "После замены", spk([("317", "r"), IP], "xl"), "Метка LSP3: 317")),
            step('<div class="s4yop">Push<br>188</div>'),
            step(stg(3, "На выходе LER2", spk([("188", "t"), ("317", "r"), IP], "xl m2flt"),
                     "188 — верхняя, транспортная метка LSP2<br>317 — нижняя метка LSP3"))]) + "</div>"
              + '<div class="m2cap s4cb">Верхняя метка показана слева. Метка 317 остаётся под новой меткой 188.</div>', "tint"),
        step(bulb("Добавление новой метки не требует отдельного „перемещения на дно“: операция Push помещает её поверх "
                  "существующего стека.", "i24a_bulb.png")),
    ]), safe="sl", sub=S24)

    slide("pptx 24 · Далее по LSP2", "bgk_21", TP, "".join([
        row(
            step('<div class="s4col">%s%s</div>' % (
                panel("Запись таблицы продвижения LER2", tbl(["Входной интерфейс", "Метка", "Выходной интерфейс", "Действия"],
                                                             [["S0", "315", "S1", "Swap 317;<br>Push 188"]])
                      + '<div class="m2cap s4l">S0 и S1 — условные обозначения интерфейсов.</div>', "or"),
                panel("Далее — по пути LSP2", '<div class="m2chain" style="align-items:center">%s</div>' % (
                    node(ico("i24a_rt.png", 50), "LER2") + arrow() + '<span class="m2flt">%s</span>' % spk(
                        [("188", "t"), ("317", "r"), IP]) + arrow() + node(ico("i24a_rt.png", 50), "LER3") + arrow()
                    + node(ico("i24a_rt.png", 50), "LSR4"))
                      + '<div class="m2big" style="margin-top:8px">Перемещение кадра вдоль пути LSP2 происходит '
                        "<b>аналогичным образом</b>.</div>"
                      + "<p>Пакет передаётся в домен 2. Внутренние LSR продвигают его по верхней метке LSP2; нижняя метка "
                        "LSP3 сохраняется до завершения транспортного участка.</p>", "gr"))),
            step(panel("Весь путь LSP3", '<div class="s4sc">%s</div>' % sc(two_domains(True), [
                "IP-пакет приходит на LER1", "LER1 начинает LSP1 и LSP3: Push 315; Push 256", "LSR1: 256 → 272",
                "LSR2: 272 → 132", "LSR3 (PHP): Pop 132 — на вершине 315", "LER2: 315 → 317, Push 188",
                "Дальше по LSP2 в домене 2"], "0 0 1200 520"), "tint")), cls="s4r12"),
    ]), safe="sl", sub=S24)


CSS = r"""
.m2>.m2in.s4rr{padding-right:clamp(170px,19vw,370px)}
.s4top>.step:first-child{flex:1.25 1 0}
.s4r21>.step:first-child{flex:2 1 0}
.s4r12>.step:last-child{flex:1.35 1 0}
.s4sc .scene{gap:6px}.s4sc .figwrap{padding:4px!important}
.s4sc svg{max-height:min(41vh,380px);width:100%}
.s4pk{display:inline-flex;border:3px solid #1d3f8a;border-radius:6px;overflow:hidden;vertical-align:middle;background:#fff;
 font:800 clamp(13px,1.1vw,21px)/1.75 "Golos Text",sans-serif;color:#13306e;white-space:nowrap}
.s4pk b{padding:0 .42em;border-right:2px solid #1d3f8a;font-weight:800;color:#13306e}
.s4pk b:last-child{border-right:0}
.s4pk.xl{font-size:clamp(17px,1.6vw,30px)}
.s4big23 .s4pk.xl{font-size:clamp(20px,2vw,38px)}
.s4pk b.r,.s4bar b.r,.s4cl b.r{background:#f2694a;color:#1d1d1d}
.s4pk b.cy,.s4cl b.cy{background:#5bd0f2}
.s4pk b.t,.s4bar b.t{background:#9fe3cc}
.s4pk b.w,.s4bar b.w,.s4cl b.w{background:#fff;padding:0 .7em}
.s4ch{align-items:flex-start}
.s4ch>.step{flex:0 1 auto}
.s4rev,.s4rev>.step{flex-direction:row-reverse}
.s4in{font:800 clamp(12px,1vw,18px)/1.15 "Golos Text",sans-serif;color:#13306e;text-align:center;margin-left:6px}
.s4hi{display:inline-grid;place-items:center;width:52px;height:52px;border-radius:50%;background:#ccefea;flex:none}
.s4hi .ico{height:40px}
.s4l{text-align:left;margin-top:6px;font-weight:600}
.s4tb td:first-child{font-weight:800;color:#13306e}
.s4tb th,.s4tb td{text-align:center}.s4tb td:first-child,.s4tb th:first-child{text-align:left}
.s4l3{position:relative}
.s4br{position:relative;height:30px;margin:0 3% 4px;border:3px solid #e2564a;border-bottom:0}
.s4br::before{content:"";position:absolute;left:0;right:0;top:10px;height:3px;background:#e2564a}
.s4br span{position:absolute;left:50%;top:-6px;transform:translateX(-50%);background:#d6ecfb;padding:0 16px;
 font:900 clamp(20px,1.9vw,36px)/1 "Rubik",sans-serif;color:#e2564a}
.s4z{flex:1;display:flex;align-items:center;justify-content:space-around;padding:22px 10px 10px}
.s4z.g{background:rgba(191,238,224,.95)}.s4z.g>.m2zl{background:#bfeee0;color:#1e7a5c}
.s4z.b{background:rgba(207,230,251,.98)}.s4z.b>.m2zl{background:#cfe6fb;color:#1f63c6}
.s4a{font:900 clamp(18px,1.6vw,30px)/1 sans-serif;color:#1f63c6}.s4a.g{color:#1e8a6a}
.s4ln{flex:0 0 clamp(30px,4vw,80px);height:3px;background:#13306e}
.s4li p{display:flex;gap:10px;align-items:flex-start;margin:0 0 .4em;font:500 clamp(15px,1.3vw,25px)/1.35 "Golos Text",sans-serif}
.s4li .m2n{background:#f2694a;width:1.45em;height:1.45em;font-size:.9em}
.s4bar{display:flex;margin:14px auto 22px;max-width:620px;border:3px solid #1d3f8a;border-radius:5px;
 font:800 clamp(14px,1.2vw,22px)/1.15 "Golos Text",sans-serif;color:#13306e;text-align:center}
.s4bar b{flex:1;display:flex;align-items:center;justify-content:center;padding:8px 4px;position:relative;min-height:2.6em;
 border-right:2px solid #1d3f8a}
.s4bar b:last-child{border-right:0}
.s4bar i{position:absolute;bottom:-1.6em;left:0;right:0;font-style:normal;color:#13306e}
.s4col{display:flex;flex-direction:column;gap:clamp(8px,1vw,16px);height:100%}
.s4col>.m2p{flex:1 1 auto}
.s4y{display:flex;align-items:center;gap:16px;background:#fde27a;border:3px solid #1f63c6;border-radius:16px;padding:10px 18px;
 font:800 clamp(16px,1.5vw,28px)/1.3 "Golos Text",sans-serif;color:#13306e;box-shadow:0 6px 0 rgba(21,80,168,.25)}
.s4y .ico{flex:none}
.s4dash{position:relative;height:28px;margin:4px 16% 0;border-bottom:3px dashed #6b6b6b;border-radius:0 0 50% 50%}
.s4dash span{position:absolute;left:50%;bottom:-.75em;transform:translateX(-50%);background:#bfe9e4;padding:0 12px;white-space:nowrap;
 font:700 clamp(14px,1.2vw,22px)/1.4 "Golos Text",sans-serif;color:#555}
.s4n{display:flex;flex-direction:column;justify-content:center;height:100%;box-sizing:border-box;font-size:clamp(16px,1.45vw,28px)}
.s4n .s4pk{font-size:clamp(16px,1.4vw,26px)}
.s4tr{display:flex;align-items:center;justify-content:center;gap:clamp(12px,2vw,40px)}
.s4arw{font:900 clamp(26px,2.4vw,46px)/1 sans-serif;color:#13306e}
.s4big{font-size:clamp(17px,1.6vw,30px);margin-top:6px}
.s4pop{position:relative;display:flex;flex-direction:column;align-items:center;padding:48px 30px 0;border-radius:50%;
 background:radial-gradient(#c8f2dc,rgba(200,242,220,0) 70%)}
.s4off{position:absolute;top:-4px;left:58%;display:flex;align-items:center;gap:8px;animation:s4u 2.6s ease-in-out infinite}
.s4off .s4pk{transform:rotate(-8deg)}
.s4off em{font:600 clamp(13px,1.1vw,21px)/1 "Golos Text",sans-serif;font-style:normal;color:#13306e;white-space:nowrap}
@keyframes s4u{50%{transform:translate(4px,-6px)}}
.s4pp{margin-top:6px;background:#f2694a!important;color:#fff!important;font-size:clamp(15px,1.3vw,25px)}
.s4st{display:flex;align-items:center;justify-content:space-around;gap:12px;text-align:center}
.s4st h4{margin:0 0 6px;font:800 clamp(16px,1.4vw,26px)/1 "Golos Text",sans-serif;color:#13306e}
.s4st small{display:block;margin-top:6px;font:600 clamp(12px,1vw,19px)/1.2 "Golos Text",sans-serif;color:#33476e}
.s4cl{display:flex;flex-direction:column;gap:4px;align-items:center}
.s4cl b{display:block;width:clamp(80px,7vw,130px);border:2.5px solid #1d3f8a;border-radius:6px;
 font:800 clamp(16px,1.4vw,26px)/1.6 "Golos Text",sans-serif;color:#13306e}
.s4op{font:900 clamp(18px,1.6vw,30px)/1.1 "Golos Text",sans-serif;color:#f2694a}
.s4php{margin-top:10px;background:#d6ebfb;border-radius:10px;padding:8px 14px;color:#13306e}
.s4ops{display:flex;align-items:stretch;justify-content:space-between;gap:8px}
.s4ops>.step{display:flex;align-items:center}
.s4ops>.step:nth-child(odd){flex:1 1 0}
.s4stg{width:100%;background:#c6ebe4;border-radius:18px;padding:12px 10px;text-align:center;display:flex;flex-direction:column;
 align-items:center;gap:10px}
.s4sh{display:flex;align-items:center;gap:10px;font:700 clamp(15px,1.35vw,26px)/1 "Golos Text",sans-serif;color:#13306e}
.s4sh .m2n{background:#1e8a8a}
.s4yop{background:#fdd44f;clip-path:polygon(0 18%,74% 18%,74% 0,100% 50%,74% 100%,74% 82%,0 82%);padding:26px 34px 26px 14px;
 font:800 clamp(15px,1.35vw,26px)/1.1 "Golos Text",sans-serif;color:#13306e;text-align:center;white-space:nowrap}
.s4h{flex:1 1 auto}.s4h>.step{display:flex}.s4h>.step>.m2p{flex:1}.s4h .m2p{display:flex;flex-direction:column}.s4h .m2b{flex:1;display:flex;flex-direction:column;justify-content:center}.s4h .m2b{font-size:clamp(16px,1.45vw,28px)}
.s4h .s4cl{gap:8px}.s4h .s4cl b{width:clamp(140px,14vw,270px);font-size:clamp(26px,2.6vw,50px);line-height:1.8}
.s4h .s4st small{font-size:clamp(15px,1.3vw,25px)}.s4h .s4php{font-size:clamp(17px,1.6vw,30px);padding:14px 18px;margin-top:18px}
.s4h .s4st h4{font-size:clamp(24px,2.3vw,44px);margin-bottom:14px}.s4h .s4op{font-size:clamp(30px,3vw,56px)}
.s4h .m2tbl{font-size:clamp(20px,2vw,38px)}.s4h .m2tbl td,.s4h .m2tbl th{padding:18px 12px}
.s4bn{font-size:clamp(17px,1.6vw,30px);padding:12px 18px}
.s4cb{margin-top:10px;background:#d6ebfb;border-radius:8px;padding:6px}
"""
