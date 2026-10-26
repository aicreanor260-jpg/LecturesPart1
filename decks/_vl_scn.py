# -*- coding: utf-8 -*-
"""Пошаговые сцены деки VLAN, построенные строго по примерам pptx (порты, MAC, VLAN — как в слайдах 25 и 37)."""

import _sw_svg as S
from _sw_lib import scene


def _strip(y, fields, ph, cap):
    cols = {"MAC": S.CY, "802.1Q": S.AM, "C-VLAN": S.AM, "S-VLAN": S.OR, "EtherType": S.MG, "Данные": S.SOFT, "FCS": S.RD}

    def col(n):
        for k, c in cols.items():
            if k in n:
                return c
        return S.CY
    share = {"Данные": 8}
    fs = [(f, share.get(f, 5), col(f)) for f in fields]
    return '<g data-ph="%d" data-ph-only>%s</g>' % (ph, S.frame_strip(150, y, fs, w=900, h=44, cap=cap))


# ---------------------------------------------------------------- pptx 25: ПК1 → SW1 → trunk → SW2 → ПК2
def trunk_example():
    o = []
    sw1, p1 = S.switch(150, 230, 330, 84, 2, "SW1", names=["Gi0/1", "Gi0/24"])
    sw2, p2 = S.switch(720, 230, 330, 84, 2, "SW2", names=["Gi0/24", "Gi0/2"])
    o += [sw1, sw2]
    o.append(S.pc(p1[0][0], 40, "ПК1", "00:11:22:33:44:01", S.LM, "VLAN 10"))
    o.append(S.pc(p2[1][0], 40, "ПК2", "00:11:22:33:44:02", S.LM, "VLAN 10"))
    o.append(S.link(p1[0][0], 118, p1[0][0], p1[0][1] + 10, S.LM, 3))
    o.append(S.link(p2[1][0], 118, p2[1][0], p2[1][1] + 10, S.LM, 3))
    o.append(S.link(p1[1][0], p1[1][1] + 10, p2[0][0], p2[0][1] + 10, S.AM, 5))
    o.append(S.badge(p1[0][0], 340, "access VLAN 10", S.LM, ph=0))
    o.append(S.badge(600, 340, "trunk: VLAN 10 с тегом 802.1Q", S.AM, ph=0))
    o.append(S.badge(p2[1][0], 340, "access VLAN 10", S.LM, ph=0))

    # ① вход через access
    o.append(S.pkt(p1[0][0], 185, p1[0][0], 230, "без тега", 1, S.LM, w=120))
    o.append(_strip(420, ["MAC ПК2", "MAC ПК1", "EtherType", "Данные", "FCS"], 1,
                     "① ПК1 → SW1 (Gi0/1): кадр без тега; SW1 относит его к VLAN 10 и изучает: ПК1 за Gi0/1"))
    # ② SW1 → SW2 через trunk, с тегом
    o.append(S.pkt(p1[1][0], 270, p2[0][0], 270, "802.1Q: VID 10", 2, S.AM, w=160))
    o.append(_strip(420, ["MAC ПК2", "MAC ПК1", "802.1Q: VID 10", "EtherType", "Данные", "FCS"], 2,
                     "② MAC ПК2 изучен за Gi0/24 — SW1 вставляет тег 802.1Q VID 10 и отправляет в trunk"))
    o.append(_strip(420, ["MAC ПК2", "MAC ПК1", "802.1Q: VID 10", "EtherType", "Данные", "FCS"], 3,
                     "SW2 принимает на Gi0/24, читает тег — VLAN 10; изучает: ПК1 доступен через trunk"))
    # ③ выход через access
    o.append(S.pkt(p2[1][0], 230, p2[1][0], 185, "без тега", 4, S.LM, w=120))
    o.append(_strip(420, ["MAC ПК2", "MAC ПК1", "EtherType", "Данные", "FCS"], 4,
                     "③ ПК2 за Gi0/2 (access VLAN 10) — тег снимается, FCS пересчитывается"))
    caps = ["ПК1 и ПК2 в VLAN 10 на access-портах, между коммутаторами trunk",
            "① ПК1 → SW1: вход через access, кадр без тега",
            "② SW1 → SW2: по trunk VLAN 10 идёт с тегом 802.1Q",
            "SW2 читает тег и определяет VLAN 10",
            "③ SW2 → ПК2: выход через access, без тега"]
    return scene(S.fig("".join(o)), caps)


# ---------------------------------------------------------------- pptx 37: C-VLAN 10 через сеть провайдера в S-VLAN 30
def qinq_example():
    o = []
    sw1, p1 = S.switch(150, 230, 330, 84, 2, "SW1 провайдера", names=["Gi0/11", "Gi0/12"])
    sw2, p2 = S.switch(720, 230, 330, 84, 2, "SW2 провайдера", names=["Gi0/12", "Gi0/11"])
    o += [sw1, sw2]
    o.append(S.pc(p1[0][0], 40, "Клиент A", "", S.CY, "C-VLAN 10"))
    o.append(S.pc(p2[1][0], 40, "Клиент B", "", S.CY, "C-VLAN 10"))
    o.append(S.link(p1[0][0], 118, p1[0][0], p1[0][1] + 10, S.CY, 3))
    o.append(S.link(p2[1][0], 118, p2[1][0], p2[1][1] + 10, S.CY, 3))
    o.append(S.link(p1[1][0], p1[1][1] + 10, p2[0][0], p2[0][1] + 10, S.OR, 5))
    o.append(S.badge(600, 340, "сеть провайдера: коммутация по S-VLAN 30", S.OR, ph=0))

    o.append(S.pkt(p1[0][0], 185, p1[0][0], 230, "C-VLAN 10", 1, S.AM, w=130))
    o.append(_strip(420, ["MAC получателя", "MAC источника", "C-VLAN 10", "EtherType", "Данные", "FCS"], 1,
                     "1. Кадр приходит на Gi0/11 SW1 с тегом C-VLAN 10 — правило: добавить S-VLAN 30"))
    o.append(S.pkt(p1[1][0], 270, p2[0][0], 270, "S-VLAN 30 + C-VLAN 10", 2, S.OR, w=230))
    o.append(_strip(420, ["MAC получателя", "MAC источника", "S-VLAN 30", "C-VLAN 10", "EtherType", "Данные", "FCS"], 2,
                     "2. SW1 добавляет внешний тег и отправляет через Gi0/12: внешняя метка 30, внутренняя 10"))
    o.append(_strip(420, ["MAC получателя", "MAC источника", "S-VLAN 30", "C-VLAN 10", "EtherType", "Данные", "FCS"], 3,
                     "3. SW2 принимает на Gi0/12, обрабатывает в S-VLAN 30 и выбирает выход Gi0/11"))
    o.append(S.pkt(p2[1][0], 230, p2[1][0], 185, "C-VLAN 10", 4, S.AM, w=130))
    o.append(_strip(420, ["MAC получателя", "MAC источника", "C-VLAN 10", "EtherType", "Данные", "FCS"], 4,
                     "4. SW2 снимает S-VLAN 30 — клиентский тег VLAN 10 сохраняется, FCS пересчитывается"))
    caps = ["Клиенты A и B с C-VLAN 10, между ними сеть провайдера",
            "1. Кадр с C-VLAN 10 приходит на Gi0/11 SW1",
            "2. SW1 добавляет внешний тег S-VLAN 30",
            "3. SW2 обрабатывает кадр в S-VLAN 30",
            "4. SW2 снимает внешний тег при отправке к клиенту"]
    return scene(S.fig("".join(o)), caps)
