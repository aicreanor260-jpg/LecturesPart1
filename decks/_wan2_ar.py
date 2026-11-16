# -*- coding: utf-8 -*-
"""WAN-2 (WAN на основе Ethernet, доступ, PPP, GRE, DMVPN): инфографики автора — вёрсткой и SVG с анимацией («Скуби-Ду»)."""
from _scoob import (page, panel, items, nums, note, grid, stack, scn, scp, lbl, chip, rt, swc, cloud, pc, bld, tower, srv, ln, L, flow, env, show,
                    tab, OUT, BLU, CY, OR, LI, PU, RD)


def seg(parts, size=17):
    """Структура кадра / пакета: [(текст, цвет, доля)]"""
    return ('<div style="display:flex;border:3px solid #2a1b4a;border-radius:10px;overflow:hidden;font-weight:900;text-align:center;color:#2a1b4a;'
            'font-size:calc(%dpx*var(--fz,1))">%s</div>' % (size, "".join('<div style="flex:%s;background:%s;padding:7px 6px;border-left:2px solid #2a1b4a">%s</div>'
                                                                            % (f, c, t) for t, c, f in parts)))


def house(x, y, s=1.0):
    return ('<g transform="translate(%d,%d) scale(%.2f)"><path d="M-26,0 v-30 l26,-22 l26,22 v30 z" fill="#ffd27a" stroke="%s" stroke-width="3"/>'
            '<path d="M-32,-28 l32,-28 l32,28" fill="none" stroke="%s" stroke-width="4"/><rect x="-8" y="-18" width="16" height="18" fill="#ffef9e" stroke="%s" stroke-width="2"/></g>'
            % (x, y, s, OUT, RD, OUT))


def arrow(x1, y1, x2, y2, col=PU, t=""):
    g = '<path d="M%d,%d L%d,%d" stroke="%s" stroke-width="4" marker-end="url(#ah)"/>' % (x1, y1, x2, y2, col)
    return g + (lbl((x1 + x2) // 2, min(y1, y2) - 8, t, 15) if t else "")


AH = '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>'


def s1():
    T = 4
    g = (cloud(500, 170, "Ethernet-сеть оператора", 420, "#d6c2ff") + swc(380, 200, "", 90) + swc(500, 130, "", 90) + swc(620, 200, "", 90)
         + ln("M425,200 L575,200 M380,186 L460,130 M620,186 L540,130", CY, 4, glow=True) + lbl(500, 280, "Оптоволоконные линии", 15)
         + '<rect x="20" y="60" width="230" height="230" rx="16" fill="#fff6dc" stroke="%s" stroke-width="3"/>' % OUT + lbl(135, 90, "LAN • Офис А", 17)
         + '<rect x="750" y="60" width="230" height="230" rx="16" fill="#fff6dc" stroke="%s" stroke-width="3"/>' % OUT + lbl(865, 90, "LAN • Офис Б", 17)
         + pc(70, 150) + pc(70, 240) + swc(190, 200, "", 80) + pc(930, 150) + pc(930, 240) + swc(810, 200, "", 80)
         + flow("M230,200 L335,200", CY, T) + flow("M665,200 L770,200", CY, T) + env("M100,240 L190,200 L380,200 L500,130 L620,200 L810,200 L930,240", .2, 3.4, T))
    return "WAN на основе Ethernet", page("", stack(scp(g, "", 1000, 300),
        grid("1fr 1fr 1fr", panel("Оптическая среда", "<p>Связь на большие расстояния</p>", "g"), panel("Высокая скорость", "<p>40GbE • 100GbE</p>", "c"),
             panel("Интеграция с LAN", "<p>Привычные Ethernet-интерфейсы</p>", "e")),
        note("Дальность зависит от оптических модулей и линии связи", "info")))


def s3():
    T = 4
    techs = [("Телефонная сеть", "xDSL", OR), ("Кабельная сеть", "DOCSIS", "#ffd43b"), ("Ethernet", "Витая пара / оптика", CY), ("Сотовая сеть", "4G / 5G", LI),
             ("Спутниковая сеть", "Спутник + терминал", "#c9a8ff")]
    g = cloud(500, 55, "Оператор связи ISP", 260, "#d6c2ff")
    for k, (t, d, c) in enumerate(techs):
        x = 100 + k * 200
        g += flow("M500,85 C500,130 %d,120 %d,170" % (x, x), c, T, 1) + ('<rect x="%d" y="170" width="180" height="190" rx="14" fill="#fff6dc" stroke="%s" stroke-width="3"/>'
                                                                          '<rect x="%d" y="170" width="180" height="40" rx="14" fill="%s" stroke="%s" stroke-width="3"/>' % (x - 90, OUT, x - 90, c, OUT))
        g += lbl(x, 197, t, 15) + lbl(x, 235, d, 13, bold=700) + house(x, 330)
    return "Технологии подключения абонентов", page("", stack(scp(g, "", 1000, 380),
        note("Выбор технологии: скорость • стоимость • расстояние • доступность", "chart", "g", "Исторические технологии: Frame Relay, ATM")))


def s4():
    T = 4
    g = (cloud(450, 160, "Сеть оператора Frame Relay", 380, "#d6c2ff") + rt(100, 200, "DTE A", 40) + rt(820, 90, "DTE Б", 40) + rt(820, 290, "DTE В", 40)
         + ln("M140,195 C300,195 350,100 780,90", OR, 6) + ln("M140,210 C300,210 350,290 780,290", CY, 6) + chip(520, 130, "PVC 1", "#ffd27a", 15) + chip(520, 270, "PVC 2", "#bff5f0", 15)
         + chip(190, 140, "DLCI 102", "#ffb347", 13) + chip(190, 260, "DLCI 103", "#7fe3e0", 13) + chip(240, 80, "Один физический интерфейс", "#fff6dc", 12)
         + env("M140,195 C300,195 350,100 780,90", 0, 2, T) + env("M140,210 C300,210 350,290 780,290", 2, 2, T))
    return "Frame Relay", page("", stack(scp(g, "", 1000, 340),
        grid("1fr 1fr 1fr", panel("PVC", "<p>Постоянный виртуальный канал</p>", "g"), panel("DLCI", "<p>Локальный идентификатор канала</p>", "g"),
             panel("NBMA", "<p>Множественный доступ без широковещания</p>", "g")),
        note("Канальный уровень OSI • историческая технология WAN", "info")))


def s6():
    T = 4
    cols = (OR, "#7ed957", "#ff5ca8", PU)
    g = "".join(chip(70, 60 + k * 60, t, "#fff6dc", 15) + ln("M120,%d L250,190" % (60 + k * 60), c, 4) for k, (t, c) in enumerate(zip(("Видео", "Веб", "VoIP", "Почта"), cols)))
    g += rt(280, 190, "", 28) + swc(390, 190, "ATM", 80) + cloud(600, 170, "Сеть ATM", 300, "#e8f4ff") + swc(810, 190, "ATM", 80) + rt(920, 190, "", 28)
    g += "".join('<rect x="%d" y="200" width="22" height="22" rx="3" fill="%s" stroke="%s" stroke-width="2"><animate attributeName="x" values="%d;%d" dur="4s" repeatCount="indefinite"/></rect>'
                 % (450 + k * 28, cols[k % 4], OUT, 440 + k * 28, 480 + k * 28) for k, _ in enumerate(range(10)))
    g += '<rect x="300" y="300" width="60" height="44" fill="#ff8c42" stroke="%s" stroke-width="3"/><rect x="360" y="300" width="360" height="44" fill="#33c3c0" stroke="%s" stroke-width="3"/>' % (OUT, OUT)
    g += lbl(330, 290, "Заголовок · 5 байт", 13) + lbl(540, 290, "Полезная нагрузка · 48 байт", 13) + lbl(510, 380, "Ячейка ATM · 53 байта", 20)
    return "ATM", page("Асинхронный режим передачи", stack(scp(g, "", 1000, 400),
        grid("1fr 1fr", panel("PVC", "<p>Постоянный виртуальный канал</p>", "g"), panel("SVC", "<p>Коммутируемый виртуальный канал</p>", "g"))))


def s8():
    T = 4
    g = (pc(70, 170, "Компьютер") + swc(220, 170, "Модем абонента", 80) + cloud(500, 160, "ТСОП / PSTN", 300, "#d6c2ff") + swc(760, 170, "Модем провайдера", 80) + cloud(910, 160, "Интернет", 150)
         + ln("M95,170 L180,170", BLU, 3) + lbl(140, 155, "0 1 0 1", 13) + '<path d="M260,170 q20,-30 40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0" stroke="%s" stroke-width="4" fill="none"/>' % OR
         + chip(500, 220, "Аналоговый сигнал", "#ffb347", 13) + env("M95,170 L720,170 L860,170", 0, 3.4, T) + chip(500, 290, "До 56 кбит/с к абоненту", "#fff6dc", 15))
    return "Телефонные линии", page("Коммутируемый доступ Dial-Up", stack(scp(g, "", 1000, 320),
        panel("Технологии на медных линиях", '<span class="sp-chip">Dial-Up</span><span class="sp-chip">ISDN</span><span class="sp-chip">DSL</span><span class="sp-chip">E1 / T1</span>', "g")))


def s10():
    ts = '<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:4px;font-weight:900;text-align:center">%s</div>' % "".join(
        '<div style="background:%s;border:3px solid #2a1b4a;border-radius:8px;padding:6px 0;color:#2a1b4a">%s</div>' % (c, t) for t, c in
        (("TS0", "#ffb347"), ("TS1", "#7fe3e0"), ("…", "#7fe3e0"), ("TS15", "#7fe3e0"), ("TS16", "#c9a8ff"), ("TS17", "#7fe3e0"), ("…", "#7fe3e0"), ("TS31", "#7fe3e0")))
    return "Стандарт E1", page("E1 • 2,048 Мбит/с · 32 интервала по 64 кбит/с", stack(panel("", ts + '<p><span class="sp-chip">TS0 — синхронизация</span>'
                                                                                            '<span class="sp-chip">TS16 — сигнализация в телефонии</span>'
                                                                                            '<span class="sp-chip">30 интервалов для полезной нагрузки</span></p>', "g"),
        panel("Скорости цифровых линий", tab(["Уровень", "США", "Европа"], [["0", "64 кбит/с", "64 кбит/с"], [("1", "y"), ("T1 · 1,544 Мбит/с", "y"), ("E1 · 2,048 Мбит/с", "y")],
                                                                          ["2", "T2 · 6,312 Мбит/с", "E2 · 8,448 Мбит/с"], ["3", "T3 · 44,736 Мбит/с", "E3 · 34,368 Мбит/с"]]), "c"),
        note("T1 — 24 канала по 64 кбит/с", "info")))


def s12():
    def card(t, f, b, d, tot):
        return panel(t, '<div class="sb-big">%s</div><ul class="li"><li><b>B:</b> %s</li><li><b>D:</b> %s</li></ul><p style="text-align:center"><b>%s</b></p>' % (f, b, d, tot), "e")
    return "ISDN", page("Цифровая сеть с интеграцией служб", stack(grid("1fr 1fr 1fr", card("BRI", "2B + D", "2 × 64 кбит/с", "16 кбит/с", "144 кбит/с — сумма B и D"),
                                                                       card("PRI на T1", "23B + D", "23 × 64 кбит/с", "64 кбит/с", "1,544 Мбит/с — скорость линии"),
                                                                       card("PRI на E1", "30B + D", "30 × 64 кбит/с", "64 кбит/с", "2,048 Мбит/с — скорость линии")),
        note("B — голос и данные · D — сигнализация", "info")))


def s15():
    T = 3
    g = (pc(110, 90, "Абонент") + swc(330, 110, "DSL-модем", 90) + cloud(780, 90, "Сеть провайдера", 240, "#d6c2ff") + swc(700, 95, "DSLAM", 90)
         + flow("M140,95 L285,105", BLU, T) + flow("M375,105 L655,95", OR, T) + chip(510, 60, "Медная витая пара", "#ffd27a", 13))
    f = ('<svg viewBox="0 0 1000 170" style="width:100%;max-height:22vh"><path d="M60,130 H960 M60,130 V10" stroke="#2a1b4a" stroke-width="3"/>'
         '<rect x="80" y="40" width="160" height="90" fill="#ffb347" stroke="#2a1b4a" stroke-width="3"/><rect x="300" y="40" width="250" height="90" fill="#d7f27a" stroke="#2a1b4a" stroke-width="3"/>'
         '<rect x="600" y="40" width="330" height="90" fill="#7fe3e0" stroke="#2a1b4a" stroke-width="3"/>'
         + lbl(160, 92, "Телефония", 17) + lbl(425, 82, "Восходящий", 17) + lbl(425, 104, "канал", 17) + lbl(765, 82, "Нисходящий", 17) + lbl(765, 104, "канал", 17)
         + lbl(160, 158, "0–4 кГц", 15) + lbl(425, 158, "26–138 кГц", 15) + lbl(765, 158, "138–1100 кГц", 15) + "</svg>")
    return "DSL", page("Цифровая абонентская линия", stack(scp(g, "", 1000, 180), panel("Частоты ADSL", f + "<p style='text-align:center'><i>Схема не в масштабе</i></p>", "e"),
        grid("1fr 1fr", panel("ADSL", "<p>К абоненту быстрее, чем от абонента</p>", "e"), panel("SDSL", "<p>Одинаковая скорость в обе стороны</p>", "e"))))


def s17():
    T = 3
    g = (pc(80, 90, "Абонент") + swc(250, 100, "Кабельный модем", 90) + '<rect x="440" y="80" width="40" height="34" rx="6" fill="#c9a8ff" stroke="%s" stroke-width="3"/>' % OUT
         + cloud(810, 90, "", 220, "#e8f4ff") + chip(810, 110, "CMTS", "#7fe3e0", 16) + lbl(810, 55, "Сеть провайдера", 14) + lbl(460, 60, "Коаксиальный кабель", 13)
         + flow("M110,95 L205,100", BLU, T) + flow("M295,100 L440,97", OUT, T) + flow("M480,97 L700,95", OUT, T) + ln("M460,114 L400,170 M460,114 L520,170", OUT, 3)
         + house(400, 210) + house(520, 210) + chip(460, 250, "Общая полоса для абонентов сегмента", "#c9a8ff", 13))
    return "Кабельное подключение", page("Интернет по сети кабельного ТВ", stack(scp(g, "", 1000, 270),
        grid("1.4fr 1fr", panel("Пример частотного плана", "<p>Восходящий: от абонента · 5–42 МГц ➜</p><p>Нисходящий: к абоненту · 50–860 МГц ⬅</p>", "v"),
             panel("DOCSIS", "<p>Передача данных по кабельной сети. Уровни 1 и 2 модели OSI.</p>", "e"))))


def s18():
    T = 3
    g = (srv(110, 120, "Головная станция / CMTS", 4) + '<rect x="420" y="50" width="90" height="80" rx="10" fill="#ddd" stroke="%s" stroke-width="3"/>' % OUT + lbl(465, 150, "Оптический узел", 14)
         + flow("M150,90 L415,90", CY, T) + chip(285, 70, "Оптоволокно", "#7fe3e0", 13) + flow("M510,90 C600,90 640,60 720,60", OR, T) + flow("M510,90 C600,90 640,140 720,140", OR, T)
         + house(760, 80) + house(760, 160) + chip(630, 40, "Коаксиальный кабель", "#ffb347", 13))
    def mini(kind):
        if kind == "t":
            return "".join('<rect x="%d" y="30" width="90" height="50" fill="%s" stroke="%s" stroke-width="2.5"/>' % (40 + k * 90, c, OUT) + lbl(85 + k * 90, 62, str(k + 1), 18)
                           for k, c in enumerate((CY, OR, LI))) + ln("M30,90 H330", OUT, 3) + lbl(180, 112, "t", 16)
        if kind == "f":
            return "".join('<rect x="40" y="%d" width="270" height="24" fill="%s" stroke="%s" stroke-width="2.5"/>' % (20 + k * 26, c, OUT) + lbl(175, 38 + k * 26, str(3 - k), 16)
                           for k, c in enumerate((LI, OR, CY))) + ln("M30,100 H330", OUT, 3) + lbl(180, 120, "f", 16)
        return ('<rect x="40" y="25" width="270" height="65" fill="url(#cd)" stroke="%s" stroke-width="2.5"/>' % OUT + ln("M30,100 H330", OUT, 3) + lbl(180, 120, "f", 16)
                + '<defs><pattern id="cd" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" fill="%s"/><circle cx="8" cy="8" r="4" fill="%s"/>'
                  '<path d="M0,16 L16,0" stroke="%s" stroke-width="3"/></pattern></defs>' % (LI, OR, CY))
    return "Кабельное подключение", page("HFC и доступ к общей среде", stack(scp(g, "", 900, 210),
        panel("Принципы множественного доступа", grid("1fr 1fr 1fr", panel("TDMA — по времени", scn(mini("t"), 360, 130), "e"),
                                                     panel("FDMA — по частоте", scn(mini("f"), 360, 130), "e"), panel("CDMA — по коду", scn(mini("c"), 360, 130), "e")), "c"),
        grid("1fr 1fr", note("Физический уровень: ширина канала и модуляция", "info", "e"), note("Канальный уровень: правила доступа MAC", "info", "e"))))


def s19():
    T = 3
    g = (srv(110, 230, "Сеть оператора", 5) + bld(820, 140, "Квартира", 110, 110, "#ffe7b0") + bld(820, 330, "Офис", 130, 110, "#a8d8ff")
         + flow("M150,150 C400,150 500,110 760,110", OR, T) + chip(420, 110, "Витая пара / RJ-45", "#fff6dc", 14) + chip(600, 70, "1 Гбит/с возможен по витой паре", "#fff6dc", 13)
         + flow("M150,200 C400,200 500,290 750,290", CY, T) + chip(420, 250, "Оптоволокно", "#fff6dc", 14))
    return "Ethernet", page("Подключение абонентов", stack(scp(g, "", 1000, 360),
        grid("1fr 1fr", panel("Для дома", '<div class="sb-big">100 Мбит/с – 1 Гбит/с</div>', "e"), panel("Для бизнеса", '<div class="sb-big">1–10 Гбит/с</div>', "c")),
        note("Скорость зависит от тарифа и оборудования.", "info")))


def s21():
    rows = [("FTTN", "до сетевого узла", 1), ("FTTC", "до шкафа рядом с домами", 2), ("FTTB", "до здания", 3), ("FTTH", "до квартиры или дома", 4)]
    pts_x = [230, 400, 570, 740, 900]
    g = ""
    for k, (t, d, end) in enumerate(rows):
        y = 50 + k * 85
        g += chip(70, y, t, "#d7f27a", 17) + lbl(70, y + 26, d, 11)
        g += ln("M%d,%d L%d,%d" % (pts_x[0], y, pts_x[end], y), CY, 7, glow=True)
        if end < 4:
            g += ln("M%d,%d L%d,%d" % (pts_x[end], y, pts_x[4], y), OR, 7)
        g += "".join('<rect x="%d" y="%d" width="46" height="40" rx="5" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x - 23, y - 20, c, OUT)
                     for x, c in zip(pts_x, ("#8fb4d9", "#c9d6e3", "#c9d6e3", "#d8b48a", "#ffd27a")))
        g += env("M%d,%d L%d,%d" % (pts_x[0], y, pts_x[4], y), k * .5, 2.6, 4)
    g += "".join(lbl(x, 395, t, 13) for x, t in zip(pts_x, ("Оператор", "Сетевой узел", "Шкаф у домов", "Здание", "Квартира")))
    return "Ethernet и оптический доступ", page("FTTx — где заканчивается оптоволокно", stack(scp(g, "", 1000, 410),
        grid("1fr 1fr", note("Бирюзовый — оптоволокно · оранжевый — медный участок", "info", "c"),
             note("FTTx описывает точку окончания волокна.", "info", "e", "xPON — семейство пассивных оптических сетей."))))


def s23():
    T = 3
    a = swc(150, 110, "Ethernet-коммутатор оператора", 150) + "".join(flow("M225,%d C450,%d 550,%d 760,%d" % (100 + k * 10, 100 + k * 10, 40 + k * 60, 40 + k * 60), CY, T, 1) + house(800, 60 + k * 60, .8)
                                                                      for k in range(3)) + chip(470, 40, "Отдельное волокно до каждого абонента", "#d7f27a", 12)
    b = (swc(110, 110, "OLT", 110, OR) + flow("M165,110 L380,110", CY, T) + chip(270, 80, "Общее волокно до сплиттера", "#d7f27a", 12)
         + '<rect x="380" y="85" width="110" height="50" rx="10" fill="#ffb347" stroke="%s" stroke-width="3"/>' % OUT + lbl(435, 115, "Сплиттер", 15)
         + "".join(flow("M490,110 C580,110 600,%d 680,%d" % (40 + k * 70, 40 + k * 70), CY, T, 1) + chip(710, 45 + k * 70, "ONT", "#d7f27a", 13) + house(800, 60 + k * 70, .8) for k in range(3)))
    return "Ethernet и оптический доступ", page("PON — пассивная оптическая сеть · EPON • GPON • 10G-EPON", stack(
        panel("Точка — точка", scn(a, 900, 230), "g"), panel("PON: точка — многоточка", scn(b, 900, 240), "g"),
        grid("1fr 1fr 1fr", note("OLT — у оператора", "info", "e"), note("Сплиттер — делит оптическую мощность", "info", "e"), note("ONT — у абонента", "info", "e"))))


def s25():
    T = 3
    a = (pc(80, 70, "Смартфон") + tower(330, 100, "Базовая станция") + srv(590, 100, "Сеть оператора") + cloud(850, 70, "Интернет", 160)
         + '<path d="M110,60 q100,-30 205,10" stroke="%s" stroke-width="3" fill="none" stroke-dasharray="8 6"/>' % CY + lbl(210, 40, "Радиоканал", 13)
         + flow("M345,70 L560,70", OR, T) + flow("M620,70 L770,70", OR, T))
    hexes = "".join('<polygon points="%s" fill="%s" fill-opacity=".35" stroke="%s" stroke-width="2.5"/>' % (
        " ".join("%d,%d" % (cx + 50 * __import__("math").cos(a * 3.14159 / 3), cy + 50 * __import__("math").sin(a * 3.14159 / 3)) for a in range(6)), LI, OUT) + tower(cx, cy + 20)
                    for cx, cy in ((500, 160), (420, 110), (580, 110), (420, 210), (580, 210), (500, 60), (500, 260)))
    b = ('<circle cx="450" cy="160" r="150" fill="%s" fill-opacity=".12" stroke="%s" stroke-width="3"/><circle cx="560" cy="160" r="150" fill="%s" fill-opacity=".12" stroke="%s" stroke-width="3"/>'
         % (CY, CY, PU, PU)) + hexes + chip(170, 160, "Соты — условная модель", "#fff6dc", 14) + chip(840, 160, "Зоны покрытия могут перекрываться", "#fff6dc", 13)
    return "Беспроводные технологии", page("Как устроена сотовая сеть", stack(scp(a, "", 1000, 160), scp(b, "", 1000, 330),
        grid("1.4fr 1fr", note("3G • 4G • 5G • 6G (в разработке)", "wifi", "e"), note("G — поколение", "info", "c"))))


def s26():
    T = 3
    a = tower(90, 150, "Базовая станция") + pc(300, 140, "Смартфон") + '<path d="M120,80 q100,-10 160,40" stroke="%s" stroke-width="3" fill="none" stroke-dasharray="8 6"/>' % CY
    a += env("M120,80 q100,-10 160,40", 0, 1.6, T)
    b = tower(90, 150, "Базовая станция") + house(320, 150, 1.4) + lbl(320, 180, "Абонентская антенна", 13) + '<path d="M120,80 q100,-10 170,20" stroke="%s" stroke-width="3" fill="none" stroke-dasharray="8 6"/>' % OR
    b += env("M120,80 q100,-10 170,20", .6, 1.6, T)
    return "Беспроводные технологии", page("LTE и WiMAX", stack(grid("1fr 1fr",
        panel("LTE · Long-Term Evolution", "<p style='text-align:center'><b>Мобильный широкополосный доступ</b></p>" + scn(a, 400, 200), "g"),
        panel("WiMAX · семейство IEEE 802.16", "<p style='text-align:center'><b>Беспроводная последняя миля</b></p>" + scn(b, 400, 200), "g")),
        note("LTE и WiMAX используют радиоканал для доступа к сети", "wifi", "e")))


def s28():
    T = 4
    g = ('<g transform="translate(500,60)"><rect x="-90" y="-14" width="70" height="28" fill="#3a86e0" stroke="%s" stroke-width="2.5"/><rect x="20" y="-14" width="70" height="28" fill="#3a86e0" '
         'stroke="%s" stroke-width="2.5"/><rect x="-20" y="-24" width="40" height="48" rx="8" fill="#8ec5ff" stroke="%s" stroke-width="3"/></g>' % (OUT, OUT, OUT)
         + chip(720, 40, "Спутник-ретранслятор", "#fff6dc", 13) + chip(800, 100, "Геостационарная орбита ≈ 35 786 км", "#fff6dc", 12)
         + cloud(90, 280, "Сеть оператора", 150) + srv(230, 320, "") + '<path d="M300,300 q40,-60 80,-20" fill="#ddd" stroke="%s" stroke-width="3"/>' % OUT + lbl(320, 200, "Земная станция", 14)
         + '<path d="M620,300 q40,-60 80,-20" fill="#ddd" stroke="%s" stroke-width="3"/>' % OUT + lbl(660, 200, "Антенна VSAT", 14) + bld(820, 340, "Сеть абонента", 160, 90, "#8fb4d9")
         + chip(770, 300, "ODU", "#7fe3e0", 12) + chip(860, 300, "IDU", "#7fe3e0", 12)
         + ln("M340,270 L480,90", LI, 3, True) + ln("M520,90 L660,270", LI, 3, True) + env("M340,270 L480,90 L520,90 L660,270", 0, 3, T) + env("M660,270 L520,90 L480,90 L340,270", 2, 1.8, T))
    return "Беспроводные технологии", page("VSAT — спутниковый доступ", stack(scp(g, "", 1000, 380),
        grid("1fr 1fr 1fr", panel("ODU", "<p>Наружный приёмопередатчик</p>", "e"), panel("IDU", "<p>Внутренний спутниковый модем</p>", "e"),
             panel("Применение", "<p>Удалённые объекты, суда, аварийная связь</p>", "e"))))


def s29():
    def nest(outer, mid, inner, col):
        return seg([(outer, "#7fe3e0", 1)]) + '<div style="margin:-6px 24px 0">%s</div>' % seg([(mid, "#d7f27a", 1)]) + '<div style="margin:-6px 60px 0">%s</div>' % seg([(inner, col, 1)])
    return "Технологии поверх других", page("", stack(grid("1fr 1fr",
        panel("PPP и PPPoE", nest("Кадр Ethernet", "PPPoE", "PPP", "#ffb347") + "<p>PPP — связь точка-точка</p>", "e"),
        panel("GRE", nest("Внешний IP", "GRE", "Исходный пакет", "#ffb347") + "<p>Туннель поверх IP</p>", "e"),
        panel("VPN", scn(rt(70, 60) + rt(430, 60) + '<rect x="110" y="40" width="280" height="40" rx="20" fill="#d7f27a" stroke="%s" stroke-width="3"/>' % OUT + lbl(250, 66, "🔒", 20)
                         + cloud(250, 40, "", 200, "#c9e8ff") + env("M110,60 L390,60", 0, 2, 3), 500, 120) + "<p>IPsec — один из способов защиты VPN</p>", "e"),
        panel("DMVPN", scn(rt(250, 30) + rt(80, 120) + rt(250, 120) + rt(420, 120) + ln("M250,55 L80,100 M250,55 L420,100", LI, 4) + ln("M110,125 L390,125", OUT, 2.5, True), 500, 160)
              + "<p>Центральный узел и прямые туннели</p>", "e")),
        note("Последовательная передача — биты по очереди · параллельная — несколько бит одновременно", "info")))


def s32():
    rows = '<div style="display:grid;grid-template-columns:200px 1fr;gap:6px;font-weight:900;color:#2a1b4a">%s</div>'
    cell = lambda t, c, extra="": '<div style="background:%s;border:3px solid #2a1b4a;border-radius:10px;padding:10px;display:grid;place-items:center;%s">%s</div>' % (c, extra, t)
    body = rows % (cell("Сетевой", "#cfe2ff") + cell('<span class="sp-chip">IP</span> <span class="sp-chip">IPX</span>', "#cfe2ff")
                   + cell("Канальный", "#ffe7b0") + '<div style="display:grid;grid-template-columns:110px 1fr;gap:6px">%s</div>' % (
                       cell("PPP", "#ffb347") + '<div style="display:grid;gap:6px">%s</div>' % (cell("NCP: IPCP · IPXCP", "#e3d6ff") + cell("LCP: управление, сжатие, аутентификация, опции", "#d7f27a")
                                                                                              + cell("HDLC", "#e6e6e6")))
                   + cell("Физический", "#ffd0dc") + cell("EIA/TIA-232, V.35, ISDN", "#ffd0dc"))
    return "PPP — структура протокола", page("", stack(panel("", body, "g"), note("IPCP управляет IP, IPXCP — IPX: для каждого сетевого протокола свой NCP", "info", "e")))


def s33():
    flow_ = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;font-weight:900;text-align:center">%s</div>' % "".join(
        '<div style="background:%s;border:3px solid #2a1b4a;border-radius:10px;padding:10px;color:#2a1b4a;font-size:calc(20px*var(--fz,1))">%s</div>' % (c, t)
        for t, c in (("LCP", "#7fe3e0"), ("Аутентификация<br><small>если согласована</small>", "#ffe48a"), ("NCP", "#7fe3e0"), ("Передача данных", "#ffe48a")))
    return "LCP и NCP", page("Как PPP поднимает соединение", stack(panel("", flow_, "g"), grid("1fr 1fr",
        panel("LCP — управление каналом", '<ul class="li"><li>Устанавливает и завершает канал</li><li>Согласует параметры и проверяет связь</li></ul>', "g"),
        panel("NCP — настройка сетевых протоколов", "<p>Для каждого протокола — свой NCP:</p><p><span class='sp-chip'>IPCP → IPv4</span> <span class='sp-chip'>IPv6CP → IPv6</span></p>", "g"))))


def s35():
    T = 6

    def ex(msgs, t0=0):
        g = rt(70, 80, "R1", 28) + rt(530, 80, "R2", 28)
        for k, (m, d, c) in enumerate(msgs):
            y = 30 + k * 32
            p = "M110,%d L490,%d" % (y, y) if d > 0 else "M490,%d L110,%d" % (y, y)
            g += ln(p, c, 3) + lbl(300, y - 5, m, 13) + env(p, t0 + k * .7, .7, T)
        return g
    s1_ = ex([("Configure-Request (LCP)", 1, CY), ("Configure-Ack (LCP)", -1, CY), ("Configure-Request (IPCP)", 1, PU), ("Configure-Ack (IPCP)", -1, PU)])
    s2_ = ex([("Echo-Request", 1, CY), ("Echo-Reply", -1, CY), ("Обмен данными IPv4", 1, PU)])
    s3_ = ex([("Terminate-Request (IPCP)", 1, PU), ("Terminate-Ack (IPCP)", -1, PU), ("Terminate-Request (LCP)", 1, CY), ("Terminate-Ack (LCP)", -1, CY)])
    return "LCP и NCP", page("", stack(
        grid("2fr 1fr", panel("1. Установление канала: настройка LCP, затем NCP", scn(s1_, 600, 160), "g"), stack(note("PAP / CHAP — если согласовано", "lock", "e"),
                                                                                                           note("При несогласии: Configure-Nak / Configure-Reject", "warn", "g"))),
        grid("2fr 1fr", panel("2. Обслуживание канала LCP", scn(s2_, 600, 130), "g"), note("При ошибке: Code-Reject / Protocol-Reject", "warn", "g")),
        panel("3. Закрытие канала: закрытие NCP, затем LCP", scn(s3_, 600, 160), "g")))


def s37():
    T = 4
    g = (rt(120, 200, "R1 · Инициатор", 40) + rt(880, 200, "R2 · Ответчик", 40) + ln("M160,200 L840,200", OUT, 3) + lbl(500, 230, "Двухэтапная аутентификация PAP", 16)
         + chip(330, 60, "Имя пользователя: R1 · Пароль: Eltex12345#", "#fff6dc", 14) + ln("M170,100 L700,100", PU, 5) + env("M170,100 L700,100", 0, 1.6, T)
         + ln("M830,150 L300,150", "#2f9e44", 5) + lbl(640, 140, "Принять / отклонить", 15) + env("M830,150 L300,150", 2, 1.6, T))
    return "PAP и CHAP", page("Аутентификация PPP · установка PPP-соединения", stack(scp(g, "", 1000, 280),
        note("Имя пользователя и пароль передаются открытым текстом", "warn", "r")))


def s39():
    T = 6
    g = (rt(120, 180, "R1 · Проверяемый узел", 40) + rt(880, 180, "R2 · Проверяющий узел", 40) + chip(500, 40, "Канал PPP установлен", "#ffe7b0", 16)
         + ln("M840,100 L160,100", "#2f9e44", 5) + lbl(500, 90, "① Challenge · случайный вызов", 15) + env("M840,100 L160,100", 0, 1.6, T)
         + ln("M160,180 L840,180", PU, 5) + lbl(500, 170, "② Response · имя R1 и хеш", 15) + env("M160,180 L840,180", 2, 1.6, T)
         + ln("M840,260 L160,260", "#2f9e44", 5) + lbl(500, 250, "③ Success / Failure", 15) + env("M840,260 L160,260", 4, 1.6, T))
    return "PAP и CHAP", page("Аутентификация CHAP", stack(scp(g, "", 1000, 300), note("MD5(ID || секрет || вызов)", "lock", "g"),
        note("Общий секрет по сети не передаётся", "shield", "e")))


def s41():
    T = 3
    a = pc(80, 80, "ПК1") + cloud(850, 70, "Провайдер", 180) + flow("M120,90 L750,90", BLU, T)
    b = pc(80, 80, "ПК1") + swc(440, 90, "DSL-модем", 90) + cloud(850, 70, "Провайдер", 180) + flow("M120,90 L395,90", BLU, T) + flow("M485,90 L750,90", BLU, T)
    b += lbl(260, 120, "Ethernet", 15) + lbl(620, 120, "DSL", 15)
    return "PPPoE", page("", stack(panel("PPP по телефонной линии", seg([("PPP", "#ffe48a", 1), ("IP-пакет", "#a8d8ff", 2)]) + scn(a, 1000, 140), "g"),
                                   panel("PPP поверх Ethernet", seg([("Ethernet", "#d7f27a", 1), ("PPPoE", "#e3d6ff", 1), ("PPP", "#ffe48a", 1), ("IP-пакет", "#a8d8ff", 1.5)]) + scn(b, 1000, 150), "g")))


def s43():
    return "MTU и TCP MSS", page("", stack(
        panel("Ethernet", "<p style='text-align:center'><b>IP MTU = 1500 байт · MSS = 1460 байт</b></p>"
              + seg([("Ethernet", "#ffe7b0", 1.2), ("IPv4<br><small>20 байт</small>", "#a8d8ff", 1), ("TCP<br><small>20 байт</small>", "#bff5e6", 1),
                     ("Данные<br><small>1460 байт</small>", "#ffd0dc", 1.4), ("FCS", "#ffe7b0", .7)]), "g"),
        panel("PPPoE", "<p style='text-align:center'><b>IP MTU = 1492 байт · MSS = 1452 байт</b></p>"
              + seg([("Ethernet", "#ffe7b0", 1), ("PPPoE + PPP<br><small>8 байт</small>", "#ff8c42", 1.2), ("IPv4<br><small>20 байт</small>", "#a8d8ff", 1),
                     ("TCP<br><small>20 байт</small>", "#bff5e6", 1), ("Данные<br><small>1452 байт</small>", "#ffd0dc", 1.3), ("FCS", "#ffe7b0", .6)]), "c"),
        note("IPv4 и TCP без опций", "info")))


def s44():
    T = 4
    g = (rt(130, 110, "R1", 50) + rt(870, 110, "R2", 50) + cloud(500, 80, "IP-сеть", 240) + '<rect x="180" y="95" width="640" height="40" rx="20" fill="#7fe3e0" stroke="%s" stroke-width="3"/>' % OUT
         + ln("M200,115 L800,115", OUT, 3, True) + env("M190,115 L810,115", 0, 3, T))
    return "Туннелирование", page("Пример инкапсуляции GRE", stack(seg([("Внешний IP-заголовок", "#ff8c42", 1), ("Заголовок GRE", "#d7f27a", 1), ("Исходный IP-пакет", "#7fe3e0", 1)], 20),
        scp(g, "", 1000, 200), grid("1fr 1fr", panel("L3 · IP-пакеты", "<p>IPv4-over-IPv4, GRE, VTI с IPsec</p>", "e"), panel("L2 · Ethernet-кадры", "<p>L2TPv3, Ethernet over GRE</p>", "e")),
        note("Между R1 и R2 нужна IP-связность", "link", "g")))


def s46():
    T = 4
    g = (rt(130, 100, "R1", 50) + rt(870, 100, "R2", 50) + cloud(500, 60, "IP-сеть", 280, "#e3d6ff")
         + '<rect x="180" y="80" width="640" height="44" rx="22" fill="#7fe3e0" stroke="%s" stroke-width="3"/>' % OUT + lbl(500, 110, "Туннель GRE", 20) + env("M190,102 L810,102", 0, 3, T))
    return "GRE", page("", stack(scp(g, "", 1000, 170),
        seg([("Внешний IPv4", "#c9a8ff", 1), ("GRE", "#e3d6ff", .8), ("Внутренний IP", "#a8d8ff", 1), ("TCP", "#ffe7b0", .8), ("Данные", "#ffd0dc", .9)], 20),
        grid("1fr 1fr", note("24 байта без опций — внешний IPv4 + GRE", "info", "e"), note("Исходный IP-пакет — внутренний IP + TCP + данные", "info", "c")),
        note("IP Protocol = 47", "bolt", "g")))


def s48():
    T = 4
    g = (cloud(110, 100, "LAN-1", 150, "#cfe2ff") + rt(250, 100, "R1", 28) + cloud(500, 120, "WAN", 200, "#e3d6ff") + rt(750, 100, "R2", 28) + cloud(890, 100, "LAN-2", 150, "#dff5b0")
         + '<rect x="280" y="75" width="440" height="34" rx="17" fill="#ffd43b" stroke="%s" stroke-width="3"/>' % OUT + lbl(500, 98, "IPsec-туннель", 16) + env("M280,92 L720,92", 0, 2.6, T))
    return "IPsec и VPN", page("", stack(scp(g, "", 1000, 200),
        grid("1fr 1fr 1fr", panel("IKE", "<p>Согласование ключей</p>", "e"), panel("ESP", "<p>Шифрование и целостность</p>", "e"), panel("AH", "<p>Целостность и аутентификация</p>", "e")),
        grid("1fr 1fr", note("Route-based · маршруты через VTI", "route", "g"), note("Policy-based · отбор по политикам", "plan", "g"))))


def _dm(on_demand=False, T=4):
    g = (cloud(70, 180, "LAN-0", 110, "#ffd0b8") + rt(200, 180, "HUB", 30) + cloud(470, 190, "WAN", 140, "#ddd") + rt(720, 70, "SPOKE-2", 28) + rt(720, 300, "SPOKE-1", 28)
         + cloud(880, 70, "LAN-2", 120, "#ffd0b8") + cloud(880, 300, "LAN-1", 120, "#ffd0b8") + ln("M230,180 L400,190 M540,190 L700,85 M540,190 L700,285", OUT, 3)
         + ln("M230,170 L690,75", "#c9a8ff", 12) + ln("M230,190 L690,295", "#c9a8ff", 12) + env("M230,170 L690,75", 0, 1.8, T))
    if on_demand:
        g += show(2, T, None, ln("M720,100 L720,270", CY, 5, True) + env("M720,100 L720,270", 2, 1.5, T) + chip(820, 185, "Туннель по запросу", "#bff5f0", 12))
    return g


def s50():
    return "DMVPN", page("", stack(grid("1fr 1fr", scp(_dm(), "GRE точка-точка", 1000, 380, "v"), scp(_dm(True), "DMVPN", 1000, 380, "v")),
        note("mGRE · туннели | NHRP · адреса | OSPF / BGP · маршруты | IPsec · защита", "info")))


def s52():
    g = _dm(True) + chip(200, 120, "NHRP-сервер", "#e3d6ff", 13) + chip(720, 20, "NHRP-клиент", "#e3d6ff", 13) + chip(720, 360, "NHRP-клиент", "#e3d6ff", 13)
    return "DMVPN и mGRE", page("", stack(scp(g, "", 1000, 400), grid("1fr 1fr", note("mGRE • несколько соседей на одном интерфейсе", "link", "g"),
                                                                       note("NHRP • помогает установить прямой туннель", "swap", "g")),
        note("Связь через WAN · Hub–Spoke · Spoke–Spoke по запросу", "info", "c")))


def s54():
    T = 4
    g = (cloud(110, 110, "192.168.0.0/24", 190, "#ffd0b8") + rt(290, 110, "R1", 26) + cloud(500, 110, "ISP", 130, "#ddd") + rt(710, 110, "R2", 26) + cloud(890, 110, "192.168.1.0/24", 190, "#ffd0b8")
         + ln("M320,110 L440,110 M560,110 L680,110", OUT, 3) + ln("M290,60 Q500,10 710,60", PU, 5) + chip(330, 40, "192.0.2.1/24", "#e3d6ff", 13) + chip(670, 40, "192.0.2.2/24", "#e3d6ff", 13)
         + chip(290, 175, "NBMA 203.0.113.1/24", "#7fe3e0", 12) + chip(710, 175, "NBMA 198.18.0.1/24", "#7fe3e0", 12) + env("M290,60 Q500,10 710,60", 0, 2.6, T))
    return "NHRP в DMVPN", page("", stack(scp(g, "", 1000, 200),
        grid("1fr 1fr", panel("1. Маршрут", "<p style='text-align:center'><b>192.168.1.0/24 → Tunnel0 через 192.0.2.2</b></p>", "e"),
             panel("2. Сопоставление NHRP", "<p style='text-align:center'><b>192.0.2.2 → 198.18.0.1</b></p>", "c")),
        panel("3. Инкапсуляция GRE", seg([("Внешний IP<br><small>203.0.113.1 → 198.18.0.1</small>", "#7fe3e0", 1.4), ("GRE", "#c9a8ff", .6),
                                          ("Внутренний IP<br><small>192.168.0.1 → 192.168.1.1</small>", "#ffd0b8", 1.4), ("Данные", "#cfe2ff", .7)]), "v")))


AR = {1: s1, 3: s3, 4: s4, 6: s6, 8: s8, 10: s10, 12: s12, 15: s15, 17: s17, 18: s18, 19: s19, 21: s21, 23: s23, 25: s25, 26: s26, 28: s28, 29: s29,
      32: s32, 33: s33, 35: s35, 37: s37, 39: s39, 41: s41, 43: s43, 44: s44, 46: s46, 48: s48, 50: s50, 52: s52, 54: s54}
