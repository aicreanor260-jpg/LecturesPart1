# -*- coding: utf-8 -*-
"""Дословная расшифровка картинок из pptx «Базовая настройка» (BASE) и «VLAN» (VLAN).
Подписи «Рисунок …» не включены. Выравнивание колонок в CLI восстановлено по
моноширинной сетке картинки (позиции символов, ±1 знак)."""


def _row(*cells):
    """cells: пары (колонка, текст) → строка с пробелами-выравниванием."""
    s = ""
    for col, txt in cells:
        s = s.ljust(col) + txt
    return s


_VLAN_HDR = [
    "Vlan mode: Basic",
    "Created by: D-Default, S-Static, G-GVRP, R-Radius Assigned VLAN, V-Voice VLAN",
    "",
    _row((0, "Vlan"), (10, "Name"), (24, "Tagged Ports"), (41, "UnTagged Ports"), (59, "Created by")),
    "---- " + "-" * 16 + " " + "-" * 17 + " " + "-" * 17 + " " + "-" * 15,
]

BASE = {
    "s05_2": {
        "kind": "form",
        "title": "Tera Term: Serial port setup and connection",
        "fields": [
            ["Порт:", "COM4"],
            ["Скорость:", "115200"],
            ["Данные:", "8 bit"],
            ["Четность:", "none"],
            ["Стоп-бит:", "1 bit"],
            ["Управление:", "none"],
            ["Задержка передачи: мс/символ", "0"],
            ["Задержка передачи: мс/строка", "0"],
        ],
        "buttons": ["New setting", "Выйти", "Помощь"],
        "info": [
            "Device Friendly Name: High-Speed USB Serial Port (COM4)",
            "Device Instance ID: QUADPORT\\QUAD_SERIAL_INTERFACE\\6&162",  # обрезано окном
            "Device Manufacturer: ASIX Electronics Corporation.",
            "Provider Name: ASIX",
            "Driver Date: 10-13-2020",
            "Driver Version: 3.20.7.200",
        ],
        "photo": "Фото на деревянном столе: слева серый плоский консольный кабель "
                 "RJ-45 — DB-9 (синий разъём DB-9 «мама» с винтами), справа "
                 "прозрачный кабель-адаптер USB-A — DB-9 (синий полупрозрачный разъём DB-9 «папа»).",
    },
    "s08_1": {
        "kind": "form",
        "title": "Auth",
        "fields": [
            ["Username", "admin"],
            ["Password", "••••••"],
            ["Language", "English"],
        ],
        "buttons": ["Sign in"],
        "ui": "Слева тёмная вертикальная панель с логотипом Eltex (серые и голубые узлы-кружки).",
    },
    "s09_1": {
        "kind": "ui",
        "header": {
            "logo": "ELTEX",
            "title": "MES2324",
            "subtitle": "MES2324 AC 28-port 1G/10G Managed Switch",
            "right": "admin1 | Ru En | Save | Sign Out",
        },
        "tree_title": "Configuration Tree",
        "tree": [
            ("-", "System", 0),
            ("", "System Information", 1),  # выделен
            ("", "Reset", 1),
            ("+", "Time", 1),
            ("-", "IP Addressing", 1),
            ("", "IP Interface", 2),
            ("", "ARP", 2),
            ("", "Ping", 2),
            ("+", "Domain Name System", 1),
            ("+", "Logs", 1),
            ("+", "File Management", 1),
            ("+", "SNMP", 0),
            ("+", "Physical", 0),
            ("+", "Management Security", 0),
            ("+", "Network Security", 0),
            ("+", "Layer 2", 0),
            ("+", "QoS", 0),
            ("+", "Statistics RMON", 0),
        ],
        "selected": "System Information",
        "panel_title": "System / System Information",
        "fields": [
            ["Model Name", "MES2324 AC 28-port 1G/10G Managed Switch"],
            ["System Name", "MES2324"],  # поле ввода
            ["System Location", ""],      # поле ввода
            ["System Contact", ""],       # поле ввода
            ["System Object ID", "1.3.6.1.4.1.35265.1.76"],
            ["System Up Time", "0 days, 5 hours, 23 minutes, 51 seconds"],
            ["Base MAC Address", "a8:f9:4b:30:fc:c0"],
            ["Hardware Version", "02.02.02"],
            ["Software Version", "4.0.20"],
            ["Boot Version", "1.0.0.0"],
        ],
        "buttons": ["Submit"],
    },
    "s12_1": {
        "kind": "cli",
        "lines": [
            # над первой строкой виден обрезанный край ещё одной строки — нечитаем
            "Console baud-rate auto detection is enabled, press Enter twice to complete the detection process",
            "",
            "Unauthorized intrusion is prohibited. Legal action may follow!",
            "Neavtorizovanniy vhod zapreschon! Unbefugtes Eindringen verboten!",
            "",
            "",
            "User Name:",
        ],
    },
    "s13_1": {
        "kind": "cli",
        "lines": [
            "User Name:admin1",
            "Password:******",
            "",
            "Welcome!",
            "Dobro pojalovat!",
            "Wilkommen!",
            "",
            "console#",
        ],
    },
    "s13_2": {
        "kind": "cli",
        "lines": [
            "banner login ^",
            "Unauthorized intrusion is prohibited. Legal action may follow!",
            "Neavtorizovanniy vhod zapreschon! Unbefugtes Eindringen verboten!",
            "^",
            "banner exec ^",
            "Welcome!",
            "Dobro pojalovat!",
            "Wilkommen!",
            "^",
            "",
            "!",
        ],
    },
    "s16_1": {
        "kind": "cli",
        "lines": [
            "console#sho run | begin username",
            "username user password encrypted 12dea96fec20593566ab75692c9949596833adc9",
            "username admin1 password encrypted 6c7ca345f63f835cb353ff15bd6c5e052ec08e7a privilege 15",
            "!",
            "end",
            "console#",
        ],
    },
    "s17_1": {
        "kind": "cli",
        "lines": [
            "console(config)#no username admin1",
            "console(config)#",
            "console(config)#",
            "console(config)#do show running-config | begin username",
            "username user password encrypted 12dea96fec20593566ab75692c9949596833adc9",
            "!",
            "end",
            "console(config)#",
        ],
    },
    "s18_1": {
        "kind": "cli",
        "lines": [
            "User Name:user",
            "Password:****",
            "",
            "",
            "console>",
            "console>",
            "console>",
            "console>",
        ],
    },
    "s19_1": {
        "kind": "cli",
        "lines": [
            "User Name:user",
            "Password:****",
            "",
            "",
            "console>enable",
            "Password:********",
            "console#14-Apr-2023 19:12:33 %AAA-I-CONNECT: User CLI session for user user over console , source",
            "0.0.0.0 destination  0.0.0.0, enable password ACCEPTED.",
            "",
            "console#show privilege",
            "Current privilege level is 15",
            "console#",
        ],
    },
    "s19_2": {
        "kind": "cli",
        "lines": [
            "User Name:user",
            "Password:****",
            "",
            "",
            "console>enable 4",
            "Password:******",
            "console#14-Apr-2023 21:40:22 %AAA-I-CONNECT: User CLI session for user user over console , source",
            "0.0.0.0 destination  0.0.0.0, enable password ACCEPTED.",
            "",
            "console#show privilege",
            "Current privilege level is 4",
            "console#",
        ],
    },
}

_MAC_T = ["VID", "MAC-address", "Interface", "Type"]

VLAN = {
    # ---------------- консоль ----------------
    "s14_1": {
        "kind": "cli",
        "lines": [
            _row((0, "VID"), (8, "MAC Address"), (29, "Interface"), (62, "Type")),
            _row((0, "-----"), (8, "-" * 18), (29, "-" * 30), (62, "-" * 7)),
            _row((0, "10"), (8, "34:60:f9:5f:df:5f"), (29, "gigabitethernet 1/0/2"), (62, "Dynamic")),
            _row((0, "10"), (8, "a0:a3:f0:d1:26:5a"), (29, "gigabitethernet 1/0/6"), (62, "Dynamic")),
            "2 valid mac entries",
        ],
    },
    "s15_1": {
        "kind": "cli",
        "lines": _VLAN_HDR + [
            _row((1, "1"), (12, "-"), (39, "gi1/0/1-24"), (63, "D")),
            _row((1, "10"), (8, "IT"), (63, "S")),
            _row((1, "20"), (8, "Management"), (63, "S")),
        ],
    },
    "s15_2": {
        "kind": "cli",
        "lines": _VLAN_HDR + [
            _row((1, "1"), (12, "-"), (39, "gi1/0/1-24"), (63, "D")),
            _row((1, "20"), (8, "Management"), (63, "S")),
        ],
    },
    "s21_1": {
        "kind": "cli",
        "bold": ["show vlan"],
        "lines": ["switch#show vlan"] + _VLAN_HDR + [
            _row((1, "1"), (12, "-"), (39, "gi1/0/1-24"), (63, "D")),
            "-" * 16 + "часть текста пропущена" + "-" * 34,
        ],
    },
    "s21_2": {
        "kind": "cli",
        "bold": ["show interfaces switchport gigabitethernet 1/0/1", "Access"],
        "lines": [
            "switch#show interfaces switchport gigabitethernet 1/0/1",
            "Added by: D-Default, S-Static, G-GVRP, R-Radius Assigned VLAN, T-Guest VLAN, V-Voice VLAN",
            "Port : gi1/0/1",
            "Port Mode: Access",
            "Gvrp Status: disabled",
            "Ingress Filtering: true",
            "Acceptable Frame Type: admitAll",
            "Ingress UnTagged VLAN ( NATIVE ): 1",
            "-" * 20 + "часть текста пропущена" + "-" * 27,
        ],
    },
    "s22_1": {
        "kind": "cli",
        "bold": ["interface gigabitethernet 1/0/1", "switchport mode access", "switchport access vlan 10"],
        "lines": [
            "switch(config)#interface gigabitethernet 1/0/1",
            "switch(config-if)#switchport mode access",
            "switch(config-if)#switchport access vlan 10",
        ],
    },
    "s22_2": {
        "kind": "cli",
        "bold": ["interface range gigabitethernet 1/0/1-4", "switchport mode access", "switchport access vlan 10"],
        "lines": [
            "switch(config)#interface range gigabitethernet 1/0/1-4",
            "switch(config-if-range)#switchport mode access",
            "switch(config-if-range)#switchport access vlan 10",
        ],
    },
    "s22_3": {
        "kind": "cli",
        "lines": _VLAN_HDR + [
            _row((1, "1"), (12, "-"), (39, "gi1/0/5-12"), (63, "D")),
            _row((1, "10"), (11, "IT"), (42, "gi1/0/1-4"), (63, "S")),
            _row((1, "20"), (7, "Management"), (63, "S")),
        ],
    },
    "s23_1": {
        "kind": "cli",
        "lines": _VLAN_HDR + [
            _row((1, "1"), (12, "-"), (43, "gi1/0/1,"), (63, "D")),
            _row((39, "gi1/0/5-12")),
            _row((1, "10"), (11, "IT"), (42, "gi1/0/2-4"), (63, "S")),
            _row((1, "20"), (7, "Management"), (63, "S")),
        ],
    },
    # ---------------- таблицы ----------------
    "s20_2": {
        "kind": "table",
        "tables": [{
            "title": "Таблица MAC-адресов SW1 после того, как оба компьютера отправили кадры:",
            "cols": _MAC_T,
            "rows": [["10", "00:11:22:33:44:01", "Gi0/1", "Dynamic"],
                     ["10", "00:11:22:33:44:02", "Gi0/2", "Dynamic"]],
            "note": None,
        }],
        "after": "",
    },
    "s25_2": {
        "kind": "table",
        "tables": [
            {"title": "Таблица MAC-адресов SW1", "cols": _MAC_T,
             "rows": [["10", "00:11:22:33:44:01", "Gi0/1", "Dynamic"],
                      ["10", "00:11:22:33:44:02", "Gi0/24", "Dynamic"]],
             "note": "После обмена кадрами в обе стороны:"},
            {"title": "Таблица MAC-адресов SW2", "cols": _MAC_T,
             "rows": [["10", "00:11:22:33:44:01", "Gi0/24", "Dynamic"],
                      ["10", "00:11:22:33:44:02", "Gi0/2", "Dynamic"]],
             "note": None},
        ],
        "after": "VID — номер VLAN. Dynamic — запись автоматически изучена по MAC-адресу источника принятого кадра.",
    },
    "s27_2": {
        "kind": "table",
        "tables": [
            {"title": "Таблица MAC-адресов SW1 после обмена в обе стороны", "cols": _MAC_T,
             "rows": [["10", "00:11:22:33:44:01", "Gi0/1", "Dynamic"],
                      ["10", "00:11:22:33:44:02", "Gi0/24", "Dynamic"]],
             "note": None},
            {"title": "Таблица MAC-адресов SW2", "cols": _MAC_T,
             "rows": [["10", "00:11:22:33:44:01", "Gi0/24", "Dynamic"],
                      ["10", "00:11:22:33:44:02", "Gi0/2", "Dynamic"]],
             "note": "VID — номер VLAN; Dynamic — запись автоматически изучена по MAC источника принятого кадра."},
            {"title": "Для сравнения, на том же trunk:",
             "cols": ["VLAN кадра", "Настройка trunk", "Передача по кабелю"],
             "rows": [["10", "Native VLAN 10", "Без тега"],
                      ["20", "VLAN 20 разрешена, не native", "С тегом VID 20"]],
             "note": None},
        ],
        "after": "Native VLAN должна совпадать на обоих концах trunk: иначе нетегированный кадр "
                 "VLAN 10 может попасть в другую VLAN на соседнем коммутаторе.",
    },
    "s33_1": {
        "kind": "table",
        "tables": [{"title": None, "cols": _MAC_T,
                    "rows": [["10", "00:11:22:33:44:01", "Gi0/1", "Dynamic"]], "note": None}],
        "after": "",
    },
    "s34_1": {
        "kind": "table",
        "tables": [{"title": None,
                    "cols": ["Участок", "Действие", "Вид кадра на кабеле"],
                    "rows": [
                        ["ПК3 → Gi0/2 SW1", "SW1 относит кадр к VLAN 20 по PVID 20", "Без тега"],
                        ["Gi0/24 SW1 → Gi0/24 SW2", "SW1 добавляет тег VID 20; SW2 определяет VLAN по тегу", "С тегом VID 20"],
                        ["Gi0/2 SW2 → ПК4", "SW2 снимает тег, поскольку VLAN 20 настроена как untagged", "Без тега"],
                    ], "note": None}],
        "after": "",
    },
    "s34_2": {
        "kind": "table",
        "tables": [
            {"title": "Таблица MAC-адресов SW1 после обмена всех компьютеров кадрами в своих VLAN",
             "cols": _MAC_T,
             "rows": [["10", "00:11:22:33:44:01", "Gi0/1", "Dynamic"],
                      ["10", "00:11:22:33:44:02", "Gi0/24", "Dynamic"],
                      ["20", "00:11:22:33:44:03", "Gi0/2", "Dynamic"],
                      ["20", "00:11:22:33:44:04", "Gi0/24", "Dynamic"]],
             "note": None},
            {"title": "Таблица MAC-адресов SW2", "cols": _MAC_T,
             "rows": [["10", "00:11:22:33:44:01", "Gi0/24", "Dynamic"],
                      ["10", "00:11:22:33:44:02", "Gi0/1", "Dynamic"],
                      ["20", "00:11:22:33:44:03", "Gi0/24", "Dynamic"],
                      ["20", "00:11:22:33:44:04", "Gi0/2", "Dynamic"]],
             "note": None},
        ],
        "after": "Dynamic означает, что запись изучена автоматически по MAC источника входящего кадра. "
                 "Настройки tagged и untagged определяют наличие тега на выходе из порта.",
    },
    "s37_2": {
        "kind": "table",
        "tables": [
            {"title": "Таблица MAC-адресов SW1", "cols": _MAC_T,
             "rows": [["30", "00:11:22:33:44:01", "Gi0/11", "Dynamic"],
                      ["30", "00:11:22:33:44:02", "Gi0/12", "Dynamic"]],
             "note": "После обмена кадрами в обе стороны, при обучении и коммутации по внешней S-VLAN:"},
            {"title": "Таблица MAC-адресов SW2", "cols": _MAC_T,
             "rows": [["30", "00:11:22:33:44:01", "Gi0/12", "Dynamic"],
                      ["30", "00:11:22:33:44:02", "Gi0/11", "Dynamic"]],
             "note": None},
        ],
        "after": "",
    },
    # ---------------- блок-схемы ----------------
    "s20_1": {
        "kind": "flow",
        "columns": [[
            {"t": "device", "text": "ПК1\nMAC: 00:11:22:33:44:01"},
            {"t": "edge", "text": "Gi0/1: кадр без тега"},
            {"t": "device", "text": "Коммутатор SW1\nGi0/1 — access VLAN 10\nGi0/2 — access VLAN 10"},
            {"t": "edge", "text": "Gi0/2: кадр без тега"},
            {"t": "device", "text": "ПК2\nMAC: 00:11:22:33:44:02"},
        ]],
    },
    "s25_1": {
        "kind": "flow",
        "columns": [[
            {"t": "device", "text": "ПК1 — VLAN 10\nMAC: 00:11:22:33:44:01"},
            {"t": "edge", "text": "① Кадр без тега"},
            {"t": "device", "text": "SW1\nGi0/1 — access VLAN 10\nGi0/24 — trunk"},
            {"t": "edge", "text": "② Добавлен тег 802.1Q: VID 10"},
            {"t": "device", "text": "SW2\nGi0/24 — trunk\nGi0/2 — access VLAN 10"},
            {"t": "edge", "text": "③ Тег удалён: кадр без тега"},
            {"t": "device", "text": "ПК2 — VLAN 10\nMAC: 00:11:22:33:44:02"},
        ]],
    },
    "s27_1": {
        "kind": "flow",
        "columns": [[
            {"t": "device", "text": "ПК1 — VLAN 10\nMAC: 00:11:22:33:44:01"},
            {"t": "edge", "text": "① Без тега"},
            {"t": "device", "text": "SW1\nGi0/1: access VLAN 10\nGi0/24: trunk, native VLAN 10"},
            {"t": "edge", "text": "② Без тега: VLAN 10 является native"},
            {"t": "device", "text": "SW2\nGi0/24: trunk, native VLAN 10\nGi0/2: access VLAN 10"},
            {"t": "edge", "text": "③ Без тега"},
            {"t": "device", "text": "ПК2 — VLAN 10\nMAC: 00:11:22:33:44:02"},
        ]],
    },
    "s37_1": {
        "kind": "flow",
        "columns": [[
            {"t": "device", "text": "Коммутатор клиента A\nMAC источника:\n00:11:22:33:44:01"},
            {"t": "edge", "text": "Один тег: C-VLAN 10"},
            {"t": "device", "text": "SW1 провайдера\nGi0/11: к клиенту — добавить S-VLAN 30\nGi0/12: в сеть провайдера"},
            {"t": "edge", "text": "Два тега: S-VLAN 30 + C-VLAN 10"},
            {"t": "device", "text": "SW2 провайдера\nGi0/12: из сети провайдера\nGi0/11: к клиенту — снять S-VLAN 30"},
            {"t": "edge", "text": "Один тег: C-VLAN 10"},
            {"t": "device", "text": "Коммутатор клиента B\nMAC получателя:\n00:11:22:33:44:02"},
        ]],
    },
}

# s33_2 и s34_3 — одна и та же картинка: две колонки, сходящиеся в общие SW1/SW2.
# Блоки с портами (Gi0/x: general …) — подписи на линиях (edge), без стрелок, просто линии.
_TWO_SW = {
    "kind": "flow",
    "shared": "SW1 Eltex, ребро Gi0/24 ↔ Gi0/24 и SW2 Eltex — общие для обеих колонок (по центру-слева)",
    "columns": [
        [
            {"t": "device", "text": "ПК1 — VLAN 10\nMAC: 00:11:22:33:44:01"},
            {"t": "edge", "text": "Gi0/1: general\nVLAN 10 untagged\nPVID 10"},
            {"t": "device", "text": "SW1 Eltex\nGi0/24: general\nVLAN 10, 20 tagged"},
            {"t": "edge", "text": "Gi0/24 ↔ Gi0/24\nVLAN 10 и 20 — с тегом"},
            {"t": "device", "text": "SW2 Eltex\nGi0/24: general\nVLAN 10, 20 tagged"},
            {"t": "edge", "text": "Gi0/1: general\nVLAN 10 untagged\nPVID 10"},
            {"t": "device", "text": "ПК2 — VLAN 10\nMAC: 00:11:22:33:44:02"},
        ],
        [
            {"t": "device", "text": "ПК3 — VLAN 20\nMAC: 00:11:22:33:44:03"},
            {"t": "edge", "text": "Gi0/2: general\nVLAN 20 untagged\nPVID 20"},
            {"t": "device", "text": "→ SW1 Eltex (общий)"},
            {"t": "device", "text": "SW2 Eltex (общий) →"},
            {"t": "edge", "text": "Gi0/2: general\nVLAN 20 untagged\nPVID 20"},
            {"t": "device", "text": "ПК4 — VLAN 20\nMAC: 00:11:22:33:44:04"},
        ],
    ],
}
VLAN["s33_2"] = _TWO_SW
VLAN["s34_3"] = dict(_TWO_SW)
