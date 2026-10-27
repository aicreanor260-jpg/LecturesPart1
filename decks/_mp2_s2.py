# -*- coding: utf-8 -*-
"""MPLS 2.9 v2 — pptx 6–12. Текст pptx дословно (из _mp_s1.py), разнесён по смыслу; заголовки блоков, пилюли и
подписи схем — из инфографик автора i06a, i06b, i07a … i12a; схемы — живая вёрстка с раскрытием по шагам."""
import os

from PIL import Image

from _mp2_kit import slide, step, panel, row, pk, node, arrow, ico, _b64, CROPS
from _mp2_s1 import chain
from _mp_s1 import arch

_uid = [0]


def _id(p):
    _uid[0] += 1
    return "m2s2%s%d" % (p, _uid[0])


# ---------------------------------------------------------------- SVG-схемы с вырезками автора
class Svg:
    """SVG-схема: вырезки (маршрутизаторы, пакеты) — через <use> одной картинки; маркеры с уникальными id."""

    def __init__(self, vb):
        self.vb, self.defs, self.ims, self.mk = vb, [], {}, {}

    def img(self, file, cx, cy, w):
        if file not in self.ims:
            i = _id("i")
            W, H = Image.open(os.path.join(CROPS, file)).size
            self.defs.append('<image id="%s" href="%s" width="%d" height="%d"/>' % (i, _b64(os.path.join(CROPS, file)), W, H))
            self.ims[file] = (i, W, H)
        i, W, H = self.ims[file]
        k = float(w) / W
        return '<use href="#%s" transform="translate(%g %g) scale(%g)"/>' % (i, cx - w / 2.0, cy - H * k / 2.0, k)

    def marker(self, col):
        if col not in self.mk:
            i = _id("m")
            self.defs.append('<marker id="%s" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4" markerHeight="4" '
                             'orient="auto"><path d="M0 0L10 5L0 10z" style="fill:%s"/></marker>' % (i, col))
            self.mk[col] = i
        return self.mk[col]

    def line(self, x1, y1, x2, y2, col, w=6, arrow=True, dash=False):
        m = ' marker-end="url(#%s)"' % self.marker(col) if arrow else ""
        d = ";stroke-dasharray:4 12" if dash else ""
        return ('<path d="M%g %gL%g %g" style="fill:none;stroke:%s;stroke-width:%g;stroke-linecap:round%s"%s/>'
                % (x1, y1, x2, y2, col, w, d, m))

    def render(self, body, cls=""):
        return '<svg class="m2s2-svg %s" viewBox="%s" xmlns="http://www.w3.org/2000/svg"><defs>%s</defs>%s</svg>' % (
            cls, self.vb, "".join(self.defs), body)


def tx(x, y, s, size=24, col="#13306e", w=800, anchor="middle"):
    return ('<text x="%g" y="%g" text-anchor="%s" style="font:%d %dpx \'Golos Text\',sans-serif;fill:%s">%s</text>'
            % (x, y, anchor, w, size, col, s))


def gstep(html):
    return '<g class="step">%s</g>' % html


def bar(x, y, n, filled, col, w=96):
    """Индикатор загрузки линии (как в инфографике i06a)."""
    c = w / float(n)
    out = ['<g class="m2s2-fly">']
    for k in range(n):
        out.append('<rect x="%g" y="%g" width="%g" height="26" style="fill:%s;stroke:#1d3f8a;stroke-width:2.5"/>'
                   % (x + k * c, y, c, col if k < filled else "#fff"))
    out.append("</g>")
    return "".join(out)


def pill(cx, y, w, head, sub, fill):
    return ('<rect x="%g" y="%g" width="%g" height="74" rx="18" style="fill:%s"/>%s%s'
            % (cx - w / 2.0, y, w, fill, tx(cx, y + 31, head, 25, "#13306e", 900), tx(cx, y + 62, sub, 22, "#1d2a44", 600)))


def net6():
    """pptx 6: два пути между пограничными маршрутизаторами — строки таблицы pptx стали подписями путей."""
    s = Svg("0 0 1400 450")
    R = {"R1": (150, 225), "R2": (700, 165), "R4": (1250, 225), "R3": (500, 300), "R5": (900, 300)}
    base = "".join(s.img("i06a_rt.png", x, y, 124) + tx(x, y + 66, n, 30, "#13306e", 900) for n, (x, y) in R.items())
    org, teal = "#f0662f", "#1f9c8a"
    l1 = "".join([s.line(215, 212, 625, 172, org), s.line(775, 172, 1180, 212, org),
                  bar(372, 158, 4, 3, org), bar(930, 158, 4, 3, org),
                  pill(700, 6, 760, "Обычная IP-маршрутизация · R1 → R2 → R4", "Имеет меньшую метрику, но сильно загружен",
                       "#fbd8c9")])
    l2 = "".join([s.line(200, 265, 432, 300, teal), s.line(565, 300, 830, 300, teal), s.line(965, 296, 1195, 262, teal),
                  bar(258, 300, 4, 1, teal, 80), bar(650, 268, 4, 1, teal, 80), bar(1050, 292, 4, 1, teal, 80),
                  pill(700, 372, 860, "LSP с MPLS TE · R1 → R3 → R5 → R4",
                       "Имеет большую метрику, но располагает свободной полосой", "#cdeee4")])
    return s.render(base + gstep(l1) + gstep(l2))


def net6b(te):
    """pptx 6 (i06b): обычная маршрутизация — IP-пакеты по пути 1; MPLS TE — LSP по пути 2."""
    s = Svg("0 0 760 360")
    R = {"R1": (70, 175), "R2": (380, 105), "R4": (690, 175), "R3": (265, 255), "R5": (495, 255)}
    out = []
    org, grey, grn = "#f0663f", "#7d8a80", "#1fa760"
    out.append('<rect x="8" y="48" width="744" height="262" rx="120" style="fill:#d7eedd"/>')
    out += [s.line(112, 165, 330, 115, org, 5), s.line(430, 115, 645, 165, org, 5)]
    for x, y in ((170, 132), (520, 128)):
        out.append(s.img("i06b_ip.png", x, y, 64))
    out.append(tx(380, 36, "Путь 1 • метрика 10 • высокая загрузка", 21, "#1d2a44", 600))
    p2 = [s.line(95, 210, 220, 252, grn if te else grey, 5), s.line(312, 255, 445, 255, grn if te else grey, 5),
          s.line(542, 250, 660, 212, grn if te else grey, 5)]
    out.append(tx(380, 345, "Путь 2 • метрика 30 • есть ресурс", 21, "#1d2a44", 600))
    for n, (x, y) in R.items():
        out.append(s.img("i06b_rt.png", x, y, 92) + tx(x, y + 52, n, 25, "#13306e", 900))
    if te:
        tags = "".join('<g class="m2s2-fly"><rect x="%g" y="%g" width="86" height="34" rx="6" style="fill:#fdd768;'
                       'stroke:#b8860b;stroke-width:2.5"/>%s</g>' % (x - 43, y - 17, tx(x, y + 8, "MPLS", 20, "#13306e", 900))
                       for x, y in ((158, 222), (380, 236), (605, 222)))
        out.append(gstep("".join(p2) + tags))
    else:
        out += p2
        out.append("".join(s.img("i06b_ipg.png", x, y, 60) for x, y in ((158, 222), (380, 236), (605, 222))))
    return s.render("".join(out), "m2s2-sm")


# ---------------------------------------------------------------- HTML-блоки
def bx(html, cls=""):
    return '<div class="m2s2-bx %s">%s</div>' % (cls, html)


def li(items, cls=""):
    return '<ul class="m2s2-ul %s">%s</ul>' % (cls, "".join("<li>%s</li>" % x for x in items))


def card(num, img, html, cls=""):
    return panel("", '<div class="m2s2-card"><span class="m2n">%s</span>%s<div>%s</div></div>' % (num, img, html), cls)


def nums(items):
    return "".join(step('<div class="m2s2-num"><span class="m2n">%d</span><div>%s</div></div>' % (k + 1, x))
                   for k, x in enumerate(items))


def build():
    # ---------------------------------------------------------------- pptx 6
    T6 = "Чем обычная IP-передача отличается от передачи по <em>виртуальному каналу</em>"
    slide("pptx 6 · Детерминированный маршрут", "bgk_30", T6, "".join([
        step(panel("", '<div class="m2big"><b>Детерминированный маршрут</b> - это <b>заранее определённый путь через сеть</b>, '
                   "которому следует трафик, направленный в соответствующий LSP.</div>")),
        panel("", '<div class="m2big" style="margin-bottom:6px">Допустим, между двумя пограничными маршрутизаторами есть '
              "два пути:</div>" + net6(), "tint"),
    ]), safe="sr")

    slide("pptx 6 · Выбор пути", "bgk_24", T6, "".join([
        row(
            step(panel("Обычная IP-маршрутизация", net6b(False) +
                       '<div class="m2s2-cc">Выбор по метрике: путь 1.</div>'
                       "<p>Обычная маршрутизация, ориентированная на метрику, может продолжать выбирать первый путь: "
                       "высокая загрузка сама по себе не обязательно меняет его метрику.</p>", "rd", num="1")),
            step(panel("MPLS Traffic Engineering", net6b(True) +
                       '<div class="m2s2-cc"><span class="m2s2-lsp">LSP по пути 2</span></div>'
                       "<p>С помощью <b>MPLS Traffic Engineering</b> можно организовать LSP по второму пути и направить "
                       "туда часть трафика.</p>", "gr", num="2"))),
        step(panel("", '<div class="m2s2-imp">%s<span class="m2s2-wa">Важно</span><div class="m2big">При этом <b>не каждый LSP '
                   "автоматически проходит по специально заданному маршруту</b>. Например, LSP, построенный с помощью LDP, "
                   "обычно следует путям обычной IP-маршрутизации. Для выбора пути с дополнительными ограничениями "
                   "применяются механизмы MPLS TE.</div></div>" % ico("i06b_ex.png", 74), "or")),
    ]), sub="Выбор пути: обычная маршрутизация и MPLS Traffic Engineering")

    # ---------------------------------------------------------------- pptx 7
    slide("pptx 7 · Инжиниринг трафика", "bgk_06", "<em>Инжиниринг</em> трафика", "".join([
        step(panel("", '<div class="m2big" style="font-size:clamp(18px,1.75vw,34px)"><b>Инжиниринг трафика — это управление '
                   "распределением потоков по сети с учётом её ресурсов и требований к передаче.</b></div>")),
        '<div class="m2s2-lead">Оператор может, например:</div>',
        row(
            step(card(1, ico("i07a_c1.png", 120), "перенести часть потоков с перегруженных линий на менее загруженные;")),
            step(card(2, ico("i07a_c2.png", 120), "проложить путь с учётом требуемой пропускной способности;")),
            step(card(3, ico("i07a_c3.png", 120), "организовать резервный путь на случай отказа."))),
        step(panel("", '<div class="m2big">Детерминированный маршрут даёт возможность <b>направить выбранный поток по нужной '
                   "последовательности узлов</b>.</div>"
                   '<div class="m2big" style="margin-top:8px">Однако сама фиксация пути ещё не гарантирует полосу, малую '
                   "задержку или отсутствие потерь: для этого необходимы соответствующие механизмы <b>резервирования "
                   "ресурсов и QoS</b>.</div>", "or")),
    ]))

    # ---------------------------------------------------------------- pptx 8
    def flow(a, tb, b, ca, cb, foot=""):
        f = ('<div class="m2s2-flow"><div>%s<small>%s</small></div>%s%s%s<div>%s<small>%s</small></div></div>'
             % (a, ca, arrow(), ico(tb, 92), arrow(), b, cb))
        return f + ('<div class="m2s2-lsp2">%s</div>' % foot if foot else "")

    slide("pptx 8 · Базовые принципы", "bgk_10", "Базовые принципы и механизмы <em>MPLS</em>", "".join([
        step(panel("", '<div class="m2s2-mb">В одном и том же устройстве поддерживается два разных способа продвижения пакетов: '
                   "<b>дейтаграммный</b> на основе IP-адресов и <b>ориентированный на соединения</b> механизм виртуальных "
                   "каналов.</div>")),
        row(
            step(panel("IP-передача", li(["Дейтаграммный способ", "Поиск по IP-адресу назначения", "Таблица IP-маршрутизации"],
                                         "gr") +
                       flow(ico("i08a_ip.png", 44), "i08a_t1.png", ico("i08a_ip.png", 44), "IP-пакет<br>(без метки)",
                            "IP-пакет<br>(без метки)"), "gr tintg")),
            '<div class="m2s2-mid">%s<b>Маршрутизатор<br>с поддержкой MPLS</b></div>' % ico("i08a_rt.png", 78, "m2flt"),
            step(panel("MPLS-передача", li(["Механизм виртуальных каналов", "Поиск по метке MPLS", "Таблица MPLS-продвижения"],
                                           "rd") +
                       flow(pk([100]), "i08a_t2.png", pk([200]), "MPLS-пакет<br>(с меткой)", "MPLS-пакет<br>(с меткой)",
                            "Продвижение по LSP"), "rd tintr"))),
        row(step(panel("Как формируются таблицы", '<div class="m2s2-tf">%s<div class="m2s2-mb">В то же время протоколы маршрутизации '
                   "используются для определения топологии сети и автоматического построения <b>таблиц IP-маршрутизации</b> "
                   "и <b>таблиц MPLS-продвижения</b>.</div>%s</div>" % (ico("i08a_topo.png", 56), ""))),
        step(panel("", '<div class="m2s2-imp">%s<div class="m2s2-mb">Комбинированное устройство может задействовать <b>любой из '
                   "двух способов</b> продвижения пакетов в зависимости от конфигурационных параметров протокола MPLS."
                   "</div></div>" % ico("i08a_bulb.png", 62), "or")), cls="m2s2-r8"),
    ]), safe="sl", sub="Одно устройство — два способа продвижения пакетов")

    # ---------------------------------------------------------------- pptx 9
    T9 = "Упрощенная архитектура стандартного <em>IP-маршрутизатора</em>"
    other = bx("Другие маршрутизаторы" + ico("i09a_rt.png", 50), "bl")
    dg1 = ('<div class="m2s2-dg">%s<span class="m2s2-ar2">⟷</span>%s<span class="m2s2-ar2">⟷</span>%s</div>'
           '<div class="m2s2-down">↓</div>%s' % (
               step(other), bx("Протоколы маршрутизации:<br>RIP, OSPF, IS-IS", "or big"), step(other),
               step('<div class="m2s2-c">%s</div>' % bx("Таблица<br>маршрутизации" + ico("i09a_tb.png", 50), "yl big"))))
    slide("pptx 9 · Управление", "bgk_19", T9, panel(
        '1. Управление <span class="m2s2-thin">— определяет, куда передавать пакеты</span>',
        row('<div class="m2s2-zone">%s</div>' % dg1,
            "<div>" + step("<p>Верхняя часть схемы отвечает за получение сведений о сетях и выбор маршрутов.</p>"
                           "<p><b>Протоколы маршрутизации RIP, OSPF, IS-IS</b> обмениваются служебными сообщениями с другими "
                           "маршрутизаторами. На основе полученных сведений маршрутизатор выбирает лучшие маршруты и вносит их "
                           "в <b>таблицу маршрутизации</b>.</p>") +
            step("<p>В ней указывается:</p>" + li(["сеть назначения;", "следующий маршрутизатор — <b>next hop</b>;",
                                                    "выходной интерфейс;", "параметры, по которым выбирается маршрут."]) +
                 "<p>Таблица также содержит напрямую подключённые сети и может включать статические маршруты, заданные "
                 "администратором. Все перечисленные протоколы одновременно запускать необязательно.</p>") + "</div>",
            cls="m2s2-r9"), "m2s2-nc m2s2-f9 m2s2-bt9"), safe="m2s2-tl")

    nic = ico("i09a_nic.png", 34)
    dg2 = ('<div class="m2s2-c m2s2-tbup">%s<div class="m2s2-down">↓</div></div>'
           '<div class="m2s2-dg2"><b class="m2s2-tr">Входящий<br>трафик</b><span class="m2s2-ar2">→</span>%s'
           '<span class="m2s2-ar2">→</span>%s<span class="m2s2-ar2">→</span>%s<span class="m2s2-ar2">→</span>'
           '<b class="m2s2-tr">Исходящий<br>трафик</b></div>' % (
               bx("Таблица маршрутизации", "yl sm"), bx("Входной<br>интерфейс" + nic, "bl"),
               bx("IP-продвижение" + ico("i09a_gear.png", 42), "or big"), bx("Выходной<br>интерфейс" + nic, "bl")))
    slide("pptx 9 · Продвижение данных", "bgk_19", T9, panel(
        '2. Продвижение данных <span class="m2s2-thin">— передаёт конкретный пакет</span>',
        '<div class="m2s2-zone">%s</div>' % dg2 +
        '<div class="m2big" style="margin:12px 0 8px">Нижняя часть схемы использует уже подготовленную информацию о маршрутах:</div>'
        '<div class="m2s2-g2">%s</div>' % nums([
            "<b>Входной интерфейс</b> принимает кадр. Маршрутизатор извлекает из него IP-пакет.",
            "Блок <b>IP-продвижения</b> читает IP-адрес назначения и находит наиболее специфичный подходящий маршрут.",
            "Маршрутизатор уменьшает TTL пакета и определяет следующий узел и выходной интерфейс.",
            "Пакет помещается в <b>новый кадр</b>, подходящий для выходного канала, и отправляется через <b>выходной "
            "интерфейс</b>."]), "or m2s2-nc m2s2-f9"), safe="m2s2-tl")

    # ---------------------------------------------------------------- pptx 10
    TL = "Архитектура комбинированного устройства <em>LSR</em>, поддерживающего технологии IP и MPLS"
    slide("pptx 10 · Устройство LSR", "bgk_22", TL, "".join([
        step(panel("", '<div class="m2big">Так как устройство LSR выполняет все функции IP-маршрутизатора, оно содержит все '
                   "блоки последнего, а для поддержки функций MPLS в LSR включен ряд <b>дополнительных блоков</b>, относящихся "
                   "как к управлению, так и к продвижению данных.</div>")),
        row(
            panel("Устройство LSR", arch(True), "tint m2s2-arch"),
            step(panel("Протоколы маршрутизации и таблица маршрутизации",
                       '<div class="m2s2-ic">%s<span class="m2pill bl">Маршруты</span></div>' % ico("i10a_n1.png", 64) +
                       '<div class="m2big"><p>Эти блоки выполняют знакомую работу: протоколы маршрутизации, например OSPF '
                       "или IS-IS, получают сведения о сети, а выбранные маршруты попадают в таблицу маршрутизации.</p>"
                       "<p>Эта информация используется для обычного IP-продвижения и служит основой для построения "
                       "MPLS-путей.</p></div>", "m2s2-nc", num="1")), cls="m2s2-r10"),
    ]))

    slide("pptx 10 · Сигнализация и LFIB", "bgk_22", TL, "".join([
        row(
            step(panel("Сигнальный протокол",
                       '<div class="m2s2-ic">%s<span class="m2pill or">Сигнализация</span></div>' % ico("i10a_n2.png", 64) +
                       "<p>Чтобы передавать пакеты по меткам, соседним маршрутизаторам нужно согласовать, <b>какие метки "
                       "использовать и с какими направлениями передачи они связаны</b>.</p>"
                       "<p>Для этого применяется сигнальный протокол.</p>"
                       "<p>Обмен служебными сообщениями позволяет сформировать согласованные записи на последовательности "
                       "маршрутизаторов. Так образуется <b>LSP — Label Switched Path, путь коммутации по меткам</b> — это "
                       "однонаправленный путь, по которому пакеты продвигаются с использованием MPLS-меток.</p>",
                       "or m2s2-nc m2s2-k12", num="2")),
            '<div class="m2s2-col">' + step(panel("Таблица продвижения по меткам",
                       '<div class="m2s2-ic">%s<span class="m2pill gr">Продвижение по меткам</span></div>' % ico("i10a_n3.png", 64) +
                       "<p>В ней хранится информация о том, <b>как обработать пакет с определённой входной меткой</b>.</p>",
                       "gr m2s2-nc m2s2-k12", num="3")) +
            step(panel("Пример записи LFIB",
                   "<p>Например:</p>"
                   '<table class="m2tbl m2s2-tb"><tr><th>Входной интерфейс</th><th>Входная метка</th><th>Выходной интерфейс</th>'
                   "<th>Действие</th></tr><tr><td>Gi0/0</td><td>100</td><td>Gi0/1</td><td>Заменить метку 100 на 200</td></tr>"
                   "</table>"
                   '<div class="m2s2-swap">%s<span class="m2s2-long">→</span>%s</div>'
                   % ('<span class="m2flt">%s</span>' % pk([100]), '<span class="m2flt">%s</span>' % pk([200])), "tint")) + "</div>",
            cls="m2s2-r10b"),
    ]))

    # ---------------------------------------------------------------- pptx 11
    slide("pptx 11 · Два способа продвижения", "bgk_16", TL, "".join([
        panel("Как выбирается дальнейшее действие",
              '<div class="m2big" style="margin-bottom:8px">В нижней части схемы находятся два блока:</div>'
              '<div class="m2s2-two">%s%s%s</div>' % (
                  step(bx('<span class="m2s2-bh">IP-продвижение</span><span class="m2s2-bt">IP-адрес назначения пакета</span>',
                          "gn wide")),
                  '<div class="m2s2-c"><span class="m2s2-ar2">⟵</span>%s<span class="m2s2-ar2">⟶</span></div>'
                  % ico("i11a_rt2.png", 74),
                  step(bx('<span class="m2s2-bh">Продвижение по меткам</span><span class="m2s2-bt">Верхняя метка в стеке '
                          "MPLS</span>", "or wide"))) +
              '<div class="m2cap" style="margin-top:6px">Блок → на основании чего выбирается дальнейшее действие</div>',
              "m2s2-nc m2s2-k11"),
        step(panel("", '<div class="m2big">При обычной IP-передаче устройство анализирует адрес назначения и выбирает следующий '
                   "узел. При передаче по MPLS оно использует таблицу продвижения по меткам. Возможные операции — "
                   "<b>добавить метку (Push)</b>, <b>заменить (Swap)</b> или <b>снять (Pop)</b>.</div>"
                   '<div class="m2s2-ops">%s%s%s</div>' % (
                       step('<span class="m2pill or">Push</span>%s%s%s' % (pk([]), arrow(), pk([100]))),
                       step('<span class="m2pill bl">Swap</span>%s%s%s' % (pk([100]), arrow(), pk([200]))),
                       step('<span class="m2pill gr">Pop</span>%s%s%s' % (pk([300]), arrow(), pk([])))), "or m2s2-k11")),
    ]), sub="4. Два способа продвижения данных")

    slide("pptx 11 · Пример передачи", "bgk_16", TL, "".join([
        panel("Пример передачи через MPLS-сеть",
              '<div class="m2big" style="margin-bottom:12px">Например, передача через MPLS-сеть может выглядеть так:</div>' +
              chain(["Входной LER", "LSR", "LSR", "Выходной LER"],
                    ["Push: добавить 100", "Swap: 100 → 200", "Swap: 200 → 300", "Pop: снять 300"], [100, 200, 300],
                    foot="Транспортная метка снимается перед выходом из MPLS-сети.", rt="i11a_rt.png", ip="i11a_ip.png") +
              '<div class="m2s2-g2" style="margin-top:12px">%s</div>' % nums([
                  "<b>Входной пограничный маршрутизатор</b> получает IP-пакет и добавляет метку 100.",
                  "<b>Промежуточный LSR</b> заменяет 100 на 200 и передаёт пакет дальше.",
                  "<b>Следующий LSR</b> заменяет 200 на 300.",
                  "<b>Перед выходом из MPLS-сети</b> транспортная метка снимается."]), "tint m2s2-nc"),
        step(panel("Одно устройство — IP-трафик и MPLS-трафик",
                   '<div class="m2s2-tf">%s<div class="m2big">Наличие двух блоков продвижения позволяет одному устройству '
                   "обслуживать <b>и обычный IP-трафик, и MPLS-трафик</b>. Верхняя часть схемы заранее подготавливает "
                   "маршруты и соответствия меток, а нижняя использует их при передаче пакетов.</div>%s</div>"
                   % (ico("i11a_g.png", 64), ico("i11a_a.png", 64)), "gr")),
    ]))

    # ---------------------------------------------------------------- pptx 12
    T12 = "Роли <em>маршрутизатора</em>"
    pills = ['<span class="m2pill or">Push</span>', '<span class="m2pill gr">Swap</span>', ""]
    slide("pptx 12 · Роли", "bgk_12", T12, "".join([
        step(panel("", '<table class="m2tbl m2s2-tb"><tr><th>Роль</th><th>Название</th><th>Основная задача</th></tr>'
                   "<tr><td><b>Вход в MPLS-сеть</b></td><td>Входной LER — Ingress LER</td><td>Определяет FEC пакета и "
                   "добавляет метку</td></tr>"
                   "<tr><td><b>Передача внутри сети</b></td><td>Транзитный LSR</td><td>Продвигает пакет по верхней метке, "
                   "обычно заменяя её</td></tr>"
                   "<tr><td><b>Выход из MPLS-сети</b></td><td>Выходной LER — Egress LER</td><td>Завершает соответствующий "
                   "MPLS-путь и передаёт данные дальше</td></tr></table>")),
        step(panel("", '<div class="m2big"><b>LER (Label Edge Router) — пограничный маршрутизатор</b>, расположенный на входе '
                   "или выходе MPLS-сети.</div>")),
        panel("", chain(["Ingress LER", "LSR", "Egress LER"], pills, [100, 200],
                        foot="Снятие метки (Pop) — на выходном LER или предыдущем маршрутизаторе.",
                        rt="i12a_rt.png", ip="i12a_ip.png"), "tint m2s2-bigch"),
    ]), safe="sr")

    slide("pptx 12 · LER и LSR", "bgk_12", T12, "".join([
        row(
            step(panel('<span class="m2s2-hp or">Входной LER (Ingress)</span>',
                       "<p><b>Входной LER (Ingress)</b> принимает пакет, определяет его FEC и добавляет MPLS-метку — операция "
                       '<span class="m2pill or">Push</span>.</p>', "or m2s2-nc m2s2-k12")),
            step(panel('<span class="m2s2-hp gr">Транзитный LSR</span>',
                       "<p><b>LSR (Label Switching Router) — маршрутизатор, выполняющий коммутацию по меткам.</b> Внутри "
                       "MPLS-сети он читает верхнюю метку, находит запись в таблице продвижения и отправляет пакет через нужный "
                       'интерфейс. Обычно при этом заменяет метку — операция <span class="m2pill gr">Swap</span>.</p>',
                       "gr m2s2-nc m2s2-k12")),
            step(panel('<span class="m2s2-hp yl">Выходной LER (Egress)</span>',
                       "<p><b>Выходной LER (Egress)</b> завершает MPLS-путь и передаёт данные дальше. Метка снимается на нём "
                       "или на предыдущем маршрутизаторе.</p>", "m2s2-nc m2s2-k12"))),
        step(panel("В операторских MPLS VPN также используют обозначения <b>CE, PE и P</b>",
                   '<div class="m2s2-ce">%s</div>' % "".join(
                       '<div><div class="m2s2-ceh"><span class="m2s2-hp %s">%s</span> — %s</div><p><b>%s.</b></p><p>%s</p></div>'
                       % c for c in (
                           ("bl", "CE", "Customer Edge", "На стороне клиента",
                            "Подключает сеть клиента к оператору; обычно MPLS не требуется"),
                           ("yl", "PE", "Provider Edge", "На границе сети оператора",
                            "Подключает клиентов, обеспечивает VPN-сервисы и обработку сервисных меток"),
                           ("rd", "P", "Provider", "Внутри сети оператора",
                            "Переносит трафик между PE по транспортным меткам"))), "tint m2s2-nc m2s2-cep m2s2-k12")),
    ]), safe="sr")



CSS = r"""
.m2s2-svg{display:block;width:100%;height:auto;max-height:46vh;margin:0 auto}
.m2s2-svg .step{transform-box:fill-box}
.m2s2-fly{animation:m2s2f 2.6s ease-in-out infinite}
@keyframes m2s2f{50%{transform:translateX(6px)}}
.m2s2-cc{text-align:center;font:800 clamp(16px,1.5vw,29px)/1.3 "Golos Text",sans-serif;color:#13306e;margin:4px 0 6px}
.m2s2-lsp{display:inline-block;background:#fde072;border-radius:14px;padding:0 16px}
.m2s2-imp{display:flex;align-items:center;gap:16px}
.m2s2-imp .ico{flex:none}
.m2s2-wa{flex:none;background:#fde58a;border-radius:16px;padding:4px 18px;font:900 clamp(22px,2vw,38px)/1.3 "Rubik",sans-serif;color:#13306e}
.m2s2-lead{font:900 clamp(20px,1.9vw,36px)/1.1 "Rubik",sans-serif;color:#fff;text-shadow:0 2px 0 #1550a8,2px 0 0 #1550a8,-2px 0 0 #1550a8,
 0 -2px 0 #1550a8,0 6px 12px rgba(10,40,90,.35)}
.m2s2-card{display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center;position:relative;
 font:600 clamp(16px,1.45vw,28px)/1.35 "Golos Text",sans-serif}
.m2s2-card>.m2n{position:absolute;left:0;top:0;width:1.9em;height:1.9em;font-size:clamp(18px,1.6vw,30px)}
.m2s2-card>div{margin-top:4px}
.m2s2-ul{margin:0 0 8px;padding:0;list-style:none}
.m2s2-ul li{position:relative;padding-left:1.1em;margin:.15em 0}
.m2s2-ul li:before{content:"";position:absolute;left:0;top:.5em;width:.55em;height:.55em;border-radius:50%;background:#1f63c6}
.m2s2-ul.gr li:before{background:#1f9c8a}.m2s2-ul.rd li:before{background:#e2564a}
.m2p.tintg{background:rgba(214,240,228,.97)}.m2p.tintr{background:rgba(253,226,216,.97)}
.m2s2-flow{display:flex;align-items:center;justify-content:center;gap:6px;text-align:center}
.m2s2-flow>div{display:flex;flex-direction:column;align-items:center;gap:2px}
.m2s2-flow small{font:600 clamp(11px,.9vw,17px)/1.15 "Golos Text",sans-serif;color:#33476e}
.m2s2-flow .m2ar{margin-top:0}
.m2s2-lsp2{margin:4px auto 0;text-align:center;font:800 clamp(13px,1.05vw,20px)/1.2 "Golos Text",sans-serif;color:#13306e;
 border-top:2px solid #13306e;width:80%;padding-top:2px}
.m2row>.m2s2-mid{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
 font:800 clamp(14px,1.2vw,23px)/1.2 "Golos Text",sans-serif;color:#fff;text-shadow:0 2px 4px rgba(10,40,90,.7)}
.m2s2-tf{display:flex;align-items:center;gap:16px}
.m2s2-tf>.ico{flex:none}
.m2in.m2s2-tl>h1.m2t{padding-left:clamp(50px,5vw,100px)}
.m2s2-nc .m2h{text-transform:none}
.m2s2-thin{font:600 .8em "Golos Text",sans-serif;color:#33476e}
.m2s2-zone{background:rgba(191,233,228,.7);border-radius:18px;padding:14px}
.m2s2-r9{align-items:center}
.m2s2-r9>.m2s2-zone{flex:1.2 1 0}
.m2s2-f9{flex:1}
.m2s2-dg{display:flex;align-items:center;gap:6px}
.m2s2-dg>.step{flex:1}
.m2s2-dg>.m2s2-bx{flex:1.3}
.m2s2-r9>.m2s2-zone{min-width:0;overflow:hidden}.m2s2-dg .m2s2-bx{padding:8px 4px}.m2s2-f9 .m2s2-dg>.step .m2s2-bx{font-size:clamp(13px,1.1vw,21px)}
.m2s2-bx{border:3px solid #1d3f8a;border-radius:14px;padding:10px 10px;text-align:center;background:#d6ebfb;color:#13306e;
 font:800 clamp(14px,1.15vw,22px)/1.2 "Golos Text",sans-serif;display:flex;flex-direction:column;align-items:center;gap:8px}
.m2s2-bx.or{background:#f9b9a3}.m2s2-bx.yl{background:#fde3a0}.m2s2-bx.gn{background:#cdeee0}
.m2s2-bx.big{font-size:clamp(16px,1.4vw,27px)}
.m2s2-bx.sm{padding:4px 14px}
.m2s2-ar2{font:900 clamp(22px,2.2vw,42px)/1 sans-serif;color:#13306e;flex:none}
.m2s2-down{text-align:center;font:900 clamp(24px,2.2vw,42px)/1 sans-serif;color:#13306e;margin:4px 0}
.m2s2-c{display:flex;justify-content:center;align-items:center;gap:8px}
.m2s2-c>.m2s2-bx{min-width:45%}
.m2s2-tbup{flex-direction:column;gap:0}
.m2s2-tbup>.m2s2-bx{min-width:0}
.m2s2-dg2{display:flex;align-items:center;gap:10px}
.m2s2-dg2>.m2s2-bx{flex:1}
.m2s2-tr{font:800 clamp(14px,1.2vw,23px)/1.2 "Golos Text",sans-serif;color:#13306e;text-align:center;flex:none}
.m2s2-g2{display:grid;grid-template-columns:1fr 1fr;gap:10px 22px}
.m2s2-num{display:flex;gap:12px;align-items:flex-start;font:500 clamp(15px,1.4vw,27px)/1.35 "Golos Text",sans-serif}
.m2s2-num b{color:#123a7a;font-weight:800}
.m2s2-num>.m2n{background:#1f9c8a;color:#fff;font:900 clamp(15px,1.3vw,25px)/1 "Rubik",sans-serif;width:1.7em;height:1.7em;
 display:inline-grid;place-items:center;border-radius:50%;flex:none}
.m2s2-r10{align-items:stretch}
.m2s2-r10>.m2s2-arch{flex:1.45 1 0}
.m2s2-arch svg.mpfig{width:100%;height:auto;display:block}
.m2s2-ic{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.m2s2-tb{font-size:clamp(15px,1.35vw,26px)}
.m2s2-tb th,.m2s2-tb td{padding:8px 14px}
.m2s2-swap{display:flex;justify-content:center;align-items:center;gap:20px;margin-top:12px}
.m2s2-long{font:900 clamp(26px,2.6vw,50px)/1 sans-serif;color:#1f8fe0;letter-spacing:-4px}
.m2s2-two{display:flex;align-items:stretch;gap:12px}
.m2s2-two>.step{flex:1;display:flex}
.m2s2-two>.step>.m2s2-bx{flex:1;justify-content:center}
.m2s2-two>.m2s2-c{flex:none}
.m2s2-bh{font:900 clamp(18px,1.6vw,31px)/1.1 "Rubik",sans-serif;text-transform:uppercase}
.m2s2-bt{font:600 clamp(16px,1.45vw,28px)/1.3 "Golos Text",sans-serif;color:#1d2a44}
.m2s2-ops{display:flex;justify-content:space-around;flex-wrap:wrap;gap:12px;margin-top:12px}
.m2s2-ops>.step{display:flex;align-items:center;gap:10px}
.m2s2-ops .m2ar{margin-top:0}
.m2s2-hp{display:inline-block;border-radius:12px;padding:2px 14px;background:#d6ebfb;color:#13306e}
.m2s2-hp.or{background:#fbd3c4}.m2s2-hp.gr{background:#c8eee6}.m2s2-hp.yl{background:#fde58a}.m2s2-hp.rd{background:#fbd3c4}
.m2s2-ce{display:grid;grid-template-columns:repeat(3,1fr);gap:0}
.m2s2-ce>div{padding:0 16px}
.m2s2-ce>div+div{border-left:2px solid #1d3f8a}
.m2s2-ceh{font:800 clamp(15px,1.3vw,25px)/1.3 "Golos Text",sans-serif;color:#13306e;margin-bottom:4px}
.m2s2-ceh .m2s2-hp{font-weight:900}
.m2s2-cep .m2h{justify-content:center}
.m2s2-svg.m2s2-sm{max-height:25vh}
.m2s2-mb{font:600 clamp(15px,1.35vw,26px)/1.35 "Golos Text",sans-serif}.m2s2-mb b{color:#123a7a;font-weight:800}
.m2s2-r8>.step{display:flex}.m2s2-r8>.step>.m2p{flex:1}
.m2s2-bt9 .m2b{font-size:clamp(16px,1.5vw,29px)}
.m2s2-f9 .m2s2-bx{font-size:clamp(16px,1.4vw,27px)}.m2s2-f9 .m2s2-bx.big{font-size:clamp(18px,1.65vw,32px)}
.m2s2-f9 .m2s2-zone{padding:22px 14px}
.m2s2-r10b>.step{flex:1 1 0}.m2s2-r10b>.m2s2-col{flex:1.15 1 0;display:flex;flex-direction:column;gap:clamp(8px,1vw,18px)}
.m2s2-col .m2s2-tb{font-size:clamp(13px,1.1vw,21px)}.m2s2-col .m2s2-tb th,.m2s2-col .m2s2-tb td{padding:6px 8px}
.m2s2-k12 .m2b{font-size:clamp(15px,1.4vw,27px)}
.m2s2-k12 .m2s2-ceh{font-size:clamp(16px,1.5vw,29px)}
.m2s2-k11 .m2s2-bx{padding:16px 12px}.m2s2-k11 .m2s2-bh{font-size:clamp(20px,1.9vw,36px)}
.m2s2-k11 .m2s2-bt{font-size:clamp(18px,1.65vw,32px)}
.m2s2-k11 .m2pk{font-size:clamp(17px,1.5vw,29px)}.m2s2-k11 .m2pill{font-size:clamp(16px,1.4vw,27px)}
.m2s2-bigch .m2nd .ico{height:92px!important}.m2s2-bigch .m2pk{font-size:clamp(17px,1.5vw,29px)}
.m2s2-bigch .m2nd strong{font-size:clamp(18px,1.6vw,31px)}.m2s2-bigch .m2pill{font-size:clamp(16px,1.35vw,26px)}
.m2s2-bigch .m2zone{padding:22px 16px 12px}
"""
