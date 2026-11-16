# -*- coding: utf-8 -*-
"""Титул и финал деки «Мониторинг и управление»: шпаргалка → задачи → тренажёры → тренажёр CLI (ESR) → тест → итоги → финал.
Все ответы — по материалу pptx."""
from _sw_lib import slide, head, sc, grow, col, card, li, step, task, quiz, p, tags, tag
import _pt_kit as K


def cover():
    slide("Титул", sc(
        '<div class="cover"><div class="big">Мониторинг<br>и <em>управление</em></div>'
        '<div class="lead">LLDP, зеркалирование SPAN и RSPAN, системный журнал Syslog, Eltex IP SLA, резервное копирование '
        'конфигурации на маршрутизаторах ESR.</div>%s'
        '<div class="lead" style="font-size:clamp(12px,.95vw,17px)">← → шаги · ↑ ↓ слайды · Esc — содержание</div></div>'
        % tags(tag("LLDP"), tag("SPAN", "v"), tag("Syslog", "g"), tag("IP SLA", "y"), tag("archive", "r"))), cover=True)


def _q(title, sub, qs):
    slide(title, sc(head(title.replace("Тест", "<em>Тест</em>"), sub), grow("g2", col(*qs[:2]), col(*qs[2:])),
                    '<div class="foot" style="margin-top:8px"><i>✓</i><span>Результат по всем вопросам: '
                    '<span class="score">0 / 0</span></span></div>'))


def _t(title, sub, items):
    slide(title, sc(head(title.replace("задачи", "<em>задачи</em>"), sub), grow("g2", col(*items[:2]), col(*items[2:]))))


def _s(title, sub, box):
    slide(title, sc(head(title.replace("Тренажёр", "<em>Тренажёр</em>"), sub), grow("g", col(box))))


def tail():
    slide("Шпаргалка команд", sc(head("Шпаргалка <em>команд</em>", "Команды лекции — в том же синтаксисе, что на слайдах."), grow("g2",
        col(step(K.conf(["MES(config)# lldp run", "ESR(config)# lldp enable", "ESR(config-if)#lldp receive", "ESR(config-if)#lldp transmit",
                         "Switch(config)# lldp timer 30", "Switch(config)# lldp hold-multiplier 4",
                         "Switch(config-if)# lldp optional-tlv sys-name sys-desc sys-cap"], "LLDP")),
            step(K.conf(["R1(config-if-gi)# port monitor interface gigabitethernet 1/0/1", "R1(config)# port monitor mode monitor-only",
                         "R1(config)# port monitor remote vlan 14", "R1(config-if-gi)# port monitor remote"], "Зеркалирование")),
            step(K.conf(["esr(config)# archive", "esr(config-archive)# type both",
                         "esr(config-archive)# path tftp://203.0.113.254:/esrexample/esr-example.cfg",
                         "esr(config-archive)# count-backup 30", "esr(config-archive)# time-period 1440", "esr(config-archive)# auto",
                         "esr(config-archive)# by-commit"], "Резервное копирование"))),
        col(step(K.conf(["esr(config)# syslog file flash:syslog/ESR", "esr(config-syslog-file)# severity info", "esr(config)# syslog host SERVER",
                         "esr(config-syslog-host)# source-address 192.0.2.1", "esr(config-syslog-host)# remote-address 192.0.2.254",
                         "esr(config-syslog-host)# transport udp", "esr(config-syslog-host)# port 514", "esr(config)# logging login on-failure",
                         "esr# show syslog configuration"], "Syslog")),
            step(K.conf(["SENDER(config)# ip sla test 1",
                         "SENDER(config-sla-test)# udp-jitter 203.0.113.1 20001 source-ip 198.51.100.1 num-packets 100 interval 20",
                         "SENDER(config-sla-test)# frequency 25", "SENDER(config-sla-test)# enable",
                         "SENDER(config)# ip sla schedule 1 life forever start-time now", "SENDER(config)# ip sla",
                         "RESPONDER(config-if-gi)# ip sla responder eltex", "esr# show ip sla test statistics 1"], "IP SLA"))))))

    _t("Итоговые задачи · 1", "LLDP и Syslog.", [
        task("mz1", "Интервал отправки LLDPDU по умолчанию на коммутаторах Eltex, секунд?", "30", "LLDPDU — раз в <b>30 секунд</b>.", "секунд"),
        task("mz2", "Hold multiplier по умолчанию (сколько интервалов)?", "4", "<b>4</b> интервала = 120 секунд.", "число"),
        task("mz3", "Порт и протокол Syslog по умолчанию?", "514|udp 514|514 udp", "<b>UDP 514</b>.", "порт"),
        task("mz4", "PRI для Facility 20 и Severity 5?", "165", "20 × 8 + 5 = <b>165</b>.", "PRI")])
    _t("Итоговые задачи · 2", "IP SLA и резервное копирование.", [
        task("mz5", "Frequency IP SLA по умолчанию, секунд?", "10", "По умолчанию <b>10 секунд</b> (диапазон 1–604800).", "секунд"),
        task("mz6", "Максимум локальных копий для count-backup?", "100", "count-backup — от 1 до <b>100</b>.", "число"),
        task("mz7", "Интервал auto по умолчанию, минут?", "780", "По умолчанию <b>780 минут</b>.", "минут"),
        task("mz8", "Номер TLV vendor-specific?", "127", "vendor-specific TLV — <b>127</b>.", "номер")])

    _s("Тренажёр: уровни Severity", "Разложите уровни важности: 0–4 — сбои (затронута работа устройства), 5–7 — остальные.",
       K.sorter("ms1", ["Сбои (0–4)", "Не сбои (5–7)"], [("emerg", 0), ("alert", 0), ("crit", 0), ("error", 0), ("warning", 0),
                                                         ("notice", 1), ("info", 1), ("debug", 1)], "Нажмите на карточку, затем на группу."))
    _s("Тренажёр: какой инструмент", "Что для чего используется?",
       K.sorter("ms2", ["LLDP", "SPAN/RSPAN", "Syslog", "IP SLA", "archive"], [
           ("сосед на другом конце кабеля", 0), ("TLV и LLDPDU", 0), ("копия трафика на анализатор", 1), ("port monitor interface", 1),
           ("Facility и Severity", 2), ("UDP 514", 2), ("SENDER и RESPONDER", 3), ("задержка, джиттер, потери", 3),
           ("by-commit", 4), ("flash:backup/", 4)], "Разложите признаки по инструментам."))

    slide("Тренажёр CLI: LLDP, SPAN, Syslog", sc(head("Тренажёр <em>CLI</em>: LLDP, SPAN, Syslog",
        "Выполните задание, примените commit и confirm. «Проверить в работе» — что произойдёт."),
        grow("g", col(K.sim("mon", [0, 1, 2, 3], send="Проверить в работе")))))
    slide("Тренажёр CLI: archive и IP SLA", sc(head("Тренажёр <em>CLI</em>: резервное копирование и IP SLA",
        "Настройте резервное копирование или IP SLA-тест."), grow("g", col(K.sim("mon", [4, 5], send="Проверить в работе")))))

    _q("Тест · 1", "LLDP.", [
        quiz("На каком уровне OSI работает LLDP?", ["L1", "L2", "L3", "L4"], 1, "Протокол уровня L2."),
        quiz("LLDP на устройствах Eltex по умолчанию…", ["включён", "выключен", "включён только на ESR", "включён на uplink"], 1,
             "Деактивирован из соображений безопасности."),
        quiz("Какой командой включается LLDP на ESR?", ["lldp run", "lldp enable", "lldp start", "ip lldp"], 1,
             "На MES — lldp run, на ESR — lldp enable."),
        quiz("Где отключать передачу LLDP?", ["на портах к оконечным устройствам и чужим сетям", "на uplink к ядру", "нигде", "на всех портах"], 0,
             "Чтобы минимизировать возможности компрометации.")])
    _q("Тест · 2", "Зеркалирование.", [
        quiz("Что такое SPAN?", ["удалённое зеркалирование через VLAN", "локальное зеркалирование на порт этого же устройства",
                                 "протокол журнала", "тест канала"], 1, "Switch Port Analyzer."),
        quiz("Что означает ключ rx в port monitor?", ["только входящий", "только исходящий", "оба направления", "VLAN"], 0,
             "rx — входящий, tx — исходящий."),
        quiz("Через что передаётся трафик RSPAN?", ["через отдельную VLAN", "через Syslog", "через IP SLA", "через TFTP"], 0,
             "Трафик дублируется в отдельный VLAN."),
        quiz("Когда начнётся зеркалирование на ESR?", ["сразу", "после commit и confirm", "после перезагрузки", "после show"], 1,
             "После применения и подтверждения.")])
    _q("Тест · 3", "Syslog.", [
        quiz("Какой документ описывает Syslog?", ["RFC 5424", "RFC 1918", "RFC 2784", "RFC 1195"], 0, "RFC5424 от 2009 года."),
        quiz("Какой уровень важнее?", ["7 debug", "6 info", "0 emerg", "4 warning"], 2, "Чем меньше число, тем важнее событие."),
        quiz("Как вычисляется PRI?", ["Facility × 8 + Severity", "Severity × 8 + Facility", "Facility + Severity", "Facility × Severity"], 0,
             "PRI = Facility Number * 8 + Severity Number."),
        quiz("Куда ESR без настроек пишет критические события?", ["flash:critlog/log", "tmpsys:syslog/debug", "USB", "tftp"], 0,
             "Файл flash:critlog/log.")])
    _q("Тест · 4", "IP SLA.", [
        quiz("Что измеряет ICMP-режим IP SLA?", ["только двунаправленную задержку", "потери и джиттер в обе стороны", "дубликаты",
                                                 "порядок пакетов"], 0, "В ICMP-режиме — только двунаправленная задержка."),
        quiz("Кто инициирует тест?", ["RESPONDER", "SENDER", "NTP-сервер", "Syslog-сервер"], 1, "SENDER инициирует, RESPONDER отвечает."),
        quiz("Что обязательно для SENDER и RESPONDER?", ["синхронизация по NTP", "одинаковый hostname", "одна VLAN", "RSPAN"], 0,
             "Должны быть синхронизированы по NTP."),
        quiz("Какой командой включается RESPONDER на ESR?", ["ip sla responder eltex", "ip sla sender", "ip sla schedule", "responder enable"], 0,
             "ip sla responder eltex (или cisco).")])
    _q("Тест · 5", "Резервное копирование.", [
        quiz("Какой тип сохраняет копию и на ESR, и на сервер?", ["local", "remote", "both", "auto"], 2, "both — и туда, и туда."),
        quiz("Что делает by-commit?", ["копия при каждом commit", "копия раз в сутки", "удаляет копии", "сохраняет на USB"], 0,
             "Новая копия при каждом применении commit."),
        quiz("Куда пишутся локальные копии?", ["flash:backup/", "tmpsys:syslog/", "USB://", "system:candidate-config"], 0, "Раздел flash:backup/."),
        quiz("Какие протоколы поддерживает path?", ["TFTP, FTP, SFTP, SCP", "только TFTP", "HTTP и HTTPS", "SMB"], 0,
             "4 протокола передачи файлов.")])

    slide("Что запомнить", sc(head("Что <em>запомнить</em>", "Главное из лекции."), grow("g2",
        col(step(card("LLDP", li(["L2-обнаружение соседей; на Eltex выключен по умолчанию.",
                                  "MES: lldp run; ESR: lldp enable; на портах — lldp receive / transmit.",
                                  "30 с интервал, hold multiplier 4; TLV базовые и дополнительные."]), "cy")),
            step(card("Зеркалирование", li(["SPAN — на порт этого устройства: port monitor interface … rx|tx.",
                                            "RSPAN — через отдельную VLAN: port monitor remote vlan, port monitor remote."]), "am"))),
        col(step(card("Syslog", li(["RFC 5424, UDP 514; PRI = Facility × 8 + Severity.", "Severity 0 emerg … 7 debug; 0–4 — сбои.",
                                    "syslog file / host, logging …; show syslog configuration."]), "lm")),
            step(card("IP SLA и резервные копии", li(["SENDER → RESPONDER; ICMP или UDP; NTP обязателен.",
                                                      "archive: type local|remote|both, path, count-backup, time-period, auto, by-commit."]),
                      "mg"))))))
    slide("Финал", sc(head("<em>Спасибо</em> за внимание", "Мониторинг и управление"), grow("g2",
        col(step(card("Что дальше", li(["Повторите тренажёр CLI: LLDP, SPAN, Syslog, archive, IP SLA."]), "cy"))),
        col(step(card("Контакты", tags(tag("VKontakte", "v"), tag("Telegram")) + p("Вопросы по лекции и лабораторным — пишите."), "mg"))))))
