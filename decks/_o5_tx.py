# -*- coding: utf-8 -*-
"""Дословная расшифровка картинок-скриншотов pptx «OSPF 2 5».
Подписи «Рисунок …», номера страниц и логотипы методички не включены.
Разметка в doc: <b>…</b> — жирный; <i>…</i> — курсив; <r>…</r> — красный текст; <bl>…</bl> — синий текст.
Угловые скобки параметров в doc экранированы: &lt;…&gt;.
Выравнивание колонок CLI восстановлено по моноширинной сетке картинки (±1 знак).
Опечатки оригинала сохранены (см. поля "note" / "orig_errors")."""


def _row(*cells):
    """cells: пары (колонка, текст) → строка с пробелами-выравниванием."""
    s = ""
    for col, txt in cells:
        s = s.ljust(col) + txt
    return s


def _help(col, pairs, indent=2):
    """Вывод контекстной справки CLI: команда + описание с колонки col."""
    return [_row((indent, a), (col, b)) if b else " " * indent + a for a, b in pairs]


def _kv(col, pairs):
    return [_row((0, a), (col, b)) for a, b in pairs]


_IF_R1 = [
    ("Interface:", "gigabitethernet 1/0/1"),
    ("Internet Address:", "172.16.10.0/24"),
    ("Router ID:", "1.1.1.1"),
    ("Network Type:", "broadcast"),
    ("Area:", "1.1.1.1 (16843009)"),
    ("Interface has:", "no authentication"),
    ("Transmit:", "1"),
    ("State:", "DR"),
    ("Priority:", "128"),
    ("Cost:", "10"),
    ("ECMP weight:", "1"),
    ("Hello timer:", "10"),
    ("Wait timer:", "40"),
    ("Dead timer:", "40"),
    ("Retransmit timer:", "5"),
    ("Designated router (ID):", "1.1.1.1"),
    ("Designated router (IP):", "172.16.10.1"),
    ("Backup designated router (ID):", "2.2.2.2"),
    ("Backup designated router (IP):", "172.16.10.100"),
    ("Neighbor Count:", "1"),
    ("Adjacent neighbor count:", "1"),
    ("  Adjacent with neighbor:", "2.2.2.2 (backup)"),
]
_R2_DIFF = {"Router ID:": "2.2.2.2", "State:": "Backup", "  Adjacent with neighbor:": "1.1.1.1 (dr)"}
_IF_R2 = [(k, _R2_DIFF.get(k, v)) for k, v in _IF_R1]

_NB_HDR = [
    _row((0, "Router ID"), (16, "Pri"), (21, "State"), (37, "DTime"), (44, "Interface"), (63, "Router IP")),
    _row((0, "---------"), (16, "---"), (21, "-----"), (37, "-----"), (44, "-----------------"), (63, "---------")),
]

_PATHS_R1 = [  # общая часть s19/s20: сеть → [(путь, метрика)]
    ("192.168.1.0/24", [("напрямую", "0")]),
    ("192.168.2.0/24", [("R1-R2", "21"), ("R1-R4-R3-R2", "41"), ("R1-R5-R4-R3-R2", "36")]),
    ("192.168.3.0/24", [("R1-R2-R3", "31"), ("R1-R4-R3", "31"), ("R1-R5-R4-R3", "26")]),
    ("192.168.4.0/24", [("R1-R4", "21"), ("R1-R5-R4", "16"), ("R1-R2-R3-R4", "41")]),
    ("192.168.5.0/24", [("R1-R5", "6"), ("R1-R4-R5", "36"), ("R1-R2-R3-R4-R5", "51")]),
    ("203.0.113.0/30", [("напрямую", "0")]),
    ("203.0.113.4/30", [("R1-R2", "30"), ("R1-R4-R3", "40"), ("R1-R5-R4-R3", "35")]),
    ("203.0.113.8/30", [("R1-R4", "30"), ("R1-R2-R3", "40")]),
    ("203.0.113.12/30", [("напрямую", "0")]),
    ("203.0.113.16/30", [("напрямую", "0")]),
    ("203.0.113.20/30", [("R1-R5", "15"), ("R1-R4", "30"), ("R1-R2-R3-R4", "50")]),
]
# сеть повторяется в каждой строке (на картинке — объединённая ячейка)
_ALL_PATHS_ROWS = [[net, p, m] for net, ps in _PATHS_R1 for p, m in ps]
_BEST_R1 = [
    ["192.168.1.0/24", "напрямую", "0"], ["192.168.2.0/24", "R1-R2", "21"],
    ["192.168.3.0/24", "R1-R5-R4-R3", "26"], ["192.168.4.0/24", "R1-R5-R4", "16"],
    ["192.168.5.0/24", "R1-R5", "6"], ["203.0.113.0/30", "напрямую", "0"],
    ["203.0.113.4/30", "R1-R2", "30"], ["203.0.113.8/30", "R1-R4", "30"],
    ["203.0.113.12/30", "напрямую", "0"], ["203.0.113.16/30", "напрямую", "0"],
    ["203.0.113.20/30", "R1-R5", "15"],
]

TX = {
    # ---------- s15: топология (схема; текстом — для перерисовки) ----------
    "s15_image20": {
        "kind": "table",
        "tables": [
            {"title": "Маршрутизаторы и LAN (метрика LAN-интерфейса — красным)",
             "cols": ["Маршрутизатор", "LAN", "Сеть", "Метрика"],
             "rows": [["R1", "LAN1", "192.168.1.0/24", "1"], ["R2", "LAN2", "192.168.2.0/24", "1"],
                      ["R3", "LAN3", "192.168.3.0/24", "1"], ["R4", "LAN4", "192.168.4.0/24", "1"],
                      ["R5", "LAN5", "192.168.5.0/24", "1"]]},
            {"title": "Каналы между маршрутизаторами (метрика — красным)",
             "cols": ["Канал", "Сеть", "Метрика"],
             "rows": [["R1—R2", "203.0.113.0/30", "20"], ["R2—R3", "203.0.113.4/30", "10"],
                      ["R3—R4", "203.0.113.8/30", "10"], ["R1—R4", "203.0.113.12/30", "20"],
                      ["R1—R5", "203.0.113.16/30", "5"], ["R4—R5", "203.0.113.20/30", "10"]],
             "note": "Схема: R1 слева сверху, R2 справа сверху, R3 справа снизу, R4 слева снизу, "
                     "R5 в центре; облака LAN: LAN1 оранжевое, LAN2 зелёное, LAN3 жёлтое, "
                     "LAN4 голубое, LAN5 сиреневое."},
        ],
    },
    # ---------- s19: таблицы соседей R1..R5 → все пути от R1 ----------
    "s19_image25": {
        "kind": "table",
        "tables": [
            {"title": "R1", "cols": ["Сеть", "Метрика", "Сосед"],
             "rows": [["192.168.1.0/24", "1", "нет"], ["203.0.113.0/30", "20", "R2"],
                      ["203.0.113.12/30", "20", "R4"], ["203.0.113.16/30", "5", "R5"]]},
            {"title": "R2", "cols": ["Сеть", "Метрика", "Сосед"],
             "rows": [["192.168.2.0/24", "1", "нет"], ["203.0.113.0/30", "20", "R1"],
                      ["203.0.113.4/30", "10", "R3"], ["", "", ""]]},
            {"title": "R3", "cols": ["Сеть", "Метрика", "Сосед"],
             "rows": [["192.168.3.0/24", "1", "нет"], ["203.0.113.4/30", "10", "R2"],
                      ["203.0.113.8/30", "10", "R4"], ["", "", ""]]},
            {"title": "R4", "cols": ["Сеть", "Метрика", "Сосед"],
             "rows": [["192.168.4.0/24", "1", "нет"], ["203.0.113.12/30", "20", "R1"],
                      ["203.0.113.8/30", "10", "R3"], ["203.0.113.20/30", "10", "R5"]]},
            {"title": "R5", "cols": ["Сеть", "Метрика", "Сосед"],
             "rows": [["192.168.5.0/24", "1", "нет"], ["203.0.113.16/30", "5", "R1"],
                      ["203.0.113.20/30", "10", "R4"], ["", "", ""]],
             "note": "Столбец «Сосед» — красным. Пустая 4-я строка у R2, R3, R5 есть на картинке. "
                     "Шапки таблиц в цвет маршрутизатора (R1 персик, R2 зелёный, R3 жёлтый, R4 голубой, "
                     "R5 сиреневый). Синие стрелки ведут к таблице путей справа."},
            {"title": "Пути от R1 (справа)", "cols": ["Сеть", "Путь", "Метрика"],
             "rows": _ALL_PATHS_ROWS,
             "note": "Сеть — объединённая ячейка на все свои пути; все значения чёрные."},
        ],
    },
    # ---------- s20: выбор лучших путей ----------
    "s20_image27": {
        "kind": "table",
        "tables": [
            {"title": "Все пути (слева)", "cols": ["Сеть", "Путь", "Метрика"],
             "rows": _ALL_PATHS_ROWS,
             "note": "Красным выделены лучшие: «напрямую»/0 у прямых сетей, R1-R2 21, R1-R5-R4-R3 26, "
                     "R1-R5-R4 16, R1-R5 6, R1-R2 30 (203.0.113.4/30), R1-R4 30, R1-R5 15."},
            {"title": "Лучшие пути (справа, после синей стрелки)", "cols": ["Сеть", "Путь", "Метрика"],
             "rows": _BEST_R1, "note": "Путь и метрика — красным, сеть — чёрным."},
        ],
    },
    # ---------- s21: лучшие пути → таблица маршрутизации R1 ----------
    "s21_image28": {
        "kind": "table",
        "tables": [
            {"title": "", "cols": ["Сеть", "Путь", "Метрика"], "rows": _BEST_R1,
             "note": "Справа: синяя стрелка → значок R1, под ним пустая плашка «ТАБЛИЦА МАРШРУТИЗАЦИИ» "
                     "(заголовок + 3 пустые строки)."},
        ],
    },
    # ---------- s35: типы областей ----------
    "s35_image45": {
        "kind": "table",
        "tables": [{
            "title": "", "cols": ["Тип области", "Что получает", "Внешние маршруты и ASBR", "Для чего подходит"],
            "rows": [
                ["<b>Backbone, Area 0</b>", "Полную информацию, нужную для связи областей",
                 "Поддерживает внешние маршруты", "Магистраль OSPF"],
                ["<b>Standard, обычная</b>", "Внутренние и межобластные маршруты, внешние маршруты",
                 "Принимает внешние маршруты; ASBR разрешён", "Область без специальных ограничений"],
                ["<b>Stub, тупиковая</b>",
                 "Внутренние и межобластные маршруты; обычно получает маршрут по умолчанию",
                 "Внешние LSA типа 5 не принимает; ASBR в такой области не размещают",
                 "Область, которой не нужны отдельные маршруты из внешних источников"],
                ["<b>Totally Stubby</b>", "Внутренние маршруты и маршрут по умолчанию",
                 "Не получает подробные межобластные и внешние маршруты; ASBR не размещают",
                 "Упрощённая таблица маршрутизации в периферийной области"],
                ["<b>NSSA</b>",
                 "Внутренние и межобластные маршруты; внешние маршруты можно вводить внутри области",
                 "Внешние LSA типа 5 не принимает напрямую. Локальный ASBR может объявлять внешние "
                 "маршруты внутри NSSA через LSA типа 7",
                 "Периферийная область, которой нужно вводить собственные внешние маршруты"],
                ["<b>Totally NSSA</b>", "Внутренние маршруты и, как правило, маршрут по умолчанию",
                 "Разрешает локальное введение внешних маршрутов через LSA типа 7, но ограничивает "
                 "подроб[…] маршруты извне области",
                 "Сочетает ограничения Totally Stubby с возможностью локально вводить внешние маршруты"],
            ],
            "note": "Скриншот чата: в последней строке слово «подроб…» перекрыто кнопкой прокрутки «↓» "
                    "(вероятно «подробные»); слово «области» обрезано снизу.",
        }],
    },
    # ---------- s47: Opaque LSA ----------
    "s47_image72": {
        "kind": "table",
        "tables": [{
            "title": "", "cols": ["OSPFv2 LSA", "Где распространяется", "Пример назначения"],
            "rows": [
                ["<b>Type 9 Opaque</b>", "Только по одному каналу", "Информация, нужная соседям на этом канале"],
                ["<b>Type 10 Opaque</b>", "В пределах одной области", "Traffic Engineering и другие расширения области"],
                ["<b>Type 11 Opaque</b>", "По всей OSPF-системе, где такой тип разрешён",
                 "Расширения с областью распространения уровня AS"],
            ],
        }],
    },
    # ---------- s50: LSA по типам областей ----------
    "s50_image78": {
        "kind": "table",
        "tables": [{
            "title": "Какие LSA используются в каждом типе области",
            "cols": ["Область", "Объявления внутри области", "Что приходит от других областей",
                     "Внешние маршруты", "Маршрут по умолчанию"],
            "rows": [
                ["<b>Backbone — Area 0</b>",
                 "LSA-1, LSA-2; также могут распространяться другие допустимые для этой области объявления",
                 "Area 0 принимает и передаёт межобластные сведения",
                 "LSA-5, если область настроена как обычная",
                 "Не требуется автоматически для всех маршрутизаторов"],
                ["<b>Standard — обычная</b>", "LSA-1, LSA-2", "LSA-3 и, когда нужен путь к ASBR, LSA-4",
                 "Принимает LSA-5", "Не обязателен"],
                ["<b>Stub</b>", "LSA-1, LSA-2", "Принимает межобластные LSA-3",
                 "LSA-5 и LSA-4 не передаются; ASBR внутри области не размещают",
                 "ABR обычно объявляет default через LSA-3"],
                ["<b>Totally Stubby</b>", "LSA-1, LSA-2", "Подробные межобластные маршруты обычно скрыты",
                 "LSA-4 и LSA-5 не передаются; ASBR внутри области не размещают",
                 "ABR обычно объявляет default через LSA-3"],
                ["<b>NSSA</b>", "LSA-1, LSA-2; локальные внешние маршруты — LSA-7",
                 "Обычно получает межобластные маршруты через LSA-3",
                 "Входящие LSA-5 не принимаются; внешний маршрут, введённый местным ASBR, объявляется через LSA-7",
                 "ABR объявляет маршрут по умолчанию; формат и настройка зависят от конфигурации"],
                ["<b>Totally NSSA</b>", "LSA-1, LSA-2 и локальные внешние LSA-7",
                 "Подробные межобластные маршруты обычно скрыты",
                 "LSA-5 извне не принимается; локальные внешние маршруты LSA-7 сохраняются",
                 "Обычно используется маршрут по умолчанию от ABR"],
            ],
            "note": "Заголовок над таблицей обрезан сверху (читается «Какие LSA используются в каждом типе области»).",
        }],
    },
    # ---------- s55: коды show ip route ----------
    "s55_image89": {
        "kind": "cli",
        "lines": [
            "esr# sh ip route",
            " Codes: C - connected, S - static, R - RIP derived,",
            "        O - OSPF derived, IA - OSPF inter area route,",
            "        E1 - OSPF external type 1 route, E2 - OSPF external type 2 route",
            "        B - BGP derived, D - DHCP derived, K - kernel route, V - VRRP route",
            "        i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area",
            "        * - FIB route",
        ],
        "marks": [{"n": 0, "lines": [2, 3], "style": "серая подсветка строк (не рамка, без цифры)"}],
        "note": "Последняя строка обрезана снизу, видна только верхушка — читается как «* - FIB route».",
    },
    # ---------- s62: типы сетей ----------
    "s62_image98": {
        "kind": "table",
        "tables": [{
            "title": "", "cols": ["Тип сети", "Пример", "Как обнаруживаются соседи", "DR/BDR"],
            "rows": [
                ["<b>Point-to-Point</b>", "Канал между двумя маршрутизаторами", "Прямой обмен по каналу", "Нет"],
                ["<b>Broadcast Multi-Access</b>", "Общий Ethernet-сегмент", "Обычно автоматически, через multicast", "Да"],
                ["<b>NBMA</b>", "Общая сеть Frame Relay без broadcast", "Часто адресно, соседей задают вручную", "Обычно да"],
                ["<b>Point-to-Multipoint</b>", "Hub-and-spoke через общую транспортную сеть",
                 "Multicast, если поддерживается; иначе адресно", "Нет"],
            ],
        }],
    },
    # ---------- s65: show ip ospf interface на R1 и R2 (два окна) ----------
    "s65_image101": {
        "kind": "cli",
        "lines": (["R1# show ip ospf interface gigabitethernet 1/0/1"] + _kv(32, _IF_R1)
                  + ["R2# show ip ospf interface gigabitethernet 1/0/1"] + _kv(32, _IF_R2)),
        "split": 23,  # с этой строки — второе окно (R2)
        "marks": [
            {"n": 1, "lines": [8, 9]}, {"n": 2, "lines": [16, 17, 18, 19]}, {"n": 3, "lines": [20, 21, 22]},
            {"n": 1, "lines": [31, 32]}, {"n": 2, "lines": [39, 40, 41, 42]}, {"n": 3, "lines": [43, 44, 45]},
        ],
    },
    # ---------- s67: show ip ospf neighbors на R1 и R2 (два окна) ----------
    "s67_image103": {
        "kind": "cli",
        "lines": ["R1# show ip ospf neighbors"] + _NB_HDR + [
            _row((0, "2.2.2.2"), (16, "128"), (21, "Full/BDR"), (37, "00:30"), (44, "gi1/0/1"), (63, "172.16.10.100")),
            "R1#",
            "R2# show ip ospf neighbors"] + _NB_HDR + [
            _row((0, "1.1.1.1"), (16, "128"), (21, "Full/DR"), (37, "00:32"), (44, "gi1/0/1"), (63, "172.16.10.1")),
            "R2#",
        ],
        "split": 5,
    },
    # ---------- s75: создание процесса ----------
    "s75_image111": {
        "kind": "cli",
        "lines": [
            "esr# config",
            "esr(config)# router ospf 777",
            "esr(config-ospf)# router-id 7.7.7.7",
            "esr(config-ospf)# area 0.0.0.0",
            "esr(config-ospf-area)# enable",
            "esr(config-ospf-area)# exit",
            "esr(config-ospf)# enable",
            "esr(config-ospf)# exit",
            "esr(config)#",
        ],
    },
    # ---------- s76 ----------
    "s76_image113": {
        "kind": "cli",
        "lines": ["esr(config-ospf)# area 0.0.0.0", "esr(config-ospf-area)#"] + _help(33, [
            ("area-type", "Configure area type"),
            ("default-information-originate", "Enable propagation default summary route to the NSSA"),
            ("do", "Execute a privileged mode command"),
            ("enable", "Enable OSPF area"),
            ("end", "Return to the root view"),
            ("exit", "Exit to the next highest mode in the CLI mode hierarchy"),
            ("help", "Show an overview of the CLI syntax"),
            ("network", "Add network for advertise"),
            ("no", "Negate command"),
            ("summary-address", "Configure summary-address"),
            ("virtual-link", "Configure OSPF virtual link"),
        ]) + ["esr(config-ospf-area)# area-type"] + _help(10, [
            ("normal", "Normal or backbone area"), ("nssa", "NSSA area"), ("stub", "Stub area"),
        ]) + ["", "esr(config-ospf-area)# area-type nssa"] + _help(14, [
            ("no-summary", "Totally NSSA area"), ("<cr>", ""),
        ]),
        "note": "Строки 0–12 мелким шрифтом, с «area-type» — крупнее: склейка двух скриншотов.",
    },
    "s76_image112": {
        "kind": "doc",
        "blocks": [
            {"t": "h", "text": "<b>Шаги создания и настройки OSPF:</b>"},
            {"t": "p", "text": "1) Создать OSPF процесс:"},
            {"t": "cmd", "text": "esr(config)# <b>router ospf &lt;OSPF process id&gt;</b>"},
            {"t": "p", "text": "2) Указать идентификатор маршрутизатора (router id) в формате IPv4-адреса:"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>router-id &lt;A.B.C.D&gt;</b>"},
            {"t": "p", "text": "3) Настроить хотя бы одну область (area) и активировать её:"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>area &lt;A.B.C.D&gt;</b>"},
            {"t": "cmd", "text": "esr(config-ospf-area)# <b>enable</b>"},
            {"t": "cmd", "text": "esr(config-ospf-area)# <b>exit</b>"},
            {"t": "p", "text": "4) Активировать OSPF процесс:"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>enable</b>"},
        ],
    },
    # ---------- s77 ----------
    "s77_image114": {
        "kind": "cli",
        "lines": ["esr(config)# interface gigabitethernet 1/0/1", "esr(config-if-gi)# ip ospf"] + _help(23, [
            ("area", "Bind OSPF area"),
            ("authentication", "Configure OSPF interface authentication"),
            ("bfd-enable", "Enable BFD"),
            ("cost", "Configure OSPF cost"),
            ("dead-interval", "Configure OSPF dead interval"),
            ("hello-interval", "Configure OSPF hello interval"),
            ("instance", "Bind OSPF process"),
            ("mtu-ignore", "Disable MTU mismatch detection on an interface"),
            ("neighbor", "Configure OSPF neighbor"),
            ("network", "Configure OSPF network type"),
            ("poll-interval", "Configure OSPF poll interval"),
            ("priority", "Configure OSPF priority"),
            ("retransmit-interval", "Configure OSPF retransmit interval"),
            ("wait-interval", "Configure OSPF wait interval"),
            ("<cr>", ""),
        ]),
    },
    # ---------- s78 ----------
    "s78_image116": {
        "kind": "doc",
        "blocks": [
            {"t": "h", "text": "<b>Шаги настройки на интерфейсе:</b>"},
            {"t": "p", "text": "1) Зайти на интерфейс:"},
            {"t": "cmd", "text": "esr(config)# <b>interface &lt;interface&gt;</b>"},
            {"t": "p", "text": "2) Указать номер OSPF процесса:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf instance &lt;OSPF process id&gt;</b>"},
            {"t": "p", "text": "3) Указать область (area):"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf area &lt;A.B.C.D&gt;</b>"},
            {"t": "p", "text": "4) Активировать OSPF процесс на интерфейсе:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf</b>"},
            {"t": "p", "text": "5) Применить (commit) и подтвердить (confirm). И настроить OSPF на удаленной стороне."},
        ],
    },
    "s78_image115": {
        "kind": "cli",
        "lines": [
            "esr(config-if-gi)# ip ospf instance 777",
            "esr(config-if-gi)# ip ospf area 0.0.0.0",
            "esr(config-if-gi)# ip ospf",
            "esr(config-if-gi)# exit",
            "esr(config)#",
        ],
        "note": "Внизу обрезана ещё одна строка (видна только верхушка, похоже на «esr(config)#»).",
    },
    "s78_image117": {
        "kind": "cli",
        "lines": ["esr# show running-config routing ospf"],
        "columns": {
            "ESR-1": [
                "ESR-1:",
                "router ospf 100",
                "  router-id 1.1.1.1",
                "  area 8.0.0.0",
                "    enable",
                "  exit",
                "  enable",
                "exit",
                "",
                "interface gigabitethernet 1/0/1",
                "  ip ospf instance 100",
                "  ip ospf network point-to-point",
                "  ip ospf area 8.0.0.0",
                "  ip ospf",
                "exit",
            ],
            "ESR-2": [
                "ESR-2:",
                "router ospf 100",
                "  router-id 2.2.2.2",
                "  area 8.0.0.0",
                "    enable",
                "  exit",
                "  enable",
                "exit",
                "",
                "interface gigabitethernet 1/0/1",
                "  ip ospf instance 100",
                "  ip ospf network point-to-point",
                "  ip ospf area 8.0.0.0",
                "  ip ospf",
                "exit",
            ],
        },
        "note": "Документ, не консоль: «esr#» обычным моноширинным, «show running-config routing ospf» жирным; "
                "конфиги ESR-1 (слева) и ESR-2 (справа) жирным моноширинным. Топология под ними не расшифровывалась.",
    },
    # ---------- s79 ----------
    "s79_image118": {
        "kind": "cli",
        "lines": [
            "esr(config-if-gi)# ip ospf authentication algorithm md5",
            "esr(config-if-gi)# ip ospf authentication key ascii-text ELTEXPAS",
            "esr(config-if-gi)# ip ospf network",
        ] + _help(23, [
            ("broadcast", "Set OSPF network type to broadcast"),
            ("non-broadcast", "Set OSPF network type to nonbroadcast multiaccess (NBMA)"),
            ("point-to-multipoint", "Set OSPF network type to point-to-multipoint"),
            ("point-to-point", "Set OSPF network type to point-to-point"),
        ]),
    },
    # ---------- s80 ----------
    "s80_image119": {
        "kind": "doc",
        "blocks": [
            {"t": "p", "text": "DR.", "cut": True},
            {"t": "p", "text": "Установить IP-адрес соседа:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf neighbor &lt;A.B.C.D&gt; [eligible]</b>"},
            {"t": "p", "text": "<b>[eligible]</b> – это опциональный параметр, позволяющий устройству "
                               "участвовать в процессе выбора DR в NBMA-сетях."},
            {"t": "p", "text": "Установить тип сети:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf network &lt;TYPE&gt;</b>"},
            {"t": "p", "text": "Где <b>&lt;TYPE&gt;:</b>"},
            {"t": "li", "text": "broadcast – тип соединения широковещательный (по умолчанию);"},
            {"t": "li", "text": "non-broadcast – тип соединения NBMA;"},
            {"t": "li", "text": "point-to-multipoint – тип соединения точка-многоточие;"},
            {"t": "li", "text": "point-to-point – тип соединения точка-точка."},
            {"t": "p", "text": "Включение аутентификации:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf authentication algorithm md5</b>"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf authentication key ascii-text &lt;password&gt;</b>"},
            {"t": "p", "text": "Назначение стоимости (метрики) интерфейса:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf cost &lt;1-65535&gt;</b>"},
            {"t": "p", "text": "Отключение детектирования несовпадения MTU на интерфейсе:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf mtu-ignore</b>"},
            {"t": "p", "text": "Установить OSPF приоритет, учитывающийся при выборе DR и BDR:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf priority &lt;0-255&gt;</b>"},
        ],
        "note": "Склейка двух страниц методички (стр. 75 → следующая, с логотипом «Академия Eltex»); "
                "«DR.» — обрезанный хвост предыдущего абзаца; «<password>» в оригинале перенесено на новую строку.",
        "orig_errors": ["«DR и BDR» — опечатка, должно быть BDR"],
    },
    # ---------- s81 ----------
    "s81_image121": {
        "kind": "doc",
        "blocks": [
            {"t": "p", "text": "<b><i>Redistribute</i></b> – механизм, анонсирующий маршруты на основании их "
                               "происхождения, протокола или процесса в другие области."},
            {"t": "p", "text": "Анонсирование напрямую подключённых маршрутов:"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>redistribute connected [route-map &lt;NAME-RM&gt;]</b>"},
            {"t": "p", "text": "Анонсирование статических маршрутов:"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>redistribute static [route-map &lt;NAME-RM&gt;]</b>"},
            {"t": "p", "text": "Анонсирование  маршрутов, полученных по протоколу RIP:"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>redistribute rip [route-map &lt;NAME-RM&gt;]</b>"},
            {"t": "p", "text": "Анонсирование  маршрутов, полученных по протоколу OSPF:"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>redistribute ospf  &lt;ID&gt; &lt;ROUTE-TYPE&gt; "
                                 "[route-map &lt;NAME-RM&gt;]</b>"},
            {"t": "p", "text": "Анонсирование маршрутов из таблицы маршрутизации для других BGP процессов:"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>redistribute bgp &lt;ASN&gt; [route-map &lt;NAME-RM&gt;]</b>"},
            {"t": "p", "text": "Например, создана новая LAN на маршрутизаторе, и настроен шлюз по умолчанию, "
                               "чтобы эту сеть не прописывать через network, используется redistribute connected."},
        ],
        "note": "Двойные пробелы «Анонсирование  маршрутов» и «ospf  <ID>» — как в оригинале; "
                "в оригинале «route-/map» перенесено на новую строку.",
        "orig_errors": ["«[route-map <NAME-RM>]» — лишняя открывающая скобка"],
    },
    "s81_image120": {
        "kind": "cli",
        "lines": ["esr(config-ospf)# redistribute"] + _help(12, [
            ("bgp", "Redistribute BGP routes to OSPF"),
            ("connected", "Redistribute directly connected networks to OSPF"),
            ("isis", "Redistribute ISIS routes to OSPF"),
            ("ospf", "Redistribute OSPF routes to OSPF"),
            ("rip", "Redistribute RIP routes to OSPF"),
            ("static", "Redistribute static routes to OSPF"),
        ]),
    },
    # ---------- s82 ----------
    "s82_image123": {
        "kind": "doc",
        "blocks": [
            {"t": "p", "text": "<b><i>Network</i></b> – это механизм, который позволяет анонсировать конкретный "
                               "маршрут в другие области. Командой network включается анонсирование указанной подсети."},
            {"t": "p", "text": "Из режима глобальной настройки переходим в режим настройки процесса OSPF, "
                               "далее – в режим настройки area,  с помощью команды network объявляем подсеть своим соседям."},
            {"t": "p", "text": "Но недостаточно прописать просто network в протоколе маршрутизации, необходимо, "
                               "чтобы маршрут в эту подсеть был в таблице маршрутизации самого маршрутизатора, "
                               "который будет анонсировать."},
            {"t": "p", "text": "Включить анонсирование подсетей для OSPF:"},
            {"t": "cmd", "text": "esr(config)# <b>router ospf &lt;Process-ID&gt;</b>"},
            {"t": "cmd", "text": "esr(config-ospf)# <b>area &lt;AREA-NUM&gt;</b>"},
            {"t": "cmd", "text": "esr(config-ospf-area)# <b>enable</b>"},
            {"t": "cmd", "text": "esr(config-ospf-area)# <b>network &lt;AAA.BBB.CCC.DDD/EE&gt;</b>"},
            {"t": "cmd", "text": "esr(config-ospf-area)# <b>enable</b>"},
            {"t": "li", "text": "&lt;Process-ID&gt; – номер процесса OSPF, значение [1-65535];"},
            {"t": "li", "text": "&lt;AREA-NUM&gt; – номер области OSPF, значения в формате XXX.XXX.XXX.XXX, "
                                "где каждая часть XXX принимает значение [0-255]."},
        ],
        "note": "Двойной пробел «area,  с» — как в оригинале.",
        "orig_errors": ["«Process-ID» — опечатка (Process)",
                        "после «area <AREA-NUM>» стоит приглашение «esr(config-ospf)# enable» вместо «esr(config-ospf-area)#»",
                        "в пояснении параметр называется «<ID>», а в команде — «<Process-ID>»"],
    },
    "s82_image122": {
        "kind": "cli",
        "lines": [
            "esr(config)# router ospf 777",
            "esr(config-ospf)# area 0.0.0.0",
            "esr(config-ospf-area)# network 203.0.113.0/24",
            "esr(config-ospf-area)# exit",
            "esr(config-ospf)# redistribute connected",
            "esr(config-ospf)# exit",
            "esr(config)#",
        ],
    },
    # ---------- s83 ----------
    "s83_image125": {
        "kind": "doc",
        "blocks": [
            {"t": "p", "text": "Изменить интервал отправки Hello-пакетов:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf hello-interval &lt;1-255&gt;</b>"},
            {"t": "p", "text": "Изменить Dead-интервал, по истечении которого сосед считается неактивным:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf dead-interval &lt;1-65535&gt;</b>"},
            {"t": "p", "text": "Изменить интервал отправки Hello-пакетов для NBMA сетей:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf poll-interval &lt;1-255&gt;</b>"},
            {"t": "p", "text": "Изменить интервал, по истечении которого Update пакет будет отправлен повторно, "
                               "если подтверждение о приеме Update пакета от соседа не было получено:"},
            {"t": "cmd", "text": "esr(config-if-gi)# <b>ip ospf retransmit-interval &lt;2-65535&gt;</b>"},
        ],
    },
    "s83_image124": {
        "kind": "cli",
        "lines": ["esr(config-if-gi)# ip ospf"] + _help(23, [
            ("dead-interval", "Configure OSPF dead interval"),
            ("hello-interval", "Configure OSPF hello interval"),
            ("poll-interval", "Configure OSPF poll interval"),
            ("retransmit-interval", "Configure OSPF retransmit interval"),
            ("wait-interval", "Configure OSPF wait interval"),
            ("<cr>", ""),
        ]),
        "note": "Укороченный вывод (только *-interval) — так на картинке.",
    },
    # ---------- s84 ----------
    "s84_image127": {
        "kind": "doc",
        "blocks": [
            {"t": "p", "text": "Включение логирования состояния OSPF сессий:"},
            {"t": "cmd", "text": "esr(config)# <b>router ospf log-adjacency-changes</b>"},
            {"t": "p", "text": "Посмотреть базы данных LSDB текущего процесса OSPF, OSPF-соседей, их "
                               "идентификаторы, приоритет, статус, IP-адрес и интерфейс:"},
            {"t": "cmd", "text": "esr# <b>show ip ospf &lt;process id&gt; database</b>"},
            {"t": "p", "text": "Просмотр суммарной информации по OSPF всем соседям:"},
            {"t": "cmd", "text": "esr# <b>show ip ospf neighbors</b>"},
            {"t": "p", "text": "Просмотр суммарной информации по OSPF-соседям определенного процесса:"},
            {"t": "cmd", "text": "esr# <b>show ip ospf &lt;process id&gt; neighbors</b>"},
            {"t": "p", "text": "Просмотр суммарной информации по виртуальным каналам:"},
            {"t": "cmd", "text": "esr# <b>show ip ospf &lt;process id&gt; virtual-links</b>"},
            {"t": "p", "text": "Просмотр суммарной информации по интерфейсам:"},
            {"t": "cmd", "text": "esr# <b>show ip ospf interface [&lt;INTERFACE&gt; &lt;PORT&gt;]</b>"},
        ],
    },
    "s84_image126": {
        "kind": "cli",
        "lines": ["esr# show ip ospf"] + _help(12, [
            ("interface", "Show OSPF interface information"),
            ("neighbors", "Show OSPF neighbors information"),
            ("1-65535", "OSPF process id"),
            ("vrf", "Virtual Routing/Forwarding instance"),
            (">", "Copy lines to file"),
            (">>", "Copy lines to end of file"),
            ("|", "Output modifiers"),
            ("<cr>", ""),
        ]),
    },
    # ---------- s85 ----------
    "s85_image129": {
        "kind": "cli",
        "lines": ["esr# clear"] + _help(18, [
            ("alarms", "Clear alarms"),
            ("arp-cache", "Clear the entire ARP cache"),
            ("bgp", "Clear BGP information"),
            ("interfaces", "Clear interfaces data"),
            ("ip", "Clear IP information"),
            ("ipv6", "Clear IPv6 information"),
            ("isis", "Clear ISIS information"),
            ("mac", "Clear MAC address table"),
            ("mpls", "Clear MPLS information"),
            ("remote-access", "Clear remote-access"),
            ("ssh", "Clear SSH information"),
            ("storage-device", "Clear storage device"),
            ("tunnels", "Clear tunnels data"),
            ("user-session", "logout all sessions"),
            ("users", "Clear users information"),
            ("vrrp-state", "Clear vrrp state"),
        ]),
    },
    "s85_image128": {
        "kind": "doc",
        "blocks": [
            {"t": "cmd", "text": "esr# <b>show ip ospf</b>"},
            {"t": "p", "text": "Просмотр RIB OSPF конкретного процесса:"},
            {"t": "cmd", "text": "esr# <b>show ip ospf &lt;process id&gt;</b>"},
        ],
    },
    "s85_image130": {
        "kind": "doc",
        "blocks": [
            {"t": "p", "text": "<b><i>Clear</i></b> – это команда из раздела «перед тем, как набрать confirm». "
                               "Если вы что-то настроили, и это может привести к тому, что IP-связность с "
                               "маршрутизатором будет нарушена, то после команды commit полезно сделать "
                               "<b>clear ip ospf.</b> В этот момент маршрутизатор стирает таблицу маршрутизации, "
                               "находит всех соседей, устанавливает с ними смежность и т.д., и если после этого "
                               "связь с маршрутизатором не прервалась, то можно смело вводить confirm."},
            {"t": "p", "text": "esr# <b>clear ip ospf</b> очищает и перезапускает процесс OSPF глобально, а используя "
                               "ключ &lt;номер процесса&gt;, можно перезапустить только определённый процесс."},
            {"t": "p", "text": "Для корректной работы рекомендуется после внесения изменений в конфигурацию OSPF "
                               "на маршрутизаторе перезапускать OSPF на обоих концах канала."},
            {"t": "p", "text": "Перезагрузить OSPF глобально:"},
            {"t": "cmd", "text": "esr# <b>clear ip ospf</b>"},
            {"t": "p", "text": "Перезагрузить OSPF-процесс:"},
            {"t": "cmd", "text": "esr# <b>clear ip ospf &lt;process id&gt;</b>"},
        ],
        "note": "Точка в «clear ip ospf.» набрана жирным моноширинным вместе с командой — как в оригинале.",
    },
    # ---------- s86: задача + решение (главное) ----------
    "s86_image132": {
        "kind": "doc",
        "blocks": [
            {"t": "h", "text": "<b>Задача:</b>"},
            {"t": "p", "text": "1) Настроить протокол OSPF на маршрутизаторе для обмена маршрутной информацией "
                               "с соседними маршрутизаторами;"},
            {"t": "p", "text": "2) Маршрутизатор должен находиться в области с идентификатором 1.1.1.1;"},
            {"t": "p", "text": "<b>Решение:</b> Необходимо предварительно настроить и включить протокол OSPF."},
            {"t": "p", "text": "1) Настроим IP-адреса на интерфейсах и отключим межсетевой экран согласно топологии:"},
            {"t": "cmd", "text": "R3# <b>config</b>"},
            {"t": "cmd", "text": "R3(config)# <b>interface gi1/0/1</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>ip address 192.168.31.1/24</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>ip firewall disable</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>exit</b>"},
            {"t": "cmd", "text": "R3(config)# <b>interface gi1/0/2</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>ip address 192.168.32.1/24</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>ip firewall disable</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>exit</b>"},
            {"t": "cmd", "text": "R3(config)# <b>interface gi1/0/5</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>ip address 198.51.100.1/24</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>ip firewall disable</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>exit</b>"},
            {"t": "cmd", "text": "R3(config)# <b>interface gi1/0/15</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>ip address 203.0.113.1/24</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>ip firewall disable</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>exit</b>"},
            {"t": "p", "text": "2) Создадим OSPF-процесс с идентификатором 100 и перейдём в режим "
                               "конфигурирования протокола OSPF:"},
            {"t": "cmd", "text": "R3(config)# <b><r>router ospf</r> <bl>100</bl></b>"},
            {"t": "p", "text": "3) Создадим и включим требуемую область:"},
            {"t": "cmd", "text": "R3(config-ospf)# <b><r>area</r> 1.1.1.1</b>"},
            {"t": "cmd", "text": "R3(config-ospf-area)# <b><r>enable</r></b>"},
            {"t": "cmd", "text": "R3(config-ospf-area)# <b>exit</b>"},
            {"t": "p", "text": "4) Включим OSPF-процесс:"},
            {"t": "cmd", "text": "R3(config-ospf)# <b><r>enable</r></b>"},
            {"t": "cmd", "text": "R3(config-ospf)# <b>exit</b>"},
            {"t": "p", "text": "5) Соседние маршрутизаторы подключены к интерфейсам gi1/0/5 и gi1/0/15. Для "
                               "установления соседства с другими маршрутизаторами привяжем их к OSPF-процессу и "
                               "области. Далее включим на интерфейсе маршрутизацию по протоколу OSPF:"},
            {"t": "cmd", "text": "R3(config)# <b>interface gigabitethernet 1/0/5</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b><r>ip ospf instance</r> <bl>100</bl></b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b><r>ip ospf area</r> 1.1.1.1</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b><r>ip ospf</r></b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>exit</b>"},
            {"t": "cmd", "text": "R3(config)# <b>interface gigabitethernet 1/0/15</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b><r>ip ospf instance</r> <bl>100</bl></b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b><r>ip ospf area</r> 1.1.1.1</b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b><r>ip ospf</r></b>"},
            {"t": "cmd", "text": "R3(config-if-gi)# <b>exit</b>"},
            {"t": "cmd", "text": "R3(config)# <b>exit</b>"},
        ],
        "note": "Склейка страниц методички (стр. 79 → следующая). Команды шага 5 в оригинале набраны другим "
                "(узким, не моноширинным) шрифтом. Красное/синее выделение — как в оригинале.",
        "orig_errors": ["«Необходимо предварительно настроить и включить протокол OSPF» — в задаче про OSPF"],
    },
}
