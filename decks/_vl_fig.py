# -*- coding: utf-8 -*-
"""Схемы из pptx «2.2 VLAN», перерисованные в стиле деки: иконки устройств — из инфографик пользователя."""
import os

import _sw_svg as S
import _dk_replib


def T(x, y, s, size=14, col="#fff", w=700, anchor="middle", mono=False):
    """Текст SVG: цвет через style, иначе общий CSS svg.fig text перекрашивает всё в белый."""
    return S.txt(x, y, s, size, col, w, anchor, mono, ' style="fill:%s"' % col)

CR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_dk_rep", "crops")
RED, BLUE, GRN, YEL = "#e8432b", "#2f6fe0", "#3fae3a", "#f2b51d"


def im(name, x, y, w, h):
    return ('<image href="%s" x="%g" y="%g" width="%g" height="%g" preserveAspectRatio="xMidYMid meet"/>'
            % (_dk_replib._webp(os.path.join(CR, name + ".png")), x, y, w, h))


def sw(cx, cy, label="", w=110):
    h = w * 80 / 131.0
    o = im("dev_vlan_sw", cx - w / 2, cy - h / 2, w, h)
    if label:
        o += T(cx, cy + h / 2 + 18, label, 14, "#fff", 800)
    return o


def pc(cx, top, label="", w=80, col="#fff"):
    o = im("dev_vlan_pc", cx - w / 2, top, w, w * 158 / 200.0)
    if label:
        o += T(cx, top + w * .79 + 17, label, 13, col, 800)
    return o


def env(cx, cy, w=40):
    return im("dev_vlan_env", cx - w / 2, cy - w * 34 / 88.0, w, w * 34 / 44.0)


def wire(x1, y1, x2, y2, col="#dfe8ff", w=4):
    return '<path class="lnk" d="M%g %gL%g %g" stroke="%s" stroke-width="%g" stroke-linecap="square"/>' % (x1, y1, x2, y2, col, w)


def bubble(x, y, text, col=YEL, w=None):
    w = w or len(text) * 8.4 + 26
    return ('<g><rect x="%g" y="%g" width="%g" height="30" fill="%s" stroke="#0a1440" stroke-width="3"/>%s</g>'
            % (x - w / 2, y - 15, w, col, T(x, y + 5, text, 13, "#10183a", 800)))


# ---------------------------------------------------------------- дерево из рисунков 2.4.1.1–2.4.1.4
def arp_tree(mode):
    """mode: req — 10.10.1.5 отправляет ARP; flood — запрос на все порты;
    seg — сеть разделена устройством L3; segflood — рассылка только в своём сегменте."""
    o = []
    seg = mode in ("seg", "segflood")
    cols = [RED, BLUE, GRN]
    xs = [200, 600, 1000]
    # в pptx подписаны только отправитель и искомый узел
    ips = [["", "", ""], ["", "", ""], ["", "10.10.1.6", "10.10.1.5"]]
    if seg:
        for i, x in enumerate(xs):
            o.append('<rect x="%g" y="160" width="370" height="370" fill="%s" fill-opacity=".16" stroke="%s" '
                     'stroke-width="3" stroke-dasharray="10 6"/>' % (x - 185, cols[i], cols[i]))
            o.append(T(x - 170, 182, "Сегмент %d · отдельный домен" % (i + 1), 13, "#fff", 800, "start"))
        o.append('<circle cx="600" cy="70" r="42" fill="#3b4a7a" stroke="#fff" stroke-width="4"/>')
        o.append(T(600, 66, "L3", 20, "#ffe14a", 900))
        o.append(T(600, 86, "маршрутизатор", 10.5, "#fff", 700))
    else:
        o.append(sw(600, 62, "SW L2", 120))
    for i, x in enumerate(xs):
        o.append(wire(600, 100, x, 225, cols[i] if seg else "#dfe8ff"))
        o.append(sw(x, 245, "SW L2"))
        for j, dx in enumerate((-115, 0, 115)):
            ip = ips[i][j]
            o.append(wire(x, 265, x + dx, 380, cols[i] if seg else "#dfe8ff"))
            hl = ip == "10.10.1.5" and "#ffe14a" or (ip == "10.10.1.6" and "#7dff9a" or "#fff")
            o.append(pc(x + dx, 380, ip, col=hl))
    if mode in ("req", "segflood", "seg"):
        o.append(bubble(1000, 352, "ARP: у кого IP 10.10.1.6?", YEL))
        o.append(env(1080, 360))
    if mode == "flood":
        for i, x in enumerate(xs):
            for dx in (-115, 0, 115):
                if not (i == 2 and dx == 115):
                    o.append(env(x + dx * .55, 330))
            o.append(env((600 + x) / 2.0, 165))
        o.append(bubble(600, 140, "FF:FF:FF:FF:FF:FF — запрос получают ВСЕ узлы", RED, 470))
    if mode == "segflood":
        for dx in (-115, 0):
            o.append(env(1000 + dx * .55, 330))
        o.append(env(800, 160))
        o.append(bubble(600, 140, "Запрос доходит до устройства L3 и дальше не передаётся", GRN, 520))
    return S.fig("".join(o), "0 0 1200 560")


# ---------------------------------------------------------------- рисунок 2.5.4.2.3
def phone_trunk():
    o = [wire(230, 230, 1010, 230, "#dfe8ff", 5)]
    o.append(sw(160, 220, "", 170))
    o.append('<circle cx="250" cy="230" r="13" fill="#3fae3a" stroke="#fff" stroke-width="3"/>')
    o.append(T(250, 278, "Gi0/1", 16, "#fff", 800))
    o.append(T(250, 300, "Trunk", 16, "#fff", 800))
    o.append(T(250, 324, "A100", 18, "#ff7a6a", 900))
    o.append(T(250, 348, "N20", 18, "#ffd23a", 900))
    o.append(im("dev_vlan_phone", 560, 150, 150, 108))
    o.append(T(635, 290, "IP-телефон", 15, "#fff", 800))
    o.append(pc(1060, 160, "PC-A", 120))
    # голос — с тегом 100, данные ПК — без тега (VLAN 20)
    o.append(env(360, 200, 56))
    o.append(bubble(360, 160, "VID 100", "#ff7a6a", 90))
    o.append(env(470, 200, 56))
    o.append(bubble(470, 160, "без тега", "#ffd23a", 100))
    o.append(env(860, 200, 56))
    o.append(bubble(860, 160, "без тега", "#ffd23a", 100))
    o.append(T(600, 420, "Голос телефона — разрешённая VLAN 100 (A100), с тегом.", 15, "#fff", 700))
    o.append(T(600, 446, "Трафик ПК идёт через телефон без тега и попадает в нативную VLAN 20 (N20).", 15, "#fff", 700))
    return S.fig("".join(o), "0 0 1200 480")


# ---------------------------------------------------------------- Selective Q-in-Q, четыре пакета
def qinq_packets():
    o = []
    specs = [("packet №1", "Вход", ["Vlan X"], ["Vlan X", "Vlan X"], True),
             ("packet №2", "Выход", ["Vlan X"], ["Vlan X", "Vlan X"], False),
             ("packet №3", "Вход", ["Vlan 31"], ["Vlan 31"], True),
             ("packet №4", "Выход", ["Vlan 31"], ["Vlan 31"], False)]
    for k, (nm, io, top, bot, down) in enumerate(specs):
        x = 150 + k * 300
        o.append(T(x - 40, 46, nm, 14, "#fff", 800))
        o.append('<rect x="%g" y="28" width="90" height="30" fill="#fff" stroke="#0a1440" stroke-width="3"/>' % (x + 10))
        o.append(T(x + 55, 49, top[0], 14, "#10183a", 800))
        if len(bot) == 2:
            o.append(T(x + 128, 49, "CVLAN", 12, "#ffe14a", 800))
        o.append('<rect x="%g" y="140" width="76" height="26" fill="%s" stroke="#0a1440" stroke-width="3"/>'
                 % (x - 110, "#3fae3a"))
        o.append(T(x - 72, 158, io, 13, "#fff", 800))
        o.append(T(x - 10, 158, "Gi0/11", 13, "#fff", 800))
        o.append(sw(x + 55, 190, "", 150))
        o.append(T(x - 10, 250, "Gi0/12", 13, "#fff", 800))
        y1, y2 = (62, 152) if down else (152, 62)
        o.append(S.arrow(x + 55, y1, x + 55, y2, "#fff", 4, "ah", flow=False))
        y3, y4 = (232, 318) if down else (318, 232)
        o.append(S.arrow(x + 55, y3, x + 55, y4, "#fff", 4, "ah", flow=False))
        for j, b in enumerate(bot):
            o.append('<rect x="%g" y="%g" width="90" height="30" fill="#fff" stroke="#0a1440" stroke-width="3"/>'
                     % (x + 10, 322 + j * 32))
            o.append(T(x + 55, 343 + j * 32, b, 14, "#10183a", 800))
            if len(bot) == 2:
                o.append(T(x + 128, 343 + j * 32, ("CVLAN", "SVLAN")[j], 12, ("#ffe14a", "#ff9a3d")[j], 800))
    o.append(T(40, 420, "Условные обозначения:", 15, "#fff", 800, "start"))
    o.append(T(40, 446, "• X — любой VLAN, кроме 31", 14, "#fff", 700, "start"))
    o.append(T(40, 470, "• При добавлении метки SVLAN является внешней, а CVLAN — внутренней", 14, "#fff", 700, "start"))
    return S.fig("".join(o), "0 0 1200 490")


# ---------------------------------------------------------------- топология примера MAC-based VLAN
def mac_topo():
    o = [wire(600, 120, 330, 330), wire(600, 120, 870, 330)]
    o.append(sw(600, 100, "", 150))
    o.append(T(420, 210, "gi 1/0/1", 17, "#fff", 800))
    o.append(T(790, 210, "gi 1/0/2", 17, "#fff", 800))
    o.append(pc(330, 320, "ПК1", 110))
    o.append(T(330, 470, "VLAN 10", 15, "#ffd23a", 900))
    o.append(pc(870, 320, "ПК2", 110))
    o.append(T(870, 470, "VLAN 10", 15, "#ffd23a", 900))
    return S.fig("".join(o), "0 0 1200 490")


# ---------------------------------------------------------------- рисунок 2.4.6.1 — классификация VLAN
def types_tree():
    br = [("По методу создания", ["По умолчанию", "Статические", "Динамические"]),
          ("По методу тегирования", ["На основе портов", "На основе MAC-адресов", "На основе протоколов", "На основе политик"]),
          ("По виду трафика", ["VLAN управления", "VLAN данных", "Voice VLAN", "Multicast VLAN"])]
    o = ['<div class="ttree"><div class="tt-root">Типы VLAN</div><div class="tt-br">']
    for t, leaves in br:
        o.append('<div class="tt-col"><div class="tt-h">%s</div>%s</div>'
                 % (t, "".join('<div class="tt-l">%s</div>' % l for l in leaves)))
    o.append("</div></div>")
    return "".join(o)


CSS = r"""
.ttree{display:flex;flex-direction:column;align-items:center;gap:16px}
.tt-root{padding:10px 26px;background:#ffd23a;color:#10183a;font:900 clamp(14px,1.1vw,20px)/1.2 var(--f);
 border:4px solid #0a1440;box-shadow:4px 4px 0 rgba(0,0,0,.45)}
.tt-br{display:flex;gap:16px;width:100%}
.tt-col{flex:1;display:flex;flex-direction:column;gap:8px;align-items:stretch}
.tt-h{padding:8px;background:#c8501e;color:#fff;text-align:center;font:800 clamp(12px,.9vw,17px)/1.25 var(--f);
 border:4px solid #3a1606;box-shadow:4px 4px 0 rgba(0,0,0,.45)}
.tt-l{padding:7px 10px;background:rgba(255,255,255,.94);color:#10183a;text-align:center;
 font:700 clamp(11px,.82vw,15.5px)/1.25 var(--f);border:3px solid #0a1440;margin-left:22px;position:relative}
.tt-l::before{content:"";position:absolute;left:-22px;top:50%;width:19px;border-top:3px solid #fff}
"""
