# -*- coding: utf-8 -*-
"""Ключевые слайды RIP 2.5.1 в логике глав 1–9: надзаголовок раздела, крупный заголовок, текст pptx слева,
схема на стеклянной панели справа; холст 1600×900, масштабируется под экран. Текст — из pptx дословно."""

from _sw_lib import SL, _esc
from _rp1_fig import Fig, t, INK, RED, GRN, TEAL, BLUE


def hs(label, items):
    SL.append('<section class="slide rpfs" data-label="%s"><div class="rpcv"><div class="rpci">%s</div></div></section>'
              % (_esc(label), "".join(items)))


def at(x, y, w, html, cls="", step=False, style=""):
    c = ("cv-at " + cls + (" step" if step else "")).strip()
    return '<div class="%s" style="left:%dpx;top:%dpx;width:%dpx;%s">%s</div>' % (c, x, y, w, style, html)


def left(eb, title, paras, x=100, y=86, w=640, size=21, tsize=46):
    """Левая колонка: надзаголовок, заголовок, абзацы (первые два — сразу, остальные — по шагам)."""
    body = '<div class="hx-eb">%s</div><div class="hx-t" style="font-size:%dpx">%s</div>' % (eb, tsize, title)
    for i, para in enumerate(paras):
        body += '<div class="hx-p%s" style="font-size:%spx">%s</div>' % (" step" if i >= 2 else "", size, para)
    return at(x, y, w, body)


def glass(x, y, w, h, html, step=False, pad=26):
    return at(x, y, w, html, "hx-glass", step, "height:%dpx;padding:%dpx" % (h, pad))


def cap(text, col="#2bb38a"):
    return '<div class="hx-cap" style="color:%s">%s</div>' % (col, text)


def svg(f):
    return f.svg().replace('class="fig rpfig"', 'class="hx-svg"')


# ---------------------------------------------------------------------------------------------- pptx 1–2
def title():
    f = Fig(600, 520)
    pts = {"R1": (120, 150), "R2": (430, 100), "R3": (480, 360), "R4": (190, 400)}
    for a, b in (("R1", "R2"), ("R2", "R3"), ("R3", "R4"), ("R4", "R1")):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        f.wire(x1, y1 + 10, x2, y2 + 10, "#2bb38a", 5)
        f.raw('<circle r="9" fill="#e2557f" class="hx-fly" style="offset-path:path(\'M%g %g L%g %g\');animation-delay:%gs"/>'
              % (x1, y1 + 10, x2, y2 + 10, (x1 % 7) * .3))
    for n, (x, y) in pts.items():
        f.router(x, y, n, .85)
    hs("Титул", [
        at(150, 190, 760, '<div class="hx-eb">Глава 2.5.1 · динамическая маршрутизация</div>'
                          '<div class="hx-big">Протокол<br>RIP</div>'
                          '<div class="hx-p" style="font-size:26px;color:#3d6b5f;max-width:660px"><b>Цель главы:</b> изучить принцип '
                          'работы «Дистанционно-векторных» протоколов;</div>'
                          '<div class="hx-pills"><span>RIPv2</span><span>UDP 520</span><span>224.0.0.9</span><span>hop ≤ 15</span></div>'
                          '<div class="hx-auth">Ананко Софья Михайловна<br>Качур Анна Юрьевна</div>'),
        at(940, 170, 600, svg(f)),
    ])


# ---------------------------------------------------------------------------------------------- pptx 3
def general1():
    hs("Общие сведения о RIP", [
        left("Общие сведения", "Общие сведения<br>о RIP", [
            "Протокол маршрутной информации (<b>Routing Informational Protocol, RIP</b>) -это самый простой протокол внутренней "
            "маршрутизации, работающий на основе <b>дистанционно-векторного</b> алгоритма и определённый в RFC 1058, RIPv2 и RFC 1388.",
            "Протокол RIP использует алгоритм <b>Беллмана-Форда</b> для расчётов кратчайших путей. RIP не знает всю топологию сети и "
            "весь путь до адреса назначения, он знает только сведения, полученные от соседних RIP-маршрутизаторов: "
            "<b>расстояние</b> (дистанцию) до удалённой сети назначения; <b>направление</b> (вектор).",
            "В качестве метрики (cost или стоимости) при выборе маршрута RIP использует <b>количество переходов (hoр)</b>: чем "
            "короче путь, тем лучше маршрут. Максимальная длина маршрута равна <b>15</b> переходам, а <b>16</b> переходов "
            "означают, что сеть назначения недоступна."], size=20),
        glass(800, 110, 700, 670, cap("Вектор = направление · Расстояние = переходы (hop)") + _hops_svg()),
    ])


def _hops_svg():
    f = Fig(650, 560)
    y = 150
    f.wire(60, y, 600, y, "#2bb38a", 5)
    f.cloud(70, y, 112, 54, ["LAN1"], "blue", size=19)
    f.cloud(590, y, 112, 54, ["LAN2"], "violet", size=19)
    for x, n in ((190, "R1"), (330, "R2"), (470, "R3")):
        f.router(x, y - 12, n, .72)
    f.raw('<g class="step"><path d="M200 80 Q260 50 320 80" fill="none" stroke="#2bb38a" stroke-width="3" stroke-dasharray="7 6"/>%s</g>'
          % _chip(260, 52, "1 hop"), True)
    f.raw('<g class="step"><path d="M340 80 Q400 50 460 80" fill="none" stroke="#2bb38a" stroke-width="3" stroke-dasharray="7 6"/>%s</g>'
          % _chip(400, 52, "2 hop"), True)
    f.raw('<g class="step"><rect x="20" y="270" width="610" height="110" rx="22" fill="#fff" stroke="#cdeee0" stroke-width="2"/>'
          '%s%s</g>' % (t(50, 315, "Чем короче путь, тем лучше маршрут", 21, INK, 800, "start"),
                        t(50, 352, "R1 о сети LAN2 знает только: дистанция 2 hop, вектор → R2", 17, "#3d6b5f", 600, "start")), True)
    f.raw('<g class="step"><rect x="20" y="410" width="295" height="110" rx="22" fill="#e3f7ee" stroke="#9fdcc3" stroke-width="2"/>'
          '<text x="50" y="482" style="font:800 44px Unbounded;fill:#0f5c47">15</text>%s%s'
          '<rect x="335" y="410" width="295" height="110" rx="22" fill="#ffe4ec" stroke="#f3a3c0" stroke-width="2"/>'
          '<text x="365" y="482" style="font:800 44px Unbounded;fill:#b02a5c">16</text>%s%s</g>'
          % (t(130, 458, "максимальная", 17, INK, 700, "start"), t(130, 482, "длина маршрута", 17, INK, 700, "start"),
             t(445, 458, "сеть назначения", 17, "#b02a5c", 700, "start"), t(445, 482, "недоступна", 17, "#b02a5c", 700, "start")), True)
    return svg(f)


def _chip(x, y, s, fill="#2bb38a", col="#fff", w=None):
    w = w or len(s) * 11 + 34
    return ('<rect x="%g" y="%g" width="%g" height="38" rx="19" fill="%s"/>%s'
            % (x - w / 2, y - 19, w, fill, t(x, y + 6, s, 16, col, 800, mono=True)))


# ---------------------------------------------------------------------------------------------- pptx 4
def general2():
    # 4a · версии
    f = Fig(650, 600)
    rows = [("RIPv1", "#2fae6a", "классовый", "255.255.255.255", "без маски"),
            ("RIPv2", "#3d8fe0", "бесклассовый", "224.0.0.9", "+ маска подсети"),
            ("RIPng", "#7b61e0", "IPv6", "FF02::9", "")]
    for i, (n, c, k, a, m) in enumerate(rows[:2]):
        y = 70 + i * 190
        f.raw('<g class="step"><rect x="20" y="%d" width="610" height="160" rx="24" fill="#fff" stroke="#cdeee0" stroke-width="2"/>'
              '<rect x="44" y="%d" width="130" height="54" rx="14" fill="%s"/>%s%s'
              '<rect x="44" y="%d" width="560" height="44" rx="12" fill="#f0faf5"/>%s</g>'
              % (y, y + 22, c, t(109, y + 57, n, 22, "#fff", 800), t(200, y + 57, k + " протокол", 21, INK, 800, "start"),
                 y + 96, t(64, y + 125, "IP | маска: " + ("— не передаётся" if i == 0 else "передаётся"), 18,
                           "#b02a5c" if i == 0 else "#0f5c47", 700, "start", True)), True)
    f.raw('<g class="step"><rect x="20" y="450" width="610" height="100" rx="24" fill="#efeaff" stroke="#c9bff3" stroke-width="2"/>'
          '<rect x="44" y="473" width="130" height="54" rx="14" fill="#7b61e0"/>%s%s</g>'
          % (t(109, 508, "RIPng", 22, "#fff", 800), t(200, 508, "для работы с IPv6-адресацией", 21, INK, 800, "start")), True)
    hs("Версии RIP", [
        left("Общие сведения", "Версии RIP", [
            "<b>RIPv1</b> - классовый протокол (100% не используется);<br><b>RIPv2</b> - бесклассовый (99,9% не используется);"
            "<br><b>RIPng</b> - для работы с IPv6-адресацией.",
            "Если в сети существуют 1 и 2 версии протокола, то нужно помнить, что устройства версии 1 не поддерживают "
            "расширений, реализованных в версии 2, например, <b>не передаётся маска подсети</b>, поэтому могут возникнуть "
            "проблемы при их взаимодействии."], size=22),
        glass(800, 110, 700, 670, svg(f)),
    ])
    # 4b · обновления и типы пакетов
    g = Fig(650, 600)
    c = (325, 300)
    for i in range(3):
        g.raw('<circle cx="%d" cy="%d" r="20" fill="none" stroke="#2bb38a" stroke-width="3" class="hx-pulse" '
              'style="animation-delay:%ds"/>' % (c[0], c[1] + 8, i), False)
    for (x, y), n, anc in (((120, 140), "R2", "end"), ((530, 140), "R3", "start"), ((325, 500), "R4", "middle")):
        g.wire(c[0], c[1] + 8, x, y + 8, "#2bb38a", 5)
        g.raw('<circle r="10" fill="#2bb38a" class="hx-fly" style="offset-path:path(\'M%d %d L%d %d\')"/>' % (c[0], c[1] + 8, x, y + 8))
        g.router(x, y, "", .72)
        g.label(x + (-62 if anc == "end" else 62 if anc == "start" else 0), y + (6 if anc != "middle" else 70), n, 19, INK, 900, anc)
    g.router(c[0], c[1], "", .8)
    g.label(c[0] + 66, c[1] - 14, "R1", 19, INK, 900, "start")
    g.raw('<g class="step">%s</g>' % _chip(150, 40, "UDP · порт 520", "#fff", "#0f5c47", 230), True)
    g.raw('<g class="step">%s</g>' % _chip(500, 40, "RIPv2 → 224.0.0.9", "#0f5c47", "#fff", 250), True)
    g.raw('<g class="step"><g transform="translate(540 430)"><circle r="56" fill="#fff" stroke="#cdeee0" stroke-width="3"/>'
          '<circle r="45" fill="none" stroke="#2bb38a" stroke-width="8" stroke-dasharray="283" class="hx-clock" transform="rotate(-90)"/>'
          '<text y="8" text-anchor="middle" style="font:800 22px Unbounded;fill:#0f5c47">30 с</text></g></g>', True)
    hs("Обновления RIP", [
        left("Общие сведения", "Обновления RIP", [
            "Протокол RIP использует для рассылки протокол <b>UDP</b> с номером порта <b>520</b>. По умолчанию рассылаются "
            "<b>каждые 30 секунд</b> вне зависимости меняется топология сети или нет:",
            '<div class="hx-li v1">для <b>RIPv1</b> широковещательная рассылка на IP-адрес <span class="hx-m">255.255.255.255</span>;</div>'
            '<div class="hx-li">для <b>RIPv2</b> многоадресная рассылка на IP-адрес <span class="hx-m">224.0.0.9</span>.</div>',
            "<b>Типы пакетов.</b> RIP использует два типа пакетов для обмена маршрутной информацией: → <b>запрос</b> на получение "
            "маршрутной информации; ← <b>ответ</b> на запрос маршрутной информации."], size=21),
        glass(800, 110, 700, 670, svg(g)),
    ])
    # 4c · возможности на ESR
    cards = [("preference", "На маршрутизаторах ESR значение <b>preference</b> по умолчанию <b>100</b>."),
             ("ECMP", "При настройке протокола RIP поддерживается <b>распределение нагрузки</b> с равной стоимостью по нескольким маршрутам."),
             ("summary", "Для уменьшения количества записей в таблице маршрутизации в RIP поддерживается <b>суммирование маршрутов</b>."),
             ("auth", "Механизм <b>аутентификации</b> используется для безопасности таблиц маршрутизации.")]
    tiles = "".join('<div class="hx-tile step"><div class="hx-tk">%s</div><div>%s</div></div>' % (k, v) for k, v in cards)
    hs("Возможности RIP на ESR", [
        left("Общие сведения", "RIP на ESR", [
            "В настоящее время все версии протокола RIP на 99,999 % не используются, так как считается, что протокол устарел.",
            "В рамках курса протокол RIP представлен как <b>самый простой пример</b> настройки протоколов динамической маршрутизации."],
            size=22),
        at(800, 110, 700, '<div class="hx-tiles">%s</div>' % tiles),
    ])


# ---------------------------------------------------------------------------------------------- pptx 10
def split():
    f = Fig(660, 600)
    y = 260
    f.wire(40, y, 620, y, "#2bb38a", 5)
    f.cloud(80, y, 140, 50, ["192.168.10.0/24"], "blue", size=15)
    for x, n in ((205, "R1"), (380, "R2"), (560, "R3")):
        f.router(x, y - 12, n, .72)
    f.label(300, y + 34, "gi1/0/1", 16, INK, 800, mono=True)
    f.label(455, y + 34, "gi1/0/2", 16, INK, 800, mono=True)
    f.raw('<g class="step">%s%s</g>' % (
        '<path d="M225 200 Q292 150 360 200" fill="none" stroke="%s" stroke-width="5" marker-end="url(#%sag)"/>' % (GRN, f.k),
        _chip(292, 130, "Обновление: 192.168.10.0/24", "#2bb38a", "#fff", 300)), True)
    f.raw('<g class="step">%s%s</g>' % (
        '<path d="M400 200 Q470 150 540 200" fill="none" stroke="%s" stroke-width="5" marker-end="url(#%sab)"/>' % (BLUE, f.k),
        _chip(500, 70, "Маршрут к сети R1 →", "#e4e3ff", "#3c46a8", 230)), True)
    f.raw('<g class="step"><path d="M360 330 Q292 380 225 330" fill="none" stroke="%s" stroke-width="5" stroke-dasharray="10 8" '
          'marker-end="url(#%sar)"/><g transform="translate(292 357)"><circle r="20" fill="#fff" stroke="%s" stroke-width="3"/>'
          '<path d="M-8 -8L8 8M8 -8L-8 8" stroke="%s" stroke-width="4" stroke-linecap="round"/></g>%s</g>'
          % (RED, f.k, RED, RED, _chip(292, 420, "Не отправлять обратно через gi1/0/1", "#ffe4ec", "#b02a5c", 380)), True)
    f.raw('<g class="step"><rect x="20" y="480" width="620" height="96" rx="22" fill="#fff" stroke="#cdeee0" stroke-width="2"/>%s%s</g>'
          % (t(44, 520, "Таблица — только после сходимости", 20, INK, 800, "start"),
             t(44, 553, "оптимальный путь известен, когда сошлись все маршрутизаторы", 16, "#3d6b5f", 600, "start")), True)
    hs("Метод разделения горизонта", [
        left("Обмен данными маршрутизации", "Метод разделения<br>горизонта", [
            "Из-за медленной сходимости дистанционно-векторных протоколов может возникнуть петля маршрутизации, предотвратить "
            "которую возможно с помощью нескольких методов, один из них – метод разделения горизонта.",
            "<b><i>Метод разделения горизонта</i></b> запрещает отправку данных из того же интерфейса, от которого они были "
            "получены. Например, R2 не отправляет обновление, содержащее сеть 192.168.10.0/24, из интерфейса gi1/0/1, так как R2 "
            "получил данные о сети 192.168.10.0/24 через этот же интерфейс gi1/0/1.",
            "Маршрутизатор может использовать данные из таблицы маршрутизации для определения оптимального пути к адресу "
            "назначения <b>только после завершения процесса сходимости</b> всех маршрутизаторов в сети."], size=19.5),
        glass(800, 110, 700, 670, svg(f)),
    ])


# ---------------------------------------------------------------------------------------------- pptx 12
def bf():
    items = [("Обмен", "механизм отправки и получения данных маршрутизации; алгоритм отправляет и принимает обновления."),
             ("Расчёт", "механизм расчёта оптимальных путей и добавления маршрутов в таблицу маршрутизации; на каждом "
                        "маршрутизаторе алгоритм самостоятельно выполняет вычисления и добавляет в таблицу маршрутизации новые данные."),
             ("Изменение сети", "механизм обнаружения и реагирования на изменения в топологии; в случае сбоя сети алгоритм "
                                "выполняет построение обновления по событию и потом удаляет сеть из таблицы маршрутизации.")]
    rows = "".join('<div class="hx-proc step"><span class="hx-n">%d</span><div><div class="hx-pt">%s</div>%s</div></div>'
                   % (i + 1, k, v) for i, (k, v) in enumerate(items))
    hs("Алгоритм Беллмана–Форда", [
        left("Беллман–Форд", "Алгоритм<br>Беллмана–Форда", [
            "Протокол RIP использует алгоритм Беллмана-Форда в качестве алгоритма маршрутизации. Основан на двух алгоритмах, "
            "разработанных в 1958 и 1956 г. Ричардом Беллманом (Richard Bellman) и Лестером Фордом-мл. (Lester Ford, Jr).",
            "Различные протоколы маршрутизации используют различные алгоритмы для установки маршрутов в таблицу маршрутизации, "
            "отправки обновлений соседним устройствам и принятия решений об определении пути.",
            "Протоколы IGRP и EIGRP используют алгоритм <b>DUAL</b>, разработанный доктором Дж. Дж. Гарсия-Луна-Асевес "
            "(SRI International)."], size=20),
        glass(800, 110, 700, 670, cap("В основе дистанционно-векторного протокола лежит алгоритм маршрутизации, который "
                                      "используется для протоколов маршрутизации, определяет процессы:", "#0f5c47") + rows),
    ])


# ---------------------------------------------------------------------------------------------- pptx 22
def setup():
    stages = ["создание и настройка процесса RIP;", "настройка на интерфейсе;", "объявление сетей;", "проверка конфигурации"]
    st = "".join('<div class="hx-proc step"><span class="hx-n">%d</span><div class="hx-pt" style="margin:0">%s</div></div>'
                 % (i + 1, s) for i, s in enumerate(stages))
    pre = ["на маршрутизаторе ESR должны быть настроены IP-адреса на интерфейсах,",
           "отключён межсетевой или настроен межсетевой экран,",
           "применены и подтверждены все команды конфигурации."]
    chk = "".join('<div class="hx-chk"><span>✓</span><div>%s</div></div>' % s for s in pre)
    hs("Настройка протокола RIP", [
        left("Настройка на ESR", "Настройка<br>протокола RIP", [
            "<b>Предварительно</b> на маршрутизаторе ESR должны быть:" + chk], size=21),
        glass(800, 150, 700, 470, cap("Этапы настройки протокола RIP:", "#0f5c47") + st),
    ])


# ---------------------------------------------------------------------------------------------- pptx 27
def loops():
    tiles = [("1", "Разделение горизонта", "split horizon"), ("2", "Триггерные обновления", "triggered update"),
             ("3", "Удержание измерений", "holddown"), ("4", "Отравление маршрута", "route poisoning")]
    h = "".join('<div class="hx-tile step"><span class="hx-n">%s</span><div class="hx-pt">%s</div><div class="hx-m">%s</div></div>'
                % x for x in tiles)
    hs("Механизмы против петель", [
        left("Защита от петель", "Механизмы<br>против петель", [
            "Чтобы не возникали петли маршрутизации, «Счёт до бесконечности» и т.д., протокол RIP и другие, основанные на "
            "дистанционно-векторном алгоритме, используют несколько механизмов, которые увеличивает его стабильность, но "
            "увеличивают и время сходимости (конвергенции):"], size=22),
        at(800, 150, 700, '<div class="hx-tiles">%s</div>' % h),
    ])


def loops_defs():
    items = [
        ("1", "Разделение горизонта (split horizon)",
         "- это механизм, который запрещает маршрутизатору передавать пакеты через интерфейс, в котором они были получены."),
        ("2", "Триггерные обновления (triggered update)",
         "- это механизм, при котором маршрутизатор в случае ошибки маршрута увеличит метрику этого маршрута до 16 (то есть "
         "сделает маршрут недоступным и запрещённым) и немедленно отправит сообщение со своей таблицей маршрутизации, не "
         "дожидаясь, пока подойдёт время периодических обновлений. Это обновление присваивает маршруту статус удержания "
         "(holddown) в то время как протокол RIP пытается обнаружить альтернативный маршрут с лучшей метрикой."),
        ("3", "Удержание измерений (holddown)",
         "- это механизм, который стабилизирует маршруты, отказываясь принимать обновления маршрутов с большей метрикой для "
         "той же сети назначения на период, когда маршрут становится неактивным. Если в течение периода удержания исходный "
         "маршрут снова становится активным или маршрутизатор получает сведения о маршруте с более низкой метрикой, "
         "маршрутизатор устанавливает маршрут в таблице маршрутизации и немедленно начинает им пользоваться. Удержание "
         "используется для удаления неверных сведений о маршруте из всех маршрутизаторов в сети. Маршрутизатор обычно "
         "переходит в режим удержания при выходе из строя канала в маршруте. По умолчанию таймер удержания равен 6 "
         "интервалам update или 180 секундам."),
        ("4", "Отравление или запрет маршрута (route poisoning)",
         "- это установка метрики маршрута равной 16 для прекращения трафика по данному маршруту и немедленная отправка "
         "триггерных обновлений по событию, запрещая маршрут."),
    ]
    boxes = [(100, 170, 690, 210), (810, 170, 690, 360), (100, 395, 690, 450), (810, 545, 690, 300)]
    out = [at(100, 70, 1400, '<div class="hx-eb">Защита от петель</div><div class="hx-t" style="font-size:42px">'
                              'Механизмы против петель: определения</div>')]
    for (n, ttl, txt), (x, y, w, h) in zip(items, boxes):
        fs = 17 if len(txt) > 300 else 20
        out.append(glass(x, y, w, h, '<div class="hx-dh"><span class="hx-n">%s</span><div class="hx-pt">%s</div></div>'
                                     '<div class="hx-p" style="font-size:%spx;margin-top:10px">%s</div>' % (n, ttl, fs, txt),
                         step=True, pad=22))
    hs("Механизмы против петель · определения", out)


def summary():
    cards = [("RIP", ["Дистанционно-векторный, алгоритм Беллмана–Форда.", "Метрика — hop: 15 предел, <b>16</b> — недоступна.",
                      "UDP <b>520</b>, обновления каждые 30 с; RIPv2 → <b>224.0.0.9</b>."]),
             ("Сходимость и петли", ["Этапы: запуск, обнаружение, обмен, сходимость.",
                                     "Split horizon, triggered update, holddown, route poisoning.",
                                     "Таймеры update 30 / invalid 180 / flush 240."]),
             ("ESR", ["<b>router rip</b> → network / redistribute → passive-interface → timers → <b>enable</b>.",
                      "Применение: <b>commit</b> и <b>confirm</b>.",
                      "Проверка: show running-config routing rip, show ip route rip."])]
    out = [at(100, 80, 1400, '<div class="hx-eb">Итоги</div><div class="hx-t" style="font-size:52px">Что запомнить</div>')]
    for i, (ttl, items) in enumerate(cards):
        body = '<div class="hx-dh"><span class="hx-n">%d</span><div class="hx-pt">%s</div></div>' % (i + 1, ttl)
        body += "".join('<div class="hx-sum">%s</div>' % x for x in items)
        out.append(glass(100 + i * 475, 250, 450, 470, body, step=True, pad=28))
    hs("Что запомнить", out)


def finale():
    f = Fig(600, 520)
    pts = {"R1": (120, 150), "R2": (430, 100), "R3": (480, 360), "R4": (190, 400)}
    for a, b in (("R1", "R2"), ("R2", "R3"), ("R3", "R4"), ("R4", "R1")):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        f.wire(x1, y1 + 10, x2, y2 + 10, "#2bb38a", 5)
        f.raw('<circle r="9" fill="#e2557f" class="hx-fly" style="offset-path:path(\'M%g %g L%g %g\');animation-delay:%gs"/>'
              % (x1, y1 + 10, x2, y2 + 10, (x1 % 7) * .3))
    for n, (x, y) in pts.items():
        f.router(x, y, n, .85)
    hs("Финал", [
        at(150, 230, 760, '<div class="hx-eb">Раздел 2.5.1 · Протокол RIP</div>'
                          '<div class="hx-big" style="font-size:88px">Спасибо<br>за внимание</div>'
                          '<div class="hx-pills"><span>VKontakte</span><span>Telegram</span></div>'
                          '<div class="hx-p" style="font-size:22px;color:#3d6b5f">Вопросы по лекции и лабораторным — пишите.</div>'),
        at(940, 170, 600, svg(f)),
    ])


CSS = r"""
.hx-sum{margin-top:14px;padding:14px 18px;border-radius:18px;background:rgba(255,255,255,.75);border:1.5px solid #fff;
 font:400 19px/1.45 "Golos Text";color:#123d33}
.hx-sum b{color:#0f5c47;font-weight:800}
.rpci .hx-svg{display:block;width:100%;height:auto}
.hx-eb{font:800 15px/1 "Golos Text",sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#2bb38a}
.hx-t{font-family:"Unbounded",sans-serif;font-weight:800;line-height:1.08;color:#0f5c47;letter-spacing:-.01em;margin-top:14px}
.hx-big{font:800 104px/1 "Unbounded",sans-serif;color:#0f5c47;letter-spacing:-.025em;margin-top:22px}
.hx-p{font-family:"Golos Text",sans-serif;font-weight:400;line-height:1.5;color:#123d33;margin-top:18px}
.hx-p b{font-weight:800;color:#0f5c47}
.hx-m{font-family:"JetBrains Mono",monospace;font-weight:700;color:#0f5c47}
.hx-pills{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.hx-pills span{padding:9px 18px;border-radius:999px;background:rgba(255,255,255,.75);border:1.5px solid rgba(43,179,138,.35);
 font:700 18px/1 "JetBrains Mono",monospace;color:#0f5c47}
.hx-auth{margin-top:40px;font:500 19px/1.6 "Golos Text";color:#3d6b5f}
.hx-glass{background:rgba(255,255,255,.62);border:1.5px solid rgba(255,255,255,.9);border-radius:28px;
 box-shadow:0 30px 60px -30px rgba(15,92,71,.35),inset 0 1px 0 #fff;backdrop-filter:blur(14px);display:flex;flex-direction:column;gap:14px}
.hx-cap{font:800 15px/1.4 "Golos Text";letter-spacing:.12em;text-transform:uppercase}
.hx-li{margin-top:10px;padding:14px 20px;border-radius:18px;background:rgba(255,255,255,.7);border:1.5px solid #fff;
 box-shadow:0 14px 30px -20px rgba(15,92,71,.4)}
.hx-li.v1 .hx-m,.hx-li.v1 b{color:#3c46a8}
.hx-tiles{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.hx-tile{background:rgba(255,255,255,.66);border:1.5px solid #fff;border-radius:26px;padding:26px;min-height:200px;
 box-shadow:0 26px 50px -30px rgba(15,92,71,.4);font:400 20px/1.45 "Golos Text";color:#123d33;display:flex;flex-direction:column;gap:12px}
.hx-tile b{color:#0f5c47;font-weight:800}
.hx-tk{font:700 17px "JetBrains Mono",monospace;color:#2bb38a;letter-spacing:.04em}
.hx-proc{display:flex;gap:18px;align-items:flex-start;background:#fff;border:1.5px solid #cdeee0;border-radius:22px;padding:18px 22px;
 font:400 18.5px/1.45 "Golos Text";color:#123d33}
.hx-pt{font:800 22px/1.2 "Unbounded",sans-serif;color:#0f5c47;margin-bottom:6px}
.hx-n{flex:none;width:46px;height:46px;border-radius:50%;background:#2bb38a;color:#fff;display:flex;align-items:center;
 justify-content:center;font:800 21px/1 "Unbounded",sans-serif;box-shadow:0 0 0 6px #d8f4e8}
.hx-dh{display:flex;gap:14px;align-items:center}
.hx-dh .hx-pt{margin:0;font-size:20px}
.hx-chk{display:flex;gap:14px;align-items:flex-start;margin-top:14px;padding:14px 18px;border-radius:18px;background:rgba(255,255,255,.7);
 border:1.5px solid #fff;font-size:inherit}
.hx-chk span{flex:none;width:30px;height:30px;border-radius:50%;background:#2bb38a;color:#fff;display:flex;align-items:center;
 justify-content:center;font-weight:800}
@keyframes hxfly{0%{offset-distance:0%;opacity:0}10%{opacity:1}90%{opacity:1}100%{offset-distance:100%;opacity:0}}
@keyframes hxpulse{0%{r:20;opacity:.7}100%{r:130;opacity:0}}
@keyframes hxclock{from{stroke-dashoffset:283}to{stroke-dashoffset:0}}
.hx-fly{animation:hxfly 2.8s linear infinite}
.hx-pulse{animation:hxpulse 3s ease-out infinite}
.hx-clock{animation:hxclock 3s linear infinite}
"""
