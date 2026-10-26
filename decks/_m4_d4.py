# -*- coding: utf-8 -*-
"""Дека 2.4, pptx 76–94: маршрутизация между VLAN — традиционный метод, Router-on-a-Stick, коммутатор L3.
Конфигурации и выводы — дословно по расшифровке скриншотов (_m4_tx.json)."""
from _sw_lib import card, p
from _m4_kit import src, tx, pslide, long_slides, fig, scn, conf, term, T
import _m4_fig4 as V
import _m4_svg as S

F_IN = ("10.10.2.20", "10.10.1.15", "AA:BB:CC:33:44:01", "AA:BB:CC:11:22:01")
F_OUT = ("10.10.2.20", "10.10.1.15", "AA:BB:CC:11:22:02", "AA:BB:CC:33:44:04")
R_IN = ("10.10.2.10", "10.10.1.15", "AA:BB:CC:33:44:01", "A2:BB:CC:11:22:A1")
R_OUT = ("10.10.2.10", "10.10.1.15", "A2:BB:CC:11:22:A2", "AA:BB:CC:33:44:02")
L_IN = ("10.10.2.20", "10.10.1.15", "AA:BB:CC:33:44:01", "0C:BB:AA:11:22:31")
L_OUT = ("10.10.2.20", "10.10.1.15", "0C:BB:AA:11:22:32", "AA:BB:CC:33:44:04")


def _conf(n, i):
    """Конфигурация из расшифровки: заголовок строкой над блоком, служебные пометки склейки убраны."""
    raw = tx(n)[i]["lines"]
    lines = []
    for k, l in enumerate(raw):
        if l.startswith("[разрыв"):
            continue
        if l == "" and ((k + 1 < len(raw) and raw[k + 1].startswith("[разрыв")) or (k > 0 and raw[k - 1].startswith("[разрыв"))):
            continue
        lines.append(l)
    while lines and not lines[-1]:
        lines.pop()
    out, blocks, title = [], [], ""
    for l in lines:
        if l and not ("#" in l) and (l.startswith("Настрой") or l.startswith("Проверка")):
            if out:
                blocks.append(conf(out, title))
            out, title = [], l.rstrip(":")
            continue
        if l == "" and not out:
            continue
        out.append(l)
    if out:
        blocks.append(conf(out, title))
    return "".join(blocks)


def build():
    TV = "Маршрутизация <em>между VLAN</em>"
    # ---------------------------------------------------------------- pptx 76
    t76 = src(76)
    pslide("Маршрутизация между VLAN", TV, [card("", p(t76[1]), "cy"), card(t76[2], p(t76[3]), "mg")],
           [fig(V.legacy(sw="both", extra="")), fig(S.fig(V.frame(20, 10, ("", "", "", ""), 0) if False else _frame76(), "0 0 900 110"))])
    pslide("Проблемы маршрутизации между VLAN", TV, [card("", p(t76[4]), "cy")], [card("", p(t76[5]), "rd")])
    # ---------------------------------------------------------------- pptx 77
    TL = "Традиционный <em>метод маршрутизации</em>"
    t77 = src(77)
    pslide("Традиционный метод", TL, [card("", p(t77[1]), "cy"), card("", p(t77[2]), "mg")], [fig(V.legacy())])
    # ---------------------------------------------------------------- pptx 78
    t78 = src(78)
    pslide("PC-1 → PC-4: кадр", TL, [card("", p(t78[1]), "cy")],
           [fig(V.legacy(sw="sw1", fr=(140, 495, F_IN, None, False))), card("", p(t78[2]), "am")])
    # ---------------------------------------------------------------- pptx 79–80
    pslide("Тег VLAN 10", TL, [card("", p(src(79)[1]), "cy")], [fig(V.legacy(sw="sw1", fr=(120, 495, F_IN, 10, False)))])
    pslide("Fa0/22: тег снят", TL, [card("", p(src(80)[1]), "cy")],
           [scn(V.legacy(sw="sw1", extra=V.frame(120, 495, F_IN, 10, False).replace("<g>", '<g data-ph="0" data-ph-only>', 1)
                         + V.frame(120, 495, F_IN, None, False).replace("<g>", '<g data-ph="1">', 1)),
                ["Кадр с тегом VLAN 10 идёт к Fa0/22", "На выходе Fa0/22 тег снят — R1 получает нетегированный кадр"])])
    # ---------------------------------------------------------------- pptx 81
    t81 = src(81)
    pslide("R1: поиск в таблице", TL, [card("", p(t81[1]), "cy"), card("", p(t81[2]), "mg")],
           [T(81, 0), fig(V.rtable([("C", "10.10.1.0/24", "Gi1/0/1"), ("C", "10.10.2.0/24", "Gi1/0/2")], (1,)))])
    pslide("R1: ARP и новый кадр", TL, [card("", p(t81[3]), "am")],
           [fig(V.legacy(sw="sw2", leg=False, fr=(600, 495, F_OUT, None, False)))])
    # ---------------------------------------------------------------- pptx 82
    t82 = src(82)
    pslide("L2SW-2: тег VLAN 20", TL, [card("", p(t82[1]), "cy"), card("", p(t82[2]), "mg")],
           [fig(V.legacy(sw="sw2", leg=False, fr=(600, 495, F_OUT, 20, False)))])
    pslide("Итог традиционного метода", TL, [card("", p(t82[3]), "am")], [fig(V.legacy(fr=(600, 495, F_OUT, None, False)))])
    # ---------------------------------------------------------------- pptx 83
    TC = "Пример конфигурации маршрутизации <em>по традиционному методу</em>"
    c83 = _conf(83, 1)
    pslide("Традиционный метод: конфигурация", TC, [_conf(83, 2)], [c83])
    # ---------------------------------------------------------------- pptx 84
    TR = "Метод <em>Router-on-a-Stick</em> (ROAS)"
    long_slides("Router-on-a-Stick", TR, [src(84)[1]], per=600, rights=[[fig(V.roas())]] * 3)
    # ---------------------------------------------------------------- pptx 85
    t85 = src(85)
    pslide("ROAS: кадр PC-1", TR, [card("", p(t85[0]), "cy"), card("", p(t85[2]), "mg")],
           [scn(V.roas(extra=V.frame(60, 470, R_IN, None, False).replace("<g>", '<g data-ph="0" data-ph-only>', 1)
                       + V.frame(60, 470, R_IN, 10, False).replace("<g>", '<g data-ph="1">', 1)),
                ["PC-1 отправляет кадр на шлюз 10.10.1.1", "На входе Fa0/1 — тег VLAN 10, через транк Fa0/24 — без изменений"])])
    # ---------------------------------------------------------------- pptx 86
    t86 = src(86)
    pslide("ROAS: подинтерфейс Gi1/0/1.10", TR, [card("", p(t86[1]), "cy")], [fig(V.roas(fr=(400, 470, R_IN, 10, False)))])
    pslide("ROAS: таблица R1", TR, [card("", p(t86[2]), "mg"), card("", p(t86[3]), "am")], [_term86()])
    # ---------------------------------------------------------------- pptx 87
    t87 = src(87)
    pslide("ROAS: ответ из Gi1/0/1.20", TR, [card("", p(t87[1]), "cy"), card("", p(t87[2]), "mg"), card("", p(t87[3]), "am")],
           [scn(V.roas(extra=V.frame(400, 470, R_OUT, 20, True).replace("<g>", '<g data-ph="0" data-ph-only>', 1)
                       + V.frame(30, 470, R_OUT, None, True).replace("<g>", '<g data-ph="1">', 1)),
                ["R1 отправляет кадр из Gi1/0/1.20 с тегом VLAN 20", "На выходе Fa0/2 тег снят — PC-2 получает кадр"])])
    # ---------------------------------------------------------------- pptx 88
    TX = "Пример настройки маршрутизации <em>методом Router-on-a-Stick</em> (ROAS)"
    pslide("ROAS: конфигурация R1", TX, [_conf(88, 1)], [_term88()])
    pslide("ROAS: конфигурация L2SW-1", TX, [_conf(88, 3)], [fig(V.roas())])
    # ---------------------------------------------------------------- pptx 89
    T3 = "Маршрутизация <em>через коммутатор L3</em>"
    t89 = src(89)
    pslide("Коммутатор L3", T3, [card("", p(t89[1]), "cy")], [scn(V.l3(arc=True), ["Топология с L3SW", "PC-1 → PC-4 через L3SW"])])
    pslide("SVI-интерфейсы", T3, [card("", p(t89[2]), "mg")], [fig(V.l3())])
    # ---------------------------------------------------------------- pptx 90
    t90 = src(90)
    pslide("L3: кадр PC-1", T3, [card("", p(t90[1]), "cy"), card("", p(t90[2]), "mg")],
           [scn(V.l3(extra=V.frame(40, 500, L_IN, None, False).replace("<g>", '<g data-ph="0" data-ph-only>', 1)
                     + V.frame(40, 500, L_IN, 10, False).replace("<g>", '<g data-ph="1">', 1)),
                ["PC-1 формирует кадр на MAC шлюза (SVI VLAN 10)", "На порту доступа L2SW-1 — тег VLAN 10"])])
    # ---------------------------------------------------------------- pptx 91–92
    t91 = src(91)
    pslide("L3: SVI VLAN 10", T3, [card("", p(t91[1]), "cy"), card("", p(t91[2]), "mg"), card("", p(t91[3]), "am")],
           [fig(V.rtable([("C", "10.10.1.0/24", "vlan 10"), ("C", "10.10.2.0/24", "vlan 20")], (1,))),
            fig(V.l3(fr=(40, 500, L_IN, 10, False)))])
    t92 = src(92)
    pslide("L3: show ip route", T3, [card("", p(t92[0]), "cy"), T(92, 0)], [card("", p(t92[2]), "mg"),
                                                                            fig(V.l3(fr=(560, 500, L_OUT, 20, False)))])
    # ---------------------------------------------------------------- pptx 93
    t93 = src(93)
    pslide("L3: доставка PC-4", T3, [card("", p(t93[1]), "cy"), card("", p(t93[2]), "mg")],
           [scn(V.l3(extra=V.frame(560, 500, L_OUT, 20, False).replace("<g>", '<g data-ph="0" data-ph-only>', 1)
                     + V.frame(560, 500, L_OUT, None, False).replace("<g>", '<g data-ph="1">', 1)),
                ["Через транки Gi1/0/2 и Fa0/24 — с тегом VLAN 20", "На выходе Fa0/2 тег снят — PC-4 получает кадр"])])
    # ---------------------------------------------------------------- pptx 94
    TY = "Пример настройки маршрутизации <em>через коммутатор уровня L3</em>"
    pslide("L3: конфигурация", TY, [_conf(94, 0), fig(V.l3(arc=False))], [_conf(94, 2)])


def _frame76():
    cells = [("Dest MAC", 130, S.F_MAC), ("Source MAC", 130, S.F_MAC), ("VLAN ID", 110, V.V10), ("Source IP", 130, S.F_IP),
             ("Dest IP", 130, S.F_IP), ("Payload", 130, S.F_PAY)]
    return (S.t(195, 22, "Заголовок L2", 14, S.GOLD2, 800) + S.t(525, 22, "Заголовок L3", 14, S.GOLD2, 800)
            + '<path d="M20 30h365M395 30h255" stroke="%s" stroke-width="2"/>' % S.GOLD + S.frame(20, 40, cells, 48, size=14))


def _term86():
    L = [l for l in tx(86)[1]["lines"]]
    return term(_join_wrapped(L))


def _term88():
    L = [l for l in tx(88)[2]["lines"] if not l.startswith("Проверка")]
    return '<div class="clih">Проверка таблицы маршрутизации на маршрутизаторе R1:</div>' + term(_join_wrapped(L))


def _join_wrapped(lines):
    """Строки, перенесённые на скриншоте («area», «11:02:03]»), — как на скриншоте, отдельной строкой."""
    return lines
