# -*- coding: utf-8 -*-
"""Титул и финал деки «Агрегация каналов — Link Aggregation, LACP». Ответы — по материалу pptx."""
from _sw_lib import slide, head, sc, grow, col, step, task, quiz
import _pt_kit as K
import _pt_fin as F

TITLES = {}


def cover():
    F.cover("Агрегация<br><em>каналов</em>", "Link Aggregation: зачем объединять линии, статический LAG и протокол LACP (802.3ad), режимы "
            "active и passive, приоритеты и таймауты, настройка и мониторинг на коммутаторах Eltex MES.",
            [("LAG", ""), ("LACP", "v"), ("802.3ad", "g"), ("Port-Channel", "y"), ("MES", "r")])


def tail():
    slide("Шпаргалка команд", sc(head("Шпаргалка <em>команд</em>", "Команды MES — как на слайдах."), grow("g2",
        col(step(K.conf(["MES2308P(config)# default interface Gigabitethernet 0/1", "MES2308P(config)# interface gigabitethernet 0/1",
                         "MES2308P(config-if)# channel-group 1 mode on", "MES2308P(config-if)# channel-group 1 mode auto",
                         "MES(config-if)# channel-group 1 mode passive", "MES2308P(config-if)# no channel-group",
                         "MES2308P(config)# interface port-channel 1"], "LAG на MES23xx/33xx/35xx/5324")),
            step(K.conf(["MES1428(config)# set port-channel enable", "MES1428(config-if)# channel-group 1 mode active"], "MES14xx/24xx"))),
        col(step(K.conf(["MES(config)# lacp system-priority 1", "MES(config)# no lacp system-priority", "MES(config-if)# lacp port-priority 100",
                         "MES(config-if)# lacp timeout short", "MES(config-if)# no lacp timeout"], "LACP")),
            step(K.conf(["MES2308P# show interfaces channel-group 1", "MES1428# show etherchannel summary"], "Мониторинг"))))))
    F.tslide("Итоговые задачи · 1", "Числа из лекции.", [
        task("lz1", "Сколько групп каналов на MES23xx/33xx/35xx/5324?", "48", "Номер группы — от 1 до <b>48</b>.", "групп"),
        task("lz2", "Сколько активных каналов в LAG в примере лекции?", "8", "<b>8 активных</b> и резервные.", "каналов"),
        task("lz3", "Приоритет порта LACP по умолчанию?", "32768", "lacp port-priority по умолчанию <b>32768</b>.", "число"),
        task("lz4", "Интервал LACPDU при timeout long, секунд?", "30", "long — каждые <b>30 с</b>; short — каждую секунду.", "секунд")])
    F.tslide("Итоговые задачи · 2", "Режимы и настройки.", [
        task("lz5", "Как называется активный режим LACP на MES23xx?", "auto", "На MES23xx/33xx/35xx/53xx — <b>auto</b>, на MES14xx/24xx — active.", "режим"),
        task("lz6", "Соберётся ли LACP, если обе стороны в passive? (да/нет)", "нет", "Passive–Passive — <b>нет</b>: никто не начинает обмен.", "да / нет"),
        task("lz7", "Режим статического LAG (без LACP)?", "on", "<b>mode on</b>.", "режим"),
        task("lz8", "System Priority по умолчанию на MES23xx/33xx/35xx/5324?", "1", "<b>1</b>; на MES14xx/24xx — 32768.", "число")])
    F.sslide("Тренажёр: соберётся ли агрегат", "Таблица совместимости режимов из лекции.",
             K.sorter("ls1", ["LAG соберётся", "LAG не соберётся"], [("Auto — Auto", 0), ("Auto — Passive", 0), ("On — On", 0),
                                                                     ("Passive — Passive", 1), ("On — Auto", 1), ("On — Passive", 1)],
                      "Разложите пары режимов соседних портов."))
    F.sslide("Тренажёр: статика или LACP", "Свойства статической и динамической агрегации.",
             K.sorter("ls2", ["Статический LAG", "LACP"], [("порты не обмениваются служебными сообщениями", 0), ("mode on", 0),
                                                         ("нельзя проверить агрегат на той стороне кабеля", 0), ("обмен LACPDU", 1),
                                                         ("резервный порт заменит отказавший", 1), ("режимы auto / passive", 1),
                                                         ("приоритеты системы и портов", 1)], "Разложите свойства."))
    slide("Тренажёр CLI: LAG и LACP", sc(head("Тренажёр <em>CLI</em>: LAG и LACP",
        "Соберите агрегат по заданию. «Проверить с соседом» — соберётся ли канал с учётом режима соседа."),
        grow("g", col(K.sim("mes", [5, 6, 7, 8], console="Console · Eltex MES2308P", send="Проверить с соседом")))))
    F.qslide("Тест · 1", "Зачем нужна агрегация.", [
        quiz("Что будет, если просто добавить второй линк между коммутаторами без настроек?", ["скорость удвоится", "образуется петля L2",
                                                                                             "ничего", "линк отключится"], 1,
             "Кадр начнёт ходить по кольцу, MAC-адреса переизучаются."),
        quiz("Как агрегат виден коммутатору?", ["как несколько портов", "как один логический интерфейс Port-Channel", "как VLAN", "как туннель"], 1,
             "Свободный порт для копирования — PortChannel 1."),
        quiz("Какой стандарт описывает LACP?", ["802.1Q", "802.3ad", "802.1D", "802.11"], 1, "IEEE 802.3ad."),
        quiz("Зачем перед добавлением в LAG выполнять default interface?", ["для исключения несовпадения параметров портов", "для ускорения",
                                                                           "для удаления VLAN 1", "не нужно"], 0, "Настройки портов в группе должны совпадать.")])
    F.qslide("Тест · 2", "LACP.", [
        quiz("Что даёт LACP по сравнению со статикой?", ["согласование и резервные порты", "шифрование", "маршрутизацию", "VLAN"], 0,
             "Резервный линк включается после отказа активного."),
        quiz("Кто «решает», какие порты активны?", ["коммутатор с меньшей суммой System Priority + System ID", "с большим MAC", "оба", "сосед всегда"], 0,
             "«Победитель» — меньшая сумма."),
        quiz("Какой timeout отправляет LACPDU раз в секунду?", ["long", "short", "auto", "passive"], 1, "short — 1 с."),
        quiz("Что проверяет show interfaces channel-group?", ["членство портов в LAG", "таблицу MAC", "VLAN", "STP"], 0,
             "Активные порты группы.")])
    F.remember("Главное из лекции.", [
        ("Агрегация", ["Несколько линий — один логический Port-Channel.", "Без агрегации второй линк даёт петлю."], "cy"),
        ("Статика", ["channel-group N mode on; порты не согласуются.", "Перед этим — default interface."], "am")],
        [("LACP 802.3ad", ["MES23xx: auto / passive; MES14xx: active / passive.", "Passive–Passive не собирается; On — только с On.",
                           "System/port priority, timeout long 30 с / short 1 с."], "lm"),
         ("Мониторинг", ["show interfaces channel-group N", "show etherchannel summary (MES14xx/24xx)."], "mg")])
    F.final("Агрегация каналов LACP", ["Масштабируемость и избыточность сети: стек, MLAG и резервирование уровней."])
