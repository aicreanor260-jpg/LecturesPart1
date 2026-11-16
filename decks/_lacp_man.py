# -*- coding: utf-8 -*-
"""LACP: ручные слайды по pptx (номер слайда pptx → слайды деки). Схемы перерисованы SVG с теми же портами,
скриншоты текста и консоли pptx перепечатаны дословно."""
from _pt_man import P, pts, box, topo, svg, bars, route, _env, SWC, PORT
import _pt_kit as K

AA = "AA:AA:AA:AA:AA:AA"
RING = "g12 g22 g23 g13 g12"


def _las(flow=True):
    """Слайд 10: два коммутатора, LLC — LAS (Collector/Distributor) — MAC/PHY, три пары кабелей; кадр идёт по шагам 1–6."""
    g = []
    cols = [("#e03131", 0), ("#1c3faa", 1), ("#2b8a3e", 2)]
    for sx, nm in ((40, "Коммутатор 1"), (440, "Коммутатор 2")):
        g.append('<text x="%d" y="22" text-anchor="middle" font-weight="700">%s</text>' % (sx + 150, nm))
        g.append(bars([(sx + 10, 32, 280, 34, "LLC (MAC Client) — Po1", False), (sx, 76, 300, 92, "", True)]))
        g.append('<text x="%d" y="94" text-anchor="middle" font-size="13" opacity=".8">LAS</text>' % (sx + 150))
        for k, (tx, nm2) in enumerate(((sx + 75, "Collector"), (sx + 225, "Distributor"))):
            g.append('<path d="M%d,104 l-48,46 h96 z" fill="none" stroke="currentColor" stroke-width="2"/>'
                     '<text x="%d" y="142" text-anchor="middle" font-size="13">%s</text>' % (tx, tx, nm2))
        for c, i in cols:
            x = sx + 40 + i * 110
            g.append(bars([(x - 30, 186, 60, 30, "MAC", False), (x - 30, 222, 60, 30, "PHY", False)]))
            g.append('<rect x="%d" y="258" width="40" height="16" fill="none" stroke="#b07a2a" stroke-width="2"/>' % (x - 20))
    for c, i in cols:
        x1, x2 = 80 + i * 110, 480 + i * 110
        yb = 300 + i * 14
        g.append('<path d="M%d,274 V%d H%d V274" fill="none" stroke="%s" stroke-width="3"/>' % (x1, 340 - i * 14, x2, c))
    g.append('<text x="10" y="130" font-size="12" opacity=".8" transform="rotate(-90 10 130)">канальный</text>'
             '<text x="10" y="270" font-size="12" opacity=".8" transform="rotate(-90 10 270)">физический</text>')
    if flow:   # Po1 → Distributor → MAC/PHY порта 1 → красный кабель → PHY/MAC → Collector → Po1
        path = "M190,50 L265,110 L80,200 L80,237 L80,340 L480,340 L480,237 L480,200 L515,110 L590,50"
        g.append(_env(path, 0.2, 6, 7.5))
        for k, (x, y, t) in enumerate(((190, 72, "1"), (300, 128, "2"), (120, 205, "3"), (120, 240, "4"), (440, 240, "5"), (555, 128, "6"))):
            g.append('<circle cx="%d" cy="%d" r="11" fill="#f08c00"/><text x="%d" y="%d" text-anchor="middle" fill="#fff" font-weight="800" '
                     'font-size="13">%s</text>' % (x, y, x, y + 5, t))
    return svg(780, 350, "".join(g))


def _lag(n_act, n_sb=0, broken=(), groups=None, flows=()):
    """Пачка каналов SW-1 ═ SW-2 (слайды 14, 21, 22): сплошные — активные, пунктир — запасные, красный крест — отказ."""
    n = n_act + n_sb
    sp = 26 if n > 6 else 46
    h = 60 + n * sp
    g = ['<rect x="30" y="20" width="70" height="%d" rx="8" fill="%s"/><rect x="680" y="20" width="70" height="%d" rx="8" fill="%s"/>'
         % (h - 40, SWC, h - 40, SWC),
         '<text x="65" y="%d" text-anchor="middle" fill="#fff" font-weight="800" transform="rotate(-90 65 %d)">SW-1</text>' % (h / 2, h / 2),
         '<text x="715" y="%d" text-anchor="middle" fill="#fff" font-weight="800" transform="rotate(90 715 %d)">SW-2</text>' % (h / 2, h / 2)]
    for i in range(n):
        y = 44 + i * sp
        sb = i >= n_act
        bad = i in broken
        g.append('<line x1="108" y1="%d" x2="672" y2="%d" stroke="%s" stroke-width="3.2" %s/>'
                 % (y, y, "#e03131" if bad else "currentColor", 'stroke-dasharray="10 7" opacity=".7"' if sb else ""))
        g.append('<circle cx="108" cy="%d" r="7" fill="%s"/><circle cx="672" cy="%d" r="7" fill="%s"/>' % (y, PORT, y, PORT))
        if bad:
            g.append('<path d="M378,%d l24,16 m0,-16 l-24,16" stroke="#e03131" stroke-width="4"/>' % (y - 8))
    for i, t0, d in flows:
        y = 44 + i * sp
        g.append(_env("M120,%d L660,%d" % (y, y), t0, d, 4))
    leg = ('<line x1="160" y1="%d" x2="210" y2="%d" stroke="currentColor" stroke-width="3"/><text x="218" y="%d">активный канал</text>'
           % (h - 2, h - 2, h + 3))
    if n_sb:
        leg += ('<line x1="430" y1="%d" x2="480" y2="%d" stroke="currentColor" stroke-width="3" stroke-dasharray="10 7"/>'
                '<text x="488" y="%d">запасной канал</text>' % (h - 2, h - 2, h + 3))
    return svg(780, h + 14, "".join(g) + leg)


LACPDU_ACT = """Link Aggregation Control Protocol
    LACP Version: 0x01
    TLV Type: Actor Information (0x01)
    TLV Length: 0x14
    Actor System Priority: 1
    Actor System ID: EltexEnt_8c:cd:d0 (e4:5a:d4:8c:cd:d0)
    Actor Key: 1000
    Actor Port Priority: 1
    Actor Port: 55
    Actor State: 0x3d, LACP Activity, Aggregation, Synchronization, Collecting, Distributing
        .... ...1 = LACP Activity: Active
        .... ..0. = LACP Timeout: Long Timeout
        .... .1.. = Aggregation: Aggregatable
        .... 1... = Synchronization: In Sync
        ...1 .... = Collecting: Enabled
        ..1. .... = Distributing: Enabled
        .0.. .... = Defaulted: No
        0... .... = Expired: No
    [Actor State Flags: **DCSG*A]
    Reserved: 000000
    TLV Type: Partner Information (0x02)
    TLV Length: 0x14
    Partner System Priority: 1
    Partner System: EltexEnt_2c:1c:c0 (e0:d9:e3:2c:1c:c0)
    Partner Key: 1000
    Partner Port Priority: 1
    Partner Port: 55
    Partner State: 0x3d, LACP Activity, Aggregation, Synchronization, Collecting, Distributing
        .... ...1 = LACP Activity: Active
        .... ..0. = LACP Timeout: Long Timeout
        .... .1.. = Aggregation: Aggregatable
        .... 1... = Synchronization: In Sync
        ...1 .... = Collecting: Enabled
        ..1. .... = Distributing: Enabled
        .0.. .... = Defaulted: No
        0... .... = Expired: No""".split("\n")

LACPDU_PAS = """Link Aggregation Control Protocol
    LACP Version: 0x01
    TLV Type: Actor Information (0x01)
    TLV Length: 0x14
    Actor System Priority: 1
    Actor System ID: EltexEnt_8c:cd:d0 (e4:5a:d4:8c:cd:d0)
    Actor Key: 1001
    Actor Port Priority: 1
    Actor Port: 52
    Actor State: 0x3c, Aggregation, Synchronization, Collecting, Distributing
        .... ...0 = [[LACP Activity: Passive]]
        .... ..0. = LACP Timeout: Long Timeout
        .... .1.. = Aggregation: Aggregatable
        .... 1... = Synchronization: In Sync
        ...1 .... = Collecting: Enabled
        ..1. .... = Distributing: Enabled
        .0.. .... = Defaulted: No
        0... .... = Expired: No
    [Actor State Flags: **DCSG**]
    Reserved: 000000""".split("\n")

HEAD7 = """Link Aggregation Control Protocol
    LACP Version: 0x01
    TLV Type: Actor Information (0x01)
    TLV Length: 0x14"""


def _hdr(hl):
    rows = HEAD7.split("\n") + ["    Actor System Priority: 1", "    Actor System ID: EltexEnt_8c:cd:d0 (e4:5a:d4:8c:cd:d0)",
                                "    Actor Key: 1001", "    Actor Port Priority: 1", "    Actor Port: 52"]
    return ["[[%s]]" % r if any(h in r for h in hl) else r for r in rows]


M = {
    3: [P(pts(["Между коммутаторами обычно идёт трафик нескольких VLAN — потеря этого канала очень чувствительна.",
               "Очевидная идея: добавить второй линк.", "Посмотрим, что будет на коммутаторах после подключения второго канала."]),
          topo(note="SW-1 и SW-2 соединены двумя линками: Gi0/2 и Gi0/3"))],
    4: [P(pts(["MAC-таблицы обоих коммутаторов пусты: адреса PC-A и PC-B неизвестны.",
               "Это обычная ситуация, если компьютеры долго не передавали трафик.", "PC-A отправляет кадр для PC-B."]),
          topo(t1=[(AA, "Gi0/1", True)], flows=[("A1", 0.2, 2.2)], T=4, note="Кадр от PC-A приходит на Gi0/1 коммутатора SW-1"))],
    5: [P([pts(["SW-1 изучает MAC источника <b>AA:AA:AA:AA:AA:AA</b> на порту Gi0/1."]),
           box('<ol class="li"><li>Кадр пришёл — MAC источника записывается в таблицу.</li>'
               '<li>MAC назначения известен — кадр копируется в этот порт.</li>'
               '<li>MAC назначения неизвестен — копия во все порты, кроме входящего (<b>unknown unicast</b>).</li></ol>', "am",
               "Правила коммутатора"),
           pts(["Итог: SW-1 копирует кадр в <b>Gi0/2</b> и <b>Gi0/3</b>."], "Что дальше", "lm")],
          topo(t1=[(AA, "Gi0/1", True)], t2=[(AA, "Gi0/2", False)],
               flows=[("A1", 0.2, 1.4), ("g11 g12 g22", 1.6, 1.6), ("g11 g13 g23", 1.8, 1.6)], T=5,
               note="Unknown unicast: две копии кадра уходят на SW-2"))],
    6: [P([pts(["Копии приходят на SW-2 не одновременно. Первая — на Gi0/2: MAC изучен на Gi0/2, кадр скопирован в Gi0/3 и Gi0/1.",
                "Вторая копия приходит на Gi0/3 — тот же MAC уже записан на другом порту."]),
           box("<b>Правило 4.</b> Если MAC уже есть в таблице на другом порту — коммутатор переписывает запись.", "am"),
           pts(["SW-2 <b>переизучает</b> (re-learning) AA:AA:AA:AA:AA:AA на Gi0/3 и снова копирует кадр в Gi0/2 и Gi0/1."], "Итог", "mg")],
          topo(t1=[(AA, "Gi0/1", False)], t2=[(AA, "Gi0/2 -> Gi0/3", True)],
               flows=[("1u", 0, 1.3), ("1d", 0.4, 1.3), ("g22 g21 b", 1.3, 1.3), ("g22 g23 g13", 1.3, 1.6),
                      ("g23 g21 b", 1.7, 1.3), ("g23 g22 g12", 1.7, 1.6)], T=4.5, note="Re-learning: запись в MAC-таблице SW-2 «прыгает»"))],
    7: [P([pts(["SW-1 получает свой же кадр обратно на Gi0/3, переизучает MAC и снова копирует его.",
                "В сети уже <b>4 копии</b> кадра вместо одной.",
                "У кадра Ethernet нет TTL, как у IP-пакета, — копии не исчезают.",
                "Ответ PC-B ждёт та же участь."]),
           box("Цепная реакция: с каждой пересылкой копий больше, пока не занята вся полоса. Это <b>широковещательный шторм</b>.", "mg")],
          topo(t1=[(AA, "Gi0/3 -> Gi0/2 -> …", True)], t2=[(AA, "Gi0/2 -> Gi0/3 -> …", True)],
               flows=[(RING, i * 0.45, 2.6) for i in range(6)] + [("g21 b", 0.8, 1), ("g11 a", 1.8, 1)], T=3,
               note="Шторм: кадры бесконечно ходят по кольцу SW-1 ↔ SW-2"))],
    8: [P(pts(["Агрегация каналов — резервирование линий <b>без петель</b>.",
               "Без агрегации: подуровень MAC получает биты с физического уровня и отдаёт собранные кадры на LLC.",
               "LLC обрабатывает кадры перед передачей на сетевой уровень."]),
          svg(520, 330, bars([(250, 20, 150, 60, "LLC", False), (250, 90, 150, 60, "MAC", False), (250, 175, 150, 60, "PHY", False)])
              + '<rect x="285" y="250" width="80" height="44" fill="none" stroke="#b07a2a" stroke-width="2.5"/>'
                '<text x="230" y="90" text-anchor="end" font-size="20">Канальный уровень</text>'
                '<text x="230" y="225" text-anchor="end" font-size="20">Физический уровень</text>'))],
    9: [P(pts(["Каналы объединяются в группу <b>LAG</b> (Link Aggregation Group) по стандарту <b>802.3ad</b> (семейство Ethernet 802.3).",
               "Объединение — внутри канального уровня, на подуровне <b>LAS</b> (Link Aggregation Sublayer).",
               "Сверху — один LLC, снизу — много пар MAC/PHY (порты Gi0/1 … Gi0/24)."]),
          svg(620, 330, bars([(150, 14, 460, 44, "LLC (MAC Client)", False), (150, 68, 460, 44, "Link Aggregation Sublayer", True)]
                             + [(150 + i * 125, 124, 85, 44, "MAC", False) for i in range(4)]
                             + [(150 + i * 125, 178, 85, 44, "PHY", False) for i in range(4)])
              + "".join('<rect x="%d" y="230" width="65" height="22" fill="none" stroke="#b07a2a" stroke-width="2"/>'
                        '<text x="%d" y="285" text-anchor="middle" font-size="17">%s</text>' % (160 + i * 125, 192 + i * 125, n)
                        for i, n in enumerate(("Gi0/1", "Gi0/2", "Gi0/3", "Gi0/24")))
              + '<text x="520" y="248" font-size="20">…</text><text x="130" y="70" text-anchor="end" font-size="16">Канальный</text>'
                '<text x="130" y="200" text-anchor="end" font-size="16">Физический</text>'))],
    10: [P([pts(["На LAS две подсистемы:", "<b>Distributor</b> — отдаёт кадр с LLC на один из портов группы;",
                 "<b>Collector</b> — собирает кадры с портов группы и передаёт на LLC."]),
            box('<ol class="li"><li>Кадр приходит на логический интерфейс <b>Po1</b>.</li>'
                '<li>Distributor выбирает порт по хешу: MAC, IP или порты TCP/UDP.</li><li>MAC выбранного порта обрабатывает кадр.</li>'
                '<li>PHY передаёт сигнал по кабелю.</li><li>Коммутатор 2 принимает кадр через PHY и MAC.</li>'
                '<li>Collector передаёт кадр выше — как пришедший через <b>Po1</b>.</li></ol>', "am", "Путь кадра по шагам")],
           _las())],
    11: [P([pts(["Ещё один канал без настроек — и трафик размножается вдвое быстрее.",
                 "Решение — <b>link aggregation</b> (не путать с «уровнем агрегации» — distribution layer).",
                 "На SW-1 порты Gi0/2 и Gi0/3 объединяют в группу (channel-group) с виртуальным интерфейсом <b>Port-Channel</b>."]),
            box('<ol class="li"><li>Кадры, полученные на любом порту группы, изучаются на <b>Port-Channel</b>.</li>'
                '<li>Отправляемые кадры копируются в Port-Channel и уходят по любому свободному порту — возможна балансировка.</li></ol>',
                "lm", "Что приказываем коммутатору")],
           topo(po=True, third=True, flows=[("A1", 0.2, 2)], T=4, note="Gi0/2 и Gi0/3 объединены в Po1"))],
    12: [P(pts(["SW-1 изучает MAC PC-A на Gi0/1.", "Свободный порт теперь только один — <b>Port-Channel 1</b>, кадр копируется в него.",
                "Дальше кадр уходит в Gi0/2 или Gi0/3 — какой свободен. Допустим, в Gi0/2."]),
           topo(t1=[(AA, "Po1", True)], po=True, flows=[("A1", 0.2, 1.4), ("g11 g12 g22", 1.6, 1.6)], T=4.5,
                note="Одна копия: кадр уходит только по Gi0/2"))],
    13: [P(pts(["SW-2 получает кадр на физическом Gi0/2, а изучает на <b>Port-Channel 1</b>.",
                "Номера Port-Channel на разных коммутаторах могут не совпадать — здесь для ясности одинаковые.",
                "Кадр уходит в Gi0/1 к PC-B — без лишних копий и без засорения полосы.",
                "Ответ PC-B → PC-A идёт так же, без копий."]),
           [topo(t1=[(AA, "Po1", False)], t2=[(AA, "Po1", True)], po=True, flows=[("1u", 0.2, 1.4), ("2B", 1.6, 1.4)], T=4,
                 note="MAC изучен на Po1 — петли нет"),
            K.term(["MES# show mac-address-table", "", "Vlan     Mac Address       Type     ConnectionId     Ports",
                    "----     -----------       ----     ------------     -----", "1        e0:d9:e3:c2:37:00 Learnt                    [[po 1]]"],
                   "Изучение MAC на Po1")])],
    14: [P([pts(["Пример: 4 кабеля по 1 Гбит/с — после настройки коммутаторы видят одну группу.",
                 "<b>Больше полоса</b>: разные потоки идут одновременно по разным кабелям.",
                 "<b>Резервирование</b>: отказал кабель — трафик идёт по оставшимся.",
                 "<b>Балансировка</b>: коммутатор выбирает кабель по MAC, IP или портам TCP/UDP — поэтому не всегда поровну."]),
            box("4 × 1 Гбит/с = до 4 Гбит/с <b>для нескольких потоков</b>, но один поток ограничен скоростью одного кабеля — <b>1 Гбит/с</b>.", "mg",
                "Важно")],
           _lag(4, flows=[(0, 0, 1.6), (1, 0.6, 1.6), (2, 1.2, 1.6), (3, 1.9, 1.6), (0, 2.2, 1.6)]), t="Агрегация и балансировка")],
    15: [P(pts(["В одну канальную группу — до <b>8</b> физических портов.", "У портов должны совпадать:",
                "1. Скорость;", "2. Дуплекс / полудуплекс;", "3. Режим работы порта (access / trunk и т. д.)."]),
           _lag(8))],
    16: [P([pts(["Статическая агрегация (<b>static LAG</b>): группу включает администратор, соседи никакими сообщениями не обмениваются.",
                 "Удобна, когда в сети оборудование разных производителей с несовместимыми протоколами динамической агрегации."]),
            box("Чтобы параметры портов группы не расходились, сначала сбросьте настройки командой <b>default interface</b>. "
                "Устройство попросит подтвердить сброс.", "am")],
           [K.conf(["MES(config)# default interface Gigabitethernet0/1", "Configuration for these interfaces will be set to default.",
                    "Are you sure you want to proceed? (Y/N)[N] Y"], "Сброс настроек порта"),
            K.conf(["MES(config)# interface Gi0/x", "MES(config-if)# channel-group N mode on"], "Агрегация на Eltex MES"),
            box("<b>N</b> — номер группы каналов, групп может быть до <b>48</b>. Port Channel N переходит в UP, об этом сообщает SysLog:", "cy"),
            K.term(["%TRUNK-I-PORTADDED: Port gi1/0/x added to Po N", "%LINK-I-Up:  Po N"], "SysLog")], stack=True)],
    17: [P([pts(["Интерфейс добавляется в статический LAG без обмена служебными сообщениями.",
                 "Он войдёт в LAG, даже если на другой стороне не член агрегата, а, например, обычный ПК.",
                 "<b>group</b> — номер интерфейса LAG: от 1 до 48."]),
            box("<i>Если на интерфейсе есть настройки режима порта (access, trunk и т. д.), перед добавлением в группу верните настройки по умолчанию.</i>", "mg")],
           [K.conf(["MES2308P(config)# interface gigabitethernet 0/1", "MES2308P(config-if)# channel-group group mode on"], "Добавить порт в LAG"),
            K.conf(["MES2308P(config-if)# no channel-group"], "Удалить порт из группы"),
            K.conf(["MES2308P(config)# interface port-channel group"], "Контекстное меню LAG")],
           t="Статический LAG на MES23xx/33xx/35xx/5324", src=False, stack=True)],
    18: [P([pts(["На MES14xx/24xx LAG сначала включают глобально: <b>set port-channel enable</b>.",
                 "Дальше — так же: channel-group в режиме конфигурации порта.", "<b>group</b> — номер интерфейса LAG: от 1 до 24."]),
            box("<i><b>Если для интерфейса произведены настройки, касающиеся режимов работы портов (access, trunk и т.д), то для добавления его в группу следует "
                "вернуть настройки по умолчанию.</b></i>", "mg")],
           [K.conf(["MES1428(config)#set port-channel enable"], "Включить LAG"),
            K.conf(["MES1428(config)#interface gigabitethernet 0/1", "MES1428(config-if)#channel-group group mode on"], "Добавить порт"),
            K.conf(["MES1428(config-if)# no channel-group"], "Удалить порт"),
            K.conf(["MES1428(config)# interface port-channel group"], "Контекстное меню LAG")],
           t="Статический LAG на MES14xx/24xx", src=False, stack=True)],
    19: [P(K.conf(["MES2308P(config)# default interface Gigabitethernet 0/1", "MES2308P(config)# interface gigabitethernet 0/1",
                   "MES2308P(config-if)# channel-group 1 mode on"], "Пример: MES23xx/33xx/35xx/5324"),
           K.conf(["MES1428(config)# default interface Fastethernet 0/1", "MES1428(config)# set port-channel enable",
                   "MES1428(config)# interface gigabitethernet 0/1", "MES1428(config-if)# channel-group 1 mode on"], "Пример: MES14xx/24xx"),
           t="Статический LAG", src=False, stack=True)],
    20: [P([pts(["Po1 поднят, оба порта — <b>active</b>, тип — <b>static LAG</b>."]),
            box("Так устроена статическая агрегация: порты группы не «общаются» с соседями. Они не могут ни «согласовать» действия, "
                "ни даже выяснить, существует ли агрегированный канал по ту сторону кабеля.", "mg", "Минус статики")],
           K.term(["MES# show interface Port-Channel 1", "", "[[Po1 is up]] (connected)", "  Interface index is 1000",
                   "  Hardware is aggregated ethernet interface(s), MAC address is e0:d9:e3:c2:37:01", "  Interface MTU is 1500",
                   "  Link is up for 0 days, 0 hours, 3 minutes and 19 seconds", "    Link aggregation type is static LAG",
                   "   No. of members in this port-channel: 2 (active 2, minimum required 1)",
                   "      gigabitethernet1/0/2, full-duplex, 100Mbps ([[active]])", "      gigabitethernet1/0/3, full-duplex, 100Mbps ([[active]])"],
                  "Пример на коммутаторах MES"), t="Статическая агрегация каналов", src=False, stack=True)],
    21: [P(pts(["Статический LAG — до 8 линков.", "Отказал один — осталось 7: пропускная способность падает.",
                "Вопрос: как держать в агрегате 8 рабочих каналов постоянно?"]),
           _lag(8, broken=(3,)))],
    22: [P([pts(["<b>LACP</b> (Link Aggregation Control Protocol) — динамическое резервирование каналов без петель, часть IEEE 802.3ad.",
                 "Коммутаторы согласуют агрегат, обмениваясь <b>LACPDU</b> на multicast MAC <b>01:80:C2:01:00:02</b>.",
                 "Такой MAC не бывает источником — он не изучается, кадры не уходят дальше первого порта.",
                 "LACP включают на <b>обеих</b> сторонах: стороны подтверждают, что они в одной группе и готовы передавать данные."]),
            box("8 активных каналов + запасные: при отказе активного включается запасной.", "lm")],
           _lag(8, 4))],
    23: [P([pts(["<b>Активный</b> коммутатор периодически шлёт LACPDU и по ответам решает, работает ли порт.",
                 "В LACPDU отправитель — <b>actor</b>, сосед — <b>partner</b>.",
                 "<b>Пассивный</b> ждёт LACPDU и отвечает, подтверждая готовность.",
                 "Нет ответа — порт в группу не включается.",
                 "Порт в <b>mode on</b> LACPDU не шлёт, поэтому с LACP канал не соберётся."])],
           K.table(["", "Auto/Active", "Passive", "On"], [["<b>Auto/Active</b>", "Да", "Да", "Нет"], ["<b>Passive</b>", "Да", "Нет", "Нет"],
                                                          ["<b>On</b>", "Нет", "Нет", "Да"]]))],
    24: [P(pts(["Активный режим: <b>auto</b> на MES 23xx/33xx/35xx/53xx, <b>active</b> на MES 14xx/24xx.",
                "Пассивный — <b>passive</b> на обеих сериях.", "Команда та же — channel-group, но с режимом active (auto) или passive."]),
           [K.conf(["MES (config-if)# channel-group 1 mode auto"], "Активный режим"),
            K.conf(["MES(config-if)# channel-group 1 mode passive"], "Пассивный режим")], t="Режимы LACP на MES")],
    25: [P([pts(["Три раздела LACPDU: версия LACP, информация об отправителе (Actor), о получателе (Partner).",
                 "Блоки Actor и Partner одинаковы по составу полей.", "В «Флагах» — текущее состояние отправителя."]),
            K.table(["Флаг", "0", "1"], [["LACP Activity", "Passive", "Active"], ["LACP Timeout", "Long: раз в 30 с, отключение через 90 с",
                                                                                  "Short: раз в 1 с, отключение через 3 с"],
                                          ["Aggregation", "индивидуальный канал", "в агрегированном канале"],
                                          ["Synchronization", "не синхронизирован", "синхронизирован"],
                                          ["Collecting", "не получает данные", "может получать"],
                                          ["Distributing", "передача отключена", "передача не отключена"],
                                          ["Defaulted", "настройки пользователя", "значения по умолчанию"],
                                          ["Expired", "LACPDU получено вовремя", "после timeout"]])],
           t="Формат LACPDU", stack=True),
         P(K.term(LACPDU_ACT[:20], "Пример LACPDU от активного к активному коммутатору · Actor"),
           K.term(LACPDU_ACT[20:], "· Partner"), t="Пример LACPDU")],
    26: [P(pts(["Получив LACPDU, коммутатор запоминает флаги из <b>Actor State</b> партнёра.",
                "В ответном LACPDU повторяет их в поле <b>Partner State</b>.",
                "Флаги хранятся до следующего LACPDU — чтобы сравнить текущее состояние с прошлым.",
                "В примере справа — пассивный порт: LACP Activity: Passive."]),
           K.term(LACPDU_PAS, "LACPDU пассивного коммутатора"), t="Actor State и Partner State")],
    27: [P(pts(["<b>Приоритет системы</b> решает, какой коммутатор «главный»: он выбирает, какие порты LAG активны, а какие — standby.",
                "«Победитель» — у кого меньше сумма <b>System Priority + System ID</b>.", "System Priority — от 0 до 65535."]),
           K.term(_hdr(["System Priority", "System ID"]), "Приоритет и ID системы в LACPDU"), t="Настройка LACP · приоритет системы", src=False)],
    28: [P([pts(["<b>value</b> — от 0 до 65535.", "По умолчанию: <b>1</b> на MES23xx/33xx/35xx/5324, <b>32768</b> на MES14xx/24xx."])],
           [K.conf(["MES(config)# lacp system-priority value"], "Приоритет системы (глобально)"),
            K.conf(["MES(config)# no lacp system-priority"], "Вернуть по умолчанию")], t="Настройка LACP · system-priority", src=False)],
    29: [P(pts(["<b>Приоритет порта</b> входит в LACP port id (port priority + port number).",
                "По нему решается, какие порты LAG активны, а какие уходят в standby (8 портов с наименьшим port id — активные).",
                "При равных приоритетах выбирают по номерам: 8 портов с наименьшими номерами — активные."]),
           K.term(_hdr(["Port Priority", "Actor Port:"]), "Приоритет и номер порта в LACPDU"), t="Настройка LACP · приоритет порта", src=False)],
    30: [P([pts(["<b>value</b> — от 0 до 65535, по умолчанию <b>32768</b>.", "Для MES23xx/33xx/35xx/5324 и MES14xx/24xx."])],
           [K.conf(["MES(config)# interface gigabitethernet 0/1", "MES(config-if)# lacp port-priority value"], "Приоритет порта"),
            K.conf(["MES(config-if)# no lacp port-priority"], "Вернуть 32768")], t="Настройка LACP · port-priority", src=False)],
    31: [P([pts(["Таймаут LACP — интервал регулярной отправки LACPDU.", "<b>long</b> — раз в 30 с (по умолчанию), <b>short</b> — раз в 1 с.",
                 "Настройка задаёт, с каким интервалом коммутатор <b>хочет получать</b> LACPDU, — т. е. влияет на отправку у соседа.",
                 "Для MES23xx/33xx/35xx/5324 и MES14xx/24xx."])],
           [K.conf(["MES(config)# interface gigabitethernet 0/1", "MES(config-if)# lacp timeout {long | short}"], "Таймаут LACPDU"),
            K.conf(["MES(config-if)# no lacp timeout"], "Вернуть по умолчанию")], t="Настройка LACP · timeout", src=False)],
    32: [P([pts(["<b>group</b> — номер LAG: от 1 до 48.", "<b>auto</b> — активный режим LACP, <b>passive</b> — пассивный."]),
            box("<i>Если для интерфейса произведены настройки, касающиеся режимов работы портов (access, trunk и т.д), то для добавления его в группу следует "
                "вернуть настройки по умолчанию.</i>", "mg")],
           [K.conf(["MES2308P(config)# interface gigabitethernet 0/1", "MES2308P(config-if)# channel-group group mode auto/passive"], "Добавить порт в LACP"),
            K.conf(["MES2308P(config-if)# no channel-group"], "Удалить порт"),
            K.conf(["MES2308P(config)# interface port-channel group"], "Контекстное меню")], t="Настройка LACP на MES23xx/33xx/35xx/5324", src=False, stack=True)],
    33: [P([pts(["Сначала глобально: <b>set port-channel enable</b>.", "<b>group</b> — номер LAG: от 1 до 24.",
                 "<b>active</b> — активный режим LACP, <b>passive</b> — пассивный."]),
            box("<i>Если для интерфейса произведены настройки, касающиеся режимов работы портов (access, trunk и т.д), то для добавления его в группу следует "
                "вернуть настройки по умолчанию.</i>", "mg")],
           [K.conf(["MES1428(config)# set port-channel enable"], "Включить LAG"),
            K.conf(["MES2308P(config)# interface gigabitethernet 0/1", "MES2308P(config-if)# channel-group group mode active/passive"], "Добавить порт"),
            K.conf(["MES1428(config-if)# no channel-group"], "Удалить порт"),
            K.conf(["MES1428(config)# interface port-channel group"], "Контекстное меню")], t="Настройка LACP на MES14xx/24xx", src=False, stack=True)],
    34: [P(K.conf(["MES2308P(config)# default interface Gigabitethernet 0/1", "MES2308P(config)# interface gigabitethernet 0/1",
                   "MES2308P(config-if)# channel-group 1 mode auto"], "LACP active: MES23xx/33xx/35xx/5324"),
           K.conf(["MES1428(config)# default interface Fastethernet 0/1", "MES1428(config)# set port-channel enable",
                   "MES1428(config)# interface gigabitethernet 0/1", "MES1428(config-if)# channel-group 1 mode active"], "LACP active: MES14xx/24xx"),
           t="Настройка LACP · пример", src=False, stack=True)],
    35: [P(pts(["Членство порта в LAG (статическом и LACP) проверяет <b>show interfaces channel-group group</b>.",
                "<b>group</b> — номер LAG, от 1 до 24.", "Видно балансировку (src-dst-mac-ip) и активные порты."]),
           K.term(["MES2308P# show interfaces channel-group 1", "Load balancing: src-dst-mac-ip", "Gathering information...",
                   "Channel  Ports", "-------  -----", "Po1      [[Active: gi1/0/1]]"]), t="Мониторинг LAG на MES23xx/33xx/35xx/5324", src=False)],
    36: [P(pts(["На MES14xx/24xx членство в LAG (статическом и LACP) — <b>show etherchannel summary</b>.",
                "Флаги: P — в port-channel, H — hot-standby (только LACP), D — down.", "В примере Po1 в работе (U, AU, OU), протокол LACP, порт gi 0/1 (P)."]),
           K.term(["MES1428# show etherchannel summary", "Flags:", "D - down        P - in port-channel", "I - stand-alone H - Hot-standby (LACP only)",
                   "E - ErrDisabled", "U - in-use      d - default port", "R - Layer3", "AD - Admin Down     AU - Admin Up",
                   "OD - Operative Down OU - Operative Up", "Group  Port-channel   Protocol  Ports",
                   "-------------------------------------------------------------------------", "1      [[Po1(U)[AU,OU]]]   LACP      gi 0/1(P)"]),
           t="Мониторинг LAG на MES14xx/24xx", src=False)],
}
