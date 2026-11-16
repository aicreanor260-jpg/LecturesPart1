# -*- coding: utf-8 -*-
"""LACP: инфографики автора (папка фото f6) повторены вёрсткой и SVG с анимацией.
Текст сцен и карточек — с инфографик автора; полный текст слайда pptx — под «Текст слайда из лекции»."""
from _pt_man import P
import _pt_kit as K
from _arena import (sw, pc, rack, pill, cable, env, show, mactab, ring, tube, xmark, scene, layout, table, GOLD, NAVY, CAB)

H = "Принципы работы агрегации каналов"
AA = "AA:AA:AA:AA:AA:AA"

# опорные точки топологии PC-A — SW-1 ═ SW-2 — PC-B (холст 1000×400)
PA, S1I, S1C, S1U, S1D = (114, 222), (215, 262), (300, 258), (385, 245), (385, 275)
S2U, S2D, S2C, S2O, PB = (615, 245), (615, 275), (700, 258), (785, 262), (886, 222)


def L(*pts):
    return "M" + " L".join("%d,%d" % p for p in pts)


def topo(up="b", down="y", down_dash=False, po=False, labels=True, extra_top=""):
    g = [cable("M114,222 C165,222 170,262 215,262", "b"), cable("M785,262 C830,262 835,222 886,222", "b"),
         cable(L(S1U, S2U), up), cable(L(S1D, S2D), down, dash=down_dash),
         sw(300, 250, "SW-1"), sw(700, 250, "SW-2"), pc(70, 250, "PC-A"), pc(930, 250, "PC-B")]
    if po:
        g += [ring(395, 260, 78), ring(605, 260, 78)]
    if labels:
        g += [pill(186, 302, "Gi0/1", "n", 13), pill(436, 228, "Gi0/2", "n", 13), pill(436, 304, "Gi0/3", "n", 13),
              pill(564, 228, "Gi0/2", "n", 13), pill(564, 304, "Gi0/3", "n", 13), pill(814, 302, "Gi0/1", "n", 13)]
    return "".join(g) + extra_top


def goals():
    items = [("Почему второй линк — это петля", "Как коммутаторы изучают MAC и почему без агрегации кадр размножается и начинается шторм."),
             ("Как устроена агрегация каналов", "LAG по IEEE 802.3ad: подуровень LAS, Collector и Distributor, Port-Channel."),
             ("Статический LAG и протокол LACP", "Режимы on, active (auto) и passive, приоритеты системы и портов, таймаут LACPDU."),
             ("Настройка и проверка на Eltex MES", "channel-group, interface port-channel, show interfaces channel-group и show etherchannel summary.")]
    g = "".join('<div class="ar-goal step"><b class="ar-n">%d</b><div><h4>%s</h4><p>%s</p></div></div>' % (k, t, d)
                for k, (t, d) in enumerate(items, 1))
    return '<div class="ar"><div class="ar-sub">Агрегация каналов — Link Aggregation</div><div class="ar-goals">%s</div></div>' % g


def s3():
    vl = ('<g transform="translate(415,70)"><rect width="80" height="70" rx="10" fill="#3d6fe0" stroke="%s" stroke-width="3"/>'
          '<text x="40" y="44" text-anchor="middle" fill="#fff" font-weight="900" font-size="17">VLAN 10</text>'
          '<animateTransform attributeName="transform" type="translate" values="415,70;415,62;415,70" dur="2.4s" repeatCount="indefinite"/></g>'
          '<g transform="translate(505,70)"><rect width="80" height="70" rx="10" fill="#8a3fe0" stroke="%s" stroke-width="3"/>'
          '<text x="40" y="44" text-anchor="middle" fill="#fff" font-weight="900" font-size="17">VLAN 20</text>'
          '<animateTransform attributeName="transform" type="translate" values="505,62;505,70;505,62" dur="2.4s" repeatCount="indefinite"/></g>') % (GOLD, GOLD)
    g = topo(down_dash=True) + vl + pill(500, 214, "Основной канал", "w", 14) + pill(500, 320, "Дополнительный канал", "g", 14)
    g += env(L(S1U, S2U), 0, 2, 4) + env(L(S2U, S1U), 2, 2, 4) + show(1, 4, 3.6, pill(500, 360, "?  Что произойдёт при подключении?", "y", 15))
    return P(layout("Один канал передаёт трафик нескольких VLAN.", "Его отказ нарушает связь сразу для нескольких сетей.",
                    scene(1000, 380, g), foot="Добавим второй линк между коммутаторами.",
                    note="Что произойдёт при подключении дополнительного канала?"), t=H, raw=True)


def s4():
    T = 5
    g = topo() + mactab(150, 40, "MAC-таблица SW-1", [(AA, "Gi0/1", 2.0, None, True)], T=T, note="после приёма кадра")
    g += mactab(550, 40, "MAC-таблица SW-2", [], T=T)
    g += env(L(PA, S1I, S1C), 0.3, 1.7, T, label="Кадр A → B")
    return P(layout("Первый кадр от PC-A к PC-B", "Сначала MAC-адреса компьютеров неизвестны обоим коммутаторам.", scene(1000, 380, g),
                    [("PC-A отправляет кадр к PC-B", ""), ("SW-1 запоминает MAC источника на Gi0/1", ""), ("MAC назначения пока неизвестен", "")],
                    foot="Динамические MAC-записи удаляются по таймеру старения, если не обновляются."), t=H, raw=True)


def s5():
    T = 6
    g = topo() + mactab(150, 40, "MAC-таблица SW-1", [(AA, "Gi0/1", 1.6, None, False)], T=T)
    g += mactab(550, 40, "MAC-таблица SW-2", [(AA, "Gi0/2", 3.5, None, True)], T=T, note="Первая копия пришла на Gi0/2")
    g += env(L(PA, S1I, S1C), 0.2, 1.4, T) + env(L(S1C, S1U, S2U, S2C), 1.7, 1.8, T) + env(L(S1C, S1D, S2D, S2C), 2.0, 1.9, T)
    return P(layout("Неизвестный MAC назначения — unknown unicast", "Учебный пример: агрегация не настроена, STP отключён.", scene(1000, 380, g),
                    [("Изучение источника", "SW-1: MAC A → Gi0/1"), ("Поиск назначения", "MAC B отсутствует в таблице"),
                     ("Рассылка копий", "SW-1 отправляет кадр в Gi0/2 и Gi0/3")],
                    foot="Unknown unicast: кадр копируется на остальные порты той же VLAN, разрешённые для передачи.",
                    note="Источник: MAC A • Назначение: MAC B"), t=H, raw=True)


def s6():
    T = 7
    g = topo() + mactab(550, 40, "MAC-таблица SW-2", [(AA, "Gi0/2", 1.5, 2.7, False), (AA, "Gi0/3", 2.7, None, True)], T=T)
    g += env(L(S1C, S1U, S2U, S2C), 0, 1.5, T) + env(L(S1C, S1D, S2D, S2C), 1.0, 1.7, T)
    g += env(L(S2C, S2O, PB), 1.5, 1.4, T) + env(L(S2C, S2D, S1D, S1C), 1.5, 1.7, T)
    g += env(L(S2C, S2O, PB), 2.7, 1.4, T) + env(L(S2C, S2U, S1U, S1C), 2.7, 1.7, T)
    g += show(4.1, T, None, pill(905, 140, "Дубликат!", "r", 15))
    g += show(1.5, T, 2.7, pill(330, 100, "1. Изучает MAC A на Gi0/2", "w", 15)) + show(2.7, T, None, pill(330, 100, "2. Переписывает: Gi0/2 → Gi0/3", "y", 15))
    return P(layout("Переизучение MAC-адреса на SW-2", "Агрегация не настроена. STP отключён. MAC назначения неизвестен.", scene(1000, 380, g),
                    [("Первая копия приходит на Gi0/2", "Изучает MAC A на Gi0/2. Копии → Gi0/3 и Gi0/1."),
                     ("Вторая копия приходит на Gi0/3", "Переписывает запись: Gi0/2 → Gi0/3. Копии → Gi0/2 и Gi0/1.")],
                    foot="Один MAC появляется на разных портах — запись переизучается. PC-B получает дубликаты кадров."), t=H, raw=True)


def s7():
    T = 3.2
    ringp = L(S1C, S1U, S2U, S2C, S2D, S1D, S1C)
    g = topo() + mactab(150, 40, "MAC-таблица SW-1", [(AA, "Gi0/3", None, None, True)], T=T, note="→ Gi0/1 → Gi0/3 → …")
    g += ('<path d="M430,205 C470,170 530,170 570,205" fill="none" stroke="#c48bff" stroke-width="6" filter="url(#glw)"/>'
          '<path d="M570,320 C530,355 470,355 430,320" fill="none" stroke="#c48bff" stroke-width="6" filter="url(#glw)"/>')
    g += pill(500, 368, "Копии одного кадра", "p", 15) + pill(800, 90, "⚠ Кадры возвращаются по второму линку", "y", 14)
    g += "".join(env(ringp, i * 0.53, 3.0, T) for i in range(6)) + env(L(S1C, S1I, PA), 0.6, 1, T) + env(L(S2C, S2O, PB), 1.6, 1, T)
    g += ('<g transform="translate(560,40)"><text x="0" y="-6" font-size="13" font-weight="800" fill="#fff">Каналы перегружены</text>'
          '<rect width="240" height="18" rx="6" fill="#13286b" stroke="%s" stroke-width="2"/><rect x="2" y="2" height="14" rx="5" fill="#ff4d4d">'
          '<animate attributeName="width" values="20;236;236" keyTimes="0;.8;1" dur="%ss" repeatCount="indefinite"/></rect></g>' % (GOLD, T * 2))
    return P(layout("Возврат кадра на SW-1: петля и шторм трафика", "⚠ Агрегация не настроена. STP отключён.", scene(1000, 400, g),
                    [("Кадр вернулся на Gi0/3", "SW-1 переизучает MAC A"), ("SW-1 копирует кадр", "В Gi0/2 и Gi0/1"),
                     ("Циркуляция продолжается", "Дубликаты и перегрузка каналов")],
                    foot="В Ethernet нет TTL: петля не прекращается сама.", note="Повторная рассылка кадров создаёт шторм трафика."), t=H, raw=True)


def _layer(x, y, w, h, text, fill, sub=""):
    s = ('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" stroke="%s" stroke-width="3"/>'
         '<text x="%d" y="%d" text-anchor="middle" fill="#fff" font-weight="900" font-size="%d">%s</text>'
         % (x, y, w, h, fill, GOLD, x + w // 2, y + h // 2 + (0 if sub else 7), 20 if w > 200 else 18, text))
    if sub:
        s += '<text x="%d" y="%d" text-anchor="middle" fill="#ead9ff" font-weight="700" font-size="13">%s</text>' % (x + w // 2, y + h // 2 + 18, sub)
    return s


def s8():
    T = 4
    left = ('<rect x="10" y="10" width="440" height="370" rx="16" fill="#0b2a44" fill-opacity=".35" stroke="%s" stroke-width="2"/>' % GOLD
            + pill(230, 44, "С агрегацией", "n", 18) + sw(95, 210, "SW-1", 140, 4) + sw(365, 210, "SW-2", 140, 4)
            + cable("M165,210 L295,210", "b", 6) + cable("M165,226 L295,226", "b", 6) + tube(160, 300, 218, 54, "Один логический канал")
            + pill(230, 345, "✔ Резервирование без петли между участниками группы", "g", 13))
    stack = ('<rect x="480" y="10" width="510" height="370" rx="16" fill="#fff7df" stroke="%s" stroke-width="2"/>' % GOLD
             + pill(735, 44, "Приём кадра без агрегации", "p", 17)
             + '<text x="735" y="86" text-anchor="middle" font-weight="800" font-size="14" fill="#13286b">К сетевому уровню ▲</text>'
             + _layer(670, 96, 130, 52, "LLC", "#6a35c9") + _layer(670, 168, 130, 52, "MAC", "#2f5fd0") + _layer(670, 240, 130, 52, "PHY", "#159ab0")
             + '<rect x="715" y="306" width="40" height="34" fill="#c9962e" stroke="#7a5310" stroke-width="2"/>'
             + '<text x="600" y="140" text-anchor="end" font-weight="900" font-size="15" fill="#13286b">Канальный</text>'
               '<text x="600" y="158" text-anchor="end" font-weight="900" font-size="15" fill="#13286b">уровень</text>'
               '<text x="600" y="268" text-anchor="end" font-weight="900" font-size="15" fill="#13286b">Физический</text>'
               '<text x="600" y="286" text-anchor="end" font-weight="900" font-size="15" fill="#13286b">уровень</text>'
             + "".join('<text x="815" y="%d" font-size="13" font-weight="700" fill="#3a2a10">%s</text>' % (y, t) for y, t in
                       ((118, "Передаёт данные"), (134, "вышележащему протоколу."), (190, "Принимает и проверяет"), (206, "Ethernet-кадр."),
                        (262, "Принимает"), (278, "физические сигналы.")))
             + '<text x="690" y="365" font-family="monospace" font-weight="900" fill="#2f5fd0" font-size="15">0 1 0 1 1<animate attributeName="opacity" '
               'values="1;.2;1" dur="1s" repeatCount="indefinite"/></text>'
             + env("M735,360 L735,268 L735,196 L735,122 L735,80", 0.2, 3.2, T))
    return P(layout("Агрегация каналов — IEEE 802.3ad", "Несколько физических каналов объединяются в один логический интерфейс.",
                    scene(1000, 390, left + stack), foot="Без агрегации: PHY → MAC → LLC",
                    note="Упрощённая схема обработки принятого кадра. Исторически IEEE 802.3ad; современный стандарт — IEEE 802.1AX."), t=H, raw=True)


def s9():
    T = 3
    g = [_layer(200, 14, 600, 54, "LLC (MAC Client)", "#2449b8"),
         '<rect x="200" y="84" width="600" height="64" rx="12" fill="#6a35c9" stroke="#d3a6ff" stroke-width="3" filter="url(#glw)">'
         '<animate attributeName="stroke-opacity" values="1;.4;1" dur="1.8s" repeatCount="indefinite"/></rect>'
         '<text x="500" y="112" text-anchor="middle" fill="#fff" font-weight="900" font-size="20">LAS — Link Aggregation Sublayer</text>'
         '<text x="500" y="134" text-anchor="middle" fill="#ead9ff" font-weight="700" font-size="14">Подуровень агрегации каналов</text>']
    for i in range(4):
        x = 215 + i * 150
        g += [_layer(x, 172, 120, 44, "MAC", "#2f5fd0"), _layer(x, 228, 120, 44, "PHY", "#159ab0"),
              '<rect x="%d" y="284" width="56" height="40" rx="4" fill="#c9962e" stroke="#7a5310" stroke-width="2"/>' % (x + 32),
              pill(x + 60, 352, "Gi0/%d" % (i + 1), "n", 14),
              env("M%d,300 L%d,250 L%d,194 L%d,116 L500,42" % (x + 60, x + 60, x + 60, x + 60), i * 0.6, 2.1, T)]
    g += ['<text x="185" y="80" text-anchor="end" font-weight="900" font-size="15" fill="#fff">Канальный</text>'
          '<text x="185" y="98" text-anchor="end" font-weight="900" font-size="15" fill="#fff">уровень OSI</text>'
          '<text x="185" y="248" text-anchor="end" font-weight="900" font-size="15" fill="#fff">Физический</text>'
          '<text x="185" y="266" text-anchor="end" font-weight="900" font-size="15" fill="#fff">уровень OSI</text>',
          pill(900, 112, "Объединяет MAC", "y", 14), pill(900, 140, "нескольких портов", "y", 14),
          pill(900, 300, "4 физических порта →", "g", 13), pill(900, 326, "1 логический интерфейс", "g", 13)]
    return P(layout("Агрегация каналов — IEEE 802.3ad", "LAG (Link Aggregation Group) — группа физических каналов, работающих как один логический интерфейс.",
                    scene(1000, 372, "".join(g)), foot="Объединение выполняется на канальном уровне, между MAC и LLC.",
                    note="IEEE 802.3ad — исходный стандарт; дальнейшее развитие — IEEE 802.1AX."), t=H, raw=True)


def s10():
    T = 8
    g = []
    for sx, nm in ((20, "Коммутатор 1"), (520, "Коммутатор 2")):
        g += ['<rect x="%d" y="6" width="460" height="300" rx="16" fill="#0b2a44" fill-opacity=".35" stroke="%s" stroke-width="2"/>' % (sx, GOLD),
              pill(sx + 230, 30, nm, "n", 15), _layer(sx + 30, 44, 400, 40, "LLC (MAC Client) — Po1", "#2449b8"),
              '<rect x="%d" y="94" width="420" height="78" rx="12" fill="#6a35c9" fill-opacity=".35" stroke="#d3a6ff" stroke-width="2.4" stroke-dasharray="8 5"/>' % (sx + 20),
              '<text x="%d" y="112" text-anchor="middle" fill="#ead9ff" font-weight="900" font-size="15">LAS</text>' % (sx + 230),
              _layer(sx + 40, 120, 150, 40, "Collector", "#6a35c9"), _layer(sx + 270, 120, 150, 40, "Distributor", "#6a35c9")]
        for i in range(3):
            x = sx + 50 + i * 140
            g += [_layer(x, 186, 90, 34, "MAC", "#2f5fd0"), _layer(x, 228, 90, 34, "PHY", "#159ab0"),
                  '<rect x="%d" y="270" width="40" height="26" rx="3" fill="#c9962e" stroke="#7a5310" stroke-width="2"/>' % (x + 25),
                  '<text x="%d" y="320" text-anchor="middle" font-weight="800" font-size="13" fill="#fff">Порт %d</text>' % (x + 45, i + 1)]
    for i, c in enumerate(("r", "b", "g")):
        x1, x2, yb = 115 + i * 140, 615 + i * 140, 340 + i * 14
        g.append(cable("M%d,296 V%d H%d V296" % (x1, yb, x2), c, 5, flow=False))
    path = "M380,64 L345,140 L255,203 L255,245 L255,340 L755,340 L755,245 L755,203 L635,140 L650,64"
    g.append(env(path, 0.3, 6.6, T))
    for x, y, n in ((330, 64, 1), (430, 140, 2), (305, 203, 3), (305, 245, 4), (805, 245, 5), (700, 140, 6)):
        g.append('<circle cx="%d" cy="%d" r="13" fill="#ffd43b" stroke="#8a5a10" stroke-width="2"/><text x="%d" y="%d" text-anchor="middle" '
                 'font-weight="900" font-size="15" fill="#13286b">%d</text>' % (x, y, x, y + 5, n))
    g += [pill(250, 380, "Выбор по хешу: MAC / IP / TCP, UDP", "y", 13), pill(760, 380, "Сбор кадров с портов группы", "y", 13)]
    return P(layout("LAS: Collector и Distributor", "", scene(1000, 396, "".join(g)),
                    [("Кадр поступает в Po1", ""), ("Distributor выбирает порт", ""), ("Кадр передаётся в MAC", ""),
                     ("PHY отправляет сигнал", ""), ("PHY и MAC принимают кадр", ""), ("Collector передаёт кадр в LLC", "")],
                    foot="Один кадр передаётся целиком через один физический канал."), t=H, raw=True)


def s11():
    T = 5
    g = topo(po=True, labels=False) + tube(410, 590, 260, 76, "Один логический канал")
    g += pill(250, 120, "Gi0/2 + Gi0/3 → Po1", "w", 15) + pill(760, 120, "✔ Общий интерфейс для коммутации", "g", 15)
    g += pill(186, 302, "Gi0/1", "n", 13) + pill(814, 302, "Gi0/1", "n", 13)
    g += env(L(PA, S1I, S1C), 0.2, 1.3, T) + env(L(S1C, S1U, S2U, S2C), 1.5, 1.6, T) + env(L(S2C, S2O, PB), 3.1, 1.3, T)
    return P(layout("Link Aggregation: несколько портов — один интерфейс", "Объединяем Gi0/2 и Gi0/3 в группу и создаём Port-Channel 1.",
                    scene(1000, 360, g),
                    [("Приём и обучение", "Кадр пришёл через участник LAG — MAC источника изучается за Po1. На принимающем SW-2: MAC A → Po1."),
                     ("Передача и балансировка", "Кадр направляется в Po1. Алгоритм выбирает один физический порт. Выбор обычно по хешу потока.")],
                    foot="Два физических соединения работают как один логический канал — без петли внутри LAG.",
                    note="Настройка согласуется на обоих концах. Один кадр не копируется на все участники группы."), t=H, raw=True)


def s12():
    T = 5
    g = topo(po=True) + mactab(150, 40, "MAC-таблица SW-1", [(AA, "Gi0/1", 1.4, None, False)], T=T)
    g += show(3.2, T, None, '<g transform="translate(560,40)"><rect width="250" height="72" rx="10" fill="#2a1466" stroke="%s" stroke-width="2.6"/>'
                            '<text x="125" y="24" text-anchor="middle" fill="#fff" font-weight="900" font-size="15">После приёма на SW-2:</text>'
                            '<text x="125" y="46" text-anchor="middle" fill="#ffd43b" font-weight="900" font-size="15">MAC A → Po1</text>'
                            '<text x="125" y="64" text-anchor="middle" fill="#ead9ff" font-weight="700" font-size="12">MAC назначения пока неизвестен</text></g>' % GOLD)
    g += pill(500, 205, "Выбран Gi0/2", "y", 14) + pill(500, 330, "Gi0/3 — участник Po1", "p", 13)
    g += env(L(PA, S1I, S1C), 0.2, 1.2, T) + env(L(S1C, S1U, S2U, S2C), 1.5, 1.7, T)
    return P(layout("Передача кадра через Port-Channel 1", "Gi0/2 и Gi0/3 объединены в Po1 на обоих коммутаторах", scene(1000, 360, g),
                    [("SW-1 изучает MAC A", "Входной порт — Gi0/1"), ("Кадр направляется в Po1", "Для коммутации это один интерфейс"),
                     ("Выбирается участник группы", "В примере кадр уходит через Gi0/2")],
                    foot="Физический порт обычно выбирается по хешу потока, а не по текущей занятости.",
                    note="Один кадр — один физический канал. Копии по обоим линкам не отправляются."), t=H, raw=True)


def s13():
    T = 5
    g = topo(po=True) + mactab(150, 40, "MAC-таблица SW-1", [("MAC A", "Gi0/1", None, None, False)], T=T)
    g += mactab(550, 40, "MAC-таблица SW-2", [("MAC A", "Po1", 1.8, None, True)], T=T)
    g += show(1.8, T, None, pill(700, 350, "MAC источника изучается за Po1", "g", 13))
    g += env(L(S1C, S1U, S2U, S2C), 0.2, 1.6, T) + env(L(S2C, S2O, PB), 2.0, 1.4, T)
    return [P(layout("Приём кадра на SW-2 через Port-Channel 1", "Физический вход — Gi0/2. Логический вход для коммутации — Po1.",
                     scene(1000, 370, g), [("Приём на Gi0/2", "Кадр поступает в Po1"), ("Обучение MAC", "SW-2: MAC A → Po1"),
                                           ("Передача к PC-B", "Выход — Gi0/1")],
                     foot="Кадр не возвращается в тот же Po1 через Gi0/3 — петля не возникает.",
                     note="В этой схеме Gi0/1 — единственный другой порт нужной VLAN. Номера Port-Channel на разных коммутаторах могут отличаться."),
              t=H, raw=True, src=False),
            P(layout("Пример изучения MAC-адресов на интерфейсе Po1", "От PC-B к PC-A кадр будет передан в обратном порядке без создания излишних копий.",
                     extra=K.term(["MES# show mac-address-table", "", "Vlan     Mac Address       Type     ConnectionId     Ports",
                                   "----     -----------       ----     ------------     -----",
                                   "1        e0:d9:e3:c2:37:00 Learnt                    [[po 1]]"], "show mac-address-table")), t=H, raw=True)]


def _bundle(n_act, n_sb=0, fail=None, T=6, x1=330, x2=670, y0=150, gap=22, phase=None):
    """Пучок каналов между двумя широкими коммутаторами (слева и справа)."""
    g = []
    n = n_act + n_sb
    for i in range(n):
        y = y0 + i * gap
        sb = i >= n_act
        g.append(cable("M%d,%d L%d,%d" % (x1, y, x2, y), "w" if sb else "b", 6, flow=not sb, dash=sb, op=.8 if sb else 1))
        if sb and phase:     # резерв загорается после отказа
            g.append(show(phase, T, None, cable("M%d,%d L%d,%d" % (x1, y, x2, y), "y", 7)))
        if fail is not None and i == fail:
            g.append(show(phase - 1.6 if phase else 0, T, None, cable("M%d,%d L%d,%d" % (x1, y, x2, y), "r", 7, flow=False)
                          + xmark((x1 + x2) // 2, y, s=11)))
    return "".join(g)


def _side_racks(y0, n, gap):
    h = n * gap + 40
    return "".join('<g><rect x="%d" y="%d" width="120" height="%d" rx="12" fill="#1f3f9c" stroke="%s" stroke-width="3"/>'
                   '<rect x="%d" y="%d" width="120" height="16" rx="6" fill="#4d86ee" stroke="%s" stroke-width="2"/>'
                   '<text x="%d" y="%d" text-anchor="middle" fill="#fff" font-weight="900" font-size="18" transform="rotate(-90 %d %d)">%s</text>%s</g>'
                   % (x, y0 - 30, h, GOLD, x, y0 - 30, GOLD, x + 60, y0 - 30 + h // 2, x + 60, y0 - 30 + h // 2, nm,
                      "".join('<circle cx="%d" cy="%d" r="5" fill="#5dff7a"/>' % (x + (112 if x < 500 else 8), y0 + i * gap) for i in range(n)))
                   for x, nm in ((210, "SW-1"), (670, "SW-2")))


def s14():
    T = 4
    g = _side_racks(150, 4, 44) + "".join(cable("M330,%d L670,%d" % (150 + i * 44, 150 + i * 44), "b", 7) for i in range(4))
    g += "".join(env("M335,%d L665,%d" % (150 + i * 44, 150 + i * 44), t0, 1.6, T) for i, t0 in ((0, 0), (1, .6), (2, 1.2), (3, 1.9), (0, 2.3)))
    g += pill(500, 90, "4 × 1 Гбит/с = до 4 Гбит/с для нескольких потоков", "y", 15)
    return P(layout("Агрегация и балансировка", "Например, между двумя коммутаторами подключены четыре кабеля по 1 Гбит/с.", scene(1000, 360, g),
                    [("Больше полосы", "Несколько потоков идут одновременно через разные кабели."),
                     ("Резервирование", "При отказе одного соединения трафик идёт через оставшиеся."),
                     ("Балансировка", "Выбор кабеля по MAC, IP или TCP/UDP-портам — нагрузка не обязательно поровну.")],
                    foot="Один поток обычно ограничен скоростью одного соединения — 1 Гбит/с.",
                    note="Агрегация создаёт общую группу соединений, а балансировка распределяет трафик между её участниками. Способы на Eltex зависят от модели."),
             t="Агрегация каналов", raw=True)


def s15():
    g = _side_racks(110, 8, 26) + "".join(cable("M330,%d L670,%d" % (110 + i * 26, 110 + i * 26), "b", 6) for i in range(8))
    g += ('<rect x="350" y="92" width="300" height="218" rx="18" fill="none" stroke="#c48bff" stroke-width="4" filter="url(#glw)">'
          '<animate attributeName="stroke-opacity" values="1;.4;1" dur="1.8s" repeatCount="indefinite"/></rect>')
    g += pill(500, 74, "Одна группа LAG / Po1", "p", 15) + pill(500, 336, "Пример: 8 физических портов", "y", 14)
    g += '<text x="500" y="366" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">Максимум участников зависит от модели и ПО.</text>'
    return P(layout("Статическая агрегация каналов", "Порты объединяются вручную на обоих устройствах, без согласования по LACP.", scene(1000, 376, g),
                    [("Одинаковая скорость", "Например, все порты — 1 Гбит/с."), ("Полный дуплекс", "Все участники работают в Full Duplex."),
                     ("Одинаковый режим", "Access или trunk; согласованные параметры VLAN.")],
                    foot="Согласуйте состав группы и настройки портов на обоих концах."), t=H, raw=True)


def s21():
    T = 7
    g = _side_racks(110, 9, 26) + _bundle(8, 1, fail=3, T=T, y0=110, gap=26, phase=4.4)
    g += show(0, T, 2.8, pill(500, 70, "8 активных + 1 резервный", "w", 17)) + show(2.8, T, 4.4, pill(500, 70, "7 активных", "r", 17))
    g += show(4.4, T, None, pill(500, 70, "Снова 8 активных", "g", 17))
    return P(layout("Динамическая агрегация каналов — LACP", "Статический LAG: отказал один канал — работают 7. LACP включает резерв.",
                    scene(1000, 360, g), [("До отказа", "8 активных + 1 резервный"), ("Отказ одного линка", "7 активных"),
                                          ("Включение резерва", "Снова 8 активных")],
                    foot="LACP согласует участие портов в группе агрегации. Чтобы восстановить 8 активных каналов после отказа, нужен дополнительный резервный линк.",
                    note="Число активных и резервных портов зависит от модели коммутатора. Переключение требует времени."), t=H, raw=True)


def s22():
    def mini(cx, act, red, gold, big, small, tone):
        g = ['<rect x="%d" y="40" width="290" height="320" rx="16" fill="#fff7df" stroke="%s" stroke-width="3"/>' % (cx - 145, GOLD),
             '<text x="%d" y="96" text-anchor="middle" font-weight="900" font-size="46" fill="%s">%s</text>' % (cx - 40, tone, big),
             '<text x="%d" y="88" font-weight="900" font-size="17" fill="#13286b">%s</text>' % (cx - 10, small)]
        g.append('<rect x="%d" y="130" width="26" height="200" rx="6" fill="#1f3f9c" stroke="%s" stroke-width="2"/>'
                 '<rect x="%d" y="130" width="26" height="200" rx="6" fill="#1f3f9c" stroke="%s" stroke-width="2"/>' % (cx - 120, GOLD, cx + 94, GOLD))
        for i in range(9):
            y = 146 + i * 21
            c = "y" if (i == 8 and gold) else ("r" if (red and i == 3) else ("w" if i == 8 else "b"))
            g.append(cable("M%d,%d L%d,%d" % (cx - 94, y, cx + 94, y), c, 5, flow=(c in "by"), dash=(c == "w")))
            if red and i == 3:
                g.append(xmark(cx, y, s=8))
        return "".join(g)
    g = (mini(165, 8, False, False, "8", "активных +1 резервный", "#2449b8") + mini(500, 7, True, False, "7", "активных", "#e03131")
         + mini(835, 8, True, True, "8", "снова активных", "#2449b8")
         + '<text x="332" y="210" text-anchor="middle" font-size="40" fill="#ffd43b">➜</text><text x="668" y="210" text-anchor="middle" font-size="40" fill="#ffd43b">➜</text>')
    return P(layout("Динамическая агрегация каналов. Протокол LACP", "LACPDU отправляются на multicast MAC 01:80:C2:01:00:02; LACP включается на обеих сторонах канала.",
                    scene(1000, 370, g), [("До отказа", "8 активных + 1 резервный"), ("Отказ одного канала", "7 активных"),
                                          ("Активация резерва", "Снова 8 активных")],
                    foot="LACP позволяет задействовать резервный линк после отказа активного.",
                    note="Лимит 8 активных каналов — пример: возможности зависят от модели. Переключение занимает время."), t=H, raw=True)


def s23():
    T = 4
    g = ('<g transform="translate(40,40)"><rect width="230" height="110" rx="14" fill="#fff7df" stroke="%s" stroke-width="3"/>'
         '<rect x="35" y="-16" width="160" height="40" rx="10" fill="#2449b8" stroke="%s" stroke-width="3"/>'
         '<text x="115" y="12" text-anchor="middle" fill="#fff" font-weight="900" font-size="20">ACTIVE</text>'
         '<text x="115" y="60" text-anchor="middle" font-weight="800" font-size="16" fill="#13286b">Инициирует</text>'
         '<text x="115" y="82" text-anchor="middle" font-weight="800" font-size="16" fill="#13286b">обмен LACPDU</text></g>'
         '<g transform="translate(730,40)"><rect width="230" height="110" rx="14" fill="#fff7df" stroke="%s" stroke-width="3"/>'
         '<rect x="35" y="-16" width="160" height="40" rx="10" fill="#6a35c9" stroke="%s" stroke-width="3"/>'
         '<text x="115" y="12" text-anchor="middle" fill="#fff" font-weight="900" font-size="20">PASSIVE</text>'
         '<text x="115" y="60" text-anchor="middle" font-weight="800" font-size="16" fill="#13286b">Ожидает LACPDU</text>'
         '<text x="115" y="82" text-anchor="middle" font-weight="800" font-size="16" fill="#13286b">и отвечает</text></g>') % (GOLD, GOLD, GOLD, GOLD)
    g += sw(300, 120, "Active", 150, 4) + sw(700, 120, "Passive", 150, 4)
    g += cable("M380,98 L620,98", "b", 6, flow=False) + cable("M620,140 L380,140", "p", 6, flow=False)
    g += env("M385,98 L615,98", 0.1, 1.6, T, label="LACPDU") + env("M615,140 L385,140", 2.0, 1.6, T, label="LACPDU")
    return P(layout("Протокол LACP: Active и Passive", "Actor — отправитель LACPDU. Partner — его сосед. Важно: actor не обязательно означает active, "
                                                       "а partner не обязательно означает passive.",
                    extra='<div class="ar-two">' + scene(1000, 210, g) + '<div>' + table(["Режимы портов", "Результат"], [["Active + Active", "LACP работает"], ["Active + Passive", "LACP работает"],
                                                                ["Passive + Passive", "Обмен не начинается"], ["LACP + On", "LACP не согласуется"]],
                                [True, True, False, False]) + '</div></div>',
                    foot="On + On — статический LAG без LACP.",
                    note="Успешное объединение также требует совместимых настроек портов. При потере LACPDU порт исключается после тайм-аута."),
             t="Динамическая агрегация каналов", raw=True)


AR = {2: [P(goals(), t="Цели лекции", raw=True, src=False)], 3: [s3()], 4: [s4()], 5: [s5()], 6: [s6()], 7: [s7()], 8: [s8()], 9: [s9()],
      10: [s10()], 11: [s11()], 12: [s12()], 13: s13(), 14: [s14()], 15: [s15()], 21: [s21()], 22: [s22()], 23: [s23()]}
